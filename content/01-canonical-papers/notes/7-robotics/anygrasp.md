---
title: "AnyGrasp — Robust and Efficient Grasp Perception in Spatial and Temporal Domains"
authors: Hao-Shu Fang, Chenxi Wang, Hongjie Fang, et al.
affiliation: Shanghai Jiao Tong University
venue: IEEE Transactions on Robotics
year: 2023
arxiv: https://arxiv.org/abs/2212.08333
doi: https://doi.org/10.1109/TRO.2023.3281153
project: https://graspnet.net/anygrasp.html
tags: [paper, manipulation, grasping]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when grasp perception is part of the thesis contribution."
---

**Fang et al., *IEEE T-RO*, vol. 39, no. 5, pp. 3929–3945, 2023** — [arXiv](https://arxiv.org/abs/2212.08333) · [DOI](https://doi.org/10.1109/TRO.2023.3281153) · [Official](https://graspnet.net/anygrasp.html)

> [!note] Math on-ramp · 수학 준비물
> Grasp representation is the thing to have straight: what a 6-DoF or 7-DoF grasp pose *is* ([[02-foundations/se3-geometry|8. SE(3)]]) and what makes one good ([[04-robotics/grasping|15. §3–§4]]). The temporal half needs nothing beyond the idea of correspondence between observations.
> 파지 표현을 분명히 해 두어야 한다: 6자유도 또는 7자유도 파지 자세가 *무엇인지*([[02-foundations/se3-geometry|8. SE(3)]]), 그리고 무엇이 좋은 파지인지([[04-robotics/grasping|15. §3~§4]]). 시간적 절반은 관측 사이의 대응 관계라는 발상 외에 필요한 것이 없다.

## English

**One-line summary**: Dense, temporally smooth 7-DoF grasp perception trained with analytic labels on real perception data, with centre-of-mass awareness and cross-observation grasp correspondence for dynamic tracking.

### Context

[[01-canonical-papers/notes/7-robotics/dex-net-2|Dex-Net 2.0]] proved that analytic labels could train a grasp network, but on synthetic depth images and planar grasps. GraspNet-1Billion moved the supervision to real sensor data. AnyGrasp is where the line arrives at something you would actually deploy: full 7-DoF, dense output, and stable across time rather than recomputed from scratch each frame.

### Method

> [!tip] Key intuition
> A grasp detector that re-decides from scratch every frame is unusable in a closed loop, because its answer jitters. Adding *temporal* correspondence — this grasp in this frame is that grasp in the last one — is what turns detection into tracking, and tracking is what a moving object needs.

- Dense spatial supervision using **real perception with analytic labels**.
- **Centre-of-mass awareness**, so the ranking accounts for where the object's mass is rather than treating the geometry alone.
- **Cross-observation grasp correspondence**, giving temporally smooth output and grasp tracking on moving objects.

### Results

From the paper's **own abstract**: a **93.3% success rate** clearing bins with **over 300 unseen objects**, which the abstract describes as "on par with human subjects under controlled conditions"; and **over 900 mean picks per hour** on a single-arm system.

### Limitations & critique

- "On par with human subjects **under controlled conditions**" is the qualifier that carries the claim — bin clearing is a well-posed setting with a known workspace and cooperative objects.
- Grasp *perception*, not grasp *use*: a good grasp pose is the start of a manipulation task, and nothing here speaks to what happens after the object is held ([[04-robotics/force-compliance-control|13]]).
- Mean picks per hour is a throughput figure from a specific cell; it does not transfer to a different arm or a different reachability situation.
- Rigid, graspable objects. The construction cases of [[04-robotics/grasping|15. §6]] — flexible panels, rebar bundles, unknown $\mu$ — are outside the setting.

### Connections

- [[04-robotics/grasping|15. Grasping]] — the concept page, whose §5 places this in the lineage
- [[01-canonical-papers/notes/7-robotics/dex-net-2|Dex-Net 2.0]] — where the learned line starts

### After reading

- [ ] Say what temporal correspondence buys that per-frame detection cannot.
- [ ] Quote the success rate with its qualifier attached.
- [ ] Name what a grasp-perception result does not tell you about a manipulation task.

## 한국어

**한 줄 요약**: 실제 인식 데이터에 해석적 라벨을 붙여 학습한, 조밀하고 시간적으로 매끄러운 7자유도 파지 인식. 무게중심을 인지하고, 관측 간 파지 대응으로 동적 추적까지 한다.

### 배경

[[01-canonical-papers/notes/7-robotics/dex-net-2|Dex-Net 2.0]]은 해석적 라벨로 파지 네트워크를 학습할 수 있음을 보였지만, 합성 깊이 이미지와 평면 파지에 한해서였다. GraspNet-1Billion이 지도 신호를 실제 센서 데이터로 옮겼다. AnyGrasp은 이 계보가 실제로 배치할 만한 것에 도달한 지점이다: 완전한 7자유도, 조밀한 출력, 그리고 매 프레임 처음부터 다시 계산하는 대신 시간에 걸쳐 안정적인 결과.

### 방법

> [!tip] 핵심 직관
> 매 프레임 처음부터 다시 결정하는 파지 검출기는 폐루프에서 쓸 수 없다. 답이 떨리기 때문이다. *시간적* 대응 — 이 프레임의 이 파지가 지난 프레임의 저 파지다 — 을 더하는 것이 검출을 추적으로 바꾸고, 움직이는 물체에 필요한 것이 추적이다.

- **해석적 라벨을 붙인 실제 인식 데이터**를 쓰는 조밀한 공간적 지도 신호.
- **무게중심 인지** — 기하만 보는 대신 물체의 질량이 어디 있는지를 순위에 반영한다.
- **관측 간 파지 대응** — 시간적으로 매끄러운 출력과 움직이는 물체에 대한 파지 추적.

### 결과

논문 **자신의 초록**에서: 처음 보는 물체 **300개 이상**이 든 통을 비우며 **93.3% 성공률**, 초록의 표현으로 "통제된 조건에서 사람 피험자와 대등"; 그리고 단일 팔 시스템에서 **시간당 평균 900회 이상 집기**.

### 한계와 비판

- "**통제된 조건에서** 사람 피험자와 대등"에서 그 한정이 주장을 지고 있다 — 통 비우기는 작업 구역이 알려져 있고 물체가 협조적인, 잘 정의된 상황이다.
- 파지 *인식*이지 파지 *사용*이 아니다: 좋은 파지 자세는 조작 작업의 시작이고, 물체를 쥔 다음에 무슨 일이 일어나는지에 대해서는 여기서 아무 말도 하지 않는다([[04-robotics/force-compliance-control|13]]).
- 시간당 평균 집기 수는 특정 셀의 처리량 수치다. 다른 팔이나 다른 도달성 상황으로 이전되지 않는다.
- 강체이고 잡을 수 있는 물체들. [[04-robotics/grasping|15. §6]]의 건설 사례 — 휘는 패널, 철근 다발, 알 수 없는 $\mu$ — 는 이 설정 밖이다.

### 연결

- [[04-robotics/grasping|15. 파지]] — §5가 이것을 계보에 놓는 개념 페이지
- [[01-canonical-papers/notes/7-robotics/dex-net-2|Dex-Net 2.0]] — 학습 계보가 시작되는 곳

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 시간적 대응이 프레임별 검출로는 얻을 수 없는 무엇을 사는지 말한다.
- [ ] 성공률을 그 한정과 함께 인용한다.
- [ ] 파지 인식 결과가 조작 작업에 대해 말해 주지 않는 것을 댄다.
