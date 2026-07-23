---
title: "ExT — Scalable Autonomous Excavation via Multi-Task Pretraining and Fine-Tuning (2025)"
authors: Yifan Zhai, Lorenzo Terenzi, Patrick Frey, Diego Garcia Soto, Pascal Egli, Marco Hutter
affiliation: ETH Zurich, Robotic Systems Lab
venue: arXiv
year: 2025
arxiv: https://arxiv.org/abs/2509.14992
pdf: https://arxiv.org/pdf/2509.14992
tags: [paper, construction, robotics, vla]
status: note-complete
last_verified: 2026-07-24
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Zhai, Terenzi et al. (ETH RSL), 2025** — [arXiv](https://arxiv.org/abs/2509.14992) · [PDF](https://arxiv.org/pdf/2509.14992)

## English

**One-line summary**: The foundation-model recipe arrives at excavation — a unified open-source framework for large-scale demonstration collection, **multi-task pretraining**, and **SFT/RLFT fine-tuning** of excavation policies, executing full digging cycles with centimeter-level accuracy.

**Why it is a signal**: this is the
[[01-canonical-papers/notes/4-vla/pi0|pretrain → post-train]] paradigm — the exact structure of
LLM/VLA training — applied to a 20-ton machine class. Demonstrations come from a *mix of
experts* (the [[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]] lesson: heterogeneous
sources beat purity), and fine-tuning offers both supervised and RL variants (the
[[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]]-shaped choice). Transfer across sim/real
and machine configurations is a design goal, not an afterthought.

**The pipeline, concretely** (what a Working-level read should extract):

- **Demonstration generation**: ~100 hours of excavation demonstrations collected in
  **GPU-parallel simulation** (the [[05-construction-robotics/sim-to-real|Isaac-Gym-lineage]]
  recipe), from **three heterogeneous sources** — RL expert policies (trained per-task),
  scripted controllers, and human teleoperation. Simulation is what makes the demos
  unlimited, labeled, and resettable; it is also the recipe's main scope limit.
- **Pretraining**: one transformer policy trained by behavior cloning across the mixed
  multi-task demonstration corpus (arm + chassis action space; excavation task family:
  digging, grading, trenching-class tasks).
- **Fine-tuning, two variants**: **SFT** (supervised, on task-specific demonstrations)
  and **RLFT** (RL fine-tuning against task reward in simulation) — read the paper's
  comparisons for when RLFT beats SFT; the headline is that *both start from the same
  pretrained policy*, which is the paradigm claim.
- **Transfer evidence**: fine-tuned policies execute full digging cycles on the real
  M545 ([[01-canonical-papers/notes/8-construction/heap|HEAP]]) with centimeter-level
  tracking accuracy — sim-to-real transfer of the *pretrained-then-fine-tuned* policy,
  not a from-scratch controller. Evaluation splits are organized around held-out tasks
  and sim-vs-real execution; trace the exact task lists and metrics in §experiments of
  the paper (the note deliberately does not reproduce every table).

**Placed in the map**: the merge that the
[[05-construction-robotics/lineage|lineage]] page calls open territory — era-4 robot
learning (imitation, pretrain→fine-tune) arriving on era-1R heavy machines — now with its
first occupant. Open questions: task diversity is still excavation-shaped; no language
conditioning; and the safety story for learned policies on real sites is unwritten.

## 한국어

**한 줄 요약**: 파운데이션 모델 레시피가 굴착에 도착했다 — 대규모 시연 수집, **멀티태스크 사전학습**, **SFT/RLFT 파인튜닝**을 하나로 묶은 오픈소스 프레임워크로, 완전한 굴착 사이클을 센티미터급 정확도로 수행한다.

**왜 신호탄인가**: 이것은 [[01-canonical-papers/notes/4-vla/pi0|사전학습 → 사후학습]] 패러다임 —
LLM/VLA 학습의 바로 그 구조 — 를 20톤급 기계에 적용한 것이다. 시연은 *전문가들의
혼합*에서 온다([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]]의 교훈: 이질적 소스가
순수함을 이긴다), 파인튜닝은 지도·RL 두 변형을 제공한다
([[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]] 모양의 선택지). 시뮬레이션/실기계와 기계
구성 간 전이가 사후 고려가 아니라 설계 목표다.

**파이프라인, 구체적으로** (Working 수준의 읽기가 뽑아내야 할 것):

- **시연 생성**: **GPU 병렬 시뮬레이션**([[05-construction-robotics/sim-to-real|Isaac Gym 계열]] 레시피)에서 수집한 약 100시간의 굴착 시연 — **세 가지 이질적 소스**: (과제별로
  학습된) RL 전문가 정책, 스크립트 제어기, 인간 원격조작. 시뮬레이션이 시연을 무제한·
  라벨된·리셋 가능하게 만들며, 동시에 이 레시피의 주된 범위 한계이기도 하다.
- **사전학습**: 혼합 멀티태스크 시연 코퍼스에 대한 행동 복제로 학습되는 하나의 트랜스포머
  정책 (팔 + 섀시 행동 공간; 굴착 과제군: 굴착·정지·트렌칭류).
- **파인튜닝, 두 변형**: **SFT**(과제별 시연에 지도학습)와 **RLFT**(시뮬레이션에서 과제
  보상에 대한 RL 파인튜닝) — RLFT가 SFT를 이기는 조건은 논문의 비교를 읽어라; 헤드라인은
  *둘 다 같은 사전학습 정책에서 출발한다*는 것 — 그게 패러다임 주장이다.
- **전이 증거**: 파인튜닝된 정책이 실제 M545([[01-canonical-papers/notes/8-construction/heap|HEAP]])
  에서 센티미터급 추종 정확도로 완전한 굴착 사이클을 수행 — 밑바닥부터 만든 제어기가
  아니라 *사전학습→파인튜닝* 정책의 sim-to-real 전이다. 평가 분할은 held-out 과제와
  sim/real 실행을 축으로 조직된다; 정확한 과제 목록과 지표는 논문의 실험 섹션에서
  추적하라 (노트는 모든 표를 재현하지 않는다).

**지도에서의 위치**: [[05-construction-robotics/lineage|계보]] 페이지가 열린 영토라 부르는
합류 — 4시대의 로봇 학습(모방, 사전학습→파인튜닝)이 1R시대의 중장비에 도착하는 지점 —
의 첫 입주자다. 열린 질문:
과제 다양성이 아직 굴착 모양이고, 언어 조건화가 없으며, 실제 현장에서 학습 정책의 안전
서사는 쓰이지 않았다.

### 연결

- 이전: [[01-canonical-papers/notes/8-construction/heap|HEAP]] (플랫폼), [[01-canonical-papers/notes/4-vla/act|ACT]]/[[01-canonical-papers/notes/4-vla/pi0|π0]] (방법론)
- 계보: [[05-construction-robotics/lineage|건설로봇 계보]]의 4시대×1R시대 합류점

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "scalable autonomous excavation"의 scalable은 프레임워크(수집→사전학습→파인튜닝)의 확장 가능성 주장이지, 실제 현장 배치의 검증이 아니다 — 안전 체계와 과제 다양성은 열린 문제로 남아 있다. "굴착의 파운데이션 모델 시대가 열렸다"는 신호로 읽되, "도착했다"로 읽지 마라.

### 읽고 나면 말할 수 있어야 하는 것 · After reading (★)

- [ ] 시연 생성(GPU 병렬 시뮬, 3소스 혼합)→사전학습→SFT/RLFT→실기계 전이의 파이프라인을 단계별로 말할 수 있다
- [ ] 사전학습→SFT/RLFT 구조가 LLM/VLA 레시피의 무엇을 가져왔는지 말할 수 있다
- [ ] "전문가 혼합 시연"이 OXE의 어떤 교훈(이질적 소스 > 순수함)을 반복하는지 말할 수 있다
- [ ] 굴착이 탁상 조작과 다른 난점(접촉력, 기계 규모, 안전)을 말할 수 있다
- [ ] 이 논문이 왜 로봇 학습(4시대)과 중장비 자율성(1R시대)의 합류점인지 설명할 수 있다
