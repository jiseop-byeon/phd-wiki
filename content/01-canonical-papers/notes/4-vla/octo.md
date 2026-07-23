---
title: "Octo — An Open-Source Generalist Robot Policy"
authors: Octo Model Team (Dibya Ghosh, Homer Walke, Karl Pertsch, Kevin Black, Oier Mees, et al.)
affiliation: UC Berkeley, Stanford, CMU, Google DeepMind
venue: RSS
year: 2024
arxiv: https://arxiv.org/abs/2405.12213
pdf: https://arxiv.org/pdf/2405.12213
code: https://github.com/octo-models/octo
project: https://octo-models.github.io
tags: [paper, vla, robot-learning]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Octo Model Team, RSS 2024** — [arXiv](https://arxiv.org/abs/2405.12213) · [PDF](https://arxiv.org/pdf/2405.12213) · [Code](https://github.com/octo-models/octo) · [Official](https://octo-models.github.io)

## English

**One-line summary**: A small open transformer trained on 800k Open X-Embodiment trajectories, with a diffusion action head and a plug-in token design — the first generalist policy anyone could download, fine-tune, and re-wire to a new robot in hours.

### Context

After [[open-x-embodiment|OXE]], the data was open but the strong models weren't: RT-2-X is
closed and 55B. Labs needed a policy they could *adapt* — new cameras, new action spaces,
new robots — without retraining from scratch. Octo's question: what architecture makes a
generalist policy maximally *modular*?

### Method

> [!tip] Key intuition
> Make everything a token and every output a "readout." If observations, language, and
> goals are just token streams into one transformer, then adding a sensor or a new action
> space is adding tokens and a small head — not surgery on the backbone.

- Inputs tokenized flexibly: language instruction *or* goal image, multiple camera streams,
  proprioception — any subset works (blockwise attention masks handle missing modalities).
- **Readout tokens** attend to everything and feed lightweight heads; the action head is a
  **[[diffusion-policy|diffusion]] policy** over action chunks — capturing multimodality
  that [[rt-1|RT-1]]-style discretization loses.
- Trained on 800k trajectories (25 OXE datasets); models at 27M and 93M parameters — small
  enough for on-robot inference and single-GPU fine-tuning.
- Fine-tuning recipe: attach new observation/action tokens, train ~5 hours on ~100 demos.

### Results

- Positive transfer out of the box across 9 evaluation setups (WidowX, Franka, bimanual
  ALOHA-style rigs); outperforms RT-1-X on zero-shot multi-robot evaluations.
- Effective fine-tuning to *new observation and action spaces* (e.g., joint-space bimanual
  control) — the modularity claim holds.
- Full open release (weights, data pipeline, code) made it the community's default baseline.

### Limitations & critique

- Small capacity and no web-scale VLM pretraining ⇒ limited semantic generalization —
  exactly the axis where [[openvla|OpenVLA]] (VLM backbone) wins.
- Diffusion head adds inference latency vs one-shot heads; wrist-camera dropout and
  data-quality issues from OXE carry through.
- Tabletop-manipulation-centric, like its training corpus.

### Impact & follow-ups

Defined the open-generalist-policy category and normalized two designs now everywhere:
diffusion action heads and token-modular multi-embodiment interfaces. The direct baseline
against which [[openvla|OpenVLA]] and later open VLAs measure themselves.

### Connections

- Previous: [[open-x-embodiment|Open X-Embodiment]], [[diffusion-policy|Diffusion Policy]]
- Next: [[openvla|OpenVLA]], [[pi0|π0]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: Open X-Embodiment 궤적 80만 개로 학습한 작은 오픈 트랜스포머 — 디퓨전 행동 헤드와 플러그인 토큰 설계로, 누구나 내려받아 몇 시간 만에 새 로봇에 재배선할 수 있는 최초의 범용 정책.

### 배경

[[open-x-embodiment|OXE]] 이후 데이터는 열렸지만 강한 모델은 닫혀 있었다: RT-2-X는
비공개에 55B다. 랩들에게 필요한 것은 *적응시킬 수 있는* 정책이었다 — 새 카메라, 새 행동
공간, 새 로봇에, 처음부터 재학습하지 않고. Octo의 질문: 범용 정책을 최대한 *모듈식*으로
만드는 구조는 무엇인가?

### 방법

> [!tip] 핵심 직관
> 모든 것을 토큰으로, 모든 출력을 "readout"으로 만들어라. 관측·언어·목표가 하나의
> 트랜스포머로 들어가는 토큰 스트림일 뿐이라면, 센서나 행동 공간을 추가하는 일은 토큰과
> 작은 헤드를 더하는 일이지 백본 수술이 아니다.

- 입력의 유연한 토큰화: 언어 지시 *또는* 목표 이미지, 복수 카메라, 고유수용감각 — 어떤
  부분집합이든 작동 (블록 어텐션 마스크가 빠진 모달리티를 처리).
- **Readout 토큰**이 전체를 참조해 가벼운 헤드에 공급; 행동 헤드는 행동 청크에 대한
  **[[diffusion-policy|디퓨전]] 정책** — [[rt-1|RT-1]]식 이산화가 잃는 다봉성을 담는다.
- 80만 궤적(OXE 25개 데이터셋)으로 학습; 27M/93M 파라미터 — 로봇 탑재 추론과 GPU 한 장
  파인튜닝이 가능한 크기.
- 파인튜닝 레시피: 새 관측/행동 토큰을 붙이고 시연 ~100개로 ~5시간 학습.

### 결과

- 9개 평가 셋업(WidowX, Franka, ALOHA식 양팔)에서 그대로 양의 전이; zero-shot 다중 로봇
  평가에서 RT-1-X 상회.
- *새로운 관측·행동 공간*(예: 관절 공간 양팔 제어)으로의 파인튜닝이 실제로 통한다 —
  모듈성 주장의 입증.
- 완전 공개(가중치, 데이터 파이프라인, 코드)로 커뮤니티의 기본 베이스라인이 됐다.

### 한계와 비판

- 작은 용량 + 웹 규모 VLM 사전학습 부재 ⇒ 의미적 일반화 제한 — 정확히 [[openvla|OpenVLA]]
  (VLM 백본)가 이기는 축이다.
- 디퓨전 헤드는 원샷 헤드 대비 추론 지연을 더한다; OXE에서 물려받은 손목 카메라 누락과
  데이터 품질 문제도 그대로.
- 학습 코퍼스처럼 탁상 조작 중심이다.

### 영향과 후속 연구

오픈 범용 정책이라는 범주를 정의했고, 지금은 어디에나 있는 두 설계 — 디퓨전 행동 헤드,
토큰 모듈식 다중-신체 인터페이스 — 를 표준화했다. [[openvla|OpenVLA]]와 이후 오픈 VLA들이
자신을 재는 직접 베이스라인.

### 연결

- 이전: [[open-x-embodiment|Open X-Embodiment]], [[diffusion-policy|Diffusion Policy]]
- 다음: [[openvla|OpenVLA]], [[pi0|π0]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 토큰-모듈 설계(모든 입력은 토큰, 모든 출력은 readout)를 설명할 수 있다
- [ ] 디퓨전 행동 헤드 채택의 이유(다봉성)를 말할 수 있다
- [ ] 새 로봇 적응 레시피(토큰 추가 + 소량 시연)를 말할 수 있다
- [ ] 웹 사전학습 부재가 만드는 의미적 한계를 말할 수 있다
