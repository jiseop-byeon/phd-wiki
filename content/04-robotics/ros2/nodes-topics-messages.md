---
title: "25.2 Nodes, Topics and Messages"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Write a publisher and a subscriber from scratch in Python and C++, define your own message type in its own package, and diagnose the silent failure when two endpoints never connect."
mastery-when: "Go deeper when you are choosing delivery semantics, executor policy or memory ownership for a rate-critical channel rather than getting data from A to B."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to write, build and debug your own pub–sub nodes in both client libraries. Not enough to reason about delivery guarantees or intra-process zero-copy.
> **Working** — 두 클라이언트 라이브러리 모두에서 자기 pub–sub 노드를 쓰고 빌드하고 디버깅할 정도. 전달 보장이나 프로세스 내 zero-copy를 따질 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], meaning a working **ROS 2 Jazzy Jalisco on Ubuntu 24.04** install that you can source, and the graph-reading commands from its section 9. Python; enough C++ to read a class. Every command below assumes a sourced terminal. Building your own packages is covered properly in [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]] — this page uses the minimum of it and tells you which lines matter.
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], 즉 source 가능한 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 설치와 거기 9절의 그래프 읽기 명령들. Python과, 클래스를 읽을 정도의 C++. 아래 모든 명령은 source된 터미널을 전제한다. 패키지 빌드는 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]에서 제대로 다루고, 이 페이지는 최소한만 쓰면서 어느 줄이 중요한지 짚는다.

### 1. Why publish–subscribe

In 25.1 you ran a graph someone else wrote. Now you write one. Before the code, the shape of the thing.

A camera driver produces frames. It does not know who wants them. Today that is a detector; next week it is also a recorder, a bandwidth monitor, and a visualiser on the operator's laptop. If the driver holds a list of consumers, every new consumer is a change to the driver — a file you must edit, rebuild, and re-certify, in a package owned by someone else.

Publish–subscribe removes that list. The driver publishes to a **topic**, a name. Anything that wants frames subscribes to that name. The driver's code does not change, and does not know whether it has zero subscribers or nine. The official concept documentation calls this a *bus*, and the analogy is the right one: a name, many things attached, no wiring between them.

This buys three things that you will use constantly:

1. **Introspection is free.** `ros2 topic echo` works because it is just another subscriber. `ros2 bag record` works the same way — the documentation says so explicitly: it creates a new subscriber to the topic without interrupting the flow of data to the rest of the system. You can inspect any channel in a running robot without modifying anything.
2. **Substitution is free.** In 25.1 you replaced a teleop driver with `ros2 topic pub` and the turtle did not notice. Replace the real camera with a bag replay or a simulator, and the detector cannot tell.
3. **Failure is local.** A subscriber that dies does not fault the publisher. A publisher that dies leaves subscribers quiet, and they resume when it returns.

The cost is stated just as plainly in section 10: with no list of consumers, nothing tells you when a connection you expected does not exist.

### 2. Nodes: one process per concern

A **node** is a participant in the ROS 2 graph that uses a client library to talk to other nodes. The official guidance on granularity is one sentence long and worth taking literally: *each node should do one logical thing.*

"One logical thing" is not "one file" and not "one class". A useful test is the restart test: if you would ever want to restart, replace, re-tune or re-deploy piece A without disturbing piece B, A and B are different nodes. A camera driver and a detector fail that test in opposite directions — you will swap detectors weekly and never touch the driver — so they are two nodes. A detector and the non-maximum-suppression step inside it will always live and die together, so they are one.

Two refinements on top of the beginner picture:

- A node is not exactly a process. One process can host several nodes; ROS 2 calls this composition, and it is how a real stack avoids paying serialisation costs between nodes that happen to run on the same machine. Composition is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]].
- A node's name is not its executable's name. You saw this in 25.1: `turtlesim_node` names itself `/turtlesim`, and `--ros-args --remap __node:=my_turtle` renames it at launch without touching the code.

### 3. Topics, and the anonymity that is the point

A topic is a name. Any number of publishers and any number of subscribers may attach to it, and when any publisher publishes, every subscriber in the system receives the data.

The word the documentation uses for the relationship is **anonymous**: when a subscriber receives a message, it does not generally know or care which publisher sent it. This is not a missing feature. It is the property that makes substitution work. The subscriber has no handle on the producer, so there is nothing in the subscriber to change when the producer is replaced.

The other property is **strongly typed**, and it has two halves. The mechanical half: each field has a declared type, enforced by generated code in every language. The semantic half, which has no enforcement at all: the core message types carry agreed meanings — an IMU's angular velocity is in radians per second, and nothing else belongs in that field. Nothing will stop you from publishing degrees. The type checker cannot help you; the convention is the only thing holding.

Names follow rules worth internalising now, because section 10's bug lives here:

| Form | Example | Resolves to |
|---|---|---|
| Absolute | `/turtle1/pose` | `/turtle1/pose`, ignoring the node's namespace |
| Relative | `turtle1/pose` | namespace + name — in namespace `/watch`, `/watch/turtle1/pose` |
| Private | `~/pose` | node's namespace + node name + `/pose` |

Names may contain alphanumerics, underscores and forward slashes; they must not start with a digit, and must not contain repeated slashes or repeated underscores. A tilde must appear at the start and must be separated from the rest by a slash — `~/foo`, never `~foo`.

Almost every example in this track — and the tutorials — writes the relative form `'topic'`. That is correct and deliberate: a relative name is what allows the same node to be launched twice into two namespaces and produce two non-colliding graphs. It is also why a node accidentally launched into a namespace goes silent against a peer that hard-coded the absolute form.

### 4. Messages, and how to read one

A message type is defined in a `.msg` file in the `msg/` directory of a package, in ROS 2's interface definition language. Each line is a field: a type, a space, a name. Optionally a third token gives a default.

Built-in field types are `bool`, `byte`, `char`, `float32`, `float64`, `int8`/`uint8` through `int64`/`uint64`, `string` and `wstring`. A field may also be another message type, written `geometry_msgs/Point center`. Arrays exist in three shapes, and the difference matters on a real robot:

```text
int32[] unbounded_integer_array
int32[5] five_integers_array
int32[<=5] up_to_five_integers_array
string<=10 up_to_ten_characters_string
```

Bounded forms (`[5]`, `[<=5]`, `string<=10`) give the middleware a maximum size it can allocate once. Unbounded forms do not, which is why a rate-critical path usually bounds its arrays. Field names must be lowercase with underscores, must start with a letter, and must not end with or repeat an underscore. Constants are written with `=` and must be UPPERCASE: `uint8 PHONE_TYPE_MOBILE=2`.

You will read far more message definitions than you write, and there is exactly one command for it:

```bash
ros2 interface show geometry_msgs/msg/Twist
```

The companions are worth knowing the day you need them: `ros2 interface list` (every interface on the system), `ros2 interface package geometry_msgs` (everything one package defines), and `ros2 interface proto geometry_msgs/msg/Twist`, which prints a filled-in prototype you can paste into a `ros2 topic pub`.

One trap that this command will not warn you about. `std_msgs/msg/Float64` looks like the obvious way to publish a number, and its own definition says otherwise. So does `std_msgs/msg/String`, which carries the identical notice and which the worked examples below still use — because the tutorials do, and you will meet it everywhere:

```bash
ros2 interface show std_msgs/msg/Float64
```

```text
# This was originally provided as an example message.
# It is deprecated as of Foxy
# It is recommended to create your own semantically meaningful message.
```

A bare `float64 data` on a topic carries no units, no frame, no timestamp, and no name for what the number is. Two years later nobody can tell whether it was metres per second or a normalised throttle. Read the definition, not just the field list — the comments in a `.msg` file *are* the semantic contract, and section 7 is how you write your own.

### 5. A publisher and a subscriber in Python

Create an `ament_python` package in the `src` directory of your workspace:

```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
```

In `py_pubsub/py_pubsub/publisher_member_function.py`:

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Four things in that file are the whole idiom, and the rest is decoration.

`create_publisher(String, 'topic', 10)` declares the contract: message type, topic name, and a queue depth of 10. That third argument is not a convenience — it is a required Quality of Service setting that bounds how many messages are held for a subscriber that is not keeping up. You are choosing a delivery policy whether or not you know it; [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] is where the choice is made deliberately.

`create_timer(0.5, self.timer_callback)` is the **timer-callback idiom**, and it is the answer to the question every beginner asks: where is the loop? There is no loop. You do not write `while True: publish(); sleep(0.5)`. You register a callback and hand control to ROS 2. Everything periodic in a ROS 2 node is a timer, because that is what lets one thread service timers, subscriptions and service requests in a policy you can control rather than in whatever order your `while` loop happens to impose.

`rclpy.spin(node)` is where that control is handed over. It blocks and runs callbacks until shutdown. A node that is constructed but never spun creates its endpoints, appears in `ros2 node list`, and never runs a single callback — a genuinely confusing failure the first time.

And the subscriber, in `subscriber_member_function.py`, which needs no timer at all because its callback fires when a message arrives:

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Note that the topic name and the message type are identical on both sides. They have to be. That is the entire connection condition, and section 10 is what happens when one of them is off by a character.

Two files of plumbing make these runnable. In `package.xml`, after the description and licence tags:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```

In `setup.py`, inside `entry_points`, which is what gives `ros2 run` something to find:

```python
entry_points={
        'console_scripts': [
                'talker = py_pubsub.publisher_member_function:main',
                'listener = py_pubsub.subscriber_member_function:main',
        ],
},
```

From the workspace root:

```bash
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build --packages-select py_pubsub
source install/setup.bash
ros2 run py_pubsub talker      # and, in a second sourced terminal:
ros2 run py_pubsub listener
```

### 6. The same pair in C++, and what it makes explicit

Production stacks — Nav2, MoveIt 2, ros2_control, every driver you will link against — are written in C++. You will read far more rclcpp than you write, so read it now while the program is four lines long.

```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_pubsub
```

`cpp_pubsub/src/publisher_member_function.cpp`:

```cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
public:
  MinimalPublisher()
  : Node("minimal_publisher"), count_(0)
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, world! " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

`cpp_pubsub/src/subscriber_member_function.cpp`:

```cpp
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
public:
  MinimalSubscriber()
  : Node("minimal_subscriber")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
  }

private:
  void topic_callback(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}
```

Structurally identical: subclass `Node`, name yourself in the constructor, create endpoints, register callbacks, spin. Four things the C++ states out loud that the Python leaves implicit.

**The type is a template parameter.** `create_publisher<std_msgs::msg::String>` fixes the type at compile time, so publishing the wrong type is a build error. In Python, `self.publisher_.publish(msg)` with a wrong-typed `msg` is a runtime error inside a callback, in a process that is otherwise running normally. Neither language catches the cross-process mismatch of section 10; the compiler protects one process, not the contract between two.

**Endpoints are owned objects with lifetimes.** `rclcpp::Publisher<T>::SharedPtr publisher_` is a member because it must outlive the constructor. Let a publisher, subscription or timer go out of scope in C++ and the endpoint is destroyed — the node keeps running, quietly, with nothing attached. The Python tutorial's odd-looking `self.subscription  # prevent unused variable warning` line is the same concern wearing a disguise.

**The callback signature names the ownership.** `const std_msgs::msg::String & msg` says the message arrives by reference and the callback will not modify it. rclcpp also accepts `std_msgs::msg::String::UniquePtr`, which is the form that makes zero-copy intra-process delivery possible. Python has one calling convention and no way to express the distinction, so the cost of a message is invisible there.

**The clock is named.** rclcpp's `create_wall_timer` says wall clock in its name. rclpy's `create_timer` takes an optional `clock` argument and, when you omit it, uses the node's clock — which is the one that follows simulated time. So the Python and C++ examples on this page do not use the same clock, and in simulation they will not behave the same. That is [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]], and it is the single most under-appreciated line on this page.

The build plumbing is CMake rather than `setup.py`. In `package.xml`, `<depend>rclcpp</depend>` and `<depend>std_msgs</depend>` (`<depend>`, not `<exec_depend>`, because C++ needs these at build time too). In `CMakeLists.txt`:

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(talker src/publisher_member_function.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/subscriber_member_function.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})
```

The `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` block is the one people forget. Without it the executables build and `ros2 run cpp_pubsub talker` cannot find them, because `ros2 run` looks in `lib/<package>`. Then `colcon build --packages-select cpp_pubsub`, source, and run — and note that the C++ talker and the Python listener interoperate, because the contract is the topic name and the message type, not the language.

### 7. Your own message, and the package it belongs in

Now do the thing section 4 told you to do instead of reaching for `Float64`. Interfaces can only be defined in `ament_cmake` packages, so the interface package is a CMake package even when everything that uses it is Python:

```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 turtle_watch_interfaces
mkdir turtle_watch_interfaces/msg
```

`turtle_watch_interfaces/msg/SpeedReport.msg` — the directory name `msg/` is required, and the file name must be `CamelCase.msg`:

```text
# Ground speed of a turtlesim turtle, derived from its pose stream.
std_msgs/Header header
float64 speed      # m/s, non-negative
float64 heading    # degrees, CCW from +x
```

In `turtle_watch_interfaces/CMakeLists.txt`:

```cmake
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SpeedReport.msg"
  DEPENDENCIES std_msgs
)
```

`rosidl_generate_interfaces` is the whole point of the package: it runs the code generators that turn one `.msg` file into a C++ header, a Python module, and the type support the middleware needs. `DEPENDENCIES` lists the packages whose types you referenced — `std_msgs` here, for `Header`. Its first argument must start with the package name, so use `${PROJECT_NAME}`.

In `turtle_watch_interfaces/package.xml`:

```xml
<depend>std_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

The split is the lesson: `rosidl_default_generators` runs at build time, `rosidl_default_runtime` is needed whenever the types are used, and `<member_of_group>rosidl_interface_packages</member_of_group>` is how the package announces itself as an interface package. Build and confirm:

```bash
colcon build --packages-select turtle_watch_interfaces
source install/setup.bash
ros2 interface show turtle_watch_interfaces/msg/SpeedReport
```

**Why a separate package.** The official guidance is that best practice is to declare interfaces in dedicated interface packages, and the reasons are structural rather than stylistic:

- **Every consumer depends on it.** If the type lives beside your perception node, anyone who merely wants to *read* your topic must build your perception node — and its solver, its CUDA dependency, its model weights.
- **Circular dependencies become impossible to avoid.** Two nodes that exchange each other's types cannot each depend on the other's package. With one interface package below both, the graph stays acyclic.
- **Rebuild blast radius.** Generated code is a build-time dependency of every consumer. Keeping interfaces in a small package that changes rarely keeps that radius small.
- **Using a type in the package that defines it needs extra CMake.** Cross-package, `find_package(turtle_watch_interfaces REQUIRED)` is enough. Same-package, you must additionally call `rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)` and `target_link_libraries` your executable against it. The plumbing is telling you which arrangement is the normal one.

The naming convention you will see everywhere is `<something>_msgs` or `<something>_interfaces`. Follow it; people grep for it.

### 8. When pub–sub is the wrong pattern

Topics are for continuous data streams — sensor readings, robot state, commands. They are asynchronous and one-way. Three shapes do not fit, and forcing them produces code that works on a good day:

- **You need an answer.** "Is this grasp reachable?" over a topic means publishing a request, subscribing to a reply topic, and inventing a correlation ID so you know which reply is yours. That is a request–response protocol, badly. Use a **service**.
- **The work takes a long time and you may want to stop it.** "Drive to the kitchen" runs for minutes, should report progress, and must be cancellable when a person walks in. A service will not do either — the documentation is explicit that services are expected to return quickly and should never be used for long-running processes. Use an **action**.
- **It is configuration, not data.** A gain, a frame name, a camera exposure. Publishing it on a topic means a node that starts late never learns the value. Use **parameters**.

All three are [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. The tell, when you are unsure: if the sender needs to know what happened to the message, it is not a topic.

### 9. Exercise: republish something derived

One sitting. You will write a node that subscribes to one topic and publishes a derived quantity on another, using the message type from section 7.

Create the Python package beside the interface package:

```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 turtle_watch
```

`turtle_watch/turtle_watch/speed_watch.py`:

```python
import math

import rclpy
from rclpy.node import Node

from turtle_watch_interfaces.msg import SpeedReport
from turtlesim.msg import Pose


class SpeedWatch(Node):

    def __init__(self):
        super().__init__('speed_watch')
        self.publisher_ = self.create_publisher(SpeedReport, 'turtle1/speed', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10)

    def pose_callback(self, msg):
        report = SpeedReport()
        report.header.stamp = self.get_clock().now().to_msg()
        report.header.frame_id = 'turtle1'
        report.speed = float(abs(msg.linear_velocity))
        report.heading = float(math.degrees(msg.theta))
        self.publisher_.publish(report)


def main(args=None):
    rclpy.init(args=args)
    node = SpeedWatch()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

Add to `turtle_watch/package.xml`:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>turtlesim</exec_depend>
<exec_depend>turtle_watch_interfaces</exec_depend>
```

and to `setup.py`:

```python
entry_points={
        'console_scripts': [
                'speed_watch = turtle_watch.speed_watch:main',
        ],
},
```

Build, including the interface package it depends on, then run the three nodes in three sourced terminals:

```bash
colcon build --packages-up-to turtle_watch
source install/setup.bash
```

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_watch speed_watch
ros2 run turtlesim turtle_teleop_key
```

Now verify it, which is the actual exercise:

```bash
ros2 topic echo /turtle1/speed
```

Drive with the arrow keys. `speed` jumps to the commanded value and falls back to zero; `heading` sweeps as you turn. Then measure:

```bash
ros2 topic hz /turtle1/pose
ros2 topic hz /turtle1/speed
```

Both report roughly the same rate — turtlesim publishes pose continuously at around 60 Hz, and your node publishes exactly once per pose because it publishes *from the subscription callback*. Note the documented caveat: `ros2 topic hz` reports the receiving rate on the subscription that the command itself created, which platform load and QoS can affect, so it need not match the publisher exactly.

Then change the design and watch the measurement change. Store the pose instead of publishing it, and publish on a timer:

```python
self.latest = None
self.timer = self.create_timer(0.1, self.publish_report)
```

with `pose_callback` doing only `self.latest = msg`, and `publish_report` returning early when `self.latest is None`. Rebuild and re-run `ros2 topic hz /turtle1/speed`: about 10 Hz, independent of the input rate. You have just made the choice that every real republisher makes — callback-driven means one output per input and an output rate you do not control; timer-driven means a fixed output rate and dropped or repeated inputs. Say out loud which one a 200 Hz IMU feeding a 20 Hz controller needs.

You are done when `ros2 topic info /turtle1/speed --verbose` shows your node as the publisher with type `turtle_watch_interfaces/msg/SpeedReport`, and you can explain both `hz` numbers.

### 10. The failure to diagnose: the silent mismatch

Two endpoints connect only if the **topic name** matches and the **message type** matches. If either differs, nothing connects — and nothing complains. Both processes start, both log normally, both appear in `ros2 node list`, and no message ever crosses. There is no error because there is no error condition: a publisher with no subscribers is a perfectly legal, extremely common state, and the middleware cannot tell that you *meant* those two to be the same channel.

Reproduce it deliberately. Launch your republisher into a namespace so its relative name resolves differently:

```bash
ros2 run turtle_watch speed_watch --ros-args --remap __ns:=/watch
```

`ros2 topic echo /turtle1/speed` does not hang here — with the publisher moved into `/watch` the topic has no endpoints at all, so echo prints `WARNING: topic [/turtle1/speed] does not appear to be published yet` and then fails with "Could not determine the type for the passed topic". That is the *lucky* version. The silent one is a name that still exists because something else publishes it, or a type mismatch on a live name, where echo sits there printing nothing. Diagnose both in this order.

**1. Are both nodes actually alive?**

```bash
ros2 node list
```

If one is missing, it crashed or was never spun, and this is not a mismatch at all. If both are there, continue.

**2. What names exist, with what types?**

```bash
ros2 topic list -t
```

```text
/turtle1/pose [turtlesim/msg/Pose]
/watch/turtle1/speed [turtle_watch_interfaces/msg/SpeedReport]
```

Two similar names where you expected one is the name mismatch, and it is usually visible right here — a namespace prefix, a typo, a missing or extra leading slash. If instead you see exactly the one name you expected, the name is fine and the type is the suspect.

**3. Who is attached to that name, and with what type?**

```bash
ros2 topic info /turtle1/speed --verbose
```

`--verbose` prints, for every endpoint, the node name and namespace, the `Endpoint type` (`PUBLISHER` or `SUBSCRIPTION`), the `Topic type`, the `Topic type hash`, and the full QoS profile. Two readings:

- `Publisher count: 1`, `Subscription count: 0` — nothing is listening on this name. Name mismatch.
- Both endpoints present but their `Topic type` and `Topic type hash` differ between the `PUBLISHER` block and the `SUBSCRIPTION` block — type mismatch. The hash is the useful part: it changes when the *definition* changes, so it also catches the nastier case where both sides name the same type but were built against different versions of the `.msg` file.

**4. What did each node actually register?**

```bash
ros2 node info /watch/speed_watch
ros2 node info /turtlesim
```

This prints each node's publishers and subscribers as fully-resolved names with types. Put the two outputs side by side and the difference is a single line. This is the authoritative answer, because it reports what the process registered rather than what you believe it registered.

`ros2 topic find turtle_watch_interfaces/msg/SpeedReport` is the shortcut when you know the type and have lost the name.

**Fixing it.** You do not need to rebuild to test a hypothesis. Remapping at launch settles it in seconds:

```bash
ros2 run turtle_watch speed_watch --ros-args --remap __ns:=/watch --remap turtle1/speed:=/turtle1/speed
```

If that makes data flow, the bug was the name. Then fix it properly — in the code if the name was wrong, or in the launch file if the namespace was, which is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]].

> [!warning] There is a third cause of silence
> Matching name and matching type, and still nothing arrives: the QoS profiles are incompatible. It presents identically — two healthy nodes, no error, no data — and `ros2 topic info --verbose` is again the command that shows it, in the QoS block you have been ignoring. Rule it out last, and read [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] before you need to.

### 11. What this page does not cover

Request–response, long-running cancellable goals, runtime configuration and managed startup are [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. Workspaces, overlays, `colcon` in earnest, composition and launch files are [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. The QoS settings behind the queue-depth argument you have been passing as `10`, the executor that decides which callback runs when several are ready, and simulated versus wall time are [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. Simulation, navigation, manipulation and hardware interfaces sit above all of it in [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Concepts: Nodes; Topics; Interfaces; Services; Actions; Interfaces (topics, services, actions).
- ROS 2 Jazzy documentation — Tutorials: Understanding nodes; Understanding topics; Writing a simple publisher and subscriber (Python); Writing a simple publisher and subscriber (C++); Creating custom msg and srv files; Implementing custom interfaces; Creating your first ROS 2 package.
- ROS 2 design article — Topic and Service name mapping to DDS (naming rules).
- `ros2/examples` repository, `jazzy` branch — `rclcpp/topics/minimal_publisher/member_function.cpp`, `rclcpp/topics/minimal_subscriber/member_function.cpp`.
- `std_msgs/msg/Float64` definition (deprecation note), `turtlesim/msg/Pose` definition.
- `rclpy` API — `Node.create_timer` clock argument.

> [!question]- Self-check · Answer
> **1. Your publisher and your subscriber both start, both log normally, and no data moves. Name the three causes and the one command that distinguishes them.** Topic-name mismatch, message-type mismatch, QoS incompatibility. `ros2 topic info <name> --verbose` shows all three: subscription count zero means the name is wrong, differing `Topic type` or type hash between the publisher and subscriber blocks means the type is wrong, and the QoS profile block is where the third lives. Start from `ros2 node list` and `ros2 topic list -t` to narrow it, and use `ros2 node info` for the authoritative per-node answer.
> **2. Why is a custom message defined in its own package rather than in the node that publishes it?** Because every consumer of the topic must depend on the type. Putting it in the node's package forces anyone who wants to read the topic to build the node and its whole dependency tree, makes mutual dependencies between two nodes circular, and widens the rebuild radius. Interfaces can also only be defined in `ament_cmake` packages, and using a type inside the package that defines it needs extra `rosidl_get_typesupport_target` plumbing that cross-package use does not.
> **3. Your republisher subscribes at 60 Hz and publishes from the subscription callback. A colleague changes it to publish from a 10 Hz timer. What changed, and when would each be right?** Callback-driven gives exactly one output per input, so the output rate is the input rate and you do not control it. Timer-driven gives a fixed output rate, dropping inputs when they arrive faster and republishing stale data when they arrive slower. Callback-driven is right when every input must be seen and downstream can keep up; timer-driven is right when a fast source feeds a slower fixed-rate consumer, or when the output rate is part of the contract.
> **4. What does the C++ version make explicit that the Python version hides?** The message type is a compile-time template parameter, so an in-process type error is a build failure. Endpoints are explicitly owned `SharedPtr` members that die if you let them go out of scope. The callback signature states how the message is passed and whether it is modifiable, which is what makes zero-copy intra-process delivery expressible. And the clock is named: `create_wall_timer` is the wall clock, while rclpy's `create_timer` silently defaults to the node's clock, which follows simulated time.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 두 클라이언트 라이브러리 모두에서 자기 pub–sub 노드를 쓰고 빌드하고 디버깅할 정도. 전달 보장이나 프로세스 내 zero-copy를 따질 정도는 아니다.
> **Working** — enough to write, build and debug your own pub–sub nodes in both client libraries, not to reason about delivery guarantees.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], 즉 source 가능한 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 설치와 그 9절의 그래프 읽기 명령들. Python과, 클래스를 읽을 정도의 C++. 아래 모든 명령은 source된 터미널을 전제한다. 패키지 빌드 자체는 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]에서 다루고, 여기서는 최소한만 쓴다.
> ROS 2 Jazzy on Ubuntu 24.04, the graph-reading commands from 25.1, Python, and enough C++ to read a class.

### 1. 왜 publish–subscribe인가

25.1에서는 남이 만든 그래프를 돌렸다. 이제 직접 만든다. 코드보다 먼저 형태를 본다.

카메라 드라이버는 프레임을 만든다. 누가 그것을 원하는지는 모른다. 오늘은 검출기이고, 다음 주에는 기록기와 대역폭 모니터와 조작자 노트북의 시각화 도구까지 붙는다. 드라이버가 소비자 목록을 들고 있다면 소비자가 하나 늘 때마다 드라이버를 고쳐야 한다. 남이 소유한 패키지의 파일을 편집하고 다시 빌드하고 다시 검증해야 한다는 뜻이다.

Publish–subscribe는 그 목록을 없앤다. 드라이버는 이름에 publish한다. 그 이름을 **토픽**(topic)이라고 부른다. 프레임이 필요한 쪽이 그 이름을 subscribe한다. 드라이버 코드는 바뀌지 않고, 구독자가 0인지 9인지도 모른다. 공식 개념 문서는 이것을 *버스*라고 부르는데 적절한 비유다. 이름 하나, 거기 붙은 여러 개, 그 사이의 배선은 없음.

여기서 얻는 것 셋은 계속 쓰게 된다.

1. **내성(introspection)이 공짜다.** `ros2 topic echo`가 동작하는 이유는 그것이 그냥 또 하나의 구독자이기 때문이다. `ros2 bag record`도 같다. 문서가 명시적으로 그렇게 적는다 — 나머지 시스템의 데이터 흐름을 끊지 않고 해당 토픽에 새 구독자를 만든다. 돌아가는 로봇의 어떤 채널이든 아무것도 고치지 않고 들여다볼 수 있다.
2. **교체가 공짜다.** 25.1에서 teleop 드라이버를 `ros2 topic pub`으로 갈아 끼웠고 거북이는 알아채지 못했다. 실제 카메라를 bag 재생이나 시뮬레이터로 바꿔도 검출기는 구분하지 못한다.
3. **고장이 국소적이다.** 구독자가 죽어도 퍼블리셔는 죽지 않는다. 퍼블리셔가 죽으면 구독자는 조용해졌다가 퍼블리셔가 돌아오면 재개한다.

대가는 10절에서 그대로 드러난다. 소비자 목록이 없으니, 있으리라 기대한 연결이 없을 때 아무것도 알려 주지 않는다.

### 2. 노드: 관심사 하나에 프로세스 하나

**노드**(node)는 클라이언트 라이브러리를 써서 다른 노드와 통신하는 ROS 2 그래프의 참여자다. 입자성에 대한 공식 지침은 한 문장이고 문자 그대로 받아들일 값어치가 있다. *각 노드는 논리적으로 한 가지 일을 해야 한다.*

"논리적으로 한 가지"는 "파일 하나"도 "클래스 하나"도 아니다. 쓸 만한 판별법은 재시작 테스트다. A를 B와 무관하게 재시작·교체·재튜닝·재배포하고 싶은 순간이 조금이라도 있다면 A와 B는 다른 노드다. 카메라 드라이버와 검출기는 이 테스트에 정반대 방향에서 걸린다. 검출기는 매주 갈아 끼우고 드라이버는 건드리지 않을 테니 둘은 두 노드다. 검출기와 그 안의 non-maximum suppression 단계는 항상 함께 살고 함께 죽으니 하나다.

초심자용 그림에 붙일 보정 둘.

- 노드는 정확히 프로세스가 아니다. 한 프로세스가 여러 노드를 담을 수 있고, ROS 2는 이것을 composition이라 부른다. 실제 스택이 같은 머신에 있는 노드들 사이의 직렬화 비용을 피하는 방법이 이것이다. Composition은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]에 있다.
- 노드 이름은 실행 파일 이름이 아니다. 25.1에서 봤다. `turtlesim_node`는 스스로를 `/turtlesim`이라 부르고, `--ros-args --remap __node:=my_turtle`은 코드를 건드리지 않고 실행 시점에 이름을 바꾼다.

### 3. 토픽, 그리고 익명성이라는 핵심

토픽은 이름이다. 퍼블리셔 몇이든 구독자 몇이든 거기 붙을 수 있고, 어느 퍼블리셔가 publish하면 시스템 안의 모든 구독자가 그 데이터를 받는다.

문서가 이 관계를 부르는 말은 **익명(anonymous)** 이다. 구독자가 데이터를 받을 때 그것을 누가 보냈는지 대체로 모르고 신경 쓰지 않는다는 뜻이다. 빠진 기능이 아니다. 교체를 가능하게 하는 바로 그 성질이다. 구독자는 생산자에 대한 손잡이를 쥐고 있지 않으므로, 생산자가 바뀔 때 구독자에서 고칠 것이 없다.

다른 성질은 **강한 타입(strongly typed)** 이고 절반이 둘이다. 기계적인 절반은 각 필드에 선언된 타입이 있고 모든 언어의 생성 코드가 그것을 강제한다는 것이다. 의미론적인 절반은 강제 장치가 전혀 없다. 핵심 메시지 타입들은 합의된 의미를 지닌다. IMU의 각속도는 라디안 매 초이고 다른 것이 그 필드에 들어가서는 안 된다. 하지만 당신이 각도(degree)를 publish하는 것을 아무도 막지 않는다. 타입 검사기는 도와줄 수 없고, 관례만이 유일한 버팀목이다.

이름 규칙은 지금 몸에 익혀 두라. 10절의 버그가 여기 산다.

| 형태 | 예 | 해석 결과 |
|---|---|---|
| 절대 | `/turtle1/pose` | `/turtle1/pose`. 노드 네임스페이스를 무시한다 |
| 상대 | `turtle1/pose` | 네임스페이스 + 이름. 네임스페이스가 `/watch`면 `/watch/turtle1/pose` |
| 비공개 | `~/pose` | 노드 네임스페이스 + 노드 이름 + `/pose` |

이름에는 영숫자, 밑줄, 슬래시가 들어갈 수 있다. 숫자로 시작하면 안 되고, 슬래시나 밑줄이 연달아 반복되면 안 된다. 물결표는 맨 앞에 와야 하고 나머지와 슬래시로 구분되어야 한다 — `~/foo`이지 `~foo`가 아니다.

이 트랙의 거의 모든 예제와 공식 튜토리얼은 상대 형태 `'topic'`을 쓴다. 옳고 의도적이다. 같은 노드를 서로 다른 두 네임스페이스에 두 번 띄워 충돌하지 않는 두 그래프를 만들 수 있게 하는 것이 상대 이름이다. 그리고 실수로 네임스페이스 안에 띄워진 노드가, 절대 형태를 하드코딩한 상대 노드에 대해 조용해지는 이유이기도 하다.

### 4. 메시지, 그리고 읽는 법

메시지 타입은 패키지의 `msg/` 디렉터리 안 `.msg` 파일에, ROS 2의 인터페이스 정의 언어로 정의된다. 각 줄이 필드다. 타입, 공백, 이름. 선택적으로 세 번째 토큰이 기본값을 준다.

내장 필드 타입은 `bool`, `byte`, `char`, `float32`, `float64`, `int8`/`uint8`부터 `int64`/`uint64`, `string`, `wstring`이다. 필드는 다른 메시지 타입일 수도 있고 `geometry_msgs/Point center`처럼 쓴다. 배열은 세 형태가 있고, 실제 로봇에서는 그 차이가 중요하다.

```text
int32[] unbounded_integer_array
int32[5] five_integers_array
int32[<=5] up_to_five_integers_array
string<=10 up_to_ten_characters_string
```

경계가 있는 형태(`[5]`, `[<=5]`, `string<=10`)는 미들웨어에 한 번에 할당할 최대 크기를 알려 준다. 경계 없는 형태는 그러지 않고, 그래서 속도가 중요한 경로는 보통 배열에 경계를 건다. 필드 이름은 소문자와 밑줄이어야 하고, 알파벳으로 시작해야 하며, 밑줄로 끝나거나 밑줄이 연달아서는 안 된다. 상수는 `=`로 쓰고 대문자여야 한다: `uint8 PHONE_TYPE_MOBILE=2`.

메시지 정의는 쓰는 것보다 읽는 일이 훨씬 많고, 명령은 정확히 하나다.

```bash
ros2 interface show geometry_msgs/msg/Twist
```

곁의 명령들도 필요한 날을 위해 알아 두라. `ros2 interface list`(시스템의 모든 인터페이스), `ros2 interface package geometry_msgs`(한 패키지가 정의하는 전부), 그리고 `ros2 interface proto geometry_msgs/msg/Twist`는 `ros2 topic pub`에 그대로 붙여 넣을 수 있는 프로토타입을 찍는다.

이 명령이 경고해 주지 않는 함정 하나. `std_msgs/msg/Float64`는 숫자를 publish하는 뻔한 방법처럼 보이는데, 정작 자기 정의가 반대로 말한다. `std_msgs/msg/String`도 똑같은 문구를 달고 있다. 아래 예제가 그래도 그것을 쓰는 이유는 튜토리얼들이 그렇게 하고 있어 어디서든 마주치게 되기 때문이다.

```bash
ros2 interface show std_msgs/msg/Float64
```

```text
# This was originally provided as an example message.
# It is deprecated as of Foxy
# It is recommended to create your own semantically meaningful message.
```

토픽 위의 맨 `float64 data`는 단위도, 프레임도, 타임스탬프도, 그 숫자가 무엇인지에 대한 이름도 나르지 않는다. 2년 뒤에는 그것이 초속 미터였는지 정규화된 스로틀이었는지 아무도 모른다. 필드 목록만 보지 말고 정의를 읽어라. `.msg` 파일의 주석이 곧 의미론적 계약이고, 자기 것을 쓰는 법은 7절이다.

### 5. Python으로 쓰는 퍼블리셔와 서브스크라이버

워크스페이스의 `src` 디렉터리에서 `ament_python` 패키지를 만든다.

```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 py_pubsub
```

`py_pubsub/py_pubsub/publisher_member_function.py`:

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

이 파일에서 네 가지가 관용구의 전부이고 나머지는 장식이다.

`create_publisher(String, 'topic', 10)`은 계약을 선언한다. 메시지 타입, 토픽 이름, 그리고 큐 깊이 10. 세 번째 인자는 편의 기능이 아니라 필수 Quality of Service 설정이고, 따라오지 못하는 구독자를 위해 몇 개까지 붙들어 둘지를 정한다. 알든 모르든 전달 정책을 고르고 있는 것이고, 그 선택을 의식적으로 하는 곳이 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]다.

`create_timer(0.5, self.timer_callback)`이 **타이머-콜백 관용구**(timer-callback idiom)이고, 초심자가 반드시 던지는 질문의 답이다. 루프는 어디 있나? 루프는 없다. `while True: publish(); sleep(0.5)`를 쓰지 않는다. 콜백을 등록하고 제어권을 ROS 2에 넘긴다. ROS 2 노드에서 주기적인 것은 전부 타이머인데, 그래야 한 스레드가 타이머와 구독과 서비스 요청을, 당신의 `while` 루프가 우연히 강제하는 순서가 아니라 제어 가능한 정책으로 처리할 수 있기 때문이다.

`rclpy.spin(node)`가 그 제어권을 넘기는 지점이다. 블로킹하면서 종료까지 콜백을 돌린다. 생성만 되고 spin되지 않은 노드는 엔드포인트를 만들고 `ros2 node list`에도 나타나면서 콜백은 하나도 돌리지 않는다. 처음 겪으면 진심으로 헷갈리는 고장이다.

그리고 서브스크라이버. `subscriber_member_function.py`이고, 콜백이 메시지 도착 시에 불리므로 타이머가 아예 필요 없다.

```python
import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

양쪽의 토픽 이름과 메시지 타입이 똑같다는 점을 보라. 그래야만 한다. 그것이 연결 조건의 전부이고, 한 글자가 어긋났을 때 무슨 일이 나는지가 10절이다.

실행 가능하게 만드는 배관은 파일 둘이다. `package.xml`의 description과 license 태그 뒤에:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>std_msgs</exec_depend>
```

`setup.py`의 `entry_points` 안에. `ros2 run`이 찾을 대상을 주는 것이 이것이다.

```python
entry_points={
        'console_scripts': [
                'talker = py_pubsub.publisher_member_function:main',
                'listener = py_pubsub.subscriber_member_function:main',
        ],
},
```

워크스페이스 루트에서:

```bash
rosdep install -i --from-path src --rosdistro jazzy -y
colcon build --packages-select py_pubsub
source install/setup.bash
ros2 run py_pubsub talker      # 그리고 source된 두 번째 터미널에서:
ros2 run py_pubsub listener
```

### 6. 같은 쌍을 C++로, 그리고 C++이 드러내는 것

실제 제품 스택 — Nav2, MoveIt 2, ros2_control, 당신이 링크할 모든 드라이버 — 은 C++로 쓰였다. rclcpp는 쓰는 것보다 읽는 일이 훨씬 많을 테니, 프로그램이 네 줄일 때 읽어 두라.

```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 cpp_pubsub
```

`cpp_pubsub/src/publisher_member_function.cpp`:

```cpp
#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

class MinimalPublisher : public rclcpp::Node
{
public:
  MinimalPublisher()
  : Node("minimal_publisher"), count_(0)
  {
    publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
    timer_ = this->create_wall_timer(
      500ms, std::bind(&MinimalPublisher::timer_callback, this));
  }

private:
  void timer_callback()
  {
    auto message = std_msgs::msg::String();
    message.data = "Hello, world! " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
    publisher_->publish(message);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  size_t count_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalPublisher>());
  rclcpp::shutdown();
  return 0;
}
```

`cpp_pubsub/src/subscriber_member_function.cpp`:

```cpp
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using std::placeholders::_1;

class MinimalSubscriber : public rclcpp::Node
{
public:
  MinimalSubscriber()
  : Node("minimal_subscriber")
  {
    subscription_ = this->create_subscription<std_msgs::msg::String>(
      "topic", 10, std::bind(&MinimalSubscriber::topic_callback, this, _1));
  }

private:
  void topic_callback(const std_msgs::msg::String & msg) const
  {
    RCLCPP_INFO(this->get_logger(), "I heard: '%s'", msg.data.c_str());
  }
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<MinimalSubscriber>());
  rclcpp::shutdown();
  return 0;
}
```

구조는 동일하다. `Node`를 상속하고, 생성자에서 스스로 이름을 짓고, 엔드포인트를 만들고, 콜백을 등록하고, spin한다. C++이 소리 내어 말하고 Python이 암묵에 남기는 것이 넷이다.

**타입이 템플릿 인자다.** `create_publisher<std_msgs::msg::String>`은 타입을 컴파일 시점에 고정하므로 잘못된 타입을 publish하면 빌드 오류다. Python에서는 타입이 틀린 `msg`로 `self.publisher_.publish(msg)`를 하면 멀쩡히 돌아가던 프로세스의 콜백 안에서 런타임 오류가 난다. 두 언어 모두 10절의 프로세스 간 불일치는 잡지 못한다. 컴파일러는 한 프로세스를 지키지, 두 프로세스 사이의 계약을 지키지 않는다.

**엔드포인트는 수명을 가진 소유 객체다.** `rclcpp::Publisher<T>::SharedPtr publisher_`가 멤버인 이유는 생성자보다 오래 살아야 하기 때문이다. C++에서 퍼블리셔나 구독, 타이머를 스코프 밖으로 흘려보내면 엔드포인트가 파괴된다. 노드는 계속 돌아가고, 조용하고, 아무것도 붙어 있지 않다. Python 튜토리얼의 어색한 `self.subscription  # prevent unused variable warning` 줄은 같은 걱정이 변장한 것이다.

**콜백 시그니처가 소유권을 명시한다.** `const std_msgs::msg::String & msg`는 메시지가 참조로 도착하고 콜백이 그것을 수정하지 않는다고 말한다. rclcpp는 `std_msgs::msg::String::UniquePtr` 형태도 받는데, 프로세스 내 zero-copy 전달을 가능하게 하는 형태가 그것이다. Python에는 호출 규약이 하나뿐이고 그 구분을 표현할 방법이 없으므로 메시지의 비용이 보이지 않는다.

**시계에 이름이 붙어 있다.** rclcpp의 `create_wall_timer`는 이름에 벽시계라고 적혀 있다. rclpy의 `create_timer`는 선택적 `clock` 인자를 받고, 생략하면 노드의 시계를 쓴다. 그것이 시뮬레이션 시간을 따라가는 시계다. 그래서 이 페이지의 Python 예제와 C++ 예제는 같은 시계를 쓰지 않으며, 시뮬레이션에서는 동작이 달라진다. 그것이 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]이고, 이 페이지에서 가장 과소평가되는 한 줄이다.

빌드 배관은 `setup.py`가 아니라 CMake다. `package.xml`에는 `<depend>rclcpp</depend>`와 `<depend>std_msgs</depend>` — `<exec_depend>`가 아니라 `<depend>`인 이유는 C++이 이것들을 빌드 시점에도 필요로 하기 때문이다. `CMakeLists.txt`에는:

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(talker src/publisher_member_function.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/subscriber_member_function.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})
```

사람들이 빼먹는 것이 `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` 블록이다. 이것이 없으면 실행 파일은 빌드되지만 `ros2 run cpp_pubsub talker`가 찾지 못한다. `ros2 run`은 `lib/<package>`를 보기 때문이다. 그다음 `colcon build --packages-select cpp_pubsub`, source, 실행. 그리고 C++ talker와 Python listener가 서로 통한다는 점을 보라. 계약은 토픽 이름과 메시지 타입이지 언어가 아니다.

### 7. 자기 메시지, 그리고 그것이 속할 패키지

이제 4절이 `Float64` 대신 하라고 한 일을 한다. 인터페이스는 `ament_cmake` 패키지에서만 정의할 수 있으므로, 그것을 쓰는 쪽이 전부 Python이어도 인터페이스 패키지는 CMake 패키지다.

```bash
ros2 pkg create --build-type ament_cmake --license Apache-2.0 turtle_watch_interfaces
mkdir turtle_watch_interfaces/msg
```

`turtle_watch_interfaces/msg/SpeedReport.msg` — 디렉터리 이름 `msg/`는 필수이고 파일 이름은 `CamelCase.msg`여야 한다.

```text
# Ground speed of a turtlesim turtle, derived from its pose stream.
std_msgs/Header header
float64 speed      # m/s, non-negative
float64 heading    # degrees, CCW from +x
```

`turtle_watch_interfaces/CMakeLists.txt`에:

```cmake
find_package(std_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/SpeedReport.msg"
  DEPENDENCIES std_msgs
)
```

`rosidl_generate_interfaces`가 이 패키지의 존재 이유다. 코드 생성기를 돌려 `.msg` 파일 하나를 C++ 헤더와 Python 모듈, 그리고 미들웨어가 필요로 하는 type support로 바꾼다. `DEPENDENCIES`에는 참조한 타입이 있는 패키지를 적는다. 여기서는 `Header` 때문에 `std_msgs`다. 첫 인자는 패키지 이름으로 시작해야 하므로 `${PROJECT_NAME}`을 쓴다.

`turtle_watch_interfaces/package.xml`에:

```xml
<depend>std_msgs</depend>
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

이 분리가 배울 점이다. `rosidl_default_generators`는 빌드 시점에 돌고, `rosidl_default_runtime`은 타입을 쓸 때마다 필요하며, `<member_of_group>rosidl_interface_packages</member_of_group>`는 이 패키지가 인터페이스 패키지임을 선언하는 방법이다. 빌드하고 확인한다.

```bash
colcon build --packages-select turtle_watch_interfaces
source install/setup.bash
ros2 interface show turtle_watch_interfaces/msg/SpeedReport
```

**왜 별도 패키지인가.** 공식 지침은 인터페이스를 전용 인터페이스 패키지에 선언하는 것이 모범 사례라고 말하고, 이유는 취향이 아니라 구조에 있다.

- **모든 소비자가 그것에 의존한다.** 타입이 당신의 인식 노드 옆에 살면, 당신의 토픽을 그저 *읽고* 싶은 사람도 당신의 인식 노드를 빌드해야 한다. 솔버와 CUDA 의존성과 모델 가중치까지 함께.
- **순환 의존을 피할 수 없게 된다.** 서로의 타입을 주고받는 두 노드는 서로의 패키지에 의존할 수 없다. 인터페이스 패키지 하나를 둘 아래에 두면 그래프가 비순환으로 남는다.
- **재빌드 파급 범위.** 생성된 코드는 모든 소비자의 빌드 시점 의존성이다. 인터페이스를 거의 바뀌지 않는 작은 패키지에 두면 그 범위가 작게 유지된다.
- **정의한 패키지 안에서 타입을 쓰려면 CMake가 더 필요하다.** 패키지가 다르면 `find_package(turtle_watch_interfaces REQUIRED)`로 끝난다. 같은 패키지라면 추가로 `rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)`를 부르고 실행 파일을 거기에 `target_link_libraries` 해야 한다. 배관 자체가 어느 쪽이 정상 배치인지 말해 주고 있다.

어디서나 보게 될 작명 관례는 `<something>_msgs` 또는 `<something>_interfaces`다. 따르라. 사람들이 그걸로 grep한다.

### 8. pub–sub이 틀린 패턴일 때

토픽은 연속적인 데이터 스트림 — 센서 값, 로봇 상태, 명령 — 을 위한 것이다. 비동기이고 단방향이다. 맞지 않는 모양이 셋 있고, 억지로 끼우면 운 좋은 날에만 동작하는 코드가 나온다.

- **답이 필요할 때.** "이 파지가 도달 가능한가?"를 토픽으로 하려면 요청을 publish하고 응답 토픽을 subscribe하고, 어느 응답이 내 것인지 알기 위해 상관 ID를 발명해야 한다. 요청–응답 프로토콜을 엉성하게 다시 만드는 것이다. **서비스**(service)를 써라.
- **오래 걸리고 중간에 멈추고 싶을 때.** "주방으로 이동"은 몇 분이 걸리고, 진행 상황을 보고해야 하며, 사람이 들어오면 취소되어야 한다. 서비스는 둘 다 못 한다. 문서가 명시적으로 적는다 — 서비스는 빨리 반환할 것으로 기대되고 장시간 프로세스에 절대 써서는 안 된다. **액션**(action)을 써라.
- **데이터가 아니라 설정일 때.** 게인, 프레임 이름, 카메라 노출. 이것을 토픽으로 내보내면 늦게 시작한 노드는 그 값을 영영 모른다. **파라미터**(parameter)를 써라.

셋 다 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]에 있다. 헷갈릴 때의 판별법: 보내는 쪽이 그 메시지가 어떻게 됐는지 알아야 한다면 그것은 토픽이 아니다.

### 9. 실습: 파생값을 다시 publish하기

한 자리에서 끝난다. 한 토픽을 subscribe해서 파생 값을 다른 토픽으로 publish하는 노드를, 7절의 메시지 타입으로 쓴다.

인터페이스 패키지 옆에 Python 패키지를 만든다.

```bash
ros2 pkg create --build-type ament_python --license Apache-2.0 turtle_watch
```

`turtle_watch/turtle_watch/speed_watch.py`:

```python
import math

import rclpy
from rclpy.node import Node

from turtle_watch_interfaces.msg import SpeedReport
from turtlesim.msg import Pose


class SpeedWatch(Node):

    def __init__(self):
        super().__init__('speed_watch')
        self.publisher_ = self.create_publisher(SpeedReport, 'turtle1/speed', 10)
        self.subscription = self.create_subscription(
            Pose,
            'turtle1/pose',
            self.pose_callback,
            10)

    def pose_callback(self, msg):
        report = SpeedReport()
        report.header.stamp = self.get_clock().now().to_msg()
        report.header.frame_id = 'turtle1'
        report.speed = float(abs(msg.linear_velocity))
        report.heading = float(math.degrees(msg.theta))
        self.publisher_.publish(report)


def main(args=None):
    rclpy.init(args=args)
    node = SpeedWatch()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

`turtle_watch/package.xml`에 추가:

```xml
<exec_depend>rclpy</exec_depend>
<exec_depend>turtlesim</exec_depend>
<exec_depend>turtle_watch_interfaces</exec_depend>
```

`setup.py`에 추가:

```python
entry_points={
        'console_scripts': [
                'speed_watch = turtle_watch.speed_watch:main',
        ],
},
```

의존하는 인터페이스 패키지까지 함께 빌드하고, source된 터미널 셋에서 노드 셋을 띄운다.

```bash
colcon build --packages-up-to turtle_watch
source install/setup.bash
```

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtle_watch speed_watch
ros2 run turtlesim turtle_teleop_key
```

이제 검증한다. 그것이 실제 실습이다.

```bash
ros2 topic echo /turtle1/speed
```

화살표 키로 몰아 보라. `speed`가 명령된 값으로 튀었다가 0으로 떨어지고, 회전하면 `heading`이 쓸려 간다. 그다음 측정한다.

```bash
ros2 topic hz /turtle1/pose
ros2 topic hz /turtle1/speed
```

둘이 거의 같은 주기를 보고한다. turtlesim은 pose를 대략 60 Hz로 계속 내고, 당신의 노드는 *구독 콜백 안에서* publish하므로 pose 하나당 정확히 한 번 낸다. 문서화된 단서를 기억하라. `ros2 topic hz`는 그 명령이 스스로 만든 구독에서의 수신 주기를 보고하며, 플랫폼 부하와 QoS의 영향을 받으므로 퍼블리셔 주기와 정확히 같을 필요는 없다.

그다음 설계를 바꾸고 측정이 바뀌는 것을 보라. pose를 publish하지 말고 저장한 뒤, 타이머로 publish한다.

```python
self.latest = None
self.timer = self.create_timer(0.1, self.publish_report)
```

`pose_callback`은 `self.latest = msg`만 하고, `publish_report`는 `self.latest is None`이면 바로 반환한다. 다시 빌드하고 `ros2 topic hz /turtle1/speed`를 다시 돌리면 입력 주기와 무관하게 약 10 Hz다. 방금 모든 실제 republisher가 내리는 선택을 한 것이다. 콜백 구동은 입력 하나당 출력 하나이고 출력 주기를 제어할 수 없다. 타이머 구동은 출력 주기가 고정이고 입력이 버려지거나 반복된다. 200 Hz IMU가 20 Hz 제어기에 들어갈 때 어느 쪽이 필요한지 소리 내어 말해 보라.

`ros2 topic info /turtle1/speed --verbose`가 당신의 노드를 퍼블리셔로, 타입을 `turtle_watch_interfaces/msg/SpeedReport`로 보여 주고, `hz` 두 숫자를 설명할 수 있으면 끝이다.

### 10. 진단할 고장: 조용한 불일치

두 엔드포인트가 연결되는 조건은 딱 둘이다. **토픽 이름** 일치, 그리고 **메시지 타입** 일치. 둘 중 하나라도 다르면 아무것도 연결되지 않고, 아무도 항의하지 않는다. 두 프로세스 모두 뜨고, 둘 다 정상 로그를 찍고, 둘 다 `ros2 node list`에 나오고, 메시지는 한 개도 건너가지 않는다. 오류가 없는 이유는 오류 조건이 없기 때문이다. 구독자가 없는 퍼블리셔는 완벽히 합법이고 매우 흔한 상태이며, 미들웨어는 당신이 그 둘을 같은 채널로 *의도했다*는 것을 알 길이 없다.

일부러 재현해 보라. 상대 이름이 다르게 풀리도록 republisher를 네임스페이스 안에 띄운다.

```bash
ros2 run turtle_watch speed_watch --ros-args --remap __ns:=/watch
```

`ros2 topic echo /turtle1/speed`는 여기서 매달리지 않는다. 퍼블리셔가 `/watch` 안으로 들어가 버려 이 토픽에는 엔드포인트가 하나도 없고, 그래서 echo는 `WARNING: topic [/turtle1/speed] does not appear to be published yet`을 찍은 뒤 "Could not determine the type for the passed topic"으로 실패한다. 이건 *운이 좋은* 쪽이다. 조용한 쪽은 다른 무언가가 발행하고 있어 이름은 살아 있는 경우, 또는 살아 있는 이름에서 타입이 어긋난 경우다. 그때는 echo가 아무것도 찍지 않고 앉아 있는다. 둘 다 이 순서로 진단한다.

**1. 두 노드가 실제로 살아 있는가?**

```bash
ros2 node list
```

하나가 없으면 죽었거나 애초에 spin되지 않은 것이고, 이건 불일치 문제가 아니다. 둘 다 있으면 다음으로.

**2. 어떤 이름들이, 어떤 타입으로 존재하는가?**

```bash
ros2 topic list -t
```

```text
/turtle1/pose [turtlesim/msg/Pose]
/watch/turtle1/speed [turtle_watch_interfaces/msg/SpeedReport]
```

하나를 기대했는데 비슷한 이름 둘이 보이면 이름 불일치이고, 보통 바로 여기서 드러난다. 네임스페이스 접두사, 오타, 앞 슬래시가 빠졌거나 더 붙었거나. 반대로 기대한 이름 하나만 정확히 보인다면 이름은 멀쩡하고 타입이 용의자다.

**3. 그 이름에 누가 붙어 있고, 타입은 무엇인가?**

```bash
ros2 topic info /turtle1/speed --verbose
```

`--verbose`는 엔드포인트마다 노드 이름과 네임스페이스, `Endpoint type`(`PUBLISHER` 또는 `SUBSCRIPTION`), `Topic type`, `Topic type hash`, 그리고 전체 QoS 프로파일을 찍는다. 읽는 법 둘.

- `Publisher count: 1`, `Subscription count: 0` — 이 이름을 아무도 듣고 있지 않다. 이름 불일치.
- 엔드포인트가 둘 다 있는데 `PUBLISHER` 블록과 `SUBSCRIPTION` 블록의 `Topic type`이나 `Topic type hash`가 다르다 — 타입 불일치. 해시가 쓸모 있는 부분이다. 해시는 *정의*가 바뀌면 바뀌므로, 양쪽이 같은 타입 이름을 대면서 서로 다른 판본의 `.msg` 파일로 빌드된 더 고약한 경우까지 잡아낸다.

**4. 각 노드가 실제로 등록한 것은 무엇인가?**

```bash
ros2 node info /watch/speed_watch
ros2 node info /turtlesim
```

각 노드의 퍼블리셔와 서브스크라이버를 완전히 해석된 이름과 타입으로 찍는다. 두 출력을 나란히 놓으면 차이는 한 줄이다. 이것이 최종 판정인데, 당신이 등록했다고 믿는 것이 아니라 프로세스가 실제로 등록한 것을 보고하기 때문이다.

타입은 아는데 이름을 잃었을 때의 지름길은 `ros2 topic find turtle_watch_interfaces/msg/SpeedReport`다.

**고치기.** 가설을 시험하는 데 다시 빌드할 필요는 없다. 실행 시점 remapping이면 몇 초에 끝난다.

```bash
ros2 run turtle_watch speed_watch --ros-args --remap __ns:=/watch --remap turtle1/speed:=/turtle1/speed
```

이걸로 데이터가 흐르면 버그는 이름이었다. 그다음 제대로 고친다. 이름이 틀렸으면 코드에서, 네임스페이스가 문제였으면 launch 파일에서. 후자는 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]다.

> [!warning] 침묵의 세 번째 원인이 있다
> 이름도 맞고 타입도 맞는데 여전히 아무것도 도착하지 않는다면 QoS 프로파일이 호환되지 않는 것이다. 증상은 똑같다 — 멀쩡한 노드 둘, 오류 없음, 데이터 없음. 그리고 그것을 보여 주는 명령도 다시 `ros2 topic info --verbose`이며, 그동안 무시해 온 QoS 블록이다. 마지막으로 배제하고, 필요해지기 전에 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]를 읽어 두라.

### 11. 이 페이지가 다루지 않는 것

요청–응답, 취소 가능한 장시간 목표, 실행 중 설정, 결정적 기동은 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. 워크스페이스, 오버레이, `colcon`의 본격적인 사용, composition, launch 파일은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. 지금까지 `10`으로 넘겨 온 큐 깊이 인자 뒤의 QoS 설정, 여러 콜백이 준비됐을 때 어느 것을 돌릴지 정하는 executor, 시뮬레이션 시간과 벽시계 시간은 [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]. 시뮬레이션, 내비게이션, 매니퓰레이션, 하드웨어 인터페이스는 그 위에 있고 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- ROS 2 Jazzy 문서 — Concepts: Nodes; Topics; Interfaces; Services; Actions; Interfaces (topics, services, actions).
- ROS 2 Jazzy 문서 — Tutorials: Understanding nodes; Understanding topics; Writing a simple publisher and subscriber (Python); Writing a simple publisher and subscriber (C++); Creating custom msg and srv files; Implementing custom interfaces; Creating your first ROS 2 package.
- ROS 2 design 문서 — Topic and Service name mapping to DDS(이름 규칙).
- `ros2/examples` 저장소 `jazzy` 브랜치 — `rclcpp/topics/minimal_publisher/member_function.cpp`, `rclcpp/topics/minimal_subscriber/member_function.cpp`.
- `std_msgs/msg/Float64` 정의(deprecation 주석), `turtlesim/msg/Pose` 정의.
- `rclpy` API — `Node.create_timer`의 clock 인자.

> [!question]- 스스로 점검 · 정답
> **1. 퍼블리셔와 서브스크라이버가 둘 다 뜨고 둘 다 정상 로그를 찍는데 데이터가 안 움직인다. 원인 셋과 그것을 구분하는 명령 하나를 대라.** 토픽 이름 불일치, 메시지 타입 불일치, QoS 비호환. `ros2 topic info <이름> --verbose`가 셋 다 보여 준다. 구독 수가 0이면 이름이 틀린 것이고, 퍼블리셔 블록과 서브스크라이버 블록의 `Topic type`이나 타입 해시가 다르면 타입이 틀린 것이며, QoS 프로파일 블록에 세 번째가 산다. 범위를 좁히는 데는 `ros2 node list`와 `ros2 topic list -t`부터 시작하고, 노드별 최종 판정에는 `ros2 node info`를 쓴다.
> **2. 커스텀 메시지를 publish하는 노드 안이 아니라 별도 패키지에 정의하는 이유는?** 토픽의 모든 소비자가 그 타입에 의존해야 하기 때문이다. 노드 패키지에 넣으면 토픽을 읽고 싶을 뿐인 사람도 그 노드와 의존성 트리 전체를 빌드해야 하고, 두 노드가 서로의 타입을 쓰면 의존이 순환하며, 재빌드 파급 범위가 넓어진다. 인터페이스는 `ament_cmake` 패키지에서만 정의할 수 있고, 정의한 패키지 안에서 그 타입을 쓰려면 패키지 간 사용에는 필요 없는 `rosidl_get_typesupport_target` 배관이 추가로 필요하다.
> **3. republisher가 60 Hz로 subscribe하고 구독 콜백에서 publish한다. 동료가 10 Hz 타이머에서 publish하도록 바꿨다. 무엇이 바뀌었고 각각 언제 옳은가?** 콜백 구동은 입력 하나당 출력 하나이므로 출력 주기가 입력 주기이고 제어할 수 없다. 타이머 구동은 출력 주기가 고정이며, 입력이 더 빨리 오면 버리고 더 늦게 오면 낡은 데이터를 다시 낸다. 모든 입력을 봐야 하고 하류가 따라올 수 있으면 콜백 구동이 맞다. 빠른 소스가 느린 고정 주기 소비자에 들어가거나 출력 주기가 계약의 일부라면 타이머 구동이 맞다.
> **4. C++ 판본이 Python 판본이 감추는 무엇을 드러내는가?** 메시지 타입이 컴파일 시점 템플릿 인자라서 프로세스 내 타입 오류가 빌드 실패가 된다. 엔드포인트가 명시적으로 소유되는 `SharedPtr` 멤버라서 스코프 밖으로 흘리면 죽는다. 콜백 시그니처가 메시지를 어떻게 넘기고 수정 가능한지를 말하고, 그것이 프로세스 내 zero-copy 전달을 표현 가능하게 만든다. 그리고 시계에 이름이 붙어 있다. `create_wall_timer`는 벽시계이고, rclpy의 `create_timer`는 말없이 노드의 시계를 기본값으로 쓰며 그것은 시뮬레이션 시간을 따라간다.
