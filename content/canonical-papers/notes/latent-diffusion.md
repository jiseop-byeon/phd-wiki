---
title: "Latent Diffusion / Stable Diffusion — High-Resolution Image Synthesis with Latent Diffusion Models"
authors: Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer
affiliation: LMU Munich (CompVis), Runway
venue: CVPR
year: 2022
arxiv: https://arxiv.org/abs/2112.10752
pdf: https://arxiv.org/pdf/2112.10752
code: https://github.com/CompVis/latent-diffusion
tags: [paper, generative, diffusion]
status: to-read
---

**Rombach et al., CVPR 2022** — [arXiv](https://arxiv.org/abs/2112.10752) · [PDF](https://arxiv.org/pdf/2112.10752) · [Code](https://github.com/CompVis/latent-diffusion)

## English

**One-line summary**: Run diffusion in a VAE's compressed latent space instead of pixel space — ~50× cheaper generation at high resolution, and (as Stable Diffusion, openly released) the model that democratized image generation.

### Context

[[ddpm|Pixel-space diffusion]] at 512²+ resolutions burned hundreds of GPU-days because
most of those pixels are perceptually redundant detail. Meanwhile [[vae|VAE]]/VQGAN
autoencoders could compress images ~8× per side almost losslessly *perceptually*. The
obvious-in-hindsight move: separate compression from generation.

### Method

> [!tip] Key intuition
> Let each stage do what it's good at: a perceptual autoencoder removes imperceptible
> detail once; diffusion then models only the *semantic* structure in a space 48× smaller.
> Same math as DDPM — just a better coordinate system.

- Stage 1: KL- or VQ-regularized autoencoder (with perceptual + patch-GAN losses) maps
  images to latents (e.g., 512²×3 → 64²×4).
- Stage 2: [[u-net|U-Net]] diffusion in latent space; **cross-attention** layers inject
  conditioning (text via CLIP/T5 encoders, layouts, depth) — the general conditioning
  interface.
- Stable Diffusion = this recipe trained on LAION-5B subsets and *released openly* with weights.

### Results

- SOTA-competitive FID on class-conditional and text-to-image benchmarks at a fraction of
  compute; inpainting, super-resolution, layout-to-image from one framework.
- The open release triggered the largest creative-tool ecosystem in generative AI
  (fine-tunes, [[lora|LoRAs]], [[controlnet|ControlNet]]).

### Limitations & critique

- The autoencoder bounds achievable detail (text, faces, fine textures) — later versions
  retrained decoders and enlarged latents.
- Two-stage training complexity; LAION data brought copyright/bias controversies that
  shaped the open-model debate.

### Impact & follow-ups

Made "diffusion in latent space" the default for images, video, and audio; cross-attention
conditioning became the standard interface. In robotics, latent diffusion thinking recurs
wherever action/video generation must be cheap ([[cosmos|Cosmos]] tokenizers,
latent world models).

### Connections

- Previous: [[ddpm|DDPM]], [[vae|VAE]]/VQGAN, [[u-net|U-Net]] · With: [[classifier-free-guidance|CFG]], [[controlnet|ControlNet]] · Next: [[dit|DiT]], [[sora|Sora]]
- Lineage: [[10-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 디퓨전을 픽셀 공간 대신 VAE의 압축된 잠재 공간에서 돌린다 — 고해상도 생성이 약 50배 저렴해졌고, (Stable Diffusion으로 공개되어) 이미지 생성을 대중화한 그 모델이 됐다.

### 배경

512² 이상에서의 [[ddpm|픽셀 공간 디퓨전]]은 수백 GPU-일을 태웠다 — 그 픽셀 대부분이
지각적으로 중복인 디테일이기 때문이다. 한편 [[vae|VAE]]/VQGAN 오토인코더는 이미지를 변당
약 8배로 *지각적으로는* 거의 무손실 압축할 수 있었다. 돌아보면 자명한 수: 압축과 생성을
분리하라.

### 방법

> [!tip] 핵심 직관
> 각 단계가 잘하는 일을 하게 하라: 지각적 오토인코더가 안 보이는 디테일을 한 번 제거하고,
> 디퓨전은 48배 작은 공간에서 *의미* 구조만 모델링한다. 수학은 DDPM 그대로 — 좌표계만
> 더 좋아졌다.

- 1단계: KL 또는 VQ 정규화 오토인코더(지각 손실 + 패치 GAN 손실)가 이미지를 잠재로 사상
  (예: 512²×3 → 64²×4).
- 2단계: 잠재 공간에서 [[u-net|U-Net]] 디퓨전; **cross-attention** 층이 조건을
  주입(CLIP/T5 인코더의 텍스트, 레이아웃, 깊이) — 범용 조건화 인터페이스.
- Stable Diffusion = 이 레시피를 LAION-5B 부분집합으로 학습해 가중치까지 *공개*한 것.

### 결과

- 훨씬 적은 연산으로 클래스 조건부·텍스트-이미지 벤치마크에서 SOTA급 FID; 인페인팅,
  초해상도, 레이아웃-이미지가 한 프레임워크에서.
- 공개 릴리스가 생성 AI 최대의 창작 도구 생태계를 촉발(파인튜닝, [[lora|LoRA]],
  [[controlnet|ControlNet]]).

### 한계와 비판

- 오토인코더가 도달 가능한 디테일의 상한(글자, 얼굴, 미세 질감) — 후속 버전들이 디코더
  재학습과 잠재 확대로 대응.
- 2단계 학습의 복잡성; LAION 데이터는 저작권/편향 논쟁을 불러 오픈 모델 논의를 형성했다.

### 영향과 후속 연구

"잠재 공간 디퓨전"을 이미지·비디오·오디오의 기본값으로 만들었다; cross-attention 조건화가
표준 인터페이스가 됐다. 로보틱스에서도 행동/비디오 생성이 저렴해야 하는 곳마다 잠재
디퓨전의 사고가 재등장한다([[cosmos|Cosmos]] 토크나이저, 잠재 월드모델).

### 연결

- 이전: [[ddpm|DDPM]], [[vae|VAE]]/VQGAN, [[u-net|U-Net]] · 함께: [[classifier-free-guidance|CFG]], [[controlnet|ControlNet]] · 다음: [[dit|DiT]], [[sora|Sora]]
- 계보: [[10-deep-learning/lineage|논문 계보도]]
