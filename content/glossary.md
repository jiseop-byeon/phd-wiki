---
title: Glossary
tags: [reference]
---

빠르게 찾아보는 용어 사전. 새 용어를 만날 때마다 여기에 추가한다. (English term — 한국어 설명)

## A–D

- **Attention** — 쿼리(Q)와 키(K)의 유사도로 값(V)을 가중합하는 연산. 시퀀스 안의 임의의 두 위치를 한 번에 연결한다. → [[canonical-papers/notes/attention-is-all-you-need|Transformer]]
- **Autoregressive (자기회귀)** — 이전 출력들을 조건으로 다음 토큰을 하나씩 생성하는 방식. GPT 계열, 대부분의 VLA가 이 방식.
- **BLEU** — 기계번역 품질 지표. 생성문과 참조 번역의 n-gram 겹침을 측정.
- **Diffusion model (디퓨전 모델)** — 데이터에 노이즈를 점진적으로 섞는 과정을 학습으로 되돌려서 생성하는 모델.

## E–L

- **Embedding (임베딩)** — 토큰·이미지 패치 등 이산적인 입력을 연속 벡터 공간으로 옮긴 표현.
- **Fine-tuning (파인튜닝)** — 사전학습된 모델을 특정 작업 데이터로 추가 학습하는 것.
- **Imitation learning (모방 학습)** — 전문가 시연 데이터로 정책을 학습. 로봇 매니퓰레이션의 주류 접근.
- **LayerNorm** — 각 샘플의 특징 차원 방향으로 정규화하는 기법. Transformer의 기본 구성 요소.

## M–R

- **MPC (Model Predictive Control)** — 매 시점마다 미래 구간의 최적 제어를 풀고 첫 입력만 적용하는 제어 기법. → [[20-robotics/index|제어 트랙]]
- **Multi-head attention** — 어텐션을 여러 개의 저차원 부분공간에서 병렬로 수행해 서로 다른 관계를 학습하게 하는 구조.
- **Positional encoding (위치 인코딩)** — 순서를 모르는 어텐션 연산에 토큰의 위치 정보를 주입하는 방법.

## S–Z

- **Self-attention** — 한 시퀀스가 자기 자신을 참조하는 어텐션. Q, K, V가 모두 같은 시퀀스에서 나온다.
- **VLA (Vision-Language-Action)** — 시각·언어 입력에서 로봇 행동을 직접 출력하는 모델. → [[10-deep-learning/index|딥러닝 지도]]
- **World model (월드모델)** — 환경의 다음 상태를 예측하도록 학습된 모델. 상상 속에서 계획·학습을 가능하게 한다.
- **Zero-shot** — 해당 작업의 학습 예시 없이 바로 수행하는 능력.
