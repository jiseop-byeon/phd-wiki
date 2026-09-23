---
title: 3. Deep Learning
study-depth: Literacy
depth-goal: "Use the map to locate a method historically and explain how neighboring research streams connect."
mastery-when: "Raise the specific downstream method pages—not the whole map—to Working or Mastery."
---

## English

Map of content for deep learning. Goal: solid foundations first, then track the frontier
(physical AI, world models, diffusion) through papers from prestigious venues
(NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, CoRL, RSS, ICRA).

### Maps

- [[03-deep-learning/lineage|1. Paper Lineage]] — the one-page big picture + per-era diagrams
- [[03-deep-learning/physical-ai-ecosystem|2. Physical AI Ecosystem]] — who builds what, mapped to the papers

### Subareas

Start with [[03-deep-learning/lab-objects|0. Deep-Learning Lab Objects]]. The six course modules reuse those fixed objects so that representations, objectives, and evidence can be compared rather than relearned from scratch.

1. [[03-deep-learning/foundations/index|Learning Systems]] — tensors, logits, loss, updates, data splits, recipes and scaling claims
   - [[03-deep-learning/foundations/sequence-models|1.1 Sequence Models]] — the recurrent network and backpropagation through time, vanishing and exploding gradients, the LSTM and GRU, linear state-space models (S4, Mamba), and linear attention, the delta rule and the attention hybrids of 2025, on D5
   - [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]] — scaled dot-product attention, masks, heads, position, the block and its cost, and the mixture-of-experts sublayer, on D2's patch tokens
   - [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale]] — initialization, normalization and residual paths as variance budgets, mixed precision, memory and compute per parameter, compute-optimal allocation and LoRA, and fp8 and fp4 precision for inference on the robot, on D1, a twenty-layer MLP and an illustrative 100M-parameter Transformer
   - [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing for Robot Learning]] — the CUDA execution model, coalescing, arithmetic intensity and the roofline, batching across parallel environments, reading a CUDA kernel, profiling and host–device synchronization, and deployment on Jetson, on a policy MLP and a course GPU
2. [[03-deep-learning/computer-vision/index|Computer Vision]] — convolution and patch tokens; classification, detection, segmentation, depth and 3D outputs
3. [[03-deep-learning/vlm/index|Vision–Language Models]] — dual encoders, fusion, generation, contrastive batches and grounding, and where modalities meet, up to omni-modal models
4. [[03-deep-learning/vla/index|Vision–Language–Action]] — action representations, behavior cloning, chunking, control interfaces and evidence; token and denoiser action heads, the embodiment gap, and in-context imitation
5. [[03-deep-learning/world-models/index|World Models]] — latent state, transition, reward, rollout error, planning and model exploitation, and the renderers, simulators and planners all called world models
6. [[03-deep-learning/diffusion/index|Diffusion & Flow]] — noising, denoising targets, flow fields, samplers and policy latency
   - [[03-deep-learning/diffusion/vae-gan|6.1 VAEs & GANs]] — the ELBO and the reparameterization gradient, the linear VAE and posterior collapse, the GAN game, its saturation and mode collapse, and the VQ-VAE's discrete codes; the prerequisite lecture for 6, on D6 widened into a distribution

These are **engineering bridge courses**: each names an object, works one calculation, gives a problem set, and states an exit test. They make the canonical papers readable and usable; the [[01-canonical-papers/canonical-list|canonical paper list]] supplies historical depth and primary evidence. Completing a module to Working does not promote the whole field to Mastery.

### Cumulative problem set · 누적 과제

Tier B. Three hand problems on the objects of [[03-deep-learning/lab-objects|0. Lab Objects]], each crossing two of them and each a variant of something a module already works. Do them after the modules, not instead of their problem sets. No new code.

1. **D1 into D2: the softmax that classifies is the softmax that attends.** Take D1 from [[03-deep-learning/foundations/index|1. Learning Systems]] and head 1 of [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]] on D2's tokens, with token 1 as the query: raw scores $(0,2,-2,0)$ against keys 1–4, divided by $\kappa$ before the softmax, where keys 2 and 4 are the bright patches.
   - **Draw.** D1's forward pass as far as the loss, shapes $2\to3\to2$, with the softmax and the cross-entropy as one block and $p-y$ leaving it; beside it, token 1's attention row — four scores, the division by $\kappa$, one softmax over four keys — with keys 2 and 4 bracketed as bright. Under each softmax, write what it normalises over.
   - **Derive.** (a) Show that a two-class softmax is $\sigma(s_1-s_2)$, and give D1's $p$, $L$ and $p-y$ when its logits are divided by $\kappa=\sqrt2$, the divisor attention uses at $d_k=2$. (b) Show that token 1's bright share $a_{12}+a_{14}$ equals $\sigma(2/\kappa)$ for every $\kappa$, and evaluate it at $\kappa=1$, $\sqrt2$ and $2$. (c) At which $\kappa$ does the bright share equal D1's catalog $p_1$, and what is its $-\ln$ there?
   - **Interpret.** Why does a four-key softmax collapse into a two-class one on D2, and which way does a larger divisor move the confidence and the size of $p-y$ in both objects? What would dividing by $d_k$ instead of $\sqrt{d_k}$ do to a head with $d_k=64$?
2. **D5 against D6: an error that is carried and an error that is replaced.** Both loops call a network once per step. D5's transition, from [[03-deep-learning/world-models/index|5. World Models]], feeds its own output back in; D6's sampler, from [[03-deep-learning/diffusion/index|6. Diffusion & Flow]], re-estimates $x_0$ at every level it visits.
   - **Draw.** Two strips over five network calls. Top: D5 free-running with the optimistic gain $\hat\lambda'=0.7$ and zero actions, each step drawn as the carried gap $\hat\lambda'\delta_t$ plus the fresh error $e_t$. Bottom: D6's $N=5$ run with $b=0.2$ over levels 20, 16, 12, 8 and 4 — five estimates of $x_0$, and an arrow to the output from the last one only.
   - **Derive.** (a) For $\hat\lambda'=0.7$: $e_t$, the closed form of $\delta_H$, $\delta_1$, $\delta_5$, the $H$ with the largest $\lvert\delta_H\rvert$, and $\delta_{10}/z_{10}$. (b) D6's five estimates in the $N=5$ run, from $\hat x_0=x_0-b\sqrt{1-\bar\alpha_i}/\sqrt{\bar\alpha_i}$ at each visited level, and the final error; then, with the network error halved to $b=0.1$, the final error at $N=1$, $5$ and $10$, and the smallest of §5's step counts that beats the catalog network's error at $N=20$.
   - **Interpret.** After five calls D5's gap is larger than its first-step error, and D6's error is smaller than its first estimate's. Why, and what one change to each loop would swap their behaviour?
3. **D3 against D4: two numbers the protocol sets.** A batch of $N$ pairs certifies at most $\log N$ nats however good the encoder ([[03-deep-learning/vlm/index|3. VLM §2]]); a chunk of $k$ actions with an inference delay of $m$ steps reacts no sooner than its next boundary ([[03-deep-learning/vla/index|4. VLA]]). Neither number is set by the model.
   - **Draw.** D3's similarity matrix at $\tau=1/2$ for the batch with pair 3 removed ($N=2$), the batch box and the diagonal marked, and beside it a loss axis carrying $\log2$, $\log3$ and both batches' $\mathcal L$. Then D4's timeline at 20 Hz with $100$ ms inference and $k=3$: the chunk boundaries every three steps, a scene change at step $n_j=21$, and the first boundary that can know about it.
   - **Derive.** (a) For $N=2$: both row losses, $\mathcal L$, and $\log N-\mathcal L$, against the full batch's $\mathcal L=0.602352$. (b) For $n_j=21$: $\ell(k)$ at $k=2$, $3$ and $4$, and the same three at the page's $n_j=20$. (c) Show that $\ell(k)$ lies between $m\Delta t$ and $(m+k-1)\Delta t$ whatever $n_j$ is.
   - **Interpret.** Removing a pair lowered the loss; moving the change by one step changed the latency. Neither touched the model. What must a paper report so that neither number can be read as a better model?

> [!tip]- Solutions
> 1. *Draw:* $x$ (2), $z$ and $h$ (3), $s$ and $p$ (2), and a scalar $L$; the attention row is scores (4) and weights (4), then the bright share (a scalar) and $o_1$ (2). D1's softmax normalises over classes, the attention row over keys. *Derive:* (a) $e^{s_1}/(e^{s_1}+e^{s_2})=1/(1+e^{-(s_1-s_2)})=\sigma(s_1-s_2)$. At $\kappa=\sqrt2$ the gap is $1/\sqrt2=0.707107$, so $p=(0.669762,\,0.330238)$, $L=0.400834$ nats and $p-y=(-0.330238,\,0.330238)$ — against $0.731059$, $0.313262$ and $\pm0.268941$ at $\kappa=1$. (b) The bright mass is $e^{2/\kappa}+1$ and the dark mass $1+e^{-2/\kappa}=e^{-2/\kappa}(e^{2/\kappa}+1)$, so their ratio is $e^{2/\kappa}$ and the share is $\sigma(2/\kappa)$: $0.880797$, $0.804430$ (the worked case's first output coordinate) and $0.731059$. (c) $\kappa=2=d_k$: the share is $\sigma(1)=0.731059$, D1's $p_1$, and $-\ln0.731059=0.313262$ nats, D1's $L$. *Interpret:* head 1 scores token 1's keys by $c_j-r_j$, and D2's bright patches are exactly its right column, so in each row the bright key outscores the dark one by $2/\kappa$ — the four keys pair up, and the row is a two-class softmax at a logit gap of $2/\kappa$. A larger divisor pushes both objects toward $1/2$ and enlarges $p-y$ ($0.268941\to0.330238$ in D1), which keeps gradients alive; a smaller one saturates. At $d_k=64$, dividing by $64$ instead of $8$ shrinks every gap eight times further and starts the head near uniform — blind, the non-example of [[03-deep-learning/foundations/attention-transformer|1.2 §2]].
> 2. *Draw:* each top step is two arrows adding, $\hat\lambda'\delta_t$ and $e_t$; the bottom strip has five estimates and one output arrow. *Derive:* (a) $e_t=(\hat\lambda'-\lambda)z_t=-0.1\cdot0.8^t$, and the page's recursion telescopes to $\delta_H=0.7^H-0.8^H$: $\delta_1=-0.1$, $\delta_5=-0.15961$, the largest $\lvert\delta_H\rvert$ at $H=4$ with $-0.1695$, and $\delta_{10}/z_{10}=0.875^{10}-1=-0.736924$ — a relative error that can never pass $-1$, where the pessimistic gain's $(9/8)^H-1$ grows without bound. (b) The estimates are $1.020204$, $1.481693$, $1.671475$, $1.784349$ and $1.870813$, and only the last survives: error $0.129187$. With $b=0.1$: $0.489898$, $0.064594$ and $0.042600$; $N=5$ still misses the catalog network's $0.058333$ at $N=20$, and $N=10$ beats it — $50$ ms instead of $100$. *Interpret:* D5's map is closed, so each step's error is multiplied by $\hat\lambda'$ and added to the next; after five calls $\lvert\delta_5\rvert/\lvert\delta_1\rvert=1.5961$, and $2.6281$ for the pessimistic gain, whose larger multiplier carries the same one-step error further. D6's error after five calls is $0.129187/0.979796=0.131851$ of its first estimate's: a constant bias re-noises the sample onto a line the next estimate reads up to the same $b$, so only the last level's amplification survives. Re-encoding a real observation at every step (teacher forcing) resets D5's gap to the fresh $e_t$; an error that depends on $x$, as in problem 3 of [[03-deep-learning/diffusion/index|6]], makes each estimate's error depend on the sample the step before left behind, so D6's errors are carried too.
> 3. *Draw:* the $2\times2$ matrix $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ with its diagonal; on the loss axis $\mathcal L_2=0.313262$ sits below $\log2=0.693147$, and $\mathcal L_3=0.602352$ below $\log3=1.098612$. On the timeline the boundaries fall at steps 21, 24 and 27, and the change at 21 is first known to the chunk that starts at step 24, whose observation is step 22. *Derive:* (a) Row 1's logits are $(2,1)$ and row 2's $(1,2)$, so each $p_{ii}=\sigma(1)=0.731059$ and each loss is $0.313262$ nats — D1's numbers, because each row is D1's logit pair with its own class on top. The columns match by symmetry, so $\mathcal L=0.313262$ and $\log2-\mathcal L=0.379885$, against the full batch's $\log3-0.602352=0.496260$. (b) With $m=\lceil0.10/0.05\rceil=2$: at $n_j=21$, $\ell=0.15$ s for all three $k$, the boundary being step 24 each time; at $n_j=20$, $0.10$, $0.20$ and $0.20$ s. One step later made $k=3$ faster and $k=2$ slower. (c) Write $n_j+m=qk+\rho$ with $0\le\rho<k$. If $\rho=0$ the boundary is $n_j+m$ itself and $\ell=m\Delta t$; otherwise it is $(q+1)k=n_j+m+(k-\rho)$ and $\ell=(m+k-\rho)\Delta t\le(m+k-1)\Delta t$ — the worst case equals the worst action age. *Interpret:* a loss needs $N$, $\tau$ and the no-information value $\log N$ beside it; a latency needs $k$, $m$, $\Delta t$ and the worst case $(m+k-1)\Delta t$, or its spread over the phase of the change, because one scene change samples one phase. A smaller batch scores lower while certifying less, and a lucky phase reacts faster without a faster policy.

### Session schedule · 학습 일정

One row is one 60–90-minute session; [[02-foundations/overview|0. Overview]] sets the unit and keeps the pacing table these counts feed. The order follows what each page stands on: 1.1 needs only 1, 1.2 reads the D2 pixels that 2. Computer Vision freezes, 1.3 stands on 1.2, and 6.1 is the prerequisite lecture for 6. A **bold** number marks a page's first pass — its object and worked case plus the sections and problems its First-pass callout names — and the bold rows alone are the Literacy pass; all rows together are the Working pass. Every page here is Tier A, so each has a lab-and-sweep session; otherwise the sizing is the robotics track's: the object and worked case open the page, the sections follow at about 1,500–2,500 words a session, and the problem set closes it.

| # | Page and sections | Activity | Check that ends the session |
|---:|---|---|---|
| **1** | [[03-deep-learning/foundations/index\|1]] object D1, diagram, worked case | first pass + worked case by hand | Forward, backward and one SGD step on D1 with the solution covered: $L=0.313262$, $p-y=(-0.268941,\,0.268941)$, and $\Delta L=-0.129177$ at $\eta=0.1$. |
| **2** | 1 §1–5, self-check, problem set 1–3 | first pass + problem set | Solutions 1–3: $17$ parameters with the biases; logits $(0,\log3)$ give $p=(1/4,\,3/4)$ and $L=1.386$; the test set became part of model selection. |
| 3 | 1 §6, problem set 4 | lab and sweep | The lab measures the step-size boundary; problem 4 reruns it with class 2 as the target and $\lambda=0.2$, starting from $L_\lambda=1.813262$. |
| **4** | [[03-deep-learning/foundations/sequence-models\|1.1]] object, diagram, worked case | first pass + worked case by hand | Two steps forward and two back on D5, five kernel taps, and the same two outputs again by convolution, with the solution covered. |
| **5** | 1.1 §1–3 | first pass | BPTT written as a product of Jacobians (§2); why the spectral radius decides vanishing or exploding (§3). |
| **6** | 1.1 problem set 1–2, self-check | problem set | Solutions 1–2 at $\hat\lambda=0.9$: $z_3=0.324$ by recurrence and by convolution; $g_3,g_2,g_1=0.324,\,0.2916,\,0.26244$. |
| 7 | 1.1 §4–8 | first pass | Clipping as a ceiling (§4); the LSTM's cell path (§5); one linear state-space model discretized by hand (§8). |
| 8 | 1.1 §9–10, §12 | first pass | What made S4 and Mamba usable as backbones (§9); sequential steps, arithmetic and memory set side by side (§10); §12's questions put to one sequence-model claim. |
| 9 | 1.1 §11, problem set 3 | lab and sweep | The horizon sweep, the recurrence–convolution check and the cell path print; with problem 3 appended, the BPTT line gives $\partial L/\partial\lambda=0.49572$. |
| 10 | 1.1 §13, self-check 7 | first pass | Two overlapping memories written by hand: added, $S=(0.4,-0.8)$ returns $0.4$ and $-0.4$; by the delta rule, $S_2=(0.04,-1.28)$ returns $-1$ exactly. Self-check 7: a $30$ s demonstration's $1.42$ GB cache, and the $0.35$ GB a 3:1 hybrid keeps. |
| **11** | [[03-deep-learning/computer-vision/index\|2]] object D2, diagram, worked case | first pass + worked case by hand | One convolution window, one output size and one IoU on D2, with the solution covered. |
| **12** | 2 §1–4, self-check, problem set 1–3 | first pass + problem set | Solutions 1–3: a $3\times3$, stride-2, padding-1 layer gives a $4\times4\times8$ output and $80$ parameters; metric depth is left unsupported. |
| 13 | 2 §5, problem set 4 | lab and sweep | The lab's formula, threshold and average reproduced; problem 4's three variants reported as tables. |
| **14** | [[03-deep-learning/foundations/attention-transformer\|1.2]] object, diagram, worked case | first pass + worked case by hand | Head 1 on D2 with the solution covered: sixteen scores, the row $(0.157323,\,0.647107,\,0.038248,\,0.157323)$ rearranged, $o_1=(0.804430,\,-0.608859)$, and the causal rows. |
| **15** | 1.2 §1–3 | first pass | Why the divisor is $\sqrt{d_k}$, in three lines (§2); a causal mask added to the scores before the softmax (§3). |
| **16** | 1.2 problem set 1–2, self-check | problem set | Solutions 1–2: head 3's grid and causal rows; $\mathrm{sd}(q\cdot k)=16$ at $d_k=64$; $872$ block parameters at $h=2$ and at $h=4$. |
| 17 | 1.2 §4–5 | first pass | Token 1's two-head output $(0.804430,\,-0.608859,\,0.195570,\,-0.608859)$ (§4); why attention needs position, and the two ways to supply it (§5). |
| 18 | 1.2 §6–7, problem set 4 | first pass + problem set | The block's parts in order (§6); problem 4: at $n=276$ and $d=4096$ the two $n\times n$ products hold about $1.1\,\%$ of the multiply-adds. |
| 19 | 1.2 §8, problem set 3 | lab and sweep | The lab matches 2(a) to six decimals; the mirror test's gap is $0.608859$ with the position table and $0$ without; the share crosses one half at $n=6d$. |
| 20 | 1.2 §9, self-check 7 | first pass | D2's four tokens routed by hand: $x_1$ gets $p=(0.269,\,0.731)$ and the dark tokens go to expert 2; the auxiliary loss is $1$ for the balanced router and $1.46$ for the collapsed one; $400$ block parameters, $252$ touched per token. Self-check 7: $160$ GB resident in bf16 against $45$ GB in NVFP4. |
| **21** | [[03-deep-learning/foundations/training-at-scale\|1.3]] object, diagram, worked case | first pass + worked case by hand | D1's variances under three initializations, and T-100M's compute, time, memory, tokens per parameter and one LoRA fraction, with the solution covered. |
| **22** | 1.3 §1, §5–6 | first pass | He and Xavier as variance budgets (§1); sixteen bytes per parameter (§5) and six FLOPs per parameter per token (§6), applied to T-100M. |
| **23** | 1.3 problem set 1–2, self-check | problem set | Solutions 1–2: the $r=8$ adapter's path beside $W_0$; He gives $\operatorname{Var}(w)=0.0078125$ for $256\to64$, keeping the forward pass and quartering the gradient's variance. |
| 24 | 1.3 §2–3 | first pass | Which axis BatchNorm and LayerNorm average over, and what changes at inference (§2); the residual stream's variance (§3). |
| 25 | 1.3 §4, §7 | first pass | The master copy and the loss scale of mixed precision (§4); the twenty-tokens-per-parameter fit and what it assumes (§7). |
| 26 | 1.3 §8–9, problem set 4 | first pass + problem set | LoRA's parameter count (§8); problem 4: full fine-tuning of the illustrative 7B model needs $112$ GB of model states, $4.7$ times the $24$ GB device. |
| 27 | 1.3 §10, problem set 3 | lab and sweep | The variance table, the residual stream, the sixteen-bit run and the budget print; problem 3's widened, deepened MLP-20 run with a fourth initialization. |
| 28 | 1.3 §11, self-check 7 | first pass | The four-weight block to fp4 by hand: scale $0.14$, each small weight off by $0.02$; then the outlier $8.4$ raises the scale to $1.4$ and stores all three as zero. The floor per token on Jetson Thor: $22.0$, $11.0$ and $6.2$ ms in bf16, fp8 and NVFP4. Self-check 7: what to measure before quantizing a $2$ Hz policy. |
| **29** | [[03-deep-learning/foundations/gpu-computing\|1.4]] object, diagram, worked case | first pass + worked case by hand | MLP-256 on G-100: $83{,}968$ weights; at $N=1$ layer 2 moves $132{,}096$ bytes for $131{,}072$ FLOPs, intensity $0.992$, memory-bound, and the whole pass takes $15.17$ µs, $98.9\%$ of it launches; at $N=4{,}096$ it takes $25.19$ µs, $6.15$ ns per environment. |
| **30** | 1.4 §1–2 | first pass | The CUDA execution model — kernel, block, grid, warp — and latency hiding (§1); a warp's fp32 load in $4$ sectors at stride 1 and $32$ at stride 8 (§2). |
| 31 | 1.4 §3–4 | first pass | The roofline with its ridge at $100$ FLOP/byte (§3); the layer caps $51.2$, $128$ and $7.76$, and layer 2 crossing the ridge at $N=457$ (§4). |
| 32 | 1.4 §5–6 | first pass | Vectorized environments and Rudin et al.'s $4{,}096$ robots (§5); the naive and tiled matrix multiplies, loading $481.9\times$ and $15.1\times$ the read-once bytes at $T=1$ and $32$ (§6). |
| 33 | 1.4 §7–8, self-check, problem set 1–2, 4 | problem set | A sync after each layer costs $25.19$ µs at $N=4{,}096$ against $15.19$ for one graph launch and $11.88$ for a fused kernel (§7); the engine built on the robot and the control budget (§8); Solutions: at $2$ TB/s the ridge falls to $50$ and $N=1$ is still $99.4\%$ launches; layer 1's cap $51.2$ stays below the ridge at any batch; a `perf_counter()` around an asynchronous call times only the launches. |
| 34 | 1.4 §9, problem set 3 | lab and sweep | The lab: the launch share falls from $98.9\%$ at $N=1$ to $27.0\%$ at $N=16{,}384$, and kernels equal launches at $N=6{,}037$; problem 3's MLP-512 variant. |
| **35** | [[03-deep-learning/vlm/index\|3]] object D3, diagram, worked case | first pass + worked case by hand | Nine dot products, row losses $(0.407606,\,0.757448,\,0.642002)$ and $\mathcal L=0.602352$ against $\log3=1.098612$, with the solution covered. |
| **36** | 3 §1–4, self-check, problem set 1–3 | first pass + problem set | Solutions 1–3: row 1 at $\tau=1/4$ is $(4,2,0)$ with $p=0.867$ and loss $0.143$; grounding in the valve pixels stays untested. |
| 37 | 3 §5, problem set 4 | lab and sweep | The temperature sweep reproduced, including the one-wrong batch's minimum at $\tau=0.1639$; problem 4's duplicate-caption variant and its losses. |
| 38 | 3 §6, self-check 6 | first pass | The four places modalities meet — at the end (CLIP, D3), through a bridge (Flamingo), in one sequence (Chameleon, Transfusion), omni-modal (GPT-4o, Qwen2.5-Omni) — and what each buys and costs. Self-check 6: what an "omni-modal" robot model must output before it is a VLA. |
| **39** | [[03-deep-learning/vla/index\|4]] object D4, diagram, worked case | first pass + worked case by hand | The chunk rebuilt from the axis rule; $m=2$, a worst age of $0.20$ s at $k=3$, and $\ell=0.20$ s against $1.00$ s at $k=20$. |
| **40** | 4 §1–3, self-check, problem set 1–2 | first pass + problem set | Solutions 1–2: a 50 Hz controller makes $m=5$ — the faster controller raised the minimum chunk — and a worst age of $0.18$ s at $k=5$, against $0.30$ s at 20 Hz. |
| 41 | 4 §4–5, problem set 3 | lab and sweep | The chunk-length sweep's latency column matches $\ell(k)$ row for row; problem 3's twice-moving target run. |
| 42 | 4 §6, self-check 7 | first pass | D4's $256$-bin step, $0.16$ mm against $2$ mm of perception jitter; the crossover at $H=5$, where denoising a chunk becomes cheaper than decoding its tokens; why a unimodal head sends $(-1,0)$ and $(1,0)$ to $(0,0)$. Self-check 7: ECoT's $7\to350$ tokens per step, and D4's $6$ passes a chunk becoming $349$. |
| 43 | 4 §7, self-check 6 | first pass | D4's normalized chunk executed on arm B, overshooting by $6$ and $3$ cm, two and a half times the intended motion; the five designs and what each pays; OXE's large-data rows, RT-1-X at $27\%$ against RT-1's $40\%$ on Bridge and the 55B RT-2-X back to $50\%$. Self-check 6: $70\%$ and $75\%$ at $100$ trials have overlapping intervals, $[0.60,\,0.78]$ and $[0.66,\,0.82]$. |
| 44 | 4 §8, self-check 8 | first pass | A twelve-second D4 demonstration as the prompt: $240$ steps and $720$ tokens before the first action; GEN-1.5's $59\%$ from one demonstration against $83\%$ after ten gradient steps. Self-check 8: which of the three conditions to check first, and the comparison that makes the number a decision. |
| **45** | [[03-deep-learning/world-models/index\|5]] object D5, diagram, worked case | first pass + worked case by hand | Returns $-1.19$ and $-1.64$; $\delta_H=0.9^H-0.8^H$, $0.26281$ at $H=5$, peaking at $H=6$ with $0.269297$. |
| **46** | 5 §1–3, self-check, problem set 1–2 | first pass + problem set | Solutions 1–2 at $\hat\lambda=0.85$: $e_t=0.05\cdot0.8^t$, $\delta_H=0.85^H-0.8^H$, $\delta_5=0.116025$. |
| 47 | 5 §4–5, problem set 3 | lab and sweep | The horizon sweep reproduced; problem 3's mis-learned action gain gives regret $0.0000$, $0.0325$, $0.0693$, $0.0929$ for $H=2$–$5$. |
| 48 | 5 §6, self-check 6 | first pass | D5's map $f(z,a)=0.8z+0.5a$ placed as a simulator and §5's enumeration as a planner; the three functions told apart by what they output, and what each gives a manipulator. Self-check 6: the phone-video site scene placed, and what it still lacks for seating a panel. |
| **49** | [[03-deep-learning/diffusion/vae-gan\|6.1]] object, diagram, worked case | first pass + worked case by hand | $\ln p_\theta(2.5)=-0.725791$, met exactly by the ELBO at the exact encoder; the wrong encoder's gap $0.154544$; $D^*(2)=0.622459$ at $m=2.5$. |
| **50** | 6.1 §1–2, §5–6 | first pass | The ELBO as an identity, with the Gaussian KL (§2); the optimal discriminator and Jensen–Shannon (§5); why the original generator loss stops learning (§6). |
| **51** | 6.1 problem set 1–2, self-check | problem set | Solutions 1–2: the swapped decoder keeps the marginal $\mathcal N(2,\,0.25)$ and $\ln p_\theta(2.5)=-0.725791$; its posterior is $\mathcal N(0.6,\,0.8^2)$. |
| 52 | 6.1 §3–4 | first pass | Why the reparameterization gradient has low variance (§3); the linear VAE's ridge and posterior collapse (§4). |
| 53 | 6.1 §7, §9 | first pass | Mode collapse and the Wasserstein distance (§7); VAE, GAN and diffusion set side by side (§9). |
| 54 | 6.1 §8, problem set 3 | lab and sweep | SGD on the linear VAE and the GAN's gradient on a grid print; problem 3's KL warm-up run. |
| 55 | 6.1 §10, self-check 7 | first pass | The VQ lookup at $x=2.5$ by hand: $k=2$ and $\hat x=2.4$; the encoder receives $-0.15$ and the code $-0.2$. The two-code VQ's $0.0908$ at $\ln2=0.693$ nats against the continuous VAE's $0.09$ at $0.5108$. Self-check 7: codebook usage before vocabulary size. |
| **56** | [[03-deep-learning/diffusion/index\|6]] object D6, diagram, worked case | first pass + worked case by hand | $\alpha_5=0.907029$, one DDPM step to $\mu_4=1.180159$, and the one-shot $\hat x_0=1.85$ — an error of $0.15=0.2\times0.75$. |
| **57** | 6 §1–2, self-check, problem set 1–2 | first pass + problem set | Solutions 1–2 with $\epsilon=+1$: $x_5=2.2$; a perfect predictor returns $2$ and the biased one $1.85$ again. |
| 58 | 6 §3–5, problem set 3 | lab and sweep | The sampler-step table reproduced; problem 3's sample-dependent error run, and why §5's closed form no longer predicts it. |
| 59 | The cumulative problem set above | problem set | All three problems match their Solutions, every number reproduced by hand. |

**Totals.** 59 sessions for the Working pass, 26 of them bold. A Literacy pass is the bold rows, or one session a page — 11 — when only each object and worked case are read. Plan on up to a fifth more for problems redone and labs debugged.

## 한국어

딥러닝 공부의 전체 지도. 먼저 기초를 다진 뒤, physical AI·월드모델·디퓨전 같은 최신 흐름을
주요 학회(NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, CoRL, RSS, ICRA) 논문으로 따라간다.

### 지도

- [[03-deep-learning/lineage|1. Paper Lineage]] — 한 페이지 큰 그림 + 시대별 계보도
- [[03-deep-learning/physical-ai-ecosystem|2. Physical AI Ecosystem]] — 누가 무엇을 만드는지, 논문과 연결

### 세부 분야

[[03-deep-learning/lab-objects|0. Deep-Learning Lab Objects]]에서 시작한다. 여섯 교과 모듈은 같은 고정 대상을 재사용해 표현·목적함수·증거를 서로 비교하게 한다.

1. [[03-deep-learning/foundations/index|Learning Systems]] — tensor, logit, loss, update, data split, 학습 recipe와 scaling 주장
   - [[03-deep-learning/foundations/sequence-models|1.1 시퀀스 모델]] — 순환 신경망과 시간 역전파, 그래디언트 소실과 폭발, LSTM과 GRU, 선형 상태공간 모델(S4, Mamba), 선형 어텐션과 델타 규칙, 2025년의 어텐션 하이브리드. 대상은 D5
   - [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]] — scaled dot-product attention, mask, head, 위치 정보, 블록과 그 비용, 전문가 혼합(MoE) 부층. 대상은 D2의 패치 토큰
   - [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습]] — 분산 예산으로 본 초기화·정규화·잔차 경로, 혼합 정밀도, 파라미터당 메모리와 연산량, compute-optimal 배분과 LoRA, 로봇 위 추론을 위한 fp8·fp4 정밀도. 대상은 D1, 20층 MLP, 예시용 1억 파라미터 Transformer
   - [[03-deep-learning/foundations/gpu-computing|1.4 로봇 학습을 위한 GPU 계산]] — CUDA 실행 모델, 병합 접근, 산술 강도와 루프라인, 병렬 환경에 걸친 배치, CUDA 커널 읽기, 프로파일링과 호스트–디바이스 동기화, Jetson 배포. 대상은 정책 MLP와 교과용 GPU
2. [[03-deep-learning/computer-vision/index|Computer Vision]] — convolution·patch token과 분류·검출·분할·depth·3D 출력
3. [[03-deep-learning/vlm/index|Vision–Language Models]] — dual encoder, fusion, generation, contrastive batch, grounding, 그리고 모달리티가 만나는 자리와 옴니모달 모델
4. [[03-deep-learning/vla/index|Vision–Language–Action]] — 행동 표현, behavior cloning, chunking, 제어 interface, 증거. 토큰 헤드와 노이즈 제거 헤드, embodiment 격차, in-context 모방학습
5. [[03-deep-learning/world-models/index|World Models]] — latent state, transition, reward, rollout error, planning, model exploitation, 그리고 월드모델이라 불리는 렌더러·시뮬레이터·플래너
6. [[03-deep-learning/diffusion/index|Diffusion & Flow]] — noising, denoising target, flow field, sampler, policy latency
   - [[03-deep-learning/diffusion/vae-gan|6.1 VAE와 GAN]] — ELBO와 reparameterization 그래디언트, 선형 VAE와 사후 붕괴, GAN 게임과 그 포화·모드 붕괴, VQ-VAE의 이산 코드. 6의 선수 강의이며, D6를 분포로 넓힌다

각 모듈은 이름 붙은 대상·완전 계산·과제·통과 기준을 갖춘 **공학 브리지 교과**다. 핵심 논문을 읽고 사용할 수 있게 만들며, [[01-canonical-papers/canonical-list|핵심 논문 리스트]]가 역사적 깊이와 1차 증거를 제공한다. 모듈을 Working으로 마쳐도 분야 전체가 Mastery가 되는 것은 아니다.

### 누적 과제 · Cumulative problem set

Tier B. [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상 가운데 둘씩을 가로지르는 손 문제 셋이고, 각각 모듈이 이미 계산한 것의 변형이다. 모듈을 마친 뒤에 하고, 모듈의 과제를 대신하지 않는다. 새 코드는 없다.

1. **D1에서 D2로: 분류하는 softmax가 곧 주의를 나누는 softmax다.** [[03-deep-learning/foundations/index|1. 학습 시스템]]의 D1과, D2 토큰 위에서 도는 [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]]의 헤드 1을 쓰고, 질의는 토큰 1이다: 키 1–4에 대한 원점수 $(0,2,-2,0)$을 softmax 전에 $\kappa$로 나누며, 밝은 패치는 키 2와 4다.
   - **그리기.** D1의 순전파를 손실까지, shape $2\to3\to2$로 그리되 softmax와 교차 엔트로피를 한 블록으로 묶고 그 블록에서 $p-y$가 나가게 한다. 옆에 토큰 1의 어텐션 행을 그린다 — 점수 넷, $\kappa$로 나누기, 키 넷에 대한 softmax 하나 — 그리고 키 2와 4를 밝은 쪽으로 묶는다. 각 softmax 밑에 무엇에 대해 정규화하는지 쓴다.
   - **유도.** (a) 두 클래스 softmax가 $\sigma(s_1-s_2)$임을 보이고, D1의 logit을 $\kappa=\sqrt2$ — $d_k=2$에서 어텐션이 쓰는 나눔수 — 로 나눴을 때의 $p$, $L$, $p-y$를 구한다. (b) 토큰 1의 밝은 몫 $a_{12}+a_{14}$가 모든 $\kappa$에서 $\sigma(2/\kappa)$임을 보이고 $\kappa=1$, $\sqrt2$, $2$에서 값을 구한다. (c) 어느 $\kappa$에서 밝은 몫이 D1의 카탈로그 $p_1$과 같아지며, 거기서 그 값의 $-\ln$은 얼마인가?
   - **해석.** D2에서 키 넷의 softmax가 왜 두 클래스 softmax로 접히는가? 나눔수가 커지면 두 대상 모두에서 확신과 $p-y$의 크기가 어느 쪽으로 움직이는가? $d_k=64$인 헤드를 $\sqrt{d_k}$ 대신 $d_k$로 나누면 무엇이 되는가?
2. **D5 대 D6: 실려 가는 오차와 갈아 끼워지는 오차.** 두 루프 모두 스텝마다 신경망을 한 번 부른다. [[03-deep-learning/world-models/index|5. 월드모델]]의 D5 전이는 자기 출력을 다시 입력으로 받고, [[03-deep-learning/diffusion/index|6. Diffusion & Flow]]의 D6 sampler는 방문하는 레벨마다 $x_0$를 새로 추정한다.
   - **그리기.** 신경망 호출 다섯 번에 걸친 띠 두 개. 위: 낙관적 이득 $\hat\lambda'=0.7$과 행동 0으로 자유 실행하는 D5 — 스텝마다 실려 온 간극 $\hat\lambda'\delta_t$와 새 오차 $e_t$가 더해지는 두 화살표. 아래: $b=0.2$인 D6의 $N=5$ 실행 — 레벨 20, 16, 12, 8, 4, $x_0$ 추정 다섯 개, 그리고 마지막 추정에서만 출력으로 가는 화살표.
   - **유도.** (a) $\hat\lambda'=0.7$일 때 $e_t$, $\delta_H$의 닫힌 형태, $\delta_1$, $\delta_5$, $\lvert\delta_H\rvert$가 가장 큰 $H$, 그리고 $\delta_{10}/z_{10}$. (b) $N=5$ 실행에서 방문한 레벨마다 $\hat x_0=x_0-b\sqrt{1-\bar\alpha_i}/\sqrt{\bar\alpha_i}$로 구한 D6의 추정 다섯 개와 최종 오차. 이어서 신경망 오차를 $b=0.1$로 절반으로 줄였을 때 $N=1$, $5$, $10$의 최종 오차와, 카탈로그 신경망의 $N=20$ 오차를 이기는 §5의 스텝 수 가운데 가장 작은 것.
   - **해석.** 호출 다섯 번 뒤 D5의 간극은 첫 스텝의 오차보다 크고, D6의 오차는 첫 추정의 오차보다 작다. 왜 그런가? 각 루프에서 무엇 하나를 바꾸면 둘의 행동이 뒤바뀌는가?
3. **D3 대 D4: 프로토콜이 정하는 두 숫자.** $N$쌍의 배치는 encoder가 아무리 좋아도 최대 $\log N$ 나트만 보증한다([[03-deep-learning/vlm/index|3. VLM §2]]). 추론 지연이 $m$ 스텝인 길이 $k$의 청크는 다음 경계보다 먼저 반응하지 못한다([[03-deep-learning/vla/index|4. VLA]]). 어느 숫자도 모델이 정하지 않는다.
   - **그리기.** 쌍 3을 뺀 배치($N=2$)의 $\tau=1/2$ 유사도 행렬을 배치 상자와 대각선과 함께 그리고, 옆의 손실 축에 $\log2$, $\log3$, 두 배치의 $\mathcal L$을 표시한다. 이어서 20 Hz, 추론 $100$ ms, $k=3$인 D4의 시간 축: 세 스텝마다의 청크 경계, 스텝 $n_j=21$의 장면 변화, 그리고 그 변화를 알 수 있는 첫 경계.
   - **유도.** (a) $N=2$일 때 행 손실 둘, $\mathcal L$, $\log N-\mathcal L$을 전체 배치의 $\mathcal L=0.602352$와 비교한다. (b) $n_j=21$일 때 $k=2$, $3$, $4$의 $\ell(k)$, 그리고 페이지의 $n_j=20$에서 같은 셋. (c) $n_j$가 무엇이든 $\ell(k)$가 $m\Delta t$와 $(m+k-1)\Delta t$ 사이에 있음을 보인다.
   - **해석.** 쌍 하나를 빼자 손실이 내려갔고, 변화를 한 스텝 옮기자 지연이 바뀌었다. 어느 쪽도 모델을 건드리지 않았다. 두 숫자 어느 것도 더 나은 모델로 읽히지 않으려면 논문이 무엇을 보고해야 하는가?

> [!tip]- 정답 · Solutions
> 1. *그리기:* $x$(2), $z$와 $h$(3), $s$와 $p$(2), 스칼라 $L$. 어텐션 행은 점수(4)와 가중치(4), 그다음 밝은 몫(스칼라)과 $o_1$(2)이다. D1의 softmax는 클래스에 대해, 어텐션 행은 키에 대해 정규화한다. *유도:* (a) $e^{s_1}/(e^{s_1}+e^{s_2})=1/(1+e^{-(s_1-s_2)})=\sigma(s_1-s_2)$. $\kappa=\sqrt2$면 간격이 $1/\sqrt2=0.707107$이므로 $p=(0.669762,\,0.330238)$, $L=0.400834$ 나트, $p-y=(-0.330238,\,0.330238)$ — $\kappa=1$의 $0.731059$, $0.313262$, $\pm0.268941$과 비교된다. (b) 밝은 질량은 $e^{2/\kappa}+1$, 어두운 질량은 $1+e^{-2/\kappa}=e^{-2/\kappa}(e^{2/\kappa}+1)$이라 둘의 비가 $e^{2/\kappa}$이고 몫은 $\sigma(2/\kappa)$다: $0.880797$, $0.804430$(계산 예제의 첫 출력 좌표), $0.731059$. (c) $\kappa=2=d_k$: 몫은 $\sigma(1)=0.731059$로 D1의 $p_1$이고, $-\ln0.731059=0.313262$ 나트로 D1의 $L$이다. *해석:* 헤드 1은 토큰 1의 키를 $c_j-r_j$로 채점하고 D2의 밝은 패치는 정확히 오른쪽 열이므로, 행마다 밝은 키가 어두운 키보다 $2/\kappa$만큼 높다 — 키 넷이 둘씩 짝지어 그 행은 logit 간격 $2/\kappa$의 두 클래스 softmax가 된다. 나눔수가 커지면 두 대상 모두 $1/2$ 쪽으로 가고 $p-y$가 커져(D1에서 $0.268941\to0.330238$) 그래디언트가 살아남는다. 작아지면 포화한다. $d_k=64$에서 $8$ 대신 $64$로 나누면 모든 간격이 여덟 배 더 줄어 헤드가 거의 균일한 상태, 곧 눈먼 상태로 출발한다 — [[03-deep-learning/foundations/attention-transformer|1.2 §2]]의 비예시다.
> 2. *그리기:* 위 띠의 스텝마다 두 화살표 $\hat\lambda'\delta_t$와 $e_t$가 더해지고, 아래 띠에는 추정 다섯 개와 출력 화살표 하나가 있다. *유도:* (a) $e_t=(\hat\lambda'-\lambda)z_t=-0.1\cdot0.8^t$이고, 페이지의 재귀를 풀면 $\delta_H=0.7^H-0.8^H$가 된다: $\delta_1=-0.1$, $\delta_5=-0.15961$, $\lvert\delta_H\rvert$는 $H=4$에서 가장 커서 $-0.1695$, 그리고 $\delta_{10}/z_{10}=0.875^{10}-1=-0.736924$ — $-1$을 넘어설 수 없는 상대 오차다. 비관적 이득의 $(9/8)^H-1$은 한없이 커진다. (b) 추정은 $1.020204$, $1.481693$, $1.671475$, $1.784349$, $1.870813$이고 마지막만 살아남아 오차는 $0.129187$이다. $b=0.1$이면 $0.489898$, $0.064594$, $0.042600$. $N=5$는 카탈로그 신경망의 $N=20$ 오차 $0.058333$에 여전히 못 미치고 $N=10$이 이긴다 — $100$ ms 대신 $50$ ms다. *해석:* D5의 사상은 닫혀 있어서 스텝마다의 오차가 $\hat\lambda'$배 되어 다음 스텝에 더해진다. 호출 다섯 번 뒤 $\lvert\delta_5\rvert/\lvert\delta_1\rvert=1.5961$이고, 비관적 이득은 같은 한 스텝 오차를 더 큰 배수로 실어 날라 $2.6281$이다. D6의 오차는 호출 다섯 번 뒤 첫 추정 오차의 $0.129187/0.979796=0.131851$배다. 상수 편향은 다시 잡음을 입힌 샘플을, 다음 추정이 같은 $b$만큼만 틀리게 읽는 직선 위에 올려놓으므로 마지막 레벨의 증폭만 남는다. 스텝마다 실제 관측을 다시 인코딩하면(teacher forcing) D5의 간극이 새 오차 $e_t$로 리셋되고, [[03-deep-learning/diffusion/index|6]]의 과제 3처럼 오차가 $x$에 의존하면 각 추정의 오차가 앞 스텝이 남긴 샘플에 달려 D6의 오차도 실려 간다.
> 3. *그리기:* $2\times2$ 행렬 $\begin{pmatrix}2&1\\1&2\end{pmatrix}$와 그 대각선. 손실 축에서 $\mathcal L_2=0.313262$는 $\log2=0.693147$ 아래, $\mathcal L_3=0.602352$는 $\log3=1.098612$ 아래에 놓인다. 시간 축의 경계는 스텝 21, 24, 27이고, 21의 변화를 처음 아는 것은 스텝 24에서 시작하는, 관측이 스텝 22인 청크다. *유도:* (a) 행 1의 logit은 $(2,1)$, 행 2는 $(1,2)$이므로 각 $p_{ii}=\sigma(1)=0.731059$, 각 손실은 $0.313262$ 나트 — 각 행이 자기 클래스를 위에 둔 D1의 logit 쌍이라 D1의 숫자 그대로다. 열도 대칭으로 같으므로 $\mathcal L=0.313262$, $\log2-\mathcal L=0.379885$이고, 전체 배치는 $\log3-0.602352=0.496260$이다. (b) $m=\lceil0.10/0.05\rceil=2$. $n_j=21$이면 세 $k$ 모두 $\ell=0.15$ s이고 경계는 매번 스텝 24다. $n_j=20$이면 $0.10$, $0.20$, $0.20$ s. 한 스텝 늦추자 $k=3$은 빨라지고 $k=2$는 느려졌다. (c) $n_j+m=qk+\rho$, $0\le\rho<k$로 쓴다. $\rho=0$이면 경계가 $n_j+m$ 자체라 $\ell=m\Delta t$이고, 아니면 $(q+1)k=n_j+m+(k-\rho)$라 $\ell=(m+k-\rho)\Delta t\le(m+k-1)\Delta t$다 — 최악의 경우가 최악의 행동 나이와 같다. *해석:* 손실 옆에는 $N$, $\tau$, 그리고 정보가 없을 때의 값 $\log N$이 있어야 한다. 지연에는 $k$, $m$, $\Delta t$와 최악값 $(m+k-1)\Delta t$, 또는 변화 시점의 위상에 따른 분포가 있어야 한다. 장면 변화 하나는 위상 하나만 표본으로 뽑기 때문이다. 작은 배치는 점수가 낮으면서도 덜 보증하고, 운 좋은 위상은 더 빠른 정책 없이도 빨리 반응한다.

### 학습 일정 · Session schedule

한 행이 60–90분 학습 회차 하나다. 그 단위와, 이 회차 수가 들어가는 페이스 표는 [[02-foundations/overview|0. Overview]]에 있다. 순서는 각 페이지가 딛는 것을 따른다: 1.1은 1만 있으면 되고, 1.2는 2. 컴퓨터비전이 고정한 D2의 픽셀을 읽으며, 1.3은 1.2 위에 서고, 6.1은 6의 선수 강의다. **굵은** 번호는 페이지의 첫 읽기 — 대상과 끝까지 계산, 그리고 처음이라면 콜아웃이 지목한 절과 문제 — 를 표시한다. 굵은 행만 하면 Literacy 통과이고, 모든 행을 하면 Working 통과다. 여기의 페이지는 모두 Tier A라 페이지마다 실습과 스윕 회차가 있다. 나머지 산정은 로보틱스 트랙과 같다: 대상과 끝까지 계산이 페이지를 열고, 절은 회차당 영어 약 1,500–2,500단어씩 이어지며, 과제가 페이지를 닫는다.

| # | 페이지와 절 | 활동 | 회차를 끝내는 확인 |
|---:|---|---|---|
| **1** | [[03-deep-learning/foundations/index\|1]] 대상 D1·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 D1의 순전파·역전파·SGD 한 스텝: $L=0.313262$, $p-y=(-0.268941,\,0.268941)$, $\eta=0.1$에서 $\Delta L=-0.129177$. |
| **2** | 1 §1–5, 스스로 점검, 과제 1–3 | 첫 읽기 + 과제 | 정답 1–3: bias를 포함해 파라미터 $17$개. logit $(0,\log3)$은 $p=(1/4,\,3/4)$, $L=1.386$을 준다. 테스트 셋이 모델 선택에 끼어들었다. |
| 3 | 1 §6, 과제 4 | 실습과 스윕 | 실습이 보폭 경계를 잰다. 과제 4는 목표를 클래스 2, $\lambda=0.2$로 바꿔 다시 돌리고 $L_\lambda=1.813262$에서 출발한다. |
| **4** | [[03-deep-learning/foundations/sequence-models\|1.1]] 대상·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 D5에서 앞으로 두 스텝과 뒤로 두 스텝, 커널 탭 다섯 개, 그리고 같은 두 출력을 합성곱으로 다시 구한다. |
| **5** | 1.1 §1–3 | 첫 읽기 | BPTT를 Jacobian의 곱으로 쓴다(§2). 소실과 폭발을 스펙트럼 반지름이 정하는 이유(§3). |
| **6** | 1.1 과제 1–2, 스스로 점검 | 과제 | 정답 1–2($\hat\lambda=0.9$): 재귀로도 합성곱으로도 $z_3=0.324$. $g_3,g_2,g_1=0.324,\,0.2916,\,0.26244$. |
| 7 | 1.1 §4–8 | 첫 읽기 | 천장으로서의 clipping(§4). LSTM의 cell 경로(§5). 선형 상태공간 모델 하나를 손으로 이산화한다(§8). |
| 8 | 1.1 §9–10, §12 | 첫 읽기 | S4와 Mamba를 백본으로 쓸 수 있게 한 것(§9). 순차 스텝·연산량·메모리를 나란히 놓는다(§10). §12의 질문을 시퀀스 모델 주장 하나에 던진다. |
| 9 | 1.1 §11, 과제 3 | 실습과 스윕 | horizon 스윕, 재귀–합성곱 검사, cell 경로가 찍힌다. 과제 3을 붙여 돌리면 BPTT 줄이 $\partial L/\partial\lambda=0.49572$를 준다. |
| 10 | 1.1 §13, 스스로 점검 7 | 첫 읽기 | 겹치는 기억 둘을 손으로 쓴다. 더하면 $S=(0.4,-0.8)$이 $0.4$와 $-0.4$를 돌려주고, 델타 규칙이면 $S_2=(0.04,-1.28)$이 $-1$을 정확히 돌려준다. 스스로 점검 7: $30$ s 시연의 캐시 $1.42$ GB와 3:1 하이브리드가 남기는 $0.35$ GB. |
| **11** | [[03-deep-learning/computer-vision/index\|2]] 대상 D2·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 D2에서 합성곱 창 하나, 출력 크기 하나, IoU 하나를 구한다. |
| **12** | 2 §1–4, 스스로 점검, 과제 1–3 | 첫 읽기 + 과제 | 정답 1–3: $3\times3$, stride 2, padding 1 층은 $4\times4\times8$ 출력과 파라미터 $80$개를 준다. metric depth 주장은 뒷받침되지 않는다. |
| 13 | 2 §5, 과제 4 | 실습과 스윕 | 실습의 공식·문턱·평균을 재현한다. 과제 4의 세 변형을 표로 보고한다. |
| **14** | [[03-deep-learning/foundations/attention-transformer\|1.2]] 대상·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 D2의 헤드 1: 점수 열여섯 개, 행 $(0.157323,\,0.647107,\,0.038248,\,0.157323)$의 재배열, $o_1=(0.804430,\,-0.608859)$, 그리고 causal 행들. |
| **15** | 1.2 §1–3 | 첫 읽기 | 나눔수가 $\sqrt{d_k}$인 이유를 세 줄로(§2). causal mask는 softmax 전에 점수에 더한다(§3). |
| **16** | 1.2 과제 1–2, 스스로 점검 | 과제 | 정답 1–2: 헤드 3의 격자와 causal 행. $d_k=64$에서 $\mathrm{sd}(q\cdot k)=16$. 블록 파라미터는 $h=2$에서도 $h=4$에서도 $872$개. |
| 17 | 1.2 §4–5 | 첫 읽기 | 토큰 1의 두 헤드 출력 $(0.804430,\,-0.608859,\,0.195570,\,-0.608859)$(§4). 어텐션에 위치 정보가 필요한 이유와 그것을 주는 두 방법(§5). |
| 18 | 1.2 §6–7, 과제 4 | 첫 읽기 + 과제 | 블록의 구성 순서(§6). 과제 4: $n=276$, $d=4096$에서 두 $n\times n$ 곱은 곱셈-덧셈의 약 $1.1\,\%$다. |
| 19 | 1.2 §8, 과제 3 | 실습과 스윕 | 실습이 2(a)와 소수 여섯째 자리까지 맞는다. 거울 검사의 차이는 위치 표가 있으면 $0.608859$, 없으면 $0$. 비율은 $n=6d$에서 절반을 넘는다. |
| 20 | 1.2 §9, 스스로 점검 7 | 첫 읽기 | D2의 네 토큰을 손으로 라우팅한다. $x_1$은 $p=(0.269,\,0.731)$을 받고 어두운 토큰은 전문가 2로 간다. 보조 손실은 균형 잡힌 라우터에서 $1$, 무너진 라우터에서 $1.46$. 블록 파라미터 $400$개 가운데 토큰 하나가 건드리는 것은 $252$개. 스스로 점검 7: bf16으로 상주하는 $160$ GB 대 NVFP4의 $45$ GB. |
| **21** | [[03-deep-learning/foundations/training-at-scale\|1.3]] 대상·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 세 초기화에서 D1의 분산, 그리고 T-100M의 연산량·시간·메모리·파라미터당 토큰 수·LoRA 비율 하나. |
| **22** | 1.3 §1, §5–6 | 첫 읽기 | 분산 예산으로서의 He와 Xavier(§1). 파라미터당 16바이트(§5)와 파라미터·토큰당 6 FLOP(§6)을 T-100M에 적용한다. |
| **23** | 1.3 과제 1–2, 스스로 점검 | 과제 | 정답 1–2: $W_0$ 옆을 지나는 $r=8$ 어댑터의 경로. $256\to64$에서 He는 $\operatorname{Var}(w)=0.0078125$로 순전파를 보존하고 그래디언트 분산을 4분의 1로 줄인다. |
| 24 | 1.3 §2–3 | 첫 읽기 | BatchNorm과 LayerNorm이 평균 내는 축과 추론 때 달라지는 것(§2). 잔차 흐름의 분산(§3). |
| 25 | 1.3 §4, §7 | 첫 읽기 | 혼합 정밀도의 master copy와 loss scale(§4). 파라미터당 20토큰이라는 적합과 그 가정(§7). |
| 26 | 1.3 §8–9, 과제 4 | 첫 읽기 + 과제 | LoRA의 파라미터 수(§8). 과제 4: 예시 7B 모델의 full fine-tuning은 모델 상태만 $112$ GB로 $24$ GB 장치의 $4.7$배다. |
| 27 | 1.3 §10, 과제 3 | 실습과 스윕 | 분산 표, 잔차 흐름, 16비트 실행, 예산이 찍힌다. 과제 3: 넓히고 깊게 한 MLP-20을 네 번째 초기화로 돌린다. |
| 28 | 1.3 §11, 스스로 점검 7 | 첫 읽기 | 가중치 넷짜리 블록을 손으로 fp4에 넣는다. 스케일 $0.14$, 작은 가중치마다 $0.02$씩 틀린다. 이상값 $8.4$가 스케일을 $1.4$로 올려 셋 모두 0으로 저장된다. Jetson Thor에서 토큰당 하한은 bf16, fp8, NVFP4에서 $22.0$, $11.0$, $6.2$ ms. 스스로 점검 7: $2$ Hz 정책을 양자화하기 전에 잴 것. |
| **29** | [[03-deep-learning/foundations/gpu-computing\|1.4]] 대상·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | G-100 위의 MLP-256: 가중치 $83{,}968$개. $N=1$에서 층 2는 $131{,}072$ FLOP에 $132{,}096$바이트를 옮겨 산술 강도 $0.992$로 메모리에 묶이고, 전체 패스 $15.17$ µs의 $98.9\%$가 launch다. $N=4{,}096$에서는 $25.19$ µs, 환경당 $6.15$ ns. |
| **30** | 1.4 §1–2 | 첫 읽기 | CUDA 실행 모델 — 커널, 블록, 그리드, 워프 — 과 지연 숨기기(§1). 워프의 fp32 읽기는 보폭 1에서 섹터 $4$개, 보폭 8에서 $32$개(§2). |
| 31 | 1.4 §3–4 | 첫 읽기 | 능선이 $100$ FLOP/byte인 루프라인(§3). 층별 상한 $51.2$, $128$, $7.76$, 그리고 층 2가 $N=457$에서 능선을 넘는 것(§4). |
| 32 | 1.4 §5–6 | 첫 읽기 | 벡터화한 환경과 Rudin 외의 로봇 $4{,}096$대(§5). 단순한 행렬곱과 타일링한 행렬곱이 $T=1$과 $32$에서 한 번 읽기 바이트의 $481.9$배와 $15.1$배를 읽는 것(§6). |
| 33 | 1.4 §7–8, 스스로 점검, 과제 1–2, 4 | 과제 | $N=4{,}096$에서 층마다 동기화하면 $25.19$ µs, 그래프 한 번이면 $15.19$, 융합 커널이면 $11.88$(§7). 로봇에서 빌드하는 엔진과 제어 예산(§8). 정답과 대조: $2$ TB/s면 능선이 $50$으로 내려가도 $N=1$은 여전히 $99.4\%$가 launch. 층 1의 상한 $51.2$는 어떤 배치에서도 능선 아래. 비동기 호출을 감싼 `perf_counter()`는 launch만 잰다. |
| 34 | 1.4 §9, 과제 3 | 실습과 스윕 | 실습: launch 비중이 $N=1$의 $98.9\%$에서 $N=16{,}384$의 $27.0\%$로 떨어지고, $N=6{,}037$에서 커널과 launch가 같아진다. 과제 3의 MLP-512 변형. |
| **35** | [[03-deep-learning/vlm/index\|3]] 대상 D3·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 풀이를 가리고 내적 아홉 개, 행 손실 $(0.407606,\,0.757448,\,0.642002)$, 그리고 $\log3=1.098612$에 대한 $\mathcal L=0.602352$. |
| **36** | 3 §1–4, 스스로 점검, 과제 1–3 | 첫 읽기 + 과제 | 정답 1–3: $\tau=1/4$의 행 1은 $(4,2,0)$, $p=0.867$, 손실 $0.143$. 밸브 픽셀에 대한 grounding은 시험되지 않은 채로 남는다. |
| 37 | 3 §5, 과제 4 | 실습과 스윕 | temperature 스윕을 재현한다(한 쌍이 틀린 배치의 최소 $\tau=0.1639$ 포함). 과제 4의 중복 캡션 변형과 그 손실. |
| 38 | 3 §6, 스스로 점검 6 | 첫 읽기 | 모달리티가 만나는 네 자리 — 끝에서(CLIP, D3), 다리를 거쳐(Flamingo), 한 시퀀스 안에서(Chameleon, Transfusion), 옴니모달(GPT-4o, Qwen2.5-Omni) — 와 각각이 얻고 치르는 것. 스스로 점검 6: "옴니모달" 로봇 모델이 VLA가 되려면 무엇을 내놓아야 하는가. |
| **39** | [[03-deep-learning/vla/index\|4]] 대상 D4·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | 축 규칙으로 청크를 다시 만든다. $m=2$, $k=3$의 최악 나이 $0.20$ s, 그리고 $\ell=0.20$ s 대 $k=20$의 $1.00$ s. |
| **40** | 4 §1–3, 스스로 점검, 과제 1–2 | 첫 읽기 + 과제 | 정답 1–2: 50 Hz 제어기에서는 $m=5$ — 빨라진 제어기가 최소 청크를 키웠다 — 이고 $k=5$의 최악 나이는 20 Hz의 $0.30$ s 대신 $0.18$ s. |
| 41 | 4 §4–5, 과제 3 | 실습과 스윕 | 청크 길이 스윕의 지연 열이 $\ell(k)$와 행마다 맞는다. 과제 3의 두 번 움직이는 목표를 돌린다. |
| 42 | 4 §6, 스스로 점검 7 | 첫 읽기 | D4의 $256$구간 한 칸 $0.16$ mm 대 지각 지터 $2$ mm. 청크를 노이즈 제거하는 쪽이 토큰을 디코딩하는 쪽보다 싸지는 교차점 $H=5$. 단봉 헤드가 $(-1,0)$과 $(1,0)$을 $(0,0)$으로 보내는 이유. 스스로 점검 7: ECoT의 스텝당 토큰 $7\to350$, 청크당 D4의 $6$패스가 $349$패스가 된다. |
| 43 | 4 §7, 스스로 점검 6 | 첫 읽기 | 정규화한 D4 청크를 팔 B에서 실행하면 $6$ cm와 $3$ cm를 지나쳐 의도한 움직임의 두 배 반이 된다. 다섯 설계와 각각이 치르는 대가. OXE의 대규모 데이터 행: Bridge에서 RT-1-X는 $27\%$, RT-1은 $40\%$이고, 55B RT-2-X가 $50\%$로 되찾는다. 스스로 점검 6: $100$회 시행의 $70\%$와 $75\%$는 구간 $[0.60,\,0.78]$과 $[0.66,\,0.82]$가 겹친다. |
| 44 | 4 §8, 스스로 점검 8 | 첫 읽기 | 12초짜리 D4 시연을 프롬프트로: $240$ 스텝, 첫 행동 전에 토큰 $720$개. GEN-1.5는 시연 하나로 $59\%$, 그래디언트 열 스텝 뒤 $83\%$. 스스로 점검 8: 세 조건 가운데 먼저 확인할 것과, 숫자를 결정으로 바꾸는 비교. |
| **45** | [[03-deep-learning/world-models/index\|5]] 대상 D5·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | return $-1.19$와 $-1.64$. $\delta_H=0.9^H-0.8^H$는 $H=5$에서 $0.26281$이고 $H=6$에서 최대 $0.269297$. |
| **46** | 5 §1–3, 스스로 점검, 과제 1–2 | 첫 읽기 + 과제 | 정답 1–2($\hat\lambda=0.85$): $e_t=0.05\cdot0.8^t$, $\delta_H=0.85^H-0.8^H$, $\delta_5=0.116025$. |
| 47 | 5 §4–5, 과제 3 | 실습과 스윕 | horizon 스윕을 재현한다. 과제 3의 잘못 학습된 행동 이득은 $H=2$–$5$에서 regret $0.0000$, $0.0325$, $0.0693$, $0.0929$를 준다. |
| 48 | 5 §6, 스스로 점검 6 | 첫 읽기 | D5의 사상 $f(z,a)=0.8z+0.5a$는 시뮬레이터이고 §5의 전수 조사는 플래너다. 세 기능을 내놓는 것으로 가르고, 각각이 매니퓰레이터에 주는 것을 말한다. 스스로 점검 6: 휴대폰 영상으로 만든 현장 장면의 자리와, 패널을 앉히는 데 아직 없는 것. |
| **49** | [[03-deep-learning/diffusion/vae-gan\|6.1]] 대상·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | $\ln p_\theta(2.5)=-0.725791$을 정확한 encoder의 ELBO가 그대로 맞춘다. 틀린 encoder의 간극은 $0.154544$. $m=2.5$에서 $D^*(2)=0.622459$. |
| **50** | 6.1 §1–2, §5–6 | 첫 읽기 | 항등식으로서의 ELBO와 가우시안 KL(§2). 최적 판별기와 Jensen–Shannon(§5). 원래 생성기 손실이 학습을 멈추는 이유(§6). |
| **51** | 6.1 과제 1–2, 스스로 점검 | 과제 | 정답 1–2: 바꾼 decoder도 주변분포 $\mathcal N(2,\,0.25)$와 $\ln p_\theta(2.5)=-0.725791$을 유지한다. 사후분포는 $\mathcal N(0.6,\,0.8^2)$. |
| 52 | 6.1 §3–4 | 첫 읽기 | reparameterization 그래디언트의 분산이 낮은 이유(§3). 선형 VAE의 능선과 사후 붕괴(§4). |
| 53 | 6.1 §7, §9 | 첫 읽기 | 모드 붕괴와 Wasserstein 거리(§7). VAE, GAN, diffusion을 나란히 놓는다(§9). |
| 54 | 6.1 §8, 과제 3 | 실습과 스윕 | 선형 VAE의 SGD와 격자 위 GAN 그래디언트가 찍힌다. 과제 3의 KL warm-up을 돌린다. |
| 55 | 6.1 §10, 스스로 점검 7 | 첫 읽기 | $x=2.5$에서 VQ 조회를 손으로: $k=2$, $\hat x=2.4$. encoder는 $-0.15$를, 코드는 $-0.2$를 받는다. 코드 둘짜리 VQ는 $\ln2=0.693$ nats에서 $0.0908$, 연속 VAE는 $0.5108$ nats에서 $0.09$. 스스로 점검 7: 어휘 크기보다 먼저 볼 코드북 사용률. |
| **56** | [[03-deep-learning/diffusion/index\|6]] 대상 D6·과제 그림·끝까지 계산 | 첫 읽기 + 손 계산 | $\alpha_5=0.907029$, DDPM 한 스텝으로 $\mu_4=1.180159$, 한 번에 추정한 $\hat x_0=1.85$ — 오차 $0.15=0.2\times0.75$. |
| **57** | 6 §1–2, 스스로 점검, 과제 1–2 | 첫 읽기 + 과제 | 정답 1–2($\epsilon=+1$): $x_5=2.2$. 완벽한 예측기는 $2$를, 편향된 예측기는 다시 $1.85$를 준다. |
| 58 | 6 §3–5, 과제 3 | 실습과 스윕 | sampler 스텝 표를 재현한다. 과제 3의 샘플 의존 오차를 돌리고, §5의 닫힌 형태가 더는 맞지 않는 이유를 말한다. |
| 59 | 위 누적 과제 | 과제 | 세 문제 모두 정답과 맞고, 모든 숫자를 손으로 재현한다. |

**합계.** Working 통과는 59회이고 그중 굵은 회차가 26회다. Literacy 통과는 굵은 회차만 하는 것이고, 대상과 끝까지 계산만 읽으면 페이지당 1회로 11회다. 다시 푸는 과제와 실습 디버깅을 위해 최대 5분의 1을 더 잡는다.
