---
title: "25.3 Services, Actions, Parameters and Lifecycle"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Choose correctly between a topic, a service and an action; configure a node with parameters from a file and the command line; and bring a node up through the managed-node state machine instead of hoping it started in order."
mastery-when: "Go deeper when you are designing the interface another team will depend on, or writing a lifecycle manager rather than using one."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to pick the right communication pattern, write both ends of it, and configure and start a node deterministically. Not enough to design a new action protocol.
> **Working** — 올바른 통신 패턴을 고르고, 양쪽 끝을 직접 작성하고, 노드를 결정론적으로 설정하고 기동할 정도. 새 액션 프로토콜을 설계할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]], and a working installation. Every command here assumes **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, with each terminal sourced (`source /opt/ros/jazzy/setup.bash`).
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]]와 동작하는 설치 환경. 여기의 모든 명령은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**를 전제하고, 터미널마다 `source /opt/ros/jazzy/setup.bash`가 되어 있다고 가정한다.

### 1. Why topics are not enough

A topic is a one-way stream with no reply and no idea who is listening. That is exactly right for a camera, a joint state, a velocity command. It is wrong for three other things a robot constantly needs to do.

**"Compute this and tell me the answer."** Spawning a second turtle, resetting a map, querying an inverse-kinematics solver. You need a reply, and you need to know it answers *your* request. That is a **service**.

**"Do this; it will take a while; keep me posted; I may change my mind."** Drive to the kitchen. Plan and execute an arm trajectory. Ten seconds to ten minutes, with progress, and with the operator able to abort. That is an **action**.

**"Come up configured this way."** Which camera device, which control gains, which frame names — none of which you want in the source. That is **parameters**, and its companion problem — starting a system in a known order, where nothing publishes until its hardware is actually open — is **managed (lifecycle) nodes**.

The distinction beginners get wrong: they reach for a service because it looks simpler than an action, then write a service handler that takes eight seconds. Section 3 is what that costs.

### 2. Services: request and response

A service is a remote procedure call. Its contract lives in a `.srv` file: request fields, then `---`, then response fields. The one used throughout the official tutorials is `example_interfaces/srv/AddTwoInts`:

```text
int64 a
int64 b
---
int64 sum
```

There should only ever be **one service server per service name** — with several, which one receives a request is undefined. There can be any number of clients. This is the opposite of topics, where several publishers on one name is legal (and, as [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot: URDF, TF2 and RViz]] will show, a common way to break a transform tree).

A Python server. The callback receives a filled `request` and an empty `response`, fills the response in, and returns it:

```python
from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response


def main():
    rclpy.init()
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

A Python client. Note `call_async`, which returns a **future** — a handle that will eventually hold the response — rather than the response itself:

```python
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)
```

and in `main`, `rclpy.spin_until_future_complete(minimal_client, future)` before reading `future.result()`. The `wait_for_service` loop matters: unlike a publisher, a client with no server is not merely quiet, it is broken, and you would rather say so than hang.

C++ has **no synchronous service API at all** — `rclcpp` gives you `async_send_request` only. That is not an omission; it is the library refusing to hand you the gun that section 10 is about. The server is the same shape:

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
          std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
{
  response->sum = request->a + request->b;
}

// in main, after rclcpp::init:
//   auto node = rclcpp::Node::make_shared("add_two_ints_server");
//   auto service = node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);
```

From the command line, without writing either end:

```bash
ros2 service list -t
ros2 service type /add_two_ints
ros2 service find example_interfaces/srv/AddTwoInts
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

`ros2 service echo <name>` exists too, but it depends on service introspection, which is **disabled by default** — so an empty `echo` is not evidence that no calls are happening.

### 3. Why a service must be fast

The official concept documentation is blunt: services are expected to return quickly, because the client is generally waiting, and they should *never* be used for long-running processes — especially ones that might need to be preempted.

There is a mechanical reason as well as a design one. By default a node runs on a **single-threaded executor**: one thread pulls one ready callback at a time and runs it to completion. A service callback that takes eight seconds is eight seconds in which that node processes no subscriptions, no timers, and no other service requests. The control loop in the same process stops. Nothing logs a warning; the node simply goes deaf. The executor mechanism, and the callback groups that change this behaviour, are [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]].

So the rule is not a style preference: **if the work is long, or cancellable, or you want progress, it is an action.**

### 4. Actions: long-running goals

An action is a service that takes time, reports progress, and can be cancelled. Underneath it is built out of topics and services, but you use it as one thing.

Its contract is a `.action` file with three message definitions separated by `---`: goal, result, feedback. The canonical example:

```text
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

The goal is the `order` to compute, the result is the final `sequence`, the feedback is the `partial_sequence` so far. Action definitions must live in a CMake (`ament_cmake`) package — a hard constraint, though a Python node can use the generated type — and are built by passing `"action/Fibonacci.action"` to `rosidl_generate_interfaces`. The full name is then `custom_action_interfaces/action/Fibonacci`.

The goal lifecycle is the part worth memorising, because it is what distinguishes an action from "a slow service":

| Stage | Who decides | What can happen |
|---|---|---|
| Goal sent | client | — |
| Goal accepted or rejected | server | A server may refuse outright — busy, out of range, unsafe |
| Executing | server | Feedback messages stream to the client |
| Cancel requested | client | The server may accept or reject the cancellation |
| Aborted | server | The server gives up, or preempts this goal for a newer one |
| Result | server | Delivered once, with a terminal status: SUCCEEDED, CANCELED or ABORTED |

Every goal gets a unique ID, which is how a client keeps several in flight straight. And "what happens when a second goal arrives" is a **server policy, not a rule**: turtlesim's rotation server aborts the previous goal, but another server may reject the new one or queue it. Do not assume.

This is why navigation and manipulation use actions. Driving to a waypoint takes minutes, the operator must be able to stop it, and the caller needs to know how far along it is — the three things a service cannot do. [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]] is an action interface from top to bottom.

Introspection first, as always:

```bash
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
```

### 5. Writing an action server and client

Python, using the `Fibonacci` action above. The whole of the goal's execution happens inside `execute_callback`, and feedback is pushed by calling `publish_feedback` on the goal handle:

```python
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(FibonacciActionServer())


if __name__ == '__main__':
    main()
```

`goal_handle.succeed()` is not optional decoration. If the execute callback never sets the state, the goal is assumed **aborted**, and you will get a warning and a puzzled client.

The client side is callback-driven, because there are three separate moments to react to — acceptance, feedback, result:

```python
def send_goal(self, order):
    goal_msg = Fibonacci.Goal()
    goal_msg.order = order
    self._action_client.wait_for_server()
    self._send_goal_future = self._action_client.send_goal_async(
        goal_msg, feedback_callback=self.feedback_callback)
    self._send_goal_future.add_done_callback(self.goal_response_callback)

def goal_response_callback(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected :(')
        return
    self._get_result_future = goal_handle.get_result_async()
    self._get_result_future.add_done_callback(self.get_result_callback)
```

Cancellation and rejection need the fuller server form, which takes `goal_callback` (accept or reject the goal), `cancel_callback` (accept or reject a cancellation) and `handle_accepted_callback`, and inside the execution loop checks `goal_handle.is_cancel_requested` and calls `goal_handle.canceled()`.

C++ makes the hazard explicit. `rclcpp_action::create_server` requires those three callbacks, and the accepted-goal callback must return immediately, so the tutorial spawns the work onto its own thread:

```cpp
auto handle_accepted = [this](const std::shared_ptr<GoalHandleFibonacci> goal_handle)
{
  // this needs to return quickly to avoid blocking the executor,
  // so we declare a lambda function to be called inside a new thread
  auto execute_in_thread = [this, goal_handle](){return this->execute(goal_handle);};
  std::thread{execute_in_thread}.detach();
};
```

That comment is section 3, restated by the library's own authors. Python's simple `ActionServer` hides the same hazard — a long `execute_callback` on a single-threaded executor blocks everything else in the node — which is why the `rclpy` examples pair a full action server with a `MultiThreadedExecutor` and a `ReentrantCallbackGroup`.

### 6. Parameters: configuring a node

A parameter is a node setting, owned by that node, living exactly as long as it does. Each is a key, a value, and a **descriptor**. The value is one of nine types and no others: `bool`, `int64`, `float64`, `string`, `byte[]`, `bool[]`, `int64[]`, `float64[]`, `string[]`. No dictionary, no nested struct — `some_lists.some_integers` is a dotted *name*, not a nesting.

A node must **declare** every parameter it will accept, so names and types are fixed at startup rather than discovered by a typo six months later:

```python
class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_parameter', 'world')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info('Hello %s!' % my_param)
```

The type is inferred from the default, and changing a declared parameter's type at runtime **fails** by default — a bool put into an int is caught, not absorbed. (For a genuinely polymorphic parameter, declare it with a descriptor whose `dynamic_typing` is true; for a node whose parameter names are not known in advance, construct it with `allow_undeclared_parameters`.)

The descriptor carries the description, ranges and other constraints, and is where **read-only** lives:

```python
from rcl_interfaces.msg import ParameterDescriptor
my_parameter_descriptor = ParameterDescriptor(description='This parameter is mine!')
self.declare_parameter('my_parameter', 'world', my_parameter_descriptor)
```

C++ is the same idea with more type:

```cpp
auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
param_desc.description = "This parameter is mine!";
this->declare_parameter("my_parameter", "world", param_desc);
// later: std::string p = this->get_parameter("my_parameter").as_string();
```

A read-only parameter can be set at startup and not afterwards. You will meet these without meaning to: every node's `qos_overrides.*` parameters are read-only, which is why `ros2 param load` prints failures for them and succeeds on the rest. Not a bug — the documentation says so explicitly.

To react to changes rather than poll, a node registers a **set-parameters callback** (`add_on_set_parameters_callback`), which inspects a proposed change and may reject it; a **pre-set** callback can amend it, and a **post-set** callback runs once it is accepted. The set callback must have no side effects — several can be chained, and none of them knows whether a later one will reject the update. Do the reacting in the post-set callback.

### 7. Setting parameters from a file and from the command line

Three routes, all of them outside the source code.

From the command line at startup, with `--ros-args -p name:=value`:

```bash
ros2 run demo_nodes_cpp parameter_blackboard --ros-args -p some_int:=42 -p "a_string:=Hello world" -p "some_lists.some_integers:=[1, 2, 3, 4]"
```

From a YAML file at startup. The file is keyed by node name, then the literal key `ros__parameters` (two underscores):

```yaml
parameter_blackboard:
    ros__parameters:
        some_int: 42
        a_string: "Hello world"
        some_lists:
            some_integers: [1, 2, 3, 4]

/**:
  ros__parameters:
    wildcard_full: "Full wildcard for any namespaces and any node names"
```

```bash
ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

`*` matches a single slash-delimited token and `**` matches zero or more, so `/**` is the wildcard every real launch file uses to hand one setting to a whole subsystem. Partial matches such as `foo*` are not allowed. And note the asymmetry that catches people: **a parameter file used at node startup updates all parameters, including the read-only ones** — the thing `ros2 param load` cannot do later.

At runtime, through the parameter services every node creates automatically:

```bash
ros2 param list /minimal_param_node
ros2 param describe /minimal_param_node my_parameter
ros2 param get /minimal_param_node my_parameter
ros2 param set /turtlesim background_r 150
ros2 param dump /turtlesim > turtlesim.yaml
ros2 param load /turtlesim turtlesim.yaml
```

Two traps in `ros2 param set`. The value is parsed as YAML, so `off` becomes a boolean and will be rejected for a string parameter — write `'!!str off'`. And ROS 2 has no heterogeneous lists, so a mixed YAML list is interpreted as a string. `ros2 param dump` piped to a file is the fastest honest way to record the configuration of a run you intend to reproduce.

### 8. Managed (lifecycle) nodes

An ordinary node starts working the moment it is constructed. For a laser, a camera or a motor driver that is wrong: the device takes seconds to boot, and a node that publishes nonsense while it warms up — or opens hardware before the rest of the system is ready — produces failures that look like sensor faults.

A **managed node** (`LifecycleNode`) adds a state machine with four steady **primary states** — `unconfigured`, `inactive`, `active`, `finalized` — and intermediate **transition states** (`configuring`, `activating`, `deactivating`, `cleaningup`, `shuttingdown`) that report whether a transition succeeded. The transitions you invoke are `configure`, `activate`, `deactivate`, `cleanup`, `shutdown`.

Each transition runs a callback you override: `on_configure` (allocate, open the device, create publishers and timers), `on_activate` (start publishing), `on_deactivate` (stop), `on_cleanup` (release), `on_shutdown`. All default to success, so a node can be managed without overriding anything. `on_error` is the exception: it runs when a transition throws, and **only** if it returns success does the machine fall back to `unconfigured` — by default it returns failure and the node goes to `finalized`. A node that keeps ending up finalized after a hiccup is telling you it has no error handler.

The payoff is that publishing is gated by state. A lifecycle publisher created in `on_configure` exists in `inactive` but transfers nothing; `publish()` is a no-op until the node is `active`. Nothing downstream sees half-initialised data.

Every managed node exposes six interfaces for free: a `<node_name>/transition_event` topic, and services `get_state`, `change_state`, `get_available_states`, `get_available_transitions`. The CLI wraps them:

```bash
ros2 lifecycle nodes
ros2 lifecycle list /lc_talker
ros2 lifecycle get /lc_talker
ros2 lifecycle set /lc_talker configure
ros2 lifecycle set /lc_talker activate
```

Run `ros2 launch lifecycle lifecycle_demo_launch.py`, or the executables `lifecycle_talker`, `lifecycle_listener` and `lifecycle_service_client` in three terminals. The talker prints nothing at first — it starts `unconfigured`, exactly as designed.

In Python the node subclasses `rclpy.lifecycle.Node` (an alias for `LifecycleNode`), overrides `on_configure` and friends to return `TransitionCallbackReturn.SUCCESS`, and creates its publisher with `create_lifecycle_publisher`. In C++ it derives from `rclcpp_lifecycle::LifecycleNode` and the callbacks return `LifecycleNodeInterface::CallbackReturn`.

This is not academic: **Nav2 is built on it**, and you will meet it in [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]]. Its `map_server`, `planner_server` and `controller_server` are lifecycle-enabled, and `nav2_lifecycle_manager` drives them through `configure` and `activate` in ordered groups on startup, and in reverse on shutdown, via a `lifecycle_manager/manage_nodes` service. It also holds a **bond** with each server, so a node that crashes after activation is noticed and the stack is brought down rather than left half-running; `bond_timeout` (default 4.0 s) is how long it waits. When Nav2 "does nothing" on startup, ask which state its servers are in — `ros2 lifecycle get` answers in one line.

### 9. Exercise: an action server that reports feedback

One sitting. Work in the `ros2_ws` from 25.2; building and sourcing workspaces is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]] if this is unfamiliar.

1. Create the interface package and the action:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces
mkdir custom_action_interfaces/action
```

Put the section 4 definition in `action/Fibonacci.action`; add `find_package(rosidl_default_generators REQUIRED)` and the `rosidl_generate_interfaces` block to `CMakeLists.txt` before `ament_package()`; add `<buildtool_depend>rosidl_default_generators</buildtool_depend>` and `<member_of_group>rosidl_interface_packages</member_of_group>` to `package.xml`; then `colcon build` from `~/ros2_ws` and `source install/local_setup.bash`.

2. Confirm the contract exists before writing code against it:

```bash
ros2 interface show custom_action_interfaces/action/Fibonacci
```

3. Save the section 5 server as `fibonacci_action_server.py` and run it with `python3 fibonacci_action_server.py`.

4. In a second terminal, send a goal *without* feedback, then with it:

```bash
ros2 action send_goal fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
```

The first prints the goal ID, waits about four seconds in silence, then prints the result and `SUCCEEDED`. The loop is `range(1, order)`, so `order: 5` gives four iterations of one second each. The second prints one `Feedback:` block per iteration — four of them — as `partial_sequence` grows. That difference *is* the argument for actions: same computation, but the caller can see inside it.

5. In a third terminal, watch the graph while a goal runs: `ros2 action list -t`, then `ros2 action info /fibonacci`.

6. Raise `order` to 30 and press Ctrl+C in the client mid-goal. The server keeps computing. Cancellation is a request the *server* must handle, not something a client can impose — which is why the full server form in section 5 exists.

You are done when you can say what each of the three parts of the `.action` file does, and why `--feedback` changes nothing on the server side.

### 10. The failure to diagnose: a service call inside a callback

A node subscribes to a trigger topic and, on each message, calls a service. In Python you used the synchronous `call()` because it reads better. The first message arrives and the node stops. Forever.

The symptom is the worst kind: **no error**. The official documentation states it plainly — no warning, no exception, nothing in a stack trace, and the call does not fail. The process is alive, the node is in the graph, and nothing happens.

```python
def trigger_request(msg):
    response = minimal_client.send_request()  # This will cause deadlock
```

The mechanism: `call()` blocks the thread until the response arrives, but the response can only be delivered by the executor spinning on *that same thread* — and that thread is inside your callback. The executor cannot preempt a running callback. The client waits for a response that only the waiter could deliver.

What finds it:

```bash
ros2 node list                  # the node is there
ros2 node info /your_node       # its subscriptions and service clients are all present
ros2 topic hz /its_output       # nothing — no messages arriving
ros2 service list | grep add_two_ints   # the server exists and is fine
```

Alive in the graph, producing nothing, with a healthy server on the other end — that combination is the signature. Distinguish it from a QoS mismatch (also silent) by checking whether the node produced output *before* the trigger arrived: a deadlocked node worked until the first trigger, a mismatched one never worked at all.

Three fixes, in order of preference. Use `call_async` and handle the future in a callback, which is safe from anywhere. Keep the call synchronous but put the service work in a different **callback group** and run a multi-threaded executor. Or follow the documented pattern: spin in a separate thread and call from `main`, never from a callback. The executor and callback-group machinery behind all three is [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. C++ gets this for free — `rclcpp` has no synchronous service API to misuse.

### 11. What this page does not cover

Custom `.srv` and `.action` packages appear here only far enough to build one; the general interface-definition rules, and starting all of this from a launch file with parameters attached instead of six terminals, are [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. Executors, callback groups and the QoS settings that make services and actions connect at all are [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. Actions as a system interface — a behaviour tree calling them, a lifecycle manager sequencing the servers — arrive in [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]]. The rest of the track is [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Concepts: Services; Actions; Parameters.
- ROS 2 Jazzy documentation — Tutorials: Understanding services; Understanding parameters; Understanding actions; Writing a simple service and client (Python and C++); Creating an action; Writing an action server and client (Python and C++); Using parameters in a class (Python and C++); Managing node lifecycles.
- ROS 2 Jazzy documentation — How-to guides: Synchronous vs. asynchronous service clients; Using the `ros2 param` command-line tool; Passing ROS arguments to nodes via the command-line.
- ros2/demos — `lifecycle` package README (primary and transition states, transition callbacks, the five lifecycle interfaces); `lifecycle_py/lifecycle_py/talker.py`.
- ros2/examples — `rclpy/actions/minimal_action_server` (goal, cancel and accepted callbacks).
- ros2/ros2cli — `ros2lifecycle` verbs (`nodes`, `list`, `get`, `set`).
- ros-navigation/navigation2 — `nav2_lifecycle_manager` README and `lifecycle_manager.cpp` (ordered bringup, `manage_nodes` service, `bond_timeout` default).

> [!question]- Self-check · Answer
> **1. You need a node to run a 30-second global plan on request. Service or action, and why?** Action. A service blocks the caller and cannot be preempted, and on a single-threaded executor a 30-second service callback stops every other callback in that node — timers, subscriptions, other services. Official guidance is that services return quickly and long work belongs in an action, which also gives you feedback and a cancellation path.
> **2. `ros2 param load /my_node params.yaml` reports "successful" for some parameters and "cannot be set because it is read-only" for others. Is something broken?** No. Read-only parameters can only be set at startup, and `qos_overrides.*` are read-only on every node, so a dump-then-load round trip always prints those failures. To apply them, pass the same file at startup with `--ros-args --params-file`, which does update read-only parameters.
> **3. A node you wrote is in `ros2 node list`, its service client and subscription show in `ros2 node info`, the server it calls is running, and it emits nothing after the first input. What is your first hypothesis?** A synchronous service call from inside a callback. The executor cannot preempt the running callback to deliver the response, so the call waits forever — no exception, no warning, no failure. Confirm by checking that the node produced output before the first trigger; fix with `call_async`, or a separate callback group plus a multi-threaded executor.
> **4. Why does Nav2 use lifecycle nodes instead of ordinary ones?** Because bringup order matters and partial startup is dangerous. The lifecycle manager transitions the servers through `configure` and `activate` in ordered groups (reverse on shutdown), so nothing publishes or accepts goals before its resources exist, then holds a bond with each so a crash after activation brings the stack down deterministically. `ros2 lifecycle get <node>` is the one-line answer to "why is Nav2 doing nothing".

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 올바른 통신 패턴을 고르고, 양쪽 끝을 직접 작성하고, 노드를 결정론적으로 설정하고 기동할 정도. 새 액션 프로토콜을 설계할 정도는 아니다.
> **Working** — enough to pick the right pattern, write both ends, and start a node deterministically.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]]와 동작하는 설치 환경. 여기의 모든 명령은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**를 전제하고, 터미널마다 `source /opt/ros/jazzy/setup.bash`가 되어 있다고 가정한다.
> 25.2 and a working install; all commands assume ROS 2 Jazzy on Ubuntu 24.04, each terminal sourced.

### 1. 토픽만으로 부족한 이유

토픽은 응답이 없고 누가 듣는지도 모르는 단방향 스트림이다. 카메라, 관절 상태, 속도 명령에는 정확히 맞다. 로봇이 늘 해야 하는 다른 세 가지에는 맞지 않는다.

**"이걸 계산해서 답을 달라."** 거북이 하나 더 띄우기, 지도 초기화, 역기구학 솔버 질의. 응답이 필요하고, 그 응답이 남의 요청이 아니라 *내* 요청의 것임을 알아야 한다. 이것이 **서비스**다.

**"이걸 해라. 오래 걸린다. 진행 상황을 알려 달라. 중간에 마음이 바뀔 수도 있다."** 주방까지 주행. 팔 궤적 계획과 실행. 10초에서 10분, 진행 보고가 있고, 조작자가 중단할 수 있어야 한다. 이것이 **액션**이다.

**"이런 설정으로 떠라."** 어느 카메라 장치, 어느 제어 게인, 어느 프레임 이름. 소스에 박고 싶지 않다. 이것이 **파라미터**이고, 그 짝이 되는 문제 — 하드웨어가 실제로 열리기 전에는 아무것도 발행하지 않는 상태로, 알려진 순서대로 시스템을 띄우는 일 — 이 **관리형(라이프사이클) 노드**다.

초심자가 틀리는 구분: 액션보다 간단해 보인다는 이유로 서비스를 고르고, 8초 걸리는 서비스 핸들러를 쓴다. 그 대가가 3절이다.

### 2. 서비스: 요청과 응답

서비스는 원격 프로시저 호출이다. 계약은 `.srv` 파일에 있다. 요청 필드, `---`, 응답 필드. 공식 튜토리얼 전체가 쓰는 `example_interfaces/srv/AddTwoInts`:

```text
int64 a
int64 b
---
int64 sum
```

한 서비스 이름당 **서버는 단 하나**여야 한다. 여럿이면 어느 서버가 요청을 받을지 정의되어 있지 않다. 클라이언트는 몇 개든 된다. 토픽과 정반대다. 토픽은 한 이름에 퍼블리셔가 여럿이어도 합법이고, [[04-robotics/ros2/describing-a-robot|25.6 로봇 기술하기: URDF, TF2, RViz]]에서 보듯 그것이 변환 트리를 깨는 흔한 방법이다.

Python 서버. 콜백은 채워진 `request`와 빈 `response`를 받아, 응답을 채우고 반환한다.

```python
from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response


def main():
    rclpy.init()
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

Python 클라이언트. `call_async`는 응답 자체가 아니라 **future**(언젠가 응답을 담을 손잡이)를 돌려준다.

```python
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)
```

`main`에서는 `future.result()`를 읽기 전에 `rclpy.spin_until_future_complete(minimal_client, future)`를 호출한다. `wait_for_service` 루프가 중요하다. 퍼블리셔와 달리 서버 없는 클라이언트는 조용한 것이 아니라 고장 난 것이고, 매달리는 것보다 그렇게 말하는 편이 낫다.

C++에는 **동기 서비스 API가 아예 없다.** `rclcpp`는 `async_send_request`만 준다. 빠뜨린 것이 아니라, 10절이 다루는 총을 건네기를 거부한 것이다. C++ 서버는 모양이 같다.

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
          std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
{
  response->sum = request->a + request->b;
}

// main에서 rclcpp::init 뒤에:
//   auto node = rclcpp::Node::make_shared("add_two_ints_server");
//   auto service = node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);
```

양쪽 다 안 쓰고 커맨드라인에서:

```bash
ros2 service list -t
ros2 service type /add_two_ints
ros2 service find example_interfaces/srv/AddTwoInts
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

`ros2 service echo <name>`도 있지만 서비스 introspection에 의존하고 그것은 **기본적으로 꺼져 있다.** 즉 `echo`가 비어 있다고 호출이 없다는 증거가 되지 않는다.

### 3. 서비스가 빨라야 하는 이유

공식 개념 문서는 단호하다. 클라이언트가 대개 기다리고 있으므로 서비스는 빨리 반환해야 하고, 장시간 프로세스에는 *절대* 쓰지 말아야 한다. 특히 선점이 필요할 수 있는 작업에는 그렇다.

설계상의 이유만이 아니라 기계적인 이유도 있다. 기본적으로 노드는 **단일 스레드 executor** 위에서 돈다. 스레드 하나가 준비된 콜백을 하나씩 꺼내 끝까지 실행한다. 8초 걸리는 서비스 콜백은 그 노드가 구독도, 타이머도, 다른 서비스 요청도 처리하지 않는 8초다. 같은 프로세스의 제어 루프가 멈춘다. 경고 로그는 없다. 노드가 그냥 귀를 닫는다. executor 기전과 이 동작을 바꾸는 콜백 그룹은 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executor, 시간]]에 있다.

그러니 이 규칙은 취향이 아니다. **오래 걸리거나, 취소 가능해야 하거나, 진행 상황이 필요하면 액션이다.**

### 4. 액션: 장시간 목표

액션은 시간이 걸리고, 진행을 보고하고, 취소할 수 있는 서비스다. 내부는 토픽과 서비스로 만들어져 있지만, 쓸 때는 하나로 쓴다.

계약은 `---`로 구분된 메시지 정의 세 개가 든 `.action` 파일이다. 목표(goal), 결과(result), 피드백(feedback). 표준 예제:

```text
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

목표는 계산할 `order`, 결과는 최종 `sequence`, 피드백은 지금까지의 `partial_sequence`다. 액션 정의는 CMake(`ament_cmake`) 패키지에 있어야 한다. 이것은 강한 제약이지만 Python 노드가 그 결과물을 쓰는 것은 된다. 빌드는 `rosidl_generate_interfaces`에 `"action/Fibonacci.action"`을 넘겨서 한다. 전체 이름은 `custom_action_interfaces/action/Fibonacci`가 된다.

목표의 생애주기는 외워 둘 만하다. 액션을 "느린 서비스"와 구별해 주는 것이 바로 이것이다.

| 단계 | 결정 주체 | 일어날 수 있는 일 |
|---|---|---|
| 목표 전송 | 클라이언트 | — |
| 목표 수락 또는 거부 | 서버 | 서버는 거절할 수 있다 — 바쁨, 범위 밖, 위험 |
| 실행 중 | 서버 | 피드백 메시지가 클라이언트로 흐른다 |
| 취소 요청 | 클라이언트 | 서버가 취소를 수락하거나 거부한다 |
| 중단(abort) | 서버 | 서버가 포기하거나, 새 목표를 위해 이 목표를 선점한다 |
| 결과 | 서버 | 한 번 전달되며 종단 상태가 붙는다: SUCCEEDED, CANCELED, ABORTED |

모든 목표에는 고유 ID가 붙고, 클라이언트는 그것으로 여러 목표를 구분한다. 그리고 "두 번째 목표가 오면 어떻게 되는가"는 **규칙이 아니라 서버 정책이다.** turtlesim의 회전 서버는 이전 목표를 중단하지만, 다른 서버는 새 목표를 거부하거나 대기시킬 수 있다. 가정하지 마라.

내비게이션과 매니퓰레이션이 액션을 쓰는 이유가 이것이다. 경유점까지 주행은 몇 분이 걸리고, 조작자가 멈출 수 있어야 하고, 호출자는 얼마나 진행됐는지 알아야 한다. 셋 다 정확히 서비스가 못 하는 것이다. [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]은 위에서 아래까지 액션 인터페이스다.

늘 그렇듯 내성 먼저:

```bash
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
```

### 5. 액션 서버와 클라이언트 작성

Python, 위의 `Fibonacci` 액션으로. 목표 실행 전체가 `execute_callback` 안에서 일어나고, 피드백은 goal handle의 `publish_feedback`으로 내보낸다.

```python
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(FibonacciActionServer())


if __name__ == '__main__':
    main()
```

`goal_handle.succeed()`는 장식이 아니다. execute 콜백이 상태를 설정하지 않으면 목표는 **중단(aborted)** 으로 간주되고, 경고와 어리둥절한 클라이언트를 얻는다.

클라이언트 쪽은 콜백 구동이다. 반응해야 할 순간이 수락, 피드백, 결과로 셋이기 때문이다.

```python
def send_goal(self, order):
    goal_msg = Fibonacci.Goal()
    goal_msg.order = order
    self._action_client.wait_for_server()
    self._send_goal_future = self._action_client.send_goal_async(
        goal_msg, feedback_callback=self.feedback_callback)
    self._send_goal_future.add_done_callback(self.goal_response_callback)

def goal_response_callback(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected :(')
        return
    self._get_result_future = goal_handle.get_result_async()
    self._get_result_future.add_done_callback(self.get_result_callback)
```

취소와 거부에는 더 완전한 서버 형태가 필요하다. `goal_callback`(수락/거부), `cancel_callback`(취소 수락/거부), `handle_accepted_callback`을 받고, 실행 루프 안에서 `goal_handle.is_cancel_requested`를 검사해 `goal_handle.canceled()`를 부른다.

C++ 쪽이 교훈적이다. `rclcpp_action::create_server`는 그 세 콜백을 명시적으로 받고, 수락된 목표 콜백은 즉시 반환해야 하므로 튜토리얼은 작업을 별도 스레드로 던진다.

```cpp
auto handle_accepted = [this](const std::shared_ptr<GoalHandleFibonacci> goal_handle)
{
  // this needs to return quickly to avoid blocking the executor,
  // so we declare a lambda function to be called inside a new thread
  auto execute_in_thread = [this, goal_handle](){return this->execute(goal_handle);};
  std::thread{execute_in_thread}.detach();
};
```

저 주석은 라이브러리를 쓴 사람들이 3절을 다시 말한 것이다. Python의 간단한 `ActionServer` 형태는 같은 위험을 감춘다. 단일 스레드 executor에서 긴 `execute_callback`은 그 노드의 나머지 전부를 막는다. `rclpy` 예제가 완전한 액션 서버에 `MultiThreadedExecutor`와 `ReentrantCallbackGroup`을 짝지어 두는 이유다.

### 6. 파라미터: 노드 설정하기

파라미터는 노드의 설정값이고, 그 노드가 소유하며, 정확히 그 노드만큼 산다. 각각은 키, 값, **디스크립터**로 이루어진다. 값의 타입은 아홉 가지뿐이다. `bool`, `int64`, `float64`, `string`, `byte[]`, `bool[]`, `int64[]`, `float64[]`, `string[]`. 사전도 중첩 구조체도 없다. `some_lists.some_integers`는 점이 들어간 *이름*이지 중첩이 아니다.

노드는 받아들일 모든 파라미터를 **선언(declare)** 해야 한다. 그래야 이름과 타입이 반년 뒤 오타로 발견되지 않고 기동 시점에 고정된다.

```python
class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_parameter', 'world')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info('Hello %s!' % my_param)
```

타입은 기본값에서 추론되고, 선언된 파라미터의 타입을 런타임에 바꾸려는 시도는 기본적으로 **실패한다.** 불리언을 정수에 넣는 실수가 흡수되지 않고 잡힌다. (정말로 다형적 파라미터가 필요하면 `dynamic_typing`이 참인 디스크립터로 선언하고, 이름을 미리 알 수 없는 노드는 `allow_undeclared_parameters`로 생성한다.)

디스크립터는 설명, 범위, 그 밖의 제약을 담고, **읽기 전용**이 사는 곳이다.

```python
from rcl_interfaces.msg import ParameterDescriptor
my_parameter_descriptor = ParameterDescriptor(description='This parameter is mine!')
self.declare_parameter('my_parameter', 'world', my_parameter_descriptor)
```

C++은 같은 생각에 타입이 더 붙는다.

```cpp
auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
param_desc.description = "This parameter is mine!";
this->declare_parameter("my_parameter", "world", param_desc);
// 나중에: std::string p = this->get_parameter("my_parameter").as_string();
```

읽기 전용 파라미터는 기동 시에만 설정할 수 있고 그 뒤에는 안 된다. 의도하지 않아도 만나게 된다. 모든 노드의 `qos_overrides.*` 파라미터가 읽기 전용이고, 그래서 `ros2 param load`가 그것들에 대해 실패를 찍고 나머지는 성공한다. 버그가 아니며 문서에 그렇게 적혀 있다.

폴링 대신 변경에 반응하려면, 제안된 변경을 검사하고 거부할 수 있는 **set-parameters 콜백**(`add_on_set_parameters_callback`), 변경을 수정할 수 있는 **pre-set** 콜백, 변경이 수락된 *뒤에* 도는 **post-set** 콜백을 등록할 수 있다. set 콜백에는 부작용이 없어야 한다. 여러 개가 사슬로 이어질 수 있고, 개별 콜백은 뒤의 콜백이 갱신을 거부할지 알 수 없다. 반응은 post-set 콜백에서 하라.

### 7. 파일과 커맨드라인으로 파라미터 설정하기

세 가지 경로, 모두 소스 코드 바깥이다.

기동 시 커맨드라인에서 `--ros-args -p 이름:=값`으로:

```bash
ros2 run demo_nodes_cpp parameter_blackboard --ros-args -p some_int:=42 -p "a_string:=Hello world" -p "some_lists.some_integers:=[1, 2, 3, 4]"
```

기동 시 YAML 파일로. 파일은 노드 이름, 그다음 리터럴 키 `ros__parameters`(밑줄 두 개)로 키를 잡는다.

```yaml
parameter_blackboard:
    ros__parameters:
        some_int: 42
        a_string: "Hello world"
        some_lists:
            some_integers: [1, 2, 3, 4]

/**:
  ros__parameters:
    wildcard_full: "Full wildcard for any namespaces and any node names"
```

```bash
ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

`*`는 슬래시로 구분된 토큰 하나에, `**`는 0개 이상의 토큰에 대응한다. 그래서 실제 런치 파일은 하위 시스템 전체에 설정 하나를 주려고 `/**`를 쓴다. `foo*` 같은 부분 일치는 허용되지 않는다. 그리고 사람들이 걸리는 비대칭: **기동 시에 쓰는 파라미터 파일은 읽기 전용 파라미터를 포함해 모든 파라미터를 갱신한다.** 나중에 `ros2 param load`로는 못 하는 일이다.

런타임에는 모든 노드가 자동으로 만드는 파라미터 서비스를 통해:

```bash
ros2 param list /minimal_param_node
ros2 param describe /minimal_param_node my_parameter
ros2 param get /minimal_param_node my_parameter
ros2 param set /turtlesim background_r 150
ros2 param dump /turtlesim > turtlesim.yaml
ros2 param load /turtlesim turtlesim.yaml
```

`ros2 param set`의 함정 둘. 값은 YAML로 파싱되므로 `off`는 불리언이 되고 문자열 파라미터에는 거부된다. `'!!str off'`라고 써라. 그리고 ROS 2에는 이종(heterogeneous) 리스트가 없어서, 타입이 섞인 YAML 리스트는 문자열로 해석된다. `ros2 param dump`를 파일로 보내는 것은 재현할 실행의 설정을 기록하는 가장 빠르고 정직한 방법이다.

### 8. 관리형(라이프사이클) 노드

보통 노드는 생성되는 순간부터 제 일을 시작한다. 레이저, 카메라, 모터 드라이버에는 그것이 틀렸다. 장치는 부팅에 몇 초가 걸리고, 예열 중에 헛소리를 발행하거나 시스템의 나머지가 준비되기 전에 하드웨어를 여는 노드는 센서 고장처럼 보이는 실패를 만든다.

**관리형 노드**(`LifecycleNode`)는 상태 기계를 더한다. 네 개의 안정적인 **주 상태** — `unconfigured`, `inactive`, `active`, `finalized` — 와, 전이 성공 여부를 알리는 **전이 상태**(`configuring`, `activating`, `deactivating`, `cleaningup`, `shuttingdown`). 호출하는 전이는 `configure`, `activate`, `deactivate`, `cleanup`, `shutdown`이다.

전이마다 재정의할 콜백이 돈다. `on_configure`(할당, 장치 열기, 퍼블리셔와 타이머 생성), `on_activate`(발행 시작), `on_deactivate`(중지), `on_cleanup`(해제), `on_shutdown`. 전부 기본 반환이 성공이라, 아무것도 재정의하지 않아도 관리형 노드가 된다. `on_error`만 예외다. 전이가 예외를 던지면 호출되고, 그것이 성공을 반환할 때에만 상태 기계가 `unconfigured`로 돌아간다. 기본값은 실패이고 그러면 노드는 `finalized`로 간다. 한 번 삐끗한 뒤 자꾸 finalized에 머무는 노드는 오류 처리기가 없다고 말하는 중이다.

이득은 발행이 상태로 게이팅된다는 것이다. `on_configure`에서 만든 라이프사이클 퍼블리셔는 `inactive`에 존재하지만 아무것도 전달하지 않는다. 노드가 `active`가 되기 전까지 `publish()`는 아무 일도 하지 않는다. 하류의 누구도 반쯤 초기화된 데이터를 보지 않는다.

모든 관리형 노드는 여섯 가지 인터페이스를 공짜로 노출한다. `<node_name>/transition_event` 토픽, 그리고 `get_state`, `change_state`, `get_available_states`, `get_available_transitions` 서비스. CLI가 그것을 감싼다.

```bash
ros2 lifecycle nodes
ros2 lifecycle list /lc_talker
ros2 lifecycle get /lc_talker
ros2 lifecycle set /lc_talker configure
ros2 lifecycle set /lc_talker activate
```

돌려 볼 데모는 `ros2 launch lifecycle lifecycle_demo_launch.py`, 또는 터미널 셋에 `lifecycle_talker`, `lifecycle_listener`, `lifecycle_service_client`. talker는 처음에 아무것도 찍지 않는다. 설계대로 `unconfigured`로 시작하기 때문이다.

Python에서는 `rclpy.lifecycle.Node`(`LifecycleNode`의 별칭)를 상속하고, `on_configure` 등을 재정의해 `TransitionCallbackReturn.SUCCESS`를 반환하고, 퍼블리셔를 `create_lifecycle_publisher`로 만든다. C++에서는 `rclcpp_lifecycle::LifecycleNode`를 상속하고 콜백은 `LifecycleNodeInterface::CallbackReturn`을 반환한다.

학술적인 이야기가 아니다. **Nav2가 이 위에 세워져 있고**, [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]에서 만나게 된다. `map_server`, `planner_server`, `controller_server`가 라이프사이클 노드이고, `nav2_lifecycle_manager`가 `lifecycle_manager/manage_nodes` 서비스를 통해 기동 시 순서 지어진 그룹으로 `configure`와 `activate`를, 종료 시에는 역순으로 몰아간다. 또 각 서버와 **bond**를 유지해서, 활성화 뒤에 죽은 노드를 알아채고 반쯤 돌아가는 상태로 두는 대신 스택 전체를 내린다. `bond_timeout`(기본 4.0초)이 판단까지 기다리는 시간이다. Nav2가 기동 후 "아무것도 안 할" 때 첫 질문은 서버들이 어느 상태인가이고, `ros2 lifecycle get`이 한 줄로 답한다.

### 9. 실습: 피드백을 보고하는 액션 서버

한 번에 앉아서. 25.2의 `ros2_ws`에서 작업한다. 워크스페이스 빌드와 source가 낯설면 [[04-robotics/ros2/workspaces-packages-launch|25.4 워크스페이스, 패키지, 빌드, 런치]]를 보라.

1. 인터페이스 패키지와 액션을 만든다.

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces
mkdir custom_action_interfaces/action
```

4절의 3부 정의를 `action/Fibonacci.action`에 넣고, `CMakeLists.txt`의 `ament_package()` 앞에 `find_package(rosidl_default_generators REQUIRED)`와 `rosidl_generate_interfaces` 블록을 추가하고, `package.xml`에 `<buildtool_depend>rosidl_default_generators</buildtool_depend>`와 `<member_of_group>rosidl_interface_packages</member_of_group>`를 추가한 뒤, `~/ros2_ws`에서 `colcon build`하고 `source install/local_setup.bash`.

2. 코드를 쓰기 전에 계약이 존재하는지 확인한다.

```bash
ros2 interface show custom_action_interfaces/action/Fibonacci
```

3. 5절의 서버를 `fibonacci_action_server.py`로 저장하고 `python3 fibonacci_action_server.py`로 실행한다.

4. 두 번째 터미널에서 피드백 *없이* 목표를 보내고, 그다음 피드백과 함께 보낸다.

```bash
ros2 action send_goal fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
```

첫 번째는 목표 ID를 찍고, 약 4초간 조용히 기다리다가, 결과와 `SUCCEEDED`를 찍는다. 루프가 `range(1, order)`라서 `order: 5`면 1초짜리 반복이 네 번이다. 두 번째는 반복마다 `Feedback:` 블록을 하나씩, 그러니까 넷을 찍는다. 그 차이가 액션을 쓰는 논거 자체다. 계산은 같은데, 호출자가 이제 그 안을 볼 수 있다.

5. 세 번째 터미널에서 목표가 도는 동안 그래프를 본다. `ros2 action list -t`, 그다음 `ros2 action info /fibonacci`.

6. `order`를 30으로 올리고 목표 중간에 클라이언트에서 Ctrl+C를 누른다. 서버는 계속 계산한다. 취소는 *서버가* 처리해야 하는 요청이지 클라이언트가 강제할 수 있는 것이 아니다. 5절의 완전한 서버 형태가 존재하는 이유다.

`.action` 파일의 세 부분이 각각 무엇을 하는지, 그리고 `--feedback`이 서버 쪽에서는 왜 아무것도 바꾸지 않는지 말할 수 있으면 끝난 것이다.

### 10. 진단할 실패: 콜백 안에서 한 서비스 호출

트리거 토픽을 구독하다가 메시지마다 서비스를 호출하는 노드가 있다. Python에서 읽기 좋다는 이유로 동기 `call()`을 쓴다. 첫 메시지가 도착하고 노드가 멈춘다. 영원히.

증상이 최악의 종류다. **오류가 없다.** 공식 문서가 그대로 적어 두었다. 경고도, 예외도, 스택 트레이스에 남는 것도 없고, 호출이 실패하지도 않는다. 프로세스는 살아 있고, 노드는 그래프에 있고, 아무 일도 일어나지 않는다.

```python
def trigger_request(msg):
    response = minimal_client.send_request()  # This will cause deadlock
```

기전은 이렇다. `call()`은 응답이 올 때까지 스레드를 막는데, 응답을 전달할 수 있는 것은 *바로 그 스레드* 위에서 도는 executor뿐이고, 그 스레드는 지금 당신의 콜백 안에 있다. executor는 실행 중인 콜백을 선점하지 못한다. 클라이언트는 기다리는 자만이 전달할 수 있는 응답을 기다린다.

무엇이 찾아내는가:

```bash
ros2 node list                  # 노드는 있다
ros2 node info /your_node       # 구독과 서비스 클라이언트가 다 보인다
ros2 topic hz /its_output       # 아무것도 없음 — 메시지가 오지 않는다
ros2 service list | grep add_two_ints   # 서버는 멀쩡히 있다
```

그래프에 살아 있고, 아무것도 생산하지 않고, 반대편 서버는 건강하다. 이 조합이 서명이다. 역시 조용한 QoS 불일치와 구별하려면 트리거가 오기 *전에* 노드가 출력을 냈는지 보라. 데드락 난 노드는 첫 트리거까지는 동작했고, 불일치 난 노드는 처음부터 한 번도 동작하지 않았다.

고치는 방법 셋, 선호 순서대로. `call_async`를 쓰고 future를 콜백에서 처리한다. 어디서 불러도 안전하다. 호출을 동기로 두되 서비스 작업을 다른 **콜백 그룹**에 넣고 다중 스레드 executor를 돌린다. 정 필요하면 문서화된 패턴을 따른다. 별도 스레드에서 spin하고 `main`에서 호출하되, 콜백에서는 절대 부르지 않는다. 셋 모두의 바탕인 executor와 콜백 그룹 기계는 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executor, 시간]]에 있다. C++ 사용자는 공짜로 안전하다. `rclcpp`에는 오용할 동기 서비스 API가 없다.

### 11. 이 페이지가 다루지 않는 것

커스텀 `.srv`와 `.action` 패키지는 여기서 하나를 빌드할 만큼만 보였다. 일반적인 인터페이스 정의 규칙과 패키지가 그것을 선언하는 방법은 [[04-robotics/ros2/workspaces-packages-launch|25.4 워크스페이스, 패키지, 빌드, 런치]]의 몫이고, 터미널 여섯 개 대신 파라미터를 붙인 런치 파일로 이 전부를 띄우는 법도 거기에 있다. Executor, 콜백 그룹, 그리고 애초에 서비스와 액션이 연결되게 만드는 QoS 설정은 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executor, 시간]]. 시스템 인터페이스로서의 액션 — 행동 트리가 액션을 부르고, 라이프사이클 관리자가 서버들을 순서 짓는 모습 — 은 [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]에서 나온다. 트랙 전체는 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- ROS 2 Jazzy 문서 — Concepts: Services; Actions; Parameters.
- ROS 2 Jazzy 문서 — Tutorials: Understanding services; Understanding parameters; Understanding actions; Writing a simple service and client (Python, C++); Creating an action; Writing an action server and client (Python, C++); Using parameters in a class (Python, C++); Managing node lifecycles.
- ROS 2 Jazzy 문서 — How-to guides: Synchronous vs. asynchronous service clients; `ros2 param` 커맨드라인 도구 사용; 커맨드라인으로 노드에 ROS 인자 넘기기.
- ros2/demos — `lifecycle` 패키지 README(주 상태와 전이 상태, 전이 콜백, 라이프사이클 인터페이스 다섯 가지); `lifecycle_py/lifecycle_py/talker.py`.
- ros2/examples — `rclpy/actions/minimal_action_server`(goal, cancel, accepted 콜백).
- ros2/ros2cli — `ros2lifecycle` 동사(`nodes`, `list`, `get`, `set`).
- ros-navigation/navigation2 — `nav2_lifecycle_manager` README와 `lifecycle_manager.cpp`(순서 지어진 기동, `manage_nodes` 서비스, `bond_timeout` 기본값).

> [!question]- 스스로 점검 · 정답
> **1. 요청을 받아 30초짜리 전역 계획을 도는 노드가 필요하다. 서비스인가 액션인가, 왜인가?** 액션이다. 서비스는 호출자를 막고 선점할 수 없으며, 단일 스레드 executor에서 30초짜리 서비스 콜백은 그 노드의 다른 모든 콜백 — 타이머, 구독, 다른 서비스 — 도 함께 멈춘다. 공식 지침은 서비스가 빨리 반환해야 하고 장시간 작업은 액션의 몫이라는 것이다. 액션은 덤으로 피드백과 취소 경로를 준다.
> **2. `ros2 param load /my_node params.yaml`이 일부는 "successful", 일부는 "cannot be set because it is read-only"를 찍는다. 뭔가 고장 났나?** 아니다. 읽기 전용 파라미터는 기동 시에만 설정된다. `qos_overrides.*`는 모든 노드에서 읽기 전용이고, 그래서 dump 후 load를 왕복하면 항상 그 실패가 찍힌다. 꼭 적용해야 하면 같은 파일을 기동 시 `--ros-args --params-file`로 넘겨라. 그쪽은 읽기 전용 파라미터도 갱신한다.
> **3. 직접 쓴 노드가 `ros2 node list`에 있고, `ros2 node info`에 서비스 클라이언트와 구독이 다 보이고, 호출하는 서버도 돌고 있는데, 첫 입력 이후 아무것도 내보내지 않는다. 첫 가설은?** 콜백 안에서 한 동기 서비스 호출. executor가 실행 중인 콜백을 선점해 응답을 전달할 수 없어서 호출이 영원히 기다린다. 예외도, 경고도, 실패도 없다. 첫 트리거 이전에는 출력이 있었는지 확인해 확증하고, `call_async`나 별도 콜백 그룹 + 다중 스레드 executor로 고친다.
> **4. Nav2는 왜 보통 노드 대신 라이프사이클 노드를 쓰는가?** 기동 순서가 중요하고 부분 기동이 위험하기 때문이다. 라이프사이클 관리자가 서버들을 순서 지어진 그룹으로 `configure`와 `activate`를 거치게(종료 시에는 역순으로) 하므로, 자원이 생기기 전에는 무엇도 발행하거나 목표를 받지 않는다. 그다음 각 서버와 bond를 유지해서, 활성화 이후의 충돌이 스택을 반쯤 살아 있는 상태로 남기지 않고 결정론적으로 내리게 한다. "Nav2가 왜 아무것도 안 하지"에 대한 한 줄 답은 `ros2 lifecycle get <node>`다.
