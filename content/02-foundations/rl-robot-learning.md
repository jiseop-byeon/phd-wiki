---
title: "7.5 RL for Robot Learning"
tags: [foundations]
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and experiment sections of a robot-learning paper: name its objective (behaviour cloning, RL fine-tuning, a learned reward), audit its reward and its protocol, and complete this page's problem set from the wiki."
mastery-when: "Raise to Mastery when a reward design, an RL fine-tuning recipe or a learned reward is the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/rl-basics|7. RL Basics §2–§4]] (values, advantage and the bucket MDP; TD and the deadly triad; policy gradients and PPO) · [[02-foundations/probability|3. Probability §4]] (maximum likelihood — behaviour cloning and every reward fit) · [[02-foundations/information-theory|5. Information Theory §1, §3]] (entropy and KL divergence — the entropy bonus, the KL anchor, MaxEnt IRL) · [[02-foundations/optimization|4. Optimization §4]] (Lagrange multipliers — constrained MDPs, MaxEnt IRL, DPO)
> [[02-foundations/rl-basics|7. RL 기초 §2–§4]](가치·어드밴티지와 버킷 MDP, TD와 deadly triad, 정책 그래디언트와 PPO) · [[02-foundations/probability|3. 확률 §4]](최대우도 — 행동 복제와 모든 보상 적합) · [[02-foundations/information-theory|5. 정보이론 §1, §3]](엔트로피와 KL 발산 — 엔트로피 보너스, KL 닻, MaxEnt IRL) · [[02-foundations/optimization|4. 최적화 §4]](라그랑주 승수 — 제약 MDP, MaxEnt IRL, DPO)
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/rl-basics|7. RL Basics]] and reads best straight after it. That page built the machinery; this one is the layer robot-learning papers spend their pages on.*

7. RL Basics gave the MDP, the Bellman equations, TD learning, the deadly triad, policy gradients and PPO. A robot-learning paper spends its pages elsewhere: whether the policy learns from demonstrations or from a reward, what that reward says, how the policy finds anything worth learning, how RL is run on a machine that can break, how the experiment was set up, and how a reward can be learned from people when nobody can write it down. That layer is this page.

> [!note] First pass · 처음이라면
> Read the running object, the picture and the Worked case first: they are §1 and §2 on one two-state MDP. Then read §1 (which half of the field your papers live in) and §2 (the reward), then §4 and §5, which are what a robot paper's method and experiment sections are made of. §3, on exploration, is short: read it when a paper's exploration scheme puzzles you. §6, learning the reward, is second-pass unless you read RLHF, DPO or inverse-RL papers; it assumes §2, and its four subsections can be read one at a time. Read §8 when a paper post-trains a policy from success alone, or says GRPO.

### Running object · 이 페이지의 대상

The **bucket MDP** of [[02-foundations/rl-basics|7. RL Basics §2]], with its "wait" action, and one operator's record of driving it. No plant from [[02-foundations/lab-plants|0.6 Lab Plants]] fits: the subject here is where a policy's data and its reward come from, and the object has to be small enough that a whole policy's value can be written down. The nearest candidate, plant P4 read as an MDP on 7. RL Basics, has no task to put off — its best move is to do nothing — so it cannot show what a reward that pays for doing nothing does. The bucket can.

- **States** $A$ (bucket empty) and $B$ (bucket full); discount $\gamma = 0.9$; every transition is deterministic.
- **Actions.** In $A$: *move* to $B$ with reward $0$, or *wait* in $A$ with reward $0$. In $B$: one action, *stay*, with reward $1$ per step.
- **Values**, derived on 7. RL Basics §2: $V^*(B) = 10$, $V^*(A) = 9$, $Q^*(A,\text{move}) = 9$ and $Q^*(A,\text{wait}) = 8.1$, so waiting has advantage $-0.9$.
- **The operator's record.** Four demonstrations from $A$: in three the operator moves at once, and in one the operator waits a step and then moves. At $A$ that is five state–action pairs, four moves and one wait.

These numbers are frozen here and never change on this page; the problem set changes $\gamma$ and the record, never the definitions.

*Scope: this page teaches the robot-learning layer on top of the MDP — imitation versus RL, reward design, exploration, RL on a physical machine, reading an RL experimental section, and learning a reward from demonstrations or preferences. It does not teach the MDP, value functions, TD learning, the deadly triad or policy gradients, which are [[02-foundations/rl-basics|7. RL Basics]], nor the transfer from simulation to a machine — the reality gap, randomization, the deployment ladder — which is the [[05-construction-robotics/sim-to-real|Sim-to-Real guide]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 520" style="max-width:100%;height:auto" role="img" aria-label="the bucket MDP with gamma 0.9: behaviour cloning of a record of four moves and one wait reaches 8.78 against the optimum 9, and an idle bonus b per wait step makes waiting forever the written optimum once b passes 0.9, worth 10 on the written reward and 0 on the task at b = 1">
  <defs><marker id="arRr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <text x="12.0" y="22.0" fill="currentColor" font-size="12">1 · the bucket MDP (γ = 0.9) and the operator’s record</text>
  <circle cx="190" cy="118" r="38" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="190.0" y="115.0" fill="currentColor" font-size="12" text-anchor="middle">A · empty</text>
  <text x="190.0" y="132.0" fill="currentColor" text-anchor="middle" opacity="0.9">V*(A) = 9</text>
  <circle cx="400" cy="118" r="38" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="400.0" y="115.0" fill="currentColor" font-size="12" text-anchor="middle">B · full</text>
  <text x="400.0" y="132.0" fill="currentColor" text-anchor="middle" opacity="0.9">V*(B) = 10</text>
  <line x1="230" y1="118" x2="359" y2="118" stroke="currentColor" stroke-width="2.2" marker-end="url(#arRr)"/>
  <text x="294.5" y="110.0" fill="currentColor" font-size="12" text-anchor="middle">move, r = 0</text>
  <text x="294.5" y="136.0" fill="currentColor" text-anchor="middle" opacity="0.9">Q*(A, move) = 9</text>
  <path d="M171.0 85.1 C144 22 236 22 209.5 84.2" stroke="currentColor" stroke-width="1.6" fill="none" stroke-opacity="0.8" stroke-dasharray="5 3" marker-end="url(#arRr)"/>
  <text x="146.0" y="52.0" fill="currentColor" font-size="12" text-anchor="end">wait, r = 0 (+ b)</text>
  <text x="146.0" y="67.0" fill="currentColor" text-anchor="end" opacity="0.9">Q*(A, wait) = 8.1</text>
  <path d="M381.0 85.1 C354 22 446 22 419.5 84.2" stroke="currentColor" stroke-width="2.2" fill="none" marker-end="url(#arRr)"/>
  <text x="444.0" y="60.0" fill="currentColor" font-size="12">stay, r = +1</text>
  <rect x="20" y="178" width="520" height="46" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="32.0" y="196.0" fill="currentColor" font-size="12">record at A: 4 moves, 1 wait   →   BC: π(move | A) = 0.8</text>
  <text x="32.0" y="214.0" fill="currentColor" font-size="12">V<tspan dy="-4" font-size="11">BC</tspan><tspan dy="4">(A) = 8.78  &lt;  V*(A) = 9: RL, given the reward, recovers the 0.22</tspan></text>
  <text x="12.0" y="262.0" fill="currentColor" font-size="12">2 · value in A against an idle bonus b paid on every wait step</text>
  <line x1="70" y1="470" x2="528" y2="470" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6"/>
  <line x1="70" y1="470" x2="70" y2="282" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6"/>
  <line x1="66" y1="470.0" x2="70" y2="470.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="474.0" fill="currentColor" text-anchor="end" opacity="0.85">0</text>
  <line x1="66" y1="395.0" x2="70" y2="395.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="399.0" fill="currentColor" text-anchor="end" opacity="0.85">5</text>
  <line x1="66" y1="335.0" x2="70" y2="335.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="339.0" fill="currentColor" text-anchor="end" opacity="0.85">9</text>
  <line x1="66" y1="320.0" x2="70" y2="320.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="324.0" fill="currentColor" text-anchor="end" opacity="0.85">10</text>
  <line x1="70.0" y1="470" x2="70.0" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="257.5" y1="470" x2="257.5" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="407.5" y1="470" x2="407.5" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="445.0" y1="470" x2="445.0" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="70.0" y="487.0" fill="currentColor" text-anchor="middle" opacity="0.85">0</text>
  <text x="257.5" y="487.0" fill="currentColor" text-anchor="middle" opacity="0.85">0.5</text>
  <text x="405.5" y="487.0" fill="currentColor" text-anchor="end" opacity="0.85">0.9 = γ</text>
  <text x="447.0" y="487.0" fill="currentColor" opacity="0.85">1</text>
  <text x="528.0" y="506.0" fill="currentColor" text-anchor="end" opacity="0.85">idle bonus b</text>
  <text x="76.0" y="286.0" fill="currentColor" opacity="0.85">value in A</text>
  <line x1="70" y1="335.0" x2="520" y2="335.0" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.75"/>
  <line x1="70" y1="470.0" x2="520.0" y2="290.0" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 4" stroke-opacity="0.85"/>
  <path d="M70 335.0 L407.5 335.0 L407.5 470.0 L520 470.0" fill="none" stroke="currentColor" stroke-width="3"/>
  <circle cx="407.5" cy="335.0" r="3.5" fill="currentColor"/>
  <circle cx="445.0" cy="320.0" r="3.2" fill="currentColor"/>
  <circle cx="445.0" cy="470.0" r="3.2" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="437.0" y="312.0" fill="currentColor" text-anchor="end">written 10</text>
  <text x="453.0" y="463.0" fill="currentColor">task 0</text>
  <text x="78.0" y="328.0" fill="currentColor">written: moving now = 9</text>
  <text x="78.0" y="352.0" fill="currentColor" font-weight="bold">task value of the written optimum</text>
  <text x="302.5" y="367.0" fill="currentColor" text-anchor="end">written: waiting forever = 10b</text>
  <text x="417.5" y="396.5" fill="currentColor">past b = γ, the</text>
  <text x="417.5" y="410.5" fill="currentColor">written optimum</text>
  <text x="417.5" y="424.5" fill="currentColor">waits forever</text>
</svg>

The bucket MDP with the operator's record: four moves and one wait at $A$ give behaviour cloning $\pi(\text{move}\mid A) = 0.8$ and $V^{\text{BC}}(A) = 8.78$, short of the optimum $V^*(A) = 9$ that RL reaches from the reward. Below, an idle bonus $b$ paid on every wait: moving now is worth $9$ on the written reward and waiting forever $10b$, so past $b = \gamma = 0.9$ the written optimum waits forever — worth $10$ on what was written and $0$ on the task at $b = 1$.

### Worked case · 대상으로 한 번 끝까지

Everything below runs on the running object. Every value comes from the Bellman expectation equation of [[02-foundations/rl-basics|7. RL Basics §2]]: a state's value is this step's reward plus $\gamma$ times the value of where you land.

**1. What imitation gets.** *Behaviour cloning* (BC) fits the policy to the recorded state–action pairs by maximum likelihood (§1); for a table of counts the maximizer is the empirical frequency, so the five pairs at $A$ give $\pi_{\text{BC}}(\text{move}\mid A) = 4/5 = 0.8$. A move lands in $B$, worth $10$, and a wait lands back in $A$, so BC's value appears on both sides of its own equation:

$$V^{\text{BC}}(A) = 0.8\,(0 + 0.9 \times 10) + 0.2\,\big(0 + 0.9\,V^{\text{BC}}(A)\big) \;\Rightarrow\; V^{\text{BC}}(A) = \frac{7.2}{1 - 0.18} = 8.78$$

The greedy policy on $Q^*$ moves every time and earns $V^*(A) = 9$. The gap of $0.22$ is what copying the operator's one hesitation costs, and it is the whole content of "RL can exceed the demonstrator": the reward says that waiting is worth $8.1$ against $9$ for moving, and BC never reads a reward.

**2. What the reward decides.** Now let the reward's author add an *idle bonus* $b$ to every wait step — the "smoothness" term of §2 that pays a policy for leaving the actuators still. Moving now still earns $9$ on the written reward, since the bonus is only paid in $A$, while waiting forever earns

$$b + 0.9\,b + 0.9^2\,b + \cdots = \frac{b}{1 - 0.9} = 10\,b$$

so the written optimum flips to waiting forever once $10b > 9$, that is past $b = 0.9$ — past $b = \gamma$ in general, since moving is worth $\gamma/(1-\gamma)$ and waiting forever $b/(1-\gamma)$. At $b = 1$ the RL policy earns $10$ on what was written and $0$ on the task, because the bucket is never filled. That is *reward hacking* (§2): the policy maximized what was written, not what was meant. BC, which never read the reward, still earns $8.78$.

**3. The same bonus, paid safely.** A *potential-based* shaping term (§2) pays $F = \gamma\Phi(s') - \Phi(s)$ for a function $\Phi$ of the state alone, and cannot change which action is best. It can still pay exactly $b = 1$ on every wait: $\gamma\Phi(A) - \Phi(A) = -0.1\,\Phi(A) = 1$ fixes $\Phi(A) = -10$, and with $\Phi(B) = 0$ the move then earns $F = 0 - (-10) = 10$ while a step in $B$ earns $0$. Under the shaped reward a step in $B$ still pays $1 + 0 = 1$, so $V'(B) = 10$ and

$$Q'(A,\text{move}) = 10 + 0.9 \times 10 = 19, \qquad Q'(A,\text{wait}) = 1 + 0.9 \times 19 = 18.1$$

where the wait is followed by the best play from $A$, worth $19$; waiting forever earns only $1/(1 - 0.9) = 10$. These are the unshaped $9$ and $8.1$ plus $10$, so moving still wins by $0.9$. The idle bonus of part 2 and this term pay the same $+1$ on every wait. The one difference is the $10$ on the move, which pays back at once the whole bank of bonuses that waiting forever would have collected.

**Reading it.** Three numbers carry the page: $8.78$ (imitation copies its data, hesitation included), $9$ (RL given the right reward removes the hesitation) and $0$ (RL given a reward with a loop in it removes the task). §1 is about the first two and §2 about the third. §4 is how a fine-tuned policy is kept near the first while it chases the second, §5 is how to tell from an experiment section which of the three a paper is reporting, and §6 is how to get the reward from people when nobody can write one without a loop.

### 1. RL vs imitation in robot learning (orientation map)

- **Imitation** ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]],
  [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]): supervised on demos —
  stable, no reward design, but plain offline BC is capped by data coverage and cannot
  learn recoveries *outside the **support** of its demos* (the support of a dataset = the
  region of states and actions it actually covers; outside it the model has seen nothing) (demos with recoveries, or DAgger-style
  data collection, change this).
- **RL** *can* exceed the demonstrator — when an informative reward and enough exploration
  are available — practical mostly in
  simulation (sim-to-real) or as *fine-tuning* atop imitation-pretrained VLAs, mirroring
  the [[01-canonical-papers/notes/1-foundations/instructgpt|pretrain → RLHF]] recipe.

**The imitation-learning toolbox** (the vocabulary of every VLA paper). Read it in three
groups — *the core objective and its one failure mode*, *what the data looks like*, and
*what makes a policy expressive* — not as six loose facts.

*Group 1 — the objective and its Achilles' heel.* **BC** just maximizes
$\log \pi_\theta(a|o)$ over demo pairs — supervised learning wearing a policy costume
([[01-canonical-papers/how-to-read|how-to-read §3]] walks this exact equation). Its one
structural weakness is **covariate shift**: the policy is trained on *expert* states but
runs on *its own*, so small errors drift the state off-distribution where errors compound.
That single failure mode is why **DAgger** exists — execute the learner, let the expert
label the states it actually visited, retrain.

- **Behaviour cloning, written out.** Given a dataset $\mathcal{D} = \{(o_i, a_i)\}_{i=1}^{N}$ of expert observations and actions,
  $$\theta^\star = \arg\max_\theta \sum_{i=1}^{N} \log \pi_\theta\big(a_i \mid o_i\big)$$
  which is maximum-likelihood supervised learning, so no reward and no environment interaction appear anywhere. For a Gaussian policy with fixed standard deviation, $-\log \pi_\theta(a \mid o) = \frac{1}{2\sigma^2}\lVert a - \mu_\theta(o)\rVert^2 + \text{const}$, so BC reduces to mean-squared-error regression onto the demonstrated actions.
- **Covariate shift, as two distributions.** Write $d_\pi(s)$ for the distribution of states a policy $\pi$ visits when it runs. BC minimizes its loss under the expert's visitation $d_{\pi_E}$, but the deployed policy is scored under its own:
  $$\text{trained on } E_{s \sim d_{\pi_E}}\big[\ell(\pi_\theta, s)\big], \qquad \text{evaluated on } E_{s \sim d_{\pi_\theta}}\big[\ell(\pi_\theta, s)\big], \qquad d_{\pi_\theta} \ne d_{\pi_E}$$
  where $\ell$ is the per-state imitation loss. The inputs' distribution moves while the correct action for each state does not, which is exactly covariate shift in the sense of [[02-foundations/ml-practice|9. ML Practice §1]].
- **DAgger, as an algorithm** (Ross, Gordon & Bagnell, 2011). Start with the demonstrations as $\mathcal{D}$ and train $\pi_1$. At iteration $i$: run a mixture that follows the expert with probability $\beta_i$ and the current learner otherwise; record the states visited; ask the expert what it *would* do in each; aggregate and retrain,
  $$\mathcal{D} \leftarrow \mathcal{D} \cup \big\{(s, \pi_E(s)) : s \sim d_{\pi_i}\big\}, \qquad \pi_{i+1} = \text{BC on } \mathcal{D}$$
  so the training distribution is pulled toward the learner's own state distribution. A common schedule is $\beta_i = 0.5^{\,i-1}$, that is $1, 0.5, 0.25, 0.125$, handing control to the learner geometrically. **Non-example:** collecting more expert demonstrations and retraining is not DAgger, because those states still come from $d_{\pi_E}$.
- **Support.** The support of a distribution is the set where it has nonzero probability, $\operatorname{supp}(d) = \{s : d(s) > 0\}$. "Outside the support of the demonstrations" means states with $d_{\pi_E}(s) = 0$, where BC's loss has never been evaluated and its output is pure extrapolation.

*How bad is it?* Suppose each step independently carries a small chance $\epsilon$ of an
error that puts the policy somewhere its demonstrations never went. Then a $T$-step task
survives with probability $(1-\epsilon)^T$, and the horizon does the damage:

<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="probability of finishing a task without a single mistake, falling with horizon for three per-step error rates">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="60" y1="170" x2="524" y2="170"/><line x1="60" y1="170" x2="60" y2="36"/>
  </g>
  <g stroke="currentColor" stroke-width="0.8" fill="none" opacity="0.25" stroke-dasharray="3 3">
    <line x1="60" y1="105" x2="524" y2="105"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="152" y1="170" x2="152" y2="175"/><line x1="244" y1="170" x2="244" y2="175"/><line x1="336" y1="170" x2="336" y2="175"/><line x1="428" y1="170" x2="428" y2="175"/><line x1="520" y1="170" x2="520" y2="175"/>
  </g>
  <path d="M 60.0 40.0 L 69.2 92.2 L 78.4 123.4 L 87.6 142.1 L 96.8 153.3 L 106.0 160.0 L 115.2 164.0 L 124.4 166.4 L 133.6 167.9 L 142.8 168.7 L 152.0 169.2 L 161.2 169.5 L 170.4 169.7 L 179.6 169.8 L 188.8 169.9 L 198.0 169.9 L 207.2 170.0 L 216.4 170.0 L 225.6 170.0 L 234.8 170.0 L 244.0 170.0 L 253.2 170.0 L 262.4 170.0 L 271.6 170.0 L 280.8 170.0 L 290.0 170.0 L 299.2 170.0 L 308.4 170.0 L 317.6 170.0 L 326.8 170.0 L 336.0 170.0 L 345.2 170.0 L 354.4 170.0 L 363.6 170.0 L 372.8 170.0 L 382.0 170.0 L 391.2 170.0 L 400.4 170.0 L 409.6 170.0 L 418.8 170.0 L 428.0 170.0 L 437.2 170.0 L 446.4 170.0 L 455.6 170.0 L 464.8 170.0 L 474.0 170.0 L 483.2 170.0 L 492.4 170.0 L 501.6 170.0 L 510.8 170.0 L 520.0 170.0" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <path d="M 60.0 40.0 L 69.2 52.4 L 78.4 63.7 L 87.6 73.8 L 96.8 83.0 L 106.0 91.3 L 115.2 98.9 L 124.4 105.7 L 133.6 111.8 L 142.8 117.4 L 152.0 122.4 L 161.2 127.0 L 170.4 131.1 L 179.6 134.8 L 188.8 138.2 L 198.0 141.2 L 207.2 144.0 L 216.4 146.5 L 225.6 148.7 L 234.8 150.7 L 244.0 152.6 L 253.2 154.2 L 262.4 155.8 L 271.6 157.1 L 280.8 158.3 L 290.0 159.5 L 299.2 160.5 L 308.4 161.4 L 317.6 162.2 L 326.8 163.0 L 336.0 163.6 L 345.2 164.2 L 354.4 164.8 L 363.6 165.3 L 372.8 165.7 L 382.0 166.1 L 391.2 166.5 L 400.4 166.8 L 409.6 167.1 L 418.8 167.4 L 428.0 167.7 L 437.2 167.9 L 446.4 168.1 L 455.6 168.3 L 464.8 168.4 L 474.0 168.6 L 483.2 168.7 L 492.4 168.8 L 501.6 169.0 L 510.8 169.1 L 520.0 169.1" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <path d="M 60.0 40.0 L 69.2 41.3 L 78.4 42.6 L 87.6 43.8 L 96.8 45.1 L 106.0 46.3 L 115.2 47.6 L 124.4 48.8 L 133.6 50.0 L 142.8 51.2 L 152.0 52.4 L 161.2 53.5 L 170.4 54.7 L 179.6 55.9 L 188.8 57.0 L 198.0 58.1 L 207.2 59.2 L 216.4 60.3 L 225.6 61.4 L 234.8 62.5 L 244.0 63.6 L 253.2 64.6 L 262.4 65.7 L 271.6 66.7 L 280.8 67.8 L 290.0 68.8 L 299.2 69.8 L 308.4 70.8 L 317.6 71.8 L 326.8 72.7 L 336.0 73.7 L 345.2 74.7 L 354.4 75.6 L 363.6 76.6 L 372.8 77.5 L 382.0 78.4 L 391.2 79.3 L 400.4 80.2 L 409.6 81.1 L 418.8 82.0 L 428.0 82.9 L 437.2 83.7 L 446.4 84.6 L 455.6 85.5 L 464.8 86.3 L 474.0 87.1 L 483.2 88.0 L 492.4 88.8 L 501.6 89.6 L 510.8 90.4 L 520.0 91.2" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="110" y="148">1 step in 20 wrong</text>
    <text x="170" y="124">1 in 100</text>
    <text x="300" y="64">1 in 1000</text>
    <text x="54" y="44" text-anchor="end">1.0</text><text x="54" y="109" text-anchor="end">0.5</text><text x="54" y="174" text-anchor="end">0</text>
    <text x="152" y="188" text-anchor="middle">100</text><text x="244" y="188" text-anchor="middle">200</text><text x="336" y="188" text-anchor="middle">300</text><text x="428" y="188" text-anchor="middle">400</text><text x="520" y="188" text-anchor="middle">500</text>
    <text x="292" y="204" text-anchor="middle">task length (steps)</text>
    <text x="20" y="30">chance of a clean run</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="226">A per-step error rate that sounds negligible becomes a task failure rate.</text>
    <text x="20" y="242">At one error in a hundred steps, a 50-step task finishes cleanly about 60% of</text>
    <text x="20" y="258">the time &#8212; and a 500-step task about 0.7%.</text>
  </g>
</svg>

Real errors are neither independent nor individually fatal, so read that curve as an
illustration, not a theorem. The theorem has the same shape: Ross, Gordon and Bagnell's
2011 reduction shows plain behaviour cloning accumulates cost as $O(\epsilon T^2)$ while a
no-regret method such as DAgger reaches $O(\epsilon T)$ — the difference between a horizon
you can grow and one you cannot. **Action chunking** (group 3 below) is the cheap version of
the same move: predicting $k$ steps at once turns a $T$-step task into a $T/k$-decision
task, sliding you back down the horizon axis. [[05-construction-robotics/imitating-contact|10. Imitating Contact §3]] prices both bounds on a
construction task, S1's last 40 mm: at $\epsilon=0.02$ the first allows $T^2\epsilon=32$ steps adrift
where the lead-in absorbs $15$, so it covers only a $27$-step phase, while the second covers $750$.

*Group 2 — reading a dataset section.* Demos come from teleoperation
([[01-canonical-papers/notes/4-vla/act|ALOHA]]-style rigs, VR, kinesthetic teaching), scripted
policies, or cross-embodiment pooling ([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]]).
Two things to check: **time-synchronization** (a mislabeled 100 ms offset silently corrupts
every observation-action pair) and **curation over count** — success filtering and
*trajectory diversity* (scenes, objects, initial conditions) usually matter more than "N
thousand demos," which is the number to audit skeptically.

*Group 3 — why the fancy output heads exist.* Demonstrations are **multimodal**: two
experts pass an obstacle on opposite sides, so a mean-regressing policy drives straight
through the middle. The fixes you'll meet are **action chunking** (predict $k$ future
actions at once — [[01-canonical-papers/notes/4-vla/act|ACT]] — trading reactivity to fight
compounding error) and **expressive heads** that can represent multiple modes
([[01-canonical-papers/notes/4-vla/diffusion-policy|diffusion]],
[[01-canonical-papers/notes/4-vla/pi0|flow matching]]). (Action *representation* also varies:
absolute vs delta, joint vs end-effector space.) Aside: **offline RL** learns from a fixed
dataset too, but uses rewards to *stitch* behavior better than any single demonstrator — at
the price of value-extrapolation instability BC never has.

- **Multimodal, precisely.** The expert's action distribution $p(a \mid o)$ has more than one separated peak (mode) for the same observation. A policy trained with mean-squared error predicts the conditional *mean*, $\mu^\star(o) = E[a \mid o]$, since that is what minimizes squared error. Two experts steering $+1$ m and $-1$ m around an obstacle, equally often, give a mean of $(1 + (-1))/2 = 0$ m: straight into the obstacle, an action *neither* expert ever took. A head that represents the distribution rather than its mean (a mixture, a diffusion or flow model, or discretized action tokens) can put probability on both sides.
- **Action chunking, precisely.** The policy outputs the next $k$ actions from one observation, $\pi_\theta(a_t, a_{t+1}, \dots, a_{t+k-1} \mid o_t)$, and the robot executes several of them before querying again. A $T$-step task then needs about $T/k$ policy decisions: $500$ steps in chunks of $10$ is $50$ decisions, and at a $1\%$ per-decision error rate the illustration above moves from $0.99^{500} = 0.7\%$ to $0.99^{50} = 60.5\%$ clean. The same formula shows the cost: within a chunk, observations after $o_t$ are not used.
- **Offline RL, precisely.** Learn a policy that maximizes expected return $J(\pi)$ from a fixed dataset of transitions $\mathcal{D} = \{(s, a, r, s')\}$ collected by some other behavior policy, with **no further interaction**. It differs from BC in using $r$, so it can prefer the better parts of mediocre trajectories, and from ordinary off-policy RL in that nothing outside $\operatorname{supp}(\mathcal{D})$ can ever be tried to correct an overestimated $Q$ — hence the pessimism of [[02-foundations/rl-basics|7. RL Basics §3.5]].

> [!important] The 2024–2026 correction to this section
> The framing above — imitation is stable but capped, RL can exceed the demonstrator — is
> right, and the last two years sharpened it in a way worth carrying. On **contact-rich
> precision** tasks the gap is not narrow: **[[01-canonical-papers/notes/7-robotics/hil-serl|HIL-SERL]]** (*Science Robotics*, 2025) reports
> 100% success on around thirteen such tasks after **1–2.5 hours of real-robot training** — the
> hours are the abstract's, the success rate and the task count are body figures, as are the
> diffusion-policy baselines it beats (**27%** on RAM insertion, **18%** on dashboard assembly).
> The abstract's own headline is a 2× average over imitation and prior RL. Demonstrations do not contain the corrective micro-adjustments needed when you
> are 2 mm off, and averaging over human demos actively destroys reactive behaviour.
>
> But the honest headline for the contact-rich precision cases discussed here is not "RL beat imitation". These results —
> HIL-SERL, ConRFT ([arXiv:2502.05450](https://arxiv.org/abs/2502.05450)) and RECAP
> ([arXiv:2511.14759](https://arxiv.org/abs/2511.14759)) — each put a **human correcting the
> policy on-distribution during learning**, which is closer to [[01-canonical-papers/notes/4-vla/dagger|DAgger]]'s lineage
> than to classical RL. **Interactive learning beat offline learning, and reward is one of
> several ways to close that loop.** Two riders: every RL success above needed a hand-built
> binary reward classifier — a per-task cost invisible in a table of 100% success rates. In
> these cases, RL is best read as an interactive finishing stage rather than a demonstrated
> general-purpose training paradigm.
>
> On the imitation side the sharpest recent result is a scaling law: generalization follows
> a power law in the **number of environments and objects, not the number of demonstrations**
> (Lin et al., [arXiv:2410.18647](https://arxiv.org/abs/2410.18647); the abstract's own words are
> a "roughly power-law relationship", from over 40,000 demonstrations and more than 15,000 real
> rollouts). Past a threshold, extra demos per
> environment do almost nothing. The two paradigms are therefore not competing for the same
> resource — **RL buys precision with interaction time, imitation buys generality with scene
> diversity.**

Entry chain into the papers: this section →
[[01-canonical-papers/notes/4-vla/act|ACT]] →
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] →
[[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]] →
[[01-canonical-papers/notes/4-vla/rt-1|RT-1]]/[[01-canonical-papers/notes/4-vla/rt-2|RT-2]] →
[[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]/[[01-canonical-papers/notes/4-vla/pi0|π0]].

- Decoder ring for papers: "BC baseline" = behavior cloning; "advantage-weighted" =
  policy improvement re-weighted by $e^{A/\beta}$; "KL-regularized policy" = stay near a
  reference policy while improving.
  - The last two are one formula. The **KL-regularized objective** trades return against distance from a reference policy $\pi_{\text{ref}}$ (the pretrained or data-collecting policy), with a temperature $\beta > 0$ setting the exchange rate:
  $$\max_\pi\ E_{a \sim \pi}\big[A(s, a)\big] - \beta\, \mathrm{KL}\big(\pi(\cdot \mid s)\ \Vert\ \pi_{\text{ref}}(\cdot \mid s)\big) \quad\Rightarrow\quad \pi^*(a \mid s) = \frac{\pi_{\text{ref}}(a \mid s)\, e^{A(s,a)/\beta}}{Z(s)}$$
  where $Z(s)$ normalizes the probabilities to one; the closed form is the same Lagrange-multiplier result used for MaxEnt IRL and DPO in §6. "Advantage-weighted" methods fit $\pi_\theta$ to this $\pi^*$ by weighted BC, each logged action weighted by $e^{A/\beta}$. Worked: two actions with $\pi_{\text{ref}} = (0.5, 0.5)$, advantages $(1, 0)$ and $\beta = 0.5$ give weights $e^{2} : e^{0}$, so $\pi^* = (0.881, 0.119)$; a larger $\beta$ keeps $\pi^*$ closer to $(0.5, 0.5)$.

### 2. Reward design — the choice that decides the outcome

Supervised learning is handed its target; RL is handed a *reward someone wrote*. That
authoring step is where most robot-RL papers actually succeed or fail, and it is the part
their abstracts never mention.

- **Sparse vs dense.** A **sparse** reward (+1 when the bucket is full, 0 otherwise) is
  honest — it says exactly what you want and nothing else — but a randomly initialized
  policy may never see it. A **dense** (shaped) reward gives signal every step and learns
  far faster, at the price that you are now optimizing your *proxy* for the goal.
  - *As formulas.* A sparse reward is an indicator of a goal set $\mathcal{G}$, $r(s) = \mathbb{1}[s \in \mathcal{G}]$, nonzero on a small fraction of states. A dense reward is informative almost everywhere, typically a negative distance such as $r(s) = -\lVert x(s) - x_{\text{goal}} \rVert$ for a position $x(s)$. "Shaped" means a dense term added to the true reward, $r' = r + F$.
- **Potential-based shaping** is the one shaping form that provably cannot change the
  optimal policy: add $F = \gamma\Phi(s') - \Phi(s)$ for any function $\Phi$ of state.
  Anything else — and most papers use something else — can change what is optimal.
  - *Why it cannot* (Ng, Harada & Russell, ICML 1999). Along any trajectory the shaping terms telescope:
  $$\sum_{t=0}^{T-1} \gamma^t \big(\gamma\,\Phi(s_{t+1}) - \Phi(s_t)\big) = \gamma^T\, \Phi(s_T) - \Phi(s_0)$$
  because each $\gamma^{t+1}\Phi(s_{t+1})$ cancels the next step's $-\gamma^{t+1}\Phi(s_{t+1})$. The shaped return therefore differs from the original only by a start-state term (plus an end term that vanishes as $T \to \infty$ with bounded $\Phi$ and $\gamma < 1$), so $Q'(s, a) = Q(s, a) - \Phi(s)$ for every action: all actions in a state shift by the same amount, and the ranking of actions — hence the optimal policy — is unchanged. The condition is that $F$ depends only on a state potential; a bonus that can be collected again by looping has no such cancellation.
  - *Worked,* on the running object — the bucket MDP of [[02-foundations/rl-basics|7. RL Basics §2]] with its "wait" action — with $\Phi(A) = 0$, $\Phi(B) = 5$, $\gamma = 0.9$. Moving $A \to B$ earns $F = 0.9(5) - 0 = 4.5$; staying in $B$ earns $F = 0.9(5) - 5 = -0.5$ on top of its reward $1$. Shaped values: $V'(B) = (1 - 0.5)/(1 - 0.9) = 5 = V(B) - \Phi(B)$, and in $A$, $Q'(A, \text{move}) = 4.5 + 0.9 \times 5 = 9$ against $Q'(A, \text{wait}) = 0 + 0.9 \times 9 = 8.1$ — the same two numbers as before shaping, because $\Phi(A) = 0$, so moving is still optimal. The Worked case, part 3, runs the same check with a potential chosen to pay $+1$ on every wait.
- **A real reward is a weighted sum of terms**, $r = \sum_{j} w_j\, r_j$, where each $r_j$ measures one aspect of behavior and each weight $w_j$ is a hyperparameter carrying its sign. A digging policy's reward typically looks
  like this, and the table *is* the method section worth reading:

| Term | Purpose | Typical sign |
|---|---|---|
| task progress (soil moved, distance to target) | do the job | + |
| tracking / pose error | do it accurately | − |
| action magnitude or rate ("smoothness") | stop the policy from chattering the actuators | − |
| energy or effort | efficiency, hardware life | − |
| constraint violation (joint limit, tipping, force cap) | stay safe | − (large) |
| termination / failure penalty | end episodes meaningfully | − (large) |

- **The weights are hyperparameters, and they fight.** Take
  $r = 2.0\,\Delta d - 0.5\,\lVert a\rVert^2$. Moving 1 cm ($\Delta d = 0.01$) with a
  unit-norm action earns $2.0(0.01) - 0.5(1) = -0.48$ — **negative**, so the optimal policy
  is to *do nothing*. Degenerate "stands still and collects the smoothness bonus" solutions
  come from arithmetic exactly this simple.

<svg viewBox="0 0 460 152" style="max-width:100%;height:auto" role="img" aria-label="the two reward terms drawn to scale: the penalty dwarfs the progress term">
  <g stroke="currentColor" stroke-width="1.2" opacity="0.5"><line x1="150" y1="20" x2="150" y2="118"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="30" y1="118" x2="430" y2="118"/></g>
  <g fill="currentColor" opacity="0.22"><rect x="150" y="34" width="4" height="26"/><rect x="50" y="74" width="100" height="26"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2"><rect x="150" y="34" width="4" height="26"/><rect x="50" y="74" width="100" height="26"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="164" y="52">+0.02 &nbsp; task progress (2.0 &#215; 0.01 m)</text>
    <text x="164" y="92">&#8722;0.50 &nbsp; action penalty (0.5 &#215; 1)</text>
    <text x="30" y="140">drawn to scale: the sum is &#8722;0.48, so standing still beats digging</text>
    <text x="122" y="20" font-size="10.5" opacity="0.7">0</text>
  </g>
</svg>

- **Reward hacking** is the general form: the policy maximizes what you wrote, not what you
  meant. A velocity reward met by vibrating in place; a distance-to-goal reward met by
  circling just inside the threshold. Symptom: reward curve rises, behavior is wrong.
  The diagnostic question is always *what is the cheapest way to earn this reward?*
  - *Stated as a condition.* Let $r^\dagger$ be the reward you meant (usually unwritable) and $\hat r$ the proxy you wrote. Reward hacking is the case where optimizing the proxy succeeds on the proxy and fails on the intent:
  $$\hat\pi = \arg\max_\pi J_{\hat r}(\pi), \qquad J_{\hat r}(\hat\pi) \ \text{high}, \qquad J_{r^\dagger}(\hat\pi) \ \text{low}$$
  so it is a property of the pair (proxy, optimizer), not of either alone — the stronger the optimizer, the more reliably it finds where $\hat r$ and $r^\dagger$ disagree. The $-0.48$ example above is the simplest instance: the proxy is maximized by standing still, which scores zero on the intended digging task.
- **Reading cue**: find the reward table, count the terms, look for the weights (often only
  in an appendix), and ask which term dominates at the operating point the paper reports.
  A paper that will not show its reward has not shown its method.

### 3. Exploration — and curriculum as its scaffolding

A policy only learns from what it tries. With a sparse reward and a random start, it may
try forever and see nothing — which is why exploration, not the update rule, is usually
the binding constraint.

- **Discrete actions**: $\epsilon$-greedy — act greedily with probability $1-\epsilon$,
  uniformly at random otherwise, with $\epsilon$ decayed over training.
  - *The policy it defines,* over $|\mathcal{A}|$ actions with greedy action $a^\star = \arg\max_a Q(s, a)$:
  $$\pi(a \mid s) = \begin{cases} 1 - \epsilon + \epsilon/|\mathcal{A}| & a = a^\star \\ \epsilon/|\mathcal{A}| & a \ne a^\star \end{cases}$$
  since the random branch can also pick $a^\star$. With $\epsilon = 0.1$ and 4 actions, the greedy action has probability $0.925$ and each other action $0.025$, so every action keeps being tried.
- **Continuous actions** (the robotics case): add noise to the action (Gaussian, or
  temporally correlated Ornstein–Uhlenbeck noise — noise that drifts from its last value
  instead of being drawn fresh each step — so the machine does not jitter), or keep
  the policy **stochastic** and let it learn its own standard deviation — what PPO does.
  - *Both noises as formulas.* Gaussian exploration executes $a_t = \mu_\theta(s_t) + \sigma \varepsilon_t$ with $\varepsilon_t \sim \mathcal{N}(0, I)$ drawn fresh each step. Ornstein–Uhlenbeck noise, discretized with time step $\Delta t$, pulls toward a mean $\mu$ at rate $\theta_{\text{OU}}$ while adding fresh randomness of scale $\sigma$:
  $$x_{t+1} = x_t + \theta_{\text{OU}}\,\big(\mu - x_t\big)\,\Delta t + \sigma\sqrt{\Delta t}\;\varepsilon_t$$
  so consecutive values are correlated with coefficient $1 - \theta_{\text{OU}}\Delta t$. With DDPG's $\theta_{\text{OU}} = 0.15$ and $\Delta t = 1$ that is $0.85$, where Gaussian noise gives $0$.
- **Entropy bonus**: add $+\alpha H(\pi)$ to the objective
  ([[02-foundations/information-theory|information theory]]) so the policy is rewarded for
  staying undecided, and does not collapse early into a mediocre deterministic habit.
  [[01-canonical-papers/notes/1-foundations/sac|SAC]] promotes this from a bonus to *the*
  objective and tunes $\alpha$ automatically.
  - *Written out.* The policy's entropy in a state, $H(\pi(\cdot \mid s)) = -\sum_a \pi(a \mid s) \log \pi(a \mid s)$ ([[02-foundations/information-theory|5. Information Theory §1]]), is added to every step's reward in SAC's maximum-entropy objective:
  $$J(\pi) = E_\pi\Big[\sum_{t} \gamma^t \Big(r(s_t, a_t) + \alpha\, H\big(\pi(\cdot \mid s_t)\big)\Big)\Big]$$
  so $\alpha \ge 0$ is the exchange rate between reward and randomness. Two actions at $(0.5, 0.5)$ have $H = \ln 2 = 0.693$ nats; at $(0.9, 0.1)$, $H = 0.325$. With $\alpha = 0.1$, collapsing from the first policy to the second must gain more than $0.1 \times (0.693 - 0.325) = 0.037$ reward per step to be worth it.
- **Curriculum learning** changes the *task* instead of the algorithm: start with shallow
  digs in soft soil, raise depth and resistance once success rate passes a threshold. It is
  cheap and often does most of the work — which is exactly why it belongs in the comparison:
  if a paper's method used a curriculum and the baseline did not, the ablation is not
  measuring the method.
  - *Its components.* A curriculum is a sequence of task variants $M_1, M_2, \dots, M_K$ ending at the target task, together with an advancement rule that decides when to switch — typically "move from $M_j$ to $M_{j+1}$ once the success rate over the last $n$ episodes exceeds a threshold". Both the sequence and the rule are design choices, and both belong in the methods section.
- Its transfer-side sibling, **domain randomization**, is about robustness rather than
  exploration and lives in the [[05-construction-robotics/sim-to-real|sim-to-real guide]].

### 4. RL on a real machine: fine-tuning, safety, and where sim-to-real sits

- **RL fine-tuning (RLFT)** is how RL now most often reaches robots — and how you will
  meet it in this wiki. Start from a policy already pretrained by behavior cloning (or an
  earlier RL run), then continue with RL on task reward. Pretraining puts you in a region
  where exploration is not hopeless; RL then fixes what the demonstrations could not cover.
  It is the same shape as [[01-canonical-papers/notes/1-foundations/instructgpt|pretrain → RLHF]],
  and it is what [[01-canonical-papers/notes/8-construction/ext|ExT]]'s SFT/RLFT stage does
  on an excavator.
- **Keep it near the reference.** RLFT is usually regularized by a KL term back to the
  pretrained policy. Drift too far and you lose what pretraining bought — and reward
  hacking becomes likely, because the reward was never meant to define the whole behavior.
  - *The RLFT objective.* Starting from the pretrained parameters $\theta_0$, with $\pi_{\text{ref}} = \pi_{\theta_0}$ kept frozen:
  $$\max_\theta\ E_{\pi_\theta}\Big[\sum_t \gamma^t\, r(s_t, a_t)\Big] - \beta\, E_{s \sim d_{\pi_\theta}}\Big[\mathrm{KL}\big(\pi_\theta(\cdot \mid s)\ \Vert\ \pi_{\text{ref}}(\cdot \mid s)\big)\Big]$$
  so $\beta$ sets how much task reward one unit of drift must buy. $\beta \to \infty$ returns the pretrained policy unchanged, and $\beta = 0$ is plain RL that has merely been initialized well. Its optimum has the exponential-tilting form given in the §1 decoder ring.
- **Safety while learning** has only a few honest answers, and reward penalties are the
  weakest of them:
  1. train in simulation (dominant — a 12-tonne machine cannot "try and correct");
  2. wrap the policy in a **safety filter / envelope** that clips or vetoes unsafe commands
     before they reach the actuator ([[04-robotics/mpc|MPC]] is often that filter);
  3. formulate a **constrained MDP** — an MDP with a second, cost signal whose expected total
     must stay under a limit — and optimize reward subject to that bound (Lagrangian methods,
     which fold the limit into the objective with a multiplier, as in
     [[02-foundations/optimization|optimization §4]]);
  4. penalize violations in the reward — convenient, and it guarantees **nothing**: a large
     enough task reward will buy the penalty.

  *Mechanisms 2 to 4 as formulas.* A **safety filter** replaces the policy's command $a_\pi$ with the closest command in a safe set $\mathcal{C}(s)$ that the filter can certify:
  $$a_{\text{safe}} = \arg\min_{a \in \mathcal{C}(s)} \lVert a - a_\pi \rVert^2$$
  so a safe command passes unchanged and an unsafe one is projected to the boundary; with a speed limit $\mathcal{C} = [-0.5, 0.5]$ m/s, a requested $0.8$ m/s is executed as $0.5$. The guarantee holds whatever the policy outputs, because it is enforced after the policy. A **constrained MDP** adds a cost function $c(s, a) \ge 0$ and a limit $d$, and its Lagrangian relaxation introduces a multiplier $\lambda \ge 0$:
  $$\max_\pi\ J_r(\pi) \ \ \text{s.t.}\ \ J_c(\pi) \le d, \qquad \mathcal{L}(\pi, \lambda) = J_r(\pi) - \lambda\,\big(J_c(\pi) - d\big)$$
  where $J_r$ and $J_c$ are expected discounted totals of reward and cost. Lagrangian methods alternate improving $\pi$ on $\mathcal{L}$ with *raising* $\lambda$ while the constraint is violated. **Worked, and the non-example it exposes.** Two policies: $\pi_1$ with $J_r = 10$, $J_c = 3$; $\pi_2$ with $J_r = 8$, $J_c = 1$; limit $d = 2$. The constrained answer is $\pi_2$, the only feasible one. A fixed reward penalty of $0.5$ per unit of cost scores them $10 - 1.5 = 8.5$ and $8 - 0.5 = 7.5$ and picks the *violating* $\pi_1$ — mechanism 4 failing exactly as stated. The Lagrangian scores are $10 - \lambda$ and $8 + \lambda$, so once $\lambda$ has been raised past $1$ it prefers $\pi_2$; the multiplier is a penalty weight that is adjusted until the constraint holds, rather than guessed.
- **The real cost is not compute.** On hardware, every episode needs a reset, resets are
  human labor, and wear and safety review are real budgets
  ([[04-robotics/hri-safety|HRI & safety]]).
- The transfer half of this story — reality gap, randomization, privileged learning,
  residuals, the deployment ladder — is the
  [[05-construction-robotics/sim-to-real|Sim-to-Real guide]]. Read it right after this page
  if your interest is robots rather than language models.

### 5. Reading an RL experimental section

RL results depend on protocol more than those of almost any other subfield. What to check:

| Paper phrase | What to check |
|---|---|
| "trained for $2\times10^9$ environment steps" | steps ≠ time, and steps ≠ real experience — how many parallel environments, and simulated or real? |
| "sample-efficient" | measured in environment steps, wall-clock, or *real machine hours*? Only the last is scarce |
| "outperforms PPO/SAC baseline" | same reward, same observation space, same curriculum, same tuning budget? |
| learning curve | x-axis units, number of seeds, and whether the shaded band is std, standard error, or a CI ([[02-foundations/ml-practice\|ML practice §4]]) |
| "we use PPO" | the optimizer name specifies almost nothing — the reward, observations and curriculum do ([[01-canonical-papers/notes/1-foundations/ppo\|PPO note]]) |
| "zero-shot transfer" | no target-domain training update — but the simulator was probably built from real data |
| success rate | how many evaluation episodes, from what initial-state distribution, under what time limit |

- **Scale, in numbers.** $2\times10^9$ steps sounds enormous. With 4,096 parallel
  environments that is 488,000 steps each; at a 50 Hz control rate, 9,760 s ≈ **2.7 hours of
  simulated experience per environment** — a few GPU-hours. The identical number on *one
  real machine* at 50 Hz would be **1.3 years**. That ratio is the whole reason robot RL
  lives in simulation.
- **Observation and action spaces are part of the result.** What the policy sees (joint
  states? terrain heightmap? privileged soil parameters?) and what it emits (joint
  velocities? valve currents? end-effector poses?) change the problem more than the
  algorithm does. Observation **normalization statistics are part of the model** — shipping
  a policy without them is a classic silent deployment failure.
- **Episode termination and time limits.** Ending an episode because the task failed and
  ending it because the clock ran out are different: the second should still bootstrap the
  value function, and treating it as terminal quietly teaches the policy that the world
  ends at the time limit.
  - *In the TD target.* Implementations carry a flag $d \in \{0, 1\}$ per transition and compute
  $$y = r + \gamma\,(1 - d)\, V(s')$$
  so $d = 1$ drops the future. **Termination** (the task truly ended: the goal was reached, or the machine tipped) sets $d = 1$. **Truncation** (the clock ran out in a state from which the task would continue) must keep $d = 0$, because $s'$ still has a future. Worked: $r = 1$, $\gamma = 0.99$, $V(s') = 10$ gives a bootstrapped target of $10.9$; marking the time-out as terminal gives $1$, less than a tenth of the correct target, for every state near the limit.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> An RL result is a claim about a *reward, an observation space, a simulator, a curriculum,
> an exploration scheme, and an evaluation protocol* — the algorithm name is the least
> informative part of it. Before comparing two RL papers, check that those six match; when
> they do not, you are comparing problem definitions, not methods.
> RL 결과는 *보상·관측 공간·시뮬레이터·커리큘럼·탐색 방식·평가 규약*에 대한 주장이고,
> 알고리즘 이름이 그중 가장 정보가 적다. 두 RL 논문을 비교하기 전에 이 여섯이 일치하는지
> 확인하라 — 일치하지 않으면 방법이 아니라 문제 정의를 비교하는 것이다.

### 6. Learning the reward: inverse RL and preferences

*In one sentence:* when nobody can write the goal down as a score, the score itself can be learned from what a person does or from which of two attempts they prefer — but many different scores explain the same behaviour, so each method is a rule for picking one of them, and the learned score still has to be optimized afterwards.

*If you need only one thing from this section:* the Bradley–Terry model $P(A \succ B)=\sigma\big(R(A)-R(B)\big)$, fitted as logistic regression on reward differences — it is the reward model behind RLHF and the loss DPO rewrites, and in §6.3's worked example one answer "A is better" moves $w$ from $(0.2,\ 0.6)$ to $(0.499,\ 0.301)$ and lowers the loss from $0.913$ to $0.599$.

§2 treated the reward as something an engineer writes. Sometimes nobody can write it down,
but someone can *show* the behaviour, or say which of two attempts was better. Then the
reward itself becomes the thing to learn.

**Why learn a reward instead of copying actions.** Behaviour cloning copies actions, and §1
showed where that breaks: the policy drifts into states its demos never covered, and errors
compound. A learned reward carries different information.

- It says *why* the expert acted — what they were trading off — not only *what* they did.
- It transfers. Optimize the same reward under different dynamics, on a different robot, or
  from a start state no demo began in, and you still get sensible behaviour; a cloned
  state-to-action map has nothing to say there.
- It can let the learner do better than an expert who was suboptimal or differently capable.

The price is RL again: a learned reward is only useful once you optimize a policy against it.

**The ambiguity every method has to break.** "The expert is optimal for some reward" does not
pin the reward down. $r = 0$ makes every policy optimal, the expert included. So does any
positive rescaling of the true reward, and so does adding the potential-based shaping term of
§2. Read each method below as one *principle for choosing* among the many rewards that
explain the same data.

#### 6.1 Feature matching and max-margin planning

**Feature matching.** Assume a linear reward over hand-chosen features,
$r(s,a) = w^\top\phi(s,a)$. A policy's expected return is then $w^\top\mu(\pi)$, where
$\mu(\pi)$ is its discounted feature expectation:

$$\mu(\pi) = E_\pi\Big[\sum_{t} \gamma^t\,\phi(s_t,a_t)\Big]$$

The return factors this way because the reward is linear, so $w$ comes out of the
expectation. The useful consequence: if a learner's $\mu$ is within $\epsilon$ of the
expert's, then for *every* $w$ with $\lVert w\rVert \le 1$ its return is within $\epsilon$
of the expert's. Writing $\mu_L$ and $\mu_E$ for the learner's and the expert's feature
expectations, Cauchy–Schwarz gives
$|w^\top\mu_L - w^\top\mu_E| \le \lVert w\rVert\,\lVert\mu_L - \mu_E\rVert \le 1 \cdot \epsilon$. Matching features guarantees expert-level return without
ever recovering the true $w$. Concretely: instead of memorizing "turn right at this
intersection" (useless at an intersection the expert never drove through), notice that the
expert's routes avoid stop signs and favour high speed limits, and seek routes with the same
feature counts. **Max-margin planning** (Ratliff, Bagnell & Zinkevich, ICML 2006) turns this
into a quadratic program: choose the smallest $w$ under which the expert beats every other
candidate policy by a margin that grows with how different that policy is, with a slack
variable for an imperfect expert. In symbols, with $\mu_E$ the expert's feature expectations, $\mu(\pi)$ a candidate's, $\ell(\pi) \ge 0$ a loss measuring how different $\pi$ is from the expert, and slack $\xi \ge 0$ weighted by $C$:
$$\min_{w,\ \xi \ge 0}\ \tfrac12 \lVert w \rVert^2 + C\,\xi \quad \text{s.t.} \quad w^\top \mu_E \ \ge\ w^\top \mu(\pi) + \ell(\pi) - \xi \quad \text{for every candidate } \pi$$
so minimizing $\lVert w\rVert$ picks the least extreme reward that still separates the expert, which is how this method breaks the scaling ambiguity. The discounted feature expectation itself is a concrete number: features $\phi = 1, 0, 1$ at steps $0, 1, 2$ with $\gamma = 0.9$ give $\mu = 1 + 0 + 0.81 = 1.81$.

#### 6.2 Maximum-entropy IRL and GAIL

**Maximum-entropy IRL** (Ziebart, Maas, Bagnell & Dey, AAAI 2008). Feature matching still
leaves ambiguity one level up: many trajectory distributions share the same feature
expectations, and some of them prefer particular paths for no reason the features give.
MaxEnt's principle is to commit to nothing the features do not demand — among all
distributions that match the expert's feature counts, take the one with maximum entropy
([[02-foundations/information-theory|information theory]]).

*The model.* Maximizing entropy subject to matching an expected feature count is a
Lagrange-multiplier problem ([[02-foundations/optimization|4. Optimization §4]]), and its
solution is always exponential in the constrained features, with the multiplier on the
feature constraint playing the role of $w$. So the solution is exponential in
the reward, with $f(\tau) = \sum_t \phi(s_t,a_t)$ the trajectory's feature count:

$$P_w(\tau) = \frac{\exp\big(w^\top f(\tau)\big)}{Z(w)}, \qquad Z(w) = \sum_{\tau}\exp\big(w^\top f(\tau)\big)$$

Read it as a noisy expert: since probability grows exponentially with reward, better
trajectories are exponentially more likely, but worse ones are never impossible.

*Fitting.* Fit $w$ by
maximum likelihood on $N$ demonstrations $\tau_1,\dots,\tau_N$:

$$\nabla_w \log \prod_{i} P_w(\tau_i) = \sum_{i=1}^{N} f(\tau_i) - N\,E_{\tau\sim P_w}\big[f(\tau)\big]$$

The second term appears because the derivative of $\log Z(w)$ is the model's own expected
feature count, so the gradient is *expert feature counts minus what the current model
expects*, and it vanishes exactly when the features match.

*The cost.* **It is all in that second
term.** It is an expectation over every trajectory the current reward makes likely, so each
gradient step needs a full planning pass under the current $w$. Ziebart et al. compute it
with a backward pass (a soft, log-sum-exp form of value iteration) and a forward pass for
state-visitation frequencies; with a sampler instead, it is a forward RL run. The outer loop
learns the reward, and the inner loop solves an RL problem every time — tractable in small
discrete worlds, expensive anywhere larger.

*The adversarial version.* **GAIL** (Ho & Ermon, NeurIPS 2016) is the
adversarial descendant: a discriminator that tells expert state-action pairs from the
policy's plays the role of the learned reward, and the policy is trained against it with RL,
without recovering an explicit reward first. Its saddle-point objective, with discriminator $D(s, a) \in (0, 1)$ scoring how *policy-like* a pair is, expert policy $\pi_E$, and entropy weight $\lambda \ge 0$:
$$\min_\pi\ \max_D\ \ E_{\pi}\big[\log D(s, a)\big] + E_{\pi_E}\big[\log\big(1 - D(s, a)\big)\big] - \lambda\, H(\pi)$$
so $D$ is trained to tell the two apart and $\pi$ is trained, by RL with cost $\log D(s, a)$, to make its pairs indistinguishable from the expert's. When no discriminator can do better than chance, $D = 0.5$ everywhere and the policy's state-action distribution matches the expert's — distribution matching, the same goal as feature matching without hand-chosen features.

> [!example] Worked example · 계산 예제
> Two trajectories with a scalar feature, $f(\tau_1) = 2$ and $f(\tau_2) = 1$. The expert
> was recorded four times: $\tau_1$ three times, $\tau_2$ once, so the expert feature sum is
> $3(2) + 1 = 7$ (mean $1.75$).
>
> - **At $w = 0$** both trajectories have probability $0.5$, the model expects $f = 1.5$, and
>   the gradient is $7 - 4(1.5) = 1.0$ — positive, so raise $w$.
> - **At $w = 1$**, $P(\tau_1) = e^{2}/(e^{2} + e^{1}) = 0.731$, expected $f = 1.731$, and the
>   gradient shrinks to $7 - 4(1.731) = 0.076$.
> - **At $w = \ln 3 \approx 1.099$**, $P(\tau_1) = 0.75$ — the expert's own frequency — expected
>   $f = 1.75$, and the gradient is exactly $0$.
>
> Two readings. The fitted model reproduces the expert's 3-to-1 mix rather than always picking
> $\tau_1$, which is the "never impossible" of the exponential form. And if all four demos had
> been $\tau_1$, the gradient $8 - 4E[f]$ would stay positive for every $w$ because $E[f] < 2$,
> so $w$ would grow without bound — a perfectly consistent expert reads as infinitely
> confident, which is why practical fits regularize $w$.

#### 6.3 Preferences: Bradley–Terry, RLHF and DPO

**Preferences instead of demonstrations.** Demonstrations are sometimes the wrong ask: a
high-dimensional arm is hard to teleoperate well, and people who demonstrate driving in
simulation have been found to prefer a more defensive style than the one they demonstrated (Basu et al., HRI 2017).
Comparing two attempts is easier. The standard model is **Bradley–Terry** (Bradley & Terry,
*Biometrika*, 1952):

$$P(A \succ B) = \sigma\big(R(A) - R(B)\big) = \frac{1}{1 + e^{-(R(A) - R(B))}}$$

Only the difference enters, so adding the same constant to every reward changes nothing —
the ambiguity again, this time as a shift. Fitting it means maximizing
$\log\sigma(R(A) - R(B))$ over labelled pairs, which is **logistic regression on reward
differences**. Logistic regression is the basic yes/no classifier: it predicts a probability
as the sigmoid of a linear score and fits the weights by maximizing exactly this kind of
log-likelihood (equivalently, minimizing cross-entropy; see
[[02-foundations/information-theory|5. Information Theory §2]]). For labelled examples $(x_i, y_i)$ with $y_i \in \{0, 1\}$:
$$P(y = 1 \mid x) = \sigma\big(w^\top x\big), \qquad \max_w \sum_i \Big[y_i \log \sigma\big(w^\top x_i\big) + (1 - y_i)\log\big(1 - \sigma(w^\top x_i)\big)\Big]$$
since each example contributes the log-probability of the label it actually has; its gradient is $\sum_i (y_i - \sigma(w^\top x_i))\,x_i$, error times input, which is the update the worked example below uses. With a linear reward, $R(A) - R(B) = w^\top(\phi(A) - \phi(B))$, so each
comparison is one logistic-regression example whose input is the feature difference, and a
noise-free answer cuts the space of possible $w$ in half along the hyperplane
$w^\top(\phi(A) - \phi(B)) = 0$.

- **Deep RL from human preferences** (Christiano et al., NeurIPS 2017) replaces the linear
  reward with a neural network fitted to human comparisons of short clips of behaviour,
  trains the policy with RL against it, and keeps asking for new comparisons as the policy
  changes.
- **This is the RLHF reward model.** [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]]
  trains its reward model with a pairwise ranking loss of this form on labeler rankings, then
  optimizes the policy against it with PPO ([[02-foundations/rl-basics|7. RL Basics §4]]) under a KL penalty (§4).
- **DPO** (Rafailov et al., NeurIPS 2023) removes the explicit reward model: for the
  KL-regularized objective the optimal policy determines the reward, so the Bradley–Terry loss
  can be written directly in policy log-probability ratios and trained without an RL loop.
  The derivation takes three lines.
  - For one prompt, the policy that maximizes
    $E_{y\sim\pi}[r(y)] - \beta\,\mathrm{KL}(\pi \Vert \pi_{\text{ref}})$ is
    $\pi^*(y) = \pi_{\text{ref}}(y)\,e^{r(y)/\beta}/Z$, with $Z$ the normalizer. This is the
    same exponential form as MaxEnt above, for the same Lagrange-multiplier reason.
  - Take logs and solve for the reward:
    $r(y) = \beta\log\big(\pi^*(y)/\pi_{\text{ref}}(y)\big) + \beta\log Z$.
  - Substitute into Bradley–Terry. $A$ and $B$ answer the same prompt, so they share $Z$, and
    $\beta\log Z$ cancels in $r(A) - r(B)$. What remains,
    $\sigma\big(\beta\log\frac{\pi(A)}{\pi_{\text{ref}}(A)} - \beta\log\frac{\pi(B)}{\pi_{\text{ref}}(B)}\big)$,
    involves only the policy being trained and the frozen reference.
  - The resulting **DPO loss**, averaged over preference triples of a prompt $x$, a preferred answer $y_w$ and a rejected answer $y_l$:
    $$\mathcal{L}_{\text{DPO}}(\theta) = -E_{(x, y_w, y_l)}\Big[\log \sigma\Big(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\Big)\Big]$$
    so it is the Bradley–Terry negative log-likelihood with $\beta \log(\pi_\theta/\pi_{\text{ref}})$ playing the reward. Worked: $\beta = 0.1$, log-ratio $+2.0$ for the preferred answer and $-1.0$ for the rejected one give $\sigma(0.2 + 0.1) = \sigma(0.3) = 0.574$ and loss $0.554$; the gradient raises the preferred answer's log-ratio and lowers the rejected one's until that probability approaches 1.
- **Active queries for robots** (Sadigh et al., RSS 2017, "Active Preference-Based Learning
  of Reward Functions"): since each answer is only one bit, choose the pair to show so that
  the answer removes as much as possible of the remaining plausible reward weights.

> [!example] Worked example · 계산 예제
> Linear reward, features $\phi(A) = (1, 0)$, $\phi(B) = (0, 1)$, current weights
> $w = (0.2, 0.6)$. So $R(A) = 0.2$, $R(B) = 0.6$, and the model predicts
> $P(A \succ B) = \sigma(-0.4) = 0.401$.
>
> The person says **A is better**. The log-likelihood gradient is
> $(1 - 0.401)\,(\phi(A) - \phi(B)) = (0.599, -0.599)$ — the error times the feature difference,
> exactly as in logistic regression. One step of size $0.5$:
>
> - $w \leftarrow (0.2, 0.6) + 0.5\,(0.599, -0.599) = (0.499, 0.301)$;
> - the prediction becomes $\sigma(0.199) = 0.550$, and the loss $-\log P$ falls from $0.913$
>   to $0.599$.
>
> The step size scales with $1 - P$, how surprised the model was; a comparison the model
> already predicted with $P$ near 1 barely moves $w$.

#### 6.4 Reading a reward-learning paper

**Reading a reward-learning paper.** Four questions, in order:

| Question | What to check |
|---|---|
| What data? | demonstrations, pairwise comparisons or rankings, physical corrections — how many, and from whom (experts, crowd workers, the authors) |
| What reward class? | linear over hand-designed features (inspectable, but the features carry most of the expertise) vs a neural network (expressive, data-hungry, hard to inspect) |
| How is it evaluated? | ① the recovered reward against a known true reward (possible only in simulation); ② a policy trained on the learned reward, scored on the *true* task metric; ③ accuracy on held-out preferences. They answer different questions: high ③ does not by itself show good ② |
| What stops reward hacking? | a learned reward is a proxy exactly like a hand-written one (§2), and it is least reliable where it saw no data — which is where an optimizing policy goes. Look for a KL anchor to a reference policy (§4) or continued querying as the policy changes |

### 7. More than one learner, briefly

Everything above assumes one learner in a stationary world. A site has several machines, so it is worth knowing exactly which assumption breaks and what the field does about it. This section is Literacy depth: enough to read a multi-agent paper and to recognize when the problem is not one.

**What breaks, on this page's own object.** Put two machines in the bucket MDP with one loading spot at $B$. Alone, moving is worth $Q^*(A,\text{move})=9$ and waiting $8.1$. If both move at once they collide, bounce back to $A$ and pay a repair cost of $1$, so each gets $7.1$. Then machine 1's value of moving depends on how often machine 2 moves, $p$:

$$Q_1(\text{move})=(1-p)\cdot 9+p\cdot 7.1=9-1.9p,\qquad Q_1(\text{wait})=8.1$$

so moving is better exactly while $p<0.9/1.9=0.474$. Nothing in the world changed, yet machine 1's optimal action flips when machine 2 learns — the transition and reward the MDP of [[02-foundations/rl-basics|7. RL Basics §1]] assumes to be *fixed* now contain another policy that is moving. This is **non-stationarity**, the defining difficulty of multi-agent learning, and it is why two independent learners can chase each other around $p=0.474$ instead of settling. The game also has two pure equilibria — one moves, the other waits — so "which machine yields" is a coordination choice that the reward alone does not make.

**Two more costs.** The joint action space multiplies: $n$ machines with $|\mathcal A|$ actions each give $|\mathcal A|^n$ joint actions, so five machines with ten actions each is $10^5$ — a critic over joint actions stops being tabular immediately. And a shared reward hides **credit assignment**: if the site's throughput rises, which machine caused it? Per-agent rewards fix attribution and create incentives to hoard; shared rewards do the opposite.

**What the field does.** The standard compromise is **centralized training, decentralized execution**: during training a critic sees every agent's observation and action, while each policy at run time sees only its own — so the critic is stationary even though each agent's world is not, and deployment still needs no shared channel. Value factorization (summing per-agent values, or mixing them monotonically) buys a decentralized argmax from a joint value; a shared critic with per-agent policies is the policy-gradient version. Parameter sharing across identical machines cuts the sample cost. Read a paper for four things: how many agents at training versus at test, whether execution is really decentralized, whether the baseline is *independent learners* rather than a single-agent method, and whether the reward is shared or per-agent.

**When it is not the problem.** Coordination often has a control answer that needs no learning at all: [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §8]] couples one leader to several followers with passivity-preserving couplings plus an avoidance function, and construction fleets today are supervised centrally rather than trained jointly ([[05-construction-robotics/lineage|lineage, Era 3]]). For the research program here the core is one manipulator in contact ([[07-research-program/index|7. §7]]), so multi-agent learning stays at Literacy: know the failure mode, and reach for it only if the contribution is the coordination itself.

### 8. Group-relative RL: reasoning models, and VLAs that learn from success

The reasoning language models of 2025 were trained with a policy-gradient method whose shape fits robots unusually well. DeepSeek-R1-Zero learned to reason from reinforcement learning alone, with rewards a program can check — was the final answer right, was the format kept — and no human-written reasoning traces; self-reflection and verification emerged along the way ([DeepSeek-AI, *Nature* 645, 2025](https://arxiv.org/abs/2501.12948)). The optimizer was GRPO.

> **Group-relative policy optimization, defined.** **GRPO** is a *policy-gradient estimator whose baseline is a group of samples from the same starting point* rather than a learned value function. Three defining conditions. For each prompt or start state it **samples a group of $G$ outcomes from the current policy**. Each outcome's **advantage is its reward standardized within the group**, so no critic network is trained. And the policy is **updated with PPO's clipped ratio** ([[02-foundations/rl-basics|7. RL Basics §4]]), with a KL penalty to a reference policy added to the loss rather than to the reward.
>
> $$\hat A_i=\frac{r_i-\operatorname{mean}(r_1,\dots,r_G)}{\operatorname{std}(r_1,\dots,r_G)},\qquad J(\theta)=\mathbb E\Big[\frac1G\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t}\min\big(\rho_{i,t}\hat A_i,\ \operatorname{clip}(\rho_{i,t},1-\varepsilon,1+\varepsilon)\,\hat A_i\big)-\beta\,D_{\mathrm{KL}}\big(\pi_\theta\,\Vert\,\pi_{\text{ref}}\big)\Big]$$
>
> where $o_i$ is the $i$-th sampled output, $|o_i|$ its length in tokens or steps, and $\rho_{i,t}$ the ratio of the new policy's probability for its $t$-th token to the old policy's — so every token of an output shares that output's advantage.
>
> - **Example**: DeepSeekMath, where GRPO was introduced: RL on English instruction data lifted GSM8K from $82.9\%$ to $88.2\%$ and MATH from $46.8\%$ to $51.7\%$ ([Shao et al., 2024](https://arxiv.org/abs/2402.03300)).
> - **Non-example**: PPO with a critic. Its baseline is a value network $V_\psi$ trained alongside the policy, which is the memory GRPO saves.
> - **Non-example**: DPO (§6.3). It samples nothing and computes no reward; it learns from a fixed set of preference pairs.

**On the bucket MDP, by hand.** Reward a rollout $1$ if the policy moves the bucket at once from $A$ and $0$ if it waits. Four rollouts from $A$ — move, wait, wait, move — give rewards $(1,0,0,1)$, mean $0.5$, standard deviation $0.5$, and advantages $(+1,-1,-1,+1)$: two pushes up on $\log\pi(\text{move}\mid A)$ and two down on $\log\pi(\text{wait}\mid A)$. [[02-foundations/rl-basics|7. RL Basics §4]] took its baseline $b=0.6$ from a known policy; GRPO estimates it from the group. Two other groups show what the estimator does. One success in four, $(1,0,0,0)$, gets $+1.73$ against $-0.58$ for each failure: a rare success is pushed hard. Four successes, $(1,1,1,1)$, have a standard deviation of zero, so no member differs from the mean and the group teaches nothing — the same holds for four failures. (These use the population standard deviation; the sample form, dividing by $G-1$, scales every advantage here by $\sqrt{3/4}$ and changes no sign.)

**Why it fits robots.** A robot's most natural reward is a binary success check, and its most natural group is one start state rolled out several times. RIPT-VLA post-trains pretrained VLAs from sparse binary success alone, with dynamic rollout sampling that drops the uninformative all-same groups and a leave-one-out advantage; it reports QueST improved by $21.2\%$ and OpenVLA-OFT raised to $97.5\%$ ([Tan et al., 2025](https://arxiv.org/abs/2505.17016)). VLA-RL treats a manipulation trajectory as a multi-turn conversation so that an autoregressive VLA can be trained online at the trajectory level ([Lu et al., 2025](https://arxiv.org/abs/2505.18719)). The reasoning models also showed that thinking longer can be bought at test time: s1 fine-tuned on only $1{,}000$ curated examples and controlled its thinking by "budget forcing" — cutting it short, or appending *Wait* to lengthen it ([Muennighoff et al., 2025](https://arxiv.org/abs/2501.19393)). On a robot that extra thinking is paid in rate, the cost counted in [[03-deep-learning/vla/index|4. VLA §6]].

**What to ask of a group-relative robot paper**, beside §5's checklist: where the rollouts ran, simulation or the real machine, and how many went into each update; what decides success, since the success detector *is* the reward; the group size, and what happened to groups that all succeeded or all failed; the KL reference; and whether the gain held on the real robot at its control rate.

### After reading

- [ ] Compute a behaviour-cloned policy's value on the bucket and its gap to the optimum, and say what DAgger changes about BC's training distribution.
- [ ] Explain why plain BC's cost grows as $O(\epsilon T^2)$ and a no-regret learner's as $O(\epsilon T)$, and what action chunking does to $T$.
- [ ] Find the idle bonus at which a written reward flips the optimum, and show why a potential-based term that pays the same bonus cannot flip it.
- [ ] Write the KL-regularized fine-tuning objective and its exponential-tilting optimum, and say what $\beta \to 0$ and $\beta \to \infty$ return.
- [ ] Say why a reward penalty is not a safety guarantee, and name the two mechanisms that are stronger.
- [ ] Convert a paper's environment-step count into simulated hours per environment and real-machine time, and tell termination from truncation in a TD target.
- [ ] Take one Bradley–Terry gradient step by hand, and derive the DPO loss from the KL-regularized optimum.
- [ ] On the two-machine bucket, find the probability at which the other machine's policy flips your own best action, and say what centralized training with decentralized execution buys.
- [ ] Compute GRPO advantages for a group of binary outcomes by hand, say why an all-success group teaches nothing, and list what to ask of a robot paper that uses it.

> [!tip] Going deeper · 더 깊이
> Sutton and Barto's [*Reinforcement Learning: An Introduction*](http://incompleteideas.net/book/the-book.html) is the book [[02-foundations/rl-basics|7. RL Basics]] compresses. It does not cover §1 and §4 — imitation against RL, and RL on a physical machine — which is what this page adds. The primary sources, section by section, are under Sources below.

### Self-check

1. Why does action chunking reduce compounding error, and what does it trade away?
2. A reward is $r = 1.0\,\Delta d - 0.2\lVert a\rVert^2 - 5.0\,\mathbb{1}[\text{limit hit}]$.
   The policy learns to freeze at the start. Give the arithmetic reason, and one fix.
3. A paper's method uses a curriculum; its PPO baseline does not. What has the ablation
   actually measured?
4. Why is "penalize constraint violations in the reward" not a safety guarantee, and what
   are two mechanisms that are stronger?
5. A paper reports $1\times10^9$ environment steps with 2,048 parallel environments at
   100 Hz. How much simulated experience is that per environment, and how long would the
   same number take on one real machine?
6. An expert is optimal for some reward $r$. Name two other rewards under which the same
   behaviour is optimal, and state the principle MaxEnt IRL uses to choose among them.
7. MaxEnt IRL with two trajectories, $f(\tau_1) = 3$, $f(\tau_2) = 1$, and one demonstration
   of $\tau_1$. What is the log-likelihood gradient at $w = 0$, and what happens to $w$ if you
   keep following it?
8. A reward model gives $R(A) = 2.0$ and $R(B) = 1.0$. What does Bradley–Terry predict for
   $P(A \succ B)$, and what changes if every reward is shifted by $+10$? The paper reports 95%
   held-out preference accuracy — why is that not yet evidence that the robot policy works?
9. A VLA post-trained with GRPO on binary success rises from $60\%$ to $90\%$ in simulation. With groups of eight, most groups are now all-success. What is the estimator doing, and what would you change?

> [!tip]- Answers
> 1. Predicting $k$ actions at once cuts by a factor of $k$ the number of times the policy re-conditions on its own (possibly drifted) state, so off-distribution drift accumulates more slowly. The trade is reactivity: during chunk execution new observations are only partially incorporated (or not at all), so a disturbance mid-chunk is answered late.
> 2. Any motion costs the smoothness term immediately while the progress term pays only $1.0\Delta d$; for a unit-norm action, moving 1 cm earns $0.01 - 0.2 = -0.19$, so standing still (reward 0) is optimal. Fixes: raise the progress weight or rescale $\Delta d$ to comparable units, penalize *action rate* rather than magnitude, or add a small per-step alive/idle penalty so doing nothing is not free.
> 3. The difference between (method + curriculum) and (baseline without curriculum) — that is, it measured the curriculum and the method together. The comparison isolates nothing unless the baseline gets the same curriculum.
> 4. Because it is a soft trade: a large enough task reward simply buys the penalty, and nothing bounds violations during the exploration that precedes learning. Stronger: a safety filter/envelope that vetoes unsafe commands before the actuator (often an MPC), and a constrained-MDP formulation that optimizes reward subject to an explicit bound on expected violation.
> 5. $1\times10^9/2{,}048 \approx 488{,}000$ steps per environment; at 100 Hz that is 4,880 s ≈ **1.4 hours** of simulated experience each. On one real machine at 100 Hz: $10^9/100 = 10^7$ s ≈ **116 days**.
> 6. $r = 0$ (every policy is optimal), any positive rescaling such as $2r$, or $r$ plus a potential-based shaping term $\gamma\Phi(s') - \Phi(s)$ (§2). MaxEnt IRL keeps only distributions that match the expert's feature counts and, among those, takes the maximum-entropy one; that fixes an exponential-family model $P_w(\tau) \propto \exp(w^\top f(\tau))$ whose $w$ is fitted by maximum likelihood.
> 7. At $w = 0$ both trajectories have probability $0.5$, so the model expects $f = 2$ and the gradient is $3 - 2 = 1$. Because $E[f] < 3$ for every finite $w$, the gradient never reaches zero and $w$ grows without bound; only a regularizer, or a demonstration of $\tau_2$, gives a finite answer.
> 8. $\sigma(2.0 - 1.0) = \sigma(1) = 0.731$. The shift changes nothing, since only the difference enters. Held-out accuracy is measured on pairs drawn from the data the model was trained near; a policy optimized against the model moves toward behaviour where the model has seen nothing and can be exploited (reward hacking, §2). The evidence that counts is a policy trained on the learned reward and scored on the true task metric.
> 9. An all-success group has zero spread, so every member's advantage is zero and the group contributes no gradient: learning stops exactly where the policy has become good, and the remaining failures sit in the few mixed groups. Keep the informative groups — RIPT-VLA's dynamic rollout sampling drops the all-same ones — draw harder start states, or enlarge the group; then check the gain on the real robot at its control rate, since the simulator's success detector was the whole reward.

### Problem set · 과제

Tier B. The running object with two knobs changed: discount $\gamma = 0.95$, and a second operator whose record at $A$ holds four moves and two waits. No simulator; every item is a hand derivation on the bucket, using §1, §2 and this page's Worked case.

1. **Draw.** The picture for this variant: the MDP with every reward and $\gamma = 0.95$, the values $V^*(A)$, $V^*(B)$ and $Q^*(A,\text{wait})$ beside it, the second operator's record with its BC policy and value, and panel 2 redrawn for $\gamma = 0.95$ — the written value of moving now and of waiting forever against the idle bonus $b$, where they cross, and the task value of the written optimum.
2. **Derive.** (a) $V^*(B)$, $V^*(A)$ and $Q^*(A,\text{wait})$ at $\gamma = 0.95$. (b) $\pi_{\text{BC}}(\text{move}\mid A)$ and $V^{\text{BC}}(A)$ for the second record, and the gap to $V^*(A)$. (c) The idle bonus $b$ at which the written optimum flips to waiting forever; show that it equals $\gamma$ whatever the record. (d) The potential with $\Phi(B) = 0$ whose shaping term pays exactly $1$ on every wait: find $\Phi(A)$, what the move then earns, and both shaped action values in $A$, and confirm that the ranking is unchanged. (e) One KL-regularized improvement step from $\pi_{\text{ref}} = \pi_{\text{BC}}$ with $\beta = 0.5$, using the closed form of §1's decoder ring and the optimum's advantages in $A$, $A^*(A,\text{move}) = 0$ and $A^*(A,\text{wait}) = Q^*(A,\text{wait}) - V^*(A)$: the new $\pi(\text{move}\mid A)$ and its value.
3. **Interpret.** A paper fine-tunes the second operator's BC policy with RL on a reward that pays $b = 1$ per wait step, and reports the written return rising from $19.02$ to $20.0$. Compute the task value of both policies, say what the table has actually shown, and list what you would ask the authors for (§2's reading cue and §5's table).

> [!note]- How to draw it · 그리는 법
> - Two circles, $A$ (empty) and $B$ (full), and three arrows: move $A \to B$, wait $A \to A$, stay $B \to B$. Write each reward on its arrow — $r = 0$, $r = 0$ (+ $b$), $r = +1$ — and $\gamma = 0.95$ once, in the panel title.
> - Draw the wait loop dashed: it is the action the optimum skips, and the one a bad reward can make it take.
> - Beside the circles the optimal values, and on each arrow out of $A$ its action value. Then the record as a tally at $A$ (moves | waits), the BC probability as their ratio, and $V^{\text{BC}}(A)$ next to $V^*(A)$ — two numbers, never one.
> - In panel 2 the horizontal axis is the idle bonus $b$ and the vertical axis the value in $A$. Draw moving now as a flat line at $V^*(A)$, waiting forever as the line $b/(1-\gamma)$ through the origin, and mark where they cross; then draw the task value of the written optimum as a heavy line that drops to $0$ there.
> - Label every number with the reward it is measured on, written or task: the whole hacking argument is the gap between the two.

> [!tip]- Solutions
> 1. As the picture, with $\gamma = 0.95$: $V^*(B) = 20$, $V^*(A) = 19$ and $Q^*(A,\text{wait}) = 18.05$ on the MDP; the record $4 \mid 2$, $\pi_{\text{BC}}(\text{move}\mid A) = 2/3$ and $V^{\text{BC}}(A) = 18.54$ beside $V^*(A) = 19$. In panel 2, moving now is flat at $19$, waiting forever is $20b$, they cross at $b = 0.95$, and the task value of the written optimum steps from $19$ to $0$ there.
> 2. (a) $V^*(B) = 1/(1 - 0.95) = 20$, $V^*(A) = 0.95 \times 20 = 19$, $Q^*(A,\text{wait}) = 0.95 \times 19 = 18.05$. (b) $\pi_{\text{BC}}(\text{move}\mid A) = 4/6 = 2/3$, and $V^{\text{BC}}(A) = \tfrac23(0.95 \times 20) + \tfrac13(0.95\,V^{\text{BC}}(A))$ gives $V^{\text{BC}}(A) = 12.67/0.6833 = 18.54$, a gap of $0.46$. Both records keep the same $40/41 = 97.6\%$ of the optimum: this operator hesitates on a third of the visits instead of a fifth, but each hesitation now costs a factor $0.95$ instead of $0.9$. (c) Moving now is worth $0.95 \times 20 = 19$ on the written reward and waiting forever $b/(1 - 0.95) = 20b$, so they cross at $b = 19/20 = 0.95 = \gamma$. In general moving is worth $\gamma/(1-\gamma)$ and waiting forever $b/(1-\gamma)$, so the flip is at $b = \gamma$; the record never enters, because RL optimizes the reward, not the record. (d) A wait pays $\gamma\Phi(A) - \Phi(A) = -0.05\,\Phi(A) = 1$, so $\Phi(A) = -20$; the move then earns $F = 0 - (-20) = 20$ and a step in $B$ earns $0$. With $V'(B) = 20$, $Q'(A,\text{move}) = 20 + 0.95 \times 20 = 39$ and $Q'(A,\text{wait}) = 1 + 0.95 \times 39 = 38.05$ — the unshaped $19$ and $18.05$ plus $20$, so moving still wins by $0.95$. The move is paid the whole bank of bonuses, $1/(1 - 0.95) = 20$, that waiting forever would have collected. (e) $A^*(A,\text{wait}) = 18.05 - 19 = -0.95$. The tilt weights the reference by $e^{A/\beta}$: $\tfrac23 e^{0}$ against $\tfrac13 e^{-1.9} = \tfrac13 \times 0.1496$, so $\pi(\text{move}\mid A) = 0.6667/(0.6667 + 0.0499) = 0.930$, worth $V(A) = 0.930 \times 19/(1 - 0.95 \times 0.070) = 18.93$. That lies between BC's $18.54$ and the optimum's $19$: the KL term keeps part of the operator's hesitation, and $\beta \to 0$ removes it.
> 3. On the written reward the fine-tuned policy has learned to wait forever, $1/(1 - 0.95) = 20$, while BC collects the bonus only on its one-in-three waits, $V = [\tfrac23(19) + \tfrac13(1)]/(1 - 0.95/3) = 19.02$. Even the honest optimum, which moves at once, scores only $19$ on this reward. On the task — filling the bucket — the fine-tuned policy scores $0$ and BC $18.54$. The table has shown that the optimizer found the loop in the reward, not that the robot works better. Ask for the reward table with every weight (a term that pays for not moving is the first suspect), the task metric reported separately from the return, whether the fine-tune was KL-anchored to the BC policy and with what $\beta$, and whether the baseline was trained on the same reward, observations and curriculum.

### Sources

- R. S. Sutton and A. G. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018 (free at the link above) — §17.4 on designing reward signals is the book's closest approach to §2.
- §1: S. Ross, G. J. Gordon and J. A. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning," AISTATS 2011 — DAgger and the $O(\epsilon T^2)$ against $O(\epsilon T)$ bounds. The 2024–2026 results: HIL-SERL (*Science Robotics*, 2025; see the [[01-canonical-papers/notes/7-robotics/hil-serl|HIL-SERL note]]); ConRFT, [arXiv:2502.05450](https://arxiv.org/abs/2502.05450); RECAP, [arXiv:2511.14759](https://arxiv.org/abs/2511.14759); "Data Scaling Laws in Imitation Learning for Robotic Manipulation," [arXiv:2410.18647](https://arxiv.org/abs/2410.18647) (ICLR 2025).
- §2: A. Y. Ng, D. Harada and S. Russell, "Policy invariance under reward transformations: Theory and application to reward shaping," ICML 1999 — the potential-based shaping theorem.
- §3: T. P. Lillicrap et al., "Continuous control with deep reinforcement learning," ICLR 2016 — DDPG and its Ornstein–Uhlenbeck noise with $\theta_{\text{OU}} = 0.15$. T. Haarnoja et al., "Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor," ICML 2018 — the maximum-entropy objective ([[01-canonical-papers/notes/1-foundations/sac|SAC note]]).
- §6: Ratliff, Bagnell & Zinkevich, "Maximum Margin Planning" (ICML 2006); Ziebart, Maas, Bagnell & Dey, "Maximum Entropy Inverse Reinforcement Learning" (AAAI 2008); Ho & Ermon, "Generative Adversarial Imitation Learning" (NeurIPS 2016); Bradley & Terry, "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons" (*Biometrika*, 1952); Basu, Yang, Hungerman, Singhal & Dragan, "Do You Want Your Autonomous Car To Drive Like You?" (HRI 2017); Christiano et al., "Deep Reinforcement Learning from Human Preferences" (NeurIPS 2017); Sadigh et al., "Active Preference-Based Learning of Reward Functions" (RSS 2017); Ouyang et al., "Training language models to follow instructions with human feedback" (NeurIPS 2022; the [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT note]]); Rafailov et al., "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (NeurIPS 2023).
- The numeric examples on this page, the bucket's included, were computed here from the stated numbers, not quoted from a source; recompute them rather than trusting them.
- Shao, Z. et al. "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." arXiv:2402.03300, 2024 — GRPO, §4.1.
- DeepSeek-AI. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." *Nature* 645:633–638, 2025.
- Muennighoff, N. et al. "s1: Simple test-time scaling." arXiv:2501.19393, 2025.
- Tan, S. et al. "Interactive Post-Training for Vision-Language-Action Models" (RIPT-VLA). arXiv:2505.17016, 2025; Lu, G. et al. "VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning." arXiv:2505.18719, 2025.

## 한국어

*[[02-foundations/rl-basics|7. RL 기초]] 위에 서고, 그 바로 다음에 읽을 때 가장 잘 읽힌다. 그 페이지가 기계장치를 세웠다면, 이 페이지는 로봇 학습 논문이 실제로 지면을 쓰는 층이다.*

7. RL 기초는 MDP, 벨만 방정식, TD 학습, deadly triad, 정책 그래디언트와 PPO를 주었다. 로봇 학습 논문은 지면을 다른 데 쓴다. 정책이 시연에서 배우는가 보상에서 배우는가, 그 보상이 무엇을 말하는가, 정책이 배울 거리를 어떻게 찾아내는가, 부서질 수 있는 기계 위에서 RL을 어떻게 돌리는가, 실험을 어떻게 짰는가, 그리고 아무도 보상을 적어 내지 못할 때 사람에게서 보상을 어떻게 배우는가. 이 페이지가 그 층이다.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상, 그림, 대상으로 한 번 끝까지를 먼저 읽는다. 셋은 두 상태 MDP 하나 위에서 본 §1과 §2다. 이어서 §1(당신의 논문이 이 분야의 어느 절반에 사는가)과 §2(보상)를, 그다음 로봇 논문의 방법 절과 실험 절을 이루는 §4와 §5를 읽는다. §3 탐색은 짧으니 논문의 탐색 방식이 궁금해질 때 읽으면 된다. §6 보상 학습은 RLHF·DPO·역강화학습 논문을 읽는 것이 아니라면 2차 통과로 미룬다. §2를 전제하고, 네 소절은 하나씩 따로 읽을 수 있다. 논문이 성공 여부만으로 정책을 사후학습하거나 GRPO를 말하면 §8을 읽는다.

### 이 페이지의 대상 · Running object

[[02-foundations/rl-basics|7. RL 기초 §2]]의 **버킷 MDP**, 곧 "대기" 행동을 더한 그 MDP와, 한 조작자가 그것을 몬 기록 하나다. [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 가운데 맞는 것이 없다. 여기서 다루는 것은 정책의 데이터와 보상이 어디서 오는가이고, 대상은 정책 하나의 가치 전체를 손으로 적을 수 있을 만큼 작아야 한다. 가장 가까운 후보인, 7. RL 기초가 MDP로 읽은 장치 P4에는 미룰 과제가 없다. 그 MDP의 최선의 수는 아무것도 하지 않는 것이라서, 아무것도 하지 않는 데 값을 쳐 주는 보상이 무슨 일을 하는지 보여 줄 수 없다. 버킷은 보여 줄 수 있다.

- **상태** $A$(빈 버킷)와 $B$(가득 찬 버킷), 할인율 $\gamma = 0.9$, 모든 전이는 결정론적이다.
- **행동.** $A$에서는 보상 $0$으로 $B$로 가는 *이동*, 또는 보상 $0$으로 $A$에 머무는 *대기*. $B$에서는 행동이 *머묾* 하나이고 스텝마다 보상 $1$을 받는다.
- **가치**(7. RL 기초 §2에서 유도): $V^*(B) = 10$, $V^*(A) = 9$, $Q^*(A,\text{이동}) = 9$, $Q^*(A,\text{대기}) = 8.1$이므로 대기의 어드밴티지는 $-0.9$다.
- **조작자의 기록.** $A$에서 시작한 시연 네 번. 세 번은 곧바로 이동했고, 한 번은 한 스텝 대기한 뒤 이동했다. $A$에서의 상태–행동 쌍으로는 다섯 개, 이동 넷과 대기 하나다.

이 숫자들은 여기서 고정하고 이 페이지에서 다시는 바꾸지 않는다. 과제는 $\gamma$와 기록을 바꿀 뿐 정의는 바꾸지 않는다.

*범위: 이 페이지는 MDP 위에 얹히는 로봇 학습의 층 — 모방 대 RL, 보상 설계, 탐색, 물리 기계 위의 RL, RL 실험 절 읽기, 시연이나 선호에서 보상 배우기 — 를 가르친다. MDP, 가치 함수, TD 학습, deadly triad, 정책 그래디언트는 가르치지 않으며 그것은 [[02-foundations/rl-basics|7. RL 기초]]에 있다. 시뮬레이션에서 기계로 옮기는 전이 — reality gap, 랜덤화, 배치 사다리 — 도 가르치지 않으며 그것은 [[05-construction-robotics/sim-to-real|Sim-to-Real 가이드]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 520" style="max-width:100%;height:auto" role="img" aria-label="γ 0.9의 버킷 MDP: 이동 넷과 대기 하나인 기록을 행동 복제하면 최적값 9에 못 미치는 8.78이고, 대기마다 주는 유휴 보너스 b가 0.9를 넘으면 영원히 대기가 써 놓은 보상의 최적해가 되어 b = 1에서 써 놓은 보상으로는 10, 과제로는 0이다">
  <defs><marker id="arRrk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker></defs>
  <text x="12.0" y="22.0" fill="currentColor" font-size="12">1 · 버킷 MDP(γ = 0.9)와 조작자의 기록</text>
  <circle cx="190" cy="118" r="38" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="190.0" y="115.0" fill="currentColor" font-size="12" text-anchor="middle">A · 빈 버킷</text>
  <text x="190.0" y="132.0" fill="currentColor" text-anchor="middle" opacity="0.9">V*(A) = 9</text>
  <circle cx="400" cy="118" r="38" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <text x="400.0" y="115.0" fill="currentColor" font-size="12" text-anchor="middle">B · 가득</text>
  <text x="400.0" y="132.0" fill="currentColor" text-anchor="middle" opacity="0.9">V*(B) = 10</text>
  <line x1="230" y1="118" x2="359" y2="118" stroke="currentColor" stroke-width="2.2" marker-end="url(#arRrk)"/>
  <text x="294.5" y="110.0" fill="currentColor" font-size="12" text-anchor="middle">이동, r = 0</text>
  <text x="294.5" y="136.0" fill="currentColor" text-anchor="middle" opacity="0.9">Q*(A, 이동) = 9</text>
  <path d="M171.0 85.1 C144 22 236 22 209.5 84.2" stroke="currentColor" stroke-width="1.6" fill="none" stroke-opacity="0.8" stroke-dasharray="5 3" marker-end="url(#arRrk)"/>
  <text x="146.0" y="52.0" fill="currentColor" font-size="12" text-anchor="end">대기, r = 0 (+ b)</text>
  <text x="146.0" y="67.0" fill="currentColor" text-anchor="end" opacity="0.9">Q*(A, 대기) = 8.1</text>
  <path d="M381.0 85.1 C354 22 446 22 419.5 84.2" stroke="currentColor" stroke-width="2.2" fill="none" marker-end="url(#arRrk)"/>
  <text x="444.0" y="60.0" fill="currentColor" font-size="12">머묾, r = +1</text>
  <rect x="20" y="178" width="520" height="46" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="32.0" y="196.0" fill="currentColor" font-size="12">A에서의 기록: 이동 4번, 대기 1번   →   BC: π(이동 | A) = 0.8</text>
  <text x="32.0" y="214.0" fill="currentColor" font-size="12">V<tspan dy="-4" font-size="11">BC</tspan><tspan dy="4">(A) = 8.78  &lt;  V*(A) = 9: 보상을 받은 RL이 0.22를 되찾는다</tspan></text>
  <text x="12.0" y="262.0" fill="currentColor" font-size="12">2 · 대기 스텝마다 주는 유휴 보너스 b에 대한 A의 가치</text>
  <line x1="70" y1="470" x2="528" y2="470" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6"/>
  <line x1="70" y1="470" x2="70" y2="282" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.6"/>
  <line x1="66" y1="470.0" x2="70" y2="470.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="474.0" fill="currentColor" text-anchor="end" opacity="0.85">0</text>
  <line x1="66" y1="395.0" x2="70" y2="395.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="399.0" fill="currentColor" text-anchor="end" opacity="0.85">5</text>
  <line x1="66" y1="335.0" x2="70" y2="335.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="339.0" fill="currentColor" text-anchor="end" opacity="0.85">9</text>
  <line x1="66" y1="320.0" x2="70" y2="320.0" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="63.0" y="324.0" fill="currentColor" text-anchor="end" opacity="0.85">10</text>
  <line x1="70.0" y1="470" x2="70.0" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="257.5" y1="470" x2="257.5" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="407.5" y1="470" x2="407.5" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <line x1="445.0" y1="470" x2="445.0" y2="474" stroke="currentColor" stroke-opacity="0.6"/>
  <text x="70.0" y="487.0" fill="currentColor" text-anchor="middle" opacity="0.85">0</text>
  <text x="257.5" y="487.0" fill="currentColor" text-anchor="middle" opacity="0.85">0.5</text>
  <text x="405.5" y="487.0" fill="currentColor" text-anchor="end" opacity="0.85">0.9 = γ</text>
  <text x="447.0" y="487.0" fill="currentColor" opacity="0.85">1</text>
  <text x="528.0" y="506.0" fill="currentColor" text-anchor="end" opacity="0.85">유휴 보너스 b</text>
  <text x="76.0" y="286.0" fill="currentColor" opacity="0.85">A의 가치</text>
  <line x1="70" y1="335.0" x2="520" y2="335.0" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.75"/>
  <line x1="70" y1="470.0" x2="520.0" y2="290.0" stroke="currentColor" stroke-width="1.4" stroke-dasharray="6 4" stroke-opacity="0.85"/>
  <path d="M70 335.0 L407.5 335.0 L407.5 470.0 L520 470.0" fill="none" stroke="currentColor" stroke-width="3"/>
  <circle cx="407.5" cy="335.0" r="3.5" fill="currentColor"/>
  <circle cx="445.0" cy="320.0" r="3.2" fill="currentColor"/>
  <circle cx="445.0" cy="470.0" r="3.2" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="437.0" y="312.0" fill="currentColor" text-anchor="end">써 놓은 값 10</text>
  <text x="453.0" y="463.0" fill="currentColor">과제 0</text>
  <text x="78.0" y="328.0" fill="currentColor">써 놓은 보상: 지금 이동 = 9</text>
  <text x="78.0" y="352.0" fill="currentColor" font-weight="bold">써 놓은 보상의 최적해가 내는 과제 가치</text>
  <text x="302.5" y="367.0" fill="currentColor" text-anchor="end">써 놓은 보상: 영원히 대기 = 10b</text>
  <text x="417.5" y="396.5" fill="currentColor">b &gt; γ이면</text>
  <text x="417.5" y="410.5" fill="currentColor">써 놓은 보상의</text>
  <text x="417.5" y="424.5" fill="currentColor">최적해가 영원히</text>
  <text x="417.5" y="438.5" fill="currentColor">대기한다</text>
</svg>

조작자의 기록과 함께 본 버킷 MDP에서, $A$의 이동 넷과 대기 하나를 행동 복제하면 $\pi(\text{이동}\mid A) = 0.8$, $V^{\text{BC}}(A) = 8.78$이 되어 RL이 보상으로부터 닿는 최적값 $V^*(A) = 9$에 못 미친다. 아래처럼 대기마다 유휴 보너스 $b$를 주면 써 놓은 보상으로 지금 이동은 $9$, 영원히 대기는 $10b$이므로 $b = \gamma = 0.9$를 넘으면 써 놓은 보상의 최적해는 영원히 대기하고, $b = 1$에서 그 값은 써 놓은 보상으로 $10$, 과제로 $0$이다.

### 대상으로 한 번 끝까지 · Worked case

아래는 모두 이 페이지의 대상 위에서 돈다. 모든 가치는 [[02-foundations/rl-basics|7. RL 기초 §2]]의 벨만 기대 방정식에서 나온다. 한 상태의 가치는 이번 스텝의 보상에, 도착한 곳의 가치를 $\gamma$배 해 더한 것이다.

**1. 모방이 얻는 것.** *행동 복제*(BC)는 기록된 상태–행동 쌍에 최대우도로 정책을 맞춘다(§1). 개수의 표라면 최대화하는 값은 경험적 빈도이므로, $A$의 다섯 쌍은 $\pi_{\text{BC}}(\text{이동}\mid A) = 4/5 = 0.8$을 준다. 이동은 가치 $10$인 $B$에 닿고 대기는 다시 $A$로 돌아오므로, BC의 가치는 자기 방정식의 양변에 나타난다.

$$V^{\text{BC}}(A) = 0.8\,(0 + 0.9 \times 10) + 0.2\,\big(0 + 0.9\,V^{\text{BC}}(A)\big) \;\Rightarrow\; V^{\text{BC}}(A) = \frac{7.2}{1 - 0.18} = 8.78$$

$Q^*$에 대한 탐욕 정책은 매번 이동해 $V^*(A) = 9$를 번다. $0.22$의 차이가 조작자의 망설임 한 번을 베낀 값이고, "RL은 시연자를 넘어설 수 있다"는 말의 내용 전부가 이것이다. 보상은 대기가 $8.1$, 이동이 $9$의 가치라고 말해 주는데 BC는 보상을 읽지 않는다.

**2. 보상이 정하는 것.** 이제 보상을 쓰는 사람이 대기 스텝마다 *유휴 보너스* $b$를 더한다고 하자. 액추에이터를 가만히 두는 정책에 값을 쳐 주는 §2의 "매끄러움" 항이다. 보너스는 $A$에서만 주어지므로 지금 이동은 써 놓은 보상으로 여전히 $9$를 벌고, 영원히 대기하면 다음을 번다.

$$b + 0.9\,b + 0.9^2\,b + \cdots = \frac{b}{1 - 0.9} = 10\,b$$

그래서 $10b > 9$, 곧 $b = 0.9$를 넘으면 써 놓은 보상의 최적해가 영원히 대기로 뒤집힌다. 일반적으로는 이동이 $\gamma/(1-\gamma)$, 영원히 대기가 $b/(1-\gamma)$의 가치이므로 문턱은 $b = \gamma$다. $b = 1$에서 RL 정책은 써 놓은 보상으로 $10$, 과제로 $0$을 번다. 버킷이 영영 차지 않기 때문이다. 이것이 *reward hacking*(§2)이다. 정책은 의도한 것이 아니라 써 놓은 것을 최대화했다. 보상을 읽은 적 없는 BC는 여전히 $8.78$을 번다.

**3. 같은 보너스를 안전하게 주기.** *포텐셜 기반* shaping 항(§2)은 상태만의 함수 $\Phi$에 대해 $F = \gamma\Phi(s') - \Phi(s)$를 주고, 어느 행동이 최선인지를 바꾸지 못한다. 그래도 대기마다 정확히 $b = 1$을 줄 수 있다. $\gamma\Phi(A) - \Phi(A) = -0.1\,\Phi(A) = 1$이 $\Phi(A) = -10$을 정하고, $\Phi(B) = 0$이면 이동은 $F = 0 - (-10) = 10$을, $B$에서의 한 스텝은 $0$을 받는다. shaped 보상에서도 $B$의 한 스텝은 $1 + 0 = 1$을 주므로 $V'(B) = 10$이고, 다음이 성립한다.

$$Q'(A,\text{이동}) = 10 + 0.9 \times 10 = 19, \qquad Q'(A,\text{대기}) = 1 + 0.9 \times 19 = 18.1$$

대기 뒤에는 가치 $19$인 $A$에서의 최선의 수가 이어지고, 영원히 대기하면 $1/(1 - 0.9) = 10$밖에 벌지 못한다. 두 값은 shaping 전의 $9$와 $8.1$에 $10$을 더한 것이라서 이동이 여전히 $0.9$ 차이로 이긴다. 2번의 유휴 보너스와 이 항은 대기마다 똑같이 $+1$을 준다. 차이는 이동에 붙은 $10$ 하나뿐인데, 그것이 영원히 대기했다면 모았을 보너스 전부를 한꺼번에 갚아 준다.

**읽는 법.** 세 숫자가 이 페이지를 떠받친다. $8.78$(모방은 망설임까지 포함해 데이터를 베낀다), $9$(맞는 보상을 받은 RL은 망설임을 없앤다), $0$(루프가 숨은 보상을 받은 RL은 과제를 없앤다). §1은 앞의 둘을, §2는 셋째를 다룬다. §4는 파인튜닝한 정책이 둘째를 좇는 동안 첫째 근처에 머물게 하는 법이고, §5는 실험 절에서 논문이 셋 중 무엇을 보고하는지 가려내는 법이며, §6은 루프 없는 보상을 아무도 적어 내지 못할 때 사람에게서 보상을 얻는 법이다.

### 1. 로봇 학습에서 RL vs 모방 (지도)

- **모방** ([[01-canonical-papers/notes/4-vla/rt-1|RT-1]],
  [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]]): 시연에 대한 지도학습 —
  안정적이고 보상 설계가 없지만, 순수 오프라인 BC는 데이터 커버리지가 상한이고 *시연
  분포 밖의* 회복 동작은 학습할 수 없다(데이터의 **support(지지집합)** = 그 데이터가 실제로
  덮고 있는 상태·행동의 영역. 그 바깥에서 모델은 본 것이 하나도 없다)(회복이 담긴 시연이나 DAgger식 데이터 수집은
  이를 바꾼다).
- **RL**은 유익한 보상과 충분한 탐색이 있으면 시연자를 넘어설 *수 있다* — 주로
  시뮬레이션(sim-to-real)
  에서, 또는 모방으로 사전학습된 VLA 위의 *파인튜닝*으로 —
  [[01-canonical-papers/notes/1-foundations/instructgpt|사전학습 → RLHF]] 레시피의 미러링이다.

**모방 학습 도구 상자** (모든 VLA 논문의 어휘). 여섯 개의 사실이 아니라 *세 묶음*으로
읽어라 — *핵심 목적함수와 그 하나의 약점*, *데이터의 모습*, *정책을 표현력 있게 만드는 것*.

*묶음 1 — 목적함수와 아킬레스건.* **BC**는 시연 쌍에 대해 $\log \pi_\theta(a|o)$를 최대화할
뿐 — 정책의 옷을 입은 지도학습이다([[01-canonical-papers/how-to-read|how-to-read §3]]이 이
식을 해부한다). 유일한 구조적 약점은 **covariate shift**다: 정책은 *전문가의* 상태에서
학습되지만 *자신의* 상태에서 실행되므로, 작은 오차가 상태를 분포 밖으로 밀고 거기서 오차가
누적된다. 이 하나의 실패 모드가 **DAgger**가 존재하는 이유다 — 학습자를 실행시키고, 실제로
방문한 상태를 전문가가 라벨하고, 재학습.

- **행동 복제를 풀어 쓰면.** 전문가 관측과 행동의 데이터셋 $\mathcal{D} = \{(o_i, a_i)\}_{i=1}^{N}$에 대해
  $$\theta^\star = \arg\max_\theta \sum_{i=1}^{N} \log \pi_\theta\big(a_i \mid o_i\big)$$
  이고, 이는 최대우도 지도학습이므로 보상도 환경 상호작용도 어디에도 나오지 않는다. 표준편차를 고정한 가우시안 정책이면 $-\log \pi_\theta(a \mid o) = \frac{1}{2\sigma^2}\lVert a - \mu_\theta(o)\rVert^2 + \text{const}$이므로 BC는 시연 행동에 대한 평균제곱오차 회귀로 줄어든다.
- **공변량 이동, 두 분포로.** 정책 $\pi$가 실행될 때 방문하는 상태의 분포를 $d_\pi(s)$로 쓰자. BC는 전문가의 방문 분포 $d_{\pi_E}$ 아래에서 손실을 줄이지만, 배포된 정책은 자기 분포 아래에서 채점된다.
  $$\text{trained on } E_{s \sim d_{\pi_E}}\big[\ell(\pi_\theta, s)\big], \qquad \text{evaluated on } E_{s \sim d_{\pi_\theta}}\big[\ell(\pi_\theta, s)\big], \qquad d_{\pi_\theta} \ne d_{\pi_E}$$
  $\ell$은 상태별 모방 손실이다. 입력의 분포는 움직이는데 각 상태의 올바른 행동은 그대로이므로, [[02-foundations/ml-practice|9. ML 실무 §1]]의 뜻 그대로 공변량 이동이다.
- **DAgger, 알고리즘으로**(Ross, Gordon & Bagnell, 2011). 시연을 $\mathcal{D}$로 두고 $\pi_1$을 학습한다. $i$번째 반복에서: 확률 $\beta_i$로 전문가를, 그 외에는 현재 학습자를 따르는 혼합 정책을 실행하고, 방문한 상태를 기록하고, 각 상태에서 전문가라면 *무엇을 했을지* 묻고, 모아서 재학습한다.
  $$\mathcal{D} \leftarrow \mathcal{D} \cup \big\{(s, \pi_E(s)) : s \sim d_{\pi_i}\big\}, \qquad \pi_{i+1} = \text{BC on } \mathcal{D}$$
  그래서 학습 분포가 학습자 자신의 상태 분포 쪽으로 끌려간다. 흔한 일정은 $\beta_i = 0.5^{\,i-1}$, 곧 $1, 0.5, 0.25, 0.125$로 제어를 기하급수적으로 학습자에게 넘긴다. **반례:** 전문가 시연을 더 모아 재학습하는 것은 DAgger가 아니다. 그 상태들은 여전히 $d_{\pi_E}$에서 오기 때문이다.
- **지지집합(support).** 분포의 지지집합은 확률이 0이 아닌 집합, $\operatorname{supp}(d) = \{s : d(s) > 0\}$다. "시연의 지지집합 밖"은 $d_{\pi_E}(s) = 0$인 상태, 곧 BC의 손실이 한 번도 계산되지 않았고 출력이 순수한 외삽인 곳이다.

*얼마나 나쁜가?* 각 스텝이 독립적으로 확률 $\epsilon$만큼, 시연이 가 본 적 없는 곳으로
정책을 밀어내는 오차를 낸다고 하자. 그러면 $T$스텝 과제가 살아남을 확률은 $(1-\epsilon)^T$이고,
피해를 입히는 것은 지평이다:

<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="한 번도 틀리지 않고 과제를 끝낼 확률이 스텝당 오류율 세 가지에 대해 지평에 따라 떨어진다">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="60" y1="170" x2="524" y2="170"/><line x1="60" y1="170" x2="60" y2="36"/>
  </g>
  <g stroke="currentColor" stroke-width="0.8" fill="none" opacity="0.25" stroke-dasharray="3 3">
    <line x1="60" y1="105" x2="524" y2="105"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="152" y1="170" x2="152" y2="175"/><line x1="244" y1="170" x2="244" y2="175"/><line x1="336" y1="170" x2="336" y2="175"/><line x1="428" y1="170" x2="428" y2="175"/><line x1="520" y1="170" x2="520" y2="175"/>
  </g>
  <path d="M 60.0 40.0 L 69.2 92.2 L 78.4 123.4 L 87.6 142.1 L 96.8 153.3 L 106.0 160.0 L 115.2 164.0 L 124.4 166.4 L 133.6 167.9 L 142.8 168.7 L 152.0 169.2 L 161.2 169.5 L 170.4 169.7 L 179.6 169.8 L 188.8 169.9 L 198.0 169.9 L 207.2 170.0 L 216.4 170.0 L 225.6 170.0 L 234.8 170.0 L 244.0 170.0 L 253.2 170.0 L 262.4 170.0 L 271.6 170.0 L 280.8 170.0 L 290.0 170.0 L 299.2 170.0 L 308.4 170.0 L 317.6 170.0 L 326.8 170.0 L 336.0 170.0 L 345.2 170.0 L 354.4 170.0 L 363.6 170.0 L 372.8 170.0 L 382.0 170.0 L 391.2 170.0 L 400.4 170.0 L 409.6 170.0 L 418.8 170.0 L 428.0 170.0 L 437.2 170.0 L 446.4 170.0 L 455.6 170.0 L 464.8 170.0 L 474.0 170.0 L 483.2 170.0 L 492.4 170.0 L 501.6 170.0 L 510.8 170.0 L 520.0 170.0" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <path d="M 60.0 40.0 L 69.2 52.4 L 78.4 63.7 L 87.6 73.8 L 96.8 83.0 L 106.0 91.3 L 115.2 98.9 L 124.4 105.7 L 133.6 111.8 L 142.8 117.4 L 152.0 122.4 L 161.2 127.0 L 170.4 131.1 L 179.6 134.8 L 188.8 138.2 L 198.0 141.2 L 207.2 144.0 L 216.4 146.5 L 225.6 148.7 L 234.8 150.7 L 244.0 152.6 L 253.2 154.2 L 262.4 155.8 L 271.6 157.1 L 280.8 158.3 L 290.0 159.5 L 299.2 160.5 L 308.4 161.4 L 317.6 162.2 L 326.8 163.0 L 336.0 163.6 L 345.2 164.2 L 354.4 164.8 L 363.6 165.3 L 372.8 165.7 L 382.0 166.1 L 391.2 166.5 L 400.4 166.8 L 409.6 167.1 L 418.8 167.4 L 428.0 167.7 L 437.2 167.9 L 446.4 168.1 L 455.6 168.3 L 464.8 168.4 L 474.0 168.6 L 483.2 168.7 L 492.4 168.8 L 501.6 169.0 L 510.8 169.1 L 520.0 169.1" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <path d="M 60.0 40.0 L 69.2 41.3 L 78.4 42.6 L 87.6 43.8 L 96.8 45.1 L 106.0 46.3 L 115.2 47.6 L 124.4 48.8 L 133.6 50.0 L 142.8 51.2 L 152.0 52.4 L 161.2 53.5 L 170.4 54.7 L 179.6 55.9 L 188.8 57.0 L 198.0 58.1 L 207.2 59.2 L 216.4 60.3 L 225.6 61.4 L 234.8 62.5 L 244.0 63.6 L 253.2 64.6 L 262.4 65.7 L 271.6 66.7 L 280.8 67.8 L 290.0 68.8 L 299.2 69.8 L 308.4 70.8 L 317.6 71.8 L 326.8 72.7 L 336.0 73.7 L 345.2 74.7 L 354.4 75.6 L 363.6 76.6 L 372.8 77.5 L 382.0 78.4 L 391.2 79.3 L 400.4 80.2 L 409.6 81.1 L 418.8 82.0 L 428.0 82.9 L 437.2 83.7 L 446.4 84.6 L 455.6 85.5 L 464.8 86.3 L 474.0 87.1 L 483.2 88.0 L 492.4 88.8 L 501.6 89.6 L 510.8 90.4 L 520.0 91.2" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.9"/>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="110" y="148">20스텝에 1번 틀림</text>
    <text x="170" y="124">100에 1번</text>
    <text x="300" y="64">1000에 1번</text>
    <text x="54" y="44" text-anchor="end">1.0</text><text x="54" y="109" text-anchor="end">0.5</text><text x="54" y="174" text-anchor="end">0</text>
    <text x="152" y="188" text-anchor="middle">100</text><text x="244" y="188" text-anchor="middle">200</text><text x="336" y="188" text-anchor="middle">300</text><text x="428" y="188" text-anchor="middle">400</text><text x="520" y="188" text-anchor="middle">500</text>
    <text x="292" y="204" text-anchor="middle">과제 길이 (스텝)</text>
    <text x="20" y="30">무결 수행 확률</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="226">무시해도 될 것 같은 스텝당 오류율이 과제 실패율이 된다.</text>
    <text x="20" y="242">100스텝에 1번 틀리면 50스텝 과제는 약 60% 확률로 깨끗하게 끝나고,</text>
    <text x="20" y="258">500스텝 과제는 약 0.7%다.</text>
  </g>
</svg>

실제 오차는 독립도 아니고 하나하나가 치명적이지도 않으므로, 저 곡선은 정리가 아니라 예시로
읽어라. 정리도 같은 모양이다: Ross, Gordon, Bagnell의 2011년 환원은 순수 행동 복제가
$O(\epsilon T^2)$로 비용을 누적하는 반면 DAgger 같은 no-regret 방법은 $O(\epsilon T)$에
도달함을 보인다 — 늘릴 수 있는 지평과 늘릴 수 없는 지평의 차이다. 아래 묶음 3의 **행동 청킹**은
같은 수를 싸게 두는 것이다: $k$스텝을 한 번에 예측하면 $T$스텝 과제가 $T/k$번의 결정 과제가
되어, 이 곡선의 지평 축을 왼쪽으로 되돌린다. [[05-construction-robotics/imitating-contact|10. 접촉 모방 §3]]은 두 상한에 건설 작업,
S1의 마지막 40 mm에서 값을 매긴다. $\epsilon=0.02$에서 앞의 것은 리드인이 흡수하는 $15$스텝에 대해
표류 $T^2\epsilon=32$스텝을 허락하므로 $27$스텝짜리 단계까지만 덮고, 뒤의 것은 $750$스텝을 덮는다.

*묶음 2 — 데이터셋 절 읽기.* 시연은 원격조작([[01-canonical-papers/notes/4-vla/act|ALOHA]]식
장비, VR, 직접 교시), 스크립트 정책, 교차-embodiment 풀링
([[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]])에서 온다. 확인할 것 둘:
**시간 동기화**(100 ms 어긋난 라벨이 모든 관측-행동 쌍을 조용히 오염시킨다)와 **개수보다
큐레이션** — 성공 필터링과 *궤적 다양성*(장면·물체·초기 조건)이 "시연 N천 개"보다 대개 더
중요하며, 그 개수야말로 회의적으로 검사할 대상이다.

*묶음 3 — 화려한 출력 헤드가 존재하는 이유.* 시연은 **다봉**이다: 두 전문가가 장애물을
반대쪽으로 지나가면 평균 회귀 정책은 한가운데로 돌진한다. 만나게 될 처방은 **행동
청킹**(미래 행동 $k$개를 한 번에 예측 — [[01-canonical-papers/notes/4-vla/act|ACT]] — 반응성을
지불해 오차 누적과 싸움)과 여러 모드를 표현할 수 있는 **표현력 있는 헤드**
([[01-canonical-papers/notes/4-vla/diffusion-policy|디퓨전]],
[[01-canonical-papers/notes/4-vla/pi0|flow matching]])다. (행동 *표현*도 갈린다: 절대 vs 델타,
관절 vs 말단 공간.) 곁가지: **오프라인 RL**도 고정 데이터셋에서 배우지만 보상으로 어느 단일
시연자보다 나은 행동을 *꿰맨다* — BC엔 없는 가치 외삽 불안정을 대가로.

- **다봉, 정확히.** 같은 관측에 대해 전문가의 행동 분포 $p(a \mid o)$에 떨어진 봉우리(모드)가 둘 이상 있다는 뜻이다. 평균제곱오차로 학습한 정책은 조건부 *평균* $\mu^\star(o) = E[a \mid o]$를 예측한다. 제곱 오차를 최소화하는 것이 그것이기 때문이다. 두 전문가가 장애물을 $+1$ m와 $-1$ m로 같은 빈도로 비켜 가면 평균은 $(1 + (-1))/2 = 0$ m, 곧 장애물 정면이고 *어느* 전문가도 한 적 없는 행동이다. 평균이 아니라 분포를 표현하는 헤드(혼합 모델, 디퓨전이나 flow 모델, 이산화한 행동 토큰)는 양쪽 모두에 확률을 둘 수 있다.
- **행동 청킹, 정확히.** 정책이 관측 하나에서 다음 $k$개 행동 $\pi_\theta(a_t, a_{t+1}, \dots, a_{t+k-1} \mid o_t)$를 내고, 로봇은 다시 묻기 전에 그중 여러 개를 실행한다. 그러면 $T$스텝 과제에 정책 결정이 약 $T/k$번 필요하다. $500$스텝을 $10$개씩 묶으면 결정 $50$번이고, 결정당 오류율 $1\%$에서 위 그림의 무결 확률이 $0.99^{500} = 0.7\%$에서 $0.99^{50} = 60.5\%$로 옮겨 간다. 같은 식이 대가도 보여 준다. 청크 안에서는 $o_t$ 이후의 관측을 쓰지 않는다.
- **오프라인 RL, 정확히.** 다른 행동 정책이 모은 고정 전이 데이터셋 $\mathcal{D} = \{(s, a, r, s')\}$에서, **추가 상호작용 없이** 기대 리턴 $J(\pi)$를 최대화하는 정책을 배운다. $r$을 쓴다는 점에서 BC와 달라 평범한 궤적의 좋은 부분을 골라 쓸 수 있고, $\operatorname{supp}(\mathcal{D})$ 밖을 시도해 과대추정된 $Q$를 바로잡을 길이 전혀 없다는 점에서 보통의 오프폴리시 RL과 다르다 — [[02-foundations/rl-basics|7. RL 기초 §3.5]]의 비관주의가 그래서 필요하다.

> [!important] 이 절에 대한 2024~26년의 교정
> 위의 프레이밍 — 모방은 안정적이지만 상한이 있고, RL은 시연자를 넘어설 수 있다 — 은 옳고,
> 지난 2년이 그것을 가져갈 만한 방식으로 날카롭게 만들었다. **접촉이 많은 정밀** 과제에서 격차는
> 좁지 않다: **[[01-canonical-papers/notes/7-robotics/hil-serl|HIL-SERL]]**(*Science Robotics*, 2025)이 그런 과제 약 열세 개에서 **실기계 학습
> 1~2.5시간** 후 100% 성공을 보고한다 — 시간은 초록의 것이고, 성공률과 과제
> 수는 본문 수치이며, 그것이 이긴 diffusion policy 베이스라인(RAM 삽입 **27%**, 대시보드 조립
> **18%**)도 마찬가지다. 초록 자신의 표제는 모방과 기존 RL 대비 2배 평균이다. 시연에는 2 mm 어긋났을 때 필요한 교정적 미세 조정이 담겨 있지
> 않고, 사람 시연들에 대해 평균을 내는 것이 반응적 거동을 적극적으로 파괴한다.
>
> 그러나 여기서 다루는 접촉 정밀 사례의 정직한 표제는 "RL이 모방을 이겼다"가 아니다. 이 결과들 — HIL-SERL, ConRFT([arXiv:2502.05450](https://arxiv.org/abs/2502.05450)),
> RECAP([arXiv:2511.14759](https://arxiv.org/abs/2511.14759)) — 하나하나가 **학습 도중 사람이
> 정책을 온-분포로 교정하게** 하고, 그것은 고전 RL보다
> [[01-canonical-papers/notes/4-vla/dagger|DAgger]]의 계보에 가깝다. **상호작용적 학습이 오프라인
> 학습을 이겼고, 보상은 그 루프를 닫는 여러 방법 중 하나다.** 단서 둘: 위의 모든 RL 성공이 손으로
> 만든 이진 보상 분류기를 필요로 했다 — 100% 성공률 표에는 보이지 않는 과제별 비용이다.
> 이 사례들에서 RL은 입증된 범용 학습 패러다임이라기보다 상호작용적 마무리 단계로 읽는 편이 안전하다.
>
> 모방 쪽의 가장 날카로운 최근 결과는 스케일링 법칙이다: 일반화가 **시연의 수가 아니라 환경과
> 물체의 수**에 대한 거듭제곱 법칙을 따른다(Lin 외,
> [arXiv:2410.18647](https://arxiv.org/abs/2410.18647). 초록 자신의 표현은 "대략적인 거듭제곱
> 관계"이고, 시연 4만 개 이상과 실기계 롤아웃 1만 5천 회 이상에서 나온 결과다).
> 임계를 넘으면 환경당 시연을 더 모아도 거의 아무 일도 일어나지 않는다. 그러므로 두 패러다임은
> 같은 자원을 놓고 경쟁하지 않는다 — **RL은 상호작용 시간으로 정밀도를 사고, 모방은 장면
> 다양성으로 일반성을 산다.**

논문으로 들어가는 진입 사슬: 이 절 →
[[01-canonical-papers/notes/4-vla/act|ACT]] →
[[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] →
[[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]] →
[[01-canonical-papers/notes/4-vla/rt-1|RT-1]]/[[01-canonical-papers/notes/4-vla/rt-2|RT-2]] →
[[01-canonical-papers/notes/4-vla/openvla|OpenVLA]]/[[01-canonical-papers/notes/4-vla/pi0|π0]].

- 논문 해독기: "BC baseline" = 행동 복제; "advantage-weighted" = $e^{A/\beta}$로 재가중된
  정책 개선; "KL-regularized policy" = 기준 정책 근처에 머물며 개선하기.
  - 뒤의 둘은 한 식이다. **KL 정규화 목적함수**는 리턴을 기준 정책 $\pi_{\text{ref}}$(사전학습 정책이나 데이터 수집 정책)로부터의 거리와 맞바꾸고, 온도 $\beta > 0$이 교환 비율을 정한다.
  $$\max_\pi\ E_{a \sim \pi}\big[A(s, a)\big] - \beta\, \mathrm{KL}\big(\pi(\cdot \mid s)\ \Vert\ \pi_{\text{ref}}(\cdot \mid s)\big) \quad\Rightarrow\quad \pi^*(a \mid s) = \frac{\pi_{\text{ref}}(a \mid s)\, e^{A(s,a)/\beta}}{Z(s)}$$
  $Z(s)$는 확률의 합을 1로 맞추는 정규화 상수이고, 이 닫힌 형태는 §6의 MaxEnt IRL과 DPO에 쓰이는 것과 같은 라그랑주 승수 결과다. "Advantage-weighted" 방법은 기록된 행동마다 $e^{A/\beta}$로 가중한 BC로 $\pi_\theta$를 이 $\pi^*$에 맞춘다. 계산 예: $\pi_{\text{ref}} = (0.5, 0.5)$인 두 행동, 어드밴티지 $(1, 0)$, $\beta = 0.5$면 가중치가 $e^{2} : e^{0}$이라 $\pi^* = (0.881, 0.119)$이고, $\beta$가 클수록 $\pi^*$는 $(0.5, 0.5)$에 가깝게 남는다.

### 2. 보상 설계 — 결과를 결정하는 선택

지도학습은 타깃을 받아 든다. RL은 *누군가 써 놓은 보상*을 받아 든다. 로봇 RL 논문이 실제로
성공하거나 실패하는 지점이 그 저술 단계이고, 초록이 결코 말하지 않는 부분이다.

- **희소 vs 촘촘.** **희소** 보상(버킷이 차면 +1, 아니면 0)은 정직하다 — 원하는 것만 정확히
  말한다 — 하지만 무작위 초기 정책은 그것을 영영 못 볼 수 있다. **촘촘한**(shaped) 보상은
  매 스텝 신호를 주어 훨씬 빨리 학습하지만, 이제 목표가 아니라 목표의 *대리물*을 최적화하게 된다.
  - *식으로.* 희소 보상은 목표 집합 $\mathcal{G}$의 지시함수 $r(s) = \mathbb{1}[s \in \mathcal{G}]$이고, 상태의 작은 일부에서만 0이 아니다. 촘촘한 보상은 거의 모든 곳에서 정보를 주며, 위치 $x(s)$에 대한 $r(s) = -\lVert x(s) - x_{\text{goal}} \rVert$처럼 음의 거리가 전형적이다. "Shaped"는 참 보상에 촘촘한 항을 더한 $r' = r + F$를 뜻한다.
- **포텐셜 기반 shaping**은 최적 정책을 바꾸지 않음이 증명된 유일한 형태다: 상태의 임의 함수
  $\Phi$에 대해 $F = \gamma\Phi(s') - \Phi(s)$를 더한다. 그 외의 것은 — 그리고 대부분의 논문이
  그 외의 것을 쓴다 — 무엇이 최적인지를 바꿀 수 있다.
  - *바꿀 수 없는 이유*(Ng, Harada & Russell, ICML 1999). 어떤 궤적을 따라서든 shaping 항은 망원경처럼 접힌다.
  $$\sum_{t=0}^{T-1} \gamma^t \big(\gamma\,\Phi(s_{t+1}) - \Phi(s_t)\big) = \gamma^T\, \Phi(s_T) - \Phi(s_0)$$
  각 $\gamma^{t+1}\Phi(s_{t+1})$이 다음 스텝의 $-\gamma^{t+1}\Phi(s_{t+1})$과 상쇄되기 때문이다. 그래서 shaped 리턴은 원래 리턴과 시작 상태 항만큼만 다르고(끝 항은 $\Phi$가 유계이고 $\gamma < 1$이면 $T \to \infty$에서 사라진다), 모든 행동에 대해 $Q'(s, a) = Q(s, a) - \Phi(s)$다. 한 상태의 모든 행동이 같은 양만큼 옮겨지므로 행동의 순위, 곧 최적 정책은 바뀌지 않는다. 조건은 $F$가 상태 포텐셜에만 의존한다는 것이다. 루프를 돌며 다시 챙길 수 있는 보너스에는 이런 상쇄가 없다.
  - *계산 예:* 이 페이지의 대상, 곧 "대기" 행동을 더한 [[02-foundations/rl-basics|7. RL 기초 §2]]의 버킷 MDP에 $\Phi(A) = 0$, $\Phi(B) = 5$, $\gamma = 0.9$를 두자. $A \to B$ 이동은 $F = 0.9(5) - 0 = 4.5$를 벌고, $B$에 머물면 보상 $1$ 위에 $F = 0.9(5) - 5 = -0.5$를 받는다. shaped 가치는 $V'(B) = (1 - 0.5)/(1 - 0.9) = 5 = V(B) - \Phi(B)$이고, $A$에서는 $Q'(A, \text{이동}) = 4.5 + 0.9 \times 5 = 9$ 대 $Q'(A, \text{대기}) = 0 + 0.9 \times 9 = 8.1$이다. $\Phi(A) = 0$이므로 shaping 전과 같은 두 숫자이고, 여전히 이동이 최적이다. 대상으로 한 번 끝까지의 3번은 대기마다 $+1$을 주도록 고른 포텐셜로 같은 확인을 한다.
- **실제 보상은 항들의 가중합이다.** 곧 $r = \sum_{j} w_j\, r_j$이고, 각 $r_j$는 거동의 한 측면을 재며 각 가중치 $w_j$는 부호를 품은 하이퍼파라미터다. 굴착 정책의 보상은 보통 이렇게 생겼고, 이 표가 곧 읽을
  가치가 있는 방법 절이다:

| 항 | 목적 | 부호 |
|---|---|---|
| 과제 진행(옮긴 토량, 목표까지 거리) | 일을 한다 | + |
| 추종·자세 오차 | 정확하게 한다 | − |
| 행동 크기·변화율("매끄러움") | 액추에이터를 떨지 않게 한다 | − |
| 에너지·노력 | 효율, 기계 수명 | − |
| 제약 위반(관절 한계, 전도, 힘 상한) | 안전 | − (큼) |
| 종료·실패 페널티 | 에피소드를 의미 있게 끝낸다 | − (큼) |

- **가중치는 하이퍼파라미터이고, 서로 싸운다.** $r = 2.0\,\Delta d - 0.5\,\lVert a\rVert^2$를
  보자. 단위 노름 행동으로 1 cm 이동($\Delta d = 0.01$)하면
  $2.0(0.01) - 0.5(1) = -0.48$ — **음수**다. 즉 최적 정책은 *아무것도 하지 않는 것*이다.
  "가만히 서서 매끄러움 보너스만 챙긴다"는 퇴화 해가 정확히 이만큼 단순한 산수에서 나온다.

<svg viewBox="0 0 460 152" style="max-width:100%;height:auto" role="img" aria-label="두 보상 항을 실제 비율로 그린 그림: 페널티가 진척 항을 압도한다">
  <g stroke="currentColor" stroke-width="1.2" opacity="0.5"><line x1="150" y1="20" x2="150" y2="118"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="30" y1="118" x2="430" y2="118"/></g>
  <g fill="currentColor" opacity="0.22"><rect x="150" y="34" width="4" height="26"/><rect x="50" y="74" width="100" height="26"/></g>
  <g fill="none" stroke="currentColor" stroke-width="1.2"><rect x="150" y="34" width="4" height="26"/><rect x="50" y="74" width="100" height="26"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="164" y="52">+0.02 &nbsp; 과제 진척 (2.0 &#215; 0.01 m)</text>
    <text x="164" y="92">&#8722;0.50 &nbsp; 행동 페널티 (0.5 &#215; 1)</text>
    <text x="30" y="140">실제 비율: 합이 &#8722;0.48이므로 가만히 있는 쪽이 파는 쪽보다 낫다</text>
    <text x="122" y="20" font-size="10.5" opacity="0.7">0</text>
  </g>
</svg>

- **Reward hacking**이 그 일반형이다: 정책은 당신이 *의도한* 것이 아니라 *써 놓은* 것을
  최대화한다. 속도 보상을 제자리 진동으로 채우고, 목표까지 거리 보상을 문턱 안쪽에서 맴돌며
  채운다. 증상: 보상 곡선은 오르는데 거동이 틀렸다. 진단 질문은 언제나
  *이 보상을 버는 가장 싼 방법이 무엇인가?* 다.
  - *조건으로 쓰면.* 의도한 보상(대개 적을 수 없다)을 $r^\dagger$, 써 놓은 대리 보상을 $\hat r$라 하자. Reward hacking은 대리물을 최적화한 결과가 대리물에서는 성공하고 의도에서는 실패하는 경우다.
  $$\hat\pi = \arg\max_\pi J_{\hat r}(\pi), \qquad J_{\hat r}(\hat\pi) \ \text{high}, \qquad J_{r^\dagger}(\hat\pi) \ \text{low}$$
  그래서 이것은 어느 한쪽이 아니라 (대리물, 최적화기) 쌍의 성질이다. 최적화기가 강할수록 $\hat r$과 $r^\dagger$가 어긋나는 곳을 더 확실히 찾아낸다. 위의 $-0.48$ 예가 가장 단순한 사례다. 대리물은 가만히 서 있기로 최대화되고, 그것은 의도한 굴착 과제에서 0점이다.
- **읽기 단서**: 보상 표를 찾고, 항의 개수를 세고, 가중치를 찾고(대개 부록에만 있다), 논문이
  보고하는 운용점에서 어느 항이 지배적인지 물어라. 보상을 보여주지 않는 논문은 방법을 보여주지
  않은 것이다.

### 3. 탐색 — 그리고 그 발판으로서의 커리큘럼

정책은 자기가 시도한 것에서만 배운다. 희소 보상에 무작위 시작이면 영원히 시도하고도 아무것도
못 볼 수 있다 — 갱신 규칙이 아니라 탐색이 대개 병목인 이유다.

- **이산 행동**: $\epsilon$-greedy — 확률 $1-\epsilon$로 탐욕적으로, 나머지는 균등 무작위로
  행동하고, 학습이 진행되면 $\epsilon$을 줄인다.
  - *이것이 정의하는 정책*은 행동 $|\mathcal{A}|$개와 탐욕 행동 $a^\star = \arg\max_a Q(s, a)$에 대해
  $$\pi(a \mid s) = \begin{cases} 1 - \epsilon + \epsilon/|\mathcal{A}| & a = a^\star \\ \epsilon/|\mathcal{A}| & a \ne a^\star \end{cases}$$
  이다. 무작위 가지도 $a^\star$를 고를 수 있기 때문이다. $\epsilon = 0.1$, 행동 4개면 탐욕 행동의 확률은 $0.925$, 나머지 각 행동은 $0.025$이므로 모든 행동이 계속 시도된다.
- **연속 행동**(로보틱스의 경우): 행동에 노이즈를 더하거나(가우시안, 또는 기계가 떨지 않도록
  시간 상관이 있는 Ornstein–Uhlenbeck 노이즈 — 매 스텝 새로 뽑지 않고 직전 값에서 조금씩
  흘러가는 노이즈), 정책을 **확률적**으로 두고 표준편차 자체를
  학습시킨다 — PPO가 하는 방식.
  - *두 노이즈를 식으로.* 가우시안 탐색은 매 스텝 새로 뽑은 $\varepsilon_t \sim \mathcal{N}(0, I)$로 $a_t = \mu_\theta(s_t) + \sigma \varepsilon_t$를 실행한다. 시간 간격 $\Delta t$로 이산화한 Ornstein–Uhlenbeck 노이즈는 비율 $\theta_{\text{OU}}$로 평균 $\mu$ 쪽으로 당기면서 크기 $\sigma$의 새 무작위성을 더한다.
  $$x_{t+1} = x_t + \theta_{\text{OU}}\,\big(\mu - x_t\big)\,\Delta t + \sigma\sqrt{\Delta t}\;\varepsilon_t$$
  그래서 연속한 값의 상관계수가 $1 - \theta_{\text{OU}}\Delta t$다. DDPG의 $\theta_{\text{OU}} = 0.15$, $\Delta t = 1$이면 $0.85$이고, 가우시안 노이즈는 $0$이다.
- **엔트로피 보너스**: 목적함수에 $+\alpha H(\pi)$를 더해
  ([[02-foundations/information-theory|정보이론]]) 정책이 결정을 유보하는 데 보상을 주고,
  이른 시점에 평범한 결정론적 습관으로 붕괴하지 않게 한다.
  [[01-canonical-papers/notes/1-foundations/sac|SAC]]는 이것을 보너스에서 *목적함수 자체*로
  승격시키고 $\alpha$를 자동 조정한다.
  - *풀어 쓰면.* 한 상태에서 정책의 엔트로피 $H(\pi(\cdot \mid s)) = -\sum_a \pi(a \mid s) \log \pi(a \mid s)$([[02-foundations/information-theory|5. 정보이론 §1]])를 SAC의 최대 엔트로피 목적함수에서는 매 스텝 보상에 더한다.
  $$J(\pi) = E_\pi\Big[\sum_{t} \gamma^t \Big(r(s_t, a_t) + \alpha\, H\big(\pi(\cdot \mid s_t)\big)\Big)\Big]$$
  그래서 $\alpha \ge 0$은 보상과 무작위성 사이의 교환 비율이다. 두 행동이 $(0.5, 0.5)$면 $H = \ln 2 = 0.693$ nat, $(0.9, 0.1)$이면 $H = 0.325$다. $\alpha = 0.1$일 때 첫 정책에서 둘째 정책으로 붕괴할 가치가 있으려면 스텝당 보상을 $0.1 \times (0.693 - 0.325) = 0.037$보다 더 얻어야 한다.
- **커리큘럼 학습**은 알고리즘 대신 *과제*를 바꾼다: 무른 토질에서 얕게 파는 것으로 시작해,
  성공률이 문턱을 넘으면 깊이와 저항을 올린다. 싸고 대개 일의 대부분을 해낸다 — 그래서 비교에
  반드시 들어가야 한다: 제안 방법은 커리큘럼을 쓰고 베이스라인은 안 썼다면, 그 절제 실험은
  방법을 재고 있는 것이 아니다.
  - *구성요소.* 커리큘럼은 목표 과제로 끝나는 과제 변형의 수열 $M_1, M_2, \dots, M_K$와, 언제 넘어갈지 정하는 진급 규칙 — 전형적으로 "최근 $n$ 에피소드의 성공률이 문턱을 넘으면 $M_j$에서 $M_{j+1}$로" — 의 쌍이다. 수열도 규칙도 설계 선택이고, 둘 다 방법 절에 들어가야 한다.
- 전이 쪽 형제인 **도메인 랜덤화**는 탐색이 아니라 강건성의 문제이고
  [[05-construction-robotics/sim-to-real|sim-to-real 가이드]]에 있다.

### 4. 실기계 위의 RL: 파인튜닝, 안전, 그리고 sim-to-real의 자리

- **RL 파인튜닝**(RLFT)이 오늘날 RL이 로봇에 닿는 가장 흔한 경로이고, 이 위키에서 만나게 될
  형태다. 행동 복제(또는 이전 RL 실행)로 이미 사전학습된 정책에서 출발해, 과제 보상으로 RL을
  이어간다. 사전학습이 탐색이 절망적이지 않은 영역에 데려다 놓고, RL이 시연으로 덮지 못한 것을
  고친다. [[01-canonical-papers/notes/1-foundations/instructgpt|사전학습 → RLHF]]와 같은
  모양이며, [[01-canonical-papers/notes/8-construction/ext|ExT]]의 SFT/RLFT 단계가 굴착기에서
  하는 일이 이것이다.
- **기준 근처에 붙들어 둔다.** RLFT는 보통 사전학습 정책으로의 KL 항으로 정규화한다. 너무 멀리
  가면 사전학습이 사 준 것을 잃고, reward hacking이 유력해진다 — 보상은 애초에 거동 전체를
  정의하려고 쓴 것이 아니기 때문이다.
  - *RLFT 목적함수.* 사전학습 파라미터 $\theta_0$에서 출발하고 $\pi_{\text{ref}} = \pi_{\theta_0}$는 얼려 둔다.
  $$\max_\theta\ E_{\pi_\theta}\Big[\sum_t \gamma^t\, r(s_t, a_t)\Big] - \beta\, E_{s \sim d_{\pi_\theta}}\Big[\mathrm{KL}\big(\pi_\theta(\cdot \mid s)\ \Vert\ \pi_{\text{ref}}(\cdot \mid s)\big)\Big]$$
  그래서 $\beta$는 이탈 한 단위가 사야 할 과제 보상의 양을 정한다. $\beta \to \infty$면 사전학습 정책이 그대로 돌아오고, $\beta = 0$이면 초기화만 잘한 평범한 RL이다. 최적해는 §1 논문 해독기의 지수 기울임 형태를 갖는다.
- **학습 중 안전**에는 정직한 선택지가 몇 개뿐이고, 보상 페널티가 그중 가장 약하다:
  1. 시뮬레이션에서 학습한다(지배적 — 12톤 기계는 "해 보고 고치기"를 할 수 없다);
  2. 안전하지 않은 명령이 액추에이터에 닿기 전에 자르거나 거부하는 **안전 필터·엔벨로프**로
     정책을 감싼다([[04-robotics/mpc|MPC]]가 흔히 그 필터다);
  3. **제약 MDP**(보상과 별도의 비용 신호가 있고 그 기대 총합이 한도 아래에 머물러야 하는 MDP)로
     정식화해 그 상한 아래에서 보상을 최적화한다(한도를 승수로 목적함수에 접어 넣는 라그랑주 방법,
     [[02-foundations/optimization|최적화 §4]] 참고);
  4. 보상에 위반 페널티를 넣는다 — 편하지만 **아무것도 보장하지 않는다**: 과제 보상이 충분히
     크면 페널티를 사 버린다.

  *장치 2~4를 식으로.* **안전 필터**는 정책의 명령 $a_\pi$를, 필터가 보증할 수 있는 안전 집합 $\mathcal{C}(s)$ 안에서 가장 가까운 명령으로 바꾼다.
  $$a_{\text{safe}} = \arg\min_{a \in \mathcal{C}(s)} \lVert a - a_\pi \rVert^2$$
  그래서 안전한 명령은 그대로 지나가고 안전하지 않은 명령은 경계로 사영된다. 속도 한계 $\mathcal{C} = [-0.5, 0.5]$ m/s에서 요청된 $0.8$ m/s는 $0.5$로 실행된다. 정책 뒤에서 강제하므로 정책이 무엇을 내든 보장이 성립한다. **제약 MDP**는 비용 함수 $c(s, a) \ge 0$와 한도 $d$를 더하고, 그 라그랑주 완화는 승수 $\lambda \ge 0$을 도입한다.
  $$\max_\pi\ J_r(\pi) \ \ \text{s.t.}\ \ J_c(\pi) \le d, \qquad \mathcal{L}(\pi, \lambda) = J_r(\pi) - \lambda\,\big(J_c(\pi) - d\big)$$
  $J_r$과 $J_c$는 보상과 비용의 기대 할인 총합이다. 라그랑주 방법은 $\mathcal{L}$에 대해 $\pi$를 개선하는 것과, 제약이 깨지는 동안 $\lambda$를 *올리는* 것을 번갈아 한다. **계산 예와, 그것이 드러내는 반례.** 정책 둘: $\pi_1$은 $J_r = 10$, $J_c = 3$, $\pi_2$는 $J_r = 8$, $J_c = 1$, 한도 $d = 2$. 제약 문제의 답은 유일하게 허용되는 $\pi_2$다. 비용 단위당 고정 보상 페널티 $0.5$는 둘을 $10 - 1.5 = 8.5$와 $8 - 0.5 = 7.5$로 매겨 *위반하는* $\pi_1$을 고른다 — 장치 4가 말한 그대로 실패한다. 라그랑주 점수는 $10 - \lambda$와 $8 + \lambda$이므로 $\lambda$가 $1$을 넘도록 올라가면 $\pi_2$를 고른다. 승수는 짐작하는 값이 아니라 제약이 성립할 때까지 조정되는 페널티 가중치다.
- **진짜 비용은 연산이 아니다.** 하드웨어에서는 에피소드마다 리셋이 필요하고, 리셋은 인간
  노동이며, 마모와 안전 심사가 실제 예산이다([[04-robotics/hri-safety|HRI·안전]]).
- 이 이야기의 전이 쪽 절반 — reality gap, 랜덤화, privileged learning, 잔차, 배치 사다리 — 은
  [[05-construction-robotics/sim-to-real|Sim-to-Real 가이드]]다. 관심이 언어모델이 아니라
  로봇이라면 이 페이지 바로 다음에 읽어라.

### 5. RL 실험 절 읽기

RL 결과는 거의 어떤 하위 분야보다 규약에 의존한다. 확인할 것:

| 논문 표현 | 확인할 것 |
|---|---|
| "$2\times10^9$ environment steps 학습" | 스텝 ≠ 시간이고 스텝 ≠ 실제 경험 — 병렬 환경이 몇 개이고, 시뮬레이션인가 실기계인가 |
| "sample-efficient" | environment step 기준인가, wall-clock인가, *실기계 시간* 기준인가? 희소한 것은 마지막뿐이다 |
| "PPO/SAC 베이스라인을 능가" | 같은 보상·같은 관측 공간·같은 커리큘럼·같은 튜닝 예산인가? |
| 학습 곡선 | x축 단위, 시드 개수, 음영이 표준편차인지 표준오차인지 신뢰구간인지 ([[02-foundations/ml-practice\|ML 실무 §4]]) |
| "PPO를 쓴다" | 옵티마이저 이름은 거의 아무것도 특정하지 않는다 — 보상·관측·커리큘럼이 특정한다 ([[01-canonical-papers/notes/1-foundations/ppo\|PPO 노트]]) |
| "zero-shot transfer" | 목표 도메인 학습 갱신이 없다는 뜻 — 단 시뮬레이터는 실데이터로 만들었을 것이다 |
| success rate | 평가 에피소드 수, 초기 상태 분포, 시간 제한은? |

- **규모, 숫자로.** $2\times10^9$ 스텝은 엄청나 보인다. 병렬 환경 4,096개면 환경당 488,000
  스텝이고, 50 Hz 제어 주기에서 9,760초 ≈ **환경당 시뮬레이션 경험 2.7시간** — GPU 몇 시간이다.
  같은 숫자를 *실기계 한 대*에서 50 Hz로 채우면 **1.3년**이다. 이 비율이 로봇 RL이 시뮬레이션에
  사는 이유 전부다.
- **관측·행동 공간이 결과의 일부다.** 정책이 무엇을 보는지(관절 상태? 지형 높이맵? 특권 토질
  파라미터?)와 무엇을 내보내는지(관절 속도? 밸브 전류? 말단 자세?)가 알고리즘보다 문제를 더
  크게 바꾼다. 관측 **정규화 통계량은 모델의 일부**다 — 그것 없이 정책만 배포하는 것이 전형적인
  조용한 실패다.
- **에피소드 종료와 시간 제한.** 과제가 실패해서 끝난 것과 시계가 다 되어 끝난 것은 다르다:
  후자는 여전히 가치 함수를 부트스트랩해야 하고, 이를 종료로 취급하면 정책에게 "시간 제한에서
  세계가 끝난다"고 조용히 가르치게 된다.
  - *TD 타깃 안에서.* 구현은 전이마다 플래그 $d \in \{0, 1\}$를 들고 다음을 계산한다.
  $$y = r + \gamma\,(1 - d)\, V(s')$$
  그래서 $d = 1$이면 미래가 빠진다. **종료**(과제가 정말 끝남: 목표 도달, 또는 기계 전도)는 $d = 1$이다. **절단**(과제가 계속될 상태에서 시계가 다 됨)은 $s'$에 여전히 미래가 있으므로 $d = 0$을 유지해야 한다. 계산 예: $r = 1$, $\gamma = 0.99$, $V(s') = 10$이면 부트스트랩 타깃은 $10.9$이고, 시간 초과를 종료로 표시하면 $1$, 곧 올바른 타깃의 10분의 1도 안 되는 값이 시간 한계 근처의 모든 상태에 들어간다.

### 6. 보상을 배우기: 역강화학습과 선호

*한 문장으로:* 아무도 목표를 점수로 적어 내지 못할 때는 사람이 하는 일이나 두 시도 중 어느 쪽을 더 좋아하는지에서 점수 자체를 배울 수 있지만, 같은 행동을 설명하는 점수가 여럿이므로 방법마다 그중 하나를 고르는 규칙이 되고, 배운 점수는 그 뒤에 여전히 최적화해야 한다.

*이 절에서 하나만 가져간다면:* 보상 차이에 대한 로지스틱 회귀로 맞추는 Bradley–Terry 모델 $P(A \succ B)=\sigma\big(R(A)-R(B)\big)$ — RLHF의 보상 모델이자 DPO가 고쳐 쓰는 손실이고, §6.3의 계산 예제에서 "A가 낫다"는 답 하나가 $w$를 $(0.2,\ 0.6)$에서 $(0.499,\ 0.301)$로 옮기고 손실을 $0.913$에서 $0.599$로 낮춘다.

§2는 보상을 엔지니어가 써 넣는 것으로 다뤘다. 그런데 때로는 아무도 보상을 적어 내지 못하고,
대신 누군가 거동을 *보여 주거나* 두 시도 중 어느 쪽이 나았는지 말해 줄 수는 있다. 그러면
보상 자체가 배울 대상이 된다.

**행동을 베끼지 않고 보상을 배우는 이유.** 행동 복제는 행동을 베끼고, 그것이 어디서 깨지는지는
§1이 보였다: 정책이 시연이 덮지 않은 상태로 흘러가고 오차가 누적된다. 학습된 보상은 다른
정보를 담는다.

- 전문가가 *무엇을* 했는지만이 아니라 *왜* 그렇게 했는지 — 무엇과 무엇을 맞바꿨는지 — 를 말한다.
- 전이된다. 같은 보상을 다른 동역학, 다른 로봇, 어떤 시연도 시작하지 않은 초기 상태에서
  최적화해도 말이 되는 거동이 나온다. 복제한 상태→행동 사상은 거기서 할 말이 없다.
- 전문가가 준최적이거나 능력이 다를 때 학습자가 전문가보다 잘할 여지를 준다.

대가는 다시 RL이다: 학습된 보상은 그것에 대해 정책을 최적화해야 비로소 쓸모가 있다.

**모든 방법이 깨야 하는 모호성.** "전문가는 어떤 보상에 대해 최적이다"라는 말은 보상을 하나로
정하지 못한다. $r = 0$이면 전문가를 포함한 모든 정책이 최적이다. 참 보상에 양수를 곱해도
마찬가지이고, §2의 포텐셜 기반 shaping 항을 더해도 마찬가지다. 아래 각 방법은 같은 데이터를
설명하는 수많은 보상 가운데 하나를 *고르는 원리*로 읽어라.

#### 6.1 특징 맞추기와 최대 마진 계획

**특징 맞추기(feature matching).** 손으로 고른 특징 위의 선형 보상
$r(s,a) = w^\top\phi(s,a)$를 가정한다. 그러면 정책의 기대 리턴은 $w^\top\mu(\pi)$이고,
$\mu(\pi)$는 할인된 특징 기댓값이다:

$$\mu(\pi) = E_\pi\Big[\sum_{t} \gamma^t\,\phi(s_t,a_t)\Big]$$

리턴이 이렇게 인수분해되는 것은 보상이 선형이어서 $w$가 기댓값 밖으로 나오기 때문이다. 쓸모
있는 귀결: 학습자의 $\mu$가 전문가의 것과 $\epsilon$ 이내이면, $\lVert w\rVert \le 1$인
*모든* $w$에 대해 리턴도 $\epsilon$ 이내다. 학습자와 전문가의 특징 기댓값을 $\mu_L$, $\mu_E$로 쓰면
코시–슈바르츠 부등식이
$|w^\top\mu_L - w^\top\mu_E| \le \lVert w\rVert\,\lVert\mu_L - \mu_E\rVert \le 1 \cdot \epsilon$을 준다. 참 $w$를 복원하지 않고도 특징을
맞추면 전문가 수준의 리턴이 보장된다. 구체적으로: "이 교차로에서 우회전"을 외우는 대신(전문가가
지나가 본 적 없는 교차로에서는 쓸모없다), 전문가의 경로가 정지 표지판을 피하고 제한 속도가 높은
길을 좋아한다는 것을 알아채고 같은 특징 합을 내는 경로를 찾는다. **최대 마진 계획**(Maximum
Margin Planning; Ratliff, Bagnell & Zinkevich, ICML 2006)은 이를 이차 계획 문제로 만든다: 전문가가
다른 모든 후보 정책을 — 그 정책이 전문가와 다를수록 더 큰 — 마진으로 이기게 하는 가장 작은
$w$를 고르고, 불완전한 전문가를 위해 슬랙 변수를 둔다. 기호로 쓰면, $\mu_E$는 전문가의 특징 기댓값, $\mu(\pi)$는 후보의 것, $\ell(\pi) \ge 0$은 $\pi$가 전문가와 얼마나 다른지 재는 손실, 슬랙 $\xi \ge 0$의 가중치는 $C$다.
$$\min_{w,\ \xi \ge 0}\ \tfrac12 \lVert w \rVert^2 + C\,\xi \quad \text{s.t.} \quad w^\top \mu_E \ \ge\ w^\top \mu(\pi) + \ell(\pi) - \xi \quad \text{for every candidate } \pi$$
$\lVert w\rVert$를 최소화하므로 전문가를 여전히 가려내는 가장 덜 극단적인 보상이 골라지고, 이 방법이 척도 모호성을 깨는 방식이 이것이다. 할인된 특징 기댓값 자체는 구체적인 숫자다. 스텝 $0, 1, 2$의 특징이 $\phi = 1, 0, 1$이고 $\gamma = 0.9$면 $\mu = 1 + 0 + 0.81 = 1.81$이다.

#### 6.2 최대 엔트로피 IRL과 GAIL

**최대 엔트로피 IRL**(Ziebart, Maas, Bagnell & Dey, AAAI 2008). 특징 맞추기에도 한 층 위의
모호성이 남는다: 특징 기댓값이 같은 궤적 분포는 많고, 그중 일부는 특징이 주지 않는 이유로 특정
경로를 편애한다. MaxEnt의 원리는 특징이 요구하지 않는 것에는 아무것도 걸지 않는 것이다 — 전문가의
특징 합을 맞추는 모든 분포 가운데 엔트로피가 최대인 것을 택한다
([[02-foundations/information-theory|정보이론]]).

*모델.* 기대 특징 합을 맞춘다는 제약 아래 엔트로피를 최대화하는 것은 라그랑주 승수 문제이고
([[02-foundations/optimization|4. 최적화 §4]]), 그 해는 언제나 제약된 특징에 대해 지수형이며
특징 제약에 붙은 승수가 $w$ 역할을 한다. 그래서 해는 보상에 대해 지수형이며,
$f(\tau) = \sum_t \phi(s_t,a_t)$는 궤적의 특징 합이다:

$$P_w(\tau) = \frac{\exp\big(w^\top f(\tau)\big)}{Z(w)}, \qquad Z(w) = \sum_{\tau}\exp\big(w^\top f(\tau)\big)$$

잡음 있는 전문가로 읽으면 된다: 확률이 보상에 지수적으로 커지므로 좋은 궤적일수록 지수적으로
더 자주 나오지만, 나쁜 궤적도 불가능하지는 않다.

*적합.* 시연 $N$개 $\tau_1,\dots,\tau_N$에 최대우도로
$w$를 맞추면:

$$\nabla_w \log \prod_{i} P_w(\tau_i) = \sum_{i=1}^{N} f(\tau_i) - N\,E_{\tau\sim P_w}\big[f(\tau)\big]$$

둘째 항은 $\log Z(w)$의 미분이 모델 자신의 기대 특징 합이기 때문에 생긴다. 그래서 그래디언트는
*전문가의 특징 합 빼기 현재 모델이 기대하는 특징 합*이고, 특징이 맞는 바로 그때 0이 된다.

*비용.* **비용은 전부 그 둘째 항에 있다.** 현재 보상이 그럴듯하게 만드는 모든 궤적에 대한 기댓값이므로,
그래디언트 한 스텝마다 현재 $w$ 아래의 계획을 한 번 통째로 풀어야 한다. Ziebart 등은 이를
역방향 패스(log-sum-exp 형태의 soft 가치 반복)와 상태 방문 빈도를 구하는 순방향 패스로 계산하고,
샘플러로 대신하면 순방향 RL 실행 한 번이 된다. 바깥 루프가 보상을 배우고 안쪽 루프가 매번 RL
문제를 푼다 — 작은 이산 세계에서는 다룰 만하지만 그보다 크면 비싸다.

*적대적 버전.* **GAIL**(Ho & Ermon,
NeurIPS 2016)이 적대적 후손이다: 전문가의 상태-행동 쌍과 정책의 것을 구별하는 판별기가 학습된
보상 역할을 하고, 명시적 보상을 먼저 복원하지 않은 채 정책을 그것에 대해 RL로 학습한다. 쌍이 얼마나 *정책 같은지* 매기는 판별기 $D(s, a) \in (0, 1)$, 전문가 정책 $\pi_E$, 엔트로피 가중치 $\lambda \ge 0$에 대한 안장점 목적함수는 다음과 같다.
$$\min_\pi\ \max_D\ \ E_{\pi}\big[\log D(s, a)\big] + E_{\pi_E}\big[\log\big(1 - D(s, a)\big)\big] - \lambda\, H(\pi)$$
그래서 $D$는 둘을 구별하도록, $\pi$는 비용 $\log D(s, a)$로 RL을 해서 자기 쌍이 전문가의 것과 구별되지 않도록 학습된다. 어떤 판별기도 우연보다 잘할 수 없으면 모든 곳에서 $D = 0.5$이고 정책의 상태-행동 분포가 전문가의 것과 일치한다. 분포 맞추기, 곧 손으로 고른 특징 없는 특징 맞추기와 같은 목표다.

> [!example] 계산 예제 · Worked example
> 스칼라 특징을 가진 궤적 둘, $f(\tau_1) = 2$, $f(\tau_2) = 1$. 전문가를 네 번 기록했더니
> $\tau_1$이 세 번, $\tau_2$가 한 번이었다. 전문가 특징 합은 $3(2) + 1 = 7$(평균 $1.75$)이다.
>
> - **$w = 0$에서** 두 궤적의 확률은 각각 $0.5$, 모델이 기대하는 $f$는 $1.5$, 그래디언트는
>   $7 - 4(1.5) = 1.0$ — 양수이므로 $w$를 올린다.
> - **$w = 1$에서** $P(\tau_1) = e^{2}/(e^{2} + e^{1}) = 0.731$, 기대 $f = 1.731$, 그래디언트는
>   $7 - 4(1.731) = 0.076$으로 줄어든다.
> - **$w = \ln 3 \approx 1.099$에서** $P(\tau_1) = 0.75$ — 전문가 자신의 빈도 — 이고 기대
>   $f = 1.75$, 그래디언트는 정확히 $0$이다.
>
> 두 가지로 읽는다. 맞춘 모델은 늘 $\tau_1$을 고르는 대신 전문가의 3대 1 혼합을 재현한다 —
> 지수형의 "불가능하지는 않다"가 이것이다. 그리고 네 시연이 모두 $\tau_1$이었다면 $E[f] < 2$이므로
> 그래디언트 $8 - 4E[f]$가 모든 $w$에서 양수로 남아 $w$가 한없이 커진다 — 완벽히 일관된 전문가는
> 무한히 확신하는 것으로 읽히고, 실제 적합에서 $w$를 정규화하는 이유가 이것이다.

#### 6.3 선호: Bradley–Terry, RLHF, DPO

**시연 대신 선호.** 시연이 잘못된 요구일 때가 있다: 고차원 팔은 잘 원격조종하기 어렵고,
시뮬레이션에서 운전을 시연한 사람들이 자기가 시연한 것보다 더 방어적인 운전 방식을
선호한다는 결과도 있다(Basu et al., HRI 2017). 두 시도를 비교하는 편이 쉽다. 표준 모델은 **Bradley–Terry**(Bradley & Terry,
*Biometrika*, 1952)다:

$$P(A \succ B) = \sigma\big(R(A) - R(B)\big) = \frac{1}{1 + e^{-(R(A) - R(B))}}$$

차이만 들어가므로 모든 보상에 같은 상수를 더해도 아무것도 바뀌지 않는다 — 이번에는 평행이동의
형태로 돌아온 모호성이다. 적합은 라벨된 쌍에 대해 $\log\sigma(R(A) - R(B))$를 최대화하는 것이고,
이는 **보상 차이에 대한 로지스틱 회귀다.** 로지스틱 회귀는 가장 기본적인 예/아니오 분류기로,
선형 점수에 시그모이드를 씌워 확률을 예측하고 바로 이런 로그우도를 최대화해(교차 엔트로피를
최소화하는 것과 같다; [[02-foundations/information-theory|5. 정보이론 §2]] 참고) 가중치를 맞춘다. $y_i \in \{0, 1\}$인 라벨 예제 $(x_i, y_i)$에 대해
$$P(y = 1 \mid x) = \sigma\big(w^\top x\big), \qquad \max_w \sum_i \Big[y_i \log \sigma\big(w^\top x_i\big) + (1 - y_i)\log\big(1 - \sigma(w^\top x_i)\big)\Big]$$
이다. 각 예제가 실제로 가진 라벨의 로그 확률을 보태기 때문이다. 그래디언트는 $\sum_i (y_i - \sigma(w^\top x_i))\,x_i$, 곧 오차 곱하기 입력이고, 아래 계산 예제가 쓰는 갱신이 이것이다. 선형 보상이면 $R(A) - R(B) = w^\top(\phi(A) - \phi(B))$이므로
비교 하나가 특징 차이를 입력으로 하는 로지스틱 회귀 예제 하나이고, 잡음 없는 답 하나는 가능한
$w$의 공간을 초평면 $w^\top(\phi(A) - \phi(B)) = 0$을 따라 반으로 자른다.

- **인간 선호로부터의 심층 RL**(Christiano et al., NeurIPS 2017)은 선형 보상을 짧은 거동 클립에
  대한 인간 비교에 맞춘 신경망으로 바꾸고, 그것에 대해 RL로 정책을 학습하며, 정책이 바뀌는 동안
  계속 새 비교를 묻는다.
- **이것이 RLHF의 보상 모델이다.** [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]]는
  라벨러 순위에 대해 이 형태의 쌍별 랭킹 손실로 보상 모델을 학습한 뒤, KL 페널티(§4) 아래에서 PPO([[02-foundations/rl-basics|7. RL 기초 §4]])로
  정책을 그것에 대해 최적화한다.
- **DPO**(Rafailov et al., NeurIPS 2023)는 명시적 보상 모델을 없앤다: KL 정규화 목적에서는 최적
  정책이 보상을 결정하므로, Bradley–Terry 손실을 정책의 로그 확률 비로 직접 쓰고 RL 루프 없이
  학습할 수 있다. 유도는 세 줄이다.
  - 프롬프트 하나에 대해 $E_{y\sim\pi}[r(y)] - \beta\,\mathrm{KL}(\pi \Vert \pi_{\text{ref}})$를
    최대화하는 정책은 $\pi^*(y) = \pi_{\text{ref}}(y)\,e^{r(y)/\beta}/Z$이고, $Z$는 정규화 상수다.
    위의 MaxEnt와 같은 지수형이며, 이유도 같은 라그랑주 승수 논리다.
  - 로그를 취해 보상에 대해 풀면
    $r(y) = \beta\log\big(\pi^*(y)/\pi_{\text{ref}}(y)\big) + \beta\log Z$.
  - 이를 Bradley–Terry에 대입한다. $A$와 $B$는 같은 프롬프트에 대한 답이므로 $Z$를 공유하고,
    $r(A) - r(B)$에서 $\beta\log Z$가 약분된다. 남는 것은
    $\sigma\big(\beta\log\frac{\pi(A)}{\pi_{\text{ref}}(A)} - \beta\log\frac{\pi(B)}{\pi_{\text{ref}}(B)}\big)$로,
    학습 중인 정책과 고정된 기준 정책만 들어 있다.
  - 그 결과인 **DPO 손실**을 프롬프트 $x$, 선호된 답 $y_w$, 거부된 답 $y_l$의 선호 삼중쌍에 대해 평균하면
    $$\mathcal{L}_{\text{DPO}}(\theta) = -E_{(x, y_w, y_l)}\Big[\log \sigma\Big(\beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)}\Big)\Big]$$
    이므로 $\beta \log(\pi_\theta/\pi_{\text{ref}})$가 보상 역할을 하는 Bradley–Terry 음의 로그우도다. 계산 예: $\beta = 0.1$, 선호된 답의 로그 비율 $+2.0$, 거부된 답의 $-1.0$이면 $\sigma(0.2 + 0.1) = \sigma(0.3) = 0.574$, 손실 $0.554$다. 그래디언트는 그 확률이 1에 다가갈 때까지 선호된 답의 로그 비율을 올리고 거부된 답의 것을 내린다.
- **로봇을 위한 능동 질의**(Sadigh et al., RSS 2017, "Active Preference-Based Learning of Reward
  Functions"): 답 하나가 1비트뿐이므로, 그 답이 남은 그럴듯한 보상 가중치를 최대한 많이 지우도록
  보여 줄 쌍을 고른다.

> [!example] 계산 예제 · Worked example
> 선형 보상, 특징 $\phi(A) = (1, 0)$, $\phi(B) = (0, 1)$, 현재 가중치 $w = (0.2, 0.6)$.
> 그러면 $R(A) = 0.2$, $R(B) = 0.6$이고 모델의 예측은 $P(A \succ B) = \sigma(-0.4) = 0.401$이다.
>
> 사람이 **A가 낫다고** 답한다. 로그우도 그래디언트는
> $(1 - 0.401)\,(\phi(A) - \phi(B)) = (0.599, -0.599)$ — 오차 곱하기 특징 차이로, 로지스틱 회귀와
> 똑같다. 스텝 크기 $0.5$로 한 번:
>
> - $w \leftarrow (0.2, 0.6) + 0.5\,(0.599, -0.599) = (0.499, 0.301)$;
> - 예측은 $\sigma(0.199) = 0.550$이 되고, 손실 $-\log P$는 $0.913$에서 $0.599$로 내려간다.
>
> 스텝 크기는 모델이 얼마나 놀랐는지인 $1 - P$에 비례한다. 이미 $P$가 1에 가깝게 예측한 비교는
> $w$를 거의 움직이지 않는다.

#### 6.4 보상 학습 논문 읽기

**보상 학습 논문 읽기.** 네 가지 질문을 순서대로:

| 질문 | 확인할 것 |
|---|---|
| 어떤 데이터인가? | 시연, 쌍별 비교나 순위, 물리적 교정 — 몇 개이고 누구에게서(전문가, 크라우드 작업자, 저자 본인) |
| 어떤 보상 클래스인가? | 손으로 설계한 특징 위의 선형(들여다볼 수 있지만 전문성 대부분을 특징이 떠안는다) vs 신경망(표현력이 크고 데이터를 많이 먹으며 들여다보기 어렵다) |
| 어떻게 평가하는가? | ① 복원한 보상을 알려진 참 보상과 비교(시뮬레이션에서만 가능) ② 학습된 보상으로 학습한 정책을 *참* 과제 지표로 채점 ③ 보류된 선호에 대한 정확도. 서로 다른 질문에 답한다: ③이 높다고 그것만으로 ②가 좋다는 뜻은 아니다 |
| 무엇이 reward hacking을 막는가? | 학습된 보상도 손으로 쓴 보상과 똑같은 대리물이고(§2), 데이터를 못 본 곳에서 가장 믿을 수 없는데 최적화하는 정책이 가는 곳이 바로 거기다. 기준 정책으로의 KL 닻(§4)이나 정책이 바뀌는 동안의 지속적 질의가 있는지 보라 |

### 7. 학습자가 둘 이상일 때, 짧게

위의 모든 내용은 정상(stationary) 세계의 학습자 하나를 가정한다. 현장에는 기계가 여러 대 있으니, 정확히 어떤 가정이 깨지고 분야가 그것에 무엇을 하는지는 알아 둘 만하다. 이 절은 Literacy 깊이다. 다중 에이전트 논문을 읽고, 그 문제가 아닐 때를 알아볼 만큼만 다룬다.

**무엇이 깨지는가, 이 페이지의 대상 위에서.** 버킷 MDP에 기계를 두 대 놓고 $B$의 적재 자리는 하나라고 하자. 혼자라면 이동의 값은 $Q^*(A,\text{move})=9$, 대기는 $8.1$이다. 둘이 동시에 움직이면 부딪쳐 $A$로 되돌아오고 수리 비용 $1$을 치러 각자 $7.1$을 받는다. 그러면 기계 1의 이동 가치는 기계 2가 얼마나 자주 움직이는지 $p$에 달린다.

$$Q_1(\text{move})=(1-p)\cdot 9+p\cdot 7.1=9-1.9p,\qquad Q_1(\text{wait})=8.1$$

즉 $p<0.9/1.9=0.474$인 동안만 이동이 낫다. 세계는 하나도 바뀌지 않았는데 기계 2가 학습하면 기계 1의 최적 행동이 뒤집힌다. [[02-foundations/rl-basics|7. RL 기초 §1]]의 MDP가 *고정*이라고 가정한 전이와 보상 안에 이제 움직이는 다른 정책이 들어 있는 것이다. 이것이 다중 에이전트 학습을 정의하는 어려움인 **비정상성**이고, 독립 학습자 둘이 $p=0.474$ 근처에서 서로를 쫓기만 하고 수렴하지 않을 수 있는 이유다. 이 게임에는 순수 균형도 둘 있다. 하나가 가고 하나가 기다리는 것인데, "어느 기계가 양보하는가"는 보상만으로는 정해지지 않는 조율의 선택이다.

**추가되는 비용 둘.** 결합 행동 공간이 곱해진다. 행동이 각 $|\mathcal A|$개인 기계 $n$대면 결합 행동은 $|\mathcal A|^n$개이므로, 행동 열 개짜리 다섯 대면 $10^5$이다. 결합 행동 위의 크리틱은 곧바로 표로 다룰 수 없게 된다. 그리고 공유 보상은 **기여 배분**을 감춘다. 현장 처리량이 올랐다면 어느 기계 덕분인가? 에이전트별 보상은 귀속을 분명히 하지만 자기 몫만 챙길 유인을 만들고, 공유 보상은 그 반대다.

**분야는 무엇을 하나.** 표준적인 절충은 **중앙 집중 학습, 분산 실행**이다. 학습할 때 크리틱은 모든 에이전트의 관측과 행동을 보고, 실행할 때 각 정책은 자기 것만 본다. 그래서 각 에이전트의 세계는 비정상이어도 크리틱은 정상이고, 배치에는 공유 채널이 필요 없다. 가치 분해(에이전트별 가치를 더하거나 단조롭게 섞는 것)는 결합 가치에서 분산 argmax를 사 오고, 에이전트별 정책에 크리틱 하나를 두는 것이 정책 그래디언트 판이다. 같은 기계끼리 파라미터를 공유하면 표본 비용이 준다. 논문에서는 넷을 본다. 학습 때와 시험 때의 에이전트 수, 실행이 정말 분산인지, 기준선이 *독립 학습자*인지 아니면 단일 에이전트 기법인지, 보상이 공유인지 에이전트별인지.

**그 문제가 아닐 때.** 조율에는 학습이 전혀 필요 없는 제어 쪽 답이 있는 경우가 많다. [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §8]]은 리더 하나를 여러 팔로워에 수동성을 지키는 결합과 회피 함수로 잇고, 오늘의 건설 기계 편대는 함께 학습되는 대신 중앙에서 감독된다([[05-construction-robotics/lineage|계보, 3시대]]). 여기 연구 프로그램의 코어는 접촉하는 매니퓰레이터 한 대이므로([[07-research-program/index|7. §7]]) 다중 에이전트 학습은 Literacy에 둔다. 실패 방식을 알아 두고, 조율 자체가 기여일 때만 꺼낸다.

### 8. 그룹 상대 RL: 추론 모델, 그리고 성공에서 배우는 VLA

2025년의 추론 언어 모델들은 로봇에 유난히 잘 맞는 모양의 정책 그래디언트 방법으로 학습되었다. DeepSeek-R1-Zero는 사람이 쓴 추론 기록 없이, 프로그램이 확인할 수 있는 보상 — 최종 답이 맞았나, 형식을 지켰나 — 만으로 강화학습을 해서 추론을 익혔고, 그 과정에서 자기 반성과 검증이 창발했다([DeepSeek-AI, *Nature* 645, 2025](https://arxiv.org/abs/2501.12948)). 최적화기는 GRPO였다.

> **그룹 상대 정책 최적화의 정의.** **GRPO**(group relative policy optimization)는 학습된 가치 함수가 아니라 *같은 출발점에서 뽑은 표본 묶음을 기준선으로 쓰는 정책 그래디언트 추정량*이다. 정의 조건은 셋이다. 프롬프트나 시작 상태마다 **현재 정책에서 결과 $G$개의 묶음을 뽑는다.** 각 결과의 **이득은 묶음 안에서 표준화한 보상**이므로 비평가 망을 학습하지 않는다. 그리고 정책은 **PPO의 잘린 비율로 갱신**하며([[02-foundations/rl-basics|7. RL 기초 §4]]), 기준 정책에 대한 KL 벌점을 보상이 아니라 손실에 더한다.
>
> $$\hat A_i=\frac{r_i-\operatorname{mean}(r_1,\dots,r_G)}{\operatorname{std}(r_1,\dots,r_G)},\qquad J(\theta)=\mathbb E\Big[\frac1G\sum_{i=1}^{G}\frac{1}{|o_i|}\sum_{t}\min\big(\rho_{i,t}\hat A_i,\ \operatorname{clip}(\rho_{i,t},1-\varepsilon,1+\varepsilon)\,\hat A_i\big)-\beta\,D_{\mathrm{KL}}\big(\pi_\theta\,\Vert\,\pi_{\text{ref}}\big)\Big]$$
>
> 여기서 $o_i$는 $i$번째로 뽑은 출력, $|o_i|$는 토큰이나 스텝으로 센 그 길이, $\rho_{i,t}$는 $t$번째 토큰에 대한 새 정책 확률과 옛 정책 확률의 비다. 그래서 한 출력의 모든 토큰이 그 출력의 이득을 나눠 갖는다.
>
> - **예**: GRPO가 처음 나온 DeepSeekMath. 영어 지시 데이터로 한 RL이 GSM8K를 $82.9\%$에서 $88.2\%$로, MATH를 $46.8\%$에서 $51.7\%$로 올렸다([Shao 외, 2024](https://arxiv.org/abs/2402.03300)).
> - **반례**: 비평가를 둔 PPO. 기준선이 정책과 함께 학습하는 가치 망 $V_\psi$이고, GRPO가 아끼는 메모리가 바로 그것이다.
> - **반례**: DPO(§6.3). 아무것도 뽑지 않고 보상도 계산하지 않는다. 고정된 선호 쌍에서 배운다.

**버킷 MDP에서, 손으로.** 정책이 $A$에서 곧바로 버킷을 옮기면 보상 $1$, 기다리면 $0$을 준다. $A$에서 네 번 돌려 옮기기, 기다리기, 기다리기, 옮기기가 나오면 보상은 $(1,0,0,1)$, 평균 $0.5$, 표준편차 $0.5$, 이득은 $(+1,-1,-1,+1)$이다. $\log\pi(\text{move}\mid A)$를 두 번 올리고 $\log\pi(\text{wait}\mid A)$를 두 번 내린다. [[02-foundations/rl-basics|7. RL 기초 §4]]는 알려진 정책에서 기준선 $b=0.6$을 얻었고, GRPO는 그것을 묶음에서 추정한다. 다른 두 묶음이 추정량의 성격을 보여 준다. 넷 중 성공 하나인 $(1,0,0,0)$은 실패 하나마다 $-0.58$에 비해 $+1.73$을 받는다. 드문 성공을 세게 민다. 네 번 모두 성공한 $(1,1,1,1)$은 표준편차가 0이라 평균과 다른 구성원이 없고, 묶음이 아무것도 가르치지 않는다. 네 번 모두 실패해도 같다. (모집단 표준편차를 썼다. $G-1$로 나누는 표본 표준편차는 여기서 모든 이득을 $\sqrt{3/4}$배 할 뿐 부호를 바꾸지 않는다.)

**로봇에 맞는 이유.** 로봇에게 가장 자연스러운 보상은 성공 여부를 확인하는 이진 판정이고, 가장 자연스러운 묶음은 시작 상태 하나를 여러 번 돌린 것이다. RIPT-VLA는 사전학습된 VLA를 드문 이진 성공 보상만으로 사후학습하며, 모두 같은 결과라 정보가 없는 묶음을 버리는 동적 롤아웃 추출과 하나를 뺀 나머지로 구하는 이득을 쓴다. QueST가 $21.2\%$ 나아지고 OpenVLA-OFT가 $97.5\%$에 이르렀다고 보고한다([Tan 외, 2025](https://arxiv.org/abs/2505.17016)). VLA-RL은 조작 궤적을 여러 차례 주고받는 대화로 다뤄, 자기회귀 VLA를 궤적 단위로 온라인 학습하게 한다([Lu 외, 2025](https://arxiv.org/abs/2505.18719)). 추론 모델은 더 오래 생각하는 것을 시험 때 살 수 있다는 것도 보였다. s1은 정선한 예제 $1{,}000$개로만 미세조정하고, 생각을 끊거나 *Wait*를 덧붙여 늘리는 "예산 강제"로 생각의 길이를 조절했다([Muennighoff 외, 2025](https://arxiv.org/abs/2501.19393)). 로봇에서 그 추가 생각은 rate로 치르고, 그 비용은 [[03-deep-learning/vla/index|4. VLA §6]]이 센다.

**그룹 상대 로봇 논문에 물을 것**, §5의 점검표에 더해: 롤아웃을 어디서 — 시뮬레이션인가 실제 기계인가 — 돌렸고 갱신마다 몇 개가 들어갔나. 무엇이 성공을 판정하나. 성공 검출기가 곧 보상이다. 묶음 크기, 그리고 모두 성공하거나 모두 실패한 묶음은 어떻게 했나. KL 기준은 무엇인가. 그리고 이득이 실제 로봇에서 제 제어 주기로 유지되었나.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 버킷에서 행동 복제한 정책의 가치와 최적값과의 차이를 계산하고, DAgger가 BC의 학습 분포에서 무엇을 바꾸는지 말한다.
- [ ] 순수 BC의 비용이 $O(\epsilon T^2)$로, no-regret 학습자의 비용이 $O(\epsilon T)$로 자라는 이유와 행동 청킹이 $T$에 하는 일을 설명한다.
- [ ] 써 놓은 보상이 최적해를 뒤집는 유휴 보너스를 찾고, 같은 보너스를 주는 포텐셜 기반 항은 왜 뒤집지 못하는지 보인다.
- [ ] KL 정규화 파인튜닝 목적함수와 그 지수 기울임 최적해를 쓰고, $\beta \to 0$과 $\beta \to \infty$가 무엇을 돌려주는지 말한다.
- [ ] 보상 페널티가 왜 안전 보장이 아닌지 말하고, 더 강한 두 장치를 댄다.
- [ ] 논문의 environment step 수를 환경당 시뮬레이션 시간과 실기계 시간으로 바꾸고, TD 타깃에서 종료와 절단을 구분한다.
- [ ] Bradley–Terry 그래디언트 한 스텝을 손으로 밟고, KL 정규화 최적해에서 DPO 손실을 유도한다.
- [ ] 기계 두 대의 버킷에서 상대의 정책이 내 최적 행동을 뒤집는 확률을 구하고, 중앙 집중 학습·분산 실행이 무엇을 사 오는지 말할 수 있다.
- [ ] 이진 결과 묶음의 GRPO 이득을 손으로 계산하고, 모두 성공한 묶음이 왜 아무것도 가르치지 않는지, 그것을 쓰는 로봇 논문에 무엇을 물을지 말할 수 있다.

> [!tip] 더 깊이 · Going deeper
> Sutton·Barto의 [*Reinforcement Learning: An Introduction*](http://incompleteideas.net/book/the-book.html)은 [[02-foundations/rl-basics|7. RL 기초]]가 압축한 책이다. 그 책은 §1과 §4 — 모방 대 RL, 물리 기계 위의 RL — 를 다루지 않고, 이 페이지가 더하는 것이 바로 그 부분이다. 절마다의 1차 출처는 아래 출처에 모았다.

### 스스로 점검

1. 행동 청킹이 오차 누적을 줄이는 이유는? 그 대가로 잃는 것은?
2. 보상이 $r = 1.0\,\Delta d - 0.2\lVert a\rVert^2 - 5.0\,\mathbb{1}[\text{한계 접촉}]$인데
   정책이 시작부터 얼어붙는다. 산술적 이유와 처방 하나를 말하라.
3. 어떤 논문의 제안 방법은 커리큘럼을 쓰고 PPO 베이스라인은 안 썼다. 그 절제 실험이 실제로
   측정한 것은 무엇인가?
4. "제약 위반을 보상에서 페널티로 준다"가 왜 안전 보장이 아닌가? 더 강한 장치 두 가지는?
5. 어떤 논문이 병렬 환경 2,048개, 100 Hz에서 $1\times10^9$ environment step을 보고했다.
   환경당 시뮬레이션 경험은 얼마이고, 같은 숫자를 실기계 한 대로 채우면 얼마나 걸리는가?
6. 전문가가 어떤 보상 $r$에 대해 최적이다. 같은 거동이 최적이 되는 다른 보상 두 가지를 들고,
   MaxEnt IRL이 그중 하나를 고르는 원리를 말하라.
7. 궤적 둘, $f(\tau_1) = 3$, $f(\tau_2) = 1$, $\tau_1$의 시연 하나로 MaxEnt IRL을 한다.
   $w = 0$에서 로그우도 그래디언트는 얼마이고, 계속 그것을 따라가면 $w$는 어떻게 되는가?
8. 보상 모델이 $R(A) = 2.0$, $R(B) = 1.0$을 준다. Bradley–Terry가 예측하는 $P(A \succ B)$는
   얼마이고, 모든 보상을 $+10$만큼 옮기면 무엇이 바뀌는가? 논문이 보류된 선호에 대해 95% 정확도를
   보고했다 — 왜 그것이 아직 로봇 정책이 작동한다는 증거가 아닌가?
9. 이진 성공으로 GRPO 사후학습한 VLA가 시뮬레이션에서 $60\%$에서 $90\%$로 올랐다. 묶음이 여덟 개씩이고 이제 대부분의 묶음이 모두 성공이다. 추정량은 무엇을 하고 있으며, 무엇을 바꾸겠는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 정책이 자기 오차 위에서 다시 예측하는 횟수가 $k$분의 1로 줄어 분포 이탈이 느려진다; 대가는 반응성 — 청크 실행 중에 들어온 새 관측을 (부분적으로만) 반영한다.
> 2. 움직이면 매끄러움 항이 즉시 비용을 물리는데 진행 항은 $1.0\Delta d$만 준다; 단위 노름 행동으로 1 cm 이동하면 $0.01 - 0.2 = -0.19$라 가만히 있기(보상 0)가 최적이다. 처방: 진행 항 가중치를 올리거나 $\Delta d$를 비교 가능한 단위로 재척도, 크기 대신 *변화율*에 페널티, 또는 아무것도 안 하는 것이 공짜가 아니도록 스텝당 작은 페널티 추가.
> 3. (방법 + 커리큘럼)과 (커리큘럼 없는 베이스라인)의 차이 — 즉 커리큘럼과 방법을 합쳐서 측정했다. 베이스라인이 같은 커리큘럼을 받기 전까지 이 비교는 아무것도 분리하지 못한다.
> 4. 부드러운 교환이기 때문이다: 과제 보상이 충분히 크면 페널티를 사 버리고, 학습 이전의 탐색 구간에서는 위반을 아무것도 제한하지 않는다. 더 강한 것: 액추에이터 앞에서 안전하지 않은 명령을 거부하는 안전 필터·엔벨로프(대개 MPC), 그리고 기대 위반량의 명시적 상한 아래에서 보상을 최적화하는 제약 MDP 정식화.
> 5. 환경당 $1\times10^9/2{,}048 \approx 488{,}000$ 스텝; 100 Hz면 4,880초 ≈ **1.4시간**의 시뮬레이션 경험이다. 실기계 한 대로는 $10^9/100 = 10^7$초 ≈ **116일**.
> 6. $r = 0$(모든 정책이 최적), $2r$ 같은 양수배, 또는 $r$에 포텐셜 기반 shaping 항 $\gamma\Phi(s') - \Phi(s)$를 더한 것(§2). MaxEnt IRL은 전문가의 특징 합을 맞추는 분포만 남기고 그중 엔트로피가 최대인 것을 택한다. 그러면 지수족 모델 $P_w(\tau) \propto \exp(w^\top f(\tau))$가 정해지고 $w$는 최대우도로 맞춘다.
> 7. $w = 0$에서 두 궤적의 확률이 각각 $0.5$이므로 모델의 기대 $f$는 $2$, 그래디언트는 $3 - 2 = 1$이다. 유한한 모든 $w$에서 $E[f] < 3$이므로 그래디언트가 0에 닿지 않고 $w$는 한없이 커진다. 정규화나 $\tau_2$의 시연이 있어야 유한한 답이 나온다.
> 8. $\sigma(2.0 - 1.0) = \sigma(1) = 0.731$. 차이만 들어가므로 평행이동은 아무것도 바꾸지 않는다. 보류 정확도는 모델이 학습된 데이터 근처에서 뽑은 쌍으로 잰 것이다. 모델에 대해 최적화한 정책은 모델이 아무것도 보지 못한 거동 쪽으로 움직여 모델을 공략할 수 있다(reward hacking, §2). 의미 있는 증거는 학습된 보상으로 학습한 정책을 참 과제 지표로 채점한 결과다.
> 9. 모두 성공한 묶음은 퍼짐이 0이므로 모든 구성원의 이득이 0이고 묶음은 그래디언트를 내지 않는다. 정책이 좋아진 바로 그곳에서 학습이 멈추고, 남은 실패는 몇 안 되는 섞인 묶음에 있다. 정보가 있는 묶음을 남기고 — RIPT-VLA의 동적 롤아웃 추출이 모두 같은 묶음을 버린다 — 더 어려운 시작 상태를 뽑거나 묶음을 키운다. 그다음 시뮬레이터의 성공 검출기가 보상의 전부였으므로, 실제 로봇에서 제 제어 주기로 이득을 확인한다.

### 과제 · Problem set

Tier B. 이 페이지의 대상에서 손잡이 둘을 바꾼다. 할인율 $\gamma = 0.95$, 그리고 $A$에서의 기록이 이동 넷과 대기 둘인 두 번째 조작자. 시뮬레이터는 없고, 모든 문항은 §1, §2와 이 페이지의 계산을 써서 버킷 위에서 손으로 하는 유도다.

1. **그리기.** 이 변형의 그림: 모든 보상과 $\gamma = 0.95$를 적은 MDP, 그 옆의 $V^*(A)$, $V^*(B)$, $Q^*(A,\text{대기})$, 두 번째 조작자의 기록과 그 BC 정책 및 가치, 그리고 $\gamma = 0.95$로 다시 그린 둘째 판 — 유휴 보너스 $b$에 대한 지금 이동과 영원히 대기의 써 놓은 가치, 둘이 만나는 곳, 써 놓은 보상의 최적해가 내는 과제 가치.
2. **유도.** (a) $\gamma = 0.95$에서 $V^*(B)$, $V^*(A)$, $Q^*(A,\text{대기})$. (b) 두 번째 기록의 $\pi_{\text{BC}}(\text{이동}\mid A)$와 $V^{\text{BC}}(A)$, 그리고 $V^*(A)$와의 차이. (c) 써 놓은 보상의 최적해가 영원히 대기로 뒤집히는 유휴 보너스 $b$. 기록이 무엇이든 그것이 $\gamma$와 같음을 보여라. (d) $\Phi(B) = 0$이면서 shaping 항이 대기마다 정확히 $1$을 주는 포텐셜: $\Phi(A)$, 그때 이동이 받는 값, $A$에서의 두 shaped 행동 가치를 구하고 순위가 그대로임을 확인하라. (e) §1 논문 해독기의 닫힌 형태와 $A$에서의 최적 어드밴티지 $A^*(A,\text{이동}) = 0$, $A^*(A,\text{대기}) = Q^*(A,\text{대기}) - V^*(A)$를 써서, $\pi_{\text{ref}} = \pi_{\text{BC}}$에서 $\beta = 0.5$로 KL 정규화 개선을 한 스텝 하라. 새 $\pi(\text{이동}\mid A)$와 그 가치.
3. **해석.** 어떤 논문이 두 번째 조작자의 BC 정책을 대기 스텝마다 $b = 1$을 주는 보상으로 RL 파인튜닝하고, 써 놓은 리턴이 $19.02$에서 $20.0$으로 올랐다고 보고한다. 두 정책의 과제 가치를 계산하고, 그 표가 실제로 보여 준 것이 무엇인지 말하고, 저자에게 요구할 것을 적어라(§2의 읽기 단서와 §5의 표).

> [!note]- 그리는 법 · How to draw it
> - 동그라미 둘, $A$(빈 버킷)와 $B$(가득)에 화살표 셋: $A \to B$ 이동, $A \to A$ 대기, $B \to B$ 머묾. 화살표마다 보상 — $r = 0$, $r = 0$ (+ $b$), $r = +1$ — 을 적고, $\gamma = 0.95$는 판 제목에 한 번 적는다.
> - 대기 루프는 점선으로 그린다. 최적해가 건너뛰는 행동이고, 나쁜 보상이 최적해로 하여금 밟게 만들 수 있는 행동이다.
> - 동그라미 옆에 최적 가치를, $A$에서 나가는 화살표마다 그 행동 가치를 적는다. 그다음 $A$에 기록을 표(이동 | 대기)로, BC 확률을 그 비로, $V^{\text{BC}}(A)$를 $V^*(A)$ 옆에 적는다. 숫자는 늘 둘이고, 하나로 합치지 않는다.
> - 둘째 판의 가로축은 유휴 보너스 $b$, 세로축은 $A$의 가치다. 지금 이동은 $V^*(A)$ 높이의 수평선, 영원히 대기는 원점을 지나는 직선 $b/(1-\gamma)$로 그리고 둘이 만나는 곳을 표시한다. 그다음 써 놓은 보상의 최적해가 내는 과제 가치를 그곳에서 $0$으로 떨어지는 굵은 선으로 그린다.
> - 모든 숫자에 그것을 잰 보상, 곧 써 놓은 보상인지 과제인지를 붙인다. hacking 논증 전체가 그 둘의 차이다.

> [!tip]- 정답 · Solutions
> 1. 그림과 같되 $\gamma = 0.95$: MDP 위에 $V^*(B) = 20$, $V^*(A) = 19$, $Q^*(A,\text{대기}) = 18.05$, 기록 $4 \mid 2$, $\pi_{\text{BC}}(\text{이동}\mid A) = 2/3$, $V^*(A) = 19$ 옆의 $V^{\text{BC}}(A) = 18.54$. 둘째 판에서 지금 이동은 $19$에서 수평, 영원히 대기는 $20b$, 둘은 $b = 0.95$에서 만나고, 써 놓은 보상의 최적해가 내는 과제 가치는 그곳에서 $19$에서 $0$으로 떨어진다.
> 2. (a) $V^*(B) = 1/(1 - 0.95) = 20$, $V^*(A) = 0.95 \times 20 = 19$, $Q^*(A,\text{대기}) = 0.95 \times 19 = 18.05$. (b) $\pi_{\text{BC}}(\text{이동}\mid A) = 4/6 = 2/3$이고, $V^{\text{BC}}(A) = \tfrac23(0.95 \times 20) + \tfrac13(0.95\,V^{\text{BC}}(A))$에서 $V^{\text{BC}}(A) = 12.67/0.6833 = 18.54$, 차이는 $0.46$이다. 두 기록 모두 최적값의 같은 $40/41 = 97.6\%$를 지킨다. 이 조작자는 방문의 5분의 1이 아니라 3분의 1에서 망설이지만, 망설임 한 번의 비용이 $0.9$배가 아니라 $0.95$배이기 때문이다. (c) 써 놓은 보상으로 지금 이동은 $0.95 \times 20 = 19$, 영원히 대기는 $b/(1 - 0.95) = 20b$이므로 $b = 19/20 = 0.95 = \gamma$에서 만난다. 일반적으로 이동은 $\gamma/(1-\gamma)$, 영원히 대기는 $b/(1-\gamma)$이므로 $b = \gamma$에서 뒤집힌다. RL은 기록이 아니라 보상을 최적화하므로 기록은 끼어들지 않는다. (d) 대기는 $\gamma\Phi(A) - \Phi(A) = -0.05\,\Phi(A) = 1$을 받으므로 $\Phi(A) = -20$이고, 이동은 $F = 0 - (-20) = 20$, $B$에서의 한 스텝은 $0$을 받는다. $V'(B) = 20$이므로 $Q'(A,\text{이동}) = 20 + 0.95 \times 20 = 39$, $Q'(A,\text{대기}) = 1 + 0.95 \times 39 = 38.05$ — shaping 전의 $19$와 $18.05$에 $20$을 더한 값이라 이동이 여전히 $0.95$ 차이로 이긴다. 이동이 영원히 대기했다면 모았을 보너스 전부 $1/(1 - 0.95) = 20$을 받는다. (e) $A^*(A,\text{대기}) = 18.05 - 19 = -0.95$. 기울임은 기준 정책에 $e^{A/\beta}$를 곱하므로 $\tfrac23 e^{0}$ 대 $\tfrac13 e^{-1.9} = \tfrac13 \times 0.1496$이고, $\pi(\text{이동}\mid A) = 0.6667/(0.6667 + 0.0499) = 0.930$, 그 가치는 $V(A) = 0.930 \times 19/(1 - 0.95 \times 0.070) = 18.93$이다. BC의 $18.54$와 최적값 $19$ 사이다. KL 항이 조작자의 망설임을 일부 남기고, $\beta \to 0$이면 그것마저 없어진다.
> 3. 써 놓은 보상에서 파인튜닝한 정책은 영원히 대기하기를 배웠고 $1/(1 - 0.95) = 20$을 받는다. BC는 셋 중 한 번의 대기에서만 보너스를 챙겨 $V = [\tfrac23(19) + \tfrac13(1)]/(1 - 0.95/3) = 19.02$다. 곧바로 이동하는 정직한 최적해조차 이 보상으로는 $19$밖에 못 받는다. 과제 — 버킷 채우기 — 에서는 파인튜닝한 정책이 $0$, BC가 $18.54$다. 표가 보여 준 것은 최적화기가 보상 속의 루프를 찾아냈다는 것이지 로봇이 더 잘 일한다는 것이 아니다. 요구할 것: 모든 가중치를 담은 보상 표(움직이지 않는 데 값을 쳐 주는 항이 첫 번째 용의자다), 리턴과 따로 보고한 과제 지표, 파인튜닝이 BC 정책에 KL로 닻을 내렸는지와 그 $\beta$, 그리고 베이스라인이 같은 보상·관측·커리큘럼으로 학습되었는지.

### 출처 · Sources

- R. S. Sutton, A. G. Barto, *Reinforcement Learning: An Introduction*, 2판, MIT Press, 2018(위 링크에서 무료) — 보상 신호 설계를 다룬 17.4절이 이 책에서 §2에 가장 가까운 부분이다.
- §1: S. Ross, G. J. Gordon, J. A. Bagnell, "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning," AISTATS 2011 — DAgger와 $O(\epsilon T^2)$ 대 $O(\epsilon T)$ 한계. 2024~26년 결과: HIL-SERL(*Science Robotics*, 2025; [[01-canonical-papers/notes/7-robotics/hil-serl|HIL-SERL 노트]]), ConRFT [arXiv:2502.05450](https://arxiv.org/abs/2502.05450), RECAP [arXiv:2511.14759](https://arxiv.org/abs/2511.14759), "Data Scaling Laws in Imitation Learning for Robotic Manipulation," [arXiv:2410.18647](https://arxiv.org/abs/2410.18647)(ICLR 2025).
- §2: A. Y. Ng, D. Harada, S. Russell, "Policy invariance under reward transformations: Theory and application to reward shaping," ICML 1999 — 포텐셜 기반 shaping 정리.
- §3: T. P. Lillicrap 외, "Continuous control with deep reinforcement learning," ICLR 2016 — DDPG와 $\theta_{\text{OU}} = 0.15$인 Ornstein–Uhlenbeck 노이즈. T. Haarnoja 외, "Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor," ICML 2018 — 최대 엔트로피 목적함수([[01-canonical-papers/notes/1-foundations/sac|SAC 노트]]).
- §6: Ratliff, Bagnell & Zinkevich, "Maximum Margin Planning" (ICML 2006); Ziebart, Maas, Bagnell & Dey, "Maximum Entropy Inverse Reinforcement Learning" (AAAI 2008); Ho & Ermon, "Generative Adversarial Imitation Learning" (NeurIPS 2016); Bradley & Terry, "Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons" (*Biometrika*, 1952); Basu, Yang, Hungerman, Singhal & Dragan, "Do You Want Your Autonomous Car To Drive Like You?" (HRI 2017); Christiano 외, "Deep Reinforcement Learning from Human Preferences" (NeurIPS 2017); Sadigh 외, "Active Preference-Based Learning of Reward Functions" (RSS 2017); Ouyang 외, "Training language models to follow instructions with human feedback" (NeurIPS 2022; [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT 노트]]); Rafailov 외, "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (NeurIPS 2023).
- 이 페이지의 수치 예제는 버킷의 것까지 모두 명시된 숫자로부터 여기서 직접 계산한 것이며 어느 출처에서 인용한 것이 아니다. 믿지 말고 다시 계산하라.
- Shao, Z. et al. "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." arXiv:2402.03300, 2024 — GRPO, §4.1.
- DeepSeek-AI. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." *Nature* 645:633–638, 2025.
- Muennighoff, N. et al. "s1: Simple test-time scaling." arXiv:2501.19393, 2025.
- Tan, S. et al. "Interactive Post-Training for Vision-Language-Action Models"(RIPT-VLA). arXiv:2505.17016, 2025; Lu, G. et al. "VLA-RL: Towards Masterful and General Robotic Manipulation with Scalable Reinforcement Learning." arXiv:2505.18719, 2025.
