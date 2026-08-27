---
title: "Beyond the Nav-Graph — Vision-and-Language Navigation in Continuous Environments"
authors: Jacob Krantz, Erik Wijmans, Arjun Majumdar, Dhruv Batra, Stefan Lee
affiliation: Oregon State University, Georgia Tech, Facebook AI Research
venue: ECCV
year: 2020
arxiv: https://arxiv.org/abs/2004.02857
project: https://jacobkrantz.github.io/vlnce/
tags: [paper, navigation, vln, benchmark, evaluation]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when the thesis argues about what a benchmark's assumptions hide."
---

**Krantz, Wijmans, Majumdar, Batra & Lee, ECCV 2020** — [arXiv:2004.02857](https://arxiv.org/abs/2004.02857) · [Project](https://jacobkrantz.github.io/vlnce/)

> [!note] Math on-ramp · 수학 준비물
> The distinction between a *nav-graph* setting — teleporting between panorama nodes along known navigable edges — and a continuous one, where the agent emits low-level actions ([[04-robotics/semantic-language-navigation|19. §5]]).
> *nav-graph* 설정 — 알려진 이동 가능 간선을 따라 파노라마 노드 사이를 순간이동 — 과 저수준 행동을 내놓는 연속 환경의 차이([[04-robotics/semantic-language-navigation|19. §5]]).

## English

**One-line summary**: Re-pose vision-and-language navigation in a continuous 3D environment with low-level actions, and the field's numbers fall — showing that performance on the old nav-graph benchmark was **inflated by strong implicit assumptions**.

### Context

Vision-and-language navigation had been evaluated on a sparse graph of panoramas with edges marking navigability. That representation smuggles in three assumptions at once, and the paper names them precisely: **known environment topology, short-range oracle navigation, and perfect agent localization.** None of the three survives on a robot.

### Method

> [!tip] Key intuition
> Do not build a better agent. Remove the assumptions and re-measure. The result is a statement about the *benchmark*, and that is a rarer and more useful kind of contribution than a leaderboard step.

The authors define the task in a continuous 3D environment where agents must execute **low-level actions** to follow natural-language directions, then port over models mirroring the advances made in the graph setting, plus single-modality baselines. The single-modality baselines matter: they measure how much of the task can be solved without actually using the language.

### Results

Some techniques transfer. But absolute performance is **significantly lower** in the continuous setting, supporting the paper's conclusion: performance in prior nav-graph settings **may be inflated by the strong implicit assumptions**.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> **The abstract states no numbers** — the claim is comparative and qualitative ("significantly lower"). Cite it for the *structure* of the argument, not for a magnitude. And note what the result does not say: it does not say the graph benchmark measured nothing, only that its number does not survive the removal of assumptions the deployment setting also removes.
> **초록에 숫자가 없다** — 주장은 비교적이고 정성적이다("현저히 낮다"). 크기가 아니라 논증의 *구조*로 인용하라. 결과가 말하지 *않는* 것도 짚어야 한다: 그래프 벤치마크가 아무것도 재지 않았다는 말이 아니라, 배포 환경도 똑같이 제거하는 가정들을 제거하면 그 숫자가 살아남지 않는다는 말이다.

### Limitations & critique

- **Continuous is still simulated.** Removing the graph does not remove the renderer. The image domain gap that [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al.]] measured is untouched by this change.
- **Harder is not automatically better.** A benchmark can be more realistic and still fail to correlate with deployment; VLN-CE argues the first and does not demonstrate the second.
- **Instructions are still human-authored for a simulator.** The language distribution reflects annotators describing rendered houses, not people directing a robot at work.

### Impact & follow-ups

VLN-CE became the standard VLN setting, and [[01-canonical-papers/notes/9-navigation/navid|NaVid]] and [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] are both evaluated on it. Beyond navigation, it is the wiki's cleanest example of a paper whose contribution is **dismantling a benchmark's hidden assumptions** — the move [[04-robotics/semantic-language-navigation|19. §5]] and [[06-research-practice/simulators-benchmarks-datasets|7]] both teach.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation §5]] — the concept page's VLN treatment
- [[01-canonical-papers/notes/9-navigation/navid|NaVid]] — a modern agent evaluated in this setting
- [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al. 2023]] — the same dismantling move, one level further out

### After reading

- [ ] Name the three assumptions the nav-graph setting hides.
- [ ] Explain why single-modality baselines belong in this paper.
- [ ] State what the result establishes about the old benchmark, precisely.
- [ ] Say what this change does *not* fix.

## 한국어

**한 줄 요약**: 시각-언어 내비게이션을 저수준 행동이 있는 연속 3D 환경으로 다시 세우자 분야의 숫자들이 떨어진다 — 기존 nav-graph 벤치마크의 성능이 **강한 암묵적 가정들로 부풀려져 있었음**을 보인다.

### 배경

시각-언어 내비게이션은 이동 가능성을 표시한 간선으로 이어진 성긴 파노라마 그래프 위에서 평가되어 왔다. 그 표현은 세 가지 가정을 한꺼번에 밀반입하고, 논문은 그것을 정확히 지목한다: **알려진 환경 위상, 근거리 오라클 내비게이션, 완벽한 자기 위치 추정.** 셋 다 실제 로봇에서는 살아남지 않는다.

### 방법

> [!tip] 핵심 직관
> 더 나은 에이전트를 만들지 마라. 가정을 제거하고 다시 재라. 그 결과는 *벤치마크*에 대한 진술이고, 리더보드 한 칸보다 드물고 쓸모 있는 종류의 기여다.

저자들은 에이전트가 자연어 지시를 따르기 위해 **저수준 행동**을 실행해야 하는 연속 3D 환경으로 과제를 정의하고, 그래프 설정에서의 진전을 반영한 모델들과 단일 모달리티 베이스라인을 옮겨온다. 단일 모달리티 베이스라인이 중요하다: 언어를 실제로 쓰지 않고도 과제의 얼마가 풀리는지를 재기 때문이다.

### 결과

일부 기법은 전이된다. 그러나 연속 환경에서 절대 성능이 **현저히 낮고**, 이것이 논문의 결론을 뒷받침한다: 기존 nav-graph 설정의 성능이 **강한 암묵적 가정으로 부풀려져 있을 수 있다**.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> **초록에 숫자가 없다** — 주장은 비교적이고 정성적이다("현저히 낮다"). 크기가 아니라 논증의 *구조*로 인용하라. 결과가 말하지 *않는* 것도 짚어야 한다: 그래프 벤치마크가 아무것도 재지 않았다는 말이 아니라, 배포 환경도 똑같이 제거하는 가정들을 제거하면 그 숫자가 살아남지 않는다는 말이다.
> The abstract states no numbers; the claim is comparative and qualitative.

### 한계와 비판

- **연속이어도 여전히 시뮬레이션이다.** 그래프를 없앤다고 렌더러가 없어지지 않는다. [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등]]이 측정한 이미지 도메인 격차는 이 변경으로 건드려지지 않는다.
- **어렵다고 자동으로 나은 것은 아니다.** 벤치마크는 더 현실적이면서도 배포와 상관하지 않을 수 있다. VLN-CE는 앞의 것을 논증하고 뒤의 것은 실증하지 않는다.
- **지시문은 여전히 시뮬레이터를 보고 사람이 쓴 것이다.** 언어 분포는 렌더링된 집을 묘사하는 주석자들을 반영하지, 일하는 로봇에게 지시하는 사람들을 반영하지 않는다.

### 영향과 후속 연구

VLN-CE는 표준 VLN 설정이 되었고, [[01-canonical-papers/notes/9-navigation/navid|NaVid]]와 [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]]가 모두 이 위에서 평가된다. 내비게이션을 넘어, **벤치마크의 숨은 가정을 해체하는** 것이 기여인 논문의 가장 깔끔한 예이기도 하다 — [[04-robotics/semantic-language-navigation|19. §5]]와 [[06-research-practice/simulators-benchmarks-datasets|7]]이 함께 가르치는 동작이다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션 §5]] — 개념 페이지의 VLN 부분
- [[01-canonical-papers/notes/9-navigation/navid|NaVid]] — 이 설정에서 평가되는 현대적 에이전트
- [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등 2023]] — 한 단계 더 바깥에서 같은 해체를 수행한 연구

### 읽고 나면 말할 수 있어야 하는 것

- [ ] nav-graph 설정이 감추는 세 가정을 댄다.
- [ ] 단일 모달리티 베이스라인이 왜 이 논문에 있어야 하는지 설명한다.
- [ ] 이 결과가 기존 벤치마크에 대해 정확히 무엇을 확립하는지 말한다.
- [ ] 이 변경이 고치지 *않는* 것을 말한다.
