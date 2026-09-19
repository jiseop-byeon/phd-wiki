---
title: 0.65 Lab Kernel
tags: [foundations, lab]
study-depth: Working
depth-goal: "Step a first- or second-order plant with a named integrator, plot the signals the problem asks for, and say how the integrator itself can inject energy."
mastery-when: "The kernel is a fixture; raise only if a new integrator is the contribution."
wiki-support: Working
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §1]] (derivatives) · [[02-foundations/lab-plants|0.6 Lab Plants]]
> [[02-foundations/engineering-math|0.5 §1]](미분) · [[02-foundations/lab-plants|0.6 Lab Plants]]

## English

Every Tier A lab on this wiki steps a continuous plant in an explicit loop. The integrator is part of the claim: a virtual wall that is passive in continuous time can still inject energy once it is sampled ([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). Name the method. Do not call `odeint` and hide the step.

### 1. Time vector

```python
t0, t1, T = 0.0, 4.0, 1e-3          # seconds
n = int(round((t1 - t0) / T)) + 1
t = [t0 + i * T for i in range(n)]
```

$T$ is the *sample period of the controller*, not a plotting convenience. Haptic walls use $T=10^{-3}$ or smaller. Heaters and carts may use $T=10^{-2}$. If a plot is noisy because $T$ is large, that is data, not a bug.

### 2. Explicit Euler

State $x$, input $u$, $\dot x = f(x,u)$:

$$x_{k+1}=x_k+T\,f(x_k,u_k)$$

Second-order plants store position and velocity. For a unit-mass handle,

$$v_{k+1}=v_k+T\,a_k,\qquad x_{k+1}=x_k+T\,v_k$$

with $a_k=F_k/m$ using forces at step $k$. This is what the P3 template uses. It is first-order accurate and can go unstable on a stiff spring even when the physical damping would have saved a better integrator.

### 3. Semi-implicit Euler (symplectic)

$$v_{k+1}=v_k+T\,a_k,\qquad x_{k+1}=x_k+T\,v_{k+1}$$

Position is updated with the *new* velocity. For a conservative spring it nearly conserves energy; explicit Euler steadily gains it. If a lab asks you to compare the two on P3 with $b=0$ and a soft spring, this is the pair.

### 4. Plotting convention

- One figure, labelled axes, SI units, a legend.
- If a wall exists, draw it as a dashed horizontal or vertical line.
- Report $T$, the integrator, and the plant id in the caption: `P3, explicit Euler, T=1e-3`.
- Do not smooth. If the trace chatters, that is the result.

### 5. Blank-and-solve pattern

Labs ship a template with `?` where a number or a law belongs. Fill the blanks; do not rewrite the loop. The collapsed solution on the same page is the reference, not a starting file.

Worked stepping of P4 (heater, $d=0$, $u=1$, $x_0=0$, $T=0.1$, explicit Euler):

$$x_1=0+0.1(-0+1)=0.10,\quad x_2=0.10+0.1(-0.10+1)=0.19$$

Continuous solution $x(t)=1-e^{-t}$ is $0.095$ then $0.181$ at the same instants — Euler is high by a few percent, which is expected.

## 한국어

이 위키의 Tier A 랩은 연속 플랜트를 명시적 루프로 전진한다. 적분기는 주장의 일부다: 연속 시간에는 수동인 가상 벽도 샘플되면 에너지를 넣을 수 있다([[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]). 방법을 이름 붙여라. `odeint`로 스텝을 숨기지 마라.

### 1. 시간 벡터

```python
t0, t1, T = 0.0, 4.0, 1e-3          # seconds
n = int(round((t1 - t0) / T)) + 1
t = [t0 + i * T for i in range(n)]
```

$T$는 *제어기의 샘플 주기*이지 플롯 편의 상수가 아니다. 햅틱 벽은 $T=10^{-3}$ 이하, 히터와 카트는 $T=10^{-2}$도 된다. $T$가 커서 플롯이 거친 것은 데이터가 그렇게 말한 것이지 버그가 아니다.

### 2. 명시적 오일러

상태 $x$, 입력 $u$, $\dot x = f(x,u)$:

$$x_{k+1}=x_k+T\,f(x_k,u_k)$$

2차 플랜트는 위치와 속도를 저장한다. 단위 질량 핸들이면

$$v_{k+1}=v_k+T\,a_k,\qquad x_{k+1}=x_k+T\,v_k$$

$a_k=F_k/m$은 스텝 $k$의 힘. P3 템플릿이 이것이다. 1차 정확하고, 물리적 댐핑이 더 나은 적분기를 구했을 강성 스프링에서도 불안정해질 수 있다.

### 3. 반음 오일러 (심플렉틱)

$$v_{k+1}=v_k+T\,a_k,\qquad x_{k+1}=x_k+T\,v_{k+1}$$

위치는 *새* 속도로 갱신한다. 보존 스프링에서 에너지를 거의 보존하고, 명시적 오일러는 꾸준히 얻는다. P3에서 $b=0$과 부드러운 스프링으로 둘을 비교하라고 하면 이 쌍이다.

### 4. 플롯 규약

- 그림 하나, 축 라벨, SI 단위, 범례.
- 벽이 있으면 점선.
- 캡션에 $T$, 적분기, 장치 id: `P3, explicit Euler, T=1e-3`.
- 부드럽게 하지 마라. 떨리면 그것이 결과다.

### 5. 빈칸을 채우는 패턴

랩은 숫자나 법칙이 들어갈 자리에 `?`가 있는 템플릿을 준다. 빈칸을 채워라. 루프를 다시 쓰지 마라. 같은 페이지의 접힌 해가 기준이지 시작 파일이 아니다.

P4 한 스텝 예($d=0$, $u=1$, $x_0=0$, $T=0.1$, 명시적 오일러):

$$x_1=0+0.1(-0+1)=0.10,\quad x_2=0.10+0.1(-0.10+1)=0.19$$

연속해 $x(t)=1-e^{-t}$는 같은 시각에 $0.095$, $0.181$ — 오일러가 몇 퍼센트 높다. 예상된 오차다.
