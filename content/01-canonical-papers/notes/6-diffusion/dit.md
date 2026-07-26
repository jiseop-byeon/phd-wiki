---
title: "DiT — Scalable Diffusion Models with Transformers"
authors: William Peebles, Saining Xie
affiliation: UC Berkeley, New York University
venue: ICCV
year: 2023
arxiv: https://arxiv.org/abs/2212.09748
pdf: https://arxiv.org/pdf/2212.09748
code: https://github.com/facebookresearch/DiT
tags: [paper, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Peebles & Xie, ICCV 2023** — [arXiv](https://arxiv.org/abs/2212.09748) · [PDF](https://arxiv.org/pdf/2212.09748) · [Code](https://github.com/facebookresearch/DiT)

## English

**One-line summary**: Replace the diffusion U-Net with a plain Transformer over latent patches — quality scales cleanly with compute (Gflops), unifying diffusion with the scaling playbook and becoming the backbone of Sora and modern robot action heads.

### Context

Diffusion's [[u-net|U-Net]] backbone was inherited, not chosen: a convolutional inductive
bias in a field where [[vit|ViT]] had shown transformers + scale beat built-in priors.
If diffusion is to ride [[scaling-laws|scaling laws]], its backbone needed to be the
architecture that scales best.

### Method

> [!tip] Key intuition
> Treat denoising as sequence modeling: patchify the ([[latent-diffusion|latent]]) image
> into tokens, run a standard ViT, and inject timestep/class via **adaLN-Zero** —
> normalization layers whose scales/shifts are predicted from the conditioning and
> initialized to zero (the residual-friendly no-op start again).

- ViT over latent patches (patch size 2/4/8); conditioning via adaLN-Zero beats
  cross-attention and in-context tokens in ablations.
- Systematic scaling study: model size × patch count → FID tracks total **Gflops**
  almost monotonically.

### Results

- DiT-XL/2: FID **2.27** on class-conditional ImageNet 256² — beating U-Net diffusion
  (ADM, LDM) at better compute efficiency; the correlation "more Gflops → better FID"
  held with no signs of saturation.

### Limitations & critique

- Class-conditional ImageNet only in the paper — text-to-image and video came from
  followers; attention cost grows quadratically with resolution (patching mitigates).
- Removed inductive bias means more data/compute needed at small scale.

### Impact & follow-ups

The default backbone of current *diffusion-family* generators: [[sora|Sora]] (spacetime DiT),
Stable Diffusion 3 / Flux (MM-DiT), and — for this wiki — robot action experts:
[[pi0|π0]] and [[gr00t-n1|GR00T]]'s flow/diffusion modules are DiT-style transformers
denoising action sequences.

### Connections

- Previous: [[vit|ViT]], [[u-net|U-Net]] (displaced), [[latent-diffusion|LDM]] · Next: [[sora|Sora]], [[pi0|π0]]/[[gr00t-n1|GR00T]] action heads
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 디퓨전의 U-Net을 잠재 패치 위의 순정 Transformer로 교체 — 품질이 연산량(Gflops)에 따라 깔끔하게 스케일하며, 디퓨전을 스케일링 플레이북과 통합하고 Sora와 현대 로봇 행동 헤드의 백본이 됐다.

### 배경

디퓨전의 [[u-net|U-Net]] 백본은 선택이 아니라 유산이었다: [[vit|ViT]]가 "트랜스포머 +
규모가 내장 사전 지식을 이긴다"는 것을 보여준 분야에서의 합성곱 귀납 편향.
디퓨전이 [[scaling-laws|스케일링 법칙]]에 올라타려면, 백본부터 가장 잘 스케일하는 구조여야
했다.

### 방법

> [!tip] 핵심 직관
> 노이즈 제거를 시퀀스 모델링으로 취급하라: ([[latent-diffusion|잠재]]) 이미지를 패치
> 토큰으로 자르고, 표준 ViT를 돌리고, 타임스텝/클래스는 **adaLN-Zero**로 주입한다 —
> 조건에서 스케일/이동을 예측하되 0으로 초기화되는 정규화 층(또 그 residual 친화적 no-op
> 출발점이다).

- 잠재 패치 위의 ViT(패치 크기 2/4/8); 절제 실험에서 adaLN-Zero 조건화가
  cross-attention과 in-context 토큰을 이긴다.
- 체계적 스케일링 연구: 모델 크기 × 패치 수 → FID가 총 **Gflops**를 거의 단조로 따라간다.

### 결과

- DiT-XL/2: 클래스 조건부 ImageNet 256²에서 FID **2.27** — U-Net 디퓨전(ADM, LDM)을 더
  나은 연산 효율로 추월; "Gflops가 늘면 FID가 좋아진다"는 상관이 포화 기미 없이 유지됐다.

### 한계와 비판

- 논문은 클래스 조건부 ImageNet뿐 — 텍스트-이미지와 비디오는 후속들의 몫; 어텐션 비용이
  해상도에 제곱으로 는다(패칭이 완화).
- 귀납 편향을 없앤 대가로 작은 규모에서는 데이터/연산이 더 필요하다.

### 영향과 후속 연구

현시대 *디퓨전 계열* 생성기의 기본 백본: [[sora|Sora]](시공간 DiT), Stable Diffusion 3 /
Flux(MM-DiT), 그리고 이 위키에 중요한 — 로봇 행동 전문가: [[pi0|π0]]와
[[gr00t-n1|GR00T]]의 flow/디퓨전 모듈이 행동 시퀀스의 노이즈를 제거하는 DiT식
트랜스포머다.

### 연결

- 이전: [[vit|ViT]], [[u-net|U-Net]] (밀려남), [[latent-diffusion|LDM]] · 다음: [[sora|Sora]], [[pi0|π0]]/[[gr00t-n1|GR00T]] 행동 헤드
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Give the argument for replacing the U-Net (unifying the scaling playbook) · U-Net 대체의 논거(스케일링 플레이북 통합)를 말할 수 있다
- [ ] State the role of adaLN-Zero and its no-op initialization pattern · adaLN-Zero의 역할과 no-op 초기화 패턴을 말할 수 있다
- [ ] Say what the Gflops–FID correlation demonstrates · Gflops-FID 상관이 보여주는 것을 말할 수 있다
- [ ] Explain why the π0 and GR00T action heads are DiTs · π0·GR00T 행동 헤드가 DiT인 이유를 말할 수 있다
