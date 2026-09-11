---
title: "25.8 Manipulation with MoveIt 2"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Stand up a MoveIt 2 arm, plan and execute a collision-free motion against a planning scene you populate yourself, and tell a planning failure apart from a controller failure."
mastery-when: "Go deeper when you are writing a planner, a collision checker or a grasp synthesiser, rather than configuring and calling one."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to configure MoveIt 2 for an arm, plan and execute against a scene you control, and diagnose the common execution failure. Not enough to write a planner or a grasp synthesiser.
> **Working** — 팔에 MoveIt 2를 설정하고, 직접 채운 씬에 대해 계획·실행하고, 흔한 실행 실패를 진단할 정도. 플래너나 파지 합성기를 직접 쓸 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]] for URDF and TF, and [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]] for controllers — MoveIt sits directly on both. Inverse kinematics at the level of [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] helps but is not required. Baseline throughout: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, MoveIt 2 from `ros-jazzy-moveit`.
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]의 URDF와 TF, [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]의 제어기. MoveIt은 이 둘 위에 바로 앉는다. [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] 수준의 역기구학은 도움이 되지만 필수는 아니다. 기준 환경은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**, MoveIt 2는 `ros-jazzy-moveit`.

### 1. What MoveIt 2 is, and three things it is not

You have an arm that moves when you send it a joint trajectory ([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). You want it to reach a pose on the other side of a column without hitting the column, the scaffolding, or itself. Writing that trajectory by hand means solving inverse kinematics, then searching a seven-dimensional configuration space for a collision-free path, then assigning times to it that no joint's velocity or acceleration limit forbids. MoveIt 2 is the assembled, plugin-based answer to exactly that problem, and it is the standard one in ROS 2.

What it is not, stated early because each misreading costs weeks:

- **It is not a controller.** MoveIt produces a time-parameterised trajectory and hands it to somebody else to track. That somebody is a `joint_trajectory_controller` from ros2_control. MoveIt never writes a torque or a velocity to hardware.
- **It is not a grasp planner.** Nothing in MoveIt tells you where to put the gripper on an object. You supply the grasp pose; MoveIt gets the gripper there. [[04-robotics/grasping|15. Grasping]] is where that pose comes from.
- **It is not a contact-aware system.** The planner's world model is a rigid geometric one in which contact is failure. The instant the gripper touches the object, you have left the regime MoveIt reasons about, and you are in [[04-robotics/force-compliance-control|13. Force & Compliance Control]].

Hold on to those three. Section 11 is what they mean for a real pick.

### 2. The move_group node: what talks to what

`move_group` is the integrator. It loads plugins, owns the world model, and exposes planning and execution over ROS actions and services. Install and inspect it:

```bash
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-resources-panda-moveit-config
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

That launch starts `move_group`, RViz with the MotionPlanning display, `robot_state_publisher`, and a ros2_control stack whose hardware is `mock_components` — the same mock hardware interface from 25.7, which is why a plan executes on a machine with no robot attached. In another sourced terminal:

```bash
ros2 node info /move_group
```

Read the surface it prints against this list of inputs:

| What move_group needs | Where it comes from |
|---|---|
| Kinematics and geometry | the `robot_description` parameter — the URDF |
| Semantics: groups, named poses, disabled collision pairs | the `robot_description_semantic` parameter — the SRDF |
| Joint limits, IK solver, planner configs, sensors | YAML in the generated config package |
| Where the robot is now | the `/joint_states` topic |
| Where frames are | TF, read only — `robot_state_publisher` publishes it |
| Where the world is | the planning scene, plus depth sensors via the occupancy map monitor |
| How to move | a `FollowJointTrajectory` action server per controller |

The two ends are worth saying plainly. Upstream, `move_group` is a consumer of the description you wrote in 25.6 and the `/joint_states` published by `joint_state_broadcaster` in 25.7. Downstream, it is a *client* of a trajectory controller's action server. MoveIt is a middle layer, and almost every integration failure is at one of those two seams.

### 3. Why the URDF is not enough: the SRDF and planning groups

The URDF says the robot has joints named `panda_joint1` through `panda_joint7` and a hand. It does not say which of those constitute "the arm", what "home" means, which link is the tip you are planning the pose of, or which link pairs can never collide because they are adjacent. A planner cannot start without all four. That semantic layer is the **SRDF** (`robot_description_semantic`), and its central concept is the **planning group**: a named set of joints that a request can target.

```xml
<group name="panda_arm">
  <chain base_link="panda_link0" tip_link="panda_link8"/>
</group>
<group_state name="ready" group="panda_arm">
  <joint name="panda_joint1" value="0"/>
  <!-- ... remaining joints ... -->
</group_state>
<end_effector name="hand" parent_link="panda_link8" group="hand"/>
<disable_collisions link1="panda_link0" link2="panda_link1" reason="Adjacent"/>
```

The **MoveIt Setup Assistant** (`ros2 run moveit_setup_assistant moveit_setup_assistant`, from `ros-jazzy-moveit-setup-assistant`) is a GUI that takes your URDF and writes this, plus the rest of the config package. Its steps are the checklist of what MoveIt needs: the **self-collision matrix** (it samples configurations and disables pairs that never, always, or by adjacency collide — this is a large runtime saving, not a cosmetic step), virtual joints fixing the robot to the world, planning groups, named robot poses, end effectors, passive joints, ros2_control tags on the URDF, ROS 2 controllers, MoveIt controllers with their `FollowJointTrajectory` interfaces, 3D perception in `sensors_3d.yaml`, and launch files.

The output is an ordinary ROS 2 package of YAML, an SRDF and launch files. Read it, keep it in version control, and edit it by hand afterwards — re-running the Assistant on a hand-edited package is a merge, not an update.

### 4. The planning pipeline: three stages, not one

A `MotionPlanRequest` does not go straight to a planner. Jazzy's pipeline runs **request adapters → planner → response adapters**, all configured in YAML and all replaceable. From the Panda OMPL config:

```yaml
planning_plugins:
  - ompl_interface/OMPLPlanner
request_adapters:
  - default_planning_request_adapters/ResolveConstraintFrames
  - default_planning_request_adapters/ValidateWorkspaceBounds
  - default_planning_request_adapters/CheckStartStateBounds
  - default_planning_request_adapters/CheckStartStateCollision
response_adapters:
  - default_planning_response_adapters/AddTimeOptimalParameterization
  - default_planning_response_adapters/ValidateSolution
  - default_planning_response_adapters/DisplayMotionPath
```

What each stage buys you:

- `ResolveConstraintFrames` rewrites constraints expressed in an object's subframe into a frame the planner knows.
- `ValidateWorkspaceBounds` supplies a default workspace (a 10 m cube) when the request omits one, so a sampling planner has somewhere bounded to sample.
- `CheckStartStateBounds` nudges a start state that is *just* outside a joint limit back inside. Real encoders report values slightly past limits; without this the plan fails before it starts.
- `CheckStartStateCollision` perturbs a start state reported as in collision to a nearby free one.
- `AddTimeOptimalParameterization` is the stage that turns a geometric path into a trajectory obeying joint velocity and acceleration limits. **The planner does not produce timing.** Path and trajectory are different objects, and this is where the difference is made.
- `ValidateSolution` re-checks the finished trajectory. `DisplayMotionPath` publishes it for RViz.

Two consequences. First, a failure message naming an adapter (`CheckStartStateBounds`) is not a planner failure — the planner never ran. Second, the order in that list *is* the execution order, so adding `default_planning_request_adapters/AddRuckigTrajectorySmoothing` for jerk-limited smoothing is a question of where in the list you put it.

### 5. The planner families, and which one you actually want

Jazzy ships four, all separately packaged, all selectable per request by `planning_pipeline` and `planner_id`.

| Family | Package | What it is for |
|---|---|---|
| **OMPL** (sampling) | `moveit_planners_ompl` | The default. RRTConnect and relatives: fast in high dimensions and cluttered scenes, probabilistically complete, **not deterministic** — the same request gives a different path each run |
| **Pilz industrial motion** | `pilz_industrial_motion_planner` | Deterministic point-to-point (`PTP`), straight-line (`LIN`) and circular (`CIRC`) motions, plus a sequence capability. What industrial programmers expect, and repeatable |
| **STOMP** | `moveit_planners_stomp` | Stochastic trajectory optimisation: samples noisy rollouts around a seed trajectory and updates it by cost |
| **CHOMP** | `moveit_planners_chomp` | Gradient-based trajectory optimisation against a signed-distance field |

The distinction that matters on a construction site: sampling planners give you *a* collision-free path, and its shape is whatever the random tree produced. Optimisers give you a *good* path by an explicit cost, but need a seed and can fail by converging into an obstacle. Pilz gives you the path you asked for, or nothing. A pipeline that plans a free-space approach with OMPL and then commands the final straight-in motion with Pilz `LIN` is a common and defensible design — and Pilz's `default_planner_config` is `PTP`, so you must set `planner_id: LIN` explicitly to get the straight line.

Repeatability deserves a warning of its own. "Works in the demo, takes a wild swing on the third run" is the normal behaviour of a sampling planner, not a bug. If repeatability is a requirement — and near formwork it is — you constrain it or you use Pilz.

### 6. The planning scene: the world the planner believes in

The **planning scene** is `move_group`'s model of the robot state plus the world, maintained by the planning scene monitor and published on `/monitored_planning_scene`. Three ways things enter it:

- **Collision objects.** Primitives, meshes or planes you publish, each with an `id` and a frame. A column, a pallet, the table. This is how you tell the planner about geometry no sensor sees.
- **Attached collision objects.** When the gripper closes, the object stops being an obstacle and becomes part of the robot: `attachObject(id, link, touch_links)` moves it from the world into the robot's collision model, attached to a link, with `touch_links` listing the gripper links permitted to touch it. Forgetting this is the classic bug — you grasp a brick and every subsequent plan fails because the hand is inside an obstacle.
- **The octomap.** Depth sensors feed the occupancy map monitor, which builds a voxel occupancy grid that the collision checker treats as obstacles. Configured in `sensors_3d.yaml` with `occupancy_map_monitor/PointCloudOctomapUpdater` or `occupancy_map_monitor/DepthImageOctomapUpdater`, plus `octomap_frame` and `octomap_resolution`. Self-filtering (the `padding_scale`/`padding_offset` parameters) is what stops the robot's own arm, seen by its own camera, from becoming an obstacle to itself.

In Python, the scene is edited through the planning scene monitor:

```python
from moveit.planning import MoveItPy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose

robot = MoveItPy(node_name="moveit_py")
psm = robot.get_planning_scene_monitor()

column = CollisionObject()
column.header.frame_id = "panda_link0"
column.id = "column"
box = SolidPrimitive()
box.type = SolidPrimitive.BOX
box.dimensions = [0.1, 0.1, 1.0]
pose = Pose()
pose.position.x = 0.4
pose.position.z = 0.5
pose.orientation.w = 1.0
column.primitives.append(box)
column.primitive_poses.append(pose)
column.operation = CollisionObject.ADD

with psm.read_write() as scene:
    scene.apply_collision_object(column)
    scene.current_state.update()
```

The `read_write()` context is not decoration: the scene is shared mutable state that the planner reads concurrently, and the lock is how you avoid planning against a half-written world.

### 7. Cartesian paths, and why `fraction` is usually less than 1.0

Sometimes you need the tool to travel in a straight line — into a slot, out of a bore. That is not a planning query, it is interpolation plus IK, and it has its own call:

```cpp
std::vector<geometry_msgs::msg::Pose> waypoints;   // start is implicit
waypoints.push_back(target_pose);
moveit_msgs::msg::RobotTrajectory trajectory;
const double eef_step = 0.01;   // metres between interpolated EE poses
double fraction = move_group.computeCartesianPath(waypoints, eef_step, trajectory);
```

It interpolates the end-effector pose at `eef_step` intervals and solves IK at each one. **The return value is the fraction of the requested path it achieved, between 0.0 and 1.0, or -1.0 on error**, and you must check it. A partial result is the normal outcome, for reasons that are all geometric rather than algorithmic: the straight line leaves the reachable workspace; it passes through or near a singularity where the IK solution degenerates; the interpolation crosses a branch of the IK solution and the nearest solution is a wrist flip; or an interpolated pose is in collision. (In Jazzy the older `jump_threshold` argument is deprecated and dropped from the current overload.)

So the honest rule is: never execute a Cartesian result without a test on `fraction`, and decide your policy deliberately. Executing a 70 % path means stopping the tool in mid-air somewhere you did not choose. Also note that `computeCartesianPath` returns a path whose timing you may still need to fix, and that Pilz `LIN` is the alternative that either gives you the whole line or fails cleanly.

### 8. Execution: handing the trajectory to ros2_control

MoveIt executes by being an action client. Its controller manager plugin is configured like this:

```yaml
trajectory_execution:
  allowed_execution_duration_scaling: 1.2
  allowed_goal_duration_margin: 0.5
  allowed_start_tolerance: 0.01
  execution_duration_monitoring: true

moveit_controller_manager: moveit_simple_controller_manager/MoveItSimpleControllerManager

moveit_simple_controller_manager:
  controller_names:
    - panda_arm_controller
  panda_arm_controller:
    action_ns: follow_joint_trajectory
    type: FollowJointTrajectory
    default: true
    joints:
      - panda_joint1
      # ... through panda_joint7
```

Every line there is a way to fail. The controller name must match a controller that ros2_control has actually loaded and activated; the `joints` list must match the controller's own joint list; the action namespace must be where the controller is serving. And the three tolerance parameters govern execution monitoring: `allowed_start_tolerance` is how far the robot's current state may differ from the trajectory's first point before MoveIt refuses to start, and the duration parameters abort a trajectory that is running too long. Section 13 is what to do when these bite.

Underneath, `joint_trajectory_controller` applies its *own* tolerances — `constraints.goal_time`, `constraints.stopped_velocity_tolerance`, and per-joint `constraints.<joint>.trajectory` and `constraints.<joint>.goal`. Two independent tolerance systems watch the same motion, and the error message tells you which one gave up.

### 9. MoveIt Servo: when planning is the wrong shape

Planning takes hundreds of milliseconds and assumes a static goal. Visual servoing onto a moving target, or teleoperating a tool by hand, does not fit that. `moveit_servo` (`ros-jazzy-moveit-servo`) is the other mode: it converts a streaming command into joint commands at control rate, with no planning at all. It accepts joint jog (individual joint velocities), twist (a desired end-effector velocity) and pose commands, and it outputs a `KinematicState` — joint names, positions, velocities, accelerations — or a trajectory/float-array topic through the ROS interface. It scales velocity down near singularities and near collisions, both on by default and both disableable.

The trade is explicit: Servo is reactive and has no lookahead, so it cannot route around an obstacle — it can only slow down as it approaches one. Use planning for getting somewhere, Servo for tracking something.

### 10. Which language interface is first-class

C++ is. `MoveGroupInterface` is the mature API, it is what the tutorials and production stacks use, and it is the only one with the full surface — `computeCartesianPath`, `attachObject`/`detachObject`, named targets, path constraints, controller selection at execute time.

Python is `moveit_py` (`ros-jazzy-moveit-py`), and it is important to know what it actually is. It does **not** wrap `MoveGroupInterface`; it binds `MoveItCpp`, which runs the planning pipeline in your own process rather than calling the `move_group` node:

```python
from moveit.planning import MoveItPy

robot = MoveItPy(node_name="moveit_py")
arm = robot.get_planning_component("panda_arm")

arm.set_start_state_to_current_state()
arm.set_goal_state(configuration_name="extended")

result = arm.plan()
if result:
    robot.execute(result.trajectory, controllers=[])
```

What Python covers: planning components (`set_start_state`, `set_goal_state` by named configuration, `RobotState`, `PoseStamped` or constraints, `set_path_constraints`, `set_workspace`), execution through `MoveItPy.execute`, the planning scene monitor and full collision-checking API, robot model and state, and multi-pipeline planning. What it does not: there is no Cartesian-path binding, no attach/detach convenience, and no ROS 1 `moveit_commander` — that package does not exist in MoveIt 2 and tutorials that import it are ROS 1 archives. Prototype in Python, and expect to write C++ once you need Cartesian moves or the full `move_group` surface.

### 11. A pick is a sequence of planning problems, not one call

MoveIt 2's `MoveGroupInterface` has no `pick()` and no `place()`. The ROS 1 grasp pipeline was not carried over, and that absence is honest rather than a gap: picking is a sequence of separate problems, and naming them is the point.

1. **Get a grasp pose.** From perception, from a grasp synthesiser, from a fixture whose geometry you measured. *MoveIt does not do this.* See [[04-robotics/grasping|15. Grasping]].
2. **Plan to a pre-grasp**, offset back along the approach axis. A free-space query — OMPL.
3. **Approach.** A short straight-line motion: `computeCartesianPath`, checking `fraction`, or Pilz `LIN`. You usually disable collision between gripper and target for this segment, because the goal is contact.
4. **Close the gripper.** A separate controller and a separate action. *MoveIt does not tell you when the grasp succeeded.* What you know is that the fingers stopped; whether the object is held is a force or tactile question — [[04-robotics/force-compliance-control|13. Force & Compliance Control]].
5. **Attach the object** to the gripper link with `touch_links`, so the planner stops treating it as an obstacle and starts carrying it.
6. **Retreat, transport, place**, then detach and remove.

Two things in that list are outside MoveIt entirely: step 1, and everything about step 4 after the fingers touch. On a construction site both are the hard part — an irregular block on an uneven surface with unknown friction is a grasp-synthesis and force-control problem, and MoveIt's contribution is only that the arm gets there without hitting the formwork. Sequencing steps 2–6 with proper failure handling and backtracking is what `moveit_task_constructor` (`ros-jazzy-moveit-task-constructor-core`) exists for, and it is the right next tool once a hand-written sequence starts growing error branches.

### 12. Exercise: plan, execute, then put a column in the way

One sitting, on the Panda demo. Nothing here needs hardware.

1. `ros2 launch moveit_resources_panda_moveit_config demo.launch.py`. In RViz's **MotionPlanning** display, check that **Planning Scene Topic** is `/monitored_planning_scene`.
2. On the **Planning** tab, drag the orange interactive marker to a goal pose, **Plan**, watch the preview, then **Execute**. The mock-hardware arm follows.
3. Press **Plan** three more times without moving the goal. The trajectory is different each time. That is OMPL being a sampling planner — fix it in your head now, before it surprises you on hardware.
4. In a second sourced terminal, watch the traffic that execution produces:

```bash
ros2 topic echo /monitored_planning_scene --once
ros2 action list | grep follow_joint_trajectory
ros2 control list_controllers
```

5. Now add the obstacle. In the MotionPlanning display's **Scene Objects** tab, add a box, scale it to roughly a 0.1 m square column a metre tall, and drag it between the arm's start and goal. Plan again. The path bends. Drag it until the planner cannot get through and read the failure in the RViz status line and the `move_group` terminal.
6. Repeat step 5 from Python, using the `apply_collision_object` snippet in section 6, and confirm the box appears in RViz. That is the loop you will actually use: scene from code, visual confirmation in RViz.
7. Switch the planner. In the **Context** tab pick the `pilz_industrial_motion_planner` pipeline and `LIN`, and plan the same motion. Note where OMPL succeeds and `LIN` refuses — that refusal is the planner telling you the straight line does not exist, which is information OMPL never gives you.

You are done when you can state which of the last two plans you would trust near a wall, and why.

### 13. The failure to diagnose: it plans in RViz but will not execute

The most common MoveIt bug report, and it is nearly always the seam in section 8. The symptom: **Plan** succeeds and animates; **Execute** fails immediately or aborts partway. Work the checks in this order, because each rules out a layer.

| # | Check | Command | What a failure means |
|---|---|---|---|
| 1 | Did planning really succeed? | RViz status line; `move_group` terminal | If an adapter name appears, the planner never ran — fix the request, not the controller |
| 2 | Is a controller loaded and active? | `ros2 control list_controllers` | `inactive`, or the controller absent, means nothing is listening. Controller spawning is a 25.7 problem |
| 3 | Does the name in MoveIt's config exist in ros2_control? | compare `moveit_controllers.yaml` `controller_names` with step 2 | A typo here gives "Unable to identify any set of controllers" — MoveIt found no controller that covers the group's joints |
| 4 | Is the action server actually there? | `ros2 action list \| grep follow_joint_trajectory` | Missing means the controller is not serving `FollowJointTrajectory`, or `action_ns` is wrong |
| 5 | Do the joint names agree? | `ros2 control list_controllers -v`, MoveIt's `joints:` list, and the SRDF group | Any mismatch — a renamed joint, a prefixed namespace on a multi-arm cell — and MoveIt cannot match the group to a controller |
| 6 | Does the start state match reality? | the `Invalid Trajectory: start point deviates from current robot state` message | Compare against `allowed_start_tolerance` (default 0.01). A stale or missing `/joint_states`, or a robot that drifted, produces this |
| 7 | Did the controller reject it on tolerance? | controller terminal, `GOAL_TOLERANCE_VIOLATED` / `PATH_TOLERANCE_VIOLATED` | The controller could not track the trajectory. Tune `constraints.<joint>.goal` and `constraints.goal_time`, or slow the trajectory with velocity scaling |
| 8 | Did MoveIt time it out? | `execution_duration_monitoring`, `allowed_execution_duration_scaling` | The controller was tracking but too slowly — usually an underpowered or badly tuned controller, not a planning fault |

The dividing line to internalise: **checks 1 is planning, checks 2–5 are wiring, and checks 6–8 are control.** Wiring failures are silent and instant; control failures produce a partial motion and a tolerance message. Knowing which you have before you start editing YAML is most of the fix.

One more worth naming because it produces no error at all: a plan executed against a stale planning scene. If you added a collision object but `move_group` did not receive it — wrong frame id, published before the subscriber existed — the arm will drive confidently through geometry that exists only in your script. `ros2 topic echo /monitored_planning_scene --once` before you plan is the two-second check.

### 14. What this page does not cover

Where a grasp pose comes from is [[04-robotics/grasping|15. Grasping]]; what happens after contact is [[04-robotics/force-compliance-control|13. Force & Compliance Control]]. The trajectory controllers that MoveIt commands, and the hardware interface beneath them, are [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]; the URDF and TF that the SRDF annotates are [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]. The mathematics of the IK that MoveIt calls as a plugin is [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]. Multi-stage task planning with backtracking is `moveit_task_constructor`; reactive planning that replans during execution is `moveit_ros/hybrid_planning`; moving the base as well as the arm sits in [[04-robotics/ros2/index|25. ROS 2]] alongside navigation.

### Sources

- MoveIt 2 documentation — Concepts: the `move_group` node; Motion Planning; Planning Scene Monitor; Trajectory Processing.
- MoveIt 2 documentation — MoveIt Setup Assistant tutorial; Perception Pipeline tutorial (octomap updater plugins and `sensors_3d.yaml`); Realtime Arm Servoing tutorial.
- `moveit/moveit2` (branch `jazzy`) — `move_group_interface.hpp` (`computeCartesianPath` return semantics, deprecated `jump_threshold`); `planning_pipeline.cpp` (request/response adapter split); `moveit_py` bindings for `PlanningComponent`, `MoveItCpp` and `PlanningScene`.
- `moveit/moveit_resources` (branch `ros2`) — `panda_moveit_config`: `ompl_planning.yaml`, `pilz_industrial_motion_planner_planning.yaml`, `moveit_controllers.yaml`, `demo.launch.py`.
- `moveit/moveit2_tutorials` — Quickstart in RViz; Motion Planning Python API.
- ros2_control documentation (Jazzy) — `joint_trajectory_controller` parameters (`constraints.*`).
- MoveIt binary install instructions (`ros-jazzy-moveit`); ROS 2 Jazzy package index.

> [!question]- Self-check · Answer
> **1. Your plan is beautiful in RViz and the arm does not move. What are the first three commands?** `ros2 control list_controllers` (is a controller active?), a comparison of its name against `controller_names` in `moveit_controllers.yaml`, and `ros2 action list | grep follow_joint_trajectory` (is the action server there?). All three are the wiring layer, and wiring failures are instant and silent — check them before touching tolerances.
> **2. Why is the URDF insufficient for MoveIt, in one sentence?** It describes geometry and kinematics but carries no semantics: no planning groups, no named poses, no tip link, no disabled collision pairs — all of which live in the SRDF and all of which a planner needs before it can accept a request.
> **3. `computeCartesianPath` returns 0.62. What do you do, and what are the likely causes?** Do not execute it — that would stop the tool 62 % of the way along a line you chose for a reason. Likely causes are the line leaving the reachable workspace, passing near a singularity, crossing to a different IK branch, or an interpolated pose in collision. Either shorten or reorient the segment, or use Pilz `LIN`, which fails cleanly instead of partially.
> **4. You close the gripper on a block and every subsequent plan fails in collision. Why?** The block is still a world collision object and the gripper is now inside it. Attach it to the gripper link with the gripper's links listed as `touch_links`, which moves it into the robot's own collision model.
> **5. Which parts of a construction-site pick does MoveIt not solve?** Where the grasp pose is — that is grasp synthesis from perception — and everything from the moment of contact onward, since MoveIt's world model treats contact as failure. It solves only the collision-free motion between those two.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 팔에 MoveIt 2를 설정하고, 직접 채운 씬에 대해 계획·실행하고, 흔한 실행 실패를 진단할 정도. 플래너나 파지 합성기를 직접 쓸 정도는 아니다.
> **Working** — enough to configure MoveIt 2, plan and execute against a scene you control, and diagnose the common execution failure.

> [!note] 선수 지식 · Prerequisites
> URDF와 TF는 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]], 제어기는 [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]. MoveIt은 이 둘 위에 바로 앉는다. [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] 수준의 역기구학은 도움이 되지만 필수는 아니다. 기준 환경은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**, MoveIt 2는 `ros-jazzy-moveit`.
> URDF/TF from 25.6 and controllers from 25.7; baseline ROS 2 Jazzy on Ubuntu 24.04.

### 1. MoveIt 2는 무엇이고, 아닌 것 세 가지

관절 궤적을 보내면 움직이는 팔은 이미 있다([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). 이제 기둥 반대편의 어떤 자세로, 기둥도 비계도 자기 몸도 치지 않고 가야 한다. 그 궤적을 손으로 쓰려면 역기구학을 풀고, 7차원 배치 공간에서 충돌 없는 경로를 탐색하고, 어느 관절의 속도·가속도 한계도 어기지 않는 시간을 그 경로에 붙여야 한다. MoveIt 2는 정확히 그 문제에 대한 조립된 플러그인 기반 답이고, ROS 2의 표준이다.

아닌 것 세 가지. 각각의 오해가 몇 주를 잡아먹는다.

- **제어기가 아니다.** MoveIt은 시간 파라미터화된 궤적을 만들어 남에게 넘긴다. 그 남은 ros2_control의 `joint_trajectory_controller`다. MoveIt은 하드웨어에 토크나 속도를 쓰지 않는다.
- **파지(grasp) 플래너가 아니다.** 물체의 어디를 잡을지는 MoveIt이 알려 주지 않는다. 파지 자세는 당신이 준다. MoveIt은 그리퍼를 거기까지 데려다줄 뿐이다. 그 자세의 출처는 [[04-robotics/grasping|15. Grasping]].
- **접촉을 다루는 시스템이 아니다.** 플래너의 세계 모형은 접촉이 곧 실패인 강체 기하 모형이다. 그리퍼가 물체에 닿는 순간 MoveIt이 추론하는 영역을 벗어나고, 거기서부터는 [[04-robotics/force-compliance-control|13. Force & Compliance Control]]이다.

이 셋을 붙잡아 두라. 11절이 실제 픽에서 이것이 무슨 뜻인지다.

### 2. move_group 노드: 무엇이 무엇과 말하는가

`move_group`이 통합자다. 플러그인을 로드하고, 세계 모형을 소유하고, 계획과 실행을 ROS 액션·서비스로 노출한다.

```bash
sudo apt install ros-jazzy-moveit ros-jazzy-moveit-resources-panda-moveit-config
source /opt/ros/jazzy/setup.bash
ros2 launch moveit_resources_panda_moveit_config demo.launch.py
```

이 런치는 `move_group`, MotionPlanning 디스플레이가 붙은 RViz, `robot_state_publisher`, 그리고 하드웨어가 `mock_components`인 ros2_control 스택을 띄운다. 25.7의 그 모의 하드웨어 인터페이스이고, 로봇이 없는 머신에서도 계획이 실행되는 이유다. source된 다른 터미널에서:

```bash
ros2 node info /move_group
```

찍히는 표면을 이 입력 목록과 대조하며 읽어라.

| move_group이 필요로 하는 것 | 출처 |
|---|---|
| 기구학과 기하 | `robot_description` 파라미터 — URDF |
| 의미론: 그룹, 이름 붙은 자세, 비활성 충돌 쌍 | `robot_description_semantic` 파라미터 — SRDF |
| 관절 한계, IK 솔버, 플래너 설정, 센서 | 생성된 config 패키지의 YAML |
| 로봇이 지금 어디인지 | `/joint_states` 토픽 |
| 프레임이 어디인지 | TF, 읽기만 — 발행은 `robot_state_publisher` |
| 세계가 어떤지 | planning scene, 그리고 occupancy map monitor를 통한 깊이 센서 |
| 어떻게 움직일지 | 제어기마다 하나씩인 `FollowJointTrajectory` 액션 서버 |

양 끝을 분명히 해 두자. 위로 `move_group`은 25.6에서 쓴 description과 25.7의 `joint_state_broadcaster`가 내는 `/joint_states`의 소비자다. 아래로는 궤적 제어기 액션 서버의 *클라이언트*다. MoveIt은 중간 계층이고, 통합 실패는 거의 전부 이 두 이음매 중 하나에서 난다.

### 3. URDF만으로 부족한 이유: SRDF와 planning group

URDF는 `panda_joint1`부터 `panda_joint7`까지의 관절과 손이 있다고 말한다. 그중 무엇이 "팔"인지, "home"이 무엇인지, 자세를 계획할 끝점 링크가 어느 것인지, 어떤 링크 쌍이 인접해 있어 절대 충돌하지 않는지는 말하지 않는다. 플래너는 이 넷 없이 시작할 수 없다. 그 의미론 계층이 **SRDF**(`robot_description_semantic`)이고, 중심 개념은 요청이 대상으로 삼을 수 있는 관절 집합에 이름을 붙인 **planning group**이다.

```xml
<group name="panda_arm">
  <chain base_link="panda_link0" tip_link="panda_link8"/>
</group>
<group_state name="ready" group="panda_arm">
  <joint name="panda_joint1" value="0"/>
  <!-- ... 나머지 관절 ... -->
</group_state>
<end_effector name="hand" parent_link="panda_link8" group="hand"/>
<disable_collisions link1="panda_link0" link2="panda_link1" reason="Adjacent"/>
```

**MoveIt Setup Assistant**(`ros2 run moveit_setup_assistant moveit_setup_assistant`, `ros-jazzy-moveit-setup-assistant`)는 URDF를 받아 이것과 config 패키지 나머지를 써 주는 GUI다. 그 단계 목록이 곧 MoveIt이 필요로 하는 것의 체크리스트다: **self-collision matrix**(배치를 샘플링해 절대·항상·인접으로 충돌하는 쌍을 비활성화한다. 장식이 아니라 큰 런타임 절감이다), 로봇을 세계에 고정하는 virtual joint, planning group, 이름 붙은 자세, end effector, passive joint, URDF의 ros2_control 태그, ROS 2 제어기, `FollowJointTrajectory` 인터페이스를 갖는 MoveIt 제어기, `sensors_3d.yaml`의 3D 인식, 런치 파일.

결과물은 YAML·SRDF·런치 파일로 된 평범한 ROS 2 패키지다. 읽고, 버전 관리에 넣고, 이후에는 손으로 고쳐라. 손으로 고친 패키지에 Assistant를 다시 돌리는 것은 갱신이 아니라 병합이다.

### 4. 계획 파이프라인: 하나가 아니라 세 단계

`MotionPlanRequest`는 플래너로 곧장 가지 않는다. Jazzy의 파이프라인은 **request adapter → 플래너 → response adapter** 순으로 돌고, 전부 YAML로 설정되고 전부 교체 가능하다. Panda의 OMPL 설정에서:

```yaml
planning_plugins:
  - ompl_interface/OMPLPlanner
request_adapters:
  - default_planning_request_adapters/ResolveConstraintFrames
  - default_planning_request_adapters/ValidateWorkspaceBounds
  - default_planning_request_adapters/CheckStartStateBounds
  - default_planning_request_adapters/CheckStartStateCollision
response_adapters:
  - default_planning_response_adapters/AddTimeOptimalParameterization
  - default_planning_response_adapters/ValidateSolution
  - default_planning_response_adapters/DisplayMotionPath
```

각 단계가 사 주는 것:

- `ResolveConstraintFrames` — 물체의 subframe으로 표현된 제약을 플래너가 아는 프레임으로 다시 쓴다.
- `ValidateWorkspaceBounds` — 요청에 작업 공간이 없으면 기본값(10 m 정육면체)을 넣는다. 샘플링 플래너가 샘플링할 유계 영역이 있어야 한다.
- `CheckStartStateBounds` — 관절 한계를 *아주 조금* 벗어난 시작 상태를 안쪽으로 밀어 넣는다. 실제 엔코더는 한계를 살짝 넘은 값을 보고하고, 이것이 없으면 계획은 시작 전에 실패한다.
- `CheckStartStateCollision` — 충돌로 보고된 시작 상태를 근처의 자유 상태로 섭동시킨다.
- `AddTimeOptimalParameterization` — 기하 경로를 관절 속도·가속도 한계를 지키는 궤적으로 바꾸는 단계다. **플래너는 시간을 만들지 않는다.** 경로와 궤적은 다른 물건이고, 그 차이가 여기서 생긴다.
- `ValidateSolution`은 완성된 궤적을 다시 검사하고, `DisplayMotionPath`는 RViz용으로 발행한다.

귀결 둘. 첫째, 어댑터 이름(`CheckStartStateBounds`)이 뜬 실패는 플래너 실패가 아니다. 플래너는 돌지도 않았다. 둘째, 그 목록의 순서가 곧 실행 순서라서, jerk 제한 평활화를 위해 `default_planning_request_adapters/AddRuckigTrajectorySmoothing`을 넣는 일은 "목록의 어디에 넣느냐"의 문제다.

### 5. 플래너 계열과 실제로 필요한 것

Jazzy는 넷을 제공하고, 전부 별도 패키지이며, 요청마다 `planning_pipeline`과 `planner_id`로 고른다.

| 계열 | 패키지 | 용도 |
|---|---|---|
| **OMPL**(샘플링) | `moveit_planners_ompl` | 기본값. RRTConnect 계열: 고차원·혼잡 씬에서 빠르고 확률적 완전성을 갖지만 **결정적이지 않다** — 같은 요청이 실행마다 다른 경로를 준다 |
| **Pilz industrial motion** | `pilz_industrial_motion_planner` | 결정적인 점대점(`PTP`), 직선(`LIN`), 원호(`CIRC`) 동작과 시퀀스 기능. 산업 프로그래머가 기대하는 것이고 재현된다 |
| **STOMP** | `moveit_planners_stomp` | 확률적 궤적 최적화. 시드 궤적 주변으로 잡음 롤아웃을 뽑아 비용으로 갱신한다 |
| **CHOMP** | `moveit_planners_chomp` | 부호 있는 거리장에 대한 경사 기반 궤적 최적화 |

건설 현장에서 중요한 구분: 샘플링 플래너는 충돌 없는 경로 *하나*를 주고 그 모양은 무작위 트리가 만든 대로다. 최적화 계열은 명시적 비용 기준으로 *좋은* 경로를 주지만 시드가 필요하고 장애물 안으로 수렴해 실패할 수 있다. Pilz는 요청한 경로를 주거나 아무것도 주지 않는다. 자유 공간 접근은 OMPL로 계획하고 마지막 직진은 Pilz `LIN`으로 명령하는 파이프라인은 흔하고 타당한 설계다. 그리고 Pilz의 `default_planner_config`는 `PTP`이므로 직선을 원하면 `planner_id: LIN`을 명시해야 한다.

재현성은 따로 경고할 값어치가 있다. "데모에서는 되는데 세 번째 실행에서 팔이 크게 휘두른다"는 버그가 아니라 샘플링 플래너의 정상 동작이다. 재현성이 요구사항이라면 — 거푸집 옆에서는 요구사항이다 — 제약을 걸거나 Pilz를 쓴다.

### 6. Planning scene: 플래너가 믿는 세계

**planning scene**은 로봇 상태와 세계에 대한 `move_group`의 모형이고, planning scene monitor가 유지하며 `/monitored_planning_scene`으로 발행된다. 들어오는 경로는 셋이다.

- **Collision object.** 당신이 발행하는 기본 도형, 메시, 평면. 각각 `id`와 프레임을 갖는다. 기둥, 팔레트, 작업대. 어떤 센서도 보지 못하는 기하를 플래너에게 알리는 방법이다.
- **Attached collision object.** 그리퍼가 닫히면 물체는 장애물이기를 그치고 로봇의 일부가 된다. `attachObject(id, link, touch_links)`가 물체를 세계에서 로봇 충돌 모형으로 옮겨 링크에 붙이고, `touch_links`는 물체에 닿아도 되는 그리퍼 링크들을 나열한다. 이걸 잊는 것이 고전적인 버그다. 벽돌을 잡은 뒤 손이 장애물 안에 들어가 있어서 이후 모든 계획이 실패한다.
- **Octomap.** 깊이 센서가 occupancy map monitor에 들어가면 복셀 점유 격자가 만들어지고 충돌 검사기가 이를 장애물로 취급한다. `sensors_3d.yaml`에서 `occupancy_map_monitor/PointCloudOctomapUpdater` 또는 `occupancy_map_monitor/DepthImageOctomapUpdater`, 그리고 `octomap_frame`과 `octomap_resolution`으로 설정한다. 자기 필터링(`padding_scale`/`padding_offset` 파라미터)이 자기 카메라에 찍힌 자기 팔이 자신의 장애물이 되는 것을 막는다.

Python에서는 planning scene monitor를 통해 편집한다.

```python
from moveit.planning import MoveItPy
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive
from geometry_msgs.msg import Pose

robot = MoveItPy(node_name="moveit_py")
psm = robot.get_planning_scene_monitor()

column = CollisionObject()
column.header.frame_id = "panda_link0"
column.id = "column"
box = SolidPrimitive()
box.type = SolidPrimitive.BOX
box.dimensions = [0.1, 0.1, 1.0]
pose = Pose()
pose.position.x = 0.4
pose.position.z = 0.5
pose.orientation.w = 1.0
column.primitives.append(box)
column.primitive_poses.append(pose)
column.operation = CollisionObject.ADD

with psm.read_write() as scene:
    scene.apply_collision_object(column)
    scene.current_state.update()
```

`read_write()` 컨텍스트는 장식이 아니다. 씬은 플래너가 동시에 읽는 공유 가변 상태이고, 이 잠금이 절반만 쓰인 세계에 대고 계획하는 것을 막는다.

### 7. Cartesian path와 `fraction`이 보통 1.0이 아닌 이유

공구가 직선으로 가야 할 때가 있다. 홈에 넣을 때, 구멍에서 뺄 때. 그것은 계획 질의가 아니라 보간 더하기 IK이고, 전용 호출이 있다.

```cpp
std::vector<geometry_msgs::msg::Pose> waypoints;   // 시작점은 암묵적
waypoints.push_back(target_pose);
moveit_msgs::msg::RobotTrajectory trajectory;
const double eef_step = 0.01;   // 보간된 EE 자세 사이 간격(m)
double fraction = move_group.computeCartesianPath(waypoints, eef_step, trajectory);
```

`eef_step` 간격으로 말단 자세를 보간하고 각 지점에서 IK를 푼다. **반환값은 요청한 경로 중 달성한 비율로 0.0에서 1.0 사이이고, 오류일 때는 -1.0**이다. 반드시 검사해야 한다. 부분 결과는 정상적인 결과이고, 이유는 알고리즘이 아니라 전부 기하적이다: 직선이 도달 가능 작업 공간을 벗어난다, 특이점을 지나거나 근처를 스쳐 IK 해가 퇴화한다, 보간이 IK 해의 다른 분기를 넘어가 가장 가까운 해가 손목 뒤집기가 된다, 보간된 자세 하나가 충돌한다. (Jazzy에서 예전의 `jump_threshold` 인자는 deprecated이고 현재 오버로드에서 빠졌다.)

그래서 정직한 규칙은 이렇다. `fraction` 검사 없이 Cartesian 결과를 실행하지 마라. 70 % 경로를 실행한다는 것은 당신이 고르지 않은 어딘가의 허공에서 공구를 멈춘다는 뜻이다. 또한 `computeCartesianPath`가 돌려준 경로는 시간 부여를 따로 손봐야 할 수 있고, 전부 아니면 깔끔한 실패를 주는 대안이 Pilz `LIN`이다.

### 8. 실행: 궤적을 ros2_control에 넘기기

MoveIt은 액션 클라이언트가 되어 실행한다. 제어기 관리자 플러그인 설정은 이렇다.

```yaml
trajectory_execution:
  allowed_execution_duration_scaling: 1.2
  allowed_goal_duration_margin: 0.5
  allowed_start_tolerance: 0.01
  execution_duration_monitoring: true

moveit_controller_manager: moveit_simple_controller_manager/MoveItSimpleControllerManager

moveit_simple_controller_manager:
  controller_names:
    - panda_arm_controller
  panda_arm_controller:
    action_ns: follow_joint_trajectory
    type: FollowJointTrajectory
    default: true
    joints:
      - panda_joint1
      # ... panda_joint7까지
```

여기 모든 줄이 실패 경로다. 제어기 이름은 ros2_control이 실제로 로드하고 활성화한 제어기와 일치해야 하고, `joints` 목록은 제어기 자신의 관절 목록과 일치해야 하며, 액션 네임스페이스는 제어기가 서비스하는 곳이어야 한다. 세 개의 허용 오차 파라미터가 실행 감시를 맡는다. `allowed_start_tolerance`는 현재 상태가 궤적 첫 점에서 얼마나 벗어나도 시작을 허용할지이고, duration 파라미터들은 너무 오래 걸리는 궤적을 중단시킨다. 이것들에 물렸을 때 무엇을 할지는 13절이다.

그 아래에서 `joint_trajectory_controller`는 *자기* 허용 오차를 따로 적용한다 — `constraints.goal_time`, `constraints.stopped_velocity_tolerance`, 관절별 `constraints.<joint>.trajectory`와 `constraints.<joint>.goal`. 같은 동작을 독립된 두 허용 오차 체계가 감시하고 있고, 어느 쪽이 포기했는지는 오류 메시지가 알려 준다.

### 9. MoveIt Servo: 계획이 맞지 않는 모양일 때

계획은 수백 밀리초가 걸리고 목표가 정지해 있다고 가정한다. 움직이는 대상에 대한 비주얼 서보잉이나 손으로 하는 원격 조작은 거기에 맞지 않는다. `moveit_servo`(`ros-jazzy-moveit-servo`)가 다른 모드다. 스트리밍 명령을 제어 주기로 관절 명령으로 바꾸며, 계획은 전혀 하지 않는다. joint jog(개별 관절 속도), twist(원하는 말단 속도), pose 명령을 받고, 관절 이름·위치·속도·가속도를 담은 `KinematicState`를 내거나 ROS 인터페이스로 궤적/실수 배열 토픽을 낸다. 특이점 근처와 충돌 근처에서 속도를 줄이며, 둘 다 기본으로 켜져 있고 둘 다 끌 수 있다.

교환 조건은 명시적이다. Servo는 반응적이고 선행 예측이 없어서 장애물을 우회할 수 없다. 다가가면서 느려질 뿐이다. 어딘가로 가는 데는 계획을, 무언가를 따라가는 데는 Servo를 쓴다.

### 10. 어느 언어 인터페이스가 1급인가

C++이다. `MoveGroupInterface`가 성숙한 API이고, 튜토리얼과 실제 제품 스택이 쓰는 것이며, 전체 표면을 가진 유일한 쪽이다 — `computeCartesianPath`, `attachObject`/`detachObject`, 이름 붙은 목표, 경로 제약, 실행 시 제어기 선택.

Python은 `moveit_py`(`ros-jazzy-moveit-py`)이고, 그것이 실제로 무엇인지 아는 것이 중요하다. `MoveGroupInterface`를 감싸지 **않는다**. `MoveItCpp`를 바인딩하며, `move_group` 노드를 호출하는 대신 계획 파이프라인을 당신 프로세스 안에서 돌린다.

```python
from moveit.planning import MoveItPy

robot = MoveItPy(node_name="moveit_py")
arm = robot.get_planning_component("panda_arm")

arm.set_start_state_to_current_state()
arm.set_goal_state(configuration_name="extended")

result = arm.plan()
if result:
    robot.execute(result.trajectory, controllers=[])
```

Python이 덮는 것: planning component(`set_start_state`, 이름 붙은 배치·`RobotState`·`PoseStamped`·제약으로 주는 `set_goal_state`, `set_path_constraints`, `set_workspace`), `MoveItPy.execute`를 통한 실행, planning scene monitor와 충돌 검사 API 전체, 로봇 모델과 상태, 다중 파이프라인 계획. 덮지 않는 것: Cartesian path 바인딩이 없고, attach/detach 편의 함수가 없으며, ROS 1의 `moveit_commander`는 MoveIt 2에 존재하지 않는다. 그것을 import하는 튜토리얼은 ROS 1 아카이브다. Python으로 시제품을 만들되, Cartesian 동작이나 `move_group`의 전체 표면이 필요해지면 C++을 쓰게 될 것을 예상하라.

### 11. 픽은 호출 하나가 아니라 계획 문제의 연속이다

MoveIt 2의 `MoveGroupInterface`에는 `pick()`도 `place()`도 없다. ROS 1의 파지 파이프라인은 이식되지 않았고, 그 부재는 결함이라기보다 정직함이다. 집는 일은 서로 다른 문제들의 연속이고, 그 이름을 부르는 것이 핵심이다.

1. **파지 자세를 얻는다.** 인식에서, 파지 합성기에서, 또는 치수를 잰 지그에서. *MoveIt은 이것을 하지 않는다.* [[04-robotics/grasping|15. Grasping]] 참조.
2. **pre-grasp까지 계획한다.** 접근 축을 따라 뒤로 물린 지점. 자유 공간 질의 — OMPL.
3. **접근.** 짧은 직선 동작: `fraction`을 검사하는 `computeCartesianPath`, 또는 Pilz `LIN`. 이 구간에서는 보통 그리퍼와 대상 사이 충돌을 끈다. 목표가 접촉이기 때문이다.
4. **그리퍼를 닫는다.** 별개의 제어기, 별개의 액션. *MoveIt은 파지가 성공했는지 알려 주지 않는다.* 아는 것은 손가락이 멈췄다는 사실뿐이고, 물체를 쥐고 있는지는 힘 또는 촉각의 문제다 — [[04-robotics/force-compliance-control|13. Force & Compliance Control]].
5. **물체를 붙인다.** `touch_links`와 함께 그리퍼 링크에 attach해서, 플래너가 그것을 장애물로 취급하기를 그치고 들고 다니기 시작하게 한다.
6. **후퇴, 운반, 내려놓기.** 그다음 detach하고 씬에서 제거한다.

이 목록에서 두 가지는 MoveIt 바깥이다. 1번, 그리고 4번에서 손가락이 닿은 뒤의 전부. 건설 현장에서는 그 둘이 어려운 부분이다. 마찰을 모르는 고르지 않은 바닥 위의 불규칙한 블록은 파지 합성과 힘 제어 문제이고, MoveIt의 기여는 팔이 거푸집을 치지 않고 거기까지 간다는 것뿐이다. 2–6번을 제대로 된 실패 처리와 역추적과 함께 엮는 일이 `moveit_task_constructor`(`ros-jazzy-moveit-task-constructor-core`)가 존재하는 이유이고, 손으로 쓴 시퀀스에 오류 분기가 늘어나기 시작하면 그때가 그 도구로 넘어갈 때다.

### 12. 실습: 계획하고 실행한 뒤, 기둥을 가져다 놓아라

한 자리에서, Panda 데모로. 하드웨어는 필요 없다.

1. `ros2 launch moveit_resources_panda_moveit_config demo.launch.py`. RViz의 **MotionPlanning** 디스플레이에서 **Planning Scene Topic**이 `/monitored_planning_scene`인지 확인한다.
2. **Planning** 탭에서 주황색 대화형 마커를 목표 자세로 끌고, **Plan**, 미리보기를 본 뒤 **Execute**. 모의 하드웨어 팔이 따라간다.
3. 목표를 그대로 둔 채 **Plan**을 세 번 더 누른다. 궤적이 매번 다르다. 샘플링 플래너인 OMPL의 정상 동작이다. 실물에서 놀라기 전에 지금 머리에 박아 두라.
4. source된 두 번째 터미널에서 실행이 만드는 트래픽을 본다.

```bash
ros2 topic echo /monitored_planning_scene --once
ros2 action list | grep follow_joint_trajectory
ros2 control list_controllers
```

5. 이제 장애물을 넣는다. MotionPlanning 디스플레이의 **Scene Objects** 탭에서 상자를 추가하고, 한 변 0.1 m에 높이 1 m 정도의 기둥으로 크기를 맞춘 뒤 시작과 목표 사이로 끌어다 놓는다. 다시 계획한다. 경로가 휜다. 플래너가 통과하지 못할 때까지 옮기고, RViz 상태 줄과 `move_group` 터미널의 실패 메시지를 읽는다.
6. 6절의 `apply_collision_object` 코드로 5번을 Python에서 반복하고, 상자가 RViz에 나타나는지 확인한다. 실제로 쓰게 될 루프가 그것이다. 코드로 씬을 만들고 RViz로 눈으로 확인한다.
7. 플래너를 바꾼다. **Context** 탭에서 `pilz_industrial_motion_planner` 파이프라인과 `LIN`을 고르고 같은 동작을 계획한다. OMPL은 성공하는데 `LIN`이 거부하는 지점을 보라. 그 거부는 직선이 존재하지 않는다고 플래너가 알려 주는 것이고, OMPL은 결코 주지 않는 정보다.

마지막 두 계획 중 어느 쪽을 벽 옆에서 믿겠는지, 그리고 왜인지 말할 수 있으면 끝이다.

### 13. 진단할 고장: RViz에서는 계획되는데 실행되지 않는다

가장 흔한 MoveIt 버그 신고이고, 거의 항상 8절의 이음매다. 증상: **Plan**은 성공하고 애니메이션이 돌지만 **Execute**가 즉시 실패하거나 중간에 중단된다. 아래 순서대로 점검하라. 각 항목이 한 계층씩 제거한다.

| # | 점검 | 명령 | 실패의 뜻 |
|---|---|---|---|
| 1 | 계획이 정말 성공했나 | RViz 상태 줄, `move_group` 터미널 | 어댑터 이름이 보이면 플래너는 돌지도 않았다. 제어기가 아니라 요청을 고쳐라 |
| 2 | 제어기가 로드·활성화되어 있나 | `ros2 control list_controllers` | `inactive`거나 제어기가 없으면 듣는 쪽이 없다. 제어기 spawn은 25.7의 문제다 |
| 3 | MoveIt 설정의 이름이 ros2_control에 있나 | `moveit_controllers.yaml`의 `controller_names`와 2번을 대조 | 오타면 "Unable to identify any set of controllers" — 그룹의 관절을 덮는 제어기를 못 찾은 것이다 |
| 4 | 액션 서버가 실제로 있나 | `ros2 action list \| grep follow_joint_trajectory` | 없으면 제어기가 `FollowJointTrajectory`를 서비스하지 않거나 `action_ns`가 틀렸다 |
| 5 | 관절 이름이 일치하나 | `ros2 control list_controllers -v`, MoveIt의 `joints:` 목록, SRDF 그룹 | 하나라도 어긋나면 — 이름을 바꾼 관절, 다중 팔 셀의 접두 네임스페이스 — MoveIt은 그룹과 제어기를 짝지을 수 없다 |
| 6 | 시작 상태가 현실과 맞나 | `Invalid Trajectory: start point deviates from current robot state` 메시지 | `allowed_start_tolerance`(기본 0.01)와 비교하라. 낡았거나 없는 `/joint_states`, 또는 흘러간 로봇이 이걸 만든다 |
| 7 | 제어기가 허용 오차로 거부했나 | 제어기 터미널의 `GOAL_TOLERANCE_VIOLATED` / `PATH_TOLERANCE_VIOLATED` | 제어기가 궤적을 추종하지 못했다. `constraints.<joint>.goal`과 `constraints.goal_time`을 조정하거나 속도 스케일링으로 궤적을 느리게 하라 |
| 8 | MoveIt이 시간 초과시켰나 | `execution_duration_monitoring`, `allowed_execution_duration_scaling` | 추종은 하는데 너무 느렸다. 보통 계획 문제가 아니라 힘이 모자라거나 잘못 튜닝된 제어기다 |

몸에 익힐 경계: **1번은 계획, 2–5번은 배선, 6–8번은 제어다.** 배선 실패는 조용하고 즉시 나고, 제어 실패는 부분 동작과 허용 오차 메시지를 남긴다. YAML을 고치기 전에 어느 쪽인지 아는 것이 수리의 대부분이다.

오류를 전혀 내지 않기 때문에 따로 이름을 불러 둘 것이 하나 더 있다. 낡은 planning scene에 대고 실행하는 경우다. collision object를 추가했는데 `move_group`이 받지 못했다면 — 프레임 id가 틀렸거나, 구독자가 생기기 전에 발행했거나 — 팔은 당신 스크립트에만 존재하는 기하를 자신 있게 통과해 간다. 계획 전에 `ros2 topic echo /monitored_planning_scene --once`가 2초짜리 점검이다.

### 14. 이 페이지가 다루지 않는 것

파지 자세가 어디서 오는지는 [[04-robotics/grasping|15. Grasping]], 접촉 이후에 벌어지는 일은 [[04-robotics/force-compliance-control|13. Force & Compliance Control]]. MoveIt이 명령하는 궤적 제어기와 그 아래 하드웨어 인터페이스는 [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]], SRDF가 주석을 다는 URDF와 TF는 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]. MoveIt이 플러그인으로 호출하는 IK의 수학은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]. 역추적이 있는 다단계 과제 계획은 `moveit_task_constructor`, 실행 중에 다시 계획하는 반응형 계획은 `moveit_ros/hybrid_planning`, 팔과 함께 베이스를 움직이는 문제는 내비게이션과 나란히 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- MoveIt 2 문서 — Concepts: `move_group` 노드, Motion Planning, Planning Scene Monitor, Trajectory Processing.
- MoveIt 2 문서 — MoveIt Setup Assistant 튜토리얼, Perception Pipeline 튜토리얼(octomap updater 플러그인과 `sensors_3d.yaml`), Realtime Arm Servoing 튜토리얼.
- `moveit/moveit2`(`jazzy` 브랜치) — `move_group_interface.hpp`(`computeCartesianPath` 반환 의미, deprecated된 `jump_threshold`), `planning_pipeline.cpp`(request/response 어댑터 분리), `PlanningComponent`·`MoveItCpp`·`PlanningScene`의 `moveit_py` 바인딩.
- `moveit/moveit_resources`(`ros2` 브랜치) — `panda_moveit_config`: `ompl_planning.yaml`, `pilz_industrial_motion_planner_planning.yaml`, `moveit_controllers.yaml`, `demo.launch.py`.
- `moveit/moveit2_tutorials` — Quickstart in RViz, Motion Planning Python API.
- ros2_control 문서(Jazzy) — `joint_trajectory_controller` 파라미터(`constraints.*`).
- MoveIt 바이너리 설치 안내(`ros-jazzy-moveit`), ROS 2 Jazzy 패키지 색인.

> [!question]- 스스로 점검 · 정답
> **1. RViz에서는 계획이 훌륭한데 팔이 움직이지 않는다. 첫 세 명령은?** `ros2 control list_controllers`(활성 제어기가 있나), 그 이름을 `moveit_controllers.yaml`의 `controller_names`와 대조, `ros2 action list | grep follow_joint_trajectory`(액션 서버가 있나). 셋 다 배선 계층이고, 배선 실패는 즉시 조용히 난다. 허용 오차를 건드리기 전에 여기부터 본다.
> **2. MoveIt에 URDF만으로는 왜 부족한가, 한 문장으로.** URDF는 기하와 기구학을 기술하지만 의미론을 담지 않는다. planning group도, 이름 붙은 자세도, tip link도, 비활성 충돌 쌍도 없고, 이것들은 전부 SRDF에 있으며 플래너가 요청을 받기 전에 전부 필요하다.
> **3. `computeCartesianPath`가 0.62를 돌려줬다. 무엇을 하고, 원인은 무엇일 가능성이 큰가?** 실행하지 마라. 이유가 있어 고른 직선의 62 % 지점에서 공구를 멈추는 일이 된다. 원인은 직선이 도달 가능 작업 공간을 벗어남, 특이점 근처 통과, 다른 IK 분기로 넘어감, 보간된 자세의 충돌 중 하나일 가능성이 크다. 구간을 줄이거나 방향을 바꾸거나, 부분이 아니라 깔끔하게 실패하는 Pilz `LIN`을 쓴다.
> **4. 블록을 쥐었더니 이후 모든 계획이 충돌로 실패한다. 왜인가?** 블록이 여전히 세계의 collision object이고 그리퍼가 그 안에 들어가 있다. 그리퍼 링크들을 `touch_links`로 넘기며 그리퍼 링크에 attach해서 로봇 자신의 충돌 모형으로 옮겨야 한다.
> **5. 건설 현장 픽에서 MoveIt이 풀어 주지 않는 부분은?** 파지 자세가 어디인가 — 인식으로부터의 파지 합성 — 그리고 접촉 순간 이후의 전부. MoveIt의 세계 모형은 접촉을 실패로 취급하기 때문이다. MoveIt이 푸는 것은 그 둘 사이의 충돌 없는 이동뿐이다.
