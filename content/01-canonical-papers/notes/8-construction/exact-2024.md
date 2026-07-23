---
title: "ExACT — End-to-End Autonomous Excavation via Action Chunking with Transformers (Chen et al., 2024)"
authors: Liangliang Chen, Shiyu Jin, Haoyu Wang, Liangjun Zhang
affiliation: Baidu Research, Robotics and Auto-Driving Lab (RAL)
venue: ICRA 2024 Workshop (3rd Workshop on Future of Construction)
year: 2024
arxiv: https://arxiv.org/abs/2405.05861
pdf: https://arxiv.org/pdf/2405.05861
tags: [paper, construction]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Chen et al., ICRA 2024 Workshop (Future of Construction)** — [arXiv](https://arxiv.org/abs/2405.05861) · [PDF](https://arxiv.org/pdf/2405.05861)

## English

**One-line summary**: Baidu Research retargets ACT to excavation — imitation learning maps raw LiDAR, camera images, and joint positions *directly to hydraulic valve commands* — but the entire validation is **in simulation only**; no real machine was moved.

**Lineage position**: this is a **Baidu Research** paper, not ETH — the same lab that built the deployed [[01-canonical-papers/notes/8-construction/aes|AES]] system here tries the opposite bet: instead of a modular perception-planning-control stack, one end-to-end policy in the style of [[01-canonical-papers/notes/4-vla/act|ACT]]. It sits between ACT (the method source) and [[01-canonical-papers/notes/8-construction/ext|ExT]] (ETH's later, larger-scale version of the same "robot learning meets excavators" merge).

**Method** (literacy level): the ACT architecture — a CVAE transformer that predicts *chunks* of future actions rather than single steps — with the observation space swapped to multimodal excavator sensing (LiDAR, camera, joint positions) and the action space swapped to excavator valve commands. Training is imitation learning from a small set of human-operated demonstration trajectories.

**Evidence**: a simulator built from captured real-world machine data models the relation between valve states and joint velocities; within that simulator, ExACT completes reaching, digging, and dumping tasks from only a few demonstrations. The authors position it as the first attempt at an end-to-end excavator system via imitation learning with minimal demonstrations.

**Limitations**: **simulator-validated only** — there is no real-machine result, so hydraulic-contact and soil-interaction fidelity are untested where they matter most; it is a workshop paper, so evaluation breadth is thin; autonomy claims are therefore about architecture feasibility, not field capability. Testbed-vs-site: neither — simulation only.

## 한국어

**한 줄 요약**: Baidu Research가 ACT를 굴착에 이식했다 — 모방학습이 원시 LiDAR·카메라·관절 위치를 *유압 밸브 명령으로 직접* 매핑한다 — 그러나 검증 전체가 **시뮬레이션뿐**이며, 실기계는 한 번도 움직이지 않았다.

**계보에서의 위치**: 이것은 ETH가 아니라 **Baidu Research** 논문이다 — 배치된 [[01-canonical-papers/notes/8-construction/aes|AES]] 시스템을 만든 바로 그 연구소가 반대 베팅을 시도한다: 모듈형 인식-계획-제어 스택 대신, [[01-canonical-papers/notes/4-vla/act|ACT]] 스타일의 단일 엔드투엔드 정책. 방법론의 원천인 ACT와, 같은 "로봇 학습 × 굴착기" 합류를 더 큰 규모로 밀고 간 ETH의 [[01-canonical-papers/notes/8-construction/ext|ExT]] 사이에 놓인다.

**방법** (리터러시 수준): 한 스텝이 아니라 미래 행동의 *청크*를 예측하는 CVAE 트랜스포머인 ACT 구조에서, 관찰 공간을 멀티모달 굴착기 센싱(LiDAR, 카메라, 관절 위치)으로, 행동 공간을 굴착기 밸브 명령으로 바꿨다. 학습은 소수의 인간 조작 시연 궤적으로부터의 모방학습이다.

**증거**: 실기계에서 수집한 데이터로 밸브 상태와 관절 속도의 관계를 모델링한 시뮬레이터를 만들었고, 그 안에서 ExACT는 소수의 시연만으로 접근(reaching)·굴착(digging)·덤핑(dumping) 과제를 완수한다. 저자들은 이를 최소 시연으로 엔드투엔드 굴착기 시스템을 만든 첫 시도로 자리매김한다.

**한계**: **시뮬레이터 검증뿐** — 실기계 결과가 없으므로, 가장 중요한 유압 접촉·토양 상호작용의 충실도가 정작 필요한 곳에서 검증되지 않았다; 워크숍 논문이라 평가 폭이 얇다; 따라서 자율성 주장은 현장 능력이 아니라 아키텍처 실현 가능성에 관한 것이다. 테스트베드 대 현장: 둘 다 아님 — 시뮬레이션뿐.

### 연결

- 이전: [[01-canonical-papers/notes/4-vla/act|ACT]] · 다음: [[01-canonical-papers/notes/8-construction/ext|ExT]]
- 같은 연구소: [[01-canonical-papers/notes/8-construction/aes|AES]] · 스트림: [[05-construction-robotics/earthmoving-heavy-machinery|3. 토공·중장비 자율화]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (○)

- [ ] ACT를 굴착기로 옮길 때 관찰 공간과 행동 공간이 무엇으로 바뀌는지 말할 수 있다
- [ ] "시뮬레이션 검증뿐"이라는 사실이 이 논문의 주장 강도를 어떻게 제한하는지 말할 수 있다
- [ ] 같은 Baidu 연구소의 모듈형 AES와 이 엔드투엔드 시도의 관계, 그리고 ExT와의 차이를 말할 수 있다
