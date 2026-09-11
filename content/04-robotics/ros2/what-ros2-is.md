---
title: "25.1 What ROS 2 Is, and Your First Running System"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Install ROS 2 Jazzy on Ubuntu 24.04, run a two-node system, and read its computation graph with the command-line tools instead of guessing at it."
mastery-when: "Go deeper when the middleware itself — discovery, transport, security — is what you are modifying, rather than something you are using."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to get a ROS 2 system running and to see what it is doing. Not enough to modify the middleware.
> **Working** — ROS 2 시스템을 띄우고 그것이 무엇을 하고 있는지 볼 정도. 미들웨어 자체를 고칠 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> A working Ubuntu 24.04 machine (or VM), comfort with a shell, and Python. No prior ROS of any version is assumed. Everything that runs here is the baseline for the rest of this track: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, paired with Gazebo Harmonic when simulation arrives in [[04-robotics/ros2/index|25. ROS 2]].
> Ubuntu 24.04 머신(또는 VM), 셸 사용 경험, Python. ROS 경험은 전제하지 않는다. 이 트랙 전체의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**이고, 시뮬레이션이 등장할 때는 Gazebo Harmonic과 짝을 이룬다.

### 1. The problem a robot middleware solves

A robot is not one program. A camera driver reads frames at 30 Hz. A motor controller wants a command every few milliseconds. A planner thinks for half a second at a time. A logger writes to disk. A user interface runs on a laptop that is not the robot.

Write that as one process and three things go wrong. The camera driver crash takes the planner with it. Changing the planner means rebuilding and restarting everything, including the motor loop that was holding the arm up. And moving the interface onto the operator's laptop means inventing a network protocol.

So you split it into processes. Now you have four new problems:

1. **Data exchange.** Processes must pass structured data — images, transforms, velocity commands — across process and machine boundaries, at rates from 1 Hz to 1 kHz.
2. **Discovery.** The planner must find the camera driver without being told its IP address and port, because the camera driver may start after it, on a different machine, with a different port each time.
3. **Independent restart.** Killing and restarting one process must not require restarting the others, and the survivors must notice and reconnect.
4. **A common type language.** Two teams writing two nodes must agree on what "a pose" is, in a way a compiler can check.

A robot middleware is the layer that solves those four. ROS 2 is one such middleware, and the most widely used one in research robotics.

### 2. What ROS 2 is not

Three misreadings cost beginners weeks.

- **It is not an operating system.** The name is historical. ROS 2 runs *on* Linux (Ubuntu 24.04 for Jazzy); it is a set of libraries, message definitions, build tooling and command-line tools.
- **It is not a framework you must write your whole robot inside.** A ROS 2 node is an ordinary process that links a library. Your perception code, your solver, your learned policy can be plain Python or C++ with a thin ROS 2 edge that publishes and subscribes. Keeping that edge thin is good practice: it is what lets you unit-test the algorithm without a running graph.
- **It is not a real-time system by itself.** Nothing about installing ROS 2 gives you deadline guarantees. The official position is that ROS 2 is *designed with* real-time constraints in mind; achieving hard real time additionally requires an RT kernel (for example RT_PREEMPT), avoiding nondeterministic operations such as dynamic allocation and unbounded blocking in the execution path, and a middleware configuration that supports it. The ROS 2 real-time demo is documented as needing a source build against a static DDS API. Treat "ROS 2 is real-time" as a claim that needs its conditions stated, not a property you get from `apt install`.

### 3. The computation graph

The central idea, and the thing you will spend the rest of this track reasoning about:

- A **node** is a participating process (more precisely, a participating unit — one process can host several).
- Nodes exchange data over named **topics** (asynchronous streams), **services** (request–response), and **actions** (long-running goals with feedback).
- **Parameters** configure a node at startup and at runtime.
- The **graph** is the live set of nodes and their connections. It is not written down anywhere. It is discovered at runtime, and it changes as nodes come and go.

The practical consequence: *you debug a ROS 2 system by interrogating the running graph*, not by reading source. Section 9 is the set of commands that does the interrogating, and it is the most durable thing on this page.

### 4. Why ROS 2 exists, given ROS 1

ROS 1 worked, and much of the robotics literature you will read ran on it. ROS 2 is a rewrite, not a version bump, for reasons that are all visible in the architecture:

- **Multi-robot systems.** ROS 1 discovery runs through a central `roscore` master. One master is a single point of failure and an awkward fit for fleets. ROS 2 uses distributed discovery with no master: nodes advertise themselves to the network and respond to each other's advertisements, and they announce when they go offline.
- **Security.** ROS 1 had no authentication, encryption, or access control on the wire. ROS 2 inherits the DDS security plugins — encryption in transit, authentication of participants, data integrity, and domain-wide access control — configured per *security enclave*.
- **Embedded and small platforms.** ROS 2's layered design (client library → `rcl` → `rmw` → middleware) was built so that constrained targets and microcontroller-oriented middleware variants are reachable, rather than assuming a full desktop Linux.
- **Real-time intent.** The official documentation states plainly that real-time performance was not considered in ROS 1's early stages and that retrofitting it is intractable; ROS 2 was prototyped with those constraints in mind from the start.

And the decisive practical fact: **ROS 1 is over.** Noetic Ninjemys, the final ROS 1 distribution, reached end of life on 31 May 2025. New work starts on ROS 2. When you read a 2016–2021 paper whose code is ROS 1, you are reading an archive.

Which ROS 2, then. Jazzy Jalisco (May 2024) is supported until May 2029 and is the baseline here. Lyrical Luth (May 2026) is the newer LTS, supported to May 2031, and pairs with Gazebo Jetty — the right target for a project starting fresh with no dependency constraints. Kilted Kaiju is a non-LTS release that ends in December 2026, so do not choose it now.

### 5. DDS underneath: what it buys and what it costs

ROS 2 does not implement its own wire protocol. It sits on **DDS** (Data Distribution Service), an OMG industry standard, using the DDSI-RTPS wire protocol. The ROS layer that adapts to a specific DDS product is the `rmw` (ROS middleware) interface, and several are supported: `rmw_fastrtps_cpp` (eProsima Fast DDS — the default, packaged with binary releases), `rmw_cyclonedds_cpp` (Eclipse Cyclone DDS, also packaged), `rmw_connextdds` (RTI Connext, commercial, installed separately), and `rmw_gurumdds_cpp` (community support).

What that buys:

- Distributed discovery with no master.
- Per-connection **Quality of Service** policies — reliability, history depth, durability, deadline, liveliness — so a lossy 30 Hz camera stream and a must-not-drop command channel can have different delivery semantics on the same system.
- Security plugins that come from the standard rather than from ROS.
- A vendor choice, so no single implementation is a dependency of the project.

What it costs:

- **QoS is now a way to fail.** Two nodes connect only if their QoS settings are compatible. A mismatch produces a publisher and a subscriber that both look healthy and never exchange a message. This is the single most common "it's just silent" bug in ROS 2, and [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] is where it is dissected.
- **Discovery traffic scales with participants**, and on a shared lab network you can see other people's graphs. `ROS_DOMAIN_ID` partitions this: set `export ROS_DOMAIN_ID=<integer>` and you only see nodes on the same domain.
- **Configuration moves outside ROS.** Tuning buffer sizes or multicast behaviour means reading DDS vendor documentation, not ROS documentation.

### 6. Installing ROS 2 Jazzy on Ubuntu 24.04

Jazzy debs target Ubuntu Noble (24.04). Follow the official page rather than trusting a blog post; what follows is that page's sequence, with the reason for each step.

First, a UTF-8 locale — minimal images and containers often have `POSIX`, which breaks tooling:

```bash
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Then enable the Ubuntu Universe repository and add the ROS 2 apt source. Jazzy's current instructions install a `ros2-apt-source` *package* that carries the key and the source list, so repository configuration updates itself later:

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

Then the distribution itself. `desktop` includes RViz, the demos and the tutorials; `ros-base` is the same communication layer without GUI tools, which is what goes on a robot:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop
sudo apt install ros-dev-tools    # colcon, rosdep, build tooling — needed from 25.4 onward
```

> [!warning] A documented Ubuntu 24.04 trap
> On some 24.04 installs the apt sources list only the base `noble` suite, and installing `ros-dev-tools` then fails on dependency conflicts. Check with `grep Suites /etc/apt/sources.list.d/ubuntu.sources`; if `noble-updates` and `noble-backports` are missing, add them to the `Suites:` line and run `sudo apt clean && sudo apt update && sudo apt full-upgrade -y`.

### 7. Sourcing the setup file, and why every new terminal needs it

```bash
source /opt/ros/jazzy/setup.bash
```

This is not a formality. The setup file exports `PATH` (so `ros2` resolves), `AMENT_PREFIX_PATH` and `CMAKE_PREFIX_PATH` (so packages are findable), `LD_LIBRARY_PATH` and `PYTHONPATH` (so libraries and Python modules import), and ROS-specific variables. Environment variables belong to a process and are inherited only by its children, so a shell you opened before sourcing, or a second tab, has none of them.

That design is deliberate: it is what lets two distributions, or a distribution and your own workspace, coexist on one machine and be selected per terminal. The cost is the discipline of sourcing.

You can put it in `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

Do that for a single-distribution learning machine. Do not do it reflexively on a machine where you will later layer workspaces — the overlay rules in [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]] are much easier to reason about when sourcing is explicit.

Verify the installation with the two-node demo, one node per terminal, each sourced:

```bash
# terminal 1
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

```bash
# terminal 2
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

The talker says `Publishing`, the listener says `I heard`. A C++ node and a Python node just exchanged typed data over a discovered connection with no configuration. That is the whole value proposition in one screen.

### 8. Your first running system: turtlesim and teleop

Turtlesim is a toy 2D simulator whose only purpose is to be a real ROS 2 graph small enough to hold in your head.

```bash
sudo apt install ros-jazzy-turtlesim ros-jazzy-rqt ros-jazzy-rqt-common-plugins
ros2 pkg executables turtlesim
```

The last command lists the package's executables — `draw_square`, `mimic`, `turtle_teleop_key`, `turtlesim_node` — and is a quick check that the package is installed and visible.

```bash
# terminal 1 (sourced)
ros2 run turtlesim turtlesim_node
```

```bash
# terminal 2 (sourced)
ros2 run turtlesim turtle_teleop_key
```

`ros2 run <package> <executable>` is the primitive: start one executable from one installed package. Put the cursor in terminal 2 and press the arrow keys; the turtle moves and draws. Note that each press produces a short motion, not continuous travel — deliberately, because a robot that keeps executing the last command after the operator's link drops is a hazard.

### 9. Reading the graph

Everything below runs in a third sourced terminal while the first two keep running. This is the actual skill on this page.

```bash
ros2 node list
```

```text
/turtlesim
/teleop_turtle
```

Two nodes. Note that the node names are not the executable names — a node names itself, and can be renamed at launch. Ask what one node is connected to:

```bash
ros2 node info /turtlesim
```

That prints its subscribers, publishers, service servers, service clients, action servers and action clients: the node's entire surface in the graph.

```bash
ros2 topic list -t
```

```text
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim/msg/Color]
/turtle1/pose [turtlesim/msg/Pose]
```

`-t` appends the message type, which you almost always want. `/parameter_events` and `/rosout` are infrastructure topics present in every ROS 2 system; the three under `/turtle1/` are this robot's.

```bash
ros2 topic echo /turtle1/cmd_vel
```

Nothing appears until you drive. Then, per arrow-key press:

```text
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

`echo` creates a temporary subscriber, so it is not a passive tap — it joins the graph, and you will see it there.

```bash
ros2 topic info /turtle1/cmd_vel
```

```text
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 2
```

One publisher (teleop), two subscribers (turtlesim, and your `echo`). Add `--verbose` and you additionally get, per endpoint, the node name and namespace, the type hash, and the full QoS profile — reliability, history and depth, durability, lifespan, deadline, liveliness. Learn that this flag exists now; in 25.5 it is the command that diagnoses a QoS mismatch.

```bash
ros2 interface show geometry_msgs/msg/Twist
```

```text
# This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
            float64 x
            float64 y
            float64 z
    Vector3  angular
            float64 x
            float64 y
            float64 z
```

This is the contract. `Twist` is a general-purpose velocity in a frame: a real differential-drive robot uses `linear.x` and `angular.z` exactly as the turtle does, which is why this toy transfers.

Finally, the picture:

```bash
ros2 run rqt_graph rqt_graph
```

Nodes as ellipses, topics as the arrows between them. Uncheck **Debug** to see the nodes created by your own `echo` and `pub` commands. Everything rqt_graph shows is available from the command line; its value is that a wrong connection is visible in a glance where it is a paragraph of text in `ros2 topic info`.

### 10. Exercise: drive the turtle and read the traffic it produces

One sitting. Four terminals, all sourced.

1. Run `turtlesim_node` and `turtle_teleop_key`.
2. In terminal 3: `ros2 topic echo /turtle1/cmd_vel`. Drive with the arrow keys and watch the values. Convince yourself which field changes for a forward press and which for a turn.
3. In terminal 4: `ros2 topic hz /turtle1/pose`. Turtlesim publishes pose continuously; the command reports the rate it is receiving. Now run `ros2 topic hz /turtle1/cmd_vel` instead and drive. Commands are event-driven, so the rate is whatever your fingers produce. *The two topics in this one system have completely different temporal characters, and nothing in the type tells you that.*
4. Drive without touching teleop:

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

The turtle circles. You replaced a driver with a command line, because the subscriber never knew who was publishing.

5. Open `rqt_graph`, uncheck **Debug**, and find your `topic pub` and `topic echo` nodes in the picture.
6. Stop turtlesim with Ctrl+C while `echo` and `hz` keep running. They do not crash; they go quiet. Restart turtlesim and they resume. That is item 3 of section 1, demonstrated.

You are done when you can state, without looking: which node publishes `/turtle1/pose`, what type it carries, and roughly at what rate.

### 11. The failure to diagnose: a terminal that was not sourced

This will happen to you, probably today, and it is worth doing on purpose once.

Open a new terminal and, without sourcing, run:

```bash
ros2 topic list
```

```text
ros2: command not found
```

That symptom is unambiguous — `PATH` has no ROS 2 — and the fix is `source /opt/ros/jazzy/setup.bash`.

The nastier variant is the *partially* wrong environment, and it is worth recognising the shapes:

| Symptom | Likely cause | Command that finds it |
|---|---|---|
| `ros2: command not found` | setup file never sourced in this shell | `echo $AMENT_PREFIX_PATH` — empty |
| `ros2` works, `ros2 node list` is empty while nodes run | different `ROS_DOMAIN_ID` in the two shells | `echo $ROS_DOMAIN_ID` in both |
| `Package 'turtlesim' not found` | package not installed, or a workspace overlay sourced without the underlay | `ros2 pkg executables turtlesim`, then `ros2 pkg prefix turtlesim` |
| Your rebuilt node runs the old code | workspace `install/setup.bash` not re-sourced after the build | `ros2 pkg prefix <pkg>` — points at `/opt/ros/jazzy` rather than your workspace |

The habit worth forming: when a ROS 2 system behaves impossibly, check the environment of the shell that is behaving impossibly *before* you read any source code. `printenv | grep -i ros` takes two seconds and settles it. The overlay cases in rows three and four are the subject of [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]].

### 12. What this page does not cover

Writing nodes of your own is [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]. Request–response, long-running goals, configuration and managed startup are [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. Building and installing your own packages, and starting many nodes at once, are [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]. The QoS settings printed by `ros2 topic info --verbose`, the executor that decides which callback runs, and simulated versus wall time are [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. Simulation, navigation, manipulation and hardware interfaces sit above all of this in [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Installation: Ubuntu (deb packages); Configuring your ROS 2 environment; Using turtlesim, ros2 and rqt; Understanding nodes; Understanding topics.
- ROS 2 Jazzy documentation — Concepts: Discovery; Different ROS 2 middleware vendors; ROS 2 Security; Understanding real-time programming.
- ROS 2 Jazzy documentation — Releases (distribution and EOL table).
- Open Robotics, "ROS Noetic End-of-Life: May 31, 2025" (ROS Discourse announcement).
- Gazebo documentation — ROS installation / ROS 2 and Gazebo version pairings.

> [!question]- Self-check · Answer
> **1. Your colleague says "we don't need ROS 2, it's just message passing — we'll use a socket." What are they underestimating?** Discovery without configuration, a checked type system shared across languages and teams, per-connection delivery semantics (QoS), and a live introspection surface. The socket is the easy quarter of the problem; the rest is what you would end up rewriting badly.
> **2. `ros2 topic info /turtle1/cmd_vel` reports one publisher and two subscribers, but you only started turtlesim and teleop. Who is the second subscriber?** Your own `ros2 topic echo`. CLI introspection tools join the graph as real nodes; that is why they appear in `rqt_graph` under **Debug**.
> **3. Why does a second terminal need `source /opt/ros/jazzy/setup.bash` when the first one already ran it?** Environment variables live in a process and are inherited only by children. The setup file sets `PATH`, `AMENT_PREFIX_PATH`, `LD_LIBRARY_PATH` and `PYTHONPATH` in the shell that runs it and nowhere else. The upside of that design is that different terminals can run different distributions or workspaces.
> **4. Someone claims ROS 2 is a real-time system. What do you ask them?** Which kernel, which middleware and configuration, and which operations were removed from the execution path. Installing ROS 2 from apt gives no deadline guarantees; the official position is that ROS 2 was *designed with* real-time constraints in mind, and the real-time demo itself is documented as requiring a source build against a static DDS API.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — ROS 2 시스템을 실행하고 그 동작을 관찰할 정도. 미들웨어 자체를 수정할 정도는 아니다.
> **Working** — enough to run a ROS 2 system and see what it does, not to modify the middleware.

> [!note] 선수 지식 · Prerequisites
> 동작하는 Ubuntu 24.04 머신(또는 VM), 셸, Python. ROS 경험은 필요 없다. 이 트랙의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**이고, 시뮬레이션 단계에서는 Gazebo Harmonic과 짝을 이룬다([[04-robotics/ros2/index|25. ROS 2]]).
> A working Ubuntu 24.04 machine, a shell, and Python; no prior ROS assumed.

### 1. 로봇 미들웨어가 푸는 문제

로봇은 프로그램 하나가 아니다. 카메라 드라이버는 30 Hz로 프레임을 읽고, 모터 제어기는 수 밀리초마다 명령을 원하고, 플래너는 한 번에 0.5초씩 생각하고, 로거는 디스크에 쓰고, 사용자 인터페이스는 로봇이 아닌 노트북에서 돈다.

이걸 한 프로세스로 짜면 세 가지가 깨진다. 카메라 드라이버가 죽으면 플래너도 같이 죽는다. 플래너를 바꾸려면 팔을 들고 있던 모터 루프까지 전부 재시작해야 한다. 인터페이스를 조작자 노트북으로 옮기려면 네트워크 프로토콜을 직접 발명해야 한다.

그래서 프로세스로 쪼갠다. 그러면 새 문제 네 개가 생긴다.

1. **데이터 교환** — 이미지, 변환, 속도 명령 같은 구조화된 데이터를 프로세스와 머신 경계를 넘어 1 Hz에서 1 kHz까지의 속도로 주고받아야 한다.
2. **탐색(discovery)** — 플래너는 카메라 드라이버의 IP와 포트를 듣지 않고도 그것을 찾아야 한다. 드라이버는 나중에, 다른 머신에서, 매번 다른 포트로 뜰 수 있다.
3. **독립적인 재시작** — 한 프로세스를 죽였다 살리는 데 다른 프로세스를 재시작해야 해서는 안 되고, 살아남은 쪽이 알아서 다시 연결해야 한다.
4. **공통 타입 언어** — 두 팀이 "자세(pose)"가 무엇인지 컴파일러가 검사할 수 있는 형태로 합의해야 한다.

로봇 미들웨어는 이 넷을 푸는 계층이다. ROS 2가 그런 미들웨어이고, 연구 로보틱스에서 가장 널리 쓰인다.

### 2. ROS 2가 아닌 것

초심자가 몇 주를 잃는 오해 세 가지.

- **운영체제가 아니다.** 이름은 역사적 유물이다. ROS 2는 Linux 위에서 돈다(Jazzy는 Ubuntu 24.04). 라이브러리, 메시지 정의, 빌드 도구, 커맨드라인 도구의 묶음이다.
- **로봇 전체를 그 안에 작성해야 하는 프레임워크가 아니다.** ROS 2 노드는 라이브러리를 링크한 평범한 프로세스다. 인식 코드, 솔버, 학습된 정책은 평범한 Python이나 C++로 두고, publish/subscribe 하는 얇은 ROS 2 경계만 붙이면 된다. 그 경계를 얇게 유지하는 것이 좋은 습관이다. 그래야 그래프를 띄우지 않고 알고리즘을 단위 테스트할 수 있다.
- **그 자체로 실시간 시스템이 아니다.** ROS 2를 설치한다고 마감 시한 보장이 생기지는 않는다. 공식 문서의 입장은 ROS 2가 실시간 제약을 *염두에 두고 설계되었다*는 것이다. 경성 실시간을 얻으려면 RT 커널(예: RT_PREEMPT), 실행 경로에서 동적 할당과 무한 블로킹 같은 비결정적 연산 제거, 그리고 그것을 지원하는 미들웨어 구성이 함께 필요하다. 공식 실시간 데모 자체가 정적 DDS API에 대한 소스 빌드를 요구한다고 문서화되어 있다. "ROS 2는 실시간"이라는 말은 조건을 명시해야 하는 주장이지 `apt install`로 얻는 성질이 아니다.

### 3. 계산 그래프(computation graph)

이 트랙 내내 다룰 중심 개념이다.

- **노드(node)** 는 참여 프로세스다(정확히는 참여 단위 — 한 프로세스가 여러 노드를 담을 수 있다).
- 노드들은 이름 붙은 **토픽**(비동기 스트림), **서비스**(요청–응답), **액션**(피드백을 주는 장시간 목표)으로 데이터를 주고받는다.
- **파라미터**는 시작 시점과 실행 중에 노드를 설정한다.
- **그래프**는 살아 있는 노드와 연결의 집합이다. 어디에도 적혀 있지 않고, 런타임에 탐색되며, 노드가 뜨고 지면 바뀐다.

실무적 귀결: *ROS 2 시스템은 소스를 읽어서가 아니라 돌아가는 그래프를 심문해서 디버깅한다.* 9절이 그 심문 명령들이고, 이 페이지에서 가장 오래 쓸 내용이다.

### 4. ROS 1이 있는데 ROS 2가 존재하는 이유

ROS 1은 잘 돌아갔고, 당신이 읽을 로보틱스 문헌의 상당수가 그 위에서 실행됐다. ROS 2는 버전 업이 아니라 재작성이며, 이유는 모두 구조에 드러난다.

- **다중 로봇.** ROS 1의 탐색은 중앙 `roscore` 마스터를 거친다. 마스터 하나는 단일 장애점이고 군집에 어울리지 않는다. ROS 2는 마스터 없는 분산 탐색을 쓴다. 노드가 네트워크에 자신을 알리고 서로의 광고에 응답하며, 종료할 때도 알린다.
- **보안.** ROS 1에는 전송 구간의 인증·암호화·접근 제어가 없었다. ROS 2는 DDS 보안 플러그인을 물려받는다 — 전송 암호화, 참여자 인증, 무결성, 도메인 전역 접근 제어. 설정 단위는 *security enclave*다.
- **임베디드·소형 플랫폼.** 계층 설계(클라이언트 라이브러리 → `rcl` → `rmw` → 미들웨어)는 데스크톱 Linux를 전제하지 않고 제약된 대상에 닿을 수 있도록 만들어졌다.
- **실시간 의도.** 공식 문서는 ROS 1 초기 설계에서 실시간이 고려되지 않았고 이제 와서 개조하는 것은 불가능에 가깝다고 분명히 적는다. ROS 2는 그 제약을 처음부터 염두에 두고 시제품화됐다.

그리고 결정적인 실무 사실: **ROS 1은 끝났다.** 마지막 ROS 1 배포판 Noetic Ninjemys는 2025년 5월 31일 지원이 종료됐다. 새 작업은 ROS 2에서 시작한다. 코드가 ROS 1인 2016–2021년 논문을 읽는다면 그것은 아카이브를 읽는 것이다.

그러면 어떤 ROS 2인가. Jazzy Jalisco(2024년 5월)는 2029년 5월까지 지원되며 여기의 기준이다. Lyrical Luth(2026년 5월)는 더 새로운 LTS로 2031년 5월까지 지원되고 Gazebo Jetty와 짝을 이룬다 — 의존성 제약이 없는 새 프로젝트라면 이쪽이 맞다. Kilted Kaiju는 비LTS이고 2026년 12월에 끝나므로 지금 고르면 안 된다.

### 5. 아래에 깔린 DDS: 무엇을 사고 무엇을 치르는가

ROS 2는 자체 와이어 프로토콜을 구현하지 않는다. OMG 산업 표준인 **DDS**(Data Distribution Service) 위에, DDSI-RTPS 와이어 프로토콜로 올라탄다. 특정 DDS 제품에 맞추는 계층이 `rmw`(ROS middleware) 인터페이스이고, 여럿이 지원된다: `rmw_fastrtps_cpp`(eProsima Fast DDS — 기본값, 바이너리 배포에 포함), `rmw_cyclonedds_cpp`(Eclipse Cyclone DDS, 역시 포함), `rmw_connextdds`(RTI Connext, 상용, 별도 설치), `rmw_gurumdds_cpp`(커뮤니티 지원).

사는 것:

- 마스터 없는 분산 탐색.
- 연결 단위의 **QoS** 정책 — reliability, history depth, durability, deadline, liveliness. 손실을 감수하는 30 Hz 카메라 스트림과 떨어뜨리면 안 되는 명령 채널이 같은 시스템에서 다른 전달 의미를 가질 수 있다.
- ROS가 아니라 표준에서 오는 보안 플러그인.
- 벤더 선택권 — 특정 구현이 프로젝트의 의존성이 되지 않는다.

치르는 것:

- **QoS가 새로운 실패 경로다.** 두 노드는 QoS가 호환될 때만 연결된다. 불일치하면 퍼블리셔와 서브스크라이버가 둘 다 멀쩡해 보이면서 메시지를 한 개도 주고받지 않는다. ROS 2에서 가장 흔한 "그냥 조용한" 버그이고, [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]에서 해부한다.
- **탐색 트래픽이 참여자 수에 따라 늘고**, 공용 실험실 네트워크에서는 남의 그래프가 보인다. `ROS_DOMAIN_ID`가 이를 나눈다. `export ROS_DOMAIN_ID=<정수>`를 하면 같은 도메인의 노드만 보인다.
- **설정이 ROS 바깥으로 나간다.** 버퍼 크기나 멀티캐스트 동작을 조정하려면 ROS 문서가 아니라 DDS 벤더 문서를 읽어야 한다.

### 6. Ubuntu 24.04에 ROS 2 Jazzy 설치

Jazzy deb은 Ubuntu Noble(24.04)을 대상으로 한다. 블로그 글 대신 공식 문서를 따르라. 아래는 그 문서의 순서에 각 단계의 이유를 붙인 것이다.

먼저 UTF-8 로케일. 최소 이미지나 컨테이너는 `POSIX`인 경우가 많고 그러면 도구가 깨진다.

```bash
locale  # check for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

다음으로 Universe 저장소를 켜고 ROS 2 apt 소스를 추가한다. 현재 Jazzy 지침은 키와 소스 목록을 담은 `ros2-apt-source` *패키지*를 설치하게 한다. 그래서 저장소 설정이 이후 자동으로 갱신된다.

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

그리고 배포판 본체. `desktop`은 RViz와 데모, 튜토리얼을 포함하고, `ros-base`는 GUI 도구 없는 같은 통신 계층으로 로봇에 올리는 쪽이다.

```bash
sudo apt update
sudo apt install ros-jazzy-desktop
sudo apt install ros-dev-tools    # colcon, rosdep 등 — 25.4부터 필요
```

> [!warning] 문서화된 Ubuntu 24.04 함정
> 일부 24.04 설치는 apt 소스에 기본 `noble` suite만 들어 있고, 그러면 `ros-dev-tools` 설치가 의존성 충돌로 실패한다. `grep Suites /etc/apt/sources.list.d/ubuntu.sources`로 확인하고, `noble-updates`와 `noble-backports`가 없으면 `Suites:` 줄에 추가한 뒤 `sudo apt clean && sudo apt update && sudo apt full-upgrade -y`를 실행한다.

### 7. setup 파일 source, 그리고 새 터미널마다 필요한 이유

```bash
source /opt/ros/jazzy/setup.bash
```

형식적인 절차가 아니다. 이 파일은 `PATH`(그래야 `ros2`가 잡힌다), `AMENT_PREFIX_PATH`와 `CMAKE_PREFIX_PATH`(패키지 탐색), `LD_LIBRARY_PATH`와 `PYTHONPATH`(라이브러리와 Python 모듈 import), 그리고 ROS 전용 변수를 내보낸다. 환경 변수는 프로세스에 속하고 자식에게만 상속되므로, source 전에 열어 둔 셸이나 두 번째 탭에는 아무것도 없다.

이 설계는 의도된 것이다. 배포판 두 개, 또는 배포판과 내 워크스페이스가 한 머신에 공존하고 터미널마다 선택되게 하는 장치다. 대가는 source하는 규율이다.

`~/.bashrc`에 넣을 수 있다.

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

배포판 하나만 쓰는 학습용 머신이라면 그렇게 하라. 나중에 워크스페이스를 겹쳐 쓸 머신에서는 반사적으로 하지 마라. [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]의 오버레이 규칙은 source가 명시적일 때 훨씬 추론하기 쉽다.

설치 확인은 두 노드 데모로 한다. 터미널마다 source한다.

```bash
# terminal 1
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

```bash
# terminal 2
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

talker는 `Publishing`, listener는 `I heard`를 찍는다. C++ 노드와 Python 노드가 설정 없이 탐색된 연결 위로 타입 있는 데이터를 주고받았다. 한 화면에 담긴 ROS 2의 가치 제안 전부다.

### 8. 첫 실행 시스템: turtlesim과 teleop

turtlesim은 장난감 2D 시뮬레이터이고, 존재 이유는 머릿속에 담길 만큼 작은 진짜 ROS 2 그래프라는 것이다.

```bash
sudo apt install ros-jazzy-turtlesim ros-jazzy-rqt ros-jazzy-rqt-common-plugins
ros2 pkg executables turtlesim
```

마지막 명령은 패키지의 실행 파일 — `draw_square`, `mimic`, `turtle_teleop_key`, `turtlesim_node` — 을 나열하며, 패키지가 설치되어 보이는지 빠르게 확인해 준다.

```bash
# terminal 1 (sourced)
ros2 run turtlesim turtlesim_node
```

```bash
# terminal 2 (sourced)
ros2 run turtlesim turtle_teleop_key
```

`ros2 run <package> <executable>`이 기본 단위다. 설치된 패키지 하나에서 실행 파일 하나를 띄운다. 터미널 2에 커서를 두고 화살표 키를 누르면 거북이가 움직이며 선을 그린다. 한 번 누르면 짧게 움직이고 멈춘다는 점을 보라. 의도된 설계다. 조작자와의 링크가 끊긴 뒤에도 마지막 명령을 계속 수행하는 로봇은 위험 요소다.

### 9. 그래프 읽기

아래는 앞의 두 터미널을 살려 둔 채 source된 세 번째 터미널에서 실행한다. 이 페이지의 실제 기술이다.

```bash
ros2 node list
```

```text
/turtlesim
/teleop_turtle
```

노드 둘. 노드 이름은 실행 파일 이름이 아니다. 노드가 스스로 이름을 정하고, 실행 시 바꿀 수 있다. 한 노드가 무엇과 연결되어 있는지 묻는다.

```bash
ros2 node info /turtlesim
```

서브스크라이버, 퍼블리셔, 서비스 서버/클라이언트, 액션 서버/클라이언트 — 그래프 안에서 그 노드가 가진 표면 전부를 찍는다.

```bash
ros2 topic list -t
```

```text
/parameter_events [rcl_interfaces/msg/ParameterEvent]
/rosout [rcl_interfaces/msg/Log]
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim/msg/Color]
/turtle1/pose [turtlesim/msg/Pose]
```

`-t`는 메시지 타입을 붙인다. 거의 항상 필요하다. `/parameter_events`와 `/rosout`은 모든 ROS 2 시스템에 있는 기반 토픽이고, `/turtle1/` 아래 셋이 이 로봇의 것이다.

```bash
ros2 topic echo /turtle1/cmd_vel
```

운전하기 전까지는 아무것도 안 나온다. 화살표 키를 누를 때마다:

```text
linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0
---
```

`echo`는 임시 서브스크라이버를 만든다. 수동적인 관측이 아니라 그래프에 참여하는 행위이고, 그래서 그래프에 보인다.

```bash
ros2 topic info /turtle1/cmd_vel
```

```text
Type: geometry_msgs/msg/Twist
Publisher count: 1
Subscription count: 2
```

퍼블리셔 하나(teleop), 서브스크라이버 둘(turtlesim과 당신의 `echo`). `--verbose`를 붙이면 엔드포인트마다 노드 이름과 네임스페이스, 타입 해시, 그리고 전체 QoS 프로파일 — reliability, history와 depth, durability, lifespan, deadline, liveliness — 이 추가로 나온다. 이 플래그의 존재를 지금 외워 두라. 25.5에서 QoS 불일치를 진단하는 명령이 이것이다.

```bash
ros2 interface show geometry_msgs/msg/Twist
```

```text
# This expresses velocity in free space broken into its linear and angular parts.
    Vector3  linear
            float64 x
            float64 y
            float64 z
    Vector3  angular
            float64 x
            float64 y
            float64 z
```

이것이 계약이다. `Twist`는 어떤 프레임에서의 범용 속도다. 실제 차동 구동 로봇도 거북이와 똑같이 `linear.x`와 `angular.z`를 쓴다. 이 장난감이 그대로 이전되는 이유다.

마지막으로 그림.

```bash
ros2 run rqt_graph rqt_graph
```

노드는 타원, 토픽은 그 사이 화살표다. **Debug** 체크를 풀면 당신의 `echo`나 `pub` 명령이 만든 노드가 보인다. rqt_graph가 보여 주는 것은 전부 커맨드라인에서도 얻을 수 있다. 가치는 `ros2 topic info`에서는 문단인 잘못된 연결이 그림에서는 한눈에 보인다는 데 있다.

### 10. 실습: 거북이를 몰고 그 결과 트래픽을 읽어라

한 자리에서 끝난다. source된 터미널 넷.

1. `turtlesim_node`와 `turtle_teleop_key`를 띄운다.
2. 터미널 3: `ros2 topic echo /turtle1/cmd_vel`. 화살표로 몰면서 값을 본다. 전진 입력에서 어느 필드가, 회전 입력에서 어느 필드가 바뀌는지 확인한다.
3. 터미널 4: `ros2 topic hz /turtle1/pose`. turtlesim은 pose를 계속 낸다. 이 명령은 수신 측정 주기를 보고한다. 이제 `ros2 topic hz /turtle1/cmd_vel`로 바꾸고 몰아 보라. 명령은 이벤트 구동이라 주기는 당신 손가락이 만든다. *한 시스템 안의 두 토픽이 완전히 다른 시간 특성을 갖고, 타입은 그 사실을 전혀 알려 주지 않는다.*
4. teleop을 건드리지 않고 몰아 보라.

```bash
ros2 topic pub /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```

거북이가 원을 그린다. 드라이버를 커맨드라인으로 갈아 끼운 셈이다. 서브스크라이버는 누가 publish하는지 애초에 몰랐기 때문이다.

5. `rqt_graph`를 열고 **Debug** 체크를 푼 뒤 그림에서 `topic pub`과 `topic echo` 노드를 찾아라.
6. `echo`와 `hz`를 살려 둔 채 turtlesim을 Ctrl+C로 끈다. 둘은 죽지 않고 조용해진다. turtlesim을 다시 띄우면 재개된다. 1절의 세 번째 항목이 눈앞에서 증명된 것이다.

보지 않고 이렇게 말할 수 있으면 끝이다: `/turtle1/pose`를 누가 publish하는가, 타입은 무엇인가, 대략 몇 Hz인가.

### 11. 진단할 고장: source하지 않은 터미널

오늘 안에 겪게 된다. 한 번은 일부러 해 볼 값어치가 있다.

새 터미널을 열고 source 없이 실행한다.

```bash
ros2 topic list
```

```text
ros2: command not found
```

증상은 명확하다 — `PATH`에 ROS 2가 없다. 해법은 `source /opt/ros/jazzy/setup.bash`.

더 고약한 변종은 *부분적으로* 잘못된 환경이다. 모양을 알아 두라.

| 증상 | 유력한 원인 | 그것을 찾는 명령 |
|---|---|---|
| `ros2: command not found` | 이 셸에서 setup 파일을 source하지 않음 | `echo $AMENT_PREFIX_PATH` — 비어 있음 |
| `ros2`는 되는데 노드가 도는 중에도 `ros2 node list`가 빔 | 두 셸의 `ROS_DOMAIN_ID`가 다름 | 양쪽에서 `echo $ROS_DOMAIN_ID` |
| `Package 'turtlesim' not found` | 미설치, 또는 언더레이 없이 워크스페이스 오버레이만 source | `ros2 pkg executables turtlesim`, 그다음 `ros2 pkg prefix turtlesim` |
| 다시 빌드한 노드가 옛 코드로 돎 | 빌드 후 워크스페이스 `install/setup.bash`를 다시 source하지 않음 | `ros2 pkg prefix <pkg>` — 워크스페이스가 아니라 `/opt/ros/jazzy`를 가리킴 |

들일 습관: ROS 2 시스템이 불가능한 동작을 하면, 소스를 읽기 *전에* 그 불가능한 동작을 하는 셸의 환경부터 확인한다. `printenv | grep -i ros`는 2초면 끝난다. 셋째·넷째 행의 오버레이 사례는 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]의 주제다.

### 12. 이 페이지가 다루지 않는 것

직접 노드를 쓰는 것은 [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]. 요청–응답, 장시간 목표, 설정, 결정적 기동은 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. 자기 패키지를 빌드·설치하고 여러 노드를 한 번에 띄우는 것은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]. `ros2 topic info --verbose`가 찍는 QoS, 어느 콜백이 도는지 정하는 executor, 시뮬레이션 시간과 벽시계 시간은 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. 시뮬레이션, 내비게이션, 매니퓰레이션, 하드웨어 인터페이스는 그 위에 있고 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- ROS 2 Jazzy 문서 — Installation: Ubuntu (deb packages); Configuring your ROS 2 environment; Using turtlesim, ros2 and rqt; Understanding nodes; Understanding topics.
- ROS 2 Jazzy 문서 — Concepts: Discovery; Different ROS 2 middleware vendors; ROS 2 Security; Understanding real-time programming.
- ROS 2 Jazzy 문서 — Releases(배포판 및 EOL 표).
- Open Robotics, "ROS Noetic End-of-Life: May 31, 2025" (ROS Discourse 공지).
- Gazebo 문서 — ROS 설치 / ROS 2와 Gazebo 버전 짝.

> [!question]- 스스로 점검 · 정답
> **1. 동료가 "ROS 2 필요 없다, 메시지 전달일 뿐이니 소켓 쓰자"고 한다. 무엇을 과소평가한 것인가?** 설정 없는 탐색, 언어와 팀을 가로지르는 검사 가능한 타입 체계, 연결 단위 전달 의미(QoS), 살아 있는 내성(introspection) 표면. 소켓은 문제의 쉬운 4분의 1이고, 나머지는 결국 엉성하게 다시 짜게 되는 부분이다.
> **2. `ros2 topic info /turtle1/cmd_vel`이 퍼블리셔 1, 서브스크라이버 2를 보고하는데 띄운 것은 turtlesim과 teleop뿐이다. 두 번째 서브스크라이버는 누구인가?** 당신의 `ros2 topic echo`. CLI 내성 도구는 진짜 노드로서 그래프에 참여하고, 그래서 `rqt_graph`의 **Debug** 항목에 나타난다.
> **3. 첫 터미널에서 이미 했는데 두 번째 터미널도 `source /opt/ros/jazzy/setup.bash`가 필요한 이유는?** 환경 변수는 프로세스에 살고 자식에게만 상속된다. setup 파일은 실행한 그 셸에만 `PATH`, `AMENT_PREFIX_PATH`, `LD_LIBRARY_PATH`, `PYTHONPATH`를 설정한다. 그 설계의 이득은 터미널마다 다른 배포판이나 워크스페이스를 쓸 수 있다는 것이다.
> **4. 누가 ROS 2는 실시간 시스템이라고 주장한다. 무엇을 되물어야 하나?** 어떤 커널, 어떤 미들웨어와 구성, 실행 경로에서 어떤 연산을 제거했는지. apt로 설치한 ROS 2는 마감 시한을 보장하지 않는다. 공식 입장은 실시간 제약을 *염두에 두고 설계했다*는 것이고, 실시간 데모 자체가 정적 DDS API에 대한 소스 빌드를 요구한다고 문서화되어 있다.
