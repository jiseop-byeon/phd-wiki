---
title: 24.4 Rendering, Sampling & Stability
tags: [haptics, control, passivity]
study-depth: Working
wiki-support: Working
depth-goal: "Explain and quantify why sampling, quantization, delay, and switching restrict rendered impedance; choose a defensible stabilization strategy."
mastery-when: "Master sampled-data proofs and passivity-controller design when stability or rendering performance is the contribution."
---

## English

### 1. Haptic rendering is a hard real-time feedback loop

An impedance display repeatedly senses joint position, applies forward kinematics, detects collision, finds a proxy/surface point, computes force, maps it by $J^\top$, and commands actuators. Graphics may update at tens of hertz; stiff contact commonly needs a haptic servo around a kilohertz or more. The important property is not average rate but bounded execution time and jitter.

A point-penetration wall is commonly written

$$F_k=\begin{cases}-Kx_k-B\hat v_k,&x_k>0\\0,&x_k\le 0,\end{cases}$$

where positive $x$ denotes penetration. The nearest geometric point is not always the correct proxy: near an edge it may jump to another face and eject the user sideways. Contact rendering therefore needs state/memory as well as collision detection.

### 2. Why a digital spring can create energy

The controller samples position and holds a force until the next update. During one interval $T$, a constant velocity $v$ moves $\Delta x=vT$. The zero-order hold makes the force lag the ideal spring. A useful worst-case energy estimate is

$$E_{\text{leak}}\approx\frac12K(vT)^2,$$

while physical viscous damping dissipates

$$E_{\text{diss}}=bv^2T.$$

Requiring $E_{\text{leak}}\le E_{\text{diss}}$ gives the intuitive bound

$$K\le\frac{2b}{T}.$$

With backward-difference virtual damping $B$, a classic one-DOF passivity condition under its model assumptions is $b>KT/2+|B|$. It is not a universal hardware rating: friction, delay, quantization, nonlinear kinematics, saturation, human grip, and implementation details change the boundary.

Worked example: with physical damping $b=0.1$ N·s/m and $T=1$ ms, the simple bound gives $K\le200$ N/m. Halving $T$ doubles that bound; adding digital damping does not substitute freely for physical dissipation because its estimate is delayed.

### 3. Sampling and quantization are different

Sampling hides **when** contact occurred between updates. Quantization hides **where** the device lies within an encoder interval $\Delta$. Under a simple Coulomb-friction model, another bound is $K\le2f_c/\Delta$. Faster sampling does not improve encoder resolution. Conversely, finer resolution does not eliminate zero-order-hold delay.

Velocity estimation exposes the tradeoff:

$$\hat v_k=\frac{x_k-x_{k-1}}{T}.$$

Small $T$ increases the velocity jump caused by one encoder count. Averaging over $n$ samples, $(x_k-x_{k-n})/(nT)$, reduces variance but increases effective delay. A low-pass filter should therefore be evaluated by both noise attenuation and phase at the contact frequencies.

### 4. Passivity, stability, and Z-width

With power defined positive into a one-port, passivity requires

$$E(t)=E_0+\int_0^t F(\tau)^\top v(\tau)d\tau\ge0.$$

Interconnected passive systems have strong stability properties, which avoids needing an exact high-frequency human model. But passivity is a sufficient design framework, not a guarantee of good feel, task success, or safety; it can be conservative, and active humans or actuators still require careful port definitions and assumptions.

**Z-width** is the range of impedances a device can render stably/passively—from light free space to hard contact. A stiffness–damping plot shows only part of it; frequency, minimum impedance, load, grip, and measurement location must be reported.

### 5. Three stabilization families

- **Virtual coupling:** place a virtual spring–damper between the device proxy and the simulated tool. It isolates a passive environment but softens transparency continuously.
- **Passivity observer/controller (PO/PC):** track discrete power/energy and inject damping only when the energy budget would be violated. It is adaptive but can introduce bursts, near-zero-velocity division problems, saturation, and delayed action after stored “energy credit.”
- **Hardware/perceptual design:** raise sample rate and sensor resolution, add physical/electrical high-frequency damping, reduce inertia, or add event-triggered impact vibration so a modest stable stiffness feels harder.

For a discrete sample, a common observer uses $\Delta E_k=T F_k^\top v_k$ with a declared sign convention. If the cumulative budget becomes negative, an impedance-causality controller may add $F_{pc}=-d_kv_k$ with $d_k$ chosen to cancel the deficit. Clamp and regularize this law near $\|v_k\|=0$; never interpret the formula without actuator limits.

### 6. Debugging order

1. Disable contact force and verify units, signs, frames, encoder direction, and motor current limits.
2. Log actual loop period and worst-case jitter, not only requested rate.
3. Add a low-stiffness wall without damping; inspect penetration, force, and energy.
4. Add velocity estimation and damping while plotting phase/noise.
5. Raise stiffness gradually; stop at sustained oscillation, saturation, overheating, or unsafe force.
6. Separate numerical instability, mechanical resonance, friction limit cycle, and collision/proxy discontinuity.

> [!question]- Self-check · Answer
> **Why may a smoother velocity trace make a virtual wall less stable?** Smoothing attenuates noise but adds phase lag. Delayed damping can act after the motion has reversed and inject rather than remove energy at the relevant frequency.

## 한국어

### 1. 햅틱 렌더링은 hard real-time feedback loop다

Impedance display는 관절 위치 측정 → 순기구학 → 충돌 검출 → proxy/surface point → 힘 계산 → $J^\top$ 매핑 → 액추에이터 명령을 반복한다. 그래픽은 수십 Hz여도 되지만 단단한 접촉은 흔히 1 kHz 안팎 이상의 servo를 요구한다. 평균 주파수보다 최악 실행시간과 jitter가 중요하다.

위의 piecewise 식은 가장 단순한 가상 벽이다. 그러나 edge 근처에서 가장 가까운 표면점이 다른 면으로 뛰면 사용자를 옆으로 밀 수 있다. 따라서 접촉 렌더링에는 충돌 검출뿐 아니라 상태를 기억하는 proxy가 필요하다.

### 2. 디지털 스프링의 에너지 누출

주기 $T$ 동안 속도 $v$로 $\Delta x=vT$만큼 움직일 때 zero-order hold의 지연이 만드는 에너지를 대략 $E_{\text{leak}}=K(vT)^2/2$로, 물리 댐핑의 소산을 $E_{\text{diss}}=bv^2T$로 볼 수 있다. 둘을 비교하면 $K\le2b/T$가 나온다. 예를 들어 $b=0.1$ N·s/m, $T=1$ ms이면 단순 모델의 상한은 200 N/m다. 이것은 보편적인 장치 정격이 아니라 특정 가정 아래의 직관적 경계다.

### 3. 샘플링과 양자화

샘플링은 update 사이에 접촉한 **시간**을 모르고, quantization은 encoder interval $\Delta$ 안의 **위치**를 모른다. 단순 Coulomb friction 모델에서는 $K\le2f_c/\Delta$ 같은 별도 경계가 나온다. 더 빠른 sampling이 encoder resolution을 높이지는 않는다.

$\hat v_k=(x_k-x_{k-1})/T$는 한 count의 변화를 작은 $T$로 나누므로 velocity spike를 만든다. 여러 샘플 averaging은 variance를 줄이지만 delay를 늘린다. 필터는 noise attenuation과 접촉 주파수에서의 phase를 함께 평가한다.

### 4. 수동성과 Z-width

포트 안으로 들어오는 power를 양수로 정하면 위 적분이 음수가 되지 않는 것이 passivity다. 수동 시스템 연결은 강한 안정성 성질을 주지만, 좋은 촉감·과제 성공·안전까지 보장하지 않는다. Z-width는 자유공간의 작은 임피던스부터 단단한 접촉까지 안정적으로 표현할 수 있는 범위이며, 주파수·load·grip·측정 위치를 함께 밝혀야 한다.

### 5. 안정화 방법

Virtual coupling은 장치와 환경 사이에 spring–damper를 넣어 안정성을 분리하지만 항상 촉감을 부드럽게 만든다. PO/PC는 에너지 예산이 깨질 때만 damping을 넣지만 zero velocity, saturation, 축적 에너지 문제를 처리해야 한다. 하드웨어에서는 빠른 주기·높은 resolution·낮은 관성·물리/전기 damping을, 지각 설계에서는 contact transient를 이용할 수 있다.

### 6. 디버깅 순서

접촉력을 끈 채 단위·부호·프레임·encoder 방향·전류 한계를 먼저 확인하고, 실제 loop period와 worst-case jitter를 기록한다. 낮은 강성부터 penetration·force·energy를 보고, velocity filter의 phase까지 확인하며 강성을 점진적으로 높인다. 수치 불안정, 구조 공진, 마찰 limit cycle, collision/proxy 불연속을 구분한다.

> [!question]- 스스로 점검 · 정답
> **더 매끄러운 속도 신호가 가상 벽을 더 불안정하게 만들 수 있는 이유는?** 필터가 noise를 줄이는 대신 phase lag를 만든다. 늦은 damping은 운동 방향이 바뀐 뒤 작용해 해당 주파수에서 에너지를 제거하지 않고 넣을 수 있다.

