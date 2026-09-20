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

> [!note] First pass · 처음이라면
> Read the Running object and the Worked case below — one handle, one thin plate, and the four forces that decide whether a rendering algorithm needs memory. Then §2 and §3, which are the two algorithms those forces came from. §4 to §6 are the surface properties layered on top, and §7 is how to read somebody else's version of all this.

### Running object · 이 페이지의 대상

Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]], with one change to what it touches: the catalog's half-space wall is replaced by a **plate of finite thickness**, because a half-space is precisely the one shape on which every algorithm in this page agrees.

| Symbol | Value | What it is |
|---|---:|---|
| $k_w$ | $400\,\mathrm{N/m}$ | catalog wall stiffness, reused as the rendering stiffness $K$ |
| $x_w$ | $0.030\,\mathrm{m}$ | the plate's **entry** face; $+x$ is into the plate |
| thickness | $4\,\mathrm{mm}$ | so the plate occupies $x\in[0.030,\ 0.034]$ and its mid-plane is at $0.032$ |
| $b$ | $0.8\,\mathrm{N{\cdot}s/m}$ | device damping, needed only to quote 24.4's ceiling $2b/T=1600\,\mathrm{N/m}$ |
| $F^{\max}$ | $2.0\,\mathrm{N}$ | the largest handle force P3's amplifier can produce, derived in [[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3 §3]] |

The plate's thickness is this page's own frozen number; everything else is catalog. A second thickness, $2\,\mathrm{mm}$, is used once, to show where the argument changes sign.

*Scope: this page teaches what the loop computes **inside** the stability ceiling — how geometry becomes a force, why a stateless force law fails on anything thinner than a half-space, what the proxy adds, and the surface properties (damping, friction, texture) layered on top. It does not teach why the ceiling exists, which is [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]; nor the $J^\top$ step that sends the force to motors, which is [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]; nor how to run a psychophysical study on the perceptual tricks of §4, which is [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]].*

### Homework diagram · 과제가 그릴 그림

Two pictures side by side, of the *same* instant, and the problem set asks for exactly these two.

**Left — penalty.** The $x$ axis horizontal, the plate as a shaded band from $0.030$ to $0.034$, the mid-plane at $0.032$ as a dashed line through it. Put the device point at $x=0.036\,\mathrm{m}$, outside the far face. Draw the force as an arrow pointing in $+x$ — *away* from where the user came in — and label it $0.80\,\mathrm{N}$. Next to it write the rule the arrow obeys, "toward the nearest face", and mark which face that is.

**Right — proxy.** The same band, the same device point at $0.036$. Now draw a second, hollow point sitting *on the entry face* at $0.030$ and label it $p_{\text{proxy}}$. Draw the spring between the two points and the force arrow in $-x$, labelled $2.4\,\mathrm{N}$. Write beside it the rule this arrow obeys, "toward the proxy", and note that the proxy has not moved since the point entered.

**Underneath both**, one shared axis: mark $x_w=0.030$, the mid-plane $0.032$, the far face $0.034$ and the device point $0.036$ to scale, so the two arrows are visibly reading the same geometry and disagreeing about the answer. The two forces differ by $3.2\,\mathrm{N}$ and point in opposite directions, which is the entire argument of §3 in one figure.

### Worked case · 대상으로 한 번 끝까지

Five steps on the plate above. Catalog numbers throughout; the one page-local number is the thickness.

**Step 1 — the penalty law, and its ceiling.** Penetration from the entry face is $d=x-x_w$, so while the device point is in the near half the force is $-Kd$ and grows linearly. The largest force the plate can produce before the point reaches the mid-plane is therefore

$$F_{\text{ceil}}=K\cdot\frac{\text{thickness}}{2}=400\cdot 0.002=0.80\,\mathrm{N}$$

because past the mid-plane the *nearest* face is no longer the one the user entered through, and §2's third failure takes over. On P3's amplifier, which can supply $2.0\,\mathrm{N}$, any determined push is $2.5$ times this ceiling: the catalog wall does not hold this plate.

**Step 2 — the penalty force after pop-through.** At $x=0.036\,\mathrm{m}$ the nearest face is the far one at $0.034$, so the penalty law measures $0.002\,\mathrm{m}$ of penetration from *that* side and pushes the point further out the back:

$$F_{\text{penalty}}=+K\cdot(0.036-0.034)=+400\cdot0.002=+0.80\,\mathrm{N}$$

the same magnitude as Step 1 and the opposite direction. Nothing in the algorithm is broken; the force law is doing exactly what it says, and what it says is wrong.

**Step 3 — the proxy force at the same instant.** Give the algorithm one state variable, a proxy constrained to stay out of the plate and moved each period toward the device point as far as the constraints allow (§3). It entered at $x_w$ and cannot pass through the plate, so it is still at $0.030$, and the rendered force is the spring between the two points:

$$F_{\text{proxy}}=K\,(x_{\text{proxy}}-x)=400\cdot(0.030-0.036)=-2.4\,\mathrm{N}$$

pulling the hand back the way it came. Same geometry, same stiffness, same instant; the two algorithms differ by $3.2\,\mathrm{N}$ and by a sign, and the only difference between them is one remembered number.

**Step 4 — can stiffness rescue the penalty law instead?** Ask it backwards. To make $F_{\text{ceil}}$ exceed the amplifier's $2.0\,\mathrm{N}$ on this plate the penalty method needs

$$K\ \ge\ \frac{F^{\max}}{\text{thickness}/2}=\frac{2.0}{0.002}=1000\,\mathrm{N/m}$$

and $1000$ is inside 24.4's ceiling of $2b/T=1600\,\mathrm{N/m}$ at $T=10^{-3}$, so on a $4\,\mathrm{mm}$ plate a stiffer penalty wall genuinely does fix it. Halve the plate to $2\,\mathrm{mm}$ and the same arithmetic asks for $2.0/0.001=2000\,\mathrm{N/m}$, which is *outside* that ceiling — and no rate, gain or tuning available on P3 reaches it.

**Step 5 — read what Step 4 actually proved.** There is a thickness below which stiffness cannot save a stateless algorithm on a given device, and on P3 at $1\,\mathrm{kHz}$ it lies between $2$ and $4$ millimetres. Above it the choice between penalty and proxy is an engineering preference; below it the proxy is the only one of the two that works, at any stiffness. That is why §3 is a different algorithm rather than a better-tuned one, and it is why the catalog half-space of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] never had to make the choice: a half-space has one face, so "nearest face" and "entry face" are the same answer and the two laws coincide exactly.

### 1. What the loop actually computes

Every impedance-type haptic loop does the same four things, once per servo period: read the device position, decide whether the user's point is touching something in the virtual environment, compute a force if it is, and send that force to the motors through $J^\top$ ([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]). [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] is about step four's stability. This page is about steps two and three: the *algorithm* that turns geometry into a force.

One fact shapes all of it. With an impedance device nothing is rigid: every contact is a spring, $F = Kx$, and $K$ is capped by the device and the sample rate. So the design question is never "how do I render a rigid wall" but "how do I make a soft spring *feel* like one". The answers fall into three families: better geometry (§2–§3), perceptual tricks (§4), and surface properties layered on top (§5–§6).

### 2. Penalty-based rendering

The simplest algorithm treats penetration as a spring compression. For a wall with unit normal $\hat n$ through a point $p_0$, the penetration depth of the device point $p$ is $d = (p_0 - p)\cdot\hat n$, and

$$F = \begin{cases} K\,d\,\hat n, & d > 0 \\ 0, & d \le 0 \end{cases}$$

pushes the point back out along the normal. A sphere is the same with $\hat n$ pointing from the centre to $p$ and $d = R - \lVert p - c\rVert$; a box is six walls with the nearest face chosen. Because the force is a function of position only, it is stateless, cheap, and the natural first thing to write.

> **Penalty-based rendering, defined.** **Penalty-based rendering** is a *memoryless function* from the current device configuration to a force — a map $\mathbb{R}^3\to\mathbb{R}^3$ and nothing more. It is not an algorithm with state, and its three failures below are consequences of that, not bugs in it. Three defining conditions. The force depends on the **current position only**, so the same position always produces the same force however the point arrived there. It is **zero outside the object** and proportional to a penetration measure inside, which makes the object's boundary the only place it is discontinuous in slope. And its direction is the outward normal at the **nearest** surface point, which is a purely geometric choice made afresh every period.
>
> $$F(p)=K\max\!\big(d(p),\,0\big)\,\hat n(p),\qquad d(p)=(p_0-p)\cdot\hat n,\qquad \hat n(p)=\hat n\big(\arg\min_{q\in\partial\mathcal{O}}\lVert q-p\rVert\big)$$
>
> where $p$ is the device point, $\mathcal{O}$ the object, $\partial\mathcal{O}$ its surface, $d$ the penetration depth along the normal and $K$ the rendering stiffness — and it is the *third* factor, the nearest-point argmin recomputed each period, that carries all three failures, because a minimiser can jump between faces between one sample and the next.
>
> - **Example**: the half-space of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §1]]. One face, so the argmin never has a choice to make, and the penalty law is not an approximation there — it is exact.
> - **Non-example**: the $4\,\mathrm{mm}$ plate of the Worked case. Two faces, so past the mid-plane the argmin returns the far one and the force reverses to $+0.80\,\mathrm{N}$. Nothing degraded gracefully; the law computed a different object's answer.
> - **Non-example**: a penalty force with a damping term $-B v_n$ added (§5). That has a velocity in it and so is no longer a function of position alone — a useful reminder that "penalty" names the *position* part, and the damping is a separate, and separately justified, addition.
> - **Why it matters**: statelessness is exactly what makes it cheap enough to run at a kilohertz on arbitrary geometry, and exactly what makes it wrong on anything with two faces near each other. Every algorithm in §3 is bought by giving that property up.

> [!example] Worked example · 계산 예제
> A wall tilted 45° from the $x$ axis, $K = 500$ N/m, and the device point $3$ mm inside it. Penetration is measured along the normal, so $F = 500 \times 0.003 = 1.5$ N along $\hat n = (\cos 45°, \sin 45°)$, i.e. about $1.06$ N in $x$ and $1.06$ N in $y$. The user feels one force normal to the surface; the device produces it as two motor torques via $J^\top$. Note what is *not* here: nothing resists sliding along the wall, which is why a penalty wall feels like ice (§5).

Penalty methods fail in three ways, and Ruspini, Kolarov and Khatib named them (SIGGRAPH 1997):

- **Lack of locality.** The force depends only on the current position, not on how the point got there. Where two surfaces meet, "nearest surface" can change from one sample to the next, and the force flips direction. 24.4 §1 mentions this as the edge that ejects the user sideways.
- **Force discontinuities.** The same flip produces a step in force, which the hand feels as a click or a kick that no real object makes.
- **Pop-through of thin objects.** A penalty force always points toward the *nearest* surface. Push past the middle of a thin wall and the nearest surface is the far side, so the algorithm helpfully pushes you out the back.

> [!example] Worked example · 계산 예제
> A virtual plate $4$ mm thick rendered with $K = 1000$ N/m. The largest force the plate can produce before the device point crosses its mid-plane is $K \times 2\,\text{mm} = 2$ N. Any user who pushes harder than $2$ N pops through and is then pushed out the other side. Raising $K$ helps only until the stability ceiling of 24.4; making the plate thicker helps only until it looks wrong. The same plate at P3's catalog $k_w = 400$ N/m holds only $0.80$ N, which is where the Worked case starts.

### 3. Constraint-based rendering: the proxy

The fix is to give the algorithm memory. Keep a second point, the **proxy** (Ruspini et al. 1997) or **god object** (Zilles & Salisbury, IROS 1995), that is constrained to stay on the surface of the virtual objects. The device point may penetrate; the proxy may not. Each servo period the proxy moves toward the device point as far as the constraints allow — the same idea as a greedy planner walking toward a goal and sliding along whatever obstacle it hits — and the rendered force is a spring between the two:

$$F = K\,(p_{\text{proxy}} - p_{\text{device}})$$

> **The proxy (god object), defined.** The **proxy** is a *state variable* — a second point carried across servo periods — together with the constrained minimization that updates it. It is not a force law, and the spring in the equation above is the smallest part of it. Three defining conditions, and the second is what makes the motion continuous. The proxy is confined to the **non-penetrating set** $\mathcal{C}$ at all times, so unlike the device point it never enters an object. Each period it moves to the point of $\mathcal{C}$ **closest to the device point that is reachable from where it was**, which is a constrained minimization rather than a global nearest-point query, and the reachability clause is the memory. And the rendered force is the spring from device point **to proxy**, so its direction is always out of the object and never into it.
>
> $$p^{\text{prox}}_k=\arg\min_{p\in\mathcal{C},\ p\ \text{reachable from}\ p^{\text{prox}}_{k-1}}\lVert p-p^{\text{dev}}_k\rVert,\qquad F_k=K\big(p^{\text{prox}}_k-p^{\text{dev}}_k\big)$$
>
> where $\mathcal{C}$ is the free space outside every object, $p^{\text{dev}}_k$ the measured device point and $p^{\text{prox}}_k$ the proxy — and the subscript $k-1$ inside the constraint is the whole difference from §2, because it is the only place the past appears.
>
> - **Example**: the Worked case at $x=0.036$. The proxy is still at the entry face $0.030$ — reachability forbids it from crossing the plate to reach the nearer far face — so the force is $-2.4\,\mathrm{N}$, inward, where the stateless law gave $+0.80\,\mathrm{N}$, outward.
> - **Non-example**: taking the global nearest surface point each period and calling it a proxy. That is the penalty law with extra steps: drop the reachability clause and the "proxy" jumps to the far face at the mid-plane exactly as $\hat n$ did.
> - **Non-example**: a 1-DoF half-space. There $\mathcal{C}$ is a half-line and the constrained minimiser is always the single boundary point, so proxy and penalty return the same force at every instant — which is why the catalog wall of 24.4 can be written in the penalty form without meeting any of §2's failures.
> - **Why it matters**: it costs one stored point per contact and resolves all three failures at once, which is the best trade in the subject. **God object** (Zilles & Salisbury 1995) is this construction with an ideal zero-radius point; **virtual proxy** (Ruspini et al. 1997) gives the same point a finite radius and adds friction and force shading on top. The defining conditions above are shared; the radius is the difference.

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

Those three are the ones a rendering paper will name, and they differ in exactly one structural decision each, so each gets its defining condition stated rather than described.

> **Karnopp model, defined.** The **Karnopp model** is a *two-mode switched map*: a mode variable, stuck or slipping, plus one algebraic force law per mode. It has no continuous internal state at all, which is what separates it from the two below. Its defining condition is a **velocity dead-zone**: the mode is decided by $\lvert v\rvert<D_v$, and inside that band the velocity is *set to zero* and the friction force is whatever balances the applied tangential force, up to $F_s$.
>
> $$F_f=\begin{cases}-\operatorname{sat}_{F_s}(F_a), & \lvert v\rvert<D_v\quad\text{(stuck; and $v$ is set to $0$)}\\[2pt] -\big(F_d\,\mathrm{sgn}(v)+b_t v\big), & \lvert v\rvert\ge D_v\quad\text{(slipping)}\end{cases}$$
>
> where $F_a$ is the applied tangential force, $F_s$ the static limit, $F_d$ the dynamic (Coulomb) level, $b_t$ the tangential viscous coefficient, $D_v$ the dead-zone half-width and $\operatorname{sat}_{F_s}(\cdot)$ clipping at $\pm F_s$ — and the dead-zone exists **because** exact zero velocity never occurs in sampled data, so a model that tested $v=0$ would never stick.
> - **Example**: the $F_s=3.5$, $F_d=3.0$, $b_t=10$ wall of the box above. A $2$ N sideways push is inside the saturation, so the rendered force is exactly $2$ N opposing and the point does not move; a $5$ N push breaks free and at $v=0.05$ m/s the friction is $3.5$ N, leaving $1.5$ N of net drive. The whole sensation of "grip" is the $F_s-F_d=0.5$ N gap and the instant of the switch.
> - **Non-example**: Coulomb friction $-F_d\,\mathrm{sgn}(v)$ on its own. It has no stuck mode, so it chatters about zero velocity instead of holding, and a surface rendered with it cannot be rested on.
> - **Why it matters**: it is cheap, it has no state to integrate, and $D_v$ is a knob with a physical meaning you can set from the encoder — but the dead-zone is also a lie about pre-sliding: inside it the point is rigidly fixed, where a real contact deflects elastically. That is the deficiency the next two models exist to remove.

> **Dahl model, defined.** The **Dahl model** is a *first-order ODE in one internal state* — a bristle deflection $z$ that behaves like a stiff spring saturating at the Coulomb level. There is no mode variable and no switch; the force is continuous in time. Its defining condition is that friction is a function of **displacement**, not of velocity: $z$ integrates $v$ rather than tracking it, so a reversal at any speed retraces the same curve.
>
> $$\dot z=v-\frac{\sigma_0\lvert v\rvert}{F_c}\,z,\qquad F_f=\sigma_0 z,\qquad z_{ss}=\frac{F_c}{\sigma_0}$$
>
> where $z$ is the bristle deflection in metres, $\sigma_0$ the bristle stiffness in N/m, $F_c$ the Coulomb level and $z_{ss}$ the steady-state deflection reached in full slip — so the model is exactly the Stribeck-free special case of the LuGre family, with the velocity-dependent $g(v)$ of that family frozen at the constant $F_c$.
> - **Example**: $\sigma_0=10^{5}$ N/m with $F_c=3.0$ N gives $z_{ss}=3.0/10^{5}=3.0\times10^{-5}$ m, or $30\,\mathrm{\mu m}$ of pre-sliding displacement. On P3 that is $30/61.4=0.49$ encoder counts ([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §4]]) — the entire elastic regime this model adds sits *below* the device's resolution, which is worth knowing before claiming a device renders it.
> - **Non-example**: Karnopp's stuck mode. There the deflection is identically zero and the force is set by force balance; here the force is set by an accumulated displacement, and the two give different answers to the same small push.
> - **Why it matters**: it renders pre-sliding, which is what makes a surface feel like it is held rather than latched — and it **drifts**: under a small oscillating tangential force whose amplitude never reaches $F_c$, integrating $\dot z$ leaves a slow net creep, so a stuck object slides away over minutes. That drift is the defect the next model was built to fix.

> **Elasto-plastic model, defined.** The **elasto-plastic model** is a *bristle model with a partitioned deflection*: the same internal state $z$ as Dahl, but with its rate split into a reversible (elastic) part and an irreversible (plastic) part by a switching function $\alpha$. Its defining condition is that partition — $\alpha(z,v)=0$ while the deflection is small, so the bristle is **purely elastic and stores no permanent displacement**, and $\alpha$ rises to $1$ only once the deflection approaches its steady-state value.
>
> $$\dot z=v\left[1-\alpha(z,v)\,\mathrm{sgn}(v)\,\frac{z}{z_{ss}(v)}\right],\qquad \alpha=0\ \text{for}\ \lvert z\rvert\le z_{ba},\qquad \alpha=1\ \text{for}\ \lvert z\rvert\ge z_{ss}$$
>
> where $z_{ba}$ is the breakaway deflection at which plastic flow begins and $z_{ss}(v)$ the steady-state deflection — and setting $\alpha\equiv1$ recovers the LuGre/Dahl form above, which is the cleanest way to see that the partition is the only thing being added.
> - **Example**: with $z_{ss}=30\,\mathrm{\mu m}$ as above and $z_{ba}=0.3\,z_{ss}=9\,\mathrm{\mu m}$, any tangential motion under $9\,\mathrm{\mu m}$ is fully reversible: release the force and the point returns exactly where it was, so no drift can accumulate however long the oscillation runs.
> - **Non-example**: Dahl or LuGre with the same $\sigma_0$ and $F_c$. Identical in full slip, and different precisely in the presliding band, which is the band the drift lives in.
> - **Why it matters**: it is the model to reach for when the object must *stay put* — a virtual fixture, a held tool, a peg resting in a hole over seconds — and it costs one extra state comparison per period over Dahl. The haptics-specific variant that removes the same drift is the Hayward–Armstrong model cited above.

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

### Problem set · 과제

Tier B. Using **P3** from [[02-foundations/lab-plants|0.6]]. Catalog wall $k_w=400$, $x_w=0.030$. Replace the half-space with a *plate* of thickness $4\,\mathrm{mm}$ occupying $x\in[0.030,0.034]$. The Euler lab stays on [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]] — do not start a second simulator.

1. **Draw.** Handle $x$, plate, mid-plane at $0.032$. Two pictures at $x=0.036$: penalty (nearest-surface force, arrow *out the back*) and proxy (proxy stuck on the entry face $x_w$, spring $k_w(x_{\mathrm{proxy}}-x)$).
2. **Derive.** (a) Penalty force just before the mid-plane, and the push that pops through. (b) Proxy force at $x=0.036$. (c) Colgate bound $2b/T$ at $T=10^{-3}$. At that ceiling, does a $2\,\mathrm{N}$ push (the 24.3 amplifier limit) still pop a $4\,\mathrm{mm}$ plate? A $2\,\mathrm{mm}$ plate?
3. **Interpret.** Why is the 24.4 half-space wall honest as a penalty law, and why does the same law lie on this plate? What memory does the proxy add that a 1-DoF *half-space* never needed?

> [!tip]- Solutions
> 1. Penalty at $x=0.036$ is $2\,\mathrm{mm}$ past mid-plane, nearest face is $x=0.034$, force points $+x$ (out the back). Proxy remains at $0.030$, spring pulls $-x$.
> 2. (a) $k_w\cdot 0.002=0.80\,\mathrm{N}$; any harder push pops through. (b) $400\cdot(0.030-0.036)=-2.4\,\mathrm{N}$. (c) $2b/T=1600\,\mathrm{N/m}$. Ceiling force before mid-plane is $K\cdot(\mathrm{thickness}/2)$: $4\,\mathrm{mm}$ plate $\to 3.2\,\mathrm{N}$ (a $2\,\mathrm{N}$ push survives); $2\,\mathrm{mm}$ plate $\to 1.6\,\mathrm{N}$ (it pops). The bound is not why catalog penalty fails here — missing state is.
> 3. A half-space has one face; nearest-surface is always the entry face, so penalty and proxy coincide. A plate has two faces; without memory the force flips at the mid-plane. The proxy remembers the entry face.

## 한국어

> [!note] 처음이라면 · First pass
> 아래 대상과 계산을 먼저 읽어라. 핸들 하나, 얇은 판 하나, 그리고 렌더링 알고리즘에 기억이 필요한지를 정하는 힘 넷이다. 그다음 그 힘들이 나온 두 알고리즘인 §2와 §3. §4–§6은 그 위에 얹는 표면 특성이고, §7은 남이 쓴 같은 이야기를 읽는 법이다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P3**. 무엇에 닿는지만 하나 바꾼다. 카탈로그의 반공간 벽 대신 **유한한 두께의 판**을 쓰는데, 이 페이지의 모든 알고리즘이 의견이 일치하는 유일한 모양이 바로 반공간이기 때문이다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $k_w$ | $400\,\mathrm{N/m}$ | 카탈로그 벽 강성. 렌더링 강성 $K$로 그대로 쓴다 |
| $x_w$ | $0.030\,\mathrm{m}$ | 판의 **진입** 면; $+x$가 판 안 |
| 두께 | $4\,\mathrm{mm}$ | 판은 $x\in[0.030,\ 0.034]$, 중간면은 $0.032$ |
| $b$ | $0.8\,\mathrm{N{\cdot}s/m}$ | 장치 댐핑. 24.4의 천장 $2b/T=1600\,\mathrm{N/m}$을 인용할 때만 쓴다 |
| $F^{\max}$ | $2.0\,\mathrm{N}$ | P3 증폭기가 낼 수 있는 최대 핸들 힘. 유도는 [[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3 §3]] |

판의 두께가 이 페이지가 고정한 숫자이고 나머지는 전부 카탈로그다. 두께 $2\,\mathrm{mm}$도 한 번 쓰는데, 논증의 부호가 바뀌는 자리를 보이기 위해서다.

*범위: 이 페이지는 안정성 천장 **안에서** 루프가 무엇을 계산하는지를 가르친다 — 기하가 힘이 되는 방식, 반공간보다 얇은 것에서 상태 없는 힘 법칙이 실패하는 이유, proxy가 더하는 것, 그리고 그 위에 얹는 표면 특성(댐핑, 마찰, 질감). 천장이 왜 있는지는 가르치지 않는다. 그것은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]다. 힘을 모터로 보내는 $J^\top$ 단계도 아니다. 그것은 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]이다. §4의 지각적 트릭에 정신물리 실험을 설계하는 법도 아니다. 그것은 [[04-robotics/haptics-teleoperation/human-haptics-psychophysics|24.1]]이다.*

### 과제가 그릴 그림 · Homework diagram

*같은* 순간의 그림 둘을 나란히. 과제가 요구하는 것이 정확히 이 둘이다.

**왼쪽 — 벌점.** $x$축을 가로로, 판을 $0.030$에서 $0.034$까지의 음영 띠로, 중간면 $0.032$를 그 안을 지나는 점선으로. 장치 점을 먼 면 바깥 $x=0.036\,\mathrm{m}$에 둔다. 힘을 $+x$ 방향 화살표로 — 사용자가 들어온 쪽의 *반대*로 — 그리고 $0.80\,\mathrm{N}$이라 적는다. 옆에 그 화살표가 따르는 규칙 "가장 가까운 면 쪽"을 쓰고, 그게 어느 면인지 표시한다.

**오른쪽 — proxy.** 같은 띠, 같은 장치 점 $0.036$. 이번에는 *진입 면* $0.030$에 앉은 속 빈 점 하나를 더 그리고 $p_{\text{proxy}}$라 적는다. 두 점 사이의 스프링과 $-x$ 방향 힘 화살표를 그리고 $2.4\,\mathrm{N}$이라 적는다. 옆에 이 화살표의 규칙 "proxy 쪽"을 쓰고, 점이 들어온 뒤로 proxy가 움직이지 않았다는 것을 적는다.

**둘 아래에** 공유하는 축 하나: $x_w=0.030$, 중간면 $0.032$, 먼 면 $0.034$, 장치 점 $0.036$을 축척대로 표시해서, 두 화살표가 같은 기하를 읽고 다른 답을 내고 있다는 것이 보이게 한다. 두 힘은 $3.2\,\mathrm{N}$ 차이로 서로 반대를 가리키고, 그것이 §3의 논증 전체다.

### 대상으로 한 번 끝까지 · Worked case

위 판에 대해 다섯 단계. 전부 카탈로그 숫자이고, 페이지가 정한 숫자는 두께 하나다.

**1단계 — 벌점 법칙과 그 천장.** 진입 면에서의 침투는 $d=x-x_w$이므로 장치 점이 앞쪽 절반에 있는 동안 힘은 $-Kd$로 선형으로 자란다. 점이 중간면에 닿기 전까지 판이 낼 수 있는 최대 힘은 따라서

$$F_{\text{ceil}}=K\cdot\frac{\text{두께}}{2}=400\cdot 0.002=0.80\,\mathrm{N}$$

인데, 중간면을 지나면 *가장 가까운* 면이 더 이상 사용자가 들어온 면이 아니고 §2의 셋째 실패가 넘겨받기 때문이다. $2.0\,\mathrm{N}$을 낼 수 있는 P3의 증폭기에 대해 작정한 가압은 이 천장의 $2.5$배다. 카탈로그 벽은 이 판을 버티지 못한다.

**2단계 — 뚫고 나간 뒤의 벌점 힘.** $x=0.036\,\mathrm{m}$에서 가장 가까운 면은 $0.034$의 먼 면이므로, 벌점 법칙은 *그쪽*에서 $0.002\,\mathrm{m}$의 침투를 재고 점을 뒤로 더 밀어낸다.

$$F_{\text{penalty}}=+K\cdot(0.036-0.034)=+400\cdot0.002=+0.80\,\mathrm{N}$$

1단계와 크기는 같고 방향은 반대다. 알고리즘은 아무것도 망가지지 않았다. 힘 법칙은 자기가 말한 그대로를 하고 있고, 그 말이 틀렸을 뿐이다.

**3단계 — 같은 순간의 proxy 힘.** 알고리즘에 상태 변수 하나를 준다. 판 밖에 머물도록 제약되고, 주기마다 제약이 허락하는 만큼 장치 점 쪽으로 움직이는 proxy다(§3). 그것은 $x_w$로 들어왔고 판을 통과할 수 없으므로 여전히 $0.030$에 있고, 렌더링되는 힘은 두 점 사이의 스프링이다.

$$F_{\text{proxy}}=K\,(x_{\text{proxy}}-x)=400\cdot(0.030-0.036)=-2.4\,\mathrm{N}$$

손을 들어온 길로 되당긴다. 같은 기하, 같은 강성, 같은 순간에 두 알고리즘은 $3.2\,\mathrm{N}$과 부호 하나만큼 다르고, 둘의 차이는 기억한 숫자 하나뿐이다.

**4단계 — 대신 강성으로 벌점 법칙을 구할 수 있나?** 거꾸로 물어보자. 이 판에서 $F_{\text{ceil}}$이 증폭기의 $2.0\,\mathrm{N}$을 넘으려면 벌점 방법은

$$K\ \ge\ \frac{F^{\max}}{\text{두께}/2}=\frac{2.0}{0.002}=1000\,\mathrm{N/m}$$

을 요구하는데, $T=10^{-3}$에서 24.4의 천장 $2b/T=1600\,\mathrm{N/m}$ 안쪽이다. 그러니 $4\,\mathrm{mm}$ 판에서는 더 단단한 벌점 벽이 정말로 문제를 고친다. 판을 $2\,\mathrm{mm}$로 줄이면 같은 계산이 $2.0/0.001=2000\,\mathrm{N/m}$을 요구하고, 이것은 그 천장 *바깥*이다. P3에서 쓸 수 있는 어떤 주기·이득·조정으로도 닿지 않는다.

**5단계 — 4단계가 실제로 증명한 것을 읽어라.** 어떤 장치에서는 상태 없는 알고리즘을 강성으로 구할 수 없게 되는 두께가 있고, $1\,\mathrm{kHz}$의 P3에서 그 두께는 $2$와 $4$ 밀리미터 사이에 있다. 그보다 두꺼우면 벌점과 proxy 중 무엇을 쓸지는 공학적 취향이고, 그보다 얇으면 어떤 강성에서도 둘 중 proxy만 작동한다. §3이 더 잘 조정한 알고리즘이 아니라 다른 알고리즘인 이유가 그것이고, [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]의 카탈로그 반공간이 그 선택을 할 필요가 없었던 이유도 그것이다. 반공간은 면이 하나라 "가장 가까운 면"과 "진입 면"이 같은 답이고 두 법칙이 정확히 일치한다.

### 1. 루프가 실제로 계산하는 것

임피던스형 햅틱 루프는 서보 주기마다 같은 네 가지를 한다. 장치 위치를 읽고, 사용자의 점이 가상 환경의 무언가에 닿았는지 판단하고, 닿았다면 힘을 계산하고, 그 힘을 $J^\top$로 모터에 보낸다([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]). [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]는 넷째 단계의 안정성을 다룬다. 이 페이지는 둘째와 셋째 단계, 즉 기하를 힘으로 바꾸는 *알고리즘*을 다룬다.

사실 하나가 전부를 결정한다. 임피던스 장치에서는 아무것도 강체가 아니다. 모든 접촉은 스프링 $F = Kx$이고, $K$는 장치와 샘플링 주기가 상한을 정한다. 그러니 설계 질문은 "강체 벽을 어떻게 렌더링하나"가 아니라 "무른 스프링을 어떻게 강체처럼 *느껴지게* 하나"다. 답은 세 계열로 나뉜다. 더 나은 기하(§2–§3), 지각적 트릭(§4), 그 위에 얹는 표면 특성(§5–§6).

### 2. 벌점 기반 렌더링

가장 단순한 알고리즘은 침투를 스프링 압축으로 다룬다. 단위 법선 $\hat n$이 점 $p_0$를 지나는 벽에 대해, 장치 점 $p$의 침투 깊이는 $d = (p_0 - p)\cdot\hat n$이고

$$F = \begin{cases} K\,d\,\hat n, & d > 0 \\ 0, & d \le 0 \end{cases}$$

가 점을 법선 방향으로 밀어낸다. 구는 $\hat n$이 중심에서 $p$를 향하고 $d = R - \lVert p - c\rVert$인 같은 식이다. 상자는 벽 여섯 개에서 가장 가까운 면을 고른 것이다. 힘이 위치만의 함수라서 상태가 없고, 싸고, 가장 먼저 쓰게 되는 코드다.

> **벌점 기반 렌더링의 정의.** **벌점 기반 렌더링**(penalty-based rendering)은 현재 장치 자세에서 힘으로 가는 *기억 없는 함수*다. 사상 $\mathbb{R}^3\to\mathbb{R}^3$이고 그 이상이 아니다. 상태를 가진 알고리즘이 아니며, 아래 세 실패는 그 사실의 귀결이지 버그가 아니다. 정의 조건 셋. 힘이 **현재 위치에만** 달려 있으므로 같은 위치는 어떻게 도달했든 언제나 같은 힘을 낸다. 물체 **밖에서 0**이고 안에서는 침투량에 비례하므로, 기울기가 불연속인 곳은 물체의 경계뿐이다. 그리고 방향은 **가장 가까운** 표면점의 바깥 법선인데, 이는 주기마다 처음부터 다시 내리는 순수 기하학적 선택이다.
>
> $$F(p)=K\max\!\big(d(p),\,0\big)\,\hat n(p),\qquad d(p)=(p_0-p)\cdot\hat n,\qquad \hat n(p)=\hat n\big(\arg\min_{q\in\partial\mathcal{O}}\lVert q-p\rVert\big)$$
>
> $p$는 장치 점, $\mathcal{O}$는 물체, $\partial\mathcal{O}$는 그 표면, $d$는 법선을 따른 침투 깊이, $K$는 렌더링 강성이다. 세 실패를 모두 나르는 것은 *셋째* 인자, 즉 주기마다 다시 푸는 최근접점 argmin이다. 최소점이 한 샘플과 다음 샘플 사이에 면을 건너뛸 수 있기 때문이다.
>
> - **예**: [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §1]]의 반공간. 면이 하나라 argmin에 고를 것이 없고, 거기서 벌점 법칙은 근사가 아니라 정확하다.
> - **비예**: 계산 절의 $4\,\mathrm{mm}$ 판. 면이 둘이라 중간면을 지나면 argmin이 먼 면을 돌려주고 힘이 $+0.80\,\mathrm{N}$으로 뒤집힌다. 성능이 완만하게 나빠진 것이 아니라, 법칙이 다른 물체의 답을 계산한 것이다.
> - **비예**: 감쇠 항 $-B v_n$을 더한 벌점 힘(§5). 거기에는 속도가 있으므로 더 이상 위치만의 함수가 아니다. "벌점"이 이름 붙이는 것은 *위치* 부분이고 감쇠는 따로 정당화해야 하는 별개의 추가라는 것을 상기시켜 준다.
> - **왜 중요한가**: 상태가 없다는 바로 그 성질이 임의의 기하에서 1 kHz로 돌 수 있을 만큼 싸게 만들고, 바로 그 성질이 면 둘이 가까운 무엇에서든 틀리게 만든다. §3의 모든 알고리즘은 그 성질을 포기하고 산 것이다.

> [!example] 계산 예제 · Worked example
> $x$축에서 45° 기울어진 벽, $K = 500$ N/m, 장치 점이 벽 안쪽 $3$ mm. 침투는 법선을 따라 재므로 $F = 500 \times 0.003 = 1.5$ N이 $\hat n = (\cos 45°, \sin 45°)$ 방향으로 걸리고, $x$와 $y$ 성분은 각각 약 $1.06$ N이다. 사용자는 표면에 수직인 힘 하나를 느끼고, 장치는 그것을 $J^\top$를 거쳐 모터 토크 둘로 만든다. 여기 *없는* 것을 보라. 벽을 따라 미끄러지는 것을 막는 힘이 전혀 없고, 그래서 벌점 벽은 얼음처럼 느껴진다(§5).

벌점 방법은 세 가지로 실패하고, Ruspini, Kolarov, Khatib(SIGGRAPH 1997)이 그 이름을 붙였다.

- **국소성의 결여.** 힘은 현재 위치에만 달려 있지 점이 어떻게 거기 왔는지와 무관하다. 두 면이 만나는 곳에서는 "가장 가까운 면"이 샘플마다 바뀔 수 있고, 힘의 방향이 뒤집힌다. 24.4 §1이 사용자를 옆으로 튕겨 내는 모서리로 언급한 것이 이것이다.
- **힘의 불연속.** 같은 뒤집힘이 힘의 계단을 만들고, 손은 그것을 실제 물체는 내지 않는 딸깍거림이나 걷어차임으로 느낀다.
- **얇은 물체의 pop-through.** 벌점 힘은 언제나 *가장 가까운* 면을 향한다. 얇은 벽의 중간을 지나 밀면 가장 가까운 면은 반대쪽이 되고, 알고리즘은 친절하게도 뒤로 밀어내 준다.

> [!example] 계산 예제 · Worked example
> 두께 $4$ mm의 가상 판을 $K = 1000$ N/m로 렌더링한다. 장치 점이 판의 중간면을 넘기 전까지 판이 낼 수 있는 최대 힘은 $K \times 2\,\text{mm} = 2$ N이다. $2$ N보다 세게 미는 사용자는 누구나 뚫고 들어가 반대쪽으로 밀려 나간다. $K$를 올리는 것은 24.4의 안정성 천장까지만 통하고, 판을 두껍게 하는 것은 보기에 이상해지기 전까지만 통한다. 같은 판을 P3의 카탈로그 $k_w = 400$ N/m로 렌더링하면 $0.80$ N밖에 버티지 못하는데, 계산 절이 거기서 시작한다.

### 3. 제약 기반 렌더링: proxy

해법은 알고리즘에 기억을 주는 것이다. 가상 물체의 표면 위에 머물도록 제약된 두 번째 점, **proxy**(Ruspini 외 1997) 또는 **god object**(Zilles & Salisbury, IROS 1995)를 둔다. 장치 점은 침투해도 되지만 proxy는 안 된다. 서보 주기마다 proxy는 제약이 허락하는 만큼 장치 점 쪽으로 움직이고 — 목표를 향해 걷다가 부딪힌 장애물을 따라 미끄러지는 탐욕적 계획기와 같은 발상이다 — 렌더링되는 힘은 둘 사이의 스프링이다.

$$F = K\,(p_{\text{proxy}} - p_{\text{device}})$$

> **Proxy(god object)의 정의.** **Proxy**는 *상태 변수*다. 서보 주기를 건너 들고 다니는 두 번째 점, 그리고 그것을 갱신하는 제약 최소화다. 힘 법칙이 아니며 위 식의 스프링은 그중 가장 작은 부분이다. 정의 조건 셋이고, 둘째가 운동을 연속으로 만드는 것이다. Proxy는 언제나 **비침투 집합** $\mathcal{C}$에 갇혀 있으므로 장치 점과 달리 물체 안으로 들어가지 않는다. 주기마다 **이전 자리에서 도달 가능한 범위 안에서** 장치 점에 가장 가까운 $\mathcal{C}$의 점으로 옮기는데, 이것은 전역 최근접점 질의가 아니라 제약 최소화이고 그 도달 가능성 조항이 곧 기억이다. 그리고 렌더링되는 힘은 장치 점에서 **proxy로** 가는 스프링이므로 방향이 언제나 물체 밖이고 결코 안쪽이 아니다.
>
> $$p^{\text{prox}}_k=\arg\min_{p\in\mathcal{C},\ p\ \text{는}\ p^{\text{prox}}_{k-1}\text{에서 도달 가능}}\lVert p-p^{\text{dev}}_k\rVert,\qquad F_k=K\big(p^{\text{prox}}_k-p^{\text{dev}}_k\big)$$
>
> $\mathcal{C}$는 모든 물체 바깥의 자유 공간, $p^{\text{dev}}_k$는 측정된 장치 점, $p^{\text{prox}}_k$는 proxy다. 제약 안의 첨자 $k-1$이 §2와의 차이 전부인데, 과거가 등장하는 자리가 거기뿐이기 때문이다.
>
> - **예**: $x=0.036$의 계산 절. Proxy는 여전히 진입 면 $0.030$에 있고 — 도달 가능성이 판을 가로질러 더 가까운 먼 면으로 가는 것을 금지한다 — 그래서 힘이 안쪽으로 $-2.4\,\mathrm{N}$이다. 상태 없는 법칙은 바깥쪽으로 $+0.80\,\mathrm{N}$을 줬다.
> - **비예**: 주기마다 전역 최근접 표면점을 잡아 놓고 proxy라 부르는 것. 그것은 단계만 늘린 벌점 법칙이다. 도달 가능성 조항을 빼면 그 "proxy"는 $\hat n$이 그랬듯 중간면에서 먼 면으로 뛴다.
> - **비예**: 1자유도 반공간. 거기서 $\mathcal{C}$는 반직선이고 제약 최소점은 언제나 그 유일한 경계점이므로, proxy와 벌점이 매 순간 같은 힘을 낸다. 24.4의 카탈로그 벽을 §2의 실패를 하나도 만나지 않고 벌점 형태로 쓸 수 있는 이유가 그것이다.
> - **왜 중요한가**: 접촉마다 저장하는 점 하나로 세 실패를 한꺼번에 풀고, 이 분야에서 가장 남는 거래다. **God object**(Zilles & Salisbury 1995)는 반지름이 0인 이상적인 점으로 본 이 구성이고, **virtual proxy**(Ruspini 외 1997)는 같은 점에 유한한 반지름을 주고 그 위에 마찰과 force shading을 얹은 것이다. 위의 정의 조건은 공유하고, 차이는 반지름이다.

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

렌더링 논문이 이름을 부를 셋이 이것들이고, 각각 구조적 결정 딱 하나에서 갈라진다. 그러니 서술 대신 각자의 정의 조건을 적는다.

> **Karnopp 모델의 정의.** **Karnopp 모델**은 *두 모드의 전환 사상*이다. 붙음/미끄러짐의 모드 변수 하나와 모드마다 하나씩의 대수적 힘 법칙이다. 연속인 내부 상태가 전혀 없고, 그것이 아래 둘과 갈리는 지점이다. 정의 조건은 **속도 사영역**(dead-zone)이다. 모드를 $\lvert v\rvert<D_v$로 판정하고, 그 띠 안에서는 속도를 *0으로 놓으며*, 마찰력은 $F_s$까지 가해진 접선 힘을 그대로 상쇄하는 값이 된다.
>
> $$F_f=\begin{cases}-\operatorname{sat}_{F_s}(F_a), & \lvert v\rvert<D_v\quad\text{(붙음; 그리고 $v$를 $0$으로)}\\[2pt] -\big(F_d\,\mathrm{sgn}(v)+b_t v\big), & \lvert v\rvert\ge D_v\quad\text{(미끄러짐)}\end{cases}$$
>
> $F_a$는 가해진 접선 힘, $F_s$는 정지 한계, $F_d$는 동(Coulomb) 수준, $b_t$는 접선 점성 계수, $D_v$는 사영역 반폭, $\operatorname{sat}_{F_s}(\cdot)$는 $\pm F_s$에서의 클리핑이다. 사영역이 있는 것은 샘플링된 데이터에서 정확한 0 속도가 결코 나오지 않기 **때문이고**, $v=0$을 검사하는 모델은 영영 붙지 못한다.
> - **예**: 위 상자의 $F_s=3.5$, $F_d=3.0$, $b_t=10$인 벽. 옆으로 $2$ N을 밀면 포화 안쪽이라 렌더링되는 힘은 정확히 $2$ N을 반대로 내고 점은 움직이지 않는다. $5$ N을 밀면 풀려서 $v=0.05$ m/s에 마찰이 $3.5$ N이 되고 순 구동력 $1.5$ N이 남는다. "그립"으로 느껴지는 모든 것이 $F_s-F_d=0.5$ N의 간격과 전환 순간이다.
> - **비예**: Coulomb 마찰 $-F_d\,\mathrm{sgn}(v)$ 단독. 붙음 모드가 없어서 0 속도 근처에서 버티는 대신 채터하고, 그것으로 렌더링한 표면에는 손을 얹어 쉴 수가 없다.
> - **왜 중요한가**: 싸고, 적분할 상태가 없고, $D_v$는 엔코더에서 값을 정할 수 있는 물리적 의미의 손잡이다. 그러나 사영역은 미끄러지기 전 거동에 대한 거짓말이기도 하다. 그 안에서 점은 강체처럼 고정되지만 실제 접촉은 탄성적으로 휜다. 다음 두 모델이 존재하는 이유가 그 결함이다.

> **Dahl 모델의 정의.** **Dahl 모델**은 *내부 상태 하나에 대한 1차 상미분방정식*이다. Coulomb 수준에서 포화하는 단단한 스프링처럼 거동하는 강모 변형 $z$다. 모드 변수도 없고 전환도 없으며 힘은 시간에 대해 연속이다. 정의 조건은 마찰이 속도가 아니라 **변위**의 함수라는 것이다. $z$는 $v$를 따라가는 것이 아니라 적분하므로, 어느 속도에서 방향을 바꿔도 같은 곡선을 되짚는다.
>
> $$\dot z=v-\frac{\sigma_0\lvert v\rvert}{F_c}\,z,\qquad F_f=\sigma_0 z,\qquad z_{ss}=\frac{F_c}{\sigma_0}$$
>
> $z$는 미터 단위의 강모 변형, $\sigma_0$는 N/m 단위의 강모 강성, $F_c$는 Coulomb 수준, $z_{ss}$는 완전 미끄럼에서 도달하는 정상 상태 변형이다. 그러므로 이 모델은 LuGre 계열에서 속도 의존 $g(v)$를 상수 $F_c$로 얼린, Stribeck 없는 특수한 경우다.
> - **예**: $\sigma_0=10^{5}$ N/m, $F_c=3.0$ N이면 $z_{ss}=3.0/10^{5}=3.0\times10^{-5}$ m, 즉 미끄러지기 전 변위가 $30\,\mathrm{\mu m}$다. P3에서 그것은 $30/61.4=0.49$ 엔코더 카운트이고([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3 §4]]), 이 모델이 더해 주는 탄성 영역 전체가 장치 해상도 *아래*에 있다. 장치가 그것을 렌더링한다고 주장하기 전에 알아 둘 값어치가 있다.
> - **비예**: Karnopp의 붙음 모드. 거기서 변형은 항등적으로 0이고 힘은 힘 평형으로 정해지는데, 여기서는 누적된 변위가 힘을 정한다. 같은 작은 가압에 두 모델이 다른 답을 낸다.
> - **왜 중요한가**: 미끄러지기 전 거동을 렌더링하고, 그것이 표면을 걸쇠로 잠긴 것이 아니라 붙들려 있는 것처럼 느끼게 한다. 그리고 **표류한다**. 진폭이 $F_c$에 닿지 않는 작은 진동 접선 힘 아래에서 $\dot z$를 적분하면 느린 순 이동이 남아, 붙어 있어야 할 물체가 몇 분에 걸쳐 흘러간다. 다음 모델이 고치려고 만들어진 결함이 그 표류다.

> **탄소성 모델의 정의.** **탄소성 모델**(elasto-plastic)은 *변형을 분할한 강모 모델*이다. Dahl과 같은 내부 상태 $z$를 쓰되, 그 변화율을 전환 함수 $\alpha$로 가역(탄성) 부분과 비가역(소성) 부분으로 나눈다. 정의 조건이 그 분할이다. 변형이 작은 동안 $\alpha(z,v)=0$이라 강모는 **순수 탄성이고 영구 변위를 저장하지 않으며**, $\alpha$는 변형이 정상 상태 값에 가까워질 때에만 $1$로 올라간다.
>
> $$\dot z=v\left[1-\alpha(z,v)\,\mathrm{sgn}(v)\,\frac{z}{z_{ss}(v)}\right],\qquad \alpha=0\ (\lvert z\rvert\le z_{ba}),\qquad \alpha=1\ (\lvert z\rvert\ge z_{ss})$$
>
> $z_{ba}$는 소성 흐름이 시작되는 breakaway 변형, $z_{ss}(v)$는 정상 상태 변형이다. $\alpha\equiv1$로 두면 위의 LuGre/Dahl 형태가 되는데, 더해진 것이 분할뿐임을 보는 가장 깔끔한 방법이다.
> - **예**: 위와 같이 $z_{ss}=30\,\mathrm{\mu m}$이고 $z_{ba}=0.3\,z_{ss}=9\,\mathrm{\mu m}$이면, $9\,\mathrm{\mu m}$ 미만의 접선 운동은 완전히 가역이다. 힘을 놓으면 점이 정확히 있던 자리로 돌아오므로 진동이 아무리 오래 이어져도 표류가 쌓이지 않는다.
> - **비예**: 같은 $\sigma_0$와 $F_c$의 Dahl 또는 LuGre. 완전 미끄럼에서는 동일하고, 정확히 미끄러지기 전 띠에서 다르다. 표류가 사는 곳이 그 띠다.
> - **왜 중요한가**: 물체가 *제자리에 있어야* 할 때 — 가상 고정구, 붙들고 있는 도구, 몇 초 동안 구멍에 놓인 펙 — 꺼내는 모델이고, Dahl보다 주기당 상태 비교 하나를 더 쓴다. 같은 표류를 없애는 햅틱 전용 변형이 위에 인용한 Hayward–Armstrong 모델이다.

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

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P3**. 카탈로그 벽 $k_w=400$, $x_w=0.030$. 반공간을 두께 $4\,\mathrm{mm}$의 *판* $x\in[0.030,0.034]$으로 바꿔라. 오일러 랩은 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4]]에 남긴다. 여기서 시뮬레이터를 하나 더 만들지 마라.

1. **그리기.** 핸들 $x$, 판, 중간면 $0.032$. $x=0.036$에서 그림 둘: 벌점(가장 가까운 면의 힘, 화살표가 *뒤로 나감*)과 proxy(진입 면 $x_w$에 붙은 proxy, 스프링 $k_w(x_{\mathrm{proxy}}-x)$).
2. **유도.** (a) 중간면 직전의 벌점 힘, 그리고 뚫고 나가는 가압. (b) $x=0.036$의 proxy 힘. (c) $T=10^{-3}$에서 Colgate 경계 $2b/T$. 그 천장에서 $2\,\mathrm{N}$ 가압(24.3 증폭기 한계)이 $4\,\mathrm{mm}$ 판을 아직 뚫는가? $2\,\mathrm{mm}$ 판은?
3. **해석.** 24.4의 반공간 벽이 벌점 법칙으로 정직한 이유, 같은 법칙이 이 판에서는 거짓인 이유는? 1자유도 *반공간*이 끝내 필요 없었던 기억을 proxy가 무엇을 더하는가?

> [!tip]- 정답 · Solutions
> 1. $x=0.036$의 벌점은 중간면을 $2\,\mathrm{mm}$ 지났고, 가장 가까운 면은 $x=0.034$, 힘은 $+x$(뒤로). Proxy는 $0.030$에 남아 스프링이 $-x$로 당긴다.
> 2. (a) $k_w\cdot 0.002=0.80\,\mathrm{N}$; 더 센 가압은 뚫고 나간다. (b) $400\cdot(0.030-0.036)=-2.4\,\mathrm{N}$. (c) $2b/T=1600\,\mathrm{N/m}$. 중간면 전 천장 힘은 강성에 반두께를 곱한 값이다: $K(4\,\mathrm{mm}/2)=3.2\,\mathrm{N}$이므로 $2\,\mathrm{N}$은 버티고, $K(2\,\mathrm{mm}/2)=1.6\,\mathrm{N}$이므로 뚫린다. 카탈로그 벌점이 여기서 실패하는 이유는 경계가 아니라 상태의 부재다.
> 3. 반공간은 면이 하나라 가장 가까운 면이 언제나 진입 면이고, 벌점과 proxy가 같다. 판은 면이 둘이라 기억 없이 중간면에서 힘이 뒤집힌다. Proxy가 진입 면을 기억한다.

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
