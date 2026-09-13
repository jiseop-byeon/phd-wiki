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

The integrator you simulate this with is part of the claim. Explicit Euler advances position with the *old* velocity, $v_{k+1}=v_k+Ta_k$ and $x_{k+1}=x_k+Tv_k$; semi-implicit Euler uses the *new* velocity in the position step. The two behave differently at the same step size, and a wall that looks stable under one can leak energy under the other. When a paper reports a stability limit from simulation, the integrator and step size are part of the result.

### 3. Sampling and quantization are different

Sampling hides **when** contact occurred between updates. Quantization hides **where** the device lies within an encoder interval $\Delta$. Under a Coulomb-plus-viscous friction model with quantization, passivity requires both bounds at once, $K\le\min(2b/T,\,2f_c/\Delta)$ (Abbott & Okamura 2005), and whichever is smaller limits the wall; the second one is $K\le2f_c/\Delta$, where $f_c$ is the device's Coulomb friction force in newtons — read the units and the shape of the bound follows: N divided by m is a stiffness, so the coarser the encoder the lower the wall you can render, and friction *raises* that second ceiling rather than lowering it (it helps only when the quantization term is the binding one). That is the uncomfortable part. The same friction that buys stability is the friction a transparency claim has to subtract, so a device reporting a high stable stiffness and high transparency owes you the friction number. Note also what this bound does not share with $K\le2b/T$ above: no $T$ appears in it. Faster sampling does not improve encoder resolution. Conversely, finer resolution does not eliminate zero-order-hold delay.

Velocity estimation exposes the tradeoff:

$$\hat v_k=\frac{x_k-x_{k-1}}{T}.$$

Small $T$ increases the velocity jump caused by one encoder count. Averaging over $n$ samples, $(x_k-x_{k-n})/(nT)$, reduces variance but increases effective delay. A low-pass filter should therefore be evaluated by both noise attenuation and phase at the contact frequencies.

The failure is worst where it is least expected. Move slowly enough and a fixed window may contain **no** encoder transition at all, so the estimate reads exactly zero and the rendered damping vanishes at the moment a wall is being approached gently. The alternative is to invert the measurement — time the interval between successive encoder ticks instead of counting ticks in a fixed interval — which is accurate at low speed for the same reason, and degrades at high speed where the ticks arrive faster than the timer resolves. Neither estimator is good everywhere, so a paper that reports a stiffness ceiling owes you the velocity estimator and the speed at which it was measured.

Colonnese and Okamura put all of this into one model — device and human dynamics, sampling, position quantization, delay, and the velocity filter together — and derive the tradeoffs between the resulting stability and quantization-error regions, including necessary conditions for avoiding limit cycles and sufficient conditions for quantization-error passivity. Read it as the reference treatment for this section; it is in the reading list in [[04-robotics/haptics-teleoperation/experiments-readings|Experiments & Readings]].

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

Impedance display는 관절 위치 측정 → 순기구학 → 충돌 검출 → proxy/표면점 결정 → 힘 계산 → $J^\top$ 매핑 → 액추에이터 명령을 반복한다. 그래픽은 수십 Hz로 갱신해도 되지만, 단단한 접촉은 보통 1 kHz 안팎 이상의 햅틱 servo를 요구한다. 중요한 성질은 평균 주기가 아니라 유계인 실행시간과 jitter다.

점 침투 방식의 가상 벽은 흔히 다음과 같이 쓴다.

$$F_k=\begin{cases}-Kx_k-B\hat v_k,&x_k>0\\0,&x_k\le 0,\end{cases}$$

여기서 양의 $x$는 침투를 뜻한다. 기하학적으로 가장 가까운 점이 항상 옳은 proxy는 아니다. 모서리 근처에서는 다른 면으로 뛰면서 사용자를 옆으로 밀어낼 수 있다. 따라서 접촉 렌더링에는 충돌 검출뿐 아니라 상태와 기억이 필요하다.

### 2. 디지털 스프링이 에너지를 만들 수 있는 이유

제어기는 위치를 샘플링하고 다음 갱신까지 힘을 유지한다. 한 주기 $T$ 동안 일정 속도 $v$는 $\Delta x=vT$만큼 움직인다. Zero-order hold 때문에 힘이 이상적인 스프링보다 늦는다. 쓸 만한 최악의 경우 에너지 추정은

$$E_{\text{leak}}\approx\frac12K(vT)^2,$$

이고, 물리적 점성 댐핑이 소산하는 에너지는

$$E_{\text{diss}}=bv^2T.$$

$E_{\text{leak}}\le E_{\text{diss}}$를 요구하면 직관적인 경계

$$K\le\frac{2b}{T}$$

를 얻는다. 후방차분 가상 댐핑 $B$를 쓸 때, 모델 가정 아래의 고전적인 1자유도 수동성 조건은 $b>KT/2+|B|$다. 이것은 보편적인 하드웨어 정격이 아니다. 마찰·지연·양자화·비선형 기구학·포화·사람의 파지·구현 세부가 경계를 바꾼다.

예제: 물리 댐핑 $b=0.1$ N·s/m, $T=1$ ms이면 단순 경계는 $K\le200$ N/m다. $T$를 절반으로 줄이면 이 경계는 두 배가 된다. 디지털 댐핑을 더하는 것은 물리적 소산을 자유롭게 대체하지 못하는데, 그 추정값 자체가 늦기 때문이다.

이것을 시뮬레이션하는 적분기도 주장의 일부다. 명시적 오일러는 *이전* 속도로 위치를 전진시키고($v_{k+1}=v_k+Ta_k$, $x_{k+1}=x_k+Tv_k$), 준음해 오일러는 위치 갱신에 *새* 속도를 쓴다. 같은 스텝 크기에서 둘의 거동이 다르고, 한쪽에서 안정해 보이는 벽이 다른 쪽에서는 에너지를 샐 수 있다. 논문이 시뮬레이션에서 얻은 안정성 한계를 보고하면 적분기와 스텝 크기가 그 결과의 일부다.

### 3. 샘플링과 양자화는 서로 다른 문제다

샘플링은 갱신 사이의 **언제** 접촉이 일어났는지를 가린다. 양자화는 장치가 encoder 간격 $\Delta$ 안의 **어디**에 있는지를 가린다. Coulomb에 점성 마찰을 더하고 양자화를 넣은 모델에서는 수동성이 두 경계를 동시에 요구한다: $K\le\min(2b/T,\,2f_c/\Delta)$(Abbott & Okamura 2005)이고, 더 작은 쪽이 벽을 제한한다. 둘째 경계가 $K\le2f_c/\Delta$다. 여기서 $f_c$는 장치의 Coulomb 마찰력이고 단위는 N이다. 단위를 읽으면 경계의 모양이 따라 나온다 — N을 m으로 나누면 강성이므로, encoder가 거칠수록 렌더링할 수 있는 벽은 낮아지고, 마찰은 그 둘째 천장을 낮추는 것이 아니라 *올린다*(양자화 항이 더 작은 쪽일 때만 도움이 된다). 불편한 지점이 여기다. 안정성을 사 주는 그 마찰이 곧 투명도 주장에서 빼야 할 마찰이다. 높은 안정 강성과 높은 투명도를 동시에 보고하는 장치라면 마찰 수치를 함께 내놓아야 한다. 위의 $K\le2b/T$와 다른 점도 보라. 이 경계에는 $T$가 등장하지 않는다. 더 빠른 샘플링이 encoder 해상도를 높여 주지는 않는다. 반대로, 더 고운 해상도가 zero-order hold 지연을 없애 주지도 않는다.

속도 추정에서 이 상충이 드러난다.

$$\hat v_k=\frac{x_k-x_{k-1}}{T}.$$

$T$가 작을수록 encoder 한 count가 만드는 속도 도약이 커진다. $n$개 샘플에 대한 평균 $(x_k-x_{k-n})/(nT)$는 분산을 줄이지만 실효 지연을 늘린다. 따라서 저역통과 필터는 noise 감쇠와 접촉 주파수에서의 위상, 두 가지로 함께 평가해야 한다.

이 고장은 예상하기 가장 어려운 곳에서 가장 심하다. 충분히 느리게 움직이면 고정된 창 안에 encoder 전이가 **하나도** 안 들어올 수 있다. 그러면 추정값이 정확히 0이 되고, 벽에 조심스럽게 다가가는 바로 그 순간에 렌더링된 감쇠가 사라진다. 대안은 측정을 뒤집는 것이다. 고정 구간의 tick 수를 세는 대신 연속한 tick 사이의 시간을 재면, 같은 이유로 저속에서 정확하고, tick이 타이머 분해능보다 빨리 도착하는 고속에서 나빠진다. 어느 추정기도 전 구간에서 좋지 않다. 그러니 강성 한계를 보고하는 논문이라면 속도 추정기와 그것을 측정한 속도를 함께 내놓아야 한다.

Colonnese와 Okamura는 이것을 전부 한 모델에 넣었다 — 장치와 인간의 동역학, 샘플링, 위치 양자화, 지연, 속도 필터를 함께 놓고, 그 결과로 생기는 안정성 영역과 양자화 오차 영역 사이의 절충을 유도한다. 극한 주기를 피하기 위한 필요조건과 양자화 오차 수동성의 충분조건도 함께 다룬다. 이 절의 기준 문헌으로 읽어라. [[04-robotics/haptics-teleoperation/experiments-readings|실험과 읽을거리]]의 읽기 목록에 있다.

### 4. 수동성, 안정성, Z-width

일률을 1-포트로 들어가는 방향을 양으로 정의하면 수동성은 다음을 요구한다.

$$E(t)=E_0+\int_0^t F(\tau)^\top v(\tau)d\tau\ge0.$$

수동 시스템을 연결하면 강한 안정성 성질이 생기고, 덕분에 사람의 정확한 고주파 모델이 필요 없어진다. 그러나 수동성은 충분조건을 주는 설계 틀이지 좋은 촉감·과제 성공·안전을 보장하지 않는다. 보수적일 수 있고, 능동적인 사람이나 액추에이터가 있으면 포트 정의와 가정을 여전히 조심해야 한다.

**Z-width**는 장치가 안정하게(수동적으로) 표현할 수 있는 임피던스의 범위다. 가벼운 자유공간에서 단단한 접촉까지가 여기에 들어간다. 강성–댐핑 평면의 그림은 그 일부만 보여 준다. 주파수, 최소 임피던스, 부하, 파지, 측정 위치를 함께 보고해야 한다.

### 5. 세 가지 안정화 계열

- **Virtual coupling:** 장치 proxy와 시뮬레이션된 도구 사이에 가상 스프링–댐퍼를 넣는다. 수동적인 환경을 분리해 주지만 투명성을 상시로 무디게 만든다.
- **Passivity observer/controller (PO/PC):** 이산 일률/에너지를 추적하다가 에너지 예산이 깨질 때만 댐핑을 넣는다. 적응적이지만 burst, 속도가 0에 가까울 때의 나눗셈 문제, 포화, 축적된 "에너지 credit" 뒤의 늦은 개입을 만들 수 있다.
- **하드웨어·지각 설계:** 샘플링 주파수와 센서 해상도를 높이고, 물리적/전기적 고주파 댐핑을 더하고, 관성을 줄이거나, 충돌 시점에 event-triggered 진동을 더해 적당한 안정 강성이 더 단단하게 느껴지게 한다.

이산 샘플에서 흔히 쓰는 observer는 부호 규약을 명시한 뒤 $\Delta E_k=T F_k^\top v_k$를 쓴다. 누적 예산이 음수가 되면, impedance 인과성의 제어기는 부족분을 상쇄하도록 고른 $d_k$로 $F_{pc}=-d_kv_k$를 더할 수 있다. $\|v_k\|=0$ 근처에서는 이 법칙을 clamp하고 정규화해야 한다. 액추에이터 한계를 빼고 이 식을 해석해서는 안 된다.

### 6. 디버깅 순서

1. 접촉력을 끄고 단위·부호·프레임·encoder 방향·모터 전류 한계를 확인한다.
2. 요청한 주기가 아니라 실제 loop period와 최악의 jitter를 기록한다.
3. 댐핑 없이 낮은 강성의 벽을 넣고 침투량·힘·에너지를 관찰한다.
4. 속도 추정과 댐핑을 더하면서 위상과 noise를 함께 그린다.
5. 강성을 점진적으로 올리고, 지속 진동·포화·과열·위험한 힘에서 멈춘다.
6. 수치 불안정, 기계 공진, 마찰 limit cycle, 충돌/proxy 불연속을 구분한다.

> [!question]- 스스로 점검 · 정답
> **더 매끄러운 속도 신호가 가상 벽을 더 불안정하게 만들 수 있는 이유는?** 필터가 noise를 줄이는 대신 phase lag를 만든다. 늦은 damping은 운동 방향이 바뀐 뒤 작용해 해당 주파수에서 에너지를 제거하지 않고 넣을 수 있다.
