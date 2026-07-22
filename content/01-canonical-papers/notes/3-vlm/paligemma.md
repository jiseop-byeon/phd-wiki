---
title: "PaliGemma — A Versatile 3B VLM for Transfer (2024)"
authors: Lucas Beyer, Andreas Steiner, et al.
affiliation: Google DeepMind
venue: arXiv
year: 2024
arxiv: https://arxiv.org/abs/2407.07726
pdf: https://arxiv.org/pdf/2407.07726
tags: [paper, vlm]
status: to-read
---

**Beyer, Steiner et al. (Google), 2024** — [arXiv](https://arxiv.org/abs/2407.07726) · [PDF](https://arxiv.org/pdf/2407.07726)

## English

**One-line summary**: A deliberately small (~3B) open VLM — SigLIP vision encoder + Gemma-2B language model — designed as a *transfer base*: pretrain broadly, then fine-tune to each downstream task.

**Why it is in this wiki**: two reasons. It is the representative "small open VLM" design
point (the counterweight to [[01-canonical-papers/notes/3-vlm/qwen-vl|Qwen-VL]]-class scaling),
and it is **the backbone of [[01-canonical-papers/notes/4-vla/pi0|π0]]** — reading π0's
architecture requires knowing what PaliGemma provides (a compact, transfer-friendly
vision-language trunk that a robotics action expert can attach to).

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

**주장 읽는 법**: "versatile"은 *파인튜닝 후 여러 과제로 잘 전이된다*는 뜻이다 —
프런티어 VLM과의 zero-shot 동급을 주장하는 것이 아니며, 3B라는 크기는 변명할 한계가
아니라 설계의 요점이다.

### 연결

- 이전: [[01-canonical-papers/notes/3-vlm/clip|CLIP]] (SigLIP은 그 후속), [[01-canonical-papers/notes/3-vlm/llava|LLaVA]] · 다음: [[01-canonical-papers/notes/4-vla/pi0|π0]]
