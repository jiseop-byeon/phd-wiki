---
title: "25.10 Debugging, Data and Reproducibility"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Diagnose a broken ROS 2 system in a fixed order instead of guessing, turn a recorded bag into a regression fixture, and package a result so someone else can reproduce it."
mastery-when: "Go deeper when you are building the test infrastructure for a lab rather than using it — tracing, fault injection, hardware-in-the-loop rigs."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to find the cause of a silent ROS 2 system in minutes, and to hand someone a bag, a container and a test that reproduces your result. Not enough to build a lab's CI infrastructure from scratch.
> **Working** — 조용히 죽은 ROS 2 시스템의 원인을 몇 분 안에 찾아내고, bag·컨테이너·테스트를 묶어 남에게 결과를 재현시킬 정도. 연구실 CI 기반을 처음부터 짓는 수준은 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] for QoS compatibility and `use_sim_time`, and [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]] for `colcon` and launch files. Baseline as everywhere in this track: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**.
> QoS 호환성과 `use_sim_time`은 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]], `colcon`과 launch 파일은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. 기준 환경은 이 트랙 전체와 같이 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**다.

### 1. Why this page exists

A ROS 2 system that does not work usually produces no error. The node starts, prints its startup log, and nothing happens. There is no stack trace, no exception, no exit code. Two nodes that will never exchange a message look exactly like two nodes that are about to.

Faced with that, most people guess. They restart things, add print statements, change a number, restart again. Sometimes it works and they do not know why, which is worse than failing, because the same bug returns in three weeks and the guessing starts over.

The alternative is an ordered set of checks that you run in the same order every time, whether or not you have a hunch. The order matters more than any individual check: it means you eliminate a whole class of causes with one command instead of circling. **Having that order is the difference between an engineer and a guesser**, and it is most of what this page is.

The second half of the page is about the same discipline applied to evidence. A bug you can only reproduce by having the robot in front of you is a bug you will fix slowly. A result you can only produce on your own laptop is not a result yet.

### 2. The ordered set of checks

Run these top to bottom. Stop at the first one that fails; do not skip ahead because you think you know.

| # | Question | Command | What a failure means |
|---|---|---|---|
| 0 | Is this shell the environment I think it is? | `printenv \| grep -i ros` | Unsourced shell, wrong overlay, or a stray `ROS_DOMAIN_ID`. See 25.4. |
| 1 | Is the node running at all? | `ros2 node list` | It crashed at startup, or it is on another domain, or launch never started it. |
| 2 | Does the node have the endpoint I expect? | `ros2 node info /my_node` | A remap you forgot, or a subscription created on a different name than you read in the source. |
| 3 | Is anything actually published on the topic? | `ros2 topic hz /my_topic` | The upstream node is alive but silent — its own input is missing, or its timer never fires. |
| 4 | Is anyone subscribed? | `ros2 topic info /my_topic` | Publisher-without-subscriber: the consumer is on a different name. |
| 5 | Do the QoS profiles match? | `ros2 topic info /my_topic --verbose` | Reliability or durability incompatibility. Endpoints exist, count is nonzero, no data moves. |
| 6 | Is the frame present, and recent? | `ros2 run tf2_ros tf2_echo map base_link` | Missing publisher, a disconnected tree, or stamps too old to interpolate. |
| 7 | Is the clock right? | `ros2 topic hz /clock` and `ros2 param get /my_node use_sim_time` | Half the graph on simulated time and half on wall time. |

Steps 3 and 4 together are the single most useful pair: they split "nobody is sending" from "nobody is listening", which are opposite bugs with identical symptoms. Step 5 catches the case where both of those pass and data still does not move, which is the failure mode DDS introduced and which 25.5 dissects.

Write this table on something near your desk. Then, when a system breaks, run it — including the checks you are sure about.

### 3. The introspection tools, gathered

`ros2 doctor` is the zero-effort first look. With no arguments it runs every check and prints `All <n> checks passed` or a count of failures; warnings are ignored by default, so add `--include-warnings` (`-iw`) to treat them as failures. On a running system it reports publishers without subscribers and subscribers without publishers, which is check 4 done automatically across the whole graph.

```bash
ros2 doctor
ros2 doctor --include-warnings
ros2 doctor --report          # NETWORK CONFIGURATION, PLATFORM INFORMATION, RMW MIDDLEWARE, ROS 2 INFORMATION, TOPIC LIST
ros2 doctor --report-failed   # only the checks that failed
```

`--report` is what you paste into a bug report or a message to a colleague: it captures the environment that your description of the problem is otherwise missing. The documentation is explicit that `ros2doctor` is not a debug tool — it checks your setup, not your code.

`ros2 node info` prints a node's entire surface: Subscribers, Publishers, Service Servers, Service Clients, Action Servers, Action Clients, each with types. Add `--include-hidden` when a topic starting with `_` is involved, such as the service-event topics.

The three rate tools answer three different questions and are constantly confused:

```bash
ros2 topic hz /scan              # message rate, averaged over a window
ros2 topic hz /scan -w 1000      # longer window: less jitter in the number
ros2 topic hz /scan --wall-time
ros2 topic bw /scan              # bandwidth in bytes/s — is this topic the reason the network is full
ros2 topic delay /scan           # age of the header stamp on arrival
```

`hz` measures how often messages arrive. `bw` measures how much they cost. `delay` measures **latency**: the difference between the stamp inside the message and the time it was received, which requires the message type to have a `std_msgs/Header`. A system where `hz` is perfect and `delay` grows without bound is a system with a queue filling up somewhere, and only `delay` shows it. `--wall-time` on `hz` — that is the spelling, and it exists only on `hz`, not on `bw` or `delay` — matters under simulation. The default is the other way round from what people assume: the CLI node runs on wall time unless you pass `-s`/`--use-sim-time`, so plain `ros2 topic hz` already measures what the CPU did. Pass `-s` to measure simulated rate, and `--wall-time` to force wall time back when the clock is unreliable.

```bash
ros2 param dump /my_node > my_node_params.yaml
```

`ros2 param dump` prints the node's complete parameter set as YAML on stdout — you redirect it yourself. Two uses: diffing a misbehaving node's live parameters against the YAML you thought you loaded, and capturing the exact configuration of a run as an artifact (see section 13). `--timeout N` waits for the node to appear.

For transforms, three tools:

```bash
ros2 run tf2_ros tf2_echo map base_link      # is this specific transform available, and what is it
ros2 run tf2_tools view_frames               # renders the whole tree to a file
ros2 run tf2_ros tf2_monitor map base_link   # timing statistics: publishing rates and delays per frame
```

`view_frames` is the one that finds a *disconnected* tree — two valid subtrees with no edge between them, which produces "could not find a connection between ... because they are not part of the same tree" and is otherwise hard to see.

The rqt plugins are the same data with a time axis, which is sometimes the whole point:

| Plugin | Run it | Use it when |
|---|---|---|
| `rqt_graph` | `ros2 run rqt_graph rqt_graph` | You need to see who is connected to whom, and the picture is faster than reading `node info` ten times. |
| `rqt_console` | `ros2 run rqt_console rqt_console` | Log messages scroll past too fast; you want to filter by severity, node and text. |
| `rqt_plot` | `ros2 run rqt_plot rqt_plot` | A number is wrong and you need its shape over time, not its value now. |
| `rqt_reconfigure` | `ros2 run rqt_reconfigure rqt_reconfigure` | You are tuning parameters live rather than restarting between values. |
| `rqt_bag` | `ros2 run rqt_bag rqt_bag` | You want to scrub a recording and look at one message. |

Or run `rqt` and dock several of them in one window. `sudo apt install ros-jazzy-rqt ros-jazzy-rqt-common-plugins` gets the common set.

### 4. RViz as a debugger, not a demo

RViz is presented in most tutorials as the thing that makes a screenshot. Treat it instead as a debugger with two specific features.

First, **Display Status**. Every display has a status of `OK`, `Warning`, `Error` or `Disabled`, shown as the background colour of its title and expandable into the specific message. An Error on a PointCloud2 display naming a missing frame tells you check 6 failed, in the one place you were already looking. Most people never expand it.

Second, the **Fixed Frame**. It is the reference frame the world is drawn in, and it must not move relative to the world — `map` or `odom`, not `base_link`. Set it to the robot base and every object the robot ever saw appears in front of the robot. A large class of "my sensor data is in the wrong place" is a Fixed Frame choice, not a calibration error. Note also that changing the Fixed Frame clears the currently displayed data rather than re-transforming it, so an empty view immediately after the change is expected.

The habit: when data does not appear in RViz, do not adjust the camera. Read the Display Status, then check the Fixed Frame, then run `tf2_echo` between the fixed frame and the data's frame.

### 5. Logging: levels, destinations, and raising one node at runtime

Severity levels, in ascending order: `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`. A logger processes messages at or above its level; the default is `INFO`, which is why your `DEBUG` lines produce nothing until you ask for them.

Every message goes to three places, each of which can be disabled per node:

- the **console**, on stderr by default (`RCUTILS_LOGGING_USE_STDOUT=1` moves it to stdout);
- **files on disk**, written by `rcl_logging_spdlog`, in `$ROS_LOG_DIR` if set, otherwise `$ROS_HOME/log`, with `ROS_HOME` defaulting to `~/.ros` — so `~/.ros/log/` unless you changed something;
- the **`/rosout` topic**, which is how `rqt_console` and `ros2 topic echo /rosout` see the logs of a node running on another machine.

`~/.ros/log` is the answer to "the node crashed and the terminal is gone". It is also the answer to "my disk is full", because nothing rotates it for you.

Setting levels at startup, via `--ros-args`:

```bash
ros2 run turtlesim turtlesim_node --ros-args --log-level WARN          # process default
ros2 run demo_nodes_cpp talker --ros-args --log-level talker:=DEBUG    # one named logger
ros2 run my_pkg my_node --ros-args --disable-rosout-logs               # saves real bandwidth on a robot
```

The second form is the one that matters in a system of twenty nodes: raise one logger to `DEBUG` and leave the rest at `INFO`, instead of drowning. Logger names are hierarchical — setting `abc` also affects `abc.def` unless that was set explicitly.

Changing a level **at runtime**, without restarting, is possible but off by default. The node must opt in:

```python
node = Node('NodeWithLoggerService', enable_logger_service=True)
```

```cpp
auto node = std::make_shared<rclcpp::Node>(
  "NodeWithLoggerService", rclcpp::NodeOptions().enable_logger_service(true));
```

That exposes two services, and the levels are the numeric values (10 = DEBUG, 20 = INFO):

```bash
ros2 service call /NodeWithLoggerService/set_logger_levels rcl_interfaces/srv/SetLoggerLevels \
  '{levels: [{name: "NodeWithLoggerService", level: 10}]}'
ros2 service call /NodeWithLoggerService/get_logger_levels rcl_interfaces/srv/GetLoggerLevels \
  '{names: ["NodeWithLoggerService"]}'
```

> [!warning] Documented limitation
> `get_logger_levels` and `set_logger_levels` are not thread-safe as of Jazzy; only one thread may call them at a time.

Turn this on in the nodes you write. The cost is one constructor argument and the benefit is diagnosing a rare fault on a running robot without restarting the run that produced it.

### 6. rosbag2: recording, and why recording everything is usually wrong

```bash
ros2 bag record --topics /scan /odom /tf /tf_static -o run_042
```

`--topics` takes a space-separated list; `-o` names the output directory. (The bare positional form still works and prints a deprecation notice; use `--topics`. There is no `-t` short option on `record` — `-t` belongs to `ros2 bag info`, so `record -t /scan` is an error rather than a deprecation.) A bag is a **directory** containing `metadata.yaml` and one or more storage files, not a single file.

`-a` records everything, and it is the wrong default for almost every research recording:

- **Disk and bandwidth.** One uncompressed 1080p camera topic at 30 Hz is about 190 MB/s — 1920 × 1080 × 3 bytes × 30. You will fill the robot's disk mid-experiment.
- **Dropped messages.** The recorder has to serialise and write everything you asked for. Ask for too much and it falls behind, and the bag you take home is missing the messages you cared about — silently.
- **Unusability.** A 400 GB bag cannot be shared with a collaborator, cannot be put in CI, and cannot be opened quickly enough to iterate.

Record the inputs of the component you are debugging, plus `/tf` and `/tf_static`, plus whatever you need to judge the outcome. If you cannot name why a topic is in the list, it should not be.

Useful flags when you do need volume:

```bash
ros2 bag record -e "^/camera/.*" --exclude-regex ".*/compressedDepth" -o cam   # by pattern
ros2 bag record --topics /scan -b 2000000000                                   # split every 2 GB
ros2 bag record --topics /scan -d 60                                           # split every 60 s
ros2 bag record -a --compression-mode file --compression-format zstd -o run    # compress whole files
ros2 bag record --topics /scan --use-sim-time                                  # stamp from /clock, under simulation
```

Press SPACE in the recorder terminal to pause and resume. `--snapshot-mode` holds messages in memory and writes only when you call `/rosbag2_recorder/snapshot` — the right tool for "record the ten seconds before the failure" on a long run.

### 7. `ros2 bag info` and the storage plugins

```bash
ros2 bag info run_042
```

```text
Files:             run_042_0.mcap
Bag size:          228.5 KiB
Storage id:        mcap
Duration:          48.47s
Start:             Oct 11 2019 06:09:09.12 (1570799349.12)
End                Oct 11 2019 06:09:57.60 (1570799397.60)
Messages:          3013
Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 9 | Serialization Format: cdr
                   Topic: /turtle1/pose | Type: turtlesim/msg/Pose | Count: 3004 | Serialization Format: cdr
```

Read the **Count** column before you read anything else. A topic you thought you recorded with a count of zero ends the investigation immediately: the recorder subscribed to a name nothing published. A count far below `Duration × expected rate` means the recorder dropped messages, which is the failure mode from the previous section showing up as evidence.

rosbag2 in Jazzy ships two storage plugins, selected with `-s`:

- **`mcap`** — the default. A self-describing, indexable container with broad tooling outside ROS; it can compress internally while remaining indexable, unlike the CLI's `--compression-mode`.
- **`sqlite3`** — the older plugin, kept for compatibility with existing bags and tooling.

You rarely need to choose. Take the default, and know the word `mcap` so that the `Storage id:` line means something. Playback detects the storage implementation automatically.

### 8. Playback, `--clock`, and `use_sim_time`

```bash
ros2 bag play run_042
ros2 bag play run_042 --clock          # also publish /clock at 40 Hz
ros2 bag play run_042 --clock 200      # at 200 Hz
ros2 bag play run_042 -r 0.5 -l        # half speed, looping
ros2 bag play run_042 --topics /scan   # replay a subset
ros2 bag play run_042 --remap /scan:=/scan_replay
ros2 bag play run_042 --start-offset 30 --playback-duration 5
```

Without `--clock`, playback is just a publisher: it republishes the recorded messages, spaced as they were recorded, while every node continues to read the wall clock. That is fine for looking at data and wrong for anything that reasons about time, because the messages carry stamps from the day of the recording and the nodes believe it is today. TF lookups fail or extrapolate; any comparison of a message stamp with `now()` is nonsense.

`--clock` makes playback the system's **time source**: it publishes `rosgraph_msgs/msg/Clock` on `/clock` at 40 Hz by default, or at the frequency you pass. Nodes that were started with `use_sim_time` true then take their `now()` from that topic, and the replayed run happens, as far as they can tell, at the time it was recorded. This is the mechanism from §10 of [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] with the bag standing in for the simulator.

The two halves must agree, and this is where people lose an afternoon:

- `--clock` **without** `use_sim_time` on the consumer: `/clock` is published and ignored. Stamps are old, `now()` is today, TF fails.
- `use_sim_time` true **without** `--clock`: the node's clock starts at zero and never advances. Timers never fire, and a time of zero means uninitialised, not the epoch. The node looks hung.

Set `use_sim_time` in the launch file for the whole graph, not per node, and verify it on a node you did not write with `ros2 param get <node> use_sim_time`.

### 9. A bag as a regression fixture

This is the payoff. A perception bug that only appears with the robot in front of you is a bug you fix at the robot's availability. Record the input once, and it becomes a fixture:

1. Record the inputs of the component, `/tf` and `/tf_static` included, at the moment the bug occurs.
2. Store the bag with the code commit, the parameter dump and the container tag that produced it (section 13).
3. Fix the bug against replay, on your laptop, at 0.5× speed with a debugger attached.
4. Keep the bag. It is now a test case: replay it in CI and assert the output.

Two cautions. Replay is **not** bit-identical to the live run: the official tutorial says so plainly about turtlesim, which "is sensitive to small changes in the system's timing". Message arrival order across topics, executor scheduling and wall-clock jitter all differ. Assert on outcomes with tolerance — "a detection appeared within 200 ms of this stamp" — not on exact floating-point equality. And use `--remap` to feed the replayed data to a node under a different name when the live topic is also present, so you know which stream you are testing.

A bag also makes a bug *communicable*. "It fails here" plus a bag is a report someone else can act on; without the bag it is an anecdote.

### 10. Unit tests inside a ROS package

The algorithm should be testable without a graph. This is the practical reason to keep the ROS edge of your node thin, as 25.1 argued: a function that takes a point cloud and returns a pose is testable in milliseconds; a node is not.

**Python** (`ament_python`). Tests go in a `tests/` directory in the package root, in files matching `test_*.py`, and `setup.py` declares the dependency:

```python
setup(
    # ...
    tests_require=['pytest'],
)
```

```python
# tests/test_geometry.py
from my_pkg.geometry import wrap_angle

def test_wrap_angle_is_symmetric():
    assert wrap_angle(3.5) == -wrap_angle(-3.5)
```

**C++** (`ament_cmake`), with GTest:

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(${PROJECT_NAME}_geometry_test test/geometry_test.cpp)
  target_include_directories(${PROJECT_NAME}_geometry_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
  # target_link_libraries(${PROJECT_NAME}_geometry_test my_library)
endif()
```

```xml
<test_depend>ament_cmake_gtest</test_depend>
```

Running them, from the workspace root — you do **not** need to source the workspace first, `colcon test` arranges the environment:

```bash
colcon test --packages-select my_pkg
colcon test-result --all --verbose          # which test cases failed, not just how many
colcon test --packages-select my_pkg --event-handlers console_cohesion+   # see output as it runs
colcon test --packages-select my_pkg --pytest-args -k test_wrap_angle     # one test
```

`colcon test` exits zero even when tests fail; `colcon test-result --all` is what tells you. Forgetting that is how a green-looking build ships a broken package.

### 11. launch_testing: the integration layer

Unit tests do not catch "the two nodes never connect", which is the bug class this whole page is about. That needs a real graph, and `launch_testing` provides one: a Python launch file that starts the system, runs `unittest` tests against it while it is running, and runs a second set after shutdown.

```python
import unittest
import launch, launch_ros, launch_testing.actions, rclpy
from turtlesim.msg import Pose

def generate_test_description():
    return (launch.LaunchDescription([
        launch_ros.actions.Node(package='turtlesim', executable='turtlesim_node', name='turtle1'),
        launch.actions.TimerAction(period=0.5, actions=[launch_testing.actions.ReadyToTest()]),
    ]), {})

class TestTurtleSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('test_turtlesim')

    def tearDown(self):
        self.node.destroy_node()

    def test_logs_spawning(self, proc_output):
        proc_output.assertWaitFor('Spawning turtle [turtle1] at x=', timeout=5, stream='stderr')

@launch_testing.post_shutdown_test()
class TestTurtleSimShutdown(unittest.TestCase):
    def test_exit_codes(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
```

Four pieces, and each is load-bearing: `generate_test_description` says what to launch; `ReadyToTest()` marks the point where the active tests may start; the undecorated `TestCase` holds the active tests, with `proc_output` giving access to the nodes' stdout and stderr; the `@post_shutdown_test()` class checks that everything exited cleanly, which catches the node that produces correct output and then segfaults.

Register it so `colcon test` runs it, with a unique `ROS_DOMAIN_ID` per test so that two tests running in parallel cannot talk to each other:

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_ros REQUIRED)
  find_package(launch_testing_ament_cmake REQUIRED)
  function(add_ros_isolated_launch_test path)
    set(RUNNER "${ament_cmake_ros_DIR}/run_test_isolated.py")
    add_launch_test("${path}" RUNNER "${RUNNER}" ${ARGN})
  endfunction()
  add_ros_isolated_launch_test(test/test_integration.py)
endif()
```

Inside the active tests, use `rclpy.spin_once(self.node, timeout_sec=1)` in a bounded loop rather than `rclpy.spin`, which never returns. `launch_testing_ros` provides conveniences such as `WaitForTopics`, and `launch_pytest` is an alternative with the same purpose.

### 12. What belongs in continuous integration

CI is not "run all the tests". It is the set of checks that must pass before a change is allowed to land, chosen so they run in minutes on a machine with no robot attached.

Put in: the build from a clean checkout (`rosdep install` then `colcon build`), the unit tests, the linters `ament_lint` runs from your `test_depend` entries, and the launch_testing integration tests, including the bag-driven regression tests from section 9. A bag test is the highest-value thing in this list, because it is the only one that tests your perception code against real sensor data on every commit.

Keep out, or move to a nightly job: anything that needs hardware, anything that needs a GUI, and long Gazebo runs. A CI job that takes forty minutes is a CI job people learn to ignore.

The thing to actually check is that CI runs on a **pinned base image**. A pipeline that installs "the latest ROS 2 Jazzy packages" is a pipeline whose result changes underneath you, and it will break on a Tuesday for reasons unrelated to your commit.

### 13. Containers, and the difference between a result and a story

```dockerfile
FROM osrf/ros:jazzy-desktop

RUN apt-get update && apt-get install -y --no-install-recommends \
      ros-jazzy-rosbag2-storage-mcap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY src/ /ws/src/
RUN . /opt/ros/jazzy/setup.sh \
    && rosdep install --from-paths src --ignore-src -r -y \
    && colcon build --symlink-install
```

Official images are published as `ros:jazzy` (base) and `osrf/ros:jazzy-desktop` (with the desktop tools). Pin the distribution in the tag, and for anything you will cite, record the image **digest** as well — tags are mutable.

The reason this matters is not tidiness. "I ran this on my laptop and got 87%" is a story. "Here is the image digest, the commit, the bag, the parameter dump and the command" is a result, because someone else can obtain it. Those two things look identical in a paper and are different kinds of object.

What to record for a run — the code commit, dependencies or container, data versions, seeds, commands, configurations, calibration, frame conventions, raw logs, exclusions, and analysis scripts — is the artifact checklist in [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]] §7, which also draws the distinction between repeatability, reproducibility and replicability that you will need when a reviewer asks which one you demonstrated. That page sets the standard; this page gives you the ROS 2 tools that meet it. `ros2 param dump` and `ros2 bag info` are two of the checklist entries, obtainable in one command each.

And when a run fails rather than succeeds, the discipline for turning that into an analysis rather than an anecdote is [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis & System Evaluation]].

### 14. Exercise: record, replay, and prove the node did not notice

One sitting, using any simulated robot from this track — turtlesim is enough if a simulator is not yet running.

1. Start the simulated system. In another terminal, record a short run of the topics one downstream node consumes, plus the transforms:

```bash
ros2 bag record --topics /turtle1/pose /turtle1/cmd_vel -o live_run
```

2. While recording, capture the live behaviour of the node under test. Log its output topic to a file so you have something to compare against:

```bash
ros2 topic echo /your_node_output > live_output.txt
```

Also capture its configuration: `ros2 param dump /your_node > live_params.yaml`.

3. Stop the recording and inspect it. Check the Count of each topic against what you expected:

```bash
ros2 bag info live_run
```

4. Shut the simulator down entirely. Start only the node under test, on simulated time:

```bash
ros2 run my_pkg my_node --ros-args -p use_sim_time:=true
ros2 param get /my_node use_sim_time     # confirm: true
```

5. Replay as the time source:

```bash
ros2 bag play live_run --clock
```

6. Capture the replayed output the same way and compare it with `live_output.txt`.

You are done when the replayed output matches the live output within timing tolerance, and — the part that matters — when you can state why it matches: the node's `now()` came from `/clock`, `/clock` came from the bag, and the bag's timestamps are the ones the live run produced. The node cannot tell the difference. You now have a development loop that does not require the robot.

### 15. The failure to diagnose: a bag that replays but produces nothing

The symptom. `ros2 bag play` runs, prints its startup lines, counts down its duration and exits normally. The downstream node produces nothing. `ros2 bag info` shows healthy message counts. Nothing errors.

There are two usual causes, and one command separates them.

**Cause A: the clock.** Either playback is publishing `/clock` and the node is not on simulated time, or the node is on simulated time and nothing is publishing `/clock`. The second is the silent-hang shape: the node's clock sits at zero, its timers never fire, and every TF lookup fails.

**Cause B: QoS durability (or reliability).** rosbag2 adapts its profiles and tries to preserve the durability the topic originally offered, but a subscriber that requests `transient_local` from a player offering `volatile`, or requests `reliable` from a `best_effort` offer, connects to nothing. Both endpoints exist and look healthy. This is the 25.5 failure mode arriving through the bag.

The separation, in order:

```bash
# 1. Are messages on the wire at all, during playback?
ros2 topic hz /scan
```

If `hz` reports a rate, the player is publishing and the data is moving — go to cause A. If `hz` reports nothing, either the player is not publishing that name or nobody can receive it — go to cause B, and check the name first:

```bash
# 2. Is it the name? Compare what the bag holds with what the node subscribes to.
ros2 bag info live_run | grep Topic
ros2 node info /my_node
```

```bash
# 3. Is it QoS? Compare the player's offer with the subscriber's request.
ros2 topic info /scan --verbose
```

Read the Reliability and Durability lines of each endpoint. If they are incompatible, fix it with an override file rather than editing code:

```yaml
# durability_override.yaml
/scan:
  durability: transient_local
  history: keep_all
```

```bash
ros2 bag play live_run --clock --qos-profile-overrides-path durability_override.yaml
```

For cause A, two commands settle it:

```bash
ros2 topic hz /clock                      # is anything publishing a time source
ros2 param get /my_node use_sim_time      # does the node believe it should listen
```

Both true or both false. Either mixture is the bug. If `/clock` is silent, you forgot `--clock` on the player; if `use_sim_time` is false, you forgot it in the launch file, and it is worth checking every node in the graph, because the one you forgot is never the one you suspected.

A third cause, rarer but worth knowing: the bag recorded a namespaced topic name and the node subscribes to the bare one. `--remap /ns/scan:=/scan` on the player fixes it without re-recording.

### 16. What this page does not cover

Tracing — instrumenting the middleware itself with LTTng to see callback-level timing — is the ROS 2 tracing documentation, and it is the right tool when the question is "where did the 40 ms go" rather than "why is nothing arriving". Getting backtraces from a crashing node under GDB is its own how-to guide. DDS-level packet inspection belongs to your middleware vendor's tooling. Formal coverage, mutation testing and the ROS build farm are beyond this track. Hardware-in-the-loop testing and what changes when replay meets a real robot are [[04-robotics/ros2/index|25. ROS 2]]. The experimental standard this page's tooling is meant to satisfy — units of analysis, comparisons, uncertainty, the artifact checklist — is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]].

### Sources

- ROS 2 Jazzy documentation — Tutorials: Recording and playing back data; Using `ros2doctor` to identify issues; Using `rqt_console` to view logs; Debugging tf2 problems.
- ROS 2 Jazzy documentation — Tutorials, Testing: Why automatic tests?; Running tests from the command line; Writing basic tests with Python; Writing basic tests with C++ with GTest; Writing basic integration tests with `launch_testing`.
- ROS 2 Jazzy documentation — Concepts: Logging and logger configuration (severity levels, targets, `ROS_LOG_DIR`/`ROS_HOME`, node options); Overview and usage of RQt.
- ROS 2 Jazzy documentation — Tutorials: RViz user guide (display status, fixed frame); Logging and logger configuration demo (logger services).
- ROS 2 Jazzy documentation — How-to guides: rosbag2 Overriding QoS policies for recording and playback; Run 2 nodes in single or separate Docker containers.
- Source, Jazzy branches, for every flag quoted: `ros2cli` (`ros2doctor/command/doctor.py`, `ros2node/verb/info.py`, `ros2param/verb/dump.py`, `ros2topic/verb/{hz,bw,delay}.py`); `rosbag2` (`ros2bag/verb/{record,play,info}.py`, repository README on storage plugins and the default `mcap`).
- ROS 2 design article — Clock and Time (`/clock`, `use_sim_time`, time of zero as uninitialised).

> [!question]- Self-check · Answer
> **1. Your node produces no output. You are certain the publisher is fine. Which check do you run first, and why not the one you think is the problem?** Check 0: the environment of the shell, then down the list in order. The point of the order is that certainty is exactly what is wrong — the cases where you are sure are the cases you skip and then spend an hour on. `ros2 node list`, `ros2 node info`, `ros2 topic hz`, `ros2 topic info`, `--verbose` for QoS, `tf2_echo`, `/clock`. Stop at the first failure.
> **2. `ros2 topic hz /scan` reports a healthy 30 Hz and `ros2 topic delay /scan` reports a delay growing by a second every second. What is happening, and why does `hz` not show it?** Something upstream is falling behind and its output is queued: messages arrive at the right rate but each one is older than the last. `hz` measures the interval between arrivals, which is unchanged by a constant backlog; only `delay`, which compares the header stamp with the arrival time, sees the accumulating age. A bounded delay is latency, a growing delay is a queue you will eventually lose.
> **3. Why is `ros2 bag record -a` a bad default for a research recording, beyond disk space?** Because the recorder must serialise and write everything it subscribed to, and when it cannot keep up it drops messages — so the topic you actually cared about comes home incomplete, with no error. `ros2 bag info`'s Count column is where you find out, usually too late. A 400 GB bag also cannot be shared, put in CI, or iterated on.
> **4. A bag replays with `--clock`, `ros2 bag info` shows thousands of messages, and your node produces nothing. Name the two usual causes and the one command that tells them apart.** The clock (the node is not on `use_sim_time`, or is on it with nothing publishing `/clock`) and QoS durability or reliability (the subscriber requests more than the player offers, so no connection is made). `ros2 topic hz /scan` during playback separates them: a reported rate means data is on the wire and the problem is time; silence means the problem is the connection, so compare names with `ros2 node info` and then profiles with `ros2 topic info /scan --verbose`.

## 한국어

### 1. 이 페이지가 존재하는 이유

동작하지 않는 ROS 2 시스템은 대개 에러를 내지 않는다. 노드가 뜨고, 기동 로그를 찍고, 그다음 아무 일도 없다. 스택 트레이스도, 예외도, 종료 코드도 없다. 영원히 메시지를 주고받지 못할 두 노드는 곧 주고받을 두 노드와 정확히 똑같아 보인다.

그러면 대부분은 추측한다. 다시 띄워 보고, print를 넣고, 숫자를 바꾸고, 또 다시 띄운다. 가끔 고쳐지는데 왜 고쳐졌는지 모른다. 이건 실패보다 나쁘다. 3주 뒤에 같은 버그가 돌아오고 추측이 처음부터 다시 시작되기 때문이다.

대안은 짐작이 있든 없든 매번 같은 순서로 돌리는 점검 목록이다. 개별 점검보다 순서가 중요하다. 순서가 있으면 명령 하나로 원인 부류 전체를 지울 수 있고, 그러지 않으면 계속 맴돈다. **그 순서를 가졌는가가 엔지니어와 추측하는 사람을 가른다.** 이 페이지의 대부분은 그 이야기다.

뒤쪽 절반은 같은 규율을 증거에 적용한 것이다. 로봇을 눈앞에 두어야만 재현되는 버그는 느리게 고쳐진다. 내 노트북에서만 나오는 결과는 아직 결과가 아니다.

### 2. 순서 있는 점검 목록

위에서 아래로 돌린다. 처음 실패하는 지점에서 멈춘다. 안다고 생각해서 건너뛰지 않는다.

| # | 질문 | 명령 | 실패의 의미 |
|---|---|---|---|
| 0 | 이 셸의 환경이 내가 생각하는 그것인가? | `printenv \| grep -i ros` | source 안 한 셸, 잘못된 오버레이, 엉뚱한 `ROS_DOMAIN_ID`. 25.4 참고. |
| 1 | 노드가 떠 있기는 한가? | `ros2 node list` | 기동 중 죽었거나, 다른 도메인에 있거나, launch가 아예 띄우지 않았다. |
| 2 | 노드에 내가 기대한 엔드포인트가 있는가? | `ros2 node info /my_node` | 잊은 remap, 또는 소스에서 읽은 이름과 다른 이름으로 만든 구독. |
| 3 | 토픽에 실제로 뭔가 발행되는가? | `ros2 topic hz /my_topic` | 상류 노드는 살아 있으나 조용하다. 자기 입력이 없거나 타이머가 안 돈다. |
| 4 | 구독자가 있는가? | `ros2 topic info /my_topic` | 구독자 없는 퍼블리셔. 소비자가 다른 이름에 붙어 있다. |
| 5 | QoS 프로파일이 맞는가? | `ros2 topic info /my_topic --verbose` | reliability 또는 durability 불일치. 엔드포인트는 있고 개수도 0이 아닌데 데이터가 안 간다. |
| 6 | 프레임이 있고, 충분히 최신인가? | `ros2 run tf2_ros tf2_echo map base_link` | 퍼블리셔 누락, 끊어진 트리, 또는 보간하기엔 너무 오래된 스탬프. |
| 7 | 시계가 맞는가? | `ros2 topic hz /clock`, `ros2 param get /my_node use_sim_time` | 그래프의 절반은 시뮬레이션 시간, 절반은 벽시계. |

3번과 4번의 조합이 가장 쓸모 있다. "아무도 안 보낸다"와 "아무도 안 듣는다"를 가른다. 증상은 같고 원인은 반대다. 5번은 그 둘을 통과하고도 데이터가 안 움직이는 경우를 잡는다. DDS가 들여온 실패 양식이고 25.5가 해부한다.

이 표를 책상 근처에 붙여 두어라. 그리고 고장이 나면 확신하는 항목까지 포함해 전부 돌려라.

### 3. 내성(introspection) 도구 모음

`ros2 doctor`는 품이 안 드는 첫 관찰이다. 인자 없이 돌리면 모든 점검을 하고 `All <n> checks passed` 또는 실패 개수를 찍는다. 경고는 기본적으로 무시되므로 실패로 취급하려면 `--include-warnings`(`-iw`)를 붙인다. 돌아가는 시스템에서는 구독자 없는 퍼블리셔와 퍼블리셔 없는 구독자를 보고하는데, 이는 그래프 전체에 대해 4번 점검을 자동으로 한 것이다.

```bash
ros2 doctor
ros2 doctor --include-warnings
ros2 doctor --report          # NETWORK CONFIGURATION, PLATFORM INFORMATION, RMW MIDDLEWARE, ROS 2 INFORMATION, TOPIC LIST
ros2 doctor --report-failed   # 실패한 점검만
```

`--report`는 버그 리포트나 동료에게 보내는 메시지에 붙여 넣는 것이다. 문제 설명에서 빠지기 마련인 환경 정보를 담는다. 문서는 `ros2doctor`가 디버그 도구가 아니라고 분명히 말한다. 코드가 아니라 설정을 점검한다.

`ros2 node info`는 노드의 표면 전체를 찍는다. Subscribers, Publishers, Service Servers, Service Clients, Action Servers, Action Clients와 각각의 타입. `_`로 시작하는 토픽(서비스 이벤트 토픽 등)이 얽히면 `--include-hidden`을 붙인다.

세 가지 측정 도구는 서로 다른 질문에 답하는데 늘 혼동된다.

```bash
ros2 topic hz /scan              # 메시지 도착률, 윈도 평균
ros2 topic hz /scan -w 1000      # 긴 윈도: 숫자의 흔들림이 줄어든다
ros2 topic hz /scan --wall-time
ros2 topic bw /scan              # 초당 바이트 — 이 토픽이 네트워크를 채우는 원인인가
ros2 topic delay /scan           # 도착 시점 기준 header 스탬프의 나이
```

`hz`는 얼마나 자주 오는지, `bw`는 얼마나 비싼지, `delay`는 **지연**을 잰다. 메시지 안의 스탬프와 수신 시각의 차이이고, 따라서 메시지 타입에 `std_msgs/Header`가 있어야 한다. `hz`는 완벽한데 `delay`가 끝없이 커지는 시스템은 어딘가 큐가 차오르는 시스템이고, 그것을 보여 주는 것은 `delay`뿐이다. 시뮬레이션에서는 `--wall-time`이 의미를 갖는다. 철자가 그것이고, `bw`나 `delay`가 아니라 `hz`에만 있다. 기본값은 흔한 짐작과 반대다. CLI 노드는 `-s`/`--use-sim-time`을 주지 않는 한 wall time으로 도니, 그냥 `ros2 topic hz`는 이미 CPU가 실제로 한 일을 재고 있다. 시뮬레이션 기준 속도를 재려면 `-s`를, 시계를 믿을 수 없을 때 wall time으로 되돌리려면 `--wall-time`을 준다.

```bash
ros2 param dump /my_node > my_node_params.yaml
```

`ros2 param dump`는 노드의 파라미터 전체를 YAML로 표준출력에 찍는다. 리다이렉트는 직접 한다. 용도는 둘이다. 오작동하는 노드의 실제 파라미터를 내가 넣었다고 믿는 YAML과 비교하는 것, 그리고 실행의 정확한 설정을 산출물로 남기는 것(13절). `--timeout N`은 노드가 나타날 때까지 기다린다.

변환(transform)은 도구가 셋이다.

```bash
ros2 run tf2_ros tf2_echo map base_link      # 이 변환이 있는가, 값은 무엇인가
ros2 run tf2_tools view_frames               # 트리 전체를 파일로 렌더링
ros2 run tf2_ros tf2_monitor map base_link   # 프레임별 발행률과 지연 통계
```

*끊어진* 트리를 찾아 주는 것은 `view_frames`다. 각각은 멀쩡한데 사이에 간선이 없는 두 부분 트리는 "not part of the same tree" 메시지 말고는 보기 어렵다.

rqt 플러그인은 같은 데이터에 시간축을 붙인 것이고, 그게 핵심일 때가 있다.

| 플러그인 | 실행 | 쓸 때 |
|---|---|---|
| `rqt_graph` | `ros2 run rqt_graph rqt_graph` | 누가 누구와 연결됐는지 봐야 하고, `node info`를 열 번 읽는 것보다 그림이 빠를 때. |
| `rqt_console` | `ros2 run rqt_console rqt_console` | 로그가 너무 빨리 지나가고, 심각도·노드·문자열로 걸러야 할 때. |
| `rqt_plot` | `ros2 run rqt_plot rqt_plot` | 숫자가 이상한데 지금 값이 아니라 시간에 따른 모양이 필요할 때. |
| `rqt_reconfigure` | `ros2 run rqt_reconfigure rqt_reconfigure` | 재시작하지 않고 파라미터를 실시간으로 조율할 때. |
| `rqt_bag` | `ros2 run rqt_bag rqt_bag` | 녹화를 훑으며 특정 메시지 하나를 볼 때. |

`rqt`를 띄워 한 창에 도킹해도 된다. 공용 묶음은 `sudo apt install ros-jazzy-rqt ros-jazzy-rqt-common-plugins`.

### 4. 데모가 아니라 디버거로서의 RViz

대부분의 튜토리얼은 RViz를 스크린샷 만드는 도구로 소개한다. 두 가지 기능을 가진 디버거로 다뤄라.

첫째, **Display Status**. 모든 display는 `OK`, `Warning`, `Error`, `Disabled` 중 하나의 상태를 갖고, 제목의 배경색으로 표시되며 펼치면 구체적인 메시지가 나온다. PointCloud2 display의 Error가 없는 프레임 이름을 말하고 있다면 6번 점검이 실패했다는 뜻이고, 그것도 이미 보고 있던 그 자리에서 알려 준다. 대부분은 이걸 펼쳐 보지 않는다.

둘째, **Fixed Frame**. 세계를 그리는 기준 프레임이고, 세계에 대해 움직이면 안 된다. `base_link`가 아니라 `map`이나 `odom`이다. 로봇 몸체로 설정하면 로봇이 본 모든 물체가 로봇 앞에 나타난다. "센서 데이터가 엉뚱한 데 찍힌다" 부류의 상당수는 보정 오류가 아니라 Fixed Frame 선택이다. 또 Fixed Frame을 바꾸면 현재 표시 중인 데이터는 재변환되지 않고 지워진다. 바꾼 직후 화면이 빈 것은 정상이다.

들일 습관은 이렇다. RViz에 데이터가 안 보이면 카메라를 만지지 말고, Display Status를 읽고, Fixed Frame을 확인하고, fixed frame과 데이터 프레임 사이로 `tf2_echo`를 돌려라.

### 5. 로깅: 수준, 출력 위치, 런타임에 한 노드만 올리기

심각도는 오름차순으로 `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`. 로거는 자기 수준 이상만 처리하고 기본값은 `INFO`다. 그래서 요청하기 전까지 `DEBUG` 줄은 아무것도 안 나온다.

모든 메시지는 세 곳으로 가고, 각각 노드 단위로 끌 수 있다.

- **콘솔**. 기본은 stderr (`RCUTILS_LOGGING_USE_STDOUT=1`이면 stdout).
- **디스크 파일**. `rcl_logging_spdlog`가 쓴다. `$ROS_LOG_DIR`이 설정돼 있으면 그곳, 아니면 `$ROS_HOME/log`이고 `ROS_HOME` 기본값은 `~/.ros`이므로 대개 `~/.ros/log/`.
- **`/rosout` 토픽**. `rqt_console`과 `ros2 topic echo /rosout`이 다른 기계의 노드 로그를 보는 통로.

`~/.ros/log`는 "노드가 죽었는데 터미널이 사라졌다"의 답이다. 동시에 "디스크가 찼다"의 답이기도 하다. 아무것도 자동으로 회전시켜 주지 않는다.

기동 시 수준 설정은 `--ros-args`로 한다.

```bash
ros2 run turtlesim turtlesim_node --ros-args --log-level WARN          # 프로세스 기본값
ros2 run demo_nodes_cpp talker --ros-args --log-level talker:=DEBUG    # 지정한 로거 하나
ros2 run my_pkg my_node --ros-args --disable-rosout-logs               # 로봇에서 대역폭을 실제로 아낀다
```

노드가 스무 개인 시스템에서 의미 있는 것은 두 번째 형태다. 하나만 `DEBUG`로 올리고 나머지는 `INFO`로 둔다. 로거 이름은 계층이라, `abc`를 바꾸면 명시적으로 설정하지 않은 `abc.def`도 함께 바뀐다.

재시작 없이 **런타임에** 바꾸는 것도 가능하지만 기본은 꺼져 있다. 노드가 켜 줘야 한다.

```python
node = Node('NodeWithLoggerService', enable_logger_service=True)
```

```cpp
auto node = std::make_shared<rclcpp::Node>(
  "NodeWithLoggerService", rclcpp::NodeOptions().enable_logger_service(true));
```

그러면 서비스 두 개가 노출된다. 수준은 숫자다(10 = DEBUG, 20 = INFO).

```bash
ros2 service call /NodeWithLoggerService/set_logger_levels rcl_interfaces/srv/SetLoggerLevels \
  '{levels: [{name: "NodeWithLoggerService", level: 10}]}'
ros2 service call /NodeWithLoggerService/get_logger_levels rcl_interfaces/srv/GetLoggerLevels \
  '{names: ["NodeWithLoggerService"]}'
```

> [!warning] 문서화된 제약
> Jazzy 기준으로 `get_logger_levels`와 `set_logger_levels`는 스레드 안전하지 않다. 한 번에 한 스레드만 호출해야 한다.

직접 쓰는 노드에서는 이걸 켜 두어라. 비용은 생성자 인자 하나이고, 이득은 그 현상을 만든 실행을 끄지 않은 채 드문 결함을 진단할 수 있다는 것이다.

### 6. rosbag2: 기록, 그리고 전부 기록하는 것이 대개 틀린 이유

```bash
ros2 bag record --topics /scan /odom /tf /tf_static -o run_042
```

`--topics`는 공백으로 구분된 목록을 받고 `-o`는 출력 디렉터리 이름을 정한다. (맨 위치 인자는 아직 동작하고 deprecation 안내를 찍는다. `--topics`를 써라. `record`에는 `-t` 단축 옵션이 없다. `-t`는 `ros2 bag info`의 것이라, `record -t /scan`은 deprecation이 아니라 오류다.) bag은 파일 하나가 아니라 `metadata.yaml`과 하나 이상의 저장 파일을 담은 **디렉터리**다.

`-a`는 전부 기록한다. 연구용 녹화의 기본값으로는 거의 항상 틀렸다.

- **디스크와 대역폭.** 압축하지 않은 1080p 카메라 토픽 하나가 30 Hz면 초당 약 190 MB다. 1920 × 1080 × 3바이트 × 30이다. 실험 도중 로봇의 디스크가 찬다.
- **메시지 유실.** 기록기는 요청받은 것을 전부 직렬화해서 써야 한다. 너무 많이 요청하면 뒤처지고, 집에 가져온 bag에는 정작 필요한 메시지가 빠져 있다. 조용히.
- **쓸 수 없음.** 400 GB짜리 bag은 공유할 수도, CI에 넣을 수도, 빠르게 열어 반복할 수도 없다.

디버깅하려는 구성요소의 입력, 거기에 `/tf`와 `/tf_static`, 그리고 결과를 판정하는 데 필요한 것을 기록하라. 어떤 토픽이 왜 목록에 있는지 말할 수 없다면 빼라.

정말 양이 필요할 때 쓰는 플래그들.

```bash
ros2 bag record -e "^/camera/.*" --exclude-regex ".*/compressedDepth" -o cam   # 패턴으로
ros2 bag record --topics /scan -b 2000000000                                   # 2 GB마다 분할
ros2 bag record --topics /scan -d 60                                           # 60초마다 분할
ros2 bag record -a --compression-mode file --compression-format zstd -o run    # 파일 단위 압축
ros2 bag record --topics /scan --use-sim-time                                  # 시뮬레이션에서 /clock 기준 스탬프
```

기록기 터미널에서 SPACE를 누르면 일시정지/재개다. `--snapshot-mode`는 메시지를 메모리에 들고 있다가 `/rosbag2_recorder/snapshot`을 호출할 때만 쓴다. 긴 실행에서 "고장 직전 10초만 기록"에 맞는 도구다.

### 7. `ros2 bag info`와 저장 플러그인

```bash
ros2 bag info run_042
```

```text
Files:             run_042_0.mcap
Bag size:          228.5 KiB
Storage id:        mcap
Duration:          48.47s
Start:             Oct 11 2019 06:09:09.12 (1570799349.12)
End                Oct 11 2019 06:09:57.60 (1570799397.60)
Messages:          3013
Topic information: Topic: /turtle1/cmd_vel | Type: geometry_msgs/msg/Twist | Count: 9 | Serialization Format: cdr
                   Topic: /turtle1/pose | Type: turtlesim/msg/Pose | Count: 3004 | Serialization Format: cdr
```

다른 무엇보다 **Count** 열을 먼저 읽어라. 기록했다고 믿은 토픽의 개수가 0이면 조사는 거기서 끝난다. 기록기가 아무도 발행하지 않는 이름을 구독한 것이다. `Duration × 예상 주기`보다 한참 적으면 기록기가 메시지를 흘린 것이고, 앞 절의 실패 양식이 증거로 드러난 것이다.

Jazzy의 rosbag2는 저장 플러그인 둘을 제공하고 `-s`로 고른다.

- **`mcap`** — 기본값. 자기 기술적이고 색인 가능한 컨테이너이며 ROS 밖의 도구 지원이 넓다. CLI의 `--compression-mode`와 달리 색인을 유지한 채 내부 압축이 가능하다.
- **`sqlite3`** — 기존 bag과 도구 호환을 위해 남은 예전 플러그인.

고를 일은 드물다. 기본값을 쓰되 `Storage id:` 줄이 무슨 뜻인지 알도록 `mcap`이라는 단어를 기억하라. 재생 시 저장 구현은 자동으로 판별된다.

### 8. 재생, `--clock`, 그리고 `use_sim_time`

```bash
ros2 bag play run_042
ros2 bag play run_042 --clock          # /clock도 40 Hz로 발행
ros2 bag play run_042 --clock 200      # 200 Hz로
ros2 bag play run_042 -r 0.5 -l        # 절반 속도, 반복
ros2 bag play run_042 --topics /scan   # 일부만 재생
ros2 bag play run_042 --remap /scan:=/scan_replay
ros2 bag play run_042 --start-offset 30 --playback-duration 5
```

`--clock` 없이는 재생은 그냥 퍼블리셔다. 기록된 간격대로 메시지를 다시 발행할 뿐 모든 노드는 계속 벽시계를 읽는다. 데이터를 눈으로 보는 데는 괜찮고, 시간을 따지는 어떤 것에도 틀렸다. 메시지는 녹화 당일의 스탬프를 달고 있는데 노드는 오늘이라고 믿기 때문이다. TF 조회는 실패하거나 외삽되고, 메시지 스탬프와 `now()`의 비교는 전부 무의미해진다.

`--clock`은 재생을 시스템의 **시간 소스**로 만든다. `/clock`에 `rosgraph_msgs/msg/Clock`을 기본 40 Hz로, 또는 지정한 주기로 발행한다. `use_sim_time`을 true로 띄운 노드는 `now()`를 거기서 가져오고, 재생된 실행은 그 노드가 아는 한 녹화된 그 시각에 일어난다. [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] §10의 기제에서 시뮬레이터 자리에 bag이 들어간 것이다.

양쪽이 일치해야 하고, 여기서 사람들이 반나절을 잃는다.

- 소비자에 `use_sim_time` 없이 `--clock`만: `/clock`은 발행되고 무시된다. 스탬프는 옛날, `now()`는 오늘, TF 실패.
- `--clock` 없이 `use_sim_time`만 true: 노드 시계가 0에서 시작해 전혀 나아가지 않는다. 타이머가 안 돌고, 시간 0은 에포크가 아니라 초기화 안 됨을 뜻한다. 노드가 멈춘 것처럼 보인다.

`use_sim_time`은 노드마다가 아니라 launch 파일에서 그래프 전체에 설정하고, 직접 쓰지 않은 노드에 대해 `ros2 param get <node> use_sim_time`으로 확인하라.

### 9. 회귀 fixture로서의 bag

여기가 보상이다. 로봇을 눈앞에 둬야만 나타나는 인지 버그는 로봇의 가용 시간에 맞춰 고쳐진다. 입력을 한 번 기록하면 그것이 fixture가 된다.

1. 버그가 나는 순간에 그 구성요소의 입력을 `/tf`, `/tf_static`까지 포함해 기록한다.
2. bag을 만든 코드 커밋, 파라미터 덤프, 컨테이너 태그와 함께 보관한다(13절).
3. 재생에 대고 버그를 고친다. 노트북에서, 0.5배속으로, 디버거를 붙이고.
4. bag을 버리지 않는다. 이제 테스트 케이스다. CI에서 재생하고 출력을 검증한다.

주의 둘. 재생은 라이브 실행과 비트 단위로 동일하지 **않다**. 공식 튜토리얼도 turtlesim에 대해 "시스템 타이밍의 작은 변화에 민감하다"고 분명히 말한다. 토픽 간 도착 순서, executor 스케줄링, 벽시계 지터가 모두 다르다. 부동소수점 동일성이 아니라 허용오차를 둔 결과로 검증하라. "이 스탬프로부터 200 ms 안에 검출이 나왔다" 같은 식이다. 그리고 라이브 토픽이 같이 떠 있을 때는 `--remap`으로 다른 이름에 재생 데이터를 흘려서 어느 스트림을 테스트 중인지 분명히 하라.

bag은 버그를 *전달 가능*하게도 만든다. "여기서 실패한다" + bag은 남이 조치할 수 있는 보고이고, bag이 없으면 일화다.

### 10. ROS 패키지 안의 단위 테스트

알고리즘은 그래프 없이 테스트 가능해야 한다. 25.1이 말한 대로 노드의 ROS 가장자리를 얇게 유지하는 실질적 이유가 이것이다. 포인트 클라우드를 받아 자세를 반환하는 함수는 밀리초 단위로 테스트되고, 노드는 그렇지 않다.

**Python** (`ament_python`). 테스트는 패키지 루트의 `tests/` 디렉터리에 `test_*.py` 패턴 파일로 두고, `setup.py`가 의존을 선언한다.

```python
setup(
    # ...
    tests_require=['pytest'],
)
```

```python
# tests/test_geometry.py
from my_pkg.geometry import wrap_angle

def test_wrap_angle_is_symmetric():
    assert wrap_angle(3.5) == -wrap_angle(-3.5)
```

**C++** (`ament_cmake`), GTest 사용.

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(${PROJECT_NAME}_geometry_test test/geometry_test.cpp)
  target_include_directories(${PROJECT_NAME}_geometry_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
  # target_link_libraries(${PROJECT_NAME}_geometry_test my_library)
endif()
```

```xml
<test_depend>ament_cmake_gtest</test_depend>
```

워크스페이스 루트에서 실행한다. 미리 워크스페이스를 source할 필요는 **없다**. `colcon test`가 환경을 맞춰 준다.

```bash
colcon test --packages-select my_pkg
colcon test-result --all --verbose          # 몇 개가 아니라 어떤 케이스가 실패했는지
colcon test --packages-select my_pkg --event-handlers console_cohesion+   # 실행 중 출력 보기
colcon test --packages-select my_pkg --pytest-args -k test_wrap_angle     # 하나만
```

`colcon test`는 테스트가 실패해도 0으로 끝난다. 알려 주는 것은 `colcon test-result --all`이다. 이걸 잊으면 초록색으로 보이는 빌드가 깨진 패키지를 내보낸다.

### 11. launch_testing: 통합 계층

단위 테스트는 "두 노드가 끝내 연결되지 않는다"를 잡지 못한다. 이 페이지 전체가 다루는 버그 부류가 바로 그것이다. 진짜 그래프가 필요하고, `launch_testing`이 제공한다. 시스템을 띄우는 Python launch 파일에서, 돌아가는 동안 `unittest` 테스트를 돌리고, 종료 후 두 번째 묶음을 돌린다.

```python
import unittest
import launch, launch_ros, launch_testing.actions, rclpy
from turtlesim.msg import Pose

def generate_test_description():
    return (launch.LaunchDescription([
        launch_ros.actions.Node(package='turtlesim', executable='turtlesim_node', name='turtle1'),
        launch.actions.TimerAction(period=0.5, actions=[launch_testing.actions.ReadyToTest()]),
    ]), {})

class TestTurtleSim(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rclpy.init()

    @classmethod
    def tearDownClass(cls):
        rclpy.shutdown()

    def setUp(self):
        self.node = rclpy.create_node('test_turtlesim')

    def tearDown(self):
        self.node.destroy_node()

    def test_logs_spawning(self, proc_output):
        proc_output.assertWaitFor('Spawning turtle [turtle1] at x=', timeout=5, stream='stderr')

@launch_testing.post_shutdown_test()
class TestTurtleSimShutdown(unittest.TestCase):
    def test_exit_codes(self, proc_info):
        launch_testing.asserts.assertExitCodes(proc_info)
```

네 조각이고 각각이 일한다. `generate_test_description`은 무엇을 띄울지 말하고, `ReadyToTest()`는 활성 테스트를 시작해도 되는 지점을 표시하며, 데코레이터 없는 `TestCase`가 활성 테스트를 담고 `proc_output`으로 노드의 stdout/stderr에 접근한다. `@post_shutdown_test()` 클래스는 전부 정상 종료했는지 확인한다. 옳은 출력을 내고 나서 segfault로 죽는 노드를 잡는 것이 이것이다.

`colcon test`가 돌리도록 등록하되, 병렬로 도는 두 테스트가 서로 통신하지 못하게 테스트마다 고유한 `ROS_DOMAIN_ID`를 준다.

```cmake
if(BUILD_TESTING)
  find_package(ament_cmake_ros REQUIRED)
  find_package(launch_testing_ament_cmake REQUIRED)
  function(add_ros_isolated_launch_test path)
    set(RUNNER "${ament_cmake_ros_DIR}/run_test_isolated.py")
    add_launch_test("${path}" RUNNER "${RUNNER}" ${ARGN})
  endfunction()
  add_ros_isolated_launch_test(test/test_integration.py)
endif()
```

활성 테스트 안에서는 영원히 돌아오지 않는 `rclpy.spin` 대신 `rclpy.spin_once(self.node, timeout_sec=1)`을 유한 루프로 돌려라. `launch_testing_ros`는 `WaitForTopics` 같은 편의 함수를 주고, `launch_pytest`는 같은 목적의 대안이다.

### 12. 지속적 통합에 무엇이 들어가는가

CI는 "모든 테스트를 돌리기"가 아니다. 변경이 병합되기 전에 반드시 통과해야 하는 점검의 집합이고, 로봇이 달려 있지 않은 기계에서 몇 분 안에 끝나도록 고른다.

넣을 것: 깨끗한 체크아웃에서의 빌드(`rosdep install` 후 `colcon build`), 단위 테스트, `test_depend` 항목이 불러오는 `ament_lint` 린터, 그리고 9절의 bag 기반 회귀 테스트를 포함한 launch_testing 통합 테스트. 이 중 가치가 가장 높은 것은 bag 테스트다. 모든 커밋마다 실제 센서 데이터로 인지 코드를 검사하는 유일한 항목이기 때문이다.

뺄 것, 또는 야간 작업으로 옮길 것: 하드웨어가 필요한 것, GUI가 필요한 것, 긴 Gazebo 실행. 40분 걸리는 CI는 사람들이 무시하는 법을 배우는 CI다.

정작 확인해야 할 것은 CI가 **고정된 베이스 이미지**에서 도는가다. "최신 ROS 2 Jazzy 패키지"를 설치하는 파이프라인은 발밑에서 결과가 바뀌는 파이프라인이고, 당신 커밋과 무관한 이유로 어느 화요일에 깨진다.

### 13. 컨테이너, 결과와 이야기를 가르는 것

```dockerfile
FROM osrf/ros:jazzy-desktop

RUN apt-get update && apt-get install -y --no-install-recommends \
      ros-jazzy-rosbag2-storage-mcap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ws
COPY src/ /ws/src/
RUN . /opt/ros/jazzy/setup.sh \
    && rosdep install --from-paths src --ignore-src -r -y \
    && colcon build --symlink-install
```

공식 이미지는 `ros:jazzy`(기본)와 `osrf/ros:jazzy-desktop`(데스크톱 도구 포함)으로 배포된다. 태그에 배포판을 고정하고, 인용할 결과라면 이미지 **다이제스트**까지 기록하라. 태그는 변한다.

이게 중요한 이유는 단정함이 아니다. "내 노트북에서 돌려서 87퍼센트가 나왔다"는 이야기다. "이미지 다이제스트, 커밋, bag, 파라미터 덤프, 명령이 여기 있다"는 결과다. 남이 얻어낼 수 있기 때문이다. 논문에서는 둘이 똑같아 보이지만 서로 다른 종류의 물건이다.

한 번의 실행에 대해 무엇을 기록할지 — 코드 커밋, 의존성 또는 컨테이너, 데이터 버전, 시드, 명령, 설정, 보정, 프레임 규약, 원시 로그, 제외 내역, 분석 스크립트 — 는 [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]] §7의 산출물 체크리스트에 있다. 그 페이지는 repeatability, reproducibility, replicability의 구분도 준다. 리뷰어가 어느 쪽을 보였느냐고 물을 때 필요하다. 기준은 그 페이지가 세우고, 이 페이지는 그 기준을 충족하는 ROS 2 도구를 준다. `ros2 param dump`와 `ros2 bag info`는 각각 명령 하나로 얻는 체크리스트 항목이다.

실행이 성공이 아니라 실패했을 때, 그것을 일화가 아닌 분석으로 바꾸는 규율은 [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis & System Evaluation]]이다.

### 14. 실습: 기록하고, 재생하고, 노드가 눈치채지 못했음을 보여라

한 자리에서. 이 트랙의 어떤 시뮬레이션 로봇이든 좋고, 시뮬레이터가 아직 없다면 turtlesim으로 충분하다.

1. 시뮬레이션 시스템을 띄운다. 다른 터미널에서 하류 노드 하나가 소비하는 토픽과 변환을 짧게 기록한다.

```bash
ros2 bag record --topics /turtle1/pose /turtle1/cmd_vel -o live_run
```

2. 기록하는 동안 테스트 대상 노드의 라이브 동작을 잡아 둔다. 비교 대상이 있도록 출력 토픽을 파일로 남긴다.

```bash
ros2 topic echo /your_node_output > live_output.txt
```

설정도 잡는다: `ros2 param dump /your_node > live_params.yaml`.

3. 기록을 멈추고 들여다본다. 각 토픽의 Count를 기대치와 대조한다.

```bash
ros2 bag info live_run
```

4. 시뮬레이터를 완전히 내린다. 테스트 대상 노드만, 시뮬레이션 시간으로 띄운다.

```bash
ros2 run my_pkg my_node --ros-args -p use_sim_time:=true
ros2 param get /my_node use_sim_time     # true인지 확인
```

5. 시간 소스로서 재생한다.

```bash
ros2 bag play live_run --clock
```

6. 재생된 출력을 같은 방식으로 잡아 `live_output.txt`와 비교한다.

재생 출력이 타이밍 허용오차 안에서 라이브 출력과 일치하고, 그리고 — 여기가 핵심인데 — 왜 일치하는지 말할 수 있으면 끝이다. 노드의 `now()`는 `/clock`에서 왔고, `/clock`은 bag에서 왔고, bag의 타임스탬프는 라이브 실행이 만든 그것이다. 노드는 차이를 알 수 없다. 이제 로봇이 없어도 되는 개발 루프를 가졌다.

### 15. 진단할 고장: 재생은 되는데 아무것도 안 나오는 bag

증상. `ros2 bag play`는 돌고, 기동 줄을 찍고, 길이를 세고, 정상 종료한다. 하류 노드는 아무것도 내지 않는다. `ros2 bag info`는 멀쩡한 메시지 개수를 보여 준다. 에러는 없다.

흔한 원인은 둘이고, 명령 하나가 갈라 준다.

**원인 A: 시계.** 재생이 `/clock`을 발행하는데 노드가 시뮬레이션 시간이 아니거나, 노드는 시뮬레이션 시간인데 아무도 `/clock`을 발행하지 않는다. 후자가 조용히 멈추는 모양이다. 노드 시계가 0에 머물고, 타이머가 안 돌고, 모든 TF 조회가 실패한다.

**원인 B: QoS durability(또는 reliability).** rosbag2는 프로파일을 조정하고 토픽이 원래 제공하던 durability를 보존하려 하지만, `volatile`을 제공하는 플레이어에게 `transient_local`을 요구하는 구독자, 또는 `best_effort` 제공에 `reliable`을 요구하는 구독자는 아무것과도 연결되지 않는다. 양쪽 엔드포인트는 존재하고 멀쩡해 보인다. 25.5의 실패 양식이 bag을 통해 도착한 것이다.

가르는 순서.

```bash
# 1. 재생 중에 메시지가 선로 위에 있기는 한가?
ros2 topic hz /scan
```

`hz`가 주기를 보고하면 플레이어는 발행 중이고 데이터는 움직인다. 원인 A로 간다. `hz`가 아무것도 보고하지 않으면 플레이어가 그 이름으로 발행하지 않거나 아무도 받을 수 없는 것이다. 원인 B로 가되 이름부터 본다.

```bash
# 2. 이름 문제인가? bag이 가진 것과 노드가 구독하는 것을 비교.
ros2 bag info live_run | grep Topic
ros2 node info /my_node
```

```bash
# 3. QoS 문제인가? 플레이어의 offer와 구독자의 request를 비교.
ros2 topic info /scan --verbose
```

각 엔드포인트의 Reliability와 Durability 줄을 읽는다. 호환되지 않으면 코드를 고치는 대신 오버라이드 파일로 해결한다.

```yaml
# durability_override.yaml
/scan:
  durability: transient_local
  history: keep_all
```

```bash
ros2 bag play live_run --clock --qos-profile-overrides-path durability_override.yaml
```

원인 A는 명령 두 개로 끝난다.

```bash
ros2 topic hz /clock                      # 시간 소스를 발행하는 것이 있는가
ros2 param get /my_node use_sim_time      # 노드가 들어야 한다고 믿는가
```

둘 다 참이거나 둘 다 거짓이어야 한다. 어느 쪽이든 섞이면 그게 버그다. `/clock`이 조용하면 플레이어에 `--clock`을 빠뜨린 것이고, `use_sim_time`이 거짓이면 launch 파일에서 빠뜨린 것이다. 그래프의 모든 노드를 확인할 가치가 있다. 빠뜨린 그 노드는 한 번도 의심한 노드가 아니다.

드물지만 알아 둘 세 번째 원인. bag은 네임스페이스가 붙은 토픽 이름을 기록했는데 노드는 맨 이름을 구독한다. 다시 기록할 것 없이 플레이어에 `--remap /ns/scan:=/scan`을 주면 된다.

### 16. 이 페이지가 다루지 않는 것

트레이싱 — LTTng로 미들웨어 자체를 계측해 콜백 수준 타이밍을 보는 것 — 은 ROS 2 tracing 문서에 있고, 질문이 "왜 아무것도 안 오나"가 아니라 "그 40 ms가 어디로 갔나"일 때 맞는 도구다. GDB로 죽는 노드의 백트레이스를 얻는 것은 별도의 how-to 가이드다. DDS 수준 패킷 검사는 미들웨어 벤더의 도구 영역이다. 형식적 커버리지, 뮤테이션 테스팅, ROS build farm은 이 트랙 밖이다. 하드웨어 인 더 루프 테스트와 재생이 실물 로봇을 만날 때 달라지는 것은 [[04-robotics/ros2/index|25. ROS 2]]에 있다. 이 페이지의 도구가 충족하려는 실험 기준 — 분석 단위, 비교, 불확실성, 산출물 체크리스트 — 은 [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]]다.

### 출처

- ROS 2 Jazzy 문서 — Tutorials: Recording and playing back data; Using `ros2doctor` to identify issues; Using `rqt_console` to view logs; Debugging tf2 problems.
- ROS 2 Jazzy 문서 — Tutorials, Testing: Why automatic tests?; Running tests from the command line; Writing basic tests with Python; Writing basic tests with C++ with GTest; Writing basic integration tests with `launch_testing`.
- ROS 2 Jazzy 문서 — Concepts: Logging and logger configuration(심각도, 출력 대상, `ROS_LOG_DIR`/`ROS_HOME`, 노드 옵션); Overview and usage of RQt.
- ROS 2 Jazzy 문서 — Tutorials: RViz user guide(display status, fixed frame); Logging and logger configuration 데모(로거 서비스).
- ROS 2 Jazzy 문서 — How-to guides: rosbag2 Overriding QoS policies for recording and playback; Run 2 nodes in single or separate Docker containers.
- 인용한 모든 플래그의 출처, Jazzy 브랜치 소스: `ros2cli`(`ros2doctor/command/doctor.py`, `ros2node/verb/info.py`, `ros2param/verb/dump.py`, `ros2topic/verb/{hz,bw,delay}.py`); `rosbag2`(`ros2bag/verb/{record,play,info}.py`, 저장 플러그인과 기본값 `mcap`에 관한 저장소 README).
- ROS 2 design article — Clock and Time(`/clock`, `use_sim_time`, 초기화 안 됨을 뜻하는 시간 0).

> [!question]- 스스로 점검 · 정답
> **1. 노드가 출력을 내지 않는다. 퍼블리셔는 확실히 멀쩡하다. 무엇부터 점검하고, 왜 짐작한 지점부터 보지 않는가?** 0번, 셸의 환경부터 시작해 목록을 순서대로 내려간다. 순서의 요점은 바로 그 확신이 틀렸다는 것이다. 확신하는 항목이 건너뛰는 항목이고, 그다음 한 시간을 거기서 잃는다. `ros2 node list`, `ros2 node info`, `ros2 topic hz`, `ros2 topic info`, QoS는 `--verbose`, `tf2_echo`, `/clock`. 처음 실패에서 멈춘다.
> **2. `ros2 topic hz /scan`은 30 Hz로 멀쩡한데 `ros2 topic delay /scan`은 1초에 1초씩 늘어난다. 무슨 일이고, 왜 `hz`는 못 보는가?** 상류 어딘가가 뒤처져 출력이 큐에 쌓이고 있다. 메시지는 제 주기로 오지만 하나하나가 앞의 것보다 오래됐다. `hz`는 도착 간격을 재고, 일정한 적체는 그 간격을 바꾸지 않는다. header 스탬프와 수신 시각을 비교하는 `delay`만 쌓이는 나이를 본다. 유계한 지연은 지연이고, 자라는 지연은 결국 잃게 될 큐다.
> **3. 연구용 녹화에서 `ros2 bag record -a`가 나쁜 기본값인 이유를 디스크 용량 말고 대라.** 기록기가 구독한 모든 것을 직렬화해서 써야 하고, 따라가지 못하면 메시지를 흘리기 때문이다. 그래서 정작 필요한 토픽이 불완전한 채로 돌아오고 에러는 없다. 알게 되는 곳은 `ros2 bag info`의 Count 열이고 보통 이미 늦었다. 400 GB짜리 bag은 공유도, CI 투입도, 반복도 불가능하다.
> **4. bag이 `--clock`으로 재생되고 `ros2 bag info`는 수천 개의 메시지를 보여 주는데 노드는 아무것도 내지 않는다. 흔한 원인 둘과 그것을 가르는 명령 하나를 대라.** 시계(노드가 `use_sim_time`이 아니거나, `use_sim_time`인데 `/clock`을 발행하는 것이 없음)와 QoS durability/reliability(구독자가 플레이어의 제공보다 많이 요구해 연결이 성립하지 않음). 재생 중의 `ros2 topic hz /scan`이 가른다. 주기가 보고되면 데이터는 선로 위에 있고 문제는 시간이다. 아무것도 안 나오면 문제는 연결이니 `ros2 node info`로 이름을, 그다음 `ros2 topic info /scan --verbose`로 프로파일을 비교한다.
