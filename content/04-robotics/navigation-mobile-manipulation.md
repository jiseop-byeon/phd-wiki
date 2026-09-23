---
title: 16. Navigation & Mobile Manipulation
tags: [robotics, navigation, mobile-manipulation]
study-depth: Working
wiki-support: Working
depth-goal: "Say what a mobile manipulator's navigation goal actually is, choose a base pose defensibly, and read a mobile-manipulation paper's error budget."
mastery-when: "The research program keeps this at Working — it is a supporting pillar, and integration rather than novelty is what it contributes."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to integrate, diagnose and evaluate. The
> [[07-research-program/index|research program]] deliberately does *not* promote this to
> Mastery: new SLAM is not the contribution.
> **Working** — 통합하고, 진단하고, 평가할 만큼. [[07-research-program/index|연구 프로그램]]은
> 의도적으로 이것을 Mastery로 올리지 *않는다*: 새 SLAM은 기여가 아니다.

> [!note] Prerequisites · 선수 지식
> You need localization and mapping ([[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]]), configuration space and planning ([[04-robotics/planning-decision-making|4. Planning & Decision-Making]]), the manipulability ellipsoid ([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]) — which turns out to be the quantity that decides where a base should stop — the pseudo-inverse and the null space of a wide Jacobian ([[02-foundations/linear-algebra|1. Linear Algebra §4.5]]), and hand–eye calibration, the camera-to-gripper transform whose error enters §4's budget ([[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration §5]]).
> 위치 추정과 지도 작성([[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]]), 자세 공간과 계획([[04-robotics/planning-decision-making|4. 계획·의사결정]]), 가조작성 타원체([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]]; 베이스를 어디에 세울지를 결정하는 양이 결국 그것이다), 넓은 야코비안의 유사역행렬과 영공간([[02-foundations/linear-algebra|1. 선형대수 §4.5]]), 그리고 §4의 예산에 오차로 들어가는 카메라–그리퍼 변환을 정하는 손–눈 보정([[04-robotics/geometric-perception-calibration|3.5 기하 인식·보정 §5]])이 필요하다.

## English

*Group H. Stands on the [[04-robotics/modern-robotics/index|MR chapters]], [[04-robotics/state-estimation-slam|3. State Estimation]] and [[04-robotics/planning-decision-making|4. Planning]].
The goal is not a point on a map but a configuration the arm can work from, and that one sentence is the whole page.*

*Scope: this page teaches where a mobile base should stop and why — the reachable workspace and manipulability as placement criteria (§2–§3), the whole-body/decoupled architecture choice (§4.5), and the error budget that decides whether an open-loop design can close (§4). It does not teach SLAM or localization, which is [[04-robotics/state-estimation-slam|3. State Estimation]]; the planners that drive the base there, which are [[04-robotics/planning-decision-making|4. Planning]]; or what the arm does once it arrives, which is [[04-robotics/grasping|15. Grasping]] and [[04-robotics/force-compliance-control|13. Force & Compliance Control]].*

> [!note] First pass · 처음이라면
> Read the picture, then §1 (the goal is a configuration, not a point), §2 (reachability and the two manipulability measures), §3 (base placement), §4 (the error budget) and §4.5 (whole-body or decoupled). Then the Worked case, which sits after §4.5 and puts §2–§4 together on P2, and §6's reading table. §5 (localizing on a site that keeps changing) is second-pass; §4 is also the section to return to when a system misses by centimetres and nobody can say which stage owns it.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 436" style="max-width:100%;height:auto" role="img" aria-label="Graph paper at 0.25 m per square: the panel at (2, 1) with its horizontal surface normal, three circles about the panel (r = 2 m, the r = 1.414 m ring and the shaded 1.311 to 1.511 m band), P2 at its frozen pose from a base at (1, 0), and a 10 cm disc of base uncertainty exactly as wide as the band.">
  <defs><marker id="aNAV" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <path d="M36 24 V384 M36 24 H396 M56 24 V384 M36 44 H396 M76 24 V384 M36 64 H396 M96 24 V384 M36 84 H396 M116 24 V384 M36 104 H396 M136 24 V384 M36 124 H396 M156 24 V384 M36 144 H396 M176 24 V384 M36 164 H396 M196 24 V384 M36 184 H396 M216 24 V384 M36 204 H396 M236 24 V384 M36 224 H396 M256 24 V384 M36 244 H396 M276 24 V384 M36 264 H396 M296 24 V384 M36 284 H396 M316 24 V384 M36 304 H396 M336 24 V384 M36 324 H396 M356 24 V384 M36 344 H396 M376 24 V384 M36 364 H396 M396 24 V384 M36 384 H396" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.14" fill="none"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#aNAV)">
    <line x1="36" y1="284" x2="400" y2="284"/>
    <line x1="56" y1="384" x2="56" y2="20"/>
  </g>
  <g stroke="currentColor" stroke-width="1">
    <line x1="136" y1="281" x2="136" y2="287"/>
    <line x1="216" y1="281" x2="216" y2="287"/>
    <line x1="296" y1="281" x2="296" y2="287"/>
    <line x1="376" y1="281" x2="376" y2="287"/>
    <line x1="53" y1="364" x2="59" y2="364"/>
    <line x1="53" y1="204" x2="59" y2="204"/>
    <line x1="53" y1="124" x2="59" y2="124"/>
    <line x1="53" y1="44" x2="59" y2="44"/>
  </g>
  <path d="M95.1 204 a120.9 120.9 0 1 0 241.7 0 a120.9 120.9 0 1 0 -241.7 0 Z M111.1 204 a104.9 104.9 0 1 0 209.7 0 a104.9 104.9 0 1 0 -209.7 0 Z" fill="currentColor" fill-opacity="0.30" fill-rule="evenodd"/>
  <path d="M102.9 204 a113.1 113.1 0 1 0 226.3 0 a113.1 113.1 0 1 0 -226.3 0 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
  <path d="M56 204 a160 160 0 1 0 320 0 a160 160 0 1 0 -320 0 Z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <line x1="216" y1="180" x2="216" y2="228" stroke="currentColor" stroke-width="4" stroke-opacity="0.75"/>
  <line x1="176" y1="204" x2="265.6" y2="204" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3" marker-end="url(#aNAV)"/>
  <polyline points="136,284 216,284 216,204" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
  <circle cx="216" cy="284" r="3.4" fill="currentColor"/>
  <circle cx="216" cy="204" r="3.4" fill="currentColor"/>
  <circle cx="136" cy="284" r="8" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"/>
  <rect x="132.5" y="280.5" width="7" height="7" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6" fill="none">
    <polyline points="345.4,110 398,92"/>
    <polyline points="324.8,172.8 398,146"/>
    <polyline points="327.8,219.7 398,200"/>
    <polyline points="265.6,204 398,246"/>
  </g>
  <circle cx="345.4" cy="110" r="2" fill="currentColor"/>
  <circle cx="324.8" cy="172.8" r="2" fill="currentColor"/>
  <circle cx="327.8" cy="219.7" r="2" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="404" y="40" opacity="0.85">one square = 0.25 m</text>
    <text x="404" y="96">r = 2 m: arm straight,</text>
    <text x="404" y="110">det J = 0</text>
    <text x="404" y="150">r = √2 = 1.414 m:</text>
    <text x="404" y="164">w largest</text>
    <text x="404" y="204">w ≥ 0.99: r = 1.311–1.511 m,</text>
    <text x="404" y="218">a band 20 cm wide</text>
    <text x="404" y="250">panel normal:</text>
    <text x="404" y="264">the push direction</text>
    <text x="404" y="330" opacity="0.85">inner circle: radius</text>
    <text x="404" y="344" opacity="0.85">|L<tspan dy="3.5">1</tspan><tspan dy="-3.5"> − L</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">| = 0 for P2, so none</tspan></text>
    <text x="208" y="194" text-anchor="end">panel (2, 1) = tip</text>
    <text x="223" y="278">elbow (2, 0)</text>
    <text x="124" y="306" text-anchor="end">base (1, 0)</text>
    <text x="124" y="320" text-anchor="end" opacity="0.85">2σ disc</text>
    <text x="124" y="334" text-anchor="end" opacity="0.85">r = 10 cm</text>
    <text x="400" y="314" text-anchor="end">x (m)</text>
    <text x="64" y="30">y (m)</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8">
    <text x="51" y="297" text-anchor="end">0</text>
    <text x="136" y="298" text-anchor="middle">1</text>
    <text x="216" y="298" text-anchor="middle">2</text>
    <text x="296" y="298" text-anchor="middle">3</text>
    <text x="376" y="298" text-anchor="middle">4</text>
    <text x="50" y="367.5" text-anchor="end">−1</text>
    <text x="50" y="207.5" text-anchor="end">1</text>
    <text x="50" y="127.5" text-anchor="end">2</text>
    <text x="50" y="47.5" text-anchor="end">3</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="12" y="409">The band is narrower than one square, and the base's 2σ disc is exactly as wide as the band:</text>
    <text x="12" y="423">a base commanded to the ring's centre can, at two sigma, be anywhere across it.</text>
  </g>
</svg>

**P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] (unit links, $L_1=L_2=1$ m) on a holonomic base, drawn at $0.25$ m per square, with the panel at world $(2,1)$ m and its surface normal, the push direction. About the panel, not the base: the outer circle $r=2$ m where the arm is straight and $\det J=0$, the ring $r=\sqrt2=1.414$ m where $w$ is largest, and the shaded $w\ge0.99$ band from $1.311$ to $1.511$ m, only $20$ cm wide, with no inner circle because $|L_1-L_2|=0$ for P2. The base at $(1,0)$ puts the tip on the panel at the frozen pose, elbow at $(2,0)$, and its $2\sigma$ localization disc of radius $10$ cm is exactly as wide as the band.

### 1. The goal is a pose, not a point

A navigation stack built for a delivery robot answers "get to this location". A mobile
manipulator needs a different answer: **get to a configuration from which the arm can do the
task**. Those come apart immediately. A base one metre from the wall may put the target
outside the arm's reach; a base flush against it may put the arm at the edge of its
workspace where the manipulability ellipsoid has collapsed
([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]) and it can barely
move in the direction the task needs.

**On P2, in numbers.** Put the panel at $(2,1)$ m, as in the picture. "Reach the panel" is satisfied by any base within $2$ m of it, a disc of $12.6\ \mathrm{m}^2$. The tip-to-base distance $r$ fixes the elbow, $\cos\theta_2=(r^2-2)/2$, and with it the manipulability $w=\lvert\sin\theta_2\rvert$ of §2: a base parked at $r=1.9$ m reaches the panel with $w=0.59$, and one at $r=2.0$ m reaches it with the arm straight and $w=0$, a singular arm that can push hard along the forearm and cannot move along it. The band where $w\ge0.99$, from $1.311$ to $1.511$ m, covers $1.77\ \mathrm{m}^2$, only $14\%$ of the disc, and the picture's $2\sigma$ localization disc, of radius $10$ cm, is as wide as that band, which is the problem §4 budgets.

So the navigation goal is not a point on a map. It is a set of base poses from which the
whole task — not one waypoint, the whole reach — is comfortably executable, and computing
that set is the subject of §3.

This is also why the research program treats navigation as a supporting pillar. What it
must deliver is *arrival in a workable configuration*, repeatedly, on a site that changed
since yesterday. That is an integration problem with real difficulty and no need for a new
SLAM algorithm.

### 2. Reachability and capability

Start from the arm alone. For a fixed base, which end-effector poses are achievable, and
how well?

**Reachable workspace, defined.** With $f$ the forward kinematics and $\mathcal{C}_{\text{free}}$ the free configuration space ([[04-robotics/planning-decision-making|4. Planning §2]]), the reachable workspace is the image of the free space under $f$ — the set of end-effector poses attained by *some* admissible configuration:

$$\mathcal{W}_{R}=\{\,f(q)\ :\ q\in\mathcal{C}_{\text{free}}\,\}$$

It is an image and not a ball, so its shape is whatever the joint limits and the link lengths make it. Its subset the **dexterous workspace** keeps only the positions reachable at *every* orientation, and the gap between the two is the anisotropy this section is about. For **P2** ($L_1=L_2=1$ m) the reachable set is the annulus between $|L_1-L_2|=0$ and $L_1+L_2=2$ m, that is the closed disc of radius 2 m. **Non-example:** asking for P2's dexterous workspace is a category error, because a planar 2R spends both degrees of freedom on the tip *position* and has no orientation left to choose — dexterity is a question you may only ask of an arm with spare dof.

**Reachability map**: discretise the workspace into voxels and record, for each, whether the
end-effector can reach it — the discretised indicator of $\mathcal{W}_R$. **Capability map** (Zacharias, Borst and Hirzinger, IROS 2007)
goes further and records *from which directions*, summarising each voxel by a **reachability index**, the fraction of sampled approach orientations that are achievable there — because reaching a point from above and
reaching it from the side are different feasibility questions, and an arm's workspace is
strongly anisotropic. Making that directional structure explicit and inspectable is the
contribution, and it is the direct ancestor of the inverse-reachability methods in §3 (reachability-based base placement itself goes back at least to Seraji 1995).

**Manipulability — "how well", made into a number.** Reachability is a yes/no; the quality of a reachable pose is a property of the Jacobian $J(q)$, whose ellipsoid is defined in [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR ch.5 §4]]. Two scalar summaries of that ellipsoid are the ones this page uses, and they answer different questions. Yoshikawa's measure is its volume, and the condition number is its distortion:

$$w(q)=\sqrt{\det\big(J J^{\top}\big)}=\lvert\det J\rvert\ \ (J\ \text{square}),\qquad \kappa(q)=\frac{\sigma_{\max}}{\sigma_{\min}}$$

$w$ falls to zero exactly at a singularity, since a collapsed ellipsoid has no volume, while $\kappa$ diverges there, because one singular value goes to zero while the largest does not. Both are properties of the **configuration**, not of the base pose — the base pose matters only because it decides which configuration the arm must adopt.

> [!example] Worked example · 계산 예제
> On **P2**, both quantities depend on the elbow angle $\theta_2$ *alone* and not on $\theta_1$, since changing $\theta_1$ only rotates the task frame. That is what turns a conditioning question into a *distance* question, because the tip-to-base distance $r=\sqrt{2+2\cos\theta_2}$ is also a function of $\theta_2$ alone — and a distance is a ring of base positions, which is §3.
>
> | $\theta_2$ | $r$ (m) | $w=\lvert\sin\theta_2\rvert$ | $\sigma_{\max},\sigma_{\min}$ | $\kappa$ |
> |---|---|---|---|---|
> | $90°$ | 1.414 | **1.000** | 1.618, 0.618 | 2.618 |
> | $131.81°$ | 0.816 | 0.745 | 1.098, 0.679 | **1.618** |
> | $5°$ | 1.998 | 0.087 | 2.234, 0.039 | 57.26 |
> | $0°$ | 2.000 | 0.000 | 2.236, 0 | $\infty$ |
>
> **The two measures disagree, and that is the point.** $w$ is largest at $\theta_2=90°$, the $r=\sqrt{2}$ band this page's figure and problem set use. But $\kappa$ is smallest at $\theta_2=\arccos(-\tfrac23)=131.81°$, where $r=\sqrt{2/3}=0.816$ m and $w$ has already fallen to $\sqrt5/3=0.745$. Maximising the ellipsoid's *volume* parks the base 1.41 m from the target; minimising its *distortion* parks it 0.82 m away. (The extremes are exact: $\kappa=\varphi^2$ at $90°$ and $\kappa=\varphi$ at $131.81°$, with $\varphi$ the golden ratio.)
>
> **Non-example — "the well-conditioned band" as a single number.** There is no such band until you say which measure you optimised. $w$ answers "can the arm move quickly in every direction", $\kappa$ answers "is it roughly as capable in one direction as another", and a contact task that pushes along one axis cares about neither in general — it cares about $\sigma$ *in the task direction*. Report the measure with the number, or the number means nothing.

### 3. Base placement — inverting the question

Given a task pose, where should the base stand? The standard answer is to **invert the
reachability map**: a forward map says "from this base pose, these targets are reachable";
inverting it gives a distribution over base poses from which a given target is reachable, so
you can sample and score candidates directly. That is Vahrenkamp, Asfour and Dillmann's
inverse-reachability formulation (ICRA 2013), and it is what the field cites for this
question.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="the set of valid base positions around a task target is an annulus, further cut by conditioning and by obstacles">
  <g fill="currentColor">
    <path d="M 196 116 m -94 0 a 94 94 0 1 0 188 0 a 94 94 0 1 0 -188 0 Z M 196 116 m -37 0 a 37 37 0 1 0 74 0 a 37 37 0 1 0 -74 0 Z" fill-rule="evenodd" fill-opacity="0.10"/>
    <path d="M 196 116 m -80 0 a 80 80 0 1 0 160 0 a 80 80 0 1 0 -160 0 Z M 196 116 m -51 0 a 51 51 0 1 0 102 0 a 51 51 0 1 0 -102 0 Z" fill-rule="evenodd" fill-opacity="0.22"/>
    <rect x="192" y="24" width="128" height="22" rx="2" fill-opacity="0.55"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <circle cx="196" cy="116" r="94"/><circle cx="196" cy="116" r="80"/><circle cx="196" cy="116" r="51"/><circle cx="196" cy="116" r="37"/>
  </g>
  <g fill="currentColor"><circle cx="196" cy="116" r="5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="204" y="113">task pose</text>
    <text x="330" y="40">obstacle: removes part of the set</text>
    <text x="330" y="96">outer ring: reachable but</text>
    <text x="330" y="110">poorly conditioned</text>
    <text x="330" y="136">shaded band: reachable AND</text>
    <text x="330" y="150">well conditioned &#8212; stand here</text>
    <text x="330" y="176">inner disc: too close, the arm</text>
    <text x="330" y="190">cannot fold that far</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="238">The valid set is an annulus, not a disc &#8212; and the useful part of it is narrower still. Every centimetre of</text>
    <text x="20" y="254">base-pose uncertainty eats into a band that was only a few tens of centimetres wide to begin with.</text>
  </g>
</svg>

Two practical points the figure is making:

- **Nearer is not better.** Too close and the arm cannot fold enough to reach; too far and it
  is extended and near-singular, and **loses controllable motion** in exactly the direction a contact task needs — note the duality: near a singularity the arm is *strong* along the collapsed direction (locked-knee mechanical advantage) and unable to move or modulate there, which is the [[04-robotics/modern-robotics/ch05-velocity-kinematics|force/velocity ellipsoid reciprocity of MR ch.5]]
  ([[02-foundations/manipulator-kinematics-dynamics|10. §6]] on why an extended arm is also
  effectively heavier).
- **The usable band is narrow**, so base-pose error is not a rounding error — it is a
  direct consumer of the margin.

> [!note] There is no survey of this · 이 주제에는 서베이가 없다
> No survey or systematic review of base placement for mobile manipulation is known, so do
> not cite one. The citable references are the primary methods —
> Zacharias et al. 2007 for capability maps, Vahrenkamp et al. 2013 for inverse
> reachability, and Makhal and Goins' Reuleaux (IRC 2018) for the open-source tooling.
> 모바일 조작의 base placement에 대한 서베이나 체계적 리뷰를 찾았으나 없었다. 없는 것을
> 인용하지 마라. 인용 가능한 것은 1차 방법들이다.

### 4. The error budget is where mobile manipulation actually differs

A fixed arm already has several sources of end-effector error — calibration, sensing,
compliance, and workpiece uncertainty. A mobile base adds localization, settling, and a
base-to-arm transform, so more uncertain transforms meet at the contact:

| Source | Typical scale | Notes |
|---|---|---|
| Base localization | centimetres | worse on a site than in a mapped building |
| Base mechanical settling | millimetres | tracks and soft ground move under load |
| Arm kinematic error | sub-millimetre to millimetres | plus deflection under load ([[01-canonical-papers/notes/8-construction/kindle-jaibot\|Kindle et al.]]) |
| Workpiece position | centimetres | the part is where someone put it |

Two consequences. First, **a centimetre-scale open-loop error budget does not support a
millimetre-tolerance claim** — such systems usually need tighter metrology, task-level
vision/contact feedback, or both. Second, the honest way to read a mobile
manipulation paper is to ask which of these four it measured and which it assumed away.

The reference treatment of why mobility and manipulation do not simply concatenate is
Brock, Park and Toussaint's *Mobility and Manipulation* chapter in the *Springer Handbook of
Robotics* — whole-body control, redundancy resolution (both defined in §4.5 below), and the interaction between
navigation and manipulation constraints.

> [!warning] Another absence worth knowing
> A survey of mobile manipulation does exist: Thakar et al., "A Survey of Wheeled Mobile Manipulation: A Decision-Making Perspective," *ASME J. Mechanisms and Robotics* 15(2):020801, 2023. What is absent is a survey in the *Annual Review of Control,
> Robotics, and Autonomous Systems*, and none by the authors it is often attributed to. The
> Springer Handbook chapter (2016) remains the reference treatment despite its age. If you
> need something recent and are willing to accept a narrow scope, there is a 2025
> *Frontiers in Robotics and AI* mini-review scoped to **variable autonomy** in hazardous
> domains — which is a different subject wearing a similar name.

> [!example] Worked example · 계산 예제
> **Adding up a mobile grasp.** As a first-order illustration, treat the listed errors as
> independent, zero-mean scalar uncertainties and add their standard deviations in
> quadrature. (Correlated errors, bias, orientation error, and non-Gaussian tails require a
> covariance propagation or empirical task-space distribution.) Take a
> representative budget at the moment the gripper closes: base localization $\sigma = 5$ cm,
> base-to-arm mount 0.3 cm, arm kinematics and joint encoders 0.3 cm, hand–eye extrinsics
> (the camera-to-gripper transform that hand–eye calibration estimates from $AX=XB$,
> [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration §5]]) 1.0 cm,
> object pose from perception 1.0 cm.
>
> $\sigma_{\text{total}} = \sqrt{5.0^2 + 0.3^2 + 0.3^2 + 1.0^2 + 1.0^2} = \sqrt{27.18} = \mathbf{5.2}$ cm.
>
> A parallel jaw opening 60 mm onto a 40 mm object has only about $\pm 10$ mm of lateral
> geometric clearance. A $5.2$ cm **one-standard-deviation** budget is far larger than that
> clearance, so this open-loop design would have a high failure risk; the calculation alone
> is not a deterministic success/failure proof.
>
> Now look at where it went. Base localization contributes $25/27.18 = \mathbf{92\%}$ of the
> *variance*. Halving the arm's calibration error changes $\sigma_{\text{total}}$ from 5.213 cm
> to 5.207 cm — nothing. Drop the base term instead, by re-observing the object from the wrist
> camera once the base has parked, and you are left with
> $\sqrt{0.3^2 + 0.3^2 + 1.0^2 + 1.0^2} = 1.5$ cm, now dominated by hand–eye and perception error.
>
> **The reading this gives you.** This single calculation is why mobile manipulation is
> organized the way it is: the base is not required to be accurate, it is required to get the
> object into a sensor's view accurately enough for the next sensing stage, after which the arm
> closes the loop locally. A paper reporting a
> mobile-manipulation success rate without saying whether it re-observes at the goal has not
> told you which of these two systems it built.

### 4.5 Whole-body or decoupled — and how to tell

The error budget above assumed the base parks and the arm then works. That is one of two
architectures, and the vocabulary for the choice is worth stating exactly, because papers use
the words loosely.

**Decoupled** (also *navigate-then-manipulate*, or *sequential*): the base is commanded to a
pose, stops, and the arm is then commanded with the base held fixed. Two problems, solved one
after the other, each with its own state and its own controller.

**Whole-body**: base and arm are treated as one kinematic chain of $n=n_b+n_a$ degrees of
freedom, and one task Jacobian maps every one of them to end-effector motion, so base motion
and joint motion are alternative ways of serving the same task error:

$$\dot x=J\dot q=\begin{pmatrix}J_b & J_a\end{pmatrix}\begin{pmatrix}\dot q_b\\ \dot q_a\end{pmatrix},\qquad \dot q=J^{+}\dot x+\big(I-J^{+}J\big)\dot q_0$$

Here $J^{+}$ is the pseudo-inverse, which for a wide $J$ with independent rows returns the smallest $\dot q$ that achieves $\dot x$ ([[02-foundations/linear-algebra|1. Linear Algebra §4.5]]). The first term achieves the task; the second lies in the **null space** of $J$, so it changes
the configuration without moving the end-effector at all, which is where secondary objectives
go — manipulability, joint limits, obstacle distance. Choosing $\dot q_0$ is **redundancy
resolution**. Three conditions define whole-body control and all three are required: one state
vector spanning base and arm, one task specification that either may serve, and commands issued
to both inside the same control cycle. Drop any one and the system is decoupled.

**Counting the freedom on P2.** Task: tip position in the plane, so $m=2$.

| Architecture | $n_b$ | $n_a$ | $n$ | null-space dim $n-m$ |
|---|---|---|---|---|
| Whole-body, holonomic base | 3 | 2 | 5 | **3** |
| Whole-body, nonholonomic base (instantaneous) | 2 | 2 | 4 | 2 |
| Decoupled, base parked | 0 | 2 | 2 | **0** |

Those two bold numbers are the whole argument of this page in a different notation. Whole-body
leaves three directions of self-motion that cost the task nothing, so the controller can keep
itself out of the flattened region of §2 *while* the tip holds still. Decoupled leaves none:
whatever conditioning the base handed the arm is what the task gets, permanently, which is
exactly why §3 spends so much effort on where to stop. A nonholonomic base does not contribute
3 at the velocity level, because an instantaneous sideways motion is unavailable
([[04-robotics/planning-decision-making|4. Planning §5.5]]).

**The null space, worked on P2.** Mount P2's shoulder at the centre of a holonomic base parked at world $(1,0)$ with heading $\varphi=0$, the arm at its frozen $\theta=(0°,90°)$, so the elbow is at $(2,0)$ and the tip on the panel at $(2,1)$, and order the five rates as $\dot q=(\dot x_b,\ \dot y_b,\ \dot\varphi,\ \dot\theta_1,\ \dot\theta_2)$. A base translation carries the tip one-for-one, a base rotation swings it about the shoulder exactly as $\dot\theta_1$ does, and the last two columns are P2's own $J$ at that pose, so

$$J=\begin{pmatrix}1&0&-1&-1&-1\\0&1&1&1&0\end{pmatrix},\qquad J^{+}=J^{\top}\big(JJ^{\top}\big)^{-1}=\frac18\begin{pmatrix}3&2\\2&4\\-1&2\\-1&2\\-3&-2\end{pmatrix}$$

because $JJ^{\top}=\begin{pmatrix}4&-2\\-2&3\end{pmatrix}$ has determinant $8$ and inverse $\tfrac18\begin{pmatrix}3&2\\2&4\end{pmatrix}$. The null-space projector is then

$$I-J^{+}J=\frac18\begin{pmatrix}5&-2&1&1&3\\-2&4&-2&-2&2\\1&-2&5&-3&-1\\1&-2&-3&5&-1\\3&2&-1&-1&5\end{pmatrix}$$

of rank $3$, the first row of the table above. Three self-motions it keeps can be read straight off $J$, and each gives $Jn=0$: $(0,0,1,-1,0)$ turns the base one way and the shoulder the other; $(1,0,0,0,1)$ drives the base $+x$ while the elbow swings the tip back by the same amount; $(1,-1,1,0,0)$ translates the base diagonally while turning it so the tip stays put. Now ask the tip to slide along the panel face at $0.2$ m/s, $\dot x=(0,\ 0.2)$:

| choice | $\dot q=(\dot x_b,\ \dot y_b,\ \dot\varphi,\ \dot\theta_1,\ \dot\theta_2)$ | $\lVert\dot q\rVert$ | what it does |
|---|---|---:|---|
| decoupled, base parked: $J_a^{-1}\dot x$ | $(0,\ 0,\ 0,\ 0.2,\ -0.2)$ | $0.283$ | shoulder and elbow both turn, and the elbow walks away from the $90°$ that §3 parked it at |
| whole-body, $\dot q_0=0$: $J^{+}\dot x$ | $(0.05,\ 0.1,\ 0.05,\ 0.05,\ -0.05)$ | $0.141$ | the minimum-norm share: all five move a little, the elbow at a quarter of the decoupled rate |
| whole-body, $\dot q_0=(0,\ 0.2,\ 0,\ 0,\ 0)$, "let the base carry it" | $(0,\ 0.2,\ 0,\ 0,\ 0)$ | $0.200$ | the arm freezes at $w=1$ and the base drives along the panel |

In the last row the projection adds $(I-J^{+}J)\dot q_0=(-0.05,\ 0.1,\ -0.05,\ -0.05,\ 0.05)$ to the minimum-norm share, and $J$ times that vector is exactly $(0,0)$: it reshapes the motion without moving the tip. That is what a secondary objective is, in numbers — the arm holds the best-conditioned elbow angle while the task is served in full, which the decoupled row, with a null space of dimension $0$, cannot do. One caveat the formula hides: the pseudo-inverse's "smallest" weighs metres per second and radians per second equally, which is harmless for P2's $1$ m links and a choice, not a fact, for any other arm; a weighted pseudo-inverse moves the split.

**Non-example.** Commanding base velocity and arm velocity in the same message is not
whole-body control. If the base command comes from a path follower and the arm from an IK
solved against the base's *estimated* pose, the two are still decoupled — they merely overlap
in time. What makes it whole-body is the single Jacobian in which base motion can absorb task
error.

*Why it matters.* §6's table asks which one a paper built. The answer decides whether base-pose
error is a disturbance the arm must absorb after the fact (decoupled, so it enters the §4
budget in full) or a coordinate the controller is still allowed to use (whole-body, so it can
be corrected while the task runs).

### Worked case · 대상으로 한 번 끝까지

§2 said where the arm is well conditioned, §3 turned that into a ring of base positions, and §4
gave the base's own error. Put the three together on **P2** and this page's central claim — *the
usable band is narrow, so base-pose error is not a rounding error* — becomes a number you can
check.

**1. The band, in metres.** On P2 the Yoshikawa measure is
$w=\lvert\det J\rvert=\lvert\sin\theta_2\rvert$ and the tip-to-base distance is
$r=\sqrt{2+2\cos\theta_2}=2\lvert\cos(\theta_2/2)\rvert$, both functions of the elbow angle alone
(§2). So "keep $w\ge w_0$" is an interval of elbow angles,
$\theta_2\in[\arcsin w_0,\ 180°-\arcsin w_0]$, and $r$ carries it to an interval of distances.
Write $c=\sqrt{1-w_0^2}$ for the cosine at either end; the two radii are $\sqrt{2+2c}$ and
$\sqrt{2-2c}$, and their difference squares to $(2+2c)+(2-2c)-2\sqrt{4-4c^2}=4-4w_0$, since the
cross term is $2\sqrt{4-4c^2}$ and $\sqrt{1-c^2}=w_0$. So the band's width is

$$\Delta r=2\sqrt{1-w_0}$$

and it closes as the square root of how much manipulability you insist on. Two thresholds, both
bands centred in elbow angle on $90°$, the $r=\sqrt2=1.414$ m ring of §2's table:

| $w_0$ | elbow interval | $r$ range (m) | band width $\Delta r$ (m) |
|---|---|---|---:|
| $0.90$ | $64.16°$–$115.84°$ | $1.062$–$1.695$ | $0.632$ |
| $0.99$ | $81.89°$–$98.11°$ | $1.311$–$1.511$ | $0.200$ |

**2. The band against the base's own error.** §4's budget puts base localization at $\sigma=5$ cm,
so a $\pm2\sigma$ interval is $20$ cm across — the entire $w\ge0.99$ band, and a third of the looser
$w\ge0.90$ band. A base commanded to the centre of the tight band is therefore, at two sigma,
anywhere between its two edges: §3's placement computation has returned a nominal pose whose
uncertainty is the size of the answer. That is the figure caption in §3 turned into arithmetic.

**3. Where the fix has to happen.** Base localization is $25/27.18=92\%$ of §4's variance, so
nothing done to the arm moves this number. Re-observe the target from the wrist camera once the
base has parked and the remaining budget is $1.5$ cm — $1.476$ cm before rounding, so its
$\pm2\sigma$ interval spans $4\times1.476=5.9$ cm — comfortably inside the $20$ cm band, with room
left for the workpiece. The conditioning requirement
did not change; what changed is which sensor measured the last transform.

**The reading this gives you.** A paper that states a base-placement criterion without stating the
base's pose uncertainty has given you one of the two numbers this section multiplied. A paper that
calls a placement "well conditioned" without naming $w_0$ has not given you even the first: the
same arm is a $63$ cm band at one threshold and a $20$ cm band at another.

### 5. Localizing on a site that keeps changing

Construction breaks the assumption most localization systems rest on: that the map is
static. The building is the workpiece, so yesterday's map is wrong by construction — and
the parts that changed are the parts you are working on.

Three responses appear in the literature:

- **An external measurement device.** Ercan et al. (ISARC 2019) localize a mobile
  construction robot with a robotic total station, so end-effector accuracy survives
  repeated base repositioning. Validated in a large-scale outdoor experiment. This is the
  pragmatic answer and it comes from the same lab lineage as the In situ Fabricator.
- **Anchoring to a reference model.** SLAM2REF (Vega-Torres, Braun and Borrmann,
  *Construction Robotics*, 2024) registers LiDAR-inertial sessions against an existing
  BIM or reference point cloud, giving drift-free poses and map extension across repeat
  visits. Evaluated on the ConSLAM real-site dataset rather than in a live robot trial.
- **Accepting drift and closing the loop at the task.** If the contact stage can correct
  centimetres, localization only has to get you into the band of §3.

**How much drift the band tolerates.** The $w\ge0.99$ band of §3 is $20$ cm wide, so a base aimed at its middle may land up to $10$ cm off in range and keep $w\ge0.99$. With the $\sigma=5$ cm localization of §4's budget that half-width is $2\sigma$, and the base lands inside it with probability $\mathrm{erf}(2/\sqrt2)=0.954$. Drift is what accumulates between re-anchorings, and it has to be judged against those $10$ cm, not against zero: at an assumed odometry drift of $1\%$ of distance travelled, a $30$ m approach accumulates $30$ cm, three times the half-width. A changing site does something else: it makes yesterday's map wrong, so the map cannot be the anchor. That is why the responses above re-anchor instead of trusting the map, the first two to an external reference (the total station's measurements, or a BIM model or earlier point cloud) and the third to the part itself at the task.

For the landscape, Yarovoi and Cho's 2024 review of SLAM for construction robotics
(*Automation in Construction*) is the survey that does exist here.

### 6. Reading a mobile-manipulation paper

| Question | What a vague answer hides |
|---|---|
| Was the base **repositioned** between trials, or placed once? | Placing once removes the hardest error source |
| How was the base pose measured — and by what, that the robot did not have? | External tracking makes a result a lower bound on difficulty |
| Is the task tolerance stated, and does the error budget close? | Without both, "successful" is undefined |
| Static map or changing environment? | The construction case is the second |
| Whole-body control (base and arm commanded jointly), or navigate-then-manipulate (base move, then a separate arm move)? | Sequential is easier and far more common than the phrasing suggests |
| Benchmark: simulation, real, or both? | HomeRobot ships both; BEHAVIOR-1K is simulation only |

### After reading

- [ ] State the navigation goal for a mobile manipulator in one sentence.
- [ ] Explain why the valid base region is an annulus and why its useful part is narrower.
- [ ] List the four error sources and say which one construction makes worst.
- [ ] Name two ways to localize on a site whose map keeps changing.
- [ ] Say what does not exist in this literature, so you do not cite it.

> [!tip] Going deeper · 더 깊이
> The nearest thing to a textbook here is a handbook chapter: Brock, Park & Toussaint, "Mobility and Manipulation," ch.40 of the *Springer Handbook of Robotics* (2nd ed., 2016). Read it for the framing, then the two papers that made base placement computable — Zacharias et al. (IROS 2007) for the capability map and Vahrenkamp et al. (ICRA 2013) for inverting reachability into a placement. What no source covers is §4: the error budget is systems folklore, which is why this page computes one rather than citing one.

### Self-check

1. A team parks the base as close to the wall as possible "to maximise reach". What is wrong?
2. The task needs 2 mm placement accuracy. Your base localizes to ±3 cm. What follows?
3. Why is a static-map SLAM benchmark a poor predictor of construction-site performance?
4. A paper reports 95% success on a mobile manipulation task, with base poses recorded by an
   external motion-capture system. What does the number mean?
5. You want to cite a survey of base placement. What do you do?

> [!tip]- Answers
> 1. Reach is not the binding constraint; conditioning is. Flush against the wall the arm is folded or extended near the edge of its workspace, where the manipulability ellipsoid has flattened, so the arm cannot move or modulate precisely in some direction — often the very direction the task pushes. (It is *strong* in that direction; what it has lost is controllable motion.) The right target is the shaded band of §3, not the outer limit of reach.
> 2. That open-loop execution cannot meet the tolerance — a ±3 cm base error alone is fifteen times the requirement, before the arm and the workpiece contribute. Something must close the loop at the task: **visual servoing** — driving the arm from the camera's live view of a feature rather than from its estimated pose — or a compliant contact stage that finds the feature mechanically ([[04-robotics/force-compliance-control|13. §5]]). This is not a weakness to apologise for; it is the design.
> 3. Because it measures the wrong difficulty. A static map benchmark rewards accurate registration to a scene that stays put, while a construction site changes *because the robot and the trades are changing it*, and the changed regions are exactly the work areas. A system that scores well on the first can drift badly on the second.
> 4. That the *manipulation* worked given accurate base poses. External motion capture supplies a pose the robot would not have on a site, so the result is a lower bound on the real difficulty — the navigation and localization contribution has been measured out of the experiment. It is a legitimate way to isolate a manipulation claim, as long as the paper says so and you read it that way.
> 5. Cite the primary methods instead — Zacharias et al. 2007 for capability maps and Vahrenkamp et al. 2013 for inverse reachability — because no such survey was found to exist. Writing "no survey of this exists; the primary references are…" is accurate and shows you looked.

### Problem set · 과제

Tier B. Using **P2** from [[02-foundations/lab-plants|0.6]] on a holonomic base. Panel at world $(2,1)\,\mathrm{m}$. Frozen pose: tip at $(1,1)$ relative to the base, $\det J=1$. No new simulator.

1. **Draw.** The picture above for an arm with the same $2$ m reach but unequal links, $L_1=1.2$ m and $L_2=0.8$ m, on the same holonomic base, panel at world $(2,1)$: the circles about the panel — outer, best-conditioned and inner — the band where $w\ge0.99\,w_{\max}$ to scale, and the base that puts the tip on the panel at $\theta=(0^\circ,90^\circ)$, with its two links. What appears that P2's picture did not have?
2. **Derive.** (a) Base position for the frozen pose. (b) Tip-to-base distance $r=\sqrt{2+2\cos\theta_2}$. Values at $\theta_2=90^\circ$, $5^\circ$, $0^\circ$. (c) $\det J=L_1 L_2\sin\theta_2$ at those three angles.
3. **Interpret.** A team parks "as close as possible" so the arm is fully extended toward the panel. What have they maximised, and what have they lost in the direction the panel-push needs?

> [!note]- How to draw it · 그리는 법
> - Axes at the world origin, one grid square to $0.25$ m, and the panel at $(2,1)$ with its surface normal drawn through it: the normal is the direction the tool will push, which §3's argument is about.
> - Circles about the panel, not about the base: this is §3's inversion, and drawing them the other way round is the usual mistake.
> - About $(2,1)$, the outer circle $r=L_1+L_2=2$ m, where the arm is straight and $\det J=0$, then the ring $r=\sqrt{L_1^2+L_2^2}=1.442$ m, where $w=L_1L_2|\sin\theta_2|$ reaches $w_{\max}=0.96$.
> - The inner circle, which P2 did not have: $r=|L_1-L_2|=0.4$ m. A base inside it cannot reach the panel at all, because the arm cannot fold its tip closer to its base than that.
> - The band where $w\ge0.99\,w_{\max}$, that is $|\sin\theta_2|\ge0.99$ or $\cos\theta_2=\pm0.141$, shaded to scale: $1.345$ to $1.533$ m, $18.8$ cm wide, under one grid square.
> - The base for $\theta=(0^\circ,90^\circ)$: the tip sits at $(1.2,\ 0.8)$ from the base, so the base is at $(2,1)-(1.2,0.8)=(0.8,\ 0.2)$. Draw its two links to the elbow and the tip, and check that it lies on the $1.442$ m ring.
> - Centred on that base, the $10$ cm-radius circle of §4's two-sigma base localization: $20$ cm across, now slightly wider than the $18.8$ cm band.

> [!tip]- Solutions
> 1. Outer circle $r=L_1+L_2=2$ m, singular as before. The new element is the inner circle $r=|L_1-L_2|=0.4$ m: a base closer than that cannot reach the panel, because this arm cannot fold its tip nearer its base than $0.4$ m. $w=L_1L_2|\sin\theta_2|$ peaks at $\theta_2=90^\circ$ with $w_{\max}=0.96$, on the ring $r=\sqrt{L_1^2+L_2^2}=\sqrt{2.08}=1.442$ m; the band $w\ge0.99\,w_{\max}$ ($\cos\theta_2=\pm0.141$) runs from $1.345$ to $1.533$ m, $18.8$ cm wide against P2's $20$ cm. The base for $\theta=(0^\circ,90^\circ)$ is $(2,1)-(1.2,0.8)=(0.8,\ 0.2)$, on that ring, and its $20$ cm localization disc now slightly overfills the band.
> 2. (a) $(2,1)-(1,1)=(1,0)$. (b) $r(90^\circ)=\sqrt{2}$, $r(5^\circ)\approx 1.998$, $r(0^\circ)=2$. (c) $\det J=1$, $\sin 5^\circ\approx 0.087$, $0$.
> 3. They maximised reach and parked on the singular ring. $\det J\to 0$: the lost direction is along the arm, which is the panel normal if they stretched straight at it. The arm is *strong* along that direction and cannot *move* or modulate force through the motors. The useful set is the $\sqrt{2}$ band, not the outer limit.

### Sources

- F. Zacharias, C. Borst, G. Hirzinger, "Capturing robot workspace structure: representing robot capabilities," IROS 2007, pp. 3229–3236 — the capability map.
- N. Vahrenkamp, T. Asfour, R. Dillmann, "Robot placement based on reachability inversion," ICRA 2013, pp. 1970–1975 — the standard base-placement formulation.
- A. Makhal, A. K. Goins, "Reuleaux: Robot Base Placement by Reachability Analysis," IRC 2018, pp. 137–142 ([arXiv:1710.01328](https://arxiv.org/abs/1710.01328)) — the open-source tooling.
- O. Brock, J. Park, M. Toussaint, "Mobility and Manipulation," ch. 40 in *Springer Handbook of Robotics*, 2nd ed., pp. 1007–1036, 2016 — the reference treatment.
- S. Ercan, S. Meier, F. Gramazio, M. Kohler, "Automated Localization of a Mobile Construction Robot with an External Measurement Device," ISARC 2019, pp. 929–936.
- M. A. Vega-Torres, A. Braun, A. Borrmann, "SLAM2REF: advancing long-term mapping with 3D LiDAR and reference map integration," *Construction Robotics*, vol. 8, no. 2, art. 13, 2024 ([arXiv:2408.15948](https://arxiv.org/abs/2408.15948)).
- A. Yarovoi, Y. K. Cho, "Review of simultaneous localization and mapping (SLAM) for construction robotics applications," *Automation in Construction*, vol. 162, art. 105344, 2024.
- Benchmarks: S. Yenamandra et al., "HomeRobot: Open-Vocabulary Mobile Manipulation," CoRL 2023, PMLR vol. 229, pp. 1975–2011 — **simulation and real robot**. C. Li et al., "BEHAVIOR-1K," CoRL 2022, PMLR vol. 205, pp. 80–93 — **simulation only**.

**Within this wiki**

- [[04-robotics/state-estimation-slam|3. State Estimation, Localization & SLAM]] — the estimation machinery
- [[05-construction-robotics/site-perception|Site Perception, Scan-to-BIM & Inspection]] — the domain's perception layer
- [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA]] — demonstration collection for mobile manipulation

## 한국어

*H군이다. [[04-robotics/modern-robotics/index|MR 챕터 요약]]과 [[04-robotics/state-estimation-slam|3. 상태 추정]]·[[04-robotics/planning-decision-making|4. 계획]] 위에 선다.
목표는 지도 위의 점이 아니라 팔이 일할 수 있는 자세다 — 그 한 문장이 이 페이지의 전부다.*

*범위: 이 페이지는 이동 베이스가 어디에 서야 하고 왜 그런지를 가르친다 — 배치 기준으로서의 도달 작업 영역과 가조작성(§2–§3), 전신/분리 아키텍처 선택(§4.5), 그리고 개루프 설계가 성립하는지를 결정하는 오차 예산(§4). SLAM이나 위치 추정은 가르치지 않는다. 그것은 [[04-robotics/state-estimation-slam|3. 상태 추정]]이다. 베이스를 그곳까지 몰고 가는 플래너는 [[04-robotics/planning-decision-making|4. 계획]]이고, 도착한 뒤 팔이 하는 일은 [[04-robotics/grasping|15. 파지]]와 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]다.*

> [!note] 처음이라면 · First pass
> 그림을 먼저 보고, §1(목표는 점이 아니라 자세다), §2(도달성과 두 가조작성 척도), §3(base placement), §4(오차 예산), §4.5(전신인가 분리인가)를 읽어라. 그다음 §4.5 뒤에 있는 Worked case가 §2–§4를 P2 위에서 하나로 합치고, §6의 읽기 표로 끝낸다. §5(계속 변하는 현장에서 위치 잡기)는 두 번째 읽기에서 본다. §4는 시스템이 센티미터 단위로 빗나가는데 어느 단계 탓인지 아무도 못 말할 때 돌아오는 절이기도 하다.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 436" style="max-width:100%;height:auto" role="img" aria-label="한 칸 0.25 m 모눈종이: 수평 법선을 가진 (2, 1)의 패널, 패널을 중심으로 한 원 셋(r = 2 m, r = 1.414 m 고리, 1.311에서 1.511 m까지 칠한 띠), (1, 0)의 베이스에서 고정 자세를 취한 P2, 띠와 정확히 같은 폭인 반지름 10 cm의 베이스 불확실성 원.">
  <defs><marker id="aNAVk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <path d="M36 24 V384 M36 24 H396 M56 24 V384 M36 44 H396 M76 24 V384 M36 64 H396 M96 24 V384 M36 84 H396 M116 24 V384 M36 104 H396 M136 24 V384 M36 124 H396 M156 24 V384 M36 144 H396 M176 24 V384 M36 164 H396 M196 24 V384 M36 184 H396 M216 24 V384 M36 204 H396 M236 24 V384 M36 224 H396 M256 24 V384 M36 244 H396 M276 24 V384 M36 264 H396 M296 24 V384 M36 284 H396 M316 24 V384 M36 304 H396 M336 24 V384 M36 324 H396 M356 24 V384 M36 344 H396 M376 24 V384 M36 364 H396 M396 24 V384 M36 384 H396" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.14" fill="none"/>
  <g stroke="currentColor" stroke-width="1.1" fill="none" marker-end="url(#aNAVk)">
    <line x1="36" y1="284" x2="400" y2="284"/>
    <line x1="56" y1="384" x2="56" y2="20"/>
  </g>
  <g stroke="currentColor" stroke-width="1">
    <line x1="136" y1="281" x2="136" y2="287"/>
    <line x1="216" y1="281" x2="216" y2="287"/>
    <line x1="296" y1="281" x2="296" y2="287"/>
    <line x1="376" y1="281" x2="376" y2="287"/>
    <line x1="53" y1="364" x2="59" y2="364"/>
    <line x1="53" y1="204" x2="59" y2="204"/>
    <line x1="53" y1="124" x2="59" y2="124"/>
    <line x1="53" y1="44" x2="59" y2="44"/>
  </g>
  <path d="M95.1 204 a120.9 120.9 0 1 0 241.7 0 a120.9 120.9 0 1 0 -241.7 0 Z M111.1 204 a104.9 104.9 0 1 0 209.7 0 a104.9 104.9 0 1 0 -209.7 0 Z" fill="currentColor" fill-opacity="0.30" fill-rule="evenodd"/>
  <path d="M102.9 204 a113.1 113.1 0 1 0 226.3 0 a113.1 113.1 0 1 0 -226.3 0 Z" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
  <path d="M56 204 a160 160 0 1 0 320 0 a160 160 0 1 0 -320 0 Z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.8"/>
  <line x1="216" y1="180" x2="216" y2="228" stroke="currentColor" stroke-width="4" stroke-opacity="0.75"/>
  <line x1="176" y1="204" x2="265.6" y2="204" stroke="currentColor" stroke-width="1.3" stroke-dasharray="6 3" marker-end="url(#aNAVk)"/>
  <polyline points="136,284 216,284 216,204" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
  <circle cx="216" cy="284" r="3.4" fill="currentColor"/>
  <circle cx="216" cy="204" r="3.4" fill="currentColor"/>
  <circle cx="136" cy="284" r="8" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"/>
  <rect x="132.5" y="280.5" width="7" height="7" fill="currentColor"/>
  <g stroke="currentColor" stroke-width="0.8" stroke-opacity="0.6" fill="none">
    <polyline points="345.4,110 398,92"/>
    <polyline points="324.8,172.8 398,146"/>
    <polyline points="327.8,219.7 398,200"/>
    <polyline points="265.6,204 398,246"/>
  </g>
  <circle cx="345.4" cy="110" r="2" fill="currentColor"/>
  <circle cx="324.8" cy="172.8" r="2" fill="currentColor"/>
  <circle cx="327.8" cy="219.7" r="2" fill="currentColor"/>
  <g font-size="11" fill="currentColor">
    <text x="404" y="40" opacity="0.85">한 칸 = 0.25 m</text>
    <text x="404" y="96">r = 2 m: 팔을 곧게 편다,</text>
    <text x="404" y="110">det J = 0</text>
    <text x="404" y="150">r = √2 = 1.414 m:</text>
    <text x="404" y="164">w가 가장 크다</text>
    <text x="404" y="204">w ≥ 0.99: r = 1.311–1.511 m,</text>
    <text x="404" y="218">폭 20 cm의 띠</text>
    <text x="404" y="250">패널 법선:</text>
    <text x="404" y="264">도구가 미는 방향</text>
    <text x="404" y="330" opacity="0.85">안쪽 원: 반지름</text>
    <text x="404" y="344" opacity="0.85">P2는 |L<tspan dy="3.5">1</tspan><tspan dy="-3.5"> − L</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">| = 0, 곧 없음</tspan></text>
    <text x="208" y="194" text-anchor="end">패널 (2, 1) = 말단</text>
    <text x="223" y="278">엘보 (2, 0)</text>
    <text x="124" y="306" text-anchor="end">베이스 (1, 0)</text>
    <text x="124" y="320" text-anchor="end" opacity="0.85">2σ 원</text>
    <text x="124" y="334" text-anchor="end" opacity="0.85">r = 10 cm</text>
    <text x="400" y="314" text-anchor="end">x (m)</text>
    <text x="64" y="30">y (m)</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.8">
    <text x="51" y="297" text-anchor="end">0</text>
    <text x="136" y="298" text-anchor="middle">1</text>
    <text x="216" y="298" text-anchor="middle">2</text>
    <text x="296" y="298" text-anchor="middle">3</text>
    <text x="376" y="298" text-anchor="middle">4</text>
    <text x="50" y="367.5" text-anchor="end">−1</text>
    <text x="50" y="207.5" text-anchor="end">1</text>
    <text x="50" y="127.5" text-anchor="end">2</text>
    <text x="50" y="47.5" text-anchor="end">3</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="12" y="409">띠는 모눈 한 칸보다 좁고, 베이스의 2σ 원은 띠와 정확히 같은 폭이다.</text>
    <text x="12" y="423">고리 한가운데로 보낸 베이스는 2σ에서 띠의 어느 쪽 끝에든 있을 수 있다.</text>
  </g>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P2**($L_1=L_2=1$ m의 단위 링크)를 홀로노믹 베이스에 얹어 모눈 한 칸 $0.25$ m로 그린 것으로, 패널은 월드 $(2,1)$ m에 있고 그 법선이 미는 방향이다. 원은 베이스가 아니라 패널을 중심으로 그렸다. 팔이 곧게 펴져 $\det J=0$인 바깥 원 $r=2$ m, $w$가 가장 큰 고리 $r=\sqrt2=1.414$ m, 그리고 칠한 $w\ge0.99$ 띠 $1.311$–$1.511$ m는 폭이 $20$ cm뿐이며, P2는 $|L_1-L_2|=0$이라 안쪽 원이 없다. $(1,0)$의 베이스가 고정 자세로 말단을 패널에 올리고(엘보는 $(2,0)$), 그 베이스의 반지름 $10$ cm짜리 $2\sigma$ 위치 원은 띠와 정확히 같은 폭이다.

### 1. 목표는 점이 아니라 자세다

배송 로봇용으로 만든 내비게이션 스택은 "이 위치로 가라"에 답한다. 모바일 매니퓰레이터에는
다른 답이 필요하다: **팔이 그 작업을 할 수 있는 자세(configuration)로 가라.** 이 둘은 곧바로
갈라진다. 벽에서 1 m 떨어진 베이스는 대상을 팔의 도달 범위 밖에 둘 수 있고, 벽에 바짝 붙인
베이스는 팔을 작업 영역 가장자리에 두어 가조작성 타원체가 붕괴한
([[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]]) 자리에서 정작 작업이
필요로 하는 방향으로 거의 움직이지 못하게 만든다.

**P2에서, 숫자로.** 그림처럼 패널을 $(2,1)$ m에 두자. "패널에 닿는다"는 패널에서 $2$ m 안의 어느 베이스로든 만족되고, 그것은 넓이 $12.6\ \mathrm{m}^2$의 원판이다. 말단–베이스 거리 $r$이 엘보를 정하고($\cos\theta_2=(r^2-2)/2$), 그와 함께 §2의 가조작성 $w=\lvert\sin\theta_2\rvert$도 정해진다. $r=1.9$ m에 선 베이스는 $w=0.59$로 패널에 닿고, $r=2.0$ m에 선 베이스는 팔을 곧게 편 채 $w=0$으로 닿는다. 특이 자세라서 팔뚝 방향으로 세게 밀 수는 있어도 그 방향으로 움직이지는 못한다. $w\ge0.99$인 띠, 곧 $1.311$에서 $1.511$ m까지는 $1.77\ \mathrm{m}^2$로 원판의 $14\%$뿐이고, 그림의 반지름 $10$ cm짜리 $2\sigma$ 위치 원이 그 띠만큼 넓다. 그것이 §4가 예산으로 다루는 문제다.

그러므로 내비게이션 목표는 지도 위의 점이 아니다. **전체 작업이** — 웨이포인트 하나가 아니라
도달 전체가 — 여유 있게 실행 가능한 베이스 자세들의 집합이고, 그 집합을 계산하는 것이 §3의
주제다.

연구 프로그램이 내비게이션을 보조 기둥으로 두는 이유이기도 하다. 그것이 내놓아야 할 것은
어제와 달라진 현장에서 *작업 가능한 자세로의 도달*을 반복적으로 해내는 것이다. 실제로 어려운
통합 문제이고, 새 SLAM 알고리즘은 필요 없다.

### 2. 도달성과 능력

팔 하나에서 시작하자. 베이스가 고정되어 있을 때 어떤 말단 자세가 달성 가능하고, 얼마나 잘
달성되는가?

**도달 작업 영역의 정의.** $f$를 순기구학, $\mathcal{C}_{\text{free}}$를 자유 컨피규레이션 공간([[04-robotics/planning-decision-making|4. 계획 §2]])이라 하면, 도달 작업 영역은 자유 공간의 $f$에 의한 상(image)이다. 즉 *어떤* 허용 컨피규레이션으로든 도달되는 말단 pose의 집합이다:

$$\mathcal{W}_{R}=\{\,f(q)\ :\ q\in\mathcal{C}_{\text{free}}\,\}$$

공이 아니라 상이므로 모양은 관절 한계와 링크 길이가 만드는 그대로다. 그 부분집합인 **덱스트러스 작업 영역**은 *모든* 방향으로 도달 가능한 위치만 남기며, 둘 사이의 간격이 이 절이 말하는 비등방성이다. **P2**($L_1=L_2=1$ m)의 도달 집합은 $|L_1-L_2|=0$과 $L_1+L_2=2$ m 사이의 고리, 즉 반경 2 m의 닫힌 원판이다. **반례:** P2의 덱스트러스 작업 영역을 묻는 것은 범주 오류다. 평면 2R은 자유도 둘을 모두 말단 *위치*에 쓰고 고를 방향이 남아 있지 않기 때문이다 — 덱스터리티는 여유 자유도가 있는 팔에만 던질 수 있는 질문이다.

**도달성 지도(reachability map)**: 팔의 작업 영역(workspace)을 복셀로 나누고 각각에 말단이 도달할 수 있는지를
기록한다 — $\mathcal{W}_R$의 이산화된 지시 함수다. **능력 지도(capability map)**(Zacharias, Borst, Hirzinger, IROS 2007)는 한 걸음 더
나아가 *어느 방향에서* 도달 가능한지를 기록하고, 각 복셀을 그 자리에서 달성 가능한 접근 방향의 비율인 **도달성 지수**로 요약한다. 어떤 점에 위에서 닿는 것과 옆에서 닿는 것은
다른 가능성 문제이고, 팔의 작업 영역은 강하게 비등방적이기 때문이다. 그 방향 구조를 명시적이고
들여다볼 수 있게 만든 것이 기여이며, §3의 역도달성 방법들의 직계 조상이다(도달성에 기반한 베이스 배치 자체는 적어도 Seraji 1995까지 거슬러 올라간다).

**가조작성 — "얼마나 잘"을 숫자로.** 도달성은 예/아니오이고, 도달한 pose의 품질은 야코비안 $J(q)$의 성질이다. 그 타원체는 [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장 §4]]에서 정의된다. 이 페이지가 쓰는 것은 그 타원체의 스칼라 요약 둘이고, 둘은 서로 다른 질문에 답한다. Yoshikawa의 척도는 그 부피이고, 조건수는 그 일그러짐이다:

$$w(q)=\sqrt{\det\big(J J^{\top}\big)}=\lvert\det J\rvert\ \ (J\ \text{가 정사각일 때}),\qquad \kappa(q)=\frac{\sigma_{\max}}{\sigma_{\min}}$$

찌그러진 타원체는 부피가 없으므로 $w$는 특이점에서 정확히 0이 되고, 가장 큰 특잇값은 그대로인데 하나가 0으로 가므로 $\kappa$는 거기서 발산한다. 둘 다 베이스 pose가 아니라 **컨피규레이션**의 성질이다 — 베이스 pose가 중요한 것은 오직 팔이 어떤 컨피규레이션을 취해야 하는지를 그것이 정하기 때문이다.

> [!example] 계산 예제 · Worked example
> **P2**에서 두 양은 $\theta_1$이 아니라 엘보 각 $\theta_2$에*만* 의존한다. $\theta_1$을 바꾸면 과제 프레임이 회전할 뿐이기 때문이다. 이것이 조건수 문제를 *거리* 문제로 바꿔 놓는다. 말단-베이스 거리 $r=\sqrt{2+2\cos\theta_2}$ 역시 $\theta_2$만의 함수이고, 거리 하나는 베이스 위치의 고리이며, 그것이 §3이기 때문이다.
>
> | $\theta_2$ | $r$ (m) | $w=\lvert\sin\theta_2\rvert$ | $\sigma_{\max},\sigma_{\min}$ | $\kappa$ |
> |---|---|---|---|---|
> | $90°$ | 1.414 | **1.000** | 1.618, 0.618 | 2.618 |
> | $131.81°$ | 0.816 | 0.745 | 1.098, 0.679 | **1.618** |
> | $5°$ | 1.998 | 0.087 | 2.234, 0.039 | 57.26 |
> | $0°$ | 2.000 | 0.000 | 2.236, 0 | $\infty$ |
>
> **두 척도가 어긋나고, 그것이 요점이다.** $w$는 $\theta_2=90°$에서 가장 크며, 이 페이지의 그림과 과제가 쓰는 $r=\sqrt{2}$ 띠가 그곳이다. 그런데 $\kappa$는 $\theta_2=\arccos(-\tfrac23)=131.81°$에서 가장 작고, 거기서 $r=\sqrt{2/3}=0.816$ m이며 $w$는 이미 $\sqrt5/3=0.745$로 떨어져 있다. 타원체의 *부피*를 최대로 하면 베이스는 목표에서 1.41 m에 서고, 그 *일그러짐*을 최소로 하면 0.82 m에 선다. (양 극값은 정확하다. $90°$에서 $\kappa=\varphi^2$, $131.81°$에서 $\kappa=\varphi$이고 $\varphi$는 황금비다.)
>
> **반례 — "잘 조건화된 띠"를 수 하나로 말하기.** 어느 척도를 최적화했는지 말하기 전에는 그런 띠가 없다. $w$는 "팔이 모든 방향으로 빠르게 움직일 수 있는가"에 답하고, $\kappa$는 "한 방향에서의 능력이 다른 방향과 엇비슷한가"에 답하며, 한 축으로 미는 접촉 과제는 일반적으로 둘 중 어느 것도 아니라 *과제 방향에서의* $\sigma$를 따진다. 숫자에는 척도를 함께 적어라. 아니면 그 숫자는 아무 뜻도 없다.

### 3. Base placement — 질문 뒤집기

작업 자세가 주어졌을 때 베이스는 어디에 서야 하는가? 표준적인 답은 **도달성 지도를 뒤집는**
것이다: 순방향 지도가 "이 베이스 자세에서는 이 대상들에 닿을 수 있다"고 말한다면, 그것을
뒤집으면 주어진 대상에 닿을 수 있는 베이스 자세들의 분포가 나오고, 후보를 직접 샘플링해
점수를 매길 수 있다. Vahrenkamp, Asfour, Dillmann의 inverse-reachability 정식화(ICRA 2013)가
그것이고, 이 질문에 대해 분야가 인용하는 것이 그것이다.

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="작업 대상 둘레의 유효한 베이스 위치 집합은 고리 모양이며, 조건수와 장애물이 그것을 더 잘라낸다">
  <g fill="currentColor">
    <path d="M 196 116 m -94 0 a 94 94 0 1 0 188 0 a 94 94 0 1 0 -188 0 Z M 196 116 m -37 0 a 37 37 0 1 0 74 0 a 37 37 0 1 0 -74 0 Z" fill-rule="evenodd" fill-opacity="0.10"/>
    <path d="M 196 116 m -80 0 a 80 80 0 1 0 160 0 a 80 80 0 1 0 -160 0 Z M 196 116 m -51 0 a 51 51 0 1 0 102 0 a 51 51 0 1 0 -102 0 Z" fill-rule="evenodd" fill-opacity="0.22"/>
    <rect x="192" y="24" width="128" height="22" rx="2" fill-opacity="0.55"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.55">
    <circle cx="196" cy="116" r="94"/><circle cx="196" cy="116" r="80"/><circle cx="196" cy="116" r="51"/><circle cx="196" cy="116" r="37"/>
  </g>
  <g fill="currentColor"><circle cx="196" cy="116" r="5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="204" y="113">작업 자세</text>
    <text x="330" y="40">장애물: 집합의 일부를 없앤다</text>
    <text x="330" y="96">바깥 고리: 닿지만</text>
    <text x="330" y="110">조건이 나쁘다</text>
    <text x="330" y="136">음영 띠: 닿고 &#8212; 그리고 &#8212;</text>
    <text x="330" y="150">조건도 좋다. 여기 서라</text>
    <text x="330" y="176">안쪽 원: 너무 가까워</text>
    <text x="330" y="190">팔이 그만큼 접히지 못한다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="238">유효 집합은 원판이 아니라 고리이고 &#8212; 쓸 만한 부분은 그보다도 좁다. 베이스 자세 불확실성 1 cm마다,</text>
    <text x="20" y="254">애초에 수십 센티미터밖에 안 되던 띠를 그만큼씩 갉아먹는다.</text>
  </g>
</svg>

그림이 말하는 실용적 요점 둘:

- **가까울수록 좋은 것이 아니다.** 너무 가까우면 팔이 충분히 접히지 못해 닿을 수 없고, 너무
  멀면 뻗은 자세라 특이점에 가깝고, 하필 접촉 작업이 필요로 하는 방향으로 **제어 가능한 운동을 잃는다** — 쌍대성에 유의하라: 특이점 근처에서 팔은 붕괴한 방향으로 오히려 *힘은 세고*(무릎을 편 기계적 이점) 그 방향으로 움직이거나 조절하지 못한다. [[04-robotics/modern-robotics/ch05-velocity-kinematics|MR 5장의 힘·속도 타원체 쌍대성]]이 그것이다
  ([[02-foundations/manipulator-kinematics-dynamics|10. §6]] — 뻗은 팔이 실효적으로 더 무겁기도
  한 이유).
- **쓸 만한 띠가 좁으므로**, 베이스 자세 오차는 반올림 오차가 아니라 여유를 직접 소비한다.

> [!note] 이 주제에는 서베이가 없다 · There is no survey of this
> 모바일 조작의 base placement에 대한 서베이나 체계적 리뷰는 **알려진 것이 없다.** 없는 것을
> 인용하지 마라. 인용 가능한 것은 1차 방법들이다 — 능력 지도는 Zacharias 등 2007, inverse
> reachability는 Vahrenkamp 등 2013, 오픈소스 도구는 Makhal과 Goins의 Reuleaux(IRC 2018).

### 4. 모바일 조작이 실제로 달라지는 곳은 오차 예산이다

고정된 팔에도 보정·센싱·유연성·작업물 불확실성처럼 말단 오차원이 여럿 있다. 모바일 베이스는
위치 추정·기계적 정착·베이스–팔 변환 오차를 더하므로, 접촉 지점에서 만나는 불확실한 변환이
더 많아진다:

| 원천 | 통상 규모 | 비고 |
|---|---|---|
| 베이스 위치추정 | 센티미터 | 지도가 있는 건물보다 현장에서 더 나쁘다 |
| 베이스의 기계적 정착 | 밀리미터 | 궤도와 무른 지반이 하중을 받아 움직인다 |
| 팔의 기구학 오차 | 밀리미터 이하~밀리미터 | 여기에 하중 하의 변형([[01-canonical-papers/notes/8-construction/kindle-jaibot\|Kindle 등]]) |
| 작업물 위치 | 센티미터 | 부재는 누군가 놓은 자리에 있다 |

귀결 둘. 첫째, **센티미터급 개루프 오차 예산은 밀리미터 공차 주장을 뒷받침하지 못한다** — 이런
시스템은 보통 더 정밀한 계측, 작업 수준의 비전·접촉 피드백, 또는 둘 다가 필요하다. 둘째, 모바일
조작 논문을 읽는 정직한 방법은 이 넷 중 무엇을 측정했고 무엇을 가정으로 없앴는지 묻는 것이다.

이동과 조작이 그냥 이어 붙는 것이 아닌 이유에 대한 기준 서술은 Brock, Park, Toussaint의
*Springer Handbook of Robotics* "Mobility and Manipulation" 장이다 — 전신 제어, 여유 자유도
해소(둘 다 아래 §4.5에서 정의한다), 그리고 내비게이션 제약과 조작 제약의 상호작용.

> [!warning] 알아 둘 또 하나의 부재
> 모바일 조작 서베이는 존재한다 — Thakar 등, "A Survey of Wheeled Mobile Manipulation: A Decision-Making Perspective," *ASME J. Mechanisms and Robotics* 15(2):020801, 2023. 없는 것은 *Annual Review of Control, Robotics, and Autonomous Systems*에 실린
> 최근 모바일 조작 서베이이고, 흔히 그것으로 귀속되는 저자들의 것도 없다. Springer Handbook 장(2016)이 나이에도
> 불구하고 여전히 기준 서술이다. 최근 것이 필요하고 좁은 범위를 감수할 수 있다면, **가변
> 자율성**을 다룬 2025년 *Frontiers in Robotics and AI* 미니 리뷰가 있다 — 비슷한 이름을 쓴
> 다른 주제다.

> [!example] 계산 예제 · Worked example
> **모바일 파지의 오차를 더해 보기.** 우선 아래 오차들을 서로 독립인 영평균 스칼라 불확실성으로
> 근사하고 표준편차를 제곱합으로 더해 보자. 상관된 오차·편향·방향 오차·비가우시안 꼬리는 공분산
> 전파나 실측 작업공간 분포가 필요하다. 그리퍼가 닫히는 순간의 대표적인 예산은 베이스 위치 추정
> $\sigma = 5$ cm, 베이스–팔 장착부 0.3 cm,
> 팔 기구학과 관절 엔코더 0.3 cm, 손–눈 외부 파라미터(손–눈 보정이 $AX=XB$로 추정하는
> 카메라–그리퍼 변환, [[04-robotics/geometric-perception-calibration|3.5 기하 인식·보정 §5]]) 1.0 cm,
> 인식이 준 물체 자세 1.0 cm.
>
> $\sigma_{\text{total}} = \sqrt{5.0^2 + 0.3^2 + 0.3^2 + 1.0^2 + 1.0^2} = \sqrt{27.18} = \mathbf{5.2}$ cm.
>
> 60 mm까지 벌어지는 평행 그리퍼가 40 mm 물체를 잡을 때 횡방향 기하 여유는 약 $\pm 10$ mm다.
> $5.2$ cm는 **1 표준편차**만으로도 그 여유보다 훨씬 크므로 이 개루프 설계는 실패 위험이 높다.
> 이 계산만으로 개별 시도의 성공·실패가 결정된다는 뜻은 아니다.
>
> 이제 그것이 어디서 왔는지 보라. 베이스 위치 추정이 *분산*의 $25/27.18 = \mathbf{92\%}$를
> 차지한다. 팔의 보정 오차를 절반으로 줄이면 $\sigma_{\text{total}}$은 5.213 cm에서 5.207 cm가
> 된다 — 아무 일도 일어나지 않는다. 대신 베이스 항을 없애라. 베이스가 선 뒤에 손목 카메라로
> 물체를 다시 관측하면 $\sqrt{0.3^2 + 0.3^2 + 1.0^2 + 1.0^2} = 1.5$ cm만 남고, 이제는 핸드–아이와 인식 오차가 지배한다.
>
> **여기서 얻는 독법.** 모바일 조작이 지금의 모양인 이유가 이 계산 하나에 다 있다. 베이스에
> 요구되는 것은 다음 감지 단계가 작동할 만큼 *물체를 센서 시야 안에 넣는 것*이고, 그다음은 팔이 국소적으로
> 루프를 닫는다. 목표 지점에서 다시 관측하는지 밝히지 않은 채 모바일 조작 성공률을 보고하는
> 논문은, 둘 중 어느 시스템을 만든 것인지 말하지 않은 것이다.

### 4.5 전신 제어인가 분리인가 — 그리고 구별하는 법

위의 오차 예산은 베이스가 선 다음 팔이 일한다고 가정했다. 그것은 두 아키텍처 중 하나이고,
그 선택을 부르는 어휘를 정확히 적어 둘 값이 있다. 논문들이 이 말을 느슨하게 쓰기 때문이다.

**분리형**(*navigate-then-manipulate*, 또는 순차형): 베이스를 어떤 pose로 명령해 세우고,
그다음 베이스를 고정한 채 팔을 명령한다. 문제가 둘이고 차례로 풀리며, 각자 자기 상태와 자기
제어기를 가진다.

**전신(whole-body) 제어**: 베이스와 팔을 자유도 $n=n_b+n_a$짜리 하나의 기구학 사슬로 다루고,
과제 야코비안 하나가 그 전부를 말단 운동으로 사상한다. 그래서 베이스의 움직임과 관절의
움직임이 같은 과제 오차를 갚는 서로 대안적인 방법이 된다:

$$\dot x=J\dot q=\begin{pmatrix}J_b & J_a\end{pmatrix}\begin{pmatrix}\dot q_b\\ \dot q_a\end{pmatrix},\qquad \dot q=J^{+}\dot x+\big(I-J^{+}J\big)\dot q_0$$

여기서 $J^{+}$는 유사역행렬이고, 행이 독립인 넓은 $J$에 대해 $\dot x$를 이루는 가장 작은 $\dot q$를 돌려준다([[02-foundations/linear-algebra|1. 선형대수 §4.5]]). 첫 항이 과제를 달성하고, 둘째 항은 $J$의 **영공간**(null space)에 있으므로 말단을 전혀 움직이지
않은 채 컨피규레이션만 바꾼다. 부차 목표 — 가조작성, 관절 한계, 장애물 거리 — 가 들어가는
자리가 거기다. $\dot q_0$를 고르는 일이 **여유 자유도 해소**(redundancy resolution)다. 전신 제어를
정의하는 조건은 셋이고 셋 다 필요하다. 베이스와 팔을 함께 담는 상태 벡터 하나, 둘 중 어느 쪽이든
갚을 수 있는 과제 명세 하나, 그리고 같은 제어 주기 안에서 양쪽으로 나가는 명령. 하나라도 빠지면
분리형이다.

**P2에서 자유도 세어 보기.** 과제는 평면에서의 말단 위치이므로 $m=2$다.

| 아키텍처 | $n_b$ | $n_a$ | $n$ | 영공간 차원 $n-m$ |
|---|---|---|---|---|
| 전신, 홀로노믹 베이스 | 3 | 2 | 5 | **3** |
| 전신, 비홀로노믹 베이스(순간적으로) | 2 | 2 | 4 | 2 |
| 분리형, 베이스 정지 | 0 | 2 | 2 | **0** |

굵게 쓴 두 수가 이 페이지의 논증 전체를 다른 표기로 적은 것이다. 전신 제어는 과제에 아무 대가도
치르지 않는 자기 운동 방향 셋을 남기므로, 말단이 가만히 있는 *동안에도* 제어기가 자신을 §2의
찌그러진 영역 밖으로 빼낼 수 있다. 분리형은 하나도 남기지 않는다. 베이스가 팔에게 넘겨준 조건수가
곧 과제가 받는 전부이고 그것으로 끝이다. §3이 어디에 설지에 그토록 공을 들이는 이유가 정확히
그것이다. 비홀로노믹 베이스는 속도 수준에서 3을 보태지 못한다. 순간적인 옆방향 운동이 없기
때문이다([[04-robotics/planning-decision-making|4. 계획 §5.5]]).

**P2에서 풀어 본 영공간.** P2의 어깨를 월드 $(1,0)$에 방향 $\varphi=0$으로 세운 홀로노믹 베이스의 중심에 달고, 팔을 고정 자세 $\theta=(0°,90°)$에 두면 팔꿈치는 $(2,0)$, 말단은 패널 위 $(2,1)$에 있다. 다섯 속도를 $\dot q=(\dot x_b,\ \dot y_b,\ \dot\varphi,\ \dot\theta_1,\ \dot\theta_2)$ 순서로 놓는다. 베이스 병진은 말단을 그대로 옮기고, 베이스 회전은 말단을 어깨 둘레로 $\dot\theta_1$과 똑같이 휘두르며, 마지막 두 열은 그 자세에서의 P2 자신의 $J$이므로

$$J=\begin{pmatrix}1&0&-1&-1&-1\\0&1&1&1&0\end{pmatrix},\qquad J^{+}=J^{\top}\big(JJ^{\top}\big)^{-1}=\frac18\begin{pmatrix}3&2\\2&4\\-1&2\\-1&2\\-3&-2\end{pmatrix}$$

이다. $JJ^{\top}=\begin{pmatrix}4&-2\\-2&3\end{pmatrix}$의 행렬식이 $8$이고 역행렬이 $\tfrac18\begin{pmatrix}3&2\\2&4\end{pmatrix}$이기 때문이다. 그러면 영공간 사영은

$$I-J^{+}J=\frac18\begin{pmatrix}5&-2&1&1&3\\-2&4&-2&-2&2\\1&-2&5&-3&-1\\1&-2&-3&5&-1\\3&2&-1&-1&5\end{pmatrix}$$

이고 랭크가 $3$으로 위 표의 첫 행과 같다. 그것이 남기는 자기 운동 셋은 $J$에서 곧바로 읽히고, 각각 $Jn=0$이다. $(0,0,1,-1,0)$은 베이스를 한쪽으로, 어깨를 반대쪽으로 돌린다. $(1,0,0,0,1)$은 베이스를 $+x$로 밀고 팔꿈치가 말단을 같은 만큼 되돌린다. $(1,-1,1,0,0)$은 베이스를 대각선으로 옮기면서 돌려 말단이 제자리에 머문다. 이제 말단이 패널 면을 따라 $0.2$ m/s로 미끄러지게 하자, $\dot x=(0,\ 0.2)$:

| 선택 | $\dot q=(\dot x_b,\ \dot y_b,\ \dot\varphi,\ \dot\theta_1,\ \dot\theta_2)$ | $\lVert\dot q\rVert$ | 하는 일 |
|---|---|---:|---|
| 분리형, 베이스 정지: $J_a^{-1}\dot x$ | $(0,\ 0,\ 0,\ 0.2,\ -0.2)$ | $0.283$ | 어깨와 팔꿈치가 모두 돌고, 팔꿈치가 §3이 세워 둔 $90°$에서 멀어진다 |
| 전신, $\dot q_0=0$: $J^{+}\dot x$ | $(0.05,\ 0.1,\ 0.05,\ 0.05,\ -0.05)$ | $0.141$ | 최소 노름 분담: 다섯이 모두 조금씩 움직이고 팔꿈치는 분리형의 4분의 1 속도다 |
| 전신, $\dot q_0=(0,\ 0.2,\ 0,\ 0,\ 0)$, "베이스가 나르게" | $(0,\ 0.2,\ 0,\ 0,\ 0)$ | $0.200$ | 팔은 $w=1$에서 멈추고 베이스가 패널을 따라 달린다 |

마지막 행에서 사영은 최소 노름 분담에 $(I-J^{+}J)\dot q_0=(-0.05,\ 0.1,\ -0.05,\ -0.05,\ 0.05)$를 더하고, $J$에 그 벡터를 곱하면 정확히 $(0,0)$이다. 말단을 움직이지 않고 운동의 모양만 바꾼다. 부차 목표란 숫자로 이것이다 — 과제를 온전히 수행하면서 팔이 가장 조건이 좋은 팔꿈치 각을 지키는 것이고, 영공간 차원이 $0$인 분리형 행은 이것을 할 수 없다. 식이 감추는 단서 하나: 유사역행렬의 "가장 작은"은 초당 미터와 초당 라디안을 같은 무게로 잰다. 링크가 $1$ m인 P2에서는 무해하지만 다른 팔에서는 사실이 아니라 선택이고, 가중 유사역행렬을 쓰면 분담이 달라진다.

**반례.** 베이스 속도와 팔 속도를 같은 메시지로 보내는 것은 전신 제어가 아니다. 베이스 명령이
경로 추종기에서 나오고 팔 명령이 베이스의 *추정* pose에 대해 푼 IK에서 나온다면 둘은 여전히
분리형이고, 시간상 겹쳐 있을 뿐이다. 전신으로 만드는 것은 베이스의 움직임이 과제 오차를 흡수할
수 있는 야코비안 하나다.

*왜 중요한가.* §6의 표는 논문이 둘 중 무엇을 만들었는지를 묻는다. 그 답이 베이스 pose 오차가
팔이 사후에 감당해야 할 외란인지(분리형이라 §4의 예산에 고스란히 들어간다), 아니면 제어기가
여전히 쓸 수 있는 좌표인지(전신이라 과제가 도는 중에 보정된다)를 결정한다.

### 대상으로 한 번 끝까지 · Worked case

§2는 팔이 어디서 조건이 좋은지 말했고, §3은 그것을 베이스 위치의 고리로 바꿨으며, §4는 베이스
자신의 오차를 주었다. 셋을 **P2** 위에서 합치면 이 페이지의 중심 주장 — *쓸 만한 띠가 좁으므로
베이스 자세 오차는 반올림 오차가 아니다* — 이 검산할 수 있는 숫자가 된다.

**1. 띠를 미터로.** P2에서 Yoshikawa 척도는 $w=\lvert\det J\rvert=\lvert\sin\theta_2\rvert$이고
말단–베이스 거리는 $r=\sqrt{2+2\cos\theta_2}=2\lvert\cos(\theta_2/2)\rvert$로, 둘 다 엘보 각만의
함수다(§2). 그러므로 "$w\ge w_0$을 지켜라"는 엘보 각의 구간
$\theta_2\in[\arcsin w_0,\ 180°-\arcsin w_0]$이고, $r$이 그것을 거리의 구간으로 옮긴다. 양 끝의
코사인을 $c=\sqrt{1-w_0^2}$라 쓰면 두 반지름은 $\sqrt{2+2c}$와 $\sqrt{2-2c}$이고, 그 차의 제곱은
$(2+2c)+(2-2c)-2\sqrt{4-4c^2}=4-4w_0$이다. 교차항이 $2\sqrt{4-4c^2}$이고
$\sqrt{1-c^2}=w_0$이기 때문이다. 따라서 띠의 폭은

$$\Delta r=2\sqrt{1-w_0}$$

이고, 가조작성을 얼마나 요구하느냐의 제곱근으로 닫힌다. 문턱값 둘, 두 띠 모두 엘보 각으로 $90°$, 곧 §2 표의
$r=\sqrt2=1.414$ m 고리를 가운데 둔다.

| $w_0$ | 엘보 구간 | $r$ 범위 (m) | 띠 폭 $\Delta r$ (m) |
|---|---|---|---:|
| $0.90$ | $64.16°$–$115.84°$ | $1.062$–$1.695$ | $0.632$ |
| $0.99$ | $81.89°$–$98.11°$ | $1.311$–$1.511$ | $0.200$ |

**2. 띠와 베이스 자신의 오차.** §4의 예산은 베이스 위치 추정을 $\sigma=5$ cm로 잡으므로
$\pm2\sigma$ 구간은 $20$ cm다 — $w\ge0.99$ 띠 전체이고, 느슨한 $w\ge0.90$ 띠의 3분의 1이다. 그러니
좁은 띠의 한가운데로 명령한 베이스는 2시그마에서 두 가장자리 사이 어디든 될 수 있다. §3의 배치
계산이 돌려준 공칭 자세의 불확실성이 답 자체의 크기인 것이다. §3의 그림 설명을 산수로 옮기면 이렇다.

**3. 고칠 곳은 어디인가.** 베이스 위치 추정이 §4 분산의 $25/27.18=92\%$이므로 팔에 무엇을 해도 이
숫자는 움직이지 않는다. 베이스가 선 뒤 손목 카메라로 대상을 다시 관측하면 남는 예산은 $1.5$ cm —
반올림 전으로는 $1.476$ cm — 이므로 $\pm2\sigma$ 구간은 $4\times1.476=5.9$ cm다. $20$ cm 띠 안에
여유 있게 들어가고 작업물 몫까지 남는다. 조건수
요구는 바뀌지 않았다. 바뀐 것은 마지막 변환을 어느 센서로 쟀는가다.

**여기서 얻는 독법.** 베이스 배치 기준만 말하고 베이스 자세 불확실성을 말하지 않은 논문은 이 절이
곱한 두 수 중 하나만 준 것이다. $w_0$을 밝히지 않은 채 "조건이 좋은" 배치라고 한 논문은 첫 번째
수조차 주지 않은 것이다. 같은 팔이 한 문턱에서는 $63$ cm 띠이고 다른 문턱에서는 $20$ cm 띠다.

### 5. 계속 변하는 현장에서 위치 잡기

건설은 대부분의 위치추정 시스템이 딛고 선 가정을 깬다: 지도가 정적이라는 가정. 건물이
작업물이므로 어제의 지도는 구조적으로 틀려 있고 — 변한 부분이 바로 지금 작업하는 부분이다.

문헌에 나타나는 대응 셋:

- **외부 측정 장치.** Ercan 등(ISARC 2019)은 로봇 토털 스테이션으로 모바일 건설 로봇의 위치를
  잡아, 베이스를 반복해서 옮겨도 말단 정확도가 살아남게 한다. 대규모 실외 실험으로 검증했다.
  실용적인 답이고, In situ Fabricator와 같은 랩 계보에서 나왔다.
- **참조 모델에 정박하기.** SLAM2REF(Vega-Torres, Braun, Borrmann, *Construction Robotics*,
  2024)는 LiDAR-관성 세션을 기존 BIM이나 참조 포인트 클라우드에 정합해, 드리프트 없는 자세와
  반복 방문에 걸친 지도 확장을 준다. 실기계 현장 시험이 아니라 ConSLAM 실제 현장 데이터셋으로
  평가했다.
- **드리프트를 받아들이고 작업에서 루프를 닫기.** 접촉 단계가 센티미터를 교정할 수 있다면,
  위치추정은 §3의 띠 안에만 데려다주면 된다.

**띠가 견디는 드리프트의 양.** §3의 $w\ge0.99$ 띠는 폭이 $20$ cm이므로, 그 가운데를 겨냥한 베이스는 거리 방향으로 $10$ cm까지 벗어나도 $w\ge0.99$를 지킨다. §4 예산의 위치추정 $\sigma=5$ cm라면 그 반폭이 $2\sigma$이고, 베이스가 그 안에 들어올 확률은 $\mathrm{erf}(2/\sqrt2)=0.954$다. 드리프트는 기준을 다시 잡는 사이사이에 쌓이는 것이고, 0이 아니라 이 $10$ cm에 대고 판단해야 한다. 이동 거리의 $1\%$라고 가정한 오도메트리 드리프트라면 $30$ m를 접근하는 동안 $30$ cm가 쌓여 반폭의 세 배가 된다. 변하는 현장은 그와 다른 일을 한다. 어제의 지도를 틀리게 만들어 지도를 기준으로 삼을 수 없게 한다. 위의 대응들이 지도를 믿지 않고 기준을 다시 잡는 이유가 그것이다. 앞의 둘은 외부 기준(토털 스테이션의 측정, 또는 BIM 모델이나 이전 포인트 클라우드)에, 셋째는 작업 지점에서 부재 자체에 기댄다.

분야 조감으로는 Yarovoi와 Cho의 2024년 건설 로보틱스 SLAM 리뷰(*Automation in Construction*)가
여기서는 실제로 존재하는 서베이다.

### 6. 모바일 조작 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 시행 사이에 베이스를 **다시 배치했는가**, 한 번만 놓았는가? | 한 번만 놓으면 가장 어려운 오차 원천이 사라진다 |
| 베이스 자세를 무엇으로 쟀는가 — 로봇에게는 없는 무엇으로? | 외부 추적은 결과를 난이도의 하한으로 만든다 |
| 작업 공차가 명시되어 있고, 오차 예산이 닫히는가? | 둘 다 없으면 "성공"이 정의되지 않는다 |
| 정적 지도인가 변하는 환경인가? | 건설의 경우는 후자다 |
| 전신 제어(베이스와 팔을 함께 명령)인가, 이동한 뒤 조작(베이스 이동 후 별도의 팔 동작)인가? | 순차 방식이 더 쉽고, 표현이 시사하는 것보다 훨씬 흔하다 |
| 벤치마크: 시뮬레이션인가, 실제인가, 둘 다인가? | HomeRobot은 둘 다, BEHAVIOR-1K는 시뮬레이션만 |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 모바일 매니퓰레이터의 내비게이션 목표를 한 문장으로 말한다.
- [ ] 유효 베이스 영역이 왜 고리이며 쓸 만한 부분은 왜 더 좁은지 설명한다.
- [ ] 오차 원천 넷을 대고 건설이 어느 것을 가장 나쁘게 만드는지 말한다.
- [ ] 지도가 계속 변하는 현장에서 위치를 잡는 두 방법을 댄다.
- [ ] 이 문헌에 존재하지 않는 것을 말해서, 그것을 인용하지 않는다.

> [!tip] 더 깊이 · Going deeper
> 여기서 교과서에 가장 가까운 것은 핸드북 한 장이다: Brock, Park, Toussaint, "Mobility and Manipulation," *Springer Handbook of Robotics* (2판, 2016) 40장. 틀을 잡기 위해 이것을 읽고, 그다음 base placement를 계산 가능하게 만든 두 논문을 읽어라 — 능력 지도의 Zacharias 외(IROS 2007), 도달성을 배치로 뒤집은 Vahrenkamp 외(ICRA 2013). 어떤 출처도 다루지 않는 것이 §4다. 오차 예산은 시스템 구전 지식이고, 이 페이지가 인용 대신 직접 계산해 보인 이유가 그것이다.

### 스스로 점검

1. 어떤 팀이 "도달 범위를 최대화하려고" 베이스를 벽에 최대한 붙여 세운다. 무엇이 잘못되었는가?
2. 작업에 2 mm 배치 정확도가 필요하다. 베이스는 ±3 cm로 위치를 잡는다. 무엇이 따라 나오는가?
3. 정적 지도 SLAM 벤치마크가 왜 건설 현장 성능의 나쁜 예측자인가?
4. 어떤 논문이 모바일 조작 과제에서 95% 성공을 보고하는데, 베이스 자세는 외부 모션 캡처로
   기록했다. 그 숫자는 무엇을 뜻하는가?
5. Base placement 서베이를 인용하고 싶다. 어떻게 하겠는가?

> [!tip]- 정답 · Answers
> 1. 구속 조건은 도달 범위가 아니라 조건수다. 벽에 바짝 붙이면 팔이 접히거나 작업 공간 가장자리 가까이 뻗은 자세가 되고, 거기서는 가조작성 타원체가 납작해져 어떤 방향으로 정밀하게 움직이거나 조절하지 못한다 — 흔히 하필 작업이 미는 그 방향이다. (그 방향으로 힘은 오히려 *세다*. 잃은 것은 제어 가능한 운동이다.) 목표는 도달 한계선이 아니라 §3의 음영 띠다.
> 2. 개루프 실행으로는 공차를 맞출 수 없다는 것 — ±3 cm의 베이스 오차만으로도 요구치의 열다섯 배이고, 팔과 작업물이 기여하기도 전이다. 무언가가 작업에서 루프를 닫아야 한다: **비전 서보잉**(추정된 자세가 아니라 카메라가 지금 보는 특징으로 팔을 구동하는 것)이나, 특징을 기계적으로 찾아 들어가는 유연 접촉 단계([[04-robotics/force-compliance-control|13. §5]]). 변명할 약점이 아니라 그것이 설계다.
> 3. 틀린 난이도를 재기 때문이다. 정적 지도 벤치마크는 가만히 있는 장면에 정확히 정합하는 것을 보상하는데, 건설 현장은 *로봇과 다른 공종이 그것을 바꾸고 있기 때문에* 변하고, 변한 영역이 정확히 작업 영역이다. 앞의 것에서 좋은 점수를 받는 시스템이 뒤의 것에서는 크게 표류할 수 있다.
> 4. 정확한 베이스 자세가 주어졌을 때 *조작*이 동작했다는 것. 외부 모션 캡처는 현장에서 로봇이 갖지 못할 자세를 공급하므로, 결과는 실제 난이도의 하한이다 — 내비게이션과 위치추정의 기여가 실험에서 빠져 있다. 조작 주장을 분리하는 정당한 방법이다. 논문이 그렇게 밝히고 독자가 그렇게 읽는다면.
> 5. 대신 1차 방법을 인용하라 — 능력 지도는 Zacharias 등 2007, inverse reachability는 Vahrenkamp 등 2013 — 그런 서베이가 존재하지 않는 것으로 확인되었기 때문이다. "이 주제의 서베이는 없으며 1차 참고문헌은…"이라고 쓰는 것이 정확하고, 찾아봤다는 것을 보여 준다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**를 홀로노믹 베이스 위에. 패널은 월드 $(2,1)\,\mathrm{m}$. 고정 자세: 말단이 베이스 기준 $(1,1)$, $\det J=1$. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** 도달 범위는 같은 $2$ m이지만 링크 길이가 다른 팔, $L_1=1.2$ m와 $L_2=0.8$ m를 같은 홀로노믹 베이스에 올리고 패널을 월드 $(2,1)$에 둔 위의 그림: 패널 둘레의 원 — 바깥, 조건이 가장 좋은 고리, 안쪽 — 축척을 지킨 $w\ge0.99\,w_{\max}$ 띠, 그리고 $\theta=(0^\circ,90^\circ)$에서 말단을 패널에 올리는 베이스와 그 링크 둘. P2의 그림에 없던 무엇이 나타나는가?
2. **유도.** (a) 고정 자세의 베이스 위치. (b) 말단–베이스 거리 $r=\sqrt{2+2\cos\theta_2}$. $\theta_2=90^\circ$, $5^\circ$, $0^\circ$의 값. (c) 그 세 각에서 $\det J=L_1 L_2\sin\theta_2$.
3. **해석.** 어떤 팀이 "최대한 가까이" 세워서 팔을 패널을 향해 완전히 뻗는다. 무엇을 최대화했고, 패널을 누르는 방향에서 무엇을 잃었는가?

> [!note]- 그리는 법 · How to draw it
> - 원점의 축과 $0.25$ m짜리 모눈 한 칸, 그리고 $(2,1)$의 패널과 그 점을 지나는 패널 법선. 법선은 도구가 밀 방향, 곧 §3의 논증이 다루는 방향이다.
> - 원은 베이스가 아니라 패널을 중심으로 그린다. 이것이 §3의 뒤집기이고, 원을 반대로 그리는 것이 흔한 실수다.
> - $(2,1)$을 중심으로, 팔이 곧게 펴지고 $\det J=0$인 바깥 원 $r=L_1+L_2=2$ m, 이어 $w=L_1L_2|\sin\theta_2|$가 최댓값 $w_{\max}=0.96$에 닿는 고리 $r=\sqrt{L_1^2+L_2^2}=1.442$ m.
> - P2에는 없던 안쪽 원 $r=|L_1-L_2|=0.4$ m. 그 안의 베이스는 패널에 아예 닿지 못한다. 이 팔은 말단을 베이스에 그보다 가깝게 접을 수 없기 때문이다.
> - $w\ge0.99\,w_{\max}$, 곧 $|\sin\theta_2|\ge0.99$ 또는 $\cos\theta_2=\pm0.141$인 띠를 축척대로 칠한다. $1.345$부터 $1.533$ m까지, 폭 $18.8$ cm로 모눈 한 칸보다 좁다.
> - $\theta=(0^\circ,90^\circ)$의 베이스: 말단이 베이스에서 $(1.2,\ 0.8)$에 있으므로 베이스는 $(2,1)-(1.2,0.8)=(0.8,\ 0.2)$다. 엘보와 말단까지 링크 둘을 그리고, 그것이 $1.442$ m 고리 위에 있는지 확인한다.
> - 그 베이스를 중심으로 §4의 베이스 위치 추정 두 시그마인 반지름 $10$ cm의 원. 지름 $20$ cm로, 이제 $18.8$ cm 띠보다 조금 넓다.

> [!tip]- 정답 · Solutions
> 1. 바깥 원 $r=L_1+L_2=2$ m는 전처럼 특이하다. 새로 생긴 것은 안쪽 원 $r=|L_1-L_2|=0.4$ m다. 그보다 가까운 베이스는 패널에 닿지 못한다. 이 팔은 말단을 베이스에 $0.4$ m보다 가깝게 접을 수 없기 때문이다. $w=L_1L_2|\sin\theta_2|$는 $\theta_2=90^\circ$에서 $w_{\max}=0.96$으로 가장 크고, 그 자리는 고리 $r=\sqrt{L_1^2+L_2^2}=\sqrt{2.08}=1.442$ m다. $w\ge0.99\,w_{\max}$ 띠($\cos\theta_2=\pm0.141$)는 $1.345$부터 $1.533$ m까지로 폭 $18.8$ cm, P2의 $20$ cm보다 좁다. $\theta=(0^\circ,90^\circ)$의 베이스는 $(2,1)-(1.2,0.8)=(0.8,\ 0.2)$로 그 고리 위에 있고, 지름 $20$ cm의 위치 추정 원은 이제 띠를 조금 넘친다.
> 2. (a) $(2,1)-(1,1)=(1,0)$. (b) $r(90^\circ)=\sqrt{2}$, $r(5^\circ)\approx 1.998$, $r(0^\circ)=2$. (c) $\det J=1$, $\sin 5^\circ\approx 0.087$, $0$.
> 3. 도달 범위를 최대화하고 특이 고리에 세웠다. $\det J\to 0$: 잃은 방향은 팔 축이고, 곧게 뻗었다면 그것이 패널 법선이다. 그 방향으로 팔은 *강하고*, 모터로 *움직이거나* 힘을 조절하지는 못한다. 쓸 집합은 바깥 한계가 아니라 $\sqrt{2}$ 띠다.

### 출처

- F. Zacharias, C. Borst, G. Hirzinger, "Capturing robot workspace structure: representing robot capabilities," IROS 2007, pp. 3229–3236 — 능력 지도.
- N. Vahrenkamp, T. Asfour, R. Dillmann, "Robot placement based on reachability inversion," ICRA 2013, pp. 1970–1975 — 표준적인 base placement 정식화.
- A. Makhal, A. K. Goins, "Reuleaux: Robot Base Placement by Reachability Analysis," IRC 2018, pp. 137–142 ([arXiv:1710.01328](https://arxiv.org/abs/1710.01328)) — 오픈소스 도구.
- O. Brock, J. Park, M. Toussaint, "Mobility and Manipulation," *Springer Handbook of Robotics* 2판 40장, pp. 1007–1036, 2016 — 기준 서술.
- S. Ercan, S. Meier, F. Gramazio, M. Kohler, "Automated Localization of a Mobile Construction Robot with an External Measurement Device," ISARC 2019, pp. 929–936.
- M. A. Vega-Torres, A. Braun, A. Borrmann, "SLAM2REF: advancing long-term mapping with 3D LiDAR and reference map integration," *Construction Robotics*, vol. 8, no. 2, art. 13, 2024 ([arXiv:2408.15948](https://arxiv.org/abs/2408.15948)).
- A. Yarovoi, Y. K. Cho, "Review of simultaneous localization and mapping (SLAM) for construction robotics applications," *Automation in Construction*, vol. 162, art. 105344, 2024.
- 벤치마크: S. Yenamandra et al., "HomeRobot: Open-Vocabulary Mobile Manipulation," CoRL 2023, PMLR vol. 229, pp. 1975–2011 — **시뮬레이션과 실기계 둘 다**. C. Li et al., "BEHAVIOR-1K," CoRL 2022, PMLR vol. 205, pp. 80–93 — **시뮬레이션만**.

**이 위키 안에서**

- [[04-robotics/state-estimation-slam|3. 상태 추정·위치추정·SLAM]] — 추정 기계 장치
- [[05-construction-robotics/site-perception|현장 인식·Scan-to-BIM·점검]] — 도메인의 인식 층
- [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA]] — 모바일 조작의 시연 수집
