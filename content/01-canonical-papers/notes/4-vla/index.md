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
what separates them. Chen et al.'s survey ([arXiv:2507.01925](https://arxiv.org/abs/2507.01925))
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
| Chen et al. ([2507.01925](https://arxiv.org/abs/2507.01925)) | how action tokens are formulated |
| Zhong et al. ([2509.19012](https://arxiv.org/abs/2509.19012)) | generation paradigm — autoregressive, diffusion, reinforcement, hybrid, specialised |
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

## 한국어

로봇 파운데이션 모델 — RT-1부터 GR00T N1까지. 이 페이지는 지도이고, 읽기 순서는
[[01-canonical-papers/canonical-list|핵심 논문 리스트]]에 있다.

### 1. 논문들이 실제로 갈리는 축

아래 노트를 연도순으로 읽으면 모델이 점점 커지는 수열처럼 보인다. 그것은 이들을 가르는 것이
아니다. Chen 외의 서베이([arXiv:2507.01925](https://arxiv.org/abs/2507.01925))는 지금의 VLA가
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
