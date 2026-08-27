---
title: "ConceptGraphs — Open-Vocabulary 3D Scene Graphs for Perception and Planning"
authors: Qiao Gu, Alihusein Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula, et al.
affiliation: University of Toronto, Université de Montréal / Mila, MIT, JHU APL, US Army Research Laboratory
venue: ICRA
year: 2024
arxiv: https://arxiv.org/abs/2309.16650
project: https://concept-graphs.github.io/
tags: [paper, navigation, mapping, scene-graph, open-vocabulary]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if the map representation is something the thesis designs rather than consumes."
---

**Gu, Kuwajerwala, Morin, Jatavallabhula et al., ICRA 2024** — [arXiv:2309.16650](https://arxiv.org/abs/2309.16650) · [Project](https://concept-graphs.github.io/)

> [!note] Math on-ramp · 수학 준비물
> Multi-view association — fusing 2D detections across frames into one 3D entity ([[04-robotics/geometric-perception-calibration|3.5 §4]]) — and the difference between a per-point feature field and a graph of objects.
> 다중 시점 결합 — 프레임에 걸친 2D 검출을 하나의 3D 개체로 융합하기([[04-robotics/geometric-perception-calibration|3.5 §4]]) — 그리고 점별 특징 장과 물체 그래프의 차이.

## English

**One-line summary**: Build the map as a **graph of objects with edges between them**, each node carrying open-vocabulary semantics fused from 2D foundation models — compact where per-point feature maps are not, and structured in a way a planner can actually query.

### Context

The previous generation of semantic maps attached a feature vector to every point. Two problems, both named in the abstract: those maps **do not scale to larger environments**, and they contain **no semantic spatial relationships between entities** — and relationships are exactly what a language-specified task needs. "The box on the pallet by the door" is a query about edges, not about points.

### Method

Build from **2D foundation models** and fuse their output into 3D by **multi-view association**. Nodes are objects; edges are relations. Because the semantics come from 2D models that already generalise, the representation **generalises to novel semantic classes without collecting large 3D datasets or finetuning** — that clause is the practical heart of the paper.

### Results

Utility is demonstrated through downstream planning tasks specified by **abstract language prompts** requiring complex reasoning over spatial and semantic concepts.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> **The abstract contains no numbers at all** — no map size, no query accuracy, no comparison. It is a representation paper, and its evidence is demonstrated capability on downstream tasks. That is legitimate, but it means there is nothing here to cite as a measurement. When you need one, you need the body.

### Limitations & critique

- **Association is the failure point.** Everything rests on deciding that this detection and that detection are the same object across views. Repeated identical objects — a stack of identical panels, a row of identical bolts — is the adversarial case, and construction sites are made of exactly that.
- **Objects, not stuff.** A graph of discrete objects handles a chair well and handles poured concrete, rebar mesh, or a partially built wall badly. There is no clean node boundary for continuous material.
- **Static.** The graph describes a scene; a site changes every day, and nothing in the representation is about how to update or expire a node.
- **Open-vocabulary is only as open as the 2D model.** Domain-specific vocabulary that CLIP-family models never saw is not rescued by putting it into a graph.

### Impact & follow-ups

ConceptGraphs made the object-graph the default for open-vocabulary mapping, and [[01-canonical-papers/notes/9-navigation/clio|Clio]] answered the question it leaves open — *at what granularity should an object be a node* — by making that choice task-dependent rather than fixed.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation §7]] — the concept page's language-queryable-map section
- [[01-canonical-papers/notes/9-navigation/clio|Clio]] — task-driven granularity
- [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] — open vocabulary in the score instead of the structure
- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — the mapping machinery underneath

### After reading

- [ ] Name the two problems with per-point semantic feature maps that this fixes.
- [ ] Explain why multi-view association is the load-bearing step.
- [ ] Say what kind of scene content the object-graph abstraction handles badly.
- [ ] State what evidence the paper offers and what it does not.

## 한국어

**한 줄 요약**: 지도를 **물체 노드와 그 사이 간선으로 이루어진 그래프**로 만든다. 각 노드는 2D 파운데이션 모델에서 융합한 개방 어휘 의미를 담는다. 점별 특징 지도와 달리 압축적이고, 계획기가 실제로 질의할 수 있는 구조를 가진다.

### 배경

이전 세대의 의미 지도는 모든 점에 특징 벡터를 붙였다. 초록이 지목하는 문제가 둘이다: 그런 지도는 **큰 환경으로 확장되지 않고**, **개체 사이의 의미론적 공간 관계를 담지 않는다** — 그런데 언어로 지정된 과제가 필요로 하는 것이 바로 관계다. "문 옆 팔레트 위의 상자"는 점이 아니라 간선에 대한 질의다.

### 방법

**2D 파운데이션 모델**에서 출발해 그 출력을 **다중 시점 결합**으로 3D에 융합한다. 노드는 물체, 간선은 관계다. 의미가 이미 일반화되는 2D 모델에서 오기 때문에, 이 표현은 **큰 3D 데이터셋을 모으거나 미세조정하지 않고도 새로운 의미 범주로 일반화된다** — 그 구절이 이 논문의 실용적 핵심이다.

### 결과

공간·의미 개념에 걸친 복잡한 추론을 요구하는 **추상적 언어 프롬프트**로 지정된 하류 계획 과제들로 유용성을 실증한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> **초록에 숫자가 하나도 없다** — 지도 크기도, 질의 정확도도, 비교도 없다. 표현에 관한 논문이고 증거는 하류 과제에서 실증된 능력이다. 정당한 형태지만, 측정치로 인용할 것이 여기에 없다는 뜻이기도 하다. 필요하면 본문으로 가야 한다.

### 한계와 비판

- **결합이 실패 지점이다.** 모든 것이 "이 검출과 저 검출이 시점을 가로질러 같은 물체다"라는 판단 위에 서 있다. 똑같은 물체가 반복되는 경우 — 동일한 패널 더미, 동일한 볼트 줄 — 가 적대적 사례이고, 건설 현장은 정확히 그런 것들로 이루어져 있다.
- **물체는 되고 재료는 안 된다.** 이산적 물체의 그래프는 의자는 잘 다루지만 타설 콘크리트, 배근 메시, 시공 중인 벽은 잘 다루지 못한다. 연속적인 재료에는 깔끔한 노드 경계가 없다.
- **정적이다.** 그래프는 한 장면을 기술한다. 현장은 매일 바뀌는데, 노드를 어떻게 갱신하거나 만료시킬지에 대한 것은 이 표현에 없다.
- **개방 어휘는 2D 모델만큼만 열려 있다.** CLIP 계열이 본 적 없는 도메인 특유의 어휘는 그래프에 넣는다고 구제되지 않는다.

### 영향과 후속 연구

ConceptGraphs는 물체 그래프를 개방 어휘 매핑의 기본값으로 만들었고, [[01-canonical-papers/notes/9-navigation/clio|Clio]]가 이 논문이 열어둔 질문 — *물체를 어느 입도에서 노드로 삼아야 하는가* — 에 그 선택을 고정하지 않고 과제에 의존하게 만드는 것으로 답했다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션 §7]] — 개념 페이지의 언어 질의 지도 절
- [[01-canonical-papers/notes/9-navigation/clio|Clio]] — 과제 주도 입도
- [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] — 구조가 아니라 점수에 개방 어휘를 넣는 방식
- [[04-robotics/state-estimation-slam|3. 상태 추정·위치 인식·SLAM]] — 그 아래의 매핑 기구

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 이것이 고치는 점별 의미 특징 지도의 두 문제를 댄다.
- [ ] 다중 시점 결합이 왜 무게를 지는 단계인지 설명한다.
- [ ] 물체 그래프 추상이 잘 다루지 못하는 장면 내용이 무엇인지 말한다.
- [ ] 논문이 제시하는 증거와 제시하지 않는 증거를 말한다.
