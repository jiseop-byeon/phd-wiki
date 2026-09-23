---
title: 4. VLA
study-depth: Literacy
depth-goal: "Use this map or guide to choose reading order, reading volume, and evidence checks."
mastery-when: "Working and Mastery are assigned on the individual concept or paper pages."
---


## English

Robot foundation models — RT-1 through GR00T N1. This page is the map; the reading order is
in the [[01-canonical-papers/canonical-list|canonical list]].

### 1. The axis the papers actually differ on

Read the notes below in date order and they look like a sequence of bigger models. That is not
what separates them. Zhong et al.'s survey ([arXiv:2507.01925](https://arxiv.org/abs/2507.01925))
argues that current VLA models share one shape — vision and language go through a series of
modules that emit a chain of **action tokens**, each stage more grounded and more actionable
than the last — and that the primary design choice distinguishing one model from another is how
those action tokens are formulated. It sorts them into eight kinds:

| Action token | What the model emits | Example in our canon |
|---|---|---|
| language description | a named skill or subgoal in words | [[01-canonical-papers/notes/4-vla/saycan\|SayCan]] |
| code | a program the runtime executes | none |
| affordance | where and how an object admits action | [[01-canonical-papers/notes/4-vla/saycan\|SayCan]]'s scoring half |
| trajectory | a path through space | none |
| goal state | the state to be reached, not the way there | none |
| latent representation | a learned code the decoder expands | none |
| raw action | joint or end-effector commands directly | most of the list below |
| reasoning | intermediate thought that conditions the action | none |

**Where our reading list actually sits.** Almost all of it is in one row. RT-1, RT-2 and OpenVLA
emit raw actions as discretised bins; Diffusion Policy, ACT, Octo, π0 and GR00T N1 emit raw
actions continuously, through diffusion, chunking or flow matching. SayCan is the one entry that
works above that level. Five of the eight kinds have no paper on our list at all, which is worth
knowing before assuming the canon covers the design space.

**The binning is a real constraint, not a formality.** FAST
([arXiv:2501.09747](https://arxiv.org/abs/2501.09747)) reports that per-dimension, per-timestep
binning performs poorly on dexterous, high-frequency data, and replaces it with a
compression-based scheme built on the discrete cosine transform, released as a universal
tokenizer trained on a million real robot trajectories. When a paper says it "tokenises
actions", that sentence is carrying a design decision.

### 2. Five surveys, five projections

There is no shortage of VLA surveys, and they disagree about the taxonomy because each projects
the field onto a different axis. Knowing which axis a survey chose is most of what you need to
read it:

| Survey | Axis it organises the field on |
|---|---|
| Ma et al. ([2405.14093](https://arxiv.org/abs/2405.14093)) | components, low-level control policies, high-level task planners |
| Zhong et al. ([2507.01925](https://arxiv.org/abs/2507.01925)) | how action tokens are formulated |
| Zhang et al. ([2509.19012](https://arxiv.org/abs/2509.19012)) | generation paradigm — autoregressive, diffusion, reinforcement, hybrid, specialised |
| Yu et al. ([2510.24795](https://arxiv.org/abs/2510.24795)) | efficiency across model, training and data |
| Xu et al. ([2512.11362](https://arxiv.org/abs/2512.11362)) | open challenges — representation, execution, generalisation, safety, data and evaluation |

These are complementary rather than competing. A model has a token type *and* a generation
paradigm *and* an efficiency profile. Ask which projection you are being shown before you
conclude that two surveys contradict each other.

### 3. The axis this list does not cover: what it costs to run

Every model below was published to show a capability, and none of the notes ask what it costs to
deploy. That question now has its own literature. Yu et al. organise it into three pillars —
efficient model design, covering architecture and compression; efficient training; and efficient
data collection — and the last is the one specific to robotics, because robot data cannot be
scraped. SmolVLA ([arXiv:2506.01844](https://arxiv.org/abs/2506.01844)) is the concrete anchor:
a deliberately small VLA trained on a single GPU using community-collected data from affordable
platforms, positioned against VLAs with billions of parameters. Read it against π0 and GR00T N1
and the comparison is about deployability rather than capability.

> [!tip] What to read next · 다음에 읽을 것
> If you want the design axis, read Chen et al. and then FAST, and re-read
> [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]] and [[01-canonical-papers/notes/4-vla/pi0|π0]]
> asking only how each turns a continuous action into something a model can predict. If you want
> the deployment axis, read Yu et al. and SmolVLA. Neither is on the canonical list, and neither
> needs to be — the list is for papers you will cite, and these are for orienting yourself in a
> literature that produces a new survey every few months.

### 4. The generalists of 2025–2026 that have no note

Some models are met often enough to recognize but have no paper note, usually because the only source is a company post. Checked against those sources on 2026-09-22; read each row as a claim about what exists, and hold it to [[03-deep-learning/vla/index|4. VLA §4]] before it carries an argument.

| model (maker, date) | what it is built from | rates and data | evidence |
|---|---|---|---|
| Helix (Figure, February 2025) | a 7B open vision–language model as "System 2" at $7$–$9$ Hz over an 80M "System 1" policy at $200$ Hz; $35$ degrees of freedom of the upper body, fingers included | about $500$ hours of teleoperation; runs on embedded GPUs on the robot | [company post](https://www.figure.ai/news/helix), no success rates |
| Redwood AI (1X, June 2025) | a 160M VLA for whole-body mobile manipulation on the NEO humanoid | on the robot's GPU at about $5$ Hz; teleoperated and autonomous episodes, failures included | [company post](https://www.1x.tech/discover/redwood-ai) |
| Large Behavior Models (Toyota Research Institute, July 2025) | multitask Diffusion Policies at scale | blind, randomized real and simulated trials with statistical confidence: multitask pretraining learned new tasks from a fraction of single-task data | [paper](https://arxiv.org/abs/2507.05331) |
| LBM on Atlas (Boston Dynamics with TRI, August 2025) | a 450M diffusion transformer trained by flow matching, whole-body control of all $50$ degrees of freedom | $30$ Hz, chunks of $48$ actions ($1.6$ s); VR teleoperation with foot tracking, plus simulation | [company post](https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/); names tactile force control as open work |
| SmolVLA (Hugging Face, June 2025) | a small VLA trained on community-collected LeRobot data, with asynchronous inference | trains on one GPU, runs on consumer GPUs or CPUs; reported comparable to VLAs ten times larger | [paper](https://arxiv.org/abs/2506.01844), open code and data |
| GraspVLA (May 2025) | a grasping VLA pretrained on SynGrasp-1B, a billion synthetic frames, with internet semantics | synthetic action data only, zero-shot real grasping | [paper](https://arxiv.org/abs/2505.03233) |
| ACT-1 (Sunday Robotics, November 2025) | a mobile-manipulation model trained on no robot data: people wearing Skill Capture Gloves in homes | clearing a table into a dishwasher: $21$ objects, $68$ interactions, over $130$ ft; needs a 3D map of a new home; $90\%$ of glove data converts to robot data | [company post](https://www.sunday.ai/journal/no-robot-data) |
| Skild Brain and S1 (Skild AI, September 2025 and August 2026) | an "omni-bodied" policy trained in simulation on $100{,}000$ robot bodies; S1 learns a new task from one video in its context | adapts in seconds to unseen or damaged bodies; S1 reports $66\%$ on unseen tasks against $9\%$ for a VLA baseline | company posts ([omni-bodied](https://www.skild.ai/blogs/omni-bodied), [S1](https://skild.ai/blogs/s1)) |
| CraftNet (Sharpa, January 2026) | a vision–tactile–language–action hierarchy: a $1$ Hz VLM, $10$ Hz motion planning, and a $100$ Hz tactile and force loop for the last millimetre | no numbers or paper | [company post](https://www.sharpa.com/blogs/news/sharpa-announces-craftnet-a-hierarchical-vtla-model-for-fine-manipulation) |

GEN-0 and GEN-1.5 (Generalist AI) and DYNA-2 (Dyna Robotics) are read in [[03-deep-learning/vla/index|4. VLA §7–§8]]; Gemini Robotics has its own [[gemini-robotics|note]]. Two patterns run through the table. The rates stack in layers — a slow reasoner over a fast controller, now with a third, tactile layer at $100$ Hz in CraftNet — which is the two-rate structure of [[gr00t-n1|GR00T]] carried one level further. And the data move off the robot: gloves, handheld grippers, human video and simulation replace teleoperation as the bulk of what a policy sees. Only three rows come with a paper or a statistical evaluation.

## 한국어

로봇 파운데이션 모델 — RT-1부터 GR00T N1까지. 이 페이지는 지도이고, 읽기 순서는
[[01-canonical-papers/canonical-list|핵심 논문 리스트]]에 있다.

### 1. 논문들이 실제로 갈리는 축

아래 노트를 연도순으로 읽으면 모델이 점점 커지는 수열처럼 보인다. 그것은 이들을 가르는 것이
아니다. Zhong 외의 서베이([arXiv:2507.01925](https://arxiv.org/abs/2507.01925))는 지금의 VLA가
하나의 형태를 공유한다고 본다. 시각과 언어가 일련의 모듈을 지나며 **액션 토큰**의 사슬을
내놓고, 뒤로 갈수록 더 접지되고 더 실행 가능해진다는 것이다. 그리고 한 모델을 다른 모델과
가르는 첫 번째 설계 선택은 그 액션 토큰을 어떤 형식으로 잡느냐라고 말한다. 여덟 가지로 나눈다.

| 액션 토큰 | 모델이 내놓는 것 | 우리 정전에서의 예 |
|---|---|---|
| 언어 서술 | 이름 붙은 skill이나 하위 목표를 말로 | [[01-canonical-papers/notes/4-vla/saycan\|SayCan]] |
| 코드 | 런타임이 실행할 프로그램 | 없음 |
| 어포던스 | 물체가 어디서 어떻게 행동을 허락하는가 | [[01-canonical-papers/notes/4-vla/saycan\|SayCan]]의 채점 쪽 절반 |
| 궤적 | 공간을 지나는 경로 | 없음 |
| 목표 상태 | 가는 길이 아니라 닿아야 할 상태 | 없음 |
| 잠재 표현 | 디코더가 펼칠 학습된 코드 | 없음 |
| 원시 행동 | 관절이나 말단 명령을 직접 | 아래 목록 대부분 |
| 추론 | 행동을 조건 짓는 중간 사고 | 없음 |

**우리 읽기 목록이 실제로 앉아 있는 자리.** 거의 전부가 한 줄에 몰려 있다. RT-1과 RT-2와
OpenVLA는 원시 행동을 이산 구간으로 내놓고, Diffusion Policy와 ACT와 Octo와 π0과 GR00T N1은
디퓨전·청킹·플로우 매칭으로 원시 행동을 연속적으로 내놓는다. 그 층 위에서 작동하는 항목은
SayCan 하나뿐이다. 여덟 가지 중 다섯 가지에는 우리 목록에 논문이 아예 없다. 정전이 설계
공간을 덮고 있다고 가정하기 전에 알아 둘 값어치가 있다.

**구간 나누기는 형식이 아니라 실제 제약이다.** FAST([arXiv:2501.09747](https://arxiv.org/abs/2501.09747))는
차원별·시점별 구간 나누기가 정교하고 고주파인 데이터에서 잘 작동하지 않는다고 보고하고, 이산
코사인 변환에 기반한 압축 방식으로 그것을 대체한다. 실제 로봇 궤적 백만 개로 학습한 범용
토크나이저로 공개했다. 논문이 "행동을 토큰화한다"고 쓸 때, 그 문장은 설계 결정을 지고 있다.

### 2. 서베이 다섯 편, 투영 다섯 개

VLA 서베이는 모자라지 않고, 서로 분류가 다르다. 각자 이 분야를 다른 축으로 투영하기 때문이다.
어느 축을 골랐는지 아는 것이 그 서베이를 읽는 데 필요한 것의 대부분이다.

| 서베이 | 어느 축으로 정리하는가 |
|---|---|
| Ma 외([2405.14093](https://arxiv.org/abs/2405.14093)) | 구성 요소, 저수준 제어 정책, 고수준 과제 계획기 |
| Chen 외([2507.01925](https://arxiv.org/abs/2507.01925)) | 액션 토큰을 어떤 형식으로 잡는가 |
| Zhong 외([2509.19012](https://arxiv.org/abs/2509.19012)) | 생성 방식 — 자기회귀, 디퓨전, 강화, 혼합, 특수 |
| Yu 외([2510.24795](https://arxiv.org/abs/2510.24795)) | 모델·학습·데이터에 걸친 효율성 |
| Xu 외([2512.11362](https://arxiv.org/abs/2512.11362)) | 미해결 문제 — 표현, 실행, 일반화, 안전, 데이터와 평가 |

이들은 경쟁이 아니라 상보적이다. 한 모델은 토큰 유형을 갖고, *동시에* 생성 방식을 갖고,
*동시에* 효율 프로파일을 갖는다. 두 서베이가 서로 모순된다고 결론 내리기 전에, 지금 보고 있는
것이 어느 투영인지 물어라.

### 3. 이 목록이 덮지 않는 축: 돌리는 데 드는 비용

아래 모든 모델은 능력을 보이려고 발표됐고, 어느 노트도 배포 비용을 묻지 않는다. 그 질문에는
이제 자기 문헌이 있다. Yu 외는 그것을 세 기둥으로 정리한다. 아키텍처와 압축을 다루는 효율적
모델 설계, 효율적 학습, 그리고 효율적 데이터 수집이다. 마지막 것이 로보틱스에 고유하다. 로봇
데이터는 긁어모을 수 없기 때문이다. 구체적 앵커는 SmolVLA([arXiv:2506.01844](https://arxiv.org/abs/2506.01844))다.
값싼 플랫폼에서 커뮤니티가 모은 데이터로 GPU 한 장에서 학습하도록 의도적으로 작게 만든 VLA이고,
파라미터가 수십억인 VLA들에 맞세워 놓았다. π0과 GR00T N1에 대 놓고 읽으면 비교의 주제가
능력이 아니라 배포 가능성이 된다.

> [!tip] 다음에 읽을 것 · What to read next
> 설계 축을 원하면 Chen 외를 읽고 이어서 FAST를 읽어라. 그다음
> [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]와 [[01-canonical-papers/notes/4-vla/pi0|π0]]을
> 다시 읽되, 각자 연속 행동을 모델이 예측할 수 있는 무엇으로 바꾸는지만 물어라. 배포 축을
> 원하면 Yu 외와 SmolVLA를 읽어라. 둘 다 핵심 논문 리스트에 없고, 있을 필요도 없다. 리스트는
> 인용할 논문을 위한 것이고, 이들은 몇 달마다 새 서베이가 나오는 문헌 속에서 방향을 잡기 위한
> 것이다.

### 4. 노트가 없는 2025–2026년의 범용 정책들

알아볼 만큼 자주 만나지만 노트가 없는 모델들이 있다. 대개 출처가 회사 글뿐이기 때문이다. 2026-09-22에 그 출처들과 대조했다. 각 행을 무엇이 있다는 주장으로 읽고, 논증을 싣기 전에 [[03-deep-learning/vla/index|4. VLA §4]]에 비춰 보라.

| 모델(만든 곳, 날짜) | 무엇으로 지었나 | 주기와 데이터 | 증거 |
|---|---|---|---|
| Helix(Figure, 2025년 2월) | $7$–$9$ Hz의 "System 2"인 7B 공개 시각–언어 모델 아래 $200$ Hz의 "System 1"인 80M 정책. 손가락까지 상체 $35$자유도 | 원격조작 약 $500$시간. 로봇 위 임베디드 GPU에서 돈다 | [회사 글](https://www.figure.ai/news/helix), 성공률 없음 |
| Redwood AI(1X, 2025년 6월) | NEO 휴머노이드의 전신 이동 조작을 위한 160M VLA | 로봇 GPU에서 약 $5$ Hz. 실패를 포함한 원격조작·자율 에피소드 | [회사 글](https://www.1x.tech/discover/redwood-ai) |
| Large Behavior Model(Toyota Research Institute, 2025년 7월) | 규모를 키운 다중 과제 Diffusion Policy | 통계적 신뢰도를 갖춘 블라인드 무작위 실제·시뮬레이션 시행. 다중 과제 사전학습은 단일 과제 데이터의 일부만으로 새 과제를 익혔다 | [논문](https://arxiv.org/abs/2507.05331) |
| Atlas의 LBM(Boston Dynamics와 TRI, 2025년 8월) | flow matching으로 학습한 450M 디퓨전 트랜스포머, $50$자유도 전신 제어 | $30$ Hz, 행동 $48$개 청크($1.6$초). 발 추적을 넣은 VR 원격조작과 시뮬레이션 | [회사 글](https://bostondynamics.com/blog/large-behavior-models-atlas-find-new-footing/). 촉각 힘 제어를 남은 과제로 꼽는다 |
| SmolVLA(Hugging Face, 2025년 6월) | 커뮤니티가 모은 LeRobot 데이터로 학습한 작은 VLA, 비동기 추론 | GPU 한 장으로 학습하고 소비자용 GPU나 CPU에서 돈다. 열 배 큰 VLA와 비슷하다고 보고 | [논문](https://arxiv.org/abs/2506.01844), 코드와 데이터 공개 |
| GraspVLA(2025년 5월) | 합성 프레임 10억 개인 SynGrasp-1B와 인터넷 의미 정보로 사전학습한 파지 VLA | 합성 행동 데이터만으로 실제 파지를 zero-shot | [논문](https://arxiv.org/abs/2505.03233) |
| ACT-1(Sunday Robotics, 2025년 11월) | 로봇 데이터 없이, 집에서 Skill Capture Glove를 낀 사람의 데이터로 학습한 이동 조작 모델 | 식탁을 치워 식기세척기에 넣기: 물체 $21$개, 조작 $68$번, $130$ft 이상 이동. 새 집에는 3D 지도가 필요하고, 장갑 데이터의 $90\%$가 로봇 데이터로 변환된다 | [회사 글](https://www.sunday.ai/journal/no-robot-data) |
| Skild Brain과 S1(Skild AI, 2025년 9월과 2026년 8월) | 시뮬레이션에서 로봇 몸 $100{,}000$종으로 학습한 "옴니바디" 정책. S1은 문맥 속 비디오 하나로 새 과제를 익힌다 | 처음 보는 몸이나 망가진 몸에 몇 초 만에 적응. S1은 처음 보는 과제에서 VLA 기준선 $9\%$ 대비 $66\%$를 보고 | 회사 글([옴니바디](https://www.skild.ai/blogs/omni-bodied), [S1](https://skild.ai/blogs/s1)) |
| CraftNet(Sharpa, 2026년 1월) | 시각–촉각–언어–행동 계층. $1$ Hz VLM, $10$ Hz 동작 계획, 마지막 1밀리미터를 위한 $100$ Hz 촉각·힘 루프 | 수치도 논문도 없음 | [회사 글](https://www.sharpa.com/blogs/news/sharpa-announces-craftnet-a-hierarchical-vtla-model-for-fine-manipulation) |

GEN-0과 GEN-1.5(Generalist AI), DYNA-2(Dyna Robotics)는 [[03-deep-learning/vla/index|4. VLA §7–§8]]에서 읽고, Gemini Robotics는 따로 [[gemini-robotics|노트]]가 있다. 표에는 두 흐름이 지나간다. 주기가 층층이 쌓인다 — 빠른 제어기 위의 느린 추론기, 그리고 CraftNet에서는 $100$ Hz의 셋째 촉각 층까지 — 이것은 [[gr00t-n1|GR00T]]의 두 주기 구조를 한 단계 더 민 것이다. 그리고 데이터가 로봇을 떠난다. 장갑, 손에 드는 그리퍼, 사람 비디오, 시뮬레이션이 정책이 보는 것의 대부분으로 원격조작을 대신한다. 논문이나 통계적 평가가 딸린 행은 셋뿐이다.
