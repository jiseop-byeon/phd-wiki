---
title: 5. World Models
tags: [deep-learning, world-models, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Separate representation, transition, observation, reward, and planner; roll out a latent model, measure multi-step against one-step error, and diagnose model exploitation."
mastery-when: "Raise when learned dynamics, latent planning, uncertainty, or model-based data generation carries the contribution."
---

> [!note] Prerequisites · 선수 지식
> Object **D5** from [[03-deep-learning/lab-objects|0. Lab Objects]] · [[02-foundations/lab-kernel|0.7 Lab Kernel]], because this page is Tier A · [[02-foundations/probability|3. Probability]], [[02-foundations/rl-basics|7. RL]], and [[04-robotics/state-estimation-slam|3. State Estimation]].
> [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상 **D5** · 이 페이지는 Tier A이므로 [[02-foundations/lab-kernel|0.7 Lab Kernel]] · [[02-foundations/probability|3. Probability]], [[02-foundations/rl-basics|7. RL]], [[04-robotics/state-estimation-slam|3. State Estimation]].

## English

*Stands on the filter of [[04-robotics/state-estimation-slam|3. State Estimation]] and the return of [[02-foundations/rl-basics|7. RL]]. First use of object **D5**.*

> [!note] First pass
> Read the running object, the worked case, §§1–3, and problems 1–2. Return to §5 when a paper reports a rollout horizon or a one-step prediction loss, and read §6 before comparing two systems that are both called world models.

### Running object · 이 페이지의 대상

**D5** from [[03-deep-learning/lab-objects|0. Lab Objects]], at the numbers that page freezes: scalar latent dynamics $z_{t+1}=0.8z_t+0.5a_t$ and reward $r_t=-z_t^2-0.1a_t^2$. Start at $z_0=1$ and test actions $a_0=-1$, $a_1=0$:

$$z_1=0.3,\quad r_0=-1.1;\qquad z_2=0.24,\quad r_1=-0.09.$$

The model can compare candidate action sequences without executing them in the real world.

| Symbol | Value | What it is |
|---|---:|---|
| $\lambda$ | $0.8$ | true transition gain — how much of the state survives one step |
| $\beta$ | $0.5$ | true action gain, shared by every model on this page |
| $\hat\lambda$ | $0.9$ | the **learned** gain of §2: one-step error of $0.1z_t$, in the pessimistic direction |
| $\hat\lambda'$ | $0.7$ | a second learned gain, the same size of error pointing the *other* way |
| $z_0$ | $1$ | start state |
| $r_t$ | $-z_t^2-0.1a_t^2$ | reward, charged on the state *before* the action |
| $\mathcal A$ | $\{-1,-0.5,0,0.5,1\}$ | the action values a planner may choose from |

Two learned gains rather than one, because §3's whole question is which *direction* a model is wrong in, and a single wrong model cannot answer it.

*Scope: this page teaches how to take a world model apart into its five components, how the transition's error behaves when the model is iterated instead of checked one step at a time, and what a planner does with that error. It does not teach how the latent is learned — the objectives that fit an encoder and a transition are [[03-deep-learning/foundations/index|1. Learning Systems]]; nor how an observation model is inverted online on a real robot, which is [[04-robotics/state-estimation-slam|3. State Estimation]]; nor the generative decoder that turns a latent into pixels, which is [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]; nor the policy-gradient and value machinery a learned model is often wrapped in, which is [[02-foundations/rl-basics|7. RL]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 478" style="max-width:100%;height:auto" role="img" aria-label="D5's world model as a block diagram with the teacher-forced and free-running paths into the transition drawn separately, and below the two paths' outputs with zero actions: the true state 0.8 to the H, the free-running rollout 0.9 to the H and their gap, which is 0.26281 at H = 5 and peaks at 0.269297 at H = 6">
  <defs><marker id="aD5e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) the block diagram, D5's numbers</text>
  <rect x="170" y="32" width="236" height="26" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="288" y="49" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">planner: argmax over action sequences</text>
  <rect x="170" y="92" width="236" height="50" rx="5" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <text x="288" y="106" font-size="11" fill="currentColor" text-anchor="middle">transition</text>
  <text x="276.2" y="121" font-size="11" fill="currentColor" text-anchor="end">z′ =</text>
  <text x="283.3" y="121" font-size="11" fill="currentColor" text-anchor="middle">λ</text>
  <text x="286.5" y="121" font-size="11" fill="currentColor">z + βa</text>
  <path d="M 280.6 112.7 L 283.3 110.7 L 285.9 112.7" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round"/>
  <text x="276.6" y="136" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">true λ = 0.8 ·</text>
  <text x="283.7" y="136" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">λ</text>
  <text x="290.8" y="136" font-size="11" fill="currentColor" fill-opacity="0.8">= 0.9 · β = 0.5</text>
  <path d="M 281 127.7 L 283.7 125.7 L 286.3 127.7" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round" stroke-opacity="0.8"/>
  <line x1="288" y1="58" x2="288" y2="90" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD5e)"/>
  <text x="280" y="80" font-size="11" fill="currentColor" text-anchor="end">action a<tspan dy="3" font-size="10">t</tspan><tspan dy="-3" dx="3.5">∈ {−1, −½, 0, ½, 1}</tspan></text>
  <line x1="406" y1="117" x2="418" y2="117" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD5e)"/>
  <rect x="420" y="105" width="40" height="24" rx="12" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="440" y="121" font-size="11" fill="currentColor" text-anchor="middle">ẑ<tspan dy="3" font-size="10">t+1</tspan></text>
  <rect x="472" y="66" width="76" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="510" y="80.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">reward</text>
  <text x="510" y="95.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">−z² − 0.1a²</text>
  <rect x="472" y="132" width="76" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="4 3"/>
  <text x="510" y="146.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">decoder</text>
  <text x="510" y="161.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">optional</text>
  <path d="M460 117 L464 117 L464 84 L470 84" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aD5e)" stroke-linejoin="round"/>
  <path d="M464 117 L464 150 L470 150" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3" marker-end="url(#aD5e)" stroke-linejoin="round"/>
  <path d="M510 66 L510 45 L408 45" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aD5e)" stroke-linejoin="round"/>
  <rect x="12" y="170" width="96" height="24" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="60" y="186" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">observation o<tspan dy="3" font-size="10">t</tspan></text>
  <rect x="120" y="170" width="64" height="24" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="152" y="186" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">encoder</text>
  <line x1="108" y1="182" x2="118" y2="182" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD5e)"/>
  <path d="M184 182 L200 182 L200 144" stroke="currentColor" stroke-width="1.8" fill="none" marker-end="url(#aD5e)" stroke-linejoin="round"/>
  <text x="206" y="164" font-size="11" fill="currentColor">z<tspan dy="3" font-size="10">t</tspan></text>
  <text x="12" y="214" font-size="11" fill="currentColor">teacher forced: re-encode a real observation</text>
  <path d="M440 129 L440 182 L376 182 L376 144" stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="6 3" marker-end="url(#aD5e)" stroke-linejoin="round"/>
  <text x="370" y="164" font-size="11" fill="currentColor" text-anchor="end">ẑ<tspan dy="3" font-size="10">t</tspan></text>
  <text x="548" y="200" font-size="11" fill="currentColor" text-anchor="end">free running: feed the model its own output</text>
  <text x="12" y="246" font-size="12" fill="currentColor">(b) the two paths on D5: zero actions, z<tspan dy="3" font-size="10.2">0</tspan><tspan dy="-3" dx="3.8">= 1</tspan></text>
  <line x1="48" y1="438" x2="540" y2="438" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="48" y1="438" x2="48" y2="258" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="44" y1="438" x2="48" y2="438" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="442" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0</text>
  <line x1="44" y1="394" x2="48" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="398" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.25</text>
  <line x1="44" y1="350" x2="48" y2="350" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="354" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.5</text>
  <line x1="44" y1="306" x2="48" y2="306" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="310" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.75</text>
  <line x1="44" y1="262" x2="48" y2="262" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="266" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">1</text>
  <line x1="48" y1="438" x2="48" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="48" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <line x1="171" y1="438" x2="171" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="171" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">5</text>
  <line x1="294" y1="438" x2="294" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="294" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">10</text>
  <line x1="417" y1="438" x2="417" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="417" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">15</text>
  <line x1="540" y1="438" x2="540" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="540" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <text x="355.5" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">horizon H</text>
  <path d="M48 262 L72.6 297.2 L97.2 325.4 L121.8 347.9 L146.4 365.9 L171 380.3 L195.6 391.9 L220.2 401.1 L244.8 408.5 L269.4 414.4 L294 419.1 L318.6 422.9 L343.2 425.9 L367.8 428.3 L392.4 430.3 L417 431.8 L441.6 433 L466.2 434 L490.8 434.8 L515.4 435.5 L540 436" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M48 262 L72.6 279.6 L97.2 295.4 L121.8 309.7 L146.4 322.5 L171 334.1 L195.6 344.5 L220.2 353.8 L244.8 362.2 L269.4 369.8 L294 376.6 L318.6 382.8 L343.2 388.3 L367.8 393.3 L392.4 397.7 L417 401.8 L441.6 405.4 L466.2 408.6 L490.8 411.6 L515.4 414.2 L540 416.6" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="7 4" stroke-linejoin="round"/>
  <path d="M48 438 L72.6 420.4 L97.2 408.1 L121.8 399.8 L146.4 394.6 L171 391.7 L195.6 390.6 L220.2 390.7 L244.8 391.8 L269.4 393.4 L294 395.5 L318.6 397.9 L343.2 400.4 L367.8 402.9 L392.4 405.5 L417 408 L441.6 410.3 L466.2 412.6 L490.8 414.8 L515.4 416.8 L540 418.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.75" stroke-linejoin="round"/>
  <circle cx="72.6" cy="279.6" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="97.2" cy="311.3" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="121.8" cy="336.6" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="146.4" cy="356.9" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="171" cy="373.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="195.6" cy="386.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="220.2" cy="396.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="244.8" cy="404.8" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="269.4" cy="411.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="294" cy="416.7" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="318.6" cy="421" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="343.2" cy="424.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="367.8" cy="427.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="392.4" cy="429.3" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="417" cy="431" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="441.6" cy="432.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="466.2" cy="433.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="490.8" cy="434.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="515.4" cy="435.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="540" cy="435.7" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="195.6" cy="390.6" r="3.6" stroke="none" fill="currentColor"/>
  <line x1="171" y1="380.3" x2="171" y2="334.1" stroke="currentColor" stroke-width="1.6"/>
  <line x1="167" y1="380.3" x2="175" y2="380.3" stroke="currentColor" stroke-width="1.6"/>
  <line x1="167" y1="334.1" x2="175" y2="334.1" stroke="currentColor" stroke-width="1.6"/>
  <text x="68.9" y="431.8" font-size="11" fill="currentColor" fill-opacity="0.85">H = 1: δ = 0.1, the one-step error</text>
  <line x1="274.3" y1="260" x2="296.3" y2="260" stroke="currentColor" stroke-width="2"/>
  <text x="304.3" y="264" font-size="11" fill="currentColor">true z<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.8</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <circle cx="285.3" cy="278.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="304.3" y="282.5" font-size="11" fill="currentColor">teacher forced 0.9·z<tspan dy="3" font-size="10">H−1</tspan></text>
  <line x1="274.3" y1="297" x2="296.3" y2="297" stroke="currentColor" stroke-width="2" stroke-dasharray="7 4"/>
  <text x="304.3" y="301" font-size="11" fill="currentColor">free running ẑ<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.9</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <line x1="274.3" y1="315.5" x2="296.3" y2="315.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75"/>
  <text x="304.3" y="319.5" font-size="11" fill="currentColor">gap δ<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.9</tspan><tspan dy="-4" font-size="10">H</tspan><tspan dy="4" dx="3.5">− 0.8</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <line x1="285.3" y1="328" x2="285.3" y2="340" stroke="currentColor" stroke-width="1.6"/>
  <line x1="281.3" y1="328" x2="289.3" y2="328" stroke="currentColor" stroke-width="1.6"/>
  <line x1="281.3" y1="340" x2="289.3" y2="340" stroke="currentColor" stroke-width="1.6"/>
  <text x="304.3" y="338" font-size="11" fill="currentColor">H = 5: 0.59049 − 0.32768 = 0.26281</text>
  <circle cx="285.3" cy="352.5" r="3.6" stroke="none" fill="currentColor"/>
  <text x="304.3" y="356.5" font-size="11" fill="currentColor">peak H = 6: 0.269297</text>
  <text x="304.3" y="375" font-size="11" fill="currentColor">H = 20: δ/z = 9.545</text>
</svg>

D5's world model as a block diagram — observation, encoder, the transition $z'=\hat\lambda z+\beta a$ with $\hat\lambda=0.9$ against the true $\lambda=0.8$ and $\beta=0.5$, a reward $-z^2-0.1a^2$ hanging off the latent, an optional decoder, and a planner that picks the action — with the two paths into the transition drawn apart: teacher forced (a real observation re-encoded every step) and free running (the model fed its own output). Below, with zero actions from $z_0=1$, the teacher-forced prediction $0.9z_{H-1}$ is never more than one step's error from the truth $0.8^H$ ($\delta=0.1$ at $H=1$), while the free-running rollout $0.9^H$ drifts away: the gap $\delta_H=0.9^H-0.8^H$ is $0.26281$ at $H=5$, peaks at $0.269297$ at $H=6$, and at $H=20$ is $9.545$ times the true state.

### Worked case · 대상으로 한 번 끝까지

This is the homework object. The problem set will ask you to draw it, derive the error recursion, and sweep the horizon. Do all three here first on the catalog numbers.

**Two candidate plans, by hand.** From $z_0=1$ with no discount, the sequence $(-1,0)$ gives $z_1=0.8(1)+0.5(-1)=0.3$ and $z_2=0.8(0.3)=0.24$, so the return is $(-1^2-0.1\cdot1)+(-0.3^2-0)=-1.1-0.09=-1.19$. The sequence $(0,0)$ gives $z_1=0.8$, $z_2=0.64$ and a return of $-1-0.64=-1.64$. Acting is worth $0.45$ of return here, and the model found that out without touching the plant.

**The error recursion, which is the page's one derivation.** Let $\delta_t=\hat z_t-z_t$ be the gap between a free-running model and the truth, with $\delta_0=0$ because both start from the same measured state. Subtracting the two updates,

$$\delta_{t+1}=\hat\lambda\hat z_t-\lambda z_t=\hat\lambda\,\delta_t+(\hat\lambda-\lambda)\,z_t,$$

so the gap has two parts: the fresh one-step error $e_t=(\hat\lambda-\lambda)z_t$, which is exactly what a teacher-forced validation loss sees, and the old gap carried forward through the model's *own* gain. Unrolling,

$$\delta_H=\sum_{t=0}^{H-1}\hat\lambda^{\,H-1-t}\,e_t,$$

because each one-step error, once made, is propagated by every later application of $\hat\lambda$. That single line is why a one-step loss cannot bound a rollout: the loss reports $e_t$ and the rollout reports a filtered sum of all of them. If every $e_t$ had the same size $e$, the sum would be $e\,(1-\hat\lambda^H)/(1-\hat\lambda)$, which for $\hat\lambda=0.9$ approaches $10e$ — a model that is 1% wrong per step can be 10% wrong at the end. The sum is a convolution of the one-step errors with the kernel $\hat\lambda^{m}$, $m$ being an error's age: the linear state-space model of [[03-deep-learning/foundations/sequence-models|1.1 Sequence Models §7]], which reads D5 itself as the same kind of linear recurrent network.

**The closed form on D5.** With zero actions, $z_t=0.8^t$ and $e_t=0.1\cdot0.8^t$, so the sum telescopes to

$$\delta_H=0.9^H-0.8^H.$$

At $H=5$ that is $0.59049-0.32768=0.26281$, which is the §2 number; at $H=1$ it is $0.1$, the one-step error itself. Check one value by hand and then let §5 sweep it.

**And the trap in the same formula.** $\delta_H$ does not grow forever. It peaks at $H=6$ ($0.269297$) and then falls, because both trajectories are decaying to zero and there is eventually nothing left to be wrong about. Measured against what remains of the state, $\delta_H/z_H=(9/8)^H-1$, which is $9.545$ at $H=20$ — the model is off by ten times the state it is predicting while its absolute error is shrinking. Which of those two curves a paper plots is a choice you should make before you read its rollout figure.

### 1. A world model is several models

| Component | Question |
|---|---|
| encoder/inference | what latent state explains observations? |
| transition | how do state and action change it? |
| observation decoder | what would sensors see? |
| reward/termination | what task signal and ending follow? |
| policy/planner | which imagined action sequence should be chosen? |

Some papers omit a pixel decoder and predict representations; others generate video but never use it for control. "World model" does not itself imply planning or physical consistency.

The second row is the one this page computes with, and it carries three conditions that the phrase "learned dynamics" hides.

> **Latent dynamics, defined.** **Latent dynamics** is a *map on a learned state space together with that space* — a function $f_\phi$ and the set it acts on — not a network architecture and not a prediction of observations. Three defining conditions. The state is **latent**: inferred from observations rather than measured, so it is pinned down only as far as the training objective pins it down, and nothing forces it to be interpretable or metric. The map is **action-conditioned**, $z_{t+1}=f_\phi(z_t,a_t)$, which is what separates a controlled model from a video model. And it is **closed**: the output lives in the same space as the input, so it can be iterated with no encoder and no decoder in the loop, which is the property that makes an imagined rollout possible at all.
>
> $$z_{t+1}=f_\phi(z_t,a_t),\qquad \text{D5: } f(z,a)=0.8z+0.5a$$
>
> where $z_t$ is the latent state, $a_t$ the action, and $\phi$ the learned parameters — and "closed" is the condition doing the work in the rollout above, because it is what lets $\delta_t$ accumulate inside the latent instead of being reset by a fresh observation.
>
> - **Example**: D5. One scalar, one gain, one action gain, and every claim on this page is about the iterate of that map.
> - **Non-example**: an observation-space predictor $\hat o_{t+1}=g(o_{\le t},a_t)$ that decodes and re-encodes at every step. It may be equivalent in principle, but it is not closed in a latent, so its rollout error contains the decoder's error too and the two cannot be separated from its curves.
> - **Non-example**: a representation trained by masked or contrastive prediction with no action input. It can be an excellent encoder and still fail condition two, which means it cannot answer "what happens if I do this" — the only question a planner asks.
> - **Why it matters**: conditions one and three together are exactly why a low one-step loss does not bound a rollout. The loss is evaluated on states the *encoder* supplied; the rollout is evaluated on states the *map* supplied, and §5 is the measurement of how far apart those two become.

### 2. Multi-step error matters

Suppose the learned coefficient is $0.9$ rather than $0.8$. With zero actions and $z_0=1$, true state after 5 steps is $0.8^5=0.328$ while the model predicts $0.9^5=0.590$. Small one-step bias compounds. Evaluate rollout horizon and downstream decisions, not only one-step loss.

### 3. Planning can exploit model errors

An optimizer searches specifically for trajectories the model rates highly. It can find unrealistic blind spots outside the training distribution. Ensembles, uncertainty penalties, short horizons, replanning, conservative objectives, and real-data correction limit—not eliminate—this problem.

That paragraph names a phenomenon that is often used loosely, and the loose use hides which of its conditions a proposed fix actually breaks.

> **Model exploitation, defined.** **Model exploitation** is a property of a *planner–model pair*, not of a model: it is the bias introduced by maximizing a return that is computed under an approximation. Three defining conditions. The quantity maximized is the **model's** return, so model error enters the *selection* of a plan and not merely the prediction of one. The model must be **optimistic somewhere the optimizer can reach** — a model that is wrong in the pessimistic direction everywhere cannot be exploited, only wasted. And the selected plan must be **executed**, which is when the difference between the predicted and the realized return is actually paid.
>
> $$\text{gap}=\hat J(a^\star_{\hat f})-J(a^\star_{\hat f}),\qquad \text{regret}=J(a^\star_{f})-J(a^\star_{\hat f}),\quad a^\star_{g}=\arg\max_{a_{0:H-1}}J_g$$
>
> where $J$ is the true return of a plan, $\hat J$ the model's return, $f$ the true dynamics and $\hat f$ the learned ones — two different numbers that papers often merge, since the gap is what the *model* was wrong about and the regret is what the *robot* lost.
>
> - **Example**: D5 planned five steps ahead with $\hat\lambda'=0.7$. The model promises $-1.1739$, the plant delivers $-1.3081$: a gap of $+0.1341$, and a regret of $0.0929$ against the best plan on the same action grid.
> - **Non-example**: the same-sized error pointing the other way, $\hat\lambda=0.9$. Its gap at $H=5$ is $-0.0996$ — the plant does *better* than promised — and its regret is $0$ on this grid. A wrong model is not automatically an exploited one, and a paper reporting only "our model has 0.1 one-step error" has not told you which of these two cases it is in.
> - **Non-example**: the rollout error of §2 with no planner attached. Nothing selected for it; it is prediction error, and calling it exploitation makes the fix unfindable.
> - **Why it matters**: each remedy in the paragraph above attacks exactly one of the three conditions, so naming the condition tells you the cost. Replanning attacks the third — and on D5 it is free: §5 shows every one of these models scoring the same $-1.2153$ once the plan is re-solved after each step.

### 4. Read claims by use

Representation learning asks whether latents preserve useful state. Prediction asks whether future observations/states are calibrated. Control asks whether imagined rollouts improve real return or success. Generation quality alone answers none of the other two.

Read [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]], [[01-canonical-papers/notes/5-world-models/jepa|JEPA]], [[01-canonical-papers/notes/5-world-models/genie|Genie]] and [[01-canonical-papers/notes/5-world-models/world-labs|World Labs]] with this component table, and §6 before comparing two systems that both call themselves world models.

### 5. The horizon sweep

Three measurements on one object: how the free-running error compares with the one-step error it is made of, what a planner loses to each of the two wrong gains, and what replanning costs and recovers. The action grid is $\mathcal A$, so the planner enumerates $5^H$ sequences and no optimizer choice is hiding in the result.

```python
import itertools
import numpy as np

lam, beta, z0 = 0.8, 0.5, 1.0          # D5, true transition and start
GRID = (-1.0, -0.5, 0.0, 0.5, 1.0)     # the actions the planner may choose from

def roll(lm, acts, z=z0):              # states z_0 ... z_H under transition lm
    out = [z]
    for a in acts:
        z = lm * z + beta * a
        out.append(z)
    return out

def ret(zs, acts):                     # sum_{t<H} -z_t^2 - 0.1 a_t^2
    return sum(-zs[t] ** 2 - 0.1 * acts[t] ** 2 for t in range(len(acts)))

for H in (1, 2, 3, 5, 6, 10, 20):      # 1. free running vs teacher forced
    acts = [0.0] * H
    zt, zm = roll(lam, acts), roll(0.9, acts)
    free = abs(zm[H] - zt[H])
    one = abs((0.9 - lam) * zt[H - 1])
    print(f"{H:>2} {zt[H]:10.6f} {zm[H]:10.6f} {free:9.6f} {one:9.6f} "
          f"{free/one:6.2f} {free/zt[H]:7.3f}")

for H in (2, 3, 4, 5):                 # 2. plan through a wrong model, execute open loop
    plans = list(itertools.product(GRID, repeat=H))
    true_r = np.array([ret(roll(lam, p), p) for p in plans])
    row = []
    for lm in (0.9, 0.7):
        mod_r = np.array([ret(roll(lm, p), p) for p in plans])
        j = int(mod_r.argmax())
        row += [true_r.max() - true_r[j], mod_r[j] - true_r[j]]
    print(H, [round(v, 4) for v in row])

def mpc(lm, H, steps=10):              # 3. the same plans, re-solved after every step
    plans = list(itertools.product(GRID, repeat=H))
    z, total = z0, 0.0
    for _ in range(steps):
        a = max(plans, key=lambda p: ret(roll(lm, p, z), p))[0]
        total += -z ** 2 - 0.1 * a ** 2
        z = lam * z + beta * a
    return total

for lm in (0.8, 0.9, 0.7):
    print(lm, [round(mpc(lm, H), 4) for H in (1, 2, 3, 5)])
```

**Rollout error against the one-step error it is made of**, zero actions, $\hat\lambda=0.9$:

| $H$ | $z_H$ (true) | $\hat z_H$ (free running) | $\lvert\delta_H\rvert$ | one-step $\lvert e_{H-1}\rvert$ | ratio | $\lvert\delta_H\rvert/z_H$ |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.800000 | 0.900000 | 0.100000 | 0.100000 | 1.00 | 0.125 |
| 2 | 0.640000 | 0.810000 | 0.170000 | 0.080000 | 2.12 | 0.266 |
| 3 | 0.512000 | 0.729000 | 0.217000 | 0.064000 | 3.39 | 0.424 |
| 5 | 0.327680 | 0.590490 | 0.262810 | 0.040960 | 6.42 | 0.802 |
| 6 | 0.262144 | 0.531441 | 0.269297 | 0.032768 | 8.22 | 1.027 |
| 10 | 0.107374 | 0.348678 | 0.241304 | 0.013422 | 17.98 | 2.247 |
| 20 | 0.011529 | 0.121577 | 0.110047 | 0.001441 | 76.36 | 9.545 |

**Planning with each wrong gain**, open loop, against the best plan on the same grid:

| $H$ | regret, $\hat\lambda=0.9$ | gap, $\hat\lambda=0.9$ | regret, $\hat\lambda'=0.7$ | gap, $\hat\lambda'=0.7$ |
|---:|---:|---:|---:|---:|
| 2 | 0.0000 | $-0.0700$ | 0.0000 | $+0.0500$ |
| 3 | 0.0000 | $-0.0820$ | 0.0325 | $+0.0880$ |
| 4 | 0.0000 | $-0.0917$ | 0.0693 | $+0.1153$ |
| 5 | 0.0000 | $-0.0996$ | 0.0929 | $+0.1341$ |

Four readings.

**The ratio column is the headline, and it has no ceiling.** At $H=1$ the free-running error *is* the one-step error, by construction. By $H=20$ it is 76 times larger. A validation number computed one step at a time is not a weak version of the rollout number; it is a different quantity, and the factor between them is set by the model's own gain and the horizon, neither of which appears in the loss.

**The absolute error is a trap.** Column four peaks at $H=6$ and then falls — by $H=20$ it is back below its $H=3$ value. Nothing improved: both trajectories decayed toward zero. The last column, error relative to the state that is left, rises monotonically to $9.545$, meaning the model is wrong by roughly ten times the quantity it is predicting. A rollout-error figure with no normalization and a long enough $x$-axis can show a model getting *better* as it gets worse.

**The two gains are the same error and not the same problem.** Both are $0.1$ off per step. The pessimistic one ($0.9$) costs nothing on this grid — regret $0.0000$ at every horizon — because a planner that over-states future cost still ranks the plans correctly here. The optimistic one ($0.7$) costs a regret that grows with the horizon, $0.0325\to0.0929$ from $H=3$ to $H=5$, and promises a return it misses by $0.1341$. Error magnitude is not the quantity that predicts damage; the sign, relative to what the optimizer is maximizing, is.

**Replanning erases all of it on this plant.** Re-solving after every executed step gives a true 10-step return of $-1.2153$ for $\hat\lambda=0.8$, $0.9$ *and* $0.7$ alike, at every planning horizon $H\ge2$. The myopic $H=1$ planner returns $-2.7458$ even with the *correct* model, since with a one-step horizon the action only ever shows up as its own penalty. So on D5 the horizon matters more than the model, and the cheap fix — one extra solve per step — is worth more than the accurate model. That is a statement about a scalar linear plant with a stable gain; it is the kind of claim that has to be re-measured before it is carried to a real system, which is precisely what §3's list of remedies is a list of.

### 6. Three things called a world model

§1 took one world model apart into five components. By 2026 the phrase also names whole systems that share little but the name, and the cleanest way to sort them — the functional taxonomy World Labs published in June 2026 ([[01-canonical-papers/notes/5-world-models/world-labs|World Labs]]) — asks what a system *outputs*. The three answers are three rows of §1's table. A **renderer** outputs pixels, the observation decoder's job. A **simulator** outputs state that a program can compute on, the transition's job. A **planner** outputs actions, the planner's job.

D5 already shows the split. Its map $f(z,a)=0.8z+0.5a$ is a simulator in this sense: it outputs the next state. §5's enumeration over $\mathcal A$ wraps it into a planner, which outputs an action. Nothing on this page renders; a decoder from $z$ to an image would make it one.

| function | outputs | examples | what a manipulation robot gets | what it does not get |
|---|---|---|---|---|
| renderer | pixels, for a viewer | [[01-canonical-papers/notes/5-world-models/sora\|Sora]]; [[01-canonical-papers/notes/5-world-models/genie\|Genie 3]], real time at $720$p and $24$ frames per second with navigation inputs; World Labs' RTFM; the video models of [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] | images and video to train perception, and synthetic demonstrations | any guarantee of physics: a renderer may show what cannot happen |
| simulator | state — geometry, physics, dynamics | physics engines such as MuJoCo and Isaac; World Labs' Marble (Gaussian splats, meshes, coarse collider meshes) and Atlas (real-to-sim reconstructions) | environments to train and test in, built faster than by hand | contact: a generated scene carries geometry, while mass, stiffness and friction must come from an engine |
| planner | actions | VLAs ([[03-deep-learning/vla/index\|4. VLA]]); JEPA world models that plan — V-JEPA 2-AC, DINO-WM, LeWorldModel ([[01-canonical-papers/notes/5-world-models/jepa\|JEPA]]) | actions, directly or through a short search in a latent | long horizons and contact: V-JEPA 2-AC's tasks are short tabletop ones, and a 2026 preprint audit reports released JEPA world models ranking candidate actions wrongly |

The boundaries blur, and the taxonomy says so. Renderers are becoming action-conditioned — Genie 3 takes navigation inputs, and Cosmos was fine-tuned to predict a robot's next frame from its action vector — and a planner can carry a renderer inside it: Dyna Robotics calls its DYNA-2 a *world-action model*, one video-diffusion model that jointly denoises future frames and future actions, pretrained on more than a million hours of human video ([[03-deep-learning/vla/index|4. VLA §7]]). So the question to ask of any system called a world model is §4's question with one word sharpened: *what does it output*, and which decision can that output support?

The companies sort the same way. LeCun's AMI Labs, launched in Paris in March 2026, builds JEPA-based world models: the planner row. World Labs builds renderers and simulators. DeepMind's Genie 3 is a renderer that takes actions, and NVIDIA's Cosmos a renderer meant to be post-trained into data generators. A company's row can change with its next release; a paper states what its model outputs, which is why the notes cite papers.

For a construction manipulator the rows answer different needs. A renderer can multiply site images for perception. A scene generator can build site-like environments for navigation and coarse placement. Only a planner, or a physics engine running under a generated scene, answers what a push does to a panel on its anchors — and none of the three yet predicts contact forces. D5 is the planner row in its smallest form, and §5's lesson, to measure the rollout and not the one-step loss, is the one that carries to every row.

### After reading

Decompose a world-model paper into five components, identify its rollout horizon, its uncertainty treatment, and whether its reported prediction error is teacher-forced or free-running, and name the real-world decision metric supporting its claim. If the paper plots absolute rollout error against horizon, check whether the plotted quantity can fall for the reason the $H=20$ row falls. For any system called a world model, say whether it outputs pixels, state or actions, and which decision that output can support.

### Self-check

1. A paper reports a one-step validation MSE of $10^{-4}$ on a latent whose learned gain is $\hat\lambda=0.95$. Bound the free-running error at $H=20$ if the one-step errors keep that size, and say why the bound is not the number you would quote.
2. Under which of latent dynamics' three conditions does a video-generation model fail, and what claim does that stop it from supporting?
3. The $\hat\lambda=0.9$ column has regret $0$ at every horizon but a gap that grows. What is a planner losing, if anything?
4. Why does the $H=1$ MPC run score $-2.7458$ even with the exact model?
5. D5's reward charges $-z_t^2$ on the state *before* the action. Whose number changes if the convention is switched to charging $z_{t+1}$, and does the ranking of $(-1,0)$ against $(0,0)$ survive it?
6. A start-up announces a "world model for robots" that turns a phone video of a building site into an explorable 3D scene. Place it among §6's three functions, and say what would still have to be supplied before a manipulator could learn to seat a panel on its anchors inside that scene.

> [!tip]- Answers
> 1. One-step MSE $10^{-4}$ is an error of $10^{-2}$ in the state. The amplification is $(1-0.95^{20})/(1-0.95)=12.83$, so the bound is about $0.128$ — three orders of magnitude worse than the loss suggests. It is not the number to quote because it assumes every one-step error is that large, in the same direction, and independent of the state; on D5 the true errors decayed with the state and the actual $\delta_{20}$ came out well under the bound. The bound is the right thing to ask a paper for, and the measured free-running curve is the right thing to demand alongside it.
> 2. Condition two: the map has no action input. It can satisfy the latent and closure conditions perfectly and still support only a prediction claim, never a control claim, because nothing in it answers a counterfactual about an action the data did not contain.
> 3. Nothing, on this action grid. The gap means the plant keeps outperforming the model's promise, which is a reporting problem rather than a control problem: the same paper's predicted returns are systematically too low. The moment the grid is fine enough that the ordering of near-optimal plans changes, that pessimism starts costing regret too — which is why the $0$ in this column is a property of this grid and is stated as such.
> 4. With $H=1$ the planner maximizes $-z_0^2-0.1a_0^2$ over $a_0$, and $z_0$ does not depend on $a_0$. The only term the action touches is its own penalty, so the optimizer always picks $a_0=0$ and the state coasts down at $0.8$ per step. The failure is the horizon, not the model — the same run with the *wrong* model and $H=2$ scores $-1.2153$.
> 5. Every return on the page shifts, because the sum loses the constant $-z_0^2=-1$ and gains $-z_H^2$. For $(-1,0)$: $-(0.3^2+0.1)-(0.24^2)=-0.1900-0.0576=-0.2476$; for $(0,0)$: $-0.64-0.4096=-1.0496$. The ranking survives and the margin widens from $0.45$ to $0.80$, which is the point: a reward convention changes the numbers a paper prints without changing which plan is better, so two papers' returns are not comparable until the convention is stated.
> 6. A simulator, and only the geometric part of one: it outputs state in the form of a scene — the Marble and Atlas kind — not pixels for a viewer and not actions. To learn a panel insertion in it you would still need a physics engine running under the scene, with the panel's mass and inertia, the stiffness and friction at the anchors and the gripper, and colliders fine enough for contact rather than the coarse ones scene generators export; then sensor models, and a real-robot test to measure what the policy lost in the move. None of that is in a generated scene, which is §6's point: the scene answers where things are, and only a physics engine or a planner that has learned contact answers what a push does.

### Problem set · 과제

Tier A. Using **D5** from [[03-deep-learning/lab-objects|0. Lab Objects]], this page, and [[02-foundations/lab-kernel|0.7 Lab Kernel]]. Original object and original problems — change the knobs in §5's listing; do not rewrite the loop. State the tier in your answer sheet.

1. **Draw.** The picture above, with the two rollout paths into the transition drawn as separate arrows and labelled *teacher forced* and *free running*, the action entering the transition, the reward hanging off the latent, and the planner's edge closing back onto the action. Mark which single arrow you would cut to turn the picture into a video model, and which to turn it into an open-loop plan.
2. **Derive.** The gain is re-learned as $\hat\lambda=0.85$, actions still zero. (a) The one-step error $e_t$ and the closed form for $\delta_H$. (b) $\delta_5$ and $\delta_{20}$, and the horizon at which $\delta_H$ peaks. (c) The relative error $\delta_{20}/z_{20}$. (d) Compare (c) with the $\hat\lambda=0.9$ row of §5 and state, in one sentence, how the relative error at a fixed horizon scales with the size of the gain error.
3. **Do.** Fill the `?` in the patch below and re-run §5's second and third blocks with it. The action gain is now mis-learned instead of the transition gain: $\hat\beta=0.6$ with $\hat\lambda=\lambda=0.8$, so the model believes its actions are stronger than they are. Report regret and gap for $H\in\{2,3,4,5\}$ and the MPC return, and answer the one question that matters: does replanning rescue this error the way it rescued the transition error?

```python
# patch to the §5 listing — fill ?, keep the rest of the loop
def roll_b(lm, bt, acts, z=z0):        # a model that may be wrong about beta too
    out = [z]
    for a in acts:
        z = ?                          # the transition with BOTH gains as arguments
        out.append(z)
    return out

# then, in blocks 2 and 3, the model's rollout becomes roll_b(0.8, 0.6, p, ...)
# and the true rollout stays roll_b(0.8, 0.5, p, ...)
```

> [!note]- How to draw it · 그리는 법
> - Draw the two paths into the transition separately: one from the encoder (a real observation, re-encoded every step) and one from the transition's own output. Those two arrows are the difference between the loss a paper trains on and the rollout it deploys, and §5 measures how far apart they get.
> - Let the action enter the transition, not the encoder. A box with no action input is a video predictor; it can be excellent and still answer no control question.
> - Hang the reward off the latent, not off the pixels. If a paper's reward needs a decoded image, the decoder is inside the planning loop and its error is inside the plan.
> - Close the planner's arrow back onto the action. That feedback edge is what turns a prediction error into a decision error, which is the whole of §3; a diagram without it describes a model, not a model-based method.

> [!tip]- Solutions
> 1. Observation → encoder → latent, latent and action → transition → next latent, next latent → reward and (optionally) decoder, reward → planner → action, and the two arrows back into the transition: one from the encoder (teacher forced) and one from the transition's own output (free running). Cutting the action arrow into the transition turns it into a video model — condition two of latent dynamics. Cutting the planner's edge back onto the action turns it into an open-loop plan, which is the third condition of model exploitation and the arrow §5 shows is worth $0.0929$ of return.
> 2. (a) $e_t=(0.85-0.8)z_t=0.05\cdot0.8^t$ and, by the same telescoping, $\delta_H=0.85^H-0.8^H$. (b) $\delta_5=0.443705-0.327680=0.116025$; $\delta_{20}=0.038760-0.011529=0.027230$; the peak is at $H=5$ itself, since $\delta_4=0.112406$ and $\delta_6=0.115006$ both sit below it — halving the gain error moved the peak in from $H=6$ to $H=5$, so "the horizon where rollout error is worst" is a property of the *model*, not of the plant. (c) $\delta_{20}/z_{20}=(0.85/0.8)^{20}-1=2.3619$. (d) Halving the gain error from $0.1$ to $0.05$ cut the relative error at $H=20$ from $9.545$ to $2.362$, a factor of about four for a factor of two — because the relative error is $(\hat\lambda/\lambda)^H-1$, it is exponential in the horizon and only the *ratio* of the gains, not their difference, controls it.
> 3. Blank: `z = lm * z + bt * a`. Running it gives regret $0.0000$, $0.0325$, $0.0693$, $0.0929$ for $H=2,3,4,5$ — *identical* to the $\hat\lambda'=0.7$ column of §5, because the model picks the same plans $(-1,0,\dots)$: on this plant, believing your actions are 20% stronger and believing the state decays faster bend the planned trajectory the same way. The gaps are not identical — $+0.0500$, $+0.0820$, $+0.1025$, $+0.1156$ against §5's $+0.0500$, $+0.0880$, $+0.1153$, $+0.1341$ — so the two models lose the robot the same return while promising different ones, which is the cleanest demonstration on this page that gap and regret are two numbers. The MPC return is $-1.2153$ again, at every $H\ge2$: replanning rescues this error too, and for the same reason — each re-solve re-anchors on a measured state, so only the *first* action of each plan is ever executed and only its one-step error can be wrong. The honest caveat is that both errors here are in the gains of a stable linear map; an error in the model's *structure*, or one that makes an unreachable state look rewarding, is not re-anchored away by measuring the state you are actually in.

## 한국어

*[[04-robotics/state-estimation-slam|3. State Estimation]]의 필터와 [[02-foundations/rl-basics|7. RL]]의 return 위에 선다. 대상 **D5**를 처음 쓴다.*

> [!note] 처음이라면
> 대상, 계산, §1–3, 문제 1–2를 먼저 한다. 논문이 rollout horizon이나 one-step 예측 손실을 보고하면 §5로 돌아온다. 둘 다 월드모델이라 불리는 두 시스템을 견주기 전에는 §6을 읽는다.

### 이 페이지의 대상 · Running object

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D5**를 그 페이지가 고정한 숫자 그대로 쓴다. $z_{t+1}=0.8z_t+0.5a_t$, $r_t=-z_t^2-0.1a_t^2$다. $z_0=1$, 행동 $(-1,0)$이면 $z_1=0.3$, $r_0=-1.1$, $z_2=0.24$, $r_1=-0.09$다. 실제 실행 없이 행동 sequence를 비교할 수 있다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $\lambda$ | $0.8$ | 참 전이 이득 — 한 스텝 뒤에 남는 상태의 비율 |
| $\beta$ | $0.5$ | 참 행동 이득, 이 페이지의 모든 모델이 공유 |
| $\hat\lambda$ | $0.9$ | §2의 **학습된** 이득: one-step 오차 $0.1z_t$, 비관 방향 |
| $\hat\lambda'$ | $0.7$ | 크기가 같고 방향이 *반대*인 두 번째 학습 이득 |
| $z_0$ | $1$ | 시작 상태 |
| $r_t$ | $-z_t^2-0.1a_t^2$ | 보상, 행동 *이전* 상태에 매긴다 |
| $\mathcal A$ | $\{-1,-0.5,0,0.5,1\}$ | planner가 고를 수 있는 행동 값 |

학습 이득이 하나가 아니라 둘인 이유는, §3의 질문 전체가 모델이 어느 *방향*으로 틀렸는가이고 틀린 모델 하나로는 그 질문에 답할 수 없기 때문이다.

*범위: 이 페이지는 월드모델을 다섯 구성요소로 분해하는 법, 전이의 오차를 한 스텝씩 확인하지 않고 반복했을 때 어떻게 되는지, planner가 그 오차로 무엇을 하는지를 가르친다. latent를 어떻게 학습하는지는 가르치지 않는다. encoder와 전이를 맞추는 목적함수는 [[03-deep-learning/foundations/index|1. Learning Systems]]다. 실제 로봇에서 관측 모델을 온라인으로 뒤집는 법도 아니다. 그것은 [[04-robotics/state-estimation-slam|3. State Estimation]]이다. latent를 픽셀로 바꾸는 생성 decoder도 아니다. 그것은 [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]다. 학습된 모델을 감싸는 policy gradient와 value 기계도 아니다. 그것은 [[02-foundations/rl-basics|7. RL]]다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 478" style="max-width:100%;height:auto" role="img" aria-label="전이로 들어가는 teacher forcing 경로와 자유 진행 경로를 따로 그린 D5 월드모델의 블록선도와, 행동이 0일 때 참 상태 0.8의 H제곱, 자유 진행 rollout 0.9의 H제곱, 그리고 H = 5에서 0.26281이고 H = 6에서 0.269297로 정점인 둘의 차이를 그린 그래프">
  <defs><marker id="aD5k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) 블록선도, D5의 숫자</text>
  <rect x="170" y="32" width="236" height="26" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="288" y="49" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">planner: 행동 sequence에 대한 argmax</text>
  <rect x="170" y="92" width="236" height="50" rx="5" stroke="currentColor" stroke-width="1.8" fill="none"/>
  <text x="288" y="106" font-size="11" fill="currentColor" text-anchor="middle">전이</text>
  <text x="276.2" y="121" font-size="11" fill="currentColor" text-anchor="end">z′ =</text>
  <text x="283.3" y="121" font-size="11" fill="currentColor" text-anchor="middle">λ</text>
  <text x="286.5" y="121" font-size="11" fill="currentColor">z + βa</text>
  <path d="M 280.6 112.7 L 283.3 110.7 L 285.9 112.7" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round"/>
  <text x="270.8" y="136" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">참 λ = 0.8 ·</text>
  <text x="277.9" y="136" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">λ</text>
  <text x="285" y="136" font-size="11" fill="currentColor" fill-opacity="0.8">= 0.9 · β = 0.5</text>
  <path d="M 275.2 127.7 L 277.9 125.7 L 280.5 127.7" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round" stroke-opacity="0.8"/>
  <line x1="288" y1="58" x2="288" y2="90" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD5k)"/>
  <text x="280" y="80" font-size="11" fill="currentColor" text-anchor="end">행동 a<tspan dy="3" font-size="10">t</tspan><tspan dy="-3" dx="3.5">∈ {−1, −½, 0, ½, 1}</tspan></text>
  <line x1="406" y1="117" x2="418" y2="117" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD5k)"/>
  <rect x="420" y="105" width="40" height="24" rx="12" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="440" y="121" font-size="11" fill="currentColor" text-anchor="middle">ẑ<tspan dy="3" font-size="10">t+1</tspan></text>
  <rect x="472" y="66" width="76" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="510" y="80.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">보상</text>
  <text x="510" y="95.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">−z² − 0.1a²</text>
  <rect x="472" y="132" width="76" height="36" rx="5" stroke="currentColor" stroke-width="1.4" fill="none" stroke-dasharray="4 3"/>
  <text x="510" y="146.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">decoder</text>
  <text x="510" y="161.5" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">선택</text>
  <path d="M460 117 L464 117 L464 84 L470 84" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aD5k)" stroke-linejoin="round"/>
  <path d="M464 117 L464 150 L470 150" stroke="currentColor" stroke-width="1.2" fill="none" stroke-dasharray="4 3" marker-end="url(#aD5k)" stroke-linejoin="round"/>
  <path d="M510 66 L510 45 L408 45" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aD5k)" stroke-linejoin="round"/>
  <rect x="12" y="170" width="96" height="24" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="60" y="186" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">관측 o<tspan dy="3" font-size="10">t</tspan></text>
  <rect x="120" y="170" width="64" height="24" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="152" y="186" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="1">encoder</text>
  <line x1="108" y1="182" x2="118" y2="182" stroke="currentColor" stroke-width="1.4" marker-end="url(#aD5k)"/>
  <path d="M184 182 L200 182 L200 144" stroke="currentColor" stroke-width="1.8" fill="none" marker-end="url(#aD5k)" stroke-linejoin="round"/>
  <text x="206" y="164" font-size="11" fill="currentColor">z<tspan dy="3" font-size="10">t</tspan></text>
  <text x="12" y="214" font-size="11" fill="currentColor">teacher forcing: 실제 관측을 다시 부호화</text>
  <path d="M440 129 L440 182 L376 182 L376 144" stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="6 3" marker-end="url(#aD5k)" stroke-linejoin="round"/>
  <text x="370" y="164" font-size="11" fill="currentColor" text-anchor="end">ẑ<tspan dy="3" font-size="10">t</tspan></text>
  <text x="548" y="200" font-size="11" fill="currentColor" text-anchor="end">자유 진행: 모델에 자기 출력을 다시 넣음</text>
  <text x="12" y="246" font-size="12" fill="currentColor">(b) D5에서 두 경로: 행동 0, z<tspan dy="3" font-size="10.2">0</tspan><tspan dy="-3" dx="3.8">= 1</tspan></text>
  <line x1="48" y1="438" x2="540" y2="438" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="48" y1="438" x2="48" y2="258" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="44" y1="438" x2="48" y2="438" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="442" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0</text>
  <line x1="44" y1="394" x2="48" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="398" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.25</text>
  <line x1="44" y1="350" x2="48" y2="350" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="354" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.5</text>
  <line x1="44" y1="306" x2="48" y2="306" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="310" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.75</text>
  <line x1="44" y1="262" x2="48" y2="262" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="41" y="266" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">1</text>
  <line x1="48" y1="438" x2="48" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="48" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <line x1="171" y1="438" x2="171" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="171" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">5</text>
  <line x1="294" y1="438" x2="294" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="294" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">10</text>
  <line x1="417" y1="438" x2="417" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="417" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">15</text>
  <line x1="540" y1="438" x2="540" y2="442" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="540" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <text x="355.5" y="454" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">horizon H</text>
  <path d="M48 262 L72.6 297.2 L97.2 325.4 L121.8 347.9 L146.4 365.9 L171 380.3 L195.6 391.9 L220.2 401.1 L244.8 408.5 L269.4 414.4 L294 419.1 L318.6 422.9 L343.2 425.9 L367.8 428.3 L392.4 430.3 L417 431.8 L441.6 433 L466.2 434 L490.8 434.8 L515.4 435.5 L540 436" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M48 262 L72.6 279.6 L97.2 295.4 L121.8 309.7 L146.4 322.5 L171 334.1 L195.6 344.5 L220.2 353.8 L244.8 362.2 L269.4 369.8 L294 376.6 L318.6 382.8 L343.2 388.3 L367.8 393.3 L392.4 397.7 L417 401.8 L441.6 405.4 L466.2 408.6 L490.8 411.6 L515.4 414.2 L540 416.6" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="7 4" stroke-linejoin="round"/>
  <path d="M48 438 L72.6 420.4 L97.2 408.1 L121.8 399.8 L146.4 394.6 L171 391.7 L195.6 390.6 L220.2 390.7 L244.8 391.8 L269.4 393.4 L294 395.5 L318.6 397.9 L343.2 400.4 L367.8 402.9 L392.4 405.5 L417 408 L441.6 410.3 L466.2 412.6 L490.8 414.8 L515.4 416.8 L540 418.6" stroke="currentColor" stroke-width="1.1" fill="none" stroke-opacity="0.75" stroke-linejoin="round"/>
  <circle cx="72.6" cy="279.6" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="97.2" cy="311.3" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="121.8" cy="336.6" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="146.4" cy="356.9" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="171" cy="373.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="195.6" cy="386.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="220.2" cy="396.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="244.8" cy="404.8" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="269.4" cy="411.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="294" cy="416.7" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="318.6" cy="421" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="343.2" cy="424.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="367.8" cy="427.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="392.4" cy="429.3" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="417" cy="431" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="441.6" cy="432.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="466.2" cy="433.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="490.8" cy="434.4" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="515.4" cy="435.1" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="540" cy="435.7" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <circle cx="195.6" cy="390.6" r="3.6" stroke="none" fill="currentColor"/>
  <line x1="171" y1="380.3" x2="171" y2="334.1" stroke="currentColor" stroke-width="1.6"/>
  <line x1="167" y1="380.3" x2="175" y2="380.3" stroke="currentColor" stroke-width="1.6"/>
  <line x1="167" y1="334.1" x2="175" y2="334.1" stroke="currentColor" stroke-width="1.6"/>
  <text x="68.9" y="431.8" font-size="11" fill="currentColor" fill-opacity="0.85">H = 1: δ = 0.1, one-step 오차</text>
  <line x1="274.3" y1="260" x2="296.3" y2="260" stroke="currentColor" stroke-width="2"/>
  <text x="304.3" y="264" font-size="11" fill="currentColor">참 z<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.8</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <circle cx="285.3" cy="278.5" r="2.6" stroke="currentColor" stroke-width="1.1" fill="none"/>
  <text x="304.3" y="282.5" font-size="11" fill="currentColor">teacher forcing 0.9·z<tspan dy="3" font-size="10">H−1</tspan></text>
  <line x1="274.3" y1="297" x2="296.3" y2="297" stroke="currentColor" stroke-width="2" stroke-dasharray="7 4"/>
  <text x="304.3" y="301" font-size="11" fill="currentColor">자유 진행 ẑ<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.9</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <line x1="274.3" y1="315.5" x2="296.3" y2="315.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75"/>
  <text x="304.3" y="319.5" font-size="11" fill="currentColor">차이 δ<tspan dy="3" font-size="10">H</tspan><tspan dy="-3" dx="3.5">= 0.9</tspan><tspan dy="-4" font-size="10">H</tspan><tspan dy="4" dx="3.5">− 0.8</tspan><tspan dy="-4" font-size="10">H</tspan></text>
  <line x1="285.3" y1="328" x2="285.3" y2="340" stroke="currentColor" stroke-width="1.6"/>
  <line x1="281.3" y1="328" x2="289.3" y2="328" stroke="currentColor" stroke-width="1.6"/>
  <line x1="281.3" y1="340" x2="289.3" y2="340" stroke="currentColor" stroke-width="1.6"/>
  <text x="304.3" y="338" font-size="11" fill="currentColor">H = 5: 0.59049 − 0.32768 = 0.26281</text>
  <circle cx="285.3" cy="352.5" r="3.6" stroke="none" fill="currentColor"/>
  <text x="304.3" y="356.5" font-size="11" fill="currentColor">정점 H = 6: 0.269297</text>
  <text x="304.3" y="375" font-size="11" fill="currentColor">H = 20: δ/z = 9.545</text>
</svg>

D5의 월드모델을 블록선도로 그렸다. 관측, encoder, 전이 $z'=\hat\lambda z+\beta a$(참 $\lambda=0.8$에 대해 $\hat\lambda=0.9$, $\beta=0.5$), latent에 매달린 보상 $-z^2-0.1a^2$, 선택적인 decoder, 행동을 고르는 planner가 있고, 전이로 들어가는 두 경로 — 매 스텝 실제 관측을 다시 부호화하는 teacher forcing과 모델에 자기 출력을 다시 넣는 자유 진행 — 를 따로 그렸다. 아래는 $z_0=1$에서 행동이 0일 때로, teacher forcing 예측 $0.9z_{H-1}$은 참값 $0.8^H$에서 한 스텝의 오차 이상 벗어나지 않지만($H=1$에서 $\delta=0.1$) 자유 진행 rollout $0.9^H$는 멀어져서, 차이 $\delta_H=0.9^H-0.8^H$가 $H=5$에서 $0.26281$, $H=6$에서 정점 $0.269297$이고 $H=20$에서는 참 상태의 $9.545$배다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 과제는 이 그림을 그리고, 오차 점화식을 유도하고, horizon을 쓸어 보라고 한다. 카탈로그 숫자로 여기서 먼저 한다.

**후보 계획 둘, 손으로.** $z_0=1$에서 할인 없이 $(-1,0)$이면 $z_1=0.8(1)+0.5(-1)=0.3$, $z_2=0.24$이므로 return은 $(-1-0.1)+(-0.09)=-1.19$다. $(0,0)$이면 $z_1=0.8$, $z_2=0.64$, return은 $-1-0.64=-1.64$다. 여기서 움직이는 것이 $0.45$의 return 값어치이고, 모델은 플랜트를 건드리지 않고 그것을 알아냈다.

**오차 점화식, 이 페이지의 유일한 유도.** 자유 진행 모델과 참값의 차이를 $\delta_t=\hat z_t-z_t$라 하자. 둘이 같은 측정 상태에서 출발하므로 $\delta_0=0$이다. 두 갱신식을 빼면 $\delta_{t+1}=\hat\lambda\,\delta_t+(\hat\lambda-\lambda)\,z_t$이므로 차이는 두 부분이다. 새로 생긴 one-step 오차 $e_t=(\hat\lambda-\lambda)z_t$ — teacher forcing 검증 손실이 보는 것이 정확히 이것이다 — 와, 모델 *자신의* 이득을 타고 실려 온 예전 차이다. 풀어 쓰면

$$\delta_H=\sum_{t=0}^{H-1}\hat\lambda^{\,H-1-t}\,e_t$$

인데, 한 번 생긴 one-step 오차가 이후의 모든 $\hat\lambda$ 적용을 타고 전파되기 때문이다. 이 한 줄이 one-step 손실로 rollout을 묶을 수 없는 이유다. 손실은 $e_t$를 보고하고 rollout은 그것들 전부의 필터된 합을 보고한다. 모든 $e_t$의 크기가 $e$로 같다면 합은 $e(1-\hat\lambda^H)/(1-\hat\lambda)$이고, $\hat\lambda=0.9$면 $10e$에 다가간다. 스텝당 1% 틀린 모델이 끝에서 10% 틀릴 수 있다. 이 합은 한 스텝 오차들을 커널 $\hat\lambda^{m}$($m$은 오차의 나이)으로 합성곱한 것이고, D5 자체를 같은 종류의 선형 순환망으로 읽는 [[03-deep-learning/foundations/sequence-models|1.1 시퀀스 모델 §7]]의 선형 상태공간 모델이 바로 이것이다.

**D5의 닫힌 형태.** 행동이 0이면 $z_t=0.8^t$, $e_t=0.1\cdot0.8^t$이므로 합이 접혀 $\delta_H=0.9^H-0.8^H$가 된다. $H=5$에서 $0.59049-0.32768=0.26281$로 §2의 숫자이고, $H=1$에서는 $0.1$로 one-step 오차 자신이다. 한 값을 손으로 확인한 뒤 §5가 쓸게 한다.

**그리고 같은 식 안의 함정.** $\delta_H$는 끝없이 자라지 않는다. $H=6$에서 $0.269297$로 정점을 찍고 내려온다. 두 궤적 모두 0으로 붕괴하고 있어 결국 틀릴 거리가 남지 않기 때문이다. 남은 상태를 기준으로 재면 $\delta_H/z_H=(9/8)^H-1$이고 $H=20$에서 $9.545$다. 절대 오차가 줄어드는 동안 모델은 자기가 예측하는 양의 열 배만큼 틀려 있다. 논문의 rollout 그림을 읽기 전에 그 두 곡선 중 무엇을 그린 것인지부터 정해야 한다.

### 1. 월드모델은 여러 모델이다

| 구성요소 | 질문 |
|---|---|
| encoder/inference | 관측을 설명하는 latent state는 무엇인가? |
| transition | 상태와 행동이 그것을 어떻게 바꾸는가? |
| observation decoder | 센서는 무엇을 볼 것인가? |
| reward/termination | 어떤 task signal과 종료가 따르는가? |
| policy/planner | 어떤 상상 행동 sequence를 고를 것인가? |

일부는 pixel decoder가 없고 일부는 video만 생성한다. "world model"이라는 이름만으로 planning이나 물리 일관성이 보장되지 않는다.

이 페이지가 계산에 쓰는 것은 둘째 행이고, 거기에는 "학습된 동역학"이라는 말이 감추는 조건 셋이 있다.

> **Latent dynamics의 정의.** **Latent dynamics**는 *학습된 상태공간 위의 사상과 그 공간을 함께 이르는 것*이다. 함수 $f_\phi$와 그것이 작용하는 집합이지 architecture도, 관측의 예측도 아니다. 정의 조건 셋. 상태가 **잠재적**이다. 측정되는 것이 아니라 관측에서 추론되므로 학습 목적함수가 묶는 만큼만 정해지고, 해석 가능하거나 거리가 보존될 이유가 없다. 사상은 **행동 조건부** $z_{t+1}=f_\phi(z_t,a_t)$이고, 이것이 제어 모델과 video 모델을 가른다. 그리고 **닫혀 있다**. 출력이 입력과 같은 공간에 살아서 encoder도 decoder도 없이 반복할 수 있고, 상상 rollout을 가능하게 하는 것이 이 성질이다.
>
> $$z_{t+1}=f_\phi(z_t,a_t),\qquad \text{D5: } f(z,a)=0.8z+0.5a$$
>
> $z_t$는 latent 상태, $a_t$는 행동, $\phi$는 학습 파라미터다. 위 rollout에서 일하는 조건이 "닫혀 있다"인데, $\delta_t$가 새 관측으로 초기화되지 않고 latent 안에서 누적되게 하는 것이 그것이기 때문이다.
>
> - **예**: D5. 스칼라 하나, 이득 하나, 행동 이득 하나. 이 페이지의 모든 주장이 그 사상의 반복에 대한 것이다.
> - **비예**: 매 스텝 복원하고 다시 부호화하는 관측공간 예측기 $\hat o_{t+1}=g(o_{\le t},a_t)$. 원리상 동등할 수 있지만 latent에서 닫혀 있지 않으므로 rollout 오차에 decoder 오차가 섞이고, 그 곡선에서 둘을 분리할 수 없다.
> - **비예**: 행동 입력 없이 masked 또는 contrastive 예측으로 학습한 표현. 훌륭한 encoder이면서 둘째 조건에서 실패하고, 그러면 "내가 이렇게 하면 어떻게 되는가"에 답하지 못한다. planner가 묻는 질문은 그것뿐이다.
> - **왜 중요한가**: 첫째와 셋째 조건이 합쳐진 것이 낮은 one-step 손실로 rollout을 묶지 못하는 정확한 이유다. 손실은 *encoder*가 준 상태 위에서 계산되고 rollout은 *사상*이 준 상태 위에서 계산되며, §5가 그 둘이 얼마나 벌어지는지를 잰 것이다.

### 2. 다단계 오차

실제 계수 0.8 대신 0.9를 학습했다면 5 step 뒤 실제 $0.328$, 예측 $0.590$이다. 작은 one-step bias가 누적되므로 one-step loss뿐 아니라 rollout horizon과 downstream decision을 평가한다.

### 3. Planner는 모델 오류를 악용한다

optimizer는 모델이 높게 평가하는 trajectory를 적극 찾으므로 학습 분포 밖 허점을 찾을 수 있다. ensemble·uncertainty penalty·짧은 horizon·replanning·보수적 목적함수·실자료 보정은 이를 줄이지만 없애지 않는다.

저 문단이 이름 붙인 현상은 느슨하게 쓰이는 일이 잦고, 느슨하게 쓰면 제안된 처방이 어느 조건을 깨는지가 가려진다.

> **Model exploitation의 정의.** **Model exploitation**은 모델의 성질이 아니라 *planner–모델 쌍*의 성질이다. 근사 아래에서 계산된 return을 최대화해서 생기는 편향이다. 정의 조건 셋. 최대화 대상이 **모델의** return이므로 모델 오차가 계획의 *선택*에 들어간다. 예측 하나가 틀리는 것과 다르다. 모델이 **optimizer가 닿을 수 있는 곳에서 낙관적으로** 틀려야 한다. 어디서나 비관 방향으로 틀린 모델은 악용되지 않고 낭비될 뿐이다. 그리고 선택된 계획이 **실행되어야** 한다. 예측한 return과 실현된 return의 차이를 실제로 치르는 것이 그때다.
>
> $$\text{gap}=\hat J(a^\star_{\hat f})-J(a^\star_{\hat f}),\qquad \text{regret}=J(a^\star_{f})-J(a^\star_{\hat f}),\quad a^\star_{g}=\arg\max_{a_{0:H-1}}J_g$$
>
> $J$는 계획의 참 return, $\hat J$는 모델의 return, $f$는 참 동역학, $\hat f$는 학습된 동역학이다. 논문이 자주 뭉뚱그리는 서로 다른 두 숫자인데, gap은 *모델*이 틀린 양이고 regret은 *로봇*이 잃은 양이기 때문이다.
>
> - **예**: $\hat\lambda'=0.7$로 다섯 스텝을 계획한 D5. 모델은 $-1.1739$를 약속하고 플랜트는 $-1.3081$을 준다. gap $+0.1341$, 같은 행동 격자의 최선에 대한 regret $0.0929$다.
> - **비예**: 크기가 같고 방향이 반대인 오차 $\hat\lambda=0.9$. $H=5$의 gap은 $-0.0996$으로 플랜트가 약속보다 *더 잘하고*, 이 격자에서 regret은 $0$이다. 틀린 모델이 곧 악용된 모델은 아니고, "우리 모델의 one-step 오차는 0.1"만 보고한 논문은 둘 중 어느 경우인지를 말하지 않은 것이다.
> - **비예**: planner 없는 §2의 rollout 오차. 아무것도 그것을 골라내지 않았다. 그것은 예측 오차이고, 그것을 악용이라 부르면 처방을 찾을 수 없게 된다.
> - **왜 중요한가**: 위 문단의 처방은 각각 세 조건 중 정확히 하나를 공격하므로, 조건을 이름 붙이면 비용을 알 수 있다. replanning은 셋째를 공격하고, D5에서 그것은 공짜다. §5에서 이 모델들 전부가 매 스텝 다시 풀기만 하면 똑같이 $-1.2153$을 받는다.

### 4. 사용에 따라 주장 읽기

representation은 latent가 state를 보존하는지, prediction은 미래가 calibrated됐는지, control은 상상 rollout이 실제 return을 높이는지 묻는다. 생성 화질만으로 나머지를 증명하지 못한다.

[[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer]], [[01-canonical-papers/notes/5-world-models/jepa|JEPA]], [[01-canonical-papers/notes/5-world-models/genie|Genie]], [[01-canonical-papers/notes/5-world-models/world-labs|World Labs]]를 이 구성요소 표와 함께 읽고, 둘 다 월드모델이라 자처하는 두 시스템을 견주기 전에는 §6을 읽어라.

### 5. Horizon 쓸기

한 대상 위의 측정 셋: 자유 진행 오차가 그것을 이루는 one-step 오차와 어떻게 다른지, planner가 두 틀린 이득 각각에 얼마를 잃는지, replanning이 무엇을 치르고 무엇을 되찾는지. 행동 격자가 $\mathcal A$이므로 planner는 $5^H$개 sequence를 전수 조사하고, 결과 속에 optimizer 선택이 숨지 않는다. 코드는 영어 절에 한 번만 싣는다.

**자유 진행 오차 대 그것을 이루는 one-step 오차**, 행동 0, $\hat\lambda=0.9$:

| $H$ | $z_H$ (참) | $\hat z_H$ (자유 진행) | $\lvert\delta_H\rvert$ | one-step $\lvert e_{H-1}\rvert$ | 비 | $\lvert\delta_H\rvert/z_H$ |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.800000 | 0.900000 | 0.100000 | 0.100000 | 1.00 | 0.125 |
| 2 | 0.640000 | 0.810000 | 0.170000 | 0.080000 | 2.12 | 0.266 |
| 3 | 0.512000 | 0.729000 | 0.217000 | 0.064000 | 3.39 | 0.424 |
| 5 | 0.327680 | 0.590490 | 0.262810 | 0.040960 | 6.42 | 0.802 |
| 6 | 0.262144 | 0.531441 | 0.269297 | 0.032768 | 8.22 | 1.027 |
| 10 | 0.107374 | 0.348678 | 0.241304 | 0.013422 | 17.98 | 2.247 |
| 20 | 0.011529 | 0.121577 | 0.110047 | 0.001441 | 76.36 | 9.545 |

**두 틀린 이득으로 계획하기**, 개루프 실행, 같은 격자의 최선에 대하여:

| $H$ | regret, $\hat\lambda=0.9$ | gap, $\hat\lambda=0.9$ | regret, $\hat\lambda'=0.7$ | gap, $\hat\lambda'=0.7$ |
|---:|---:|---:|---:|---:|
| 2 | 0.0000 | $-0.0700$ | 0.0000 | $+0.0500$ |
| 3 | 0.0000 | $-0.0820$ | 0.0325 | $+0.0880$ |
| 4 | 0.0000 | $-0.0917$ | 0.0693 | $+0.1153$ |
| 5 | 0.0000 | $-0.0996$ | 0.0929 | $+0.1341$ |

읽는 방법 넷.

**비 열이 요지이고 천장이 없다.** $H=1$에서는 정의상 자유 진행 오차가 one-step 오차 *그 자체*다. $H=20$에서는 76배다. 한 스텝씩 계산한 검증 숫자는 rollout 숫자의 약한 판본이 아니라 다른 양이고, 둘 사이의 배수를 정하는 것은 모델 자신의 이득과 horizon인데 둘 다 손실에는 나타나지 않는다.

**절대 오차는 함정이다.** 넷째 열은 $H=6$에서 정점을 찍고 내려와 $H=20$에서는 $H=3$ 값보다도 낮다. 좋아진 것은 없다. 두 궤적이 함께 0으로 붕괴했을 뿐이다. 남은 상태 대비인 마지막 열은 단조로 올라 $9.545$가 되고, 모델이 자기가 예측하는 양의 대략 열 배만큼 틀렸다는 뜻이다. 정규화 없이 $x$축만 충분히 길게 잡은 rollout 오차 그림은 나빠지는 모델을 *좋아지는* 것처럼 보이게 할 수 있다.

**두 이득은 같은 오차이고 같은 문제는 아니다.** 둘 다 스텝당 $0.1$ 틀렸다. 비관 쪽($0.9$)은 이 격자에서 아무 대가도 치르지 않는다. 모든 horizon에서 regret $0.0000$이다. 미래 비용을 과대평가하는 planner도 여기서는 계획의 순위를 맞게 매기기 때문이다. 낙관 쪽($0.7$)은 horizon과 함께 자라는 regret을 치르고($H=3$의 $0.0325$에서 $H=5$의 $0.0929$로), 약속한 return을 $0.1341$만큼 놓친다. 피해를 예측하는 양은 오차의 크기가 아니라, optimizer가 최대화하는 것에 대한 부호다.

**이 플랜트에서 replanning은 그 전부를 지운다.** 실행한 스텝마다 다시 풀면 $\hat\lambda=0.8$, $0.9$, $0.7$ 모두 $H\ge2$인 모든 계획 horizon에서 참 10-스텝 return이 $-1.2153$이다. 근시안적 $H=1$ planner는 *맞는* 모델로도 $-2.7458$을 받는다. horizon이 하나면 행동이 자기 벌점으로만 나타나기 때문이다. 그러므로 D5에서는 모델보다 horizon이 중요하고, 값싼 처방 — 스텝당 한 번 더 푸는 것 — 이 정확한 모델보다 값지다. 이것은 안정 이득을 가진 스칼라 선형 플랜트에 대한 진술이고, 실제 시스템으로 옮기기 전에 다시 재야 하는 종류의 주장이다. §3의 처방 목록이 바로 그 목록이다.

### 6. 월드모델이라 불리는 세 가지

§1은 월드모델 하나를 다섯 구성요소로 나눴다. 2026년에 이 말은 이름 말고는 공통점이 거의 없는 시스템 전체도 가리키고, 그것들을 가르는 가장 깔끔한 방법 — World Labs가 2026년 6월에 낸 기능 분류([[01-canonical-papers/notes/5-world-models/world-labs|World Labs]]) — 은 시스템이 무엇을 *내놓는지* 묻는다. 세 답은 §1 표의 세 행이다. **렌더러**는 픽셀을 내놓고, 관측 디코더의 일이다. **시뮬레이터**는 프로그램이 계산할 수 있는 상태를 내놓고, 전이의 일이다. **플래너**는 행동을 내놓고, 플래너의 일이다.

D5가 이미 그 분할을 보여 준다. 사상 $f(z,a)=0.8z+0.5a$는 이 뜻의 시뮬레이터다. 다음 상태를 내놓는다. §5가 $\mathcal A$ 위를 모두 훑는 것은 그것을 행동을 내놓는 플래너로 감싼다. 이 페이지에는 렌더링하는 것이 없다. $z$에서 이미지로 가는 디코더를 붙이면 렌더러가 된다.

| 기능 | 내놓는 것 | 예 | 조작 로봇이 얻는 것 | 얻지 못하는 것 |
|---|---|---|---|---|
| 렌더러 | 보는 사람을 위한 픽셀 | [[01-canonical-papers/notes/5-world-models/sora\|Sora]]; 내비게이션 입력을 받으며 $720$p, 초당 $24$프레임으로 실시간인 [[01-canonical-papers/notes/5-world-models/genie\|Genie 3]]; World Labs의 RTFM; [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]]의 비디오 모델 | 인식을 학습시킬 이미지와 비디오, 합성 시연 | 물리의 보장. 렌더러는 일어날 수 없는 일도 보여 줄 수 있다 |
| 시뮬레이터 | 상태 — 기하, 물리, 동역학 | MuJoCo, Isaac 같은 물리 엔진; World Labs의 Marble(Gaussian splat, 메시, 거친 충돌용 메시)과 Atlas(real-to-sim 재구성) | 손으로보다 빨리 만든, 학습하고 시험할 환경 | 접촉. 생성된 장면은 기하를 지니고, 질량·강성·마찰은 엔진이 대야 한다 |
| 플래너 | 행동 | VLA([[03-deep-learning/vla/index\|4. VLA]]); 계획하는 JEPA 월드모델 — V-JEPA 2-AC, DINO-WM, LeWorldModel([[01-canonical-papers/notes/5-world-models/jepa\|JEPA]]) | 곧바로, 또는 잠재 공간의 짧은 탐색을 거친 행동 | 긴 지평과 접촉. V-JEPA 2-AC의 과제는 짧은 탁상 과제이고, 2026년의 프리프린트 감사는 공개된 JEPA 월드모델이 행동 후보의 순위를 틀리게 매긴다고 보고한다 |

경계는 흐려지고, 분류도 그렇게 말한다. 렌더러는 행동 조건을 갖춰 간다 — Genie 3는 내비게이션 입력을 받고, Cosmos는 로봇의 행동 벡터로 다음 프레임을 예측하도록 미세조정되었다 — 그리고 플래너는 안에 렌더러를 품을 수 있다. Dyna Robotics는 DYNA-2를 *월드–액션 모델*이라 부른다. 미래 프레임과 미래 행동을 함께 노이즈 제거하는 비디오 디퓨전 모델 하나로, 사람 비디오 100만 시간 이상으로 사전학습했다([[03-deep-learning/vla/index|4. VLA §7]]). 그러니 월드모델이라 불리는 시스템에 물을 것은 §4의 질문을 한 단어 날카롭게 한 것이다. *무엇을 내놓는가*, 그리고 그 출력이 어떤 결정을 받칠 수 있는가?

회사들도 같은 방식으로 갈린다. 2026년 3월 파리에서 출범한 LeCun의 AMI Labs는 JEPA 기반 월드모델을 만든다. 플래너 행이다. World Labs는 렌더러와 시뮬레이터를 만든다. DeepMind의 Genie 3는 행동을 받는 렌더러이고, NVIDIA의 Cosmos는 데이터 생성기로 사후학습되도록 만든 렌더러다. 회사의 행은 다음 출시에 바뀔 수 있지만 논문은 제 모델이 무엇을 내놓는지 적는다. 노트들이 논문을 인용하는 이유다.

건설 매니퓰레이터에게 세 행은 서로 다른 필요에 답한다. 렌더러는 인식을 위한 현장 이미지를 늘릴 수 있다. 장면 생성기는 내비게이션과 거친 배치를 위한 현장 같은 환경을 지을 수 있다. 앵커 위의 패널을 밀면 무슨 일이 생기는지는 플래너만, 또는 생성된 장면 밑에서 도는 물리 엔진만 답한다 — 그리고 셋 중 어느 것도 아직 접촉력을 예측하지 않는다. D5는 가장 작은 형태의 플래너 행이고, 한 스텝 손실이 아니라 rollout을 재라는 §5의 교훈이 모든 행으로 옮겨 가는 교훈이다.

### 읽고 나면

월드모델 논문을 다섯 구성요소로 분해하고, rollout horizon과 불확실성 처리를 짚고, 보고된 예측 오차가 teacher forcing인지 자유 진행인지 가려내고, 주장을 받치는 실세계 의사결정 metric을 말할 수 있다. 논문이 절대 rollout 오차를 horizon에 대해 그렸다면, 그 양이 §5의 $H=20$ 행이 내려온 이유로 내려올 수 있는지 확인한다. 월드모델이라 불리는 어떤 시스템이든 픽셀·상태·행동 가운데 무엇을 내놓는지, 그 출력이 어떤 결정을 받칠 수 있는지 말한다.

### 스스로 점검

1. 학습된 이득이 $\hat\lambda=0.95$인 latent에서 one-step 검증 MSE를 $10^{-4}$로 보고했다. one-step 오차가 그 크기를 유지한다면 $H=20$의 자유 진행 오차를 묶고, 그 상계를 그대로 인용하면 안 되는 이유를 말하라.
2. video 생성 모델은 latent dynamics의 세 조건 중 무엇에서 실패하며, 그 때문에 어떤 주장을 받치지 못하는가?
3. $\hat\lambda=0.9$ 열은 모든 horizon에서 regret이 $0$인데 gap은 자란다. planner는 무엇을 잃고 있는가, 잃는 것이 있다면?
4. $H=1$ MPC가 정확한 모델로도 $-2.7458$인 이유는?
5. D5의 보상은 행동 *이전* 상태에 $-z_t^2$을 매긴다. $z_{t+1}$에 매기는 규약으로 바꾸면 누구의 숫자가 바뀌고, $(-1,0)$과 $(0,0)$의 순위는 살아남는가?
6. 어느 스타트업이 건설 현장을 휴대폰으로 찍은 영상을 돌아다닐 수 있는 3D 장면으로 바꾸는 "로봇을 위한 월드모델"을 발표했다. §6의 세 기능 가운데 어디에 두겠으며, 매니퓰레이터가 그 장면 안에서 패널을 앵커에 앉히는 법을 배우려면 무엇을 더 대야 하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. one-step MSE $10^{-4}$는 상태 오차 $10^{-2}$다. 증폭은 $(1-0.95^{20})/(1-0.95)=12.83$이므로 상계는 약 $0.128$이고, 손실이 시사하는 것보다 세 자릿수 나쁘다. 그대로 인용하면 안 되는 이유는 모든 one-step 오차가 그 크기로, 같은 방향으로, 상태와 무관하게 난다고 가정하기 때문이다. D5에서는 실제 오차가 상태와 함께 줄었고 실제 $\delta_{20}$은 상계보다 한참 작았다. 상계는 논문에 요구할 옳은 값이고, 함께 요구할 옳은 값은 측정된 자유 진행 곡선이다.
> 2. 둘째 조건이다. 사상에 행동 입력이 없다. latent와 닫힘 조건을 완벽히 만족하면서도 예측 주장만 받치고 제어 주장은 결코 받치지 못한다. 자료에 없던 행동에 대한 반사실을 답하는 것이 그 안에 없기 때문이다.
> 3. 이 행동 격자에서는 없다. gap은 플랜트가 모델의 약속을 계속 웃돈다는 뜻이고, 제어 문제라기보다 보고 문제다. 같은 논문의 예측 return이 체계적으로 낮다. 격자가 촘촘해져 최적 근처 계획들의 순서가 바뀌는 순간부터는 이 비관도 regret을 치르기 시작한다. 그래서 이 열의 $0$은 이 격자의 성질이고, 그렇게 적어야 한다.
> 4. $H=1$이면 planner는 $a_0$에 대해 $-z_0^2-0.1a_0^2$을 최대화하는데 $z_0$은 $a_0$에 의존하지 않는다. 행동이 건드리는 항은 자기 벌점뿐이라 언제나 $a_0=0$을 고르고 상태는 스텝당 $0.8$로 흘러내린다. 실패한 것은 모델이 아니라 horizon이다. *틀린* 모델로도 $H=2$면 $-1.2153$이다.
> 5. 페이지의 모든 return이 옮겨 간다. 합에서 상수 $-z_0^2=-1$이 빠지고 $-z_H^2$이 들어온다. $(-1,0)$은 $-(0.3^2+0.1)-(0.24^2)=-0.2476$, $(0,0)$은 $-0.64-0.4096=-1.0496$이다. 순위는 살아남고 차이는 $0.45$에서 $0.80$으로 벌어진다. 요점이 그것이다. 보상 규약은 어떤 계획이 나은지를 바꾸지 않은 채 논문이 인쇄하는 숫자를 바꾸므로, 규약을 밝히기 전까지 두 논문의 return은 비교 대상이 아니다.
> 6. 시뮬레이터, 그것도 그 기하 부분뿐이다. 장면 형태의 상태를 내놓는다 — Marble과 Atlas 같은 종류 — 보는 사람을 위한 픽셀도, 행동도 아니다. 그 안에서 패널 삽입을 배우려면 여전히 장면 밑에서 도는 물리 엔진이 있어야 하고, 패널의 질량과 관성, 앵커와 그리퍼에서의 강성과 마찰, 장면 생성기가 내보내는 거친 것이 아니라 접촉을 다룰 만큼 촘촘한 충돌 기하가 필요하다. 그다음 센서 모델, 그리고 옮겨 가며 정책이 잃은 것을 재는 실제 로봇 시험이다. 그 어느 것도 생성된 장면 안에 없고, 그것이 §6의 요점이다. 장면은 무엇이 어디 있는지 답하고, 밀면 무슨 일이 생기는지는 물리 엔진이나 접촉을 배운 플래너만 답한다.

### 과제 · Problem set

Tier A. [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D5**, 이 페이지, [[02-foundations/lab-kernel|0.7 Lab Kernel]]. 영어 절 §5의 손잡이를 바꿔라. 루프를 다시 쓰지 마라. 답안에 tier를 명시하라.

1. **그리기.** 위의 그림을 그린다. 전이로 들어가는 rollout 경로 둘을 따로 그려 *teacher forced*와 *free running*으로 이름 붙이고, 행동은 전이로 들어가게, 보상은 latent에 매달리게, planner의 변은 행동으로 돌아와 닫히게 그린다. 어느 화살표 하나를 자르면 video 모델이 되는지, 어느 것을 자르면 개루프 계획이 되는지 표시한다.
2. **유도.** 이득을 $\hat\lambda=0.85$로 다시 학습했고 행동은 여전히 0이다. (a) one-step 오차 $e_t$와 $\delta_H$의 닫힌 형태. (b) $\delta_5$와 $\delta_{20}$, 그리고 $\delta_H$가 정점을 찍는 horizon. (c) 상대 오차 $\delta_{20}/z_{20}$. (d) (c)를 §5의 $\hat\lambda=0.9$ 행과 비교해, 고정된 horizon에서 상대 오차가 이득 오차 크기에 따라 어떻게 커지는지 한 문장으로.
3. **실행.** 영어 절 패치의 `?`를 채우고 §5의 둘째·셋째 블록을 다시 돌린다. 이번에는 전이 이득이 아니라 행동 이득을 잘못 배웠다. $\hat\lambda=\lambda=0.8$에 $\hat\beta=0.6$이므로 모델은 자기 행동이 실제보다 세다고 믿는다. $H\in\{2,3,4,5\}$의 regret과 gap, 그리고 MPC return을 보고하고, 중요한 질문 하나에 답하라. replanning이 전이 오차를 구했던 것처럼 이 오차도 구하는가?

> [!note]- 그리는 법 · How to draw it
> - 전이로 들어가는 경로 둘을 따로 그린다. 하나는 encoder에서(매 스텝 실제 관측을 다시 부호화), 하나는 전이 자신의 출력에서 온다. 이 두 화살표가 논문이 학습하는 손실과 배포하는 rollout의 차이이고, §5가 그 둘이 얼마나 벌어지는지를 잰다.
> - 행동은 encoder가 아니라 전이로 들어가게 그린다. 행동 입력이 없는 상자는 video 예측기다. 훌륭해도 제어 질문에는 하나도 답하지 못한다.
> - 보상은 픽셀이 아니라 latent에 매단다. 논문의 보상이 복원된 이미지를 필요로 하면 decoder가 planning 루프 안에 있고 그 오차도 계획 안에 있다.
> - planner의 화살표는 행동으로 돌아와 닫히게 그린다. 예측 오차를 결정 오차로 바꾸는 것이 그 되먹임 변이고, 그것이 §3 전부다. 그 변이 없는 그림은 모델을 설명한 것이지 모델 기반 방법을 설명한 것이 아니다.

> [!tip]- 정답 · Solutions
> 1. 관측 → encoder → latent, latent와 행동 → 전이 → 다음 latent, 다음 latent → 보상과 (선택적) decoder, 보상 → planner → 행동, 그리고 전이로 되돌아오는 화살표 둘: encoder에서 오는 것(teacher forced)과 전이 자신의 출력에서 오는 것(free running). 전이로 들어가는 행동 화살표를 자르면 video 모델이 된다. latent dynamics의 둘째 조건이다. planner에서 행동으로 가는 변을 자르면 개루프 계획이 되고, 그것이 model exploitation의 셋째 조건이며 §5가 $0.0929$의 return 값어치라고 보인 화살표다.
> 2. (a) $e_t=(0.85-0.8)z_t=0.05\cdot0.8^t$이고 같은 방식으로 접으면 $\delta_H=0.85^H-0.8^H$다. (b) $\delta_5=0.443705-0.327680=0.116025$, $\delta_{20}=0.038760-0.011529=0.027230$이고 정점은 $H=5$ 자신이다. $\delta_4=0.112406$, $\delta_6=0.115006$ 둘 다 그 아래다. 이득 오차를 반으로 줄이자 정점이 $H=6$에서 $H=5$로 당겨졌으므로 "rollout 오차가 가장 나쁜 horizon"은 플랜트가 아니라 *모델*의 성질이다. (c) $\delta_{20}/z_{20}=(0.85/0.8)^{20}-1=2.3619$. (d) 이득 오차를 $0.1$에서 $0.05$로 반으로 줄이자 $H=20$의 상대 오차가 $9.545$에서 $2.362$로, 두 배에 대해 약 네 배 줄었다. 상대 오차가 $(\hat\lambda/\lambda)^H-1$이라 horizon에 지수적이고, 이득의 차이가 아니라 *비*만이 그것을 정하기 때문이다.
> 3. 빈칸은 `z = lm * z + bt * a`다. 돌려 보면 $H=2,3,4,5$의 regret이 $0.0000$, $0.0325$, $0.0693$, $0.0929$로 §5의 $\hat\lambda'=0.7$ 열과 *똑같다*. 모델이 같은 계획 $(-1,0,\dots)$을 고르기 때문이다. 이 플랜트에서는 행동이 20% 세다고 믿는 것과 상태가 더 빨리 붕괴한다고 믿는 것이 계획 궤적을 같은 방향으로 휜다. gap은 같지 않다. $+0.0500$, $+0.0820$, $+0.1025$, $+0.1156$으로 §5의 $+0.0500$, $+0.0880$, $+0.1153$, $+0.1341$과 다르다. 두 모델이 로봇에게 같은 return을 잃히면서 서로 다른 return을 약속한 것이고, gap과 regret이 두 개의 숫자라는 것을 이 페이지에서 가장 깨끗하게 보이는 자리다. MPC return도 다시 $-1.2153$이고 모든 $H\ge2$에서 그렇다. replanning이 이 오차도 구하며, 이유도 같다. 다시 풀 때마다 측정된 상태에 다시 닻을 내리므로 각 계획의 *첫* 행동만 실행되고 그 one-step 오차만 틀릴 수 있다. 정직한 단서는 여기의 두 오차가 모두 안정한 선형 사상의 이득에 있다는 점이다. 모델의 *구조*가 틀렸거나, 도달할 수 없는 상태를 보상이 높아 보이게 만드는 오차는, 지금 있는 상태를 재는 것만으로 닻이 다시 내려지지 않는다.
