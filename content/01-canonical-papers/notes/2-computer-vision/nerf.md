---
title: "NeRF — Representing Scenes as Neural Radiance Fields for View Synthesis"
authors: Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, Ren Ng
affiliation: UC Berkeley, Google Research, UC San Diego
venue: ECCV
year: 2020
arxiv: https://arxiv.org/abs/2003.08934
pdf: https://arxiv.org/pdf/2003.08934
project: https://www.matthewtancik.com/nerf
tags: [paper, computer-vision, 3d]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Mildenhall et al., ECCV 2020** — [arXiv](https://arxiv.org/abs/2003.08934) · [PDF](https://arxiv.org/pdf/2003.08934) · [Official](https://www.matthewtancik.com/nerf)

> [!note] 수학 준비물 · Math on-ramp
> Read the volume-rendering integral as "a weighted average along a ray": colour $c$ averaged with density-derived weights, i.e. an $E[c]$ ([[02-foundations/probability|3. Probability §2]]'s expectation sense). In code it is a weighted sum over finitely many samples. The positional-encoding sinusoids are [[02-foundations/engineering-math|0.5 §7]]'s Fourier intuition.
> 볼륨 렌더링 적분은 "광선 위의 가중 평균"으로 읽으면 된다: 색 $c$를 밀도 기반 가중치로 평균하는 $E[c]$ 꼴([[02-foundations/probability|확률 §2]]의 기댓값 감각). 구현에서는 광선을 유한 샘플로 이산화한 가중합이다. 위치 인코딩의 사인파는 [[02-foundations/engineering-math|0.5 §7]]의 푸리에 감각.

## English

**One-line summary**: Represent a scene as an MLP mapping (position, view direction) → (color, density), trained only by re-rendering the input photos — photorealistic novel views from an implicit neural 3D representation.

### Context

3D reconstruction meant explicit structures — meshes, voxels, point clouds — each trading
resolution against memory, and none differentiable end-to-end from photos alone. The
implicit-function idea was in the air (occupancy networks); NeRF made it *photorealistic*.

### Method

> [!tip] Key intuition
> Don't store the scene — store a *function* of the scene. A tiny MLP answers "what is at
> point (x,y,z) seen from direction d?" Volume rendering along camera rays is
> differentiable, so multi-view photos supervise the function directly.

- MLP: $(x, y, z, \theta, \phi) \to (\text{RGB}, \sigma)$; **positional encoding**
  (Fourier features) lets the MLP express high frequencies. It cannot otherwise because of
  **spectral bias**: a coordinate MLP fits low frequencies far faster than high ones, so on
  raw $(x,y,z)$ inputs the fitted radiance field comes out over-smoothed. Lifting the input
  into a Fourier basis makes the high-frequency directions as easy to fit as the low ones.
- **Differentiable volume rendering**: integrate color×density along each ray; loss = pixel
  MSE against input photos. Hierarchical coarse-to-fine sampling.
- View-direction input captures specular/reflective effects.

### Results

- Novel-view synthesis of unprecedented quality on real scenes from ~20–100 posed photos;
  an entire scene compressed into ~5MB of MLP weights.

### Limitations & critique

- Slow: hours-to-days training, seconds per frame rendering (v1); per-scene optimization,
  no generalization; requires known camera poses (COLMAP); static scenes only.
- The speed problem defined follow-up research — and its explicit-representation rival
  [[3d-gaussian-splatting|3DGS]] ultimately won the real-time race.

### Impact & follow-ups

Launched neural rendering as a field (Instant-NGP's hash grids, Mip-NeRF, Zip-NeRF,
dynamic/large-scale variants) and made *differentiable rendering* a standard tool.
In robotics/construction: photorealistic digital twins of sites and simulation assets for
data generation ([[cosmos|world-model data engines]]).

### Connections

- Next: [[3d-gaussian-splatting|3D Gaussian Splatting]] (the explicit counter), [[vggt|VGGT]] (feed-forward 3D)
- Domain: [[05-construction-robotics/index|site digital twins]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 장면을 (위치, 시선 방향) → (색, 밀도)를 내는 MLP로 표현하고 입력 사진의 재렌더링만으로 학습 — 암시적 신경 3D 표현에서 사진 수준의 새 시점 합성을 얻었다.

### 배경

3D 재구성은 명시적 구조 — 메시, 복셀, 포인트 클라우드 — 를 뜻했고, 각각 해상도와 메모리를
맞바꾸며 사진만으로 end-to-end 미분 가능한 것은 없었다. 암시적 함수 아이디어는 이미
떠돌고 있었지만(occupancy network), NeRF가 그것을 *사진 수준*으로 만들었다.

### 방법

> [!tip] 핵심 직관
> 장면을 저장하지 말고 장면의 *함수*를 저장하라. 작은 MLP가 "점 (x,y,z)를 방향 d에서 보면
> 무엇이 있는가?"에 답한다. 카메라 광선을 따라가는 볼륨 렌더링은 미분 가능하므로, 다시점
> 사진이 그 함수를 직접 감독한다.

- MLP: $(x, y, z, \theta, \phi) \to (\text{RGB}, \sigma)$; **위치 인코딩**(푸리에 특징)이
  MLP가 고주파를 표현하게 한다. 그것 없이는 못 하는 이유가 **스펙트럼 편향**이다: 좌표 MLP는 저주파를 고주파보다 훨씬 빨리 맞추므로, 날것의 $(x,y,z)$ 입력으로는 복원된 radiance field가 과하게 매끄럽게 나온다. 입력을 푸리에 기저로 들어올리면 고주파 방향도 저주파만큼 맞추기 쉬워진다.
- **미분 가능한 볼륨 렌더링**: 광선을 따라 색×밀도를 적분; 손실 = 입력 사진과의 픽셀 MSE.
  거친→세밀 계층 샘플링.
- 시선 방향 입력이 반사/광택 효과를 담는다.

### 결과

- 자세를 아는 사진 20~100장으로 실제 장면의 전례 없는 품질의 새 시점 합성;
  장면 전체가 약 5MB의 MLP 가중치로 압축된다.

### 한계와 비판

- 느리다: 학습 수 시간~수 일, 렌더링 프레임당 수 초(v1); 장면별 최적화라 일반화 없음;
  카메라 자세 필요(COLMAP); 정적 장면 한정.
- 속도 문제가 후속 연구의 방향을 정의했다 — 그리고 명시적 표현의 라이벌
  [[3d-gaussian-splatting|3DGS]]가 결국 실시간 경쟁에서 이겼다.

### 영향과 후속 연구

신경 렌더링이라는 분야를 출범시켰고(Instant-NGP의 해시 그리드, Mip-NeRF, Zip-NeRF,
동적/대규모 변형), *미분 가능 렌더링*을 표준 도구로 만들었다. 로보틱스/건설에서는: 현장의
사진 수준 디지털 트윈과 데이터 생성용 시뮬레이션 자산([[cosmos|월드모델 데이터 엔진]]).

### 연결

- 다음: [[3d-gaussian-splatting|3D Gaussian Splatting]] (명시적 반격), [[vggt|VGGT]] (feed-forward 3D)
- 도메인: [[05-construction-robotics/index|현장 디지털 트윈]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Explain the relation between the $(x,d)\to(c,\sigma)$ MLP and ray volume rendering · $(x, d) \to (c, \sigma)$ MLP와 광선 볼륨 렌더링의 관계를 설명할 수 있다
- [ ] Say why high frequencies cannot be represented without positional encoding · 위치 인코딩 없이는 고주파를 못 그리는 이유를 말할 수 있다
- [ ] State the limit of per-scene optimization and its cost · 장면별 최적화라는 한계와 그 비용을 말할 수 있다
- [ ] Say what 3DGS changed to obtain real-time rendering · 3DGS가 무엇을 바꿔 실시간을 얻었는지 말할 수 있다
