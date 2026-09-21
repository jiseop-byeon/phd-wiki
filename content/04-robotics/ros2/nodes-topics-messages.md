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
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], meaning a working **ROS 2 Jazzy Jalisco on Ubuntu 24.04** install that you can source, and the graph-reading commands from its section 9. Python; enough C++ to read a class. Every command below assumes a sourced terminal.
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], 즉 source 가능한 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 설치와 거기 9절의 그래프 읽기 명령들. Python과, 클래스를 읽을 정도의 C++. 아래 모든 명령은 source된 터미널을 전제한다.

*Comes after this page, not before it: building your own packages is taught properly in [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]], which assumes this page. Here you use the minimum of it, and each step says which lines matter.*

### Homework diagram: two P6 nodes, with every name resolved

The object is **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] — a cart on a line, encoder $N=2048$ counts/m, vision publishing a goal at $50\,\mathrm{Hz}$, a controller commanding the motor at $200\,\mathrm{Hz}$, $70\,\mathrm{ms}$ of end-to-end budget. Both nodes are launched into the namespace `/cart`. Draw three panels; the problem set asks for the same three with the namespace changed.

<svg viewBox="0 0 560 378" style="max-width:100%;height:auto" role="img" aria-label="Left: nodes camera and controller launched into /cart, with code names and resolved names, the topic goal resolving to /cart/goal, and a stray /goal stub on the controller. Right: inside the controller, on_goal at 50 Hz stores the goal and on_tick on a 5 ms timer reads the store and the encoder and publishes cmd. Bottom: goals at 0 and 20 ms, ticks every 5 ms, three ticks re-using one goal, encoder reads, and the 70 ms budget for scale.">
  <defs><marker id="n2eopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="n2esol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">Names, as written and as resolved</text>
  <ellipse cx="54" cy="84" rx="36" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="54" y="88" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">vision</text>
  <text x="54" y="116" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">camera</text>
  <text x="54" y="131" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/camera</text>
  <ellipse cx="222" cy="84" rx="42" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="222" y="88" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">control</text>
  <text x="222" y="116" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">controller</text>
  <text x="222" y="131" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/controller</text>
  <line x1="90" y1="84" x2="178" y2="84" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2eopen)"/>
  <text x="135" y="78" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <text x="135" y="99" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/goal</text>
  <line x1="276" y1="44" x2="241.7" y2="69" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2eopen)"/>
  <text x="270" y="40" font-size="11" text-anchor="end" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <text x="12" y="166" font-size="11" fill-opacity="0.6" fill="currentColor">upper: the string in the code</text>
  <text x="12" y="180" font-size="11" fill-opacity="0.6" fill="currentColor">lower: resolved under /cart</text>
  <text x="12" y="196" font-size="11" fill-opacity="0.6" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan>: a second name, no publisher (§10)</text>
  <text x="300" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">Inside controller: two callbacks</text>
  <ellipse cx="438" cy="108" rx="112" ry="76" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <text x="438" y="52" font-size="11" text-anchor="middle" fill-opacity="0.6" font-family="ui-monospace,monospace" fill="currentColor">/cart/controller</text>
  <rect x="352" y="66" width="74" height="22" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <text x="389" y="81" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">on_goal</text>
  <rect x="446" y="66" width="70" height="22" rx="3" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none"/>
  <text x="481" y="81" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">goal store</text>
  <line x1="426" y1="77" x2="444" y2="77" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" fill="none" marker-end="url(#n2esol)"/>
  <line x1="292" y1="77" x2="350" y2="77" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2eopen)"/>
  <text x="292" y="70" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <text x="292" y="96" font-size="11" fill-opacity="0.9" fill="currentColor">50 Hz</text>
  <rect x="352" y="122" width="90" height="22" rx="3" stroke="currentColor" stroke-width="1.5" stroke-opacity="0.9" fill="none"/>
  <circle cx="363" cy="133" r="6.5" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <line x1="363" y1="133" x2="363" y2="129" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <line x1="363" y1="133" x2="366.5" y2="133" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <text x="374" y="137" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">on_tick</text>
  <text x="356" y="115" font-size="11" fill-opacity="0.9" fill="currentColor">200 Hz, 5 ms</text>
  <line x1="470" y1="88" x2="438" y2="121" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" fill="none" marker-end="url(#n2esol)"/>
  <text x="476" y="110" font-size="11" fill-opacity="0.75" font-style="italic" fill="currentColor">reads</text>
  <line x1="382" y1="198" x2="382" y2="145" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="2 3" fill="none" marker-end="url(#n2esol)"/>
  <text x="388" y="197" font-size="11" fill-opacity="0.8" fill="currentColor">encoder (outside the graph)</text>
  <line x1="442" y1="133" x2="552" y2="133" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2eopen)"/>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">cmd</text>
  <text x="12" y="222" font-size="12" fill-opacity="0.8" fill="currentColor">Five lines of clock (ms)</text>
  <text x="100" y="244" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">goal 50 Hz</text>
  <text x="100" y="266" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">tick 200 Hz</text>
  <text x="100" y="288" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">re-use</text>
  <text x="100" y="308" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">encoder read</text>
  <text x="100" y="330" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">budget</text>
  <line x1="108" y1="240" x2="228" y2="240" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <circle cx="108" cy="240" r="4.2" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="228" cy="240" r="4.2" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <line x1="108" y1="262" x2="228" y2="262" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <path d="M108.0 256v12M138.0 256v12M168.0 256v12M198.0 256v12M228.0 256v12" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" fill="none"/>
  <path d="M138.0 277V284H198.0V277" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none"/>
  <text x="208" y="288" font-size="11" fill-opacity="0.85" fill="currentColor">ticks 5, 10, 15 re-use the goal from 0</text>
  <rect x="104.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="134.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="164.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="194.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="224.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <line x1="108" y1="326" x2="528" y2="326" stroke="currentColor" stroke-width="2.4" stroke-opacity="0.8" fill="none"/>
  <line x1="108" y1="320" x2="108" y2="332" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <line x1="528" y1="320" x2="528" y2="332" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <text x="318" y="319" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">70 ms budget, for scale</text>
  <line x1="108" y1="344" x2="528" y2="344" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="108" y1="344" x2="108" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="138" y1="344" x2="138" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="168" y1="344" x2="168" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="198" y1="344" x2="198" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="228" y1="344" x2="228" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="258" y1="344" x2="258" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="288" y1="344" x2="288" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="318" y1="344" x2="318" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="348" y1="344" x2="348" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="378" y1="344" x2="378" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="408" y1="344" x2="408" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="438" y1="344" x2="438" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="468" y1="344" x2="468" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="498" y1="344" x2="498" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="528" y1="344" x2="528" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <text x="108" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="138" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">5</text>
  <text x="168" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">10</text>
  <text x="198" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">15</text>
  <text x="228" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">20</text>
  <text x="288" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">30</text>
  <text x="348" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">40</text>
  <text x="408" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">50</text>
  <text x="468" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="528" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">70</text>
  <path d="M108.0 270V344M138.0 270V344M168.0 270V344M198.0 270V344M228.0 270V344" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.25" stroke-dasharray="1 3" fill="none"/>
</svg>

**Left — the two nodes, each labelled with both of its names.** Two ellipses. Under each, two lines: the name the code passes to `super().__init__` (`camera`, `controller`) and the fully resolved name after the launch namespace (`/cart/camera`, `/cart/controller`). Between them, one arrow for the topic, labelled twice in the same way: the string written in the code (`goal`) above the arrow and what section 3's table resolves it to (`/cart/goal`) below it. Then draw a *second* arrow stub leaving the controller, labelled `/goal`, with nothing on the other end. That is section 10's bug, and the point of drawing it is that it is a second name, not a broken arrow — nothing in the picture is red.

**Right — inside the controller, the two callbacks.** Two boxes within the node ellipse. `on_goal` fires when a message arrives, so it is drawn with the subscription arrow entering it and is labelled $50\,\mathrm{Hz}$; all it does is store the goal, so draw the store as a small box beside it. `on_tick` fires on a $5\,\mathrm{ms}$ timer, so it is drawn with a clock symbol and labelled $200\,\mathrm{Hz}$; it reads the store *and* the encoder, and the `cmd` arrow leaves the node from `on_tick`. Draw the encoder as an arrow into `on_tick` from outside the graph. The diagram is wrong the moment `cmd` leaves from `on_goal`, and section 9 is where you make that mistake on purpose.

**Bottom — five lines of clock.** Line 1: goals at $0$ and $20\,\mathrm{ms}$. Line 2: ticks at $0,5,10,15,20\,\mathrm{ms}$. Line 3: a bracket under ticks $5$, $10$ and $15$ marking them as re-users of the goal from $0$. Line 4: an encoder read on every tick. Line 5: the $70\,\mathrm{ms}$ budget line, for scale.

### Worked case: one encoder count through a message, and what it is worth in velocity

Six numbers, all of them from P6's two constants and two rates.

**Step 1 — counts to metres.** The encoder is a counter; the graph must carry metres. With $N=2048$ counts/m the conversion and its resolution are

$$p=\frac{c}{N}=\frac{c}{2048}\,\mathrm{m},\qquad \Delta p=\frac{1}{2048}=4.8828125\times10^{-4}\,\mathrm{m}=0.488\,\mathrm{mm}$$

because one count is one unit of $c$, so nothing this encoder ever reports distinguishes two positions closer than half a millimetre. At $c=1024$ the cart is at exactly $0.5\,\mathrm{m}$.

**Step 2 — the message that carries it.** Section 4 told you what `std_msgs/msg/Float64` costs. Here is the type this cart deserves, in its own interface package:

```text
# Cart state, from the encoder on the rail. See 0.6 Lab Plants, P6.
std_msgs/Header header
int32 counts        # raw quadrature counts since homing
float64 position    # m, = counts / 2048.0
```

The raw count travels beside the derived metre for a reason that is entirely practical: `counts` is exact and `position` is not, so a downstream node that suspects the scale factor can check it, and a bag recorded today survives a recalibration tomorrow. The `Header` carries the stamp the $70\,\mathrm{ms}$ budget is measured against.

**Step 3 — what one count is worth as a velocity.** A controller that wants speed usually differences two positions one period apart, and the resolution of that estimate is the resolution of the position divided by the period:

$$\Delta v=\frac{\Delta p}{T}=\frac{1/2048}{T}\quad\Longrightarrow\quad \Delta v\big|_{200\,\mathrm{Hz}}=\frac{0.00048828125}{0.005}=0.0977\,\mathrm{m/s},\qquad \Delta v\big|_{50\,\mathrm{Hz}}=\frac{0.00048828125}{0.020}=0.0244\,\mathrm{m/s}$$

since dividing a fixed quantum by a shorter interval magnifies it. Read the first number again: at the control rate, **one count of jitter is $9.8\,\mathrm{cm/s}$ of apparent speed**. A cart crawling at $2\,\mathrm{cm/s}$ produces a velocity signal that alternates between $0$ and $9.8\,\mathrm{cm/s}$, and no amount of care in the message type fixes it. That is why a fast loop differences over a longer window, or filters, or reads velocity from somewhere other than a naive difference — and why publishing a bare `float64 velocity` with no stamp and no statement of how it was computed is the worst of the options in section 4.

**Step 4 — how often each thing happens.** $T_{\text{vision}}/T_{\text{ctrl}}=20/5=4$ exactly, so each goal is consumed by four ticks, and in one $70\,\mathrm{ms}$ budget window there are $14$ ticks and $3$ complete vision periods. Now the design choice of section 9, on P6's numbers: publish `cmd` from `on_goal` and the motor is commanded at $50\,\mathrm{Hz}$, because a callback-driven publisher inherits its input's rate; publish from the $5\,\mathrm{ms}$ timer and it is commanded at $200\,\mathrm{Hz}$ with the newest goal in hand, whatever the camera is doing. The second is the contract P6 states, which is why the controller is timer-driven and the store between the callbacks exists.

**Step 5 — and the name that silently undoes all of it.** Both nodes are launched into `/cart`. Section 3's three forms then resolve like this:

| Written in the controller's code | Resolves to | Consequence for P6 |
|---|---|---|
| `goal` (relative) | `/cart/goal` | matches the camera's relative `goal`; data flows |
| `/goal` (absolute) | `/goal` | namespace ignored; two names, no connection, no error |
| `~/gain` (private) | `/cart/controller/gain` | per-node configuration, safe to launch twice |

One character of difference between rows one and two costs a silent robot: `ros2 node list` shows both nodes, `ros2 topic list -t` shows *two* names where you expected one, and the motor holds its last command forever. Section 10 is the four commands that find it, and this is the case they find.

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

"One logical thing" is not "one file" and not "one class". A useful test is the restart test: if you would ever want to restart, replace, re-tune or re-deploy piece A without disturbing piece B, A and B are different nodes. A camera driver and a detector fail that test in opposite directions — you will swap detectors weekly and never touch the driver — so they are two nodes. A detector and the non-maximum-suppression step inside it (the post-processing that deletes duplicate, overlapping boxes around one object) will always live and die together, so they are one.

Two refinements on top of the beginner picture:

- A node is not exactly a process. One process can host several nodes; ROS 2 calls this composition, and it is how a real stack avoids paying serialisation costs (converting a message to bytes and back) between nodes that happen to run on the same machine: nodes sharing one process's memory can hand a message over directly when intra-process communication is enabled. Composition is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]].
- A node's name is not its executable's name. You saw this in 25.1: `turtlesim_node` names itself `/turtlesim`, and `--ros-args --remap __node:=my_turtle` renames it at launch without touching the code.

### 3. Topics, and the anonymity that is the point

A topic is a name. Any number of publishers and any number of subscribers may attach to it, and when any publisher publishes, every subscriber in the system receives the data.

The word the documentation uses for the relationship is **anonymous**: when a subscriber receives a message, it does not generally know or care which publisher sent it. This is not a missing feature. It is the property that makes substitution work. The subscriber has no handle on the producer, so there is nothing in the subscriber to change when the producer is replaced.

The other property is **strongly typed**, and it has two halves. The mechanical half: each field has a declared type, enforced by generated code in every language. The semantic half, which has no enforcement at all: the core message types carry agreed meanings — the angular velocity from an IMU (inertial measurement unit, the accelerometer-plus-gyroscope sensor) is in radians per second, and nothing else belongs in that field. Nothing will stop you from publishing degrees. The type checker cannot help you; the convention is the only thing holding.

Names follow rules worth internalising now, because section 10's bug lives here:

| Form | Example | Resolves to |
|---|---|---|
| Absolute | `/turtle1/pose` | `/turtle1/pose`, ignoring the node's namespace |
| Relative | `turtle1/pose` | namespace + name — in namespace `/watch`, `/watch/turtle1/pose` |
| Private | `~/pose` | node's namespace + node name + `/pose` — node `monitor` in namespace `/watch` gives `/watch/monitor/pose` |

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
# However if you would like to continue using this please use the equivalent in example_msgs.

float64 data
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

Note that the topic name and the message type are identical on both sides. They have to be. Matching name and type are necessary — compatible QoS is the third condition (section 10's box) — and section 10 is what happens when one of them is off by a character.

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

**Endpoints are owned objects with lifetimes.** `rclcpp::Publisher<T>::SharedPtr publisher_` is a member because it must outlive the constructor. Let a publisher, subscription or timer go out of scope in C++ and the endpoint is destroyed — the node keeps running, quietly, with nothing attached. Python is different: the rclpy node keeps its own reference to every endpoint, so dropping yours does not destroy it, and the tutorial's odd-looking `self.subscription  # prevent unused variable warning` line only silences a linter. C++ has no such safety net.

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

`rosidl_generate_interfaces` is the whole point of the package: it runs the code generators that turn one `.msg` file into a C++ header, a Python module, and the type support the middleware needs (generated per-type code that tells the middleware how to serialise and deserialise that message). `DEPENDENCIES` lists the packages whose types you referenced — `std_msgs` here, for `Header`. Its first argument must start with the package name, so use `${PROJECT_NAME}`.

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
- **Using a type in the package that defines it needs extra CMake.** Cross-package, `find_package(turtle_watch_interfaces REQUIRED)` is enough. Same-package, you must additionally call `rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)` and `target_link_libraries` your executable against it. The reason: `find_package` locates packages that are already installed, and a package is not installed while it is still being built, so the executable must link the generated target by name. The plumbing is telling you which arrangement is the normal one.

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

`ros2 topic echo /turtle1/speed` does not hang here — with the publisher moved into `/watch` the topic has no endpoints at all, so echo prints `WARNING: topic [/turtle1/speed] does not appear to be published yet` and then fails with "Could not determine the type for the passed topic". That is the *lucky* version. The silent one is a name that still exists because something else publishes it, where echo sits there printing nothing. A type mismatch on a live name is not silent for echo: it refuses with "contains more than one type", and `ros2 topic list -t` shows both types on that one name. Diagnose both in this order.

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
# excerpt — /parameter_events, /rosout, /turtle1/cmd_vel and /turtle1/color_sensor are also listed
/turtle1/pose [turtlesim/msg/Pose]
/watch/turtle1/speed [turtle_watch_interfaces/msg/SpeedReport]
```

Two similar names where you expected one is the name mismatch, and it is usually visible right here — a namespace prefix, a typo, a missing or extra leading slash. If instead you see exactly the one name you expected, the name is fine and the type is the suspect.

**3. Who is attached to that name, and with what type?**

```bash
ros2 topic info /turtle1/speed --verbose
```

`--verbose` prints, for every endpoint, the node name and namespace, the `Endpoint type` (`PUBLISHER` or `SUBSCRIPTION`), the `Topic type`, the `Topic type hash`, and the full QoS profile. Three readings:

- `Unknown topic '/turtle1/speed'` — nothing at all is on this name, which is what the reproduction above gives. Look for the similar name from step 2.
- One side's count is 0 — publisher count 0 when you query the subscriber's intended name, or subscription count 0 when you query the publisher's. Name mismatch.
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

### Self-check

1. Your publisher and your subscriber both start, both log normally, and no data moves. Name
   the three causes and the one command that distinguishes them.
2. Why is a custom message defined in its own package rather than in the node that publishes it?
3. Your republisher subscribes at 60 Hz and publishes from the subscription callback. A
   colleague changes it to publish from a 10 Hz timer. What changed, and when would each be right?
4. What does the C++ version make explicit that the Python version hides?
5. P6's controller estimates speed by differencing encoder positions one control period apart.
   What is the resolution of that estimate at $200\,\mathrm{Hz}$, what at $50\,\mathrm{Hz}$, and
   what does it say about publishing a bare `float64 velocity`?

> [!tip]- Answers
> 1. Topic-name mismatch, message-type mismatch, QoS incompatibility. `ros2 topic info <name> --verbose` shows all three: `Unknown topic`, or a zero count on one side, means the name is wrong, differing `Topic type` or type hash between the publisher and subscriber blocks means the type is wrong, and the QoS profile block is where the third lives. Start from `ros2 node list` and `ros2 topic list -t` to narrow it, and use `ros2 node info` for the authoritative per-node answer.
> 2. Because every consumer of the topic must depend on the type. Putting it in the node's package forces anyone who wants to read the topic to build the node and its whole dependency tree, makes mutual dependencies between two nodes circular, and widens the rebuild radius. Interfaces can also only be defined in `ament_cmake` packages, and using a type inside the package that defines it needs extra `rosidl_get_typesupport_target` plumbing that cross-package use does not.
> 3. Callback-driven gives exactly one output per input, so the output rate is the input rate and you do not control it. Timer-driven gives a fixed output rate, dropping inputs when they arrive faster and republishing stale data when they arrive slower. Callback-driven is right when every input must be seen and downstream can keep up; timer-driven is right when a fast source feeds a slower fixed-rate consumer, or when the output rate is part of the contract.
> 4. The message type is a compile-time template parameter, so an in-process type error is a build failure. Endpoints are explicitly owned `SharedPtr` members that die if you let them go out of scope. The callback signature states how the message is passed and whether it is modifiable, which is what makes zero-copy intra-process delivery expressible. And the clock is named: `create_wall_timer` is the wall clock, while rclpy's `create_timer` silently defaults to the node's clock, which follows simulated time.
> 5. One count is $1/2048=0.488\,\mathrm{mm}$, so differencing over one period gives $\Delta v=\Delta p/T$: $0.00048828125/0.005=0.0977\,\mathrm{m/s}$ at $200\,\mathrm{Hz}$ and $0.00048828125/0.020=0.0244\,\mathrm{m/s}$ at $50\,\mathrm{Hz}$. The faster the loop, the coarser the velocity — one count of jitter reads as almost $10\,\mathrm{cm/s}$ at the control rate. A bare `float64 velocity` hides all of this: no stamp, no units, no statement of the window it was differenced over, and no raw `counts` beside it for a consumer to re-derive from. Publish the counts and the position with a `Header`, and say in the `.msg` comments how anything derived was computed.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]]. Vision publishes `/goal` at $50\,\mathrm{Hz}$; the controller must command the motor at $200\,\mathrm{Hz}$. No new simulator.

1. **Draw.** Two nodes, topic `/goal`, encoder counts in, motor command out. Mark the $50\,\mathrm{Hz}$ subscription and the $200\,\mathrm{Hz}$ timer. Five-line timeline: vision message, three controller ticks with no new vision, next vision.
2. **Derive.** (a) If the controller publishes from the *vision callback*, what is the motor rate? (b) Encoder $\Delta p$ for one count. (c) Silent case: vision publishes `/cart/goal`, controller subscribes `/goal`. Both nodes log "ok". Which three causes look like this, and which command splits them?
3. **Interpret.** Why is the timer-driven controller the right contract for P6, and when would callback-driven be right instead?

> [!tip]- Solutions
> 1. `camera` → `/goal` → `controller`; controller also reads $2048$ counts/m and publishes `cmd` from a $5\,\mathrm{ms}$ timer. Timeline: vision at $0,20\,\mathrm{ms}$; ticks at $0,5,10,15,20$.
> 2. (a) $50\,\mathrm{Hz}$ — the motor inherits the camera. (b) $0.488\,\mathrm{mm}$. (c) Name mismatch, type mismatch, QoS. `ros2 topic info /goal --verbose` (then `ros2 node info`).
> 3. The $200\,\mathrm{Hz}$ rate is the contract; vision is a slower input that may miss ticks. Callback-driven is right when every frame must be seen and the downstream can keep up — not when a motor loop has its own period.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 두 클라이언트 라이브러리 모두에서 자기 pub–sub 노드를 쓰고 빌드하고 디버깅할 정도. 전달 보장이나 프로세스 내 zero-copy를 따질 정도는 아니다.
> **Working** — enough to write, build and debug your own pub–sub nodes in both client libraries, not to reason about delivery guarantees.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], 즉 source 가능한 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 설치와 그 9절의 그래프 읽기 명령들. Python과, 클래스를 읽을 정도의 C++. 아래 모든 명령은 source된 터미널을 전제한다.
> ROS 2 Jazzy on Ubuntu 24.04, the graph-reading commands from 25.1, Python, and enough C++ to read a class.

*이 페이지보다 먼저가 아니라 뒤에 오는 페이지: 자기 패키지를 빌드하는 법은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]에서 제대로 가르치고, 그 페이지가 이 페이지를 전제한다. 여기서는 최소한만 쓰고, 단계마다 어느 줄이 중요한지 짚는다.*

### 과제가 그릴 그림: P6 노드 둘, 모든 이름을 풀어서 · Homework diagram

대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**. 직선 위의 카트, 엔코더 $N=2048$ counts/m, 목표를 $50\,\mathrm{Hz}$로 내는 비전, 모터를 $200\,\mathrm{Hz}$로 명령하는 제어기, 종단 예산 $70\,\mathrm{ms}$. 두 노드는 네임스페이스 `/cart`로 띄운다. 패널 셋을 그려라. 과제는 네임스페이스만 바꾼 같은 그림 셋을 요구한다.

<svg viewBox="0 0 560 378" style="max-width:100%;height:auto" role="img" aria-label="왼쪽: /cart로 띄운 camera와 controller 노드, 코드 이름과 풀린 이름, /cart/goal로 풀리는 토픽 goal, 그리고 controller에 붙은 /goal 토막. 오른쪽: controller 안에서 50 Hz on_goal은 목표를 저장하고, 5 ms 타이머의 on_tick은 저장소와 엔코더를 읽어 cmd를 낸다. 아래: 0과 20 ms의 목표, 5 ms마다의 틱, 목표 하나를 재사용하는 틱 셋, 엔코더 읽기, 축척용 70 ms 예산.">
  <defs><marker id="n2kopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="n2ksol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">이름: 코드에 쓴 것과 풀린 것</text>
  <ellipse cx="54" cy="84" rx="36" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="54" y="88" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">비전</text>
  <text x="54" y="116" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">camera</text>
  <text x="54" y="131" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/camera</text>
  <ellipse cx="222" cy="84" rx="42" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="222" y="88" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">제어</text>
  <text x="222" y="116" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">controller</text>
  <text x="222" y="131" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/controller</text>
  <line x1="90" y1="84" x2="178" y2="84" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2kopen)"/>
  <text x="135" y="78" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <text x="135" y="99" font-size="11" text-anchor="middle" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">/cart/goal</text>
  <line x1="276" y1="44" x2="241.7" y2="69" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2kopen)"/>
  <text x="270" y="40" font-size="11" text-anchor="end" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <text x="12" y="166" font-size="11" fill-opacity="0.6" fill="currentColor">위: 코드에 쓴 문자열</text>
  <text x="12" y="180" font-size="11" fill-opacity="0.6" fill="currentColor">아래: /cart에서 풀린 이름</text>
  <text x="12" y="196" font-size="11" fill-opacity="0.6" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan>: 두 번째 이름, 퍼블리셔 없음 (10절)</text>
  <text x="300" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">controller 안: 콜백 둘</text>
  <ellipse cx="438" cy="108" rx="112" ry="76" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <text x="438" y="52" font-size="11" text-anchor="middle" fill-opacity="0.6" font-family="ui-monospace,monospace" fill="currentColor">/cart/controller</text>
  <rect x="352" y="66" width="74" height="22" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <text x="389" y="81" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">on_goal</text>
  <rect x="446" y="66" width="70" height="22" rx="3" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none"/>
  <text x="481" y="81" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">목표 저장</text>
  <line x1="426" y1="77" x2="444" y2="77" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" fill="none" marker-end="url(#n2ksol)"/>
  <line x1="292" y1="77" x2="350" y2="77" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2kopen)"/>
  <text x="292" y="70" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <text x="292" y="96" font-size="11" fill-opacity="0.9" fill="currentColor">50 Hz</text>
  <rect x="352" y="122" width="90" height="22" rx="3" stroke="currentColor" stroke-width="1.5" stroke-opacity="0.9" fill="none"/>
  <circle cx="363" cy="133" r="6.5" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <line x1="363" y1="133" x2="363" y2="129" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <line x1="363" y1="133" x2="366.5" y2="133" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85" fill="none"/>
  <text x="374" y="137" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">on_tick</text>
  <text x="356" y="115" font-size="11" fill-opacity="0.9" fill="currentColor">200 Hz, 5 ms</text>
  <line x1="470" y1="88" x2="438" y2="121" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" fill="none" marker-end="url(#n2ksol)"/>
  <text x="476" y="110" font-size="11" fill-opacity="0.75" font-style="italic" fill="currentColor">읽음</text>
  <line x1="382" y1="198" x2="382" y2="145" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="2 3" fill="none" marker-end="url(#n2ksol)"/>
  <text x="388" y="197" font-size="11" fill-opacity="0.8" fill="currentColor">엔코더 (그래프 바깥)</text>
  <line x1="442" y1="133" x2="552" y2="133" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#n2kopen)"/>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">cmd</text>
  <text x="12" y="222" font-size="12" fill-opacity="0.8" fill="currentColor">시계 다섯 줄 (ms)</text>
  <text x="100" y="244" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">목표 50 Hz</text>
  <text x="100" y="266" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">틱 200 Hz</text>
  <text x="100" y="288" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">재사용</text>
  <text x="100" y="308" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">엔코더 읽기</text>
  <text x="100" y="330" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">예산</text>
  <line x1="108" y1="240" x2="228" y2="240" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <circle cx="108" cy="240" r="4.2" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="228" cy="240" r="4.2" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <line x1="108" y1="262" x2="228" y2="262" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <path d="M108.0 256v12M138.0 256v12M168.0 256v12M198.0 256v12M228.0 256v12" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" fill="none"/>
  <path d="M138.0 277V284H198.0V277" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none"/>
  <text x="208" y="288" font-size="11" fill-opacity="0.85" fill="currentColor">틱 5, 10, 15는 0의 목표를 재사용</text>
  <rect x="104.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="134.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="164.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="194.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <rect x="224.5" y="300.5" width="7" height="7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none"/>
  <line x1="108" y1="326" x2="528" y2="326" stroke="currentColor" stroke-width="2.4" stroke-opacity="0.8" fill="none"/>
  <line x1="108" y1="320" x2="108" y2="332" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <line x1="528" y1="320" x2="528" y2="332" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8" fill="none"/>
  <text x="318" y="319" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">70 ms 예산, 축척용</text>
  <line x1="108" y1="344" x2="528" y2="344" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="108" y1="344" x2="108" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="138" y1="344" x2="138" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="168" y1="344" x2="168" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="198" y1="344" x2="198" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="228" y1="344" x2="228" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="258" y1="344" x2="258" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="288" y1="344" x2="288" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="318" y1="344" x2="318" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="348" y1="344" x2="348" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="378" y1="344" x2="378" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="408" y1="344" x2="408" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="438" y1="344" x2="438" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="468" y1="344" x2="468" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="498" y1="344" x2="498" y2="348" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="528" y1="344" x2="528" y2="350" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <text x="108" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="138" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">5</text>
  <text x="168" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">10</text>
  <text x="198" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">15</text>
  <text x="228" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">20</text>
  <text x="288" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">30</text>
  <text x="348" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">40</text>
  <text x="408" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">50</text>
  <text x="468" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="528" y="362" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">70</text>
  <path d="M108.0 270V344M138.0 270V344M168.0 270V344M198.0 270V344M228.0 270V344" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.25" stroke-dasharray="1 3" fill="none"/>
</svg>

**왼쪽 — 노드 둘, 각각 이름 두 개를 달아서**. 타원 둘. 각 타원 아래에 두 줄을 쓴다. 코드가 `super().__init__`에 넘기는 이름(`camera`, `controller`), 그리고 launch 네임스페이스를 거친 완전 이름(`/cart/camera`, `/cart/controller`). 둘 사이에 토픽 화살표 하나를 긋고 같은 방식으로 두 번 적는다. 화살표 위에는 코드에 쓰인 문자열(`goal`), 아래에는 3절의 표가 그것을 푸는 결과(`/cart/goal`). 그다음 제어기에서 나가는 *두 번째* 화살표 토막을 `/goal`이라고 적고 반대편은 비워 둔다. 10절의 버그이고, 그것을 그리는 이유는 그것이 끊어진 화살표가 아니라 두 번째 *이름*이기 때문이다. 그림 어디에도 빨간 표시는 없다.

**오른쪽 — 제어기 안의 콜백 둘**. 노드 타원 안에 상자 둘. `on_goal`은 메시지가 도착할 때 불리므로 구독 화살표가 그 상자로 들어가고 $50\,\mathrm{Hz}$라고 적는다. 하는 일은 목표를 저장하는 것뿐이니 옆에 작은 저장 상자를 그린다. `on_tick`은 $5\,\mathrm{ms}$ 타이머로 불리므로 시계 기호를 달고 $200\,\mathrm{Hz}$라고 적는다. 저장 상자와 엔코더를 *둘 다* 읽고, `cmd` 화살표는 `on_tick`에서 노드 밖으로 나간다. 엔코더는 그래프 바깥에서 `on_tick`으로 들어가는 화살표다. `cmd`가 `on_goal`에서 나가는 순간 그림은 틀린 것이고, 9절이 그 실수를 일부러 해 보는 자리다.

**아래 — 시계 다섯 줄**. 1줄: 목표가 $0$과 $20\,\mathrm{ms}$. 2줄: 틱이 $0,5,10,15,20\,\mathrm{ms}$. 3줄: 틱 $5$, $10$, $15$ 아래에 괄호를 치고 $0$의 목표를 재사용하는 틱이라고 표시. 4줄: 틱마다 엔코더 읽기. 5줄: 축척을 위한 $70\,\mathrm{ms}$ 예산선.

### 대상으로 한 번 끝까지: 엔코더 한 카운트가 메시지를 지나 속도가 되기까지 · Worked case

숫자 여섯 개, 전부 P6의 상수 둘과 주기 둘에서 나온다.

**1단계 — 카운트에서 미터로**. 엔코더는 계수기이고 그래프는 미터를 날라야 한다. $N=2048$ counts/m이면 변환과 그 해상도는

$$p=\frac{c}{N}=\frac{c}{2048}\,\mathrm{m},\qquad \Delta p=\frac{1}{2048}=4.8828125\times10^{-4}\,\mathrm{m}=0.488\,\mathrm{mm}$$

한 카운트가 $c$의 최소 단위이기 때문이다. 즉 이 엔코더는 $0.5\,\mathrm{mm}$보다 가까운 두 위치를 영원히 구분하지 못한다. $c=1024$면 카트는 정확히 $0.5\,\mathrm{m}$에 있다.

**2단계 — 그것을 나르는 메시지**. `std_msgs/msg/Float64`의 값은 4절이 말했다. 위 영문 `.msg` 블록이 이 카트에 어울리는 타입이고, 자기 인터페이스 패키지에 들어간다. `Header`, 원시 카운트 `int32 counts`, 파생된 미터 `float64 position` 세 줄이다. 원시 카운트를 파생값 옆에 함께 싣는 이유는 대단히 실무적이다. `counts`는 정확하고 `position`은 그렇지 않으므로, 축척 계수를 의심하는 하위 노드가 직접 검산할 수 있고, 오늘 녹화한 bag이 내일의 재보정에서도 살아남는다. `Header`의 스탬프가 $70\,\mathrm{ms}$ 예산을 재는 기준이다.

**3단계 — 한 카운트는 속도로 얼마인가**. 속도가 필요한 제어기는 보통 한 주기 떨어진 위치 둘을 뺀다. 그 추정값의 해상도는 위치의 해상도를 주기로 나눈 것이다.

$$\Delta v=\frac{\Delta p}{T}=\frac{1/2048}{T}\quad\Longrightarrow\quad \Delta v\big|_{200\,\mathrm{Hz}}=\frac{0.00048828125}{0.005}=0.0977\,\mathrm{m/s},\qquad \Delta v\big|_{50\,\mathrm{Hz}}=\frac{0.00048828125}{0.020}=0.0244\,\mathrm{m/s}$$

고정된 양자를 더 짧은 간격으로 나누면 그만큼 커지기 때문이다. 첫 숫자를 다시 읽어라. 제어 주기에서 **한 카운트의 떨림은 겉보기 속도로 $9.8\,\mathrm{cm/s}$에 해당한다**. $2\,\mathrm{cm/s}$로 기어가는 카트가 $0$과 $9.8\,\mathrm{cm/s}$를 오가는 속도 신호를 만들고, 메시지 타입을 아무리 잘 짜도 고쳐지지 않는다. 빠른 루프가 더 긴 창으로 차분하거나, 필터를 걸거나, 단순 차분이 아닌 곳에서 속도를 읽는 이유가 이것이다. 그리고 스탬프도 없고 계산 방식도 밝히지 않은 맨 `float64 velocity`가 4절의 선택지 중 최악인 이유이기도 하다.

**4단계 — 무엇이 얼마나 자주 일어나는가**. $T_{\text{vision}}/T_{\text{ctrl}}=20/5=4$로 정확히 나누어떨어지므로 목표 하나를 네 틱이 소비하고, $70\,\mathrm{ms}$ 예산 창 하나에는 틱 $14$개와 온전한 비전 주기 $3$개가 들어간다. 이제 9절의 설계 선택을 P6 숫자로 본다. `cmd`를 `on_goal`에서 내면 모터 명령은 $50\,\mathrm{Hz}$가 된다. 콜백 구동 퍼블리셔는 입력의 주기를 물려받기 때문이다. $5\,\mathrm{ms}$ 타이머에서 내면 카메라가 무엇을 하든 손에 쥔 가장 새 목표로 $200\,\mathrm{Hz}$로 명령한다. P6이 명시한 계약은 두 번째이고, 그래서 제어기가 타이머 구동이며 콜백 둘 사이에 저장소가 존재한다.

**5단계 — 그리고 이 모든 것을 조용히 무너뜨리는 이름**. 두 노드 모두 `/cart`로 띄웠다. 3절의 세 형태는 이렇게 풀린다.

| 제어기 코드에 쓴 것 | 풀린 이름 | P6에 미치는 결과 |
|---|---|---|
| `goal` (상대) | `/cart/goal` | 카메라의 상대 `goal`과 일치. 데이터가 흐른다 |
| `/goal` (절대) | `/goal` | 네임스페이스 무시. 이름 둘, 연결 없음, 오류도 없음 |
| `~/gain` (비공개) | `/cart/controller/gain` | 노드별 설정. 두 번 띄워도 안전 |

1행과 2행의 차이는 문자 하나인데 대가는 조용한 로봇이다. `ros2 node list`에는 노드 둘이 다 보이고, `ros2 topic list -t`에는 하나를 기대한 자리에 이름이 *둘* 보이며, 모터는 마지막 명령을 영원히 붙들고 있다. 10절이 그것을 찾는 명령 넷이고, 이 사례가 바로 그 명령들이 찾아내는 사례다.

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

"논리적으로 한 가지"는 "파일 하나"도 "클래스 하나"도 아니다. 쓸 만한 판별법은 재시작 테스트다. A를 B와 무관하게 재시작·교체·재튜닝·재배포하고 싶은 순간이 조금이라도 있다면 A와 B는 다른 노드다. 카메라 드라이버와 검출기는 이 테스트에 정반대 방향에서 걸린다. 검출기는 매주 갈아 끼우고 드라이버는 건드리지 않을 테니 둘은 두 노드다. 검출기와 그 안의 non-maximum suppression 단계(한 물체 주위에 겹쳐 나온 중복 박스를 지우는 후처리)는 항상 함께 살고 함께 죽으니 하나다.

초심자용 그림에 붙일 보정 둘.

- 노드는 정확히 프로세스가 아니다. 한 프로세스가 여러 노드를 담을 수 있고, ROS 2는 이것을 composition이라 부른다. 실제 스택이 같은 머신에 있는 노드들 사이의 직렬화(메시지를 바이트로 바꿨다가 되돌리는 것) 비용을 피하는 방법이 이것이다. 한 프로세스의 메모리를 공유하는 노드들은 intra-process 통신을 켜면 메시지를 직접 넘겨줄 수 있다. Composition은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]에 있다.
- 노드 이름은 실행 파일 이름이 아니다. 25.1에서 봤다. `turtlesim_node`는 스스로를 `/turtlesim`이라 부르고, `--ros-args --remap __node:=my_turtle`은 코드를 건드리지 않고 실행 시점에 이름을 바꾼다.

### 3. 토픽, 그리고 익명성이라는 핵심

토픽은 이름이다. 퍼블리셔 몇이든 구독자 몇이든 거기 붙을 수 있고, 어느 퍼블리셔가 publish하면 시스템 안의 모든 구독자가 그 데이터를 받는다.

문서가 이 관계를 부르는 말은 **익명(anonymous)** 이다. 구독자가 데이터를 받을 때 그것을 누가 보냈는지 대체로 모르고 신경 쓰지 않는다는 뜻이다. 빠진 기능이 아니다. 교체를 가능하게 하는 바로 그 성질이다. 구독자는 생산자에 대한 손잡이를 쥐고 있지 않으므로, 생산자가 바뀔 때 구독자에서 고칠 것이 없다.

다른 성질은 **강한 타입(strongly typed)** 이고 절반이 둘이다. 기계적인 절반은 각 필드에 선언된 타입이 있고 모든 언어의 생성 코드가 그것을 강제한다는 것이다. 의미론적인 절반은 강제 장치가 전혀 없다. 핵심 메시지 타입들은 합의된 의미를 지닌다. IMU(관성 측정 장치, 가속도계와 자이로스코프를 묶은 센서)의 각속도는 라디안 매 초이고 다른 것이 그 필드에 들어가서는 안 된다. 하지만 당신이 각도(degree)를 publish하는 것을 아무도 막지 않는다. 타입 검사기는 도와줄 수 없고, 관례만이 유일한 버팀목이다.

이름 규칙은 지금 몸에 익혀 두라. 10절의 버그가 여기 산다.

| 형태 | 예 | 해석 결과 |
|---|---|---|
| 절대 | `/turtle1/pose` | `/turtle1/pose`. 노드 네임스페이스를 무시한다 |
| 상대 | `turtle1/pose` | 네임스페이스 + 이름. 네임스페이스가 `/watch`면 `/watch/turtle1/pose` |
| 비공개 | `~/pose` | 노드 네임스페이스 + 노드 이름 + `/pose`. 네임스페이스 `/watch`의 노드 `monitor`라면 `/watch/monitor/pose` |

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
# However if you would like to continue using this please use the equivalent in example_msgs.

float64 data
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

양쪽의 토픽 이름과 메시지 타입이 똑같다는 점을 보라. 그래야만 한다. 이름과 타입의 일치는 필요조건이고 — 호환되는 QoS가 세 번째 조건이다(10절의 상자) — 한 글자가 어긋났을 때 무슨 일이 나는지가 10절이다.

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

**엔드포인트는 수명을 가진 소유 객체다.** `rclcpp::Publisher<T>::SharedPtr publisher_`가 멤버인 이유는 생성자보다 오래 살아야 하기 때문이다. C++에서 퍼블리셔나 구독, 타이머를 스코프 밖으로 흘려보내면 엔드포인트가 파괴된다. 노드는 계속 돌아가고, 조용하고, 아무것도 붙어 있지 않다. Python은 다르다. rclpy 노드가 모든 엔드포인트의 참조를 스스로 쥐고 있어 내 참조를 버려도 파괴되지 않고, 튜토리얼의 어색한 `self.subscription  # prevent unused variable warning` 줄은 린터 경고를 끌 뿐이다. C++에는 그런 안전망이 없다.

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

`rosidl_generate_interfaces`가 이 패키지의 존재 이유다. 코드 생성기를 돌려 `.msg` 파일 하나를 C++ 헤더와 Python 모듈, 그리고 미들웨어가 필요로 하는 type support(그 메시지를 어떻게 직렬화·역직렬화할지 미들웨어에 알려 주는 타입별 생성 코드)로 바꾼다. `DEPENDENCIES`에는 참조한 타입이 있는 패키지를 적는다. 여기서는 `Header` 때문에 `std_msgs`다. 첫 인자는 패키지 이름으로 시작해야 하므로 `${PROJECT_NAME}`을 쓴다.

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
- **정의한 패키지 안에서 타입을 쓰려면 CMake가 더 필요하다.** 패키지가 다르면 `find_package(turtle_watch_interfaces REQUIRED)`로 끝난다. 같은 패키지라면 추가로 `rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} rosidl_typesupport_cpp)`를 부르고 실행 파일을 거기에 `target_link_libraries` 해야 한다. 이유는 `find_package`가 이미 설치된 패키지를 찾는 명령인데 패키지는 빌드 도중에는 아직 설치되지 않았으므로, 실행 파일이 생성된 타깃을 이름으로 직접 링크해야 하기 때문이다. 배관 자체가 어느 쪽이 정상 배치인지 말해 주고 있다.

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

`ros2 topic echo /turtle1/speed`는 여기서 매달리지 않는다. 퍼블리셔가 `/watch` 안으로 들어가 버려 이 토픽에는 엔드포인트가 하나도 없고, 그래서 echo는 `WARNING: topic [/turtle1/speed] does not appear to be published yet`을 찍은 뒤 "Could not determine the type for the passed topic"으로 실패한다. 이건 *운이 좋은* 쪽이다. 조용한 쪽은 다른 무언가가 발행하고 있어 이름은 살아 있는 경우이고, 그때 echo는 아무것도 찍지 않고 앉아 있는다. 살아 있는 이름에서 타입이 어긋나면 echo에게는 조용하지 않다. "contains more than one type"으로 거부하고, `ros2 topic list -t`는 그 한 이름에 타입 둘을 보여 준다. 둘 다 이 순서로 진단한다.

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
# excerpt — /parameter_events, /rosout, /turtle1/cmd_vel and /turtle1/color_sensor are also listed
/turtle1/pose [turtlesim/msg/Pose]
/watch/turtle1/speed [turtle_watch_interfaces/msg/SpeedReport]
```

하나를 기대했는데 비슷한 이름 둘이 보이면 이름 불일치이고, 보통 바로 여기서 드러난다. 네임스페이스 접두사, 오타, 앞 슬래시가 빠졌거나 더 붙었거나. 반대로 기대한 이름 하나만 정확히 보인다면 이름은 멀쩡하고 타입이 용의자다.

**3. 그 이름에 누가 붙어 있고, 타입은 무엇인가?**

```bash
ros2 topic info /turtle1/speed --verbose
```

`--verbose`는 엔드포인트마다 노드 이름과 네임스페이스, `Endpoint type`(`PUBLISHER` 또는 `SUBSCRIPTION`), `Topic type`, `Topic type hash`, 그리고 전체 QoS 프로파일을 찍는다. 읽는 법 셋.

- `Unknown topic '/turtle1/speed'` — 이 이름에는 아무것도 없다. 위의 재현이 주는 결과이고, 2단계에서 본 비슷한 이름을 찾아라.
- 한쪽 수가 0 — 서브스크라이버가 의도한 이름을 조회하면 퍼블리셔 수가 0, 퍼블리셔의 이름을 조회하면 구독 수가 0. 이름 불일치.
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

### 스스로 점검

1. 퍼블리셔와 서브스크라이버가 둘 다 뜨고 둘 다 정상 로그를 찍는데 데이터가 안 움직인다.
   원인 셋과 그것을 구분하는 명령 하나를 대라.
2. 커스텀 메시지를 publish하는 노드 안이 아니라 별도 패키지에 정의하는 이유는?
3. republisher가 60 Hz로 subscribe하고 구독 콜백에서 publish한다. 동료가 10 Hz 타이머에서
   publish하도록 바꿨다. 무엇이 바뀌었고 각각 언제 옳은가?
4. C++ 판본이 Python 판본이 감추는 무엇을 드러내는가?
5. P6 제어기가 제어 주기 하나만큼 떨어진 엔코더 위치를 빼서 속도를 추정한다. $200\,\mathrm{Hz}$
   에서 그 추정의 해상도는 얼마이고 $50\,\mathrm{Hz}$에서는 얼마이며, 맨
   `float64 velocity`를 publish하는 것에 대해 무엇을 말해 주는가?

> [!tip]- 정답 · Answers
> 1. 토픽 이름 불일치, 메시지 타입 불일치, QoS 비호환. `ros2 topic info <이름> --verbose`가 셋 다 보여 준다. `Unknown topic`이거나 한쪽 수가 0이면 이름이 틀린 것이고, 퍼블리셔 블록과 서브스크라이버 블록의 `Topic type`이나 타입 해시가 다르면 타입이 틀린 것이며, QoS 프로파일 블록에 세 번째가 산다. 범위를 좁히는 데는 `ros2 node list`와 `ros2 topic list -t`부터 시작하고, 노드별 최종 판정에는 `ros2 node info`를 쓴다.
> 2. 토픽의 모든 소비자가 그 타입에 의존해야 하기 때문이다. 노드 패키지에 넣으면 토픽을 읽고 싶을 뿐인 사람도 그 노드와 의존성 트리 전체를 빌드해야 하고, 두 노드가 서로의 타입을 쓰면 의존이 순환하며, 재빌드 파급 범위가 넓어진다. 인터페이스는 `ament_cmake` 패키지에서만 정의할 수 있고, 정의한 패키지 안에서 그 타입을 쓰려면 패키지 간 사용에는 필요 없는 `rosidl_get_typesupport_target` 배관이 추가로 필요하다.
> 3. 콜백 구동은 입력 하나당 출력 하나이므로 출력 주기가 입력 주기이고 제어할 수 없다. 타이머 구동은 출력 주기가 고정이며, 입력이 더 빨리 오면 버리고 더 늦게 오면 낡은 데이터를 다시 낸다. 모든 입력을 봐야 하고 하류가 따라올 수 있으면 콜백 구동이 맞다. 빠른 소스가 느린 고정 주기 소비자에 들어가거나 출력 주기가 계약의 일부라면 타이머 구동이 맞다.
> 4. 메시지 타입이 컴파일 시점 템플릿 인자라서 프로세스 내 타입 오류가 빌드 실패가 된다. 엔드포인트가 명시적으로 소유되는 `SharedPtr` 멤버라서 스코프 밖으로 흘리면 죽는다. 콜백 시그니처가 메시지를 어떻게 넘기고 수정 가능한지를 말하고, 그것이 프로세스 내 zero-copy 전달을 표현 가능하게 만든다. 그리고 시계에 이름이 붙어 있다. `create_wall_timer`는 벽시계이고, rclpy의 `create_timer`는 말없이 노드의 시계를 기본값으로 쓰며 그것은 시뮬레이션 시간을 따라간다.
> 5. 한 카운트는 $1/2048=0.488\,\mathrm{mm}$이므로 한 주기 차분의 해상도는 $\Delta v=\Delta p/T$다. $200\,\mathrm{Hz}$에서 $0.00048828125/0.005=0.0977\,\mathrm{m/s}$, $50\,\mathrm{Hz}$에서 $0.00048828125/0.020=0.0244\,\mathrm{m/s}$. 루프가 빠를수록 속도는 거칠어진다 — 제어 주기에서는 한 카운트의 떨림이 거의 $10\,\mathrm{cm/s}$로 읽힌다. 맨 `float64 velocity`는 이 전부를 감춘다. 스탬프도, 단위도, 어떤 창으로 차분했는지도, 소비자가 다시 유도할 원시 `counts`도 없다. `Header`와 함께 카운트와 위치를 싣고, 파생값을 어떻게 계산했는지는 `.msg` 주석에 적어라.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**. 비전이 `/goal`을 $50\,\mathrm{Hz}$로 발행하고, 제어기는 모터를 $200\,\mathrm{Hz}$로 명령해야 한다. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** 노드 둘, 토픽 `/goal`, 엔코더 카운트 입력, 모터 명령 출력. $50\,\mathrm{Hz}$ 구독과 $200\,\mathrm{Hz}$ 타이머. 다섯 줄 타임라인: 비전 메시지, 새 비전 없이 제어 틱 셋, 다음 비전.
2. **유도.** (a) 제어기가 *비전 콜백*에서 publish하면 모터 주기는? (b) 엔코더 한 카운트의 $\Delta p$. (c) 조용한 고장: 비전은 `/cart/goal`, 제어기는 `/goal`을 구독. 두 노드 모두 "ok". 이렇게 보이는 원인 셋과, 가르는 명령은?
3. **해석.** P6에서 타이머 구동 제어기가 옳은 계약인 이유, 그리고 콜백 구동이 오히려 옳을 때는?

> [!tip]- 정답 · Solutions
> 1. `camera` → `/goal` → `controller`; 제어기는 $2048$ counts/m를 읽고 $5\,\mathrm{ms}$ 타이머에서 `cmd`를 낸다. 타임라인: 비전 $0,20\,\mathrm{ms}$; 틱 $0,5,10,15,20$.
> 2. (a) $50\,\mathrm{Hz}$ — 모터가 카메라를 상속. (b) $0.488\,\mathrm{mm}$. (c) 이름, 타입, QoS. `ros2 topic info /goal --verbose`(그다음 `ros2 node info`).
> 3. $200\,\mathrm{Hz}$가 계약이고 비전은 틱을 놓칠 수 있는 느린 입력이다. 모든 프레임을 봐야 하고 하류가 따라오면 콜백 구동이 맞다 — 모터 루프가 자기 주기를 가질 때는 아니다.
