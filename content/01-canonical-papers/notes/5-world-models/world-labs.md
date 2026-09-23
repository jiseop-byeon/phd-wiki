---
title: "World Labs — Marble, RTFM, Atlas, and a Functional Taxonomy of World Models"
authors: World Labs (founded by Fei-Fei Li, Justin Johnson, Ben Mildenhall and Christoph Lassner)
affiliation: World Labs
venue: Technical posts
year: 2025
pdf: https://www.worldlabs.ai/blog/marble-world-model
tags: [paper, world-models, generative, 3d]
status: note-complete
last_verified: 2026-09-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**World Labs, 2025–2026 (technical posts)** — [Marble](https://www.worldlabs.ai/blog/marble-world-model) · [RTFM](https://www.worldlabs.ai/blog/rtfm) · [Atlas](https://www.worldlabs.ai/blog/atlas) · [A Functional Taxonomy of World Models](https://www.worldlabs.ai/blog/taxonomy-of-world-models)

> [!note] Math on-ramp · 수학 준비물
> [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]] and [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]], the 3D representations these systems output, and the component table of [[03-deep-learning/world-models/index|5. World Models §1]], onto which the taxonomy's three functions map. No new mathematics: the posts disclose no model details, so this note reads claims about outputs, not a method.
> 이 시스템들이 내놓는 3D 표현인 [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]와 [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]], 그리고 분류의 세 기능이 대응되는 [[03-deep-learning/world-models/index|5. 월드모델 §1]]의 구성요소 표. 새 수학은 없다. 글들이 모델 세부를 밝히지 않으므로, 이 노트는 방법이 아니라 출력에 관한 주장을 읽는다.

## English

**One-line summary**: A company built around "spatial intelligence" that generates explorable 3D worlds (Marble), renders them in real time (RTFM) and pretrained one model across text, images, video and 3D (Atlas) — and that proposed the clearest way to sort everything now called a world model: by whether it outputs pixels, state or actions.

### Context

By 2025 "world model" named at least three kinds of system: video generators that look like worlds ([[sora|Sora]], [[genie|Genie]]), latent dynamics a robot plans with ([[dreamer|Dreamer]], the V-JEPA 2-AC of [[jepa|JEPA]]), and models that output a 3D scene. World Labs, founded by Fei-Fei Li with Justin Johnson, Ben Mildenhall — first author of [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]] — and Christoph Lassner, builds the third kind. Its argument is that a model should keep one consistent 3D world rather than a sequence of plausible frames.

### Method (as disclosed)

> [!tip] Key intuition
> Make the world, not the video. Generate a persistent 3D scene once, then render any view of it: a camera can leave a room and come back to the same room, because the room exists.

- **Marble (November 2025)**: takes text, one or several images, video, a coarse 3D layout sketched in its Chisel mode, or existing 3D assets. It outputs Gaussian splats (the highest-fidelity form), triangle meshes, *collider meshes* — low-fidelity geometry meant for rough physics — and video with exact camera control. Worlds can be edited, expanded and composed. It was not interactive at release; the post names interaction as the next step.
- **RTFM (October 2025)**: a real-time frame model that renders video of a scene as the camera moves, on a single H100 GPU. It keeps a large world persistent by storing each generated frame with its 3D pose and retrieving the nearby ones as context, instead of attending to every frame it has made. Camera-conditioned only; released as a research preview.
- **Atlas (September 2026)**: an "omni model" pretrained from scratch on text, images, video and 3D, described as a multimodal autoregressive diffusion transformer. It takes camera poses and depth, and produces images, video up to a minute long at 1440p, point clouds, Gaussian splats and depth. The post shows real-to-sim for navigation and manipulation: reconstruct a real space, then generate the RGB and depth a simulated robot would see as it moves through it.
- **The taxonomy (June 2026)**: a *renderer* outputs pixels for a viewer and may show physically impossible things (text-to-video models, Genie 3, RTFM); a *simulator* outputs state — a representation faithful to geometry, physics or dynamics that programs can compute on, for designers and for agents such as robot controllers; a *planner* outputs actions (vision–language–action models, world action models). The three form a loop, and the post expects the boundaries to blur as renderers become action-conditioned.

### Results (as reported)

- Marble and Atlas are products with demonstrations, not benchmarks. Atlas's post reports comparisons on camera-controlled generation and 3D reconstruction against specialized models, with no paper to check them against.
- The taxonomy is the durable contribution for a reader: it turns "is it a world model?" into "what does it output, and what consumes it?"

### Limitations & critique

- **No paper.** Model sizes, data and training are undisclosed, and the evidence is demonstrations and the company's own comparisons — the [[sora|Sora]] situation, to be read the same way.
- **No dynamics, no contact.** A generated scene has geometry and appearance. The colliders are coarse, and nothing in a generated world says how heavy a panel is, how stiff a surface is or what friction a gripper meets; a physics engine must supply all of it. The taxonomy post itself warns that generated geometry can look right while carrying the wrong scale or self-intersections that break physics.
- **Camera, not action.** As described, RTFM and Atlas are conditioned on camera poses. A robot's own actions — a grasp, a push, a force — are not inputs, so none of these is a model a robot can plan with; the planner row belongs to [[jepa|JEPA]]-style world models and to VLAs.

### Impact & follow-ups

For robotics the offer is the *simulator* row: varied 3D environments produced faster than by hand, and real-to-sim reconstructions of the places a robot will work in. In construction, where every site differs and is costly to model, that is attractive for navigation and perception. For contact-rich manipulation the missing physics is the whole problem. Where the three functions sit among the wiki's world models is [[03-deep-learning/world-models/index|5. World Models §6]].

> [!question] Reading the claim · 핵심 주장 읽는 법
> A generated world that looks right is a renderer's success. Before treating it as a simulator for a robot, ask what state it outputs, whose physics runs on that state, and whether a policy trained in it was ever tested on a real robot.

### Connections

- Previous: [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]] and [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]] (the representations), [[genie|Genie]] (interactive generated worlds)
- Parallel: [[cosmos|Cosmos]] (video world models for physical AI) · Contrast: [[jepa|JEPA]] (the planner row), [[sora|Sora]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: "공간 지능"을 내건 회사로, 돌아다닐 수 있는 3D 세계를 생성하고(Marble), 그것을 실시간으로 렌더링하며(RTFM), 텍스트·이미지·비디오·3D를 한 모델로 사전학습했다(Atlas). 그리고 지금 월드모델이라 불리는 모든 것을 가르는 가장 분명한 방법을 내놓았다. 픽셀을 내는지, 상태를 내는지, 행동을 내는지로 가르는 것이다.

### 배경

2025년이면 "월드모델"은 적어도 세 종류의 시스템을 가리켰다. 세계처럼 보이는 비디오 생성기([[sora|Sora]], [[genie|Genie]]), 로봇이 계획에 쓰는 잠재 동역학([[dreamer|Dreamer]], [[jepa|JEPA]]의 V-JEPA 2-AC), 그리고 3D 장면을 내놓는 모델이다. 페이페이 리가 Justin Johnson, [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]의 제1저자 Ben Mildenhall, Christoph Lassner와 세운 World Labs는 세 번째 종류를 만든다. 그들의 주장은 모델이 그럴듯한 프레임의 연속이 아니라 일관된 3D 세계 하나를 지녀야 한다는 것이다.

### 방법 (공개된 만큼)

> [!tip] 핵심 직관
> 비디오가 아니라 세계를 만들어라. 지속되는 3D 장면을 한 번 생성하고, 그다음 어느 시점이든 렌더링한다. 카메라가 방을 나갔다 돌아와도 같은 방이다. 방이 실제로 있기 때문이다.

- **Marble (2025년 11월)**: 텍스트, 이미지 한 장이나 여러 장, 비디오, Chisel 모드로 그린 거친 3D 배치, 기존 3D 자산을 받는다. Gaussian splat(가장 충실한 형태), 삼각형 메시, *충돌용 메시* — 거친 물리 계산을 위한 저해상도 기하 — 그리고 카메라를 정확히 제어한 비디오를 낸다. 세계를 편집하고 넓히고 이어 붙일 수 있다. 공개 당시에는 상호작용이 없었고, 글은 상호작용을 다음 단계로 꼽는다.
- **RTFM (2025년 10월)**: 카메라가 움직이는 동안 장면의 비디오를 H100 한 장에서 실시간으로 렌더링하는 실시간 프레임 모델이다. 생성한 모든 프레임에 주의를 두는 대신, 각 프레임을 3D 자세와 함께 저장하고 가까운 것들을 문맥으로 불러와 큰 세계를 유지한다. 카메라 조건만 있고, 연구 미리보기로 공개됐다.
- **Atlas (2026년 9월)**: 텍스트·이미지·비디오·3D로 처음부터 사전학습한 "옴니 모델"로, 다중 모달 자기회귀 디퓨전 트랜스포머라고 설명된다. 카메라 자세와 깊이를 받아 이미지, 1440p로 최대 1분 길이의 비디오, 점군, Gaussian splat, 깊이를 낸다. 글은 내비게이션과 조작을 위한 real-to-sim을 보인다. 실제 공간을 재구성한 뒤, 시뮬레이션 로봇이 그 속을 움직일 때 볼 RGB와 깊이를 생성한다.
- **분류 (2026년 6월)**: *렌더러*는 보는 사람을 위한 픽셀을 내고 물리적으로 불가능한 것도 보여 줄 수 있다(텍스트→비디오 모델, Genie 3, RTFM). *시뮬레이터*는 상태를 낸다. 기하·물리·동역학에 충실해서 프로그램이 계산할 수 있는 표현으로, 설계자와 로봇 제어기 같은 에이전트를 위한 것이다. *플래너*는 행동을 낸다(시각–언어–행동 모델, 월드 액션 모델). 셋은 고리를 이루고, 글은 렌더러가 행동 조건을 갖추면서 경계가 흐려지리라 본다.

### 결과 (보고 기준)

- Marble과 Atlas는 벤치마크가 아니라 시연이 있는 제품이다. Atlas의 글은 카메라 제어 생성과 3D 재구성에서 특화 모델과의 비교를 보고하지만, 대조해 볼 논문은 없다.
- 읽는 사람에게 오래 남는 기여는 분류다. "월드모델인가?"를 "무엇을 내놓고, 무엇이 그것을 쓰는가?"로 바꾼다.

### 한계와 비판

- **논문이 없다.** 모델 크기, 데이터, 학습이 공개되지 않았고, 증거는 시연과 회사 자신의 비교다. [[sora|Sora]]와 같은 처지이고, 같은 방식으로 읽어야 한다.
- **동역학도 접촉도 없다.** 생성된 장면에는 기하와 겉모습이 있다. 충돌용 메시는 거칠고, 생성된 세계의 어디에도 패널이 얼마나 무거운지, 표면이 얼마나 단단한지, 그리퍼가 어떤 마찰을 만나는지가 없다. 물리 엔진이 그 전부를 대야 한다. 분류 글 스스로도 생성된 기하가 맞아 보이면서 스케일이 틀리거나 자기 교차가 있어 물리를 망칠 수 있다고 경고한다.
- **행동이 아니라 카메라다.** 설명된 대로라면 RTFM과 Atlas는 카메라 자세를 조건으로 받는다. 잡기, 밀기, 힘 같은 로봇 자신의 행동은 입력이 아니므로, 어느 것도 로봇이 계획에 쓸 수 있는 모델이 아니다. 플래너 행은 [[jepa|JEPA]]식 월드모델과 VLA의 몫이다.

### 영향과 후속 연구

로봇에게 주는 것은 *시뮬레이터* 행이다. 손으로 만드는 것보다 빠르게 만든 다양한 3D 환경, 그리고 로봇이 일할 곳의 real-to-sim 재구성이다. 현장마다 다르고 모델링이 비싼 건설에서는 내비게이션과 인식에 매력적이다. 접촉이 많은 조작에는 빠진 물리가 문제 전부다. 세 기능이 위키의 월드모델들 사이 어디에 서는지는 [[03-deep-learning/world-models/index|5. 월드모델 §6]]에 있다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 맞아 보이는 생성된 세계는 렌더러의 성공이다. 그것을 로봇의 시뮬레이터로 다루기 전에, 어떤 상태를 내놓는지, 그 상태 위에서 누구의 물리가 도는지, 그 안에서 학습한 정책을 실제 로봇에서 시험한 적이 있는지 물어라.

### 연결

- 이전: [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]와 [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]] (표현), [[genie|Genie]] (상호작용하는 생성 세계)
- 병행: [[cosmos|Cosmos]] (physical AI를 위한 비디오 월드모델) · 대비: [[jepa|JEPA]] (플래너 행), [[sora|Sora]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Sort a system called a world model by what it outputs — pixels, state or actions · "월드모델"이라 불리는 시스템을 내놓는 것 — 픽셀, 상태, 행동 — 으로 가를 수 있다
- [ ] Say what Marble outputs and which of those a physics engine can use · Marble이 무엇을 내놓고 그중 무엇을 물리 엔진이 쓸 수 있는지 말할 수 있다
- [ ] Explain how RTFM keeps a large world persistent · RTFM이 큰 세계를 어떻게 유지하는지 설명할 수 있다
- [ ] Name what a generated scene lacks for contact-rich manipulation · 생성된 장면이 접촉이 많은 조작에 무엇을 빠뜨리는지 말할 수 있다
