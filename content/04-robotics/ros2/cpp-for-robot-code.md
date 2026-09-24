---
title: "25.0 C++ for Robot Code"
tags: [robotics, ros2, systems, cpp]
study-depth: Working
wiki-support: Working
depth-goal: "Read a robot's C++ controller and say who owns each object and how long it lives; lay out a struct byte by byte; count what one control tick copies, allocates and calls; build it with CMake; and find and fix the classic defects — a dangling reference, a shared_ptr cycle, a base class without a virtual destructor, a copied resource owner, an allocation or a blocking call in the tick."
mastery-when: "Raise when a real-time driver, hardware component or controller you write is what an experiment or a deployment rests on."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]] (plant **P6**: 2,048 counts/m, a 50 Hz goal, a 200 Hz loop, a 70 ms budget), [[04-robotics/robot-systems-deployment|10. Robot Systems §3]] (the latency budget, deadlines and jitter, which §9 applies to one tick) and [[02-foundations/algorithms/data-structures|11.2 Core Data Structures]] (§2's arrays and dynamic arrays with amortized growth, §3's hash tables and §5's search trees, taught there in Python). Python is assumed and C++ is not. The listings need a C++17 compiler (clang++ or g++) and a terminal, and §8 needs CMake; no ROS installation is needed.
> [[02-foundations/lab-plants|0.6 Lab Plants]](장치 **P6**: 2,048 counts/m, 50 Hz 목표, 200 Hz 루프, 70 ms 예산), [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]](§9가 틱 하나에 적용하는 지연 예산, 마감, 지터), [[02-foundations/algorithms/data-structures|11.2 핵심 자료구조]](거기서 Python으로 가르친 §2의 배열과 분할상환 성장을 하는 동적 배열, §3의 해시 테이블, §5의 탐색 트리). Python은 전제하고 C++는 전제하지 않는다. 목록을 돌리려면 C++17 컴파일러(clang++나 g++)와 터미널이, §8에는 CMake가 필요하다. ROS 설치는 필요 없다.

## English

*Stands on [[02-foundations/lab-plants|0.6 Lab Plants]], whose plant **P6** is the cart this page programs, and [[04-robotics/robot-systems-deployment|10. Robot Systems §3]], which sets the 70 ms budget and the per-tick deadline the program has to meet. First use of **P6** as a C++ program. The ROS 2 track after it assumes what is taught here: [[04-robotics/ros2/nodes-topics-messages|25.2 §6]] reads a C++ node line by line, [[04-robotics/ros2/workspaces-packages-launch|25.4]] builds C++ packages with ament and colcon, [[04-robotics/ros2/simulation-and-control|25.7 §5]] puts controllers and hardware on the two sides of an interface, and [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]] writes one side of it.*

> [!note] Why this matters · 왜 배우는가
> C++ is the layer of the physical-AI stack of [[07-research-program/index|7 §5]] where the controller and the drivers actually run: ros2_control's controllers and hardware components, and most robot drivers, are C++ called every period, so in "install that panel on the frame" it is the code that moves the component, detects contact and performs the fitting (its place is marked on the [[physical-ai-map|Physical AI Map]]). A defect there fails the robot, not a test: a base class without a virtual destructor leaves P6's drive enabled at its last command, a `shared_ptr` cycle keeps a node — and the drive it owns — alive after Ctrl-C, and a `push_back` in the tick moves 262,144 bytes inside one 5 ms period 41 s into a run. The need arrives in block 2 of the dissertation path ([[07-research-program/index|7 §8]]), the first time you read a C++ node ([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]) or put a controller and hardware on the two sides of an interface ([[04-robotics/ros2/simulation-and-control|25.7 §5]], [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]), and again in block 7, where the learned policy's impedance targets are rendered by a controller running at its own rate ([[05-construction-robotics/imitating-contact|10. Imitating Contact §6]]). After this page you can say who owns each object in a robot's C++ and how long it lives, and keep a control tick free of allocation, blocking and undefined behaviour.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes, compiling as you read — every listing was built with `clang++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined`, and each output shown is what a run printed. **Session 1 — who owns what, and for how long.** The Running object and the picture, then §1–§5: values and references, lifetime, layout, classes and RAII, ownership. Answer Self-check 1–4. **Session 2 — the controller and its tick.** §6, §7 and §9, then the Worked case, which counts one tick with all of it; answer Self-check 5 and 7 and do the code review of problem 3. Read §8 the first time a build fails and §10 the first time a sanitizer speaks; problems 1–2 and every *Deeper* callout can wait for a second pass.

### Running object · 이 페이지의 대상

Plant **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], at the catalog's numbers: a cart on a line, position $p$ in metres, an encoder of $N=2048$ counts/m, a vision node that publishes a goal at $f_v=50$ Hz, a controller that reads the encoder and commands the motor at $f_c=200$ Hz, and a 70 ms budget from camera mid-exposure to applied force. A rate and its period are reciprocals, so the control period is $T=1/f_c=5$ ms and the vision period $T_v=1/f_v=20$ ms.

This page writes that controller as one C++ program and freezes the program's own numbers here. They are this page's, not the catalog's, and no other page depends on them:

| Name | Value | What it is |
|---|---|---|
| `EncoderSample`, as first written | `bool valid;` `std::int64_t stamp_ns;` `std::int32_t counts;` | one encoder read: a validity flag, the time of the read in nanoseconds, the count |
| `EncoderSample` (§3) | `std::int64_t stamp_ns;` `std::int32_t counts;` `bool valid;` | the same three fields, largest alignment first |
| `TickRecord` | `std::int64_t stamp_ns;` then three `double`: `goal_m`, `position_m`, `effort` | one line of the run log |
| $K$ | 5 samples | the ring buffer `RingBuffer<EncoderSample, 5>`: a velocity over $(K-1)T=20$ ms, one vision period |
| run | 60 s = 12,000 ticks | one test run, and so the length of the log |
| $k_p$, $k_d$ | 2.0 per m, 0.5 per m/s | the PD gains; `effort` is a normalized command in $[-1,1]$ |
| simulated cart | 0.5 m/s at full effort | used only by the test run of §9 |
| `MotorInterface` | `enable()`, `disable()`, `set_effort(double)` | the seam between controller and drive; `SimMotor` and `RealMotor` implement it (§7) |

Byte counts on this page hold for 64-bit Linux on x86-64 and on ARM64, and for the ARM64 Mac the listings ran on; §3 says which of them the language fixes and which the platform does.

*Scope: the C++ a robotics researcher needs to read, modify and debug robot code — values, references and pointers; lifetime; layout; classes and RAII; ownership; templates and containers; interfaces; building with CMake; the rules of a real-time tick; and the tools that catch what those rules forbid — all on P6's controller. It does not teach C++ as a whole, which §10 maps, nor ROS 2's C++ API ([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]), ament and colcon ([[04-robotics/ros2/workspaces-packages-launch|25.4]]) or a ros2_control hardware component ([[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]).*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 440" style="max-width:100%;height:auto" role="img" aria-label="Two panels. (a) P6's encoder sample drawn byte by byte: as first written, a 1-byte valid flag, 7 bytes of padding, an 8-byte stamp, a 4-byte count and 4 bytes of tail padding, 24 bytes; reordered with the stamp first, 16 bytes with 3 of padding. (b) The process's memory during a tick: main's stack frame holds a shared_ptr to the node with use count 1; the node on the heap holds its timer with use count 1 and the controller, which owns the motor through a unique_ptr, keeps its 96-byte ring buffer in place and owns 384,000 bytes of reserved log storage; the timer's callback observes the node through this, and the executor observes the timer through a weak_ptr.">
  <defs><marker id="cppAr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="8" y="16" font-size="12" fill="currentColor">(a) EncoderSample, one cell per byte, before and after reordering</text>
  <text x="8" y="41" font-size="11" fill="currentColor">as written</text>
  <text x="8" y="53" font-size="10" fill="currentColor" fill-opacity="0.8">24 B · 11 pad</text>
  <rect x="104" y="30" width="18" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="113" y="46" font-size="10" fill="currentColor" text-anchor="middle">v</text>
  <rect x="122" y="30" width="126" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="185" y="46" font-size="10" fill="currentColor" text-anchor="middle">padding 7</text>
  <rect x="248" y="30" width="144" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="320" y="46" font-size="10" fill="currentColor" text-anchor="middle">stamp_ns (8)</text>
  <rect x="392" y="30" width="72" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="428" y="46" font-size="10" fill="currentColor" text-anchor="middle">counts (4)</text>
  <rect x="464" y="30" width="72" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="500" y="46" font-size="10" fill="currentColor" text-anchor="middle">pad 4</text>
  <g stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"><line x1="122" y1="30" x2="122" y2="35"/><line x1="122" y1="49" x2="122" y2="54"/><line x1="140" y1="30" x2="140" y2="35"/><line x1="140" y1="49" x2="140" y2="54"/><line x1="158" y1="30" x2="158" y2="35"/><line x1="158" y1="49" x2="158" y2="54"/><line x1="176" y1="30" x2="176" y2="35"/><line x1="176" y1="49" x2="176" y2="54"/><line x1="194" y1="30" x2="194" y2="35"/><line x1="194" y1="49" x2="194" y2="54"/><line x1="212" y1="30" x2="212" y2="35"/><line x1="212" y1="49" x2="212" y2="54"/><line x1="230" y1="30" x2="230" y2="35"/><line x1="230" y1="49" x2="230" y2="54"/><line x1="248" y1="30" x2="248" y2="35"/><line x1="248" y1="49" x2="248" y2="54"/><line x1="266" y1="30" x2="266" y2="35"/><line x1="266" y1="49" x2="266" y2="54"/><line x1="284" y1="30" x2="284" y2="35"/><line x1="284" y1="49" x2="284" y2="54"/><line x1="302" y1="30" x2="302" y2="35"/><line x1="302" y1="49" x2="302" y2="54"/><line x1="320" y1="30" x2="320" y2="35"/><line x1="320" y1="49" x2="320" y2="54"/><line x1="338" y1="30" x2="338" y2="35"/><line x1="338" y1="49" x2="338" y2="54"/><line x1="356" y1="30" x2="356" y2="35"/><line x1="356" y1="49" x2="356" y2="54"/><line x1="374" y1="30" x2="374" y2="35"/><line x1="374" y1="49" x2="374" y2="54"/><line x1="392" y1="30" x2="392" y2="35"/><line x1="392" y1="49" x2="392" y2="54"/><line x1="410" y1="30" x2="410" y2="35"/><line x1="410" y1="49" x2="410" y2="54"/><line x1="428" y1="30" x2="428" y2="35"/><line x1="428" y1="49" x2="428" y2="54"/><line x1="446" y1="30" x2="446" y2="35"/><line x1="446" y1="49" x2="446" y2="54"/><line x1="464" y1="30" x2="464" y2="35"/><line x1="464" y1="49" x2="464" y2="54"/><line x1="482" y1="30" x2="482" y2="35"/><line x1="482" y1="49" x2="482" y2="54"/><line x1="500" y1="30" x2="500" y2="35"/><line x1="500" y1="49" x2="500" y2="54"/><line x1="518" y1="30" x2="518" y2="35"/><line x1="518" y1="49" x2="518" y2="54"/></g>
  <text x="104" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="248" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">8</text>
  <text x="392" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">16</text>
  <text x="536" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">24</text>
  <text x="8" y="87" font-size="11" fill="currentColor">reordered</text>
  <text x="8" y="99" font-size="10" fill="currentColor" fill-opacity="0.8">16 B · 3 pad</text>
  <rect x="104" y="76" width="144" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="176" y="92" font-size="10" fill="currentColor" text-anchor="middle">stamp_ns (8)</text>
  <rect x="248" y="76" width="72" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="284" y="92" font-size="10" fill="currentColor" text-anchor="middle">counts (4)</text>
  <rect x="320" y="76" width="18" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="329" y="92" font-size="10" fill="currentColor" text-anchor="middle">v</text>
  <rect x="338" y="76" width="54" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="92" font-size="10" fill="currentColor" text-anchor="middle">pad 3</text>
  <g stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"><line x1="122" y1="76" x2="122" y2="81"/><line x1="122" y1="95" x2="122" y2="100"/><line x1="140" y1="76" x2="140" y2="81"/><line x1="140" y1="95" x2="140" y2="100"/><line x1="158" y1="76" x2="158" y2="81"/><line x1="158" y1="95" x2="158" y2="100"/><line x1="176" y1="76" x2="176" y2="81"/><line x1="176" y1="95" x2="176" y2="100"/><line x1="194" y1="76" x2="194" y2="81"/><line x1="194" y1="95" x2="194" y2="100"/><line x1="212" y1="76" x2="212" y2="81"/><line x1="212" y1="95" x2="212" y2="100"/><line x1="230" y1="76" x2="230" y2="81"/><line x1="230" y1="95" x2="230" y2="100"/><line x1="248" y1="76" x2="248" y2="81"/><line x1="248" y1="95" x2="248" y2="100"/><line x1="266" y1="76" x2="266" y2="81"/><line x1="266" y1="95" x2="266" y2="100"/><line x1="284" y1="76" x2="284" y2="81"/><line x1="284" y1="95" x2="284" y2="100"/><line x1="302" y1="76" x2="302" y2="81"/><line x1="302" y1="95" x2="302" y2="100"/><line x1="320" y1="76" x2="320" y2="81"/><line x1="320" y1="95" x2="320" y2="100"/><line x1="338" y1="76" x2="338" y2="81"/><line x1="338" y1="95" x2="338" y2="100"/><line x1="356" y1="76" x2="356" y2="81"/><line x1="356" y1="95" x2="356" y2="100"/><line x1="374" y1="76" x2="374" y2="81"/><line x1="374" y1="95" x2="374" y2="100"/></g>
  <text x="104" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="248" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">8</text>
  <text x="320" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">12</text>
  <text x="392" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">16</text>
  <text x="8" y="132" font-size="10" fill="currentColor">v = valid (bool, 1 B) · int64 8 B · int32 4 B · shaded = padding · ring of 5: 136 B → 96 B</text>
  <text x="8" y="156" font-size="12" fill="currentColor">(b) Memory during a tick: solid arrows own, dashed arrows observe</text>
  <rect x="8" y="166" width="124" height="266" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <text x="16" y="182" font-size="11" fill="currentColor" font-weight="bold">stack</text>
  <text x="16" y="196" font-size="10" fill="currentColor" fill-opacity="0.8">main's frame</text>
  <rect x="16" y="206" width="108" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="22" y="221" font-size="10" fill="currentColor">node: shared_ptr</text>
  <rect x="16" y="382" width="108" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="22" y="397" font-size="10" fill="currentColor">executor</text>
  <rect x="144" y="166" width="408" height="266" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <text x="152" y="182" font-size="11" fill="currentColor" font-weight="bold">heap</text>
  <rect x="156" y="190" width="360" height="140" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="164" y="206" font-size="11" fill="currentColor" font-weight="bold">CartNode</text>
  <text x="164" y="222" font-size="10" fill="currentColor">timer_: shared_ptr&lt;Timer&gt;</text>
  <rect x="176" y="230" width="300" height="92" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="184" y="245" font-size="10" fill="currentColor" font-style="italic">controller_: CartController, inside the node</text>
  <text x="184" y="262" font-size="10" fill="currentColor">motor_: unique_ptr&lt;MotorInterface&gt;</text>
  <text x="184" y="278" font-size="10" fill="currentColor">history_: RingBuffer, 96 B, in place</text>
  <text x="184" y="294" font-size="10" fill="currentColor">log_: vector&lt;TickRecord&gt;</text>
  <text x="184" y="310" font-size="10" fill="currentColor">goal_m_: atomic&lt;double&gt;</text>
  <rect x="156" y="342" width="100" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="206" y="358" font-size="10" fill="currentColor" text-anchor="middle">SimMotor or</text>
  <text x="206" y="373" font-size="10" fill="currentColor" text-anchor="middle">RealMotor</text>
  <rect x="268" y="342" width="164" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="350" y="358" font-size="10" fill="currentColor" text-anchor="middle">log storage</text>
  <text x="350" y="373" font-size="10" fill="currentColor" text-anchor="middle">12,000 × 32 B = 384,000 B</text>
  <rect x="444" y="342" width="100" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="494" y="358" font-size="10" fill="currentColor" text-anchor="middle">Timer</text>
  <text x="494" y="373" font-size="10" fill="currentColor" text-anchor="middle">callback: this</text>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <line x1="124" y1="217" x2="155" y2="217" marker-end="url(#cppAr)"/>
    <polyline points="318,219 494,219 494,341" marker-end="url(#cppAr)"/>
    <polyline points="182,258 168,258 168,341" marker-end="url(#cppAr)"/>
    <polyline points="330,290 344,290 344,341" marker-end="url(#cppAr)"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3">
    <polyline points="544,362 550,362 550,200 517,200" marker-end="url(#cppAr)"/>
    <polyline points="124,393 138,393 138,416 494,416 494,383" marker-end="url(#cppAr)"/>
  </g>
  <text x="140" y="211" font-size="10" fill="currentColor" text-anchor="middle" font-weight="bold">1</text>
  <text x="500" y="290" font-size="10" fill="currentColor" font-weight="bold">1</text>
  <text x="533" y="282" font-size="10" fill="currentColor" text-anchor="middle">this</text>
  <text x="316" y="428" font-size="10" fill="currentColor" text-anchor="middle">weak_ptr</text>
</svg>

Top: P6's encoder sample one cell per byte — as first written it is 24 bytes, 11 of them padding, and with the 8-byte stamp first it is 16 bytes, 3 of them padding, so the five-sample ring with its two indices takes 96 bytes instead of 136. Bottom: the process's memory while the loop runs — `main`'s frame holds a `shared_ptr` to the node (use count 1, and 2 while `spin` holds its own copy), the node owns its timer (use count 1) and its controller, the controller owns the drive and 384,000 bytes of reserved log, and the timer's callback observes the node through `this` while the executor observes the timer through a `weak_ptr`.

### 1. Values, references and pointers

*In one sentence:* coming from Python, the first surprise is that a C++ variable holds its value itself, so handing it to a function by value copies every byte of it, and a reference or a pointer is how a function reaches an object without that copy — the reference as a second name that must name something, the pointer as an address that may be null.

In Python a name refers to an object, and passing it to a function passes that reference; nothing is copied. C++ works the other way round. `EncoderSample b = a;` creates a second sample and copies `a`'s 16 bytes into it, and a function parameter of type `EncoderSample` is a new object initialized as a copy of the argument. For a 16-byte struct that costs next to nothing. For a `std::vector` it means a new block of heap memory and a copy of every element (§6), because copying a vector copies what it holds, not a handle to it.

Four ways to hand P6's sample to a function, and the parameter type that says which one a function uses:

```cpp
// pass.cpp - four ways to hand P6's encoder sample to a function
#include <cstdint>
#include <cstdio>

struct EncoderSample {                          // section 3 explains the field order
  std::int64_t stamp_ns;                        // time of the read, nanoseconds
  std::int32_t counts;                          // encoder counts, 2048 per metre (P6)
  bool valid;                                   // false if the read failed
};

constexpr double kCountsPerMetre = 2048.0;

double metres(const EncoderSample& s) {         // const&: an alias, no copy, no writes
  return s.counts / kCountsPerMetre;
}

EncoderSample shifted(EncoderSample s, std::int32_t offset) {  // by value: the callee owns a copy
  s.counts -= offset;                           // changes the copy only
  return s;
}

void zero(EncoderSample& s) { s.counts = 0; }   // non-const &: writes reach the caller

bool metres_if_valid(const EncoderSample* s, double* out) {    // a pointer may be null
  if (s == nullptr || !s->valid) return false;
  *out = metres(*s);
  return true;
}

int main() {
  EncoderSample s{5'000'000, 819, true};        // read at t = 5 ms, 819 counts
  const EncoderSample moved = shifted(s, 10);
  std::printf("metres %.4f, shifted copy %.4f, caller still has %d counts\n",
              metres(s), metres(moved), s.counts);
  double p = -1.0;
  const bool got = metres_if_valid(&s, &p);
  const bool none = metres_if_valid(nullptr, &p);
  zero(s);
  std::printf("pointer: %s at %.4f m; null pointer: %s; after zero(): %d counts\n",
              got ? "read" : "no sample", p, none ? "read" : "no sample", s.counts);
}
```

```bash
clang++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined pass.cpp -o pass && ./pass
```

```text
metres 0.3999, shifted copy 0.3950, caller still has 819 counts
pointer: read at 0.3999 m; null pointer: no sample; after zero(): 0 counts
```

Read the four signatures, not the bodies. `const EncoderSample&`, a reference to const, is the default for reading anything larger than a few machine words: there is no copy, and the compiler rejects any write through it, so the caller knows its sample comes back unchanged. By value, `EncoderSample s`, is right when the callee wants a copy of its own to change, as `shifted` does; the first output line shows the caller's 819 counts untouched after the copy was shifted to 809. A reference to non-const, `EncoderSample&`, is an output: `zero` wrote through it and the caller saw 0. A pointer, `const EncoderSample*`, is the only one of the four that can say "there is no sample", by being null, and so the only one the callee must check before using it. Reading through a null pointer is undefined behaviour — defined in §2: not an exception and not a guaranteed crash, but a program the language no longer describes.

`const` is a promise the compiler enforces: on a variable (`const double p`), on a parameter (`const EncoderSample&`), or on a member function (`double effort() const` promises not to change the object it is called on). It costs nothing when the program runs. It pays when the program is read: a `const&` parameter tells whoever reads a 2,000-line driver that this call cannot change the argument. The ROS 2 client library states message ownership the same way — a subscription callback declared with `const std_msgs::msg::String & msg` receives the message by reference and promises not to modify it ([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]).

**What each costs at 200 Hz.** A by-value `EncoderSample` copies 16 bytes per call, 3,200 bytes a second at one call per tick, and the whole five-sample ring by value is 96 bytes per call — still no allocation, because the ring's storage is inside the object (§6). A `std::vector<EncoderSample>` holding every sample of a 60 s run is another matter: by value at the end of the run it is $12{,}000\times16=192{,}000$ bytes and one heap allocation per call, 38.4 MB and 200 allocations a second, which the Worked case counts and §9 times. A `const&` to any of them passes one address, 8 bytes. The C++ Core Guidelines put the rule as F.16: for "in" parameters, pass cheaply copied types by value and others by reference to `const`.

> **Pointer, defined.** A **pointer** is *an object whose value is an address*, of a compound type written `T*`; it is not the object it points to, and not a reference. Three defining conditions. It is **itself an object**: it has its own storage — 8 bytes on the platforms of this page — its own lifetime, and it can be reassigned to point elsewhere. Its value is **one of four kinds**: a pointer to an object or a function, a pointer one past the end of an array, the null pointer value, or an invalid pointer value, such as one whose object's storage has been released. And **reading or writing through it is defined only for the first kind**: `*p` or `p->counts` on a null, invalid or past-the-end pointer is undefined behaviour, which the program must rule out itself, usually with a check.
>
> $$\mathrm{addr}(p+i)=\mathrm{addr}(p)+i\,\mathrm{sizeof}(T),\qquad 0\le i\le n$$
>
> where $p$ points to element 0 of an array of $n$ elements of type $T$ and $i$ is an index — so pointer arithmetic moves in whole elements, and $p+n$ may be formed but not read through, since it points one past the end.
>
> - **Example**: a `const EncoderSample*` into an array of P6's five samples: `p + 1` is 16 bytes further on, at the next sample, and `p + 5` marks the end. In the listing, `metres_if_valid(&s, &p)` received two pointers and read through both; `metres_if_valid(nullptr, &p)` returned `false` because the callee checked first.
> - **Non-example**: a reference. It has no null value, cannot be re-bound and needs no check, which is why F.16 prefers `const&` for an argument that must exist and keeps pointers for the case where "none" is a legal answer.
> - **Why it matters**: drivers, C libraries and every `->` in rclcpp code hand you pointers, and the two ways they fail on a robot — null and dangling — both fail as undefined behaviour, which §10's sanitizers exist to catch.

> **Reference, defined.** A **reference** is *an alias*: a second name for an object that already exists, declared as `T&` or `const T&`. It is not an object, and it may occupy no storage at all. Four defining conditions. It is **bound when it is initialized**, to a valid object; there is no null reference and no uninitialized one. It is **never re-bound**: assigning to `r` writes to the object `r` names. It has **its object's identity**: the address of `r` and the size of `r` are the address and the size of that object. And a **reference to const** forbids writes through it and can bind to a temporary — in a local declaration, extending the temporary's lifetime to its own.
>
> $$\&r=\&x,\qquad \mathrm{sizeof}(r)=\mathrm{sizeof}(x)$$
>
> where $r$ is a reference bound to the object $x$ — so a `const&` parameter costs no copy however large $x$ is, since the callee works on $x$ itself.
>
> - **Example**: `metres(const EncoderSample& s)` works on the caller's 16-byte sample in place. Inside it, `&s` is the caller's `&s`, and `sizeof(s)` is 16, not the size of an address.
> - **Non-example**: `const EncoderSample& s = latest();`, where `latest()` returns a reference to its own local variable (§2). The reference is bound, but to an object whose lifetime ended as `latest` returned: a dangling reference. Being a reference guarantees that the name was bound, not that its object is still alive.
> - **Why it matters**: `const&` is how a tick reads a message, a buffer or a trajectory without copying it, and the dangling reference is what forgetting whose object it is costs.

### 2. Object lifetime: stack, heap, and the dangling reference

*In one sentence:* the classic C++ crash is using an object after it is gone: every object exists from the end of its construction to the start of its destruction, its storage duration decides when those two moments come — the closing brace for a local, `delete` or the end of its owner for a heap object — and a reference or pointer used after the second moment is dangling, and using it is undefined behaviour.

The language gives every object one of four storage durations. **Automatic**: variables declared in a block without `static`, function parameters and temporaries; their storage lasts until the block exits, and they are destroyed at the closing brace in the reverse of the order they were made. **Static**: variables at namespace scope and `static` locals, alive for the whole program. **Thread**: `thread_local` variables, one per thread. **Dynamic**: objects made by `new`, which live until `delete` — or, in the code on this page, until the object that owns them ends. The standard defines these durations without saying where the storage is; stack and heap are the usual answers. Automatic objects live in their function's frame on the call stack, released when the function returns, and dynamic objects in memory the allocator hands out on request. The words are used below in that sense.

In the tick of §9, `const double p = ...` is automatic: it exists from its line to the closing brace, a few nanoseconds later. The controller is automatic in `main` in §9's test run, so it lives for the whole run. The motor it owns and its log storage are dynamic: allocated once before the loop, released when the controller is destroyed.

**Why robot code almost never writes `new` or `delete`.** `new T(args)` allocates storage and constructs a `T` in it; `delete p` destroys the object and releases the storage. Every `new` needs exactly one `delete` on every path out of the code that made it — the normal return, each early `return`, each exception — and nothing makes the compiler check the pairing. One missing `delete` leaks; one extra is undefined behaviour. §4 and §5 hand that bookkeeping to objects whose destructors do it: a container for many objects, `std::unique_ptr` for one, `std::shared_ptr` where ownership really is shared. After that, a `new` in a code review is a question, and a `delete` is almost always a bug.

**The first dangling reference: a reference to a local, returned.** Deliberately wrong:

```cpp
// deliberately wrong: returns a reference to a local that dies at the closing brace
#include <cstdint>
#include <cstdio>

struct EncoderSample { std::int64_t stamp_ns; std::int32_t counts; bool valid; };

EncoderSample read_encoder() { return {5'000'000, 819, true}; }   // stand-in for the driver call

const EncoderSample& latest() {
  EncoderSample s = read_encoder();             // s lives in latest's stack frame
  return s;                                     // the frame is gone when the caller reads s
}

int main() {
  const EncoderSample& s = latest();            // dangling from its first use
  std::printf("%d counts\n", s.counts);
}
```

```text
return_local.cpp:11:10: warning: reference to stack memory associated with local variable 's' returned [-Wreturn-stack-address]
   11 |   return s;                                     // the frame is gone when the caller reads s
      |          ^
```

The compiler sees it, and this warning is on by default. Run it anyway and, on this Mac, it prints `819 counts` — the right number, read from the frame of a function that had already returned, because nothing had yet overwritten it. That is the dangerous half of undefined behaviour: it can look right. Run it with `ASAN_OPTIONS=detect_stack_use_after_return=1`, which is the default on Linux, and AddressSanitizer stops it at the read:

```text
==86024==ERROR: AddressSanitizer: stack-use-after-return on address 0x000102e55028 ...
READ of size 4 at 0x000102e55028 thread T0
    #0 0x000100bb8b50 in main+0xd8 (return_local:arm64+0x100000b50)
...
Address 0x000102e55028 is located in stack of thread T0 at offset 40 in frame
    #0 0x000100bb88cc in latest()+0xc (return_local:arm64+0x1000008cc)

  This frame has 1 object(s):
    [32, 48) 's' <== Memory access at offset 40 is inside this variable
```

A read of 4 bytes at offset 40 of `latest()`'s frame, where `s` occupied bytes 32 to 48: the read of `counts`, which sits 8 bytes into the sample. The fix is to return the 16-byte sample by value. The C++ Core Guidelines state the rule as F.43: never return a pointer or a reference to a local object.

**The second: a callback that outlives its object.** A robot program registers callbacks with things that live longer than the code that registers them — an executor, a driver's event list, a thread. A callback that captured `this` is then a pointer to an object whose lifetime nothing ties to the callback's. Deliberately wrong:

```cpp
// deliberately wrong: a callback that outlives the object it captured
#include <cstdio>
#include <functional>
#include <memory>
#include <vector>

struct Scheduler {                              // lives for the whole run, as an executor does
  std::vector<std::function<void()>> callbacks;
  void run_once() { for (auto& cb : callbacks) cb(); }
};

class GoalFilter {                              // smooths P6's 50 Hz goal
 public:
  explicit GoalFilter(Scheduler& s) {
    s.callbacks.push_back([this] { update(); });  // the scheduler now holds a raw this
  }
  void update() { filtered_ += 0.2 * (raw_ - filtered_); }
  double filtered() const { return filtered_; }
 private:
  double raw_ = 0.40;                           // metres
  double filtered_ = 0.0;
};

int main() {
  Scheduler scheduler;
  auto filter = std::make_unique<GoalFilter>(scheduler);
  scheduler.run_once();                         // fine: the filter is alive
  std::printf("filtered goal %.3f m\n", filter->filtered());
  filter.reset();                               // the filter is destroyed; its callback is not
  scheduler.run_once();                         // update() runs on freed memory
  std::printf("second run done\n");
}
```

The first `run_once()` works and prints the filtered goal, `0.080 m`: one step of 0.2 towards 0.40 m. Then `filter.reset()` destroys the filter, and the scheduler, which still holds the lambda, calls `update()` on freed memory. §10 shows AddressSanitizer's report. Without the sanitizer the update writes into whatever the allocator has put there since. There are two fixes: make the owner of the object also the owner of the registration, so that the two end together, or have the callback hold a `std::weak_ptr` and check it (§5). The usual rclcpp pattern is the first: the timer a node creates is kept alive by a member of that node, so a timer callback that captures `this` cannot outlive the node (§5). The danger is a callback handed to anything else — a driver's thread, another node, a global list.

> **Object lifetime, defined.** The **lifetime** of an object is *the interval of a program's execution during which the object exists* — a property of each object, set by its **storage duration**, the rule that decides when its storage is obtained and released. It is not the scope of a name: a name is visible in a stretch of code, an object exists for a stretch of time. Three defining conditions. It **begins** when storage of the right size and alignment has been obtained and the object's initialization — for a class, its constructor — has completed. It **ends** when the destructor call starts, for a class type, or when the storage is released or reused. And using the object **outside that interval** through a reference or a pointer — reading it, writing it, calling a member function on it — is undefined behaviour, whatever value happens to be found there.
>
> $$\text{a use of } x \text{ at time } t \text{ is defined}\iff t_{\text{init}}(x)\le t<t_{\text{destroy}}(x)$$
>
> where $t_{\text{init}}$ is the moment $x$'s initialization completes and $t_{\text{destroy}}$ the moment its destruction starts — so a reference can outlive its object, since nothing in the language shortens a reference when its object ends.
>
> - **Example**: the controller in §9's test run is automatic in `main`. Its $t_{\text{init}}$ is its declaration and its $t_{\text{destroy}}$ the closing brace of `main`, 12,000 ticks later; its log storage is dynamic and lives exactly as long, because the controller owns it.
> - **Non-example**: the sample `s` inside `latest()`. Its lifetime ends at `latest`'s closing brace, before the caller's first read; the caller's reference is dangling, and the correct 819 printed on this Mac does not make the read defined.
> - **Why it matters**: the lifetimes that matter in a robot program belong to callbacks, threads and drivers, which outlast the code that set them up, and every use-after-free a sanitizer finds is a lifetime someone assumed.

> **Undefined behaviour, defined.** **Undefined behaviour** is *a category the C++ standard assigns to certain operations: for an execution that performs one, the standard places no requirement on what the program does*. It is a property of an operation in an execution, not an error message. Three defining conditions. The operation is **one the standard names as undefined**: using an object outside its lifetime, reading through a null pointer, indexing outside an array, signed integer overflow, a data race between threads, deleting a derived object through a base class that lacks a virtual destructor (§7). **No diagnosis is required**: the compiler need not warn, and the program need not crash. And **the compiler may assume it never happens**, and optimizes on that assumption, so its effects can move, vanish or change with the optimization level. Two neighbouring categories are different. *Implementation-defined* behaviour varies between platforms, but each documents its choice — the size of `bool` is one. *Unspecified* behaviour is one of several allowed outcomes, without saying which — the order in which a function's arguments are evaluated is one.
>
> $$\exists\,k:\ \mathrm{op}_k\ \text{undefined}\ \Rightarrow\ \text{no requirement on that execution}$$
>
> where $\mathrm{op}_k$ is the $k$-th operation of one execution with one input — so an execution is only as defined as its worst operation, since one undefined operation removes every requirement on it.
>
> - **Example**: `return_local` printed `819 counts` in a plain run on this Mac and was stopped by AddressSanitizer in an instrumented one. Both are allowed, and neither is "the" behaviour.
> - **Non-example**: an exception. The `throw` in §4's listing is fully defined: the stack unwinds, destructors run, a handler catches it. Undefined behaviour has no such mechanism.
> - **Why it matters**: on a robot, undefined behaviour is the defect that passes the bench test and fails in the field, because what it does depends on what happens to be in memory. Warnings and sanitizers (§10) find much of it; nothing finds all of it.

> [!note]- Deeper · 더 깊이
> **How far back undefined behaviour reaches.** In C++17 the standard places no requirement even on what the program did before the undefined operation ([intro.execution]/5 of the C++17 standard, N4659); the current working draft narrows this and keeps the observable behaviour before it ([intro.abstract]/6).

### 3. Memory layout: sizeof, alignment and padding

*In one sentence:* a sample costs more bytes than its fields add up to, because every type has a size and an alignment, a struct places its members in declaration order at offsets that are multiples of their alignments and rounds its own size up to a multiple of its largest alignment — so the order of the fields decides how many bytes of padding a sample carries through every buffer, log and copy.

`sizeof(T)` is the number of bytes an object of type `T` occupies, padding included, and `alignof(T)` its alignment: an object of type `T` may start only at an address that is a multiple of it. The language fixes very little of this — the members of a class are allocated in declaration order, and not much more — and the rest belongs to the platform's ABI, the binary conventions its compilers agree on. On the platforms robot computers run, x86-64 and ARM64 Linux, and on the Apple laptop that ran this page's listings, the types used here agree: `bool` is 1 byte, `std::int32_t` 4, `std::int64_t`, `double` and every pointer 8, each aligned to its own size. Two rules then turn member sizes into a struct size: a struct is aligned like its most-aligned member, and its size is the smallest multiple of that alignment that holds all its members.

> [!note]- Deeper · 더 깊이
> **What the language fixes, and what the ABI adds.** `sizeof` of the narrow character types (`char` and its signed and unsigned forms) is 1; the size of every other fundamental type is implementation-defined; every alignment is a power of two; and the members of a class are allocated in declaration order, each at a higher address than the one before. The rest is the ABI's — the System V x86-64 psABI for x86-64 Linux, Arm's AAPCS64 for ARM64 Linux — and both documents state the two struct rules in nearly the same words. The three platforms were checked by compiling the same `static_assert`s for each target with clang.

```cpp
// layout.cpp - P6's encoder sample, byte by byte, in two field orders
#include <cstddef>
#include <cstdint>
#include <cstdio>

struct SampleAsWritten {            // the order a first draft uses
  bool valid;                       // false if the read failed
  std::int64_t stamp_ns;            // time of the read, nanoseconds
  std::int32_t counts;              // encoder counts, 2048 per metre
};

struct EncoderSample {              // the same three fields, largest alignment first
  std::int64_t stamp_ns;
  std::int32_t counts;
  bool valid;
};

int main() {
  std::printf("as written : size %zu, align %zu, offsets valid %zu stamp_ns %zu counts %zu\n",
              sizeof(SampleAsWritten), alignof(SampleAsWritten),
              offsetof(SampleAsWritten, valid), offsetof(SampleAsWritten, stamp_ns),
              offsetof(SampleAsWritten, counts));
  std::printf("reordered  : size %zu, align %zu, offsets stamp_ns %zu counts %zu valid %zu\n",
              sizeof(EncoderSample), alignof(EncoderSample),
              offsetof(EncoderSample, stamp_ns), offsetof(EncoderSample, counts),
              offsetof(EncoderSample, valid));
  const std::size_t payload = sizeof(bool) + sizeof(std::int64_t) + sizeof(std::int32_t);
  std::printf("payload %zu bytes; padding %zu as written, %zu reordered\n", payload,
              sizeof(SampleAsWritten) - payload, sizeof(EncoderSample) - payload);
  std::printf("five samples: %zu bytes as written, %zu reordered\n",
              sizeof(SampleAsWritten[5]), sizeof(EncoderSample[5]));
}
```

```text
as written : size 24, align 8, offsets valid 0 stamp_ns 8 counts 16
reordered  : size 16, align 8, offsets stamp_ns 0 counts 8 valid 12
payload 13 bytes; padding 11 as written, 3 reordered
five samples: 120 bytes as written, 80 reordered
```

Walk through the first order. `valid` sits at offset 0 and takes 1 byte. `stamp_ns` needs an offset that is a multiple of 8, so it goes to 8, and bytes 1 to 7 are padding. `counts` needs a multiple of 4, and 16 is one, so it takes bytes 16 to 19. The members end at 20, but the struct's alignment is 8, so its size rounds up to 24, and bytes 20 to 23 are tail padding: 13 bytes of data in 24. Reordered, `stamp_ns` takes 0 to 7, `counts` 8 to 11, `valid` byte 12, and the size rounds 13 up to 16. The tail padding exists for arrays. Every element of an array of samples must start at a multiple of 8, which is why `sizeof` includes it and why five samples are exactly five times `sizeof`: 120 bytes against 80.

Largest alignment first is the rule of thumb, and here it gives the smallest size there is. It does not always remove padding: no order can make a struct smaller than its payload rounded up to its alignment, $\lceil 13/8\rceil\cdot 8=16$ bytes here, so this sample now carries the minimum, 3 bytes. Problem 1's IMU sample is a case where the minimum still leaves a byte over.

What the sample's size decides, on P6. The ring buffer of §6 holds five samples in place plus two 8-byte indices, $5\cdot16+16=96$ bytes against $5\cdot24+16=136$ as first written. A `TickRecord` is four 8-byte fields and has no padding at all, 32 bytes, so the 60 s log is $12{,}000\cdot32=384{,}000$ bytes. At 200 Hz the stream of samples is $16\cdot200=3{,}200$ bytes per second against $4{,}800$: a third of every buffer, log and copy of the first version was padding.

One more consequence, more dangerous than the bytes. A struct's raw bytes are not a file format or a wire format. The padding bytes are not part of the value — they hold nothing meaningful — and the layout belongs to one ABI, so the same bytes written by one program can be read wrongly by another built differently. ROS 2 messages are serialized by the middleware for this reason ([[04-robotics/ros2/nodes-topics-messages|25.2 §4]] reads a message definition), and a log written to disk should be written field by field or through a serialization library.

> **Alignment and padding, defined.** The **alignment** of a type is *the number of bytes between successive addresses at which objects of that type may be allocated* — an implementation-defined power of two, a property of the type on a given ABI. **Padding** is *the bytes of an object that belong to none of its members*, inserted to meet those alignments. Three defining conditions fix a struct's layout on the ABIs of this page; the language itself guarantees only the order. Its members are **placed in declaration order**, each at the lowest offset, at or after the end of the member before it, that is a multiple of its own alignment. The struct's **alignment is the largest of its members' alignments**. And its **size is rounded up** to a multiple of that alignment, so that every element of an array of it is aligned too.
>
> $$o_1=0,\quad o_i=\Big\lceil\frac{o_{i-1}+s_{i-1}}{a_i}\Big\rceil a_i,\qquad \mathrm{sizeof}(S)=\Big\lceil\frac{o_n+s_n}{a_S}\Big\rceil a_S,\quad a_S=\max_i a_i$$
>
> where $s_i$, $a_i$ and $o_i$ are the size, the alignment and the offset of the $i$-th of the struct's $n$ members — so the padding is whatever the ceilings add, and it depends on the order because each offset depends on the member before it.
>
> - **Example**: as first written, $o=0,8,16$, the members end at $16+4=20$, $a_S=8$ and $\lceil 20/8\rceil\cdot 8=24$ bytes, 11 of them padding. Reordered, $o=0,8,12$, the end is $13$ and $\lceil 13/8\rceil\cdot 8=16$, with 3 of padding. `layout.cpp` printed both.
> - **Non-example**: "a struct is the sum of its members". That gives 13 bytes for either order, and the compiler agrees with neither.
> - **Non-example**: a layout carried from one platform to another. The formula is general but its $s_i$ and $a_i$ are not: the language fixes the bit widths of `std::int32_t` and `std::int64_t` but none of the alignments, so a sample layout computed for x86-64 is a claim about x86-64.
> - **Why it matters**: every sample is copied into a ring, appended to a log and often sent; its padding is paid at the sample rate — $(24-16)\cdot200=1{,}600$ bytes a second here — and its layout decides whether two programs can share its bytes at all.

### 4. Classes, invariants and RAII

*In one sentence:* a resource such as an enabled drive must be released on every way out of the code that acquired it, and C++ does it with classes: a class bundles data with the functions that keep a condition true of it, its constructor establishes that condition and its destructor ends it, and RAII uses the pairing to tie the resource to an object, so that it is released on every path out of the object's scope.

A class declares data members and member functions, and its `private:` members can be touched only by its own functions. The point is an **invariant**: a condition true of every object of the class between calls to its member functions. For P6's drive, "the port is open and the drive enabled exactly while this object exists" is one. The **constructor** establishes the invariant before anyone can call anything. It initializes the members in the order they are declared in the class, whatever order its member initializer list is written in — clang's `-Wall` flags a list written in another order (`-Wreorder-ctor`), because a member initialized from one declared after it reads a value that does not exist yet. The **destructor** runs when the object's lifetime ends: at the closing brace of its scope, at `delete`, or during stack unwinding, when an exception passes through the scope. It runs its body, then destroys the members in the reverse order of their declaration.

RAII — resource acquisition is initialization — is that pairing used for resources. The listing is P6's drive as a class; its port calls are stand-ins that print, where a real driver would write to its port.

```cpp
// raii.cpp - P6's drive owned by one object, released on every way out of a scope
#include <cstdio>
#include <stdexcept>

class MotorDriver {
 public:
  explicit MotorDriver(const char* port) : port_(port) {
    std::printf("  %s: open, enable\n", port_);        // real code: open the port, enable the stage
  }
  ~MotorDriver() {                                     // runs however the owner's scope ends
    set_effort(0.0);
    std::printf("  %s: effort %.1f, disable, close\n", port_, effort_);
  }
  MotorDriver(const MotorDriver&) = delete;            // one drive, one owner
  MotorDriver& operator=(const MotorDriver&) = delete;

  void set_effort(double effort) { effort_ = effort; } // real code: write to the bus

 private:
  const char* port_;
  double effort_ = 0.0;
};

int run(int ticks, int fail_at) {                      // the loop, with two early ways out
  MotorDriver drive("cart0");
  for (int k = 0; k < ticks; ++k) {
    drive.set_effort(0.25);
    if (k == fail_at) throw std::runtime_error("encoder read failed");
    if (k == 2) return k;                              // an early return
  }
  return ticks;
}

int main() {
  std::printf("normal end:\n");
  run(2, -1);
  std::printf("early return:\n");
  run(5, -1);
  std::printf("exception:\n");
  try {
    run(5, 1);
  } catch (const std::exception& e) {
    std::printf("  caught: %s\n", e.what());
  }
}
```

```text
normal end:
  cart0: open, enable
  cart0: effort 0.0, disable, close
early return:
  cart0: open, enable
  cart0: effort 0.0, disable, close
exception:
  cart0: open, enable
  cart0: effort 0.0, disable, close
  caught: encoder read failed
```

Three ways out of `run`, and on each the drive is commanded to zero and disabled, once: at the end of the loop, at the early `return` of tick 2, and when the exception thrown at tick 1 passes through `run` on its way to the handler in `main`. The last line pair shows the order: the drive is released before `caught` is printed, because the stack is unwound, and every automatic object between the `throw` and the handler destroyed, before the handler runs. No line of `run` mentions shutdown; its scope does it.

What RAII cannot do: it runs only when the language leaves a scope. `std::exit` does not unwind the stack, so automatic objects are not destroyed; `std::abort` destroys nothing; whether an uncaught exception unwinds the stack before `std::terminate` is implementation-defined; and a crash, a `SIGKILL` or a power cut runs nothing at all. A real drive therefore also needs a watchdog that disables it when commands stop arriving, and an emergency stop, below all software. What rclcpp does do is install handlers for SIGINT and SIGTERM by default — the Jazzy `rclcpp::init` takes `SignalHandlerOptions::All` unless told otherwise — so Ctrl-C shuts the context down, `spin` returns, `main` returns, and the destructors run.

**Copying a resource owner is a bug.** The compiler writes a copy constructor for any class that does not declare one, even for a class with a user-written destructor, where C++11 already deprecated doing so. A copy of `MotorDriver` shares the port with the original and runs the destructor a second time. Deliberately wrong:

```cpp
// deliberately wrong: the driver can be copied, and a copy's destructor disables the drive
#include <cstdio>

class MotorDriver {
 public:
  explicit MotorDriver(const char* port) : port_(port) { std::printf("%s: open, enable\n", port_); }
  ~MotorDriver() { effort_ = 0.0; std::printf("%s: effort 0, disable, close\n", port_); }
  void set_effort(double effort) { effort_ = effort; }
 private:
  const char* port_;
  double effort_ = 0.0;
};

void log_status(MotorDriver d) { (void)d; }   // by value: a second owner, for one call

int main() {
  MotorDriver drive("cart0");
  drive.set_effort(0.25);
  log_status(drive);                          // the copy dies here and disables the drive
  drive.set_effort(0.30);                     // the loop goes on commanding a disabled drive
  std::printf("still commanding cart0\n");
}
```

```text
cart0: open, enable
cart0: effort 0, disable, close
still commanding cart0
cart0: effort 0, disable, close
```

The copy made for `log_status` dies as the call returns and disables the drive; the loop then commands a disabled drive, and the original disables it a second time at the end. `-Wall -Wextra` say nothing about it. `-Wdeprecated` does:

```text
raii_copy_wrong.cpp:7:3: warning: definition of implicit copy constructor for 'MotorDriver' is deprecated because it has a user-provided destructor [-Wdeprecated-copy-with-user-provided-dtor]
```

The fix is the two `= delete` lines that `raii.cpp` already has. With them the by-value call no longer compiles — `error: call to deleted constructor of 'MotorDriver'` — and a compile error is where this bug should be found. ros2_control's hardware components do exactly this: in Jazzy, `hardware_interface::HardwareComponentInterface` deletes its copy and move constructors, and its comment gives the reason — a hardware interface has one owner, so that the hardware is never accessed twice at once.

The general form is the **rule of zero**. A class that owns a resource directly declares its destructor and its copy and move operations, deleting the ones it cannot support. Every other class declares none of them and lets its members' own do the work. `CartController` in §9 declares none: its `std::unique_ptr` member is already impossible to copy, so the controller is too, and it needs no destructor body because each member releases itself.

> **RAII, defined.** **RAII** (resource acquisition is initialization) is *a technique that binds the life of a resource to the lifetime of an object* — a way of writing classes, not a library, and not garbage collection. Four defining conditions. The **constructor acquires** the resource and establishes the class invariant, or throws if it cannot, so that no object exists without its resource. The **destructor releases** it and does not throw. The owning object **has automatic storage duration**, or is owned by something that has, so that leaving its scope by any route the language knows — a return, an exception, the end of `main` — runs the destructor. And **copies are either correct or deleted**, so that each acquisition has exactly one release.
>
> $$n_{\text{release}}=n_{\text{acquire}}\ \text{ on every path out of a scope, releases in reverse order of acquisition}$$
>
> where $n$ counts the resources acquired and released by the objects of one scope — so a function with several exits needs release code at none of them, since the end of the scope is the one place where release happens.
>
> - **Example**: `raii.cpp` acquired the drive three times and released it three times, once for each way out — the end of the loop, the early return, the exception — and printed each pair.
> - **Non-example**: the copyable `MotorDriver`. One acquisition and two releases, $2\ne1$, and the first release lands in the middle of the run.
> - **Non-example**: a kill signal, `std::abort` or a power cut. No scope is left by the language, no destructor runs, and the drive stays as it was last commanded — which is why RAII is the first shutdown path, not the only one.
> - **Why it matters**: the cart is commanded to zero and disabled whenever the software stops itself, however it stops, without a line of shutdown code in the loop.

### 5. Ownership: unique_ptr, shared_ptr, weak_ptr

*In one sentence:* every heap object needs one answer to "who destroys it?", and its owner is whatever is responsible for that; `std::unique_ptr` makes that one owner, `std::shared_ptr` shares it among several with a use count and destroys the object when the count reaches zero, and `std::weak_ptr` observes without owning — which is how the cycle that keeps a node, and the drive it owns, alive forever is broken.

Every heap object in a program needs exactly one answer to "who destroys it?", and modern C++ writes the answer into the type.

- `std::unique_ptr<T>` is **unique ownership**: exactly one owner, which deletes its object when it is itself destroyed, reset or assigned another pointer. It cannot be copied, only moved, and after a move the source is empty, so there is always one place to look to know when an object dies. `std::make_unique<T>(args)` creates the object and its owner together — never make two `unique_ptr`s from one raw pointer, since each would delete it. With this machine's standard library it is 8 bytes, the size of the pointer it holds.
- `std::shared_ptr<T>` shares ownership through a use count kept in a control block, and destroys the object when the count reaches zero (the box at the end of this section defines it). `std::make_shared` allocates the object and its control block in one allocation; a typical `shared_ptr` holds two pointers — 16 bytes here — and updates its count atomically, so copies used in different threads are safe, though one `shared_ptr` object used from two threads at once is not.
- `std::weak_ptr<T>` observes a shared object without owning it. `lock()` returns a `shared_ptr` that keeps the object alive while it is in use, or an empty one if the object is gone.
- A raw `T*` or `T&` in such code owns nothing: it observes an object whose owner is elsewhere and must outlive the observer. In §9's test run, `const SimMotor* sim = motor.get();` observes the motor that the controller owns.

**Moving, in one paragraph.** `CartController controller(std::move(motor), kTicks);` in §9 hands the drive to the controller. `std::move` moves nothing by itself: it is a cast that lets the argument bind to a move constructor, and `unique_ptr`'s move constructor takes the pointer over and leaves `motor` empty, so a later line that reads through `motor` reads through a null pointer. Moved-from objects of the standard library are left in a valid but unspecified state in general; a moved-from `unique_ptr` is specified to be empty. That is all the move semantics this page needs: ownership that cannot be copied is transferred with `std::move`, and the moved-from name is not used again.

**How rclcpp uses `SharedPtr`**, as read from its Jazzy branch. `rclcpp::Node::SharedPtr` is `std::shared_ptr<rclcpp::Node>` and nothing more. `create_wall_timer` returns a `SharedPtr` to a timer that keeps the callback — with everything the callback captured — as a member, and the node's callback group keeps only `WeakPtr`s to its timers, so the `SharedPtr` you store in a member is what keeps a timer alive: drop it and the timer is destroyed, which is why [[04-robotics/ros2/nodes-topics-messages|25.2 §6]] stores its timer as a member. And `rclcpp::spin` takes the node's `SharedPtr` by value, one more owner while it runs. The listing rebuilds that ownership with the standard library alone, and counts it; the `shared_from_this()` it uses returns a `shared_ptr` to the object itself, provided one already owns it:

```cpp
// ownership.cpp - who keeps P6's controller node alive, counted
#include <cstdio>
#include <functional>
#include <memory>
#include <vector>

struct Timer {                                  // a wall timer, reduced to what it owns
  std::function<void()> callback;               // the callback, with everything it captured
};

struct Executor {                               // observes timers, as rclcpp's callback groups do
  std::vector<std::weak_ptr<Timer>> timers;
  void spin_once() {
    for (auto& w : timers)
      if (auto t = w.lock()) t->callback();     // run it only if someone still owns it
  }
};

class CartNode : public std::enable_shared_from_this<CartNode> {
 public:
  ~CartNode() { std::printf("  ~CartNode: effort 0, drive disabled\n"); }
  void start(Executor& ex, bool capture_self) {
    timer_ = std::make_shared<Timer>();         // the node owns its timer
    if (capture_self) {
      auto self = shared_from_this();           // an owning copy of the node...
      timer_->callback = [self] { self->tick(); };  // ...stored inside the node's own timer
    } else {
      timer_->callback = [this] { tick(); };    // observing: the timer cannot outlive the node
    }
    ex.timers.push_back(timer_);
  }
  void tick() { ++ticks_; }

 private:
  std::shared_ptr<Timer> timer_;
  int ticks_ = 0;
};

void spin(std::shared_ptr<CartNode> node, Executor& ex) {  // by value, like rclcpp::spin
  std::printf("  inside spin: %ld\n", node.use_count());
  ex.spin_once();
}

int main() {
  for (bool capture_self : {false, true}) {
    std::printf("callback captures %s\n", capture_self ? "shared_from_this():" : "this:");
    Executor ex;
    std::weak_ptr<CartNode> watch;
    {
      auto node = std::make_shared<CartNode>();
      watch = node;
      std::printf("  after make_shared: %ld\n", node.use_count());
      node->start(ex, capture_self);
      std::printf("  after start: %ld\n", node.use_count());
      spin(node, ex);
      std::printf("  after spin: %ld\n", node.use_count());
    }                                           // main's shared_ptr is destroyed here
    std::printf("  after main lets go: %ld, %s\n", watch.use_count(),
                watch.expired() ? "destroyed" : "never destroyed");
  }
}
```

```text
callback captures this:
  after make_shared: 1
  after start: 1
  inside spin: 2
  after spin: 1
  ~CartNode: effort 0, drive disabled
  after main lets go: 0, destroyed
callback captures shared_from_this():
  after make_shared: 1
  after start: 2
  inside spin: 3
  after spin: 2
  after main lets go: 1, never destroyed
```

With `this` captured, the use count goes 1, 1, 2 while `spin` holds its copy, back to 1, and to 0 when `main` lets go; the node is destroyed and its destructor zeroes the drive. With `shared_from_this()` captured, the lambda stored inside the node's own timer is a second owner of the node, so the count never falls below 1: 1, 2, 3 inside `spin`, 2, and 1 when `main` lets go. Nothing outside the node refers to it any more, yet the node owns the timer, the timer owns the callback and the callback owns the node — a cycle. The destructor never runs, and neither does anything that depends on it, the drive's shutdown included. On Linux, where AddressSanitizer's leak checker is on by default, the leaked node would be reported when the program exits; on this Mac the leak checker is not supported, and the run prints `detect_leaks is not supported on this platform` when asked for it.

The fixes. Capture `this` when the object owns whatever holds the callback, as here — the Jazzy C++ tutorial writes its timer callback as `[this]() -> void {...}` for that reason. Capture a `std::weak_ptr` and `lock()` it inside the callback when the object might not outlive the holder. And prefer `unique_ptr` wherever one owner is the truth: a `shared_ptr` is an admission that no single object decides when something ends, and each one is a count someone must be able to trace.

> [!note]- Deeper · 더 깊이
> **Where rclcpp's pointer types come from.** rclcpp's classes declare them with one family of macros, `RCLCPP_SMART_PTR_DEFINITIONS` and its variants, which define `SharedPtr` as `std::shared_ptr` of the class, `WeakPtr` as `std::weak_ptr` and `UniquePtr` as `std::unique_ptr`. `rclcpp::Node` derives from `std::enable_shared_from_this<Node>`, which is what lets a node call `shared_from_this()` — and so what makes the cycle above possible in real rclcpp code.

> **Shared ownership and reference counting, defined.** **Shared ownership** is *the relation in which several objects own one jointly, and it is destroyed when the last of them lets go*; `std::shared_ptr<T>` implements it with a **use count** kept in a control block. It is not garbage collection: nothing searches for objects that cannot be reached. Four defining conditions. Every **copy increments** the use count, and every destruction, reset or reassignment of an owner **decrements** it. The object is **destroyed when the use count reaches zero**. A `std::weak_ptr` **does not count**, and can be turned into an owner with `lock()` only while the object lives. And a **cycle** of owners — A owns B, B owns A — keeps every count in it at 1 or more for good.
>
> $$u(t)=\#\{\text{shared\_ptr objects owning } x \text{ at } t\},\qquad t_{\text{destroy}}(x)=\min\{\,t: u(t)=0\,\}$$
>
> where $u$ is the use count of the object $x$ — so the object's life is decided by the last owner to go, and is finite only if every owner eventually goes.
>
> - **Example**: the node of `ownership.cpp` capturing `this`. Its use count ran 1, 1, 2 inside `spin`, 1, 0, and the destructor ran at the step to 0.
> - **Non-example**: the same node capturing `shared_from_this()`: 1, 2, 3, 2, 1. The count never reaches 0 because one owner sits inside the object it owns; `this` or a `weak_ptr` breaks the cycle.
> - **Why it matters**: rclcpp hands out nodes, publishers, subscriptions and timers as `shared_ptr`s, so on a ROS 2 robot the moment a node ends — and with it the moment its drive is shut down — is a use count reaching zero.

### 6. Templates and the standard containers

*In one sentence:* a control loop needs containers whose storage does not grow while it runs: a template is a pattern the compiler turns into a separate class for every set of arguments, which is how one `RingBuffer<T, N>` serves any sample type with its storage fixed at compile time, and the standard containers built the same way differ in the one thing a control loop cares about — whether adding an element can allocate.

`template <typename T, std::size_t N> class RingBuffer` declares a family of classes. `T` is a type parameter and `N` a constant parameter, an integer the compiler must know. `RingBuffer<EncoderSample, 5>` and `RingBuffer<EncoderSample, 8>` are two different classes — 96 and 144 bytes — generated from one definition, and the compiler generates code only for the member functions a program uses. It needs the whole definition to do that, at every place a new combination of arguments is used, so a template lives in a header: `ring_buffer.hpp` has no `.cpp`, and neither do most template libraries. The last N samples of a sensor are the standard shape of data in a control loop, and this is the buffer for them:

```cpp
// include/cart/ring_buffer.hpp - the last N items, in storage fixed at compile time
#pragma once
#include <array>
#include <cstddef>

template <typename T, std::size_t N>
class RingBuffer {
  static_assert(N >= 2, "a difference needs at least two items");

 public:
  void push(const T& item) {                    // overwrites the oldest once full
    data_[head_] = item;
    head_ = (head_ + 1) % N;
    if (count_ < N) ++count_;
  }
  std::size_t size() const { return count_; }
  const T& newest() const { return data_[(head_ + N - 1) % N]; }       // needs size() >= 1
  const T& oldest() const { return data_[(head_ + N - count_) % N]; }  // needs size() >= 1

 private:
  std::array<T, N> data_{};                     // inside the object: no heap
  std::size_t head_ = 0;                        // where the next push goes
  std::size_t count_ = 0;                       // items held, at most N
};
```

`data_` is a `std::array<T, N>`, an aggregate that holds a C array `T[N]` as its only member (cppreference). So the samples are inside the `RingBuffer` object — $5\cdot16=80$ bytes — followed by the two indices: 96 bytes, allocated wherever the buffer itself is, and never again. A class holding a `std::vector<EncoderSample>` instead has a `sizeof` of the vector's 24 bytes of pointers whatever the length, because its elements live in a heap block that the vector allocates, and reallocates, while the program runs. `push` writes at `head_`, moves `head_` on modulo `N`, and counts up to `N`; once the buffer is full, each push overwrites the oldest sample. `newest()` is the slot before `head_` and `oldest()` the slot `count_` places back; both return references into the buffer, which read whatever the slot holds when they are used — a later `push` may have overwritten it. `static_assert` stops `RingBuffer<EncoderSample, 1>` at compile time, since a velocity needs two samples. The velocity that P6's controller reads from it is a function template in the same header family, with `N` deduced from its argument:

```cpp
// include/cart/sample.hpp - P6's two records and the velocity they give
#pragma once
#include <cstdint>
#include "cart/ring_buffer.hpp"

struct EncoderSample {                          // 16 bytes (section 3)
  std::int64_t stamp_ns;                        // time of the read, nanoseconds
  std::int32_t counts;                          // encoder counts, 2048 per metre (P6)
  bool valid;                                   // false if the read failed
};

struct TickRecord {                             // one line of the run log, 32 bytes
  std::int64_t stamp_ns;
  double goal_m;
  double position_m;
  double effort;
};

constexpr double kCountsPerMetre = 2048.0;

template <std::size_t N>
double velocity(const RingBuffer<EncoderSample, N>& h) {   // m/s over the whole buffer
  if (h.size() < 2) return 0.0;
  const EncoderSample& a = h.oldest();
  const EncoderSample& b = h.newest();
  return (b.counts - a.counts) / kCountsPerMetre / ((b.stamp_ns - a.stamp_ns) * 1e-9);
}
```

With $K=5$ the velocity is taken over $(K-1)T=20$ ms, one vision period, and one encoder count across that window is $1/(2048\cdot0.020)=0.0244$ m/s, against $1/(2048\cdot0.005)=0.0977$ m/s if the velocity were differenced over a single tick. [[04-robotics/ros2/simulation-and-control|25.7]] meets the same trade between noise and delay from the other side.

**`std::vector` and its capacity.** A vector keeps its elements in one heap block and knows two numbers: `size()`, the elements it holds, and `capacity()`, the elements the block can hold. `push_back` into spare capacity only copies one element. `push_back` into a full vector allocates a larger block, moves the existing elements across, frees the old block and then appends — and every pointer, reference and iterator into the old block now dangles. How much larger is the library's choice. The standard demands only amortized constant time per `push_back`, which forces geometric growth ([[02-foundations/algorithms/data-structures|11.2 §2]] has the argument, [[02-foundations/algorithms/complexity-recursion|11.1 §4]] the accounting). Both libraries a robot computer is likely to use — libc++ with Apple's clang, libstdc++ on Ubuntu — double, so from an empty vector the capacity goes 1, 2, 4, 8 and so on (the callout below gives each library's rule). The run below used libc++:

```cpp
// capacity.cpp - how a 60 s log grows at 200 Hz, with and without reserve
#include <cstdint>
#include <cstdio>
#include <vector>

struct TickRecord { std::int64_t stamp_ns; double goal_m, position_m, effort; };  // 32 bytes

int main() {
  for (bool reserve : {false, true}) {
    std::vector<TickRecord> log;
    if (reserve) log.reserve(12'000);           // before the loop, as a constructor would
    std::printf("%s, capacity after each growth:", reserve ? "reserved" : "not reserved");
    std::size_t growths = 0, moved = 0;
    for (int k = 1; k <= 12'000; ++k) {         // one record per tick
      const std::size_t cap = log.capacity(), n = log.size();
      log.push_back({});
      if (log.capacity() != cap) {              // new storage: allocate, move n records, free
        ++growths;
        moved += n;
        std::printf(" %zu", log.capacity());
      }
    }
    std::printf("\n  %zu growths, %zu records moved, final capacity %zu = %zu bytes\n",
                growths, moved, log.capacity(), log.capacity() * sizeof(TickRecord));
  }
}
```

```text
not reserved, capacity after each growth: 1 2 4 8 16 32 64 128 256 512 1024 2048 4096 8192 16384
  15 growths, 16383 records moved, final capacity 16384 = 524288 bytes
reserved, capacity after each growth:
  0 growths, 0 records moved, final capacity 12000 = 384000 bytes
```

Fifteen allocations of new storage in the first minute, the last and largest at record 8,193, 41 s in, which moved 8,192 records — 262,144 bytes — in one tick. The final block holds 16,384 records, 36.5% more than needed. `reserve(12'000)` allocates the whole block once, before the loop, and after it no `push_back` of the run allocates. Two warnings from cppreference's page on `reserve` go with it: `reserve` before every `push_back` defeats the geometric growth and makes appending slower, and `reserve` is only useful when the final size is known, as a log's length at a known rate is.

> [!note]- Deeper · 더 깊이
> **How each library grows.** In their current sources, libc++ (LLVM's, used by Apple's clang) asks for the larger of twice the capacity and the size needed (`__recommend` in `__vector/vector.h`), and libstdc++ (GCC's, the default on Ubuntu) grows a full vector by its own size for each `push_back` (`_M_check_len` in `bits/stl_vector.h`).

**Two more containers, one sentence each.** `std::unordered_map` is a hash table ([[02-foundations/algorithms/data-structures|11.2 §3]]): lookup, insertion and removal take constant time on average, and an insertion can rehash the whole table. `std::map` is a balanced search tree, usually red–black ([[02-foundations/algorithms/data-structures|11.2 §5]]): it keeps its keys sorted and takes logarithmic time. Both store each element in a node of its own — since C++17 a node can even be extracted and moved to another container — so inserting a new key allocates, and neither is filled inside a tick. Looking a key up with `find` in a map filled before the loop does not allocate; `operator[]` with a missing key inserts it, and does.

### 7. Interfaces: inheritance and virtual

*In one sentence:* the controller must drive a simulated cart and a real one without knowing which: an abstract base class declares what every motor can do as pure virtual functions, `SimMotor` and `RealMotor` implement them, and a call through a `MotorInterface` pointer runs the implementation of whatever object is behind it, chosen at run time for about a nanosecond — provided the base's destructor is virtual, since otherwise deleting through that pointer skips the destructor that shuts the drive down.

The controller should not know whether it is driving a simulated cart or a real one, so it talks to an interface:

```cpp
// include/cart/motor.hpp - the seam between the controller and whatever moves the cart
#pragma once

class MotorInterface {
 public:
  virtual ~MotorInterface() = default;          // delete through a base pointer runs the derived one
  virtual void enable() = 0;
  virtual void disable() = 0;
  virtual void set_effort(double effort) = 0;   // normalized command, -1 to 1
};

class SimMotor final : public MotorInterface {  // for tests and simulation: remembers the command
 public:
  void enable() override { enabled_ = true; }
  void disable() override { enabled_ = false; }
  void set_effort(double effort) override { effort_ = enabled_ ? effort : 0.0; }
  double effort() const { return effort_; }

 private:
  bool enabled_ = false;
  double effort_ = 0.0;
};

class RealMotor final : public MotorInterface { // section 4's driver, behind the interface
 public:
  explicit RealMotor(const char* port);         // opens the port
  ~RealMotor() override;                        // effort 0, disable, close: on every way out
  RealMotor(const RealMotor&) = delete;         // one drive, one owner
  RealMotor& operator=(const RealMotor&) = delete;
  void enable() override;
  void disable() override;
  void set_effort(double effort) override;

 private:
  const char* port_;
  bool enabled_ = false;
  double effort_ = 0.0;
};
```

```cpp
// src/real_motor.cpp - the one translation unit that defines RealMotor
#include "cart/motor.hpp"
#include <cstdio>

// The bus calls are stand-ins that print; a real driver writes to its port here.
RealMotor::RealMotor(const char* port) : port_(port) { std::printf("%s: open\n", port_); }
RealMotor::~RealMotor() {
  set_effort(0.0);
  disable();
  std::printf("%s: effort %.1f, close\n", port_, effort_);
}
void RealMotor::enable() { enabled_ = true; std::printf("%s: enable\n", port_); }
void RealMotor::disable() {
  if (enabled_) std::printf("%s: disable\n", port_);
  enabled_ = false;
}
void RealMotor::set_effort(double effort) { effort_ = enabled_ ? effort : 0.0; }
```

`virtual` marks a function whose version is chosen by the object's type when the program runs; `= 0` makes it **pure**, with no version in the base at all, which makes `MotorInterface` an **abstract class**: no object of it can be made, but pointers and references to it can. `override` asks the compiler to check that a function really does override one in the base — misspell `set_effort` and the build fails instead of quietly adding a new function. `final` forbids further derivation. The controller holds a `std::unique_ptr<MotorInterface>` and calls `motor_->set_effort(u)`, and the same line runs `SimMotor::set_effort` in §9's test run and `RealMotor::set_effort` on the cart.

How it is done is not in the standard, but every mainstream compiler does it the same way: each object of a class with virtual functions carries a hidden pointer to a table of function addresses for its class, and a virtual call loads the address from the table and calls it. The standard's own note on class layout allows for "space for managing virtual functions". The pointer is the whole of `MotorInterface`, whose `sizeof` is 8 on this machine; `SimMotor` is 24 — the table pointer, the `bool` with 7 bytes of padding, and the `double` — and `RealMotor` 32.

**The virtual destructor.** `delete` on a `MotorInterface*` that points to a `RealMotor` must run `~RealMotor`, which is what commands zero and disables the drive. It does only if `~MotorInterface` is virtual; otherwise the standard makes the deletion undefined behaviour. Deliberately wrong:

```cpp
// deliberately wrong: the base class has no virtual destructor
#include <cstdio>
#include <memory>

class MotorInterface {
 public:
  ~MotorInterface() = default;                  // not virtual
  virtual void set_effort(double effort) = 0;
};

class RealMotor final : public MotorInterface {
 public:
  ~RealMotor() { std::printf("effort 0, disable, close\n"); }  // never runs below
  void set_effort(double effort) override { effort_ = effort; }
 private:
  double effort_ = 0.0;
};

int main() {
  std::unique_ptr<MotorInterface> motor = std::make_unique<RealMotor>();
  motor->set_effort(0.25);
}                                               // deletes a RealMotor through MotorInterface*
```

```text
.../c++/v1/__memory/unique_ptr.h:77:5: warning: delete called on 'MotorInterface' that is abstract but has non-virtual destructor [-Wdelete-abstract-non-virtual-dtor]
...
no_virtual_dtor.cpp:20:43: note: in instantiation of member function 'std::unique_ptr<MotorInterface>::~unique_ptr' requested here
```

Clang warns even without `-Wall`, pointing into the standard library where the `delete` happens and then at the line of this program that caused it. The run prints nothing: `~RealMotor` never ran, so on a real cart the drive would have been left enabled at its last command. The fix is one word, `virtual ~MotorInterface() = default;`, which is how the listing above declares it. The rule of thumb for any class meant to be used through a base pointer: its destructor is public and virtual.

A second trap sits next to the first. During a destructor, the object is only as derived as the class whose destructor is running: by the time `~MotorInterface` runs, the `RealMotor` part is already gone, and a virtual call made there does not reach `RealMotor`'s version — calling a pure virtual function there is undefined behaviour. So `disable()` belongs in `~RealMotor`, which is where `real_motor.cpp` calls it, and not in the base.

**The same seam in ros2_control.** A ros2_control controller and a hardware component are exactly this pattern: the controller manager loads both by name at run time and knows them only through base classes with virtual destructors, so every call it makes each period — `read()` on the hardware, `update()` on each active controller, `write()` on the hardware — is a virtual call ([[04-robotics/ros2/simulation-and-control|25.7 §5]] and [[04-robotics/ros2/simulation-and-control|25.7 §7]]). `MotorInterface` is that seam with one joint, and [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]] writes a real component.

> [!note]- Deeper · 더 깊이
> **The Jazzy base classes.** A controller derives from `controller_interface::ControllerInterface`, whose base `ControllerInterfaceBase` declares a virtual destructor and, among its pure virtual functions, `update(const rclcpp::Time & time, const rclcpp::Duration & period)`. A hardware component for a multi-joint machine derives from `hardware_interface::SystemInterface`, which derives from `HardwareComponentInterface`; that base has a virtual destructor, a pure virtual `read(time, period)` and a virtual `write(time, period)` that `SystemInterface` makes pure.

**The cost against 5 ms.** On this Apple M1, built with `-O3`, a loop of 200 million `set_effort` calls through a `MotorInterface*` whose dynamic type was chosen at run time took 0.97 to 1.10 ns per call over three repetitions — the same, within the noise, as the same loop calling a non-inlined, non-virtual function. One such call per tick is $1\ \mathrm{ns}/5\ \mathrm{ms}=2\times10^{-7}$ of the budget. What a virtual call really costs is that the compiler cannot inline through it unless it can prove the object's type, which marking a class `final` sometimes lets it do. That matters in an inner loop over thousands of elements; it does not matter for one call to the drive per tick.

> **Dynamic dispatch, defined.** **Dynamic dispatch** is *the rule by which a call to a virtual function runs the version belonging to the object's dynamic type, chosen when the call executes* — a property of a call made through a base-class pointer or reference, not of a function alone. Four defining conditions. The function is **declared `virtual`** in the base class, and a derived class **overrides** it with the same signature. The call is made **through a pointer or a reference** to the base; a call on an object named directly, or a qualified call such as `MotorInterface::set_effort`, is bound at compile time. The version that runs is the **final overrider** for the dynamic type — the most-derived class that defines one. And **during construction and destruction** the dynamic type is the class whose constructor or destructor is running, so a base's destructor cannot reach a derived class's override.
>
> $$\texttt{b->f(a)}\ \longmapsto\ \mathrm{final}_{\,\mathrm{dyn}(\texttt{*b})}(f)\,(a)$$
>
> where `b` is a pointer to a base class, $\mathrm{dyn}(\texttt{*b})$ the type of the object it points to when the call executes, and $\mathrm{final}_D(f)$ that type's final overrider of $f$ — so the same line of controller code drives a simulated cart or a real one, since the object and not the line decides which version runs.
>
> - **Example**: `motor_->set_effort(u)` in `CartController::tick` runs `SimMotor::set_effort` in §9's run and `RealMotor::set_effort` on the cart, with no change to the controller.
> - **Non-example**: a destructor that is not virtual. `delete` through a `MotorInterface*` then binds to `~MotorInterface` at compile time, and `no_virtual_dtor` printed nothing because `~RealMotor` never ran.
> - **Non-example**: `disable()` called from `~MotorInterface`. By then the `RealMotor` part is destroyed, the dynamic type is the base, and the call reaches no override.
> - **Why it matters**: the controller–hardware seam of ros2_control is this mechanism, and so is every switch between simulation and hardware that leaves the controller's code unchanged.

### 8. Building: headers, translation units, linking, CMake

*In one sentence:* a program is many source files, and its two classic build errors come from how they are joined: the compiler turns one source file, with the headers it includes, into an object file, the linker joins the object files and libraries into a program by matching every function a file uses to exactly one definition, and CMake writes down which files make which library and which program links to which library.

Three tools run in order. The **preprocessor** handles the lines that start with `#`: `#include` pastes a header's text in place, `#define` defines a macro, and `#if` keeps or drops text. The **compiler** translates one source file together with everything it includes — one **translation unit** — into an object file: machine code for the functions that unit defines, plus a list of the names it uses but does not define. The **linker** then joins the object files and libraries into one program and gives every used name the address of its one definition. The compiler never sees two `.cpp` files at once, so it cannot know whether a function declared in a header is defined anywhere; only the linker can, and that is why the two errors of this section are linker errors.

A **header** declares — classes, function signatures — and defines only what may appear in every translation unit that includes it: classes, `inline` functions, templates, constants. A **source file** defines the rest, once. Headers get included more than once: a unit that includes both `controller.hpp` and `sample.hpp` receives `sample.hpp` twice, since `controller.hpp` includes it too, and a class defined twice in one unit is an error — clang's "redefinition of 'EncoderSample'" when the guard is missing. An **include guard** — `#ifndef CART_SAMPLE_HPP`, `#define CART_SAMPLE_HPP` at the top, `#endif` at the bottom — is the standard remedy. `#pragma once`, which this page's headers use, is shorter and not part of the standard, but the vast majority of modern compilers support it. A name's **linkage** says whether other units can refer to it: a function at namespace scope has external linkage, and one inside an unnamed `namespace { }`, like `kKp` in `controller.cpp` in §9, has internal linkage and is private to its file.

P6's controller as a project:

```text
cart_controller/
├── CMakeLists.txt
├── include/cart/ring_buffer.hpp   RingBuffer<T, N>          (section 6)
├── include/cart/sample.hpp        EncoderSample, TickRecord (section 6)
├── include/cart/motor.hpp         MotorInterface, SimMotor  (section 7)
├── include/cart/controller.hpp    CartController            (section 9)
├── src/real_motor.cpp             RealMotor                 (section 7)
├── src/controller.cpp             CartController            (section 9)
└── src/main.cpp                   the 60 s test run         (section 9)
```

```cmake
cmake_minimum_required(VERSION 3.16)
project(cart_controller LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# The controller and the drive, compiled once into a library.
add_library(cart_core src/controller.cpp src/real_motor.cpp)
target_include_directories(cart_core PUBLIC include)     # its users see include/ too
target_compile_options(cart_core PRIVATE -Wall -Wextra)

# The program: its own main.cpp, linked against the library, not recompiling it.
add_executable(cart_controller src/main.cpp)
target_link_libraries(cart_controller PRIVATE cart_core)
target_compile_options(cart_controller PRIVATE -Wall -Wextra)
```

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release    # configure: write the build files into build/
cmake --build build                               # compile both .cpp of the library, then main.cpp, then link
./build/cart_controller
cmake -S . -B build-asan -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined"   # the checked build
```

`add_library` makes `cart_core` from the two sources it lists — a static library, unless the `BUILD_SHARED_LIBS` option asks for shared ones. `target_include_directories(... PUBLIC include)` puts `include/` on the header search path of `cart_core` and, being `PUBLIC`, of everything that links to it. `add_executable` makes the program from `main.cpp` alone, and `target_link_libraries(... PRIVATE cart_core)` links the library into it and passes on the library's public requirements, the include path among them. Each source is compiled once, in one target, and the targets that need it link that target: listing `controller.cpp` in the executable as well would compile it twice and leave two copies of its functions in the build. `CMAKE_CXX_STANDARD 17` with `REQUIRED` asks for C++17 and fails the configure step if the compiler lacks it.

**Undefined symbols.** Deliberately wrong: the same project with the `target_link_libraries` line replaced by an include path only, so `main.cpp` compiles against the headers and the library is never linked. Apple's linker on this Mac reports:

```text
Undefined symbols for architecture arm64:
  "CartController::tick(EncoderSample const&)", referenced from:
      _main in main.cpp.o
  "CartController::on_goal(double)", referenced from:
      _main in main.cpp.o
  "CartController::CartController(std::__1::unique_ptr<MotorInterface, std::__1::default_delete<MotorInterface>>, unsigned long)", referenced from:
      _main in main.cpp.o
ld: symbol(s) not found for architecture arm64
```

GNU ld, the default linker on Ubuntu, reports the same failure as an "undefined reference to" each function. `main.cpp` compiled, because the header declared the three functions; nothing linked defined them. The two usual causes are the one shown — the file that defines them is not compiled into anything the program links — and a definition that does not match its declaration: a different parameter type, a missing `const`, or a member function defined without its `CartController::` prefix, which defines a new free function instead.

**Duplicate symbols.** Deliberately wrong: a helper defined in `sample.hpp` without `inline`,

```cpp
double counts_to_metres(std::int32_t counts) {  // deliberately wrong: a non-inline definition in a header
  return counts / kCountsPerMetre;
}
```

and called from both `controller.cpp` and `main.cpp`. Both units compile, and each object file now defines the function:

```text
duplicate symbol 'counts_to_metres(int)' in:
    .../CMakeFiles/cart_controller.dir/src/main.cpp.o
    .../libcart_core.a[2](controller.cpp.o)
ld: 1 duplicate symbols
```

GNU ld calls it a "multiple definition of" the function and treats it as a fatal error. Writing `inline double counts_to_metres(...)` fixes it, because an inline function may be defined in every unit that uses it; so does declaring it in the header and defining it in one `.cpp`.

> [!note]- Deeper · 더 깊이
> **In a ROS 2 package** the file gains `find_package(ament_cmake REQUIRED)` and one `find_package` per dependency, and the Jazzy tutorials attach dependencies with `ament_target_dependencies(talker rclcpp std_msgs)`, an ament macro that adds each package's include directories and libraries to the target through `target_include_directories` and `target_link_libraries`. colcon builds a whole workspace of such packages in dependency order. That is [[04-robotics/ros2/workspaces-packages-launch|25.4 §3]] and [[04-robotics/ros2/workspaces-packages-launch|25.4 §4]]; this page stops at the plain CMake underneath.

> **Translation unit, linkage and the one-definition rule, defined.** A **translation unit** is *one source file after preprocessing* — a `.cpp` with every header it includes pasted in — and the unit the compiler translates, alone, into an object file. **Linkage** is *the property of a name that says whether other translation units can refer to the same entity*: external (they can), internal (only its own unit), or none (only its own scope). The **one-definition rule** says *how many definitions each entity may have*. Three defining conditions. **Within one translation unit**, no variable, function, class or template may be defined twice — include guards exist so that a header included twice still defines its classes once. **Across the whole program**, every non-inline function and variable that is used must be defined exactly once. And classes, templates and `inline` functions **may be defined in every translation unit that uses them**, provided the definitions are identical token for token, which including one header guarantees. The compiler cannot check the program-wide rule, since it sees one unit at a time; the linker reports the common violations, and some pass silently as undefined behaviour.
>
> $$n_{\text{def}}(e)=1\ \text{ for every used non-inline function or variable } e;\qquad n_{\text{def}}=0\Rightarrow\text{undefined symbol},\quad n_{\text{def}}\ge2\Rightarrow\text{duplicate symbol}$$
>
> where $n_{\text{def}}(e)$ counts the definitions of $e$ across all the object files and libraries linked — so the two classic link errors are the two ways of missing the number one.
>
> - **Example**: `CartController::tick` is declared in `controller.hpp`, which two units include, and defined once, in `controller.cpp`: $n_{\text{def}}=1$. `RingBuffer` is defined in every unit that includes its header, which the rule allows for a template.
> - **Non-example**: `counts_to_metres` defined in a header without `inline`, $n_{\text{def}}=2$; and `cart_controller` linked without `cart_core`, $n_{\text{def}}=0$ for three members of `CartController`.
> - **Why it matters**: these two errors are the first a C++ package in a ROS 2 workspace produces, and each names its cause exactly once it is read as a count.

### 9. The rules of a real-time tick

*In one sentence:* a tick that runs over its period leaves the previous command on the motor, so a tick is real-time safe only when its worst case, not its average, fits in the period — and because a heap allocation, a blocking call, a contended lock, a thrown exception or a page fault has no useful bound on its time, a real-time tick does none of them, with everything it needs allocated and touched before the loop starts.

P6's controller is released every $T=5$ ms and must finish each tick before the next release; a tick that runs over leaves the previous command on the motor for another period. [[04-robotics/robot-systems-deployment|10. Robot Systems §3]] defines the deadline, the response time and the jitter this needs, and makes the point that decides everything below: the mean is the number that looks good in a table, and the maximum is the one that decides whether the loop works.

**What the ROS 2 documentation says.** The Jazzy tutorial "Understanding real-time programming" names the same enemies: a real-time loop must update periodically to meet its deadlines, with only a small margin of error, and to do so it must avoid page faults, dynamic memory allocation and deallocation, and synchronization primitives that block indefinitely. Its example run shows why the mean misleads: on a 1 ms loop, a mean latency of 19,871.8 ns and a maximum of 2,752,187 ns — a worst case 138 times the mean and 2.75 periods long, which, as the tutorial says, exceeded the loop's own period.

> [!note]- Deeper · 더 깊이
> **How the tutorial's demo is set up.** Its pendulum demo locks its memory into RAM with `mlockall`, runs its control thread at priority 98, and warns that without a PREEMPT_RT kernel the goal will probably not be met.

**The rules, each with its reason.**

1. *No allocation or deallocation in the tick.* The allocator may take a lock another thread holds, ask the operating system for memory, or hand out pages never touched before; none of that has a bound worth writing down. The hidden cases count too, everything that may allocate or free: `push_back` past capacity, a vector copied by value, a `std::string` built at run time, an exception, and the last `shared_ptr` to a message released inside the tick, which frees the message there.
2. *No blocking I/O.* Printing, logging to a console or a file, a socket, waiting for the next message. The ROS 2 design article on real-time systems recommends keeping disk reads and writes out of the real-time path, at the start or end of the program, and handing printing to a thread that is not real-time.
3. *No unbounded waits on locks.* A tick that locks a mutex held by a lower-priority thread waits as long as that thread takes — priority inversion. Hand one value across threads with a `std::atomic`, and larger data with a structure whose real-time side only tries: ros2_control's `realtime_tools::RealtimeBuffer` reads with `try_to_lock` and, if the lock is taken, returns the previous data instead of waiting.
4. *No thrown exceptions.* In the Itanium C++ ABI, which GCC and Clang use on Linux and macOS, a throw allocates the exception object on the heap when it can. Errors in the tick are values: a status, a zero command.
5. *Preallocate, and touch before the loop.* Everything the tick uses is sized in the constructor — `reserve`, `std::array`, `RingBuffer` — and on Linux `mlockall` keeps it in RAM, as the tutorial's demo does.
6. *Measure the worst case,* over a long run, on the target computer, under load.

P6's controller, written to those rules: the header declares what the controller owns, and the source file defines what it does.

```cpp
// include/cart/controller.hpp - P6's 200 Hz controller: what it owns, declared
#pragma once
#include <atomic>
#include <cstddef>
#include <memory>
#include <vector>
#include "cart/motor.hpp"
#include "cart/sample.hpp"

class CartController {
 public:
  CartController(std::unique_ptr<MotorInterface> motor, std::size_t log_capacity);
  void on_goal(double goal_m);                  // vision callback, 50 Hz, another thread
  void tick(const EncoderSample& s);            // control loop, 200 Hz
  const std::vector<TickRecord>& log() const { return log_; }

 private:
  std::unique_ptr<MotorInterface> motor_;       // owns the drive
  RingBuffer<EncoderSample, 5> history_;        // 96 bytes, inside this object
  std::vector<TickRecord> log_;                 // on the heap, reserved once
  std::atomic<double> goal_m_{0.0};             // written at 50 Hz, read at 200 Hz
};
```

```cpp
// src/controller.cpp - every allocation happens before the first tick
#include "cart/controller.hpp"
#include <algorithm>
#include <utility>

namespace {
constexpr double kKp = 2.0;                     // effort per metre of error
constexpr double kKd = 0.5;                     // effort per m/s of velocity
}  // namespace

CartController::CartController(std::unique_ptr<MotorInterface> motor, std::size_t log_capacity)
    : motor_(std::move(motor)) {
  log_.reserve(log_capacity);                   // the log's one allocation
  motor_->enable();
}

void CartController::on_goal(double goal_m) { goal_m_.store(goal_m); }

void CartController::tick(const EncoderSample& s) {  // no allocation, no blocking, no throw
  if (!s.valid) {                               // a failed read commands zero
    motor_->set_effort(0.0);
    return;
  }
  history_.push(s);                             // a 16-byte copy into fixed storage
  const double p = s.counts / kCountsPerMetre;
  const double v = velocity(history_);          // reads the buffer through a const&
  const double goal = goal_m_.load();           // lock-free on x86-64 and ARM64
  const double u = std::clamp(kKp * (goal - p) - kKd * v, -1.0, 1.0);
  motor_->set_effort(u);                        // one virtual call
  if (log_.size() < log_.capacity()) log_.push_back({s.stamp_ns, goal, p, u});  // never grows
}
```

The constructor does the allocating: `reserve` sizes the log for the whole run, and the ring buffer needs nothing, since it is inside the object. `tick` then copies one 16-byte sample into the ring, reads the ring through a `const&`, reads the goal with one atomic load, clamps, makes one virtual call and appends 32 bytes to a log that has room for them — no `new`, no lock, no `throw`, no I/O. `goal_m_` is a `std::atomic<double>` because `on_goal` runs on the vision callback's thread (with a multi-threaded executor, [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]) while `tick` reads it on the control thread; an atomic makes a write in one thread and a read in another well-defined. An 8-byte atomic is always lock-free on x86-64 Linux, ARM64 Linux and ARM64 macOS — the compiler's `__atomic_always_lock_free(8, 0)` holds for all three — so the load takes no lock and cannot block. The failed read takes the safe branch: it commands zero rather than throwing.

A test can prove the first rule instead of trusting it. The C++ standard lets a program replace the global `operator new`, and every `new` in the program, the standard containers' included, then goes through the replacement, so `main.cpp` counts them around the loop — and times every tick:

```cpp
// src/main.cpp - a 60 s run of P6's controller against a simulated cart
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <new>
#include <utility>
#include "cart/controller.hpp"

static long g_allocations = 0;                  // every operator new in the program, counted
void* operator new(std::size_t n) {
  ++g_allocations;
  if (void* p = std::malloc(n)) return p;
  throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }

int main() {
  constexpr int kTicks = 12'000;                // 60 s at 200 Hz
  constexpr std::int64_t kPeriodNs = 5'000'000; // T = 5 ms
  auto motor = std::make_unique<SimMotor>();
  const SimMotor* sim = motor.get();            // observes; the controller will own it
  CartController controller(std::move(motor), kTicks);   // motor is empty from here on

  double p = 0.0;                               // the simulated cart, metres
  double sum_us = 0.0, worst_us = 0.0;
  const long before = g_allocations;
  for (int k = 0; k < kTicks; ++k) {
    if (k % 4 == 0) controller.on_goal(0.40);   // the 50 Hz goal, every fourth tick
    const EncoderSample s{k * kPeriodNs, static_cast<std::int32_t>(p * kCountsPerMetre), true};
    const auto t0 = std::chrono::steady_clock::now();
    controller.tick(s);
    const auto t1 = std::chrono::steady_clock::now();
    const double us = std::chrono::duration<double, std::micro>(t1 - t0).count();
    sum_us += us;
    worst_us = std::max(worst_us, us);
    p += sim->effort() * 0.5 * 0.005;           // the cart moves 0.5 m/s at full effort
  }
  std::printf("allocations during %d ticks: %ld\n", kTicks, g_allocations - before);
  std::printf("log records %zu, cart at %.4f m\n", controller.log().size(), p);
  std::printf("tick time: mean %.3f us, worst %.3f us, budget 5000 us\n", sum_us / kTicks, worst_us);
}
```

```text
allocations during 12000 ticks: 0
log records 12000, cart at 0.4004 m
tick time: mean 0.028 us, worst 1.625 us, budget 5000 us
```

That run is the Release build (`-O3`) on an Apple M1. Ten runs gave a mean of 0.022–0.028 µs and a worst tick of 1.2–10.7 µs, 53 to 427 times the mean; the sanitizer build of the same project also counted 0 allocations. Two cautions about these numbers. The clock on this machine advances in steps of about 41.7 ns, so a single 25 ns tick reads as 0 or 42 ns and only an average of many ticks resolves it; the worst values, in microseconds, are real. And a laptop running macOS is not a real-time system: the numbers show the shape — a worst case far above the mean, and far below 5 ms — not a guarantee. The guarantee needs the robot's own computer, a PREEMPT_RT kernel and a long run under load.

The rules matter more than those numbers suggest, because what they forbid grows. Timing one call of the Worked case's first-draft function, `velocity_all`, which takes the whole history by value, 200 times on this M1: with one minute of history (12,000 samples) the median call took 3.1–3.8 µs over five runs; with one hour (720,000 samples) it took 0.41–0.56 ms, and the slowest calls took 1.0–2.8 ms — up to more than half the period, from one line, in a test that passes for its first minute. A blocking call needs no growth at all: a tick that waits for the next 50 Hz goal can wait up to $T_v=20$ ms, four periods, whatever its own computation costs.

ros2_control writes the same rules into its interface. In Jazzy, `ControllerInterfaceBase::update` carries the comment that it must be real-time safe, because the controller manager calls it from its loop, and the hardware component's `set_state` and `get_command` that take an interface's name are marked not real-time safe; [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]] explains why and shows the handle-based forms to use in the loop instead.

> **Real-time-safe tick, defined.** A tick is **real-time safe** when *its worst-case execution time is bounded and the bound fits in the period, with room for everything else the core must do* — a property of the code a loop runs each period on a given machine, not of the language, of the rate or of the average. Five defining conditions, the first four being how the fifth is reached. It **allocates and frees nothing**: all its storage exists before the first tick. It **blocks on nothing**: no I/O, no sleep, no wait for a message, and no lock another thread can hold for long — at most a `try_lock` or a lock-free exchange. It **throws nothing**. It **causes no page faults**: its memory was touched, and on Linux locked, before the loop. And its **measured worst case**, over a long run on the target under load, is below the period.
>
> $$C_{\max}=\max_k C_k\ \le\ T-C_{\text{other}},\qquad T=\frac{1}{f_c}=5\ \mathrm{ms}$$
>
> where $C_k$ is the execution time of tick $k$ and $C_{\text{other}}$ the time the same core owes to everything else within the period — so a mean below $T$ says nothing, since one tick above it is a miss.
>
> - **Example**: §9's tick allocated nothing in 12,000 ticks and its worst tick on this laptop took 1.2–10.7 µs over ten runs, against a 5,000 µs period. It meets the first four conditions by construction; the fifth has to be measured again on the robot's computer.
> - **Non-example**: the Worked case's first draft, which allocated 12,030 times in 60 s and by the end copied 192,000 bytes per tick. Its average is a few microseconds, but its cost grows with the run and its allocations have no bound.
> - **Non-example**: a tick that waits for the next 50 Hz goal. Its computation is trivial and it is still late, by up to 20 ms, four periods.
> - **Why it matters**: the controller manager of ros2_control calls every active controller's `update()` from its loop, and the Jazzy interface says in its own comment that `update()` must be real-time safe.

### Worked case · 대상으로 한 번 끝까지

This is the homework object: one tick of P6's controller, counted, at the end of a 60 s run. The problem set changes one knob at a time — the struct, the rate, the code — so do the page's version here first. Every number is checked twice: by hand below, and by a C++ program whose output is quoted. The first draft that the count is set against is the controller as a newcomer writes it: every sample kept in a `std::vector` that is never reserved, the velocity computed by a function that takes that vector by value, and a log that is never reserved either.

**Step 1 — the sample's bytes (§3).** With $o_i$ the offsets, $s_i$ the sizes and $a_S=8$ the largest alignment, the rule $\mathrm{sizeof}(S)=\lceil (o_n+s_n)/a_S\rceil\,a_S$ gives, as first written, offsets $0, 8, 16$ and

$$\mathrm{sizeof}=\Big\lceil\frac{16+4}{8}\Big\rceil 8=24\ \text{bytes},\qquad \text{reordered: } \Big\lceil\frac{12+1}{8}\Big\rceil 8=16\ \text{bytes}$$

since the members end at byte 20 in the first order and at byte 13 in the second. The payload is $1+8+4=13$ bytes either way, so the padding falls from 11 bytes to 3 and the sample from 24 bytes to 16, a third less. `layout.cpp` printed 24 and 16, with offsets 0, 8, 16 and 0, 8, 12.

**Step 2 — the ring buffer (§6).** `RingBuffer<EncoderSample, 5>` holds $K=5$ samples in place and two 8-byte indices: $5\cdot16+2\cdot8=96$ bytes, against $5\cdot24+16=136$ with the first layout. It lives inside the controller, so it is allocated when the controller is and never again. Its window is $(K-1)T=4\cdot5=20$ ms, over which one count is a velocity of $1/(2048\cdot0.020)=0.0244$ m/s.

**Step 3 — what one tick copies (§1).** Section 9's tick copies the new sample into the ring, 16 bytes, reads the ring through a `const&`, 0 bytes, and appends one record, 32 bytes: 48 bytes a tick, $48\cdot200=9{,}600$ bytes a second, the same in the first second as in the last. Passing the ring by value instead would add its 96 bytes, 19,200 a second, and still allocate nothing. The first draft's by-value vector copies every sample kept so far, $16k$ bytes at tick $k$:

$$B_{\text{copy}}(k)=16k,\qquad B_{\text{copy}}(12{,}000)=192{,}000\ \text{bytes},\qquad 200\cdot192{,}000=38.4\ \text{MB/s}$$

because the $k$-th call copies $k$ samples of 16 bytes, and the tick rate is 200 per second. Over the whole run the copies add up to $16\cdot(1+2+\dots+12{,}000)=16\cdot12{,}000\cdot12{,}001/2=1{,}152{,}096{,}000$ bytes, each with one allocation.

**Step 4 — what the run allocates (§6).** Without `reserve`, a vector that starts empty and doubles grows to capacities $1, 2, 4, \dots, 16{,}384$ — fifteen allocations, since $2^{13}=8{,}192<12{,}000\le2^{14}=16{,}384$ — and moves $1+2+\dots+8{,}192=16{,}383$ elements on the way. The first draft has two such vectors, the samples and the log, so its loop makes $12{,}000+15+15=12{,}030$ allocations of

$$1{,}152{,}096{,}000+16\cdot32{,}767+32\cdot32{,}767=1{,}152{,}096{,}000+524{,}272+1{,}048{,}544=1{,}153{,}668{,}816\ \text{bytes}$$

since each doubling allocates a block of the new capacity and $1+2+\dots+16{,}384=32{,}767$. The log's largest growth comes at record 8,193, 41 s in, and moves 8,192 records, 262,144 bytes, inside one tick. With `reserve(12'000)` in the constructor the log makes one allocation of $12{,}000\cdot32=384{,}000$ bytes before the loop and none in it; the ring makes none at all. Averaged over the minute, the first draft's log grew $15/60=0.25$ times a second, a number that looks harmless and hides a single tick that moved a quarter of a megabyte. The program:

```cpp
// tick_cost.cpp - what one 60 s run allocates and copies, first draft against section 9's tick
#include <cstdio>
#include <cstdlib>
#include <new>
#include <vector>
#include "cart/sample.hpp"

static long g_calls = 0, g_bytes = 0;           // operator new, counted
void* operator new(std::size_t n) {
  ++g_calls;
  g_bytes += static_cast<long>(n);
  if (void* p = std::malloc(n)) return p;
  throw std::bad_alloc();
}
void operator delete(void* p) noexcept { std::free(p); }

double velocity_all(std::vector<EncoderSample> h) {        // first draft: by value
  if (h.size() < 5) return 0.0;
  const EncoderSample& a = h[h.size() - 5];
  const EncoderSample& b = h.back();
  return (b.counts - a.counts) / kCountsPerMetre / ((b.stamp_ns - a.stamp_ns) * 1e-9);
}

int main() {
  constexpr int kTicks = 12'000;
  std::vector<EncoderSample> samples;           // first draft: every sample, never reserved
  std::vector<TickRecord> draft_log;            // first draft: not reserved
  RingBuffer<EncoderSample, 5> history;         // section 9: five samples, in place
  std::vector<TickRecord> log;
  log.reserve(kTicks);                          // section 9: reserved before the loop

  long calls = g_calls, bytes = g_bytes;
  double v = 0.0;
  for (int k = 1; k <= kTicks; ++k) {
    const EncoderSample s{k * 5'000'000LL, k, true};  // one count per tick
    samples.push_back(s);
    v = velocity_all(samples);
    draft_log.push_back({s.stamp_ns, 0.40, s.counts / kCountsPerMetre, 0.0});
  }
  std::printf("first draft: %ld allocations, %ld bytes allocated, v %.4f m/s\n",
              g_calls - calls, g_bytes - bytes, v);

  calls = g_calls, bytes = g_bytes;
  for (int k = 1; k <= kTicks; ++k) {
    const EncoderSample s{k * 5'000'000LL, k, true};  // one count per tick
    history.push(s);
    v = velocity(history);
    log.push_back({s.stamp_ns, 0.40, s.counts / kCountsPerMetre, 0.0});
  }
  std::printf("section 9  : %ld allocations, %ld bytes allocated, v %.4f m/s\n",
              g_calls - calls, g_bytes - bytes, v);
  std::printf("sizeof: sample %zu, record %zu, ring %zu\n",
              sizeof(EncoderSample), sizeof(TickRecord), sizeof(history));
}
```

```text
first draft: 12030 allocations, 1153668816 bytes allocated, v 0.0977 m/s
section 9  : 0 allocations, 0 bytes allocated, v 0.0977 m/s
sizeof: sample 16, record 32, ring 96
```

Both loops compute the same velocity, 0.0977 m/s, which is the fake encoder's one count per tick; one allocates 12,030 times and the other not once.

**Step 5 — who keeps the node alive (§5).** Wrapped in a ROS 2 node, the controller lives as long as the node, and the node as long as its use count is above zero. `ownership.cpp` printed the count through the node's life: 1 after `make_shared`, still 1 after the timer is created with a callback that captures `this`, 2 while `spin` holds its by-value copy, 1 after, and 0 when `main` lets go — at which point the destructor runs and the drive is zeroed. Capture `shared_from_this()` instead and the count reads 1, 2, 3, 2 and finally 1: the node owns its timer, the timer's callback owns the node, and the destructor that would shut the drive down never runs.

**Step 6 — the budget (§9).** The tick has $T=1/f_c=1/200\ \mathrm{s}=5$ ms. Measured on this laptop, section 9's tick took 0.022–0.028 µs on average and at most 1.2–10.7 µs over ten runs: at worst about 0.2% of the period. A tick that instead waits for the next vision goal waits up to

$$T_v=\frac{1}{f_v}=\frac{1}{50\ \mathrm{Hz}}=20\ \mathrm{ms}=4\,T$$

because a goal arrives only every fourth tick; such a loop runs at the goal rate, 50 Hz, and three ticks in four are lost. And the first draft's velocity call alone reaches 0.41–0.56 ms in its median after an hour of history, with slowest calls of 1.0–2.8 ms, measured the same way.

| One tick at the end of a 60 s run | first draft | §9's tick |
|---|---:|---:|
| bytes copied: sample, velocity argument, log record | 16 + 192,000 + 32 | 16 + 0 + 32 |
| heap allocations in the tick | 1, plus 30 growths over the run | 0 |
| allocations over the whole run | 12,030 | 0 |
| bytes allocated over the whole run | 1,153,668,816 | 0 |
| worst wait on another thread | none here; a blocking goal wait would add up to 20 ms | none: one atomic load |

### 10. Tools, and what this page does not cover

*In one sentence:* the defects of this page do not announce themselves, so tools must find them: compiler warnings catch some before the program runs, the sanitizers catch most of the rest while it runs, a debugger shows where it stopped, and what this page leaves out has better homes, listed at the end.

**Warnings.** Build everything with `-Wall -Wextra`, and add `-Werror` in continuous integration so that a warning cannot be merged. On this page they did less than one might hope:

| Defect | What clang said | Section |
|---|---|---|
| returning a reference to a local | warned, even without flags (`-Wreturn-stack-address`) | §2 |
| member initializers written out of order | warned with `-Wall` (`-Wreorder-ctor`) | §4 |
| copying a class that has a user-written destructor | silent with `-Wall -Wextra`; `-Wdeprecated` warned | §4 |
| deleting through a base without a virtual destructor | warned, even without flags (`-Wdelete-abstract-non-virtual-dtor`) | §7 |
| a non-inline function defined in a header | silent; the linker reported it | §8 |
| a `shared_ptr` cycle, an allocation or a blocking call in the tick | silent | §5, §9 |

**Sanitizers.** AddressSanitizer (`-fsanitize=address`) instruments every memory access and finds reads and writes out of the bounds of heap, stack and global objects, use after free, use after return, use after scope, and double or invalid frees; its typical slowdown is about 2×. On Linux its leak checker, LeakSanitizer, is on by default and reports what was never freed when the program exits. UndefinedBehaviorSanitizer (`-fsanitize=undefined`) checks for a list of undefined operations — signed overflow, a null or misaligned pointer, a shift out of range, an index out of bounds, a call through a pointer of the wrong dynamic type, among others — prints a report, and by default carries on; `-fno-sanitize-recover` makes it stop. GCC and Clang both accept both options; ThreadSanitizer, for data races, needs a build of its own, since it cannot be combined with AddressSanitizer. Sanitizers are for test builds and bench runs, never for the binary that drives the robot in real time: they slow it, about 2× for AddressSanitizer, and replace how it allocates memory.

Here is what AddressSanitizer printed for §2's callback that outlived its object, built with `-g` so that frames carry file and line:

```text
filtered goal 0.080 m
=================================================================
==86123==ERROR: AddressSanitizer: heap-use-after-free on address 0x6020000000b0 at pc 0x000102b837a4 bp 0x00016d2864b0 sp 0x00016d2864a8
READ of size 8 at 0x6020000000b0 thread T0
    #0 0x000102b837a0 in GoalFilter::update() callback_outlives.cpp:17
    #1 0x000102b83710 in GoalFilter::GoalFilter(Scheduler&)::'lambda'()::operator()() const callback_outlives.cpp:15
    ...                                                  (frames #2 to #7: std::function's call path)
    #8 0x000102b79154 in Scheduler::run_once() callback_outlives.cpp:9
    #9 0x000102b78b30 in main callback_outlives.cpp:30

0x6020000000b0 is located 0 bytes inside of 16-byte region [0x6020000000b0,0x6020000000c0)
freed by thread T0 here:
    #0 0x0001034d8358 in _ZdlPv+0x74 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x50358)
    ...
    #3 0x000102b78b28 in main callback_outlives.cpp:29

previously allocated by thread T0 here:
    #0 0x0001034d7f50 in _Znwm+0x74 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x4ff50)
    ...
    #2 0x000102b78a9c in main callback_outlives.cpp:26

SUMMARY: AddressSanitizer: heap-use-after-free callback_outlives.cpp:17 in GoalFilter::update()
```

Read it in three blocks, each a stack. The first is where the bad access happened: an 8-byte read — one of the filter's two `double`s — in `update()` at line 17, called through the lambda of line 15 by `run_once()` at line 9, from line 30 of `main`. The second is where that memory was freed: `operator delete` (`_ZdlPv` is its mangled name), called by `filter.reset()` at line 29. The third is where it was allocated: `operator new` (`_Znwm`), by `make_unique` at line 26. The 16-byte region is the whole `GoalFilter`. Three line numbers — use, free, allocation — are the whole diagnosis: something at line 30 used what line 29 destroyed.

UndefinedBehaviorSanitizer names the undefined operation itself. Deliberately wrong:

```cpp
// deliberately wrong: reads a sample through a null pointer
#include <cstdint>
#include <cstdio>

struct EncoderSample { std::int64_t stamp_ns; std::int32_t counts; bool valid; };

std::int32_t counts_of(const EncoderSample* s) { return s->counts; }  // no null check

int main() {
  const EncoderSample* latest = nullptr;        // no sample has arrived yet
  std::printf("%d counts\n", counts_of(latest));
}
```

```text
null_read.cpp:7:60: runtime error: member access within null pointer of type 'const EncoderSample'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior null_read.cpp:7:60
AddressSanitizer:DEADLYSIGNAL
==95159==ERROR: AddressSanitizer: SEGV on unknown address 0x000000000008 (pc 0x000104368984 bp 0x00016ba96980 sp 0x00016ba96930 T0)
==95159==The signal is caused by a READ memory access.
==95159==Hint: address points to the zero page.
    #0 0x000104368984 in counts_of(EncoderSample const*) null_read.cpp:7
```

The faulting address is 8 — the offset of `counts` in the reordered sample (§3), added to a null pointer.

**A debugger, in one paragraph.** Build with `-g` (and `-O0` if you want to step line by line), start the program under `lldb` on macOS or `gdb` on Linux, and type `run`. When it crashes, the debugger stops at the faulting line with the program intact: `null_read` built with `-g -O0` stopped with `stop reason = EXC_BAD_ACCESS (code=1, address=0x8)` in `counts_of(s=0x0000000000000000) at null_read.cpp:7:60`, which names the function, the null argument and the column. `bt` (`backtrace` in gdb) then prints the chain of calls that led there, `frame` or `up` moves along it, `print` shows a variable, and a breakpoint (`b file:line` in lldb, `break file:line` in gdb) stops the next run earlier. For a ROS 2 node, the ROS 2 how-to guide on backtraces builds the package with `colcon build --packages-up-to <package> --cmake-args -DCMAKE_BUILD_TYPE=Debug` and starts the node with `ros2 run --prefix 'gdb -ex run --args' <package> <executable>`, so that the node runs inside gdb with its ROS environment intact.

**What this page does not cover.** Templates beyond reading and writing a simple one — metaprogramming, concepts, variadic templates. Move semantics beyond §5's paragraph: rvalue references, move constructors of your own, perfect forwarding. Concurrency beyond the rules of §9: threads, the memory orders of atomics, lock-free structures; threads, races, locks and deadlock in general are [[02-foundations/tools/concurrency|12.8 Concurrency]], and how rclcpp's executors put callbacks on threads is [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]] and [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]. Object-oriented design beyond one interface. Build systems beyond one `CMakeLists.txt`, which [[04-robotics/ros2/workspaces-packages-launch|25.4]] continues. For the language itself, cppreference.com is the reference used throughout this page, and the C++ Core Guidelines are the rule book this page quoted twice; read a rule when a review cites it rather than reading the book through.

### After reading

- [ ] Say what a parameter of type `T`, `const T&`, `T&` and `const T*` each lets a function do, and what each costs per call at 200 Hz.
- [ ] Name the four storage durations, say when an automatic and a dynamic object die, and recognize both dangling references of §2 on sight.
- [ ] Lay out a struct byte by byte with its offsets and padding, and reorder it to the smallest size its payload allows.
- [ ] Write a class that owns a resource with RAII: acquire in the constructor, release in the destructor, delete the copy; and say which exits RAII does not cover.
- [ ] Say who owns what in a piece of rclcpp code, trace a node's use count through `make_shared`, a timer and `spin`, and break a `shared_ptr` cycle.
- [ ] Read and write a class template like `RingBuffer<T, N>`, and say when `std::vector` allocates, what `reserve` changes, and what doubling costs in the worst tick.
- [ ] Declare an interface with a virtual destructor, implement it twice, and say what goes wrong without the `virtual`.
- [ ] Say what the compiler and the linker each do, and fix an undefined-symbol and a duplicate-symbol error from their messages.
- [ ] State the rules of a real-time tick with the reason for each, and test a tick for allocations and for its worst case.
- [ ] Read a sanitizer report — access, free, allocation — and get a backtrace from a debugger.

### Self-check

1. `EncoderSample` as first written is 24 bytes and reordered is 16. Where do the 8 bytes go, and could any order make it 13?
2. A helper takes `std::vector<EncoderSample> history` by value and is called once per tick with every sample of the run. What does one call cost at the end of a 60 s run, and what change to the parameter's type removes nearly all of it?
3. A function returns `const EncoderSample&` to a local, and the program prints the right count. Why is that no evidence the program is correct, and what would show it is wrong?
4. A node's timer callback captures `shared_from_this()`. Trace the node's use count from `make_shared` to the end of `main`, and say what happens to the drive the node owns.
5. `std::unique_ptr<MotorInterface> motor_` holds a `RealMotor`, and `MotorInterface` has no virtual destructor. What happens when the controller is destroyed, and what does clang say about it?
6. The linker reports an undefined symbol for `CartController::tick`, though `controller.cpp` defines it. Name two causes.
7. Your tick averages 0.02 µs on the bench. Is it real-time safe? What would you check, and what would you measure?

> [!tip]- Answers
> 1. Into padding. As first written, 7 bytes sit between the 1-byte `valid` and the 8-byte `stamp_ns`, and 4 after `counts` to round 20 up to 24; reordered, only 3 bytes of tail padding remain. No order gives 13: the struct is aligned to 8, so its size is a multiple of 8, and $\lceil 13/8\rceil\cdot8=16$ is the smallest possible.
> 2. At tick 12,000 it copies $12{,}000\cdot16=192{,}000$ bytes into a freshly allocated block: one allocation and 192 kB per tick, 38.4 MB and 200 allocations a second. Declaring the parameter `const std::vector<EncoderSample>&` passes an address instead: 8 bytes and no allocation. The better change is the ring buffer, which also stops the history growing.
> 3. Because reading a dead object is undefined behaviour, and one of the things undefined behaviour may do is return the old value: nothing had yet overwritten the dead frame. The compiler's `-Wreturn-stack-address` warning already says it is wrong; AddressSanitizer with `detect_stack_use_after_return=1`, the default on Linux, stops the read and names `latest()`'s frame.
> 4. 1 after `make_shared`; 2 after the timer is created, since the callback stored in the timer holds a copy; 3 inside `spin`, which takes its own by value; 2 after `spin` returns; 1 after `main`'s pointer is destroyed. It never reaches 0, because the node owns the timer and the timer's callback owns the node, so the node's destructor never runs and the drive is never commanded to zero or disabled by it. Capture `this`, or a `weak_ptr`.
> 5. Deleting a `RealMotor` through a `MotorInterface*` whose destructor is not virtual is undefined behaviour; in the run of §7 `~RealMotor` simply never ran, so the drive would have stayed enabled at its last command. Clang warns even without `-Wall`: "delete called on 'MotorInterface' that is abstract but has non-virtual destructor". The fix is `virtual ~MotorInterface() = default;`.
> 6. The object file with the definition is not linked into the program — `controller.cpp` is missing from the library, or the program does not link the library — or the definition does not match the declaration: a different parameter type, a missing `const`, or `tick` defined without its `CartController::` prefix, which makes a free function nobody calls.
> 7. Not from the average. Check the code for allocation, blocking, locks and throws — the rules of §9 — and test it: count allocations around the loop, as §9's `main.cpp` does. Then measure the worst tick, not the mean, over a long run on the robot's own computer under load, and compare that with 5 ms minus everything else the core must do.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and [[02-foundations/lab-plants|0.6 Lab Plants]]. The work is by hand: the C++ is read and reasoned about, and the wiki's checks do not run it — compile it yourself if you like. Each problem changes one knob of the Worked case — the struct, the loop rate, the code under review — so no answer can be copied from the page.

1. **Draw.** P6's cart gets the single-axis IMU of [[04-robotics/sensor-models|3.2 Sensor Models & Noise]], read with the encoder at 200 Hz, and its driver delivers

    ```cpp
    struct ImuSample { bool valid; double accel_mps2; std::uint16_t seq; std::int64_t stamp_ns; float gyro_rps; };
    ```

    Redraw the picture for it. In panel (a), draw `ImuSample` byte by byte as written and with its fields reordered by decreasing alignment, with every offset, the padding shaded and both sizes. In panel (b), add a `RingBuffer<ImuSample, 5>` inside the controller and the IMU driver, owned by the node through a `std::unique_ptr`, with the bytes of the new ring. Say how many bytes per second the IMU's samples cost in each order.
2. **Derive.** Run P6's controller at $f_c=1$ kHz instead of 200 Hz, every other number unchanged, for the same 60 s. (a) The log: its bytes when reserved; without `reserve`, the number of growths, the final capacity in bytes, the records moved, and which push moves the most, how many bytes, and when. (b) The first draft's by-value history: the bytes copied at the last tick, per second at the end, and over the whole run, and the allocations its loop makes. (c) The ring length $K$ that keeps a 20 ms velocity window, its `sizeof`, and the one-count velocity if $K$ stays 5. (d) How many periods a tick that waits for the next 50 Hz goal can block, and what fraction of ticks such a loop loses. (e) What changes in the node's use counts.
3. **Interpret.** A code review. The node below comes from a lab's repository and drives P6's cart. Name each of its five defects, say what each does to the cart, and give the fix; then say which of them `-Wall -Wextra` would have reported at compile time, which AddressSanitizer would have caught in a test run, and which only a review or a test of §9's kind would find.

```cpp
// deliberately wrong: a cart node with five defects, for problem 3
class Drive {                                   // base of the sim and serial drives
 public:
  ~Drive() {}
  virtual void set_effort(double effort) = 0;
};

class SerialDrive : public Drive {
 public:
  explicit SerialDrive(const std::string& port) : fd_(open_port(port)) { enable(fd_); }
  ~SerialDrive() { write_effort(fd_, 0.0); disable(fd_); close_port(fd_); }
  void set_effort(double effort) override { write_effort(fd_, effort); }
 private:
  int fd_;
};

class CartNode : public rclcpp::Node {
 public:
  CartNode() : Node("cart_controller"), drive_(std::make_unique<SerialDrive>("/dev/ttyUSB0")) {}
  void start() {                                // called once, after make_shared
    auto self = std::static_pointer_cast<CartNode>(shared_from_this());
    timer_ = create_wall_timer(5ms, [self] { self->tick(); });
  }
  void on_goal(const Goal& msg) {               // vision callback, 50 Hz, another thread
    std::lock_guard<std::mutex> lock(goal_mutex_);
    goal_m_ = msg.position_m;
    plan_path_to(goal_m_);                      // takes about 12 ms
  }

 private:
  const EncoderSample& read_encoder() {
    EncoderSample s = encoder_.read();
    return s;
  }
  void tick() {                                 // 200 Hz
    const EncoderSample& s = read_encoder();
    history_.push_back(s);
    double goal = 0.0;
    { std::lock_guard<std::mutex> lock(goal_mutex_); goal = goal_m_; }
    drive_->set_effort(2.0 * (goal - s.counts / 2048.0));
  }

  std::unique_ptr<Drive> drive_;
  rclcpp::TimerBase::SharedPtr timer_;
  std::vector<EncoderSample> history_;
  std::mutex goal_mutex_;
  double goal_m_ = 0.0;
  Encoder encoder_;
};
```

> [!note]- How to draw it · 그리는 법
> - Give panel (a) one scale: one cell per byte, the same width in every row, with the offsets written at each multiple of 8.
> - Place each member at the next multiple of its own alignment, shade the gaps, then round the end up to the struct's largest alignment and shade the tail; the size must come out a multiple of that alignment.
> - For the reordered row, sort the members by decreasing alignment and check the result against the bound $\lceil \text{payload}/a_S\rceil\,a_S$: if the size meets it, no order does better.
> - In panel (b), keep the stack and the heap apart. Draw an object stored inside another — a ring buffer, an atomic — inside its box, with no arrow. Draw arrows only for pointers: solid for owners (`unique_ptr`, `shared_ptr`, a vector's storage), dashed for observers (raw pointers, a captured `this`, `weak_ptr`).
> - Write the use count on every `shared_ptr` edge. Follow the solid arrows from the stack: if they can return to a box they have already passed through, there is a cycle, and one of its edges has to become dashed.
> - Write the bytes of everything the tick touches next to it: each ring, the log's storage.

> [!tip]- Solutions
> 1. As written: `valid` at 0, padding 1–7, `accel_mps2` 8–15, `seq` 16–17, padding 18–23, `stamp_ns` 24–31, `gyro_rps` 32–35, tail padding 36–39. The members end at 36 and the size rounds up to 40 bytes, 17 of them padding, for a payload of $1+8+2+8+4=23$. Reordered by decreasing alignment: `accel_mps2` 0–7, `stamp_ns` 8–15, `gyro_rps` 16–19, `seq` 20–21, `valid` 22, tail padding 23: 24 bytes with 1 of padding, which is the bound $\lceil 23/8\rceil\cdot8=24$, so no order does better. (A compiled check prints 40 and 24, with offsets 0, 8, 16, 24, 32 and 0, 8, 16, 20, 22.) Panel (b): `imu_history_: RingBuffer<ImuSample, 5>` inside the controller, $5\cdot24+16=136$ bytes in place ($5\cdot40+16=216$ as written), no arrow; the node gains `imu_: unique_ptr<ImuDriver>` with a solid arrow to an `ImuDriver` box on the heap, with no count because a unique owner has none; the node's own counts are unchanged, 1, and 2 while `spin` holds it. At 200 Hz the IMU's samples cost $200\cdot40=8{,}000$ bytes a second as written and $200\cdot24=4{,}800$ reordered; with the encoder's 3,200, the two streams together are 8,000 bytes a second reordered against 12,800 as first written.
> 2. (a) Reserved: $60{,}000\cdot32=1{,}920{,}000$ bytes, one allocation before the loop. Without `reserve`: $2^{15}=32{,}768<60{,}000\le2^{16}=65{,}536$, so 17 growths, a final capacity of 65,536 records or 2,097,152 bytes, and $1+2+\dots+32{,}768=65{,}535$ records moved. The biggest move is at push 32,769, 32.768 s in: 32,768 records, 1,048,576 bytes in one tick. (b) At the last tick $60{,}000\cdot16=960{,}000$ bytes; per second at the end $1{,}000\cdot960{,}000=960$ MB; over the run $16\cdot60{,}000\cdot60{,}001/2=28{,}800{,}480{,}000$ bytes, about 28.8 GB; its loop makes $60{,}000+17+17=60{,}034$ allocations. (c) $K-1=0.020/0.001=20$, so $K=21$ and `sizeof` is $21\cdot16+16=352$ bytes. With $K=5$ the window is 4 ms and one count is $1/(2048\cdot0.004)=0.122$ m/s, five times the 0.0244 m/s of a 20 ms window. (d) Up to $T_v=20$ ms, which is now 20 periods; the loop runs at 50 Hz and loses 19 ticks in 20, 95%. (e) Nothing: a use count counts owners, not ticks — 1, 1, 2 inside `spin`, 1, 0 with `this` captured, and 1, 2, 3, 2, 1 with the cycle.
> 3. (i) `~Drive() {}` is not virtual, and `drive_` is a `unique_ptr<Drive>` holding a `SerialDrive`. Destroying the node deletes through the base: undefined behaviour, and in practice `~SerialDrive` does not run, so the effort is not zeroed, the drive not disabled and the port not closed. Clang warns even without `-Wall`. Fix: `virtual ~Drive() = default;`. (ii) `start()` stores `self`, a `shared_ptr` to the node, in the callback of the node's own timer: the node owns the timer, the timer owns the node, the use count never reaches 0, and the node and its `drive_` are never destroyed — so even a clean Ctrl-C shutdown leaves the drive enabled, and with (i) fixed it still would. Nothing warns; on Linux LeakSanitizer reports the leaked node at exit. Fix: capture `this`, since the node owns the timer, or a `weak_ptr`. (iii) `read_encoder()` returns a reference to its local `s`, so `tick()` computes the effort from a dead sample: right on the bench by luck, garbage in the field. Clang warns (`-Wreturn-stack-address`), and AddressSanitizer with use-after-return detection, the default on Linux, stops the read at `history_.push_back(s)`. Fix: return `EncoderSample` by value. (iv) `history_.push_back(s)` in the tick: the vector grows without bound and reallocates at every doubling — 15 times in the first minute, the latest moving 8,192 samples, 131,072 bytes, in one tick — and its memory grows by $16\cdot200=3{,}200$ bytes a second for as long as the node runs, 11.52 MB of samples an hour. Nothing reports it; §9's allocation count would. Fix: a `RingBuffer<EncoderSample, 5>`, or a log reserved in the constructor and bounded. (v) `on_goal()` holds `goal_mutex_` for the 12 ms of `plan_path_to`, and `tick()` takes the same lock: a tick that arrives during planning waits up to 12 ms, 2.4 periods, and at 50 Hz the lock is held 12 ms of every 20, so three ticks in five find it taken; if the vision thread runs at lower priority, priority inversion can stretch the wait further. Nothing reports it; timing the worst tick would. Fix: plan outside the lock and hand the goal over through a `std::atomic<double>` or a `RealtimeBuffer`, so the tick never waits. Summary: warnings catch (i) and (iii); AddressSanitizer catches (iii) at run time and, on Linux, LeakSanitizer (ii) at exit; (iv) and (v) need a review or the tests of §9.

### Sources

- cppreference.com ([en.cppreference.com/w/cpp](https://en.cppreference.com/w/cpp)) — the language and library rules quoted throughout: storage duration and lifetime, references and pointers, undefined behaviour, object layout and `sizeof`, constructors, destructors and exceptions, `std::exit`, RAII and the rule of zero, the implicit copy's deprecation, the smart pointers and `enable_shared_from_this`, `std::move`, the containers and `reserve`, templates, virtual functions and abstract classes, the ODR, `#pragma once`, `operator new`, `std::atomic`.
- ISO C++ working draft ([eel.is/c++draft](https://eel.is/c++draft/)) and the C++17 standard as N4659 ([timsong-cpp.github.io/cppwp/n4659](https://timsong-cpp.github.io/cppwp/n4659/)) — alignment, `sizeof`, member placement, deleting through a base without a virtual destructor, and how far back undefined behaviour reaches.
- C++ Core Guidelines ([isocpp.github.io/CppCoreGuidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)) — F.16 (how to pass "in" parameters) and F.43 (never return a pointer or reference to a local).
- System V AMD64 psABI ([gitlab.com/x86-psABIs/x86-64-ABI](https://gitlab.com/x86-psABIs/x86-64-ABI)) and Arm's AAPCS64 ([github.com/ARM-software/abi-aa](https://github.com/ARM-software/abi-aa)) — scalar sizes and alignments; a struct's alignment and size.
- Itanium C++ ABI, Exception Handling ([itanium-cxx-abi.github.io](https://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html)) — §2.4.2, the exception object allocated on the heap when possible.
- LLVM libc++ `__vector/vector.h` and GCC libstdc++ `bits/stl_vector.h` — how each grows a full vector.
- rclcpp, Jazzy branch ([github.com/ros2/rclcpp](https://github.com/ros2/rclcpp/tree/jazzy)) — `macros.hpp`, `node.hpp`, `timer.hpp`, `callback_group.hpp`, `executors.hpp`, `utilities.hpp`: the pointer aliases, `enable_shared_from_this`, timers held by `WeakPtr`, `spin` by value, the default signal handlers.
- ros2_control and realtime_tools, Jazzy branches ([github.com/ros-controls](https://github.com/ros-controls)) — `hardware_component_interface.hpp` (copies deleted, not-real-time-safe by-name accessors), `controller_interface_base.hpp` (`update` "needs to be real-time safe"), `realtime_buffer.hpp` (`try_to_lock`).
- ROS 2 documentation, Jazzy branch ([github.com/ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — "Understanding real-time programming" (what to avoid, `mlockall`, priority 98, PREEMPT_RT, the example latencies), "Getting Backtraces in ROS 2", the C++ publisher tutorial (`[this]`, `ament_target_dependencies`); J. Kay, "Introduction to Real-time Systems" ([ros2/design](https://github.com/ros2/design), 2016).
- ament_cmake, Jazzy branch — what `ament_target_dependencies` adds to a target.
- CMake documentation ([cmake.org/cmake/help/latest](https://cmake.org/cmake/help/latest/)) — `add_library`, `add_executable`, `target_link_libraries`, `target_include_directories`, `CXX_STANDARD`.
- Clang documentation ([clang.llvm.org/docs](https://clang.llvm.org/docs/AddressSanitizer.html)) — AddressSanitizer and UndefinedBehaviorSanitizer; GCC's *Program Instrumentation Options* — both sanitizers, and ThreadSanitizer apart.
- GNU ld manual ([sourceware.org/binutils/docs/ld](https://sourceware.org/binutils/docs/ld/Options.html)) and binutils bug 27311 — multiple definitions fatal; the "undefined reference to" and "multiple definition of" wording.
- The runs: Apple clang 21.0.0 on an Apple M1 with macOS 26.6.2, libc++, CMake 3.31.2; Linux layouts checked with `--target=x86_64-unknown-linux-gnu` and `--target=aarch64-unknown-linux-gnu`.

## 한국어

*[[02-foundations/lab-plants|0.6 Lab Plants]] 위에 선다. 그 페이지의 장치 **P6**가 이 페이지가 프로그램하는 카트다. 그리고 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]] 위에 선다. 거기서 정한 70 ms 예산과 틱마다의 마감을 이 프로그램이 지켜야 한다. **P6**를 C++ 프로그램으로 처음 쓰는 페이지다. 뒤따르는 ROS 2 트랙은 여기서 가르치는 것을 전제한다. [[04-robotics/ros2/nodes-topics-messages|25.2 §6]]은 C++ 노드를 한 줄씩 읽고, [[04-robotics/ros2/workspaces-packages-launch|25.4]]는 ament와 colcon으로 C++ 패키지를 빌드하며, [[04-robotics/ros2/simulation-and-control|25.7 §5]]는 제어기와 하드웨어를 인터페이스의 양쪽에 두고, [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]은 그 한쪽을 직접 쓴다.*

> [!note] 왜 배우는가 · Why this matters
> C++는 [[07-research-program/index|7 §5]]의 물리 AI 스택에서 제어기와 드라이버가 실제로 도는 층이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). ros2_control의 제어기와 하드웨어 컴포넌트, 그리고 대부분의 로봇 드라이버는 매 주기 불리는 C++이고, 그래서 "그 패널을 프레임에 설치해"에서 부품을 옮기고, 접촉을 감지하고, 끼워 맞추는 코드가 바로 이것이다. 여기의 결함은 시험이 아니라 로봇을 망가뜨린다. 가상 소멸자가 없는 기반 클래스는 P6의 구동기를 마지막 명령으로 켜 둔 채 남기고, `shared_ptr` 순환은 Ctrl-C 뒤에도 노드와 그 노드가 소유한 구동기를 살려 두며, 틱 안의 `push_back` 하나는 실행 41 s째에 5 ms 주기 하나 안에서 262,144바이트를 옮긴다. 이 지식이 처음 필요해지는 것은 학위논문 경로([[07-research-program/index|7 §8]])의 2블록, C++ 노드를 처음 읽거나([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]) 제어기와 하드웨어를 인터페이스의 양쪽에 둘 때이고([[04-robotics/ros2/simulation-and-control|25.7 §5]], [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]), 다시 필요해지는 것은 7블록에서 학습한 정책의 임피던스 목표를 자기 주기로 도는 제어기가 구현할 때다([[05-construction-robotics/imitating-contact|10. 접촉 모방 §6]]). 이 페이지를 마치면 로봇 C++의 객체마다 누가 소유하고 얼마나 사는지 말하고, 제어 틱에서 할당, 막힘, 정의되지 않은 동작을 몰아낼 수 있다.

> [!note] 처음이라면 · First pass
> 90분 안팎으로 두 번 앉되, 읽으면서 직접 컴파일한다. 모든 목록은 `clang++ -std=c++17 -Wall -Wextra -fsanitize=address,undefined`로 빌드했고, 보이는 출력은 모두 실제 실행이 찍은 것이다. **첫 번째 — 누가 무엇을 얼마나 오래 소유하는가.** 이 페이지의 대상과 그림, 그다음 §1–§5 — 값과 참조, 수명, 배치, 클래스와 RAII, 소유권 — 를 읽고 스스로 점검 1–4에 답한다. **두 번째 — 제어기와 그 틱.** §6, §7, §9를 읽고, 그 모든 것으로 틱 하나를 세는 계산 절을 따라간 뒤, 스스로 점검 5와 7에 답하고 문제 3의 코드 리뷰를 한다. §8은 빌드가 처음 실패할 때, §10은 새니타이저가 처음 말할 때 읽는다. 문제 1–2와 *더 깊이* 콜아웃은 두 번째 읽기로 미뤄도 된다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P6**를 카탈로그 숫자 그대로 쓴다. 직선 위의 카트, 위치 $p$는 미터, 엔코더 $N=2048$ counts/m, 목표를 $f_v=50$ Hz로 발행하는 비전 노드, 엔코더를 읽고 모터를 $f_c=200$ Hz로 명령하는 제어기, 그리고 카메라 노출 중간부터 힘이 걸릴 때까지 70 ms의 예산이다. 주기와 주파수는 서로 역수이므로 제어 주기는 $T=1/f_c=5$ ms, 비전 주기는 $T_v=1/f_v=20$ ms다.

이 페이지는 그 제어기를 C++ 프로그램 하나로 쓰고, 프로그램 자신의 숫자를 여기서 고정한다. 카탈로그가 아니라 이 페이지의 숫자이며, 다른 어떤 페이지도 이 숫자에 기대지 않는다.

| 이름 | 값 | 무엇인가 |
|---|---|---|
| `EncoderSample`, 처음 쓴 그대로 | `bool valid;` `std::int64_t stamp_ns;` `std::int32_t counts;` | 엔코더 읽기 한 번: 유효 플래그, 나노초 단위 읽은 시각, 카운트 |
| `EncoderSample` (§3) | `std::int64_t stamp_ns;` `std::int32_t counts;` `bool valid;` | 같은 세 필드를 정렬이 큰 순서로 |
| `TickRecord` | `std::int64_t stamp_ns;` 다음에 `double` 셋: `goal_m`, `position_m`, `effort` | 실행 로그의 한 줄 |
| $K$ | 샘플 5개 | 링 버퍼 `RingBuffer<EncoderSample, 5>`. 속도를 $(K-1)T=20$ ms, 곧 비전 주기 하나에 걸쳐 잰다 |
| 실행 | 60 s = 틱 12,000번 | 시험 실행 한 번, 따라서 로그의 길이 |
| $k_p$, $k_d$ | m당 2.0, m/s당 0.5 | PD 이득. `effort`는 $[-1,1]$로 정규화한 명령 |
| 모의 카트 | 최대 노력에서 0.5 m/s | §9의 시험 실행에서만 쓴다 |
| `MotorInterface` | `enable()`, `disable()`, `set_effort(double)` | 제어기와 구동기 사이의 이음매. `SimMotor`와 `RealMotor`가 구현한다(§7) |

이 페이지의 바이트 수는 x86-64와 ARM64의 64비트 리눅스, 그리고 목록을 실제로 돌린 ARM64 맥에서 성립한다. 그 가운데 무엇을 언어가 정하고 무엇을 플랫폼이 정하는지는 §3이 말한다.

*범위: 로보틱스 연구자가 로봇 코드를 읽고 고치고 디버깅하는 데 필요한 C++ — 값·참조·포인터, 수명, 배치, 클래스와 RAII, 소유권, 템플릿과 컨테이너, 인터페이스, CMake 빌드, 실시간 틱의 규칙, 그리고 그 규칙이 금하는 것을 잡아내는 도구 — 를 모두 P6의 제어기 위에서 가르친다. C++ 전체는 가르치지 않고(§10이 지도를 준다), ROS 2의 C++ API([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]), ament와 colcon([[04-robotics/ros2/workspaces-packages-launch|25.4]]), ros2_control 하드웨어 컴포넌트([[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]])도 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 440" style="max-width:100%;height:auto" role="img" aria-label="패널 두 개. (a) P6의 엔코더 샘플을 바이트 단위로 그린 것: 처음 쓴 그대로는 1바이트 valid 플래그, 패딩 7바이트, 8바이트 스탬프, 4바이트 카운트, 꼬리 패딩 4바이트로 24바이트, 스탬프를 앞에 두어 재배치하면 패딩 3바이트를 포함해 16바이트. (b) 틱 도중 프로세스의 메모리: main의 스택 프레임이 노드를 가리키는 shared_ptr을 사용 횟수 1로 들고 있고, 힙 위의 노드는 사용 횟수 1인 타이머와 제어기를 들고 있으며, 제어기는 unique_ptr로 모터를 소유하고 96바이트 링 버퍼를 제자리에 두며 예약된 로그 저장소 384,000바이트를 소유한다. 타이머의 콜백은 this로 노드를 관찰하고, executor는 weak_ptr로 타이머를 관찰한다.">
  <defs><marker id="cppArk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="8" y="16" font-size="12" fill="currentColor">(a) EncoderSample, 칸 하나가 1바이트, 재배치 전과 후</text>
  <text x="8" y="41" font-size="11" fill="currentColor">쓴 그대로</text>
  <text x="8" y="53" font-size="10" fill="currentColor" fill-opacity="0.8">24 B · 패딩 11</text>
  <rect x="104" y="30" width="18" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="113" y="46" font-size="10" fill="currentColor" text-anchor="middle">v</text>
  <rect x="122" y="30" width="126" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="185" y="46" font-size="10" fill="currentColor" text-anchor="middle">패딩 7</text>
  <rect x="248" y="30" width="144" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="320" y="46" font-size="10" fill="currentColor" text-anchor="middle">stamp_ns (8)</text>
  <rect x="392" y="30" width="72" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="428" y="46" font-size="10" fill="currentColor" text-anchor="middle">counts (4)</text>
  <rect x="464" y="30" width="72" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="500" y="46" font-size="10" fill="currentColor" text-anchor="middle">패딩 4</text>
  <g stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"><line x1="122" y1="30" x2="122" y2="35"/><line x1="122" y1="49" x2="122" y2="54"/><line x1="140" y1="30" x2="140" y2="35"/><line x1="140" y1="49" x2="140" y2="54"/><line x1="158" y1="30" x2="158" y2="35"/><line x1="158" y1="49" x2="158" y2="54"/><line x1="176" y1="30" x2="176" y2="35"/><line x1="176" y1="49" x2="176" y2="54"/><line x1="194" y1="30" x2="194" y2="35"/><line x1="194" y1="49" x2="194" y2="54"/><line x1="212" y1="30" x2="212" y2="35"/><line x1="212" y1="49" x2="212" y2="54"/><line x1="230" y1="30" x2="230" y2="35"/><line x1="230" y1="49" x2="230" y2="54"/><line x1="248" y1="30" x2="248" y2="35"/><line x1="248" y1="49" x2="248" y2="54"/><line x1="266" y1="30" x2="266" y2="35"/><line x1="266" y1="49" x2="266" y2="54"/><line x1="284" y1="30" x2="284" y2="35"/><line x1="284" y1="49" x2="284" y2="54"/><line x1="302" y1="30" x2="302" y2="35"/><line x1="302" y1="49" x2="302" y2="54"/><line x1="320" y1="30" x2="320" y2="35"/><line x1="320" y1="49" x2="320" y2="54"/><line x1="338" y1="30" x2="338" y2="35"/><line x1="338" y1="49" x2="338" y2="54"/><line x1="356" y1="30" x2="356" y2="35"/><line x1="356" y1="49" x2="356" y2="54"/><line x1="374" y1="30" x2="374" y2="35"/><line x1="374" y1="49" x2="374" y2="54"/><line x1="392" y1="30" x2="392" y2="35"/><line x1="392" y1="49" x2="392" y2="54"/><line x1="410" y1="30" x2="410" y2="35"/><line x1="410" y1="49" x2="410" y2="54"/><line x1="428" y1="30" x2="428" y2="35"/><line x1="428" y1="49" x2="428" y2="54"/><line x1="446" y1="30" x2="446" y2="35"/><line x1="446" y1="49" x2="446" y2="54"/><line x1="464" y1="30" x2="464" y2="35"/><line x1="464" y1="49" x2="464" y2="54"/><line x1="482" y1="30" x2="482" y2="35"/><line x1="482" y1="49" x2="482" y2="54"/><line x1="500" y1="30" x2="500" y2="35"/><line x1="500" y1="49" x2="500" y2="54"/><line x1="518" y1="30" x2="518" y2="35"/><line x1="518" y1="49" x2="518" y2="54"/></g>
  <text x="104" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="248" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">8</text>
  <text x="392" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">16</text>
  <text x="536" y="66" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">24</text>
  <text x="8" y="87" font-size="11" fill="currentColor">재배치</text>
  <text x="8" y="99" font-size="10" fill="currentColor" fill-opacity="0.8">16 B · 패딩 3</text>
  <rect x="104" y="76" width="144" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="176" y="92" font-size="10" fill="currentColor" text-anchor="middle">stamp_ns (8)</text>
  <rect x="248" y="76" width="72" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="284" y="92" font-size="10" fill="currentColor" text-anchor="middle">counts (4)</text>
  <rect x="320" y="76" width="18" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="329" y="92" font-size="10" fill="currentColor" text-anchor="middle">v</text>
  <rect x="338" y="76" width="54" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="92" font-size="10" fill="currentColor" text-anchor="middle">패딩 3</text>
  <g stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"><line x1="122" y1="76" x2="122" y2="81"/><line x1="122" y1="95" x2="122" y2="100"/><line x1="140" y1="76" x2="140" y2="81"/><line x1="140" y1="95" x2="140" y2="100"/><line x1="158" y1="76" x2="158" y2="81"/><line x1="158" y1="95" x2="158" y2="100"/><line x1="176" y1="76" x2="176" y2="81"/><line x1="176" y1="95" x2="176" y2="100"/><line x1="194" y1="76" x2="194" y2="81"/><line x1="194" y1="95" x2="194" y2="100"/><line x1="212" y1="76" x2="212" y2="81"/><line x1="212" y1="95" x2="212" y2="100"/><line x1="230" y1="76" x2="230" y2="81"/><line x1="230" y1="95" x2="230" y2="100"/><line x1="248" y1="76" x2="248" y2="81"/><line x1="248" y1="95" x2="248" y2="100"/><line x1="266" y1="76" x2="266" y2="81"/><line x1="266" y1="95" x2="266" y2="100"/><line x1="284" y1="76" x2="284" y2="81"/><line x1="284" y1="95" x2="284" y2="100"/><line x1="302" y1="76" x2="302" y2="81"/><line x1="302" y1="95" x2="302" y2="100"/><line x1="320" y1="76" x2="320" y2="81"/><line x1="320" y1="95" x2="320" y2="100"/><line x1="338" y1="76" x2="338" y2="81"/><line x1="338" y1="95" x2="338" y2="100"/><line x1="356" y1="76" x2="356" y2="81"/><line x1="356" y1="95" x2="356" y2="100"/><line x1="374" y1="76" x2="374" y2="81"/><line x1="374" y1="95" x2="374" y2="100"/></g>
  <text x="104" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">0</text>
  <text x="248" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">8</text>
  <text x="320" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">12</text>
  <text x="392" y="112" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">16</text>
  <text x="8" y="132" font-size="10" fill="currentColor">v = valid (bool, 1 B) · int64 8 B · int32 4 B · 음영 = 패딩 · 5칸 링: 136 B → 96 B</text>
  <text x="8" y="156" font-size="12" fill="currentColor">(b) 틱 도중의 메모리: 실선 화살표는 소유, 점선 화살표는 관찰</text>
  <rect x="8" y="166" width="124" height="266" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <text x="16" y="182" font-size="11" fill="currentColor" font-weight="bold">스택</text>
  <text x="16" y="196" font-size="10" fill="currentColor" fill-opacity="0.8">main의 프레임</text>
  <rect x="16" y="206" width="108" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="22" y="221" font-size="10" fill="currentColor">node: shared_ptr</text>
  <rect x="16" y="382" width="108" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="22" y="397" font-size="10" fill="currentColor">executor</text>
  <rect x="144" y="166" width="408" height="266" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.55"/>
  <text x="152" y="182" font-size="11" fill="currentColor" font-weight="bold">힙</text>
  <rect x="156" y="190" width="360" height="140" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="164" y="206" font-size="11" fill="currentColor" font-weight="bold">CartNode</text>
  <text x="164" y="222" font-size="10" fill="currentColor">timer_: shared_ptr&lt;Timer&gt;</text>
  <rect x="176" y="230" width="300" height="92" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="184" y="245" font-size="10" fill="currentColor" font-style="italic">controller_: CartController, 노드 안에 저장</text>
  <text x="184" y="262" font-size="10" fill="currentColor">motor_: unique_ptr&lt;MotorInterface&gt;</text>
  <text x="184" y="278" font-size="10" fill="currentColor">history_: RingBuffer, 96 B, 제자리</text>
  <text x="184" y="294" font-size="10" fill="currentColor">log_: vector&lt;TickRecord&gt;</text>
  <text x="184" y="310" font-size="10" fill="currentColor">goal_m_: atomic&lt;double&gt;</text>
  <rect x="156" y="342" width="100" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="206" y="358" font-size="10" fill="currentColor" text-anchor="middle">SimMotor 또는</text>
  <text x="206" y="373" font-size="10" fill="currentColor" text-anchor="middle">RealMotor</text>
  <rect x="268" y="342" width="164" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="350" y="358" font-size="10" fill="currentColor" text-anchor="middle">로그 저장소</text>
  <text x="350" y="373" font-size="10" fill="currentColor" text-anchor="middle">12,000 × 32 B = 384,000 B</text>
  <rect x="444" y="342" width="100" height="40" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="494" y="358" font-size="10" fill="currentColor" text-anchor="middle">Timer</text>
  <text x="494" y="373" font-size="10" fill="currentColor" text-anchor="middle">콜백: this</text>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <line x1="124" y1="217" x2="155" y2="217" marker-end="url(#cppArk)"/>
    <polyline points="318,219 494,219 494,341" marker-end="url(#cppArk)"/>
    <polyline points="182,258 168,258 168,341" marker-end="url(#cppArk)"/>
    <polyline points="330,290 344,290 344,341" marker-end="url(#cppArk)"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3">
    <polyline points="544,362 550,362 550,200 517,200" marker-end="url(#cppArk)"/>
    <polyline points="124,393 138,393 138,416 494,416 494,383" marker-end="url(#cppArk)"/>
  </g>
  <text x="140" y="211" font-size="10" fill="currentColor" text-anchor="middle" font-weight="bold">1</text>
  <text x="500" y="290" font-size="10" fill="currentColor" font-weight="bold">1</text>
  <text x="533" y="282" font-size="10" fill="currentColor" text-anchor="middle">this</text>
  <text x="316" y="428" font-size="10" fill="currentColor" text-anchor="middle">weak_ptr</text>
</svg>

위: P6의 엔코더 샘플을 칸 하나에 1바이트씩 그렸다. 처음 쓴 그대로는 24바이트이고 그중 11바이트가 패딩이며, 8바이트 스탬프를 앞에 두면 16바이트, 그중 3바이트가 패딩이다. 그래서 인덱스 둘을 포함한 5칸 링은 136바이트 대신 96바이트를 차지한다. 아래: 루프가 도는 동안의 프로세스 메모리다. `main`의 프레임이 노드를 가리키는 `shared_ptr`을 들고 있고(사용 횟수 1, `spin`이 자기 사본을 쥐는 동안은 2), 노드는 자기 타이머(사용 횟수 1)와 제어기를 소유하며, 제어기는 구동기와 예약된 로그 384,000바이트를 소유한다. 타이머의 콜백은 `this`로 노드를 관찰하고, executor는 `weak_ptr`로 타이머를 관찰한다.

### 1. 값, 참조, 포인터

*한 문장으로:* Python에서 온 사람이 처음 놀라는 것은 C++ 변수가 값 자체를 담는다는 점이어서, 값으로 함수에 넘기면 모든 바이트가 복사되고, 참조와 포인터는 그 복사 없이 함수가 객체에 닿는 방법이다 — 참조는 반드시 무언가를 가리켜야 하는 두 번째 이름이고, 포인터는 null일 수 있는 주소다.

Python에서 이름은 객체를 가리키고, 함수에 넘기면 그 가리킴이 넘어간다. 아무것도 복사되지 않는다. C++는 반대다. `EncoderSample b = a;`는 샘플을 하나 더 만들고 `a`의 16바이트를 거기로 복사하며, `EncoderSample` 타입의 매개변수는 인자를 복사해 초기화한 새 객체다. 16바이트 구조체라면 거의 공짜다. `std::vector`라면 힙 메모리 블록을 새로 잡고 원소를 전부 복사한다는 뜻이다(§6). 벡터를 복사하면 손잡이가 아니라 담긴 것이 복사되기 때문이다.

영어 절의 첫 목록 `pass.cpp`는 P6의 샘플을 함수에 넘기는 네 가지 방법이고, 각 함수가 어느 방법을 쓰는지는 매개변수 타입이 말한다. 출력은 두 줄이다. 첫 줄에서 미터로 0.3999, 이동한 사본 0.3950, 호출자는 여전히 819 카운트를 갖고 있다. 둘째 줄에서 포인터로 읽은 값은 0.3999 m, null 포인터로는 "no sample", `zero()` 뒤에는 0 카운트다.

본문이 아니라 네 서명을 읽는다. `const EncoderSample&`, 곧 const 참조는 머신 워드 몇 개보다 큰 것을 읽을 때의 기본값이다. 복사가 없고, 그것을 통한 쓰기는 컴파일러가 거부하므로 호출자는 자기 샘플이 바뀌지 않고 돌아온다는 것을 안다. 값으로 받는 `EncoderSample s`는 호출된 쪽이 바꿀 자기 사본을 원할 때 맞다. `shifted`가 그렇다. 출력 첫 줄에서 사본은 809로 옮겨졌지만 호출자의 819 카운트는 그대로다. const가 아닌 참조 `EncoderSample&`는 출력이다. `zero`가 그것을 통해 썼고 호출자는 0을 봤다. 포인터 `const EncoderSample*`는 넷 가운데 유일하게 null이 됨으로써 "샘플이 없다"고 말할 수 있고, 그래서 쓰기 전에 검사해야 하는 유일한 것이다. null 포인터를 통해 읽으면 정의되지 않은 동작(§2에서 정의)이다. 예외도 아니고 확실한 충돌도 아니며, 언어가 더는 기술하지 않는 프로그램이 될 뿐이다.

`const`는 컴파일러가 강제하는 약속이다. 변수에(`const double p`), 매개변수에(`const EncoderSample&`), 멤버 함수에(`double effort() const`는 자기가 불린 객체를 바꾸지 않겠다고 약속한다) 붙는다. 실행할 때는 비용이 없고, 쓸모는 프로그램을 읽을 때 드러난다. 2,000줄짜리 드라이버를 읽는 사람에게 `const&` 매개변수는 이 호출이 인자를 바꿀 수 없다고 알려 준다. ROS 2 클라이언트 라이브러리도 메시지 소유를 같은 방식으로 적는다. `const std_msgs::msg::String & msg`로 선언한 구독 콜백은 메시지를 참조로 받고 바꾸지 않겠다고 약속한다([[04-robotics/ros2/nodes-topics-messages|25.2 §6]]).

**200 Hz에서 각각의 값.** `EncoderSample`을 값으로 넘기면 호출마다 16바이트, 틱마다 한 번이면 초당 3,200바이트를 복사하고, 5칸 링 버퍼 전체를 값으로 넘겨도 호출마다 96바이트다. 링의 저장 공간이 객체 안에 있으므로 여전히 할당은 없다(§6). 60 s 실행의 모든 샘플을 담은 `std::vector<EncoderSample>`는 다르다. 값으로 넘기면 실행 끝에서 호출마다 $12{,}000\times16=192{,}000$바이트와 힙 할당 한 번, 곧 초당 38.4 MB와 할당 200번이고, 계산 절이 이것을 세고 §9가 시간을 잰다. 어느 것이든 `const&`로 넘기면 주소 하나, 8바이트다. C++ Core Guidelines는 이 규칙을 F.16으로 적는다. "입력" 매개변수는 복사가 싼 타입이면 값으로, 아니면 const 참조로 넘긴다.

> **포인터의 정의.** **포인터**(pointer)는 *값이 주소인 객체*이고, `T*`로 쓰는 복합 타입이다. 가리키는 객체 자체도 아니고 참조도 아니다. 정의 조건 셋. **그 자체가 객체다.** 자기 저장 공간(이 페이지의 플랫폼에서 8바이트)과 자기 수명을 갖고, 다른 곳을 가리키도록 다시 대입할 수 있다. 값은 **네 종류 중 하나다.** 객체나 함수를 가리키는 포인터, 배열의 끝 하나 뒤를 가리키는 포인터, null 포인터 값, 그리고 저장 공간이 해제된 객체를 가리키던 것 같은 무효한 포인터 값이다. 그리고 **그것을 통한 읽기와 쓰기는 첫째 종류에서만 정의된다.** null이거나 무효하거나 끝을 지난 포인터에 `*p`나 `p->counts`를 쓰면 정의되지 않은 동작이고, 프로그램이 대개 검사로 스스로 막아야 한다.
>
> $$\mathrm{addr}(p+i)=\mathrm{addr}(p)+i\,\mathrm{sizeof}(T),\qquad 0\le i\le n$$
>
> $p$는 $T$ 타입 원소 $n$개짜리 배열의 0번 원소를 가리키고 $i$는 첨자다. 그러므로 포인터 산술은 원소 단위로 움직이고, $p+n$은 끝 하나 뒤를 가리키므로 만들 수는 있지만 그것을 통해 읽을 수는 없다.
>
> - **예**: P6 샘플 다섯 개짜리 배열을 가리키는 `const EncoderSample*`. `p + 1`은 16바이트 뒤, 다음 샘플이고 `p + 5`는 끝을 표시한다. 목록에서 `metres_if_valid(&s, &p)`는 포인터 둘을 받아 둘 다 통해 읽었고, `metres_if_valid(nullptr, &p)`는 먼저 검사했으므로 `false`를 돌려주었다.
> - **비예**: 참조. null 값이 없고 다시 묶을 수 없으며 검사가 필요 없다. 그래서 F.16은 반드시 있어야 하는 인자에 `const&`를 권하고, 포인터는 "없음"이 정당한 답인 경우에 남겨 둔다.
> - **왜 중요한가**: 드라이버, C 라이브러리, rclcpp 코드의 모든 `->`가 포인터를 건넨다. 그리고 로봇에서 포인터가 실패하는 두 방식, null과 댕글링은 모두 정의되지 않은 동작으로 실패하며, §10의 새니타이저가 그것을 잡으려고 있다.

> **참조의 정의.** **참조**(reference)는 *별칭*, 곧 이미 있는 객체의 두 번째 이름이며 `T&`나 `const T&`로 선언한다. 객체가 아니고, 저장 공간을 전혀 차지하지 않을 수도 있다. 정의 조건 넷. **초기화할 때 묶이며**, 유효한 객체에 묶여야 한다. null 참조도, 초기화되지 않은 참조도 없다. **다시 묶이지 않는다.** `r`에 대입하면 `r`이 가리키는 객체에 쓴다. **객체의 정체를 그대로 갖는다.** `r`의 주소와 크기는 그 객체의 주소와 크기다. 그리고 **const 참조**는 그것을 통한 쓰기를 막고 임시 객체에도 묶일 수 있으며, 지역 선언에서는 그 임시 객체의 수명을 자기 수명까지 늘린다.
>
> $$\&r=\&x,\qquad \mathrm{sizeof}(r)=\mathrm{sizeof}(x)$$
>
> $r$은 객체 $x$에 묶인 참조다. 그러므로 `const&` 매개변수는 $x$가 아무리 커도 복사 비용이 없는데, 호출된 쪽이 $x$ 자체를 다루기 때문이다.
>
> - **예**: `metres(const EncoderSample& s)`는 호출자의 16바이트 샘플을 제자리에서 다룬다. 그 안에서 `&s`는 호출자의 `&s`이고, `sizeof(s)`는 주소의 크기가 아니라 16이다.
> - **비예**: `latest()`가 자기 지역 변수에 대한 참조를 돌려주는 `const EncoderSample& s = latest();`(§2). 참조는 묶였지만, 그 객체의 수명은 `latest`가 돌아올 때 끝났다. 댕글링 참조다. 참조라는 사실은 이름이 묶였다는 것만 보장하지, 객체가 아직 살아 있다는 것은 보장하지 않는다.
> - **왜 중요한가**: `const&`는 틱이 메시지나 버퍼나 궤적을 복사 없이 읽는 방법이고, 댕글링 참조는 그것이 누구의 객체인지 잊은 값이다.

### 2. 객체의 수명: 스택, 힙, 댕글링 참조

*한 문장으로:* C++의 고전적인 충돌은 이미 사라진 객체를 쓰는 것인데, 모든 객체는 생성이 끝난 순간부터 소멸이 시작되는 순간까지 존재하고, 그 두 순간이 언제 오는지는 저장 기간이 정하며 — 지역 변수는 닫는 중괄호에서, 힙 객체는 `delete`나 소유자의 끝에서 끝난다 — 두 번째 순간 뒤에 쓰인 참조나 포인터는 댕글링이고, 그것을 쓰는 것은 정의되지 않은 동작이다.

언어는 모든 객체에 네 가지 저장 기간 중 하나를 준다. **자동**: 블록 안에서 `static` 없이 선언한 변수, 함수 매개변수, 임시 객체다. 저장 공간은 블록을 나갈 때까지 유지되고, 닫는 중괄호에서 만들어진 순서의 역순으로 소멸한다. **정적**: 네임스페이스 범위의 변수와 `static` 지역 변수로, 프로그램 내내 산다. **스레드**: `thread_local` 변수로, 스레드마다 하나다. **동적**: `new`로 만든 객체로, `delete`까지 — 이 페이지의 코드에서는 그것을 소유한 객체가 끝날 때까지 — 산다. 표준은 이 기간들을 정의할 뿐 저장 공간이 어디 있는지는 말하지 않으며, 스택과 힙이 흔한 답이다. 자동 객체는 호출 스택 위 자기 함수의 프레임에 살다가 함수가 돌아올 때 풀리고, 동적 객체는 할당자가 요청에 따라 내주는 메모리에 산다. 아래에서 두 낱말은 이 뜻으로 쓴다.

§9의 틱에서 `const double p = ...`는 자동이다. 그 줄부터 몇 나노초 뒤의 닫는 중괄호까지 존재한다. §9의 시험 실행에서 제어기는 `main` 안의 자동 객체이므로 실행 내내 산다. 제어기가 소유한 모터와 로그 저장 공간은 동적이다. 루프 전에 한 번 할당되고, 제어기가 소멸할 때 풀린다.

**로봇 코드가 `new`나 `delete`를 거의 쓰지 않는 이유.** `new T(args)`는 저장 공간을 할당하고 거기에 `T`를 생성하며, `delete p`는 객체를 소멸시키고 저장 공간을 푼다. 모든 `new`에는 그것을 만든 코드를 빠져나가는 모든 경로 — 정상 반환, 각각의 이른 `return`, 각각의 예외 — 에서 정확히 한 번의 `delete`가 필요한데, 그 짝이 맞는지 컴파일러가 확인하게 할 방법은 없다. 하나를 빠뜨리면 새고, 하나가 더 많으면 정의되지 않은 동작이다. §4와 §5는 그 장부를 소멸자가 대신 적는 객체에 넘긴다. 여럿이면 컨테이너, 하나면 `std::unique_ptr`, 소유가 정말로 공유되면 `std::shared_ptr`이다. 그다음부터 코드 리뷰에서 `new`는 질문이고 `delete`는 거의 늘 버그다.

**첫 번째 댕글링 참조: 반환된 지역 변수의 참조.** 영어 절의 `return_local.cpp`는 일부러 틀리게 쓴 목록이다. `latest()`가 자기 프레임에 사는 지역 `s`의 참조를 돌려준다. 컴파일러는 이것을 보고, 켜 두지 않아도 기본으로 경고한다: `reference to stack memory associated with local variable 's' returned [-Wreturn-stack-address]`. 그래도 실행하면 이 맥에서는 `819 counts`를 찍는다. 이미 돌아온 함수의 프레임에서, 아직 아무것도 덮어쓰지 않았기 때문에 맞는 숫자를 읽은 것이다. 이것이 정의되지 않은 동작의 위험한 절반이다. 맞아 보일 수 있다. 리눅스에서는 기본값인 `ASAN_OPTIONS=detect_stack_use_after_return=1`로 실행하면 AddressSanitizer가 읽는 자리에서 멈추고 `stack-use-after-return`을 보고한다. `latest()`의 프레임에서 `s`가 32–48바이트를 차지했고, 오프셋 40에서 4바이트를 읽었다. 샘플 안에서 8바이트 지점에 있는 `counts`를 읽은 것이다. 고치는 법은 16바이트 샘플을 값으로 돌려주는 것이다. C++ Core Guidelines는 이 규칙을 F.43으로 적는다. 지역 객체에 대한 포인터나 참조를 절대 돌려주지 마라.

**두 번째: 자기 객체보다 오래 사는 콜백.** 로봇 프로그램은 콜백을 등록하는 코드보다 오래 사는 것에 콜백을 등록한다. executor, 드라이버의 이벤트 목록, 스레드다. 그러면 `this`를 캡처한 콜백은, 수명이 콜백과 아무것으로도 묶이지 않은 객체를 가리키는 포인터가 된다. 영어 절의 `callback_outlives.cpp`가 일부러 틀리게 쓴 예다. 첫 `run_once()`는 잘 돌고 걸러진 목표 `0.080 m`를 찍는다. 0.40 m를 향해 0.2만큼 한 걸음 간 값이다. 그다음 `filter.reset()`이 필터를 소멸시키고, 람다를 여전히 쥔 스케줄러가 해제된 메모리 위에서 `update()`를 부른다. AddressSanitizer의 보고는 §10에 있다. 새니타이저가 없으면 이 갱신은 할당자가 그사이 그 자리에 둔 무언가에 쓴다. 고치는 법은 둘이다. 객체의 소유자가 등록도 소유하게 해서 둘이 함께 끝나게 하거나, 콜백이 `std::weak_ptr`을 쥐고 검사하게 한다(§5). rclcpp의 흔한 방식이 앞의 것이다. 노드가 만든 타이머는 그 노드의 멤버가 살려 두므로, `this`를 캡처한 타이머 콜백은 노드보다 오래 살 수 없다(§5). 위험한 것은 다른 무언가 — 드라이버의 스레드, 다른 노드, 전역 목록 — 에 넘긴 콜백이다.

> **객체 수명의 정의.** 객체의 **수명**(lifetime)은 *그 객체가 존재하는, 프로그램 실행의 구간*이다. 객체마다의 성질이고, 저장 공간을 언제 얻고 언제 푸는지 정하는 규칙인 **저장 기간**(storage duration)이 정한다. 이름의 범위와는 다르다. 이름은 코드의 한 구간에서 보이고, 객체는 시간의 한 구간 동안 존재한다. 정의 조건 셋. 맞는 크기와 정렬의 저장 공간을 얻고 객체의 초기화 — 클래스라면 생성자 — 가 끝나면 **시작한다.** 클래스 타입이면 소멸자 호출이 시작될 때, 아니면 저장 공간이 풀리거나 재사용될 때 **끝난다.** 그리고 **그 구간 밖에서** 참조나 포인터를 통해 객체를 쓰는 것 — 읽기, 쓰기, 멤버 함수 호출 — 은 거기서 어떤 값이 보이든 정의되지 않은 동작이다.
>
> $$\text{a use of } x \text{ at time } t \text{ is defined}\iff t_{\text{init}}(x)\le t<t_{\text{destroy}}(x)$$
>
> $t_{\text{init}}$은 $x$의 초기화가 끝난 순간, $t_{\text{destroy}}$는 소멸이 시작된 순간이다. 그러므로 참조는 자기 객체보다 오래 살 수 있다. 객체가 끝날 때 참조를 줄여 주는 장치가 언어에 없기 때문이다.
>
> - **예**: §9의 시험 실행에서 제어기는 `main` 안의 자동 객체다. $t_{\text{init}}$은 선언이고 $t_{\text{destroy}}$는 틱 12,000번 뒤 `main`의 닫는 중괄호다. 로그 저장 공간은 동적이지만 제어기가 소유하므로 정확히 그만큼 산다.
> - **비예**: `latest()` 안의 샘플 `s`. 수명은 `latest`의 닫는 중괄호에서, 호출자가 처음 읽기 전에 끝난다. 호출자의 참조는 댕글링이고, 이 맥에서 맞는 819가 찍혔다고 그 읽기가 정의되는 것은 아니다.
> - **왜 중요한가**: 로봇 프로그램에서 중요한 수명은 콜백, 스레드, 드라이버의 것이고, 이들은 자기를 설정한 코드보다 오래 산다. 새니타이저가 찾는 해제 후 사용은 하나하나가 누군가 가정한 수명이다.

> **정의되지 않은 동작의 정의.** **정의되지 않은 동작**(undefined behaviour)은 *C++ 표준이 특정 연산에 매기는 범주로, 그런 연산을 하는 실행에 대해 표준은 프로그램이 무엇을 하든 아무 요구도 하지 않는다*. 실행 안의 연산이 가진 성질이며 오류 메시지가 아니다. 정의 조건 셋. 그 연산은 **표준이 정의되지 않았다고 이름 붙인 것**이다. 수명 밖의 객체 사용, null 포인터를 통한 읽기, 배열 밖의 첨자, 부호 있는 정수 오버플로, 스레드 사이의 데이터 경쟁, 가상 소멸자가 없는 기반 클래스를 통한 파생 객체 삭제(§7)다. **진단이 요구되지 않는다.** 컴파일러는 경고하지 않아도 되고 프로그램은 죽지 않아도 된다. 그리고 **컴파일러는 그것이 일어나지 않는다고 가정해도 되며** 그 가정 위에서 최적화하므로, 그 효과는 옮겨 가거나 사라지거나 최적화 수준에 따라 바뀔 수 있다. 이웃한 두 범주는 다르다. *구현 정의* 동작은 플랫폼마다 다르지만 각 플랫폼이 자기 선택을 문서화한다. `bool`의 크기가 그 예다. *미지정* 동작은 허용된 여러 결과 중 하나이되 어느 것인지 밝히지 않는다. 함수 인자들이 평가되는 순서가 그 예다.
>
> $$\exists\,k:\ \mathrm{op}_k\ \text{undefined}\ \Rightarrow\ \text{no requirement on that execution}$$
>
> $\mathrm{op}_k$는 입력 하나에 대한 실행 하나의 $k$번째 연산이다. 정의되지 않은 연산 하나가 그 실행에 대한 요구를 모두 지우므로, 실행은 가장 나쁜 연산만큼만 정의된다.
>
> - **예**: `return_local`은 이 맥의 평범한 실행에서 `819 counts`를 찍었고, 계측한 실행에서는 AddressSanitizer에 멈췄다. 둘 다 허용되며, 어느 쪽도 "그" 동작이 아니다.
> - **비예**: 예외. §4 목록의 `throw`는 완전히 정의되어 있다. 스택이 풀리고, 소멸자가 돌고, 핸들러가 잡는다. 정의되지 않은 동작에는 그런 장치가 없다.
> - **왜 중요한가**: 로봇에서 정의되지 않은 동작은 벤치 시험을 통과하고 현장에서 실패하는 결함이다. 그것이 하는 일이 메모리에 우연히 무엇이 있느냐에 달렸기 때문이다. 경고와 새니타이저(§10)가 많이 찾아 주지만, 전부 찾아 주는 것은 없다.

> [!note]- 더 깊이 · Deeper
> **정의되지 않은 동작은 얼마나 거슬러 올라가는가.** C++17에서 표준은 정의되지 않은 연산 이전에 프로그램이 한 일조차 보호하지 않는다(N4659로 본 C++17 표준의 [intro.execution]/5). 현재 작업 초안은 이를 좁혀, 그 이전의 관측 가능한 동작은 지킨다([intro.abstract]/6).

### 3. 메모리 배치: sizeof, 정렬, 패딩

*한 문장으로:* 샘플은 필드를 더한 것보다 많은 바이트를 치르는데, 모든 타입에는 크기와 정렬이 있고, 구조체는 멤버를 선언 순서대로 각자 정렬의 배수인 오프셋에 놓은 뒤 자기 크기를 가장 큰 정렬의 배수로 올리기 때문이며, 그래서 필드의 순서가 샘플이 모든 버퍼·로그·복사를 거치며 끌고 다니는 패딩 바이트의 수를 정한다.

`sizeof(T)`는 `T` 타입 객체가 차지하는 바이트 수이고 패딩을 포함한다. `alignof(T)`는 정렬이다. `T` 타입 객체는 그 배수인 주소에서만 시작할 수 있다. 언어는 여기서 정하는 것이 아주 적다 — 클래스의 멤버가 선언 순서대로 할당된다는 것 정도다 — 그리고 나머지는 플랫폼의 ABI, 곧 그 플랫폼의 컴파일러들이 합의한 바이너리 규약의 몫이다. 로봇 컴퓨터가 쓰는 x86-64와 ARM64 리눅스, 그리고 이 페이지의 목록을 돌린 애플 노트북에서, 여기 쓰는 타입들은 일치한다. `bool`은 1바이트, `std::int32_t`는 4, `std::int64_t`와 `double`과 모든 포인터는 8이며, 각자 자기 크기로 정렬된다. 그다음 두 규칙이 멤버 크기를 구조체 크기로 바꾼다. 구조체는 가장 크게 정렬된 멤버처럼 정렬되고, 크기는 모든 멤버를 담는 그 정렬의 배수 가운데 가장 작은 것이다.

> [!note]- 더 깊이 · Deeper
> **언어가 정하는 것, ABI가 더하는 것.** 좁은 문자 타입(`char`와 그 signed, unsigned 형)의 `sizeof`는 1이고, 그 밖의 모든 기본 타입의 크기는 구현 정의이며, 모든 정렬은 2의 거듭제곱이고, 클래스의 멤버는 선언 순서대로 앞의 멤버보다 높은 주소에 할당된다. 나머지는 ABI — x86-64 리눅스는 System V x86-64 psABI, ARM64 리눅스는 Arm의 AAPCS64 — 의 몫이고, 두 문서는 구조체의 두 규칙을 거의 같은 말로 적는다. 세 플랫폼은 같은 `static_assert`를 clang으로 각 타깃에 대해 컴파일해 확인했다.

영어 절의 `layout.cpp`가 두 순서의 크기, 정렬, 오프셋을 찍는다. 처음 쓴 그대로는 크기 24, 정렬 8, 오프셋 `valid` 0, `stamp_ns` 8, `counts` 16이다. 재배치하면 크기 16, 정렬 8, 오프셋 `stamp_ns` 0, `counts` 8, `valid` 12다. 데이터는 13바이트이고 패딩은 11바이트와 3바이트, 샘플 다섯 개는 120바이트와 80바이트다.

첫 순서를 따라가 본다. `valid`는 오프셋 0에서 1바이트를 차지한다. `stamp_ns`는 8의 배수인 오프셋이 필요하므로 8로 가고, 1–7바이트는 패딩이다. `counts`는 4의 배수가 필요한데 16이 그렇으므로 16–19바이트를 차지한다. 멤버는 20에서 끝나지만 구조체의 정렬이 8이므로 크기는 24로 올라가고, 20–23바이트는 꼬리 패딩이다. 24바이트 안에 데이터가 13바이트다. 재배치하면 `stamp_ns`가 0–7, `counts`가 8–11, `valid`가 12를 차지하고 크기는 13을 올린 16이다. 꼬리 패딩은 배열을 위해 있다. 샘플 배열의 모든 원소는 8의 배수에서 시작해야 하고, 그래서 `sizeof`가 꼬리 패딩을 포함하며 샘플 다섯 개가 정확히 `sizeof`의 다섯 배, 120바이트 대 80바이트다.

정렬이 큰 것부터 놓는 것이 경험칙이고, 여기서는 그것이 가능한 가장 작은 크기를 준다. 하지만 패딩을 늘 없애 주지는 않는다. 어떤 순서도 구조체를 페이로드를 정렬의 배수로 올린 값보다 작게 만들 수 없다. 여기서는 $\lceil 13/8\rceil\cdot 8=16$바이트이므로, 이 샘플은 이제 최소인 3바이트만 싣는다. 문제 1의 IMU 샘플은 최소에서도 1바이트가 남는 경우다.

P6에서 샘플 크기가 정하는 것. §6의 링 버퍼는 샘플 다섯 개를 제자리에 담고 8바이트 인덱스 둘을 더해, 처음 쓴 그대로의 $5\cdot24+16=136$바이트 대신 $5\cdot16+16=96$바이트다. `TickRecord`는 8바이트 필드 넷이라 패딩이 전혀 없는 32바이트이고, 그래서 60 s 로그는 $12{,}000\cdot32=384{,}000$바이트다. 200 Hz에서 샘플의 흐름은 $4{,}800$바이트 대신 초당 $16\cdot200=3{,}200$바이트다. 첫 판의 모든 버퍼, 로그, 복사에서 3분의 1이 패딩이었다.

바이트 수보다 더 위험한 결과가 하나 더 있다. 구조체의 날 바이트는 파일 형식도 통신 형식도 아니다. 패딩 바이트는 값의 일부가 아니라 의미 있는 것을 담지 않고, 배치는 하나의 ABI에 속하므로, 한 프로그램이 쓴 같은 바이트를 다르게 빌드된 다른 프로그램이 틀리게 읽을 수 있다. ROS 2 메시지를 미들웨어가 직렬화하는 이유가 이것이고([[04-robotics/ros2/nodes-topics-messages|25.2 §4]]가 메시지 정의를 읽는다), 디스크에 쓰는 로그는 필드 하나하나로 쓰거나 직렬화 라이브러리를 거쳐 써야 한다.

> **정렬과 패딩의 정의.** 타입의 **정렬**(alignment)은 *그 타입의 객체가 할당될 수 있는 연속한 주소 사이의 바이트 수*다. 구현이 정하는 2의 거듭제곱이고, 주어진 ABI 위에서 타입이 갖는 성질이다. **패딩**(padding)은 *객체의 바이트 가운데 어느 멤버에도 속하지 않는 것*으로, 정렬을 맞추려고 끼워 넣는다. 이 페이지의 ABI에서 구조체의 배치를 정하는 정의 조건 셋이며, 언어 자체가 보장하는 것은 순서뿐이다. 멤버는 **선언 순서대로 놓이며**, 각자 앞 멤버의 끝 이후에서 자기 정렬의 배수인 가장 낮은 오프셋에 놓인다. 구조체의 **정렬은 멤버 정렬 가운데 가장 큰 것**이다. 그리고 크기는 그 정렬의 배수로 **올려져**, 그 구조체의 배열에서도 모든 원소가 정렬된다.
>
> $$o_1=0,\quad o_i=\Big\lceil\frac{o_{i-1}+s_{i-1}}{a_i}\Big\rceil a_i,\qquad \mathrm{sizeof}(S)=\Big\lceil\frac{o_n+s_n}{a_S}\Big\rceil a_S,\quad a_S=\max_i a_i$$
>
> $s_i$, $a_i$, $o_i$는 구조체의 멤버 $n$개 가운데 $i$번째의 크기, 정렬, 오프셋이다. 그러므로 패딩은 올림이 보태는 몫이고, 각 오프셋이 앞 멤버에 달려 있으므로 순서에 따라 달라진다.
>
> - **예**: 처음 쓴 그대로는 $o=0,8,16$이고 멤버는 $16+4=20$에서 끝나며 $a_S=8$이므로 $\lceil 20/8\rceil\cdot 8=24$바이트, 그중 11바이트가 패딩이다. 재배치하면 $o=0,8,12$, 끝은 $13$이고 $\lceil 13/8\rceil\cdot 8=16$바이트, 패딩은 3바이트다. `layout.cpp`가 둘 다 찍었다.
> - **비예**: "구조체는 멤버의 합이다." 어느 순서든 13바이트가 나오고, 컴파일러는 그 어느 쪽과도 다르다.
> - **비예**: 다른 플랫폼으로 가져간 배치. 식은 일반적이지만 $s_i$와 $a_i$는 그렇지 않다. 언어는 `std::int32_t`와 `std::int64_t`의 비트 폭은 정하지만 정렬은 하나도 정하지 않으므로, x86-64에서 계산한 샘플 배치는 x86-64에 대한 주장이다.
> - **왜 중요한가**: 모든 샘플은 링에 복사되고 로그에 덧붙고 흔히 전송된다. 패딩은 샘플 주기마다 치러지며 — 여기서는 초당 $(24-16)\cdot200=1{,}600$바이트 — 배치는 두 프로그램이 그 바이트를 공유할 수 있는지부터 정한다.

### 4. 클래스, 불변식, RAII

*한 문장으로:* 켜진 구동기 같은 자원은 그것을 얻은 코드를 빠져나가는 모든 길에서 풀려야 하는데, C++는 그것을 클래스로 한다 — 클래스는 데이터를 그것에 대해 어떤 조건이 참이도록 지키는 함수와 묶고, 생성자는 그 조건을 세우고 소멸자는 끝내며, RAII는 그 짝을 이용해 자원을 객체에 묶어 객체의 범위를 빠져나가는 모든 경로에서 풀리게 한다.

클래스는 데이터 멤버와 멤버 함수를 선언하고, `private:` 멤버는 자기 함수만 건드릴 수 있다. 핵심은 **불변식**(invariant)이다. 멤버 함수 호출과 호출 사이에 그 클래스의 모든 객체에 대해 참인 조건이다. P6의 구동기라면 "이 객체가 존재하는 동안, 그리고 오직 그 동안 포트가 열려 있고 구동기가 켜져 있다"가 불변식이다. **생성자**(constructor)는 누가 무엇을 부르기 전에 불변식을 세운다. 멤버를 멤버 초기화 목록에 쓴 순서가 아니라 클래스에 선언한 순서대로 초기화한다. clang의 `-Wall`은 다른 순서로 쓴 목록을 짚는다(`-Wreorder-ctor`). 뒤에 선언된 멤버로 앞 멤버를 초기화하면 아직 존재하지 않는 값을 읽기 때문이다. **소멸자**(destructor)는 객체의 수명이 끝날 때, 곧 범위의 닫는 중괄호에서, `delete`에서, 또는 예외가 그 범위를 지나며 스택을 풀 때 돈다. 본문을 실행한 뒤 멤버를 선언의 역순으로 소멸시킨다.

RAII(resource acquisition is initialization, 자원 획득은 초기화)는 그 짝을 자원에 쓰는 것이다. 영어 절의 `raii.cpp`는 P6의 구동기를 클래스로 쓴 것이다. 포트 호출은 출력만 하는 대역이고, 실제 드라이버라면 그 자리에서 포트에 쓴다. 출력은 세 경우 모두 `cart0: open, enable` 다음에 `cart0: effort 0.0, disable, close`가 한 번씩 찍히고, 예외의 경우에는 그 뒤에 `caught: encoder read failed`가 찍힌다.

`run`을 빠져나가는 세 길 모두에서 구동기는 한 번씩 0을 명령받고 꺼진다. 루프가 끝날 때, 틱 2의 이른 `return`에서, 그리고 틱 1에서 던진 예외가 `run`을 지나 `main`의 핸들러로 갈 때다. 마지막 두 줄이 순서를 보여 준다. `caught`가 찍히기 전에 구동기가 풀린다. 핸들러가 돌기 전에 스택이 풀리고, `throw`와 핸들러 사이의 모든 자동 객체가 소멸하기 때문이다. `run`의 어느 줄도 정지를 말하지 않는다. 범위가 그것을 한다.

RAII가 못 하는 것. RAII는 언어가 범위를 떠날 때만 돈다. `std::exit`는 스택을 풀지 않으므로 자동 객체는 소멸하지 않는다. `std::abort`는 아무것도 소멸시키지 않는다. 잡히지 않은 예외가 `std::terminate` 전에 스택을 푸는지는 구현 정의다. 그리고 충돌, `SIGKILL`, 정전은 아무것도 돌리지 않는다. 그래서 실제 구동기에는 명령이 끊기면 구동기를 끄는 워치독과, 모든 소프트웨어 아래의 비상 정지도 필요하다. rclcpp가 하는 일은 기본으로 SIGINT와 SIGTERM 핸들러를 설치하는 것이다. Jazzy의 `rclcpp::init`은 따로 말하지 않으면 `SignalHandlerOptions::All`을 받는다. 그래서 Ctrl-C는 컨텍스트를 닫고, `spin`이 돌아오고, `main`이 돌아오고, 소멸자가 돈다.

**자원 소유자를 복사하면 버그다.** 컴파일러는 복사 생성자를 선언하지 않은 모든 클래스에 복사 생성자를 써 준다. 사용자가 쓴 소멸자가 있는 클래스에도 그렇게 하며, C++11은 이미 그것을 폐기 예정으로 돌렸다. `MotorDriver`의 사본은 원본과 포트를 공유하고 소멸자를 한 번 더 돌린다. 영어 절의 `raii_copy_wrong.cpp`가 일부러 틀리게 쓴 예다. 출력은 `open, enable`, 그다음 `effort 0, disable, close`, 그다음 `still commanding cart0`, 마지막으로 다시 `effort 0, disable, close`다. `log_status`를 위해 만든 사본이 호출이 돌아올 때 죽으면서 구동기를 끄고, 루프는 꺼진 구동기를 계속 명령하며, 원본이 끝에서 한 번 더 끈다. `-Wall -Wextra`는 아무 말도 하지 않는다. `-Wdeprecated`는 말한다: `definition of implicit copy constructor for 'MotorDriver' is deprecated because it has a user-provided destructor`.

고치는 법은 `raii.cpp`에 이미 있는 두 `= delete` 줄이다. 그러면 값으로 넘기는 호출이 더는 컴파일되지 않는다 — `error: call to deleted constructor of 'MotorDriver'` — 그리고 이 버그는 컴파일 오류에서 찾아져야 한다. ros2_control의 하드웨어 컴포넌트가 바로 이렇게 한다. Jazzy에서 `hardware_interface::HardwareComponentInterface`는 복사 생성자와 이동 생성자를 지우고, 주석에 이유를 적는다. 하드웨어 인터페이스는 소유자가 하나여서, 하드웨어에 두 번 동시에 접근하는 일이 없게 한다는 것이다.

이것의 일반형이 **0의 규칙**(rule of zero)이다. 자원을 직접 소유하는 클래스는 소멸자와 복사·이동 연산을 선언하고, 지원할 수 없는 것은 지운다. 다른 모든 클래스는 그 어느 것도 선언하지 않고 멤버의 것들이 일하게 둔다. §9의 `CartController`는 아무것도 선언하지 않는다. `std::unique_ptr` 멤버가 이미 복사될 수 없으므로 제어기도 그렇고, 멤버가 각자 스스로를 풀기 때문에 소멸자 본문도 필요 없다.

> **RAII의 정의.** **RAII**(resource acquisition is initialization)는 *자원의 생애를 객체의 수명에 묶는 기법*이다. 클래스를 쓰는 방식이지 라이브러리가 아니고, 가비지 컬렉션도 아니다. 정의 조건 넷. **생성자가 자원을 획득**하고 클래스 불변식을 세우며, 그럴 수 없으면 예외를 던지므로 자원 없는 객체는 존재하지 않는다. **소멸자가 자원을 풀고** 예외를 던지지 않는다. 소유하는 객체는 **자동 저장 기간을 갖거나**, 자동 저장 기간을 가진 것에 소유되므로, 언어가 아는 어떤 길 — 반환, 예외, `main`의 끝 — 로 범위를 떠나도 소멸자가 돈다. 그리고 **사본은 옳거나 지워져 있어서**, 획득 하나마다 해제가 정확히 하나다.
>
> $$n_{\text{release}}=n_{\text{acquire}}\ \text{ on every path out of a scope, releases in reverse order of acquisition}$$
>
> $n$은 한 범위의 객체들이 획득하고 푼 자원의 수다. 그러므로 출구가 여러 개인 함수도 어느 출구에도 해제 코드가 필요 없다. 범위의 끝이 해제가 일어나는 단 하나의 자리이기 때문이다.
>
> - **예**: `raii.cpp`는 구동기를 세 번 획득하고 세 번 풀었다. 빠져나가는 길 — 루프의 끝, 이른 반환, 예외 — 마다 한 번씩이고, 짝마다 출력했다.
> - **비예**: 복사할 수 있는 `MotorDriver`. 획득 한 번에 해제 두 번, $2\ne1$이고, 첫 해제가 실행 한가운데에 떨어진다.
> - **비예**: kill 신호, `std::abort`, 정전. 언어가 범위를 떠나지 않으므로 소멸자는 돌지 않고, 구동기는 마지막으로 명령받은 상태로 남는다. RAII가 유일한 정지 경로가 아니라 첫 번째 정지 경로인 이유다.
> - **왜 중요한가**: 소프트웨어가 스스로 멈출 때마다, 어떻게 멈추든, 루프에 정지 코드 한 줄 없이 카트는 0을 명령받고 꺼진다.

### 5. 소유권: unique_ptr, shared_ptr, weak_ptr

*한 문장으로:* 모든 힙 객체에는 "누가 이것을 소멸시키는가"에 대한 답이 하나 있어야 하고, 소유자는 그 책임을 진 것이다 — `std::unique_ptr`는 소유자를 하나로 만들고, `std::shared_ptr`는 사용 횟수를 두고 여럿이 소유를 나누다가 횟수가 0이 되면 객체를 소멸시키며, `std::weak_ptr`는 소유하지 않고 관찰해, 노드와 그 노드가 소유한 구동기를 영원히 살려 두는 순환을 끊는다.

프로그램의 모든 힙 객체에는 "누가 이것을 소멸시키는가"에 대한 답이 정확히 하나 있어야 하고, 현대 C++는 그 답을 타입에 적는다.

- `std::unique_ptr<T>`는 **단일 소유권**(unique ownership)이다. 소유자가 정확히 하나이고, 자기가 소멸하거나 reset되거나 다른 포인터를 대입받으면 객체를 지운다. 복사할 수 없고 이동만 되며, 이동한 뒤 원본은 비어 있으므로 객체가 언제 죽는지 알려면 볼 곳이 늘 한 군데다. `std::make_unique<T>(args)`가 객체와 소유자를 함께 만든다. 날 포인터 하나로 `unique_ptr` 둘을 만들면 둘 다 그것을 지우므로 절대 그러지 않는다. 이 기계의 표준 라이브러리에서는 담은 포인터의 크기와 같은 8바이트다.
- `std::shared_ptr<T>`는 제어 블록에 둔 사용 횟수로 소유를 나누고, 횟수가 0이 되면 객체를 소멸시킨다(이 절 끝의 상자가 정의한다). `std::make_shared`는 객체와 제어 블록을 한 번의 할당으로 잡는다. 전형적인 `shared_ptr`은 포인터 둘을 담아 — 여기서 16바이트 — 횟수를 원자적으로 갱신하므로 서로 다른 스레드에서 쓰는 사본들은 안전하지만, 한 `shared_ptr` 객체를 두 스레드에서 동시에 쓰는 것은 안전하지 않다.
- `std::weak_ptr<T>`는 공유된 객체를 소유하지 않고 관찰한다. `lock()`은 쓰는 동안 객체를 살려 두는 `shared_ptr`을 돌려주고, 객체가 이미 없으면 빈 것을 돌려준다.
- 이런 코드에서 날 `T*`나 `T&`는 아무것도 소유하지 않는다. 소유자가 다른 데 있고 관찰자보다 오래 살아야 하는 객체를 관찰한다. §9의 시험 실행에서 `const SimMotor* sim = motor.get();`은 제어기가 소유한 모터를 관찰한다.

**이동, 한 문단으로.** §9의 `CartController controller(std::move(motor), kTicks);`는 구동기를 제어기에 넘긴다. `std::move`는 그 자체로 아무것도 옮기지 않는다. 인자가 이동 생성자에 묶이게 해 주는 캐스트일 뿐이고, `unique_ptr`의 이동 생성자가 포인터를 넘겨받으며 `motor`를 비워 둔다. 그러니 뒤에서 `motor`를 통해 읽는 줄은 null 포인터를 통해 읽는다. 이동당한 표준 라이브러리 객체는 일반적으로 유효하되 미지정인 상태에 남지만, 이동당한 `unique_ptr`은 비어 있다고 명시되어 있다. 이 페이지에 필요한 이동 의미론은 이것이 전부다. 복사할 수 없는 소유권은 `std::move`로 넘기고, 이동당한 이름은 다시 쓰지 않는다.

**rclcpp가 `SharedPtr`을 쓰는 법**, Jazzy 브랜치에서 읽은 대로. `rclcpp::Node::SharedPtr`은 `std::shared_ptr<rclcpp::Node>`이고 그 이상도 아니다. `create_wall_timer`는 콜백을 — 콜백이 캡처한 모든 것과 함께 — 멤버로 간직하는 타이머의 `SharedPtr`을 돌려주고, 노드의 콜백 그룹은 타이머에 대한 `WeakPtr`만 간직한다. 그러니 멤버에 저장한 `SharedPtr`이 타이머를 살려 두는 것이고, 그것을 놓으면 타이머가 소멸한다. [[04-robotics/ros2/nodes-topics-messages|25.2 §6]]이 타이머를 멤버로 저장하는 이유가 이것이다. 그리고 `rclcpp::spin`은 노드의 `SharedPtr`을 값으로 받으므로, 도는 동안 소유자가 하나 더 생긴다. 영어 절의 `ownership.cpp`는 그 소유 관계를 표준 라이브러리만으로 다시 짓고, 센다. 거기서 쓰는 `shared_from_this()`는 이미 `shared_ptr`이 객체를 소유하고 있을 때 그 객체 자신에 대한 `shared_ptr`을 돌려준다.

`this`를 캡처하면 사용 횟수는 1, 1, `spin`이 사본을 쥐는 동안 2, 다시 1, 그리고 `main`이 놓을 때 0이 된다. 노드가 소멸하고 소멸자가 구동기를 0으로 만든다. `shared_from_this()`를 캡처하면 노드 자신의 타이머 안에 저장된 람다가 노드의 두 번째 소유자가 되어 횟수가 1 밑으로 내려가지 않는다. 1, 2, `spin` 안에서 3, 2, 그리고 `main`이 놓을 때 1이다. 노드 밖의 어떤 것도 더는 노드를 가리키지 않는데, 노드는 타이머를 소유하고, 타이머는 콜백을 소유하고, 콜백은 노드를 소유한다. 순환이다. 소멸자는 돌지 않고, 그것에 기대는 어떤 것도 — 구동기의 정지까지 — 돌지 않는다. AddressSanitizer의 누수 검사기가 기본으로 켜져 있는 리눅스라면 프로그램이 끝날 때 새어 나간 노드가 보고된다. 이 맥에서는 누수 검사기가 지원되지 않아, 요청하면 `detect_leaks is not supported on this platform`을 찍는다.

고치는 법. 콜백을 쥔 것을 객체가 소유할 때는, 여기처럼 `this`를 캡처한다. Jazzy의 C++ 튜토리얼이 타이머 콜백을 `[this]() -> void {...}`로 쓰는 이유가 이것이다. 객체가 쥔 쪽보다 오래 살지 않을 수 있으면 `std::weak_ptr`을 캡처하고 콜백 안에서 `lock()`한다. 그리고 소유자가 하나인 것이 사실이면 어디서든 `unique_ptr`을 택한다. `shared_ptr`은 무언가가 언제 끝나는지 어느 한 객체도 정하지 않는다는 고백이고, 하나하나가 누군가 추적할 수 있어야 하는 횟수다.

> [!note]- 더 깊이 · Deeper
> **rclcpp의 포인터 타입은 어디서 오는가.** rclcpp의 클래스들은 매크로 한 가족, 곧 `RCLCPP_SMART_PTR_DEFINITIONS`와 그 변형들로 포인터 타입을 선언하고, 이 매크로들은 `SharedPtr`을 그 클래스의 `std::shared_ptr`로, `WeakPtr`을 `std::weak_ptr`로, `UniquePtr`을 `std::unique_ptr`로 정의한다. `rclcpp::Node`는 `std::enable_shared_from_this<Node>`에서 파생하는데, 노드가 `shared_from_this()`를 부를 수 있는 것 — 그래서 실제 rclcpp 코드에서 위의 순환이 가능한 것 — 이 이 때문이다.

> **공유 소유권과 참조 계수의 정의.** **공유 소유권**(shared ownership)은 *여러 객체가 하나를 함께 소유하고, 마지막 소유자가 놓을 때 그것이 소멸하는 관계*이며, `std::shared_ptr<T>`는 제어 블록에 둔 **사용 횟수**(use count)로 그것을 구현한다. 가비지 컬렉션이 아니다. 도달할 수 없는 객체를 찾아다니는 것은 없다. 정의 조건 넷. **복사할 때마다** 사용 횟수가 **늘고**, 소유자가 소멸하거나 reset되거나 다시 대입될 때마다 **준다.** 객체는 **사용 횟수가 0이 될 때 소멸한다.** `std::weak_ptr`는 **세지 않으며**, 객체가 살아 있는 동안에만 `lock()`으로 소유자가 될 수 있다. 그리고 소유자의 **순환** — A가 B를, B가 A를 소유 — 은 그 안의 모든 횟수를 영원히 1 이상으로 묶어 둔다.
>
> $$u(t)=\#\{\text{shared\_ptr objects owning } x \text{ at } t\},\qquad t_{\text{destroy}}(x)=\min\{\,t: u(t)=0\,\}$$
>
> $u$는 객체 $x$의 사용 횟수다. 그러므로 객체의 생애는 마지막으로 떠나는 소유자가 정하고, 모든 소유자가 언젠가 떠날 때만 끝이 있다.
>
> - **예**: `this`를 캡처한 `ownership.cpp`의 노드. 사용 횟수가 1, 1, `spin` 안에서 2, 1, 0으로 갔고, 0이 되는 순간 소멸자가 돌았다.
> - **비예**: 같은 노드가 `shared_from_this()`를 캡처하면 1, 2, 3, 2, 1이다. 소유자 하나가 자기가 소유한 객체 안에 있으므로 횟수는 0에 닿지 않는다. `this`나 `weak_ptr`이 순환을 끊는다.
> - **왜 중요한가**: rclcpp는 노드, 퍼블리셔, 구독, 타이머를 `shared_ptr`로 건넨다. 그러니 ROS 2 로봇에서 노드가 끝나는 순간 — 그리고 그와 함께 구동기가 정지되는 순간 — 은 사용 횟수가 0에 닿는 순간이다.

### 6. 템플릿과 표준 컨테이너

*한 문장으로:* 제어 루프에는 도는 동안 저장 공간이 자라지 않는 컨테이너가 필요한데, 템플릿은 컴파일러가 쓰이는 인자 조합마다 별도의 클래스로 바꾸는 틀이어서 `RingBuffer<T, N>` 하나가 저장 공간을 컴파일 때 고정한 채 어떤 샘플 타입이든 섬기고, 같은 방식으로 지은 표준 컨테이너들은 제어 루프가 신경 쓰는 단 한 가지, 원소를 더할 때 할당할 수 있느냐에서 갈린다.

`template <typename T, std::size_t N> class RingBuffer`는 클래스의 한 가족을 선언한다. `T`는 타입 매개변수, `N`은 상수 매개변수, 곧 컴파일러가 알아야 하는 정수다. `RingBuffer<EncoderSample, 5>`와 `RingBuffer<EncoderSample, 8>`은 정의 하나에서 만들어진 서로 다른 두 클래스 — 96바이트와 144바이트 — 이고, 컴파일러는 프로그램이 쓰는 멤버 함수에 대해서만 코드를 만든다. 그러려면 새 인자 조합이 쓰이는 모든 자리에서 정의 전체가 필요하므로 템플릿은 헤더에 산다. `ring_buffer.hpp`에 `.cpp`가 없고, 대부분의 템플릿 라이브러리에도 없는 이유다. 센서의 최근 N개 샘플은 제어 루프에서 데이터의 표준적인 모양이고, 영어 절의 `ring_buffer.hpp`가 그것을 담는 버퍼다.

`data_`는 `std::array<T, N>`이고, C 배열 `T[N]` 하나를 유일한 멤버로 담은 집합체다(cppreference). 그러니 샘플은 `RingBuffer` 객체 안에 — $5\cdot16=80$바이트 — 있고 그 뒤에 인덱스 둘이 온다. 96바이트이며, 버퍼 자신이 할당되는 곳에서 함께 할당되고 다시는 할당되지 않는다. 대신 `std::vector<EncoderSample>`를 담은 클래스는 길이가 얼마든 `sizeof`가 벡터의 포인터 24바이트뿐이다. 원소들이 벡터가 실행 중에 할당하고 다시 할당하는 힙 블록에 있기 때문이다. `push`는 `head_`에 쓰고, `head_`를 `N`의 나머지로 한 칸 옮기고, `N`까지 센다. 버퍼가 차면 push마다 가장 오래된 샘플을 덮어쓴다. `newest()`는 `head_` 바로 앞 칸, `oldest()`는 `count_`칸 뒤의 칸이다. 둘 다 버퍼 안을 가리키는 참조를 돌려주며, 그 참조는 쓰일 때 칸에 든 값을 읽는다. 나중의 `push`가 그것을 덮어썼을 수도 있다. `static_assert`는 `RingBuffer<EncoderSample, 1>`을 컴파일 때 막는다. 속도에는 샘플 둘이 필요하기 때문이다. P6의 제어기가 거기서 읽는 속도는 영어 절의 `sample.hpp`에 있는 함수 템플릿이고, `N`은 인자에서 추론된다.

$K=5$면 속도는 $(K-1)T=20$ ms, 곧 비전 주기 하나에 걸쳐 재고, 그 창에서 엔코더 한 카운트는 $1/(2048\cdot0.020)=0.0244$ m/s다. 틱 하나에 걸쳐 차분하면 $1/(2048\cdot0.005)=0.0977$ m/s다. [[04-robotics/ros2/simulation-and-control|25.7]]은 같은 잡음 대 지연의 거래를 반대편에서 만난다.

**`std::vector`와 그 용량.** 벡터는 원소를 힙 블록 하나에 두고 두 숫자를 안다. `size()`는 담은 원소 수, `capacity()`는 블록이 담을 수 있는 원소 수다. 남은 용량으로의 `push_back`은 원소 하나를 복사할 뿐이다. 가득 찬 벡터로의 `push_back`은 더 큰 블록을 할당하고, 있던 원소를 옮기고, 옛 블록을 풀고, 그다음에 덧붙인다. 그 순간 옛 블록을 가리키던 모든 포인터, 참조, 반복자는 댕글링이 된다. 얼마나 더 크게 잡을지는 라이브러리의 선택이다. 표준은 `push_back`마다 분할상환 상수 시간만 요구하고, 그것이 기하급수적 성장을 강제한다([[02-foundations/algorithms/data-structures|11.2 §2]]에 논증이, [[02-foundations/algorithms/complexity-recursion|11.1 §4]]에 계산이 있다). 로봇 컴퓨터가 쓸 법한 두 라이브러리 — 애플의 clang과 함께 오는 libc++, Ubuntu의 libstdc++ — 는 모두 두 배로 키우므로, 빈 벡터에서 시작하면 용량은 1, 2, 4, 8, … 로 간다(라이브러리마다의 규칙은 아래 콜아웃에 있다). 영어 절의 `capacity.cpp`는 libc++로 돌렸다. 예약하지 않으면 용량이 1, 2, 4, …, 16,384로 자라며 15번 커지고, 레코드 16,383개를 옮기고, 최종 용량 16,384 = 524,288바이트다. 예약하면 0번 커지고, 옮긴 레코드도 0이며, 용량 12,000 = 384,000바이트다.

첫 1분에 새 저장 공간 할당이 15번이고, 마지막이자 가장 큰 것은 레코드 8,193번, 실행 41 s째에 레코드 8,192개 — 262,144바이트 — 를 틱 하나 안에서 옮겼다. 최종 블록은 레코드 16,384개로 필요량보다 36.5% 많다. `reserve(12'000)`는 루프 전에 블록 전체를 한 번에 할당하고, 그 뒤로 실행의 어떤 `push_back`도 할당하지 않는다. cppreference의 `reserve` 페이지가 적는 주의 두 가지가 따라온다. `push_back`마다 `reserve`를 부르면 기하급수적 성장이 무너져 덧붙이기가 오히려 느려지고, `reserve`는 알려진 속도의 로그 길이처럼 최종 크기를 알 때만 쓸모 있다.

> [!note]- 더 깊이 · Deeper
> **라이브러리마다 어떻게 키우는가.** 현재 소스에서 libc++(애플의 clang이 쓰는 LLVM의 것)는 용량의 두 배와 필요한 크기 가운데 큰 쪽을 요청하고(`__vector/vector.h`의 `__recommend`), libstdc++(Ubuntu의 기본인 GCC의 것)는 가득 찬 벡터를 `push_back`마다 자기 크기만큼 키운다(`bits/stl_vector.h`의 `_M_check_len`).

**컨테이너 둘 더, 한 문장씩.** `std::unordered_map`은 해시 테이블이다([[02-foundations/algorithms/data-structures|11.2 §3]]). 찾기, 삽입, 삭제가 평균 상수 시간이고, 삽입 한 번이 테이블 전체를 재해시할 수 있다. `std::map`은 균형 탐색 트리, 흔히 레드-블랙 트리다([[02-foundations/algorithms/data-structures|11.2 §5]]). 키를 정렬해 두고 로그 시간이 걸린다. 둘 다 원소마다 자기 노드에 저장하므로 — C++17부터는 노드를 꺼내 다른 컨테이너로 옮길 수도 있다 — 새 키를 넣으면 할당이 일어나고, 어느 쪽도 틱 안에서 채우지 않는다. 루프 전에 채운 맵에서 `find`로 키를 찾는 것은 할당하지 않는다. 없는 키에 `operator[]`를 쓰면 그 키를 삽입하므로 할당한다.

### 7. 인터페이스: 상속과 virtual

*한 문장으로:* 제어기는 모의 카트와 실제 카트를 어느 쪽인지 모른 채 몰아야 하는데, 추상 기반 클래스가 모든 모터가 할 수 있는 일을 순수 가상 함수로 선언하고, `SimMotor`와 `RealMotor`가 그것을 구현하며, `MotorInterface` 포인터를 통한 호출은 그 뒤에 있는 객체의 구현을 실행 시간에 약 1나노초를 들여 골라 부른다 — 단, 기반의 소멸자가 가상이어야 하고, 그렇지 않으면 그 포인터로 지울 때 구동기를 정지시키는 소멸자를 건너뛴다.

제어기는 자기가 모의 카트를 모는지 실제 카트를 모는지 몰라야 하므로 인터페이스에 대고 말한다. 영어 절의 `motor.hpp`가 인터페이스와 두 구현을 선언하고, `real_motor.cpp`가 `RealMotor`를 정의한다.

`virtual`은 프로그램이 돌 때 객체의 타입이 어느 판을 부를지 고르는 함수를 표시한다. `= 0`은 그것을 **순수**(pure) 가상으로 만들어 기반에는 판이 아예 없게 하며, 그래서 `MotorInterface`는 **추상 클래스**(abstract class)가 된다. 그 객체는 만들 수 없지만, 그것을 가리키는 포인터와 참조는 쓸 수 있다. `override`는 그 함수가 정말로 기반의 함수를 재정의하는지 컴파일러에게 확인시킨다. `set_effort`의 철자를 틀리면 새 함수가 조용히 더해지는 대신 빌드가 실패한다. `final`은 더 이상의 파생을 막는다. 제어기는 `std::unique_ptr<MotorInterface>`를 쥐고 `motor_->set_effort(u)`를 부르며, 같은 줄이 §9의 시험 실행에서는 `SimMotor::set_effort`를, 카트 위에서는 `RealMotor::set_effort`를 실행한다.

어떻게 하는지는 표준에 없지만, 주류 컴파일러는 모두 같은 방식으로 한다. 가상 함수가 있는 클래스의 객체는 그 클래스의 함수 주소 표를 가리키는 숨은 포인터를 하나씩 싣고, 가상 호출은 표에서 주소를 꺼내 부른다. 클래스 배치에 대한 표준 자신의 주석도 "가상 함수를 관리하기 위한 공간"을 허용한다. 이 기계에서 그 포인터가 `MotorInterface`의 전부여서 `sizeof`가 8이다. `SimMotor`는 24 — 표 포인터, 패딩 7바이트를 동반한 `bool`, 그리고 `double` — 이고 `RealMotor`는 32다.

**가상 소멸자.** `RealMotor`를 가리키는 `MotorInterface*`에 `delete`를 하면 `~RealMotor`가 돌아야 하고, 0을 명령하고 구동기를 끄는 것이 그 소멸자다. `~MotorInterface`가 가상일 때만 그렇게 되며, 아니면 표준은 그 삭제를 정의되지 않은 동작으로 만든다. 영어 절의 `no_virtual_dtor.cpp`가 일부러 틀리게 쓴 예다. clang은 `-Wall` 없이도 경고한다: `delete called on 'MotorInterface' that is abstract but has non-virtual destructor [-Wdelete-abstract-non-virtual-dtor]`. 경고는 `delete`가 실제로 일어나는 표준 라이브러리 안을 가리킨 뒤, 그것을 부른 이 프로그램의 줄(20행)을 짚는다. 실행은 아무것도 찍지 않는다. `~RealMotor`가 한 번도 돌지 않았고, 실제 카트였다면 구동기는 마지막 명령으로 켜진 채 남았을 것이다. 고치는 법은 한 낱말, `virtual ~MotorInterface() = default;`이고, 위의 목록이 그렇게 선언한다. 기반 포인터로 쓰일 클래스의 경험칙: 소멸자는 public이고 가상이다.

두 번째 함정이 바로 옆에 있다. 소멸자가 도는 동안 객체는 소멸자가 돌고 있는 클래스만큼만 파생된 것이다. `~MotorInterface`가 돌 때쯤 `RealMotor` 부분은 이미 없고, 거기서 한 가상 호출은 `RealMotor`의 판에 닿지 않는다. 거기서 순수 가상 함수를 부르면 정의되지 않은 동작이다. 그래서 `disable()`은 기반이 아니라 `~RealMotor`에 있어야 하고, `real_motor.cpp`가 그 자리에서 부른다.

**ros2_control의 같은 이음매.** ros2_control의 제어기와 하드웨어 컴포넌트가 바로 이 모양이다. 컨트롤러 매니저는 둘 다 실행 중에 이름으로 불러들여 가상 소멸자를 가진 기반 클래스를 통해서만 알고, 그래서 매 주기 하는 호출 — 하드웨어에 `read()`, 활성 제어기마다 `update()`, 하드웨어에 `write()` — 은 모두 가상 호출이다([[04-robotics/ros2/simulation-and-control|25.7 §5]]와 [[04-robotics/ros2/simulation-and-control|25.7 §7]]). `MotorInterface`는 관절 하나짜리 그 이음매이고, [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]이 실제 컴포넌트를 쓴다.

> [!note]- 더 깊이 · Deeper
> **Jazzy의 기반 클래스.** 제어기는 `controller_interface::ControllerInterface`에서 파생하고, 그 기반 `ControllerInterfaceBase`는 가상 소멸자를 선언하며, 순수 가상 함수 가운데 `update(const rclcpp::Time & time, const rclcpp::Duration & period)`가 있다. 다관절 기계의 하드웨어 컴포넌트는 `hardware_interface::SystemInterface`에서 파생하고, 이것은 `HardwareComponentInterface`에서 파생한다. 그 기반은 가상 소멸자, 순수 가상 `read(time, period)`, 그리고 `SystemInterface`가 순수로 만드는 가상 `write(time, period)`를 갖는다.

**5 ms에 대한 비용.** 이 애플 M1에서 `-O3`로 빌드하고, 동적 타입을 실행 중에 고른 `MotorInterface*`를 통해 `set_effort`를 2억 번 부르는 루프는 세 번 반복에서 호출당 0.97–1.10 ns가 걸렸다. 인라인되지 않는 비가상 함수를 부르는 같은 루프와 잡음 범위 안에서 같다. 틱마다 한 번이면 예산의 $1\ \mathrm{ns}/5\ \mathrm{ms}=2\times10^{-7}$이다. 가상 호출의 진짜 값은 컴파일러가 객체의 타입을 증명하지 못하면 그 너머로 인라인할 수 없다는 것이고, 클래스에 `final`을 붙이면 증명이 가능해질 때가 있다. 원소 수천 개를 도는 안쪽 루프라면 중요하지만, 틱마다 구동기를 한 번 부르는 데는 중요하지 않다.

> **동적 디스패치의 정의.** **동적 디스패치**(dynamic dispatch)는 *가상 함수 호출이 호출이 실행되는 순간 객체의 동적 타입에 속한 판을 골라 실행한다는 규칙*이다. 기반 클래스의 포인터나 참조를 통한 호출이 가진 성질이지, 함수 하나만의 성질이 아니다. 정의 조건 넷. 함수가 기반 클래스에서 **`virtual`로 선언되고**, 파생 클래스가 같은 서명으로 그것을 **재정의한다.** 호출은 기반을 가리키는 **포인터나 참조를 통해** 이루어진다. 이름으로 직접 부른 객체의 호출이나 `MotorInterface::set_effort` 같은 한정된 호출은 컴파일 때 묶인다. 실행되는 판은 동적 타입에 대한 **최종 재정의자**(final overrider), 곧 그것을 정의한 가장 많이 파생된 클래스의 것이다. 그리고 **생성과 소멸 도중에는** 동적 타입이 생성자나 소멸자가 돌고 있는 클래스이므로, 기반의 소멸자는 파생 클래스의 재정의에 닿을 수 없다.
>
> $$\texttt{b->f(a)}\ \longmapsto\ \mathrm{final}_{\,\mathrm{dyn}(\texttt{*b})}(f)\,(a)$$
>
> `b`는 기반 클래스를 가리키는 포인터, $\mathrm{dyn}(\texttt{*b})$는 호출이 실행될 때 그것이 가리키는 객체의 타입, $\mathrm{final}_D(f)$는 그 타입의 $f$에 대한 최종 재정의자다. 그러므로 제어기 코드의 같은 줄이 모의 카트도 실제 카트도 몬다. 어느 판이 돌지는 줄이 아니라 객체가 정하기 때문이다.
>
> - **예**: `CartController::tick`의 `motor_->set_effort(u)`는 §9의 실행에서는 `SimMotor::set_effort`를, 카트 위에서는 `RealMotor::set_effort`를 제어기 수정 없이 실행한다.
> - **비예**: 가상이 아닌 소멸자. 그러면 `MotorInterface*`를 통한 `delete`는 컴파일 때 `~MotorInterface`에 묶이고, `no_virtual_dtor`는 `~RealMotor`가 한 번도 돌지 않았으므로 아무것도 찍지 않았다.
> - **비예**: `~MotorInterface`에서 부른 `disable()`. 그때는 `RealMotor` 부분이 이미 소멸해 동적 타입이 기반이고, 호출은 어떤 재정의에도 닿지 않는다.
> - **왜 중요한가**: ros2_control의 제어기–하드웨어 이음매가 이 장치이고, 제어기 코드를 그대로 둔 채 시뮬레이션과 하드웨어를 바꾸는 모든 전환이 이 장치다.

### 8. 빌드: 헤더, 번역 단위, 링크, CMake

*한 문장으로:* 프로그램은 소스 파일 여럿이고, 고전적인 빌드 오류 둘은 그것들을 잇는 방식에서 나온다 — 컴파일러는 소스 파일 하나와 그것이 포함한 헤더를 목적 파일 하나로 바꾸고, 링커는 파일이 쓰는 모든 함수를 정확히 하나의 정의에 짝지어 목적 파일과 라이브러리를 프로그램으로 이으며, CMake는 어느 파일이 어느 라이브러리가 되고 어느 프로그램이 어느 라이브러리에 링크되는지를 적는다.

도구 셋이 차례로 돈다. **전처리기**(preprocessor)는 `#`로 시작하는 줄을 처리한다. `#include`는 헤더의 글을 그 자리에 붙이고, `#define`은 매크로를 정의하며, `#if`는 글을 남기거나 뺀다. **컴파일러**는 소스 파일 하나와 그것이 포함한 모든 것 — **번역 단위**(translation unit) 하나 — 를 목적 파일로 번역한다. 그 단위가 정의하는 함수의 기계어, 그리고 쓰지만 정의하지 않는 이름의 목록이다. **링커**(linker)는 목적 파일과 라이브러리를 프로그램 하나로 잇고, 쓰인 모든 이름에 그 하나의 정의의 주소를 준다. 컴파일러는 `.cpp` 두 개를 한꺼번에 보는 일이 없으므로, 헤더에 선언된 함수가 어딘가에 정의되어 있는지 알 수 없다. 링커만 알 수 있고, 이 절의 두 오류가 링커 오류인 이유가 그것이다.

**헤더**는 선언한다 — 클래스, 함수 서명 — 그리고 그것을 포함하는 모든 번역 단위에 나타나도 되는 것만 정의한다. 클래스, `inline` 함수, 템플릿, 상수다. **소스 파일**은 나머지를 한 번 정의한다. 헤더는 여러 번 포함되기 마련이다. `controller.hpp`와 `sample.hpp`를 둘 다 포함하는 단위는 `controller.hpp`도 `sample.hpp`를 포함하므로 `sample.hpp`를 두 번 받고, 한 단위 안에서 두 번 정의된 클래스는 오류다. 가드가 없으면 clang은 "redefinition of 'EncoderSample'"이라고 말한다. **포함 가드**(include guard) — 맨 위의 `#ifndef CART_SAMPLE_HPP`, `#define CART_SAMPLE_HPP`, 맨 아래의 `#endif` — 가 표준적인 해결이다. 이 페이지의 헤더가 쓰는 `#pragma once`는 더 짧고 표준의 일부가 아니지만, 현대 컴파일러 대다수가 지원한다. 이름의 **링키지**(linkage)는 다른 단위가 그 이름을 가리킬 수 있는지를 말한다. 네임스페이스 범위의 함수는 외부 링키지를 갖고, §9의 `controller.cpp`에 있는 `kKp`처럼 이름 없는 `namespace { }` 안의 것은 내부 링키지를 가져 자기 파일에만 속한다.

P6의 제어기를 프로젝트로 만들면 파일은 일곱이다. 루트의 `CMakeLists.txt`, `include/cart/` 아래 헤더 넷 — `ring_buffer.hpp`와 `sample.hpp`(§6), `motor.hpp`(§7), `controller.hpp`(§9) — 그리고 `src/` 아래 소스 셋 — `real_motor.cpp`(§7), `controller.cpp`와 60 s 시험 실행인 `main.cpp`(§9) — 이다. 영어 절에 `CMakeLists.txt`와 빌드 명령이 있다. `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release`가 빌드 파일을 쓰고, `cmake --build build`가 라이브러리의 `.cpp` 둘, 그다음 `main.cpp`를 컴파일하고 링크하며, `-DCMAKE_CXX_FLAGS="-fsanitize=address,undefined"`를 준 두 번째 구성이 검사용 빌드다.

`add_library`는 나열한 소스 둘로 `cart_core`를 만든다. `BUILD_SHARED_LIBS` 옵션이 공유 라이브러리를 요구하지 않으면 정적 라이브러리다. `target_include_directories(... PUBLIC include)`는 `include/`를 `cart_core`의 헤더 검색 경로에 넣고, `PUBLIC`이므로 그것에 링크하는 모든 것의 경로에도 넣는다. `add_executable`은 `main.cpp` 하나로 프로그램을 만들고, `target_link_libraries(... PRIVATE cart_core)`는 라이브러리를 거기에 링크하면서 포함 경로를 비롯한 라이브러리의 공개 요구 사항을 넘겨준다. 각 소스는 한 타깃에서 한 번 컴파일하고, 그것이 필요한 타깃은 그 타깃에 링크한다. `controller.cpp`를 실행 파일에도 나열하면 두 번 컴파일되어 그 함수들의 사본 둘이 빌드에 남는다. `CMAKE_CXX_STANDARD 17`에 `REQUIRED`를 더하면 C++17을 요구하고, 컴파일러에 그것이 없으면 옛 표준으로 물러서는 대신 오류로 멈춘다.

**정의되지 않은 심볼.** 일부러 틀리게: 같은 프로젝트에서 `target_link_libraries` 줄을 포함 경로 하나로 바꾸어, `main.cpp`는 헤더에 맞춰 컴파일되지만 라이브러리는 한 번도 링크되지 않게 한다. 이 맥의 애플 링커는 `Undefined symbols for architecture arm64`를 보고하며, `CartController::tick(EncoderSample const&)`, `CartController::on_goal(double)`, `CartController`의 생성자, 이 셋을 `main.cpp.o`가 참조했다고 적은 뒤 `ld: symbol(s) not found for architecture arm64`로 끝난다. Ubuntu의 흔한 링커인 GNU ld는 같은 실패를 함수마다 "undefined reference to"로 보고한다. 헤더가 세 함수를 선언했으므로 `main.cpp`는 컴파일되었고, 링크된 어느 것도 그것들을 정의하지 않았다. 흔한 원인 둘은 보인 경우 — 정의한 파일이 프로그램이 링크하는 어디에도 컴파일되어 들어가지 않은 것 — 와, 선언과 맞지 않는 정의다. 매개변수 타입이 다르거나, `const`가 빠졌거나, 멤버 함수를 `CartController::` 접두사 없이 정의해 새 자유 함수를 정의해 버린 경우다.

**중복된 심볼.** 일부러 틀리게: `sample.hpp`에 `inline` 없이 도우미를 정의하고 — 영어 절의 `counts_to_metres` — `controller.cpp`와 `main.cpp` 양쪽에서 부른다. 두 단위 모두 컴파일되고, 이제 목적 파일마다 그 함수를 정의한다. 애플 링커는 `duplicate symbol 'counts_to_metres(int)'`이 `main.cpp.o`와 `libcart_core.a`의 `controller.cpp.o`에 있다고 적고 `ld: 1 duplicate symbols`로 끝난다. GNU ld는 그 함수의 "multiple definition of"라고 부르고 치명적 오류로 다룬다. `inline double counts_to_metres(...)`라고 쓰면 고쳐진다. 인라인 함수는 그것을 쓰는 모든 단위에서 정의되어도 되기 때문이다. 헤더에서 선언하고 `.cpp` 하나에서 정의해도 고쳐진다.

> [!note]- 더 깊이 · Deeper
> **ROS 2 패키지에서는** 이 파일에 `find_package(ament_cmake REQUIRED)`와 의존성마다 `find_package`가 하나씩 더해지고, Jazzy 튜토리얼은 `ament_target_dependencies(talker rclcpp std_msgs)`로 의존성을 붙인다. 이것은 각 패키지의 포함 디렉터리와 라이브러리를 `target_include_directories`와 `target_link_libraries`를 거쳐 타깃에 더하는 ament 매크로다. colcon은 그런 패키지로 가득한 워크스페이스를 의존성 순서대로 빌드한다. 그것은 [[04-robotics/ros2/workspaces-packages-launch|25.4 §3]]과 [[04-robotics/ros2/workspaces-packages-launch|25.4 §4]]이고, 이 페이지는 그 밑의 평범한 CMake에서 멈춘다.

> **번역 단위, 링키지, 단일 정의 규칙의 정의.** **번역 단위**(translation unit)는 *전처리를 마친 소스 파일 하나*, 곧 포함한 모든 헤더를 붙여 넣은 `.cpp`이며, 컴파일러가 홀로 목적 파일로 번역하는 단위다. **링키지**(linkage)는 *다른 번역 단위가 같은 개체를 가리킬 수 있는지 말해 주는 이름의 성질*이다. 외부(가리킬 수 있다), 내부(자기 단위만), 없음(자기 범위만)이 있다. **단일 정의 규칙**(one-definition rule)은 *각 개체가 정의를 몇 개 가질 수 있는지*를 말한다. 정의 조건 셋. **한 번역 단위 안에서** 어떤 변수, 함수, 클래스, 템플릿도 두 번 정의될 수 없다. 포함 가드는 두 번 포함된 헤더도 자기 클래스를 한 번만 정의하게 하려고 있다. **프로그램 전체에서** 쓰이는 모든 비인라인 함수와 변수는 정확히 한 번 정의되어야 한다. 그리고 클래스, 템플릿, `inline` 함수는 정의들이 토큰 하나하나까지 같다면 **그것을 쓰는 모든 번역 단위에서 정의될 수 있고**, 헤더 하나를 포함하는 것이 그것을 보장한다. 컴파일러는 한 번에 단위 하나만 보므로 프로그램 전체 규칙을 검사할 수 없다. 흔한 위반은 링커가 보고하고, 일부는 정의되지 않은 동작으로 조용히 지나간다.
>
> $$n_{\text{def}}(e)=1\ \text{ for every used non-inline function or variable } e;\qquad n_{\text{def}}=0\Rightarrow\text{undefined symbol},\quad n_{\text{def}}\ge2\Rightarrow\text{duplicate symbol}$$
>
> $n_{\text{def}}(e)$는 링크되는 모든 목적 파일과 라이브러리에 걸친 $e$의 정의 수다. 그러므로 고전적인 링크 오류 둘은 숫자 1을 놓치는 두 가지 방식이다.
>
> - **예**: `CartController::tick`은 두 단위가 포함하는 `controller.hpp`에서 선언되고 `controller.cpp`에서 한 번 정의된다. $n_{\text{def}}=1$이다. `RingBuffer`는 그 헤더를 포함하는 모든 단위에서 정의되는데, 템플릿이므로 규칙이 허용한다.
> - **비예**: 헤더에 `inline` 없이 정의한 `counts_to_metres`는 $n_{\text{def}}=2$이고, `cart_core` 없이 링크한 `cart_controller`에서는 `CartController`의 멤버 셋이 $n_{\text{def}}=0$이다.
> - **왜 중요한가**: 이 두 오류는 ROS 2 워크스페이스의 C++ 패키지가 가장 먼저 내는 것이고, 횟수로 읽는 순간 각자 자기 원인을 정확히 말한다.

### 9. 실시간 틱의 규칙

*한 문장으로:* 주기를 넘긴 틱은 이전 명령을 모터에 걸어 두므로, 틱은 평균이 아니라 최악의 경우가 주기 안에 들어갈 때만 실시간 안전하고, 힙 할당, 막히는 호출, 경합하는 잠금, 던져진 예외, 페이지 폴트는 걸리는 시간에 쓸 만한 상한이 없으므로, 실시간 틱은 그 어느 것도 하지 않으며 필요한 모든 것을 루프가 시작되기 전에 할당하고 건드려 둔다.

P6의 제어기는 $T=5$ ms마다 풀려나고, 틱마다 다음 풀림 전에 끝나야 한다. 넘친 틱은 이전 명령을 한 주기 더 모터에 걸어 둔다. [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]이 여기 필요한 마감, 응답 시간, 지터를 정의하고, 아래의 모든 것을 정하는 요점을 짚는다. 평균은 표에서 좋아 보이는 숫자이고, 루프가 작동하는지를 정하는 것은 최댓값이다.

**ROS 2 문서가 말하는 것.** Jazzy 튜토리얼 "Understanding real-time programming"은 같은 적을 꼽는다. 실시간 루프는 마감을 지키도록 주기적으로 갱신해야 하고 허용되는 오차는 작으며, 그러려면 페이지 폴트, 동적 메모리 할당과 해제, 무한정 막힐 수 있는 동기화 수단을 피해야 한다. 문서가 찍어 보이는 예시 실행이 평균이 왜 오도하는지 보여 준다. 1 ms 루프에서 평균 지연 19,871.8 ns, 최대 2,752,187 ns — 최악이 평균의 138배, 주기의 2.75배이고, 튜토리얼 말대로 루프 자신의 주기를 넘었다.

> [!note]- 더 깊이 · Deeper
> **튜토리얼의 데모는 어떻게 설정되어 있나.** 그 펜듈럼 데모는 `mlockall`로 메모리를 RAM에 잠그고, 제어 스레드를 우선순위 98로 돌리며, PREEMPT_RT 커널 없이는 목표를 아마 지키지 못할 것이라고 경고한다.

**규칙, 각각의 이유와 함께.**

1. *틱 안에서 할당도 해제도 하지 않는다.* 할당자는 다른 스레드가 쥔 잠금을 잡거나, 운영체제에 메모리를 청하거나, 한 번도 건드리지 않은 페이지를 내줄 수 있고, 그 어느 것에도 적어 둘 만한 상한이 없다. 할당하거나 해제할 수 있는 숨은 경우도 모두 센다. 용량을 넘는 `push_back`, 값으로 복사한 벡터, 실행 중에 만드는 `std::string`, 예외, 그리고 틱 안에서 놓인 메시지에 대한 마지막 `shared_ptr` — 그 자리에서 메시지를 해제한다 — 이다.
2. *막히는 입출력을 하지 않는다.* 출력, 콘솔이나 파일로의 로깅, 소켓, 다음 메시지 기다리기다. 실시간 시스템에 대한 ROS 2 설계 문서는 디스크 읽기·쓰기를 실시간 경로 밖, 프로그램의 시작이나 끝에 두고, 출력은 실시간이 아닌 스레드에 맡기라고 권한다.
3. *잠금에서 무한정 기다리지 않는다.* 우선순위가 낮은 스레드가 쥔 뮤텍스를 잠그려는 틱은 그 스레드가 걸리는 만큼 기다린다. 우선순위 역전이다. 값 하나는 `std::atomic`으로, 더 큰 데이터는 실시간 쪽이 시도만 하는 구조로 스레드 사이에 넘긴다. ros2_control의 `realtime_tools::RealtimeBuffer`는 `try_to_lock`으로 읽고, 잠금이 잡혀 있으면 기다리는 대신 이전 데이터를 돌려준다.
4. *예외를 던지지 않는다.* GCC와 Clang이 리눅스와 macOS에서 쓰는 Itanium C++ ABI에서 throw는 가능하면 예외 객체를 힙에 할당한다. 틱 안의 오류는 값이다. 상태 하나, 0 명령 하나.
5. *미리 할당하고, 루프 전에 건드린다.* 틱이 쓰는 모든 것은 생성자에서 크기가 정해지고 — `reserve`, `std::array`, `RingBuffer` — 리눅스에서는 튜토리얼의 데모처럼 `mlockall`이 그것을 RAM에 붙잡아 둔다.
6. *최악의 경우를 잰다.* 긴 실행으로, 목표 컴퓨터에서, 부하 아래에서.

그 규칙대로 쓴 P6의 제어기가 영어 절의 `controller.hpp`와 `controller.cpp`다. 헤더는 제어기가 소유하는 것을 선언하고, 소스 파일은 하는 일을 정의한다.

할당은 생성자가 한다. `reserve`가 로그의 크기를 실행 전체에 맞춰 잡고, 링 버퍼는 객체 안에 있으므로 아무것도 필요 없다. 그다음 `tick`은 16바이트 샘플 하나를 링에 복사하고, 링을 `const&`로 읽고, 원자적 적재 한 번으로 목표를 읽고, 자르고, 가상 호출을 한 번 하고, 자리가 있는 로그에 32바이트를 덧붙인다. `new`도, 잠금도, `throw`도, 입출력도 없다. `goal_m_`이 `std::atomic<double>`인 것은 `on_goal`은 비전 콜백의 스레드에서(다중 스레드 executor라면, [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]) 돌고 `tick`은 제어 스레드에서 그것을 읽기 때문이다. 원자 변수는 한 스레드의 쓰기와 다른 스레드의 읽기를 잘 정의된 것으로 만든다. 8바이트 원자 변수는 x86-64 리눅스, ARM64 리눅스, ARM64 macOS에서 늘 잠금 없이 동작한다. 컴파일러의 `__atomic_always_lock_free(8, 0)`이 셋 모두에서 참이다. 그래서 적재는 잠금을 잡지 않고 막히지 않는다. 읽기가 실패하면 안전한 갈래를 탄다. 예외를 던지는 대신 0을 명령한다.

시험으로 첫 규칙을 믿지 않고 증명할 수 있다. C++ 표준은 프로그램이 전역 `operator new`를 바꿔 끼우는 것을 허용하고, 그러면 표준 컨테이너의 것을 포함해 프로그램의 모든 `new`가 대체품을 지난다. 그래서 영어 절의 `main.cpp`는 루프 둘레에서 그것을 세고, 틱마다 시간을 잰다. 출력은 틱 12,000번 동안 할당 0번, 로그 레코드 12,000개, 카트 위치 0.4004 m, 그리고 틱 시간 평균 0.028 µs, 최악 1.625 µs, 예산 5000 µs다.

그 실행은 애플 M1 위의 Release 빌드(`-O3`)다. 열 번 실행하면 평균은 0.022–0.028 µs, 최악의 틱은 1.2–10.7 µs로 평균의 53–427배였고, 같은 프로젝트의 새니타이저 빌드도 할당 0번을 셌다. 이 숫자에 대한 주의 둘. 이 기계의 시계는 약 41.7 ns씩 나아가므로, 25 ns짜리 틱 하나는 0이나 42 ns로 읽히고 틱 여럿의 평균만이 그것을 가려낸다. 마이크로초 단위의 최악값은 진짜다. 그리고 macOS를 도는 노트북은 실시간 시스템이 아니다. 숫자가 보여 주는 것은 모양 — 평균보다 훨씬 높고 5 ms보다 훨씬 낮은 최악 — 이지 보장이 아니다. 보장에는 로봇 자신의 컴퓨터, PREEMPT_RT 커널, 부하 아래의 긴 실행이 필요하다.

규칙은 그 숫자가 말하는 것보다 더 중요하다. 규칙이 금하는 것은 자라기 때문이다. 계산 절의 첫 판 함수 `velocity_all` — 이력 전체를 값으로 받는다 — 을 이 M1에서 200번씩 불러 시간을 재면, 1분 분량의 이력(샘플 12,000개)에서는 다섯 번의 실행에서 호출의 중앙값이 3.1–3.8 µs였고, 1시간 분량(샘플 720,000개)에서는 0.41–0.56 ms, 가장 느린 호출은 1.0–2.8 ms였다. 줄 하나가 주기의 절반을 넘기까지 하고, 그 시험은 처음 1분 동안 통과한다. 막히는 호출은 자랄 필요도 없다. 다음 50 Hz 목표를 기다리는 틱은 자기 계산이 얼마든 $T_v=20$ ms, 곧 네 주기까지 기다릴 수 있다.

ros2_control은 같은 규칙을 인터페이스에 적는다. Jazzy에서 `ControllerInterfaceBase::update`에는 실시간 안전해야 한다는 주석이 붙어 있다. 컨트롤러 매니저가 자기 루프에서 부르기 때문이다. 그리고 하드웨어 컴포넌트의 `set_state`와 `get_command` 가운데 인터페이스 이름을 받는 것은 실시간 안전하지 않다고 표시되어 있다. [[04-robotics/ros2/from-simulation-to-hardware|25.11 §3]]이 그 이유를 설명하고 루프에서 대신 쓸 핸들 기반 형식을 보인다.

> **실시간 안전한 틱의 정의.** 틱이 **실시간 안전하다**(real-time safe)는 것은 *최악 실행 시간에 상한이 있고, 그 상한이 코어가 해야 할 다른 모든 일의 자리를 남기고 주기 안에 들어간다*는 뜻이다. 주어진 기계에서 루프가 주기마다 도는 코드의 성질이지, 언어나 주기나 평균의 성질이 아니다. 정의 조건 다섯, 앞의 넷은 다섯째에 이르는 방법이다. **아무것도 할당하거나 해제하지 않는다.** 모든 저장 공간은 첫 틱 전에 존재한다. **아무것에도 막히지 않는다.** 입출력, 잠자기, 메시지 기다리기, 다른 스레드가 오래 쥘 수 있는 잠금이 없고, 기껏해야 `try_lock`이나 잠금 없는 교환이다. **아무것도 던지지 않는다.** **페이지 폴트를 일으키지 않는다.** 메모리는 루프 전에 건드려 두었고, 리눅스에서는 잠가 두었다. 그리고 부하 아래의 목표 기계에서 긴 실행으로 **잰 최악의 경우**가 주기보다 작다.
>
> $$C_{\max}=\max_k C_k\ \le\ T-C_{\text{other}},\qquad T=\frac{1}{f_c}=5\ \mathrm{ms}$$
>
> $C_k$는 틱 $k$의 실행 시간, $C_{\text{other}}$는 같은 코어가 주기 안에서 다른 모든 일에 내줘야 하는 시간이다. 그러므로 $T$보다 작은 평균은 아무것도 말하지 않는다. $T$를 넘는 틱 하나가 곧 마감 놓침이기 때문이다.
>
> - **예**: §9의 틱은 12,000번 동안 아무것도 할당하지 않았고, 이 노트북에서 열 번의 실행에 걸쳐 최악의 틱이 5,000 µs 주기에 대해 1.2–10.7 µs였다. 앞의 네 조건은 구성으로 만족하고, 다섯째는 로봇의 컴퓨터에서 다시 재야 한다.
> - **비예**: 계산 절의 첫 판. 60 s 동안 12,030번 할당했고 끝에는 틱마다 192,000바이트를 복사했다. 평균은 몇 마이크로초지만 비용이 실행과 함께 자라고, 할당에는 상한이 없다.
> - **비예**: 다음 50 Hz 목표를 기다리는 틱. 계산은 사소한데도 늦는다. 최대 20 ms, 네 주기다.
> - **왜 중요한가**: ros2_control의 컨트롤러 매니저는 활성 제어기마다 `update()`를 자기 루프에서 부르고, Jazzy 인터페이스는 자기 주석에서 `update()`가 실시간 안전해야 한다고 말한다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 60 s 실행이 끝날 무렵 P6 제어기의 틱 하나를 센다. 과제는 손잡이를 하나씩 — 구조체, 주기, 코드 — 바꾸므로, 페이지의 판을 여기서 먼저 한다. 모든 숫자를 두 번 확인한다. 아래에서 손으로, 그리고 출력을 인용한 C++ 프로그램으로. 셈의 비교 대상인 첫 판은 처음 쓰는 사람이 쓰는 제어기다. 모든 샘플을 예약하지 않은 `std::vector`에 모으고, 그 벡터를 값으로 받는 함수로 속도를 구하며, 로그도 예약하지 않는다.

**1단계 — 샘플의 바이트(§3).** $o_i$를 오프셋, $s_i$를 크기, 가장 큰 정렬을 $a_S=8$이라 하면 규칙 $\mathrm{sizeof}(S)=\lceil (o_n+s_n)/a_S\rceil\,a_S$는 처음 쓴 그대로에서 오프셋 $0, 8, 16$과

$$\mathrm{sizeof}=\Big\lceil\frac{16+4}{8}\Big\rceil 8=24\ \text{bytes},\qquad \text{reordered: } \Big\lceil\frac{12+1}{8}\Big\rceil 8=16\ \text{bytes}$$

를 준다. 멤버가 첫 순서에서는 20번째 바이트에서, 둘째 순서에서는 13번째 바이트에서 끝나기 때문이다. 페이로드는 어느 쪽이든 $1+8+4=13$바이트이므로 패딩은 11바이트에서 3바이트로, 샘플은 24바이트에서 16바이트로, 3분의 1이 준다. `layout.cpp`가 오프셋 0, 8, 16과 0, 8, 12와 함께 24와 16을 찍었다.

**2단계 — 링 버퍼(§6).** `RingBuffer<EncoderSample, 5>`는 샘플 $K=5$개를 제자리에 두고 8바이트 인덱스 둘을 더한다. $5\cdot16+2\cdot8=96$바이트이고, 첫 배치라면 $5\cdot24+16=136$바이트다. 제어기 안에 살므로 제어기와 함께 할당되고 다시는 할당되지 않는다. 창은 $(K-1)T=4\cdot5=20$ ms이고, 그 창에서 한 카운트는 속도 $1/(2048\cdot0.020)=0.0244$ m/s다.

**3단계 — 틱 하나가 복사하는 것(§1).** §9의 틱은 새 샘플을 링에 16바이트 복사하고, 링을 `const&`로 0바이트에 읽고, 레코드 하나를 32바이트 덧붙인다. 틱마다 48바이트, 초당 $48\cdot200=9{,}600$바이트이고, 첫 초나 마지막 초나 같다. 링을 값으로 넘기면 96바이트, 초당 19,200바이트가 더해지지만 여전히 아무것도 할당하지 않는다. 첫 판의 값 벡터는 그때까지 모은 샘플을 전부, 틱 $k$에서 $16k$바이트를 복사한다.

$$B_{\text{copy}}(k)=16k,\qquad B_{\text{copy}}(12{,}000)=192{,}000\ \text{bytes},\qquad 200\cdot192{,}000=38.4\ \text{MB/s}$$

$k$번째 호출이 16바이트 샘플 $k$개를 복사하고 틱이 초당 200번이기 때문이다. 실행 전체로는 복사가 $16\cdot(1+2+\dots+12{,}000)=16\cdot12{,}000\cdot12{,}001/2=1{,}152{,}096{,}000$바이트에 이르고, 하나하나마다 할당이 한 번씩이다.

**4단계 — 실행이 할당하는 것(§6).** `reserve`가 없으면 빈 채로 시작해 두 배씩 자라는 벡터는 용량 $1, 2, 4, \dots, 16{,}384$로 자란다. $2^{13}=8{,}192<12{,}000\le2^{14}=16{,}384$이므로 할당 15번이고, 그 길에 원소 $1+2+\dots+8{,}192=16{,}383$개를 옮긴다. 첫 판에는 그런 벡터가 둘, 샘플과 로그가 있으므로 루프는 $12{,}000+15+15=12{,}030$번 할당하며, 그 크기는

$$1{,}152{,}096{,}000+16\cdot32{,}767+32\cdot32{,}767=1{,}152{,}096{,}000+524{,}272+1{,}048{,}544=1{,}153{,}668{,}816\ \text{bytes}$$

다. 두 배로 자랄 때마다 새 용량만큼의 블록을 할당하고 $1+2+\dots+16{,}384=32{,}767$이기 때문이다. 로그의 가장 큰 성장은 레코드 8,193번, 실행 41 s째에 오고, 틱 하나 안에서 레코드 8,192개, 262,144바이트를 옮긴다. 생성자에 `reserve(12'000)`가 있으면 로그는 루프 전에 $12{,}000\cdot32=384{,}000$바이트를 한 번 할당하고 루프 안에서는 한 번도 하지 않는다. 링은 아예 하지 않는다. 1분에 걸쳐 평균하면 첫 판의 로그는 초당 $15/60=0.25$번 자랐다. 해롭지 않아 보이는 숫자이고, 4분의 1메가바이트를 옮긴 틱 하나를 숨긴다. 영어 절의 `tick_cost.cpp`가 두 판을 12,000틱씩 돌리며 할당을 센다. 첫 판은 할당 12,030번에 1,153,668,816바이트, §9의 판은 할당 0번에 0바이트이고, 크기는 샘플 16, 레코드 32, 링 96바이트다.

두 루프 모두 같은 속도 0.0977 m/s를 계산한다. 가짜 엔코더가 틱마다 한 카운트씩 가기 때문이다. 하나는 12,030번 할당하고 다른 하나는 한 번도 하지 않는다.

**5단계 — 누가 노드를 살려 두는가(§5).** ROS 2 노드로 감싸면 제어기는 노드만큼 살고, 노드는 사용 횟수가 0보다 큰 동안 산다. `ownership.cpp`가 노드의 생애를 따라 횟수를 찍었다. `make_shared` 뒤 1, `this`를 캡처하는 콜백으로 타이머를 만든 뒤에도 1, `spin`이 값으로 받은 사본을 쥐는 동안 2, 그 뒤 1, 그리고 `main`이 놓을 때 0이다. 그 순간 소멸자가 돌고 구동기가 0이 된다. 대신 `shared_from_this()`를 캡처하면 횟수는 1, 2, 3, 2, 그리고 마지막에 1이다. 노드는 타이머를 소유하고 타이머의 콜백은 노드를 소유하며, 구동기를 정지시켰을 소멸자는 끝내 돌지 않는다.

**6단계 — 예산(§9).** 틱에는 $T=1/f_c=1/200\ \mathrm{s}=5$ ms가 있다. 이 노트북에서 잰 §9의 틱은 열 번의 실행에서 평균 0.022–0.028 µs, 최대 1.2–10.7 µs가 걸렸다. 최악이 주기의 약 0.2%다. 대신 다음 비전 목표를 기다리는 틱은

$$T_v=\frac{1}{f_v}=\frac{1}{50\ \mathrm{Hz}}=20\ \mathrm{ms}=4\,T$$

까지 기다린다. 목표가 네 번째 틱마다 한 번만 오기 때문이다. 그런 루프는 목표 주기인 50 Hz로 돌고, 틱 넷 가운데 셋을 잃는다. 그리고 첫 판의 속도 호출 하나만으로도, 같은 방식으로 재면 1시간 분량의 이력에서 중앙값 0.41–0.56 ms, 가장 느린 호출 1.0–2.8 ms에 이른다.

| 60 s 실행 끝의 틱 하나 | 첫 판 | §9의 틱 |
|---|---:|---:|
| 복사한 바이트: 샘플, 속도 인자, 로그 레코드 | 16 + 192,000 + 32 | 16 + 0 + 32 |
| 틱 안의 힙 할당 | 1번, 실행 전체로 성장 30번 추가 | 0 |
| 실행 전체의 할당 | 12,030 | 0 |
| 실행 전체에 할당한 바이트 | 1,153,668,816 | 0 |
| 다른 스레드를 기다리는 최악 | 여기서는 없음. 목표를 막혀서 기다리면 최대 20 ms 추가 | 없음: 원자적 적재 한 번 |

### 10. 도구, 그리고 이 페이지가 다루지 않는 것

*한 문장으로:* 이 페이지의 결함들은 스스로 드러나지 않으므로 도구가 찾아야 하는데, 컴파일러 경고는 일부를 프로그램이 돌기 전에 잡고, 새니타이저는 도는 동안 나머지 대부분을 잡으며, 디버거는 멈춘 자리를 보여 주고, 이 페이지가 빼놓은 것에는 더 나은 집이 있으며 끝에 적어 둔다.

**경고.** 모든 것을 `-Wall -Wextra`로 빌드하고, 지속적 통합에서는 `-Werror`를 더해 경고가 병합되지 못하게 한다. 이 페이지에서 경고는 기대보다 덜 했다.

| 결함 | clang이 한 말 | 절 |
|---|---|---|
| 지역 변수에 대한 참조 반환 | 플래그 없이도 경고(`-Wreturn-stack-address`) | §2 |
| 순서가 어긋난 멤버 초기화 목록 | `-Wall`에서 경고(`-Wreorder-ctor`) | §4 |
| 사용자 소멸자가 있는 클래스의 복사 | `-Wall -Wextra`에서는 침묵, `-Wdeprecated`가 경고 | §4 |
| 가상 소멸자 없는 기반을 통한 삭제 | 플래그 없이도 경고(`-Wdelete-abstract-non-virtual-dtor`) | §7 |
| 헤더에 정의한 비인라인 함수 | 침묵, 링커가 보고 | §8 |
| `shared_ptr` 순환, 틱 안의 할당이나 막히는 호출 | 침묵 | §5, §9 |

**새니타이저.** AddressSanitizer(`-fsanitize=address`)는 모든 메모리 접근을 계측해, 힙·스택·전역 객체의 경계 밖 읽기와 쓰기, 해제 후 사용, 반환 후 사용, 범위 밖 사용, 이중 해제나 잘못된 해제를 찾는다. 전형적인 속도 저하는 약 2배다. 리눅스에서는 누수 검사기 LeakSanitizer가 기본으로 켜져 있어, 프로그램이 끝날 때 해제되지 않은 것을 보고한다. UndefinedBehaviorSanitizer(`-fsanitize=undefined`)는 정의되지 않은 연산의 목록 — 부호 있는 오버플로, null이거나 정렬이 어긋난 포인터, 범위를 벗어난 시프트, 경계 밖 첨자, 틀린 동적 타입의 포인터를 통한 호출 등 — 을 검사하고, 보고를 찍은 뒤 기본으로 계속 간다. `-fno-sanitize-recover`는 멈추게 한다. GCC와 Clang 모두 두 옵션을 받는다. 데이터 경쟁을 찾는 ThreadSanitizer는 AddressSanitizer와 함께 쓸 수 없으므로 따로 빌드해야 한다. 새니타이저는 시험 빌드와 벤치 실행용이지, 실시간으로 로봇을 모는 바이너리용이 결코 아니다. 프로그램을 느리게 하고 — AddressSanitizer는 약 2배 — 메모리를 할당하는 방식을 바꿔 놓는다.

영어 절에 §2의 자기 객체보다 오래 사는 콜백에 대해 AddressSanitizer가 찍은 보고가 있다. 프레임에 파일과 줄이 붙도록 `-g`로 빌드했다. 스택 셋으로 나누어 읽는다. 첫째는 잘못된 접근이 일어난 곳이다. 8바이트 읽기 — 필터의 `double` 둘 가운데 하나 — 가 17행 `update()`에서 일어났고, 15행의 람다를 거쳐 9행 `run_once()`가 불렀으며, 그것은 `main`의 30행에서 불렸다. 둘째는 그 메모리가 해제된 곳이다. 29행의 `filter.reset()`이 부른 `operator delete`(`_ZdlPv`는 그 맹글링된 이름)다. 셋째는 할당된 곳이다. 26행의 `make_unique`가 부른 `operator new`(`_Znwm`)다. 16바이트 영역은 `GoalFilter` 전체다. 사용, 해제, 할당의 세 줄 번호가 진단의 전부다. 30행의 무언가가 29행이 소멸시킨 것을 썼다.

UndefinedBehaviorSanitizer는 정의되지 않은 연산 자체에 이름을 붙인다. 영어 절의 `null_read.cpp`가 일부러 틀리게 쓴 예로, null 포인터를 통해 샘플의 `counts`를 읽는다. UBSan은 `null_read.cpp:7:60: runtime error: member access within null pointer of type 'const EncoderSample'`을 찍고, 이어 AddressSanitizer가 `SEGV on unknown address 0x000000000008`, 읽기 접근, 0번 페이지를 가리키는 주소라고 보고한다. 문제의 주소 8은 재배치한 샘플(§3)에서 `counts`의 오프셋을 null 포인터에 더한 값이다.

**디버거, 한 문단으로.** `-g`로 (줄 단위로 따라가고 싶으면 `-O0`까지) 빌드하고, macOS에서는 `lldb`, 리눅스에서는 `gdb` 아래에서 프로그램을 띄운 뒤 `run`을 친다. 프로그램이 죽으면 디버거는 프로그램을 그대로 둔 채 문제의 줄에서 멈춘다. `-g -O0`로 빌드한 `null_read`는 `stop reason = EXC_BAD_ACCESS (code=1, address=0x8)`와 함께 `counts_of(s=0x0000000000000000) at null_read.cpp:7:60`에서 멈췄다. 함수, null 인자, 열까지 짚는다. 이어 `bt`(gdb에서는 `backtrace`)가 그 자리에 이른 호출의 사슬을 찍고, `frame`이나 `up`이 그 사슬을 따라 움직이며, `print`가 변수를 보이고, 중단점(lldb에서는 `b file:line`, gdb에서는 `break file:line`)이 다음 실행을 더 일찍 멈춘다. ROS 2 노드라면, 백트레이스에 대한 ROS 2 how-to 가이드대로 `colcon build --packages-up-to <package> --cmake-args -DCMAKE_BUILD_TYPE=Debug`로 패키지를 빌드하고 `ros2 run --prefix 'gdb -ex run --args' <package> <executable>`로 노드를 띄워, ROS 환경을 그대로 둔 채 노드가 gdb 안에서 돌게 한다.

**이 페이지가 다루지 않는 것.** 간단한 것을 읽고 쓰는 것을 넘어서는 템플릿 — 메타프로그래밍, 콘셉트, 가변 인자 템플릿. §5의 한 문단을 넘는 이동 의미론 — rvalue 참조, 직접 쓰는 이동 생성자, 완벽한 전달. §9의 규칙을 넘는 동시성 — 스레드, 원자 변수의 메모리 순서, 잠금 없는 자료구조. 스레드, 경쟁, 잠금, 교착 일반은 [[02-foundations/tools/concurrency|12.8 동시성]]이고, rclcpp의 executor가 콜백을 스레드에 어떻게 올리는지는 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §1]]과 [[04-robotics/ros2/executors-callbacks-time|25.5.1 §2]]다. 인터페이스 하나를 넘는 객체지향 설계. `CMakeLists.txt` 하나를 넘는 빌드 시스템은 [[04-robotics/ros2/workspaces-packages-launch|25.4]]가 이어 간다. 언어 자체에 대해서는 이 페이지 내내 참고한 cppreference.com이 참조서이고, C++ Core Guidelines는 이 페이지가 두 번 인용한 규칙집이다. 처음부터 끝까지 읽기보다, 리뷰가 규칙을 인용할 때 그 규칙을 읽는다.

### 읽고 나면

- [ ] `T`, `const T&`, `T&`, `const T*` 타입의 매개변수가 각각 함수에게 무엇을 허용하는지, 200 Hz에서 호출마다 각각 얼마가 드는지 말한다.
- [ ] 네 가지 저장 기간을 대고, 자동 객체와 동적 객체가 언제 죽는지 말하며, §2의 댕글링 참조 두 가지를 보자마자 알아본다.
- [ ] 구조체를 오프셋과 패딩까지 바이트 단위로 배치하고, 페이로드가 허용하는 가장 작은 크기로 재배치한다.
- [ ] 자원을 소유하는 클래스를 RAII로 쓴다. 생성자에서 획득하고, 소멸자에서 풀고, 복사를 지운다. 그리고 RAII가 다루지 못하는 출구를 말한다.
- [ ] rclcpp 코드 한 조각에서 누가 무엇을 소유하는지 말하고, `make_shared`, 타이머, `spin`을 지나는 노드의 사용 횟수를 추적하고, `shared_ptr` 순환을 끊는다.
- [ ] `RingBuffer<T, N>` 같은 클래스 템플릿을 읽고 쓰며, `std::vector`가 언제 할당하는지, `reserve`가 무엇을 바꾸는지, 두 배 성장이 최악의 틱에서 얼마를 치르는지 말한다.
- [ ] 가상 소멸자를 가진 인터페이스를 선언하고 두 번 구현하며, `virtual`이 없으면 무엇이 잘못되는지 말한다.
- [ ] 컴파일러와 링커가 각각 무엇을 하는지 말하고, 정의되지 않은 심볼과 중복된 심볼 오류를 그 메시지로부터 고친다.
- [ ] 실시간 틱의 규칙을 각각의 이유와 함께 말하고, 틱의 할당과 최악의 경우를 시험한다.
- [ ] 새니타이저 보고 — 접근, 해제, 할당 — 를 읽고, 디버거로 백트레이스를 얻는다.

### 스스로 점검

1. 처음 쓴 그대로의 `EncoderSample`은 24바이트이고 재배치하면 16바이트다. 8바이트는 어디로 가며, 어떤 순서로든 13바이트로 만들 수 있는가?
2. 어떤 도우미가 `std::vector<EncoderSample> history`를 값으로 받고, 틱마다 실행의 모든 샘플을 받아 한 번 불린다. 60 s 실행 끝에서 호출 한 번의 값은 얼마이고, 매개변수 타입을 어떻게 바꾸면 그 거의 전부가 사라지는가?
3. 함수가 지역 변수에 대한 `const EncoderSample&`를 돌려주는데 프로그램은 맞는 카운트를 찍는다. 이것이 왜 프로그램이 옳다는 증거가 못 되며, 무엇이 틀렸음을 보여 주는가?
4. 노드의 타이머 콜백이 `shared_from_this()`를 캡처한다. `make_shared`부터 `main`의 끝까지 노드의 사용 횟수를 추적하고, 노드가 소유한 구동기에 무슨 일이 일어나는지 말하라.
5. `std::unique_ptr<MotorInterface> motor_`가 `RealMotor`를 쥐고 있고 `MotorInterface`에는 가상 소멸자가 없다. 제어기가 소멸할 때 무슨 일이 일어나며, clang은 무엇이라고 말하는가?
6. `controller.cpp`가 `CartController::tick`을 정의하는데도 링커가 그것을 정의되지 않은 심볼로 보고한다. 원인 둘을 대라.
7. 벤치에서 틱이 평균 0.02 µs다. 실시간 안전한가? 무엇을 확인하고 무엇을 재겠는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 패딩으로 간다. 처음 쓴 그대로는 1바이트 `valid`와 8바이트 `stamp_ns` 사이에 7바이트, `counts` 뒤에 20을 24로 올리는 4바이트가 있다. 재배치하면 꼬리 패딩 3바이트만 남는다. 13은 어떤 순서로도 안 된다. 구조체가 8로 정렬되므로 크기는 8의 배수이고, $\lceil 13/8\rceil\cdot8=16$이 가능한 가장 작은 값이다.
> 2. 틱 12,000에서 $12{,}000\cdot16=192{,}000$바이트를 새로 할당한 블록에 복사한다. 틱마다 할당 한 번과 192 kB, 초당 38.4 MB와 할당 200번이다. 매개변수를 `const std::vector<EncoderSample>&`로 선언하면 주소 하나, 8바이트만 넘어가고 할당은 없다. 더 나은 변경은 링 버퍼다. 이력이 자라는 것까지 멈춘다.
> 3. 죽은 객체를 읽는 것은 정의되지 않은 동작이고, 정의되지 않은 동작이 할 수 있는 일 가운데 하나가 옛 값을 돌려주는 것이기 때문이다. 죽은 프레임을 아직 아무것도 덮어쓰지 않았을 뿐이다. 컴파일러의 `-Wreturn-stack-address` 경고가 이미 틀렸다고 말하고, 리눅스의 기본값인 `detect_stack_use_after_return=1`을 켠 AddressSanitizer가 읽기를 멈추고 `latest()`의 프레임을 짚는다.
> 4. `make_shared` 뒤 1. 타이머를 만든 뒤 2, 타이머에 저장된 콜백이 사본을 쥐기 때문이다. `spin` 안에서 3, 자기 사본을 값으로 받기 때문이다. `spin`이 돌아온 뒤 2. `main`의 포인터가 소멸한 뒤 1. 0에 닿지 않는다. 노드가 타이머를 소유하고 타이머의 콜백이 노드를 소유하므로, 노드의 소멸자는 돌지 않고 구동기는 그것에 의해 0을 명령받지도 꺼지지도 않는다. `this`나 `weak_ptr`을 캡처한다.
> 5. 가상이 아닌 소멸자를 가진 `MotorInterface*`를 통해 `RealMotor`를 지우는 것은 정의되지 않은 동작이다. §7의 실행에서는 `~RealMotor`가 그냥 돌지 않았으므로, 구동기는 마지막 명령으로 켜진 채 남았을 것이다. clang은 `-Wall` 없이도 "delete called on 'MotorInterface' that is abstract but has non-virtual destructor"라고 경고한다. 고치는 법은 `virtual ~MotorInterface() = default;`다.
> 6. 정의를 담은 목적 파일이 프로그램에 링크되지 않았다 — `controller.cpp`가 라이브러리에서 빠졌거나, 프로그램이 라이브러리를 링크하지 않는다. 또는 정의가 선언과 맞지 않는다 — 매개변수 타입이 다르거나, `const`가 빠졌거나, `tick`을 `CartController::` 접두사 없이 정의해 아무도 부르지 않는 자유 함수를 만들었다.
> 7. 평균으로는 알 수 없다. 코드에서 할당, 막힘, 잠금, 예외 — §9의 규칙 — 를 확인하고 시험한다. §9의 `main.cpp`처럼 루프 둘레의 할당을 센다. 그다음 로봇 자신의 컴퓨터에서 부하 아래 긴 실행으로 평균이 아니라 최악의 틱을 재고, 그것을 5 ms에서 코어가 해야 할 다른 모든 일을 뺀 값과 비교한다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6 Lab Plants]]만 쓴다. 손으로 하는 과제다. C++는 읽고 추론하며, 위키의 검사는 그것을 실행하지 않는다. 원하면 직접 컴파일해 본다. 문제마다 계산 절의 손잡이를 하나씩 — 구조체, 루프 주기, 리뷰할 코드 — 바꾸므로 페이지에서 답을 그대로 옮길 수 없다.

1. **그리기.** P6의 카트에 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]의 단축 IMU가 붙어 엔코더와 함께 200 Hz로 읽히고, 그 드라이버가 영어 절 문제 1의 `ImuSample`을 내준다. 필드는 `bool valid`, `double accel_mps2`, `std::uint16_t seq`, `std::int64_t stamp_ns`, `float gyro_rps` 순서다. 그림을 이 샘플에 맞게 다시 그린다. (a) 패널에는 `ImuSample`을 쓴 그대로, 그리고 필드를 정렬이 큰 순서로 재배치한 것을 바이트 단위로 그리되, 모든 오프셋과 음영 친 패딩과 두 크기를 적는다. (b) 패널에는 제어기 안에 `RingBuffer<ImuSample, 5>`를, 그리고 노드가 `std::unique_ptr`로 소유하는 IMU 드라이버를 더하고, 새 링의 바이트를 적는다. IMU 샘플이 각 순서에서 초당 몇 바이트를 치르는지 말하라.
2. **유도.** P6의 제어기를 200 Hz 대신 $f_c=1$ kHz로, 다른 숫자는 그대로 두고 같은 60 s 동안 돌린다. (a) 로그: 예약할 때의 바이트, `reserve` 없이 자라는 횟수, 최종 용량의 바이트, 옮기는 레코드 수, 그리고 가장 많이 옮기는 push가 어느 것이며 몇 바이트를 언제 옮기는지. (b) 첫 판의 값 이력: 마지막 틱에서 복사하는 바이트, 끝에서 초당, 실행 전체로, 그리고 루프가 하는 할당 횟수. (c) 20 ms 속도 창을 지키는 링 길이 $K$와 그 `sizeof`, 그리고 $K$를 5로 두었을 때의 한 카운트 속도. (d) 다음 50 Hz 목표를 기다리는 틱이 몇 주기 동안 막힐 수 있으며, 그런 루프가 틱의 몇 분의 몇을 잃는지. (e) 노드의 사용 횟수에서 무엇이 바뀌는지.
3. **해석.** 코드 리뷰. 영어 절 문제 3의 노드는 한 연구실 저장소에서 온 것으로 P6의 카트를 몬다. 결함 다섯 개를 하나하나 이름 대고, 각각이 카트에 무엇을 하는지 말하고, 고치는 법을 적는다. 그다음 그 가운데 무엇을 `-Wall -Wextra`가 컴파일 때 보고했을지, 무엇을 AddressSanitizer가 시험 실행에서 잡았을지, 무엇은 리뷰나 §9 같은 시험만이 찾을지 말하라.

> [!note]- 그리는 법 · How to draw it
> - (a) 패널의 척도를 하나로 한다. 칸 하나가 1바이트, 모든 줄에서 같은 너비이고, 8의 배수마다 오프셋을 적는다.
> - 각 멤버를 자기 정렬의 다음 배수에 놓고 틈을 음영 친 뒤, 끝을 구조체의 가장 큰 정렬로 올리고 꼬리를 음영 친다. 크기는 그 정렬의 배수로 나와야 한다.
> - 재배치한 줄은 멤버를 정렬이 큰 순서로 늘어놓고, 결과를 한계 $\lceil \text{payload}/a_S\rceil\,a_S$와 비교한다. 크기가 그 한계에 닿으면 어떤 순서도 더 낫지 않다.
> - (b) 패널에서는 스택과 힙을 떼어 놓는다. 다른 객체 안에 저장된 객체 — 링 버퍼, 원자 변수 — 는 그 상자 안에 화살표 없이 그린다. 화살표는 포인터에만 그린다. 소유자(`unique_ptr`, `shared_ptr`, 벡터의 저장 공간)는 실선, 관찰자(날 포인터, 캡처한 `this`, `weak_ptr`)는 점선이다.
> - 모든 `shared_ptr` 간선에 사용 횟수를 적는다. 스택에서 실선 화살표를 따라갔을 때 이미 지나온 상자로 돌아올 수 있으면 순환이 있는 것이고, 그 간선 하나는 점선이 되어야 한다.
> - 틱이 건드리는 모든 것 — 각 링, 로그 저장 공간 — 옆에 바이트를 적는다.

> [!tip]- 정답 · Solutions
> 1. 쓴 그대로: `valid`는 0, 패딩 1–7, `accel_mps2` 8–15, `seq` 16–17, 패딩 18–23, `stamp_ns` 24–31, `gyro_rps` 32–35, 꼬리 패딩 36–39. 멤버는 36에서 끝나고 크기는 40바이트로 올라가며, 페이로드 $1+8+2+8+4=23$에 대해 패딩이 17바이트다. 정렬이 큰 순서로 재배치: `accel_mps2` 0–7, `stamp_ns` 8–15, `gyro_rps` 16–19, `seq` 20–21, `valid` 22, 꼬리 패딩 23. 24바이트에 패딩 1바이트이고, 이것이 한계 $\lceil 23/8\rceil\cdot8=24$이므로 어떤 순서도 더 낫지 않다. (컴파일한 확인 프로그램은 오프셋 0, 8, 16, 24, 32와 0, 8, 16, 20, 22와 함께 40과 24를 찍는다.) (b) 패널: 제어기 안에 `imu_history_: RingBuffer<ImuSample, 5>`, 제자리에 $5\cdot24+16=136$바이트(쓴 그대로라면 $5\cdot40+16=216$), 화살표 없음. 노드는 `imu_: unique_ptr<ImuDriver>`를 얻고 힙의 `ImuDriver` 상자로 실선 화살표를 그으며, 단일 소유자에게는 횟수가 없으므로 횟수는 적지 않는다. 노드 자신의 횟수는 그대로 1, `spin`이 쥐는 동안 2다. 200 Hz에서 IMU 샘플은 쓴 그대로 초당 $200\cdot40=8{,}000$바이트, 재배치하면 $200\cdot24=4{,}800$바이트다. 엔코더의 3,200을 더하면 두 흐름의 합은 재배치해서 초당 8,000바이트, 처음 쓴 그대로라면 12,800바이트다.
> 2. (a) 예약하면 $60{,}000\cdot32=1{,}920{,}000$바이트, 루프 전에 할당 한 번. `reserve` 없이는 $2^{15}=32{,}768<60{,}000\le2^{16}=65{,}536$이므로 17번 자라고, 최종 용량은 레코드 65,536개, 2,097,152바이트이며, 레코드 $1+2+\dots+32{,}768=65{,}535$개를 옮긴다. 가장 큰 이동은 32.768 s째의 push 32,769번이고, 틱 하나에서 레코드 32,768개, 1,048,576바이트를 옮긴다. (b) 마지막 틱에서 $60{,}000\cdot16=960{,}000$바이트, 끝에서 초당 $1{,}000\cdot960{,}000=960$ MB, 실행 전체로 $16\cdot60{,}000\cdot60{,}001/2=28{,}800{,}480{,}000$바이트, 약 28.8 GB. 루프는 $60{,}000+17+17=60{,}034$번 할당한다. (c) $K-1=0.020/0.001=20$이므로 $K=21$이고 `sizeof`는 $21\cdot16+16=352$바이트다. $K=5$면 창은 4 ms이고 한 카운트는 $1/(2048\cdot0.004)=0.122$ m/s로, 20 ms 창의 0.0244 m/s의 다섯 배다. (d) 최대 $T_v=20$ ms이고, 이제 그것은 20주기다. 루프는 50 Hz로 돌며 틱 20개 가운데 19개, 95%를 잃는다. (e) 아무것도 바뀌지 않는다. 사용 횟수는 틱이 아니라 소유자를 센다. `this`를 캡처하면 1, 1, `spin` 안에서 2, 1, 0이고, 순환이면 1, 2, 3, 2, 1이다.
> 3. (i) `~Drive() {}`가 가상이 아닌데 `drive_`는 `SerialDrive`를 쥔 `unique_ptr<Drive>`다. 노드를 소멸시키면 기반을 통해 지운다. 정의되지 않은 동작이고, 실제로는 `~SerialDrive`가 돌지 않아 노력은 0이 되지 않고 구동기는 꺼지지 않으며 포트는 닫히지 않는다. clang은 `-Wall` 없이도 경고한다. 고치는 법: `virtual ~Drive() = default;`. (ii) `start()`가 노드에 대한 `shared_ptr`인 `self`를 노드 자신의 타이머 콜백에 저장한다. 노드는 타이머를, 타이머는 노드를 소유하므로 사용 횟수는 0에 닿지 않고, 노드와 그 `drive_`는 끝내 소멸하지 않는다. 그래서 깨끗한 Ctrl-C 정지 뒤에도 구동기는 켜진 채 남고, (i)을 고쳐도 여전히 그렇다. 아무것도 경고하지 않는다. 리눅스에서는 LeakSanitizer가 종료 때 새어 나간 노드를 보고한다. 고치는 법: 노드가 타이머를 소유하므로 `this`를 캡처하거나, `weak_ptr`을 캡처한다. (iii) `read_encoder()`가 자기 지역 `s`에 대한 참조를 돌려주므로 `tick()`은 죽은 샘플로 노력을 계산한다. 벤치에서는 운 좋게 맞고, 현장에서는 쓰레기다. clang이 경고하고(`-Wreturn-stack-address`), 리눅스의 기본값인 반환 후 사용 검출을 켠 AddressSanitizer가 `history_.push_back(s)`에서 읽기를 멈춘다. 고치는 법: `EncoderSample`을 값으로 돌려준다. (iv) 틱 안의 `history_.push_back(s)`. 벡터는 한없이 자라며 두 배가 될 때마다 재할당한다. 첫 1분에 15번이고, 가장 최근 것은 틱 하나에서 샘플 8,192개, 131,072바이트를 옮긴다. 메모리는 노드가 도는 한 초당 $16\cdot200=3{,}200$바이트씩, 시간당 샘플 11.52 MB씩 는다. 아무것도 보고하지 않고, §9의 할당 세기라면 잡는다. 고치는 법: `RingBuffer<EncoderSample, 5>`, 또는 생성자에서 예약하고 길이를 제한한 로그. (v) `on_goal()`이 `plan_path_to`의 12 ms 동안 `goal_mutex_`를 쥐고, `tick()`이 같은 잠금을 잡는다. 계획 도중에 도착한 틱은 최대 12 ms, 2.4주기를 기다리고, 50 Hz에서 잠금은 20 ms마다 12 ms 잡혀 있으므로 틱 다섯 가운데 셋이 잡힌 잠금을 만난다. 비전 스레드의 우선순위가 낮다면 우선순위 역전이 기다림을 더 늘릴 수 있다. 아무것도 보고하지 않고, 최악의 틱을 재면 잡는다. 고치는 법: 계획은 잠금 밖에서 하고 목표는 `std::atomic<double>`이나 `RealtimeBuffer`로 넘겨, 틱이 결코 기다리지 않게 한다. 요약: 경고는 (i)과 (iii)을 잡고, AddressSanitizer는 실행 중에 (iii)을, 리눅스에서는 LeakSanitizer가 종료 때 (ii)를 잡는다. (iv)와 (v)에는 리뷰나 §9의 시험이 필요하다.

### 출처

- cppreference.com([en.cppreference.com/w/cpp](https://en.cppreference.com/w/cpp)) — 이 페이지가 인용한 언어·라이브러리 규칙: 저장 기간과 수명, 참조와 포인터, 정의되지 않은 동작, 객체 배치와 `sizeof`, 생성자·소멸자·예외, `std::exit`, RAII와 0의 규칙, 암시적 복사의 폐기 예정, 스마트 포인터와 `enable_shared_from_this`, `std::move`, 컨테이너와 `reserve`, 템플릿, 가상 함수와 추상 클래스, ODR, `#pragma once`, `operator new`, `std::atomic`.
- ISO C++ 작업 초안([eel.is/c++draft](https://eel.is/c++draft/))과 N4659로 본 C++17 표준([timsong-cpp.github.io/cppwp/n4659](https://timsong-cpp.github.io/cppwp/n4659/)) — 정렬, `sizeof`, 멤버 배치, 가상 소멸자 없는 기반을 통한 삭제, 정의되지 않은 동작이 거슬러 올라가는 범위.
- C++ Core Guidelines([isocpp.github.io/CppCoreGuidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)) — F.16("입력" 매개변수를 넘기는 법)과 F.43(지역 객체에 대한 포인터나 참조를 돌려주지 마라).
- System V AMD64 psABI([gitlab.com/x86-psABIs/x86-64-ABI](https://gitlab.com/x86-psABIs/x86-64-ABI))와 Arm의 AAPCS64([github.com/ARM-software/abi-aa](https://github.com/ARM-software/abi-aa)) — 스칼라의 크기와 정렬, 구조체의 정렬과 크기.
- Itanium C++ ABI, Exception Handling([itanium-cxx-abi.github.io](https://itanium-cxx-abi.github.io/cxx-abi/abi-eh.html)) — §2.4.2, 예외 객체는 가능하면 힙에 할당.
- LLVM libc++의 `__vector/vector.h`와 GCC libstdc++의 `bits/stl_vector.h` — 가득 찬 벡터를 키우는 규칙.
- rclcpp, Jazzy 브랜치([github.com/ros2/rclcpp](https://github.com/ros2/rclcpp/tree/jazzy)) — `macros.hpp`, `node.hpp`, `timer.hpp`, `callback_group.hpp`, `executors.hpp`, `utilities.hpp`: 포인터 별칭, `enable_shared_from_this`, `WeakPtr`로 보관하는 타이머, 값으로 받는 `spin`, 기본 신호 핸들러.
- ros2_control과 realtime_tools, Jazzy 브랜치([github.com/ros-controls](https://github.com/ros-controls)) — `hardware_component_interface.hpp`(지운 복사, 실시간 안전하지 않은 이름 기반 접근자), `controller_interface_base.hpp`("needs to be real-time safe"인 `update`), `realtime_buffer.hpp`(`try_to_lock`).
- ROS 2 문서, Jazzy 브랜치([github.com/ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — "Understanding real-time programming"(피할 것, `mlockall`, 우선순위 98, PREEMPT_RT, 예시 지연), "Getting Backtraces in ROS 2", C++ 퍼블리셔 튜토리얼(`[this]`, `ament_target_dependencies`). J. Kay, "Introduction to Real-time Systems"([ros2/design](https://github.com/ros2/design), 2016).
- ament_cmake, Jazzy 브랜치 — `ament_target_dependencies`가 타깃에 더하는 것.
- CMake 문서([cmake.org/cmake/help/latest](https://cmake.org/cmake/help/latest/)) — `add_library`, `add_executable`, `target_link_libraries`, `target_include_directories`, `CXX_STANDARD`.
- Clang 문서([clang.llvm.org/docs](https://clang.llvm.org/docs/AddressSanitizer.html)) — AddressSanitizer와 UndefinedBehaviorSanitizer. GCC의 *Program Instrumentation Options* — 두 새니타이저, 따로 빌드하는 ThreadSanitizer.
- GNU ld 매뉴얼([sourceware.org/binutils/docs/ld](https://sourceware.org/binutils/docs/ld/Options.html))과 binutils 버그 27311 — 중복 정의는 치명적 오류, "undefined reference to"와 "multiple definition of"라는 문구.
- 실행 환경: macOS 26.6.2를 도는 Apple M1 위의 Apple clang 21.0.0, libc++, CMake 3.31.2. 리눅스 배치는 `--target=x86_64-unknown-linux-gnu`와 `--target=aarch64-unknown-linux-gnu`로 확인했다.
