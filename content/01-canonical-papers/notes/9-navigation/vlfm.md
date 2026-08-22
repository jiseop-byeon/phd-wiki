---
title: "VLFM — Vision-Language Frontier Maps for Zero-Shot Semantic Navigation"
authors: Naoki Yokoyama, Sehoon Ha, Dhruv Batra, Jiuguang Wang, Bernadette Bucher
affiliation: Georgia Tech, Boston Dynamics AI Institute
venue: ICRA
year: 2024
arxiv: https://arxiv.org/abs/2312.03275
project: https://naoki.io/portfolio/vlfm
tags: [paper, navigation, objectnav, zero-shot, vlm]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery if open-vocabulary semantic exploration becomes part of the contribution."
---

**Yokoyama, Ha, Batra, Wang & Bucher, ICRA 2024** — [arXiv:2312.03275](https://arxiv.org/abs/2312.03275)

> [!note] Math on-ramp · 수학 준비물
> Frontier-based exploration (the boundary between mapped free space and the unknown), plus SPL as a metric ([[04-robotics/semantic-language-navigation|19. §2]]) and what a pretrained vision-language model scores ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]).
> frontier 기반 탐색(지도로 만든 자유 공간과 미지 영역의 경계), SPL 지표([[04-robotics/semantic-language-navigation|19. §2]]), 그리고 사전학습 시각-언어 모델이 매기는 점수가 무엇인지([[01-canonical-papers/notes/3-vlm/clip|CLIP]]).

## English

**One-line summary**: Keep the classical frontier map, but score each frontier with a **pretrained vision-language model** instead of a learned policy — giving zero-shot object-goal navigation that needs no ObjectNav training at all, and runs on a Spot in a real office.

### Context

[[01-canonical-papers/notes/9-navigation/semexp|SemExp]] learned where to look from data, which means it can only look for categories it was trained on. The question VLFM asks is whether the "where should I look" judgement can be borrowed from a model that already knows how the world is arranged, without any navigation training.

### Method

> [!tip] Key intuition
> A frontier is a *place you could go*. A vision-language model can tell you how much a place looks like it leads to a toilet. Put the second on top of the first and semantic exploration becomes a scoring problem with no learned policy in it.

Three layers, each doing one thing:

| Layer | Input | Output |
|---|---|---|
| Occupancy mapping | depth | frontiers — the boundary of the known |
| Value map | RGB + a pretrained VLM | a **language-grounded** score over space |
| Selection | both | the most promising frontier to explore |

The design is deliberately modular, which is the property [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al. 2023]] identified as the sim-to-real mechanism.

### Results

Evaluated in Habitat on **Gibson, HM3D, and MP3D**, reaching state-of-the-art **SPL** on all three for object-goal navigation. Deployed zero-shot on a **Boston Dynamics Spot** and shown navigating to target objects in a real office building with no prior knowledge of the environment.

> [!warning] Reading the claims · 주장 읽는 법
> **SPL, not success, is the reported metric** — SPL penalises inefficient paths, so a method can lead on SPL while a competitor finds the object more often. Check which one a comparison uses before repeating it. The real-world result is a demonstration ("we deploy and show"), not a measured success rate; the abstract gives no real-world number.
> **보고된 지표는 success가 아니라 SPL이다** — SPL은 비효율적 경로에 벌점을 주므로, 어떤 방법이 SPL에서 앞서면서도 물체를 더 자주 찾는 쪽은 경쟁 방법일 수 있다. 비교를 옮기기 전에 어느 지표인지 확인하라. 실제 환경 결과는 측정된 성공률이 아니라 실증("배포해서 보인다")이고, 초록에 실제 환경 숫자는 없다.

### Limitations & critique

- **Zero-shot on the policy, not on the perception.** Nothing is trained for navigation, but everything depends on what the VLM already encodes — and its priors are internet priors about ordinary indoor scenes.
- **Depth is still required** for the occupancy map, so the sensor gap [[01-canonical-papers/notes/9-navigation/navid|NaVid]] removes is still present here.
- **Frontiers assume connected free space.** In a partially built structure with temporary openings and no floor in places, the frontier abstraction itself gets shaky.
- The value map scores *appearance*, so it inherits the scene-bias problem of [[04-robotics/video-action-understanding|20. §2]] — a place that looks like where a thing should be is not where the thing is.

### Impact & follow-ups

VLFM is the cleanest demonstration that **foundation-model priors can replace task-specific navigation training**, and it is the strongest current argument that the modular pipeline is not a legacy design but the one that gets you onto real hardware fastest.

**For construction**: the open vocabulary is what matters. A site's objects — formwork, a specific valve, a pallet of a specific material — will never be a fixed category set, and a method that needs one is unusable there.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]] — the concept page
- [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] — the learned-prior predecessor
- [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] — open-vocabulary structure in the map rather than in the score
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]] — the source of the language grounding

### After reading

- [ ] Draw the three layers and say what each consumes and produces.
- [ ] Explain what makes this zero-shot, and what part is not zero-shot at all.
- [ ] State which metric the results are on and why that distinction matters.
- [ ] Name the failure mode inherited from scoring appearance.

## 한국어

**한 줄 요약**: 고전적 frontier 지도를 유지하되, 각 frontier의 점수를 학습된 정책이 아니라 **사전학습 시각-언어 모델**로 매긴다. ObjectNav 학습이 전혀 필요 없는 zero-shot 물체 목표 내비게이션이 되고, 실제 사무실에서 Spot 위로 돌아간다.

### 배경

[[01-canonical-papers/notes/9-navigation/semexp|SemExp]]는 어디를 봐야 하는지를 데이터에서 배웠고, 그래서 학습한 범주만 찾을 수 있다. VLFM이 던지는 질문은 "어디를 봐야 하는가"라는 판단을, 세상이 어떻게 배치되는지 이미 아는 모델에서 내비게이션 학습 없이 빌려올 수 있는가다.

### 방법

> [!tip] 핵심 직관
> frontier는 *갈 수 있는 곳*이다. 시각-언어 모델은 어떤 곳이 변기로 이어질 것처럼 보이는 정도를 말해줄 수 있다. 둘째를 첫째 위에 얹으면 의미론적 탐색은 학습된 정책이 하나도 없는 점수 매기기 문제가 된다.

각각 한 가지만 하는 세 계층:

| 계층 | 입력 | 출력 |
|---|---|---|
| 점유 매핑 | 깊이 | frontier — 아는 것의 경계 |
| 가치 지도 | RGB + 사전학습 VLM | 공간 위의 **언어에 접지된** 점수 |
| 선택 | 둘 다 | 탐색할 가장 유망한 frontier |

설계가 의도적으로 모듈형이고, 그것이 [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등 2023]]이 sim-to-real 기구로 지목한 성질이다.

### 결과

Habitat의 **Gibson, HM3D, MP3D**에서 평가해 물체 목표 내비게이션 **SPL** 기준 세 데이터셋 모두에서 state-of-the-art. **Boston Dynamics Spot**에 zero-shot으로 배포해, 사전 지식 없는 실제 사무실 건물에서 목표 물체까지 주행하는 것을 보인다.

> [!warning] 주장 읽는 법 · Reading the claim
> **보고된 지표는 success가 아니라 SPL이다** — SPL은 비효율적 경로에 벌점을 주므로, 어떤 방법이 SPL에서 앞서면서도 물체를 더 자주 찾는 쪽은 경쟁 방법일 수 있다. 비교를 옮기기 전에 어느 지표인지 확인하라. 실제 환경 결과는 측정된 성공률이 아니라 실증이고, 초록에 실제 환경 숫자는 없다.
> The reported metric is SPL, not success rate, and the real-world result is a demonstration rather than a measurement.

### 한계와 비판

- **zero-shot인 것은 정책이지 인지가 아니다.** 내비게이션을 위해 학습된 것은 없지만, 모든 것이 VLM이 이미 부호화한 것에 의존한다. 그리고 그 사전지식은 평범한 실내 장면에 대한 인터넷 사전지식이다.
- **깊이는 여전히 필요하다.** 점유 지도를 위해서다. 그러니 [[01-canonical-papers/notes/9-navigation/navid|NaVid]]가 없앤 센서 격차가 여기에는 그대로 남아 있다.
- **frontier는 연결된 자유 공간을 전제한다.** 임시 개구부가 있고 바닥이 없는 곳도 있는 시공 중 구조물에서는 frontier 추상 자체가 흔들린다.
- 가치 지도는 *외형*에 점수를 매기므로 [[04-robotics/video-action-understanding|20. §2]]의 장면 편향 문제를 물려받는다 — 무언가가 있을 법해 *보이는* 곳이 그것이 있는 곳은 아니다.

### 영향과 후속 연구

VLFM은 **파운데이션 모델의 사전지식이 과제별 내비게이션 학습을 대체할 수 있다**는 것을 가장 깔끔하게 보인 사례이고, 모듈형 파이프라인이 유산 설계가 아니라 실제 하드웨어에 가장 빨리 올라가는 설계라는 현재로선 가장 강한 논증이다.

**건설의 경우**: 중요한 것은 개방 어휘다. 현장의 물체 — 거푸집, 특정 밸브, 특정 자재 한 팔레트 — 는 결코 고정된 범주 집합이 되지 않을 것이고, 그것을 요구하는 방법은 현장에서 쓸 수 없다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] — 학습된 사전지식을 쓴 선행 연구
- [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] — 점수가 아니라 지도의 구조에 개방 어휘를 넣는 방식
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]] — 언어 접지의 원천

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 세 계층을 그리고 각각이 무엇을 먹고 무엇을 내놓는지 말한다.
- [ ] 무엇이 이것을 zero-shot으로 만들며, 어느 부분은 전혀 zero-shot이 아닌지 설명한다.
- [ ] 결과가 어느 지표 위에 있고 그 구분이 왜 중요한지 말한다.
- [ ] 외형에 점수를 매기는 데서 물려받은 실패 양상을 댄다.
