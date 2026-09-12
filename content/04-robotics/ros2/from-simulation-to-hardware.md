---
title: "25.11 From Simulation to Real Hardware"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "State what changes when the robot is physical, swap a simulated hardware component for a real driver at the ros2_control seam, get two machines talking over DDS, and pass a readiness checklist before a motor is ever powered."
mastery-when: "Go deeper when you are writing the hardware component or the motor-controller firmware itself, or when a safety function has to be certified rather than merely implemented."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to bring a stack that worked in simulation onto a real machine safely, and to diagnose it when nothing moves. Not enough to certify a safety function or write motor-controller firmware.
> **Working** — 시뮬레이션에서 돌던 스택을 실제 기계 위로 안전하게 옮기고, 아무것도 움직이지 않을 때 진단할 정도. 안전 기능을 인증하거나 모터 제어기 펌웨어를 작성할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> A stack that already runs in simulation under a controller: [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]. The silent-failure mechanisms in [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]] and the ordered checks in [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]] are used here rather than re-taught. Baseline throughout: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**.
> 이미 시뮬레이션에서 제어기 아래 돌아가는 스택([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]의 조용한 실패 메커니즘과 [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]의 순서 있는 점검은 여기서 다시 가르치지 않고 사용한다. 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**.

### 1. What actually changes

Nothing in your launch file changes. Almost everything under it does.

**Latency and jitter.** In simulation the physics step, the controller update and the sensor publication are scheduled by one process that can wait for all of them. On hardware there is a serial or EtherCAT or CAN bus with a transmission time, a driver with a buffer, a Linux scheduler that may not run your thread for 8 ms because a `dpkg` job took the CPU, and a network stack. The mean added delay is usually survivable and the *variance* is what destabilises a loop. A controller tuned against a simulator that delivered every sample exactly on time has never been tested against the thing that breaks it.

**Sensor noise and dropouts.** Simulated sensors are clean unless you asked for noise, and even then the noise you asked for is Gaussian and stationary, which real noise is not. Real sensors also stop: a USB camera renumbers itself after a re-plug, a lidar drops a rotation under vibration, an encoder line picks up interference from the motor it is bolted next to. Your node has to have an answer for "the last message was 400 ms ago" that is not "keep using the old value forever".

**Calibration.** In simulation the camera is exactly where the URDF says it is, because the URDF is what put it there. On the robot the URDF is a claim about a physical assembly, and it is wrong by a few millimetres and a degree or two on day one and by more after someone bumps it. Extrinsic calibration is a real, repeatable procedure that produces numbers you have to store, version and re-run — and a transform tree that is quietly wrong is the subject of [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot: URDF, TF2 and RViz]].

**Clocks.** One machine, one clock, no problem. Two machines and the timestamps in your messages come from two different clocks, so a "300 ms old" image may actually be 20 ms old and the tf buffer will tell you so in an error message that blames the wrong component.

**Power and thermal limits.** A simulated motor has no duty cycle. A real one has a continuous torque rating well below its peak, a driver that will current-limit or fault out, and a battery whose voltage sags under load so the same commanded velocity produces less motion at the end of a run than at the start. Nothing in the ROS layer tells you this is happening; the symptom is a controller that tracks worse over time.

**And the contact model, which was the most optimistic part of the whole stack.** Every other gap above is a parameter you can measure. Contact is usually a *model-form* error: rigid-body engines resolve contact as point constraints solved per timestep, while real impacts and stick–slip transitions are genuine discontinuities. A grasp that closed reliably in Gazebo can fail on the real object not because the friction coefficient was wrong but because the simulator could not represent the contact patch at all. [[05-construction-robotics/sim-to-real|Sim-to-Real]] treats this properly; the practical rule here is that free-space motion transfers far better than contact does, so plan your first real experiments to be free-space ones.

### 2. The seam: the hardware interface

The reason any of the simulation work transfers is that `ros2_control` puts a plugin boundary between *the controller* and *the thing being controlled*, and simulation sits on the same side of that boundary as a real robot does.

Three kinds of hardware component exist, all loaded as `pluginlib` plugins:

| Type | Base class | Use |
|---|---|---|
| System | `hardware_interface::SystemInterface` | a multi-DoF machine, e.g. an arm — read and write |
| Actuator | `hardware_interface::ActuatorInterface` | a single simple actuator — read and write |
| Sensor | `hardware_interface::SensorInterface` | read-only |

Your URDF already names one, inside the `<ros2_control>` tag:

```xml
<ros2_control name="MySystem" type="system">
  <hardware>
    <plugin>mock_components/GenericSystem</plugin>
  </hardware>
  <!-- joints and their state/command interfaces -->
</ros2_control>
```

`mock_components/GenericSystem` is the one that loops commands straight back as states. Under Gazebo the plugin line instead reads `gz_ros2_control/GazeboSimSystem`. On the real machine it reads the plugin name your vendor's driver package exports. **That line is the seam.** The controller, the controller configuration YAML, the joint names, the topic names, MoveIt, Nav2 and your own nodes do not know which of the three is loaded.

This is worth being concrete about, because it is the single strongest argument for doing the earlier work in `ros2_control` at all rather than publishing to a vendor topic directly. A stack that talks to a vendor's own `/my_arm/set_joint_positions` topic has to be rewritten for the next arm. A stack that talks to `joint_trajectory_controller` does not.

The check that the seam is intact:

```bash
ros2 control list_hardware_components
ros2 control list_hardware_interfaces
ros2 control list_controllers
```

The first prints each component, its plugin type and its lifecycle state. The second prints every state and command interface by name — `joint_1/position`, `joint_1/velocity` — and, crucially, whether each command interface is **claimed** by a controller. The third prints controllers and whether they are `active`. Those three commands answer almost every "why doesn't it move" question, and they are in section 11 for that reason.

### 3. read, update, write

The control loop is one thread in `controller_manager` running at a fixed rate, and it does three things per cycle:

1. the resource manager calls `read()` on every hardware component, which pulls state off the bus into the component's own storage;
2. the controller manager calls `update()` on every active controller, which reads those states and produces commands;
3. the resource manager calls `write()`, which pushes those commands out to the bus.

The two methods you implement have these signatures, identical for simulated and real components:

```cpp
hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;
```

Plus the lifecycle: `on_init`, `on_configure` (open the connection), `on_activate` (release brakes, enable power stage), `on_deactivate`, `on_cleanup`, `on_shutdown`, `on_error`. The states mean what they say — in `INACTIVE` states can be read but command interfaces are not available; only in `ACTIVE` can the machine move. A driver that enables the motors in `on_configure` instead of `on_activate` is a driver that energises an arm the moment the launch file starts, which is a bug with physical consequences.

The rate is the `controller_manager` parameter `update_rate`, an integer in Hz, **default 100**, read-only after startup. Set it to what the hardware can actually service. If `read()` blocks for 15 ms on a serial round-trip, a 1000 Hz update rate is a request the loop cannot meet, and the overrun will show up as jitter rather than as an error.

#### The skeleton, read off the installed header

Checked against `hardware_interface` **4.48.0**, which is what `apt` installs for Jazzy today.
At this version `SystemInterface` is a thin subclass of `HardwareComponentInterface` that makes
`write()` pure virtual; everything else you override comes from the base. Three things you
override, and one large thing you do not:

```cpp
#include "hardware_interface/system_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace my_robot
{
class MyRobotHardware : public hardware_interface::SystemInterface
{
public:
  // Parse the <ros2_control> block. params.hardware_info carries it.
  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareComponentInterfaceParams & params) override;

  // Open and close the connection. Nothing may move here.
  hardware_interface::CallbackReturn on_configure(const rclcpp_lifecycle::State &) override;
  hardware_interface::CallbackReturn on_cleanup(const rclcpp_lifecycle::State &) override;

  // Energise and de-energise. Only ACTIVE may move the machine.
  hardware_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State &) override;
  hardware_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State &) override;

  // The loop, at controller_manager's update_rate.
  hardware_interface::return_type read(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
  hardware_interface::return_type write(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
};
}  // namespace my_robot
```

Inside `read()` you publish what the machine reports, and inside `write()` you send what the
controller asked for, both addressed by the interface names your URDF declared:

```cpp
hardware_interface::return_type MyRobotHardware::read(
  const rclcpp::Time &, const rclcpp::Duration &)
{
  set_state("joint_1/position", encoder_radians_);
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type MyRobotHardware::write(
  const rclcpp::Time &, const rclcpp::Duration &)
{
  const double target = get_command("joint_1/position");
  send_to_drive(target);
  return hardware_interface::return_type::OK;
}
```

The large thing you do not write is the interface export. At 4.48.0 the framework builds the
state and command interfaces from the `<ros2_control>` block in the URDF, and the header says so
in the deprecation itself: `export_state_interfaces()` and `export_command_interfaces()` are
marked *"Replaced by ... on_export_state_interfaces() ... Exporting is handled by the
Framework."* You override `on_export_state_interfaces()` only to add interfaces that the URDF
does not declare. In the ordinary case you declare them in the URDF and reach them by name, as
above.

> [!warning] This API moved inside the Jazzy line, so check your own version
> `on_init(const HardwareInfo &)` is deprecated in favour of the `HardwareComponentInterfaceParams` overload shown here, and both old export methods are deprecated. `apt` currently ships 4.48.0 while the `jazzy` branch is at 4.48.1, and the header was refactored within that line — `system_interface.hpp` is now three lines that include `hardware_component_interface.hpp`, where the declarations actually live. Before writing a component, run `ros2 pkg xml -t version hardware_interface` and read the header you actually have. Do not copy a skeleton out of a blog post, and treat the one above as dated rather than permanent.

### 4. Drivers, and what to check before trusting one

Most of the time you will not write the hardware component — the vendor or a community project ships one. Before you build a thesis on it:

- **Does it target your distribution?** A driver whose only branch is `humble` is not a Jazzy driver. Check the branch list, not the README.
- **Is it a `ros2_control` hardware component, or a node with its own topics?** The second is much more common than the marketing suggests, and it means the seam in section 2 does not exist for you. You can still use it, but you are now writing the adapter.
- **Which interfaces does it export?** An arm that exports only `position` command interfaces cannot run a torque or impedance controller no matter what the arm's datasheet claims, because the driver is the limiting surface.
- **Is there an emergency stop path that does not go through your code?** Ask before buying, not after.
- **How does it behave on disconnection?** Unplug the cable while it runs. A driver that returns `ERROR` and deactivates is correct; one that keeps returning the last state forever is dangerous, because every node downstream will believe the robot is exactly where it last was.
- **Does it publish diagnostics and joint states at a stated rate?** `ros2 topic hz` on the real thing, compared with what the documentation claims, is a two-minute test that has saved people months.

### 5. DDS across a network

The moment the robot is one machine and your laptop is another, discovery stops being invisible.

The rules, in the order they bite:

- **`ROS_DOMAIN_ID` must match.** It is an integer; choose between 0 and 101 inclusive on Linux, which is the range that avoids the default ephemeral port range 32768–60999. Different domain on the two hosts means two systems that cannot see each other at all, with no error.
- **The hosts must be on the same subnet and multicast must work**, because default discovery is multicast. Jazzy also gives you `ROS_AUTOMATIC_DISCOVERY_RANGE`, with values `SUBNET` (the default), `LOCALHOST`, `OFF` and `SYSTEM_DEFAULT`, and `ROS_STATIC_PEERS`, a semicolon-separated list of addresses to discover on directly. Use the pair of them when multicast is blocked or the two machines are not on one subnet.
- **The RMW implementation must match** on both hosts. `rmw_fastrtps_cpp` on one and `rmw_cyclonedds_cpp` on the other will not interoperate.
- **Clocks must be disciplined.** Run `chrony` on both machines against the same source — or PTP if you need sub-millisecond — and verify it, rather than assuming that two machines that both said "NTP" agree.

Test multicast directly, one command per machine:

```bash
# machine A
ros2 multicast receive
```

```bash
# machine B
ros2 multicast send
```

Machine A should print something of the form `Received from <address>:<port>: 'Hello World!'`. If it does not, the firewall is the first suspect; the documented fix is to allow UDP to and from the multicast range:

```bash
sudo ufw allow in proto udp to 224.0.0.0/4
sudo ufw allow in proto udp from 224.0.0.0/4
```

**The characteristic multi-machine failure is that both hosts see each other's nodes and no data flows.** `ros2 node list` is complete on both sides, `ros2 topic list` is complete on both sides, `ros2 topic echo` on the remote topic prints nothing. This is not mysterious once you know that *discovery and data take different paths*: discovery is multicast to a well-known port, data is unicast to per-participant ports. A firewall rule that allows the multicast range and nothing else produces exactly this symptom. So does a VPN or Docker bridge that carries multicast but NATs unicast, and so does a QoS mismatch — which produces the same silence on one machine, so rule out the network before you blame QoS, or you will spend the afternoon in the wrong file.

The second characteristic failure appears only with large messages on WiFi: a camera topic that hangs for roughly 30 seconds at a time. That is IP fragment reassembly. A UDP datagram larger than the MTU is fragmented; one lost fragment leaves the rest occupying the kernel's reassembly buffer until `net.ipv4.ipfrag_time` (default 30 s) expires, and while that buffer is full nothing else gets through. The documented mitigations are best-effort QoS for that topic, lowering `net.ipv4.ipfrag_time`, and raising `net.ipv4.ipfrag_high_thresh`. The better fix is usually to not send raw images over WiFi at all.

### 6. Real-time, stated honestly

ROS 2 is **not** a real-time system, and installing it from apt gives you no deadline guarantees. The official position is that ROS 2 is *designed with* real-time constraints in mind; the real-time demo itself is documented as requiring a source build against a static DDS API, currently only Connext.

What a real-time kernel (RT_PREEMPT) gives you: bounded scheduling latency, so a thread that is ready to run actually runs within a known time. What it does not give you: anything about the code inside that thread. Real-time behaviour requires removing nondeterministic operations from the execution path — page faults, dynamic allocation and deallocation, and synchronisation primitives that can block indefinitely. A `malloc` in your `update()` defeats the kernel entirely.

`controller_manager` does what can be done at this layer, and it is worth knowing what it is doing on your behalf:

- its update thread attempts `SCHED_FIFO` at priority 50, which requires your user to have an `rtprio` limit granted in `/etc/security/limits.conf` — without that the attempt fails and you silently get ordinary scheduling;
- the `lock_memory` parameter locks the node's memory into physical RAM at startup to avoid page faults, defaulting to false on a normal kernel and true on a real-time one.

And the part that matters most for how you design the system: **hard timing lives below ROS, not in it.** The current loop that keeps a motor from cooking itself runs in the motor controller at tens of kilohertz. The safety-rated stop runs in a safety relay. ROS 2 sends setpoints at 100–1000 Hz to a device that is already closing a faster loop around them. If your architecture requires ROS 2 to meet a hard deadline, the architecture is wrong before the tuning is.

### 7. Safety

Once the machine can move, this stops being optional, and it stops being software.

**An emergency stop is hardware.** A button that publishes a `std_msgs/msg/Bool` on a topic is not an emergency stop; it is a feature that shares a failure mode with everything it is supposed to protect against. A real E-stop is a hard-wired circuit that removes power or engages brakes independently of the computer, latches until deliberately reset, and works when the software has hung, the DDS link has dropped and the laptop has gone to sleep. Test it by pressing it while the stack is running, and then by pulling the network cable.

Beyond the stop: limit the workspace physically where you can (a table edge, a barrier, a shortened tether), limit speed for every experiment that does not need the full envelope, limit force where the hardware supports it, and never run a new trajectory at full speed on the first attempt.

The standards vocabulary — what a *safety-rated monitored stop* and *monitored standstill* are, how speed-and-separation distances are computed, which standard governs an arm versus an AMR versus an earth-moving machine, and why the version pins move — is already set out in [[04-robotics/hri-safety|11. HRI & Safety]], and the version-sensitive parts of it are stated there rather than here so that there is one place to keep current. Read that section before your first human-adjacent experiment, not after. [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]] covers the surrounding operational questions.

### 8. Choosing hardware: criteria, not a recommendation

This page will not tell you what to buy, and neither should anyone who has not seen your experiment.

**Try the institution first.** Most engineering departments already own more robots than are in use at any moment, and access to an existing arm with an existing maintainer is worth more than ownership of a new one. Ask the lab manager, ask senior students which machines are idle, and ask whether you can be added to an existing safety training and risk assessment rather than writing one. The cost of borrowing is scheduling; the cost of buying is everything in the last paragraph of this section.

**The experiment chooses the hardware.** The common failure is the reverse: a platform arrives, and the research question quietly deforms into whatever that platform can demonstrate. Write down the measurement your thesis needs — forces at a contact, centimetre-scale placement accuracy, a policy running at 50 Hz, hours of teleoperated demonstrations — and only then ask which class of machine can produce it. If two very different platforms both satisfy the written requirement, the requirement is not yet specific enough to justify a purchase.

The classes, and what each actually teaches:

| Class | What it genuinely teaches | What it does not |
|---|---|---|
| A low-cost arm | the whole stack end to end — URDF, controllers, calibration, the hardware seam, safety habits — on a machine whose failures are cheap | stiffness, repeatability, payload, or any result that depends on accurate force control |
| A teleoperation rig (leader–follower, in the manner of [[01-canonical-papers/notes/7-robotics/gello\|GELLO]]) | demonstration collection, the ergonomics of data volume, and what a dataset costs in human hours | autonomy of any kind; and note that such rigs are typically unilateral, so the data carries no force channel |
| A mobile base | odometry drift, localisation, the Nav2 stack against a real floor, and power budgeting over a run | manipulation, contact, or anything about an arm |

And the thing nobody puts in the purchase justification: **none of them teaches you whether your method works at the scale the paper claims.** A result on a low-cost arm is a result on a low-cost arm. That can be enough — plenty of good papers are exactly that, honestly scoped — but it has to be scoped that way in writing from the start rather than defended later.

> [!warning] The maintenance cost is real and it is taken from your research time
> A physical robot generates work that looks nothing like research: cables that fail intermittently, a firmware update that changes an interface, a gripper that needs rebuilding, a driver that breaks on a distribution upgrade, and the recurring tax of being the person who knows how to start the machine. Budget it explicitly. If you are the only maintainer, a substantial fraction of your week belongs to the robot, and it is taken from the fraction you planned to spend on the thesis.

### 9. Exercise: a readiness checklist

You may not have hardware yet, so the exercise is the artefact that comes before hardware. Write this out for your specific machine and make every line *verifiable* — a command to run or a physical thing to observe, not an intention.

**Before power:**

1. The E-stop circuit is wired, and you can state what it removes (motor power? logic power? brakes engage?) without looking it up.
2. Pressing the E-stop with the machine off produces a measurable open circuit, or the vendor's documented indication. You have tested the button as a button.
3. The workspace is clear to the full reach of the machine, and someone other than the operator is present for the first power-on.
4. The robot is mechanically restrained or in a pose from which a fault cannot let it fall onto anything, including itself.

**Software, all checkable from a terminal:**

5. `ros2 control list_hardware_components` shows the real component, not `mock_components/GenericSystem` and not `gz_ros2_control/GazeboSimSystem`. Confirm it by reading the `<plugin>` line, not by memory.
6. `ros2 control list_hardware_interfaces` shows every command interface you expect, and shows them **unclaimed** — you are not starting with a controller already active.
7. `ros2 param get /controller_manager use_sim_time` returns `False`, and no launch argument is setting it true. A stack that still expects `/clock` will simply not tick.
8. `ros2 param get /controller_manager update_rate` returns a rate your bus can service, and you can say how long `read()` takes.
9. Joint limits in the URDF match the machine's real limits, and you have checked at least one by hand rather than trusting the file you inherited.
10. The first controller you intend to activate is a low-authority one — a joint state broadcaster first, then position at reduced speed. Write the exact `ros2 control switch_controllers` invocation now, so you are not composing it while the arm is live.
11. `chronyc tracking` on both machines, and the offset is small enough for your timestamps to mean anything.
12. `ros2 multicast send` / `ros2 multicast receive` passes between robot and laptop, and `ROS_DOMAIN_ID` and the RMW implementation are printed and identical on both.
13. You can record a bag of the first run: `ros2 bag record -a` is started before power-on, not after something interesting happens. [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]] is why.

**The last line, which is not a technical one:** you can describe, out loud, what the machine will do in the next thirty seconds, and what you will do if it does something else.

You are done when every line above is a command with an expected output, and someone else in the lab could run the list without you.

### 10. The failure to diagnose: it worked in simulation and the real robot does nothing

The most common day-one symptom, and the reason it is hard is that there is no error message anywhere. Work in this order and stop at the first failure; each check is cheap and each one rules out a whole class.

| # | Check | Command | What a failure looks like |
|---|---|---|---|
| 1 | Is the driver up at all? | `ros2 node list` | `/controller_manager` missing, or the vendor node missing |
| 2 | Is the hardware component loaded and **active**? | `ros2 control list_hardware_components` | component in `unconfigured` or `inactive`; nothing can move outside `active` |
| 3 | Are the command interfaces **claimed**? | `ros2 control list_hardware_interfaces` | interfaces listed but unclaimed — the controller is loaded but not active |
| 4 | Is a controller active? | `ros2 control list_controllers` | `inactive`, or a controller that failed to claim an interface another controller already owns |
| 5 | Is the clock shared and real? | `ros2 param get /controller_manager use_sim_time`, `chronyc tracking` | `use_sim_time: True` with no `/clock` publisher — the loop never advances |
| 6 | Do the two machines agree on the domain? | `echo $ROS_DOMAIN_ID` and `echo $RMW_IMPLEMENTATION` on both | different values; nodes visible but no data, or nothing visible at all |
| 7 | Is the E-stop latched? | look at the button, and at the drive's fault LED | commands accepted, states reported, zero motion — the software is fine and the power stage is off |

Row 7 is last in the table and first in real life, in the sense that it is the one experienced people check before opening a terminal. It produces a perfect-looking system: the controller is active, the interfaces are claimed, `ros2 topic echo` on the command topic shows sensible numbers, and the arm does not move, because a latched E-stop or an undervoltage fault has cut the power stage while leaving the communication bus alive. Learn the fault indication on your specific drive.

If all seven pass and the machine still does not move, the next step is `ros2 topic delay` on the command topic to see whether commands are arriving late, and then reading the driver's own diagnostics — at which point you are debugging the driver rather than ROS, which is a different and more productive activity than re-reading your launch file.

### 11. What this page does not cover

Writing a hardware component for a bus that has no driver, and motor-controller firmware, are both below this page. Certification of a safety function — as opposed to implementing something sensible — is a process involving documents, a risk assessment and usually another person; [[04-robotics/hri-safety|11. HRI & Safety]] is the entry point. Domain randomisation, system identification and learned residual models, which are what you reach for when the transfer gap is a policy rather than a controller, are [[05-construction-robotics/sim-to-real|Sim-to-Real]]. Fleet operations, logging infrastructure and long-run deployment sit in [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]]. The rest of the track is [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- `control.ros.org` (Jazzy) — Getting Started (controller manager, resource manager, hardware components, the read–update–write loop); Hardware Components / Writing a Hardware Component; `controller_manager` user documentation (`update_rate`, `lock_memory`, `use_sim_time`, `SCHED_FIFO` priority 50 and `rtprio` limits).
- `ros-controls/ros2_control`, `jazzy` branch — `hardware_interface` headers (`SystemInterface`, `read`/`write` signatures, the `on_export_*` deprecation), `mock_components_plugin_description.xml`, and the `ros2controlcli` verb list.
- `ros-controls/gz_ros2_control`, `jazzy` branch — `gz_hardware_plugins.xml` (`gz_ros2_control/GazeboSimSystem`).
- ROS 2 Jazzy documentation — The ROS_DOMAIN_ID; Improved Dynamic Discovery (`ROS_AUTOMATIC_DISCOVERY_RANGE`, `ROS_STATIC_PEERS`); Installation Troubleshooting (multicast test and `ufw` rules); DDS tuning (IP fragmentation, `ipfrag_time`, `ipfrag_high_thresh`); Understanding real-time programming.
- Safety standards are cited via [[04-robotics/hri-safety|11. HRI & Safety]] rather than restated here.

> [!question]- Self-check · Answer
> **1. Which single line in your configuration is the difference between driving a simulator and driving a real arm, and why does that make the rest of the stack transfer?** The `<plugin>` line inside the URDF's `<ros2_control>` tag — `mock_components/GenericSystem`, `gz_ros2_control/GazeboSimSystem`, or the vendor's component. It transfers because the controller, its YAML, the joint names and everything above them talk to the controller manager's interfaces, not to the hardware, so they cannot tell which plugin is loaded.
> **2. Two machines both list each other's nodes and topics, and `ros2 topic echo` prints nothing. What is the first thing to suspect, and why is it not a QoS mismatch?** Discovery and data take different paths: discovery is multicast, data is unicast to per-participant ports. A firewall or NAT that permits the multicast range and blocks unicast produces exactly this. Rule out the network first, because a QoS mismatch gives the identical symptom and is much slower to diagnose.
> **3. Your supervisor asks whether an RT_PREEMPT kernel will make the control loop deterministic. What is the accurate answer?** It bounds scheduling latency — a runnable thread runs within a known time — and does nothing about what the thread does. Page faults, dynamic allocation and unbounded blocking in the execution path still destroy determinism, which is why `controller_manager` also offers `lock_memory` and attempts `SCHED_FIFO`. And hard deadlines should not be in ROS at all; they belong in the motor controller.
> **4. A grasp succeeded in Gazebo and fails on the real object. Why is "tune the friction coefficient" usually the wrong first move?** Because contact failures are commonly model-form errors rather than parameter errors. The rigid-body engine resolves contact as per-timestep point constraints and cannot represent the real contact patch, so no value of the parameter recovers the behaviour. Free-space motion transfers far better than contact, which is why the first real experiments should be free-space ones.
> **5. What is wrong with an emergency stop implemented as a topic?** It shares failure modes with the system it is meant to protect against: if the executor has hung, the DDS link has dropped or the machine has been unplugged from the network, the message is never delivered. An E-stop must remove power or engage brakes through hard-wired circuitry, latch, and work with the computer switched off.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 시뮬레이션에서 돌던 스택을 실제 기계 위로 안전하게 옮기고, 아무것도 움직이지 않을 때 진단할 정도. 안전 기능을 인증하거나 모터 제어기 펌웨어를 쓸 정도는 아니다.
> **Working** — enough to bring a simulated stack onto a real machine safely and diagnose it, not to certify a safety function.

> [!note] 선수 지식 · Prerequisites
> 이미 시뮬레이션에서 제어기 아래 돌아가는 스택([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time]]의 조용한 실패와 [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]의 순서 있는 점검은 여기서 사용만 한다. 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**.
> A stack already running in simulation under a controller; Jazzy on Ubuntu 24.04 throughout.

### 1. 실제로 무엇이 달라지는가

런치 파일은 하나도 바뀌지 않는다. 그 아래는 거의 전부 바뀐다.

**지연과 지터.** 시뮬레이션에서는 물리 스텝, 제어기 업데이트, 센서 publish를 한 프로세스가 스케줄하고 모두를 기다려 줄 수 있다. 실제에는 전송 시간이 있는 시리얼·EtherCAT·CAN 버스, 버퍼를 가진 드라이버, `dpkg` 작업이 CPU를 잡아서 8 ms 동안 내 스레드를 실행하지 않을 수도 있는 리눅스 스케줄러, 그리고 네트워크 스택이 있다. 평균 지연은 대개 버틸 만하고, 루프를 불안정하게 만드는 것은 *분산*이다. 모든 샘플을 정확히 제때 주던 시뮬레이터로 튜닝한 제어기는 자신을 무너뜨릴 것과 한 번도 마주친 적이 없다.

**센서 잡음과 유실.** 시뮬레이션 센서는 잡음을 요청하지 않으면 깨끗하고, 요청해도 그 잡음은 가우시안이고 정상(stationary)이다. 실제 잡음은 그렇지 않다. 게다가 실제 센서는 멈춘다. USB 카메라는 다시 꽂으면 번호가 바뀌고, 라이다는 진동에서 한 회전을 빠뜨리고, 엔코더 선은 바로 옆에 볼트로 붙은 모터의 간섭을 탄다. "마지막 메시지가 400 ms 전"이라는 상황에 대해 "옛 값을 영원히 계속 쓴다"가 아닌 답을 노드가 가지고 있어야 한다.

**캘리브레이션.** 시뮬레이션에서 카메라는 URDF가 말하는 바로 그 자리에 있다. URDF가 거기에 놓았기 때문이다. 실제 로봇에서 URDF는 물리적 조립체에 대한 *주장*이고, 첫날부터 몇 밀리미터와 1~2도쯤 틀려 있으며 누가 부딪히면 더 틀어진다. 외부 캘리브레이션은 저장하고 버전을 매기고 다시 돌려야 하는 숫자를 내놓는 실제 절차다. 조용히 틀린 변환 트리는 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot: URDF, TF2 and RViz]]의 주제다.

**시계.** 머신 하나면 시계도 하나이고 문제가 없다. 머신이 둘이면 메시지의 타임스탬프가 서로 다른 시계에서 나오고, "300 ms 된" 이미지가 실은 20 ms 된 것일 수 있으며, tf 버퍼는 엉뚱한 구성요소를 탓하는 오류 메시지로 그 사실을 알려 준다.

**전력과 열 한계.** 시뮬레이션 모터에는 듀티 사이클이 없다. 실제 모터에는 피크보다 한참 낮은 연속 토크 정격이 있고, 전류 제한을 걸거나 폴트로 빠지는 드라이버가 있고, 부하에서 전압이 처지는 배터리가 있어서 같은 속도 명령이 실험 초반보다 후반에 더 적은 움직임을 낸다. ROS 계층의 어떤 것도 이 일이 일어나는 중이라고 알려 주지 않는다. 증상은 시간이 갈수록 추종 성능이 나빠지는 제어기다.

**그리고 접촉 모델 — 스택 전체에서 가장 낙관적이던 부분.** 위의 다른 간극은 전부 측정할 수 있는 파라미터다. 접촉은 대개 *모델 형식(model-form)* 오류다. 강체 엔진은 접촉을 시간 스텝마다 푸는 점 구속으로 처리하는데, 실제 충격과 stick–slip 전이는 진짜 불연속이다. Gazebo에서 안정적으로 닫히던 파지가 실물에서 실패하는 이유는 마찰 계수가 틀려서가 아니라 시뮬레이터가 접촉 면적 자체를 표현할 수 없었기 때문인 경우가 많다. [[05-construction-robotics/sim-to-real|Sim-to-Real]]이 이를 제대로 다룬다. 여기서의 실무 규칙은 자유 공간 운동이 접촉보다 훨씬 잘 이전된다는 것이고, 그러니 첫 실기 실험은 자유 공간으로 계획하라.

### 2. 이음매: 하드웨어 인터페이스

시뮬레이션 작업이 이전되는 이유는 `ros2_control`이 *제어기*와 *제어 대상* 사이에 플러그인 경계를 두고, 시뮬레이션이 실제 로봇과 같은 쪽에 앉기 때문이다.

하드웨어 컴포넌트는 세 종류이고 모두 `pluginlib` 플러그인으로 로드된다.

| 종류 | 기반 클래스 | 용도 |
|---|---|---|
| System | `hardware_interface::SystemInterface` | 다자유도 기계, 예: 팔 — read와 write |
| Actuator | `hardware_interface::ActuatorInterface` | 단순 액추에이터 하나 — read와 write |
| Sensor | `hardware_interface::SensorInterface` | 읽기 전용 |

URDF의 `<ros2_control>` 태그가 이미 하나를 지정하고 있다.

```xml
<ros2_control name="MySystem" type="system">
  <hardware>
    <plugin>mock_components/GenericSystem</plugin>
  </hardware>
  <!-- joints and their state/command interfaces -->
</ros2_control>
```

`mock_components/GenericSystem`은 명령을 그대로 상태로 되돌려 주는 컴포넌트다. Gazebo 아래에서는 그 줄이 `gz_ros2_control/GazeboSimSystem`이 된다. 실제 기계에서는 벤더 드라이버 패키지가 내보내는 플러그인 이름이 된다. **그 한 줄이 이음매다.** 제어기, 제어기 설정 YAML, 관절 이름, 토픽 이름, MoveIt, Nav2, 그리고 당신의 노드들은 셋 중 무엇이 로드됐는지 모른다.

이 점은 구체적으로 짚을 값어치가 있다. 앞선 작업을 벤더 토픽에 직접 publish하지 않고 `ros2_control` 안에서 한 가장 강한 이유이기 때문이다. 벤더 고유의 `/my_arm/set_joint_positions` 토픽에 말을 거는 스택은 다음 팔에서 다시 써야 한다. `joint_trajectory_controller`에 말을 거는 스택은 그렇지 않다.

이음매가 온전한지 확인하는 명령:

```bash
ros2 control list_hardware_components
ros2 control list_hardware_interfaces
ros2 control list_controllers
```

첫째는 각 컴포넌트와 플러그인 타입, 생명주기 상태를 찍는다. 둘째는 모든 상태·명령 인터페이스를 이름으로 — `joint_1/position`, `joint_1/velocity` — 찍고, 결정적으로 각 명령 인터페이스가 제어기에 **claim(점유)** 되었는지를 보여 준다. 셋째는 제어기와 그것이 `active`인지를 찍는다. 이 셋이 "왜 안 움직이나" 질문의 거의 전부에 답하고, 그래서 10절에 다시 나온다.

### 3. read, update, write

제어 루프는 `controller_manager` 안의 스레드 하나가 고정 주기로 도는 것이고, 한 주기에 세 가지를 한다.

1. resource manager가 모든 하드웨어 컴포넌트의 `read()`를 호출해 버스에서 상태를 컴포넌트 저장소로 끌어온다.
2. controller manager가 활성 제어기의 `update()`를 호출해 그 상태를 읽고 명령을 만든다.
3. resource manager가 `write()`를 호출해 그 명령을 버스로 내보낸다.

당신이 구현하는 두 메서드의 서명은 이렇고, 시뮬레이션 컴포넌트와 실제 컴포넌트가 동일하다.

```cpp
hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;
```

여기에 생명주기가 붙는다: `on_init`, `on_configure`(연결을 연다), `on_activate`(브레이크를 풀고 파워 스테이지를 켠다), `on_deactivate`, `on_cleanup`, `on_shutdown`, `on_error`. 상태의 의미는 말 그대로다. `INACTIVE`에서는 상태를 읽을 수 있지만 명령 인터페이스는 제공되지 않고, `ACTIVE`에서만 기계가 움직일 수 있다. 모터를 `on_activate`가 아니라 `on_configure`에서 켜는 드라이버는 런치 파일이 시작되는 순간 팔에 전원을 넣는 드라이버이고, 이것은 물리적 결과를 갖는 버그다.

주기는 `controller_manager` 파라미터 `update_rate`이고, Hz 단위 정수, **기본값 100**, 시작 후 읽기 전용이다. 하드웨어가 실제로 감당할 수 있는 값으로 두라. `read()`가 시리얼 왕복에 15 ms 블로킹된다면 1000 Hz 업데이트는 루프가 지킬 수 없는 요구이고, 초과분은 오류가 아니라 지터로 나타난다.

#### 뼈대, 설치된 헤더에서 읽어 온 것

`hardware_interface` **4.48.0** 기준이다. 오늘 Jazzy에서 `apt`가 설치하는 버전이다. 이
버전에서 `SystemInterface`는 `HardwareComponentInterface`의 얇은 하위 클래스이고 `write()`를
순수 가상으로 만든다. 나머지 재정의 대상은 모두 기반 클래스에서 온다. 재정의하는 것이 셋,
그리고 재정의하지 *않는* 큰 것이 하나다.

```cpp
#include "hardware_interface/system_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"

namespace my_robot
{
class MyRobotHardware : public hardware_interface::SystemInterface
{
public:
  // <ros2_control> 블록을 파싱한다. params.hardware_info가 그것을 담는다.
  hardware_interface::CallbackReturn on_init(
    const hardware_interface::HardwareComponentInterfaceParams & params) override;

  // 연결을 열고 닫는다. 여기서는 아무것도 움직여서는 안 된다.
  hardware_interface::CallbackReturn on_configure(const rclcpp_lifecycle::State &) override;
  hardware_interface::CallbackReturn on_cleanup(const rclcpp_lifecycle::State &) override;

  // 전원을 넣고 끈다. ACTIVE에서만 기계가 움직일 수 있다.
  hardware_interface::CallbackReturn on_activate(const rclcpp_lifecycle::State &) override;
  hardware_interface::CallbackReturn on_deactivate(const rclcpp_lifecycle::State &) override;

  // 루프. controller_manager의 update_rate로 돈다.
  hardware_interface::return_type read(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
  hardware_interface::return_type write(
    const rclcpp::Time & time, const rclcpp::Duration & period) override;
};
}  // namespace my_robot
```

`read()` 안에서는 기계가 보고하는 값을 싣고, `write()` 안에서는 제어기가 요청한 값을 내보낸다.
둘 다 URDF가 선언한 인터페이스 이름으로 주소를 붙인다.

```cpp
hardware_interface::return_type MyRobotHardware::read(
  const rclcpp::Time &, const rclcpp::Duration &)
{
  set_state("joint_1/position", encoder_radians_);
  return hardware_interface::return_type::OK;
}

hardware_interface::return_type MyRobotHardware::write(
  const rclcpp::Time &, const rclcpp::Duration &)
{
  const double target = get_command("joint_1/position");
  send_to_drive(target);
  return hardware_interface::return_type::OK;
}
```

작성하지 *않는* 큰 것은 인터페이스 export다. 4.48.0에서는 프레임워크가 URDF의
`<ros2_control>` 블록에서 상태·명령 인터페이스를 만든다. 헤더의 deprecation 문구가 그렇게
적고 있다. `export_state_interfaces()`와 `export_command_interfaces()`에 *"Replaced by ...
on_export_state_interfaces() ... Exporting is handled by the Framework."* 라고 붙어 있다.
`on_export_state_interfaces()`를 재정의하는 것은 URDF가 선언하지 않은 인터페이스를 더할 때뿐이다.
보통은 URDF에 선언하고 위처럼 이름으로 접근한다.

> [!warning] 이 API는 Jazzy 계열 *안에서* 움직였으니 자기 버전을 확인하라
> `on_init(const HardwareInfo &)`는 deprecated이고 위에 보인 `HardwareComponentInterfaceParams` 오버로드가 대신 쓰인다. 옛 export 메서드 둘도 deprecated다. `apt`는 현재 4.48.0을, `jazzy` 브랜치는 4.48.1을 두고 있으며 그 사이에 헤더가 재편됐다. `system_interface.hpp`는 이제 세 줄짜리이고 선언은 `hardware_component_interface.hpp`에 있다. 컴포넌트를 쓰기 전에 `ros2 pkg xml -t version hardware_interface`로 자기 버전을 확인하고 실제로 설치된 헤더를 읽어라. 블로그에서 뼈대를 복사하지 말고, 위의 뼈대도 영구적인 것이 아니라 시점이 박힌 것으로 다뤄라.

### 4. 드라이버, 그리고 믿기 전에 확인할 것

대개는 하드웨어 컴포넌트를 직접 쓰지 않는다. 벤더나 커뮤니티 프로젝트가 배포한다. 그 위에 학위논문을 올리기 전에:

- **당신의 배포판을 대상으로 하는가?** 브랜치가 `humble`뿐인 드라이버는 Jazzy 드라이버가 아니다. README가 아니라 브랜치 목록을 보라.
- **`ros2_control` 하드웨어 컴포넌트인가, 아니면 자기 토픽을 가진 노드인가?** 두 번째가 홍보 문구가 시사하는 것보다 훨씬 흔하고, 그렇다면 2절의 이음매는 당신에게 존재하지 않는다. 써도 되지만 이제 어댑터를 쓰는 쪽은 당신이다.
- **어떤 인터페이스를 export하는가?** `position` 명령 인터페이스만 내보내는 팔은 데이터시트가 무엇을 주장하든 토크나 임피던스 제어기를 돌릴 수 없다. 드라이버가 한계면이기 때문이다.
- **당신 코드를 거치지 않는 비상정지 경로가 있는가?** 사고 나서가 아니라 사기 전에 물어라.
- **연결이 끊기면 어떻게 행동하는가?** 돌아가는 중에 케이블을 뽑아 보라. `ERROR`를 반환하고 비활성화되는 드라이버가 옳다. 마지막 상태를 영원히 계속 반환하는 드라이버는 위험하다. 하류의 모든 노드가 로봇이 마지막 그 자리에 정확히 있다고 믿기 때문이다.
- **진단과 joint state를 명시된 주기로 publish하는가?** 실물에 `ros2 topic hz`를 걸어 문서가 주장하는 값과 비교하는 2분짜리 시험이 사람들의 몇 달을 구한 적이 있다.

### 5. 네트워크를 건너는 DDS

로봇이 한 머신이고 노트북이 다른 머신이 되는 순간, 탐색은 더 이상 보이지 않는 존재가 아니다.

물리는 순서대로의 규칙:

- **`ROS_DOMAIN_ID`가 같아야 한다.** 정수이고, 리눅스에서는 0에서 101 사이를 고르라. 기본 임시 포트 범위 32768–60999를 피하는 구간이다. 두 호스트의 도메인이 다르면 두 시스템은 서로를 전혀 보지 못하고, 오류는 없다.
- **같은 서브넷에 있고 멀티캐스트가 되어야 한다.** 기본 탐색이 멀티캐스트이기 때문이다. Jazzy에는 `ROS_AUTOMATIC_DISCOVERY_RANGE`(값은 `SUBNET`이 기본, `LOCALHOST`, `OFF`, `SYSTEM_DEFAULT`)와 세미콜론으로 구분된 주소 목록 `ROS_STATIC_PEERS`도 있다. 멀티캐스트가 막혀 있거나 두 머신이 한 서브넷이 아닐 때 이 둘을 함께 쓴다.
- **RMW 구현이 양쪽에서 같아야 한다.** 한쪽 `rmw_fastrtps_cpp`, 다른 쪽 `rmw_cyclonedds_cpp`는 상호 운용되지 않는다.
- **시계가 규율되어야 한다.** 두 머신에서 같은 소스를 향해 `chrony`를 돌리고(1 ms 미만이 필요하면 PTP), 둘 다 "NTP"라고 말했으니 일치할 것이라고 가정하지 말고 확인하라.

멀티캐스트는 머신마다 한 명령으로 직접 시험한다.

```bash
# machine A
ros2 multicast receive
```

```bash
# machine B
ros2 multicast send
```

A는 `Received from <address>:<port>: 'Hello World!'` 형태를 찍어야 한다. 안 찍히면 첫 용의자는 방화벽이고, 문서화된 해법은 멀티캐스트 범위에 대한 UDP 송수신을 허용하는 것이다.

```bash
sudo ufw allow in proto udp to 224.0.0.0/4
sudo ufw allow in proto udp from 224.0.0.0/4
```

**다중 머신의 전형적 실패는 두 호스트가 서로의 노드를 다 보면서 데이터가 하나도 흐르지 않는 것이다.** 양쪽에서 `ros2 node list`가 완전하고, 양쪽에서 `ros2 topic list`가 완전하고, 원격 토픽에 `ros2 topic echo`를 걸면 아무것도 안 나온다. *탐색과 데이터가 서로 다른 경로를 탄다*는 것을 알면 신비롭지 않다. 탐색은 잘 알려진 포트로 가는 멀티캐스트이고, 데이터는 참여자마다의 포트로 가는 유니캐스트다. 멀티캐스트 범위만 허용하고 나머지를 막은 방화벽 규칙이 정확히 이 증상을 만든다. 멀티캐스트는 나르면서 유니캐스트를 NAT하는 VPN이나 Docker 브리지도 그렇다. QoS 불일치도 그렇다 — 한쪽에서 같은 침묵을 만드니, QoS를 탓하기 전에 네트워크부터 배제하라. 아니면 오후를 엉뚱한 파일에서 보낸다.

두 번째 전형적 실패는 WiFi에서 큰 메시지에만 나타난다. 카메라 토픽이 한 번에 30초쯤 멈춘다. IP 단편 재조립이다. MTU보다 큰 UDP 데이터그램은 단편화되고, 단편 하나가 유실되면 나머지가 `net.ipv4.ipfrag_time`(기본 30초)이 만료될 때까지 커널 재조립 버퍼를 차지하며, 그 버퍼가 가득 찬 동안에는 다른 무엇도 통과하지 못한다. 문서화된 완화책은 그 토픽에 best-effort QoS, `net.ipv4.ipfrag_time` 낮추기, `net.ipv4.ipfrag_high_thresh` 올리기다. 더 나은 해법은 보통 원본 이미지를 WiFi로 아예 보내지 않는 것이다.

### 6. 실시간을 정직하게

ROS 2는 실시간 시스템이 **아니고**, apt로 설치한다고 마감 시한 보장이 생기지 않는다. 공식 입장은 ROS 2가 실시간 제약을 *염두에 두고 설계되었다*는 것이며, 실시간 데모 자체가 정적 DDS API에 대한 소스 빌드를 요구한다고 — 현재는 Connext만 지원된다고 — 문서화되어 있다.

실시간 커널(RT_PREEMPT)이 주는 것: 유계 스케줄링 지연. 실행 준비가 된 스레드가 알려진 시간 안에 실제로 실행된다. 주지 않는 것: 그 스레드 안의 코드에 관한 어떤 것도. 실시간 동작은 실행 경로에서 비결정적 연산 — 페이지 폴트, 동적 할당과 해제, 무한히 블로킹될 수 있는 동기화 원시 — 을 제거해야 얻어진다. `update()` 안의 `malloc` 하나가 커널의 노력을 전부 무효화한다.

`controller_manager`는 이 계층에서 할 수 있는 일을 하며, 그것이 무엇인지 알아 둘 값어치가 있다.

- 업데이트 스레드가 우선순위 50의 `SCHED_FIFO`를 시도한다. 이를 위해서는 `/etc/security/limits.conf`에서 사용자에게 `rtprio` 한도가 부여되어 있어야 한다. 없으면 시도가 실패하고 조용히 보통 스케줄링이 된다.
- `lock_memory` 파라미터는 페이지 폴트를 피하려고 시작 시 노드 메모리를 물리 RAM에 고정한다. 일반 커널에서는 기본 false, 실시간 커널에서는 true다.

그리고 시스템 설계에 가장 중요한 부분: **경성 타이밍은 ROS 위가 아니라 아래에 산다.** 모터가 타지 않게 지키는 전류 루프는 모터 제어기 안에서 수십 kHz로 돈다. 안전 등급 정지는 안전 릴레이에서 돈다. ROS 2는 이미 더 빠른 루프를 닫고 있는 장치에 100–1000 Hz로 설정값을 보낼 뿐이다. 아키텍처가 ROS 2에게 경성 마감을 지키라고 요구한다면, 튜닝 이전에 아키텍처가 틀린 것이다.

### 7. 안전

기계가 움직일 수 있게 되는 순간 이것은 선택 사항이기를 그만두고, 소프트웨어이기를 그만둔다.

**비상정지는 하드웨어다.** 토픽에 `std_msgs/msg/Bool`을 publish하는 버튼은 비상정지가 아니다. 그것이 막아야 할 대상과 실패 모드를 공유하는 기능일 뿐이다. 진짜 E-stop은 컴퓨터와 독립적으로 전원을 끊거나 브레이크를 거는 하드와이어 회로이고, 의도적으로 리셋할 때까지 래치되며, 소프트웨어가 멈췄을 때도 DDS 링크가 끊겼을 때도 노트북이 잠들었을 때도 동작한다. 스택이 돌아가는 중에 눌러 보고, 그다음 네트워크 케이블을 뽑아서 시험하라.

정지 너머로는: 가능하면 작업 공간을 물리적으로 제한하고(테이블 모서리, 차단물, 짧게 줄인 테더), 전체 범위가 필요 없는 모든 실험에서 속도를 제한하고, 하드웨어가 지원하면 힘을 제한하고, 새 궤적을 처음부터 전속으로 돌리지 마라.

표준의 어휘 — *safety-rated monitored stop*과 *monitored standstill*이 무엇인지, 속도·분리 거리를 어떻게 계산하는지, 팔과 AMR과 토공 기계 각각을 어느 표준으로 읽는지, 판본 표기가 왜 계속 움직이는지 — 는 이미 [[04-robotics/hri-safety|11. HRI & Safety]]에 정리돼 있다. 판본에 민감한 부분은 최신으로 유지할 곳을 하나로 두기 위해 여기서 되풀이하지 않고 거기에 둔다. 사람 곁에서 하는 첫 실험 *전에* 그 절을 읽어라. 주변의 운영 문제는 [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]]가 다룬다.

### 8. 하드웨어 선택: 추천이 아니라 기준

이 쪽은 무엇을 사라고 말하지 않는다. 당신의 실험을 보지 않은 사람은 누구도 그래서는 안 된다.

**먼저 기관을 써라.** 대부분의 공대 학과는 어느 시점에 실제로 쓰이는 것보다 많은 로봇을 이미 보유하고 있고, 유지관리자가 딸린 기존 팔에 접근할 권한이 새 팔의 소유권보다 값어치가 크다. 랩 매니저에게 묻고, 선배에게 어느 기계가 놀고 있는지 묻고, 안전 교육과 위험성 평가를 새로 쓰는 대신 기존의 것에 이름을 올릴 수 있는지 물어라. 빌리는 비용은 일정 조율이고, 사는 비용은 이 절의 마지막 문단 전부다.

**실험이 하드웨어를 고른다.** 흔한 실패는 그 반대다. 플랫폼이 도착하고, 연구 질문이 그 플랫폼이 시연할 수 있는 것으로 조용히 변형된다. 학위논문에 필요한 측정을 먼저 적어라 — 접촉에서의 힘, 센티미터 규모의 배치 정확도, 50 Hz로 도는 정책, 원격조작 시연 수십 시간 — 그다음에야 어느 부류의 기계가 그것을 낼 수 있는지 물어라. 아주 다른 두 플랫폼이 그 요구를 모두 만족한다면, 그 요구는 아직 구매를 정당화할 만큼 구체적이지 않다.

부류와, 각각이 실제로 가르치는 것:

| 부류 | 정말로 가르치는 것 | 가르치지 않는 것 |
|---|---|---|
| 저가형 팔 | 스택 전체 — URDF, 제어기, 캘리브레이션, 하드웨어 이음매, 안전 습관 — 을 고장이 싼 기계 위에서 | 강성, 반복 정밀도, 가반하중, 정확한 힘 제어에 의존하는 어떤 결과도 |
| 원격조작 리그(리더–팔로워, [[01-canonical-papers/notes/7-robotics/gello\|GELLO]]가 기술하는 방식) | 시연 수집, 데이터 양의 인간공학, 데이터셋이 사람 시간으로 얼마인지 | 어떤 종류의 자율성도. 게다가 그런 리그는 보통 단방향이라 데이터에 힘 채널이 없다 |
| 이동 베이스 | 오도메트리 드리프트, 위치 추정, 실제 바닥 위의 Nav2 스택, 한 주행 동안의 전력 예산 | 매니퓰레이션, 접촉, 팔에 관한 어떤 것도 |

그리고 구매 사유서에 아무도 적지 않는 것: **그중 어느 것도 당신의 방법이 논문이 주장하는 규모에서 통하는지를 가르쳐 주지 않는다.** 저가형 팔에서의 결과는 저가형 팔에서의 결과다. 그것으로 충분할 수 있고 — 정직하게 범위를 밝힌 좋은 논문이 많다 — 다만 나중에 방어하는 대신 처음부터 글로 그렇게 범위가 정해져 있어야 한다.

> [!warning] 유지관리 비용은 실재하고, 당신의 연구 시간에서 빠진다
> 물리적 로봇은 연구와 전혀 닮지 않은 일을 만들어 낸다. 간헐적으로 끊기는 케이블, 인터페이스를 바꿔 놓는 펌웨어 업데이트, 다시 조립해야 하는 그리퍼, 배포판 업그레이드에서 깨지는 드라이버, 그리고 기계를 켤 줄 아는 사람이라는 지위에 붙는 반복 세금. 명시적으로 예산에 넣어라. 유지관리자가 당신 혼자라면 한 주의 상당 부분이 로봇의 몫이고, 그것은 학위논문에 쓰려던 몫에서 빠진다.

### 9. 실습: 준비 완료 점검표

아직 하드웨어가 없을 수 있으니, 실습은 하드웨어보다 먼저 오는 산출물이다. 당신의 특정 기계에 대해 이것을 적되, 모든 줄을 *확인 가능*하게 — 실행할 명령이거나 눈으로 볼 물리적 사실이지, 의도가 아니게 — 만들어라.

**전원 전:**

1. E-stop 회로가 배선되어 있고, 그것이 무엇을 끊는지(모터 전원? 로직 전원? 브레이크가 걸리는가?) 찾아보지 않고 말할 수 있다.
2. 기계가 꺼진 상태에서 E-stop을 누르면 측정 가능한 개방 회로가 되거나 벤더가 문서화한 표시가 나온다. 버튼을 버튼으로서 시험했다.
3. 기계의 최대 도달 범위까지 작업 공간이 비어 있고, 첫 전원 투입에는 조작자 외의 사람이 함께 있다.
4. 로봇이 기계적으로 구속되어 있거나, 폴트가 나도 자기 자신을 포함해 무엇 위로도 떨어질 수 없는 자세에 있다.

**소프트웨어, 전부 터미널에서 확인 가능:**

5. `ros2 control list_hardware_components`가 `mock_components/GenericSystem`도 `gz_ros2_control/GazeboSimSystem`도 아닌 실제 컴포넌트를 보여 준다. 기억이 아니라 `<plugin>` 줄을 읽어서 확인하라.
6. `ros2 control list_hardware_interfaces`가 기대하는 명령 인터페이스를 전부 보여 주고, 그것들이 **claim되지 않은** 상태다. 제어기가 이미 활성인 채로 시작하는 것이 아니다.
7. `ros2 param get /controller_manager use_sim_time`이 `False`를 반환하고, 어떤 런치 인자도 이를 true로 만들지 않는다. 여전히 `/clock`을 기다리는 스택은 그냥 틱하지 않는다.
8. `ros2 param get /controller_manager update_rate`가 버스가 감당할 수 있는 값을 반환하고, `read()`가 얼마나 걸리는지 말할 수 있다.
9. URDF의 관절 한계가 기계의 실제 한계와 일치하고, 물려받은 파일을 믿는 대신 최소한 하나는 손으로 확인했다.
10. 처음 활성화할 제어기가 권한이 낮은 것이다 — 먼저 joint state broadcaster, 그다음 감속된 위치 제어. 팔에 전원이 들어간 상태에서 명령을 조립하지 않도록 정확한 `ros2 control switch_controllers` 호출을 지금 적어 두라.
11. 양쪽 머신에서 `chronyc tracking`을 돌렸고, 오프셋이 타임스탬프가 의미를 가질 만큼 작다.
12. 로봇과 노트북 사이에서 `ros2 multicast send` / `ros2 multicast receive`가 통과하고, `ROS_DOMAIN_ID`와 RMW 구현을 양쪽에서 출력해 동일함을 확인했다.
13. 첫 주행의 bag을 기록할 수 있다. `ros2 bag record -a`는 흥미로운 일이 벌어진 뒤가 아니라 전원 투입 전에 시작한다. 이유는 [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]에 있다.

**기술적이지 않은 마지막 줄:** 앞으로 30초 동안 기계가 무엇을 할지, 그리고 그것이 다른 일을 하면 당신이 무엇을 할지를 소리 내어 말할 수 있다.

모든 줄이 기대 출력을 가진 명령이 되고, 당신 없이도 랩의 다른 사람이 그 목록을 돌릴 수 있으면 끝이다.

### 10. 진단할 고장: 시뮬레이션에서는 됐는데 실제 로봇이 아무것도 안 한다

가장 흔한 첫날 증상이고, 어려운 이유는 어디에도 오류 메시지가 없다는 것이다. 이 순서로 진행하고 첫 실패에서 멈춰라. 각 점검은 싸고, 각각이 한 부류 전체를 배제한다.

| # | 점검 | 명령 | 실패의 모습 |
|---|---|---|---|
| 1 | 드라이버가 떠 있기는 한가? | `ros2 node list` | `/controller_manager`가 없거나 벤더 노드가 없다 |
| 2 | 하드웨어 컴포넌트가 로드되어 **active** 상태인가? | `ros2 control list_hardware_components` | `unconfigured`나 `inactive`. `active` 밖에서는 아무것도 움직일 수 없다 |
| 3 | 명령 인터페이스를 제어기가 **claim** 했는가? | `ros2 control list_hardware_interfaces` | 인터페이스는 나열되는데 claim되지 않음 — 제어기가 로드만 되고 활성이 아니다 |
| 4 | 제어기가 활성인가? | `ros2 control list_controllers` | `inactive`, 또는 다른 제어기가 이미 소유한 인터페이스를 claim하지 못한 제어기 |
| 5 | 시계가 공유되고 실제 시계인가? | `ros2 param get /controller_manager use_sim_time`, `chronyc tracking` | `/clock` publisher 없이 `use_sim_time: True` — 루프가 전진하지 않는다 |
| 6 | 두 머신이 도메인에 합의하는가? | 양쪽에서 `echo $ROS_DOMAIN_ID`와 `echo $RMW_IMPLEMENTATION` | 값이 다름. 노드는 보이는데 데이터가 없거나, 아무것도 안 보인다 |
| 7 | E-stop이 래치되어 있나? | 버튼과 드라이브의 폴트 LED를 본다 | 명령은 받아들여지고 상태도 보고되는데 움직임이 0 — 소프트웨어는 멀쩡하고 파워 스테이지가 꺼져 있다 |

7행은 표에서는 마지막이고 실제에서는 첫째다. 경험 있는 사람이 터미널을 열기 전에 확인하는 항목이라는 뜻이다. 이것은 완벽해 보이는 시스템을 만든다. 제어기는 활성이고, 인터페이스는 claim되어 있고, 명령 토픽에 `ros2 topic echo`를 걸면 멀쩡한 숫자가 나오고, 팔은 움직이지 않는다. 래치된 E-stop이나 저전압 폴트가 통신 버스는 살려 둔 채 파워 스테이지만 끊었기 때문이다. 당신의 특정 드라이브의 폴트 표시를 익혀 두라.

일곱 개가 모두 통과하는데도 기계가 움직이지 않으면, 다음 단계는 명령 토픽에 `ros2 topic delay`를 걸어 명령이 늦게 도착하는지 보는 것이고, 그다음은 드라이버 자신의 진단을 읽는 것이다. 그 시점에서 당신은 ROS가 아니라 드라이버를 디버깅하고 있으며, 이는 런치 파일을 다시 읽는 것과는 다르고 더 생산적인 활동이다.

### 11. 이 페이지가 다루지 않는 것

드라이버가 없는 버스를 위한 하드웨어 컴포넌트 작성과 모터 제어기 펌웨어는 둘 다 이 쪽 아래에 있다. 안전 기능의 *인증* — 그럴듯한 것을 구현하는 일과 다르다 — 은 문서와 위험성 평가와 보통 다른 사람이 관여하는 절차이고, 진입점은 [[04-robotics/hri-safety|11. HRI & Safety]]다. 도메인 무작위화, 시스템 식별, 학습된 잔차 모델 — 이전 간극이 제어기가 아니라 정책일 때 손을 뻗는 것들 — 은 [[05-construction-robotics/sim-to-real|Sim-to-Real]]. 플릿 운영, 로깅 인프라, 장기 배치는 [[04-robotics/robot-systems-deployment|Robot Systems & Deployment]]. 트랙의 나머지는 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- `control.ros.org`(Jazzy) — Getting Started(controller manager, resource manager, 하드웨어 컴포넌트, read–update–write 루프); Hardware Components / Writing a Hardware Component; `controller_manager` 문서(`update_rate`, `lock_memory`, `use_sim_time`, `SCHED_FIFO` 우선순위 50과 `rtprio` 한도).
- `ros-controls/ros2_control` `jazzy` 브랜치 — `hardware_interface` 헤더(`SystemInterface`, `read`/`write` 서명, `on_export_*` deprecation), `mock_components_plugin_description.xml`, `ros2controlcli` verb 목록.
- `ros-controls/gz_ros2_control` `jazzy` 브랜치 — `gz_hardware_plugins.xml`(`gz_ros2_control/GazeboSimSystem`).
- ROS 2 Jazzy 문서 — The ROS_DOMAIN_ID; Improved Dynamic Discovery(`ROS_AUTOMATIC_DISCOVERY_RANGE`, `ROS_STATIC_PEERS`); Installation Troubleshooting(멀티캐스트 시험과 `ufw` 규칙); DDS tuning(IP 단편화, `ipfrag_time`, `ipfrag_high_thresh`); Understanding real-time programming.
- 안전 표준은 여기서 되풀이하지 않고 [[04-robotics/hri-safety|11. HRI & Safety]]를 통해 인용한다.

> [!question]- 스스로 점검 · 정답
> **1. 설정에서 시뮬레이터를 모는 것과 실제 팔을 모는 것을 가르는 단 한 줄은 무엇이고, 왜 그것이 나머지 스택을 이전시키는가?** URDF의 `<ros2_control>` 태그 안에 있는 `<plugin>` 줄 — `mock_components/GenericSystem`, `gz_ros2_control/GazeboSimSystem`, 또는 벤더 컴포넌트. 제어기와 그 YAML, 관절 이름, 그 위의 모든 것이 하드웨어가 아니라 controller manager의 인터페이스에 말을 걸기 때문에 어떤 플러그인이 로드됐는지 알 수 없고, 그래서 그대로 이전된다.
> **2. 두 머신이 서로의 노드와 토픽을 다 나열하는데 `ros2 topic echo`는 아무것도 찍지 않는다. 무엇을 먼저 의심하고, 왜 QoS 불일치가 아닌가?** 탐색과 데이터는 경로가 다르다. 탐색은 멀티캐스트, 데이터는 참여자별 포트로 가는 유니캐스트다. 멀티캐스트 범위는 허용하고 유니캐스트를 막는 방화벽이나 NAT가 정확히 이것을 만든다. QoS 불일치도 같은 증상을 주지만 진단이 훨씬 느리므로 네트워크를 먼저 배제한다.
> **3. 지도교수가 RT_PREEMPT 커널을 쓰면 제어 루프가 결정적이 되느냐고 묻는다. 정확한 답은?** 스케줄링 지연을 유계로 만든다 — 실행 준비된 스레드가 알려진 시간 안에 실행된다 — 그리고 그 스레드가 무엇을 하는지에 대해서는 아무것도 하지 않는다. 실행 경로의 페이지 폴트, 동적 할당, 무한 블로킹은 여전히 결정성을 파괴하고, 그래서 `controller_manager`가 `lock_memory`를 제공하고 `SCHED_FIFO`를 시도한다. 그리고 경성 마감은 애초에 ROS에 있으면 안 되고 모터 제어기에 속한다.
> **4. Gazebo에서 성공한 파지가 실물에서 실패한다. "마찰 계수를 튜닝한다"가 왜 보통 틀린 첫수인가?** 접촉 실패는 파라미터 오류가 아니라 모델 형식 오류인 경우가 많기 때문이다. 강체 엔진은 접촉을 시간 스텝마다의 점 구속으로 풀고 실제 접촉 면적을 표현하지 못하므로, 파라미터를 어떤 값으로 해도 그 거동은 복원되지 않는다. 자유 공간 운동은 접촉보다 훨씬 잘 이전되고, 그래서 첫 실기 실험은 자유 공간이어야 한다.
> **5. 토픽으로 구현한 비상정지의 무엇이 잘못됐나?** 그것이 막아야 할 시스템과 실패 모드를 공유한다. executor가 멈췄거나 DDS 링크가 끊겼거나 기계가 네트워크에서 뽑혔다면 메시지는 영영 전달되지 않는다. E-stop은 하드와이어 회로로 전원을 끊거나 브레이크를 걸어야 하고, 래치되어야 하며, 컴퓨터가 꺼진 상태에서도 동작해야 한다.
