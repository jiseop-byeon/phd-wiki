---
title: 19. Semantic & Language-Driven Navigation
tags: [robotics, navigation, vlm]
study-depth: Working
wiki-support: Working
depth-goal: "State the ObjectNav and VLN task definitions and metrics, explain what the nav-graph formulation assumes and why continuous (VLN-CE) results are not comparable to it, and say what happened to the field's benchmarks."
mastery-when: "Raise to Mastery only if language-grounded navigation becomes the contribution."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to read this literature accurately, and to know why its leaderboards
> stopped being the thing to climb.
> **Working** — 이 문헌을 정확히 읽고, 그 리더보드가 왜 더 이상 오를 대상이 아니게 되었는지
> 알 만큼.

> [!note] Prerequisites · 선수 지식
> You need CLIP-style vision-language grounding ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), frontier-based exploration and costmaps ([[04-robotics/planning-decision-making|4. Planning]]), and what a VLA is ([[01-canonical-papers/notes/4-vla/rt-2|RT-2]]).
> CLIP식 시각-언어 접지([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), 프런티어 기반 탐색과 costmap([[04-robotics/planning-decision-making|4. 계획]]), 그리고 VLA가 무엇인지([[01-canonical-papers/notes/4-vla/rt-2|RT-2]])가 필요하다.

## English

*Group I. Stands on [[04-robotics/planning-decision-making|4. Planning]] and, in practice, on the VLM notes.
When the goal is a word rather than a coordinate, the hard problem stops being path-finding and becomes deciding where to look.*

> [!note] First pass · 처음이라면
> Read the running object and the worked case below — one map, one instruction, and the two numbers this literature reports — then §1, the shift a classically trained reader has to make, then §2, because most confusion here is people arguing about ObjectNav without agreeing on its definition, then §8. §3 to §7 are the history; read it once the definitions are solid.

### Running object: the map G4

No plant from [[02-foundations/lab-plants|0.6]] fits a page whose object is a *map*, so this page freezes its own and never changes it. **G4** is a 4×4 grid of 1 m cells, cell centres at integer coordinates $(c, r)$ with $c$ the column left to right and $r$ the row bottom to top, both running 0 to 3. Motion is four-connected, one metre per step, and there are no diagonals.

| | $c=0$ | $c=1$ | $c=2$ | $c=3$ |
|---|---|---|---|---|
| $r=3$ | **sofa** | · | · | **plant** |
| $r=2$ | · | · | · | · |
| $r=1$ | · | · | · | **tv** |
| $r=0$ | **start** | · | · | · |

Three labelled objects fill three cells, which the agent therefore cannot enter: **sofa** at $(0,3)$, **tv** at $(3,1)$, **plant** at $(3,3)$. The agent starts at $(0,0)$. Three **wall segments** sit on edges between cells and block motion across them, nothing more:

- **A** between $(0,1)$ and $(0,2)$
- **B** between $(1,1)$ and $(1,2)$
- **C** between $(2,1)$ and $(3,1)$

A and B are a partition across the left of the room; C is the short wall the television is mounted on. The instruction is fixed too: **"go to the television."** The agent carries an object-centric map of the kind §7 describes, so the three labels and their cells are given; what it has to do is ground the instruction onto one of them and then stop somewhere legal.

Finally, the agent's open-vocabulary detector has already scored each map node against the goal phrase. These three cosine similarities are frozen page-local numbers, not measurements from any system: $s_{\text{sofa}} = 0.11$, $s_{\text{tv}} = 0.34$, $s_{\text{plant}} = 0.09$.

*Scope: this page teaches the two definitions this literature is written in — the ObjectNav success criterion and SPL — and how a grounding score and a map geometry combine into a stop decision. It does not teach how the frontier is chosen or the local controller drives ([[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]]), how the vision-language features are trained ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), or outdoor traversability ([[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]).*

### The picture: G4, its legal stops, and one path

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="Map G4 for the instruction go to the television: a 4 by 4 grid with sofa, tv and plant cells shaded, walls A, B and C drawn on cell edges, legal stops (3,0) and (3,2) circled, (2,1) crossed, the shortest path dashed and episode 3's walk solid">
  <defs><marker id="arG4e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="40" y="18" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <rect x="250" y="158" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <rect x="250" y="18" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <line x1="40" y1="18" x2="320" y2="18" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="18" x2="40" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="88" x2="320" y2="88" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="110" y1="18" x2="110" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="158" x2="320" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="180" y1="18" x2="180" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="228" x2="320" y2="228" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="250" y1="18" x2="250" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="298" x2="320" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="320" y1="18" x2="320" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <text x="44" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(0,0)</text>
  <text x="44" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(0,1)</text>
  <text x="44" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(0,2)</text>
  <text x="44" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(0,3)</text>
  <text x="114" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(1,0)</text>
  <text x="114" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(1,1)</text>
  <text x="114" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(1,2)</text>
  <text x="114" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(1,3)</text>
  <text x="184" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(2,0)</text>
  <text x="184" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(2,1)</text>
  <text x="184" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(2,2)</text>
  <text x="184" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(2,3)</text>
  <text x="254" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(3,0)</text>
  <text x="254" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(3,1)</text>
  <text x="254" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(3,2)</text>
  <text x="254" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(3,3)</text>
  <text x="75" y="58" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">sofa</text>
  <text x="285" y="198" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">tv</text>
  <text x="285" y="58" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">plant</text>
  <text x="75" y="290" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">start</text>
  <circle cx="75" cy="263" r="3.2" fill="currentColor" fill-opacity="1"/>
  <line x1="41.5" y1="158" x2="108.5" y2="158" stroke="currentColor" stroke-width="6"/>
  <text x="75" y="151" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">A</text>
  <line x1="111.5" y1="158" x2="178.5" y2="158" stroke="currentColor" stroke-width="6"/>
  <text x="145" y="151" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">B</text>
  <line x1="250" y1="159.5" x2="250" y2="226.5" stroke="currentColor" stroke-width="6"/>
  <text x="243" y="174.5" font-size="12" fill="currentColor" text-anchor="end" font-weight="700">C</text>
  <circle cx="285" cy="263" r="19" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="285" cy="123" r="19" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="202" y1="180" x2="228" y2="206" stroke="currentColor" stroke-width="2.2"/>
  <line x1="202" y1="206" x2="228" y2="180" stroke="currentColor" stroke-width="2.2"/>
  <line x1="87" y1="269" x2="133" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4e)"/>
  <line x1="157" y1="269" x2="203" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4e)"/>
  <line x1="227" y1="269" x2="263" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4e)"/>
  <line x1="69" y1="251" x2="69" y2="205" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4e)"/>
  <line x1="81" y1="193" x2="127" y2="193" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4e)"/>
  <line x1="151" y1="193" x2="188" y2="193" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4e)"/>
  <circle cx="354" cy="36" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="372" y="40" font-size="11" fill="currentColor">legal stop: next to the tv,</text>
  <text x="372" y="54" font-size="11" fill="currentColor">no wall on the shared edge</text>
  <line x1="348" y1="72" x2="360" y2="84" stroke="currentColor" stroke-width="2"/>
  <line x1="348" y1="84" x2="360" y2="72" stroke="currentColor" stroke-width="2"/>
  <text x="372" y="82" font-size="11" fill="currentColor">1.0 m from the tv, wall C</text>
  <text x="372" y="96" font-size="11" fill="currentColor">between: not a legal stop</text>
  <line x1="344" y1="120" x2="363" y2="120" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4e)"/>
  <text x="372" y="124" font-size="11" fill="currentColor">shortest path to the nearest</text>
  <text x="372" y="138" font-size="11" fill="currentColor">legal stop (3,0): ℓ = 3 m</text>
  <line x1="344" y1="162" x2="363" y2="162" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4e)"/>
  <text x="372" y="166" font-size="11" fill="currentColor">walked, episode 3: p = 3 m,</text>
  <text x="372" y="180" font-size="11" fill="currentColor">stops at (2,1): S = 0</text>
  <line x1="344" y1="204" x2="364" y2="204" stroke="currentColor" stroke-width="6"/>
  <text x="372" y="208" font-size="11" fill="currentColor">wall: lives on an edge</text>
  <rect x="345" y="225" width="18" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <text x="372" y="238" font-size="11" fill="currentColor">object: fills a cell</text>
  <text x="12" y="324" font-size="11" fill="currentColor">(3,0) and (2,1) are both 3 steps from the start and 1.0 m from the tv;</text>
  <text x="12" y="339" font-size="11" fill="currentColor">only (3,0) can see it. The grounding g(tv) = 0.846 was right; the stop was not.</text>
</svg>

The worked case on G4, instruction "go to the television": the sofa, tv and plant fill their cells, walls **A**, **B** and **C** lie on cell edges, the legal stops $(3,0)$ and $(3,2)$ are circled, and $(2,1)$, $1.0$ m from the tv but behind wall **C**, is crossed. The dashed path is the shortest route to the nearest legal stop, $\ell = 3$ m; the solid one is episode 3's walk, also $p = 3$ m, which stops at $(2,1)$ and scores $S = 0$. Both cells are three steps from the start and $1.0$ m from the tv, but only $(3,0)$ can see it: the grounding $g(\text{tv}) = 0.846$ was right, and the stop was not.

### Worked case: one instruction, one map, two numbers

**Step 1 — the grounding score.**

> [!info] Definition · 정의 — grounding score
> **What kind of thing it is.** A *probability distribution over a closed candidate set*: one number per candidate object, non-negative, summing to 1 across exactly the candidates considered. It is not a similarity, and it is not a confidence that the goal exists.
>
> **Its defining conditions.** Three. (i) The candidate set is **closed and declared** — the scores are normalised over exactly those objects, so an object outside the set cannot be chosen and its absence is invisible in the numbers. (ii) The map is **order-preserving** in the raw scores: the highest similarity is always the highest grounding score. (iii) A **temperature** $T > 0$ sets the sharpness and is a design choice, not something the vision-language model reports.
>
> $$g(o) = \frac{\exp\big(s_o / T\big)}{\sum_{o' \in \mathcal{O}} \exp\big(s_{o'} / T\big)}$$
>
> $\mathcal{O}$ is the declared candidate set, $o$ one object in it, $s_o$ the raw similarity between the instruction's goal phrase and that object's label, and $T$ the temperature: small $T$ sharpens toward a hard argmax, large $T$ flattens toward the uniform distribution $1/|\mathcal{O}|$.
>
> **Example.** The three objects of G4 at $T = 0.10$, worked below: $g(\text{tv}) = 0.846$.
>
> **Non-examples.** The raw cosine $s_{\text{tv}} = 0.34$ is not a grounding score — nothing normalises it, so it cannot be compared across instructions or across maps. Neither is a score normalised over only the objects detected *so far* in an episode: that is a grounding score over a different $\mathcal{O}$, which is why the same instruction can report a different confidence at two points in one run without the model having changed its mind.
>
> **Why it matters.** The number a paper prints as "the model understood the instruction" is a function of two design choices, the candidate set and the temperature, and only the *ranking* survives both. Whenever a navigation failure is blamed on language, check the ranking first — if the ranking is right, the failure is somewhere else, which is exactly what happens below.

Exponentiate each frozen similarity at $T = 0.10$, because the exponent $s_o/T$ is what the softmax acts on:

$$e^{0.11/0.10} = 3.004, \qquad e^{0.34/0.10} = 29.964, \qquad e^{0.09/0.10} = 2.460$$

The normaliser is $Z = 3.004 + 29.964 + 2.460 = 35.428$, so

$$g(\text{sofa}) = 0.085, \qquad g(\text{tv}) = 0.846, \qquad g(\text{plant}) = 0.069$$

The instruction grounds on the television at 0.846. That is the language half of the task, and it is finished.

**Step 2 — the legal stops, from the geometry.** The success criterion of §2 has two parts, and on G4 they read: the agent must stop within 1.0 m of the goal — a four-adjacent cell — **and** the object must be viewable from there, which on this map means no wall segment on the shared edge. The television at $(3,1)$ has three four-adjacent cells: $(3,0)$, $(3,2)$ and $(2,1)$. Wall **C** sits between $(2,1)$ and $(3,1)$, so $(2,1)$ fails the second part. The legal stops are $(3,0)$ and $(3,2)$.

Breadth-first from the start over the free cells, respecting the three walls, gives the geodesic distance to every cell: $(3,0)$ is 3 steps, $(3,2)$ is 5, and $(2,1)$ is also 3. So the shortest path length to the goal, measured to the nearest *legal* stop, is $\ell = 3$ m.

**Step 3 — SPL over three episodes on this map.**

> [!info] Definition · 정의 — SPL (Success weighted by normalised inverse Path Length)
> **What kind of thing it is.** A scalar in $[0, 1]$ reported for a whole evaluation set: the mean, over episodes, of a per-episode term that is zero on failure and a path-efficiency ratio on success.
>
> **Its defining conditions.** Four, and each is a place the number is misreported. (i) **Every episode contributes**, and a failed one contributes exactly 0 — failures are not dropped. (ii) The term is **success-gated**, so an efficient failure earns nothing and a wasteful success earns something. (iii) $\ell_i$ is the **geodesic** shortest path from the agent's start to the nearest position that would satisfy the success criterion for the goal — not straight-line distance, and not measured from where the agent ended up. (iv) The $\max(p_i, \ell_i)$ caps each term at 1, so an episode cannot be rewarded for appearing to beat the shortest path.
>
> $$\text{SPL} = \frac{1}{N}\sum_{i=1}^{N} S_i \, \frac{\ell_i}{\max(p_i, \ell_i)}$$
>
> $N$ is the number of episodes, $S_i \in \{0, 1\}$ is whether episode $i$ satisfied the full success criterion, $\ell_i$ is its shortest-path length and $p_i$ the length the agent actually walked.
>
> **Example.** The three G4 episodes below: 0.519, next to a success rate of 0.667.
>
> **Non-examples.** The mean of $\ell_i / p_i$ over the *successful* episodes only is not SPL — on the episodes below it is $(1.000 + 0.556)/2 = 0.778$, a path-efficiency figure for the runs that worked, which says nothing about how often they work. Nor is "success rate × mean efficiency" SPL: it coincides only when efficiency is uncorrelated with success, and the whole interest of the metric is that it usually is not.
>
> **Why it matters.** A single SPL is compatible with a wandering near-perfect navigator and with a straight-line mediocre one — the §2 box works that out — so SPL is uninterpretable without the success rate beside it, and the two together are what this literature reports.

Three episodes on G4, all starting at $(0,0)$:

| Episode | Goal | Stop cell | $S_i$ | $\ell_i$ | $p_i$ | Term |
|---|---|---|---|---:|---:|---|
| 1 | tv | $(3,0)$ | yes | 3 | 3 | $1 \times 3/3 = 1.000$ |
| 2 | plant | $(2,3)$ | yes | 5 | 9 | $1 \times 5/9 = 0.556$ |
| 3 | tv | $(2,1)$ | **no** | 3 | 3 | $0$ |

Episode 2 is the agent checking the wrong room first: $(0,0) \to (0,1) \to (1,1) \to (2,1) \to (2,2) \to (1,2) \to (1,3) \to (1,2) \to (2,2) \to (2,3)$, nine steps against a five-step optimum, ending on a legal plant stop. Episode 3 is the failure this page exists to name. Therefore

$$\text{SPL} = \frac{1.000 + 0.556 + 0}{3} = 0.519, \qquad \text{success rate} = \frac{2}{3} = 0.667$$

**Step 4 — the failure where the language matched and the geometry did not.** In episode 3 the agent grounded the instruction on the television with confidence 0.846 and then walked until its distance to the television node dropped to 1.0 m. Two cells meet that test three steps from the start, $(3,0)$ and $(2,1)$, so nothing in the planner preferred either; the agent came round from the west and stopped at $(2,1)$. Nothing about the language went wrong — the ranking is tv, sofa, plant and the margin is wide. What went wrong is that the stopping rule tested *distance to the object* and never tested *visibility of the object*, and wall **C** stands between $(2,1)$ and the television. A tie the planner was indifferent to became the whole difference between 1 and 0 in the metric, and the agent is one metre from a screen it cannot see.

Price the visibility clause exactly. Score the same three runs on distance alone, dropping the second half of the criterion, and episode 3 becomes a success:

$$\text{SPL}_{\text{distance only}} = \frac{1.000 + 0.556 + 1.000}{3} = 0.852, \qquad \text{success rate} = \frac{3}{3} = 1.000$$

The clause costs 0.333 of SPL and 0.333 of success rate on this three-episode set — a third of the score, produced entirely by one wall. That is the arithmetic behind the sentence in §2 that an agent could otherwise succeed standing on the far side of a wall, and it is why "we dropped the oracle-visibility check for efficiency" is never a small change to an evaluation.

### 1. The shift a classical reader has to make

Classically the goal is a **pose in a known metric space**, and planning is finding a path to
it. Here the goal is a **word** — "toilet", or "go past the kitchen and turn left at the
plant" — its location is unknown, and the hard problem is not path-finding at all. It is
**deciding where to look.**

That converts exploration from a coverage problem into an inference problem over
object-and-room co-occurrence, and it is why a vision-language model turns out to be a
navigation component.

### 2. ObjectNav — the definition, stated precisely

The agent spawns at a random pose in a **previously unseen** environment, is given only a
goal object *category*, and must navigate to **any instance** and signal completion.
Observations are RGB-D plus a noiseless GPS+Compass; no map, no scene graph, no ground-truth
semantics.

The success criterion is two-part, and the second half is what makes it a real task:

> On emitting `STOP`, the agent must be **within 1.0 m** of an instance of the target
> category **and** the object must be viewable by an oracle from that stopping position by
> turning or looking up and down.

Without the visibility clause an agent could succeed standing on the far side of a wall
0.9 m from the goal. Metrics are Success Rate and **SPL**, with the shortest path measured
to the instance nearest the agent's *start*.

> [!warning] Both defining documents are unrefereed
> SPL was introduced in *On Evaluation of Embodied Navigation Agents* (2018), which
> describes itself as a working-group report. The task definition comes from
> *ObjectNav Revisited* (2020). **Neither was ever peer-reviewed**, and between them they
> define the metrics the entire literature reports. That is worth saying out loud when you
> cite them.

> [!example] Worked example · 계산 예제
> **What an SPL of 0.47 actually says.** Success weighted by Path Length (Anderson et al. 2018)
> is $\text{SPL} = \frac{1}{N}\sum_i S_i \frac{\ell_i}{\max(p_i, \ell_i)}$, where $S_i$ is
> success, $\ell_i$ the shortest path and $p_i$ the path actually walked. Three episodes:
>
> | Episode | Success | Shortest $\ell$ | Walked $p$ | Term |
> |---|---|---|---|---|
> | 1 | yes | 10 m | 10 m | $1 \times 10/10 = 1.00$ |
> | 2 | yes | 10 m | 25 m | $1 \times 10/25 = 0.40$ |
> | 3 | no | 10 m | 8 m | $0$ |
>
> $\text{SPL} = (1.00 + 0.40 + 0)/3 = \mathbf{0.47}$, while the success rate is $2/3 = 0.67$.
>
> **The reading this gives you.** An agent that succeeds *every single time* but always walks
> twice the shortest path scores $1 \times 10/20 = 0.50$ — so 0.47 is compatible with a
> near-perfect navigator that wanders, and equally with a 47% navigator that walks straight
> lines. SPL alone cannot tell you which. This is why an SPL reported without its success rate
> is uninterpretable, and why the field now insists on both. When a paper shows only SPL and
> claims an efficiency improvement, check whether success moved at all.

### 3. The method arc, in three moves

**Move 1 — modular semantic mapping.** Active Neural SLAM established the skeleton: learned
SLAM, a global policy choosing long-term goals, an analytical planner, and a local policy.
Its thesis is that hierarchy plus classical planning beats end-to-end RL on sample
complexity. **SemExp** put a semantic map in that skeleton and let a learned global policy
pick long-term exploration goals on it. It won the 2020 challenge and its architecture is
still the backbone.

**Move 2 — replace the learned scorer with a pretrained VLM, and train nothing ObjectNav-specific.**
**VLFM** builds an occupancy map, extracts frontiers, and scores each frontier by
**vision-language similarity to the goal text**, choosing where to explore next. No ObjectNav
training data at all (it still follows waypoints with a PointNav policy trained for 2.5B steps on HM3D), and it deployed on a real Spot. **ESC** does the same job with LLM
commonsense — object-and-room co-occurrence — compiled into soft logic predicates over a
frontier scorer. A soft logic predicate is a rule such as "a frontier near a sofa is likely
near the TV" whose truth value lies between 0 and 1 instead of being true or false, so the
scorer can pick the frontier that best satisfies all the weighted rules at once. And **CoWs** established that a zero-shot pipeline "matches the navigation
efficiency of a state-of-the-art ZSON (Zero-Shot Object-goal Navigation) method trained for 500M steps" — parity on SPL, not on
success, on Habitat MP3D (SPL 4.9 vs 4.8, success 9.2 vs 15.3), where the paper says its own comparison "indicates that there can be benefits to
in-domain learning over CoW baselines". On RoboTHOR the same CoW beats the prior zero-shot model by 15.6 points in success. It is also weak at exploiting complex language.

**Move 3 — throw the modular apparatus away.** See §5.

> [!note] Cite CoWs by its real title
> The paper is *"CoWs on Pasture: Baselines and Benchmarks for Language-Driven Zero-Shot
> Object Navigation."* "CLIP on Wheels" is the *method* name. Secondary sources routinely
> miscite this.

### 4. The critique that reframes everything

Gervet et al. tested classical, modular-learning and end-to-end approaches on real robots
**across six real homes**:

| Approach | Result |
|---|---|
| **Classical** | 78% in simulation → 80% in the real world |
| **Modular learning** | 81% in simulation → **90% in the real world** |
| **End-to-end learning** | **77% in simulation → 23% in the real world** |

The load-bearing conclusion is not the gap itself but its explanation: simulators fail as
evaluation benchmarks for **two** reasons — the visual sim-to-real gap, and **misaligned
error patterns**. All three families sat near 80% in simulation, so simulation could not tell them apart, and because simulation and reality fail in *different ways* it cannot tell you which bottleneck to fix. Among end-to-end design variants, **the choices that raised simulation scores lowered real-world scores.** A leaderboard can be climbed without the thing it
measures improving.

### 5. VLN, and the paper that admitted the benchmark was cheating

**R2R** created the task and the Matterport3D Simulator: follow a natural-language route
instruction through a real building. But R2R is **discrete** — the agent teleports between
nodes of a pre-built navigation graph. **RxR** added multilingual instructions and
word-level temporal alignment to poses (each spoken word is timestamped against where the
annotator was on the path, which tells a model and an evaluator which stretch of the path each
phrase describes), and corrected R2R's path bias (R2R paths are all
shortest paths, which lets an agent cheat).

**VLN-CE is the most consequential paper in this literature.** It ports R2R into Habitat with
**low-level continuous actions**, removing three assumptions at once — known topology, oracle
navigation, perfect localization — and performance drops dramatically. The conclusion the
field accepted without rebuttal: **prior nav-graph results were inflated by their own
simplifying assumptions.**

The empirical companion is Anderson et al.'s sim-to-real study: **55.9% in simulation →
46.8% real with a pre-built map → 22.5% real with no prior mapping.**

The transformer era — **HAMT** (a hierarchical [[01-canonical-papers/notes/1-foundations/vit|ViT]], or Vision Transformer, an image model that splits each view into patches and processes them as a token sequence, over the full history of past panoramas,
gaining most on long trajectories) and **DUET** (a topological map built on the fly,
combining coarse global planning including backtracking with fine local encoding) — is the
high-water mark of the discrete paradigm, and worth reading as such.

Then **NaVid** supplied a different branch: a video VLM taking **monocular RGB video only — no maps, no
odometry, no depth** — and emitting actions directly. It threw away the entire modular
apparatus HAMT and DUET depended on. Several later video-VLA systems build on this idea,
while graph-based and modular VLN research continues in parallel.

> [!important] Say it precisely
> **The nav-graph action space is not the only modern formulation, and R2R is not simply
> obsolete.** VLN-CE ports R2R and RxR into Habitat, while discrete graph-based benchmarks
> and continuous embodied variants coexist. State which action space, localization access
> and navigation oracle a result uses before comparing numbers.

### 6. The two threads merged, and the benchmarks dissolved

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="two separate navigation threads from 2018 converging into one video-VLA by 2025, while the challenges end">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="34" y1="212" x2="528" y2="212"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="60" y1="212" x2="60" y2="218"/><line x1="180" y1="212" x2="180" y2="218"/><line x1="300" y1="212" x2="300" y2="218"/><line x1="380" y1="212" x2="380" y2="218"/><line x1="460" y1="212" x2="460" y2="218"/>
  </g>
  <g fill="currentColor">
    <rect x="34" y="52" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="34" y="112" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="392" y="76" width="136" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="34" y="52" width="250" height="32" rx="3"/><rect x="34" y="112" width="250" height="32" rx="3"/><rect x="392" y="76" width="136" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.8" marker-end="url(#arS)">
    <path d="M 290 68 L 340 68 L 340 92 L 386 92"/>
    <path d="M 290 128 L 340 128 L 340 106 L 386 106"/>
  </g>
  <defs><marker id="arS" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="72">ObjectNav &#8212; find a named object</text>
    <text x="46" y="132">VLN &#8212; follow a route instruction</text>
    <text x="460" y="95" text-anchor="middle" font-size="11">one video-VLA</text>
    <text x="460" y="110" text-anchor="middle" font-size="9">nav + object search + EQA + following</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="60" y="230" text-anchor="middle">2018</text><text x="180" y="230" text-anchor="middle">2020</text><text x="300" y="230" text-anchor="middle">2023</text><text x="380" y="230" text-anchor="middle">2024</text><text x="460" y="230" text-anchor="middle">2025</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" stroke-dasharray="4 3">
    <line x1="300" y1="160" x2="300" y2="206"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="306" y="170">Oct 2023: Habitat Challenge archived, read-only</text>
    <text x="306" y="184">CVPR 2026: zero navigation challenges</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="34" y="250">Navigation was not solved. It was absorbed &#8212; upward into VLAs, sideways into mobile manipulation.</text>
  </g>
</svg>

**Uni-NaVid** is the merge: one video-VLA trained on 3.6M samples spanning **VLN, object
search, embodied question answering and person-following**, reporting state of the art across
all of them at 5 Hz. In 2020 those were separate communities with separate simulators and
separate challenges.

Simultaneously the institutional scaffolding came down. The Habitat Challenge repository was
**archived read-only in October 2023** and the 2023 edition was the last. The CVPR 2025
Embodied AI Workshop ran four challenges and **none was ObjectNav**; CVPR 2026 ran three and
**all three were manipulation**.

Where the energy went is measurable: **open-vocabulary mobile manipulation**, where HomeRobot
reports ~20% real-world success and the challenge post-mortem records a baseline of **0.8%**
rising to a winning **10.8%** — a 13× improvement that still leaves the task ~90% unsolved.
That is a leaderboard worth climbing; a saturated six-category ObjectNav was not.

The successors that did appear are open-vocabulary by construction: **HM3D-OVON** (379
categories, free-form language goals) and **GOAT-Bench** (goals given as a category, a
description, *or* an image, over long horizons with memory).

### 7. The other half: maps you can query with language

Running alongside, and now more consequential than the ObjectNav leaderboard:

- **VLMaps** fuses vision-language features into a 3D reconstruction the robot builds itself,
  enabling **spatial** language goals — "between the sofa and the TV" — via LLM code
  generation, and emitting robot-specific obstacle maps shareable across embodiments.
- **ConceptFusion**'s distinctive claim is *multimodal query*: language, image, audio, and a
  click all index the same map.
- **ConceptGraphs** replaced dense feature fields with an **object-centric graph** — multi-view
  fusion into nodes, LLM-inferred edges. Cheaper and composable, which is why it became the
  default backbone.
- **Clio** asks the better question: granularity is not a fixed threshold but is **derived
  from the task list via an [[02-foundations/information-theory|Information Bottleneck]]**, which
  compresses a representation while keeping only what predicts a target, here the tasks. The same scene needs a coarse map for
  navigation and a fine one for manipulation, and the task should decide.
- **Hydra** is the real-time systems foundation the rest assumes, with **Khronos** extending
  it to spatio-temporal mapping in dynamic environments.

Two visible 2025–2026 directions are broader use of **Gaussian splatting** as a semantic
substrate alongside NeRF-style fields, and object-centric **scene graphs** as queryable
interfaces over several geometric substrates. Neither representation has universally
displaced the others; compare update cost, geometry quality, dynamics and query needs.

> [!note] One map, or many experiences? · 지도 하나인가, 여러 경험인가
> Every representation above produces one coherent estimate of where things currently are. Churchill and Newman's experience-based navigation (IJRR 2013) took the opposite route for places whose appearance changes. Rather than correcting a single model toward the present, a vehicle driving the same workspace over a three-month period — across times of day, weather and lighting — accumulated **distinct visual experiences**, each capturing one visual mode. Localisation then means matching the live images against those previous experiences; failing to match enough of them is itself the signal to lay the current sequence down as a new experience. Over 37 km and more than 136,000 frames, the number of experiences needed tended to a constant rather than growing without bound.
>
> Hold that next to the maps above, because it changes what "the map is wrong" means. In a single-model map a moved chair or a changed light is an error to be corrected away. In an experience-based representation it is a mode to be kept and recognised the next time it appears. The difference only shows in deployments long enough for the same place to look several ways.

> [!important] This is where the wiki's perception notes were heading
> [[01-canonical-papers/notes/2-computer-vision/sam|SAM]],
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]],
> [[01-canonical-papers/notes/2-computer-vision/dino|DINO]],
> [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]]
> and [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]] are the *ingredients*. This
> section is what gets built out of them — and the map is where navigation and manipulation
> meet before any controller does.

### 8. Reading a paper in this area

| Question | What a vague answer hides |
|---|---|
| Nav-graph or continuous? | Nav-graph numbers are not comparable to VLN-CE numbers |
| Simulation or real robot? | Sim ranking does not preserve real ranking |
| What data was used: ObjectNav-specific, other embodied data, or none? | Strong zero-shot modular methods may use no ObjectNav-specific training; end-to-end video/VLA methods can use large embodied datasets |
| Which HM3D/MP3D split, and how many categories? | 6-category ObjectNav is saturated; 379-category is not |
| Is the language actually load-bearing? | Rephrase-sensitivity is the standard failure |
| SPL or bare success rate? | Success alone rewards inefficient wandering |

One more question is worth asking of any 2025–2026 paper advertising self-correction or
reasoning: *where does the extra capability live?* A model post-trained on its own recovery
data has learned to act correctly in situations resembling failures seen during training. A
system that estimates its uncertainty during a run and then spends more computation is doing
something different. Both are called self-correction, so read for the mechanism
([[03-deep-learning/lineage|Lineage — Robot learning]]).

### After reading

- [ ] State the ObjectNav success criterion, including the visibility clause, and why it exists.
- [ ] Explain what VLN-CE removed and what it showed.
- [ ] Give the modular-versus-end-to-end real-world numbers and the reason behind them.
- [ ] Say what happened to the Habitat Challenge and where the field went.
- [ ] Name the map representation that became the default backbone, and Clio's better question.

> [!tip] Going deeper · 더 깊이
> This field's canon is not a book but two definition papers and a critique, and reading them in order is what keeps you out of its recurring arguments. Anderson et al. (2018) first, for SPL and the evaluation vocabulary — note it is unrefereed and cite it as such. Then "ObjectNav Revisited" (2020), which exists because the first definition was not tight enough. Then the critique in §4, which is what makes the benchmark history in §5–§6 legible. Habitat's papers are infrastructure documentation; read the one matching the version a paper used, not all of them.

### Self-check

1. Why does the ObjectNav success criterion have two parts?
2. A 2026 paper reports 68% success on nav-graph R2R. What do you conclude?
3. A method scores well on a simulated navigation benchmark. What does Gervet et al. say you
   may *not* infer?
4. ObjectNav challenges stopped running. Does that mean object-goal navigation is solved?
5. You want a map that supports both navigating to a room and grasping something in it. What
   does the current literature suggest?

> [!tip]- Answers
> 1. Because proximity alone is not the task. Without the oracle-visibility clause an agent could stop 0.9 m from the target with a wall between them and be scored correct — which would reward reaching a *coordinate* rather than finding an *object*. The two-part criterion is what makes ObjectNav a perception problem rather than a metric-navigation problem in disguise.
> 2. That it is not directly comparable to continuous embodied results. A pre-built graph can provide known topology, discrete viewpoints and localization assumptions absent from VLN-CE. But graph-based VLN remains an active formulation; compare results only within a stated action space and oracle-access protocol.
> 3. That its real-world ranking will follow. Their finding is not merely that performance drops but that **simulation and reality fail in different ways**, so simulation cannot separate methods or show what to fix. All three families sat near 80% in simulation (classical 78, modular 81, end-to-end 77) and spread to 80 / 90 / 23 in the real world; among end-to-end variants, real-world performance was inversely related to simulation performance. Sim results are evidence about sim.
> 4. No. Ending a challenge or saturating one configuration is not evidence that the underlying task is solved. Open-vocabulary and lifelong variants (HM3D-OVON, GOAT-Bench), continuous control, sim-to-real transfer and mobile manipulation test different unresolved capabilities.
> 5. That granularity should be **task-derived rather than fixed** — Clio's Information Bottleneck formulation exists precisely because navigation wants a coarse map and manipulation wants a fine one of the same scene. Architecturally, build an object-centric scene graph (the ConceptGraphs lineage) as the queryable interface, over whatever geometric substrate you use, and let the task list set the level of detail.

**Worked: the three readings the homework asks.** The ranking, not the confidence, is what survives the temperature — a grounding score that falls from 0.846 to 0.566 has not got worse, so a wide-margin grounding is never what failed. A stop one metre from the goal with a wall between is a coordinate, not an object, and on G4 the visibility clause was worth a third of both scores. And SPL without its success rate tells two different stories at the same number: 0.50 is perfect paths failing half the time, and it is also every episode succeeding at twice the shortest path.

### Problem set · 과제

Tier B. Hand derivation on **G4**, using only this page and its prerequisites. Same grid, same three objects, same start $(0,0)$, same instruction "go to the television", same frozen similarities $(0.11, 0.34, 0.09)$. Two things change: the television is remounted, so wall **C** between $(2,1)$ and $(3,1)$ is **removed** and a new wall **E** is added between $(3,1)$ and $(3,2)$; and the grounding temperature is raised from $T = 0.10$ to $T = 0.25$.

1. **Draw.** The picture above, with walls **A**, **B** and **E**. Circle every legal stop for the television and cross every cell that is 1.0 m from it but illegal. Then draw the two episodes of question 2 as step-counted paths, dashed for the shortest path and solid for the walked one.
2. **Derive.** (a) Recompute $g(\text{sofa})$, $g(\text{tv})$, $g(\text{plant})$ at $T = 0.25$ and say what changed and what did not. (b) Give $\ell$ for the television on the new map. (c) Score two episodes: the agent walks 3 m and stops at $(2,1)$; then, in a second run, it walks 5 m by $(0,0) \to (1,0) \to (2,0) \to (2,1) \to (2,2) \to (3,2)$ and stops there. Report SPL and the success rate.
3. **Interpret.** A paper evaluates on maps like this one, reports SPL 0.50, no success rate, and explains its failures as "language grounding errors under ambiguous instructions". Using your answer to 2(a), say what the reported SPL is consistent with, and what evidence would be needed before accepting the language explanation.

> [!note]- How to draw it · 그리는 법
> - The grid full size, 4×4, one square per cell, with every cell labelled $(c, r)$, and the three object cells shaded with their names written in.
> - The wall segments as thick lines *on the edges between* cells, not inside cells: the whole geometry lesson is that a wall lives on an edge and an object lives in a cell.
> - For the goal object, every **legal stop** circled: four-adjacent to the object cell, with no wall segment on the shared edge.
> - A cross on every cell that is four-adjacent to the object but separated from it by a wall: exactly $1.0$ m from the goal and *not* a legal stop (worked case, wall **C**: circles on $(3,0)$ and $(3,2)$, the cross on $(2,1)$).
> - Two paths from $(0,0)$: the shortest path to the nearest circled cell, dashed, and the path the agent actually walked, solid.
> - An arrowhead at each step of both paths, so the steps can be counted.

> [!tip]- Solutions
> 1. The circles go on $(3,0)$ and $(2,1)$; the cross goes on $(3,2)$, which is 1.0 m from the television with wall **E** between. It is the mirror image of the worked case — the legal and illegal cells have swapped.
> 2. (a) The exponents are $0.11/0.25 = 0.44$, $1.36$ and $0.36$, giving $1.553$, $3.896$ and $1.433$ with $Z = 6.882$, so $g = 0.226$, $0.566$, $0.208$. The television's score falls from 0.846 to 0.566 — a flatter distribution, because a larger temperature moves every softmax toward uniform — but the **ranking is unchanged**, and the ranking is all the agent acts on. Nothing about the grounding got worse. (b) Both $(3,0)$ and $(2,1)$ are 3 steps from the start, so $\ell = 3$ m. (c) Run 1 stops on a legal cell after the shortest path: $S = 1$, term $3/3 = 1.000$. Run 2 stops at $(3,2)$, which is 1.0 m from the television but on the far side of wall **E**, so $S = 0$ and the term is 0 whatever the path length. $\text{SPL} = (1.000 + 0)/2 = 0.500$ and the success rate is $1/2 = 0.500$.
> 3. An SPL of 0.50 is consistent with half the episodes failing on perfect paths, as here, and equally with every episode succeeding at twice the shortest path — the §2 box shows the two are indistinguishable without the success rate, which is the first missing piece. The language explanation is the second problem: at both temperatures the ranking puts the television first by a wide margin, so a grounding score cannot be what produced run 2's failure. Before accepting it you would want the ranking reported per failed episode, and the stop cell reported next to the goal cell — which would show immediately that the stop was one wall away from legal. The honest label for this failure is that the planner optimised distance to the object rather than to a legal stop.

### Sources

**Definitions and evaluation** — P. Anderson, A. Chang, D. S. Chaplot, et al., "On Evaluation of Embodied Navigation Agents," [arXiv:1807.06757](https://arxiv.org/abs/1807.06757), 2018 (introduces SPL; **unrefereed**); D. Batra, A. Gokaslan, A. Kembhavi, et al., "ObjectNav Revisited," [arXiv:2006.13171](https://arxiv.org/abs/2006.13171), 2020 (**unrefereed**).

**Simulators and datasets** — Habitat (ICCV 2019, [arXiv:1904.01201](https://arxiv.org/abs/1904.01201)); Habitat 2.0 (NeurIPS 2021); Habitat 3.0 (ICLR 2024); HM3D (NeurIPS 2021 D&B); HM3D-Semantics (CVPR 2023); HM3D-OVON ([arXiv:2409.14296](https://arxiv.org/abs/2409.14296)); GOAT-Bench ([arXiv:2404.06609](https://arxiv.org/abs/2404.06609)).

**ObjectNav methods** — Active Neural SLAM (ICLR 2020, [arXiv:2004.05155](https://arxiv.org/abs/2004.05155)); SemExp ([arXiv:2007.00643](https://arxiv.org/abs/2007.00643), CVPR 2020 challenge winner); "CoWs on Pasture" (CVPR 2023, [arXiv:2203.10421](https://arxiv.org/abs/2203.10421)); VLFM (ICRA 2024, [arXiv:2312.03275](https://arxiv.org/abs/2312.03275)); ESC (ICML 2023, [arXiv:2301.13166](https://arxiv.org/abs/2301.13166)).

**The critique** — T. Gervet, S. Chintala, D. Batra, J. Malik, D. S. Chaplot, "Navigating to Objects in the Real World," *Science Robotics*, 2023 ([arXiv:2212.00922](https://arxiv.org/abs/2212.00922)).

**VLN** — R2R (CVPR 2018 Spotlight, [arXiv:1711.07280](https://arxiv.org/abs/1711.07280)); RxR (EMNLP 2020, [arXiv:2010.07954](https://arxiv.org/abs/2010.07954)); VLN-CE (ECCV 2020, [arXiv:2004.02857](https://arxiv.org/abs/2004.02857)); HAMT (NeurIPS 2021, [arXiv:2110.13309](https://arxiv.org/abs/2110.13309)); DUET (CVPR 2022, [arXiv:2202.11742](https://arxiv.org/abs/2202.11742)); sim-to-real: P. Anderson et al., CoRL 2020 ([arXiv:2011.03807](https://arxiv.org/abs/2011.03807)); NaVid (RSS 2024, [arXiv:2402.15852](https://arxiv.org/abs/2402.15852)); Uni-NaVid (RSS 2025, [arXiv:2412.06224](https://arxiv.org/abs/2412.06224)); NaVILA (RSS 2025, [arXiv:2412.04453](https://arxiv.org/abs/2412.04453)).

**Language-queryable maps** — Hydra (RSS 2022, [arXiv:2201.13360](https://arxiv.org/abs/2201.13360)); Khronos (RSS 2024); CLIP-Fields (RSS 2023); ConceptFusion (RSS 2023, [arXiv:2302.07241](https://arxiv.org/abs/2302.07241)); VLMaps (ICRA 2023, [arXiv:2210.05714](https://arxiv.org/abs/2210.05714)); ConceptGraphs (ICRA 2024, [arXiv:2309.16650](https://arxiv.org/abs/2309.16650)); HOV-SG (RSS 2024); Clio (*IEEE RA-L* 9(10):8921–8928, 2024, [arXiv:2404.13696](https://arxiv.org/abs/2404.13696)).

**Where the energy went** — HomeRobot (CoRL 2023, [arXiv:2306.11565](https://arxiv.org/abs/2306.11565)); the OVMM challenge post-mortem ([arXiv:2407.06939](https://arxiv.org/abs/2407.06939)).

**Within this wiki**

- **Paper notes** — [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] · [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] · [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] · [[01-canonical-papers/notes/9-navigation/navid|NaVid]] · [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] · [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] · [[01-canonical-papers/notes/9-navigation/clio|Clio]] · [[01-canonical-papers/notes/9-navigation/vint-nomad|ViNT / NoMaD]] · [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al. 2023]]
- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — the geometric half of the same problem
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — the outdoor counterpart
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]] and [[01-canonical-papers/notes/2-computer-vision/sam|SAM]] — the ingredients §7 assembles

## 한국어

*I군이다. [[04-robotics/planning-decision-making|4. 계획]] 위에 서고, 실질적으로는 VLM 노트에도 기댄다.
목표가 좌표가 아니라 단어일 때 어려운 문제는 경로 찾기가 아니라 어디를 볼지 정하는 것이 된다.*

> [!note] 처음이라면 · First pass
> 먼저 아래의 계속 쓰는 대상과 끝까지 계산해 보는 예제 — 지도 하나, 지시 하나, 이 문헌이 보고하는 두 숫자 — 그다음 §1, 고전적 독자가 해야 하는 전환, 그다음 §2, 이 분야 혼란 대부분이 ObjectNav의 정의에 합의하지 않은 채 논쟁하는 데서 오기 때문이다, 그다음 §8. §3~§7은 역사이니 정의가 단단해진 뒤에 읽어라.

### 계속 쓰는 대상: 지도 G4

대상이 *지도*인 페이지에는 [[02-foundations/lab-plants|0.6]]의 어떤 장치도 맞지 않으므로, 이 페이지는 자기 것을 하나 고정하고 끝까지 바꾸지 않는다. **G4**는 1 m 칸 4×4 격자다. 칸 중심은 정수 좌표 $(c, r)$이고 $c$는 왼쪽에서 오른쪽으로 가는 열, $r$은 아래에서 위로 가는 행이며 둘 다 0에서 3까지다. 이동은 4-연결, 한 걸음에 1 m, 대각선은 없다.

| | $c=0$ | $c=1$ | $c=2$ | $c=3$ |
|---|---|---|---|---|
| $r=3$ | **sofa** | · | · | **plant** |
| $r=2$ | · | · | · | · |
| $r=1$ | · | · | · | **tv** |
| $r=0$ | **start** | · | · | · |

라벨이 붙은 물체 셋이 칸 셋을 채우고, 그 칸에는 에이전트가 들어갈 수 없다: $(0,3)$의 **sofa**, $(3,1)$의 **tv**, $(3,3)$의 **plant**. 에이전트는 $(0,0)$에서 출발한다. **벽 선분** 셋은 칸 사이의 변 위에 놓여 그 변을 가로지르는 이동만 막는다. 그 이상은 아무것도 하지 않는다:

- **A**: $(0,1)$과 $(0,2)$ 사이
- **B**: $(1,1)$과 $(1,2)$ 사이
- **C**: $(2,1)$과 $(3,1)$ 사이

A와 B는 방 왼쪽을 가로지르는 칸막이이고, C는 텔레비전이 걸린 짧은 벽이다. 지시도 고정이다: **"텔레비전으로 가라."** 에이전트는 §7이 말하는 종류의 물체 중심 지도를 들고 있어서 라벨 셋과 그 칸은 주어져 있다. 해야 할 일은 지시를 그중 하나에 접지(ground)하고, 합법적인 곳에 멈추는 것이다.

마지막으로, 에이전트의 open-vocabulary 검출기가 각 지도 노드를 목표 구절과 이미 대조해 두었다. 이 코사인 유사도 셋은 어떤 시스템의 측정값이 아니라 이 페이지가 고정한 숫자다: $s_{\text{sofa}} = 0.11$, $s_{\text{tv}} = 0.34$, $s_{\text{plant}} = 0.09$.

*범위: 이 페이지는 이 문헌이 쓰인 두 정의 — ObjectNav 성공 기준과 SPL — 와, 접지 점수와 지도 기하가 어떻게 정지 결정 하나로 합쳐지는지를 가르친다. 프런티어를 어떻게 고르고 지역 제어기가 어떻게 모는지([[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 조작]]), 시각-언어 특징을 어떻게 학습하는지([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), 실외 traversability([[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]])는 가르치지 않는다.*

### 그림으로 먼저 보기: G4와 합법적 정지 칸, 그리고 경로 하나

<svg viewBox="0 0 560 350" style="max-width:100%;height:auto" role="img" aria-label="지시 텔레비전으로 가라에 대한 지도 G4: sofa, tv, plant 칸을 칠한 4×4 격자, 칸의 변 위에 그린 벽 A, B, C, 동그라미 친 합법적 정지 칸 (3,0)과 (3,2), 가위표 친 (2,1), 점선의 최단 경로와 실선의 에피소드 3 경로">
  <defs><marker id="arG4k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="40" y="18" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <rect x="250" y="158" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <rect x="250" y="18" width="70" height="70" fill="currentColor" fill-opacity="0.16"/>
  <line x1="40" y1="18" x2="320" y2="18" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="18" x2="40" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="88" x2="320" y2="88" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="110" y1="18" x2="110" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="158" x2="320" y2="158" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="180" y1="18" x2="180" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="228" x2="320" y2="228" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="250" y1="18" x2="250" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="40" y1="298" x2="320" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <line x1="320" y1="18" x2="320" y2="298" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <text x="44" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(0,0)</text>
  <text x="44" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(0,1)</text>
  <text x="44" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(0,2)</text>
  <text x="44" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(0,3)</text>
  <text x="114" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(1,0)</text>
  <text x="114" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(1,1)</text>
  <text x="114" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(1,2)</text>
  <text x="114" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(1,3)</text>
  <text x="184" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(2,0)</text>
  <text x="184" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(2,1)</text>
  <text x="184" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(2,2)</text>
  <text x="184" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(2,3)</text>
  <text x="254" y="241" font-size="11" fill="currentColor" fill-opacity="0.6">(3,0)</text>
  <text x="254" y="171" font-size="11" fill="currentColor" fill-opacity="0.6">(3,1)</text>
  <text x="254" y="101" font-size="11" fill="currentColor" fill-opacity="0.6">(3,2)</text>
  <text x="254" y="31" font-size="11" fill="currentColor" fill-opacity="0.6">(3,3)</text>
  <text x="75" y="58" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">sofa</text>
  <text x="285" y="198" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">tv</text>
  <text x="285" y="58" font-size="12.5" fill="currentColor" text-anchor="middle" font-weight="600">plant</text>
  <text x="75" y="290" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">출발</text>
  <circle cx="75" cy="263" r="3.2" fill="currentColor" fill-opacity="1"/>
  <line x1="41.5" y1="158" x2="108.5" y2="158" stroke="currentColor" stroke-width="6"/>
  <text x="75" y="151" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">A</text>
  <line x1="111.5" y1="158" x2="178.5" y2="158" stroke="currentColor" stroke-width="6"/>
  <text x="145" y="151" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">B</text>
  <line x1="250" y1="159.5" x2="250" y2="226.5" stroke="currentColor" stroke-width="6"/>
  <text x="243" y="174.5" font-size="12" fill="currentColor" text-anchor="end" font-weight="700">C</text>
  <circle cx="285" cy="263" r="19" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <circle cx="285" cy="123" r="19" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="202" y1="180" x2="228" y2="206" stroke="currentColor" stroke-width="2.2"/>
  <line x1="202" y1="206" x2="228" y2="180" stroke="currentColor" stroke-width="2.2"/>
  <line x1="87" y1="269" x2="133" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4k)"/>
  <line x1="157" y1="269" x2="203" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4k)"/>
  <line x1="227" y1="269" x2="263" y2="269" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4k)"/>
  <line x1="69" y1="251" x2="69" y2="205" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4k)"/>
  <line x1="81" y1="193" x2="127" y2="193" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4k)"/>
  <line x1="151" y1="193" x2="188" y2="193" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4k)"/>
  <circle cx="354" cy="36" r="8" fill="none" stroke="currentColor" stroke-width="1.6"/>
  <text x="372" y="40" font-size="11" fill="currentColor">합법적 정지 칸: tv와 인접,</text>
  <text x="372" y="54" font-size="11" fill="currentColor">공유 변에 벽이 없음</text>
  <line x1="348" y1="72" x2="360" y2="84" stroke="currentColor" stroke-width="2"/>
  <line x1="348" y1="84" x2="360" y2="72" stroke="currentColor" stroke-width="2"/>
  <text x="372" y="82" font-size="11" fill="currentColor">tv에서 1.0 m지만 벽 C가</text>
  <text x="372" y="96" font-size="11" fill="currentColor">사이에 있음: 정지 칸 아님</text>
  <line x1="344" y1="120" x2="363" y2="120" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3" marker-end="url(#arG4k)"/>
  <text x="372" y="124" font-size="11" fill="currentColor">가장 가까운 합법적 정지</text>
  <text x="372" y="138" font-size="11" fill="currentColor">(3,0)까지 최단 경로: ℓ = 3 m</text>
  <line x1="344" y1="162" x2="363" y2="162" stroke="currentColor" stroke-width="1.8" marker-end="url(#arG4k)"/>
  <text x="372" y="166" font-size="11" fill="currentColor">실제로 걸은 경로(에피소드 3):</text>
  <text x="372" y="180" font-size="11" fill="currentColor">p = 3 m, (2,1)에 정지: S = 0</text>
  <line x1="344" y1="204" x2="364" y2="204" stroke="currentColor" stroke-width="6"/>
  <text x="372" y="208" font-size="11" fill="currentColor">벽: 변 위에 산다</text>
  <rect x="345" y="225" width="18" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/>
  <text x="372" y="238" font-size="11" fill="currentColor">물체: 칸을 채운다</text>
  <text x="12" y="324" font-size="11" fill="currentColor">(3,0)과 (2,1)은 둘 다 출발에서 3걸음, tv에서 1.0 m다.</text>
  <text x="12" y="339" font-size="11" fill="currentColor">tv를 볼 수 있는 것은 (3,0)뿐이다. 접지 g(tv) = 0.846은 맞았고, 정지가 틀렸다.</text>
</svg>

지시 "텔레비전으로 가라"에 대한 아래 계산의 경우를 G4 위에 그린 것으로, sofa, tv, plant가 제 칸을 채우고 벽 **A**, **B**, **C** 셋은 칸의 변 위에 있으며, 합법적 정지 칸 $(3,0)$과 $(3,2)$에는 동그라미를, tv에서 $1.0$ m이지만 벽 **C** 뒤에 있는 $(2,1)$에는 가위표를 쳤다. 점선은 가장 가까운 합법적 정지 칸까지의 최단 경로 $\ell = 3$ m이고, 실선은 에피소드 3이 걸은 경로로 역시 $p = 3$ m이지만 $(2,1)$에 멈춰 $S = 0$이다. 두 칸 모두 출발에서 세 걸음, tv에서 $1.0$ m이지만 tv를 볼 수 있는 것은 $(3,0)$뿐이어서, 접지 $g(\text{tv}) = 0.846$은 맞았고 정지가 틀렸다.

### 대상으로 한 번 끝까지: 지시 하나, 지도 하나, 숫자 둘

**1단계 — 접지 점수.**

> [!info] 정의 · Definition — 접지 점수(grounding score)
> **어떤 종류의 것인가.** *닫힌 후보 집합 위의 확률 분포*다. 후보마다 숫자 하나, 음이 아니고, 고려한 후보 전체에 대해 합이 정확히 1이다. 유사도가 아니고, 목표가 존재한다는 확신도 아니다.
>
> **정의 조건.** 셋이다. (i) 후보 집합은 **닫혀 있고 명시되어야** 한다 — 점수는 정확히 그 물체들에 대해 정규화되므로, 집합 밖의 물체는 선택될 수 없고 그 부재는 숫자에 전혀 드러나지 않는다. (ii) 원 점수에 대해 **순서를 보존한다**: 유사도가 가장 높은 것이 언제나 접지 점수도 가장 높다. (iii) **온도** $T > 0$가 뾰족함을 정하며, 이는 설계 선택이지 시각-언어 모델이 보고하는 값이 아니다.
>
> $$g(o) = \frac{\exp\big(s_o / T\big)}{\sum_{o' \in \mathcal{O}} \exp\big(s_{o'} / T\big)}$$
>
> $\mathcal{O}$는 명시된 후보 집합, $o$는 그 안의 물체 하나, $s_o$는 지시의 목표 구절과 그 물체 라벨 사이의 원 유사도, $T$는 온도다. $T$가 작으면 하드 argmax 쪽으로 날카로워지고, 크면 균등 분포 $1/|\mathcal{O}|$ 쪽으로 평평해진다.
>
> **예.** $T = 0.10$에서 G4의 물체 셋, 아래에서 계산한다: $g(\text{tv}) = 0.846$.
>
> **비-예.** 원 코사인 $s_{\text{tv}} = 0.34$는 접지 점수가 아니다 — 정규화하는 것이 없으므로 지시끼리도, 지도끼리도 비교할 수 없다. 한 에피소드에서 *지금까지* 검출한 물체들에 대해서만 정규화한 점수도 아니다. 그것은 다른 $\mathcal{O}$ 위의 접지 점수이고, 모델이 마음을 바꾼 적이 없는데도 같은 지시가 한 실행의 두 시점에서 다른 확신을 보고하는 이유가 그것이다.
>
> **왜 중요한가.** 논문이 "모델이 지시를 이해했다"며 찍는 숫자는 후보 집합과 온도라는 설계 선택 둘의 함수이고, 둘 다를 견디는 것은 *순서*뿐이다. 내비게이션 실패를 언어 탓으로 돌리는 주장을 보면 순서부터 확인하라 — 순서가 맞으면 실패는 다른 데 있고, 아래에서 정확히 그 일이 일어난다.

$T = 0.10$에서 고정된 유사도를 각각 지수화한다. softmax가 작용하는 대상이 지수 $s_o/T$이기 때문이다.

$$e^{0.11/0.10} = 3.004, \qquad e^{0.34/0.10} = 29.964, \qquad e^{0.09/0.10} = 2.460$$

정규화 상수는 $Z = 3.004 + 29.964 + 2.460 = 35.428$이므로

$$g(\text{sofa}) = 0.085, \qquad g(\text{tv}) = 0.846, \qquad g(\text{plant}) = 0.069$$

지시는 0.846으로 텔레비전에 접지된다. 과제의 언어 절반은 그것으로 끝났다.

**2단계 — 기하가 정하는 합법적 정지 칸.** §2의 성공 기준은 두 부분이고, G4에서는 이렇게 읽힌다: 에이전트는 목표에서 1.0 m 이내 — 4-인접 칸 — 에 멈춰야 **하고**, 그 자리에서 물체를 볼 수 있어야 하는데 이 지도에서는 공유 변에 벽 선분이 없다는 뜻이다. $(3,1)$의 텔레비전에는 4-인접 칸이 셋 있다: $(3,0)$, $(3,2)$, $(2,1)$. 벽 **C**가 $(2,1)$과 $(3,1)$ 사이에 있으므로 $(2,1)$은 두 번째 조건에서 탈락한다. 합법적 정지 칸은 $(3,0)$과 $(3,2)$다.

출발점에서 자유 칸 위로 벽 셋을 지키며 너비 우선 탐색을 하면 모든 칸까지의 측지 거리가 나온다: $(3,0)$은 3걸음, $(3,2)$는 5걸음, $(2,1)$도 3걸음이다. 그러므로 가장 가까운 *합법적* 정지 칸까지로 잰 최단 경로 길이는 $\ell = 3$ m다.

**3단계 — 이 지도 위 세 에피소드의 SPL.**

> [!info] 정의 · Definition — SPL(경로 길이로 가중한 성공률)
> **어떤 종류의 것인가.** 평가 집합 전체에 대해 보고하는 $[0, 1]$의 스칼라다. 실패면 0이고 성공이면 경로 효율 비인 에피소드별 항을, 에피소드에 대해 평균한 값이다.
>
> **정의 조건.** 넷이고, 각각이 이 숫자가 잘못 보고되는 자리다. (i) **모든 에피소드가 기여하고**, 실패한 에피소드는 정확히 0으로 기여한다 — 빼지 않는다. (ii) 항은 **성공으로 게이팅된다**. 효율적인 실패는 아무것도 못 얻고 낭비한 성공은 얼마간 얻는다. (iii) $\ell_i$는 출발 자세에서, 그 목표의 성공 기준을 만족시킬 가장 가까운 위치까지의 **측지** 최단 경로다 — 직선 거리가 아니고, 에이전트가 결국 멈춘 곳에서 재는 것도 아니다. (iv) $\max(p_i, \ell_i)$가 각 항을 1로 자르므로, 최단 경로를 이긴 것처럼 보이는 에피소드에 상을 줄 수 없다.
>
> $$\text{SPL} = \frac{1}{N}\sum_{i=1}^{N} S_i \, \frac{\ell_i}{\max(p_i, \ell_i)}$$
>
> $N$은 에피소드 수, $S_i \in \{0, 1\}$은 에피소드 $i$가 성공 기준 전체를 만족했는지, $\ell_i$는 그 최단 경로 길이, $p_i$는 실제로 걸은 길이다.
>
> **예.** 아래 G4의 세 에피소드: 0.519, 그리고 그 옆의 성공률 0.667.
>
> **비-예.** *성공한* 에피소드에 대해서만 $\ell_i / p_i$를 평균한 값은 SPL이 아니다 — 아래 에피소드들에서는 $(1.000 + 0.556)/2 = 0.778$이고, 이는 잘 된 실행들의 경로 효율 수치일 뿐 얼마나 자주 되는지는 말하지 않는다. "성공률 × 평균 효율"도 SPL이 아니다. 효율이 성공과 무상관일 때만 일치하는데, 이 지표가 흥미로운 이유가 바로 보통은 무상관이 아니라는 데 있다.
>
> **왜 중요한가.** 하나의 SPL 값은 헤매는 거의 완벽한 내비게이터와도, 직선으로 걷는 평범한 내비게이터와도 양립한다 — §2의 예제가 그것을 계산해 둔다 — 그래서 SPL은 옆에 성공률이 없으면 해석할 수 없고, 이 문헌이 보고하는 것은 그 둘을 함께다.

G4 위의 세 에피소드, 모두 $(0,0)$에서 출발한다:

| 에피소드 | 목표 | 정지 칸 | $S_i$ | $\ell_i$ | $p_i$ | 항 |
|---|---|---|---|---:|---:|---|
| 1 | tv | $(3,0)$ | O | 3 | 3 | $1 \times 3/3 = 1.000$ |
| 2 | plant | $(2,3)$ | O | 5 | 9 | $1 \times 5/9 = 0.556$ |
| 3 | tv | $(2,1)$ | **X** | 3 | 3 | $0$ |

에피소드 2는 엉뚱한 방을 먼저 확인한 것이다: $(0,0) \to (0,1) \to (1,1) \to (2,1) \to (2,2) \to (1,2) \to (1,3) \to (1,2) \to (2,2) \to (2,3)$, 최적 다섯 걸음에 아홉 걸음을 썼고 합법적인 plant 정지 칸에서 끝난다. 에피소드 3은 이 페이지가 존재하는 이유인 그 실패다. 따라서

$$\text{SPL} = \frac{1.000 + 0.556 + 0}{3} = 0.519, \qquad \text{성공률} = \frac{2}{3} = 0.667$$

**4단계 — 언어는 맞았는데 기하가 틀린 실패.** 에피소드 3에서 에이전트는 확신 0.846으로 지시를 텔레비전에 접지한 뒤, 텔레비전 노드까지의 거리가 1.0 m로 떨어질 때까지 걸었다. 출발에서 세 걸음 거리에 그 조건을 만족하는 칸이 둘 — $(3,0)$과 $(2,1)$ — 있으므로 플래너는 어느 쪽도 선호하지 않았다. 에이전트는 서쪽으로 돌아 들어와 $(2,1)$에 멈췄다. 언어 쪽에서는 아무것도 어긋나지 않았다. 순서는 tv, sofa, plant이고 격차도 넓다. 어긋난 것은 정지 규칙이 *물체까지의 거리*만 검사하고 *물체의 가시성*은 한 번도 검사하지 않았다는 점이고, $(2,1)$과 텔레비전 사이에는 벽 **C**가 서 있다. 플래너가 무심했던 동점이 지표에서는 1과 0의 차이 전부가 되었고, 에이전트는 볼 수 없는 화면에서 1 m 떨어져 있다.

가시성 조항의 값을 정확히 매겨 보자. 기준의 두 번째 절반을 빼고 거리만으로 같은 세 실행을 채점하면 에피소드 3이 성공이 된다:

$$\text{SPL}_{\text{거리만}} = \frac{1.000 + 0.556 + 1.000}{3} = 0.852, \qquad \text{성공률} = \frac{3}{3} = 1.000$$

이 세 에피소드 집합에서 그 조항은 SPL 0.333, 성공률 0.333을 앗아간다 — 점수의 3분의 1이고, 전부 벽 하나가 만든 것이다. 그것이 가시성 조항이 없으면 에이전트가 벽 반대편에 서서도 성공할 수 있다는 §2 문장 뒤의 산수이고, "효율을 위해 오라클 가시성 검사를 뺐다"가 결코 평가의 사소한 변경이 아닌 이유다.

### 1. 고전적 독자가 해야 하는 전환

고전적으로 목표는 **알려진 계량 공간의 자세**이고, 계획은 거기로 가는 경로를 찾는 것이다. 여기서
목표는 **단어**다 — "변기", 또는 "주방을 지나 화분에서 왼쪽" — 그 위치는 알려져 있지 않고,
어려운 문제는 경로 찾기가 전혀 아니다. **어디를 볼지 정하는 것**이다.

그것이 탐색을 커버리지 문제에서 물체-방 동시 출현에 대한 추론 문제로 바꾸고, 시각-언어 모델이
내비게이션 구성 요소가 되는 이유다.

### 2. ObjectNav — 정의를 정확히

에이전트가 **처음 보는** 환경의 임의 자세에서 시작해, 목표 물체의 *범주*만 받고, **아무 인스턴스**
로든 이동해 완료를 알려야 한다. 관측은 RGB-D와 잡음 없는 GPS+Compass이고, 지도도, 장면 그래프도,
정답 의미 라벨도 없다.

성공 기준은 두 부분이며, 두 번째 절반이 이것을 진짜 과제로 만든다:

> `STOP`을 낼 때, 에이전트는 목표 범주 인스턴스로부터 **1.0 m 이내**에 있어야 **하고**, 그 정지
> 위치에서 회전하거나 위아래를 봄으로써 오라클이 그 물체를 볼 수 있어야 한다.

가시성 조항이 없으면 에이전트가 목표에서 0.9 m 떨어진 벽 반대편에 서서 성공할 수 있다. 지표는
성공률과 **SPL**이고, 최단 경로는 에이전트의 *출발점*에 가장 가까운 인스턴스까지로 잰다.

> [!warning] 정의하는 두 문서 모두 심사를 거치지 않았다
> SPL은 *On Evaluation of Embodied Navigation Agents*(2018)에서 도입되었고, 그 문서는 스스로를
> 워킹 그룹 보고서라고 서술한다. 과제 정의는 *ObjectNav Revisited*(2020)에서 온다. **둘 다 심사를
> 거친 적이 없고**, 그 둘이 문헌 전체가 보고하는 지표를 정의한다. 인용할 때 소리 내어 말할
> 가치가 있다.

> [!example] 계산 예제 · Worked example
> **SPL 0.47이 실제로 하는 말.** 경로 길이로 가중한 성공률(Anderson 외 2018)은
> $\text{SPL} = \frac{1}{N}\sum_i S_i \frac{\ell_i}{\max(p_i, \ell_i)}$이다. $S_i$는 성공 여부,
> $\ell_i$는 최단 경로, $p_i$는 실제로 걸은 경로다. 에피소드 셋:
>
> | 에피소드 | 성공 | 최단 $\ell$ | 실제 $p$ | 항 |
> |---|---|---|---|---|
> | 1 | O | 10 m | 10 m | $1 \times 10/10 = 1.00$ |
> | 2 | O | 10 m | 25 m | $1 \times 10/25 = 0.40$ |
> | 3 | X | 10 m | 8 m | $0$ |
>
> $\text{SPL} = (1.00 + 0.40 + 0)/3 = \mathbf{0.47}$이고, 성공률은 $2/3 = 0.67$이다.
>
> **여기서 얻는 독법.** *매번* 성공하지만 늘 최단 경로의 두 배를 걷는 에이전트는
> $1 \times 10/20 = 0.50$을 받는다. 즉 0.47은 헤매는 거의 완벽한 내비게이터와도, 직선으로
> 걷는 47%짜리 내비게이터와도 똑같이 들어맞는다. SPL만으로는 둘을 구분할 수 없다. 성공률
> 없이 보고된 SPL이 해석 불가능한 이유이자, 이 분야가 이제 둘을 함께 요구하는 이유다. SPL만
> 보이면서 효율 개선을 주장하는 논문이라면, 성공률이 움직이기는 했는지부터 확인하라.

### 3. 방법의 궤적, 세 수

**1수 — 모듈형 의미 지도.** Active Neural SLAM이 골격을 세웠다: 학습된 SLAM, 장기 목표를 고르는
전역 정책, 해석적 계획기, 지역 정책. 그 주장은 계층 구조와 고전 계획이 샘플 복잡도에서 종단간
RL을 이긴다는 것이다. **SemExp**가 그 골격에 의미 지도를 넣고, 학습된 전역 정책이 그 위에서
장기 탐색 목표를 고르게 했다. 2020년 챌린지를 우승했고 그 아키텍처가 여전히 중추다.

**2수 — 학습된 채점기를 사전학습 VLM으로 갈고, ObjectNav 전용으로는 아무것도 학습하지 않기.** **VLFM**은 점유 지도를
만들고 프런티어를 뽑은 뒤, 각 프런티어를 **목표 텍스트와의 시각-언어 유사도**로 채점해 다음에
어디를 탐색할지 고른다. ObjectNav 학습 데이터가 하나도 없고(웨이포인트 추종에는 HM3D에서 25억 스텝 학습한 PointNav 정책을 쓴다), 실제 Spot에 배치되었다. **ESC**는
같은 일을 LLM 상식 — 물체-방 동시 출현 — 을 프런티어 채점기 위의 소프트 논리 술어로 컴파일해
한다. 소프트 논리 술어란 "소파 근처의 프런티어는 TV 근처일 가능성이 높다" 같은 규칙인데, 참과
거짓이 아니라 0과 1 사이의 참값을 가지므로 채점기는 가중된 규칙 전부를 가장 잘 만족하는
프런티어를 고를 수 있다. 그리고 **CoWs**가, zero-shot 파이프라인이 "5억 스텝을 학습한 최신 ZSON(Zero-Shot Object-goal Navigation) 방법의 주행 효율과
대등하다"는 것을 보였다 — Habitat MP3D에서 대등한 것은 SPL이지 성공률이 아니다(SPL 4.9 vs 4.8, 성공률 9.2 vs 15.3). 성공률에서는 논문 스스로 그
비교가 "CoW 계열보다 in-domain 학습이 이로울 수 있음을 시사한다"고 적는다. RoboTHOR에서는 같은 CoW가 이전 zero-shot 모델보다 성공률이 15.6포인트 높다. 복잡한 언어를 활용하는
데는 약하다는 것을 확립했다.

**3수 — 모듈형 장치를 통째로 버리기.** §5를 보라.

> [!note] CoWs는 진짜 제목으로 인용하라
> 논문은 *"CoWs on Pasture: Baselines and Benchmarks for Language-Driven Zero-Shot Object
> Navigation"* 이다. "CLIP on Wheels"는 *방법* 이름이다. 2차 출처가 어김없이 잘못 인용한다.

### 4. 모든 것을 재구성하는 비판

Gervet 등이 고전·모듈형 학습·종단간 접근을 **실제 가정 여섯 곳**의 실기계에서 시험했다:

| 접근 | 결과 |
|---|---|
| **고전** | 시뮬레이션 78% → 실세계 80% |
| **모듈형 학습** | 시뮬레이션 81% → **실세계 90%** |
| **종단간 학습** | **시뮬레이션 77% → 실세계 23%** |

부하를 지는 결론은 격차 자체가 아니라 그 설명이다: 시뮬레이터가 평가 벤치마크로서 실패하는
이유가 **둘**이라는 것 — 시각적 sim-to-real 격차, 그리고 **어긋난 실패 패턴**. 세 계열 모두 시뮬레이션에서 80% 근처라
시뮬레이션으로는 서로를 가를 수 없었고, 시뮬레이션과 현실이 *다른 방식으로* 실패하므로 무엇을 고쳐야 할지도 알려 주지 못한다. 종단간 설계 변형들 사이에서는 **시뮬레이션 점수를 올린 선택이 실세계 점수를 낮췄다.** 재는
대상이 나아지지 않은 채로 리더보드를 오를 수 있다.

### 5. VLN, 그리고 벤치마크가 부정행위였음을 인정한 논문

**R2R**이 과제와 Matterport3D 시뮬레이터를 만들었다: 실제 건물에서 자연어 경로 지시를 따르기.
그러나 R2R은 **이산적**이다 — 에이전트가 미리 만든 내비게이션 그래프의 노드 사이를 순간이동한다.
**RxR**이 다국어 지시와 자세에 대한 단어 수준 시간 정렬(말한 단어마다 그때 주석자가 경로 위 어디에 있었는지 시각을
맞춰, 모델과 평가자가 각 구절이 경로의 어느 구간을 가리키는지 알 수 있게 한다)을 더하고, R2R의 경로 편향(R2R 경로가
전부 최단 경로여서 에이전트가 부정행위를 할 수 있다)을 교정했다.

**VLN-CE가 이 문헌에서 가장 중대한 논문이다.** R2R을 **저수준 연속 행동**과 함께 Habitat으로
옮겨, 세 가정을 한 번에 제거한다 — 알려진 위상, 오라클 내비게이션, 완벽한 위치추정 — 그리고
성능이 급격히 떨어진다. 분야가 반박 없이 받아들인 결론: **이전의 내비 그래프 결과들은 자기
단순화 가정에 의해 부풀려져 있었다.**

그 경험적 짝이 Anderson 등의 sim-to-real 연구다: **시뮬레이션 55.9% → 사전 지도가 있는 실제
46.8% → 사전 지도 없는 실제 22.5%.**

트랜스포머 시대 — **HAMT**(지난 파노라마 전체 이력에 대한 계층적 [[01-canonical-papers/notes/1-foundations/vit|ViT]](Vision Transformer, 각 시야를 패치로 잘라 토큰 열로 처리하는 이미지 모델), 긴 궤적에서 가장 크게
이득)와 **DUET**(즉석에서 만드는 위상 지도, 되돌아가기를 포함한 거친 전역 계획과 미세 지역
인코딩의 결합) — 는 이산 패러다임의 정점이고, 그렇게 읽을 가치가 있다.

그다음 **NaVid**가 다른 가지를 열었다: **단안 RGB 비디오만 — 지도도, 오도메트리도, 깊이도 없이** — 받아
행동을 직접 내는 비디오 VLM이다. HAMT와 DUET의 모듈형 장치를 버렸고 여러 후속 video-VLA가
이 발상을 잇지만, 그래프 기반·모듈형 VLN 연구도 병행된다.

> [!important] 정확히 말하라
> **내비 그래프는 현대의 유일한 정식화가 아니며, R2R도 단순히 낡았다고 할 수 없다.** VLN-CE는
> R2R과 RxR을 Habitat으로 옮겼고, 이산 그래프 벤치마크와 연속 embodied 변형이 함께 쓰인다.
> 숫자를 비교하기 전에 행동 공간·위치추정 접근·내비게이션 오라클을 밝힌다.

### 6. 두 갈래가 합쳐졌고, 벤치마크는 해체되었다

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="2018년의 두 별개 내비게이션 갈래가 2025년까지 하나의 비디오 VLA로 수렴하고, 그동안 챌린지들이 끝난다">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="34" y1="212" x2="528" y2="212"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="60" y1="212" x2="60" y2="218"/><line x1="180" y1="212" x2="180" y2="218"/><line x1="300" y1="212" x2="300" y2="218"/><line x1="380" y1="212" x2="380" y2="218"/><line x1="460" y1="212" x2="460" y2="218"/>
  </g>
  <g fill="currentColor">
    <rect x="34" y="52" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="34" y="112" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="392" y="76" width="136" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="34" y="52" width="250" height="32" rx="3"/><rect x="34" y="112" width="250" height="32" rx="3"/><rect x="392" y="76" width="136" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.8" marker-end="url(#arSk)">
    <path d="M 290 68 L 340 68 L 340 92 L 386 92"/>
    <path d="M 290 128 L 340 128 L 340 106 L 386 106"/>
  </g>
  <defs><marker id="arSk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="72">ObjectNav &#8212; 지명된 물체 찾기</text>
    <text x="46" y="132">VLN &#8212; 경로 지시 따르기</text>
    <text x="460" y="95" text-anchor="middle" font-size="11">하나의 비디오 VLA</text>
    <text x="460" y="110" text-anchor="middle" font-size="9">내비 + 물체 탐색 + EQA + 사람 추종</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="60" y="230" text-anchor="middle">2018</text><text x="180" y="230" text-anchor="middle">2020</text><text x="300" y="230" text-anchor="middle">2023</text><text x="380" y="230" text-anchor="middle">2024</text><text x="460" y="230" text-anchor="middle">2025</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" stroke-dasharray="4 3">
    <line x1="300" y1="160" x2="300" y2="206"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="306" y="170">2023년 10월: Habitat 챌린지 저장소 보관</text>
    <text x="306" y="184">CVPR 2026: 내비게이션 챌린지 0개</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="34" y="250">내비게이션은 풀린 것이 아니라 흡수되었다 &#8212; 위로는 VLA로, 옆으로는 모바일 조작으로.</text>
  </g>
</svg>

**Uni-NaVid**가 그 합류다: **VLN, 물체 탐색, embodied QA, 사람 추종**에 걸친 360만 샘플로 학습한
하나의 비디오 VLA가 그 전부에서 SOTA를 5 Hz로 보고한다. 2020년에 저것들은 별도의 시뮬레이터와
별도의 챌린지를 가진 별도의 공동체였다.

동시에 제도적 발판이 내려앉았다. Habitat 챌린지 저장소가 **2023년 10월 읽기 전용으로 보관**
되었고 2023년판이 마지막이었다. CVPR 2025 Embodied AI 워크숍은 챌린지 넷을 돌렸고 **그중 ObjectNav는
없었다.** CVPR 2026은 셋을 돌렸고 **셋 다 매니퓰레이션이었다.**

에너지가 간 곳은 측정 가능하다: **open-vocabulary 모바일 조작**이다. HomeRobot이 실세계 성공률
약 20%를 보고하고, 챌린지 사후 보고가 기준선 **0.8%**, 우승 **10.8%** 를 기록한다 — 13배
개선인데도 과제는 여전히 약 90% 미해결이다. 그것이 오를 가치가 있는 리더보드이고, 포화된 6범주
ObjectNav는 아니었다.

실제로 나온 후속들은 구조적으로 open-vocabulary다: **HM3D-OVON**(379범주, 자유 형식 언어 목표)과
**GOAT-Bench**(범주·서술·이미지 중 무엇으로든 주어지는 목표, 기억을 요구하는 긴 지평).

### 7. 나머지 절반: 언어로 질의할 수 있는 지도

나란히 굴러왔고, 이제는 ObjectNav 리더보드보다 중대하다:

- **VLMaps**는 로봇이 스스로 만든 3D 재구성에 시각-언어 특징을 융합해 **공간적** 언어 목표 —
  "소파와 TV 사이" — 를 LLM 코드 생성으로 가능하게 하고, embodiment를 가로질러 공유 가능한 로봇별
  장애물 지도를 내놓는다.
- **ConceptFusion**의 독특한 주장은 *멀티모달 질의*다: 언어·이미지·오디오·클릭이 모두 같은 지도를
  색인한다.
- **ConceptGraphs**가 조밀한 특징 필드를 **물체 중심 그래프**로 대체했다 — 다시점 융합으로 노드를,
  LLM 추론으로 간선을. 더 싸고 조합 가능해서 기본 중추가 되었다.
- **Clio**가 더 나은 질문을 한다: granularity는 고정 임계값이 아니라 **[[02-foundations/information-theory|정보 병목(Information Bottleneck)]]을 통해 과제
  목록에서 유도된다.** 정보 병목은 목표를 예측하는 것만 남기고 표현을 압축하며, 여기서 목표는 과제들이다. 같은 장면이 내비게이션에는 거친 지도를, 조작에는 세밀한 지도를 필요로 하고,
  그것을 과제가 정해야 한다.
- **Hydra**가 나머지가 가정하는 실시간 시스템 기반이고, **Khronos**가 그것을 동적 환경의 시공간
  매핑으로 확장한다.

2025~26년에 보이는 두 방향은 **가우시안 스플래팅**이 NeRF식 필드와 나란히 의미 substrate로
넓게 쓰이는 것, 그리고 물체 중심 **장면 그래프**가 여러 기하 substrate 위의 질의 인터페이스로
쓰이는 것이다. 어느 하나가 보편적으로 나머지를 밀어낸 것은 아니다. 갱신 비용·기하 품질·동적
장면·질의 요구를 비교해야 한다.

> [!note] 지도 하나인가, 여러 경험인가 · One map, or many experiences?
> 위의 표현은 모두 무엇이 지금 어디 있는지에 대한 일관된 추정 하나를 만든다. Churchill과 Newman의 경험 기반 내비게이션(IJRR 2013)은 겉모습이 변하는 장소에 대해 반대 길을 택했다. 모델 하나를 현재 쪽으로 고쳐 가는 대신, 같은 작업 공간을 석 달간 — 시간대·날씨·조명을 가로질러 — 주행한 차량이 **서로 구별되는 시각 경험**들을 쌓았다. 각 경험이 하나의 시각 모드를 담는다. 그러면 localization은 현재 영상을 그 이전 경험들에 정합시키는 일이 되고, 충분한 수에 정합하지 못하는 것 자체가 지금 영상 열을 새 경험으로 눕히라는 신호가 된다. 37 km, 13만 6천 프레임 넘게 주행하는 동안 필요한 경험의 수는 끝없이 늘지 않고 상수로 수렴했다.
>
> 이것을 위의 지도들 옆에 놓아 보라. "지도가 틀렸다"는 말의 뜻이 달라진다. 모델 하나짜리 지도에서 옮겨진 의자와 달라진 조명은 고쳐 없앨 오류다. 경험 기반 표현에서는 다음에 다시 나타날 때 알아볼 모드다. 이 차이는 같은 장소가 여러 모습을 갖기에 충분할 만큼 긴 운용에서만 드러난다.

> [!important] 위키의 인식 노트들이 향하던 곳이 여기다
> [[01-canonical-papers/notes/2-computer-vision/sam|SAM]],
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]],
> [[01-canonical-papers/notes/2-computer-vision/dino|DINO]],
> [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]],
> [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]가 *재료*다. 이 절이 그것들로 만들어지는
> 것이고 — 지도야말로 어떤 제어기보다 먼저 내비게이션과 매니퓰레이션이 만나는 곳이다.

### 8. 이 분야의 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 내비 그래프인가 연속인가? | 내비 그래프 수치는 VLN-CE 수치와 비교 불가다 |
| 시뮬레이션인가 실기계인가? | 시뮬 순위는 실제 순위를 보존하지 않는다 |
| 어떤 데이터를 썼는가: ObjectNav 전용, 다른 embodied 데이터, 또는 없음? | 강한 zero-shot 모듈형 방법은 ObjectNav 전용 학습을 쓰지 않을 수 있지만 종단간 비디오/VLA는 대규모 embodied 데이터를 학습할 수 있다 |
| 어느 HM3D/MP3D 분할이며 범주가 몇 개인가? | 6범주 ObjectNav는 포화, 379범주는 아니다 |
| 언어가 실제로 부하를 지고 있는가? | 재구성 문장에 대한 민감성이 표준적 실패다 |
| SPL인가 맨 성공률인가? | 성공률만으로는 비효율적 배회가 보상된다 |

2025~26년 논문이 self-correction이나 reasoning을 내세운다면 물어 볼 질문이 하나 더 있다.
*추가된 능력은 어디에 사는가?* 자기 복구 데이터로 post-training한 모델은 학습 중 본 실패와 닮은
상황에서 올바로 행동하도록 배운 것이다. 실행 중 불확실성을 추정하고 그때 계산을 더 쓰는 시스템은
다른 일을 하고 있다. 둘 다 self-correction이라 불리므로 기전을 읽어라
([[03-deep-learning/lineage|계보 — Robot Learning]]).

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 가시성 조항을 포함한 ObjectNav 성공 기준과 그것이 존재하는 이유를 말한다.
- [ ] VLN-CE가 무엇을 제거했고 무엇을 보였는지 설명한다.
- [ ] 모듈형 대 종단간의 실세계 수치와 그 이유를 댄다.
- [ ] Habitat 챌린지에 무슨 일이 있었고 분야가 어디로 갔는지 말한다.
- [ ] 기본 중추가 된 지도 표현과, Clio가 던진 더 나은 질문을 댄다.

> [!tip] 더 깊이 · Going deeper
> 이 분야의 정본은 책이 아니라 정의 논문 둘과 비판 하나이고, 그것을 순서대로 읽는 것이 이 분야가 되풀이하는 논쟁에 휘말리지 않는 방법이다. 먼저 Anderson 외(2018), SPL과 평가 어휘를 위해 — 심사를 거치지 않은 논문이니 그렇게 인용하라. 그다음 "ObjectNav Revisited"(2020), 첫 정의가 충분히 조이지 못했기 때문에 존재하는 논문이다. 그다음 §4의 비판, 이것이 §5~§6의 벤치마크 역사를 읽히게 만든다. Habitat 논문들은 인프라 문서다. 지금 읽는 논문이 쓴 판본에 해당하는 것만 읽고 전부 읽지는 마라.

### 스스로 점검

1. ObjectNav 성공 기준이 왜 두 부분인가?
2. 2026년 논문이 내비 그래프 R2R에서 68% 성공을 보고한다. 무엇을 결론짓겠는가?
3. 어떤 방법이 시뮬레이션 내비게이션 벤치마크에서 좋은 점수를 낸다. Gervet 등에 따르면 무엇을
   추론하면 *안 되는가*?
4. ObjectNav 챌린지가 중단되었다. 물체 목표 내비게이션이 풀렸다는 뜻인가?
5. 방으로 이동하는 것과 그 안의 무언가를 파지하는 것을 모두 지원하는 지도가 필요하다. 현재 문헌은
   무엇을 시사하는가?

> [!tip]- 정답 · Answers
> 1. 근접만으로는 과제가 아니기 때문이다. 오라클 가시성 조항이 없으면 에이전트가 목표에서 0.9 m 떨어진, 그 사이에 벽이 있는 곳에 멈춰서 정답 처리를 받을 수 있고, 그것은 *물체*를 찾은 것이 아니라 *좌표*에 도달한 것을 보상하는 셈이다. 두 부분 기준이 ObjectNav를 변장한 계량 내비게이션 문제가 아니라 인식 문제로 만든다.
> 2. 연속 embodied 결과와 직접 비교할 수 없다는 것. 사전 구축 그래프는 VLN-CE에 없는 알려진 위상·이산 viewpoint·위치추정 가정을 제공할 수 있다. 그러나 그래프 기반 VLN도 계속 연구되므로, 명시한 행동 공간과 오라클 접근 프로토콜 안에서만 비교한다.
> 3. 실세계 순위가 따라올 것이라는 점. 그들의 발견은 성능이 떨어진다는 것만이 아니라 **시뮬레이션과 현실이 다른 방식으로 실패한다**는 것이고, 그래서 시뮬레이션은 방법을 가르지도, 무엇을 고칠지 보여 주지도 못한다. 세 계열은 시뮬에서 모두 80% 근처(고전 78, 모듈형 81, 종단간 77)였다가 실세계에서 80 / 90 / 23으로 벌어졌고, 종단간 변형들 사이에서는 실세계 성능이 시뮬 성능과 반비례했다. 시뮬 결과는 시뮬에 관한 증거다.
> 4. 아니다. 챌린지가 끝났거나 한 설정이 포화됐다는 사실은 바탕 과제가 해결됐다는 증거가 아니다. Open-vocabulary·평생 변형(HM3D-OVON, GOAT-Bench), 연속 제어, sim-to-real, 모바일 조작은 서로 다른 미해결 능력을 시험한다.
> 5. Granularity가 **고정이 아니라 과제에서 유도되어야 한다**는 것 — Clio의 정보 병목 정식화가 존재하는 이유가 정확히, 같은 장면에 대해 내비게이션은 거친 지도를 원하고 조작은 세밀한 지도를 원하기 때문이다. 아키텍처로는, 어떤 기하 substrate를 쓰든 그 위에 물체 중심 장면 그래프(ConceptGraphs 계보)를 질의 가능한 인터페이스로 세우고, 상세도는 과제 목록이 정하게 하라.

**계산으로 확인: 과제가 묻는 세 독법.** 온도를 견디는 것은 확신값이 아니라 순서다 — 0.846에서 0.566으로 떨어진 접지 점수는 나빠진 것이 아니므로, 격차가 넓은 접지가 실패의 원인일 수는 없다. 목표에서 1 m 떨어졌는데 사이에 벽이 있는 정지는 물체가 아니라 좌표이고, G4에서 그 가시성 조항의 값은 두 점수 모두의 3분의 1이었다. 그리고 성공률 없는 SPL은 같은 숫자로 두 이야기를 한다: 0.50은 완벽한 경로로 절반이 실패한 것이기도 하고, 모든 에피소드가 최단 경로의 두 배를 걸어 성공한 것이기도 하다.

### 과제 · Problem set

Tier B. **G4** 위에서 손으로 유도한다. 이 페이지와 선수 지식만 쓴다. 같은 격자, 같은 물체 셋, 같은 출발 $(0,0)$, 같은 지시 "텔레비전으로 가라", 같은 고정 유사도 $(0.11, 0.34, 0.09)$. 두 가지가 바뀐다. 텔레비전을 다시 걸어서 $(2,1)$과 $(3,1)$ 사이의 벽 **C**를 **없애고** $(3,1)$과 $(3,2)$ 사이에 새 벽 **E**를 놓는다. 그리고 접지 온도를 $T = 0.10$에서 $T = 0.25$로 올린다.

1. **그리기.** 위의 그림을 벽 **A**, **B**, **E** 셋으로 다시 그려라. 텔레비전의 합법적 정지 칸을 모두 동그라미 치고, 1.0 m이지만 합법적이지 않은 칸마다 가위표를 쳐라. 그다음 2번의 두 에피소드를 걸음 수가 보이는 경로로 그려라. 최단 경로는 점선, 실제로 걸은 경로는 실선이다.
2. **유도.** (a) $T = 0.25$에서 $g(\text{sofa})$, $g(\text{tv})$, $g(\text{plant})$를 다시 계산하고, 무엇이 바뀌고 무엇이 바뀌지 않았는지 말하라. (b) 새 지도에서 텔레비전의 $\ell$을 구하라. (c) 에피소드 둘을 채점하라: 에이전트가 3 m를 걸어 $(2,1)$에 멈춘다. 두 번째 실행에서는 $(0,0) \to (1,0) \to (2,0) \to (2,1) \to (2,2) \to (3,2)$로 5 m를 걷고 거기에 멈춘다. SPL과 성공률을 보고하라.
3. **해석.** 어떤 논문이 이런 지도들에서 평가하고, SPL 0.50을 보고하고, 성공률은 보고하지 않고, 실패를 "모호한 지시에서의 언어 접지 오류"로 설명한다. 2(a)의 답을 써서, 보고된 SPL이 무엇과 양립하는지, 그리고 그 언어 설명을 받아들이기 전에 어떤 증거가 필요한지 말하라.

> [!note]- 그리는 법 · How to draw it
> - 칸 하나에 정사각형 하나씩 크게 그린 4×4 격자와 모든 칸에 적은 $(c, r)$, 그리고 칠하고 이름을 써 넣은 물체 칸 셋.
> - 칸 안이 아니라 칸과 칸 *사이의 변 위에* 굵은 선으로 그린 벽 선분. 벽은 변에 살고 물체는 칸에 산다는 것이 이 기하 수업의 전부다.
> - 목표 물체의 합법적 정지 칸 전부에 친 동그라미: 물체 칸과 4-인접이면서 공유하는 변에 벽 선분이 없는 칸이다.
> - 물체와 4-인접이지만 벽으로 갈린 칸마다 친 가위표: 목표에서 정확히 $1.0$ m이면서 합법적 정지 칸이 *아닌* 칸이다(계산 예제, 벽 **C** 기준: 동그라미는 $(3,0)$과 $(3,2)$, 가위표는 $(2,1)$).
> - $(0,0)$에서 출발하는 경로 둘: 가장 가까운 동그라미 칸까지의 최단 경로는 점선, 에이전트가 실제로 걸은 경로는 실선.
> - 걸음을 셀 수 있게 두 경로의 걸음마다 단 화살표.

> [!tip]- 정답 · Solutions
> 1. 동그라미는 $(3,0)$과 $(2,1)$, 가위표는 $(3,2)$다. $(3,2)$는 텔레비전에서 1.0 m이고 사이에 벽 **E**가 있다. 계산 예제의 거울상이다 — 합법 칸과 불법 칸이 맞바뀌었다.
> 2. (a) 지수는 $0.11/0.25 = 0.44$, $1.36$, $0.36$이고, 값은 $1.553$, $3.896$, $1.433$, $Z = 6.882$이므로 $g = 0.226$, $0.566$, $0.208$이다. 텔레비전의 점수는 0.846에서 0.566으로 떨어진다 — 온도가 커지면 모든 softmax가 균등 쪽으로 밀리므로 더 평평해진 분포다 — 그러나 **순서는 그대로이고**, 에이전트가 행동의 근거로 삼는 것은 순서뿐이다. 접지가 나빠진 것은 아무것도 없다. (b) $(3,0)$과 $(2,1)$ 모두 출발에서 3걸음이므로 $\ell = 3$ m다. (c) 실행 1은 최단 경로로 합법 칸에 멈추므로 $S = 1$, 항은 $3/3 = 1.000$이다. 실행 2는 $(3,2)$에 멈추는데 텔레비전에서 1.0 m이지만 벽 **E** 반대편이므로 $S = 0$이고, 경로 길이가 얼마든 항은 0이다. $\text{SPL} = (1.000 + 0)/2 = 0.500$, 성공률은 $1/2 = 0.500$이다.
> 3. SPL 0.50은 여기처럼 완벽한 경로로 걸으면서 절반이 실패하는 것과도, 모든 에피소드가 최단 경로의 두 배를 걸으며 성공하는 것과도 양립한다 — §2의 예제가 성공률 없이는 둘을 구분할 수 없음을 보인다. 그 성공률이 빠진 첫 번째 조각이다. 언어 설명은 두 번째 문제다. 두 온도 모두에서 순서는 텔레비전을 넓은 격차로 1위에 두므로, 실행 2의 실패를 만든 것이 접지 점수일 수는 없다. 받아들이기 전에 실패한 에피소드별 순서와, 목표 칸 옆에 나란히 적은 정지 칸을 요구해야 한다. 그러면 정지가 합법에서 벽 하나 떨어져 있었다는 것이 즉시 드러난다. 이 실패의 정직한 이름은 플래너가 합법적 정지 칸이 아니라 물체까지의 거리를 최적화했다는 것이다.

### 출처

**정의와 평가** — P. Anderson, A. Chang, D. S. Chaplot, et al., "On Evaluation of Embodied Navigation Agents," [arXiv:1807.06757](https://arxiv.org/abs/1807.06757), 2018 (SPL 도입, **미심사**); D. Batra, A. Gokaslan, A. Kembhavi, et al., "ObjectNav Revisited," [arXiv:2006.13171](https://arxiv.org/abs/2006.13171), 2020 (**미심사**).

**시뮬레이터와 데이터셋** — Habitat (ICCV 2019, [arXiv:1904.01201](https://arxiv.org/abs/1904.01201)); Habitat 2.0 (NeurIPS 2021); Habitat 3.0 (ICLR 2024); HM3D (NeurIPS 2021 D&B); HM3D-Semantics (CVPR 2023); HM3D-OVON ([arXiv:2409.14296](https://arxiv.org/abs/2409.14296)); GOAT-Bench ([arXiv:2404.06609](https://arxiv.org/abs/2404.06609)).

**ObjectNav 방법** — Active Neural SLAM (ICLR 2020, [arXiv:2004.05155](https://arxiv.org/abs/2004.05155)); SemExp ([arXiv:2007.00643](https://arxiv.org/abs/2007.00643)); "CoWs on Pasture" (CVPR 2023, [arXiv:2203.10421](https://arxiv.org/abs/2203.10421)); VLFM (ICRA 2024, [arXiv:2312.03275](https://arxiv.org/abs/2312.03275)); ESC (ICML 2023, [arXiv:2301.13166](https://arxiv.org/abs/2301.13166)).

**비판** — T. Gervet, S. Chintala, D. Batra, J. Malik, D. S. Chaplot, "Navigating to Objects in the Real World," *Science Robotics*, 2023 ([arXiv:2212.00922](https://arxiv.org/abs/2212.00922)).

**VLN** — R2R (CVPR 2018 Spotlight, [arXiv:1711.07280](https://arxiv.org/abs/1711.07280)); RxR (EMNLP 2020, [arXiv:2010.07954](https://arxiv.org/abs/2010.07954)); VLN-CE (ECCV 2020, [arXiv:2004.02857](https://arxiv.org/abs/2004.02857)); HAMT (NeurIPS 2021, [arXiv:2110.13309](https://arxiv.org/abs/2110.13309)); DUET (CVPR 2022, [arXiv:2202.11742](https://arxiv.org/abs/2202.11742)); sim-to-real: P. Anderson et al., CoRL 2020 ([arXiv:2011.03807](https://arxiv.org/abs/2011.03807)); NaVid (RSS 2024, [arXiv:2402.15852](https://arxiv.org/abs/2402.15852)); Uni-NaVid (RSS 2025, [arXiv:2412.06224](https://arxiv.org/abs/2412.06224)); NaVILA (RSS 2025, [arXiv:2412.04453](https://arxiv.org/abs/2412.04453)).

**언어로 질의하는 지도** — Hydra (RSS 2022, [arXiv:2201.13360](https://arxiv.org/abs/2201.13360)); Khronos (RSS 2024); CLIP-Fields (RSS 2023); ConceptFusion (RSS 2023, [arXiv:2302.07241](https://arxiv.org/abs/2302.07241)); VLMaps (ICRA 2023, [arXiv:2210.05714](https://arxiv.org/abs/2210.05714)); ConceptGraphs (ICRA 2024, [arXiv:2309.16650](https://arxiv.org/abs/2309.16650)); HOV-SG (RSS 2024); Clio (*IEEE RA-L* 9(10):8921–8928, 2024, [arXiv:2404.13696](https://arxiv.org/abs/2404.13696)).

**에너지가 간 곳** — HomeRobot (CoRL 2023, [arXiv:2306.11565](https://arxiv.org/abs/2306.11565)); OVMM 챌린지 사후 보고 ([arXiv:2407.06939](https://arxiv.org/abs/2407.06939)).

**이 위키 안에서**

- **논문 노트** — [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] · [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] · [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] · [[01-canonical-papers/notes/9-navigation/navid|NaVid]] · [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] · [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] · [[01-canonical-papers/notes/9-navigation/clio|Clio]] · [[01-canonical-papers/notes/9-navigation/vint-nomad|ViNT / NoMaD]] · [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등 2023]]
- [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 조작]] — 같은 문제의 기하학적 절반
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]] — 실외 대응물
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]]과 [[01-canonical-papers/notes/2-computer-vision/sam|SAM]] — §7이 조립하는 재료들
