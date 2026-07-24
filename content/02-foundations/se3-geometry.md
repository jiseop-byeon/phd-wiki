---
title: 8. 3D Geometry & SE(3)
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 연결 지도 · prerequisites & connection map

## English

Every robot action, camera pose, and 3D reconstruction in this wiki lives in SE(3) — the
space of rigid-body poses. This page is the working set for reading VLA action spaces and
3D vision papers; the full treatment (screws, exponential coordinates) lives in
[[04-robotics/modern-robotics-book|Modern Robotics ch. 3]].

### 1. Rotations are matrices with rules

- A 3D rotation is a matrix $R \in \mathbb{R}^{3\times 3}$ with $R^\top R = I$ and
  $\det R = +1$ — the set of all such matrices is the group **SO(3)**.
- Consequences: columns are an orthonormal frame (the rotated x/y/z axes);
  $R^{-1} = R^\top$ (undoing a rotation is free); rotations compose by multiplication,
  and **order matters** ($R_1 R_2 \ne R_2 R_1$ — rotate your phone about two axes in both
  orders to feel it).
- 2D worked example: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — check $R(90°)\,(1,0)^\top = (0,1)^\top$. All of SO(3) is this idea, three axes at once.

### 2. The four ways papers write rotations

| Representation | Numbers | Strengths | The catch |
|---|---|---|---|
| Rotation matrix | 9 | composition, no singularities | redundant (6 constraints) |
| Euler angles (roll-pitch-yaw) | 3 | human-readable | **gimbal lock**; order conventions bite |
| Axis-angle $(\hat\omega, \theta)$ | 3 | minimal, geometric | composition is awkward |
| **Quaternion** $(w, x, y, z)$ | 4 | no singularities, cheap composition, interpolation (slerp) | double cover: $q$ and $-q$ are the same rotation |

- Learning-specific fact worth knowing: all 3- and 4-number representations are
  *discontinuous* as targets for neural networks — which is why many robot-learning papers
  regress a **6D representation** (first two columns of $R$, then Gram-Schmidt) instead.

### 3. Poses: SE(3) and homogeneous transforms

- A **pose** = rotation + position, packaged as
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ (a $4\times4$ matrix).
- Composition is matrix multiplication: $T_{AC} = T_{AB}\,T_{BC}$ — read subscripts like
  units and they cancel. Inverse: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$.
- **Frames discipline** is 90% of not making sign errors: every quantity has a frame
  (world, base, camera, end-effector); write it down. "Where is the camera?" = $T_{world \leftarrow cam}$.

### 4. Velocity and small motions (the on-ramp to Modern Robotics)

- Angular velocity $\omega$ is a vector (axis × speed); rigid-body velocity = **twist**
  $(\omega, v)$ — six numbers, and the reason end-effector velocity commands are 6-DoF.
- Small rotation ≈ $I + [\hat\omega\theta]_\times$. Why skew-symmetric? A rotation keeps
  lengths fixed, so $R^\top R = I$; differentiating at $R=I$ gives $\dot R + \dot R^\top = 0$,
  i.e. the generator $\dot R$ *must* be skew — its off-diagonal $\pm$ entries are exactly the
  components of the rotation axis $\omega$ (that is what $[\cdot]_\times$ packs). Rotations are
  thus *locally linear*, which is what lets Jacobians ([[02-foundations/calculus-backprop|2. Calculus]])
  map joint rates to end-effector twists, and what the exponential map formalizes
  ([[04-robotics/modern-robotics-book|MR ch. 3]]).

### 5. Where this appears in the wiki

- **VLA action spaces**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]'s 7-DoF action = end-effector
  position (3) + rotation (3) + gripper (1); [[01-canonical-papers/notes/4-vla/pi0|π0]] outputs
  joint-space chunks — reading these requires exactly this page.
- **3D vision**: camera pose in [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]
  is $T \in SE(3)$; "pose estimation" = regressing this matrix.
- **Sim & digital twins**: every simulator state and BIM-robot registration is a stack of
  $T$'s ([[05-construction-robotics/index|construction]]).

### Self-check

1. Verify $R(\theta)R(-\theta) = I$ in 2D, and explain why $R^{-1} = R^\top$ in general.
2. Why does regressing Euler angles with MSE misbehave near $\pm180°$? What do quaternions'
   double cover do to naive MSE?
3. Given $T_{base \leftarrow cam}$ and a point $p_{cam}$, write the point in base frame.
4. A gripper command is "move 5cm along the *gripper's own* z-axis." Is that a left- or
   right-multiplication of the current pose? Why?

> [!tip]- Answers
> 1. Expanding the product gives $\cos^2\theta + \sin^2\theta = 1$ terms → $I$. In general $R$'s columns are orthonormal, so $R^\top R = I \Rightarrow R^{-1} = R^\top$.
> 2. Angle values jump at the $\pm180°$ boundary ($179° \to -179°$, not $-181°$) — neighboring rotations become distant targets and MSE explodes. Quaternions' double cover means $q$ and $-q$ are the same rotation, so a sign-flipped target gives a large loss (wrong gradient) for a correct answer.
> 3. $p_{base} = T_{base \leftarrow cam}\,[p_{cam}; 1]$ (append 1 for homogeneous coordinates, then multiply).
> 4. Right-multiplication $T \cdot \Delta T$ — motion in the body (gripper) frame multiplies on the right; world-frame motion on the left.

### Robotics bridge

This notation is used verbatim throughout the [[04-robotics/modern-robotics/index|Modern Robotics summary]] and the extrinsics of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]]; it becomes operational in [[04-robotics/state-estimation-slam|SLAM and localization]] and the time-indexed TF trees of [[04-robotics/robot-systems-deployment|Robot Systems]].

## 한국어

이 위키의 모든 로봇 행동, 카메라 자세, 3D 재구성은 SE(3) — 강체 자세의 공간 — 에 산다.
이 페이지는 VLA 행동 공간과 3D 비전 논문을 읽기 위한 작업 세트다; 완전한 전개(스크류,
지수 좌표)는 [[04-robotics/modern-robotics-book|Modern Robotics 3장]]의 몫이다.

### 1. 회전은 규칙 있는 행렬이다

- 3D 회전은 $R^\top R = I$이고 $\det R = +1$인 행렬 $R \in \mathbb{R}^{3\times 3}$ —
  이런 행렬 전체의 집합이 군 **SO(3)**다.
- 따름정리: 열들은 정규직교 프레임(회전된 x/y/z 축)이다; $R^{-1} = R^\top$(회전 되돌리기는
  공짜); 회전은 곱셈으로 합성되고 **순서가 중요하다** ($R_1 R_2 \ne R_2 R_1$ — 폰을 두 축으로
  순서 바꿔 돌려보면 몸으로 느껴진다).
- 2D 계산 예제: $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$
  — $R(90°)\,(1,0)^\top = (0,1)^\top$ 검산. SO(3) 전체가 이 아이디어를 세 축으로 한 것이다.

### 2. 논문이 회전을 쓰는 네 가지 방법

| 표현 | 숫자 | 강점 | 함정 |
|---|---|---|---|
| 회전 행렬 | 9 | 합성 쉬움, 특이점 없음 | 중복 (제약 6개) |
| 오일러 각 (roll-pitch-yaw) | 3 | 사람이 읽기 쉬움 | **짐벌 락**; 순서 규약이 문다 |
| 축-각 $(\hat\omega, \theta)$ | 3 | 최소, 기하적 | 합성이 어색 |
| **쿼터니언** $(w, x, y, z)$ | 4 | 특이점 없음, 싼 합성, 보간(slerp) | 이중 덮개: $q$와 $-q$가 같은 회전 |

- 학습 특화 상식: 3·4개 숫자 표현은 모두 신경망의 회귀 타깃으로서 *불연속*이다 — 많은
  로봇 학습 논문이 대신 **6D 표현**($R$의 앞 두 열 + Gram-Schmidt)을 회귀하는 이유다.

### 3. 자세: SE(3)와 동차 변환

- **자세** = 회전 + 위치를 하나로 포장:
  $T = \begin{pmatrix} R & p \\ 0 & 1 \end{pmatrix} \in SE(3)$ ($4\times4$ 행렬).
- 합성은 행렬곱: $T_{AC} = T_{AB}\,T_{BC}$ — 아래 첨자를 단위처럼 읽으면 약분된다.
  역: $T^{-1} = \begin{pmatrix} R^\top & -R^\top p \\ 0 & 1 \end{pmatrix}$
- **프레임 규율**이 부호 실수 안 하기의 90%다: 모든 양에는 프레임(월드, 베이스, 카메라,
  말단)이 있다; 항상 적어라. "카메라가 어디 있나?" = $T_{world \leftarrow cam}$.

### 4. 속도와 미소 운동 (Modern Robotics로 가는 진입로)

- 각속도 $\omega$는 벡터(축 × 속력); 강체 속도 = **twist** $(\omega, v)$ — 여섯 숫자이고,
  말단 속도 명령이 6자유도인 이유다.
- 미소 회전 ≈ $I + [\hat\omega\theta]_\times$. 왜 반대칭인가? 회전은 길이를 보존하므로
  $R^\top R = I$; $R=I$에서 미분하면 $\dot R + \dot R^\top = 0$, 즉 생성원 $\dot R$는 *반드시*
  반대칭이고, 그 비대각 $\pm$ 성분이 정확히 회전축 $\omega$의 성분이다($[\cdot]_\times$가
  담는 것). 그래서 회전은 *국소적으로 선형*이고,
  이것이 야코비안([[02-foundations/calculus-backprop|2. 미적분]])이 관절 속도를 말단
  twist로 사상할 수 있는 이유이자, 지수 사상이 정식화하는 내용이다
  ([[04-robotics/modern-robotics-book|MR 3장]]).

### 5. 이 위키에서 등장하는 곳

- **VLA 행동 공간**: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]의 7자유도 행동 = 말단 위치(3) +
  회전(3) + 그리퍼(1); [[01-canonical-papers/notes/4-vla/pi0|π0]]는 관절 공간 청크를 출력 —
  이들을 읽는 데 정확히 이 페이지가 필요하다.
- **3D 비전**: [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]의
  카메라 자세가 $T \in SE(3)$; "자세 추정" = 이 행렬의 회귀.
- **시뮬레이션과 디지털 트윈**: 모든 시뮬레이터 상태와 BIM-로봇 정합이 $T$들의 스택이다
  ([[05-construction-robotics/index|건설]]).

### 스스로 점검

1. 2D에서 $R(\theta)R(-\theta) = I$를 검산하고, 일반적으로 $R^{-1} = R^\top$인 이유를
   설명하라.
2. 오일러 각을 MSE로 회귀하면 $\pm180°$ 근처에서 왜 이상해지는가? 쿼터니언의 이중 덮개는
   순진한 MSE에 무슨 짓을 하는가?
3. $T_{base \leftarrow cam}$과 점 $p_{cam}$이 주어졌을 때, 베이스 프레임의 점을 써라.
4. "그리퍼 *자신의* z축 방향으로 5cm 이동" 명령은 현재 자세에 왼쪽 곱인가 오른쪽 곱인가?
   왜인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 곱을 전개하면 $\cos^2\theta + \sin^2\theta = 1$ 항등으로 $I$가 나온다. 일반적으로는 $R$의 열들이 정규직교라 $R^\top R = I \Rightarrow R^{-1} = R^\top$.
> 2. $\pm 180°$ 경계에서 각도 값이 점프한다($179° \to -181°$가 아니라 $-179°$) — 이웃한 회전이 먼 타깃이 되어 MSE가 폭발. 쿼터니언은 $q$와 $-q$가 같은 회전이라, 타깃과 부호가 반대면 옳은 답에 큰 손실을 주는 잘못된 그래디언트가 생긴다.
> 3. $p_{base} = T_{base \leftarrow cam}\,[p_{cam}; 1]$ (동차 좌표로 확장해 곱한다).
> 4. 오른쪽 곱 $T \cdot \Delta T$ — 자기(그리퍼) 프레임 기준 운동은 오른쪽에, 월드 프레임 기준 운동은 왼쪽에 곱한다.

### 로보틱스 다리

여기서의 회전·변환 표기는 [[04-robotics/modern-robotics/index|Modern Robotics 요약]] 전체와 [[04-robotics/geometric-perception-calibration|3.5 기하 인식]]의 extrinsics가 그대로 사용하며, [[04-robotics/state-estimation-slam|SLAM·위치 추정]]과 [[04-robotics/robot-systems-deployment|로봇 시스템]]의 시간 인덱스 TF 트리에서 실전이 된다.
