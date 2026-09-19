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
| **D1** | small classifier | $x=(1,2)$, $W_1\in\mathbb R^{3\times2}$, $W_2\in\mathbb R^{2\times3}$, biases $0$; forward $s=(2,1)$ | learning foundations |
| **D2** | patch image | grayscale $8\times8$ image, $4\times4$ patches, 4 patch tokens | computer vision |
| **D3** | aligned batch | three unit 2-D pairs, $\tau=1/2$; image-1 logits $(2,1,0)$ | VLM |
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

### Frozen numbers

**D1.** Biases zero, $\sigma=\mathrm{ReLU}$. Distinct from **P1** ($2\to3\to1$ MSE) on [[02-foundations/lab-plants|0.6]].

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}$$

Forward: $W_1x=(1,2,1)$, $h=(1,2,1)$, $s=W_2h=(2,1)$. Home of [[03-deep-learning/foundations/index|1. Learning Systems]].

**D3.** Matched pairs are aligned. All vectors are unit length.

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix},\quad\tau=\tfrac12$$

Dots $v_1^\top t_j=(1,1/2,0)$, so image-1 logits are $\ell_{1j}=v_1^\top t_j/\tau=(2,1,0)$. Lowering $\tau$ to $1/4$ on the same row gives $(4,2,0)$. Home of [[03-deep-learning/vlm/index|3. VLM]].

## 한국어

이 장치들은 의도적으로 작다. 벤치마크 성능이 목적이 아니라 여섯 교과 페이지의 기호와 텐서를 모두 손으로 추적하는 것이 목적이다. 한 페이지의 계산을 다른 페이지에서 검산할 수 있도록 숫자를 고정한다.

| ID | 대상 | 고정 사양 | 사용처 |
|---|---|---|---|
| **D1** | 작은 분류기 | $x=(1,2)$, $W_1\in\mathbb R^{3\times2}$, $W_2\in\mathbb R^{2\times3}$, bias $0$; 순전파 $s=(2,1)$ | 학습 기초 |
| **D2** | 패치 이미지 | 회색조 $8\times8$, $4\times4$ 패치, 패치 토큰 4개 | 컴퓨터비전 |
| **D3** | 정렬 배치 | 단위 2차원 3쌍, $\tau=1/2$; 이미지 1 logit $(2,1,0)$ | VLM |
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

### 고정 숫자

**D1.** bias 0, $\sigma=\mathrm{ReLU}$. [[02-foundations/lab-plants|0.6]]의 **P1**($2\to3\to1$ MSE)과 다른 장치다.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\quad W_2=\begin{pmatrix}0&1&0\\1&0&0\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix}$$

순전파: $W_1x=(1,2,1)$, $h=(1,2,1)$, $s=W_2h=(2,1)$. 사용처 [[03-deep-learning/foundations/index|1. Learning Systems]].

**D3.** 짝이 맞는 쌍은 정렬되어 있고 모든 벡터는 단위 길이다.

$$v_1=t_1=\begin{pmatrix}1\\0\end{pmatrix},\quad v_2=t_2=\begin{pmatrix}1/2\\\sqrt{3}/2\end{pmatrix},\quad v_3=t_3=\begin{pmatrix}0\\1\end{pmatrix},\quad\tau=\tfrac12$$

내적 $v_1^\top t_j=(1,1/2,0)$이므로 이미지 1 logit은 $(2,1,0)$이다. 같은 행에서 $\tau=1/4$이면 $(4,2,0)$이다. 사용처 [[03-deep-learning/vlm/index|3. VLM]].

