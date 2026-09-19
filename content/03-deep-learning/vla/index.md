---
title: 4. Vision–Language–Action
tags: [deep-learning, vla, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Specify a VLA by observation, instruction, action representation, horizon, objective, control interface, and closed-loop evidence."
mastery-when: "Raise when policy architecture, action representation, data mixture, or adaptation is the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/vlm/index|3. VLM]], [[02-foundations/rl-basics|7. RL §6]], [[04-robotics/robot-systems-deployment|10. Robot Systems]], and [[04-robotics/teleoperation-demonstration|12. Teleoperation]].

## English

> [!note] First pass
> Read the interface, §§1–3, and questions 1–2. Return to §4 when a paper reports a success rate.

### Running object: D4

At time $t$, **D4** receives image features $o_t$, instruction $l=$ “move left, then down,” and predicts a chunk $a_{t:t+2}$ of three 2-D end-effector deltas. The robot executes only the first $k$ actions before observing again. Write the interface before the architecture:

$$\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l),\qquad a_i=(\Delta x_i,\Delta y_i).$$

### 1. Action representation is part of the method

Joint position, joint velocity, torque, end-effector pose, delta pose, gripper state, and discrete action tokens have different feasibility and control assumptions. “The model outputs actions” is incomplete without units, frame, rate, horizon, and the downstream controller.

If D4 predicts $(0.02,0)$ three times in metres but the low-level interface interprets centimetres, the intended 6 cm motion becomes 0.06 cm. Representation errors are physical errors.

### 2. Behavior cloning and multimodality

For continuous demonstrations, a simple objective is

$$L_{\mathrm{BC}}=\frac1H\sum_{h=0}^{H-1}\|a_{t+h}-\hat a_{t+h}\|_2^2.$$

If equally valid demonstrations pass left and right of an obstacle, their MSE mean may go through it. On D4, two demonstrations at one state are $a=(-1,0)$ and $a=(1,0)$. The MSE-optimal deterministic action is their mean $(0,0)$: neither demonstrated mode, and a collision if the obstacle sits at the origin of the local action frame. Discrete tokens, mixture models, diffusion, and flow policies are alternative output distributions; they do not remove the need for good demonstrations and closed-loop recovery.

### 3. Chunking trades smoothness against feedback

Long chunks reduce compounding autoregressive calls and can preserve coordinated motion, but they delay correction. If inference takes 100 ms and the robot executes 10 actions at 20 Hz, a full open-loop chunk lasts 0.5 s. Receding execution—predict 10, execute 2, observe again—restores feedback at extra compute cost.

### 4. What VLA evidence proves

Separate semantic generalization (choosing the relevant object), motor competence (executing contact-rich motion), embodiment transfer, and recovery. Success rate must define episode, reset, intervention, tolerance, and environment variation. An impressive video is a sample, not an estimator.

Read [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/act|ACT]], and [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] in that order before newer generalist policies.

### Problem set

1. **Draw.** Draw D4 from camera and instruction through policy, chunk buffer, low-level controller, robot, and new observation. Label rates.
2. **Derive.** Three demonstrations at one D4 state are $(-1,0)$, $(-1,0)$, and $(1,0)$. Find the MSE-optimal deterministic prediction and explain its danger.
3. **Interpret.** A policy succeeds on novel object names but uses the same practiced reaching trajectory. Which generalization was shown, and which was not?

> [!tip]- Solutions
> 1. The important loop is observation → policy → buffered actions → controller → world → observation; policy and controller rates are distinct.
> 2. The mean $(-1/3,0)$; still between modes, now biased toward the more frequent left pass, and still not a demonstrated action.
> 3. Semantic/generalization of task selection was shown; new motor-skill acquisition was not.

### Exit check

For any VLA, fill one row containing observation, language, action space/frame/rate, horizon, training data/objective, controller, replanning, and evidence ladder.

## 한국어

> [!note] 처음이라면
> interface와 §1–3, 문제 1–2를 먼저 한다. 논문이 성공률을 보고하면 §4로 돌아온다.

### 계속 쓰는 대상: D4

시간 $t$에 **D4**는 image feature $o_t$와 “왼쪽으로 간 다음 아래로”라는 instruction $l$을 받고, 2차원 말단 delta 행동 세 개의 chunk를 예측한다. architecture보다 먼저 $\pi_\theta(a_{t:t+H-1}\mid o_{\le t},l)$와 $a_i=(\Delta x_i,\Delta y_i)$라는 interface를 쓴다.

### 1. 행동 표현도 방법이다

관절 위치·속도·torque, 말단 pose·delta pose, gripper, action token은 물리 가정이 다르다. 단위·frame·rate·horizon·하위 controller가 없으면 “행동 출력”은 불완전하다.

D4가 $(0.02,0)$을 미터로 세 번 예측했는데 하위 interface가 센티미터로 해석하면, 의도한 6 cm가 0.06 cm가 된다. 표현 오차는 물리 오차다.

### 2. Behavior cloning과 다봉성

$L_{BC}=H^{-1}\sum_h\|a_{t+h}-\hat a_{t+h}\|^2$. 장애물의 좌우로 지나가는 시연을 평균하면 장애물 중앙으로 갈 수 있다. D4의 한 상태에서 시연이 $(-1,0)$과 $(1,0)$이면 MSE-optimal 결정 행동은 평균 $(0,0)$이다. 어느 시연 mode도 아니고, 장애물이 국소 행동 원점에 있으면 충돌한다. token·mixture·diffusion·flow는 출력 분포의 대안이지, 나쁜 시연과 recovery 문제를 없애지 않는다.

### 3. Chunking의 교환

긴 chunk는 호출 횟수와 흔들림을 줄이지만 보정을 늦춘다. 추론이 100 ms이고 로봇이 20 Hz로 행동 10개를 실행하면 전체 open-loop chunk는 0.5초다. 10개를 예측하고 2개만 실행한 뒤 다시 관측하면 feedback을 회복하지만 계산량이 늘어난다.

### 4. 증거 읽기

semantic generalization, motor competence, embodiment transfer, recovery를 나눈다. success rate에는 episode·reset·intervention·tolerance·환경 변동 정의가 필요하다.

### 과제

1. camera→policy→chunk→controller→robot→새 관측 폐루프와 rate를 그린다.
2. D4 한 상태의 시연이 $(-1,0)$, $(-1,0)$, $(1,0)$일 때 MSE-optimal 예측과 위험을 구한다.
3. 새 물체 이름에는 성공하지만 같은 reaching만 썼다면 무엇이 일반화됐는가.

> [!tip]- 정답
> 1. policy rate와 controller rate를 분리한다.
> 2. 평균 $(-1/3,0)$; 여전히 mode 사이이고, 더 잦은 왼쪽 통과 쪽으로 치우치며, 시연된 행동이 아니다.
> 3. semantic 선택은 보였지만 새로운 motor skill은 보이지 않았다.

### 통과 기준

VLA 하나를 observation·language·action/frame/rate·horizon·data/objective·controller·replanning·evidence로 완전히 명세할 수 있다.

