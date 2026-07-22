---
title: "MR Ch.5 — Velocity Kinematics & Statics"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.5** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: how do joint velocities map to end-effector velocity — and forces back?

- **The Jacobian**: $\mathcal{V} = J(\theta)\,\dot\theta$ — column $i$ = the end-effector
  twist produced by unit velocity of joint $i$ (all others frozen). Same object as
  [[02-foundations/calculus-backprop|calculus §1]]'s Jacobian; here its columns are
  transformed screw axes.
- **Statics duality** — the chapter's most elegant result: from power conservation
  ($\dot\theta^\top \tau = \mathcal{V}^\top \mathcal{F}$):
  $$\tau = J^\top(\theta)\,\mathcal{F}$$
  The *same* matrix maps velocities out and wrenches (forces/torques) back in. Gravity
  compensation, force control, and contact reasoning all run on this line.
- **Singularities**: configurations where $J$ loses rank — the arm loses a direction of
  motion (fully stretched arm can't extend further). Near-singularity ⇒ huge joint
  velocities for small task motions.
- **Manipulability ellipsoid**: the image of a unit joint-velocity ball under $J$ — its
  shape (singular values, [[02-foundations/linear-algebra|linear algebra §4]]) tells you
  in which directions the arm moves easily. Force ellipsoid is its inverse-shaped twin.

**Wiki connections**: teleoperation rigs ([[01-canonical-papers/notes/act|ALOHA]]) and
compliant control live on $\tau = J^\top \mathcal{F}$; singularity-aware motion is why raw
VLA outputs get safety-filtered on real arms.

## 한국어

**핵심 질문**: 관절 속도는 말단 속도로, 힘은 그 반대로 어떻게 사상되는가?

- **야코비안**: $\mathcal{V} = J(\theta)\,\dot\theta$ — $i$번째 열 = 관절 $i$만 단위 속도로
  움직일 때의 말단 twist. [[02-foundations/calculus-backprop|미적분 §1]]의 야코비안과 같은
  대상이고, 여기서는 그 열들이 변환된 스크류 축이다.
- **정역학 쌍대성** — 이 장의 가장 우아한 결과: 일률 보존
  ($\dot\theta^\top \tau = \mathcal{V}^\top \mathcal{F}$)에서:
  $$\tau = J^\top(\theta)\,\mathcal{F}$$
  *같은* 행렬이 속도를 내보내고 렌치(힘/토크)를 되받는다. 중력 보상, 힘 제어, 접촉 추론이
  전부 이 한 줄 위에서 돈다.
- **특이점**: $J$가 랭크를 잃는 자세 — 팔이 운동 방향 하나를 잃는다(완전히 뻗은 팔은 더
  뻗을 수 없다). 특이점 근처 ⇒ 작은 작업 운동에 거대한 관절 속도.
- **가조작성 타원체**: 단위 관절 속도 공이 $J$를 통과한 상 — 그 모양(특이값,
  [[02-foundations/linear-algebra|선형대수 §4]])이 팔이 어느 방향으로 쉽게 움직이는지
  알려준다. 힘 타원체는 그 역 모양의 쌍둥이다.

**위키 연결**: 원격조작 장비([[01-canonical-papers/notes/act|ALOHA]])와 유연 제어가
$\tau = J^\top \mathcal{F}$ 위에 살고, 특이점 인지 운동은 실제 팔에서 VLA 원출력에 안전
필터를 거는 이유다.
