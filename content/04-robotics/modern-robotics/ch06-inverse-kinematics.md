---
title: "MR Ch.06 — Inverse Kinematics"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.6** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

## English

**Core question**: given a desired end-effector pose, what joint angles achieve it?

- Unlike FK, IK has **zero, one, several, or infinitely many** solutions (elbow-up vs
  elbow-down; a 7-dof arm has a continuum). This multimodality is exactly why
  [[01-canonical-papers/notes/4-vla/diffusion-policy|generative policies]] beat regression on
  action prediction — IK is the classical face of the same problem.
- **Analytic IK**: closed-form for specific geometries (6R with spherical wrist) — fast,
  exact, enumerate all branches.
- **Numerical IK** = Newton-Raphson on the pose error: iterate
  $\Delta\theta = J^\dagger(\theta)\, \mathcal{V}_{err}$ where $\mathcal{V}_{err} = \log(T_{now}^{-1} T_{goal})$
  — the error *twist* from [[04-robotics/modern-robotics/ch03-rigid-body-motions|ch.3]]'s
  log map, and $J^\dagger$ the pseudoinverse
  ([[02-foundations/linear-algebra|least squares]]). It's gradient-based root finding —
  the same [[02-foundations/optimization|optimization]] toolbox.
- Near singularities the pseudoinverse explodes → **damped least squares**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$ trades accuracy for sanity (ridge regression in
  disguise).
- **Redundancy** ($n > 6$): the null space of $J$ moves joints without moving the tool —
  spend it on secondary objectives (avoid limits, obstacles, singularities).

**Wiki connections**: every teleop stack ([[01-canonical-papers/notes/4-vla/act|ALOHA]]) and
end-effector-space VLA runs IK (or its velocity-level cousin) between policy output and
motor commands.

## 한국어

**핵심 질문**: 원하는 말단 자세가 주어지면 어떤 관절 각이 그것을 달성하는가?

- FK와 달리 IK의 해는 **0개, 1개, 여러 개, 무한히 많을 수** 있다(팔꿈치 위/아래; 7자유도
  팔은 연속체). 이 다봉성이 정확히 [[01-canonical-papers/notes/4-vla/diffusion-policy|생성형
  정책]]이 행동 예측에서 회귀를 이기는 이유다 — IK는 같은 문제의 고전적 얼굴이다.
- **해석적 IK**: 특정 기하(구면 손목의 6R)의 닫힌 형태 — 빠르고 정확하며 모든 가지를 열거.
- **수치적 IK** = 자세 오차에 대한 뉴턴-랩슨: 반복
  $\Delta\theta = J^\dagger(\theta)\, \mathcal{V}_{err}$, 여기서
  $\mathcal{V}_{err} = \log(T_{now}^{-1} T_{goal})$ —
  [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]] 로그 사상의 오차 *twist*,
  $J^\dagger$는 유사역행렬([[02-foundations/linear-algebra|최소제곱]]).
  그래디언트 기반 근 찾기 — 같은 [[02-foundations/optimization|최적화]] 도구 상자다.
- 특이점 근처에서 유사역행렬이 폭발 → **감쇠 최소제곱**
  $J^\top(JJ^\top + \lambda^2 I)^{-1}$이 정확도를 제정신과 맞바꾼다(변장한 릿지 회귀).
- **여유자유도** ($n > 6$): $J$의 영공간은 도구를 움직이지 않고 관절만 움직인다 — 이를 2차
  목표(한계·장애물·특이점 회피)에 쓴다.

**위키 연결**: 모든 원격조작 스택([[01-canonical-papers/notes/4-vla/act|ALOHA]])과 말단 공간 VLA가
정책 출력과 모터 명령 사이에서 IK(또는 그 속도 수준 사촌)를 돌린다.
