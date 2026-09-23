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
> A working Ubuntu 24.04 machine (or VM), comfort with a shell, and Python; for the picture and the Worked case, **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] (its two rates and its $70\,\mathrm{ms}$ budget). No prior ROS of any version is assumed. Everything that runs here is the baseline for the rest of this track: **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, paired with Gazebo Harmonic when simulation arrives in [[04-robotics/ros2/index|25. ROS 2]].
> Ubuntu 24.04 머신(또는 VM), 셸 사용 경험, Python. 그림과 계산 절에는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**(두 주기와 $70\,\mathrm{ms}$ 예산). ROS 경험은 전제하지 않는다. 이 트랙 전체의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**이고, 시뮬레이션이 등장할 때는 Gazebo Harmonic과 짝을 이룬다.

> [!note] First pass · 처음이라면
> Two routes, one page. If you have never typed a ROS 2 command, sit at a keyboard for §6–§10 first — install, source, run turtlesim, read its graph — and then come back to the picture and the Worked case, which are arithmetic on P6's two rates and need nothing installed. Either way, §1–§3 are the ideas every later page uses, and §2 is where "real-time" gets its meaning. §4–§5 (why ROS 2 replaced ROS 1, and DDS underneath) and the environment table in §11 are second-pass reading: open them when somebody asks why QoS exists, or when a shell behaves impossibly.

### The picture: the P6 graph, and one budget on a clock

<svg viewBox="0 0 560 400" style="max-width:100%;height:auto" role="img" aria-label="Top: the P6 computation graph, with /camera, /controller and /logger inside one ROS domain, topics /goal at 50 Hz and /cmd at 200 Hz, and the motor and encoder outside the graph. Bottom: the five budget terms as consecutive brackets on a 0 to 80 ms clock, ending left of the 70 ms deadline.">
  <defs><marker id="w1eopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="w1esol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">Computation graph, as ros2 node list and ros2 topic list -t report it</text>
  <rect x="12" y="30" width="314" height="174" rx="10" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.55" stroke-dasharray="5 4" fill="none"/>
  <text x="20" y="46" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">export ROS_DOMAIN_ID=&lt;integer&gt;</text>
  <ellipse cx="66" cy="96" rx="44" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="66" y="100" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="250" cy="96" rx="60" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="250" y="100" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <ellipse cx="158" cy="160" rx="44" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="158" y="164" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/logger</text>
  <line x1="110" y1="96" x2="188" y2="96" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1eopen)"/>
  <text x="150" y="86" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan> <tspan font-style="italic">[type]</tspan></text>
  <text x="150" y="110" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">50 Hz</text>
  <line x1="86.4" y1="110.2" x2="136.1" y2="144.8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1eopen)"/>
  <text x="84" y="140" font-size="11" text-anchor="middle" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <line x1="228.5" y1="110.9" x2="179.9" y2="144.8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1eopen)"/>
  <text x="236" y="142" font-size="11" text-anchor="middle" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">/cmd</text>
  <rect x="404" y="70" width="144" height="40" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="476" y="87" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">motor</text>
  <text x="476" y="102" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">hardware, not a node</text>
  <line x1="309.4" y1="93.7" x2="402" y2="90" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1eopen)"/>
  <text x="366" y="82" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/cmd</tspan> <tspan font-style="italic">[type]</tspan></text>
  <text x="366" y="108" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">200 Hz</text>
  <rect x="404" y="134" width="144" height="28" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="476" y="152" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">encoder</text>
  <line x1="403" y1="148" x2="289.2" y2="109.6" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="2 3" fill="none" marker-end="url(#w1esol)"/>
  <text x="356" y="147" font-size="11" text-anchor="middle" fill-opacity="0.9" font-style="italic" fill="currentColor">read</text>
  <text x="20" y="194" font-size="11" fill-opacity="0.5" fill="currentColor"><tspan font-family="ui-monospace,monospace">/rosout  /parameter_events</tspan>  (in every graph, §9)</text>
  <text x="404" y="184" font-size="11" fill-opacity="0.6" fill="currentColor">[type]: the page leaves P6's</text>
  <text x="404" y="198" font-size="11" fill-opacity="0.6" fill="currentColor">message types open</text>
  <text x="12" y="232" font-size="12" fill-opacity="0.8" fill="currentColor">One budget on a clock, to scale (ms after camera mid-exposure)</text>
  <line x1="104" y1="316" x2="544" y2="316" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" fill="none"/>
  <path d="M104.0 316v-7M131.5 316v-7M159.0 316v-7M186.5 316v-7M214.0 316v-7M241.5 316v-7M269.0 316v-7M296.5 316v-7M324.0 316v-7M351.5 316v-7M379.0 316v-7M406.5 316v-7M434.0 316v-7M461.5 316v-7M489.0 316v-7M516.5 316v-7M544.0 316v-7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="none"/>
  <path d="M104.0 316v11M214.0 316v11M324.0 316v11M434.0 316v11" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.9" fill="none"/>
  <text x="104" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="214" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">20</text>
  <text x="324" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">40</text>
  <text x="434" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="544" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">80</text>
  <text x="96" y="315" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">control 200 Hz</text>
  <text x="96" y="327" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">vision 50 Hz</text>
  <path d="M104.8 288V282H213.2V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="159" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">cam</tspan></text>
  <path d="M214.8 288V282H240.7V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="227.8" y="262" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">net</tspan></text>
  <line x1="227.8" y1="266" x2="227.8" y2="281" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <rect x="241.5" y="282" width="27.5" height="34" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <path d="M242.3 288V282H268.2V288" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <text x="255.2" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" font-weight="bold" fill="currentColor">L<tspan font-size="9.4" dy="3">wait</tspan></text>
  <path d="M269.8 288V282H284.7V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="277.2" y="262" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">ctrl</tspan></text>
  <line x1="277.2" y1="266" x2="277.2" y2="281" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <path d="M286.3 288V282H323.2V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="304.8" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">act</tspan></text>
  <line x1="489" y1="248" x2="489" y2="328" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9" fill="none"/>
  <text x="489" y="243" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">70 ms deadline</text>
  <text x="332.2" y="245" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">cam</tspan>  <tspan dy="-3">camera pipeline</tspan></text>
  <text x="332.2" y="258" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">net</tspan>  <tspan dy="-3">transport</tspan></text>
  <text x="332.2" y="271" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">L<tspan font-size="8.6" dy="3">wait</tspan>  <tspan dy="-3">wait for the next tick</tspan></text>
  <text x="332.2" y="284" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">ctrl</tspan>  <tspan dy="-3">compute</tspan></text>
  <text x="332.2" y="297" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">act</tspan>  <tspan dy="-3">actuation</tspan></text>
  <text x="12" y="358" font-size="11" fill-opacity="0.85" fill="currentColor">t = 0 is camera mid-exposure; vision spacing 20 ms = 4 control periods.</text>
  <text x="12" y="373" font-size="11" fill-opacity="0.85" fill="currentColor">Solid: L<tspan font-size="8.6" dy="3">wait</tspan> <tspan dy="-3">&lt; T</tspan><tspan font-size="8.6" dy="3">ctrl</tspan> <tspan dy="-3">= 5 ms, the one term the two rates fix.</tspan></text>
  <text x="12" y="388" font-size="11" fill-opacity="0.85" fill="currentColor">Dashed: the four measured terms, widths illustrative; together at most 70 − 5 = 65 ms.</text>
</svg>

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] as a ROS 2 computation graph inside one `ROS_DOMAIN_ID` (an integer, 0 unless the shell exports another; only nodes with the same value discover each other, §5): `/camera` publishes `/goal` at $50\,\mathrm{Hz}$, `/controller` publishes `/cmd` at $200\,\mathrm{Hz}$ to a motor that is hardware rather than a node, `/logger` subscribes to both, and the encoder is read inside the controller instead of arriving on a topic. Below, the $70\,\mathrm{ms}$ from camera mid-exposure to applied force is drawn to scale as five consecutive terms, with vision publications every $20\,\mathrm{ms}$, four control periods apart. Only the wait for the next control tick is fixed by the two rates, at under one control period of $5\,\mathrm{ms}$, which leaves at most $65\,\mathrm{ms}$ for the four terms that must be measured.

### Worked case: where P6's 70 ms goes, and what the control rate actually buys

Periods first, because every other number on this page is one of these two divided into something:

$$T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=0.020\,\mathrm{s}=20\,\mathrm{ms},\qquad T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=0.005\,\mathrm{s}=5\,\mathrm{ms}$$

so one budget window holds $70/5=14$ whole control periods, and $70/20=3.5$ vision periods — three complete ones, the fourth ending at $80\,\mathrm{ms}$, outside the budget.

**Step 1 — write the budget as a sum, not as a number.** From mid-exposure to applied force the delay is

$$70\,\mathrm{ms}\;\ge\;L_{\text{cam}}+L_{\text{net}}+L_{\text{wait}}+L_{\text{ctrl}}+L_{\text{act}}$$

because the five stages are strictly sequential: the frame is captured and published ($L_{\text{cam}}$), crosses a process or machine boundary ($L_{\text{net}}$), waits for a controller that is not listening continuously ($L_{\text{wait}}$), becomes a command ($L_{\text{ctrl}}$), and becomes current in a motor ($L_{\text{act}}$). Four of the five are properties of your code and your hardware and have to be measured. Exactly one is fixed by P6's two rates alone, and that is the reason to write the sum down before measuring anything.

**Step 2 — the one term the graph decides.** A goal published at time $g$ is invisible until the next control tick, and ticks are one control period apart, so

$$0\le L_{\text{wait}}<T_{\text{ctrl}}=5\,\mathrm{ms}$$

since a goal can land anywhere inside a period and the worst case is landing just after a tick. No property of ROS 2, DDS (the communication layer ROS 2 sits on, §5) or the operating system moves that bound; it is arithmetic on $50$ and $200$.

**Step 3 — the allowance that leaves, and what a slower loop would cost.** $70-5=65\,\mathrm{ms}$ for the four measured terms. Run the same controller at $50\,\mathrm{Hz}$ and the bound becomes $L_{\text{wait}}<20\,\mathrm{ms}$, leaving $70-20=50\,\mathrm{ms}$. So the four-fold control rate buys $15\,\mathrm{ms}$ of the frame-to-force path, which is $15/70=21.4\%$ of the whole budget, without touching the camera, the network or the motor. That is the honest version of "we run the loop fast".

**Step 4 — and what it does not buy.** $T_{\text{vision}}/T_{\text{ctrl}}=20/5=4$ exactly, so every goal is consumed by exactly four ticks. Only the first acts on it while it is fresh; the other three re-use it, adding $5$, $10$ and $15\,\mathrm{ms}$ of extra age — mean $7.5\,\mathrm{ms}$ over the four ticks, or $10.7\%$ of the budget, worst case $15\,\mathrm{ms}$, or $21.4\%$. Add the two effects and the total is bounded whatever you do to the loop:

$$L_{\text{wait}}+L_{\text{reuse}}<T_{\text{vision}}=20\,\mathrm{ms}$$

because the freshest goal in hand at any tick was published less than one vision period ago, by definition of "freshest". Raising the control rate shrinks the first term and grows the second by the same amount. The vision path cannot be made fresher by a faster controller; only a faster camera does that. Know this number before somebody proposes a $1\,\mathrm{kHz}$ loop as the fix for a late robot.

**Step 5 — so why $200\,\mathrm{Hz}$ at all?** Because the loop's other input is not on a topic (a named stream that nodes publish to and subscribe from, like `/goal` in the picture; §3). The encoder is read inside the controller at the tick, so its data is never more than one compute time old, and the motor is corrected every $5\,\mathrm{ms}$ instead of every $20$. P6 is two loops with two clocks sharing one process boundary: a slow outer path that says *where to go* and a fast inner path that says *how hard to push*. Every page in this track is about keeping those two apart, and section 1 is the first argument for it.

### 1. The problem a robot middleware solves

A robot is not one program. A camera driver reads frames at 30 Hz. A motor controller wants a command every few milliseconds. A planner thinks for half a second at a time. A logger writes to disk. A user interface runs on a laptop that is not the robot.

Write that as one process and three things go wrong. The camera driver crash takes the planner with it. Changing the planner means rebuilding and restarting everything, including the motor loop that was holding the arm up. And moving the interface onto the operator's laptop means inventing a network protocol.

So you split it into processes. Now you have four new problems:

1. **Data exchange.** Processes must pass structured data — images, transforms, velocity commands — across process and machine boundaries, at rates from 1 Hz to 1 kHz.
2. **Discovery.** The planner must find the camera driver without being told its IP address and port, because the camera driver may start after it, on a different machine, with a different port each time.
3. **Independent restart.** Killing and restarting one process must not require restarting the others, and the survivors must notice and reconnect.
4. **A common type language.** Two teams writing two nodes must agree on what "a pose" is, in a way a compiler can check.

A robot middleware is the layer that solves those four. ROS 2 is one such middleware, and the most widely used one in research robotics.

> **Robot middleware, defined.** A **robot middleware** is a *software layer*, libraries and tools between a robot's processes and the network, and it earns the name only by meeting all four conditions above: (1) **typed data exchange** across process and machine boundaries; (2) **discovery**, so no process is told another's address; (3) **independent restart**, the survivors reconnecting on their own; (4) **a common type language** a compiler can check. ROS 2 is one, plus conventions that make it usable: shared message definitions, name rules, build and command-line tools (§2).
>
> $$A_{\text{wired}}=\sum_{k}n^{\text{pub}}_{k}\,n^{\text{sub}}_{k},\qquad A_{\text{middleware}}=0$$
>
> where $A$ counts the addresses someone must configure and keep current, $k$ runs over the data streams, and $n^{\text{pub}}_k$, $n^{\text{sub}}_k$ count the processes producing and consuming stream $k$: hand-wired, every producer–consumer pair needs one, so the count grows as a product; with discovery (§4) a process names only its streams.
>
> - **Example**: P6 in the picture. `/goal` has $1$ producer and $2$ consumers and `/cmd` has $1$ and $1$ (the logger), so hand-wired $A=1\cdot2+1\cdot1=3$; under ROS 2, $0$ addresses and $2$ names.
> - **Non-example**: a raw socket. It moves bytes, condition (1) without the types, and none of (2)–(4): the $3$ addresses are kept by hand, and a camera restarted on a new port leaves both its consumers pointing at nothing. Those missing conditions are what a "just use a socket" proposal takes on (Self-check 1).

### 2. What ROS 2 is not

Three misreadings cost beginners weeks.

- **It is not an operating system.** The name is historical. ROS 2 runs *on* Linux (Ubuntu 24.04 for Jazzy); it is a set of libraries, message definitions, build tooling and command-line tools.
- **It is not a framework you must write your whole robot inside.** A ROS 2 node is an ordinary process that links a library. Your perception code, your solver, your learned policy can be plain Python or C++ with a thin ROS 2 edge that publishes and subscribes. Keeping that edge thin is good practice: it is what lets you unit-test the algorithm without a running graph.
- **It is not a real-time system by itself.** Nothing about installing ROS 2 gives you deadline guarantees. The official position is that ROS 2 is *designed with* real-time constraints in mind; achieving hard real time additionally requires an RT kernel (for example RT_PREEMPT, which bounds how long a ready thread waits to be scheduled; see [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]]), avoiding nondeterministic operations such as dynamic allocation and unbounded blocking in the execution path, and a middleware configuration that supports it. The ROS 2 real-time demo is documented as needing a source build against a static DDS API (DDS is the communication standard ROS 2 sits on, explained in Section 5). Treat "ROS 2 is real-time" as a claim that needs its conditions stated, not a property you get from `apt install`.

**What "real-time" means.** The word is about deadlines, not speed. A system is **real-time** when its correctness depends on *when* each result arrives as well as on its value: every job — one callback run, one control update — has a deadline, and it counts as correct only if it finishes by it. For one job the miss is measured as

$$\ell=\max\bigl(0,\;f-(r+D)\bigr)$$

where $r$ is the release time (when the job became ready to run), $D$ the relative deadline (how long it may take), $f$ the finish time, and $\ell$ the lateness, zero whenever the deadline was met. Two conditions separate the kinds. **Hard** real-time requires $\ell=0$ for every job, worst case included, because a late answer is a wrong answer: an airbag that fires after the head has hit the wheel. **Soft** real-time tolerates $\ell>0$ at a cost that grows with it, because a late answer is still used, only worse. P6's budget is soft in this sense: a goal released at camera mid-exposure ($r=0$, $D=70\,\mathrm{ms}$) whose force is applied at $f=75\,\mathrm{ms}$ has $\ell=5\,\mathrm{ms}$ and still moves the cart, a little off. The non-example is *fast*. A loop whose jobs take $1\,\mathrm{ms}$ on average but $100\,\mathrm{ms}$ once a minute is fast, and against a $10\,\mathrm{ms}$ deadline that one job has $\ell=100-10=90\,\mathrm{ms}$, so it is not real-time: real-time is a statement about the worst case, not the average. That is why the bullet above asks for an RT kernel and no dynamic allocation — both remove sources of rare, long delays that an average never shows.

### 3. The computation graph

The central idea, and the thing you will spend the rest of this track reasoning about:

- A **node** is a participating process (more precisely, a participating unit — one process can host several).
- Nodes exchange data over named **topics** (asynchronous streams), **services** (request–response), and **actions** (long-running goals with feedback).
- **Parameters** configure a node at startup and at runtime.
- The **graph** is the live set of nodes and their connections. It is not written down anywhere. It is discovered at runtime, and it changes as nodes come and go.

> **Computation graph, defined.** The **computation graph** is a *runtime data structure*, not a file: the nodes alive at time $t$ and the connections the middleware has matched between their endpoints. Three conditions: its **vertices** are nodes (defined in full on [[04-robotics/ros2/nodes-topics-messages|25.2 §2]]); an **edge** joins a publisher to a subscription, or a client to a server, only when the two are **matched** — same `ROS_DOMAIN_ID` (§4), same resolved name, same type, compatible QoS (§5); and it is **discovered, never declared**, so it exists only while its processes run.
>
> $$E(t)=\{(p,s):\ p,s\ \text{alive at }t,\ d_p=d_s,\ n_p=n_s,\ \tau_p=\tau_s,\ Q_p\sim Q_s\}$$
>
> where $p$ ranges over publishers and $s$ over subscriptions, $d$ is the domain ID, $n$ the resolved topic name, $\tau$ the message type and $Q_p\sim Q_s$ compatible QoS — a conjunction, so a mismatch in any one term deletes the edge without an error.
>
> - **Example**: P6 in the picture has $|E|=3$ — camera→controller and camera→logger on `/goal`, controller→logger on `/cmd` — and `ros2 topic info /goal` reports $1$ publisher and $2$ subscriptions.
> - **Non-example**: the launch file or the drawing. Stop `/logger` and neither changes, but $|E|$ drops from $3$ to $1$; a shell with `ROS_DOMAIN_ID=1` sees none of P6's nodes (§11). The tools report $E(t)$, which is why the next paragraph says to interrogate the running graph rather than the source.

The practical consequence: *you debug a ROS 2 system by interrogating the running graph*, not by reading source. Section 9 is the set of commands that does the interrogating, and it is the most durable thing on this page.

### 4. Why ROS 2 exists, given ROS 1

ROS 1 worked, and much of the robotics literature you will read ran on it. ROS 2 is a rewrite, not a version bump, for reasons that are all visible in the architecture:

- **Multi-robot systems.** ROS 1 discovery runs through a central `roscore` master. One master is a single point of failure and an awkward fit for fleets. ROS 2 uses distributed discovery with no master: nodes advertise themselves to the network and respond to each other's advertisements, and they announce when they go offline.
- **Security.** ROS 1 had no authentication, encryption, or access control on the wire. ROS 2 inherits the DDS security plugins — encryption in transit, authentication of participants, data integrity, and domain-wide access control — configured per *security enclave* (a named set of keys, certificates and permissions that the nodes using it share).
- **Embedded and small platforms.** ROS 2's layered design (client library → `rcl`, the shared C core that `rclcpp` and `rclpy` both wrap → `rmw`, the thin interface to whichever middleware is installed, detailed in Section 5 → middleware) was built so that constrained targets and microcontroller-oriented middleware variants are reachable, rather than assuming a full desktop Linux.
- **Real-time intent.** The official documentation states plainly that real-time performance was not considered in ROS 1's early stages and that retrofitting it is intractable; ROS 2 was prototyped with those constraints in mind from the start.

> **Discovery and the domain ID, defined.** **Discovery**, the mechanism in the first bullet, is a *distributed protocol every participant runs*, with no master; `ROS_DOMAIN_ID` is the *integer that scopes it*, $0$ unless the shell exports another. Four conditions: a starting node **announces itself** to nodes with the same domain ID, which answer with their own details; it **re-announces periodically**, so late arrivals are found; it **announces its departure**; and endpoints connect only if their QoS is **compatible** (§5). ROS 2 promises the partition; the DDS implementations of §5 enforce it by deriving their UDP ports from the domain ID:
>
> $$p_{\text{disc}}=7400+250\,d,\qquad p_{\text{uni}}=7410+250\,d+2i$$
>
> where $d$ is the domain ID, $p_{\text{disc}}$ the discovery multicast port and $p_{\text{uni}}$ the unicast discovery port of participant $i$, one per process on the machine, as the documentation's port calculator gives them; a port must fit in $16$ bits, so $d\le232$, and $0$–$101$ is the documented safe range on Linux.
>
> - **Example**: P6 on the default domain discovers on port $7400$; with `ROS_DOMAIN_ID=7` in all three shells it moves to $7400+250\cdot7=9150$, invisible to every domain-$0$ node.
> - **Non-example**: a namespace, or a lock. A second cart in `/cart2` on domain $0$ changes names, not discovery: both carts share port $7400$ and one graph. And a domain ID is no access control; anyone exporting the same integer joins, which security enclaves (second bullet) exist to stop.

And the decisive practical fact: **ROS 1 is over.** Noetic Ninjemys, the final ROS 1 distribution, reached end of life on 31 May 2025. New work starts on ROS 2. When you read a 2016–2021 paper whose code is ROS 1, you are reading an archive.

Which ROS 2, then. Jazzy Jalisco (May 2024) is supported until May 2029 and is the baseline here. Lyrical Luth (May 2026) is the newer LTS, supported to May 2031, and pairs with Gazebo Jetty — the right target for a project starting fresh with no dependency constraints. Kilted Kaiju is a non-LTS release that ends in December 2026, so do not choose it now.

### 5. DDS underneath: what it buys and what it costs

ROS 2 does not implement its own wire protocol, meaning the byte-level format that travels over the network. It borrows one.

That borrowed layer is **DDS** (Data Distribution Service), an OMG industry standard, and its wire protocol is called DDSI-RTPS. Several vendors ship DDS implementations. The ROS layer that adapts to a specific DDS product is the `rmw` (ROS middleware) interface, and several are supported:

- `rmw_fastrtps_cpp` — eProsima Fast DDS; the default, packaged with binary releases.
- `rmw_cyclonedds_cpp` — Eclipse Cyclone DDS; also packaged.
- `rmw_connextdds` — RTI Connext; commercial, installed separately.
- `rmw_gurumdds_cpp` — community support.

> **The rmw layer, defined.** `rmw` is an *interface*, the C API through which ROS reaches a middleware, and an **rmw implementation** is a *library* that fulfils it on one product, as `rmw_fastrtps_cpp` does on Fast DDS. Three conditions: everything above it is **vendor-agnostic** — your node, `rclpy` or `rclcpp`, and `rcl` call only `rmw`, so switching vendors needs no rebuild of your code; each process **uses one implementation**, named by the `RMW_IMPLEMENTATION` environment variable when it starts, `rmw_fastrtps_cpp` when unset; and **what crosses the wire belongs to the implementation**, not to ROS.
>
> $$\text{node}\ \to\ \texttt{rclpy}\,|\,\texttt{rclcpp}\ \to\ \texttt{rcl}\ \to\ \texttt{rmw}\ \to\ \texttt{rmw\_}\langle\text{impl}\rangle\ \to\ \text{vendor DDS}\ \to\ \text{network}$$
>
> where each arrow points to the layer that does the work; ROS 2 fixes the first four and `RMW_IMPLEMENTATION` picks the rest, so anything decided below `rmw` — discovery traffic, buffer sizes, the port formula of §4 — is a vendor property.
>
> - **Example**: start P6's three nodes with `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` in all three shells: the same code, the same graph of $3$ edges, a different library underneath.
> - **Non-example**: setting it in two shells of the three. The documentation calls communication between different implementations possible in limited circumstances and **not guaranteed**, so a P6 split $2:1$ across vendors may or may not connect — one implementation for the whole system is the rule.

What that buys:

- Distributed discovery with no master.
- Per-connection **Quality of Service** policies — reliability (retransmit lost messages or not), history depth (how many messages to queue), durability (whether a late joiner receives past messages), deadline (the longest allowed gap between messages), liveliness (how a dead publisher is detected), each explained in 25.5 — so a lossy 30 Hz camera stream and a must-not-drop command channel can have different delivery semantics on the same system.
- Security plugins that come from the standard rather than from ROS.
- A vendor choice, so no single implementation is a dependency of the project.

What it costs:

- **QoS is now a way to fail.** Two nodes connect only if their QoS settings are compatible. A mismatch produces a publisher and a subscriber that both look healthy and never exchange a message. This is the single most common "it's just silent" bug in ROS 2, and [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]] is where it is dissected.
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

Then the distribution itself. The official page interposes an upgrade between the update and the install, and it is not decoration: installing a large ROS package set against a stale Ubuntu invites dependency conflicts. (The separate `noble-updates` note below is about installing `ros-dev-tools`.) `desktop` includes RViz, the demos and the tutorials; `ros-base` is the same communication layer without GUI tools, which is what goes on a robot:

```bash
sudo apt update
sudo apt upgrade
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

> **Sourcing, defined.** **Sourcing** a setup file is an *operation on one shell*: `source` runs the file's commands inside the current shell rather than in a child, so the variables it exports, `PATH` and `AMENT_PREFIX_PATH` among them, change that shell's environment. Three conditions: it acts on the **current shell only**; its effect reaches **only processes started from that shell afterwards**, because a process receives a copy of its parent's environment when it starts and never sees later changes; and it **accumulates**, each sourced workspace putting its paths in front of what earlier ones set (the overlays of [[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]).
>
> $$\text{env}(c)=\text{env}(\text{parent of }c)\ \text{at the moment }c\text{ starts}$$
>
> where $c$ is any process, so a variable exported in one terminal exists in exactly the processes that terminal starts from then on, and in no other terminal.
>
> - **Example**: started by hand, P6's camera, controller and logger take three terminals, and each needs its own `source /opt/ros/jazzy/setup.bash`: $3$ sources for $3$ nodes, and a $4$th for the terminal where `ros2 topic list` runs.
> - **Non-example**: `bash /opt/ros/jazzy/setup.bash`. It runs without an error and changes nothing you can use: the exports happened in a child shell that has already exited, so the next command still answers `ros2: command not found` (§11). Sourcing in one tab and working in another fails the same way, hence §11's `printenv` before any code.

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

The short motion is a timer in the simulator, and its numbers are worth reading once. Each arrow press publishes one `geometry_msgs/msg/Twist` — for the up arrow, `linear.x` $=2.0$, the teleop node's `scale_linear` default — and `turtlesim_node` stores it and zeroes the velocity once more than $1.0\,\mathrm{s}$ has passed since the last command arrived. So one press moves the turtle about $2.0\times1.0=2.0$ units, holding the key down is many presses at the terminal's key-repeat rate, and the `ros2 topic pub` of §10 keeps the turtle circling only because it republishes once a second by default, renewing the timeout; stop it and the turtle halts about a second later. Two details carry over to real robots. The timer runs from the command's *arrival*, on the receiver's clock, because `Twist` carries no stamp, so it can see a silent link but not a late one; knowing how old the data is needs a stamped message ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §3]]). And the length is a design number: on P6 the same guard is the $70\,\mathrm{ms}$ budget, $14$ control ticks, and a one-second timeout borrowed from turtlesim would let the cart run $200$ ticks on a command nobody is sending any more.

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
6. Put terminal 4 back on `ros2 topic hz /turtle1/pose`, then stop turtlesim with Ctrl+C while `echo` and `hz` keep running. Neither crashes: `hz` on the pose goes quiet (turtlesim published it), while `echo` on `/turtle1/cmd_vel` keeps working because teleop, not turtlesim, publishes that topic. Restart turtlesim and `hz` resumes. That is item 3 of section 1, demonstrated.

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
| Your rebuilt node runs the old code | workspace overlay not sourced in this shell (or the package was first built after this shell sourced `install/setup.bash`) | `ros2 pkg prefix <pkg>` — points at `/opt/ros/jazzy` rather than your workspace |

The habit worth forming: when a ROS 2 system behaves impossibly, check the environment of the shell that is behaving impossibly *before* you read any source code. `printenv | grep -i ros` takes two seconds and settles it. The overlay cases in rows three and four are the subject of [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]].

### 12. What this page does not cover

Writing nodes of your own is [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]. Request–response, long-running goals, configuration and managed startup are [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. Building and installing your own packages, and starting many nodes at once, are [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]. The QoS settings printed by `ros2 topic info --verbose`, the executor that decides which callback runs, and simulated versus wall time are [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]] and [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]]. Simulation, navigation, manipulation and hardware interfaces sit above all of this in [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Installation: Ubuntu (deb packages); Configuring your ROS 2 environment; Using turtlesim, ros2 and rqt; Understanding nodes; Understanding topics.
- ROS 2 Jazzy documentation — Concepts: Discovery; Different ROS 2 middleware vendors; ROS 2 Security; Understanding real-time programming.
- ROS 2 Jazzy documentation — Concepts: [The ROS_DOMAIN_ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html) (default domain 0, the safe ranges, and the port calculator whose formula §4 writes out); [Internal ROS interfaces](https://docs.ros.org/en/jazzy/Concepts/Advanced/About-Internal-Interfaces.html) (client library → `rcl` → `rmw` → implementation); How-to guides: [Working with multiple RMW implementations](https://docs.ros.org/en/jazzy/How-To-Guides/Working-with-multiple-RMW-implementations.html) (`RMW_IMPLEMENTATION`).
- ROS 2 Jazzy documentation — Releases (distribution and EOL table).
- Open Robotics, "ROS Noetic End-of-Life: May 31, 2025" (ROS Discourse announcement).
- Gazebo documentation — ROS installation / ROS 2 and Gazebo version pairings.
- `ros/ros_tutorials` (jazzy branch) — turtlesim `src/turtle.cpp` (the velocity zeroed 1.0 s after the last command arrived) and `tutorials/teleop_turtle_key.cpp` (one `Twist` per key press, `scale_linear` default 2.0); `ros2/ros2cli` (jazzy branch) — `ros2topic/verb/pub.py` (default rate 1 Hz).

### Self-check

1. Your colleague says "we don't need ROS 2, it's just message passing — we'll use a socket."
   What are they underestimating?
2. `ros2 topic info /turtle1/cmd_vel` reports one publisher and two subscribers, but you only
   started turtlesim and teleop. Who is the second subscriber?
3. Why does a second terminal need `source /opt/ros/jazzy/setup.bash` when the first one
   already ran it?
4. Someone claims ROS 2 is a real-time system. What do you ask them?
5. P6's controller is dropped from $200\,\mathrm{Hz}$ to $50\,\mathrm{Hz}$ to save CPU. Which
   term of the $70\,\mathrm{ms}$ budget changes, by how much, and why does the age of the goal
   the motor is acting on barely move?

> [!tip]- Answers
> 1. Discovery without configuration, a checked type system shared across languages and teams, per-connection delivery semantics (QoS), and a live introspection surface. The socket is the easy quarter of the problem; the rest is what you would end up rewriting badly.
> 2. Your own `ros2 topic echo`. CLI introspection tools join the graph as real nodes; that is why they appear in `rqt_graph` under **Debug**.
> 3. Environment variables live in a process and are inherited only by children. The setup file sets `PATH`, `AMENT_PREFIX_PATH`, `LD_LIBRARY_PATH` and `PYTHONPATH` in the shell that runs it and nowhere else. The upside of that design is that different terminals can run different distributions or workspaces.
> 4. Hard or soft, against which deadline, and shown for the worst case or only the average (§2). Then which kernel, which middleware and configuration, and which operations were removed from the execution path. Installing ROS 2 from apt gives no deadline guarantees; the official position is that ROS 2 was *designed with* real-time constraints in mind, and the real-time demo itself is documented as requiring a source build against a static DDS API.
> 5. Only $L_{\text{wait}}$, the wait for the next control tick, which is bounded by one control period: it goes from under $5\,\mathrm{ms}$ to under $20\,\mathrm{ms}$, so the allowance left for camera, transport, compute and actuation falls from $65$ to $50\,\mathrm{ms}$ — $15\,\mathrm{ms}$, or $21.4\%$ of the budget. The *age* of the goal in force barely moves because $L_{\text{wait}}+L_{\text{reuse}}<T_{\text{vision}}=20\,\mathrm{ms}$ either way: at $200\,\mathrm{Hz}$ the goal waits at most $5\,\mathrm{ms}$ and is then re-used for three more ticks, at $50\,\mathrm{Hz}$ it waits up to $20\,\mathrm{ms}$ and is used once. What the fast loop really buys is the *encoder* path, which is read at the tick and corrects the motor every $5\,\mathrm{ms}$ rather than every $20$.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]]: encoder $N=2048$ counts/m, vision $50\,\mathrm{Hz}$, control $200\,\mathrm{Hz}$, end-to-end budget $70\,\mathrm{ms}$. No new simulator.

1. **Draw.** The picture's graph for a lab where a second, identical cart is started from the same launch on the same network: first with both carts on `ROS_DOMAIN_ID` 0, then with cart 2 moved to domain 1. Mark every `/goal` edge each controller receives, with the rate it arrives at, and the dashed domain boundaries. Then the picture's five-line timeline for cart 1 in the shared case, with the goals from both cameras on it.
2. **Derive.** (a) Vision period and control period. (b) Encoder $\Delta p$ for one count. (c) How many control samples fit in the $70\,\mathrm{ms}$ budget? How many vision frames?
3. **Interpret.** A colleague says "ROS 2 is real-time, so the $70\,\mathrm{ms}$ is guaranteed." What do you ask, and what does putting camera, controller, and logger in *one* process destroy that P6's budget cares about?

> [!note]- How to draw it · 그리는 법
> - Nodes are ellipses and the motors rectangles outside the graph, as in the picture — but now six ellipses, and in the shared case two of each name: `/camera`, `/controller`, `/logger` twice over.
> - In the shared case draw one `/goal` topic, not two: both cameras publish into it and both controllers and both loggers subscribe to it. Label the arrow into each controller with what arrives, $2\times50=100\,\mathrm{Hz}$ of goals, half of them from the other cart.
> - Write beside it what the tools say: `ros2 node list` shows each name twice with a warning about nodes sharing an exact name, and `ros2 topic info /goal` counts two publishers. Nothing errors.
> - In the split case, one dashed boundary per domain, labelled $0$ and $1$, and no edge crossing either: each controller receives only its own camera's $50\,\mathrm{Hz}$, and neither graph can see the other.
> - The encoder stays a short *read* arrow into each controller from its own hardware, not a topic, in both cases.
> - The timeline for cart 1 in the shared case: control ticks every $5\,\mathrm{ms}$ above, and below it goals every $20\,\mathrm{ms}$ from its own camera and, offset by the other camera's phase, every $20\,\mathrm{ms}$ from cart 2's. The controller acts on whichever arrived last, so its target jumps between the two carts' goals.

> [!tip]- Solutions
> 1. Shared domain: six nodes with three names each used twice (`ros2 node list` warns about nodes sharing an exact name) and one `/goal` topic with two publishers: each controller receives both carts' goals interleaved, $2\times50=100\,\mathrm{Hz}$, and steers toward whichever arrived last. Nothing errors; the timeline shows cart 1's target switching between two goal streams. Split: with cart 2 on domain 1, two dashed boundaries and no edge across them; each controller receives only its own $50\,\mathrm{Hz}$, and the two graphs do not discover each other. Namespaces, `/cart1/goal` and `/cart2/goal` on [[04-robotics/ros2/workspaces-packages-launch|25.3]], are the other fix, and they keep both carts in one `ros2 topic list`.
> 2. (a) $20\,\mathrm{ms}$, $5\,\mathrm{ms}$. (b) $1/2048\approx 0.488\,\mathrm{mm}$. (c) $14$ control samples, $3$ vision frames (a fourth would land at $80\,\mathrm{ms}$).
> 3. Which kernel, which rmw, which allocations were removed. Apt ROS 2 gives no deadline. One process: a logger stall or camera crash takes the $200\,\mathrm{Hz}$ loop with it — the independent-restart reason §1 split the robot.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — ROS 2 시스템을 실행하고 그 동작을 관찰할 정도. 미들웨어 자체를 수정할 정도는 아니다.
> **Working** — enough to run a ROS 2 system and see what it does, not to modify the middleware.

> [!note] 선수 지식 · Prerequisites
> 동작하는 Ubuntu 24.04 머신(또는 VM), 셸, Python. 그림과 계산 절에는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**(두 주기와 $70\,\mathrm{ms}$ 예산). ROS 경험은 필요 없다. 이 트랙의 기준 환경은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**이고, 시뮬레이션 단계에서는 Gazebo Harmonic과 짝을 이룬다([[04-robotics/ros2/index|25. ROS 2]]).
> A working Ubuntu 24.04 machine, a shell, and Python; **P6** from 0.6 for the picture and the Worked case; no prior ROS assumed.

> [!note] 처음이라면 · First pass
> 한 페이지에 길이 둘이다. ROS 2 명령을 한 번도 쳐 본 적이 없다면 먼저 키보드 앞에서 6–10절을 끝내라 — 설치, source, turtlesim 실행, 그 그래프 읽기 — 그리고 그림과 계산 절로 돌아온다. 그 둘은 P6의 두 주기에 대한 산수라 아무것도 설치하지 않아도 된다. 어느 길이든 1–3절은 뒤의 모든 페이지가 쓰는 개념이고, "실시간"이 뜻을 얻는 곳이 2절이다. 4–5절(ROS 2가 ROS 1을 대체한 이유, 아래에 깔린 DDS)과 11절의 환경 표는 두 번째 읽기다. 누가 QoS가 왜 있느냐고 묻거나 셸이 불가능한 동작을 할 때 연다.

### 그림으로 먼저 보기: P6 그래프와 시계 위의 예산 하나 · The picture

<svg viewBox="0 0 560 400" style="max-width:100%;height:auto" role="img" aria-label="위: P6 계산 그래프. ROS 도메인 하나 안의 /camera, /controller, /logger, 50 Hz /goal과 200 Hz /cmd 토픽, 그래프 밖의 모터와 엔코더. 아래: 0에서 80 ms 시계 위에 예산 항 다섯을 이어지는 괄호로 그렸고, 70 ms 마감선 왼쪽에서 끝난다.">
  <defs><marker id="w1kopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="w1ksol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">계산 그래프 (ros2 node list와 ros2 topic list -t가 보고하는 그대로)</text>
  <rect x="12" y="30" width="314" height="174" rx="10" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.55" stroke-dasharray="5 4" fill="none"/>
  <text x="20" y="46" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">export ROS_DOMAIN_ID=&lt;정수&gt;</text>
  <ellipse cx="66" cy="96" rx="44" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="66" y="100" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="250" cy="96" rx="60" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="250" y="100" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <ellipse cx="158" cy="160" rx="44" ry="16" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="158" y="164" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/logger</text>
  <line x1="110" y1="96" x2="188" y2="96" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1kopen)"/>
  <text x="150" y="86" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan> <tspan font-style="italic">[type]</tspan></text>
  <text x="150" y="110" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">50 Hz</text>
  <line x1="86.4" y1="110.2" x2="136.1" y2="144.8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1kopen)"/>
  <text x="84" y="140" font-size="11" text-anchor="middle" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <line x1="228.5" y1="110.9" x2="179.9" y2="144.8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1kopen)"/>
  <text x="236" y="142" font-size="11" text-anchor="middle" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">/cmd</text>
  <rect x="404" y="70" width="144" height="40" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="476" y="87" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">모터</text>
  <text x="476" y="102" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">하드웨어, 노드가 아님</text>
  <line x1="309.4" y1="93.7" x2="402" y2="90" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#w1kopen)"/>
  <text x="366" y="82" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/cmd</tspan> <tspan font-style="italic">[type]</tspan></text>
  <text x="366" y="108" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">200 Hz</text>
  <rect x="404" y="134" width="144" height="28" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="476" y="152" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">엔코더</text>
  <line x1="403" y1="148" x2="289.2" y2="109.6" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" stroke-dasharray="2 3" fill="none" marker-end="url(#w1ksol)"/>
  <text x="356" y="147" font-size="11" text-anchor="middle" fill-opacity="0.9" font-style="italic" fill="currentColor">읽음</text>
  <text x="20" y="194" font-size="11" fill-opacity="0.5" fill="currentColor"><tspan font-family="ui-monospace,monospace">/rosout  /parameter_events</tspan>  (모든 그래프에 있음, 9절)</text>
  <text x="404" y="184" font-size="11" fill-opacity="0.6" fill="currentColor">[type]: P6의 메시지 타입은</text>
  <text x="404" y="198" font-size="11" fill-opacity="0.6" fill="currentColor">이 페이지가 정하지 않음</text>
  <text x="12" y="232" font-size="12" fill-opacity="0.8" fill="currentColor">시계 위의 예산 하나, 축척대로 (카메라 노출 중간부터 ms)</text>
  <line x1="104" y1="316" x2="544" y2="316" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" fill="none"/>
  <path d="M104.0 316v-7M131.5 316v-7M159.0 316v-7M186.5 316v-7M214.0 316v-7M241.5 316v-7M269.0 316v-7M296.5 316v-7M324.0 316v-7M351.5 316v-7M379.0 316v-7M406.5 316v-7M434.0 316v-7M461.5 316v-7M489.0 316v-7M516.5 316v-7M544.0 316v-7" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="none"/>
  <path d="M104.0 316v11M214.0 316v11M324.0 316v11M434.0 316v11" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.9" fill="none"/>
  <text x="104" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="214" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">20</text>
  <text x="324" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">40</text>
  <text x="434" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="544" y="340" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">80</text>
  <text x="96" y="315" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">제어 200 Hz</text>
  <text x="96" y="327" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">비전 50 Hz</text>
  <path d="M104.8 288V282H213.2V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="159" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">cam</tspan></text>
  <path d="M214.8 288V282H240.7V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="227.8" y="262" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">net</tspan></text>
  <line x1="227.8" y1="266" x2="227.8" y2="281" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <rect x="241.5" y="282" width="27.5" height="34" fill="currentColor" fill-opacity="0.13" stroke="none"/>
  <path d="M242.3 288V282H268.2V288" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <text x="255.2" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" font-weight="bold" fill="currentColor">L<tspan font-size="9.4" dy="3">wait</tspan></text>
  <path d="M269.8 288V282H284.7V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="277.2" y="262" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">ctrl</tspan></text>
  <line x1="277.2" y1="266" x2="277.2" y2="281" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <path d="M286.3 288V282H323.2V288" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none"/>
  <text x="304.8" y="277" font-size="12" text-anchor="middle" fill-opacity="0.9" fill="currentColor">L<tspan font-size="9.4" dy="3">act</tspan></text>
  <line x1="489" y1="248" x2="489" y2="328" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9" fill="none"/>
  <text x="489" y="243" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">70 ms 마감</text>
  <text x="332.2" y="245" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">cam</tspan>  <tspan dy="-3">카메라 파이프라인</tspan></text>
  <text x="332.2" y="258" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">net</tspan>  <tspan dy="-3">전송</tspan></text>
  <text x="332.2" y="271" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">L<tspan font-size="8.6" dy="3">wait</tspan>  <tspan dy="-3">다음 틱까지 대기</tspan></text>
  <text x="332.2" y="284" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">ctrl</tspan>  <tspan dy="-3">계산</tspan></text>
  <text x="332.2" y="297" font-size="11" fill-opacity="0.85" fill="currentColor">L<tspan font-size="8.6" dy="3">act</tspan>  <tspan dy="-3">구동</tspan></text>
  <text x="12" y="358" font-size="11" fill-opacity="0.85" fill="currentColor">t = 0이 카메라 노출 중간. 비전 간격 20 ms = 제어 주기 넷.</text>
  <text x="12" y="373" font-size="11" fill-opacity="0.85" fill="currentColor">실선: L<tspan font-size="8.6" dy="3">wait</tspan> <tspan dy="-3">&lt; T</tspan><tspan font-size="8.6" dy="3">ctrl</tspan> <tspan dy="-3">= 5 ms, 두 주기가 정하는 유일한 항.</tspan></text>
  <text x="12" y="388" font-size="11" fill-opacity="0.85" fill="currentColor">점선: 재야 할 네 항. 폭은 예시이고, 넷의 합은 70 − 5 = 65 ms 이하.</text>
</svg>

위는 `ROS_DOMAIN_ID`(셸이 다른 값을 export하지 않으면 0인 정수로, 값이 같은 노드끼리만 서로를 탐색한다. 5절) 하나 안에 그린 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** 계산 그래프로, `/camera`가 `/goal`을 $50\,\mathrm{Hz}$로 발행하고 `/controller`가 노드가 아니라 하드웨어인 모터에 `/cmd`를 $200\,\mathrm{Hz}$로 보내며 `/logger`가 둘 다 구독하고, 엔코더는 토픽으로 받지 않고 제어기 안에서 직접 읽는다. 아래는 카메라 노출 중간부터 힘이 나갈 때까지의 $70\,\mathrm{ms}$를 이어지는 항 다섯으로 축척대로 그린 것이고, 비전 발행은 $20\,\mathrm{ms}$마다, 곧 제어 주기 넷 간격이다. 두 주기만으로 정해지는 항은 다음 제어 틱까지의 대기 하나로 제어 주기 하나인 $5\,\mathrm{ms}$ 미만이며, 그래서 재야 할 나머지 네 항에는 많아야 $65\,\mathrm{ms}$가 남는다.

### 대상으로 한 번 끝까지: P6의 70 ms는 어디로 가고, 제어 주기는 무엇을 사 주는가 · Worked case

주기부터. 이 페이지의 다른 모든 숫자가 이 둘 중 하나를 나눈 값이기 때문이다.

$$T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=0.020\,\mathrm{s}=20\,\mathrm{ms},\qquad T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=0.005\,\mathrm{s}=5\,\mathrm{ms}$$

이므로 예산 창 하나에는 제어 주기가 $70/5=14$개 온전히 들어가고, 비전 주기는 $70/20=3.5$개 — 온전한 것은 셋이고 넷째는 $80\,\mathrm{ms}$에서 끝나 예산 밖이다.

**1단계 — 예산을 숫자가 아니라 합으로 쓴다**. 노출 중간에서 힘까지의 지연은

$$70\,\mathrm{ms}\;\ge\;L_{\text{cam}}+L_{\text{net}}+L_{\text{wait}}+L_{\text{ctrl}}+L_{\text{act}}$$

다섯 단계가 엄격히 순차적이기 때문이다. 프레임이 잡혀 발행되고($L_{\text{cam}}$), 프로세스나 머신 경계를 넘고($L_{\text{net}}$), 계속 듣고 있지 않은 제어기를 기다리고($L_{\text{wait}}$), 명령이 되고($L_{\text{ctrl}}$), 모터의 전류가 된다($L_{\text{act}}$). 다섯 중 넷은 당신 코드와 하드웨어의 성질이라 재어야 한다. 정확히 하나만 P6의 두 주기만으로 정해지고, 무엇을 재기 전에 이 합부터 적는 이유가 그것이다.

**2단계 — 그래프가 정하는 그 한 항**. 시각 $g$에 발행된 목표는 다음 제어 틱 전까지 보이지 않고 틱 간격은 제어 주기 하나이므로

$$0\le L_{\text{wait}}<T_{\text{ctrl}}=5\,\mathrm{ms}$$

목표는 주기 안 아무 데나 떨어질 수 있고 최악은 틱 직후에 떨어지는 경우이기 때문이다. ROS 2도, DDS(ROS 2가 올라타는 통신 계층, 5절)도, 운영체제도 이 한계를 옮기지 못한다. $50$과 $200$에 대한 산수일 뿐이다.

**3단계 — 그래서 남는 여유, 그리고 느린 루프의 값**. 측정해야 할 네 항에 $70-5=65\,\mathrm{ms}$가 남는다. 같은 제어기를 $50\,\mathrm{Hz}$로 돌리면 한계가 $L_{\text{wait}}<20\,\mathrm{ms}$가 되어 $70-20=50\,\mathrm{ms}$만 남는다. 제어 주기를 네 배로 올린 것이 프레임-투-포스 경로에서 $15\,\mathrm{ms}$, 곧 전체 예산의 $15/70=21.4\%$를 사 준 셈이고, 카메라도 네트워크도 모터도 건드리지 않았다. "루프를 빠르게 돌린다"는 말의 정직한 판본이다.

**4단계 — 그리고 사 주지 못하는 것**. $T_{\text{vision}}/T_{\text{ctrl}}=20/5=4$가 정확히 나누어떨어지므로 목표 하나는 정확히 네 틱이 소비한다. 신선한 상태로 쓰는 것은 첫 틱뿐이고 나머지 셋은 재사용이라 $5$, $10$, $15\,\mathrm{ms}$의 나이를 더한다. 네 틱 평균 $7.5\,\mathrm{ms}$로 예산의 $10.7\%$, 최악 $15\,\mathrm{ms}$로 $21.4\%$다. 두 효과를 더하면 루프를 어떻게 하든 한계가 같다.

$$L_{\text{wait}}+L_{\text{reuse}}<T_{\text{vision}}=20\,\mathrm{ms}$$

어느 틱에서든 손에 쥔 가장 최신 목표는 정의상 한 비전 주기 안에 발행된 것이기 때문이다. 제어 주기를 올리면 첫 항이 줄고 둘째 항이 그만큼 는다. 비전 경로는 빠른 제어기로 신선해지지 않는다. 그건 빠른 카메라만 한다. 누군가 늦는 로봇의 처방으로 $1\,\mathrm{kHz}$ 루프를 제안하기 전에 이 숫자를 알고 있어야 한다.

**5단계 — 그러면 왜 $200\,\mathrm{Hz}$인가**. 루프의 다른 입력이 토픽(노드들이 publish하고 subscribe하는 이름 붙은 스트림. 그림의 `/goal`이 그렇다. 3절) 위에 있지 않기 때문이다. 엔코더는 틱마다 제어기 안에서 읽으므로 그 데이터는 계산 시간 이상 낡지 않고, 모터는 $20\,\mathrm{ms}$가 아니라 $5\,\mathrm{ms}$마다 보정된다. P6은 프로세스 경계 하나를 공유하는, 시계가 둘인 루프 둘이다. *어디로 갈지*를 말하는 느린 바깥 경로와 *얼마나 세게 밀지*를 말하는 빠른 안쪽 경로. 이 트랙의 모든 페이지가 그 둘을 갈라 두는 이야기이고, 1절이 그 첫 논거다.

### 1. 로봇 미들웨어가 푸는 문제

로봇은 프로그램 하나가 아니다. 카메라 드라이버는 30 Hz로 프레임을 읽고, 모터 제어기는 수 밀리초마다 명령을 원하고, 플래너는 한 번에 0.5초씩 생각하고, 로거는 디스크에 쓰고, 사용자 인터페이스는 로봇이 아닌 노트북에서 돈다.

이걸 한 프로세스로 짜면 세 가지가 깨진다. 카메라 드라이버가 죽으면 플래너도 같이 죽는다. 플래너를 바꾸려면 팔을 들고 있던 모터 루프까지 전부 재시작해야 한다. 인터페이스를 조작자 노트북으로 옮기려면 네트워크 프로토콜을 직접 발명해야 한다.

그래서 프로세스로 쪼갠다. 그러면 새 문제 네 개가 생긴다.

1. **데이터 교환** — 이미지, 변환, 속도 명령 같은 구조화된 데이터를 프로세스와 머신 경계를 넘어 1 Hz에서 1 kHz까지의 속도로 주고받아야 한다.
2. **탐색(discovery)** — 플래너는 카메라 드라이버의 IP와 포트를 듣지 않고도 그것을 찾아야 한다. 드라이버는 나중에, 다른 머신에서, 매번 다른 포트로 뜰 수 있다.
3. **독립적인 재시작** — 한 프로세스를 죽였다 살리는 데 다른 프로세스를 재시작해야 해서는 안 되고, 살아남은 쪽이 알아서 다시 연결해야 한다.
4. **공통 타입 언어** — 두 팀이 "자세(pose)"가 무엇인지 컴파일러가 검사할 수 있는 형태로 합의해야 한다.

로봇 미들웨어는 이 넷을 푸는 계층이다. ROS 2가 그런 미들웨어이고, 연구 로보틱스에서 가장 널리 쓰인다.

> **로봇 미들웨어의 정의.** **로봇 미들웨어**(robot middleware)는 로봇의 프로세스들과 네트워크 사이에 놓인 *소프트웨어 계층*, 곧 라이브러리와 도구의 묶음이고, 위의 네 조건을 모두 채워야만 이 이름을 얻는다. (1) 프로세스와 머신 경계를 넘는 **타입 있는 데이터 교환**, (2) 어느 프로세스도 남의 주소를 전해 듣지 않아도 되는 **탐색**, (3) 살아남은 쪽이 알아서 다시 붙는 **독립 재시작**, (4) 컴파일러가 검사할 수 있는 **공통 타입 언어**. ROS 2가 그런 미들웨어이고, 그것을 쓸 만하게 만드는 관례 — 공유 메시지 정의, 이름 규칙, 빌드와 커맨드라인 도구(2절) — 가 함께 온다.
>
> $$A_{\text{wired}}=\sum_{k}n^{\text{pub}}_{k}\,n^{\text{sub}}_{k},\qquad A_{\text{middleware}}=0$$
>
> $A$는 누군가 설정하고 최신으로 유지해야 하는 주소의 수, $k$는 데이터 스트림, $n^{\text{pub}}_k$와 $n^{\text{sub}}_k$는 스트림 $k$를 내는 프로세스와 받는 프로세스의 수다. 손으로 배선하면 생산자–소비자 쌍마다 주소가 하나씩 필요해서 곱으로 늘고, 탐색(4절)이 있으면 프로세스는 자기가 쓰는 스트림의 이름만 안다.
>
> - **예**: 그림의 P6. `/goal`은 생산자 $1$, 소비자 $2$이고 `/cmd`는 $1$과 $1$(로거)이므로 손 배선이면 $A=1\cdot2+1\cdot1=3$이다. ROS 2에서는 주소 $0$개, 이름 $2$개다.
> - **비예**: 맨 소켓. 바이트를 옮기니 조건 (1)을 타입 없이 채울 뿐이고 (2)–(4)는 하나도 주지 않는다. 주소 $3$개를 손으로 관리해야 하고, 카메라가 새 포트로 재시작하면 두 소비자가 모두 아무것도 없는 곳을 가리킨다. "그냥 소켓 쓰자"는 제안이 떠안는 일이 바로 이 빠진 조건들이다(스스로 점검 1번).

### 2. ROS 2가 아닌 것

초심자가 몇 주를 잃는 오해 세 가지.

- **운영체제가 아니다.** 이름은 역사적 유물이다. ROS 2는 Linux 위에서 돈다(Jazzy는 Ubuntu 24.04). 라이브러리, 메시지 정의, 빌드 도구, 커맨드라인 도구의 묶음이다.
- **로봇 전체를 그 안에 작성해야 하는 프레임워크가 아니다.** ROS 2 노드는 라이브러리를 링크한 평범한 프로세스다. 인식 코드, 솔버, 학습된 정책은 평범한 Python이나 C++로 두고, publish/subscribe 하는 얇은 ROS 2 경계만 붙이면 된다. 그 경계를 얇게 유지하는 것이 좋은 습관이다. 그래야 그래프를 띄우지 않고 알고리즘을 단위 테스트할 수 있다.
- **그 자체로 실시간 시스템이 아니다.** ROS 2를 설치한다고 마감 시한 보장이 생기지는 않는다. 공식 문서의 입장은 ROS 2가 실시간 제약을 *염두에 두고 설계되었다*는 것이다. 경성 실시간을 얻으려면 RT 커널(예: RT_PREEMPT. 실행 준비된 스레드가 스케줄되기까지 기다리는 시간을 유계로 만든다. [[04-robotics/ros2/from-simulation-to-hardware|25.11 From Simulation to Real Hardware]] 참고), 실행 경로에서 동적 할당과 무한 블로킹 같은 비결정적 연산 제거, 그리고 그것을 지원하는 미들웨어 구성이 함께 필요하다. 공식 실시간 데모 자체가 정적 DDS API(DDS는 ROS 2가 올라타는 통신 표준으로, 5절에서 설명한다)에 대한 소스 빌드를 요구한다고 문서화되어 있다. "ROS 2는 실시간"이라는 말은 조건을 명시해야 하는 주장이지 `apt install`로 얻는 성질이 아니다.

**"실시간"이 뜻하는 것.** 이 말은 속도가 아니라 마감에 관한 것이다. 시스템의 올바름이 결과의 값만이 아니라 결과가 *언제* 도착하는지에도 달려 있으면 그 시스템은 **실시간(real-time)** 이다. 모든 작업(job) — 콜백 한 번 실행, 제어 갱신 한 번 — 에 마감이 있고, 마감까지 끝나야만 올바른 것으로 친다. 작업 하나가 마감을 얼마나 놓쳤는지는

$$\ell=\max\bigl(0,\;f-(r+D)\bigr)$$

로 잰다. $r$는 해제 시각(작업이 실행 준비된 시각), $D$는 상대 마감(걸려도 되는 시간), $f$는 끝난 시각, $\ell$은 지각(lateness)이고, 마감을 지키면 0이다. 종류를 가르는 조건은 둘이다. **경성(hard)** 실시간은 최악의 경우까지 포함해 모든 작업에 $\ell=0$을 요구한다. 늦은 답은 틀린 답이기 때문이다. 머리가 핸들에 부딪힌 뒤에 터지는 에어백이 그렇다. **연성(soft)** 실시간은 $\ell>0$을 허용하되 그에 따라 커지는 비용을 치른다. 늦은 답도 쓰이지만 더 나쁘게 쓰이기 때문이다. P6의 예산은 이 뜻에서 연성이다. 카메라 노출 중간에 해제된 목표($r=0$, $D=70\,\mathrm{ms}$)의 힘이 $f=75\,\mathrm{ms}$에 나가면 $\ell=5\,\mathrm{ms}$이고, 카트는 조금 어긋나게나마 여전히 움직인다. 반례는 *빠름*이다. 작업이 평균 $1\,\mathrm{ms}$ 걸리지만 1분에 한 번 $100\,\mathrm{ms}$ 걸리는 루프는 빠르다. 그러나 $10\,\mathrm{ms}$ 마감에 대해 그 한 작업은 $\ell=100-10=90\,\mathrm{ms}$이므로 실시간이 아니다. 실시간은 평균이 아니라 최악의 경우에 대한 진술이다. 위 항목이 RT 커널과 동적 할당 제거를 요구하는 이유가 이것이다. 둘 다 평균에는 드러나지 않는 드물고 긴 지연의 원천을 없앤다.

### 3. 계산 그래프(computation graph)

이 트랙 내내 다룰 중심 개념이다.

- **노드(node)** 는 참여 프로세스다(정확히는 참여 단위 — 한 프로세스가 여러 노드를 담을 수 있다).
- 노드들은 이름 붙은 **토픽**(비동기 스트림), **서비스**(요청–응답), **액션**(피드백을 주는 장시간 목표)으로 데이터를 주고받는다.
- **파라미터**는 시작 시점과 실행 중에 노드를 설정한다.
- **그래프**는 살아 있는 노드와 연결의 집합이다. 어디에도 적혀 있지 않고, 런타임에 탐색되며, 노드가 뜨고 지면 바뀐다.

> **계산 그래프의 정의.** **계산 그래프**(computation graph)는 파일이 아니라 *실행 중에만 존재하는 자료 구조*다. 시각 $t$에 살아 있는 노드들과, 미들웨어가 그 엔드포인트 사이에 맺어 준 연결이다. 조건은 셋이다. **꼭짓점**은 노드다(완전한 정의는 [[04-robotics/ros2/nodes-topics-messages|25.2 §2]]). **간선**은 퍼블리셔와 서브스크립션, 또는 클라이언트와 서버가 **짝지어졌을 때만** 생긴다 — 같은 `ROS_DOMAIN_ID`(4절), 같은 해석된 이름, 같은 타입, 호환되는 QoS(5절). 그리고 **선언되지 않고 탐색된다**. 그래서 프로세스가 도는 동안에만 존재한다.
>
> $$E(t)=\{(p,s):\ p,s\ \text{alive at }t,\ d_p=d_s,\ n_p=n_s,\ \tau_p=\tau_s,\ Q_p\sim Q_s\}$$
>
> $p$는 퍼블리셔, $s$는 서브스크립션, $d$는 도메인 ID, $n$은 해석된 토픽 이름, $\tau$는 메시지 타입, $Q_p\sim Q_s$는 QoS 호환이다. 조건들의 논리곱이므로 어느 한 항만 어긋나도 간선은 오류 없이 사라진다.
>
> - **예**: 그림의 P6은 $|E|=3$이다. `/goal` 위의 카메라→제어기와 카메라→로거, `/cmd` 위의 제어기→로거. `ros2 topic info /goal`은 퍼블리셔 $1$, 서브스크립션 $2$를 보고한다.
> - **비예**: launch 파일이나 그림. `/logger`를 멈춰도 둘은 그대로지만 $|E|$는 $3$에서 $1$로 준다. `ROS_DOMAIN_ID=1`인 셸에서는 P6의 노드가 하나도 보이지 않는다(11절). 도구가 보고하는 것은 $E(t)$이고, 그래서 다음 문단이 소스가 아니라 돌아가는 그래프를 심문하라고 말한다.

실무적 귀결: *ROS 2 시스템은 소스를 읽어서가 아니라 돌아가는 그래프를 심문해서 디버깅한다.* 9절이 그 심문 명령들이고, 이 페이지에서 가장 오래 쓸 내용이다.

### 4. ROS 1이 있는데 ROS 2가 존재하는 이유

ROS 1은 잘 돌아갔고, 당신이 읽을 로보틱스 문헌의 상당수가 그 위에서 실행됐다. ROS 2는 버전 업이 아니라 재작성이며, 이유는 모두 구조에 드러난다.

- **다중 로봇.** ROS 1의 탐색은 중앙 `roscore` 마스터를 거친다. 마스터 하나는 단일 장애점이고 군집에 어울리지 않는다. ROS 2는 마스터 없는 분산 탐색을 쓴다. 노드가 네트워크에 자신을 알리고 서로의 광고에 응답하며, 종료할 때도 알린다.
- **보안.** ROS 1에는 전송 구간의 인증·암호화·접근 제어가 없었다. ROS 2는 DDS 보안 플러그인을 물려받는다 — 전송 암호화, 참여자 인증, 무결성, 도메인 전역 접근 제어. 설정 단위는 *security enclave*(그것을 쓰는 노드들이 공유하는 키·인증서·권한의 이름 붙은 묶음)다.
- **임베디드·소형 플랫폼.** 계층 설계(클라이언트 라이브러리 → `rcl`: `rclcpp`와 `rclpy`가 함께 감싸는 공용 C 코어 → `rmw`: 설치된 미들웨어에 닿는 얇은 인터페이스, 5절에서 설명 → 미들웨어)는 데스크톱 Linux를 전제하지 않고 제약된 대상에 닿을 수 있도록 만들어졌다.
- **실시간 의도.** 공식 문서는 ROS 1 초기 설계에서 실시간이 고려되지 않았고 이제 와서 개조하는 것은 불가능에 가깝다고 분명히 적는다. ROS 2는 그 제약을 처음부터 염두에 두고 시제품화됐다.

> **탐색과 도메인 ID의 정의.** **탐색**(discovery)은 첫째 항목의 그 메커니즘으로, 마스터 없이 *모든 참여자가 함께 돌리는 분산 프로토콜*이다. `ROS_DOMAIN_ID`는 그 범위를 정하는 *정수*이고, 셸이 다른 값을 export하지 않으면 $0$이다. 조건은 넷이다. 시작하는 노드는 도메인 ID가 같은 노드들에게 **자신을 알리고**, 그들은 자기 정보로 답한다. 주기적으로 **다시 알려서** 늦게 온 쪽도 찾는다. 떠날 때 **떠난다고 알린다**. 그리고 엔드포인트는 QoS가 **호환될 때만** 연결된다(5절). ROS 2가 약속하는 것은 분리 자체이고, 5절의 DDS 구현들은 도메인 ID에서 UDP 포트를 계산하는 방식으로 그것을 지킨다.
>
> $$p_{\text{disc}}=7400+250\,d,\qquad p_{\text{uni}}=7410+250\,d+2i$$
>
> $d$는 도메인 ID, $p_{\text{disc}}$는 탐색용 멀티캐스트 포트, $p_{\text{uni}}$는 참여자 $i$의 탐색용 유니캐스트 포트이고, 참여자는 그 머신의 프로세스마다 하나다. 문서의 포트 계산기가 쓰는 식 그대로다. 포트는 $16$비트에 들어가야 하므로 $d\le232$이고, 문서가 Linux에서 안전하다고 하는 범위는 $0$–$101$이다.
>
> - **예**: 기본 도메인의 P6은 포트 $7400$에서 탐색한다. 세 셸 모두 `ROS_DOMAIN_ID=7`이면 $7400+250\cdot7=9150$으로 옮겨 가고, 도메인 $0$의 어떤 노드에게도 보이지 않는다.
> - **비예**: 네임스페이스, 또는 자물쇠. 도메인 $0$에서 `/cart2`로 밀어 넣은 두 번째 카트는 이름만 바뀌고 탐색은 그대로라, 두 카트가 포트 $7400$과 그래프 하나를 함께 쓴다. 그리고 도메인 ID는 접근 제어가 아니다. 같은 정수를 export한 누구든 들어오고, 그것을 막으라고 있는 것이 보안 enclave(둘째 항목)다.

그리고 결정적인 실무 사실: **ROS 1은 끝났다.** 마지막 ROS 1 배포판 Noetic Ninjemys는 2025년 5월 31일 지원이 종료됐다. 새 작업은 ROS 2에서 시작한다. 코드가 ROS 1인 2016–2021년 논문을 읽는다면 그것은 아카이브를 읽는 것이다.

그러면 어떤 ROS 2인가. Jazzy Jalisco(2024년 5월)는 2029년 5월까지 지원되며 여기의 기준이다. Lyrical Luth(2026년 5월)는 더 새로운 LTS로 2031년 5월까지 지원되고 Gazebo Jetty와 짝을 이룬다 — 의존성 제약이 없는 새 프로젝트라면 이쪽이 맞다. Kilted Kaiju는 비LTS이고 2026년 12월에 끝나므로 지금 고르면 안 된다.

### 5. 아래에 깔린 DDS: 무엇을 사고 무엇을 치르는가

ROS 2는 자체 와이어 프로토콜, 즉 네트워크를 오가는 바이트 수준 형식을 구현하지 않는다. 빌려 쓴다.

빌려 쓰는 계층이 OMG 산업 표준인 **DDS**(Data Distribution Service)이고, 그 와이어 프로토콜 이름이 DDSI-RTPS다. 여러 벤더가 DDS 구현을 내놓는다. 특정 DDS 제품에 맞추는 ROS 계층이 `rmw`(ROS middleware) 인터페이스이고, 여럿이 지원된다.

- `rmw_fastrtps_cpp` — eProsima Fast DDS. 기본값, 바이너리 배포에 포함.
- `rmw_cyclonedds_cpp` — Eclipse Cyclone DDS. 역시 포함.
- `rmw_connextdds` — RTI Connext. 상용, 별도 설치.
- `rmw_gurumdds_cpp` — 커뮤니티 지원.

> **rmw 계층의 정의.** `rmw`는 *인터페이스*, 곧 ROS가 미들웨어에 닿는 C API이고, **rmw 구현**(rmw implementation)은 그것을 제품 하나 위에서 이행하는 *라이브러리*다. `rmw_fastrtps_cpp`가 Fast DDS 위에서 그렇게 한다. 조건은 셋이다. 그 위의 모든 것이 **벤더와 무관하다** — 당신의 노드, `rclpy`나 `rclcpp`, `rcl`은 `rmw`만 부르므로 벤더를 바꿔도 당신 코드를 다시 빌드할 필요가 없다. 프로세스마다 **구현 하나를 쓴다** — 프로세스가 시작할 때 `RMW_IMPLEMENTATION` 환경 변수가 정하고, 비어 있으면 `rmw_fastrtps_cpp`다. 그리고 **와이어 위로 나가는 것은 구현의 몫**이지 ROS의 몫이 아니다.
>
> $$\text{node}\ \to\ \texttt{rclpy}\,|\,\texttt{rclcpp}\ \to\ \texttt{rcl}\ \to\ \texttt{rmw}\ \to\ \texttt{rmw\_}\langle\text{impl}\rangle\ \to\ \text{vendor DDS}\ \to\ \text{network}$$
>
> 화살표는 실제 일을 하는 아래 계층을 가리킨다. 앞의 넷은 ROS 2가 고정하고 나머지는 `RMW_IMPLEMENTATION`이 고르므로, `rmw` 아래에서 정해지는 것 — 탐색 트래픽, 버퍼 크기, 4절의 포트 식 — 은 벤더의 성질이다.
>
> - **예**: P6의 노드 셋을 세 셸 모두 `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`로 띄운다. 같은 코드, 간선 $3$개인 같은 그래프이고, 아래의 라이브러리만 다르다.
> - **비예**: 세 셸 중 둘에만 설정하기. 문서는 서로 다른 구현 사이의 통신이 제한된 상황에서는 될 수 있지만 **보장되지 않는다**고 적으므로, 벤더가 $2:1$로 갈린 P6은 연결될 수도 안 될 수도 있다. 시스템 전체에 구현 하나가 규칙이다.

사는 것:

- 마스터 없는 분산 탐색.
- 연결 단위의 **QoS** 정책 — reliability(잃은 메시지를 재전송할지), history depth(메시지를 몇 개 쌓을지), durability(늦게 합류한 쪽이 지난 메시지를 받을지), deadline(메시지 사이 허용 최대 간격), liveliness(죽은 퍼블리셔를 어떻게 감지할지). 각각 25.5에서 설명한다. 손실을 감수하는 30 Hz 카메라 스트림과 떨어뜨리면 안 되는 명령 채널이 같은 시스템에서 다른 전달 의미를 가질 수 있다.
- ROS가 아니라 표준에서 오는 보안 플러그인.
- 벤더 선택권 — 특정 구현이 프로젝트의 의존성이 되지 않는다.

치르는 것:

- **QoS가 새로운 실패 경로다.** 두 노드는 QoS가 호환될 때만 연결된다. 불일치하면 퍼블리셔와 서브스크라이버가 둘 다 멀쩡해 보이면서 메시지를 한 개도 주고받지 않는다. ROS 2에서 가장 흔한 "그냥 조용한" 버그이고, [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]]에서 해부한다.
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

그리고 배포판 본체. 공식 문서는 update와 install 사이에 upgrade를 끼워 넣는데, 장식이 아니다. 낡은 우분투 위에 큰 ROS 패키지 묶음을 설치하면 의존성 충돌을 부른다. (아래의 `noble-updates` 주의는 별개로 `ros-dev-tools` 설치에 관한 것이다.) `desktop`은 RViz와 데모, 튜토리얼을 포함하고, `ros-base`는 GUI 도구 없는 같은 통신 계층으로 로봇에 올리는 쪽이다.

```bash
sudo apt update
sudo apt upgrade
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

> **source의 정의.** setup 파일을 **source**한다는 것은 *셸 하나에 가하는 조작*이다. `source`는 파일의 명령을 자식 프로세스가 아니라 지금 셸 안에서 실행하므로, 그 파일이 export하는 `PATH`, `AMENT_PREFIX_PATH` 같은 변수가 그 셸의 환경을 바꾼다. 조건은 셋이다. **지금 셸에만** 작용한다. 그 효과는 **그 셸에서 그 뒤에 시작된 프로세스에게만** 간다. 프로세스는 시작하는 순간 부모 환경의 사본을 받고, 그 뒤의 변화는 보지 못하기 때문이다. 그리고 **쌓인다**. source한 워크스페이스마다 앞서 설정된 경로 앞에 자기 경로를 붙인다([[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]의 오버레이).
>
> $$\text{env}(c)=\text{env}(\text{parent of }c)\ \text{at the moment }c\text{ starts}$$
>
> $c$는 아무 프로세스다. 그래서 한 터미널에서 export한 변수는 그 터미널이 그 뒤에 띄우는 프로세스에만 있고, 다른 어느 터미널에도 없다.
>
> - **예**: P6의 camera, controller, logger를 손으로 띄우면 터미널 셋이 들고, 터미널마다 따로 `source /opt/ros/jazzy/setup.bash`가 필요하다. 노드 $3$개에 source $3$번, 그리고 `ros2 topic list`를 칠 터미널에 $4$번째.
> - **비예**: `bash /opt/ros/jazzy/setup.bash`. 오류 없이 끝나지만 쓸 수 있는 것은 아무것도 바뀌지 않는다. export는 이미 끝나 버린 자식 셸에서 일어났으므로 다음 명령은 여전히 `ros2: command not found`라고 답한다(11절). 한 탭에서 source하고 다른 탭에서 일해도 똑같이 실패한다. 11절이 코드보다 `printenv`를 먼저 보는 이유다.

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

짧은 움직임은 시뮬레이터 안의 타이머이고, 그 숫자는 한 번 읽어 둘 만하다. 화살표를 한 번 누를 때마다 `geometry_msgs/msg/Twist`가 하나 발행된다. 위 화살표라면 `linear.x` $=2.0$이고, teleop 노드의 `scale_linear` 기본값이다. `turtlesim_node`는 그것을 저장해 두었다가, 마지막 명령이 도착한 지 $1.0\,\mathrm{s}$가 넘으면 속도를 0으로 만든다. 그래서 한 번 누르면 거북이는 약 $2.0\times1.0=2.0$ 단위를 가고, 키를 누르고 있는 것은 터미널의 키 반복 속도로 여러 번 누르는 것이며, 10절의 `ros2 topic pub`가 거북이를 계속 돌게 하는 것도 기본값으로 1초에 한 번씩 다시 발행해 타임아웃을 갱신하기 때문일 뿐이다. 그것을 멈추면 거북이는 약 1초 뒤에 선다. 실제 로봇으로 옮겨 가는 세부가 둘 있다. 타이머는 명령의 *도착*에서부터, 받는 쪽의 시계로 잰다. `Twist`에는 스탬프가 없어서 끊긴 링크는 볼 수 있어도 늦은 링크는 보지 못한다. 데이터가 얼마나 묵었는지 알려면 스탬프가 있는 메시지가 필요하다([[04-robotics/ros2/debugging-data-reproducibility|25.10 §3]]). 그리고 그 길이는 설계로 정하는 숫자다. P6에서 같은 보호 장치는 $70\,\mathrm{ms}$ 예산, 곧 제어 틱 $14$개이고, turtlesim에서 빌려 온 1초 타임아웃이라면 카트는 아무도 더는 보내지 않는 명령으로 $200$틱을 달린다.

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
6. 터미널 4를 `ros2 topic hz /turtle1/pose`로 되돌린 뒤, `echo`와 `hz`를 살려 둔 채 turtlesim을 Ctrl+C로 끈다. 둘 다 죽지 않는다: pose를 보던 `hz`는 조용해지고(turtlesim이 내던 토픽), `/turtle1/cmd_vel`을 보던 `echo`는 계속 돈다(그 토픽은 turtlesim이 아니라 teleop이 낸다). turtlesim을 다시 띄우면 `hz`가 재개된다. 1절의 세 번째 항목이 눈앞에서 증명된 것이다.

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
| 다시 빌드한 노드가 옛 코드로 돎 | 이 셸에서 워크스페이스 overlay를 source하지 않음(또는 이 셸이 `install/setup.bash`를 source한 뒤에야 패키지를 처음 빌드함) | `ros2 pkg prefix <pkg>` — 워크스페이스가 아니라 `/opt/ros/jazzy`를 가리킴 |

들일 습관: ROS 2 시스템이 불가능한 동작을 하면, 소스를 읽기 *전에* 그 불가능한 동작을 하는 셸의 환경부터 확인한다. `printenv | grep -i ros`는 2초면 끝난다. 셋째·넷째 행의 오버레이 사례는 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]의 주제다.

### 12. 이 페이지가 다루지 않는 것

직접 노드를 쓰는 것은 [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]. 요청–응답, 장시간 목표, 설정, 결정적 기동은 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. 자기 패키지를 빌드·설치하고 여러 노드를 한 번에 띄우는 것은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages and Launch]]. `ros2 topic info --verbose`가 찍는 QoS, 어느 콜백이 도는지 정하는 executor, 시뮬레이션 시간과 벽시계 시간은 [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]]와 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]. 시뮬레이션, 내비게이션, 매니퓰레이션, 하드웨어 인터페이스는 그 위에 있고 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- ROS 2 Jazzy 문서 — Installation: Ubuntu (deb packages); Configuring your ROS 2 environment; Using turtlesim, ros2 and rqt; Understanding nodes; Understanding topics.
- ROS 2 Jazzy 문서 — Concepts: Discovery; Different ROS 2 middleware vendors; ROS 2 Security; Understanding real-time programming.
- ROS 2 Jazzy 문서 — Concepts: [The ROS_DOMAIN_ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html)(기본 도메인 0, 안전한 범위, 그리고 4절이 식으로 적은 포트 계산기); [Internal ROS interfaces](https://docs.ros.org/en/jazzy/Concepts/Advanced/About-Internal-Interfaces.html)(클라이언트 라이브러리 → `rcl` → `rmw` → 구현); How-to guides: [Working with multiple RMW implementations](https://docs.ros.org/en/jazzy/How-To-Guides/Working-with-multiple-RMW-implementations.html)(`RMW_IMPLEMENTATION`).
- ROS 2 Jazzy 문서 — Releases(배포판 및 EOL 표).
- Open Robotics, "ROS Noetic End-of-Life: May 31, 2025" (ROS Discourse 공지).
- Gazebo 문서 — ROS 설치 / ROS 2와 Gazebo 버전 짝.
- `ros/ros_tutorials`(jazzy 브랜치) — turtlesim `src/turtle.cpp`(마지막 명령이 도착하고 1.0 s 뒤 속도를 0으로)와 `tutorials/teleop_turtle_key.cpp`(키 한 번에 `Twist` 하나, `scale_linear` 기본 2.0), `ros2/ros2cli`(jazzy 브랜치) — `ros2topic/verb/pub.py`(기본 발행률 1 Hz).

### 스스로 점검

1. 동료가 "ROS 2 필요 없다, 메시지 전달일 뿐이니 소켓 쓰자"고 한다. 무엇을 과소평가한 것인가?
2. `ros2 topic info /turtle1/cmd_vel`이 퍼블리셔 1, 서브스크라이버 2를 보고하는데 띄운 것은
   turtlesim과 teleop뿐이다. 두 번째 서브스크라이버는 누구인가?
3. 첫 터미널에서 이미 했는데 두 번째 터미널도 `source /opt/ros/jazzy/setup.bash`가
   필요한 이유는?
4. 누가 ROS 2는 실시간 시스템이라고 주장한다. 무엇을 되물어야 하나?
5. CPU를 아끼려고 P6 제어기를 $200\,\mathrm{Hz}$에서 $50\,\mathrm{Hz}$로 낮췄다. $70\,\mathrm{ms}$
   예산의 어느 항이 얼마나 바뀌고, 모터가 실제로 따르는 목표의 나이는 왜 거의 그대로인가?

> [!tip]- 정답 · Answers
> 1. 설정 없는 탐색, 언어와 팀을 가로지르는 검사 가능한 타입 체계, 연결 단위 전달 의미(QoS), 살아 있는 내성(introspection) 표면. 소켓은 문제의 쉬운 4분의 1이고, 나머지는 결국 엉성하게 다시 짜게 되는 부분이다.
> 2. 당신의 `ros2 topic echo`. CLI 내성 도구는 진짜 노드로서 그래프에 참여하고, 그래서 `rqt_graph`의 **Debug** 항목에 나타난다.
> 3. 환경 변수는 프로세스에 살고 자식에게만 상속된다. setup 파일은 실행한 그 셸에만 `PATH`, `AMENT_PREFIX_PATH`, `LD_LIBRARY_PATH`, `PYTHONPATH`를 설정한다. 그 설계의 이득은 터미널마다 다른 배포판이나 워크스페이스를 쓸 수 있다는 것이다.
> 4. 경성인가 연성인가, 어떤 마감에 대해서인가, 최악의 경우로 보였는가 평균으로만 보였는가(2절). 그다음 어떤 커널, 어떤 미들웨어와 구성, 실행 경로에서 어떤 연산을 제거했는지. apt로 설치한 ROS 2는 마감 시한을 보장하지 않는다. 공식 입장은 실시간 제약을 *염두에 두고 설계했다*는 것이고, 실시간 데모 자체가 정적 DDS API에 대한 소스 빌드를 요구한다고 문서화되어 있다.
> 5. 다음 제어 틱까지의 대기 $L_{\text{wait}}$ 하나뿐이고, 그 한계는 제어 주기다. $5\,\mathrm{ms}$ 미만에서 $20\,\mathrm{ms}$ 미만으로 커지므로 카메라·전송·계산·구동에 남는 여유가 $65$에서 $50\,\mathrm{ms}$로 줄고, 차이는 $15\,\mathrm{ms}$, 곧 예산의 $21.4\%$다. 반면 실제로 작용 중인 목표의 *나이*는 거의 그대로인데, 어느 쪽이든 $L_{\text{wait}}+L_{\text{reuse}}<T_{\text{vision}}=20\,\mathrm{ms}$이기 때문이다. $200\,\mathrm{Hz}$에서는 최대 $5\,\mathrm{ms}$ 기다린 뒤 세 틱 더 재사용되고, $50\,\mathrm{Hz}$에서는 최대 $20\,\mathrm{ms}$ 기다린 뒤 한 번 쓰인다. 빠른 루프가 실제로 사는 것은 *엔코더* 경로다. 틱마다 직접 읽어 모터를 $20\,\mathrm{ms}$가 아니라 $5\,\mathrm{ms}$마다 보정한다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**: 엔코더 $N=2048$ counts/m, 비전 $50\,\mathrm{Hz}$, 제어 $200\,\mathrm{Hz}$, 종단 예산 $70\,\mathrm{ms}$. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** 똑같은 카트 하나를 같은 런치로 같은 네트워크에 더 띄운 실험실에 대한 위 그림의 그래프: 먼저 두 카트가 모두 `ROS_DOMAIN_ID` 0에 있을 때, 그다음 카트 2를 도메인 1로 옮겼을 때. 각 제어기가 받는 `/goal` 간선마다 도착하는 주기를 적고, 도메인 경계를 점선으로 그려라. 이어서 공유한 경우에 카트 1의 다섯 줄 타임라인을, 두 카메라의 목표를 모두 올려 그려라.
2. **유도.** (a) 비전 주기와 제어 주기. (b) 엔코더 한 카운트의 $\Delta p$. (c) $70\,\mathrm{ms}$ 예산 안에 제어 샘플이 몇 개, 비전 프레임이 몇 장?
3. **해석.** 동료가 "ROS 2는 실시간이라 $70\,\mathrm{ms}$는 보장된다"고 한다. 무엇을 묻고, 카메라·제어기·로거를 *한* 프로세스에 넣으면 P6 예산이 아끼는 무엇이 무너지는가?

> [!note]- 그리는 법 · How to draw it
> - 노드는 타원, 모터는 그래프 바깥의 사각형으로 위 그림과 같다. 다만 이제 타원이 여섯이고, 공유한 경우에는 `/camera`, `/controller`, `/logger`가 같은 이름으로 둘씩이다.
> - 공유한 경우에 `/goal` 토픽은 둘이 아니라 하나로 그린다. 두 카메라가 모두 거기에 발행하고 두 제어기와 두 로거가 모두 구독한다. 각 제어기로 들어가는 화살표에 도착하는 것을 적는다. $2\times50=100\,\mathrm{Hz}$의 목표이고, 그 절반은 다른 카트 것이다.
> - 옆에 도구가 하는 말을 적는다. `ros2 node list`는 이름마다 두 번 보여 주며 정확히 같은 이름의 노드가 있다고 경고하고, `ros2 topic info /goal`은 퍼블리셔를 둘로 센다. 오류는 없다.
> - 나눈 경우에는 도메인마다 점선 경계 하나에 $0$과 $1$을 적고, 어느 경계도 가로지르는 간선이 없게 그린다. 각 제어기는 자기 카메라의 $50\,\mathrm{Hz}$만 받고, 두 그래프는 서로를 보지 못한다.
> - 엔코더는 두 경우 모두 각자의 하드웨어에서 제어기로 들어가는 짧은 *읽기* 화살표이지 토픽이 아니다.
> - 공유한 경우 카트 1의 타임라인: 위에는 $5\,\mathrm{ms}$마다 제어 틱, 아래에는 자기 카메라의 $20\,\mathrm{ms}$ 간격 목표와, 다른 카메라의 위상만큼 어긋난 카트 2의 $20\,\mathrm{ms}$ 간격 목표. 제어기는 마지막에 도착한 것을 따르므로 목표가 두 카트의 것 사이를 오간다.

> [!tip]- 정답 · Solutions
> 1. 도메인 공유: 노드 여섯에 이름 셋이 각각 두 번 쓰이고(`ros2 node list`가 같은 이름의 노드가 있다고 경고한다), `/goal` 토픽 하나에 퍼블리셔가 둘이다. 각 제어기는 두 카트의 목표를 섞어서 $2\times50=100\,\mathrm{Hz}$로 받고, 마지막에 도착한 쪽으로 간다. 오류는 없고, 타임라인에서는 카트 1의 목표가 두 흐름 사이를 오간다. 분리: 카트 2를 도메인 1에 두면 점선 경계 둘이 생기고 그것을 넘는 간선은 없다. 각 제어기는 자기 $50\,\mathrm{Hz}$만 받고, 두 그래프는 서로를 발견하지 않는다. 다른 해법은 [[04-robotics/ros2/workspaces-packages-launch|25.3]]의 네임스페이스 `/cart1/goal`, `/cart2/goal`이고, 그쪽은 두 카트를 한 `ros2 topic list`에 함께 둔다.
> 2. (a) $20\,\mathrm{ms}$, $5\,\mathrm{ms}$. (b) $1/2048\approx 0.488\,\mathrm{mm}$. (c) 제어 샘플 $14$, 비전 프레임 $3$(네 번째는 $80\,\mathrm{ms}$).
> 3. 어떤 커널, 어떤 rmw, 어떤 할당을 뺐는가. apt ROS 2는 마감을 주지 않는다. 한 프로세스면 로거 지연이나 카메라 프로세스의 죽음이 $200\,\mathrm{Hz}$ 루프를 함께 가져간다 — §1이 로봇을 나눈 이유인 독립 재시작.
