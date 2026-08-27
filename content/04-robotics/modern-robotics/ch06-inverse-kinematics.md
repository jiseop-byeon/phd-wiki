---
title: "MR Ch.06 — Inverse Kinematics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.6** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the Jacobian from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]], least squares / the pseudoinverse ([[02-foundations/linear-algebra|1. Linear Algebra §2]]), and Newton's method ([[02-foundations/optimization|4. Optimization §3]]).
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 야코비안과 [[02-foundations/linear-algebra|최소제곱/유사역행렬]], [[02-foundations/optimization|뉴턴법]]을 알고 있어야 한다.

## English

**Core question**: given a desired end-effector pose, what joint angles achieve it?

### 1. IK is structurally harder than FK

Unlike FK, IK has **zero, one, several, or infinitely many** solutions (elbow-up vs
elbow-down; a 7-dof arm has a continuum). This multimodality is exactly why
[[01-canonical-papers/notes/4-vla/diffusion-policy|generative policies]] beat regression
on action prediction — IK is the classical face of the same problem. **Analytic IK**
(closed-form, e.g. 6R with spherical wrist) enumerates all branches exactly; when geometry
doesn't permit it, go numerical.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="one target reached by two joint solutions, and the average of the two overshooting it">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="40" y1="190" x2="250" y2="190"/><line x1="60" y1="200" x2="60" y2="30"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.85">
    <polyline points="60,190 160,190 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.45">
    <polyline points="60,190 60,90 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.7">
    <polyline points="60,190 131,119 201,49"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="4.5"/>
    <circle cx="160" cy="190" r="3.5" opacity="0.85"/>
    <circle cx="60" cy="90" r="3.5" opacity="0.45"/>
    <circle cx="131" cy="119" r="3" opacity="0.7"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <circle cx="160" cy="90" r="6"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.7">
    <line x1="196" y1="44" x2="206" y2="54"/>
    <line x1="196" y1="54" x2="206" y2="44"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="176" y="196">solution 1 &#183; (0&#176;, +90&#176;)</text>
    <text x="24" y="78" opacity="0.85">solution 2 &#183; (90&#176;, &#8722;90&#176;)</text>
    <text x="214" y="46" opacity="0.85">lands at (1.41, 1.41)</text>
    <text x="176" y="94">target (1, 1)</text>
    <text x="286" y="140" opacity="0.85">average &#183; (45&#176;, 0&#176;)</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5" fill="none">
    <line x1="283" y1="136" x2="140" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">Two joint pairs put the tip on the same target &#8212; that is what &#8220;several solutions&#8221; means.</text>
    <text x="24" y="226">Average them and the arm straightens to (1.41, 1.41), missing by 0.59. The mean of two</text>
    <text x="24" y="240">valid answers is not an answer, which is the classical face of why generative policies</text>
    <text x="24" y="254">beat regression on multimodal action prediction.</text>
  </g>
</svg>

### 2. Numerical IK = Newton-Raphson on the pose error

Iterate:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(task-space error)}$$
where in the full SE(3) case $e$ is the error *twist* $\log(T_{now}^{-1} T_{goal})$
([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3]]'s log map), and $J^\dagger$
is the pseudoinverse ([[02-foundations/linear-algebra|least squares]]).

### 3. One full iteration, by hand — planar 2R arm

$L_1 = L_2 = 1$; target tip $(-1, 1)$ (true answer: $\theta^* = (90°, 90°)$, from
[[04-robotics/modern-robotics/ch04-forward-kinematics|ch.4]]'s example). Start at
$\theta^{(0)} = (45°, 90°)$.

- **FK**: tip $= (\cos 45° + \cos 135°,\; \sin 45° + \sin 135°)$ — compute:
  $(0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **Error**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **Jacobian** (ch.5 formula, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$):
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **Update**: $\Delta\theta = J^{-1} e = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$, so
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **Check**: FK at $\theta^{(1)}$ gives tip $\approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **the error halved in one step**, and the iterate is moving toward
  $(90°, 90°)$. A few more iterations converge; that plot of $\|e\|$ vs iteration is the
  standard sanity check for any IK implementation.

### 4. The two practical complications

- **Singularities**: near them $J^\dagger$ explodes → **damped least squares**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$ trades accuracy for stability — ridge regression in
  disguise. It is also, exactly, the **Levenberg–Marquardt** step for this residual: the
  identity $J^\top(JJ^\top + \lambda I)^{-1} = (J^\top J + \lambda I)^{-1}J^\top$ makes the
  two expressions the same, so $\lambda$ is a trust parameter and damped IK is the same
  algorithm SLAM and calibration run ([[02-foundations/optimization|4. Optimization §3.5]]).
  MR writes $\lambda^2$ so that $\lambda$ carries units; the optimization page writes
  $\lambda$.
- **Redundancy** ($n > 6$): the null space of $J$ moves joints without moving the tool —
  spend it on secondary objectives (joint limits, obstacles, singularity avoidance).

**Wiki connections**: every teleop stack ([[01-canonical-papers/notes/4-vla/act|ALOHA]])
and end-effector-space VLA runs IK (or its velocity-level cousin) between policy output
and motor commands.

### Self-check

1. For the target $(-1,1)$ above, what is the *other* analytic solution besides
   $(90°, 90°)$?
2. Why does Newton IK need a *good initial guess*, and what typically supplies it in a
   control loop?
3. What goes wrong if you run the ch.5 arm's IK starting exactly at $\theta_2 = 0$?
4. Write the damped least squares update and say what $\lambda$ trades off.

> [!tip]- Answers
> 1. The elbow-down branch: $(180°, -90°)$. Check: link 1 points along $-\hat x$ to $(-1,0)$, then link 2 turns $-90°$ to point along $+\hat y$, giving tip $(-1,1)$. ✓ Two joint configurations, one task pose — that is IK's multimodality in a single example.
> 2. Newton's method converges only locally: far from a solution the linearization $J$ is a poor model and the step can diverge or land in a different branch. In a control loop the previous timestep's solution is the natural seed, since the target moves continuously — which also keeps the arm on one branch instead of flipping elbow configurations mid-motion.
> 3. $\theta_2 = 0$ is a singularity: $\det J = L_1L_2\sin\theta_2 = 0$, so $J^{-1}$ does not exist. The pseudoinverse still returns a step, but it cannot reduce error in the lost direction at all — the iteration stalls (or blows up numerically without damping).
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1}e$. Large $\lambda$ = stable near singularities but slower and biased (the step no longer solves the exact least-squares problem); small $\lambda$ = accurate away from singularities but explosive near them. It is ridge regression, and $\lambda$ is the ridge.

## 한국어

**핵심 질문**: 원하는 말단 자세가 주어지면 어떤 관절 각이 그것을 달성하는가?

### 1. IK는 구조적으로 FK보다 어렵다

FK와 달리 IK의 해는 **0개, 1개, 여러 개, 무한히 많을 수** 있다(팔꿈치 위/아래; 7자유도
팔은 연속체). 이 다봉성이 정확히
[[01-canonical-papers/notes/4-vla/diffusion-policy|생성형 정책]]이 행동 예측에서 회귀를
이기는 이유다 — IK는 같은 문제의 고전적 얼굴이다. **해석적 IK**(닫힌 형태, 예: 구면
손목의 6R)는 모든 가지를 정확히 열거한다; 기하가 허락하지 않으면 수치로 간다.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="같은 목표에 도달하는 두 관절 해와, 그 평균이 목표를 지나쳐 버리는 것">
  <g stroke="currentColor" stroke-width="1" opacity="0.25">
    <line x1="40" y1="190" x2="250" y2="190"/><line x1="60" y1="200" x2="60" y2="30"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.85">
    <polyline points="60,190 160,190 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.45">
    <polyline points="60,190 60,90 160,90"/>
  </g>
  <g stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-dasharray="6 4" opacity="0.7">
    <polyline points="60,190 131,119 201,49"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="4.5"/>
    <circle cx="160" cy="190" r="3.5" opacity="0.85"/>
    <circle cx="60" cy="90" r="3.5" opacity="0.45"/>
    <circle cx="131" cy="119" r="3" opacity="0.7"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.8">
    <circle cx="160" cy="90" r="6"/>
  </g>
  <g fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.7">
    <line x1="196" y1="44" x2="206" y2="54"/>
    <line x1="196" y1="54" x2="206" y2="44"/>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="176" y="196">해 1 &#183; (0&#176;, +90&#176;)</text>
    <text x="24" y="78" opacity="0.85">해 2 &#183; (90&#176;, &#8722;90&#176;)</text>
    <text x="214" y="46" opacity="0.85">(1.41, 1.41)에 도착</text>
    <text x="176" y="94">목표 (1, 1)</text>
    <text x="286" y="140" opacity="0.85">두 해의 평균 &#183; (45&#176;, 0&#176;)</text>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.5" fill="none">
    <line x1="283" y1="136" x2="140" y2="112"/>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="212">관절 각 두 쌍이 끝점을 같은 목표에 놓는다 &#8212; &#8220;해가 여러 개&#8221;라는 말의 뜻이 이것이다.</text>
    <text x="24" y="226">평균을 내면 팔이 펴져 (1.41, 1.41)에 가고 0.59만큼 빗나간다. 유효한 두 답의 평균은</text>
    <text x="24" y="240">답이 아니며, 다봉적 행동 예측에서 생성형 정책이 회귀를 이기는 이유의</text>
    <text x="24" y="254">고전적 얼굴이 바로 이것이다.</text>
  </g>
</svg>

### 2. 수치 IK = 자세 오차에 대한 뉴턴-랩슨

반복:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(작업 공간 오차)}$$
완전한 SE(3)의 경우 $e$는 오차 *twist* $\log(T_{now}^{-1} T_{goal})$
([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]]의 로그 사상)이고,
$J^\dagger$는 유사역행렬([[02-foundations/linear-algebra|최소제곱]])이다.

### 3. 한 반복을 손으로 끝까지 — 평면 2R 팔

$L_1 = L_2 = 1$; 목표 끝점 $(-1, 1)$ (참값: $\theta^* = (90°, 90°)$ —
[[04-robotics/modern-robotics/ch04-forward-kinematics|4장]] 예제에서). 초기값
$\theta^{(0)} = (45°, 90°)$에서 시작.

- **FK**: 끝점 $= (0.707 - 0.707,\; 0.707 + 0.707) = (0,\, 1.414)$.
- **오차**: $e = (-1, 1) - (0, 1.414) = (-1, -0.414)$; $\|e\| = 1.08$.
- **야코비안** (5장 공식, $s_1 = c_1 = 0.707$, $s_{12} = 0.707$, $c_{12} = -0.707$):
  $$J = \begin{pmatrix} -1.414 & -0.707 \\ 0 & -0.707 \end{pmatrix}, \quad \det J = 1.0$$
- **갱신**: $\Delta\theta = J^{-1} e = (0.41,\; 0.59)$ rad $= (23.7°,\; 33.6°)$, 따라서
  $\theta^{(1)} = (68.7°,\; 123.6°)$.
- **확인**: $\theta^{(1)}$에서 FK 끝점 $\approx (-0.61,\, 0.72)$;
  $\|e\| = 0.48$ — **한 스텝에 오차가 절반**이 됐고, 반복점은 $(90°, 90°)$ 쪽으로
  움직이고 있다. 몇 번 더 반복하면 수렴한다; 반복 대비 $\|e\|$ 그래프가 모든 IK 구현의
  표준 검산이다.

### 4. 실전의 두 가지 복잡성

- **특이점**: 근처에서 $J^\dagger$가 폭발 → **감쇠 최소제곱**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$이 정확도를 안정성과 맞바꾼다 — 변장한 릿지 회귀.
  그리고 정확히 이 잔차에 대한 **Levenberg–Marquardt** 스텝이기도 하다. 항등식
  $J^\top(JJ^\top + \lambda I)^{-1} = (J^\top J + \lambda I)^{-1}J^\top$가 두 식을 같게
  만들므로 $\lambda$는 신뢰 파라미터이고, 감쇠 IK는 SLAM과 보정이 돌리는 바로 그 알고리즘이다
  ([[02-foundations/optimization|4. 최적화 §3.5]]). MR은 $\lambda$가 단위를 갖도록
  $\lambda^2$로 쓰고, 최적화 페이지는 $\lambda$로 쓴다.
- **여유자유도** ($n > 6$): $J$의 영공간은 도구를 움직이지 않고 관절만 움직인다 — 이를
  2차 목표(관절 한계, 장애물, 특이점 회피)에 쓴다.

**위키 연결**: 모든 원격조작 스택([[01-canonical-papers/notes/4-vla/act|ALOHA]])과 말단
공간 VLA가 정책 출력과 모터 명령 사이에서 IK(또는 그 속도 수준 사촌)를 돌린다.

### 스스로 점검

1. 위의 목표 $(-1,1)$에 대해 $(90°, 90°)$ 말고 *다른* 해석해는 무엇인가?
2. 뉴턴 IK에 *좋은 초기값*이 필요한 이유는, 그리고 제어 루프에서는 보통 무엇이 그것을
   제공하는가?
3. $\theta_2 = 0$에서 정확히 시작해 IK를 돌리면 무엇이 잘못되는가?
4. 감쇠 최소제곱 갱신식을 쓰고, $\lambda$가 무엇을 맞바꾸는지 말하라.

> [!tip]- 정답 · Answers
> 1. $(180°, -90°)$ — elbow-down 가지.
> 2. 뉴턴법은 국소 수렴; 제어 루프에서는 직전 시점의 해가 초기값이 된다.
> 3. 특이점이라 $\det J = 0$ — 역행렬이 없고, 한 방향의 오차를 줄일 수 없다.
> 4. $\Delta\theta = J^\top(JJ^\top + \lambda^2 I)^{-1} e$; 큰 $\lambda$ = 안정·느림·편향, 작은 $\lambda$ = 정확·특이점 근처 폭주.
