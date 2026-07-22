---
title: "ExT — Scalable Autonomous Excavation via Multi-Task Pretraining and Fine-Tuning (2025)"
authors: Yifan Zhai, Lorenzo Terenzi, Patrick Frey, Diego Garcia Soto, Pascal Egli, Marco Hutter
affiliation: ETH Zurich, Robotic Systems Lab
venue: arXiv
year: 2025
arxiv: https://arxiv.org/abs/2509.14992
pdf: https://arxiv.org/pdf/2509.14992
tags: [paper, construction, robotics, vla]
status: to-read
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

**Placed in the map**: the merge point of the
[[05-construction-robotics/lineage|lineage]]'s stream 1 (imitation learning) and stream 5
(heavy-machine autonomy) — the open territory this wiki identified, now with its first
occupant. Open questions: task diversity is still excavation-shaped; no language
conditioning; and the safety story for learned policies on real sites is unwritten.

## 한국어

**한 줄 요약**: 파운데이션 모델 레시피가 굴착에 도착했다 — 대규모 시연 수집, **멀티태스크 사전학습**, **SFT/RLFT 파인튜닝**을 하나로 묶은 오픈소스 프레임워크로, 완전한 굴착 사이클을 센티미터급 정확도로 수행한다.

**왜 신호탄인가**: 이것은 [[01-canonical-papers/notes/4-vla/pi0|사전학습 → 사후학습]] 패러다임 —
LLM/VLA 학습의 바로 그 구조 — 를 20톤급 기계에 적용한 것이다. 시연은 *전문가들의
혼합*에서 온다([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]]의 교훈: 이질적 소스가
순수함을 이긴다), 파인튜닝은 지도·RL 두 변형을 제공한다
([[01-canonical-papers/notes/1-foundations/instructgpt|RLHF]] 모양의 선택지). 시뮬레이션/실기계와 기계
구성 간 전이가 사후 고려가 아니라 설계 목표다.

**지도에서의 위치**: [[05-construction-robotics/lineage|계보]]의 1번 흐름(모방학습)과 5번
흐름(중장비 자율성)의 합류점 — 이 위키가 지목했던 열린 영토의 첫 입주자다. 열린 질문:
과제 다양성이 아직 굴착 모양이고, 언어 조건화가 없으며, 실제 현장에서 학습 정책의 안전
서사는 쓰이지 않았다.

### 연결

- 이전: [[01-canonical-papers/notes/8-construction/heap|HEAP]] (플랫폼), [[01-canonical-papers/notes/4-vla/act|ACT]]/[[01-canonical-papers/notes/4-vla/pi0|π0]] (방법론)
- 계보: [[05-construction-robotics/lineage|건설로봇 계보]] 1+5 합류점
