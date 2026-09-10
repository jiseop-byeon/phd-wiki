---
title: 24.6 Hapkit Lab & Real-Time Software
tags: [haptics, mechatronics, software]
study-depth: Working
wiki-support: Working
depth-goal: "Bring up a one-DOF haptic device in safe layers and produce logs that distinguish wiring, calibration, timing, dynamics, and rendering failures."
mastery-when: "Master embedded current control and safety engineering when the experimental platform itself carries the contribution."
---

## English

### 1. What the course kit can teach

The local Longhorn Hapkit packet contains seven printable mechanical parts—base, PCB mount, sector, handle, bearing housing, motor shaft, and tensioner—plus a brushed DC motor with encoder, Arduino-class controller, H-bridge, cable/capstan transmission, and assembly instructions. It is a one-DOF platform: ideal for learning the full loop because every hidden approximation becomes visible.

The mesh files are manufacturing geometry, not a specification. Before printing, inspect units, bounding boxes, tolerances, bearing/motor revisions, layer direction, support, shaft fit, and cable path. A seam or rough pulley can be felt as a periodic force artifact.

> [!warning] Version conflict
> Two supplied documents assign the H-bridge direction pins in opposite order. Do not copy either mapping blindly. Trace the actual board, identify its revision, compare against the current starter code, test with motor power limited/off where appropriate, and verify encoder and commanded torque signs separately. Never publish or reuse room access codes contained in teaching slides.

### 2. Safe bring-up ladder

1. **Mechanical-only:** confirm free motion, hard stops, cable alignment/tension, no rubbing, and secure mounting.
2. **Logic-only:** common reference ground, correct logic voltage, no motor supply; read encoder counts and direction.
3. **Low-energy actuation:** current-limited supply; short pulses away from stops; emergency power cut accessible.
4. **Calibration:** counts→radians, handle radius/transmission, motor current→torque, torque sign, zero position.
5. **Free-space controller:** command zero torque, then small viscous damping; measure friction and bias.
6. **Soft virtual wall:** start with low $K$, log $x$, $\hat v$, $F$, command, current, loop period, saturation, and energy.
7. **Increase cautiously:** change one parameter at a time; stop at oscillation, excessive force, current, temperature, or missed deadlines.

### 3. Minimal control architecture

The hard real-time path should be bounded and allocation-free:

```text
read encoder → convert units → estimate velocity → compute contact/proxy
→ compute force → map to motor torque/current → saturate safely → write command
```

Graphics, file I/O, networking, model loading, and console output belong in slower threads. Transfer the newest state through a bounded, nonblocking mechanism. “1 kHz” means every deadline is met closely enough for the design assumptions, not that the mean loop count is 1000 per second.

### 4. Filter convention that often causes bugs

The supplied lecture uses

$$y_k=\alpha x_k+(1-\alpha)y_{k-1},$$

so larger $\alpha$ trusts the **new sample** more and filters less. Many signal-processing texts and the foundation page instead use

$$y_k=\alpha y_{k-1}+(1-\alpha)x_k,$$

where larger $\alpha$ trusts the **old output** more and filters more. The formulas are equivalent after replacing $\alpha$ by $1-\alpha$; the symbol alone is meaningless without the equation.

### 5. Simulation before hardware

Start with a mass–damper device and a human spring–damper model. For explicit Euler,

$$a_k=F_k/m,\quad v_{k+1}=v_k+Ta_k,\quad x_{k+1}=x_k+Tv_k.$$

Integration order matters. Semi-implicit Euler uses updated velocity in the position step and often behaves differently. A solver that appears stable at one step size may be hiding a numerical artifact, so sweep $T$ and compare energy.

### 6. Software route

- **MATLAB/Python:** dynamics, filters, integrators, and energy plots.
- **Arduino/C++:** deterministic sensor/actuator loop and calibration; keep motor protection outside application logic.
- **CHAI3D:** begin with its numbered examples, then trace the world/tool/device/haptic-thread structure and modify one effect. Its official documentation recommends learning through examples.
- **ROS 2:** use for state, commands, logging, experiments, and slower robot integration. A normal ROS graph is not automatically a hard-real-time haptic servo. ROS 2's real-time guidance emphasizes bounded latency, avoiding page faults, dynamic allocation, and indefinite blocking in the real-time path.

Official starting points: [CHAI3D documentation](https://chai3d.org/documentation/), [CHAI3D example review](https://www.chai3d.org/download/doc/html/chapter5-example.html), and [ROS 2 real-time programming](https://docs.ros.org/en/rolling/Tutorials/Demos/Real-Time-Programming.html).

### 7. Diagnostic table

| Symptom | First checks |
|---|---|
| force assists penetration | motor/encoder sign, frame normal, $J^\top$ convention |
| buzzes only in wall | sampling/jitter, stiffness, velocity phase, proxy switching |
| periodic ripple in free space | cogging, shaft seam, cable/pulley, encoder eccentricity |
| force weakens at speed | back-EMF, supply voltage, current saturation |
| occasional violent kick | missed deadline, stale packet, uninitialized state, derivative spike |

> [!question]- Self-check · Answer
> **Why should printing to the console be excluded from the haptic servo?** It has nondeterministic latency and can block. One missed deadline changes the zero-order hold interval and therefore the energy injected by the sampled controller.

## 한국어

### 1. 과목 키트가 가르치는 것

Longhorn Hapkit 자료에는 base·PCB mount·sector·handle·bearing housing·motor shaft·tensioner의 7개 출력 부품과 DC 모터·encoder·Arduino 계열 controller·H-bridge·cable/capstan 전달장치가 있다. 1자유도이므로 전체 햅틱 루프의 숨은 근사를 보기 좋은 플랫폼이다. STL은 제작 형상이지 완전한 사양서가 아니다. 단위·공차·부품 revision·출력 방향·shaft fit·cable path를 확인한다.

> [!warning] 버전 충돌
> 제공 문서 두 개의 H-bridge 방향 핀 순서가 서로 반대다. 실제 보드 revision과 배선, 현재 starter code를 대조하고 encoder 부호와 torque 부호를 따로 검증한다. 강의안에 포함된 출입 코드는 공개하거나 재사용하지 않는다.

### 2. 안전한 bring-up

기계 자유운동과 hard stop → motor power 없이 encoder → current limit를 둔 짧은 구동 → counts/radian·전류/토크·부호 보정 → zero torque와 작은 damping → 낮은 강성 벽 → 한 파라미터씩 증가 순서로 진행한다. 항상 $x,\hat v,F$, command, current, loop period, saturation, energy를 기록한다.

### 3. 실시간 구조

Hard real-time 경로는 encoder 읽기 → 단위 변환 → 속도 추정 → contact/proxy → 힘 → torque/current → 안전 포화 → 출력만 수행한다. 그래픽·파일·네트워크·모델 로딩·console은 느린 thread로 분리한다. 평균 1 kHz가 아니라 worst-case deadline과 jitter가 설계 가정 안에 있어야 한다.

### 4. 필터 $\alpha$ 규약

강의식 $y_k=\alpha x_k+(1-\alpha)y_{k-1}$에서는 큰 $\alpha$가 새 측정을 더 믿어 필터링이 약하다. 흔한 다른 식 $y_k=\alpha y_{k-1}+(1-\alpha)x_k$에서는 큰 $\alpha$가 과거 출력을 더 믿어 필터링이 강하다. 두 식은 $\alpha\leftrightarrow1-\alpha$ 관계이므로 숫자만 복사하면 안 된다.

### 5. 하드웨어 전 시뮬레이션

질량–댐퍼 장치와 사람 spring–damper를 먼저 시뮬레이션한다. 위 explicit Euler 식에서 position update가 이전 velocity를 쓰는지 새 velocity를 쓰는지에 따라 수치 에너지가 달라진다. 주기 $T$를 sweep하고 energy를 비교한다.

### 6. 소프트웨어 경로

MATLAB/Python으로 dynamics·filter·integrator, Arduino/C++로 deterministic I/O와 calibration, CHAI3D의 번호순 example로 virtual environment, ROS 2로 logging과 느린 시스템 통합을 배운다. 일반 ROS node graph를 hard-real-time 햅틱 servo라고 가정해서는 안 된다.

> [!question]- 스스로 점검 · 정답
> **햅틱 servo에서 console print를 빼야 하는 이유는?** 지연이 비결정적이고 block될 수 있다. 한 번의 missed deadline도 zero-order hold 시간을 바꾸고 샘플드 제어기가 주입하는 에너지를 바꾼다.

