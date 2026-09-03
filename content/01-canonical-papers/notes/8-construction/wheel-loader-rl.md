---
title: "Automatic Loading of Unknown Material with a Wheel Loader Using RL (Eriksson et al., 2024)"
authors: Eriksson, Ghabcheloo & Geimer
affiliation: Tampere University (Ghabcheloo group) · Karlsruhe Institute of Technology (Geimer)
venue: ICRA 2024
year: 2024
pdf: https://trepo.tuni.fi/bitstream/handle/10024/211807/icra2024.pdf
tags: [paper, construction, wheel-loader, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Eriksson, Ghabcheloo & Geimer, ICRA 2024** — [Open PDF (Trepo)](https://trepo.tuni.fi/bitstream/handle/10024/211807/icra2024.pdf)

> [!note] Math on-ramp · 수학 준비물
> [[02-foundations/rl-basics|7. RL Basics §6 and §9]] — the recipe is imitation pretraining followed by RL fine-tuning on hardware, which is exactly the RLFT pattern §9 describes, including its safety-envelope question.
> [[02-foundations/rl-basics|7. RL 기초 §6·§9]] — 레시피가 모방 사전학습 후 실기계 RL 파인튜닝이고, 이는 §9가 기술하는 RLFT 패턴 그대로다(안전 영역 문제까지 포함해서).

## English

**One-line summary**: An imitation-pretrained, RL-fine-tuned controller performs wheel-loader bucket filling on a real machine against previously unknown material, bringing learned contact control across material variation onto a real heavy-machine task.

**Lineage position**: alongside [[01-canonical-papers/notes/8-construction/egli-rl|Egli's RL excavation work at ETH]], this is the RL-on-real-heavy-machines strand — the wheel-loader counterpart of learned bucket–pile interaction, and one of the few real-machine (not simulator-only) results in the [[05-construction-robotics/sim-to-real|sim-to-real]] stream.

> [!tip] Key intuition · 핵심 직관
> Imitation gives the controller an initial loading behavior, while reinforcement learning adjusts coordinated vehicle and bucket actions under interaction with the pile. The useful mechanism is coordination under changing resistance, not a universal advantage of one learning label over every classical controller.

**Method**: the policy is pretrained by imitation from demonstrations and fine-tuned with reinforcement learning, then evaluated on a real wheel loader across materials. Bucket filling couples vehicle motion (traction into the pile) with boom/bucket motion under uncertain granular contact — the coordination problem that makes scripted controllers brittle. Read the observation/action space, the simulator's material model, the safety envelope, and the real-machine test protocol together; the contribution is not "RL beats classical control everywhere" but that one learned policy coordinates vehicle and bucket motion during uncertain pile interaction.

**Evidence and limitations**: the evaluation is on a real wheel loader with materials not directly parameterized for the policy — "unknown material" means outside the policy's identified parameters in the reported evaluation, not all granular materials, pile geometries, weather conditions, or machines. Inspect the variation actually tested before generalizing the claim.

> [!question] Reading the claim · 핵심 주장 읽는 법
> "Unknown material" claims generalization to materials not used in training, not a guarantee for arbitrary materials — the list of materials tested *is* the scope of the claim. And "automatic loading" means automating the short loading cycle, not site operations as a whole.

## 한국어

**한 줄 요약**: 모방학습으로 사전학습하고 RL로 파인튜닝한 제어기가 실제 휠로더에서 미지의 재료에 대한 버킷 채우기를 수행해, 재료 변동을 가로지르는 학습 기반 접촉 제어를 실제 중장비 과제로 가져왔다.

**계보에서의 위치**: [[01-canonical-papers/notes/8-construction/egli-rl|ETH Egli의 RL 굴착 연구]]와 나란히, 실제 중장비 위의 RL 갈래다 — 학습된 버킷–더미 상호작용의 휠로더 판이며, [[05-construction-robotics/sim-to-real|sim-to-real]] 스트림에서 시뮬레이터 전용이 아닌 몇 안 되는 실기계 결과 중 하나다.

> [!tip] 핵심 직관 · Key intuition
> 모방은 초기 적재 행동을 주고 강화학습은 더미와의 상호작용 아래 차량·버킷 협응을 조절한다. 유용한 기전은 변하는 저항 아래 협응이다. 특정 학습 방식이 모든 고전 제어기보다 낫다는 뜻은 아니다.

**방법**: 정책은 시연으로부터 모방 사전학습된 뒤 강화학습으로 파인튜닝되고, 실제 휠로더에서 여러 재료에 걸쳐 평가된다. 버킷 채우기는 불확실한 입상 접촉 아래에서 차량 운동(더미로의 견인)과 붐/버킷 운동을 결합한다 — 스크립트 제어기를 취약하게 만드는 바로 그 조정 문제다. 관측/행동 공간, 시뮬레이터의 재료 모델, 안전 영역, 실기계 시험 프로토콜을 함께 읽어야 한다. 기여는 "RL이 어디서나 고전 제어를 이긴다"가 아니라, 하나의 학습 정책이 불확실한 더미 상호작용 중에 차량과 버킷 운동을 조정한다는 것이다.

**증거와 한계**: 평가는 정책에 직접 매개변수화되지 않은 재료로 실제 휠로더에서 이루어졌다 — "unknown material"은 보고된 평가에서 정책의 식별된 매개변수 밖이라는 뜻이지, 모든 입상 재료·더미 기하·날씨·기계를 뜻하지 않는다. 주장을 일반화하기 전에 실제로 시험된 변동 범위를 확인하라.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "unknown material"은 학습에 안 쓴 재료로의 일반화 주장이지 임의 재료 보장이 아니다 — 시험된 재료 목록이 곧 주장의 범위다. 그리고 "automatic loading"은 짧은 적재 사이클(short loading cycle)의 자동화이지 현장 운영 전체가 아니다.

### 연결

- 이웃: [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL 굴착]] (굴착기 쪽의 RL 대응물)
- 스트림: [[05-construction-robotics/earthmoving-heavy-machinery|토공·중장비]] · [[05-construction-robotics/sim-to-real|sim-to-real]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (◐)

- [ ] State the control scope the learned policy covers in wheel-loader bucket filling (vehicle plus boom/bucket coordination) · 휠로더 버킷 채우기에서 학습 정책이 담당하는 제어 범위(차량 + 붐/버킷 조정)를 말할 수 있다
- [ ] Find and state the IL-pretraining plus RL-fine-tuning structure, the sim-to-real evidence, and the safety devices in the paper · IL 사전학습 + RL 파인튜닝 구조와 sim-to-real 증거·안전 장치를 논문에서 찾아 말할 수 있다
- [ ] Explain how the "unknown material" claim is bounded by the variation distribution actually tested · "unknown material" 주장이 실제로 시험된 변동 분포에 어떻게 한정되는지 설명할 수 있다
- [ ] Say where the learning problem is the same and where it differs between excavators (Egli) and wheel loaders (cycle structure, driving coupling) · 굴착기(Egli)와 휠로더의 학습 문제가 어디서 같고 어디서 다른지(사이클 구조·주행 결합) 말할 수 있다
