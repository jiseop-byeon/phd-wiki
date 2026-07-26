---
title: "MR Ch.12 — Grasping & Manipulation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.12** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> You need the wrench (moment + force) concept from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]] and vector cross products.
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 렌치(모멘트+힘) 개념과 벡터 외적이 필요하다.

## English

**Core question**: when does a grasp actually hold the object?

- **Contact models**: a frictionless point contact can only *push* along the surface
  normal; a point contact with friction can push anywhere inside the **friction cone** —
  half-angle $\alpha = \tan^{-1}\mu$. For $\mu = 0.5$, $\alpha \approx 26.6°$: the physical
  meaning of a friction coefficient is *an angle*.
- **Form closure**: the geometry alone traps the object (no friction needed) — for
  frictionless point contacts in general position, at least 4 contacts in the plane and
  7 in space. Robust but demanding.
- **Force closure**: with friction, the contacts can resist *any* external wrench —
  the contact friction cones must positively span the whole wrench space. Practical grasps
  are usually force closures with 2–3 fingers.
- **The antipodal intuition** (worked): two fingers gripping opposite sides of an object
  give force closure iff each contact point lies inside the *other* contact's friction
  cone — "the fingers can see each other through their cones." This one picture explains
  why parallel-jaw grippers work on so much of the world.
- **Learning-era continuation**: grasp synthesis is now largely learned (grasp-detection
  networks, dexterous-hand policies), but the *verification* language — cones, wrenches,
  closure — is still how failures are analyzed. Construction case in this wiki:
  [[01-canonical-papers/notes/8-construction/heap|HEAP's dry-stone wall]] is force-closure
  reasoning on irregular, heavy objects.

### Self-check

1. What is the friction cone half-angle for $\mu = 1.0$? What does that imply physically?
2. Why does form closure need more contacts than force closure?
3. State the antipodal grasp condition for a parallel-jaw gripper.

> [!tip]- Answers
> 1. $\alpha = \tan^{-1}1.0 = 45°$: the contact force may tilt up to 45° away from the surface normal before the model says it slips. A friction coefficient is an *angle*, which is why doubling $\mu$ from 0.5 to 1.0 widens the cone from ~26.6° to 45° rather than doubling anything.
> 2. Form closure must block every direction using geometry alone, without the "free" tangential directions that friction cones supply — so it needs more contacts (at least 4 in the plane, 7 in space for frictionless point contacts in general position).
> 3. Each contact point must lie inside the *other* contact's friction cone — the two cones must be able to "see" each other along the line joining the contacts.

### Continue beyond this chapter

[[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] extends grasping to contact modes, force/impedance control, tactile sensing, deformable materials, and sim-to-real evaluation.

## 한국어

**핵심 질문**: 파지는 언제 실제로 물체를 붙잡는가?

- **접촉 모델**: 마찰 없는 점 접촉은 표면 법선 방향으로만 *밀 수* 있다; 마찰 있는 점
  접촉은 **마찰 원뿔** 안 어디로든 밀 수 있다 — 반각 $\alpha = \tan^{-1}\mu$.
  $\mu = 0.5$면 $\alpha \approx 26.6°$: 마찰 계수의 물리적 의미는 *각도*다.
- **Form closure**: 기하만으로 물체를 가둔다(마찰 불필요) — 마찰 없는 점 접촉·일반
  위치 가정에서 평면 최소 4개, 공간 최소 7개의 접촉이 필요하다. 강건하지만 요구가 크다.
- **Force closure**: 마찰이 있으면 접촉들이 *임의의* 외부 렌치를 버틸 수 있다 — 접촉
  마찰 원뿔들이 렌치 공간 전체를 양의 결합으로 생성해야 한다. 실용적 파지는 대개 손가락
  2~3개의 force closure다.
- **대척 파지의 직관** (예제): 물체의 반대편을 잡는 두 손가락이 force closure가 되는
  조건은 각 접촉점이 *상대* 접촉의 마찰 원뿔 안에 있는 것 — "두 손가락이 원뿔을 통해
  서로를 본다." 평행 그리퍼가 세상 대부분에 통하는 이유가 이 그림 하나로 설명된다.
- **학습 시대의 연속**: 파지 생성은 이제 대부분 학습된다(파지 검출 네트워크, 정밀 손
  정책) — 하지만 *검증*의 언어(원뿔, 렌치, closure)는 여전히 실패 분석의 도구다. 이
  위키의 건설 사례: [[01-canonical-papers/notes/8-construction/heap|HEAP의 돌담]]이 불규칙한
  무거운 물체에 대한 force-closure 추론이다.

### 스스로 점검

1. $\mu = 1.0$일 때 마찰 원뿔 반각은? 물리적으로 무엇을 의미하는가?
2. form closure가 force closure보다 많은 접촉을 요구하는 이유는?
3. 평행 그리퍼의 대척 파지 조건을 말하라.

> [!tip]- 정답 · Answers
> 1. $45°$ — 접촉력이 법선에서 45°까지 기울어도 미끄러지지 않는다.
> 2. 마찰 원뿔이 주는 여유 방향 없이 기하만으로 모든 방향을 막아야 하기 때문.
> 3. 두 접촉점이 서로 상대의 마찰 원뿔 안에 있을 것.
