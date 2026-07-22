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
status: to-read
---

**Radford et al., ICML 2021** — [arXiv](https://arxiv.org/abs/2103.00020) · [PDF](https://arxiv.org/pdf/2103.00020) · [Code](https://github.com/openai/CLIP)

## English

**One-line summary**: Contrastively align 400M image-text pairs into a shared embedding space — vision learns from raw language supervision, and classification becomes zero-shot prompting.

### Context

Vision models were trained on fixed label sets (1000 ImageNet classes): expensive to build and frozen in scope — recognizing anything new meant new labels and retraining. NLP had just shown ([[canonical-papers/notes/gpt-3|GPT-3]]) that web-scale weak supervision produces transferable, promptable models. Could vision learn from the web's *natural pairing* of images and text instead of curated labels?

### Method

> [!tip] Key intuition
> Don't predict the exact caption (too hard, wasteful) — just learn *which caption goes with which image*. Matching in a shared embedding space is an easier objective that still forces semantic understanding, and it scales to noisy web data.

- Two encoders: image (ResNet or [[canonical-papers/notes/vit|ViT]]) and text (Transformer), each projecting into a shared space.
- **Contrastive objective**: within a batch of N pairs, maximize cosine similarity of the N correct pairs against the N²−N incorrect ones (symmetric InfoNCE, learned temperature).
- Trained on **WIT-400M**, a web-collected dataset of 400M image-text pairs.
- **Zero-shot classification**: embed prompts like "a photo of a {class}" and pick the nearest class embedding — the label set is now free-form text.

### Results

- Zero-shot CLIP matches the original supervised ResNet-50 on **ImageNet without seeing any of its training labels**, and is competitive across 30+ datasets (OCR, actions, fine-grained).
- Far more robust to distribution shift (ImageNet-V2/R/A sketches) than supervised counterparts — it learned concepts, not dataset idiosyncrasies.
- Contrastive objective is ~4–10× more compute-efficient than caption prediction.

### Limitations & critique

- Weak at counting, spatial relations, and fine compositional structure — a limitation inherited by every CLIP-based VLM since.
- Zero-shot performance depends on prompt engineering; web data embeds social biases directly into the embedding space.
- Not generative: CLIP scores image-text agreement but cannot produce text — VLMs bolt CLIP encoders onto LLMs to fix this.

### Impact & follow-ups

The foundation of the multimodal era: CLIP encoders power text-to-image diffusion guidance (Stable Diffusion), open-vocabulary detection/segmentation, and are the visual front-end of VLMs (LLaVA, Flamingo lineage) — and through them, VLAs: RT-2's "vision-language-action" is CLIP's alignment idea extended to robot actions. Successors: ALIGN, OpenCLIP, SigLIP.

### Connections

- Previous: [[canonical-papers/notes/vit|ViT]], [[canonical-papers/notes/gpt-3|GPT-3]] (web-scale supervision) · Next: Flamingo, LLaVA → RT-2
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 4억 쌍의 이미지-텍스트를 대조학습으로 공유 임베딩 공간에 정렬 — 비전이 날것의 언어 감독에서 배우게 되고, 분류는 zero-shot 프롬프팅이 된다.

### 배경

비전 모델은 고정된 라벨 집합(ImageNet 1000 클래스)으로 학습됐다: 만들기 비싸고 범위가 얼어붙어 있어, 새로운 것을 인식하려면 새 라벨과 재학습이 필요했다. NLP는 웹 규모의 약한 감독이 전이 가능하고 프롬프트 가능한 모델을 만든다는 것을 막 보여준 참이었다([[canonical-papers/notes/gpt-3|GPT-3]]). 비전도 선별된 라벨 대신 웹에 *자연적으로 존재하는* 이미지-텍스트 쌍에서 배울 수 없을까?

### 방법

> [!tip] 핵심 직관
> 정확한 캡션을 예측하려 하지 마라(너무 어렵고 낭비다) — *어느 캡션이 어느 이미지 것인지*만 배우자. 공유 임베딩 공간에서의 매칭은 더 쉬운 목표지만 여전히 의미 이해를 강제하고, 시끄러운 웹 데이터로도 스케일된다.

- 인코더 둘: 이미지(ResNet 또는 [[canonical-papers/notes/vit|ViT]])와 텍스트(Transformer), 각각 공유 공간으로 투영.
- **대조 목적함수**: N쌍 배치에서 올바른 N쌍의 코사인 유사도를 나머지 N²−N개의 잘못된 쌍 대비 최대화(대칭 InfoNCE, 학습된 온도).
- **WIT-400M** — 웹에서 수집한 4억 이미지-텍스트 쌍으로 학습.
- **Zero-shot 분류**: "a photo of a {class}" 같은 프롬프트를 임베딩해 가장 가까운 클래스를 선택 — 라벨 집합이 자유 텍스트가 된다.

### 결과

- Zero-shot CLIP이 **ImageNet 학습 라벨을 하나도 보지 않고** 지도학습 ResNet-50과 대등; 30개 이상의 데이터셋(OCR, 행동, 세밀 분류)에서 경쟁력.
- 분포 이동(ImageNet-V2/R/A, 스케치)에 지도학습 모델보다 훨씬 강건 — 데이터셋의 버릇이 아니라 개념을 배웠다는 뜻.
- 대조 목적함수는 캡션 예측보다 4~10배 연산 효율적.

### 한계와 비판

- 개수 세기, 공간 관계, 세밀한 조합 구조에 약하다 — 이후 모든 CLIP 기반 VLM이 물려받은 한계.
- Zero-shot 성능이 프롬프트 엔지니어링에 의존; 웹 데이터의 사회적 편향이 임베딩 공간에 그대로 들어간다.
- 생성 불가: CLIP은 이미지-텍스트 일치를 점수화할 뿐 텍스트를 만들지 못한다 — VLM들이 CLIP 인코더를 LLM에 접붙여 해결.

### 영향과 후속 연구

멀티모달 시대의 초석: CLIP 인코더는 텍스트-이미지 디퓨전의 가이던스(Stable Diffusion), open-vocabulary 검출·분할을 구동하고, VLM(LLaVA, Flamingo 계열)의 시각 front-end다 — 그리고 그 연장선에서 VLA로: RT-2의 "vision-language-action"은 CLIP의 정렬 아이디어를 로봇 행동까지 확장한 것이다. 후속: ALIGN, OpenCLIP, SigLIP.

### 연결

- 이전: [[canonical-papers/notes/vit|ViT]], [[canonical-papers/notes/gpt-3|GPT-3]] (웹 규모 감독) · 다음: Flamingo, LLaVA → RT-2
- 계보: [[10-deep-learning/lineage|논문 계보도]]
