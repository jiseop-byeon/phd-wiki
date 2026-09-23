---
title: "1.4 GPU Computing for Robot Learning"
tags: [deep-learning, curriculum, gpu]
study-depth: Working
wiki-support: Working
depth-goal: "On the frozen policy MLP-256 and the course GPU G-100, compute each layer's FLOPs, bytes and arithmetic intensity at any batch, place it on the roofline and price a forward pass with its launches; count the sectors a warp touches at any stride and the global loads of a naive and a tiled kernel; read a CUDA or Warp kernel, and say where a vectorized simulator, a profiler and a robot's control loop put the time."
mastery-when: "Raise when the thesis needs a custom GPU simulator — soil or deformable materials, which no simulator covers well — or on-robot latency engineering."
---

> [!note] Prerequisites · 선수 지식
> [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale]] (bf16 and the other number formats of §4, the bytes and FLOPs a parameter costs in §5–§6, and §11's memory-bound decoding on Jetson Thor), [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]] (the multiply-add count of §7, and why FlashAttention works in tiles), [[03-deep-learning/foundations/index|1. Learning Systems]] (a batched MLP forward pass with a shape on every tensor), [[02-foundations/linear-algebra|1. Linear Algebra]] (a matrix product, row by column) and [[02-foundations/rl-basics|7. RL Basics]] (an environment step, an episode and its reset, and the on-policy loop PPO runs, for §5). The page freezes its own two objects, a policy network and a course GPU; the Tier A lab in §9 needs NumPy and nothing else, and the CUDA, Warp and PyTorch listings of §6–§7 are read, not run.
> [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습]](§4의 bf16과 다른 수 형식, §5–§6의 파라미터당 바이트와 FLOP, §11의 Jetson Thor 위 메모리 한계 디코딩), [[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]](§7의 곱셈-덧셈 셈과, FlashAttention이 타일 단위로 계산하는 이유), [[03-deep-learning/foundations/index|1. 학습 시스템]](모든 텐서에 shape을 붙인 배치 MLP 순전파), [[02-foundations/linear-algebra|1. 선형대수]](행과 열로 하는 행렬곱), [[02-foundations/rl-basics|7. RL 기초]](§5를 위한 환경 스텝, 에피소드와 리셋, PPO가 도는 on-policy 루프). 이 페이지는 정책 신경망과 교과용 GPU라는 대상 둘을 스스로 고정한다. §9의 Tier A 실습에는 NumPy만 있으면 되고, §6–§7의 CUDA·Warp·PyTorch 코드는 실행하지 않고 읽는다.

## English

*Stands on [[03-deep-learning/foundations/training-at-scale|1.3 Training at Scale]], whose §5–§6 count the bytes and FLOPs a parameter costs and whose §11 finds a robot policy's decoding memory-bound on a Jetson Thor. This page asks where those FLOPs and bytes are spent: on which units of a GPU, in what order, how fast, and what a robot-learning program must do to keep them busy. It freezes its own objects, the policy network MLP-256 and the course GPU G-100 — cost objects, where D1–D6 are tensor objects. [[04-robotics/robot-systems-deployment|10. Robot Systems §3]] budgets the latency that §8 fills in, and [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets §2]] lists the parallel simulators that §5 explains.*

> [!note] First pass · 처음이라면
> Look at the picture, then work the Worked case with a calculator — MLP-256's three layers at one environment and at 4,096, each placed on G-100's roofline and timed with its launches. Read §1, §3 and §4 and do problems 1–2. Open §2 and §6 when a paper or a codebase says "coalesced", "shared memory" or "tiled"; §5 when a paper trains thousands of simulated robots on one GPU; §7 before you time or speed up anything; §8 before a policy goes on the robot. §9 runs §2–§4, §6 and §7 as code.

### Running object · 이 페이지의 대상

Two objects, one for the work and one for the machine, both frozen here. The objects of [[03-deep-learning/lab-objects|0. Lab Objects]] are tensor objects: their numbers are values that a page computes *with*. These two are cost objects: their numbers are shapes, byte counts and rates that a page computes the *price* of, and the values inside the network never enter. The nearest catalog entry is **D1**, also a ReLU MLP without biases, but its twelve weights are 24 bytes in bf16 — nothing a GPU can time — and every D1 page asks what the network outputs, which never matters here. **D4** carries a policy's inference time, 100 ms, as a given; this page derives one.

**MLP-256**, the policy network:

| Symbol | Value | What it is |
|---|---:|---|
| layers | $64\to256\to256\to8$ | an observation of 64 numbers in, 8 action numbers out, two hidden layers of 256 |
| activation | ReLU | after each hidden layer, applied inside that layer's kernel; the output layer is linear |
| biases | none | they would add 520 parameters, 0.6%, and change no conclusion below |
| weights | $16{,}384+65{,}536+2{,}048=83{,}968$ | $W_1\in\mathbb R^{256\times64}$, $W_2\in\mathbb R^{256\times256}$, $W_3\in\mathbb R^{8\times256}$, each stored row by row |
| format | bf16, $e=2$ bytes per number | weights, observations, activations and actions alike ([[03-deep-learning/foundations/training-at-scale\|1.3 §4]]); the weights are $167{,}936$ bytes |
| $N$ | 1 to 16,384 | environments served by one forward pass: one robot, or a simulator's batch (§5) |
| kernels | one per layer | each reads its weights and input activations from DRAM and writes its output back, every operand moved once |

**G-100**, the course GPU. Every number is a rounded course number chosen for clean arithmetic; none is a product specification.

| Symbol | Value | What it is |
|---|---:|---|
| $P$ | $100$ TFLOP/s $=10^{14}$ FLOP/s | peak bf16 tensor throughput, dense |
| $\beta$ | $1{,}000$ GB/s $=10^{12}$ bytes/s | DRAM (global-memory) bandwidth |
| $I^\star=P/\beta$ | $100$ FLOP/byte | the ridge point of §3 |
| $t_L$ | $5$ µs | launch overhead: the fixed cost of issuing one kernel from the host (§4) |
| $\beta_{\text{host}}$ | $25$ GB/s | the link between host memory and the GPU (§2) |

Two more numbers are facts of CUDA hardware, not course numbers: a warp is 32 threads, and global memory is read in 32-byte sectors (§1, §2). The robot side reuses only what [[03-deep-learning/foundations/training-at-scale|1.3 §11]] cites for Jetson Thor: $2{,}070$ sparse fp4 TFLOPS, $273$ GB/s, and a ridge near $7{,}600$ FLOP/byte.

*Scope: this page teaches the GPU execution model and CUDA at reading level — kernels, threads, blocks, grids, warps and the memory hierarchy — and, at working level, the performance reasoning a robot-learning researcher uses: coalesced access, arithmetic intensity and the roofline, what batching buys and where launch overhead dominates, why parallel simulators keep everything on the GPU, what tiling does, how to measure with a profiler, and what changes on the robot. It does not teach writing production CUDA — occupancy tuning, tensor-core programming, streams and multi-GPU work belong to the CUDA Programming Guide — nor the simulators themselves, which are [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]]; nor number formats and quantization, which are [[03-deep-learning/foundations/training-at-scale|1.3 §4 and §11]]; nor distributed training. Writing a GPU simulator in NVIDIA Warp or JAX is taught only as far as §5–§6 go, because the owner needs it only if the thesis needs a custom simulator for soil or deformable materials — the gaps that [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]] and [[06-research-practice/simulators-benchmarks-datasets|7. Simulators §5]] name.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 432" style="max-width:100%;height:auto" role="img" aria-label="Two panels. (a) G-100's roofline on log-log axes: a slanted roof of 1 TB/s times the intensity and a flat roof at 100 TFLOP/s, meeting at the ridge, 100 FLOP/byte. MLP-256's three layers sit near 1 FLOP/byte at one environment; at 4,096 environments the 256 by 256 layer reaches the flat roof at 124 FLOP/byte, while the input layer stays at 50.6 and the output layer at 7.74, under their caps. (b) One forward pass drawn to scale: 15.17 microseconds at one environment, almost all of it three 5-microsecond launches, and 25.19 microseconds at 4,096 environments.">
  <text x="12" y="18" font-size="12" fill="currentColor">(a) MLP-256 on G-100’s roofline</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.15"><line x1="119.7" y1="44" x2="119.7" y2="246"/><line x1="259.8" y1="44" x2="259.8" y2="246"/><line x1="399.9" y1="44" x2="399.9" y2="246"/><line x1="540.0" y1="44" x2="540.0" y2="246"/><line x1="64" y1="217.2" x2="540" y2="217.2"/><line x1="64" y1="145.0" x2="540" y2="145.0"/><line x1="64" y1="72.8" x2="540" y2="72.8"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6" fill="none"><line x1="64" y1="44" x2="64" y2="246"/><line x1="64" y1="246" x2="540" y2="246"/></g>
  <text x="119.7" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">1</text>
  <text x="259.8" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">10</text>
  <text x="399.9" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">100</text>
  <text x="540.0" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">1000</text>
  <text x="58" y="221.2" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">1</text>
  <text x="58" y="149.0" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">10</text>
  <text x="58" y="76.8" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">100</text>
  <text x="302" y="274" font-size="11" fill="currentColor" text-anchor="middle">arithmetic intensity I (FLOP/byte), log scale</text>
  <text x="58" y="36" font-size="11" fill="currentColor" text-anchor="end">TFLOP/s</text>
  <polyline points="64.0,246.0 399.9,72.8 540.0,72.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <line x1="399.9" y1="72.8" x2="399.9" y2="246" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <text x="536.0" y="50.8" font-size="11" fill="currentColor" text-anchor="end">flat roof</text>
  <text x="536.0" y="64.8" font-size="11" fill="currentColor" text-anchor="end">P = 100 TFLOP/s</text>
  <text x="405.9" y="238" font-size="11" fill="currentColor">ridge I* = P/β = 100</text>
  <line x1="161.9" y1="198.5" x2="171.9" y2="223" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="150" y="234" font-size="11" fill="currentColor">slanted roof I × β, β = 1 TB/s</text>
  <text x="72" y="58" font-size="11" fill="currentColor">● N = 4,096     ○ N = 1</text>
  <text x="72" y="72" font-size="11" fill="currentColor" fill-opacity="0.85">• 256→256 at N = 4, 16, 64, 256, 1024</text>
  <circle cx="202.2" cy="174.7" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="281.3" cy="133.9" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="348.1" cy="99.5" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="390.3" cy="77.7" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="407.8" cy="72.8" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <text x="385.3" y="71.7" font-size="10" fill="currentColor" fill-opacity="0.85" text-anchor="end">256</text>
  <text x="410.8" y="64.8" font-size="10" fill="currentColor" fill-opacity="0.85">1024</text>
  <circle cx="118.6" cy="217.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="119.3" cy="217.5" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="112.4" cy="221.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="98" y1="121" x2="117.1" y2="212.6" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="72" y="104" font-size="11" fill="currentColor">N = 1: layers at 0.89–0.99 FLOP/byte,</text>
  <text x="72" y="118" font-size="11" fill="currentColor" fill-opacity="0.85">1% of the way to the ridge</text>
  <circle cx="244.3" cy="153.0" r="4" fill="currentColor"/>
  <circle cx="358.4" cy="94.1" r="4" fill="currentColor"/>
  <circle cx="413.1" cy="72.8" r="4" fill="currentColor"/>
  <text x="254.3" y="173.0" font-size="11" fill="currentColor" font-weight="bold">256→8: 7.74</text>
  <text x="254.3" y="187.0" font-size="11" fill="currentColor" fill-opacity="0.85">(cap 7.76)</text>
  <text x="391.9" y="134.1" font-size="11" fill="currentColor" font-weight="bold" text-anchor="end">64→256: 50.6</text>
  <text x="391.9" y="148.1" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="end">(cap 51.2)</text>
  <text x="421.1" y="90.8" font-size="11" fill="currentColor" font-weight="bold">256→256: 124</text>
  <text x="421.1" y="104.8" font-size="11" fill="currentColor" fill-opacity="0.85">compute-bound</text>
  <text x="12" y="294" font-size="12" fill="currentColor">(b) one forward pass, to scale</text>
  <rect x="76.0" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="156.0" y="308" width="1.2" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="156.5" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="236.5" y="308" width="2.1" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="238.6" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="318.6" y="308" width="1.2" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="76.0" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="156.0" y="348" width="42.5" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="198.5" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="278.5" y="348" width="85.9" height="18" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.6"/>
  <rect x="364.4" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="444.4" y="348" width="34.7" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <text x="70" y="321" font-size="11" fill="currentColor" text-anchor="end">N = 1</text>
  <text x="70" y="361" font-size="11" fill="currentColor" text-anchor="end">N = 4,096</text>
  <text x="76" y="339" font-size="11" fill="currentColor" fill-opacity="0.9">15.17 µs: launches 15 µs (98.9%), kernels 0.17 µs — 15.17 µs per environment</text>
  <text x="76" y="379" font-size="11" fill="currentColor" fill-opacity="0.9">25.19 µs = 15 µs of launches + 2.65 + 5.37 + 2.17 µs — 6.15 ns per environment</text>
  <line x1="76" y1="390" x2="492.0" y2="390" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="76.0" y1="390" x2="76.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="76.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0</text>
  <line x1="156.0" y1="390" x2="156.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="156.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">5</text>
  <line x1="236.0" y1="390" x2="236.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="236.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">10</text>
  <line x1="316.0" y1="390" x2="316.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="316.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">15</text>
  <line x1="396.0" y1="390" x2="396.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="396.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">20</text>
  <line x1="476.0" y1="390" x2="476.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="476.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">25</text>
  <text x="498.0" y="405" font-size="10" fill="currentColor" fill-opacity="0.8">µs</text>
  <rect x="76" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <text x="100" y="420" font-size="11" fill="currentColor">launch, 5 µs</text>
  <rect x="206" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <text x="230" y="420" font-size="11" fill="currentColor">memory-bound kernel</text>
  <rect x="376" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.6"/>
  <text x="400" y="420" font-size="11" fill="currentColor">compute-bound kernel</text>
</svg>

MLP-256's three layers on G-100's roofline: the slanted roof is 1 TB/s times the intensity, the flat roof 100 TFLOP/s, and they meet at the ridge, 100 FLOP/byte. At one environment all three layers sit near 1 FLOP/byte, one percent of the way to the ridge; at 4,096 the 256×256 layer crosses it (124 FLOP/byte, compute-bound) while the input and output layers stay memory-bound under their caps of 51.2 and 7.76. Below, one forward pass to scale: 15.17 µs at $N=1$, of which 15 µs are three launches, and 25.19 µs at $N=4{,}096$, 6.15 ns per environment.

### Worked case · 대상으로 한 번 끝까지

This is the homework object at both of its scales. The problem set moves the ridge, widens the network and changes the batch; do the catalog version here first, so the set is a change of knobs rather than a first derivation. Three terms are glossed here and derived later: a kernel's **arithmetic intensity** $I=F/B$ is its FLOPs per byte of DRAM traffic (§3); on the **roofline** a kernel's time is at least the larger of $F/P$ and $B/\beta$, memory-bound when the second is larger and compute-bound otherwise (§3); and every kernel also pays the launch overhead $t_L$ before it runs (§4).

**Count one layer.** A layer multiplies an $N\times n_{\text{in}}$ matrix of activations by the transpose of its $n_{\text{out}}\times n_{\text{in}}$ weight matrix. Every weight takes part in one multiply and one add per environment — the forward product of [[03-deep-learning/foundations/training-at-scale|1.3 §6]], 2 FLOPs per weight — and the kernel moves each operand once, at $e=2$ bytes per number:

$$F_\ell=2Nn_{\text{in}}n_{\text{out}},\qquad B_\ell=e\big(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}}\big),\qquad t_\ell=t_L+\max\Big(\frac{F_\ell}{P},\ \frac{B_\ell}{\beta}\Big)$$

since the weights are read once whatever $N$ is, while the inputs and outputs grow with it.

**One environment.** Layer 2 has $F=2\cdot1\cdot256\cdot256=131{,}072$ FLOPs and $B=2(65{,}536+256+256)=132{,}096$ bytes, so $I=0.992$ FLOP/byte: the weights are nearly all the traffic and each is used once, one FLOP per byte, like the decoding of 1.3 §11. Under the two roofs $F/P=0.00131$ µs and $B/\beta=0.13210$ µs, so the layer is memory-bound. All three layers:

| layer | $n_{\text{in}}\to n_{\text{out}}$ | $F$ (FLOP) | $B$ (bytes) | $I$ (FLOP/byte) | $F/P$ (µs) | $B/\beta$ (µs) | bound |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | $64\to256$ | 32,768 | 33,408 | 0.981 | 0.00033 | 0.03341 | memory |
| 2 | $256\to256$ | 131,072 | 132,096 | 0.992 | 0.00131 | 0.13210 | memory |
| 3 | $256\to8$ | 4,096 | 4,624 | 0.886 | 0.00004 | 0.00462 | memory |
| all | | 167,936 | 170,128 | 0.987 | | 0.1701 | |

$$t(1)=3t_L+\sum_\ell\frac{B_\ell}{\beta}=15+0.1701=15.170\ \mu\text{s}$$

because each of the three kernels pays $t_L=5$ µs before it runs. The network's own traffic takes 0.17 µs; 98.9% of the pass is launching. It does 167,936 FLOPs in 15.17 µs, 11.1 GFLOP/s — about one ten-thousandth of $P$.

**4,096 environments.** Now every weight read is used 4,096 times:

| layer | $n_{\text{in}}\to n_{\text{out}}$ | $F$ (FLOP) | $B$ (bytes) | $I$ (FLOP/byte) | $F/P$ (µs) | $B/\beta$ (µs) | bound |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | $64\to256$ | 134,217,728 | 2,654,208 | 50.568 | 1.34218 | 2.65421 | memory |
| 2 | $256\to256$ | 536,870,912 | 4,325,376 | 124.121 | 5.36871 | 4.32538 | **compute** |
| 3 | $256\to8$ | 16,777,216 | 2,166,784 | 7.743 | 0.16777 | 2.16678 | memory |
| all | | 687,865,856 | 9,146,368 | 75.206 | | | |

Layer 2 is now above the ridge, $124.1>100$, and runs under the flat roof; layers 1 and 3 are still below it. Adding each kernel's larger time,

$$t(4096)=3t_L+2.654+5.369+2.167=15+10.190=25.190\ \mu\text{s}$$

which is $25.19/4096=6.15$ ns per environment against 15.17 µs at $N=1$: 2,467 times cheaper per environment for 1.66 times the wall-clock time. The pass reaches $687.9\ \text{MFLOP}/25.19\ \mu\text{s}=27.3$ TFLOP/s, 27% of $P$, and the launches are still 60% of it.

**Why the thin layers stay memory-bound.** Divide $B_\ell$ by $F_\ell$: in bf16, $1/I_\ell=1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})$ (§4), so as $N$ grows a layer's intensity rises toward the cap $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$ and never past it — 128 for layer 2, 51.2 for layer 1 and 7.76 for layer 3. The output layer does $2\cdot256\cdot8=4{,}096$ FLOPs per environment and moves $2(256+8)=528$ bytes of activations for them, $4{,}096/528=7.76$; no batch changes that ratio, so a layer whose cap is below the ridge is memory-bound at every $N$.

**The average hides the split.** The whole pass at $N=4{,}096$ has $687.9\ \text{M}/9.15\ \text{M}=75.2$ FLOP/byte, below the ridge — as if all of it were memory-bound, while the layer holding 78% of the FLOPs is compute-bound. Intensity belongs to a kernel, not to a network. §9 prints every number of both tables.

### 1. Why a GPU: many threads, warps and latency hiding

*In one sentence:* a GPU is fast by running tens of thousands of threads at once in groups of 32, and it keeps busy while some of them wait for memory by switching to others that are ready.

A CPU core is built to finish one thread's instructions as soon as possible, with large caches and elaborate control logic to avoid waiting. A GPU makes the opposite trade. It is designed to run thousands of threads in parallel, giving up single-thread speed for total throughput, and it spends more of its transistors on arithmetic units and fewer on caches and flow control than a CPU does (CUDA Programming Guide §1.1.2). The price is that a GPU is fast only when it is handed thousands of independent pieces of work. MLP-256's layer 2 at $N=4{,}096$ has $4{,}096\times256=1{,}048{,}576$ outputs, each a 256-term dot product — ample work. At $N=1$ it has 256.

**How the work is written down.** CUDA expresses parallel work as a kernel, which the host launches with an execution configuration inside triple chevrons, `kernel<<<G, B>>>(args)`: $G$ blocks of $B$ threads each, every thread running the kernel's body once. Four built-in variables tell a thread who it is — `threadIdx`, its index within its block; `blockIdx`, its block's index within the grid; `blockDim` and `gridDim`, the sizes of the block and of the grid — and a kernel's first line usually combines them into a global index (Programming Guide §2.1.2). Two optional arguments may follow inside the chevrons: the dynamic shared memory each block gets, and the stream the launch is queued on. The launch returns to the host at once, before the kernel has run.

> **The CUDA execution model, defined.** The **CUDA execution model** is the *contract between a program and an NVIDIA GPU about how parallel work is organized and scheduled* — a programming model, not a library and not a piece of hardware. Four defining conditions. A **kernel** is a function marked `__global__`, launched from the host and executed on the device by many threads, every thread running the same code on the index it computes for itself; the launch is asynchronous, so the host continues at once. The threads come in **blocks** of up to 1,024; all threads of a block run on one streaming multiprocessor (SM), where they can share on-chip memory and wait for one another at a barrier. The blocks form a **grid**, and the program must be correct in whatever order the blocks run — in parallel or one after another — so no block may wait for another. And the SM runs each block's threads in **warps** of 32 consecutive threads that issue one instruction at a time together, single instruction, multiple threads (SIMT); when threads of a warp take different branches, the warp runs each path in turn with the threads not on it masked off (Programming Guide §1.2.2.1–§1.2.2.2).
>
> $$i=b\,B+t,\qquad 0\le t<B\le1024,\qquad G=\Big\lceil\frac{n}{B}\Big\rceil,\qquad \text{warps per block}=\Big\lceil\frac{B}{32}\Big\rceil$$
>
> where $t$ is `threadIdx.x`, $b$ is `blockIdx.x`, $B$ is `blockDim.x`, $G$ is `gridDim.x`, $n$ is the number of elements and $i$ the element a thread takes — so $GB\ge n$ threads start, and the spare threads of the last block are kept out by a bounds check, `if (i < n)`, which the Programming Guide notes costs little (§2.1.2.3.1).
>
> - **Example**: MLP-256's layer 2 at $N=4{,}096$ written as one thread per output: $n=4{,}096\times256=1{,}048{,}576$, and with $B=256$ the grid has $G=4{,}096$ blocks of 8 warps, 32,768 warps in all. Thread $i$ computes the dot product of environment $\lfloor i/256\rfloor$'s activations with row $i\bmod256$ of $W_2$.
> - **Non-example**: a Python loop that calls the network once per environment. That is 4,096 batch-1 passes, each paying its own launches (§4), not one launch with a thread per output.
> - **Non-example**: a kernel in which block 7 waits for a value that block 3 writes. Blocks may run in any order, and block 3 may not have started; a step that needs every block's result belongs in a second kernel, which starts only after the first has finished.
> - **Why it matters**: every GPU simulator, every framework operator and every Warp kernel is written in this model, so reading one starts with the same two questions — which element does thread $i$ own, and which threads must wait for which.

**What a warp does with a branch.** A physics kernel that advances one environment per thread might contain `if (done[i]) reset(i); else step(i);`. In a warp whose 32 environments include three that have just ended, the warp runs `reset` with 29 threads masked off and then `step` with 3 masked off, so all 32 pay for both paths. That is one reason to reset finished environments in a separate batched step over their indices, as Isaac Lab's environments do (§5), rather than inside the physics step.

**Why tens of thousands of threads.** A load from global memory takes a long time to come back, and a GPU does not try to make that one thread wait less. Each SM keeps many warps resident, their registers and program counters held on chip for their whole life, so switching from one warp to another costs nothing; at every issue cycle a scheduler picks a warp whose next instruction is ready (Programming Guide §3.2.2.2). The Programming Guide's advice follows: keep occupancy — active warps as a fraction of the SM's maximum — as high as possible, because that hides latency (§2.3.7). The waiting is not shortened; it is filled.

> **Latency hiding, defined.** **Latency hiding** is a *property of how a GPU schedules warps* — the way it keeps its arithmetic and memory units busy while individual threads wait — not a cache, and not a speedup of any single thread. Four defining conditions. Many warps are **resident** on each SM at once. Each resident warp's **execution context stays on chip**, so switching from one warp to another costs no time. At every instruction-issue cycle a **scheduler picks a warp whose next instruction is ready**, so a warp waiting on memory is simply not picked. And the kernel has **enough independent work in flight** to cover the wait: by Little's law, a memory system that delivers $\beta$ bytes per second with latency $\ell$ runs at full speed only if $\beta\ell$ bytes are requested and not yet returned at every moment.
>
> $$Q=\beta\,\ell,\qquad t_{\text{mem}}\ \ge\ \max\Big(\frac{B}{\beta},\ \ell\Big)$$
>
> where $Q$ is the bytes in flight, $\beta$ the DRAM bandwidth, $\ell$ the time of one memory round trip, $B$ the bytes a kernel moves and $t_{\text{mem}}$ its memory time — so at G-100's $\beta=10^{12}$ bytes/s every microsecond of latency needs a megabyte in flight, and a kernel whose whole traffic is below $\beta\ell$ cannot finish in less than about one latency, however few bytes it moves.
>
> - **Example**: MLP-256's layer 2 at $N=4{,}096$ moves 4.33 MB, 4.33 µs of G-100's bandwidth, and offers 32,768 warps of independent work; the SMs keep as many of them resident as they can hold — a number that depends on the GPU and that G-100 does not freeze — and switch among those.
> - **Non-example**: the same layer at $N=1$ moves 132,096 bytes, 0.13 µs of bandwidth, from 8 warps of work at one thread per output. For any latency above 0.13 µs that is less than one latency's worth of bytes, so its time is set by $\ell$, not by $B/\beta$ — one more reason the slanted roof overstates what a batch-1 kernel attains.
> - **Non-example**: a CPU's large cache. It avoids the wait for data it has kept; latency hiding tolerates the wait by doing other work, and so needs the other work to exist.
> - **Why it matters**: a GPU is fast only with parallel slack, which a single robot's observation lacks and a simulator's 4,096 environments supply (§4, §5).

### 2. The memory hierarchy and coalesced access

*In one sentence:* data lives in a hierarchy from registers to host memory, each level larger and slower than the one above, and a warp's loads from global memory are cheap only when its 32 threads read neighbouring addresses.

| level | where it sits | who can use it | lives as long as | what to know |
|---|---|---|---|---|
| registers | on the SM | one thread | the thread | the fastest storage; the compiler assigns it (Programming Guide §2.3.3.3) |
| local memory | device DRAM, through the caches | one thread | the thread | where registers spill; as slow as global memory (§2.3.3.4) |
| shared memory | on the SM, in the same store as L1 | the threads of one block | the block | declared `__shared__`; much higher bandwidth and lower latency than global memory; read after a `__syncthreads()` barrier (§2.3.3.2) |
| L1 and L2 caches | L1 on each SM, L2 shared by all SMs | automatic | — | catch repeated reads before they reach DRAM (§1.2.3.3.1) |
| global memory | the GPU's DRAM | every thread of every kernel; the host through copies | until freed | read in 32-byte sectors (§2.3.4.1); $\beta=1{,}000$ GB/s on G-100 |
| host memory | the CPU's DRAM | the host; the GPU through copies | until freed | $25$ GB/s to G-100; pinned memory is the fastest to copy (Best Practices §10.1.1) |

Two gaps in that table shape the rest of the page. *On chip against off chip*: shared memory has much higher bandwidth and lower latency than global memory (Best Practices §10.2.3), so a kernel that loads a value once into shared memory and reuses it there saves global traffic — the tiling of §6. *Device against host*: G-100's DRAM delivers forty times what its host link does; NVIDIA's own illustration of the same gap is 898 GB/s of device-memory bandwidth on a Tesla V100 against 16 GB/s over PCIe x16 Gen3 (Best Practices §10.1).

**How global memory is read.** Global memory moves in 32-byte transactions, called sectors, and a warp's 32 loads are served together: on devices of compute capability 6.0 and newer, the accesses of a warp combine into as many 32-byte transactions as it takes to cover them (Best Practices §10.2.1). What costs bandwidth is therefore not how many threads load but how many distinct sectors their addresses fall in.

> **Coalesced access, defined.** A warp's access to global memory is **coalesced** when its 32 threads' addresses fall into as few 32-byte sectors as their total size allows — a *property of a warp's access pattern*, decided by the addresses the threads compute; not a property of the data type, and not of the kernel as a whole. Three defining conditions. The unit of transfer is the **32-byte sector**: a warp's access costs one transaction per distinct sector its threads touch. The 32 threads' requests are **served together**, combined into exactly the transactions they need. And **efficiency is useful bytes over moved bytes**, which reaches 100% only when the bytes the warp touches fill whole aligned sectors — neighbouring threads reading neighbouring addresses from an aligned start is the usual case, and any permutation within those sectors costs the same (Best Practices §10.2.1.1).
>
> $$S=\min\Big(w,\ \Big\lceil\frac{w\,\sigma e}{s}\Big\rceil\Big),\qquad \eta=\frac{w\,e}{s\,S}$$
>
> where $w=32$ threads per warp, $s=32$ bytes per sector, $e$ the bytes per element, $\sigma$ the stride between consecutive threads' elements, $S$ the sectors a warp needs from an aligned start (for power-of-two strides) and $\eta$ the fraction of moved bytes the threads use — so in fp32 a warp at stride 1 needs 4 sectors and uses all 128 bytes, and at any stride of 32 bytes or more it needs 32 sectors and uses 128 of 1,024, 12.5%: the two cases the Programming Guide works through (§2.3.4.1).
>
> - **Example**: MLP-256's $W_2$ in bf16, stored row by row. A warp reading 32 consecutive weights of one row ($\sigma=1$, $e=2$) needs $\lceil64/32\rceil=2$ sectors and uses all 64 bytes.
> - **Non-example**: the same warp reading one column, thread $k$ taking $W_2[k,j]$. The stride is 256 elements, 512 bytes, so each thread lands in its own sector: 32 sectors, 1,024 bytes moved for 64 used, 6.25% — sixteen times the traffic for the same 32 numbers.
> - **Non-example**: stride 1 in fp32 but starting 4 bytes past a sector boundary: 5 sectors instead of 4 (Best Practices §10.2.1.2). The CUDA runtime aligns its allocations to at least 256 bytes, so the misalignment comes from the indexing, not from the allocator.
> - **Why it matters**: the roofline's $\beta$ assumes every moved byte is used. A kernel reading $W_2$ by columns has an effective bandwidth of $\eta\beta=62.5$ GB/s, and its slanted roof sits sixteen times lower than the one in the picture.

The lab (§9) counts the sectors for every stride from the addresses themselves. The steps are as the formula says: fp32 needs 4, 8, 16 and then 32 sectors at strides 1, 2, 4 and 8, where 8 elements are 32 bytes; bf16 reaches 32 sectors only at stride 16. Best Practices §10.2.1.4 describes the same fall — 50% efficiency at stride 2, then less until each thread has its own sector — and concludes that non-unit strides should be avoided whenever possible.

**Host–device transfer.** Copying 4,096 environments' observations, $4{,}096\times64\times2=524{,}288$ bytes, takes 0.52 µs from G-100's DRAM and 20.97 µs over its host link, before the fixed overhead every transfer pays. NVIDIA's guide draws three rules from this (Best Practices §10.1): keep data on the device between kernels — even when that means running a kernel on the GPU that is no faster there than on the CPU; create intermediate data on the device and never copy it to the host; and batch many small transfers into one large one. Copies from pinned (page-locked) host memory reach the highest bandwidth and can run asynchronously, overlapping computation (§10.1.1–§10.1.2), but pinned memory is scarce and overusing it slows the whole system. On a Jetson the CPU and the GPU share one DRAM, so this link does not exist (§8).

### 3. Arithmetic intensity and the roofline

*In one sentence:* a kernel is limited either by how fast the GPU computes or by how fast it brings in data, and its FLOPs per byte — its arithmetic intensity — say which, against a threshold that belongs to the GPU.

A kernel needs time for its arithmetic, at best $F/P$, and time to move its data, at best $B/\beta$. If the two overlap perfectly, the larger decides. Their ratio separates into a property of the kernel and a property of the machine,

$$\frac{F/P}{B/\beta}=\frac{F/B}{P/\beta}$$

so the kernel is limited by computation exactly when its FLOPs per byte exceed the machine's FLOPs per byte.

> **Arithmetic intensity, defined.** The **arithmetic intensity** of a kernel is the *ratio of the arithmetic it does to the bytes it moves between DRAM and the chip* — a property of one kernel as implemented, on a given data layout and batch; not a property of the GPU, and not of the model's mathematics alone. Three defining conditions. The numerator counts the **useful floating-point operations**, two per multiply-add. The denominator counts **DRAM traffic**: the bytes that cross between global memory and the SMs after the caches have caught repeated reads — not the loads the threads issue, which §6 counts separately. And both are counted **for one kernel**: two kernels have two intensities, and a ratio of whole-network totals is the intensity of no kernel.
>
> $$I=\frac{F}{B},\qquad I_\ell(N)=\frac{2Nn_{\text{in}}n_{\text{out}}}{e\big(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}}\big)}$$
>
> where $F$ is FLOPs, $B$ bytes, and the second form is a dense layer's on a batch of $N$ at $e$ bytes per number, with each operand moved once — so the intensity grows with the batch, because only the weights are shared across it, and falls with $e$, because the same arithmetic then moves more bytes.
>
> - **Example**: MLP-256's layer 2 at $N=1$: $131{,}072/132{,}096=0.992$ FLOP/byte; at $N=4{,}096$: 124.1.
> - **Non-example**: the whole network at $N=4{,}096$, $687.9\ \text{M}/9.15\ \text{M}=75.2$ FLOP/byte, which would put the pass below G-100's ridge although the layer with 78% of its FLOPs is above it.
> - **Non-example**: counting the loads the threads issue. The naive kernel of §6 issues 1.07 GB of loads for layer 2 at $N=4{,}096$, whose DRAM traffic can be as little as 4.33 MB; its intensity is set by what reaches DRAM.
> - **Why it matters**: it is the only property of a kernel the roofline needs, and the one that batching (§4), tiling (§6) and fusion (§8) change.

> **The roofline model, defined.** The **roofline model** is an *upper bound on a kernel's throughput as a function of its arithmetic intensity, drawn for one machine* — a visual performance model (Williams, Waterman and Patterson, 2009); not a prediction that the bound is reached, and not a benchmark. Four defining conditions. The machine is summarized by **two ceilings**, its peak arithmetic rate $P$ and its peak DRAM bandwidth $\beta$, for the precision and mode the kernel actually uses. A kernel of intensity $I$ **cannot exceed either**: at most $P$ FLOP/s, and at most $I\beta$ FLOP/s, since it gets $I$ FLOPs from each byte and at most $\beta$ bytes per second. The two roofs meet at the **ridge point** $I^\star=P/\beta$, the least intensity at which peak is reachable; a kernel below it is **memory-bound** and one above it **compute-bound**. And the bound assumes **arithmetic and data movement overlap perfectly**, with nothing else in the way — no launches, no latency, no synchronization.
>
> $$\Pi(I)=\min\big(P,\ I\beta\big),\qquad I^\star=\frac{P}{\beta},\qquad t\ \ge\ \max\Big(\frac{F}{P},\ \frac{B}{\beta}\Big)$$
>
> where $\Pi$ is the attainable FLOP/s and $t$ a kernel's time — so on log–log axes the bound is a line of slope one that turns flat at the ridge, which is the picture's shape.
>
> - **Example**: G-100's ridge is $10^{14}/10^{12}=100$ FLOP/byte. MLP-256's layer 2 at $N=1$ (0.992) can attain at most 0.99 TFLOP/s, 1% of peak; at $N=4{,}096$ (124.1) it reaches the flat roof, 100 TFLOP/s.
> - **Non-example**: MLP-256's whole pass at $N=1$ read as a time. The roofline gives 0.17 µs; the three launches add 15 µs. "Nothing else in the way" is the condition that fails.
> - **Non-example**: a roof taken from another precision or mode. Jetson Thor's 2,070 TFLOPS is a sparse fp4 rating ([[03-deep-learning/foundations/training-at-scale|1.3 §11]]); a dense bf16 kernel's flat roof sits below it by a factor its datasheet, not this page, supplies — and with it the ridge moves left.
> - **Why it matters**: it turns "is this kernel fast?" into "under which roof is it, and how far below?", and so says which remedy can work: more intensity below the ridge (batching, tiling, fusion), less arithmetic or a faster format above it.

The terms are the paper's except one: Williams et al. call the ratio *operational intensity* and measure it against DRAM traffic, and NVIDIA's Nsight Compute, which can draw a roofline chart for a kernel it profiles, calls the same ratio arithmetic intensity (§7).

**Reading the picture.** At $N=1$ the three layers sit at 0.89–0.99 FLOP/byte, a hundredth of the way to G-100's ridge, so at most they attain 0.9–1 TFLOP/s. At $N=4{,}096$ they spread out: the output layer stops at 7.74, under its cap of 7.76; the input layer at 50.6, under 51.2; and layer 2 at 124.1 is past the ridge, attaining the flat roof. Their times add; their intensities do not average.

**The same physics on the robot.** [[03-deep-learning/foundations/training-at-scale|1.3 §11]] found a 3B policy decoding one token at batch 1 on Jetson Thor at about 1 FLOP per byte in bf16, against a ridge near 7,600: memory-bound, so its time is its bytes over 273 GB/s, 22.0 ms for 6.0 GB. MLP-256 at $N=1$ sits at the same intensity for the same reason — every weight read once and used once — and is memory-bound too, but its 170,128 bytes take 0.17 µs at G-100's bandwidth and 0.62 µs at Thor's. "Memory-bound" is true of both; it decides the time of only the first. What 1.3 §11 could not do is batch: one robot has one observation, while a simulator has 4,096 (§4, §5).

**What the roofline leaves out.** The launches, which §4 prices; the latency of a kernel too small to fill the memory pipe (§1); the caches — a pass that reads the same 168 KB of weights over and over may find them in the L2 cache, which makes the memory term smaller still; and every synchronization with the host (§7). For MLP-256 at $N=1$ the first of these is 98.9% of the time.

### 4. Batching: reusing each weight across environments

*In one sentence:* passing $N$ environments through a layer at once reads each weight once for all of them, which raises the intensity about $N$-fold until the activations' own traffic caps it, and pays each launch once instead of $N$ times.

Batching is §3's lever for a kernel below the ridge, and its algebra is one line. Invert the intensity of a dense layer and split the fraction:

> **Batched evaluation, defined.** **Batched evaluation** is the *execution of one network on $N$ independent inputs as a single pass whose tensors carry a leading batch axis* — a way of scheduling the same computation, not a larger model and not an approximation. Three defining conditions. The $N$ inputs go through **the same function with the same weights**, so a weight read once serves all of them. The inputs are **independent**: none needs another's output, so all $N$ can be in flight at once. And the batch is issued as **one kernel per operation**, so the per-kernel costs — the launch, the weight traffic — are paid once per pass instead of once per input.
>
> $$\frac{1}{I_\ell(N)}=\frac{e}{2}\Big(\frac1N+\frac{1}{I_{\ell,\infty}}\Big),\qquad I_{\ell,\infty}=\frac{n_{\text{in}}n_{\text{out}}}{n_{\text{in}}+n_{\text{out}}}$$
>
> where $I_{\ell,\infty}$ is the layer's cap and $e$ the bytes per number — so in bf16 ($e=2$) the intensity is $N$ and the cap combined like two resistors in parallel: close to $N$ while $N\ll I_{\ell,\infty}$, close to the cap once $N\gg I_{\ell,\infty}$, and never above the smaller of the two.
>
> - **Example**: MLP-256's layer 2, cap 128. At $N=16$ the intensity is 14.22, near $N$; at $N=4{,}096$ it is 124.1, near the cap; it crosses G-100's ridge where $1/100=1/N+1/128$, at $N=457.1$.
> - **Non-example**: the time steps of one environment. Step $t+1$ needs the state step $t$ produced, so a simulator can batch across environments but not across time, and a control loop is sequential however large the GPU.
> - **Non-example**: $N$ environments driven by $N$ different policies — a population, or per-robot fine-tuned copies. There are no shared weights to reuse, and each network pays its own weight traffic and its own launches.
> - **Why it matters**: it is the reason a simulator's 4,096 environments are cheap for a policy and a single robot's one observation is expensive per decision, and it says where the benefit ends — at the cap, which only removing the activation traffic can lift (§8).

The other fixed cost that batching spreads is not in the roofline at all.

> **Launch overhead, defined.** The **launch overhead** of a kernel is the *fixed time the host spends issuing it* — the driver's preparation of a kernel for execution, paid once per kernel issued, whatever the kernel computes; not the kernel's own run time and not a data transfer. Three defining conditions. It is **per kernel**, not per thread or per byte: a launch of a million threads pays it once, as a launch of one does. It is **paid on the host**, before the device can start the kernel. And it matters when **kernels are short**: the CUDA Programming Guide notes that for a kernel with a short execution time it can be a significant fraction of the end-to-end time (§4.2).
>
> $$t_{\text{pass}}=K\,t_L+\sum_{k=1}^{K}\max\Big(\frac{F_k}{P},\ \frac{B_k}{\beta}\Big)$$
>
> where $K$ is the number of kernels in the pass and $t_L$ the overhead per launch — the serial model, in which each kernel waits for its own launch: a sum that §7's overlap of launches with running kernels can only shorten.
>
> - **Example**: MLP-256 is $K=3$ kernels, so every pass pays 15 µs on G-100, against 0.17 µs of roofline time at $N=1$ and 10.19 µs at $N=4{,}096$.
> - **Non-example**: the first call's setup. Creating the CUDA context and compiling code happen once, at the first call that needs them (Programming Guide §2.1.6); they are a warm-up cost, not a per-launch one.
> - **Non-example**: a synchronous copy, `cudaMemcpy`. It also has a fixed part, but it moves bytes over the host link (§2), and the host waits for it where it does not wait for a launch.
> - **Why it matters**: for a small network it, not the arithmetic, sets the time of a step, and the three remedies — fewer kernels by fusion (§8), one launch for many kernels by a CUDA graph (§7), and batching — act on it differently.

**The sweep.** The lab runs MLP-256 through the serial model at eight batches:

| $N$ | $I$, layer 1 | $I$, layer 2 | $I$, layer 3 | layers past the ridge | roofline time (µs) | with 3 launches (µs) | per environment (ns) | launches' share |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.98 | 0.99 | 0.89 | 0 | 0.170 | 15.170 | 15,170.13 | 98.9% |
| 4 | 3.71 | 3.88 | 2.64 | 0 | 0.177 | 15.177 | 3,794.18 | 98.8% |
| 16 | 12.19 | 14.22 | 5.22 | 0 | 0.203 | 15.203 | 950.19 | 98.7% |
| 64 | 28.44 | 42.67 | 6.92 | 0 | 0.308 | 15.308 | 239.19 | 98.0% |
| 256 | 42.67 | 85.33 | 7.53 | 0 | 0.729 | 15.729 | 61.44 | 95.4% |
| 1,024 | 48.76 | 113.78 | 7.70 | 1 | 2.575 | 17.575 | 17.16 | 85.3% |
| 4,096 | 50.57 | 124.12 | 7.74 | 1 | 10.190 | 25.190 | 6.15 | 59.5% |
| 16,384 | 51.04 | 127.01 | 7.75 | 1 | 40.648 | 55.648 | 3.40 | 27.0% |

**Reading the sweep.** Four things the algebra predicted and the numbers show.

- **Intensity tracks $N$, then the cap.** At $N=4$ the three layers sit at 3.71, 3.88 and 2.64 — roughly $N$, pulled down by each layer's $1/I_\infty$ term, most for the output layer whose cap is 7.76. By $N=64$ the output layer is at 6.92, already 89% of its cap; layer 1 approaches 51.2 more slowly and layer 2 128 more slowly still, crossing the ridge between $N=256$ (85.3) and $N=1{,}024$ (113.8), at 457.1.
- **The time hardly moves until the launches are shared out.** From $N=1$ to $N=256$ the pass goes from 15.17 to 15.73 µs, 4% longer for 256 times the work, because the launches are 95–99% of it. The kernels' own time first equals the launches' 15 µs at $N=6{,}037$; the popular batch of 4,096 is still launch-dominated, 59.5%.
- **The cost per environment falls about 4,500-fold** from $N=1$ to $N=16{,}384$, from 15.17 µs to 3.40 ns; by then the pass is 73% kernel time, and doubling $N$ again doubles the kernels' 40.65 µs but lengthens the pass only 1.73-fold, from 55.65 to 96.26 µs, because the 15 µs of launches stay fixed.
- **This is what a policy costs inside a GPU simulator.** Rudin et al. timed each part of an environment step against the number of robots and found the policy's inference, with the actuator network, nearly constant in time while the simulation grew (their Appendix A.1). They do not say why; this page's reading is that it is the flat, launch-dominated part of this table (§5).

What is left after batching — the launches and the capped thin layers — is what CUDA graphs (§7) and fusion (§8) attack.

### 5. Parallel simulation for robot learning

*In one sentence:* a vectorized simulator keeps thousands of environments as one batch of arrays on the GPU, so physics, rewards, resets and the policy all run as batched kernels and nothing crosses to the CPU inside the loop.

On-policy reinforcement learning, PPO for instance ([[02-foundations/rl-basics|7. RL Basics §4]]), alternates two phases: collect a batch of experience by stepping environments with the current policy, then update the policy on that batch. Collection is a loop — observe, act, advance the physics, compute rewards, reset the environments whose episode has ended ([[02-foundations/rl-basics|7. RL Basics §1]]) — run thousands of times per update. Where each stage runs decides what the loop costs.

**The split pipeline.** With the simulator on the CPU and the policy on the GPU, every step moves the observations up the host link and the actions down it. At $N=4{,}096$ on G-100 that is 20.97 µs up and 2.62 µs down, 23.59 µs per step before the per-transfer overheads and before the CPU has simulated anything, against 17.54 µs for the policy's own pass when its launches overlap (§7). And the download synchronizes: the host cannot step the physics until the policy's actions arrive, and the GPU cannot run the next pass until the host's physics is done, so each side idles while the other works.

> **Vectorized environment, defined.** A **vectorized environment** is a *simulator interface that holds $N$ copies of a task as one batched state and advances them together* — an organization of data and kernels, not a faster physics method and not $N$ simulator processes. Four defining conditions. The state is **stored as arrays with a leading environment axis**, on the device that computes on it. One step call **advances all $N$ environments**, with the same time step, as batched kernels. Environments **terminate and reset individually**: those that ended are reset by index while the rest continue, so no environment waits for another's episode. And observations, rewards and termination flags are **returned as batched device arrays**, handed to the policy without passing through the host.
>
> $$D=N\,n_{\text{steps}},\qquad \text{samples per second}=\frac{N\,n_{\text{steps}}}{t_{\text{update}}}$$
>
> where $D$ is the batch one policy update learns from, $n_{\text{steps}}$ the steps each environment takes per update and $t_{\text{update}}$ the wall-clock time of one collect-and-learn cycle — so throughput grows with $N$ for as long as a step's time does not, which is §4's sweep applied to physics as well as to the policy.
>
> - **Example**: Rudin et al.'s final ANYmal policy, trained with $N=4{,}096$ robots and a batch of $D=98{,}304$, 24 steps per robot per update, for 1,500 updates in under 20 minutes on one RTX A6000 — at least $98{,}304\times1{,}500/1{,}200\ \text{s}=122{,}880$ samples per second, learning included.
> - **Non-example**: $N$ CPU simulator processes behind a batched interface, whose observations are stacked and copied to the GPU each step. The API is vectorized; the data is not, and every step pays the round trip above.
> - **Non-example**: resetting all $N$ environments whenever any one ends. The finished ones restart, but so do the others, and every episode is cut to the shortest.
> - **Why it matters**: it is what makes the numbers in robot-learning papers possible, and its conditions are exactly what a custom simulator must meet to be worth writing.

**The evidence.** Makoviychuk et al. built Isaac Gym on this principle: physics simulation and policy training both on the GPU, passing data from physics buffers to PyTorch tensors without going through the CPU, and they report training 2–3 orders of magnitude faster than with a CPU simulator feeding a GPU network. Rudin et al. used it to train ANYmal to walk on flat terrain in under four minutes and on rough terrain in twenty, against the twelve hours and more of earlier work, and their appendix times each part of an environment step as the number of robots grows. The simulation is the most expensive part and grows slowly with the robots; computing observations and rewards comes second and also grows slowly; the policy's inference and the actuator network take nearly constant time. Training time scaled nearly linearly up to about 4,000 robots, after which the simulator's throughput gains slowed. Their claim is wall-clock time on one GPU, not sample efficiency — which is how [[04-robotics/legged-locomotion|18. Legged Locomotion §3]] reads it.

**Resets and synchronization, the usual bottleneck.** Once everything is on the GPU, the remaining ways to lose the speed are on the host: a Python `if` over the termination flags, an `.item()` per step for logging, a reset done on the CPU, a statistic printed every step — each one a synchronization (§7). Isaac Lab's direct workflow shows the batched alternative: `_get_dones()` returns terminations and time-outs as a pair of boolean tensors, and `_reset_idx(env_ids)` resets exactly the listed environments while the others run on. Rudin et al. keep the two kinds of ending apart for learning too: a time-out is not a failure, so the critic's target is bootstrapped with its own prediction there.

**The simulators.** MJX runs MuJoCo in JAX on any accelerator XLA supports, and its documentation states the batching trade plainly: it works best with thousands or tens of thousands of scenes in parallel, and a single scene can be about ten times slower than MuJoCo, which is tuned for the CPU. MJX-Warp targets NVIDIA GPUs and removes MJX-JAX's bottlenecks around contacts and constraints, but has no automatic differentiation; MuJoCo Warp itself is maintained by Google DeepMind and NVIDIA as part of Newton, on which Isaac Lab can also run. Which one to use, and the version traps, are [[06-research-practice/simulators-benchmarks-datasets|7. Simulators §2]].

**When you would write one.** The general-purpose simulators above do not model soil; the leading real-time soil models are validated only to roughly 10–25% of a particle-level reference, and no simulator has a documented model of construction materials ([[06-research-practice/simulators-benchmarks-datasets|7. Simulators §4–§5]]). A thesis that needs a custom soil or deformable model at scale writes GPU kernels itself, in one of two styles. In NVIDIA Warp, the physics of one environment, or one particle, is a Python function that runs once per thread and is compiled to CUDA on first launch (§6). In JAX, one environment's step is a pure array function, batched over the environment axis with `jax.vmap` and compiled with `jax.jit` — MJX's approach. Either way this page's rules apply: one kernel over all environments, the data kept on the device, no host-side branch inside the loop.

### 6. Two CUDA kernels, read line by line

*In one sentence:* a kernel reads like ordinary code run once per thread, and reading one means finding how a thread's index picks its data, how many times each global value is loaded, and where threads must wait for one another.

**Vector add.** The smallest complete CUDA program: $y=a+b$ for $n$ floats, one thread per element.

```cpp
// y = a + b for n floats: one thread per element
__global__ void vec_add(const float* a, const float* b, float* y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;   // the element this thread owns
    if (i < n) y[i] = a[i] + b[i];                   // the last block's spare threads do nothing
}

// host side
float *d_a, *d_b, *d_y;                              // pointers into device memory
cudaMalloc(&d_a, n * sizeof(float));                 // likewise d_b and d_y
cudaMemcpy(d_a, a, n * sizeof(float), cudaMemcpyHostToDevice);   // likewise b; returns when copied
int B = 256, G = (n + B - 1) / B;                    // 256 threads per block, enough blocks for n
vec_add<<<G, B>>>(d_a, d_b, d_y, n);                 // returns at once: the launch is asynchronous
cudaMemcpy(y, d_y, n * sizeof(float), cudaMemcpyDeviceToHost);  // queued after the kernel; returns when done
cudaFree(d_a);                                       // likewise d_b and d_y
```

Every line is a piece of §1–§2: the global index, the bounds check, the host allocating and copying device memory, the chevrons, and a synchronous `cudaMemcpy` that — queued behind the kernel — is also where the host waits for it (Programming Guide §2.1.3.2). Consecutive threads read consecutive floats, so every load and store is coalesced. Its intensity is one FLOP per 12 bytes, 0.083 FLOP/byte: for $n=2^{20}$, 12.58 MB take 12.58 µs at G-100's $\beta$, while the arithmetic would take 0.01 µs even at $P$ — and $P$ is a bf16 tensor rate: plain fp32 additions run slower, but even a hundred times slower they would stay under the memory time. A vector add is as memory-bound as a kernel can be, and its speed is $\beta$.

**A matrix product, naive.** Layer 2 is $C=AB$ with $A$ the $4{,}096\times256$ activations and $B$ the $256\times256$ matrix $W_2^\top$, which the kernel reads from a transposed copy of $W_2$ stored row by row, so that `B[k * N + col]` is $W_2[\text{col},k]$ and the product is $AW_2^\top$. The direct kernel gives each thread one element of $C$:

```cpp
// C (M x N) = A (M x K) times B (K x N), all row-major: one thread per element of C
__global__ void matmul_naive(const float* A, const float* B, float* C, int M, int N, int K) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row < M && col < N) {
        float acc = 0.0f;
        for (int k = 0; k < K; ++k)
            acc += A[row * K + k] * B[k * N + col];  // two global loads per multiply-add
        C[row * N + col] = acc;
    }
}
```

Each thread issues $2K$ loads, one element of $A$ and one of $B$ per multiply-add, so the grid issues $2MNK$. Every element of $A$ is loaded by all $N$ threads of its row of $C$ and every element of $B$ by all $M$ threads of its column; whether those repeats reach DRAM is left to the caches.

**The same product, tiled.**

```cpp
#define T 16                                        // tile width: blocks of T x T threads
// the same product, for M, N and K that are multiples of T
__global__ void matmul_tiled(const float* A, const float* B, float* C, int M, int N, int K) {
    __shared__ float As[T][T], Bs[T][T];            // one tile of A and one of B, shared by the block
    int row = blockIdx.y * T + threadIdx.y;
    int col = blockIdx.x * T + threadIdx.x;
    float acc = 0.0f;
    for (int k0 = 0; k0 < K; k0 += T) {             // one phase per tile along K
        As[threadIdx.y][threadIdx.x] = A[row * K + k0 + threadIdx.x];    // each thread loads one element
        Bs[threadIdx.y][threadIdx.x] = B[(k0 + threadIdx.y) * N + col];  // of each tile: 2 loads a phase
        __syncthreads();                            // both tiles complete before anyone reads them
        for (int k = 0; k < T; ++k)
            acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];              // T multiply-adds from shared memory
        __syncthreads();                            // everyone done before the tiles are overwritten
    }
    C[row * N + col] = acc;
}
// launch: dim3 block(T, T), grid(N / T, M / T);  matmul_tiled<<<grid, block>>>(A, B, C, M, N, K);
```

A block of $T\times T$ threads computes a $T\times T$ tile of $C$ in $K/T$ phases. In each phase its threads load one $T\times T$ tile of $A$ and one of $B$ into shared memory, one element each — and since `threadIdx.x` runs along a row in both loads, the loads are coalesced — wait at the barrier, and then do $T$ multiply-adds each out of shared memory. A thread now issues 2 loads per phase, $2K/T$ in all. In bf16 the arrays would be `__nv_bfloat16` with a float accumulator, and the counts are the same.

> **Shared-memory tiling, defined.** **Tiling** is a *restructuring of a kernel's loops so that a thread block loads a tile of its inputs into shared memory once and every thread of the block reuses it from there* — a change to where the operands are read from, not to what is computed. Four defining conditions. The block loads each tile **cooperatively, with coalesced loads**, one element per thread. A **barrier** (`__syncthreads()`) separates loading from use, and another separates use from the next overwrite, because threads of a block run in no fixed order. Each loaded element is **used $T$ times** from shared memory, by the $T$ threads that need it. And the result is **the same sum**, taken in tiles — possibly in a different order, which can change the last bits of a floating-point result.
>
> $$L_{\text{naive}}=2MNK,\qquad L_{\text{tiled}}=\frac{2MNK}{T}$$
>
> where $L$ counts element loads from global memory for $C=AB$ with $A\in\mathbb R^{M\times K}$ and $B\in\mathbb R^{K\times N}$, and $T$ is the tile width — so the global loads fall by exactly the tile width, since each loaded element now serves $T$ multiply-adds instead of one.
>
> - **Example**: layer 2 at $N=4{,}096$: 536,870,912 loads naive, 33,554,432 with $T=16$ and 16,777,216 with $T=32$ — 1.07 GB, 67.1 MB and 33.6 MB in bf16, against the 2.23 MB of reading the input and the weights once, 481.9, 30.1 and 15.1 times as much (§9).
> - **Non-example**: relying on the L1 and L2 caches. They catch some of the naive kernel's repeated loads, but automatically and without guarantee; tiling makes the reuse explicit and bounded.
> - **Non-example**: a tile loaded into shared memory and read once. Staging data through shared memory pays only when the tile is reused, or when it turns an uncoalesced global access into a coalesced one — the transpose example of the Programming Guide (§2.3.4.2.1).
> - **Why it matters**: the loads that reach global memory are what the slanted roof charges for, so tiling is how a kernel's traffic approaches the once-per-operand count the roofline assumes; FlashAttention is the same idea applied to attention's score table ([[03-deep-learning/foundations/attention-transformer|1.2 §7]]).

The lab checks the count on a small case: a $64\times64$ by $64\times32$ product with $T=16$ loads 16,384 elements, against 262,144 naive, and returns exactly $AB$. Production libraries go further — larger tiles, registers, tensor cores — which is why a framework's matrix product is seldom written by hand. Reading one, though, uses exactly these questions.

**The vector add in NVIDIA Warp.** Warp writes a kernel as a Python function and compiles it to CUDA C++ on its first launch, caching the result (Warp documentation, Runtime):

```python
# not-run: needs NVIDIA Warp and a GPU
import numpy as np
import warp as wp

@wp.kernel
def vec_add(a: wp.array(dtype=float), b: wp.array(dtype=float), y: wp.array(dtype=float)):
    i = wp.tid()                                        # this thread's index, 0 .. n-1
    y[i] = a[i] + b[i]

n = 1 << 20
a = wp.array(np.ones(n, dtype=np.float32), dtype=float, device="cuda")
b = wp.array(np.full(n, 2.0, dtype=np.float32), dtype=float, device="cuda")
y = wp.zeros(n, dtype=float, device="cuda")
wp.launch(vec_add, dim=n, inputs=[a, b], outputs=[y], device="cuda")   # compiled on first launch; asynchronous
print(y.numpy()[:3])                                    # .numpy() waits for the kernel, then copies to the host
```

The CUDA vocabulary maps one to one. `@wp.kernel` is `__global__`; the typed arguments, which Warp requires, are the pointers; `wp.tid()` is the global index; `dim=n` asks for $n$ threads and leaves the blocks to Warp; and `wp.launch` is the chevrons, asynchronous like them. `.numpy()` is one of the operations that synchronize with the GPU, like `cudaMemcpy` above. Warp initializes itself at the first call that needs it, and its default device is `cuda:0` when a GPU is present. Since release 1.12 the annotation may also be written `wp.array[float]`, an alternative the call form still stands beside.

**Reading someone else's kernel**, the checklist this section has used: which element does thread $i$ own, and is there a bounds check; along which index do consecutive threads move, and is that the contiguous one in memory (§2); how many times is each global value loaded (tiling); where are the barriers, and is every shared-memory read behind one; and how many threads does the launch start, and how many warps of work is that (§1).

### 7. Measure before optimizing

*In one sentence:* the GPU runs behind the CPU, so a timer that does not wait for it measures only the launches, and any line that needs a GPU result on the CPU stops the pipeline until the GPU catches up.

A launch returns to the host before the kernel has run (Programming Guide §2.1.2.2), and PyTorch's operations are queued the same way: a call that uses the GPU enqueues its work, which executes later, in the order queued, and the framework synchronizes by itself whenever data is copied between CPU and GPU (PyTorch, CUDA semantics). The host can therefore run ahead, issuing the next launch while the GPU works on the last. Two clocks describe it, the host's and the device's:

> **Host–device synchronization, defined.** A **synchronization** is a *point at which the host thread stops until the device has finished work already queued* — an event in a program's timeline, not a kind of operation and not a cost of the GPU's arithmetic. Three defining conditions. Work is **queued asynchronously**: a launch returns before the kernel runs, and kernels on one stream run in the order issued. The host **needs something from the device** — a value on the CPU, through `.item()`, `.cpu()`, `print` or a Python `if` on a GPU tensor — or asks for the wait explicitly, with `torch.cuda.synchronize()` or `cudaDeviceSynchronize()`. And the host **waits**, so its next launch is issued only after the device has drained: the overlap of the two is lost.
>
> $$h\leftarrow h+t_L,\qquad g\leftarrow\max(h,g)+d_k,\qquad \text{at a sync:}\ \ h\leftarrow\max(h,g)$$
>
> where $h$ is the host's clock, $g$ the time the device becomes free, $t_L$ the launch overhead and $d_k$ kernel $k$'s own time — so without a sync the two overlap — a kernel shorter than $t_L$ hides behind the next launch, and one longer than $t_L$ hides the next launch behind it — while a sync forces the two clocks together.
>
> - **Example**: MLP-256 at $N=4{,}096$. Pipelined, the host issues layer 2's launch while layer 1 runs, and the pass ends at 17.54 µs. With an `.item()` after every layer each launch waits for the kernel before it, and the pass takes the serial model's 25.19 µs — 44% longer for the same arithmetic.
> - **Non-example**: the same comparison at $N=1$: 15.00 µs against 15.17. The kernels are shorter than a launch, so all the overlap can hide is their own 0.17 µs, and the sync costs almost nothing; the launches are the whole cost either way.
> - **Non-example**: an asynchronous copy from pinned memory, or recording a CUDA event. Both are queued like a kernel and leave the host free; only a later wait on them blocks.
> - **Why it matters**: timing without a sync measures the queueing, not the work — PyTorch's notes say such measurements are not accurate — and one stray `.item()` per step in an RL loop turns every step into a full round trip.

**What synchronizes in PyTorch.** PyTorch's performance tuning guide lists the usual culprits: printing a CUDA tensor, `.item()`, memory copies such as `tensor.cuda()`, `.cpu()` or the equivalent `.to(device)`, `.nonzero()`, and Python control flow that depends on the result of a CUDA operation. `torch.cuda.set_sync_debug_mode("warn")` warns at each synchronizing operation it covers — an experimental feature, and not every such operation triggers it — and `CUDA_LAUNCH_BLOCKING=1` makes every launch synchronous, which is for debugging an error's location, not for timing.

**Timing it correctly.** Wait for the device before reading the clock: call `torch.cuda.synchronize()` before measuring, or record CUDA events around the work and read their elapsed time after synchronizing (PyTorch, CUDA semantics; Best Practices §9.1). Run a few warm-up iterations first, because the first call creates the CUDA context and may compile code (Programming Guide §2.1.6) — and Warp compiles each kernel at its first launch.

**Paying the launches once.** A CUDA graph records a sequence of kernels once and replays it with a single launch, so the per-kernel preparation is paid when the graph is instantiated rather than every time (Programming Guide §4.2). In PyTorch, `torch.cuda.graph` captures a region and `torch.cuda.make_graphed_callables` wraps a module; replay trades eager execution's flexibility for greatly reduced CPU overhead, and the captured region may not change shapes or synchronize with the CPU — an `.item()` inside it is prohibited (PyTorch, CUDA semantics). Warp records one with `wp.ScopedCapture`. In the lab's model, MLP-256 as one graph launch takes 5.17 µs at $N=1$ instead of 15.17, and 15.19 µs at $N=4{,}096$ instead of 25.19.

**What a profiler shows, and which one to open.**

| tool | the question it answers | what it shows |
|---|---|---|
| CUDA events with `torch.cuda.synchronize()` | how long does this take on the GPU? | elapsed device time between two recorded points |
| `torch.profiler` | which operators and kernels take the time? | per operator, CPU time and CUDA time, self and total, input shapes when `record_shapes=True`, and a Chrome trace of the run |
| `torch.cuda.set_sync_debug_mode` | where does my code make the host wait? | a warning or an error at each synchronizing operation it covers |
| Nsight Systems (`nsys profile`) | where are the gaps between kernels, and what causes them? | a timeline of CPU threads, CUDA API calls, kernels, memory copies and synchronizations, with NVTX ranges if the code marks them |
| Nsight Compute | why is this one kernel slow? | one kernel in depth: its throughput against the hardware's limits, and its point on a roofline chart |

Start from the timeline, not from a kernel. A step whose timeline shows kernels separated by gaps is launch- or host-bound, and no kernel optimization will shorten it; a step whose kernels run back to back is kernel-bound, and then Nsight Compute's roofline says which roof each kernel is under. For MLP-256 the timeline would answer the question at $N=1$: three kernels of well under a microsecond between launches of 5 µs.

```python
# not-run: needs PyTorch and a CUDA GPU
import torch
from torch.profiler import profile, ProfilerActivity, record_function

policy = torch.nn.Sequential(                               # MLP-256 in bf16, no biases
    torch.nn.Linear(64, 256, bias=False), torch.nn.ReLU(),
    torch.nn.Linear(256, 256, bias=False), torch.nn.ReLU(),
    torch.nn.Linear(256, 8, bias=False)).to("cuda", torch.bfloat16)
obs = torch.randn(4096, 64, device="cuda", dtype=torch.bfloat16)

with torch.no_grad():
    for _ in range(10):                                     # warm-up: the first calls pay one-time setup
        policy(obs)
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    for _ in range(100):
        act = policy(obs)
    end.record()
    torch.cuda.synchronize()                                # wait for the GPU before reading the events
    print("ms per forward pass:", start.elapsed_time(end) / 100)

    torch.cuda.set_sync_debug_mode("warn")                  # from here on, warn at synchronizing operations
    with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], record_shapes=True) as prof:
        with record_function("policy_step"):
            act = policy(obs)
            worst = act.abs().max().item()                  # .item() brings one number to the CPU: a sync
    print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
    prof.export_chrome_trace("policy_step.json")            # a timeline, for chrome://tracing
```

Run eagerly like this, the network may launch more kernels than the page's model counts — an eager framework can run each ReLU as a kernel of its own, where the model folds it into the matrix product — and the profiler's table is where that shows.

### 8. On the robot: Jetson, TensorRT and the control budget

*In one sentence:* on the robot the GPU serves one observation at a time inside a control period, so a large policy's rate is set by the bytes per weight and a small policy's by its launches and synchronizations, and TensorRT attacks both.

**The robot's GPU.** A Jetson module is a Tegra system-on-chip: its CPU and its integrated GPU share one physical DRAM, and host memory, device memory and unified memory are all allocated in it (CUDA for Tegra §3). There is no host link to cross, so §2's 20.97 µs upload does not exist on the robot — but the CPU and the GPU draw on the same memory, whose bandwidth on Jetson Thor is 273 GB/s ([[03-deep-learning/foundations/training-at-scale|1.3 §11]]). And the robot serves one observation at a time, $N=1$: the left end of §4's sweep.

**Two regimes at batch one.** MLP-256 needs 170,128 bytes per pass, 0.62 µs at 273 GB/s; its time is launches and synchronization, and a faster number format would halve a term nobody can see. A 3B policy needs 6.0 GB per token in bf16, 22.0 ms at the same bandwidth, and there the bytes per weight are the time: 1.3 §11's table gives 11.0 ms in fp8 and 6.2 ms in NVFP4 for the same model. The first regime needs fewer launches and syncs, the second fewer bytes, and a deployment has to know which it is in before it changes anything.

**TensorRT's role.** TensorRT is NVIDIA's inference compiler and runtime. In its build phase it takes a trained network, fuses layers wherever its patterns allow — its layer fusion catalog illustrates fusion with a matrix-multiply layer merged with the ReLU after it — picks for each layer the fastest kernel available on the target GPU by timing candidates, and can run layers in reduced precision: INT8, INT4 weights, FP8 and FP4 in release 11.3, the current release for discrete GPUs — the formats of [[03-deep-learning/foundations/training-at-scale|1.3 §11]]. The result is a serialized *engine*, which its runtime loads and executes. By default an engine is guaranteed to work only on the same operating system, CPU architecture, GPU model and TensorRT version it was built with — the timing that chose its kernels ran on that GPU. On a Jetson nothing loosens that tie. TensorRT 11.3.0 does not support JetPack, so a Jetson deployment stays on the TensorRT 10.x release its JetPack supports, whose own notes say which reduced formats it offers (11.3.0 release notes); the hardware-compatibility option that relaxes the tie to the GPU is not supported on JetPack, and version compatibility only lets an engine built with an earlier TensorRT run under a later one (Engine Compatibility). The engine is therefore built on the robot itself, with its JetPack's TensorRT 10.x. Both of this section's regimes gain: fusion removes launches and activation traffic, and precision removes bytes.

> **Kernel fusion, defined.** **Kernel fusion** is a *transformation of a sequence of operations into fewer kernels* — a change to how a computation is scheduled on the GPU, not to what it computes. Three defining conditions. The fused operations are **consecutive**, each consuming what the one before produced. The intermediate results **stay on chip**, in registers or shared memory, instead of being written to DRAM and read back. And the sequence becomes **one launch** instead of one per operation.
>
> $$t_{\text{fused}}=t_L+\max\Big(\frac{\sum_\ell F_\ell}{P},\ \frac{e\,(W+Nn_0+Nn_L)}{\beta}\Big)$$
>
> where $W$ is the number of weights, $n_0$ and $n_L$ the network's input and output widths, and the other symbols are those of §3–§4 — so the activations between layers leave the byte count, and the launches fall from one per layer to one.
>
> - **Example**: MLP-256 as one ideal fused kernel. At $N=1$ it takes 5.17 µs instead of 15.17; at $N=4{,}096$ its intensity rises from the separate layers' 50.6, 124.1 and 7.74 to 907.8 for the whole pass, which is then compute-bound: 11.88 µs instead of 25.19, or 17.54 pipelined.
> - **Non-example**: a CUDA graph. It removes the per-kernel launch cost — one launch for the pass, 15.19 µs at $N=4{,}096$ in the model — but every layer still writes its activations to DRAM and reads them back.
> - **Non-example**: batching. It raises each kernel's intensity and keeps one launch per layer, and it cannot lift §4's caps, which are set by the activation traffic that only fusion removes.
> - **Why it matters**: it is what TensorRT's builder does at build time and what FlashAttention does for attention ([[03-deep-learning/foundations/attention-transformer|1.2 §7]]), and it is the one lever that acts on both costs a small policy pays.

**The control-rate budget.** [[04-robotics/robot-systems-deployment|10. Robot Systems §3]] builds a robot's observation-to-action latency as a sum of stages — sampling, exposure, transport, inference, decoding, actuation — around an illustrative 70 ms budget in which inference is 40 ms, and asks for the worst case, not the mean. Put this track's two policies into the inference term. MLP-256's 15 µs of launches are 0.03% of D4's 50 ms control period and 1.5% of a 1 kHz servo's millisecond; its term is set by the launches, the synchronization that brings the actions to the CPU, the Python around them and the first call's setup, which is why a small policy is warmed up before the loop starts and judged by its worst tick. A 3B policy pays 22.0 ms per token in bf16 just to read its weights, longer than a 20 ms vision period, as [[04-robotics/robot-systems-deployment|10. Robot Systems §11]] computes — and there the bytes decide the rate. The two policies sit at opposite ends of §4's sweep: one is all launch, the other all bytes.

### 9. The lab: roofline, batching, coalescing and tiling

Five parts on the frozen objects. Part 1 prints the Worked case — each layer's FLOPs, bytes, intensity and bound at $N=1$ and $N=4{,}096$ — with each layer's cap and ridge crossing. Part 2 is the batch sweep of §4, with the batch at which the kernels first take as long as the launches. Part 3 counts the 32-byte sectors a warp touches, from the addresses, at several strides and two element sizes. Part 4 counts a matrix product's global loads, naive and tiled, checks the count and the product on a small case by carrying out the tiled algorithm, and applies it to layer 2. Part 5 runs the host–device timeline of §7 and prices a CUDA graph, a fused kernel and the host link of §5. There are no timings anywhere: every number is the model's, so the output is the same on any machine.

```python
# 1.4 lab: MLP-256 on the course GPU G-100 - roofline, batching, coalescing, tiling, the host timeline. NumPy only.
import numpy as np

# --- 0. the frozen objects (Running object) ------------------------------------------------------
LAYERS = [(64, 256), (256, 256), (256, 8)]   # MLP-256 as (n_in, n_out) per layer; the ReLUs ride in layers 1-2
E = 2                                        # bytes per number: bf16
P, BETA = 100e12, 1000e9                     # G-100: peak bf16 FLOP/s and DRAM bytes/s (course numbers)
T_L, LINK = 5e-6, 25e9                       # G-100: launch overhead in s, host link in bytes/s (course numbers)
US = 1e6                                     # seconds -> microseconds

def layer_cost(n_in, n_out, N, e=E):
    """FLOPs and ideal DRAM bytes of one layer kernel on N inputs: weights, input and output each moved once."""
    return 2 * N * n_in * n_out, e * (n_in * n_out + N * n_in + N * n_out)

def kernel_time(F, B, p=P, beta=BETA):
    return max(F / p, B / beta)              # the lower of the two roofs decides

def forward(N, layers=LAYERS, e=E, p=P, beta=BETA, t_l=T_L):
    """Per-layer (F, B, I, time, bound) and the serial time: every kernel waits for its own launch."""
    rows = []
    for n_in, n_out in layers:
        F, B = layer_cost(n_in, n_out, N, e)
        rows.append((F, B, F / B, kernel_time(F, B, p, beta), "compute" if F / B > p / beta else "memory"))
    t_roof = sum(r[3] for r in rows)
    return rows, t_roof, len(layers) * t_l + t_roof

# --- 1. the Worked case: one forward pass at N = 1 and N = 4096 ----------------------------------
print("ridge P/beta = %.0f FLOP/byte" % (P / BETA))
for N in (1, 4096):
    rows, t_roof, t = forward(N)
    for (n_in, n_out), (F, B, I, tk, bound) in zip(LAYERS, rows):
        print("N=%-5d %3d->%-3d F=%10d B=%8d I=%8.3f F/P=%8.5f us B/beta=%8.5f us %s-bound"
              % (N, n_in, n_out, F, B, I, F / P * US, B / BETA * US, bound))
    F_all, B_all = sum(r[0] for r in rows), sum(r[1] for r in rows)
    print("N=%-5d all     F=%10d B=%8d I=%8.3f  roofs %.4f us + launches %.0f us = %.4f us, %.2f ns per env"
          % (N, F_all, B_all, F_all / B_all, t_roof * US, len(LAYERS) * T_L * US, t * US, t / N * 1e9))
for n_in, n_out in LAYERS:                   # each layer's cap, and the batch at which it crosses the ridge
    cap = n_in * n_out / (n_in + n_out)
    cross = "N = %.1f" % (1 / (1 / (P / BETA) - 1 / cap)) if cap > P / BETA else "never"
    print("%3d->%-3d cap %.2f FLOP/byte, crosses the ridge: %s" % (n_in, n_out, cap, cross))

# --- 2. the batch sweep ---------------------------------------------------------------------------
for N in (1, 4, 16, 64, 256, 1024, 4096, 16384):
    rows, t_roof, t = forward(N)
    print("N=%6d  I = %6.2f %7.2f %5.2f  over the ridge %d  roofs %7.3f us  with launches %7.3f us"
          "  per env %8.2f ns  launch share %4.1f%%"
          % (N, *[r[2] for r in rows], sum(r[4] == "compute" for r in rows), t_roof * US, t * US,
             t / N * 1e9, 100 * len(LAYERS) * T_L / t))
lo, hi = 1.0, 65536.0                        # the batch at which the kernels take as long as the launches
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if forward(mid)[1] < len(LAYERS) * T_L else (lo, mid)
print("the three kernels take as long as the three launches at N = %.0f" % lo)

# --- 3. coalescing: 32-byte sectors a warp touches ------------------------------------------------
def sectors(stride, e, start=0, w=32, s=32):
    """Distinct s-byte sectors touched when thread k of a warp reads e bytes at start + k*stride*e."""
    addr = start + np.arange(w) * stride * e
    return len(set(np.concatenate([np.arange(a // s, (a + e - 1) // s + 1) for a in addr])))

for e, name in ((4, "fp32"), (2, "bf16")):
    for stride in (1, 2, 4, 8, 16, 256):
        S = sectors(stride, e)
        print("%s stride %3d: %2d sectors, %4d bytes moved for %3d used, efficiency %6.2f%%"
              % (name, stride, S, 32 * S, 32 * e, 100 * e / S))
print("fp32 stride 1 starting 4 bytes past a sector boundary: %d sectors" % sectors(1, 4, start=4))

# --- 4. tiling: global loads of C = A B, naive and tiled, checked on a small case ------------------
def loads(M, N, K, T=1):
    """Element loads from global memory: 2K per output naive (T=1), 2K/T with T x T shared-memory tiles."""
    return 2 * M * N * K // T

def tiled_matmul(A, B, T):
    """C = A B one T x T tile of C at a time, counting the elements loaded into 'shared memory'."""
    M, K = A.shape; N = B.shape[1]; C = np.zeros((M, N)); count = 0
    for i0 in range(0, M, T):
        for j0 in range(0, N, T):                    # one thread block per tile of C
            acc = np.zeros((T, T))
            for k0 in range(0, K, T):                # one phase: a tile of A and a tile of B
                As, Bs = A[i0:i0+T, k0:k0+T], B[k0:k0+T, j0:j0+T]
                count += As.size + Bs.size           # one element of each tile per thread
                acc += As @ Bs                       # every loaded element used T times
            C[i0:i0+T, j0:j0+T] = acc
    return C, count

rng = np.random.default_rng(0)
A, B = rng.integers(-3, 4, (64, 64)).astype(float), rng.integers(-3, 4, (64, 32)).astype(float)
C, count = tiled_matmul(A, B, 16)
print("64x64 times 64x32, T=16: counted %d loads, formula %d, naive %d, product exact: %s"
      % (count, loads(64, 32, 64, 16), loads(64, 32, 64), np.array_equal(C, A @ B)))
M, N, K = 4096, 256, 256                             # layer 2 at N = 4096: X (4096x256) times W2^T (256x256)
once = E * (M * K + K * N)                           # the input and the weights, each read once
for T in (1, 16, 32):
    print("layer 2, T=%2d: %9d loads = %10d bytes, %5.1f times the %d bytes read once"
          % (T, loads(M, N, K, T), E * loads(M, N, K, T), E * loads(M, N, K, T) / once, once))

# --- 5. the host timeline: asynchronous launches, a sync, a graph, a fused kernel, a host link ----
def timeline(durations, t_l=T_L, sync_each=False):
    """Host issues kernels back to back; each launch costs t_l of host time; kernels run in order."""
    h = g = 0.0                                      # host clock, device clock
    for d in durations:
        h += t_l                                     # the host issues the launch
        g = max(h, g) + d                            # the kernel starts once issued and once the GPU is free
        if sync_each:
            h = max(h, g)                            # e.g. an .item() after the layer: the host waits
    return max(h, g)                                 # reading the actions back waits for the last kernel

for N in (1, 4096):
    rows, t_roof, t_serial = forward(N)
    d = [r[3] for r in rows]
    F_all = sum(r[0] for r in rows)
    B_fused = E * (sum(i * o for i, o in LAYERS) + N * (LAYERS[0][0] + LAYERS[-1][1]))  # no activations in DRAM
    print("N=%-5d pipelined %8.4f us   sync after each layer %8.4f us   one graph launch %8.4f us"
          "   fused kernel %8.4f us (I = %.1f)"
          % (N, timeline(d) * US, timeline(d, sync_each=True) * US, (T_L + sum(d)) * US,
             (T_L + kernel_time(F_all, B_fused)) * US, F_all / B_fused))
N = 4096                                             # a CPU simulator feeding the GPU policy, per step
up, down = E * N * LAYERS[0][0] / LINK, E * N * LAYERS[-1][1] / LINK
print("N=4096 over the host link: observations %.2f us, actions %.2f us, %.2f us per step before any overhead"
      % (up * US, down * US, (up + down) * US))
```

**The worked case and the caps**, Part 1 — the two tables of the Worked case, with the whole pass at $N=1$ at 15.1701 µs (15,170.13 ns per environment) and at $N=4{,}096$ at 25.1897 µs (6.15 ns per environment):

| layer | cap $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$ | crosses G-100's ridge |
|---|---:|---|
| $64\to256$ | 51.20 | never |
| $256\to256$ | 128.00 | at $N=457.1$ |
| $256\to8$ | 7.76 | never |

**The sweep**, Part 2, is the table of §4, and the three kernels take as long as the three launches at $N=6{,}037$.

**Sectors per warp**, Part 3:

| stride (elements) | fp32: sectors | bytes moved for 128 used | efficiency | bf16: sectors | bytes moved for 64 used | efficiency |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 128 | 100.00% | 2 | 64 | 100.00% |
| 2 | 8 | 256 | 50.00% | 4 | 128 | 50.00% |
| 4 | 16 | 512 | 25.00% | 8 | 256 | 25.00% |
| 8 | 32 | 1,024 | 12.50% | 16 | 512 | 12.50% |
| 16 | 32 | 1,024 | 12.50% | 32 | 1,024 | 6.25% |
| 256 | 32 | 1,024 | 12.50% | 32 | 1,024 | 6.25% |

and fp32 at stride 1 starting 4 bytes past a sector boundary touches 5 sectors.

**Global loads**, Part 4: the small case counts 16,384 loads, as the formula says, against 262,144 naive, and its product is exact. For layer 2 at $N=4{,}096$:

| tile width $T$ | global loads | bytes (bf16) | against reading input and weights once (2,228,224 bytes) |
|---:|---:|---:|---:|
| 1 (naive) | 536,870,912 | 1,073,741,824 | 481.9× |
| 16 | 33,554,432 | 67,108,864 | 30.1× |
| 32 | 16,777,216 | 33,554,432 | 15.1× |

**The host timeline**, Part 5:

| $N$ | pipelined (µs) | sync after each layer (µs) | one graph launch (µs) | fused kernel (µs) | fused intensity |
|---:|---:|---:|---:|---:|---:|
| 1 | 15.0046 | 15.1701 | 5.1701 | 5.1681 | 1.0 |
| 4,096 | 17.5355 | 25.1897 | 15.1897 | 11.8787 | 907.8 |

and at $N=4{,}096$ a CPU simulator's host-link copies take 20.97 µs up and 2.62 µs down, 23.59 µs per step before any overhead.

**Reading the tables.** Five things the lecture predicted and the numbers now show.

- **Batch 1 is launch-bound, not memory-bound.** The roofline calls all three layers memory-bound at $N=1$, correctly, and their memory time is 0.17 µs; the launches are 15 µs. A GPU that doubled its bandwidth would make the pass 0.56% faster, 15.09 µs instead of 15.17 (problem 1).
- **Batching moves the big layer across the ridge and leaves the thin ones behind.** Layer 2 crosses at 457.1; layers 1 and 3 are capped at 51.2 and 7.76, below G-100's ridge at any batch — the sweep's intensities creep toward 51.04 and 7.75 at 16,384.
- **Strides multiply traffic, in steps.** fp32 reaches the worst case at a 32-byte stride and bf16 at 16 elements, which is also 32 bytes: the sector, not the element, sets the unit. A column of $W_2$ in bf16 costs 1,024 bytes for 64.
- **Tiling divides loads by the tile width and nothing else.** 481.9, 30.1 and 15.1 times the once-through bytes at $T=1$, 16 and 32 — the ratio falls exactly as $1/T$.
- **Overlap, graphs and fusion attack different costs.** Pipelining overlaps the two clocks — each kernel shorter than a launch hides behind the next launch, and each longer one hides the next launch — 17.54 against 25.19 µs at 4,096, and at $N=1$ only the kernels' own 0.17 µs (15.00 against 15.17); a graph removes launches but not activation traffic (15.19); fusion removes both (11.88). At $N=1$ the graph and the fused kernel agree, 5.17 µs, because there all that remains is one launch.

### After reading

- [ ] Say what a kernel, a thread, a block, a grid and a warp are; write the launch line and the global index; and say why no block may wait for another.
- [ ] Explain latency hiding with Little's law, and why a batch-1 layer is latency-bound.
- [ ] Count the 32-byte sectors a warp touches at any stride and element size, and the efficiency.
- [ ] Compute a layer's FLOPs, bytes and intensity at any batch, place it on a roofline, and say which roof bounds it.
- [ ] Derive $1/I=(e/2)(1/N+1/I_\infty)$, find a layer's cap, and find the batch at which it crosses a ridge.
- [ ] Price a forward pass with its launches, and say at what batch the launches stop dominating.
- [ ] Say what a vectorized environment keeps on the GPU, why a CPU simulator costs a round trip per step, and what Rudin et al. actually measured.
- [ ] Read a CUDA or Warp kernel: its index, bounds check, coalescing, shared memory and barriers; and count its loads naive and tiled.
- [ ] Time GPU code correctly, name what forces a synchronization in PyTorch, and pick the tool for a performance question.
- [ ] Say what TensorRT's build phase does, why an engine belongs to one GPU, and which cost fusion removes that a CUDA graph does not.

### Self-check

1. A GPU runs one thread far more slowly than a CPU core does. Why is it faster on MLP-256 at $N=4{,}096$, and why does that argument fail at $N=1$?
2. A warp reads 32 consecutive bf16 weights along a row of $W_2$, and then 32 weights down a column. How many 32-byte sectors does each access need, and what fraction of the moved bytes is used?
3. MLP-256's layer 3 ($256\to8$) is memory-bound at every batch. Why, and what would change that?
4. The Worked case prices MLP-256 at $N=1$ at 15.17 µs, of which 0.17 µs is memory traffic. Where do the other 15 µs go, and what are two ways to remove most of them?
5. A training loop logs `loss.item()` at every step. What does that line cost, and when does it matter?
6. Your policy's time per pass is the same at 1 and at 1,024 environments. What does that tell you, and what does the page's model predict at 16,384?
7. MJX can be ten times slower than MuJoCo for a single scene, yet papers train locomotion policies with it. Why is there no contradiction?

> [!tip]- Answers
> 1. By throughput, not by speed: layer 2 at $N=4{,}096$ has 1,048,576 independent dot products, 32,768 warps, so while some warps wait for memory others compute, and the pass runs at 27.3 TFLOP/s. At $N=1$ the layer has 256 outputs, 8 warps, and 132,096 bytes to move — less than one memory latency's worth for any latency above 0.13 µs — so there is no work to switch to, and what little there is sits behind three 5 µs launches.
> 2. Along a row the stride is 1, so the 64 bytes fill $\lceil64/32\rceil=2$ sectors, all used. Down a column the stride is 256 elements, 512 bytes, so every thread has its own sector: 32 sectors, 1,024 bytes moved for 64 used, 6.25%.
> 3. Its intensity is capped at $256\cdot8/(256+8)=7.76$ FLOP/byte, because per environment it does 4,096 FLOPs and moves 528 bytes of activations, and batching shares only the weights. No batch reaches G-100's ridge of 100. Fusing it with the layer before, so that its 256 inputs never go to DRAM, removes most of those bytes; a wider output would raise the cap.
> 4. Into three kernel launches of 5 µs each. Fusing the network into one kernel leaves one launch, 5.17 µs in all; capturing the three kernels in a CUDA graph and replaying it also pays one launch, 5.17 µs. (Pipelining barely helps: all it can hide behind the launches is the kernels' own 0.17 µs, 15.00 against 15.17.)
> 5. A synchronization per step: the host waits for all queued GPU work before it can read the loss, so the next step's launches start only after the GPU has drained, and the overlap of host and device is lost. It matters when a step's kernels are short compared with the launches the host could have issued meanwhile — the small-network, launch-bound regime of robot policies — and hardly at all when each kernel is long; logging every hundred steps, or accumulating on the GPU, avoids it.
> 6. That the time is launch-bound: the kernels are much shorter than the launches, so the batch is almost free, as in §4's sweep, where 1 to 1,024 environments go from 15.17 to 17.58 µs. The flat part ends where the kernels take as long as the launches, $N=6{,}037$ for MLP-256 on G-100; at 16,384 the model predicts 55.65 µs, 3.67 times the value at $N=1$, as the pass becomes kernel-bound.
> 7. The same batching trade applied to physics: a single scene cannot fill a GPU and pays its fixed costs for one environment, while thousands of scenes share them. MJX's own documentation says it works best at thousands to tens of thousands of scenes in parallel. What papers report is throughput across the batch, and at that it wins.

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and [[03-deep-learning/lab-objects|0. Lab Objects]]. The objects are MLP-256 and G-100; every problem changes a knob — the bandwidth, an alignment, a layer's width, the tile, the element size, the code that measures — so none of the page's numbers can be copied.

1. **Draw.** The picture above, for MLP-256 on a variant of G-100 with its bandwidth doubled to $\beta=2{,}000$ GB/s ($P$ and $t_L$ unchanged), at $N=1$ and $N=1{,}024$: the roofline with both roofs and the new ridge, the three layers at both batches with their intensities, and the two time bars to scale. Say which layers sit on which side of the new ridge, and what the doubled bandwidth did to the $N=1$ bar.
2. **Derive.** (a) Show that a dense layer at $e$ bytes per number has $1/I=(e/2)\big(1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})\big)$. Find the cap of MLP-256's layer 1 and say why no batch makes it compute-bound on G-100; then find the batch at which a $512\times512$ layer in bf16 crosses G-100's ridge. (b) A warp reads 32 consecutive bf16 values starting 16 bytes past a sector boundary: how many sectors, at what efficiency? A warp reads one column of $W_1$, stored row by row as $256\times64$: how many sectors, at what efficiency, and how would you store $W_1$ to make that read coalesced? (c) Treat layer 1 at $N=4{,}096$ as a matrix product and count its global loads naive and tiled with $T=16$ and $T=32$, in elements and in bf16 bytes, against the bytes of reading its input and its weights once. (d) Estimate by hand the batch at which MLP-256's three kernels take as long as its three launches on G-100, from the growth of the roofline time per added environment at large $N$; check it against §9.
3. **Do.** Fill the `?` blanks, then run MLP-512 — MLP-256 with both hidden layers widened to 512 — on G-100 at $N\in\{1,16,256,4096\}$. Report (a) each layer's intensity and bound, the roofline and serial times, the cost per environment, and the batch at which the hidden layer crosses the ridge; (b) the sectors and efficiency of a warp reading fp64 (8-byte) values at strides 1, 2, 4 and 8; (c) the hidden layer's global loads at $N=4{,}096$, naive and with $T=16$ and 32; (d) the pipelined and synchronized times at $N=4{,}096$. Compare each with MLP-256.
4. **Interpret.** A lab reports that its three-layer MLP policy "runs in 0.04 ms" on the robot's Jetson, timed with Python's `time.perf_counter()` around `act = policy(obs)`. The 1 kHz control loop, which then calls `act.cpu()` and sends the command, misses its 1 ms deadline on some ticks, and always on the first. Using §4, §7 and §8, say what the 0.04 ms measured, what the real cost of a tick contains, why the first tick is slow, and what you would measure instead, with which tool.

```python
# Problem 3 (Do). MLP-512 (64 -> 512 -> 512 -> 8) on G-100: the calculator, the sweep, a warp of fp64, tiles. Fill ?.
import numpy as np

LAYERS = [(64, 512), (512, 512), (512, 8)]
E, P, BETA, T_L = 2, 100e12, 1000e9, 5e-6              # bf16 and G-100 (course numbers)

def layer_cost(n_in, n_out, N, e=E):
    F = ?                                                # one multiply and one add per weight per input
    B = ?                                                # weights, input and output, each moved once
    return F, B

def forward(N):
    times, out = [], []
    for n_in, n_out in LAYERS:
        F, B = layer_cost(n_in, n_out, N)
        t = ?                                            # the roofline time of this kernel
        times.append(t); out.append("%.2f%s" % (F / B, "c" if F / B > P / BETA else "m"))
    return times, out, ? + sum(times)                    # the serial model: launches plus kernels

for N in (1, 16, 256, 4096):
    times, out, t = forward(N)
    print("N=%5d  I per layer %s  roofs %.3f us  total %.3f us  per env %.4f us"
          % (N, " ".join(out), sum(times) * 1e6, t * 1e6, t / N * 1e6))
cap = ?                                                  # the hidden layer's cap, n_in n_out / (n_in + n_out)
print("hidden layer: cap %.1f, crosses the ridge at N = %.1f" % (cap, ?))   # from 1/I = 1/N + 1/cap

def sectors(stride, e, start=0, w=32, s=32):
    addr = start + np.arange(w) * stride * e
    return len(set(np.concatenate([np.arange(a // s, (a + e - 1) // s + 1) for a in addr])))

for stride in (1, 2, 4, 8):
    S = sectors(stride, 8)                               # fp64: 8 bytes per element
    print("fp64 stride %d: %2d sectors, efficiency %5.1f%%" % (stride, S, ?))

M, N, K = 4096, 512, 512                                 # the hidden layer at N = 4096
for T in (1, 16, 32):
    print("T=%2d: %d loads" % (T, ?))

def timeline(durations, sync_each=False):
    h = g = 0.0
    for d in durations:
        h += T_L
        g = ?                                            # starts when issued and when the GPU is free
        if sync_each:
            h = ?                                        # the host waits for the kernel
    return max(h, g)

times, _, _ = forward(4096)
print("N=4096: pipelined %.3f us, sync after each layer %.3f us"
      % (timeline(times) * 1e6, timeline(times, True) * 1e6))
```

> [!note]- How to draw it · 그리는 법
> - Make both axes logarithmic, FLOP/byte across and FLOP/s up, and label the two roofs with their numbers — the slope $\beta$ and the height $P$ — and the ridge at $P/\beta$. A doubled $\beta$ lifts the slanted roof and moves the ridge left; it moves no point sideways, because intensity belongs to the kernel, not to the GPU.
> - Put each layer at $(I,\ \min(P, I\beta))$, on the roof and not under it: the model's point is the bound.
> - Compute $I$ with the activations in the bytes. A point drawn at $I=N$ has forgotten them, and would put the output layer past any ridge at a large enough batch.
> - Mark each layer's cap $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$; a layer whose cap is left of the ridge can never reach the flat roof, whatever the batch.
> - Draw the time bars to scale with each launch as its own segment before its kernel, and shade memory- and compute-bound kernels differently. At small batches the bar is almost all launch, and doubling $\beta$ leaves it almost unchanged.
> - Keep the three layers as three points and three segments. A single whole-network point at the average intensity hides the one compute-bound layer.

> [!tip]- Solutions
> 1. The new ridge is $10^{14}/(2\times10^{12})=50$ FLOP/byte. At $N=1$ the intensities are unchanged, 0.981, 0.992 and 0.886, all memory-bound, but each point sits twice as high, at 1.96, 1.98 and 1.77 TFLOP/s; the memory times halve to 0.0167, 0.0660 and 0.0023 µs, so the bar is $15+0.0851=15.085$ µs instead of 15.170 — 99.4% launches, a change nobody could see. At $N=1{,}024$: layer 1 at 48.76 FLOP/byte stays just below the new ridge, memory-bound, 0.3441 µs (its compute time, 0.3355 µs, is within 3%); layer 2 at 113.78 is compute-bound, 1.3422 µs, as it already was on G-100; layer 3 at 7.70 is memory-bound, 0.2724 µs. The bar is $15+1.9586=16.959$ µs, 16.56 ns per environment and 88.5% launches, against 17.575 µs on G-100: the doubled bandwidth saved 0.62 µs, because only the memory-bound kernels shrank.
> 2. (a) $F=2Nn_{\text{in}}n_{\text{out}}$ and $B=e(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}})$, so $1/I=B/F=(e/2)\big(1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})\big)$. Layer 1's cap is $64\cdot256/320=51.2$: per environment it does 32,768 FLOPs and moves 640 bytes of activations, and no batch changes that ratio, which is below 100. A $512\times512$ layer has cap 256, so $1/100=1/N+1/256$ gives $N=164.1$. (b) The bytes run from 16 to 79, which is sectors 0, 1 and 2: 3 sectors, 96 bytes moved for 64 used, 66.7%. A column of $W_1$ has a stride of 64 elements, 128 bytes, so 32 sectors, 1,024 bytes for 64, 6.25%; storing $W_1$ transposed, as $64\times256$ row by row, makes that column a row: 2 sectors, 100%. (c) $M=4{,}096$, $N=256$, $K=64$: naive $2MNK=134{,}217{,}728$ loads, 268,435,456 bytes; $T=16$: 8,388,608 loads, 16,777,216 bytes; $T=32$: 4,194,304 loads, 8,388,608 bytes; reading the input and the weights once is $2(4{,}096\cdot64+64\cdot256)=557{,}056$ bytes, so the ratios are 481.9, 30.1 and 15.1 — the same as layer 2's, since $2MN/(M+N)$ does not involve $K$. (d) At large $N$ each environment adds 640 bytes to layer 1 (0.640 ns), 131,072 FLOPs to layer 2, which is compute-bound (1.311 ns), and 528 bytes to layer 3 (0.528 ns): 2.479 ns per environment, on top of 0.037 µs for the weights of layers 1 and 3. The kernels reach 15 µs at $N\approx(15-0.037)/0.002479=6{,}036$; §9 prints 6,037.
> 3. Blanks: `2 * N * n_in * n_out`, `e * (n_in * n_out + N * n_in + N * n_out)`, `max(F / P, B / BETA)`, `len(LAYERS) * T_L`, `512 * 512 / (512 + 512)`, `1 / (1 / (P / BETA) - 1 / cap)`, `100 * 32 * 8 / (32 * S)`, `2 * M * N * K // T`, `max(h, g) + d` and `max(h, g)`. The output, with `m` for memory-bound and `c` for compute-bound:
>
>    ```text
>    N=    1  I per layer 0.98m 1.00m 0.89m  roofs 0.602 us  total 15.602 us  per env 15.6023 us
>    N=   16  I per layer 12.49m 15.06m 5.28m  roofs 0.666 us  total 15.666 us  per env 0.9791 us
>    N=  256  I per layer 46.55m 128.00c 7.64m  roofs 1.977 us  total 16.977 us  per env 0.0663 us
>    N= 4096  I per layer 56.11m 240.94c 7.86m  roofs 30.527 us  total 45.527 us  per env 0.0111 us
>    hidden layer: cap 256.0, crosses the ridge at N = 164.1
>    fp64 stride 1:  8 sectors, efficiency 100.0%
>    fp64 stride 2: 16 sectors, efficiency  50.0%
>    fp64 stride 4: 32 sectors, efficiency  25.0%
>    fp64 stride 8: 32 sectors, efficiency  25.0%
>    T= 1: 2147483648 loads
>    T=16: 134217728 loads
>    T=32: 67108864 loads
>    N=4096: pipelined 35.743 us, sync after each layer 45.527 us
>    ```
>
>    (a) Four times the hidden weights make the $N=1$ pass 0.60 µs of memory instead of 0.17 — still 96% launches, 15.60 µs. The hidden layer's cap doubles to 256, so it crosses the ridge at $N=164.1$ instead of 457.1 and is already compute-bound at 256; the input and output layers stay memory-bound, capped at 56.9 and 7.88. At 4,096 the pass takes 45.53 µs, 11.1 ns per environment against MLP-256's 6.15: the hidden layer alone is 21.47 µs of compute. (b) An fp64 warp moves 256 bytes at stride 1, 8 sectors, and hits the 32-sector worst case already at stride 4, which is 32 bytes; efficiency bottoms out at 25%, not 12.5%, since each thread uses 8 of its sector's 32 bytes. (c) With $N$ and $K$ both doubled, $2MNK$ is four times layer 2's: 2.15 billion loads naive, divided by 16 or 32 when tiled. (d) Pipelined 35.74 µs against 45.53: the overlap saves 9.8 µs, more than MLP-256's 7.7, because its first kernel is longer (4.78 µs against 2.65) and hides behind the second launch; in both networks only the hidden layer outlasts a launch, and it hides the third launch whole.
> 4. `perf_counter()` around an asynchronous call measures the host's side only: the Python and the launches that enqueue the kernels, which return before the kernels run. The tick's real cost is those launches, plus the kernels, plus the synchronization in `act.cpu()` — the host waits for the last kernel — plus the copy into the host's buffer (on a Jetson it stays within the shared DRAM, with no PCIe hop, but it still waits), plus whatever else shares the GPU, such as a perception network, which is also where the occasional misses come from. The first tick also pays for creating the CUDA context and any code compiled at the first call (Programming Guide §2.1.6). Measure the whole tick, from the observation to the command, on every tick of a long run, and report its maximum and high percentiles against the 1 ms deadline, as [[04-robotics/robot-systems-deployment|10. Robot Systems §3]] asks — timed with a synchronized clock or CUDA events, never with a bare timer around the call. An Nsight Systems timeline shows where the gaps are and what else is running; `torch.cuda.set_sync_debug_mode("warn")` finds hidden syncs. Then act on what it shows: warm up before the loop; make a tick one launch by capturing the network in a CUDA graph — or by building a TensorRT engine, which fuses what its patterns allow but may still run several kernels, and capturing its enqueue in a CUDA graph, as TensorRT's performance guide describes; and keep exactly one synchronization per tick, the one that fetches the command.

### Sources

- NVIDIA. *CUDA Programming Guide*, v13.4 ([docs.nvidia.com/cuda/cuda-programming-guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html)) — §1.1.2 (why a GPU trades single-thread speed for throughput), §1.2.2.1–§1.2.2.2 (thread blocks and grids, blocks in any order; warps and SIMT, masking on divergence), §1.2.3 (host and device memory; caches), §2.1.2 (kernels, the triple-chevron launch, up to 1,024 threads per block, index intrinsics, bounds checking, asynchronous launch), §2.1.3.2 (`cudaMalloc`, a synchronous `cudaMemcpy`), §2.1.6 (runtime initialization), §2.3.3 (memory spaces: global, shared, registers, local, caches), §2.3.4.1 (coalesced access: four 32-byte transactions at 100%, 12.5% at a stride of 32 bytes or more), §2.3.4.2.1 (the transpose through shared memory), §2.3.7 (occupancy), §3.2.2.2 (hardware multithreading: warp contexts on chip, a scheduler issuing from ready warps), §4.2 (CUDA Graphs and the per-kernel launch cost).
- NVIDIA. *CUDA C++ Best Practices Guide*, v13.4 ([docs.nvidia.com/cuda/cuda-c-best-practices-guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)) — §9.1 (timing with events and synchronization), §10.1 (host–device transfer: 898 GB/s against 16 GB/s, keep data on the device, batch small transfers), §10.1.1–§10.1.2 (pinned memory, asynchronous transfers), §10.2.1 (coalescing for compute capability 6.0 and newer; §10.2.1.1 a simple access pattern, where permuting accesses within the touched sectors costs the same; §10.2.1.2 a misaligned start, five sectors; §10.2.1.4 strided access, 50% at stride 2), §10.2.3 and §10.2.3.2 (shared memory, and its use in matrix multiplication).
- NVIDIA. *CUDA for Tegra*, application note 13.4 ([docs.nvidia.com/cuda/cuda-for-tegra-appnote](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html)) — §3, the CPU and the integrated GPU sharing one SoC DRAM.
- NVIDIA. *Warp* documentation, 1.17 ([nvidia.github.io/warp](https://nvidia.github.io/warp/stable/)) — User Guide: Basics (kernels with typed arguments, `wp.tid`, arrays, `wp.launch`, `.numpy()` synchronizing) and Runtime (asynchronous launches, the default device, the compilation model and its cache, graph capture with `wp.ScopedCapture`); and the Warp changelog, 1.12.0 (subscript-style array annotations as an alternative).
- PyTorch 2.14 documentation ([docs.pytorch.org](https://docs.pytorch.org/docs/stable/notes/cuda.html)) — the "CUDA semantics" note (asynchronous execution, automatic synchronization on CPU–GPU copies, timing with `torch.cuda.Event`, pinned memory, CUDA graphs and their constraints); the `torch.profiler` reference and profiler recipe; `torch.cuda.set_sync_debug_mode`; and S. Migacz, "Performance Tuning Guide", PyTorch tutorials, updated 2025-07-09 (the operations that synchronize).
- NVIDIA. *Nsight Systems User Guide*, 2026.5 ([docs.nvidia.com/nsight-systems](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)) — `nsys profile`, CUDA and NVTX tracing, the timeline; *Nsight Compute Profiling Guide*, 2026.3 ([docs.nvidia.com/nsight-compute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)) — kernel-level profiling and its roofline charts (arithmetic intensity, the ridge point).
- NVIDIA. *TensorRT* documentation, 11.3 ([docs.nvidia.com/deeplearning/tensorrt](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html)) — "How TensorRT Works" (build and runtime phases, kernels chosen by timing, engine compatibility), "Layer Fusion Catalog", "Working with Quantized Types" (INT8, INT4 weights, FP8, FP4), "Engine Compatibility" (hardware compatibility not supported on JetPack or DriveOS; version compatibility), "Optimizing TensorRT Performance" (inference with CUDA graphs: an `enqueueV3()` call captured and replayed), and the TensorRT 11.3.0 release notes (JetPack not supported; Jetson deployments stay on TensorRT 10.x).
- Williams, S., Waterman, A. & Patterson, D. "Roofline: An insightful visual performance model for multicore architectures." *Communications of the ACM* 52(4):65–76, 2009 — the model, operational intensity against DRAM traffic, the ridge point; and NERSC, "Roofline Performance Model" ([docs.nersc.gov](https://docs.nersc.gov/tools/performance/roofline/)) — the ridge point as machine balance.
- Little, J. D. C. "A proof for the queuing formula: $L=\lambda W$." *Operations Research* 9(3):383–387, 1961.
- Rudin, N., Hoeller, D., Reist, P. & Hutter, M. "Learning to walk in minutes using massively parallel deep reinforcement learning." *Proceedings of the 5th Conference on Robot Learning*, PMLR 164:91–100, 2022 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — abstract (four and twenty minutes), §2 (data collection and updates on the GPU), §2.2.1 ($B=n_{\text{robots}}n_{\text{steps}}$), §2.2.2 (time-outs and bootstrapping), §4.1 (scaling to about 4,000 robots), §4.2 (4,096 robots, a batch of 98,304, 1,500 updates in under 20 minutes, RTX A6000), Appendix A.1 and Figure 8 (the time of each part of a step against the number of robots).
- Makoviychuk, V. et al. "Isaac Gym: High performance GPU-based physics simulation for robot learning." [arXiv:2108.10470](https://arxiv.org/abs/2108.10470), 2021 — abstract.
- MuJoCo documentation, "MuJoCo XLA (MJX)" ([mujoco.readthedocs.io](https://mujoco.readthedocs.io/en/stable/mjx.html)) — MJX-JAX's sharp bits and MJX-Warp; and the MuJoCo Warp repository ([github.com/google-deepmind/mujoco_warp](https://github.com/google-deepmind/mujoco_warp)).
- Isaac Lab documentation, "Creating a Direct Workflow RL Environment" ([isaac-sim.github.io/IsaacLab](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_direct_rl_env.html)) — `_get_dones`, `_reset_idx(env_ids)`, `num_envs`.
- JAX documentation ([docs.jax.dev](https://docs.jax.dev/en/latest/_autosummary/jax.vmap.html)) — `jax.vmap` and `jax.jit`.

## 한국어

*[[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습]] 위에 선다. 그 페이지의 §5–§6은 파라미터 하나가 치르는 바이트와 FLOP을 세고, §11은 로봇 정책의 디코딩이 Jetson Thor에서 메모리 한계임을 보인다. 이 페이지는 그 FLOP과 바이트가 어디서 쓰이는지 묻는다. GPU의 어느 장치에서, 어떤 순서로, 얼마나 빨리 쓰이는지, 그리고 로봇 학습 프로그램이 그 장치들을 쉬지 않게 하려면 무엇을 해야 하는지다. 대상은 이 페이지가 스스로 고정하는 정책 신경망 MLP-256과 교과용 GPU G-100이고, D1–D6가 텐서 대상인 것과 달리 비용 대상이다. [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]이 세우는 지연 예산을 §8이 채우고, [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋 §2]]가 나열하는 병렬 시뮬레이터를 §5가 설명한다.*

> [!note] 처음이라면 · First pass
> 그림을 먼저 본 뒤 계산기로 계산 절을 따라간다. MLP-256의 세 층을 환경 하나와 4,096개에서 G-100의 루프라인에 올리고, launch까지 넣어 시간을 매긴다. §1, §3, §4를 읽고 문제 1–2를 푼다. 논문이나 코드가 "coalesced", "shared memory", "tiled"를 말하면 §2와 §6을, 논문이 GPU 하나로 모의 로봇 수천 대를 학습시키면 §5를, 무엇이든 시간을 재거나 빠르게 만들기 전에는 §7을, 정책을 로봇에 올리기 전에는 §8을 연다. §9가 §2–§4, §6, §7을 코드로 돌린다.

### 이 페이지의 대상 · Running object

대상은 둘이다. 하나는 일, 하나는 기계이고, 둘 다 여기서 고정한다. [[03-deep-learning/lab-objects|0. Lab Objects]]의 대상은 텐서 대상이라서, 그 숫자는 페이지가 *가지고* 계산하는 값이다. 이 둘은 비용 대상이라서, 그 숫자는 페이지가 *값을 매기는* shape, 바이트 수, 속도이고 신경망 안의 값은 끝까지 등장하지 않는다. 카탈로그에서 가장 가까운 것은 역시 bias 없는 ReLU MLP인 **D1**이지만, 가중치 열두 개가 bf16으로 24바이트라 GPU로 잴 것이 없고, D1을 쓰는 페이지는 모두 신경망이 무엇을 출력하는지 묻는데 그것은 여기서 전혀 중요하지 않다. **D4**는 정책의 추론 시간 100 ms를 주어진 값으로 싣는다. 이 페이지는 그 값을 유도한다.

**MLP-256**, 정책 신경망:

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| 층 | $64\to256\to256\to8$ | 관측 64개가 들어가고 행동 8개가 나오며, 폭 256인 은닉층이 둘 |
| 활성함수 | ReLU | 각 은닉층 뒤, 그 층의 커널 안에서 적용한다. 출력층은 선형 |
| bias | 없음 | 있으면 파라미터가 520개(0.6%) 늘지만 아래 결론은 하나도 바뀌지 않는다 |
| 가중치 | $16{,}384+65{,}536+2{,}048=83{,}968$ | $W_1\in\mathbb R^{256\times64}$, $W_2\in\mathbb R^{256\times256}$, $W_3\in\mathbb R^{8\times256}$, 모두 행 단위로 저장 |
| 형식 | bf16, 숫자당 $e=2$바이트 | 가중치, 관측, activation, 행동 모두([[03-deep-learning/foundations/training-at-scale\|1.3 §4]]). 가중치는 $167{,}936$바이트 |
| $N$ | 1부터 16,384까지 | 순전파 한 번이 처리하는 환경 수. 로봇 하나, 또는 시뮬레이터의 배치(§5) |
| 커널 | 층마다 하나 | 각 커널은 가중치와 입력 activation을 DRAM에서 읽고 출력을 다시 쓰며, 모든 피연산자를 한 번씩만 옮긴다 |

**G-100**, 교과용 GPU. 모든 숫자는 산수가 깔끔하도록 고른 교과용 어림값이고, 어떤 제품의 사양도 아니다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $P$ | $100$ TFLOP/s $=10^{14}$ FLOP/s | bf16 텐서 연산의 최대 처리량, dense 기준 |
| $\beta$ | $1{,}000$ GB/s $=10^{12}$ 바이트/s | DRAM(전역 메모리) 대역폭 |
| $I^\star=P/\beta$ | $100$ FLOP/byte | §3의 능선점 |
| $t_L$ | $5$ µs | launch 오버헤드. 호스트가 커널 하나를 내보내는 고정 비용(§4) |
| $\beta_{\text{host}}$ | $25$ GB/s | 호스트 메모리와 GPU 사이의 링크(§2) |

숫자 둘은 교과용 값이 아니라 CUDA 하드웨어의 사실이다. 워프는 스레드 32개이고, 전역 메모리는 32바이트 섹터 단위로 읽힌다(§1, §2). 로봇 쪽은 [[03-deep-learning/foundations/training-at-scale|1.3 §11]]이 Jetson Thor에 대해 인용한 값만 다시 쓴다. 희소 fp4 $2{,}070$ TFLOPS, $273$ GB/s, 약 $7{,}600$ FLOP/byte의 능선점이다.

*범위: 이 페이지는 GPU 실행 모델과 CUDA를 읽는 수준으로 — 커널, 스레드, 블록, 그리드, 워프, 메모리 계층 — 가르치고, 로봇 학습 연구자가 쓰는 성능 추론을 쓰는 수준으로 가르친다. 병합 접근, 산술 강도와 루프라인, 배치가 사 주는 것과 launch 오버헤드가 지배하는 곳, 병렬 시뮬레이터가 모든 것을 GPU에 두는 이유, 타일링이 하는 일, 프로파일러로 재는 법, 그리고 로봇 위에서 무엇이 달라지는지다. 실전용 CUDA 작성 — occupancy 조율, 텐서 코어 프로그래밍, 스트림, 다중 GPU — 은 가르치지 않는다. 그것은 CUDA Programming Guide의 몫이다. 시뮬레이터 자체도 아니다. 그것은 [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]이다. 수 형식과 양자화도 아니다. 그것은 [[03-deep-learning/foundations/training-at-scale|1.3 §4와 §11]]이다. 분산 학습도 아니다. NVIDIA Warp나 JAX로 GPU 시뮬레이터를 쓰는 일은 §5–§6이 다루는 만큼만 가르친다. 페이지 주인에게 그것이 필요한 것은 학위논문이 흙이나 변형 재료를 위한 자체 시뮬레이터를 요구할 때뿐이기 때문이다. [[05-construction-robotics/sim-to-real|7.5 Sim-to-Real §1]]과 [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터 §5]]가 그 공백을 짚는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 432" style="max-width:100%;height:auto" role="img" aria-label="패널 두 개. (a) 로그-로그 축 위의 G-100 루프라인: 기울어진 지붕은 1 TB/s 곱하기 강도, 평평한 지붕은 100 TFLOP/s이고 둘은 능선 100 FLOP/byte에서 만난다. 환경 하나에서 MLP-256의 세 층은 모두 1 FLOP/byte 근처에 있고, 환경 4,096개에서는 256×256 층이 124 FLOP/byte로 평평한 지붕에 닿지만 입력층은 50.6, 출력층은 7.74로 각자의 상한 아래에 남는다. (b) 순전파 한 번을 같은 척도로: 환경 하나에서 15.17마이크로초이고 거의 전부가 5마이크로초짜리 launch 세 번이며, 환경 4,096개에서는 25.19마이크로초다.">
  <text x="12" y="18" font-size="12" fill="currentColor">(a) G-100 루프라인 위의 MLP-256</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.15"><line x1="119.7" y1="44" x2="119.7" y2="246"/><line x1="259.8" y1="44" x2="259.8" y2="246"/><line x1="399.9" y1="44" x2="399.9" y2="246"/><line x1="540.0" y1="44" x2="540.0" y2="246"/><line x1="64" y1="217.2" x2="540" y2="217.2"/><line x1="64" y1="145.0" x2="540" y2="145.0"/><line x1="64" y1="72.8" x2="540" y2="72.8"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.6" fill="none"><line x1="64" y1="44" x2="64" y2="246"/><line x1="64" y1="246" x2="540" y2="246"/></g>
  <text x="119.7" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">1</text>
  <text x="259.8" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">10</text>
  <text x="399.9" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">100</text>
  <text x="540.0" y="260" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.8">1000</text>
  <text x="58" y="221.2" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">1</text>
  <text x="58" y="149.0" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">10</text>
  <text x="58" y="76.8" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">100</text>
  <text x="302" y="274" font-size="11" fill="currentColor" text-anchor="middle">산술 강도 I (FLOP/byte), 로그 척도</text>
  <text x="58" y="36" font-size="11" fill="currentColor" text-anchor="end">TFLOP/s</text>
  <polyline points="64.0,246.0 399.9,72.8 540.0,72.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <line x1="399.9" y1="72.8" x2="399.9" y2="246" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.7"/>
  <text x="536.0" y="50.8" font-size="11" fill="currentColor" text-anchor="end">평평한 지붕</text>
  <text x="536.0" y="64.8" font-size="11" fill="currentColor" text-anchor="end">P = 100 TFLOP/s</text>
  <text x="405.9" y="238" font-size="11" fill="currentColor">능선 I* = P/β = 100</text>
  <line x1="161.9" y1="198.5" x2="171.9" y2="223" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="150" y="234" font-size="11" fill="currentColor">기울어진 지붕 I × β, β = 1 TB/s</text>
  <text x="72" y="58" font-size="11" fill="currentColor">● N = 4,096     ○ N = 1</text>
  <text x="72" y="72" font-size="11" fill="currentColor" fill-opacity="0.85">• N = 4, 16, 64, 256, 1024의 256→256</text>
  <circle cx="202.2" cy="174.7" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="281.3" cy="133.9" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="348.1" cy="99.5" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="390.3" cy="77.7" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <circle cx="407.8" cy="72.8" r="2.4" fill="currentColor" fill-opacity="0.55"/>
  <text x="385.3" y="71.7" font-size="10" fill="currentColor" fill-opacity="0.85" text-anchor="end">256</text>
  <text x="410.8" y="64.8" font-size="10" fill="currentColor" fill-opacity="0.85">1024</text>
  <circle cx="118.6" cy="217.9" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="119.3" cy="217.5" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="112.4" cy="221.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="98" y1="121" x2="117.1" y2="212.6" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <text x="72" y="104" font-size="11" fill="currentColor">N = 1: 세 층이 0.89–0.99 FLOP/byte,</text>
  <text x="72" y="118" font-size="11" fill="currentColor" fill-opacity="0.85">능선까지 가는 길의 1%</text>
  <circle cx="244.3" cy="153.0" r="4" fill="currentColor"/>
  <circle cx="358.4" cy="94.1" r="4" fill="currentColor"/>
  <circle cx="413.1" cy="72.8" r="4" fill="currentColor"/>
  <text x="254.3" y="173.0" font-size="11" fill="currentColor" font-weight="bold">256→8: 7.74</text>
  <text x="254.3" y="187.0" font-size="11" fill="currentColor" fill-opacity="0.85">(상한 7.76)</text>
  <text x="391.9" y="134.1" font-size="11" fill="currentColor" font-weight="bold" text-anchor="end">64→256: 50.6</text>
  <text x="391.9" y="148.1" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="end">(상한 51.2)</text>
  <text x="421.1" y="90.8" font-size="11" fill="currentColor" font-weight="bold">256→256: 124</text>
  <text x="421.1" y="104.8" font-size="11" fill="currentColor" fill-opacity="0.85">계산 한계</text>
  <text x="12" y="294" font-size="12" fill="currentColor">(b) 순전파 한 번, 같은 척도</text>
  <rect x="76.0" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="156.0" y="308" width="1.2" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="156.5" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="236.5" y="308" width="2.1" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="238.6" y="308" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="318.6" y="308" width="1.2" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="76.0" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="156.0" y="348" width="42.5" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <rect x="198.5" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="278.5" y="348" width="85.9" height="18" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.6"/>
  <rect x="364.4" y="348" width="80.0" height="18" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <rect x="444.4" y="348" width="34.7" height="18" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <text x="70" y="321" font-size="11" fill="currentColor" text-anchor="end">N = 1</text>
  <text x="70" y="361" font-size="11" fill="currentColor" text-anchor="end">N = 4,096</text>
  <text x="76" y="339" font-size="11" fill="currentColor" fill-opacity="0.9">15.17 µs: launch 15 µs (98.9%), 커널 0.17 µs — 환경당 15.17 µs</text>
  <text x="76" y="379" font-size="11" fill="currentColor" fill-opacity="0.9">25.19 µs = launch 15 µs + 2.65 + 5.37 + 2.17 µs — 환경당 6.15 ns</text>
  <line x1="76" y1="390" x2="492.0" y2="390" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <line x1="76.0" y1="390" x2="76.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="76.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">0</text>
  <line x1="156.0" y1="390" x2="156.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="156.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">5</text>
  <line x1="236.0" y1="390" x2="236.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="236.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">10</text>
  <line x1="316.0" y1="390" x2="316.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="316.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">15</text>
  <line x1="396.0" y1="390" x2="396.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="396.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">20</text>
  <line x1="476.0" y1="390" x2="476.0" y2="394" stroke="currentColor" stroke-width="1" stroke-opacity="0.5"/>
  <text x="476.0" y="405" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">25</text>
  <text x="498.0" y="405" font-size="10" fill="currentColor" fill-opacity="0.8">µs</text>
  <rect x="76" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <text x="100" y="420" font-size="11" fill="currentColor">launch, 5 µs</text>
  <rect x="206" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.6"/>
  <text x="230" y="420" font-size="11" fill="currentColor">메모리 한계 커널</text>
  <rect x="376" y="411" width="18" height="10" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.6"/>
  <text x="400" y="420" font-size="11" fill="currentColor">계산 한계 커널</text>
</svg>

G-100의 루프라인 위에 놓인 MLP-256의 세 층이다. 기울어진 지붕은 1 TB/s 곱하기 강도, 평평한 지붕은 100 TFLOP/s이고, 둘은 능선점 100 FLOP/byte에서 만난다. 환경 하나에서는 세 층이 모두 1 FLOP/byte 근처, 능선점까지 가는 길의 1%에 있고, 4,096개에서는 256×256 층이 능선점을 넘어서(124 FLOP/byte, 계산 한계) 입력층과 출력층만 각자의 상한 51.2와 7.76 아래에서 메모리 한계로 남는다. 아래는 순전파 한 번을 같은 척도로 그린 것으로, $N=1$에서는 15.17 µs 가운데 15 µs가 launch 세 번이고, $N=4{,}096$에서는 25.19 µs, 환경당 6.15 ns다.

### 대상으로 한 번 끝까지 · Worked case

이것이 두 규모 모두에서 과제의 대상이다. 과제는 능선점을 옮기고, 신경망을 넓히고, 배치를 바꾼다. 카탈로그 판을 여기서 먼저 하면 과제는 첫 유도가 아니라 손잡이를 바꾸는 일이 된다. 용어 셋은 여기서 한 줄로 풀고 뒤에서 유도한다. 커널의 **산술 강도**(arithmetic intensity) $I=F/B$는 DRAM 트래픽 1바이트당 FLOP이다(§3). **루프라인**(roofline) 위에서 커널의 시간은 적어도 $F/P$와 $B/\beta$ 중 큰 쪽이고, 뒤쪽이 크면 메모리 한계, 아니면 계산 한계다(§3). 그리고 모든 커널은 돌기 전에 launch 오버헤드 $t_L$을 치른다(§4).

**층 하나 세기.** 층은 $N\times n_{\text{in}}$ activation 행렬에 $n_{\text{out}}\times n_{\text{in}}$ 가중치 행렬의 전치를 곱한다. 가중치 하나는 환경마다 곱셈 하나와 덧셈 하나에 쓰이고 — [[03-deep-learning/foundations/training-at-scale|1.3 §6]]의 순방향 곱, 가중치당 2 FLOP — 커널은 피연산자를 숫자당 $e=2$바이트로 한 번씩 옮긴다.

$$F_\ell=2Nn_{\text{in}}n_{\text{out}},\qquad B_\ell=e\big(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}}\big),\qquad t_\ell=t_L+\max\Big(\frac{F_\ell}{P},\ \frac{B_\ell}{\beta}\Big)$$

가중치는 $N$이 얼마든 한 번 읽히지만 입력과 출력은 $N$과 함께 자라기 때문이다.

**환경 하나.** 2층은 $F=2\cdot1\cdot256\cdot256=131{,}072$ FLOP, $B=2(65{,}536+256+256)=132{,}096$바이트이므로 $I=0.992$ FLOP/byte다. 트래픽은 거의 전부 가중치이고 가중치 하나는 한 번만 쓰이니, 1.3 §11의 디코딩처럼 바이트당 1 FLOP이다. 두 지붕 아래에서 $F/P=0.00131$ µs, $B/\beta=0.13210$ µs이므로 이 층은 메모리 한계다. 세 층 모두:

| 층 | $n_{\text{in}}\to n_{\text{out}}$ | $F$ (FLOP) | $B$ (바이트) | $I$ (FLOP/byte) | $F/P$ (µs) | $B/\beta$ (µs) | 한계 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | $64\to256$ | 32,768 | 33,408 | 0.981 | 0.00033 | 0.03341 | 메모리 |
| 2 | $256\to256$ | 131,072 | 132,096 | 0.992 | 0.00131 | 0.13210 | 메모리 |
| 3 | $256\to8$ | 4,096 | 4,624 | 0.886 | 0.00004 | 0.00462 | 메모리 |
| 전체 | | 167,936 | 170,128 | 0.987 | | 0.1701 | |

$$t(1)=3t_L+\sum_\ell\frac{B_\ell}{\beta}=15+0.1701=15.170\ \mu\text{s}$$

커널 셋이 각각 돌기 전에 $t_L=5$ µs를 치르기 때문이다. 신경망 자신의 트래픽은 0.17 µs이고, 순전파의 98.9%가 launch다. 15.17 µs에 167,936 FLOP이니 11.1 GFLOP/s, $P$의 약 만분의 일이다.

**환경 4,096개.** 이제 가중치를 한 번 읽을 때마다 4,096번 쓴다.

| 층 | $n_{\text{in}}\to n_{\text{out}}$ | $F$ (FLOP) | $B$ (바이트) | $I$ (FLOP/byte) | $F/P$ (µs) | $B/\beta$ (µs) | 한계 |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | $64\to256$ | 134,217,728 | 2,654,208 | 50.568 | 1.34218 | 2.65421 | 메모리 |
| 2 | $256\to256$ | 536,870,912 | 4,325,376 | 124.121 | 5.36871 | 4.32538 | **계산** |
| 3 | $256\to8$ | 16,777,216 | 2,166,784 | 7.743 | 0.16777 | 2.16678 | 메모리 |
| 전체 | | 687,865,856 | 9,146,368 | 75.206 | | | |

2층은 이제 능선점 위($124.1>100$)에 있어 평평한 지붕 아래에서 돌고, 1층과 3층은 여전히 그 아래다. 커널마다 큰 쪽 시간을 더하면

$$t(4096)=3t_L+2.654+5.369+2.167=15+10.190=25.190\ \mu\text{s}$$

환경당 $25.19/4096=6.15$ ns로, $N=1$의 15.17 µs보다 환경당 2,467배 싸고 벽시계 시간은 1.66배일 뿐이다. 순전파는 $687.9\ \text{MFLOP}/25.19\ \mu\text{s}=27.3$ TFLOP/s, $P$의 27%에 이르고, 그래도 launch가 60%를 차지한다.

**얇은 층이 메모리 한계에 머무는 이유.** $B_\ell$을 $F_\ell$로 나누면 bf16에서 $1/I_\ell=1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})$이다(§4). 그래서 $N$이 커지면 층의 강도는 상한 $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$으로 다가가되 넘지 못한다. 2층 128, 1층 51.2, 3층 7.76이다. 출력층은 환경 하나에 $2\cdot256\cdot8=4{,}096$ FLOP을 하려고 activation $2(256+8)=528$바이트를 옮기니 $4{,}096/528=7.76$이고, 어떤 배치도 이 비를 바꾸지 못한다. 상한이 능선점 아래인 층은 모든 $N$에서 메모리 한계다.

**평균은 갈라짐을 숨긴다.** $N=4{,}096$에서 순전파 전체는 $687.9\ \text{M}/9.15\ \text{M}=75.2$ FLOP/byte로 능선점 아래다. 전부 메모리 한계인 것처럼 보이지만, FLOP의 78%를 가진 층은 계산 한계다. 강도는 신경망이 아니라 커널의 것이다. §9가 두 표의 숫자를 모두 출력한다.

### 1. GPU인 이유: 많은 스레드, 워프, 지연 숨기기

*한 문장으로:* GPU는 스레드 수만 개를 32개씩 묶어 한꺼번에 돌려서 빠르고, 그중 일부가 메모리를 기다리는 동안에는 준비된 다른 묶음으로 넘어가 쉬지 않는다.

CPU 코어는 스레드 하나의 명령을 가능한 한 빨리 끝내도록, 기다림을 피하는 큰 캐시와 정교한 제어 논리를 갖춰 만든다. GPU는 반대쪽을 택한다. 스레드 수천 개를 병렬로 돌리도록 설계되어 스레드 하나의 속도를 내주고 전체 처리량을 얻으며, CPU보다 트랜지스터를 연산 장치에 더 쓰고 캐시와 흐름 제어에 덜 쓴다(CUDA Programming Guide §1.1.2). 대가는 독립적인 일감을 수천 개 받아야만 빠르다는 것이다. $N=4{,}096$의 MLP-256 2층은 출력이 $4{,}096\times256=1{,}048{,}576$개이고 각각이 항 256개짜리 내적이니 일감이 넉넉하다. $N=1$에서는 256개다.

**일을 적는 법.** CUDA는 병렬 작업을 커널로 표현하고, 호스트는 세 겹 꺾쇠 안의 실행 구성으로 그것을 launch한다. `kernel<<<G, B>>>(args)`는 스레드 $B$개짜리 블록 $G$개이고, 스레드마다 커널 본문을 한 번 돈다. 내장 변수 넷이 스레드에게 자기가 누구인지 알려 준다. `threadIdx`는 블록 안의 번호, `blockIdx`는 그리드 안에서 블록의 번호, `blockDim`과 `gridDim`은 블록과 그리드의 크기다. 커널의 첫 줄은 보통 이것들로 전역 번호를 만든다(Programming Guide §2.1.2). 꺾쇠 안에는 선택 인자 둘이 더 올 수 있다. 블록마다 받을 동적 공유 메모리와, launch가 들어갈 스트림이다. launch는 커널이 돌기 전에 곧바로 호스트로 돌아온다.

> **CUDA 실행 모델의 정의.** **CUDA 실행 모델**(CUDA execution model)은 *병렬 작업을 어떻게 조직하고 스케줄할지에 대한 프로그램과 NVIDIA GPU 사이의 계약*이다. 프로그래밍 모델이고, 라이브러리도 하드웨어 부품도 아니다. 정의 조건 넷. **커널**은 `__global__`로 표시한 함수로, 호스트에서 launch되어 디바이스에서 많은 스레드가 실행하며, 모든 스레드가 스스로 계산한 번호 위에서 같은 코드를 돈다. launch는 비동기이므로 호스트는 곧바로 다음으로 간다. 스레드는 최대 1,024개짜리 **블록**으로 묶인다. 한 블록의 스레드는 모두 스트리밍 멀티프로세서(SM) 하나에서 돌고, 거기서 칩 위 메모리를 나누어 쓰며 장벽에서 서로를 기다릴 수 있다. 블록들은 **그리드**를 이루고, 프로그램은 블록이 어떤 순서로 돌든 — 병렬이든 차례로든 — 옳아야 한다. 그러니 어떤 블록도 다른 블록을 기다려서는 안 된다. 그리고 SM은 블록의 스레드를 연속된 32개씩 **워프**로 묶어, 한 번에 명령 하나를 함께 내보내며 돌린다. 단일 명령 다중 스레드(SIMT)다. 워프의 스레드들이 서로 다른 분기로 가면, 워프는 각 경로를 차례로 돌며 그 경로에 없는 스레드를 가려 둔다(Programming Guide §1.2.2.1–§1.2.2.2).
>
> $$i=b\,B+t,\qquad 0\le t<B\le1024,\qquad G=\Big\lceil\frac{n}{B}\Big\rceil,\qquad \text{블록당 워프}=\Big\lceil\frac{B}{32}\Big\rceil$$
>
> $t$는 `threadIdx.x`, $b$는 `blockIdx.x`, $B$는 `blockDim.x`, $G$는 `gridDim.x`, $n$은 원소 수, $i$는 스레드가 맡는 원소다. 그러므로 스레드가 $GB\ge n$개 출발하고, 마지막 블록의 남는 스레드는 경계 검사 `if (i < n)`으로 막는다. Programming Guide는 그 비용이 작다고 적는다(§2.1.2.3.1).
>
> - **예**: $N=4{,}096$의 MLP-256 2층을 출력 하나에 스레드 하나로 쓰기. $n=4{,}096\times256=1{,}048{,}576$이고, $B=256$이면 그리드는 워프 8개짜리 블록 $G=4{,}096$개, 워프로 모두 32,768개다. 스레드 $i$는 환경 $\lfloor i/256\rfloor$의 activation과 $W_2$의 $i\bmod256$번째 행의 내적을 계산한다.
> - **비예**: 환경마다 한 번씩 신경망을 부르는 Python 반복문. 출력마다 스레드를 둔 launch 한 번이 아니라 배치 1 순전파 4,096번이고, 저마다 launch를 치른다(§4).
> - **비예**: 블록 7이 블록 3이 쓰는 값을 기다리는 커널. 블록은 어떤 순서로든 돌 수 있고 블록 3은 아직 시작도 안 했을 수 있다. 모든 블록의 결과가 필요한 단계는 두 번째 커널에 두어야 하고, 그 커널은 첫 커널이 끝난 뒤에야 시작한다.
> - **왜 중요한가**: GPU 시뮬레이터, 프레임워크 연산자, Warp 커널이 모두 이 모델로 쓰여 있다. 그래서 무엇을 읽든 같은 두 질문에서 시작한다. 스레드 $i$는 어느 원소를 맡는가, 어느 스레드가 어느 스레드를 기다려야 하는가.

**워프가 분기를 만나면.** 스레드 하나가 환경 하나를 진행시키는 물리 커널에 `if (done[i]) reset(i); else step(i);`가 있다고 하자. 32개 환경 중 셋이 막 끝난 워프는 스레드 29개를 가린 채 `reset`을 돌고, 다시 3개를 가린 채 `step`을 돈다. 32개 모두가 두 경로의 값을 치르는 것이다. 끝난 환경을 물리 스텝 안이 아니라, Isaac Lab의 환경들처럼(§5) 그 번호들 위의 별도 배치 스텝에서 리셋하는 이유 하나가 이것이다.

**스레드가 수만 개 필요한 이유.** 전역 메모리에서 읽은 값은 돌아오는 데 오래 걸리고, GPU는 그 스레드 하나의 기다림을 줄이려 하지 않는다. SM은 워프를 많이 상주시키고, 그 레지스터와 프로그램 카운터를 워프의 일생 동안 칩 위에 두므로 워프에서 워프로 넘어가는 데 비용이 없다. 명령을 내보내는 주기마다 스케줄러가 다음 명령이 준비된 워프를 고른다(Programming Guide §3.2.2.2). Programming Guide의 조언이 여기서 나온다. occupancy — SM이 최대로 담을 수 있는 워프 대비 활성 워프의 비율 — 를 가능한 한 높게 두라. 그것이 지연을 숨기기 때문이다(§2.3.7). 기다림은 줄지 않고 채워진다.

> **지연 숨기기의 정의.** **지연 숨기기**(latency hiding)는 *GPU가 워프를 스케줄하는 방식의 성질*이다. 스레드 하나하나가 기다리는 동안 연산 장치와 메모리 장치를 바쁘게 두는 방식이고, 캐시도 아니고 어떤 스레드 하나를 빠르게 하는 것도 아니다. 정의 조건 넷. SM마다 워프가 한꺼번에 많이 **상주**한다. 상주한 워프마다 **실행 문맥이 칩 위에 남아** 있어, 워프를 바꾸는 데 시간이 들지 않는다. 명령을 내보내는 주기마다 **스케줄러가 다음 명령이 준비된 워프를 고르므로**, 메모리를 기다리는 워프는 그냥 뽑히지 않는다. 그리고 커널이 기다림을 덮을 만큼 **독립적인 일을 충분히 띄워 둔다**. Little의 법칙에 따르면, 초당 $\beta$바이트를 지연 $\ell$로 배달하는 메모리 시스템은 매 순간 $\beta\ell$바이트가 요청되고 아직 돌아오지 않은 상태여야 최대 속도로 돈다.
>
> $$Q=\beta\,\ell,\qquad t_{\text{mem}}\ \ge\ \max\Big(\frac{B}{\beta},\ \ell\Big)$$
>
> $Q$는 날아가는 중인 바이트, $\beta$는 DRAM 대역폭, $\ell$은 메모리 왕복 한 번의 시간, $B$는 커널이 옮기는 바이트, $t_{\text{mem}}$은 그 메모리 시간이다. 그러므로 G-100의 $\beta=10^{12}$바이트/s에서는 지연 1마이크로초마다 1메가바이트가 날아가는 중이어야 하고, 전체 트래픽이 $\beta\ell$보다 작은 커널은 바이트가 아무리 적어도 대략 지연 한 번보다 빨리 끝날 수 없다.
>
> - **예**: $N=4{,}096$의 MLP-256 2층은 4.33 MB, G-100 대역폭으로 4.33 µs어치를 옮기고, 독립적인 일을 워프 32,768개어치 내놓는다. SM은 그 가운데 담을 수 있는 만큼을 상주시키고 — 그 수는 GPU마다 다르며 G-100은 고정하지 않는다 — 그 사이를 오간다.
> - **비예**: 같은 층의 $N=1$은 132,096바이트, 대역폭으로 0.13 µs어치를 출력당 스레드 하나로 워프 8개가 옮긴다. 지연이 0.13 µs보다 길기만 하면 지연 한 번어치에도 못 미치므로, 그 시간은 $B/\beta$가 아니라 $\ell$이 정한다. 기울어진 지붕이 배치 1 커널이 실제로 닿는 값을 부풀리는 이유가 하나 더 생긴다.
> - **비예**: CPU의 큰 캐시. 붙들어 둔 데이터에 대해서는 기다림 자체를 피한다. 지연 숨기기는 다른 일을 하면서 기다림을 견디는 것이라, 그 다른 일이 있어야 한다.
> - **왜 중요한가**: GPU는 병렬 여유가 있을 때만 빠르고, 로봇 하나의 관측에는 그것이 없고 시뮬레이터의 환경 4,096개에는 있다(§4, §5).

### 2. 메모리 계층과 병합 접근

*한 문장으로:* 데이터는 레지스터에서 호스트 메모리까지 계층에 놓이고 아래로 갈수록 크고 느리며, 워프가 전역 메모리에서 읽는 값은 32개 스레드가 이웃한 주소를 읽을 때만 싸다.

| 수준 | 위치 | 누가 쓰나 | 수명 | 알아 둘 것 |
|---|---|---|---|---|
| 레지스터 | SM 위 | 스레드 하나 | 그 스레드 | 가장 빠른 저장소. 컴파일러가 배정한다(Programming Guide §2.3.3.3) |
| 로컬 메모리 | 디바이스 DRAM, 캐시를 거침 | 스레드 하나 | 그 스레드 | 레지스터가 넘칠 때 가는 곳. 전역 메모리만큼 느리다(§2.3.3.4) |
| 공유 메모리 | SM 위, L1과 같은 저장소 | 블록 하나의 스레드들 | 그 블록 | `__shared__`로 선언. 전역 메모리보다 대역폭이 훨씬 크고 지연이 짧다. `__syncthreads()` 장벽 뒤에 읽는다(§2.3.3.2) |
| L1, L2 캐시 | L1은 SM마다, L2는 모든 SM이 공유 | 자동 | — | 반복 읽기가 DRAM에 닿기 전에 잡는다(§1.2.3.3.1) |
| 전역 메모리 | GPU의 DRAM | 모든 커널의 모든 스레드, 호스트는 복사로 | 해제할 때까지 | 32바이트 섹터로 읽힌다(§2.3.4.1). G-100에서 $\beta=1{,}000$ GB/s |
| 호스트 메모리 | CPU의 DRAM | 호스트, GPU는 복사로 | 해제할 때까지 | G-100까지 $25$ GB/s. 고정(pinned) 메모리가 복사에 가장 빠르다(Best Practices §10.1.1) |

이 표의 틈 두 개가 나머지를 정한다. *칩 위 대 칩 밖*: 공유 메모리는 전역 메모리보다 대역폭이 훨씬 크고 지연이 짧으므로(Best Practices §10.2.3), 값을 공유 메모리에 한 번 올려 거기서 재사용하는 커널은 전역 트래픽을 아낀다. §6의 타일링이다. *디바이스 대 호스트*: G-100의 DRAM은 호스트 링크의 40배를 배달한다. NVIDIA 자신이 드는 같은 틈의 예는 Tesla V100의 디바이스 메모리 898 GB/s 대 PCIe x16 Gen3의 16 GB/s다(Best Practices §10.1).

**전역 메모리를 읽는 방식.** 전역 메모리는 섹터라 부르는 32바이트 트랜잭션 단위로 오가고, 워프의 적재 32개는 함께 처리된다. compute capability 6.0 이상의 장치에서는 워프의 접근들이 그것을 덮는 데 필요한 만큼의 32바이트 트랜잭션으로 합쳐진다(Best Practices §10.2.1). 그러니 대역폭을 쓰는 것은 적재하는 스레드의 수가 아니라, 그 주소들이 떨어지는 서로 다른 섹터의 수다.

> **병합 접근의 정의.** 워프의 전역 메모리 접근이 **병합되었다**(coalesced)는 것은 스레드 32개의 주소가 총 크기가 허락하는 가장 적은 수의 32바이트 섹터에 들어간다는 뜻이다. *워프 접근 패턴의 성질*로, 스레드가 계산하는 주소가 정하며, 데이터 형식의 성질도 커널 전체의 성질도 아니다. 정의 조건 셋. 전송 단위는 **32바이트 섹터**이고, 워프의 접근은 스레드들이 건드리는 서로 다른 섹터 하나마다 트랜잭션 하나를 치른다. 스레드 32개의 요청은 **함께 처리되어**, 꼭 필요한 트랜잭션으로 합쳐진다. 그리고 **효율은 쓰인 바이트 나누기 옮겨진 바이트**라서, 워프가 건드리는 바이트가 정렬된 섹터를 온전히 채울 때만 100%에 닿는다. 섹터에 맞춘 시작점에서 이웃한 스레드가 이웃한 주소를 읽는 것이 흔한 경우이고, 그 섹터들 안에서 순서를 뒤섞어도 값은 같다(Best Practices §10.2.1.1).
>
> $$S=\min\Big(w,\ \Big\lceil\frac{w\,\sigma e}{s}\Big\rceil\Big),\qquad \eta=\frac{w\,e}{s\,S}$$
>
> $w=32$는 워프당 스레드, $s=32$는 섹터당 바이트, $e$는 원소당 바이트, $\sigma$는 이웃한 스레드의 원소 사이 간격(stride), $S$는 섹터에 맞춘 시작점에서 워프가 필요로 하는 섹터 수(2의 거듭제곱 간격일 때), $\eta$는 옮겨진 바이트 중 스레드가 쓰는 비율이다. 그러므로 fp32에서 간격 1인 워프는 섹터 4개를 쓰고 128바이트를 모두 쓰며, 간격이 32바이트 이상이면 섹터 32개를 쓰고 1,024바이트 중 128바이트, 12.5%만 쓴다. Programming Guide가 따라가 보이는 두 경우다(§2.3.4.1).
>
> - **예**: 행 단위로 저장한 bf16 $W_2$. 워프가 한 행의 연속된 가중치 32개를 읽으면($\sigma=1$, $e=2$) 섹터 $\lceil64/32\rceil=2$개이고 64바이트를 모두 쓴다.
> - **비예**: 같은 워프가 한 열을 읽기, 스레드 $k$가 $W_2[k,j]$를 맡는다. 간격이 원소 256개, 512바이트라서 스레드마다 자기 섹터에 떨어진다. 섹터 32개, 64바이트를 쓰려고 1,024바이트를 옮기니 6.25%이고, 같은 숫자 32개에 트래픽이 열여섯 배다.
> - **비예**: fp32에서 간격은 1이지만 섹터 경계에서 4바이트 지난 곳에서 시작하기. 섹터가 4개가 아니라 5개다(Best Practices §10.2.1.2). CUDA 런타임은 할당을 적어도 256바이트에 맞추므로, 어긋남은 할당기가 아니라 인덱싱에서 온다.
> - **왜 중요한가**: 루프라인의 $\beta$는 옮긴 바이트를 모두 쓴다고 가정한다. $W_2$를 열로 읽는 커널의 실효 대역폭은 $\eta\beta=62.5$ GB/s이고, 그 기울어진 지붕은 그림의 것보다 열여섯 배 낮다.

실습(§9)은 모든 간격에 대해 주소 자체에서 섹터를 센다. 단계는 공식 그대로다. fp32는 간격 1, 2, 4, 8에서 섹터 4, 8, 16, 그리고 32개가 되는데, 원소 8개가 32바이트다. bf16은 간격 16에서야 32개에 닿는다. Best Practices §10.2.1.4도 같은 하락 — 간격 2에서 효율 50%, 그 뒤로 스레드마다 섹터를 하나씩 차지할 때까지 더 낮아짐 — 을 적고, 간격이 1이 아닌 접근은 될 수 있는 한 피하라고 결론짓는다.

**호스트–디바이스 전송.** 환경 4,096개의 관측, $4{,}096\times64\times2=524{,}288$바이트를 G-100의 DRAM에서 읽으면 0.52 µs, 호스트 링크로 옮기면 20.97 µs이고, 전송마다 치르는 고정 오버헤드는 그 전이다. NVIDIA의 안내서는 여기서 규칙 셋을 끌어낸다(Best Practices §10.1). 커널 사이에서 데이터를 디바이스에 두라, CPU보다 빠르지 않은 커널을 GPU에서 돌리게 되더라도. 중간 데이터는 디바이스에서 만들고 호스트로 복사하지 말라. 작은 전송 여럿을 큰 전송 하나로 묶으라. 고정(page-locked) 호스트 메모리에서의 복사가 가장 빠르고 비동기로 돌아 계산과 겹칠 수 있지만(§10.1.1–§10.1.2), 고정 메모리는 귀한 자원이라 너무 쓰면 시스템 전체가 느려진다. Jetson에서는 CPU와 GPU가 DRAM 하나를 나누어 쓰므로 이 링크가 없다(§8).

### 3. 산술 강도와 루프라인

*한 문장으로:* 커널은 GPU가 얼마나 빨리 계산하느냐, 아니면 데이터를 얼마나 빨리 가져오느냐에 묶이고, 커널의 바이트당 FLOP — 산술 강도 — 이 GPU가 정한 문턱과 비교해 어느 쪽인지 말해 준다.

커널에는 산술을 위한 시간, 잘해야 $F/P$와, 데이터를 옮기는 시간, 잘해야 $B/\beta$가 필요하다. 둘이 완벽히 겹치면 큰 쪽이 결정한다. 둘의 비는 커널의 성질과 기계의 성질로 갈라진다.

$$\frac{F/P}{B/\beta}=\frac{F/B}{P/\beta}$$

그러므로 커널은 자기 바이트당 FLOP이 기계의 바이트당 FLOP을 넘을 때 정확히 계산에 묶인다.

> **산술 강도의 정의.** 커널의 **산술 강도**(arithmetic intensity)는 *커널이 하는 산술 대 DRAM과 칩 사이에서 옮기는 바이트의 비*다. 주어진 데이터 레이아웃(메모리 배열)과 배치 크기 위에서 구현된 커널 하나의 성질이고, GPU의 성질도 모델의 수학만의 성질도 아니다. 정의 조건 셋. 분자는 **쓸모 있는 부동소수점 연산**을 곱셈-덧셈 하나에 둘로 센다. 분모는 **DRAM 트래픽**, 곧 캐시가 반복 읽기를 잡고 난 뒤 전역 메모리와 SM 사이를 오가는 바이트를 센다. 스레드가 내보내는 적재 횟수가 아니며, 그것은 §6이 따로 센다. 그리고 둘 다 **커널 하나에 대해** 센다. 커널이 둘이면 강도도 둘이고, 신경망 전체 합계의 비는 어느 커널의 강도도 아니다.
>
> $$I=\frac{F}{B},\qquad I_\ell(N)=\frac{2Nn_{\text{in}}n_{\text{out}}}{e\big(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}}\big)}$$
>
> $F$는 FLOP, $B$는 바이트이고, 둘째 식은 숫자당 $e$바이트, 피연산자를 한 번씩 옮기는 배치 $N$의 dense 층의 강도다. 그러므로 강도는 배치와 함께 자라는데, 배치 전체가 나누어 쓰는 것은 가중치뿐이기 때문이다. 그리고 $e$와 함께 줄어드는데, 같은 산술이 더 많은 바이트를 옮기기 때문이다.
>
> - **예**: MLP-256 2층, $N=1$에서 $131{,}072/132{,}096=0.992$ FLOP/byte, $N=4{,}096$에서 124.1.
> - **비예**: $N=4{,}096$의 신경망 전체, $687.9\ \text{M}/9.15\ \text{M}=75.2$ FLOP/byte. FLOP의 78%를 가진 층이 G-100의 능선점 위에 있는데도 순전파 전체를 그 아래에 둔다.
> - **비예**: 스레드가 내보내는 적재를 세기. §6의 단순 커널은 $N=4{,}096$의 2층에 대해 1.07 GB어치 적재를 내보내지만, 그 DRAM 트래픽은 4.33 MB까지 작을 수 있다. 강도는 DRAM에 닿는 것이 정한다.
> - **왜 중요한가**: 루프라인이 커널에 대해 알아야 하는 유일한 성질이고, 배치(§4), 타일링(§6), 융합(§8)이 바꾸는 것도 이것이다.

> **루프라인 모델의 정의.** **루프라인 모델**(roofline model)은 *기계 하나에 대해 그린, 산술 강도의 함수로서의 커널 처리량 상한*이다. 시각적 성능 모델이고(Williams, Waterman, Patterson, 2009), 상한에 닿는다는 예측도 벤치마크도 아니다. 정의 조건 넷. 기계는 커널이 실제로 쓰는 정밀도와 방식에 대한 **천장 둘**, 최대 산술 속도 $P$와 최대 DRAM 대역폭 $\beta$로 요약된다. 강도 $I$인 커널은 **어느 쪽도 넘지 못한다**. 초당 $P$ FLOP이 최대이고, 바이트마다 $I$ FLOP을 얻는데 바이트는 초당 $\beta$개가 최대이므로 초당 $I\beta$ FLOP도 최대다. 두 지붕은 **능선점** $I^\star=P/\beta$에서 만나고, 이것이 최대 성능에 닿을 수 있는 가장 작은 강도다. 그 아래 커널은 **메모리 한계**(memory-bound), 위의 커널은 **계산 한계**(compute-bound)다. 그리고 이 상한은 **산술과 데이터 이동이 완벽히 겹치고** 그 밖에 아무것도 — launch도, 지연도, 동기화도 — 끼어들지 않는다고 가정한다.
>
> $$\Pi(I)=\min\big(P,\ I\beta\big),\qquad I^\star=\frac{P}{\beta},\qquad t\ \ge\ \max\Big(\frac{F}{P},\ \frac{B}{\beta}\Big)$$
>
> $\Pi$는 닿을 수 있는 FLOP/s, $t$는 커널의 시간이다. 그러므로 로그–로그 축에서 상한은 기울기 1의 직선이 능선점에서 평평해지는 모양이고, 그림의 모양이 그것이다.
>
> - **예**: G-100의 능선점은 $10^{14}/10^{12}=100$ FLOP/byte다. $N=1$의 MLP-256 2층(0.992)은 기껏해야 0.99 TFLOP/s, 최대의 1%에 닿고, $N=4{,}096$(124.1)에서는 평평한 지붕 100 TFLOP/s에 닿는다.
> - **비예**: $N=1$의 MLP-256 순전파 전체를 시간으로 읽기. 루프라인은 0.17 µs를 주지만 launch 셋이 15 µs를 더한다. 무너지는 조건은 "그 밖에 아무것도 끼어들지 않는다"이다.
> - **비예**: 다른 정밀도나 방식의 지붕을 가져오기. Jetson Thor의 2,070 TFLOPS는 희소 fp4 등급이다([[03-deep-learning/foundations/training-at-scale|1.3 §11]]). dense bf16 커널의 평평한 지붕은 그보다 낮고, 얼마나 낮은지는 이 페이지가 아니라 데이터시트가 준다. 그와 함께 능선점도 왼쪽으로 간다.
> - **왜 중요한가**: "이 커널은 빠른가?"를 "어느 지붕 아래에 있고, 얼마나 아래인가?"로 바꾸고, 그래서 어떤 처방이 통할지 말해 준다. 능선점 아래면 강도를 올리고(배치, 타일링, 융합), 위면 산술을 줄이거나 더 빠른 형식을 쓴다.

용어는 하나만 빼고 논문의 것이다. Williams 외는 이 비를 *operational intensity*라 부르고 DRAM 트래픽에 대해 재며, 프로파일한 커널에 대해 루프라인 도표를 그려 줄 수 있는 NVIDIA의 Nsight Compute는 같은 비를 arithmetic intensity라 부른다(§7).

**그림 읽기.** $N=1$에서 세 층은 0.89–0.99 FLOP/byte, G-100 능선점까지 가는 길의 100분의 1에 있어서 기껏해야 0.9–1 TFLOP/s에 닿는다. $N=4{,}096$에서는 흩어진다. 출력층은 상한 7.76 아래의 7.74에서, 입력층은 51.2 아래의 50.6에서 멈추고, 2층은 124.1로 능선점을 지나 평평한 지붕에 닿는다. 시간은 더해지고, 강도는 평균 내지 않는다.

**로봇 위의 같은 물리.** [[03-deep-learning/foundations/training-at-scale|1.3 §11]]은 Jetson Thor에서 배치 1로 토큰 하나를 디코딩하는 3B 정책이 bf16에서 바이트당 약 1 FLOP이고 능선점은 약 7,600임을 보았다. 메모리 한계이니 시간은 바이트 나누기 273 GB/s, 6.0 GB에 22.0 ms다. $N=1$의 MLP-256도 같은 이유 — 가중치 하나를 한 번 읽어 한 번 쓴다 — 로 같은 강도에 있고 역시 메모리 한계이지만, 그 170,128바이트는 G-100 대역폭으로 0.17 µs, Thor 대역폭으로 0.62 µs다. "메모리 한계"는 둘 다에게 참이고, 시간을 정하는 것은 앞의 경우뿐이다. 1.3 §11이 할 수 없던 것은 배치다. 로봇 하나에는 관측이 하나이고, 시뮬레이터에는 4,096개가 있다(§4, §5).

**루프라인이 빼놓는 것.** §4가 값을 매기는 launch. 메모리 파이프를 채우기에는 너무 작은 커널의 지연(§1). 캐시 — 같은 168 KB 가중치를 거듭 읽는 순전파는 그것을 L2 캐시에서 찾을 수 있어 메모리 항이 더 작아진다. 그리고 호스트와의 모든 동기화(§7)다. $N=1$의 MLP-256에서는 이 가운데 첫째가 시간의 98.9%다.

### 4. 배치: 가중치 하나를 여러 환경에 재사용하기

*한 문장으로:* 환경 $N$개를 한꺼번에 층에 통과시키면 가중치를 모두를 위해 한 번만 읽으므로, activation 자신의 트래픽이 상한을 씌울 때까지 강도가 약 $N$배로 오르고, launch도 $N$번이 아니라 한 번 치른다.

배치는 능선점 아래 커널을 위한 §3의 손잡이이고, 그 대수는 한 줄이다. dense 층의 강도를 뒤집어 분수를 가르면 된다.

> **배치 평가의 정의.** **배치 평가**(batched evaluation)는 *신경망 하나를 독립적인 입력 $N$개에, 텐서에 배치 축을 앞에 붙인 순전파 한 번으로 실행하는 것*이다. 같은 계산을 스케줄하는 방식이고, 더 큰 모델도 근사도 아니다. 정의 조건 셋. 입력 $N$개가 **같은 가중치의 같은 함수**를 지나므로, 한 번 읽은 가중치가 모두를 섬긴다. 입력들은 **독립적**이다. 어느 것도 다른 것의 출력을 필요로 하지 않으니 $N$개가 한꺼번에 떠 있을 수 있다. 그리고 배치는 **연산마다 커널 하나**로 내보내져, 커널당 비용 — launch, 가중치 트래픽 — 을 입력마다가 아니라 순전파마다 한 번 치른다.
>
> $$\frac{1}{I_\ell(N)}=\frac{e}{2}\Big(\frac1N+\frac{1}{I_{\ell,\infty}}\Big),\qquad I_{\ell,\infty}=\frac{n_{\text{in}}n_{\text{out}}}{n_{\text{in}}+n_{\text{out}}}$$
>
> $I_{\ell,\infty}$는 층의 상한, $e$는 숫자당 바이트다. 그러므로 bf16($e=2$)에서 강도는 $N$과 상한을 병렬 저항 둘처럼 합친 것이다. $N\ll I_{\ell,\infty}$이면 $N$에 가깝고, $N\gg I_{\ell,\infty}$이면 상한에 가깝고, 둘 중 작은 쪽을 넘지 않는다.
>
> - **예**: 상한이 128인 MLP-256 2층. $N=16$에서 강도는 14.22로 $N$에 가깝고, $N=4{,}096$에서 124.1로 상한에 가깝다. G-100의 능선점은 $1/100=1/N+1/128$, 곧 $N=457.1$에서 넘는다.
> - **비예**: 환경 하나의 시간 스텝들. 스텝 $t+1$은 스텝 $t$가 만든 상태를 필요로 하므로, 시뮬레이터는 환경을 가로질러서는 배치할 수 있어도 시간을 가로질러서는 못 한다. 제어 루프는 GPU가 아무리 커도 순차적이다.
> - **비예**: 서로 다른 정책 $N$개가 모는 환경 $N$개 — 개체군이나, 로봇마다 파인튜닝한 사본. 재사용할 공유 가중치가 없어 신경망마다 제 가중치 트래픽과 제 launch를 치른다.
> - **왜 중요한가**: 시뮬레이터의 환경 4,096개는 정책에게 싸고 로봇 하나의 관측 하나는 결정 하나당 비싼 이유가 이것이고, 이득이 끝나는 곳도 말해 준다. 상한이다. 그 상한은 activation 트래픽을 없애야만 올라간다(§8).

배치가 나누어 주는 또 하나의 고정 비용은 루프라인에 아예 없다.

> **launch 오버헤드의 정의.** 커널의 **launch 오버헤드**(launch overhead)는 *호스트가 커널을 내보내는 데 쓰는 고정 시간*이다. 드라이버가 커널을 실행할 준비를 하는 일로, 커널이 무엇을 계산하든 내보낸 커널마다 한 번 치르며, 커널 자신의 실행 시간도 데이터 전송도 아니다. 정의 조건 셋. **커널마다** 치르고, 스레드나 바이트마다가 아니다. 스레드 백만 개의 launch도 하나짜리처럼 한 번 치른다. **호스트에서** 치르고, 디바이스는 그 뒤에야 커널을 시작할 수 있다. 그리고 **커널이 짧을 때** 문제가 된다. CUDA Programming Guide는 실행 시간이 짧은 커널에서는 이것이 끝에서 끝까지 걸리는 시간의 상당한 몫일 수 있다고 적는다(§4.2).
>
> $$t_{\text{pass}}=K\,t_L+\sum_{k=1}^{K}\max\Big(\frac{F_k}{P},\ \frac{B_k}{\beta}\Big)$$
>
> $K$는 순전파의 커널 수, $t_L$은 launch당 오버헤드다. 커널마다 제 launch를 기다리는 직렬 모델이고, launch를 돌고 있는 커널과 겹치는 §7의 경우는 이 합을 줄이기만 한다.
>
> - **예**: MLP-256은 커널 $K=3$개라서 G-100에서 순전파마다 15 µs를 치른다. 루프라인 시간은 $N=1$에서 0.17 µs, $N=4{,}096$에서 10.19 µs다.
> - **비예**: 첫 호출의 준비. CUDA 문맥을 만들고 코드를 컴파일하는 일은 그것이 필요한 첫 호출에서 한 번 일어난다(Programming Guide §2.1.6). launch마다가 아니라 예열 비용이다.
> - **비예**: 동기식 복사 `cudaMemcpy`. 이것에도 고정 부분이 있지만 호스트 링크로 바이트를 옮기고(§2), launch와 달리 호스트가 그것을 기다린다.
> - **왜 중요한가**: 작은 신경망에서는 산술이 아니라 이것이 스텝의 시간을 정하고, 세 처방 — 융합으로 커널 줄이기(§8), CUDA 그래프로 커널 여럿에 launch 한 번(§7), 그리고 배치 — 이 이것에 서로 다르게 작용한다.

**스윕.** 실습은 MLP-256을 직렬 모델로 여덟 배치에서 돌린다.

| $N$ | $I$, 1층 | $I$, 2층 | $I$, 3층 | 능선점을 넘은 층 | 루프라인 시간 (µs) | launch 3번 포함 (µs) | 환경당 (ns) | launch의 몫 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.98 | 0.99 | 0.89 | 0 | 0.170 | 15.170 | 15,170.13 | 98.9% |
| 4 | 3.71 | 3.88 | 2.64 | 0 | 0.177 | 15.177 | 3,794.18 | 98.8% |
| 16 | 12.19 | 14.22 | 5.22 | 0 | 0.203 | 15.203 | 950.19 | 98.7% |
| 64 | 28.44 | 42.67 | 6.92 | 0 | 0.308 | 15.308 | 239.19 | 98.0% |
| 256 | 42.67 | 85.33 | 7.53 | 0 | 0.729 | 15.729 | 61.44 | 95.4% |
| 1,024 | 48.76 | 113.78 | 7.70 | 1 | 2.575 | 17.575 | 17.16 | 85.3% |
| 4,096 | 50.57 | 124.12 | 7.74 | 1 | 10.190 | 25.190 | 6.15 | 59.5% |
| 16,384 | 51.04 | 127.01 | 7.75 | 1 | 40.648 | 55.648 | 3.40 | 27.0% |

**스윕 읽기.** 대수가 예측했고 숫자가 보여 주는 것 넷.

- **강도는 $N$을 따라가다 상한을 따라간다.** $N=4$에서 세 층은 3.71, 3.88, 2.64로 대략 $N$이고, 층마다 $1/I_\infty$ 항이 끌어내리는데 상한이 7.76인 출력층이 가장 많이 끌린다. $N=64$면 출력층은 6.92로 이미 상한의 89%다. 1층은 51.2로 더 천천히, 2층은 128로 더 천천히 다가가며, 2층은 $N=256$(85.3)과 $N=1{,}024$(113.8) 사이, 457.1에서 능선점을 넘는다.
- **launch를 나누어 갖기 전까지 시간은 거의 움직이지 않는다.** $N=1$에서 $N=256$까지 순전파는 15.17 µs에서 15.73 µs로, 일은 256배인데 4% 길어질 뿐이다. launch가 95–99%이기 때문이다. 커널 자신의 시간은 $N=6{,}037$에서 처음으로 launch의 15 µs와 같아지고, 흔히 쓰는 배치 4,096은 여전히 launch가 지배한다. 59.5%다.
- **환경당 비용은 약 4,500배 떨어진다.** $N=1$에서 $N=16{,}384$까지 15.17 µs에서 3.40 ns로다. 그때쯤 순전파는 73%가 커널 시간이고, $N$을 한 번 더 두 배로 하면 커널의 40.65 µs는 두 배가 되지만 순전파는 55.65에서 96.26 µs로 1.73배만 길어진다. launch의 15 µs는 그대로이기 때문이다.
- **이것이 GPU 시뮬레이터 안에서 정책이 치르는 값이다.** Rudin 외는 환경 스텝의 부분마다 로봇 수에 따라 시간을 쟀고, 시뮬레이션이 자라는 동안 정책의 추론은 액추에이터 신경망과 함께 거의 일정했다(그들의 부록 A.1). 이유는 적지 않았고, 그것을 이 표의 평평하고 launch가 지배하는 구간으로 읽는 것은 이 페이지의 해석이다(§5).

배치 뒤에 남는 것 — launch와, 상한에 묶인 얇은 층 — 을 CUDA 그래프(§7)와 융합(§8)이 공략한다.

### 5. 로봇 학습을 위한 병렬 시뮬레이션

*한 문장으로:* 벡터화 환경은 환경 수천 개를 GPU 위의 배열 한 묶음으로 두어, 물리, 보상, 리셋, 정책이 모두 배치 커널로 돌고 루프 안에서는 아무것도 CPU로 건너가지 않게 한다.

on-policy 강화학습, 예컨대 PPO([[02-foundations/rl-basics|7. RL 기초 §4]])는 두 국면을 오간다. 현재 정책으로 환경을 진행시켜 경험 한 배치를 모으고, 그 배치로 정책을 갱신한다. 모으기는 루프다. 관측하고, 행동하고, 물리를 진행시키고, 보상을 계산하고, 에피소드가 끝난 환경을 리셋한다([[02-foundations/rl-basics|7. RL 기초 §1]]). 이것을 갱신 한 번에 수천 번 돈다. 단계마다 어디서 도느냐가 루프의 값을 정한다.

**갈라진 파이프라인.** 시뮬레이터가 CPU에, 정책이 GPU에 있으면 스텝마다 관측이 호스트 링크를 타고 올라가고 행동이 내려온다. G-100에서 $N=4{,}096$이면 올라가는 데 20.97 µs, 내려오는 데 2.62 µs, 스텝당 23.59 µs이고, 전송마다의 오버헤드와 CPU가 무엇이든 시뮬레이션하는 시간은 그 전이다. launch가 겹칠 때 정책 자신의 순전파 17.54 µs(§7)와 비교된다. 그리고 내려받기가 동기화를 건다. 호스트는 정책의 행동이 올 때까지 물리를 진행시킬 수 없고, GPU는 호스트의 물리가 끝날 때까지 다음 순전파를 돌릴 수 없다. 한쪽이 일하는 동안 다른 쪽은 논다.

> **벡터화 환경의 정의.** **벡터화 환경**(vectorized environment)은 *과제의 사본 $N$개를 배치된 상태 하나로 담아 함께 진행시키는 시뮬레이터 인터페이스*다. 데이터와 커널의 조직 방식이고, 더 빠른 물리 방법도, 시뮬레이터 프로세스 $N$개도 아니다. 정의 조건 넷. 상태는 그것을 계산하는 장치 위에 **환경 축을 앞에 붙인 배열로 저장**된다. 스텝 호출 한 번이 같은 시간 간격으로 **$N$개 환경을 모두 진행**시키며, 배치 커널로 돈다. 환경은 **하나하나 끝나고 리셋된다**. 끝난 것은 번호로 리셋되고 나머지는 계속되므로, 어떤 환경도 다른 환경의 에피소드를 기다리지 않는다. 그리고 관측, 보상, 종료 표시는 **디바이스 위의 배치 배열로 돌려받아**, 호스트를 거치지 않고 정책에 넘어간다.
>
> $$D=N\,n_{\text{steps}},\qquad \text{초당 샘플}=\frac{N\,n_{\text{steps}}}{t_{\text{update}}}$$
>
> $D$는 정책 갱신 한 번이 배우는 배치, $n_{\text{steps}}$는 환경마다 갱신 한 번에 밟는 스텝 수, $t_{\text{update}}$는 모으고 배우는 한 주기의 벽시계 시간이다. 그러므로 처리량은 스텝의 시간이 $N$과 함께 자라지 않는 동안 $N$과 함께 자란다. §4의 스윕을 정책뿐 아니라 물리에 적용한 것이다.
>
> - **예**: Rudin 외의 최종 ANYmal 정책. 로봇 $N=4{,}096$대, 배치 $D=98{,}304$, 곧 갱신마다 로봇당 24스텝으로, RTX A6000 한 장에서 갱신 1,500번을 20분 안에 학습했다. 학습까지 넣어 초당 적어도 $98{,}304\times1{,}500/1{,}200\ \text{s}=122{,}880$ 샘플이다.
> - **비예**: 배치 인터페이스 뒤에 CPU 시뮬레이터 프로세스 $N$개를 두고, 관측을 쌓아 스텝마다 GPU로 복사하기. API는 벡터화되었지만 데이터는 아니고, 스텝마다 위의 왕복을 치른다.
> - **비예**: 하나라도 끝나면 $N$개 환경을 모두 리셋하기. 끝난 것이 다시 시작하지만 나머지도 다시 시작해, 모든 에피소드가 가장 짧은 것에 맞춰 잘린다.
> - **왜 중요한가**: 로봇 학습 논문의 숫자를 가능하게 하는 것이 이것이고, 이 조건들이 곧 자체 시뮬레이터가 쓸 가치가 있으려면 갖춰야 하는 것이다.

**증거.** Makoviychuk 외는 Isaac Gym을 이 원리로 만들었다. 물리 시뮬레이션과 정책 학습이 둘 다 GPU에 있고, 데이터는 물리 버퍼에서 PyTorch 텐서로 CPU를 거치지 않고 넘어간다. 그들은 CPU 시뮬레이터가 GPU 신경망을 먹이는 방식보다 학습이 2–3자릿수 빠르다고 보고한다. Rudin 외는 그것으로 ANYmal이 평지에서는 4분 안에, 거친 지형에서는 20분에 걷도록 학습시켰고, 앞선 연구는 12시간 이상이었다. 그들의 부록은 로봇 수가 늘 때 환경 스텝의 부분마다 시간을 잰다. 시뮬레이션이 가장 비싸고 로봇 수와 함께 천천히 자란다. 관측과 보상 계산이 둘째이고 역시 천천히 자란다. 정책의 추론과 액추에이터 신경망은 거의 일정한 시간이 걸린다. 학습 시간은 로봇 약 4,000대까지 거의 반비례해 줄었고, 그 뒤로는 시뮬레이터 처리량의 이득이 느려졌다. 그들의 주장은 샘플 효율이 아니라 GPU 한 장 위의 벽시계 시간이다. [[04-robotics/legged-locomotion|18. 보행 로코모션 §3]]도 그렇게 읽는다.

**리셋과 동기화, 흔한 병목.** 모든 것이 GPU에 오르고 나면 속도를 잃는 남은 길은 호스트에 있다. 종료 표시 위의 Python `if`, 로그를 위한 스텝마다의 `.item()`, CPU에서 하는 리셋, 스텝마다 찍는 통계 — 하나하나가 동기화다(§7). Isaac Lab의 direct 워크플로가 배치로 하는 대안을 보여 준다. `_get_dones()`는 종료와 시간 초과를 불리언 텐서 한 쌍으로 돌려주고, `_reset_idx(env_ids)`는 나열된 환경만 정확히 리셋하며 나머지는 계속 돈다. Rudin 외는 학습에서도 두 종류의 끝을 가른다. 시간 초과는 실패가 아니므로, 그 경우 critic의 목표값을 자기 예측으로 bootstrap한다.

**시뮬레이터들.** MJX는 MuJoCo를 JAX로 옮겨 XLA가 지원하는 어떤 가속기에서든 돌리고, 문서가 배치의 거래를 분명히 적는다. 장면 수천에서 수만 개를 병렬로 돌릴 때 가장 잘 돌고, 장면 하나는 CPU에 맞춰 다듬은 MuJoCo보다 약 열 배 느릴 수 있다. MJX-Warp는 NVIDIA GPU를 겨냥해 MJX-JAX의 접촉과 제약 주변 병목을 없애지만 자동 미분이 없다. MuJoCo Warp 자체는 Google DeepMind와 NVIDIA가 Newton의 일부로 관리하고, Isaac Lab도 Newton 위에서 돌 수 있다. 무엇을 쓸지와 버전의 함정은 [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터 §2]]에 있다.

**직접 쓰게 되는 때.** 위의 범용 시뮬레이터들은 흙을 모델링하지 않는다. 앞서가는 실시간 흙 모델도 입자 수준 기준과 대략 10–25%까지만 맞춰 검증되었고, 건설 재료를 문서화된 모델로 갖춘 시뮬레이터는 없다([[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터 §4–§5]]). 규모 있는 자체 흙 모델이나 변형체 모델이 필요한 학위논문은 GPU 커널을 스스로 쓰며, 방식은 둘이다. NVIDIA Warp에서는 환경 하나, 또는 입자 하나의 물리가 스레드마다 한 번 도는 Python 함수이고 첫 launch 때 CUDA로 컴파일된다(§6). JAX에서는 환경 하나의 스텝이 순수한 배열 함수이고, `jax.vmap`으로 환경 축을 따라 배치하고 `jax.jit`으로 컴파일한다. MJX의 방식이다. 어느 쪽이든 이 페이지의 규칙이 그대로 선다. 모든 환경 위에 커널 하나, 데이터는 디바이스에, 루프 안에 호스트 쪽 분기는 없다.

### 6. CUDA 커널 두 개를 한 줄씩 읽기

*한 문장으로:* 커널은 스레드마다 한 번 도는 평범해 보이는 코드이고, 커널을 읽는다는 것은 스레드의 번호가 데이터를 어떻게 고르는지, 전역 값 하나가 몇 번 적재되는지, 스레드가 어디서 서로를 기다려야 하는지를 찾는 일이다.

**벡터 덧셈.** 영어 절의 첫 코드가 가장 작은 완결 CUDA 프로그램이다. $n$개 float에 대해 $y=a+b$를 원소마다 스레드 하나로 계산한다. 줄마다 §1–§2의 한 조각이다. 전역 번호, 경계 검사, 호스트가 디바이스 메모리를 할당하고 복사하는 일, 꺾쇠, 그리고 커널 뒤에 줄을 서 있어서 호스트가 커널을 기다리는 자리이기도 한 동기식 `cudaMemcpy`(Programming Guide §2.1.3.2)다. 이웃한 스레드가 이웃한 float를 읽으므로 적재와 저장이 모두 병합된다. 강도는 12바이트에 1 FLOP, 0.083 FLOP/byte다. $n=2^{20}$이면 12.58 MB가 G-100의 $\beta$로 12.58 µs 걸리고, 산술은 $P$로 해도 0.01 µs다. $P$는 bf16 텐서 연산의 속도라서 일반 fp32 덧셈은 더 느리지만, 백 배 느려도 메모리 시간 아래에 머문다. 벡터 덧셈은 커널이 될 수 있는 만큼 메모리 한계이고, 그 속도는 $\beta$다.

**단순한 행렬곱.** 2층은 $C=AB$이고, $A$는 $4{,}096\times256$ activation, $B$는 $256\times256$ 행렬 $W_2^\top$이다. 커널은 $W_2$의 전치 사본을 행 단위로 저장해 두고 읽으므로 `B[k * N + col]`이 $W_2[\text{col},k]$이고 곱은 $AW_2^\top$이다. 영어 절의 둘째 코드인 직접 커널은 스레드마다 $C$의 원소 하나를 준다. 스레드는 곱셈-덧셈마다 $A$의 원소 하나와 $B$의 원소 하나, 모두 $2K$번 적재하므로 그리드 전체는 $2MNK$번 적재한다. $A$의 원소 하나는 $C$의 그 행에 있는 스레드 $N$개가 모두 적재하고, $B$의 원소 하나는 그 열의 스레드 $M$개가 모두 적재한다. 그 반복이 DRAM에 닿는지는 캐시에 맡겨진다.

**같은 곱을 타일로.** 영어 절의 셋째 코드에서 $T\times T$ 스레드 블록은 $C$의 $T\times T$ 타일 하나를 $K/T$ 단계로 계산한다. 단계마다 스레드들이 $A$의 $T\times T$ 타일 하나와 $B$의 타일 하나를 원소 하나씩 공유 메모리에 올린다. 두 적재 모두에서 `threadIdx.x`가 행을 따라 달리므로 적재는 병합된다. 그리고 장벽에서 기다렸다가, 각자 공유 메모리에서 곱셈-덧셈 $T$번을 한다. 이제 스레드는 단계마다 2번, 모두 $2K/T$번 적재한다. bf16이라면 배열은 `__nv_bfloat16`, 누산기는 float이고, 횟수는 같다.

> **공유 메모리 타일링의 정의.** **타일링**(tiling)은 *스레드 블록이 입력의 타일을 공유 메모리에 한 번 올리고, 블록의 모든 스레드가 거기서 그것을 재사용하도록 커널의 반복문을 재구성하는 것*이다. 피연산자를 어디서 읽느냐를 바꿀 뿐 무엇을 계산하느냐는 바꾸지 않는다. 정의 조건 넷. 블록은 타일마다 **함께, 병합된 적재로** 스레드당 원소 하나씩 올린다. 블록의 스레드는 정해진 순서 없이 돌기 때문에, **장벽**(`__syncthreads()`) 하나가 올리기와 쓰기를 가르고, 또 하나가 쓰기와 다음 덮어쓰기를 가른다. 올린 원소 하나는 그것이 필요한 스레드 $T$개가 공유 메모리에서 **$T$번 쓴다**. 그리고 결과는 타일로 나누어 더한 **같은 합**이다. 순서는 달라질 수 있고, 그것이 부동소수점 결과의 마지막 비트를 바꿀 수 있다.
>
> $$L_{\text{naive}}=2MNK,\qquad L_{\text{tiled}}=\frac{2MNK}{T}$$
>
> $L$은 $A\in\mathbb R^{M\times K}$, $B\in\mathbb R^{K\times N}$인 $C=AB$에서 전역 메모리로부터의 원소 적재 횟수, $T$는 타일 폭이다. 그러므로 전역 적재는 정확히 타일 폭만큼 줄어드는데, 올린 원소 하나가 이제 곱셈-덧셈 한 번이 아니라 $T$번을 섬기기 때문이다.
>
> - **예**: $N=4{,}096$의 2층. 단순하게는 536,870,912번, $T=16$이면 33,554,432번, $T=32$면 16,777,216번 적재한다. bf16으로 1.07 GB, 67.1 MB, 33.6 MB이고, 입력과 가중치를 한 번씩 읽는 2.23 MB의 481.9배, 30.1배, 15.1배다(§9).
> - **비예**: L1과 L2 캐시에 기대기. 단순 커널의 반복 적재 일부를 잡아 주지만 자동이고 보장이 없다. 타일링은 재사용을 명시적이고 한정된 것으로 만든다.
> - **비예**: 공유 메모리에 올리고 한 번만 읽는 타일. 공유 메모리를 거치는 것은 타일이 재사용될 때, 또는 병합되지 않는 전역 접근을 병합된 것으로 바꿀 때만 값을 한다. Programming Guide의 전치 예가 뒤의 경우다(§2.3.4.2.1).
> - **왜 중요한가**: 기울어진 지붕이 값을 매기는 것은 전역 메모리에 닿는 적재이므로, 타일링은 커널의 트래픽을 루프라인이 가정하는 피연산자당 한 번의 셈에 다가가게 하는 방법이다. FlashAttention은 같은 발상을 어텐션의 점수 표에 적용한 것이다([[03-deep-learning/foundations/attention-transformer|1.2 §7]]).

실습은 작은 경우에서 이 셈을 검산한다. $64\times64$와 $64\times32$의 곱을 $T=16$으로 하면 원소 16,384개를 적재하고, 단순하게는 262,144개이며, 결과는 정확히 $AB$다. 실전 라이브러리는 더 나아가 — 더 큰 타일, 레지스터, 텐서 코어 — 그래서 프레임워크의 행렬곱은 손으로 쓰는 일이 드물다. 그래도 그것을 읽을 때는 바로 이 질문들을 쓴다.

**NVIDIA Warp로 쓴 벡터 덧셈.** Warp는 커널을 Python 함수로 쓰고 첫 launch 때 CUDA C++로 컴파일해 그 결과를 캐시한다(Warp 문서, Runtime). 영어 절의 넷째 코드가 그것이고, CUDA의 어휘와 하나씩 대응한다. `@wp.kernel`은 `__global__`이고, Warp가 요구하는 타입 붙은 인자는 포인터이며, `wp.tid()`는 전역 번호이고, `dim=n`은 스레드 $n$개를 요청하며 블록은 Warp에 맡긴다. `wp.launch`는 꺾쇠이고, 그처럼 비동기다. `.numpy()`는 위의 `cudaMemcpy`처럼 GPU와 동기화하는 연산 가운데 하나다. Warp는 그것이 필요한 첫 호출에서 스스로 초기화하고, GPU가 있으면 기본 장치는 `cuda:0`이다. 1.12판부터는 주석을 `wp.array[float]`로도 쓸 수 있고, 호출 형식도 여전히 나란히 쓰인다.

**남의 커널 읽기**, 이 절이 써 온 점검 목록: 스레드 $i$는 어느 원소를 맡고, 경계 검사가 있는가. 이웃한 스레드는 어느 번호를 따라 움직이고, 그것이 메모리에서 연속된 번호인가(§2). 전역 값 하나를 몇 번 적재하는가(타일링). 장벽은 어디에 있고, 공유 메모리 읽기가 모두 장벽 뒤에 있는가. launch가 스레드를 몇 개 출발시키고, 그것은 워프로 몇 개어치 일인가(§1).

### 7. 최적화 전에 측정하기

*한 문장으로:* GPU는 CPU 뒤에서 돌기 때문에 GPU를 기다리지 않는 타이머는 launch만 재고, CPU에서 GPU의 결과가 필요한 줄은 GPU가 따라잡을 때까지 파이프라인을 멈춰 세운다.

launch는 커널이 돌기 전에 호스트로 돌아오고(Programming Guide §2.1.2.2), PyTorch의 연산도 같은 식으로 줄을 선다. GPU를 쓰는 호출은 일을 큐에 넣고, 일은 나중에 넣은 순서대로 실행되며, 프레임워크는 CPU와 GPU 사이에서 데이터를 복사할 때마다 스스로 동기화한다(PyTorch, CUDA semantics). 그래서 호스트는 앞서 달리며, GPU가 이전 것을 하는 동안 다음 launch를 내보낼 수 있다. 시계 둘, 호스트의 것과 디바이스의 것이 이를 그린다.

> **호스트–디바이스 동기화의 정의.** **동기화**(synchronization)는 *이미 큐에 넣은 일을 디바이스가 끝낼 때까지 호스트 스레드가 멈추는 지점*이다. 프로그램 시간선 위의 사건이고, 연산의 한 종류도 GPU 산술의 비용도 아니다. 정의 조건 셋. 일은 **비동기로 큐에 들어간다**. launch는 커널이 돌기 전에 돌아오고, 한 스트림의 커널은 내보낸 순서대로 돈다. 호스트가 **디바이스에서 무언가를 필요로 한다**. `.item()`, `.cpu()`, `print`, GPU 텐서 위의 Python `if`를 통해 CPU에 값이 필요하거나, `torch.cuda.synchronize()`나 `cudaDeviceSynchronize()`로 기다림을 명시적으로 요청한다. 그리고 호스트는 **기다린다**. 그래서 다음 launch는 디바이스가 비워진 뒤에야 나가고, 둘의 겹침이 사라진다.
>
> $$h\leftarrow h+t_L,\qquad g\leftarrow\max(h,g)+d_k,\qquad \text{동기화에서:}\ \ h\leftarrow\max(h,g)$$
>
> $h$는 호스트의 시계, $g$는 디바이스가 비는 시각, $t_L$은 launch 오버헤드, $d_k$는 커널 $k$ 자신의 시간이다. 그러므로 동기화가 없으면 둘이 겹친다. $t_L$보다 짧은 커널은 다음 launch 뒤에 숨고, 긴 커널은 다음 launch를 제 뒤에 숨긴다. 동기화는 두 시계를 강제로 맞춘다.
>
> - **예**: $N=4{,}096$의 MLP-256. 파이프라인으로 돌면 1층이 도는 동안 호스트가 2층의 launch를 내보내고, 순전파는 17.54 µs에 끝난다. 층마다 뒤에 `.item()`이 있으면 launch마다 앞 커널을 기다려, 순전파는 직렬 모델의 25.19 µs가 된다. 같은 산술에 44% 더 길다.
> - **비예**: 같은 비교를 $N=1$에서 하면 15.00 µs 대 15.17이다. 커널이 launch보다 짧아 겹침이 숨길 수 있는 것은 커널 자신의 0.17 µs뿐이니 동기화의 값은 거의 없다. 어느 쪽이든 launch가 비용의 전부다.
> - **비예**: 고정 메모리에서의 비동기 복사, 또는 CUDA 이벤트 기록. 둘 다 커널처럼 줄을 서고 호스트를 놓아 둔다. 나중에 그것을 기다릴 때만 막힌다.
> - **왜 중요한가**: 동기화 없이 잰 시간은 일이 아니라 줄 서기를 잰다. PyTorch의 문서도 그런 측정은 정확하지 않다고 적는다. 그리고 RL 루프의 스텝마다 흘러든 `.item()` 하나가 모든 스텝을 완전한 왕복으로 바꾼다.

**PyTorch에서 동기화를 거는 것.** PyTorch의 성능 조율 안내서가 흔한 범인을 나열한다. CUDA 텐서를 출력하기, `.item()`, `tensor.cuda()`나 `.cpu()`나 그와 같은 `.to(device)` 같은 메모리 복사, `.nonzero()`, 그리고 CUDA 연산의 결과에 따라 갈리는 Python 제어 흐름이다. `torch.cuda.set_sync_debug_mode("warn")`은 자기가 다루는 동기화 연산마다 경고한다. 실험적 기능이라 모든 동기화 연산이 걸리지는 않는다. `CUDA_LAUNCH_BLOCKING=1`은 모든 launch를 동기로 만드는데, 이것은 오류의 위치를 찾는 디버깅용이지 시간 재기용이 아니다.

**제대로 재기.** 시계를 읽기 전에 디바이스를 기다린다. 재기 전에 `torch.cuda.synchronize()`를 부르거나, 일 앞뒤로 CUDA 이벤트를 기록하고 동기화한 뒤 그 사이 시간을 읽는다(PyTorch, CUDA semantics; Best Practices §9.1). 먼저 예열 반복을 몇 번 돈다. 첫 호출이 CUDA 문맥을 만들고 코드를 컴파일할 수 있기 때문이다(Programming Guide §2.1.6). Warp는 커널마다 첫 launch 때 컴파일한다.

**launch를 한 번만 치르기.** CUDA 그래프는 커널의 연쇄를 한 번 기록해 두었다가 launch 한 번으로 다시 돌리므로, 커널마다의 준비를 매번이 아니라 그래프를 인스턴스화할 때 한 번 치른다(Programming Guide §4.2). PyTorch에서는 `torch.cuda.graph`가 구간을 붙잡고 `torch.cuda.make_graphed_callables`가 모듈을 감싼다. 재생은 eager 실행의 유연성을 내주고 CPU 오버헤드를 크게 줄이며, 붙잡은 구간은 shape을 바꾸거나 CPU와 동기화해서는 안 된다. 그 안의 `.item()`은 금지다(PyTorch, CUDA semantics). Warp는 `wp.ScopedCapture`로 기록한다. 실습의 모델에서 그래프 launch 한 번짜리 MLP-256은 $N=1$에서 15.17 대신 5.17 µs, $N=4{,}096$에서 25.19 대신 15.19 µs다.

**프로파일러가 보여 주는 것, 그리고 무엇을 열지.**

| 도구 | 답하는 질문 | 보여 주는 것 |
|---|---|---|
| CUDA 이벤트와 `torch.cuda.synchronize()` | GPU에서 이것이 얼마나 걸리나? | 기록한 두 지점 사이의 디바이스 경과 시간 |
| `torch.profiler` | 어느 연산자와 커널이 시간을 먹나? | 연산자마다 CPU 시간과 CUDA 시간(자기 몫과 전체), `record_shapes=True`일 때 입력 shape, 실행의 Chrome 추적 |
| `torch.cuda.set_sync_debug_mode` | 내 코드는 어디서 호스트를 기다리게 하나? | 다루는 동기화 연산마다 경고나 오류 |
| Nsight Systems (`nsys profile`) | 커널 사이의 틈은 어디 있고, 무엇 때문인가? | CPU 스레드, CUDA API 호출, 커널, 메모리 복사, 동기화의 시간선, 코드가 표시했다면 NVTX 구간까지 |
| Nsight Compute | 이 커널 하나는 왜 느린가? | 커널 하나를 깊이: 하드웨어 한계 대비 처리량과 루프라인 도표 위의 점 |

커널이 아니라 시간선에서 시작한다. 커널 사이에 틈이 벌어진 스텝은 launch나 호스트에 묶였고, 어떤 커널 최적화도 그것을 줄이지 못한다. 커널이 빈틈없이 이어지는 스텝은 커널에 묶였고, 그때 Nsight Compute의 루프라인이 커널마다 어느 지붕 아래인지 말해 준다. MLP-256이라면 $N=1$의 질문은 시간선이 답한다. 5 µs짜리 launch 사이에 1마이크로초에 한참 못 미치는 커널 셋이다.

영어 절의 마지막 코드는 MLP-256을 bf16으로 PyTorch에 올려, 예열한 뒤 CUDA 이벤트로 순전파 한 번의 시간을 재고, 동기화 디버그 모드를 켜고, 일부러 넣은 `.item()` 하나와 함께 한 스텝을 입력 shape까지 기록하며 프로파일해 CUDA 시간순 표와 Chrome 추적을 남긴다. 이렇게 eager로 돌리면 신경망이 이 페이지의 모델이 세는 것보다 많은 커널을 launch할 수 있다. eager 프레임워크는 ReLU마다 제 커널을 돌릴 수 있고 모델은 그것을 행렬곱에 접어 넣는데, 그 차이가 드러나는 곳이 프로파일러의 표다.

### 8. 로봇 위에서: Jetson, TensorRT, 제어 예산

*한 문장으로:* 로봇 위의 GPU는 제어 주기 안에서 관측을 하나씩 처리하므로, 큰 정책의 속도는 가중치당 바이트가, 작은 정책의 속도는 launch와 동기화가 정하고, TensorRT는 둘 다를 공략한다.

**로봇의 GPU.** Jetson 모듈은 Tegra 시스템 온 칩이다. CPU와 통합 GPU가 물리 DRAM 하나를 나누어 쓰고, 호스트 메모리, 디바이스 메모리, 통합 메모리가 모두 그 안에 할당된다(CUDA for Tegra §3). 건널 호스트 링크가 없으니 §2의 20.97 µs 올려 보내기는 로봇 위에 없다. 대신 CPU와 GPU가 같은 메모리를 끌어 쓰고, 그 대역폭은 Jetson Thor에서 273 GB/s다([[03-deep-learning/foundations/training-at-scale|1.3 §11]]). 그리고 로봇은 관측을 하나씩, $N=1$로 처리한다. §4 스윕의 왼쪽 끝이다.

**배치 1의 두 영역.** MLP-256은 순전파마다 170,128바이트, 273 GB/s로 0.62 µs가 필요하다. 시간은 launch와 동기화이고, 더 빠른 수 형식은 아무도 볼 수 없는 항을 반으로 줄일 뿐이다. 3B 정책은 bf16에서 토큰마다 6.0 GB, 같은 대역폭으로 22.0 ms가 필요하고, 거기서는 가중치당 바이트가 곧 시간이다. 1.3 §11의 표는 같은 모델에 fp8 11.0 ms, NVFP4 6.2 ms를 준다. 앞의 영역에는 더 적은 launch와 동기화가, 뒤의 영역에는 더 적은 바이트가 필요하고, 배포는 무엇이든 바꾸기 전에 자기가 어느 영역에 있는지 알아야 한다.

**TensorRT의 역할.** TensorRT는 NVIDIA의 추론 컴파일러이자 런타임이다. 빌드 단계에서 학습된 신경망을 받아, 패턴이 허락하는 곳마다 층을 융합하고 — 층 융합 카탈로그는 행렬곱 층을 그 뒤의 ReLU와 합친 예로 융합을 설명한다 — 층마다 후보를 시간 재어 대상 GPU에서 쓸 수 있는 가장 빠른 커널을 고르며, 층을 낮은 정밀도로 돌릴 수 있다. 이산 GPU용 현행 판인 11.3에서 INT8, INT4 가중치, FP8, FP4이고, [[03-deep-learning/foundations/training-at-scale|1.3 §11]]의 형식들이다. 결과는 직렬화된 *엔진*이고, 런타임이 그것을 불러 실행한다. 기본적으로 엔진은 그것을 만든 것과 같은 운영체제, CPU 구조, GPU 모델, TensorRT 버전에서만 동작이 보장된다. 커널을 고른 시간 재기가 그 GPU에서 돌았기 때문이다. Jetson에서는 그 묶임을 푸는 길이 없다. TensorRT 11.3.0은 JetPack을 지원하지 않으므로 Jetson 배포는 자기 JetPack이 지원하는 TensorRT 10.x 판에 머물고, 어떤 낮은 정밀도 형식을 쓸 수 있는지는 그 판의 문서가 말한다(11.3.0 릴리스 노트). GPU와의 묶임을 푸는 하드웨어 호환 선택지는 JetPack에서 지원되지 않고, 버전 호환은 이전 TensorRT로 만든 엔진을 이후 판에서 돌게 할 뿐이다(Engine Compatibility). 그래서 엔진은 로봇 위에서, 그 JetPack의 TensorRT 10.x로 만든다. 이 절의 두 영역이 모두 얻는다. 융합은 launch와 activation 트래픽을 없애고, 정밀도는 바이트를 없앤다.

> **커널 융합의 정의.** **커널 융합**(kernel fusion)은 *연산의 연쇄를 더 적은 커널로 바꾸는 변환*이다. 계산을 GPU 위에서 어떻게 스케줄하느냐를 바꿀 뿐 무엇을 계산하느냐는 바꾸지 않는다. 정의 조건 셋. 융합하는 연산은 **연속**이라, 각각이 앞의 것이 만든 것을 먹는다. 중간 결과는 DRAM에 썼다가 다시 읽는 대신 레지스터나 공유 메모리에 **칩 위에 남는다**. 그리고 연쇄는 연산마다 하나가 아니라 **launch 한 번**이 된다.
>
> $$t_{\text{fused}}=t_L+\max\Big(\frac{\sum_\ell F_\ell}{P},\ \frac{e\,(W+Nn_0+Nn_L)}{\beta}\Big)$$
>
> $W$는 가중치 수, $n_0$와 $n_L$은 신경망의 입력 폭과 출력 폭이고, 나머지 기호는 §3–§4의 것이다. 그러므로 층 사이의 activation이 바이트 셈에서 빠지고, launch가 층마다 하나에서 하나로 준다.
>
> - **예**: 이상적인 융합 커널 하나로 만든 MLP-256. $N=1$에서 15.17 대신 5.17 µs이고, $N=4{,}096$에서는 강도가 따로 도는 층들의 50.6, 124.1, 7.74에서 순전파 전체 907.8로 올라 계산 한계가 된다. 25.19 대신 11.88 µs, 파이프라인의 17.54보다도 짧다.
> - **비예**: CUDA 그래프. 커널마다의 launch 비용을 없애지만 — 순전파에 launch 한 번, 모델에서 $N=4{,}096$일 때 15.19 µs — 층마다 activation을 여전히 DRAM에 썼다가 다시 읽는다.
> - **비예**: 배치. 커널마다 강도를 올리고 층마다 launch 하나를 그대로 두며, §4의 상한을 올리지 못한다. 그 상한은 융합만이 없애는 activation 트래픽이 정한다.
> - **왜 중요한가**: TensorRT의 빌더가 빌드 때 하는 일이고 FlashAttention이 어텐션에 하는 일이며([[03-deep-learning/foundations/attention-transformer|1.2 §7]]), 작은 정책이 치르는 두 비용 모두에 작용하는 유일한 손잡이다.

**제어 속도 예산.** [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]은 로봇의 관측에서 행동까지의 지연을 단계의 합 — 샘플링, 노출, 전송, 추론, 디코딩, 구동 — 으로 세우는데, 예시 예산 70 ms 가운데 추론이 40 ms이고, 평균이 아니라 최악을 묻는다. 이 트랙의 두 정책을 그 추론 항에 넣어 보자. MLP-256의 launch 15 µs는 D4의 제어 주기 50 ms의 0.03%, 1 kHz 서보의 1밀리초의 1.5%다. 그 항을 정하는 것은 launch, 행동을 CPU로 가져오는 동기화, 그 둘레의 Python, 그리고 첫 호출의 준비이고, 그래서 작은 정책은 루프를 시작하기 전에 예열하고 가장 나쁜 틱으로 판단한다. 3B 정책은 bf16에서 가중치를 읽는 데만 토큰마다 22.0 ms를 치러 20 ms 영상 주기보다 길고, [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §11]]이 그렇게 계산한다. 거기서는 바이트가 속도를 정한다. 두 정책은 §4 스윕의 양 끝에 있다. 하나는 전부 launch이고, 다른 하나는 전부 바이트다.

### 9. 실습: 루프라인, 배치, 병합, 타일링

고정된 대상 위의 다섯 부분이다. 영어 절의 코드가 그것이다. 1부는 계산 절 — $N=1$과 $N=4{,}096$에서 층마다의 FLOP, 바이트, 강도, 한계 — 을 층마다의 상한과 능선점 넘는 배치와 함께 출력한다. 2부는 §4의 배치 스윕이고, 커널이 처음으로 launch만큼 걸리는 배치를 함께 찾는다. 3부는 주소에서 직접, 여러 간격과 원소 크기 둘에 대해 워프가 건드리는 32바이트 섹터를 센다. 4부는 행렬곱의 전역 적재를 단순과 타일로 세고, 작은 경우에서 타일 알고리즘을 실제로 돌려 셈과 곱을 검산한 뒤 2층에 적용한다. 5부는 §7의 호스트–디바이스 시간선을 돌리고, CUDA 그래프, 융합 커널, §5의 호스트 링크에 값을 매긴다. 어디에도 시간 측정은 없다. 모든 숫자가 모델의 것이라 어느 기계에서나 출력이 같다.

**계산 절과 상한**, 1부 — 계산 절의 두 표이고, 순전파 전체는 $N=1$에서 15.1701 µs(환경당 15,170.13 ns), $N=4{,}096$에서 25.1897 µs(환경당 6.15 ns)다.

| 층 | 상한 $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$ | G-100 능선점을 넘는 배치 |
|---|---:|---|
| $64\to256$ | 51.20 | 넘지 않음 |
| $256\to256$ | 128.00 | $N=457.1$ |
| $256\to8$ | 7.76 | 넘지 않음 |

**스윕**, 2부는 §4의 표이고, 커널 셋은 $N=6{,}037$에서 launch 셋만큼 걸린다.

**워프당 섹터**, 3부:

| 간격 (원소) | fp32: 섹터 | 128바이트를 쓰려고 옮긴 바이트 | 효율 | bf16: 섹터 | 64바이트를 쓰려고 옮긴 바이트 | 효율 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 128 | 100.00% | 2 | 64 | 100.00% |
| 2 | 8 | 256 | 50.00% | 4 | 128 | 50.00% |
| 4 | 16 | 512 | 25.00% | 8 | 256 | 25.00% |
| 8 | 32 | 1,024 | 12.50% | 16 | 512 | 12.50% |
| 16 | 32 | 1,024 | 12.50% | 32 | 1,024 | 6.25% |
| 256 | 32 | 1,024 | 12.50% | 32 | 1,024 | 6.25% |

그리고 섹터 경계에서 4바이트 지나 시작하는 간격 1의 fp32는 섹터 5개를 건드린다.

**전역 적재**, 4부: 작은 경우는 공식대로 16,384번을 세고 단순하게는 262,144번이며, 곱은 정확하다. $N=4{,}096$의 2층은:

| 타일 폭 $T$ | 전역 적재 | 바이트 (bf16) | 입력과 가중치를 한 번씩 읽기(2,228,224바이트) 대비 |
|---:|---:|---:|---:|
| 1 (단순) | 536,870,912 | 1,073,741,824 | 481.9× |
| 16 | 33,554,432 | 67,108,864 | 30.1× |
| 32 | 16,777,216 | 33,554,432 | 15.1× |

**호스트 시간선**, 5부:

| $N$ | 파이프라인 (µs) | 층마다 동기화 (µs) | 그래프 launch 한 번 (µs) | 융합 커널 (µs) | 융합 강도 |
|---:|---:|---:|---:|---:|---:|
| 1 | 15.0046 | 15.1701 | 5.1701 | 5.1681 | 1.0 |
| 4,096 | 17.5355 | 25.1897 | 15.1897 | 11.8787 | 907.8 |

그리고 $N=4{,}096$에서 CPU 시뮬레이터의 호스트 링크 복사는 올라가는 데 20.97 µs, 내려오는 데 2.62 µs, 오버헤드 전에 스텝당 23.59 µs다.

**표 읽기.** 강의가 예측했고 숫자가 이제 보여 주는 것 다섯.

- **배치 1은 메모리가 아니라 launch에 묶인다.** 루프라인은 $N=1$의 세 층을 모두 메모리 한계라 부르고 그것은 옳지만, 그 메모리 시간은 0.17 µs이고 launch는 15 µs다. 대역폭이 두 배인 GPU는 순전파를 0.56%, 15.17에서 15.09 µs로 빠르게 할 뿐이다(과제 1).
- **배치는 큰 층을 능선점 너머로 옮기고 얇은 층은 남겨 둔다.** 2층은 457.1에서 넘고, 1층과 3층은 51.2와 7.76에 묶여 어떤 배치에서도 G-100의 능선점 아래다. 스윕의 강도는 16,384에서 51.04와 7.75로 기어간다.
- **간격은 트래픽을 계단식으로 곱한다.** fp32는 32바이트 간격에서, bf16은 원소 16개 — 역시 32바이트 — 에서 최악에 닿는다. 단위를 정하는 것은 원소가 아니라 섹터다. bf16 $W_2$의 열 하나는 64바이트에 1,024바이트를 치른다.
- **타일링은 적재를 타일 폭으로 나눌 뿐 다른 것은 하지 않는다.** $T=1$, 16, 32에서 한 번씩 읽기의 481.9, 30.1, 15.1배로, 비가 정확히 $1/T$로 준다.
- **겹침, 그래프, 융합은 서로 다른 비용을 공략한다.** 파이프라인은 두 시계를 겹친다. launch보다 짧은 커널은 다음 launch 뒤에 숨고, 긴 커널은 다음 launch를 숨긴다(4,096에서 25.19 대 17.54 µs, $N=1$에서는 커널 자신의 0.17 µs뿐이라 15.17 대 15.00). 그래프는 launch를 없애지만 activation 트래픽은 못 없애고(15.19), 융합은 둘 다 없앤다(11.88). $N=1$에서 그래프와 융합 커널이 5.17 µs로 같은 것은, 거기서는 launch 한 번만 남기 때문이다.

### 읽고 나면

- [ ] 커널, 스레드, 블록, 그리드, 워프가 무엇인지 말하고, launch 줄과 전역 번호를 쓰고, 어떤 블록도 다른 블록을 기다리면 안 되는 이유를 말한다.
- [ ] 지연 숨기기를 Little의 법칙으로 설명하고, 배치 1 층이 지연에 묶이는 이유를 말한다.
- [ ] 어떤 간격과 원소 크기에서든 워프가 건드리는 32바이트 섹터와 효율을 센다.
- [ ] 어떤 배치에서든 층의 FLOP, 바이트, 강도를 계산해 루프라인에 올리고, 어느 지붕이 그것을 묶는지 말한다.
- [ ] $1/I=(e/2)(1/N+1/I_\infty)$를 유도하고, 층의 상한과 능선점을 넘는 배치를 찾는다.
- [ ] launch까지 넣어 순전파에 값을 매기고, 어느 배치에서 launch가 지배를 멈추는지 말한다.
- [ ] 벡터화 환경이 GPU에 무엇을 두는지, CPU 시뮬레이터가 왜 스텝마다 왕복을 치르는지, Rudin 외가 실제로 무엇을 쟀는지 말한다.
- [ ] CUDA나 Warp 커널을 읽는다. 번호, 경계 검사, 병합, 공유 메모리와 장벽을 짚고, 적재를 단순과 타일로 센다.
- [ ] GPU 코드의 시간을 제대로 재고, PyTorch에서 동기화를 거는 것을 대고, 성능 질문에 맞는 도구를 고른다.
- [ ] TensorRT의 빌드 단계가 하는 일, 엔진이 GPU 하나에 속하는 이유, 그리고 CUDA 그래프는 못 하고 융합은 없애는 비용을 말한다.

### 스스로 점검

1. GPU는 스레드 하나를 CPU 코어보다 훨씬 느리게 돌린다. 그런데 $N=4{,}096$의 MLP-256에서는 왜 더 빠르고, 그 논리는 $N=1$에서 왜 무너지는가?
2. 워프가 $W_2$의 한 행을 따라 연속된 bf16 가중치 32개를 읽고, 다음에는 한 열을 따라 32개를 읽는다. 접근마다 32바이트 섹터가 몇 개 필요하고, 옮긴 바이트 중 얼마를 쓰는가?
3. MLP-256의 3층($256\to8$)은 모든 배치에서 메모리 한계다. 왜 그런가, 그리고 무엇이 그것을 바꾸겠는가?
4. 계산 절은 $N=1$의 MLP-256을 15.17 µs로 매기고 그 가운데 0.17 µs가 메모리 트래픽이다. 나머지 15 µs는 어디로 가며, 그 대부분을 없애는 두 방법은 무엇인가?
5. 학습 루프가 스텝마다 `loss.item()`을 로그로 남긴다. 그 한 줄의 값은 무엇이고, 언제 문제가 되는가?
6. 정책의 순전파 시간이 환경 1개에서나 1,024개에서나 같다. 그것은 무엇을 말해 주고, 이 페이지의 모델은 16,384개에서 무엇을 예측하는가?
7. MJX는 장면 하나에서 MuJoCo보다 열 배 느릴 수 있는데도 논문들은 그것으로 보행 정책을 학습시킨다. 왜 모순이 아닌가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 속도가 아니라 처리량 덕분이다. $N=4{,}096$의 2층에는 독립적인 내적이 1,048,576개, 워프로 32,768개 있어서, 몇몇 워프가 메모리를 기다리는 동안 다른 워프가 계산하고 순전파는 27.3 TFLOP/s로 돈다. $N=1$에서는 출력이 256개, 워프 8개이고 옮길 것은 132,096바이트 — 지연이 0.13 µs보다 길기만 하면 지연 한 번어치에도 못 미친다 — 라서 넘어갈 다른 일이 없고, 그나마 있는 일도 5 µs짜리 launch 셋 뒤에 앉아 있다.
> 2. 행을 따르면 간격이 1이라 64바이트가 섹터 $\lceil64/32\rceil=2$개를 채우고 모두 쓰인다. 열을 따르면 간격이 원소 256개, 512바이트라서 스레드마다 제 섹터를 갖는다. 섹터 32개, 64바이트를 쓰려고 1,024바이트를 옮기니 6.25%다.
> 3. 강도의 상한이 $256\cdot8/(256+8)=7.76$ FLOP/byte이기 때문이다. 환경 하나마다 4,096 FLOP을 하려고 activation 528바이트를 옮기는데, 배치가 나누어 주는 것은 가중치뿐이다. 어떤 배치도 G-100의 능선점 100에 닿지 못한다. 앞 층과 융합해 입력 256개가 DRAM에 가지 않게 하면 그 바이트 대부분이 사라지고, 출력이 넓어지면 상한이 오른다.
> 4. 5 µs짜리 커널 launch 세 번으로 간다. 신경망을 커널 하나로 융합하면 launch가 하나 남아 모두 5.17 µs이고, 커널 셋을 CUDA 그래프로 붙잡아 다시 돌려도 launch 한 번, 5.17 µs다. (파이프라인은 거의 돕지 못한다. launch 뒤에 숨길 수 있는 것은 커널 자신의 0.17 µs뿐이라 15.00 대 15.17 µs다.)
> 5. 스텝마다 동기화 한 번이다. 호스트는 손실을 읽기 전에 큐에 든 GPU 일을 모두 기다리므로, 다음 스텝의 launch는 GPU가 비워진 뒤에야 시작하고 호스트와 디바이스의 겹침이 사라진다. 스텝의 커널이 그동안 호스트가 내보낼 수 있었을 launch에 비해 짧을 때 — 로봇 정책의 작은 신경망, launch에 묶인 영역 — 문제가 되고, 커널 하나하나가 길면 거의 문제가 안 된다. 백 스텝마다 로그를 남기거나 GPU에 쌓아 두면 피한다.
> 6. 시간이 launch에 묶였다는 것이다. 커널이 launch보다 훨씬 짧아 배치가 거의 공짜다. §4의 스윕에서 환경 1개에서 1,024개로 가도 15.17에서 17.58 µs다. 평평한 구간은 커널이 launch만큼 걸리는 곳, G-100 위 MLP-256에서는 $N=6{,}037$에서 끝나고, 16,384에서 모델은 55.65 µs, $N=1$ 값의 3.67배를 예측한다. 순전파가 커널에 묶이기 때문이다.
> 7. 같은 배치의 거래를 물리에 적용한 것이다. 장면 하나는 GPU를 채우지 못하고 고정 비용을 환경 하나가 다 치르지만, 장면 수천 개는 그것을 나누어 갖는다. MJX의 문서 자체가 장면 수천에서 수만 개를 병렬로 돌릴 때 가장 잘 돈다고 적는다. 논문이 보고하는 것은 배치 전체의 처리량이고, 거기서 이긴다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[03-deep-learning/lab-objects|0. Lab Objects]]만 쓴다. 대상은 MLP-256과 G-100이고, 모든 문제가 손잡이 하나를 바꾸므로 — 대역폭, 정렬, 층의 폭, 타일, 원소 크기, 재는 코드 — 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 위의 그림을, 대역폭을 $\beta=2{,}000$ GB/s로 두 배 한 G-100 변형($P$와 $t_L$은 그대로)에서 $N=1$과 $N=1{,}024$의 MLP-256에 대해 다시 그린다. 두 지붕과 새 능선점을 가진 루프라인, 두 배치에서 강도를 적은 세 층, 같은 척도의 시간 막대 둘이다. 새 능선점의 어느 쪽에 어느 층이 있는지, 두 배가 된 대역폭이 $N=1$ 막대에 무엇을 했는지 말하라.
2. **유도.** (a) 숫자당 $e$바이트인 dense 층이 $1/I=(e/2)\big(1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})\big)$임을 보여라. MLP-256 1층의 상한을 구하고 어떤 배치도 G-100에서 그것을 계산 한계로 만들지 못하는 이유를 말한 뒤, bf16의 $512\times512$ 층이 G-100의 능선점을 넘는 배치를 구하라. (b) 워프가 섹터 경계에서 16바이트 지난 곳에서 시작해 연속된 bf16 값 32개를 읽는다. 섹터 몇 개, 효율은 얼마인가? 워프가 $256\times64$로 행 단위 저장한 $W_1$의 열 하나를 읽는다. 섹터 몇 개, 효율은 얼마이고, 이 읽기가 병합되려면 $W_1$을 어떻게 저장하겠는가? (c) $N=4{,}096$의 1층을 행렬곱으로 보고 전역 적재를 단순, $T=16$, $T=32$로 원소와 bf16 바이트로 세어, 입력과 가중치를 한 번씩 읽는 바이트와 비교하라. (d) 큰 $N$에서 환경 하나를 더할 때 루프라인 시간이 느는 양으로부터, G-100 위 MLP-256의 커널 셋이 launch 셋만큼 걸리는 배치를 손으로 어림하고 §9와 대조하라.
3. **실행.** 영어 절 템플릿의 `?`를 채운 뒤, 은닉층 둘을 512로 넓힌 MLP-512를 G-100에서 $N\in\{1,16,256,4096\}$으로 돌린다. (a) 층마다의 강도와 한계, 루프라인 시간과 직렬 시간, 환경당 비용, 은닉층이 능선점을 넘는 배치, (b) fp64(8바이트) 값을 간격 1, 2, 4, 8로 읽는 워프의 섹터와 효율, (c) $N=4{,}096$에서 은닉층의 전역 적재를 단순과 $T=16$, 32로, (d) $N=4{,}096$의 파이프라인 시간과 동기화 시간을 보고하라. 각각을 MLP-256과 비교하라.
4. **해석.** 어떤 연구실이 세 층짜리 MLP 정책이 로봇의 Jetson에서 "0.04 ms에 돈다"고 보고한다. `act = policy(obs)` 둘레를 Python의 `time.perf_counter()`로 잰 값이다. 그 뒤 `act.cpu()`를 부르고 명령을 보내는 1 kHz 제어 루프는 1 ms 마감을 몇몇 틱에서, 그리고 첫 틱에서는 늘 놓친다. §4, §7, §8을 써서 0.04 ms가 무엇을 쟀는지, 틱 하나의 실제 비용에 무엇이 들어 있는지, 첫 틱이 왜 느린지, 대신 무엇을 어떤 도구로 재겠는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - 두 축을 모두 로그로 하고 가로에 FLOP/byte, 세로에 FLOP/s를 둔다. 두 지붕에 숫자 — 기울기 $\beta$와 높이 $P$ — 를, 능선점에 $P/\beta$를 적는다. $\beta$가 두 배면 기울어진 지붕이 올라가고 능선점이 왼쪽으로 가지만 점은 옆으로 움직이지 않는다. 강도는 GPU가 아니라 커널의 것이다.
> - 층마다 $(I,\ \min(P, I\beta))$에, 지붕 아래가 아니라 지붕 위에 점을 찍는다. 모델의 점은 상한이다.
> - 강도는 activation을 바이트에 넣어 계산한다. $I=N$에 찍은 점은 그것을 잊은 것이고, 배치만 크면 출력층을 어떤 능선점 너머로도 보낸다.
> - 층마다 상한 $n_{\text{in}}n_{\text{out}}/(n_{\text{in}}+n_{\text{out}})$를 표시한다. 상한이 능선점 왼쪽인 층은 배치가 얼마든 평평한 지붕에 닿지 못한다.
> - 시간 막대는 같은 척도로, launch를 제 커널 앞의 따로 된 토막으로 그리고, 메모리 한계 커널과 계산 한계 커널을 다르게 칠한다. 작은 배치에서 막대는 거의 전부 launch이고, $\beta$를 두 배 해도 거의 그대로다.
> - 세 층을 점 셋, 토막 셋으로 둔다. 평균 강도에 찍은 신경망 전체의 점 하나는 계산 한계인 층 하나를 숨긴다.

> [!tip]- 정답 · Solutions
> 1. 새 능선점은 $10^{14}/(2\times10^{12})=50$ FLOP/byte다. $N=1$에서 강도는 0.981, 0.992, 0.886 그대로이고 모두 메모리 한계이지만, 점은 저마다 두 배 높이인 1.96, 1.98, 1.77 TFLOP/s에 있다. 메모리 시간은 0.0167, 0.0660, 0.0023 µs로 반이 되어 막대는 15.170 대신 $15+0.0851=15.085$ µs, launch가 99.4%로 아무도 볼 수 없는 변화다. $N=1{,}024$에서 1층은 48.76 FLOP/byte로 새 능선점 바로 아래, 메모리 한계 0.3441 µs다(계산 시간 0.3355 µs와 3% 안). 2층은 113.78로 G-100에서 이미 그랬듯 계산 한계 1.3422 µs이고, 3층은 7.70으로 메모리 한계 0.2724 µs다. 막대는 $15+1.9586=16.959$ µs, 환경당 16.56 ns, launch 88.5%로 G-100의 17.575 µs와 비교된다. 두 배 대역폭이 아낀 것은 0.62 µs이고, 메모리 한계 커널만 줄었기 때문이다.
> 2. (a) $F=2Nn_{\text{in}}n_{\text{out}}$, $B=e(n_{\text{in}}n_{\text{out}}+Nn_{\text{in}}+Nn_{\text{out}})$이므로 $1/I=B/F=(e/2)\big(1/N+(n_{\text{in}}+n_{\text{out}})/(n_{\text{in}}n_{\text{out}})\big)$이다. 1층의 상한은 $64\cdot256/320=51.2$다. 환경 하나마다 32,768 FLOP을 하고 activation 640바이트를 옮기는데, 어떤 배치도 이 비를 바꾸지 못하고 그 비는 100 아래다. $512\times512$ 층은 상한 256이므로 $1/100=1/N+1/256$에서 $N=164.1$이다. (b) 바이트가 16에서 79까지라 섹터 0, 1, 2, 곧 섹터 3개이고 64바이트를 쓰려고 96바이트를 옮기니 66.7%다. $W_1$의 열은 간격이 원소 64개, 128바이트라 섹터 32개, 64바이트에 1,024바이트, 6.25%다. $W_1$을 전치해 $64\times256$으로 행 단위 저장하면 그 열이 행이 되어 섹터 2개, 100%다. (c) $M=4{,}096$, $N=256$, $K=64$. 단순 $2MNK=134{,}217{,}728$번, 268,435,456바이트. $T=16$은 8,388,608번, 16,777,216바이트. $T=32$는 4,194,304번, 8,388,608바이트. 입력과 가중치를 한 번씩 읽으면 $2(4{,}096\cdot64+64\cdot256)=557{,}056$바이트이므로 비는 481.9, 30.1, 15.1이다. $2MN/(M+N)$에는 $K$가 없으니 2층의 비와 같다. (d) 큰 $N$에서 환경 하나가 1층에 640바이트(0.640 ns), 계산 한계인 2층에 131,072 FLOP(1.311 ns), 3층에 528바이트(0.528 ns)를 더해 환경당 2.479 ns이고, 1층과 3층의 가중치로 0.037 µs가 얹힌다. 커널은 $N\approx(15-0.037)/0.002479=6{,}036$에서 15 µs에 닿고, §9는 6,037을 출력한다.
> 3. 빈칸은 `2 * N * n_in * n_out`, `e * (n_in * n_out + N * n_in + N * n_out)`, `max(F / P, B / BETA)`, `len(LAYERS) * T_L`, `512 * 512 / (512 + 512)`, `1 / (1 / (P / BETA) - 1 / cap)`, `100 * 32 * 8 / (32 * S)`, `2 * M * N * K // T`, `max(h, g) + d`, `max(h, g)`이다. 출력은 영어 절의 정답 3과 같고, 요약하면:
>
>    | $N$ | 1층 $I$ | 은닉층 $I$ | 3층 $I$ | 루프라인 시간 (µs) | 직렬 시간 (µs) | 환경당 (µs) |
>    |---:|---:|---:|---:|---:|---:|---:|
>    | 1 | 0.98 (메모리) | 1.00 (메모리) | 0.89 (메모리) | 0.602 | 15.602 | 15.6023 |
>    | 16 | 12.49 (메모리) | 15.06 (메모리) | 5.28 (메모리) | 0.666 | 15.666 | 0.9791 |
>    | 256 | 46.55 (메모리) | 128.00 (계산) | 7.64 (메모리) | 1.977 | 16.977 | 0.0663 |
>    | 4,096 | 56.11 (메모리) | 240.94 (계산) | 7.86 (메모리) | 30.527 | 45.527 | 0.0111 |
>
>    은닉층의 상한은 256.0이고 능선점은 $N=164.1$에서 넘는다. fp64 워프는 간격 1, 2, 4, 8에서 섹터 8, 16, 32, 32개, 효율 100.0, 50.0, 25.0, 25.0%다. 은닉층의 적재는 단순 2,147,483,648번, $T=16$이면 134,217,728번, $T=32$면 67,108,864번이다. $N=4{,}096$에서 파이프라인 35.743 µs, 층마다 동기화 45.527 µs다. (a) 은닉 가중치가 네 배라 $N=1$ 순전파의 메모리가 0.17 대신 0.60 µs이지만 여전히 96%가 launch, 15.60 µs다. 은닉층의 상한이 256으로 두 배가 되어 457.1 대신 164.1에서 능선점을 넘고, 256에서 이미 계산 한계다. 입력층과 출력층은 56.9와 7.88에 묶여 메모리 한계로 남는다. 4,096에서 순전파는 45.53 µs, 환경당 11.1 ns로 MLP-256의 6.15와 비교되고, 은닉층 하나가 계산으로만 21.47 µs다. (b) fp64 워프는 간격 1에서 256바이트, 섹터 8개를 옮기고, 이미 간격 4 — 32바이트 — 에서 최악인 섹터 32개에 닿는다. 스레드마다 섹터 32바이트 중 8바이트를 쓰므로 효율은 12.5%가 아니라 25%에서 바닥이다. (c) $N$과 $K$가 모두 두 배라 $2MNK$가 2층의 네 배, 단순하게는 약 21억 5천만 번이고 타일이면 16이나 32로 나뉜다. (d) 파이프라인 35.74 µs 대 45.53이다. 겹침이 9.8 µs를 아껴 MLP-256의 7.7보다 많은데, 첫 커널이 더 길어서(2.65 대신 4.78 µs) 둘째 launch 뒤에 숨기 때문이다. 두 신경망 모두 launch보다 오래 도는 커널은 은닉층 하나뿐이고, 그것이 셋째 launch를 통째로 숨긴다.
> 4. 비동기 호출 둘레의 `perf_counter()`는 호스트 쪽만 잰다. 커널을 큐에 넣는 Python과 launch인데, 이것은 커널이 돌기 전에 돌아온다. 틱의 실제 비용은 그 launch, 그리고 커널, 그리고 `act.cpu()`의 동기화 — 호스트가 마지막 커널을 기다린다 — 그리고 호스트 버퍼로의 복사(Jetson에서는 공유 DRAM 안에서 일어나 PCIe를 건너지 않지만 여전히 기다린다), 그리고 인식 신경망처럼 GPU를 나누어 쓰는 다른 무엇이다. 가끔의 마감 놓침도 거기서 온다. 첫 틱은 CUDA 문맥을 만들고 첫 호출에서 컴파일되는 코드의 값까지 치른다(Programming Guide §2.1.6). 관측에서 명령까지 틱 전체를 긴 실행의 모든 틱에서 재고, 1 ms 마감에 대해 최댓값과 높은 백분위수를 보고한다. [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]이 요구하는 대로다. 시간은 동기화한 시계나 CUDA 이벤트로 재고, 호출 둘레의 맨 타이머로는 절대 재지 않는다. Nsight Systems의 시간선이 틈이 어디 있고 무엇이 함께 도는지 보여 주고, `torch.cuda.set_sync_debug_mode("warn")`이 숨은 동기화를 찾는다. 그런 다음 보이는 대로 손을 쓴다. 루프 전에 예열한다. 신경망을 CUDA 그래프로 붙잡아 틱을 launch 한 번으로 만든다. TensorRT 엔진은 패턴이 허락하는 만큼 융합하지만 여전히 커널 여럿을 돌릴 수 있으므로, TensorRT의 성능 안내서가 적듯 그 enqueue를 CUDA 그래프로 붙잡아야 launch 한 번이 된다. 그리고 틱마다 동기화를 정확히 하나 — 명령을 가져오는 것 — 만 둔다.

### 출처

- NVIDIA. *CUDA Programming Guide*, v13.4 ([docs.nvidia.com/cuda/cuda-programming-guide](https://docs.nvidia.com/cuda/cuda-programming-guide/index.html)) — §1.1.2(GPU가 스레드 하나의 속도를 처리량과 바꾸는 이유), §1.2.2.1–§1.2.2.2(스레드 블록과 그리드, 블록의 임의 순서; 워프와 SIMT, 분기 시 가림), §1.2.3(호스트와 디바이스 메모리, 캐시), §2.1.2(커널, 세 겹 꺾쇠 launch, 블록당 최대 1,024 스레드, 번호 내장 변수, 경계 검사, 비동기 launch), §2.1.3.2(`cudaMalloc`, 동기식 `cudaMemcpy`), §2.1.6(런타임 초기화), §2.3.3(메모리 공간: 전역, 공유, 레지스터, 로컬, 캐시), §2.3.4.1(병합 접근: 32바이트 트랜잭션 넷으로 100%, 32바이트 이상 간격에서 12.5%), §2.3.4.2.1(공유 메모리를 거친 전치), §2.3.7(occupancy), §3.2.2.2(하드웨어 멀티스레딩: 칩 위의 워프 문맥, 준비된 워프에서 내보내는 스케줄러), §4.2(CUDA 그래프와 커널마다의 launch 비용).
- NVIDIA. *CUDA C++ Best Practices Guide*, v13.4 ([docs.nvidia.com/cuda/cuda-c-best-practices-guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)) — §9.1(이벤트와 동기화로 시간 재기), §10.1(호스트–디바이스 전송: 898 GB/s 대 16 GB/s, 데이터를 디바이스에 두기, 작은 전송 묶기), §10.1.1–§10.1.2(고정 메모리, 비동기 전송), §10.2.1(compute capability 6.0 이상의 병합; §10.2.1.1 단순 접근 패턴, 건드린 섹터 안에서 접근 순서를 뒤섞어도 값이 같음; §10.2.1.2 어긋난 시작과 섹터 5개; §10.2.1.4 간격 있는 접근, 간격 2에서 50%), §10.2.3과 §10.2.3.2(공유 메모리와 행렬곱에서의 사용).
- NVIDIA. *CUDA for Tegra*, application note 13.4 ([docs.nvidia.com/cuda/cuda-for-tegra-appnote](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html)) — §3, CPU와 통합 GPU가 SoC DRAM 하나를 나누어 씀.
- NVIDIA. *Warp* 문서, 1.17 ([nvidia.github.io/warp](https://nvidia.github.io/warp/stable/)) — User Guide의 Basics(타입 붙은 인자의 커널, `wp.tid`, 배열, `wp.launch`, 동기화하는 `.numpy()`)와 Runtime(비동기 launch, 기본 장치, 컴파일 모델과 캐시, `wp.ScopedCapture`로 그래프 붙잡기), 그리고 Warp 변경 기록 1.12.0(대안으로서의 첨자형 배열 주석).
- PyTorch 2.14 문서 ([docs.pytorch.org](https://docs.pytorch.org/docs/stable/notes/cuda.html)) — "CUDA semantics" 노트(비동기 실행, CPU–GPU 복사 시 자동 동기화, `torch.cuda.Event`로 시간 재기, 고정 메모리, CUDA 그래프와 그 제약), `torch.profiler` 참조와 profiler recipe, `torch.cuda.set_sync_debug_mode`, 그리고 S. Migacz, "Performance Tuning Guide", PyTorch 튜토리얼, 2025-07-09 갱신(동기화를 거는 연산).
- NVIDIA. *Nsight Systems User Guide*, 2026.5 ([docs.nvidia.com/nsight-systems](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)) — `nsys profile`, CUDA와 NVTX 추적, 시간선. *Nsight Compute Profiling Guide*, 2026.3 ([docs.nvidia.com/nsight-compute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)) — 커널 수준 프로파일링과 루프라인 도표(산술 강도, 능선점).
- NVIDIA. *TensorRT* 문서, 11.3 ([docs.nvidia.com/deeplearning/tensorrt](https://docs.nvidia.com/deeplearning/tensorrt/latest/architecture/how-trt-works.html)) — "How TensorRT Works"(빌드와 런타임 단계, 시간 재기로 고르는 커널, 엔진 호환성), "Layer Fusion Catalog", "Working with Quantized Types"(INT8, INT4 가중치, FP8, FP4), "Engine Compatibility"(JetPack과 DriveOS에서 하드웨어 호환 미지원, 버전 호환), "Optimizing TensorRT Performance"(CUDA 그래프로 추론: `enqueueV3()` 호출을 붙잡아 다시 돌림), 그리고 TensorRT 11.3.0 릴리스 노트(JetPack 미지원, Jetson 배포는 TensorRT 10.x에 머묾).
- Williams, S., Waterman, A. & Patterson, D. "Roofline: An insightful visual performance model for multicore architectures." *Communications of the ACM* 52(4):65–76, 2009 — 모델, DRAM 트래픽에 대한 operational intensity, 능선점. NERSC, "Roofline Performance Model" ([docs.nersc.gov](https://docs.nersc.gov/tools/performance/roofline/)) — machine balance로서의 능선점.
- Little, J. D. C. "A proof for the queuing formula: $L=\lambda W$." *Operations Research* 9(3):383–387, 1961.
- Rudin, N., Hoeller, D., Reist, P. & Hutter, M. "Learning to walk in minutes using massively parallel deep reinforcement learning." *Proceedings of the 5th Conference on Robot Learning*, PMLR 164:91–100, 2022 ([arXiv:2109.11978](https://arxiv.org/abs/2109.11978)) — 초록(4분과 20분), §2(GPU 위의 데이터 수집과 갱신), §2.2.1($B=n_{\text{robots}}n_{\text{steps}}$), §2.2.2(시간 초과와 bootstrap), §4.1(로봇 약 4,000대까지의 규모 확장), §4.2(로봇 4,096대, 배치 98,304, 20분 안의 갱신 1,500번, RTX A6000), 부록 A.1과 그림 8(로봇 수에 따른 스텝 부분마다의 시간).
- Makoviychuk, V. et al. "Isaac Gym: High performance GPU-based physics simulation for robot learning." [arXiv:2108.10470](https://arxiv.org/abs/2108.10470), 2021 — 초록.
- MuJoCo 문서, "MuJoCo XLA (MJX)" ([mujoco.readthedocs.io](https://mujoco.readthedocs.io/en/stable/mjx.html)) — MJX-JAX의 sharp bits와 MJX-Warp. MuJoCo Warp 저장소 ([github.com/google-deepmind/mujoco_warp](https://github.com/google-deepmind/mujoco_warp)).
- Isaac Lab 문서, "Creating a Direct Workflow RL Environment" ([isaac-sim.github.io/IsaacLab](https://isaac-sim.github.io/IsaacLab/main/source/tutorials/03_envs/create_direct_rl_env.html)) — `_get_dones`, `_reset_idx(env_ids)`, `num_envs`.
- JAX 문서 ([docs.jax.dev](https://docs.jax.dev/en/latest/_autosummary/jax.vmap.html)) — `jax.vmap`과 `jax.jit`.
