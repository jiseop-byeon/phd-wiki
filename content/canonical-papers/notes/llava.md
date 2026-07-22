---
title: "LLaVA — Visual Instruction Tuning"
authors: Haotian Liu, Chunyuan Li, Qingyang Wu, Yong Jae Lee
affiliation: University of Wisconsin–Madison, Microsoft Research, Columbia University
venue: NeurIPS
year: 2023
arxiv: https://arxiv.org/abs/2304.08485
pdf: https://arxiv.org/pdf/2304.08485
code: https://github.com/haotian-liu/LLaVA
project: https://llava-vl.github.io
tags: [paper, vlm]
status: to-read
---

**Liu et al., NeurIPS 2023** — [arXiv](https://arxiv.org/abs/2304.08485) · [PDF](https://arxiv.org/pdf/2304.08485) · [Code](https://github.com/haotian-liu/LLaVA) · [Official](https://llava-vl.github.io)

## English

**One-line summary**: Use GPT-4 to synthesize multimodal instruction-following data, then train the simplest possible architecture (CLIP encoder + linear projection + LLM) on it — the open recipe that democratized VLMs.

### Context

By early 2023, [[instructgpt|instruction tuning]] had turned LLMs into assistants, and [[flamingo|Flamingo]]/[[blip-2|BLIP-2]] had connected vision to LLMs — but as caption-style generators, not instruction followers. The missing piece was *data*: no dataset existed of images paired with diverse instructions and helpful responses. Human annotation at that scale was impractical.

### Method

> [!tip] Key intuition
> Two bets: (1) a strong LLM can *write the training data* — feed text-only GPT-4 the captions and box coordinates of an image and it can author conversations, descriptions, and reasoning Q&A "about" the image sight unseen; (2) the connector can be trivial — a single linear layer — if the instruction data is good.

- **Data**: 158K GPT-4-generated multimodal instruction samples from COCO annotations — conversations, detailed descriptions, complex reasoning.
- **Architecture**: frozen [[clip|CLIP]] ViT-L/14 → **one linear projection** → Vicuna LLM. That's all.
- **Training**: stage 1 aligns the projection on image-caption pairs (both towers frozen); stage 2 fine-tunes projection + LLM on the instruction data.
- LLaVA-1.5 (2023) upgraded to an MLP connector and academic VQA data, reaching SOTA across 11 benchmarks — still with the same minimal design.

### Results

- Near GPT-4V-style conversational behavior on unseen images; 85%+ relative score against text-only GPT-4 judging on a synthetic multimodal benchmark.
- With modest fine-tuning, then-SOTA on ScienceQA (with GPT-4 ensembling).
- The 1.5 revision showed the simple projection matches or beats Q-Former-class connectors given clean instruction data.

### Limitations & critique

- Judge-by-GPT-4 evaluation is circular (the judge authored the training distribution); later benchmarks (MMMU etc.) exposed real gaps.
- Single low-resolution image, hallucination-prone, weak OCR/counting — inherited from [[clip|CLIP]] features and small visual token budgets.
- Synthetic data caps quality at the teacher model's ability and biases.

### Impact & follow-ups

Set off the open-VLM explosion: the "encoder + projection + open LLM + synthetic instructions" recipe underlies LLaVA-NeXT, Qwen-VL-style lines, and countless domain VLMs. Crucially for robotics, VLA models are structurally LLaVA-like — OpenVLA literally fine-tunes a Prismatic/LLaVA-style backbone to emit robot actions.

### Connections

- Previous: [[clip|CLIP]] + [[instructgpt|InstructGPT]] (the two ingredients), [[blip-2|BLIP-2]]
- Next: RT-2, OpenVLA (VLM → VLA)
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: GPT-4로 멀티모달 지시-응답 데이터를 합성하고, 가장 단순한 구조(CLIP 인코더 + 선형 투영 + LLM)를 그 데이터로 학습 — VLM을 대중화한 오픈 레시피.

### 배경

2023년 초, [[instructgpt|지시 튜닝]]은 LLM을 어시스턴트로 바꿔 놨고 [[flamingo|Flamingo]]/[[blip-2|BLIP-2]]는 시각을 LLM에 연결해 놨다 — 하지만 캡션 생성기로서였지, 지시를 따르는 모델은 아니었다. 빠진 조각은 *데이터*: 이미지에 다양한 지시와 유용한 응답이 짝지어진 데이터셋이 없었고, 그 규모의 사람 주석은 비현실적이었다.

### 방법

> [!tip] 핵심 직관
> 두 가지 베팅: (1) 강한 LLM이 *학습 데이터를 대신 쓸 수 있다* — 텍스트 전용 GPT-4에 이미지의 캡션과 박스 좌표를 주면, 이미지를 보지 않고도 그 이미지에 "관한" 대화·묘사·추론 문답을 지어낼 수 있다. (2) 지시 데이터가 좋으면 연결자는 사소해도 된다 — 선형층 하나면 충분.

- **데이터**: COCO 주석에서 GPT-4가 생성한 15.8만 개 멀티모달 지시 샘플 — 대화, 상세 묘사, 복합 추론.
- **구조**: 얼린 [[clip|CLIP]] ViT-L/14 → **선형 투영 한 층** → Vicuna LLM. 이게 전부다.
- **학습**: 1단계는 이미지-캡션 쌍으로 투영층만 정렬(양쪽 타워 동결); 2단계는 지시 데이터로 투영층+LLM 파인튜닝.
- LLaVA-1.5(2023)는 MLP 연결자와 학술 VQA 데이터로 업그레이드해 11개 벤치마크 SOTA — 여전히 같은 미니멀 설계로.

### 결과

- 처음 보는 이미지에서 GPT-4V풍 대화 능력; 합성 멀티모달 벤치마크에서 텍스트 GPT-4 심판 기준 상대 점수 85%+.
- 가벼운 파인튜닝으로 ScienceQA 당시 SOTA(GPT-4 앙상블 포함).
- 1.5 개정판은 깨끗한 지시 데이터만 있으면 단순 투영이 Q-Former급 연결자와 대등하거나 낫다는 것을 보였다.

### 한계와 비판

- GPT-4 심판 평가는 순환적이다(심판이 학습 분포의 저자다); 이후 벤치마크(MMMU 등)가 실제 격차를 드러냈다.
- 저해상도 단일 이미지, 환각 취약, 약한 OCR/개수 세기 — [[clip|CLIP]] 특징과 적은 시각 토큰 예산에서 물려받은 약점.
- 합성 데이터는 품질 상한이 교사 모델의 능력과 편향에 묶인다.

### 영향과 후속 연구

오픈 VLM 폭발의 기폭제: "인코더 + 투영 + 오픈 LLM + 합성 지시 데이터" 레시피가 LLaVA-NeXT, Qwen-VL 계열, 무수한 도메인 VLM의 밑바탕이다. 로보틱스에 결정적인 점: VLA 모델은 구조적으로 LLaVA와 같다 — OpenVLA는 말 그대로 Prismatic(LLaVA풍) 백본을 파인튜닝해 로봇 행동을 출력한다.

### 연결

- 이전: [[clip|CLIP]] + [[instructgpt|InstructGPT]] (두 재료), [[blip-2|BLIP-2]]
- 다음: RT-2, OpenVLA (VLM → VLA)
- 계보: [[10-deep-learning/lineage|논문 계보도]]
