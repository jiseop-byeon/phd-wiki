---
title: "Clio — Real-time Task-Driven Open-Set 3D Scene Graphs"
authors: Dominic Maggio, Yun Chang, Nathan Hughes, Matthew Trang, Dan Griffith, Carlyn Dougherty, Eric Cristofalo, Lukas Schmid, Luca Carlone
affiliation: MIT (SPARK Lab), MIT Lincoln Laboratory
venue: IEEE RA-L
year: 2024
journal-ref: "IEEE RA-L 9(10), 8921–8928"
arxiv: https://arxiv.org/abs/2404.13696
project: https://github.com/MIT-SPARK/Clio
tags: [paper, navigation, mapping, scene-graph, open-vocabulary]
status: note-complete
last_verified: 2026-08-22
study-depth: Literacy
wiki-support: Working
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if map granularity becomes a design decision you have to defend."
---

**Maggio, Chang, Hughes et al., *IEEE RA-L* 9(10), 8921–8928, 2024** — [arXiv:2404.13696](https://arxiv.org/abs/2404.13696) · [Code](https://github.com/MIT-SPARK/Clio)

> [!note] Math on-ramp · 수학 준비물
> The Information Bottleneck: compress a representation while keeping what predicts a target. Here the target is a set of tasks, so the bottleneck decides which detail survives ([[02-foundations/information-theory|information theory]]).
> Information Bottleneck: 표적을 예측하는 것은 유지하면서 표현을 압축한다. 여기서 표적이 과제 집합이므로, 병목이 어떤 세부가 살아남을지를 결정한다([[02-foundations/information-theory|정보 이론]]).

## English

**One-line summary**: The right granularity for an object in a map is **not a property of the object — it is a property of the task**, and the Information Bottleneck turns that observation into an algorithm that clusters primitives into task-relevant objects online, on onboard compute.

### Context

Class-agnostic segmentation and open-set semantic understanding made open-vocabulary mapping possible, and immediately raised a question nobody had a principled answer to: **at what granularity should a thing be an object?** Is a bookshelf one node, or is each book a node? [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] has to answer this and answers it by fiat.

### Method

> [!tip] Key intuition
> Ask what the robot has been asked to do. If the task is "bring me the red book", the book is an object and the shelf is context. If the task is "clear the room", the shelf is the object and the books are irrelevant detail. Granularity is a function of the task list, so make the task list an input.

Given a set of natural-language tasks, Clio forms **task-relevant clusters of object primitives** using an Information-Bottleneck formulation, then constructs a **hierarchical 3D scene graph** of the environment **online, using only onboard compute**, as the robot explores. The paper reports improved task-execution accuracy from the semantic filtering that follows.

### Results

Real-time construction on onboard compute, with better task execution than granularity-agnostic mapping.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> "Real-time" and "onboard compute" are the load-bearing systems claims, and they are the ones worth checking against your own hardware before adopting — RA-L papers state them for a specific platform. The accuracy improvement is reported relative to the paper's own baselines; treat it as evidence that task-conditioning helps, not as a portable number.

### Limitations & critique

- **You must know the tasks in advance.** The bottleneck compresses toward a given task set; a task that arrives later may need detail that was already discarded. That is the exact trade the method makes, and it is a real cost, not a detail.
- **Discarding is irreversible in a single pass.** Re-granularising means re-observing.
- **Tasks as natural language inherits language ambiguity.** "Clear the area" does not determine granularity by itself.

### Impact & follow-ups

Clio is the paper that made **granularity a first-class design variable** in robot mapping rather than an implementation accident. For a construction robot the framing is unusually apt: the same site is a different map depending on whether today's task is inspection, delivery, or installation, and a single fixed-granularity map serves none of them well.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation §7]] — the concept page
- [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] — the fixed-granularity predecessor
- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — hierarchical scene graphs in the SLAM lineage
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — where task-dependent granularity would pay

### After reading

- [ ] State the question Clio answers that ConceptGraphs answers by fiat.
- [ ] Explain what the Information Bottleneck is compressing and toward what.
- [ ] Name the cost of task-conditioned compression.
- [ ] Say which of the paper's claims are systems claims and should be re-checked on your hardware.

## 한국어

**한 줄 요약**: 지도에서 물체의 올바른 입도는 **물체의 성질이 아니라 과제의 성질이다.** Information Bottleneck이 그 관찰을, 원시 요소들을 과제와 관련된 물체로 온라인·온보드에서 군집화하는 알고리즘으로 바꾼다.

### 배경

클래스 불가지론적 분할과 개방 집합 의미 이해가 개방 어휘 매핑을 가능하게 했고, 곧바로 아무도 원리적으로 답하지 못한 질문을 낳았다: **무엇을 어느 입도에서 물체로 볼 것인가?** 책장이 노드 하나인가, 책마다 노드인가? [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]]는 이 질문에 답해야 하고, 임의로 답한다.

### 방법

> [!tip] 핵심 직관
> 로봇이 무엇을 하라고 요청받았는지를 물어라. 과제가 "빨간 책을 가져와"라면 책이 물체이고 책장은 맥락이다. 과제가 "방을 비워"라면 책장이 물체이고 책은 무의미한 세부다. 입도는 과제 목록의 함수이므로, 과제 목록을 입력으로 삼아라.

자연어 과제 집합이 주어지면 Clio는 Information Bottleneck 정식화로 **과제 관련 원시 요소 군집**을 만들고, 로봇이 탐색하는 동안 **온보드 연산만으로 온라인에서** 환경의 **계층적 3D 장면 그래프**를 구성한다. 뒤따르는 의미 필터링에서 과제 수행 정확도가 향상된다고 보고한다.

### 결과

온보드 연산 위에서의 실시간 구성, 그리고 입도를 고려하지 않는 매핑보다 나은 과제 수행.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "실시간"과 "온보드 연산"이 무게를 지는 시스템 주장이고, 채택 전에 자기 하드웨어와 대조해 볼 값어치가 있는 것도 그쪽이다 — RA-L 논문은 특정 플랫폼을 기준으로 그것을 진술한다. 정확도 향상은 논문 자신의 베이스라인 대비로 보고된다. 이식 가능한 숫자가 아니라 과제 조건화가 도움이 된다는 증거로 다뤄라.

### 한계와 비판

- **과제를 미리 알아야 한다.** 병목은 주어진 과제 집합 쪽으로 압축한다. 나중에 도착한 과제는 이미 버려진 세부를 필요로 할 수 있다. 그것이 이 방법이 치르는 정확한 교환이고, 세부가 아니라 실제 비용이다.
- **한 번의 통과에서 버림은 되돌릴 수 없다.** 입도를 다시 잡으려면 다시 관측해야 한다.
- **자연어 과제는 언어의 모호성을 물려받는다.** "구역을 정리하라"만으로는 입도가 정해지지 않는다.

### 영향과 후속 연구

Clio는 로봇 매핑에서 **입도를 구현상의 우연이 아니라 일급 설계 변수로** 만든 논문이다. 건설 로봇에는 이 프레이밍이 유난히 잘 맞는다: 같은 현장도 오늘의 과제가 검사인지, 운반인지, 설치인지에 따라 다른 지도이고, 입도가 하나로 고정된 지도는 그 어느 것에도 잘 봉사하지 못한다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션 §7]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] — 입도가 고정된 선행 연구
- [[04-robotics/state-estimation-slam|3. 상태 추정·위치 인식·SLAM]] — SLAM 계보에서의 계층적 장면 그래프
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 과제 의존 입도가 값을 하는 곳

### 읽고 나면 말할 수 있어야 하는 것

- [ ] ConceptGraphs가 임의로 답하는 질문에 Clio가 무엇이라 답하는지 말한다.
- [ ] Information Bottleneck이 무엇을 무엇 쪽으로 압축하는지 설명한다.
- [ ] 과제 조건부 압축의 비용을 댄다.
- [ ] 논문의 주장 중 어느 것이 시스템 주장이고 자기 하드웨어에서 다시 확인해야 하는지 말한다.
