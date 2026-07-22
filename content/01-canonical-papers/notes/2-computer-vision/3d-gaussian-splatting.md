---
title: "3D Gaussian Splatting for Real-Time Radiance Field Rendering"
authors: Bernhard Kerbl, Georgios Kopanas, Thomas Leimkühler, George Drettakis
affiliation: Inria, Université Côte d'Azur, MPI Informatik
venue: SIGGRAPH
year: 2023
arxiv: https://arxiv.org/abs/2308.04079
pdf: https://arxiv.org/pdf/2308.04079
code: https://github.com/graphdeco-inria/gaussian-splatting
tags: [paper, computer-vision, 3d]
status: to-read
---

**Kerbl et al., SIGGRAPH 2023** — [arXiv](https://arxiv.org/abs/2308.04079) · [PDF](https://arxiv.org/pdf/2308.04079) · [Code](https://github.com/graphdeco-inria/gaussian-splatting)

## English

**One-line summary**: Represent the scene as millions of optimizable 3D Gaussians and *rasterize* them — NeRF-quality novel views at 100+ fps, trained in minutes, returning 3D reconstruction to an explicit, editable representation.

### Context

[[nerf|NeRF]] won on quality but paid in ray-marching: millions of MLP queries per frame.
Three years of acceleration research (Instant-NGP et al.) still fought the implicit
representation itself. The heretical alternative: go back to explicit primitives — but make
them soft, differentiable, and optimizable.

### Method

> [!tip] Key intuition
> A cloud of anisotropic 3D Gaussians is both a *scene representation* and a *rendering
> primitive*: project each Gaussian to screen, sort, and alpha-blend — a rasterization
> pipeline GPUs already excel at, with gradients flowing to every Gaussian's parameters.

- Each Gaussian: position, anisotropic covariance (scale+rotation), opacity, spherical-
  harmonics color — initialized from the SfM point cloud, optimized by rendering loss.
- **Adaptive density control**: clone/split Gaussians where detail is missing, prune
  transparent ones.
- **Tile-based differentiable rasterizer**: visibility-sorted alpha blending — the
  engineering core enabling real-time rates.

### Results

- Matches or beats Mip-NeRF360 quality with **~30–60 min training and ≥100 fps 1080p
  rendering** (vs days/seconds-per-frame for NeRF-class methods).

### Limitations & critique

- Memory-heavy (millions of Gaussians, hundreds of MB); artifacts in sparsely observed
  regions; still needs SfM poses; static scenes in v1.
- Explicitness is also a gift: editing, physics coupling, and semantic attachment are far
  easier than with an MLP — driving its adoption over NeRF.

### Impact & follow-ups

Displaced NeRF as the default radiance-field method almost overnight; spawned dynamic
(4D), SLAM-integrated, and semantic variants. For construction: fast photorealistic site
digital twins, and — via [[vggt|VGGT]]-style feed-forward geometry — a path toward
real-time as-built capture.

### Connections

- Previous: [[nerf|NeRF]] (the implicit rival) · Next: [[vggt|VGGT]], GS-SLAM lines
- Domain: [[05-construction-robotics/index|site digital twins]] · Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 장면을 최적화 가능한 수백만 개의 3D 가우시안으로 표현하고 *래스터라이즈* — NeRF급 새 시점 합성을 100+ fps로, 학습은 수십 분에, 그리고 3D 재구성을 명시적이고 편집 가능한 표현으로 되돌렸다.

### 배경

[[nerf|NeRF]]는 품질에서 이겼지만 레이 마칭의 값을 치렀다: 프레임당 수백만 번의 MLP 질의.
3년의 가속 연구(Instant-NGP 등)도 암시적 표현 자체와 싸우고 있었다. 이단적 대안: 명시적
프리미티브로 돌아가되 — 부드럽고, 미분 가능하고, 최적화 가능하게 만들자.

### 방법

> [!tip] 핵심 직관
> 이방성 3D 가우시안 구름은 *장면 표현*이자 동시에 *렌더링 프리미티브*다: 각 가우시안을
> 화면에 투영하고, 정렬하고, 알파 블렌딩한다 — GPU가 이미 잘하는 래스터라이제이션
> 파이프라인이고, 그래디언트가 모든 가우시안의 파라미터로 흐른다.

- 각 가우시안: 위치, 이방성 공분산(스케일+회전), 불투명도, 구면 조화 색 — SfM 포인트
  클라우드로 초기화, 렌더링 손실로 최적화.
- **적응적 밀도 제어**: 디테일이 부족한 곳은 가우시안을 복제/분할, 투명한 것은 제거.
- **타일 기반 미분 가능 래스터라이저**: 가시성 정렬 알파 블렌딩 — 실시간을 가능하게 한
  공학적 핵심.

### 결과

- Mip-NeRF360급 품질을 **학습 약 30~60분, 1080p 렌더링 100 fps 이상**으로
  (NeRF류의 수 일 학습/프레임당 수 초와 대비).

### 한계와 비판

- 메모리를 많이 쓴다(수백만 가우시안, 수백 MB); 관측이 적은 영역의 아티팩트; 여전히 SfM
  자세 필요; v1은 정적 장면.
- 명시성은 선물이기도 하다: 편집, 물리 결합, 의미 부착이 MLP보다 훨씬 쉽다 — NeRF 대신
  채택되는 원동력.

### 영향과 후속 연구

거의 하룻밤 사이에 radiance field의 기본 기법 자리에서 NeRF를 밀어냈다; 동적(4D),
SLAM 통합, 의미론 변형들을 낳았다. 건설에서는: 빠른 사진 수준 현장 디지털 트윈, 그리고
[[vggt|VGGT]]식 feed-forward 기하를 거쳐 실시간 준공(as-built) 캡처로 가는 길.

### 연결

- 이전: [[nerf|NeRF]] (암시적 라이벌) · 다음: [[vggt|VGGT]], GS-SLAM 계열
- 도메인: [[05-construction-robotics/index|현장 디지털 트윈]] · 계보: [[03-deep-learning/lineage|논문 계보도]]
