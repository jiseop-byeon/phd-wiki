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
elbow-down; a 7-dof arm has a continuum). This multimodality is a useful analogy for why
[[01-canonical-papers/notes/4-vla/diffusion-policy|generative policies]] represent alternative actions: averaging distinct valid solutions may give an invalid one. It does not establish that a particular learned policy performs better. **Analytic IK**
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

**A pose target is not yet a motion plan.** Elbow-up and elbow-down solutions can reach the same tip pose through very different arm configurations. Joint limits or an obstacle can invalidate one branch without invalidating the other. A solver returning a target configuration therefore answers a narrower question than a planner finding a collision-free route to it.

A numerical solver usually follows the branch near its initial guess. If it stops without success, distinguish an unreachable target from a poor initialization, a singular local map, a violated limit, or an iteration budget that expired. One unsuccessful local search does not prove that the robot has no solution.

**Check your understanding.** For successive nearby targets, the previous solution is often a useful starting point because it encourages continuity. It does not guarantee continuity through singularities or changes of feasible branch. The analogy to multimodal learned actions is about representing alternatives; it is not a theorem that every generative policy outperforms regression.

### 2. Numerical IK = Newton-Raphson on the pose error

Iterate:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(task-space error)}$$
where in the full SE(3) case $e$ is the six-vector error $[\log(T_{now}^{-1} T_{goal})]^\vee$ in body coordinates, paired with the body Jacobian
([[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3]]'s log map), and $J^\dagger$
is the pseudoinverse ([[02-foundations/linear-algebra|least squares]]).

**Follow one iteration.** Compute the current pose, express the goal error in a chosen frame, and evaluate the matching Jacobian at the current joints. Solve the local relation JΔθ ≈ e, update the joint guess, then recompute both pose and error. Repeating is necessary because the Jacobian describes only local change. A damping or step-size rule can keep the update from trusting that approximation too far.

For the body-frame pose error written above, the matrix logarithm is first a matrix in the Lie algebra; its six coordinates form the error vector. Pair those coordinates with the body Jacobian. Use separate rotation and translation stopping tolerances because radians and length are different units. Also enforce joint limits and check collision separately from numerical convergence.

**Check your understanding.** The pseudoinverse minimizes the local linear residual and selects a minimum-norm update when alternatives remain. It does not directly solve the entire nonlinear pose problem. See the [official numerical IK walkthrough](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/) for the local approximation and update loop.

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
팔은 연속체). 이 다봉성은
[[01-canonical-papers/notes/4-vla/diffusion-policy|생성형 정책]]이 대안 행동을 표현하는 이유에 대한 비유다. 서로 다른 유효 해를 평균하면 무효 해가 될 수 있다. 특정 학습 정책의 성능 우위를 증명하는 것은 아니다. **해석적 IK**(닫힌 형태, 예: 구면
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

**목표 자세는 아직 운동 계획이 아니다.** 팔꿈치가 위·아래인 해는 말단 자세가 같아도 팔 구성은 크게 다를 수 있다. 관절 한계나 장애물 때문에 한 분기만 불가능할 수 있다. 목표 구성을 반환하는 해법과 그곳까지 충돌 없는 경로를 찾는 계획기는 다른 질문에 답한다.

수치 해법은 대개 초기 추정 근처의 분기를 따라간다. 성공하지 못하면 도달 불가, 나쁜 초기값, 특이한 국소 사상, 한계 위반, 반복 예산 소진을 나눈다. 국소 탐색 한 번의 실패가 로봇에 해가 없다는 증거는 아니다.

**이해 확인.** 가까운 목표를 연속으로 풀 때 이전 해는 연속성을 유도하는 좋은 초기값일 수 있다. 특이점이나 가능 분기 변경을 지나도 연속성을 보장하지는 않는다. 다중모드 학습 행동과의 비유는 대안을 표현하는 문제다. 모든 생성 정책이 회귀보다 낫다는 정리가 아니다.

### 2. 수치 IK = 자세 오차에 대한 뉴턴-랩슨

반복:
$$\Delta\theta = J^\dagger(\theta)\; e, \qquad e = \text{(작업 공간 오차)}$$
완전한 SE(3)의 경우 $e$는 바디 좌표의 6차원 오차 $[\log(T_{now}^{-1} T_{goal})]^\vee$이며 바디 자코비안과 짝지어 쓴다
([[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]]의 로그 사상)이고,
$J^\dagger$는 유사역행렬([[02-foundations/linear-algebra|최소제곱]])이다.

**반복 한 번을 따라간다.** 현재 자세를 계산하고 목표 오차를 정한 프레임으로 표현한다. 현재 관절에서 그 프레임의 야코비안을 구한다. 국소 관계 JΔθ ≈ e를 풀고 관절 추정을 갱신한 뒤 자세와 오차를 다시 계산한다. 야코비안이 국소 변화만 설명하므로 반복이 필요하다. 감쇠나 보폭 규칙은 근사를 너무 멀리 믿지 않게 한다.

위 바디 프레임 자세 오차에서 행렬 로그의 결과는 먼저 리 대수의 행렬이다. 그 여섯 좌표를 오차 벡터로 뽑아 바디 야코비안과 짝짓는다. 라디안과 길이는 단위가 달라 회전·병진 정지 허용오차를 따로 쓴다. 수치 수렴과 별개로 관절 한계와 충돌도 검사한다.

**이해 확인.** 유사역행렬은 국소 선형 잔차를 최소화하고 대안이 남으면 최소 노름 갱신을 고른다. 전체 비선형 자세 문제를 곧바로 푸는 것은 아니다. 국소 근사와 갱신 루프는 [공식 수치 IK 설명](https://modernrobotics.northwestern.edu/nu-gm-book-resource/6-2-numerical-inverse-kinematics-part-1-of-2/)에서도 따라갈 수 있다.

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
