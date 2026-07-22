---
title: "MR Ch.3 — Rigid-Body Motions"
tags: [robotics, modern-robotics]
---

**Modern Robotics ch.3** — [[04-robotics/modern-robotics-book|book guide & free PDF]] · prerequisite: [[02-foundations/se3-geometry|8. SE(3)]]

## English

**Core question**: how do we represent and compose rotations, poses, and velocities of rigid bodies — without singularities?

- **SO(3)/SE(3)** basics are in [[02-foundations/se3-geometry|foundations 8]]; this chapter
  adds the machinery that makes them *computable*:
- **Skew-symmetric bridge**: a vector $\omega \in \mathbb{R}^3$ ↔ matrix
  $[\omega] = \begin{pmatrix}0&-\omega_3&\omega_2\\ \omega_3&0&-\omega_1\\ -\omega_2&\omega_1&0\end{pmatrix}$,
  so cross products become matrix products: $[\omega]v = \omega \times v$.
- **Exponential coordinates (Rodrigues)**: rotating about unit axis $\hat\omega$ by $\theta$:
  $$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2$$
  Every rotation is *one* axis-angle exponential (Euler's theorem); $\log$ recovers it.
  This is the door between Lie group (rotations) and Lie algebra (angular velocities).
- **Twists**: rigid-body velocity $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$; every twist
  is a **screw** (rotate about an axis while translating along it). Pose exponential:
  $T = e^{[\mathcal{S}]\theta}$ — "follow screw $\mathcal{S}$ for angle $\theta$."
- **Adjoint** $[\text{Ad}_T]$: changes the frame of a twist — the bookkeeping operator that
  makes ch.4–5 formulas one-liners.

**Why learning people should care**: exponential/log maps are how you interpolate poses,
average rotations, and define losses on SE(3) correctly — and diffusion/flow policies on
SE(3) ([[01-canonical-papers/notes/pi0|π0]]-style heads for end-effector actions) are built
on exactly this Lie-group machinery.

## 한국어

**핵심 질문**: 강체의 회전·자세·속도를 특이점 없이 어떻게 표현하고 합성하는가?

- **SO(3)/SE(3)** 기초는 [[02-foundations/se3-geometry|기초 8]]에 있다; 이 장은 그것을
  *계산 가능*하게 만드는 기계장치를 더한다:
- **반대칭 다리**: 벡터 $\omega \in \mathbb{R}^3$ ↔ 행렬 $[\omega]$, 그래서 외적이 행렬곱이
  된다: $[\omega]v = \omega \times v$.
- **지수 좌표 (로드리게스)**: 단위축 $\hat\omega$ 둘레로 $\theta$만큼 회전:
  $$R = e^{[\hat\omega]\theta} = I + \sin\theta\,[\hat\omega] + (1-\cos\theta)\,[\hat\omega]^2$$
  모든 회전은 *하나의* 축-각 지수다(오일러 정리); $\log$가 그것을 복원한다.
  리 군(회전)과 리 대수(각속도) 사이의 문이다.
- **Twist**: 강체 속도 $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$; 모든 twist는
  **스크류**다(축 둘레로 돌며 축 방향으로 이동). 자세의 지수:
  $T = e^{[\mathcal{S}]\theta}$ — "스크류 $\mathcal{S}$를 각도 $\theta$만큼 따라가라."
- **Adjoint** $[\text{Ad}_T]$: twist의 프레임을 바꾼다 — 4~5장의 공식들을 한 줄로 만들어
  주는 장부 정리 연산자.

**학습 쪽에서 중요한 이유**: 지수/로그 사상이 자세 보간, 회전 평균, SE(3) 위의 올바른 손실
정의의 방법이고 — 말단 행동에 대한 SE(3) 디퓨전/flow 정책
([[01-canonical-papers/notes/pi0|π0]]류 헤드)이 정확히 이 리 군 기계장치 위에 세워진다.
