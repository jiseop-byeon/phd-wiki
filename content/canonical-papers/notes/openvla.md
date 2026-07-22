---
title: "OpenVLA — An Open-Source Vision-Language-Action Model"
authors: Moo Jin Kim, Karl Pertsch, Siddharth Karamcheti, et al.
affiliation: Stanford, UC Berkeley, Toyota Research Institute, Google DeepMind, MIT
venue: CoRL
year: 2024
arxiv: https://arxiv.org/abs/2406.09246
pdf: https://arxiv.org/pdf/2406.09246
code: https://github.com/openvla/openvla
project: https://openvla.github.io
tags: [paper, vla, robot-learning]
status: to-read
---

**Kim et al., CoRL 2024** — [arXiv](https://arxiv.org/abs/2406.09246) · [PDF](https://arxiv.org/pdf/2406.09246) · [Code](https://github.com/openvla/openvla) · [Official](https://openvla.github.io)

## English

**One-line summary**: A fully open 7B VLA — SigLIP+DINOv2 vision fused into a Llama-2 backbone, trained on 970k OXE trajectories — that outperforms the closed 55B RT-2-X and fine-tunes on a consumer GPU via LoRA.

### Context

[[rt-2|RT-2]] proved the VLM-to-robot recipe but stayed closed and huge; [[octo|Octo]] was
open but small and semantically weak. The field needed the RT-2 recipe at accessible scale:
open weights, open data, open fine-tuning path. OpenVLA is that reproduction — plus design
lessons the closed papers never reported.

### Method

> [!tip] Key intuition
> The RT-2 recipe, openly and carefully: start from a strong open VLM, keep actions as
> discrete tokens, and pour in the community's shared data. The interesting findings are in
> the details — fused vision features and *which* fine-tuning knobs matter.

- Backbone: **Prismatic-7B** VLM — vision = **SigLIP + DINOv2 features fused** (semantics +
  spatial detail; a [[llava|LLaVA]]-style projector), language = Llama-2 7B.
- Actions: 256-bin discretization per dimension mapped onto reserved LM tokens
  ([[rt-1|RT-1]] convention), autoregressive decoding.
- Data: **970k trajectories** from the [[open-x-embodiment|OXE]] mixture with careful
  dataset weighting.
- Practicality results baked in: **LoRA fine-tuning** matches full fine-tuning on new robot
  setups; 4-bit quantization preserves task performance for deployment.

### Results

- **+16.5%p absolute** over RT-2-X (55B) across 29 evaluation tasks on WidowX and Google
  robot platforms — with ~8× fewer parameters.
- Beats [[diffusion-policy|Diffusion Policy]] baselines when fine-tuned on multi-task setups
  involving language grounding, though single-task dexterity remains competitive territory.
- Fine-tunes to new robots with ~10–150 demos on a single consumer GPU (LoRA).

### Limitations & critique

- Autoregressive discrete tokens cap control rate (~6 Hz) and fit continuous multimodal
  actions poorly — the exact axis [[pi0|π0]] attacks with flow matching.
- Single-image, no proprioception input in the base recipe; tabletop-biased like its data.
- 7B still strains on-robot compute budgets without quantization.

### Impact & follow-ups

Became the reference open VLA: the standard starting checkpoint for academic fine-tuning
studies (including construction/manufacturing task adaptations) and the baseline every new
VLA reports against. OpenVLA-OFT and successors revisit its action head with chunked,
continuous outputs — converging toward the [[pi0|π0]]/[[gr00t-n1|GR00T]] design point.

### Connections

- Previous: [[rt-2|RT-2]] (the recipe), [[open-x-embodiment|OXE]] (the data), [[llava|LLaVA]] (the architecture family)
- Next: [[pi0|π0]], [[gr00t-n1|GR00T N1]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 완전 공개 7B VLA — SigLIP+DINOv2 시각 특징을 Llama-2 백본에 융합, OXE 97만 궤적으로 학습 — 비공개 55B RT-2-X를 능가하고 소비자용 GPU에서 LoRA로 파인튜닝된다.

### 배경

[[rt-2|RT-2]]는 VLM-로봇 레시피를 증명했지만 비공개에 거대했고, [[octo|Octo]]는 열려
있지만 작고 의미적으로 약했다. 분야에 필요한 것은 접근 가능한 규모의 RT-2 레시피 —
공개 가중치, 공개 데이터, 공개 파인튜닝 경로였다. OpenVLA가 그 재현이다 — 비공개
논문들이 보고하지 않던 설계 교훈까지 얹어서.

### 방법

> [!tip] 핵심 직관
> RT-2 레시피를 공개적으로, 꼼꼼하게: 강한 오픈 VLM에서 출발해, 행동을 이산 토큰으로
> 유지하고, 커뮤니티의 공유 데이터를 쏟아붓는다. 흥미로운 발견은 디테일에 있다 —
> 융합된 시각 특징, 그리고 *어떤* 파인튜닝 손잡이가 중요한가.

- 백본: **Prismatic-7B** VLM — 시각 = **SigLIP + DINOv2 특징 융합**(의미론 + 공간 디테일;
  [[llava|LLaVA]]식 프로젝터), 언어 = Llama-2 7B.
- 행동: 차원당 256 구간 이산화를 예약된 LM 토큰에 매핑([[rt-1|RT-1]] 규약), 자기회귀 디코딩.
- 데이터: [[open-x-embodiment|OXE]] 혼합물에서 신중히 가중치를 준 **97만 궤적**.
- 실용성 결과 내장: **LoRA 파인튜닝**이 새 로봇 셋업에서 전체 파인튜닝과 대등; 4비트
  양자화가 과제 성능을 보존.

### 결과

- WidowX·Google 로봇 플랫폼의 29개 평가 과제에서 RT-2-X(55B) 대비 **절대 +16.5%p** —
  파라미터는 약 8분의 1로.
- 언어 접지가 필요한 다중 과제 파인튜닝에서 [[diffusion-policy|Diffusion Policy]]
  베이스라인 상회 — 단일 과제 정밀 조작에서는 여전히 접전.
- 시연 10~150개 + 소비자용 GPU 한 장(LoRA)으로 새 로봇에 파인튜닝.

### 한계와 비판

- 자기회귀 이산 토큰이 제어 주기를 제한하고(~6 Hz) 연속·다봉 행동에 잘 안 맞는다 —
  정확히 [[pi0|π0]]가 flow matching으로 공략한 축.
- 기본 레시피는 단일 이미지, 고유수용감각 입력 없음; 데이터처럼 탁상 편향.
- 7B도 양자화 없이는 로봇 탑재 연산 예산에 부담.

### 영향과 후속 연구

기준 오픈 VLA가 됐다: 학계 파인튜닝 연구(건설·제조 과제 적응 포함)의 표준 시작
체크포인트이자 모든 새 VLA가 비교 보고하는 베이스라인. OpenVLA-OFT 등 후속은 행동
헤드를 청크·연속 출력으로 재설계 — [[pi0|π0]]/[[gr00t-n1|GR00T]]의 설계 지점으로 수렴 중.

### 연결

- 이전: [[rt-2|RT-2]] (레시피), [[open-x-embodiment|OXE]] (데이터), [[llava|LLaVA]] (구조 계열)
- 다음: [[pi0|π0]], [[gr00t-n1|GR00T N1]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
