---
title: 24.3 Haptic Device Design & Kinematics
tags: [haptics, mechatronics, kinematics]
study-depth: Working
wiki-support: Working
depth-goal: "Trace a command from Cartesian force to joint torque and motor current, and identify the hardware limitation that breaks the ideal mapping."
mastery-when: "Master mechanism optimization and device identification when new hardware is the contribution."
---

## English

### 1. Impedance and admittance causality

An **impedance display** measures motion and commands force: $x,\dot x\mapsto F$. It should feel light and backdrivable in free space, so low inertia, friction, cogging, backlash, and cable drag matter. An **admittance display** measures force and commands motion: $F\mapsto x,\dot x$. It relies on a high-bandwidth motion servo and is often built on a non-backdrivable industrial mechanism. These are interface causalities, not synonyms for impedance or admittance control used around an arbitrary robot.

Only one member of an effort–flow pair can be independently imposed at a port. In mechanics the pair is force and velocity, and instantaneous power is $P=F^\top v$. This energy view will reappear in passivity and bilateral teleoperation.

### 2. The device chain and the Jacobian

```mermaid
flowchart LR
    C["encoder counts"] --> Q["joint angles q"] --> X["pose x=f(q)"] --> VE["virtual/remote<br/>environment"] --> F["Cartesian force F"] --> T["joint torque τ"] --> I["motor current i"]
```

The kinematic differential is $v=J(q)\dot q$. Equality of mechanical power gives

$$\tau^\top\dot q=F^\top v=F^\top J\dot q\quad\Rightarrow\quad \tau=J^\top F.$$

This mapping does not require $J^{-1}$ and remains valid for non-square Jacobians. Near a singularity, however, some Cartesian velocities need very large joint rates or become unavailable, and a force along the singular direction is carried by the structure with little joint torque, so it cannot be actively modulated. Use singular values and condition number across the usable workspace, not only $\det J$ at one pose.

Worked example: for $J=\begin{bmatrix}0.2&0.1\\0&0.15\end{bmatrix}$ m/rad and $F=[5,-2]^\top$ N,

$$\tau=J^\top F=\begin{bmatrix}0.2&0\\0.1&0.15\end{bmatrix}\begin{bmatrix}5\\-2\end{bmatrix}=\begin{bmatrix}1.0\\0.2\end{bmatrix}\ \mathrm{N\,m}.$$

The computation only means anything if the units and the coordinate frames line up on both
sides.

### 3. Actuation is not “PWM equals force”

For a brushed DC motor,

$$\tau_m=k_t i,\qquad V=Ri+L\dot i+k_e\omega.$$

Current is the direct torque variable. PWM duty cycle approximately controls average terminal voltage; current still depends on resistance, inductance, back-EMF, switching, and load. Stall torque is a short-duration operating point, not a continuous-force rating. Thermal limits, saturation, torque ripple, and amplifier current/voltage limits must be included in the force envelope.

A transmission multiplies torque and reflected inertia approximately by $N$ and $N^2$, respectively. Gears can add backlash and friction; capstan drives can be low-backlash but require tension, alignment, and no-slip contact. High torque ratio can make a device strong yet heavy-feeling—bad for free-space transparency.

### 4. Sensing and differentiation

Quadrature encoders provide counts and direction; angle requires counts-per-revolution and transmission calibration. Velocity from $(q_k-q_{k-1})/T$ amplifies quantization and noise. Filtering reduces noise but adds phase lag, which can destabilize a haptic loop. Force sensors add direct interaction information but require bias, temperature, frame, bandwidth, and inertial-load checks.

### 5. Design from two ends

From the person: workspace, grasp, comfortable continuous/peak force, perceptual bandwidth, and safety. From the virtual task: minimum free-space impedance, maximum stable wall stiffness, directions of force, update rate, collision complexity, and desired cue. A useful design maximizes the intersection; no scalar “best haptic device” captures it.

> [!question]- Self-check · Answer
> **Why can increasing a gear ratio worsen a haptic interface even when maximum force rises?** Reflected motor inertia grows approximately with the square of ratio, and friction/backlash may grow. The device becomes harder to backdrive and corrupts free-space motion and small forces.

## 한국어

### 1. 임피던스·어드미턴스 인과성

**Impedance display**는 운동을 측정해 힘을 명령한다: $x,\dot x\mapsto F$. 자유공간에서 가볍고 backdrivable해야 하므로 관성·마찰·cogging·backlash·케이블 항력이 중요하다. **Admittance display**는 힘을 측정해 운동을 명령한다: $F\mapsto x,\dot x$. 고대역폭 motion servo에 의존하며 역구동이 되지 않는 산업용 메커니즘 위에 만드는 경우가 많다. 이것은 인터페이스의 인과성이며, 임의의 로봇에 두르는 impedance/admittance 제어기와 같은 말이 아니다.

한 포트에서 effort–flow 쌍 중 독립적으로 부과할 수 있는 것은 하나뿐이다. 역학에서 그 쌍은 힘과 속도이고 순간 일률은 $P=F^\top v$다. 이 에너지 관점은 수동성과 양방향 원격조작에서 다시 등장한다.

### 2. 장치 사슬과 야코비안

```mermaid
flowchart LR
    C["encoder counts"] --> Q["관절각 q"] --> X["자세 x=f(q)"] --> VE["가상/원격<br/>환경"] --> F["직교좌표 힘 F"] --> T["관절 토크 τ"] --> I["모터 전류 i"]
```

기구학 미분은 $v=J(q)\dot q$다. 기계적 일률이 같다는 조건에서

$$\tau^\top\dot q=F^\top v=F^\top J\dot q\quad\Rightarrow\quad \tau=J^\top F.$$

이 사상에는 $J^{-1}$가 필요하지 않고 비정방 야코비안에서도 성립한다. 다만 특이점 근처에서는 어떤 직교 속도가 매우 큰 관절 속도를 요구하거나 아예 만들 수 없고, 특이 방향의 힘은 관절 토크를 거의 쓰지 않고 구조가 받아 내므로 능동적으로 조절할 수 없다. 한 자세의 $\det J$만이 아니라 사용 가능한 작업공간 전체에서 특이값과 조건수를 본다.

예제: $J=\begin{bmatrix}0.2&0.1\\0&0.15\end{bmatrix}$ m/rad, $F=[5,-2]^\top$ N일 때

$$\tau=J^\top F=\begin{bmatrix}0.2&0\\0.1&0.15\end{bmatrix}\begin{bmatrix}5\\-2\end{bmatrix}=\begin{bmatrix}1.0\\0.2\end{bmatrix}\ \mathrm{N\,m}.$$

단위와 좌표 프레임이 함께 맞아야 이 계산이 물리적 의미를 가진다.

### 3. PWM은 곧 힘이 아니다

브러시 DC 모터에서

$$\tau_m=k_t i,\qquad V=Ri+L\dot i+k_e\omega.$$

전류가 직접적인 토크 변수다. PWM duty는 평균 단자 전압을 근사적으로 제어할 뿐이고, 전류는 여전히 저항·인덕턴스·역기전력·스위칭·부하에 달려 있다. Stall torque는 짧은 시간의 동작점이지 연속 힘 정격이 아니다. 열 한계·포화·torque ripple·증폭기의 전류/전압 한계를 힘 범위 안에 포함해야 한다.

전달장치는 토크를 대략 $N$배, 반사 관성을 대략 $N^2$배로 만든다. 기어는 backlash와 마찰을 더할 수 있고, capstan은 backlash가 작지만 장력·정렬·미끄럼 없는 접촉을 요구한다. 큰 감속비는 장치를 강하지만 무겁게 느껴지게 만들며, 이는 자유공간 투명성에 나쁘다.

### 4. 센싱과 미분

Quadrature encoder는 count와 방향을 준다. 각도를 얻으려면 회전당 count 수와 전달비 보정이 필요하다. $(q_k-q_{k-1})/T$로 얻는 속도는 quantization과 noise를 증폭한다. 필터는 noise를 줄이지만 phase lag를 더해 햅틱 루프를 불안정하게 만들 수 있다. Force sensor는 상호작용 정보를 직접 주지만 bias·온도·프레임·대역폭·관성 부하를 함께 점검해야 한다.

### 5. 양쪽에서 설계하기

사람 쪽에서: 작업공간, 파지, 편안한 지속/최대 힘, 지각 대역폭, 안전. 가상 과제 쪽에서: 자유공간 최소 임피던스, 안정하게 낼 수 있는 최대 벽 강성, 힘의 방향, 갱신 주기, 충돌 복잡도, 원하는 cue. 좋은 설계는 이 두 집합의 교집합을 최대로 만든다. "최고의 햅틱 장치"라는 하나의 스칼라 지표는 존재하지 않는다.

> [!question]- 스스로 점검 · 정답
> **감속비를 높이면 최대 힘이 커져도 왜 햅틱 인터페이스가 나빠질 수 있는가?** 반사 모터 관성이 대략 감속비의 제곱으로 커지고 마찰·backlash도 함께 커질 수 있다. 장치가 역구동하기 어려워지면서 자유공간 운동과 작은 힘의 표현이 망가진다.
