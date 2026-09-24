---
title: "12.8 Concurrency: Processes, Threads and Races"
tags: [foundations, tools, concurrency]
study-depth: Working
wiki-support: Working
depth-goal: "On P6's node, count by enumeration the interleavings that tear a two-field goal or lose an update, remove a lock-order deadlock, size a bounded log queue against a disk stall and choose what happens when it is full, bound a speedup with Amdahl's law and a data loader by its slowest stage, and choose threads, processes or asyncio for a Python job, including a PyTorch DataLoader's workers and their seeds."
mastery-when: "Raise when the thesis ships multi-threaded robot software of its own — lock-free queues, memory ordering, response-time analysis of a control chain — rather than configuring nodes and loaders that others wrote."
---

> [!note] Prerequisites · 선수 지식
> Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] (the 50 Hz goal, the 200 Hz controller, the 70 ms budget) and Python at the level of functions, lists and dictionaries. The lab needs the standard library and NumPy only; listings that start real threads or PyTorch are marked not-run, were run on this page's machine, and their outputs are labelled as its measurements.
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**(50 Hz 목표, 200 Hz 제어기, 70 ms 예산)와 함수·리스트·딕셔너리 수준의 Python. 실습에는 표준 라이브러리와 NumPy만 있으면 된다. 실제 스레드나 PyTorch를 띄우는 코드는 not-run 표시를 달고 이 페이지를 쓴 기계에서 돌렸으며, 그 출력은 그 기계의 측정값이라고 밝혀 두었다.

## English

*Stands on [[02-foundations/lab-plants|0.6 Lab Plants]]: P6's vision callback stores a goal every 20 ms and its controller reads it every 5 ms. Run the two on two threads, add a logger and a data loader, and you have the bugs this page teaches — a lost update, a torn read, a deadlock, a full queue, and what Python's global interpreter lock hides — with their fixes. [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]] later applies them to ROS 2 callbacks.*

> [!note] Why this matters · 왜 배우는가
> This page is part of the floor beneath the physical-AI stack of [[07-research-program/index|research program §5]] — the tools every layer runs on (its place is marked on the [[physical-ai-map|Physical AI Map]]). In that section's worked instance, "Install that panel on the frame", it serves the steps that run at the same time on one robot computer: the camera callback that identifies the frame hands its goal to the control loop that moves the component and detects contact. Get the sharing wrong and nothing crashes, yet the experiment is corrupted: on P6 a torn goal pairs a new position with an old stamp, 10 mm and 20 ms apart, a lock-order deadlock freezes the node while the motor keeps its last command, and a data loader's workers silently repeat half their augmentation. [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]] applies the page to ROS 2 callback groups and [[04-robotics/ros2/cpp-for-robot-code|25.0 §9]] to a real-time C++ tick; the page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it before the ROS 2 build track reaches 25.5.1 for the rig, ahead of block 7, or the first time you parallelize a Python job. After it you can count the interleavings that break shared data, fix them with a lock, one assignment or a bounded queue with a stated policy, bound a speedup with Amdahl's law, and choose threads, processes or asyncio for a Python job.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes. **Session 1 — races, counted.** The picture, then §1–§3: by the end you can trace a lost update step by step and count the orders that cause it. Then §4, the lock that removes them; end with Self-check 1 and 2. **Session 2 — the other two fixes.** §5 and §6, then the Worked case on P6's numbers — a lock, one lock order, a queue with a policy — and Self-check 3 and 4. After that: §7–§9 (Amdahl's law, the GIL and the DataLoader) with Self-check 5 before you parallelize a Python job or tune a data loader, §10 when you write a C++ or ROS 2 node, and §11 with the problem set last. Open a collapsed *Deeper* box only when you need it.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], seen from inside its software: a vision callback that stores a new goal every $T_v=20\,\mathrm{ms}$, a control tick that reads the newest goal every $T_c=5\,\mathrm{ms}$, the budget $B=70\,\mathrm{ms}$ and the encoder's 2,048 counts per metre. The rest is this page's own, frozen here as course numbers, not measurements.

| Object | Course numbers |
|---|---|
| the goal | two fields, position $p$ (m) and camera stamp $s$ (ms): the previous goal $(0.500\,\mathrm{m},\,1000\,\mathrm{ms})$, the new one $(0.510\,\mathrm{m},\,1020\,\mathrm{ms})$, since the target moves at $v=0.5\,\mathrm{m/s}$ |
| the callback counter `n_cb` | every callback adds 1 for a health check, 250 per second; it holds 100 before the picture's two callbacks |
| two locks | `goal_lock` guards the goal, `log_lock` the log buffer |
| the logger | a 64-byte record per control tick, $\lambda=200$ records/s, into a queue of $N=32$ slots; a writer thread takes $\mu=1$ record per ms while the disk responds; one disk stall of $D=300\,\mathrm{ms}$ |
| the data loader | $W$ worker processes, $t_{\text{load}}=40\,\mathrm{ms}$ per batch per worker, $t_{\text{GPU}}=10\,\mathrm{ms}$ per training step, $t_{\text{main}}=1\,\mathrm{ms}$ per batch in the main process |
| the preprocessing job | one hour of logs into training windows: $T_1=120\,\mathrm{s}$ on one core, a fraction $P=0.9$ of it divisible across cores |

The node runs `on_goal` and the control timer on two threads, in different callback groups of a multi-threaded executor — in ROS 2 the executor is the loop that runs a node's callbacks, and a callback group says which of them may overlap. It is the arrangement [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]] uses so that a slow callback cannot stall the timer. From then on the two can run at the same time, and what they share is this page's subject.

*Scope: this page teaches the concurrency bugs a robot-learning researcher meets — lost updates, torn reads, lock-order deadlocks, full queues and the effect of Python's global interpreter lock — with their fixes, and the minimum about threads, processes, scheduling, Amdahl's law, `threading`, `multiprocessing`, `asyncio` and a PyTorch DataLoader's workers needed to apply them. It does not teach operating-system internals, memory ordering, lock-free programming, real-time scheduling analysis, GPU streams or distributed training; C++ threads point to [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]] and ROS 2 callback groups to [[04-robotics/ros2/executors-callbacks-time|25.5.1]]; §12 says where the rest lives.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 540" style="max-width:100%;height:auto" role="img" aria-label="Three panels on plant P6. (a) One vision callback and one control tick interleaved in the order A B B A A B A B over eight steps: the control tick reads the new position 0.510 m with the old stamp 1000 ms, and the callback counter goes from 100 to 101 instead of 102. (b) The control tick holds goal_lock and waits for log_lock while the log writer holds log_lock and waits for goal_lock, a cycle. (c) The log queue during a 300 ms disk stall: records arrive at 200 per second, the 32-slot queue is full at 160 ms; dropping loses 28 records, blocking stops the control thread from 165 to 301 ms, and an unbounded queue peaks at 60 records and is empty again at 374 ms.">
  <defs><marker id="ccArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) One on_goal and one control tick, interleaved: 8 atomic steps, two bugs</text>
  <text x="12" y="55" font-size="11" fill="currentColor">on_goal</text>
  <text x="12" y="67" font-size="10" fill-opacity="0.7" fill="currentColor">vision thread</text>
  <text x="12" y="93" font-size="11" fill="currentColor">control tick</text>
  <text x="12" y="105" font-size="10" fill-opacity="0.7" fill="currentColor">control thread</text>
  <line x1="92" y1="56" x2="540" y2="56" stroke="currentColor" stroke-width="1" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <line x1="92" y1="94" x2="540" y2="94" stroke="currentColor" stroke-width="1" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <text x="120" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">1</text>
  <rect x="94" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="120" y="60" font-size="10" text-anchor="middle" fill="currentColor">p ← 0.510</text>
  <text x="176" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">2</text>
  <rect x="150" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="176" y="98" font-size="10" text-anchor="middle" fill="currentColor">read p</text>
  <text x="232" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">3</text>
  <rect x="206" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="232" y="98" font-size="10" text-anchor="middle" fill="currentColor">read s</text>
  <text x="288" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">4</text>
  <rect x="262" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="288" y="60" font-size="10" text-anchor="middle" fill="currentColor">s ← 1020</text>
  <text x="344" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">5</text>
  <rect x="318" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="344" y="60" font-size="10" text-anchor="middle" fill="currentColor">r ← n</text>
  <text x="400" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">6</text>
  <rect x="374" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="400" y="98" font-size="10" text-anchor="middle" fill="currentColor">r ← n</text>
  <text x="456" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">7</text>
  <rect x="430" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="456" y="60" font-size="10" text-anchor="middle" fill="currentColor">n ← r+1</text>
  <text x="512" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">8</text>
  <rect x="486" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="512" y="98" font-size="10" text-anchor="middle" fill="currentColor">n ← r+1</text>
  <text x="12" y="126" font-size="10" fill-opacity="0.8" fill="currentColor">shared memory</text>
  <text x="12" y="138" font-size="10" fill-opacity="0.8" fill="currentColor">after each step</text>
  <text x="88" y="126" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">p</text>
  <text x="88" y="140" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">s</text>
  <text x="88" y="154" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">n</text>
  <text x="120" y="126" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">0.510</text>
  <text x="120" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="120" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="176" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="176" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="176" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="232" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="232" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="232" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="288" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="288" y="140" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">1020</text>
  <text x="288" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="344" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="344" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="344" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="400" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="400" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="400" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="456" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="456" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="456" y="154" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">101</text>
  <text x="512" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="512" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="512" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">101</text>
  <path d="M150 162v5H258v-5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="204" y="180" font-size="11" text-anchor="middle" fill="currentColor">control gets (0.510 m, 1000 ms):</text>
  <text x="204" y="194" font-size="11" text-anchor="middle" fill="currentColor">a goal nobody published</text>
  <path d="M318 162v5H538v-5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="428" y="180" font-size="11" text-anchor="middle" fill="currentColor">n: 100 → 101, not 102</text>
  <text x="428" y="194" font-size="11" text-anchor="middle" fill="currentColor">one update lost</text>
  <text x="12" y="222" font-size="12" fill="currentColor">(b) The control tick and the log writer take two locks in opposite orders</text>
  <rect x="30" y="262" width="140" height="26" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="100" y="279" font-size="11" text-anchor="middle" fill="currentColor">control tick</text>
  <rect x="390" y="262" width="140" height="26" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="460" y="279" font-size="11" text-anchor="middle" fill="currentColor">log writer</text>
  <rect x="215" y="236" width="130" height="24" rx="10" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="252" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">goal_lock</text>
  <rect x="215" y="292" width="130" height="24" rx="10" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="308" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">log_lock</text>
  <line x1="215" y1="248" x2="172" y2="266" stroke="currentColor" stroke-width="1.4" marker-end="url(#ccArrow)"/>
  <text x="178" y="246" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">held by</text>
  <line x1="172" y1="284" x2="213" y2="302" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ccArrow)"/>
  <text x="150" y="312" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">waits for</text>
  <line x1="345" y1="304" x2="388" y2="284" stroke="currentColor" stroke-width="1.4" marker-end="url(#ccArrow)"/>
  <text x="382" y="314" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">held by</text>
  <line x1="388" y1="266" x2="347" y2="248" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ccArrow)"/>
  <text x="380" y="240" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">waits for</text>
  <text x="280" y="336" font-size="11" text-anchor="middle" fill="currentColor">2 of the 6 schedules end in this cycle; with goal_lock first in both threads, 0 of 2</text>
  <text x="12" y="364" font-size="12" fill="currentColor">(c) The log queue in a 300 ms disk stall: 200 records/s in, N = 32 slots, 1 record/ms out</text>
  <rect x="70" y="394" width="345" height="100" fill="currentColor" fill-opacity="0.06"/>
  <text x="74.6" y="405" font-size="10" fill-opacity="0.7" fill="currentColor">disk stalled, 0–300 ms</text>
  <line x1="70" y1="494" x2="530" y2="494" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70" y1="494" x2="70" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70" y1="494" x2="70" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="70" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <line x1="185" y1="494" x2="185" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="185" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">100</text>
  <line x1="300" y1="494" x2="300" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="300" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">200</text>
  <line x1="415" y1="494" x2="415" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="415" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">300</text>
  <line x1="530" y1="494" x2="530" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="530" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">400</text>
  <text x="65" y="497.5" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="65" y="444.2" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">32</text>
  <text x="65" y="397.5" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="65" y="384" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">records</text>
  <line x1="70" y1="440.7" x2="530" y2="440.7" stroke="currentColor" stroke-width="1" stroke-dasharray="5 3" stroke-opacity="0.7"/>
  <text x="530" y="436.7" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">N = 32</text>
  <polyline points="70,494 254,440.7 415,440.7 459.9,494 530,494" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="70,494 415,394 500.1,494 530,494" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 3"/>
  <text x="336.8" y="453.7" font-size="10" text-anchor="middle" fill="currentColor">drop newest: 28 records lost</text>
  <text x="438" y="400.7" font-size="10" fill="currentColor">grow: 60 at 300 ms,</text>
  <text x="438" y="412.7" font-size="10" fill="currentColor">empty at 374 ms</text>
  <text x="435.7" y="480.7" font-size="10" text-anchor="end" fill="currentColor">empty at 339 ms</text>
  <rect x="259.8" y="516" width="156.4" height="6" fill="currentColor" fill-opacity="0.55"/>
  <text x="255.2" y="522" font-size="10" text-anchor="end" fill="currentColor">block: control stuck 165–301 ms</text>
  <text x="420.8" y="522" font-size="10" fill="currentColor">27 ticks never run</text>
  <text x="300" y="535" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">time since the stall began (ms)</text>
</svg>

(a) One `on_goal` and one control tick interleaved as ABBAABAB: the tick reads the new position with the old stamp, $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$, and the counter ends at 101, not 102 — of the 70 possible orders, 20 tear the goal and 40 lose an update. (b) The tick holds `goal_lock` and waits for `log_lock` while the log writer holds `log_lock` and waits for `goal_lock`: 2 of the 6 schedules end in this cycle, none once both take `goal_lock` first. (c) In a 300 ms disk stall the 32-slot log queue is full at 160 ms: dropping loses 28 records, blocking stops the control thread from 165 to 301 ms, and an unbounded queue peaks at 60 records and is empty at 374 ms.

### 1. Processes and threads: what is shared

*In one sentence:* threads of one process share its memory and processes do not — which makes threads cheap and races possible, and processes safe but costly.

**The problem.** P6's node needs two activities that both touch one goal: `on_goal` writes it, the control tick reads it. P6's training job needs the opposite: several workers decoding batches at once, touching nothing in common. Operating systems offer two units of execution, and the choice between them is a choice about sharing.

**The idea.** Think of a **process** as a workshop with its own tools and its own benches — its own address space. A **thread** is a worker inside a workshop: every worker in it uses the same tools, and each keeps only a notebook of their own, the stack (pthreads(7)). Two workshops share nothing unless they send parcels to each other: after `fork()` a child process starts as a copy of its parent, but from then on neither sees the other's writes (fork(2)). How a process is started, signalled and stopped from the shell is [[02-foundations/tools/linux-shell|12.1 Linux and the Shell §3]].

> **Thread, defined.** A **thread** is *one sequence of instructions that the operating system schedules on its own, inside a process* — a path of execution, not a program and not a core. Three conditions: it **belongs to one process and shares its memory**, so what one thread writes at an address the others read there; it **has its own stack and registers**, so its local variables and its place in the code are private; and it is **scheduled independently**, so two threads may run on two cores at once or take turns on one.
>
> $$c=\begin{cases}1 & n\ \text{threads of one process}\\ 1+n & \text{a main process and}\ n\ \text{worker processes}\end{cases}$$
>
> where $c$ is the number of copies of the data that $n$ workers read, so memory grows with the worker count only when the workers are processes.
>
> - **Example**: P6's node holds one goal that both callback threads see — which is exactly why §3 can tear it. Its data loader with $W=4$ worker processes and a 3 GB dataset of Python objects (a course number) can reach $c=5$ copies, 15 GB (§9).
> - **Non-example**: a forked child. It starts with the same goal, but when `on_goal` in the parent writes a new one, the child keeps reading the old one, and nothing reports it.
> - **Why it matters**: sharing makes threads fast to start and to talk to, and it is exactly what every race needs — two threads, one address, one write.

**A number.** Starting is where the two differ most. On this page's machine (macOS on Apple silicon, Python 3.12.4; medians of three runs — a measurement of this machine, not a course number):

| | threads of one process | separate processes |
|---|---|---|
| memory | shared: one thread's write is every other thread's read | separate; data travels as copies — Python's `multiprocessing` pickles it, that is, serializes it to bytes |
| a crash | takes the whole process down | stays in its process |
| start and join, empty | 31–39 µs | 46–48 ms, with `spawn` |

A `spawn`ed process starts a fresh interpreter that imports the program again, which is why it costs more than a thousand threads.

**The trap.** Choosing threads for convenience and then sharing more than you meant to. Choose by sharing: P6's goal must be one copy written by one callback and read by another, so the callbacks are threads, and §3–§5 are the price; the loader's workers share no writes, so they can be processes, whose price is copies and start-up (§9).

### 2. Scheduling: why a thread can stop between any two steps

*In one sentence:* a thread can be suspended at a point it did not choose, or run at the same moment as another on a second core, so no two steps of a thread are guaranteed to run together.

**The problem.** You write two lines — store the goal's position, store its stamp — and picture them running back to back. Can another thread come in between?

**The idea.** Yes. The scheduler decides which ready thread runs (sched(7)), and a thread leaves the CPU in one of two ways. It **blocks**: it waits for I/O, a lock or a sleep and gives the CPU up itself. Or it is **preempted**: suspended wherever it happens to be, because its time slice ended or a higher-priority thread woke up, and resumed later with no sign that anything happened. On a machine with several cores there is a third way two threads overlap: they simply run at the same moment.

**The rule, for Python.** Python first compiles each line into **bytecode**, the small instructions its interpreter actually executes. In standard CPython, which has a global interpreter lock (§8), the unit that cannot be split is therefore not a line but one bytecode instruction: the interpreter switches threads only between instructions, and each instruction is atomic from the program's point of view (Python FAQ, "What kinds of global value mutation are thread-safe?").

**A number.** P6's counter update is one line and four instructions. On this page's machine:

```bash
python3 -c "import dis; dis.dis('n_cb += 1')"
```

```text
  1           2 LOAD_NAME                0 (n_cb)
              4 LOAD_CONST               0 (1)
              6 BINARY_OP               13 (+=)
             10 STORE_NAME               0 (n_cb)
```

That is Python 3.12.4's output, trimmed to the line's four instructions; other versions number and name them differently. Read it as a recipe: fetch the counter, fetch 1, add, store. A switch is allowed after any of the first three, so another thread can read the old counter before this one stores the new — the whole of §3's lost update.

**The trap.** "One line is one step." The FAQ says it directly: `i = i+1` is not atomic, while single operations on built-in types — `L.append(x)`, `x = y`, `x.field = y` — are. Which lines are safe is a fact about the interpreter, not something you can see in the source.

> [!note]- Deeper · 더 깊이
> **Priorities.** Linux runs ordinary threads under the time-sharing policy `SCHED_OTHER` and offers two real-time policies with static priorities 1 (low) to 99 (high) that run ahead of every ordinary thread: `SCHED_FIFO`, without time slicing, and `SCHED_RR`, with a maximum quantum per turn. By default 5% of CPU time is kept for non-real-time processes (`sched_rt_runtime_us` is 950,000 of each 1,000,000 µs), and since Linux 6.12 the kernel's real-time preemption (PREEMPT_RT) can be enabled without patches (sched(7)). A 200 Hz control thread is the natural candidate for a real-time priority, and then a lock it shares with a low-priority thread invites priority inversion, defined with its cure in [[02-foundations/algorithms/interview-code|11.7 §6]]. The C++ side of those rules is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code §9]]; which ROS 2 callbacks share a thread is [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]].

### 3. Races: lost updates and torn reads, counted

*In one sentence:* when two threads touch the same data and one writes, the result depends on how their steps interleave, and for small cases the interleavings can be listed and counted.

**The problem.** P6's health check expects 250 callbacks a second, and now and then it counts fewer. Nothing crashed, nothing was logged.

**The idea, traced.** Both callbacks run `n_cb += 1`: a load, then a store of the loaded value plus one. Here is one way their four steps can fall:

| step | thread | does | `n_cb` in memory | registers |
|---:|---|---|---:|---|
| 1 | A (`on_goal`) | load | 100 | A holds 100 |
| 2 | B (tick) | load | 100 | A 100, B 100 |
| 3 | A | store A + 1 | 101 | |
| 4 | B | store B + 1 | 101 | |

Each thread did its job correctly, yet memory shows one increment: B's store wrote over A's, because B had loaded before A stored. That is a **lost update**. The same thing happens to the goal. `on_goal` stores $p$ then $s$, and the tick loads $p$ then $s$; if the tick's two loads fall between the two stores, it gets the new position with the old stamp — a **torn read**, a pair nobody wrote. All six orders of those four steps (lab, part 1b):

| order (A = `on_goal`, B = tick) | the tick reads | |
|---|---|---|
| AABB | (0.510 m, 1020 ms) | new, consistent |
| ABAB | (0.510 m, 1020 ms) | new, consistent |
| ABBA | (0.510 m, 1000 ms) | **torn**: new position, old stamp |
| BAAB | (0.500 m, 1020 ms) | **torn**: old position, new stamp |
| BABA | (0.500 m, 1000 ms) | old, consistent |
| BBAA | (0.500 m, 1000 ms) | old, consistent |

Reading the old goal is harmless — its stamp truthfully says it is 20 ms older. A mixture is not: its stamp misstates the age of the position it travels with (the Worked case prices it).

**The rule.** Two definitions turn "it depends on timing" into something you can count.

> **Interleaving, defined.** An **interleaving** is *one total order of all the atomic steps of several threads that keeps each thread's own order* — a possible history of the program, not a probability. Three conditions: the steps are **atomic** (a load, a store, a bytecode instruction, or a whole critical section under a lock, §4); **each thread's order is kept**; and **every step appears exactly once**.
>
> $$I(m_A,m_B)=\binom{m_A+m_B}{m_A}$$
>
> where $m_A$ and $m_B$ are the threads' step counts, since an interleaving is fixed by choosing which of the $m_A+m_B$ positions thread A's steps take — thread B's fill the rest in order.
>
> - **Example**: two stores against two loads, $I(2,2)=\binom{4}{2}=6$: the six rows above, two of them torn. With the counter's steps added, four each, $I(4,4)=70$.
> - **Non-example**: six equally likely outcomes. The count says what is *possible*: on this machine the goal written as two plain stores was never read torn in 2.3 million reads (§8), though the enumeration shows it can be.
> - **Why it matters**: a concurrent program is correct only if every interleaving gives an acceptable result, and listing them proves or refutes that for small cases.

> **Race condition, defined.** A **race condition** is *a property of a program whose result depends on the relative timing or order of its threads' steps* (Python glossary) — a defect of the code, whether or not a given run shows it. Four conditions: **shared data**, **at least one write**, **no enforced order** between the conflicting accesses (no lock, message or join), and **different outcomes** across the resulting interleavings. A **data race** — unsynchronized conflicting accesses to one memory location — is undefined behaviour in C++ ([intro.races]).
>
> $$\text{race}\iff\exists\,\sigma_1,\sigma_2\in\Sigma:\ \text{out}(\sigma_1)\neq\text{out}(\sigma_2)$$
>
> where $\Sigma$ is the set of possible interleavings and $\text{out}(\sigma)$ the observable result of $\sigma$, so two interleavings with different results prove a race.
>
> - **Example**: the counter: of the six orders of one increment each, four end at 101 and two at 102, so the program has a race whether or not today's run lost anything.
> - **Non-example**: the same callbacks in one mutually exclusive callback group, ROS 2's default ([[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]). They never overlap, so only the two whole-callback orders remain, and both end at 102.
> - **Why it matters**: bad interleavings can be rare in practice and still possible, so a race survives testing; only an enforced order removes it (§4–§6).

**Numbers: more increments, fewer right answers** (lab, part 1a):

| $k$ increments per thread | interleavings $\binom{4k}{2k}$ | possible final values | right ($2k$) | share right |
|---:|---:|---|---:|---:|
| 1 | 6 | 1–2 | 2 | 33.33% |
| 2 | 70 | 2–4 | 6 | 8.57% |
| 3 | 924 | 2–6 | 20 | 2.16% |
| 4 | 12,870 | 2–8 | 70 | 0.54% |
| 5 | 184,756 | 2–10 | 252 | 0.14% |

The right answer comes out in exactly the $\binom{2k}{k}$ orders in which no increment is split — the lab checks it. And the worst case does not grow with the work: the smallest result is 2 however large $k$ is. The recipe: A loads 0; B completes $k-1$ increments; A stores 1 over all of them; B loads that 1; A completes its other $k-1$; B's last store writes 2 over everything (`ABBBBBBBBABAAAAAAAAB` for $k=5$).

**The trap: a count is not a probability.** A thread usually runs thousands of steps before it is switched out, so the orders a real run produces are mostly unsplit ones, and the race survives testing: on this machine the bare `n_cb += 1` loop lost no update in 5 × 2,000,000, while one function call between the load and the store lost 27–33% (§8). A result that depends on the interleaving also makes a run non-repeatable in the sense of [[06-research-practice/experimental-design-reproducibility|research practice 2 §6]].

### 4. Locks and critical sections

*In one sentence:* a lock makes a critical section run as one step for every thread that takes the same lock, which removes the race at the price of waiting.

**The problem.** §3's bugs both come from a two-step update that another thread can split. We want `on_goal`'s two stores, and the tick's two loads, each to happen as one.

**The idea.** A lock is a token: only the thread holding it may enter the guarded code, and anyone else who wants in waits at the door. `threading.Lock` is locked or unlocked; `acquire()` blocks until it is unlocked and then locks it, `release()` unlocks it and lets one waiting thread in, and `with lock:` does both, even if the block raises (the `threading` documentation). Around P6's goal, on one thread so the output is deterministic:

```python
import threading

goal_lock = threading.Lock()
goal = {"p": 0.500, "s": 1000}                 # P6's goal: position (m) and camera stamp (ms)

def on_goal(p, s):                             # the vision callback
    with goal_lock:                            # both fields change inside one critical section
        goal["p"], goal["s"] = p, s

def read_goal():                               # the control tick
    with goal_lock:
        return goal["p"], goal["s"]

on_goal(0.510, 1020)
print("control reads", read_goal())
print("free lock, acquire:", goal_lock.acquire(timeout=0.01))          # taken at once
print("same thread again: ", goal_lock.acquire(timeout=0.01))          # a Lock is not reentrant: gives up after 10 ms
goal_lock.release()
r = threading.RLock()
print("RLock, twice:      ", r.acquire(timeout=0.01), r.acquire(timeout=0.01))   # the owner may re-acquire
r.release(); r.release()
```

```text
control reads (0.51, 1020)
free lock, acquire: True
same thread again:  False
RLock, twice:       True True
```

The last lines show a property that bites: a `Lock` is not reentrant, so a thread that acquires it twice waits for itself — forever, without the timeout. A `threading.RLock` may be re-acquired by its holder.

> **Lock, defined.** A **lock** (mutex) is *a synchronization object that at most one thread holds at a time* — an agreement among the threads that use it, not a property of the data. Three conditions: **acquire** blocks until the lock is free, then takes it; **release** frees it for one waiting thread; and **every access to the guarded data holds that same lock** — the code in between is the **critical section**, and one access without the lock voids the guarantee.
>
> $$\sum_i h_i(t)\le1,\qquad w_A\le c_B$$
>
> where $h_i(t)$ is 1 while thread $i$ holds the lock, $w_A$ is how long thread A waits to acquire it and $c_B$ the longest critical section of the other thread B, so critical sections never overlap and, with two threads, an acquisition waits at most one of the other's critical sections.
>
> - **Example**: `on_goal` and the tick each take `goal_lock` around both field accesses. Each critical section is now one step, so the six orders of §3 collapse to $I(1,1)=2$ — the tick reads $(0.500\,\mathrm{m},\,1000\,\mathrm{ms})$ or $(0.510\,\mathrm{m},\,1020\,\mathrm{ms})$, never a mixture. With the increment under the lock, $k=5$ gives $\binom{10}{5}=252$ orders, all ending at 10.
> - **Non-example**: a lock that only `on_goal` takes. The tick still loads without it, and all six orders — the torn ones too — remain.
> - **Why it matters**: it is the simplest fix for a race, and its whole cost is the waiting that the other critical sections impose.

**A number: what a lock costs.** Taking a free lock is cheap. On this machine:

```bash
python3 -m timeit -s "import threading; lock = threading.Lock()" "with lock: pass"
```

```text
1000000 loops, best of 5: 291 nsec per loop
```

Two runs gave 256 and 291 ns, about 0.006% of P6's 5 ms period (a measurement of this machine). What costs is waiting, and $w_A\le c_B$ says the waiting is as long as the other side's critical section. So a log writer that held `log_lock` while writing to disk would hold it through the 300 ms stall, and the tick taking the same lock would wait 300 ms — $300/5=60$ ticks, $300/70=4.3$ budgets. Hold the lock only to swap the full buffer for an empty one, and write outside it.

**The traps: what a lock does not fix.**
- *An access that skips it* — the non-example above.
- *A check and an action in two critical sections.* `if not q.full(): q.put(x)` can still block, because another thread can fill the queue in between; the `queue` documentation warns that `qsize() < maxsize` does not guarantee a non-blocking `put()`. Use the non-blocking call and handle its failure (§6).
- *Deadlock and priority inversion*, which locks create: §5 and [[02-foundations/algorithms/interview-code|11.7 §6]].

**Without a lock: one assignment.** Some updates come as one indivisible operation. C++'s `std::atomic<T>::fetch_add` adds and returns the old value in one step (cppreference). Python has no atomic integer, but the FAQ's single operations are atomic under the GIL — CPython's interpreter lock, §8 — and that gives a lock-free fix for the torn read: `on_goal` builds the goal as one immutable tuple and publishes it with one assignment, `self.goal = (p, s)`, so a reader gets the old tuple or the new one, never half of each — the hand-over-in-one-assignment that [[04-robotics/ros2/executors-callbacks-time|25.5.1]] recommends.

### 5. Deadlock and lock ordering

*In one sentence:* two threads that take two locks in opposite orders can each end up holding one and waiting for the other forever, and one global lock order makes that impossible.

**The problem.** With the goal and the log each under a lock, the node sometimes freezes: no command, no log line, the process still listed.

**The idea, traced.** The tick takes `goal_lock` to read the goal and then, still holding it, `log_lock` to log what it read. The log writer takes `log_lock` to swap its buffer and then, still holding it, `goal_lock` to put the current goal in a status line. One unlucky order:

1. The tick acquires `goal_lock` — it was free.
2. The writer acquires `log_lock` — it was free.
3. The tick asks for `log_lock`: held by the writer, so the tick waits.
4. The writer asks for `goal_lock`: held by the tick, so the writer waits.

Each would release its lock only after getting the other, so neither ever will (panel b). The lab searches every schedule, allowing an acquire only while its lock is free:

| the log writer takes its locks | schedules | finish | deadlock |
|---|---:|---:|---:|
| in the opposite order to the tick | 6 | 4 | 2 |
| in the same order as the tick | 2 | 2 | 0 |
| one at a time, never both | 7 | 7 | 0 |

> **Deadlock, defined.** A **deadlock** is *a state in which each thread of a set waits for something only another thread of the set can provide, so none proceeds* (Python glossary) — a state some interleavings reach and others do not, not a slowdown. Four conditions, each necessary, so removing any one prevents it: **mutual exclusion** (one holder per lock), **hold and wait** (a thread holds one lock while waiting for another), **no preemption** (a lock cannot be taken away) and **circular wait** (the waits form a cycle).
>
> $$T_1\to L_a\to T_2\to L_b\to T_1,\qquad r(L_a)<r(L_b)<r(L_a)\ \text{is impossible}$$
>
> where a thread-to-lock arrow means *waits for*, a lock-to-thread arrow means *held by*, and $r$ ranks the locks; if every thread acquires only in increasing rank, a cycle would need each rank to exceed the one before it all the way round, so no cycle, and so no deadlock, can form.
>
> - **Example**: tick → `log_lock` → writer → `goal_lock` → tick, reached in 2 of 6 schedules; with `goal_lock` ranked first and taken first by both threads, 0 of 2.
> - **Non-example**: the tick waiting 300 ms for `log_lock` while the writer holding it is stuck in a disk stall — blocking, not deadlock, since the writer will finish and release.
> - **Why it matters**: a deadlocked node stays in the process list and logs nothing — its logger is one of the stopped threads — and P6's motor keeps its last command, since a dead node can leave a live command ([[04-robotics/robot-systems-deployment|10. Robot Systems §7]]).

**The fixes, one per condition.** Rank the locks and acquire them only upward — the Python glossary's own advice is to acquire multiple locks in a consistent order. Or never hold two at once: the writer copies the goal under `goal_lock`, releases it, then takes `log_lock` (the table's third row). In C++, `std::scoped_lock` takes several mutexes with a deadlock-avoidance algorithm (§10).

**The traps.** A timeout, `lock.acquire(timeout=0.01)`, detects rather than cures: it turns a silent hang into an error you can log, which is worth having on a robot, but the code must still back off and retry. And the same shape hides where there is only one lock: the ROS 2 deadlock of a synchronous service call inside a callback is a callback holding its mutually exclusive group while it waits for a result only that group can deliver ([[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]).

### 6. Queues between threads: producers, consumers and bounded buffers

*In one sentence:* instead of sharing data under a lock, a producer can hand items to a consumer through a queue that does its own locking — and when the producer outpaces the consumer, the capacity and the full-queue policy decide what breaks.

**The problem.** The control tick should log every command, but writing to disk inside a 5 ms tick makes the controller wait for the disk.

**The idea.** Hand the record over instead. In the **producer–consumer** pattern each item has one owner at a time: the tick puts a record into a queue and forgets it, and a writer thread takes records out and writes them. The queue is a mailbox with a fixed number of slots, and `queue.Queue` does the locking for any number of producers and consumers (the `queue` documentation). The only question left is what happens when the mailbox is full.

> **Bounded buffer, defined.** A **bounded buffer** is *a first-in, first-out queue with a fixed capacity between producer and consumer threads* — a data structure plus a policy. Four conditions: items leave **in arrival order**; at most **$N$ items** are held; a **full-buffer policy** — block the producer, drop the newest or drop the oldest — is part of it ("grow", with no bound, makes it an unbounded queue instead); and it **does its own locking**.
>
> $$t_{\text{full}}=\frac{N-q_0}{\lambda-\mu},\qquad n_{\text{over}}=(\lambda-\mu)\,(D-t_{\text{full}})$$
>
> where $q_0$ items are queued at the start, items arrive at $\lambda$ and leave at $\mu<\lambda$ for an episode of length $D$, $t_{\text{full}}$ is when the buffer fills and $n_{\text{over}}$ the items that arrive to a full buffer, since the buffer gains $\lambda-\mu$ items per second until it is full and, after that, every one of those surplus items finds no slot and is dropped or blocks the producer.
>
> - **Example**: P6's logger in the 300 ms stall: $\lambda=200$ records/s, $\mu=0$, $N=32$, $q_0=0$, so $t_{\text{full}}=0.16\,\mathrm{s}$ and $n_{\text{over}}=200\times0.14=28$.
> - **Non-example**: `queue.Queue()` with its default `maxsize=0`, which the documentation defines as infinite — the "grow" policy, whose memory rises for as long as the consumer is stalled.
> - **Why it matters**: the policy chooses the failure you accept — lost records, a stalled producer or growing memory — and a control thread must never be the one that blocks.

**The policies in Python**, on one thread so the output is deterministic:

```python
import queue
from collections import deque

q = queue.Queue(maxsize=2)                     # a bounded buffer of 2 slots
for record in ("tick at 5 ms", "tick at 10 ms", "tick at 15 ms"):
    try:
        q.put_nowait(record)                   # never wait: if the buffer is full, drop the newest
    except queue.Full:
        print("full, dropped:", record)
print("in the queue:", [q.get_nowait() for _ in range(2)])
ring = deque(maxlen=3)                         # a bounded deque drops the oldest instead
for t in range(5, 30, 5):
    ring.append(t)
print("deque keeps:", list(ring))
```

```text
full, dropped: tick at 15 ms
in the queue: ['tick at 5 ms', 'tick at 10 ms']
deque keeps: [15, 20, 25]
```

`put_nowait` raises `queue.Full` instead of waiting, so catching it drops the newest record — the control thread's side of the logger. A plain `put()` blocks the producer until a slot frees — the right policy when every item matters and the producer can wait, as a data loader's workers can (§9), and never for a control thread. `collections.deque(maxlen=N)` discards from the opposite end and keeps the newest $N$ — drop-oldest, with appends and pops the documentation calls thread-safe, and the same rule as a ROS 2 subscription's keep-last history ([[04-robotics/ros2/qos-executors-time|25.5 §2]]).

**The trap.** Dropping the wrong end. For goals only the newest matters, so drop the oldest; for a log both ends matter, so drop either — but count the drops, or a gap in the log looks like a quiet robot.

### Worked case · 대상으로 한 번 끝까지

One vision period of P6's node, with the Running object and §3–§6. The picture is this case and the lab (§11) prints every number; the problem set then turns the knobs.

**Step 1 — count the overlaps.** `on_goal` runs four atomic steps (store $p$, store $s$, load `n_cb`, store `n_cb` + 1) and so does the tick (load $p$, load $s$, load `n_cb`, store `n_cb` + 1), so they can interleave in

$$I(4,4)=\binom{8}{4}=\frac{8!}{4!\,4!}=70$$

orders, since an order is fixed by the four positions of `on_goal`'s steps among the eight. The lab runs all 70: 22 are clean, 8 tear the goal only, 28 lose an update only and 12 do both — 20 tear and 40 lose. The picture's ABBAABAB is one of the 12.

**Step 2 — price the torn read.** A torn pair mixes two goals one vision period apart:

$$\Delta a=T_v=20\,\mathrm{ms}=0.29\,B,\qquad \Delta p=v\,T_v=0.5\,\mathrm{m/s}\times0.020\,\mathrm{s}=0.010\,\mathrm{m}=20.5\ \text{counts}$$

because consecutive goals are 20 ms apart and the target moves at 0.5 m/s: the position is 10 mm — 20.5 encoder counts — from where its stamp puts it, and its age is wrong by 29% of the budget. The direction matters. $(0.500\,\mathrm{m},\,1020\,\mathrm{ms})$ passes a staler position off as fresh: at $t=1085\,\mathrm{ms}$ it is 85 ms old, over budget, yet stamped 65 ms old, and a staleness check accepts it. $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$ does the reverse: at $t=1075\,\mathrm{ms}$ a 55 ms-old goal looks 75 ms old and is rejected.

**Step 3 — the lost update.** One increment each: $I(2,2)=6$ orders, 4 of which leave `n_cb` at 101 instead of 102. The health check undercounts only when the callbacks overlap — rarely, silently, and most often under load, which is when the check matters.

**Step 4 — the deadlock.** Tick: `goal_lock` then `log_lock`; writer: the reverse. 2 of the 6 schedules deadlock, and then both threads stop for good — no command, no log line, the motor on its last command. With the writer taking `goal_lock` first, 0 of 2.

**Step 5 — the log queue in the stall.** With $\mu=0$ during the stall, the empty 32-slot queue fills after

$$t_{\text{full}}=\frac{N}{\lambda}=\frac{32}{200\,\mathrm{s^{-1}}}=0.160\,\mathrm{s},\qquad n_{\text{over}}=\lambda\,(D-t_{\text{full}})=200\,\mathrm{s^{-1}}\times0.140\,\mathrm{s}=28$$

since records keep arriving and none leaves until the disk returns at 300 ms. The four policies (lab, part 3):

| policy | records lost | the control thread | queue peak | empty again at |
|---|---:|---|---:|---:|
| drop newest | 28 (made 165–300 ms) | never waits | 32 | 339 ms |
| drop oldest | 28 (made 5–140 ms) | never waits | 32 | 339 ms |
| block | 0 | stuck in `put()` 165–301 ms: 136 ms, 27 ticks never run | 32 | 340 ms |
| grow | 0 | never waits | 60 records, 3,840 bytes | 374 ms |

Blocking breaks P6: the motor gets no new command from the tick at 165 ms to the one at 305 ms — 140 ms, twice the budget. Growing costs 3,840 bytes here, and 12.8 kB/s — 46 MB an hour — while a disk stays away, so "grow with a cap" and "drop newest and count the drops" are both fair for P6's small records.

**Step 6 — the fixes, each checked in the lab.** `goal_lock` on both sides, or one tuple published in one assignment: 2 orders, both consistent. The increment under the lock: 2 orders, both 102. One lock order: no deadlock. A non-blocking put with a drop counter in the control thread, and a writer that holds `log_lock` only to swap buffers.

### 7. What parallelism buys: Amdahl's law and the data-loader pipeline

*In one sentence:* adding workers speeds up only the divisible part of a job, so the rest sets a ceiling — and a pipeline runs at the rate of its slowest stage.

**The problem.** The preprocessing job takes 120 s on one core. The workstation has 8. Will it take 15 s?

**The idea, as arithmetic.** Split the 120 s by what can be divided. Reading the file and joining the results cannot: $120\times(1-0.9)=12\,\mathrm{s}$ stays serial. The per-window arithmetic can: $108\,\mathrm{s}$ shared by 8 cores is $13.5\,\mathrm{s}$. The job takes $12+13.5=25.5\,\mathrm{s}$, a speedup of $120/25.5=4.71$, not 8 — and with a thousand cores it would still take more than the serial 12 s. The **speedup** is the one-worker time divided by the $n$-worker time, and the serial part caps it.

> **Amdahl's law, defined.** **Amdahl's law** is *an upper bound on the speedup of a fixed-size job of which a fraction $P$ of the one-worker time can be spread over workers* — a bound, not a prediction. Four conditions: the **problem size is fixed** (for a problem that grows with the workers, the same guide gives Gustafson's law, $S=N+(1-P)(1-N)$); the parallel part **divides perfectly**; the serial part **does not shrink**; and **nothing else is added** — no start-up, communication or lock waiting.
>
> $$S(n)=\frac{1}{(1-P)+P/n},\qquad \lim_{n\to\infty}S(n)=\frac{1}{1-P}$$
>
> where $n$ is the number of workers and $P$ the parallelizable fraction (NVIDIA CUDA C++ Best Practices Guide §4.1.3.1) — the arithmetic above divided by $T_1$, so the serial fraction alone sets the ceiling.
>
> - **Example**: the preprocessing job: $S(8)=1/(0.1+0.9/8)=4.71$, so 120 s becomes 25.5 s on 8 cores, and the limit is $1/0.1=10$.
> - **Non-example**: the data loader below, whose stages work on different batches at once; its rate is its slowest stage's, not Amdahl's formula.
> - **Why it matters**: it tells you the most you can gain before you write parallel code, and every critical section all workers pass through (§4) belongs to the serial part.

**Numbers** (lab, part 4):

| $P$ | $n=1$ | 2 | 4 | 8 | 16 | 64 | limit |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 1.00 | 1.33 | 1.60 | 1.78 | 1.88 | 1.97 | 2 |
| 0.90 | 1.00 | 1.82 | 3.08 | 4.71 | 6.40 | 8.77 | 10 |
| 0.95 | 1.00 | 1.90 | 3.48 | 5.93 | 9.14 | 15.42 | 20 |
| 0.99 | 1.00 | 1.98 | 3.88 | 7.48 | 13.91 | 39.26 | 100 |

At $P=0.9$ the first doubling gives 1.82× and going from 16 to 64 cores only 1.37× more, because by then the serial 10% is most of the time.

**The trap: a pipeline is not Amdahl.** The DataLoader's stages work at the same time on different batches — $W$ workers each load a batch in 40 ms, the main process spends 1 ms receiving it, the GPU spends 10 ms on the step — so the whole runs at the rate of its slowest stage:

$$R(W)=\min\Big(\frac{W}{t_{\text{load}}},\ \frac{1}{t_{\text{main}}},\ \frac{1}{t_{\text{GPU}}}\Big),\qquad u=R\,t_{\text{GPU}}$$

because a batch cannot leave a stage faster than that stage makes it, where $R$ is batches per second and $u$ the GPU's busy fraction. With one worker, batches arrive every 40 ms and the GPU works 10 ms of each 40: busy 25%. With `num_workers=0` nothing overlaps: 51 ms per batch.

| workers $W$ | 0 | 1 | 2 | 3 | 4 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| batches/s | 19.6 | 25.0 | 50.0 | 75.0 | 100.0 | 100.0 |
| GPU busy | 19.6% | 25.0% | 50.0% | 75.0% | 100.0% | 100.0% |

The GPU is fed at $W=\lceil t_{\text{load}}/t_{\text{GPU}}\rceil=\lceil40/10\rceil=4$; more workers only wait. A GPU busy 25% of the time shows on a profiler's timeline as short steps between long gaps ([[03-deep-learning/foundations/gpu-computing|1.4 §7]]), and the gaps are the loader.

### 8. Python threads and the global interpreter lock

*In one sentence:* in standard CPython only one thread runs Python bytecode at a time, so threads give concurrency for waiting but not parallelism for computing — and they do not make your code atomic.

**The problem.** Two puzzles with one cause. Python preprocessing split over 8 threads runs no faster than on one. And the racy counter of §3 passes every test.

**The idea.** CPython has one lock around its interpreter, like a single talking stick: only the thread holding it may run Python code, and threads pass it around. A thread gives it up while it waits for I/O, and the holder is asked to pass it on every few milliseconds.

> **Global interpreter lock, defined.** The **global interpreter lock** (GIL) is *the mechanism CPython uses to make sure only one thread executes Python bytecode at a time* (Python glossary) — a property of the interpreter build, not of the language. Four conditions: **one holder**, which alone may run bytecode; it is **released while a thread waits for I/O**, and extensions may release it in long computations — NumPy does for many low-level operations; the holder is **asked to hand it over after the switch interval**, 5 ms by default (What's New in Python 3.2 shows `sys.getswitchinterval()` returning 0.005, as on this machine), with switches only between bytecode instructions; and it is **optional**: a free-threaded build runs without it.
>
> $$N_{\text{bc}}(t)\le1\ \ \text{per interpreter},\qquad S_{\text{Python}}(n)\le1$$
>
> where $N_{\text{bc}}(t)$ counts the threads running bytecode at time $t$ and $S_{\text{Python}}(n)$ is the speedup of $n$ threads on pure-Python computation, so threads can overlap their waiting but never their Python arithmetic.
>
> - **Example**: P6's node in Python: `on_goal` and the tick interleave but never run Python at the same moment, and a callback computing in pure Python can delay the tick by about one switch interval — 5 ms, a whole control period — each time the tick wants to run.
> - **Non-example**: the GIL as a lock around your code. It makes each bytecode instruction atomic, not each line, and the FAQ lists `i = i+1` as not atomic.
> - **Why it matters**: it decides the tool — threads for waiting, processes for computing (§9).

**Numbers: what the GIL hides, measured.** Whether a run shows a possible race depends on where the interpreter happens to switch. This script runs two real threads, so its counts depend on timing and it stays out of CI:

```python
# not-run: real threads - the counts depend on timing, so this block stays out of CI
import sys, threading, time

class Msg:                                   # fields behind properties, as in a generated message class
    def __init__(self, k): self._p, self._s = k, k
    p = property(lambda self: self._p)
    s = property(lambda self: self._s)

class Store:                                 # what on_goal writes and the control tick reads
    p = s = 0
    goal = (0, 0)

def two_stores(k):   Store.p = k; Store.s = k
def from_msg(k):     m = Msg(k); Store.p = m.p; Store.s = m.s     # a property call between the two stores
def one_tuple(k):    Store.goal = (k, k)                          # a single reference store
def read_two():      return Store.p, Store.s
def read_tuple():    return Store.goal

def torn_reads(write, read, seconds=1.0):
    """Writer and reader threads for one second; count the pairs the reader saw with p != s."""
    box = {"stop": False, "torn": 0, "reads": 0}
    def writer():
        k = 0
        while not box["stop"]:
            k += 1; write(k)
    def reader():
        while not box["stop"]:
            p, s = read(); box["reads"] += 1; box["torn"] += p != s
    threads = [threading.Thread(target=writer), threading.Thread(target=reader)]
    for t in threads: t.start()
    time.sleep(seconds); box["stop"] = True
    for t in threads: t.join()
    return box["torn"], box["reads"]

n_cb = 0
def plus_one(x): return x + 1
def bare(N):
    global n_cb
    for _ in range(N): n_cb += 1
def with_call(N):
    global n_cb
    for _ in range(N):
        r = n_cb; r = plus_one(r); n_cb = r               # read, a call, write
def lost_updates(body, N=1_000_000):
    global n_cb
    n_cb = 0
    threads = [threading.Thread(target=body, args=(N,)) for _ in range(2)]
    for t in threads: t.start()
    for t in threads: t.join()
    return 2 * N - n_cb

print(sys.version.split()[0], sys.platform)
for body in (bare, with_call):
    print("%-10s updates lost of 2,000,000:" % body.__name__, [lost_updates(body) for _ in range(5)])
for name, w, r in (("two stores", two_stores, read_two), ("from message", from_msg, read_two),
                   ("one tuple", one_tuple, read_tuple)):
    print("%-12s (torn, reads):" % name, [torn_reads(w, r) for _ in range(3)])
```

Its output on this page's machine (Python 3.12.4, macOS on Apple silicon):

```text
3.12.4 darwin
bare       updates lost of 2,000,000: [0, 0, 0, 0, 0]
with_call  updates lost of 2,000,000: [543241, 560489, 660005, 581193, 598678]
two stores   (torn, reads): [(0, 722215), (0, 959396), (0, 607897)]
from message (torn, reads): [(121339, 875444), (105810, 442423), (176962, 668146)]
one tuple    (torn, reads): [(0, 1189642), (0, 895147), (0, 824756)]
```

| experiment, two threads, about a second each | result on this machine |
|---|---|
| `n_cb += 1`, 1,000,000 per thread, 5 runs | no update lost |
| load, a function call, store, 1,000,000 per thread, 5 runs | 27–33% of 2,000,000 lost |
| goal written as two plain attribute stores, 3 runs | 0 torn in 2,289,508 reads |
| goal written from a message's two properties, 3 runs | 13.9–26.5% of reads torn |
| goal published as one tuple, 3 runs | 0 torn in 2,909,545 reads |

The bare increment and the plain stores never failed because on this interpreter a switch did not happen to fall between those instructions. Put a call in between — a helper function, or a property getter like those of generated message classes — and the same race appears at once, in up to a third of the increments. Nothing in the source marks the difference, and another interpreter version may switch elsewhere. Only the last row is safe by construction: one reference store, which the FAQ lists as atomic.

**The trap: the GIL is going away, and the races stay.** Since Python 3.13 CPython can be built without the GIL, and in 3.14 that free-threaded build became officially supported (PEP 779), though not the default. In it, threads run Python truly in parallel, every race of §3 can bite, and its documentation recommends `threading.Lock` over relying on the internal locks of built-in types. Code that is safe by construction — a lock, one assignment, a queue — stays safe.

**When threads are the right tool.** The `threading` documentation's advice: threads for I/O-bound work, `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` for multi-core computation. NumPy adds an exception: threads that spend most of their time in NumPy's low-level code, which releases the GIL, run in parallel — best when each owns its arrays, since two threads reading and writing one array get, in NumPy's words, inconsistent results. A ROS 2 node in Python meets the GIL too: rclpy's executor threads share it ([[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]).

> [!note]- Deeper · 더 깊이
> **Inside the free-threaded build.** `sys._is_gil_enabled()` (3.13+) reports whether the GIL is on, and the official macOS and Windows installers offer the build as an option. Built-in types such as `dict`, `list` and `set` protect themselves with internal locks, which the free-threading HOWTO calls a description of the current implementation, not a guarantee. Single-threaded code runs somewhat slower — the HOWTO measures about 1% on macOS aarch64 to 8% on x86-64 Linux on pyperformance, What's New in Python 3.14 says roughly 5–10% — and importing an extension not marked as supporting free threading may switch the GIL back on, with a warning. NumPy has had experimental support since 2.1.

### 9. Python processes, asyncio and the DataLoader's workers

*In one sentence:* processes side-step the GIL at the price of start-up and copies, asyncio runs many waiting tasks on one thread by switching only at `await`, and a PyTorch DataLoader is a pool of worker processes behind a bounded queue.

**The problem.** Training on P6's logs needs batches decoded and augmented in parallel, which §8 says threads cannot do in Python.

**The idea.** Use processes: each has its own interpreter and so its own GIL. `multiprocessing` side-steps the GIL with subprocesses, and `concurrent.futures.ProcessPoolExecutor` puts a pool of them behind one call; functions and arguments travel to the workers pickled. Two rules for any script that starts processes. Guard its entry point with `if __name__ == "__main__":` (the script structure of [[02-foundations/tools/python-research-code|12.3 Python for Research Code §8]]) — the package requires the `__main__` module to be importable by the children, and the documentation's programming guidelines for the `spawn` and `forkserver` start methods, the defaults on macOS and Windows and, since Python 3.14, on Linux, ask for the guard. And pass only what can be pickled.

> [!note]- Deeper · 더 깊이
> **Start methods** (the `multiprocessing` documentation). `spawn` starts a fresh interpreter and is the default on Windows and macOS. `fork` copies the parent at `os.fork()`; it is no longer the default anywhere since Python 3.14, and since 3.12 Python warns when it forks a process it knows has other threads. `forkserver` forks from a single-threaded server started early and, since 3.14, is the default on Linux and the other POSIX platforms except macOS. The trouble with `fork` is §4's locks: the child has only the thread that called it but inherits the whole address space, mutex states included, so a lock another thread held at that moment stays locked forever in the child, which may call only async-signal-safe functions until it calls `exec` (fork(2)).

**The DataLoader, as a rule and its numbers.** PyTorch's documentation starts from the same point — within one process the GIL prevents truly parallel Python across threads — so a `DataLoader` with `num_workers` > 0 starts that many worker processes, each time an iterator is created, and hands each the dataset, `collate_fn` and `worker_init_fn`. Each worker loads `prefetch_factor` batches ahead, 2 by default, so up to $2\times$ `num_workers` batches are loaded ahead of the training loop — a bounded buffer in §6's sense, in which the workers, not the training loop, are held back; for P6's loader with $W=4$ that is 8 batches. `persistent_workers=True` keeps workers alive between epochs, so their start-up (§1) is paid once.

**The traps.** Two come with processes.
- **Memory.** Workers that read the parent's Python objects — a list of a million file names, say — come to hold as much memory for them as the parent: overall, the documentation warns, the number of workers times the size of the parent process. Its workaround is non-refcounted storage such as NumPy, pandas or PyArrow. That is §1's $c=1+W$.
- **Randomness.** Each worker's PyTorch seed is `base_seed + worker_id`, but other libraries' seeds may be duplicated, so every worker returns the same "random" numbers; the documented fix is a `worker_init_fn` that seeds them from `get_worker_info().seed`.

The second trap, run on this page's machine with PyTorch 2.6.0 (not in CI, which has no PyTorch):

```python
# not-run: needs PyTorch, which CI does not have; run on this page's machine with PyTorch 2.6.0
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, get_worker_info

class NoisyWindows(Dataset):                    # 8 windows of P6's log, each with augmentation noise
    def __init__(self):
        self.rng = np.random.default_rng(0)     # made once, in the main process
    def __len__(self):
        return 8
    def __getitem__(self, i):
        return i, float(self.rng.normal())      # the noise drawn for window i

def reseed(worker_id):                          # runs in each worker after PyTorch has seeded it
    info = get_worker_info()                    # this worker's own copy of the dataset, and its seed
    info.dataset.rng = np.random.default_rng(info.seed)

if __name__ == "__main__":
    torch.manual_seed(0)
    for init in (None, reseed):
        loader = DataLoader(NoisyWindows(), batch_size=2, num_workers=2, worker_init_fn=init)
        noise = {int(i): round(float(x), 4) for idx, xs in loader for i, x in zip(idx, xs)}
        print(init.__name__ if init else "no worker_init_fn", noise)
```

```text
no worker_init_fn {0: 0.1257, 1: -0.1321, 2: 0.1257, 3: -0.1321, 4: 0.6404, 5: 0.1049, 6: 0.6404, 7: 0.1049}
reseed {0: 1.0644, 1: 0.8712, 2: -0.0576, 3: -0.8624, 4: 0.7892, 5: 0.4204, 6: -1.1319, 7: -0.0696}
```

Without `worker_init_fn`, windows 0 and 2 get the same noise, and so do 1 and 3, 4 and 6, 5 and 7: each worker holds a copy of the dataset, and so a copy of the same generator in the same state. Half the augmentation is a duplicate and nothing fails. The lab (part 5) shows the mechanism with NumPy alone, together with NumPy's documented way to give workers independent streams, `SeedSequence(seed).spawn(n)`. A run seeded from one base seed is repeatable ([[06-research-practice/experimental-design-reproducibility|research practice 2 §6]]); duplicated streams keep it repeatable too — and wrong.

**asyncio, in one paragraph.** For many waits rather than computation — network clients, a robot's command link, a dashboard — `asyncio` runs concurrent code with `async`/`await` on one thread: an event loop runs every task, a running task keeps the thread until it reaches an `await`, and there it is suspended and the next task runs (the asyncio development guide). Code between two `await`s therefore runs uninterrupted, so no torn read can happen there; but one blocking call stalls everything — a function computing for 1 s delays every task by 1 s — which is why blocking work goes to `loop.run_in_executor`.

### 10. C++ threads and ROS 2 callback groups

*In one sentence:* C++ gives truly parallel threads with no interpreter lock, so §3's races become data races with undefined behaviour, and a ROS 2 node's callback groups are §4's mutual exclusion applied to whole callbacks.

**The problem.** P6's controller will also run as a C++ node under a ROS 2 executor, and there §3–§6 look different: no interpreter lock hides a race, and the executor, not you, decides which callbacks share a thread.

**C++, in one paragraph.** A `std::thread` (C++11) starts running at construction and must be joined or detached before it is destroyed, or the program terminates. `std::mutex` guards shared data; locking one you already own is undefined behaviour, typically a deadlock; it is held through `std::lock_guard`, or `std::scoped_lock` (C++17), which locks several mutexes with a deadlock-avoidance algorithm (cppreference). Two conflicting accesses to one memory location, not both atomic and not ordered by synchronization, are a data race, and a program with one has undefined behaviour ([intro.races]) — not a lost update but anything at all. Clang's ThreadSanitizer finds data races at run time with `-fsanitize=thread`, at a 5–15× slowdown. How a C++ node hands P6's goal from the 50 Hz callback to the 200 Hz tick with a `std::atomic`, inside the rules of a real-time tick, is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code §9]].

**ROS 2, as a map.**

| this page | in a ROS 2 node | taught in |
|---|---|---|
| threads (§1) | a multi-threaded executor's threads | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §1]] |
| a lock (§4) | a mutually exclusive callback group, the default | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §2]] |
| the GIL (§8) | shared by rclpy's executor threads | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §1]] |
| a deadlock (§5) | a synchronous service call inside a callback of the group that must answer it | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §2]] |
| a drop-oldest bounded buffer (§6) | a subscription's keep-last history of depth $N$ | [[04-robotics/ros2/qos-executors-time\|25.5 §2]] |

So P6's goal and counter are safe while `on_goal` and the tick share one mutually exclusive group, and at risk the moment they are split across groups to run in parallel — the Running object's arrangement, which is why §4's fixes are needed.

### 11. The lab: interleavings, a deadlock search, the log queue and Amdahl's law

Five parts on the frozen objects, deterministic, with no threads and no timings, so the output is the same on any machine: (1) interleavings of the counter for $k=1$–5, the torn read, the picture's schedule and the same with a lock; (2) every schedule of the tick and the writer under three lock disciplines; (3) the log queue in 1 ms steps under the four policies, with a sweep of capacity and stall; (4) Amdahl's table, the job and the loader pipeline; (5) why copied random generators repeat each other.

```python
# 12.8 lab: P6's shared goal, callback counter, two locks, log queue and data loader. Standard library and NumPy only.
import pickle
from collections import Counter, deque
from itertools import combinations
from math import comb
import numpy as np

# --- 0. the frozen numbers (Running object) ------------------------------------------------------
T_C, BUDGET = 5, 70                                   # ms: P6's control period and its end-to-end budget
P_OLD, S_OLD, P_NEW, S_NEW = 0.500, 1000, 0.510, 1020 # the goal before and after on_goal: m, ms
N_CB0 = 100                                           # the callback counter before the two callbacks

# --- 1. interleavings: every order in which two threads' steps can run -----------------------------
def interleavings(n_a, n_b):
    """Yield each order of A's n_a steps and B's n_b steps that keeps both threads' own order."""
    for slots in combinations(range(n_a + n_b), n_a):    # the positions A's steps take
        a = set(slots)
        yield "".join("A" if k in a else "B" for k in range(n_a + n_b))

def run(order, prog_a, prog_b, mem):
    """Execute one order. Each step is atomic: a function of shared memory and the thread's registers."""
    mem, regs, nxt = dict(mem), {"A": {}, "B": {}}, {"A": 0, "B": 0}
    for who in order:
        (prog_a if who == "A" else prog_b)[nxt[who]](mem, regs[who])
        nxt[who] += 1
    return mem, regs

def load_n(mem, reg):  reg["n"] = mem["n"]            # read the counter into a register
def store_n(mem, reg): mem["n"] = reg["n"] + 1        # write the register plus one back
def write_p(mem, reg): mem["p"] = P_NEW               # on_goal stores the new goal, one field at a time
def write_s(mem, reg): mem["s"] = S_NEW
def read_p(mem, reg):  reg["p"] = mem["p"]            # the control tick reads it, one field at a time
def read_s(mem, reg):  reg["s"] = mem["s"]

def split(order):
    """True if some increment (a load and its store) has a step of the other thread between them."""
    where = {"A": [], "B": []}
    for k, who in enumerate(order):
        where[who].append(k)
    return any(w[j + 1] != w[j] + 1 for w in where.values() for j in range(0, len(w), 2))

print("1a. two threads, k increments each")
for k in range(1, 6):
    prog = [load_n, store_n] * k
    ends = {o: run(o, prog, prog, {"n": 0})[0]["n"] for o in interleavings(2 * k, 2 * k)}
    orders, final = list(ends), Counter(ends.values())
    right = [o for o in orders if ends[o] == 2 * k]
    assert len(orders) == comb(4 * k, 2 * k) and len(right) == comb(2 * k, k)
    assert all(not split(o) for o in right) and sum(not split(o) for o in orders) == len(right)
    print("k=%d %7d orders, final %d..%2d, right (%2d) in %3d = %6.2f%%, %s"
          % (k, len(orders), min(final), max(final), 2 * k, len(right), 100 * len(right) / len(orders),
             dict(sorted(final.items())) if k <= 2 else "every right order is one with no increment split"))
k = 5                                                 # the schedule that ends at 2
worst = "A" + "BB" * (k - 1) + "A" + "B" + "AA" * (k - 1) + "B"
print("k=5, order %s ends at %d" % (worst, run(worst, [load_n, store_n] * k, [load_n, store_n] * k, {"n": 0})[0]["n"]))

print("1b. on_goal writes p then s; the control tick reads p then s")
goal0 = {"p": P_OLD, "s": S_OLD}
for o in interleavings(2, 2):
    pair = tuple(run(o, [write_p, write_s], [read_p, read_s], goal0)[1]["B"].values())
    kind = "torn" if pair in ((P_NEW, S_OLD), (P_OLD, S_NEW)) else "consistent"
    print("   %s  control reads (%.3f m, %d ms)  %s" % (o, *pair, kind))

print("1c. the picture: both callbacks, four steps each")
vision, control = [write_p, write_s, load_n, store_n], [read_p, read_s, load_n, store_n]
start = {"p": P_OLD, "s": S_OLD, "n": N_CB0}
tally = Counter()
for o in interleavings(4, 4):
    mem, regs = run(o, vision, control, start)
    tally[((regs["B"]["p"], regs["B"]["s"]) in ((P_NEW, S_OLD), (P_OLD, S_NEW)), mem["n"] != N_CB0 + 2)] += 1
print("   %d orders: clean %d, torn only %d, lost only %d, both %d"
      % (sum(tally.values()), tally[(False, False)], tally[(True, False)], tally[(False, True)], tally[(True, True)]))
mem, regs = run("ABBAABAB", vision, control, start)
print("   ABBAABAB: control reads (%.3f m, %d ms); counter %d -> %d, should be %d"
      % (regs["B"]["p"], regs["B"]["s"], N_CB0, mem["n"], N_CB0 + 2))

print("1d. with a lock, each critical section is one step")
def write_goal(mem, reg): write_p(mem, reg); write_s(mem, reg)
def read_goal(mem, reg):  read_p(mem, reg); read_s(mem, reg)
def increment(mem, reg):  load_n(mem, reg); store_n(mem, reg)
for o in interleavings(1, 1):
    print("   goal, order %s: control reads (%.3f m, %d ms)" % (o, *run(o, [write_goal], [read_goal], goal0)[1]["B"].values()))
for k in (1, 5):
    final = Counter(run(o, [increment] * k, [increment] * k, {"n": 0})[0]["n"] for o in interleavings(k, k))
    print("   counter, k=%d: %d orders, final %s" % (k, sum(final.values()), dict(final)))

# --- 2. deadlock: every schedule of two threads that take two locks --------------------------------
def schedules(prog_a, prog_b):
    """Explore every schedule; an acquire can run only while its lock is free. Count how they end."""
    ends = Counter()
    def go(i, j, held):
        moves = [(who, op, lock) for who, prog, x in (("A", prog_a, i), ("B", prog_b, j)) if x < len(prog)
                 for op, lock in (prog[x],) if op == "release" or lock not in held]
        if not moves:
            ends["finish" if (i, j) == (len(prog_a), len(prog_b)) else "deadlock"] += 1
        for who, op, lock in moves:
            go(i + (who == "A"), j + (who == "B"), held | {lock} if op == "acquire" else held - {lock})
    go(0, 0, frozenset())
    return ends

def nested(first, second):                            # take first, then second while still holding first
    return [("acquire", first), ("acquire", second), ("release", second), ("release", first)]

tick = nested("goal_lock", "log_lock")                # the control tick logs the goal it holds
print("2. the log writer takes its two locks ...")
for name, writer in (("in the opposite order", nested("log_lock", "goal_lock")),
                     ("in the same order", nested("goal_lock", "log_lock")),
                     ("one at a time", [("acquire", "goal_lock"), ("release", "goal_lock"),
                                        ("acquire", "log_lock"), ("release", "log_lock")])):
    e = schedules(tick, writer)
    print("   %-22s %d schedules, %d finish, %d deadlock" % (name, sum(e.values()), e["finish"], e["deadlock"]))

# --- 3. the log queue: 200 records/s into N slots; the writer drains 1 per ms after a stall -------
def log_queue(N, policy, stall=300, horizon=600, period=T_C):
    """1 ms steps. The writer is stalled while t <= stall, then writes one record per ms.
    The control thread makes one record per tick; when the queue is full, the policy decides."""
    q, dropped, lost, peak, blocked_at, blocked, empty_at, due = deque(), 0, 0, 0, None, 0, None, period
    for t in range(1, horizon + 1):
        if t > stall and q:                           # the writer
            q.popleft()
            if not q and empty_at is None:
                empty_at = t
        if blocked_at is not None:                    # the control thread is stuck in put()
            if len(q) < N:
                q.append(t); blocked, blocked_at = t - blocked_at, None
                due = (t // period + 1) * period      # a late tick does not catch up
            elif t % period == 0:
                lost += 1                             # a tick that falls due and never runs
        elif t == due:
            due += period
            if len(q) < N or policy == "grow":
                q.append(t)
            elif policy == "drop newest":
                dropped += 1
            elif policy == "drop oldest":
                q.popleft(); q.append(t); dropped += 1
            else:                                     # "block"
                blocked_at = t
        peak = max(peak, len(q))
    return peak, dropped, lost, blocked, empty_at

print("3. N=32, 300 ms stall:   peak  dropped  ticks lost  control blocked  queue empty at")
for policy in ("drop newest", "drop oldest", "block", "grow"):
    print("   %-18s %7d %8d %11d %13d ms %12d ms" % (policy, *log_queue(32, policy)))
print("   'block', control blocked (ms):")
for stall in (100, 300, 1000):
    print("   stall %4d ms: " % stall + "  ".join("N=%3d %3d" % (N, log_queue(N, "block", stall, stall + 400)[3])
                                               for N in (16, 32, 64, 128)))

# --- 4. Amdahl's law, and the data loader as a pipeline --------------------------------------------
def amdahl(P, n):
    return 1 / ((1 - P) + P / n)

print("4. S(n) = 1/((1-P) + P/n)")
for P in (0.5, 0.9, 0.95, 0.99):
    print("   P=%.2f " % P + " ".join("%6.2f" % amdahl(P, n) for n in (1, 2, 4, 8, 16, 64))
          + "   limit %3.0f" % (1 / (1 - P)))
T1, P = 120.0, 0.9                                    # the preprocessing job: seconds on one core, parallel fraction
print("   the job: " + ", ".join("%d cores %.1f s" % (n, T1 / amdahl(P, n)) for n in (1, 2, 4, 8))
      + ", never below %.0f s" % (T1 * (1 - P)))
T_LOAD, T_GPU, T_MAIN = 40.0, 10.0, 1.0               # ms per batch: one worker, the GPU step, the main process
for W in (0, 1, 2, 3, 4, 8):
    rate = 1000 / (T_LOAD + T_MAIN + T_GPU) if W == 0 else min(1000 * W / T_LOAD, 1000 / T_MAIN, 1000 / T_GPU)
    print("   W=%d: %5.1f batches/s, GPU busy %5.1f%%" % (W, rate, 100 * rate * T_GPU / 1000))

# --- 5. why DataLoader workers can repeat each other's 'random' numbers ------------------------------
rng = np.random.default_rng(0)                        # made in a dataset's __init__, in the main process
workers = [pickle.loads(pickle.dumps(rng)) for _ in range(2)]   # spawn pickles the dataset into each worker
draws = [w.normal(size=4) for w in workers]
print("5. copies of one generator: %s and %s, identical: %s"
      % (np.round(draws[0], 4), np.round(draws[1], 4), np.array_equal(*draws)))
streams = [np.random.default_rng(s) for s in np.random.SeedSequence(0).spawn(2)]   # one child per worker
draws = [g.normal(size=4) for g in streams]
print("   spawned streams:           %s and %s, identical: %s"
      % (np.round(draws[0], 4), np.round(draws[1], 4), np.array_equal(*draws)))
```

Its output:

```text
1a. two threads, k increments each
k=1       6 orders, final 1.. 2, right ( 2) in   2 =  33.33%, {1: 4, 2: 2}
k=2      70 orders, final 2.. 4, right ( 4) in   6 =   8.57%, {2: 32, 3: 32, 4: 6}
k=3     924 orders, final 2.. 6, right ( 6) in  20 =   2.16%, every right order is one with no increment split
k=4   12870 orders, final 2.. 8, right ( 8) in  70 =   0.54%, every right order is one with no increment split
k=5  184756 orders, final 2..10, right (10) in 252 =   0.14%, every right order is one with no increment split
k=5, order ABBBBBBBBABAAAAAAAAB ends at 2
1b. on_goal writes p then s; the control tick reads p then s
   AABB  control reads (0.510 m, 1020 ms)  consistent
   ABAB  control reads (0.510 m, 1020 ms)  consistent
   ABBA  control reads (0.510 m, 1000 ms)  torn
   BAAB  control reads (0.500 m, 1020 ms)  torn
   BABA  control reads (0.500 m, 1000 ms)  consistent
   BBAA  control reads (0.500 m, 1000 ms)  consistent
1c. the picture: both callbacks, four steps each
   70 orders: clean 22, torn only 8, lost only 28, both 12
   ABBAABAB: control reads (0.510 m, 1000 ms); counter 100 -> 101, should be 102
1d. with a lock, each critical section is one step
   goal, order AB: control reads (0.510 m, 1020 ms)
   goal, order BA: control reads (0.500 m, 1000 ms)
   counter, k=1: 2 orders, final {2: 2}
   counter, k=5: 252 orders, final {10: 252}
2. the log writer takes its two locks ...
   in the opposite order  6 schedules, 4 finish, 2 deadlock
   in the same order      2 schedules, 2 finish, 0 deadlock
   one at a time          7 schedules, 7 finish, 0 deadlock
3. N=32, 300 ms stall:   peak  dropped  ticks lost  control blocked  queue empty at
   drop newest             32       28           0             0 ms          339 ms
   drop oldest             32       28           0             0 ms          339 ms
   block                   32        0          27           136 ms          340 ms
   grow                    60        0           0             0 ms          374 ms
   'block', control blocked (ms):
   stall  100 ms: N= 16  16  N= 32   0  N= 64   0  N=128   0
   stall  300 ms: N= 16 216  N= 32 136  N= 64   0  N=128   0
   stall 1000 ms: N= 16 916  N= 32 836  N= 64 676  N=128 356
4. S(n) = 1/((1-P) + P/n)
   P=0.50   1.00   1.33   1.60   1.78   1.88   1.97   limit   2
   P=0.90   1.00   1.82   3.08   4.71   6.40   8.77   limit  10
   P=0.95   1.00   1.90   3.48   5.93   9.14  15.42   limit  20
   P=0.99   1.00   1.98   3.88   7.48  13.91  39.26   limit 100
   the job: 1 cores 120.0 s, 2 cores 66.0 s, 4 cores 39.0 s, 8 cores 25.5 s, never below 12 s
   W=0:  19.6 batches/s, GPU busy  19.6%
   W=1:  25.0 batches/s, GPU busy  25.0%
   W=2:  50.0 batches/s, GPU busy  50.0%
   W=3:  75.0 batches/s, GPU busy  75.0%
   W=4: 100.0 batches/s, GPU busy 100.0%
   W=8: 100.0 batches/s, GPU busy 100.0%
5. copies of one generator: [ 0.1257 -0.1321  0.6404  0.1049] and [ 0.1257 -0.1321  0.6404  0.1049], identical: True
   spawned streams:           [ 1.4437 -0.8959  0.736   0.0059] and [ 0.8051 -1.9121 -3.4966  0.9338], identical: False
```

**Reading the output.** Parts 1–4 are the tables of §3–§7 and the Worked case; three things are new here.
- **A lock removes the bad orders; it does not make them unlikely.** For every $k$ the orders that end at $2k$ are exactly the unsplit ones, $\binom{2k}{k}$ of them — the same count part 1d gets by making each increment one step.
- **Capacity buys time, not safety.** Under "block", a 100 ms stall is absorbed by 32 slots and a 300 ms stall needs 64, but a 1,000 ms stall still stops the control thread for 356 ms with 128: each slot covers only 5 ms. Only the policy — never blocking the control thread — covers every stall.
- **Copies repeat, spawned streams do not.** Two pickled copies of `default_rng(0)` draw the same four numbers; two children of one `SeedSequence` draw different ones — §9's DataLoader trap without PyTorch.

### 12. What this page does not cover

Memory ordering (C++'s `std::memory_order`) and lock-free data structures; the single-producer single-consumer ring buffer and the real-time rules for a control loop are in [[02-foundations/algorithms/interview-code|11.7 §6]]. Condition variables, semaphores and events are in the `threading` documentation. Response-time analysis of ROS 2 callback chains is pointed to from [[04-robotics/ros2/executors-callbacks-time|25.5.1 §6]]; GPU streams and host synchronization are [[03-deep-learning/foundations/gpu-computing|1.4 §7]]. Distributed training, the theory of deadlock prevention and detection (the 1971 survey in the Sources) and model checkers are not covered; running a data loader on a cluster node's allocated cores, with its data staged there, is [[02-foundations/tools/gpu-clusters|12.7 GPU Clusters §8]].

### After reading

- [ ] Say what threads of one process share and why a data loader's workers are processes while P6's callbacks are threads.
- [ ] Explain why one Python line is several steps that another thread can come between.
- [ ] Trace a lost update step by step, count interleavings with $\binom{m_A+m_B}{m_A}$, and list the orders that tear a two-field goal.
- [ ] Put a lock around a critical section, say what it costs and does not fix, or publish shared data in one assignment.
- [ ] Remove a lock-order deadlock by ranking the locks or by never holding two.
- [ ] Size a bounded buffer against a stall with $t_{\text{full}}$ and $n_{\text{over}}$, and choose its full-queue policy.
- [ ] Bound a speedup with Amdahl's law, find a loader's workers from its slowest stage, and choose threads, processes or asyncio for a Python job.

### Self-check

1. Two threads each run `n_cb += 1` once. How many interleavings of their loads and stores are there, how many lose an update, and why does "it never failed in a million runs" not settle it?
2. The tick reads the goal's two fields under `goal_lock`, but `on_goal` writes them without it. Is the torn read fixed?
3. P6's log writer holds `log_lock` while writing to disk, and the tick takes the same lock to append a record. What does a 300 ms disk stall do to the tick, and what is the fix?
4. The tick takes `goal_lock` then `log_lock`; the writer takes them in the other order. Name the four deadlock conditions here and two one-line fixes.
5. Why does a PyTorch training script load data with worker processes rather than threads, and what goes wrong when the dataset makes a NumPy generator in `__init__`?

> [!tip]- Answers
> 1. $I(2,2)=\binom{4}{2}=6$, and 4 lose an update: both threads load 100 before either stores, so both store 101. A million clean runs show that bad orders are rare on this interpreter, not impossible — here the bare increment lost nothing while the same increment with a call in the middle lost 27–33%. Only an enforced order (a lock, one assignment, a queue) makes every interleaving right.
> 2. No. A lock guards only the code that takes it; `on_goal`'s two stores are not a critical section, so the tick's whole critical section can run between them and read $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$. Lock both sides, or publish one immutable tuple in one assignment.
> 3. The tick waits as long as the writer holds the lock — the whole stall: $300/5=60$ ticks, $300/70=4.3$ budgets without a command. Hold `log_lock` only to swap buffers, write outside it, and give the tick a non-blocking put so a full queue drops a record instead of stopping the controller.
> 4. Mutual exclusion (one holder per lock), hold and wait (each holds its first lock while waiting for its second), no preemption (neither lock can be taken away), circular wait (tick → `log_lock` → writer → `goal_lock` → tick). Make the writer take `goal_lock` first (no cycle), or copy the goal and release `goal_lock` before taking `log_lock` (no hold and wait); the lab finds 2 deadlocking schedules of 6 before, 0 after either.
> 5. Within one process the GIL prevents truly parallel Python across threads, so decoding and augmenting in threads would not run in parallel; each worker process has its own interpreter. But each worker gets a copy of the dataset, generator included, in the same state, so all draw the same "random" numbers — here windows 0 and 2 got the same noise. Seed each worker in `worker_init_fn` from `get_worker_info().seed`, or give each a stream from `SeedSequence.spawn`.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and [[02-foundations/lab-plants|0.6 Lab Plants]]. Every problem turns a knob — a third field in the goal, a third lock, a larger queue in a longer stall, a more parallel job, a slower loader — so none of the page's numbers can be copied.

1. **Draw.** The picture for the variant. (a) The goal gains a sequence number $q$, 50 → 51, stored after $p$ and $s$ and read after them: draw one order of `on_goal`'s three stores and the tick's three loads that tears it, with the shared memory after each step. (b) A disk monitor takes a new `disk_lock` then `goal_lock`, the writer now takes `log_lock` then `disk_lock`, and the tick still takes `goal_lock` then `log_lock`: draw the wait-for cycle and mark the arrow a lock order removes. (c) The log queue with $N=48$ slots in a $D=400\,\mathrm{ms}$ stall under "drop newest" and "grow", with the interval "block" would stop the control thread.
2. **Derive.** (a) Count the interleavings of three stores and three loads, and among them the orders in which the tick reads all old, all new, or a torn mix (field $i$ is new exactly when its store precedes its load); compare the torn share with the two-field goal's. (b) Give a schedule in which the three threads of 1(b) deadlock, name the four conditions, and give lock ranks and the one thread that must change. (c) For $N=48$ and $D=400\,\mathrm{ms}$: $t_{\text{full}}$, the records over capacity, how long "block" holds the control thread and how long the motor goes without a command against the 70 ms budget, and the "grow" peak in bytes. (d) Amdahl with $P=0.95$: the 120 s job on 8 cores and its floor; and a loader with $t_{\text{load}}=60\,\mathrm{ms}$ and $t_{\text{GPU}}=8\,\mathrm{ms}$: the fewest workers that keep the GPU busy, and its busy share with 4.
3. **Do.** Fill the `?` blanks, run the block after the lab of §11, and compare its (a)–(c) with your derivations and with the page's two-field, $N=32$ and $P=0.9$ numbers.

```python
# Problem 3 (Do). A three-field goal, a larger queue in a longer stall, a more parallel job, a slower loader.
# Run after the lab of §11: it uses interleavings, run, the step functions, log_queue and amdahl. Fill ?.
SEQ_OLD, SEQ_NEW = 50, 51                        # the goal's third field: a sequence number
def write_q(mem, reg): mem["q"] = ?              # on_goal's third store
def read_q(mem, reg):  reg["q"] = ?              # the tick's third load
old3, new3 = (P_OLD, S_OLD, SEQ_OLD), (P_NEW, S_NEW, SEQ_NEW)
views = Counter()
for o in interleavings(?, ?):
    got = tuple(run(o, [write_p, write_s, write_q], [read_p, read_s, read_q],
                    dict(zip("psq", old3)))[1]["B"].values())
    views["old" if got == old3 else "new" if got == new3 else "torn"] += 1
print("(a) three fields: %d orders, %d old, %d new, %d torn"
      % (sum(views.values()), views["old"], views["new"], views["torn"]))

print("(b) N=48, 400 ms stall:  peak  dropped  ticks lost  blocked (ms)  empty at (ms)")
for policy in ("drop newest", "drop oldest", "block", "grow"):
    print("    %-12s %8d %8d %11d %13d %14d" % (policy, *log_queue(?, policy, stall=?, horizon=700)))

P2 = ?                                           # the more parallel job
print("(c) P=%.2f: " % P2 + "  ".join("n=%d %.2f" % (n, amdahl(P2, n)) for n in (2, 4, 8, 16))
      + "; the 120 s job on 8 cores: %.2f s, never below %.0f s" % (120 / amdahl(P2, 8), 120 * (1 - P2)))
T_LOAD, T_GPU = ?, ?                             # the slower loader: ms per batch per worker, ms per GPU step
for W in (1, 4, 7, 8, 12):
    rate = min(?, 1000 / T_MAIN, 1000 / T_GPU)  # batches/s: the slowest stage
    print("    W=%2d: %6.2f batches/s, GPU busy %5.1f%%" % (W, rate, 100 * rate * T_GPU / 1000))
```

> [!note]- How to draw it · 그리는 법
> - (a) One column per atomic step in your order, one lane per thread, and one row per field of shared memory with its value after every step; the torn read is the triple the tick's loads return, which no store wrote as a whole.
> - (b) Threads as boxes, locks as rounded boxes; a solid arrow from a lock to its holder, a dashed arrow from a thread to the lock it waits for. With ranks `goal_lock` < `log_lock` < `disk_lock`, the forbidden arrow is the wait from a higher-ranked lock held to a lower-ranked lock.
> - (c) Time across from the stall's start, records up, a dashed line at the capacity, the stall shaded. "Drop newest" rises at 200 records/s to $N$, stays flat until the disk returns, then falls at the net 800/s; "grow" rises to $\lambda D$ and falls at the same rate; "block" is a bar from the first tick that finds the queue full to the writer's first write, labelled with the ticks it swallows.

> [!tip]- Solutions
> 1. (a) For example AABBBA: `on_goal` stores $p=0.510$ and $s=1020$, the tick loads all three, and only then is $q=51$ stored. Memory reads $(0.510, 1000, 50)$, then $(0.510, 1020, 50)$ to step 5, then $(0.510, 1020, 51)$; the tick reads $(0.510\,\mathrm{m},\,1020\,\mathrm{ms},\,50)$ — goal 51's data under goal 50's number. (b) Tick → `log_lock` → writer → `disk_lock` → monitor → `goal_lock` → tick; the monitor's wait for `goal_lock` while holding `disk_lock` goes down in rank and is the arrow to remove. (c) Both curves reach 48 at 240 ms; "drop newest" stays at 48 until 400 ms, drops 32 records and is empty at 459 ms; "grow" peaks at 80 at 400 ms and is empty at 499 ms; the "block" bar runs 245–401 ms, 156 ms, 31 ticks.
> 2. (a) $\binom{6}{3}=20$: 5 all old, 5 all new, 10 torn — 50% against $2/6=33\%$ for two fields. (The all-old and all-new counts are the Catalan numbers 2, 5, 14, …, so $n$ fields tear in a share $(n-1)/(n+1)$ of the orders.) (b) The tick takes `goal_lock`, the writer `log_lock`, the monitor `disk_lock`, and each then asks for the lock the next one holds. Mutual exclusion, hold and wait, no preemption, circular wait (the cycle of 1(b)). With ranks `goal_lock` < `log_lock` < `disk_lock`, the tick and the writer already climb; the monitor must take `goal_lock` before `disk_lock`, or copy the goal and release `goal_lock` first. (c) $t_{\text{full}}=48/200=0.240\,\mathrm{s}$; $n_{\text{over}}=200\times(0.400-0.240)=32$. "Block" holds the tick at 245 ms until the writer's first write at 401 ms, 156 ms, and the 31 ticks due from 250 to 400 ms never run; no new command from 245 to 405 ms, 160 ms, 2.29 budgets. "Grow" peaks at $200\times0.4=80$ records, $80\times64=5{,}120$ bytes. (d) $S(8)=1/(0.05+0.95/8)=5.93$: 120 s becomes 20.25 s, never below $120\times0.05=6\,\mathrm{s}$. The loader needs $\lceil60/8\rceil=\lceil7.5\rceil=8$ workers; with 4 it delivers $4/0.060=66.67$ batches/s and the GPU is busy $66.67\times0.008=53.3\%$.
> 3. The blanks, in order: `SEQ_NEW`, `mem["q"]`, `3, 3`, `48` and `400` in the queue call, `0.95` for `P2`, `60.0, 8.0` and `1000 * W / T_LOAD`. The output:
>
>    ```text
>    (a) three fields: 20 orders, 5 old, 5 new, 10 torn
>    (b) N=48, 400 ms stall:  peak  dropped  ticks lost  blocked (ms)  empty at (ms)
>        drop newest        48       32           0             0            459
>        drop oldest        48       32           0             0            459
>        block              48        0          31           156            460
>        grow               80        0           0             0            499
>    (c) P=0.95: n=2 1.90  n=4 3.48  n=8 5.93  n=16 9.14; the 120 s job on 8 cores: 20.25 s, never below 6 s
>        W= 1:  16.67 batches/s, GPU busy  13.3%
>        W= 4:  66.67 batches/s, GPU busy  53.3%
>        W= 7: 116.67 batches/s, GPU busy  93.3%
>        W= 8: 125.00 batches/s, GPU busy 100.0%
>        W=12: 125.00 batches/s, GPU busy 100.0%
>    ```
>
>    (a) matches 2(a): a third field raises the torn share from a third to a half. (b) Against $N=32$ and 300 ms, 16 more slots bought 80 ms before the queue filled, yet the longer stall still overran it by 32 records, and "block" still stops the control thread for 156 ms, over twice the budget. (c) At $P=0.95$ the job gains 5.93× on 8 cores against 4.71× at $P=0.9$; the slower loader needs 8 workers where the page's needed 4, because $\lceil t_{\text{load}}/t_{\text{GPU}}\rceil$ doubled.

### Sources

- Python 3.14 documentation, [docs.python.org/3](https://docs.python.org/3/) — glossary, library FAQ (thread-safe operations, the GIL), `threading`, `queue`, `collections`, `multiprocessing`, `concurrent.futures`, the asyncio development guide, `sys`, the free-threading HOWTO, What's New in 3.14 and 3.2.
- PyTorch 2.14, [torch.utils.data](https://docs.pytorch.org/docs/2.14/data.html) — worker processes, prefetching, memory with Python objects, worker seeds.
- NumPy 2.5, [thread safety](https://numpy.org/doc/stable/reference/thread_safety.html) and [parallel random number generation](https://numpy.org/doc/stable/reference/random/parallel.html).
- Linux man-pages, [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html) — shared memory, scheduling policies, fork and copy-on-write.
- C++: [intro.races](https://eel.is/c++draft/intro.races) in the working draft, and cppreference on [std::thread](https://en.cppreference.com/w/cpp/thread/thread), [std::mutex](https://en.cppreference.com/w/cpp/thread/mutex), [std::scoped_lock](https://en.cppreference.com/w/cpp/thread/scoped_lock), [std::atomic::fetch_add](https://en.cppreference.com/w/cpp/atomic/atomic/fetch_add).
- Clang, [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) — `-fsanitize=thread` and its cost.
- NVIDIA, [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) v13.4, §4.1.3.1–§4.1.3.2 — Amdahl's and Gustafson's laws.
- G. M. Amdahl, "Validity of the single processor approach to achieving large scale computing capabilities", AFIPS Spring Joint Computer Conference, 1967 — record checked at Crossref.
- E. G. Coffman, M. Elphick, A. Shoshani, "System Deadlocks", ACM Computing Surveys 3(2):67–78, 1971 — a survey of deadlock treatment; record and abstract checked at Crossref.
- This page's machine (macOS on Apple silicon, Python 3.12.4, NumPy 2.0.2, PyTorch 2.6.0) — the measurements of §1, §2, §4, §8 and §9.

## 한국어

*[[02-foundations/lab-plants|0.6 Lab Plants]] 위에 선다. P6의 비전 콜백은 20 ms마다 목표를 저장하고, 제어기는 5 ms마다 그것을 읽는다. 이 둘을 스레드 두 개에 올리고 로거와 데이터 로더를 더하면, 이 페이지가 다루는 버그가 모두 생긴다. 잃어버린 갱신, 찢어진 읽기, 교착, 가득 찬 큐, 그리고 Python의 전역 인터프리터 락이 가려 주는 것들이다. 이 페이지는 그 버그들과 고치는 법을 가르치고, [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]]이 나중에 같은 이야기를 ROS 2 콜백에 적용한다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]가 그리는 피지컬 AI 스택 아래의 바닥, 곧 모든 층이 그 위에서 도는 도구에 속한다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 그 절의 사례 "저 패널을 프레임에 설치해"에서 이 페이지가 맡는 것은 로봇 컴퓨터 한 대 위에서 동시에 도는 단계들이다. 프레임을 알아보는 카메라 콜백이 부품을 옮기고 접촉을 감지하는 제어 루프에 목표를 넘긴다. 공유를 잘못하면 아무것도 죽지 않은 채 실험이 오염된다. P6에서 찢어진 목표는 새 위치를 옛 스탬프와 짝지어 10 mm, 20 ms 어긋나고, 락 순서 교착은 모터가 마지막 명령을 유지하는 동안 노드를 얼리며, 데이터 로더의 워커들은 증강의 절반을 소리 없이 되풀이한다. [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]가 이 페이지를 ROS 2 콜백 그룹에, [[04-robotics/ros2/cpp-for-robot-code|25.0 §9]]가 실시간 C++ 틱에 적용한다. 이 페이지는 학위논문 경로([[07-research-program/index|연구 프로그램 §8]])의 일곱 블록 밖에 있으니, 리그를 위한 ROS 2 빌드 트랙이 25.5.1에 이르기 전, 곧 블록 7보다 앞에, 또는 Python 작업을 처음 병렬화할 때 읽는다. 읽고 나면 공유 데이터를 깨뜨리는 인터리빙을 세고, 락이나 대입 한 번이나 정책을 밝힌 유한 큐로 고치고, 암달의 법칙으로 속도 향상의 상한을 정하고, Python 작업에 스레드·프로세스·asyncio 가운데 무엇을 쓸지 고를 수 있다.

> [!note] 처음이라면 · First pass
> 약 90분씩 두 번. **1회차 — 경쟁 상태를 세기.** 그림을 보고 §1–§3을 읽는다. 여기까지 오면 잃어버린 갱신을 한 단계씩 따라갈 수 있고, 그것을 일으키는 순서의 수를 셀 수 있다. 이어서 그 순서들을 없애는 락, §4를 읽고 스스로 점검 1번과 2번으로 마친다. **2회차 — 나머지 두 해법.** §5와 §6을 읽고, 계산 절에서 세 가지 해법(락, 하나로 정한 락 순서, 정책을 가진 큐)을 P6의 숫자로 본 뒤 스스로 점검 3번과 4번에 답한다. 그다음은 필요할 때: §7–§9(암달의 법칙, GIL, DataLoader)와 스스로 점검 5번은 Python 작업을 병렬화하거나 데이터 로더를 손보기 전에, §10은 C++나 ROS 2 노드를 쓸 때 읽고, §11과 과제는 맨 나중에 한다. 접혀 있는 *더 깊이* 상자는 필요할 때만 연다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**를 소프트웨어 안쪽에서 본다. $T_v=20\,\mathrm{ms}$마다 새 목표를 저장하는 비전 콜백, $T_c=5\,\mathrm{ms}$마다 가장 새 목표를 읽는 제어 틱, 예산 $B=70\,\mathrm{ms}$, 그리고 미터당 2,048 count인 엔코더다. 나머지는 이 페이지가 여기서 고정하는 교과용 숫자이고, 측정값이 아니다.

| 대상 | 교과용 숫자 |
|---|---|
| 목표 | 필드 둘, 위치 $p$(m)와 카메라 스탬프 $s$(ms). 이전 목표는 $(0.500\,\mathrm{m},\,1000\,\mathrm{ms})$, 새 목표는 $(0.510\,\mathrm{m},\,1020\,\mathrm{ms})$다. 대상이 $v=0.5\,\mathrm{m/s}$로 움직이기 때문이다 |
| 콜백 카운터 `n_cb` | 상태 점검을 위해 콜백마다 1을 더한다. 초당 250번. 그림의 두 콜백 전에는 100이다 |
| 락 둘 | `goal_lock`은 목표를, `log_lock`은 로그 버퍼를 지킨다 |
| 로거 | 제어 틱마다 64바이트 기록 하나, $\lambda=200$개/s가 $N=32$칸 큐로 간다. 기록 스레드는 디스크가 응답하는 동안 ms당 $\mu=1$개를 꺼낸다. 디스크가 $D=300\,\mathrm{ms}$ 동안 한 번 멈춘다 |
| 데이터 로더 | 워커 프로세스 $W$개. 워커 하나가 배치 하나에 $t_{\text{load}}=40\,\mathrm{ms}$, 학습 스텝에 $t_{\text{GPU}}=10\,\mathrm{ms}$, 메인 프로세스가 배치마다 $t_{\text{main}}=1\,\mathrm{ms}$ |
| 전처리 작업 | 한 시간 로그를 학습용 윈도로 바꾼다. 코어 하나로 $T_1=120\,\mathrm{s}$, 그중 코어에 나눌 수 있는 비율 $P=0.9$ |

노드는 `on_goal`과 제어 타이머를 두 스레드에서, 멀티스레드 executor의 서로 다른 콜백 그룹에 두고 돌린다. ROS 2에서 executor는 노드의 콜백을 돌리는 루프이고, 콜백 그룹은 그중 어느 콜백끼리 겹쳐 돌 수 있는지를 정한다. 느린 콜백 하나가 타이머를 붙잡지 못하게 하려고 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]가 쓰는 배치다. 그 순간부터 두 콜백은 동시에 돌 수 있고, 둘이 함께 만지는 것이 모두 이 페이지의 주제가 된다.

*범위: 이 페이지는 로봇 학습 연구자가 실제로 만나는 동시성 버그 — 잃어버린 갱신, 찢어진 읽기, 락 순서 교착, 가득 찬 큐, Python 전역 인터프리터 락의 효과 — 와 그 해법, 그리고 그것을 쓰는 데 필요한 만큼의 스레드, 프로세스, 스케줄링, 암달의 법칙, `threading`, `multiprocessing`, `asyncio`, PyTorch DataLoader의 워커를 가르친다. 운영체제 내부, 메모리 순서, 락 없는 프로그래밍, 실시간 스케줄링 분석, GPU 스트림, 분산 학습은 다루지 않는다. C++ 스레드는 [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]]를, ROS 2 콜백 그룹은 [[04-robotics/ros2/executors-callbacks-time|25.5.1]]을 가리키고, 나머지가 어디 있는지는 §12가 말한다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 540" style="max-width:100%;height:auto" role="img" aria-label="장치 P6 위의 세 칸. (a) 비전 콜백 하나와 제어 틱 하나가 여덟 단계에 걸쳐 A B B A A B A B 순서로 끼어든다. 제어 틱은 새 위치 0.510 m를 옛 스탬프 1000 ms와 함께 읽고, 콜백 카운터는 100에서 102가 아니라 101이 된다. (b) 제어 틱은 goal_lock을 쥔 채 log_lock을 기다리고 로그 기록 스레드는 log_lock을 쥔 채 goal_lock을 기다린다. 순환이다. (c) 300 ms 디스크 정지 동안의 로그 큐. 기록이 초당 200개 들어오고 32칸 큐는 160 ms에 찬다. 버리면 기록 28개를 잃고, 막으면 제어 스레드가 165에서 301 ms까지 멈추며, 한없이 늘리면 기록 60개까지 쌓였다가 374 ms에 다시 빈다.">
  <defs><marker id="ccArrowk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) on_goal 하나와 제어 틱 하나가 끼어든다: 원자적 단계 8개, 버그 둘</text>
  <text x="12" y="55" font-size="11" fill="currentColor">on_goal</text>
  <text x="12" y="67" font-size="10" fill-opacity="0.7" fill="currentColor">비전 스레드</text>
  <text x="12" y="93" font-size="11" fill="currentColor">제어 틱</text>
  <text x="12" y="105" font-size="10" fill-opacity="0.7" fill="currentColor">제어 스레드</text>
  <line x1="92" y1="56" x2="540" y2="56" stroke="currentColor" stroke-width="1" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <line x1="92" y1="94" x2="540" y2="94" stroke="currentColor" stroke-width="1" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <text x="120" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">1</text>
  <rect x="94" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="120" y="60" font-size="10" text-anchor="middle" fill="currentColor">p ← 0.510</text>
  <text x="176" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">2</text>
  <rect x="150" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="176" y="98" font-size="10" text-anchor="middle" fill="currentColor">p 읽기</text>
  <text x="232" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">3</text>
  <rect x="206" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="232" y="98" font-size="10" text-anchor="middle" fill="currentColor">s 읽기</text>
  <text x="288" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">4</text>
  <rect x="262" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="288" y="60" font-size="10" text-anchor="middle" fill="currentColor">s ← 1020</text>
  <text x="344" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">5</text>
  <rect x="318" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="344" y="60" font-size="10" text-anchor="middle" fill="currentColor">r ← n</text>
  <text x="400" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">6</text>
  <rect x="374" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="400" y="98" font-size="10" text-anchor="middle" fill="currentColor">r ← n</text>
  <text x="456" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">7</text>
  <rect x="430" y="44" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="456" y="60" font-size="10" text-anchor="middle" fill="currentColor">n ← r+1</text>
  <text x="512" y="37" font-size="10" text-anchor="middle" fill-opacity="0.6" fill="currentColor">8</text>
  <rect x="486" y="82" width="52" height="24" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.1"/>
  <text x="512" y="98" font-size="10" text-anchor="middle" fill="currentColor">n ← r+1</text>
  <text x="12" y="126" font-size="10" fill-opacity="0.8" fill="currentColor">공유 메모리</text>
  <text x="12" y="138" font-size="10" fill-opacity="0.8" fill="currentColor">각 단계 뒤</text>
  <text x="88" y="126" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">p</text>
  <text x="88" y="140" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">s</text>
  <text x="88" y="154" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">n</text>
  <text x="120" y="126" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">0.510</text>
  <text x="120" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="120" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="176" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="176" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="176" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="232" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="232" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1000</text>
  <text x="232" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="288" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="288" y="140" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">1020</text>
  <text x="288" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="344" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="344" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="344" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="400" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="400" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="400" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">100</text>
  <text x="456" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="456" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="456" y="154" font-size="10" text-anchor="middle" font-weight="bold" fill="currentColor">101</text>
  <text x="512" y="126" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">0.510</text>
  <text x="512" y="140" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">1020</text>
  <text x="512" y="154" font-size="10" text-anchor="middle" fill-opacity="0.65" fill="currentColor">101</text>
  <path d="M150 162v5H258v-5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="204" y="180" font-size="11" text-anchor="middle" fill="currentColor">제어가 받은 값 (0.510 m, 1000 ms):</text>
  <text x="204" y="194" font-size="11" text-anchor="middle" fill="currentColor">누구도 발행한 적 없는 목표</text>
  <path d="M318 162v5H538v-5" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="428" y="180" font-size="11" text-anchor="middle" fill="currentColor">n: 100 → 101, 102가 아님</text>
  <text x="428" y="194" font-size="11" text-anchor="middle" fill="currentColor">갱신 하나를 잃음</text>
  <text x="12" y="222" font-size="12" fill="currentColor">(b) 제어 틱과 로그 기록 스레드가 락 둘을 서로 반대 순서로 잡는다</text>
  <rect x="30" y="262" width="140" height="26" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="100" y="279" font-size="11" text-anchor="middle" fill="currentColor">제어 틱</text>
  <rect x="390" y="262" width="140" height="26" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="460" y="279" font-size="11" text-anchor="middle" fill="currentColor">로그 기록 스레드</text>
  <rect x="215" y="236" width="130" height="24" rx="10" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="252" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">goal_lock</text>
  <rect x="215" y="292" width="130" height="24" rx="10" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="308" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">log_lock</text>
  <line x1="215" y1="248" x2="172" y2="266" stroke="currentColor" stroke-width="1.4" marker-end="url(#ccArrowk)"/>
  <text x="178" y="246" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">쥔 쪽</text>
  <line x1="172" y1="284" x2="213" y2="302" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ccArrowk)"/>
  <text x="150" y="312" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">기다림</text>
  <line x1="345" y1="304" x2="388" y2="284" stroke="currentColor" stroke-width="1.4" marker-end="url(#ccArrowk)"/>
  <text x="382" y="314" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">쥔 쪽</text>
  <line x1="388" y1="266" x2="347" y2="248" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ccArrowk)"/>
  <text x="380" y="240" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">기다림</text>
  <text x="280" y="336" font-size="11" text-anchor="middle" fill="currentColor">스케줄 6개 중 2개가 이 순환으로 끝난다. 두 스레드 모두 goal_lock을 먼저 잡으면 2개 중 0개</text>
  <text x="12" y="364" font-size="12" fill="currentColor">(c) 300 ms 디스크 정지 속의 로그 큐: 초당 200개 입력, N = 32칸, ms당 1개 출력</text>
  <rect x="70" y="394" width="345" height="100" fill="currentColor" fill-opacity="0.06"/>
  <text x="74.6" y="405" font-size="10" fill-opacity="0.7" fill="currentColor">디스크 정지, 0–300 ms</text>
  <line x1="70" y1="494" x2="530" y2="494" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70" y1="494" x2="70" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70" y1="494" x2="70" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="70" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <line x1="185" y1="494" x2="185" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="185" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">100</text>
  <line x1="300" y1="494" x2="300" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="300" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">200</text>
  <line x1="415" y1="494" x2="415" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="415" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">300</text>
  <line x1="530" y1="494" x2="530" y2="498" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="530" y="509" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">400</text>
  <text x="65" y="497.5" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="65" y="444.2" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">32</text>
  <text x="65" y="397.5" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">60</text>
  <text x="65" y="384" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">기록</text>
  <line x1="70" y1="440.7" x2="530" y2="440.7" stroke="currentColor" stroke-width="1" stroke-dasharray="5 3" stroke-opacity="0.7"/>
  <text x="530" y="436.7" font-size="10" text-anchor="end" fill-opacity="0.8" fill="currentColor">N = 32</text>
  <polyline points="70,494 254,440.7 415,440.7 459.9,494 530,494" fill="none" stroke="currentColor" stroke-width="2"/>
  <polyline points="70,494 415,394 500.1,494 530,494" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 3"/>
  <text x="336.8" y="453.7" font-size="10" text-anchor="middle" fill="currentColor">최신 버리기: 기록 28개 잃음</text>
  <text x="438" y="400.7" font-size="10" fill="currentColor">늘리기: 300 ms에 60개,</text>
  <text x="438" y="412.7" font-size="10" fill="currentColor">374 ms에 빔</text>
  <text x="435.7" y="480.7" font-size="10" text-anchor="end" fill="currentColor">339 ms에 빔</text>
  <rect x="259.8" y="516" width="156.4" height="6" fill="currentColor" fill-opacity="0.55"/>
  <text x="255.2" y="522" font-size="10" text-anchor="end" fill="currentColor">막기: 제어가 165–301 ms 멈춤</text>
  <text x="420.8" y="522" font-size="10" fill="currentColor">틱 27번이 돌지 못함</text>
  <text x="300" y="535" font-size="10" text-anchor="middle" fill-opacity="0.8" fill="currentColor">정지가 시작된 뒤의 시간 (ms)</text>
</svg>

(a) `on_goal` 하나와 제어 틱 하나가 ABBAABAB 순서로 끼어든다. 틱은 새 위치를 옛 스탬프와 함께 $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$로 읽고, 카운터는 102가 아니라 101로 끝난다. 가능한 순서 70개 중 20개가 목표를 찢고 40개가 갱신을 잃는다. (b) 틱은 `goal_lock`을 쥔 채 `log_lock`을, 로그 기록 스레드는 `log_lock`을 쥔 채 `goal_lock`을 기다린다. 스케줄 6개 중 2개가 이 순환으로 끝나고, 둘 다 `goal_lock`을 먼저 잡으면 하나도 없다. (c) 300 ms 디스크 정지에서 32칸 로그 큐는 160 ms에 찬다. 버리면 기록 28개를 잃고, 막으면 제어 스레드가 165 ms부터 301 ms까지 멈추고, 한없이 늘리면 60개까지 쌓였다가 374 ms에 빈다.

### 1. 프로세스와 스레드: 무엇을 함께 쓰는가

*한 문장으로:* 한 프로세스의 스레드들은 메모리를 함께 쓰고 프로세스끼리는 그렇지 않다. 그래서 스레드는 싸지만 경쟁 상태가 생길 수 있고, 프로세스는 안전하지만 비싸다.

**풀려는 문제.** P6의 노드에는 목표 하나를 함께 만지는 두 활동이 있다. `on_goal`이 쓰고 제어 틱이 읽는다. 학습 작업은 정반대를 원한다. 여러 워커가 공통으로 만지는 것 없이 배치를 동시에 푼다. 운영체제가 주는 실행 단위는 둘이고, 그중 무엇을 고르느냐는 곧 무엇을 공유하느냐의 문제다.

**생각.** **프로세스**(process)를 자기 공구와 작업대를 가진 작업장 하나, 곧 자기 주소 공간으로 생각하자. **스레드**(thread)는 그 작업장 안의 일꾼이다. 한 작업장의 일꾼들은 같은 공구를 쓰고, 각자 가진 것은 수첩 한 권, 곧 스택뿐이다(pthreads(7)). 두 작업장은 소포를 주고받지 않는 한 아무것도 나누지 않는다. `fork()`로 만든 자식 프로세스는 부모의 사본으로 시작하지만, 그 뒤로는 어느 쪽이 쓴 것도 다른 쪽에 보이지 않는다(fork(2)). 셸에서 프로세스를 띄우고, 시그널을 보내고, 멈추는 법은 [[02-foundations/tools/linux-shell|12.1 리눅스와 셸 §3]]이다.

> **스레드의 정의.** **스레드**(thread)는 *운영체제가 따로 스케줄하는, 프로세스 안의 명령 흐름 하나*다. 실행 경로이지 프로그램도 코어도 아니다. 조건 셋. **한 프로세스에 속해 그 메모리를 함께 쓴다**. 그래서 한 스레드가 어느 주소에 쓴 것을 다른 스레드가 그 주소에서 읽는다. **자기 스택과 레지스터를 갖는다**. 그래서 지역 변수와 코드 속 자기 위치는 자기만의 것이다. 그리고 **따로 스케줄된다**. 그래서 두 스레드가 두 코어에서 동시에 돌 수도, 한 코어에서 번갈아 돌 수도 있다.
>
> $$c=\begin{cases}1 & n\ \text{threads of one process}\\ 1+n & \text{a main process and}\ n\ \text{worker processes}\end{cases}$$
>
> $c$는 워커 $n$개가 읽는 데이터의 사본 수다. 그러므로 워커 수에 따라 메모리가 느는 것은 워커가 프로세스일 때뿐이다.
>
> - **예**: P6의 노드에는 두 콜백 스레드가 함께 보는 목표가 하나 있다. §3이 그것을 찢을 수 있는 이유가 바로 이것이다. 워커 프로세스 $W=4$개와 Python 객체 3 GB짜리 데이터셋(교과용 숫자)을 쓰는 데이터 로더는 사본 $c=5$개, 15 GB까지 갈 수 있다(§9).
> - **비예**: fork한 자식. 같은 목표를 들고 시작하지만, 부모의 `on_goal`이 새 목표를 써도 자식은 옛 목표를 계속 읽고, 아무도 그 사실을 알려 주지 않는다.
> - **왜 중요한가**: 공유 덕분에 스레드는 띄우기도 말을 주고받기도 빠르다. 그리고 모든 경쟁 상태가 필요로 하는 것 — 스레드 둘, 주소 하나, 쓰기 하나 — 이 바로 그 공유다.

**숫자로.** 둘이 가장 크게 다른 것은 띄우는 비용이다. 이 페이지를 쓴 기계(Apple silicon의 macOS, Python 3.12.4, 세 번 돌린 중앙값)에서 잰 값이고, 교과용 숫자가 아니라 이 기계의 측정값이다.

| | 한 프로세스의 스레드들 | 서로 다른 프로세스들 |
|---|---|---|
| 메모리 | 공유. 한 스레드가 쓴 것을 다른 스레드가 모두 읽는다 | 따로. 데이터는 사본으로 오간다. Python `multiprocessing`은 pickle한다. 곧 바이트로 직렬화해 보낸다 |
| 한쪽의 충돌 | 프로세스 전체를 쓰러뜨린다 | 그 프로세스 안에 머문다 |
| 빈 것을 띄우고 join하기 | 31–39 µs | `spawn`으로 46–48 ms |

`spawn`으로 띄운 프로세스는 새 인터프리터를 띄우고 그것이 프로그램을 다시 import하므로, 스레드 천 개 넘게 든다.

**함정.** 편해서 스레드를 골랐다가 생각보다 많은 것을 공유하게 되는 것. 공유를 기준으로 고른다. P6의 목표는 한 콜백이 쓰고 다른 콜백이 읽는 사본 하나여야 하므로 콜백은 스레드이고, 그 값이 §3–§5다. 로더의 워커들은 함께 쓰는 것이 없으므로 프로세스여도 되고, 그 값은 사본과 띄우는 시간이다(§9).

### 2. 스케줄링: 스레드는 왜 어느 두 단계 사이에서도 멈출 수 있는가

*한 문장으로:* 스레드는 자기가 고르지 않은 지점에서 멈춰지거나 다른 코어에서 다른 스레드와 같은 순간에 돌 수 있으므로, 한 스레드의 두 단계가 이어서 돈다는 보장은 없다.

**풀려는 문제.** 목표의 위치를 저장하고 그다음 스탬프를 저장하는 두 줄을 쓰면, 머릿속에서는 둘이 붙어서 돈다. 그 사이에 다른 스레드가 끼어들 수 있는가?

**생각.** 끼어들 수 있다. 준비된 스레드 중 무엇을 돌릴지는 스케줄러가 정하고(sched(7)), 스레드가 CPU를 떠나는 길은 둘이다. **막히는**(block) 것은 I/O나 락이나 sleep을 기다리며 CPU를 스스로 내주는 것이다. **선점되는**(preempt) 것은 타임 슬라이스가 끝났거나 우선순위가 더 높은 스레드가 깨어나서, 어디에 있든 그 자리에서 멈춰졌다가 나중에 아무 일도 없었던 듯 다시 이어지는 것이다. 코어가 여럿인 기계에는 셋째 길도 있다. 두 스레드가 그냥 같은 순간에 돈다.

**규칙, Python의 경우.** Python은 각 줄을 먼저 **바이트코드**(bytecode), 곧 인터프리터가 실제로 실행하는 작은 명령들로 컴파일한다. 그래서 전역 인터프리터 락(§8)이 있는 표준 CPython에서 쪼갤 수 없는 단위는 줄이 아니라 바이트코드 명령 하나다. 인터프리터는 명령과 명령 사이에서만 스레드를 바꾸고, 명령 하나는 프로그램이 보기에 원자적이다(Python FAQ, "What kinds of global value mutation are thread-safe?").

**숫자로.** P6 카운터의 갱신은 한 줄이지만 명령은 넷이다. 영어 절의 `dis` 출력, 곧 이 기계의 Python 3.12.4가 `n_cb += 1`을 풀어 놓은 것이 `LOAD_NAME`, `LOAD_CONST`, `BINARY_OP`, `STORE_NAME`이다(그 줄의 명령 넷만 남기고 잘랐고, 다른 버전은 번호와 이름이 다르다). 요리법처럼 읽으면 된다. 카운터를 가져오고, 1을 가져오고, 더하고, 저장한다. 앞의 세 명령 뒤 어디에서든 전환이 허락되므로, 이 스레드가 새 값을 저장하기 전에 다른 스레드가 옛 카운터를 읽을 수 있다. 그것이 §3의 잃어버린 갱신의 전부다.

**함정.** "한 줄은 한 단계"라는 믿음. FAQ가 그대로 말한다. `i = i+1`은 원자적이지 않고, 내장 타입에 대한 단일 연산 — `L.append(x)`, `x = y`, `x.field = y` — 은 원자적이다. 어느 줄이 안전한지는 인터프리터에 대한 사실이지 소스에서 눈으로 볼 수 있는 것이 아니다.

> [!note]- 더 깊이 · Deeper
> **우선순위.** Linux는 보통 스레드를 시분할 정책 `SCHED_OTHER`로 돌리고, 정적 우선순위 1(낮음)–99(높음)로 모든 보통 스레드보다 먼저 도는 실시간 정책 둘을 준다. 타임 슬라이스가 없는 `SCHED_FIFO`와, 차례마다 최대 퀀텀이 있는 `SCHED_RR`다. 기본값으로 CPU 시간의 5%는 실시간이 아닌 프로세스 몫으로 남고(`sched_rt_runtime_us`가 1,000,000 µs마다 950,000), Linux 6.12부터는 커널의 실시간 선점(PREEMPT_RT)을 패치 없이 켤 수 있다(sched(7)). 200 Hz 제어 스레드는 실시간 우선순위의 자연스러운 후보인데, 그러면 우선순위가 낮은 스레드와 함께 쓰는 락이 우선순위 역전을 부른다. 그 정의와 치료법은 [[02-foundations/algorithms/interview-code|11.7 §6]]에 있다. 이 규칙의 C++ 쪽은 [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code §9]]이고, 어떤 ROS 2 콜백이 스레드를 함께 쓰는지는 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]이다.

### 3. 경쟁 상태: 잃어버린 갱신과 찢어진 읽기, 세어 보기

*한 문장으로:* 두 스레드가 같은 데이터를 만지고 그중 하나가 쓰면 결과는 단계들이 끼어드는 순서에 달려 있고, 작은 경우에는 그 순서를 모두 적어 셀 수 있다.

**풀려는 문제.** P6의 상태 점검은 초당 콜백 250번을 기대하는데, 가끔 그보다 적게 센다. 아무것도 죽지 않았고, 로그에는 아무것도 없다.

**생각을 따라가 보기.** 두 콜백 모두 `n_cb += 1`을 돈다. 읽고, 읽은 값에 1을 더해 저장한다. 네 단계가 이렇게 떨어질 수 있다:

| 단계 | 스레드 | 하는 일 | 메모리의 `n_cb` | 레지스터 |
|---:|---|---|---:|---|
| 1 | A (`on_goal`) | 읽기 | 100 | A가 100을 들고 있음 |
| 2 | B (틱) | 읽기 | 100 | A 100, B 100 |
| 3 | A | A + 1 저장 | 101 | |
| 4 | B | B + 1 저장 | 101 | |

두 스레드 모두 제 일을 바르게 했는데 메모리에는 증가가 하나만 남았다. A가 저장하기 전에 B가 읽어 두었으므로 B의 저장이 A의 저장을 덮어쓴 것이다. 이것이 **잃어버린 갱신**(lost update)이다. 목표에도 같은 일이 생긴다. `on_goal`은 $p$ 다음 $s$를 저장하고 틱은 $p$ 다음 $s$를 읽는데, 틱의 두 읽기가 두 저장 사이에 떨어지면 새 위치와 옛 스탬프를 받는다. 아무도 쓴 적 없는 쌍, **찢어진 읽기**(torn read)다. 이 네 단계의 여섯 순서 전부(실습 1b부):

| 순서 (A = `on_goal`, B = 틱) | 틱이 읽는 값 | |
|---|---|---|
| AABB | (0.510 m, 1020 ms) | 새 값, 일관 |
| ABAB | (0.510 m, 1020 ms) | 새 값, 일관 |
| ABBA | (0.510 m, 1000 ms) | **찢어짐**: 새 위치, 옛 스탬프 |
| BAAB | (0.500 m, 1020 ms) | **찢어짐**: 옛 위치, 새 스탬프 |
| BABA | (0.500 m, 1000 ms) | 옛 값, 일관 |
| BBAA | (0.500 m, 1000 ms) | 옛 값, 일관 |

옛 목표를 읽는 것은 해가 없다. 스탬프가 20 ms 더 오래되었다고 정직하게 말해 주기 때문이다. 섞인 것은 다르다. 스탬프가 함께 다니는 위치의 나이를 틀리게 말한다(그 값은 계산 절이 매긴다).

**규칙.** "타이밍에 달렸다"를 셀 수 있는 것으로 바꿔 주는 정의가 둘 있다.

> **인터리빙의 정의.** **인터리빙**(interleaving)은 *여러 스레드의 원자적 단계 전부를, 스레드마다의 순서는 지키면서 한 줄로 세운 것*이다. 프로그램이 겪을 수 있는 역사 하나이지 확률이 아니다. 조건 셋. 단계는 **원자적**이다(읽기 하나, 쓰기 하나, 바이트코드 명령 하나, 또는 락 아래의 임계 구역 하나 통째, §4). **스레드마다의 순서가 지켜진다**. 그리고 **모든 단계가 정확히 한 번** 나온다.
>
> $$I(m_A,m_B)=\binom{m_A+m_B}{m_A}$$
>
> $m_A$와 $m_B$는 두 스레드의 단계 수다. $m_A+m_B$개 자리 가운데 스레드 A의 단계가 어느 자리를 차지할지 고르면 인터리빙이 정해지기 때문이다. B의 단계는 남은 자리를 순서대로 채운다.
>
> - **예**: 쓰기 둘 대 읽기 둘, $I(2,2)=\binom{4}{2}=6$. 위 표의 여섯 줄이고 그중 둘이 찢어진다. 카운터 단계까지 더해 각각 넷이면 $I(4,4)=70$이다.
> - **비예**: 여섯 가지가 똑같이 일어난다고 보는 것. 이 수는 무엇이 *가능한지*를 말한다. 이 기계에서 평범한 쓰기 둘로 쓴 목표는 229만 번 읽는 동안 한 번도 찢어져 읽히지 않았지만(§8), 나열은 그럴 수 있다는 것을 보여 준다.
> - **왜 중요한가**: 동시 프로그램은 모든 인터리빙이 받아들일 만한 결과를 낼 때만 옳고, 작은 경우에는 그것을 모두 적어 봄으로써 증명하거나 반박할 수 있다.

> **경쟁 상태의 정의.** **경쟁 상태**(race condition)는 *결과가 스레드 단계들의 상대적 시점이나 순서에 따라 달라지는 프로그램의 성질*이다(Python 용어집). 어느 실행에서 드러나든 말든 코드에 있는 결함이다. 조건 넷. **공유 데이터**, **적어도 하나의 쓰기**, 충돌하는 접근들 사이에 **강제된 순서가 없음**(락도, 메시지도, join도 없음), 그리고 그로 인해 생기는 인터리빙들 사이에서 **결과가 다름**. **데이터 경쟁**(data race), 곧 메모리 위치 하나에 대한 동기화되지 않은 충돌 접근은 C++에서 정의되지 않은 동작이다([intro.races]).
>
> $$\text{race}\iff\exists\,\sigma_1,\sigma_2\in\Sigma:\ \text{out}(\sigma_1)\neq\text{out}(\sigma_2)$$
>
> $\Sigma$는 가능한 인터리빙의 집합, $\text{out}(\sigma)$는 $\sigma$의 관측 가능한 결과다. 그러므로 결과가 다른 인터리빙 둘만 찾으면 경쟁 상태가 증명된다.
>
> - **예**: 카운터. 증가를 하나씩 하는 여섯 순서 중 넷은 101, 둘은 102로 끝나므로, 오늘 실행이 무엇을 잃었든 이 프로그램에는 경쟁 상태가 있다.
> - **비예**: 같은 콜백들을 ROS 2의 기본값인 상호 배타 콜백 그룹 하나에 둔 경우([[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]). 둘은 결코 겹치지 않으므로 콜백 통째의 순서 둘만 남고, 둘 다 102로 끝난다.
> - **왜 중요한가**: 나쁜 인터리빙은 실제로는 드물어도 가능할 수 있으므로 경쟁 상태는 테스트를 통과해 버린다. 없애는 길은 순서를 강제하는 것뿐이다(§4–§6).

**숫자로: 증가가 많을수록 옳은 답은 적다**(실습 1a부):

| 스레드마다 증가 $k$개 | 인터리빙 $\binom{4k}{2k}$ | 가능한 최종값 | 옳은 것($2k$) | 옳은 비율 |
|---:|---:|---|---:|---:|
| 1 | 6 | 1–2 | 2 | 33.33% |
| 2 | 70 | 2–4 | 6 | 8.57% |
| 3 | 924 | 2–6 | 20 | 2.16% |
| 4 | 12,870 | 2–8 | 70 | 0.54% |
| 5 | 184,756 | 2–10 | 252 | 0.14% |

옳은 답은 어떤 증가도 쪼개지지 않은 $\binom{2k}{k}$개 순서에서만, 그리고 그 모두에서 나온다. 실습이 확인한다. 게다가 최악의 경우는 일의 양과 함께 커지지 않는다. $k$가 얼마든 가장 작은 결과는 2다. 요리법은 이렇다. A가 0을 읽는다. B가 증가 $k-1$개를 끝낸다. A가 그 모두 위에 1을 저장한다. B가 그 1을 읽는다. A가 나머지 $k-1$개를 끝낸다. B의 마지막 저장이 모든 것 위에 2를 쓴다($k=5$에서 `ABBBBBBBBABAAAAAAAAB`).

**함정: 센 것은 확률이 아니다.** 스레드는 보통 수천 단계를 돌고 나서야 바뀌므로, 실제 실행이 만드는 순서는 대부분 쪼개지지 않은 것이고, 그래서 경쟁 상태는 테스트를 통과한다. 이 기계에서 맨 `n_cb += 1` 반복은 5 × 2,000,000번 동안 갱신을 하나도 잃지 않았지만, 읽기와 쓰기 사이에 함수 호출 하나를 둔 것은 27–33%를 잃었다(§8). 결과가 인터리빙에 달려 있으면 [[06-research-practice/experimental-design-reproducibility|연구 실무 2 §6]]의 뜻으로 실행이 반복 가능하지도 않다.

### 4. 락과 임계 구역

*한 문장으로:* 락은 같은 락을 잡는 모든 스레드에게 임계 구역을 한 단계처럼 보이게 해서 경쟁 상태를 없애고, 그 대가로 기다림을 치르게 한다.

**풀려는 문제.** §3의 두 버그는 모두 다른 스레드가 쪼갤 수 있는 두 단계짜리 갱신에서 나온다. `on_goal`의 두 저장과 틱의 두 읽기가 각각 한 번에 일어나게 하고 싶다.

**생각.** 락은 통행증이다. 통행증을 쥔 스레드만 지켜지는 코드에 들어갈 수 있고, 들어가려는 다른 스레드는 문 앞에서 기다린다. `threading.Lock`은 잠김 아니면 풀림이다. `acquire()`는 풀릴 때까지 기다렸다가 잠그고, `release()`는 풀어서 기다리던 스레드 하나를 들여보내며, `with lock:`은 블록이 예외를 던져도 둘을 다 해 준다(`threading` 문서). 영어 절의 코드가 P6의 목표 둘레에 이것을 두른 모습이고, 스레드 하나로 돌려서 출력이 결정적이다. 틱은 `(0.51, 1020)`을 읽고, 풀린 락은 곧바로 잡히고(`True`), 같은 스레드가 한 번 더 잡으려 하면 10 ms 뒤에 포기하며(`False`), `RLock`은 두 번 다 잡힌다(`True True`).

마지막 줄들이 물리는 성질을 보여 준다. `Lock`은 재진입이 되지 않으므로 두 번 잡는 스레드는 자기 자신을 기다린다. 타임아웃이 없으면 영원히. `threading.RLock`은 쥔 스레드가 다시 잡을 수 있다.

> **락의 정의.** **락**(lock, 뮤텍스)은 *한 번에 많아야 스레드 하나가 쥐는 동기화 객체*다. 그것을 쓰는 스레드들 사이의 약속이지 데이터의 성질이 아니다. 조건 셋. **acquire**는 락이 풀릴 때까지 기다렸다가 잡는다. **release**는 기다리던 스레드 하나에게 락을 넘긴다. 그리고 **지켜지는 데이터에 대한 모든 접근은 바로 그 락을 쥔 채 일어난다**. 그 사이의 코드가 **임계 구역**(critical section)이고, 락 없는 접근이 하나만 있어도 보장은 사라진다.
>
> $$\sum_i h_i(t)\le1,\qquad w_A\le c_B$$
>
> $h_i(t)$는 스레드 $i$가 락을 쥔 동안 1이고, $w_A$는 스레드 A가 락을 잡으려고 기다리는 시간, $c_B$는 다른 스레드 B의 가장 긴 임계 구역이다. 그러므로 임계 구역은 결코 겹치지 않고, 스레드가 둘이면 한 번 잡을 때 기다리는 것은 많아야 상대의 임계 구역 하나다.
>
> - **예**: `on_goal`과 틱이 두 필드 접근을 각각 `goal_lock`으로 두른다. 임계 구역이 한 단계가 되었으므로 §3의 여섯 순서는 $I(1,1)=2$로 줄고, 틱은 $(0.500\,\mathrm{m},\,1000\,\mathrm{ms})$ 아니면 $(0.510\,\mathrm{m},\,1020\,\mathrm{ms})$를 읽을 뿐 섞인 것은 읽지 않는다. 증가도 락 아래에 두면 $k=5$에서 순서 $\binom{10}{5}=252$개가 모두 10으로 끝난다.
> - **비예**: `on_goal`만 잡는 락. 틱은 여전히 락 없이 읽으므로, 찢어진 것까지 여섯 순서가 모두 남는다.
> - **왜 중요한가**: 경쟁 상태를 고치는 가장 단순한 방법이고, 그 값은 다른 스레드의 임계 구역이 떠안기는 기다림이 전부다.

**숫자로: 락의 값.** 풀린 락을 잡는 것은 싸다. 이 기계에서 `python3 -m timeit`으로 잰 경합 없는 `with lock: pass`는 두 번 돌려 256 ns와 291 ns였고, P6의 5 ms 주기의 약 0.006%다(이 기계의 측정값). 비싼 것은 기다림이고, $w_A\le c_B$가 말하듯 기다림은 상대 임계 구역의 길이만큼이다. 그래서 디스크에 쓰는 동안 `log_lock`을 쥐는 기록 스레드는 300 ms 정지 내내 그것을 쥐게 되고, 같은 락을 잡는 틱은 300 ms를 기다린다. $300/5=60$틱, $300/70=4.3$예산이다. 가득 찬 버퍼를 빈 버퍼와 바꾸는 동안만 락을 쥐고, 쓰기는 락 밖에서 한다.

**함정: 락이 고치지 못하는 것.**
- *락을 건너뛰는 접근.* 위의 비예다.
- *두 임계 구역으로 나뉜 확인과 행동.* `if not q.full(): q.put(x)`는 그래도 막힐 수 있다. 그 사이에 다른 스레드가 큐를 채울 수 있기 때문이다. `queue` 문서도 `qsize() < maxsize`가 `put()`이 막히지 않음을 보장하지 않는다고 경고한다. 막히지 않는 호출을 쓰고 그 실패를 처리한다(§6).
- *교착과 우선순위 역전.* 락이 만들어 내는 것들이다. §5와 [[02-foundations/algorithms/interview-code|11.7 §6]].

**락 없이: 대입 한 번.** 어떤 갱신은 쪼갤 수 없는 연산 하나로 주어진다. C++의 `std::atomic<T>::fetch_add`는 더하기와 옛 값 돌려주기를 한 단계로 한다(cppreference). Python에는 원자적 정수가 없지만 FAQ의 단일 연산들은 GIL — CPython의 인터프리터 락, §8 — 아래에서 원자적이고, 그것이 찢어진 읽기를 락 없이 고치는 길을 준다. `on_goal`이 목표를 불변 튜플 하나로 만들어 대입 한 번, `self.goal = (p, s)`로 공개하면, 읽는 쪽은 옛 튜플 아니면 새 튜플을 받을 뿐 반반은 받지 않는다. [[04-robotics/ros2/executors-callbacks-time|25.5.1]]이 권하는 대입 한 번으로 넘기기다.

### 5. 교착과 락 순서

*한 문장으로:* 락 두 개를 서로 반대 순서로 잡는 두 스레드는 저마다 하나를 쥔 채 다른 하나를 영원히 기다리게 될 수 있고, 전체에 하나뿐인 락 순서가 그것을 불가능하게 만든다.

**풀려는 문제.** 목표와 로그를 각각 락으로 지키자, 노드가 가끔 얼어붙는다. 명령도 로그 줄도 없는데 프로세스는 목록에 그대로 있다.

**생각을 따라가 보기.** 틱은 목표를 읽으려 `goal_lock`을 잡고, 그것을 쥔 채 읽은 것을 로그에 남기려 `log_lock`을 잡는다. 로그 기록 스레드는 버퍼를 바꾸려 `log_lock`을 잡고, 그것을 쥔 채 상태 줄에 현재 목표를 넣으려 `goal_lock`을 잡는다. 운 나쁜 순서 하나:

1. 틱이 `goal_lock`을 잡는다. 풀려 있었다.
2. 기록 스레드가 `log_lock`을 잡는다. 풀려 있었다.
3. 틱이 `log_lock`을 청한다. 기록 스레드가 쥐고 있으니 기다린다.
4. 기록 스레드가 `goal_lock`을 청한다. 틱이 쥐고 있으니 기다린다.

둘 다 상대의 락을 얻은 뒤에야 자기 락을 풀 텐데, 그런 일은 끝내 오지 않는다(그림 b). 실습은 락이 풀려 있을 때만 acquire를 허락하며 모든 스케줄을 탐색한다:

| 로그 기록 스레드가 락을 잡는 방식 | 스케줄 | 끝남 | 교착 |
|---|---:|---:|---:|
| 틱과 반대 순서로 | 6 | 4 | 2 |
| 틱과 같은 순서로 | 2 | 2 | 0 |
| 한 번에 하나씩, 둘을 함께 쥐지 않고 | 7 | 7 | 0 |

> **교착의 정의.** **교착**(deadlock)은 *한 무리의 스레드가 저마다 그 무리의 다른 스레드만이 줄 수 있는 것을 기다려서 아무도 나아가지 못하는 상태*다(Python 용어집). 어떤 인터리빙은 이르고 어떤 인터리빙은 이르지 않는 상태이지 느려짐이 아니다. 조건 넷, 모두 필요조건이므로 하나만 없애도 막힌다. **상호 배제**(락마다 쥔 쪽 하나), **점유와 대기**(락 하나를 쥔 채 다른 락을 기다림), **비선점**(락을 빼앗을 수 없음), **순환 대기**(기다림이 고리를 이룸).
>
> $$T_1\to L_a\to T_2\to L_b\to T_1,\qquad r(L_a)<r(L_b)<r(L_a)\ \text{is impossible}$$
>
> 스레드에서 락으로 가는 화살표는 *기다림*, 락에서 스레드로 가는 화살표는 *쥔 쪽*이고, $r$은 락의 순위다. 모든 스레드가 순위가 오르는 쪽으로만 잡으면, 고리를 이루려면 한 바퀴 내내 각 순위가 앞의 것보다 커야 하므로 고리는 — 그러므로 교착도 — 생길 수 없다.
>
> - **예**: 틱 → `log_lock` → 기록 스레드 → `goal_lock` → 틱. 스케줄 6개 중 2개가 이른다. `goal_lock`을 1순위로 두고 두 스레드가 모두 그것을 먼저 잡으면 2개 중 0개다.
> - **비예**: `log_lock`을 쥔 기록 스레드가 디스크 정지에 갇힌 동안 틱이 그 락을 300 ms 기다리는 것. 기록 스레드가 끝나면 풀어 줄 것이므로 교착이 아니라 막힘이다.
> - **왜 중요한가**: 교착한 노드는 프로세스 목록에 남아 아무것도 기록하지 않는다. 로거가 멈춘 스레드 중 하나이기 때문이다. 그리고 P6의 모터는 마지막 명령을 유지한다. 죽은 노드가 살아 있는 명령을 남길 수 있기 때문이다([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §7]]).

**해법, 조건마다 하나.** 락에 순위를 매기고 오르는 쪽으로만 잡는다. Python 용어집 자신의 권고도 여러 락을 늘 같은 순서로 잡으라는 것이다. 아니면 둘을 함께 쥐지 않는다. 기록 스레드가 `goal_lock` 아래에서 목표를 복사하고, 풀고, 그다음에 `log_lock`을 잡는다(표의 셋째 줄). C++에서는 `std::scoped_lock`이 교착 회피 알고리즘으로 뮤텍스 여럿을 잡는다(§10).

**함정.** 타임아웃 `lock.acquire(timeout=0.01)`은 치료가 아니라 탐지다. 소리 없는 멈춤을 로그에 남길 수 있는 오류로 바꿔 주니 로봇에서는 가질 만하지만, 코드는 여전히 물러났다가 다시 시도해야 한다. 그리고 같은 모양이 락이 하나뿐인 곳에도 숨어 있다. 콜백 안에서 서비스를 동기 호출할 때의 ROS 2 교착은, 콜백이 자기 상호 배타 그룹을 쥔 채 그 그룹만이 전해 줄 수 있는 결과를 기다리는 것이다([[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]).

### 6. 스레드 사이의 큐: 생산자, 소비자, 유한 버퍼

*한 문장으로:* 데이터를 락 아래에서 함께 쓰는 대신, 스스로 잠금을 처리하는 큐로 생산자가 소비자에게 항목을 넘길 수 있다. 생산자가 더 빠르면 무엇이 깨질지는 용량과 찬 큐에 대한 정책이 정한다.

**풀려는 문제.** 제어 틱은 명령을 모두 기록해야 하는데, 5 ms짜리 틱 안에서 디스크에 쓰면 제어기가 디스크를 기다리게 된다.

**생각.** 직접 쓰지 말고 넘긴다. **생산자–소비자**(producer–consumer) 패턴에서는 항목마다 한 번에 주인이 하나다. 틱은 기록을 큐에 넣고 잊어버리고, 기록 스레드가 꺼내서 쓴다. 큐는 칸 수가 정해진 우편함이고, 생산자와 소비자가 몇이든 필요한 잠금은 `queue.Queue`가 알아서 한다(`queue` 문서). 남는 질문은 하나다. 우편함이 가득 차면 어떻게 하는가.

> **유한 버퍼의 정의.** **유한 버퍼**(bounded buffer)는 *생산자 스레드와 소비자 스레드 사이에 놓인, 용량이 정해진 선입선출 큐*다. 자료 구조에 정책을 더한 것이다. 조건 넷. 항목은 **들어온 순서대로** 나간다. 많아야 **$N$개**를 담는다. **찬 버퍼 정책** — 생산자 막기, 가장 새것 버리기, 가장 오래된 것 버리기 — 이 그 일부다("늘리기", 곧 한도가 없으면 유한 버퍼가 아니라 무한 큐다). 그리고 **스스로 잠금을 처리한다**.
>
> $$t_{\text{full}}=\frac{N-q_0}{\lambda-\mu},\qquad n_{\text{over}}=(\lambda-\mu)\,(D-t_{\text{full}})$$
>
> 처음에 $q_0$개가 들어 있고, 길이 $D$인 구간 동안 항목이 $\lambda$로 들어와 $\mu<\lambda$로 나가며, $t_{\text{full}}$은 버퍼가 차는 시각, $n_{\text{over}}$는 찬 버퍼에 도착하는 항목 수다. 버퍼는 찰 때까지 초당 $\lambda-\mu$개씩 늘고, 찬 뒤로는 그 남는 항목 하나하나가 자리를 못 찾아 버려지거나 생산자를 막기 때문이다.
>
> - **예**: 300 ms 정지 속의 P6 로거. $\lambda=200$개/s, $\mu=0$, $N=32$, $q_0=0$이므로 $t_{\text{full}}=0.16\,\mathrm{s}$, $n_{\text{over}}=200\times0.14=28$이다.
> - **비예**: 기본값 `maxsize=0`인 `queue.Queue()`. 문서가 무한이라고 정의한다. "늘리기" 정책이라서, 소비자가 멈춰 있는 동안 내내 메모리가 는다.
> - **왜 중요한가**: 정책은 어떤 실패 — 잃는 기록, 멈추는 생산자, 느는 메모리 — 를 받아들일지 고르는 일이고, 막히는 쪽이 제어 스레드여서는 결코 안 된다.

**Python의 정책들.** 영어 절의 코드는 스레드 하나로, 그래서 결정적으로 보여 준다. 칸 둘짜리 큐에 기록 셋을 `put_nowait`으로 넣으면 셋째(`tick at 15 ms`)가 `queue.Full`로 버려지고 앞의 둘이 남는다. `deque(maxlen=3)`에 5, 10, 15, 20, 25를 넣으면 `[15, 20, 25]`가 남는다. `put_nowait`은 기다리는 대신 `queue.Full`을 던지므로, 그것을 잡으면 가장 새 기록을 버리게 된다. 로거에서 제어 스레드 쪽이 할 일이다. 평범한 `put()`은 자리가 날 때까지 생산자를 막는다. 모든 항목이 중요하고 생산자가 기다려도 될 때, 이를테면 데이터 로더의 워커(§9)에게는 맞는 정책이고, 제어 스레드에게는 결코 아니다. `collections.deque(maxlen=N)`은 반대쪽 끝에서 버려 가장 새 $N$개를 남긴다. 가장 오래된 것 버리기이고, 문서는 그 덧붙이기와 꺼내기가 스레드 안전하다고 말하며, ROS 2 구독의 keep-last 기록과 같은 규칙이다([[04-robotics/ros2/qos-executors-time|25.5 §2]]).

**함정.** 엉뚱한 쪽을 버리는 것. 목표는 가장 새것만 중요하니 가장 오래된 것을 버린다. 로그는 양쪽 다 중요하니 어느 쪽을 버려도 되지만, 버린 개수는 반드시 센다. 그렇지 않으면 로그의 빈틈이 조용히 서 있던 로봇처럼 보인다.

### 대상으로 한 번 끝까지 · Worked case

이 페이지의 대상과 §3–§6으로 P6 노드의 비전 주기 하나를 끝까지 본다. 그림이 이 경우이고 실습(§11)이 모든 숫자를 출력하며, 과제는 여기서 손잡이를 돌린다.

**1단계 — 겹치는 방법을 센다.** `on_goal`은 원자적 단계 넷($p$ 저장, $s$ 저장, `n_cb` 읽기, `n_cb` + 1 저장)을, 틱도 넷($p$ 읽기, $s$ 읽기, `n_cb` 읽기, `n_cb` + 1 저장)을 돈다. 그래서 둘이 끼어드는 순서는

$$I(4,4)=\binom{8}{4}=\frac{8!}{4!\,4!}=70$$

가지다. 여덟 자리 중 `on_goal`의 단계가 차지할 네 자리로 순서가 정해지기 때문이다. 실습이 70개를 모두 돌린다. 22개는 멀쩡하고, 8개는 목표만 찢고, 28개는 갱신만 잃고, 12개는 둘 다 한다. 찢는 것이 20개, 잃는 것이 40개다. 그림의 ABBAABAB는 둘 다 하는 12개 중 하나다.

**2단계 — 찢어진 읽기의 값.** 찢어진 쌍은 비전 주기 하나만큼 떨어진 두 목표를 섞는다:

$$\Delta a=T_v=20\,\mathrm{ms}=0.29\,B,\qquad \Delta p=v\,T_v=0.5\,\mathrm{m/s}\times0.020\,\mathrm{s}=0.010\,\mathrm{m}=20.5\ \text{counts}$$

연속한 목표는 20 ms 떨어져 있고 대상은 0.5 m/s로 움직이기 때문이다. 위치는 스탬프가 말하는 곳에서 10 mm, 엔코더로 20.5 count 떨어져 있고, 나이는 예산의 29%만큼 틀린다. 방향이 중요하다. $(0.500\,\mathrm{m},\,1020\,\mathrm{ms})$는 더 오래된 위치를 새것으로 속인다. $t=1085\,\mathrm{ms}$에 그것은 85 ms 묵어 예산을 넘었는데 스탬프로는 65 ms이고, 묵음 검사가 받아들인다. $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$는 거꾸로다. $t=1075\,\mathrm{ms}$에 55 ms 된 목표가 75 ms로 보여 버려진다.

**3단계 — 잃어버린 갱신.** 증가를 하나씩 하면 순서 $I(2,2)=6$개 중 4개가 `n_cb`를 102가 아니라 101에 둔다. 상태 점검은 콜백이 겹칠 때만 덜 세므로 드물게, 조용히, 그리고 부하가 클 때 — 곧 점검이 가장 필요할 때 — 가장 자주 그렇다.

**4단계 — 교착.** 틱은 `goal_lock` 다음 `log_lock`, 기록 스레드는 그 반대. 스케줄 6개 중 2개가 교착하고, 그러면 두 스레드가 영영 멈춘다. 명령도 로그 줄도 없이 모터는 마지막 명령에 머문다. 기록 스레드도 `goal_lock`을 먼저 잡으면 2개 중 0개다.

**5단계 — 정지 속의 로그 큐.** 정지 동안 $\mu=0$이므로 빈 32칸 큐는

$$t_{\text{full}}=\frac{N}{\lambda}=\frac{32}{200\,\mathrm{s^{-1}}}=0.160\,\mathrm{s},\qquad n_{\text{over}}=\lambda\,(D-t_{\text{full}})=200\,\mathrm{s^{-1}}\times0.140\,\mathrm{s}=28$$

뒤에 찬다. 디스크가 300 ms에 돌아올 때까지 기록은 계속 오고 하나도 나가지 않기 때문이다. 네 정책(실습 3부):

| 정책 | 잃는 기록 | 제어 스레드 | 큐 최고치 | 다시 비는 시각 |
|---|---:|---|---:|---:|
| 최신 버리기 | 28개 (165–300 ms에 만든 것) | 기다리지 않음 | 32 | 339 ms |
| 가장 오래된 것 버리기 | 28개 (5–140 ms에 만든 것) | 기다리지 않음 | 32 | 339 ms |
| 막기 | 0 | 165–301 ms 동안 `put()`에 갇힘: 136 ms, 틱 27번이 돌지 못함 | 32 | 340 ms |
| 늘리기 | 0 | 기다리지 않음 | 60개, 3,840바이트 | 374 ms |

P6을 깨는 것은 막기다. 모터는 165 ms의 틱부터 305 ms의 틱까지 새 명령을 받지 못한다. 140 ms, 예산의 두 배다. 늘리기는 여기서 3,840바이트이고 디스크가 돌아오지 않는 동안 초당 12.8 kB(시간당 46 MB)이므로, P6의 작은 기록에는 "상한 있는 늘리기"와 "최신 버리기와 버린 수 세기"가 둘 다 괜찮은 선택이다.

**6단계 — 해법, 모두 실습으로 확인.** 양쪽 모두 `goal_lock`을 잡거나 튜플 하나를 대입 한 번으로 공개하면 순서 2개, 둘 다 일관. 증가를 락 아래에 두면 순서 2개, 둘 다 102. 락 순서 하나로 교착 없음. 제어 스레드에는 버린 수를 세는 막히지 않는 put, 기록 스레드는 버퍼를 바꾸는 동안만 `log_lock`을 쥔다.

### 7. 병렬화가 사 주는 것: 암달의 법칙과 데이터 로더 파이프라인

*한 문장으로:* 워커를 더하면 작업 중 나눌 수 있는 부분만 빨라지므로 나머지가 천장을 정하고, 파이프라인은 가장 느린 단계의 속도로 돈다.

**풀려는 문제.** 전처리 작업은 코어 하나로 120 s가 걸린다. 워크스테이션의 코어는 8개다. 15 s가 될까?

**생각을 계산으로.** 120 s를 나눌 수 있는 것과 없는 것으로 쪼갠다. 파일을 읽고 결과를 합치는 일은 나눌 수 없어서 $120\times(1-0.9)=12\,\mathrm{s}$가 그대로 남는다. 윈도마다의 계산은 나눌 수 있어서 $108\,\mathrm{s}$를 코어 8개가 나누면 $13.5\,\mathrm{s}$다. 작업은 $12+13.5=25.5\,\mathrm{s}$가 걸리고, 속도 향상은 8이 아니라 $120/25.5=4.71$이다. 코어가 천 개여도 직렬 12 s보다는 오래 걸린다. **속도 향상**(speedup)은 워커 하나의 시간을 워커 $n$개의 시간으로 나눈 것이고, 직렬 부분이 그 상한을 정한다.

> **암달의 법칙의 정의.** **암달의 법칙**(Amdahl's law)은 *워커 하나일 때의 시간 중 비율 $P$만 워커들에게 나눌 수 있는, 크기가 고정된 작업의 속도 향상에 대한 상한*이다. 상한이지 예측이 아니다. 조건 넷. **문제 크기가 고정**되어 있다(워커와 함께 커지는 문제에는 같은 안내서가 구스타프슨 법칙 $S=N+(1-P)(1-N)$을 준다). 병렬 부분은 **완벽히 나뉜다**. 직렬 부분은 **줄지 않는다**. 그리고 **다른 것이 더해지지 않는다**. 띄우는 비용도, 통신도, 락 기다림도 없다.
>
> $$S(n)=\frac{1}{(1-P)+P/n},\qquad \lim_{n\to\infty}S(n)=\frac{1}{1-P}$$
>
> $n$은 워커 수, $P$는 병렬화할 수 있는 비율이다(NVIDIA CUDA C++ Best Practices Guide §4.1.3.1). 위의 계산을 $T_1$로 나눈 것이므로, 천장은 직렬 비율 하나가 정한다.
>
> - **예**: 전처리 작업. $S(8)=1/(0.1+0.9/8)=4.71$이므로 120 s가 코어 8개에서 25.5 s가 되고, 극한은 $1/0.1=10$이다.
> - **비예**: 아래의 데이터 로더. 그 단계들은 서로 다른 배치를 동시에 처리하므로, 속도는 암달의 식이 아니라 가장 느린 단계의 속도다.
> - **왜 중요한가**: 병렬 코드를 쓰기 전에 얻을 수 있는 최대치를 알려 주고, 모든 워커가 지나가야 하는 임계 구역(§4)은 모두 직렬 부분에 들어간다.

**숫자로**(실습 4부):

| $P$ | $n=1$ | 2 | 4 | 8 | 16 | 64 | 극한 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 1.00 | 1.33 | 1.60 | 1.78 | 1.88 | 1.97 | 2 |
| 0.90 | 1.00 | 1.82 | 3.08 | 4.71 | 6.40 | 8.77 | 10 |
| 0.95 | 1.00 | 1.90 | 3.48 | 5.93 | 9.14 | 15.42 | 20 |
| 0.99 | 1.00 | 1.98 | 3.88 | 7.48 | 13.91 | 39.26 | 100 |

$P=0.9$에서 처음 두 배로 늘리면 1.82배이고, 16개에서 64개로 가면 1.37배가 더해질 뿐이다. 그쯤이면 직렬 10%가 시간의 대부분이기 때문이다.

**함정: 파이프라인은 암달이 아니다.** DataLoader의 단계들은 서로 다른 배치를 동시에 처리한다. 워커 $W$개가 저마다 배치 하나를 40 ms에 읽고, 메인 프로세스가 받는 데 1 ms, GPU가 스텝에 10 ms를 쓴다. 그래서 전체는 가장 느린 단계의 속도로 돈다:

$$R(W)=\min\Big(\frac{W}{t_{\text{load}}},\ \frac{1}{t_{\text{main}}},\ \frac{1}{t_{\text{GPU}}}\Big),\qquad u=R\,t_{\text{GPU}}$$

배치는 한 단계가 만드는 것보다 빨리 그 단계를 떠날 수 없기 때문이다. $R$은 초당 배치 수, $u$는 GPU가 바쁜 비율이다. 워커가 하나면 배치가 40 ms마다 오고 GPU는 그 40 ms 중 10 ms만 일하니 25%만 바쁘다. `num_workers=0`이면 아무것도 겹치지 않아 배치당 51 ms다.

| 워커 $W$ | 0 | 1 | 2 | 3 | 4 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| 초당 배치 | 19.6 | 25.0 | 50.0 | 75.0 | 100.0 | 100.0 |
| GPU 가동률 | 19.6% | 25.0% | 50.0% | 75.0% | 100.0% | 100.0% |

GPU는 $W=\lceil t_{\text{load}}/t_{\text{GPU}}\rceil=\lceil40/10\rceil=4$에서 배가 부르고, 워커를 더 늘리면 기다리기만 한다. 25%만 바쁜 GPU는 프로파일러 시간선에 긴 틈 사이의 짧은 스텝으로 보이고([[03-deep-learning/foundations/gpu-computing|1.4 §7]]), 그 틈이 로더다.

### 8. Python 스레드와 전역 인터프리터 락

*한 문장으로:* 표준 CPython에서는 한 번에 한 스레드만 바이트코드를 돌리므로 스레드는 기다림에는 동시성을 주지만 계산에는 병렬성을 주지 못하고, 코드를 원자적으로 만들어 주지도 않는다.

**풀려는 문제.** 원인이 같은 수수께끼 둘. 스레드 8개로 나눈 Python 전처리가 하나로 돌릴 때보다 빠르지 않다. 그리고 §3의 경쟁하는 카운터는 모든 테스트를 통과한다.

**생각.** CPython은 인터프리터 둘레에 락을 하나 두고 있다. 발언 막대 하나를 떠올리면 된다. 막대를 쥔 스레드만 Python 코드를 돌릴 수 있고, 스레드들이 막대를 돌려 가며 쓴다. I/O를 기다리는 스레드는 막대를 내려놓고, 쥔 스레드는 몇 ms마다 넘기라는 요청을 받는다.

> **전역 인터프리터 락의 정의.** **전역 인터프리터 락**(global interpreter lock, GIL)은 *한 번에 한 스레드만 Python 바이트코드를 실행하도록 CPython이 쓰는 메커니즘*이다(Python 용어집). 언어가 아니라 인터프리터 빌드의 성질이다. 조건 넷. **쥐는 쪽은 하나**이고 그 스레드만 바이트코드를 돌린다. 스레드가 **I/O를 기다리는 동안 풀리며**, 확장 모듈은 긴 계산 동안 풀 수 있다. NumPy는 많은 저수준 연산에서 푼다. 쥔 쪽은 **전환 간격이 지나면 넘기라는 요청을 받는다**. 기본값은 5 ms이고(What's New in Python 3.2가 `sys.getswitchinterval()`이 0.005를 돌려주는 것을 보여 주며, 이 기계에서도 그렇다), 전환은 바이트코드 명령 사이에서만 일어난다. 그리고 **선택적**이다. 자유 스레드 빌드는 그것 없이 돈다.
>
> $$N_{\text{bc}}(t)\le1\ \ \text{per interpreter},\qquad S_{\text{Python}}(n)\le1$$
>
> $N_{\text{bc}}(t)$는 시각 $t$에 바이트코드를 돌리는 스레드 수, $S_{\text{Python}}(n)$은 순수 Python 계산에서 스레드 $n$개의 속도 향상이다. 그러므로 스레드들은 기다림은 겹칠 수 있어도 Python 계산은 결코 겹치지 못한다.
>
> - **예**: Python으로 쓴 P6의 노드. `on_goal`과 틱은 끼어들지만 같은 순간에 Python을 돌리지는 않고, 순수 Python으로 계산하는 콜백은 틱이 돌려 할 때마다 전환 간격 하나, 5 ms — 제어 주기 하나 전체 — 쯤 틱을 늦출 수 있다.
> - **비예**: GIL을 내 코드를 두르는 락으로 보는 것. GIL은 줄이 아니라 바이트코드 명령 하나하나를 원자적으로 만들 뿐이고, FAQ는 `i = i+1`을 원자적이지 않은 것으로 든다.
> - **왜 중요한가**: 도구를 정해 준다. 기다림에는 스레드, 계산에는 프로세스(§9).

**숫자로: GIL이 숨기는 것, 측정.** 가능한 경쟁 상태가 어느 실행에서 드러나는지는 인터프리터가 어디서 전환하느냐에 달려 있다. 영어 절의 스크립트는 실제 스레드 둘을 돌리므로 그 수가 타이밍에 달려 있고, 그래서 CI 밖에 둔다. 이 페이지를 쓴 기계(Python 3.12.4, Apple silicon의 macOS)에서의 결과:

| 실험, 스레드 둘, 각각 약 1초 | 이 기계의 결과 |
|---|---|
| `n_cb += 1`, 스레드마다 1,000,000번, 5회 | 잃은 갱신 없음 |
| 읽기, 함수 호출, 쓰기, 스레드마다 1,000,000번, 5회 | 2,000,000번 중 27–33% 잃음 |
| 목표를 평범한 속성 쓰기 둘로, 3회 | 2,289,508번 읽기 중 찢어짐 0 |
| 목표를 메시지의 속성 둘에서 읽어 쓰기, 3회 | 읽기의 13.9–26.5%가 찢어짐 |
| 목표를 튜플 하나로 공개, 3회 | 2,909,545번 읽기 중 찢어짐 0 |

맨 증가와 평범한 쓰기가 한 번도 틀리지 않은 것은, 이 인터프리터에서는 마침 그 명령들 사이에 전환이 떨어지지 않았기 때문이다. 그 사이에 호출 — 도우미 함수든, 생성된 메시지 클래스가 쓰는 종류의 속성 getter든 — 을 하나 넣으면 같은 경쟁 상태가 곧바로, 증가의 3분의 1까지 나타난다. 소스에는 그 차이가 드러나지 않고, 다른 인터프리터 버전은 다른 곳에서 전환할 수 있다. 구조적으로 안전한 것은 마지막 줄 하나다. FAQ가 원자적이라고 적는 참조 대입 하나.

**함정: GIL은 사라지고 있고, 경쟁 상태는 남는다.** Python 3.13부터 CPython은 GIL 없이 빌드할 수 있고, 3.14에서 이 자유 스레드 빌드가 공식 지원되었다(PEP 779). 기본값은 아니다. 거기서는 스레드가 정말로 병렬로 Python을 돌리므로 §3의 모든 경쟁 상태가 문제를 일으킬 수 있고, 그 문서는 내장 타입의 내부 락에 기대지 말고 `threading.Lock`을 쓰라고 권한다. 구조적으로 안전한 코드 — 락, 대입 한 번, 큐 — 는 그대로 안전하다.

**스레드가 맞는 도구일 때.** `threading` 문서의 권고다. I/O에 묶인 일에는 스레드, 멀티코어 계산에는 `multiprocessing`이나 `concurrent.futures.ProcessPoolExecutor`. NumPy는 예외 하나를 더한다. GIL을 푸는 NumPy 저수준 코드 안에서 대부분의 시간을 보내는 스레드들은 병렬로 돈다. 스레드마다 자기 배열을 가질 때 가장 좋다. 두 스레드가 한 배열을 함께 읽고 쓰면, NumPy의 말로 일관성 없는 결과를 얻는다. Python으로 쓴 ROS 2 노드도 GIL을 만난다. rclpy executor의 스레드들이 그것을 함께 쓴다([[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]).

> [!note]- 더 깊이 · Deeper
> **자유 스레드 빌드 안쪽.** `sys._is_gil_enabled()`(3.13+)가 GIL이 켜져 있는지 알려 주고, 공식 macOS와 Windows 설치 프로그램이 이 빌드를 선택 사항으로 준다. `dict`, `list`, `set` 같은 내장 타입은 내부 락으로 자신을 지키는데, 자유 스레드 HOWTO는 이것을 보장이 아니라 현재 구현의 묘사라고 부른다. 단일 스레드 코드는 조금 느려진다. HOWTO는 pyperformance에서 macOS aarch64의 약 1%부터 x86-64 Linux의 8%까지를 재고, What's New in Python 3.14는 대략 5–10%라고 말한다. 자유 스레드를 지원한다고 표시하지 않은 확장을 import하면 경고와 함께 GIL이 다시 켜질 수 있다. NumPy는 2.1부터 실험적으로 지원한다.

### 9. Python 프로세스, asyncio, DataLoader의 워커

*한 문장으로:* 프로세스는 띄우는 비용과 사본을 치르고 GIL을 비켜 가고, asyncio는 `await`에서만 바꿔 가며 기다리는 태스크 여럿을 스레드 하나에서 돌리며, PyTorch DataLoader는 유한 큐 뒤에 선 워커 프로세스의 풀이다.

**풀려는 문제.** P6의 로그로 학습하려면 배치를 병렬로 풀고 증강해야 하는데, §8은 Python 스레드로는 그럴 수 없다고 말한다.

**생각.** 프로세스를 쓴다. 프로세스마다 자기 인터프리터, 그러니 자기 GIL을 갖는다. `multiprocessing`은 하위 프로세스로 GIL을 비켜 가고, `concurrent.futures.ProcessPoolExecutor`는 그 풀을 호출 하나 뒤에 둔다. 함수와 인자는 pickle되어 워커에게 건너간다. 프로세스를 띄우는 스크립트에는 규칙이 둘 있다. 진입점을 `if __name__ == "__main__":`으로 감싼다([[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python §8]]의 스크립트 구조). 이 패키지는 자식 프로세스가 `__main__` 모듈을 import할 수 있어야 하고, macOS와 Windows, 그리고 Python 3.14부터 Linux의 기본값인 `spawn`·`forkserver` 시작 방식에 대한 문서의 프로그래밍 지침이 이 보호 장치를 요구하기 때문이다. 그리고 pickle할 수 있는 것만 넘긴다.

> [!note]- 더 깊이 · Deeper
> **시작 방식**(`multiprocessing` 문서). `spawn`은 새 인터프리터를 띄우고 Windows와 macOS의 기본값이다. `fork`는 `os.fork()` 순간의 부모를 복사한다. Python 3.14부터 어느 플랫폼의 기본값도 아니고, 3.12부터는 다른 스레드가 있다고 아는 프로세스를 fork할 때 경고한다. `forkserver`는 일찍 띄운 단일 스레드 서버에서 fork하고, 3.14부터 macOS를 뺀 POSIX 플랫폼, 곧 Linux 등의 기본값이다. `fork`의 문제는 §4의 락이다. 자식에는 fork를 부른 스레드 하나만 있지만 뮤텍스 상태까지 포함한 주소 공간 전체를 물려받으므로, 그 순간 다른 스레드가 쥐고 있던 락은 자식에서 영원히 잠긴 채 남고, 자식은 `exec`을 부를 때까지 async-signal-safe 함수만 부를 수 있다(fork(2)).

**DataLoader, 규칙과 숫자.** PyTorch 문서도 같은 곳에서 출발한다. 한 프로세스 안에서 GIL은 스레드들에 걸친 진정한 병렬 Python을 막으므로, `num_workers` > 0인 `DataLoader`는 반복자를 만들 때마다 그만큼의 워커 프로세스를 띄우고, 각각에 데이터셋, `collate_fn`, `worker_init_fn`을 넘긴다. 워커마다 `prefetch_factor`개 배치를 미리 읽는데 기본값이 2이므로, 학습 루프보다 많아야 $2\times$ `num_workers`개 배치를 앞서 읽는다. §6의 뜻으로 유한 버퍼이고, 붙잡히는 쪽은 학습 루프가 아니라 워커들이다. $W=4$인 P6의 로더라면 8개다. `persistent_workers=True`는 워커를 에포크 사이에도 살려 두어 띄우는 비용(§1)을 한 번만 치르게 한다.

**함정.** 프로세스와 함께 둘이 온다.
- **메모리.** 부모의 Python 객체 — 이를테면 파일 이름 백만 개의 리스트 — 를 읽는 워커들은 그것에 대해 부모만큼의 메모리를 쥐게 된다. 문서의 경고로는 전체 사용량이 워커 수 곱하기 부모 프로세스 크기다. 우회책은 참조 카운트가 없는 저장, 곧 NumPy, pandas, PyArrow 객체다. §1의 $c=1+W$다.
- **무작위성.** 워커마다 PyTorch 시드는 `base_seed + worker_id`이지만 다른 라이브러리의 시드는 중복될 수 있어서, 모든 워커가 같은 "무작위" 수를 돌려준다. 문서의 해법은 `get_worker_info().seed`로 그것들을 시딩하는 `worker_init_fn`이다.

두 번째 함정을 이 페이지를 쓴 기계에서 PyTorch 2.6.0으로 돌렸다(CI에는 PyTorch가 없으므로 CI 밖에서). 영어 절의 출력에서, `worker_init_fn`이 없으면 윈도 0과 2가 같은 잡음(0.1257)을 받고, 1과 3(−0.1321), 4와 6(0.6404), 5와 7(0.1049)도 그렇다. 워커마다 데이터셋의 사본을, 그러니 같은 상태의 같은 생성기 사본을 들고 있기 때문이다. 증강의 절반이 중복인데 아무것도 실패하지 않는다. `reseed`를 주면 여덟 값이 모두 다르다. 실습(5부)은 그 메커니즘을 NumPy만으로 보여 주고, 워커들에게 독립 스트림을 주는 NumPy의 문서화된 방법 `SeedSequence(seed).spawn(n)`도 함께 보여 준다. 기본 시드 하나에서 시딩한 실행은 반복 가능하다([[06-research-practice/experimental-design-reproducibility|연구 실무 2 §6]]). 중복된 스트림도 실행을 반복 가능하게 둔다. 틀린 채로.

**asyncio, 한 문단으로.** 계산이 아니라 기다림이 많을 때 — 네트워크 클라이언트, 로봇의 명령 링크, 대시보드 — `asyncio`는 `async`/`await`로 쓴 동시 코드를 스레드 하나에서 돌린다. 이벤트 루프가 모든 태스크를 돌리고, 도는 태스크는 `await`에 닿을 때까지 스레드를 쥐며, 거기서 멈추면 다음 태스크가 돈다(asyncio 개발 안내). 그래서 두 `await` 사이의 코드는 방해받지 않고 돌아 그 안에서는 찢어진 읽기가 생기지 않지만, 막히는 호출 하나가 모든 것을 멈춘다. 1 s 동안 계산하는 함수는 모든 태스크를 1 s 늦춘다. 막히는 일을 `loop.run_in_executor`로 보내는 이유다.

### 10. C++ 스레드와 ROS 2 콜백 그룹

*한 문장으로:* C++는 인터프리터 락 없는 진짜 병렬 스레드를 주므로 §3의 경쟁 상태가 정의되지 않은 동작의 데이터 경쟁이 되고, ROS 2 노드의 콜백 그룹은 §4의 상호 배제를 콜백 통째에 적용한 것이다.

**풀려는 문제.** P6의 제어기는 ROS 2 executor 아래의 C++ 노드로도 돈다. 거기서는 §3–§6이 다르게 보인다. 경쟁 상태를 가려 줄 인터프리터 락이 없고, 어느 콜백이 스레드를 함께 쓸지는 여러분이 아니라 executor가 정한다.

**C++, 한 문단으로.** `std::thread`(C++11)는 만들어지는 순간 돌기 시작하고, 소멸하기 전에 join하거나 detach해야 한다. 아니면 프로그램이 끝난다. `std::mutex`는 공유 데이터를 지킨다. 이미 가진 뮤텍스를 다시 잠그면 정의되지 않은 동작, 대개 교착이다. 보통 `std::lock_guard`나, 교착 회피 알고리즘으로 뮤텍스 여럿을 잠그는 `std::scoped_lock`(C++17)으로 쥔다(cppreference). 메모리 위치 하나에 대한 충돌 접근 둘이 둘 다 원자적이지도 않고 동기화로 순서가 정해지지도 않으면 데이터 경쟁이고, 그런 프로그램의 동작은 정의되지 않는다([intro.races]). 갱신 하나를 잃는 정도가 아니라 무엇이든 일어날 수 있다. Clang의 ThreadSanitizer는 `-fsanitize=thread`로 실행 중에 데이터 경쟁을 찾고, 대가로 5–15배 느려진다. C++ 노드가 50 Hz 콜백에서 200 Hz 틱으로 P6의 목표를 `std::atomic` 하나로 넘기는 법은, 실시간 틱의 규칙과 함께 [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code §9]]에 있다.

**ROS 2, 지도로.**

| 이 페이지 | ROS 2 노드에서 | 가르치는 곳 |
|---|---|---|
| 스레드(§1) | 멀티스레드 executor의 스레드들 | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §1]] |
| 락(§4) | 상호 배타 콜백 그룹, 기본값이 이것 | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §2]] |
| GIL(§8) | rclpy executor의 스레드들이 함께 씀 | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §1]] |
| 교착(§5) | 응답해야 할 그룹의 콜백 안에서 하는 동기 서비스 호출 | [[04-robotics/ros2/executors-callbacks-time\|25.5.1 §2]] |
| 가장 오래된 것을 버리는 유한 버퍼(§6) | 깊이 $N$인 구독의 keep-last 기록 | [[04-robotics/ros2/qos-executors-time\|25.5 §2]] |

그러니 P6의 목표와 카운터는 `on_goal`과 틱이 상호 배타 그룹 하나를 함께 쓰는 동안은 안전하고, 병렬로 돌리려고 둘을 다른 그룹으로 나누는 순간 위험해진다. 이 페이지 대상의 배치가 바로 그것이고, 그래서 §4의 해법이 필요하다.

### 11. 실습: 인터리빙, 교착 탐색, 로그 큐, 암달의 법칙

고정된 대상 위의 다섯 부분이다. 결정적이고 스레드도 시간 측정도 없으므로 어느 기계에서나 같은 것을 출력한다. 영어 절의 코드가 그것이다. (1) $k=1$–5 카운터, 찢어진 읽기, 그림의 스케줄, 그리고 락을 둔 같은 것들의 인터리빙, (2) 락 규율 셋에서 틱과 기록 스레드의 모든 스케줄, (3) 1 ms 단위로 네 정책 아래 모의한 로그 큐와 용량·정지 길이 훑기, (4) 암달의 표, 전처리 작업, 로더 파이프라인, (5) 복사된 난수 생성기가 서로를 되풀이하는 이유.

**출력 읽기.** 1–4부는 §3–§7의 표와 계산 절이다. 3부 둘째 블록, 막기 정책에서 제어 스레드가 갇히는 시간(ms)은 여기서만 나온다:

| 정지 | $N=16$ | $N=32$ | $N=64$ | $N=128$ |
|---:|---:|---:|---:|---:|
| 100 ms | 16 | 0 | 0 | 0 |
| 300 ms | 216 | 136 | 0 | 0 |
| 1,000 ms | 916 | 836 | 676 | 356 |

여기서 새로 보이는 것 셋.
- **락은 나쁜 순서를 드물게 하는 것이 아니라 지운다.** 모든 $k$에서 $2k$로 끝나는 순서는 정확히 쪼개지지 않은 순서이고 $\binom{2k}{k}$개다. 1d부가 증가마다 한 단계로 만들어 얻는 수와 같다.
- **용량은 시간을 살 뿐 안전을 사지 않는다.** 막기에서 100 ms 정지는 32칸이 흡수하고 300 ms 정지는 64칸이 필요하지만, 1,000 ms 정지는 128칸으로도 제어 스레드를 356 ms 멈춘다. 한 칸은 5 ms만 덮는다. 모든 정지를 덮는 것은 정책 — 제어 스레드를 막지 않기 — 뿐이다.
- **사본은 되풀이하고 spawn한 스트림은 그러지 않는다.** `default_rng(0)`을 pickle한 사본 둘은 같은 네 수를 뽑고, `SeedSequence` 하나의 자식 둘은 다른 수를 뽑는다. PyTorch 없이 본 §9의 DataLoader 함정이다.

### 12. 이 페이지가 다루지 않는 것

메모리 순서(C++의 `std::memory_order`)와 락 없는 자료 구조. 단일 생산자 단일 소비자 링 버퍼와 제어 루프의 실시간 규칙은 [[02-foundations/algorithms/interview-code|11.7 §6]]에 있다. 조건 변수, 세마포어, 이벤트는 `threading` 문서에 있다. ROS 2 콜백 체인의 응답 시간 분석은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §6]]이 가리키고, GPU 스트림과 호스트 동기화는 [[03-deep-learning/foundations/gpu-computing|1.4 §7]]이다. 분산 학습, 교착 예방과 탐지의 이론(출처의 1971년 서베이), 모델 검사기는 다루지 않는다. 클러스터 노드에 할당된 코어 위에서 데이터를 옮겨 두고 데이터 로더를 돌리는 법은 [[02-foundations/tools/gpu-clusters|12.7 GPU 클러스터 §8]]이다.

### 읽고 나면

- [ ] 한 프로세스의 스레드들이 무엇을 함께 쓰는지, 그리고 데이터 로더의 워커는 프로세스이고 P6의 콜백은 스레드인 이유를 말한다.
- [ ] Python 한 줄이 다른 스레드가 끼어들 수 있는 여러 단계인 이유를 설명한다.
- [ ] 잃어버린 갱신을 한 단계씩 따라가고, $\binom{m_A+m_B}{m_A}$로 인터리빙을 세고, 두 필드 목표를 찢는 순서를 나열한다.
- [ ] 임계 구역에 락을 두르고 그 값과 그것이 고치지 못하는 것을 말하거나, 공유 데이터를 대입 한 번으로 공개한다.
- [ ] 락에 순위를 매기거나 락 둘을 함께 쥐지 않아서 락 순서 교착을 없앤다.
- [ ] $t_{\text{full}}$과 $n_{\text{over}}$로 정지에 맞서 유한 버퍼의 크기를 정하고, 찬 큐 정책을 고른다.
- [ ] 암달의 법칙으로 속도 향상의 상한을 구하고, 가장 느린 단계로 로더의 워커 수를 정하고, Python 작업에 스레드·프로세스·asyncio 중 무엇을 쓸지 고른다.

### 스스로 점검

1. 두 스레드가 각자 `n_cb += 1`을 한 번 돈다. 읽기와 저장의 인터리빙은 몇 개이고, 그중 몇 개가 갱신을 잃는가? "백만 번 돌려도 한 번도 틀리지 않았다"가 답이 되지 못하는 이유는?
2. 틱은 `goal_lock` 아래에서 목표의 두 필드를 읽지만 `on_goal`은 락 없이 쓴다. 찢어진 읽기는 고쳐졌는가?
3. P6의 로그 기록 스레드가 디스크에 쓰는 동안 `log_lock`을 쥐고, 틱은 기록을 덧붙이려 같은 락을 잡는다. 300 ms 디스크 정지가 틱에 무엇을 하는가, 그리고 고치는 법은?
4. 틱은 `goal_lock` 다음 `log_lock`을 잡고 기록 스레드는 반대 순서로 잡는다. 여기서 드러나는 교착의 네 조건과, 한 줄로 고치는 법 둘을 말하라.
5. PyTorch 학습 스크립트가 스레드가 아니라 워커 프로세스로 데이터를 읽는 이유는? 데이터셋이 `__init__`에서 NumPy 생성기를 만들면 무엇이 잘못되는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. $I(2,2)=\binom{4}{2}=6$개이고 그중 4개가 갱신을 잃는다. 두 스레드가 모두 어느 쪽도 저장하기 전에 100을 읽으므로 둘 다 101을 저장한다. 백만 번의 깨끗한 실행은 이 인터프리터에서 나쁜 순서가 드물다는 것을 보여 줄 뿐 불가능하다는 것을 보여 주지 않는다. 여기서 맨 증가는 아무것도 잃지 않았지만 가운데에 호출을 둔 같은 증가는 27–33%를 잃었다. 모든 인터리빙을 옳게 만드는 것은 강제된 순서(락, 대입 한 번, 큐)뿐이다.
> 2. 아니다. 락은 그것을 잡는 코드만 지킨다. `on_goal`의 두 저장은 임계 구역이 아니므로, 틱의 임계 구역 전체가 그 사이에 돌아 $(0.510\,\mathrm{m},\,1000\,\mathrm{ms})$를 읽을 수 있다. 양쪽 모두 락을 잡거나, 불변 튜플 하나를 대입 한 번으로 공개한다.
> 3. 틱은 기록 스레드가 락을 쥐는 동안 내내, 곧 정지 전체 동안 기다린다. 명령 없이 $300/5=60$틱, $300/70=4.3$예산이다. 버퍼를 바꾸는 동안만 `log_lock`을 쥐고 쓰기는 락 밖에서 하며, 틱에는 막히지 않는 put을 주어 큐가 차면 제어기를 멈추는 대신 기록 하나를 버리게 한다.
> 4. 상호 배제(락마다 쥔 쪽 하나), 점유와 대기(각자 첫 락을 쥔 채 둘째 락을 기다림), 비선점(어느 락도 빼앗을 수 없음), 순환 대기(틱 → `log_lock` → 기록 스레드 → `goal_lock` → 틱). 기록 스레드가 `goal_lock`을 먼저 잡게 하거나(고리 없음), 목표를 복사하고 `goal_lock`을 푼 뒤 `log_lock`을 잡게 한다(점유와 대기 없음). 실습은 변경 전에 스케줄 6개 중 2개가 교착하고, 어느 변경 뒤에도 0개임을 찾는다.
> 5. 한 프로세스 안에서 GIL은 스레드들에 걸친 진정한 병렬 Python을 막으므로, 디코딩과 증강을 스레드로 하면 병렬로 돌지 않는다. 워커 프로세스는 저마다 자기 인터프리터를 갖는다. 그러나 워커마다 생성기까지 든 데이터셋의 사본을 같은 상태로 받으므로 모두 같은 "무작위" 수를 뽑는다. 여기서는 윈도 0과 2가 같은 잡음을 받았다. 워커마다 `worker_init_fn`에서 `get_worker_info().seed`로 시딩하거나, `SeedSequence.spawn`으로 스트림을 따로 준다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6 Lab Plants]]만 쓴다. 모든 문제가 손잡이 하나를 돌린다 — 목표의 셋째 필드, 셋째 락, 더 긴 정지 속의 더 큰 큐, 더 병렬적인 작업, 더 느린 로더 — 그러니 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 변형에 대한 그림. (a) 목표에 순번 $q$(50 → 51)가 생기고 $p$와 $s$ 뒤에 저장되고 그 뒤에 읽힌다. `on_goal`의 저장 셋과 틱의 읽기 셋을 목표를 찢는 순서 하나로 그리고, 각 단계 뒤의 공유 메모리를 적는다. (b) 디스크 감시 스레드가 새 `disk_lock` 다음 `goal_lock`을 잡고, 기록 스레드는 이제 `log_lock` 다음 `disk_lock`을, 틱은 여전히 `goal_lock` 다음 `log_lock`을 잡는다. 대기 고리를 그리고, 락 순서가 없앨 화살표를 표시한다. (c) $D=400\,\mathrm{ms}$ 정지 속 $N=48$칸 로그 큐를 "최신 버리기"와 "늘리기"로 그리고, "막기"가 제어 스레드를 멈출 구간을 표시한다.
2. **유도.** (a) 저장 셋과 읽기 셋의 인터리빙을 세고, 그중 틱이 모두 옛 값, 모두 새 값, 찢어진 섞임을 읽는 순서를 센다(필드 $i$는 그 저장이 그 읽기보다 앞설 때 정확히 새 값으로 읽힌다). 찢어진 비율을 두 필드 목표와 비교한다. (b) 1(b)의 세 스레드가 교착하는 스케줄을 보이고, 네 조건을 말하고, 락 순위와 바뀌어야 할 스레드 하나를 댄다. (c) $N=48$, $D=400\,\mathrm{ms}$에서 $t_{\text{full}}$, 용량을 넘는 기록 수, "막기"가 제어 스레드를 붙잡는 시간과 모터가 새 명령 없이 지내는 시간을 70 ms 예산에 견주어, 그리고 "늘리기"의 최고치를 바이트로. (d) $P=0.95$의 암달: 120 s 작업의 코어 8개 시간과 바닥. 그리고 $t_{\text{load}}=60\,\mathrm{ms}$, $t_{\text{GPU}}=8\,\mathrm{ms}$인 로더에서 GPU를 바쁘게 두는 가장 적은 워커 수와, 워커 4개일 때의 가동률.
3. **실행.** 영어 절 템플릿의 `?`를 채워 §11의 실습 뒤에 돌리고, 출력의 (a)–(c)를 유도와, 페이지의 두 필드, $N=32$, $P=0.9$ 숫자와 견준다.

> [!note]- 그리는 법 · How to draw it
> - (a) 고른 순서의 원자적 단계마다 열 하나, 스레드마다 레인 하나, 공유 메모리의 필드마다 행 하나를 두고 각 단계 뒤의 값을 적는다. 찢어진 읽기는 틱의 읽기 셋이 돌려주는 세 값이고, 어떤 저장도 그것을 통째로 쓴 적이 없다.
> - (b) 스레드는 상자, 락은 둥근 상자. 락에서 쥔 스레드로 실선 화살표, 스레드에서 기다리는 락으로 점선 화살표. 순위를 `goal_lock` < `log_lock` < `disk_lock`으로 두면, 순위 높은 락을 쥔 채 순위 낮은 락을 기다리는 화살표가 금지되는 것이다.
> - (c) 가로는 정지 시작부터의 시간, 세로는 기록 수, 용량에 점선, 정지 구간은 음영. "최신 버리기"는 초당 200개씩 $N$까지 올라 디스크가 돌아올 때까지 평평하다가 순 초당 800개로 내려가고, "늘리기"는 $\lambda D$까지 올라 같은 속도로 내려간다. "막기"는 큐가 찬 것을 처음 본 틱부터 기록 스레드의 첫 쓰기까지 막대로 그리고, 삼키는 틱 수를 적는다.

> [!tip]- 정답 · Solutions
> 1. (a) 예컨대 AABBBA. `on_goal`이 $p=0.510$과 $s=1020$을 저장하고, 틱이 셋을 모두 읽고, 그다음에야 $q=51$이 저장된다. 메모리는 $(0.510, 1000, 50)$, 5단계까지 $(0.510, 1020, 50)$, 그다음 $(0.510, 1020, 51)$이다. 틱은 $(0.510\,\mathrm{m},\,1020\,\mathrm{ms},\,50)$을 읽는다. 목표 51의 데이터에 목표 50의 번호다. (b) 틱 → `log_lock` → 기록 스레드 → `disk_lock` → 감시 스레드 → `goal_lock` → 틱. `disk_lock`을 쥔 채 `goal_lock`을 기다리는 감시 스레드의 화살표가 순위를 내려가므로 그것을 없앤다. (c) 두 곡선 모두 240 ms에 48에 닿는다. "최신 버리기"는 400 ms까지 48에 머물며 32개를 버리고 459 ms에 빈다. "늘리기"는 400 ms에 80까지 올라 499 ms에 빈다. "막기" 막대는 245–401 ms, 156 ms, 틱 31번이다.
> 2. (a) $\binom{6}{3}=20$개. 모두 옛 값 5, 모두 새 값 5, 찢어짐 10으로 50%, 두 필드의 $2/6=33\%$와 비교된다. (모두 옛 값과 모두 새 값의 수는 카탈랑 수 2, 5, 14, …이므로 필드 $n$개면 순서의 $(n-1)/(n+1)$이 찢어진다.) (b) 틱이 `goal_lock`을, 기록 스레드가 `log_lock`을, 감시 스레드가 `disk_lock`을 잡은 뒤, 저마다 다음 스레드가 쥔 락을 청한다. 상호 배제, 점유와 대기, 비선점, 순환 대기(1(b)의 고리). 순위 `goal_lock` < `log_lock` < `disk_lock`에서 틱과 기록 스레드는 이미 오르고, 감시 스레드가 `disk_lock` 전에 `goal_lock`을 잡거나 목표를 복사하고 `goal_lock`을 먼저 풀어야 한다. (c) $t_{\text{full}}=48/200=0.240\,\mathrm{s}$, $n_{\text{over}}=200\times(0.400-0.240)=32$. "막기"는 245 ms의 틱을 401 ms의 첫 쓰기까지 156 ms 붙잡고, 250 ms부터 400 ms까지 도래하는 틱 31번은 돌지 못한다. 245 ms부터 405 ms까지 새 명령 없이 160 ms, 예산 2.29개다. "늘리기"는 $200\times0.4=80$개, $80\times64=5{,}120$바이트가 최고치다. (d) $S(8)=1/(0.05+0.95/8)=5.93$이므로 120 s가 20.25 s가 되고, $120\times0.05=6\,\mathrm{s}$ 아래로는 내려가지 않는다. 로더에는 $\lceil60/8\rceil=\lceil7.5\rceil=8$개 워커가 필요하고, 4개면 초당 $4/0.060=66.67$개 배치로 GPU는 $66.67\times0.008=53.3\%$만 바쁘다.
> 3. 빈칸은 차례로 `SEQ_NEW`, `mem["q"]`, `3, 3`, 큐 호출의 `48`과 `400`, `P2`의 `0.95`, `60.0, 8.0`, `1000 * W / T_LOAD`다. 출력은 영어 절 정답 3과 같고, 요약하면:
>
>    | 부분 | 결과 |
>    |---|---|
>    | (a) 세 필드 | 순서 20개: 옛 값 5, 새 값 5, 찢어짐 10 |
>    | (b) $N=48$, 400 ms 정지 | 두 버리기: 최고 48, 32개 버림, 459 ms에 빔. 막기: 틱 31번 잃음, 156 ms 갇힘, 460 ms에 빔. 늘리기: 최고 80, 499 ms에 빔 |
>    | (c) $P=0.95$와 느린 로더 | $n=2, 4, 8, 16$에서 1.90, 3.48, 5.93, 9.14. 120 s 작업은 코어 8개에서 20.25 s, 6 s 아래로는 안 됨. 워커 1, 4, 7, 8, 12개에서 초당 16.67, 66.67, 116.67, 125.00, 125.00개, GPU 13.3, 53.3, 93.3, 100.0, 100.0% |
>
>    (a)는 2(a)와 맞는다. 셋째 필드가 찢어진 비율을 3분의 1에서 절반으로 올린다. (b) $N=32$와 300 ms에 견주면 16칸이 큐가 차기까지 80 ms를 더 벌었지만, 더 긴 정지는 여전히 32개만큼 넘치고 "막기"는 제어 스레드를 여전히 156 ms, 예산의 두 배 넘게 멈춘다. (c) $P=0.95$에서 작업은 코어 8개로 5.93배를 얻어 $P=0.9$의 4.71배와 비교되고, 느린 로더는 페이지의 4개 대신 8개 워커가 필요하다. $\lceil t_{\text{load}}/t_{\text{GPU}}\rceil$이 두 배가 되었기 때문이다.

### 출처

- Python 3.14 문서, [docs.python.org/3](https://docs.python.org/3/) — 용어집, 라이브러리 FAQ(스레드 안전한 연산, GIL), `threading`, `queue`, `collections`, `multiprocessing`, `concurrent.futures`, asyncio 개발 안내, `sys`, 자유 스레드 HOWTO, What's New in 3.14와 3.2.
- PyTorch 2.14, [torch.utils.data](https://docs.pytorch.org/docs/2.14/data.html) — 워커 프로세스, 미리 읽기, Python 객체와 메모리, 워커 시드.
- NumPy 2.5, [스레드 안전성](https://numpy.org/doc/stable/reference/thread_safety.html)과 [병렬 난수 생성](https://numpy.org/doc/stable/reference/random/parallel.html).
- Linux man-pages, [pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html), [sched(7)](https://man7.org/linux/man-pages/man7/sched.7.html), [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html) — 공유 메모리, 스케줄링 정책, fork와 copy-on-write.
- C++: 작업 초안의 [intro.races](https://eel.is/c++draft/intro.races), 그리고 cppreference의 [std::thread](https://en.cppreference.com/w/cpp/thread/thread), [std::mutex](https://en.cppreference.com/w/cpp/thread/mutex), [std::scoped_lock](https://en.cppreference.com/w/cpp/thread/scoped_lock), [std::atomic::fetch_add](https://en.cppreference.com/w/cpp/atomic/atomic/fetch_add).
- Clang, [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) — `-fsanitize=thread`와 그 비용.
- NVIDIA, [CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) v13.4, §4.1.3.1–§4.1.3.2 — 암달과 구스타프슨의 법칙.
- G. M. Amdahl, "Validity of the single processor approach to achieving large scale computing capabilities", AFIPS Spring Joint Computer Conference, 1967 — Crossref에서 서지 기록 확인.
- E. G. Coffman, M. Elphick, A. Shoshani, "System Deadlocks", ACM Computing Surveys 3(2):67–78, 1971 — 교착 처리에 대한 서베이. Crossref에서 서지 기록과 초록 확인.
- 이 페이지를 쓴 기계(Apple silicon의 macOS, Python 3.12.4, NumPy 2.0.2, PyTorch 2.6.0) — §1, §2, §4, §8, §9의 측정값.
