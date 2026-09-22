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
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]] for URDF and TF, and [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]] for controllers — MoveIt sits directly on both. Inverse kinematics at the level of [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] helps but is not required. Not required either, and named because the page points at them four times each: where a grasp pose comes from is [[04-robotics/grasping|15. Grasping]], and what happens after contact is [[04-robotics/force-compliance-control|13. Force & Compliance Control]]. Baseline throughout: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, MoveIt 2 from `ros-jazzy-moveit`.
> [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]의 URDF와 TF, [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]의 제어기. MoveIt은 이 둘 위에 바로 앉는다. [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] 수준의 역기구학은 도움이 되지만 필수는 아니다. 역시 필수는 아니지만 이 페이지가 네 번씩 가리키므로 밝혀 둔다: 파지 자세가 어디서 오는지는 [[04-robotics/grasping|15. Grasping]], 접촉 이후는 [[04-robotics/force-compliance-control|13. Force & Compliance Control]]이다. 기준 환경은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**, MoveIt 2는 `ros-jazzy-moveit`.

> [!note] First pass · 처음이라면
> Read the Running object and the picture, then §1 (what MoveIt is not), §2 (what `move_group` talks to), §4 (the pipeline) and §6 (the scene). Then the Worked case, which sits after §11 because it leans on §6–§9, and the §12 exercise, whose last three steps put your own arm into MoveIt. §3, §5 and §7–§11 are reference for the specific call you are making; §13 is the checklist for a plan that will not execute.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] as the *base* the arm is bolted to: a cart on a line, carrying an arm that must reach a panel. P6 is the right object here precisely because MoveIt has no model of it — the planning scene is a snapshot, and the cart keeps moving through it.

*Three objects, stated once.* The arithmetic is done on P6. The exercise (§12) runs first on the stock **Panda** demo, a seven-joint arm with a ready-made configuration, because the planner-family and scene lessons need an arm with room to route around a column. Its last three steps then put **your own two-link arm** from 25.6 and 25.7 into MoveIt, and run the Worked case there where it can run. Step 3's gate becomes $0.01\,\mathrm{rad}$ per joint, $8\,\mathrm{mm}$ at the tip of the straight $0.8\,\mathrm{m}$ arm, and you watch it refuse a plan. Step 4's twenty control ticks per trajectory point become something you read off the planned trajectory. Steps 1 and 2 have no counterpart, because your arm is bolted to `world` (25.7, §11 Step 1) and no base moves under it; a deliberate nudge of the shoulder plays the moving base instead.

| Symbol | Value | What it is here |
|---|---:|---|
| $N$ | $2048$ counts/m | cart encoder, the resolution of the base pose |
| $f_v$ | $50\,\mathrm{Hz}$ | vision supplying the panel pose into the planning scene |
| $f_c$ | $200\,\mathrm{Hz}$ | the `ros2_control` loop the trajectory is executed on |
| $B$ | $70\,\mathrm{ms}$ | P6's camera-to-force budget, which belongs to a different loop from planning |
| $v$ | $0.25\,\mathrm{m/s}$ | cart speed — **page-local**, used only to turn planning latencies into millimetres |
| $T_{\text{plan}}$ | $0.80\,\mathrm{s}$ | one OMPL solve — **page-local** and illustrative, not a benchmark |
| $T_{\text{exec}}$ | $1.50\,\mathrm{s}$ | the resulting trajectory's duration — **page-local** |

*Scope: this page teaches the shape of MoveIt 2 — what `move_group` owns, what the SRDF adds to the URDF, what the pipeline's adapters do, and how a trajectory reaches a controller — and computes what a planner's own latency costs on a base that does not wait. It does not teach where a grasp pose comes from, which is [[04-robotics/grasping|Grasping]]; nor anything from the moment of contact onward, which is [[04-robotics/force-compliance-control|Force & Compliance Control]]; nor the IK and singularity mathematics behind `fraction`, which is [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 492" style="max-width:100%;height:auto" role="img" aria-label="Panel A: perception, move_group and ros2_control side by side; the physical panel and its collision object in the planning scene are joined by a dashed arrow applied once; the follow_joint_trajectory action crosses from move_group to the trajectory controller on P6's 200 Hz loop; the camera has no arrow into ros2_control. Panel B: a seconds axis with the scene snapshot, a 0.80 s plan and a 1.50 s execution, the panel pose aging from 20 ms to 0.82 s to 2.32 s, and a separate millisecond axis with 5 ms control ticks and a 70 ms bracket, unconnected.">
  <text x="8" y="20" font-size="12" fill="currentColor" font-weight="600">A · who believes what</text>
  <line x1="158" y1="42" x2="158" y2="250" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="5 4"/>
  <text x="158" y="37" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">scene update</text>
  <line x1="386" y1="42" x2="386" y2="250" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="5 4"/>
  <text x="386" y="37" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">action</text>
  <text x="83" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">perception</text>
  <text x="276" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">move_group</text>
  <text x="475" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">ros2_control</text>
  <rect x="12" y="64" width="140" height="36" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="18" y="79" font-size="11" fill="currentColor">camera · 50 Hz</text>
  <text x="18" y="94" font-size="11" fill="currentColor" opacity="0.75">publishes a panel pose</text>
  <rect x="36" y="150" width="88" height="14" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2"/>
  <line x1="44" y1="164" x2="49" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="52" y1="164" x2="57" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="60" y1="164" x2="65" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="68" y1="164" x2="73" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="76" y1="164" x2="81" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="84" y1="164" x2="89" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="92" y1="164" x2="97" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="100" y1="164" x2="105" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="108" y1="164" x2="113" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="116" y1="164" x2="121" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="80" y="180" font-size="11" fill="currentColor" text-anchor="middle">panel (physical)</text>
  <line x1="60" y1="100" x2="66" y2="148" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="1.5 3"/>
  <line x1="104" y1="100" x2="96" y2="148" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="1.5 3"/>
  <rect x="166" y="64" width="200" height="178" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <rect x="174" y="74" width="184" height="104" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="182" y="90" font-size="11" fill="currentColor">planning scene</text>
  <rect x="256" y="150" width="88" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 3"/>
  <text x="300" y="128" font-size="11" fill="currentColor" text-anchor="middle">panel as a</text>
  <text x="300" y="142" font-size="11" fill="currentColor" text-anchor="middle">collision object</text>
  <rect x="174" y="188" width="88" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="218" y="204" font-size="11" fill="currentColor" text-anchor="middle">SRDF groups</text>
  <rect x="270" y="188" width="88" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="314" y="204" font-size="11" fill="currentColor" text-anchor="middle">pipeline</text>
  <line x1="126" y1="157" x2="246.5" y2="157" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>
  <polygon points="253,157 246,160.4 246,153.6" fill="currentColor"/>
  <text x="162" y="150" font-size="11" fill="currentColor" font-weight="600">applied once</text>
  <text x="18" y="206" font-size="11" fill="currentColor" opacity="0.75">not a loop: nothing</text>
  <text x="18" y="220" font-size="11" fill="currentColor" opacity="0.75">republishes the scene</text>
  <rect x="404" y="96" width="148" height="42" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="478" y="121" font-size="11" fill="currentColor" text-anchor="middle">trajectory controller</text>
  <rect x="404" y="160" width="148" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="478" y="176" font-size="11" fill="currentColor" text-anchor="middle">P6 loop · 200 Hz</text>
  <text x="478" y="191" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.75">read–update–write</text>
  <line x1="478" y1="138" x2="478" y2="153.5" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="478,160 474.6,153 481.4,153" fill="currentColor"/>
  <text x="396" y="72" font-size="11" fill="currentColor" font-weight="600">follow_joint_trajectory</text>
  <text x="396" y="87" font-size="11" fill="currentColor" opacity="0.8">goal out, result back</text>
  <line x1="366" y1="106" x2="397.5" y2="106" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="404,106 397,109.4 397,102.6" fill="currentColor"/>
  <line x1="404" y1="128" x2="372.5" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="366,128 373,124.6 373,131.4" fill="currentColor"/>
  <text x="8" y="268" font-size="11" fill="currentColor" opacity="0.85">No arrow from the camera into ros2_control: P6's 70 ms chain does not pass through MoveIt.</text>
  <line x1="8" y1="284" x2="552" y2="284" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="8" y="302" font-size="12" fill="currentColor" font-weight="600">B · two clocks, not one</text>
  <path d="M30.0 396.0 L333.6 396.0 L333.6 346.0 L30.0 395.6 Z" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <polyline points="30,395.6 333.6,346" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="30" y1="396" x2="333.6" y2="396" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="30" y="326" font-size="11" fill="currentColor" font-weight="600">age of the panel pose</text>
  <text x="30" y="340" font-size="11" fill="currentColor" opacity="0.75">cart has moved</text>
  <line x1="30" y1="338" x2="30" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <line x1="135.6" y1="338" x2="135.6" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <line x1="333.6" y1="338" x2="333.6" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <text x="34" y="362" font-size="11" fill="currentColor" font-weight="600">20 ms</text>
  <text x="34" y="376" font-size="11" fill="currentColor" opacity="0.75">5.0 mm</text>
  <text x="139.6" y="352.3" font-size="11" fill="currentColor" font-weight="600">0.82 s</text>
  <text x="139.6" y="366.3" font-size="11" fill="currentColor" opacity="0.75">205 mm</text>
  <text x="328.6" y="367" font-size="11" fill="currentColor" text-anchor="end" font-weight="600">2.32 s</text>
  <text x="328.6" y="381" font-size="11" fill="currentColor" text-anchor="end" opacity="0.75">580 mm</text>
  <rect x="30" y="406" width="105.6" height="16" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <rect x="135.6" y="406" width="198" height="16" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <line x1="30" y1="400" x2="30" y2="428" stroke="currentColor" stroke-width="2.6"/>
  <text x="84.8" y="418" font-size="11" fill="currentColor" text-anchor="middle">plan 0.80 s</text>
  <text x="234.6" y="418" font-size="11" fill="currentColor" text-anchor="middle">execute 1.50 s</text>
  <line x1="30" y1="434" x2="360" y2="434" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="30" y1="434" x2="30" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="30" y="450" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="96" y1="434" x2="96" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="96" y="450" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="162" y1="434" x2="162" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="162" y="450" font-size="11" fill="currentColor" text-anchor="middle">1.0</text>
  <line x1="228" y1="434" x2="228" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="228" y="450" font-size="11" fill="currentColor" text-anchor="middle">1.5</text>
  <line x1="294" y1="434" x2="294" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="294" y="450" font-size="11" fill="currentColor" text-anchor="middle">2.0</text>
  <line x1="360" y1="434" x2="360" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="360" y="450" font-size="11" fill="currentColor" text-anchor="middle">2.5</text>
  <text x="360" y="466" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">seconds</text>
  <text x="26" y="466" font-size="11" fill="currentColor" opacity="0.85">↑ scene snapshot</text>
  <rect x="386" y="314" width="166" height="150" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.5"/>
  <text x="394" y="330" font-size="11" fill="currentColor" font-weight="600">milliseconds (magnified)</text>
  <line x1="398" y1="360" x2="398" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="406.9" y1="360" x2="406.9" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="415.8" y1="360" x2="415.8" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="424.6" y1="360" x2="424.6" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="433.5" y1="360" x2="433.5" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="442.4" y1="360" x2="442.4" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="451.2" y1="360" x2="451.2" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="460.1" y1="360" x2="460.1" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="469" y1="360" x2="469" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="477.9" y1="360" x2="477.9" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="486.8" y1="360" x2="486.8" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="495.6" y1="360" x2="495.6" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="504.5" y1="360" x2="504.5" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="513.4" y1="360" x2="513.4" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="522.2" y1="360" x2="522.2" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="531.1" y1="360" x2="531.1" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="540" y1="360" x2="540" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <text x="394" y="352" font-size="11" fill="currentColor" opacity="0.85">5 ms control ticks</text>
  <polyline points="398,392 398,398 522.2,398 522.2,392" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <text x="460.1" y="413" font-size="11" fill="currentColor" text-anchor="middle">70 ms budget</text>
  <line x1="398" y1="424" x2="540" y2="424" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="398" y1="424" x2="398" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="398" y="440" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="433.5" y1="424" x2="433.5" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="433.5" y="440" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <line x1="469" y1="424" x2="469" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="469" y="440" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <line x1="504.5" y1="424" x2="504.5" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="504.5" y="440" font-size="11" fill="currentColor" text-anchor="middle">60</text>
  <line x1="540" y1="424" x2="540" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="540" y="440" font-size="11" fill="currentColor" text-anchor="middle">80</text>
  <text x="550" y="480" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">nothing connects the two axes</text>
</svg>

Panel A shows who believes what: the camera publishes the panel pose at $50\,\mathrm{Hz}$, the planning scene in `move_group` holds that pose as a collision object applied once and never refreshed, and `move_group` reaches the trajectory controller on P6's $200\,\mathrm{Hz}$ loop only through the `follow_joint_trajectory` action, with no arrow from the camera into `ros2_control`. Panel B keeps two clocks apart: on the seconds axis the panel pose ages from $20\,\mathrm{ms}$ at the scene snapshot to $0.82\,\mathrm{s}$ after the $0.80\,\mathrm{s}$ plan and $2.32\,\mathrm{s}$ after the $1.50\,\mathrm{s}$ execution while the cart moves $5.0$, $205$ and $580\,\mathrm{mm}$, and the millisecond inset holds the $5\,\mathrm{ms}$ control ticks and P6's $70\,\mathrm{ms}$ budget, with nothing connecting the two axes.

### 1. What MoveIt 2 is, and three things it is not

You have an arm that moves when you send it a joint trajectory ([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). You want it to reach a pose on the other side of a column without hitting the column, the scaffolding, or itself. Writing that trajectory by hand means solving inverse kinematics (finding the joint angles that put the tool at a requested pose; [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]), then searching a seven-dimensional configuration space (the space of all joint-angle vectors, one axis per joint; see [[04-robotics/modern-robotics/ch02-configuration-space|MR Ch.02 — Configuration Space]]) for a collision-free path, then assigning times to it that no joint's velocity or acceleration limit forbids. MoveIt 2 is the assembled, plugin-based answer to exactly that problem, and it is the standard one in ROS 2.

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

That launch starts `move_group`, RViz with the MotionPlanning display, `robot_state_publisher`, and a ros2_control stack whose hardware is `mock_components/GenericSystem`, which loops commands back as states ([[04-robotics/ros2/from-simulation-to-hardware|25.11]]) — which is why a plan executes on a machine with no robot attached. In another sourced terminal:

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

The URDF says the robot has joints named `panda_joint1` through `panda_joint7` and a hand. It does not say which of those constitute "the arm", what "home" means, which link is the tip you are planning the pose of, or which link pairs can never collide because they are adjacent. A planner cannot start without all four. That semantic layer is the **SRDF** (Semantic Robot Description Format; `robot_description_semantic`), and its central concept is the **planning group**: a named set of joints that a request can target.

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

What each stage buys you. The first four are request-side checks, which run before the planner and can stop it from running at all:

- `ResolveConstraintFrames` rewrites constraints expressed in an object's subframe into a frame the planner knows.
- `ValidateWorkspaceBounds` supplies a default workspace when the request omits one, so a sampling planner has somewhere bounded to sample. In Jazzy that default is the `default_workspace_bounds` parameter, whose value is `1000000000000.0` — a cube edge of 1e12 m, effectively unbounded, with the source carrying a TODO saying it should have been infinity. If you need a real bound, set it yourself; do not assume the 10 m cube that older MoveIt hardcoded.
- `CheckStartStateBounds` **rejects** a start state outside a joint limit — `START_STATE_INVALID`, and the planner never runs. It does not nudge a revolute joint back inside. The one thing it will rewrite is the *rotation* of continuous, planar and floating joints, and only when `fix_start_state` is true, which defaults to false. Real encoders do report values slightly past limits, and this adapter is what turns that into a failure rather than what absorbs it.
- `CheckStartStateCollision` reports a start state in collision and stops there — `START_STATE_IN_COLLISION`, with the contacts in the message. It does not sample a nearby free state. The plugin description still advertises the ROS 1 behaviour, which was not carried over; the source only sets the error code. Fix the scene or the start state yourself.

The remaining stages are response-side processing, which runs on the planner's output:

- `AddTimeOptimalParameterization` is the stage that turns a geometric path into a trajectory obeying joint velocity and acceleration limits. **The planner does not produce timing.** Path and trajectory are different objects, and this is where the difference is made.
- `ValidateSolution` re-checks the finished trajectory. `DisplayMotionPath` publishes it for RViz.

Two consequences. First, a failure message naming an adapter (`CheckStartStateBounds`) is not a planner failure — the planner never ran. Second, the order in that list *is* the execution order, so where you put an adapter matters. But put it in the right list: `AddRuckigTrajectorySmoothing` is registered as `default_planning_response_adapters/AddRuckigTrajectorySmoothing`, a **response** adapter, and belongs under `response_adapters` after `AddTimeOptimalParameterization`. Under `request_adapters` it fails to load at `move_group` startup. Some upstream config comments still show the old request-adapter spelling.

### 5. The planner families, and which one you actually want

Jazzy ships four, all separately packaged, all selectable per request by `planning_pipeline` and `planner_id`.

| Family | Package | What it is for |
|---|---|---|
| **OMPL** (sampling) | `moveit_planners_ompl` | The default. RRTConnect and relatives: fast in high dimensions and cluttered scenes, probabilistically complete (if a path exists, the chance of finding it approaches 1 as it runs longer, but it cannot prove that none exists), **not deterministic** — the same request gives a different path each run |
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

In Python, the scene is edited through the planning scene monitor. These snippets need the MoveIt configuration (URDF, SRDF, kinematics, planning pipelines) as parameters, so run them from a launch file built with `MoveItConfigsBuilder`, or pass `MoveItPy(..., config_dict=...)`; a bare `python3` invocation has no robot model:

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

It interpolates the end-effector pose at `eef_step` intervals and solves IK at each one. **The return value is the fraction of the requested path it achieved, between 0.0 and 1.0, or -1.0 on error**, and you must check it. A partial result is the normal outcome, for reasons that are all geometric rather than algorithmic: the straight line leaves the reachable workspace; it passes through or near a singularity where the IK solution degenerates (a configuration where the arm loses the ability to move its tip in some direction, so nearby poses demand very large joint motions; see [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR Ch.05 — Velocity Kinematics & Statics]] §4); the interpolation crosses a branch of the IK solution and the nearest solution is a wrist flip; or an interpolated pose is in collision. (In Jazzy the older `jump_threshold` argument is deprecated and dropped from the current overload.)

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

Planning takes hundreds of milliseconds and assumes a static goal. Visual servoing onto a moving target, or teleoperating a tool by hand, does not fit that. `moveit_servo` (`ros-jazzy-moveit-servo`) is the other mode: it converts a streaming command into joint commands at control rate, with no planning at all. It accepts joint jog (individual joint velocities), twist (a desired end-effector velocity) and pose commands, and it outputs a `KinematicState` — joint names, positions, velocities, accelerations — or a trajectory/float-array topic through the ROS interface. It scales velocity down near singularities and near collisions, both on by default; collision checking can be turned off with `check_collisions`, while singularity slowdown has no switch and is tuned through its thresholds.

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

### Worked case · 대상으로 한 번 끝까지

This is the homework object. It sits here, after §11, because every step leans on a section above it: the planning scene (§6), the Cartesian path (§7), the execution gate (§8) and Servo (§9). The arithmetic is the catalog plus the three page-local durations; the problem set changes one of them, and the exercise that follows runs Steps 3 and 4 on your own arm.

**Step 1 — the scene is a photograph.** The planner reads the planning scene once, when the request starts. The panel pose in it came from vision, so at that instant it is already up to one vision period old:

$$a_0 = T_v = \frac{1}{50} = 20\,\mathrm{ms},$$

because nothing can be fresher than the last frame. Planning then runs for $T_{\text{plan}}$ and execution for $T_{\text{exec}}$, and §6 is explicit that nothing refreshes a collision object unless your code republishes it. So the age of the belief at the two later boundaries is

$$a_1 = a_0 + T_{\text{plan}} = 0.020 + 0.80 = 0.82\,\mathrm{s},\qquad a_2 = a_1 + T_{\text{exec}} = 0.82 + 1.50 = 2.32\,\mathrm{s}.$$

**Step 2 — the age in millimetres and counts.** At the page-local $v$, the cart carrying the arm has moved $d=v\,a$ while the scene did not:

| Boundary | age | $d=va$ | counts |
|---|---:|---:|---:|
| scene read | $20\,\mathrm{ms}$ | $5.0\,\mathrm{mm}$ | $10.2$ |
| plan returned | $0.82\,\mathrm{s}$ | $205\,\mathrm{mm}$ | $420$ |
| trajectory finished | $2.32\,\mathrm{s}$ | $580\,\mathrm{mm}$ | $1188$ |

Over half a metre, and every joint angle in the trajectory was computed for the first row. This is not a MoveIt defect: the planner solved exactly the problem it was given, on a world someone told it was static. The defect is in the caller that let the base move.

**Step 3 — MoveIt's own gate, read in P6's units.** §8's `allowed_start_tolerance: 0.01` is how far the current state may differ from the trajectory's first point before execution is refused. For a prismatic cart joint that is $0.01\,\mathrm{m}$, which is

$$0.01\times 2048 = 20.5\ \text{counts},\qquad \frac{0.01\,\mathrm{m}}{0.25\,\mathrm{m/s}} = 40\,\mathrm{ms},$$

since the tolerance is a distance and the cart crosses it at the page-local speed. Forty milliseconds. The gate that decides whether execution begins at all is crossed in less time than P6 allots to a whole camera-to-force chain, $40 < 70$. On a moving base, plan-then-execute-later is not a slow design, it is a design that will not start. Either stop the base before planning, or use Servo (§9), which has no plan to go stale.

**Step 4 — what the $200\,\mathrm{Hz}$ loop does with the trajectory.** The response adapter `AddTimeOptimalParameterization` is what gives the path timing (§4); suppose it emits points $100\,\mathrm{ms}$ apart. Then

$$\frac{100\,\mathrm{ms}}{T_c} = \frac{0.100}{0.005} = 20,$$

so twenty control cycles fall between consecutive trajectory points and the controller interpolates across them ([[04-robotics/ros2/simulation-and-control|25.7 §11]]). The trajectory is coarse and the loop is fine, and that is the intended division: MoveIt says where and when, `ros2_control` says how often.

**Step 5 — `fraction`, as a distance rather than a ratio.** Take a $0.20\,\mathrm{m}$ insertion line at §7's `eef_step` of $0.01\,\mathrm{m}$. That is $0.20/0.01 = 20$ interpolated poses and $20$ IK solves, each step being $0.01\times2048=20.5$ encoder counts of base motion — comparable to the whole start tolerance, which is worth noticing. A return of $0.62$ then means the tool reaches $0.20\times0.62=0.124\,\mathrm{m}$ and stops $0.076\,\mathrm{m}$ short: $76\,\mathrm{mm}$, or $156$ counts, of unfinished slot, with the tool halted in mid-air at a pose nobody chose. §7's rule follows directly — the number is a fraction of *your* line, so read it back in the units of the line.

**Step 6 — the two budgets, kept apart.** Nothing in Steps 1 to 5 violates P6's $70\,\mathrm{ms}$, because that budget measures camera mid-exposure to applied force on the cart's own $200\,\mathrm{Hz}$ loop, and planning is not on that chain. A $0.80\,\mathrm{s}$ plan is not a budget failure. A panel pose that reaches the *scene* $200\,\mathrm{ms}$ late is not a MoveIt failure either — MoveIt will plan against it without complaint. Both are failures of the caller to say which clock each number belongs to, and Step 3 is what happens when the two are finally forced to meet.

### 12. Exercise: plan, execute, then put a column in the way

Two sittings: steps 1–7 on the Panda demo, steps 8–10 on your own arm. Nothing here needs hardware.

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
8. **Your arm, in MoveIt.** Copy your 25.7 description into a package's `urdf/` folder (25.4) as `two_link_arm_moveit.urdf.xacro`, and delete its `<ros2_control>` and `<gazebo>` blocks. The Assistant keeps any `<ros2_control>` block it finds, and a Gazebo hardware plugin cannot load outside Gazebo; with the block gone it writes its own `mock_components/GenericSystem` block, the same loop-back hardware as the Panda demo. Keep the `world` link, so no virtual joint is needed. Run `ros2 run moveit_setup_assistant moveit_setup_assistant` and walk §3's list: load the copy; generate the self-collision matrix; add a planning group `arm`, a kinematic chain from `base_link` to `link2`; add two robot poses, `home` (both joints $0$) and `raised` (`shoulder` $0.8$, `elbow` $-1.0$, the pose 25.7's Step 6 commanded); accept the defaults for ros2_control, ROS 2 controllers and MoveIt controllers; generate `two_link_arm_moveit_config` into your workspace. In its `config/ros2_controllers.yaml`, change `update_rate: 100` to `200`, P6's $f_c$ and 25.7's. Build, source, and `ros2 launch two_link_arm_moveit_config demo.launch.py`.
9. **Plan between named poses, and read Step 4 off the plan.** On the **Planning** tab set *Goal State* to `raised`, then **Plan** and **Execute**. Dragging the marker mostly fails, and that is correct: two joints reach only a two-dimensional set of tip positions in the x–z plane, so almost no pose you drag to has an IK solution. Now `ros2 topic echo /display_planned_path --once` and read the `time_from_start` of successive points. They step by $0.1\,\mathrm{s}$ (the last step may be shorter), the default `resample_dt` of `AddTimeOptimalParameterization`, so at `update_rate: 200` twenty control ticks fall between points: the Worked case's $0.100/0.005=20$, on your arm.
10. **Watch the start gate refuse.** Set *Goal State* to `home` and **Plan**, but do not execute. In a second terminal, move the arm under MoveIt's feet through its controller; the Assistant names it `arm_controller` for a group called `arm`, and `ros2 control list_controllers` confirms:

```bash
ros2 topic pub -1 /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.85, -1.0], time_from_start: {sec: 1}}]}"
```

Now press **Execute**. `move_group` refuses with *Invalid Trajectory: start point deviates from current robot state more than 0.01 at joint 'shoulder'*. The plan was computed for a shoulder at $0.80\,\mathrm{rad}$; it is now at $0.85$, five times the $0.01\,\mathrm{rad}$ gate. That is the Worked case's Step 3 on your arm, with the nudge standing in for the moving cart. Apply Step 3's first fix, stop the base and plan again from where the robot now is: **Plan**, then **Execute**, and it runs.

You are done when you can state which of the Panda's last two plans you would trust near a wall and why, and when you can predict, before pressing **Execute**, whether a nudge of a given size will be refused.

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

### Self-check

1. Your plan is beautiful in RViz and the arm does not move. What are the first three commands?
2. Why is the URDF insufficient for MoveIt, in one sentence?
3. `computeCartesianPath` returns 0.62. What do you do, and what are the likely causes?
4. You close the gripper on a block and every subsequent plan fails in collision. Why?
5. Which parts of a construction-site pick does MoveIt not solve?
6. On P6, the worked case finds that `allowed_start_tolerance: 0.01` corresponds to $40\,\mathrm{ms}$ of cart motion. A colleague proposes raising it to $0.10$ so execution stops being refused. What does that buy, what does it cost, and what is the fix they are avoiding?

> [!tip]- Answers
> 1. `ros2 control list_controllers` (is a controller active?), a comparison of its name against `controller_names` in `moveit_controllers.yaml`, and `ros2 action list | grep follow_joint_trajectory` (is the action server there?). All three are the wiring layer, and wiring failures are instant and silent — check them before touching tolerances.
> 2. It describes geometry and kinematics but carries no semantics: no planning groups, no named poses, no tip link, no disabled collision pairs — all of which live in the SRDF and all of which a planner needs before it can accept a request.
> 3. Do not execute it — that would stop the tool 62 % of the way along a line you chose for a reason. Likely causes are the line leaving the reachable workspace, passing near a singularity, crossing to a different IK branch, or an interpolated pose in collision. Either shorten or reorient the segment, or use Pilz `LIN`, which fails cleanly instead of partially.
> 4. The block is still a world collision object and the gripper is now inside it. Attach it to the gripper link with the gripper's links listed as `touch_links`, which moves it into the robot's own collision model.
> 5. Where the grasp pose is — that is grasp synthesis from perception — and everything from the moment of contact onward, since MoveIt's world model treats contact as failure. It solves only the collision-free motion between those two.
> 6. It buys ten times the window: $0.10\,\mathrm{m}$ is $205$ counts and $0.10/0.25=0.40\,\mathrm{s}$ of cart motion, so execution starts where it used to refuse. What it costs is the guarantee the parameter exists for — the trajectory's first point is now allowed to be $0.10\,\mathrm{m}$ from where the robot actually is, and the controller will drag the arm to it, through whatever is in between, as a motion nobody planned. The refusal was not the problem; it was the only thing reporting the problem. The fix being avoided is in Step 1: the scene was $0.82\,\mathrm{s}$ stale before execution even began, so either stop the base while planning and executing, or drop planning for Servo (§9), which tracks a moving target and has no stale plan to start from.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]] as the mobile base a planner must not treat as instant. Vision $50\,\mathrm{Hz}$ supplies a panel pose; the cart controller is $200\,\mathrm{Hz}$; budget $70\,\mathrm{ms}$. No new simulator.

1. **Draw.** P6 cart, a panel, MoveIt's planning scene. Mark `/goal` from vision, the `follow_joint_trajectory` action, and the $200\,\mathrm{Hz}$ controller underneath. Five-line timeline: a $2\,\mathrm{s}$ plan, then execution ticks at $5\,\mathrm{ms}$, with the $70\,\mathrm{ms}$ sensing budget on a *different* clock from planning.
2. **Derive.** (a) Why a $2\,\mathrm{s}$ plan does not violate the $70\,\mathrm{ms}$ budget — which loop owns which number. (b) Encoder $\Delta p$ for one count, as the base-pose resolution the scene is *not* given. (c) `computeCartesianPath` returns $0.62$. Execute?
3. **Interpret.** The plan is beautiful in RViz and the cart never moves. First three commands. Separately: a $200\,\mathrm{ms}$-late panel pose in the scene — is that a MoveIt bug or a P6 budget bug?

> [!note]- How to draw it · 그리는 법
> - Three regions side by side with two labelled boundaries between them: `perception` (the $50\,\mathrm{Hz}$ camera publishing the panel pose), `move_group` (the planning scene, the SRDF groups, the pipeline), `ros2_control` (the trajectory controller on P6's $200\,\mathrm{Hz}$ loop).
> - Draw the panel twice — the physical object on the left, a collision object inside the planning scene — and join the two with a dashed arrow labelled `applied once`.
> - That dashed arrow is not a feedback loop: nothing republishes the scene unless your code does.
> - The boundary between `move_group` and `ros2_control` carries an action, `follow_joint_trajectory`, not a topic, because MoveIt is an action client and needs the result.
> - The camera has no arrow at all into `ros2_control`: P6's $70\,\mathrm{ms}$ budget lives on a chain MoveIt is not part of.
> - Two axes: seconds, with `scene snapshot`, `plan` and `execute` laid end to end, and a separate millisecond inset with the $5\,\mathrm{ms}$ control ticks and one $70\,\mathrm{ms}$ bracket; connect nothing between them, because the gap is the figure's argument.
> - Above the seconds axis, a bar labelled `age of the panel pose` that grows from left to right, with its value written at the three boundaries (worked case, $0.80\,\mathrm{s}$ plan: $20\,\mathrm{ms}$, $0.82\,\mathrm{s}$, $2.32\,\mathrm{s}$).

> [!tip]- Solutions
> 1. Scene holds the panel; MoveIt talks to the trajectory controller, not to the camera. Planning seconds; control milliseconds; the $70\,\mathrm{ms}$ is camera-to-force, not planner-to-scene.
> 2. (a) $70\,\mathrm{ms}$ is the sensing/control chain; planning is allowed to be slow if execution still samples at $200\,\mathrm{Hz}$. (b) $0.488\,\mathrm{mm}$, invisible to a scene that was painted once. (c) No — stop at 62% of a line you chose.
> 3. `list_controllers`, match `controller_names`, `ros2 action list | grep follow_joint_trajectory`. The late pose is a P6 budget bug: MoveIt will happily plan against a stale scene.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 팔에 MoveIt 2를 설정하고, 직접 채운 씬에 대해 계획·실행하고, 흔한 실행 실패를 진단할 정도. 플래너나 파지 합성기를 직접 쓸 정도는 아니다.
> **Working** — enough to configure MoveIt 2, plan and execute against a scene you control, and diagnose the common execution failure.

> [!note] 선수 지식 · Prerequisites
> URDF와 TF는 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]], 제어기는 [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]. MoveIt은 이 둘 위에 바로 앉는다. [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] 수준의 역기구학은 도움이 되지만 필수는 아니다. 기준 환경은 **Ubuntu 24.04의 ROS 2 Jazzy Jalisco**, MoveIt 2는 `ros-jazzy-moveit`.
> URDF/TF from 25.6 and controllers from 25.7; Grasping and Force & Compliance Control named, not required; baseline ROS 2 Jazzy on Ubuntu 24.04.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상과 그림을 보고, §1(MoveIt이 아닌 것), §2(`move_group`이 누구와 말하는가), §4(파이프라인), §6(씬)을 읽어라. 그다음 Worked case로 가라. §6–§9에 기대므로 §11 뒤에 있다. 이어서 §12 실습을 하라. 그 마지막 세 단계가 당신의 팔을 MoveIt에 넣는다. §3, §5, §7–§11은 지금 부르는 호출에 맞춰 찾아보는 참고 자료이고, §13은 실행되지 않는 계획을 위한 점검표다.

### 이 페이지의 대상 · Running object

팔이 볼트로 얹힌 *베이스*로 쓰는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**. 직선 위 카트가 팔을 싣고 패널에 닿아야 한다. 여기서 P6가 맞는 대상인 이유는 바로 MoveIt이 그것의 모델을 갖고 있지 않다는 데 있다. planning scene은 스냅샷이고, 카트는 그 사이에도 계속 움직인다.

*대상이 셋이라는 것을 한 번 밝혀 둔다.* 계산은 P6 위에서 한다. 실습(§12)은 먼저 기성 **Panda** 데모에서 돈다. 설정이 다 갖춰진 7관절 팔이고, 플래너 계열과 씬의 교훈에는 기둥을 돌아갈 여유가 있는 팔이 필요하기 때문이다. 그 마지막 세 단계는 25.6과 25.7에서 만든 **당신의 2링크 팔** 자체를 MoveIt에 넣고, Worked case를 돌릴 수 있는 곳에서는 거기서 돌린다. Step 3의 관문은 관절당 $0.01\,\mathrm{rad}$, 곧게 편 $0.8\,\mathrm{m}$ 팔의 끝에서 $8\,\mathrm{mm}$가 되고, 그것이 계획을 거부하는 모습을 직접 본다. Step 4의 궤적 점당 제어 틱 스무 개는 계획된 궤적에서 읽어 내는 값이 된다. Step 1과 2에는 짝이 없다. 당신의 팔은 `world`에 볼트로 고정되어 있어(25.7의 §11 1단계) 그 아래 움직이는 베이스가 없기 때문이다. 대신 어깨를 일부러 살짝 미는 것이 움직이는 베이스 역할을 한다.

| 기호 | 값 | 여기서의 뜻 |
|---|---:|---|
| $N$ | $2048$ counts/m | 카트 엔코더. 베이스 자세의 분해능 |
| $f_v$ | $50\,\mathrm{Hz}$ | planning scene에 패널 자세를 넣는 비전 |
| $f_c$ | $200\,\mathrm{Hz}$ | 궤적이 실행되는 `ros2_control` 루프 |
| $B$ | $70\,\mathrm{ms}$ | P6의 카메라–힘 예산. 계획과는 다른 루프에 속한다 |
| $v$ | $0.25\,\mathrm{m/s}$ | 카트 속도 — **페이지 국소 값**. 계획 지연을 밀리미터로 바꾸는 데에만 쓴다 |
| $T_{\text{plan}}$ | $0.80\,\mathrm{s}$ | OMPL 한 번의 해 — **페이지 국소 값**이고 예시다. 벤치마크가 아니다 |
| $T_{\text{exec}}$ | $1.50\,\mathrm{s}$ | 그 결과 궤적의 지속 시간 — **페이지 국소 값** |

*범위: 이 페이지는 MoveIt 2의 모양 — `move_group`이 무엇을 소유하는지, SRDF가 URDF에 무엇을 더하는지, 파이프라인의 어댑터가 무슨 일을 하는지, 궤적이 어떻게 제어기에 닿는지 — 을 가르치고, 기다려 주지 않는 베이스 위에서 플래너 자신의 지연이 얼마를 치르는지 계산한다. 파지 자세가 어디서 오는지는 가르치지 않는다. 그것은 [[04-robotics/grasping|파지]]다. 접촉 순간 이후도 아니다. 그것은 [[04-robotics/force-compliance-control|힘·컴플라이언스 제어]]다. `fraction` 뒤의 역기구학과 특이점 수학도 아니다. 그것은 [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 492" style="max-width:100%;height:auto" role="img" aria-label="패널 A: 지각, move_group, ros2_control이 나란히 있고, 실제 패널과 planning scene 안의 collision object가 한 번만 적용이라는 점선 화살표로 이어지며, follow_joint_trajectory 액션이 move_group에서 P6의 200 Hz 루프 위 궤적 제어기로 건너가고, 카메라에서 ros2_control로 가는 화살표는 없다. 패널 B: 초 축 위에 씬 스냅샷, 0.80 s 계획, 1.50 s 실행이 있고 패널 자세의 나이가 20 ms에서 0.82 s, 2.32 s로 자라며, 5 ms 제어 틱과 70 ms 괄호를 담은 밀리초 축이 따로 있고 둘은 이어지지 않는다.">
  <text x="8" y="20" font-size="12" fill="currentColor" font-weight="600">A · 누가 무엇을 믿는가</text>
  <line x1="158" y1="42" x2="158" y2="250" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="5 4"/>
  <text x="158" y="37" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">씬 갱신</text>
  <line x1="386" y1="42" x2="386" y2="250" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55" stroke-dasharray="5 4"/>
  <text x="386" y="37" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">액션</text>
  <text x="83" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">지각</text>
  <text x="276" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">move_group</text>
  <text x="475" y="52" font-size="12" fill="currentColor" text-anchor="middle" font-weight="600">ros2_control</text>
  <rect x="12" y="64" width="140" height="36" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="18" y="79" font-size="11" fill="currentColor">카메라 · 50 Hz</text>
  <text x="18" y="94" font-size="11" fill="currentColor" opacity="0.75">패널 자세를 발행</text>
  <rect x="36" y="150" width="88" height="14" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.2"/>
  <line x1="44" y1="164" x2="49" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="52" y1="164" x2="57" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="60" y1="164" x2="65" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="68" y1="164" x2="73" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="76" y1="164" x2="81" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="84" y1="164" x2="89" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="92" y1="164" x2="97" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="100" y1="164" x2="105" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="108" y1="164" x2="113" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <line x1="116" y1="164" x2="121" y2="150" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6"/>
  <text x="80" y="180" font-size="11" fill="currentColor" text-anchor="middle">패널 (실물)</text>
  <line x1="60" y1="100" x2="66" y2="148" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="1.5 3"/>
  <line x1="104" y1="100" x2="96" y2="148" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="1.5 3"/>
  <rect x="166" y="64" width="200" height="178" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <rect x="174" y="74" width="184" height="104" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="182" y="90" font-size="11" fill="currentColor">planning scene</text>
  <rect x="256" y="150" width="88" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 3"/>
  <text x="300" y="128" font-size="11" fill="currentColor" text-anchor="middle">collision object</text>
  <text x="300" y="142" font-size="11" fill="currentColor" text-anchor="middle">로서의 패널</text>
  <rect x="174" y="188" width="88" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="218" y="204" font-size="11" fill="currentColor" text-anchor="middle">SRDF 그룹</text>
  <rect x="270" y="188" width="88" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="314" y="204" font-size="11" fill="currentColor" text-anchor="middle">파이프라인</text>
  <line x1="126" y1="157" x2="246.5" y2="157" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 3"/>
  <polygon points="253,157 246,160.4 246,153.6" fill="currentColor"/>
  <text x="162" y="150" font-size="11" fill="currentColor" font-weight="600">한 번만 적용</text>
  <text x="18" y="206" font-size="11" fill="currentColor" opacity="0.75">루프가 아니다: 씬을</text>
  <text x="18" y="220" font-size="11" fill="currentColor" opacity="0.75">다시 발행하는 것은 없다</text>
  <rect x="404" y="96" width="148" height="42" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="478" y="121" font-size="11" fill="currentColor" text-anchor="middle">궤적 제어기</text>
  <rect x="404" y="160" width="148" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="478" y="176" font-size="11" fill="currentColor" text-anchor="middle">P6 루프 · 200 Hz</text>
  <text x="478" y="191" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.75">read–update–write</text>
  <line x1="478" y1="138" x2="478" y2="153.5" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="478,160 474.6,153 481.4,153" fill="currentColor"/>
  <text x="396" y="72" font-size="11" fill="currentColor" font-weight="600">follow_joint_trajectory</text>
  <text x="396" y="87" font-size="11" fill="currentColor" opacity="0.8">목표를 보내고 결과를 기다린다</text>
  <line x1="366" y1="106" x2="397.5" y2="106" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="404,106 397,109.4 397,102.6" fill="currentColor"/>
  <line x1="404" y1="128" x2="372.5" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="366,128 373,124.6 373,131.4" fill="currentColor"/>
  <text x="8" y="268" font-size="11" fill="currentColor" opacity="0.85">카메라에서 ros2_control로 가는 화살표는 없다. P6의 70 ms 사슬은 MoveIt을 지나지 않는다.</text>
  <line x1="8" y1="284" x2="552" y2="284" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="8" y="302" font-size="12" fill="currentColor" font-weight="600">B · 시계는 하나가 아니라 둘</text>
  <path d="M30.0 396.0 L333.6 396.0 L333.6 346.0 L30.0 395.6 Z" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <polyline points="30,395.6 333.6,346" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="30" y1="396" x2="333.6" y2="396" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="30" y="326" font-size="11" fill="currentColor" font-weight="600">패널 자세의 나이</text>
  <text x="30" y="340" font-size="11" fill="currentColor" opacity="0.75">카트가 간 거리</text>
  <line x1="30" y1="338" x2="30" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <line x1="135.6" y1="338" x2="135.6" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <line x1="333.6" y1="338" x2="333.6" y2="426" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.45" stroke-dasharray="2 2"/>
  <text x="34" y="362" font-size="11" fill="currentColor" font-weight="600">20 ms</text>
  <text x="34" y="376" font-size="11" fill="currentColor" opacity="0.75">5.0 mm</text>
  <text x="139.6" y="352.3" font-size="11" fill="currentColor" font-weight="600">0.82 s</text>
  <text x="139.6" y="366.3" font-size="11" fill="currentColor" opacity="0.75">205 mm</text>
  <text x="328.6" y="367" font-size="11" fill="currentColor" text-anchor="end" font-weight="600">2.32 s</text>
  <text x="328.6" y="381" font-size="11" fill="currentColor" text-anchor="end" opacity="0.75">580 mm</text>
  <rect x="30" y="406" width="105.6" height="16" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <rect x="135.6" y="406" width="198" height="16" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <line x1="30" y1="400" x2="30" y2="428" stroke="currentColor" stroke-width="2.6"/>
  <text x="84.8" y="418" font-size="11" fill="currentColor" text-anchor="middle">계획 0.80 s</text>
  <text x="234.6" y="418" font-size="11" fill="currentColor" text-anchor="middle">실행 1.50 s</text>
  <line x1="30" y1="434" x2="360" y2="434" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="30" y1="434" x2="30" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="30" y="450" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="96" y1="434" x2="96" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="96" y="450" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
  <line x1="162" y1="434" x2="162" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="162" y="450" font-size="11" fill="currentColor" text-anchor="middle">1.0</text>
  <line x1="228" y1="434" x2="228" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="228" y="450" font-size="11" fill="currentColor" text-anchor="middle">1.5</text>
  <line x1="294" y1="434" x2="294" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="294" y="450" font-size="11" fill="currentColor" text-anchor="middle">2.0</text>
  <line x1="360" y1="434" x2="360" y2="438" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="360" y="450" font-size="11" fill="currentColor" text-anchor="middle">2.5</text>
  <text x="360" y="466" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">초</text>
  <text x="26" y="466" font-size="11" fill="currentColor" opacity="0.85">↑ 씬 스냅샷</text>
  <rect x="386" y="314" width="166" height="150" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.5"/>
  <text x="394" y="330" font-size="11" fill="currentColor" font-weight="600">밀리초 (확대)</text>
  <line x1="398" y1="360" x2="398" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="406.9" y1="360" x2="406.9" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="415.8" y1="360" x2="415.8" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="424.6" y1="360" x2="424.6" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="433.5" y1="360" x2="433.5" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="442.4" y1="360" x2="442.4" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="451.2" y1="360" x2="451.2" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="460.1" y1="360" x2="460.1" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="469" y1="360" x2="469" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="477.9" y1="360" x2="477.9" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="486.8" y1="360" x2="486.8" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="495.6" y1="360" x2="495.6" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="504.5" y1="360" x2="504.5" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="513.4" y1="360" x2="513.4" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="522.2" y1="360" x2="522.2" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="531.1" y1="360" x2="531.1" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <line x1="540" y1="360" x2="540" y2="376" stroke="currentColor" stroke-width="1.1"/>
  <text x="394" y="352" font-size="11" fill="currentColor" opacity="0.85">5 ms 제어 틱</text>
  <polyline points="398,392 398,398 522.2,398 522.2,392" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <text x="460.1" y="413" font-size="11" fill="currentColor" text-anchor="middle">70 ms 예산</text>
  <line x1="398" y1="424" x2="540" y2="424" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="398" y1="424" x2="398" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="398" y="440" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="433.5" y1="424" x2="433.5" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="433.5" y="440" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <line x1="469" y1="424" x2="469" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="469" y="440" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <line x1="504.5" y1="424" x2="504.5" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="504.5" y="440" font-size="11" fill="currentColor" text-anchor="middle">60</text>
  <line x1="540" y1="424" x2="540" y2="428" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="540" y="440" font-size="11" fill="currentColor" text-anchor="middle">80</text>
  <text x="550" y="480" font-size="11" fill="currentColor" text-anchor="end" opacity="0.8">두 축 사이는 아무것도 잇지 않는다</text>
</svg>

패널 A는 누가 무엇을 믿는가다 — 카메라는 패널 자세를 $50\,\mathrm{Hz}$로 내고, `move_group`의 planning scene은 그 자세를 한 번만 적용되고 다시는 갱신되지 않는 collision object로 쥐며, `move_group`은 `follow_joint_trajectory` 액션을 통해서만 P6의 $200\,\mathrm{Hz}$ 루프 위 궤적 제어기에 닿고, 카메라에서 `ros2_control`로 가는 화살표는 없다. 패널 B는 두 시계를 떼어 둔다 — 초 축에서 패널 자세의 나이는 씬 스냅샷의 $20\,\mathrm{ms}$에서 $0.80\,\mathrm{s}$ 계획 뒤 $0.82\,\mathrm{s}$, $1.50\,\mathrm{s}$ 실행 뒤 $2.32\,\mathrm{s}$로 자라고 그동안 카트는 $5.0$, $205$, $580\,\mathrm{mm}$를 움직이며, 밀리초 확대 축에는 $5\,\mathrm{ms}$ 제어 틱과 P6의 $70\,\mathrm{ms}$ 예산이 있고 두 축 사이는 아무것도 잇지 않는다.

### 1. MoveIt 2는 무엇이고, 아닌 것 세 가지

관절 궤적을 보내면 움직이는 팔은 이미 있다([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). 이제 기둥 반대편의 어떤 자세로, 기둥도 비계도 자기 몸도 치지 않고 가야 한다. 그 궤적을 손으로 쓰려면 역기구학(요청한 자세에 도구를 두는 관절각을 찾는 일. [[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]])을 풀고, 7차원 배치 공간(관절마다 축이 하나씩인, 가능한 모든 관절각 벡터의 공간. [[04-robotics/modern-robotics/ch02-configuration-space|MR Ch.02 — Configuration Space]] 참고)에서 충돌 없는 경로를 탐색하고, 어느 관절의 속도·가속도 한계도 어기지 않는 시간을 그 경로에 붙여야 한다. MoveIt 2는 정확히 그 문제에 대한 조립된 플러그인 기반 답이고, ROS 2의 표준이다.

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

이 런치는 `move_group`, MotionPlanning 디스플레이가 붙은 RViz, `robot_state_publisher`, 그리고 하드웨어가 `mock_components/GenericSystem`인 ros2_control 스택을 띄운다. 명령을 그대로 상태로 되돌려 주는 모의 하드웨어이고([[04-robotics/ros2/from-simulation-to-hardware|25.11]]), 로봇이 없는 머신에서도 계획이 실행되는 이유다. source된 다른 터미널에서:

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

URDF는 `panda_joint1`부터 `panda_joint7`까지의 관절과 손이 있다고 말한다. 그중 무엇이 "팔"인지, "home"이 무엇인지, 자세를 계획할 끝점 링크가 어느 것인지, 어떤 링크 쌍이 인접해 있어 절대 충돌하지 않는지는 말하지 않는다. 플래너는 이 넷 없이 시작할 수 없다. 그 의미론 계층이 **SRDF**(Semantic Robot Description Format, `robot_description_semantic`)이고, 중심 개념은 요청이 대상으로 삼을 수 있는 관절 집합에 이름을 붙인 **planning group**이다.

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

각 단계가 사 주는 것. 앞의 넷은 요청 쪽 점검으로, 플래너보다 먼저 돌며 플래너가 아예 돌지 못하게 막을 수 있다.

- `ResolveConstraintFrames` — 물체의 subframe으로 표현된 제약을 플래너가 아는 프레임으로 다시 쓴다.
- `ValidateWorkspaceBounds` — 요청에 작업 공간이 없으면 기본값을 넣는다. 샘플링 플래너가 샘플링할 유계 영역이 있어야 하기 때문이다. Jazzy에서 그 기본값은 `default_workspace_bounds` 파라미터이고 값이 `1000000000000.0`, 즉 한 변 1e12 m의 사실상 무한한 정육면체다. 소스에도 원래 무한대여야 한다는 TODO가 붙어 있다. 실제 경계가 필요하면 직접 설정하라. 예전 MoveIt이 박아 두었던 10 m 정육면체를 가정하지 마라.
- `CheckStartStateBounds` — 관절 한계를 벗어난 시작 상태를 **거부한다**. `START_STATE_INVALID`가 뜨고 플래너는 돌지 않는다. 회전 관절을 한계 안으로 밀어 넣어 주지 않는다. 이 어댑터가 고쳐 쓰는 것은 연속·평면·부유 관절의 *회전값*뿐이고, 그것도 `fix_start_state`가 참일 때만인데 기본값은 거짓이다. 실제 엔코더가 한계를 살짝 넘은 값을 보고하는 것은 맞지만, 이 어댑터는 그것을 흡수하는 장치가 아니라 실패로 바꾸는 장치다.
- `CheckStartStateCollision` — 시작 상태가 충돌이라고 보고하고 거기서 멈춘다. `START_STATE_IN_COLLISION`과 접촉 정보가 메시지에 담긴다. 근처의 자유 상태를 표본으로 찾아 주지 않는다. 플러그인 설명문은 아직 ROS 1 시절 동작을 광고하고 있지만 그 동작은 옮겨 오지 않았고, 소스는 오류 코드만 설정한다. 장면이나 시작 상태는 직접 고쳐야 한다.

나머지 단계는 응답 쪽 처리로, 플래너의 출력에 대해 돈다.

- `AddTimeOptimalParameterization` — 기하 경로를 관절 속도·가속도 한계를 지키는 궤적으로 바꾸는 단계다. **플래너는 시간을 만들지 않는다.** 경로와 궤적은 다른 물건이고, 그 차이가 여기서 생긴다.
- `ValidateSolution`은 완성된 궤적을 다시 검사하고, `DisplayMotionPath`는 RViz용으로 발행한다.

귀결 둘. 첫째, 어댑터 이름(`CheckStartStateBounds`)이 뜬 실패는 플래너 실패가 아니다. 플래너는 돌지도 않았다. 둘째, 그 목록의 순서가 곧 실행 순서라서, 어댑터를 어디에 넣느냐가 중요하다. 다만 올바른 목록에 넣어야 한다. `AddRuckigTrajectorySmoothing`은 `default_planning_response_adapters/AddRuckigTrajectorySmoothing`으로 등록된 **response** 어댑터이고, `response_adapters`의 `AddTimeOptimalParameterization` 뒤에 들어간다. `request_adapters`에 넣으면 `move_group` 시작 시점에 로드가 실패한다. 상류의 일부 설정 주석에는 아직 옛 request 어댑터 표기가 남아 있다.

### 5. 플래너 계열과 실제로 필요한 것

Jazzy는 넷을 제공하고, 전부 별도 패키지이며, 요청마다 `planning_pipeline`과 `planner_id`로 고른다.

| 계열 | 패키지 | 용도 |
|---|---|---|
| **OMPL**(샘플링) | `moveit_planners_ompl` | 기본값. RRTConnect 계열: 고차원·혼잡 씬에서 빠르고 확률적 완전성을 갖지만(경로가 있다면 오래 돌릴수록 찾을 확률이 1에 가까워지지만, 경로가 없음을 증명하지는 못한다) **결정적이지 않다** — 같은 요청이 실행마다 다른 경로를 준다 |
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

Python에서는 planning scene monitor를 통해 편집한다. 이 코드 조각들은 MoveIt 설정(URDF, SRDF, kinematics, 계획 파이프라인)을 파라미터로 받아야 하므로, `MoveItConfigsBuilder`로 만든 launch 파일에서 돌리거나 `MoveItPy(..., config_dict=...)`로 넘겨라. 맨 `python3`로 실행하면 로봇 모델이 없다.

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

`eef_step` 간격으로 말단 자세를 보간하고 각 지점에서 IK를 푼다. **반환값은 요청한 경로 중 달성한 비율로 0.0에서 1.0 사이이고, 오류일 때는 -1.0**이다. 반드시 검사해야 한다. 부분 결과는 정상적인 결과이고, 이유는 알고리즘이 아니라 전부 기하적이다: 직선이 도달 가능 작업 공간을 벗어난다, 특이점(팔이 끝점을 어떤 방향으로 움직일 능력을 잃는 자세라서, 그 근처의 자세는 매우 큰 관절 운동을 요구한다. [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR Ch.05 — Velocity Kinematics & Statics]] §4 참고)을 지나거나 근처를 스쳐 IK 해가 퇴화한다, 보간이 IK 해의 다른 분기를 넘어가 가장 가까운 해가 손목 뒤집기가 된다, 보간된 자세 하나가 충돌한다. (Jazzy에서 예전의 `jump_threshold` 인자는 deprecated이고 현재 오버로드에서 빠졌다.)

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

계획은 수백 밀리초가 걸리고 목표가 정지해 있다고 가정한다. 움직이는 대상에 대한 비주얼 서보잉이나 손으로 하는 원격 조작은 거기에 맞지 않는다. `moveit_servo`(`ros-jazzy-moveit-servo`)가 다른 모드다. 스트리밍 명령을 제어 주기로 관절 명령으로 바꾸며, 계획은 전혀 하지 않는다. joint jog(개별 관절 속도), twist(원하는 말단 속도), pose 명령을 받고, 관절 이름·위치·속도·가속도를 담은 `KinematicState`를 내거나 ROS 인터페이스로 궤적/실수 배열 토픽을 낸다. 특이점 근처와 충돌 근처에서 속도를 줄이며 둘 다 기본으로 켜져 있다. 충돌 검사는 `check_collisions`로 끌 수 있지만, 특이점 감속에는 스위치가 없고 문턱값으로 조정한다.

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

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. §11 뒤, 여기에 있는 까닭은 모든 단계가 앞 절에 기대기 때문이다. planning scene(§6), Cartesian path(§7), 실행 관문(§8), Servo(§9)다. 계산은 카탈로그에 페이지 국소 지속 시간 셋을 더한 것이고, 과제는 그중 하나를 바꾸며, 이어지는 실습은 Step 3과 4를 당신의 팔에서 돌린다.

**Step 1 — 씬은 사진이다.** 플래너는 요청이 시작될 때 planning scene을 한 번 읽는다. 그 안의 패널 자세는 비전에서 왔으므로 그 순간 이미 비전 한 주기만큼 낡아 있을 수 있다.

$$a_0 = T_v = \frac{1}{50} = 20\,\mathrm{ms}.$$

마지막 프레임보다 새로울 수 있는 것은 없기 때문이다. 그다음 계획이 $T_{\text{plan}}$, 실행이 $T_{\text{exec}}$ 동안 돌고, §6은 내 코드가 다시 발행하지 않는 한 collision object를 갱신하는 것은 없다고 못 박는다. 그래서 뒤의 두 경계에서 믿음의 나이는

$$a_1 = a_0 + T_{\text{plan}} = 0.020 + 0.80 = 0.82\,\mathrm{s},\qquad a_2 = a_1 + T_{\text{exec}} = 0.82 + 1.50 = 2.32\,\mathrm{s}$$

이다.

**Step 2 — 그 나이를 밀리미터와 카운트로.** 페이지 국소 $v$에서 씬이 가만있는 동안 팔을 실은 카트는 $d=v\,a$만큼 움직였다.

| 경계 | 나이 | $d=va$ | counts |
|---|---:|---:|---:|
| 씬을 읽음 | $20\,\mathrm{ms}$ | $5.0\,\mathrm{mm}$ | $10.2$ |
| 계획이 돌아옴 | $0.82\,\mathrm{s}$ | $205\,\mathrm{mm}$ | $420$ |
| 궤적이 끝남 | $2.32\,\mathrm{s}$ | $580\,\mathrm{mm}$ | $1188$ |

반 미터가 넘는다. 그런데 궤적의 모든 관절각은 첫 행을 보고 계산됐다. 이것은 MoveIt의 결함이 아니다. 플래너는 주어진 문제를 정확히 풀었고, 누군가 그 세계가 정적이라고 말해 주었다. 결함은 베이스를 움직이게 둔 호출자 쪽에 있다.

**Step 3 — MoveIt 자신의 관문을 P6 단위로 읽기.** §8의 `allowed_start_tolerance: 0.01`은 현재 상태가 궤적 첫 점에서 얼마나 떨어져 있어도 실행을 거부하지 않는지를 정한다. 직동 카트 관절에서는 $0.01\,\mathrm{m}$이고, 이는

$$0.01\times 2048 = 20.5\ \text{counts},\qquad \frac{0.01\,\mathrm{m}}{0.25\,\mathrm{m/s}} = 40\,\mathrm{ms}$$

이다. 허용 오차가 거리이고 카트가 페이지 국소 속도로 그것을 지나가기 때문이다. 40 밀리초다. 실행을 시작할지 말지를 정하는 관문이, P6가 카메라부터 힘까지의 사슬 전체에 주는 시간보다 짧게 넘어간다. $40 < 70$이다. 움직이는 베이스에서 계획하고 나중에 실행하는 설계는 느린 설계가 아니라 시작되지 않는 설계다. 계획 전에 베이스를 세우거나, 낡을 계획 자체가 없는 Servo(§9)를 쓴다.

**Step 4 — $200\,\mathrm{Hz}$ 루프가 궤적으로 하는 일.** 경로에 시간을 붙이는 것은 응답 어댑터 `AddTimeOptimalParameterization`이다(§4). 그것이 점을 $100\,\mathrm{ms}$ 간격으로 내놓는다고 하자. 그러면

$$\frac{100\,\mathrm{ms}}{T_c} = \frac{0.100}{0.005} = 20$$

이므로 이웃한 궤적 점 사이에 제어 주기 스무 번이 들어가고 제어기가 그 사이를 보간한다([[04-robotics/ros2/simulation-and-control|25.7 §11]]). 궤적은 성기고 루프는 촘촘하다. 그것이 의도된 분업이다. MoveIt은 어디로 언제를 말하고, `ros2_control`은 얼마나 자주를 말한다.

**Step 5 — `fraction`을 비율이 아니라 거리로.** $0.20\,\mathrm{m}$짜리 삽입 직선을 §7의 `eef_step` $0.01\,\mathrm{m}$로 잡자. 보간 자세 $0.20/0.01 = 20$개와 IK 해 20번이고, 한 스텝은 $0.01\times2048=20.5$ 엔코더 카운트의 베이스 이동에 해당한다. 시작 허용 오차 전체와 맞먹는 값이라 눈여겨볼 만하다. 여기서 $0.62$가 돌아왔다면 도구는 $0.20\times0.62=0.124\,\mathrm{m}$까지 가서 $0.076\,\mathrm{m}$을 남기고 멈춘다. $76\,\mathrm{mm}$, 즉 $156$ 카운트만큼 슬롯이 덜 들어갔고, 도구는 아무도 고르지 않은 자세로 허공에 서 있다. §7의 규칙이 여기서 곧바로 따라 나온다. 그 숫자는 *내가 그은* 직선의 분수이므로, 그 직선의 단위로 되읽어야 한다.

**Step 6 — 두 예산을 갈라 두기.** Step 1부터 5까지의 어느 것도 P6의 $70\,\mathrm{ms}$를 어기지 않는다. 그 예산은 카트 자신의 $200\,\mathrm{Hz}$ 루프 위에서 카메라 노출 중간부터 힘까지를 재고, 계획은 그 사슬 위에 있지 않기 때문이다. $0.80\,\mathrm{s}$짜리 계획은 예산 위반이 아니다. 패널 자세가 *씬*에 $200\,\mathrm{ms}$ 늦게 닿는 것도 MoveIt의 실패가 아니다. MoveIt은 불평 없이 그것으로 계획한다. 둘 다 각 숫자가 어느 시계에 속하는지 말하지 않은 호출자의 실패이고, 두 시계가 끝내 마주치면 무슨 일이 나는지가 Step 3이다.

### 12. 실습: 계획하고 실행한 뒤, 기둥을 가져다 놓아라

두 자리에 나눠서. 1–7번은 Panda 데모로, 8–10번은 당신의 팔로. 하드웨어는 필요 없다.

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
8. **당신의 팔을 MoveIt에.** 25.7의 기술을 어느 패키지의 `urdf/` 폴더(25.4)에 `two_link_arm_moveit.urdf.xacro`로 복사하고, 그 안의 `<ros2_control>`과 `<gazebo>` 블록을 지운다. Assistant는 찾아낸 `<ros2_control>` 블록을 그대로 두는데, Gazebo 하드웨어 플러그인은 Gazebo 밖에서 올라오지 못한다. 블록이 없으면 Assistant가 Panda 데모와 같은 되먹임 하드웨어인 `mock_components/GenericSystem` 블록을 직접 쓴다. `world` 링크는 남겨 두어 virtual joint가 필요 없게 한다. `ros2 run moveit_setup_assistant moveit_setup_assistant`를 띄우고 §3의 목록을 따라가라. 복사본을 불러오고, self-collision matrix를 만들고, `base_link`에서 `link2`까지의 kinematic chain으로 planning group `arm`을 더하고, robot pose 둘 — `home`(두 관절 모두 $0$)과 `raised`(`shoulder` $0.8$, `elbow` $-1.0$, 25.7의 6단계가 명령한 자세) — 을 더하고, ros2_control·ROS 2 controllers·MoveIt controllers는 기본값을 받아들이고, 워크스페이스에 `two_link_arm_moveit_config`를 생성한다. 그 `config/ros2_controllers.yaml`에서 `update_rate: 100`을 P6와 25.7의 $f_c$인 `200`으로 바꾼다. 빌드하고 source한 뒤 `ros2 launch two_link_arm_moveit_config demo.launch.py`.
9. **이름 붙은 자세 사이를 계획하고, 계획에서 Step 4를 읽는다.** **Planning** 탭에서 *Goal State*를 `raised`로 두고 **Plan**, **Execute**. 마커를 끄는 것은 대부분 실패하는데, 그게 맞다. 관절 둘은 x–z 평면의 2차원 끝점 집합에만 닿으므로, 끌어다 놓는 자세 거의 어디에도 IK 해가 없다. 이제 `ros2 topic echo /display_planned_path --once`로 연속한 점들의 `time_from_start`를 읽어라. $0.1\,\mathrm{s}$씩 나아가는데(마지막 간격은 더 짧을 수 있다), `AddTimeOptimalParameterization`의 기본 `resample_dt`다. 그러므로 `update_rate: 200`에서 점 사이에 제어 틱 스무 개가 들어간다. Worked case의 $0.100/0.005=20$을 당신의 팔에서 본 것이다.
10. **시작 관문이 거부하는 것을 본다.** *Goal State*를 `home`으로 두고 **Plan** 버튼을 누르되 실행하지는 않는다. 두 번째 터미널에서 MoveIt 모르게 팔을 제어기로 움직인다. Assistant는 `arm` 그룹의 제어기를 `arm_controller`로 이름 짓고, `ros2 control list_controllers`로 확인된다.

```bash
ros2 topic pub -1 /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.85, -1.0], time_from_start: {sec: 1}}]}"
```

이제 **Execute** 버튼을 누른다. `move_group`은 *Invalid Trajectory: start point deviates from current robot state more than 0.01 at joint 'shoulder'* 로 거부한다. 계획은 어깨가 $0.80\,\mathrm{rad}$일 때 계산되었는데 지금은 $0.85$, $0.01\,\mathrm{rad}$ 관문의 다섯 배다. 움직이는 카트 자리에 이 밀기를 넣은 Worked case의 Step 3을 당신의 팔에서 본 것이다. Step 3의 첫 번째 처방, 베이스를 멈추고 로봇이 지금 있는 곳에서 다시 계획하기를 적용하라. **Plan**, 그다음 **Execute**. 이번에는 돈다.

Panda의 마지막 두 계획 중 어느 쪽을 벽 옆에서 믿겠는지와 그 이유를 말할 수 있고, **Execute** 버튼을 누르기 전에 주어진 크기의 밀기가 거부될지 예측할 수 있으면 끝이다.

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

### 스스로 점검

1. RViz에서는 계획이 훌륭한데 팔이 움직이지 않는다. 첫 세 명령은?
2. MoveIt에 URDF만으로는 왜 부족한가, 한 문장으로.
3. `computeCartesianPath`가 0.62를 돌려줬다. 무엇을 하고, 원인은 무엇일 가능성이 큰가?
4. 블록을 쥐었더니 이후 모든 계획이 충돌로 실패한다. 왜인가?
5. 건설 현장 픽에서 MoveIt이 풀어 주지 않는 부분은?
6. P6에서 계산 절은 `allowed_start_tolerance: 0.01`이 카트 운동 $40\,\mathrm{ms}$에 해당함을 보인다. 동료가 실행이 거부되지 않게 그 값을 $0.10$으로 올리자고 한다. 그것이 사는 것과 치르는 값은 무엇이고, 그들이 피하고 있는 진짜 수정은 무엇인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. `ros2 control list_controllers`(활성 제어기가 있나), 그 이름을 `moveit_controllers.yaml`의 `controller_names`와 대조, `ros2 action list | grep follow_joint_trajectory`(액션 서버가 있나). 셋 다 배선 계층이고, 배선 실패는 즉시 조용히 난다. 허용 오차를 건드리기 전에 여기부터 본다.
> 2. URDF는 기하와 기구학을 기술하지만 의미론을 담지 않는다. planning group도, 이름 붙은 자세도, tip link도, 비활성 충돌 쌍도 없고, 이것들은 전부 SRDF에 있으며 플래너가 요청을 받기 전에 전부 필요하다.
> 3. 실행하지 마라. 이유가 있어 고른 직선의 62 % 지점에서 공구를 멈추는 일이 된다. 원인은 직선이 도달 가능 작업 공간을 벗어남, 특이점 근처 통과, 다른 IK 분기로 넘어감, 보간된 자세의 충돌 중 하나일 가능성이 크다. 구간을 줄이거나 방향을 바꾸거나, 부분이 아니라 깔끔하게 실패하는 Pilz `LIN`을 쓴다.
> 4. 블록이 여전히 세계의 collision object이고 그리퍼가 그 안에 들어가 있다. 그리퍼 링크들을 `touch_links`로 넘기며 그리퍼 링크에 attach해서 로봇 자신의 충돌 모형으로 옮겨야 한다.
> 5. 파지 자세가 어디인가 — 인식으로부터의 파지 합성 — 그리고 접촉 순간 이후의 전부. MoveIt의 세계 모형은 접촉을 실패로 취급하기 때문이다. MoveIt이 푸는 것은 그 둘 사이의 충돌 없는 이동뿐이다.
> 6. 창이 열 배로 넓어진다. $0.10\,\mathrm{m}$는 $205$ 카운트이고 카트 운동으로는 $0.10/0.25=0.40\,\mathrm{s}$이므로, 전에 거부되던 자리에서 실행이 시작된다. 대신 그 파라미터가 존재하는 이유인 보증을 잃는다. 이제 궤적의 첫 점이 로봇의 실제 위치에서 $0.10\,\mathrm{m}$ 떨어져 있어도 되고, 제어기는 그 사이에 무엇이 있든 팔을 거기까지 끌고 간다. 아무도 계획하지 않은 이동으로. 문제는 거부가 아니었다. 거부만이 문제를 보고하고 있었다. 피하고 있는 진짜 수정은 Step 1에 있다. 실행이 시작되기도 전에 씬은 이미 $0.82\,\mathrm{s}$ 낡아 있었으므로, 계획하고 실행하는 동안 베이스를 세우거나, 계획을 버리고 Servo(§9)로 가야 한다. Servo는 움직이는 목표를 추종하고 낡을 계획을 애초에 갖고 있지 않다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**를 플래너가 순간 이동으로 취급하면 안 되는 모바일 베이스로. 비전 $50\,\mathrm{Hz}$가 패널 자세를 주고, 카트 제어기는 $200\,\mathrm{Hz}$, 예산 $70\,\mathrm{ms}$. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** P6 카트, 패널, MoveIt planning scene. 비전의 `/goal`, `follow_joint_trajectory` 액션, 그 아래 $200\,\mathrm{Hz}$ 제어기. 다섯 줄 타임라인: $2\,\mathrm{s}$ 계획, 그다음 $5\,\mathrm{ms}$ 실행 틱. $70\,\mathrm{ms}$ 센싱 예산은 계획과 *다른* 시계.
2. **유도.** (a) $2\,\mathrm{s}$ 계획이 $70\,\mathrm{ms}$ 예산을 어기지 않는 이유 — 어느 루프가 어느 숫자를 소유하는가. (b) 엔코더 한 카운트의 $\Delta p$, 씬이 *받지 않는* 베이스 자세 해상도. (c) `computeCartesianPath`가 $0.62$를 반환. 실행하는가?
3. **해석.** RViz 계획은 훌륭한 데 카트가 안 움직인다. 첫 세 명령. 별도로: 씬 안의 $200\,\mathrm{ms}$ 늦은 패널 자세 — MoveIt 버그인가 P6 예산 버그인가?

> [!note]- 그리는 법 · How to draw it
> - 영역 셋을 나란히 두고 그 사이에 이름 붙은 경계 둘을 긋는다. `지각`($50\,\mathrm{Hz}$로 패널 자세를 내는 카메라), `move_group`(planning scene, SRDF 그룹, 파이프라인), `ros2_control`(P6의 $200\,\mathrm{Hz}$ 루프 위의 궤적 제어기).
> - 패널은 두 번 그린다. 왼쪽에는 실제 물체로, planning scene 안에는 collision object로. 둘을 점선 화살표로 잇고 `한 번만 적용`이라고 적는다.
> - 그 점선 화살표는 되먹임 루프가 아니다. 내 코드가 다시 발행하지 않는 한 씬을 갱신하는 것은 없다.
> - `move_group`과 `ros2_control` 사이의 경계에는 토픽이 아니라 액션 `follow_joint_trajectory`가 놓인다. MoveIt은 액션 클라이언트이고 결과를 알아야 하기 때문이다.
> - 카메라에서 `ros2_control`로 가는 화살표는 하나도 없다. P6의 $70\,\mathrm{ms}$ 예산은 MoveIt이 끼어 있지 않은 사슬 위에 있다.
> - 축은 둘이다. `씬 스냅샷`, `계획`, `실행`을 이어 붙이는 초 축, 그리고 $5\,\mathrm{ms}$ 제어 틱과 $70\,\mathrm{ms}$ 괄호 하나를 담은 밀리초 확대 축. 둘 사이는 아무것도 잇지 않는다. 그 빈틈이 이 그림의 논증이다.
> - 초 축 위에는 왼쪽에서 오른쪽으로 길어지는 `패널 자세의 나이` 막대를 그리고 경계 셋에서의 값을 적는다(계산 절, $0.80\,\mathrm{s}$ 계획: $20\,\mathrm{ms}$, $0.82\,\mathrm{s}$, $2.32\,\mathrm{s}$).

> [!tip]- 정답 · Solutions
> 1. 씬이 패널을 쥐고, MoveIt은 카메라가 아니라 궤적 제어기와 말한다. 계획은 초, 제어는 밀리초; $70\,\mathrm{ms}$는 카메라–힘이지 플래너–씬이 아니다.
> 2. (a) $70\,\mathrm{ms}$는 센싱/제어 사슬이고, 실행이 여전히 $200\,\mathrm{Hz}$로 샘플하면 계획은 느려도 된다. (b) $0.488\,\mathrm{mm}$, 한 번 그린 씬에는 안 보인다. (c) 아니오 — 고른 직선의 62 %에서 멈춘다.
> 3. `list_controllers`, `controller_names` 대조, `ros2 action list | grep follow_joint_trajectory`. 늦은 자세는 P6 예산 버그: MoveIt은 낡은 씬에 대해 기꺼이 계획한다.
