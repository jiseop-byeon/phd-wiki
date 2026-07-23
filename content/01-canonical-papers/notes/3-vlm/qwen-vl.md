---
title: "Qwen-VL Series — Qwen-VL, Qwen2-VL, Qwen2.5-VL"
authors: Jinze Bai, Shuai Bai, et al. (Qwen Team)
affiliation: Alibaba Group
venue: arXiv
year: 2023
arxiv: https://arxiv.org/abs/2308.12966  # Qwen-VL (2023); Qwen2-VL 2409.12191; Qwen2.5-VL 2502.13923
pdf: https://arxiv.org/pdf/2308.12966
code: https://github.com/QwenLM/Qwen2.5-VL
tags: [paper, vlm]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Qwen Team (Alibaba), 2023–2025** — [Qwen-VL arXiv](https://arxiv.org/abs/2308.12966) · [Qwen2-VL arXiv](https://arxiv.org/abs/2409.12191) · [Qwen2.5-VL arXiv/PDF](https://arxiv.org/pdf/2502.13923) · [Code](https://github.com/QwenLM/Qwen2.5-VL)

## English

**One-line summary**: The representative *open-weights production* VLM line — three iterations that show what turns the [[llava|LLaVA]]-era recipe into a deployable model family: native resolution, grounding, video, and document intelligence.

### Context

After [[llava|LLaVA]] settled the architecture debate, the frontier moved from "how to
connect" to "how to make it *production-grade*": arbitrary resolutions, OCR/documents,
grounding boxes, long video, multilinguality — with open weights. Qwen-VL is the line this
wiki tracks as the exemplar (peers: InternVL, PaliGemma).

### Method (what each generation added)

> [!tip] Key intuition
> No single big idea — compounding engineering: better visual tokenization, more
> capability-targeted data, longer context. The lesson of this line is that VLM progress
> after 2023 is mostly a *data and interface* story, not an architecture story.

- **Qwen-VL (2023)**: ViT encoder + cross-attention resampler into Qwen-7B; grounding
  (boxes as text) and OCR built into pretraining — an early open VLM that could point.
- **Qwen2-VL (2024)**: **naive dynamic resolution** (images become however many tokens
  they need — no fixed square resize) + **M-RoPE** (multimodal rotary positions across
  text/image/video axes); handles 20min+ video; 2B/7B/72B open weights.
- **Qwen2.5-VL (2025)**: native-resolution ViT trained with window attention, absolute-time
  video alignment for hour-long video with second-level event localization, document
  parsing (tables, formulas), and **agentic UI operation** (computer/phone use).

### Results

- Qwen2.5-VL-72B matches or beats closed frontier models (GPT-4o-class) on document/OCR,
  grounding, and video benchmarks at publication; the small variants (3B/7B) became default
  open VLM backbones for downstream research.

### Limitations & critique

- Iteration-driven reports: heavy benchmark tables, limited ablation of *why* each change
  matters; data mixtures largely undisclosed (open weights ≠ open data).
- Same inherited VLM weaknesses: hallucination, spatial reasoning limits ([[clip|CLIP]]-line
  inheritance) — relevant when a VLA borrows the backbone.

### Impact & follow-ups

The de-facto open VLM backbone family of 2024–25: robotics stacks and VLA research
increasingly initialize from Qwen2/2.5-VL checkpoints (as [[openvla|OpenVLA]] did from
Prismatic/Llama-2, and [[pi0|π0]] from PaliGemma). Tracking this line ≈ tracking what
production VLMs can do.

### Connections

- Previous: [[llava|LLaVA]] (the recipe it industrializes), [[clip|CLIP]]/[[vit|ViT]]
- Next: VLA backbones ([[openvla|OpenVLA]]-style fine-tunes)
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 대표적인 *오픈 가중치 프로덕션* VLM 계열 — [[llava|LLaVA]] 시대의 레시피를 배포 가능한 모델 패밀리로 만드는 데 무엇이 필요한지(네이티브 해상도, 그라운딩, 비디오, 문서 지능)를 세 번의 반복으로 보여준다.

### 배경

[[llava|LLaVA]]가 구조 논쟁을 정리한 뒤, 최전선은 "어떻게 연결하나"에서 "어떻게
*프로덕션급*으로 만드나"로 이동했다: 임의 해상도, OCR/문서, 그라운딩 박스, 긴 비디오,
다국어 — 그것도 오픈 가중치로. 이 위키는 그 대표로 Qwen-VL 계열을 추적한다
(동급: InternVL, PaliGemma).

### 방법 (세대별 추가점)

> [!tip] 핵심 직관
> 하나의 큰 아이디어가 아니라 누적되는 공학이다: 더 나은 시각 토큰화, 능력별 표적 데이터,
> 더 긴 문맥. 이 계열의 교훈은 2023년 이후 VLM의 진보가 구조 이야기가 아니라 주로
> *데이터와 인터페이스* 이야기라는 것.

- **Qwen-VL (2023)**: ViT 인코더 + cross-attention 리샘플러를 Qwen-7B에; 그라운딩(박스를
  텍스트로)과 OCR을 사전학습에 내장 — 가리킬 줄 아는 이른 오픈 VLM.
- **Qwen2-VL (2024)**: **naive dynamic resolution**(이미지가 필요한 만큼의 토큰이 된다 —
  고정 정사각 리사이즈 없음) + **M-RoPE**(텍스트/이미지/비디오 축의 멀티모달 회전 위치);
  20분+ 비디오 처리; 2B/7B/72B 오픈 가중치.
- **Qwen2.5-VL (2025)**: window attention으로 학습한 네이티브 해상도 ViT, 초 단위 이벤트
  위치 추정이 되는 절대 시간 비디오 정렬(시간 단위 비디오), 문서 파싱(표, 수식), 그리고
  **에이전트형 UI 조작**(컴퓨터/폰 사용).

### 결과

- Qwen2.5-VL-72B는 발표 시점 문서/OCR, 그라운딩, 비디오 벤치마크에서 폐쇄형 프런티어
  (GPT-4o급)와 대등하거나 우세; 소형(3B/7B)은 다운스트림 연구의 기본 오픈 VLM 백본이 됐다.

### 한계와 비판

- 반복 개발형 보고서: 벤치마크 표는 많지만 각 변화가 *왜* 중요한지의 절제 실험은 제한적;
  데이터 혼합은 대부분 비공개 (오픈 가중치 ≠ 오픈 데이터).
- VLM의 공통 약점 상속: 환각, 공간 추론 한계 ([[clip|CLIP]] 계열의 유산) — VLA가 이 백본을
  빌릴 때 그대로 따라온다.

### 영향과 후속 연구

2024~25년의 사실상 표준 오픈 VLM 백본 패밀리: 로보틱스 스택과 VLA 연구가 점점
Qwen2/2.5-VL 체크포인트에서 출발한다 ([[openvla|OpenVLA]]가 Prismatic/Llama-2에서,
[[pi0|π0]]가 PaliGemma에서 출발했듯이). 이 계열을 추적하는 것 ≈ 프로덕션 VLM이 무엇을 할
수 있는지를 추적하는 것.

### 연결

- 이전: [[llava|LLaVA]] (산업화된 레시피), [[clip|CLIP]]/[[vit|ViT]]
- 다음: VLA 백본 ([[openvla|OpenVLA]]식 파인튜닝)
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 세 세대 각각이 추가한 것을 하나씩 말할 수 있다
- [ ] 동적 해상도가 고정 리사이즈 대비 푸는 문제를 말할 수 있다
- [ ] 2023년 이후 VLM 진보가 구조가 아니라 데이터·인터페이스 이야기라는 주장을 설명할 수 있다
- [ ] 오픈 가중치 ≠ 오픈 데이터의 함의를 말할 수 있다
