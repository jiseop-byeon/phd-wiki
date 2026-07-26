---
title: 1. Paper Lineage
tags: [moc, reference]
study-depth: Literacy
depth-goal: "Use the map to locate a method historically and explain how neighboring research streams connect."
mastery-when: "Raise the specific downstream method pages—not the whole map—to Working or Mastery."
---

## English

Papers read one at a time are forgotten; papers read as a lineage stay. This page is the
map of which idea split off from which.

**How to read it**: solid arrows = a strong technical or architectural predecessor
relationship; dotted = looser conceptual or ecosystem influence (this is a *teaching*
narrative, not a claim of single strict causation). Follow the nodes top to bottom in time
and they become one story. Start with the single big picture, then descend into the
per-area maps.

### The whole thing on one page: 2012 → today

```mermaid
graph TD
    A["2012 AlexNet<br/>scale beats hand-design"] --> B["2017 Transformer<br/>everything becomes tokens"]
    B --> C["2020-21 the pretraining era<br/>GPT-3 · ViT · CLIP"]
    C --> D["2020-23 the generative turn<br/>DDPM to Stable Diffusion to Flow Matching"]
    C --> E["2023- VLA<br/>RT-2 to OpenVLA to pi-0 to GR00T"]
    D --> E
    C --> F["2018- world models<br/>Dreamer to Genie to Cosmos"]
    D --> F
    F -. synthetic data .-> E
    E --> G["Open question:<br/>physical AI on construction<br/>and manufacturing sites<br/>(ExT is the first signal)"]
    F -.-> G
```

In one sentence: **scale (2012) met tokenization (2017) and became pretraining (2020),
which split into generation (diffusion), action (VLA) and imagination (world models) — and
those three are now meeting again in the physical world.** That last confluence is this
wiki's research direction.

### 2012–2017: two branches meet at the Transformer

```mermaid
graph TD
    subgraph CNNEN["CNN branch - vision"]
    AlexNetE["AlexNet 2012<br/>scale beats hand-design"] --> VGGE["VGG 2015<br/>depth plus small filters"]
    VGGE --> ResNetE["ResNet 2016<br/>residual connections"]
    end
    subgraph RNNEN["RNN branch - language"]
    LSTME["LSTM 1997"] --> S2SE["seq2seq 2014<br/>encoder-decoder"]
    S2SE --> BahdanauE["Bahdanau Attention 2015<br/>attention is born"]
    end
    BahdanauE --> TE["Attention Is All You Need 2017"]
    ResNetE -."residual connections live in<br/>every Transformer block".-> TE
    ResNetE --> ViTE2["ViT 2021"]
```

### Backbone: the main currents after the Transformer

```mermaid
graph TD
    TE["Attention Is All You Need 2017"] --> BERTE["BERT 2019<br/>encoder family"]
    TE --> GPTE["GPT-2/3 2019-20<br/>decoder family"]
    TE --> ViTE["ViT 2021<br/>images as tokens too"]
    ViTE --> CLIPE["CLIP 2021<br/>image-text alignment"]
    GPTE --> LLME["instruction-tuned LLMs<br/>InstructGPT 2022"]
    CLIPE --> VLME["VLM<br/>Flamingo · BLIP-2 · LLaVA"]
    LLME --> VLME
    VLME --> VLAE["VLA<br/>RT-2 · OpenVLA · pi-0 · GR00T"]
```

### Generative: the diffusion family

```mermaid
graph TD
    VAEE["VAE 2014"] --> DDPME["DDPM 2020"]
    GANE["GAN 2014"] -. mainstream shift .-> DDPME
    DDPME --> LDME["Latent Diffusion /<br/>Stable Diffusion 2022"]
    DDPME --> ScoreE["Score SDE 2021"]
    ScoreE --> FME["Flow Matching 2023"]
    LDME --> DiTE["DiT 2023"]
    DiTE --> VideoE["video generation<br/>Sora 2024"]
    FME --> Pi0E["the action head of pi-0, 2024"]
```

### Robot learning: from demonstrations to foundation models

```mermaid
graph TD
    BCE["behavior cloning"] --> RT1E["RT-1 2023"]
    RT1E --> RT2E["RT-2 2023<br/>a VLM put on a robot"]
    DPE["Diffusion Policy 2023"] --> Pi0E2["pi-0 2024"]
    ACTE["ACT/ALOHA 2023"] --> Pi0E2
    RT2E --> OpenVLAE["OpenVLA 2024"]
    OXEE["Open X-Embodiment 2023<br/>dataset"] --> OpenVLAE
    OpenVLAE --> GR00TE["GR00T N1 2025"]
    Pi0E2 --> GR00TE
```

### World models: learning inside imagination

```mermaid
graph TD
    WME["World Models 2018"] --> PlaNetE["PlaNet 2019"]
    PlaNetE --> DreamerE["Dreamer v1-v3<br/>2020-23"]
    JEPAE["JEPA position paper 2022"] --> IJEPAE["I-JEPA 2023"]
    IJEPAE --> VJEPAE["V-JEPA 1-2 2024-25"]
    GenieE["Genie 1-2 2024"] --> PhysAIE["world models for physical AI<br/>Cosmos 2025"]
    DreamerE --> PhysAIE
    VJEPAE --> PhysAIE
```

Related: [[01-canonical-papers/canonical-list|Canonical Paper List]] · [[03-deep-learning/index|Deep Learning map]] · [[05-construction-robotics/lineage|Construction Robotics Lineage]] — the three genealogies of this wiki's own domain.

## 한국어

논문을 낱개로 읽으면 잊어버리지만, 계보로 읽는다면 남는다.
각 분야가 어떤 논문에서 갈라져 나왔는지 한눈에 보기 위한 지도.

**읽는 법**: 실선 화살표 = 강한 기술적·구조적 선행 관계, 점선 = 느슨한 아이디어·생태계
영향 (교육적 서사이지 엄밀한 단일 인과가 아니다). 노드를 시대순(위→아래)으로 따라가면 하나의 이야기가 된다. 아래의 큰 그림 한 장을
먼저 보고, 그다음 분야별 상세 지도로 내려가라.

### 큰 그림 한 장: 2012 → 오늘

```mermaid
graph TD
    A["2012 AlexNet<br/>규모가 설계를 이긴다"] --> B["2017 Transformer<br/>모든 것이 토큰이 된다"]
    B --> C["2020~21 사전학습 시대<br/>GPT-3 · ViT · CLIP"]
    C --> D["2020~23 생성모델 혁명<br/>DDPM → Stable Diffusion → Flow Matching"]
    C --> E["2023~ VLA<br/>RT-2 → OpenVLA → π0 → GR00T"]
    D --> E
    C --> F["2018~ 월드모델<br/>Dreamer → Genie → Cosmos"]
    D --> F
    F -.합성 데이터.-> E
    E --> G["열린 질문:<br/>건설·제조 현장의 physical AI<br/>(ExT가 첫 신호탄)"]
    F -.-> G
```

한 문장으로: **규모(2012)가 토큰화(2017)를 만나 사전학습(2020)이 되고, 그것이 생성(디퓨전)과
행동(VLA)과 상상(월드모델)으로 갈라졌다가, 물리 세계에서 다시 만나는 중이다** — 그 마지막
합류점이 이 위키의 연구 방향이다.

### 2012–2017: 딥러닝의 부상 — 두 갈래가 Transformer에서 만나다

```mermaid
graph TD
    subgraph CNN["CNN 계열 (비전)"]
    AlexNet["AlexNet (2012)<br/>규모가 설계를 이긴다"] --> VGG["VGG (2015)<br/>깊이 + 작은 필터"]
    VGG --> ResNet["ResNet (2016)<br/>residual 연결"]
    end
    subgraph RNN["RNN 계열 (언어)"]
    LSTM["LSTM (1997)"] --> S2S["seq2seq (2014)<br/>인코더-디코더"]
    S2S --> Bahdanau["Bahdanau Attention (2015)<br/>어텐션의 탄생"]
    end
    Bahdanau --> T["Attention Is All You Need (2017)"]
    ResNet -."residual 연결은 모든<br/>Transformer 블록에".-> T
    ResNet --> ViT2["ViT (2021)"]
```

### Backbone: Transformer 이후의 큰 흐름

```mermaid
graph TD
    T["Attention Is All You Need (2017)"] --> BERT["BERT (2019)<br/>인코더 계열"]
    T --> GPT["GPT-2/3 (2019–20)<br/>디코더 계열"]
    T --> ViT["ViT (2021)<br/>이미지도 토큰으로"]
    ViT --> CLIP["CLIP (2021)<br/>이미지-텍스트 정렬"]
    GPT --> LLM["명령어 튜닝 LLM<br/>(InstructGPT, 2022)"]
    CLIP --> VLM["VLM<br/>(Flamingo, BLIP-2, LLaVA)"]
    LLM --> VLM
    VLM --> VLA["VLA<br/>(RT-2, OpenVLA, π0, GR00T)"]
```

### Generative: 디퓨전 계열

```mermaid
graph TD
    VAE["VAE (2014)"] --> DDPM["DDPM (2020)"]
    GAN["GAN (2014)"] -.주류 이동.-> DDPM
    DDPM --> LDM["Latent Diffusion /<br/>Stable Diffusion (2022)"]
    DDPM --> Score["Score SDE (2021)"]
    Score --> FM["Flow Matching (2023)"]
    LDM --> DiT["DiT (2023)"]
    DiT --> Video["비디오 생성<br/>(Sora, 2024)"]
    FM --> Pi0["π0의 action head (2024)"]
```

### Robot Learning: 시연에서 파운데이션 모델로

```mermaid
graph TD
    BC["행동 복제 (BC)"] --> RT1["RT-1 (2023)"]
    RT1 --> RT2["RT-2 (2023)<br/>VLM을 로봇에"]
    DP["Diffusion Policy (2023)"] --> Pi0["π0 (2024)"]
    ACT["ACT/ALOHA (2023)"] --> Pi0
    RT2 --> OpenVLA["OpenVLA (2024)"]
    OXE["Open X-Embodiment (2023)<br/>데이터셋"] --> OpenVLA
    OpenVLA --> GR00T["GR00T N1 (2025)"]
    Pi0 --> GR00T
```

### World Models: 상상 속에서 배우기

```mermaid
graph TD
    WM["World Models (2018)"] --> PlaNet["PlaNet (2019)"]
    PlaNet --> Dreamer["Dreamer v1–v3<br/>(2020–23)"]
    JEPA["JEPA 선언문 (2022)"] --> IJEPA["I-JEPA (2023)"]
    IJEPA --> VJEPA["V-JEPA 1–2 (2024–25)"]
    Genie["Genie 1–2 (2024)"] --> PhysAI["Physical AI용 월드모델<br/>(Cosmos, 2025)"]
    Dreamer --> PhysAI
    VJEPA --> PhysAI
```

관련: [[01-canonical-papers/canonical-list|핵심 논문 리스트]] · [[03-deep-learning/index|딥러닝 지도]] · [[05-construction-robotics/lineage|건설로봇 계보]] — 이 위키 도메인의 세 계보
