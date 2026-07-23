---
title: "RT-2 — Vision-Language-Action Models Transfer Web Knowledge to Robotic Control"
authors: Anthony Brohan, Noah Brown, Justice Carbajal, et al.
affiliation: Google DeepMind
venue: CoRL
year: 2023
arxiv: https://arxiv.org/abs/2307.15818
pdf: https://arxiv.org/pdf/2307.15818
project: https://robotics-transformer2.github.io
tags: [paper, vla, robot-learning]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Brohan et al., CoRL 2023** — [arXiv](https://arxiv.org/abs/2307.15818) · [PDF](https://arxiv.org/pdf/2307.15818) · [Official](https://robotics-transformer2.github.io)

## English

**One-line summary**: Express robot actions as text tokens and co-fine-tune a web-pretrained VLM on robot data — the robot inherits the internet's semantics, and "vision-language-action model" enters the vocabulary.

### Context

[[rt-1|RT-1]] generalized within its 700 tasks but knew nothing beyond them — it had never
seen Taylor Swift, a soda brand, or the concept "extinct animal." Meanwhile
[[flamingo|VLMs]] built on [[clip|CLIP]]-scale pretraining could reason about anything on
the web but couldn't act. The question RT-2 answers: can a single model keep the web's
semantic knowledge *and* output motor commands?

### Method

> [!tip] Key intuition
> Don't bolt a policy head onto a VLM — make actions *literally another language* the VLM
> speaks. If "move gripper to 0.3, 0.5" is just a string, then robot control is one more
> text task, and everything the VLM knows transfers to control for free.

- Backbones: **PaLI-X (up to 55B)** and **PaLM-E (12B)**, pretrained on web-scale
  vision-language data.
- **Actions as text**: RT-1's 256-bin discretization, but each bin is emitted as a (reused
  or reserved) *text token* — the action space is a sentence.
- **Co-fine-tuning**: robot episodes are mixed with the original web VQA-style data during
  fine-tuning — keeping web knowledge alive instead of catastrophically forgetting it.
- Inference: constrained decoding to valid action tokens, run in the cloud at 1–3 Hz.
- Chain-of-thought variant: emit a reasoning step ("Plan: pick energy drink") before action tokens.

### Results

- On unseen objects/backgrounds/instructions: roughly **2–3× RT-1's generalization**
  (~62% vs ~32–35% on the hardest unseen splits), while matching RT-1 on seen tasks.
- **Emergent capabilities** absent from robot data: symbol understanding (place object on
  "3"), semantic reasoning (pick the drink for a tired person), relational grounding
  (smallest/largest, "animal that is extinct" → toy dinosaur).
- Capability scales with VLM size — the web-pretraining investment transfers.

### Limitations & critique

- No new *motor skills*: generalization is semantic; dexterity remains bounded by the robot
  data distribution.
- 55B parameters need cloud inference — latency and deployment costs are severe
  ([[openvla|OpenVLA]]-class open 7B models and quantization respond to this).
- Autoregressive discrete tokens still fit continuous, multimodal trajectories poorly
  ([[diffusion-policy|diffusion]]/flow heads in π0 respond to this).

### Impact & follow-ups

Named and defined the **VLA** category. Every subsequent robot foundation model — OpenVLA,
π0, GR00T — is a descendant of the "pretrained VLM + action output head" template; the
field's debates (discrete tokens vs continuous heads, co-training ratios) are debates about
RT-2's design choices.

### Connections

- Previous: [[rt-1|RT-1]] (the data & tokenization), [[flamingo|Flamingo]]/[[llava|LLaVA]] (the VLM substrate)
- Next: OpenVLA, π0, GR00T N1
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 로봇 행동을 텍스트 토큰으로 표현하고 웹 사전학습 VLM을 로봇 데이터와 공동 파인튜닝 — 로봇이 인터넷의 의미론을 상속받고, "vision-language-action 모델"이라는 용어가 태어났다.

### 배경

[[rt-1|RT-1]]은 700개 과제 안에서는 일반화했지만 그 밖은 전혀 몰랐다 — Taylor Swift도,
음료 브랜드도, "멸종한 동물"이라는 개념도 본 적이 없다. 한편 [[clip|CLIP]] 규모의 사전학습
위에 세워진 [[flamingo|VLM]]들은 웹의 무엇이든 추론할 수 있지만 행동하지 못했다.
RT-2가 답한 질문: 하나의 모델이 웹의 의미 지식을 유지하면서 *동시에* 모터 명령을 출력할 수 있는가?

### 방법

> [!tip] 핵심 직관
> VLM에 정책 헤드를 접붙이지 말고, 행동을 VLM이 말하는 *말 그대로 또 하나의 언어*로
> 만들어라. "그리퍼를 0.3, 0.5로 이동"이 그냥 문자열이라면 로봇 제어는 텍스트 과제 하나가
> 더 생긴 것이고, VLM이 아는 모든 것이 제어로 공짜로 전이된다.

- 백본: 웹 규모 시각-언어 데이터로 사전학습된 **PaLI-X(최대 55B)**와 **PaLM-E(12B)**.
- **행동의 텍스트화**: RT-1의 256 구간 이산화를 쓰되, 각 구간을 (재사용 또는 예약된)
  *텍스트 토큰*으로 출력 — 행동 공간이 문장이 된다.
- **공동 파인튜닝**: 파인튜닝 중 로봇 에피소드를 원래의 웹 VQA류 데이터와 섞는다 —
  웹 지식을 파국적으로 잊는 대신 살려두는 장치.
- 추론: 유효한 행동 토큰으로 제약된 디코딩, 클라우드에서 1~3 Hz.
- Chain-of-thought 변형: 행동 토큰 전에 추론 스텝("계획: 에너지 드링크를 집는다")을 출력.

### 결과

- 처음 보는 물체/배경/지시에서 **RT-1의 약 2~3배 일반화** (최난이도 미학습 분할에서
  ~62% vs ~32–35%), 본 과제에서는 RT-1과 대등.
- 로봇 데이터에 없던 **창발 능력**: 기호 이해(물체를 숫자 "3" 위에 놓기), 의미 추론
  (피곤한 사람에게 줄 음료 고르기), 관계 접지(가장 작은/큰 것, "멸종한 동물" → 공룡 인형).
- 능력이 VLM 크기에 따라 스케일 — 웹 사전학습 투자가 제어로 전이된다.

### 한계와 비판

- 새로운 *운동 기술*은 없다: 일반화는 의미론 쪽이고, 손재주는 여전히 로봇 데이터 분포에 갇혀 있다.
- 55B 파라미터는 클라우드 추론 필수 — 지연과 배포 비용이 크다
  ([[openvla|OpenVLA]]급 오픈 7B 모델과 양자화가 이에 대한 응답).
- 자기회귀 이산 토큰은 연속적·다봉적 궤적에 여전히 잘 안 맞는다
  (π0의 [[diffusion-policy|디퓨전]]/flow 헤드가 이에 대한 응답).

### 영향과 후속 연구

**VLA**라는 범주를 명명하고 정의했다. 이후의 모든 로봇 파운데이션 모델 — OpenVLA, π0,
GR00T — 은 "사전학습 VLM + 행동 출력 헤드" 템플릿의 후손이며, 분야의 논쟁들(이산 토큰
vs 연속 헤드, 공동 학습 비율)은 곧 RT-2의 설계 선택에 대한 논쟁이다.

### 연결

- 이전: [[rt-1|RT-1]] (데이터와 토큰화), [[flamingo|Flamingo]]/[[llava|LLaVA]] (VLM 토대)
- 다음: OpenVLA, π0, GR00T N1
- 계보: [[03-deep-learning/lineage|논문 계보도]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 제목의 "transfers web knowledge to robotic control"은 로봇이 새 운동 기술을 웹에서 배웠다는 뜻이 아니다 — 웹 사전학습의 의미 지식이 행동 선택으로 전이됐다는 뜻이다. 실험도 정확히 그것(semantic generalization)만 재고, 새로운 손재주 획득은 재지 않는다. 제목이 허용하는 가장 강한 독해와 실험이 지지하는 독해의 간극을 확인하라.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] "행동을 토큰화한다"의 구체적 의미(차원당 256 구간 → 예약된 텍스트 토큰)를 설명할 수 있다
- [ ] co-fine-tuning이 무엇을 막기 위한 장치인지(웹 지식의 파국적 망각) 말할 수 있다
- [ ] 의미적 일반화와 운동 기술 일반화를 구분하고, RT-2가 어느 쪽만 얻었는지 말할 수 있다
- [ ] 창발 능력 평가가 증명하는 것과 증명하지 않는 것을 말할 수 있다
