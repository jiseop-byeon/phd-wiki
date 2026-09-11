---
title: "25.5 QoS, Executors and Time"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Diagnose the three ROS 2 failures that produce no error — an incompatible QoS pair, a callback that blocks its own executor, and a node reading the wrong clock — and fix each with a command or a two-line change."
mastery-when: "Go deeper when you are doing response-time analysis of a control chain, or writing a custom executor, rather than making an ordinary node behave."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to recognise all three silent failures in a running system and fix them. Not enough to do formal timing analysis of an executor.
> **Working** — 돌아가는 시스템에서 세 가지 조용한 실패를 알아보고 고칠 정도. Executor의 형식적 타이밍 분석을 할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]] and [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]] — you should have written a publisher, a subscriber and a service client. Everything here runs on **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, the baseline of [[04-robotics/ros2/index|25. ROS 2]]; no workspace is needed, the exercises run from the command line and from plain Python files.
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]]와 [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]] — 퍼블리셔, 서브스크라이버, 서비스 클라이언트를 한 번씩 써 봤다고 가정한다. 기준 환경은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**이고, 워크스페이스는 필요 없다. 실습은 커맨드라인과 평범한 Python 파일로 돌아간다.

### 1. Why this page exists

Most ROS 2 problems announce themselves. A wrong topic name gives you an empty `ros2 topic echo`. A missing package gives you an error. A type mismatch refuses to build.

Three mechanisms do not announce themselves, and they are the three on this page:

- **QoS.** A publisher and a subscriber on the same topic with the same type do not connect, because their delivery policies are incompatible. Both processes are healthy. Both appear in `ros2 node list`. No message is ever exchanged.
- **Executors.** A callback blocks waiting for something that can only be produced by another callback that the same executor thread is supposed to run. The node stops responding. It does not crash, it does not log, and its publishers stay advertised.
- **Time.** A node reads the wall clock while the rest of the system is running on simulated or replayed time. Its timestamps are consistent with nothing, its timeouts fire at the wrong moments, and every value it produces looks plausible.

The shared symptom is "nothing happens". The shared cure is knowing that these three exist and having one command each.

### 2. The QoS policies

A QoS *profile* is a set of *policies*, applied independently to each publisher, subscription, service server and client. The base profile carries:

| Policy | Values | What it controls |
|---|---|---|
| History | *Keep last* (store up to N samples) \| *Keep all* (subject to middleware resource limits) | What the middleware retains |
| Depth | queue size N | Only honoured when history is *keep last* |
| Reliability | *Best effort* \| *Reliable* | Whether delivery is retried until acknowledged |
| Durability | *Volatile* \| *Transient local* | Whether the publisher persists samples for late-joining subscriptions |
| Deadline | duration | Expected maximum time between consecutive messages on the topic |
| Lifespan | duration | After this age a message is stale; expired messages are dropped silently and never received |
| Liveliness | *Automatic* \| *Manual by topic* | How a publisher is judged to still be alive |
| Lease duration | duration | How long a publisher has to assert liveliness before it is considered lost |

Every non-duration policy also accepts *system default*, which defers to the middleware, and every duration policy accepts *default*, an unspecified duration that middleware usually treats as infinite.

Deadline, lifespan and liveliness are the three most people never set, and they are the only policies that can tell you a stream has *stopped*: a deadline gives the subscription a *requested deadline missed* event, a liveliness lease gives it a *liveliness changed* event when a publisher dies quietly. Without them, a dead sensor and a slow sensor look identical.

### 3. Compatibility: the request-versus-offered rule

This is the rule to memorise, because everything in section 4 follows from it.

> A subscription **requests** a profile: the *minimum quality* it will accept. A publisher **offers** a profile: the *maximum quality* it can provide. A connection is made only if **every** policy of the request is no more stringent than the corresponding offer.

Compatibility is per-pair and independent of who else is on the topic: one publisher can serve several subscriptions with different requested profiles, and the presence of a third node changes nothing.

*Reliability:*

| Publisher offers | Subscription requests | Compatible |
|---|---|---|
| Best effort | Best effort | Yes |
| Best effort | Reliable | **No** |
| Reliable | Best effort | Yes |
| Reliable | Reliable | Yes |

*Durability:*

| Publisher offers | Subscription requests | Compatible | Result |
|---|---|---|---|
| Volatile | Volatile | Yes | New messages only |
| Volatile | Transient local | **No** | No communication |
| Transient local | Volatile | Yes | New messages only |
| Transient local | Transient local | Yes | New and old messages |

Deadline and lease duration follow the same shape with durations: publisher *default* against a subscription that names a duration is incompatible; a publisher period *x* against a request *y* is compatible when *y ≥ x*, and incompatible when *y < x*. Liveliness: *manual by topic* offered satisfies an *automatic* request, but not the reverse.

All policies must be compatible at once. A pair with matching reliability and mismatched durability does not connect. This is new relative to ROS 1, where any publisher and subscriber with the same type on the same topic were connected, full stop.

### 4. The silent case, and the one warning you might get

The canonical case. A camera driver publishes at 30 Hz and is written sensibly: dropping a frame is better than blocking, so it offers **best effort**. You write a subscriber and do not think about QoS, so you get the default profile, which is **reliable**. Your subscription requests a quality the publisher does not offer.

The result: `ros2 node list` shows both nodes. `ros2 topic list` shows the topic. `ros2 topic info` shows one publisher and one subscription. Your callback never runs.

One correction to the folklore, because it matters when you are hunting: this failure is not *completely* invisible. Both rclcpp and rclpy register a default handler for the incompatible-QoS event, and it logs a warning once, at discovery, on the node's own logger:

```text
[WARN] [...] [my_subscriber]: New publisher discovered on topic '/image', offering incompatible QoS. No messages will be received from it. Last incompatible policy: RELIABILITY
```

The publisher side has the mirror-image warning about a subscription requesting incompatible QoS. So why does everyone still lose an afternoon to this?

- It fires **once**, at discovery, in the startup noise of a launch file with twenty nodes, as a WARN on that node's own logger.
- Registration is wrapped in a try-and-ignore for middleware that does not support the event, so its absence proves nothing.
- After that line, the steady-state failure produces no output at all. Attach to a system that has been running for an hour and the log is empty.

Treat the warning as a gift when you get it, never as the thing you rely on.

### 5. The predefined profiles, and the latched-equivalent

Choosing eight policies per endpoint is not a reasonable ask, so ROS 2 ships profiles that are known to go together:

| Profile | History (depth) | Reliability | Durability | Use it for |
|---|---|---|---|---|
| Default | Keep last (10) | Reliable | Volatile | Ordinary topics — commands, state, anything where you want ROS 1-like behaviour |
| Sensor data | Keep last (5) | Best effort | Volatile | High-rate streams where the newest sample matters and losses are acceptable |
| Services | Keep last (10) | Reliable | Volatile | Services; volatile matters so a restarted server does not receive stale requests |
| Parameters | Keep last (1000) | Reliable | Volatile | Parameter traffic; the deep queue keeps requests from being lost |
| System default | middleware's own | middleware's own | middleware's own | Only when you deliberately want the DDS vendor's defaults |

**Sensor data** is the one you will reach for and the one that creates most mismatches, because it changes reliability. Use it when the consumer wants the latest sample as soon as it is captured and can tolerate losing some: camera frames, lidar scans, IMU. Do not use it for a topic whose messages are individually meaningful — a goal, an emergency stop, a mode change.

**Transient local** replaces ROS 1's *latching* publisher: it persists its samples for late-joining subscriptions, so a node started ten minutes after the map was published still receives the map. Two examples from stacks you will use:

- `robot_state_publisher` publishes the URDF on `robot_description` with `rclcpp::QoS(1).transient_local()`. That is why RViz can be started last and still know what the robot looks like.
- Nav2's map server publishes the occupancy grid with `rclcpp::QoS(rclcpp::KeepLast(1)).transient_local().reliable()`, with a comment in the source saying it exists to emulate a ROS 1 latched topic.

The trap follows from the durability table: latching only works if **both** sides ask for transient local. A subscriber on the default volatile profile *will* connect to a transient-local map publisher — that pair is compatible — but it receives only new messages, and the map was published once, before it started. So it waits forever on a topic that is working, and unlike the reliability case there is no warning at all, because the connection is legitimate.

Rule of thumb: anything published once and needed by whoever shows up later — map, robot description, static configuration — is transient local on both ends.

### 6. Setting QoS in code

Python:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from rclpy.qos import qos_profile_sensor_data

# A latched-equivalent publisher: keep the last message for late joiners.
latched = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)
self.map_pub = self.create_publisher(OccupancyGrid, 'map', latched)

# A subscriber that matches a best-effort sensor publisher.
self.sub = self.create_subscription(Image, 'image', self.cb, qos_profile_sensor_data)
```

C++, where the same thing is a builder chain:

```cpp
// Latched-equivalent publisher.
map_pub_ = this->create_publisher<nav_msgs::msg::OccupancyGrid>(
  "map", rclcpp::QoS(rclcpp::KeepLast(1)).transient_local().reliable());

// Sensor subscriber.
sub_ = this->create_subscription<sensor_msgs::msg::Image>(
  "image", rclcpp::SensorDataQoS(), std::bind(&MyNode::cb, this, std::placeholders::_1));
```

The `rclcpp::QoS` object also has `.best_effort()`, `.durability_volatile()`, `.deadline()`, `.lifespan()`, `.liveliness()` and `.liveliness_lease_duration()`, and the preset classes `SensorDataQoS`, `ServicesQoS`, `ParametersQoS` and `SystemDefaultsQoS` exist alongside it.

The design habit worth forming: **write the QoS of every publisher and subscription explicitly in a node you intend other people to connect to**, and say in the node's documentation what it offers. A profile that is implicit is a profile nobody can check.

### 7. Seeing a mismatch: `ros2 topic info --verbose`

This is the command. Plain `ros2 topic info` gives you counts; `--verbose` (or `-v`) prints, for every publisher and every subscription on the topic, the node name, namespace, type, type hash, GID and the full QoS profile:

```bash
ros2 topic info /image --verbose
```

```text
Type: sensor_msgs/msg/Image

Publisher count: 1

Node name: camera_driver
Node namespace: /
Topic type: sensor_msgs/msg/Image
Topic type hash: RIHS01_...
Endpoint type: PUBLISHER
GID: 01.0f.cd.24...
QoS profile:
  Reliability: BEST_EFFORT
  History (Depth): KEEP_LAST (5)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 1

Node name: my_subscriber
...
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
...
```

Read the two `Reliability` lines against the table in section 3 and you have your answer in one screen. Do this *before* you read any source code: the profile printed here is the one actually in force, which is not always the one you believe you wrote.

One CLI behaviour will mislead you. `ros2 topic echo` defaults to the sensor-data profile but then *inspects the publishers and adapts*: if every publisher offers reliable it requests reliable, if any is best effort it falls back to best effort, and the same for transient local, printing a note when it falls back. So **`ros2 topic echo` will usually show you data on a topic your own node cannot receive** — a feature for inspection, a trap for diagnosis. To make `echo` behave like your node, pin the policy yourself:

```bash
ros2 topic echo /image --qos-reliability reliable   # now it fails the same way your node does
```

`ros2 topic pub` has the same family of flags (`--qos-profile`, `--qos-reliability`, `--qos-durability`, `--qos-depth`, `--qos-history`, `--qos-liveliness`) and defaults to the `default` profile with no adaptation.

### 8. Executors: one thread or many

Callbacks do not run by themselves. An **executor** owns one or more OS threads, watches the middleware for available messages and expired timers through a *wait set*, and invokes the corresponding callbacks. `rclpy.spin(node)` and `rclcpp::spin(node)` are shorthand for instantiating a single-threaded executor, adding the node and spinning it.

rclcpp offers three: `SingleThreadedExecutor`, `MultiThreadedExecutor`, and `StaticSingleThreadedExecutor`, which scans the node's structure only once when the node is added — faster, but only correct for nodes that create all their subscriptions and timers during initialisation. rclpy offers the first two.

Two consequences that beginners get wrong:

- **One thread means one callback at a time, and a long callback delays everything.** A 200 ms callback on a node whose control timer fires at 100 Hz does not "run in the background"; it stalls the timer. Incoming messages are not queued at the client-library level — they stay in the middleware until a callback takes them, which is a deliberate difference from ROS 1, and means QoS depth (not some ROS-side buffer) decides what survives the stall.
- **The order is round-robin, not FIFO.** The wait set reports only *whether* a topic has messages, not how many or how old, so an overloaded executor processes topics in rotation rather than in arrival order.

### 9. Callback groups, and the deadlock 25.3 left open

Callbacks can be organised into **callback groups**, created with `create_callback_group` in rclcpp and by constructing the group class in rclpy. There are two kinds:

- **Mutually exclusive**: its callbacks are never executed in parallel with each other. Effectively, the group behaves as if it had its own single-threaded executor.
- **Reentrant**: its callbacks may run in parallel, including several concurrent invocations of the *same* callback.

Callbacks in *different* groups may always run in parallel. Anything created without naming a group joins the node's **default callback group, which is mutually exclusive**. Hold a reference to any group you create — if it is garbage-collected, its callbacks stop being triggered.

That default is the whole story behind the deadlock. If every entity in a node uses the default group, the node behaves exactly as if it were on a single-threaded executor *even when you gave it a multi-threaded one*. Choosing `MultiThreadedExecutor` and assigning no groups buys you nothing.

Now the failure [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]] left open. A timer callback makes a synchronous service call — `client.call(request)` in rclpy, or waiting on the future returned by `async_send_request` in rclcpp:

```python
def _timer_cb(self):
    self.get_logger().info('Sending request')
    _ = self.client.call(Empty.Request())          # blocks here, forever
    self.get_logger().info('Received response')
```

You see `Sending request` once. You never see `Received response`, and the timer never fires again. The server logs that it received the request and responded.

The mechanism: a synchronous call is not the absence of callbacks, it is a *hidden* callback. The client hands its callback group to the future whose done-callback must run for the result to become available. That done-callback and the timer callback are in the same mutually exclusive group, and the timer callback is still on the stack waiting — so the done-callback can never be scheduled. The stuck timer callback also blocks its own next firing, which is why the node goes completely quiet rather than merely missing one response.

The rule:

> If you make a synchronous call inside a callback, the callback and the client must be in **different callback groups**, or in the **same reentrant group** — and the node must be on a multi-threaded executor.

Both halves are required. Groups *permit* parallelism; a multi-threaded executor *supplies* the second thread. On a single-threaded executor the call deadlocks no matter how you arrange the groups, because there is one thread and it is already busy.

| Timer group | Client group | Executor | Outcome |
|---|---|---|---|
| default | default | multi-threaded | **Deadlock** |
| group A (mutually exclusive) | same group A | multi-threaded | **Deadlock** — a different group does not help if it is the same one |
| group A (mutually exclusive) | group B (mutually exclusive) | multi-threaded | Works |
| shared reentrant group | shared reentrant group | multi-threaded | Works |
| default | group A (mutually exclusive) | multi-threaded | Works |
| any arrangement | any arrangement | single-threaded | **Deadlock** |

The fix in Python is two lines in the constructor:

```python
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

client_cb_group = MutuallyExclusiveCallbackGroup()
timer_cb_group = MutuallyExclusiveCallbackGroup()
self.client = self.create_client(Empty, 'test_service', callback_group=client_cb_group)
self.call_timer = self.create_timer(1, self._timer_cb, callback_group=timer_cb_group)
```

and in C++, `create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive)` twice, passed to `create_client` and `create_wall_timer`.

The safer alternative, and the one the documentation prefers: **do not call synchronously inside a callback at all.** Use `async_send_request` with a done-callback and there is no group puzzle to solve. A blocking call is worth the care only where it genuinely simplifies the code — a one-shot query at startup, say.

### 10. Time: `use_sim_time`, `/clock`, and the wall clock

ROS 2 gives you three time abstractions: **SystemTime** (the machine's clock), **SteadyTime** (monotonic, for hardware timeouts, never comparable to the other two), and **ROSTime**, which is what you should use for anything that gets published or compared with a message stamp.

ROSTime reports the same as SystemTime *until a ROS time source is active*. It becomes active when the node's `use_sim_time` parameter is set. From then on, the node's clock returns the latest value received on the `/clock` topic (`rosgraph_msgs/msg/Clock`), published by the simulator or by bag playback. The consequences you have to design for:

- A time of **zero means uninitialised**, not "the epoch". A node that starts before `/clock` is published reads zero until the first clock message.
- **Time can jump backwards** — a looping bag replay does exactly that. Client libraries let you register jump handlers; algorithms that assume monotonic time will misbehave.
- The rate and granularity of `/clock` are unspecified, and timestamp accuracy is bounded by network latency multiplied by the real-time factor: a run that needs accurate stamps should be slowed down, not sped up.

Which is why the following is a bug, even though it runs:

```python
import time
stamp = time.time()            # wall clock: ignores /clock entirely
```

```python
stamp = self.get_clock().now().to_msg()    # ROS time: follows /clock when use_sim_time is set
```

Under simulation the wall-clock version drifts against every other timestamp by the real-time factor; under bag replay it stamps two-year-old sensor data with today's date, and TF lookups against it fail or silently extrapolate. It is one of very few bugs whose symptom is *worse* results rather than no results.

Timers split the same way. In rclpy, `create_timer(period, callback)` uses the node's clock, so it follows simulated time. In rclcpp, `create_wall_timer` deliberately uses the wall clock and does **not** follow `/clock`, while `create_timer(period, callback, group)` uses the node clock and does — a controller that must tick in simulated time needs the latter. Note also the rclcpp header warning: do not construct `rclcpp::Clock(RCL_ROS_TIME)` by hand, because an unattached clock silently runs on system time; use `this->get_clock()`.

Turning it on:

```bash
ros2 run my_pkg my_node --ros-args -p use_sim_time:=true
ros2 param set /my_node use_sim_time true
```

```python
# in a launch file
Node(package='my_pkg', executable='my_node', parameters=[{'use_sim_time': True}])
```

And on the source side, bag playback becomes a clock with one flag:

```bash
ros2 bag play my_bag --clock          # publishes /clock at 40 Hz by default
ros2 bag play my_bag --clock 200      # or at a rate you choose
```

The failure mode to expect: `use_sim_time` set on *some* nodes. Half the graph is on simulated time and half on wall time, transforms between them fail, and every node individually looks correct. Set it in the launch file for the whole system, and check it with `ros2 param get <node> use_sim_time` on a node you did not write.

### 11. Exercise: break a topic with QoS, then fix it

Three sourced terminals, no workspace, about fifteen minutes.

1. Publish as a sensor would — best effort:

```bash
ros2 topic pub /demo_qos std_msgs/msg/String "{data: hello}" --qos-reliability best_effort --rate 5
```

2. Subscribe as an unthinking node would — reliable. Pinning the flag is what stops `echo` from adapting to the publisher:

```bash
ros2 topic echo /demo_qos --qos-reliability reliable
```

Nothing arrives. Leave it running. Note what you have: a live publisher, a live subscriber, a matching topic name, a matching type, and no data. Check that the middleware sees them both:

```bash
ros2 topic info /demo_qos
```

Publisher count 1, subscription count 1. Every count is right and nothing works.

3. Diagnose:

```bash
ros2 topic info /demo_qos --verbose
```

Find the two `Reliability:` lines — `BEST_EFFORT` on the publisher, `RELIABLE` on the subscription — and check them against the reliability table in section 3. That is the whole diagnosis, and it took one command.

4. Fix it from the subscriber side, which is the side that is asking for too much:

```bash
ros2 topic echo /demo_qos --qos-reliability best_effort
```

Messages appear immediately. Re-run `ros2 topic info /demo_qos --verbose` and confirm both ends now read `BEST_EFFORT`.

5. Now the durability half. Publish one latched message and leave it:

```bash
ros2 topic pub /demo_latched std_msgs/msg/String "{data: the-map}" --qos-durability transient_local --qos-depth 1 --once -w 0
```

Then subscribe *after* it has exited, first with the default volatile request and then with transient local:

```bash
ros2 topic echo /demo_latched --qos-durability volatile          # nothing: the message is in the past
ros2 topic echo /demo_latched --qos-durability transient_local   # the message arrives
```

You are done when you can say, without looking, which of the four reliability combinations and which of the four durability combinations fail to connect.

### 12. The failure to diagnose: the node that stops when you add a second callback

The realistic version of section 9, and the shape it takes in a real week: a node works, you add one more thing to it, and it dies quietly.

Save this as `deadlock_demo.py` and run it with `python3 deadlock_demo.py` in a sourced terminal, with `ros2 run demo_nodes_py add_two_ints_server` running in another:

```python
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from example_interfaces.srv import AddTwoInts


class Poller(Node):
    def __init__(self):
        super().__init__('poller')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        self.client.wait_for_service()
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.get_logger().info('calling')
        req = AddTwoInts.Request(a=2, b=3)
        result = self.client.call(req)          # synchronous call inside a callback
        self.get_logger().info(f'got {result.sum}')


rclpy.init()
node = Poller()
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

**Symptom.** One `calling`. No `got 5`. No error, no traceback, no exit. The server's terminal shows it handled the request. `ros2 node list` still shows `/poller`; it answers nothing and its timer never fires again.

**Why it looks like "adding a second callback broke it".** The client alone works, the timer alone works, and only the combination — a blocking wait inside one callback for a result another callback must deliver — deadlocks. The bisection instinct ("it worked before I added the timer") therefore points at the wrong thing.

**How to find it.** In order:

1. `ros2 node list` — the node is alive. That rules out a crash.
2. `ros2 topic hz /rosout` or simply watching the log — no output at all, rather than errors, points at a stuck thread rather than a logic bug.
3. `ros2 service list` and `ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"` from a third terminal — the server answers you instantly. The server is not the problem.
4. Now the decisive question, which is about your own source, not the graph: *does any callback in this node block on something another callback must produce?* A synchronous service call, `spin_until_future_complete` inside a callback, an action `get_result` wait, `time.sleep` in a callback waiting for a message.
5. Confirm by running with a `MultiThreadedExecutor` and two separate mutually exclusive callback groups, one for the client and one for the timer. If it starts working, that was it.

**The fix**, as in section 9: put the timer and the client in different callback groups on a multi-threaded executor, or convert the call to `call_async` with a done-callback — the second is what to do in code you will maintain.

Practise this one deliberately, because no command hands you the answer: there is no error message, the symptom matches a dozen other causes, and the fix lives in a part of the code most people never touch. Recognising the *shape* — a callback waiting for a callback — is the whole skill.

### 13. What this page does not cover

Per-topic QoS overrides for recording and replay, and the ordered set of checks to run when a system misbehaves, are [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]. Real-time execution — RT kernels, memory locking, response-time analysis of callback chains, and the rclc executor with its explicit execution order — is beyond this track; the Casini et al. ECRTS 2019 analysis of ROS 2 processing chains is the entry point. DDS vendor tuning (buffer sizes, multicast, shared-memory transports) is in the vendor's documentation, not in ROS 2's. How `/clock` actually gets published by a simulator, and what `use_sim_time` does to a controller, arrive with Gazebo in [[04-robotics/ros2/index|25. ROS 2]]. Intra-process communication and composition, which change the executor picture substantially, are the ROS 2 composition documentation.

### Sources

- ROS 2 Jazzy documentation — Concepts: Quality of Service settings (policies, profiles, compatibility tables, QoS events, matched events).
- ROS 2 Jazzy documentation — Concepts: Executors (executor types, callback groups, wait set, scheduling semantics).
- ROS 2 Jazzy documentation — How-to Guides: Using Callback Groups (deadlock example, working and non-working configurations).
- ROS 2 Jazzy documentation — Tutorials: Using quality-of-service settings for lossy networks.
- ROS 2 design article — Clock and Time (SystemTime, SteadyTime, ROSTime, the `/clock` time source, `use_sim_time`, time jumps).
- Source, Jazzy branches, for values and messages quoted verbatim: `rmw/qos_profiles.h` (profile contents), `rclcpp/subscription_base.cpp` and `publisher_base.cpp`, `rclpy/event_handler.py` (default incompatible-QoS warnings), `rclpy/topic_endpoint_info.py` (the `--verbose` output format), `ros2cli/ros2topic` (QoS flags and `echo`'s publisher-matching behaviour), `ros2bag` play verb (`--clock`), `robot_state_publisher` and `nav2_map_server` (transient-local publishers).
- Daniel Casini, Tobias Blass, Ingo Lütkebohle, Björn Brandenburg, "Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling", ECRTS 2019.

> [!question]- Self-check · Answer
> **1. A publisher offers reliable and a subscription requests best effort. Do they connect, and why is the reverse case different?** They connect. The request is the minimum quality the subscription will accept and the offer is the maximum the publisher can provide, so a reliable publisher over-satisfies a best-effort request. The reverse — best-effort publisher, reliable subscription — asks for a guarantee that is not on offer, so no connection is made and no message is exchanged.
> **2. Your node subscribes to `/map` and never receives anything, but `ros2 topic echo /map` prints a map immediately. What is going on?** Almost certainly durability. The map server publishes transient local, once, before your node started; your node requests the default volatile profile, which connects legitimately but receives only new messages. `ros2 topic echo` inspects the publishers and adapts its own request to transient local, so it gets the retained sample. Fix your subscription to request transient local, and remember that `echo` succeeding does not prove your node can.
> **3. You put your node on a `MultiThreadedExecutor` and the synchronous service call in your timer still deadlocks. Why?** Because you did not assign callback groups. Everything created without a group joins the node's default group, which is mutually exclusive, so the node behaves as if it were single-threaded. The timer callback holds the group while waiting, and the future's hidden done-callback — which must run for the result to appear — cannot be scheduled in the same mutually exclusive group. Put the client and the timer in different groups, or in one shared reentrant group.
> **4. A node stamps its messages with `time.time()`. Everything works in the lab and the numbers are wrong on a bag replay. What exactly goes wrong, and what should it call?** `time.time()` is the wall clock and ignores `/clock` entirely, so under replay it stamps data recorded two years ago with today's time; under simulation it drifts against the rest of the system by the real-time factor. Downstream TF lookups and any comparison with other message stamps then fail or silently extrapolate. It should call `self.get_clock().now()` on the node's clock, with `use_sim_time` set for the whole graph — and use `create_timer` rather than a wall timer if its period must follow simulated time.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 돌아가는 시스템에서 세 가지 조용한 실패를 알아보고 고칠 정도. Executor의 형식적 타이밍 분석을 할 정도는 아니다.
> **Working** — enough to recognise and fix all three silent failures, not to do formal timing analysis.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]]와 [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]] — 퍼블리셔, 서브스크라이버, 서비스 클라이언트를 한 번씩 써 봤다고 가정한다. 기준 환경은 [[04-robotics/ros2/index|25. ROS 2]]와 같은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**이고, 워크스페이스는 필요 없다. 실습은 커맨드라인과 평범한 Python 파일로 돌아간다.
> 25.2 and 25.3 are assumed; everything runs on ROS 2 Jazzy on Ubuntu 24.04 without a workspace.

### 1. 이 페이지가 존재하는 이유

ROS 2의 문제는 대개 스스로를 알린다. 토픽 이름을 틀리면 `ros2 topic echo`가 비고, 패키지가 없으면 오류가 나고, 타입이 어긋나면 빌드가 거부된다.

스스로를 알리지 않는 기전이 셋 있고, 이 페이지가 그 셋이다.

- **QoS.** 같은 토픽, 같은 타입인데도 전달 정책이 호환되지 않아 퍼블리셔와 서브스크라이버가 연결되지 않는다. 두 프로세스 다 멀쩡하고, `ros2 node list`에도 다 나오고, 메시지는 한 개도 오가지 않는다.
- **Executor.** 어떤 콜백이, 같은 executor 스레드가 실행해야 하는 다른 콜백만이 만들어 낼 수 있는 것을 기다리며 막힌다. 노드는 응답을 멈춘다. 죽지도 않고, 로그도 남기지 않고, 퍼블리셔는 광고된 채로 남는다.
- **시간.** 시스템 나머지가 시뮬레이션 시간이나 재생 시간 위에서 도는데 어떤 노드가 벽시계를 읽는다. 그 노드의 타임스탬프는 무엇과도 맞지 않고, 타임아웃은 엉뚱한 순간에 터지고, 내놓는 값은 전부 그럴듯해 보인다.

증상은 공통적으로 "아무 일도 일어나지 않음"이다. 처방도 공통이다. 이 셋이 존재한다는 것을 알고, 각각에 대해 명령 하나씩을 갖고 있으면 된다.

### 2. QoS 정책들

QoS *프로파일*은 *정책*의 묶음이고, 퍼블리셔·서브스크립션·서비스 서버·클라이언트마다 독립적으로 적용된다. 기본 프로파일이 담는 것:

| 정책 | 값 | 무엇을 정하는가 |
|---|---|---|
| History | *Keep last*(최대 N개 보관) \| *Keep all*(미들웨어 자원 한도까지) | 미들웨어가 무엇을 보관하는가 |
| Depth | 큐 크기 N | history가 *keep last*일 때만 유효 |
| Reliability | *Best effort* \| *Reliable* | 확인 응답을 받을 때까지 재전송하는가 |
| Durability | *Volatile* \| *Transient local* | 늦게 들어온 구독자를 위해 샘플을 보존하는가 |
| Deadline | 기간 | 토픽에 메시지가 연달아 발행되는 최대 간격 기대치 |
| Lifespan | 기간 | 이 나이를 넘긴 메시지는 만료로 간주되어 조용히 버려지고 영영 수신되지 않는다 |
| Liveliness | *Automatic* \| *Manual by topic* | 퍼블리셔가 살아 있다고 판정하는 방식 |
| Lease duration | 기간 | 살아 있음을 주장해야 하는 기한. 넘기면 liveliness를 잃은 것으로 본다 |

기간이 아닌 모든 정책에는 미들웨어에 위임하는 *system default*가 있고, 기간인 모든 정책에는 지정하지 않음을 뜻하는 *default*가 있다. 미들웨어는 보통 후자를 무한으로 해석한다.

deadline, lifespan, liveliness는 대부분 설정하지 않는 셋이지만, 스트림이 *멈췄다*는 것을 알려 줄 수 있는 유일한 정책들이다. deadline을 걸면 서브스크립션이 *requested deadline missed* 이벤트를 받고, liveliness lease를 걸면 퍼블리셔가 조용히 죽을 때 *liveliness changed* 이벤트를 받는다. 이것이 없으면 죽은 센서와 느린 센서가 똑같아 보인다.

### 3. 호환성: request 대 offered 규칙

외워야 할 규칙이다. 4절의 모든 것이 여기서 따라 나온다.

> 서브스크립션은 받아들일 수 있는 *최소 품질*을 **request**한다. 퍼블리셔는 제공할 수 있는 *최대 품질*을 **offer**한다. 요청의 **모든** 정책이 대응하는 제공보다 더 까다롭지 않을 때만 연결된다.

호환성은 쌍 단위이고 다른 참여자와 무관하다. 퍼블리셔 하나가 서로 다른 요청 프로파일을 가진 여러 서브스크립션을 동시에 상대할 수 있고, 제3의 노드가 있어도 판정은 바뀌지 않는다.

*Reliability:*

| 퍼블리셔 offer | 서브스크립션 request | 호환 |
|---|---|---|
| Best effort | Best effort | 예 |
| Best effort | Reliable | **아니오** |
| Reliable | Best effort | 예 |
| Reliable | Reliable | 예 |

*Durability:*

| 퍼블리셔 offer | 서브스크립션 request | 호환 | 결과 |
|---|---|---|---|
| Volatile | Volatile | 예 | 새 메시지만 |
| Volatile | Transient local | **아니오** | 통신 없음 |
| Transient local | Volatile | 예 | 새 메시지만 |
| Transient local | Transient local | 예 | 새 메시지와 과거 메시지 |

deadline과 lease duration은 기간에 대해 같은 모양을 따른다. 퍼블리셔가 *default*인데 서브스크립션이 기간을 명시하면 비호환이고, 퍼블리셔 *x*에 대해 요청 *y*는 *y ≥ x*이면 호환, *y < x*이면 비호환이다. liveliness는 *manual by topic* 제공이 *automatic* 요청을 만족시키지만 그 반대는 아니다.

모든 정책이 동시에 호환이어야 한다. reliability가 맞아도 durability가 어긋나면 연결되지 않는다. ROS 1에서는 같은 토픽에 같은 타입이면 무조건 연결됐으므로, 이것은 ROS 2에서 새로 생긴 실패 경로다.

### 4. 조용한 사례, 그리고 운이 좋으면 나오는 경고 한 줄

정석 사례. 카메라 드라이버가 30 Hz로 발행하고, 합리적으로 작성되어 있다. 프레임을 떨어뜨리는 편이 막히는 것보다 나으므로 **best effort**를 offer한다. 당신은 QoS를 생각하지 않고 서브스크라이버를 쓴다. 기본 프로파일, 즉 **reliable**이 된다. 제공되지 않는 품질을 요청한 것이다.

결과: `ros2 node list`에 두 노드가 다 있다. `ros2 topic list`에 토픽이 있다. `ros2 topic info`는 퍼블리셔 1, 서브스크립션 1을 보고한다. 콜백은 한 번도 실행되지 않는다.

통설에 한 가지 정정이 필요하다. 추적할 때 중요하다. 이 실패는 *완전히* 보이지 않는 것은 아니다. rclcpp와 rclpy 모두 incompatible-QoS 이벤트의 기본 핸들러를 등록하고, 그것이 탐색 시점에 노드 자신의 로거로 경고를 한 번 찍는다.

```text
[WARN] [...] [my_subscriber]: New publisher discovered on topic '/image', offering incompatible QoS. No messages will be received from it. Last incompatible policy: RELIABILITY
```

퍼블리셔 쪽에는 비호환 요청을 하는 서브스크립션에 대한 대칭적인 경고가 있다. 그런데도 왜 다들 반나절을 잃는가.

- 탐색 시점에 **한 번** 나온다. 노드 스무 개짜리 런치 파일의 기동 소음 속에서, ERROR가 아니라 WARN으로, 그 노드 자신의 로거를 통해.
- 이벤트를 지원하지 않는 미들웨어를 위해 등록이 try-후-무시로 감싸여 있다. 경고가 없다는 것은 아무것도 증명하지 않는다.
- 그 한 줄 이후의 정상 상태 실패는 출력을 전혀 만들지 않는다. 한 시간째 돌던 시스템에 붙으면 로그가 비어 있다.

경고가 나오면 선물로 여기되, 그것에 의존하지는 마라.

### 5. 미리 정의된 프로파일, 그리고 latched의 대체물

엔드포인트마다 정책 여덟 개를 고르라는 것은 합당한 요구가 아니므로, ROS 2는 서로 잘 어울린다고 알려진 프로파일을 제공한다.

| 프로파일 | History (depth) | Reliability | Durability | 쓰는 곳 |
|---|---|---|---|---|
| Default | Keep last (10) | Reliable | Volatile | 보통 토픽 — 명령, 상태, ROS 1과 비슷한 동작을 원하는 모든 것 |
| Sensor data | Keep last (5) | Best effort | Volatile | 최신 샘플이 중요하고 손실을 감수하는 고속 스트림 |
| Services | Keep last (10) | Reliable | Volatile | 서비스. 재시작한 서버가 낡은 요청을 받지 않도록 volatile이 중요하다 |
| Parameters | Keep last (1000) | Reliable | Volatile | 파라미터 트래픽. 깊은 큐가 요청 유실을 막는다 |
| System default | 미들웨어 기본값 | 미들웨어 기본값 | 미들웨어 기본값 | DDS 벤더 기본값을 일부러 원할 때만 |

**Sensor data**는 가장 자주 손이 가고 가장 많은 불일치를 만든다. reliability를 바꾸기 때문이다. 소비자가 캡처 직후의 최신 샘플을 원하고 일부 손실을 감당할 수 있을 때 쓴다. 카메라 프레임, 라이다 스캔, IMU. 메시지 하나하나가 개별적으로 의미를 갖는 토픽 — 목표, 비상 정지, 모드 변경 — 에는 쓰지 마라.

**Transient local**은 ROS 1의 *latching* 퍼블리셔를 대신한다. 늦게 들어오는 구독자를 위해 샘플을 보존하므로, 지도가 발행되고 10분 뒤에 뜬 노드도 그 지도를 받는다. 실제로 쓰게 될 스택의 예 둘:

- `robot_state_publisher`는 `robot_description`에 URDF를 `rclcpp::QoS(1).transient_local()`로 발행한다. RViz를 맨 마지막에 켜도 로봇 생김새를 아는 이유다.
- Nav2의 map server는 점유 격자를 `rclcpp::QoS(rclcpp::KeepLast(1)).transient_local().reliable()`로 발행하며, 소스의 주석은 이것이 ROS 1 latched 토픽을 흉내 내기 위한 것이라고 적고 있다.

함정은 durability 표에서 곧장 따라 나온다. latching은 **양쪽 모두** transient local을 요구할 때만 동작한다. 기본 volatile 프로파일을 쓰는 구독자도 transient local 퍼블리셔에 연결은 *된다*. 호환되는 쌍이기 때문이다. 하지만 새 메시지만 받는데, 지도는 그 노드가 뜨기 전에 한 번 발행됐다. 그래서 멀쩡히 동작하는 토픽 위에서 영원히 기다리고, reliability 쪽과 달리 경고조차 나오지 않는다. 연결 자체는 정당하기 때문이다.

경험칙: 한 번 발행되고 나중에 뜬 쪽이 필요로 하는 것 — 지도, 로봇 기술, 정적 설정 — 은 양쪽 다 transient local로 한다.

### 6. 코드에서 QoS 설정하기

Python:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from rclpy.qos import qos_profile_sensor_data

# latched 대체 퍼블리셔: 늦게 온 구독자를 위해 마지막 메시지를 보관한다.
latched = QoSProfile(
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
)
self.map_pub = self.create_publisher(OccupancyGrid, 'map', latched)

# best effort 센서 퍼블리셔에 맞추는 서브스크라이버.
self.sub = self.create_subscription(Image, 'image', self.cb, qos_profile_sensor_data)
```

C++에서는 같은 것이 빌더 체인이다.

```cpp
// latched 대체 퍼블리셔.
map_pub_ = this->create_publisher<nav_msgs::msg::OccupancyGrid>(
  "map", rclcpp::QoS(rclcpp::KeepLast(1)).transient_local().reliable());

// 센서 서브스크라이버.
sub_ = this->create_subscription<sensor_msgs::msg::Image>(
  "image", rclcpp::SensorDataQoS(), std::bind(&MyNode::cb, this, std::placeholders::_1));
```

`rclcpp::QoS` 객체에는 `.best_effort()`, `.durability_volatile()`, `.deadline()`, `.lifespan()`, `.liveliness()`, `.liveliness_lease_duration()`도 있고, 프리셋 클래스로 `SensorDataQoS`, `ServicesQoS`, `ParametersQoS`, `SystemDefaultsQoS`가 함께 있다.

들일 습관: **남이 붙을 노드라면 모든 퍼블리셔와 서브스크립션의 QoS를 명시적으로 쓰고**, 무엇을 offer하는지 노드 문서에 적어라. 암묵적인 프로파일은 아무도 검사할 수 없는 프로파일이다.

### 7. 불일치 보기: `ros2 topic info --verbose`

이것이 그 명령이다. 그냥 `ros2 topic info`는 개수만 주지만, `--verbose`(또는 `-v`)는 토픽의 퍼블리셔와 서브스크립션마다 노드 이름, 네임스페이스, 타입, 타입 해시, GID, 그리고 전체 QoS 프로파일을 찍는다.

```bash
ros2 topic info /image --verbose
```

```text
Type: sensor_msgs/msg/Image

Publisher count: 1

Node name: camera_driver
Node namespace: /
Topic type: sensor_msgs/msg/Image
Topic type hash: RIHS01_...
Endpoint type: PUBLISHER
GID: 01.0f.cd.24...
QoS profile:
  Reliability: BEST_EFFORT
  History (Depth): KEEP_LAST (5)
  Durability: VOLATILE
  Lifespan: Infinite
  Deadline: Infinite
  Liveliness: AUTOMATIC
  Liveliness lease duration: Infinite

Subscription count: 1

Node name: my_subscriber
...
  Reliability: RELIABLE
  History (Depth): KEEP_LAST (10)
  Durability: VOLATILE
...
```

두 `Reliability` 줄을 3절의 표에 대조하면 한 화면에서 답이 나온다. 소스를 읽기 *전에* 이것을 하라. 여기 찍히는 프로파일이 실제로 적용 중인 프로파일이고, 그것이 당신이 썼다고 믿는 프로파일과 늘 같지는 않다.

사람을 속이는 CLI 동작이 하나 있다. `ros2 topic echo`는 기본값이 sensor data 프로파일이지만 *퍼블리셔들을 조사해 스스로를 맞춘다*. 모두 reliable이면 reliable을 요청하고, 하나라도 best effort면 best effort로 물러서며, transient local도 마찬가지이고 물러설 때는 안내 문구를 찍는다. 그래서 **`ros2 topic echo`는 당신 노드가 받지 못하는 토픽에서도 대개 데이터를 보여 준다.** 관측에는 기능이고 진단에는 함정이다. `echo`를 당신 노드처럼 굴게 하려면 정책을 직접 고정하라.

```bash
ros2 topic echo /image --qos-reliability reliable   # 이제 당신 노드와 똑같이 실패한다
```

`ros2 topic pub`도 같은 계열의 플래그(`--qos-profile`, `--qos-reliability`, `--qos-durability`, `--qos-depth`, `--qos-history`, `--qos-liveliness`)를 갖고, 기본값은 `default` 프로파일이며 이쪽은 맞춰 주지 않는다.

### 8. Executor: 스레드 하나인가 여럿인가

콜백은 저절로 돌지 않는다. **Executor**가 OS 스레드 하나 이상을 소유하고, *wait set*을 통해 미들웨어에 도착한 메시지와 만료된 타이머를 감시하며 해당 콜백을 호출한다. `rclpy.spin(node)`와 `rclcpp::spin(node)`는 단일 스레드 executor를 만들고 노드를 붙여 spin하는 것의 축약이다.

rclcpp는 셋을 제공한다. `SingleThreadedExecutor`, `MultiThreadedExecutor`, 그리고 노드를 붙일 때 구조를 한 번만 훑는 `StaticSingleThreadedExecutor`다. 마지막 것은 더 빠르지만 모든 서브스크립션과 타이머를 초기화 때 만드는 노드에서만 옳다. rclpy는 앞의 둘을 제공한다.

초심자가 틀리는 귀결 둘:

- **스레드 하나는 한 번에 콜백 하나를 뜻하고, 긴 콜백은 모든 것을 지연시킨다.** 100 Hz 제어 타이머를 가진 노드에서 200 ms짜리 콜백은 "뒤에서 도는" 것이 아니라 타이머를 세운다. 도착한 메시지는 클라이언트 라이브러리 층에 쌓이지 않고 콜백이 가져갈 때까지 미들웨어에 남는다. ROS 1과의 의도적인 차이이고, 그 정체 구간에서 무엇이 살아남는지는 ROS 쪽 버퍼가 아니라 QoS depth가 정한다는 뜻이다.
- **순서는 FIFO가 아니라 라운드 로빈이다.** wait set은 어떤 토픽에 메시지가 *있는지*만 보고할 뿐 몇 개인지, 얼마나 오래됐는지는 보고하지 않는다. 그래서 과부하된 executor는 도착 순서가 아니라 토픽을 돌아가며 처리한다.

### 9. 콜백 그룹, 그리고 25.3이 남겨 둔 교착

콜백은 **콜백 그룹**으로 묶을 수 있다. rclcpp에서는 `create_callback_group`으로, rclpy에서는 그룹 클래스를 생성해서 만든다. 두 종류가 있다.

- **Mutually exclusive**: 이 그룹의 콜백들은 서로 병렬로 실행되지 않는다. 사실상 그룹이 자기만의 단일 스레드 executor를 가진 것처럼 동작한다.
- **Reentrant**: 이 그룹의 콜백은 병렬로 실행될 수 있고, *같은* 콜백의 동시 실행도 허용된다.

*다른* 그룹의 콜백끼리는 언제나 병렬 실행이 가능하다. 그룹을 지정하지 않고 만든 것은 전부 노드의 **기본 콜백 그룹에 들어가고, 그것은 mutually exclusive다.** 직접 만든 그룹은 참조를 붙들고 있어야 한다. 수거되면 그 콜백은 더 이상 트리거되지 않는다.

그 기본값이 교착의 전말이다. 노드의 모든 엔티티가 기본 그룹을 쓰면, *멀티 스레드 executor를 줬더라도* 노드는 단일 스레드 executor 위에 있는 것과 똑같이 동작한다. `MultiThreadedExecutor`를 고르고 그룹을 하나도 지정하지 않으면 얻는 것이 없다.

이제 [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]]이 남겨 둔 실패다. 타이머 콜백이 동기 서비스 호출을 한다. rclpy의 `client.call(request)`, 또는 rclcpp에서 `async_send_request`가 돌려준 future를 기다리는 것.

```python
def _timer_cb(self):
    self.get_logger().info('Sending request')
    _ = self.client.call(Empty.Request())          # 여기서 영원히 막힌다
    self.get_logger().info('Received response')
```

`Sending request`가 한 번 보인다. `Received response`는 영영 없고, 타이머는 다시 울리지 않는다. 서버 쪽 터미널에는 요청을 받아 응답했다고 찍힌다.

기전: 동기 호출은 콜백이 없는 것이 아니라 콜백이 *숨어 있는* 것이다. 클라이언트는 자기 콜백 그룹을 future에 넘기고, 결과가 나오려면 그 future의 done-callback이 실행되어야 한다. 그 done-callback과 타이머 콜백이 같은 mutually exclusive 그룹에 있는데 타이머 콜백은 기다리며 스택에 남아 있으므로, done-callback은 영영 스케줄되지 못한다. 막힌 타이머 콜백은 자기 다음 발화도 막으므로 노드는 응답 하나를 놓치는 정도가 아니라 완전히 조용해진다.

규칙:

> 콜백 안에서 동기 호출을 한다면, 그 콜백과 클라이언트는 **서로 다른 콜백 그룹**에 있거나 **같은 reentrant 그룹**에 있어야 한다 — 그리고 노드는 멀티 스레드 executor 위에 있어야 한다.

두 조건 다 필요하다. 그룹은 병렬을 *허용*하고, 멀티 스레드 executor가 두 번째 스레드를 *공급*한다. 단일 스레드 executor에서는 그룹을 어떻게 배치하든 교착한다. 스레드가 하나뿐이고 이미 바쁘기 때문이다.

| 타이머 그룹 | 클라이언트 그룹 | Executor | 결과 |
|---|---|---|---|
| 기본 | 기본 | 멀티 스레드 | **교착** |
| 그룹 A (mutually exclusive) | 같은 그룹 A | 멀티 스레드 | **교착** — 같은 그룹이면 기본이 아니어도 소용없다 |
| 그룹 A (mutually exclusive) | 그룹 B (mutually exclusive) | 멀티 스레드 | 동작 |
| 공유 reentrant 그룹 | 공유 reentrant 그룹 | 멀티 스레드 | 동작 |
| 기본 | 그룹 A (mutually exclusive) | 멀티 스레드 | 동작 |
| 어떤 배치든 | 어떤 배치든 | 단일 스레드 | **교착** |

Python에서의 수정은 생성자 두 줄이다.

```python
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor

client_cb_group = MutuallyExclusiveCallbackGroup()
timer_cb_group = MutuallyExclusiveCallbackGroup()
self.client = self.create_client(Empty, 'test_service', callback_group=client_cb_group)
self.call_timer = self.create_timer(1, self._timer_cb, callback_group=timer_cb_group)
```

C++에서는 `create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive)`을 두 번 만들어 `create_client`와 `create_wall_timer`에 넘긴다.

더 안전한 대안이자 문서가 선호하는 쪽: **콜백 안에서는 아예 동기 호출을 하지 않는 것이다.** `async_send_request`와 done-callback을 쓰면 풀어야 할 그룹 퍼즐 자체가 없다. 막고 기다리는 호출은 그것이 코드를 실제로 단순하게 만들 때 — 예컨대 기동 시 한 번 하는 질의 — 에만 값어치가 있다.

### 10. 시간: `use_sim_time`, `/clock`, 그리고 벽시계

ROS 2는 시간 추상을 셋 준다. **SystemTime**(머신의 시계), **SteadyTime**(단조 증가. 하드웨어 타임아웃용이며 다른 둘과 비교 불가), 그리고 **ROSTime**. 발행되거나 메시지 스탬프와 비교되는 모든 것에는 ROSTime을 써야 한다.

ROSTime은 *ROS 시간 소스가 활성화되기 전까지는* SystemTime과 같은 값을 보고한다. 활성화 조건은 노드의 `use_sim_time` 파라미터가 설정되는 것이다. 그 뒤로 노드의 시계는 `/clock` 토픽(`rosgraph_msgs/msg/Clock`)으로 받은 최신 값을 돌려준다. 이 토픽은 시뮬레이터나 bag 재생이 발행한다. 설계할 때 감안해야 할 귀결들:

- 시간 **0은 초기화되지 않았다는 뜻**이지 에포크가 아니다. `/clock` 발행 전에 뜬 노드는 첫 clock 메시지까지 0을 읽는다.
- **시간이 뒤로 점프할 수 있다.** 루프 재생이 바로 그렇게 한다. 점프 핸들러를 등록할 수 있지만, 단조 증가를 가정한 알고리즘은 오작동한다.
- `/clock`의 주기와 해상도는 규정되어 있지 않고, 타임스탬프 정확도는 네트워크 지연에 실시간 계수를 곱한 만큼으로 제한된다. 정확한 스탬프가 필요한 실행은 빠르게가 아니라 느리게 돌려야 한다.

그래서 아래는 실행은 되지만 버그다.

```python
import time
stamp = time.time()            # 벽시계: /clock을 완전히 무시한다
```

```python
stamp = self.get_clock().now().to_msg()    # ROS 시간: use_sim_time이 켜지면 /clock을 따른다
```

시뮬레이션에서 벽시계 버전은 다른 모든 타임스탬프에 대해 실시간 계수만큼 어긋나고, bag 재생에서는 2년 전 센서 데이터에 오늘 날짜를 찍는다. 그러면 그 값에 대한 TF 조회는 실패하거나 조용히 외삽한다. 증상이 "결과 없음"이 아니라 "더 나쁜 결과"인 드문 버그다.

타이머도 같은 분기를 갖는다. rclpy의 `create_timer(period, callback)`은 노드 시계를 쓰므로 시뮬레이션 시간을 따른다. rclcpp의 `create_wall_timer`는 의도적으로 벽시계를 쓰고 `/clock`을 따르지 **않으며**, `create_timer(period, callback, group)`이 노드 시계를 쓴다. 제어기가 시뮬레이션 시간으로 tick해야 한다면 후자가 필요하다. rclcpp 헤더의 경고도 기억하라. `rclcpp::Clock(RCL_ROS_TIME)`을 직접 생성하지 마라. 붙이지 않은 시계는 조용히 시스템 시간으로 돈다. `this->get_clock()`을 쓴다.

켜는 방법:

```bash
ros2 run my_pkg my_node --ros-args -p use_sim_time:=true
ros2 param set /my_node use_sim_time true
```

```python
# 런치 파일에서
Node(package='my_pkg', executable='my_node', parameters=[{'use_sim_time': True}])
```

공급하는 쪽에서는 플래그 하나로 bag 재생이 시계가 된다.

```bash
ros2 bag play my_bag --clock          # 기본 40 Hz로 /clock 발행
ros2 bag play my_bag --clock 200      # 원하는 주기로
```

예상해야 할 실패 양상: `use_sim_time`이 *일부* 노드에만 설정된 경우다. 그래프의 절반은 시뮬레이션 시간, 절반은 벽시계 위에 있고, 그 사이의 변환은 실패하는데 노드는 하나씩 보면 전부 멀쩡하다. 런치 파일에서 시스템 전체에 설정하고, 남이 쓴 노드는 `ros2 param get <node> use_sim_time`으로 확인하라.

### 11. 실습: QoS로 토픽을 망가뜨리고 고치기

source된 터미널 셋, 워크스페이스 없이 15분쯤.

1. 센서처럼 best effort로 발행한다.

```bash
ros2 topic pub /demo_qos std_msgs/msg/String "{data: hello}" --qos-reliability best_effort --rate 5
```

2. 생각 없는 노드처럼 reliable로 구독한다. 플래그를 고정해야 `echo`가 퍼블리셔에 맞춰 주지 않는다.

```bash
ros2 topic echo /demo_qos --qos-reliability reliable
```

아무것도 오지 않는다. 그대로 둔다. 지금 가진 것을 보라. 살아 있는 퍼블리셔, 살아 있는 서브스크라이버, 일치하는 토픽 이름, 일치하는 타입, 그리고 데이터 없음. 미들웨어가 둘 다 보고 있는지 확인한다.

```bash
ros2 topic info /demo_qos
```

퍼블리셔 1, 서브스크립션 1. 숫자는 전부 맞는데 아무것도 동작하지 않는다.

3. 진단한다.

```bash
ros2 topic info /demo_qos --verbose
```

두 `Reliability:` 줄 — 퍼블리셔 `BEST_EFFORT`, 서브스크립션 `RELIABLE` — 을 찾아 3절의 reliability 표에 대조한다. 진단 끝이고, 명령 하나면 됐다.

4. 과하게 요구한 쪽, 즉 서브스크라이버 쪽에서 고친다.

```bash
ros2 topic echo /demo_qos --qos-reliability best_effort
```

즉시 메시지가 나온다. `ros2 topic info /demo_qos --verbose`를 다시 돌려 양쪽이 `BEST_EFFORT`인지 확인한다.

5. 이제 durability 쪽. latched 메시지 하나를 발행하고 둔다.

```bash
ros2 topic pub /demo_latched std_msgs/msg/String "{data: the-map}" --qos-durability transient_local --qos-depth 1 --once -w 0
```

그것이 끝난 *뒤에* 구독한다. 먼저 기본 volatile 요청으로, 다음에 transient local로.

```bash
ros2 topic echo /demo_latched --qos-durability volatile          # 없음: 메시지는 과거에 있다
ros2 topic echo /demo_latched --qos-durability transient_local   # 메시지가 온다
```

reliability 네 조합과 durability 네 조합 중 어느 것이 연결에 실패하는지 보지 않고 말할 수 있으면 끝난 것이다.

### 12. 진단할 실패: 콜백을 하나 더 붙이자 멈추는 노드

9절의 현실판이고, 실제 한 주에 나타나는 모양이다. 노드가 잘 돌던 중에 뭔가 하나를 더 붙였더니 조용히 죽는다.

아래를 `deadlock_demo.py`로 저장하고, 다른 터미널에서 `ros2 run demo_nodes_py add_two_ints_server`를 띄운 채 source된 터미널에서 `python3 deadlock_demo.py`로 실행한다.

```python
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from example_interfaces.srv import AddTwoInts


class Poller(Node):
    def __init__(self):
        super().__init__('poller')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        self.client.wait_for_service()
        self.timer = self.create_timer(1.0, self.on_timer)

    def on_timer(self):
        self.get_logger().info('calling')
        req = AddTwoInts.Request(a=2, b=3)
        result = self.client.call(req)          # 콜백 안의 동기 호출
        self.get_logger().info(f'got {result.sum}')


rclpy.init()
node = Poller()
executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()
```

**증상.** `calling` 한 번. `got 5`는 없음. 오류도, 트레이스백도, 종료도 없음. 서버 터미널에는 요청을 처리했다고 찍힌다. `ros2 node list`에는 `/poller`가 여전히 있다. 아무것에도 응답하지 않고 타이머는 다시 울리지 않는다.

**왜 "콜백을 하나 더 붙여서 깨진 것"처럼 보이는가.** 클라이언트만 있으면 동작하고 타이머만 있어도 동작한다. 깨지는 것은 조합 — 다른 콜백이 내놓아야 할 결과를 한 콜백 안에서 막고 기다리는 것 — 뿐이므로, "타이머를 붙이기 전에는 됐다"는 이분 탐색 본능이 엉뚱한 곳을 가리킨다.

**찾는 법.** 순서대로:

1. `ros2 node list` — 노드는 살아 있다. 크래시는 배제된다.
2. `ros2 topic hz /rosout`, 또는 그냥 로그를 본다. 오류가 아니라 출력이 전혀 없다는 것은 논리 버그가 아니라 막힌 스레드를 가리킨다.
3. 세 번째 터미널에서 `ros2 service list`와 `ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"` — 서버는 즉시 답한다. 서버는 문제가 아니다.
4. 이제 결정적인 질문. 그래프가 아니라 자기 소스에 대한 질문이다. *이 노드의 어떤 콜백이 다른 콜백이 만들어야 할 것을 기다리며 막히는가?* 동기 서비스 호출, 콜백 안의 `spin_until_future_complete`, 액션 `get_result` 대기, 메시지를 기다리는 콜백 안의 `time.sleep`.
5. `MultiThreadedExecutor`와 클라이언트용·타이머용 mutually exclusive 그룹 둘로 바꿔 돌려 확인한다. 동작하기 시작하면 그것이 원인이었다.

**수정**은 9절과 같다. 멀티 스레드 executor 위에서 타이머와 클라이언트를 다른 콜백 그룹에 넣거나, 호출을 `call_async`와 done-callback으로 바꾼다. 계속 유지할 코드라면 후자가 답이다.

이것은 일부러 연습해 둘 값어치가 있다. 답을 대신 알려 주는 명령이 없기 때문이다. 오류 메시지가 없고, 증상이 다른 열두 가지 원인과 똑같고, 수정 지점이 대부분 손대지 않는 부분에 있다. *모양* — 콜백이 콜백을 기다린다 — 을 알아보는 것이 기술의 전부다.

### 13. 이 페이지가 다루지 않는 것

기록과 재생 시의 토픽별 QoS 오버라이드, 그리고 시스템이 이상할 때 돌릴 순서 있는 점검 목록은 [[04-robotics/ros2/debugging-data-reproducibility|25.10 디버깅, 데이터, 재현성]]에 있다. 실시간 실행 — RT 커널, 메모리 고정, 콜백 체인의 응답 시간 분석, 실행 순서를 명시하는 rclc executor — 는 이 트랙 밖이다. 시작점은 Casini 외의 ECRTS 2019 분석이다. DDS 벤더 튜닝(버퍼 크기, 멀티캐스트, 공유 메모리 전송)은 ROS 2가 아니라 벤더 문서에 있다. 시뮬레이터가 `/clock`을 실제로 어떻게 발행하는지, `use_sim_time`이 제어기에 무엇을 하는지는 Gazebo와 함께 [[04-robotics/ros2/index|25. ROS 2]]에서 온다. Executor 그림을 크게 바꾸는 프로세스 내 통신과 composition은 ROS 2 composition 문서를 보라.

### 출처

- ROS 2 Jazzy 문서 — Concepts: Quality of Service settings(정책, 프로파일, 호환성 표, QoS 이벤트, matched 이벤트).
- ROS 2 Jazzy 문서 — Concepts: Executors(executor 종류, 콜백 그룹, wait set, 스케줄링 의미).
- ROS 2 Jazzy 문서 — How-to Guides: Using Callback Groups(교착 예제, 동작하는 구성과 동작하지 않는 구성).
- ROS 2 Jazzy 문서 — Tutorials: Using quality-of-service settings for lossy networks.
- ROS 2 design article — Clock and Time(SystemTime, SteadyTime, ROSTime, `/clock` 시간 소스, `use_sim_time`, 시간 점프).
- 그대로 인용한 값과 메시지의 출처(Jazzy 브랜치 소스): `rmw/qos_profiles.h`(프로파일 내용), `rclcpp/subscription_base.cpp`와 `publisher_base.cpp`, `rclpy/event_handler.py`(기본 incompatible-QoS 경고), `rclpy/topic_endpoint_info.py`(`--verbose` 출력 형식), `ros2cli/ros2topic`(QoS 플래그와 `echo`의 퍼블리셔 맞춤 동작), `ros2bag` play verb(`--clock`), `robot_state_publisher`와 `nav2_map_server`(transient local 퍼블리셔).
- Daniel Casini, Tobias Blass, Ingo Lütkebohle, Björn Brandenburg, "Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling", ECRTS 2019.

> [!question]- 스스로 점검 · 정답
> **1. 퍼블리셔가 reliable을 offer하고 서브스크립션이 best effort를 request한다. 연결되는가, 그리고 반대 경우는 왜 다른가?** 연결된다. 요청은 서브스크립션이 받아들일 최소 품질이고 제공은 퍼블리셔가 낼 수 있는 최대 품질이므로, reliable 퍼블리셔는 best effort 요청을 넘치게 만족시킨다. 반대 — best effort 퍼블리셔와 reliable 서브스크립션 — 는 제공되지 않는 보장을 요구하므로 연결이 만들어지지 않고 메시지가 하나도 오가지 않는다.
> **2. 내 노드는 `/map`을 구독하는데 아무것도 못 받고, `ros2 topic echo /map`은 지도를 바로 찍는다. 무슨 일인가?** 거의 확실히 durability다. map server는 transient local로, 내 노드가 뜨기 전에 한 번 발행했다. 내 노드는 기본 volatile을 요청하므로 연결은 정당하게 되지만 새 메시지만 받는다. `ros2 topic echo`는 퍼블리셔를 조사해 자기 요청을 transient local로 맞추므로 보존된 샘플을 받는다. 구독 쪽을 transient local로 고치고, `echo`가 된다고 해서 내 노드가 받을 수 있다는 증명이 되지는 않는다는 것을 기억하라.
> **3. 노드를 `MultiThreadedExecutor`에 올렸는데도 타이머 안의 동기 서비스 호출이 여전히 교착한다. 왜인가?** 콜백 그룹을 지정하지 않았기 때문이다. 그룹 없이 만든 것은 전부 노드 기본 그룹에 들어가고 그것은 mutually exclusive이므로, 노드는 단일 스레드처럼 동작한다. 타이머 콜백이 기다리는 동안 그룹을 붙들고 있고, 결과가 나오려면 실행되어야 하는 future의 숨은 done-callback은 같은 mutually exclusive 그룹에서 스케줄될 수 없다. 클라이언트와 타이머를 다른 그룹에 두거나, 공유된 reentrant 그룹 하나에 두어라.
> **4. 어떤 노드가 `time.time()`으로 메시지에 스탬프를 찍는다. 실험실에서는 잘 되는데 bag 재생에서는 숫자가 틀린다. 정확히 무엇이 잘못됐고, 무엇을 불러야 하나?** `time.time()`은 벽시계이고 `/clock`을 완전히 무시한다. 그래서 재생에서는 2년 전에 기록된 데이터에 오늘 시각을 찍고, 시뮬레이션에서는 시스템 나머지에 대해 실시간 계수만큼 어긋난다. 그러면 하류의 TF 조회와 다른 메시지 스탬프와의 비교가 실패하거나 조용히 외삽한다. 노드 시계의 `self.get_clock().now()`를 부르고 그래프 전체에 `use_sim_time`을 설정해야 하며, 주기가 시뮬레이션 시간을 따라야 한다면 wall timer가 아니라 `create_timer`를 쓴다.
