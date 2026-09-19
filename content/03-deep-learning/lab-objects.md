---
title: 0. Deep-Learning Lab Objects
tags: [deep-learning, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Reuse six small, fully specified objects to trace tensor shapes, objectives, inference, and failure across the deep-learning curriculum."
mastery-when: "Raise only the object family that becomes part of the thesis contribution."
---

## English

These objects are deliberately tiny. Their purpose is not benchmark performance; it is to make every symbol and tensor in the six course pages concrete. All numbers below are fixed so that a calculation in one page can be checked in another.

| ID | Object | Fixed specification | Used in |
|---|---|---|---|
| **D1** | small classifier | input $x=(1,2)$, hidden width 3, two classes | learning foundations |
| **D2** | patch image | grayscale $8\times8$ image, $4\times4$ patches, 4 patch tokens | computer vision |
| **D3** | aligned batch | three image–caption pairs; unit-normalized 2-D embeddings | VLM |
| **D4** | action chunk | observation token plus three 2-D delta actions | VLA |
| **D5** | scalar latent plant | $z_{t+1}=0.8z_t+0.5a_t$, reward $r_t=-z_t^2-0.1a_t^2$ | world models |
| **D6** | scalar diffusion datum | clean $x_0=2$, noise $\epsilon=-1$, $\bar\alpha_t=0.64$ | diffusion and flow |

### The common reading contract

For every object, keep four lines separate:

1. **Representation:** what numbers stand for the world.
2. **Prediction:** what the model computes from its inputs.
3. **Objective:** which discrepancy changes learned parameters.
4. **Evaluation:** which measurement supports the paper's claim.

If a paper changes only line 1, it proposes a representation. If it changes line 3, it proposes a training method. If it reports only line 4 without defining the deployment distribution, its claim is incomplete. This four-line ledger is the bridge from the equations here to the canonical-paper notes.

## 한국어

이 장치들은 의도적으로 작다. 벤치마크 성능이 목적이 아니라 여섯 교과 페이지의 기호와 텐서를 모두 손으로 추적하는 것이 목적이다. 한 페이지의 계산을 다른 페이지에서 검산할 수 있도록 숫자를 고정한다.

| ID | 대상 | 고정 사양 | 사용처 |
|---|---|---|---|
| **D1** | 작은 분류기 | 입력 $x=(1,2)$, 은닉 폭 3, 두 클래스 | 학습 기초 |
| **D2** | 패치 이미지 | 회색조 $8\times8$, $4\times4$ 패치, 패치 토큰 4개 | 컴퓨터비전 |
| **D3** | 정렬 배치 | 이미지–캡션 3쌍, 단위 정규화 2차원 임베딩 | VLM |
| **D4** | 행동 청크 | 관측 토큰 하나와 2차원 델타 행동 3개 | VLA |
| **D5** | 스칼라 잠재 장치 | $z_{t+1}=0.8z_t+0.5a_t$, $r_t=-z_t^2-0.1a_t^2$ | 월드모델 |
| **D6** | 스칼라 확산 자료 | $x_0=2$, 잡음 $\epsilon=-1$, $\bar\alpha_t=0.64$ | 디퓨전·flow |

### 공통 독해 계약

모든 대상에서 네 줄을 분리한다.

1. **표현:** 어떤 숫자가 세계의 무엇을 뜻하는가.
2. **예측:** 모델이 입력에서 무엇을 계산하는가.
3. **목적함수:** 어떤 오차가 학습 파라미터를 바꾸는가.
4. **평가:** 어떤 측정이 논문의 주장을 뒷받침하는가.

1번만 바꾸면 표현 연구, 3번을 바꾸면 학습법 연구다. 배포 분포를 정의하지 않은 채 4번만 보고하면 주장은 불완전하다. 이 네 줄 장부가 여기의 수식과 핵심 논문 노트를 잇는다.

