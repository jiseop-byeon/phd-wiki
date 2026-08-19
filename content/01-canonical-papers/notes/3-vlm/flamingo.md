---
title: "Flamingo — a Visual Language Model for Few-Shot Learning"
authors: Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, et al.
affiliation: DeepMind
venue: NeurIPS
year: 2022
arxiv: https://arxiv.org/abs/2204.14198
pdf: https://arxiv.org/pdf/2204.14198
code: https://github.com/mlfoundations/open_flamingo
tags: [paper, vlm]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Alayrac et al., NeurIPS 2022** — [arXiv](https://arxiv.org/abs/2204.14198) · [PDF](https://arxiv.org/pdf/2204.14198) · [Code (open repro)](https://github.com/mlfoundations/open_flamingo)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]] (the frozen vision side) and [[02-foundations/neural-network-basics|0.7 §6]] for *frozen* — the whole design question here is which parts receive gradient and which do not, so that one word carries the paper.
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]](얼어붙은 비전 쪽)과 *frozen*의 뜻은 [[02-foundations/neural-network-basics|0.7 §6]] — 여기서 설계 질문 전체가 "어느 부분이 그래디언트를 받고 어느 부분이 받지 않는가"이므로, 그 한 단어가 논문을 떠받친다.

## English

**One-line summary**: Bridge a frozen vision encoder and a frozen LLM with trainable connector layers (Perceiver Resampler + gated cross-attention — themselves billions of parameters at the 80B scale) — the resulting VLM inherits the LLM's few-shot learning and handles interleaved image-text sequences.

### Context

[[clip|CLIP]] could match images and text but not generate; [[gpt-3|GPT-3]] could reason in language but not see. Training a giant multimodal model from scratch would waste both pretrained investments. The engineering question of 2022: how do you *graft* vision onto a frozen LLM without destroying what it knows?

### Method

> [!tip] Key intuition
> Keep both pretrained giants frozen; learn only the "adapters" between them. If the connector feeds visual tokens gently into the LM (starting from a no-op), the LM's abilities — including in-context few-shot learning — transfer to the multimodal setting for free.

- **Frozen parts**: a contrastively pretrained NFNet vision encoder + Chinchilla LM (up to 70B).
- **Perceiver Resampler**: compresses variable-length visual features into a fixed small set of visual tokens.
- **Gated cross-attention layers** interleaved between frozen LM blocks; their tanh gates start at zero, so training begins exactly at the pretrained LM and learns to blend vision in gradually.
- Trained on web-scale **interleaved image-text sequences** (M3W) plus image/video-text pairs — the interleaving is what enables few-shot prompting with (image, text) example pairs.

### Results

- Few-shot SOTA on 16 multimodal benchmarks (VQA, captioning, video QA); with 32 shots, **beats fine-tuned SOTA on 6 of them** — without any task-specific training.
- Performance scales with LM size and shot count, mirroring GPT-3's scaling behavior in the multimodal domain.

### Limitations & critique

- Closed model and dataset; the open reproduction (OpenFlamingo) lags in quality.
- Inherits LM weaknesses: hallucination, weak classification vs contrastive models, sensitivity to prompt design.
- Gated cross-attention adds many parameters per LM layer — later connectors ([[blip-2|BLIP-2]]'s Q-Former, [[llava|LLaVA]]'s projection) proved far cheaper.

### Impact & follow-ups

Defined the frozen-backbone + connector recipe every subsequent VLM refines — [[blip-2|BLIP-2]], [[llava|LLaVA]], IDEFICS, and the perception stack of VLAs. Interleaved-data training became standard for multimodal in-context learning.

### Connections

- Previous: [[clip|CLIP]] (vision side), [[gpt-3|GPT-3]] (few-shot paradigm)
- Next: [[blip-2|BLIP-2]] → [[llava|LLaVA]] → RT-2
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 얼린 비전 인코더와 얼린 LLM을 학습 가능한 연결층(Perceiver Resampler + 게이트 교차 어텐션 — 80B 스케일에서는 그 자체로 수십억 파라미터)으로 잇는다 — 그 결과물인 VLM은 LLM의 few-shot 학습 능력을 물려받고, 이미지-텍스트가 뒤섞인 시퀀스를 다룬다.

### 배경

[[clip|CLIP]]은 이미지와 텍스트를 맞출 수 있지만 생성하지 못했고, [[gpt-3|GPT-3]]는 언어로 추론하지만 볼 수 없었다. 거대 멀티모달 모델을 처음부터 학습하는 건 양쪽의 사전학습 투자를 모두 버리는 일이다. 2022년의 공학적 질문: 얼린 LLM이 아는 것을 망가뜨리지 않으면서 어떻게 시각을 *접붙일* 것인가?

### 방법

> [!tip] 핵심 직관
> 사전학습된 거인 둘을 모두 얼려두고, 둘 사이의 "어댑터"만 학습하자. 연결층이 시각 토큰을 LM에 부드럽게(no-op에서 시작해서) 흘려 넣으면, in-context few-shot 학습을 포함한 LM의 능력이 멀티모달로 공짜로 전이된다.

- **얼린 부분**: 대조학습으로 사전학습된 NFNet 비전 인코더 + Chinchilla LM(최대 70B).
- **Perceiver Resampler**: 가변 길이 시각 특징을 고정된 소수의 시각 토큰으로 압축.
- 얼린 LM 블록 사이에 **게이트 달린 cross-attention 층** 삽입; tanh 게이트가 0에서 시작해 학습 시작 시점이 정확히 사전학습 LM과 같고, 시각 정보를 점진적으로 섞는 법을 배운다.
- 웹 규모의 **이미지-텍스트 혼재 시퀀스**(M3W) + 이미지/비디오-텍스트 쌍으로 학습 — 이 혼재 구조가 (이미지, 텍스트) 예시 쌍으로 few-shot 프롬프팅을 가능하게 한다.

### 결과

- 16개 멀티모달 벤치마크(VQA, 캡셔닝, 비디오 QA)에서 few-shot SOTA; 32-shot으로는 **그중 6개에서 파인튜닝된 SOTA까지 추월** — 과제별 학습 없이.
- 성능이 LM 크기·shot 수에 따라 스케일 — GPT-3의 스케일링 행동이 멀티모달에서 재현된다.

### 한계와 비판

- 모델·데이터 비공개; 오픈 재현(OpenFlamingo)은 품질이 못 미친다.
- LM의 약점을 물려받는다: 환각, 대조학습 모델 대비 약한 분류, 프롬프트 설계 민감성.
- 게이트 cross-attention은 LM 층마다 상당한 파라미터를 추가한다 — 이후의 연결자([[blip-2|BLIP-2]]의 Q-Former, [[llava|LLaVA]]의 투영층)가 훨씬 저렴함을 증명했다.

### 영향과 후속 연구

이후 모든 VLM이 다듬게 되는 "얼린 백본 + 연결자" 레시피를 정의했다 — [[blip-2|BLIP-2]], [[llava|LLaVA]], IDEFICS, 그리고 VLA의 인식 스택까지. 혼재 데이터 학습은 멀티모달 in-context 학습의 표준이 됐다.

### 연결

- 이전: [[clip|CLIP]] (시각 축), [[gpt-3|GPT-3]] (few-shot 패러다임)
- 다음: [[blip-2|BLIP-2]] → [[llava|LLaVA]] → RT-2
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Describe the design: two frozen giants joined by gated cross-attention · 얼린 두 거인 + 게이트 cross-attention 연결이라는 설계를 말할 수 있다
- [ ] Explain why interleaved data made multimodal few-shot possible · 혼재 데이터가 멀티모달 few-shot을 가능하게 한 이유를 말할 수 있다
- [ ] Place this paper within the later competition of connector designs (Q-Former → linear) · 이후 연결자 경쟁(Q-Former→선형)에서 이 논문의 위치를 말할 수 있다
