---
title: "MR Ch.12 — Grasping & Manipulation"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.12** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] Prerequisites · 선수 지식
> You need the wrench (moment + force) concept from [[04-robotics/modern-robotics/ch05-velocity-kinematics|ch.5]] and vector cross products.
> [[04-robotics/modern-robotics/ch05-velocity-kinematics|5장]]의 렌치(모멘트+힘) 개념과 벡터 외적이 필요하다.

## English

**Core question**: when does a grasp actually hold the object?

- **Contact models**: a frictionless point contact can only *push* along the surface
  normal; a point contact with friction can push anywhere inside the **friction cone** —
  half-angle $\alpha = \tan^{-1}\mu$. For $\mu = 0.5$, $\alpha \approx 26.6°$: the physical
  meaning of a friction coefficient is *an angle*.
- **Form closure**: the geometry alone traps the object (no friction needed) — for
  frictionless point contacts, at least 4 contacts in the plane and 7 in space. Robust but
  demanding. Those counts are for **first-order** form closure, which is the qualifier that
  matters: they follow from linearizing the contact constraints, so they only see the contact
  normals. Let the surfaces curve and second-order effects can immobilize a planar body with
  **two** contacts, well under the bound. So the number to quote depends on the order of the
  analysis, not on how the contacts are arranged.
- **Force closure**: with friction, the contacts can resist *any* external wrench —
  the contact friction cones must positively span the whole wrench space. Practical grasps
  are usually force closures with 2–3 fingers.
- **The antipodal intuition** (worked): for a **planar body with two frictional point
  contacts**, the line joining the contacts must lie inside both friction cones — "the
  fingers can see each other through their cones." In spatial grasping, two hard point
  contacts cannot resist torque about their connecting axis; at least three point contacts
  are needed. Two **soft-finger** contacts can add torsional moments and achieve spatial
  force closure. Always name the contact model before claiming closure.
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
> 2. Form closure must block every direction using geometry alone, without the "free" tangential directions that friction cones supply — so it needs more contacts (at least 4 in the plane, 7 in space for frictionless point contacts). Those bounds are first-order results; curvature is a second-order effect and can immobilize a planar body with two contacts.
> 3. For the planar two-point model, the line joining the contacts lies inside both friction cones. This is not by itself a spatial force-closure test for two hard point contacts; a spatial parallel-jaw argument needs a soft-finger contact model or another source of torsional resistance.

### Continue beyond this chapter

[[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] extends grasping to contact modes, force/impedance control, tactile sensing, deformable materials, and sim-to-real evaluation.

## 한국어

**핵심 질문**: 파지는 언제 실제로 물체를 붙잡는가?

- **접촉 모델**: 마찰 없는 점 접촉은 표면 법선 방향으로만 *밀 수* 있다; 마찰 있는 점
  접촉은 **마찰 원뿔** 안 어디로든 밀 수 있다 — 반각 $\alpha = \tan^{-1}\mu$.
  $\mu = 0.5$면 $\alpha \approx 26.6°$: 마찰 계수의 물리적 의미는 *각도*다.
- **Form closure**: 기하만으로 물체를 가둔다(마찰 불필요) — 마찰 없는 점 접촉에서 평면
  최소 4개, 공간 최소 7개의 접촉이 필요하다. 강건하지만 요구가 크다. 이 수는 **1차**
  form closure에 대한 것이고, 그 단서가 핵심이다. 접촉 구속을 선형화해서 얻은 결과라 접촉
  법선만 본다. 표면이 휘면 2차 효과가 개입해 평면 물체를 접촉 **2개**로 가둘 수 있고, 이는
  경계보다 한참 아래다. 즉 인용할 숫자는 접촉을 어떻게 배치했는지가 아니라 몇 차까지
  분석했는지에 달렸다.
- **Force closure**: 마찰이 있으면 접촉들이 *임의의* 외부 렌치를 버틸 수 있다 — 접촉
  마찰 원뿔들이 렌치 공간 전체를 양의 결합으로 생성해야 한다. 실용적 파지는 대개 손가락
  2~3개의 force closure다.
- **대척 파지의 직관** (예제): **평면 물체와 마찰 점접촉 둘**의 모델에서는 두 접촉점을
  잇는 선이 두 마찰 원뿔 안에 있어야 한다 — "두 손가락이 원뿔을 통해 서로를 본다."
  공간에서는 hard point 접촉 둘만으로 두 점을 잇는 축 둘레의 토크를 막을 수 없어 최소 세
  점접촉이 필요하다. **Soft-finger** 접촉 둘은 비틀림 모멘트를 더해 공간 force closure가
  가능하다. Closure를 주장하기 전에 접촉 모델부터 밝혀야 한다.
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
> 2. 마찰 원뿔이 주는 여유 방향 없이 기하만으로 모든 방향을 막아야 하기 때문이다(마찰 없는 점 접촉에서 평면 최소 4개, 공간 최소 7개). 이 경계는 1차 결과이고, 곡률은 2차 효과라 평면 물체를 접촉 2개로 가둘 수 있다.
> 3. 평면 2점 모델에서는 두 접촉점을 잇는 선이 두 마찰 원뿔 안에 있어야 한다. 이것만으로
> 공간의 hard point 접촉 둘이 force closure인 것은 아니다. 공간 평행 그리퍼에는 soft-finger
> 모델이나 다른 비틀림 저항이 필요하다.

### 이 장 다음으로

[[04-robotics/contact-force-tactile|접촉·힘·촉각 상호작용]]이 파지를 접촉 모드, 힘·임피던스
제어, 촉각 센싱, 변형체, sim-to-real 평가로 확장한다.
