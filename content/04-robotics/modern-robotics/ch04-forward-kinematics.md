---
title: "MR Ch.04 — Forward Kinematics"
tags: [robotics, modern-robotics]
study-depth: Working
wiki-support: Literacy
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
---

**Modern Robotics ch.4** — [[04-robotics/modern-robotics-book|book guide & free PDF]]

> [!note] 시작 전 점검 · Before you start
> [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장]]의 $e^{[\mathcal{S}]\theta}$와 스크류 축, 그리고 4×4 동차 변환의 곱을 쓸 수 있어야 한다.

## English

**Core question**: given joint angles $\theta$, where is the end-effector?

### The Product of Exponentials — one formula

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

Read right-to-left: start at the home pose $M$ (all joints zero), then each joint screws
everything downstream of it. Two ingredients only: the home pose, and one screw axis per
joint *written in the fixed frame at the home position*. No intermediate link frames —
which is the advantage over Denavit-Hartenberg and why modern software is PoE-native.
(The **body form** $T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$ expresses the same thing
with axes in the end-effector frame.)

### Worked example, start to finish — planar 2R arm

Links $L_1 = L_2 = 1$, both stretched along $+\hat x$ at home. The general recipe, then
the numbers:

**Step 1 — home pose $M$.** End-effector at $(2, 0, 0)$, aligned with the base:
$$M = \begin{pmatrix} 1&0&0&2\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 2 — screw axis of joint 1.** Axis direction $\hat\omega_1 = (0,0,1)$; a point on
the axis $q_1 = (0,0,0)$; linear part $v_1 = -\hat\omega_1 \times q_1 = (0,0,0)$.
So $\mathcal{S}_1 = (0,0,1;\; 0,0,0)$.

**Step 3 — screw axis of joint 2.** $\hat\omega_2 = (0,0,1)$; $q_2 = (1,0,0)$;
$v_2 = -\hat\omega_2 \times q_2 = -(0,1,0) = (0,-1,0)$.
So $\mathcal{S}_2 = (0,0,1;\; 0,-1,0)$.

**Step 4 — evaluate at $\theta_1 = \theta_2 = 90°$.**
$e^{[\mathcal{S}_2]\,90°}$ rotates everything by 90° about the vertical axis through
$q_2 = (1,0,0)$. Apply it to $M$: the end-effector sits at $p - q_2 = (1,0,0)$ relative to
the axis; rotated 90° it becomes $(0,1,0)$; adding $q_2$ back gives $(1,1,0)$, with
orientation $R_z(90°)$. Then $e^{[\mathcal{S}_1]\,90°}$ rotates that result 90° about the
origin: $(1,1,0) \to (-1,1,0)$, orientation $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**Step 5 — sanity check against plain geometry.** $\theta_1 = 90°$ points link 1 along
$+\hat y$ (elbow at $(0,1)$); $\theta_2 = 90°$ adds another 90°, pointing link 2 along
$-\hat x$; tip $= (0,1) + (-1,0) = (-1, 1)$, total orientation $180°$. **Same answer.**
Do this double-check on every robot you model — geometric FK and PoE FK must agree.

The recipe generalizes verbatim: home pose → per-joint $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → exponentials → multiply. For code, the Modern Robotics
Python library implements `FKinSpace(M, Slist, thetalist)` — verify your hand computation
against it once per mechanism.

**Wiki connections**: FK is the deterministic core inside every simulator and digital
twin ([[05-construction-robotics/index|construction]]); VLAs that output joint chunks
([[01-canonical-papers/notes/4-vla/pi0|π0]]) rely on FK to interpret them in task space.

### Self-check

1. For the same arm, compute $T(0°, 90°)$ — elbow position, tip position, orientation.
2. Why is $v_i = -\hat\omega_i \times q_i$? (What is the velocity of the origin-coincident
   point when the body rotates about the axis through $q_i$?)
3. In the body form, which joint's exponential sits closest to $M$, and why?

> [!tip]- 정답 · Answers
> 1. 팔꿈치 $(1,0)$, 관절 2만 90° 회전 → 링크 2가 $+\hat y$ 방향, 끝점 $(1,1,0)$, 방향 $R_z(90°)$.
> 2. 축이 $q_i$를 지나므로 원점과 겹친 몸체 점의 속도는 $\omega \times (0 - q_i) = -\omega \times q_i$ — [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]]의 "$v$의 정확한 의미" 그대로다.
> 3. 관절 $n$ (말단에 가장 가까운 관절) — 바디 형식은 말단 프레임 기준이라 곱의 순서가 뒤집힌다.

## 한국어

**핵심 질문**: 관절 각 $\theta$가 주어지면 말단은 어디에 있는가?

### 지수 곱 공식 — 단 하나의 공식

$$T(\theta) = e^{[\mathcal{S}_1]\theta_1}\, e^{[\mathcal{S}_2]\theta_2} \cdots e^{[\mathcal{S}_n]\theta_n}\, M$$

오른쪽에서 왼쪽으로 읽어라: 홈 자세 $M$(모든 관절 0)에서 시작해, 각 관절이 자기 하류
전체를 스크류로 돌린다. 재료는 둘뿐이다: 홈 자세, 그리고 관절마다 *홈 위치에서 고정
프레임 기준으로 쓴* 스크류 축 하나. 중간 링크 프레임이 필요 없다 — 이것이 D-H 대비
장점이고 현대 소프트웨어가 PoE 네이티브인 이유다. (**바디 형식**
$T = M\,e^{[\mathcal{B}_1]\theta_1}\cdots$은 축을 말단 프레임에서 쓴 같은 내용이다.)

### 처음부터 끝까지 계산 예제 — 평면 2R 팔

링크 $L_1 = L_2 = 1$, 홈에서 둘 다 $+\hat x$ 방향으로 뻗어 있다. 일반 레시피와 숫자를
함께 따라가라:

**1단계 — 홈 자세 $M$.** 말단이 $(2, 0, 0)$, 베이스와 같은 방향:
$$M = \begin{pmatrix} 1&0&0&2\\ 0&1&0&0\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**2단계 — 관절 1의 스크류 축.** 축 방향 $\hat\omega_1 = (0,0,1)$; 축 위의 점
$q_1 = (0,0,0)$; 선형부 $v_1 = -\hat\omega_1 \times q_1 = (0,0,0)$.
따라서 $\mathcal{S}_1 = (0,0,1;\; 0,0,0)$.

**3단계 — 관절 2의 스크류 축.** $\hat\omega_2 = (0,0,1)$; $q_2 = (1,0,0)$;
$v_2 = -\hat\omega_2 \times q_2 = (0,-1,0)$.
따라서 $\mathcal{S}_2 = (0,0,1;\; 0,-1,0)$.

**4단계 — $\theta_1 = \theta_2 = 90°$에서 평가.**
$e^{[\mathcal{S}_2]\,90°}$는 $q_2 = (1,0,0)$를 지나는 수직축 둘레로 모든 것을 90° 돌린다.
$M$에 적용하면: 말단은 축 기준 $p - q_2 = (1,0,0)$에 있고, 90° 돌리면 $(0,1,0)$, $q_2$를
되더하면 $(1,1,0)$, 방향은 $R_z(90°)$. 그다음 $e^{[\mathcal{S}_1]\,90°}$가 그 결과를 원점
둘레로 90° 돌린다: $(1,1,0) \to (-1,1,0)$, 방향 $R_z(180°)$:
$$T(90°, 90°) = \begin{pmatrix} -1&0&0&-1\\ 0&-1&0&1\\ 0&0&1&0\\ 0&0&0&1 \end{pmatrix}$$

**5단계 — 순수 기하로 검산.** $\theta_1 = 90°$면 링크 1이 $+\hat y$ 방향(팔꿈치
$(0,1)$); $\theta_2 = 90°$가 90°를 더해 링크 2는 $-\hat x$ 방향; 끝점 $= (0,1) + (-1,0)
= (-1, 1)$, 총 방향 $180°$. **같은 답이다.** 모델링하는 모든 로봇에서 이 이중 검산을
하라 — 기하 FK와 PoE FK는 반드시 일치해야 한다.

레시피는 그대로 일반화된다: 홈 자세 → 관절별 $(\hat\omega_i, q_i)$ →
$v_i = -\hat\omega_i \times q_i$ → 지수들 → 곱. 코드로는 Modern Robotics 파이썬
라이브러리의 `FKinSpace(M, Slist, thetalist)`가 이것을 구현한다 — 기구마다 한 번은
손계산과 라이브러리 결과를 대조하라.

**위키 연결**: FK는 모든 시뮬레이터·디지털 트윈([[05-construction-robotics/index|건설]])
안의 결정론적 핵심이고, 관절 청크를 출력하는 VLA([[01-canonical-papers/notes/4-vla/pi0|π0]])를
작업 공간에서 해석하는 데 쓰인다.

### 스스로 점검

1. 같은 팔에서 $T(0°, 90°)$를 계산하라 — 팔꿈치 위치, 끝점 위치, 방향.
2. 왜 $v_i = -\hat\omega_i \times q_i$인가? ($q_i$를 지나는 축 둘레로 돌 때, 원점과 겹친
   몸체 점의 속도는 무엇인가?)
3. 바디 형식에서는 어느 관절의 지수가 $M$에 가장 가까이 붙는가? 왜인가?

> [!tip]- 정답 · Answers
> 1. 팔꿈치 $(1,0)$; 링크 2가 $+\hat y$ 방향 → 끝점 $(1,1,0)$; 방향 $R_z(90°)$.
> 2. 원점과 겹친 몸체 점은 축에서 $-q_i$만큼 떨어져 있으므로 속도는 $\omega \times (-q_i)$ — [[04-robotics/modern-robotics/ch03-rigid-body-motions|3장 §3]]의 $v$ 정의 그대로.
> 3. 관절 $n$(말단 쪽) — 바디 형식은 말단 프레임 기준이므로 곱 순서가 공간 형식과 반대다.
