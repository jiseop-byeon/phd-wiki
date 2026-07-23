---
title: 0. Study Depth Guide
tags: [curriculum, guide]
study-depth: Literacy
depth-goal: "Use this guide to assign the minimum depth for every topic before studying."
mastery-when: "The guide itself is not a mastery target; promote the selected contribution pages."
---

This page sets the **recommended minimum depth for a construction Physical AI
researcher**. It is different from the ★·◐·○ marks in the paper list:

- **★·◐·○ = how much of that paper to read.**
- **Literacy / Working / Mastery = how well to use that knowledge.**

Every substantive page displays its recommended minimum and the condition for raising it
to Mastery. The recommendation is a starting profile, not a permanent label.

## The three depths

| Depth | Completion test | Use it for |
|---|---|---|
| **Literacy** | Explain the problem, vocabulary, inputs/outputs, central claim, evidence, and limitation | every adjacent field |
| **Working** | Select the method, follow its formulation or code, choose evaluation, and diagnose common failure | methods and system layers used in experiments |
| **Mastery** | Critique assumptions, reproduce or modify the method, design decisive experiments, and defend novelty | the thesis contribution and its closest dependency |

> [!important] Mastery is contribution-dependent
> No fixed curriculum can declare every future thesis topic in advance. This guide assigns
> the common minimum. When a research question is selected, promote its contribution page
> and closest dependency to Mastery; do not promote an entire field.

## Recommended profile

| Area | Default | Raise to Mastery when… |
|---|---:|---|
| Engineering math, linear algebra, calculus, probability, optimization | Working | the thesis contribution is mathematical, probabilistic, or optimization-based |
| Information theory | Literacy | the objective or representation claim depends on KL, entropy, mutual information, or a variational bound |
| Signal processing, state estimation, calibration, SE(3) | Working | sensing, localization, or calibration is the claimed contribution |
| Deep-learning history and ecosystem maps | Literacy | never as a whole—promote the specific method instead |
| Perception, 3D geometry, point clouds | Working | perception or geometric reconstruction carries the novelty |
| VLM | Literacy; selected encoders at Working | multimodal grounding or semantic reasoning is modified |
| VLA, imitation learning, robot learning | Working | policy learning, action representation, or data mixture carries the novelty |
| Diffusion, flow matching, world models | Literacy broadly; directly used methods at Working | the generative objective, dynamics model, or planner is modified |
| Kinematics, dynamics, planning, control, robot systems | Working | the corresponding subsystem is modified or defended as novel |
| HRI and safety | Working for deployed field systems | interaction, safety assurance, or human factors is the contribution |
| Construction lineage, labs, industry map | Literacy | these are landscape maps, not implementation methods |
| Construction task streams and deployment evaluation | Working | the selected task, workflow, or field-deployment layer carries the novelty |
| Research practice | Working | throughout the project; mastery is demonstrated through defensible research |

## How to adjust the profile

1. Begin with each page's `study-depth`.
2. When a candidate problem appears, identify its **contribution layer** and one closest
   **dependency layer**.
3. Promote the contribution layer to Mastery and the dependency to at least Working.
4. Keep the rest at Literacy unless an experiment repeatedly fails there.
5. Revisit the decision after the first baseline and failure analysis.

Example: a construction-excavator VLA thesis might use **construction deployment,
action representation, and policy learning** at Mastery; **SE(3), perception, control,
and sim-to-real** at Working; and the remaining model families at Literacy.

## 한국어

이 페이지는 **건설 Physical AI 연구자에게 권장하는 최소 학습 깊이**를 정한다.
논문 목록의 ★·◐·○와는 역할이 다르다.

- **★·◐·○ = 그 논문을 얼마나 읽을 것인가**
- **Literacy / Working / Mastery = 그 지식을 어느 수준으로 사용할 것인가**

모든 주요 페이지는 권장 최소 깊이와 Mastery로 올려야 하는 조건을 표시한다.
이 값은 출발점이지 영구적인 등급이 아니다.

### 세 가지 깊이

| 깊이 | 완료 기준 | 적용 범위 |
|---|---|---|
| **Literacy · 독해** | 문제·용어·입출력·핵심 주장·근거·한계를 설명한다 | 모든 인접 분야 |
| **Working · 실무** | 방법을 선택하고 정식화/코드를 따라가며 평가와 실패 원인을 판단한다 | 실험에서 직접 쓰는 방법과 시스템 층 |
| **Mastery · 숙달** | 가정을 비판하고 재현·변형하며 결정적 실험과 novelty를 방어한다 | 논문의 기여 영역과 가장 가까운 의존 영역 |

> [!important] Mastery는 연구 기여에 따라 정한다
> 미래의 논문 주제를 커리큘럼이 미리 확정할 수는 없다. 이 가이드는 공통 최소값을
> 배정한다. 연구 질문이 정해지면 **기여 페이지와 가장 가까운 의존 페이지**만
> Mastery로 올리고, 분야 전체를 Mastery로 올리지 않는다.

### 권장 프로필

| 영역 | 기본 깊이 | Mastery가 필요한 경우 |
|---|---:|---|
| 공업수학·선형대수·미적분·확률·최적화 | Working | 수학적 정식화·추정·최적화가 기여일 때 |
| 정보이론 | Literacy | KL·엔트로피·상호정보량·변분 경계가 주장에 직접 필요할 때 |
| 신호처리·상태추정·보정·SE(3) | Working | 센싱·위치추정·보정이 기여일 때 |
| 딥러닝 역사·생태계 지도 | Literacy | 전체가 아니라 실제 사용하는 방법만 승격 |
| 인식·3D 기하·포인트 클라우드 | Working | 인식이나 기하 복원이 novelty일 때 |
| VLM | Literacy, 선택한 encoder는 Working | 멀티모달 grounding이나 의미 추론을 수정할 때 |
| VLA·모방학습·로봇러닝 | Working | 정책·행동 표현·데이터 혼합이 기여일 때 |
| 디퓨전·flow matching·world model | 넓게 Literacy, 직접 쓰는 방법은 Working | 생성 목적함수·동역학 모델·planner를 수정할 때 |
| 기구학·동역학·계획·제어·로봇 시스템 | Working | 해당 subsystem이 novelty일 때 |
| HRI·안전 | 현장 배치 연구에서는 Working | 상호작용·안전 보증·human factors가 기여일 때 |
| 건설 계보·랩·산업 지도 | Literacy | 구현 방법이 아닌 분야 지도 |
| 건설 작업 스트림·현장 평가 | Working | 선택한 작업·workflow·배치 층이 기여일 때 |
| Research Practice | Working | 프로젝트 전체에서 적용하며, 숙달은 실제 연구로 증명 |

### 깊이를 조절하는 방법

1. 각 페이지의 `study-depth`에서 시작한다.
2. 연구 후보가 생기면 **기여 층**과 가장 가까운 **의존 층** 하나를 고른다.
3. 기여 층은 Mastery, 의존 층은 최소 Working으로 올린다.
4. 나머지는 실험 실패가 반복되기 전까지 Literacy로 유지한다.
5. 첫 baseline과 실패 분석 뒤 다시 조정한다.

예를 들어 건설 굴착기 VLA 논문이라면 건설 현장 평가·행동 표현·정책 학습은
Mastery, SE(3)·인식·제어·sim-to-real은 Working, 나머지 모델 계열은 Literacy가
될 수 있다.

### Connections

- [[01-canonical-papers/how-to-read|How to Read Papers]] · [[01-canonical-papers/canonical-list|Canonical Paper List]] · [[08-research-radar/index|Research Radar]]
