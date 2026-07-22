---
title: "U-Net — Convolutional Networks for Biomedical Image Segmentation"
authors: Olaf Ronneberger, Philipp Fischer, Thomas Brox
affiliation: University of Freiburg
venue: MICCAI
year: 2015
arxiv: https://arxiv.org/abs/1505.04597
pdf: https://arxiv.org/pdf/1505.04597
tags: [paper, computer-vision]
status: to-read
---

**Ronneberger et al., MICCAI 2015** — [arXiv](https://arxiv.org/abs/1505.04597) · [PDF](https://arxiv.org/pdf/1505.04597)

## English

**One-line summary**: An encoder-decoder with skip connections at every scale — the architecture that made dense per-pixel prediction work, and a decade later became the default backbone of diffusion models.

### Context

Classification throws spatial detail away on purpose; segmentation needs a label *per
pixel*. Downsampling encoders capture "what," but "where" is destroyed by pooling. And
biomedical imaging added a constraint: only tens of annotated images.

### Method

> [!tip] Key intuition
> Let the decoder ask the encoder for the details it lost: at each upsampling stage,
> concatenate the encoder's same-resolution feature map. Semantics flow up the U; precise
> localization teleports across it.

- Symmetric contracting/expanding paths with **skip connections** concatenating encoder
  features into the decoder at every resolution.
- Heavy **elastic-deformation augmentation** to survive tiny datasets; weighted loss to
  separate touching object borders.

### Results

- Won the ISBI cell tracking and EM segmentation challenges by large margins with ~30
  training images — end-to-end, no sliding windows.

### Limitations & critique

- Plain convolutions: limited global context (later hybridized with attention);
  memory-hungry at high resolution.
- Designed for 2D single-class biomedical tasks; the community generalized it far beyond
  its evidence.

### Impact & follow-ups

The most re-used architecture diagram in deep learning: medical imaging standard, and —
crucially — the denoiser backbone of [[ddpm|DDPM]]/[[latent-diffusion|Stable Diffusion]]
(noise prediction is dense per-pixel prediction). nnU-Net showed a well-tuned U-Net still
beats most successors.

### Connections

- Previous: [[vgg|VGG]]-style encoders · Next: [[ddpm|DDPM]] (as denoiser), [[detr|DETR]]-era dense prediction
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 모든 스케일에 skip connection을 둔 인코더-디코더 — 픽셀 단위 밀집 예측을 작동하게 만든 구조이며, 10년 뒤 디퓨전 모델의 기본 백본이 됐다.

### 배경

분류는 공간 디테일을 일부러 버리지만, 분할은 *픽셀마다* 라벨이 필요하다. 다운샘플링
인코더는 "무엇"은 잡지만 "어디"는 풀링이 파괴한다. 게다가 의료 영상은 주석 달린 이미지가
수십 장뿐이라는 제약을 더했다.

### 방법

> [!tip] 핵심 직관
> 디코더가 인코더에게 잃어버린 디테일을 물어보게 하라: 업샘플링 단계마다 인코더의 같은
> 해상도 특징맵을 이어붙인다. 의미는 U자를 따라 올라오고, 정밀한 위치는 U자를 가로질러
> 순간이동한다.

- 대칭적인 수축/확장 경로와, 모든 해상도에서 인코더 특징을 디코더에 이어붙이는
  **skip connection**.
- 작은 데이터셋을 버티기 위한 강한 **탄성 변형 증강**; 붙어 있는 물체 경계를 분리하는
  가중 손실.

### 결과

- 학습 이미지 약 30장으로 ISBI 세포 추적·EM 분할 챌린지를 큰 차이로 우승 — end-to-end,
  슬라이딩 윈도 없이.

### 한계와 비판

- 순수 합성곱이라 전역 문맥이 제한적(이후 어텐션과 혼합됨); 고해상도에서 메모리를 많이 쓴다.
- 2D 단일 클래스 의료 과제용 설계 — 커뮤니티가 그 증거 범위를 훨씬 넘어 일반화해서 썼다.

### 영향과 후속 연구

딥러닝에서 가장 많이 재사용된 구조 다이어그램: 의료 영상의 표준이자, 결정적으로
[[ddpm|DDPM]]/[[latent-diffusion|Stable Diffusion]]의 노이즈 제거 백본이다(노이즈 예측이
곧 밀집 픽셀 예측이라서). nnU-Net은 잘 튜닝된 U-Net이 여전히 대부분의 후속을 이긴다는
것을 보였다.

### 연결

- 이전: [[vgg|VGG]]식 인코더 · 다음: [[ddpm|DDPM]] (디노이저로), [[detr|DETR]] 시대의 밀집 예측
- 계보: [[03-deep-learning/lineage|논문 계보도]]
