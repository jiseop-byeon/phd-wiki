---
title: "25.9 Navigation with Nav2"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Bring up Nav2 on a simulated differential-drive robot with a map, send a goal through the action interface, read the costmap and the plan in RViz, and diagnose a robot that spins in place or refuses to move."
mastery-when: "Go deeper when you are writing a planner, controller or costmap layer plugin, or porting the stack to a robot that is not flat, circular and indoors."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to configure, launch and debug the stack on a robot you did not write. Not enough to author a planner or controller plugin.
> **Working** — 직접 작성하지 않은 로봇 위에서 스택을 설정하고 띄우고 디버깅할 정도. 플래너나 제어기 플러그인을 새로 짤 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> The transform tree and RViz from [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]], a simulated base that accepts velocity commands and publishes odometry from [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]], and actions and managed nodes from [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. Baseline for every command here: **ROS 2 Jazzy Jalisco on Ubuntu 24.04 with Gazebo Harmonic**.
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]의 변환 트리와 RViz, [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]의 속도 명령을 받고 오도메트리를 내는 시뮬레이션 베이스, [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]의 액션과 관리형 노드. 이 페이지 모든 명령의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco와 Gazebo Harmonic**이다.

### 1. The problem Nav2 solves

You have a robot that takes `geometry_msgs/msg/Twist` and publishes odometry and a laser scan. You want to say "go to that corner" and have it arrive. Between those two facts sit a dozen sub-problems, and the reason Nav2 exists is that every one of them has been solved badly by hand, repeatedly:

- Where is the robot in the map, given that wheel odometry drifts?
- What does the world look like right now, combining a stored floor plan with what the laser sees this instant?
- What route exists from here to there, at map scale, avoiding walls?
- What velocity command, at 20 Hz, follows that route without hitting the person who just stepped in front of the robot?
- What should happen when there is no such command — when the robot is boxed in, the plan has expired, or the costmap has filled with phantom obstacles from a sensor glitch?

The last one is the interesting one. A stack that only answers the first four is a demo. Nav2 is a framework for building a navigation system out of swappable algorithm plugins, coordinated by an explicit, editable policy about what to do when the algorithms fail. It is the ROS 2 successor to ROS 1's `move_base`, and the parts a beginner thinks are the whole system — the planner and the controller — are perhaps a third of it.

Install it alongside a simulated TurtleBot:

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-nav2-minimal-tb\*
```

Jazzy is the first distribution where `nav2_bringup` targets modern Gazebo rather than Gazebo Classic, which is why the TurtleBot assets moved into `nav2_minimal_tb*` packages.

### 2. The behaviour-tree navigator, and why not a state machine

`bt_navigator` is the node that receives your goal. It does not plan or control. It ticks a **behaviour tree** whose leaves are action clients calling the other servers. Nav2 uses BehaviorTree.CPP V4; the tree is an XML file loaded at runtime, and the leaf nodes are pluginlib plugins registered by name.

The default tree for a single goal is `navigate_to_pose_w_replanning_and_recovery.xml`, and its top two nodes tell you the whole design:

```xml
<RecoveryNode number_of_retries="6" name="NavigateRecovery">
  <PipelineSequence name="NavigateWithReplanning">
    ...
  </PipelineSequence>
  ...
</RecoveryNode>
```

Two control-flow types carry most of the meaning:

- **`PipelineSequence`** ticks the first child until it succeeds, then ticks the first *and* second, then the first, second and third, and so on. This is what makes navigation *continuous rather than sequential*: the planner keeps being re-ticked (once per second, in the default tree) while the controller is running, so the path is replanned underneath a robot that is already moving.
- **`RecoveryNode`** has exactly two children. It returns SUCCESS only if the first child succeeds. If the first fails, the second runs; if the second succeeds, the first is retried; if the second fails, the whole node fails. `number_of_retries` bounds the loop.

Why this rather than a finite state machine. In an FSM, "if the controller fails, clear the local costmap and try again, but if a new goal arrived, abandon the recovery immediately" is a transition — and every such rule multiplies against every state it could fire from. The official framing is that an FSM encoding of a comparably rich behaviour needs dozens of states and hundreds of transitions, because primitives cannot be reused across contexts.

What the tree buys when recovery is needed is specifically this: **recovery is scoped.** The default tree wraps the planner in its own `RecoveryNode` whose recovery is *clear the global costmap*, and the controller in its own whose recovery is *clear the local costmap*. Only when those contextual recoveries are exhausted does execution fall into the system-level recovery subtree — clear both costmaps, spin, wait, back up — retrying the whole navigation subtree after each one. A `GoalUpdated` condition sits in the reactive fallbacks so a new goal preempts a recovery in progress. You can read the policy, edit it, and hand a different XML file per goal via the action's `behavior_tree` field.

### 3. The servers, and what each owns

Nav2 is a set of separate nodes, each hosting a map of named algorithm plugins behind an action interface.

| Node | Owns | Default plugin in `nav2_params.yaml` |
|---|---|---|
| `planner_server` | the global costmap; computes a path | `GridBased` → `nav2_navfn_planner::NavfnPlanner` |
| `controller_server` | the local costmap; emits velocity commands | `FollowPath` → `nav2_mppi_controller::MPPIController` |
| `smoother_server` | refines a path after planning | `simple_smoother` → `nav2_smoother::SimpleSmoother` |
| `behavior_server` | spin, back up, drive-on-heading, wait, assisted teleop | `nav2_behaviors::Spin`, `::BackUp`, `::DriveOnHeading`, `::Wait`, `::AssistedTeleop` |
| `bt_navigator` | the behaviour tree; the goal-facing action | `nav2_bt_navigator::NavigateToPoseNavigator` |

Three points that are easy to miss. First, the plugin **name** is an alias and the plugin **type** is the implementation: DWB configured under the name `FollowPath` means every DWB parameter lives at `FollowPath.<param>`, and the behaviour tree asks for `FollowPath` without knowing which algorithm answers. Swapping controllers is a config edit, not a tree edit.

Second, the servers own the costmaps, not the other way round. Everything that needs the local costmap lives in or subscribes to the controller server's copy — the behaviour server subscribes to `local_costmap/costmap_raw` rather than building its own — because a duplicated costmap is expensive.

Third, "recovery server" is the older name. In current Nav2 it is the **behaviour server**, because the same infrastructure hosts behaviours that are not recoveries at all (assisted teleop, docking approaches). Each behaviour plugin exposes its *own* action server, since there is no single interface that fits "spin 1.57 radians" and "back up 15 cm".

### 4. Costmaps and the layered model

The environmental representation is a `nav2_costmap_2d::Costmap2D`: a regular 2D grid whose cells carry a cost — unknown, free, occupied, or inflated. Planners search it; controllers sample it.

There are two, with different jobs and different frames:

- **Global costmap** — `global_frame: map`, sized to the map, `update_frequency: 1.0`, `track_unknown_space: true`. It is what the planner searches.
- **Local costmap** — `global_frame: odom`, a rolling window (3 m × 3 m by default), `update_frequency: 5.0`. It is what the controller samples. It lives in `odom` deliberately: the controller must keep working smoothly through an AMCL correction that jumps the `map` frame.

Each costmap is built by a stack of **layers**, which are pluginlib plugins applied in the listed order:

| Layer | Type | What it contributes |
|---|---|---|
| Static | `nav2_costmap_2d::StaticLayer` | the stored map from `map_server`, as the base |
| Obstacle | `nav2_costmap_2d::ObstacleLayer` | 2D marking and raytrace clearing from `LaserScan` or `PointCloud2` sources |
| Voxel | `nav2_costmap_2d::VoxelLayer` | the same, but buffering into a 3D voxel grid and projecting down, so overhangs and low obstacles are handled |
| Inflation | `nav2_costmap_2d::InflationLayer` | cost gradient around lethal cells |

The Jazzy defaults are `["static_layer", "obstacle_layer", "inflation_layer"]` for the global costmap and `["voxel_layer", "inflation_layer"]` for the local one. Order matters: inflation is last because it reads whatever the layers below it wrote.

Your robot's shape enters here, as either `robot_radius` (a circle) or `footprint` (a polygon). The maintainers' guidance is that a non-circular robot should give the real polygon, because several planners and all current controllers do full SE(2) footprint collision checking and will plan into tighter spaces with it. Three exceptions where a radius is still right: the robot is tiny relative to the environment, compute is too limited for SE(2) checking, or you are using a holonomic planner (NavFn, Theta\*, Smac 2D) that ignores the footprint anyway.

### 5. What the inflation radius actually does

Beginners read `inflation_radius` as a safety margin: "keep the robot this far from walls." That is not what it is, and reading it that way produces the single most common misconfiguration in the ecosystem.

Two distinct things are happening in the inflation layer. It writes a **lethal** cost within the robot's fully inscribed radius of an obstacle — that is the collision-avoidance part, and it is derived from your footprint, not from `inflation_radius`. Then, out to `inflation_radius`, it writes an **exponentially decaying** cost with `cost_scaling_factor` as the decay rate. Defaults are `inflation_radius: 0.55` and `cost_scaling_factor: 10.0` in the plugin, and `0.7` / `3.0` in the Jazzy TurtleBot configuration.

That decaying skirt is not a safety margin. It is a **potential field that steers search**. NavFn, Theta\* and the Smac planners are cost-aware: given a smooth gradient they will run down the middle of a corridor and give obstacles a wide berth long before the search ever touches them. Given a thin inflation ring around the walls and a large zero-cost void in between, they have nothing to prefer inside the void, and produce paths that hug one wall or cut corners for no reason.

The maintainers say this directly in the tuning guide: most configuration files they see miss the point of the inflation layer, and the recommendation is to *increase* the cost scale and radius until there is a smooth potential across the whole traversable width. Large open rooms may keep a zero-cost middle; halls and aisles should not. So the practical rule is the inverse of the beginner's: if your robot is clipping corners or riding a wall, your inflation is probably too *small*, not too large.

The cost of over-inflating is real and worth naming: inflate further than the narrowest gap the robot must pass and that gap fills with high cost or becomes unplannable, and the robot refuses doorways it physically fits through. Section 13 uses exactly that symptom.

### 6. Global planners and local controllers

The division is: the **planner** answers "what route exists, at map scale, given everything I know", once per replan; the **controller** answers "what velocity right now, given the last metre of that route and what the sensors see this instant", at `controller_frequency` (20 Hz by default).

Planners available in Jazzy, with the maintainers' robot-type guidance:

| Planner | Suits |
|---|---|
| `nav2_navfn_planner::NavfnPlanner` | circular differential or omnidirectional bases; Dijkstra or A\* on the grid; broad sweeping curves |
| Theta\* (`nav2_theta_star_planner`) | the same bases, when you prefer straight lines at arbitrary angles |
| Smac 2D | the same bases; classical A\* with cost-aware penalties |
| Smac Hybrid-A\* | non-circular or circular Ackermann and legged bases; kinematically feasible SE(2) paths |
| Smac State Lattice | non-circular differential or omnidirectional, and arbitrary bases |

The dividing question is not "which is best" but "can my robot drive the path this produces". The first three are holonomic: they will happily return a path with a 90° corner, which a differential base can execute only by stopping and pivoting, and an Ackermann base cannot execute at all. The Smac feasible planners respect the starting heading and the turning constraints, so the path is drivable as written.

Controllers:

- **DWB** (`dwb_core`, the ROS 2 rewrite of DWA) samples forward trajectories within velocity and acceleration limits and scores each against **critic** plugins — `PathAlign`, `GoalDist`, `BaseObstacle`, `Oscillation`, `PreferForward` and others, each with a tunable weight. Differential and omnidirectional bases. Right when you need to know exactly why a trajectory was chosen, because the score decomposes; costly because its behaviour is a function of about a dozen weights you must tune.
- **MPPI** (`nav2_mppi_controller::MPPIController`) is the Jazzy default and optimisation-based: it perturbs the previous optimal trajectory with noise, rolls out a batch (2000 samples over 56 steps at `model_dt: 0.05` by default), and weights them against critic objective functions. Handles dynamic agents considerably better than DWB's constant-action rollouts, usually works untuned, costs moderately more compute. Differential, omnidirectional, Ackermann and legged.
- **Regulated Pure Pursuit** is geometric: pick a lookahead point on the path and steer at it, with regulation that slows the robot near obstacles and in sharp turns. It does *not* deviate from the path to avoid dynamic obstacles. Use it when you want exact path following and you trust the path — so pair it with a feasible planner, or with a differential base that can pivot onto any heading.

A fourth worth knowing: the **Rotation Shim** controller wraps another and rotates the robot in place toward the new path's heading before handing over. It exists because holonomic planners produce paths whose initial heading differs sharply from the robot's, and a controller tuned for accurate tracking handles that badly — spiralling out, or whipping around. Unnecessary with a feasible planner, which already starts from your current heading.

### 7. Localisation: AMCL and the map → odom → base_link chain

[[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]] built the transform tree below `base_link`. Nav2 requires the two transforms above it, and REP 105 fixes who publishes what:

$$ \texttt{map} \rightarrow \texttt{odom} \rightarrow \texttt{base\_link} \rightarrow [\text{sensor frames}] $$

- `odom` → `base_link` is published by the **odometry system**. It must be smooth and continuous; it is allowed to drift without bound.
- `map` → `odom` is published by the **global positioning system** — AMCL, SLAM Toolbox, motion capture, GNSS fusion. It is allowed to jump; it exists precisely to absorb the odometry's accumulated drift.
- Everything below `base_link` is static and comes from your URDF.

Nav2 ships `nav2_amcl`, Adaptive Monte Carlo Localization: a particle filter over a static occupancy grid served by `map_server`. Each particle is a pose hypothesis; each scan reweights them under a sensor model (`laser_model_type: "likelihood_field"` by default) and a motion model (`robot_model_type: "nav2_amcl::DifferentialMotionModel"`). It runs between 500 and 2000 particles and only updates when the robot has moved `update_min_d: 0.25` m or `update_min_a: 0.2` rad, because a stationary robot gains no information. Its output *is* the `map` → `odom` transform, published because `tf_broadcast: true`.

Two consequences follow, and both bite. AMCL needs an initial pose — that is what RViz's **2D Pose Estimate** button publishes on `/initialpose`, and until you give it one the `map` → `odom` link does not exist and Nav2 cannot start navigating. And AMCL tracks; it does not, in its default configuration, globally relocalise. `recovery_alpha_slow` and `recovery_alpha_fast` default to `0.0`, which disables the random-particle injection that could recover from a kidnapped robot. A robot picked up and moved will stay confidently wrong until you re-estimate.

Nothing requires AMCL, or a lidar. Any source that publishes a valid `map` → `odom` satisfies the contract. SLAM Toolbox is the default when you have no map yet; `robot_localization` is the usual way to fuse wheel odometry, IMU and visual odometry into the `odom` → `base_link` half.

### 8. Lifecycle management, and why managed nodes

Every Nav2 server is a **managed (lifecycle) node** in the sense of [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]: unconfigured → inactive → active, with configuration done in a transition rather than in the constructor.

The reason is ordering. A controller that activates before the costmap has a map, or before the transform tree is complete, does not fail cleanly — it publishes garbage or blocks. Managed nodes let the bringup impose a deterministic order and a deterministic teardown.

`nav2_lifecycle_manager` does that imposing. It takes an ordered `node_names` list, transitions each into configured then active in order, and brings them down in reverse:

```yaml
lifecycle_manager:
  ros__parameters:
    autostart: true
    node_names: ['controller_server', 'planner_server', 'behavior_server', 'bt_navigator', 'waypoint_follower']
    bond_timeout: 4.0
    attempt_respawn_reconnection: true
    bond_respawn_max_duration: 10.0
```

It also holds a **bond** with each server — a heartbeat. If a server crashes or stops responding for `bond_timeout` seconds, the manager transitions the *entire stack* down rather than leaving a robot driving on a half-dead navigation system. That is a safety decision, and it is why a single crashed node takes the whole stack with it. With `autostart: false` nothing activates until you press **Startup** in the RViz Nav2 panel, which is the behaviour you want while debugging.

```bash
ros2 lifecycle list /planner_server
ros2 lifecycle get /controller_server
```

### 9. Costmap filters and keepout zones

Sometimes the constraint is not physical. A corridor is fine to drive through but you do not want robots in it during working hours; a lab bay is off limits; a stretch near a loading dock needs a speed cap.

A **costmap filter** encodes that as a second annotated image — a **filter mask**, the same format as a map, not necessarily the same size or pose — published by a `map_server` instance alongside a `nav2_costmap_2d::CostmapFilterInfo` message from the **Costmap Filter Info Server** that says how mask pixel values map into the filter's own space. Filters are costmap plugins, but they go in a separate `filters:` list rather than `plugins:`:

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      filters: ["keepout_filter"]
      keepout_filter:
        plugin: "nav2_costmap_2d::KeepoutFilter"
        enabled: True
        filter_info_topic: "/costmap_filter_info"
```

`KeepoutFilter` writes cost into the costmap from the mask, so planners will not route through marked areas. `SpeedFilter` caps velocity in marked areas instead of blocking them. `BinaryFilter` toggles a boolean topic on entering a zone, for anything else you want to trigger.

One documented trap: **filters do not get the inflation layer applied to them**, because inflating a speed zone is meaningless. Some feasible planners check the cost at the robot's centre point as a cheap pre-filter before running the full SE(2) footprint check, so an un-inflated keepout zone is respected for the robot's centre but not its extremities. If you need the whole footprint kept out, add an inflation layer that covers the filter.

The advantage over editing the map file is that the mask is a separate layer of authority: the map describes what is there, the mask describes what you have decided. You can change policy without corrupting the thing localisation depends on.

### 10. Sending a goal as an action, and what the feedback carries

`bt_navigator` exposes `/navigate_to_pose`, of type `nav2_msgs/action/NavigateToPose`. Actions are the right pattern here for the reasons in 25.3: navigation takes minutes, you want progress while it runs, and you must be able to cancel.

```bash
ros2 action list -t
ros2 action info /navigate_to_pose -t
```

The goal is a pose and, optionally, the name of a behaviour tree to use for this goal:

```text
# goal
geometry_msgs/PoseStamped pose
string behavior_tree
```

Send one from the command line — this is the same thing RViz's **Nav2 Goal** tool does:

```bash
ros2 action send_goal --feedback /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.5, y: 0.5, z: 0.0}, orientation: {w: 1.0}}}}"
```

The feedback, streamed while it drives:

```text
geometry_msgs/PoseStamped current_pose
builtin_interfaces/Duration navigation_time
builtin_interfaces/Duration estimated_time_remaining
int16 number_of_recoveries
float32 distance_remaining
```

`number_of_recoveries` is the field that earns its place. Everything else tells you the robot is making progress; that one tells you *how hard the tree is working to make it*. A run that completes with three recoveries is not a success you should ship — it is a configuration problem that happened to resolve. Log it.

The result carries `error_code` and `error_msg`. The codes are namespaced per server — the planner's occupy 200–208 (`START_OCCUPIED`, `GOAL_OUTSIDE_MAP`, `NO_VALID_PATH`), the controller's 100–107 (`FAILED_TO_MAKE_PROGRESS`, `NO_VALID_CONTROL`, `TF_ERROR`) — so a failed goal names which server gave up and why.

From Python, `nav2_simple_commander` wraps all of this:

```python
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

rclpy.init()
nav = BasicNavigator()
nav.waitUntilNav2Active()      # if autostarted; else lifecycleStartup()
nav.goToPose(goal_pose)        # non-blocking
while not nav.isTaskComplete():
    feedback = nav.getFeedback()
result = nav.getResult()       # TaskResult.SUCCEEDED / CANCELED / FAILED
```

`goToPose` is deliberately non-blocking, which is what lets a single-threaded application poll feedback and call `nav.cancelTask()` on its own criteria.

### 11. Scope: what assumes a flat, mapped, indoor world

Being precise here matters more than it looks, because Nav2 demos transfer badly and the failure is quiet.

Assumes flat, mapped and indoor:

- **The 2D costmap itself.** Cost per cell in a plane, with no notion of slope, roughness, step height or surface type. A 20° grass ramp and a polished floor are indistinguishable to it; so are a kerb and a wall.
- **AMCL over a static occupancy grid.** A stored map assumed not to change, and a horizontal scan assumed to hit walls rather than tall grass.
- **The obstacle and voxel layers' clearing model.** Raytrace clearing assumes free space between the sensor and the return. On uneven ground the beam hits the ground ahead and marks it as an obstacle — the classic phantom-wall-on-a-ramp failure.
- **`DiffDrive` kinematics and near-zero-cost free space.** The default MPPI motion model and the planner/controller split assume the robot can be commanded anywhere the cost is low.

Transfers unchanged to outdoor and construction sites: the behaviour-tree architecture, the server/plugin split, lifecycle management and the action interface, none of which know anything about terrain; the `map` → `odom` → `base_link` contract, so swapping AMCL for GNSS/IMU fusion leaves everything above it working; costmap filters, which are how site rules actually get encoded; and MPPI and RPP as tracking algorithms, given a costmap that means something.

What must be replaced is the environmental representation: a map whose cell values encode whether terrain can be driven, not whether it is occupied. That is a different problem with its own literature, and this wiki treats it in [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]. The Nav2 documentation acknowledges the gap itself, listing gradient maps, 3D costmaps and mesh maps as other environmental representations. Read that page rather than assuming an inflation-radius tweak will get you there.

### 12. Exercise: a goal, a costmap and a plan

One sitting. Everything is simulated; a differential-drive TurtleBot with a prebuilt map.

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

`headless` defaults to `true`, which starts the simulation without the 3D view; `False` gives you Gazebo and RViz side by side.

1. **Localise.** The robot does not know where it is. Find it in the Gazebo world, then in RViz click **2D Pose Estimate** and click-drag at the matching spot on the map — the drag sets orientation. The particle cloud on `/particle_cloud` appears and the map snaps into place. If autostart is off, press **Startup** in the Nav2 panel first.
2. **Inspect the graph before you drive.** In a second sourced terminal:

```bash
ros2 node list
ros2 action list -t
ros2 topic hz /local_costmap/costmap
```

3. **Set up the displays.** The four that matter, and they are in the default RViz config: `/global_costmap/costmap` (Map display), `/local_costmap/costmap`, `/plan` (Path), `/local_plan` (Path). Toggle the two costmaps on and off and note that the local one is a small square that follows the robot.
4. **Send the goal from the command line**, not the RViz button, so you see the feedback:

```bash
ros2 action send_goal --feedback /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.5, y: 0.5, z: 0.0}, orientation: {w: 1.0}}}}"
```

Watch `distance_remaining` fall and `number_of_recoveries` stay at zero.

5. **Watch the replanning.** `/plan` is recomputed roughly once a second while the robot drives — the whole path twitches. `/local_plan` is the controller's short trajectory, updating at 20 Hz.
6. **Make it recover on purpose.** In Gazebo, drag a box into the corridor ahead of the robot while it is driving. The voxel layer marks it, the local costmap changes, and MPPI deviates around it. Now box the robot in completely. The controller fails, the tree clears the local costmap, retries, then falls into the recovery subtree — you will see the robot spin and back up, and `number_of_recoveries` increment in your feedback stream.
7. **Cancel.** Ctrl+C the `send_goal` command mid-run and confirm the robot stops. That is the action's cancel path, not a crash.

You are done when you can point at the screen and say which node published each of those four topics, and what the local costmap is in `odom` rather than `map` for.

### 13. The failure to diagnose: the robot spins in place, or will not move at all

This is the characteristic Nav2 failure, and it has four common causes that look identical from the outside. Check them in this order, because each check is cheaper than the next and rules out the ones after it.

**First, the transform tree.** More than half of these are a TF problem, and every downstream component fails silently when TF does.

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
ros2 run tf2_ros tf2_monitor map base_link
```

`view_frames` writes a PDF of the tree with per-edge rates. Look for: a missing `map` → `odom` (AMCL never got an initial pose, or is not running), a *disconnected* tree in two pieces, or `tf2_monitor` reporting an average delay larger than the consumers' `transform_tolerance` (0.1 s for the behaviour server and MPPI, 1.0 s for AMCL). A stale transform makes the controller reject every trajectory, which presents as a robot that will not move. If the tree is wrong, stop here — [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]] is where you fix it.

**Second, the costmap content.** Look at `/local_costmap/costmap` in RViz. Two diagnostic pictures:

- *The robot is sitting inside lethal or inflated cost.* No trajectory is valid, so it spins, backs up and spins again. Causes: the laser is mounted with the wrong transform and sees the robot's own chassis; `max_obstacle_height` is letting the ground plane in; the obstacle layer marked a transient and never cleared it because `raytrace_max_range` (3.0 m) is too short to clear what `obstacle_max_range` (2.5 m) marked.
- *The costmap is empty or not updating.* Check the source topic arrives — `ros2 topic hz /scan` — and that `observation_sources` names it.

Clear it by hand to test the hypothesis:

```bash
ros2 service call /global_costmap/clear_entirely_global_costmap nav2_msgs/srv/ClearEntireCostmap
ros2 service call /local_costmap/clear_entirely_local_costmap nav2_msgs/srv/ClearEntireCostmap
```

If clearing makes the robot move, the problem is what is writing into the costmap, not the planner.

**Third, the footprint.** Display `/local_costmap/published_footprint` in RViz and compare it with the robot. A `robot_radius` that is too large — or a `footprint` polygon in the wrong units or centred on the wrong frame — makes the inscribed-radius lethal region swallow the robot's own cell, so the robot believes it is in collision standing still. That is exactly the spin-forever symptom. Section 5's over-inflation case lands here too: if the robot refuses a doorway it fits through, check `inflation_radius` against half the door width minus the inscribed radius.

**Fourth, the controller parameters.** Only now:

- `min_x_velocity_threshold` / `min_theta_velocity_threshold` set so high the computed command is treated as zero.
- Velocity limits (`vx_max`, `wz_max` for MPPI) that cannot achieve the required turn, so no sampled trajectory reaches the goal region.
- `xy_goal_tolerance` / `yaw_goal_tolerance` too tight — the robot arrives, cannot satisfy the yaw tolerance, and oscillates around the goal forever.
- A holonomic planner feeding a controller with no rotation shim, so the robot whips or spirals at every new path.

```bash
ros2 param get /controller_server FollowPath.vx_max
ros2 param dump /controller_server
```

The ordering is the point. A parameter you change before checking TF is a parameter you will have to change back.

### 14. What this page does not cover

Building the map in the first place — SLAM Toolbox, and the `map_server` save cycle — is a separate exercise; the Nav2 first-time robot setup guide covers it. Writing your own planner, controller or costmap layer plugin is the next step past this page and has its own Nav2 tutorials. The waypoint follower, the collision monitor, the velocity smoother and the docking server are all part of the stack and none of them appear here. Multi-robot bringup with namespaces is in `nav2_bringup` but not in this page.

For the algorithms underneath — search, sampling, MPC, and what optimality means for a path — see [[04-robotics/planning-decision-making|4. Planning & Decision-Making]]. For where navigation meets an arm on the same base, see [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]]. For terrain that a 2D occupancy grid cannot describe, see [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]. The rest of the track is [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- Nav2 documentation (Jazzy) — Navigation Concepts: Navigation Servers; Environmental Representation; State Estimation; Behavior Trees.
- Nav2 documentation (Jazzy) — Getting Started: Quickstart.
- Nav2 documentation (Jazzy) — Configuration Guide: Inflation Layer; Obstacle Layer; Voxel Layer; Static Layer; Keepout Filter; Lifecycle Manager; Behavior Tree Navigator; Costmap 2D.
- Nav2 documentation (Jazzy) — Behavior Tree nodes: RecoveryNode; PipelineSequence; Navigate To Pose with replanning and recovery.
- Nav2 documentation (Jazzy) — Tuning Guide (inflation potential fields, footprint vs radius, planner and controller plugin selection); Simple Commander API.
- `ros-navigation/navigation2`, `jazzy` branch — `nav2_msgs/action/NavigateToPose.action`, `FollowPath.action`, `ComputePathToPose.action`; `nav2_bringup/params/nav2_params.yaml`; `nav2_bringup/rviz/nav2_default_view.rviz`.
- REP 105, Coordinate Frames for Mobile Platforms.
- `ros2/geometry2`, `jazzy` branch — `tf2_tools` and `tf2_ros` executables.

> [!question]- Self-check · Answer
> **1. Why is the local costmap in the `odom` frame when the global one is in `map`?** Because `map` → `odom` is published by AMCL and is allowed to jump when localisation corrects. A controller running at 20 Hz on top of a frame that teleports would produce discontinuous commands. `odom` drifts but is smooth, which is what short-horizon control needs; the planner, which cares about global consistency and replans once a second, takes the jumpy frame instead.
> **2. Your robot clips corners and hugs walls, though it never collides. What is the likely cause and which direction do you change it?** Inflation that is too small, not too large. The decaying inflation cost is a potential field that steers cost-aware planners toward the middle of free space; a thin ring around walls leaves a large zero-cost void the planner has no reason to prefer any part of. Increase `inflation_radius` and `cost_scaling_factor` until there is a smooth gradient across the traversable width — while checking that the narrowest gap the robot must pass is still plannable.
> **3. The robot spins in place and never departs. What do you check first, and why not the controller parameters?** The transform tree: `ros2 run tf2_tools view_frames` and `ros2 run tf2_ros tf2_monitor map base_link`. A missing `map` → `odom` or a transform older than `transform_tolerance` makes every trajectory invalid, and it produces exactly this symptom with no error that names TF. Costmap content and footprint come next; controller parameters are fourth because a parameter changed before TF is verified is a parameter you will change back.
> **4. Why a behaviour tree rather than a state machine, given that the nominal path is just "plan, then follow"?** Because the nominal path is not the hard part. Recovery is, and in an FSM every recovery rule is a transition that must be duplicated for every state it can fire from. The tree scopes recovery: a `RecoveryNode` around the planner clears the global costmap, one around the controller clears the local costmap, and only a system-level failure reaches the shared spin/wait/back-up subtree. It is also editable as data — a different XML per goal, via the action's `behavior_tree` field — rather than as compiled control flow.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 남이 만든 로봇 위에서 스택을 설정하고 띄우고 디버깅할 정도. 플래너나 제어기 플러그인을 직접 작성할 정도는 아니다.
> **Working** — enough to configure, launch and debug the stack; not to author a planner or controller plugin.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]의 변환 트리와 RViz, [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]의 속도 명령을 받고 오도메트리를 내는 시뮬레이션 베이스, [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]의 액션과 관리형 노드. 이 페이지 모든 명령의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco와 Gazebo Harmonic**이다.
> TF and RViz from 25.6, a simulated base from 25.7, actions and managed nodes from 25.3. Baseline: ROS 2 Jazzy on Ubuntu 24.04 with Gazebo Harmonic.

### 1. Nav2가 푸는 문제

`geometry_msgs/msg/Twist`를 받고 오도메트리와 레이저 스캔을 내보내는 로봇이 있다. "저 구석으로 가라"고 말하면 도착하게 만들고 싶다. 그 두 사실 사이에 하위 문제가 열 몇 개 있고, Nav2가 존재하는 이유는 그 하나하나를 사람들이 반복해서 엉성하게 풀어 왔기 때문이다.

- 바퀴 오도메트리가 표류하는데, 지도 위에서 로봇은 어디에 있는가?
- 저장된 평면도와 레이저가 지금 보는 것을 합치면, 세계는 지금 어떻게 생겼는가?
- 지도 규모에서 벽을 피해 여기서 저기로 가는 경로는 무엇인가?
- 방금 앞을 가로막은 사람을 치지 않으면서 그 경로를 따라가는 20 Hz 속도 명령은 무엇인가?
- 그런 명령이 없을 때 — 로봇이 갇혔거나, 경로가 만료됐거나, 센서 오류로 costmap이 유령 장애물로 가득 찼을 때 — 무슨 일이 일어나야 하는가?

마지막 것이 중요하다. 앞의 넷만 답하는 내비게이션 스택은 데모다. Nav2는 교체 가능한 알고리즘 플러그인으로 내비게이션 시스템을 조립하고, 알고리즘이 실패했을 때 무엇을 할지에 대한 명시적이고 편집 가능한 정책으로 그것들을 조율하는 프레임워크다. ROS 1 `move_base`의 ROS 2 후계이고, 초심자가 시스템 전부라고 생각하는 부분 — 플래너와 제어기 — 은 아마 3분의 1쯤이다.

시뮬레이션 TurtleBot과 함께 설치한다.

```bash
sudo apt update
sudo apt install ros-jazzy-navigation2 ros-jazzy-nav2-bringup
sudo apt install ros-jazzy-nav2-minimal-tb\*
```

Jazzy는 `nav2_bringup`이 Gazebo Classic이 아니라 현대 Gazebo를 대상으로 하는 첫 배포판이고, 그래서 TurtleBot 자산이 `nav2_minimal_tb*` 패키지로 옮겨졌다.

### 2. 행동 트리 내비게이터, 그리고 왜 상태 기계가 아닌가

목표를 받는 노드는 `bt_navigator`다. 이 노드는 계획도 제어도 하지 않는다. **행동 트리(behaviour tree)** 를 tick하고, 그 잎 노드들이 다른 서버를 호출하는 액션 클라이언트다. Nav2는 BehaviorTree.CPP V4를 쓴다. 트리는 런타임에 로드되는 XML 파일이고, 잎 노드는 이름으로 등록된 pluginlib 플러그인이다.

단일 목표에 대한 기본 트리는 `navigate_to_pose_w_replanning_and_recovery.xml`이고, 최상위 두 노드가 설계 전부를 말해 준다.

```xml
<RecoveryNode number_of_retries="6" name="NavigateRecovery">
  <PipelineSequence name="NavigateWithReplanning">
    ...
  </PipelineSequence>
  ...
</RecoveryNode>
```

의미의 대부분은 제어 흐름 노드 두 종류가 지고 있다.

- **`PipelineSequence`** 는 첫 자식이 성공할 때까지 tick하고, 그다음 첫째와 *둘째* 를 tick하고, 그다음 첫째·둘째·셋째를 tick하는 식으로 간다. 이것이 내비게이션을 *순차가 아니라 연속* 으로 만드는 장치다. 제어기가 도는 동안에도 플래너가 계속 다시 tick되므로(기본 트리에서 1초에 한 번), 이미 움직이고 있는 로봇 발밑에서 경로가 다시 계산된다.
- **`RecoveryNode`** 는 자식이 정확히 둘이다. 첫 자식이 성공할 때만 SUCCESS를 낸다. 첫 자식이 실패하면 둘째가 실행되고, 둘째가 성공하면 첫째를 다시 시도하고, 둘째가 실패하면 노드 전체가 실패한다. `number_of_retries`가 그 반복 횟수를 제한한다.

왜 유한 상태 기계가 아닌가. FSM에서 "제어기가 실패하면 지역 costmap을 지우고 다시 시도하되, 새 목표가 들어오면 복구를 즉시 포기한다"는 전이(transition)다. 그리고 그런 규칙 하나하나가 그것이 발동할 수 있는 모든 상태와 곱해진다. 공식 설명은 비슷한 수준의 로봇 행동을 FSM으로 인코딩하면 상태 수십 개와 전이 수백 개가 필요하다는 것이다. 원시 동작을 문맥 사이에서 재사용할 수 없기 때문이다.

복구가 필요할 때 트리가 사 주는 것은 구체적으로 이것이다: **복구에 범위가 생긴다.** 기본 트리는 플래너를 자기 `RecoveryNode`로 감싸고 그 복구는 *전역 costmap 지우기*, 제어기를 자기 `RecoveryNode`로 감싸고 그 복구는 *지역 costmap 지우기* 다. 이 문맥별 복구가 소진되어야 비로소 시스템 수준 복구 서브트리 — 양쪽 costmap 지우기, 제자리 회전, 대기, 후진 — 로 떨어지고, 각 복구 뒤에 내비게이션 서브트리 전체를 재시도한다. reactive fallback 안의 `GoalUpdated` 조건 덕분에 새 목표는 진행 중인 복구가 끝나기를 기다리지 않고 선점한다. 이 정책은 읽을 수 있고, 편집할 수 있고, 액션의 `behavior_tree` 필드로 목표마다 다른 XML을 넘길 수 있다.

### 3. 서버들, 그리고 각각이 소유하는 것

Nav2는 별개 노드들의 집합이고, 각각은 이름 붙은 알고리즘 플러그인들의 맵을 액션 인터페이스 뒤에 둔다.

| 노드 | 소유하는 것 | `nav2_params.yaml`의 기본 플러그인 |
|---|---|---|
| `planner_server` | 전역 costmap. 경로를 계산한다 | `GridBased` → `nav2_navfn_planner::NavfnPlanner` |
| `controller_server` | 지역 costmap. 속도 명령을 낸다 | `FollowPath` → `nav2_mppi_controller::MPPIController` |
| `smoother_server` | 계획 뒤 경로를 다듬는다 | `simple_smoother` → `nav2_smoother::SimpleSmoother` |
| `behavior_server` | 회전, 후진, 헤딩 주행, 대기, assisted teleop | `nav2_behaviors::Spin`, `::BackUp`, `::DriveOnHeading`, `::Wait`, `::AssistedTeleop` |
| `bt_navigator` | 행동 트리. 목표를 받는 액션 | `nav2_bt_navigator::NavigateToPoseNavigator` |

놓치기 쉬운 점 셋. 첫째, 플러그인 **이름** 은 별칭이고 플러그인 **타입** 이 구현이다. DWB를 `FollowPath`라는 이름으로 설정하면 DWB의 모든 파라미터는 `FollowPath.<param>`에 놓이고, 행동 트리는 어떤 알고리즘이 답하는지 모른 채 `FollowPath`를 요청한다. 제어기 교체는 설정 수정이지 트리 수정이 아니다.

둘째, costmap을 서버가 소유하지 그 반대가 아니다. 지역 costmap이 필요한 모든 것은 제어기 서버의 사본에 얹히거나 그것을 구독한다 — behavior server는 자기 costmap을 만들지 않고 `local_costmap/costmap_raw`를 구독한다 — costmap 복제가 비싸기 때문이다.

셋째, "recovery server"는 옛 이름이다. 현재 Nav2에서는 **behavior server**이고, 같은 인프라가 복구가 아닌 행동(assisted teleop, 도킹 접근)도 담기 때문이다. 각 behavior 플러그인은 *자기 자신의* 액션 서버를 노출한다. "1.57 rad 회전"과 "15 cm 후진"을 함께 담을 단일 인터페이스가 없기 때문이다.

### 4. Costmap과 계층 모델

환경 표현은 `nav2_costmap_2d::Costmap2D`다. 각 칸이 비용 — 미지, 자유, 점유, 팽창 — 을 담는 규칙적인 2D 격자다. 플래너는 이것을 탐색하고, 제어기는 표본을 뽑는다.

일 목적과 프레임이 다른 두 개가 있다.

- **전역 costmap** — `global_frame: map`, 지도 크기, `update_frequency: 1.0`, `track_unknown_space: true`. 플래너가 탐색하는 대상이다.
- **지역 costmap** — `global_frame: odom`, 롤링 윈도(기본 3 m × 3 m), `update_frequency: 5.0`. 제어기가 표본을 뽑는 대상이다. `odom`에 있는 것은 의도적이다. AMCL 보정이 `map` 프레임을 튀게 만드는 동안에도 제어기는 매끄럽게 계속 돌아야 한다.

각 costmap은 나열된 순서대로 적용되는 pluginlib 플러그인인 **계층(layer)** 들이 쌓아 만든다.

| 계층 | 타입 | 기여하는 것 |
|---|---|---|
| Static | `nav2_costmap_2d::StaticLayer` | `map_server`가 주는 저장된 지도를 바탕으로 |
| Obstacle | `nav2_costmap_2d::ObstacleLayer` | `LaserScan`이나 `PointCloud2` 소스로부터의 2D 마킹과 레이 추적 소거 |
| Voxel | `nav2_costmap_2d::VoxelLayer` | 같은 일을 3D 복셀 격자에 버퍼링한 뒤 투영. 머리 위 장애물과 낮은 장애물을 다룬다 |
| Inflation | `nav2_costmap_2d::InflationLayer` | 치명(lethal) 칸 주변의 비용 경사 |

Jazzy 기본값은 전역이 `["static_layer", "obstacle_layer", "inflation_layer"]`, 지역이 `["voxel_layer", "inflation_layer"]`다. 순서가 중요하다. inflation이 마지막인 것은 아래 계층들이 쓴 결과를 읽기 때문이다.

로봇의 모양은 여기서 들어온다. `robot_radius`(원) 또는 `footprint`(다각형) 중 하나다. 관리자들의 지침은 비원형 로봇이면 실제 다각형을 주라는 것이다. 여러 플래너와 현재의 모든 제어기가 완전한 SE(2) 발자국 충돌 검사를 하고, 그래야 더 좁은 공간으로 계획할 수 있기 때문이다. 반지름이 여전히 옳은 예외 셋: 환경에 비해 로봇이 아주 작을 때, SE(2) 검사를 감당할 연산 자원이 없을 때, 그리고 발자국을 어차피 무시하는 홀로노믹 플래너(NavFn, Theta\*, Smac 2D)를 쓸 때.

### 5. inflation radius가 실제로 하는 일

초심자는 `inflation_radius`를 안전 여유로 읽는다. "벽에서 이만큼 떨어뜨려라." 그건 이 값의 정체가 아니고, 그렇게 읽는 것이 생태계에서 가장 흔한 오설정을 만든다.

inflation layer 안에서는 서로 다른 두 가지가 벌어진다. 장애물로부터 로봇의 **내접 반지름(fully inscribed radius)** 안쪽에는 치명 비용을 쓴다 — 이것이 충돌 회피 부분이고, `inflation_radius`가 아니라 당신의 발자국에서 유도된다. 그다음 `inflation_radius`까지는 `cost_scaling_factor`를 감쇠율로 하는 **지수 감쇠** 비용을 쓴다. 플러그인 기본값은 `inflation_radius: 0.55`, `cost_scaling_factor: 10.0`이고, Jazzy TurtleBot 설정에서는 `0.7` / `3.0`이다.

그 감쇠하는 자락은 안전 여유가 아니다. **탐색을 조종하는 퍼텐셜 필드**다. NavFn, Theta\*, Smac 플래너는 비용을 인식한다. 매끄러운 경사가 주어지면 복도 한가운데로 달리고, 탐색이 장애물에 닿기 훨씬 전부터 장애물에 넓은 여유를 준다. 벽 주변에 얇은 팽창 고리만 있고 그 사이가 넓은 0 비용 공백이면, 플래너는 공백 안에서 어느 지점을 선호할 근거가 없고, 이유 없이 한쪽 벽에 붙거나 모서리를 깎는 경로를 낸다.

관리자들은 튜닝 가이드에서 이를 직접 말한다. 자신들이 보는 설정 파일 대부분이 inflation layer의 요점을 놓치고 있으며, 권고는 주행 가능한 폭 전체에 매끄러운 퍼텐셜이 생길 때까지 비용 스케일과 반지름을 *키우라*는 것이다. 아주 넓은 방은 가운데가 0 비용이어도 되지만, 복도와 통로는 그러면 안 된다. 그러니 실무 규칙은 초심자의 직관과 반대다. 로봇이 모서리를 깎거나 벽에 붙는다면 inflation은 큰 게 아니라 아마 *작다*.

과도한 팽창의 대가도 실재하니 명시해 둔다. 로봇이 반드시 통과해야 하는 가장 좁은 틈보다 더 멀리 팽창시키면 그 틈이 높은 비용으로 채워지거나 계획 불가능해지고, 로봇은 물리적으로 들어가는 문을 거부한다. 13절이 바로 그 증상을 쓴다.

### 6. 전역 플래너와 지역 제어기

역할 분담은 이렇다. **플래너** 는 "내가 아는 모든 것을 고려할 때 지도 규모에서 어떤 경로가 존재하는가"를 재계획마다 한 번 답한다. **제어기** 는 "그 경로의 마지막 1미터와 센서가 지금 보는 것을 고려할 때 지금 이 순간의 속도는 무엇인가"를 `controller_frequency`(기본 20 Hz)로 답한다.

Jazzy에서 쓸 수 있는 플래너와 관리자들의 로봇 유형 지침.

| 플래너 | 적합한 경우 |
|---|---|
| `nav2_navfn_planner::NavfnPlanner` | 원형 차동 구동·전방향 베이스. 격자 위 Dijkstra 또는 A\*. 넓게 휘는 곡선 |
| Theta\* (`nav2_theta_star_planner`) | 같은 베이스. 임의 각도의 직선을 선호할 때 |
| Smac 2D | 같은 베이스. 비용 인식 페널티를 붙인 고전 A\* |
| Smac Hybrid-A\* | 비원형·원형 Ackermann과 다리형. 기구학적으로 실현 가능한 SE(2) 경로 |
| Smac State Lattice | 비원형 차동·전방향, 그리고 임의 형상 |

가르는 질문은 "무엇이 최고인가"가 아니라 "내 로봇이 이 경로를 주행할 수 있는가"다. 앞의 셋은 홀로노믹이다. 90° 모서리가 든 경로를 태연히 돌려주는데, 차동 구동 베이스는 멈춰서 제자리 회전을 해야만 실행할 수 있고 Ackermann 베이스는 아예 실행할 수 없다. Smac 계열의 실현 가능 플래너는 출발 헤딩과 회전 제약을 존중하므로 경로가 적힌 그대로 주행 가능하다.

제어기.

- **DWB** (`dwb_core`, DWA의 ROS 2 재작성)는 속도·가속도 한계 안에서 전방 궤적 집합을 표본으로 뽑고, 각각을 **critic** 플러그인들 — `PathAlign`, `GoalDist`, `BaseObstacle`, `Oscillation`, `PreferForward` 등, 각각 조정 가능한 가중치를 가진다 — 로 채점한다. 차동 구동과 전방향에 적합하다. 어떤 궤적이 왜 뽑혔는지 정확히 알아야 할 때 옳은 선택이다. 점수가 분해되기 때문이다. 대가는 동작이 열몇 개 가중치의 함수이고 그것들을 직접 튜닝해야 한다는 점이다.
- **MPPI** (`nav2_mppi_controller::MPPIController`)가 Jazzy 기본값이다. 최적화 기반이다. 직전의 최적 궤적에 무작위 잡음을 섞어 배치를 롤아웃하고(기본 설정에서 `model_dt: 0.05`로 56 스텝, 2000 표본), critic이라 불리는 목적 함수 플러그인들로 가중한다. DWB의 고정 행동 모델 롤아웃보다 동적 객체를 훨씬 잘 다루고 보통 튜닝 없이도 동작한다. 대신 연산 비용이 다소 높다. 차동 구동, 전방향, Ackermann, 다리형에 적합하다.
- **Regulated Pure Pursuit** (`nav2_regulated_pure_pursuit_controller`)는 기하학적이다. 경로 위 lookahead 점을 골라 그쪽으로 조향하고, 장애물 근처와 급회전에서 속도를 줄이는 규제가 붙는다. 동적 장애물을 피하려고 경로를 *벗어나지 않는다*. 경로를 정확히 따르게 하고 싶고 그 경로를 신뢰할 때 쓴다. 즉 기구학적으로 실현 가능한 플래너와 짝지어야 하거나, 어떤 헤딩으로든 제자리 회전할 수 있는 차동 구동 베이스여야 한다.

알아 둘 네 번째: **Rotation Shim** 제어기는 다른 제어기를 감싸고, 넘기기 전에 새 경로의 헤딩 쪽으로 로봇을 제자리 회전시킨다. 홀로노믹 플래너가 로봇의 현재 헤딩과 크게 다른 시작 헤딩의 경로를 만들고, 정확한 추종에 맞춰 튜닝한 제어기가 그 상황을 잘 못 다루기 때문에 — 나선형으로 빠져나가거나 휙 돌아버린다 — 존재한다. 현재 헤딩에서 출발하는 실현 가능 플래너를 쓰면 필요 없다.

### 7. 위치 추정: AMCL과 map, odom, base_link 사슬

[[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]가 `base_link` 아래의 변환 트리를 만들었다. Nav2는 그 위의 변환 둘을 요구하고, REP 105가 누가 무엇을 발행하는지 고정한다.

$$ \texttt{map} \rightarrow \texttt{odom} \rightarrow \texttt{base\_link} \rightarrow [\text{sensor frames}] $$

- `odom` → `base_link`는 **오도메트리 시스템** 이 발행한다. 매끄럽고 연속이어야 한다. 무한히 표류해도 된다.
- `map` → `odom`은 **전역 측위 시스템** — AMCL, SLAM Toolbox, 모션 캡처, GNSS 융합 — 이 발행한다. 튀어도 된다. 오도메트리에 누적된 표류를 흡수하는 것이 존재 이유다.
- `base_link` 아래는 전부 정적이고 URDF에서 온다.

Nav2는 `nav2_amcl`을 제공한다. Adaptive Monte Carlo Localization, 즉 `map_server`가 서빙하는 정적 점유 격자 위의 입자 필터다. 각 입자가 자세 가설이고, 스캔마다 센서 모델(기본 `laser_model_type: "likelihood_field"`)과 운동 모델(`robot_model_type: "nav2_amcl::DifferentialMotionModel"`)로 재가중된다. 입자 500~2000개로 돌고, 로봇이 `update_min_d: 0.25` m 또는 `update_min_a: 0.2` rad만큼 움직였을 때만 갱신한다. 정지한 로봇은 새 정보를 주지 않기 때문이다. 출력은 `map` → `odom` 변환 *그 자체* 이고, `tf_broadcast: true`이므로 발행된다.

여기서 따라오는 결과 둘이 있고 둘 다 사람을 문다. AMCL은 초기 자세가 필요하다. RViz의 **2D Pose Estimate** 버튼이 `/initialpose`로 발행하는 것이 그것이고, 그것을 주기 전에는 `map` → `odom` 연결이 존재하지 않아 Nav2는 내비게이션을 시작할 수 없다. 그리고 AMCL은 추적하지, 기본 설정에서 전역 재측위를 하지 않는다. `recovery_alpha_slow`와 `recovery_alpha_fast`가 `0.0`이 기본값이고, 이는 납치된 로봇에서 회복할 수 있는 무작위 입자 주입을 끈다. 들려서 옮겨진 로봇은 당신이 다시 추정해 줄 때까지 확신에 차서 틀린 채로 있다.

AMCL도, 라이다도 필수가 아니다. 유효한 `map` → `odom`을 발행하는 어떤 소스든 계약을 만족한다. 지도가 아직 없으면 SLAM Toolbox가 기본이고, `odom` → `base_link` 쪽에서 바퀴 오도메트리·IMU·시각 오도메트리를 융합하는 통상적인 방법은 `robot_localization`이다.

### 8. 라이프사이클 관리, 그리고 왜 관리형 노드인가

모든 Nav2 서버는 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]에서 말한 의미의 **관리형(lifecycle) 노드**다. unconfigured → inactive → active로 가고, 설정은 생성자가 아니라 전이에서 이뤄진다.

이유는 순서다. costmap이 지도를 받기 전에, 또는 변환 트리가 완성되기 전에 활성화된 제어기는 깨끗하게 실패하지 않는다. 쓰레기를 발행하거나 블로킹된다. 관리형 노드는 기동 순서와 종료 순서를 결정론적으로 강제할 수 있게 한다.

그 강제를 하는 것이 `nav2_lifecycle_manager`다. 순서 있는 `node_names` 목록을 받아 차례로 configured, active로 전이시키고, 내릴 때는 역순으로 내린다.

```yaml
lifecycle_manager:
  ros__parameters:
    autostart: true
    node_names: ['controller_server', 'planner_server', 'behavior_server', 'bt_navigator', 'waypoint_follower']
    bond_timeout: 4.0
    attempt_respawn_reconnection: true
    bond_respawn_max_duration: 10.0
```

또 각 서버와 **bond**, 즉 심장박동을 유지한다. 서버가 죽거나 `bond_timeout` 초 동안 응답하지 않으면 매니저는 *스택 전체* 를 내린다. 반쯤 죽은 내비게이션 시스템 위에서 로봇이 계속 달리게 두지 않기 위해서다. 이것은 안전에 대한 결정이고, 노드 하나가 죽으면 스택 전부가 함께 내려가는 이유다. `autostart: false`면 RViz Nav2 패널에서 **Startup** 을 누를 때까지 아무것도 활성화되지 않는다. 디버깅 중에는 그 동작이 맞다.

```bash
ros2 lifecycle list /planner_server
ros2 lifecycle get /controller_server
```

### 9. Costmap 필터와 keepout 구역

제약이 물리적이지 않을 때가 있다. 어떤 복도는 주행에 문제가 없지만 업무 시간에는 로봇이 들어가지 않았으면 하고, 어떤 실험 구역은 출입 금지이고, 하역장 근처 구간은 속도 제한이 필요하다.

**costmap 필터** 는 그것을 두 번째 주석 이미지 — 지도와 같은 형식이지만 크기나 자세가 같을 필요는 없는 **filter mask** — 로 인코딩한다. 이 마스크는 `map_server` 인스턴스가 발행하고, 마스크 픽셀 값이 필터 자체의 공간으로 어떻게 매핑되는지 알려 주는 `nav2_costmap_2d::CostmapFilterInfo` 메시지를 **Costmap Filter Info Server** 가 함께 발행한다. 필터는 costmap 플러그인이지만 `plugins:`가 아니라 별도의 `filters:` 목록에 들어간다.

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
      filters: ["keepout_filter"]
      keepout_filter:
        plugin: "nav2_costmap_2d::KeepoutFilter"
        enabled: True
        filter_info_topic: "/costmap_filter_info"
```

`KeepoutFilter`는 마스크에서 읽은 비용을 costmap에 써서 플래너가 표시된 구역을 통과하지 않게 한다. `SpeedFilter`는 막는 대신 표시된 구역에서 속도 상한을 건다. `BinaryFilter`는 구역에 진입할 때 불리언 토픽을 토글해, 그 밖의 무엇이든 촉발할 수 있게 한다.

문서화된 함정 하나: **필터에는 inflation layer가 적용되지 않는다.** 속도 구역을 팽창시키는 것이 무의미하기 때문이다. 일부 실현 가능 플래너는 전체 SE(2) 발자국 검사에 앞서 로봇 중심점의 비용을 값싼 선검사로 확인한다. 그래서 팽창되지 않은 keepout 구역은 로봇 중심에 대해서는 지켜지지만 가장자리에 대해서는 지켜지지 않는다. 발자국 전체를 구역 밖에 두고 싶다면 필터를 덮는 inflation layer를 추가해야 한다.

지도 파일을 직접 고치는 것보다 나은 점은 마스크가 별개의 권한 계층이라는 것이다. 지도는 무엇이 거기 있는지를 기술하고, 마스크는 당신이 무엇을 결정했는지를 기술한다. 위치 추정이 의존하는 대상을 훼손하지 않고 정책을 바꿀 수 있다.

### 10. 액션으로 목표 보내기, 그리고 피드백이 담는 것

`bt_navigator`는 `/navigate_to_pose`를 노출하고, 타입은 `nav2_msgs/action/NavigateToPose`다. 여기서 액션이 옳은 패턴인 이유는 25.3에서 말한 그대로다. 내비게이션은 몇 분이 걸리고, 도는 동안 진행 상황이 필요하고, 취소할 수 있어야 한다.

```bash
ros2 action list -t
ros2 action info /navigate_to_pose -t
```

목표는 자세 하나와, 선택적으로 이 목표에 쓸 행동 트리의 이름이다.

```text
# goal
geometry_msgs/PoseStamped pose
string behavior_tree
```

커맨드라인에서 하나 보낸다. RViz의 **Nav2 Goal** 도구가 하는 일과 같다.

```bash
ros2 action send_goal --feedback /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.5, y: 0.5, z: 0.0}, orientation: {w: 1.0}}}}"
```

주행하는 동안 흘러나오는 피드백은 이렇다.

```text
geometry_msgs/PoseStamped current_pose
builtin_interfaces/Duration navigation_time
builtin_interfaces/Duration estimated_time_remaining
int16 number_of_recoveries
float32 distance_remaining
```

제 값을 하는 필드는 `number_of_recoveries`다. 나머지는 로봇이 진전하고 있음을 알려 주지만, 그 필드는 *그 진전을 만들어 내려고 트리가 얼마나 애쓰고 있는지* 를 알려 준다. 복구 세 번으로 완료된 주행은 출하해도 되는 성공이 아니라, 어쩌다 해결된 설정 문제다. 기록으로 남겨라.

결과는 `error_code`와 `error_msg`를 담는다. 코드는 서버별로 구획되어 있다. 플래너가 200–208(`START_OCCUPIED`, `GOAL_OUTSIDE_MAP`, `NO_VALID_PATH`), 제어기가 100–107(`FAILED_TO_MAKE_PROGRESS`, `NO_VALID_CONTROL`, `TF_ERROR`)이다. 그래서 실패한 목표는 어느 서버가 왜 포기했는지를 스스로 말한다.

Python에서는 `nav2_simple_commander`가 이 전부를 감싼다.

```python
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

rclpy.init()
nav = BasicNavigator()
nav.waitUntilNav2Active()      # autostart인 경우. 아니면 lifecycleStartup()
nav.goToPose(goal_pose)        # 논블로킹
while not nav.isTaskComplete():
    feedback = nav.getFeedback()
result = nav.getResult()       # TaskResult.SUCCEEDED / CANCELED / FAILED
```

`goToPose`가 논블로킹인 것은 의도된 설계다. 그래야 단일 스레드 애플리케이션이 피드백을 폴링하면서 자기 기준으로 `nav.cancelTask()`를 부를 수 있다.

### 11. 범위: 어디까지가 평평하고 지도가 있는 실내를 전제하는가

이 부분을 정확히 말하는 것이 보기보다 중요하다. Nav2 데모는 잘 이전되지 않고, 그 실패가 조용하기 때문이다.

평평하고, 지도가 있고, 실내임을 전제하는 것.

- **2D costmap 자체.** 평면 위 칸당 비용이다. 경사, 거칠기, 단차 높이, 표면 종류 개념이 없다. 20° 잔디 경사와 매끈한 바닥이 구별되지 않고, 연석과 벽도 구별되지 않는다.
- **정적 점유 격자 위의 AMCL.** 변하지 않는다고 가정된 저장된 지도, 그리고 키 큰 풀이 아니라 벽에 맞는다고 가정된 수평 레이저 스캔.
- **obstacle/voxel 계층의 소거 모델.** 레이 추적 소거는 센서와 반사점 사이가 비어 있다고 가정한다. 울퉁불퉁한 지면에서는 빔이 앞쪽 땅에 맞고 그것이 장애물로 표시된다 — 경사로 위의 전형적인 유령 벽 고장이다.
- **`DiffDrive` 기구학과 거의 0 비용인 자유 공간.** 기본 MPPI 운동 모델과 플래너/제어기 분할 전체가, 비용이 낮은 곳이면 어디로든 로봇을 명령할 수 있다고 가정한다.

옥외와 건설 현장으로 그대로 이전되는 것.

- 행동 트리 구조, 서버/플러그인 분할, 라이프사이클 관리, 액션 인터페이스. 이 중 어느 것도 지형에 대해 아는 바가 없다.
- `map` → `odom` → `base_link` 계약. AMCL을 GNSS/IMU 융합으로 바꿔도 그 위의 모든 것이 그대로 동작한다.
- Costmap 필터. 현장 규칙 — 출입 금지 구역, 속도 제한 구역 — 이 실제로 인코딩되는 방식이다.
- 궤적 추종 알고리즘으로서의 MPPI와 RPP. 단, 의미 있는 costmap이 주어진다는 조건에서.

바뀌어야 하는 것은 환경 표현이다. 칸 값이 점유 여부가 아니라 주행 가능 여부를 인코딩하는 지도가 필요하다. 그것은 자체 문헌을 가진 다른 문제이고, 이 위키는 [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]에서 다룬다. Nav2 문서 스스로도 이 공백을 인정하며 gradient map, 3D costmap, mesh map을 다른 환경 표현으로 나열한다. inflation radius 조정으로 거기까지 갈 수 있다고 가정하지 말고 그 페이지를 읽어라.

### 12. 실습: 목표 하나, costmap, 그리고 계획

한 자리에서 끝난다. 전부 시뮬레이션이고, 미리 만들어 둔 지도를 가진 차동 구동 TurtleBot이다.

```bash
source /opt/ros/jazzy/setup.bash
ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False
```

`headless`의 기본값은 `true`이고 3D 뷰 없이 시뮬레이션을 띄운다. `False`면 Gazebo와 RViz가 나란히 뜬다.

1. **위치를 잡아 준다.** 로봇은 자기가 어디인지 모른다. Gazebo 세계에서 로봇을 찾고, RViz에서 **2D Pose Estimate** 를 눌러 지도 위 같은 지점을 클릭한 채 끌어라. 끄는 방향이 방위를 정한다. `/particle_cloud`의 입자 구름이 나타나고 지도가 제자리를 잡는다. autostart가 꺼져 있으면 Nav2 패널의 **Startup** 을 먼저 누른다.
2. **몰기 전에 그래프를 본다.** source된 두 번째 터미널에서:

```bash
ros2 node list
ros2 action list -t
ros2 topic hz /local_costmap/costmap
```

3. **디스플레이를 설정한다.** 중요한 넷이고 기본 RViz 설정에 이미 들어 있다: `/global_costmap/costmap`(Map 디스플레이), `/local_costmap/costmap`, `/plan`(Path), `/local_plan`(Path). 두 costmap을 번갈아 켜고 끄면서, 지역 쪽이 로봇을 따라다니는 작은 정사각형임을 확인하라.
4. **RViz 버튼이 아니라 커맨드라인으로 목표를 보낸다.** 그래야 피드백이 보인다.

```bash
ros2 action send_goal --feedback /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 1.5, y: 0.5, z: 0.0}, orientation: {w: 1.0}}}}"
```

`distance_remaining`이 줄어들고 `number_of_recoveries`가 0에 머무는 것을 보라.

5. **재계획을 관찰한다.** `/plan`은 로봇이 달리는 동안 대략 1초에 한 번 다시 계산된다 — 경로 전체가 꿈틀거린다. `/local_plan`은 제어기의 짧은 궤적이고 20 Hz로 갱신된다.
6. **일부러 복구시킨다.** 로봇이 달리는 동안 Gazebo에서 상자를 앞 복도에 끌어다 놓아라. voxel 계층이 그것을 표시하고, 지역 costmap이 바뀌고, MPPI가 돌아간다. 이제 로봇을 완전히 가둬라. 제어기가 실패하고, 트리가 지역 costmap을 지우고 재시도하고, 그다음 복구 서브트리로 떨어진다 — 로봇이 제자리 회전하고 후진하는 것이 보이고, 피드백 스트림의 `number_of_recoveries`가 올라간다.
7. **취소한다.** 주행 중에 `send_goal` 명령을 Ctrl+C로 끊고 로봇이 서는지 확인하라. 그것은 크래시가 아니라 액션의 취소 경로다.

화면을 가리키며 저 네 토픽을 각각 어느 노드가 발행했는지, 그리고 지역 costmap이 `map`이 아니라 `odom`에 있는 이유가 무엇인지 말할 수 있으면 끝이다.

### 13. 진단할 고장: 제자리에서 돌기만 하거나, 아예 움직이지 않는 로봇

Nav2의 대표적인 고장이고, 밖에서 보면 똑같아 보이는 흔한 원인이 넷 있다. 이 순서로 확인하라. 각 점검이 다음 것보다 싸고, 뒤의 것들을 배제해 주기 때문이다.

**첫째, 변환 트리.** 절반 이상이 TF 문제이고, TF가 실패하면 그 아래 모든 구성 요소가 조용히 실패한다.

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo map base_link
ros2 run tf2_ros tf2_monitor map base_link
```

`view_frames`는 간선별 주기가 적힌 트리 PDF를 쓴다. 찾을 것: `map` → `odom`의 부재(AMCL이 초기 자세를 못 받았거나 아예 안 돌고 있다), 트리가 두 조각으로 *끊긴* 상태, 또는 `tf2_monitor`가 보고하는 평균 지연이 소비자들의 `transform_tolerance`(behavior server와 MPPI는 0.1초, AMCL은 1.0초)보다 큰 경우. 오래된 변환은 제어기가 모든 궤적을 기각하게 만들고, 그것은 움직이지 않는 로봇으로 나타난다. 트리가 잘못됐으면 여기서 멈춰라. 고치는 곳은 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]다.

**둘째, costmap의 내용.** RViz에서 `/local_costmap/costmap`을 보라. 진단이 되는 그림은 둘이다.

- *로봇이 치명 비용 또는 팽창 비용 안에 앉아 있다.* 그러면 유효한 궤적이 없고 로봇은 돌고, 후진하고, 또 돈다. 원인: 레이저가 잘못된 변환으로 장착되어 자기 차체를 보고 있다, `max_obstacle_height`가 지면을 들여보내고 있다, obstacle 계층이 일시적 물체를 표시했는데 `raytrace_max_range`(기본 3.0 m)가 `obstacle_max_range`(2.5 m)를 소거하기에 충분히 길지 않아 지워지지 않았다.
- *costmap이 비어 있거나 갱신되지 않는다.* 소스 토픽이 실제로 도착하는지(`ros2 topic hz /scan`), 그리고 `observation_sources`가 그것을 지명하는지 확인하라. 갱신되지 않는 costmap은 로봇이 확신에 차서 물체로 돌진하게 만들거나, 전역 쪽이 빈 경우 아예 계획을 거부하게 만든다.

가설을 시험하려면 손으로 지워 보라.

```bash
ros2 service call /global_costmap/clear_entirely_global_costmap nav2_msgs/srv/ClearEntireCostmap
ros2 service call /local_costmap/clear_entirely_local_costmap nav2_msgs/srv/ClearEntireCostmap
```

지웠더니 로봇이 움직인다면 문제는 플래너가 아니라 costmap에 쓰고 있는 무언가다.

**셋째, 발자국.** RViz에서 `/local_costmap/published_footprint`를 띄우고 로봇과 비교하라. 너무 큰 `robot_radius`, 또는 단위가 틀렸거나 엉뚱한 프레임 기준으로 중심이 잡힌 `footprint` 다각형은 내접 반지름 치명 영역이 로봇 자신의 칸을 삼키게 만든다. 그러면 로봇은 가만히 서 있으면서 자기가 충돌 중이라고 믿는다. 정확히 영원히 도는 증상이다. 5절의 과팽창 사례도 여기서 잡힌다. 로봇이 물리적으로 들어가는 문을 거부한다면 `inflation_radius`를 문 너비 절반에서 내접 반지름을 뺀 값과 비교해 보라.

**넷째, 제어기 파라미터.** 이제서야. 이 증상을 만드는 것들:

- `min_x_velocity_threshold` / `min_theta_velocity_threshold`가 너무 높아 계산된 명령이 0으로 취급된다.
- 속도 한계(MPPI의 `vx_max`, `wz_max`)가 필요한 회전을 낼 수 없어, 표본 궤적 중 어느 것도 목표 영역에 닿지 못한다.
- `xy_goal_tolerance` / `yaw_goal_tolerance`가 너무 빡빡하다. 로봇이 도착했는데 yaw 허용 오차를 만족하지 못하고 목표 주변에서 영원히 진동한다.
- 홀로노믹 플래너가 rotation shim 없는 제어기에 경로를 먹여, 새 경로마다 로봇이 휙 돌거나 나선을 그린다.

```bash
ros2 param get /controller_server FollowPath.vx_max
ros2 param dump /controller_server
```

순서가 요점이다. TF를 확인하기 전에 바꾼 파라미터는 결국 되돌리게 될 파라미터다.

### 14. 이 페이지가 다루지 않는 것

애초에 지도를 만드는 일 — SLAM Toolbox와 `map_server` 저장 절차 — 은 별도 실습이고, Nav2의 first-time robot setup 가이드가 다룬다. 자기 플래너·제어기·costmap 계층 플러그인을 작성하는 것은 이 페이지 다음 단계이고 Nav2에 별도 튜토리얼이 있다. waypoint follower, collision monitor, velocity smoother, docking server는 모두 스택의 일부지만 여기에는 나오지 않는다. 네임스페이스를 쓰는 다중 로봇 기동은 `nav2_bringup`에 있지만 이 페이지에는 없다.

그 아래 깔린 알고리즘 — 탐색, 표본 기반 계획, MPC, 그리고 경로에 대한 최적성이 무슨 뜻인지 — 은 [[04-robotics/planning-decision-making|4. Planning & Decision-Making]]. 같은 베이스 위의 팔과 내비게이션이 만나는 지점은 [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]]. 2D 점유 격자로 기술할 수 없는 지형은 [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]. 트랙의 나머지는 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- Nav2 문서(Jazzy) — Navigation Concepts: Navigation Servers; Environmental Representation; State Estimation; Behavior Trees.
- Nav2 문서(Jazzy) — Getting Started: Quickstart.
- Nav2 문서(Jazzy) — Configuration Guide: Inflation Layer; Obstacle Layer; Voxel Layer; Static Layer; Keepout Filter; Lifecycle Manager; Behavior Tree Navigator; Costmap 2D.
- Nav2 문서(Jazzy) — 행동 트리 노드: RecoveryNode; PipelineSequence; Navigate To Pose with replanning and recovery.
- Nav2 문서(Jazzy) — Tuning Guide(inflation 퍼텐셜 필드, 발자국 대 반지름, 플래너·제어기 플러그인 선택); Simple Commander API.
- `ros-navigation/navigation2`, `jazzy` 브랜치 — `nav2_msgs/action/NavigateToPose.action`, `FollowPath.action`, `ComputePathToPose.action`; `nav2_bringup/params/nav2_params.yaml`; `nav2_bringup/rviz/nav2_default_view.rviz`.
- REP 105, Coordinate Frames for Mobile Platforms.
- `ros2/geometry2`, `jazzy` 브랜치 — `tf2_tools`와 `tf2_ros` 실행 파일.

> [!question]- 스스로 점검 · 정답
> **1. 전역 costmap은 `map` 프레임인데 지역 costmap은 왜 `odom` 프레임인가?** `map` → `odom`은 AMCL이 발행하고, 위치가 보정될 때 튀어도 되는 변환이기 때문이다. 순간이동하는 프레임 위에서 20 Hz로 도는 제어기는 불연속한 명령을 낸다. `odom`은 표류하지만 매끄럽고, 그것이 짧은 시평의 제어가 필요로 하는 성질이다. 전역 일관성이 중요하고 1초에 한 번 재계획하는 플래너가 대신 튀는 프레임을 받는다.
> **2. 로봇이 모서리를 깎고 벽에 붙는데 충돌은 한 번도 하지 않는다. 유력한 원인은 무엇이고 어느 방향으로 바꾸는가?** 팽창이 너무 큰 게 아니라 너무 작다. 감쇠하는 팽창 비용은 비용 인식 플래너를 자유 공간 한가운데로 이끄는 퍼텐셜 필드다. 벽 주변의 얇은 고리만 있으면 그 사이의 넓은 0 비용 공백 안에서 플래너가 어느 지점을 선호할 근거가 없다. 주행 가능한 폭 전체에 매끄러운 경사가 생길 때까지 `inflation_radius`와 `cost_scaling_factor`를 키워라. 단, 반드시 통과해야 하는 가장 좁은 틈이 여전히 계획 가능한지 확인하면서.
> **3. 로봇이 제자리에서 돌기만 하고 출발하지 않는다. 무엇을 먼저 확인하고, 제어기 파라미터는 왜 먼저가 아닌가?** 변환 트리다. `ros2 run tf2_tools view_frames`와 `ros2 run tf2_ros tf2_monitor map base_link`. `map` → `odom`이 없거나 변환이 `transform_tolerance`보다 오래됐으면 모든 궤적이 무효가 되고, TF를 지목하는 오류 한 줄 없이 정확히 이 증상이 나온다. 그다음이 costmap 내용과 발자국이다. 제어기 파라미터가 넷째인 이유는, TF를 확인하기 전에 바꾼 파라미터는 결국 되돌리게 되기 때문이다.
> **4. 정상 경로는 "계획하고 따라간다"뿐인데 왜 상태 기계가 아니라 행동 트리인가?** 어려운 부분이 정상 경로가 아니기 때문이다. 어려운 것은 복구이고, FSM에서는 복구 규칙 하나하나가 그것이 발동할 수 있는 모든 상태마다 복제되어야 하는 전이다. 트리는 복구에 범위를 준다. 플래너를 감싼 `RecoveryNode`는 전역 costmap을 지우고, 제어기를 감싼 것은 지역 costmap을 지우며, 시스템 수준 실패만이 공유되는 회전/대기/후진 서브트리에 도달한다. 또한 컴파일된 제어 흐름이 아니라 데이터로 편집된다 — 액션의 `behavior_tree` 필드를 통해 목표마다 다른 XML을 쓸 수 있다.
