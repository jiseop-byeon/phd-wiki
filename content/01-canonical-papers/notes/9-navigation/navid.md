---
title: "NaVid — Video-based VLM Plans the Next Step for Vision-and-Language Navigation"
authors: Jiazhao Zhang, Kunyu Wang, Rongtao Xu, Gengze Zhou, Yicong Hong, Xiaomeng Fang, Qi Wu, Zhizheng Zhang, He Wang
affiliation: Peking University, Galbot, University of Adelaide, Beijing Academy of Artificial Intelligence
venue: RSS
year: 2024
arxiv: https://arxiv.org/abs/2402.15852
project: https://pku-epic.github.io/NaVid/
tags: [paper, navigation, vln, vlm, sim-to-real]
status: note-complete
last_verified: 2026-08-22
study-depth: Literacy
wiki-support: Working
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if a video-conditioned VLM becomes the policy class in the thesis."
---

**Zhang et al., RSS 2024** — [arXiv:2402.15852](https://arxiv.org/abs/2402.15852) · [Project](https://pku-epic.github.io/NaVid/)

> [!note] Math on-ramp · 수학 준비물
> What a video-conditioned VLM is and why the history matters ([[04-robotics/video-action-understanding|20. §3]]), plus the VLN-CE setting ([[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]]).
> 비디오 조건부 VLM이 무엇이고 이력이 왜 중요한지([[04-robotics/video-action-understanding|20. §3]]), 그리고 VLN-CE 설정([[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]]).

## English

**One-line summary**: Feed a monocular RGB video stream and an instruction to a video-based VLM and have it emit the next action directly — **no map, no odometry, no depth** — which removes the sim-to-real gaps those inputs carry.

### Context

VLN's chronic problem is generalisation, both to out-of-distribution scenes and from sim to real. The paper's diagnosis locates the failure in the *inputs*: odometry has noise, and maps and depth carry their own sim-to-real gaps. A policy built on them inherits all of it.

### Method

> [!tip] Key intuition
> Remove the inputs that do not survive the transfer. If the only input is what a camera sees, the only gap left is the visual one — and that is the gap foundation-model pretraining is best at absorbing.

NaVid takes only an **on-the-fly video stream from a monocular RGB camera** and outputs the next-step action. The video formulation is doing two jobs at once: it encodes the robot's historical observations as spatio-temporal context for decision making, which is what replaces the map.

Training data: **510k navigation samples** collected from continuous environments — split between action-planning and instruction-reasoning samples — plus **763k large-scale web data**.

### Results

**What it measured.** Per the [abstract](https://arxiv.org/abs/2402.15852): Training combines 510k navigation samples with 763k web-data samples. These quantify the training mixture; the abstract gives no numerical navigation-success or transfer advantage.

The paper claims state-of-the-art performance in simulation and the real world, with superior cross-dataset and sim-to-real transfer, and states it is **the first** to reach state-of-the-art navigation without maps, odometers, or depth.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> The quantified claims in the abstract are the **data volumes**, not the performance — 510k navigation samples and 763k web samples are stated exactly, while "state-of-the-art" and "superior transfer" are not. Note also that the 763k web samples are how the model gets its generality, which means the recipe is only reproducible by someone who can assemble comparable web data.

### Limitations & critique

- **No map means no memory beyond the context window.** Spatio-temporal context is bounded by how much video the model can attend over; a long search in a large building exceeds it.
- **Removing depth removes metric scale.** For navigation among obstacles that is survivable. For anything that has to reach or place — the mobile-manipulation problem of [[04-robotics/navigation-mobile-manipulation|16]] — it is not.
- **Latency.** A large VLM in the control loop is a very different timing budget from a policy network, and the abstract does not report inference rate.
- The end-to-end family is exactly the one [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al. 2023]] found collapsing in real homes. NaVid claims to have solved that; the claim deserves the same style of independent, in-the-wild test rather than acceptance.

### Impact & follow-ups

NaVid is the reference point for "VLM as the navigation policy itself", and [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] extends the same architecture to unify several navigation tasks in one model.

### Connections

- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]] — the concept page
- [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] — the setting it is evaluated in
- [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] — the unified successor
- [[01-canonical-papers/notes/4-vla/pi0|π0]] — the manipulation analogue of a large pretrained model as policy

### After reading

- [ ] Name the three inputs NaVid deliberately does without, and the gap each one carries.
- [ ] Explain what the video history replaces.
- [ ] State which of the abstract's claims are quantified.
- [ ] Say what limits how far this can search.

## 한국어

**한 줄 요약**: 단안 RGB 비디오 스트림과 지시문을 비디오 기반 VLM에 넣고 다음 행동을 바로 내놓게 한다 — **지도도, 오도메트리도, 깊이도 없이**. 그 입력들이 데리고 오는 sim-to-real 격차를 함께 없앤다.

### 배경

VLN의 만성적 문제는 일반화다. 분포 밖 장면으로도, 시뮬레이션에서 현실로도. 이 논문의 진단은 실패의 자리를 *입력*에서 찾는다: 오도메트리에는 잡음이 있고, 지도와 깊이는 각자의 sim-to-real 격차를 갖고 있다. 그 위에 세운 정책은 그것을 전부 물려받는다.

### 방법

> [!tip] 핵심 직관
> 전이에서 살아남지 못하는 입력을 없애라. 유일한 입력이 카메라가 보는 것이라면 남는 격차는 시각적인 것뿐이고, 그것이 파운데이션 모델 사전학습이 가장 잘 흡수하는 격차다.

NaVid는 **단안 RGB 카메라의 실시간 비디오 스트림**만 받아 다음 행동을 출력한다. 비디오 정식화가 두 가지 일을 동시에 한다: 로봇의 과거 관측을 의사결정을 위한 시공간 맥락으로 부호화하고, 그것이 지도를 대신한다.

학습 데이터: 연속 환경에서 모은 **내비게이션 표본 51만** — 행동 계획 표본과 지시 추론 표본으로 나뉜다 — 그리고 **대규모 웹 데이터 76.3만**.

### 결과

**무엇을 쟀는가.** [초록](https://arxiv.org/abs/2402.15852) 기준: 학습은 항법 표본 510k개와 웹 데이터 표본 763k개를 결합한다. 학습 혼합의 규모이며 초록에 항법 성공이나 전이 우위의 수치는 없다.

시뮬레이션과 실제 환경 모두에서 state-of-the-art 성능, 우수한 교차 데이터셋·sim-to-real 전이를 주장하고, 지도·오도미터·깊이 없이 state-of-the-art 내비게이션에 도달한 **최초**라고 진술한다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 초록에서 정량화된 주장은 성능이 아니라 **데이터 규모**다 — 내비게이션 표본 51만과 웹 데이터 76.3만은 정확히 진술되지만, "state-of-the-art"와 "우수한 전이"는 그렇지 않다. 76.3만 웹 표본이 모델의 일반성을 만든다는 점도 짚어야 한다. 비슷한 웹 데이터를 모을 수 있는 사람만 이 레시피를 재현할 수 있다는 뜻이다.

### 한계와 비판

- **지도가 없다는 것은 문맥 창 너머의 기억이 없다는 뜻이다.** 시공간 맥락은 모델이 주의를 줄 수 있는 비디오 길이에 묶인다. 큰 건물에서의 긴 탐색은 그것을 넘어선다.
- **깊이를 없애면 미터 스케일이 사라진다.** 장애물 사이 주행에는 견딜 만하다. 뻗거나 놓아야 하는 것 — [[04-robotics/navigation-mobile-manipulation|16]]의 모바일 매니퓰레이션 문제 — 에는 아니다.
- **지연.** 큰 VLM을 제어 루프에 넣는 것은 정책 네트워크와 전혀 다른 타이밍 예산이고, 초록은 추론 속도를 보고하지 않는다.
- end-to-end 계열은 정확히 [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등 2023]]이 실제 주택에서 무너지는 것을 확인한 그 계열이다. NaVid는 그것을 풀었다고 주장하는데, 그 주장은 수용이 아니라 같은 방식의 독립적 야외 시험을 받아야 한다.

### 영향과 후속 연구

NaVid는 "VLM 자체가 내비게이션 정책"의 기준점이고, [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]]가 같은 구조를 확장해 여러 내비게이션 과제를 한 모델로 통합한다.

### 연결

- [[04-robotics/semantic-language-navigation|19. 의미·언어 기반 내비게이션]] — 개념 페이지
- [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] — 평가가 이루어지는 설정
- [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] — 통합된 후속
- [[01-canonical-papers/notes/4-vla/pi0|π0]] — 큰 사전학습 모델을 정책으로 쓰는 매니퓰레이션 쪽 대응물

### 읽고 나면 말할 수 있어야 하는 것

- [ ] NaVid가 의도적으로 쓰지 않는 입력 셋과 각각이 데리고 오는 격차를 댄다.
- [ ] 비디오 이력이 무엇을 대신하는지 설명한다.
- [ ] 초록의 주장 중 정량화된 것을 말한다.
- [ ] 이 방법이 얼마나 멀리 탐색할 수 있는지를 무엇이 제한하는지 말한다.
