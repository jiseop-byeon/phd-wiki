---
title: "PaliGemma — A Versatile 3B VLM for Transfer (2024)"
authors: Lucas Beyer, Andreas Steiner, et al.
affiliation: Google DeepMind
venue: arXiv
year: 2024
arxiv: https://arxiv.org/abs/2407.07726
pdf: https://arxiv.org/pdf/2407.07726
tags: [paper, vlm]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Beyer, Steiner et al. (Google), 2024** — [arXiv](https://arxiv.org/abs/2407.07726) · [PDF](https://arxiv.org/pdf/2407.07726)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]] for the vision encoder lineage and [[02-foundations/neural-network-basics|0.7 §4]] for the training-budget arithmetic (batch, epoch, steps) — this paper is a *recipe* paper, so its contribution lives in those numbers rather than in a new equation.
> 비전 인코더 계보는 [[01-canonical-papers/notes/3-vlm/clip|CLIP]], 학습 예산 산수(배치·에포크·스텝)는 [[02-foundations/neural-network-basics|0.7 §4]] — 이 논문은 *레시피* 논문이라 새 수식이 아니라 그 숫자들에 기여가 담겨 있다.

## English

**One-line summary**: A deliberately small (~3B) open VLM — SigLIP vision encoder + Gemma-2B language model — designed as a *transfer base*: pretrain broadly, then fine-tune to each downstream task.

**Why it is in this wiki**: two reasons. It is the representative "small open VLM" design
point (the counterweight to [[01-canonical-papers/notes/3-vlm/qwen-vl|Qwen-VL]]-class scaling),
and it is **the backbone of [[01-canonical-papers/notes/4-vla/pi0|π0]]** — reading π0's
architecture requires knowing what PaliGemma provides (a compact, transfer-friendly
vision-language trunk that a robotics action expert can attach to).

**How it works (literacy level)**: SigLIP-So400m encodes the image into tokens; Gemma-2B
consumes image tokens + text prompt with **prefix-LM attention** (full bidirectional
attention over the image+prompt prefix, causal only over the generated answer) — so the
"question" can see the whole image, unlike a purely causal LM. Pretraining runs in stages
of increasing image resolution (224→448→896) on broad multimodal mixtures; the released
checkpoint is deliberately *not* instruction-tuned — you fine-tune it per task with a
provided recipe.

**Limitations**: no zero-shot chat ability out of the box (by design); performance is
claimed *after* per-task fine-tuning, so comparisons against instruction-tuned VLMs'
zero-shot numbers are apples-to-oranges in both directions.

**Reading the claim**: "versatile" means *transfers well to many tasks after fine-tuning*
— it is not claiming zero-shot parity with frontier VLMs; the 3B size is the point, not a
limitation to apologize for.

## 한국어

**한 줄 요약**: 의도적으로 작은(~3B) 오픈 VLM — SigLIP 비전 인코더 + Gemma-2B 언어모델 — *전이 베이스*로 설계됐다: 넓게 사전학습하고, 다운스트림 과제마다 파인튜닝한다.

**이 위키에 있는 이유**: 둘이다. "작은 오픈 VLM" 설계 지점의 대표
([[01-canonical-papers/notes/3-vlm/qwen-vl|Qwen-VL]]류 스케일링의 대척점)이고,
**[[01-canonical-papers/notes/4-vla/pi0|π0]]의 백본**이다 — π0의 구조를 읽으려면
PaliGemma가 무엇을 제공하는지(로봇 행동 전문가를 붙일 수 있는 작고 전이 친화적인
시각-언어 몸통)를 알아야 한다.

**작동 방식 (문해력 수준)**: SigLIP-So400m이 이미지를 토큰으로 인코딩하고, Gemma-2B가
이미지 토큰 + 텍스트 프롬프트를 **prefix-LM 어텐션**으로 소비한다(이미지+프롬프트
접두부에는 완전 양방향 어텐션, 생성되는 답변에만 인과 어텐션) — 순수 인과 LM과 달리
"질문"이 이미지 전체를 볼 수 있다. 사전학습은 해상도를 키워 가는 단계(224→448→896)로
넓은 멀티모달 혼합에서 진행되며, 공개 체크포인트는 의도적으로 지시 튜닝을 *하지 않은*
상태다 — 제공된 레시피로 과제마다 파인튜닝한다.

**한계**: 즉시 쓰는 zero-shot 대화 능력은 없다(설계상); 성능 주장은 과제별 파인튜닝
*후*의 것이므로, 지시 튜닝된 VLM의 zero-shot 수치와의 비교는 양방향 모두
사과-오렌지 비교다.

**주장 읽는 법**: "versatile"은 *파인튜닝 후 여러 과제로 잘 전이된다*는 뜻이다 —
프런티어 VLM과의 zero-shot 동급을 주장하는 것이 아니며, 3B라는 크기는 변명할 한계가
아니라 설계의 요점이다.

### 연결

- 이전: [[01-canonical-papers/notes/3-vlm/clip|CLIP]] (SigLIP은 그 후속), [[01-canonical-papers/notes/3-vlm/llava|LLaVA]] · 다음: [[01-canonical-papers/notes/4-vla/pi0|π0]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading (○)

- [ ] Name the two components (SigLIP + Gemma-2B) and the "transfer base" design philosophy · 구성 두 조각(SigLIP + Gemma-2B)과 "전이 베이스" 설계 철학을 말할 수 있다
- [ ] Explain why π0 chose this 3B model as its backbone rather than a frontier VLM · π0가 왜 프런티어급 VLM이 아니라 이 3B 모델을 백본으로 골랐는지 설명할 수 있다
- [ ] Distinguish "versatile" as a claim about fine-tuning transfer breadth from a claim about zero-shot performance · "versatile"이 zero-shot 성능이 아니라 파인튜닝 전이 범위에 대한 주장임을 구분할 수 있다
