---
title: "25.7 Simulation and ros2_control"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Spawn your own URDF into Gazebo Harmonic, attach ros2_control to it, activate a joint trajectory controller, command a motion, and work through the chain of checks when an active controller does not move anything."
mastery-when: "Go deeper when you are writing the hardware interface itself — a real driver, a transmission, a chained controller — rather than configuring the ones that exist."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to make your described robot move in simulation under a real controller stack, and to diagnose the silent version of that not happening. Not enough to write a hardware interface for a real drive.
> **Working** — 기술한 로봇을 실제 제어 스택 위에서 시뮬레이션으로 움직이게 하고, 그것이 조용히 실패할 때 진단할 정도. 실제 구동계의 하드웨어 인터페이스를 작성할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> A sourced **ROS 2 Jazzy Jalisco on Ubuntu 24.04** installation, a workspace you can build in ([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), and the two-link arm you wrote in [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]. Simulated versus wall time matters here and is covered in [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]].
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**, 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), 그리고 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]에서 작성한 2링크 팔. 시뮬레이션 시간과 벽시계 시간의 구분이 여기서 중요해진다([[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]).

### 1. Why simulate, and what simulation will not tell you

After 25.6 you have a robot that exists as a description and a transform tree. Nothing about it moves on its own: you dragged sliders, and `robot_state_publisher` recomputed frames. There was no physics, no actuator, and no controller.

Simulation supplies the three things a description lacks. It integrates dynamics, so a joint you command accelerates against inertia and gravity instead of teleporting. It generates sensor data — camera images, lidar returns, IMU — from a world you control. And it lets you run the failure cases that would break a real machine: driving into a wall, commanding past a limit, losing a sensor mid-task.

The practical argument is cheaper than any of those: a simulator gives you a robot that is always available, always resettable to an identical initial state, and free to break.

What simulation cannot settle is **contact**. This wiki makes that argument in one place rather than repeating it: [[05-construction-robotics/sim-to-real|Sim-to-Real]] separates the dynamics, sensing, task and implementation gaps — which randomisation can span — from the contact gap, which it cannot, because a rigid-body engine resolving contact as per-timestep point constraints does not represent the contact patch at all. Read that page before you claim a manipulation result transfers. [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] is the companion question of which simulator models what.

Keep the boundary in mind while you use Gazebo here: everything on this page about plumbing — interfaces, controllers, topics, timing — transfers exactly to hardware. The physics does not transfer for free.

### 2. Which Gazebo, and why the name is confusing

The naming history is worth thirty seconds because search results are full of all three eras.

- **Gazebo Classic** is the original simulator, the one whose last release was Gazebo 11 in January 2020. It reached **end of life in January 2025** after five years of LTS. Its ROS 2 glue was `gazebo_ros_pkgs`; its plugin tags read `<plugin filename="libgazebo_ros...">`.
- **Ignition Gazebo** was the ground-up rewrite, a set of versioned libraries with `ign` commands and `ignition::` namespaces.
- In **April 2022** the project retired the Ignition name and moved everything back to **Gazebo**: `ign gazebo` became `gz sim`, `ign-gazebo` became `gz-sim`, `ros_ign` became `ros_gz`. Garden (2022) was the first release carrying the new name; Fortress, the older LTS, still uses `ign`.

The consequence for you: **do not start new work on Gazebo Classic.** It is out of support, and every tutorial that tells you to write `<gazebo><plugin filename="libgazebo_ros_control.so">` is describing a dead system. The current releases are **Harmonic** (Sep 2023 – May 2029, LTS) and **Jetty** (Sep 2025 – May 2031, LTS).

This page uses **Gazebo Harmonic**, because that is the pairing with ROS 2 Jazzy that has binary packages — `ros-jazzy-ros-gz` and `ros-jazzy-gz-ros2-control`. Lyrical Luth pairs with Jetty in the same way; the structure of everything below is unchanged, only the package names shift.

### 3. Two message systems, and why a bridge exists

Gazebo is not a ROS program. It has its own transport layer (Gazebo Transport) and its own message definitions (`gz.msgs.*`, Protobuf), and it runs perfectly well with no ROS installed. ROS 2 has DDS and `sensor_msgs/msg/*`. Neither speaks the other's wire format or type system.

That separation is deliberate — Gazebo is used outside ROS — and the cost is `ros_gz_bridge`, a node that subscribes on one side and republishes on the other, per topic, per type pair.

```bash
sudo apt install ros-jazzy-ros-gz
ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
```

Read the syntax carefully, because the punctuation is the direction:

| Form | Direction |
|---|---|
| `/topic@ros_type@gz_type` | bidirectional |
| `/topic@ros_type[gz_type` | Gazebo → ROS only |
| `/topic@ros_type]gz_type` | ROS → Gazebo only |

For more than a couple of topics, put them in a YAML file and pass it as a parameter, which is what launch files do:

```yaml
- topic_name: "scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS
```

```bash
ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=/path/to/bridge.yaml
```

Three things follow from the bridge existing. Only supported type pairs can cross, so a Gazebo message with no ROS counterpart needs a custom bridge. Every bridged topic costs a copy and a hop, which is a real latency term for high-rate images. And — the one that bites — **a topic you did not bridge does not exist on the ROS side**, with no error anywhere. The commonest instance is `/clock`: without it, nothing in your ROS graph knows simulated time.

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

### 4. Spawning the robot from its description

Gazebo starts with a world, not with your robot:

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:='-r -v 1 empty.sdf'
```

`-r` runs the simulation immediately rather than starting paused; `-v 1` sets verbosity. Then insert the robot with the `create` node from `ros_gz_sim`, whose arguments are:

| Argument | Meaning |
|---|---|
| `-world` | world to insert into |
| `-file` | read the model from a file or a Fuel URL |
| `-topic` | read the model from a ROS topic carrying the XML as a string |
| `-string` | read the model from an inline XML string |
| `-name` | name of the spawned entity |
| `-allow_renaming` | rename instead of failing if the name is taken |
| `-x -y -z -R -P -Y` | initial pose |

`-topic` is the one to use, and the reason is structural. `robot_state_publisher` already republishes the URDF on a transient-local `/robot_description` topic (25.6, §6). Spawning from that topic means the simulator and the transform tree are guaranteed to be looking at the same description — there is no expanded `.urdf` on disk to go stale:

```bash
ros2 run ros_gz_sim create -topic robot_description -name two_link_arm -allow_renaming true
```

Gazebo parses URDF by converting it to SDF internally. Most of what you wrote survives; the parts that beginners lose are the ones URDF has no concept of, which is why extra information goes in `<gazebo>` tags that the URDF parser ignores and the SDF converter reads.

### 5. ros2_control: the seam

You could write a Gazebo plugin that reads a topic and sets joint forces. People do, and then the code is worthless the day the robot is real.

`ros2_control` exists to put a defined seam in the middle of that path, with a stable interface on both sides:

- On one side, **controllers** — a joint trajectory follower, a differential drive kinematic layer, a PID. A controller is an object derived from `ControllerInterface` whose `update()` reads state and writes commands. It never knows what the hardware is.
- On the other, **hardware components** — the thing that actually talks to a motor driver, a CAN bus, an EtherCAT slave, or a simulator. Three kinds exist: `System` (multi-DOF with coupling), `Actuator` (single-DOF, read and write), `Sensor` (read only).

Between them sits a set of named interfaces, and *that* is the contract. The controller asks for `shoulder/position` as a command interface; something provides it. Whether that something is a servo drive or a physics engine is not the controller's problem.

This is why the same joint trajectory controller, with the same YAML, runs in Gazebo and on a real arm. Moving from simulation to hardware means swapping one plugin name in the URDF — everything above the seam is untouched. That is the single most valuable property on this page, and [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]] is where the parts that do *not* transfer are dealt with.

```bash
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control
```

### 6. Command interfaces and state interfaces

The interface model is two lists of strings, per joint.

- A **state interface** is something the hardware can be read for: `position`, `velocity`, `effort`.
- A **command interface** is something the hardware can be told: `position`, `velocity`, `effort`, `acceleration`.

They are declared in the URDF, inside a `<ros2_control>` block that lives alongside your links and joints:

```xml
<ros2_control name="GazeboSimSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
  <joint name="shoulder">
    <command_interface name="position"/>
    <state_interface name="position">
      <param name="initial_value">0.0</param>
    </state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
</ros2_control>
```

Two rules that beginners collide with. **A command interface can be claimed by at most one active controller at a time** — this is what makes the framework safe, and it is why activating a second controller on the same joints fails rather than producing two writers. And a controller will refuse to activate if an interface it needs is not provided: a controller configured with `command_interfaces: [velocity]` against a joint that declares only `position` does not start.

The `<hardware><plugin>` line is the only part of this block that differs between simulation and a real robot.

### 7. The controller manager

The **controller manager** is the process that holds both halves together. It loads hardware components through `pluginlib`, loads controllers through `pluginlib`, matches required interfaces against provided ones, and runs the loop: `read()` from hardware, `update()` every active controller, `write()` to hardware. Its `update_rate` parameter is that loop's frequency in Hz, default 100. It gets the robot description by subscribing to the `robot_description` topic.

A controller is a lifecycle object with three states that matter:

- **unconfigured** — loaded, parameters not read.
- **inactive** — configured, interfaces resolved, `update()` not running.
- **active** — claiming its command interfaces and writing to them.

The separation is what allows a controlled handover: deactivate the trajectory controller, activate the teleop controller, in one atomic switch, with no window in which both or neither is writing.

### 8. The `ros2 control` CLI

Installing `ros2_control` adds a verb to the `ros2` command. These are the ones you will use constantly:

```bash
ros2 control list_controllers                       # name, type, state
ros2 control list_controllers --claimed-interfaces  # and what each one is holding
ros2 control list_hardware_interfaces               # every interface, and whether it is claimed
ros2 control list_hardware_components -v
ros2 control list_controller_types                  # what is installed and loadable
```

```bash
ros2 control load_controller joint_trajectory_controller controllers.yaml
ros2 control set_controller_state joint_trajectory_controller active
ros2 control switch_controllers --deactivate a --activate b --strict
ros2 control unload_controller joint_trajectory_controller
```

`load_controller` also takes `--set-state {inactive,active}` so a load and a transition are one command. In launch files the equivalent is the `spawner` script, which loads, configures and activates in one step:

```bash
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner joint_trajectory_controller --param-file controllers.yaml
```

`spawner` takes `--controller-manager` (when the manager is not at `/controller_manager`), `--inactive` to stop at configured, and `--activate-as-group`. `unspawner` reverses it.

### 9. The controllers you will actually use

`ros2_controllers` ships a set; four cover most work.

| Controller | What it is for | Interface it wants |
|---|---|---|
| `joint_state_broadcaster/JointStateBroadcaster` | reads state interfaces and publishes `/joint_states`; not a controller in the commanding sense, but nothing sees your robot without it | state only |
| `joint_trajectory_controller/JointTrajectoryController` | follows a timed multi-joint trajectory; what MoveIt 2 executes through | `position`, or `velocity`/`effort` with PID gains |
| `forward_command_controller` variants (`position_controllers/JointGroupPositionController`, and the velocity and effort versions) | pass a raw command array straight to the hardware, no trajectory, no interpolation — the right tool for a learned policy or a hand-written loop | whichever it names |
| `diff_drive_controller/DiffDriveController` | converts a body velocity into left and right wheel commands and publishes odometry | `velocity` on the wheel joints |

Their surfaces, which are what you actually type against:

- **Joint trajectory controller** — topic `<name>/joint_trajectory` (`trajectory_msgs/msg/JointTrajectory`) and action `<name>/follow_joint_trajectory` (`control_msgs/action/FollowJointTrajectory`). Use the action when you need to know whether the motion finished; the topic is fire-and-forget. Parameters: `joints`, `command_interfaces`, `state_interfaces`. `state_interfaces` must include `position`, and must include `velocity` when the command interface is `velocity` or `effort` alone.
- **Forward command controllers** — topic `<name>/commands` (`std_msgs/msg/Float64MultiArray`), parameters `joints` and `interface_name`. The array is positional: element *i* goes to joint *i* of the `joints` list. Nothing validates that you meant that ordering.
- **Differential drive controller** — subscribes `<name>/cmd_vel` as `geometry_msgs/msg/TwistStamped` in Jazzy (not plain `Twist`; this is a frequent version trap), publishes `<name>/odom` and, when `enable_odom_tf` is true, the `odom` → `base_link` edge on `/tf`. Parameters: `left_wheel_names`, `right_wheel_names`, `wheel_separation`, `wheel_radius`.

### 10. gz_ros2_control: the simulation hardware interface

`gz_ros2_control` is a Gazebo system plugin that instantiates a controller manager inside the simulation process and connects it to a Gazebo model. Its joints are the hardware. Because the controller manager runs *inside* Gazebo, the control loop is stepped by the simulator's clock rather than by wall time — which is what makes a paused or slowed simulation behave correctly instead of racing.

Two tags attach it, and they do different jobs.

The `<ros2_control>` block names the hardware plugin — this is the line you change for real hardware:

```xml
<hardware>
  <plugin>gz_ros2_control/GazeboSimSystem</plugin>
</hardware>
```

The `<gazebo>` block loads the system plugin into the simulator and hands it the controller configuration:

```xml
<gazebo>
  <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>/absolute/path/to/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

`<parameters>` may appear more than once to merge several YAML files. Optional children include `<controller_manager_name>` (default `controller_manager`), `<hold_joints>`, `<position_proportional_gain>`, and a `<ros>` block for namespace and remapping.

### 11. Exercise: the two-link arm, moving in Gazebo Harmonic

One sitting. Baseline is ROS 2 Jazzy on Ubuntu 24.04 with Gazebo Harmonic.

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control
```

**Step 1 — anchor the arm and give it mass.** The 25.6 arm has a `base_link` with no `<inertial>` and no attachment to the world. In RViz that was fine. In a physics engine it falls. Add, to `two_link_arm.urdf.xacro`:

```xml
<link name="world"/>
<joint name="world_to_base" type="fixed">
  <parent link="world"/>
  <child link="base_link"/>
</joint>
```

and give `base_link` an `<inertial>` with the `default_inertial` macro you already wrote. Re-run `check_urdf` before going further.

**Step 2 — the `<ros2_control>` block.** Append inside `<robot>`, using the joint names `shoulder` and `elbow` exactly as the joints are named:

```xml
<ros2_control name="GazeboSimSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
  <joint name="shoulder">
    <command_interface name="position"/>
    <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
  <joint name="elbow">
    <command_interface name="position"/>
    <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
</ros2_control>

<gazebo>
  <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>/absolute/path/to/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

**Step 3 — `config/controllers.yaml`.**

```yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

joint_trajectory_controller:
  ros__parameters:
    type: joint_trajectory_controller/JointTrajectoryController
    joints:
      - shoulder
      - elbow
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
```

**Step 4 — the launch file**, following the structure of the `gz_ros2_control_demos` launch files. Note the ordering: the entity must exist before the controller manager it contains can be spawned into, so the spawners are chained on process exit.

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'
CONTROLLERS = '/absolute/path/to/config/controllers.yaml'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               output='screen',
               parameters=[{'robot_description': robot_description,
                            'use_sim_time': True}])

    spawn = Node(package='ros_gz_sim', executable='create', output='screen',
                 arguments=['-topic', 'robot_description',
                            '-name', 'two_link_arm', '-allow_renaming', 'true'])

    jsb = Node(package='controller_manager', executable='spawner',
               arguments=['joint_state_broadcaster'])

    jtc = Node(package='controller_manager', executable='spawner',
               arguments=['joint_trajectory_controller', '--param-file', CONTROLLERS])

    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge', output='screen',
                  arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'])

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([PathJoinSubstitution(
                [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])]),
            launch_arguments=[('gz_args', '-r -v 1 empty.sdf')]),
        rsp, bridge, spawn,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[jsb])),
        RegisterEventHandler(OnProcessExit(target_action=jsb, on_exit=[jtc])),
    ])
```

**Step 5 — verify before commanding.** In a second sourced terminal:

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers
```

You want both controllers `active`, the exercise's two `position` command interfaces each listed as `[available] [claimed]`, and `/joint_states` echoing at the broadcaster's rate.

**Step 6 — command a trajectory.**

```bash
ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.8, -1.0], time_from_start: {sec: 2, nanosec: 0}}]}"
```

The arm swings over two seconds. Send a second message with two points and different `time_from_start` values and watch it interpolate. You are done when you can predict, before pressing enter, which joint moves which way for a given sign.

### 12. The failure to diagnose: the controller is active and nothing moves

The symptom that eats an evening: `list_controllers` says `active`, no node logs an error, the simulation is running, and the arm sits still. Work the chain in this order, because each step rules out the one below it.

**1. Is it actually active, and has it stayed active?**

```bash
ros2 control list_controllers
```

`inactive` means configuration succeeded and activation did not — usually a missing interface. `unconfigured` means the parameters never arrived; the commonest cause is a `--param-file` path that was wrong, or a YAML whose top-level key is not the controller's name. A controller that activated and then fell back to `inactive` has had its hardware component go into an error state; check `ros2 control list_hardware_components -v`.

**2. Is it claiming the command interfaces?**

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers --claimed-interfaces
```

The first prints every interface with two independent markers: `[available]` or `[unavailable]` says whether the hardware offers it, and `[claimed]` or `[unclaimed]` says whether an active controller holds it. A healthy interface reads `[available] [claimed]`, so the tell is `[available] [unclaimed]` — offered, and nobody writing to it. An active controller holding nothing is the clearest possible signal: it started, but it is writing to nowhere. An interface that reads `[unavailable]`, or that does not appear at all, sends you to step 3.

**3. Do the joint names agree?**

This is the single most common cause, and it produces exactly this symptom. Three places name the same joints and all three must match character for character:

- the `<joint name="...">` elements of the URDF itself,
- the `<joint name="...">` entries inside the `<ros2_control>` block,
- the `joints:` list in the controller YAML.

`shoulder` in the URDF and `shoulder_joint` in the YAML gives you a controller that loads, configures, activates, claims nothing, and reports no error. Diff the three lists explicitly:

```bash
xacro two_link_arm.urdf.xacro | grep -E '<joint name=|<command_interface|<state_interface'
grep -A6 'joints:' config/controllers.yaml
```

Check the *interface names* the same way: a YAML asking for `command_interfaces: [velocity]` against a URDF declaring only `position` fails at activation, not at load.

**4. Is the trajectory actually being published, and being received?**

```bash
ros2 topic info /joint_trajectory_controller/joint_trajectory --verbose
```

Subscription count zero means you are publishing to a topic the controller is not listening on — almost always because the controller's *spawned name* is not `joint_trajectory_controller`, or because the controller manager is in a namespace and the real topic is `/my_robot/joint_trajectory_controller/joint_trajectory`. `ros2 topic list | grep trajectory` settles it in one line.

If the subscription exists and the message is arriving, look at time. The controller manager inside Gazebo runs on simulated time; a `ros2 topic pub` from a shell where `use_sim_time` is not set stamps the message with wall-clock time, and the trajectory's start is then either years in the past or years in the future. Check that the `/clock` bridge is running (`ros2 topic hz /clock`) and that `time_from_start` is nonzero — a trajectory whose single point is at `t=0` is a command to be there instantly, which a position interface may satisfy so fast you see nothing.

Last, confirm the simulator is stepping at all: `ros2 topic hz /joint_states` against a paused Gazebo reports a rate of zero, and a world started without `-r` is paused. Press play, or add `-r`.

### 13. What this page does not cover

Writing a hardware component of your own — a real driver behind the same interfaces — is 25.11's territory, along with the latency, safety and e-stop questions that simulation lets you ignore: [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]. Planning a collision-free trajectory to hand to the joint trajectory controller, rather than typing joint angles, is [[04-robotics/ros2/manipulation-moveit2|25.8 Manipulation with MoveIt 2]]. Sensor plugins, worlds, meshes and photorealistic rendering are Gazebo's own documentation. Chained controllers, transmissions, joint limit enforcement and controller-level safety are `ros2_control` topics one level deeper than this page. The whole track is indexed at [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- `ros2_control` documentation (Jazzy) — Getting Started (architecture, controller manager, resource manager, hardware components); Controller Manager userdoc (`update_rate`, `robot_description`, `spawner`, `unspawner`); `ros2controlcli` userdoc (CLI verbs and flags).
- `ros2_controllers` documentation (Jazzy) — Controllers index; Joint Trajectory Controller; Forward Command Controller; Differential Drive Controller; Joint State Broadcaster.
- `gz_ros2_control` (jazzy branch) — README compatibility matrix; `doc/index.rst`; `gz_ros2_control_demos` cart launch file, controller YAML and URDF.
- `ros_gz` (ros2 branch) — `ros_gz_bridge` README (direction syntax, YAML config); `ros_gz_sim` README and `create.cpp` argument list.
- Gazebo documentation — Releases (Harmonic, Jetty support windows); ROS 2 Integration; Migration from Ignition.
- Open Robotics Discourse — "Gazebo Classic End-of-Life" (Gazebo 11 end of life, January 2025).

> [!question]- Self-check · Answer
> **1. Why does `ros2_control` put a named-interface seam between the controller and the hardware, rather than letting the controller write to the motor?** Because the seam is what makes the controller portable. A controller asks for `shoulder/position` and neither knows nor cares whether a physics engine or an EtherCAT drive provides it, so the same controller and the same YAML run in Gazebo and on the real arm. Moving to hardware changes one `<plugin>` line in the URDF. It also enforces exclusivity: a command interface can be claimed by at most one active controller, which is why two writers on one joint is a failed activation rather than a fight.
> **2. Your controller is `active`, the simulation is running, and the arm does not move. What is the first command, and what is the most likely cause?** `ros2 control list_hardware_interfaces` — if the command interfaces read `[available] [unclaimed]`, the active controller is writing nowhere. The two markers are independent, so a healthy interface is `[available] [claimed]` and `[available]` on its own tells you nothing. The most likely cause is a joint name that differs between the URDF, the `<ros2_control>` block and the controller YAML. That mismatch produces no error at any stage.
> **3. Why does a `/clock` bridge matter, when nothing in the exercise reads the clock explicitly?** The controller manager runs inside Gazebo on simulated time. Without the bridge, ROS-side nodes have no simulated clock, so a trajectory stamped from a wall-clock shell has a start time unrelated to the controller's notion of now — the motion is silently in the past or the far future. Bridged topics are opt-in, and an unbridged topic does not exist on the ROS side with no error anywhere.
> **4. A tutorial tells you to add `<plugin filename="libgazebo_ros_control.so">` to your URDF. What is wrong with it?** It is Gazebo Classic, which reached end of life in January 2025. The current stack is Gazebo Harmonic with `gz_ros2_control`: `<plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">` in a `<gazebo>` tag, plus `gz_ros2_control/GazeboSimSystem` as the hardware plugin in `<ros2_control>`. Anything written with `ign` prefixes is the intermediate Ignition era, renamed back to Gazebo in April 2022.
> **5. You get a manipulation policy working in Gazebo. What can you claim?** That the plumbing works — interfaces, controllers, topics, timing, and the launch ordering. Not that the contact behaviour transfers. [[05-construction-robotics/sim-to-real|Sim-to-Real]] separates the gaps randomisation can span from the contact gap it cannot, and a contact-rich result is not comparable evidence to a locomotion result even from the same simulator.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 기술한 로봇을 실제 제어 스택 위에서 시뮬레이션으로 움직이게 하고, 그것이 조용히 실패할 때 진단할 정도. 실제 구동계의 하드웨어 인터페이스를 작성할 정도는 아니다.
> **Working** — enough to make your described robot move in simulation under a real controller stack, and to diagnose the silent version of that not happening.

> [!note] 선수 지식 · Prerequisites
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**, 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]에서 만든 2링크 팔. 시뮬레이션 시간과 벽시계 시간의 구분이 여기서 중요해진다([[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]).
> A sourced ROS 2 Jazzy install, a buildable workspace, and the two-link arm from 25.6.

### 1. 왜 시뮬레이션하는가, 그리고 시뮬레이션이 말해 주지 않는 것

25.6을 마치면 로봇은 기술(description)과 변환 트리로 존재한다. 스스로 움직이는 것은 없다. 슬라이더를 끌면 `robot_state_publisher`가 프레임을 다시 계산했을 뿐이다. 물리도, 구동기도, 제어기도 없었다.

시뮬레이션은 기술에 없는 셋을 채운다. 동역학을 적분하므로 명령한 관절이 순간이동하는 대신 관성과 중력을 거슬러 가속한다. 내가 정한 세계에서 센서 데이터 — 카메라 영상, 라이다, IMU — 를 만든다. 그리고 실물이라면 망가질 실패 사례를 돌려 볼 수 있다. 벽으로 돌진하기, 한계를 넘어 명령하기, 작업 도중 센서를 잃기.

실무적 근거는 그보다 싸다. 시뮬레이터는 항상 대기 중이고, 언제나 동일한 초기 상태로 리셋되며, 망가뜨려도 공짜인 로봇을 준다.

시뮬레이션이 결론 내 줄 수 없는 것은 **접촉(contact)** 이다. 이 위키는 그 논증을 한 곳에서만 한다. [[05-construction-robotics/sim-to-real|Sim-to-Real]]은 랜덤화가 걸칠 수 있는 동역학·센싱·과제·구현 격차와, 걸칠 수 없는 접촉 격차를 분리한다. 접촉을 타임스텝마다 점 구속으로 푸는 강체 엔진은 접촉 패치 자체를 표현하지 못하기 때문이다. 매니퓰레이션 결과가 전이된다고 주장하기 전에 그 쪽을 읽어라. 어느 시뮬레이터가 무엇을 모델링하는가는 [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]]의 질문이다.

여기서 Gazebo를 쓰는 동안 그 경계를 기억하라. 이 페이지의 배관 — 인터페이스, 제어기, 토픽, 타이밍 — 은 하드웨어로 그대로 옮겨간다. 물리는 공짜로 옮겨가지 않는다.

### 2. 어느 Gazebo인가, 그리고 이름이 헷갈리는 이유

검색 결과에 세 시대가 뒤섞여 나오므로 30초를 쓸 값어치가 있다.

- **Gazebo Classic** 은 원래 시뮬레이터다. 마지막 릴리스가 2020년 1월의 Gazebo 11이고, 5년 LTS를 마치고 **2025년 1월에 지원이 종료됐다**. ROS 2 접착제는 `gazebo_ros_pkgs`였고, 플러그인 태그는 `<plugin filename="libgazebo_ros...">` 모양이었다.
- **Ignition Gazebo** 는 바닥부터 다시 쓴 버전이다. `ign` 명령과 `ignition::` 네임스페이스를 쓰는 버전별 라이브러리 묶음이었다.
- **2022년 4월** 프로젝트는 Ignition이라는 이름을 폐기하고 전부 **Gazebo** 로 되돌렸다. `ign gazebo`는 `gz sim`이 되고, `ign-gazebo`는 `gz-sim`, `ros_ign`은 `ros_gz`가 됐다. 새 이름을 단 첫 릴리스는 Garden(2022)이고, 구 LTS인 Fortress는 여전히 `ign`을 쓴다.

당신에게 오는 귀결: **새 작업을 Gazebo Classic에서 시작하지 마라.** 지원이 끝났고, `<gazebo><plugin filename="libgazebo_ros_control.so">`를 쓰라는 모든 튜토리얼은 죽은 시스템을 설명하고 있다. 현행 릴리스는 **Harmonic**(2023년 9월 – 2029년 5월, LTS)과 **Jetty**(2025년 9월 – 2031년 5월, LTS)다.

이 페이지는 **Gazebo Harmonic** 을 쓴다. ROS 2 Jazzy와 바이너리 패키지가 있는 짝이기 때문이다 — `ros-jazzy-ros-gz`, `ros-jazzy-gz-ros2-control`. Lyrical Luth는 같은 방식으로 Jetty와 짝을 이룬다. 아래 구조는 그대로이고 패키지 이름만 바뀐다.

### 3. 메시지 체계가 둘인 이유, 그리고 브리지

Gazebo는 ROS 프로그램이 아니다. 자체 전송 계층(Gazebo Transport)과 자체 메시지 정의(`gz.msgs.*`, Protobuf)를 갖고, ROS가 없어도 멀쩡히 돈다. ROS 2는 DDS와 `sensor_msgs/msg/*`를 쓴다. 둘은 서로의 와이어 포맷도 타입 체계도 모른다.

그 분리는 의도된 것이고 — Gazebo는 ROS 밖에서도 쓰인다 — 대가가 `ros_gz_bridge`다. 한쪽에서 구독해 다른 쪽으로 다시 publish하는 노드이고, 토픽마다 타입 쌍마다 하나씩 필요하다.

```bash
sudo apt install ros-jazzy-ros-gz
ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
```

문법을 주의해서 읽어라. 구두점이 방향이다.

| 형태 | 방향 |
|---|---|
| `/topic@ros_type@gz_type` | 양방향 |
| `/topic@ros_type[gz_type` | Gazebo → ROS |
| `/topic@ros_type]gz_type` | ROS → Gazebo |

토픽이 몇 개를 넘으면 YAML에 넣고 파라미터로 넘긴다. launch 파일이 하는 방식이다.

```yaml
- topic_name: "scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS
```

```bash
ros2 run ros_gz_bridge parameter_bridge --ros-args -p config_file:=/path/to/bridge.yaml
```

브리지가 존재한다는 사실에서 셋이 따라 나온다. 지원되는 타입 쌍만 건너갈 수 있으므로, ROS 대응물이 없는 Gazebo 메시지는 직접 브리지를 써야 한다. 브리지된 토픽마다 복사와 홉이 하나씩 붙고, 고속 영상에서는 실제 지연 항이 된다. 그리고 물리는 것 하나 — **브리지하지 않은 토픽은 ROS 쪽에 존재하지 않으며**, 아무 데도 에러가 나지 않는다. 가장 흔한 사례가 `/clock`이다. 이것 없이는 ROS 그래프의 어떤 것도 시뮬레이션 시간을 모른다.

```bash
ros2 run ros_gz_bridge parameter_bridge /clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock
```

### 4. 기술로부터 로봇 띄우기

Gazebo는 내 로봇이 아니라 world로 시작한다.

```bash
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:='-r -v 1 empty.sdf'
```

`-r`은 일시정지 대신 곧바로 시뮬레이션을 돌리고, `-v 1`은 로그 수준이다. 그다음 `ros_gz_sim`의 `create` 노드로 로봇을 삽입한다. 인자는 다음과 같다.

| 인자 | 의미 |
|---|---|
| `-world` | 삽입할 world |
| `-file` | 파일 또는 Fuel URL에서 모델을 읽음 |
| `-topic` | XML 문자열을 담은 ROS 토픽에서 모델을 읽음 |
| `-string` | 인라인 XML 문자열에서 읽음 |
| `-name` | 생성될 엔티티 이름 |
| `-allow_renaming` | 이름이 겹치면 실패 대신 개명 |
| `-x -y -z -R -P -Y` | 초기 자세 |

`-topic`을 써야 하고, 이유는 구조적이다. `robot_state_publisher`는 이미 URDF를 transient-local `/robot_description` 토픽으로 다시 내보낸다(25.6 §6). 그 토픽에서 띄우면 시뮬레이터와 변환 트리가 같은 기술을 본다는 것이 보장된다. 디스크에 낡을 `.urdf` 파일이 아예 없다.

```bash
ros2 run ros_gz_sim create -topic robot_description -name two_link_arm -allow_renaming true
```

Gazebo는 URDF를 내부적으로 SDF로 변환해 파싱한다. 쓴 것 대부분은 살아남는다. 초심자가 잃는 부분은 URDF에 개념이 없는 것들이고, 그래서 추가 정보는 URDF 파서가 무시하고 SDF 변환기가 읽는 `<gazebo>` 태그에 들어간다.

### 5. ros2_control: 이음매

토픽을 읽어 관절 힘을 주는 Gazebo 플러그인을 직접 쓸 수도 있다. 실제로 그렇게 하고, 그러면 로봇이 실물이 되는 날 그 코드는 쓸모가 없어진다.

`ros2_control`은 그 경로 한가운데에 정의된 이음매를 놓고 양쪽에 안정된 인터페이스를 두려고 존재한다.

- 한쪽에는 **제어기(controller)** — 관절 궤적 추종기, 차동 구동 기구학 계층, PID. 제어기는 `ControllerInterface`에서 파생된 객체이고, `update()`가 상태를 읽고 명령을 쓴다. 하드웨어가 무엇인지는 전혀 모른다.
- 다른 쪽에는 **하드웨어 컴포넌트** — 모터 드라이버, CAN 버스, EtherCAT 슬레이브, 또는 시뮬레이터와 실제로 대화하는 것. 세 종류가 있다: `System`(결합이 있는 다자유도), `Actuator`(1자유도, 읽기·쓰기), `Sensor`(읽기 전용).

둘 사이에 이름 붙은 인터페이스 집합이 있고, *그것이* 계약이다. 제어기는 `shoulder/position`을 명령 인터페이스로 요구하고, 무언가가 그것을 제공한다. 그 무언가가 서보 드라이브인지 물리 엔진인지는 제어기의 문제가 아니다.

같은 관절 궤적 제어기가 같은 YAML로 Gazebo에서도 실제 팔에서도 도는 이유가 이것이다. 시뮬레이션에서 하드웨어로 옮긴다는 것은 URDF의 플러그인 이름 한 줄을 바꾸는 일이고, 이음매 위쪽은 손대지 않는다. 이 페이지에서 가장 값진 성질이며, 전이되지 *않는* 부분은 [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]에서 다룬다.

```bash
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control
```

### 6. 명령 인터페이스와 상태 인터페이스

인터페이스 모형은 관절당 문자열 목록 둘이다.

- **상태 인터페이스(state interface)** 는 하드웨어에서 읽을 수 있는 것이다: `position`, `velocity`, `effort`.
- **명령 인터페이스(command interface)** 는 하드웨어에 지시할 수 있는 것이다: `position`, `velocity`, `effort`, `acceleration`.

URDF 안, 링크·관절 옆에 놓이는 `<ros2_control>` 블록에서 선언한다.

```xml
<ros2_control name="GazeboSimSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
  <joint name="shoulder">
    <command_interface name="position"/>
    <state_interface name="position">
      <param name="initial_value">0.0</param>
    </state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
</ros2_control>
```

초심자가 부딪히는 규칙 둘. **명령 인터페이스는 한 번에 최대 하나의 활성 제어기만 점유(claim)할 수 있다.** 이것이 이 프레임워크를 안전하게 만드는 장치이고, 같은 관절에 두 번째 제어기를 활성화하면 두 개의 writer가 생기는 대신 실패하는 이유다. 그리고 제어기는 필요한 인터페이스가 제공되지 않으면 활성화를 거부한다. `command_interfaces: [velocity]`로 설정된 제어기는 `position`만 선언한 관절에서 시작하지 않는다.

이 블록에서 시뮬레이션과 실제 로봇이 다른 부분은 `<hardware><plugin>` 줄 하나뿐이다.

### 7. 컨트롤러 매니저

**컨트롤러 매니저(controller manager)** 는 양쪽을 붙들고 있는 프로세스다. `pluginlib`으로 하드웨어 컴포넌트를 싣고, 같은 방식으로 제어기를 싣고, 요구된 인터페이스와 제공된 인터페이스를 맞추고, 루프를 돈다: 하드웨어에서 `read()`, 활성 제어기마다 `update()`, 하드웨어로 `write()`. `update_rate` 파라미터가 그 루프의 주기(Hz)이고 기본값은 100이다. 로봇 기술은 `robot_description` 토픽을 구독해 얻는다.

제어기는 상태 셋이 중요한 lifecycle 객체다.

- **unconfigured** — 적재됨, 파라미터는 아직 안 읽음.
- **inactive** — 설정 완료, 인터페이스 해결됨, `update()`는 돌지 않음.
- **active** — 명령 인터페이스를 점유하고 거기에 씀.

이 분리가 통제된 인계를 가능하게 한다. 궤적 제어기를 비활성화하고 teleop 제어기를 활성화하는 것을 한 번의 원자적 전환으로 하며, 둘 다 쓰거나 아무도 쓰지 않는 구간이 생기지 않는다.

### 8. `ros2 control` CLI

`ros2_control`을 설치하면 `ros2` 명령에 동사가 하나 추가된다. 계속 쓰게 될 것들.

```bash
ros2 control list_controllers                       # 이름, 타입, 상태
ros2 control list_controllers --claimed-interfaces  # 각자 무엇을 점유 중인지
ros2 control list_hardware_interfaces               # 모든 인터페이스와 점유 여부
ros2 control list_hardware_components -v
ros2 control list_controller_types                  # 설치되어 적재 가능한 것들
```

```bash
ros2 control load_controller joint_trajectory_controller controllers.yaml
ros2 control set_controller_state joint_trajectory_controller active
ros2 control switch_controllers --deactivate a --activate b --strict
ros2 control unload_controller joint_trajectory_controller
```

`load_controller`는 `--set-state {inactive,active}`도 받아서 적재와 전이를 한 명령으로 끝낸다. launch 파일에서의 대응물은 `spawner` 스크립트이고, 적재·설정·활성화를 한 번에 한다.

```bash
ros2 run controller_manager spawner joint_state_broadcaster
ros2 run controller_manager spawner joint_trajectory_controller --param-file controllers.yaml
```

`spawner`는 `--controller-manager`(매니저가 `/controller_manager`에 없을 때), configured에서 멈추는 `--inactive`, 그리고 `--activate-as-group`을 받는다. `unspawner`가 되돌린다.

### 9. 실제로 쓰게 될 제어기들

`ros2_controllers`가 한 묶음을 제공한다. 넷이 대부분의 작업을 덮는다.

| 제어기 | 용도 | 요구 인터페이스 |
|---|---|---|
| `joint_state_broadcaster/JointStateBroadcaster` | 상태 인터페이스를 읽어 `/joint_states`로 publish. 명령한다는 의미의 제어기는 아니지만, 이것 없이는 아무도 로봇을 보지 못한다 | 상태만 |
| `joint_trajectory_controller/JointTrajectoryController` | 시간이 붙은 다관절 궤적을 추종. MoveIt 2가 실행에 쓰는 것 | `position`, 또는 PID 게인과 함께 `velocity`/`effort` |
| `forward_command_controller` 계열 (`position_controllers/JointGroupPositionController` 및 velocity·effort 판) | 궤적도 보간도 없이 명령 배열을 하드웨어로 그대로 전달. 학습된 정책이나 직접 짠 루프에 맞는 도구 | 지정한 것 |
| `diff_drive_controller/DiffDriveController` | 몸체 속도를 좌우 바퀴 명령으로 변환하고 오도메트리를 publish | 바퀴 관절의 `velocity` |

실제로 손으로 치게 되는 표면.

- **관절 궤적 제어기** — 토픽 `<name>/joint_trajectory`(`trajectory_msgs/msg/JointTrajectory`), 액션 `<name>/follow_joint_trajectory`(`control_msgs/action/FollowJointTrajectory`). 동작이 끝났는지 알아야 하면 액션을 쓴다. 토픽은 보내고 잊는 쪽이다. 파라미터는 `joints`, `command_interfaces`, `state_interfaces`. `state_interfaces`에는 `position`이 반드시 있어야 하고, 명령 인터페이스가 `velocity`나 `effort` 단독일 때는 `velocity`도 있어야 한다.
- **Forward command 제어기** — 토픽 `<name>/commands`(`std_msgs/msg/Float64MultiArray`), 파라미터 `joints`와 `interface_name`. 배열은 위치 기반이다. *i* 번째 원소가 `joints` 목록의 *i* 번째 관절로 간다. 그 순서를 의도했는지 검증하는 것은 아무것도 없다.
- **차동 구동 제어기** — Jazzy에서는 `<name>/cmd_vel`을 `geometry_msgs/msg/TwistStamped`로 구독한다(평범한 `Twist`가 아니다. 버전 함정으로 자주 걸린다). `<name>/odom`을 publish하고, `enable_odom_tf`가 true면 `/tf`에 `odom` → `base_link` 간선을 낸다. 파라미터는 `left_wheel_names`, `right_wheel_names`, `wheel_separation`, `wheel_radius`.

### 10. gz_ros2_control: 시뮬레이션용 하드웨어 인터페이스

`gz_ros2_control`은 시뮬레이션 프로세스 안에 컨트롤러 매니저를 만들고 그것을 Gazebo 모델에 연결하는 Gazebo 시스템 플러그인이다. 그 관절이 곧 하드웨어다. 컨트롤러 매니저가 Gazebo *안에서* 돌기 때문에 제어 루프는 벽시계가 아니라 시뮬레이터의 시계로 진행된다. 일시정지하거나 느리게 돌린 시뮬레이션에서도 폭주하지 않고 올바르게 동작하는 이유다.

붙이는 태그는 둘이고, 하는 일이 다르다.

`<ros2_control>` 블록은 하드웨어 플러그인을 지정한다. 실제 하드웨어로 갈 때 바꾸는 줄이 이것이다.

```xml
<hardware>
  <plugin>gz_ros2_control/GazeboSimSystem</plugin>
</hardware>
```

`<gazebo>` 블록은 시스템 플러그인을 시뮬레이터에 싣고 제어기 설정을 건넨다.

```xml
<gazebo>
  <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>/absolute/path/to/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

`<parameters>`는 여러 YAML을 합치려고 여러 번 쓸 수 있다. 선택적 자식으로 `<controller_manager_name>`(기본 `controller_manager`), `<hold_joints>`, `<position_proportional_gain>`, 그리고 네임스페이스와 리매핑을 위한 `<ros>` 블록이 있다.

### 11. 실습: Gazebo Harmonic에서 2링크 팔 움직이기

한 자리에서 끝난다. 기준은 Ubuntu 24.04 + ROS 2 Jazzy + Gazebo Harmonic.

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control
```

**1단계 — 팔을 고정하고 질량을 준다.** 25.6의 팔은 `base_link`에 `<inertial>`이 없고 world에 붙어 있지도 않다. RViz에서는 문제없었다. 물리 엔진에서는 떨어진다. `two_link_arm.urdf.xacro`에 추가한다.

```xml
<link name="world"/>
<joint name="world_to_base" type="fixed">
  <parent link="world"/>
  <child link="base_link"/>
</joint>
```

그리고 이미 작성해 둔 `default_inertial` 매크로로 `base_link`에 `<inertial>`을 준다. 다음으로 넘어가기 전에 `check_urdf`를 다시 돌린다.

**2단계 — `<ros2_control>` 블록.** 관절 이름을 `shoulder`, `elbow`로 관절 정의와 정확히 같게 써서 `<robot>` 안에 붙인다.

```xml
<ros2_control name="GazeboSimSystem" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
  <joint name="shoulder">
    <command_interface name="position"/>
    <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
  <joint name="elbow">
    <command_interface name="position"/>
    <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
    <state_interface name="velocity"/>
    <state_interface name="effort"/>
  </joint>
</ros2_control>

<gazebo>
  <plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>/absolute/path/to/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

**3단계 — `config/controllers.yaml`.**

```yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

joint_trajectory_controller:
  ros__parameters:
    type: joint_trajectory_controller/JointTrajectoryController
    joints:
      - shoulder
      - elbow
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
```

**4단계 — launch 파일.** `gz_ros2_control_demos`의 launch 파일 구조를 따른다. 순서에 주의하라. 엔티티가 존재해야 그 안의 컨트롤러 매니저에 spawn할 수 있으므로, spawner들을 프로세스 종료 이벤트로 사슬처럼 엮는다.

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'
CONTROLLERS = '/absolute/path/to/config/controllers.yaml'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               output='screen',
               parameters=[{'robot_description': robot_description,
                            'use_sim_time': True}])

    spawn = Node(package='ros_gz_sim', executable='create', output='screen',
                 arguments=['-topic', 'robot_description',
                            '-name', 'two_link_arm', '-allow_renaming', 'true'])

    jsb = Node(package='controller_manager', executable='spawner',
               arguments=['joint_state_broadcaster'])

    jtc = Node(package='controller_manager', executable='spawner',
               arguments=['joint_trajectory_controller', '--param-file', CONTROLLERS])

    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge', output='screen',
                  arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'])

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([PathJoinSubstitution(
                [FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'])]),
            launch_arguments=[('gz_args', '-r -v 1 empty.sdf')]),
        rsp, bridge, spawn,
        RegisterEventHandler(OnProcessExit(target_action=spawn, on_exit=[jsb])),
        RegisterEventHandler(OnProcessExit(target_action=jsb, on_exit=[jtc])),
    ])
```

**5단계 — 명령하기 전에 확인.** source된 두 번째 터미널에서:

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers
```

제어기 둘이 `active`, 이 실습이 만든 `position` 명령 인터페이스 둘이 각각 `[available] [claimed]`, 그리고 브로드캐스터 주기로 `/joint_states`가 나와야 한다.

**6단계 — 궤적 명령.**

```bash
ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.8, -1.0], time_from_start: {sec: 2, nanosec: 0}}]}"
```

팔이 2초에 걸쳐 움직인다. 점 두 개와 서로 다른 `time_from_start`로 메시지를 한 번 더 보내고 보간을 지켜보라. 엔터를 치기 전에 어떤 부호가 어느 관절을 어느 쪽으로 움직일지 예측할 수 있으면 끝이다.

### 12. 진단할 고장: 제어기는 active인데 아무것도 움직이지 않는다

저녁 하나를 잡아먹는 증상. `list_controllers`는 `active`라 하고, 어떤 노드도 에러를 찍지 않고, 시뮬레이션은 돌고 있는데, 팔은 가만히 있다. 아래 순서대로 확인하라. 각 단계가 그 아래 단계를 배제한다.

**1. 정말로 active인가, 그리고 계속 active였는가?**

```bash
ros2 control list_controllers
```

`inactive`는 설정은 됐고 활성화가 안 됐다는 뜻이고, 보통 인터페이스가 없어서다. `unconfigured`는 파라미터가 도착하지 않은 것이고, 가장 흔한 원인은 `--param-file` 경로가 틀렸거나 YAML의 최상위 키가 제어기 이름이 아닌 경우다. 활성화됐다가 `inactive`로 떨어진 제어기는 하드웨어 컴포넌트가 에러 상태로 간 것이다. `ros2 control list_hardware_components -v`로 확인한다.

**2. 명령 인터페이스를 점유하고 있는가?**

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers --claimed-interfaces
```

첫 명령은 모든 인터페이스를 찍으면서 서로 독립적인 표시 둘을 붙인다. `[available]`과 `[unavailable]`은 하드웨어가 그것을 제공하는지를, `[claimed]`와 `[unclaimed]`는 활성 제어기가 쥐고 있는지를 말한다. 정상 인터페이스는 `[available] [claimed]`이므로 찾아야 할 신호는 `[available] [unclaimed]`다. 제공은 되는데 아무도 쓰지 않는 상태다. 아무것도 쥐지 않은 활성 제어기는 가장 명확한 신호다. 시작은 했는데 아무 데도 쓰고 있지 않다. `[unavailable]`로 나오거나 아예 나타나지 않는 인터페이스는 3단계로 보낸다.

**3. 관절 이름이 일치하는가?**

가장 흔한 원인이고, 정확히 이 증상을 만든다. 같은 관절을 세 곳이 이름 부르며, 셋이 글자 하나까지 같아야 한다.

- URDF 자체의 `<joint name="...">` 요소,
- `<ros2_control>` 블록 안의 `<joint name="...">` 항목,
- 제어기 YAML의 `joints:` 목록.

URDF에는 `shoulder`, YAML에는 `shoulder_joint`이면 적재되고 설정되고 활성화되고 아무것도 점유하지 않으며 에러도 없는 제어기가 나온다. 세 목록을 명시적으로 비교하라.

```bash
xacro two_link_arm.urdf.xacro | grep -E '<joint name=|<command_interface|<state_interface'
grep -A6 'joints:' config/controllers.yaml
```

*인터페이스 이름* 도 같은 방식으로 확인한다. `position`만 선언한 URDF에 `command_interfaces: [velocity]`를 요구하는 YAML은 적재가 아니라 활성화에서 실패한다.

**4. 궤적이 실제로 publish되고, 수신되고 있는가?**

```bash
ros2 topic info /joint_trajectory_controller/joint_trajectory --verbose
```

Subscription count가 0이면 제어기가 듣지 않는 토픽에 publish하고 있는 것이다. 거의 항상 제어기의 *spawn된 이름* 이 `joint_trajectory_controller`가 아니거나, 컨트롤러 매니저가 네임스페이스 안에 있어서 실제 토픽이 `/my_robot/joint_trajectory_controller/joint_trajectory`인 경우다. `ros2 topic list | grep trajectory` 한 줄이면 끝난다.

구독이 있고 메시지도 도착한다면 시간을 보라. Gazebo 안의 컨트롤러 매니저는 시뮬레이션 시간으로 돈다. `use_sim_time`이 설정되지 않은 셸에서 보낸 `ros2 topic pub`은 메시지에 벽시계 시각을 찍고, 그러면 궤적의 시작이 몇 년 전이거나 몇 년 뒤가 된다. `/clock` 브리지가 돌고 있는지(`ros2 topic hz /clock`), 그리고 `time_from_start`가 0이 아닌지 확인하라. 점 하나가 `t=0`인 궤적은 "지금 당장 거기 있어라"라는 명령이고, position 인터페이스는 그것을 눈에 보이지 않을 만큼 빨리 만족시킬 수 있다.

마지막으로 시뮬레이터가 진행 중인지 확인한다. 일시정지된 Gazebo에 대해 `ros2 topic hz /joint_states`는 0을 보고하고, `-r` 없이 시작한 world는 일시정지 상태다. 재생을 누르거나 `-r`을 붙여라.

### 13. 이 페이지가 다루지 않는 것

같은 인터페이스 뒤에 실제 드라이버를 놓는 하드웨어 컴포넌트를 직접 작성하는 것은 25.11의 영역이고, 시뮬레이션이 무시하게 해 주는 지연·안전·비상정지 문제도 거기 있다: [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]. 관절 각도를 손으로 치는 대신 충돌 없는 궤적을 계획해 관절 궤적 제어기에 넘기는 것은 [[04-robotics/ros2/manipulation-moveit2|25.8 Manipulation with MoveIt 2]]. 센서 플러그인, world, 메시, 사실적 렌더링은 Gazebo 자체 문서의 몫이다. 체인 제어기, transmission, 관절 한계 강제, 제어기 수준의 안전은 이 페이지보다 한 단계 깊은 `ros2_control` 주제다. 트랙 전체 색인은 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- `ros2_control` 문서(Jazzy) — Getting Started(구조, 컨트롤러 매니저, 리소스 매니저, 하드웨어 컴포넌트); Controller Manager userdoc(`update_rate`, `robot_description`, `spawner`, `unspawner`); `ros2controlcli` userdoc(CLI 동사와 플래그).
- `ros2_controllers` 문서(Jazzy) — Controllers index; Joint Trajectory Controller; Forward Command Controller; Differential Drive Controller; Joint State Broadcaster.
- `gz_ros2_control`(jazzy 브랜치) — README 호환 표; `doc/index.rst`; `gz_ros2_control_demos`의 cart launch 파일, 제어기 YAML, URDF.
- `ros_gz`(ros2 브랜치) — `ros_gz_bridge` README(방향 문법, YAML 설정); `ros_gz_sim` README와 `create.cpp` 인자 목록.
- Gazebo 문서 — Releases(Harmonic, Jetty 지원 기간); ROS 2 Integration; Migration from Ignition.
- Open Robotics Discourse — "Gazebo Classic End-of-Life"(Gazebo 11 지원 종료, 2025년 1월).

> [!question]- 스스로 점검 · 정답
> **1. `ros2_control`은 왜 제어기가 모터에 직접 쓰게 두지 않고 이름 붙은 인터페이스 이음매를 두는가?** 그 이음매가 제어기를 이식 가능하게 만들기 때문이다. 제어기는 `shoulder/position`을 요구할 뿐 그것을 물리 엔진이 주는지 EtherCAT 드라이브가 주는지 알지도 신경 쓰지도 않는다. 그래서 같은 제어기와 같은 YAML이 Gazebo에서도 실제 팔에서도 돈다. 하드웨어로 옮기는 것은 URDF의 `<plugin>` 한 줄을 바꾸는 일이다. 배타성도 여기서 나온다. 명령 인터페이스는 활성 제어기 하나만 점유할 수 있고, 그래서 한 관절에 writer 둘이 붙는 상황은 싸움이 아니라 활성화 실패가 된다.
> **2. 제어기는 `active`, 시뮬레이션은 돌고, 팔은 안 움직인다. 첫 명령은 무엇이고 가장 유력한 원인은?** `ros2 control list_hardware_interfaces` — 명령 인터페이스가 `[available] [unclaimed]`로 나오면 활성 제어기가 아무 데도 쓰고 있지 않은 것이다. 두 표시는 독립이라 정상 인터페이스는 `[available] [claimed]`이고 `[available]`만으로는 아무것도 알 수 없다. 가장 유력한 원인은 URDF, `<ros2_control>` 블록, 제어기 YAML 사이의 관절 이름 불일치다. 그 불일치는 어느 단계에서도 에러를 내지 않는다.
> **3. 실습에서 아무도 시계를 명시적으로 읽지 않는데 `/clock` 브리지가 왜 중요한가?** 컨트롤러 매니저는 Gazebo 안에서 시뮬레이션 시간으로 돈다. 브리지가 없으면 ROS 쪽 노드에는 시뮬레이션 시계가 없고, 벽시계 셸에서 찍힌 궤적의 시작 시각은 제어기의 "지금"과 무관해진다. 동작은 조용히 과거나 먼 미래에 놓인다. 브리지된 토픽은 opt-in이고, 브리지되지 않은 토픽은 ROS 쪽에 존재하지 않으면서 아무 에러도 남기지 않는다.
> **4. 어떤 튜토리얼이 URDF에 `<plugin filename="libgazebo_ros_control.so">`를 넣으라고 한다. 무엇이 잘못됐나?** Gazebo Classic이고, 2025년 1월에 지원이 종료됐다. 현행 스택은 Gazebo Harmonic + `gz_ros2_control`이다. `<gazebo>` 태그 안에 `<plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">`, 그리고 `<ros2_control>` 안의 하드웨어 플러그인으로 `gz_ros2_control/GazeboSimSystem`. `ign` 접두사로 쓰인 것은 중간의 Ignition 시대이고, 2022년 4월에 Gazebo로 되돌려졌다.
> **5. Gazebo에서 매니퓰레이션 정책이 동작한다. 무엇을 주장할 수 있나?** 배관이 동작한다는 것 — 인터페이스, 제어기, 토픽, 타이밍, launch 순서. 접촉 거동이 전이된다는 것은 아니다. [[05-construction-robotics/sim-to-real|Sim-to-Real]]은 랜덤화가 걸칠 수 있는 격차와 걸칠 수 없는 접촉 격차를 분리하며, 접촉이 많은 결과는 같은 시뮬레이터에서 나온 보행 결과와 견줄 수 있는 증거가 아니다.
