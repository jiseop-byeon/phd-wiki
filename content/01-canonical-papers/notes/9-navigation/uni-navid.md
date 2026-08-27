---
title: "Uni-NaVid — A Video-based Vision-Language-Action Model for Unifying Embodied Navigation Tasks"
authors: Jiazhao Zhang, Kunyu Wang, Shaoan Wang, Minghan Li, Haoran Liu, Songlin Wei, Zhongyuan Wang, Zhizheng Zhang, He Wang
affiliation: Peking University, Galbot, Beijing Academy of Artificial Intelligence
venue: RSS
year: 2025
arxiv: https://arxiv.org/abs/2412.06224
project: https://pku-epic.github.io/Uni-NaVid/
tags: [paper, navigation, vla, vln, objectnav, generalist]
status: note-complete
last_verified: 2026-08-22
study-depth: Literacy
wiki-support: Working
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if task unification across navigation modes becomes part of the architecture."
---

**Zhang et al., RSS 2025** — [arXiv:2412.06224](https://arxiv.org/abs/2412.06224) · [Project](https://pku-epic.github.io/Uni-NaVid/)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/9-navigation/navid|NaVid]] first — this is the same architecture asked to do more. Then the VLA framing of [[01-canonical-papers/notes/4-vla/rt-2|RT-2]]: one model, many tasks, actions as outputs.
> 먼저 [[01-canonical-papers/notes/9-navigation/navid|NaVid]] — 같은 구조에 더 많은 일을 시킨 것이다. 그다음 [[01-canonical-papers/notes/4-vla/rt-2|RT-2]]의 VLA 프레이밍: 하나의 모델, 여러 과제, 출력으로서의 행동.

## English

**One-line summary**: Harmonise the input and output formats of the common navigation tasks — instruction following, object search, question answering, person following — so a single video-based VLA can do all of them, including mixed long-horizon tasks in unseen real environments.

### Context

A practical navigation agent has to handle a range of interaction demands, and existing embodied-navigation models fall short as generalists because they are tied to a specific task configuration or to pre-defined maps with discretised waypoints. The fragmentation is not only inconvenient; it means each task's data cannot help the others.

### Method

Uni-NaVid is presented as **the first video-based VLA model** unifying diverse embodied navigation tasks. The mechanism is stated plainly: **harmonise the input and output data configurations** for all commonly used navigation tasks, and thereby integrate them in one model. Training uses **3.6 million navigation data samples** drawn from four essential navigation sub-tasks, with the explicit aim of fostering **synergy in learning across them** — that cross-task synergy is the paper's actual scientific claim, distinct from the engineering claim of unification.

### Results

State-of-the-art performance on comprehensive navigation benchmarks, plus real-world experiments confirming effectiveness and efficiency.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> Again the only exact number in the abstract is a **data volume — 3.6 M samples**. "State-of-the-art" is unquantified, "efficiency" is asserted without a rate, and the real-world experiments are described but not sized. Also weigh the claim structure: unification papers can post SOTA on a benchmark suite while being worse than the specialist on any single one. Check the per-task table in the body before repeating the headline.

### Limitations & critique

- **Unification is a claim about interfaces, not about capability.** Making four tasks share an input format is engineering; showing they help each other is the science, and it is the part that needs the ablation.
- **Inherits NaVid's limits.** No map, no depth, bounded context — see [[01-canonical-papers/notes/9-navigation/navid|NaVid]]'s critique section, which applies unchanged.
- **The four sub-tasks are the world.** Anything outside instruction following, object search, question answering and person following is not unified, and adding a fifth means retraining.

### Impact & follow-ups

Uni-NaVid is the navigation counterpart of the generalist turn that [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] and [[01-canonical-papers/notes/4-vla/pi0|π0]] represent in manipulation, and it is the paper to cite for "one model, many navigation tasks". Person-following is the sub-task most directly relevant to a construction robot that must accompany a worker rather than merely avoid them ([[04-robotics/hri-safety|11]]).

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]] — the concept page
- [[01-canonical-papers/notes/9-navigation/navid|NaVid]] — the single-task predecessor
- [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] — the generalist argument in manipulation
- [[04-robotics/hri-safety|11. Human–Robot Interaction & Safety]] — where person-following becomes a safety question

### After reading

- [ ] State the mechanism by which four tasks become one model.
- [ ] Separate the paper's engineering claim from its scientific one.
- [ ] Say what number the abstract actually gives you.
- [ ] Name which sub-task matters most for a site robot and why.

## 한국어

**한 줄 요약**: 흔히 쓰는 내비게이션 과제들 — 지시 따르기, 물체 탐색, 질의응답, 사람 추종 — 의 입출력 형식을 통일해서, 하나의 비디오 기반 VLA가 그 전부를 하게 만든다. 처음 보는 실제 환경에서의 혼합 장기 과제까지 포함해서.

### 배경

실용적인 내비게이션 에이전트는 다양한 상호작용 요구를 감당해야 하는데, 기존의 체화 내비게이션 모델들은 특정 과제 설정이나 이산화된 웨이포인트가 있는 사전 지도에 묶여 있어 범용 에이전트가 되지 못한다. 이 파편화는 불편하기만 한 것이 아니다. 각 과제의 데이터가 다른 과제를 돕지 못한다는 뜻이다.

### 방법

Uni-NaVid는 다양한 체화 내비게이션 과제를 통합하는 **최초의 비디오 기반 VLA 모델**로 제시된다. 기구는 평이하게 진술된다: 흔히 쓰는 모든 내비게이션 과제의 **입출력 데이터 구성을 조화시켜** 하나의 모델로 통합한다. 학습에는 네 개의 핵심 하위 과제에서 뽑은 **내비게이션 데이터 360만 표본**을 쓰고, **그들 사이의 학습 시너지를 키우는 것**을 명시적 목표로 삼는다 — 그 교차 과제 시너지가 논문의 실제 과학적 주장이고, 통합이라는 공학적 주장과는 구별된다.

### 결과

포괄적 내비게이션 벤치마크에서 state-of-the-art 성능, 그리고 효과와 효율을 확인하는 실제 환경 실험.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 여기서도 초록의 유일한 정확한 숫자는 **데이터 규모 — 360만 표본**이다. "state-of-the-art"는 정량화되지 않았고, "효율"은 속도 없이 주장되며, 실제 환경 실험은 기술되지만 규모가 밝혀지지 않는다. 주장 구조도 저울질하라: 통합 논문은 벤치마크 묶음에서 SOTA를 찍으면서도 개별 과제에서는 전문 모델보다 나쁠 수 있다. 헤드라인을 옮기기 전에 본문의 과제별 표를 확인하라.

### 한계와 비판

- **통합은 인터페이스에 대한 주장이지 능력에 대한 주장이 아니다.** 네 과제가 입력 형식을 공유하게 만드는 것은 공학이고, 그들이 서로 돕는다는 것을 보이는 것이 과학이며, 절제 실험이 필요한 부분이 그쪽이다.
- **NaVid의 한계를 물려받는다.** 지도 없음, 깊이 없음, 유한한 문맥 — [[01-canonical-papers/notes/9-navigation/navid|NaVid]]의 비판 절이 그대로 적용된다.
- **네 하위 과제가 곧 세계다.** 지시 따르기·물체 탐색·질의응답·사람 추종 밖의 것은 통합되지 않았고, 다섯 번째를 더하려면 재학습해야 한다.

### 영향과 후속 연구

Uni-NaVid는 매니퓰레이션에서 [[01-canonical-papers/notes/4-vla/rt-2|RT-2]]와 [[01-canonical-papers/notes/4-vla/pi0|π0]]가 대표하는 범용화 전환의 내비게이션 대응물이고, "하나의 모델, 여러 내비게이션 과제"로 인용할 논문이다. 사람 추종은, 작업자를 피하기만 하는 것이 아니라 동행해야 하는 건설 로봇에 가장 직접적으로 관련된 하위 과제다([[04-robotics/hri-safety|11]]).

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/navid|NaVid]] — 단일 과제 선행 연구
- [[01-canonical-papers/notes/4-vla/rt-2|RT-2]] — 매니퓰레이션에서의 범용화 논증
- [[04-robotics/hri-safety|11. 인간-로봇 상호작용과 안전]] — 사람 추종이 안전 문제가 되는 지점

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 네 과제가 하나의 모델이 되는 기구를 말한다.
- [ ] 논문의 공학적 주장과 과학적 주장을 가른다.
- [ ] 초록이 실제로 주는 숫자가 무엇인지 말한다.
- [ ] 현장 로봇에 가장 중요한 하위 과제와 그 이유를 댄다.
