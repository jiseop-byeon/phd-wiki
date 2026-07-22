---
title: Paper Lineage · 논문 계보도
tags: [moc, reference]
---

논문을 낱개로 읽으면 잊어버리지만, 계보로 읽으면 남는다.
각 분야가 어떤 논문에서 갈라져 나왔는지 한눈에 보기 위한 지도.
노트를 작성할 때마다 여기에 연결한다.

## 2012–2017: 딥러닝의 부상 — 두 갈래가 Transformer에서 만나다

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

## Backbone: Transformer 이후의 큰 흐름

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

## Generative: 디퓨전 계열

```mermaid
graph TD
    VAE["VAE (2014)"] --> DDPM["DDPM (2020)"]
    GAN["GAN (2014)"] -.대체됨.-> DDPM
    DDPM --> LDM["Latent Diffusion /<br/>Stable Diffusion (2022)"]
    DDPM --> Score["Score SDE (2021)"]
    Score --> FM["Flow Matching (2023)"]
    LDM --> DiT["DiT (2023)"]
    DiT --> Video["비디오 생성<br/>(Sora, 2024)"]
    FM --> Pi0["π0의 action head (2024)"]
```

## Robot Learning: 시연에서 파운데이션 모델로

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

## World Models: 상상 속에서 배우기

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

관련: [[canonical-papers/canonical-list|핵심 논문 리스트]] · [[10-deep-learning/index|딥러닝 지도]]
