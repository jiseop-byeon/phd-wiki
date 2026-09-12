---
title: "25.6 Describing a Robot: URDF, TF2 and RViz"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Write a robot description in Xacro, publish its frames with robot_state_publisher, read the resulting transform tree with view_frames, tf2_echo and RViz, and diagnose the two transform errors every beginner meets."
mastery-when: "Go deeper when you are writing the localisation or odometry component that owns the map and odom edges, rather than consuming the tree they produce."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to describe a robot, publish its frames correctly, and find out who is publishing a frame wrongly. Not enough to write a state estimator that owns `map`.
> **Working** — 로봇을 기술하고 프레임을 올바르게 publish하며, 어떤 프레임을 누가 잘못 내보내는지 찾아낼 정도. `map`을 소유하는 상태 추정기를 작성할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> A sourced **ROS 2 Jazzy Jalisco on Ubuntu 24.04** installation and a workspace you can build in ([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). Rigid-body transforms help but are not required first: [[02-foundations/se3-geometry|3D Geometry & SE(3)]] and [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**와 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). 강체 변환은 도움이 되지만 먼저 읽을 필요는 없다: [[02-foundations/se3-geometry|3D Geometry & SE(3)]], [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].

### 1. Why a robot needs a machine-readable description

Everything after this page needs to know where things are. A planner needs to know that the gripper is 0.8 m from the base when the elbow is at 1.2 rad. A collision checker needs shapes. A physics engine needs masses and inertias. A perception node that gets a point in the camera frame needs to express it in the base frame before the arm can reach for it. RViz needs to know what to draw and where.

You could hard-code all of that in every node. Then the day someone lengthens the forearm by 2 cm, six nodes are wrong and three of them fail silently.

ROS 2's answer splits the problem in two, and the split is the thing to remember:

- **URDF** is the *static* description — which links exist, how they are connected, what they look like, what they weigh. It does not change while the robot runs.
- **TF2** is the *live* answer — where every frame actually is right now, and where it was 0.3 seconds ago when that camera image was captured.

`robot_state_publisher` is the bridge: it reads the URDF once, subscribes to joint angles, and publishes the resulting frames into TF2 continuously.

### 2. URDF: a tree of links and joints

URDF (Unified Robot Description Format) is XML. It has exactly two structural elements.

A **link** is a rigid body. It carries appearance, collision shape and mass properties, and it defines a coordinate frame.

A **joint** connects exactly two links — a `parent` and a `child` — and says how the child may move relative to the parent. Its `<origin xyz="..." rpy="..."/>` is the fixed offset from the parent link's frame to the joint, and it is where most of the geometry of a robot actually lives.

The constraint that follows: **the links and joints must form a tree.** Every link has at most one parent joint; there is exactly one root link; no cycles. A parallel mechanism — a delta robot, a four-bar linkage — cannot be expressed as URDF, and that is a real limitation, not a beginner's misunderstanding. The common workarounds are to model the open chain and close the loop in the physics engine, or to use SDF instead.

Units are SI throughout, per REP 103: metres, radians, kilograms. Frames are right-handed, and the body convention is x forward, y left, z up.

Getting the tree drawn on paper before writing XML saves more time than any other habit on this page. Once it is written, check it:

```bash
sudo apt install liburdfdom-tools
check_urdf my_robot.urdf
```

`check_urdf` parses the file and prints the link tree. If it prints one root and the links you expect, the structure is right; if a link is missing from the printout, its joint is wrong.

### 3. The joint types

| Type | Motion | Needs `<axis>` | Needs `<limit>` | Appears in `joint_states` |
|---|---|---|---|---|
| `fixed` | none | no | no | no |
| `revolute` | rotation about the axis, bounded | yes | yes (`lower`, `upper` in rad, plus `effort`, `velocity`) | yes |
| `continuous` | rotation about the axis, unbounded | yes | no | yes |
| `prismatic` | translation along the axis, bounded | yes | yes (`lower`, `upper` in m, plus `effort`, `velocity`) | yes |
| `planar` | two translations plus a rotation in a plane | yes | — | not as one number |
| `floating` | unconstrained, six degrees of freedom | no | — | not as one number |

Three practical notes. A wheel is `continuous`, not `revolute`, because a bounded wheel stops rolling at its limit. A `revolute` joint without a `<limit>` tag will not parse. And `fixed` joints are not decoration — a sensor mount is a `fixed` joint, and that is what makes the sensor's data transformable into the base frame at all.

`planar` and `floating` cannot be described by a single scalar, so `joint_state_publisher` and `robot_state_publisher` do not handle them the way they handle the other three movable types; a floating base is normally published as a transform by an odometry or localisation node instead.

### 4. Visual, collision and inertial — and the mesh that wrecks your planner

A link has up to three sub-elements, and beginners conflate them:

```xml
<link name="forearm">
  <visual>
    <origin xyz="0 0 0.2"/>
    <geometry><mesh filename="package://my_robot/meshes/forearm.dae"/></geometry>
    <material name="grey"/>
  </visual>
  <collision>
    <origin xyz="0 0 0.2"/>
    <geometry><cylinder radius="0.04" length="0.4"/></geometry>
  </collision>
  <inertial>
    <mass value="1.2"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</link>
```

- `<visual>` is what a human sees. Its accuracy costs nothing but rendering.
- `<collision>` is what the collision checker and the physics engine query. Its accuracy costs *every query*.
- `<inertial>` is mass and the 3×3 rotational inertia tensor, symmetric so six numbers suffice. Only simulation and dynamics use it.

**The trap: reusing the detailed visual mesh as the collision geometry.** The official URDF tutorial states the reason plainly — collision detection between two meshes is far more computationally complex than between two primitives. A motion planner samples and checks thousands of configurations per query, and a physics engine runs a narrow-phase check every step at 1 kHz. A 50,000-triangle CAD export in `<collision>` multiplies that cost by orders of magnitude, and the symptom is not an error: it is a planner that times out, a simulation whose real-time factor sits at 0.05, and a controller that misses its period. Use primitives — box, cylinder, sphere — or a convex decomposition, and make them slightly larger than the visual rather than slightly smaller. The same element doubles as a safety envelope: a cylinder that encases a sensor head keeps planned paths away from it.

On inertia: the tutorial's guidance is that a matrix with `ixx`/`iyy`/`izz` of `1e-3` or smaller is a reasonable default for a mid-sized link, and that the identity matrix is a particularly bad choice — it corresponds to a 0.1 m box weighing 600 kg. Inertias of zero or near-zero make a simulated model collapse without warning, with every link's origin snapping to the world origin. If you ever see that in Gazebo, look at `<inertial>` first.

### 5. Xacro: properties, macros, and how it is expanded

A URDF for a real robot repeats itself relentlessly: the same cylinder written in `<visual>` and `<collision>`, the same leg written twice with a sign flipped, joint origins computed by hand from link lengths. Xacro is an XML macro language that removes that repetition. It gives you three things: **properties** (constants), **arithmetic**, and **macros**.

The file must declare the namespace, or nothing expands:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">
  <xacro:property name="link_len" value="0.4"/>
  <cylinder radius="0.03" length="${link_len}"/>
  <origin xyz="0 0 ${link_len/2}" rpy="0 ${pi/2} 0"/>
</robot>
```

`${...}` substitutes a property or evaluates an expression; `+ - * /`, unary minus, parentheses, `sin`, `cos` and the constant `pi` are available. Substitution works inside any attribute and composes with literal text, so `<link name="${prefix}_leg"/>` is how you get two similarly named links from one macro.

Macros take parameters, and a parameter prefixed with `*` is an XML *block* that the caller supplies and `<xacro:insert_block>` inserts:

```xml
<xacro:macro name="default_inertial" params="mass">
  <inertial>
    <mass value="${mass}"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</xacro:macro>
<xacro:default_inertial mass="10"/>
```

> [!warning] The silent Xacro failure
> A typo in a macro name is loud, not silent: `handle_macro_call` raises `XacroException("unknown macro name: ...")`, xacro exits non-zero and produces no output at all. What *is* silent is a typo in a property or an argument name, which expands to an empty string and leaves you with a link at the origin or a joint with a zero-length offset. Expand to a file and read it whenever a number looks wrong rather than whenever something is missing.

Xacro is a preprocessor: nothing downstream understands it. Expansion happens one of two ways.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
```

That is the debugging path — run it and read the output whenever the robot is not what you expected. The production path runs xacro inside the launch file so the URDF is never stale on disk, as the official `urdf_launch` package does:

```python
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
```

The `value_type=str` matters: without it the parameter is guessed at, and a URDF that begins with a number or parses as something else will arrive at the wrong type.

### 6. What robot_state_publisher and joint_state_publisher_gui actually do

`robot_state_publisher` is the node that turns the static description plus live joint angles into live frames. Per its documentation:

- It takes the URDF through the `robot_description` **parameter**, which must be set at startup or the node fails to start.
- It subscribes to `joint_states` (`sensor_msgs/msg/JointState`).
- **Fixed** joints are published once at startup to `/tf_static`, on a transient-local topic so any later subscriber still receives them.
- **Movable** joints are published to `/tf` whenever the relevant joint appears in a `joint_states` message, rate-limited by the `publish_frequency` parameter, which defaults to 20.0 Hz.
- It also republishes the URDF itself on a transient-local `robot_description` topic, which is how RViz and `joint_state_publisher` get the model without being given the file.
- `frame_prefix` (default empty) prefixes every published frame, which is the standard way to run two identical robots in one graph.

It does *not* invent joint angles. With no `joint_states` publisher, the movable part of the tree never appears, and RViz shows the base link alone. On a real robot the joint states come from the hardware driver or from `ros2_control` ([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). With no robot at all, you supply them by hand:

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

This node reads the model — in ROS 2 it subscribes to the `/robot_description` topic — finds every non-fixed joint and its limits, and gives you one slider per joint. Moving a slider publishes a `JointState` message; `robot_state_publisher` recomputes the chain; RViz redraws. It is a stand-in for a robot, and nothing more: it is a debugging tool, not part of a running system. Leaving it in a launch file that also starts a real driver gives you two publishers of `joint_states` fighting each other.

### 7. TF2: the frame tree, and who owns an edge

TF2 is the library that answers "where is frame A relative to frame B, at time t". It is where most newcomer hours are lost, so be precise about four things.

**Frames form a tree, not a graph.** Each frame has exactly one parent and any number of children. There is one root. This is not a style rule; it is what makes a lookup a unique path.

**Direction.** A transform is published as parent → child: `header.frame_id` is the parent, `child_frame_id` is the child. In a lookup, `lookup_transform(target_frame, source_frame, time)` returns the transform that takes data *expressed in* `source_frame` and gives it *expressed in* `target_frame`. The tf2 concept documentation warns explicitly that the published `geometry_msgs/msg/Transform` is the *frame* formulation, which is the inverse of the data formulation — the library inverts as needed while traversing, but this is the sign error you will make.

Composition along the chain is what the tree buys you. For a two-link arm,

$$ {}_{\text{base}}T_{\text{tip}} = {}_{\text{base}}T_{\text{link1}} \cdot {}_{\text{link1}}T_{\text{tip}} $$

and TF2 walks that product for you across any number of edges published by any number of nodes.

**Exactly one publisher may own a given parent–child edge.** Internally tf2 keeps one time-ordered buffer per *child* frame. It is keyed by the child frame alone — not by who sent the data. Two nodes publishing the same edge therefore interleave their samples into one buffer, and a lookup interpolates between whichever neighbouring samples bracket the requested time, regardless of authorship. If the two disagree, the frame alternates between two answers. Section 13 reproduces this on purpose.

**Broadcasting is cheap and local.** Any node can broadcast any edge. Nothing checks, at any point, that the tree you intended is the tree you got. The tools in section 10 are the check.

### 8. Static and dynamic transforms, the buffer, and the time argument

A **static** transform never changes: base to laser mount, base to camera. It goes on `/tf_static`, which is published with transient-local durability, so it is sent once and every later subscriber still receives it. Publish it with the dedicated executable rather than writing code:

```bash
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id mystaticturtle
```

All arguments except `--frame-id` and `--child-frame-id` are optional and default to identity, and `--qx --qy --qz --qw` is accepted instead of roll/pitch/yaw. Note that these are named options in ROS 2, not the bare positional numbers the ROS 1 command used; copying a ROS 1 line here is a common failure.

A **dynamic** transform changes and is stamped every time: odom to base_link, and every movable joint of your arm. It goes on `/tf` and is republished continuously.

A listener does not read those topics directly. It fills a **buffer** — a time-indexed cache, 10 seconds deep by default — and queries it:

```python
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)

t = self.tf_buffer.lookup_transform('base_link', 'link2', Time())
```

The third argument is the part that decides whether your node works.

- `Time()` in Python (`tf2::TimePointZero` in C++) means **the latest available transform**, not "now". This is what you want for a live query, and what the official debugging tutorial gives as the correct fix.
- An actual timestamp — typically `msg.header.stamp` from the sensor message you are transforming — means "where were these frames when this image was taken". This is the whole point of a buffer, and it is what makes a transformed detection correct on a moving robot instead of 100 ms stale.
- `self.get_clock().now()` means "now", and **now has not happened yet** as far as the buffer is concerned. Transforms arrive with a delay. Section 9 is the error this produces.

Add a `timeout` to block briefly rather than fail on the first miss, which is what you want in a startup path:

```python
t = self.tf_buffer.lookup_transform('base_link', 'link2', Time(), timeout=Duration(seconds=0.05))
```

### 9. The two errors everyone meets

**A frame that does not exist.** The message is unambiguous:

```text
"turtle3" passed to lookupTransform argument target_frame does not exist
```

It means what it says. The cause is almost always a typo, a missing `frame_prefix`, or a publisher that has not started yet. Confirm it with `tf2_echo`, which reports the same thing from `canTransform`, and then look at what frames *do* exist with `view_frames`.

**A lookup that would require extrapolation into the future.**

```text
Could not transform turtle2 to turtle1: Lookup would require extrapolation into the future.
Requested time 1630223704.617054 but the latest data is at time 1630223704.616726, when
looking up transform from frame [turtle1] to frame [turtle2]
```

Read the two numbers: the request is *later* than the newest sample in the buffer, here by about 0.3 ms. The buffer will not extrapolate, by design — a made-up transform is worse than no transform. The cause is asking for `now`. The diagnostic is `tf2_monitor`, which reports the delay of the chain between two frames:

```bash
ros2 run tf2_ros tf2_monitor turtle2 turtle1
```

It prints the chain, the net average and maximum delay, and the rate of each broadcaster. If the net delay is 3 ms, then `now` will fail most of the time and `now - 0.1 s` will work — but that is a diagnosis, not a fix. The fix is `Time()` for "latest", or the message's own stamp with a timeout. Reaching for a hard-coded delay means you have papered over a question you have not answered.

The mirror-image error, `Lookup would require extrapolation into the past`, means the request is older than the buffer, which is either a stale sensor stamp or a buffer that needs to be constructed with a longer `cache_time`.

### 10. Looking at the tree: view_frames, tf2_echo and RViz

Three tools, each better at a different question.

```bash
sudo apt install ros-jazzy-tf2-tools ros-jazzy-tf2-ros graphviz
ros2 run tf2_tools view_frames
```

`view_frames` subscribes for five seconds (change it with `--wait-time`), then renders the whole tree with Graphviz. In Jazzy it writes `frames_<date>_<time>.gv` and `frames_<date>_<time>.pdf` into the current directory — not the `frames.pdf` that older tutorials mention — and `-o NAME` overrides the name. It is the only tool that answers "what is the shape of my tree", and each edge is labelled with the broadcaster, the average rate, the buffer length, and the most recent and oldest transform times. Those labels are the diagnostic content; read them, not just the arrows.

```bash
ros2 run tf2_ros tf2_echo [source_frame] [target_frame]
```

`tf2_echo` prints one edge or chain repeatedly: translation, rotation as quaternion and as RPY in radians and degrees, and the full 4×4 matrix. Use it to answer "is this number right", and to catch a sign or axis error that looks fine in a picture.

RViz answers "does this look like my robot". Start it, set **Fixed Frame** to a frame that actually exists (with `Fixed Frame` set to something unpublished, every display fails at once and the errors point everywhere but the cause), then add two displays:

- **RobotModel**, whose *Description Source* is `Topic` by default. The *Description Topic* field has **no default** — RViz renames the inherited topic property but sets no value — so pick `/robot_description` from its dropdown. Until you do, the display is simply empty and says nothing, which is the commonest "my robot does not show up" report. The topic is transient-local, so it needs no file path once `robot_state_publisher` is running. Its *Visual Enabled* and *Collision Enabled* checkboxes draw the two geometries separately, which is how you see that your collision shape is the 50,000-triangle mesh. *Mass* and *Inertia* draw the inertial properties.
- **TF**, which draws every frame with axes, names, and arrows from child to parent. *Frames* lists them all with checkboxes, *Tree* shows the parent–child structure, and *Frame Timeout* controls how long a frame that has stopped updating stays drawn before fading to grey and disappearing — a frame fading out in RViz means its publisher died.

### 11. REP 105: map, odom and base_link

For mobile platforms the frame names and their order are standardised by REP 105, and every navigation stack assumes it:

```text
map --> odom --> base_link
```

- `base_link` is rigidly attached to the robot base, at whatever point on the base is an obvious reference.
- `odom` is a world-fixed frame whose origin is wherever the robot started. The robot's pose in `odom` is **continuous** — it evolves smoothly, with no discrete jumps — but it **drifts without bound**, because it is computed by integrating wheel encoders, visual odometry or an IMU.
- `map` is a world-fixed frame with z up. The robot's pose in `map` does **not drift** over time, because a localisation component keeps recomputing it from sensor observations, but it is **not continuous**: it can jump discretely whenever new sensor information arrives.

That is the trade you cannot escape, and it is why both frames exist. Use `odom` for anything local and short-term — a velocity controller, obstacle avoidance over the next second, anything that would be destabilised by a pose that jumps 30 cm sideways. Use `map` for anything long-term and global — "go to the kitchen" — where drift would eventually put you in the wrong room.

The structure surprises people: intuition says both `map` and `odom` should be parents of `base_link`, but a frame may have only one parent, so REP 105 makes `map` the parent of `odom` instead. The consequence is that the localisation node does not publish the robot's pose directly; it publishes the `map` → `odom` correction, which is the accumulated drift of the odometry. Odometry publishes `odom` → `base_link`. Neither ever publishes the other's edge — that is section 7's rule applied to the most important edges in the system. Everything from `base_link` downward comes from `robot_state_publisher` reading your URDF.

Above `map` sits an optional `earth` frame (ECEF), present only when several robots with separate maps have to be related.

### 12. Exercise: a two-link arm in Xacro, moving in RViz

One sitting. Baseline is ROS 2 Jazzy on Ubuntu 24.04.

```bash
sudo apt install ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui ros-jazzy-robot-state-publisher ros-jazzy-rviz2 ros-jazzy-tf2-tools liburdfdom-tools graphviz
```

Write `two_link_arm.urdf.xacro`:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">

  <material name="grey">
    <color rgba="0.6 0.6 0.6 1"/>
  </material>

  <xacro:property name="link_len" value="0.4"/>
  <xacro:property name="link_rad" value="0.03"/>

  <xacro:macro name="default_inertial" params="mass">
    <inertial>
      <mass value="${mass}"/>
      <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
    </inertial>
  </xacro:macro>

  <xacro:macro name="arm_link" params="name">
    <link name="${name}">
      <visual>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
      </collision>
      <xacro:default_inertial mass="1.0"/>
    </link>
  </xacro:macro>

  <link name="base_link"/>
  <xacro:arm_link name="link1"/>
  <xacro:arm_link name="link2"/>

  <joint name="shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  </joint>

  <joint name="elbow" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 ${link_len}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="2.0" effort="10.0" velocity="1.0"/>
  </joint>

</robot>
```

Expand it and check the structure before running anything:

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
check_urdf two_link_arm.urdf
```

Read the expanded URDF once. The two `arm_link` calls produced two full link definitions, and `${link_len/2}` became `0.2`. That is all xacro is.

Now `display.launch.py`, following the `urdf_launch` pattern from section 5:

```python
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', output='screen'),
    ])
```

```bash
ros2 launch ./display.launch.py
```

In RViz set **Fixed Frame** to `base_link`, add a **RobotModel** display and a **TF** display. Then:

1. Drag the two sliders. The cylinders move and the TF axes move with them. `shoulder` rotates about y, so the arm swings in the x–z plane.
2. `ros2 topic echo /joint_states` — two names, two positions, changing as you drag.
3. `ros2 topic echo /tf_static --once` — nothing. Every joint here is movable, so there are no static transforms. Add a `fixed` joint for a sensor mount and it appears.
4. `ros2 run tf2_ros tf2_echo base_link link2` with both sliders at zero. The translation should be `[0, 0, 0.4]` — `link2`'s origin sits at the *end* of `link1`, which is what the elbow joint's `<origin>` says. Move the shoulder to 1.57 and watch x and z swap.
5. `ros2 run tf2_tools view_frames`, then open the generated PDF. Three frames, two edges, each labelled with `robot_state_publisher` as broadcaster and a rate near 10 Hz. That 10 is `joint_state_publisher`'s `rate` default — `robot_state_publisher` only republishes what it receives, and its own `publish_frequency` default of 20 Hz is a *maximum*, not a target.

You are done when you can predict, before looking, what `tf2_echo base_link link2` will print for a given pair of slider values.

### 13. The failure to diagnose: two publishers on one edge

Leave the exercise running and add a second owner of `base_link` → `link1`. Use a second `robot_state_publisher`, not a `static_transform_publisher`: the static one publishes once onto a latched `/tf_static` and then only spins, which produces a single glitch rather than the continuous fight, and none of the tells below appear.

```bash
# a SECOND robot_state_publisher on the same description, so both write /tf continuously
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro two_link_arm.urdf.xacro)"
```

**Symptom.** In RViz, `link1` and everything below it — `link2`, the whole rest of the arm — jitters or snaps between two poses. Moving the shoulder slider moves the arm but it keeps flicking back towards the static pose. A listener node computing a grasp from this tree gets a different answer each cycle, and averaging makes it worse, not better. Nothing logs an error. Both publishers are behaving exactly as told.

**Mechanism.** From section 7: tf2 stores one time-ordered buffer per child frame, keyed by the child frame alone. Both publishers' samples land in the buffer for `link1`, and a lookup interpolates between whichever neighbouring samples bracket the requested time — which is sometimes a pair from `robot_state_publisher` and sometimes a pair straddling a `static_transform_publisher` sample. The mixed static/dynamic case is even worse: the buffer type differs for static and dynamic frames, so alternating messages of the two kinds make tf2 reallocate the frame's cache repeatedly, discarding history.

**The command that finds it.**

```bash
ros2 run tf2_tools view_frames
```

Open the PDF and read the `base_link` → `link1` edge label:

- **Average rate** is roughly the sum of both publishers, not the rate you expect from one. An edge you believe is published at 20 Hz showing 30 or 120 Hz is the tell.
- **Broadcaster** names only *one* node. tf2 records the authority of the most recent successful insert and overwrites it, so the label flickers between the two names each time you regenerate the diagram. Running `view_frames` twice and getting two different broadcasters for the same edge is proof.

Then confirm which nodes are actually publishing:

```bash
ros2 topic info /tf --verbose
ros2 topic info /tf_static --verbose
```

`--verbose` lists every endpoint by node name ([[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]] introduced the flag). Two publishers on `/tf` where you expected one, or a `static_transform_publisher` on `/tf_static` claiming a frame your URDF also owns, ends the investigation.

**The fix is architectural, not a tuning knob.** Decide which node owns each edge and delete the other publisher. The realistic versions of this bug are: a `static_transform_publisher` left in a launch file for a frame the URDF later gained a joint for; two launch files each starting their own `robot_state_publisher`; a localisation node and a bag playback both publishing `map` → `odom`; or a driver publishing `odom` → `base_link` while an EKF publishes the same edge. The last one is the reason robot_localization publishes `map` → `odom` and tells the wheel driver to stop broadcasting.

### 14. What this page does not cover

Driving the joints for real — controllers, hardware interfaces, and the Gazebo Harmonic side of the URDF — is [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]], which also covers the `<transmission>` and `<ros2_control>` tags this page skipped, and the SDF format Gazebo uses natively. Timestamps, the `use_sim_time` parameter and the executor that decides when your TF callback runs are [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] — and TF2's transient-local `/tf_static` is a QoS story the moment a subscriber gets it wrong. Packaging the description properly, with `package://` mesh paths that resolve after installation, is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. The mathematics that `lookup_transform` is doing for you is [[02-foundations/se3-geometry|3D Geometry & SE(3)]] and [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]]. Everything above this sits in [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Tutorials/Intermediate/URDF: Building a movable robot model; Adding physical and collision properties; Using Xacro to clean up your code; Using URDF with `robot_state_publisher`.
- ROS 2 Jazzy documentation — Tutorials/Intermediate/Tf2: Introducing tf2; Writing a static broadcaster (Python); Debugging tf2 problems.
- ROS 2 Jazzy documentation — Concepts/Intermediate: Tf2 (transform direction and `lookupTransform` semantics).
- `robot_state_publisher` package README (jazzy) — parameters, published and subscribed topics.
- `geometry2` source (jazzy) — `tf2/src/buffer_core.cpp` and `tf2/src/cache.cpp` for per-child-frame buffering and broadcaster recording; `tf2_tools/view_frames.py` for output file naming and edge labels.
- `rviz_default_plugins` source (jazzy) — RobotModel and TF display properties.
- REP 105, Coordinate Frames for Mobile Platforms; REP 103, Standard Units of Measure and Coordinate Conventions.
- `urdf_launch` package — `description.launch.py` and `display.launch.py`.

> [!question]- Self-check · Answer
> **1. Your node calls `lookup_transform('base_link', 'camera_link', self.get_clock().now())` and logs "extrapolation into the future" most cycles. What is wrong, and what are the two correct fixes?** It is asking for a time the buffer has not received data for yet; transforms always arrive with some delay. Use `Time()` (`tf2::TimePointZero`) to get the latest available transform, or — better, when transforming sensor data — use that message's own `header.stamp`, with a short `timeout` so the call waits rather than failing on the first miss. Subtracting a hard-coded 0.1 s is a diagnostic, not a fix.
> **2. Why can't `map` and `odom` both be parents of `base_link`, and what does the localisation node publish instead?** A tf2 frame has exactly one parent, which is what makes a lookup a unique path. REP 105 therefore chains `map` → `odom` → `base_link`: odometry owns `odom` → `base_link`, and localisation publishes the `map` → `odom` correction, which is the accumulated odometry drift. `odom` is continuous but drifts; `map` does not drift but jumps.
> **3. Your planner takes 40 seconds per query on a robot whose URDF loads fine and looks right in RViz. Where do you look first?** The `<collision>` elements. If they reuse the detailed visual meshes, every one of the thousands of collision checks per query is mesh-versus-mesh instead of primitive-versus-primitive. Turn off *Visual Enabled* and turn on *Collision Enabled* in RViz's RobotModel display to see what the checker is actually using, then replace the meshes with primitives or a convex decomposition.
> **4. `view_frames` shows one broadcaster per edge. How can it still be hiding two publishers of the same edge?** tf2 stores the authority of the most recent successful insert and overwrites it, so the label names whichever node wrote last — regenerate the diagram and it may name the other one. The reliable signal on the same label is the average rate: an edge you publish at 20 Hz reporting 30 or 120 Hz has more than one owner. Confirm with `ros2 topic info /tf --verbose` and `/tf_static`.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 로봇을 기술하고 프레임을 올바르게 publish하며, 어떤 프레임을 누가 잘못 내보내는지 찾아낼 정도. `map`을 소유하는 상태 추정기를 작성할 정도는 아니다.
> **Working** — enough to describe a robot, publish its frames correctly, and find who publishes a frame wrongly.

> [!note] 선수 지식 · Prerequisites
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**와 빌드할 수 있는 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). 강체 변환은 도움이 되지만 선행 조건은 아니다: [[02-foundations/se3-geometry|3D Geometry & SE(3)]], [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].
> A sourced ROS 2 Jazzy on Ubuntu 24.04 and a buildable workspace; rigid-body transforms help but are not required.

### 1. 로봇에 기계가 읽을 수 있는 기술(description)이 필요한 이유

이 페이지 이후의 모든 것은 물건이 어디에 있는지를 알아야 한다. 플래너는 팔꿈치가 1.2 rad일 때 그리퍼가 베이스에서 0.8 m라는 것을 알아야 하고, 충돌 검사기는 형상을, 물리 엔진은 질량과 관성을 필요로 한다. 카메라 프레임의 점을 받은 인식 노드는 팔이 뻗기 전에 그것을 base 프레임으로 옮겨야 한다. RViz는 무엇을 어디에 그릴지 알아야 한다.

이걸 노드마다 하드코딩할 수는 있다. 그러면 누군가 전완 길이를 2 cm 늘린 날 여섯 개 노드가 틀리고 그중 셋은 조용히 실패한다.

ROS 2의 답은 문제를 둘로 나눈다. 그 분할이 기억할 대상이다.

- **URDF**는 *정적* 기술이다 — 어떤 링크가 있고, 어떻게 연결되고, 어떻게 생겼고, 무게가 얼마인지. 로봇이 도는 동안 바뀌지 않는다.
- **TF2**는 *실시간* 답이다 — 지금 모든 프레임이 실제로 어디에 있는지, 그리고 저 카메라 이미지가 찍힌 0.3초 전에는 어디에 있었는지.

`robot_state_publisher`가 다리다. URDF를 한 번 읽고, 조인트 각도를 구독하고, 그 결과 프레임을 TF2로 계속 내보낸다.

### 2. URDF: 링크와 조인트의 트리

URDF(Unified Robot Description Format)는 XML이다. 구조 요소는 정확히 둘이다.

**링크(link)** 는 강체다. 외형, 충돌 형상, 질량 특성을 담고, 좌표 프레임을 정의한다.

**조인트(joint)** 는 정확히 두 링크 — `parent`와 `child` — 를 잇고, 자식이 부모에 대해 어떻게 움직일 수 있는지 말한다. `<origin xyz="..." rpy="..."/>`는 부모 링크 프레임에서 조인트까지의 고정 오프셋이며, 로봇 기하의 대부분이 실제로 여기에 들어 있다.

여기서 따라오는 제약: **링크와 조인트는 트리를 이루어야 한다.** 모든 링크는 부모 조인트를 최대 하나 갖고, 루트 링크는 정확히 하나이며, 순환은 없다. 델타 로봇이나 4절 링크 같은 병렬 기구는 URDF로 표현할 수 없다. 이것은 초심자의 오해가 아니라 실제 한계다. 흔한 우회는 열린 사슬로 모델링하고 물리 엔진에서 루프를 닫거나, SDF를 쓰는 것이다.

단위는 REP 103에 따라 전부 SI다: 미터, 라디안, 킬로그램. 프레임은 오른손 좌표계이고, 본체 관례는 x 전방, y 좌측, z 상방이다.

XML을 쓰기 전에 트리를 종이에 그려 두는 습관이 이 페이지의 어떤 것보다 시간을 아껴 준다. 다 썼으면 확인한다.

```bash
sudo apt install liburdfdom-tools
check_urdf my_robot.urdf
```

`check_urdf`는 파일을 파싱하고 링크 트리를 찍는다. 루트 하나와 기대한 링크들이 나오면 구조는 맞다. 출력에서 링크가 빠져 있으면 그 조인트가 틀린 것이다.

### 3. 조인트 타입

| 타입 | 운동 | `<axis>` 필요 | `<limit>` 필요 | `joint_states`에 등장 |
|---|---|---|---|---|
| `fixed` | 없음 | 아니오 | 아니오 | 아니오 |
| `revolute` | 축 둘레 회전, 제한 있음 | 예 | 예 (`lower`, `upper`는 rad, 그리고 `effort`, `velocity`) | 예 |
| `continuous` | 축 둘레 회전, 무제한 | 예 | 아니오 | 예 |
| `prismatic` | 축 방향 병진, 제한 있음 | 예 | 예 (`lower`, `upper`는 m, 그리고 `effort`, `velocity`) | 예 |
| `planar` | 평면 안에서 병진 둘 + 회전 하나 | 예 | — | 숫자 하나로는 아님 |
| `floating` | 구속 없음, 6자유도 | 아니오 | — | 숫자 하나로는 아님 |

실무 메모 셋. 바퀴는 `revolute`가 아니라 `continuous`다. 제한이 걸린 바퀴는 한계에서 구르기를 멈춘다. `<limit>` 태그 없는 `revolute`는 파싱되지 않는다. 그리고 `fixed`는 장식이 아니다. 센서 마운트가 `fixed` 조인트이고, 그것이 있어야 센서 데이터를 base 프레임으로 옮길 수 있다.

`planar`와 `floating`은 스칼라 하나로 기술할 수 없어서, `joint_state_publisher`와 `robot_state_publisher`가 나머지 가동 타입처럼 다루지 않는다. 부유 베이스는 보통 오도메트리나 위치추정 노드가 변환으로 publish한다.

### 4. visual, collision, inertial — 그리고 플래너를 망치는 메시

링크는 하위 요소를 최대 셋 갖는다. 초심자는 이 셋을 뭉뚱그린다.

```xml
<link name="forearm">
  <visual>
    <origin xyz="0 0 0.2"/>
    <geometry><mesh filename="package://my_robot/meshes/forearm.dae"/></geometry>
    <material name="grey"/>
  </visual>
  <collision>
    <origin xyz="0 0 0.2"/>
    <geometry><cylinder radius="0.04" length="0.4"/></geometry>
  </collision>
  <inertial>
    <mass value="1.2"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</link>
```

- `<visual>`은 사람이 보는 것이다. 정밀해도 렌더링 비용뿐이다.
- `<collision>`은 충돌 검사기와 물리 엔진이 질의하는 것이다. 정밀함의 대가를 *질의마다* 치른다.
- `<inertial>`은 질량과 3×3 회전 관성 텐서다. 대칭이라 여섯 수면 충분하다. 시뮬레이션과 동역학만 쓴다.

**함정: 정밀한 visual 메시를 collision 형상으로 재사용하는 것.** 공식 URDF 튜토리얼이 이유를 분명히 적는다 — 메시 대 메시 충돌 검사는 원시 도형 둘 사이보다 계산 복잡도가 훨씬 크다. 모션 플래너는 질의마다 수천 개 구성을 샘플링해 검사하고, 물리 엔진은 매 스텝 1 kHz로 좁은 단계 검사를 돈다. 삼각형 5만 개짜리 CAD 출력이 `<collision>`에 들어가면 그 비용이 자릿수 단위로 뛰고, 증상은 에러가 아니다. 시간 초과하는 플래너, 실시간 계수 0.05에 머무는 시뮬레이션, 주기를 놓치는 제어기다. 원시 도형(상자, 원기둥, 구)이나 볼록 분해를 쓰고, visual보다 약간 작게가 아니라 약간 크게 잡아라. 같은 요소가 안전 여유로도 쓰인다. 센서 헤드를 감싸는 원기둥은 계획 경로를 그 근처에서 떼어 놓는다.

관성에 대해: 튜토리얼의 지침은 중간 크기 링크에 `ixx`/`iyy`/`izz`를 `1e-3` 이하로 두는 것이 합리적 기본값이고, 단위 행렬은 특히 나쁜 선택이라는 것이다. 단위 행렬은 한 변 0.1 m에 600 kg인 상자에 해당한다. 관성이 0이거나 0에 가까우면 시뮬레이션 모델이 경고 없이 붕괴하고 모든 링크 원점이 월드 원점으로 몰린다. Gazebo에서 그 광경을 보면 `<inertial>`부터 보라.

### 5. Xacro: property, macro, 그리고 전개 방식

실제 로봇의 URDF는 지독하게 반복된다. 같은 원기둥이 `<visual>`과 `<collision>`에 두 번, 같은 다리가 부호만 바뀌어 두 번, 조인트 원점은 링크 길이로 손계산. Xacro는 그 반복을 없애는 XML 매크로 언어다. **property**(상수), **산술**, **macro** 셋을 준다.

네임스페이스를 선언해야 하고, 아니면 아무것도 전개되지 않는다.

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">
  <xacro:property name="link_len" value="0.4"/>
  <cylinder radius="0.03" length="${link_len}"/>
  <origin xyz="0 0 ${link_len/2}" rpy="0 ${pi/2} 0"/>
</robot>
```

`${...}`는 property를 치환하거나 식을 계산한다. `+ - * /`, 단항 마이너스, 괄호, `sin`, `cos`, 상수 `pi`를 쓸 수 있다. 치환은 어떤 속성 안에서든 되고 리터럴 문자열과 합쳐지므로, `<link name="${prefix}_leg"/>`가 매크로 하나로 비슷한 이름의 링크 둘을 얻는 방법이다.

매크로는 파라미터를 받고, 이름 앞에 `*`를 붙인 파라미터는 호출자가 넘기는 XML *블록*이며 `<xacro:insert_block>`이 삽입한다.

```xml
<xacro:macro name="default_inertial" params="mass">
  <inertial>
    <mass value="${mass}"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</xacro:macro>
<xacro:default_inertial mass="10"/>
```

> [!warning] 조용한 Xacro 실패
> 매크로 이름 오타는 조용하지 않고 시끄럽다. `handle_macro_call`이 `XacroException("unknown macro name: ...")`을 던지고, xacro는 0이 아닌 값으로 종료하며 출력물을 아예 내지 않는다. 정작 조용한 것은 property나 인자 이름의 오타다. 빈 문자열로 전개되어 링크가 원점에 놓이거나 조인트 오프셋이 0이 된 URDF가 남는다. 무언가 없을 때가 아니라 숫자가 이상할 때 파일로 전개해서 읽어라.

Xacro는 전처리기다. 하류의 어떤 것도 이해하지 못한다. 전개는 두 방식 중 하나다.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
```

이쪽이 디버깅 경로다. 로봇이 기대와 다를 때마다 실행해서 출력을 읽어라. 운영 경로는 launch 파일 안에서 xacro를 돌려 디스크의 URDF가 낡지 않게 한다. 공식 `urdf_launch` 패키지가 하는 방식이다.

```python
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
```

`value_type=str`이 중요하다. 없으면 파라미터 타입이 추정되고, 숫자로 시작하거나 다른 것으로 파싱되는 URDF는 엉뚱한 타입으로 도착한다.

### 6. robot_state_publisher와 joint_state_publisher_gui가 실제로 하는 일

`robot_state_publisher`는 정적 기술과 실시간 조인트 각도를 실시간 프레임으로 바꾸는 노드다. 문서에 따르면,

- URDF를 `robot_description` **파라미터**로 받는다. 시작 시점에 설정되어 있지 않으면 노드가 뜨지 않는다.
- `joint_states`(`sensor_msgs/msg/JointState`)를 구독한다.
- **fixed** 조인트는 시작 시 한 번 `/tf_static`으로 나간다. transient local 토픽이라 나중에 붙은 구독자도 받는다.
- **가동** 조인트는 해당 조인트가 `joint_states`에 들어올 때마다 `/tf`로 나가고, `publish_frequency` 파라미터가 상한을 정한다. 기본값은 20.0 Hz.
- URDF 자체도 transient local인 `robot_description` 토픽으로 다시 내보낸다. RViz와 `joint_state_publisher`가 파일 경로 없이 모델을 얻는 경로가 이것이다.
- `frame_prefix`(기본값 빈 문자열)는 publish되는 모든 프레임에 접두사를 붙인다. 동일한 로봇 둘을 한 그래프에 띄우는 표준 방법이다.

조인트 각도를 지어내지는 *않는다*. `joint_states`를 내는 쪽이 없으면 트리의 가동 부분은 아예 나타나지 않고 RViz는 베이스 링크만 보여 준다. 실제 로봇에서는 하드웨어 드라이버나 `ros2_control`이 조인트 상태를 준다([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). 로봇이 아예 없으면 손으로 준다.

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

이 노드는 모델을 읽고 — ROS 2에서는 `/robot_description` 토픽을 구독한다 — 고정이 아닌 모든 조인트와 그 한계를 찾아 조인트마다 슬라이더를 하나씩 준다. 슬라이더를 움직이면 `JointState`가 나가고, `robot_state_publisher`가 사슬을 다시 계산하고, RViz가 다시 그린다. 로봇 대역품일 뿐 그 이상이 아니다. 디버깅 도구이지 운영 시스템의 일부가 아니다. 실제 드라이버를 띄우는 launch 파일에 이것을 남겨 두면 `joint_states` 퍼블리셔 둘이 서로 싸운다.

### 7. TF2: 프레임 트리, 그리고 간선의 소유자

TF2는 "시각 t에 프레임 A가 B에 대해 어디 있는가"에 답하는 라이브러리다. 초심자가 가장 많은 시간을 잃는 곳이므로 네 가지를 정확히 하자.

**프레임은 그래프가 아니라 트리다.** 각 프레임은 부모가 정확히 하나, 자식은 몇이든 가진다. 루트는 하나다. 취향 규칙이 아니라, 조회 경로가 유일해지는 근거다.

**방향.** 변환은 부모 → 자식으로 publish된다. `header.frame_id`가 부모, `child_frame_id`가 자식이다. 조회에서 `lookup_transform(target_frame, source_frame, time)`은 `source_frame`에 *표현된* 데이터를 `target_frame`에 표현된 것으로 바꾸는 변환을 돌려준다. tf2 개념 문서는 publish되는 `geometry_msgs/msg/Transform`이 *프레임* 형식이고 이는 데이터 형식의 역이라고 명시적으로 경고한다. 라이브러리가 순회하면서 알아서 역을 취하지만, 당신이 저지를 부호 오류가 바로 이것이다.

사슬을 따라 합성하는 것이 트리의 이득이다. 2링크 팔이라면

$$ {}_{\text{base}}T_{\text{tip}} = {}_{\text{base}}T_{\text{link1}} \cdot {}_{\text{link1}}T_{\text{tip}} $$

이고, TF2가 몇 개 노드가 내보낸 몇 개 간선이든 이 곱을 대신 계산한다.

**주어진 부모–자식 간선은 퍼블리셔가 정확히 하나여야 한다.** 내부적으로 tf2는 *자식* 프레임마다 시간순 버퍼를 하나씩 둔다. 키는 자식 프레임뿐이고, 누가 보냈는지는 키가 아니다. 같은 간선을 내보내는 두 노드의 샘플은 한 버퍼에 섞여 들어가고, 조회는 요청 시각을 감싸는 이웃 샘플 사이를 저자와 무관하게 보간한다. 둘이 어긋나면 프레임은 두 답 사이를 오간다. 13절에서 일부러 재현한다.

**브로드캐스트는 싸고 국소적이다.** 어느 노드든 어느 간선이든 내보낼 수 있다. 의도한 트리가 실제 트리인지 검사하는 장치는 어디에도 없다. 10절의 도구가 그 검사다.

### 8. 정적 변환과 동적 변환, 버퍼, 그리고 조회의 시간 인자

**정적** 변환은 변하지 않는다. base에서 라이다 마운트, base에서 카메라. `/tf_static`으로 나가고 transient local durability로 publish되므로 한 번 보내면 이후 구독자도 받는다. 코드를 쓰지 말고 전용 실행 파일로 내보내라.

```bash
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id mystaticturtle
```

`--frame-id`와 `--child-frame-id`를 뺀 모든 인자는 선택이고 생략하면 항등이며, roll/pitch/yaw 대신 `--qx --qy --qz --qw`도 받는다. ROS 2에서는 이것이 이름 있는 옵션이지 ROS 1이 쓰던 맨 위치 인자가 아니다. ROS 1 줄을 그대로 복사하는 것이 흔한 실패다.

**동적** 변환은 변하고 매번 타임스탬프가 찍힌다. odom에서 base_link, 그리고 팔의 모든 가동 조인트. `/tf`로 계속 나간다.

리스너는 그 토픽을 직접 읽지 않는다. **버퍼** — 기본 10초 깊이의 시간 색인 캐시 — 를 채우고 거기에 질의한다.

```python
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)

t = self.tf_buffer.lookup_transform('base_link', 'link2', Time())
```

세 번째 인자가 노드의 동작 여부를 가른다.

- Python의 `Time()`(C++의 `tf2::TimePointZero`)은 "지금"이 아니라 **가장 최근에 쓸 수 있는 변환**을 뜻한다. 실시간 질의에 원하는 값이고, 공식 디버깅 튜토리얼이 제시하는 올바른 수정이다.
- 실제 타임스탬프 — 보통 변환하려는 센서 메시지의 `msg.header.stamp` — 는 "이 이미지가 찍혔을 때 프레임들이 어디 있었나"를 뜻한다. 버퍼가 존재하는 이유 전부이고, 움직이는 로봇에서 검출 결과가 100 ms 낡지 않고 맞게 만드는 것이 이것이다.
- `self.get_clock().now()`는 "지금"이고, 버퍼 입장에서 **지금은 아직 오지 않았다**. 변환은 지연을 두고 도착한다. 9절이 이 오류다.

첫 실패에 바로 죽는 대신 잠깐 기다리려면 `timeout`을 준다. 기동 경로에서 원하는 동작이다.

```python
t = self.tf_buffer.lookup_transform('base_link', 'link2', Time(), timeout=Duration(seconds=0.05))
```

### 9. 누구나 만나는 오류 둘

**존재하지 않는 프레임.** 메시지가 명확하다.

```text
"turtle3" passed to lookupTransform argument target_frame does not exist
```

말 그대로다. 원인은 거의 항상 오타, 빠진 `frame_prefix`, 아직 뜨지 않은 퍼블리셔다. `tf2_echo`로 확인하면 `canTransform` 쪽에서 같은 말을 하고, 그다음 `view_frames`로 *존재하는* 프레임을 본다.

**미래로의 외삽을 요구하는 조회.**

```text
Could not transform turtle2 to turtle1: Lookup would require extrapolation into the future.
Requested time 1630223704.617054 but the latest data is at time 1630223704.616726, when
looking up transform from frame [turtle1] to frame [turtle2]
```

두 수를 읽어라. 요청 시각이 버퍼의 최신 샘플보다 *뒤*이고, 여기서는 약 0.3 ms 차이다. 버퍼는 설계상 외삽하지 않는다. 지어낸 변환은 변환이 없는 것보다 나쁘다. 원인은 `now`를 물은 것이다. 진단 도구는 두 프레임 사이 사슬의 지연을 보고하는 `tf2_monitor`다.

```bash
ros2 run tf2_ros tf2_monitor turtle2 turtle1
```

사슬, 평균과 최대 지연, 브로드캐스터별 주기를 찍는다. 순 지연이 3 ms라면 `now`는 대개 실패하고 `now - 0.1초`는 동작한다 — 그러나 그것은 진단이지 해법이 아니다. 해법은 "최신"을 뜻하는 `Time()`이거나, 메시지 자신의 타임스탬프에 timeout을 붙이는 것이다. 하드코딩한 지연에 손을 뻗었다면 답하지 않은 질문을 덮은 것이다.

거울상인 `Lookup would require extrapolation into the past`는 요청이 버퍼보다 오래됐다는 뜻이고, 센서 타임스탬프가 낡았거나 버퍼를 더 긴 `cache_time`으로 만들어야 한다는 신호다.

### 10. 트리 들여다보기: view_frames, tf2_echo, RViz

도구 셋, 각각 잘 답하는 질문이 다르다.

```bash
sudo apt install ros-jazzy-tf2-tools ros-jazzy-tf2-ros graphviz
ros2 run tf2_tools view_frames
```

`view_frames`는 5초 동안 구독하고(`--wait-time`으로 변경), 트리 전체를 Graphviz로 그린다. Jazzy에서는 현재 디렉터리에 `frames_<날짜>_<시각>.gv`와 `frames_<날짜>_<시각>.pdf`를 쓴다. 옛 튜토리얼이 말하는 `frames.pdf`가 아니다. `-o NAME`으로 이름을 바꾼다. "내 트리의 모양은 무엇인가"에 답하는 유일한 도구이고, 간선마다 브로드캐스터, 평균 주기, 버퍼 길이, 가장 최근과 가장 오래된 변환 시각이 라벨로 붙는다. 그 라벨이 진단 내용이다. 화살표만 보지 말고 라벨을 읽어라.

```bash
ros2 run tf2_ros tf2_echo [source_frame] [target_frame]
```

`tf2_echo`는 간선 하나 또는 사슬을 반복 출력한다. 병진, 쿼터니언과 RPY(라디안·도) 회전, 그리고 4×4 행렬 전체. "이 숫자가 맞나"에 답하고, 그림으로는 멀쩡해 보이는 부호·축 오류를 잡는 데 쓴다.

RViz는 "이게 내 로봇처럼 보이나"에 답한다. 띄우고 **Fixed Frame**을 실제로 존재하는 프레임으로 맞춘 뒤(존재하지 않는 프레임을 넣으면 모든 display가 한꺼번에 실패하고 에러가 원인 아닌 곳을 가리킨다) display 둘을 추가한다.

- **RobotModel**. *Description Source*는 기본이 `Topic`이다. 다만 *Description Topic* 필드에는 **기본값이 없다.** RViz가 상속받은 토픽 속성의 이름만 바꿀 뿐 값을 넣지 않는다. 그러니 드롭다운에서 `/robot_description`을 직접 고르라. 고르기 전까지 디스플레이는 그냥 비어 있고 아무 말도 하지 않는데, "로봇이 안 보인다"는 신고의 가장 흔한 원인이 이것이다. 그 토픽은 transient local이라 `robot_state_publisher`만 돌고 있으면 파일 경로는 필요 없다. *Visual Enabled*와 *Collision Enabled* 체크박스가 두 형상을 따로 그리며, 충돌 형상이 삼각형 5만 개짜리 메시라는 사실을 이걸로 본다. *Mass*와 *Inertia*는 관성 특성을 그린다.
- **TF**. 모든 프레임을 축, 이름, 자식에서 부모로 가는 화살표로 그린다. *Frames*가 전체를 체크박스로 나열하고, *Tree*가 부모–자식 구조를 보여 주며, *Frame Timeout*은 갱신이 멈춘 프레임이 회색으로 바랬다가 사라지기까지의 시간을 정한다. RViz에서 프레임이 바래면 그 퍼블리셔가 죽은 것이다.

### 11. REP 105: map, odom, base_link

이동 플랫폼의 프레임 이름과 순서는 REP 105로 표준화되어 있고, 모든 내비게이션 스택이 이를 전제한다.

```text
map --> odom --> base_link
```

- `base_link`는 로봇 베이스에 강체로 붙어 있고, 베이스에서 기준으로 삼기 자연스러운 지점에 둔다.
- `odom`은 월드 고정 프레임이고 원점은 로봇이 출발한 자리다. `odom`에서의 로봇 자세는 **연속**이다. 불연속 도약 없이 매끄럽게 변한다. 그러나 휠 엔코더, 시각 오도메트리, IMU를 적분해 얻으므로 **한계 없이 표류**한다.
- `map`은 z가 위인 월드 고정 프레임이다. `map`에서의 자세는 위치추정 요소가 센서 관측으로 계속 다시 계산하므로 **표류하지 않는다**. 대신 **연속이 아니다**. 새 센서 정보가 들어올 때마다 불연속으로 도약할 수 있다.

피할 수 없는 맞교환이고, 두 프레임이 모두 존재하는 이유다. 국소적이고 단기적인 것 — 속도 제어기, 1초 앞 장애물 회피, 자세가 옆으로 30 cm 튀면 불안정해지는 모든 것 — 에는 `odom`을 쓴다. 장기적이고 전역적인 것 — "부엌으로 가라" — 에는 `map`을 쓴다. 표류하면 결국 엉뚱한 방에 도착하기 때문이다.

구조가 사람을 놀라게 한다. 직관은 `map`과 `odom`이 둘 다 `base_link`의 부모여야 한다고 말하지만, 프레임은 부모를 하나만 가질 수 있으므로 REP 105는 `map`을 `odom`의 부모로 둔다. 그 귀결로, 위치추정 노드는 로봇 자세를 직접 내보내지 않는다. `map` → `odom` 보정 — 곧 누적된 오도메트리 표류 — 을 내보낸다. 오도메트리는 `odom` → `base_link`를 낸다. 어느 쪽도 상대의 간선을 내지 않는다. 7절의 규칙을 시스템에서 가장 중요한 간선들에 적용한 것이다. `base_link` 아래는 전부 `robot_state_publisher`가 당신의 URDF를 읽어서 만든다.

`map` 위에는 선택적인 `earth` 프레임(ECEF)이 있고, 서로 다른 지도를 가진 여러 로봇을 엮어야 할 때만 등장한다.

### 12. 실습: Xacro로 쓴 2링크 팔을 RViz에서 움직이기

한 자리에서 끝난다. 기준 환경은 Ubuntu 24.04 위 ROS 2 Jazzy.

```bash
sudo apt install ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui ros-jazzy-robot-state-publisher ros-jazzy-rviz2 ros-jazzy-tf2-tools liburdfdom-tools graphviz
```

`two_link_arm.urdf.xacro`를 쓴다.

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">

  <material name="grey">
    <color rgba="0.6 0.6 0.6 1"/>
  </material>

  <xacro:property name="link_len" value="0.4"/>
  <xacro:property name="link_rad" value="0.03"/>

  <xacro:macro name="default_inertial" params="mass">
    <inertial>
      <mass value="${mass}"/>
      <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
    </inertial>
  </xacro:macro>

  <xacro:macro name="arm_link" params="name">
    <link name="${name}">
      <visual>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
      </collision>
      <xacro:default_inertial mass="1.0"/>
    </link>
  </xacro:macro>

  <link name="base_link"/>
  <xacro:arm_link name="link1"/>
  <xacro:arm_link name="link2"/>

  <joint name="shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  </joint>

  <joint name="elbow" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 ${link_len}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="2.0" effort="10.0" velocity="1.0"/>
  </joint>

</robot>
```

무엇을 실행하기 전에 전개해서 구조를 확인한다.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
check_urdf two_link_arm.urdf
```

전개된 URDF를 한 번 읽어라. `arm_link` 호출 둘이 완전한 링크 정의 둘을 만들었고 `${link_len/2}`는 `0.2`가 됐다. xacro는 그게 전부다.

이제 5절의 `urdf_launch` 방식을 따른 `display.launch.py`.

```python
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', output='screen'),
    ])
```

```bash
ros2 launch ./display.launch.py
```

RViz에서 **Fixed Frame**을 `base_link`로 두고 **RobotModel**과 **TF** display를 추가한다. 그다음:

1. 슬라이더 둘을 끌어 보라. 원기둥이 움직이고 TF 축이 따라 움직인다. `shoulder`는 y 둘레로 돌므로 팔은 x–z 평면에서 흔들린다.
2. `ros2 topic echo /joint_states` — 이름 둘, 위치 둘, 끌 때마다 변한다.
3. `ros2 topic echo /tf_static --once` — 아무것도 없다. 여기 조인트는 전부 가동이라 정적 변환이 없다. 센서 마운트용 `fixed` 조인트를 하나 넣으면 나타난다.
4. 슬라이더 둘을 0에 두고 `ros2 run tf2_ros tf2_echo base_link link2`. 병진이 `[0, 0, 0.4]`여야 한다. `link2`의 원점은 `link1`의 *끝*에 있고, 이는 elbow 조인트의 `<origin>`이 말하는 바다. shoulder를 1.57로 옮기고 x와 z가 뒤바뀌는 것을 보라.
5. `ros2 run tf2_tools view_frames` 후 생성된 PDF를 연다. 프레임 셋, 간선 둘, 각 간선에 브로드캐스터로 `robot_state_publisher`와 10 Hz 근처의 주기가 보인다. 그 10은 `joint_state_publisher`의 `rate` 기본값이다. `robot_state_publisher`는 받은 것을 다시 낼 뿐이고, 자기 `publish_frequency` 기본값 20 Hz는 목표치가 아니라 *상한*이다.

주어진 슬라이더 값에 대해 `tf2_echo base_link link2`가 무엇을 찍을지 보기 전에 예측할 수 있으면 끝이다.

### 13. 진단할 고장: 한 간선에 퍼블리셔 둘

실습을 띄워 둔 채 `base_link` → `link1`의 두 번째 소유자를 추가한다. `static_transform_publisher`가 아니라 두 번째 `robot_state_publisher`를 써야 한다. static 쪽은 latched `/tf_static`에 한 번만 발행하고 이후로는 spin만 하므로, 지속적인 충돌이 아니라 한 번의 글리치로 끝나고 아래의 신호들이 나타나지 않는다.

```bash
# a SECOND robot_state_publisher on the same description, so both write /tf continuously
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro two_link_arm.urdf.xacro)"
```

**증상.** RViz에서 `link1`과 그 아래 전부 — `link2`, 팔의 나머지 — 가 두 자세 사이에서 떨거나 튄다. shoulder 슬라이더를 움직이면 팔이 움직이긴 하지만 자꾸 정적 자세 쪽으로 튕겨 돌아온다. 이 트리로 파지 자세를 계산하는 리스너 노드는 주기마다 다른 답을 받고, 평균을 내면 나아지는 게 아니라 나빠진다. 에러 로그는 없다. 두 퍼블리셔 모두 시킨 대로 정확히 동작하고 있다.

**기전.** 7절에서: tf2는 자식 프레임마다 시간순 버퍼 하나를 두고, 키는 자식 프레임뿐이다. 두 퍼블리셔의 샘플이 모두 `link1`의 버퍼에 들어가고, 조회는 요청 시각을 감싸는 이웃 샘플 사이를 보간한다 — 그 쌍이 어떤 때는 `robot_state_publisher`의 것 둘이고 어떤 때는 `static_transform_publisher` 샘플을 걸친다. 정적·동적이 섞이면 더 나쁘다. 정적 프레임과 동적 프레임은 버퍼 타입이 달라서, 두 종류가 번갈아 들어오면 tf2가 그 프레임의 캐시를 반복해 재할당하며 이력을 버린다.

**그것을 찾는 명령.**

```bash
ros2 run tf2_tools view_frames
```

PDF를 열어 `base_link` → `link1` 간선의 라벨을 읽는다.

- **Average rate**가 하나가 아니라 대략 둘의 합이다. 20 Hz로 내보낸다고 믿는 간선이 30이나 120 Hz로 찍히면 그것이 단서다.
- **Broadcaster**는 노드를 *하나만* 적는다. tf2는 가장 최근에 성공한 삽입의 authority를 기록하고 덮어쓰므로, 다이어그램을 다시 만들 때마다 라벨이 두 이름 사이에서 깜빡인다. `view_frames`를 두 번 돌려 같은 간선에 다른 브로드캐스터가 나오면 그것이 증거다.

그다음 실제로 어떤 노드가 내보내는지 확인한다.

```bash
ros2 topic info /tf --verbose
ros2 topic info /tf_static --verbose
```

`--verbose`는 모든 엔드포인트를 노드 이름으로 나열한다([[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]]에서 이 플래그를 소개했다). 하나를 기대한 `/tf`에 퍼블리셔가 둘이거나, URDF가 이미 소유한 프레임을 `/tf_static`의 `static_transform_publisher`가 주장하고 있으면 조사는 끝난다.

**해법은 조정 손잡이가 아니라 구조다.** 각 간선의 소유자를 정하고 나머지 퍼블리셔를 지운다. 이 버그의 현실적 형태는 이렇다. URDF가 나중에 조인트를 갖게 된 프레임에 대해 launch 파일에 남아 있는 `static_transform_publisher`. 각자 `robot_state_publisher`를 띄우는 launch 파일 둘. `map` → `odom`을 동시에 내보내는 위치추정 노드와 bag 재생. 그리고 드라이버가 `odom` → `base_link`를 내보내는데 EKF가 같은 간선을 내보내는 경우. 마지막 것이 robot_localization이 `map` → `odom`을 내보내고 휠 드라이버에게 브로드캐스트를 끄라고 하는 이유다.

### 14. 이 페이지가 다루지 않는 것

조인트를 실제로 구동하는 것 — 제어기, 하드웨어 인터페이스, URDF의 Gazebo Harmonic 쪽 — 은 [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]이고, 여기서 건너뛴 `<transmission>`과 `<ros2_control>` 태그, Gazebo가 기본으로 쓰는 SDF 형식도 거기 있다. 타임스탬프, `use_sim_time` 파라미터, TF 콜백이 언제 도는지 정하는 executor는 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]이다. TF2의 transient local `/tf_static`도 구독자가 QoS를 틀리는 순간 QoS 이야기가 된다. 설치 후에도 `package://` 메시 경로가 풀리도록 기술을 제대로 패키징하는 것은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. `lookup_transform`이 대신 해 주는 수학은 [[02-foundations/se3-geometry|3D Geometry & SE(3)]]와 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]]. 이 모든 것의 위층은 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- ROS 2 Jazzy 문서 — Tutorials/Intermediate/URDF: Building a movable robot model; Adding physical and collision properties; Using Xacro to clean up your code; Using URDF with `robot_state_publisher`.
- ROS 2 Jazzy 문서 — Tutorials/Intermediate/Tf2: Introducing tf2; Writing a static broadcaster (Python); Debugging tf2 problems.
- ROS 2 Jazzy 문서 — Concepts/Intermediate: Tf2(변환 방향과 `lookupTransform` 의미).
- `robot_state_publisher` 패키지 README(jazzy) — 파라미터, publish/subscribe 토픽.
- `geometry2` 소스(jazzy) — 자식 프레임 단위 버퍼와 브로드캐스터 기록은 `tf2/src/buffer_core.cpp`, `tf2/src/cache.cpp`; 출력 파일 이름과 간선 라벨은 `tf2_tools/view_frames.py`.
- `rviz_default_plugins` 소스(jazzy) — RobotModel과 TF display 속성.
- REP 105, Coordinate Frames for Mobile Platforms; REP 103, Standard Units of Measure and Coordinate Conventions.
- `urdf_launch` 패키지 — `description.launch.py`, `display.launch.py`.

> [!question]- 스스로 점검 · 정답
> **1. 노드가 `lookup_transform('base_link', 'camera_link', self.get_clock().now())`을 호출하는데 주기마다 "extrapolation into the future"가 찍힌다. 무엇이 잘못됐고 올바른 수정 둘은?** 버퍼가 아직 데이터를 받지 못한 시각을 묻고 있다. 변환은 항상 얼마간 지연을 두고 도착한다. 가장 최근 변환을 원하면 `Time()`(`tf2::TimePointZero`)을 쓰고, 센서 데이터를 변환하는 경우라면 그 메시지의 `header.stamp`를 쓰되 짧은 `timeout`을 붙여 첫 실패에 죽지 않고 기다리게 한다. 0.1초를 하드코딩해 빼는 것은 진단이지 수정이 아니다.
> **2. `map`과 `odom`이 둘 다 `base_link`의 부모가 될 수 없는 이유는 무엇이고, 위치추정 노드는 대신 무엇을 내보내나?** tf2 프레임은 부모가 정확히 하나이고, 그것이 조회 경로를 유일하게 만든다. 그래서 REP 105는 `map` → `odom` → `base_link`로 잇는다. 오도메트리가 `odom` → `base_link`를 소유하고, 위치추정은 누적된 오도메트리 표류인 `map` → `odom` 보정을 내보낸다. `odom`은 연속이지만 표류하고, `map`은 표류하지 않지만 도약한다.
> **3. URDF는 잘 로드되고 RViz에서도 멀쩡한데 플래너가 질의당 40초를 쓴다. 어디부터 보나?** `<collision>` 요소. 정밀한 visual 메시를 재사용하고 있다면 질의당 수천 번의 충돌 검사가 원시 도형 대신 메시 대 메시로 돈다. RViz의 RobotModel display에서 *Visual Enabled*를 끄고 *Collision Enabled*를 켜서 검사기가 실제로 쓰는 형상을 보고, 원시 도형이나 볼록 분해로 바꾼다.
> **4. `view_frames`는 간선마다 브로드캐스터를 하나만 보여 준다. 그런데도 같은 간선의 퍼블리셔 둘을 숨길 수 있는 이유는?** tf2는 가장 최근에 성공한 삽입의 authority를 저장하고 덮어쓰므로 라벨은 마지막에 쓴 노드를 가리킨다. 다이어그램을 다시 만들면 다른 이름이 나올 수 있다. 같은 라벨에서 믿을 만한 신호는 평균 주기다. 20 Hz로 내보내는 간선이 30이나 120 Hz로 보고되면 소유자가 둘 이상이다. `ros2 topic info /tf --verbose`와 `/tf_static`으로 확인한다.
