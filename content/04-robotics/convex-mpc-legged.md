---
title: "8. Convex MPC (Legged Robots)"
tags: [robotics, control, resource]
study-depth: Literacy
depth-goal: "Read the MPC formulation and recognize its assumptions and role in a complete robot system."
mastery-when: "Raise to Working or Mastery when legged control or MPC design is used directly."
---

**Key references** — Di Carlo et al., *Dynamic Locomotion in the MIT Cheetah 3 Through Convex Model-Predictive Control*, IROS 2018 · [IEEE](https://ieeexplore.ieee.org/document/8594448) · Kim et al., *Highly Dynamic Quadruped Locomotion via Whole-Body Impulse Control and MPC* (open access) · [arXiv](https://arxiv.org/abs/1909.06586) · [PDF](https://arxiv.org/pdf/1909.06586)

## English

*Last of group D and its worked application. Stands on [[04-robotics/mpc|7. MPC]], [[04-robotics/contact-force-tactile|9. Contact]] and the [[04-robotics/modern-robotics/index|MR chapters]].
The cleanest case study of the skill the optimization page teaches: choose the approximation that makes the problem convex.*

> [!info] Depth target · 깊이 목표
> Understand why the problem is convexified and what the simplification costs. This is a representative-application read, not a controller-design guide.
> 왜 문제를 볼록화했고 그 단순화의 대가가 무엇인지 이해하는 것이 목표다. 대표 응용 읽기이지 제어기 설계 가이드가 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/mpc|7. MPC]] (the formulation being applied) · [[02-foundations/optimization|4. Optimization §5]] (QP) · [[04-robotics/contact-force-tactile|9. Contact §2]] (the friction cone that becomes the constraint set) · [[04-robotics/modern-robotics/ch08-dynamics|MR ch.8]] (what the single-rigid-body approximation throws away) · [[02-foundations/se3-geometry|8. 3D Geometry §2]] (roll, pitch, yaw)
> [[04-robotics/mpc|7. MPC]] (적용되는 정식화) · [[02-foundations/optimization|4. 최적화 §5]] (QP) · [[04-robotics/contact-force-tactile|9. 접촉 §2]] (제약 집합이 되는 마찰 원뿔) · [[04-robotics/modern-robotics/ch08-dynamics|MR 8장]] (단일 강체 근사가 버리는 것) · [[02-foundations/se3-geometry|8. 3D 기하 §2]] (롤·피치·요)

**What it is**: the paper that made real-time MPC standard on legged robots. The trick is a
*deliberate simplification*, made in five modelling moves:

1. **Single rigid body**: approximate the robot as one rigid body (ignore leg dynamics). That is reasonable when the legs are light compared with the body, but it is a real omission: the momentum of a fast leg swing is simply not in the model.
2. **Small roll and pitch**: linearize the rotation dynamics under a small roll-and-pitch
   assumption (roll, pitch and yaw are the body's rotations about its forward, sideways and
   vertical axes). The single state matrix uses the *average* reference yaw over the horizon, while
   each step's input matrix uses that step's reference yaw and footholds.
   The one exception is the first step, which uses the current robot state instead.
3. **Forces as decisions**: treat ground reaction forces as the decision variables.
4. **Friction pyramid**: approximate each circular friction cone by linear facets.
5. **Condensed QP, solved fast**: those linear inequalities keep the problem a **convex QP**,
   solved in the condensed form of [[04-robotics/mpc|7. MPC §2]], that solved in under a
   millisecond in the reported implementation and was re-run at tens of Hz (Di Carlo et al.'s
   abstract says 20–30 Hz while their experiments ran at 25 to 50 Hz depending on gait, so the
   50 Hz [[04-robotics/mpc|7. MPC §2]] sizes is the top of the paper's own range, not a
   disagreement) — exactly the machinery of [[02-foundations/optimization|4. Optimization §5]].

**The model behind the five moves, written out.**

- **Single rigid body dynamics** (move 1). With the legs treated as massless, the only forces on the body are gravity and the four ground reaction forces, so Newton's and Euler's equations give
$$m\,\ddot p=\sum_{i=1}^{4}f_i-m\,g,\qquad \frac{d}{dt}\big(I\,\omega\big)=\sum_{i=1}^{4}r_i\times f_i$$
  where $m$ is the total mass, $p$ the centre-of-mass position, $g=(0,0,9.81)$ m/s², $f_i\in\mathbb{R}^3$ the ground reaction force at foot $i$, $r_i$ the foot position relative to the centre of mass, $I$ the body inertia in world axes and $\omega$ the angular velocity. Example: a 12 kg robot standing still on four feet with equal load needs $f_{i,z}=12\times9.81/4=29.43$ N per foot. Non-example: a 2 kg leg swung fast carries momentum these equations have no term for.
- **Small roll and pitch** (move 2). Write $\Theta=(\phi,\theta,\psi)$ for roll, pitch and yaw. The exact map from $\omega$ to $\dot\Theta$ contains factors $\tan\theta$ and $1/\cos\theta$; with $\phi\approx\theta\approx0$ it keeps only yaw, and the world-frame inertia keeps only the yaw rotation of the body-frame inertia $I_B$:
$$\dot\Theta\approx R_z(\psi)^\top\omega,\qquad I\approx R_z(\psi)\,I_B\,R_z(\psi)^\top$$
  and the gyroscopic term $\omega\times I\omega$ is dropped as small. At $5°$ pitch the neglected factors are $\tan5°=0.087$ and $1/\cos5°=1.004$; at $30°$ they are $0.577$ and $1.155$, which is where the approximation stops being small. With the 13-dimensional state $x=(\Theta,p,\omega,\dot p,g)$ (gravity appended as a constant state so the model has no offset term), discretizing gives $x_{k+1}=A\,x_k+B_k\,u_k$, with one $A$ from the average yaw and a $B_k$ per step.
- **Forces as decisions** (move 3). The input at step $k$ is $u_k=(f_1,\dots,f_4)\in\mathbb{R}^{12}$. A gait's **contact schedule** ([[04-robotics/legged-locomotion|18. Legged Locomotion §2]]) says which feet are down at each step, and a foot in swing gets the equality constraint $f_i=0$, since it cannot push on the ground.
- **Friction pyramid** (move 4). The circular cone $\sqrt{f_x^2+f_y^2}\le\mu f_z$ of [[04-robotics/contact-force-tactile|Contact, Force & Tactile §2]] is not linear. Bounding each tangential axis separately is, and each absolute value is two linear inequalities, which gives the four faces counted below:
$$|f_x|\le\mu f_z,\qquad |f_y|\le\mu f_z$$
  Example: $\mu=0.6$, $f_z=100$ N. The cone allows tangential force up to $60$ N, but the pyramid's corner $(60,60)$ N has magnitude $84.9$ N, so this pyramid admits forces that would slip. Shrinking the coefficient to $\mu/\sqrt2=0.424$ puts the corner at exactly $60$ N, which is safe but rejects $(60,0)$, a force the real cone allows.
- **The QP** (move 5). With reference states $x^{\text{ref}}_k$ from the commanded body motion, weights $Q\succeq0$ on tracking error and $R\succ0$ on force magnitude, and $\lVert v\rVert_Q^2=v^\top Qv$, the controller solves
$$\min_{u_0,\dots,u_{N-1}}\ \sum_{k=0}^{N-1}\lVert x_{k+1}-x_{k+1}^{\text{ref}}\rVert_Q^2+\lVert u_k\rVert_R^2$$
  subject to the dynamics, the pyramid inequalities and the swing equalities. The cost is quadratic and every constraint is linear, so it is a convex QP; substituting the dynamics out leaves the condensed form.

Cheetah 3 galloped on this; the follow-up (Kim et al., open access) pairs the MPC with
whole-body impulse control (built from the null-space task priority and whole-body QP of [[04-robotics/force-compliance-control|13. Force & Compliance Control §4]]) — the standard two-level stack (slow MPC plans forces, fast WBC
tracks them) that echoes [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]'s System 2/System 1 split.

> [!example] Worked example · 계산 예제
> How big is the QP? Take a 13-dimensional state, 4 feet × 3 force components = 12 inputs per step, and horizon $N = 10$.
> - Condensed form eliminates the states, so the decision variables are the forces only: $N \cdot 12 = 120$.
> - (Keeping states as variables too would give $10\cdot 13 + 10\cdot 12 = 250$ — condensing trades these for a denser matrix.)
> - Friction pyramid: 4 faces per foot, per step: $4 \cdot 4 \cdot 10 = 160$ linear inequalities.
> - This counts only the pyramid faces; any force bounds or swing-foot constraints the implementation adds come on top and are not counted here.
> - A 120-variable, 160-inequality QP is tiny, which is why a sub-millisecond solve is plausible.

**Why read it here**: it is the cleanest case study of the modeling craft this wiki's
optimization page teaches — *choose the approximation that makes the problem convex, and
buy back accuracy with re-solving speed*. Also the classical baseline that learned
locomotion policies (RL) are compared against.

**Suggested path**: [[02-foundations/optimization|optimization page]] → Di Carlo et al. (IROS 2018; open copy on MIT DSpace)
§III–IV (simplified dynamics + QP), skimming §V for results → Kim et al. (arXiv 1909.06586) §III–IV for the MPC + whole-body impulse control stack.

### Self-check

1. Which modelling move makes the friction constraint linear, and what does it give up?
2. Why can the state matrix be shared across the horizon while the input matrix changes every step?
3. In the condensed QP above ($N = 10$, 12 inputs), what happens to the number of decision variables if the horizon doubles?

> [!tip]- Answers
> 1. Move 4, the friction pyramid: replacing the circular cone by linear facets gives linear inequalities (keeping the QP convex), at the cost of only approximating the true cone: near its edge the facets and the circle disagree about which forces are feasible.
> 2. The state matrix uses one *average* reference yaw over the horizon; the input matrix depends on that step's reference yaw and footholds, which change as the feet move.
> 3. It doubles: $20 \cdot 12 = 240$ variables (and $4\cdot 4\cdot 20 = 320$ pyramid inequalities).

### Problem set · 과제

Tier C. Claim-reading. Running task: a quadruped carries **P2** toward a panel ([[02-foundations/lab-plants|0.6]]).

1. **Claim.** Which number is the timing claim for the condensed QP?
2. **Falsify.** What motion would falsify the small-roll-and-pitch linearization as “small”?
3. **Task.** P2 on that body, pressing the panel: what does the single-rigid-body QP not contain?

> [!tip]- Solutions
> 1. Sub-millisecond solve, re-run at tens of Hz (abstract 20–30 Hz, experiments 25–50 Hz) — those times *are* the claim.
> 2. Pitch $30^\circ$: the neglected factors are $\tan 30^\circ=0.577$ and $1/\cos 30^\circ=1.155$, which this page already calls no longer small. A rear-up or a fall would do it.
> 3. No arm, no tool wrench, no P3 wall. Ground-reaction forces on four feet are the decisions; contact at the panel is outside the QP.

## 한국어

*D군의 마지막이자 그 응용 사례다. [[04-robotics/mpc|7. MPC]]·[[04-robotics/contact-force-tactile|9. 접촉]]과 [[04-robotics/modern-robotics/index|MR 챕터 요약]] 위에 선다.
최적화 페이지가 가르치는 기술 — 문제를 볼록하게 만드는 근사를 고르는 것 — 의 가장 깔끔한 사례 연구다.*

**무엇인가**: 보행 로봇에서 실시간 MPC를 표준으로 만든 논문. 비결은 *의도된 단순화*이고,
다섯 가지 모델링 선택으로 이루어진다:

1. **단일 강체**: 로봇을 단일 강체로 근사한다(다리 동역학 무시). 다리가 몸통에 비해 가벼우면 합리적이지만, 실제로 빠뜨리는 것이 있다. 다리를 빠르게 휘두를 때의 운동량은 모델에 아예 없다.
2. **작은 롤·피치**: 회전 동역학을 롤과 피치가 작다는 가정 아래 선형화한다(롤·피치·요는 몸통의
   앞뒤·좌우·수직 축에 대한 회전이다). 상태 행렬 하나는
   지평 전체 기준 궤적의 *평균* 요를 쓰고, 단계별 입력 행렬은 그 단계의 기준 요와 발 위치를
   쓴다. 단 하나의 예외는 첫 단계로, 그 단계는 대신 현재 로봇 상태를 쓴다.
3. **힘을 결정 변수로**: 지면 반력을 결정 변수로 삼는다.
4. **마찰 피라미드**: 원형 마찰 원뿔을 선형 면들로 이루어진 마찰 피라미드로 근사한다.
5. **condensed QP, 빠른 풀이**: 이 선형 부등식 덕분에 문제는 **볼록 QP**로 남고,
   [[04-robotics/mpc|7. MPC §2]]의 condensed 형태로 푼다. 보고된 구현에서 1밀리초 안에 풀리고
   수십 Hz로 다시 돈다(Di Carlo 등의 초록은 20~30 Hz지만 실험은 보행 방식에 따라 25~50 Hz로
   돌았다. 그러니 [[04-robotics/mpc|7. MPC §2]]가 잡는 50 Hz는 논문 자신의 범위 상단이지
   불일치가 아니다). 정확히 [[02-foundations/optimization|4. 최적화 §5]]의 기계장치다.

**다섯 선택 뒤의 모델을 풀어 쓰면.**

- **단일 강체 동역학**(선택 1). 다리를 질량 없는 것으로 보면 몸통에 작용하는 힘은 중력과 네 지면 반력뿐이므로 뉴턴·오일러 방정식이 다음을 준다.
$$m\,\ddot p=\sum_{i=1}^{4}f_i-m\,g,\qquad \frac{d}{dt}\big(I\,\omega\big)=\sum_{i=1}^{4}r_i\times f_i$$
  $m$은 전체 질량, $p$는 무게중심 위치, $g=(0,0,9.81)$ m/s², $f_i\in\mathbb{R}^3$는 발 $i$의 지면 반력, $r_i$는 무게중심에 대한 발 위치, $I$는 월드 축의 몸통 관성, $\omega$는 각속도다. 예: 네 발로 하중을 똑같이 나눠 가만히 선 12 kg 로봇은 발마다 $f_{i,z}=12\times9.81/4=29.43$ N이 필요하다. 반례: 빠르게 휘두르는 2 kg 다리가 나르는 운동량에는 이 식에 해당 항이 없다.
- **작은 롤·피치**(선택 2). 롤·피치·요를 $\Theta=(\phi,\theta,\psi)$로 쓴다. $\omega$에서 $\dot\Theta$로 가는 정확한 사상에는 $\tan\theta$와 $1/\cos\theta$ 인자가 들어 있다. $\phi\approx\theta\approx0$이면 요만 남고, 월드 프레임 관성도 몸통 프레임 관성 $I_B$를 요만큼 돌린 것만 남는다.
$$\dot\Theta\approx R_z(\psi)^\top\omega,\qquad I\approx R_z(\psi)\,I_B\,R_z(\psi)^\top$$
  자이로 항 $\omega\times I\omega$도 작다고 보고 버린다. 피치 $5°$에서 버린 인자는 $\tan5°=0.087$, $1/\cos5°=1.004$이고, $30°$에서는 $0.577$과 $1.155$라 근사가 더는 작지 않다. 13차원 상태 $x=(\Theta,p,\omega,\dot p,g)$(모델에 오프셋 항이 없도록 중력을 상수 상태로 덧붙임)로 이산화하면 $x_{k+1}=A\,x_k+B_k\,u_k$가 되고, $A$는 평균 요로 하나, $B_k$는 단계마다 하나다.
- **힘을 결정 변수로**(선택 3). 단계 $k$의 입력은 $u_k=(f_1,\dots,f_4)\in\mathbb{R}^{12}$다. 보행 양식의 **접촉 스케줄**([[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]])이 단계마다 어느 발이 땅에 있는지 정하고, 유각 중인 발은 땅을 밀 수 없으므로 등식 제약 $f_i=0$을 받는다.
- **마찰 피라미드**(선택 4). [[04-robotics/contact-force-tactile|접촉·힘·촉각 §2]]의 원형 원뿔 $\sqrt{f_x^2+f_y^2}\le\mu f_z$는 선형이 아니다. 접선 축을 따로따로 묶으면 선형이 되고, 절댓값 하나가 선형 부등식 둘이므로 아래에서 세는 면 네 개가 나온다.
$$|f_x|\le\mu f_z,\qquad |f_y|\le\mu f_z$$
  예: $\mu=0.6$, $f_z=100$ N. 원뿔은 접선력을 $60$ N까지 허용하지만 피라미드의 모서리 $(60,60)$ N은 크기가 $84.9$ N이라, 이 피라미드는 미끄러질 힘을 허용한다. 계수를 $\mu/\sqrt2=0.424$로 줄이면 모서리가 정확히 $60$ N이 되어 안전하지만, 실제 원뿔이 허용하는 $(60,0)$은 거부한다.
- **QP**(선택 5). 명령한 몸통 운동에서 온 기준 상태 $x^{\text{ref}}_k$, 추종 오차 가중치 $Q\succeq0$, 힘 크기 가중치 $R\succ0$, $\lVert v\rVert_Q^2=v^\top Qv$로 제어기는 다음을 푼다.
$$\min_{u_0,\dots,u_{N-1}}\ \sum_{k=0}^{N-1}\lVert x_{k+1}-x_{k+1}^{\text{ref}}\rVert_Q^2+\lVert u_k\rVert_R^2$$
  제약은 동역학, 피라미드 부등식, 유각 등식이다. 비용이 이차이고 모든 제약이 선형이므로 볼록 QP이고, 동역학을 대입해 없애면 condensed 형태가 남는다.

Cheetah 3가 이걸로 질주했고, 후속(Kim et al., 공개 접근)은 MPC를 전신 임펄스
제어([[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어 §4]]의 영공간 과제 우선순위와 전신 QP로 짜인 것)와 결합한다 — 느린 MPC가 힘을 계획하고 빠른 WBC가 추종하는 표준 2단 스택으로,
[[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T]]의 System 2/System 1 분할과 공명한다.

> [!example] 계산 예제 · Worked example
> QP는 얼마나 큰가? 상태 13차원, 발 4개 × 힘 성분 3개 = 단계당 입력 12개, 지평 $N = 10$으로 잡는다.
> - condensed 형태는 상태를 소거하므로 결정 변수는 힘뿐이다: $N \cdot 12 = 120$개.
> - (상태도 변수로 두면 $10\cdot 13 + 10\cdot 12 = 250$개 — condensed는 이를 더 조밀한 행렬과 맞바꾼다.)
> - 마찰 피라미드: 발마다, 단계마다 면 4개: $4 \cdot 4 \cdot 10 = 160$개의 선형 부등식.
> - 여기서는 피라미드 면만 셌다. 구현이 더하는 힘 한계나 유각(swing) 발 제약은 그 위에 추가되며 세지 않았다.
> - 변수 120개, 부등식 160개짜리 QP는 아주 작다. 1밀리초 미만 풀이가 가능한 이유다.

**여기서 읽는 이유**: 이 위키 최적화 페이지가 가르치는 모델링 기술 — *문제를 볼록하게
만드는 근사를 고르고, 정확도는 재풀이 속도로 되산다* — 의 가장 깔끔한 사례 연구다.
학습 기반 보행 정책(RL)이 비교당하는 고전 베이스라인이기도 하다.

**권장 경로**: [[02-foundations/optimization|최적화 페이지]] → Di Carlo 외(IROS 2018; MIT DSpace 공개본) §III~IV(단순화 동역학 + QP), 결과는 §V를 훑기 → Kim 외(arXiv 1909.06586) §III~IV에서 MPC + 전신 임펄스 제어 스택.

### 스스로 점검

1. 마찰 제약을 선형으로 만드는 모델링 선택은 무엇이고, 그 대가는?
2. 상태 행렬은 지평 전체에서 하나를 공유하는데 입력 행렬은 왜 단계마다 바뀌는가?
3. 위 condensed QP($N = 10$, 입력 12개)에서 지평을 두 배로 늘리면 결정 변수 수는?

> [!tip]- 정답
> 1. 4번, 마찰 피라미드: 원형 원뿔을 선형 면으로 바꿔 선형 부등식을 얻고(QP가 볼록하게 남음), 대신 실제 원뿔은 근사로만 남는다: 가장자리 근처에서는 면과 원이 어떤 힘이 허용되는지 서로 다르게 판정한다.
> 2. 상태 행렬은 지평 전체의 *평균* 기준 요 하나를 쓰지만, 입력 행렬은 그 단계의 기준 요와 발 위치에 의존하고 이것들은 발이 움직이며 바뀐다.
> 3. 두 배가 된다: $20 \cdot 12 = 240$개 (피라미드 부등식은 $4\cdot 4\cdot 20 = 320$개).

### 과제 · Problem set

Tier C. 주장 읽기. 관통 과제: 사족이 [[02-foundations/lab-plants|0.6]]의 **P2**를 패널로 나른다.

1. **주장.** condensed QP의 시간 주장은 어느 숫자인가?
2. **반증.** 작은 롤·피치 선형화를 “작다”고 읽는 주장을 깨는 운동은?
3. **과제.** 그 몸통 위 P2가 패널을 누를 때, 단일 강체 QP에 없는 것은?

> [!tip]- 정답 · Solutions
> 1. 1밀리초 미만 풀이, 수십 Hz 재실행(초록 20–30 Hz, 실험 25–50 Hz) — 그 시간이 곧 주장이다.
> 2. 피치 $30^\circ$: 버린 인자가 $0.577$과 $1.155$로, 이 페이지가 이미 더는 작지 않다고 한다. 뒷발 들기나 전복이면 충분하다.
> 3. 팔 없음, 도구 렌치 없음, P3 벽 없음. 결정 변수는 네 발의 지면 반력이고, 패널 접촉은 QP 밖이다.

### 연결

- 기초: [[02-foundations/optimization|최적화]] · 이전: [[04-robotics/mpc|MPC]]
- 반향: [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] (이중 시스템)

### After reading · 읽고 나면 말할 수 있어야 하는 것

- [ ] Say what the single-rigid-body approximation throws away and what it buys (convexity) · 단일 강체 근사가 버리는 것과 사는 것(볼록성)을 말할 수 있다
- [ ] Describe the setup in which ground reaction forces are the decision variables and friction cones the constraints · 지면 반력 + 마찰 원뿔이 결정 변수·제약이 되는 구성을 말할 수 있다
- [ ] Explain the division of labor in the slow-MPC + fast-WBC two-level stack · 느린 MPC + 빠른 WBC 2단 스택의 분업을 말할 수 있다
- [ ] State the modeling craft this case teaches: choose the approximation that makes the problem convex · 이 사례가 가르치는 모델링 기술(볼록하게 만드는 근사 선택)을 말할 수 있다
