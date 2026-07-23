---
title: "BLIP-2 — Bootstrapping Language-Image Pre-training with Frozen Encoders"
authors: Junnan Li, Dongxu Li, Silvio Savarese, Steven Hoi
affiliation: Salesforce Research
venue: ICML
year: 2023
arxiv: https://arxiv.org/abs/2301.12597
pdf: https://arxiv.org/pdf/2301.12597
code: https://github.com/salesforce/LAVIS
tags: [paper, vlm]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Li et al., ICML 2023** — [arXiv](https://arxiv.org/abs/2301.12597) · [PDF](https://arxiv.org/pdf/2301.12597) · [Code](https://github.com/salesforce/LAVIS)

## English

**One-line summary**: A small Q-Former distills an image into 32 query tokens through two-stage pretraining, connecting frozen vision encoders to frozen LLMs at a fraction of Flamingo's training cost.

### Context

[[flamingo|Flamingo]] proved the frozen-backbone recipe but its connector was heavy (billions of trainable parameters) and its data web-scale private. The efficiency question: what is the *minimal* trainable bridge that closes the modality gap between a frozen image encoder and a frozen LLM?

### Method

> [!tip] Key intuition
> The connector's real job is translation: extract only the visual information the language model can use, in a form it can read. So train a tiny "interpreter" (Q-Former) first to *understand* images with language supervision, then teach it to *speak* the LLM's input language.

- **Q-Former**: a small Transformer with **32 learned query vectors** that cross-attend to frozen image features — the image becomes a fixed 32-token summary regardless of resolution.
- **Stage 1 (representation learning)**: with the frozen image encoder, train on image-text contrastive, image-text matching, and image-grounded text generation objectives — forcing queries to extract text-relevant visual content.
- **Stage 2 (generative pretraining)**: plug the 32 tokens (via a linear projection) into a frozen LLM (OPT or FlanT5) as soft visual prompts; train the Q-Former so the LLM can caption from them.
- Trainable parameters: ~188M — **~54× fewer than Flamingo's** trainable footprint.

### Results

- Zero-shot VQAv2: outperforms Flamingo-80B with 54× fewer trainable parameters.
- SOTA at the time on captioning and retrieval benchmarks; instruction-following image-to-text emerges when paired with FlanT5.
- Demonstrated the modality gap can be closed with a compact, reusable module.

### Limitations & critique

- No in-context learning over multiple images (single-image conditioning; the LLM never saw interleaved data).
- 32 tokens bottleneck fine-grained detail — OCR-heavy and spatial tasks suffer; later VLMs went back to more visual tokens.
- Frozen LLM inherits its knowledge cutoff and hallucinations; the two-stage pipeline adds complexity that [[llava|LLaVA]] soon showed may be unnecessary.

### Impact & follow-ups

The Q-Former became the era's standard connector — reused by InstructBLIP, MiniGPT-4, and video variants. Together with [[flamingo|Flamingo]] it framed the design space (heavy cross-attention vs. compact query bottleneck vs. plain projection) that [[llava|LLaVA]] resolved in favor of simplicity.

### Connections

- Previous: [[clip|CLIP]], [[flamingo|Flamingo]] · Next: [[llava|LLaVA]], InstructBLIP
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 작은 Q-Former가 2단계 사전학습으로 이미지를 32개 쿼리 토큰으로 증류해, 얼린 비전 인코더와 얼린 LLM을 Flamingo의 몇십분의 일 비용으로 연결한다.

### 배경

[[flamingo|Flamingo]]가 얼린 백본 레시피를 증명했지만, 연결자가 무겁고(수십억 학습 파라미터) 데이터는 웹 규모의 비공개였다. 효율의 질문: 얼린 이미지 인코더와 얼린 LLM 사이의 모달리티 간극을 닫는 *최소한의* 학습 가능한 다리는 무엇인가?

### 방법

> [!tip] 핵심 직관
> 연결자의 진짜 일은 번역이다: 언어모델이 쓸 수 있는 시각 정보만, 언어모델이 읽을 수 있는 형태로 추출하는 것. 그러니 작은 "통역사"(Q-Former)에게 먼저 언어 감독으로 이미지를 *이해*하는 법을 가르치고, 그다음 LLM의 입력 언어로 *말하는* 법을 가르치자.

- **Q-Former**: **학습된 쿼리 벡터 32개**가 얼린 이미지 특징에 cross-attention하는 작은 Transformer — 해상도와 무관하게 이미지가 고정된 32토큰 요약이 된다.
- **1단계 (표현 학습)**: 얼린 이미지 인코더와 함께 이미지-텍스트 대조·매칭·이미지 기반 텍스트 생성 목적함수로 학습 — 쿼리들이 텍스트와 관련된 시각 정보를 뽑도록 강제.
- **2단계 (생성 사전학습)**: 32개 토큰을 (선형 투영을 거쳐) 얼린 LLM(OPT 또는 FlanT5)에 소프트 시각 프롬프트로 주입; LLM이 그것으로 캡션을 생성할 수 있도록 Q-Former를 학습.
- 학습 파라미터 약 1.88억 — **Flamingo 대비 약 54배 적다**.

### 결과

- Zero-shot VQAv2에서 54배 적은 학습 파라미터로 Flamingo-80B를 추월.
- 캡셔닝·검색 벤치마크에서 당시 SOTA; FlanT5와 결합하면 지시를 따르는 이미지-텍스트 생성이 나타난다.
- 모달리티 간극을 작고 재사용 가능한 모듈로 닫을 수 있음을 실증.

### 한계와 비판

- 여러 이미지에 걸친 in-context 학습 불가(단일 이미지 조건; LLM이 혼재 데이터를 본 적 없음).
- 32토큰이 세밀한 정보를 병목화 — OCR·공간 과제에서 약하다; 이후 VLM들은 다시 시각 토큰 수를 늘렸다.
- 얼린 LLM의 지식 시점·환각을 물려받고, 2단계 파이프라인의 복잡성은 [[llava|LLaVA]]가 곧 불필요할 수 있음을 보였다.

### 영향과 후속 연구

Q-Former는 그 시대의 표준 연결자가 됐다 — InstructBLIP, MiniGPT-4, 비디오 변형들이 재사용. [[flamingo|Flamingo]]와 함께 "무거운 cross-attention vs 작은 쿼리 병목 vs 단순 투영"이라는 설계 공간을 정의했고, [[llava|LLaVA]]가 단순함의 손을 들어주며 결론냈다.

### 연결

- 이전: [[clip|CLIP]], [[flamingo|Flamingo]] · 다음: [[llava|LLaVA]], InstructBLIP
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Q-Former 병목(32 토큰)의 역할과 비용 절감을 말할 수 있다
- [ ] 2단계 사전학습이 각각 가르치는 것을 말할 수 있다
- [ ] LLaVA가 이 복잡성을 어떻게 우회했는지 말할 수 있다
