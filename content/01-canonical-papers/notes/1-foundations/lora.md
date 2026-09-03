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
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Hu et al., ICLR 2022** — [arXiv](https://arxiv.org/abs/2106.09685) · [PDF](https://arxiv.org/pdf/2106.09685) · [Code](https://github.com/microsoft/LoRA)

> [!note] 수학 준비물 · Math on-ramp
> [[02-foundations/linear-algebra|1. Linear Algebra §2 and §4]] — rank and the SVD (Eckart–Young) are the whole mathematics here. Note the honest distinction that page draws: LoRA does not SVD-approximate a finished update, it *parameterizes* the update as low-rank from the start.
> [[02-foundations/linear-algebra|선형대수 §2·§4]]의 랭크와 SVD(Eckart–Young)가 이 논문의 수학 전부다: "업데이트가 저랭크"라는 가설은 $\Delta W$를 얇은 행렬 둘의 곱으로 근사해도 된다는 뜻이다.

## English

**One-line summary**: Freeze the pretrained weights and learn only a low-rank update ΔW = BA per weight matrix — fine-tune giant models by training ~0.01–1% of parameters, with zero added inference latency.

### Context

By 2021, the pretrain-finetune paradigm ([[01-canonical-papers/notes/1-foundations/bert|BERT]]) collided with model scale ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] 175B): full fine-tuning means storing and serving a complete model copy *per task*. Existing parameter-efficient methods had costs — adapters add inference latency; prefix-tuning eats context length and optimizes poorly.

### Method

> [!tip] Key intuition
> Fine-tuning barely moves weights, and the movement has low *intrinsic rank* — the update lives in a small subspace. So parameterize the update itself as a product of two thin matrices and learn only that.

- For a frozen weight $W_0 \in \mathbb{R}^{d\times k}$, learn $\Delta W = BA$ with $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r\times k}$, rank $r \ll \min(d,k)$ (r = 1–64 works).
- Forward pass: $h = W_0 x + BAx$; $A$ initialized Gaussian, $B$ zero — so training starts from the pretrained model exactly.
- **Merge at deployment**: $W = W_0 + BA$ — no extra latency, unlike adapters. Task switching = swapping small LoRA weights.
- Applied to attention projections ($W_q$, $W_v$ suffice in the paper).
<svg viewBox="0 0 560 224" style="max-width:100%;height:auto" role="img" aria-label="full fine-tuning trains one large weight-update matrix while LoRA freezes it and trains two thin matrices whose product replaces it">
  <g font-size="11" fill="currentColor">
    <text x="60" y="20">full fine-tuning</text><text x="285" y="20">LoRA</text>
  </g>
  <g fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2">
    <rect x="60" y="34" width="110" height="110" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.2">
    <rect x="285" y="34" width="100" height="100" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2">
    <rect x="416" y="34" width="18" height="100" rx="2"/>
    <rect x="452" y="76" width="100" height="18" rx="2"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="86">&#916;W</text>
    <text x="335" y="80">W&#8320;</text>
    <text x="401" y="90">+</text>
    <text x="443" y="90">&#215;</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85" text-anchor="middle">
    <text x="115" y="102">d &#215; k, all trained</text>
    <text x="335" y="96">frozen</text>
    <text x="425" y="148">d &#215; r</text>
    <text x="502" y="112">r &#215; k</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="176">The product of the two thin matrices stands in for the large one. Counting a single matrix with</text>
    <text x="24" y="190">d = k = 4096 and r = 8: 4096&#178; = 16.8M trained values against 2 &#183; 4096 &#183; 8 = 65,536 &#8212; about 256&#215;.</text>
    <text x="24" y="204">The ratio a paper reports depends on which matrices got an adapter and at what r, which is why</text>
    <text x="24" y="218">the two figures above disagree; read the box before quoting either.</text>
  </g>
</svg>


### Results

- Matches or beats full fine-tuning on GLUE (RoBERTa/DeBERTa) and GPT-2/GPT-3 175B benchmarks while training a small fraction of the parameters. **Two different figures circulate for that fraction, and they are not the same claim:** the abstract says **10,000× fewer** trainable parameters (≈0.01%), while the GPT-3 table reports **4.7M** at rank $r{=}8$ and 37.7M at $r{=}64$ — and 4.7M against 175B is ≈**37,000×**, or 0.003%. Quote the abstract's round number or the table's exact one, but do not present one as arithmetic for the other.
- GPU memory for GPT-3 fine-tuning cut ~3×; checkpoint size from ~350GB to ~35MB.
- Analysis: learned updates strongly amplify directions already latent in $W_0$; very low rank suffices.

### Limitations & critique

- Optimal rank and placement are empirical; capacity can cap out on hard domain shifts (where full fine-tuning still wins).
- Batch-serving different tasks in one pass is awkward once weights are merged.
- The intrinsic-rank hypothesis is demonstrated, not explained — theory followed later.

### Impact & follow-ups

Democratized fine-tuning: LoRA (+QLoRA quantized variant) is *the* standard way individuals adapt LLMs, diffusion models (style LoRAs), and robot policies — fine-tuning [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]-scale VLAs like OpenVLA on a single GPU. Huge ecosystem: QLoRA, DoRA, AdaLoRA, and merged-LoRA model sharing.

> [!question] Reading the claim · 핵심 주장 읽는 법
> Low-rank adaptation concerns the trainable update, not the total size of the pretrained model. No added inference layer assumes the update can be merged appropriately. Check rank, target matrices, and matched fine-tuning budgets before extending the result to a new domain.

### Connections

- Enables cheap adaptation of: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]-class models, VLAs (OpenVLA fine-tuning)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 사전학습 가중치는 얼리고 가중치 행렬마다 저랭크 업데이트 ΔW = BA만 학습 — 파라미터의 0.01~1%만 훈련해서 거대 모델을 파인튜닝하고, 추론 지연은 0.

### 배경

2021년, 사전학습-파인튜닝 패러다임([[01-canonical-papers/notes/1-foundations/bert|BERT]])이 모델 규모([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] 175B)와 충돌했다: 전체 파인튜닝은 *과제마다* 완전한 모델 복사본을 저장·서빙해야 한다는 뜻이다. 기존의 파라미터 효율 기법들은 대가가 있었다 — 어댑터는 추론 지연을 더하고, prefix-tuning은 문맥 길이를 잡아먹으며 최적화도 불안정했다.

### 방법

> [!tip] 핵심 직관
> 파인튜닝은 가중치를 거의 움직이지 않고, 그 움직임의 *내재적 랭크*는 낮다 — 업데이트가 작은 부분공간 안에 산다. 그렇다면 업데이트 자체를 얇은 행렬 두 개의 곱으로 파라미터화하고 그것만 배우자.

- 얼린 가중치 $W_0 \in \mathbb{R}^{d\times k}$에 대해 $\Delta W = BA$를 학습: $B \in \mathbb{R}^{d\times r}$, $A \in \mathbb{R}^{r\times k}$, 랭크 $r \ll \min(d,k)$ (r = 1~64면 충분).
- 순전파: $h = W_0 x + BAx$; $A$는 가우시안, $B$는 0으로 초기화 — 학습이 정확히 사전학습 모델에서 출발한다.
- **배포 시 병합**: $W = W_0 + BA$ — 어댑터와 달리 추가 지연이 없다. 과제 전환 = 작은 LoRA 가중치 교체.
- 어텐션 투영에 적용(논문에서는 $W_q$, $W_v$면 충분).
<svg viewBox="0 0 560 224" style="max-width:100%;height:auto" role="img" aria-label="전체 파인튜닝은 큰 가중치 갱신 행렬 하나를 학습하고 LoRA는 그것을 얼린 뒤 곱이 그것을 대신하는 얇은 행렬 둘을 학습한다">
  <g font-size="11" fill="currentColor">
    <text x="60" y="20">전체 파인튜닝</text><text x="285" y="20">LoRA</text>
  </g>
  <g fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2">
    <rect x="60" y="34" width="110" height="110" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.2">
    <rect x="285" y="34" width="100" height="100" rx="3"/>
  </g>
  <g fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.2">
    <rect x="416" y="34" width="18" height="100" rx="2"/>
    <rect x="452" y="76" width="100" height="18" rx="2"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="115" y="86">&#916;W</text>
    <text x="335" y="80">W&#8320;</text>
    <text x="401" y="90">+</text>
    <text x="443" y="90">&#215;</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85" text-anchor="middle">
    <text x="115" y="102">d &#215; k, 전부 학습</text>
    <text x="335" y="96">얼림</text>
    <text x="425" y="148">d &#215; r</text>
    <text x="502" y="112">r &#215; k</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.9">
    <text x="24" y="176">얇은 두 행렬의 곱이 큰 행렬을 대신한다. 행렬 하나만 놓고 세어 보면 d = k = 4096, r = 8일 때</text>
    <text x="24" y="190">4096&#178; = 1,678만 개 대 2 &#183; 4096 &#183; 8 = 65,536개 &#8212; 약 256배다.</text>
    <text x="24" y="204">논문이 보고하는 비율은 어느 행렬에 얼마의 r로 붙였느냐에 따라 달라지고, 위의 두 수치가</text>
    <text x="24" y="218">갈리는 이유가 그것이다. 어느 쪽이든 인용하기 전에 그 상자를 읽어라.</text>
  </g>
</svg>


### 결과

- GLUE(RoBERTa/DeBERTa)와 GPT-2/GPT-3 175B 벤치마크에서 전체 파인튜닝과 대등하거나 상회 — 훈련 파라미터는 극히 일부다. **그 '일부'를 가리키는 수치가 둘 돌아다니는데 서로 다른 주장이다:** 초록은 훈련 파라미터 **10,000배 감소**(≈0.01%)라 하고, GPT-3 표는 $r{=}8$에서 **470만**, $r{=}64$에서 3,770만을 보고한다 — 470만 대 175B는 약 **37,000배**, 즉 0.003%다. 초록의 어림수든 표의 정확한 수든 하나를 인용하되, 한쪽을 다른 쪽의 산술 근거처럼 붙이지 마라.
- GPT-3 파인튜닝의 GPU 메모리 약 3배 절감; 체크포인트 크기 약 350GB → 35MB.
- 분석: 학습된 업데이트는 $W_0$에 이미 잠재된 방향들을 증폭한다; 아주 낮은 랭크로 충분하다.

### 한계와 비판

- 최적 랭크와 적용 위치는 경험적이다; 어려운 도메인 전환에서는 용량이 부족해 전체 파인튜닝이 여전히 이긴다.
- 가중치를 병합하면 한 배치에서 여러 과제를 동시에 서빙하기 어색해진다.
- 내재적 저랭크 가설은 실증됐을 뿐 설명되진 않았다 — 이론은 나중에 따라왔다.

### 영향과 후속 연구

파인튜닝을 민주화했다: LoRA(+양자화 버전 QLoRA)는 개인이 LLM, 디퓨전 모델(스타일 LoRA), 로봇 정책을 적응시키는 표준 방법이다 — OpenVLA 같은 VLA를 GPU 한 장으로 파인튜닝하는 것도 LoRA 덕분. QLoRA, DoRA, AdaLoRA와 병합 LoRA 공유 생태계가 형성됐다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 저계수 적응은 학습할 갱신에 관한 것으로 사전학습 모델 전체 크기는 그대로다. 추론 층을 추가하지 않는다는 말에는 갱신을 적절히 합칠 수 있다는 조건이 있다. 새 도메인에 적용하기 전에 계수, 대상 행렬, 미세조정 예산을 확인한다.

### 연결

- 저렴한 적응을 가능하게 함: [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]급 모델, VLA(OpenVLA 파인튜닝)
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Compute the number of trained parameters in $\Delta W = BA$ from $d, k, r$ · $\Delta W = BA$의 학습 파라미터 수를 $d, k, r$로 계산할 수 있다
- [ ] State what the $B = 0$ initialization guarantees · $B = 0$ 초기화가 보장하는 것을 말할 수 있다
- [ ] Explain why merging at deployment leaves zero inference latency (and how that differs from adapters) · 배포 시 병합으로 추론 지연이 0인 이유(어댑터와의 차이)를 설명할 수 있다
- [ ] Say why the intrinsic low-rank hypothesis is an empirical finding rather than an explanation · 내재적 저랭크 가설이 실증이지 설명이 아니라는 점을 말할 수 있다
