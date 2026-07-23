---
title: "Sora — Video Generation Models as World Simulators"
authors: OpenAI (Tim Brooks, Bill Peebles, et al.)
affiliation: OpenAI
venue: Technical report
year: 2024
pdf: https://openai.com/index/video-generation-models-as-world-simulators/
tags: [paper, world-models, generative, diffusion]
status: note-complete
last_verified: 2026-07-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**OpenAI, 2024 (technical report)** — [Report](https://openai.com/index/video-generation-models-as-world-simulators/)

## English

**One-line summary**: A diffusion transformer over spacetime patches of video latents, scaled hard — and the claim that emergent 3D consistency and object permanence make video generators a path to world simulators.

### Context

Video generation had been short, low-resolution, and fixed-format. Two of this wiki's
threads converge here: [[ddpm|diffusion]] with transformer backbones (DiT — Peebles
co-authored both), and the [[scaling-laws|scaling]] playbook. The report's provocation is
in its title: video generation is not (only) content creation — it's *simulation*.

### Method

> [!tip] Key intuition
> Do to video what [[vit|ViT]] did to images and [[gpt-3|GPT]] did to text: chop everything
> into uniform tokens — here spacetime patches of a compressed video latent — and let one
> scalable architecture eat variable durations, resolutions, and aspect ratios.

- Videos compressed by a visual encoder into a latent; cut into **spacetime patches** =
  tokens ([[vit|ViT]] logic extended in time).
- Backbone: **diffusion transformer (DiT)** denoising all patches jointly, conditioned on
  text (with descriptive recaptioning à la DALL·E 3 for better prompt following).
- Native variable-size training (up to 1080p, up to 60s, any aspect ratio); also
  image-to-video, video extension, and editing modes.

### Results (as reported)

- Minute-long, high-fidelity, prompt-faithful video — far past prior systems.
- **Emergent simulation properties with scale**: 3D-consistent camera motion, object
  permanence through occlusion, simple world interactions (a bite leaves a mark) —
  *not architecturally built in*.
- Quality scales smoothly with training compute (the report's compute-comparison grid).

### Limitations & critique

- Physics fails exactly where it matters for robotics: glass shatters wrong, cause-effect
  chains break, quantities don't conserve — plausibility ≠ physical correctness.
- **No actions**: unlike [[genie|Genie]], you cannot *act* in Sora's worlds — it simulates
  appearances, not an interactive environment.
- A technical report, not a paper: no reproducible details, no benchmarks; "world
  simulator" is a hypothesis, and [[jepa|the JEPA camp]] argues pixel prediction is the
  wrong abstraction for it.

### Impact & follow-ups

Reframed video generation as a physical-AI adjacent capability and ignited the
"video models = world models?" debate. Practical descendants: video models used for robot
data augmentation and *neural trajectories* ([[gr00t-n1|GR00T]]), and action-conditioned
video world models ([[cosmos|Cosmos]]) that add what Sora lacks — control.

### Connections

- Previous: [[ddpm|DDPM]] + DiT, [[vit|ViT]] (patch logic), [[scaling-laws|Scaling Laws]]
- Parallel: [[genie|Genie]] (interactive), [[jepa|JEPA]] (the counter-position) · Next: [[cosmos|Cosmos]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 비디오 잠재 표현의 시공간 패치 위에서 도는 디퓨전 트랜스포머를 강하게 스케일 — 그리고 창발한 3D 일관성과 물체 영속성이 비디오 생성기를 월드 시뮬레이터로 가는 길로 만든다는 주장.

### 배경

비디오 생성은 짧고, 저해상도이고, 고정 포맷이었다. 이 위키의 두 갈래가 여기서 만난다:
트랜스포머 백본의 [[ddpm|디퓨전]](DiT — Peebles가 양쪽 모두의 저자다), 그리고
[[scaling-laws|스케일링]] 플레이북. 보고서의 도발은 제목에 있다: 비디오 생성은 (단지)
콘텐츠 제작이 아니라 *시뮬레이션*이다.

### 방법

> [!tip] 핵심 직관
> [[vit|ViT]]가 이미지에, [[gpt-3|GPT]]가 텍스트에 한 일을 비디오에 하라: 모든 것을 균일한
> 토큰으로 자르고 — 여기서는 압축된 비디오 잠재 표현의 시공간 패치 — 하나의 스케일 가능한
> 구조가 가변 길이·해상도·종횡비를 먹게 하라.

- 비디오를 시각 인코더로 잠재 표현으로 압축; **시공간 패치** = 토큰으로 절단
  ([[vit|ViT]] 논리의 시간 확장).
- 백본: 모든 패치의 노이즈를 함께 제거하는 **디퓨전 트랜스포머(DiT)**, 텍스트 조건
  (DALL·E 3식 상세 리캡셔닝으로 프롬프트 충실도 개선).
- 가변 크기 네이티브 학습(최대 1080p, 최대 60초, 임의 종횡비); 이미지→비디오, 비디오 연장,
  편집 모드도 지원.

### 결과 (보고 기준)

- 1분 길이의 고품질·프롬프트 충실 비디오 — 기존 시스템을 크게 상회.
- **규모와 함께 창발한 시뮬레이션 성질**: 3D 일관적 카메라 이동, 가림을 통과하는 물체
  영속성, 간단한 상호작용(베어 문 자국이 남는다) — *구조적으로 넣은 것이 아니다*.
- 품질이 학습 연산량에 따라 매끄럽게 스케일 (보고서의 연산 비교 그리드).

### 한계와 비판

- 로보틱스에 중요한 지점에서 정확히 물리가 실패한다: 유리가 이상하게 깨지고, 인과 사슬이
  끊기고, 양이 보존되지 않는다 — 그럴듯함 ≠ 물리적 정확함.
- **행동이 없다**: [[genie|Genie]]와 달리 Sora의 세계에서는 *행동*할 수 없다 — 상호작용
  환경이 아니라 외양의 시뮬레이션이다.
- 논문이 아니라 기술 보고서: 재현 가능한 세부도, 벤치마크도 없다; "월드 시뮬레이터"는
  가설이고, [[jepa|JEPA 진영]]은 픽셀 예측이 그 목적에 잘못된 추상화라고 반박한다.

### 영향과 후속 연구

비디오 생성을 physical AI 인접 능력으로 재프레임하고 "비디오 모델 = 월드모델?" 논쟁에
불을 붙였다. 실용적 후손: 로봇 데이터 증강과 *신경 궤적*([[gr00t-n1|GR00T]])에 쓰이는
비디오 모델, 그리고 Sora에 없는 것 — 제어 — 를 더한 행동 조건 비디오
월드모델([[cosmos|Cosmos]]).

### 연결

- 이전: [[ddpm|DDPM]] + DiT, [[vit|ViT]] (패치 논리), [[scaling-laws|Scaling Laws]]
- 병행: [[genie|Genie]] (상호작용형), [[jepa|JEPA]] (반대 진영) · 다음: [[cosmos|Cosmos]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] 시공간 패치 = ViT 논리의 시간 확장이라는 것을 말할 수 있다
- [ ] "창발한 시뮬레이션 성질" 주장과 그 반례(물리 실패)를 말할 수 있다
- [ ] 행동이 없다는 한계와 Genie/Cosmos와의 차이를 말할 수 있다
