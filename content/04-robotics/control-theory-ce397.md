---
title: "5. Control Theory"
tags: [robotics, control, resource]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Matthew Bartos, UT Austin CE397** — [Course packet PDF (public)](https://future-water-website.s3.amazonaws.com/docs/teaching/ce397/ce397_course_packet.pdf) · [Teaching page](https://future-water.org/teaching/)

## English

> [!info] Depth target · 깊이 목표
> Read state-space models, stability, and controllability/observability claims in robotics papers accurately. Designing controllers beyond the LQR/MPC formulations here is a working/mastery topic.
> 로보틱스 논문의 상태공간 모델·안정성·가제어성/가관측성 주장을 정확히 읽는 것이 목표다. 이 트랙의 LQR/MPC 정식화를 넘는 제어기 설계는 실무/숙달 단계의 주제다.

**What it is**: an introduction to control theory written *for civil engineers* — the same
mathematical core as any controls course (modeling → state space → feedback), but with
examples drawn from infrastructure: structural, hydraulic, transportation, HVAC, and
water systems. The full course packet is publicly available from the instructor's site,
which makes it this wiki's primary control-theory text.

**Contents map** (and where each part connects in this wiki):

1. **Mathematical modeling of infrastructure systems** — writing ODEs for physical systems
   → [[02-foundations/engineering-math|0.5 Engineering Math §8]] is the on-ramp
2. **Time & frequency domain representations** — Laplace, transfer functions, poles
   → [[02-foundations/engineering-math|0.5 §9]] and [[02-foundations/signal-processing|6. Signal Processing §5]]
3. **Linear spaces and operators; state-space models & modal analysis** — the
   [[02-foundations/linear-algebra|1. Linear Algebra §5]] control connection, done properly:
   eigenvalues = modes = stability
4. **Controllability & observability** — the rank conditions
5. **Feedback control** — closing the loop; from here [[04-robotics/lqr-lqg|LQR]] is one
   step (optimal feedback) and [[04-robotics/mpc|MPC]] is two (optimal + constraints,
   re-solved online)
6. **State estimation & system identification** — the
   [[02-foundations/probability|Kalman filter]] in its native habitat, plus learning models
   from data (the classical ancestor of learned dynamics in
   [[01-canonical-papers/notes/5-world-models/dreamer|world models]])

**Suggested path**: read alongside foundations pages 0.5(§8–9) → 1 → 4; then this packet
front to back; then [[04-robotics/lqr-lqg|LQR]] → [[04-robotics/mpc|MPC]]. For a
construction-robotics researcher this packet has a bonus: its examples *are* your domain.

## 한국어

**무엇인가**: *토목 엔지니어를 위해* 쓰인 제어 이론 입문 — 수학적 핵심(모델링 → 상태공간 →
피드백)은 여느 제어 수업과 같지만, 예제가 인프라에서 나온다: 구조물, 수리 시스템, 교통,
HVAC, 상수도. 교수자 사이트에서 코스 패킷 전체가 공개되어 있어, 이 위키의 제어 이론 주교재로
삼는다.

**내용 지도** (각 부분이 이 위키의 어디와 연결되는가):

1. **인프라 시스템의 수학적 모델링** — 물리 시스템의 미분방정식 세우기
   → [[02-foundations/engineering-math|0.5 공업수학 §8]]이 진입로
2. **시간·주파수 영역 표현** — 라플라스, 전달함수, 극점
   → [[02-foundations/engineering-math|0.5 §9]]와 [[02-foundations/signal-processing|6. 신호처리 §5]]
3. **선형 공간과 연산자; 상태공간 모델과 모드 해석** —
   [[02-foundations/linear-algebra|1. 선형대수 §5]]의 제어 연결을 제대로: 고유값 = 모드 = 안정성
4. **가제어성과 가관측성** — 랭크 조건
5. **피드백 제어** — 루프 닫기; 여기서 [[04-robotics/lqr-lqg|LQR]]은 한 걸음(최적 피드백),
   [[04-robotics/mpc|MPC]]는 두 걸음(최적 + 제약, 온라인 재풀이)
6. **상태 추정과 시스템 식별** — [[02-foundations/probability|칼만 필터]]의 본고장, 그리고
   데이터에서 모델 배우기 ([[01-canonical-papers/notes/5-world-models/dreamer|월드모델]]의 학습 동역학의
   고전적 조상)

**권장 경로**: 기초 0.5(§8~9) → 1 → 4와 병행해 이 패킷을 처음부터 끝까지; 그다음
[[04-robotics/lqr-lqg|LQR]] → [[04-robotics/mpc|MPC]]. 건설로봇 연구자에게 이 패킷의 보너스:
예제가 *곧 당신의 도메인*이다.

### 연결

- 기초: [[02-foundations/engineering-math|0.5 공업수학 §8–9]], [[02-foundations/linear-algebra|1. 선형대수]], [[02-foundations/probability|3. 확률]]
- 다음: [[04-robotics/lqr-lqg|LQR/LQG]] → [[04-robotics/mpc|MPC]] → [[04-robotics/convex-mpc-legged|보행 convex MPC]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 상태공간 모델 $\dot x = Ax + Bu$의 각 기호가 물리계의 무엇에 대응하는지 말할 수 있다
- [ ] 안정성 = $A$의 고유값이라는 판정과 s-평면 그림을 연결할 수 있다
- [ ] 가제어성 랭크 조건이 실용적으로 묻는 질문을 말할 수 있다
- [ ] 피드백이 개루프 대비 무엇을 사는지(외란·모델 오차 억제)를 말할 수 있다
