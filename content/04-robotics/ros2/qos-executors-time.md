---
title: "25.5 Quality of Service"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Predict from both ends' QoS profiles whether a publisher and a subscription connect, find the silent mismatch with one command, and size history depth, lifespan and deadline for a stream against a latency budget."
mastery-when: "Go deeper when you are tuning a DDS vendor's transport or analysing the end-to-end latency of a control chain, rather than making two nodes connect."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to recognise a QoS mismatch in a running system, fix it, and choose a stream's profile against a latency budget. Not enough to tune a DDS vendor's transport.
> **Working** — 돌아가는 시스템에서 QoS 불일치를 알아보고 고치며, 지연 예산에 맞춰 스트림의 프로파일을 고를 정도. DDS 벤더의 전송 계층을 튜닝할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]] (where middleware, DDS and `rmw` are defined) and [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]] — you should have written a publisher and a subscriber and inspected a topic with `ros2 topic info` and `ros2 topic echo`. The numbers are plant P6 of [[02-foundations/lab-plants|0.6 Lab Plants]]. Everything here runs on **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, the baseline of [[04-robotics/ros2/index|25. ROS 2]]; no workspace is needed, and the exercise runs from the command line.
> [[04-robotics/ros2/what-ros2-is|25.1 ROS 2란 무엇이고, 첫 시스템 돌리기]](미들웨어, DDS, `rmw`를 정의한다)와 [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]] — 퍼블리셔와 서브스크라이버를 한 번씩 써 봤고 `ros2 topic info`와 `ros2 topic echo`로 토픽을 살펴봤다고 가정한다. 숫자는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P6이다. 기준 환경은 Ubuntu 24.04의 **ROS 2 Jazzy Jalisco**. 워크스페이스는 필요 없고, 실습은 커맨드라인에서 돌아간다.

> [!note] First pass · 처음이라면
> Read the picture, then §3 (the request-versus-offered rule every connection obeys) and §7 (the one command that prints both profiles), then the Worked case — it sits after §7 because it uses all of §2–§5. §2's policy table and §5's profile table are reference you come back to; §4 is the one warning you might get, §6 the code, and §8 the fifteen-minute exercise that makes §3 stick. §1 says why the page exists and §9 where the rest lives.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], the 1-D cart and its clock, seen as one edge of its graph: `/goal`, from the camera node to the timer-driven controller of [[04-robotics/ros2/nodes-topics-messages|25.2]]. P6 freezes the rates and the budget; the two QoS profiles are this page's own.

| Symbol | Value | What it is here |
|---|---|---|
| $T_{\text{vision}}$ | $20\,\mathrm{ms}$ ($50\,\mathrm{Hz}$) | the camera publishes one goal on `/goal` per period |
| $T_{\text{ctrl}}$ | $5\,\mathrm{ms}$ ($200\,\mathrm{Hz}$) | the controller's timer, which acts on the newest goal it holds |
| $B$ | $70\,\mathrm{ms}$ | end-to-end budget, camera mid-exposure to applied force |
| offered | best effort, keep last 5, volatile, deadline $40\,\mathrm{ms}$ | the camera's publisher — **page-local** |
| requested | reliable, keep last 10, volatile, deadline $40\,\mathrm{ms}$ | the controller's subscription before the fix — **page-local** |

One fact about `/goal` decides §5's choice of profile for it: it is a stream of set-points, each replacing the one published $20\,\mathrm{ms}$ before, so a lost sample costs $20\,\mathrm{ms}$ of freshness and the next one repairs it. It is called a goal, but it behaves like a sensor.

*Scope: this page teaches Quality of Service — the policies, the rule that decides whether two endpoints connect, the one warning and the one command, the predefined profiles, and how to size depth, lifespan and deadline against P6's budget. It does not teach what runs your callbacks or which clock stamps a message — executors, callback groups, `use_sim_time` — which are [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]]; nor per-topic QoS overrides for recording, which are [[04-robotics/ros2/debugging-data-reproducibility|25.10]].*

### The picture: one P6 edge, its two profiles, and its queue during a pause

<svg viewBox="0 0 560 416" style="max-width:100%;height:auto" role="img" aria-label="Top: the /goal edge from /camera to /controller with the offered and requested QoS profiles stacked on the arrow; only the reliability pair, best effort offered against reliable requested, is crossed. Bottom: ten goals stamped 20 to 200 ms arrive while the controller takes nothing for 200 ms; a depth-5 window keeps the newest five, aged 80, 60, 40, 20 and 0 ms, and only the 80 ms one crosses the 70 ms budget line.">
  <defs><marker id="q5eopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="q5esol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">One edge, both profiles, as ros2 topic info --verbose prints them</text>
  <ellipse cx="54" cy="124" rx="42" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="54" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="500" cy="124" rx="52" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <line x1="96" y1="124" x2="446" y2="124" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#q5eopen)"/>
  <text x="124" y="118" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <rect x="150" y="32" width="206" height="84" rx="4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="currentColor" fill-opacity="0.04"/>
  <text x="159" y="47" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">offered by /camera</text>
  <text x="159" y="62" font-size="11" fill-opacity="0.95" font-weight="bold" fill="currentColor">reliability</text>
  <text x="238" y="62" font-size="11" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">BEST_EFFORT</text>
  <text x="159" y="75" font-size="11" fill-opacity="0.7" fill="currentColor">history</text>
  <text x="238" y="75" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">KEEP_LAST (5)</text>
  <text x="159" y="88" font-size="11" fill-opacity="0.7" fill="currentColor">durability</text>
  <text x="238" y="88" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">VOLATILE</text>
  <text x="159" y="101" font-size="11" fill-opacity="0.7" fill="currentColor">deadline</text>
  <text x="238" y="101" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">40 ms</text>
  <text x="159" y="114" font-size="11" fill-opacity="0.7" fill="currentColor">liveliness</text>
  <text x="238" y="114" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">AUTOMATIC</text>
  <rect x="150" y="132" width="206" height="84" rx="4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="currentColor" fill-opacity="0.04"/>
  <text x="159" y="147" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">requested by /controller</text>
  <text x="159" y="162" font-size="11" fill-opacity="0.95" font-weight="bold" fill="currentColor">reliability</text>
  <text x="238" y="162" font-size="11" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">RELIABLE</text>
  <text x="159" y="175" font-size="11" fill-opacity="0.7" fill="currentColor">history</text>
  <text x="238" y="175" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">KEEP_LAST (10)</text>
  <text x="159" y="188" font-size="11" fill-opacity="0.7" fill="currentColor">durability</text>
  <text x="238" y="188" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">VOLATILE</text>
  <text x="159" y="201" font-size="11" fill-opacity="0.7" fill="currentColor">deadline</text>
  <text x="238" y="201" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">40 ms</text>
  <text x="159" y="214" font-size="11" fill-opacity="0.7" fill="currentColor">liveliness</text>
  <text x="238" y="214" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">AUTOMATIC</text>
  <line x1="364.5" y1="152.5" x2="375.5" y2="163.5" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <line x1="364.5" y1="163.5" x2="375.5" y2="152.5" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <path d="M358 58H370V149" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="2 2" fill="none"/>
  <text x="382" y="156" font-size="11" fill-opacity="0.9" fill="currentColor">reliable requested,</text>
  <text x="382" y="169" font-size="11" fill-opacity="0.9" fill="currentColor">best effort offered:</text>
  <text x="382" y="182" font-size="11" fill-opacity="0.75" fill="currentColor">no connection, no error</text>
  <text x="12" y="244" font-size="12" fill-opacity="0.8" fill="currentColor">The queue during a 200 ms pause, after the fix: subscriber KEEP_LAST (5)</text>
  <rect x="26" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="48" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">20</text>
  <rect x="76" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="98" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">40</text>
  <rect x="126" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="148" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">60</text>
  <rect x="176" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="198" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">80</text>
  <rect x="226" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="248" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">100</text>
  <rect x="276" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="298" y="286" font-size="11" text-anchor="middle" fill="currentColor">120</text>
  <rect x="326" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="348" y="286" font-size="11" text-anchor="middle" fill="currentColor">140</text>
  <rect x="376" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="398" y="286" font-size="11" text-anchor="middle" fill="currentColor">160</text>
  <rect x="426" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="448" y="286" font-size="11" text-anchor="middle" fill="currentColor">180</text>
  <rect x="476" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="498" y="286" font-size="11" text-anchor="middle" fill="currentColor">200</text>
  <rect x="272" y="264" width="252" height="36" rx="5" stroke="currentColor" stroke-width="2" stroke-opacity="0.9" fill="none"/>
  <text x="398" y="259" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">kept: the subscription's depth 5 (stamps in ms)</text>
  <text x="26" y="259" font-size="11" fill-opacity="0.6" fill="currentColor">dropped silently (ages 100–180 ms)</text>
  <line x1="266" y1="304" x2="30" y2="304" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" fill="none" marker-end="url(#q5esol)"/>
  <text x="148" y="318" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">pushed out, oldest first</text>
  <text x="298" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" font-weight="bold" fill="currentColor">80 ms</text>
  <rect x="291" y="318" width="14" height="72" fill="currentColor" fill-opacity="0.45" stroke="none"/>
  <rect x="291" y="318" width="14" height="72" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="348" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">60 ms</text>
  <rect x="341" y="318" width="14" height="54" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="341" y="318" width="14" height="54" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="398" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">40 ms</text>
  <rect x="391" y="318" width="14" height="36" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="391" y="318" width="14" height="36" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="448" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">20 ms</text>
  <rect x="441" y="318" width="14" height="18" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="441" y="318" width="14" height="18" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="498" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">0 ms</text>
  <line x1="26" y1="381" x2="520" y2="381" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" stroke-dasharray="6 3" fill="none"/>
  <text x="270" y="376" font-size="11" text-anchor="end" fill-opacity="0.9" fill="currentColor">70 ms budget</text>
  <text x="298" y="404" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">↑ delivered first</text>
  <text x="520" y="404" font-size="11" text-anchor="end" fill-opacity="0.6" fill="currentColor">age when the controller resumes</text>
</svg>

P6's `/goal` edge, from the $50\,\mathrm{Hz}$ camera to the controller on its $5\,\mathrm{ms}$ timer. On top, both QoS profiles as `ros2 topic info --verbose` prints them, with one crossed line out of five — `BEST_EFFORT` offered against `RELIABLE` requested, which gives no connection and no error. Below, the same edge after the controller adopts the sensor-data profile, `KEEP_LAST (5)`: of the ten goals published while the controller takes nothing for $200\,\mathrm{ms}$, the newest five survive, aged $80$, $60$, $40$, $20$ and $0\,\mathrm{ms}$, and only the $80\,\mathrm{ms}$ one is past the $70\,\mathrm{ms}$ budget.

### 1. Why this page exists

Most ROS 2 problems announce themselves. A wrong topic name gives you an empty `ros2 topic echo`. A missing package gives you an error. A type mismatch refuses to build.

Three mechanisms do not announce themselves. This page is the first of them; the other two — a callback that blocks its own executor, and a node reading the wrong clock — are [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]].

- **QoS.** A publisher and a subscriber on the same topic with the same type do not connect, because their delivery policies are incompatible. Both processes are healthy. Both appear in `ros2 node list`. No message is ever exchanged.

The symptom is "nothing happens". The cure is knowing that the mechanism exists and having one command for it — here `ros2 topic info --verbose`, §7.

On P6 the silence has a size. When the two ends of `/goal` disagree on a policy that must match (§3), the camera still publishes $50$ goals a second and the controller receives none of them, while its timer goes on firing $200$ times a second on the last goal it held, or on none. A minute of that fault is $60\times200=12\,000$ control ticks without a fresh goal, and not one line in any log. The page's two P6 questions follow in that order: whether `/goal` connects at all (§3, checked with §7's command), and, once it does, how old a goal may be when the controller acts on it, which the Worked case settles against the $70\,\mathrm{ms}$ budget.

### 2. The QoS policies

*In one sentence:* each publisher and each subscriber carries its own short list of delivery settings — how many messages to keep, whether to resend lost ones, whether to save the last one for latecomers, how long a message stays worth delivering, how often one must arrive — and this section lists them and what each one controls.

*If you need only one thing from this section:* a profile belongs to one end, not to the topic, and its depth and lifespan decide what a paused subscriber is handed — P6's controller at depth $5$ through a $200\,\mathrm{ms}$ pause keeps goals aged $80$ to $0\,\mathrm{ms}$, and a $70\,\mathrm{ms}$ lifespan lets only the $4$ inside the budget through; it is worked in the *QoS profile, defined* box below.

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

Every non-duration policy also accepts *system default*, which defers to the middleware, and every duration policy accepts *default*, an unspecified duration that middleware usually treats as infinite. Reliability and history are a network's two old answers to a lost packet — resend until acknowledged, or keep only the freshest — priced on P6's goal in [[02-foundations/tools/computer-networks|12.5 Computer Networks §5–§6]], and a keep-last history is the drop-oldest bounded buffer of [[02-foundations/tools/concurrency|12.8 Concurrency §6]].

> **QoS profile, defined.** A **QoS profile** is a *set of policy values attached to one endpoint* — a publisher, subscription, service server or client. Three defining conditions. It gives **every policy one value**, defaults filling any you omit. It **belongs to one endpoint, not to a topic**, so each end of `/goal` carries its own. And each end sets it **independently**: history, depth and lifespan are never compared across the pair, while the other five must agree (§3). The first three obey one rule for a subscription that takes nothing for a time $D$:
>
> $$n_{\text{kept}}=|K|=\min\!\Big(N,\ \frac{D}{T}\Big),\qquad n_{\text{cb}}=\#\{\,k\in K:\ t-t_k\le\ell\,\}$$
>
> where $N$ is its *keep last* depth, $T$ the publisher's period, $K$ the samples kept, $t-t_k$ a sample's age, $\ell$ the lifespan and $n_{\text{cb}}$ how many reach the callback; each arrival past the $N$-th pushes out the oldest.
>
> - **Example**: P6's controller at $N=5$ through the Worked case's $200\,\mathrm{ms}$ pause keeps $\min(5,10)=5$ goals, aged $80$ to $0\,\mathrm{ms}$, and with $\ell=70\,\mathrm{ms}$, $n_{\text{cb}}=4$.
> - **Non-example**: the camera's `KEEP_LAST (5)` read as the depth of `/goal`. A controller that fixed only its reliability, keeping `KEEP_LAST (10)`, would hold all $10$, the oldest $180\,\mathrm{ms}$ old and $110\,\mathrm{ms}$ past the budget: one end's profile says nothing about the other's, so read both (§7).

Deadline, lifespan and liveliness are the three most people never set, and deadline and liveliness are the only policies that can tell you a stream has *stopped* (lifespan expires stale samples but raises no event): a deadline gives the subscription a *requested deadline missed* event, a liveliness lease gives it a *liveliness changed* event when a publisher dies quietly. Without them, a dead sensor and a slow sensor look identical. A concrete case: a 30 Hz camera sends a frame every 33 ms; if the publisher offers and the subscription requests a 40 ms deadline, the subscription gets a *requested deadline missed* event whenever more than 40 ms pass without a frame.

> **Deadline and liveliness, defined.** Both are *timing contracts between a publisher and its subscriptions*, offered, requested and matched by §3's rule. A broken one raises an **event** at each end, seen only through a callback you register — never an error or a lost connection. **Deadline** has two conditions: a **promised maximum gap** $T_{\text{dl}}$ between consecutive messages, and an **event** (*requested* or *offered deadline missed*) whenever a gap exceeds it. **Liveliness** has two: a **kind** — *automatic*, renewed whenever any publisher of the node publishes, or *manual by topic*, renewed only when this publisher asserts it — and a **lease** $T_{\text{lease}}$, past which the ends get *liveliness changed* and *liveliness lost*.
>
> $$\text{miss}_k\iff t_{k+1}-t_k>T_{\text{dl}},\qquad \text{alive}(t)\iff t-t_{\text{renew}}\le T_{\text{lease}}$$
>
> where $t_k$ is when message $k$ was sent (publisher side) or received (subscription side) and $t_{\text{renew}}$ the last renewal: deadline watches the data, liveliness the writer.
>
> - **Example**: P6's camera every $20\,\mathrm{ms}$ against $T_{\text{dl}}=40\,\mathrm{ms}$: $20\le40$, no event; a $200\,\mathrm{ms}$ camera stall exceeds $40$ and raises one.
> - **Non-example**: the controller's own $200\,\mathrm{ms}$ pause in the Worked case: the gaps stay $20\,\mathrm{ms}$, so nothing fires, because neither contract watches the consumer. And P6's profiles set no lease, so the lease stays *default*, usually infinite, and liveliness is never lost. A stopped stream is reported only if you set these durations.

**Worked: P6's camera versus the $70\,\mathrm{ms}$ budget.** Vision at $50\,\mathrm{Hz}$ is a $20\,\mathrm{ms}$ period; a healthy camera therefore meets a $40\,\mathrm{ms}$ deadline on `/goal`. A $200\,\mathrm{ms}$ stall misses it and fires *requested deadline missed*. Separately, camera *best effort* against a controller that requests *reliable* does not connect at all — `ros2 topic echo` still prints, because `echo` adapts, while the node never runs. Fixing QoS still leaves a $200\,\mathrm{ms}$ stamp inside a $70\,\mathrm{ms}$ budget: $130\,\mathrm{ms}$ over, force applied to a goal the cart has already rolled past ([[02-foundations/lab-plants|0.6]], arithmetic on [[04-robotics/robot-systems-deployment|10]]). The problem set is this pair: incompatible reliability, then a late stamp after QoS is fixed.

### 3. Compatibility: the request-versus-offered rule

This is the rule to memorise, because everything in section 4 follows from it.

> A subscription **requests** a profile: the *minimum quality* it will accept. A publisher **offers** a profile: the *maximum quality* it can provide. A connection is made only if **every** policy of the request is no more stringent than the corresponding offer.

Compatibility is per-pair and independent of who else is on the topic: one publisher can serve several subscriptions with different requested profiles, and the presence of a third node changes nothing.

> **QoS compatibility, defined.** **Compatibility** is a *property of one publisher–subscription pair*: a yes-or-no predicate on their two profiles, blind to every other endpoint on the topic. Three defining conditions. Five policies are **ordered by strictness**: best effort below reliable, volatile below transient local, automatic below manual by topic, and for deadline and lease duration the *shorter* duration is stricter, *default* counting as infinite. The request must be **no stricter than the offer on all five at once**, so one failure refuses the pair. And history, depth and lifespan are **never compared**.
>
> $$\mathrm{match}(o,r)=[r_{\text{rel}}\preceq o_{\text{rel}}]\wedge[r_{\text{dur}}\preceq o_{\text{dur}}]\wedge[r_{\text{live}}\preceq o_{\text{live}}]\wedge[r_{\text{dl}}\ge o_{\text{dl}}]\wedge[r_{\text{lease}}\ge o_{\text{lease}}]$$
>
> where $o$ is the offered (publisher) profile, $r$ the requested (subscription) one and $\preceq$ "no stricter than"; durations compare the other way because a longer promised gap is a weaker promise, so a default publisher fails any subscription that names a deadline ($x\ge\infty$ is false).
>
> - **Example**: P6's `/goal` before the fix fails the first bracket, reliable $\not\preceq$ best effort, and nothing is ever delivered. After it all five hold: best effort, volatile and automatic at both ends, $40\ge40\,\mathrm{ms}$, and $\infty\ge\infty$ for the lease neither end sets.
> - **Non-example**: the pre-fix depths, `KEEP_LAST (5)` offered against `KEEP_LAST (10)` requested. They differ in `--verbose` and draw the eye, but depth is not in the predicate: they neither block the pair nor explain its failure. A false predicate raises no error, so reading these five lines is the whole diagnosis.

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

One correction to the folklore, because it matters when you are hunting: this failure is not *completely* invisible. Both rclcpp and rclpy register a default handler for the incompatible-QoS event, and it logs a warning once, at discovery, on the node's own logger. The wording differs by client library; this is rclpy's:

```text
[WARN] [...] [my_subscriber]: New publisher discovered on topic '/image', offering incompatible QoS. No messages will be received from it. Last incompatible policy: RELIABILITY
```

An rclcpp subscriber says "No messages will be sent to it" and names the policy `RELIABILITY_QOS_POLICY`, so grep for `incompatible QoS` rather than the whole sentence.

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

**Sensor data** is the one you will reach for and the one that creates most mismatches, because it changes reliability. Use it when the consumer wants the latest sample as soon as it is captured and can tolerate losing some: camera frames, lidar scans, IMU. Do not use it for a topic whose messages are individually meaningful — sent once, or not made irrelevant by the next one: a one-shot goal such as a navigation target, an emergency stop, a mode change. The test is whether the next message makes a lost one irrelevant. P6's `/goal` passes it despite its name: a $50\,\mathrm{Hz}$ stream in which each set-point replaces the one $20\,\mathrm{ms}$ before is a sensor-like stream, and the Worked case below gives it this profile for that reason.

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

This is the command. Plain `ros2 topic info` gives you counts; `--verbose` (or `-v`) prints, for every publisher and every subscription on the topic, the node name, namespace, type, type hash, GID (the globally unique ID the middleware gives each publisher and subscription) and the full QoS profile:

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

One CLI behaviour will mislead you. `ros2 topic echo` defaults to the sensor-data profile but then *inspects the publishers and adapts*: if every publisher offers reliable it requests reliable, if any is best effort it falls back to best effort, and the same for transient local. It prints a note only in the *mixed* case — "Some, but not all, publishers are offering…" — so when every publisher is best effort it adapts in silence. Absence of a note is not evidence that it did not adapt. So **`ros2 topic echo` will usually show you data on a topic your own node cannot receive** — a feature for inspection, a trap for diagnosis. To make `echo` behave like your node, pin the policy yourself:

```bash
ros2 topic echo /image --qos-reliability reliable   # now it fails the same way your node does
```

`ros2 topic pub` has the same family of flags (`--qos-profile`, `--qos-reliability`, `--qos-durability`, `--qos-depth`, `--qos-history`, `--qos-liveliness`) and defaults to the `default` profile with no adaptation.

### Worked case: how deep a queue P6 needs, and what a 200 ms pause does to it

Everything in §2–§5, on P6's `/goal`. The two periods first, because every count below is one of them divided into the pause:

$$T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=20\,\mathrm{ms},\qquad T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=5\,\mathrm{ms}$$

and the event is this: the controller takes no messages for $D=200\,\mathrm{ms}$, from $t=0$ to $t=200\,\mathrm{ms}$, because one of its callbacks runs that long and nothing else in its node runs meanwhile — why, and how to stop it, is [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]. The camera is healthy throughout and publishes at $20, 40, \ldots, 200\,\mathrm{ms}$.

**Step 1 — what accumulates.** During the pause the publisher emits

$$n=\frac{D}{T_{\text{vision}}}=\frac{200}{20}=10\ \text{samples},\qquad \frac{D}{T_{\text{ctrl}}}=\frac{200}{5}=40\ \text{control firings lost}$$

so ten goals arrive with nobody to take them, and forty commands are never sent. Neither number appears in any log.

**Step 2 — what survives, under the profile the fix in step 7 gives you.** Messages are not queued at the client-library level; they sit in the middleware under the *subscription's* history, so it is the controller's own depth that decides this, not the camera's. Take the controller after it has adopted the sensor-data profile of §5 to match the best-effort camera — that profile is `KEEP_LAST (5)`. It is the right family of profile for this topic and not a breach of §5's rule, because `/goal` is a stream in which each set-point replaces the one $20\,\mathrm{ms}$ before it; a navigation goal sent once would be the case the rule forbids. Each arrival past the fifth pushes out the oldest, so five of the ten are discarded before your code exists to see them. At $t=200\,\mathrm{ms}$ the survivors are the samples stamped $120,140,160,180,200$, whose ages are

$$200-\{120,140,160,180,200\}=\{80,60,40,20,0\}\ \mathrm{ms}$$

because age is just the elapsed time since the stamp. The five dropped ones had ages $100$ through $180\,\mathrm{ms}$.

**Step 3 — the order they come out in, which is the part that hurts.** From one publisher the survivors are delivered in publication order, so the first callback after the pause is handed the **oldest** survivor, at $80\,\mathrm{ms}$, and the freshest goal is the fifth callback you run. (The executor's round-robin, [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]], is about which *topic* an overloaded executor services next, not about the order of samples within one.) So the controller's first action after recovering is to steer towards a goal that is older than its entire $70\,\mathrm{ms}$ budget.

**Step 4 — score the survivors against the budget.** Of $\{80,60,40,20,0\}\,\mathrm{ms}$, exactly four are at or under $70\,\mathrm{ms}$ and one is not. So a depth of five bought one guaranteed-useless callback and three extra old ones, to deliver the single sample — the $0\,\mathrm{ms}$ one — that the controller actually wanted. Set the depth to 1 and nine samples are dropped instead of five, the callback runs once, and it runs on the newest goal. **For a control input, a deep queue is not a safety margin; it is a backlog you will have to throw away with the motor still moving.** Depth belongs to streams where every sample matters — a bag recorder, a counter, an integrator — not to "where should I go now".

**Step 5 — make the middleware do the age check.** Lifespan is the policy for this, and it is the one most people never set: a sample older than the lifespan is stale, and expired samples are dropped silently and never received. Set `lifespan` to the budget itself, $70\,\mathrm{ms}$, and the $80\,\mathrm{ms}$ survivor never reaches your callback at all — the four inside the budget do. You have moved a check you would otherwise write in every callback into the profile, where `ros2 topic info --verbose` can show it to a colleague.

**Step 6 — and what the deadline does not tell you here.** The camera offers a $40\,\mathrm{ms}$ deadline and the controller requests $40\,\mathrm{ms}$, which is compatible since the request is no more stringent than the offer, and a healthy P6 camera publishing every $20\,\mathrm{ms}$ meets it with $20\,\mathrm{ms}$ to spare. During this pause it goes on meeting it, on every interval, and no *requested deadline missed* event is raised — the camera published on time and the middleware received on time. Deadline watches the gap between messages on the topic; it cannot see that your controller stopped taking them. The gap in the problem set is the other one, where the camera itself goes quiet for $200\,\mathrm{ms}$: there the deadline does fire, and the first frame afterwards carries a stamp $200\,\mathrm{ms}$ old, which is $130\,\mathrm{ms}$ past a budget of $70$. Two failures, the same duration, and only one of them has an event to tell you about it.

**Step 7 — none of which happens if the reliability line is crossed.** Read the top panel of the picture above again. Camera offering best effort against a controller requesting reliable never connects, so the count in step 1 is not ten, it is zero, forever, with both nodes healthy. Rule that out first with `ros2 topic info /goal --verbose`, then reason about depth.

### 8. Exercise: break a topic with QoS, then fix it

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

5. Now the durability half. Publish one latched message and **leave the publisher running** — transient local is held in the publisher's own history, so when the process exits the retained sample goes with it. `--once` would exit; use a repeating publish and keep the terminal open:

```bash
ros2 topic pub /demo_latched std_msgs/msg/String "{data: the-map}" --qos-durability transient_local --qos-depth 1 --rate 0.2
```

Then, from another terminal *while that one is still running*, subscribe first with the default volatile request and then with transient local. The volatile subscriber sees only messages published after it joins; the transient local one is handed the retained sample immediately:

```bash
ros2 topic echo /demo_latched --qos-durability volatile          # waits for the next one
ros2 topic echo /demo_latched --qos-durability transient_local   # the retained message arrives at once
```

You are done when you can say, without looking, which of the four reliability combinations and which of the four durability combinations fail to connect.

### 9. What this page does not cover

What runs your callbacks, what happens to the rest of a node when one of them blocks, and which clock stamps a message — executors, callback groups and `use_sim_time` — are the other two silent failures, on [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]]. Per-topic QoS overrides for recording and replay, and the ordered set of checks to run when a system misbehaves, are [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]. DDS vendor tuning (buffer sizes, multicast, shared-memory transports) is in the vendor's documentation, not in ROS 2's. Intra-process communication and composition, which let nodes in one process pass messages without serialising them through the middleware, are the ROS 2 composition documentation.

### After reading · 읽고 나면

- State the request-versus-offered rule, and apply it to reliability, durability, deadline and liveliness without the tables.
- Find a mismatch with `ros2 topic info --verbose`, and say why `ros2 topic echo` printing data proves nothing about your node.
- Choose a predefined profile for a topic, and decide whether best effort suits something called a goal by asking whether the next message makes a lost one irrelevant.
- Size history depth and lifespan for a control input against a latency budget, and say why a deep queue is a backlog.
- Say which silent failure a deadline event can report and which it cannot.

### Self-check

1. A publisher offers reliable and a subscription requests best effort. Do they connect, and
   why is the reverse case different?
2. Your node subscribes to `/map` and never receives anything, but `ros2 topic echo /map`
   prints a map immediately. What is going on?
3. P6's controller takes no messages for $200\,\mathrm{ms}$ while the $50\,\mathrm{Hz}$
   camera keeps publishing. With `KEEP_LAST (5)`, how many goals are lost, how old is the
   first one your callback is handed, and how many survivors are inside the
   $70\,\mathrm{ms}$ budget? Would a deadline have told you?
4. §5 says not to use the sensor-data profile for a goal, and the Worked case uses it for
   P6's `/goal`. Which is right, and what one question settles it for any topic?

> [!tip]- Answers
> 1. They connect. The request is the minimum quality the subscription will accept and the offer is the maximum the publisher can provide, so a reliable publisher over-satisfies a best-effort request. The reverse — best-effort publisher, reliable subscription — asks for a guarantee that is not on offer, so no connection is made and no message is exchanged.
> 2. Almost certainly durability. The map server publishes transient local, once, before your node started; your node requests the default volatile profile, which connects legitimately but receives only new messages. `ros2 topic echo` inspects the publishers and adapts its own request to transient local, so it gets the retained sample. Fix your subscription to request transient local, and remember that `echo` succeeding does not prove your node can.
> 3. Ten goals are published during the pause ($200/20$) and five are lost, because `KEEP_LAST (5)` keeps only the newest five and each arrival pushes out the oldest. At the instant the controller resumes the survivors are $\{80,60,40,20,0\}\,\mathrm{ms}$ old and they arrive in publication order, so the first callback is handed the $80\,\mathrm{ms}$ one — already past the budget — and the freshest goal is the fifth callback. Four of the five survivors are inside $70\,\mathrm{ms}$. No deadline event is raised: the camera published on time and the middleware received on time, so nothing on the topic missed its interval. Depth 1, or a $70\,\mathrm{ms}$ lifespan, is the fix; a deeper queue is a backlog, not a margin.
> 4. Both. The rule is about messages that are individually meaningful — sent once, or not made irrelevant by the next one — and P6's `/goal` is not one: it is a $50\,\mathrm{Hz}$ stream in which each set-point replaces the one $20\,\mathrm{ms}$ before, so a lost sample costs $20\,\mathrm{ms}$ of freshness and the next one repairs it. The question is whether the next message makes a lost one irrelevant. If it does, best effort with a shallow depth is right; if it does not — a navigation goal sent once, an emergency stop, a mode change — ask for reliable, and for something published once and needed by late joiners, transient local too.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]]. Budget $70\,\mathrm{ms}$ from camera mid-exposure to applied force. A vision message arrives $200\,\mathrm{ms}$ late. No new simulator.

1. **Draw.** The picture above for a controller that gets a different policy wrong: it requests best effort, as the camera offers, but *transient local* durability, hoping to catch a goal published before it started, while the camera offers the sensor-data profile (best effort, volatile). Cross the incompatible line. Then the lower half for the fixed controller with `KEEP_LAST (3)` instead of $5$, through the same $200\,\mathrm{ms}$ pause: which goals survive, their ages, and which, if any, are past the $70\,\mathrm{ms}$ budget.
2. **Derive.** (a) Do those QoS endpoints connect? (b) $200\,\mathrm{ms}$ versus the $70\,\mathrm{ms}$ budget — by how much is the force late if the controller still uses that stamp? (c) A deadline of $40\,\mathrm{ms}$ on `/goal`: does a healthy $50\,\mathrm{Hz}$ camera meet it? Does a $200\,\mathrm{ms}$ stall raise an event?
3. **Interpret.** `ros2 topic echo /goal` prints frames, the controller callback never runs. What is the silent failure, and why is a $200\,\mathrm{ms}$ late vision *also* a budget failure even after QoS is fixed?

> [!note]- How to draw it · 그리는 법
> - Draw the edge as two ellipses and one arrow, with two stacked boxes on the arrow instead of a label: what the camera *offers* above, what the controller *requests* below, as `ros2 topic info --verbose` prints them.
> - Write every policy line in both boxes — reliability, history, durability, deadline, liveliness — not only the one you suspect. Reliability now matches, which is exactly why the eye slides past the box.
> - Rule each pair against the tables in §3 and cross only the incompatible pair: a *volatile* offer against a *transient local* request is "No" in the durability table, because the request is stricter than the offer. One crossed line, and it is not the one crossed in the picture above.
> - Beside the crossed line, what you would see: no connection, and one warning at discovery whose last incompatible policy is durability, not reliability.
> - The lower half on a clock: ten goals published at $20\,\mathrm{ms}$ spacing while the controller takes nothing for $200\,\mathrm{ms}$, and a queue of depth $3$ that keeps only the newest.
> - Write each survivor's age when the controller wakes and draw the $70\,\mathrm{ms}$ budget as a line, so any goal older than the budget sits visibly on the wrong side of it.

> [!tip]- Solutions
> 1. Top: reliability matches, best effort at both ends; durability does not. A transient-local request against a volatile offer is incompatible (§3's durability table), so that is the one crossed line out of five, and the endpoints still do not connect, with a single discovery warning naming durability. Bottom: with depth $3$, of the ten goals published during the pause only the newest three survive, aged $40$, $20$ and $0\,\mathrm{ms}$, and none is past the $70\,\mathrm{ms}$ budget, where depth $5$ kept one $80\,\mathrm{ms}$-old goal. A shallower queue discards more, which is what a stream read only for its latest value wants.
> 2. (a) No — reliable request vs best-effort offer. (b) $130\,\mathrm{ms}$ over budget. (c) Healthy $20\,\mathrm{ms}$ period meets $40\,\mathrm{ms}$; a $200\,\mathrm{ms}$ gap misses and fires *requested deadline missed*.
> 3. Incompatible reliability; `echo` adapts, the node does not. Fixing QoS still leaves a $200\,\mathrm{ms}$ stamp inside a $70\,\mathrm{ms}$ budget — the force is applied to a goal the cart has already rolled past.

### Sources

- ROS 2 Jazzy documentation — Concepts: Quality of Service settings (policies, profiles, compatibility tables, QoS events, matched events).
- ROS 2 Jazzy documentation — Tutorials: Using quality-of-service settings for lossy networks.
- Source, Jazzy branches, for values and messages quoted verbatim: `rmw/qos_profiles.h` (profile contents), `rclcpp/subscription_base.cpp` and `publisher_base.cpp`, `rclpy/event_handler.py` (default incompatible-QoS warnings), `rclpy/topic_endpoint_info.py` (the `--verbose` output format), `ros2cli/ros2topic` (QoS flags and `echo`'s publisher-matching behaviour), `robot_state_publisher` and `nav2_map_server` (transient-local publishers).
- Source, Jazzy branches, for the definitions in §2 and §3: [`rmw_dds_common/src/qos.cpp`](https://github.com/ros2/rmw_dds_common/blob/jazzy/rmw_dds_common/src/qos.cpp) (`qos_profile_check_compatible` compares reliability, durability, deadline, liveliness and lease duration, and nothing else); [`rclpy/qos.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/qos.py) and [`rclcpp/qos.hpp`](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/qos.hpp) (policies left unset come from the default profile); [`rclcpp/subscription_base.cpp`](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/src/rclcpp/subscription_base.cpp), `publisher_base.cpp` and `rclpy/event_handler.py` (deadline and liveliness events have no default handler, only the callback you register).

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 돌아가는 시스템에서 QoS 불일치를 알아보고 고치며, 지연 예산에 맞춰 스트림의 프로파일을 고를 정도. DDS 벤더의 전송 계층을 튜닝할 정도는 아니다.
> **Working** — enough to recognise and fix a QoS mismatch and size a stream's profile, not to tune DDS transports.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/what-ros2-is|25.1 ROS 2란 무엇이고, 첫 시스템 돌리기]](미들웨어, DDS, `rmw`를 정의한다)와 [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]] — 퍼블리셔와 서브스크라이버를 한 번씩 써 봤고 `ros2 topic info`와 `ros2 topic echo`로 토픽을 살펴봤다고 가정한다. 숫자는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P6이다. 기준 환경은 [[04-robotics/ros2/index|25. ROS 2]]와 같은 Ubuntu 24.04의 **ROS 2 Jazzy Jalisco**. 워크스페이스는 필요 없고, 실습은 커맨드라인에서 돌아간다.
> 25.1 and 25.2 are assumed, with P6 from 0.6; everything runs on ROS 2 Jazzy on Ubuntu 24.04 without a workspace.

> [!note] 처음이라면 · First pass
> 그림을 보고, 3절(모든 연결이 따르는 request 대 offered 규칙)과 7절(두 프로파일을 찍어 주는 명령 하나)을 읽은 다음 대상으로 한 번 끝까지로 간다. 그것은 2–5절을 모두 쓰므로 7절 뒤에 있다. 2절의 정책 표와 5절의 프로파일 표는 돌아와서 찾아보는 참고이고, 4절은 운이 좋으면 나오는 경고 한 줄, 6절은 코드, 8절은 3절을 몸에 붙이는 15분짜리 실습이다. 1절은 이 페이지가 왜 있는지, 9절은 나머지가 어디 있는지 말한다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6** — 1차원 카트와 그 시계 — 를 그래프의 간선 하나로 본다. 카메라 노드에서 [[04-robotics/ros2/nodes-topics-messages|25.2]]의 타이머 구동 제어기로 가는 `/goal`이다. 주기와 예산은 P6이 고정하고, 두 QoS 프로파일은 이 페이지의 것이다.

| 기호 | 값 | 여기서 무엇인가 |
|---|---|---|
| $T_{\text{vision}}$ | $20\,\mathrm{ms}$ ($50\,\mathrm{Hz}$) | 카메라가 주기마다 `/goal`에 목표 하나를 발행한다 |
| $T_{\text{ctrl}}$ | $5\,\mathrm{ms}$ ($200\,\mathrm{Hz}$) | 제어기의 타이머. 들고 있는 가장 새 목표로 동작한다 |
| $B$ | $70\,\mathrm{ms}$ | 카메라 노출 중간부터 힘이 걸리기까지의 종단 간 예산 |
| 제공(offered) | best effort, keep last 5, volatile, deadline $40\,\mathrm{ms}$ | 카메라의 퍼블리셔 — **이 페이지 고유** |
| 요청(requested) | reliable, keep last 10, volatile, deadline $40\,\mathrm{ms}$ | 고치기 전 제어기의 서브스크립션 — **이 페이지 고유** |

`/goal`에 관한 사실 하나가 5절에서 이 토픽의 프로파일을 정한다. 이것은 설정점의 스트림이고, 각 메시지는 $20\,\mathrm{ms}$ 전에 발행된 것을 대체한다. 그래서 샘플 하나를 잃으면 $20\,\mathrm{ms}$어치 신선도를 잃을 뿐이고 다음 샘플이 그것을 메운다. 이름은 목표지만 센서처럼 행동한다.

*범위: 이 페이지는 서비스 품질(QoS)을 가르친다 — 정책들, 두 끝점이 연결되는지를 정하는 규칙, 경고 한 줄과 명령 하나, 미리 정의된 프로파일, 그리고 P6의 예산에 맞춰 depth, lifespan, deadline을 정하는 법. 콜백을 무엇이 돌리는지, 메시지에 어느 시계로 스탬프를 찍는지 — executor, 콜백 그룹, `use_sim_time` — 는 가르치지 않으며 그것은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에 있다. 기록용 토픽별 QoS 오버라이드는 [[04-robotics/ros2/debugging-data-reproducibility|25.10]]에 있다.*

### 그림으로 먼저 보기: P6의 간선 하나, 프로파일 둘, 그리고 정지 동안의 큐 · The picture

<svg viewBox="0 0 560 416" style="max-width:100%;height:auto" role="img" aria-label="위: /camera에서 /controller로 가는 /goal 간선 위에 제공 프로파일과 요청 프로파일을 위아래로 쌓았고, best effort 제공 대 reliable 요청인 reliability 짝에만 가위표가 있다. 아래: 제어기가 200 ms 동안 아무것도 가져가지 않는 사이 20에서 200 ms 스탬프의 목표 열 개가 도착하고, 깊이 5의 창이 가장 새 다섯(나이 80, 60, 40, 20, 0 ms)을 남기며, 70 ms 예산선을 넘는 것은 80 ms 하나뿐이다.">
  <defs><marker id="q5kopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="q5ksol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">간선 하나, 프로파일 둘 (ros2 topic info --verbose가 찍는 그대로)</text>
  <ellipse cx="54" cy="124" rx="42" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="54" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="500" cy="124" rx="52" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="500" y="128" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <line x1="96" y1="124" x2="446" y2="124" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#q5kopen)"/>
  <text x="124" y="118" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/goal</text>
  <rect x="150" y="32" width="206" height="84" rx="4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="currentColor" fill-opacity="0.04"/>
  <text x="159" y="47" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">/camera가 제공(offer)</text>
  <text x="159" y="62" font-size="11" fill-opacity="0.95" font-weight="bold" fill="currentColor">reliability</text>
  <text x="238" y="62" font-size="11" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">BEST_EFFORT</text>
  <text x="159" y="75" font-size="11" fill-opacity="0.7" fill="currentColor">history</text>
  <text x="238" y="75" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">KEEP_LAST (5)</text>
  <text x="159" y="88" font-size="11" fill-opacity="0.7" fill="currentColor">durability</text>
  <text x="238" y="88" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">VOLATILE</text>
  <text x="159" y="101" font-size="11" fill-opacity="0.7" fill="currentColor">deadline</text>
  <text x="238" y="101" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">40 ms</text>
  <text x="159" y="114" font-size="11" fill-opacity="0.7" fill="currentColor">liveliness</text>
  <text x="238" y="114" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">AUTOMATIC</text>
  <rect x="150" y="132" width="206" height="84" rx="4" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" fill="currentColor" fill-opacity="0.04"/>
  <text x="159" y="147" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">/controller가 요청(request)</text>
  <text x="159" y="162" font-size="11" fill-opacity="0.95" font-weight="bold" fill="currentColor">reliability</text>
  <text x="238" y="162" font-size="11" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">RELIABLE</text>
  <text x="159" y="175" font-size="11" fill-opacity="0.7" fill="currentColor">history</text>
  <text x="238" y="175" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">KEEP_LAST (10)</text>
  <text x="159" y="188" font-size="11" fill-opacity="0.7" fill="currentColor">durability</text>
  <text x="238" y="188" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">VOLATILE</text>
  <text x="159" y="201" font-size="11" fill-opacity="0.7" fill="currentColor">deadline</text>
  <text x="238" y="201" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">40 ms</text>
  <text x="159" y="214" font-size="11" fill-opacity="0.7" fill="currentColor">liveliness</text>
  <text x="238" y="214" font-size="11" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">AUTOMATIC</text>
  <line x1="364.5" y1="152.5" x2="375.5" y2="163.5" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <line x1="364.5" y1="163.5" x2="375.5" y2="152.5" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none"/>
  <path d="M358 58H370V149" stroke="currentColor" stroke-width="1" stroke-opacity="0.55" stroke-dasharray="2 2" fill="none"/>
  <text x="382" y="156" font-size="11" fill-opacity="0.9" fill="currentColor">reliable 요청 대</text>
  <text x="382" y="169" font-size="11" fill-opacity="0.9" fill="currentColor">best effort 제공:</text>
  <text x="382" y="182" font-size="11" fill-opacity="0.75" fill="currentColor">연결 없음, 오류도 없음</text>
  <text x="12" y="244" font-size="12" fill-opacity="0.8" fill="currentColor">200 ms 정지 동안의 큐, 고친 뒤: 구독자 KEEP_LAST (5)</text>
  <rect x="26" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="48" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">20</text>
  <rect x="76" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="98" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">40</text>
  <rect x="126" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="148" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">60</text>
  <rect x="176" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="198" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">80</text>
  <rect x="226" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="3 2" fill="none"/>
  <text x="248" y="286" font-size="11" text-anchor="middle" fill-opacity="0.5" fill="currentColor">100</text>
  <rect x="276" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="298" y="286" font-size="11" text-anchor="middle" fill="currentColor">120</text>
  <rect x="326" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="348" y="286" font-size="11" text-anchor="middle" fill="currentColor">140</text>
  <rect x="376" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="398" y="286" font-size="11" text-anchor="middle" fill="currentColor">160</text>
  <rect x="426" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="448" y="286" font-size="11" text-anchor="middle" fill="currentColor">180</text>
  <rect x="476" y="270" width="44" height="24" rx="2" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.1"/>
  <text x="498" y="286" font-size="11" text-anchor="middle" fill="currentColor">200</text>
  <rect x="272" y="264" width="252" height="36" rx="5" stroke="currentColor" stroke-width="2" stroke-opacity="0.9" fill="none"/>
  <text x="398" y="259" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">남는 것: 구독의 깊이 5 (스탬프, ms)</text>
  <text x="26" y="259" font-size="11" fill-opacity="0.6" fill="currentColor">조용히 버려짐 (나이 100–180 ms)</text>
  <line x1="266" y1="304" x2="30" y2="304" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" fill="none" marker-end="url(#q5ksol)"/>
  <text x="148" y="318" font-size="11" text-anchor="middle" fill-opacity="0.55" fill="currentColor">오래된 것부터 밀려남</text>
  <text x="298" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" font-weight="bold" fill="currentColor">80 ms</text>
  <rect x="291" y="318" width="14" height="72" fill="currentColor" fill-opacity="0.45" stroke="none"/>
  <rect x="291" y="318" width="14" height="72" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="348" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">60 ms</text>
  <rect x="341" y="318" width="14" height="54" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="341" y="318" width="14" height="54" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="398" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">40 ms</text>
  <rect x="391" y="318" width="14" height="36" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="391" y="318" width="14" height="36" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="448" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">20 ms</text>
  <rect x="441" y="318" width="14" height="18" fill="currentColor" fill-opacity="0.22" stroke="none"/>
  <rect x="441" y="318" width="14" height="18" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7" fill="none"/>
  <text x="498" y="310" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">0 ms</text>
  <line x1="26" y1="381" x2="520" y2="381" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" stroke-dasharray="6 3" fill="none"/>
  <text x="270" y="376" font-size="11" text-anchor="end" fill-opacity="0.9" fill="currentColor">70 ms 예산</text>
  <text x="298" y="404" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">↑ 먼저 전달됨</text>
  <text x="520" y="404" font-size="11" text-anchor="end" fill-opacity="0.6" fill="currentColor">제어기가 재개한 순간의 나이</text>
</svg>

P6의 `/goal` 간선, 곧 $50\,\mathrm{Hz}$ 카메라에서 $5\,\mathrm{ms}$ 타이머의 제어기로 가는 간선이다. 위에는 두 QoS 프로파일을 `ros2 topic info --verbose`가 찍는 그대로 적었고, 다섯 줄 중 가위표는 `BEST_EFFORT` 제공 대 `RELIABLE` 요청 하나뿐이며 그 결과는 연결 없음, 오류도 없음이다. 아래는 제어기가 sensor-data 프로파일 `KEEP_LAST (5)`를 받아들인 뒤의 같은 간선으로, 제어기가 $200\,\mathrm{ms}$ 동안 아무것도 가져가지 않는 사이 발행된 목표 열 개 중 가장 새 다섯이 나이 $80$, $60$, $40$, $20$, $0\,\mathrm{ms}$로 살아남고, $70\,\mathrm{ms}$ 예산을 넘는 것은 $80\,\mathrm{ms}$ 하나뿐이다.

### 1. 이 페이지가 존재하는 이유

ROS 2의 문제는 대개 스스로를 알린다. 토픽 이름을 틀리면 `ros2 topic echo`가 비고, 패키지가 없으면 오류가 나고, 타입이 어긋나면 빌드가 거부된다.

스스로를 알리지 않는 기전이 셋 있다. 이 페이지는 그 첫째이고, 나머지 둘 — 자기 executor를 막는 콜백, 엉뚱한 시계를 읽는 노드 — 은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]이다.

- **QoS.** 같은 토픽, 같은 타입인데도 전달 정책이 호환되지 않아 퍼블리셔와 서브스크라이버가 연결되지 않는다. 두 프로세스 다 멀쩡하고, `ros2 node list`에도 다 나오고, 메시지는 한 개도 오가지 않는다.

증상은 "아무 일도 일어나지 않음"이다. 처방은 이 기전이 존재한다는 것을 알고 명령 하나를 갖고 있는 것이다. 여기서는 7절의 `ros2 topic info --verbose`다.

P6에서는 그 침묵에 크기가 있다. `/goal`의 두 끝이 서로 맞아야 하는 정책(3절)에서 어긋나면, 카메라는 여전히 초당 $50$개의 목표를 발행하는데 제어기는 하나도 받지 못하고, 그 타이머는 쥐고 있던 마지막 목표로, 혹은 목표 없이 초당 $200$번씩 계속 돈다. 그 고장이 1분이면 새 목표 없는 제어 틱이 $60\times200=12\,000$번이고, 어느 로그에도 한 줄이 남지 않는다. 이 페이지가 P6에 대해 묻는 두 질문도 그 순서를 따른다. 먼저 `/goal`이 애초에 연결되는가(3절, 7절의 명령으로 확인), 그리고 연결된 뒤에는 제어기가 목표에 따라 움직이는 순간 그 목표가 얼마나 묵어도 되는가다. 뒤의 것은 대상으로 한 번 끝까지가 $70\,\mathrm{ms}$ 예산에 대어 정한다.

### 2. QoS 정책들

*한 문장으로:* 퍼블리셔와 서브스크라이버는 저마다 짧은 전달 설정 목록을 들고 있다 — 메시지를 몇 개 보관할지, 잃은 것을 다시 보낼지, 늦게 들어온 쪽을 위해 마지막 것을 남겨 둘지, 메시지가 얼마 동안 전달할 가치가 있는지, 얼마나 자주 와야 하는지 — 이 절은 그것들을 나열하고 각각이 무엇을 정하는지 적는다.

*이 절에서 하나만 가져간다면:* 프로파일은 토픽이 아니라 한쪽 끝의 것이고, 그 depth와 lifespan이 멈췄던 서브스크라이버가 무엇을 건네받을지 정한다는 것 — depth $5$인 P6 제어기가 $200\,\mathrm{ms}$ 정지를 지나면 나이 $80$에서 $0\,\mathrm{ms}$까지의 목표를 쥐고 있고, lifespan을 $70\,\mathrm{ms}$로 두면 예산 안의 $4$개만 통과한다. 아래 *QoS 프로파일의 정의* 상자에서 계산한다.

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

기간이 아닌 모든 정책에는 미들웨어에 위임하는 *system default*가 있고, 기간인 모든 정책에는 지정하지 않음을 뜻하는 *default*가 있다. 미들웨어는 보통 후자를 무한으로 해석한다. 신뢰성과 이력은 잃어버린 패킷에 대한 네트워크의 오래된 두 대답 — 확인 응답이 올 때까지 다시 보내기, 또는 가장 새것만 남기기 — 이고, P6의 목표 위에서 그 값을 매기는 곳이 [[02-foundations/tools/computer-networks|12.5 컴퓨터 네트워크 §5–§6]]이다. keep-last 이력은 [[02-foundations/tools/concurrency|12.8 동시성 §6]]의 가장 오래된 것을 버리는 유한 버퍼다.

> **QoS 프로파일의 정의.** **QoS 프로파일**은 *끝점 하나에 붙는 정책 값의 묶음*이다. 끝점은 퍼블리셔, 서브스크립션, 서비스 서버, 클라이언트 중 하나다. 정의 조건은 셋이다. **모든 정책에 값이 하나씩** 있고, 지정하지 않은 것은 기본값으로 채워진다. **토픽이 아니라 끝점 하나에 속하므로**, `/goal`의 두 끝은 각자 제 프로파일을 갖는다. 그리고 끝마다 **따로 정한다.** history, depth, lifespan은 쌍 사이에서 비교되지 않고, 나머지 다섯은 서로 맞아야 한다(3절). 앞의 셋은 시간 $D$ 동안 아무것도 가져가지 않은 서브스크립션에서 규칙 하나를 따른다.
>
> $$n_{\text{kept}}=|K|=\min\!\Big(N,\ \frac{D}{T}\Big),\qquad n_{\text{cb}}=\#\{\,k\in K:\ t-t_k\le\ell\,\}$$
>
> 여기서 $N$은 그 서브스크립션의 *keep last* 깊이, $T$는 퍼블리셔의 주기, $K$는 남은 샘플, $t-t_k$는 샘플의 나이, $\ell$은 lifespan, $n_{\text{cb}}$는 콜백까지 가는 개수다. $N$개를 넘어 도착하는 샘플마다 가장 오래된 것을 밀어낸다.
>
> - **예**: $N=5$인 P6 제어기가 대상으로 한 번 끝까지의 $200\,\mathrm{ms}$ 정지를 지나면 $\min(5,10)=5$개가 남고 나이는 $80$부터 $0\,\mathrm{ms}$까지다. $\ell=70\,\mathrm{ms}$이면 $n_{\text{cb}}=4$다.
> - **비예**: 카메라의 `KEEP_LAST (5)`를 `/goal`의 깊이로 읽는 것. reliability만 고치고 `KEEP_LAST (10)`은 그대로 둔 제어기는 $10$개를 모두 들고 있고, 가장 오래된 것은 $180\,\mathrm{ms}$ 되어 예산을 $110\,\mathrm{ms}$ 넘는다. 한쪽 끝의 프로파일은 다른 쪽에 대해 아무것도 말해 주지 않으니, 양쪽을 다 읽어라(7절).

deadline, lifespan, liveliness는 대부분 설정하지 않는 셋이고, 그중 deadline과 liveliness가 스트림이 *멈췄다*는 것을 알려 줄 수 있는 유일한 정책이다(lifespan은 낡은 샘플을 만료시킬 뿐 이벤트를 내지 않는다). deadline을 걸면 서브스크립션이 *requested deadline missed* 이벤트를 받고, liveliness lease를 걸면 퍼블리셔가 조용히 죽을 때 *liveliness changed* 이벤트를 받는다. 이것이 없으면 죽은 센서와 느린 센서가 똑같아 보인다. 구체적인 예: 30 Hz 카메라는 33 ms마다 프레임을 보낸다. 퍼블리셔가 40 ms deadline을 제공하고 서브스크립션도 40 ms를 요청하면, 프레임 없이 40 ms가 넘게 지날 때마다 서브스크립션이 *requested deadline missed* 이벤트를 받는다.

> **Deadline과 liveliness의 정의.** 둘은 *퍼블리셔와 그 서브스크립션 사이의 시간 계약*이고, 제공되고 요청되며 3절의 규칙으로 맞춰진다. 깨진 계약은 양 끝에 **이벤트**를 내는데, 직접 등록한 콜백으로만 보이며 오류나 연결 끊김으로 나타나지는 않는다. **Deadline**의 조건은 둘이다. 연속한 메시지 사이의 **약속된 최대 간격** $T_{\text{dl}}$, 그리고 간격이 그것을 넘을 때마다 나는 **이벤트**(*requested* 또는 *offered deadline missed*)다. **Liveliness**의 조건도 둘이다. 하나는 **종류**로, *automatic*은 같은 노드의 퍼블리셔 중 하나라도 발행하면 갱신되고 *manual by topic*은 이 퍼블리셔가 스스로 살아 있음을 알릴 때만 갱신된다. 다른 하나는 **lease** $T_{\text{lease}}$이고, 그 안에 갱신이 없으면 두 끝은 *liveliness changed*와 *liveliness lost*를 받는다.
>
> $$\text{miss}_k\iff t_{k+1}-t_k>T_{\text{dl}},\qquad \text{alive}(t)\iff t-t_{\text{renew}}\le T_{\text{lease}}$$
>
> 여기서 $t_k$는 $k$번째 메시지를 보낸 시각(퍼블리셔 쪽) 또는 받은 시각(서브스크립션 쪽), $t_{\text{renew}}$는 마지막 갱신 시각이다. deadline은 데이터를, liveliness는 쓰는 쪽을 본다.
>
> - **예**: $20\,\mathrm{ms}$마다 발행하는 P6 카메라와 $T_{\text{dl}}=40\,\mathrm{ms}$. $20\le40$이므로 이벤트가 없다. 카메라가 $200\,\mathrm{ms}$ 멈추면 $40$을 넘고 이벤트가 난다.
> - **비예**: 대상으로 한 번 끝까지에서 제어기 자신이 $200\,\mathrm{ms}$ 멈추는 경우. 간격은 계속 $20\,\mathrm{ms}$이므로 아무것도 울리지 않는다. 두 계약 모두 소비자를 보지 않기 때문이다. 또 P6의 프로파일은 lease를 정하지 않으므로 lease는 *default*, 곧 대개 무한으로 남고 liveliness를 잃는 일이 없다. 멈춘 스트림은 이 기간들을 직접 정했을 때만 보고된다.

**계산: P6 카메라와 $70\,\mathrm{ms}$ 예산.** 비전 $50\,\mathrm{Hz}$는 주기 $20\,\mathrm{ms}$이므로 건강한 카메라는 `/goal`의 $40\,\mathrm{ms}$ deadline을 통과한다. $200\,\mathrm{ms}$ 정지는 놓치고 *requested deadline missed*를 낸다. 별도로, 카메라 *best effort*에 제어기의 *reliable* 요청은 연결되지 않는다. `echo`는 적응해서 출력하고 노드는 안 돈다. QoS를 고쳐도 $200\,\mathrm{ms}$ 스탬프는 $70\,\mathrm{ms}$ 예산 안에 남는다. 초과 $130\,\mathrm{ms}$, 카트가 이미 지나간 목표에 힘이 나간다([[02-foundations/lab-plants|0.6]], 산수는 [[04-robotics/robot-systems-deployment|10]]). 과제는 이 쌍이다. 비호환 신뢰성, 그다음 QoS를 고친 뒤의 늦은 스탬프.

### 3. 호환성: request 대 offered 규칙

외워야 할 규칙이다. 4절의 모든 것이 여기서 따라 나온다.

> 서브스크립션은 받아들일 수 있는 *최소 품질*을 요청(**request**)한다. 퍼블리셔는 제공할 수 있는 *최대 품질*을 제공(**offer**)한다. 요청의 **모든** 정책이 대응하는 제공보다 더 까다롭지 않을 때만 연결된다.

호환성은 쌍 단위이고 다른 참여자와 무관하다. 퍼블리셔 하나가 서로 다른 요청 프로파일을 가진 여러 서브스크립션을 동시에 상대할 수 있고, 제3의 노드가 있어도 판정은 바뀌지 않는다.

> **QoS 호환성의 정의.** **호환성**은 *퍼블리셔–서브스크립션 쌍 하나의 성질*이다. 두 프로파일에 대한 예/아니오 술어이고, 토픽의 다른 끝점은 보지 않는다. 정의 조건은 셋이다. 다섯 정책에는 **엄격함의 순서**가 있다. best effort는 reliable보다, volatile은 transient local보다, automatic은 manual by topic보다 느슨하고, deadline과 lease duration은 기간이 *짧을수록* 엄격하며 *default*는 무한으로 친다. 요청은 **다섯 모두에서 동시에 제공보다 엄격하지 않아야** 하므로, 하나만 어긋나도 쌍은 거부된다. 그리고 history, depth, lifespan은 **아예 비교되지 않는다.**
>
> $$\mathrm{match}(o,r)=[r_{\text{rel}}\preceq o_{\text{rel}}]\wedge[r_{\text{dur}}\preceq o_{\text{dur}}]\wedge[r_{\text{live}}\preceq o_{\text{live}}]\wedge[r_{\text{dl}}\ge o_{\text{dl}}]\wedge[r_{\text{lease}}\ge o_{\text{lease}}]$$
>
> 여기서 $o$는 제공하는(퍼블리셔) 프로파일, $r$은 요청하는(서브스크립션) 프로파일, $\preceq$는 "더 엄격하지 않음"이다. 기간 둘의 부등호가 반대 방향인 것은 약속한 간격이 길수록 약한 약속이기 때문이다. 그래서 default로 둔 퍼블리셔는 deadline을 명시한 어떤 서브스크립션과도 맞지 않는다($x\ge\infty$는 거짓).
>
> - **예**: 고치기 전 P6의 `/goal`은 첫 괄호에서 실패한다. reliable $\not\preceq$ best effort이므로 아무것도 전달되지 않는다. 고친 뒤에는 다섯이 모두 성립한다. 양 끝 모두 best effort, volatile, automatic이고, $40\ge40\,\mathrm{ms}$이며, 어느 쪽도 정하지 않은 lease는 $\infty\ge\infty$다.
> - **비예**: 고치기 전의 depth, 곧 `KEEP_LAST (5)` 제공 대 `KEEP_LAST (10)` 요청. `--verbose`에서 값이 달라 눈길을 끌지만 depth는 술어에 없으므로, 쌍을 막지도 않고 실패를 설명하지도 않는다. 술어가 거짓이어도 오류는 나지 않으니, 이 다섯 줄을 읽는 것이 진단의 전부다.

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

정석 사례. 카메라 드라이버가 30 Hz로 발행하고, 합리적으로 작성되어 있다. 프레임을 떨어뜨리는 편이 막히는 것보다 나으므로 **best effort** 쪽을 offer한다. 당신은 QoS를 생각하지 않고 서브스크라이버를 쓴다. 기본 프로파일, 즉 **reliable** 쪽이 된다. 제공되지 않는 품질을 요청한 것이다.

결과: `ros2 node list`에 두 노드가 다 있다. `ros2 topic list`에 토픽이 있다. `ros2 topic info`는 퍼블리셔 1, 서브스크립션 1을 보고한다. 콜백은 한 번도 실행되지 않는다.

통설에 한 가지 정정이 필요하다. 추적할 때 중요하다. 이 실패는 *완전히* 보이지 않는 것은 아니다. rclcpp와 rclpy 모두 incompatible-QoS 이벤트의 기본 핸들러를 등록하고, 그것이 탐색 시점에 노드 자신의 로거로 경고를 한 번 찍는다. 문구는 클라이언트 라이브러리마다 다르다. 아래는 rclpy의 것이다.

```text
[WARN] [...] [my_subscriber]: New publisher discovered on topic '/image', offering incompatible QoS. No messages will be received from it. Last incompatible policy: RELIABILITY
```

rclcpp 서브스크립션은 "No messages will be sent to it"이라고 쓰고 정책 이름을 `RELIABILITY_QOS_POLICY`로 적으므로, 문장 전체가 아니라 `incompatible QoS`로 grep하라.

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

**Sensor data** 프로파일은 가장 자주 손이 가고 가장 많은 불일치를 만든다. reliability를 바꾸기 때문이다. 소비자가 캡처 직후의 최신 샘플을 원하고 일부 손실을 감당할 수 있을 때 쓴다. 카메라 프레임, 라이다 스캔, IMU. 메시지 하나하나가 개별적으로 의미를 갖는 토픽 — 한 번만 보내지거나 다음 메시지로 대체되지 않는 것, 곧 내비게이션 목표 같은 일회성 목표, 비상 정지, 모드 변경 — 에는 쓰지 마라. 판별 기준은 다음 메시지가 잃어버린 메시지를 무의미하게 만드느냐다. P6의 `/goal`은 이름과 달리 이 기준을 통과한다. 각 설정점이 $20\,\mathrm{ms}$ 전의 것을 대체하는 $50\,\mathrm{Hz}$ 스트림은 센서 같은 스트림이고, 아래 대상으로 한 번 끝까지가 여기에 이 프로파일을 주는 이유가 그것이다.

**Transient local** durability는 ROS 1의 *latching* 퍼블리셔를 대신한다. 늦게 들어오는 구독자를 위해 샘플을 보존하므로, 지도가 발행되고 10분 뒤에 뜬 노드도 그 지도를 받는다. 실제로 쓰게 될 스택의 예 둘:

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

이것이 그 명령이다. 그냥 `ros2 topic info`는 개수만 주지만, `--verbose`(또는 `-v`)는 토픽의 퍼블리셔와 서브스크립션마다 노드 이름, 네임스페이스, 타입, 타입 해시, GID(미들웨어가 퍼블리셔와 서브스크립션마다 붙이는 전역 고유 ID), 그리고 전체 QoS 프로파일을 찍는다.

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

사람을 속이는 CLI 동작이 하나 있다. `ros2 topic echo`는 기본값이 sensor data 프로파일이지만 *퍼블리셔들을 조사해 스스로를 맞춘다*. 모두 reliable이면 reliable을 요청하고, 하나라도 best effort면 best effort로 물러서며, transient local도 마찬가지다. 다만 안내 문구는 *섞인* 경우에만 찍는다. "Some, but not all, publishers are offering…"이라는 문구이고, 발행자가 전부 best effort이면 아무 말 없이 물러선다. 문구가 없다는 것이 맞춰 가지 않았다는 증거는 아니다. 그래서 **`ros2 topic echo`는 당신 노드가 받지 못하는 토픽에서도 대개 데이터를 보여 준다.** 관측에는 기능이고 진단에는 함정이다. `echo`를 당신 노드처럼 굴게 하려면 정책을 직접 고정하라.

```bash
ros2 topic echo /image --qos-reliability reliable   # 이제 당신 노드와 똑같이 실패한다
```

`ros2 topic pub`도 같은 계열의 플래그(`--qos-profile`, `--qos-reliability`, `--qos-durability`, `--qos-depth`, `--qos-history`, `--qos-liveliness`)를 갖고, 기본값은 `default` 프로파일이며 이쪽은 맞춰 주지 않는다.

### 대상으로 한 번 끝까지: P6에 필요한 큐 깊이와 200 ms 정지가 하는 일 · Worked case

2–5절 전부를 P6의 `/goal` 위에서 계산한다. 주기 둘부터. 아래의 모든 개수가 정지 시간을 이 둘 중 하나로 나눈 값이기 때문이다.

$$T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=20\,\mathrm{ms},\qquad T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=5\,\mathrm{ms}$$

사건은 이렇다. 제어기가 $t=0$부터 $t=200\,\mathrm{ms}$까지 $D=200\,\mathrm{ms}$ 동안 메시지를 하나도 가져가지 않는다. 콜백 하나가 그만큼 오래 돌고, 그동안 그 노드의 다른 것은 아무것도 돌지 않기 때문이다 — 왜 그런지, 어떻게 막는지는 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]이다. 그동안 카메라는 멀쩡하고 $20, 40, \ldots, 200\,\mathrm{ms}$에 발행한다.

**1단계 — 무엇이 쌓이는가**. 정지 동안 퍼블리셔가 내보내는 것은

$$n=\frac{D}{T_{\text{vision}}}=\frac{200}{20}=10\ \text{개},\qquad \frac{D}{T_{\text{ctrl}}}=\frac{200}{5}=40\ \text{번의 제어 발화 손실}$$

이므로 가져갈 사람 없는 목표가 열 개 도착하고 명령 마흔 번이 나가지 않는다. 두 숫자 모두 어떤 로그에도 남지 않는다.

**2단계 — 7단계의 수정이 남기는 프로파일에서 무엇이 살아남는가**. 메시지는 클라이언트 라이브러리 층에 쌓이지 않고 *구독*의 history 아래 미들웨어에 앉는다. 즉 여기서 정하는 것은 카메라의 깊이가 아니라 제어기 자신의 깊이다. best effort 카메라에 맞추려고 제어기가 5절의 sensor-data 프로파일을 받아들인 뒤를 보자. 그 프로파일이 `KEEP_LAST (5)`다. 이것은 이 토픽에 맞는 계열의 프로파일이고 5절의 규칙을 어기는 것도 아니다. `/goal`은 각 설정점이 $20\,\mathrm{ms}$ 전의 것을 대체하는 스트림이기 때문이다. 한 번만 보내는 내비게이션 목표라면 그 규칙이 금하는 경우다. 여섯 번째부터는 도착할 때마다 가장 오래된 것을 밀어내므로, 열 중 다섯은 당신 코드가 보기도 전에 버려진다. $t=200\,\mathrm{ms}$에 살아남은 것은 스탬프 $120,140,160,180,200$이고 그 나이는

$$200-\{120,140,160,180,200\}=\{80,60,40,20,0\}\ \mathrm{ms}$$

나이는 스탬프 이후 흐른 시간일 뿐이기 때문이다. 버려진 다섯의 나이는 $100$에서 $180\,\mathrm{ms}$였다.

**3단계 — 나오는 순서, 이쪽이 아픈 부분**. 퍼블리셔 하나에서 온 생존자들은 발행 순서대로 전달되므로, 정지 이후 첫 콜백이 받는 것은 나이 $80\,\mathrm{ms}$의 **가장 오래된** 생존자이고 가장 새 목표는 다섯 번째 콜백이다. (executor의 round-robin([[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]])은 과부하 executor가 다음에 어느 *토픽*을 볼지에 대한 것이지 한 토픽 안 샘플 순서가 아니다.) 그래서 제어기가 회복한 직후 처음 하는 일은 자기 $70\,\mathrm{ms}$ 예산 전체보다 오래된 목표를 향해 모는 것이다.

**4단계 — 생존자를 예산에 채점한다**. $\{80,60,40,20,0\}\,\mathrm{ms}$ 중 정확히 넷이 $70\,\mathrm{ms}$ 이하이고 하나가 아니다. 즉 깊이 5는 확실히 쓸모없는 콜백 하나와 낡은 콜백 셋을 사서, 제어기가 실제로 원한 단 하나 — 나이 $0$짜리 — 를 배달한 셈이다. 깊이를 1로 두면 다섯 대신 아홉이 버려지고, 콜백은 한 번 돌며, 그 한 번이 가장 새 목표 위에서 돈다. **제어 입력에서 깊은 큐는 안전 여유가 아니라, 모터가 도는 중에 버려야 할 밀린 짐이다.** 깊이는 샘플 하나하나가 의미를 갖는 스트림 — bag 기록기, 계수기, 적분기 — 의 것이지 "지금 어디로 갈까"의 것이 아니다.

**5단계 — 나이 검사는 미들웨어에 시킨다**. 그 정책이 lifespan이고, 대부분이 끝내 설정하지 않는 바로 그것이다. lifespan보다 오래된 샘플은 stale이고, 만료된 샘플은 조용히 버려져 아예 수신되지 않는다. `lifespan`을 예산 그 자체인 $70\,\mathrm{ms}$로 두면 나이 $80\,\mathrm{ms}$ 생존자는 콜백에 닿지도 않고 예산 안의 넷만 닿는다. 콜백마다 손으로 쓰게 될 검사를 프로파일로 옮긴 것이고, 거기서는 `ros2 topic info --verbose`가 동료에게 그것을 보여 줄 수 있다.

**6단계 — 그리고 여기서 deadline이 말해 주지 않는 것**. 카메라가 $40\,\mathrm{ms}$ deadline을 제공하고 제어기가 $40\,\mathrm{ms}$를 요청하면 호환이다. 요청이 제공보다 더 엄격하지 않기 때문이다. 그리고 $20\,\mathrm{ms}$마다 발행하는 건강한 P6 카메라는 $20\,\mathrm{ms}$의 여유를 두고 그것을 충족한다. 이번 정지 동안에도 모든 구간에서 계속 충족하고, *requested deadline missed*는 한 번도 올라오지 않는다. 카메라는 제때 발행했고 미들웨어는 제때 수신했기 때문이다. deadline은 토픽 위 메시지 사이의 간격을 보지, 당신의 제어기가 그것을 가져가기를 멈췄다는 사실은 보지 못한다. 과제의 공백은 반대쪽, 카메라 자신이 $200\,\mathrm{ms}$ 조용해지는 경우다. 그쪽에서는 deadline이 울리고, 그 뒤 첫 프레임은 $200\,\mathrm{ms}$ 된 스탬프를 달고 오며 $70\,\mathrm{ms}$ 예산을 $130\,\mathrm{ms}$ 넘긴다. 길이가 같은 고장 둘인데 알려 주는 이벤트가 있는 쪽은 하나뿐이다.

**7단계 — 물론 reliability 줄에 가위표가 있으면 이 중 아무것도 일어나지 않는다**. 위의 그림에서 맨 위 패널을 다시 보라. 카메라의 best effort 제공에 제어기의 reliable 요청은 연결되지 않으므로 1단계의 개수는 열이 아니라 영이고, 영원히 영이며, 노드 둘은 멀쩡하다. `ros2 topic info /goal --verbose`로 그것부터 배제한 다음에 깊이를 따져라.

### 8. 실습: QoS로 토픽을 망가뜨리고 고치기

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

5. 이제 durability 쪽. latched 메시지를 발행하고 **발행자를 켜 둔 채로** 둔다. transient local은 발행자 자신의 이력에 보관되므로 프로세스가 끝나면 보관본도 함께 사라진다. `--once`는 종료해 버리니 반복 발행으로 터미널을 열어 둔다.

```bash
ros2 topic pub /demo_latched std_msgs/msg/String "{data: the-map}" --qos-durability transient_local --qos-depth 1 --rate 0.2
```

그 터미널이 *살아 있는 동안* 다른 터미널에서 구독한다. 먼저 기본 volatile 요청으로, 다음에 transient local로. volatile 구독자는 자기가 합류한 뒤에 발행된 것만 보고, transient local 구독자는 보관본을 즉시 받는다.

```bash
ros2 topic echo /demo_latched --qos-durability volatile          # 다음 것을 기다린다
ros2 topic echo /demo_latched --qos-durability transient_local   # 보관본이 즉시 온다
```

reliability 네 조합과 durability 네 조합 중 어느 것이 연결에 실패하는지 보지 않고 말할 수 있으면 끝난 것이다.

### 9. 이 페이지가 다루지 않는 것

콜백을 무엇이 돌리는지, 콜백 하나가 막히면 노드의 나머지에 무슨 일이 생기는지, 메시지에 어느 시계로 스탬프를 찍는지 — executor, 콜백 그룹, `use_sim_time` — 는 나머지 두 조용한 실패이고 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에 있다. 기록과 재생 시의 토픽별 QoS 오버라이드, 그리고 시스템이 이상할 때 돌릴 순서 있는 점검 목록은 [[04-robotics/ros2/debugging-data-reproducibility|25.10 디버깅, 데이터, 재현성]]에 있다. DDS 벤더 튜닝(버퍼 크기, 멀티캐스트, 공유 메모리 전송)은 ROS 2가 아니라 벤더 문서에 있다. 한 프로세스 안의 노드들이 미들웨어를 거쳐 직렬화하지 않고 메시지를 넘기게 하는 프로세스 내 통신과 composition은 ROS 2 composition 문서를 보라.

### 읽고 나면 · After reading

- request 대 offered 규칙을 말하고, 표 없이 reliability, durability, deadline, liveliness에 적용할 수 있다.
- `ros2 topic info --verbose`로 불일치를 찾고, `ros2 topic echo`가 데이터를 찍는다는 것이 내 노드에 대해 아무것도 증명하지 않는 이유를 말할 수 있다.
- 토픽에 미리 정의된 프로파일을 고르고, "다음 메시지가 잃어버린 메시지를 무의미하게 만드는가"를 물어 목표라는 이름의 토픽에 best effort가 맞는지 판단할 수 있다.
- 지연 예산에 맞춰 제어 입력의 history depth와 lifespan을 정하고, 깊은 큐가 밀린 짐인 이유를 말할 수 있다.
- deadline 이벤트가 알려 줄 수 있는 조용한 실패와 알려 줄 수 없는 조용한 실패를 구분할 수 있다.

### 스스로 점검

1. 퍼블리셔가 reliable을 offer하고 서브스크립션이 best effort를 request한다. 연결되는가,
   그리고 반대 경우는 왜 다른가?
2. 내 노드는 `/map`을 구독하는데 아무것도 못 받고, `ros2 topic echo /map`은 지도를 바로
   찍는다. 무슨 일인가?
3. $50\,\mathrm{Hz}$ 카메라가 계속 발행하는 동안 P6 제어기가 $200\,\mathrm{ms}$ 동안
   메시지를 가져가지 않는다. `KEEP_LAST (5)`에서 목표를 몇 개 잃고, 콜백이 처음 받는
   것은 몇 밀리초짜리이며, 생존자 중 몇 개가 $70\,\mathrm{ms}$ 예산 안인가? deadline이
   알려 주었겠는가?
4. 5절은 목표에 sensor-data 프로파일을 쓰지 말라고 하는데, 대상으로 한 번 끝까지는 P6의
   `/goal`에 그것을 쓴다. 어느 쪽이 맞고, 어떤 토픽에든 답을 정해 주는 질문 하나는 무엇인가?

> [!tip]- 정답 · Answers
> 1. 연결된다. 요청은 서브스크립션이 받아들일 최소 품질이고 제공은 퍼블리셔가 낼 수 있는 최대 품질이므로, reliable 퍼블리셔는 best effort 요청을 넘치게 만족시킨다. 반대 — best effort 퍼블리셔와 reliable 서브스크립션 — 는 제공되지 않는 보장을 요구하므로 연결이 만들어지지 않고 메시지가 하나도 오가지 않는다.
> 2. 거의 확실히 durability다. map server는 transient local로, 내 노드가 뜨기 전에 한 번 발행했다. 내 노드는 기본 volatile을 요청하므로 연결은 정당하게 되지만 새 메시지만 받는다. `ros2 topic echo`는 퍼블리셔를 조사해 자기 요청을 transient local로 맞추므로 보존된 샘플을 받는다. 구독 쪽을 transient local로 고치고, `echo`가 된다고 해서 내 노드가 받을 수 있다는 증명이 되지는 않는다는 것을 기억하라.
> 3. 정지 동안 목표 열 개가 발행되고($200/20$) 다섯을 잃는다. `KEEP_LAST (5)`는 가장 새 다섯만 남기고 도착할 때마다 가장 오래된 것을 밀어내기 때문이다. 제어기가 다시 받기 시작한 순간 생존자의 나이는 $\{80,60,40,20,0\}\,\mathrm{ms}$이고 발행 순서대로 전달되므로, 첫 콜백이 받는 것은 이미 예산을 넘긴 $80\,\mathrm{ms}$짜리이고 가장 새 목표는 다섯 번째 콜백이다. 생존자 다섯 중 넷이 $70\,\mathrm{ms}$ 안이다. deadline 이벤트는 울리지 않는다. 카메라는 제때 발행했고 미들웨어는 제때 수신했으므로 토픽 위에서 구간을 놓친 것이 없기 때문이다. 처방은 깊이 1, 또는 $70\,\mathrm{ms}$ lifespan이다. 깊은 큐는 여유가 아니라 밀린 짐이다.
> 4. 둘 다 맞다. 규칙은 메시지 하나하나가 개별적으로 의미를 갖는 토픽 — 한 번만 보내지거나 다음 메시지로 대체되지 않는 것 — 에 관한 것이고, P6의 `/goal`은 그런 토픽이 아니다. 각 설정점이 $20\,\mathrm{ms}$ 전의 것을 대체하는 $50\,\mathrm{Hz}$ 스트림이므로, 샘플 하나를 잃으면 $20\,\mathrm{ms}$어치 신선도를 잃고 다음 샘플이 그것을 메운다. 질문은 '다음 메시지가 잃어버린 메시지를 무의미하게 만드는가'다. 그렇다면 얕은 depth의 best effort가 맞다. 아니라면 — 한 번 보내는 내비게이션 목표, 비상 정지, 모드 변경 — reliable을 요청하고, 한 번 발행되어 늦게 온 쪽이 필요로 하는 것이라면 transient local까지 요청한다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**. 카메라 노출 중간부터 힘까지 예산 $70\,\mathrm{ms}$. 비전 메시지가 $200\,\mathrm{ms}$ 늦다. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** 다른 정책을 잘못 고른 제어기에 대한 위의 그림: 제어기는 카메라가 제공하는 대로 best effort를 요청하지만, 자기가 뜨기 전에 발행된 목표를 잡으려고 *transient local* 내구성을 요청하고, 카메라는 sensor-data 프로파일(best effort, volatile)을 제공한다. 비호환인 줄에 가위표를 쳐라. 이어서 depth $5$가 아니라 `KEEP_LAST (3)`로 고친 제어기에 대한 아래 절반을 같은 $200\,\mathrm{ms}$ 정지를 지나며 그려라. 어느 목표가 살아남고, 나이는 얼마이며, $70\,\mathrm{ms}$ 예산을 넘은 것이 있는가?
2. **유도.** (a) 그 QoS 끝점이 연결되는가? (b) $200\,\mathrm{ms}$ 대 $70\,\mathrm{ms}$ 예산 — 제어기가 그 스탬프를 그대로 쓰면 힘은 얼마나 늦은가? (c) `/goal`에 $40\,\mathrm{ms}$ deadline: 건강한 $50\,\mathrm{Hz}$ 카메라는 통과하는가? $200\,\mathrm{ms}$ 정지는 이벤트를 내는가?
3. **해석.** `ros2 topic echo /goal`은 프레임을 찍는데 제어기 콜백은 안 돈다. 조용한 고장은 무엇이고, QoS를 고친 뒤에도 $200\,\mathrm{ms}$ 늦은 비전이 *역시* 예산 실패인 이유는?

> [!note]- 그리는 법 · How to draw it
> - 간선은 타원 둘과 화살표 하나이고, 화살표 위에는 라벨이 아니라 상자 둘을 위아래로 놓는다. 위는 카메라가 *제공(offer)* 하는 것, 아래는 제어기가 *요청(request)* 하는 것, `ros2 topic info --verbose`가 찍는 그대로.
> - 두 상자 모두에 정책 줄을 전부 적는다 — reliability, history, durability, deadline, liveliness. 의심 가는 하나만 적지 않는다. 이번에는 reliability가 맞고, 바로 그래서 눈이 상자를 그냥 지나친다.
> - 줄을 짝지어 3절의 표에 대보고 비호환인 짝에만 가위표를 친다. *volatile* 제공 대 *transient local* 요청은 내구성 표에서 "No"다. 요청이 제공보다 엄격하기 때문이다. 가위표는 하나이고, 위 그림에서 친 줄이 아니다.
> - 가위표 옆에 보게 될 것을 적는다. 연결은 없고, 발견 시점의 경고 한 줄이 마지막 비호환 정책으로 reliability가 아니라 durability를 댄다.
> - 아래 절반은 시계 위에: 제어기가 $200\,\mathrm{ms}$ 동안 아무것도 가져가지 않는 사이 $20\,\mathrm{ms}$ 간격으로 발행된 목표 열 개와, 가장 새것만 남기는 depth $3$의 큐.
> - 제어기가 깨어날 때 살아남은 것마다 나이를 적고 $70\,\mathrm{ms}$ 예산을 선으로 그어, 예산보다 오래된 목표가 있다면 눈에 띄게 선의 반대편에 있게 한다.

> [!tip]- 정답 · Solutions
> 1. 위: reliability는 양 끝 모두 best effort로 맞고 durability가 맞지 않는다. transient local 요청 대 volatile 제공은 비호환이므로(3절의 내구성 표) 다섯 줄 중 가위표는 그 하나이고, 끝점은 여전히 연결되지 않으며, 발견 시점의 경고 한 줄은 durability를 댄다. 아래: depth $3$이면 정지 동안 발행된 목표 열 개 가운데 가장 새로운 셋만 살아남아 나이가 $40$, $20$, $0\,\mathrm{ms}$이고, $70\,\mathrm{ms}$ 예산을 넘은 것은 없다. depth $5$는 $80\,\mathrm{ms}$ 된 목표 하나를 남겼다. 큐가 얕을수록 더 많이 버리고, 늘 가장 최근 값만 읽는 흐름이 원하는 것이 바로 그것이다.
> 2. (a) 아니오 — reliable 요청 대 best-effort 제공. (b) 예산 초과 $130\,\mathrm{ms}$. (c) 건강한 $20\,\mathrm{ms}$ 주기는 $40\,\mathrm{ms}$를 통과; $200\,\mathrm{ms}$ 공백은 *requested deadline missed*.
> 3. 신뢰성 비호환. `echo`는 맞추고 노드는 안 맞춘다. QoS를 고쳐도 $70\,\mathrm{ms}$ 예산 안에 $200\,\mathrm{ms}$ 스탬프가 남는다 — 힘은 카트가 이미 지나간 목표에 걸린다.

### 출처

- ROS 2 Jazzy 문서 — Concepts: Quality of Service settings(정책, 프로파일, 호환성 표, QoS 이벤트, matched 이벤트).
- ROS 2 Jazzy 문서 — Tutorials: Using quality-of-service settings for lossy networks.
- 그대로 인용한 값과 메시지의 출처(Jazzy 브랜치 소스): `rmw/qos_profiles.h`(프로파일 내용), `rclcpp/subscription_base.cpp`와 `publisher_base.cpp`, `rclpy/event_handler.py`(기본 incompatible-QoS 경고), `rclpy/topic_endpoint_info.py`(`--verbose` 출력 형식), `ros2cli/ros2topic`(QoS 플래그와 `echo`의 퍼블리셔 맞춤 동작), `robot_state_publisher`와 `nav2_map_server`(transient local 퍼블리셔).
- 2절과 3절의 정의에 쓴 Jazzy 브랜치 소스: [`rmw_dds_common/src/qos.cpp`](https://github.com/ros2/rmw_dds_common/blob/jazzy/rmw_dds_common/src/qos.cpp)(`qos_profile_check_compatible`은 reliability, durability, deadline, liveliness, lease duration만 비교한다), [`rclpy/qos.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/qos.py)와 [`rclcpp/qos.hpp`](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/qos.hpp)(지정하지 않은 정책은 기본 프로파일에서 온다), [`rclcpp/subscription_base.cpp`](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/src/rclcpp/subscription_base.cpp), `publisher_base.cpp`, `rclpy/event_handler.py`(deadline과 liveliness 이벤트에는 기본 핸들러가 없고, 등록한 콜백만 그것을 받는다).
