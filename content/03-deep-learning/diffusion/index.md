---
title: 6. Diffusion & Flow
tags: [deep-learning, diffusion, flow-matching, curriculum]
study-depth: Literacy
wiki-support: Working
depth-goal: "Compute one forward noising step and one DDPM denoising step, distinguish score/noise/velocity parameterizations, and sweep sampler steps against reconstruction error and latency."
mastery-when: "Raise when the generative objective, sampler, action distribution, or flow field is modified in the thesis."
---

> [!note] Prerequisites · 선수 지식
> Object **D6** from [[03-deep-learning/lab-objects|0. Lab Objects]] · [[02-foundations/lab-kernel|0.65 Lab Kernel]], because this page is Tier A · [[02-foundations/probability|3. Probability]], [[02-foundations/information-theory|5. Information Theory]], [[03-deep-learning/foundations/index|1. Learning Systems]], and [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs]].
> [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상 **D6** · 이 페이지는 Tier A이므로 [[02-foundations/lab-kernel|0.65 Lab Kernel]] · [[02-foundations/probability|3. Probability]], [[02-foundations/information-theory|5. Information Theory]], [[03-deep-learning/foundations/index|1. Learning Systems]], [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN]].

## English

*Stands on the Gaussian algebra of [[02-foundations/probability|3. Probability]] and the training loop of [[03-deep-learning/foundations/index|1. Learning Systems]]. First use of object **D6**.*

> [!note] First pass
> Read the running object, the worked case, §§1–2, and problems 1–2. Return to §4 when a policy cuts denoising steps, and to §5 for the number of steps it can afford.

### Running object · 이 페이지의 대상

**D6** from [[03-deep-learning/lab-objects|0. Lab Objects]], at the numbers that page freezes. For **D6**, $x_0=2$, $\epsilon=-1$, and $\bar\alpha_t=0.64$. The standard closed-form forward sample is

$$x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon=0.8(2)+0.6(-1)=1.$$

Training can ask a network to recover the known noise $\epsilon=-1$ from $(x_t,t)$, optionally conditioned on context.

| Symbol | Value | What it is |
|---|---:|---|
| $x_0$ | $2$ | the clean datum |
| $\epsilon$ | $-1$ | the frozen noise draw used for every forward sample on this page |
| $T$ | $20$ | levels in the schedule, $i=0$ clean and $i=20$ noisiest |
| $\sqrt{\bar\alpha_i}$ | $1-0.8\,i/T$ | the signal coefficient: linear from $1.0$ down to $0.2$ |
| $\bar\alpha_5$ | $0.64$ | the catalog level, where $x_t=1$ |
| $\bar\alpha_{20}$ | $0.04$ | the noisiest level the sampler starts from |
| $b$ | $0.2$ | the network's frozen error in its noise output |
| $c$ | $5\,\mathrm{ms}$ | assumed cost of one network evaluation on the deployment machine |

The network is specified as completely as the datum: it returns the noise that would explain $x$ if the datum were $x_0$, plus a constant offset, $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+b$. At the catalog level that is $-1+0.2=-0.8$, which is exactly the imperfect prediction §2 already uses. Freezing the *model* as well as the data is what makes the sampler the only thing left varying in §5.

*Scope: this page teaches the two processes a diffusion model is made of, how a prediction target is translated between parameterizations, and what the number of sampler steps costs and buys. It does not teach the score-matching and variational derivations that justify the loss, which live with the density estimation of [[02-foundations/probability|3. Probability]] and [[02-foundations/information-theory|5. Information Theory]] and, for the variational bound, [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs]]; nor the network architectures (U-Net, DiT) that carry it, which are [[03-deep-learning/computer-vision/index|2. Computer Vision]]; nor how a sampled action is committed to a robot, which is the chunk of [[03-deep-learning/vla/index|4. VLA]].*

### Homework diagram · 과제가 그릴 그림

Two paths that share a set of levels and nothing else, and the problem set asks for exactly this drawing. The figure is the worked case: D6's schedule on top, and the reverse loop drawn for $N=4$, the sweep row that equals the worked case's one-shot $1.85$.

<svg viewBox="0 0 560 384" style="max-width:100%;height:auto" role="img" aria-label="D6's schedule, the square root of alpha-bar falling linearly from 1 to 0.2 over 20 levels with its partner rising to 0.979796, above the two paths on the same levels: the forward path as one jump from the known x0 = 2 to x5 = 1 feeding the loss, and the reverse path starting at level 20 without any x0, looping N = 4 times through levels 15, 10 and 5 to the estimate 1.85">
  <defs><marker id="aD6e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) the schedule: levels, not times</text>
  <line x1="62" y1="130" x2="62" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="62" y1="36" x2="62" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="62" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <line x1="84.6" y1="130" x2="84.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="107.2" y1="130" x2="107.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="129.8" y1="130" x2="129.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="152.4" y1="130" x2="152.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="175" y1="130" x2="175" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="175" y1="36" x2="175" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="175" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">5</text>
  <line x1="197.6" y1="130" x2="197.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="220.2" y1="130" x2="220.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="242.8" y1="130" x2="242.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="265.4" y1="130" x2="265.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288" y1="130" x2="288" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288" y1="36" x2="288" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="288" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">10</text>
  <line x1="310.6" y1="130" x2="310.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="333.2" y1="130" x2="333.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="355.8" y1="130" x2="355.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="378.4" y1="130" x2="378.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="401" y1="130" x2="401" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="401" y1="36" x2="401" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="401" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">15</text>
  <line x1="423.6" y1="130" x2="423.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="446.2" y1="130" x2="446.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="468.8" y1="130" x2="468.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="491.4" y1="130" x2="491.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="514" y1="130" x2="514" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="514" y1="36" x2="514" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="514" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <text x="516" y="163" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">level i</text>
  <line x1="62" y1="130" x2="514" y2="130" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="62" y1="130" x2="62" y2="34" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="58" y1="130" x2="62" y2="130" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="134" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0</text>
  <line x1="58" y1="84" x2="62" y2="84" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="88" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.5</text>
  <line x1="58" y1="38" x2="62" y2="38" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="42" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">1</text>
  <path d="M62 38 L84.6 41.7 L107.2 45.4 L129.8 49 L152.4 52.7 L175 56.4 L197.6 60.1 L220.2 63.8 L242.8 67.4 L265.4 71.1 L288 74.8 L310.6 78.5 L333.2 82.2 L355.8 85.8 L378.4 89.5 L401 93.2 L423.6 96.9 L446.2 100.6 L468.8 104.2 L491.4 107.9 L514 111.6" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M62 130 L84.6 104.2 L107.2 93.9 L129.8 86.3 L152.4 80.1 L175 74.8 L197.6 70.2 L220.2 66.2 L242.8 62.5 L265.4 59.3 L288 56.4 L310.6 53.8 L333.2 51.4 L355.8 49.3 L378.4 47.4 L401 45.7 L423.6 44.2 L446.2 42.8 L468.8 41.7 L491.4 40.7 L514 39.9" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="6 3" stroke-linejoin="round"/>
  <circle cx="62" cy="38" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="62" cy="130" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="84.6" cy="41.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="84.6" cy="104.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="107.2" cy="45.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="107.2" cy="93.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="129.8" cy="49" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="129.8" cy="86.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="152.4" cy="52.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="152.4" cy="80.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="56.4" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="74.8" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="197.6" cy="60.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="197.6" cy="70.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="220.2" cy="63.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="220.2" cy="66.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="242.8" cy="67.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="242.8" cy="62.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="265.4" cy="71.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="265.4" cy="59.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="288" cy="74.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="288" cy="56.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="310.6" cy="78.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="310.6" cy="53.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="333.2" cy="82.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="333.2" cy="51.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="355.8" cy="85.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="355.8" cy="49.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="378.4" cy="89.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="378.4" cy="47.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="401" cy="93.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="401" cy="45.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="423.6" cy="96.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="423.6" cy="44.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="446.2" cy="100.6" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="446.2" cy="42.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="468.8" cy="104.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="468.8" cy="41.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="491.4" cy="107.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="491.4" cy="40.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="514" cy="111.6" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="514" cy="39.9" r="3.6" stroke="none" fill="currentColor"/>
  <text x="182" y="51.4" font-size="11" fill="currentColor">0.8</text>
  <text x="182" y="89.8" font-size="11" fill="currentColor">0.6</text>
  <text x="521" y="115.6" font-size="11" fill="currentColor">0.2</text>
  <text x="508" y="33.9" font-size="11" fill="currentColor" text-anchor="end">0.979796</text>
  <text x="306.1" y="124" font-size="11" fill="currentColor">√ᾱ<tspan dy="3" font-size="10">i</tspan><tspan dy="-3" dx="3.5">= 1 − 0.8 i/20</tspan></text>
  <text x="319.6" y="39" font-size="11" fill="currentColor">√(1 − ᾱ<tspan dy="3" font-size="10">i</tspan><tspan dy="-3">)</tspan></text>
  <text x="12" y="172" font-size="12" fill="currentColor">(b) two paths that share the levels and nothing else</text>
  <circle cx="62" cy="252" r="4.5" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="252" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M 65.0 247 Q 118.5 202 171.0 245" stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#aD6e)"/>
  <text x="118.5" y="194" font-size="11" fill="currentColor" text-anchor="middle">√ᾱ<tspan dy="3" font-size="10">5</tspan><tspan dy="-3" dx="3.5">x</tspan><tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">+ √(1 − ᾱ</tspan><tspan dy="3" font-size="10">5</tspan><tspan dy="-3">) ε</tspan></text>
  <text x="118.5" y="210" font-size="11" fill="currentColor" text-anchor="middle">= 0.8·2 + 0.6·(−1) = 1</text>
  <text x="12" y="271" font-size="11" fill="currentColor">x<tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">= 2, known</tspan></text>
  <text x="175" y="271" font-size="11" fill="currentColor" text-anchor="middle">x<tspan dy="3" font-size="10">5</tspan><tspan dy="-3" dx="3.5">= 1</tspan></text>
  <text x="199.9" y="221" font-size="11" fill="currentColor" fill-opacity="0.85">forward: one jump, no chain</text>
  <line x1="181" y1="252" x2="277" y2="252" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD6e)"/>
  <rect x="279" y="233" width="269" height="38" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="413.5" y="248" font-size="11" fill="currentColor" text-anchor="middle">loss: predict ε = −1 from (x<tspan dy="3" font-size="10">5</tspan><tspan dy="-3">, 5)</tspan></text>
  <text x="436.3" y="265" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">the network gives</text>
  <text x="443" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">ε</text>
  <text x="449.6" y="265" font-size="11" fill="currentColor" fill-opacity="0.85">= −0.8</text>
  <path d="M 440.3 258.9 L 443 256.9 L 445.6 258.9" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round" stroke-opacity="0.85"/>
  <text x="12" y="302" font-size="11" fill="currentColor" fill-opacity="0.85">reverse: a loop with a counter N</text>
  <text x="548" y="302" font-size="11" fill="currentColor" text-anchor="end">x<tspan dy="3" font-size="10">20</tspan><tspan dy="-3">: no x</tspan><tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">behind it</tspan></text>
  <line x1="508" y1="324" x2="408" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6e)"/>
  <line x1="395" y1="324" x2="295" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6e)"/>
  <line x1="282" y1="324" x2="182" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6e)"/>
  <line x1="169" y1="324" x2="69" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6e)"/>
  <circle cx="514" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="514" y="343" font-size="11" fill="currentColor" text-anchor="middle">−0.579796</text>
  <circle cx="401" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="401" y="343" font-size="11" fill="currentColor" text-anchor="middle">−0.325130</text>
  <circle cx="288" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="288" y="343" font-size="11" fill="currentColor" text-anchor="middle">0.102951</text>
  <circle cx="175" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="175" y="343" font-size="11" fill="currentColor" text-anchor="middle">0.683880</text>
  <circle cx="62" cy="324" r="4.5" stroke="none" fill="currentColor"/>
  <text x="15.2" y="343" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">x</text>
  <text x="18.5" y="343" font-size="11" fill="currentColor" font-weight="bold"><tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">= 1.85</tspan></text>
  <path d="M 12.6 336.9 L 15.2 334.9 L 17.9 336.9" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round"/>
  <text x="12" y="359" font-size="11" fill="currentColor" fill-opacity="0.85">error 0.15 = 0.2 × 0.75</text>
  <text x="340" y="368" font-size="11" fill="currentColor" text-anchor="middle">× N, one network call per hop · N = 4 here: 4 × 5 ms = 20 ms</text>
  <line x1="62" y1="152.4" x2="62" y2="159.9" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="177.6" x2="62" y2="182.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="215.4" x2="62" y2="259.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="279.4" x2="62" y2="290.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="307.4" x2="62" y2="330.9" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="152.4" x2="175" y2="159.9" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="177.6" x2="175" y2="182.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="215.4" x2="175" y2="259.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="279.4" x2="175" y2="290.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="307.4" x2="175" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="152.4" x2="288" y2="159.9" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="177.6" x2="288" y2="209.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="226.4" x2="288" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="273" x2="288" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="401" y1="152.4" x2="401" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="401" y1="273" x2="401" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="168.4" x2="514" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="273" x2="514" y2="290.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="310.4" x2="514" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
</svg>

The reverse loop drawn is §5's deterministic sampler at $N=4$, whose last estimate is the one-shot $1.85$ — not the worked case's single ancestral step, whose mean $\mu_4=1.180159$ takes the catalog $x_5=1$ down one level.

Four things the drawing has to get right.
**The forward path is one arrow, not a chain.** Training never walks down the levels; it samples a level and jumps there in closed form. Drawing a chain there is claiming a cost the training loop does not pay.
**The reverse path is a loop with a counter on it.** Write $N$ on the loop. That counter is the only quantity §5 varies and the only one the latency budget sees.
**The two paths do not share a starting point.** The forward path starts at a known $x_0$; the reverse starts where no $x_0$ exists. Every confusion about "why can't it just do one step" is that arrow drawn wrongly.
**Label the levels, not the times.** Put $\sqrt{\bar\alpha_i}$ and $\sqrt{1-\bar\alpha_i}$ on the arrows rather than $t$. The schedule, not the index, is what the arithmetic uses, and two papers with the same $T$ can have completely different schedules.

### Worked case · 대상으로 한 번 끝까지

This is the homework object. The problem set will ask you to draw it, take one denoising step by hand, and sweep the step count. Do all three here first, on the catalog numbers.

**The schedule at the catalog level.** The level index is $i=5$ of $T=20$, since $\sqrt{\bar\alpha_5}=1-0.8(5/20)=0.8$ and therefore $\bar\alpha_5=0.64$. The neighbouring level is $\sqrt{\bar\alpha_4}=0.84$, $\bar\alpha_4=0.7056$, so the per-step coefficients are

$$\alpha_5=\frac{\bar\alpha_5}{\bar\alpha_4}=\frac{0.64}{0.7056}=\Big(\frac{20}{21}\Big)^2=0.907029,\qquad \beta_5=1-\alpha_5=\frac{41}{441}=0.092971.$$

**One DDPM denoising step, all of it.** The ancestral step's mean is

$$\mu_{4}=\frac{1}{\sqrt{\alpha_t}}\Big(x_t-\frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\,\hat\epsilon\Big)=\frac{21}{20}\Big(1-\frac{0.092971}{0.6}(-0.8)\Big)=1.05\times1.123961=1.180159,$$

using the network's $\hat\epsilon=-0.8$. With the exact $\hat\epsilon=-1$ the same formula gives $1.212698$, which is also what the posterior-from-$x_0$ form gives, $\frac{\sqrt{\bar\alpha_4}\beta_5}{1-\bar\alpha_5}x_0+\frac{\sqrt{\alpha_5}(1-\bar\alpha_4)}{1-\bar\alpha_5}x_t=0.433862+0.778836=1.212698$ — the two forms agree, which is the check that the step was taken correctly. The step's variance is $\tilde\beta_5=\frac{1-\bar\alpha_4}{1-\bar\alpha_5}\beta_5=0.076029$, a standard deviation of $0.275734$. Note the size of that against the $0.0325$ the biased $\hat\epsilon$ cost: on this object the sampler's own injected noise is eight times the model's error, so a single trajectory tells you almost nothing about the model, which is why samplers are compared over many draws or run deterministically.

**The error amplification, which is the whole of §5 in one factor.** Solving the forward equation for $x_0$ turns an error in $\hat\epsilon$ into an error in $\hat x_0$ scaled by

$$\frac{\partial\hat x_0}{\partial\hat\epsilon}=-\frac{\sqrt{1-\bar\alpha_i}}{\sqrt{\bar\alpha_i}}=-\frac{1}{\sqrt{\mathrm{SNR}_i}},\qquad \mathrm{SNR}_i=\frac{\bar\alpha_i}{1-\bar\alpha_i},$$

so the same network error is harmless at a clean level and ruinous at a noisy one, because at $i=20$ there is only $20\%$ signal for the $98\%$ noise to be divided by. Numerically: $\mathrm{SNR}_5=1.7778$ and the factor is $0.75$; $\mathrm{SNR}_{20}=0.041667$ and the factor is $4.899$. The same $b=0.2$ therefore costs $0.15$ of $\hat x_0$ at the catalog level and $0.98$ at the noisiest — half the datum.

**The one-shot estimate.** At the catalog level, $\hat x_0=(x_t-\sqrt{1-\bar\alpha_t}\hat\epsilon)/\sqrt{\bar\alpha_t}=(1-0.6(-0.8))/0.8=1.85$, an error of $0.15=0.2\times0.75$, exactly the factor above. §5 shows that this single number is the $N=4$ row of a whole sweep.

### 1. Training target and sampling process are different

The common noise-prediction loss is

$$L=\mathbb E_{x_0,\epsilon,t}\|\epsilon-\epsilon_\theta(x_t,t,c)\|^2.$$

During training, $x_t$ is produced directly from $x_0$ at a sampled time. During generation, there is no $x_0$: start from noise and integrate or step backward repeatedly. A paper's parameterization may predict noise, clean data, score, velocity, or a flow vector; translate it before comparing objectives.

Those two sentences name two different objects, and almost every confusion about diffusion is the two being given one name.

> **Forward process, defined.** The **forward process** is a *fixed, known corruption* — a family of conditional distributions $q(x_i\mid x_0)$ indexed by a level — with no learned parameters in it at all. Three defining conditions. It is **specified in advance** by the schedule, so nothing about it is fit to data and two runs with the same schedule corrupt identically. It admits a **closed form at any level given $x_0$**, so training jumps straight to a sampled level rather than iterating. And it is **variance-preserving in the sense declared by its schedule**: the signal is scaled by $\sqrt{\bar\alpha_i}$ while noise of scale $\sqrt{1-\bar\alpha_i}$ is added, so the two coefficients are tied and only one of them is free.
>
> $$q(x_i\mid x_0)=\mathcal N\big(\sqrt{\bar\alpha_i}\,x_0,\ (1-\bar\alpha_i)I\big),\qquad x_i=\sqrt{\bar\alpha_i}\,x_0+\sqrt{1-\bar\alpha_i}\,\epsilon,\ \epsilon\sim\mathcal N(0,I)$$
>
> where $\bar\alpha_i\in(0,1]$ is the schedule's cumulative signal fraction and $\epsilon$ the noise draw — and the second equality is the first one written as a sampler, which is why the whole training loop is two lines of arithmetic.
>
> - **Example**: D6 at $i=5$. $0.8(2)+0.6(-1)=1$, one multiplication and one addition, and the label $\epsilon=-1$ is known because it was drawn rather than inferred.
> - **Non-example**: the *reverse* chain run in the corrupting direction one level at a time. It reaches the same distribution but costs $i$ steps instead of one, and using it in a training loop is a common way to make a correct implementation 20 times slower than it needs to be.
> - **Non-example**: data augmentation that adds noise of a fixed size. It has no level index and no $\bar\alpha$, so nothing in it tells the network *how much* signal is left, and the network cannot learn a level-dependent denoiser from it.
> - **Why it matters**: because the forward process is known and closed-form, the training loss is a plain regression with a free label — that is the entire reason the method trains stably at scale, and it is also why the loss says nothing about sampling, which is the other object.

Read as a generative model, this makes diffusion a latent-variable model whose encoder — the forward process — is fixed in advance rather than learned, which is how [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs §9]] sets it beside the VAE.

> **Reverse process, defined.** The **reverse process** is a *sampler*: a rule for producing $x_{i-1}$ from $x_i$ using the learned network, iterated from a noisy start down to a clean sample. Three defining conditions. It **begins without $x_0$**, so there is no label anywhere in it. It uses the network **once per level it visits**, which makes the number of levels visited, $N$, the unit of cost. And it is **a choice, not a consequence**: the same trained network supports a stochastic ancestral sampler, a deterministic DDIM-style sampler, and higher-order ODE solvers, which differ in output at the same $N$.
>
> $$x_{i-1}=\frac{1}{\sqrt{\alpha_i}}\Big(x_i-\frac{1-\alpha_i}{\sqrt{1-\bar\alpha_i}}\,\epsilon_\theta(x_i,i)\Big)+\sigma_i z,\qquad z\sim\mathcal N(0,I)$$
>
> where $\alpha_i=\bar\alpha_i/\bar\alpha_{i-1}$ is the per-level signal fraction and $\sigma_i$ the sampler's injected noise, zero for a deterministic sampler — so setting $\sigma_i=0$ changes the algorithm and not the model, which is why sampler and model must be reported as two separate facts.
>
> - **Example**: the worked case's single step, $1\to1.180159$ in mean, with $\sigma_5=\sqrt{0.076029}=0.275734$ if the ancestral variance is used.
> - **Non-example**: the one-shot $\hat x_0=(x_i-\sqrt{1-\bar\alpha_i}\hat\epsilon)/\sqrt{\bar\alpha_i}$. That is an *estimator* of $x_0$ computed inside a step, not a sampler; §5's $N=1$ row is what happens when it is used as one.
> - **Non-example**: the training loss with $\epsilon$ replaced by $\epsilon_\theta$. It is a number, not a process, and no amount of it fixes a sampler that visits the wrong levels.
> - **Why it matters**: $N$ lives here and nowhere else. A paper may improve the model, the schedule, or the sampler, and only the last of the three changes the latency that §4 cares about.

Conditioning sits in the same place, and it has its own arithmetic.

> **Classifier-free guidance, defined.** **Classifier-free guidance** is a *sampling-time extrapolation* between two predictions of the same network — conditional and unconditional — and therefore a change to the reverse process, not to the trained weights. Three defining conditions. The network must have been **trained with the condition dropped some fraction of the time**, so that one set of weights supplies both predictions. The two predictions are **combined by extrapolation, not interpolation**: the weight on the conditional exceeds one, which is what pushes the sample *away* from the unconditional prediction. And it **costs two network evaluations per level**, so a guided sampler at $N$ levels is $2N$ calls.
>
> $$\tilde\epsilon_w(x,i)=(1+w)\,\epsilon_\theta(x,i,c)-w\,\epsilon_\theta(x,i,\varnothing)$$
>
> where $c$ is the condition, $\varnothing$ the dropped condition and $w\ge0$ the guidance weight — and $w=0$ recovers the plain conditional prediction, since the two terms collapse, which is why $w$ is reported as a number and never as "on".
>
> - **Example**: on D6, give the unconditional branch the predictor for a datum of $0$, $\epsilon_\theta(x,i,\varnothing)=x/\sqrt{1-\bar\alpha_i}$, which at the catalog level is $1/0.6=1.6667$ against the conditional $-0.8$. Then $w=0$ gives $\hat x_0=1.85$, $w=0.5$ gives $\tilde\epsilon=-2.0333$ and $\hat x_0=2.775$, and $w=1$ gives $\tilde\epsilon=-3.2667$ and $\hat x_0=3.7$. Guidance walked the estimate from $7.5\%$ below the datum to $85\%$ above it.
> - **Non-example**: training a separate classifier and differentiating it. That is classifier guidance, the method this one replaced; it needs a second network trained on noisy inputs, which is the cost "classifier-free" names.
> - **Non-example**: turning up the conditioning weight inside the network, or sharpening a softmax over conditions. Those change the model's prediction; guidance leaves each prediction intact and moves along the line between them.
> - **Why it matters**: the D6 numbers show the failure mode before any image does. Guidance is an extrapolation, so past some $w$ it leaves the data manifold entirely — over-saturation in images, out-of-range actions in a policy — and it doubles the call count, so it competes for the same millisecond budget as the step count in §5.

### 2. One reconstruction calculation

If the model predicts $\hat\epsilon=-0.8$, estimate

$$\hat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\hat\epsilon}{\sqrt{\bar\alpha_t}}=\frac{1-0.6(-0.8)}{0.8}=1.85.$$

The residual error comes from imperfect noise prediction. This equation is an estimator, not a claim that every sampler reconstructs $x_0$ in one step.

The factor that turned $0.2$ of noise error into $0.15$ of data error is the schedule's, and the schedule is worth defining because papers quote its name instead of its numbers.

> **Noise schedule, defined.** A **noise schedule** is a *monotone map from level index to signal fraction*, $i\mapsto\bar\alpha_i$, together with the number of levels — a specification of the forward process, not a hyperparameter of the network. Three defining conditions. It is **monotonically decreasing** in $i$, from $\bar\alpha_0=1$ (clean) toward a small $\bar\alpha_T$, so "level" means something. It **determines the per-level coefficients** by division, $\alpha_i=\bar\alpha_i/\bar\alpha_{i-1}$, so a schedule fixes every $\beta_i$ and none of them is free once it is chosen. And it sets the **signal-to-noise ratio at every level**, which is the quantity the error analysis actually uses.
>
> $$\mathrm{SNR}_i=\frac{\bar\alpha_i}{1-\bar\alpha_i},\qquad\text{D6: }\ \sqrt{\bar\alpha_i}=1-0.8\,\frac{i}{20}$$
>
> where $\bar\alpha_i$ is the cumulative signal fraction at level $i$ — and this one number per level is what a comparison between two papers' schedules has to be reduced to, because $T$ alone says nothing.
>
> - **Example**: D6. $\mathrm{SNR}_5=0.64/0.36=1.7778$ so the error amplification $1/\sqrt{\mathrm{SNR}}$ is $0.75$; $\mathrm{SNR}_{20}=0.04/0.96=0.041667$ and the amplification is $4.899$. Two levels of the same schedule differ by a factor of $6.5$ in how much they punish the same network error.
> - **Non-example**: the number of training levels $T$ on its own. Two schedules with $T=1000$ can put their levels in completely different places, and only the $\bar\alpha_i$ curve says where.
> - **Non-example**: the sampler's step count $N$. It is chosen after training, from the same schedule, and §5 is the sweep over it; a paper that reports $N$ as "the schedule" has merged the two objects of §1.
> - **Why it matters**: the last level a sampler visits before it stops sets the amplification on its final estimate, so the schedule and the step count multiply. That product, not either factor, is the error in §5's table.

### 3. Diffusion and flow matching

Diffusion objectives learn quantities associated with a noisy probability path. Flow matching directly regresses the vector field of a chosen probability path. Diffusion paths can be represented within flow formulations; optimal-transport-inspired paths may be straighter, but "flow matching" does not universally mean straight or one-step generation.

> **Flow matching, defined.** **Flow matching** is a *training objective for a velocity field* along a chosen probability path — a regression target, not a sampler and not a claim about straightness. Three defining conditions. A **path between noise and data is chosen first**, and it is part of the method rather than a consequence of a noise process. The network regresses the **velocity of that path**, $u_t(x)$, rather than a noise or a score. And the target is **conditional**: the regression is against the velocity of the path conditioned on a data point, which is what makes an intractable marginal field trainable.
>
> $$L_{\mathrm{FM}}=\mathbb E_{u,x_0,\epsilon}\big\lVert v_\theta(x_u,u)-\dot x_u\big\rVert^2,\qquad\text{linear path: } x_u=(1-u)x_0+u\,\epsilon,\ \dot x_u=\epsilon-x_0$$
>
> where $u\in[0,1]$ indexes the path, $x_0$ is data and $\epsilon$ noise — and on the linear path the target is *constant along the trajectory*, which is the property that makes such paths cheap to integrate and is the real content of "straighter."
>
> - **Example**: D6 on the linear path. $\dot x_u=\epsilon-x_0=-1-2=-3$ at every $u$, and at $u=0.25$ the path is at $0.75(2)+0.25(-1)=1.25$.
> - **Non-example**: D6's own schedule at the matching level. At $u=0.25$ the variance-preserving path is at $0.8(2)+0.6(-1)=1$, not $1.25$, because its coefficients are $(0.8,0.6)$ rather than $(0.75,0.25)$ — so this page's schedule is *not* the straight path, which is the concrete version of "diffusion paths are curved in this coordinate."
> - **Non-example**: a one-step generator distilled from a diffusion model. It produces a sample in one call, but its training objective is distillation against a teacher's output, not a velocity regression, and the two have different failure modes.
> - **Why it matters**: the parameterizations translate — noise, score, clean data, and velocity are affine rearrangements of each other at a known level — so the comparison between two papers is never "diffusion versus flow." It is which path, which prediction target, and which solver, and only the first and third of those change the step count that §5 prices.

### 4. Robot policy consequences

For images, extra sampling steps cost latency. For action policies they also determine control rate and how often observations can correct a plan. Report solver, step count, action horizon, receding execution, and wall-clock latency. Fewer numerical steps are useful only if closed-loop quality is maintained.

Read [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]], DDIM, score-SDE, flow-matching, and DiT notes before [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] and $\pi_0$.

### 5. The sampler-step sweep

The model is frozen, the schedule is frozen, and the datum is frozen, so the only thing varying is $N$, the number of levels the sampler visits. The sampler is the deterministic DDIM-style update — estimate $\hat x_0$ at the current level, then re-noise to the next — started from the frozen corruption at the noisiest level, $x_{20}=0.2(2)+0.979796(-1)=-0.579796$. Latency is $N$ network calls at the declared $c=5\,\mathrm{ms}$; the 20 Hz control budget of a policy is $50\,\mathrm{ms}$.

```python
import numpy as np

T, x0, bias, c_ms = 20, 2.0, 0.2, 5.0     # D6 schedule, datum, epsilon bias, ms per call
i = np.arange(T + 1)
s = 1.0 - 0.8 * i / T                     # sqrt(alpha-bar): linear from 1.0 to 0.2
n = np.sqrt(1.0 - s ** 2)                 # sqrt(1 - alpha-bar)

def eps_model(x, k):                      # ideal predictor for the D6 datum, plus a bias
    return (x - s[k] * x0) / n[k] + bias

def ddim(N):                              # N uniform steps from i=T down to i=0
    idx = list(range(T, -1, -T // N))
    x = s[T] * x0 + n[T] * (-1.0)         # the frozen corruption at the noisiest level
    for a, b in zip(idx[:-1], idx[1:]):
        e = eps_model(x, a)
        xh = (x - n[a] * e) / s[a]        # this level's estimate of x0
        x = s[b] * xh + n[b] * e          # re-noise to the next level
    return x, idx[-2]

for N in (1, 2, 4, 5, 10, 20):
    xN, last = ddim(N)
    print(f"{N:>2} {last:>3} {xN:>9.6f} {abs(xN - x0):>9.6f} "
          f"{bias * n[last] / s[last]:>9.6f} {c_ms*N:>6.1f} {1000/(c_ms*N):>7.2f} "
          f"{c_ms * N <= 50!s:>6}")
```

| $N$ | last level $i$ | $\hat x_0$ | error | $b/\sqrt{\mathrm{SNR}_i}$ | latency (ms) | rate (Hz) | fits 20 Hz |
|---:|---:|---:|---:|---:|---:|---:|:--|
| 1 | 20 | 1.020204 | 0.979796 | 0.979796 | 5.0 | 200.00 | yes |
| 2 | 10 | 1.733333 | 0.266667 | 0.266667 | 10.0 | 100.00 | yes |
| 4 | 5 | 1.850000 | 0.150000 | 0.150000 | 20.0 | 50.00 | yes |
| 5 | 4 | 1.870813 | 0.129187 | 0.129187 | 25.0 | 40.00 | yes |
| 10 | 2 | 1.914800 | 0.085200 | 0.085200 | 50.0 | 20.00 | yes |
| 20 | 1 | 1.941667 | 0.058333 | 0.058333 | 100.0 | 10.00 | no |

Four readings.

**One step is not 4 times worse than four steps; it is 6.5 times worse.** The error falls $0.979796\to0.150000$ from $N=1$ to $N=4$, and the $N=4$ row *is* §2's $1.85$. The reason is in the fifth column: the error equals the network's constant $b=0.2$ multiplied by the amplification $1/\sqrt{\mathrm{SNR}}$ at the last level the sampler visited, and that last level is $20/N$. A sampler that stops at a noisy level is dividing a small noise error by a small signal.

**The intermediate estimates do not accumulate — only the last one survives.** Inside the $N=4$ run the estimates of $x_0$ are $1.020204$, $1.541742$, $1.733333$, $1.850000$, and the trajectory itself passes through $-0.579796$, $-0.325130$, $0.102951$, $0.683880$. Each estimate is wrong, and none of that error is carried: with a bias that does not depend on $x$, every re-noising puts the trajectory back on a line the next estimate reads correctly up to the same $b$. This is worth seeing in the loop because it is not the intuition — "more steps, more chances to go wrong" is the usual guess, and here the opposite holds for a reason the closed form makes exact.

**Returns diminish like $1/\sqrt N$, not like $1/N$.** Four times the calls, from $N=5$ to $N=20$, buys a factor of $2.2$ in error. Near the clean end $\sqrt{1-\bar\alpha}\approx\sqrt{2\times0.8\,u}$, so the amplification falls like the square root of the remaining level, and every further halving of the error costs four times the compute.

**The budget picks the row, and it is tighter than it looks.** At $c=5\,\mathrm{ms}$, a 20 Hz policy can afford $N=10$ — and that consumes the entire 50 ms period, leaving nothing for perception, the controller, or the chunk buffer of [[03-deep-learning/vla/index|4. VLA]]. The honest choice on this budget is $N=5$ at 25 ms and $0.129$ of error, or $N=4$ at 20 ms and $0.150$: the difference between those two rows is $14\%$ of the error for $5\,\mathrm{ms}$, a tenth of the period, which is the kind of trade that should be decided by a closed-loop success rate and not by a reconstruction number. And if the same policy uses classifier-free guidance, every row's latency doubles and $N=5$ becomes the last affordable one.

### After reading

Given a generative paper, identify the path, the prediction target, the conditioning and its guidance weight, the solver and its step count, and which downstream metric — not sample aesthetics alone — supports the claim. For a policy, convert the step count into milliseconds and check it against the control period before reading any success rate.

### Self-check

1. A paper halves its sampler's step count and reports unchanged FID. What has it *not* shown about a policy built on the same model?
2. On D6 at the catalog level, a second network has bias $b=-0.2$ instead of $+0.2$. What is its one-shot $\hat x_0$, and what does the pair say about reading a single reconstruction number?
3. Why is $T=20$ not a fact about how many calls generation costs?
4. The worked case's ancestral step has standard deviation $0.2757$ while the model's error contributes $0.0325$ to the same step. What follows about comparing two models on one generated sample?
5. Guidance at $w=1$ moved $\hat x_0$ from $1.85$ to $3.70$ on D6. If these were robot actions with a $\pm2.5$ joint limit, what would the sampler have produced, and which of the three conditions in the guidance definition is responsible?

> [!tip]- Answers
> 1. That the latency saved is available, or that closed-loop behaviour survived. FID is computed on a distribution of images with no clock and no feedback loop; a policy's step count sets the control rate and therefore how stale each committed action is. The evidence needed is wall-clock latency on the deployment machine and success under the same observation and action protocol — §4's list, not a distributional score.
> 2. $\hat x_0=(1-0.6(-1.2))/0.8=2.15$, an error of $+0.15$ where the first network had $-0.15$. Same magnitude, opposite sign, and a reconstruction number reported without its sign cannot distinguish a model that over-shoots from one that under-shoots — which matters the moment the output is an action with an asymmetric cost, such as a gripper closing too far.
> 3. $T$ is a property of the schedule, which belongs to the forward process; the number of calls is $N$, which belongs to the sampler and is chosen after training. D6 has $T=20$ and the table spends between 1 and 20 calls on the same trained model. A paper that reports only $T$ has reported the corruption, not the cost.
> 4. Almost nothing follows from one sample. The sampler's injected noise is $8.5$ times the size of the difference the model made, so a single draw is dominated by a quantity that is not the model. Compare models with a deterministic sampler (set $\sigma_i=0$), or over enough draws that the standard error of the statistic is below the difference being claimed.
> 5. It would have produced $2.5$ after clipping — a saturated action, indistinguishable from confidence, and silently outside the data. The responsible condition is the second: guidance *extrapolates*, with a weight on the conditional prediction greater than one, so it is designed to leave the region between the two predictions and nothing in the method bounds where it lands.

### Problem set · 과제

Tier A. Using **D6** from [[03-deep-learning/lab-objects|0. Lab Objects]], this page, and [[02-foundations/lab-kernel|0.65 Lab Kernel]]. Original object and original problems — change the knobs in §5's listing; do not rewrite the loop. State the tier in your answer sheet.

1. **Draw.** The homework diagram: the forward path as a single arrow from $x_0$ to an arbitrary level with $\sqrt{\bar\alpha_i}$ and $\sqrt{1-\bar\alpha_i}$ on it, the reverse path as a loop carrying the counter $N$, and the two starting points kept apart. Add, on the reverse loop, the one extra arrow that classifier-free guidance introduces, and write next to it what it does to the latency column of §5.
2. **Derive.** Work the same level with the noise draw flipped to $\epsilon=+1$. (a) $x_5$. (b) The one-shot $\hat x_0$ with a perfect predictor, and with this page's biased network. (c) The DDPM ancestral mean $\mu_4$ with the biased network, using the catalog $\alpha_5$ and $\beta_5$. (d) Say which of (a)–(c) changed by the same amount as the flip and which did not, and why.
3. **Do.** Fill the `?` in the patch below and re-run §5's sweep with it. The network's error now depends on the sample instead of being constant: $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+0.2\,x$, which at the catalog level still returns exactly $-0.8$ and so is indistinguishable from §5's network on the worked case. Report $\hat x_0$ and the error for $N\in\{1,2,4,5,10,20\}$, compare against §5's closed-form column, and say what this shows about the fifth column of that table.

```python
# patch to the §5 listing — fill ?, keep the rest of the loop
def eps_model(x, k):                      # same value at the catalog level, different law
    return (x - s[k] * x0) / n[k] + ?     # a bias proportional to the current sample
```

> [!tip]- Solutions
> 1. Forward: one arrow from $x_0$ to $x_i$ labelled $\sqrt{\bar\alpha_i}x_0+\sqrt{1-\bar\alpha_i}\epsilon$, feeding the loss. Reverse: a loop from $x_{20}$ through $x_i$ back into itself, labelled with $N$, ending at $\hat x_0$, and starting at a point with no $x_0$ behind it. Guidance adds a *second* evaluation of the same network with the condition dropped, whose output is combined with the first by $(1+w)\epsilon_c-w\epsilon_\varnothing$ — so the arrow doubles every entry of the latency column, and the $N=10$ row that exactly filled a 20 Hz period becomes 100 ms and does not fit.
> 2. (a) $x_5=0.8(2)+0.6(+1)=2.2$. (b) Perfect: $(2.2-0.6(1))/0.8=2$. Biased, $\hat\epsilon=1+0.2=1.2$: $(2.2-0.6(1.2))/0.8=1.85$ — the same $1.85$ as §2, because the bias is the same $0.2$ and it is amplified by the same $0.75$. (c) $\mu_4=\frac{21}{20}\big(2.2-\frac{0.092971}{0.6}(1.2)\big)=1.05\times2.014059=2.114762$. (d) $x_5$ moved by $1.2=2\times0.6$, the full flip scaled by the noise coefficient, and $\mu_4$ moved with it. The *error* in $\hat x_0$ did not move at all: it is $b/\sqrt{\mathrm{SNR}_5}=0.15$ regardless of which noise was drawn, which is why the sweep in §5 is a statement about the schedule and the network and not about the draw.
> 3. Blank: `0.2 * x`. Running it gives $\hat x_0=2.568082$, $1.827178$, $1.845251$, $1.853453$, $1.882015$, $1.909234$ for $N=1,2,4,5,10,20$, that is errors $0.568082$, $0.172822$, $0.154749$, $0.146547$, $0.117985$, $0.090766$. The closed-form column of §5 no longer predicts any of them: at $N=1$ this network is *better* than the constant-bias one ($0.568$ against $0.980$) and it overshoots past the datum, while from $N=4$ up it is worse ($0.0908$ against $0.0583$ at $N=20$), so the two curves cross. Both networks return exactly $-0.8$ at the catalog level, so the worked case cannot tell them apart; only the loop can. That is what the fifth column of §5 is really claiming — not "sampler error equals $b/\sqrt{\mathrm{SNR}}$" but "for a network whose error does not depend on its input, the intermediate errors cancel and only the last level survives." Change that assumption and the closed form goes, while the qualitative trade — more steps, less error, proportionally more latency — stays.

## 한국어

*[[02-foundations/probability|3. Probability]]의 가우시안 대수와 [[03-deep-learning/foundations/index|1. Learning Systems]]의 학습 루프 위에 선다. 대상 **D6**를 처음 쓴다.*

> [!note] 처음이라면
> 대상, 계산, §1–2, 문제 1–2를 먼저 한다. 정책이 denoising step을 줄이면 §4로, 감당할 수 있는 step 수를 찾으려면 §5로 돌아온다.

### 이 페이지의 대상 · Running object

[[03-deep-learning/lab-objects|0. Lab Objects]]의 **D6**를 그 페이지가 고정한 숫자 그대로 쓴다. $x_0=2$, $\epsilon=-1$, $\bar\alpha_t=0.64$이므로 $x_t=0.8(2)+0.6(-1)=1$이다. 학습에서는 $(x_t,t)$에서 이미 알고 있는 noise $-1$을 복원하게 할 수 있다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $x_0$ | $2$ | 깨끗한 자료 |
| $\epsilon$ | $-1$ | 이 페이지의 모든 forward 표본이 쓰는 고정된 noise |
| $T$ | $20$ | schedule의 레벨 수, $i=0$이 깨끗하고 $i=20$이 가장 시끄럽다 |
| $\sqrt{\bar\alpha_i}$ | $1-0.8\,i/T$ | 신호 계수: $1.0$에서 $0.2$까지 선형 |
| $\bar\alpha_5$ | $0.64$ | 카탈로그 레벨, 여기서 $x_t=1$ |
| $\bar\alpha_{20}$ | $0.04$ | sampler가 출발하는 가장 시끄러운 레벨 |
| $b$ | $0.2$ | 신경망의 고정된 noise 출력 오차 |
| $c$ | $5\,\mathrm{ms}$ | 배포 기계에서 신경망 1회 평가 비용(가정) |

신경망도 자료만큼 완전히 명세한다. 자료가 $x_0$였다면 $x$를 설명했을 noise에 상수를 더해 돌려준다. $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+b$다. 카탈로그 레벨에서 $-1+0.2=-0.8$이고, §2가 이미 쓰는 불완전한 예측이 정확히 이것이다. 자료뿐 아니라 *모델*까지 고정해야 §5에서 변하는 것이 sampler 하나만 남는다.

*범위: 이 페이지는 diffusion 모델을 이루는 두 과정, 예측 target을 parameterization 사이에서 번역하는 법, sampler step 수가 무엇을 치르고 무엇을 사는지를 가르친다. 손실을 정당화하는 score matching과 변분 유도는 가르치지 않는다. 그것은 [[02-foundations/probability|3. Probability]]와 [[02-foundations/information-theory|5. Information Theory]]의 밀도 추정 쪽이고, 변분 하한은 [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN]]에도 있다. 그것을 실어 나르는 architecture(U-Net, DiT)도 아니다. 그것은 [[03-deep-learning/computer-vision/index|2. Computer Vision]]이다. 뽑힌 행동을 로봇에 확정하는 법도 아니다. 그것은 [[03-deep-learning/vla/index|4. VLA]]의 chunk다.*

### 과제가 그릴 그림 · Homework diagram

레벨 집합만 공유하고 나머지는 공유하지 않는 두 경로. 과제가 요구하는 것이 정확히 이 그림이다. 그림은 계산 절이다. 위에 D6의 schedule을 그렸고, reverse 고리는 계산 절의 한 번에 끝내는 추정 $1.85$와 같은 $N=4$ 행으로 그렸다.

<svg viewBox="0 0 560 384" style="max-width:100%;height:auto" role="img" aria-label="20레벨에 걸쳐 1에서 0.2로 선형으로 줄어드는 루트 알파바와 0.979796으로 오르는 짝을 그린 D6의 schedule과, 같은 레벨 위에서 알려진 x0 = 2에서 x5 = 1로 한 번에 건너뛰어 손실로 가는 forward 경로와 x0가 없는 레벨 20에서 출발해 N = 4번 돌아 1.85에 닿는 reverse 경로">
  <defs><marker id="aD6k" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill="currentColor">(a) schedule: 시간이 아니라 레벨</text>
  <line x1="62" y1="130" x2="62" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="62" y1="36" x2="62" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="62" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <line x1="84.6" y1="130" x2="84.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="107.2" y1="130" x2="107.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="129.8" y1="130" x2="129.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="152.4" y1="130" x2="152.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="175" y1="130" x2="175" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="175" y1="36" x2="175" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="175" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">5</text>
  <line x1="197.6" y1="130" x2="197.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="220.2" y1="130" x2="220.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="242.8" y1="130" x2="242.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="265.4" y1="130" x2="265.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288" y1="130" x2="288" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="288" y1="36" x2="288" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="288" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">10</text>
  <line x1="310.6" y1="130" x2="310.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="333.2" y1="130" x2="333.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="355.8" y1="130" x2="355.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="378.4" y1="130" x2="378.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="401" y1="130" x2="401" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="401" y1="36" x2="401" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="401" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">15</text>
  <line x1="423.6" y1="130" x2="423.6" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="446.2" y1="130" x2="446.2" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="468.8" y1="130" x2="468.8" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="491.4" y1="130" x2="491.4" y2="133" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="514" y1="130" x2="514" y2="135" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="514" y1="36" x2="514" y2="130" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <text x="514" y="147" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.75">20</text>
  <text x="516" y="163" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">레벨 i</text>
  <line x1="62" y1="130" x2="514" y2="130" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="62" y1="130" x2="62" y2="34" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="58" y1="130" x2="62" y2="130" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="134" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0</text>
  <line x1="58" y1="84" x2="62" y2="84" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="88" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">0.5</text>
  <line x1="58" y1="38" x2="62" y2="38" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="55" y="42" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.75">1</text>
  <path d="M62 38 L84.6 41.7 L107.2 45.4 L129.8 49 L152.4 52.7 L175 56.4 L197.6 60.1 L220.2 63.8 L242.8 67.4 L265.4 71.1 L288 74.8 L310.6 78.5 L333.2 82.2 L355.8 85.8 L378.4 89.5 L401 93.2 L423.6 96.9 L446.2 100.6 L468.8 104.2 L491.4 107.9 L514 111.6" stroke="currentColor" stroke-width="2" fill="none" stroke-linejoin="round"/>
  <path d="M62 130 L84.6 104.2 L107.2 93.9 L129.8 86.3 L152.4 80.1 L175 74.8 L197.6 70.2 L220.2 66.2 L242.8 62.5 L265.4 59.3 L288 56.4 L310.6 53.8 L333.2 51.4 L355.8 49.3 L378.4 47.4 L401 45.7 L423.6 44.2 L446.2 42.8 L468.8 41.7 L491.4 40.7 L514 39.9" stroke="currentColor" stroke-width="2" fill="none" stroke-dasharray="6 3" stroke-linejoin="round"/>
  <circle cx="62" cy="38" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="62" cy="130" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="84.6" cy="41.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="84.6" cy="104.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="107.2" cy="45.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="107.2" cy="93.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="129.8" cy="49" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="129.8" cy="86.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="152.4" cy="52.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="152.4" cy="80.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="56.4" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="74.8" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="197.6" cy="60.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="197.6" cy="70.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="220.2" cy="63.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="220.2" cy="66.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="242.8" cy="67.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="242.8" cy="62.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="265.4" cy="71.1" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="265.4" cy="59.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="288" cy="74.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="288" cy="56.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="310.6" cy="78.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="310.6" cy="53.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="333.2" cy="82.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="333.2" cy="51.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="355.8" cy="85.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="355.8" cy="49.3" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="378.4" cy="89.5" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="378.4" cy="47.4" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="401" cy="93.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="401" cy="45.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="423.6" cy="96.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="423.6" cy="44.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="446.2" cy="100.6" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="446.2" cy="42.8" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="468.8" cy="104.2" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="468.8" cy="41.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="491.4" cy="107.9" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="491.4" cy="40.7" r="1.8" stroke="none" fill="currentColor"/>
  <circle cx="514" cy="111.6" r="3.6" stroke="none" fill="currentColor"/>
  <circle cx="514" cy="39.9" r="3.6" stroke="none" fill="currentColor"/>
  <text x="182" y="51.4" font-size="11" fill="currentColor">0.8</text>
  <text x="182" y="89.8" font-size="11" fill="currentColor">0.6</text>
  <text x="521" y="115.6" font-size="11" fill="currentColor">0.2</text>
  <text x="508" y="33.9" font-size="11" fill="currentColor" text-anchor="end">0.979796</text>
  <text x="306.1" y="124" font-size="11" fill="currentColor">√ᾱ<tspan dy="3" font-size="10">i</tspan><tspan dy="-3" dx="3.5">= 1 − 0.8 i/20</tspan></text>
  <text x="319.6" y="39" font-size="11" fill="currentColor">√(1 − ᾱ<tspan dy="3" font-size="10">i</tspan><tspan dy="-3">)</tspan></text>
  <text x="12" y="172" font-size="12" fill="currentColor">(b) 레벨만 공유하고 나머지는 공유하지 않는 두 경로</text>
  <circle cx="62" cy="252" r="4.5" stroke="none" fill="currentColor"/>
  <circle cx="175" cy="252" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <path d="M 65.0 247 Q 118.5 202 171.0 245" stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#aD6k)"/>
  <text x="118.5" y="194" font-size="11" fill="currentColor" text-anchor="middle">√ᾱ<tspan dy="3" font-size="10">5</tspan><tspan dy="-3" dx="3.5">x</tspan><tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">+ √(1 − ᾱ</tspan><tspan dy="3" font-size="10">5</tspan><tspan dy="-3">) ε</tspan></text>
  <text x="118.5" y="210" font-size="11" fill="currentColor" text-anchor="middle">= 0.8·2 + 0.6·(−1) = 1</text>
  <text x="12" y="271" font-size="11" fill="currentColor">x<tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">= 2, 알려짐</tspan></text>
  <text x="175" y="271" font-size="11" fill="currentColor" text-anchor="middle">x<tspan dy="3" font-size="10">5</tspan><tspan dy="-3" dx="3.5">= 1</tspan></text>
  <text x="199.9" y="221" font-size="11" fill="currentColor" fill-opacity="0.85">forward: 사슬이 아니라 한 번의 건너뛰기</text>
  <line x1="181" y1="252" x2="277" y2="252" stroke="currentColor" stroke-width="1.6" marker-end="url(#aD6k)"/>
  <rect x="279" y="233" width="269" height="38" rx="5" stroke="currentColor" stroke-width="1.4" fill="none"/>
  <text x="413.5" y="248" font-size="11" fill="currentColor" text-anchor="middle">손실: (x<tspan dy="3" font-size="10">5</tspan><tspan dy="-3">, 5)에서 ε = −1을 예측</tspan></text>
  <text x="390.4" y="265" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">신경망은</text>
  <text x="397.1" y="265" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.85">ε</text>
  <text x="403.7" y="265" font-size="11" fill="currentColor" fill-opacity="0.85">= −0.8을 낸다</text>
  <path d="M 394.5 258.9 L 397.1 256.9 L 399.7 258.9" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round" stroke-opacity="0.85"/>
  <text x="12" y="302" font-size="11" fill="currentColor" fill-opacity="0.85">reverse: 계수기 N이 붙은 고리</text>
  <text x="548" y="302" font-size="11" fill="currentColor" text-anchor="end">x<tspan dy="3" font-size="10">20</tspan><tspan dy="-3">: 뒤에 x</tspan><tspan dy="3" font-size="10">0</tspan><tspan dy="-3">가 없다</tspan></text>
  <line x1="508" y1="324" x2="408" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6k)"/>
  <line x1="395" y1="324" x2="295" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6k)"/>
  <line x1="282" y1="324" x2="182" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6k)"/>
  <line x1="169" y1="324" x2="69" y2="324" stroke="currentColor" stroke-width="1.8" stroke-dasharray="7 3" marker-end="url(#aD6k)"/>
  <circle cx="514" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="514" y="343" font-size="11" fill="currentColor" text-anchor="middle">−0.579796</text>
  <circle cx="401" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="401" y="343" font-size="11" fill="currentColor" text-anchor="middle">−0.325130</text>
  <circle cx="288" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="288" y="343" font-size="11" fill="currentColor" text-anchor="middle">0.102951</text>
  <circle cx="175" cy="324" r="4.5" stroke="currentColor" stroke-width="1.6" fill="none"/>
  <text x="175" y="343" font-size="11" fill="currentColor" text-anchor="middle">0.683880</text>
  <circle cx="62" cy="324" r="4.5" stroke="none" fill="currentColor"/>
  <text x="15.2" y="343" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">x</text>
  <text x="18.5" y="343" font-size="11" fill="currentColor" font-weight="bold"><tspan dy="3" font-size="10">0</tspan><tspan dy="-3" dx="3.5">= 1.85</tspan></text>
  <path d="M 12.6 336.9 L 15.2 334.9 L 17.9 336.9" stroke="currentColor" stroke-width="0.99" fill="none" stroke-linejoin="round"/>
  <text x="12" y="359" font-size="11" fill="currentColor" fill-opacity="0.85">오차 0.15 = 0.2 × 0.75</text>
  <text x="340" y="368" font-size="11" fill="currentColor" text-anchor="middle">× N, 한 칸마다 신경망 1회 · 여기서 N = 4: 4 × 5 ms = 20 ms</text>
  <line x1="62" y1="152.4" x2="62" y2="159.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="177.6" x2="62" y2="182.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="215.4" x2="62" y2="259" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="279.4" x2="62" y2="290" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="62" y1="307.4" x2="62" y2="330.9" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="152.4" x2="175" y2="159.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="177.6" x2="175" y2="182.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="215.4" x2="175" y2="259.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="175" y1="279.4" x2="175" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="152.4" x2="288" y2="159.2" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="177.6" x2="288" y2="209" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="226.4" x2="288" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="288" y1="273" x2="288" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="401" y1="152.4" x2="401" y2="209" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="401" y1="226.4" x2="401" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="401" y1="273" x2="401" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="168.4" x2="514" y2="231" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="273" x2="514" y2="290" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
  <line x1="514" y1="310.4" x2="514" y2="331.6" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.22" stroke-dasharray="2 3"/>
</svg>

그림의 reverse 고리는 계산 절의 ancestral 한 스텝(평균 $\mu_4=1.180159$, 카탈로그 $x_5=1$에서 한 레벨 아래로)이 아니라 §5의 결정론적 sampler를 $N=4$로 돌린 것이고, 그 마지막 추정이 한 번에 끝내는 $1.85$다.

그림이 맞혀야 할 것이 넷이다.
**forward 경로는 사슬이 아니라 화살표 하나다.** 학습은 레벨을 하나 뽑아 닫힌 형태로 곧장 건너뛴다. 거기에 사슬을 그리는 것은 학습 루프가 치르지 않는 비용을 주장하는 것이다.
**reverse 경로는 계수기가 붙은 고리다.** 고리 위에 $N$을 적는다. §5가 바꾸는 유일한 양이고 지연 예산이 보는 유일한 양이다.
**두 경로의 출발점은 같지 않다.** forward는 알려진 $x_0$에서 출발하고 reverse는 $x_0$가 없는 곳에서 출발한다. "왜 한 스텝으로 안 되나"라는 혼동은 전부 그 화살표를 잘못 그린 것이다.
**시간이 아니라 레벨에 이름을 붙인다.** 화살표에 $t$ 대신 $\sqrt{\bar\alpha_i}$와 $\sqrt{1-\bar\alpha_i}$를 적는다. 산수가 쓰는 것은 색인이 아니라 schedule이고, 같은 $T$를 가진 두 논문의 schedule이 전혀 다를 수 있다.

### 대상으로 한 번 끝까지 · Worked case

이것이 과제의 대상이다. 과제는 이 그림을 그리고, denoising 한 스텝을 손으로 밟고, step 수를 쓸어 보라고 한다. 카탈로그 숫자로 여기서 먼저 한다.

**카탈로그 레벨의 schedule.** $\sqrt{\bar\alpha_5}=1-0.8(5/20)=0.8$이므로 레벨 색인은 $T=20$ 중 $i=5$이고 $\bar\alpha_5=0.64$다. 이웃 레벨은 $\sqrt{\bar\alpha_4}=0.84$, $\bar\alpha_4=0.7056$이므로 레벨별 계수는 $\alpha_5=0.64/0.7056=(20/21)^2=0.907029$, $\beta_5=41/441=0.092971$이다.

**DDPM denoising 한 스텝, 전부.** ancestral 스텝의 평균은

$$\mu_{4}=\frac{1}{\sqrt{\alpha_t}}\Big(x_t-\frac{1-\alpha_t}{\sqrt{1-\bar\alpha_t}}\,\hat\epsilon\Big)=\frac{21}{20}\Big(1-\frac{0.092971}{0.6}(-0.8)\Big)=1.05\times1.123961=1.180159$$

이고 신경망의 $\hat\epsilon=-0.8$을 썼다. 정확한 $\hat\epsilon=-1$이면 같은 식이 $1.212698$을 주는데, $x_0$에서 쓴 사후 평균 형태 $\frac{\sqrt{\bar\alpha_4}\beta_5}{1-\bar\alpha_5}x_0+\frac{\sqrt{\alpha_5}(1-\bar\alpha_4)}{1-\bar\alpha_5}x_t=0.433862+0.778836=1.212698$과 같다. 두 형태가 일치하는 것이 스텝을 제대로 밟았는지의 검사다. 스텝의 분산은 $\tilde\beta_5=\frac{1-\bar\alpha_4}{1-\bar\alpha_5}\beta_5=0.076029$, 표준편차 $0.275734$다. 편향된 $\hat\epsilon$이 이 스텝에 물린 $0.0325$와 견주어 보라. 이 대상에서는 sampler가 스스로 넣는 noise가 모델 오차의 여덟 배이므로 궤적 하나로는 모델에 대해 거의 아무것도 알 수 없고, 그래서 sampler는 여러 표본으로 비교하거나 결정론적으로 돌린다.

**오차 증폭, §5 전체를 담은 인자 하나.** forward 식을 $x_0$에 대해 풀면 $\hat\epsilon$의 오차가 $\hat x_0$의 오차로 바뀌며 곱해지는 값이

$$\frac{\partial\hat x_0}{\partial\hat\epsilon}=-\frac{\sqrt{1-\bar\alpha_i}}{\sqrt{\bar\alpha_i}}=-\frac{1}{\sqrt{\mathrm{SNR}_i}},\qquad \mathrm{SNR}_i=\frac{\bar\alpha_i}{1-\bar\alpha_i}$$

이다. 그래서 같은 신경망 오차가 깨끗한 레벨에서는 해롭지 않고 시끄러운 레벨에서는 치명적이다. $i=20$에서는 $98\%$의 noise를 나눌 신호가 $20\%$뿐이기 때문이다. 숫자로는 $\mathrm{SNR}_5=1.7778$이라 인자가 $0.75$이고, $\mathrm{SNR}_{20}=0.041667$이라 인자가 $4.899$다. 같은 $b=0.2$가 카탈로그 레벨에서는 $\hat x_0$의 $0.15$를, 가장 시끄러운 레벨에서는 $0.98$ — 자료의 절반 — 을 치른다.

**한 번에 끝내는 추정.** 카탈로그 레벨에서 $\hat x_0=(1-0.6(-0.8))/0.8=1.85$, 오차 $0.15=0.2\times0.75$로 위의 인자 그대로다. §5는 이 숫자 하나가 쓸기 전체의 $N=4$ 행임을 보인다.

### 1. 학습 target과 sampling은 다르다

$L=\mathbb E\|\epsilon-\epsilon_\theta(x_t,t,c)\|^2$. 학습은 깨끗한 $x_0$에서 임의 시간의 $x_t$를 바로 만든다. 생성에는 $x_0$가 없으므로 noise에서 시작해 반복적으로 적분한다. noise·clean data·score·velocity·flow vector 중 무엇을 예측하는지 번역한 뒤 비교한다.

저 두 문장은 서로 다른 두 대상을 부르고 있고, diffusion에 대한 혼동은 거의 전부 그 둘에 이름을 하나만 준 데서 온다.

> **Forward process의 정의.** **Forward process**는 *고정되고 알려진 오염*이다. 레벨로 색인된 조건부 분포족 $q(x_i\mid x_0)$이고 학습 파라미터가 하나도 없다. 정의 조건 셋. schedule로 **미리 명세되므로** 자료에 맞춰 적합되는 부분이 없고, 같은 schedule의 두 실행이 똑같이 오염시킨다. $x_0$가 주어지면 **어느 레벨에서든 닫힌 형태**를 가지므로 학습은 반복 없이 뽑은 레벨로 곧장 건너뛴다. 그리고 **schedule이 선언한 의미에서 분산을 보존한다**. 신호에 $\sqrt{\bar\alpha_i}$를 곱하고 크기 $\sqrt{1-\bar\alpha_i}$의 noise를 더하므로 두 계수가 묶여 있고 자유로운 것은 하나뿐이다.
>
> $$q(x_i\mid x_0)=\mathcal N\big(\sqrt{\bar\alpha_i}\,x_0,\ (1-\bar\alpha_i)I\big),\qquad x_i=\sqrt{\bar\alpha_i}\,x_0+\sqrt{1-\bar\alpha_i}\,\epsilon,\ \epsilon\sim\mathcal N(0,I)$$
>
> $\bar\alpha_i\in(0,1]$은 schedule의 누적 신호 비율, $\epsilon$은 뽑은 noise다. 두 번째 등식은 첫 번째를 sampler로 쓴 것이고, 그래서 학습 루프 전체가 산수 두 줄이다.
>
> - **예**: $i=5$의 D6. $0.8(2)+0.6(-1)=1$, 곱셈 하나와 덧셈 하나. label $\epsilon=-1$을 아는 이유는 추론한 것이 아니라 뽑았기 때문이다.
> - **비예**: *reverse* 사슬을 오염 방향으로 한 레벨씩 돌리는 것. 같은 분포에 도달하지만 한 스텝 대신 $i$ 스텝이 들고, 학습 루프에서 그렇게 하면 맞는 구현을 필요보다 20배 느리게 만든다.
> - **비예**: 정해진 크기의 noise를 더하는 data augmentation. 레벨 색인도 $\bar\alpha$도 없으므로 신호가 얼마나 남았는지를 신경망에 말해 주는 것이 없고, 레벨 의존 denoiser를 배울 수 없다.
> - **왜 중요한가**: forward가 알려져 있고 닫힌 형태이므로 학습 손실이 label이 공짜인 평범한 회귀가 된다. 이것이 이 방법이 규모에서 안정적으로 학습되는 이유 전부이고, 동시에 손실이 sampling에 대해 아무 말도 하지 않는 이유다. sampling은 다른 대상이다.

생성 모델로 읽으면 diffusion 모델은 인코더 — 곧 이 forward process — 가 학습되지 않고 미리 고정된 잠재변수 모델이고, [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN §9]]가 그것을 VAE와 나란히 놓는 방식이 이것이다.

> **Reverse process의 정의.** **Reverse process**는 *sampler*다. 학습된 신경망을 써서 $x_i$에서 $x_{i-1}$을 만드는 규칙이고, 시끄러운 출발점에서 깨끗한 표본까지 반복한다. 정의 조건 셋. **$x_0$ 없이 시작하므로** 그 안에는 label이 어디에도 없다. 방문하는 **레벨마다 신경망을 한 번** 쓰므로 방문 레벨 수 $N$이 비용의 단위다. 그리고 **결과가 아니라 선택이다**. 같은 학습 가중치가 확률적 ancestral sampler, 결정론적 DDIM 계열 sampler, 고차 ODE 풀이를 모두 지원하고 같은 $N$에서 출력이 다르다.
>
> $$x_{i-1}=\frac{1}{\sqrt{\alpha_i}}\Big(x_i-\frac{1-\alpha_i}{\sqrt{1-\bar\alpha_i}}\,\epsilon_\theta(x_i,i)\Big)+\sigma_i z,\qquad z\sim\mathcal N(0,I)$$
>
> $\alpha_i=\bar\alpha_i/\bar\alpha_{i-1}$은 레벨별 신호 비율, $\sigma_i$는 sampler가 넣는 noise이고 결정론적 sampler에서는 0이다. $\sigma_i=0$으로 두는 것이 모델이 아니라 알고리즘을 바꾸는 것이므로, sampler와 모델은 별개의 사실로 보고해야 한다.
>
> - **예**: 계산 절의 한 스텝. 평균이 $1\to1.180159$이고 ancestral 분산을 쓰면 $\sigma_5=\sqrt{0.076029}=0.275734$다.
> - **비예**: 한 번에 끝내는 $\hat x_0=(x_i-\sqrt{1-\bar\alpha_i}\hat\epsilon)/\sqrt{\bar\alpha_i}$. 그것은 스텝 안에서 계산되는 $x_0$의 *추정량*이지 sampler가 아니다. §5의 $N=1$ 행이 그것을 sampler로 쓴 결과다.
> - **비예**: 손실에서 $\epsilon$을 $\epsilon_\theta$로 바꾼 것. 그것은 숫자이지 과정이 아니고, 아무리 좋아도 엉뚱한 레벨을 방문하는 sampler를 고치지 못한다.
> - **왜 중요한가**: $N$은 여기에만 산다. 논문은 모델을, schedule을, sampler를 개선할 수 있고, §4가 신경 쓰는 지연을 바꾸는 것은 그중 마지막 하나뿐이다.

조건부도 같은 자리에 있고, 자기 산수를 갖고 있다.

> **Classifier-free guidance의 정의.** **Classifier-free guidance**는 같은 신경망의 두 예측 — 조건부와 무조건부 — 사이의 *sampling 시점 외삽*이고, 따라서 학습된 가중치가 아니라 reverse process를 바꾸는 것이다. 정의 조건 셋. 신경망이 **조건을 일정 비율로 떨어뜨린 채 학습**되어 있어야 하고, 그래야 가중치 한 벌이 두 예측을 다 준다. 두 예측은 **보간이 아니라 외삽으로 결합된다**. 조건부의 가중치가 1을 넘고, 그것이 표본을 무조건부 예측에서 *멀어지게* 민다. 그리고 **레벨마다 신경망 평가가 둘** 드므로 $N$ 레벨의 guided sampler는 $2N$번 부른다.
>
> $$\tilde\epsilon_w(x,i)=(1+w)\,\epsilon_\theta(x,i,c)-w\,\epsilon_\theta(x,i,\varnothing)$$
>
> $c$는 조건, $\varnothing$은 떨어뜨린 조건, $w\ge0$은 guidance 가중치다. $w=0$이면 두 항이 접혀 평범한 조건부 예측으로 돌아오므로, $w$는 "켬"이 아니라 숫자로 보고한다.
>
> - **예**: D6에서 무조건부 가지에 자료가 $0$일 때의 예측기 $\epsilon_\theta(x,i,\varnothing)=x/\sqrt{1-\bar\alpha_i}$를 주면 카탈로그 레벨에서 $1/0.6=1.6667$이고 조건부는 $-0.8$이다. $w=0$이면 $\hat x_0=1.85$, $w=0.5$면 $\tilde\epsilon=-2.0333$에 $\hat x_0=2.775$, $w=1$이면 $\tilde\epsilon=-3.2667$에 $\hat x_0=3.7$이다. guidance가 추정을 자료보다 $7.5\%$ 아래에서 $85\%$ 위로 걸어 보냈다.
> - **비예**: 분류기를 따로 학습해 미분하는 것. 그것이 이 방법이 대체한 classifier guidance이고, 시끄러운 입력으로 학습한 두 번째 신경망이 필요하다. "classifier-free"가 가리키는 비용이 그것이다.
> - **비예**: 신경망 안에서 조건 가중치를 올리거나 조건에 대한 softmax를 날카롭게 하는 것. 그것들은 모델의 예측을 바꾼다. guidance는 각 예측을 그대로 두고 둘을 잇는 직선 위로 움직인다.
> - **왜 중요한가**: D6의 숫자가 어떤 이미지보다 먼저 실패 양상을 보여 준다. guidance는 외삽이므로 어느 $w$를 넘으면 자료 다양체를 완전히 벗어난다. 이미지에서는 과포화, 정책에서는 범위 밖 행동이다. 그리고 호출 수를 두 배로 만들어 §5의 step 수와 같은 밀리초 예산을 두고 경쟁한다.

### 2. 한 번의 복원 계산

$\hat\epsilon=-0.8$이면 $\hat x_0=(1-0.6(-0.8))/0.8=1.85$다. 오차는 noise prediction이 완벽하지 않아서 생긴다. 이 식은 estimator이지 모든 sampler가 한 step에 복원한다는 뜻이 아니다.

noise 오차 $0.2$를 자료 오차 $0.15$로 바꾼 인자는 schedule의 것이고, 논문들이 schedule의 숫자 대신 이름을 인용하므로 정의해 둘 값어치가 있다.

> **Noise schedule의 정의.** **Noise schedule**은 *레벨 색인에서 신호 비율로 가는 단조 사상* $i\mapsto\bar\alpha_i$와 레벨 개수를 함께 이르는 것이다. forward process의 명세이지 신경망의 hyperparameter가 아니다. 정의 조건 셋. $i$에 대해 **단조 감소**한다. $\bar\alpha_0=1$(깨끗)에서 작은 $\bar\alpha_T$로 가고, 그래야 "레벨"이 뜻을 갖는다. 나눗셈으로 **레벨별 계수를 결정한다**. $\alpha_i=\bar\alpha_i/\bar\alpha_{i-1}$이므로 schedule을 고르면 모든 $\beta_i$가 고정되고 자유로운 것이 없다. 그리고 **모든 레벨의 신호 대 잡음비를 정한다**. 오차 분석이 실제로 쓰는 양이 그것이다.
>
> $$\mathrm{SNR}_i=\frac{\bar\alpha_i}{1-\bar\alpha_i},\qquad\text{D6: }\ \sqrt{\bar\alpha_i}=1-0.8\,\frac{i}{20}$$
>
> $\bar\alpha_i$는 레벨 $i$의 누적 신호 비율이다. 두 논문의 schedule 비교는 결국 레벨당 이 숫자 하나로 환원해야 한다. $T$만으로는 아무 말도 되지 않기 때문이다.
>
> - **예**: D6. $\mathrm{SNR}_5=0.64/0.36=1.7778$이라 오차 증폭 $1/\sqrt{\mathrm{SNR}}$이 $0.75$이고, $\mathrm{SNR}_{20}=0.04/0.96=0.041667$이라 증폭이 $4.899$다. 같은 schedule의 두 레벨이 같은 신경망 오차를 벌하는 정도에서 $6.5$배 차이가 난다.
> - **비예**: 학습 레벨 수 $T$ 하나. $T=1000$인 두 schedule이 레벨을 전혀 다른 곳에 놓을 수 있고, 어디인지를 말하는 것은 $\bar\alpha_i$ 곡선뿐이다.
> - **비예**: sampler의 step 수 $N$. 학습이 끝난 뒤 같은 schedule에서 고르는 것이고 §5가 그것을 쓴 것이다. $N$을 "schedule"이라 보고한 논문은 §1의 두 대상을 합쳐 버린 것이다.
> - **왜 중요한가**: sampler가 멈추기 전 마지막으로 방문한 레벨이 마지막 추정의 증폭을 정하므로 schedule과 step 수가 곱해진다. §5 표의 오차는 둘 중 하나가 아니라 그 곱이다.

### 3. Diffusion과 flow matching

diffusion은 noisy probability path와 관련된 양을 학습하고, flow matching은 선택한 path의 vector field를 회귀한다. diffusion path도 flow formulation에 들어갈 수 있다. OT 계열 경로가 더 곧을 수 있지만 모든 FM이 직선·one-step인 것은 아니다.

> **Flow matching의 정의.** **Flow matching**은 선택한 확률 경로를 따르는 *속도장의 학습 목적함수*다. 회귀 target이지 sampler도 아니고 곧음에 대한 주장도 아니다. 정의 조건 셋. **noise와 자료를 잇는 경로를 먼저 고르고**, 그 경로가 noise 과정의 결과가 아니라 방법의 일부다. 신경망은 noise나 score가 아니라 **그 경로의 속도** $u_t(x)$를 회귀한다. 그리고 target이 **조건부**다. 자료점 하나에 조건부인 경로의 속도를 상대로 회귀하고, 그것이 다루기 힘든 주변 장을 학습 가능하게 만든다.
>
> $$L_{\mathrm{FM}}=\mathbb E_{u,x_0,\epsilon}\big\lVert v_\theta(x_u,u)-\dot x_u\big\rVert^2,\qquad\text{선형 경로: } x_u=(1-u)x_0+u\,\epsilon,\ \dot x_u=\epsilon-x_0$$
>
> $u\in[0,1]$이 경로를 색인하고 $x_0$는 자료, $\epsilon$은 noise다. 선형 경로에서는 target이 *궤적을 따라 상수*이고, 그런 경로가 적분하기 싼 이유이자 "더 곧다"의 실제 내용이 그것이다.
>
> - **예**: 선형 경로 위의 D6. 모든 $u$에서 $\dot x_u=\epsilon-x_0=-1-2=-3$이고, $u=0.25$에서 경로는 $0.75(2)+0.25(-1)=1.25$에 있다.
> - **비예**: 같은 레벨에서 D6 자신의 schedule. $u=0.25$에서 분산 보존 경로는 $1.25$가 아니라 $0.8(2)+0.6(-1)=1$에 있다. 계수가 $(0.75,0.25)$가 아니라 $(0.8,0.6)$이기 때문이다. 그러므로 이 페이지의 schedule은 직선 경로가 *아니고*, 그것이 "diffusion 경로는 이 좌표에서 휘어 있다"의 구체판이다.
> - **비예**: diffusion 모델에서 증류한 one-step 생성기. 한 번 호출로 표본을 내놓지만 학습 목적함수가 속도 회귀가 아니라 교사 출력에 대한 증류이고, 실패 양상이 다르다.
> - **왜 중요한가**: parameterization은 서로 번역된다. 알려진 레벨에서 noise·score·clean data·velocity는 서로의 아핀 재배열이다. 그래서 두 논문의 비교는 결코 "diffusion 대 flow"가 아니다. 어떤 경로, 어떤 예측 target, 어떤 solver인지이고, 그중 §5가 값을 매기는 step 수를 바꾸는 것은 첫째와 셋째뿐이다.

### 4. 로봇 정책에서의 결과

sampling step은 latency·control rate·재관측 주기를 바꾼다. solver·step 수·action horizon·receding execution·실제 시간을 보고해야 한다.

### 5. Sampler step 쓸기

모델이 고정이고 schedule이 고정이고 자료가 고정이므로 변하는 것은 sampler가 방문하는 레벨 수 $N$뿐이다. sampler는 결정론적 DDIM 계열 갱신 — 현재 레벨에서 $\hat x_0$을 추정하고 다음 레벨로 다시 오염 — 이고, 가장 시끄러운 레벨의 고정된 오염 $x_{20}=0.2(2)+0.979796(-1)=-0.579796$에서 출발한다. 지연은 선언한 $c=5\,\mathrm{ms}$로 신경망 $N$회 호출이고, 정책의 20 Hz 예산은 $50\,\mathrm{ms}$다. 코드는 영어 절에 한 번만 싣는다.

| $N$ | 마지막 레벨 $i$ | $\hat x_0$ | 오차 | $b/\sqrt{\mathrm{SNR}_i}$ | 지연 (ms) | 주파수 (Hz) | 20 Hz 충족 |
|---:|---:|---:|---:|---:|---:|---:|:--|
| 1 | 20 | 1.020204 | 0.979796 | 0.979796 | 5.0 | 200.00 | 예 |
| 2 | 10 | 1.733333 | 0.266667 | 0.266667 | 10.0 | 100.00 | 예 |
| 4 | 5 | 1.850000 | 0.150000 | 0.150000 | 20.0 | 50.00 | 예 |
| 5 | 4 | 1.870813 | 0.129187 | 0.129187 | 25.0 | 40.00 | 예 |
| 10 | 2 | 1.914800 | 0.085200 | 0.085200 | 50.0 | 20.00 | 예 |
| 20 | 1 | 1.941667 | 0.058333 | 0.058333 | 100.0 | 10.00 | 아니오 |

읽는 방법 넷.

**한 스텝은 네 스텝보다 4배가 아니라 6.5배 나쁘다.** $N=1$에서 $N=4$로 가며 오차가 $0.979796\to0.150000$으로 떨어지고, $N=4$ 행이 곧 §2의 $1.85$다. 이유는 다섯째 열에 있다. 오차는 신경망의 상수 $b=0.2$에 sampler가 마지막으로 방문한 레벨의 증폭 $1/\sqrt{\mathrm{SNR}}$을 곱한 값이고, 그 마지막 레벨이 $20/N$이다. 시끄러운 레벨에서 멈춘 sampler는 작은 noise 오차를 작은 신호로 나누고 있다.

**중간 추정은 누적되지 않는다. 마지막 것만 살아남는다.** $N=4$ 실행 안에서 $x_0$ 추정은 $1.020204$, $1.541742$, $1.733333$, $1.850000$이고 궤적 자신은 $-0.579796$, $-0.325130$, $0.102951$, $0.683880$을 지난다. 추정마다 틀렸는데 그 오차가 하나도 실려 오지 않는다. $x$에 의존하지 않는 편향이면 다시 오염할 때마다 궤적이 다음 추정이 같은 $b$까지 정확히 읽는 직선 위로 되돌아가기 때문이다. 루프로 봐야 하는 이유가 이것이다. "스텝이 많을수록 틀릴 기회도 많다"가 보통의 추측인데 여기서는 반대가 성립하고, 그 이유를 닫힌 형태가 정확히 말해 준다.

**수확 체감은 $1/N$이 아니라 $1/\sqrt N$이다.** $N=5$에서 $N=20$으로 호출을 네 배 늘려 오차에서 $2.2$배를 산다. 깨끗한 쪽 끝에서 $\sqrt{1-\bar\alpha}\approx\sqrt{2\times0.8\,u}$이므로 증폭이 남은 레벨의 제곱근으로 떨어지고, 오차를 다시 절반으로 만들 때마다 계산이 네 배 든다.

**예산이 행을 고르고, 보기보다 빡빡하다.** $c=5\,\mathrm{ms}$에서 20 Hz 정책이 감당하는 것은 $N=10$이고, 그것이 50 ms 주기를 통째로 먹어 지각에도 제어기에도 [[03-deep-learning/vla/index|4. VLA]]의 chunk 버퍼에도 남기는 것이 없다. 이 예산에서 정직한 선택은 25 ms에 오차 $0.129$인 $N=5$이거나 20 ms에 $0.150$인 $N=4$다. 두 행의 차이는 주기의 십분의 일인 $5\,\mathrm{ms}$를 주고 오차의 $14\%$를 사는 것인데, 복원 숫자가 아니라 폐루프 성공률로 정해야 할 종류의 거래다. 그리고 같은 정책이 classifier-free guidance를 쓰면 모든 행의 지연이 두 배가 되고 $N=5$가 마지막으로 감당 가능한 행이 된다.

### 읽고 나면

생성 논문 하나에서 경로·예측 target·조건과 guidance 가중치·solver와 step 수를 짚고, sample의 미관이 아니라 어떤 downstream metric이 주장을 받치는지 말할 수 있다. 정책이라면 step 수를 밀리초로 바꿔 제어 주기와 견준 뒤에 success rate를 읽는다.

### 스스로 점검

1. 어떤 논문이 sampler step 수를 절반으로 줄이고 FID가 그대로라고 보고했다. 같은 모델 위에 세운 정책에 대해 *보이지 않은* 것은 무엇인가?
2. 카탈로그 레벨의 D6에서 두 번째 신경망의 편향이 $+0.2$가 아니라 $b=-0.2$다. 한 번에 끝내는 $\hat x_0$은 얼마이고, 이 쌍은 복원 숫자 하나를 읽는 일에 대해 무엇을 말하는가?
3. $T=20$이 생성 호출 수에 대한 사실이 아닌 이유는?
4. 계산 절의 ancestral 스텝은 표준편차가 $0.2757$인데 모델 오차가 같은 스텝에 기여하는 것은 $0.0325$다. 생성된 표본 하나로 두 모델을 비교하는 일에 대해 무엇이 따라 나오는가?
5. D6에서 $w=1$의 guidance가 $\hat x_0$을 $1.85$에서 $3.70$으로 옮겼다. 이것이 관절 한계 $\pm2.5$인 로봇 행동이었다면 sampler는 무엇을 내놓았겠고, guidance 정의의 세 조건 중 무엇이 그 책임인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 아낀 지연을 실제로 쓸 수 있다는 것, 그리고 폐루프 거동이 살아남았다는 것이다. FID는 시계도 되먹임도 없는 이미지 분포에서 계산된다. 정책의 step 수는 제어 주기를 정하고 따라서 확정된 행동이 얼마나 묵었는지를 정한다. 필요한 증거는 배포 기계의 실제 시간 지연과 같은 관측·행동 protocol 아래의 성공률이다. §4의 목록이지 분포 점수가 아니다.
> 2. $\hat x_0=(1-0.6(-1.2))/0.8=2.15$로, 첫 신경망이 $-0.15$였던 자리에서 $+0.15$다. 크기가 같고 부호가 반대다. 부호 없이 보고된 복원 숫자는 넘치는 모델과 모자라는 모델을 구분하지 못하고, 출력이 비대칭 비용을 가진 행동 — 예를 들어 너무 많이 닫히는 gripper — 인 순간 그 구분이 중요해진다.
> 3. $T$는 schedule의 성질이고 schedule은 forward process에 속한다. 호출 수는 $N$이고 sampler에 속하며 학습이 끝난 뒤에 고른다. D6의 $T$는 20이고 표는 같은 학습 모델에 1회에서 20회까지 쓴다. $T$만 보고한 논문은 비용이 아니라 오염을 보고한 것이다.
> 4. 표본 하나에서 따라 나오는 것은 거의 없다. sampler가 넣는 noise가 모델이 만든 차이의 $8.5$배라서 한 번 뽑기는 모델이 아닌 양이 지배한다. 결정론적 sampler로 비교하거나($\sigma_i=0$), 통계량의 표준오차가 주장하는 차이 아래로 내려갈 만큼 여러 번 뽑아 비교한다.
> 5. 클리핑 뒤 $2.5$를 내놓았을 것이다. 포화된 행동이고, 확신과 구분되지 않으며, 조용히 자료 밖이다. 책임은 둘째 조건이다. guidance는 조건부 예측에 1보다 큰 가중치를 주는 *외삽*이므로 두 예측 사이 영역을 벗어나도록 설계돼 있고, 어디에 떨어질지를 묶는 장치가 방법 안에 없다.

### 과제 · Problem set

Tier A. [[03-deep-learning/lab-objects|0. Lab Objects]]의 **D6**, 이 페이지, [[02-foundations/lab-kernel|0.65 Lab Kernel]]. 영어 절 §5의 손잡이를 바꿔라. 루프를 다시 쓰지 마라. 답안에 tier를 명시하라.

1. **그리기.** 과제 그림. forward 경로는 $x_0$에서 임의 레벨로 가는 화살표 하나로, 위에 $\sqrt{\bar\alpha_i}$와 $\sqrt{1-\bar\alpha_i}$를 적는다. reverse 경로는 계수기 $N$을 단 고리로 그리고, 두 출발점을 떼어 놓는다. reverse 고리에 classifier-free guidance가 더하는 화살표 하나를 그리고, 그것이 §5의 지연 열에 무엇을 하는지 옆에 적는다.
2. **유도.** 같은 레벨에서 noise를 $\epsilon=+1$로 뒤집어 계산한다. (a) $x_5$. (b) 완벽한 예측기의 한 번에 끝내는 $\hat x_0$과 이 페이지의 편향된 신경망의 것. (c) 카탈로그 $\alpha_5$, $\beta_5$로 편향된 신경망의 DDPM ancestral 평균 $\mu_4$. (d) (a)–(c) 중 뒤집은 만큼 바뀐 것과 바뀌지 않은 것을 가르고 이유를 말한다.
3. **실행.** 영어 절 패치의 `?`를 채우고 §5의 쓸기를 다시 돌린다. 신경망 오차가 상수가 아니라 표본에 의존한다. $\epsilon_\theta(x,i)=(x-\sqrt{\bar\alpha_i}x_0)/\sqrt{1-\bar\alpha_i}+0.2\,x$이고, 카탈로그 레벨에서는 여전히 정확히 $-0.8$을 돌려주므로 계산 절만으로는 §5의 신경망과 구분되지 않는다. $N\in\{1,2,4,5,10,20\}$의 $\hat x_0$과 오차를 보고하고 §5의 닫힌 형태 열과 비교한 뒤, 그 표의 다섯째 열에 대해 무엇을 보이는지 말한다.

> [!tip]- 정답 · Solutions
> 1. forward는 $x_0$에서 $x_i$로 가는 화살표 하나에 $\sqrt{\bar\alpha_i}x_0+\sqrt{1-\bar\alpha_i}\epsilon$을 적고 손실로 들어간다. reverse는 $x_{20}$에서 $x_i$를 거쳐 자신으로 돌아오는 고리에 $N$을 적고 $\hat x_0$에서 끝나며, 뒤에 $x_0$가 없는 점에서 시작한다. guidance는 조건을 떨어뜨린 같은 신경망의 *두 번째* 평가를 더하고 그 출력을 $(1+w)\epsilon_c-w\epsilon_\varnothing$으로 첫 번째와 결합한다. 그래서 그 화살표가 지연 열의 모든 항을 두 배로 만들고, 20 Hz 주기를 정확히 채우던 $N=10$ 행이 100 ms가 되어 들어가지 못한다.
> 2. (a) $x_5=0.8(2)+0.6(+1)=2.2$. (b) 완벽하면 $(2.2-0.6(1))/0.8=2$. 편향되면 $\hat\epsilon=1+0.2=1.2$이므로 $(2.2-0.6(1.2))/0.8=1.85$로 §2와 같은 $1.85$다. 편향이 같은 $0.2$이고 같은 $0.75$로 증폭되기 때문이다. (c) $\mu_4=\frac{21}{20}\big(2.2-\frac{0.092971}{0.6}(1.2)\big)=1.05\times2.014059=2.114762$. (d) $x_5$는 $1.2=2\times0.6$만큼, 즉 뒤집은 전부에 noise 계수를 곱한 만큼 움직였고 $\mu_4$도 따라 움직였다. $\hat x_0$의 *오차*는 전혀 움직이지 않았다. 어느 noise를 뽑았든 $b/\sqrt{\mathrm{SNR}_5}=0.15$이고, 그래서 §5의 쓸기가 뽑기에 대한 진술이 아니라 schedule과 신경망에 대한 진술이다.
> 3. 빈칸은 `0.2 * x`다. 돌려 보면 $N=1,2,4,5,10,20$에서 $\hat x_0$이 $2.568082$, $1.827178$, $1.845251$, $1.853453$, $1.882015$, $1.909234$, 즉 오차가 $0.568082$, $0.172822$, $0.154749$, $0.146547$, $0.117985$, $0.090766$이다. §5의 닫힌 형태 열은 이 중 어느 것도 예측하지 못한다. $N=1$에서는 이 신경망이 상수 편향 쪽보다 *낫고*($0.568$ 대 $0.980$) 자료를 넘어 과하게 가며, $N=4$부터는 나쁘다($N=20$에서 $0.0908$ 대 $0.0583$). 두 곡선이 교차한다. 두 신경망 모두 카탈로그 레벨에서 정확히 $-0.8$을 돌려주므로 계산 절로는 구분할 수 없고 루프만이 구분한다. §5의 다섯째 열이 실제로 주장하는 것이 그것이다. "sampler 오차는 $b/\sqrt{\mathrm{SNR}}$이다"가 아니라 "입력에 의존하지 않는 오차를 가진 신경망에서는 중간 오차가 상쇄되고 마지막 레벨만 살아남는다"이다. 그 가정을 바꾸면 닫힌 형태는 사라지고, 질적 거래 — 스텝이 많을수록 오차가 줄고 지연이 비례해 는다 — 는 남는다.
