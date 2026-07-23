---
title: "MR Ch.03 — Rigid-Body Motions"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.3** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · prerequisite: [[02-foundations/se3-geometry|8. SE(3)]]

> [!note] 시작 전 점검 · Before you start
> 다음을 할 수 있어야 한다: ① 회전 행렬 곱셈과 $R^{-1} = R^\top$ ([[02-foundations/se3-geometry|SE(3) §1]]) ② 외적 $\omega \times v$ 계산 ③ $\dot x = ax \Rightarrow x = e^{at}x_0$ ([[02-foundations/engineering-math|0.5 공업수학 §8]]). 셋 중 하나라도 흔들리면 해당 페이지를 먼저 읽어라.

## English

**Core question**: how do we represent and compose rotations, poses, and velocities of rigid bodies — without singularities?

This is the longest-feeling chapter of the book, and the one worth ~30% of your total
study time: every later chapter is this machinery applied. Take it in four steps.

### 1. The skew-symmetric bridge: cross products become matrices

For $\omega = (\omega_1, \omega_2, \omega_3)$, define
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
Check one entry yourself: the first row of $[\omega]v$ is $-\omega_3 v_2 + \omega_2 v_3$ —
exactly the first component of $\omega \times v$. Why bother? Because once cross products
are matrices, *linear algebra applies to rotation dynamics* — including the matrix
exponential below.

### 2. Why an exponential? Rotation is a linear ODE

A frame spinning at constant angular velocity $\omega$ obeys $\dot R = [\omega]\,R$.
This is the matrix version of $\dot x = ax$ — so its solution is the matrix version of
$e^{at}$: rotating about unit axis $\hat\omega$ for "time" $\theta$ gives
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(Rodrigues' formula)}.$$
The infinite series collapses to three terms because $[\hat\omega]^3 = -[\hat\omega]$.

**Worked check** — rotate about $\hat z = (0,0,1)$ by $\theta = 90°$:
$[\hat z] = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&0\end{pmatrix}$,
$[\hat z]^2 = \begin{pmatrix}-1&0&0\\0&-1&0\\0&0&0\end{pmatrix}$, so
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix},$$
which is exactly $R_z(90°)$ — it sends $\hat x \to \hat y$. Every rotation is *one*
axis-angle exponential (Euler's theorem); $\log$ recovers $(\hat\omega, \theta)$ from $R$.
This exp/log pair is the door between the Lie group (rotations) and the Lie algebra
(angular velocities) — and the reason poses can be interpolated and averaged correctly.

### 3. Twists: body velocity is six numbers — but read $v$ carefully

A moving body's velocity is a **twist** $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$.
The most common misconception in the whole book: **$v$ is *not* "the velocity of the
end-effector point."** It is the velocity of *the point of the (imagined, infinitely
large) body that currently coincides with the frame origin*. That is why a body rotating
about a distant axis has a nonzero $v$ even if "its center" barely moves. Every twist is a
**screw**: rotate about an axis while translating along it; pure translation is the
zero-pitch limit.

### 4. One motion, two descriptions: space frame vs body frame

The same physical motion can be written in the fixed frame ($\mathcal{V}_s$) or the moving
body frame ($\mathcal{V}_b$). They are related by the **adjoint** of the current pose
$T = (R, p)$:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
A special case worth memorizing: if $p = 0$ (pure rotation), this is just "rotate both
halves": $\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **Frame subscripts are not decoration**
— most sign errors in later chapters are $s$/$b$ confusions, so write the subscript every
time. The pose exponential works like the rotation one:
$T = e^{[\mathcal{S}]\theta}$ means "follow screw $\mathcal{S}$ for angle $\theta$."

**Why learning people should care**: exp/log maps are how you interpolate poses, average
rotations, and define losses on SE(3) — the machinery under SE(3) diffusion/flow action
heads ([[01-canonical-papers/notes/4-vla/pi0|π0]]-style).

### Self-check

1. Verify Rodrigues for $\theta = 180°$ about $\hat z$. What matrix do you get?
2. A body rotates about an axis through the point $(0, 2, 0)$ (axis direction $\hat z$,
   speed 1 rad/s). What is its space twist $\mathcal{V}_s = (\omega_s, v_s)$?
3. Why does $[\hat\omega]^3 = -[\hat\omega]$ terminate the exponential series?
4. If $T$ is a pure translation by $p$, what does $[\text{Ad}_T]$ do to a twist?

> [!tip]- 정답 · Answers
> 1. $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1, -1, 1)$ — x·y축이 뒤집힌다.
> 2. $\omega_s = (0,0,1)$; $v_s = -\omega \times q = -(0,0,1)\times(0,2,0) = (2, 0, 0)$ — 원점과 겹친 몸체 점이 +x 방향 2 m/s.
> 3. 3×3 반대칭 행렬의 거듭제곱이 자기 자신의 배수로 되돌아오기 때문 — 무한급수의 모든 항이 $[\hat\omega]$, $[\hat\omega]^2$의 계수로 흡수된다.
> 4. $\omega$는 그대로 두고 $v \mapsto v + p \times \omega$ — 축의 위치 이동만큼 선속도가 보정된다.

## 한국어

**핵심 질문**: 강체의 회전·자세·속도를 특이점 없이 어떻게 표현하고 합성하는가?

책에서 가장 길게 느껴지는 장이고, 전체 공부 시간의 약 30%를 써도 되는 장이다 —
이후의 모든 장이 이 기계장치의 응용이기 때문이다. 네 단계로 나눠 잡아라.

### 1. 반대칭 다리: 외적이 행렬이 된다

$\omega = (\omega_1, \omega_2, \omega_3)$에 대해
$$[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}, \qquad [\omega]\,v = \omega \times v.$$
한 성분을 직접 검산하라: $[\omega]v$의 첫 행은 $-\omega_3 v_2 + \omega_2 v_3$ —
정확히 $\omega \times v$의 첫 성분이다. 왜 이렇게 하나? 외적이 행렬이 되는 순간
*회전 동역학에 선형대수가 통째로 적용*되기 때문이다 — 아래의 행렬 지수를 포함해서.

### 2. 왜 지수함수인가? 회전은 선형 미분방정식이다

일정한 각속도 $\omega$로 도는 프레임은 $\dot R = [\omega]\,R$을 따른다.
$\dot x = ax$의 행렬판이다 — 그러므로 해도 $e^{at}$의 행렬판이다: 단위축 $\hat\omega$
둘레로 "시간" $\theta$만큼 돌면
$$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2 \quad \text{(로드리게스 공식)}.$$
무한급수가 세 항으로 접히는 이유는 $[\hat\omega]^3 = -[\hat\omega]$이기 때문이다.

**검산 예제** — $\hat z = (0,0,1)$ 둘레 $\theta = 90°$ 회전:
$[\hat z]$와 $[\hat z]^2$를 대입하면
$$R = I + (1)[\hat z] + (1)[\hat z]^2 = \begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$$
— 정확히 $R_z(90°)$이고, $\hat x$를 $\hat y$로 보낸다. 모든 회전은 *하나의* 축-각
지수다(오일러 정리); $\log$가 $R$에서 $(\hat\omega, \theta)$를 복원한다. 이 exp/log 쌍이
리 군(회전)과 리 대수(각속도) 사이의 문이고 — 자세를 올바르게 보간하고 평균할 수 있는
이유다.

### 3. Twist: 강체의 속도는 여섯 숫자 — 단, $v$를 조심해서 읽어라

움직이는 강체의 속도는 **twist** $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$이다.
이 책 전체에서 가장 흔한 오해: **$v$는 "말단 점의 속도"가 아니다.** $v$는 *(무한히
크다고 상상한) 몸체에서 지금 프레임 원점과 겹쳐 있는 점*의 속도다. 그래서 멀리 있는 축
둘레로 도는 몸체는 "중심"이 거의 안 움직여도 $v$가 0이 아니다. 모든 twist는
**스크류**다: 축 둘레로 돌면서 그 축 방향으로 나아가는 운동; 순수 병진은 피치 0의
극한이다.

### 4. 하나의 운동, 두 개의 기술: space 프레임 vs body 프레임

같은 물리적 운동을 고정 프레임에서 쓰면 $\mathcal{V}_s$, 움직이는 몸체 프레임에서 쓰면
$\mathcal{V}_b$다. 둘은 현재 자세 $T = (R, p)$의 **adjoint**로 연결된다:
$$\mathcal{V}_s = [\text{Ad}_T]\,\mathcal{V}_b, \qquad [\text{Ad}_T] = \begin{pmatrix} R & 0 \\ [p]R & R\end{pmatrix}.$$
외울 가치가 있는 특수 사례: $p = 0$(순수 회전)이면 그냥 "양쪽을 회전"이다:
$\omega_s = R\,\omega_b$, $v_s = R\,v_b$. **프레임 아래 첨자는 장식이 아니다** — 이후
장들의 부호 실수 대부분이 $s$/$b$ 혼동이므로, 매번 아래 첨자를 써라. 자세의 지수도
회전과 같다: $T = e^{[\mathcal{S}]\theta}$ = "스크류 $\mathcal{S}$를 $\theta$만큼
따라가라."

**학습 쪽에서 중요한 이유**: exp/log 사상이 자세 보간, 회전 평균, SE(3) 위의 손실 정의의
방법이고 — SE(3) 디퓨전/flow 행동 헤드([[01-canonical-papers/notes/4-vla/pi0|π0]]류)의
밑바닥 기계장치다.

### 스스로 점검

1. $\hat z$ 둘레 $\theta = 180°$에 대해 로드리게스를 검산하라. 어떤 행렬이 나오는가?
2. 몸체가 점 $(0, 2, 0)$을 지나는 축($\hat z$ 방향, 1 rad/s) 둘레로 돈다.
   space twist $\mathcal{V}_s = (\omega_s, v_s)$는?
3. $[\hat\omega]^3 = -[\hat\omega]$가 지수 급수를 세 항으로 끝내는 이유는?
4. $T$가 $p$만큼의 순수 병진이면 $[\text{Ad}_T]$는 twist에 무슨 일을 하는가?

> [!tip]- 정답 · Answers
> 1. $R = I + 0 + 2[\hat z]^2 = \text{diag}(-1, -1, 1)$ — x·y축이 뒤집힌다.
> 2. $\omega_s = (0,0,1)$; $v_s = -\omega \times q = (2, 0, 0)$.
> 3. 3×3 반대칭 행렬의 거듭제곱이 자기 자신의 배수로 되돌아오기 때문 — 급수의 모든 항이 $[\hat\omega]$, $[\hat\omega]^2$의 계수로 흡수된다.
> 4. $\omega$는 그대로, $v \mapsto v + p \times \omega$.
