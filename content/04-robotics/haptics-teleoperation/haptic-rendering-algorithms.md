---
title: 24.7 Haptic Rendering Algorithms
tags: [haptics, rendering, virtual-environments]
study-depth: Working
wiki-support: Working
depth-goal: "Read a haptic rendering paper and say which algorithm computes the force, what it cannot render, and which of its realism claims rest on perception rather than physics."
mastery-when: "Master constraint-based rendering and friction-model identification when the rendering algorithm itself is the contribution."
---

> [!note] Prerequisites · 선수 지식
> The rendering loop and its stability limits from [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] — this page assumes you already know why $K \le 2b/T$ exists and asks what to compute *inside* that limit. Jacobians from [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]] for the last step of every loop.
> [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]의 렌더링 루프와 안정성 한계 — 이 페이지는 $K \le 2b/T$가 왜 생기는지 이미 안다고 보고, 그 한계 *안에서* 무엇을 계산할지를 묻는다. 모든 루프의 마지막 단계에 필요한 야코비안은 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]].

## English

### 1. What the loop actually computes

Every impedance-type haptic loop does the same four things, once per servo period: read the device position, decide whether the user's point is touching something in the virtual environment, compute a force if it is, and send that force to the motors through $J^\top$ ([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]). [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] is about step four's stability. This page is about steps two and three: the *algorithm* that turns geometry into a force.

One fact shapes all of it. With an impedance device nothing is rigid: every contact is a spring, $F = Kx$, and $K$ is capped by the device and the sample rate. So the design question is never "how do I render a rigid wall" but "how do I make a soft spring *feel* like one". The answers fall into three families: better geometry (§2–§3), perceptual tricks (§4), and surface properties layered on top (§5–§6).

### 2. Penalty-based rendering

The simplest algorithm treats penetration as a spring compression. For a wall with unit normal $\hat n$ through a point $p_0$, the penetration depth of the device point $p$ is $d = (p_0 - p)\cdot\hat n$, and

$$F = \begin{cases} K\,d\,\hat n, & d > 0 \\ 0, & d \le 0 \end{cases}$$

pushes the point back out along the normal. A sphere is the same with $\hat n$ pointing from the centre to $p$ and $d = R - \lVert p - c\rVert$; a box is six walls with the nearest face chosen. Because the force is a function of position only, it is stateless, cheap, and the natural first thing to write.

> [!example] Worked example · 계산 예제
> A wall tilted 45° from the $x$ axis, $K = 500$ N/m, and the device point $3$ mm inside it. Penetration is measured along the normal, so $F = 500 \times 0.003 = 1.5$ N along $\hat n = (\cos 45°, \sin 45°)$, i.e. about $1.06$ N in $x$ and $1.06$ N in $y$. The user feels one force normal to the surface; the device produces it as two motor torques via $J^\top$. Note what is *not* here: nothing resists sliding along the wall, which is why a penalty wall feels like ice (§5).

Penalty methods fail in three ways, and Ruspini, Kolarov and Khatib named them (SIGGRAPH 1997):

- **Lack of locality.** The force depends only on the current position, not on how the point got there. Where two surfaces meet, "nearest surface" can change from one sample to the next, and the force flips direction. 24.4 §1 mentions this as the edge that ejects the user sideways.
- **Force discontinuities.** The same flip produces a step in force, which the hand feels as a click or a kick that no real object makes.
- **Pop-through of thin objects.** A penalty force always points toward the *nearest* surface. Push past the middle of a thin wall and the nearest surface is the far side, so the algorithm helpfully pushes you out the back.

> [!example] Worked example · 계산 예제
> A virtual plate $4$ mm thick rendered with $K = 1000$ N/m. The largest force the plate can produce before the device point crosses its mid-plane is $K \times 2\,\text{mm} = 2$ N. Any user who pushes harder than $2$ N pops through and is then pushed out the other side. Raising $K$ helps only until the stability ceiling of 24.4; making the plate thicker helps only until it looks wrong.

### 3. Constraint-based rendering: the proxy

The fix is to give the algorithm memory. Keep a second point, the **proxy** (Ruspini et al. 1997) or **god object** (Zilles & Salisbury, IROS 1995), that is constrained to stay on the surface of the virtual objects. The device point may penetrate; the proxy may not. Each servo period the proxy moves toward the device point as far as the constraints allow — the same idea as a greedy planner walking toward a goal and sliding along whatever obstacle it hits — and the rendered force is a spring between the two:

$$F = K\,(p_{\text{proxy}} - p_{\text{device}})$$

This resolves all three failures at once. The proxy remembers which side of the wall it entered from, so a thin plate holds; it follows the surface continuously around edges, so there is no flip; and the force direction is always proxy-minus-device, so it never points *into* the object. Friction comes almost free: let the proxy lag the device point tangentially until the tangential spring force exceeds a friction cone, then let it slip. The same proxy idea extends to streaming point clouds (Ryden & Chizeck, *IEEE ToH* 6(3), 2013), which is how telepresence systems render a depth camera's view as a touchable surface. On a one-degree-of-freedom device the proxy is trivial — the surface is a single coordinate — which is why a 1-DOF wall can be written as the penalty form in 24.4 without meeting any of these problems. The idea also scales up. Deformable objects replace the rigid surface with a simulated mesh that the proxy presses on (for example Ding & Hasegawa, EuroHaptics 2020), and multi-point hand or exoskeleton interfaces give each contact link its own proxy (Galvan, Ramirez, Deshpande & Fey, WHC 2023).

### 4. Perceptual tricks: event-based haptics

The stiffness ceiling is a physics limit. Perceived hardness, it turns out, is not mostly about stiffness. When you tap a table, what tells you it is hard is the short, high-frequency transient at the instant of contact, not the steady spring afterwards. Kuchenbecker, Fiene and Niemeyer (*IEEE TVCG* 12(2), 2006) built on this: keep the proportional wall soft enough to be stable, and at the moment of contact add a brief **open-loop transient** — a fixed-width pulse, a decaying sinusoid, or a recorded acceleration profile scaled to the incoming velocity (**acceleration matching**).

Their user study (WHC 2005, nine subjects, eleven samples rated for realism on a 1–7 scale, average tap speed 0.11 m/s) is the evidence to remember: real wood was rated most realistic, followed by wood-on-foam and the acceleration-matched virtual surfaces; plain foam and the two proportional-only virtual walls were rated least realistic. The acceleration-matched library recorded from the wood-on-foam sample was rated at the same level as that sample. Two caveats travel with the result. The transients are large force spikes, and users drove the device into saturation an average of five times each, most often with the decaying sinusoid and acceleration matching. And realism was a rating, not a task outcome — see [[04-robotics/haptics-teleoperation/experiments-readings|24.6]] for why that distinction matters.

A second trick lives in the graphics: never draw the tool penetrating the surface, even though it does. Vision dominates, and the surface is judged stiffer when the picture says the tool stopped. Wu, Basdogan and Srinivasan (ASME IMECE 1999) measured this visual effect on perceived stiffness. Both tricks are honest in the same sense: they render the *cue* the nervous system uses, not the physics the device cannot produce.

### 5. Damping and friction on the surface

A pure spring wall feels active and slippery. Two cheap additions fix most of it:

- **Normal damping, entering only.** Add $-B v_n$ while the point moves *into* the wall and nothing while it leaves. Damping on the way out would pull the user back in. Entry damping also bleeds off the vibration that a stiff spring rings with at impact. This is the wall of 24.4 §1, and the $B$ there is this $B$.
- **Tangential damping.** Add $-B_t v_t$ for motion parallel to the surface. It is not friction — it vanishes at rest — but it removes the ice feeling.

Real friction has a stuck state, and rendering it means switching between two regimes. The **Karnopp model** (*J. Dyn. Sys. Meas. Control* 107(1), 1985) is the workhorse: while the point is *stuck*, the friction force equals the applied tangential force up to a static limit $F_s$; once $\lvert F_a\rvert > F_s$ the point *slides* with friction $F_d\,\mathrm{sgn}(v) + b v$; when speed drops below a small threshold $D_v$ it sticks again and the velocity is set to zero. The threshold is the trick that makes it computable: exact zero velocity never occurs in sampled data. The **Dahl** and **elasto-plastic** models (Dupont, Armstrong & Hayward, ACC 2000) replace the switch with a bristle-like state that captures pre-sliding displacement, and the Hayward–Armstrong variant (2000) removes the position drift the original Dahl model has.

> [!example] Worked example · 계산 예제
> Karnopp wall with $F_s = 3.5$ N, $F_d = 3.0$ N, $b = 10$ N·s/m. The user pushes sideways with $2$ N: below $F_s$, so the point stays stuck and the rendered friction is exactly $2$ N, opposing — the hand feels a surface that holds. The user pushes with $5$ N: the point breaks free and slides; at $v = 0.05$ m/s the friction is $3.0 + 10 \times 0.05 = 3.5$ N, so the net accelerating force is $1.5$ N. Slow down below $D_v$ and it sticks again. Everything the user feels as "grip" is the $F_s - F_d$ gap and the switch.

Is friction worth rendering? Richard and Cutkosky (ICRA 2002) measured it with Fitts-type targeting: twenty subjects, five resistance conditions, nine difficulty indices. Moderate friction — a real aluminium block on rubber at about 3.5 N, or a simulated match — made the easiest index about 17% (real) and 23% (simulated) faster with fewer errors. High stiction (about 7 N) slowed one index by 64% and produced hunting around the target. So friction is a feature at the right level and a defect past it, and the level is task-dependent.

### 6. Textures and moving objects

**Bumps and textures** are the penalty idea turned sideways: derive a force from a height field, opposing motion "uphill", and the hand reports a bump. Minsky et al. (I3D 1990) built the first such display, and Robles-De-La-Torre and Hayward (*Nature* 412, 2001) showed the surprising half: force information can *overcome* geometry, so a flat surface with the right lateral force pattern is felt as a bump, and a real bump with the force pattern removed is not. Texture rendering therefore has a frequency budget — the device must reproduce the force pattern at the speed the finger crosses it — which is the same bandwidth argument as [[04-robotics/haptics-teleoperation/tactile-display-design|24.2]]. Damping can be textured the same way: vary $B$ over position and a smooth surface reads as sticky or rough patches. Recorded vibration is the other route; the event-based transients of §4 grew out of reality-based vibration models fitted to tapping data (Okamura, Cutkosky & Dennerlein, *IEEE/ASME T-Mech* 2001).

**Dynamic objects** add simulation to rendering. Each period: sum the forces on the object (the user's spring force, equal and opposite to what the user feels, plus penalty forces from other objects), divide by mass, integrate to a new velocity and position, and use the new position for next period's collision check. The integrator matters — 24.4 §2 explains why — and the trapezoidal rule is the common choice (a numerical integrator that averages the old and new rates over the step, $x_{k+1}=x_k+\tfrac{T}{2}(v_k+v_{k+1})$; unrelated to the trapezoidal velocity profile of [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]], which only shares the name).

> [!example] Worked example · 계산 예제
> A virtual $0.5$ kg block, $K = 1000$ N/m, the user's point $2$ mm into it: the user feels $2$ N and the block receives $2$ N, so $a = 4$ m/s². At a $1$ kHz loop one period adds $4$ mm/s of velocity and, with the trapezoidal rule, moves the block about $2$ µm — small enough that the collision state does not change between samples, which is the assumption the whole scheme rests on. Halve the mass or double the stiffness and check that assumption again.

### 7. Reading a rendering paper

Four questions separate the claims. **Which algorithm computes the force** — penalty, proxy, or something learned — because that fixes what cannot be rendered (thin objects, edges, friction). **What device, at what stiffness** — the "Nerf World" complaint that force feedback feels soft is a device limit, and a rendering result on a $200$ N/m wall does not transfer to a $2000$ N/m one. **Is realism a rating or a task outcome** — the event-based study measured ratings; the friction study measured completion time and errors; both are legitimate, and they answer different questions. **Where is the perceptual trick** — an acceleration transient or a visual clamp is a valid contribution, but it is a claim about the human, not about the physics, and it should be evaluated with the tools of [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]].

### After reading

- Write the penalty force for a tilted wall and a sphere, and name its three failure modes.
- Explain what the proxy adds, and why a 1-DOF device never needs it.
- State what event-based haptics renders, what the WHC 2005 study measured, and its two caveats.
- Give the Karnopp state machine and say when friction helps a task and when it hurts.

### Self-check

1. A user reports being "thrown out the back" of a thin virtual panel. Which algorithm is running, why does it happen, and what is the one-line fix?
2. Your device's stability limit is $K \le 300$ N/m and a reviewer says the wall feels like foam. Name two changes that make it feel harder *without* raising $K$, and say what each one costs.
3. A paper renders friction with a Karnopp model and reports that users finished a peg-insertion task faster. What would you check before believing that friction was the cause?

> [!tip]- Answers
> 1. A penalty (position-only) method: the force points toward the nearest surface, which becomes the far face once the point passes the panel's mid-plane. Fix: track a surface-constrained proxy and render the spring between proxy and device point, so the algorithm remembers which side the user entered from.
> 2. Add an event-based contact transient (a pulse or acceleration-matched profile at impact); it costs force headroom and can saturate the actuators. Clamp the visual tool at the surface; it costs nothing physically but is a perceptual claim and can conflict with other visual cues. Normal damping on entry is a third option; it costs some of the passivity budget of 24.4.
> 3. Whether the comparison was against no friction or against a *different* friction level (Richard & Cutkosky found moderate friction helped and high stiction hurt), whether the effect held across difficulty indices or only the easiest, whether errors moved with time, and whether the friction level was matched to a real reference or tuned until it "felt good" — which would make the result a preference, not a task effect.

## 한국어

### 1. 루프가 실제로 계산하는 것

임피던스형 햅틱 루프는 서보 주기마다 같은 네 가지를 한다. 장치 위치를 읽고, 사용자의 점이 가상 환경의 무언가에 닿았는지 판단하고, 닿았다면 힘을 계산하고, 그 힘을 $J^\top$로 모터에 보낸다([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]). [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]는 넷째 단계의 안정성을 다룬다. 이 페이지는 둘째와 셋째 단계, 즉 기하를 힘으로 바꾸는 *알고리즘*을 다룬다.

사실 하나가 전부를 결정한다. 임피던스 장치에서는 아무것도 강체가 아니다. 모든 접촉은 스프링 $F = Kx$이고, $K$는 장치와 샘플링 주기가 상한을 정한다. 그러니 설계 질문은 "강체 벽을 어떻게 렌더링하나"가 아니라 "무른 스프링을 어떻게 강체처럼 *느껴지게* 하나"다. 답은 세 계열로 나뉜다. 더 나은 기하(§2–§3), 지각적 트릭(§4), 그 위에 얹는 표면 특성(§5–§6).

### 2. 벌점 기반 렌더링

가장 단순한 알고리즘은 침투를 스프링 압축으로 다룬다. 단위 법선 $\hat n$이 점 $p_0$를 지나는 벽에 대해, 장치 점 $p$의 침투 깊이는 $d = (p_0 - p)\cdot\hat n$이고

$$F = \begin{cases} K\,d\,\hat n, & d > 0 \\ 0, & d \le 0 \end{cases}$$

가 점을 법선 방향으로 밀어낸다. 구는 $\hat n$이 중심에서 $p$를 향하고 $d = R - \lVert p - c\rVert$인 같은 식이다. 상자는 벽 여섯 개에서 가장 가까운 면을 고른 것이다. 힘이 위치만의 함수라서 상태가 없고, 싸고, 가장 먼저 쓰게 되는 코드다.

> [!example] 계산 예제 · Worked example
> $x$축에서 45° 기울어진 벽, $K = 500$ N/m, 장치 점이 벽 안쪽 $3$ mm. 침투는 법선을 따라 재므로 $F = 500 \times 0.003 = 1.5$ N이 $\hat n = (\cos 45°, \sin 45°)$ 방향으로 걸리고, $x$와 $y$ 성분은 각각 약 $1.06$ N이다. 사용자는 표면에 수직인 힘 하나를 느끼고, 장치는 그것을 $J^\top$를 거쳐 모터 토크 둘로 만든다. 여기 *없는* 것을 보라. 벽을 따라 미끄러지는 것을 막는 힘이 전혀 없고, 그래서 벌점 벽은 얼음처럼 느껴진다(§5).

벌점 방법은 세 가지로 실패하고, Ruspini, Kolarov, Khatib(SIGGRAPH 1997)이 그 이름을 붙였다.

- **국소성의 결여.** 힘은 현재 위치에만 달려 있지 점이 어떻게 거기 왔는지와 무관하다. 두 면이 만나는 곳에서는 "가장 가까운 면"이 샘플마다 바뀔 수 있고, 힘의 방향이 뒤집힌다. 24.4 §1이 사용자를 옆으로 튕겨 내는 모서리로 언급한 것이 이것이다.
- **힘의 불연속.** 같은 뒤집힘이 힘의 계단을 만들고, 손은 그것을 실제 물체는 내지 않는 딸깍거림이나 걷어차임으로 느낀다.
- **얇은 물체의 pop-through.** 벌점 힘은 언제나 *가장 가까운* 면을 향한다. 얇은 벽의 중간을 지나 밀면 가장 가까운 면은 반대쪽이 되고, 알고리즘은 친절하게도 뒤로 밀어내 준다.

> [!example] 계산 예제 · Worked example
> 두께 $4$ mm의 가상 판을 $K = 1000$ N/m로 렌더링한다. 장치 점이 판의 중간면을 넘기 전까지 판이 낼 수 있는 최대 힘은 $K \times 2\,\text{mm} = 2$ N이다. $2$ N보다 세게 미는 사용자는 누구나 뚫고 들어가 반대쪽으로 밀려 나간다. $K$를 올리는 것은 24.4의 안정성 천장까지만 통하고, 판을 두껍게 하는 것은 보기에 이상해지기 전까지만 통한다.

### 3. 제약 기반 렌더링: proxy

해법은 알고리즘에 기억을 주는 것이다. 가상 물체의 표면 위에 머물도록 제약된 두 번째 점, **proxy**(Ruspini 외 1997) 또는 **god object**(Zilles & Salisbury, IROS 1995)를 둔다. 장치 점은 침투해도 되지만 proxy는 안 된다. 서보 주기마다 proxy는 제약이 허락하는 만큼 장치 점 쪽으로 움직이고 — 목표를 향해 걷다가 부딪힌 장애물을 따라 미끄러지는 탐욕적 계획기와 같은 발상이다 — 렌더링되는 힘은 둘 사이의 스프링이다.

$$F = K\,(p_{\text{proxy}} - p_{\text{device}})$$

이것이 세 실패를 한꺼번에 푼다. proxy가 어느 쪽에서 벽에 들어왔는지 기억하므로 얇은 판이 버틴다. 모서리를 돌 때 표면을 연속으로 따라가므로 뒤집힘이 없다. 힘의 방향이 언제나 proxy 빼기 장치이므로 물체 *안쪽*을 가리키는 일이 없다. 마찰은 거의 공짜로 온다. 접선 방향 스프링 힘이 마찰 원뿔을 넘을 때까지 proxy를 접선 방향으로 뒤처지게 두고, 넘으면 미끄러지게 한다. 같은 proxy 발상은 스트리밍 점군으로 확장되어(Ryden & Chizeck, *IEEE ToH* 6(3), 2013), 텔레프레즌스 시스템이 깊이 카메라의 시야를 만질 수 있는 표면으로 렌더링하는 방식이 된다. 1자유도 장치에서는 proxy가 자명하다 — 표면이 좌표 하나다 — 그래서 24.4의 1자유도 벽은 이 문제들을 하나도 만나지 않고 벌점 형태로 쓸 수 있다. 이 발상은 규모도 키울 수 있다. 변형 물체는 강체 표면 대신 proxy가 누르는 시뮬레이션 메시를 쓰고(예: Ding & Hasegawa, EuroHaptics 2020), 손이나 외골격의 다점 인터페이스는 접촉 링크마다 proxy를 둔다(Galvan, Ramirez, Deshpande & Fey, WHC 2023).

### 4. 지각적 트릭: 사건 기반 햅틱

강성 천장은 물리 한계다. 그런데 지각되는 단단함은 대부분 강성의 문제가 아니다. 탁자를 두드릴 때 단단하다고 알려 주는 것은 접촉 순간의 짧은 고주파 과도 신호이지 그 뒤의 정상 스프링이 아니다. Kuchenbecker, Fiene, Niemeyer(*IEEE TVCG* 12(2), 2006)는 여기서 출발했다. 비례 벽은 안정할 만큼 무르게 두고, 접촉 순간에 짧은 **개루프 과도 신호**를 더한다 — 고정 폭 펄스, 감쇠 정현파, 또는 진입 속도에 맞춰 크기를 조절한 기록된 가속도 프로파일(**가속도 정합**).

기억할 증거는 그들의 사용자 연구다(WHC 2005, 피험자 9명, 시료 11개를 1–7점 현실감으로 평가, 평균 두드림 속도 0.11 m/s). 실제 나무가 가장 현실적이라 평가됐고, 폼 위의 나무와 가속도 정합 가상 표면이 그 뒤를 이었다. 맨 폼과 비례 제어만 쓴 두 가상 벽이 가장 낮았다. 폼 위 나무에서 기록한 가속도 정합 라이브러리는 그 시료와 같은 수준으로 평가됐다. 단서 둘이 결과에 따라붙는다. 과도 신호는 큰 힘 스파이크라서 사용자가 장치를 평균 다섯 번씩 포화시켰고, 감쇠 정현파와 가속도 정합에서 가장 잦았다. 그리고 현실감은 평가 점수이지 과제 결과가 아니다 — 그 구분이 왜 중요한지는 [[04-robotics/haptics-teleoperation/experiments-readings|24.6]].

두 번째 트릭은 그래픽에 있다. 도구가 실제로는 표면을 뚫고 들어가더라도 뚫는 모습을 절대 그리지 않는다. 시각이 지배하므로, 그림이 도구가 멈췄다고 말하면 표면은 더 단단하다고 판단된다. Wu, Basdogan, Srinivasan(ASME IMECE 1999)이 인지 강성에 대한 이 시각 효과를 측정했다. 두 트릭은 같은 의미에서 정직하다. 장치가 낼 수 없는 물리가 아니라 신경계가 쓰는 *단서*를 렌더링하는 것이다.

### 5. 표면 위의 댐핑과 마찰

순수 스프링 벽은 능동적이고 미끄럽게 느껴진다. 값싼 추가 둘이 대부분을 고친다.

- **들어갈 때만 거는 법선 댐핑.** 점이 벽 *안으로* 움직이는 동안만 $-B v_n$을 더하고 나올 때는 아무것도 하지 않는다. 나올 때의 댐핑은 사용자를 다시 안으로 끌어당긴다. 진입 댐핑은 단단한 스프링이 충돌 순간 울리는 진동도 흘려 없앤다. 이것이 24.4 §1의 벽이고, 거기의 $B$가 이 $B$다.
- **접선 댐핑.** 표면에 평행한 운동에 $-B_t v_t$를 더한다. 마찰은 아니다 — 정지하면 사라진다 — 하지만 얼음 느낌은 없앤다.

실제 마찰에는 붙어 있는 상태가 있고, 이를 렌더링하려면 두 영역을 전환해야 한다. **Karnopp 모델**(*J. Dyn. Sys. Meas. Control* 107(1), 1985)이 주력이다. 점이 *붙어 있는* 동안 마찰력은 정지 한계 $F_s$까지 가해진 접선 힘과 같다. $\lvert F_a\rvert > F_s$가 되면 점은 $F_d\,\mathrm{sgn}(v) + b v$의 마찰을 받으며 *미끄러진다*. 속도가 작은 문턱 $D_v$ 아래로 떨어지면 다시 붙고 속도는 0으로 놓는다. 이 문턱이 계산 가능하게 만드는 요령이다. 샘플링된 데이터에서 정확한 0 속도는 결코 나오지 않는다. **Dahl** 모델과 **탄소성** 모델(Dupont, Armstrong, Hayward, ACC 2000)은 이 스위치를 미끄러지기 전 변위를 담는 강모(bristle) 같은 상태로 바꾸고, Hayward–Armstrong 변형(2000)은 원래 Dahl 모델의 위치 표류를 없앤다.

> [!example] 계산 예제 · Worked example
> $F_s = 3.5$ N, $F_d = 3.0$ N, $b = 10$ N·s/m인 Karnopp 벽. 사용자가 옆으로 $2$ N을 민다. $F_s$보다 작으므로 점은 붙어 있고 렌더링되는 마찰은 정확히 $2$ N을 반대 방향으로 낸다 — 손은 버티는 표면을 느낀다. $5$ N을 밀면 점이 풀려 미끄러지고, $v = 0.05$ m/s에서 마찰은 $3.0 + 10 \times 0.05 = 3.5$ N이라 순 가속력은 $1.5$ N이다. $D_v$ 아래로 느려지면 다시 붙는다. 사용자가 "그립"으로 느끼는 모든 것은 $F_s - F_d$의 간격과 스위치다.

마찰은 렌더링할 가치가 있나? Richard와 Cutkosky(ICRA 2002)는 Fitts형 표적 과제로 쟀다. 피험자 20명, 저항 조건 다섯, 난이도 지수 아홉. 적당한 마찰 — 고무 위의 실제 알루미늄 블록으로 약 3.5 N, 또는 그에 맞춘 시뮬레이션 — 은 가장 쉬운 지수를 약 17%(실제)와 23%(시뮬레이션) 빠르게 하고 오류를 줄였다. 높은 정지 마찰(약 7 N)은 한 지수를 64% 느리게 하고 표적 주변에서 헤매게 만들었다. 그러니 마찰은 알맞은 수준에서는 기능이고 그것을 넘으면 결함이며, 그 수준은 과제에 달렸다.

### 6. 질감과 움직이는 물체

**돌기와 질감**은 벌점 발상을 옆으로 돌린 것이다. 높이장에서 힘을 유도해 "오르막" 운동을 막으면 손은 돌기를 보고한다. Minsky 외(I3D 1990)가 그런 디스플레이를 처음 만들었고, Robles-De-La-Torre와 Hayward(*Nature* 412, 2001)가 놀라운 절반을 보였다. 힘 정보는 기하를 *이길* 수 있다. 알맞은 횡방향 힘 패턴을 가진 평면은 돌기로 느껴지고, 힘 패턴을 제거한 실제 돌기는 돌기로 느껴지지 않는다. 그래서 질감 렌더링에는 주파수 예산이 있다 — 손가락이 지나는 속도로 힘 패턴을 재현해야 한다 — 그리고 이것은 [[04-robotics/haptics-teleoperation/tactile-display-design|24.2]]와 같은 대역폭 논증이다. 댐핑도 같은 방식으로 질감을 줄 수 있다. 위치에 따라 $B$를 바꾸면 매끈한 표면이 끈적하거나 거친 패치로 읽힌다. 기록된 진동이 또 다른 길이다. §4의 사건 기반 과도 신호는 두드림 데이터에 맞춘 실측 기반 진동 모델에서 자라났다(Okamura, Cutkosky & Dennerlein, *IEEE/ASME T-Mech* 2001).

**동적 물체**는 렌더링에 시뮬레이션을 더한다. 주기마다 물체에 걸리는 힘을 합하고(사용자의 스프링 힘, 즉 사용자가 느끼는 것과 크기가 같고 방향이 반대인 힘, 그리고 다른 물체들의 벌점 힘), 질량으로 나누고, 적분해 새 속도와 위치를 얻고, 그 새 위치를 다음 주기의 충돌 검사에 쓴다. 적분기가 중요하고 — 24.4 §2가 이유를 설명한다 — 사다리꼴 규칙이 흔한 선택이다(한 스텝 동안 이전 변화율과 새 변화율을 평균하는 수치 적분기, $x_{k+1}=x_k+\tfrac{T}{2}(v_k+v_{k+1})$. [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]의 사다리꼴 속도 프로파일과는 이름만 같을 뿐 관계가 없다).

> [!example] 계산 예제 · Worked example
> $0.5$ kg의 가상 블록, $K = 1000$ N/m, 사용자의 점이 $2$ mm 안에 있다. 사용자는 $2$ N을 느끼고 블록은 $2$ N을 받으므로 $a = 4$ m/s²다. $1$ kHz 루프에서 한 주기는 속도를 $4$ mm/s 더하고, 사다리꼴 규칙으로 블록을 약 $2$ µm 움직인다 — 샘플 사이에 충돌 상태가 바뀌지 않을 만큼 작고, 이 방식 전체가 그 가정 위에 서 있다. 질량을 반으로 줄이거나 강성을 두 배로 하면 그 가정을 다시 확인하라.

### 7. 렌더링 논문 읽기

질문 넷이 주장을 가른다. **어느 알고리즘이 힘을 계산하는가** — 벌점, proxy, 아니면 학습된 것 — 그것이 렌더링할 수 없는 것(얇은 물체, 모서리, 마찰)을 정하기 때문이다. **어떤 장치를, 어떤 강성으로** — 힘 피드백이 무르게 느껴진다는 "Nerf World" 불평은 장치 한계이고, $200$ N/m 벽의 렌더링 결과는 $2000$ N/m 벽으로 옮겨지지 않는다. **현실감이 평가 점수인가 과제 결과인가** — 사건 기반 연구는 점수를 쟀고 마찰 연구는 완료 시간과 오류를 쟀다. 둘 다 정당하고 서로 다른 질문에 답한다. **지각적 트릭은 어디 있는가** — 가속도 과도 신호나 시각적 고정은 정당한 기여지만 물리가 아니라 인간에 대한 주장이고, [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]]의 도구로 평가해야 한다.

### 읽고 나면

- 기울어진 벽과 구의 벌점 힘을 쓰고, 세 가지 실패 방식의 이름을 댄다.
- proxy가 무엇을 더하는지, 왜 1자유도 장치에는 필요 없는지 설명한다.
- 사건 기반 햅틱이 무엇을 렌더링하는지, WHC 2005 연구가 무엇을 쟀는지, 그 단서 둘을 말한다.
- Karnopp 상태 기계를 쓰고, 마찰이 과제에 도움이 될 때와 해가 될 때를 말한다.

### 스스로 점검

1. 사용자가 얇은 가상 패널의 "뒤로 튕겨 나간다"고 보고한다. 어떤 알고리즘이 돌고 있고, 왜 그런 일이 생기며, 한 줄짜리 수정은 무엇인가?
2. 장치의 안정성 한계가 $K \le 300$ N/m인데 심사자가 벽이 폼처럼 느껴진다고 한다. $K$를 올리지 *않고* 더 단단하게 느끼게 하는 변경 둘을 대고, 각각의 대가를 말하라.
3. 어떤 논문이 Karnopp 모델로 마찰을 렌더링하고 사용자가 펙 삽입 과제를 더 빨리 끝냈다고 보고한다. 마찰이 원인이라고 믿기 전에 무엇을 확인하겠는가?

> [!tip]- 정답 · Answers
> 1. 벌점(위치만 보는) 방법이다. 힘은 가장 가까운 면을 향하는데, 점이 패널의 중간면을 지나면 그것이 반대쪽 면이 된다. 수정: 표면에 제약된 proxy를 추적하고 proxy와 장치 점 사이의 스프링을 렌더링해, 알고리즘이 사용자가 어느 쪽에서 들어왔는지 기억하게 한다.
> 2. 사건 기반 접촉 과도 신호(충돌 시 펄스나 가속도 정합 프로파일)를 더한다. 힘 여유를 쓰고 액추에이터를 포화시킬 수 있다. 시각적 도구를 표면에 고정한다. 물리적 비용은 없지만 지각에 대한 주장이고 다른 시각 단서와 충돌할 수 있다. 진입 시 법선 댐핑이 셋째 선택지이고, 24.4의 수동성 예산 일부를 쓴다.
> 3. 비교 대상이 마찰 없음이었는지 *다른* 마찰 수준이었는지(Richard & Cutkosky는 적당한 마찰은 돕고 높은 정지 마찰은 해친다고 보았다), 효과가 난이도 지수 전체에서 나타났는지 가장 쉬운 것에서만 나타났는지, 오류가 시간과 함께 움직였는지, 그리고 마찰 수준이 실제 기준에 맞춰졌는지 아니면 "느낌이 좋을 때까지" 조정됐는지 — 후자라면 결과는 과제 효과가 아니라 선호다.

### Sources

- K. Salisbury, F. Conti, F. Barbagli, "Haptic rendering: introductory concepts," *IEEE Computer Graphics and Applications* 24(2):24–32, 2004. DOI 10.1109/MCG.2004.1274058 — the survey the four-step loop and "nothing is rigid" framing come from.
- D. C. Ruspini, K. Kolarov, O. Khatib, "The haptic display of complex graphical environments," *SIGGRAPH 1997*, pp. 345–352. DOI 10.1145/258734.258878 — the three penalty failures and the virtual proxy.
- C. B. Zilles, J. K. Salisbury, "A constraint-based god-object method for haptic display," *IROS 1995*, vol. 3, pp. 146–151. DOI 10.1109/IROS.1995.525876.
- K. J. Kuchenbecker, J. Fiene, G. Niemeyer, "Improving contact realism through event-based haptic feedback," *IEEE TVCG* 12(2):219–230, 2006. DOI 10.1109/TVCG.2006.32; the user study cited here is the conference version, "Event-based haptics and acceleration matching," *WHC 2005*, pp. 381–387. DOI 10.1109/WHC.2005.52.
- P. Richard, M. R. Cutkosky, "Friction modeling and display in haptic applications involving user performance," *ICRA 2002*, pp. 605–611. DOI 10.1109/ROBOT.2002.1013425.
- D. Karnopp, "Computer simulation of stick-slip friction in mechanical dynamic systems," *J. Dyn. Sys. Meas. Control* 107(1):100–103, 1985. DOI 10.1115/1.3140698.
- P. Dupont, B. Armstrong, V. Hayward, "Elasto-plastic friction model: contact compliance and stiction," *ACC 2000*, pp. 1072–1077. DOI 10.1109/ACC.2000.876665. V. Hayward, B. Armstrong, "A new computational model of friction applied to haptic rendering," *Experimental Robotics VI*, LNCIS 250, pp. 403–412, 2000. DOI 10.1007/BFb0119418.
- M. Minsky, M. Ouh-young, O. Steele, F. P. Brooks, M. Behensky, "Feeling and seeing: issues in force display," *I3D 1990*, pp. 235–241. DOI 10.1145/91385.91451.
- G. Robles-De-La-Torre, V. Hayward, "Force can overcome object geometry in the perception of shape through active touch," *Nature* 412:445–448, 2001. DOI 10.1038/35086588.
- F. Ryden, H. J. Chizeck, "A proxy method for real-time 3-DOF haptic rendering of streaming point cloud data," *IEEE Transactions on Haptics* 6(3):257–267, 2013. DOI 10.1109/TOH.2013.20.
- M. A. Srinivasan, C. Basdogan, "Haptics in virtual environments: taxonomy, research status, and challenges," *Computers & Graphics* 21(4):393–404, 1997. DOI 10.1016/S0097-8493(97)00030-7.
- K. S. Hale, K. M. Stanney, "Deriving haptic design guidelines from human physiological, psychophysical, and neurological foundations," *IEEE CG&A* 24(2):33–39, 2004. DOI 10.1109/MCG.2004.1274059.
- W.-C. Wu, C. Basdogan, M. A. Srinivasan, "Visual, haptic, and bimodal perception of size and stiffness in virtual environments," *ASME IMECE 1999*, DSC. DOI 10.1115/IMECE1999-0003.
- A. M. Okamura, M. R. Cutkosky, J. T. Dennerlein, "Reality-based models for vibration feedback in virtual environments," *IEEE/ASME Transactions on Mechatronics* 6(3):245–252, 2001. DOI 10.1109/3516.951362.
- Y. Ding, S. Hasegawa, EuroHaptics 2020, LNCS 12272. DOI 10.1007/978-3-030-58147-3_27.
- M. Galvan, C. Ramirez, A. D. Deshpande, A. M. Fey, WHC 2023, pp. 176–182. DOI 10.1109/WHC56415.2023.10224434.
