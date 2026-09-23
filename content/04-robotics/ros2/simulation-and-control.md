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
> A sourced **ROS 2 Jazzy Jalisco on Ubuntu 24.04** installation, a workspace you can build in ([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), and the two-link arm you wrote in [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]. Simulated versus wall time matters here and is covered in [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]].
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**, 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), 그리고 [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]에서 작성한 2링크 팔. 시뮬레이션 시간과 벽시계 시간의 구분이 여기서 중요해진다([[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]).

> [!note] First pass · 처음이라면
> Read the Running object and the picture, then the Worked case; its three one-line glosses point to §7 (the loop rate) and §10 (why the loop runs on simulated time, and the real-time factor). Then §5–§7 (the seam, the interfaces, the controller manager) and do §11, whose Step 7 makes the Worked case's Step 5 happen in your own terminal. §1–§4 are the Gazebo background (what simulation settles, which Gazebo, the bridge, spawning); §8–§10 are reference; §12 is the chain of checks for when an active controller moves nothing.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the 1-D cart and its clock — drawn in Gazebo Harmonic and driven through `ros2_control`. Every number below is the catalog's.

*Two objects, stated once.* The cart is what you compute with; nothing on this page builds it. The exercise (§11) builds the two-link arm from 25.6 instead, because that is the description you already have. What carries over to the arm unchanged is the loop: the exercise sets the same `update_rate: 200`, so Step 1's $T_c=5\,\mathrm{ms}$ and Step 5's real-time-factor arithmetic are what you measure in §11, Steps 5 and 7. What does not carry over: the arm has no encoder, since Gazebo reports each joint angle as a floating-point number, so Step 2's $0.488\,\mathrm{mm}$ quantum has no counterpart; and it has no camera, so there is no $T_v$ term and the arm's rate ledger is the hold term $T_c$ alone.

| Symbol | Value | What it is here |
|---|---:|---|
| $N$ | $2048$ counts/m | cart encoder, the only position sensor |
| $f_v$ | $50\,\mathrm{Hz}$ | vision node publishing a goal, bridged out of Gazebo |
| $f_c$ | $200\,\mathrm{Hz}$ | controller manager `update_rate`, the `read`–`update`–`write` loop of §7 |
| $B$ | $70\,\mathrm{ms}$ | end-to-end budget, camera mid-exposure to applied force |
| $v$ | $0.25\,\mathrm{m/s}$ | commanded cart speed — **page-local**: P6 freezes no speed, and this one is used only to turn times into millimetres |

*Scope: this page teaches the plumbing between a description and a moving robot — the bridge, the interface seam, the controller manager and its clock — and computes what those rates cost in latency and resolution. It does not teach whether the contact physics transfers, which is [[05-construction-robotics/sim-to-real|Sim-to-Real]]; nor how to write the hardware component behind the same seam, which is [[04-robotics/ros2/from-simulation-to-hardware|25.11]]; nor how to plan the trajectory you hand the controller, which is [[04-robotics/ros2/manipulation-moveit2|25.8]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 574" style="max-width:100%;height:auto" role="img" aria-label="Panel A: Gazebo Harmonic holds the gz_ros2_control plugin and the controller manager at update_rate 200; state interfaces cart/position and cart/velocity cross the seam to the controllers, the command interface cart/velocity comes back marked available and claimed, and the camera and /clock leave Gazebo through ros_gz_bridge. Panel B: five lanes on simulated time from 0 to 80 ms, camera every 20 ms, controller every 5 ms, one frame's command on the cart for L plus 25 ms, under a 70 ms budget that is wall time.">
  <text x="8" y="20" font-size="12" fill="currentColor" font-weight="600">A · who provides what</text>
  <rect x="8" y="24" width="226" height="172" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <text x="16" y="40" font-size="12" fill="currentColor">Gazebo Harmonic</text>
  <text x="16" y="54" font-size="11" fill="currentColor" opacity="0.75">physics and the model: the P6 cart</text>
  <rect x="16" y="62" width="210" height="102" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="22" y="76" font-size="11" fill="currentColor">gz_ros2_control system plugin</text>
  <rect x="24" y="84" width="194" height="74" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="32" y="101" font-size="11" fill="currentColor">controller manager</text>
  <text x="32" y="117" font-size="11" fill="currentColor">update_rate: 200</text>
  <text x="32" y="132" font-size="11" fill="currentColor" opacity="0.7">(per simulated second)</text>
  <rect x="16" y="170" width="96" height="20" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="64" y="184" font-size="11" fill="currentColor" text-anchor="middle">camera sensor</text>
  <rect x="124" y="170" width="102" height="20" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="175" y="184" font-size="11" fill="currentColor" text-anchor="middle">sim clock</text>
  <line x1="388" y1="70" x2="388" y2="190" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6" stroke-dasharray="5 4"/>
  <text x="388" y="64" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">seam</text>
  <text x="311" y="80" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.7">state interfaces</text>
  <line x1="218" y1="96" x2="393.5" y2="96" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="400,96 393,99.4 393,92.6" fill="currentColor"/>
  <text x="311" y="92" font-size="11" fill="currentColor" text-anchor="middle">cart/position</text>
  <line x1="218" y1="114" x2="393.5" y2="114" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="400,114 393,117.4 393,110.6" fill="currentColor"/>
  <text x="311" y="110" font-size="11" fill="currentColor" text-anchor="middle">cart/velocity</text>
  <text x="311" y="131" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.7">command interface</text>
  <line x1="400" y1="148" x2="224.5" y2="148" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="218,148 225,144.6 225,151.4" fill="currentColor"/>
  <text x="311" y="144" font-size="11" fill="currentColor" text-anchor="middle">cart/velocity</text>
  <text x="311" y="163" font-size="11" fill="currentColor" text-anchor="middle" font-weight="600">[available] [claimed]</text>
  <rect x="400" y="84" width="152" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="406" y="100" font-size="11" fill="currentColor">joint_state_broadcaster</text>
  <text x="406" y="116" font-size="11" fill="currentColor" opacity="0.7">publishes /joint_states</text>
  <rect x="400" y="134" width="152" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="406" y="150" font-size="11" fill="currentColor">velocity controller</text>
  <text x="406" y="166" font-size="11" fill="currentColor" opacity="0.7">the one claimant</text>
  <rect x="8" y="212" width="226" height="34" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="121" y="226" font-size="11" fill="currentColor" text-anchor="middle">ros_gz_bridge</text>
  <text x="121" y="241" font-size="11" fill="currentColor" text-anchor="middle">token [ : GZ → ROS only</text>
  <line x1="36" y1="190" x2="36" y2="253.5" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="36,260 32.6,253 39.4,253" fill="currentColor"/>
  <text x="42" y="207" font-size="11" fill="currentColor">/camera</text>
  <line x1="206" y1="190" x2="206" y2="259.5" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="206,266 202.6,259 209.4,259" fill="currentColor"/>
  <text x="212" y="207" font-size="11" fill="currentColor">/clock</text>
  <rect x="8" y="260" width="132" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="74" y="276" font-size="11" fill="currentColor" text-anchor="middle">vision node · 50 Hz</text>
  <text x="156" y="280" font-size="11" fill="currentColor" opacity="0.85">ROS nodes on use_sim_time</text>
  <polyline points="74,284 74,296 476,296" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="476" y1="296" x2="476" y2="180.5" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="476,174 479.4,181 472.6,181" fill="currentColor"/>
  <text x="468" y="292" font-size="11" fill="currentColor" text-anchor="end">/goal · 50 Hz</text>
  <line x1="8" y1="306" x2="552" y2="306" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="8" y="324" font-size="12" fill="currentColor" font-weight="600">B · the timeline, on sim time</text>
  <circle cx="222.8" cy="320.5" r="3.4" fill="currentColor"/>
  <text x="231.8" y="324" font-size="11" fill="currentColor" opacity="0.85">new goal</text>
  <circle cx="301.8" cy="320.5" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <text x="310.8" y="324" font-size="11" fill="currentColor" opacity="0.85">same goal: 3 of every 4</text>
  <rect x="462.2" y="316.5" width="8" height="8" fill="currentColor" fill-opacity="0.75"/>
  <text x="475.2" y="324" font-size="11" fill="currentColor" opacity="0.85">from frame k</text>
  <rect x="170" y="360" width="115" height="120" fill="currentColor" fill-opacity="0.1"/>
  <line x1="170" y1="360" x2="170" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="193" y1="360" x2="193" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="216" y1="360" x2="216" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="239" y1="360" x2="239" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="262" y1="360" x2="262" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="285" y1="360" x2="285" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="308" y1="360" x2="308" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="331" y1="360" x2="331" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="354" y1="360" x2="354" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="377" y1="360" x2="377" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="400" y1="360" x2="400" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="423" y1="360" x2="423" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="446" y1="360" x2="446" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="469" y1="360" x2="469" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="492" y1="360" x2="492" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="515" y1="360" x2="515" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="538" y1="360" x2="538" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <text x="8" y="376" font-size="11" fill="currentColor">camera exposure</text>
  <line x1="170" y1="384" x2="538" y2="384" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="400" font-size="11" fill="currentColor">bridge</text>
  <line x1="170" y1="408" x2="538" y2="408" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="424" font-size="11" fill="currentColor">controller read</text>
  <line x1="170" y1="432" x2="538" y2="432" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="448" font-size="11" fill="currentColor">controller update/write</text>
  <line x1="170" y1="456" x2="538" y2="456" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="472" font-size="11" fill="currentColor">force at the cart</text>
  <line x1="170" y1="480" x2="538" y2="480" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <circle cx="170" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="262" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="354" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="446" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="538" cy="372" r="3.6" fill="currentColor"/>
  <text x="176" y="367" font-size="11" fill="currentColor" opacity="0.9">frame k</text>
  <text x="268" y="367" font-size="11" fill="currentColor" opacity="0.9">k+1</text>
  <line x1="172.5" y1="377" x2="172.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="172.5,401 169.9,396 175.1,396" fill="currentColor"/>
  <line x1="264.5" y1="377" x2="264.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="264.5,401 261.9,396 267.1,396" fill="currentColor"/>
  <line x1="356.5" y1="377" x2="356.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="356.5,401 353.9,396 359.1,396" fill="currentColor"/>
  <line x1="448.5" y1="377" x2="448.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="448.5,401 445.9,396 451.1,396" fill="currentColor"/>
  <circle cx="170" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="193" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="216" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="239" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="262" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="285" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="308" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="331" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="354" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="377" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="400" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="423" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="446" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="469" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="492" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="515" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="538" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <rect x="167" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="190" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="213" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="236" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="259" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="282" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="305" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="328" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="351" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="374" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="397" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="420" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="466" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="489" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="512" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="535" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="170.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="193.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="216.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="239.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="262.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="285.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="308.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="331.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="354.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="377.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="400.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="423.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="446.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="469.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="492.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="515.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <polyline points="171,356 171,352 261,352 261,356" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>
  <polyline points="263,356 263,352 284,352 284,356" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>
  <text x="216" y="347" font-size="11" fill="currentColor" text-anchor="middle">T<tspan font-size="8.5" dy="2.5">v</tspan><tspan dy="-2.5" dx="4">= 20 ms</tspan></text>
  <text x="264" y="347" font-size="11" fill="currentColor">T<tspan font-size="8.5" dy="2.5">c</tspan><tspan dy="-2.5" dx="4">= 5 ms</tspan></text>
  <text x="329" y="347" font-size="11" fill="currentColor" font-weight="600">L + 20 + 5 = L + 25 ms</text>
  <line x1="170" y1="484" x2="538" y2="484" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="170" y1="484" x2="170" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="170" y="500" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="216" y1="484" x2="216" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="216" y="500" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <line x1="262" y1="484" x2="262" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="262" y="500" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <line x1="308" y1="484" x2="308" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="308" y="500" font-size="11" fill="currentColor" text-anchor="middle">30</text>
  <line x1="354" y1="484" x2="354" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="354" y="500" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <line x1="400" y1="484" x2="400" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="400" y="500" font-size="11" fill="currentColor" text-anchor="middle">50</text>
  <line x1="446" y1="484" x2="446" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="446" y="500" font-size="11" fill="currentColor" text-anchor="middle">60</text>
  <line x1="492" y1="484" x2="492" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="492" y="500" font-size="11" fill="currentColor" text-anchor="middle">70</text>
  <line x1="538" y1="484" x2="538" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="538" y="500" font-size="11" fill="currentColor" text-anchor="middle">80</text>
  <text x="8" y="500" font-size="11" fill="currentColor" opacity="0.8">simulated time (ms)</text>
  <polyline points="170,507 170,512 492,512 492,507" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="285" y1="507" x2="285" y2="515" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="8" y="516" font-size="11" fill="currentColor">budget B = 70 ms</text>
  <text x="227.5" y="527" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">25: the rates</text>
  <text x="388.5" y="527" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">45 left: L, driver, actuator</text>
  <text x="170" y="546" font-size="12" fill="currentColor" font-weight="600">This axis is sim time, and the budget is wall time.</text>
  <text x="8" y="564" font-size="11" fill="currentColor" opacity="0.75">Worst case: each goal lands just after a tick. L (mid-exposure to landing) is drawn as zero.</text>
</svg>

Panel A is P6's cart in Gazebo Harmonic, whose `gz_ros2_control` plugin hosts the controller manager at `update_rate: 200`: the state interfaces `cart/position` and `cart/velocity` cross the seam to the controllers, the command interface `cart/velocity` comes back from the velocity controller, its one claimant, marked `[available] [claimed]`, and the camera and `/clock` reach ROS only through `ros_gz_bridge`. Panel B puts the loop on simulated time — a camera frame every $T_v=20\,\mathrm{ms}$ and a control tick every $T_c=5\,\mathrm{ms}$, so three ticks in four reuse the last goal — and in the worst case a frame's command is still on the cart $L+25\,\mathrm{ms}$ after mid-exposure (the Worked case's Step 3 derives it), leaving $45$ of the $70\,\mathrm{ms}$ budget for $L$, the driver and the actuator. The axis is sim time, and the budget is wall time.

### Worked case · 대상으로 한 번 끝까지

This is the homework object. Do the arithmetic here on the catalog numbers so the problem set is a change of rate, not a first derivation.

**Step 1 — two periods and their ratio.** The controller manager's `update_rate` is a frequency in Hz (§7), so

$$T_c=\frac{1}{f_c}=\frac{1}{200}=5\,\mathrm{ms},\qquad T_v=\frac{1}{f_v}=\frac{1}{50}=20\,\mathrm{ms},\qquad \frac{f_c}{f_v}=\frac{200}{50}=4,$$

so the loop performs four complete `read`–`update`–`write` cycles per camera frame and three of those four see a goal they have already seen. That ratio, not either rate alone, is what the timeline has to show.

**Step 2 — what one encoder count is worth.** The cart encoder is a count per unit length, so its quantum is the reciprocal:

$$\Delta p=\frac{1}{N}=\frac{1}{2048}=4.883\times10^{-4}\,\mathrm{m}=0.488\,\mathrm{mm}.$$

Difference two successive position reads one control period apart and the smallest non-zero velocity you can report is one count per period, $\Delta p/T_c=0.0977\,\mathrm{m/s}=97.7\,\mathrm{mm/s}$, because a single count is the smallest change the numerator can take. Do the same differencing across a whole vision interval instead and the quantum falls to $\Delta p/T_v=24.4\,\mathrm{mm/s}$, at the cost of $10\,\mathrm{ms}$ of lag, half the $20\,\mathrm{ms}$ window — the same noise-versus-delay trade the velocity estimator makes in [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]].

**Step 3 — the staleness the rates alone impose.** Let a measurement be taken at mid-exposure $t_0$ and let $L$ be everything between that instant and the goal message arriving at the controller: exposure half-window, readout, bridge, DDS. The rates add two more terms after $L$. The controller keeps using this goal until the next frame replaces it, which is at most $T_v$ later; and the command computed at that last tick is written and then *held* until the following tick, one more $T_c$. So the worst-case age of the vision measurement while the force it caused is still on the cart is

$$A_{\max}=L+T_v+T_c=L+20+5=L+25\,\mathrm{ms},$$

since the vision period bounds how long a stale goal survives and the control period bounds how long a stale command is held. Against P6's budget that leaves $70-25=45\,\mathrm{ms}$ for the whole of $L$ plus the driver and the actuator. The rates have already spent $36\%$ of the budget before a single line of your code runs.

**Step 4 — the same ledger in millimetres.** At the page-local $v=0.25\,\mathrm{m/s}$ the cart covers $0.25\times0.025=6.25\,\mathrm{mm}$ during those $25\,\mathrm{ms}$, which is $6.25\times2.048=12.8$ encoder counts: the goal the controller is chasing is nearly thirteen counts behind the cart even when nothing is late. Per control period the cart moves $0.25\times0.005=1.25\,\mathrm{mm}=2.56$ counts, comfortably above the quantum. Slow it to $0.05\,\mathrm{m/s}$ and one period covers $0.25\,\mathrm{mm}=0.512$ counts, so nearly half the ticks see *no* count change at all and the differenced velocity reads exactly $0$ or exactly $97.7\,\mathrm{mm/s}$ — a velocity signal that is pure quantization noise, at the speed where you most wanted it to be smooth.

**Step 5 — and why Gazebo cannot certify any of it.** The controller manager runs inside the simulator, so `update_rate: 200` is 200 ticks per simulated second (§10). The real-time factor is simulated time elapsed per wall-clock second, $\mathrm{RTF}=\Delta t_{\text{sim}}/\Delta t_{\text{wall}}$ (defined in §10). Let it be $0.5$, a simulation running at half speed. The loop then executes $200\times0.5=100$ times per *wall* second, and the $25\,\mathrm{ms}$ sim-time ledger of Step 3 occupies $25/0.5=50\,\mathrm{ms}$ of wall time, leaving $70-50=20\,\mathrm{ms}$ instead of $45$.

Nothing in the simulation misbehaves: sim time is internally consistent, the trajectory tracks, and `ros2 topic hz --use-sim-time /joint_states` reports 200, per simulated second. Drop the flag and the same command reports about 100, because Jazzy's `ros2 topic hz` timestamps each arrival on its own node's clock, and that node follows `/clock` only when `-s`/`--use-sim-time` is given; otherwise it reads the wall clock (`ros2topic/verb/hz.py` and `ros2cli/node/direct.py`, jazzy branch; `--wall-time` forces the wall clock even with the flag).

P6's $70\,\mathrm{ms}$ is a wall-clock budget about a real camera and a real motor, and a run that does not report its real-time factor has not measured it. That is the precise version of §1's warning, and it is the thing the problem set's third item asks you to say out loud. §11's Step 7 makes it happen on your own arm.

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

The consequence for you: **do not start new work on Gazebo Classic.** It is out of support, and every tutorial that tells you to write `<gazebo><plugin filename="libgazebo_ros_control.so">` is describing a dead system. The current LTS releases are **Harmonic** (Sep 2023 – May 2029) and **Jetty** (Sep 2025 – May 2031); Fortress (LTS, to May 2027) and Ionic (to Dec 2026) are still supported but not for new work.

This page uses **Gazebo Harmonic**, because that is the pairing with ROS 2 Jazzy that has binary packages — `ros-jazzy-ros-gz` and `ros-jazzy-gz-ros2-control`. Lyrical Luth pairs with Jetty in the same way; the structure of everything below is unchanged, only the package names shift.

### 3. Two message systems, and why a bridge exists

Gazebo is not a ROS program. It has its own transport layer (Gazebo Transport) and its own message definitions (`gz.msgs.*`, Protobuf), and it runs perfectly well with no ROS installed. ROS 2 has DDS (its transport standard, see [[04-robotics/ros2/what-ros2-is#5. DDS underneath: what it buys and what it costs|25.1 §5]]) and `sensor_msgs/msg/*`. Neither speaks the other's wire format or type system.

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

Gazebo parses URDF by converting it to SDF (Simulation Description Format, Gazebo's native format for robots and worlds) internally. Most of what you wrote survives; the parts that beginners lose are the ones URDF has no concept of, which is why extra information goes in `<gazebo>` tags that the URDF parser ignores and the SDF converter reads.

### 5. ros2_control: the seam

You could write a Gazebo plugin that reads a topic and sets joint forces. People do, and then the code is worthless the day the robot is real.

`ros2_control` exists to put a defined seam in the middle of that path, with a stable interface on both sides:

- On one side, **controllers** — a joint trajectory follower, a differential drive kinematic layer, a PID (proportional–integral–derivative feedback on the error, derived in [[04-robotics/control-theory-ce397#7. Designing the feedback: pole placement and PID|5. Control Theory §7]]). A controller is an object derived from `ControllerInterface` whose `update()` reads state and writes commands. It never knows what the hardware is.
- On the other, **hardware components** — the thing that actually talks to a motor driver, a CAN bus (a two-wire serial bus common on motor drives), an EtherCAT slave (one device on EtherCAT, an Ethernet-based real-time fieldbus), or a simulator. Three kinds exist: `System` (multi-DOF with coupling), `Actuator` (single-DOF, read and write), `Sensor` (read only).

> **Hardware component, defined.** A **hardware component** is a *plugin class that stands for one piece of hardware below the seam* — a drive, a sensor board, or a simulated model. Three defining conditions. It **exports named interfaces**: state interfaces it can be read for and command interfaces it can be told (§6). Its **type fixes what it may export**: a `Sensor` only reads, an `Actuator` reads and writes one joint, and a `System` reads and writes any number of joints over one channel. And it is **declared, not built into a controller**: the `<ros2_control>` block's `type` and `<hardware><plugin>` line name it, and the controller manager loads it by that name and calls its `read()` and `write()` from the loop of §7.
>
> $$\mathcal{C}_{\texttt{Sensor}}=\varnothing,\qquad \mathcal{C}_{\texttt{Actuator}}\subseteq\{j\}\times\mathcal{N},\qquad \mathcal{C}_{\texttt{System}}\subseteq J\times\mathcal{N}$$
>
> where $\mathcal{C}$ is the set of command interfaces a component exports, each a pair `joint/name`, $j$ one joint, $J$ a set of joints and $\mathcal{N}$ the interface names (`position`, `velocity`, `effort`, …).
>
> - **Example**: P6's cart in Gazebo is one `System`, `gz_ros2_control/GazeboSimSystem`, exporting state $\{\texttt{cart/position},\ \texttt{cart/velocity}\}$ and command $\{\texttt{cart/velocity}\}$, read and written $200$ times per simulated second.
> - **Non-example**: P6's camera. It senses, but it is not a `Sensor` component: its frames reach ROS as a $50\,\mathrm{Hz}$ topic through `ros_gz_bridge`, outside `read()`. That is why $T_v=20\,\mathrm{ms}$ enters the Worked case's ledger apart from $T_c$, and why no `update_rate` can shorten it.

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

> **Command and state interfaces, defined.** An **interface** is a *named number that a hardware component exports*, written `joint/name` — `cart/velocity` is one. Three defining conditions. A **state interface** is read above the seam, and **any number of controllers may read it** at once. A **command interface** is written, and **at most one active controller holds it**: activating a controller *claims* every command interface it lists until it is deactivated. And a controller **activates only if** every interface it lists is exported and none of its command interfaces is held already, so a name that matches nothing fails at activation, not at load.
>
> $$\mathrm{activate}(k)\iff R_{\text{cmd}}(k)\subseteq\mathcal{C}\setminus H\ \ \wedge\ \ R_{\text{state}}(k)\subseteq\mathcal{S}$$
>
> where $R_{\text{cmd}}(k)$ and $R_{\text{state}}(k)$ are the command and state interfaces controller $k$ lists, $\mathcal{C}$ and $\mathcal{S}$ those the hardware exports, and $H$ those held by the other active controllers.
>
> - **Example**: P6's velocity controller lists $R_{\text{cmd}}=\{\texttt{cart/velocity}\}$, which is exported and not in $H=\varnothing$, so it activates and the interface reads `[available] [claimed]`; `joint_state_broadcaster` reads `cart/position` and `cart/velocity` alongside it.
> - **Non-example**: a second velocity controller on the same cart. Now $\texttt{cart/velocity}\in H$, so its activation is refused as "currently claimed by another controller". Two writers on one actuator is a failed activation, not a tug of war — the safety property the seam exists to give.

The `<hardware><plugin>` line is the only part of this block that differs between simulation and a real robot.

### 7. The controller manager

The **controller manager** is the process that holds both halves together. It loads hardware components through `pluginlib` (the ROS library that loads a C++ class from a shared library at runtime by its registered name), loads controllers through `pluginlib`, matches required interfaces against provided ones, and runs the loop: `read()` from hardware, `update()` every active controller, `write()` to hardware. Its `update_rate` parameter is that loop's frequency in Hz, default 100. It gets the robot description by subscribing to the `robot_description` topic.

> **Controller manager, defined.** The **controller manager** is the *node that owns the control loop*, and not itself a controller. Three defining conditions. It **loads both sides by name**: hardware components through its resource manager, controllers through `pluginlib`. It **matches** what each controller lists against what the hardware exports, and grants or refuses activation by §6's rule. And it **runs one loop at `update_rate`**: every period it calls `read()` on the hardware, `update()` on each *active* controller and `write()` on the hardware, in that order, skipping controllers that are loaded but inactive.
>
> $$T_c=\frac{1}{f_c},\qquad u(t)=u_k\quad \forall\,t\in[\,kT_c,\ (k+1)T_c)$$
>
> where $f_c$ is `update_rate` in Hz, $100$ unless set, and $u_k$ the command written at tick $k$; it stays on the hardware until the next write, which is why $T_c$ appears in the Worked case's rate ledger.
>
> - **Example**: P6's `update_rate: 200` gives $T_c=5\,\mathrm{ms}$: four read–update–write cycles per $20\,\mathrm{ms}$ camera frame, each written velocity held for $5\,\mathrm{ms}$.
> - **Non-example**: `update_rate` as the rate of the whole chain from camera to force. Raising it to $500$ shortens only the hold, from $5$ to $2\,\mathrm{ms}$, so the rate ledger falls from $20+5=25$ to $20+2=22\,\mathrm{ms}$. The manager cannot make a goal newer than the last camera frame, so the faster loop buys $3\,\mathrm{ms}$ of a $70\,\mathrm{ms}$ budget.

A controller is a lifecycle object (the managed-node state machine of [[04-robotics/ros2/services-actions-parameters#8. Managed (lifecycle) nodes|25.3 §8]]) with three states that matter:

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

Two of these verbs repay a closer look. `list_hardware_interfaces` is §6's claim rule made visible: every command interface is printed `[available]` or `[unavailable]` and `[claimed]` or `[unclaimed]`, so a controller that loads and configures but will not activate is explained in one line — its interface is already claimed or is not there, as §6's box reads it for P6's `cart/velocity`.

`switch_controllers` has a default worth knowing. Given neither `--strict` nor `--best-effort`, the manager applies its `defaults.switch_controller.strictness` parameter, which is `best_effort`: a controller that cannot activate is dropped from the request while the deactivations still run, so `--deactivate a --activate b` can leave P6's cart with no active controller at all, the very window §7's atomic switch exists to close. `--strict` makes the request all or nothing, and a hand-over on a moving cart should use it. The switch is also timed against the loop rather than dropped into the middle of it: the manager waits until an `update()` has finished, within about one period, $5\,\mathrm{ms}$ at P6's `update_rate: 200`, and the controllers named in the request skip their updates until the switch is done. The CLI waits up to `--switch-timeout`, $5.0\,\mathrm{s}$ by default, $5.0/0.005=1000$ of P6's cycles, before it reports the switch as failed.

### 9. The controllers you will actually use

`ros2_controllers` ships a set; four cover most work.

| Controller | What it is for | Interface it wants |
|---|---|---|
| `joint_state_broadcaster/JointStateBroadcaster` | reads state interfaces and publishes `/joint_states`; not a controller in the commanding sense, but nothing sees your robot without it | state only |
| `joint_trajectory_controller/JointTrajectoryController` | follows a timed multi-joint trajectory; what MoveIt 2 executes through | `position`, or `velocity`/`effort` with PID gains |
| `forward_command_controller` variants (`position_controllers/JointGroupPositionController`, and the velocity and effort versions) | pass a raw command array straight to the hardware, no trajectory, no interpolation — the right tool for a learned policy or a hand-written loop | whichever it names |
| `diff_drive_controller/DiffDriveController` | converts a body velocity into left and right wheel commands and publishes odometry | `velocity` on the wheel joints |

Their surfaces, which are what you actually type against:

- **Joint trajectory controller** — topic `<name>/joint_trajectory` (`trajectory_msgs/msg/JointTrajectory`) and action `<name>/follow_joint_trajectory` (`control_msgs/action/FollowJointTrajectory`). Use the action when you need to know whether the motion finished; the topic is fire-and-forget. Parameters: `joints`, `command_interfaces`, `state_interfaces`. `state_interfaces` must include `position`, and must include `velocity` when the command interface is `velocity` or `effort` alone, because in that case the controller closes a PID loop on the tracking error and that loop needs the measured joint velocity as well as the position.
- **Forward command controllers** — topic `<name>/commands` (`std_msgs/msg/Float64MultiArray`), parameter `joints` (plus `interface_name` for the generic `forward_command_controller/ForwardCommandController`; the position/velocity/effort variants fix the interface). The array is positional: element *i* goes to joint *i* of the `joints` list. Nothing validates that you meant that ordering.
- **Differential drive controller** — subscribes `<name>/cmd_vel` as `geometry_msgs/msg/TwistStamped` in Jazzy (not plain `Twist`; this is a frequent version trap), publishes `<name>/odom` and, when `enable_odom_tf` is true, the `odom` → `base_link` edge on `/tf`. Parameters: `left_wheel_names`, `right_wheel_names`, `wheel_separation`, `wheel_radius`.

### 10. gz_ros2_control: the simulation hardware interface

`gz_ros2_control` is a Gazebo system plugin that instantiates a controller manager inside the simulation process and connects it to a Gazebo model. Its joints are the hardware. Because the controller manager runs *inside* Gazebo, the control loop is stepped by the simulator's clock rather than by wall time — which is what makes a paused or slowed simulation behave correctly instead of racing.

**The real-time factor** is the number that ties those two clocks together. It is a ratio of two durations measured over the same stretch of one run:

$$\mathrm{RTF}=\frac{\Delta t_{\text{sim}}}{\Delta t_{\text{wall}}}$$

where $\Delta t_{\text{sim}}$ is how far simulated time (the `/clock` the bridge carries) advanced and $\Delta t_{\text{wall}}$ is how much wall-clock time passed meanwhile. $\mathrm{RTF}=1$ means the simulation keeps pace with the wall; $0.5$ means one simulated second takes two wall seconds, because the physics could not step faster or the world file asked for that pace. It is a measured property of a run on one machine, not of the model: the world file's `<real_time_factor>` is a target the simulator throttles to and falls below when the machine is too slow, and Gazebo shows the measured value in the bottom-right corner of its window. A non-example: `use_sim_time: true` is not a real-time factor. It says *which* clock a node reads, not how fast that clock runs. It matters because every sim-time duration $d$ occupies $d/\mathrm{RTF}$ of wall time, and wall time is what a real camera and a real motor are budgeted in (the Worked case's Step 5).

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
    update_rate: 200  # Hz, P6's f_c

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

`update_rate: 200` is the Running object's $f_c$, so the $5\,\mathrm{ms}$ period the Worked case computed with is the period your arm runs at. (The `gz_ros2_control` demos use `1000`, one update per $1\,\mathrm{ms}$ physics step of the default world; 200 is one update every five steps.)

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

You want both controllers `active`, the exercise's two `position` command interfaces each listed as `[available] [claimed]`, and `/joint_states` echoing at the broadcaster's rate. Then read that rate on both clocks — the Worked case's Step 5, in your terminal:

```bash
ros2 topic hz --use-sim-time /joint_states   # per simulated second: about 200, the update_rate
ros2 topic hz /joint_states                  # per wall second: about 200 × RTF
```

With nothing else loading the machine the RTF is close to 1 and the two agree.

**Step 6 — command a trajectory.**

```bash
ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.8, -1.0], time_from_start: {sec: 2, nanosec: 0}}]}"
```

The arm swings over two seconds. Send a second message with two points and different `time_from_start` values and watch it interpolate.

**Step 7 — make the Worked case's Step 5 happen.** Slow the world down on purpose. Find the stock world with `find /opt/ros/jazzy -name empty.sdf`, copy it next to your launch file as `half_speed.sdf`, and change its `<real_time_factor>1.0</real_time_factor>` to `0.5`. Point `gz_args` in the launch file at the copy (`'-r -v 1 /absolute/path/to/half_speed.sdf'`), relaunch, and repeat Steps 5 and 6. Predict first:

- `ros2 topic hz --use-sim-time /joint_states` still reads about $200$;
- plain `ros2 topic hz /joint_states` reads about $200\times0.5=100$;
- Step 6's two-second trajectory takes about $2/0.5=4\,\mathrm{s}$ by your watch, while `time_from_start` still says 2.

On the arm the only rate term is the hold, $T_c=5\,\mathrm{ms}$ of simulated time, and at this RTF it is $10\,\mathrm{ms}$ of wall time. Nothing logs a warning, which is the Worked case's point.

You are done when you can predict, before pressing enter, which joint moves which way for a given sign, and how long the motion will take by your watch at a given real-time factor.

### 12. The failure to diagnose: the controller is active and nothing moves

The symptom that eats an evening: `list_controllers` says `active`, no node logs an error, the simulation is running, and the arm sits still. Work the chain in this order, because each step rules out the one below it.

**1. Is it actually active, and has it stayed active?**

```bash
ros2 control list_controllers
```

`inactive` means configuration succeeded and activation did not — usually a missing interface, including a joint-name mismatch (step 3); the controller manager logs "Unable to activate controller '…' since the command interface '…' is not available." once, easy to lose in launch output. A controller that is *absent* from the list failed to load: for the joint trajectory controller, parameters that never arrived — a wrong `--param-file` path, or a YAML whose top-level key is not the controller's name — make `on_init` fail, and the spawner reports the error. A controller that activated and then fell back to `inactive` has had its hardware component go into an error state; check `ros2 control list_hardware_components -v`.

**2. Is it claiming the command interfaces?**

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers --claimed-interfaces
```

The first prints every command interface with two independent markers (state interfaces are listed without markers): `[available]` or `[unavailable]` says whether the hardware offers it, and `[claimed]` or `[unclaimed]` says whether an active controller holds it. A healthy interface reads `[available] [claimed]`. An active controller always holds its command interfaces — the controller manager refuses to activate one that cannot — so if yours read `[claimed]`, the chain up to the hardware is intact and the problem is downstream (step 4). `[available] [unclaimed]` means no active controller holds it: the controller you think is active is not the one you configured. An interface that reads `[unavailable]`, or that does not appear at all, sends you to step 3.

**3. Do the joint names agree?**

This is the most common reason a controller never becomes active. Three places name the same joints and all three must match character for character:

- the `<joint name="...">` elements of the URDF itself,
- the `<joint name="...">` entries inside the `<ros2_control>` block,
- the `joints:` list in the controller YAML.

`shoulder` in the URDF and `shoulder_joint` in the YAML gives you a controller that loads and configures but will not activate: `list_controllers` shows it `inactive`, and the only report that names the cause is one "Unable to activate controller 'joint_trajectory_controller' since the command interface 'shoulder_joint/position' is not available." warning. Diff the three lists explicitly:

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

If the subscription exists and the message is arriving, look at time. Four facts decide whether a received trajectory moves the arm:

- **Sim time.** The controller manager inside Gazebo runs on simulated time, not the wall clock.
- **Zero versus non-zero stamp.** `ros2 topic pub` leaves `header.stamp` at zero unless you write `now`, and the joint trajectory controller reads a zero stamp as "start now" — which is why step 6 works. A *non-zero* stamp is read on the controller's sim-time clock, so a wall-clock stamp puts the start far in the future and the arm waits.
- **The clock bridge.** Sim time only advances if the `/clock` bridge is running; check with `ros2 topic hz /clock`.
- **`time_from_start`.** It must be nonzero. A trajectory whose single point is at `t=0` is a command to be there instantly, which a position interface may satisfy so fast you see nothing.

Last, confirm the simulator is stepping at all: against a paused Gazebo, `ros2 topic hz /joint_states` prints no rate at all — it reports only when messages arrive, and a paused world publishes none — and a world started without `-r` is paused. Press play, or add `-r`.

### 13. What this page does not cover

Writing a hardware component of your own — a real driver behind the same interfaces — is 25.11's territory, along with the latency, safety and e-stop questions that simulation lets you ignore: [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]. Planning a collision-free trajectory to hand to the joint trajectory controller, rather than typing joint angles, is [[04-robotics/ros2/manipulation-moveit2|25.8 Manipulation with MoveIt 2]]. Sensor plugins, worlds, meshes and photorealistic rendering are Gazebo's own documentation. Chained controllers, transmissions, joint limit enforcement and controller-level safety are `ros2_control` topics one level deeper than this page. The whole track is indexed at [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- `ros2_control` documentation (Jazzy) — Getting Started (architecture, controller manager, resource manager, hardware components); Controller Manager userdoc (`update_rate`, `robot_description`, `spawner`, `unspawner`); `ros2controlcli` userdoc (CLI verbs and flags).
- `ros2_control` source (jazzy branch) — `controller_manager/src/controller_manager.cpp` (`check_for_interfaces_availability_to_activate`, the source of the "Unable to activate controller" warning).
- `ros2_controllers` documentation (Jazzy) — Controllers index; Joint Trajectory Controller; Forward Command Controller; Differential Drive Controller; Joint State Broadcaster.
- `gz_ros2_control` (jazzy branch) — README compatibility matrix; `doc/index.rst`; `gz_ros2_control_demos` cart launch file, controller YAML and URDF.
- `ros_gz` (ros2 branch) — `ros_gz_bridge` README (direction syntax, YAML config); `ros_gz_sim` README and `create.cpp` argument list.
- Gazebo documentation — Releases (Harmonic, Jetty support windows); ROS 2 Integration; Migration from Ignition.
- Open Robotics Discourse — "Gazebo Classic End-of-Life" (Gazebo 11 end of life, January 2025).
- `ros2_control` source (jazzy branch) — `ros2controlcli/verb/switch_controllers.py` (`--strict`, `--best-effort`, `--switch-timeout` default 5.0 s) and `list_hardware_interfaces.py` (the `[available]`/`[unavailable]` and `[claimed]`/`[unclaimed]` labels); `controller_manager/src/controller_manager_parameters.yaml` (`defaults.switch_controller.strictness`, default `best_effort`); `controller_manager/src/controller_manager.cpp` (strict versus best-effort handling of a controller that cannot activate; the switch waiting for the end of an `update()` while the controllers it names skip theirs).

### Self-check

1. Why does `ros2_control` put a named-interface seam between the controller and the hardware, rather than letting the controller write to the motor?
2. Your controller was spawned, the simulation is running, and the arm does not move. What is the first command, and what is the most likely cause?
3. Why does a `/clock` bridge matter, when nothing in the exercise reads the clock explicitly?
4. A tutorial tells you to add `<plugin filename="libgazebo_ros_control.so">` to your URDF. What is wrong with it?
5. You get a manipulation policy working in Gazebo. What can you claim?
6. On P6, the worked case spends $25\,\mathrm{ms}$ of the $70\,\mathrm{ms}$ budget on the two sampling rates alone. Which of the two terms would halving `update_rate` to 100 change, and by how much — and what would the same change do to the encoder's velocity quantum?

> [!tip]- Answers
> 1. Because the seam is what makes the controller portable. A controller asks for `shoulder/position` and neither knows nor cares whether a physics engine or an EtherCAT drive provides it, so the same controller and the same YAML run in Gazebo and on the real arm. Moving to hardware changes one `<plugin>` line in the URDF. It also enforces exclusivity: a command interface can be claimed by at most one active controller, which is why two writers on one joint is a failed activation rather than a fight.
> 2. `ros2 control list_controllers` — if it reads `inactive`, activation failed, and the most likely cause is a joint name that differs between the URDF, the `<ros2_control>` block and the controller YAML; the controller manager logged one "Unable to activate controller '…' since the command interface '…' is not available." warning. If it reads `active`, its command interfaces are necessarily `[available] [claimed]` in `list_hardware_interfaces`, so look downstream: the topic name, the trajectory's stamp and `time_from_start`, and whether the simulation is paused.
> 3. The controller manager runs inside Gazebo on simulated time. Without the bridge, ROS-side nodes that set `use_sim_time` — robot_state_publisher, TF consumers, anything stamping or looking up transforms — have no time source and stall, and a trajectory given a wall-clock stamp is read on the controller's sim clock as starting far in the future. (A zero stamp, which `ros2 topic pub` sends by default, means "start now" and dodges this.) Bridged topics are opt-in, and an unbridged topic does not exist on the ROS side with no error anywhere.
> 4. It is Gazebo Classic, which reached end of life in January 2025. The current stack is Gazebo Harmonic with `gz_ros2_control`: `<plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">` in a `<gazebo>` tag, plus `gz_ros2_control/GazeboSimSystem` as the hardware plugin in `<ros2_control>`. Anything written with `ign` prefixes is the intermediate Ignition era, renamed back to Gazebo in April 2022.
> 5. That the plumbing works — interfaces, controllers, topics, timing, and the launch ordering. Not that the contact behaviour transfers. [[05-construction-robotics/sim-to-real|Sim-to-Real]] separates the gaps randomisation can span from the contact gap it cannot, and a contact-rich result is not comparable evidence to a locomotion result even from the same simulator.
> 6. Only the hold term. The ledger is $A_{\max}=L+T_v+T_c$, and `update_rate` sets $T_c$ alone: at $100\,\mathrm{Hz}$ it becomes $10\,\mathrm{ms}$, so the rate cost rises from $25$ to $30\,\mathrm{ms}$ and the room left for $L$ falls from $45$ to $40\,\mathrm{ms}$. The $20\,\mathrm{ms}$ vision term is untouched, because it is set by the camera and no control rate can make a goal newer than the last frame. The encoder quantum moves the other way and is the reason this is a trade rather than a loss: differencing over $10\,\mathrm{ms}$ instead of $5$ halves the velocity quantum from $97.7$ to $48.8\,\mathrm{mm/s}$, so the slower loop reports a finer velocity and applies it later.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]] in Gazebo Harmonic. Controller `update_rate: 200`. Vision is a bridged camera at $50\,\mathrm{Hz}$. Budget $70\,\mathrm{ms}$. No new Euler simulator.

1. **Draw.** The picture above at item 2(a)'s rates, `update_rate: 500` and the camera at $30\,\mathrm{Hz}$: panel A with the new rate on the controller manager, and panel B on sim time over $0$–$100\,\mathrm{ms}$ — camera exposure, bridge, controller `read`–`update`–`write`, force — with the $70\,\mathrm{ms}$ budget, one frame's command span shaded, and the instants where a camera tick and a control tick coincide.
2. **Derive.** (a) Redo the worked case's Steps 1–3 with `update_rate: 500` and the camera at $30\,\mathrm{Hz}$: the tick-per-frame ratio, the velocity quantum from one-count differencing, and the rate ledger against the $70\,\mathrm{ms}$ budget. Say which of the two changes helped and which hurt. (b) The controller is `active` and the cart does not move. First command, most likely cause. (c) No `/clock` bridge; a trajectory is stamped with wall time. What does the sim-time controller read?
3. **Interpret.** A $200\,\mathrm{ms}$-late bridged vision frame still meets Gazebo's physics rate. Does it meet P6's budget? What can a Gazebo success claim, and what can it not?

> [!note]- How to draw it · 그리는 법
> - **Panel A nests three boxes left of the seam**: `Gazebo Harmonic`, holding the physics and the model, contains the `gz_ros2_control` system plugin, which contains the controller manager, now labelled `update_rate: 500`. Right of the dashed seam sit `joint_state_broadcaster` and the velocity controller.
> - **Interfaces are named arrows, not plain lines**: `cart/position` and `cart/velocity` cross the seam left to right as state, and `cart/velocity` comes back right to left as command, with the claim mark `[available] [claimed]`.
> - **`/clock` leaves Gazebo and enters ROS**, never the reverse, and **the camera arrow crosses a box marked `ros_gz_bridge`**: neither changes with the rates.
> - **Panel B is five parallel lanes against one axis in simulated milliseconds**, $0$ to $100$, with control ticks every $T_c=2\,\mathrm{ms}$ (mark every fifth if fifty is too many) and camera frames every $T_v=33.3\,\mathrm{ms}$, at $0$, $33.3$, $66.7$ and $100$.
> - **Circle the coincidences**: a camera tick lands on a control tick only at $0$ and $100\,\mathrm{ms}$, because $500/30=16.7$ is not an integer. Between them the goal's age at a tick differs from frame to frame, which the picture's clean ratio of $4$ hid.
> - **Shade one frame and bracket the budget**: from one camera tick, shade the span during which its command is still on the actuator, $L+T_v+T_c=L+35.3\,\mathrm{ms}$, against the picture's $L+25$. Draw the $70\,\mathrm{ms}$ budget as a bracket under the axis, with the sentence *this axis is sim time, and the budget is wall time.*

> [!tip]- Solutions
> 1. Panel A is the picture's with `update_rate: 500`; the plugin is still `gz_ros2_control/GazeboSimSystem`, and `/clock` still leaves Gazebo into ROS. Panel B: control ticks every $2\,\mathrm{ms}$ and camera frames every $33.3\,\mathrm{ms}$, coinciding only at $0$ and $100\,\mathrm{ms}$ — $50$ ticks and three frames — so the goal's age at a tick changes from frame to frame. A frame's command can still be on the cart $L+T_v+T_c=L+35.3\,\mathrm{ms}$ after mid-exposure, against $L+25$ in the picture: the faster loop took $3\,\mathrm{ms}$ off and the slower camera added $13.3$, which is item 2(a)'s ledger, drawn. The axis is sim time and the budget wall time, as before.
> 2. (a) $T_c=1/500=2\,\mathrm{ms}$ and $T_v=1/30=33.3\,\mathrm{ms}$, so the ratio is $500/30=16.7$ — *not* an integer, so ticks and frames line up only once every three frames ($100\,\mathrm{ms}=50$ ticks) and the goal's age differs from tick to tick, which the catalog's clean $4$ hid. The velocity quantum rises to $\Delta p/0.002=244\,\mathrm{mm/s}$, worse than the catalog's $97.7$, since a shorter differencing window divides the same single count by a smaller time. The ledger becomes $33.3+2=35.3\,\mathrm{ms}$, leaving $34.7$ against the catalog's $45$: the faster loop bought $3\,\mathrm{ms}$ and the slower camera cost $13.3$, a net loss of $10.3\,\mathrm{ms}$. The term you cannot reach from the controller is the one that dominates. (b) `ros2 control list_controllers`, to confirm it really reads `active`. If it does, its interface is `[claimed]` and the cause is downstream: the command topic, the stamp or `time_from_start`, or a paused simulation. A joint-name mismatch among URDF, `<ros2_control>`, YAML would have left it `inactive`. (c) A start far in the future (unless the stamp is zero, "start now").
> 3. No: $200>70$. Gazebo success claims plumbing — interfaces, rates, launch. Not that the $70\,\mathrm{ms}$ camera-to-force chain, or contact, will hold on hardware.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 기술한 로봇을 실제 제어 스택 위에서 시뮬레이션으로 움직이게 하고, 그것이 조용히 실패할 때 진단할 정도. 실제 구동계의 하드웨어 인터페이스를 작성할 정도는 아니다.
> **Working** — enough to make your described robot move in simulation under a real controller stack, and to diagnose the silent version of that not happening.

> [!note] 선수 지식 · Prerequisites
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**, 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]), [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot]]에서 만든 2링크 팔. 시뮬레이션 시간과 벽시계 시간의 구분이 여기서 중요해진다([[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]).
> A sourced ROS 2 Jazzy install, a buildable workspace, and the two-link arm from 25.6.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상과 그림을 보고 Worked case로 가라. 그 안의 한 줄 설명 셋이 §7(루프 주기)과 §10(루프가 시뮬레이션 시간으로 도는 이유, 그리고 실시간 계수)을 가리킨다. 그다음 §5–§7(이음매, 인터페이스, 컨트롤러 매니저)을 읽고 §11을 하라. 그 7단계가 Worked case의 Step 5를 당신의 터미널에서 일으킨다. §1–§4는 Gazebo 배경(시뮬레이션이 해결하는 것, 어느 Gazebo인가, 브리지, 스폰)이고, §8–§10은 참고 자료이며, §12는 active인 제어기가 아무것도 움직이지 않을 때 밟는 점검 사슬이다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**, 1차원 카트와 그 시계다. Gazebo Harmonic 안에 그려 넣고 `ros2_control`로 구동한다. 아래 숫자는 모두 카탈로그의 것이다.

*대상이 둘이라는 것을 한 번 밝혀 둔다.* 카트는 계산하는 대상이고, 이 페이지에서 그것을 만들지는 않는다. 실습(§11)은 대신 25.6의 2링크 팔을 만든다. 이미 가진 기술이 그것이기 때문이다. 팔로 그대로 옮겨 가는 것은 루프다. 실습이 같은 `update_rate: 200`을 쓰므로 Step 1의 $T_c=5\,\mathrm{ms}$와 Step 5의 실시간 계수 산수가 §11의 5단계와 7단계에서 직접 재는 값이다. 옮겨 가지 않는 것도 있다. 팔에는 엔코더가 없어서(Gazebo는 관절 각을 부동소수점 수로 보고한다) Step 2의 $0.488\,\mathrm{mm}$ 양자에 해당하는 것이 없고, 카메라도 없어서 $T_v$ 항이 없으며 팔의 속도 장부는 유지 항 $T_c$ 하나뿐이다.

| 기호 | 값 | 여기서의 뜻 |
|---|---:|---|
| $N$ | $2048$ counts/m | 카트 엔코더. 유일한 위치 센서 |
| $f_v$ | $50\,\mathrm{Hz}$ | 목표를 발행하는 비전 노드. Gazebo에서 브리지된다 |
| $f_c$ | $200\,\mathrm{Hz}$ | 컨트롤러 매니저 `update_rate`. §7의 `read`–`update`–`write` 루프 |
| $B$ | $70\,\mathrm{ms}$ | 카메라 노출 중간부터 힘이 나갈 때까지의 종단 예산 |
| $v$ | $0.25\,\mathrm{m/s}$ | 명령한 카트 속도 — **페이지 국소 값**. P6는 속도를 고정하지 않으며, 시간을 밀리미터로 바꾸는 데에만 쓴다 |

*범위: 이 페이지는 기술과 움직이는 로봇 사이의 배관 — 브리지, 인터페이스 이음매, 컨트롤러 매니저와 그 시계 — 을 가르치고, 그 속도들이 지연과 분해능으로 얼마를 치르는지 계산한다. 접촉 물리가 옮겨 가는지는 가르치지 않는다. 그것은 [[05-construction-robotics/sim-to-real|Sim-to-Real]]이다. 같은 이음매 뒤에 하드웨어 컴포넌트를 작성하는 법도 아니다. 그것은 [[04-robotics/ros2/from-simulation-to-hardware|25.11]]이다. 제어기에 넘길 궤적을 계획하는 법도 아니다. 그것은 [[04-robotics/ros2/manipulation-moveit2|25.8]]이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 574" style="max-width:100%;height:auto" role="img" aria-label="패널 A: Gazebo Harmonic 안에 gz_ros2_control 플러그인과 update_rate 200의 컨트롤러 매니저가 있고, 상태 인터페이스 cart/position과 cart/velocity가 이음매를 건너 제어기로 가며, 명령 인터페이스 cart/velocity는 available·claimed 표시를 달고 돌아오고, 카메라와 /clock은 ros_gz_bridge를 지나 Gazebo를 나간다. 패널 B: 시뮬레이션 시간 0에서 80 ms 위의 레인 다섯. 카메라는 20 ms, 제어기는 5 ms마다이고, 한 프레임의 명령은 L 더하기 25 ms 동안 카트에 걸려 있으며, 70 ms 예산은 벽시계 시간이다.">
  <text x="8" y="20" font-size="12" fill="currentColor" font-weight="600">A · 누가 무엇을 제공하는가</text>
  <rect x="8" y="24" width="226" height="172" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <text x="16" y="40" font-size="12" fill="currentColor">Gazebo Harmonic</text>
  <text x="16" y="54" font-size="11" fill="currentColor" opacity="0.75">물리와 모델: P6 카트</text>
  <rect x="16" y="62" width="210" height="102" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="22" y="76" font-size="11" fill="currentColor">gz_ros2_control system plugin</text>
  <rect x="24" y="84" width="194" height="74" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="32" y="101" font-size="11" fill="currentColor">controller manager</text>
  <text x="32" y="117" font-size="11" fill="currentColor">update_rate: 200</text>
  <text x="32" y="132" font-size="11" fill="currentColor" opacity="0.7">(시뮬레이션 1초당)</text>
  <rect x="16" y="170" width="96" height="20" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="64" y="184" font-size="11" fill="currentColor" text-anchor="middle">카메라 센서</text>
  <rect x="124" y="170" width="102" height="20" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <text x="175" y="184" font-size="11" fill="currentColor" text-anchor="middle">시뮬레이션 시계</text>
  <line x1="388" y1="70" x2="388" y2="190" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.6" stroke-dasharray="5 4"/>
  <text x="388" y="64" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.8">이음매</text>
  <text x="311" y="80" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.7">상태 인터페이스</text>
  <line x1="218" y1="96" x2="393.5" y2="96" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="400,96 393,99.4 393,92.6" fill="currentColor"/>
  <text x="311" y="92" font-size="11" fill="currentColor" text-anchor="middle">cart/position</text>
  <line x1="218" y1="114" x2="393.5" y2="114" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="400,114 393,117.4 393,110.6" fill="currentColor"/>
  <text x="311" y="110" font-size="11" fill="currentColor" text-anchor="middle">cart/velocity</text>
  <text x="311" y="131" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.7">명령 인터페이스</text>
  <line x1="400" y1="148" x2="224.5" y2="148" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="218,148 225,144.6 225,151.4" fill="currentColor"/>
  <text x="311" y="144" font-size="11" fill="currentColor" text-anchor="middle">cart/velocity</text>
  <text x="311" y="163" font-size="11" fill="currentColor" text-anchor="middle" font-weight="600">[available] [claimed]</text>
  <rect x="400" y="84" width="152" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="406" y="100" font-size="11" fill="currentColor">joint_state_broadcaster</text>
  <text x="406" y="116" font-size="11" fill="currentColor" opacity="0.7">/joint_states 발행</text>
  <rect x="400" y="134" width="152" height="40" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="406" y="150" font-size="11" fill="currentColor">속도 제어기</text>
  <text x="406" y="166" font-size="11" fill="currentColor" opacity="0.7">유일한 점유자</text>
  <rect x="8" y="212" width="226" height="34" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="121" y="226" font-size="11" fill="currentColor" text-anchor="middle">ros_gz_bridge</text>
  <text x="121" y="241" font-size="11" fill="currentColor" text-anchor="middle">토큰 [ : GZ → ROS 한 방향</text>
  <line x1="36" y1="190" x2="36" y2="253.5" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="36,260 32.6,253 39.4,253" fill="currentColor"/>
  <text x="42" y="207" font-size="11" fill="currentColor">/camera</text>
  <line x1="206" y1="190" x2="206" y2="259.5" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="206,266 202.6,259 209.4,259" fill="currentColor"/>
  <text x="212" y="207" font-size="11" fill="currentColor">/clock</text>
  <rect x="8" y="260" width="132" height="24" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <text x="74" y="276" font-size="11" fill="currentColor" text-anchor="middle">비전 노드 · 50 Hz</text>
  <text x="156" y="280" font-size="11" fill="currentColor" opacity="0.85">use_sim_time인 ROS 노드들</text>
  <polyline points="74,284 74,296 476,296" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="476" y1="296" x2="476" y2="180.5" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="476,174 479.4,181 472.6,181" fill="currentColor"/>
  <text x="468" y="292" font-size="11" fill="currentColor" text-anchor="end">/goal · 50 Hz</text>
  <line x1="8" y1="306" x2="552" y2="306" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="8" y="324" font-size="12" fill="currentColor" font-weight="600">B · 타임라인, 시뮬레이션 시간 위에서</text>
  <circle cx="280.1" cy="320.5" r="3.4" fill="currentColor"/>
  <text x="289.1" y="324" font-size="11" fill="currentColor" opacity="0.85">새 목표</text>
  <circle cx="343.1" cy="320.5" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <text x="352.1" y="324" font-size="11" fill="currentColor" opacity="0.85">같은 목표: 넷 중 셋</text>
  <rect x="460.4" y="316.5" width="8" height="8" fill="currentColor" fill-opacity="0.75"/>
  <text x="473.4" y="324" font-size="11" fill="currentColor" opacity="0.85">프레임 k의 명령</text>
  <rect x="170" y="360" width="115" height="120" fill="currentColor" fill-opacity="0.1"/>
  <line x1="170" y1="360" x2="170" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="193" y1="360" x2="193" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="216" y1="360" x2="216" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="239" y1="360" x2="239" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="262" y1="360" x2="262" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="285" y1="360" x2="285" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="308" y1="360" x2="308" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="331" y1="360" x2="331" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="354" y1="360" x2="354" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="377" y1="360" x2="377" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="400" y1="360" x2="400" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="423" y1="360" x2="423" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="446" y1="360" x2="446" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <line x1="469" y1="360" x2="469" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="492" y1="360" x2="492" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="515" y1="360" x2="515" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.13"/>
  <line x1="538" y1="360" x2="538" y2="480" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.32"/>
  <text x="8" y="376" font-size="11" fill="currentColor">카메라 노출</text>
  <line x1="170" y1="384" x2="538" y2="384" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="400" font-size="11" fill="currentColor">브리지</text>
  <line x1="170" y1="408" x2="538" y2="408" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="424" font-size="11" fill="currentColor">제어기 read</text>
  <line x1="170" y1="432" x2="538" y2="432" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="448" font-size="11" fill="currentColor">제어기 update/write</text>
  <line x1="170" y1="456" x2="538" y2="456" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <text x="8" y="472" font-size="11" fill="currentColor">카트에 걸리는 힘</text>
  <line x1="170" y1="480" x2="538" y2="480" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.12"/>
  <circle cx="170" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="262" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="354" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="446" cy="372" r="3.6" fill="currentColor"/>
  <circle cx="538" cy="372" r="3.6" fill="currentColor"/>
  <text x="176" y="367" font-size="11" fill="currentColor" opacity="0.9">프레임 k</text>
  <text x="268" y="367" font-size="11" fill="currentColor" opacity="0.9">k+1</text>
  <line x1="172.5" y1="377" x2="172.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="172.5,401 169.9,396 175.1,396" fill="currentColor"/>
  <line x1="264.5" y1="377" x2="264.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="264.5,401 261.9,396 267.1,396" fill="currentColor"/>
  <line x1="356.5" y1="377" x2="356.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="356.5,401 353.9,396 359.1,396" fill="currentColor"/>
  <line x1="448.5" y1="377" x2="448.5" y2="396.5" stroke="currentColor" stroke-width="1.1"/>
  <polygon points="448.5,401 445.9,396 451.1,396" fill="currentColor"/>
  <circle cx="170" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="193" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="216" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="239" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="262" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="285" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="308" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="331" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="354" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="377" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="400" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="423" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="446" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="469" cy="420" r="3.4" fill="currentColor"/>
  <circle cx="492" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="515" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="538" cy="420" r="3.4" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <rect x="167" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="190" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="213" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="236" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="259" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.9"/>
  <rect x="282" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="305" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="328" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="351" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="374" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="397" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="420" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="466" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="489" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="512" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="535" y="441" width="6" height="6" fill="currentColor" fill-opacity="0.35"/>
  <rect x="170.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="193.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="216.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="239.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="262.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.75"/>
  <rect x="285.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="308.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="331.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="354.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="377.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="400.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="423.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="446.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="469.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="492.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <rect x="515.8" y="463" width="21.4" height="10" fill="currentColor" fill-opacity="0.22"/>
  <polyline points="171,356 171,352 261,352 261,356" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>
  <polyline points="263,356 263,352 284,352 284,356" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>
  <text x="216" y="347" font-size="11" fill="currentColor" text-anchor="middle">T<tspan font-size="8.5" dy="2.5">v</tspan><tspan dy="-2.5" dx="4">= 20 ms</tspan></text>
  <text x="264" y="347" font-size="11" fill="currentColor">T<tspan font-size="8.5" dy="2.5">c</tspan><tspan dy="-2.5" dx="4">= 5 ms</tspan></text>
  <text x="329" y="347" font-size="11" fill="currentColor" font-weight="600">L + 20 + 5 = L + 25 ms</text>
  <line x1="170" y1="484" x2="538" y2="484" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="170" y1="484" x2="170" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="170" y="500" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="216" y1="484" x2="216" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="216" y="500" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <line x1="262" y1="484" x2="262" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="262" y="500" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <line x1="308" y1="484" x2="308" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="308" y="500" font-size="11" fill="currentColor" text-anchor="middle">30</text>
  <line x1="354" y1="484" x2="354" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="354" y="500" font-size="11" fill="currentColor" text-anchor="middle">40</text>
  <line x1="400" y1="484" x2="400" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="400" y="500" font-size="11" fill="currentColor" text-anchor="middle">50</text>
  <line x1="446" y1="484" x2="446" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="446" y="500" font-size="11" fill="currentColor" text-anchor="middle">60</text>
  <line x1="492" y1="484" x2="492" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="492" y="500" font-size="11" fill="currentColor" text-anchor="middle">70</text>
  <line x1="538" y1="484" x2="538" y2="488" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="538" y="500" font-size="11" fill="currentColor" text-anchor="middle">80</text>
  <text x="8" y="500" font-size="11" fill="currentColor" opacity="0.8">시뮬레이션 시간 (ms)</text>
  <polyline points="170,507 170,512 492,512 492,507" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
  <line x1="285" y1="507" x2="285" y2="515" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="8" y="516" font-size="11" fill="currentColor">예산 B = 70 ms</text>
  <text x="227.5" y="527" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">25: 속도들</text>
  <text x="388.5" y="527" font-size="11" fill="currentColor" text-anchor="middle" opacity="0.85">45 남음: L, 드라이버, 구동기</text>
  <text x="170" y="546" font-size="12" fill="currentColor" font-weight="600">이 축은 시뮬레이션 시간이고, 예산은 벽시계 시간이다.</text>
  <text x="8" y="564" font-size="11" fill="currentColor" opacity="0.75">최악의 경우를 그렸다. 목표는 틱 직후에 도착하고, L(노출 중간에서 도착까지)은 폭 0으로 그렸다.</text>
</svg>

패널 A는 Gazebo Harmonic 안의 P6 카트로, `gz_ros2_control` 플러그인이 `update_rate: 200`의 컨트롤러 매니저를 품고, 상태 인터페이스 `cart/position`과 `cart/velocity`가 이음매를 건너 제어기로 가며, 명령 인터페이스 `cart/velocity`는 유일한 점유자인 속도 제어기에서 `[available] [claimed]` 표시를 달고 돌아오고, 카메라와 `/clock`은 `ros_gz_bridge`를 거쳐야만 ROS에 닿는다. 패널 B는 같은 루프를 시뮬레이션 시간 위에 놓은 것으로, 카메라 프레임은 $T_v=20\,\mathrm{ms}$마다, 제어 틱은 $T_c=5\,\mathrm{ms}$마다 와서 틱 넷 중 셋이 지난 목표를 다시 쓰고, 최악의 경우 한 프레임의 명령은 노출 중간으로부터 $L+25\,\mathrm{ms}$ 뒤까지 카트에 걸려 있어(Worked case의 Step 3이 유도한다) $70\,\mathrm{ms}$ 예산 중 $L$과 드라이버와 구동기에 남는 몫은 $45\,\mathrm{ms}$다. 축은 시뮬레이션 시간이고, 예산은 벽시계 시간이다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 카탈로그 숫자로 여기서 먼저 계산해 두면 과제는 속도 하나를 바꾸는 일이지 첫 유도가 아니다.

**Step 1 — 주기 둘과 그 비.** 컨트롤러 매니저의 `update_rate`는 Hz 단위 주파수이므로(§7)

$$T_c=\frac{1}{f_c}=\frac{1}{200}=5\,\mathrm{ms},\qquad T_v=\frac{1}{f_v}=\frac{1}{50}=20\,\mathrm{ms},\qquad \frac{f_c}{f_v}=\frac{200}{50}=4,$$

이다. 그래서 루프는 카메라 프레임 하나당 `read`–`update`–`write`를 네 번 완주하고, 그중 셋은 이미 본 목표를 다시 본다. 타임라인이 보여야 하는 것은 둘 중 한 속도가 아니라 이 비다.

**Step 2 — 엔코더 한 카운트의 값.** 카트 엔코더는 길이당 카운트이므로 양자는 그 역수다.

$$\Delta p=\frac{1}{N}=\frac{1}{2048}=4.883\times10^{-4}\,\mathrm{m}=0.488\,\mathrm{mm}.$$

제어 주기 하나 떨어진 두 위치 읽기를 차분하면 보고할 수 있는 가장 작은 0이 아닌 속도는 주기당 한 카운트, 즉 $\Delta p/T_c=0.0977\,\mathrm{m/s}=97.7\,\mathrm{mm/s}$다. 분자가 취할 수 있는 가장 작은 변화가 한 카운트이기 때문이다. 같은 차분을 비전 구간 전체에 걸쳐 하면 양자는 $\Delta p/T_v=24.4\,\mathrm{mm/s}$로 내려가고 대신 창 $20\,\mathrm{ms}$의 절반인 $10\,\mathrm{ms}$의 지연을 문다. [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]의 속도 추정기가 하는 잡음–지연 거래와 같은 것이다.

**Step 3 — 속도만으로 생기는 낡음.** 측정이 노출 중간 $t_0$에 일어나고, 그 순간부터 목표 메시지가 제어기에 도착할 때까지의 모든 것을 $L$이라 하자. 노출 반폭, 판독, 브리지, DDS다. 속도는 $L$ 뒤에 항 둘을 더한다. 제어기는 다음 프레임이 이 목표를 갈아치울 때까지 계속 쓰고, 그것은 길어야 $T_v$ 뒤다. 그리고 그 마지막 틱에서 계산된 명령은 기록된 뒤 다음 틱까지 *유지되므로* $T_c$가 한 번 더 붙는다. 그래서 그 프레임이 만든 힘이 아직 카트에 걸려 있는 동안 비전 측정이 가질 수 있는 최악의 나이는

$$A_{\max}=L+T_v+T_c=L+20+5=L+25\,\mathrm{ms}$$

이다. 낡은 목표가 얼마나 오래 살아남는지를 비전 주기가, 낡은 명령이 얼마나 오래 유지되는지를 제어 주기가 각각 묶기 때문이다. P6의 예산에 대면 $L$ 전체와 드라이버와 구동기가 쓸 몫으로 $70-25=45\,\mathrm{ms}$가 남는다. 내 코드가 한 줄도 돌기 전에 속도들이 이미 예산의 $36\%$를 썼다.

**Step 4 — 같은 장부를 밀리미터로.** 페이지 국소 값 $v=0.25\,\mathrm{m/s}$에서 카트는 그 $25\,\mathrm{ms}$ 동안 $0.25\times0.025=6.25\,\mathrm{mm}$를 간다. 이는 $6.25\times2.048=12.8$ 엔코더 카운트다. 아무것도 늦지 않아도 제어기가 쫓는 목표는 카트보다 열세 카운트 가까이 뒤에 있다. 제어 주기당으로는 $0.25\times0.005=1.25\,\mathrm{mm}=2.56$ 카운트여서 양자보다 넉넉히 위다. 속도를 $0.05\,\mathrm{m/s}$로 낮추면 한 주기가 $0.25\,\mathrm{mm}=0.512$ 카운트를 덮으므로 틱의 절반 가까이에서 카운트가 *전혀* 바뀌지 않고, 차분 속도는 정확히 $0$ 아니면 정확히 $97.7\,\mathrm{mm/s}$를 읽는다. 가장 매끄럽기를 바랐던 속도에서 속도 신호가 순수한 양자화 잡음이 된다.

**Step 5 — 그리고 Gazebo가 그 무엇도 보증하지 못하는 이유.** 컨트롤러 매니저는 시뮬레이터 안에서 돌므로 `update_rate: 200`은 시뮬레이션 1초당 200틱이다(§10). 실시간 계수는 벽시계 1초당 흐른 시뮬레이션 시간, $\mathrm{RTF}=\Delta t_{\text{sim}}/\Delta t_{\text{wall}}$이다(정의는 §10). 이것이 $0.5$, 즉 절반 속도로 도는 시뮬레이션이라고 하자. 루프는 *벽시계* 1초당 $200\times0.5=100$번 실행되고, Step 3의 $25\,\mathrm{ms}$ 시뮬레이션 장부는 벽시계로 $25/0.5=50\,\mathrm{ms}$를 차지해 남는 몫이 $45$가 아니라 $70-50=20\,\mathrm{ms}$가 된다.

시뮬레이션 안에서는 아무것도 잘못되지 않는다. 시뮬레이션 시간은 내부적으로 일관되고, 궤적은 잘 추종되며, `ros2 topic hz --use-sim-time /joint_states`는 시뮬레이션 1초당 200을 보고한다. 플래그를 빼면 같은 명령이 약 100을 보고한다. Jazzy의 `ros2 topic hz`는 도착 시각을 자기 노드의 시계로 찍는데, 그 노드는 `-s`/`--use-sim-time`을 줄 때만 `/clock`을 따르고 그렇지 않으면 벽시계를 읽기 때문이다(jazzy 브랜치의 `ros2topic/verb/hz.py`와 `ros2cli/node/direct.py`. `--wall-time`은 플래그가 있어도 벽시계를 강제한다).

P6의 $70\,\mathrm{ms}$는 실제 카메라와 실제 모터에 관한 벽시계 예산이고, 실시간 계수를 보고하지 않은 실행은 그것을 잰 적이 없다. 이것이 §1의 경고를 정확한 형태로 쓴 것이고, 과제 3번이 소리 내어 말하라고 요구하는 것이다. §11의 7단계가 이것을 당신의 팔에서 일으킨다.

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

당신에게 오는 귀결: **새 작업을 Gazebo Classic에서 시작하지 마라.** 지원이 끝났고, `<gazebo><plugin filename="libgazebo_ros_control.so">`를 쓰라는 모든 튜토리얼은 죽은 시스템을 설명하고 있다. 현행 LTS 릴리스는 **Harmonic**(2023년 9월 – 2029년 5월)과 **Jetty**(2025년 9월 – 2031년 5월)다. Fortress(LTS, 2027년 5월까지)와 Ionic(2026년 12월까지)도 아직 지원되지만 새 작업용은 아니다.

이 페이지는 **Gazebo Harmonic** 을 쓴다. ROS 2 Jazzy와 바이너리 패키지가 있는 짝이기 때문이다 — `ros-jazzy-ros-gz`, `ros-jazzy-gz-ros2-control`. Lyrical Luth는 같은 방식으로 Jetty와 짝을 이룬다. 아래 구조는 그대로이고 패키지 이름만 바뀐다.

### 3. 메시지 체계가 둘인 이유, 그리고 브리지

Gazebo는 ROS 프로그램이 아니다. 자체 전송 계층(Gazebo Transport)과 자체 메시지 정의(`gz.msgs.*`, Protobuf)를 갖고, ROS가 없어도 멀쩡히 돈다. ROS 2는 DDS(ROS 2의 전송 표준, [[04-robotics/ros2/what-ros2-is#5. 아래에 깔린 DDS: 무엇을 사고 무엇을 치르는가|25.1 §5]] 참고)와 `sensor_msgs/msg/*`를 쓴다. 둘은 서로의 와이어 포맷도 타입 체계도 모른다.

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

Gazebo는 URDF를 내부적으로 SDF(Simulation Description Format, 로봇과 world를 기술하는 Gazebo 고유 형식)로 변환해 파싱한다. 쓴 것 대부분은 살아남는다. 초심자가 잃는 부분은 URDF에 개념이 없는 것들이고, 그래서 추가 정보는 URDF 파서가 무시하고 SDF 변환기가 읽는 `<gazebo>` 태그에 들어간다.

### 5. ros2_control: 이음매

토픽을 읽어 관절 힘을 주는 Gazebo 플러그인을 직접 쓸 수도 있다. 실제로 그렇게 하고, 그러면 로봇이 실물이 되는 날 그 코드는 쓸모가 없어진다.

`ros2_control`은 그 경로 한가운데에 정의된 이음매를 놓고 양쪽에 안정된 인터페이스를 두려고 존재한다.

- 한쪽에는 **제어기(controller)** — 관절 궤적 추종기, 차동 구동 기구학 계층, PID(오차에 대한 비례·적분·미분 피드백, [[04-robotics/control-theory-ce397#7. 피드백 설계: 극점 배치와 PID|5. 제어 이론 §7]]에서 유도). 제어기는 `ControllerInterface`에서 파생된 객체이고, `update()`가 상태를 읽고 명령을 쓴다. 하드웨어가 무엇인지는 전혀 모른다.
- 다른 쪽에는 **하드웨어 컴포넌트** — 모터 드라이버, CAN 버스(모터 드라이브에 흔한 2선 직렬 버스), EtherCAT 슬레이브(이더넷 기반 실시간 필드버스인 EtherCAT 위의 장치 하나), 또는 시뮬레이터와 실제로 대화하는 것. 세 종류가 있다: `System`(결합이 있는 다자유도), `Actuator`(1자유도, 읽기·쓰기), `Sensor`(읽기 전용).

> **하드웨어 컴포넌트의 정의.** **하드웨어 컴포넌트**는 *이음매 아래에서 하드웨어 하나를 대신하는 플러그인 클래스*다. 그 하드웨어는 드라이브일 수도, 센서 보드일 수도, 시뮬레이션 속 모델일 수도 있다. 정의 조건은 셋이다. **이름 붙은 인터페이스를 내보낸다.** 읽을 수 있는 상태 인터페이스와 지시할 수 있는 명령 인터페이스다(6절). **타입이 내보낼 수 있는 것을 정한다.** `Sensor`는 읽기만 하고, `Actuator`는 관절 하나를 읽고 쓰며, `System`은 채널 하나로 관절 여럿을 읽고 쓴다. 그리고 **제어기에 박혀 있지 않고 선언된다.** `<ros2_control>` 블록의 `type`과 `<hardware><plugin>` 줄이 그것을 지명하고, 컨트롤러 매니저가 그 이름으로 싣고 7절의 루프에서 `read()`와 `write()`를 부른다.
>
> $$\mathcal{C}_{\texttt{Sensor}}=\varnothing,\qquad \mathcal{C}_{\texttt{Actuator}}\subseteq\{j\}\times\mathcal{N},\qquad \mathcal{C}_{\texttt{System}}\subseteq J\times\mathcal{N}$$
>
> 여기서 $\mathcal{C}$는 컴포넌트가 내보내는 명령 인터페이스의 집합이고 원소는 `joint/name` 쌍이다. $j$는 관절 하나, $J$는 관절 집합, $\mathcal{N}$은 인터페이스 이름(`position`, `velocity`, `effort`, …)이다.
>
> - **예**: Gazebo 안의 P6 카트는 `System` 하나, `gz_ros2_control/GazeboSimSystem`이다. 상태 $\{\texttt{cart/position},\ \texttt{cart/velocity}\}$와 명령 $\{\texttt{cart/velocity}\}$를 내보내고, 시뮬레이션 1초에 $200$번 읽히고 쓰인다.
> - **비예**: P6의 카메라. 감지는 하지만 `Sensor` 컴포넌트가 아니다. 그 프레임은 `ros_gz_bridge`를 거쳐 $50\,\mathrm{Hz}$ 토픽으로 ROS에 닿고 `read()` 밖에 있다. 그래서 $T_v=20\,\mathrm{ms}$가 대상으로 한 번 끝까지의 장부에 $T_c$와 따로 들어가고, 어떤 `update_rate`로도 그것을 줄일 수 없다.

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

> **명령 인터페이스와 상태 인터페이스의 정의.** **인터페이스**는 *하드웨어 컴포넌트가 내보내는 이름 붙은 숫자*이고, `joint/name`으로 쓴다. `cart/velocity`가 그 하나다. 정의 조건은 셋이다. **상태 인터페이스**는 이음매 위에서 읽히며, **몇 개의 제어기든 동시에 읽을 수 있다.** **명령 인터페이스**는 쓰이며, **한 번에 많아야 활성 제어기 하나가 쥔다.** 제어기를 활성화하면 그것이 나열한 명령 인터페이스를 모두 점유(claim)하고, 비활성화될 때까지 놓지 않는다. 그리고 제어기는 나열한 인터페이스가 모두 내보내져 있고 그 명령 인터페이스를 이미 쥔 쪽이 없을 **때만 활성화된다.** 그래서 아무것과도 맞지 않는 이름은 적재가 아니라 활성화에서 실패한다.
>
> $$\mathrm{activate}(k)\iff R_{\text{cmd}}(k)\subseteq\mathcal{C}\setminus H\ \ \wedge\ \ R_{\text{state}}(k)\subseteq\mathcal{S}$$
>
> 여기서 $R_{\text{cmd}}(k)$와 $R_{\text{state}}(k)$는 제어기 $k$가 나열한 명령·상태 인터페이스, $\mathcal{C}$와 $\mathcal{S}$는 하드웨어가 내보내는 명령·상태 인터페이스, $H$는 다른 활성 제어기들이 쥔 것이다.
>
> - **예**: P6의 속도 제어기는 $R_{\text{cmd}}=\{\texttt{cart/velocity}\}$를 나열한다. 내보내져 있고 $H=\varnothing$에 없으므로 활성화되고, 그 인터페이스는 `[available] [claimed]`로 읽힌다. 그동안 `joint_state_broadcaster`는 `cart/position`과 `cart/velocity`를 나란히 읽는다.
> - **비예**: 같은 카트에 두 번째 속도 제어기. 이제 $\texttt{cart/velocity}\in H$이므로 활성화가 "currently claimed by another controller"로 거부된다. 한 구동기에 writer 둘은 줄다리기가 아니라 실패한 활성화이고, 이음매가 존재하는 이유인 안전성이 바로 이것이다.

이 블록에서 시뮬레이션과 실제 로봇이 다른 부분은 `<hardware><plugin>` 줄 하나뿐이다.

### 7. 컨트롤러 매니저

**컨트롤러 매니저(controller manager)** 는 양쪽을 붙들고 있는 프로세스다. `pluginlib`(등록된 이름으로 공유 라이브러리에서 C++ 클래스를 실행 중에 불러오는 ROS 라이브러리)으로 하드웨어 컴포넌트를 싣고, 같은 방식으로 제어기를 싣고, 요구된 인터페이스와 제공된 인터페이스를 맞추고, 루프를 돈다: 하드웨어에서 `read()`, 활성 제어기마다 `update()`, 하드웨어로 `write()`. `update_rate` 파라미터가 그 루프의 주파수(Hz)이고 기본값은 100이다. 로봇 기술은 `robot_description` 토픽을 구독해 얻는다.

> **컨트롤러 매니저의 정의.** **컨트롤러 매니저**는 *제어 루프를 소유한 노드*이고, 그 자체는 제어기가 아니다. 정의 조건은 셋이다. **양쪽을 이름으로 싣는다.** 하드웨어 컴포넌트는 리소스 매니저를 통해, 제어기는 `pluginlib`으로 싣는다. 각 제어기가 나열한 것을 하드웨어가 내보내는 것과 **맞춰 보고**, 6절의 규칙으로 활성화를 허락하거나 거부한다. 그리고 **`update_rate`로 루프 하나를 돈다.** 매 주기 하드웨어의 `read()`, 각 *활성* 제어기의 `update()`, 하드웨어의 `write()`를 그 순서로 부르고, 실려 있어도 비활성인 제어기는 건너뛴다.
>
> $$T_c=\frac{1}{f_c},\qquad u(t)=u_k\quad \forall\,t\in[\,kT_c,\ (k+1)T_c)$$
>
> 여기서 $f_c$는 Hz 단위의 `update_rate`(정하지 않으면 $100$), $u_k$는 $k$번째 틱에 쓴 명령이다. 명령은 다음 쓰기까지 하드웨어에 남으므로, $T_c$가 대상으로 한 번 끝까지의 속도 장부에 들어간다.
>
> - **예**: P6의 `update_rate: 200`이면 $T_c=5\,\mathrm{ms}$. $20\,\mathrm{ms}$ 카메라 프레임 하나당 read–update–write가 네 번이고, 쓴 속도 명령은 하나하나 $5\,\mathrm{ms}$씩 유지된다.
> - **비예**: `update_rate`를 카메라에서 힘까지 사슬 전체의 속도로 읽는 것. $500$으로 올려도 줄어드는 것은 유지 구간뿐이어서 $5$에서 $2\,\mathrm{ms}$가 되고, 속도 장부는 $20+5=25$에서 $20+2=22\,\mathrm{ms}$가 될 뿐이다. 매니저는 마지막 카메라 프레임보다 새 목표를 만들 수 없으므로, 빠른 루프가 $70\,\mathrm{ms}$ 예산에서 사 오는 것은 $3\,\mathrm{ms}$다.

제어기는 상태 셋이 중요한 lifecycle 객체다([[04-robotics/ros2/services-actions-parameters#8. 관리형(라이프사이클) 노드|25.3 §8]]의 관리형 노드 상태 기계).

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

이 동사들 가운데 둘은 한 번 더 들여다볼 만하다. `list_hardware_interfaces`는 §6의 점유 규칙을 눈에 보이게 한 것이다. 모든 명령 인터페이스가 `[available]` 또는 `[unavailable]`, 그리고 `[claimed]` 또는 `[unclaimed]`로 찍히므로, 적재와 설정은 되는데 활성화되지 않는 제어기는 한 줄로 설명된다. 그 인터페이스가 이미 점유되었거나 아예 없는 것이다. §6의 상자가 P6의 `cart/velocity`를 그렇게 읽는다.

`switch_controllers`에는 알아 둘 기본값이 있다. `--strict`도 `--best-effort`도 주지 않으면 매니저는 자기 파라미터 `defaults.switch_controller.strictness`를 따르는데, 그 값이 `best_effort`다. 활성화할 수 없는 제어기는 요청에서 빠지고 비활성화는 그대로 실행되므로, `--deactivate a --activate b`는 P6의 카트에 활성 제어기가 하나도 없는 상태를 남길 수 있다. §7의 원자적 전환이 없애려는 바로 그 구간이다. `--strict`는 요청을 전부 아니면 전무로 만들고, 움직이는 카트를 인계할 때는 그것을 써야 한다. 전환은 루프 한가운데 끼어드는 대신 루프에 맞춰 이뤄진다. 매니저는 `update()` 하나가 끝나기를 기다리는데, 이는 대략 한 주기 안, P6의 `update_rate: 200`에서 $5\,\mathrm{ms}$ 안이다. 그리고 요청에 이름이 오른 제어기들은 전환이 끝날 때까지 update를 건너뛴다. CLI는 `--switch-timeout`, 기본 $5.0\,\mathrm{s}$, 곧 P6의 $5.0/0.005=1000$주기까지 기다린 뒤에야 전환이 실패했다고 알린다.

### 9. 실제로 쓰게 될 제어기들

`ros2_controllers`가 한 묶음을 제공한다. 넷이 대부분의 작업을 덮는다.

| 제어기 | 용도 | 요구 인터페이스 |
|---|---|---|
| `joint_state_broadcaster/JointStateBroadcaster` | 상태 인터페이스를 읽어 `/joint_states`로 publish. 명령한다는 의미의 제어기는 아니지만, 이것 없이는 아무도 로봇을 보지 못한다 | 상태만 |
| `joint_trajectory_controller/JointTrajectoryController` | 시간이 붙은 다관절 궤적을 추종. MoveIt 2가 실행에 쓰는 것 | `position`, 또는 PID 게인과 함께 `velocity`/`effort` |
| `forward_command_controller` 계열 (`position_controllers/JointGroupPositionController` 및 velocity·effort 판) | 궤적도 보간도 없이 명령 배열을 하드웨어로 그대로 전달. 학습된 정책이나 직접 짠 루프에 맞는 도구 | 지정한 것 |
| `diff_drive_controller/DiffDriveController` | 몸체 속도를 좌우 바퀴 명령으로 변환하고 오도메트리를 publish | 바퀴 관절의 `velocity` |

실제로 손으로 치게 되는 표면.

- **관절 궤적 제어기** — 토픽 `<name>/joint_trajectory`(`trajectory_msgs/msg/JointTrajectory`), 액션 `<name>/follow_joint_trajectory`(`control_msgs/action/FollowJointTrajectory`). 동작이 끝났는지 알아야 하면 액션을 쓴다. 토픽은 보내고 잊는 쪽이다. 파라미터는 `joints`, `command_interfaces`, `state_interfaces`. `state_interfaces`에는 `position`이 반드시 있어야 하고, 명령 인터페이스가 `velocity`나 `effort` 단독일 때는 `velocity`도 있어야 한다. 그 경우 제어기가 추종 오차에 PID 루프를 닫는데, 그 루프가 위치뿐 아니라 측정된 관절 속도도 쓰기 때문이다.
- **Forward command 제어기** — 토픽 `<name>/commands`(`std_msgs/msg/Float64MultiArray`), 파라미터 `joints`(범용 `forward_command_controller/ForwardCommandController`에는 `interface_name`도 있고, position/velocity/effort 변형은 인터페이스가 고정이다). 배열은 위치 기반이다. *i* 번째 원소가 `joints` 목록의 *i* 번째 관절로 간다. 그 순서를 의도했는지 검증하는 것은 아무것도 없다.
- **차동 구동 제어기** — Jazzy에서는 `<name>/cmd_vel`을 `geometry_msgs/msg/TwistStamped`로 구독한다(평범한 `Twist`가 아니다. 버전 함정으로 자주 걸린다). `<name>/odom`을 publish하고, `enable_odom_tf`가 true면 `/tf`에 `odom` → `base_link` 간선을 낸다. 파라미터는 `left_wheel_names`, `right_wheel_names`, `wheel_separation`, `wheel_radius`.

### 10. gz_ros2_control: 시뮬레이션용 하드웨어 인터페이스

`gz_ros2_control`은 시뮬레이션 프로세스 안에 컨트롤러 매니저를 만들고 그것을 Gazebo 모델에 연결하는 Gazebo 시스템 플러그인이다. 그 관절이 곧 하드웨어다. 컨트롤러 매니저가 Gazebo *안에서* 돌기 때문에 제어 루프는 벽시계가 아니라 시뮬레이터의 시계로 진행된다. 일시정지하거나 느리게 돌린 시뮬레이션에서도 폭주하지 않고 올바르게 동작하는 이유다.

**실시간 계수**(real-time factor)는 그 두 시계를 묶는 숫자다. 한 실행의 같은 구간에서 잰 두 시간 길이의 비다.

$$\mathrm{RTF}=\frac{\Delta t_{\text{sim}}}{\Delta t_{\text{wall}}}$$

여기서 $\Delta t_{\text{sim}}$은 시뮬레이션 시간(브리지가 나르는 `/clock`)이 나아간 양, $\Delta t_{\text{wall}}$은 그동안 흐른 벽시계 시간이다. $\mathrm{RTF}=1$이면 시뮬레이션이 벽시계와 보조를 맞추고, $0.5$이면 시뮬레이션 1초가 벽시계 2초를 먹는다. 물리가 더 빨리 걸을 수 없었거나 월드 파일이 그 속도를 요구했기 때문이다. 이것은 모델의 성질이 아니라 한 기계에서 돈 한 실행을 잰 값이다. 월드 파일의 `<real_time_factor>`는 시뮬레이터가 맞춰 늦추는 목표치이고 기계가 느리면 그 아래로 떨어지며, Gazebo는 잰 값을 창 오른쪽 아래에 보여 준다. 아닌 예 하나: `use_sim_time: true`는 실시간 계수가 아니다. 노드가 *어느* 시계를 읽는지를 말할 뿐, 그 시계가 얼마나 빨리 가는지는 말하지 않는다. 이것이 중요한 이유는 시뮬레이션 시간의 길이 $d$가 벽시계로는 $d/\mathrm{RTF}$를 차지하고, 실제 카메라와 실제 모터의 예산은 벽시계로 매겨지기 때문이다(Worked case의 Step 5).

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
    update_rate: 200  # Hz, P6's f_c

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

`update_rate: 200`은 이 페이지의 대상의 $f_c$이므로, Worked case가 계산에 쓴 $5\,\mathrm{ms}$ 주기가 곧 당신의 팔이 도는 주기다. (`gz_ros2_control` 데모는 기본 월드의 $1\,\mathrm{ms}$ 물리 스텝마다 한 번씩 갱신하는 `1000`을 쓴다. 200은 다섯 스텝마다 한 번이다.)

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

제어기 둘이 `active`, 이 실습이 만든 `position` 명령 인터페이스 둘이 각각 `[available] [claimed]`, 그리고 브로드캐스터 주기로 `/joint_states`가 나와야 한다. 그다음 그 주기를 두 시계로 읽어라. Worked case의 Step 5를 당신의 터미널에서 하는 것이다.

```bash
ros2 topic hz --use-sim-time /joint_states   # per simulated second: about 200, the update_rate
ros2 topic hz /joint_states                  # per wall second: about 200 × RTF
```

기계에 다른 부하가 없으면 실시간 계수는 1에 가깝고 두 값이 일치한다.

**6단계 — 궤적 명령.**

```bash
ros2 topic pub -1 /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder, elbow], points: [{positions: [0.8, -1.0], time_from_start: {sec: 2, nanosec: 0}}]}"
```

팔이 2초에 걸쳐 움직인다. 점 두 개와 서로 다른 `time_from_start`로 메시지를 한 번 더 보내고 보간을 지켜보라.

**7단계 — Worked case의 Step 5를 일으킨다.** 일부러 월드를 느리게 만든다. `find /opt/ros/jazzy -name empty.sdf`로 기본 월드를 찾아 launch 파일 옆에 `half_speed.sdf`로 복사하고, 그 안의 `<real_time_factor>1.0</real_time_factor>`를 `0.5`로 바꾼다. launch 파일의 `gz_args`가 복사본을 가리키게 하고(`'-r -v 1 /absolute/path/to/half_speed.sdf'`) 다시 띄운 뒤 5단계와 6단계를 반복하라. 먼저 예측하라.

- `ros2 topic hz --use-sim-time /joint_states`는 여전히 약 $200$을 읽는다.
- 그냥 `ros2 topic hz /joint_states`는 약 $200\times0.5=100$을 읽는다.
- 6단계의 2초짜리 궤적은 손목시계로 약 $2/0.5=4\,\mathrm{s}$가 걸리지만 `time_from_start`는 여전히 2라고 말한다.

팔에서 속도 항은 유지 항 하나, 시뮬레이션 시간으로 $T_c=5\,\mathrm{ms}$뿐이고, 이 실시간 계수에서 그것은 벽시계로 $10\,\mathrm{ms}$다. 경고는 하나도 찍히지 않는다. 그것이 Worked case가 말하려던 바다.

엔터를 치기 전에 어떤 부호가 어느 관절을 어느 쪽으로 움직일지, 그리고 주어진 실시간 계수에서 그 동작이 손목시계로 얼마나 걸릴지 예측할 수 있으면 끝이다.

### 12. 진단할 고장: 제어기는 active인데 아무것도 움직이지 않는다

저녁 하나를 잡아먹는 증상. `list_controllers`는 `active`라 하고, 어떤 노드도 에러를 찍지 않고, 시뮬레이션은 돌고 있는데, 팔은 가만히 있다. 아래 순서대로 확인하라. 각 단계가 그 아래 단계를 배제한다.

**1. 정말로 active인가, 그리고 계속 active였는가?**

```bash
ros2 control list_controllers
```

`inactive`는 설정은 됐고 활성화가 안 됐다는 뜻이고, 보통 인터페이스가 없어서다 — 관절 이름 불일치(3단계)도 여기에 속한다. 컨트롤러 매니저는 "Unable to activate controller '…' since the command interface '…' is not available."라는 경고를 한 번 찍는데, launch 출력에 묻히기 쉽다. 목록에 아예 *없는* 제어기는 적재에 실패한 것이다. joint trajectory controller라면 파라미터가 도착하지 않았을 때 — `--param-file` 경로가 틀렸거나 YAML의 최상위 키가 제어기 이름이 아닐 때 — `on_init`이 실패하고 spawner가 오류를 보고한다. 활성화됐다가 `inactive`로 떨어진 제어기는 하드웨어 컴포넌트가 에러 상태로 간 것이다. `ros2 control list_hardware_components -v`로 확인한다.

**2. 명령 인터페이스를 점유하고 있는가?**

```bash
ros2 control list_hardware_interfaces
ros2 control list_controllers --claimed-interfaces
```

첫 명령은 모든 명령 인터페이스를 찍으면서 서로 독립적인 표시 둘을 붙인다(상태 인터페이스는 표시 없이 나열된다). `[available]`과 `[unavailable]`은 하드웨어가 그것을 제공하는지를, `[claimed]`와 `[unclaimed]`는 활성 제어기가 쥐고 있는지를 말한다. 정상 인터페이스는 `[available] [claimed]`다. 활성 제어기는 언제나 자기 명령 인터페이스를 쥐고 있다 — 쥘 수 없는 제어기는 컨트롤러 매니저가 활성화를 거부한다 — 그러니 `[claimed]`로 나오면 하드웨어까지의 사슬은 멀쩡하고 문제는 그 아래(4단계)다. `[available] [unclaimed]`는 어떤 활성 제어기도 쥐고 있지 않다는 뜻이다. 활성이라고 믿는 제어기가 내가 설정한 그 제어기가 아니다. `[unavailable]`로 나오거나 아예 나타나지 않는 인터페이스는 3단계로 보낸다.

**3. 관절 이름이 일치하는가?**

제어기가 끝내 활성화되지 않는 가장 흔한 원인이다. 같은 관절을 세 곳이 이름 부르며, 셋이 글자 하나까지 같아야 한다.

- URDF 자체의 `<joint name="...">` 요소,
- `<ros2_control>` 블록 안의 `<joint name="...">` 항목,
- 제어기 YAML의 `joints:` 목록.

URDF에는 `shoulder`, YAML에는 `shoulder_joint`이면 적재되고 설정되지만 활성화되지 않는 제어기가 나온다. `list_controllers`에는 `inactive`로 보이고, 원인을 밝히는 보고는 "Unable to activate controller 'joint_trajectory_controller' since the command interface 'shoulder_joint/position' is not available." 경고 한 줄뿐이다. 세 목록을 명시적으로 비교하라.

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

구독이 있고 메시지도 도착한다면 시간을 보라. 수신된 궤적이 팔을 움직이는지는 네 가지로 정해진다.

- **시뮬레이션 시간.** Gazebo 안의 컨트롤러 매니저는 벽시계가 아니라 시뮬레이션 시간으로 돈다.
- **0 스탬프와 0이 아닌 스탬프.** `ros2 topic pub`은 `now`를 쓰지 않는 한 `header.stamp`를 0으로 두고, joint trajectory controller는 0 스탬프를 "지금 시작"으로 읽는다 — 6단계가 되는 이유다. 0이 *아닌* 스탬프는 제어기의 시뮬레이션 시계로 읽히므로, 벽시계 스탬프는 시작을 먼 미래에 놓고 팔은 기다린다.
- **시계 브리지.** 시뮬레이션 시간은 `/clock` 브리지가 돌 때만 흐른다. `ros2 topic hz /clock`으로 확인한다.
- **`time_from_start`.** 0이 아니어야 한다. 점 하나가 `t=0`인 궤적은 "지금 당장 거기 있어라"라는 명령이고, position 인터페이스는 그것을 눈에 보이지 않을 만큼 빨리 만족시킬 수 있다.

마지막으로 시뮬레이터가 진행 중인지 확인한다. 일시정지된 Gazebo에 대해 `ros2 topic hz /joint_states`는 아무 주기도 출력하지 않는다. 메시지가 도착할 때만 보고하는데 일시정지된 world는 아무것도 내지 않기 때문이다. `-r` 없이 시작한 world는 일시정지 상태다. 재생을 누르거나 `-r`을 붙여라.

### 13. 이 페이지가 다루지 않는 것

같은 인터페이스 뒤에 실제 드라이버를 놓는 하드웨어 컴포넌트를 직접 작성하는 것은 25.11의 영역이고, 시뮬레이션이 무시하게 해 주는 지연·안전·비상정지 문제도 거기 있다: [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]. 관절 각도를 손으로 치는 대신 충돌 없는 궤적을 계획해 관절 궤적 제어기에 넘기는 것은 [[04-robotics/ros2/manipulation-moveit2|25.8 Manipulation with MoveIt 2]]. 센서 플러그인, world, 메시, 사실적 렌더링은 Gazebo 자체 문서의 몫이다. 체인 제어기, transmission, 관절 한계 강제, 제어기 수준의 안전은 이 페이지보다 한 단계 깊은 `ros2_control` 주제다. 트랙 전체 색인은 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- `ros2_control` 문서(Jazzy) — Getting Started(구조, 컨트롤러 매니저, 리소스 매니저, 하드웨어 컴포넌트); Controller Manager userdoc(`update_rate`, `robot_description`, `spawner`, `unspawner`); `ros2controlcli` userdoc(CLI 동사와 플래그).
- `ros2_control` 소스(jazzy 브랜치) — `controller_manager/src/controller_manager.cpp`(`check_for_interfaces_availability_to_activate`, "Unable to activate controller" 경고가 나오는 곳).
- `ros2_controllers` 문서(Jazzy) — Controllers index; Joint Trajectory Controller; Forward Command Controller; Differential Drive Controller; Joint State Broadcaster.
- `gz_ros2_control`(jazzy 브랜치) — README 호환 표; `doc/index.rst`; `gz_ros2_control_demos`의 cart launch 파일, 제어기 YAML, URDF.
- `ros_gz`(ros2 브랜치) — `ros_gz_bridge` README(방향 문법, YAML 설정); `ros_gz_sim` README와 `create.cpp` 인자 목록.
- Gazebo 문서 — Releases(Harmonic, Jetty 지원 기간); ROS 2 Integration; Migration from Ignition.
- Open Robotics Discourse — "Gazebo Classic End-of-Life"(Gazebo 11 지원 종료, 2025년 1월).
- `ros2_control` 소스(jazzy 브랜치) — `ros2controlcli/verb/switch_controllers.py`(`--strict`, `--best-effort`, 기본 5.0 s인 `--switch-timeout`)와 `list_hardware_interfaces.py`(`[available]`/`[unavailable]`, `[claimed]`/`[unclaimed]` 표시), `controller_manager/src/controller_manager_parameters.yaml`(`defaults.switch_controller.strictness`, 기본 `best_effort`), `controller_manager/src/controller_manager.cpp`(활성화할 수 없는 제어기를 strict와 best effort가 다루는 방식, `update()` 하나가 끝나기를 기다리는 전환과 그동안 update를 건너뛰는 해당 제어기).

### 스스로 점검

1. `ros2_control`은 왜 제어기가 모터에 직접 쓰게 두지 않고 이름 붙은 인터페이스 이음매를 두는가?
2. 제어기를 spawn했고 시뮬레이션은 돌고 팔은 안 움직인다. 첫 명령은 무엇이고 가장 유력한 원인은?
3. 실습에서 아무도 시계를 명시적으로 읽지 않는데 `/clock` 브리지가 왜 중요한가?
4. 어떤 튜토리얼이 URDF에 `<plugin filename="libgazebo_ros_control.so">`를 넣으라고 한다. 무엇이 잘못됐나?
5. Gazebo에서 매니퓰레이션 정책이 동작한다. 무엇을 주장할 수 있나?
6. P6에서 계산 절은 $70\,\mathrm{ms}$ 예산 중 $25\,\mathrm{ms}$를 두 샘플링 속도만으로 쓴다. `update_rate`를 100으로 절반 낮추면 두 항 중 어느 것이 얼마나 바뀌는가? 같은 변경이 엔코더의 속도 양자에는 무엇을 하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 그 이음매가 제어기를 이식 가능하게 만들기 때문이다. 제어기는 `shoulder/position`을 요구할 뿐 그것을 물리 엔진이 주는지 EtherCAT 드라이브가 주는지 알지도 신경 쓰지도 않는다. 그래서 같은 제어기와 같은 YAML이 Gazebo에서도 실제 팔에서도 돈다. 하드웨어로 옮기는 것은 URDF의 `<plugin>` 한 줄을 바꾸는 일이다. 배타성도 여기서 나온다. 명령 인터페이스는 활성 제어기 하나만 점유할 수 있고, 그래서 한 관절에 writer 둘이 붙는 상황은 싸움이 아니라 활성화 실패가 된다.
> 2. `ros2 control list_controllers` — `inactive`면 활성화가 실패한 것이고, 가장 유력한 원인은 URDF, `<ros2_control>` 블록, 제어기 YAML 사이의 관절 이름 불일치다. 컨트롤러 매니저는 "Unable to activate controller '…' since the command interface '…' is not available." 경고를 한 번 찍었을 것이다. `active`라면 그 명령 인터페이스는 `list_hardware_interfaces`에서 반드시 `[available] [claimed]`이므로, 그 아래를 본다: 토픽 이름, 궤적의 스탬프와 `time_from_start`, 시뮬레이션이 일시정지됐는지.
> 3. 컨트롤러 매니저는 Gazebo 안에서 시뮬레이션 시간으로 돈다. 브리지가 없으면 `use_sim_time`을 켠 ROS 쪽 노드 — robot_state_publisher, TF 소비자, 스탬프를 찍거나 변환을 조회하는 모든 것 — 에 시간 원천이 없어 멈추고, 벽시계 스탬프를 준 궤적은 제어기의 시뮬레이션 시계에서 먼 미래에 시작하는 것으로 읽힌다. (`ros2 topic pub`이 기본으로 보내는 0 스탬프는 "지금 시작"이라 이 문제를 비켜 간다.) 브리지된 토픽은 opt-in이고, 브리지되지 않은 토픽은 ROS 쪽에 존재하지 않으면서 아무 에러도 남기지 않는다.
> 4. Gazebo Classic이고, 2025년 1월에 지원이 종료됐다. 현행 스택은 Gazebo Harmonic + `gz_ros2_control`이다. `<gazebo>` 태그 안에 `<plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin">`, 그리고 `<ros2_control>` 안의 하드웨어 플러그인으로 `gz_ros2_control/GazeboSimSystem`. `ign` 접두사로 쓰인 것은 중간의 Ignition 시대이고, 2022년 4월에 Gazebo로 되돌려졌다.
> 5. 배관이 동작한다는 것 — 인터페이스, 제어기, 토픽, 타이밍, launch 순서. 접촉 거동이 전이된다는 것은 아니다. [[05-construction-robotics/sim-to-real|Sim-to-Real]]은 랜덤화가 걸칠 수 있는 격차와 걸칠 수 없는 접촉 격차를 분리하며, 접촉이 많은 결과는 같은 시뮬레이터에서 나온 보행 결과와 견줄 수 있는 증거가 아니다.
> 6. 유지 항만 바뀐다. 장부는 $A_{\max}=L+T_v+T_c$이고 `update_rate`가 정하는 것은 $T_c$뿐이다. $100\,\mathrm{Hz}$에서는 $10\,\mathrm{ms}$가 되므로 속도가 치르는 값은 $25$에서 $30\,\mathrm{ms}$로 오르고 $L$에 남는 자리는 $45$에서 $40\,\mathrm{ms}$로 준다. $20\,\mathrm{ms}$짜리 비전 항은 그대로다. 그것은 카메라가 정하고, 어떤 제어 속도도 목표를 마지막 프레임보다 새롭게 만들 수 없기 때문이다. 엔코더 양자는 반대 방향으로 움직이고, 그래서 이것이 손실이 아니라 거래다. $5$ 대신 $10\,\mathrm{ms}$에 걸쳐 차분하면 속도 양자가 $97.7$에서 $48.8\,\mathrm{mm/s}$로 절반이 되므로, 느린 루프는 더 고운 속도를 더 늦게 내놓는다.

### 과제 · Problem set

Tier B. Gazebo Harmonic 안의 [[02-foundations/lab-plants|0.6]] **P6**. 제어기 `update_rate: 200`. 비전은 $50\,\mathrm{Hz}$로 브리지된 카메라. 예산 $70\,\mathrm{ms}$. 새 오일러 시뮬레이터는 만들지 마라.

1. **그리기.** 2(a)번의 주기, `update_rate: 500`과 $30\,\mathrm{Hz}$ 카메라에서의 위 그림: 컨트롤러 매니저에 새 주기를 적은 패널 A, 그리고 $0$–$100\,\mathrm{ms}$의 시뮬 시간 위 패널 B — 카메라 노출, 브리지, 제어기 `read`–`update`–`write`, 힘 — 와 $70\,\mathrm{ms}$ 예산, 음영으로 칠한 프레임 하나의 명령 구간, 그리고 카메라 틱과 제어 틱이 겹치는 순간들.
2. **유도.** (a) 계산 절의 Step 1–3을 `update_rate: 500`과 $30\,\mathrm{Hz}$ 카메라로 다시 하라. 프레임당 틱 비, 한 카운트 차분의 속도 양자, 그리고 $70\,\mathrm{ms}$ 예산에 대한 속도 장부. 두 변경 중 무엇이 도왔고 무엇이 해쳤는지 말하라. (b) 제어기는 `active`인데 카트가 안 움직인다. 첫 명령, 가장 유력한 원인. (c) `/clock` 브리지가 없고 궤적에 벽시계 스탬프. 시뮬 시간 제어기는 무엇을 읽는가?
3. **해석.** $200\,\mathrm{ms}$ 늦은 브리지 비전 프레임이 Gazebo 물리 주기는 만족한다. P6 예산을 만족하는가? Gazebo 성공이 주장할 수 있는 것과 없는 것은?

> [!note]- 그리는 법 · How to draw it
> - **패널 A는 이음매 왼쪽에 상자 셋을 겹쳐 넣는다.** 물리와 모델을 쥔 `Gazebo Harmonic` 안에 `gz_ros2_control` system plugin, 다시 그 안에 이제 `update_rate: 500`이라 적은 컨트롤러 매니저. 점선 이음매 오른쪽에는 `joint_state_broadcaster`와 속도 제어기를 둔다.
> - **인터페이스는 맨 선이 아니라 이름 붙은 화살표다.** 상태인 `cart/position`과 `cart/velocity`는 왼쪽에서 오른쪽으로 이음매를 건너고, 명령인 `cart/velocity`는 점유 표시 `[available] [claimed]`를 달고 오른쪽에서 왼쪽으로 돌아온다.
> - **`/clock`은 Gazebo에서 나와 ROS로 들어가고**(반대 방향은 없다), **카메라 화살표는 `ros_gz_bridge`라고 쓴 상자를 지나간다.** 둘 다 주기와 상관없이 그대로다.
> - **패널 B는 시뮬레이션 밀리초로 된 축 하나에 건 평행한 레인 다섯이다.** $0$부터 $100$까지이고, 제어 틱은 $T_c=2\,\mathrm{ms}$마다(쉰 개가 너무 많으면 다섯째마다 표시), 카메라 프레임은 $T_v=33.3\,\mathrm{ms}$마다, 곧 $0$, $33.3$, $66.7$, $100$에 둔다.
> - **겹치는 순간에 동그라미를 친다.** $500/30=16.7$이 정수가 아니므로 카메라 틱이 제어 틱과 겹치는 것은 $0$과 $100\,\mathrm{ms}$뿐이다. 그 사이에서는 틱에서 본 목표의 나이가 프레임마다 다르고, 위 그림의 깔끔한 비 $4$가 그것을 가렸다.
> - **프레임 하나를 칠하고 예산을 괄호로 묶는다.** 카메라 틱 하나에서 시작해 그 명령이 아직 구동기에 걸려 있는 구간 $L+T_v+T_c=L+35.3\,\mathrm{ms}$를 칠하고, 위 그림의 $L+25$와 견준다. 축 아래에 $70\,\mathrm{ms}$ 예산을 괄호로 긋고 한 문장을 적는다. *이 축은 시뮬레이션 시간이고, 예산은 벽시계 시간이다.*

> [!tip]- 정답 · Solutions
> 1. 패널 A는 `update_rate: 500`인 위 그림이다. 플러그인은 여전히 `gz_ros2_control/GazeboSimSystem`이고 `/clock`도 여전히 Gazebo에서 ROS로 나간다. 패널 B: 제어 틱은 $2\,\mathrm{ms}$마다, 카메라 프레임은 $33.3\,\mathrm{ms}$마다 오고, 둘은 $0$과 $100\,\mathrm{ms}$에서만 겹친다 — 틱 $50$개, 프레임 셋. 그래서 틱에서 본 목표의 나이가 프레임마다 바뀐다. 한 프레임의 명령은 노출 중간 뒤 $L+T_v+T_c=L+35.3\,\mathrm{ms}$까지 카트에 걸려 있을 수 있고, 위 그림은 $L+25$였다. 빠른 루프가 $3\,\mathrm{ms}$를 덜고 느린 카메라가 $13.3$을 더했다. 2(a)번의 장부를 그린 것이다. 축은 시뮬 시간이고 예산은 벽시계 시간인 것도 그대로다.
> 2. (a) $T_c=1/500=2\,\mathrm{ms}$, $T_v=1/30=33.3\,\mathrm{ms}$이므로 비는 $500/30=16.7$이다. 정수가 *아니어서* 틱과 프레임이 세 프레임에 한 번($100\,\mathrm{ms}=50$틱)만 맞아떨어지고 목표의 나이가 틱마다 달라진다. 카탈로그의 깔끔한 $4$가 가리고 있던 사실이다. 속도 양자는 $\Delta p/0.002=244\,\mathrm{mm/s}$로 올라 카탈로그의 $97.7$보다 나빠진다. 차분 창이 짧아지면 같은 한 카운트를 더 작은 시간으로 나누기 때문이다. 장부는 $33.3+2=35.3\,\mathrm{ms}$가 되어 카탈로그의 $45$ 대신 $34.7$만 남는다. 빠른 루프가 $3\,\mathrm{ms}$를 벌고 느린 카메라가 $13.3$을 썼으니 순손실 $10.3\,\mathrm{ms}$다. 제어기에서 손댈 수 없는 항이 지배한다. (b) `ros2 control list_controllers`로 정말 `active`인지 확인. 그렇다면 인터페이스는 `[claimed]`이고 원인은 그 아래다. 명령 토픽, 스탬프나 `time_from_start`, 일시정지된 시뮬레이션. URDF, `<ros2_control>`, YAML 사이 관절 이름 불일치였다면 `inactive`로 남았을 것이다. (c) 먼 미래 시작(스탬프 0, "지금 시작"이 아니면).
> 3. 아니오: $200>70$. Gazebo 성공은 배관 — 인터페이스, 주기, launch — 을 주장한다. $70\,\mathrm{ms}$ 카메라–힘 사슬이나 접촉이 하드웨어에서 버틴다는 것은 아니다.
