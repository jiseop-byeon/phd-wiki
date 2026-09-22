---
title: 0.6 Lab Plants
tags: [foundations, lab]
study-depth: Working
depth-goal: "Use these six numbered plants as the shared objects of every Foundations and Robotics problem set."
mastery-when: "The catalog is a fixture, not a mastery target."
wiki-support: Working
---

> [!note] Prerequisites · 선수 지식
> None. Open this page whenever a problem set says **P1**–**P6**.
> 없음. 과제가 **P1**–**P6**을 말하면 이 페이지를 연다.

## English

Six plants, numbers frozen once. Problem sets in Foundations and Robotics name a plant by id instead of re-specifying it. Change a number here and every lab that points here is using a different machine. How to step one of them in time is the next page, [[02-foundations/lab-kernel|0.7 Lab Kernel]].

The robotics running task — *move a tool to a panel and make controlled contact* — is **P2** carrying a tool, meeting a wall whose stiffness is the same order as **P3**.

The whole task as one loop, with **P5** locating the panel and **P6** supplying the latency budget, is [[04-robotics/capstone-panel-contact|26. Capstone]].

### P1 — two-layer net

The network of [[02-foundations/neural-network-basics|0.8 §2]] and [[02-foundations/calculus-backprop|2. §3]]. Biases zero, $\sigma=\mathrm{ReLU}$.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\quad W_2=\begin{pmatrix}1&-1&0.5\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix},\quad y=1$$

Forward: $z=(1,2,3)$, $h=(1,2,3)$, $\hat y=0.5$, $L=\tfrac12(0.5-1)^2=0.125$. Canonical for backprop, parameter counts, and a one-step SGD update.

### P2 — planar 2R

Unit links, point masses at the distal end of each link. Angles from the positive $x$-axis, elbow relative. Gravity $g=9.81\,\mathrm{m/s}^2$ acts in $-y$ when a page needs it.

$$L_1=L_2=1\,\mathrm{m},\quad m_1=m_2=1\,\mathrm{kg}$$

At $\theta=(0^\circ,90^\circ)$ the forearm points up. Tip at $(1,1)\,\mathrm{m}$. Position Jacobian and mass matrix (derived on [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5]] and [[02-foundations/manipulator-kinematics-dynamics|10. §3]]):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix},\qquad M=\begin{pmatrix}3&1\\1&1\end{pmatrix},\qquad \det J=1$$

Operational-space inertia at this pose, for a position task: $\Lambda=(JM^{-1}J^\top)^{-1}=\mathrm{diag}(1,2)$. The tip feels twice as heavy in $y$ as in $x$. Used from FK through force control.

Each joint's drive (DC motor, amplifier and $n=100$ gearbox) is frozen on [[04-robotics/actuators-drives|10.5 Actuators & Drives]]. In the horizontal plane P2's dynamics are linear in three base inertial parameters, $\pi=(2,1,1)\,\mathrm{kg\,m^2}$, and a $3\,\mathrm{kg}$ payload at the tip makes them $(5,4,4)$ ([[04-robotics/system-identification|5.5 System Identification §9]]).

### P3 — 1-DoF handle

A translating handle, impedance causality, no Jacobian (identity). Public physics, not a copied worksheet. SI units.

| Symbol | Value | Meaning |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | effective mass at the handle |
| $b$ | $0.8\,\mathrm{N\cdot s/m}$ | physical viscous damping |
| $k_h$ | $400\,\mathrm{N/m}$ | human hand stiffness |
| $b_h$ | $8\,\mathrm{N\cdot s/m}$ | human hand damping |
| $k_w$ | $400\,\mathrm{N/m}$ | virtual-wall stiffness (default) |
| $x_w$ | $0.030\,\mathrm{m}$ | wall location; $+x$ is into the wall |
| Capstan | $r_m=0.010\,\mathrm{m}$, $r_s=0.050\,\mathrm{m}$ | motor pulley / sector radii |
| Encoder | $N=1024$ counts/rev | quadrature after decode |

Human desired position $x_d$ is an external input. Handle position $x$ is the device state. Virtual wall: $F_a=-k_w(x-x_w)$ when $x>x_w$, else $0$. Home of [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]] and [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]. [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] reuses its mass and wall in a drop cell, and [[06-research-practice/psychophysics-human-measurement|8. Psychophysics & Human Measurement §7]] uses it as a stiffness display for a staircase.

### P4 — leaky heater

$$\dot x=-x+u+d$$

$x$ is temperature error, $u$ the command, $d$ an unknown disturbance. Open-loop $u=1$ sits at $x=1+d$. Feedback $u=-Kx$ gives steady state $x=d/(1+K)$. The plant of [[04-robotics/control-theory-ce397|5. Control Theory §1]], reused by LQR and MPC.

Sampled with a zero-order hold at $T=0.1\,\mathrm{s}$ it is exactly $x_{k+1}=0.904837\,x_k+0.095163\,u_k$ when $d=0$, the model [[04-robotics/system-identification|5.5 System Identification]] identifies from data.

### P5 — 1-D range

A wall. Prior: $10\,\mathrm{cm}$ away, variance $4\,\mathrm{cm}^2$. Sensor: reads $12\,\mathrm{cm}$, variance $1\,\mathrm{cm}^2$. Scalar Kalman: $K=4/(4+1)=0.8$, fused estimate $11.6\,\mathrm{cm}$, posterior variance $0.8$. Crack-detector companion (same page): $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$, so $P(c|+)\approx0.16$. Home of [[02-foundations/probability|3. §5]] and [[04-robotics/state-estimation-slam|3. State Estimation]].

### P6 — 1-D cart and a clock

A cart on a line, position $p$ in metres, encoder $N=2048$ counts/m. A vision node publishes a goal at $50\,\mathrm{Hz}$. A controller samples the encoder and commands a motor at $200\,\mathrm{Hz}$. End-to-end budget from camera mid-exposure to applied force: $70\,\mathrm{ms}$ (the number on [[04-robotics/robot-systems-deployment|10. Robot Systems]]). Used for timing, frames, and “nothing happens” failures in ROS 2.

Its sensor noise models (encoder quantization, a single-axis IMU, a range sensor and the camera) are frozen on [[04-robotics/sensor-models|3.2 Sensor Models & Noise]].

### Where each lab lives

| Plant | Canonical lab page (Tier A) |
|---|---|
| P1 | [[02-foundations/calculus-backprop\|2. Calculus & Backprop]] |
| P2 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR ch.5]] and [[02-foundations/manipulator-kinematics-dynamics\|10]] |
| P2, its drive | [[04-robotics/actuators-drives\|10.5 Actuators & Drives]] |
| P2, its inertial parameters | [[04-robotics/system-identification\|5.5 §9]] |
| P3 | [[04-robotics/haptics-teleoperation/rendering-sampling-stability\|24.4]] |
| P4 | [[04-robotics/control-theory-ce397\|5. Control Theory]] |
| P4, identified from data | [[04-robotics/system-identification\|5.5 System Identification]] |
| P5 | [[02-foundations/probability\|3. Probability]] |
| P6 | [[04-robotics/ros2/index\|25. ROS 2]] (weekend path) and [[04-robotics/robot-systems-deployment\|10]] |
| P6, its sensor noise | [[04-robotics/sensor-models\|3.2 Sensor Models & Noise]] |
| P2, P3, P5 and P6 as one loop | [[04-robotics/capstone-panel-contact\|26. Capstone]] |

How to step a continuous plant: [[02-foundations/lab-kernel|0.7 Lab Kernel]]. How a page should use these plants: [[templates/course-page|course-page template]].

## 한국어

장치 여섯 개, 숫자는 한 번만 고정한다. 기초와 로보틱스 과제는 장치를 다시 정의하지 않고 **P1**–**P6** 번호로 부른다. 여기 숫자를 바꾸면 이 페이지를 가리키는 모든 랩이 다른 기계를 쓴다. 이 장치들을 시간에 따라 전진하는 법은 다음 페이지 [[02-foundations/lab-kernel|0.7 Lab Kernel]]이다.

로보틱스 관통 과제 — *도구를 패널까지 옮겨 힘을 조절하며 접촉한다* — 는 도구를 든 **P2**가 **P3** 정도의 강성을 가진 벽을 만나는 것이다.

과제 전체를 **P5**(패널 위치)와 **P6**(지연 예산)까지 넣어 루프 하나로 돌린 것이 [[04-robotics/capstone-panel-contact|26. 캡스톤]]이다.

### P1 — 2층 네트워크

[[02-foundations/neural-network-basics|0.8 §2]]와 [[02-foundations/calculus-backprop|2. §3]]의 네트워크. 편향 0, $\sigma=\mathrm{ReLU}$.

$$W_1=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\quad W_2=\begin{pmatrix}1&-1&0.5\end{pmatrix},\quad x=\begin{pmatrix}1\\2\end{pmatrix},\quad y=1$$

순전파: $z=(1,2,3)$, $h=(1,2,3)$, $\hat y=0.5$, $L=\tfrac12(0.5-1)^2=0.125$. 역전파, 파라미터 수, SGD 한 스텝의 기준 장치.

### P2 — 평면 2R

단위 링크, 각 링크 말단에 점질량. 각은 $+x$축에서, 엘보는 상대각. 중력이 필요하면 $g=9.81\,\mathrm{m/s}^2$가 $-y$.

$$L_1=L_2=1\,\mathrm{m},\quad m_1=m_2=1\,\mathrm{kg}$$

$\theta=(0^\circ,90^\circ)$에서 전완이 위. 말단 $(1,1)\,\mathrm{m}$. 위치 야코비안과 질량 행렬([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장]]과 [[02-foundations/manipulator-kinematics-dynamics|10. §3]]에서 유도):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix},\qquad M=\begin{pmatrix}3&1\\1&1\end{pmatrix},\qquad \det J=1$$

이 자세의 위치 과제에서 작업공간 관성은 $\Lambda=(JM^{-1}J^\top)^{-1}=\mathrm{diag}(1,2)$. 말단은 $x$보다 $y$에서 두 배 무겁다. FK부터 힘 제어까지 이 팔을 쓴다.

관절마다의 구동계(DC 모터, 증폭기, $n=100$ 기어박스)는 [[04-robotics/actuators-drives|10.5 액추에이터·구동계]]에서 고정한다. 수평면에서 P2의 동역학은 기저 관성 파라미터 셋 $\pi=(2,1,1)\,\mathrm{kg\,m^2}$에 선형이고, 말단의 $3\,\mathrm{kg}$ 페이로드는 그것을 $(5,4,4)$로 만든다([[04-robotics/system-identification|5.5 시스템 식별 §9]]).

### P3 — 1자유도 핸들

병진 핸들, 임피던스 인과, 야코비안은 항등. 공개 물리량이지 복사한 워크시트가 아니다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $m$ | $0.04\,\mathrm{kg}$ | 핸들의 유효 질량 |
| $b$ | $0.8\,\mathrm{N\cdot s/m}$ | 물리적 점성 댐핑 |
| $k_h$ | $400\,\mathrm{N/m}$ | 손 강성 |
| $b_h$ | $8\,\mathrm{N\cdot s/m}$ | 손 댐핑 |
| $k_w$ | $400\,\mathrm{N/m}$ | 가상 벽 강성(기본값) |
| $x_w$ | $0.030\,\mathrm{m}$ | 벽 위치; $+x$가 벽 안 |
| 캡스턴 | $r_m=0.010\,\mathrm{m}$, $r_s=0.050\,\mathrm{m}$ | 모터 풀리 / 섹터 반지름 |
| 엔코더 | $N=1024$ counts/rev | 디코드 후 |

사람 목표 $x_d$는 외부 입력, 핸들 위치 $x$가 상태. 가상 벽: $x>x_w$이면 $F_a=-k_w(x-x_w)$, 아니면 $0$. [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]과 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]의 집. [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]은 그 질량과 벽을 낙하 셀에 다시 쓰고, [[06-research-practice/psychophysics-human-measurement|8. 심리물리와 인간 측정 §7]]은 그것을 강성 디스플레이로 삼아 계단법을 돌린다.

### P4 — 새는 히터

$$\dot x=-x+u+d$$

$x$는 온도 오차, $u$는 명령, $d$는 미지 외란. 개루프 $u=1$은 $x=1+d$에 앉는다. 피드백 $u=-Kx$의 정상상태는 $x=d/(1+K)$. [[04-robotics/control-theory-ce397|5. 제어 이론 §1]]의 플랜트. LQR·MPC가 재사용.

영차 유지로 $T=0.1\,\mathrm{s}$마다 샘플하면 $d=0$일 때 정확히 $x_{k+1}=0.904837\,x_k+0.095163\,u_k$이고, [[04-robotics/system-identification|5.5 시스템 식별]]이 데이터에서 식별하는 모델이 이것이다.

### P5 — 1차원 거리

벽. 사전: $10\,\mathrm{cm}$, 분산 $4\,\mathrm{cm}^2$. 센서: $12\,\mathrm{cm}$, 분산 $1\,\mathrm{cm}^2$. 스칼라 칼만: $K=0.8$, 융합 $11.6\,\mathrm{cm}$, 사후 분산 $0.8$. 짝인 균열 감지기: $P(+|c)=0.95$, $P(+|\neg c)=0.05$, $P(c)=0.01$이면 $P(c|+)\approx0.16$. [[02-foundations/probability|3. §5]]와 [[04-robotics/state-estimation-slam|3. 상태 추정]]의 집.

### P6 — 1차원 카트와 시계

직선 위 카트, 위치 $p$는 미터, 엔코더 $N=2048$ counts/m. 비전 노드가 목표를 $50\,\mathrm{Hz}$로 발행. 제어기는 엔코더를 샘플해 모터를 $200\,\mathrm{Hz}$로 명령. 카메라 노출 중간부터 힘이 나갈 때까지 예산 $70\,\mathrm{ms}$([[04-robotics/robot-systems-deployment|10. 로봇 시스템]]의 숫자). 타이밍·프레임·ROS 2의 “아무 일도 안 일어남”에 쓴다.

센서 잡음 모델(엔코더 양자화, 단축 IMU, 거리 센서, 카메라)은 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]에서 고정한다.

### 랩이 사는 곳

| 장치 | 정규 랩 페이지 (Tier A) |
|---|---|
| P1 | [[02-foundations/calculus-backprop\|2. 미적분과 역전파]] |
| P2 | [[04-robotics/modern-robotics/ch05-velocity-kinematics\|MR 5장]]과 [[02-foundations/manipulator-kinematics-dynamics\|10]] |
| P2의 구동계 | [[04-robotics/actuators-drives\|10.5 액추에이터·구동계]] |
| P2의 관성 파라미터 | [[04-robotics/system-identification\|5.5 §9]] |
| P3 | [[04-robotics/haptics-teleoperation/rendering-sampling-stability\|24.4]] |
| P4 | [[04-robotics/control-theory-ce397\|5. 제어 이론]] |
| P4를 데이터로 식별 | [[04-robotics/system-identification\|5.5 시스템 식별]] |
| P5 | [[02-foundations/probability\|3. 확률]] |
| P6 | [[04-robotics/ros2/index\|25. ROS 2]](주말 경로)와 [[04-robotics/robot-systems-deployment\|10]] |
| P6의 센서 잡음 | [[04-robotics/sensor-models\|3.2 센서 모델과 잡음]] |
| P2, P3, P5, P6을 루프 하나로 | [[04-robotics/capstone-panel-contact\|26. 캡스톤]] |

연속 플랜트를 이산 시간으로 푸는 법: [[02-foundations/lab-kernel|0.7 Lab Kernel]]. 페이지가 이 장치를 쓰는 법: [[templates/course-page|course-page 템플릿]].
