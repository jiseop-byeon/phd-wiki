---
title: "CLIP — Learning Transferable Visual Models From Natural Language Supervision"
authors: Alec Radford, Jong Wook Kim, Chris Hallacy, et al.
affiliation: OpenAI
venue: ICML
year: 2021
arxiv: https://arxiv.org/abs/2103.00020
pdf: https://arxiv.org/pdf/2103.00020
code: https://github.com/openai/CLIP
tags: [paper, foundations, vlm, computer-vision]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Radford et al., ICML 2021** — [arXiv](https://arxiv.org/abs/2103.00020) · [PDF](https://arxiv.org/pdf/2103.00020) · [Code](https://github.com/openai/CLIP)

> [!note] Math on-ramp · 수학 준비물
> Two prerequisites, both short. [[02-foundations/linear-algebra|1. Linear Algebra §1]]: cosine similarity is a normalized dot product, and [[02-foundations/linear-algebra|§6]] explains why unrelated high-dimensional embeddings score near zero — the geometric reason retrieval over 400M pairs is possible at all. [[02-foundations/information-theory|5. Information Theory §4]]: the InfoNCE loss is a lower bound on mutual information, so "align the two modalities" has a precise meaning.
> 선수 지식 둘, 둘 다 짧다. [[02-foundations/linear-algebra|1. 선형대수 §1]]: 코사인 유사도는 정규화된 내적이고, 무관한 고차원 임베딩이 왜 0 근처 점수를 받는지는 [[02-foundations/linear-algebra|§6]] — 4억 쌍에 대한 검색이 애초에 가능한 기하학적 이유다. [[02-foundations/information-theory|5. 정보이론 §4]]: InfoNCE 손실이 상호정보량의 하한이므로 "두 모달리티를 정렬한다"는 말에 정확한 뜻이 생긴다.

## English

**One-line summary**: Contrastively align 400M image-text pairs into a shared embedding space — vision learns from raw language supervision, and classification becomes zero-shot prompting.

### Context

Vision models were trained on fixed label sets (1000 ImageNet classes): expensive to build and frozen in scope — recognizing anything new meant new labels and retraining. NLP had just shown ([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]) that web-scale weak supervision produces transferable, promptable models. Could vision learn from the web's *natural pairing* of images and text instead of curated labels?

### Method

> [!tip] Key intuition
> Don't predict the exact caption (too hard, wasteful) — just learn *which caption goes with which image*. Matching in a shared embedding space is an easier objective that still forces semantic understanding, and it scales to noisy web data.

- Two encoders: image (ResNet or [[01-canonical-papers/notes/1-foundations/vit|ViT]]) and text (Transformer), each projecting into a shared space.
- **Contrastive objective**: within a batch of N pairs, maximize cosine similarity of the N correct pairs against the N²−N incorrect ones (symmetric InfoNCE, learned temperature).

<svg viewBox="0 0 620 236" style="max-width:100%;height:auto" role="img" aria-label="the CLIP batch as a similarity matrix: N matches on the diagonal, everything else a negative">
  <rect x="150" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="167" y="40">T&#8321;</text><text x="205" y="40">T&#8322;</text><text x="243" y="40">T&#8323;</text><text x="281" y="40">T&#8324;</text>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="end">
    <text x="144" y="68">I&#8321;</text><text x="144" y="106">I&#8322;</text><text x="144" y="144">I&#8323;</text><text x="144" y="182">I&#8324;</text>
  </g>
  <g fill="currentColor"><rect x="318" y="60" width="12" height="12" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/><rect x="318" y="86" width="12" height="12" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/></g>
  <g font-size="11" fill="currentColor">
    <text x="150" y="24">cosine similarity of every image with every caption</text>
    <text x="338" y="70">the N correct pairs &#8212; pushed up</text>
    <text x="338" y="96">the N&#178; &#8722; N wrong pairs &#8212; pushed down</text>
    <text x="338" y="132">loss = softmax across each row</text>
    <text x="338" y="150">+ softmax down each column</text>
    <text x="30" y="212" opacity="0.9">A batch of N gives N positives and N&#178; &#8722; N negatives for free &#8212; which is why batch size is part of</text>
    <text x="30" y="228" opacity="0.9">the method, not a training detail. At N = 4 that is 4 against 12; at CLIP's 32,768 it is 32k against a billion.</text>
  </g>
</svg>


- Trained on **WIT-400M**, a web-collected dataset of 400M image-text pairs.
- **Zero-shot classification**: embed prompts like "a photo of a {class}" and pick the nearest class embedding — the label set is now free-form text.

### Results

- Zero-shot CLIP matches the original supervised ResNet-50 on **ImageNet without seeing any of its training labels**, and is competitive across 30+ datasets (OCR, actions, fine-grained).
- Far more robust to distribution shift (ImageNet-V2/R/A, sketches) than supervised counterparts — commonly interpreted as learning concepts rather than dataset idiosyncrasies (an interpretation the robustness numbers support but do not prove; training-distribution breadth is a competing explanation).
- Contrastive objective is markedly more compute-efficient than generative alternatives — ~4× vs a bag-of-words prediction baseline and ~12× vs transformer captioning in the paper's comparison.

### Limitations & critique

- Weak at counting, spatial relations, and fine compositional structure — a limitation inherited by every CLIP-based VLM since.
- Zero-shot performance depends on prompt engineering; web data embeds social biases directly into the embedding space.
- Not generative: CLIP scores image-text agreement but cannot produce text — VLMs bolt CLIP encoders onto LLMs to fix this.

### Impact & follow-ups

The foundation of the multimodal era: CLIP encoders power text-to-image diffusion guidance (Stable Diffusion), open-vocabulary detection/segmentation, and are the visual front-end of VLMs (LLaVA, Flamingo lineage) — and through them, VLAs: RT-2's "vision-language-action" is CLIP's alignment idea extended to robot actions. Successors: ALIGN, OpenCLIP, SigLIP.

### Connections

- Previous: [[01-canonical-papers/notes/1-foundations/vit|ViT]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] (web-scale supervision) · Next: Flamingo, LLaVA → RT-2
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 4억 쌍의 이미지-텍스트를 대조학습으로 공유 임베딩 공간에 정렬 — 비전이 날것의 언어 감독에서 배우게 되고, 분류는 zero-shot 프롬프팅이 된다.

### 배경

비전 모델은 고정된 라벨 집합(ImageNet 1000 클래스)으로 학습됐다: 만들기 비싸고 범위가 얼어붙어 있어, 새로운 것을 인식하려면 새 라벨과 재학습이 필요했다. NLP는 웹 규모의 약한 감독이 전이 가능하고 프롬프트 가능한 모델을 만든다는 것을 막 보여준 참이었다([[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]]). 비전도 선별된 라벨 대신 웹에 *자연적으로 존재하는* 이미지-텍스트 쌍에서 배울 수 없을까?

### 방법

> [!tip] 핵심 직관
> 정확한 캡션을 예측하려 하지 마라(너무 어렵고 낭비다) — *어느 캡션이 어느 이미지 것인지*만 배우자. 공유 임베딩 공간에서의 매칭은 더 쉬운 목표지만 여전히 의미 이해를 강제하고, 시끄러운 웹 데이터로도 스케일된다.

- 인코더 둘: 이미지(ResNet 또는 [[01-canonical-papers/notes/1-foundations/vit|ViT]])와 텍스트(Transformer), 각각 공유 공간으로 투영.
- **대조 목적함수**: N쌍 배치에서 올바른 N쌍의 코사인 유사도를 나머지 N²−N개의 잘못된 쌍 대비 최대화(대칭 InfoNCE, 학습된 온도).

<svg viewBox="0 0 620 236" style="max-width:100%;height:auto" role="img" aria-label="CLIP 배치를 유사도 행렬로 본 것: 대각선의 N개가 정답, 나머지는 전부 음성">
  <rect x="150" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="46" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="84" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="122" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="150" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="188" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="226" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/>
  <rect x="264" y="160" width="34" height="34" rx="2" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="167" y="40">T&#8321;</text><text x="205" y="40">T&#8322;</text><text x="243" y="40">T&#8323;</text><text x="281" y="40">T&#8324;</text>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="end">
    <text x="144" y="68">I&#8321;</text><text x="144" y="106">I&#8322;</text><text x="144" y="144">I&#8323;</text><text x="144" y="182">I&#8324;</text>
  </g>
  <g fill="currentColor"><rect x="318" y="60" width="12" height="12" fill-opacity="0.30" stroke="currentColor" stroke-width="0.8"/><rect x="318" y="86" width="12" height="12" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8"/></g>
  <g font-size="11" fill="currentColor">
    <text x="150" y="24">모든 이미지와 모든 캡션 사이의 코사인 유사도</text>
    <text x="338" y="70">정답 N쌍 &#8212; 올린다</text>
    <text x="338" y="96">틀린 N&#178; &#8722; N쌍 &#8212; 내린다</text>
    <text x="338" y="132">손실 = 각 행에 대한 softmax</text>
    <text x="338" y="150">+ 각 열에 대한 softmax</text>
    <text x="30" y="212" opacity="0.9">배치 크기 N 하나가 정답 N개와 음성 N&#178; &#8722; N개를 공짜로 만든다 &#8212; 배치 크기가 학습 디테일이 아니라</text>
    <text x="30" y="228" opacity="0.9">방법의 일부인 이유다. N = 4면 4 대 12, CLIP의 32,768이면 3만 2천 대 10억이다.</text>
  </g>
</svg>


- **WIT-400M** — 웹에서 수집한 4억 이미지-텍스트 쌍으로 학습.
- **Zero-shot 분류**: "a photo of a {class}" 같은 프롬프트를 임베딩해 가장 가까운 클래스를 선택 — 라벨 집합이 자유 텍스트가 된다.

### 결과

- Zero-shot CLIP이 **ImageNet 학습 라벨을 하나도 보지 않고** 지도학습 ResNet-50과 대등; 30개 이상의 데이터셋(OCR, 행동, 세밀 분류)에서 경쟁력.
- 분포 이동(ImageNet-V2/R/A, 스케치)에 지도학습 모델보다 훨씬 강건 — 흔히 "데이터셋의 버릇이 아니라 개념을 배웠다"로 해석된다(강건성 수치가 지지하지만 증명하지는 않는 해석 — 학습 분포의 폭 자체가 경쟁 설명이다).
- 대조 목적함수는 생성적 대안보다 눈에 띄게 연산 효율적 — 논문의 비교에서 bag-of-words 예측 대비 약 4배, 트랜스포머 캡셔닝 대비 약 12배.

### 한계와 비판

- 개수 세기, 공간 관계, 세밀한 조합 구조에 약하다 — 이후 모든 CLIP 기반 VLM이 물려받은 한계.
- Zero-shot 성능이 프롬프트 엔지니어링에 의존; 웹 데이터의 사회적 편향이 임베딩 공간에 그대로 들어간다.
- 생성 불가: CLIP은 이미지-텍스트 일치를 점수화할 뿐 텍스트를 만들지 못한다 — VLM들이 CLIP 인코더를 LLM에 접붙여 해결.

### 영향과 후속 연구

멀티모달 시대의 초석: CLIP 인코더는 텍스트-이미지 디퓨전의 가이던스(Stable Diffusion), open-vocabulary 검출·분할을 구동하고, VLM(LLaVA, Flamingo 계열)의 시각 front-end다 — 그리고 그 연장선에서 VLA로: RT-2의 "vision-language-action"은 CLIP의 정렬 아이디어를 로봇 행동까지 확장한 것이다. 후속: ALIGN, OpenCLIP, SigLIP.

### 연결

- 이전: [[01-canonical-papers/notes/1-foundations/vit|ViT]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]] (웹 규모 감독) · 다음: Flamingo, LLaVA → RT-2
- 계보: [[03-deep-learning/lineage|논문 계보도]]

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "Transferable visual models from natural language supervision" — the substance is zero-shot transfer and robustness to distribution shift, not the best performance on every vision task (it is weak on fine-grained classification and counting). And the data condition, 400 million pairs, is built into the claim: data scale is half the result, not the method alone.
>
> "transferable visual models from natural language supervision" — 주장의 핵심은 zero-shot 전이와 분포 이동 강건성이지, 모든 시각 과제의 최고 성능이 아니다(세밀 분류·카운팅에선 약하다). 그리고 "4억 쌍"이라는 데이터 조건이 주장에 내장되어 있다 — 방법만이 아니라 데이터 규모가 결과의 절반이다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain how the contrastive objective differs from "predict the exact caption" and why that makes it robust to web noise · 대조 목적함수가 "정확한 캡션 예측"과 어떻게 다르고 왜 웹 노이즈에 강한지 설명할 수 있다
- [ ] Describe zero-shot classification procedurally as a similarity comparison against class-prompt embeddings · zero-shot 분류 = 클래스 프롬프트 임베딩과의 유사도 비교임을 절차 수준에서 말할 수 있다
- [ ] Separate why it is robust to distribution shift from why it is weak at counting and spatial relations · 분포 이동에 강한 이유와 개수 세기·공간 관계에 약한 이유를 구분해 말할 수 있다
- [ ] Name at least two places a CLIP encoder is reused as a component (VLM vision encoder, diffusion text conditioning, …) · CLIP 인코더가 부품으로 들어가는 곳을 두 가지 이상(VLM 시각 인코더, 디퓨전 텍스트 조건 등) 들 수 있다
