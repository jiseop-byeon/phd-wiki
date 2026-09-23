---
title: "25.5.1 Executors, Callback Groups and Time"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Predict which callbacks of a node can run while another is busy, fix the synchronous-call deadlock with callback groups and a multi-threaded executor, and make a node's stamps and timers follow simulated or replayed time."
mastery-when: "Go deeper when you are doing response-time analysis of a control chain, or writing a custom executor, rather than making an ordinary node behave."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to recognise a blocked executor and a node on the wrong clock in a running system, and fix each with a two-line change. Not enough to do formal timing analysis of an executor.
> **Working** — 돌아가는 시스템에서 막힌 executor와 엉뚱한 시계를 읽는 노드를 알아보고, 각각을 두 줄 수정으로 고칠 정도. Executor의 형식적 타이밍 분석을 할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]] (you have written a timer, a publisher and a subscriber), [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]] (you have written a service client and met the blocking call whose deadlock this page explains) and [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]] (what the middleware keeps while no callback takes it). The numbers are plant P6 of [[02-foundations/lab-plants|0.6 Lab Plants]]. Everything runs on **ROS 2 Jazzy Jalisco on Ubuntu 24.04**; no workspace is needed, and the exercises run from the command line and from plain Python files.
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]](타이머, 퍼블리셔, 서브스크라이버를 써 봤다), [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]](서비스 클라이언트를 써 봤고, 이 페이지가 풀어 주는 교착을 남긴 막히는 호출을 만났다), [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]](콜백이 가져가지 않는 동안 미들웨어가 무엇을 들고 있는가). 숫자는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P6이다. 기준 환경은 Ubuntu 24.04의 **ROS 2 Jazzy Jalisco**. 워크스페이스는 필요 없고, 실습은 커맨드라인과 평범한 Python 파일로 돌아간다.

> [!note] First pass · 처음이라면
> Read the picture and the Worked case, then §1 and §2: one thread runs one callback at a time, and a callback group decides which callbacks may overlap — the deadlock at the end of §2 is the one to recognise on sight. §3 (time) does not depend on §1–§2 and can be read on its own, with §4 as its exercise. §5 is the executor failure to practise, and §6 where the rest lives.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], the 1-D cart and its clock, seen from inside its controller node — the timer-driven controller of [[04-robotics/ros2/nodes-topics-messages|25.2]], with one callback added. P6 freezes the rates and the budget; the third callback is this page's own.

| Callback | Fires every | Runs for | What it does |
|---|---|---|---|
| control timer | $T_{\text{ctrl}}=5\,\mathrm{ms}$ ($200\,\mathrm{Hz}$) | well under $5\,\mathrm{ms}$ | reads the encoder, uses the newest stored goal, publishes the motor command |
| `/goal` subscription, `on_goal` | $T_{\text{vision}}=20\,\mathrm{ms}$ ($50\,\mathrm{Hz}$) | well under $5\,\mathrm{ms}$ | stores the newest goal for the timer |
| calibration timer — **page-local** | $1\,\mathrm{s}$ | $D=200\,\mathrm{ms}$ | reloads the rail calibration from a network share, blocked on the file the whole time |

The end-to-end budget is P6's $B=70\,\mathrm{ms}$, camera mid-exposure to applied force. All three callbacks are created without naming a callback group, and the node is spun with `rclpy.spin(node)`; §1 and §2 are why both facts matter.

*Scope: this page teaches who runs a node's callbacks — executors and callback groups, including the synchronous-call deadlock — and which clock a node reads: wall, steady and ROS time, `/clock` and `use_sim_time`. It does not teach what the middleware keeps while no callback takes it, which is QoS history on [[04-robotics/ros2/qos-executors-time|25.5]]; nor real-time scheduling of callback chains, which is beyond this track (§6).*

### The picture: P6's controller during a 200 ms callback, on one thread and on two

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="P6's controller node on a 0 to 200 ms axis while its calibration callback blocks for 200 ms. A, one thread with every callback in the default group: the calibration bar fills the thread, 40 control firings due every 5 ms are hollow because none runs on time, and 10 goals arriving every 20 ms wait in the middleware. B, two threads with the calibration timer in its own group: the calibration bar fills thread 1 while thread 2 runs all 40 control firings and all 10 goal callbacks on time.">
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">A · rclpy.spin(node): one thread, every callback in the default group</text>
  <text x="70" y="40" font-size="11" fill-opacity="0.7" fill="currentColor">control timer: 40 firings due, one every 5 ms — none runs on time</text>
  <path d="M81.25 58v-10M92.5 58v-10M103.75 58v-10M115 58v-10M126.25 58v-10M137.5 58v-10M148.75 58v-10M160 58v-10M171.25 58v-10M182.5 58v-10M193.75 58v-10M205 58v-10M216.25 58v-10M227.5 58v-10M238.75 58v-10M250 58v-10M261.25 58v-10M272.5 58v-10M283.75 58v-10M295 58v-10M306.25 58v-10M317.5 58v-10M328.75 58v-10M340 58v-10M351.25 58v-10M362.5 58v-10M373.75 58v-10M385 58v-10M396.25 58v-10M407.5 58v-10M418.75 58v-10M430 58v-10M441.25 58v-10M452.5 58v-10M463.75 58v-10M475 58v-10M486.25 58v-10M497.5 58v-10M508.75 58v-10M520 58v-10" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 2" fill="none"/>
  <text x="12" y="75" font-size="11" fill-opacity="0.85" fill="currentColor">thread 1</text>
  <rect x="70" y="61" width="450" height="22" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="295" y="76" font-size="11" text-anchor="middle" fill="currentColor">calibration callback, 200 ms, waiting on the file</text>
  <path d="M111 89H119L115 97zM156 89H164L160 97zM201 89H209L205 97zM246 89H254L250 97zM291 89H299L295 97zM336 89H344L340 97zM381 89H389L385 97zM426 89H434L430 97zM471 89H479L475 97zM516 89H524L520 97z" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="70" y="114" font-size="11" fill-opacity="0.7" fill="currentColor">/goal: 10 goals arrive, one every 20 ms, and wait in the middleware</text>
  <text x="12" y="150" font-size="12" fill-opacity="0.8" fill="currentColor">B · two threads, the calibration timer in its own group</text>
  <text x="12" y="177" font-size="11" fill-opacity="0.85" fill="currentColor">thread 1</text>
  <rect x="70" y="163" width="450" height="22" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="295" y="178" font-size="11" text-anchor="middle" fill="currentColor">calibration group: the same 200 ms</text>
  <text x="12" y="215" font-size="11" fill-opacity="0.85" fill="currentColor">thread 2</text>
  <line x1="70" y1="211" x2="520" y2="211" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <path d="M81.25 222v-22M92.5 222v-22M103.75 222v-22M115 222v-22M126.25 222v-22M137.5 222v-22M148.75 222v-22M160 222v-22M171.25 222v-22M182.5 222v-22M193.75 222v-22M205 222v-22M216.25 222v-22M227.5 222v-22M238.75 222v-22M250 222v-22M261.25 222v-22M272.5 222v-22M283.75 222v-22M295 222v-22M306.25 222v-22M317.5 222v-22M328.75 222v-22M340 222v-22M351.25 222v-22M362.5 222v-22M373.75 222v-22M385 222v-22M396.25 222v-22M407.5 222v-22M418.75 222v-22M430 222v-22M441.25 222v-22M452.5 222v-22M463.75 222v-22M475 222v-22M486.25 222v-22M497.5 222v-22M508.75 222v-22M520 222v-22" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" fill="none"/>
  <path d="M111 228H119L115 236zM156 228H164L160 236zM201 228H209L205 236zM246 228H254L250 236zM291 228H299L295 236zM336 228H344L340 236zM381 228H389L385 236zM426 228H434L430 236zM471 228H479L475 236zM516 228H524L520 236z" fill="currentColor" fill-opacity="0.9" stroke="none"/>
  <text x="70" y="252" font-size="11" fill-opacity="0.8" fill="currentColor">default group: 40 control firings and 10 goal callbacks, all on time</text>
  <line x1="70" y1="266" x2="520" y2="266" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <path d="M70 266v5M160 266v5M250 266v5M340 266v5M430 266v5M520 266v5" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" fill="none"/>
  <text x="70" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">0</text>
  <text x="160" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">40</text>
  <text x="250" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">80</text>
  <text x="340" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">120</text>
  <text x="430" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">160</text>
  <text x="526" y="286" font-size="11" text-anchor="end" fill-opacity="0.75" fill="currentColor">200 ms</text>
</svg>

P6's controller node over the $200\,\mathrm{ms}$ its calibration callback blocks, on two executors. In A, `rclpy.spin` gives one thread and every callback sits in the default group, so the $40$ control firings due every $5\,\mathrm{ms}$ never run on time and the $10$ goals published every $20\,\mathrm{ms}$ wait in the middleware. In B, the calibration timer has its own mutually exclusive group and the executor has a second thread, so all $40$ firings and all $10$ goal callbacks run on time on thread 2.

### Worked case: what a 200 ms callback costs P6's controller, and what callback groups buy back

The two periods and the one duration, because every count below is a ratio of them:

$$T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=5\,\mathrm{ms},\qquad T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=20\,\mathrm{ms},\qquad D=200\,\mathrm{ms}$$

**Step 1 — what one thread does with 200 ms.** At $t=0$ the calibration timer fires and its callback blocks for $D$. The node is on `rclpy.spin(node)`, which builds a single-threaded *executor* — the loop that takes ready callbacks from the middleware and runs them, here one at a time on one thread (§1). So nothing else in the node runs until $t=200\,\mathrm{ms}$, and meanwhile

$$\frac{D}{T_{\text{ctrl}}}=\frac{200}{5}=40\ \text{control firings fall due},\qquad \frac{D}{T_{\text{vision}}}=\frac{200}{20}=10\ \text{goals are published}$$

None of the forty runs on time, and they are not made up afterwards, because a timer that runs late fires once and skips the periods it missed (§1). So the motor holds its last command for $200\,\mathrm{ms}$ — forty control periods, and $130\,\mathrm{ms}$ longer than P6's whole $70\,\mathrm{ms}$ budget. The ten goals wait in the middleware, where the subscription's QoS depth decides which survive; under `KEEP_LAST (5)` the first one handed over is already $80\,\mathrm{ms}$ old ([[04-robotics/ros2/qos-executors-time|25.5]], its Worked case).

**Step 2 — the rate of the damage.** The calibration fires once a second, so the controller is deaf for

$$\frac{D}{1000\,\mathrm{ms}}=\frac{200}{1000}=20\,\%$$

of the time, since one blocked stretch of $D$ recurs in every second: $40$ of every $200$ firings are lost, every second, with nothing in any log.

**Step 3 — two changes that do nothing on their own.**

- Spin on a *multi-threaded* executor — the same loop with a pool of threads (§1) — and change nothing else. Still $40$ lost: all three callbacks sit in the node's default *callback group*, a set of callbacks the executor may or may not run in parallel, and the default group is mutually exclusive — its callbacks never overlap, however many threads exist (§2).
- Give the calibration timer its own group and keep `rclpy.spin`. Still $40$ lost: a group permits parallelism, but a single-threaded executor has one thread, and it is busy.

**Step 4 — both together.** The calibration timer in its own `MutuallyExclusiveCallbackGroup`, the control timer and `on_goal` left in the default group, and a `MultiThreadedExecutor` with at least two threads. Calibration now occupies one thread for its $200\,\mathrm{ms}$ while the other runs all forty firings and all ten goal callbacks on time: the loss goes from $40$ per second to $0$. The default group keeps doing a second, useful job — the control timer and `on_goal` still never overlap each other, so the timer never reads the stored goal while `on_goal` is writing it. The price is the mirror image: calibration now runs *concurrently* with control, so it must build the new calibration in a local variable and hand it over in one assignment at the end.

**Step 5 — the version that never ends.** Replace the file read with a synchronous call to a calibration service, `client.call(...)`, with the client created in the default group — the blocking call of [[04-robotics/ros2/services-actions-parameters|25.3]]. The callback no longer waits $200\,\mathrm{ms}$. It waits for a response that only another callback of its own mutually exclusive group can deliver, so it waits forever: $D$ is unbounded, every firing from then on is lost, and the node still answers `ros2 node list`. §2 derives why, and the same two changes as step 4 fix it.

### 1. Executors: one thread or many

Two of the three ROS 2 failures that produce no error live on this page; the third, an incompatible QoS pair, is [[04-robotics/ros2/qos-executors-time|25.5 §1]].

- **Executors.** A callback blocks waiting for something that can only be produced by another callback that the same executor thread is supposed to run. The node stops responding. It does not crash, it does not log, and its publishers stay advertised. That is this section, §2 and §5.
- **Time.** A node reads the wall clock while the rest of the system is running on simulated or replayed time. Its timestamps are consistent with nothing, its timeouts fire at the wrong moments, and every value it produces looks plausible. That is §3 and §4.

Callbacks do not run by themselves. An **executor** owns one or more OS threads, watches the middleware for available messages and expired timers through a *wait set*, and invokes the corresponding callbacks. `rclpy.spin(node)` and `rclcpp::spin(node)` are shorthand for instantiating a single-threaded executor, adding the node and spinning it.

> **Executor, defined.** An **executor** is a *scheduler object inside one process* — neither a node nor a thread. Three defining conditions. It **holds entities**: the subscriptions, timers, services and clients of the nodes added to it. It **waits on a wait set**, which reports only *which* entities are ready — a timer due, a topic with a message in the middleware — never how many or how old. And it **runs each ready callback to completion on one of its threads**, within the limits of §2's callback groups.
>
> $$N_{\text{run}}(t)\le n_{\text{th}},\qquad n_{\text{late}}=\Big\lfloor\frac{D}{T}\Big\rfloor$$
>
> where $N_{\text{run}}(t)$ counts the callbacks running at $t$, $n_{\text{th}}$ is the thread count ($1$ for `rclpy.spin`) and $n_{\text{late}}$ the firings of a period-$T$ timer that fall due while one callback holds the only thread for $D$ — none replayed, since a late timer skips the periods it missed.
>
> - **Example**: P6's controller on `rclpy.spin` while calibration blocks for $D=200\,\mathrm{ms}$: $\lfloor200/5\rfloor=40$ control firings late, $40$ of the $200$ owed each second.
> - **Non-example**: an executor that queues the goals. The $200/20=10$ goals arriving meanwhile never enter it; they wait in the middleware under the subscription's QoS depth, so `KEEP_LAST (5)` loses five before any callback runs. More threads cannot recover them, which is why executor and QoS are sized together.

rclcpp offers `SingleThreadedExecutor`, `MultiThreadedExecutor`, and `StaticSingleThreadedExecutor`, which caches the node's entity list (its publishers, subscriptions, timers, services and clients — everything that can have a callback) and rebuilds it only when entities are added or removed — so, since the Jazzy executor rework, it is no longer limited to nodes that create everything during initialisation: the [Jazzy source](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/src/rclcpp/executors/static_single_threaded_executor.cpp) re-collects its entities whenever one is added or removed, while the Executors concept page still carries the older advice to use it only with such nodes. Jazzy also ships an experimental `EventsExecutor`. rclpy offers the first two.

Three consequences that beginners get wrong:

- **One thread means one callback at a time, and a long callback delays everything.** A 200 ms callback on P6's controller, whose control timer fires at 200 Hz, does not "run in the background"; it stalls the timer, forty firings' worth (the Worked case). Incoming messages are not queued at the client-library level — they stay in the middleware until a callback takes them, which is a deliberate difference from ROS 1, and means QoS depth (not some ROS-side buffer) decides what survives the stall: under *keep last*, the middleware holds only the newest N samples and each new arrival pushes out the oldest ([[04-robotics/ros2/qos-executors-time|25.5 §2]]).
- **A late timer does not catch up.** When a timer's callback finally runs late, the timer moves its next firing to the next whole multiple of its period and skips every firing it missed — rcl, the C layer under both client libraries, does this in `rcl_timer_call`. A stalled 5 ms timer therefore loses firings rather than bursting through them afterwards, which is kinder to the motor and invisible in the log.
- **The order is round-robin, not FIFO.** The wait set reports only *whether* a topic has messages, not how many or how old, so an overloaded executor processes topics in rotation rather than in arrival order.

One caveat for rclpy: the threads of a `MultiThreadedExecutor` share Python's global interpreter lock, so two Python callbacks truly run at once only while one of them is waiting — on a file, a socket, a sleep, a service response — or is inside C code that releases the lock. A callback that computes in pure Python for 200 ms still delays the others, each of which may wait up to Python's thread switch interval, $5\,\mathrm{ms}$ by default, for its turn. That is why P6's calibration callback is one that *waits* on a file; rclcpp's threads have no such lock.

### 2. Callback groups, and the deadlock 25.3 left open

Callbacks can be organised into **callback groups**, created with `create_callback_group` in rclcpp and by constructing the group class in rclpy. There are two kinds:

- **Mutually exclusive**: its callbacks are never executed in parallel with each other. Effectively, the group behaves as if it had its own single-threaded executor.
- **Reentrant**: its callbacks may run in parallel, including several concurrent invocations of the *same* callback.

Callbacks in *different* groups may always run in parallel. Anything created without naming a group joins the node's **default callback group, which is mutually exclusive**. Hold a reference to any group you create — if it is garbage-collected, its callbacks stop being triggered.

> **Callback group, defined.** A **callback group** is a *set of one node's callbacks carrying one concurrency rule* — a permission, not a thread. Three defining conditions. **Every callback belongs to exactly one group**, the node's default unless another is named, and an entity passes its group to the callbacks it spawns, a service call's hidden done-callback included. The group's **type sets the rule inside it**: *mutually exclusive* runs at most one of its callbacks at a time, *reentrant* any number, even of the same callback. And **callbacks in different groups may overlap**, but only on threads the executor has.
>
> $$N^{g}_{\text{run}}(t)\le 1\ \ (g\in\mathcal{G}_{\text{ME}}),\qquad N_{\text{run}}(t)\le n_{\text{th}}$$
>
> where $\mathcal{G}_{\text{ME}}$ is the node's mutually exclusive groups and $N^{g}_{\text{run}}(t)$ the callbacks of $g$ running at $t$; both bounds hold at every instant, so two callbacks at once need two groups (or a reentrant one) *and* two threads.
>
> - **Example**: P6's calibration timer in its own mutually exclusive group, the control timer and `on_goal` in the default one, two threads: calibration holds one for $200\,\mathrm{ms}$ while the other runs all $40$ control firings and $10$ goal callbacks, and the loss is $0$.
> - **Non-example**: the same groups on `rclpy.spin`. The groups permit overlap, but $n_{\text{th}}=1$ caps the node at one running callback, so $40$ firings are still lost — which is why the fix is always the pair, a group and a thread.

That default is the whole story behind the deadlock. If every entity in a node uses the default group, the node behaves exactly as if it were on a single-threaded executor *even when you gave it a multi-threaded one*. Choosing `MultiThreadedExecutor` and assigning no groups buys you nothing.

Now the failure [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]] left open. A timer callback makes a synchronous service call — `client.call(request)` in rclpy, or waiting on the future returned by `async_send_request` in rclcpp:

```python
def _timer_cb(self):
    self.get_logger().info('Sending request')
    _ = self.client.call(Empty.Request())          # blocks here, forever
    self.get_logger().info('Received response')
```

You see `Sending request` once. You never see `Received response`, and the timer never fires again. The server logs that it received the request and responded.

The mechanism: a synchronous call is not the absence of callbacks, it is a *hidden* callback. Step by step:

1. The timer callback starts running and calls `client.call()`, which waits for the result.
2. The client hands its callback group to the future, and the result becomes available only when that future's done-callback runs.
3. That done-callback and the timer callback are in the same mutually exclusive group, so the done-callback cannot start while the timer callback is still running.
4. The timer callback is still on the stack waiting for the result — so the done-callback can never be scheduled, and the wait never ends.
5. The stuck timer callback also blocks its own next firing, which is why the node goes completely quiet rather than merely missing one response.

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

### 3. Time: `use_sim_time`, `/clock`, and the wall clock

ROS 2 gives you three time abstractions: **SystemTime** (the machine's clock), **SteadyTime** (monotonic, for hardware timeouts, never comparable to the other two), and **ROSTime**, which is what you should use for anything that gets published or compared with a message stamp.

ROSTime reports the same as SystemTime *until a ROS time source is active*. It becomes active when the node's `use_sim_time` parameter is set. From then on, the node's clock returns the latest value received on the `/clock` topic (`rosgraph_msgs/msg/Clock`), published by the simulator or by bag playback — a *bag* is a recording of topics, and `ros2 bag play` publishes it again ([[04-robotics/ros2/debugging-data-reproducibility|25.10]]).

> **ROS time, defined.** **ROS time** is *the value a node's own clock returns* — of the three clock types, the only one that can follow a simulator or a replay. Three defining conditions. With `use_sim_time` false it **equals system time**. With it true it is **the latest value received on `/clock`**, and **zero until the first message**, meaning *uninitialised*. And it is **not monotonic**: a looping replay sends it backwards.
>
> $$t_{\text{ROS}}=\begin{cases}t_{\text{sys}} & \texttt{use\_sim\_time}=\text{false}\\ t_{\text{clock}} & \texttt{use\_sim\_time}=\text{true}\end{cases}$$
>
> where $t_{\text{sys}}$ is the machine's clock and $t_{\text{clock}}$ the newest `/clock` stamp; node-clock timers wait on $t_{\text{ROS}}$, wall timers do not.
>
> - **Example**: P6 simulated at real-time factor $r=0.5$ (defined next), `use_sim_time` set: a $5\,\mathrm{ms}$ node-clock timer fires every $10\,\mathrm{ms}$ of wall time, still $20/5=4$ times per goal.
> - **Non-example**: rclcpp's `create_wall_timer(5ms, …)` on that node never reads ROS time, so each firing spans $0.5\times5=2.5\,\mathrm{ms}$ simulated: $8$ per goal, $400\,\mathrm{Hz}$ in simulated time. A period on the wrong clock is off by exactly $r$, and no log says so.

**Real-time factor.** A simulator does not promise to keep pace with the wall clock. Its *real-time factor* $r$ is the ratio of simulated time to wall time over the same stretch of a run:

$$r=\frac{\Delta t_{\text{sim}}}{\Delta t_{\text{wall}}}$$

where $\Delta t_{\text{sim}}$ is how far `/clock` advanced and $\Delta t_{\text{wall}}$ how much wall time passed meanwhile. So $r=1$ is real time, $r=0.5$ means each simulated second takes two wall seconds — what a heavy scene on a laptop gives you — and $r>1$ is faster than real time. It is a property of the run, not of any node; a non-example is the publishing rate of `/clock`, which says how finely time is sliced, not how fast it passes. It matters because a period measured in simulated time lasts $1/r$ times as long on the wall, while a period measured on the wall does not stretch at all.

The consequences you have to design for:

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

Under simulation the wall-clock version drifts against every other timestamp by the real-time factor; under bag replay it stamps two-year-old sensor data with today's date, and TF lookups against it — the transform tree of [[04-robotics/robot-systems-deployment|10 §4]] — fail or silently extrapolate. It is one of very few bugs whose symptom is *worse* results rather than no results.

Timers split the same way. In rclpy, `create_timer(period, callback)` uses the node's clock, so it follows simulated time. In rclcpp, `create_wall_timer` deliberately uses the wall clock and does **not** follow `/clock`, while `create_timer(period, callback, group)` uses the node clock and does — a controller that must tick in simulated time needs the latter. Note also the rclcpp header warning: do not construct `rclcpp::Clock(RCL_ROS_TIME)` by hand, because an unattached clock silently runs on system time; use `this->get_clock()`.

**Worked: P6 in a simulator running at $r=0.5$.** By the definition above, a period of $T$ in simulated time takes $T/r$ on the wall, and a period of $T$ on the wall covers $rT$ of simulated time. The simulated camera publishes every $20\,\mathrm{ms}$ of simulated time, which is every $40\,\mathrm{ms}$ of wall time. On a controller node with `use_sim_time` set, a timer made with rclpy's `create_timer(0.005, …)` follows the node clock: every $5\,\mathrm{ms}$ simulated, $10\,\mathrm{ms}$ wall, so there are still $20/5=4$ control firings per goal, as P6 is designed. The same controller in C++ on `create_wall_timer(5ms, …)` fires every $5\,\mathrm{ms}$ of wall time, which is

$$rT=0.5\times5\,\mathrm{ms}=2.5\,\mathrm{ms}\ \text{of simulated time}$$

so it fires $8$ times per goal, at $400\,\mathrm{Hz}$ in the simulation's own time — twice P6's rate, with nothing in any log to say so. A controller left off simulated time altogether is worse: its clock reads about $1.79\times10^{9}\,\mathrm{s}$ (seconds since 1970) while the goal stamps count from the simulator's start, so a $70\,\mathrm{ms}$ staleness check rejects every goal and the cart never moves.

Turning it on, for one node from the command line, or for every node a launch file ([[04-robotics/ros2/workspaces-packages-launch|25.4]]) starts:

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

### 4. Exercise: put a node on a clock nobody publishes

Three sourced terminals, no workspace, about ten minutes. It shows §3's two timer calls behaving differently under the same parameter.

1. Start the Python demo talker on simulated time:

```bash
ros2 run demo_nodes_py talker --ros-args -p use_sim_time:=true
```

Nothing is printed, and `ros2 topic echo /chatter` in a second terminal stays empty. There is no error. Diagnose it from a third terminal:

```bash
ros2 param get /talker use_sim_time
ros2 topic info /clock
```

The parameter is `True`, and `/clock` shows `Publisher count: 0` with at least one subscription: the talker is listening for a clock that nobody publishes. A node on simulated time reads zero until `/clock` arrives, zero does not advance, and so the talker's timer — made with `create_timer`, on the node clock — never fires.

2. Give it a clock. Save this as `fake_clock.py` and run it with `python3 fake_clock.py`; it publishes `/clock` at a real-time factor of 0.5:

```python
import time
import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock

RTF = 0.5                                   # simulated seconds per wall second

rclpy.init()
node = Node('fake_clock')
pub = node.create_publisher(Clock, '/clock', 10)
start = time.monotonic()
while rclpy.ok():
    sim = RTF * (time.monotonic() - start)  # simulated seconds since start
    msg = Clock()
    msg.clock.sec = int(sim)
    msg.clock.nanosec = int((sim - int(sim)) * 1e9)
    pub.publish(msg)
    time.sleep(0.005)                       # about 200 clock messages per wall second
```

The talker starts publishing, one message every two wall seconds: its 1 s timer is one second of *simulated* time.

3. Stop the talker and start the C++ one with the same parameter:

```bash
ros2 run demo_nodes_cpp talker --ros-args -p use_sim_time:=true
```

It publishes once per wall second whether `fake_clock.py` runs or not, because this demo makes its timer with `create_wall_timer`. Stop `fake_clock.py` to see it: the C++ talker carries on, where the Python talker of step 1 would have gone quiet again.

You are done when you can say, without running it, how often each talker publishes with `/clock` absent, at $r=0.5$ and at $r=2$.

### 5. The failure to diagnose: the node that stops when you add a second callback

The realistic version of section 2, and the shape it takes in a real week: a node works, you add one more thing to it, and it dies quietly.

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

**The fix**, as in section 2: put the timer and the client in different callback groups on a multi-threaded executor, or convert the call to `call_async` with a done-callback — the second is what to do in code you will maintain.

Practise this one deliberately, because no command hands you the answer: there is no error message, the symptom matches a dozen other causes, and the fix lives in a part of the code most people never touch. Recognising the *shape* — a callback waiting for a callback — is the whole skill.

### 6. What this page does not cover

What the middleware keeps for a subscription while no callback takes it — history depth, lifespan, deadline — is [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]]. Real-time execution — RT kernels, memory locking, response-time analysis of callback chains, and the rclc executor with its explicit execution order — is beyond this track; the Casini et al. ECRTS 2019 analysis of ROS 2 processing chains is the entry point. The code-level half of the same concern — keeping heap allocation, locks and exceptions out of a callback that runs every cycle — is [[02-foundations/algorithms/interview-code|11.7 §6]]. How a simulator actually publishes `/clock`, and what `use_sim_time` does to a controller under ros2_control, arrive with Gazebo in [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]. Recording and replaying bags is [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]. Intra-process communication and composition, which change the executor picture substantially, are the ROS 2 composition documentation.

### After reading · 읽고 나면

- Say what an executor does, why one thread means one callback at a time, and why a late timer loses firings rather than making them up.
- Predict, from a node's callback groups and its executor, which callbacks can overlap — and name the two changes a blocked control timer needs.
- Walk through the synchronous-call deadlock in five steps, and fix it two ways.
- Compute what a blocking callback costs P6 in lost firings and deaf time.
- Choose ROS time or the wall clock for a stamp and `create_timer` or `create_wall_timer` for a period, and predict both under a real-time factor.

### Self-check

1. You put your node on a `MultiThreadedExecutor` and the synchronous service call in your
   timer still deadlocks. Why?
2. A node stamps its messages with `time.time()`. Everything works in the lab and the numbers
   are wrong on a bag replay. What exactly goes wrong, and what should it call?
3. P6's calibration callback blocks for $200\,\mathrm{ms}$ once a second. You give it its own
   callback group and leave `rclpy.spin(node)` in `main`. How many control firings are lost
   per second, and why?
4. A node started with `use_sim_time:=true` publishes nothing and logs nothing, and
   `ros2 topic info /clock` shows `Publisher count: 0`. What is going on?
5. After a $200\,\mathrm{ms}$ stall, why does P6's $5\,\mathrm{ms}$ control timer fire once
   rather than forty times in a burst — and why is that the better behaviour?

> [!tip]- Answers
> 1. Because you did not assign callback groups. Everything created without a group joins the node's default group, which is mutually exclusive, so the node behaves as if it were single-threaded. The timer callback holds the group while waiting, and the future's hidden done-callback — which must run for the result to appear — cannot be scheduled in the same mutually exclusive group. Put the client and the timer in different groups, or in one shared reentrant group.
> 2. `time.time()` is the wall clock and ignores `/clock` entirely, so under replay it stamps data recorded two years ago with today's time; under simulation it drifts against the rest of the system by the real-time factor. Downstream TF lookups and any comparison with other message stamps then fail or silently extrapolate. It should call `self.get_clock().now()` on the node's clock, with `use_sim_time` set for the whole graph — and use `create_timer` rather than a wall timer if its period must follow simulated time.
> 3. Forty, as before. A callback group only permits parallelism; the single-threaded executor that `rclpy.spin` builds has one thread, and the calibration callback is holding it. It takes both changes — its own group *and* a `MultiThreadedExecutor` with at least two threads — and then the loss is zero.
> 4. The node is on simulated time and nothing publishes `/clock`, so its ROS time reads zero and never advances; every timer made on the node clock waits forever for a period that never elapses. Start the simulator or `ros2 bag play --clock`, or set `use_sim_time` back to false. No error is raised, because from the node's point of view nothing is wrong.
> 5. A timer that runs late moves its next firing to the next whole multiple of its period (`rcl_timer_call`), so the forty missed periods are skipped, not queued. Forty commands computed back to back on the same state would carry no new information; one command on the newest state is what a controller wants — provided you know the forty are gone, because no log says so.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]] and this page's controller node (control timer every $5\,\mathrm{ms}$, `/goal` every $20\,\mathrm{ms}$, calibration timer once a second). One knob changes: the calibration callback now blocks for $D=130\,\mathrm{ms}$. Budget $70\,\mathrm{ms}$. No new simulator.

1. **Draw.** The picture's two lanes for $D=130\,\mathrm{ms}$: a single-threaded executor with every callback in the default group, and a two-thread `MultiThreadedExecutor` with the calibration timer in its own mutually exclusive group. Mark every control firing that falls due in $(0,130]\,\mathrm{ms}$ and every goal arrival, filled if it runs on time and hollow if it does not.
2. **Derive.** (a) On the single-threaded executor, how many control firings fall due during the calibration callback, how many run on time, and how many goals arrive? (b) What fraction of each second is the controller deaf, and how many of its $200$ firings per second are lost? (c) Firings lost per second under each of: a `MultiThreadedExecutor` with no groups; its own group for calibration on `rclpy.spin`; both. (d) The same controller in a simulator at real-time factor $r=0.5$, with the control timer made by rclcpp's `create_wall_timer(5ms, …)`: how many control firings per goal, and at what rate in simulated time? And with `create_timer` on the node clock?
3. **Interpret.** P6's controller runs on a `MultiThreadedExecutor`, the calibration timer was given a `MutuallyExclusiveCallbackGroup`, and control firings are still lost for exactly as long as calibration runs. `ros2 node list` shows the node and nothing is logged. Name two causes this page predicts, and the line of code you would read to confirm each.

> [!note]- How to draw it · 그리는 법
> - One horizontal time axis in milliseconds, shared by both executors, with a lane per thread.
> - Draw each callback as a bar on the thread that runs it, from when it starts to when it returns.
> - Mark the control timer's firings every $5\,\mathrm{ms}$ on or above the lane: filled if the callback runs at that instant, hollow if it falls due while the thread is busy.
> - Mark each goal arrival every $20\,\mathrm{ms}$ under the lane, and say where it waits — in the middleware, when no thread takes it.
> - Label every bar with its callback group, and write the count of filled and hollow marks beside each lane, so the two executors compare at a glance.

> [!tip]- Solutions
> 1. Single-threaded: one bar from $0$ to $130\,\mathrm{ms}$ on thread 1; $26$ hollow control marks at $5,10,\ldots,130$; $6$ goal arrivals at $20,40,\ldots,120$, waiting in the middleware. Two threads: the same bar on thread 1, labelled with the calibration group; $26$ filled control marks and $6$ goal callbacks on thread 2, in the default group.
> 2. (a) $130/5=26$ fall due and $0$ run on time; $6$ goals arrive, at $20,\ldots,120$. (b) $130/1000=13\,\%$; $26$ of $200$. (c) $26$, $26$, $0$ — the default group is mutually exclusive, a single-threaded executor has one thread, and only both changes together free the timer. (d) Each firing covers $rT=0.5\times5=2.5\,\mathrm{ms}$ of simulated time, so $20/2.5=8$ firings per goal, at $400\,\mathrm{Hz}$ simulated; with `create_timer`, $5\,\mathrm{ms}$ simulated, $4$ per goal, $200\,\mathrm{Hz}$.
> 3. (i) The control timer and calibration share a group after all: either the control timer was created with `callback_group=` set to the calibration group, or the calibration timer was created without that argument and so sits in the default group with the control timer — read the `create_timer` calls. (ii) The executor has one thread, `MultiThreadedExecutor(num_threads=1)` — read the line that constructs it. (In rclpy a weaker third cause is a calibration that computes in pure Python instead of waiting: then the firings run, but late, because of the interpreter lock.)

### Sources

- ROS 2 Jazzy documentation — Concepts: Executors (executor types, callback groups, wait set, scheduling semantics).
- ROS 2 Jazzy documentation — How-to Guides: Using Callback Groups (deadlock example, working and non-working configurations).
- ROS 2 design article — Clock and Time (SystemTime, SteadyTime, ROSTime, the `/clock` time source, `use_sim_time`, time jumps).
- Source, Jazzy branches: `rcl/src/rcl/timer.c` (`rcl_timer_call` skips missed periods), `rclpy/executors.py` (`MultiThreadedExecutor`), the `demo_nodes_py` and `demo_nodes_cpp` talkers (`create_timer` versus `create_wall_timer`), `ros2bag` play verb (`--clock`).
- Python documentation — `sys.setswitchinterval` (the thread switch interval, 5 ms by default).
- Daniel Casini, Tobias Blass, Ingo Lütkebohle, Björn Brandenburg, "Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling", ECRTS 2019.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 돌아가는 시스템에서 막힌 executor와 엉뚱한 시계를 읽는 노드를 알아보고, 각각을 두 줄 수정으로 고칠 정도. Executor의 형식적 타이밍 분석을 할 정도는 아니다.
> **Working** — enough to recognise and fix a blocked executor and a node on the wrong clock, not to do formal timing analysis.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]](타이머, 퍼블리셔, 서브스크라이버를 써 봤다), [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]](서비스 클라이언트를 써 봤고, 이 페이지가 풀어 주는 교착을 남긴 막히는 호출을 만났다), [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]](콜백이 가져가지 않는 동안 미들웨어가 무엇을 들고 있는가). 숫자는 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P6이다. 기준 환경은 Ubuntu 24.04의 **ROS 2 Jazzy Jalisco**. 워크스페이스는 필요 없고, 실습은 커맨드라인과 평범한 Python 파일로 돌아간다.
> 25.2, 25.3 and 25.5 are assumed, with P6 from 0.6; everything runs on ROS 2 Jazzy on Ubuntu 24.04 without a workspace.

> [!note] 처음이라면 · First pass
> 그림과 대상으로 한 번 끝까지를 보고 1절과 2절을 읽는다. 스레드 하나는 한 번에 콜백 하나를 돌리고, 콜백 그룹은 어떤 콜백끼리 겹쳐도 되는지를 정한다 — 2절 끝의 교착은 보자마자 알아봐야 할 모양이다. 3절(시간)은 1–2절에 기대지 않으므로 따로 읽어도 되고, 4절이 그 실습이다. 5절은 연습해 둘 executor 실패, 6절은 나머지가 어디 있는지다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6** — 1차원 카트와 그 시계 — 를 제어기 노드 안에서 본다. [[04-robotics/ros2/nodes-topics-messages|25.2]]의 타이머 구동 제어기에 콜백을 하나 더한 것이다. 주기와 예산은 P6이 고정하고, 세 번째 콜백은 이 페이지의 것이다.

| 콜백 | 발화 주기 | 실행 시간 | 하는 일 |
|---|---|---|---|
| 제어 타이머 | $T_{\text{ctrl}}=5\,\mathrm{ms}$ ($200\,\mathrm{Hz}$) | $5\,\mathrm{ms}$보다 훨씬 짧음 | 엔코더를 읽고, 저장된 가장 새 목표를 쓰고, 모터 명령을 발행한다 |
| `/goal` 서브스크립션, `on_goal` | $T_{\text{vision}}=20\,\mathrm{ms}$ ($50\,\mathrm{Hz}$) | $5\,\mathrm{ms}$보다 훨씬 짧음 | 타이머가 쓸 가장 새 목표를 저장한다 |
| 보정 타이머 — **이 페이지 고유** | $1\,\mathrm{s}$ | $D=200\,\mathrm{ms}$ | 네트워크 공유 폴더에서 레일 보정값을 다시 읽는다. 그동안 내내 파일을 기다리며 막혀 있다 |

종단 간 예산은 P6의 $B=70\,\mathrm{ms}$, 카메라 노출 중간부터 힘이 걸리기까지다. 세 콜백 모두 콜백 그룹을 지정하지 않고 만들었고, 노드는 `rclpy.spin(node)`로 돈다. 이 두 사실이 왜 중요한지가 1절과 2절이다.

*범위: 이 페이지는 노드의 콜백을 누가 돌리는지 — executor와 콜백 그룹, 동기 호출 교착까지 — 와 노드가 어느 시계를 읽는지 — 벽시계, steady, ROS 시간, `/clock`과 `use_sim_time` — 를 가르친다. 콜백이 가져가지 않는 동안 미들웨어가 무엇을 들고 있는지는 [[04-robotics/ros2/qos-executors-time|25.5]]의 QoS history이고, 콜백 체인의 실시간 스케줄링은 이 트랙 밖이다(6절).*

### 그림으로 먼저 보기: 200 ms 콜백 동안의 P6 제어기, 스레드 하나와 둘 · The picture

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="0에서 200 ms 축 위에서 보정 콜백이 200 ms 동안 막는 P6 제어기 노드. A는 스레드 하나에 모든 콜백이 기본 그룹: 보정 막대가 스레드를 채우고, 5 ms마다 도래하는 제어 발화 40번은 제때 도는 것이 없어 속이 비어 있으며, 20 ms마다 오는 목표 10개는 미들웨어에서 기다린다. B는 스레드 둘에 보정 타이머가 자기 그룹: 보정 막대가 스레드 1을 채우는 동안 스레드 2가 제어 발화 40번과 목표 콜백 10번을 모두 제때 돌린다.">
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">A · rclpy.spin(node): 스레드 하나, 모든 콜백이 기본 그룹</text>
  <text x="70" y="40" font-size="11" fill-opacity="0.7" fill="currentColor">제어 타이머: 5 ms마다 40번 도래 — 제때 도는 것 없음</text>
  <path d="M81.25 58v-10M92.5 58v-10M103.75 58v-10M115 58v-10M126.25 58v-10M137.5 58v-10M148.75 58v-10M160 58v-10M171.25 58v-10M182.5 58v-10M193.75 58v-10M205 58v-10M216.25 58v-10M227.5 58v-10M238.75 58v-10M250 58v-10M261.25 58v-10M272.5 58v-10M283.75 58v-10M295 58v-10M306.25 58v-10M317.5 58v-10M328.75 58v-10M340 58v-10M351.25 58v-10M362.5 58v-10M373.75 58v-10M385 58v-10M396.25 58v-10M407.5 58v-10M418.75 58v-10M430 58v-10M441.25 58v-10M452.5 58v-10M463.75 58v-10M475 58v-10M486.25 58v-10M497.5 58v-10M508.75 58v-10M520 58v-10" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 2" fill="none"/>
  <text x="12" y="75" font-size="11" fill-opacity="0.85" fill="currentColor">스레드 1</text>
  <rect x="70" y="61" width="450" height="22" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="295" y="76" font-size="11" text-anchor="middle" fill="currentColor">보정 콜백 200 ms, 파일을 기다리는 중</text>
  <path d="M111 89H119L115 97zM156 89H164L160 97zM201 89H209L205 97zM246 89H254L250 97zM291 89H299L295 97zM336 89H344L340 97zM381 89H389L385 97zM426 89H434L430 97zM471 89H479L475 97zM516 89H524L520 97z" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="70" y="114" font-size="11" fill-opacity="0.7" fill="currentColor">/goal: 20 ms마다 목표 10개 도착, 미들웨어에서 대기</text>
  <text x="12" y="150" font-size="12" fill-opacity="0.8" fill="currentColor">B · 스레드 둘, 보정 타이머는 자기 그룹</text>
  <text x="12" y="177" font-size="11" fill-opacity="0.85" fill="currentColor">스레드 1</text>
  <rect x="70" y="163" width="450" height="22" rx="3" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="295" y="178" font-size="11" text-anchor="middle" fill="currentColor">보정 그룹: 같은 200 ms</text>
  <text x="12" y="215" font-size="11" fill-opacity="0.85" fill="currentColor">스레드 2</text>
  <line x1="70" y1="211" x2="520" y2="211" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <path d="M81.25 222v-22M92.5 222v-22M103.75 222v-22M115 222v-22M126.25 222v-22M137.5 222v-22M148.75 222v-22M160 222v-22M171.25 222v-22M182.5 222v-22M193.75 222v-22M205 222v-22M216.25 222v-22M227.5 222v-22M238.75 222v-22M250 222v-22M261.25 222v-22M272.5 222v-22M283.75 222v-22M295 222v-22M306.25 222v-22M317.5 222v-22M328.75 222v-22M340 222v-22M351.25 222v-22M362.5 222v-22M373.75 222v-22M385 222v-22M396.25 222v-22M407.5 222v-22M418.75 222v-22M430 222v-22M441.25 222v-22M452.5 222v-22M463.75 222v-22M475 222v-22M486.25 222v-22M497.5 222v-22M508.75 222v-22M520 222v-22" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" fill="none"/>
  <path d="M111 228H119L115 236zM156 228H164L160 236zM201 228H209L205 236zM246 228H254L250 236zM291 228H299L295 236zM336 228H344L340 236zM381 228H389L385 236zM426 228H434L430 236zM471 228H479L475 236zM516 228H524L520 236z" fill="currentColor" fill-opacity="0.9" stroke="none"/>
  <text x="70" y="252" font-size="11" fill-opacity="0.8" fill="currentColor">기본 그룹: 제어 발화 40번과 목표 콜백 10번, 모두 제때</text>
  <line x1="70" y1="266" x2="520" y2="266" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7"/>
  <path d="M70 266v5M160 266v5M250 266v5M340 266v5M430 266v5M520 266v5" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.7" fill="none"/>
  <text x="70" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">0</text>
  <text x="160" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">40</text>
  <text x="250" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">80</text>
  <text x="340" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">120</text>
  <text x="430" y="286" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">160</text>
  <text x="526" y="286" font-size="11" text-anchor="end" fill-opacity="0.75" fill="currentColor">200 ms</text>
</svg>

보정 콜백이 막는 $200\,\mathrm{ms}$ 동안의 P6 제어기 노드를 두 executor 위에서 본 것이다. A에서는 `rclpy.spin`이 스레드 하나를 주고 모든 콜백이 기본 그룹에 있으므로, $5\,\mathrm{ms}$마다 도래하는 제어 발화 $40$번은 하나도 제때 돌지 못하고 $20\,\mathrm{ms}$마다 발행되는 목표 $10$개는 미들웨어에서 기다린다. B에서는 보정 타이머가 자기 mutually exclusive 그룹을 갖고 executor에 두 번째 스레드가 있으므로, 발화 $40$번과 목표 콜백 $10$번이 모두 스레드 2에서 제때 돈다.

### 대상으로 한 번 끝까지: 200 ms 콜백이 P6 제어기에서 앗아 가는 것, 콜백 그룹이 되찾아 주는 것 · Worked case

주기 둘과 길이 하나. 아래의 모든 개수가 이들의 비이기 때문이다.

$$T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=5\,\mathrm{ms},\qquad T_{\text{vision}}=\frac{1}{50\,\mathrm{Hz}}=20\,\mathrm{ms},\qquad D=200\,\mathrm{ms}$$

**1단계 — 스레드 하나가 200 ms로 하는 일.** $t=0$에 보정 타이머가 울리고 그 콜백이 $D$ 동안 막힌다. 노드는 `rclpy.spin(node)` 위에 있고, 이것은 단일 스레드 *executor* — 미들웨어에서 준비된 콜백을 가져와 실행하는 루프, 여기서는 스레드 하나로 한 번에 하나씩(1절) — 를 만든다. 그래서 $t=200\,\mathrm{ms}$까지 노드의 다른 것은 아무것도 돌지 않고, 그동안

$$\frac{D}{T_{\text{ctrl}}}=\frac{200}{5}=40\ \text{번의 제어 발화 도래},\qquad \frac{D}{T_{\text{vision}}}=\frac{200}{20}=10\ \text{개의 목표 발행}$$

이다. 마흔 번 중 제때 도는 것은 하나도 없고 나중에 메워지지도 않는다. 늦게 도는 타이머는 한 번만 울리고 놓친 주기는 건너뛰기 때문이다(1절). 그래서 모터는 마지막 명령을 $200\,\mathrm{ms}$ 동안 붙들고 있다. 제어 주기 마흔 개이고, P6의 $70\,\mathrm{ms}$ 예산 전체보다 $130\,\mathrm{ms}$ 길다. 목표 열 개는 미들웨어에서 기다리고, 무엇이 살아남는지는 서브스크립션의 QoS depth가 정한다. `KEEP_LAST (5)`에서는 처음 넘겨받는 것이 이미 $80\,\mathrm{ms}$ 된 것이다([[04-robotics/ros2/qos-executors-time|25.5]]의 대상으로 한 번 끝까지).

**2단계 — 손해의 비율.** 보정은 1초에 한 번 울리므로 제어기는

$$\frac{D}{1000\,\mathrm{ms}}=\frac{200}{1000}=20\,\%$$

의 시간 동안 귀가 먹는다. 길이 $D$의 막힌 구간이 매초 한 번 돌아오기 때문이다. 매초 발화 $200$번 중 $40$번을 잃고, 어떤 로그에도 남지 않는다.

**3단계 — 혼자서는 아무것도 못 하는 변경 둘.**

- *멀티 스레드* executor — 같은 루프에 스레드 풀을 붙인 것(1절) — 로 spin하고 나머지는 그대로 둔다. 여전히 $40$번을 잃는다. 세 콜백이 모두 노드의 기본 *콜백 그룹* — executor가 병렬로 돌려도 되는지를 정해 두는 콜백 묶음 — 에 있고, 기본 그룹은 mutually exclusive, 곧 그 콜백들은 스레드가 몇 개든 서로 겹치지 않기 때문이다(2절).
- 보정 타이머에 자기 그룹을 주고 `rclpy.spin`은 그대로 둔다. 여전히 $40$번을 잃는다. 그룹은 병렬을 허용할 뿐이고, 단일 스레드 executor에는 스레드가 하나뿐인데 그것이 바쁘다.

**4단계 — 둘 다 함께.** 보정 타이머는 자기 `MutuallyExclusiveCallbackGroup`에 두고, 제어 타이머와 `on_goal`은 기본 그룹에 남기고, 스레드가 둘 이상인 `MultiThreadedExecutor`를 쓴다. 이제 보정이 스레드 하나를 $200\,\mathrm{ms}$ 동안 차지하는 사이 다른 스레드가 발화 마흔 번과 목표 콜백 열 번을 모두 제때 돌린다. 손실은 매초 $40$번에서 $0$번이 된다. 기본 그룹은 두 번째의 쓸모 있는 일을 계속한다. 제어 타이머와 `on_goal`은 여전히 서로 겹치지 않으므로, `on_goal`이 쓰고 있는 도중의 저장된 목표를 타이머가 읽는 일이 없다. 대가는 그 거울상이다. 이제 보정이 제어와 *동시에* 돌므로, 새 보정값은 지역 변수에서 다 만든 다음 마지막에 대입 한 번으로 넘겨야 한다.

**5단계 — 끝나지 않는 판.** 파일 읽기를 보정 서비스에 대한 동기 호출 `client.call(...)`로 바꾸고, 클라이언트를 기본 그룹에 만든다. [[04-robotics/ros2/services-actions-parameters|25.3]]의 막히는 호출이다. 이제 콜백은 $200\,\mathrm{ms}$를 기다리지 않는다. 자기와 같은 mutually exclusive 그룹의 다른 콜백만이 넘겨줄 수 있는 응답을 기다리므로 영원히 기다린다. $D$는 끝이 없고, 그때부터의 발화는 전부 잃으며, 노드는 여전히 `ros2 node list`에 나온다. 왜 그런지는 2절이 유도하고, 4단계와 같은 두 변경이 이것도 고친다.

### 1. Executor: 스레드 하나인가 여럿인가

오류를 내지 않는 ROS 2 실패 셋 중 둘이 이 페이지에 있다. 셋째, 호환되지 않는 QoS 쌍은 [[04-robotics/ros2/qos-executors-time|25.5 §1]]이다.

- **Executor.** 어떤 콜백이, 같은 executor 스레드가 실행해야 하는 다른 콜백만이 만들어 낼 수 있는 것을 기다리며 막힌다. 노드는 응답을 멈춘다. 죽지도 않고, 로그도 남기지 않고, 퍼블리셔는 광고된 채로 남는다. 이 절, 2절, 5절이다.
- **시간.** 시스템 나머지가 시뮬레이션 시간이나 재생 시간 위에서 도는데 어떤 노드가 벽시계를 읽는다. 그 노드의 타임스탬프는 무엇과도 맞지 않고, 타임아웃은 엉뚱한 순간에 터지고, 내놓는 값은 전부 그럴듯해 보인다. 3절과 4절이다.

콜백은 저절로 돌지 않는다. **Executor**(실행기)가 OS 스레드 하나 이상을 소유하고, *wait set*을 통해 미들웨어에 도착한 메시지와 만료된 타이머를 감시하며 해당 콜백을 호출한다. `rclpy.spin(node)`와 `rclcpp::spin(node)`는 단일 스레드 executor를 만들고 노드를 붙여 spin하는 것의 축약이다.

> **Executor의 정의.** **Executor**는 *한 프로세스 안의 스케줄러 객체*다. 노드도 스레드도 아니다. 정의 조건은 셋이다. **엔티티를 들고 있다.** 붙인 노드들의 서브스크립션, 타이머, 서비스, 클라이언트다. **wait set 위에서 기다린다.** wait set은 *어느* 엔티티가 준비됐는지 — 만기된 타이머, 미들웨어에 메시지가 있는 토픽 — 만 알릴 뿐, 몇 개인지 얼마나 오래됐는지는 알리지 않는다. 그리고 **준비된 콜백을 자기 스레드 하나에서 끝까지 돌린다.** 2절의 콜백 그룹이 정한 한도 안에서다.
>
> $$N_{\text{run}}(t)\le n_{\text{th}},\qquad n_{\text{late}}=\Big\lfloor\frac{D}{T}\Big\rfloor$$
>
> 여기서 $N_{\text{run}}(t)$는 시각 $t$에 돌고 있는 콜백 수, $n_{\text{th}}$는 스레드 수(`rclpy.spin`이면 $1$), $n_{\text{late}}$는 콜백 하나가 하나뿐인 스레드를 $D$ 동안 붙드는 사이 도래하는 주기 $T$ 타이머의 발화 수다. 늦은 타이머는 놓친 주기를 건너뛰므로 그중 어느 것도 나중에 재생되지 않는다.
>
> - **예**: 보정이 $D=200\,\mathrm{ms}$ 동안 막히는 사이 `rclpy.spin` 위의 P6 제어기. $\lfloor200/5\rfloor=40$번의 제어 발화가 늦고, 매초 내야 할 $200$번 중 $40$번이다.
> - **비예**: 목표를 줄 세워 두는 executor. 그동안 도착하는 목표 $200/20=10$개는 executor에 들어오지 않고 서브스크립션의 QoS depth 아래 미들웨어에서 기다리므로, `KEEP_LAST (5)`는 어떤 콜백이 돌기도 전에 다섯을 잃는다. 스레드를 늘려도 되찾을 수 없으니, executor와 QoS는 함께 정한다.

rclcpp는 `SingleThreadedExecutor`, `MultiThreadedExecutor`, 그리고 노드의 엔티티 목록(퍼블리셔, 서브스크립션, 타이머, 서비스, 클라이언트 — 콜백을 가질 수 있는 모든 것)을 캐시했다가 엔티티가 추가·제거될 때만 다시 만드는 `StaticSingleThreadedExecutor`를 제공한다. Jazzy의 executor 재작성 이후로는 모든 것을 초기화 때 만드는 노드에만 쓸 수 있다는 제한이 없어졌다. [Jazzy 소스](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/src/rclcpp/executors/static_single_threaded_executor.cpp)는 엔티티가 추가되거나 제거될 때마다 목록을 다시 모으고, Executors 개념 문서에는 그런 노드에만 쓰라는 예전 권고가 아직 남아 있다. Jazzy에는 실험적인 `EventsExecutor`도 있다. rclpy는 앞의 둘을 제공한다.

초심자가 틀리는 귀결 셋:

- **스레드 하나는 한 번에 콜백 하나를 뜻하고, 긴 콜백은 모든 것을 지연시킨다.** 200 Hz 제어 타이머를 가진 P6 제어기에서 200 ms짜리 콜백은 "뒤에서 도는" 것이 아니라 타이머를 세운다. 발화 마흔 번어치다(대상으로 한 번 끝까지). 도착한 메시지는 클라이언트 라이브러리 층에 쌓이지 않고 콜백이 가져갈 때까지 미들웨어에 남는다. ROS 1과의 의도적인 차이이고, 그 정체 구간에서 무엇이 살아남는지는 ROS 쪽 버퍼가 아니라 QoS depth가 정한다는 뜻이다. *keep last*에서는 미들웨어가 가장 최근 샘플 N개만 들고 있고, 새 샘플이 올 때마다 가장 오래된 것이 밀려난다([[04-robotics/ros2/qos-executors-time|25.5 §2]]).
- **늦은 타이머는 따라잡지 않는다.** 타이머 콜백이 마침내 늦게 돌면, 타이머는 다음 발화를 자기 주기의 다음 정수배로 옮기고 놓친 발화는 전부 건너뛴다. 두 클라이언트 라이브러리 아래의 C 계층인 rcl이 `rcl_timer_call`에서 그렇게 한다. 그래서 멈췄던 5 ms 타이머는 나중에 몰아서 쏘는 것이 아니라 발화를 잃는다. 모터에는 더 친절하고, 로그에는 보이지 않는다.
- **순서는 FIFO가 아니라 라운드 로빈이다.** wait set은 어떤 토픽에 메시지가 *있는지*만 보고할 뿐 몇 개인지, 얼마나 오래됐는지는 보고하지 않는다. 그래서 과부하된 executor는 도착 순서가 아니라 토픽을 돌아가며 처리한다.

rclpy에 대한 단서 하나. `MultiThreadedExecutor`의 스레드들은 Python의 전역 인터프리터 락(GIL)을 공유한다. 그래서 두 Python 콜백이 정말로 동시에 도는 것은 한쪽이 기다리는 동안 — 파일, 소켓, sleep, 서비스 응답 — 이거나 락을 푸는 C 코드 안에 있을 때뿐이다. 순수 Python으로 200 ms 동안 계산하는 콜백은 여전히 다른 콜백을 늦추고, 다른 콜백은 자기 차례를 Python의 스레드 전환 간격, 기본 $5\,\mathrm{ms}$까지 기다릴 수 있다. P6의 보정 콜백을 파일을 *기다리는* 것으로 둔 이유가 이것이다. rclcpp의 스레드에는 이런 락이 없다.

### 2. 콜백 그룹, 그리고 25.3이 남겨 둔 교착

콜백은 **콜백 그룹**(callback group)으로 묶을 수 있다. rclcpp에서는 `create_callback_group`으로, rclpy에서는 그룹 클래스를 생성해서 만든다. 두 종류가 있다.

- **Mutually exclusive**: 이 그룹의 콜백들은 서로 병렬로 실행되지 않는다. 사실상 그룹이 자기만의 단일 스레드 executor를 가진 것처럼 동작한다.
- **Reentrant**: 이 그룹의 콜백은 병렬로 실행될 수 있고, *같은* 콜백의 동시 실행도 허용된다.

*다른* 그룹의 콜백끼리는 언제나 병렬 실행이 가능하다. 그룹을 지정하지 않고 만든 것은 전부 노드의 **기본 콜백 그룹에 들어가고, 그것은 mutually exclusive다.** 직접 만든 그룹은 참조를 붙들고 있어야 한다. 수거되면 그 콜백은 더 이상 트리거되지 않는다.

> **콜백 그룹의 정의.** **콜백 그룹**은 *한 노드의 콜백을 묶어 동시 실행 규칙 하나를 붙인 집합*이다. 허가이지 스레드가 아니다. 정의 조건은 셋이다. **모든 콜백은 정확히 한 그룹에 속한다.** 따로 지정하지 않으면 노드의 기본 그룹이고, 엔티티는 자기가 만들어 내는 콜백에 — 서비스 호출의 숨은 done-callback까지 — 자기 그룹을 물려준다. **그룹의 종류가 그 안의 규칙을 정한다.** *mutually exclusive*는 그 콜백을 한 번에 하나만, *reentrant*는 같은 콜백이라도 몇 개든 돌린다. 그리고 **다른 그룹의 콜백끼리는 겹쳐 돌 수 있다.** 단, executor에 있는 스레드 위에서만이다.
>
> $$N^{g}_{\text{run}}(t)\le 1\ \ (g\in\mathcal{G}_{\text{ME}}),\qquad N_{\text{run}}(t)\le n_{\text{th}}$$
>
> 여기서 $\mathcal{G}_{\text{ME}}$는 노드의 mutually exclusive 그룹들, $N^{g}_{\text{run}}(t)$는 시각 $t$에 도는 그룹 $g$의 콜백 수다. 두 한도가 매 순간 함께 걸리므로, 콜백 둘을 동시에 돌리려면 그룹 둘(또는 reentrant 그룹 하나) *그리고* 스레드 둘이 필요하다.
>
> - **예**: P6의 보정 타이머는 자기 mutually exclusive 그룹에, 제어 타이머와 `on_goal`은 기본 그룹에 두고 스레드 둘로 돌린다. 보정이 스레드 하나를 $200\,\mathrm{ms}$ 붙드는 동안 다른 스레드가 제어 발화 $40$번과 목표 콜백 $10$번을 모두 돌리고, 손실은 $0$이다.
> - **비예**: 같은 그룹 배치를 `rclpy.spin`에 올린 경우. 그룹은 겹침을 허락하지만 $n_{\text{th}}=1$이 노드를 한 번에 콜백 하나로 묶으므로 여전히 $40$번을 잃는다. 해법이 언제나 그룹과 스레드의 짝인 이유다.

그 기본값이 교착의 전말이다. 노드의 모든 엔티티가 기본 그룹을 쓰면, *멀티 스레드 executor를 줬더라도* 노드는 단일 스레드 executor 위에 있는 것과 똑같이 동작한다. `MultiThreadedExecutor`를 고르고 그룹을 하나도 지정하지 않으면 얻는 것이 없다.

이제 [[04-robotics/ros2/services-actions-parameters|25.3 서비스, 액션, 파라미터, 라이프사이클]]이 남겨 둔 실패다. 타이머 콜백이 동기 서비스 호출을 한다. rclpy의 `client.call(request)`, 또는 rclcpp에서 `async_send_request`가 돌려준 future를 기다리는 것.

```python
def _timer_cb(self):
    self.get_logger().info('Sending request')
    _ = self.client.call(Empty.Request())          # 여기서 영원히 막힌다
    self.get_logger().info('Received response')
```

`Sending request`가 한 번 보인다. `Received response`는 영영 없고, 타이머는 다시 울리지 않는다. 서버 쪽 터미널에는 요청을 받아 응답했다고 찍힌다.

기전: 동기 호출은 콜백이 없는 것이 아니라 콜백이 *숨어 있는* 것이다. 단계별로:

1. 타이머 콜백이 실행을 시작하고 `client.call()`을 부르며, 이 호출은 결과를 기다린다.
2. 클라이언트는 자기 콜백 그룹을 future에 넘기고, 결과는 그 future의 done-callback이 실행되어야만 나온다.
3. 그 done-callback과 타이머 콜백은 같은 mutually exclusive 그룹에 있으므로, 타이머 콜백이 실행 중인 동안 done-callback은 시작할 수 없다.
4. 타이머 콜백은 결과를 기다리며 여전히 스택에 남아 있다. 그래서 done-callback은 영영 스케줄되지 못하고, 기다림은 끝나지 않는다.
5. 막힌 타이머 콜백은 자기 다음 발화도 막으므로, 노드는 응답 하나를 놓치는 정도가 아니라 완전히 조용해진다.

규칙:

> 콜백 안에서 동기 호출을 한다면, 그 콜백과 클라이언트는 **서로 다른 콜백 그룹** 안에 있거나 **같은 reentrant 그룹** 안에 있어야 한다 — 그리고 노드는 멀티 스레드 executor 위에 있어야 한다.

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

### 3. 시간: `use_sim_time`, `/clock`, 그리고 벽시계

ROS 2는 시간 추상을 셋 준다. **SystemTime**(머신의 시계), **SteadyTime**(단조 증가. 하드웨어 타임아웃용이며 다른 둘과 비교 불가), 그리고 **ROSTime**. 발행되거나 메시지 스탬프와 비교되는 모든 것에는 ROSTime을 써야 한다.

ROSTime은 *ROS 시간 소스가 활성화되기 전까지는* SystemTime과 같은 값을 보고한다. 활성화 조건은 노드의 `use_sim_time` 파라미터가 설정되는 것이다. 그 뒤로 노드의 시계는 `/clock` 토픽(`rosgraph_msgs/msg/Clock`)으로 받은 최신 값을 돌려준다. 이 토픽은 시뮬레이터나 bag 재생이 발행한다. bag은 토픽을 녹화한 것이고 `ros2 bag play`가 그것을 다시 발행한다([[04-robotics/ros2/debugging-data-reproducibility|25.10]]).

> **ROS 시간의 정의.** **ROS 시간**은 *노드 자신의 시계가 돌려주는 값*이다. 세 시계 종류 가운데 시뮬레이터나 재생을 따라갈 수 있는 것은 이것뿐이다. 정의 조건은 셋이다. `use_sim_time`이 거짓이면 **시스템 시간과 같다.** 참이면 **`/clock`으로 받은 가장 최근 값**이고, 첫 메시지 전에는 **0**, 곧 *초기화 안 됨*이다. 그리고 **단조 증가가 아니다.** 루프 재생은 시간을 뒤로 되돌린다.
>
> $$t_{\text{ROS}}=\begin{cases}t_{\text{sys}} & \texttt{use\_sim\_time}=\text{false}\\ t_{\text{clock}} & \texttt{use\_sim\_time}=\text{true}\end{cases}$$
>
> 여기서 $t_{\text{sys}}$는 머신의 시계, $t_{\text{clock}}$은 가장 새 `/clock` 스탬프다. 노드 시계 타이머는 $t_{\text{ROS}}$를 기다리고, 벽시계 타이머는 그러지 않는다.
>
> - **예**: 실시간 계수 $r=0.5$(바로 아래에서 정의)로 시뮬레이션되는 P6에서 `use_sim_time`을 켜면, 노드 시계의 $5\,\mathrm{ms}$ 타이머는 벽시계 $10\,\mathrm{ms}$마다 울리고 목표 하나당 여전히 $20/5=4$번이다.
> - **비예**: 같은 노드의 rclcpp `create_wall_timer(5ms, …)`는 ROS 시간을 읽지 않으므로 발화 하나가 시뮬레이션 시간 $0.5\times5=2.5\,\mathrm{ms}$를 덮는다. 목표당 $8$번, 시뮬레이션 시간으로 $400\,\mathrm{Hz}$다. 엉뚱한 시계 위의 주기는 정확히 $r$만큼 어긋나고, 그렇다고 말해 주는 로그는 없다.

**실시간 계수.** 시뮬레이터는 벽시계와 같은 속도로 간다고 약속하지 않는다. 그 *실시간 계수*(real-time factor) $r$은 실행의 같은 구간에서 시뮬레이션 시간과 벽시계 시간의 비다.

$$r=\frac{\Delta t_{\text{sim}}}{\Delta t_{\text{wall}}}$$

여기서 $\Delta t_{\text{sim}}$은 그동안 `/clock`이 나아간 양이고 $\Delta t_{\text{wall}}$은 그동안 흐른 벽시계 시간이다. 그래서 $r=1$은 실시간이고, $r=0.5$는 시뮬레이션 1초에 벽시계 2초가 걸린다는 뜻이며 — 노트북에서 무거운 장면을 돌리면 이렇게 된다 — $r>1$은 실시간보다 빠르다. 이것은 실행의 성질이지 어느 노드의 성질도 아니다. 반례로 `/clock`의 발행 주기는 시간을 얼마나 잘게 자르는지를 말할 뿐, 시간이 얼마나 빨리 흐르는지는 말하지 않는다. 이것이 중요한 이유는 시뮬레이션 시간으로 잰 주기는 벽시계 위에서 $1/r$배로 늘어나고, 벽시계로 잰 주기는 전혀 늘어나지 않기 때문이다.

설계할 때 감안해야 할 귀결들:

- 시간 0은 에포크가 아니다. **초기화되지 않았다는 뜻이다.** `/clock` 발행 전에 뜬 노드는 첫 clock 메시지까지 0을 읽는다.
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

시뮬레이션에서 벽시계 버전은 다른 모든 타임스탬프에 대해 실시간 계수만큼 어긋나고, bag 재생에서는 2년 전 센서 데이터에 오늘 날짜를 찍는다. 그러면 그 값에 대한 TF 조회 — [[04-robotics/robot-systems-deployment|10 §4]]의 변환 트리 — 는 실패하거나 조용히 외삽한다. 증상이 "결과 없음"이 아니라 "더 나쁜 결과"인 드문 버그다.

타이머도 같은 분기를 갖는다. rclpy의 `create_timer(period, callback)`은 노드 시계를 쓰므로 시뮬레이션 시간을 따른다. rclcpp의 `create_wall_timer`는 의도적으로 벽시계를 쓰고 `/clock`을 따르지 **않으며**, `create_timer(period, callback, group)`이 노드 시계를 쓴다. 제어기가 시뮬레이션 시간으로 tick해야 한다면 후자가 필요하다. rclcpp 헤더의 경고도 기억하라. `rclcpp::Clock(RCL_ROS_TIME)`을 직접 생성하지 마라. 붙이지 않은 시계는 조용히 시스템 시간으로 돈다. `this->get_clock()`을 쓴다.

**계산: 시뮬레이터가 $r=0.5$로 도는 P6.** 위 정의에 따라 시뮬레이션 시간으로 $T$인 주기는 벽시계로 $T/r$이 걸리고, 벽시계로 $T$인 주기는 시뮬레이션 시간 $rT$를 덮는다. 시뮬레이션 속 카메라는 시뮬레이션 시간 $20\,\mathrm{ms}$마다, 곧 벽시계 $40\,\mathrm{ms}$마다 발행한다. `use_sim_time`을 켠 제어기 노드에서 rclpy의 `create_timer(0.005, …)`로 만든 타이머는 노드 시계를 따르므로 시뮬레이션 $5\,\mathrm{ms}$, 벽시계 $10\,\mathrm{ms}$마다 울리고, 목표 하나당 제어 발화는 P6의 설계대로 $20/5=4$번이다. 같은 제어기를 C++에서 `create_wall_timer(5ms, …)`로 만들면 벽시계 $5\,\mathrm{ms}$마다 울리고, 그것은

$$rT=0.5\times5\,\mathrm{ms}=2.5\,\mathrm{ms}\ \text{(시뮬레이션 시간)}$$

이므로 목표 하나당 $8$번, 시뮬레이션 자신의 시간으로 $400\,\mathrm{Hz}$ — P6 제어율의 두 배 — 로 울리고, 어떤 로그도 그렇다고 말하지 않는다. 시뮬레이션 시간을 아예 켜지 않은 제어기는 더 나쁘다. 그 시계는 약 $1.79\times10^{9}\,\mathrm{s}$(1970년 이후 초)를 읽는데 목표 스탬프는 시뮬레이터 시작부터 세므로, $70\,\mathrm{ms}$ 낡음 검사가 모든 목표를 거부하고 카트는 움직이지 않는다.

켜는 방법. 노드 하나는 커맨드라인에서, 시스템 전체는 런치 파일([[04-robotics/ros2/workspaces-packages-launch|25.4]])이 띄우는 모든 노드에:

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

### 4. 실습: 아무도 발행하지 않는 시계에 노드 올리기

source된 터미널 셋, 워크스페이스 없이 10분쯤. 3절의 두 타이머 호출이 같은 파라미터 아래에서 다르게 동작하는 것을 보여 준다.

1. Python 데모 talker를 시뮬레이션 시간으로 띄운다.

```bash
ros2 run demo_nodes_py talker --ros-args -p use_sim_time:=true
```

아무것도 찍히지 않고, 두 번째 터미널의 `ros2 topic echo /chatter`도 조용하다. 오류는 없다. 세 번째 터미널에서 진단한다.

```bash
ros2 param get /talker use_sim_time
ros2 topic info /clock
```

파라미터는 `True`이고, `/clock`은 `Publisher count: 0`에 서브스크립션이 적어도 하나다. talker가 아무도 발행하지 않는 시계를 듣고 있는 것이다. 시뮬레이션 시간 위의 노드는 `/clock`이 오기 전까지 0을 읽고 그 0은 나아가지 않으므로, 노드 시계 위에 `create_timer`로 만든 talker의 타이머는 영영 울리지 않는다.

2. 시계를 준다. 아래를 `fake_clock.py`로 저장하고 `python3 fake_clock.py`로 실행한다. 실시간 계수 0.5로 `/clock`을 발행한다.

```python
import time
import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock

RTF = 0.5                                   # 벽시계 1초당 시뮬레이션 초

rclpy.init()
node = Node('fake_clock')
pub = node.create_publisher(Clock, '/clock', 10)
start = time.monotonic()
while rclpy.ok():
    sim = RTF * (time.monotonic() - start)  # 시작 이후 시뮬레이션 초
    msg = Clock()
    msg.clock.sec = int(sim)
    msg.clock.nanosec = int((sim - int(sim)) * 1e9)
    pub.publish(msg)
    time.sleep(0.005)                       # 벽시계 1초에 clock 메시지 약 200개
```

talker가 발행을 시작하는데, 벽시계 2초에 한 번이다. 1초 타이머가 *시뮬레이션* 시간으로 1초이기 때문이다.

3. talker를 멈추고 같은 파라미터로 C++ talker를 띄운다.

```bash
ros2 run demo_nodes_cpp talker --ros-args -p use_sim_time:=true
```

`fake_clock.py`가 돌든 말든 벽시계 1초에 한 번 발행한다. 이 데모는 타이머를 `create_wall_timer`로 만들기 때문이다. `fake_clock.py`를 멈춰서 확인하라. C++ talker는 계속 발행하고, 1단계의 Python talker였다면 다시 조용해졌을 것이다.

두 talker 각각이 `/clock`이 없을 때, $r=0.5$일 때, $r=2$일 때 얼마나 자주 발행하는지 돌려 보지 않고 말할 수 있으면 끝난 것이다.

### 5. 진단할 실패: 콜백을 하나 더 붙이자 멈추는 노드

2절의 현실판이고, 실제 한 주에 나타나는 모양이다. 노드가 잘 돌던 중에 뭔가 하나를 더 붙였더니 조용히 죽는다.

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

**수정.** 2절과 같다. 멀티 스레드 executor 위에서 타이머와 클라이언트를 다른 콜백 그룹에 넣거나, 호출을 `call_async`와 done-callback으로 바꾼다. 계속 유지할 코드라면 후자가 답이다.

이것은 일부러 연습해 둘 값어치가 있다. 답을 대신 알려 주는 명령이 없기 때문이다. 오류 메시지가 없고, 증상이 다른 열두 가지 원인과 똑같고, 수정 지점이 대부분 손대지 않는 부분에 있다. *모양* — 콜백이 콜백을 기다린다 — 을 알아보는 것이 기술의 전부다.

### 6. 이 페이지가 다루지 않는 것

콜백이 가져가지 않는 동안 미들웨어가 서브스크립션을 위해 들고 있는 것 — history depth, lifespan, deadline — 은 [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]]이다. 실시간 실행 — RT 커널, 메모리 고정, 콜백 체인의 응답 시간 분석, 실행 순서를 명시하는 rclc executor — 는 이 트랙 밖이다. 시작점은 Casini 외의 ECRTS 2019 분석이다. 같은 문제의 코드 쪽 절반 — 매 주기 도는 콜백에서 힙 할당, 락, 예외를 빼내는 것 — 은 [[02-foundations/algorithms/interview-code|11.7 §6]]에 있다. 시뮬레이터가 `/clock`을 실제로 어떻게 발행하는지, ros2_control 아래에서 `use_sim_time`이 제어기에 무엇을 하는지는 Gazebo와 함께 [[04-robotics/ros2/simulation-and-control|25.7 시뮬레이션과 ros2_control]]에서 온다. bag의 기록과 재생은 [[04-robotics/ros2/debugging-data-reproducibility|25.10 디버깅, 데이터, 재현성]]이다. Executor 그림을 크게 바꾸는 프로세스 내 통신과 composition은 ROS 2 composition 문서를 보라.

### 읽고 나면 · After reading

- executor가 무엇을 하는지, 스레드 하나가 왜 한 번에 콜백 하나를 뜻하는지, 늦은 타이머가 왜 발화를 메우지 않고 잃는지 말할 수 있다.
- 노드의 콜백 그룹과 executor를 보고 어떤 콜백끼리 겹칠 수 있는지 예측하고, 막힌 제어 타이머에 필요한 두 변경을 댈 수 있다.
- 동기 호출 교착을 다섯 단계로 따라가고, 두 가지 방법으로 고칠 수 있다.
- 막히는 콜백이 P6에서 앗아 가는 발화 수와 귀먹은 시간을 계산할 수 있다.
- 스탬프에 ROS 시간과 벽시계 중 무엇을, 주기에 `create_timer`와 `create_wall_timer` 중 무엇을 쓸지 고르고, 실시간 계수 아래에서 둘을 예측할 수 있다.

### 스스로 점검

1. 노드를 `MultiThreadedExecutor`에 올렸는데도 타이머 안의 동기 서비스 호출이 여전히
   교착한다. 왜인가?
2. 어떤 노드가 `time.time()`으로 메시지에 스탬프를 찍는다. 실험실에서는 잘 되는데 bag
   재생에서는 숫자가 틀린다. 정확히 무엇이 잘못됐고, 무엇을 불러야 하나?
3. P6의 보정 콜백은 1초에 한 번 $200\,\mathrm{ms}$ 동안 막힌다. 여기에 자기 콜백 그룹을
   주고 `main`에는 `rclpy.spin(node)`를 그대로 둔다. 매초 제어 발화를 몇 번 잃고, 왜인가?
4. `use_sim_time:=true`로 띄운 노드가 아무것도 발행하지 않고 아무 로그도 남기지 않으며,
   `ros2 topic info /clock`은 `Publisher count: 0`을 보여 준다. 무슨 일인가?
5. $200\,\mathrm{ms}$ 정체 뒤에 P6의 $5\,\mathrm{ms}$ 제어 타이머는 왜 마흔 번을 몰아서가
   아니라 한 번 울리는가 — 그리고 왜 그쪽이 더 나은 동작인가?

> [!tip]- 정답 · Answers
> 1. 콜백 그룹을 지정하지 않았기 때문이다. 그룹 없이 만든 것은 전부 노드 기본 그룹에 들어가고 그것은 mutually exclusive이므로, 노드는 단일 스레드처럼 동작한다. 타이머 콜백이 기다리는 동안 그룹을 붙들고 있고, 결과가 나오려면 실행되어야 하는 future의 숨은 done-callback은 같은 mutually exclusive 그룹에서 스케줄될 수 없다. 클라이언트와 타이머를 다른 그룹에 두거나, 공유된 reentrant 그룹 하나에 두어라.
> 2. `time.time()`은 벽시계이고 `/clock`을 완전히 무시한다. 그래서 재생에서는 2년 전에 기록된 데이터에 오늘 시각을 찍고, 시뮬레이션에서는 시스템 나머지에 대해 실시간 계수만큼 어긋난다. 그러면 하류의 TF 조회와 다른 메시지 스탬프와의 비교가 실패하거나 조용히 외삽한다. 노드 시계의 `self.get_clock().now()`를 부르고 그래프 전체에 `use_sim_time`을 설정해야 하며, 주기가 시뮬레이션 시간을 따라야 한다면 wall timer가 아니라 `create_timer`를 쓴다.
> 3. 여전히 마흔 번이다. 콜백 그룹은 병렬을 허용할 뿐이고, `rclpy.spin`이 만드는 단일 스레드 executor에는 스레드가 하나뿐인데 보정 콜백이 그것을 붙들고 있다. 두 변경이 모두 필요하다 — 자기 그룹, *그리고* 스레드가 둘 이상인 `MultiThreadedExecutor`. 그러면 손실은 0이다.
> 4. 노드는 시뮬레이션 시간 위에 있는데 아무도 `/clock`을 발행하지 않으므로, ROS 시간이 0을 읽고 나아가지 않는다. 노드 시계로 만든 타이머는 전부 흐르지 않는 주기를 영원히 기다린다. 시뮬레이터나 `ros2 bag play --clock`을 띄우거나 `use_sim_time`을 false로 되돌려라. 노드 입장에서는 잘못된 것이 없으므로 오류도 나지 않는다.
> 5. 늦게 도는 타이머는 다음 발화를 자기 주기의 다음 정수배로 옮기므로(`rcl_timer_call`) 놓친 마흔 주기는 쌓이지 않고 건너뛰어진다. 같은 상태로 연달아 계산한 명령 마흔 개는 새 정보를 하나도 담지 않는다. 가장 새 상태로 낸 명령 하나가 제어기가 원하는 것이다 — 단, 마흔 번이 사라졌다는 사실을 알고 있을 때의 얘기이고, 어떤 로그도 그것을 말해 주지 않는다.

### 과제 · Problem set

Tier B. 장치는 [[02-foundations/lab-plants|0.6]]의 **P6**, 그리고 이 페이지의 제어기 노드(제어 타이머 $5\,\mathrm{ms}$마다, `/goal` $20\,\mathrm{ms}$마다, 보정 타이머 1초에 한 번). 손잡이 하나만 바뀐다. 보정 콜백이 이제 $D=130\,\mathrm{ms}$ 동안 막힌다. 예산 $70\,\mathrm{ms}$. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** $D=130\,\mathrm{ms}$에 대해 그림의 두 레인을 그린다. 모든 콜백이 기본 그룹에 있는 단일 스레드 executor, 그리고 보정 타이머가 자기 mutually exclusive 그룹에 있는 스레드 둘의 `MultiThreadedExecutor`. $(0,130]\,\mathrm{ms}$에 도래하는 제어 발화와 목표 도착을 모두 표시하고, 제때 돌면 채우고 못 돌면 비운다.
2. **유도.** (a) 단일 스레드 executor에서 보정 콜백 동안 도래하는 제어 발화는 몇 번이고, 제때 도는 것은 몇 번이며, 목표는 몇 개 도착하는가? (b) 매초 몇 퍼센트 동안 제어기의 귀가 먹고, 초당 발화 $200$번 중 몇 번을 잃는가? (c) 그룹 없는 `MultiThreadedExecutor`, `rclpy.spin` 위에서 보정에 자기 그룹, 둘 다 — 각각 매초 잃는 발화 수는? (d) 같은 제어기가 실시간 계수 $r=0.5$의 시뮬레이터에서 돌고, 제어 타이머를 rclcpp의 `create_wall_timer(5ms, …)`로 만들었다. 목표 하나당 제어 발화는 몇 번이고, 시뮬레이션 시간으로 몇 Hz인가? 노드 시계 위의 `create_timer`라면?
3. **해석.** P6 제어기가 `MultiThreadedExecutor` 위에서 돌고 보정 타이머에는 `MutuallyExclusiveCallbackGroup`을 줬는데, 보정이 도는 시간만큼 정확히 제어 발화를 여전히 잃는다. `ros2 node list`에는 노드가 있고 아무 로그도 없다. 이 페이지가 예측하는 원인 둘과, 각각을 확인하려고 읽을 코드 줄을 대라.

> [!note]- 그리는 법 · How to draw it
> - 두 executor가 공유하는 밀리초 단위 수평 시간축 하나, 스레드마다 레인 하나.
> - 콜백은 그것을 돌리는 스레드 위에, 시작부터 반환까지 막대로 그린다.
> - 제어 타이머의 발화는 $5\,\mathrm{ms}$마다 레인 위나 레인에 표시한다. 그 순간 콜백이 돌면 채우고, 스레드가 바쁜 동안 도래하면 비운다.
> - 목표 도착은 $20\,\mathrm{ms}$마다 레인 아래에 표시하고, 어디서 기다리는지 적는다 — 아무 스레드도 가져가지 않으면 미들웨어다.
> - 막대마다 콜백 그룹을 적고, 레인 옆에 채운 표시와 빈 표시의 개수를 적어 두 executor를 한눈에 비교하게 한다.

> [!tip]- 정답 · Solutions
> 1. 단일 스레드: 스레드 1에 $0$부터 $130\,\mathrm{ms}$까지 막대 하나, $5,10,\ldots,130$에 빈 제어 표시 $26$개, $20,40,\ldots,120$에 미들웨어에서 기다리는 목표 도착 $6$개. 스레드 둘: 스레드 1에 같은 막대(보정 그룹), 스레드 2에 채운 제어 표시 $26$개와 목표 콜백 $6$개(기본 그룹).
> 2. (a) $130/5=26$번 도래, 제때 $0$번. 목표 $6$개($20,\ldots,120$). (b) $130/1000=13\,\%$. $200$번 중 $26$번. (c) $26$, $26$, $0$ — 기본 그룹은 mutually exclusive이고 단일 스레드 executor에는 스레드가 하나뿐이어서, 두 변경이 함께일 때만 타이머가 풀려난다. (d) 발화 하나가 시뮬레이션 시간 $rT=0.5\times5=2.5\,\mathrm{ms}$를 덮으므로 목표 하나당 $20/2.5=8$번, 시뮬레이션 시간으로 $400\,\mathrm{Hz}$. `create_timer`라면 시뮬레이션 $5\,\mathrm{ms}$, 목표당 $4$번, $200\,\mathrm{Hz}$.
> 3. (i) 제어 타이머와 보정이 결국 같은 그룹에 있다. 제어 타이머를 `callback_group=`에 보정 그룹을 넘겨 만들었거나, 보정 타이머를 그 인자 없이 만들어 제어 타이머와 함께 기본 그룹에 남겼다 — `create_timer` 호출들을 읽는다. (ii) executor의 스레드가 하나다, `MultiThreadedExecutor(num_threads=1)` — executor를 생성하는 줄을 읽는다. (rclpy에서 더 약한 셋째 원인은 보정이 기다리는 대신 순수 Python으로 계산하는 경우다. 그러면 발화는 돌되 인터프리터 락 때문에 늦는다.)

### 출처

- ROS 2 Jazzy 문서 — Concepts: Executors(executor 종류, 콜백 그룹, wait set, 스케줄링 의미).
- ROS 2 Jazzy 문서 — How-to Guides: Using Callback Groups(교착 예제, 동작하는 구성과 동작하지 않는 구성).
- ROS 2 design article — Clock and Time(SystemTime, SteadyTime, ROSTime, `/clock` 시간 소스, `use_sim_time`, 시간 점프).
- Jazzy 브랜치 소스: `rcl/src/rcl/timer.c`(`rcl_timer_call`이 놓친 주기를 건너뜀), `rclpy/executors.py`(`MultiThreadedExecutor`), `demo_nodes_py`와 `demo_nodes_cpp`의 talker(`create_timer` 대 `create_wall_timer`), `ros2bag` play verb(`--clock`).
- Python 문서 — `sys.setswitchinterval`(스레드 전환 간격, 기본 5 ms).
- Daniel Casini, Tobias Blass, Ingo Lütkebohle, Björn Brandenburg, "Response-Time Analysis of ROS 2 Processing Chains under Reservation-Based Scheduling", ECRTS 2019.
