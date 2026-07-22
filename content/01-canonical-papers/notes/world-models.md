---
title: "World Models"
authors: David Ha, Jürgen Schmidhuber
affiliation: Google Brain, IDSIA/NNAISENSE
venue: NeurIPS
year: 2018
arxiv: https://arxiv.org/abs/1803.10122
pdf: https://arxiv.org/pdf/1803.10122
project: https://worldmodels.github.io
tags: [paper, world-models, rl]
status: to-read
---

**Ha & Schmidhuber, NeurIPS 2018** — [arXiv](https://arxiv.org/abs/1803.10122) · [PDF](https://arxiv.org/pdf/1803.10122) · [Official](https://worldmodels.github.io)

## English

**One-line summary**: Learn a compressed generative model of the environment (VAE + RNN), then train a tiny controller *inside the model's dream* — the modern founding document of world-model-based agents.

### Context

Model-free RL ([[02-foundations/rl-basics|RL basics]]) needs millions of real environment
steps because the policy network must learn perception, dynamics, and control all at once
from sparse reward. Cognitive science's counter-proposal: brains learn a predictive model
of the world and act inside it. Could an agent *train* inside its own learned simulation?

### Method

> [!tip] Key intuition
> Split the agent: a big world model that learns *what the world is like* (unsupervised,
> dense signal), and a minimal controller that learns *what to do* (RL, sparse signal).
> The hard perception/prediction problem gets the parameters; the RL problem becomes tiny.

- **V** (vision): a [[vae|VAE]] compresses each frame to a small latent $z$.
- **M** (memory): an MDN-RNN predicts $p(z_{t+1}|z_t, a_t, h_t)$ — stochastic latent
  dynamics with a temperature knob.
- **C** (controller): a *single linear layer* on $[z_t, h_t]$, trained with evolution
  strategies (CMA-ES) — small enough that credit assignment is trivial.
- **Training in the dream**: for VizDoom, C is trained entirely inside M's hallucinated
  rollouts, then transferred to the real environment.

### Results

- Solved CarRacing-v0 (first agent to do so) with the world-model features.
- The dream-trained VizDoom policy *transfers to the real game*; raising dream temperature
  regularizes against exploiting model errors.

### Limitations & critique

- Stagewise training (V, M, C separately) — later work made it end-to-end; the linear
  controller obviously caps task complexity.
- Model exploitation: the agent finds and abuses the model's errors — the core disease of
  all model-based RL, managed here only by temperature.
- Simple 2D environments only.

### Impact & follow-ups

Named the field. The V/M/C decomposition — learn dynamics in latent space, act on latent
states — is the skeleton of [[planet|PlaNet]] and [[dreamer|Dreamer]], and the
"train in imagination" idea returns at scale in [[genie|Genie]] and
[[cosmos|Cosmos]]-style synthetic data engines.

### Connections

- Foundations: [[vae|VAE]], [[lstm|LSTM]], [[02-foundations/rl-basics|RL basics]]
- Next: [[planet|PlaNet]] → [[dreamer|Dreamer]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 환경의 압축된 생성 모델(VAE + RNN)을 배우고, 그 모델의 *꿈속에서* 아주 작은 컨트롤러를 학습 — 월드모델 기반 에이전트의 현대적 창립 문서.

### 배경

모델 프리 RL([[02-foundations/rl-basics|RL 기초]])은 정책망이 지각·동역학·제어를 희소한
보상만으로 한꺼번에 배워야 해서 수백만 실제 스텝이 필요하다. 인지과학의 반론: 뇌는
세계의 예측 모델을 배우고 그 안에서 행동한다. 에이전트가 자기가 배운 시뮬레이션 *안에서*
훈련될 수 있을까?

### 방법

> [!tip] 핵심 직관
> 에이전트를 쪼개라: *세계가 어떤 곳인지*를 배우는 큰 월드모델(비지도, 밀집 신호)과
> *무엇을 할지*를 배우는 최소한의 컨트롤러(RL, 희소 신호). 어려운 지각/예측 문제에
> 파라미터를 몰아주면 RL 문제는 아주 작아진다.

- **V** (시각): [[vae|VAE]]가 각 프레임을 작은 잠재변수 $z$로 압축.
- **M** (기억): MDN-RNN이 $p(z_{t+1}|z_t, a_t, h_t)$를 예측 — 온도 조절이 가능한 확률적
  잠재 동역학.
- **C** (제어): $[z_t, h_t]$ 위의 *선형층 하나*, 진화 전략(CMA-ES)으로 학습 — 신용 할당이
  자명할 만큼 작다.
- **꿈속 훈련**: VizDoom에서 C를 M이 환각한 롤아웃 안에서만 학습한 뒤 실제 환경으로 전이.

### 결과

- CarRacing-v0을 (최초로) 해결.
- 꿈에서 훈련된 VizDoom 정책이 *실제 게임으로 전이*; 꿈의 온도를 높이면 모델 오류를
  악용하는 것을 막는 정규화가 된다.

### 한계와 비판

- 단계별 학습(V, M, C 따로) — 이후 연구가 end-to-end로 만들었다; 선형 컨트롤러는 과제
  복잡도의 명백한 상한.
- 모델 악용: 에이전트가 모델의 오류를 찾아 악용한다 — 모든 모델 기반 RL의 핵심 질병,
  여기서는 온도로만 관리된다.
- 단순한 2D 환경뿐.

### 영향과 후속 연구

분야에 이름을 붙였다. V/M/C 분해 — 잠재 공간에서 동역학을 배우고 잠재 상태 위에서
행동하기 — 는 [[planet|PlaNet]]과 [[dreamer|Dreamer]]의 골격이고, "상상 속 훈련"은
[[genie|Genie]]와 [[cosmos|Cosmos]]류 합성 데이터 엔진에서 규모를 갖춰 되돌아온다.

### 연결

- 기초: [[vae|VAE]], [[lstm|LSTM]], [[02-foundations/rl-basics|RL 기초]]
- 다음: [[planet|PlaNet]] → [[dreamer|Dreamer]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]
