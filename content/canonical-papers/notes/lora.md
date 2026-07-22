---
title: "LoRA — Low-Rank Adaptation of Large Language Models"
authors: Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen
affiliation: Microsoft
venue: ICLR
year: 2022
arxiv: https://arxiv.org/abs/2106.09685
pdf: https://arxiv.org/pdf/2106.09685
code: https://github.com/microsoft/LoRA
tags: [paper, foundations, efficiency]
status: to-read
---

**Hu et al., ICLR 2022** — [arXiv](https://arxiv.org/abs/2106.09685) · [PDF](https://arxiv.org/pdf/2106.09685) · [Code](https://github.com/microsoft/LoRA)

## English

**One-line summary**: Freeze the pretrained weights and learn only a low-rank update ΔW = BA per weight matrix — fine-tune giant models by training ~0.01–1% of parameters, with zero added inference latency.

### Context

By 2021, the pretrain-finetune paradigm ([[canonical-papers/notes/bert|BERT]]) collided with model scale ([[canonical-papers/notes/gpt-3|GPT-3]] 175B): full fine-tuning means storing and serving a complete model copy *per task*. Existing parameter-efficient methods had costs — adapters add inference latency; prefix-tuning eats context length and optimizes poorly.

### Method

> [!tip] Key intuition
> Fine-tuning barely moves weights, and the movement has low *intrinsic rank* — the update lives in a small subspace. So parameterize the update itself as a product of two thin matrices and learn only that.

- For a frozen weight $W_0 \in \mathbb{R}^{d\times k}$, learn $\Delta W = BA$ with $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r\times k}$, rank $r \ll \min(d,k)$ (r = 1–64 works).
- Forward pass: $h = W_0 x + BAx$; $A$ initialized Gaussian, $B$ zero — so training starts from the pretrained model exactly.
- **Merge at deployment**: $W = W_0 + BA$ — no extra latency, unlike adapters. Task switching = swapping small LoRA weights.
- Applied to attention projections ($W_q$, $W_v$ suffice in the paper).

### Results

- Matches or beats full fine-tuning on GLUE (RoBERTa/DeBERTa) and GPT-2/GPT-3 175B benchmarks while training ~**0.01%** of parameters (GPT-3: 4.7M vs 175B).
- GPU memory for GPT-3 fine-tuning cut ~3×; checkpoint size from ~350GB to ~35MB.
- Analysis: learned updates strongly amplify directions already latent in $W_0$; very low rank suffices.

### Limitations & critique

- Optimal rank and placement are empirical; capacity can cap out on hard domain shifts (where full fine-tuning still wins).
- Batch-serving different tasks in one pass is awkward once weights are merged.
- The intrinsic-rank hypothesis is demonstrated, not explained — theory followed later.

### Impact & follow-ups

Democratized fine-tuning: LoRA (+QLoRA quantized variant) is *the* standard way individuals adapt LLMs, diffusion models (style LoRAs), and robot policies — fine-tuning [[canonical-papers/notes/gpt-3|GPT-3]]-scale VLAs like OpenVLA on a single GPU. Huge ecosystem: QLoRA, DoRA, AdaLoRA, and merged-LoRA model sharing.

### Connections

- Enables cheap adaptation of: [[canonical-papers/notes/gpt-3|GPT-3]]-class models, VLAs (OpenVLA fine-tuning)
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 사전학습 가중치는 얼리고 가중치 행렬마다 저랭크 업데이트 ΔW = BA만 학습 — 파라미터의 0.01~1%만 훈련해서 거대 모델을 파인튜닝하고, 추론 지연은 0.

### 배경

2021년, 사전학습-파인튜닝 패러다임([[canonical-papers/notes/bert|BERT]])이 모델 규모([[canonical-papers/notes/gpt-3|GPT-3]] 175B)와 충돌했다: 전체 파인튜닝은 *과제마다* 완전한 모델 복사본을 저장·서빙해야 한다는 뜻이다. 기존의 파라미터 효율 기법들은 대가가 있었다 — 어댑터는 추론 지연을 더하고, prefix-tuning은 문맥 길이를 잡아먹으며 최적화도 불안정했다.

### 방법

> [!tip] 핵심 직관
> 파인튜닝은 가중치를 거의 움직이지 않고, 그 움직임의 *내재적 랭크*는 낮다 — 업데이트가 작은 부분공간 안에 산다. 그렇다면 업데이트 자체를 얇은 행렬 두 개의 곱으로 파라미터화하고 그것만 배우자.

- 얼린 가중치 $W_0 \in \mathbb{R}^{d\times k}$에 대해 $\Delta W = BA$를 학습: $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r\times k}$, 랭크 $r \ll \min(d,k)$ (r = 1~64면 충분).
- 순전파: $h = W_0 x + BAx$; $A$는 가우시안, $B$는 0으로 초기화 — 학습이 정확히 사전학습 모델에서 출발한다.
- **배포 시 병합**: $W = W_0 + BA$ — 어댑터와 달리 추가 지연이 없다. 과제 전환 = 작은 LoRA 가중치 교체.
- 어텐션 투영에 적용(논문에서는 $W_q$, $W_v$면 충분).

### 결과

- GLUE(RoBERTa/DeBERTa)와 GPT-2/GPT-3 175B 벤치마크에서 전체 파인튜닝과 대등하거나 상회 — 훈련 파라미터는 약 **0.01%**(GPT-3: 175B 중 470만).
- GPT-3 파인튜닝의 GPU 메모리 약 3배 절감; 체크포인트 크기 약 350GB → 35MB.
- 분석: 학습된 업데이트는 $W_0$에 이미 잠재된 방향들을 증폭한다; 아주 낮은 랭크로 충분하다.

### 한계와 비판

- 최적 랭크와 적용 위치는 경험적이다; 어려운 도메인 전환에서는 용량이 부족해 전체 파인튜닝이 여전히 이긴다.
- 가중치를 병합하면 한 배치에서 여러 과제를 동시에 서빙하기 어색해진다.
- 내재적 저랭크 가설은 실증됐을 뿐 설명되진 않았다 — 이론은 나중에 따라왔다.

### 영향과 후속 연구

파인튜닝을 민주화했다: LoRA(+양자화 버전 QLoRA)는 개인이 LLM, 디퓨전 모델(스타일 LoRA), 로봇 정책을 적응시키는 표준 방법이다 — OpenVLA 같은 VLA를 GPU 한 장으로 파인튜닝하는 것도 LoRA 덕분. QLoRA, DoRA, AdaLoRA와 병합 LoRA 공유 생태계가 형성됐다.

### 연결

- 저렴한 적응을 가능하게 함: [[canonical-papers/notes/gpt-3|GPT-3]]급 모델, VLA(OpenVLA 파인튜닝)
- 계보: [[10-deep-learning/lineage|논문 계보도]]
