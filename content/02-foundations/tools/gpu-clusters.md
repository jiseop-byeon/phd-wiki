---
title: "12.7 GPU Clusters and Remote Training"
tags: [foundations, tools, hpc]
study-depth: Working
wiki-support: Working
depth-goal: "For a training job of your own on a shared Slurm cluster, write the batch script and the chain of jobs that carries it past the wall-time limit, price it in GPU-hours, lay out and stage its data so that the quota holds and the GPUs stay fed, and choose its checkpoint interval from the save cost and the interruption rate — each with the arithmetic."
mastery-when: "Raise when the thesis runs large sweeps or multi-node training on shared clusters, or when a compute budget is part of a claim."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/probability|3. Probability §2]] (the exponential waiting time and its mean), [[02-foundations/engineering-math|0.5 §1, §2 and §5]] (a minimum where the derivative is zero, the Taylor expansion of $e^x$, the geometric sum), [[02-foundations/ml-practice|9. ML Practice §6]] (batch, epochs, Adam's two moments beside an fp32 master copy of the weights, a learning-rate schedule that depends on the step) and [[02-foundations/lab-kernel|0.7 Lab Kernel §5]] (the blank-and-solve lab). A Linux shell and `ssh` are assumed. The page freezes its own objects, a fine-tuning job and a course cluster; its Python needs NumPy and the standard library only, and its Slurm, Apptainer, Lmod and `nvidia-smi` commands are shown as their documentation specifies and were not run here.
> [[02-foundations/probability|3. 확률 §2]](지수분포 대기 시간과 그 평균), [[02-foundations/engineering-math|0.5 §1, §2, §5]](도함수가 0인 곳의 최솟값, $e^x$의 테일러 전개, 기하급수 합), [[02-foundations/ml-practice|9. ML 실무 §6]](배치, 에폭, fp32 마스터 사본 곁의 Adam 두 모멘트, 스텝에 따라 달라지는 학습률 스케줄), [[02-foundations/lab-kernel|0.7 Lab Kernel §5]](빈칸 채우기 실습). 리눅스 셸과 `ssh`는 안다고 본다. 이 페이지는 파인튜닝 작업과 교과용 클러스터라는 대상을 스스로 고정한다. 파이썬 코드에는 NumPy와 표준 라이브러리만 있으면 되고, Slurm·Apptainer·Lmod·`nvidia-smi` 명령은 각 문서가 정한 대로 보이며 여기서 실행하지 않았다.

## English

*Stands on [[02-foundations/ml-practice|9. ML Practice §6]], whose training recipe this page runs on someone else's machines, and on [[02-foundations/probability|3. Probability §2]], whose exponential waiting time prices an interruption. A shared cluster imposes three things a desk machine never does — a queue, a wall-time limit and a filesystem shared with hundreds of people — and this page is about training correctly and fast under all three. The GPU inside the node is [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing]]'s subject.*

> [!note] Why this matters · 왜 배우는가
> This page sits under the stack of [[07-research-program/index|the research program §5]]: it is the compute floor beneath the "learning and adaptation" layer, where the policy that does the fitting in §5's worked instance — "Install that panel on the frame" — is trained (its place is marked on the [[physical-ai-map|Physical AI Map]]). That policy, the learned policy of [[05-construction-robotics/imitating-contact|10. Imitating Contact]], outgrows the lab workstation the day it is fine-tuned on a real demonstration corpus, and on a shared cluster the first mistakes cost days: a 50-hour fine-tuning run submitted as one 48-hour job without a checkpoint is killed at hour 48 and starts again from zero, and the same corpus stored as 3.6 million small files is refused by the quota and, read anyway, leaves the GPUs idle 35% of the time. [[03-deep-learning/foundations/training-at-scale|1.3 §5–§6]] prices such a run's memory and compute and [[03-deep-learning/foundations/gpu-computing|1.4 §7]] what the GPU does with it, and both assume the run reaches the GPU and survives to its end. The page sits outside the seven blocks of [[07-research-program/index|the dissertation path §8]]: read it when a training run first leaves your own machine, and at the latest in block 7, where 10. Imitating Contact's policy is trained. After it you can write the batch script and the chain of jobs for a run of your own, stage its data so that the GPUs stay busy, and choose its checkpoint interval from the save cost and the interruption rate.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes. **Session 1 — a long run through the queue.** The picture, §1, §4 and §5, then the Worked case's steps 1 and 4 with a calculator: FT-1 is 200 GPU-hours and needs two jobs because of the 48 h limit. End with Self-check 1, 2 and 4. **Session 2 — surviving interruptions.** §6 (run its loop and compare the two resumed runs) and §7, then step 5 by hand — a 12-minute interval — and Self-check 3 and 6. After that: §2 and §8 with steps 2–3 before you move a dataset onto a cluster, §9 and step 6 once a job runs for days, §3 the day you set up software on a cluster and §10 the day you need more GPUs; the problem set and §11's lab come last. Open a *Deeper* callout when its detail bites.

### Running object · 이 페이지의 대상

Two objects, frozen here: a training job and the machine it runs on. Neither is a plant of [[02-foundations/lab-plants|0.6 Lab Plants]]: FT-1 is a cost object, like 1.4's MLP-256 — sizes, rates and times whose *price* the page computes. Its corpus is in the spirit of [[04-robotics/teleoperation-demonstration|12. Teleoperation]]'s demonstrations and [[05-construction-robotics/imitating-contact|10. Imitating Contact]]'s policy, pooled and scaled up; nothing here depends on either page.

**FT-1**, the fine-tuning job:

| Symbol | Value | What it is |
|---|---:|---|
| $N$ | $3.0\times10^{8}$ parameters | a policy fine-tuned on demonstrations with Adam in mixed precision |
| $S$ | $12N=3.6$ GB | one checkpoint: fp32 weights and Adam's two moments, 4 bytes each per parameter (§6) |
| $G$ | 4 GPUs on one node | data parallel, 64 samples per GPU per step (§10) |
| batch, $t_{\text{step}}$ | 256 samples; 0.25 s per step | while the input keeps up, $r_{\text{need}}=256/0.25=1{,}024$ samples/s |
| steps | 720,000 | $W=720{,}000\times0.25\ \text{s}=50$ h of training, 153.6 epochs |
| corpus | 2,000 episodes × 600 samples | 60 s at 10 Hz each: 1,200,000 samples |
| sample | 3 camera images, 50 kB each | 150 kB per sample, 180 GB in all; states and actions add under 0.1% and are left out |
| layouts | 3,600,000 files, or 200 shards | one file per image, or ten episodes per 900 MB file (§8) |

**The course cluster:**

| Symbol | Value | What it is |
|---|---:|---|
| $L$ | 48 h | wall-time limit of both GPU partitions, `gpu` and `gpu-preempt` |
| node | 4 GPUs, 64 cores, 512 GB; 1.6 TB local NVMe at 2 GB/s | one compute node |
| $\beta_r$, $\beta_w$ | 1.0 GB/s, 0.5 GB/s | the shared filesystem's read and write bandwidth, per node |
| $r_f$ | 2,000 files/s | small files the shared filesystem opens per second, per node |
| home, work, scratch | 50 GB and 500,000 files; 1 TB and 1,000,000 files; 20 TB and 10,000,000 files | quotas; home is backed up, scratch deletes files 30 days after they were last read (§2) |
| $M$ | 10 h | mean time between preemptions on `gpu-preempt` (§7) |
| $q$ | 20 h for a 48 h request on `gpu`, 2 h for a 3 h one; 12 min on `gpu-preempt` | waits in the queue (§5) |
| $p$ | USD 2.00 per GPU-hour | a rented GPU's price (§10) |

Every number in both tables is this page's own course number, chosen for clean arithmetic — not a measurement of any cluster, product or price list; 1 GB $=10^9$ bytes. Slurm clusters share the shape; your site's numbers are in its user guide.

*Scope: this page teaches the everyday workflow of training on a shared GPU cluster run by Slurm — where things run and where they live, how to write, submit, chain and watch jobs, what a checkpoint must hold and how often to write one, how to lay out data so that the GPUs stay busy — with the arithmetic that prices each choice and the traps that cost days. It does not teach Linux, the shell and `ssh` ([[02-foundations/tools/linux-shell|12.1]]), Git ([[02-foundations/tools/git-research-code|12.2]]) or Python environments ([[02-foundations/tools/python-research-code|12.3]]), which have their own pages in this track; nor the GPU's internals, which are [[03-deep-learning/foundations/gpu-computing|1.4]]; nor distributed-training methods, which [[03-deep-learning/foundations/training-at-scale|1.3 §5]] names; nor scheduler internals. Every Slurm option shown is checked against Slurm's documentation, and your site's user guide has the last word on its partitions, limits and policies.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 540" style="max-width:100%;height:auto" role="img" aria-label="Two panels. (a) Where FT-1 runs: a laptop reaches the shared login node by ssh; sbatch hands the job to the Slurm controller, which allocates a compute node with four GPUs, 64 cores, 512 GB and a 1.6 TB local NVMe disk. The shared filesystem holds home (50 GB, 0.5 million files, backed up), work (1 TB, 1 million files) and scratch (20 TB, 10 million files, purged 30 days after last access). Staging the 180 GB corpus takes 3.0 minutes as 200 shards and 33.0 minutes as 3.6 million files; a 3.6 GB checkpoint goes back to work in 7.2 seconds every 12 minutes. (b) The checkpoint trade on log-log axes: saving costs C over tau, falling; lost work costs tau over 2M, rising; they cross at tau star equal to 12 minutes, 1 percent each, where their sum is at its minimum, 2 percent. The exact model with restarts lies above it, 4.59 percent at 12 minutes.">
  <defs><marker id="gc7arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) Where FT-1 runs, and what moves</text>
  <rect x="12" y="30" width="92" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="58" y="47" font-size="11" fill="currentColor" text-anchor="middle">your laptop</text>
  <text x="58" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">ssh key</text>
  <rect x="146" y="30" width="118" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="205" y="47" font-size="11" fill="currentColor" text-anchor="middle">login node</text>
  <text x="205" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">edit · submit · copy</text>
  <rect x="306" y="30" width="242" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="427" y="47" font-size="11" fill="currentColor" text-anchor="middle">Slurm controller</text>
  <text x="427" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">queue · gpu 48 h · gpu-preempt M = 10 h</text>
  <line x1="104" y1="51" x2="144" y2="51" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arr)"/>
  <text x="125" y="45" font-size="10" fill="currentColor" text-anchor="middle">ssh</text>
  <line x1="264" y1="51" x2="304" y2="51" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arr)"/>
  <text x="285" y="45" font-size="10" fill="currentColor" text-anchor="middle">sbatch</text>
  <line x1="427" y1="72" x2="427" y2="102" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arr)"/>
  <text x="433" y="91" font-size="10" fill="currentColor" fill-opacity="0.85">allocates 4 GPUs for ≤ 48 h</text>
  <rect x="306" y="104" width="242" height="112" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="316" y="120" font-size="11" fill="currentColor">compute node</text>
  <rect x="316" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="350" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="364" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="384" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="398" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="418" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="432" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <text x="456" y="142" font-size="10" fill="currentColor" fill-opacity="0.85">64 cores · 512 GB</text>
  <rect x="316" y="158" width="222" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <text x="427" y="172" font-size="10" fill="currentColor" text-anchor="middle">local NVMe 1.6 TB, 2 GB/s</text>
  <text x="316" y="200" font-size="10" fill="currentColor" fill-opacity="0.85">needs 1,024 samples/s = 153.6 MB/s</text>
  <rect x="12" y="104" width="252" height="112" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="22" y="120" font-size="11" fill="currentColor">shared filesystem</text>
  <rect x="22" y="128" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="140" font-size="10" fill="currentColor">home  50 GB · 0.5 M files · backed up</text>
  <rect x="22" y="148" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="160" font-size="10" fill="currentColor">work  1 TB · 1 M files: shards, checkpoints</text>
  <rect x="22" y="168" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="180" font-size="10" fill="currentColor">scratch  20 TB · 10 M files · purged at 30 d</text>
  <text x="22" y="206" font-size="10" fill="currentColor" fill-opacity="0.8">per node: 1 GB/s read · 0.5 GB/s write · 2,000 files/s</text>
  <line x1="255" y1="154" x2="314" y2="165" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arr)"/>
  <text x="283" y="152" font-size="10" fill="currentColor" text-anchor="middle">stage</text>
  <line x1="306" y1="190" x2="257" y2="162" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#gc7arr)"/>
  <text x="283" y="196" font-size="10" fill="currentColor" text-anchor="middle">save</text>
  <text x="12" y="240" font-size="10" fill="currentColor">staging 180 GB, to scale:</text>
  <rect x="160" y="231" width="27.3" height="11" fill="currentColor" fill-opacity="0.75"/>
  <text x="193.3" y="240" font-size="10" fill="currentColor">200 shards: 3.0 min</text>
  <rect x="160" y="248" width="300.0" height="11" fill="currentColor" fill-opacity="0.3"/>
  <text x="166" y="257" font-size="10" fill="currentColor">3,600,000 files: 33.0 min</text>
  <text x="12" y="280" font-size="10" fill="currentColor" fill-opacity="0.85">checkpoint: 3.6 GB to work in 7.2 s, every 12 min (§6–§7)</text>
  <text x="12" y="306" font-size="12" fill="currentColor">(b) The checkpoint trade for FT-1: C = 7.2 s, M = 10 h</text>
  <line x1="70.0" y1="471.4" x2="540.0" y2="471.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="474.9" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.1%</text>
  <line x1="70.0" y1="422.9" x2="540.0" y2="422.9" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="426.4" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">1%</text>
  <line x1="70.0" y1="374.5" x2="540.0" y2="374.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="378.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">10%</text>
  <line x1="70.0" y1="326.0" x2="540.0" y2="326.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="329.5" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">100%</text>
  <line x1="70.0" y1="326.0" x2="70.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="70.0" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1 min</text>
  <line x1="164.2" y1="326.0" x2="164.2" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="164.2" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">3</text>
  <line x1="267.5" y1="326.0" x2="267.5" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="267.5" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <line x1="361.7" y1="326.0" x2="361.7" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="361.7" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">30</text>
  <line x1="421.1" y1="326.0" x2="421.1" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="421.1" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1 h</text>
  <line x1="540.0" y1="326.0" x2="540.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="540.0" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">4 h</text>
  <line x1="70.0" y1="326.0" x2="70.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70.0" y1="486.0" x2="540.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="305" y="513.0" font-size="10" fill="currentColor" text-anchor="middle">checkpoint interval τ, log scale</text>
  <text x="76.0" y="338.0" font-size="10" fill="currentColor" fill-opacity="0.8">share of W</text>
  <polyline points="70.0,370.6 77.8,372.6 85.7,374.5 93.5,376.4 101.3,378.3 109.2,380.2 117.0,382.2 124.8,384.1 132.7,386.0 140.5,387.9 148.3,389.9 156.2,391.8 164.0,393.7 171.8,395.6 179.7,397.6 187.5,399.5 195.3,401.4 203.2,403.3 211.0,405.2 218.8,407.2 226.7,409.1 234.5,411.0 242.3,412.9 250.2,414.9 258.0,416.8 265.8,418.7 273.7,420.6 281.5,422.5 289.3,424.5 297.2,426.4 305.0,428.3 312.8,430.2 320.7,432.2 328.5,434.1 336.3,436.0 344.2,437.9 352.0,439.9 359.8,441.8 367.7,443.7 375.5,445.6 383.3,447.5 391.2,449.5 399.0,451.4 406.8,453.3 414.7,455.2 422.5,457.2 430.3,459.1 438.2,461.0 446.0,462.9 453.8,464.8 461.7,466.8 469.5,468.7 477.3,470.6 485.2,472.5 493.0,474.5 500.8,476.4 508.7,478.3 516.5,480.2 524.3,482.2 532.2,484.1 540.0,486.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="5 3"/>
  <polyline points="70.0,475.2 77.8,473.3 85.7,471.4 93.5,469.5 101.3,467.6 109.2,465.6 117.0,463.7 124.8,461.8 132.7,459.9 140.5,457.9 148.3,456.0 156.2,454.1 164.0,452.2 171.8,450.3 179.7,448.3 187.5,446.4 195.3,444.5 203.2,442.6 211.0,440.6 218.8,438.7 226.7,436.8 234.5,434.9 242.3,432.9 250.2,431.0 258.0,429.1 265.8,427.2 273.7,425.3 281.5,423.3 289.3,421.4 297.2,419.5 305.0,417.6 312.8,415.6 320.7,413.7 328.5,411.8 336.3,409.9 344.2,407.9 352.0,406.0 359.8,404.1 367.7,402.2 375.5,400.3 383.3,398.3 391.2,396.4 399.0,394.5 406.8,392.6 414.7,390.6 422.5,388.7 430.3,386.8 438.2,384.9 446.0,383.0 453.8,381.0 461.7,379.1 469.5,377.2 477.3,375.3 485.2,373.3 493.0,371.4 500.8,369.5 508.7,367.6 516.5,365.6 524.3,363.7 532.2,361.8 540.0,359.9" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <polyline points="70.0,370.5 77.8,372.4 85.7,374.3 93.5,376.1 101.3,378.0 109.2,379.9 117.0,381.7 124.8,383.6 132.7,385.4 140.5,387.2 148.3,389.0 156.2,390.7 164.0,392.4 171.8,394.1 179.7,395.7 187.5,397.3 195.3,398.8 203.2,400.3 211.0,401.6 218.8,402.9 226.7,404.1 234.5,405.1 242.3,406.1 250.2,406.8 258.0,407.5 265.8,407.9 273.7,408.2 281.5,408.3 289.3,408.3 297.2,408.1 305.0,407.7 312.8,407.1 320.7,406.4 328.5,405.5 336.3,404.5 344.2,403.4 352.0,402.2 359.8,400.9 367.7,399.4 375.5,397.9 383.3,396.4 391.2,394.8 399.0,393.1 406.8,391.4 414.7,389.7 422.5,387.9 430.3,386.1 438.2,384.3 446.0,382.5 453.8,380.6 461.7,378.8 469.5,376.9 477.3,375.0 485.2,373.2 493.0,371.3 500.8,369.4 508.7,367.5 516.5,365.6 524.3,363.6 532.2,361.7 540.0,359.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polyline points="70.0,366.0 77.8,367.6 85.7,369.1 93.5,370.6 101.3,372.1 109.2,373.5 117.0,374.9 124.8,376.3 132.7,377.6 140.5,378.8 148.3,380.0 156.2,381.2 164.0,382.3 171.8,383.3 179.7,384.3 187.5,385.2 195.3,386.1 203.2,386.9 211.0,387.6 218.8,388.3 226.7,388.9 234.5,389.4 242.3,389.8 250.2,390.2 258.0,390.5 265.8,390.7 273.7,390.8 281.5,390.9 289.3,390.8 297.2,390.7 305.0,390.5 312.8,390.3 320.7,389.9 328.5,389.5 336.3,389.0 344.2,388.4 352.0,387.8 359.8,387.1 367.7,386.3 375.5,385.4 383.3,384.5 391.2,383.5 399.0,382.4 406.8,381.3 414.7,380.1 422.5,378.8 430.3,377.5 438.2,376.2 446.0,374.8 453.8,373.3 461.7,371.8 469.5,370.3 477.3,368.7 485.2,367.0 493.0,365.3 500.8,363.6 508.7,361.8 516.5,360.0 524.3,358.1 532.2,356.2 540.0,354.3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.5"/>
  <line x1="283.1" y1="344.0" x2="283.1" y2="486.0" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 2" stroke-opacity="0.8"/>
  <circle cx="283.1" cy="408.3" r="3.8" fill="currentColor"/>
  <circle cx="283.1" cy="422.9" r="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="283.1" cy="390.9" r="3.4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="289.1" y="338.0" font-size="10" fill="currentColor" font-weight="bold">τ* = √(2CM) = 12 min</text>
  <text x="289.1" y="351.0" font-size="10" fill="currentColor">first order 1% + 1% = 2.0%; exact 4.59%</text>
  <line x1="16" y1="527.5" x2="36" y2="527.5" stroke="currentColor" stroke-width="2.2"/>
  <text x="41" y="531.0" font-size="10" fill="currentColor">sum, first order</text>
  <line x1="140" y1="527.5" x2="160" y2="527.5" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.5"/>
  <text x="165" y="531.0" font-size="10" fill="currentColor">exact, with restarts</text>
  <line x1="300" y1="527.5" x2="320" y2="527.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="5 3"/>
  <text x="325" y="531.0" font-size="10" fill="currentColor">saving C/τ</text>
  <line x1="420" y1="527.5" x2="440" y2="527.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <text x="445" y="531.0" font-size="10" fill="currentColor">lost work τ/2M</text>
</svg>

FT-1 on the course cluster. (a) The laptop reaches the login node over `ssh` and hands FT-1 to Slurm with `sbatch`; Slurm allocates a node with four GPUs, the job stages the corpus from work to the node's own disk — 3.0 min as 200 shards, 33.0 min as 3,600,000 files, the same 180 GB — and writes a 3.6 GB checkpoint back to work every 12 minutes. (b) On the preemptible partition ($C=7.2$ s, $M=10$ h) saving costs $C/\tau$ of the training time and lost work $\tau/2M$; the two cross at $\tau^\star=12$ min, 1% each, where their sum is smallest, 2%, and the exact model, which adds the restarts, sits at 4.59%.

### 1. Cluster anatomy: login node, scheduler, compute nodes

*In one sentence:* hundreds of users share the cluster's GPUs, so you never simply take one: you type on a shared login node and ask the scheduler, and your training runs only inside a job — with exactly the resources the job asked for, for at most the time it asked for.

**The problem.** FT-1 needs four GPUs for 50 hours. The cluster has hundreds of GPUs and hundreds of users, and something must decide who gets which GPU, and when.

**The idea.** That something is the scheduler, Slurm. You log in with `ssh` to a **login node**, one of a few that every user shares, and from there you *ask*: a **job** is a request for resources for a stated time, with a script to run on them. Slurm queues it, starts the script on **compute nodes** when they are free, and takes the nodes back when the script ends or the time runs out. Nobody logs into a compute node to work; a program runs on one only because Slurm started it there. Nodes are grouped into **partitions**, each with its own limits. The course cluster's `gpu` and `gpu-preempt` hold the same nodes under the same 48 h limit; on the second, a running job can be stopped to make room for others (§7).

> **Batch job, defined.** A **batch job** is *a request to the scheduler* — resources, a time limit and a script — not a running program. Four defining conditions. It **names its resources** (nodes, GPUs, cores, memory, a partition) and receives nothing it did not name. It has a **time limit**, no longer than its partition's, and it ends when its script ends or when the limit arrives, whichever comes first. It runs **without your terminal**: `sbatch` returns as soon as the script has a job ID, and when resources are free Slurm runs one copy of the script, usually on the job's first node, with its output going to a file. And it **uses up its whole allocation** while it holds it, whatever the resources are doing.
>
> $$t_{\text{end}}=t_{\text{start}}+\min\big(t_{\text{script}},\ L_{\text{job}}\big),\qquad L_{\text{job}}\le L,\qquad \text{GPU-hours}=G\,\big(t_{\text{end}}-t_{\text{start}}\big)$$
>
> where $t_{\text{script}}$ is how long the script would run if nothing stopped it, $L_{\text{job}}$ the job's limit, $L$ the partition's and $G$ the allocated GPUs — so the charge follows the allocation and the clock, never how busy the GPUs were.
>
> - **Example**: FT-1's first job asks for one node, `--gres=gpu:4` and 48 h. Its script wants 50 h of training, so the job ends at the limit, after 48 h, having used 192 GPU-hours.
> - **Non-example**: `python train.py` typed at the login node's prompt. No scheduler started it, no GPU was allocated to it, and it ends with your `ssh` session.
> - **Why it matters**: jobs stop at the limit whether training is done or not, so a long run has to be cut into several (§5); and they are charged for what they hold, so an idle GPU inside one costs as much as a busy one (§9).

**The traps.**

- *Working on the login node.* It is for editing, submitting, moving files and a test that takes seconds. A data loader with 32 worker processes started there "just to check that it runs" slows every user's session, has no GPU, and dies with your connection. Test in a short interactive allocation instead (§5).
- *Forgetting the GPUs.* Slurm allocates GPUs only to jobs that ask for them, per node with `--gres=gpu:4` or with `--gpus`. A job that forgets lands on a GPU node and sees none — and if the code falls back to the CPU, it trains for days instead of failing in a second. For the GPUs a job does get, Slurm sets `CUDA_VISIBLE_DEVICES`, so the code should use whatever devices it sees.
- *Asking for more than the partition allows.* A job with `--time=72:00:00` on a 48 h partition does not start and fail: it pends, possibly forever, with the reason `PartitionTimeLimit`.

What a job held, and for how long, is what `sacct` records and what you pay — in GPU-hours from a budget where the site keeps one, and in priority: Slurm's fair-share factor is the gap between the share of the machine you were promised and what you have used, so an idle allocated GPU lowers your next job's priority as a busy one does.

### 2. Storage: where data may live

*In one sentence:* FT-1's corpus and checkpoints need a place that every node sees, that is not deleted and that they fit in, and a cluster's filesystems differ in exactly those promises — backed up or purged, shared or private to one node — each with a quota that counts files as well as bytes.

**The problem.** FT-1 has a 180 GB corpus, writes a 3.6 GB checkpoint every 12 minutes, and runs from a container image and some code. Each must live where every node can reach it, where it will not be deleted, and where it fits.

**The idea.** Sites offer the same four kinds of place under different names. The numbers are the course cluster's:

| place | course cluster | its promise | for | never for |
|---|---|---|---|---|
| home | 50 GB, 500,000 files | backed up, never purged | code, configs, job scripts | datasets, checkpoints, environments |
| work | 1 TB, 1,000,000 files | kept, not backed up | the corpus as shards, checkpoints, the image | millions of small files |
| scratch | 20 TB, 10,000,000 files | deletes files unread for 30 days | intermediate outputs, a working copy | the only copy of anything |
| the node's own NVMe | 1.6 TB, no quota | this job only | the staged corpus, temporary files | anything the next job needs |

Home, work and scratch are *shared*: every node sees the same files. The node's own disk is *private*: the fastest place on the machine for many small reads, and invisible from every other node — FT-1's second job may run on another node, which cannot see what the first left behind.

**Why files count, not only bytes.** A parallel filesystem such as Lustre keeps the contents of files on data servers, and each file's name, permissions and layout — where its data lives — on metadata servers that every user shares; a client asks the metadata server to open a file and then reads the bytes from the data servers directly (Lustre wiki). Reading a file therefore costs one request to open it, and then the bytes stream at the bandwidth. The course cluster serves one node about $r_f=2{,}000$ opens per second beside $\beta_r=1$ GB/s of reads, so a million files of 50 kB are not "50 GB" to the filesystem: they are a million requests. §8 prices this, and the quota enforces it.

> **Storage quota, defined.** A **storage quota** is *a limit that a filesystem enforces on one user's or one project's usage* — a rule applied when you write, not a measure of free space. Four defining conditions. It has **two limits**, on bytes and on files, and every file counts once towards the second however small it is. It is **per filesystem**: home, work and scratch each have their own. It is **enforced at the write**: creating a file past either limit fails — Linux's `open` returns `EDQUOT`, "Disk quota exceeded", once the quota of disk blocks or of inodes is used up. And it is **not a purge**: a quota refuses new data by amount, a purge deletes old data by age.
>
> $$\text{a write succeeds only if}\quad \sum_{i=1}^{n} b_i\le Q_b\quad\text{and}\quad n\le Q_n$$
>
> where $b_i$ is the size of file $i$, $n$ the number of files, and $Q_b$, $Q_n$ the byte and file limits — so a corpus of $B$ bytes fits only if its files average at least $B/Q_n$ bytes: 180 kB for FT-1's 180 GB on work.
>
> - **Example**: FT-1's corpus as one file per image on work: 180 GB against 1 TB passes, 3,600,000 files against 1,000,000 fails. Every file after the millionth is refused, so at most 27.8% of the corpus arrives. As 200 shards of 900 MB it is 180 GB and 200 files, and both limits hold.
> - **Non-example**: scratch's 30-day rule. A corpus inside scratch's quota is still deleted if nobody reads it for a month: the quota let it in, the purge takes it away.
> - **Why it matters**: the file limit is the one people forget, because a laptop has none — and it is why FT-1 is sharded.

**The traps.**

- *Scratch as the only copy.* The corpus left there over the summer is partly gone in September.
- *Checkpoints on the node's own disk.* Complete, and invisible to the next job.
- *An environment in home.* A Python environment is tens of thousands of files (§3); two or three of them fill most of home's 500,000.

### 3. Software: modules and containers

*In one sentence:* you cannot install into a cluster's system, so the software FT-1 needs must come from the site's modules, from an environment in your own directories or from a container image — and the job script, not the terminal you submitted from, must set it up.

**The problem.** FT-1 needs particular versions of Python, PyTorch and CUDA. On your workstation you would `sudo apt install` them; on a cluster you have no root, and the system's software belongs to the administrators and changes when they upgrade.

**The idea.** Three sources. The site's **modules**: software the site installed, which `module load` adds to your shell's environment. **Your own environment**, a virtual or conda environment in work: it works, and it is many files. A **container image**: Apptainer packs a whole software environment into one SIF file, which runs as you, on the node's own kernel and GPU driver — `--nv` for the GPUs, `--bind` for the data. Verified in Lmod's and Apptainer's documentation, not run here:

```bash
module avail                                                   # software the site offers
module load cuda                                               # add it to this shell's environment
apptainer build policy.sif docker://<registry>/<image>:<tag>   # an existing image, as one file
apptainer exec --nv --bind /path/to/shards:/data policy.sif python train.py --data /data
```

**The rule, on the object.** An environment costs files: as a directory, one per file it holds — against the file quota, and against the metadata servers at every start-up; as a SIF image, one. The Python installation on the laptop this page was written on holds 127,915 files in 3.5 GB (measured; the callout shows how) — 12.8% of work's file quota for one environment. FT-1's `policy.sif` is 1 file.

**The traps.**

- *The job inherits your terminal.* A job starts with the whole environment of the shell that ran `sbatch`: Slurm's `--export` loads all of it unless told otherwise. A script that works when submitted from the terminal where you activated an environment, and fails with `ModuleNotFoundError` from a fresh login, was running on your terminal's state. Put the setup in the script — `module purge` and the `module load` lines, or the container.
- *An image newer than the driver.* The GPU driver is the node's, not the image's; software built for a CUDA version the node's driver does not support fails there, however complete the image is.
- *No record of the environment.* Record the image's checksum with the results, as the pinned run of [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]] records an image digest and [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §7]] lists the container among a run's artifacts.

> [!note]- Deeper · 더 깊이
> - **Modules.** `module spider <name>` searches every module the site has, including those that appear only after another is loaded; `module list` shows what is loaded and `module purge` unloads it all (Lmod user guide).
> - **Apptainer.** You are the same user inside a container as outside and gain no privilege on the host by default. An unprivileged `apptainer build policy.sif policy.def`, from a definition file of your own, runs with `--fakeroot` implied. `--nv` makes the host's NVIDIA devices visible, binds the host's CUDA driver libraries in and points `LD_LIBRARY_PATH` at them. By default the container sees your home, the current directory, `/tmp`, `/var/tmp` and system paths such as `/dev` and `/proc` — the administrator can change that list — and anything else only through `--bind src:dest`; several binds go comma-separated or in several `--bind` options (Apptainer user guide).
> - **The measurement**, on macOS; `find`, `wc` and `du -sh` behave the same on Linux:
>
>   ```bash
>   python3 -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
>   find /opt/anaconda3/lib/python3.12/site-packages -type f | wc -l
>   du -sh /opt/anaconda3/lib/python3.12/site-packages
>   ```
>
>   ```text
>   /opt/anaconda3/lib/python3.12/site-packages
>     127915
>   3.5G	/opt/anaconda3/lib/python3.12/site-packages
>   ```

### 4. The batch script and a job's life

*In one sentence:* Slurm runs only what it can read, so FT-1's request goes into a batch script whose `#SBATCH` comment lines Slurm reads before any shell does; `sbatch` queues it and returns at once, and `squeue` and `sacct` follow the job from pending to the state it ends in.

**The problem.** FT-1's request — one node, four GPUs, 32 cores, 256 GB, a log file, a warning before the limit — must be written where Slurm reads it, together with the commands to run.

**The idea.** A batch script. Its `#SBATCH` lines carry the options `sbatch` would take on its command line, and the rest is an ordinary bash script that runs on the job's first node. FT-1's `ft1.sbatch` — every option from the `sbatch` page of Slurm's documentation (version 26.05), `torchrun`'s single-node form from PyTorch's; the `/path/to/...` parts stand for your site's paths; not run here:

```bash
#!/bin/bash
#SBATCH --job-name=ft1                  # %x in file names; the name a singleton dependency matches (§5)
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --gres=gpu:4                    # four GPUs on the node; without it, no GPU at all
#SBATCH --cpus-per-task=32              # cores for the data loader; the default is one per task
#SBATCH --mem=256G
#SBATCH --output=logs/%x-%j.out         # %j is the job ID; stdout and stderr share the file
#SBATCH --signal=USR1@600               # SIGUSR1 to the job's steps about 10 min before the limit (§6)
#SBATCH --mail-type=END,FAIL,INVALID_DEPEND
# no --time line: each job's limit is given on the sbatch command line (§5)
set -euo pipefail
WORK=/path/to/work/ft1                              # the site's persistent project space
LOCAL=/path/to/node-local-disk/$SLURM_JOB_ID        # the node's own disk; the site documents where
mkdir -p "$LOCAL/shards"
rsync -a "$WORK/shards/" "$LOCAL/shards/"           # stage 200 shards, 180 GB: about 3 min (§8)
srun apptainer exec --nv --bind "$LOCAL/shards":/data,"$WORK":/run "$WORK/policy.sif" \
     torchrun --standalone --nnodes=1 --nproc-per-node=4 train.py \
     --data /data --ckpt-dir /run/ckpt --save-every-min 12 --resume latest
```

**The rules.** Slurm reads the `#SBATCH` lines itself, before any shell does, so a shell variable written into one — the home directory's, say — is taken letter for letter, dollar sign included. It stops reading them at the first line that is neither a comment nor blank, so all of them must come before `set -euo pipefail`. That line then stops the job at the first failing command: an `rsync` that fails halfway ends the job instead of starting a training run on part of the corpus. `srun` starts the training as a job step, `apptainer exec` runs it in the container, and `torchrun` starts one worker process per GPU (§10). `train.py` and its options are FT-1's own.

**On the object: a job's life.** Verified in Slurm's documentation, not run here:

```bash
mkdir -p logs                                         # the directory the --output pattern names
JOB1=$(sbatch --parsable --time=48:00:00 ft1.sbatch)  # --parsable prints only the new job's ID
squeue --me                                           # your jobs, their state and, while pending, the reason
sacct -j "$JOB1" --format=JobID,JobName,State,ExitCode,Elapsed,Timelimit,MaxRSS
scancel "$JOB1"                                       # cancel it, pending or running
```

`sbatch` returns as soon as the job has an ID. While the job waits in state `PD` its reason says why: `Priority` (other jobs come first), `Resources` (it waits for nodes to free up) or `Dependency` (it waits for another job, §5). Running, it is in state `R` and writes `logs/ft1-<jobid>.out`. It ends `COMPLETED` if every process exited with code zero, or `FAILED`, `TIMEOUT` (it reached its limit), `CANCELLED`, `OUT_OF_MEMORY`, `NODE_FAIL` or `PREEMPTED`; afterwards `sacct` shows that state, the exit code and the peak memory of its tasks.

**The traps.**

- *The limit kills.* At the limit every task receives SIGTERM and then SIGKILL — 30 s later in Slurm's default configuration, and whatever your site has set. Whatever was not saved is gone. FT-1 asks for a warning ten minutes earlier with `--signal=USR1@600` and saves on it (§6).
- *Polling the scheduler.* Every `squeue` is a request to the Slurm controller, and Slurm's documentation warns that client commands run in loops from scripts can slow the controller for everyone. `watch -n 1 squeue` is such a loop; let `--mail-type=END,FAIL` tell you instead.

> [!note]- Deeper · 더 깊이
> More pending reasons: `PartitionTimeLimit` (the limit exceeds the partition's: it waits forever — or, where the site sets `EnforcePartLimits`, `sbatch` refuses it at submission), `QOSMaxGRESPerUser` (the request exceeds the GPUs each user may hold under that quality of service), `DependencyNeverSatisfied` (§5). `squeue --me --start` shows when the scheduler expects each pending job to start. `sacct` without `-j` or a start time lists only the jobs since midnight. `--mail-type` also takes `TIME_LIMIT_80` (80% of the limit used) and `INVALID_DEPEND`. `sbatch --test-only` checks a script and estimates when it would start, without submitting it.

### 5. Longer than the limit: chains of jobs, job arrays and interactive work

*In one sentence:* 50 hours of training do not fit a 48-hour limit, so the run becomes a chain of jobs that each resume from the last checkpoint, joined by a dependency whose type decides whether the chain survives the limit — and an honest, short time limit gets each job started sooner.

**The problem.** FT-1 needs 50 h of training; the partitions allow 48.

**The idea.** Cut the run into **windows**: jobs that each resume from the latest checkpoint and train until their own limit, each queued to start when the one before it has ended. A window loses a little to fixed costs at its start — staging the data, loading the checkpoint — and a little to the saves along the way; the rest of it is training.

**The rule.** A window first pays a fixed cost $o$, then pauses $C$ to save after every $\tau$ of training (§6–§7), so a full window holds

$$w=(L-o)\,\frac{\tau}{\tau+C},\qquad k=\Big\lceil\frac{W}{w}\Big\rceil$$

hours of training, because the saves take the fraction $C/(\tau+C)$ of whatever time the fixed cost leaves; $k$ is the number of windows.

**On the object.** $o=180.1+3.6=183.7$ s $=0.0510$ h (staging 200 shards, loading 3.6 GB), $C=7.2$ s and $\tau=12$ min give $w=(48-0.0510)\times0.2/0.202=47.47$ h, so $k=\lceil50/47.47\rceil=2$. The second window needs only $0.0510+(50-47.47)\times1.01=2.60$ h, and it asks for 3 h, not 48, because of **backfill**: Slurm starts a lower-priority job early if that delays no higher-priority job's expected start, and since those starts are computed from time limits, a node that is free for the next 5 h can take a 3 h job and not a 48 h one. In the course numbers, a 3 h request waits 2 h and a 48 h request 20 h. The chain, verified in Slurm's documentation and not run here:

```bash
JOB1=$(sbatch --parsable --time=48:00:00 ft1.sbatch)
sbatch --time=03:00:00 --dependency=afterany:$JOB1 ft1.sbatch     # eligible once window 1 has ended, however
```

`--dependency=singleton` would do the same by name: the job may start once every earlier job of yours named `ft1` has ended.

> **Job dependency, defined.** A **job dependency** is *a condition attached to a pending job, naming other jobs and how they must have ended before this one may start* — a rule the scheduler evaluates, not the order in which you wrote the scripts. Four defining conditions. Its **type** says which endings count: `afterany`, any ending; `afterok`, completion with exit code zero; `afternotok`, a failed ending — a non-zero exit, a node failure, a timeout; `singleton`, the end of every earlier job of yours with the same name. Until the condition holds, the job **pends with the reason `Dependency`**. Once the condition **can no longer hold**, the job never runs — its reason becomes `DependencyNeverSatisfied`, and a later requeue of the earlier job does not revive it. And a satisfied dependency only makes the job **eligible**: it then waits for resources like any other.
>
> $$t_{\text{eligible}}(B)=\begin{cases}t_{\text{end}}(A)&\text{if state}(A)\in S_{\text{type}}\\ \infty&\text{otherwise}\end{cases},\qquad S_{\text{afterok}}=\{\text{COMPLETED}\},\quad S_{\text{afterany}}=\{\text{every end state}\}$$
>
> where $A$ is the earlier job, $B$ the dependent one and $S_{\text{type}}$ the end states of $A$ that the type accepts — so $B$ starts no earlier than $A$'s end plus its own wait for resources, and never if $A$ ends outside the set.
>
> - **Example**: FT-1's second window, `--dependency=afterany:$JOB1`. Window 1 ends in `TIMEOUT` at 48 h, which `afterany` accepts, so window 2 is eligible at once and, asking for 3 h, starts 2 h later in the course numbers.
> - **Non-example**: the same chain with `afterok`, the choice that looks natural. A job that timed out did not complete with exit code zero, so window 2 is never eligible: it waits as `DependencyNeverSatisfied` while a weekend passes without training. (A window that saved on the warning and exited with code zero would satisfy `afterok` — so such a chain holds only while every window ends cleanly.)
> - **Why it matters**: a chain is how a run longer than the limit continues while you sleep; the type decides whether it survives the very limit it was built for, and `--mail-type=INVALID_DEPEND` mails you the moment a dependency can no longer be met.

**Sweeps: job arrays.** Many variants of one run are one script with an index: `--array=0-11%4` submits twelve tasks under one job ID, at most four running at once, and each task reads its index from `SLURM_ARRAY_TASK_ID`. A learning-rate-by-seed sweep of a shortened FT-1, 5 h per task, is $12\times4\times5=240$ GPU-hours, never more than 16 GPUs at once. The tasks are independent — `%4` limits how many run, not their order — so "train, then evaluate" is a dependency, not an array.

**Debugging: interactive allocations.** `salloc --partition=gpu --gres=gpu:1 --time=01:00:00` holds one GPU for an hour and gives you a shell; `srun <command>` runs a command on the allocated node; `exit` gives it back. The trap is where that shell runs — on the login node, unless the site configured otherwise — so compare `hostname` with `srun hostname` before working. And the allocation ends with the shell: close the laptop, and the dropped `ssh` connection takes both.

> [!note]- Deeper · 더 깊이
> - **Interactive shells.** Given no command, `salloc` runs your default shell and gives the allocation back when it exits. With `LaunchParameters=use_interactive_step` in the site's configuration, it starts that shell on an allocated node; Slurm's FAQ calls this the recommended way to get an interactive shell since 20.11, and no longer recommends `srun --pty bash -i`.
> - **Arrays.** `%A` and `%a` put the array's ID and the task's index into file names; `scancel <id>` cancels every task and `scancel <id>_3` one; indices run to one less than the site's `MaxArraySize`, 1,001 by default. The sweep's lines — the index arithmetic was checked in bash on the laptop, with `echo` in place of `python`, for $i=0,\dots,11$:
>
>   ```bash
>   #SBATCH --array=0-11%4                  # twelve tasks, at most four at a time
>   #SBATCH --output=logs/%x-%A_%a.out      # %A the array's job ID, %a the task's index
>   LR=(1e-4 3e-4 1e-3); SEED=(0 1 2 3)
>   i=$SLURM_ARRAY_TASK_ID
>   python train.py --steps 72000 --lr ${LR[$((i / 4))]} --seed ${SEED[$((i % 4))]}
>   ```
>
>   Tasks 0–3 take the first learning rate with seeds 0–3, tasks 4–7 the second, tasks 8–11 the third.
> - **Time limits.** `--time-min` lets Slurm lower a job's limit, no further than the value given, if that lets it start earlier.

### 6. Checkpoints: what to save, and how

*In one sentence:* every interruption loses everything since the last save, and a resume is only as good as what was saved; a checkpoint is therefore the run's complete state at a step boundary, written atomically to storage that outlives the job, so that the resumed run is the same run.

**The problem.** On `gpu-preempt` FT-1 is stopped about five times in its 50 hours (§7), and each time the next job starts from whatever the last one saved: nothing, and it starts again at step 0; the weights alone, and it starts a different run from the one its config describes.

**The idea.** Save everything the next step will read, between steps, on shared storage, under a temporary name that is renamed into place — and save once more when Slurm warns that the limit is near. PyTorch's guidance for resuming training makes the same point about the optimizer: save its state beside the model's, since it holds buffers and parameters updated during training, and save the epoch too.

**On the object: what goes in.** FT-1 trains with Adam in mixed precision ([[02-foundations/ml-practice|9. ML Practice §6]]), so the checkpoint holds the fp32 master weights and Adam's two moments, 4 bytes each per parameter: $S=12\times3.0\times10^8=3.6$ GB, written in $C=3.6/0.5=7.2$ s. The 16-bit copies and the gradients of [[03-deep-learning/foundations/training-at-scale|1.3 §5]]'s sixteen-byte ledger are rebuilt by the next step. Then the small things that decide *which* run you are continuing: the step counter, since the learning-rate schedule is a function of it; every random-number generator's state, since they draw the minibatches; the loader's position in the epoch; an EMA copy — an exponential moving average of the weights — if the recipe keeps one; and the config, code and image versions. Keep the last two checkpoints, on work.

**How.** A rename within one filesystem is atomic, so a job killed in the middle of a save leaves the last good checkpoint intact. And the signal handler only sets a flag, which the loop checks between optimizer steps: Python runs a handler later, in the main thread, between two bytecodes, so a handler that saved by itself could catch the weights halfway through an update. The loop below does all of this on a toy problem, sending itself the signal in place of Slurm's warning.

```python
# 12.7 §6: a resumable training loop - what a checkpoint must hold. NumPy + stdlib.
import json, math, os, signal, tempfile
import numpy as np

# A small stand-in for FT-1's training: Adam fitting a linear model to 4,096 points, minibatches drawn from a
# seeded generator, a cosine learning-rate schedule over T_TOTAL steps. Its whole state is five things:
# the weights, Adam's two moments, the step counter and the generator's state.
D, N_DATA, T_TOTAL, LR_MAX, BS = 8, 4096, 1000, 0.05, 64
g = np.random.default_rng(0)
X = g.random((N_DATA, D)) * 2 - 1
y = X @ (g.random(D) * 2 - 1) + 0.1 * (g.random(N_DATA) * 2 - 1)

def new_run(seed=1):
    return {"w": np.zeros(D), "m": np.zeros(D), "v": np.zeros(D), "t": 0, "rng": np.random.default_rng(seed)}

def lr(t):                                    # cosine schedule: depends on the step counter
    return 0.5 * LR_MAX * (1 + math.cos(math.pi * t / T_TOTAL))

def step(run):
    idx = (run["rng"].random(BS) * N_DATA).astype(np.int64)        # this step's minibatch
    grad = 2 * X[idx].T @ (X[idx] @ run["w"] - y[idx]) / BS
    run["m"] = 0.9 * run["m"] + 0.1 * grad
    run["v"] = 0.999 * run["v"] + 0.001 * grad ** 2
    run["t"] += 1
    m_hat, v_hat = run["m"] / (1 - 0.9 ** run["t"]), run["v"] / (1 - 0.999 ** run["t"])
    run["w"] = run["w"] - lr(run["t"] - 1) * m_hat / (np.sqrt(v_hat) + 1e-8)

def save(run, path):
    """Write everything to path + '.tmp', then rename it over path: a crash leaves the old file or the new."""
    with open(path + ".tmp", "wb") as f:
        np.savez(f, w=run["w"], m=run["m"], v=run["v"], t=run["t"],
                 rng=json.dumps(run["rng"].bit_generator.state))
    os.replace(path + ".tmp", path)

def load(path):
    with np.load(path) as z:
        run = {"w": z["w"], "m": z["m"], "v": z["v"], "t": int(z["t"]), "rng": np.random.default_rng()}
        run["rng"].bit_generator.state = json.loads(str(z["rng"]))
    return run

stop = {"requested": False}
def on_usr1(signum, frame):                   # the handler only sets a flag; the loop saves between steps
    stop["requested"] = True

def train(run, path, warn_at=None):
    while run["t"] < T_TOTAL:
        if stop["requested"]:
            save(run, path)
            return "saved at step %d and stopped" % run["t"]
        step(run)
        if run["t"] == warn_at:
            os.kill(os.getpid(), signal.SIGUSR1)                     # stands in for Slurm's --signal=USR1@600
    return "finished at step %d" % run["t"]

ref = new_run()
train(ref, None)                              # the run as it goes when nothing interrupts it
loss = lambda w: float(np.mean((X @ w - y) ** 2))
previous = signal.signal(signal.SIGUSR1, on_usr1)
with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, "ft1.npz")
    first = train(new_run(), path, warn_at=400)
    with np.load(path) as z:
        print("first window:", first, "- the file holds", ", ".join(sorted(z.files)))
    stop["requested"] = False
    weights_only = new_run()                  # a resume that keeps only the weights:
    weights_only["w"] = load(path)["w"]       # fresh moments, step 0, the generator re-seeded
    for name, run in (("full state", load(path)), ("weights only", weights_only)):
        t0, lr0 = run["t"], lr(run["t"])
        train(run, path)
        print("%-12s resumes at step %3d with lr %.4f, runs %4d more steps, final loss %.6f, max |w - w_ref| = %.1e"
              % (name, t0, lr0, T_TOTAL - t0, loss(run["w"]), np.max(np.abs(run["w"] - ref["w"]))))
signal.signal(signal.SIGUSR1, previous)
print("uninterrupted: %d steps, final loss %.6f" % (T_TOTAL, loss(ref["w"])))
```

```text
first window: saved at step 400 and stopped - the file holds m, rng, t, v, w
full state   resumes at step 400 with lr 0.0327, runs  600 more steps, final loss 0.003350, max |w - w_ref| = 0.0e+00
weights only resumes at step   0 with lr 0.0500, runs 1000 more steps, final loss 0.003352, max |w - w_ref| = 1.7e-03
uninterrupted: 1000 steps, final loss 0.003350
```

The run resumed from its full state is, bit for bit, the run that was never stopped. The run resumed from its weights alone restarts its schedule at the peak, 0.0500 instead of 0.0327, draws its first 400 minibatches again, trains 400 extra steps — 1,400 in all — and ends at different weights. On this convex toy the loss barely notices, 0.003352 against 0.003350; on a policy late in training, a jump back to the peak learning rate can undo much of what the schedule's decay achieved. In both cases the result is no longer the run that the config describes.

> **Checkpoint, defined.** A **checkpoint** is *the saved state from which a training run continues exactly as if it had not stopped* — the run's complete state at one step boundary, not a copy of the model. Four defining conditions. It is **complete**: every quantity the next step reads — weights, optimizer moments, the step counter, every random-number generator's state, the data position — and the versions that interpret them. It is taken **at a step boundary**, never during an update. It is **written atomically**, under a temporary name renamed over the old one, so the previous checkpoint stays valid until the new one is whole. And it is **durable**: on storage that outlives the job and that the next job's node can see.
>
> $$S=b\,N,\qquad C=\frac{S}{\beta_w},\qquad b=\underbrace{4}_{\text{fp32 weights}}+\underbrace{4+4}_{\text{Adam's }m,\ v}\ \big(+\,4\ \text{with an EMA copy}\big)$$
>
> where $N$ is the number of parameters, $b$ the bytes per parameter, $S$ the checkpoint's size, $\beta_w$ the write bandwidth where it is stored and $C$ the time the training stands still while it is written — so a checkpoint's cost grows with the model, not with the data.
>
> - **Example**: FT-1: $S=3.6$ GB and $C=7.2$ s on work. The loop above resumes from its checkpoint bit for bit.
> - **Non-example**: the weights alone. The loop above, resumed from its weights, restarts its schedule at the peak, repeats 400 minibatches, trains 400 extra steps and ends $1.7\times10^{-3}$ away. Saved weights are the checkpoints that [[02-foundations/ml-practice|9. ML Practice §1]] chooses among by validation score — enough to evaluate a model, not to resume a run.
> - **Non-example**: a complete checkpoint on the node's own disk. Every field is there, and the next job, on another node, cannot see it.
> - **Why it matters**: §7's arithmetic assumes that an interruption costs only the unsaved work and a restart; an incomplete checkpoint adds a cost no interval can repair, because the resumed run is a different experiment ([[06-research-practice/experimental-design-reproducibility|2. Experimental Design §6]]).

**The traps.** The weights alone; the node's own disk; a save inside the signal handler; and counting on the 30 s between SIGTERM and SIGKILL at the limit — FT-1's 7.2 s fit on a quiet filesystem, which is not a plan.

> [!note]- Deeper · 더 깊이
> **Will the warning reach Python?** `--signal=USR1@600` sends SIGUSR1 about 600 s before the limit — up to 60 s earlier, the resolution of Slurm's event handling — to every job step and, by default, not to the batch shell; with the `B:` prefix only the batch shell gets it. Whether it reaches your Python process depends on how that process was started — by `srun`, inside a container, under a launcher with worker processes — so test it once on a short job with `scancel --signal=USR1 <jobid>` and look for the handler's line in the log. **Why a rename is safe.** Linux's `rename(2)` replaces an existing name atomically, so no process ever finds it missing, and Python's `os.replace` states that a successful rename is atomic on POSIX systems — within one filesystem; across two it can fail.

### 7. How often to save: the checkpoint interval

*In one sentence:* saving often wastes time writing and saving rarely wastes time redoing, and when interruptions come at random the best interval is the square root of twice the save time times the mean time between interruptions.

**The problem.** On `gpu-preempt`, FT-1 is stopped every 10 h on average. Save every minute and much of the run goes to writing; save every few hours and much of it goes to redoing lost work. Somewhere between is a best interval.

**The idea in plain words.** Two costs pull in opposite directions. Each save costs $C$, so saving's share of the run falls like $1/\tau$. Each interruption throws away the work since the last save — on average half an interval — so the loss grows with $\tau$. The best interval balances the two, and at the best interval they turn out to be exactly equal.

**The rule.** Let interruptions arrive independently, at a constant mean spacing $M$ — a Poisson process, whose gaps are exponential with mean $M$ ([[02-foundations/probability|3. Probability §2]]). Per hour of training, saving costs $C/\tau$; interruptions arrive at the rate $1/M$ and each loses $\tau/2$ on average, while $C\ll\tau\ll M$ so that a segment rarely sees two. The fraction of $W$ wasted is therefore

$$w(\tau)=\frac{C}{\tau}+\frac{\tau}{2M}$$

since the first term falls as saves grow rarer and the second rises as the unsaved stretch grows. Setting its derivative to zero, $-C/\tau^2+1/(2M)=0$ ([[02-foundations/engineering-math|0.5 §1]]), gives the interval in the box. This is the classical first-order analysis that the checkpointing literature attributes to Young and to Daly (Aupy et al., 2013); the page derives it rather than quoting them.

> **Checkpoint interval, defined.** The **checkpoint interval** $\tau$ is *the training time between two saves* — a choice the job makes, trading time spent saving against work lost to interruptions; not a property of the cluster. Four defining conditions for its first-order optimum. Interruptions are **random and memoryless**: independent, at a constant mean spacing $M$. A save **costs a fixed $C$**, during which training stands still. An interruption **loses exactly the work since the last completed save**, which a complete checkpoint (§6) guarantees. And **$C\ll\tau\ll M$**, so a segment almost never sees two interruptions and, when it sees one, loses half of itself on average.
>
> $$\tau^\star=\sqrt{2CM},\qquad w(\tau^\star)=\sqrt{\frac{2C}{M}},\qquad \frac{C}{\tau^\star}=\frac{\tau^\star}{2M}=\sqrt{\frac{C}{2M}}$$
>
> where $\tau^\star$ minimizes $w(\tau)=C/\tau+\tau/2M$ — so at the optimum the two wastes are equal, each half of the total, and the interval depends on $C$ and $M$ only through their product, the waste only through their ratio.
>
> - **Example**: FT-1 on `gpu-preempt`: $C=7.2$ s $=0.002$ h and $M=10$ h give $\tau^\star=\sqrt{0.04}=0.2$ h $=12$ min and $w=0.02$ — over 50 h, 0.50 h spent saving and 0.50 h of lost work, to first order.
> - **Non-example**: the 48 h limit. It is not random — you know when it comes — so it is not an $M$: the answer to it is §6's save on the warning, which loses nothing, not a shorter $\tau$.
> - **Non-example**: "every minute, to be safe". Saving alone then costs $C/\tau=0.002/0.0167=12\%$ of the run, 6 h of FT-1's 50 — six times the waste at $\tau^\star$.
> - **Why it matters**: the minimum is flat and the ends are steep, so the rule's job is to rule out the intervals that are wrong by ten times; and it says what can be bought — halving $C$ (a faster filesystem, a smaller checkpoint) or doubling $M$ (a quieter partition) cuts the waste by a factor of $\sqrt2$.

**The exact model.** The first-order rule assumes at most one interruption per segment and forgets the time it takes to come back. Counting both is a short calculation. Take one segment, $\tau$ of training and its save, $s=\tau+C$. It runs without interruption with probability $e^{-s/M}$, so the number of interruptions before a clean run is geometric, with mean $(1-e^{-s/M})/e^{-s/M}=e^{s/M}-1$ ([[02-foundations/engineering-math|0.5 §5]]). Each interruption costs the time already spent in the segment — given that it came before $s$, $M-s/(e^{s/M}-1)$ on average, which is $\int_0^s x\,e^{-x/M}\,dx/M$ integrated by parts and divided by the probability $1-e^{-s/M}$ that it came before $s$ — plus a restart $R$: the queue wait, re-staging and reloading, $0.2+0.0500+0.0010=0.2510$ h for FT-1. Adding the clean run's $s$,

$$E[T_{\text{seg}}]=s+\big(e^{s/M}-1\big)\Big(M-\frac{s}{e^{s/M}-1}+R\Big)=\big(e^{s/M}-1\big)\big(M+R\big)$$

because the two $s$ terms cancel; the whole run takes $E[T]=(W/\tau)(M+R)(e^{(\tau+C)/M}-1)$. Expanding $e^x-1\approx x+x^2/2$ ([[02-foundations/engineering-math|0.5 §2]]) with $x=(\tau+C)/M$: the linear term gives $W(1+C/\tau)(1+R/M)$, the square term adds about $W\tau/2M$, and together they make $W(1+C/\tau+\tau/2M+R/M)$ plus smaller terms: the first-order waste, plus the restarts, $R/M$ of the run, which no choice of $\tau$ touches.

**On the object.** At $\tau=12$ min, $E[T]=250\times10.2510\times(e^{0.0202}-1)=52.29$ h: 0.50 h saving, 0.51 h lost work and 1.28 h of restarts over 5.10 expected preemptions. §11 finds the exact optimum at 11.92 min, where the overhead rounds to the same 2.29 h.

| interval $\tau$ | expected time (h) | saving (h) | lost work (h) | restarts (h) |
|---|---:|---:|---:|---:|
| every 3 min | 53.44 | 2.00 | 0.14 | 1.31 |
| $\tau^\star=12$ min | 52.29 | 0.50 | 0.51 | 1.28 |
| every epoch, 19.5 min | 52.42 | 0.31 | 0.83 | 1.28 |
| every 10 epochs, 3.26 h | 60.62 | 0.03 | 9.11 | 1.48 |
| only at the end | 1,511.44 | 0.00 | 1,424.43 | 37.01 |

**The traps.** Saving "every N epochs" by habit, without asking how long N epochs take: every 10 epochs is 3.26 h, and costs 8.3 h more than $\tau^\star$. Never saving: FT-1 then needs one clean 50 h stretch on a partition that preempts every 10 h, $e^{5}-1=147$ interruptions are expected first, and the run takes 63 days — checkpointing is what makes a preemptible partition usable at all. And expecting a small $\tau$ to fix everything: the 1.28 h of restarts are paid per interruption, and only a smaller $R$ or a larger $M$ lowers them.

> [!note]- Deeper · 더 깊이
> **What preemption sends.** When Slurm selects a job for preemption it sets the job's end to now plus the grace time, sends SIGCONT and SIGTERM at once, and sends SIGCONT, SIGTERM and SIGKILL when that end arrives; the grace time is zero unless the site sets one. Whether the job is then cancelled, requeued or suspended is the site's `PreemptMode` (Slurm, preemption); a requeued batch job starts its script again from the beginning, with the same job ID — which is why a script that resumes from `latest` is also the right script for a requeue. **The exact optimum** sits 0.08 min, 4.8 s, below $\tau^\star$ for every $M$ in §11's sweep. **On `gpu`** the random interruptions are node failures, much rarer than preemptions: §11's column for $M=160$ h puts $\tau^\star$ at 48 min.

### 8. Getting data to the GPUs: staging and the input pipeline

*In one sentence:* four GPUs that consume 1,024 samples a second starve if the data cannot arrive that fast, and the same 180 GB takes 3 minutes or 33 to copy, and trains in 50 hours or 77, depending only on how many files it is split into — because every file costs a metadata request that bytes do not.

**The problem.** FT-1's four GPUs consume 1,024 samples a second — 3,072 images, 153.6 MB — for 50 hours, and the corpus sits on a filesystem shared with everyone.

**The idea.** A file costs two things: a request to open it, and then its bytes. For small files the requests are the slow part. So store the corpus as a few large **shards**, copy them once at the start of each job to the node's own disk — **staging** — and let training read locally. Slurm moves no file for a job but its script, so the copy is a line of the script (§4). And remember that the whole pipeline runs at the pace of its slowest stage.

**The rules.** Staging $n$ files of $B$ bytes in all takes

$$t_{\text{stage}}=\frac{n}{r_f}+\frac{B}{\beta_r}$$

because each file costs one open at the rate $r_f$ and the bytes stream at $\beta_r$; below $\beta_r/r_f=500$ kB per file on the course cluster, the file count and not the size sets the time. Once training runs, the input pipeline has to keep up:

> **Input-pipeline throughput, defined.** The **input throughput** of a training job is *the rate at which its data loader delivers ready samples* — the smallest of several independent caps, set by where the data is read from and how it is stored; not a property of the GPU. Three defining conditions. **Every stage caps it**: the files opened per second divided by the files per sample, the read bandwidth divided by the bytes per sample, and the rate at which the allocated CPU cores decode samples. The GPUs **consume at a fixed rate** $r_{\text{need}}$, the batch divided by the step's compute time. And **what the pipeline cannot deliver, the GPUs wait for**: a step takes its compute time or the time its batch takes to arrive, whichever is longer.
>
> $$r_{\text{in}}=\min\Big(\frac{r_f}{f},\ \frac{\beta}{s},\ r_{\text{cpu}}\Big),\qquad u=\min\Big(1,\ \frac{r_{\text{in}}}{r_{\text{need}}}\Big),\qquad t_{\text{train}}=\frac{W}{u}$$
>
> where $f$ is the files per sample, $s$ the bytes per sample, $\beta$ the bandwidth of wherever the data is read from, $r_{\text{cpu}}$ the decoding rate and $u$ the fraction of the time the GPUs are busy — so the slowest stage sets the pace, and a GPU faster than it only waits longer.
>
> - **Example**: FT-1 reading small files in place: $r_f/f=2{,}000/3=666.7$ samples/s against $\beta/s=10^9/150{,}000=6{,}667$, so $r_{\text{in}}=666.7$ and $u=666.7/1{,}024=0.651$. Each step takes $0.25/0.651=0.384$ s, 0.134 s of it waiting for data, and 50 h of training become 76.8 h. From staged shards the byte cap is $2\times10^9/150{,}000=13{,}333$ samples/s, so $u=1$ if the cores keep up.
> - **Non-example**: a faster GPU for the small-file layout. It raises $r_{\text{need}}$, lowers $u$, and leaves the 76.8 h where they were.
> - **Why it matters**: it is the most common reason a training job's GPUs sit partly idle, and the one that §9's utilization reading warns about.

**On the object.** Staging 200 shards takes $200/2{,}000+180=180.1$ s, 3.0 min; one file per image, $3{,}600{,}000/2{,}000+180=1{,}980$ s, 33.0 min — the same bytes, eleven times the time, paid again after every preemption, so §7's restart $R$ grows from 15.06 to 45.06 min. Shards keep the GPUs busy even read in place, since the bytes were never the problem; but then every epoch goes back to the shared filesystem, $153.6\times180$ GB $=27.6$ TB of reads over the run, on servers everyone shares.

**The traps.**

- *One file per sample, or per image.* The quota refuses it (§2), staging takes eleven times as long, and in place it starves the GPUs.
- *Forgetting `--cpus-per-task`.* Slurm allocates one processor per task unless told otherwise. Where a site confines a job to its allocated cores, the loader's worker processes then all share one core, and $r_{\text{cpu}}$ becomes the cap however the data is stored.
- *"Staging" to scratch.* It is the same shared filesystem with the same metadata servers; the files have only moved.

A shard is any file that packs many samples — a `tar` archive of an episode's images, an HDF5 file, a Parquet file; which format to use is a separate question. The loader opens 200 files instead of 3,600,000 and reads each front to back.

> [!note]- Deeper · 더 깊이
> **Seen on a laptop.** The same effect shows up, smaller, even on a laptop's internal SSD. A miniature corpus of 30,000 files of 5 kB (150 MB) was copied with `rsync` five times, removing the copy between trials, and so was one `tar` archive of the same files — on the macOS laptop this page was written on. `--no-xattrs --no-mac-metadata` keep macOS's own `tar` from storing file attributes; GNU `tar` on Linux stores none unless asked with `--xattrs`.
>
> ```bash
> find many -type f | wc -l                                          # 30000
> tar --no-xattrs --no-mac-metadata -cf manyshards/all.tar -C many .
> /usr/bin/time -p rsync -a many/ local/many/
> /usr/bin/time -p rsync -a manyshards/ local/manyshards/
> ```
>
> | trial | 30,000 files (s) | one 169 MB archive (s) | ratio |
> |---:|---:|---:|---:|
> | 1 | 49.78 | 4.56 | 10.9 |
> | 2 | 37.10 | 2.76 | 13.4 |
> | 3 | 31.54 | 2.59 | 12.2 |
> | 4 | 11.80 | 1.41 | 8.4 |
> | 5 | 11.08 | 1.30 | 8.5 |
>
> The times are the `real` line of each `time -p`, the rest trimmed. They moved fourfold with whatever else the laptop was doing; within every trial the files took 8 to 13 times as long. A laptop is not a parallel filesystem and these are not the course cluster's numbers; the direction is the same.

### 9. Watching a running job

*In one sentence:* a job that runs for days must be checked without being disturbed — through its queue state, its log, its GPUs and its accounting record — and a GPU utilization well below 100% warns that the time is going somewhere other than the GPU.

**The problem.** A job has run for six hours. Is it healthy, and is it fast?

**The idea.** Four windows. The queue: `squeue --me`, state and reason (§4). The log: every 100 steps FT-1's script prints the step, the loss, the samples per second and the seconds per step spent waiting for data — the one number that tells §8's starvation apart from everything else. The GPUs: one line in the batch script, before `srun`, logs every GPU's utilization once a minute. And afterwards `sacct`: `OUT_OF_MEMORY` with `MaxRSS` near the request means more memory or smaller loads; `TIMEOUT` means the chain of §5 was needed. The GPU lines, from NVIDIA's `nvidia-smi` documentation, not run here:

```bash
nvidia-smi dmon -s u -d 60 > "logs/gpu-$SLURM_JOB_ID.log" &    # utilization of every GPU, once a minute
nvidia-smi -q -d UTILIZATION                                    # one detailed reading
```

Logging from inside the job is the dependable way; a step started from outside with `srun --jobid=<id>` can wait behind the job's own step, because Slurm's job steps have been exclusive by default since version 20.11 (Slurm FAQ).

> **GPU utilization, defined.** The **GPU utilization** that `nvidia-smi` reports is *the percentage of a recent sample period during which one or more kernels were executing on the GPU* — a measure of time, not of work; the period is between 1/6 s and 1 s, depending on the product (NVIDIA, `nvidia-smi` documentation). Three defining conditions. It is **all or nothing at each instant**: a kernel that keeps a small part of the GPU busy counts as fully as one that fills it. It is **an average over the sample period**, so gaps shorter than the period blur into it. And it is **silent about causes**: an idle GPU looks the same whether it waits for data, for the host, or for nothing.
>
> $$U=\frac{t_{\text{kernel}}}{t_{\text{sample}}}\times100\%,\qquad U\le u\times100\%\ \ \text{when the input pipeline caps the steps}$$
>
> where $t_{\text{kernel}}$ is the time within the period $t_{\text{sample}}$ with at least one kernel executing and $u$ is §8's busy fraction — so a starved input shows as a utilization at or below $u$, while a full reading says only that kernels were running.
>
> - **Example**: FT-1 reading small files in place: each 0.384 s step spends 0.134 s waiting for data, $u=0.651$, so the four GPUs cannot read above 65%.
> - **Non-example**: 100% read as "the GPU is used well". A kernel far below its roofline — memory-bound, or too small to fill the GPU — keeps the reading at 100% while most of the arithmetic idles ([[03-deep-learning/foundations/gpu-computing|1.4 §3]]).
> - **Why it matters**: it is the cheapest alarm there is — a job at 65% leaks a third of its allocation — and the leak is almost always outside the GPU.

**The trap.** Blaming the data by reflex. Launch overhead and host synchronizations also leave gaps between kernels ([[03-deep-learning/foundations/gpu-computing|1.4 §4 and §7]]); the log's data-wait column tells input starvation apart from those. FT-1 reading small files waits 0.134 s of each 0.384 s step — the whole 35%.

### 10. More GPUs, rented GPUs, and a shared machine

*In one sentence:* when four GPUs are too few or the queue too long, more GPUs multiply the rate at which data must arrive, rented GPUs trade the queue for a bill, and a machine shared with others asks you to take only what you use.

**The problem.** A deadline can make FT-1's 72.60 h to a trained policy on `gpu` too long, and a larger policy can outgrow four GPUs. The two ways out — more GPUs, or rented ones — each move a number this page has computed, and either way the machine you share asks something of you.

**More GPUs.** FT-1 already trains on four, data parallel: `torchrun` starts one worker process per GPU, each with its own replica of the policy and 64 of the batch's 256 samples. PyTorch's `DistributedDataParallel` copies rank 0's state to every replica when it is built, and during the backward pass averages the gradients across processes, bucket by bucket, so every replica takes the same step. The replicas stay identical, so one process — rank 0, the first of the numbered workers — writes the checkpoint. Each GPU holds the full model states, 16 bytes per parameter or 4.8 GB for FT-1, until a sharding method divides them ([[03-deep-learning/foundations/training-at-scale|1.3 §5]]). What scales with the GPUs is the input: eight GPUs consume 2,048 samples/s, and the small-file layout would feed them 32.6% of the time. Several nodes add `--nodes=2`, a launcher on each and the network between them — beyond this page.

**Rented GPUs.** A cloud GPU has no queue in the cluster's sense — when capacity is available, an instance starts on request — and it is charged for every hour it is allocated, busy or idle. At the course price of USD 2.00 per GPU-hour, FT-1 costs USD 405 as staged shards (202.4 GPU-hours, §11) and USD 621 as small files read in place (310.3): the slow layout's 108 extra GPU-hours become USD 216 on the bill, and storage and data transfer may be billed on top. Capacity that the provider can take back, often sold at a discount, behaves like `gpu-preempt`: §7 applies with the provider's $M$. The course cluster's 20 h wait for a 48 h job is what the money buys back.

**A shared machine.**

- Nothing heavy on a login node (§1); test in a short interactive allocation (§5).
- Ask for what you use: a job holding four GPUs and using one keeps three from others and spends your fair share.
- Do not poll the scheduler in a loop (§4); use `--mail-type`.
- Clean scratch after a project, and keep one copy of a corpus, not one per experiment.
- Log in with an SSH key protected by a passphrase; never share an account or a key; never write a password or an access token into a job script, a log, a notebook or a repository — job scripts and logs sit on a shared filesystem, where file permissions, not intentions, decide who reads them.

### Worked case · 대상으로 한 번 끝까지

FT-1 from submission to a trained policy, in six steps; each goes from symbols to rule to numbers, and §11 prints every number.

**Step 1 — the budget.** Training time is steps times step time, and the allocation is GPUs times that:

$$W=n_{\text{steps}}\,t_{\text{step}}=720{,}000\times0.25\ \text{s}=180{,}000\ \text{s}=50\ \text{h},\qquad G\,W=4\times50=200\ \text{GPU-hours}$$

since each step takes 0.25 s on the four GPUs together. That is $720{,}000\times256/1{,}200{,}000=153.6$ epochs of 19.5 min, and the GPUs consume $r_{\text{need}}=256/0.25=1{,}024$ samples/s, 153.6 MB/s.

**Step 2 — the layout against the quota (§2).** $B=1{,}200{,}000\times3\times50$ kB $=180$ GB $\le1$ TB holds. One file per image is $n=3{,}600{,}000>1{,}000{,}000$ and fails; 200 shards is $n=200$ and fits.

**Step 3 — staging and the input rate (§8).** $t_{\text{stage}}=n/r_f+B/\beta_r$ is $1{,}800+180=1{,}980$ s $=33.0$ min for the small files and $0.1+180=180.1$ s $=3.0$ min for the shards: the bytes cost 180 s either way, and the other 30 minutes are file opens. Read in place, the small files deliver $r_{\text{in}}=\min(2{,}000/3,\ 10^9/150{,}000)=666.7$ samples/s, so $u=0.651$ and training takes $50/0.651=76.8$ h; staged shards deliver 13,333 samples/s, $u=1$, 50 h.

**Step 4 — windows on `gpu` (§5).** A window pays $o=0.0510$ h and saves 7.2 s after each 12 min, so it holds $w=(48-0.0510)\times0.2/0.202=47.47$ h of training, and FT-1 needs $k=\lceil50/47.47\rceil=2$ windows: 48 h, then $0.0510+(50-47.47)\times1.01=2.60$ h — $4\times50.60=202.4$ GPU-hours. The small files read in place need 76.8 h of training: two windows, 48 h and 29.57 h, 310.3 GPU-hours. The layout alone costs 108 GPU-hours.

**Step 5 — the interval on `gpu-preempt` (§6–§7).** $C=S/\beta_w=3.6/0.5=7.2$ s $=0.002$ h. With $M=10$ h,

$$\tau^\star=\sqrt{2CM}=\sqrt{2\times0.002\times10}=0.2\ \text{h}=12\ \text{min},\qquad w(\tau^\star)=\sqrt{2C/M}=0.02$$

because saving and lost work are equal there, 1% each. The exact model, with $R=0.2510$ h, gives $E[T]=250\times10.2510\times(e^{0.0202}-1)=52.29$ h over 5.10 expected preemptions. Saving every 10 epochs would give 60.62 h, and never saving 1,511 h.

**Step 6 — which partition.** On `gpu`: 20 h in the queue, the 48 h window, 2 h for the 3 h window to backfill, and its 2.60 h — 72.60 h to a trained policy. On `gpu-preempt`: 0.2 h in the queue and 52.29 h expected — 52.49 h, and 95% of 4,000 simulated runs (§11) finish within 53.70 h of starting. The preemptible partition returns FT-1 20 h sooner, and only because it checkpoints every 12 minutes. The waits are course numbers; at your site the comparison is yours to make with its numbers.

### 11. The lab: budget, layout, windows and the checkpoint interval

Every number in the lecture and the Worked case has to come from one place that anyone can rerun and check. Six parts on the frozen objects, printed by one block of NumPy and the standard library: the budget; the two layouts against the quota and their staging times; the input rates and busy fractions; the windows on `gpu` with GPU-hours and the course price; the checkpoint interval — the named intervals, a sweep over $\tau$ and $M$, the exact optimum for each $M$, and 4,000 simulated runs that check the exact formula; and the time to a trained policy on each partition. There is no timing anywhere: every number is the model's, so the output is the same on any machine.

```python
# 12.7 lab: FT-1 on the course cluster - budget, data layout, windows, checkpoint interval. NumPy + stdlib.
import math
import numpy as np

# --- 0. the frozen numbers (Running object): course numbers, decimal units (1 GB = 1e9 bytes) -------
N_PARAM, B_PER_PARAM = 3.0e8, 12              # parameters; checkpoint bytes per parameter
STEPS, BATCH, T_STEP, GPUS = 720_000, 256, 0.25, 4   # optimizer steps, samples/step, s/step when fed, GPUs
EPISODES, PER_EP, FILES_PER_SAMPLE, B_IMG = 2000, 600, 3, 50e3   # corpus; one 50 kB image per camera
SHARDS = 200                                  # ten episodes per shard file
FS_READ, FS_WRITE, FS_FILES = 1.0e9, 0.5e9, 2000     # shared filesystem, per node: B/s, B/s, files/s
LOCAL_READ = 2.0e9                            # node-local NVMe, B/s
WORK_QUOTA = (1.0e12, 1_000_000)              # work: bytes, files
LIMIT, TAU = 48.0, 0.2                        # h: wall-time limit; FT-1's checkpoint interval (12 min)
M_PRE, Q_PRE = 10.0, 0.2                      # gpu-preempt: mean h between preemptions; queue wait per start
Q_LONG, Q_SHORT = 20.0, 2.0                   # gpu: queue wait for a 48 h request, for a 3 h one (backfill)
PRICE = 2.00                                  # USD per GPU-hour: a course number, not a quote
H = 3600.0                                    # seconds per hour

# --- 1. the budget -------------------------------------------------------------------------------------
W = STEPS * T_STEP / H                        # hours of training when the input keeps up
NEED = BATCH / T_STEP                         # samples per second the four GPUs consume
N_SAMPLES = EPISODES * PER_EP
B_SAMPLE = FILES_PER_SAMPLE * B_IMG
DATA = N_SAMPLES * B_SAMPLE
print("1. W = %.1f h on %d GPUs = %.0f GPU-hours; %.1f epochs of %.1f min; %.0f samples/s = %.1f MB/s needed"
      % (W, GPUS, GPUS * W, STEPS * BATCH / N_SAMPLES, N_SAMPLES / NEED / 60, NEED, NEED * B_SAMPLE / 1e6))

# --- 2. two layouts of the same corpus: the quota and the staging time ------------------------------------
def stage_time(n_files, n_bytes, files_per_s=FS_FILES, bw=FS_READ):
    """Seconds to copy from the shared filesystem: one metadata cost per file, then the bytes."""
    return n_files / files_per_s + n_bytes / bw

LAYOUTS = (("one file per image", N_SAMPLES * FILES_PER_SAMPLE), ("200 shards", SHARDS))
for name, n in LAYOUTS:
    fits = DATA <= WORK_QUOTA[0] and n <= WORK_QUOTA[1]
    print("2. %-18s %9d files, %5.1f GB, fits work's quota: %-5s  staging %6.1f s = %4.1f min"
          % (name, n, DATA / 1e9, fits, stage_time(n, DATA), stage_time(n, DATA) / 60))

# --- 3. the input pipeline: the slowest cap sets the rate, the rate sets the GPUs' busy fraction ----------
def input_rate(files_per_sample, bw, files_per_s=None):
    """Samples per second the loader can deliver: capped by file opens (if any) and by bytes."""
    caps = [bw / B_SAMPLE]
    if files_per_s is not None:
        caps.append(files_per_s / files_per_sample)
    return min(caps)

for name, rate in (("small files, read in place", input_rate(FILES_PER_SAMPLE, FS_READ, FS_FILES)),
                   ("shards, read in place", input_rate(1 / 6000, FS_READ, FS_FILES)),
                   ("shards, staged to NVMe", input_rate(1 / 6000, LOCAL_READ))):
    busy = min(1.0, rate / NEED)
    print("3. %-27s %8.1f samples/s, GPUs busy %5.1f%%, training %5.1f h, data wait %.3f s per step"
          % (name, rate, 100 * busy, W / busy, T_STEP / busy - T_STEP))

# --- 4. windows under the 48 h limit on gpu, the GPU-hours charged and the price ---------------------------
C = N_PARAM * B_PER_PARAM / FS_WRITE / H      # hours to write one checkpoint
LOAD = N_PARAM * B_PER_PARAM / FS_READ / H    # hours to read it back

def windows(w_train, start, limit=LIMIT, tau=TAU, c=C):
    """Elapsed hours of each window: pay `start`, then train, pausing c after every tau of training."""
    full = (limit - start) * tau / (tau + c)  # training hours one whole window holds
    k = math.ceil(w_train / full)
    return [limit] * (k - 1) + [start + (w_train - (k - 1) * full) * (tau + c) / tau], full

for name, w_train, start in (("shards, staged", W, stage_time(SHARDS, DATA) / H + LOAD),
                             ("small files, read in place",
                              W * NEED / input_rate(FILES_PER_SAMPLE, FS_READ, FS_FILES), LOAD)):
    el, full = windows(w_train, start)
    print("4. %-26s a window holds %.2f h of training: %d windows, %s h, %.1f GPU-hours, USD %.0f"
          % (name, full, len(el), " + ".join("%.2f" % e for e in el), GPUS * sum(el), PRICE * GPUS * sum(el)))

# --- 5. the checkpoint interval under preemption (gpu-preempt) ---------------------------------------------
R = Q_PRE + stage_time(SHARDS, DATA) / H + LOAD   # hours from a preemption to training again

def expected(tau, M, w=W, c=C, r=R):
    """Exact expectation, interruptions Poisson with mean spacing M: w/tau segments of tau + c hours, each
    retried until it runs clean; an interruption loses the partial segment and pays r.
    Returns (total, saving, lost work, restarts, interruptions)."""
    s = tau + c
    n_seg = w / tau
    fails = math.expm1(s / M)                 # expected interruptions per segment, e^(s/M) - 1
    lost_each = M - s / fails                 # mean time into a segment when it is interrupted
    saving, lost, restarts = n_seg * c, n_seg * fails * lost_each, n_seg * fails * r
    return w + saving + lost + restarts, saving, lost, restarts, n_seg * fails

tau_star = math.sqrt(2 * C * M_PRE)
print("5. C = %.1f s, load %.1f s, R = %.2f min; first order: tau* = %.2f min, waste %.2f%%"
      % (C * H, LOAD * H, R * 60, 60 * tau_star, 100 * math.sqrt(2 * C / M_PRE)))
epoch = N_SAMPLES / NEED / H
for name, tau in (("every 3 min", 0.05), ("tau* = 12 min", tau_star), ("every epoch", epoch),
                  ("every 10 epochs", 10 * epoch), ("only at the end", W)):
    T, sv, lo, rs, k = expected(tau, M_PRE)
    print("   %-15s %8.3f h: expected %8.2f h = 50 + saving %5.2f + lost %7.2f + restarts %5.2f (%.2f interruptions)"
          % (name, tau, T, sv, lo, rs, k))

MS, TAUS = (2.5, 10.0, 40.0, 160.0), (3, 6, 12, 30, 60, 120, 240)
print("   overhead T - W in hours, lost work in brackets; rows tau (min), columns M (h)")
for tm in TAUS:
    print("   %4d  " % tm + "  ".join("%6.2f (%5.2f)" % (expected(tm / 60, M)[0] - W, expected(tm / 60, M)[2])
                                     for M in MS))

def best_tau(M, lo=1e-3, hi=10.0):
    """Golden-section search for the exact optimum, on log(tau)."""
    a, b, g = math.log(lo), math.log(hi), (math.sqrt(5) - 1) / 2
    for _ in range(200):
        c1, c2 = b - g * (b - a), a + g * (b - a)
        a, b = (a, c2) if expected(math.exp(c1), M)[0] < expected(math.exp(c2), M)[0] else (c1, b)
    return math.exp((a + b) / 2)

for M in MS:
    t1, te = math.sqrt(2 * C * M), best_tau(M)
    print("   M = %5.1f h: tau* %5.2f min (exact optimum %5.2f), overhead %5.2f h (%5.2f), %5.2f interruptions"
          % (M, 60 * t1, 60 * te, expected(t1, M)[0] - W, expected(te, M)[0] - W, expected(te, M)[4]))

def life(tau, M, rng, w=W, c=C, r=R):
    """One simulated run of the job: hours until w hours of training are saved."""
    t, done = 0.0, 0.0
    while done < w - 1e-9:
        seg = min(tau, w - done)
        x = -M * math.log(1.0 - rng.random())      # hours to the next interruption, exponential with mean M
        if x >= seg + c:
            t, done = t + seg + c, done + seg
        else:
            t += x + r                               # the unsaved part is lost, then the restart
    return t

rng = np.random.default_rng(12)
lives = np.array([life(TAU, M_PRE, rng) for _ in range(4000)])
print("   4,000 simulated runs: mean %.2f h (standard error %.2f), exact %.2f h, 95th percentile %.2f h"
      % (lives.mean(), lives.std(ddof=1) / math.sqrt(lives.size), expected(TAU, M_PRE)[0],
         np.percentile(lives, 95)))

# --- 6. time to a trained policy: the 48 h partition against the preemptible one ---------------------------
el, _ = windows(W, stage_time(SHARDS, DATA) / H + LOAD)
print("6. gpu: %.1f + %.2f + %.1f + %.2f = %.2f h;  gpu-preempt: %.1f + %.2f = %.2f h (expected)"
      % (Q_LONG, el[0], Q_SHORT, el[1], Q_LONG + el[0] + Q_SHORT + el[1],
         Q_PRE, expected(TAU, M_PRE)[0], Q_PRE + expected(TAU, M_PRE)[0]))
```

**Parts 1–3, the budget, the layouts and the input:** $W=50.0$ h on 4 GPUs, 200 GPU-hours, 153.6 epochs of 19.5 min, and 1,024 samples/s, 153.6 MB/s, needed.

| layout | files | GB | fits work's quota | staging |
|---|---:|---:|---|---:|
| one file per image | 3,600,000 | 180.0 | no | 1,980.0 s = 33.0 min |
| 200 shards | 200 | 180.0 | yes | 180.1 s = 3.0 min |

| read from | samples/s | GPUs busy | training (h) | data wait per step (s) |
|---|---:|---:|---:|---:|
| small files, in place | 666.7 | 65.1% | 76.8 | 0.134 |
| shards, in place | 6,666.7 | 100.0% | 50.0 | 0.000 |
| shards, staged to the node | 13,333.3 | 100.0% | 50.0 | 0.000 |

**Part 4, the windows:**

| layout | training a window holds (h) | windows | elapsed (h) | GPU-hours | at USD 2.00 |
|---|---:|---:|---|---:|---:|
| shards, staged | 47.47 | 2 | 48.00 + 2.60 | 202.4 | 405 |
| small files, read in place | 47.52 | 2 | 48.00 + 29.57 | 310.3 | 621 |

**Part 5, the checkpoint interval:** $C=7.2$ s, loading 3.6 s, $R=15.06$ min, and to first order $\tau^\star=12.00$ min with a waste of 2.00%; the named intervals are §7's table. The sweep gives the expected overhead $E[T]-W$ in hours, with the lost work in brackets:

| $\tau$ \ $M$ | 2.5 h | 10 h | 40 h | 160 h |
|---:|---:|---:|---:|---:|
| 3 min | 7.82 (0.54) | 3.44 (0.14) | 2.36 (0.03) | 2.09 (0.01) |
| 6 min | 7.28 (1.05) | 2.55 (0.26) | 1.39 (0.07) | 1.10 (0.02) |
| 12 min | 7.88 (2.10) | 2.29 (0.51) | 0.95 (0.13) | 0.61 (0.03) |
| 30 min | 11.18 (5.40) | 2.77 (1.28) | 0.83 (0.32) | 0.36 (0.08) |
| 60 min | 17.82 (11.53) | 4.02 (2.60) | 1.05 (0.63) | 0.34 (0.16) |
| 120 min | 34.41 (26.66) | 6.80 (5.36) | 1.65 (1.27) | 0.44 (0.31) |
| 240 min | 86.07 (73.63) | 13.06 (11.49) | 2.94 (2.59) | 0.74 (0.63) |

| $M$ (h) | $\tau^\star$, first order (min) | exact optimum (min) | overhead at $\tau^\star$ (h) | at the exact optimum (h) | interruptions |
|---:|---:|---:|---:|---:|---:|
| 2.5 | 6.00 | 5.92 | 7.28 | 7.28 | 20.82 |
| 10 | 12.00 | 11.92 | 2.29 | 2.29 | 5.10 |
| 40 | 24.00 | 23.92 | 0.82 | 0.82 | 1.26 |
| 160 | 48.00 | 47.92 | 0.33 | 0.33 | 0.31 |

4,000 simulated runs at $\tau=12$ min and $M=10$ h take 52.29 h on average (standard error 0.01 h), against the exact 52.29 h, with a 95th percentile of 53.70 h.

**Part 6, the time to a policy:** on `gpu`, $20.0+48.00+2.0+2.60=72.60$ h; on `gpu-preempt`, $0.2+52.29=52.49$ h expected.

**Reading the tables.** Four things the lecture predicted and the numbers now show.

- **Files, not bytes, set the data path.** The same 180 GB stages eleven times slower as 3,600,000 files, does not fit work at all, and, read in place, keeps the GPUs 65.1% busy — 26.8 h of training and 108 GPU-hours lost. As shards, the same bytes keep the GPUs busy even read in place.
- **The optimum is flat; the ends are steep.** At $M=10$ h anything from 6 to 30 min costs within 0.5 h of the best; every 10 epochs costs 8.3 h more, never saving 1,459 h more.
- **$\tau^\star$ grows as $\sqrt M$.** 6, 12, 24 and 48 min for $M=2.5$, 10, 40 and 160 h: four times the spacing, twice the interval.
- **The formula and the simulation agree, and restarts are the floor.** 52.29 h both ways, 95% of runs within 1.41 h of the mean; at $\tau^\star$ the restarts, 1.28 h, outweigh saving and lost work together, 1.01 h.

### 12. What this page does not cover

A page that tried to cover every scheduler, every site and every scale would teach none of them well; these are left to other pages and to the manuals. Other schedulers — PBS, LSF, Kubernetes-based systems — which express the same ideas with other commands. Training across several nodes in depth, and the sharding methods that [[03-deep-learning/foundations/training-at-scale|1.3 §5]] names. Asynchronous checkpointing libraries and elastic training. Workflow managers that build chains of jobs for you. The GPU's internals and profilers, which are [[03-deep-learning/foundations/gpu-computing|1.4]]. Linux, the shell and `ssh` ([[02-foundations/tools/linux-shell|12.1]]), Git ([[02-foundations/tools/git-research-code|12.2]]), Python environments ([[02-foundations/tools/python-research-code|12.3]]) and data formats ([[02-foundations/tools/config-data-formats|12.4]]), which have their own pages in this track; the data loader's worker processes and the bound Amdahl's law puts on them are [[02-foundations/tools/concurrency|12.8 Concurrency §7 and §9]]. And any one site's policies, which its user guide states.

### After reading

- [ ] Say what runs on a login node and what on a compute node, and why a job gets no GPU unless it asks.
- [ ] Write a batch script for a job of your own, and say why a variable in an `#SBATCH` line is not expanded.
- [ ] Follow a job through `PD`, `R` and its end state, and read a pending reason.
- [ ] Check a dataset against a quota of bytes and files, and say where a corpus, a checkpoint and an environment belong.
- [ ] Cut a run longer than the limit into windows, $k=\lceil W/w\rceil$, chain them with a dependency that survives a timeout, and say why the last window asks for little time.
- [ ] List what a checkpoint must hold, write it atomically, and save it on the warning signal.
- [ ] Derive $\tau^\star=\sqrt{2CM}$ and $E[T]=(W/\tau)(M+R)(e^{(\tau+C)/M}-1)$, and say what $R$ adds that no interval removes.
- [ ] Compute staging time and input throughput from files, bytes and rates, and read a GPU utilization of 65% back to its cause.

### Self-check

1. A job asks for `--partition=gpu --time=48:00:00` and nothing else. What does it get, and what does a training script that uses the GPU "if one is available" do?
2. FT-1 needs 50 h of training and the limit is 48 h. How many windows, how long is the last, what should it ask for, and why does the request matter?
3. On a partition with $M=40$ h, what are FT-1's $\tau^\star$ and first-order waste, and how do they compare with $M=10$ h?
4. A chain of windows built with `afterok` stops after the first. Why, and what are two fixes?
5. `nvidia-smi` reads 65% on all four GPUs. Name two causes, and the one number in the job's log that tells them apart.
6. A checkpoint holds only the model's weights. What is missing, and what does each missing piece do to the resumed run?
7. The same 180 GB stages in 3.0 min as 200 shards and in 33.0 min as 3,600,000 files. Where do the other 30 minutes go, and which limit does the second layout also break?

> [!tip]- Answers
> 1. A share of a node's cores and memory, and no GPU: Slurm allocates GPUs only to jobs that ask, with `--gres` or `--gpus`. The script trains on the CPU, slowly, instead of failing. Add `--gres=gpu:4`, and let a script that expects a GPU stop when it finds none.
> 2. Two: a window holds $(48-0.0510)\times0.2/0.202=47.47$ h, so $k=\lceil50/47.47\rceil=2$, and the last needs 2.60 h. Ask for about 3 h: backfill can fit a short job into a gap before a higher-priority job's planned start, which a 48 h request cannot use — 2 h in the queue instead of 20, in the course numbers.
> 3. $\tau^\star=\sqrt{2\times0.002\times40}=0.4$ h $=24$ min and $w=\sqrt{2\times0.002/40}=0.01$: four times the spacing doubles the interval and halves the waste. The exact overhead is 0.82 h against 2.29 h (§11).
> 4. Window 1 ends in `TIMEOUT`, not in a completion with exit code zero, so `afterok` can never be met and window 2 waits as `DependencyNeverSatisfied`. Use `afterany` or `singleton` — or make every window save on the warning and exit with code zero, which one unclean end then breaks.
> 5. Input starvation — small files, too few cores for the loader (§8) — or host-side gaps from launch overhead and synchronizations ([[03-deep-learning/foundations/gpu-computing|1.4 §4 and §7]]). The seconds per step spent waiting for data tell them apart: 0.134 s of each 0.384 s step for FT-1's small files, the whole 35%.
> 6. Adam's two moments, the step counter, the generators' state, the data position, any EMA copy. Without them Adam restarts its averages, the schedule restarts at its peak and runs extra steps, and the minibatches repeat — in §6's loop, learning rate 0.0500 instead of 0.0327, 400 extra steps, weights $1.7\times10^{-3}$ away.
> 7. Into 3,600,000 opens at 2,000 per second, 1,800 s; the bytes take 180 s either way. The layout also breaks work's file quota, 3,600,000 files against 1,000,000.

### Problem set · 과제

Tier A. Using only this page, its prerequisites, and the two objects frozen above. Every problem changes a knob — the model's size, the step time, the interruption rate, the layout, the script — so none of the page's numbers can be copied.

The variant **FT-2** is FT-1 with a policy four times as large, $N=1.2\times10^9$ ($S=14.4$ GB, $C=28.8$ s), and four times slower per step, $t_{\text{step}}=1.0$ s, for 180,000 steps, so again $W=50$ h; the corpus and the cluster are unchanged.

1. **Draw.** The picture for FT-2 on a partition with $M=2.5$ h: in panel (a), the labels that change; in panel (b), $C/\tau$ and $\tau/2M$ on log-log axes, their sum with its minimum marked, and the exact curve's value at $\tau^\star$. Say why $\tau^\star$ did not move from FT-1's, and what did.
2. **Derive.** (a) From $w(\tau)=C/\tau+\tau/2M$, derive $\tau^\star$ and $w(\tau^\star)$, and show that the two terms are equal at $\tau^\star$. (b) Derive $E[T_{\text{seg}}]=(e^{s/M}-1)(M+R)$ from the geometric number of interruptions and the mean time into a segment at which an interruption comes, and expand it for $s\ll M$ to recover the first-order waste plus $R/M$. (c) FT-1 with its small files read in place on `gpu`: the training time, the windows and their lengths, and the GPU-hours. (d) How many samples must a shard hold for FT-1's corpus to use at most 1% of work's file quota, how large is each shard, and how long does staging take?
3. **Do.** Fill the `?` blanks, then run FT-2 at $M=2.5$ h and $M=10$ h. Report $\tau^\star$, the first-order waste, and the expected time at $\tau^\star$ and when saving once per epoch; and the input rate and busy fraction of the small files read in place against staged shards. Compare each with FT-1.
4. **Interpret.** A lab-mate submits the script below on Friday evening, then chains a second job with `sbatch --dependency=afterok:<id> bc-part2.sbatch`. Before submitting, they ran `python train.py --data . --epochs 1` on the login node for an hour "to check that it starts", and the week before, the job had run fine when submitted from the terminal in which they had activated their environment. On Monday nothing has trained. Name each problem, its symptom, and the fix.

   ```bash
   #!/bin/bash
   #SBATCH --job-name=bc-policy
   #SBATCH --partition=gpu
   #SBATCH --gres=gpu:4
   #SBATCH --time=72:00:00
   #SBATCH --output=$HOME/logs/bc-%j.out
   cd /path/to/scratch/corpus_jpg          # 3,600,000 JPEG files, copied here in May
   python train.py --data . --ckpt-dir /tmp/bc --save-every-epochs 50
   ```

The template for problem 3:

```python
# Problem 3 (Do). FT-2: FT-1's corpus and cluster, a policy four times larger and four times slower per step. Fill every ?.
import math

N_PARAM, B_PER_PARAM = 1.2e9, 12                          # parameters; checkpoint bytes per parameter
STEPS, BATCH, T_STEP, GPUS = 180_000, 256, 1.0, 4         # optimizer steps, samples per step, s per step, GPUs
N_SAMPLES, FILES_PER_SAMPLE, B_SAMPLE, SHARDS = 1_200_000, 3, 150e3, 200
FS_READ, FS_WRITE, FS_FILES, LOCAL_READ = 1.0e9, 0.5e9, 2000, 2.0e9
LIMIT, Q_PRE, H = 48.0, 0.2, 3600.0

W = ?                                                     # h of training when the input keeps up
NEED = ?                                                  # samples per second the GPUs consume
C = ?                                                     # h to write one checkpoint to work
LOAD = N_PARAM * B_PER_PARAM / FS_READ / H                # h to read it back
STAGE = ?                                                 # h to stage the shards: one open per file, then the bytes
print("W = %.1f h, %.0f GPU-hours, need %.0f samples/s; C = %.1f s, load %.1f s, staging %.1f min"
      % (W, GPUS * W, NEED, C * H, LOAD * H, STAGE * 60))

for name, rate in (("small files in place", ?),           # the lower of the file-open cap and the byte cap
                   ("shards staged", LOCAL_READ / B_SAMPLE)):
    busy = ?                                              # the GPUs' busy fraction, at most 1
    print("%-21s %7.1f samples/s, GPUs busy %5.1f%%, training %.1f h" % (name, rate, 100 * busy, W / busy))

def expected(tau, M, w=W, c=C, r=Q_PRE + STAGE + LOAD):
    """Expected hours to finish w hours of training, saving every tau, interruptions of mean spacing M."""
    fails = ?                                             # expected interruptions per segment of tau + c
    return ?                                              # w / tau segments, each costing (M + r) per interruption

tau_ep = N_SAMPLES / NEED / H                             # one epoch, in hours
for M in (2.5, 10.0):
    tau_star = ?                                          # the first-order optimum
    print("M = %4.1f h: tau* %.2f min, waste %.2f%%, expected %.2f h at tau*, %.2f h saving every epoch (%.1f min)"
          % (M, 60 * tau_star, 100 * ?, expected(tau_star, M), expected(tau_ep, M), 60 * tau_ep))
```

> [!note]- How to draw it · 그리는 법
> - Put both axes on log scales, $\tau$ across and the share of $W$ up. There $C/\tau$ is a straight line of slope $-1$ and $\tau/2M$ one of slope $+1$; draw each from its values at two intervals, not by eye.
> - The lines cross at $\tau^\star$, where each equals $w(\tau^\star)/2$; the sum's minimum is directly above the crossing.
> - Multiplying $C$ by 4 and dividing $M$ by 4 lifts both lines by a factor of 4 — the same vertical shift on log axes — so the crossing moves up, not sideways. A change of $C$ alone would move it sideways.
> - Draw the exact curve above the sum and label its value at $\tau^\star$; the gap is mostly $R/M$, the restarts, which no $\tau$ removes.
> - In panel (a), change only what FT-2 changes — the checkpoint's size and save time, and the interval; the staging bars belong to the corpus, which is the same.

> [!tip]- Solutions
> 1. $C=14.4/0.5=28.8$ s $=0.008$ h and $M=2.5$ h, so $CM=0.02$ h², the same as FT-1's $0.002\times10$: $\tau^\star=\sqrt{0.04}=0.2$ h $=12$ min again. The waste is $\sqrt{2\times0.008/2.5}=0.08$, four times FT-1's, because $C/M$ grew sixteenfold and the waste goes as its square root. Both lines rise by a factor of 4 and cross at 4% each; the sum's minimum is 8.0%, and the exact curve is at 19.47% there, about 10.2 points of it $R/M=0.2540/2.5$. Panel (a): a 14.4 GB checkpoint written in 28.8 s every 12 min; the staging bars are unchanged.
> 2. (a) $dw/d\tau=-C/\tau^2+1/(2M)=0$ gives $\tau^\star=\sqrt{2CM}$; then $C/\tau^\star=\sqrt{C/2M}=\tau^\star/2M$, and their sum is $\sqrt{2C/M}$. (b) A segment runs clean with probability $p=e^{-s/M}$, so the interruptions before the first clean run are geometric with mean $(1-p)/p=e^{s/M}-1$; one that comes before $s$ comes on average $M-s/(e^{s/M}-1)$ in, and costs a restart $R$ besides, so $E[T_{\text{seg}}]=s+(e^{s/M}-1)(M-s/(e^{s/M}-1)+R)=(e^{s/M}-1)(M+R)$. With $e^x-1\approx x+x^2/2$ and $W/\tau$ segments, $E[T]\approx W(1+C/\tau+\tau/2M+R/M)$ when $C\ll\tau\ll M$ and $R\ll M$. (c) $u=0.651$, so 76.8 h of training. Without staging a window pays only the 3.6 s load, $o=0.001$ h, and holds $(48-0.001)\times0.2/0.202=47.52$ h; $k=\lceil76.8/47.52\rceil=2$, of 48.00 and $0.001+(76.8-47.52)\times1.01=29.57$ h — 77.57 h elapsed, 310.3 GPU-hours against 202.4. (d) 1% of 1,000,000 is 10,000 files, so at least $1{,}200{,}000/10{,}000=120$ samples, $120\times150$ kB $=18$ MB, per shard. Staging takes $10{,}000/2{,}000+180=185$ s, within 5 s of the 200 shards: past about 500 kB per file, the bytes set the time.
> 3. Blanks: `STEPS * T_STEP / H`, `BATCH / T_STEP`, `N_PARAM * B_PER_PARAM / FS_WRITE / H`, `(SHARDS / FS_FILES + N_SAMPLES * B_SAMPLE / FS_READ) / H`, `min(FS_FILES / FILES_PER_SAMPLE, FS_READ / B_SAMPLE)`, `min(1.0, rate / NEED)`, `math.expm1((tau + c) / M)`, `(w / tau) * (M + r) * fails`, `math.sqrt(2 * C * M)` and `math.sqrt(2 * C / M)`. The output:
>
>    ```text
>    W = 50.0 h, 200 GPU-hours, need 256 samples/s; C = 28.8 s, load 14.4 s, staging 3.0 min
>    small files in place    666.7 samples/s, GPUs busy 100.0%, training 50.0 h
>    shards staged         13333.3 samples/s, GPUs busy 100.0%, training 50.0 h
>    M =  2.5 h: tau* 12.00 min, waste 8.00%, expected 59.73 h at tau*, 72.85 h saving every epoch (78.1 min)
>    M = 10.0 h: tau* 24.00 min, waste 4.00%, expected 53.38 h at tau*, 55.12 h saving every epoch (78.1 min)
>    ```
>
>    At $M=10$ h FT-2's interval is 24 min against FT-1's 12 — $C$ is four times larger and $\tau^\star$ grows as its square root — the waste 4% against 2%, the expected time 53.38 h against 52.29. At $M=2.5$ h the interval is back to 12 min with 8% waste: 59.73 h. FT-2's epoch, 78.1 min, is far past $\tau^\star$, so saving once per epoch costs 13.1 h more at $M=2.5$ h and 1.7 h more at $M=10$ h. And FT-2's slower steps need only 256 samples/s, below the small files' 666.7: the GPUs no longer starve, but the layout is still refused by work's quota and still stages in 33 min after every preemption — the throughput problem went away, the storage problem did not.
> 4. Seven problems, each with its symptom and fix. (1) `--time=72:00:00` on a 48 h partition: pending forever as `PartitionTimeLimit`; ask for 48 h and chain windows. (2) The `--output` line: Slurm does not expand the home-directory variable, so the log never reaches `~/logs`; write the path out, or use `logs/bc-%j.out` with `logs/` made first. (3) No environment in the script: last week it ran on the terminal's inherited environment; from a fresh login it fails at `import`; put the `module` lines or the container in the script. (4) 3,600,000 small files on scratch since May: files unread for 30 days are deleted, and the rest, read in place, keep the GPUs about 65% busy; keep 200 shards on work and stage them. (5) `--ckpt-dir /tmp/bc`: the node's own disk, invisible to the second job's node; checkpoint to work, atomically. (6) `--save-every-epochs 50`: one save per 16.3 h of training even at full speed — 25 h with the small files read in place — so the limit or a preemption can throw away that much; save every 12 min and on a `--signal` warning. (7) `afterok`: the first job ends in `TIMEOUT`, so the second waits forever as `DependencyNeverSatisfied`; use `afterany` or `singleton`. And the hour on the login node shared a machine with every user, without a GPU; the test belongs in a short `salloc`.

### Sources

- SchedMD, *Slurm* documentation, 26.05 ([slurm.schedmd.com](https://slurm.schedmd.com/documentation.html)) — the command pages, `slurm.conf`, the FAQ, and the job-reason, job-array, GRES, preemption, scheduling and multifactor-priority pages: every Slurm option, state, default and behaviour above.
- Apptainer User Guide, 1.5 ([apptainer.org](https://apptainer.org/docs/user/latest/introduction.html)) — security model, SIF, building, `--nv`, bind paths.
- Lmod User Guide ([lmod.readthedocs.io](https://lmod.readthedocs.io/en/latest/010_user.html)) — the `module` commands.
- Lustre wiki, "Introduction to Lustre" ([wiki.lustre.org](https://wiki.lustre.org/Introduction_to_Lustre)) — metadata servers hold names, permissions and layouts; clients read file data from the object storage servers directly.
- NVIDIA, *nvidia-smi* documentation ([docs.nvidia.com](https://docs.nvidia.com/deploy/nvidia-smi/index.html)) — utilization's definition and sample period; `-q -d`, `dmon`.
- PyTorch 2.14 documentation ([docs.pytorch.org](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)) — resuming from a general checkpoint; the DDP design note; `torchrun`.
- Python 3 documentation ([docs.python.org](https://docs.python.org/3/library/signal.html)) — `signal` handlers; `os.replace`. NumPy 2 documentation ([numpy.org](https://numpy.org/doc/stable/reference/random/generator.html)) — `default_rng`, `PCG64.state`.
- Linux man-pages ([man7.org](https://man7.org/linux/man-pages/man2/rename.2.html)) — `rename(2)`, `open(2)`, `errno(3)`, `time(1)`; GNU Bash manual, "The Set Builtin"; rsync manual; GNU tar manual, "Extended File Attributes".
- Aupy, Robert, Vivien & Zaidouni, "Checkpointing algorithms and fault prediction", [arXiv:1302.3752](https://arxiv.org/abs/1302.3752), 2013 — "the classical first-order analysis of Young and Daly".
- Young, *Communications of the ACM* 17(9):530–531, 1974, and Daly, *Future Generation Computer Systems* 22(3):303–312, 2006 — bibliographic data only; the page derives its own results.

## 한국어

*[[02-foundations/ml-practice|9. ML 실무 §6]]과 [[02-foundations/probability|3. 확률 §2]] 위에 선다. 앞의 것은 이 페이지가 남의 기계에서 돌리는 학습 레시피이고, 뒤의 것은 중단 한 번의 값을 매기는 지수분포 대기 시간이다. 공유 클러스터는 책상 위 컴퓨터가 결코 요구하지 않는 세 가지를 요구한다. 대기열, 벽시계 시간 한도, 그리고 수백 명이 함께 쓰는 파일시스템이다. 이 페이지는 그 셋 아래에서 제대로, 그리고 빠르게 학습시키는 법을 다룬다. 노드 안의 GPU 자체는 [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산]]의 주제다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]의 스택 아래에 놓인다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 그 '학습과 적응' 층 밑의 연산 바닥으로, §5의 사례 — "저 패널을 프레임에 설치해" — 에서 끼움을 해내는 정책이 학습되는 곳이다. 그 정책, [[05-construction-robotics/imitating-contact|10. 접촉 모방]]의 학습된 정책은 실제 시연 코퍼스로 파인튜닝하는 날 연구실 워크스테이션을 넘어서고, 공유 클러스터에서는 첫 실수가 며칠을 앗아 간다. 체크포인트 없이 48시간짜리 작업 하나로 낸 50시간 파인튜닝은 48시간째에 죽어 처음부터 다시 시작하고, 같은 코퍼스를 작은 파일 360만 개로 두면 쿼터가 거절하며, 억지로 읽으면 GPU가 시간의 35%를 논다. [[03-deep-learning/foundations/training-at-scale|1.3 §5–§6]]은 그런 학습의 메모리와 연산량을, [[03-deep-learning/foundations/gpu-computing|1.4 §7]]은 GPU가 그것으로 하는 일을 따지는데, 둘 다 학습이 GPU에 닿아 끝까지 살아남는다고 가정한다. 이 페이지는 [[07-research-program/index|학위논문 경로 §8]]의 일곱 블록 밖에 있으니, 학습이 처음 여러분 기계를 떠날 때, 늦어도 10. 접촉 모방의 정책을 학습하는 블록 7에서 읽는다. 읽고 나면 자기 학습의 배치 스크립트와 작업 사슬을 쓰고, GPU가 쉬지 않게 데이터를 스테이징하고, 저장 비용과 중단 비율로 체크포인트 간격을 고를 수 있다.

> [!note] 처음이라면 · First pass
> 약 90분씩 두 번. **1회차 — 긴 학습을 대기열에 통과시키기.** 그림, §1, §4, §5를 읽고, 계산기를 들고 계산 절의 1단계와 4단계를 따라간다. FT-1은 200 GPU-시간이고, 48 h 한도 때문에 작업 둘이 필요하다. 스스로 점검 1, 2, 4번으로 마친다. **2회차 — 중단에서 살아남기.** §6(루프를 돌려 재개한 두 실행을 비교한다)과 §7을 읽고, 5단계를 손으로 풀고 — 12분 간격이 나온다 — 스스로 점검 3번과 6번에 답한다. 그다음은 필요할 때: §2와 §8, 계산 절 2–3단계는 데이터셋을 클러스터에 옮기기 전에, §9와 6단계는 작업이 며칠씩 돌기 시작하면, §3은 클러스터에 소프트웨어를 처음 갖추는 날, §10은 GPU가 더 필요해지는 날 읽고, 과제와 §11의 실습은 맨 나중에 한다. *더 깊이* 접은 상자는 그 세부가 발목을 잡을 때 연다.

### 이 페이지의 대상 · Running object

대상은 둘이고 여기서 고정한다. 학습 작업 하나와, 그것이 도는 기계다. 둘 다 [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치가 아니다. FT-1은 1.4의 MLP-256처럼 비용 대상이어서, 페이지가 *값을 매기는* 크기, 속도, 시간으로 이루어져 있다. 코퍼스는 [[04-robotics/teleoperation-demonstration|12. 원격조작]]의 시연과 [[05-construction-robotics/imitating-contact|10. 접촉 모방]]의 정책을 모아 키운 것에 가깝지만, 여기서는 어느 페이지에도 기대지 않는다.

**FT-1**, 파인튜닝 작업:

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $N$ | 파라미터 $3.0\times10^{8}$개 | 시연 데이터로 파인튜닝하는 정책. 혼합 정밀도의 Adam으로 학습한다 |
| $S$ | $12N=3.6$ GB | 체크포인트 하나: fp32 가중치와 Adam의 두 모멘트, 파라미터당 각 4바이트(§6) |
| $G$ | 노드 하나의 GPU 4개 | 데이터 병렬, 스텝마다 GPU당 샘플 64개(§10) |
| 배치, $t_{\text{step}}$ | 샘플 256개, 스텝당 0.25 s | 입력이 따라오는 한 $r_{\text{need}}=256/0.25=1{,}024$ 샘플/s |
| 스텝 | 720,000 | $W=720{,}000\times0.25\ \text{s}=50$ h의 학습, 153.6 에폭 |
| 코퍼스 | 에피소드 2,000개 × 샘플 600개 | 각각 10 Hz로 60 s: 샘플 1,200,000개 |
| 샘플 | 카메라 이미지 3장, 장당 50 kB | 샘플당 150 kB, 모두 180 GB. 상태와 행동은 0.1%도 안 되어 뺀다 |
| 저장 배치 | 파일 3,600,000개, 또는 샤드 200개 | 이미지마다 파일 하나, 또는 에피소드 10개씩 담은 900 MB 파일(§8) |

**교과용 클러스터:**

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $L$ | 48 h | 두 GPU 파티션 `gpu`와 `gpu-preempt`의 벽시계 시간 한도 |
| 노드 | GPU 4개, 코어 64개, 512 GB; 2 GB/s의 로컬 NVMe 1.6 TB | 계산 노드 하나 |
| $\beta_r$, $\beta_w$ | 1.0 GB/s, 0.5 GB/s | 공유 파일시스템의 노드당 읽기·쓰기 대역폭 |
| $r_f$ | 초당 파일 2,000개 | 공유 파일시스템이 노드 하나에 초당 열어 주는 작은 파일 수 |
| home, work, scratch | 50 GB와 파일 500,000개; 1 TB와 파일 1,000,000개; 20 TB와 파일 10,000,000개 | 쿼터. home은 백업되고, scratch는 마지막으로 읽힌 지 30일 된 파일을 지운다(§2) |
| $M$ | 10 h | `gpu-preempt`에서 선점 사이의 평균 시간(§7) |
| $q$ | `gpu`에서 48 h 요청은 20 h, 3 h 요청은 2 h; `gpu-preempt`에서는 12분 | 대기열에서 기다리는 시간(§5) |
| $p$ | GPU-시간당 USD 2.00 | 빌린 GPU의 값(§10) |

두 표의 숫자는 모두 산수가 깔끔하도록 이 페이지가 정한 교과용 값이다. 어떤 클러스터, 제품, 가격표를 잰 값도 아니며, 1 GB $=10^9$바이트다. 모양은 Slurm 클러스터들이 공유하고, 여러분 사이트의 숫자는 그 사이트의 사용자 안내서에 있다.

*범위: 이 페이지는 Slurm이 운영하는 공유 GPU 클러스터에서 학습시키는 일상의 작업 흐름을 가르친다. 무엇이 어디서 돌고 어디에 사는지, 작업을 어떻게 쓰고, 제출하고, 잇고, 지켜보는지, 체크포인트에 무엇이 들어가야 하고 얼마나 자주 써야 하는지, GPU가 쉬지 않도록 데이터를 어떻게 놓는지를, 선택마다 값을 매기는 산수와 며칠을 잃게 하는 함정과 함께 다룬다. 리눅스, 셸, `ssh`([[02-foundations/tools/linux-shell|12.1]]), Git([[02-foundations/tools/git-research-code|12.2]]), 파이썬 환경([[02-foundations/tools/python-research-code|12.3]])은 가르치지 않는다. 이 트랙의 다른 페이지들이 맡는다. GPU의 내부는 [[03-deep-learning/foundations/gpu-computing|1.4]]의 몫이고, 분산 학습 기법은 [[03-deep-learning/foundations/training-at-scale|1.3 §5]]가 이름만 대며, 스케줄러의 내부 구조도 다루지 않는다. 여기 보인 Slurm 옵션은 모두 Slurm 문서와 대조했지만, 파티션·한도·정책에 대한 마지막 말은 여러분 사이트의 사용자 안내서가 한다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 540" style="max-width:100%;height:auto" role="img" aria-label="패널 두 개. (a) FT-1이 도는 곳: 노트북에서 ssh로 공유 로그인 노드에 들어가고, sbatch가 작업을 Slurm 컨트롤러에 넘기면 컨트롤러가 GPU 넷, 코어 64개, 512 GB, 1.6 TB 로컬 NVMe 디스크를 가진 계산 노드를 할당한다. 공유 파일시스템에는 home(50 GB, 파일 50만 개, 백업), work(1 TB, 파일 100만 개), scratch(20 TB, 파일 1,000만 개, 마지막 접근 뒤 30일에 삭제)가 있다. 180 GB 코퍼스를 스테이징하는 데 샤드 200개로는 3.0분, 파일 360만 개로는 33.0분이 걸리고, 3.6 GB 체크포인트는 12분마다 7.2초에 work로 돌아간다. (b) 로그-로그 축 위의 체크포인트 거래: 저장 비용 C/τ는 내려가고 잃는 작업 τ/2M은 올라가며, 둘은 τ* = 12분에서 각각 1%로 만나고 합은 거기서 최소 2%다. 재시작까지 넣은 정확한 모형은 그 위에 있어 12분에서 4.59%다.">
  <defs><marker id="gc7arrk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) FT-1이 도는 곳과 움직이는 것</text>
  <rect x="12" y="30" width="92" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="58" y="47" font-size="11" fill="currentColor" text-anchor="middle">내 노트북</text>
  <text x="58" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">ssh 키</text>
  <rect x="146" y="30" width="118" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="205" y="47" font-size="11" fill="currentColor" text-anchor="middle">로그인 노드</text>
  <text x="205" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">편집 · 제출 · 복사</text>
  <rect x="306" y="30" width="242" height="42" rx="4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="427" y="47" font-size="11" fill="currentColor" text-anchor="middle">Slurm 컨트롤러</text>
  <text x="427" y="63" font-size="10" fill="currentColor" fill-opacity="0.75" text-anchor="middle">대기열 · gpu 48 h · gpu-preempt M = 10 h</text>
  <line x1="104" y1="51" x2="144" y2="51" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arrk)"/>
  <text x="125" y="45" font-size="10" fill="currentColor" text-anchor="middle">ssh</text>
  <line x1="264" y1="51" x2="304" y2="51" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arrk)"/>
  <text x="285" y="45" font-size="10" fill="currentColor" text-anchor="middle">sbatch</text>
  <line x1="427" y1="72" x2="427" y2="102" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arrk)"/>
  <text x="433" y="91" font-size="10" fill="currentColor" fill-opacity="0.85">GPU 4개, 48 h 이하로 할당</text>
  <rect x="306" y="104" width="242" height="112" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="316" y="120" font-size="11" fill="currentColor">계산 노드</text>
  <rect x="316" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="350" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="364" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="384" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="398" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <rect x="418" y="128" width="28" height="20" rx="2" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="432" y="142" font-size="10" fill="currentColor" text-anchor="middle">GPU</text>
  <text x="456" y="142" font-size="10" fill="currentColor" fill-opacity="0.85">코어 64개 · 512 GB</text>
  <rect x="316" y="158" width="222" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <text x="427" y="172" font-size="10" fill="currentColor" text-anchor="middle">로컬 NVMe 1.6 TB, 2 GB/s</text>
  <text x="316" y="200" font-size="10" fill="currentColor" fill-opacity="0.85">초당 1,024 샘플 = 153.6 MB/s 필요</text>
  <rect x="12" y="104" width="252" height="112" rx="4" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="22" y="120" font-size="11" fill="currentColor">공유 파일시스템</text>
  <rect x="22" y="128" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="140" font-size="10" fill="currentColor">home  50 GB · 파일 50만 · 백업</text>
  <rect x="22" y="148" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="160" font-size="10" fill="currentColor">work  1 TB · 파일 100만: 샤드, 체크포인트</text>
  <rect x="22" y="168" width="232" height="17" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.6"/>
  <text x="28" y="180" font-size="10" fill="currentColor">scratch  20 TB · 파일 1,000만 · 30일에 삭제</text>
  <text x="22" y="206" font-size="10" fill="currentColor" fill-opacity="0.8">노드당: 읽기 1 GB/s · 쓰기 0.5 GB/s · 초당 파일 2,000개</text>
  <line x1="255" y1="154" x2="314" y2="165" stroke="currentColor" stroke-width="1.2" marker-end="url(#gc7arrk)"/>
  <text x="283" y="152" font-size="10" fill="currentColor" text-anchor="middle">스테이징</text>
  <line x1="306" y1="190" x2="257" y2="162" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" marker-end="url(#gc7arrk)"/>
  <text x="283" y="196" font-size="10" fill="currentColor" text-anchor="middle">저장</text>
  <text x="12" y="240" font-size="10" fill="currentColor">180 GB 스테이징, 같은 척도:</text>
  <rect x="160" y="231" width="27.3" height="11" fill="currentColor" fill-opacity="0.75"/>
  <text x="193.3" y="240" font-size="10" fill="currentColor">샤드 200개: 3.0분</text>
  <rect x="160" y="248" width="300.0" height="11" fill="currentColor" fill-opacity="0.3"/>
  <text x="166" y="257" font-size="10" fill="currentColor">파일 3,600,000개: 33.0분</text>
  <text x="12" y="280" font-size="10" fill="currentColor" fill-opacity="0.85">체크포인트: 3.6 GB를 work에 7.2초, 12분마다(§6–§7)</text>
  <text x="12" y="306" font-size="12" fill="currentColor">(b) FT-1의 체크포인트 거래: C = 7.2 s, M = 10 h</text>
  <line x1="70.0" y1="471.4" x2="540.0" y2="471.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="474.9" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">0.1%</text>
  <line x1="70.0" y1="422.9" x2="540.0" y2="422.9" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="426.4" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">1%</text>
  <line x1="70.0" y1="374.5" x2="540.0" y2="374.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="378.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">10%</text>
  <line x1="70.0" y1="326.0" x2="540.0" y2="326.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="66.0" y="329.5" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="end">100%</text>
  <line x1="70.0" y1="326.0" x2="70.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="70.0" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1분</text>
  <line x1="164.2" y1="326.0" x2="164.2" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="164.2" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">3</text>
  <line x1="267.5" y1="326.0" x2="267.5" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="267.5" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">10</text>
  <line x1="361.7" y1="326.0" x2="361.7" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="361.7" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">30</text>
  <line x1="421.1" y1="326.0" x2="421.1" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="421.1" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">1 h</text>
  <line x1="540.0" y1="326.0" x2="540.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>
  <text x="540.0" y="499.0" font-size="10" fill="currentColor" fill-opacity="0.8" text-anchor="middle">4 h</text>
  <line x1="70.0" y1="326.0" x2="70.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="70.0" y1="486.0" x2="540.0" y2="486.0" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="305" y="513.0" font-size="10" fill="currentColor" text-anchor="middle">체크포인트 간격 τ, 로그 척도</text>
  <text x="76.0" y="338.0" font-size="10" fill="currentColor" fill-opacity="0.8">W 대비 비율</text>
  <polyline points="70.0,370.6 77.8,372.6 85.7,374.5 93.5,376.4 101.3,378.3 109.2,380.2 117.0,382.2 124.8,384.1 132.7,386.0 140.5,387.9 148.3,389.9 156.2,391.8 164.0,393.7 171.8,395.6 179.7,397.6 187.5,399.5 195.3,401.4 203.2,403.3 211.0,405.2 218.8,407.2 226.7,409.1 234.5,411.0 242.3,412.9 250.2,414.9 258.0,416.8 265.8,418.7 273.7,420.6 281.5,422.5 289.3,424.5 297.2,426.4 305.0,428.3 312.8,430.2 320.7,432.2 328.5,434.1 336.3,436.0 344.2,437.9 352.0,439.9 359.8,441.8 367.7,443.7 375.5,445.6 383.3,447.5 391.2,449.5 399.0,451.4 406.8,453.3 414.7,455.2 422.5,457.2 430.3,459.1 438.2,461.0 446.0,462.9 453.8,464.8 461.7,466.8 469.5,468.7 477.3,470.6 485.2,472.5 493.0,474.5 500.8,476.4 508.7,478.3 516.5,480.2 524.3,482.2 532.2,484.1 540.0,486.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="5 3"/>
  <polyline points="70.0,475.2 77.8,473.3 85.7,471.4 93.5,469.5 101.3,467.6 109.2,465.6 117.0,463.7 124.8,461.8 132.7,459.9 140.5,457.9 148.3,456.0 156.2,454.1 164.0,452.2 171.8,450.3 179.7,448.3 187.5,446.4 195.3,444.5 203.2,442.6 211.0,440.6 218.8,438.7 226.7,436.8 234.5,434.9 242.3,432.9 250.2,431.0 258.0,429.1 265.8,427.2 273.7,425.3 281.5,423.3 289.3,421.4 297.2,419.5 305.0,417.6 312.8,415.6 320.7,413.7 328.5,411.8 336.3,409.9 344.2,407.9 352.0,406.0 359.8,404.1 367.7,402.2 375.5,400.3 383.3,398.3 391.2,396.4 399.0,394.5 406.8,392.6 414.7,390.6 422.5,388.7 430.3,386.8 438.2,384.9 446.0,383.0 453.8,381.0 461.7,379.1 469.5,377.2 477.3,375.3 485.2,373.3 493.0,371.4 500.8,369.5 508.7,367.6 516.5,365.6 524.3,363.7 532.2,361.8 540.0,359.9" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <polyline points="70.0,370.5 77.8,372.4 85.7,374.3 93.5,376.1 101.3,378.0 109.2,379.9 117.0,381.7 124.8,383.6 132.7,385.4 140.5,387.2 148.3,389.0 156.2,390.7 164.0,392.4 171.8,394.1 179.7,395.7 187.5,397.3 195.3,398.8 203.2,400.3 211.0,401.6 218.8,402.9 226.7,404.1 234.5,405.1 242.3,406.1 250.2,406.8 258.0,407.5 265.8,407.9 273.7,408.2 281.5,408.3 289.3,408.3 297.2,408.1 305.0,407.7 312.8,407.1 320.7,406.4 328.5,405.5 336.3,404.5 344.2,403.4 352.0,402.2 359.8,400.9 367.7,399.4 375.5,397.9 383.3,396.4 391.2,394.8 399.0,393.1 406.8,391.4 414.7,389.7 422.5,387.9 430.3,386.1 438.2,384.3 446.0,382.5 453.8,380.6 461.7,378.8 469.5,376.9 477.3,375.0 485.2,373.2 493.0,371.3 500.8,369.4 508.7,367.5 516.5,365.6 524.3,363.6 532.2,361.7 540.0,359.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <polyline points="70.0,366.0 77.8,367.6 85.7,369.1 93.5,370.6 101.3,372.1 109.2,373.5 117.0,374.9 124.8,376.3 132.7,377.6 140.5,378.8 148.3,380.0 156.2,381.2 164.0,382.3 171.8,383.3 179.7,384.3 187.5,385.2 195.3,386.1 203.2,386.9 211.0,387.6 218.8,388.3 226.7,388.9 234.5,389.4 242.3,389.8 250.2,390.2 258.0,390.5 265.8,390.7 273.7,390.8 281.5,390.9 289.3,390.8 297.2,390.7 305.0,390.5 312.8,390.3 320.7,389.9 328.5,389.5 336.3,389.0 344.2,388.4 352.0,387.8 359.8,387.1 367.7,386.3 375.5,385.4 383.3,384.5 391.2,383.5 399.0,382.4 406.8,381.3 414.7,380.1 422.5,378.8 430.3,377.5 438.2,376.2 446.0,374.8 453.8,373.3 461.7,371.8 469.5,370.3 477.3,368.7 485.2,367.0 493.0,365.3 500.8,363.6 508.7,361.8 516.5,360.0 524.3,358.1 532.2,356.2 540.0,354.3" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.5"/>
  <line x1="283.1" y1="344.0" x2="283.1" y2="486.0" stroke="currentColor" stroke-width="0.9" stroke-dasharray="2 2" stroke-opacity="0.8"/>
  <circle cx="283.1" cy="408.3" r="3.8" fill="currentColor"/>
  <circle cx="283.1" cy="422.9" r="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="283.1" cy="390.9" r="3.4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8"/>
  <text x="289.1" y="338.0" font-size="10" fill="currentColor" font-weight="bold">τ* = √(2CM) = 12분</text>
  <text x="289.1" y="351.0" font-size="10" fill="currentColor">1차 근사 1% + 1% = 2.0%, 정확한 값 4.59%</text>
  <line x1="16" y1="527.5" x2="36" y2="527.5" stroke="currentColor" stroke-width="2.2"/>
  <text x="41" y="531.0" font-size="10" fill="currentColor">합, 1차 근사</text>
  <line x1="140" y1="527.5" x2="160" y2="527.5" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.5"/>
  <text x="165" y="531.0" font-size="10" fill="currentColor">정확한 값, 재시작 포함</text>
  <line x1="300" y1="527.5" x2="320" y2="527.5" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="5 3"/>
  <text x="325" y="531.0" font-size="10" fill="currentColor">저장 C/τ</text>
  <line x1="420" y1="527.5" x2="440" y2="527.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.75" stroke-dasharray="1.5 2.5"/>
  <text x="445" y="531.0" font-size="10" fill="currentColor">잃는 작업 τ/2M</text>
</svg>

교과용 클러스터 위의 FT-1이다. (a) 노트북에서 `ssh`로 로그인 노드에 들어가 `sbatch`로 FT-1을 Slurm에 넘긴다. Slurm이 GPU 넷을 가진 노드를 할당하면, 작업은 코퍼스를 work에서 노드 자신의 디스크로 스테이징하고 — 같은 180 GB가 샤드 200개로는 3.0분, 파일 3,600,000개로는 33.0분 — 12분마다 3.6 GB 체크포인트를 work에 다시 쓴다. (b) 선점형 파티션($C=7.2$ s, $M=10$ h)에서 저장에 드는 몫은 학습 시간의 $C/\tau$, 잃는 작업은 $\tau/2M$이다. 두 선은 $\tau^\star=12$분에서 각각 1%로 만나고 그 합은 거기서 가장 작은 2%이며, 재시작까지 넣은 정확한 모형은 그 자리에서 4.59%다.

### 1. 클러스터의 구조: 로그인 노드, 스케줄러, 계산 노드

*한 문장으로:* 클러스터의 GPU는 사용자 수백 명이 함께 쓰므로 그냥 가져다 쓸 수는 없다. 모두가 함께 쓰는 로그인 노드에서 스케줄러에 요청하고, 학습은 작업 안에서만 — 작업이 요청한 자원 그대로, 요청한 시간을 넘지 않는 동안만 — 돈다.

**문제.** FT-1에는 GPU 네 개가 50시간 필요하다. 클러스터에는 GPU 수백 개와 사용자 수백 명이 있고, 누가 어느 GPU를 언제 쓸지 누군가 정해야 한다.

**생각.** 그 누군가가 스케줄러, Slurm이다. `ssh`로 **로그인 노드**(login node)에 들어가는데, 이것은 모든 사용자가 함께 쓰는 몇 대 가운데 하나다. 거기서 여러분은 *요청한다*. **작업**(job)은 정해진 시간 동안의 자원 요청이고, 그 자원 위에서 돌릴 스크립트가 딸려 있다. Slurm은 요청을 대기열에 넣었다가 **계산 노드**(compute node)가 비면 거기서 스크립트를 시작하고, 스크립트가 끝나거나 시간이 다하면 노드를 거두어 간다. 계산 노드에 로그인해서 일하는 사람은 없다. 프로그램은 Slurm이 거기서 시작했기 때문에만 거기서 돈다. 노드는 한도가 저마다 다른 **파티션**(partition)으로 묶인다. 교과용 클러스터의 `gpu`와 `gpu-preempt`는 같은 노드를 같은 48 h 한도로 담고, 뒤의 것에서는 다른 작업에 자리를 내주려고 돌던 작업이 멈춰질 수 있다(§7).

> **배치 작업의 정의.** **배치 작업**(batch job)은 *스케줄러에 보내는 요청*이다. 자원, 시간 한도, 스크립트로 이루어지며, 돌고 있는 프로그램이 아니다. 정의 조건 넷. **자원을 이름으로 요청하고**(노드, GPU, 코어, 메모리, 파티션) 요청하지 않은 것은 받지 않는다. 파티션의 한도를 넘지 않는 **시간 한도**가 있고, 스크립트가 끝나거나 한도에 이르거나 둘 중 먼저 오는 때에 끝난다. **터미널 없이 돈다**: `sbatch`는 스크립트가 작업 번호를 받자마자 돌아오고, 자원이 비면 Slurm이 스크립트 한 벌을 대개 작업의 첫 노드에서 돌리며 출력은 파일로 간다. 그리고 할당을 쥐고 있는 동안에는 자원이 무엇을 하든 **할당 전체를 쓴 것으로 친다**.
>
> $$t_{\text{end}}=t_{\text{start}}+\min\big(t_{\text{script}},\ L_{\text{job}}\big),\qquad L_{\text{job}}\le L,\qquad \text{GPU-hours}=G\,\big(t_{\text{end}}-t_{\text{start}}\big)$$
>
> 여기서 $t_{\text{script}}$는 아무것도 막지 않을 때 스크립트가 도는 시간, $L_{\text{job}}$은 작업의 한도, $L$은 파티션의 한도, $G$는 할당된 GPU 수다. 그러니 비용은 할당과 시계를 따를 뿐, GPU가 얼마나 바빴는지와는 상관이 없다.
>
> - **예**: FT-1의 첫 작업은 노드 하나, `--gres=gpu:4`, 48 h를 요청한다. 스크립트는 50 h의 학습을 원하므로 작업은 48 h 뒤 한도에서 끝나고, 그동안 192 GPU-시간을 쓴다.
> - **비예**: 로그인 노드의 프롬프트에 친 `python train.py`. 스케줄러가 시작한 것이 아니고, 할당된 GPU도 없으며, `ssh` 세션과 함께 끝난다.
> - **왜 중요한가**: 작업은 학습이 끝났든 아니든 한도에서 멈추므로 긴 학습은 여러 작업으로 잘라야 하고(§5), 쥔 만큼 값을 치르므로 작업 안에서 노는 GPU도 바쁜 GPU와 같은 값을 치른다(§9).

**함정.**

- *로그인 노드에서 일하기.* 로그인 노드는 편집, 제출, 파일 옮기기, 몇 초짜리 시험을 위한 곳이다. "잘 도는지만 보려고" 거기서 워커 프로세스 32개짜리 데이터 로더를 띄우면 모든 사용자의 세션이 느려지고, GPU는 없으며, 연결이 끊기면 함께 죽는다. 시험은 짧은 대화형 할당에서 한다(§5).
- *GPU를 잊기.* Slurm은 GPU를 요청한 작업에만 준다. 노드당 `--gres=gpu:4`, 또는 `--gpus`다. 이것을 빠뜨린 작업은 GPU 노드에 앉고도 GPU를 하나도 보지 못한다. 코드가 CPU로 물러나는 식이라면 1초 만에 실패하는 대신 며칠 동안 학습한다. 작업이 받은 GPU에 대해서는 Slurm이 `CUDA_VISIBLE_DEVICES`를 정해 주므로, 코드는 보이는 장치를 그대로 쓰면 된다.
- *파티션이 허락하는 것보다 많이 요청하기.* 48 h 파티션에 `--time=72:00:00`으로 낸 작업은 시작했다가 실패하지 않는다. `PartitionTimeLimit`이라는 사유로, 어쩌면 영원히 대기한다.

작업이 무엇을 얼마 동안 쥐었는지는 `sacct`가 기록하고, 그것이 여러분이 치르는 값이다. 사이트가 예산을 둔다면 그 GPU-시간으로, 그리고 우선순위로 치른다. Slurm의 공정 분배(fair-share) 인자는 약속받은 몫과 실제로 쓴 양의 차이여서, 할당해 놓고 놀린 GPU도 바쁜 GPU만큼 다음 작업의 우선순위를 낮춘다.

### 2. 저장소: 데이터가 살 수 있는 곳

*한 문장으로:* FT-1의 코퍼스와 체크포인트에는 모든 노드가 보고, 지워지지 않으며, 들어갈 자리가 있는 곳이 필요한데, 클러스터의 파일시스템들은 바로 그 약속 — 백업되거나 지워지거나, 공유되거나 노드 하나의 것이거나 — 에서 서로 다르고, 저마다 바이트만이 아니라 파일 수까지 세는 쿼터가 있다.

**문제.** FT-1에는 180 GB 코퍼스가 있고, 12분마다 3.6 GB 체크포인트를 쓰며, 컨테이너 이미지와 약간의 코드로 돈다. 저마다 모든 노드가 닿을 수 있고, 지워지지 않으며, 들어갈 자리가 있는 곳에 살아야 한다.

**생각.** 사이트들은 이름만 다를 뿐 같은 네 종류의 자리를 준다. 숫자는 교과용 클러스터의 것이다.

| 자리 | 교과용 클러스터 | 약속 | 여기에 둘 것 | 절대 두지 말 것 |
|---|---|---|---|---|
| home | 50 GB, 파일 500,000개 | 백업, 삭제 없음 | 코드, 설정, 작업 스크립트 | 데이터셋, 체크포인트, 환경 |
| work | 1 TB, 파일 1,000,000개 | 보존, 백업 없음 | 샤드로 만든 코퍼스, 체크포인트, 이미지 | 작은 파일 수백만 개 |
| scratch | 20 TB, 파일 10,000,000개 | 30일 동안 안 읽힌 파일 삭제 | 중간 산출물, 작업용 사본 | 무엇이든 유일한 사본 |
| 노드 자신의 NVMe | 1.6 TB, 쿼터 없음 | 이 작업 동안만 | 스테이징한 코퍼스, 임시 파일 | 다음 작업이 필요로 하는 것 |

home, work, scratch는 *공유*다. 모든 노드가 같은 파일을 본다. 노드 자신의 디스크는 *사적*이다. 작은 파일을 많이 읽기에는 기계에서 가장 빠른 곳이지만 다른 노드에서는 보이지 않는다. FT-1의 두 번째 작업은 다른 노드에서 돌 수 있고, 그 노드는 첫 작업이 남긴 것을 보지 못한다.

**바이트만이 아니라 파일 수가 값을 매기는 이유.** Lustre 같은 병렬 파일시스템은 파일의 내용을 데이터 서버에, 파일마다의 이름·권한·배치 — 데이터가 어디 있는지 — 를 모든 사용자가 함께 쓰는 메타데이터 서버에 둔다. 클라이언트는 메타데이터 서버에 파일을 열어 달라고 청하고, 그다음 바이트는 데이터 서버에서 곧바로 읽는다(Lustre 위키). 그래서 파일 하나를 읽으려면 먼저 열어 달라는 요청을 한 번 보내고, 그다음 바이트가 대역폭으로 흘러온다. 교과용 클러스터는 노드 하나에 초당 약 $r_f=2{,}000$번 열어 주고 읽기는 $\beta_r=1$ GB/s이니, 50 kB 파일 백만 개는 파일시스템에게 "50 GB"가 아니라 요청 백만 번이다. §8이 이 값을 매기고, 쿼터가 이것을 강제한다.

> **저장소 쿼터의 정의.** **저장소 쿼터**(storage quota)는 *파일시스템이 사용자 한 명이나 프로젝트 하나의 사용량에 거는 제한*이다. 쓸 때 적용되는 규칙이지, 남은 공간을 재는 값이 아니다. 정의 조건 넷. **제한이 둘**이다. 바이트와 파일 수이고, 파일은 아무리 작아도 뒤의 것에 하나로 셈한다. **파일시스템마다** 따로다. home, work, scratch가 저마다 쿼터를 가진다. **쓰는 순간에 집행된다**. 둘 중 어느 한도든 넘는 파일 생성은 실패한다. 리눅스의 `open`은 디스크 블록이나 inode 쿼터가 다하면 `EDQUOT`, "Disk quota exceeded"를 돌려준다. 그리고 **삭제 정책(purge)이 아니다**. 쿼터는 새 데이터를 양으로 거절하고, 삭제 정책은 오래된 데이터를 나이로 지운다.
>
> $$\text{a write succeeds only if}\quad \sum_{i=1}^{n} b_i\le Q_b\quad\text{and}\quad n\le Q_n$$
>
> 여기서 $b_i$는 파일 $i$의 크기, $n$은 파일 수, $Q_b$와 $Q_n$은 바이트와 파일 수의 한도다. 그러니 $B$바이트의 코퍼스는 파일 크기의 평균이 적어도 $B/Q_n$바이트일 때만 들어간다. work 위 FT-1의 180 GB라면 180 kB다.
>
> - **예**: 이미지마다 파일 하나로 work에 둔 FT-1의 코퍼스. 1 TB에 대한 180 GB는 통과하지만 1,000,000개에 대한 파일 3,600,000개는 실패한다. 백만 번째 다음 파일부터는 모두 거절되므로 코퍼스의 27.8%까지만 도착한다. 900 MB짜리 샤드 200개라면 180 GB와 파일 200개여서 두 한도가 모두 지켜진다.
> - **비예**: scratch의 30일 규칙. scratch 쿼터 안에 든 코퍼스도 한 달 동안 아무도 읽지 않으면 지워진다. 쿼터는 들여보냈고, 삭제 정책이 가져간다.
> - **왜 중요한가**: 파일 수 한도는 노트북에는 없어서 다들 잊는 쪽이다. FT-1을 샤드로 만드는 이유가 이것이다.

**함정.**

- *scratch를 유일한 사본으로.* 여름 동안 거기 둔 코퍼스는 9월이면 일부가 사라져 있다.
- *노드 자신의 디스크에 체크포인트.* 온전하지만 다음 작업에는 보이지 않는다.
- *home에 환경.* 파이썬 환경 하나는 파일 수만 개다(§3). 둘셋이면 home의 500,000개 대부분이 찬다.

### 3. 소프트웨어: 모듈과 컨테이너

*한 문장으로:* 클러스터의 시스템에는 설치할 수 없으므로 FT-1이 필요로 하는 소프트웨어는 사이트의 모듈, 여러분 디렉터리에 만든 환경, 또는 컨테이너 이미지에서 와야 하고 — 그것을 갖추는 일은 제출한 터미널이 아니라 작업 스크립트가 해야 한다.

**문제.** FT-1에는 특정 버전의 파이썬, PyTorch, CUDA가 필요하다. 자기 워크스테이션이라면 `sudo apt install`로 깔겠지만, 클러스터에서는 root 권한이 없고, 시스템 소프트웨어는 관리자의 것이며 관리자가 업그레이드하면 바뀐다.

**생각.** 출처는 셋이다. 사이트의 **모듈**(module): 사이트가 설치해 둔 소프트웨어로, `module load`가 셸 환경에 더해 준다. **자기 환경**: work에 만든 가상 환경이나 conda 환경으로, 잘 되지만 파일이 많다. **컨테이너 이미지**(container image): Apptainer는 소프트웨어 환경 전체를 SIF 파일 하나에 담고, 그 파일은 여러분의 권한으로 노드 자신의 커널과 GPU 드라이버 위에서 돈다. GPU에는 `--nv`, 데이터에는 `--bind`를 쓴다. 영어 절의 명령 네 줄은 Lmod와 Apptainer 문서로 확인했고 여기서 실행하지 않았다. 사이트가 제공하는 것 보기, 셸에 더하기, 기존 이미지를 파일 하나로 만들기, 그 안에서 학습 명령 돌리기다.

**규칙을 대상에.** 환경은 파일 수로 값을 치른다. 디렉터리로 두면 담긴 파일마다 하나씩 — 파일 수 쿼터에, 그리고 시작할 때마다 메타데이터 서버에 — 치르고, SIF 이미지로 두면 하나다. 이 페이지를 쓴 노트북의 파이썬 설치는 3.5 GB에 파일 127,915개를 담고 있다(잰 값이며, 재는 법은 접은 상자에 있다). 환경 하나로 work 파일 쿼터의 12.8%다. FT-1의 `policy.sif`는 파일 1개다.

**함정.**

- *작업이 터미널을 물려받는다.* 작업은 `sbatch`를 친 셸의 환경을 통째로 가지고 시작한다. Slurm의 `--export`는 따로 말하지 않으면 그 전부를 싣는다. 환경을 활성화해 둔 터미널에서 내면 되고 새로 로그인해서 내면 `ModuleNotFoundError`로 실패하는 스크립트는, 자기 상태가 아니라 여러분 터미널의 상태 위에서 돌고 있었던 것이다. 준비는 스크립트 안에 넣는다. `module purge`와 `module load` 줄들, 또는 컨테이너다.
- *드라이버보다 새 이미지.* GPU 드라이버는 이미지가 아니라 노드의 것이다. 노드의 드라이버가 지원하지 않는 CUDA 버전으로 빌드한 소프트웨어는 이미지가 아무리 완전해도 그 노드에서 실패한다.
- *환경의 기록이 없다.* 결과와 함께 이미지의 체크섬을 기록한다. [[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]의 고정된 실행(pinned run)이 이미지 digest를 기록하고, [[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §7]]이 실행의 산출물 목록에 컨테이너를 넣는 것과 같다.

> [!note]- 더 깊이 · Deeper
> - **모듈.** `module spider <이름>`은 다른 모듈을 먼저 불러야 보이는 것까지 포함해 사이트의 모든 모듈을 찾는다. `module list`는 불러온 것을 보여 주고 `module purge`는 모두 내린다(Lmod 사용자 안내서).
> - **Apptainer.** 컨테이너 안에서도 바깥과 같은 사용자이고, 기본적으로 호스트에서 권한을 더 얻지 못한다. 권한 없는 사용자가 자기 정의 파일로 `apptainer build policy.sif policy.def`를 하면 `--fakeroot`가 암묵적으로 붙는다. `--nv`는 호스트의 NVIDIA 장치를 보이게 하고, 호스트의 CUDA 드라이버 라이브러리를 안으로 묶어 넣고, `LD_LIBRARY_PATH`가 그것을 가리키게 한다. 기본으로 컨테이너는 home, 현재 디렉터리, `/tmp`, `/var/tmp`, 그리고 `/dev`나 `/proc` 같은 시스템 경로를 보는데 — 이 목록은 관리자가 바꿀 수 있다 — 그 밖의 것은 `--bind src:dest`로만 본다. 묶을 경로가 여럿이면 쉼표로 잇거나 `--bind`를 여러 번 쓴다(Apptainer 사용자 안내서).
> - **잰 방법.** 영어 절의 명령 세 줄 — 패키지 디렉터리 찾기, 그 안의 파일 세기(`find ... -type f | wc -l`), 크기 재기(`du -sh`) — 을 macOS에서 돌려 127,915개와 3.5G를 얻었다. `find`, `wc`, `du -sh`는 리눅스에서도 같게 돈다.

### 4. 배치 스크립트와 작업의 일생

*한 문장으로:* Slurm은 읽을 수 있는 것만 돌리므로 FT-1의 요청은 배치 스크립트에 들어간다. Slurm은 그 `#SBATCH` 주석 줄을 어떤 셸보다 먼저 읽고, `sbatch`는 그것을 대기열에 넣고 곧바로 돌아오며, `squeue`와 `sacct`가 대기부터 끝 상태까지 작업을 따라간다.

**문제.** FT-1의 요청 — 노드 하나, GPU 넷, 코어 32개, 256 GB, 로그 파일, 한도 전의 경고 — 을 Slurm이 읽는 곳에, 돌릴 명령과 함께 적어야 한다.

**생각.** 배치 스크립트다. `#SBATCH` 줄은 `sbatch`가 명령줄에서 받을 옵션을 담고, 나머지는 작업의 첫 노드에서 도는 평범한 bash 스크립트다. 영어 절의 `ft1.sbatch`는 옵션마다 Slurm 문서(26.05판)의 `sbatch` 페이지에서, `torchrun`의 단일 노드 형태는 PyTorch 문서에서 확인했고, `/path/to/...`는 여러분 사이트의 경로 자리이며, 여기서 실행하지 않았다. 줄마다 읽으면 이렇다. 작업 이름 `ft1`(파일 이름의 `%x`이자 singleton 의존성이 맞추는 이름), 파티션 `gpu`, 노드 하나, 노드의 GPU 넷(이것이 없으면 GPU는 하나도 없다), 데이터 로더를 위한 코어 32개(기본은 태스크당 하나), 메모리 256 GB, 로그 `logs/%x-%j.out`(`%j`는 작업 번호이고 표준 출력과 표준 오류가 한 파일을 쓴다), 한도 약 10분 전에 작업 단계들에 SIGUSR1을 보내 달라는 `--signal=USR1@600`(§6), 끝나거나 실패하거나 의존성이 끝내 충족될 수 없을 때의 메일. `--time` 줄은 없다. 작업마다 한도가 달라서 명령줄에서 준다(§5). 그다음 `set -euo pipefail`, work와 노드 로컬 디스크의 경로, `rsync`로 샤드 200개(180 GB, 약 3분)를 스테이징하고(§8), `srun`이 컨테이너 안에서 `torchrun`으로 GPU마다 워커 하나씩 학습을 띄운다.

**규칙.** Slurm은 어떤 셸보다 먼저 `#SBATCH` 줄을 직접 읽으므로, 거기 쓴 셸 변수 — 예컨대 홈 디렉터리의 변수 — 는 달러 기호까지 글자 그대로 받아들여진다. 주석도 빈 줄도 아닌 첫 줄에서 읽기를 멈추므로, 모든 `#SBATCH` 줄은 `set -euo pipefail`보다 앞에 와야 한다. 그 줄은 실패한 첫 명령에서 작업을 멈춘다. 중간에 실패한 `rsync`는 코퍼스 일부로 학습을 시작하는 대신 작업을 끝낸다. `srun`은 학습을 작업 단계로 시작하고, `apptainer exec`는 그것을 컨테이너에서 돌리고, `torchrun`은 GPU마다 워커 프로세스를 하나씩 띄운다(§10). `train.py`와 그 옵션은 FT-1 자신의 것이다.

**대상 위에서: 작업의 일생.** 영어 절의 다섯 줄은 Slurm 문서로 확인했고 여기서 실행하지 않았다. 로그 디렉터리 만들기, `--parsable`로 새 작업 번호만 받아 두며 48 h로 제출하기, `squeue --me`로 상태와 대기 사유 보기, `sacct`로 끝난 뒤의 기록 보기, `scancel`로 취소하기다. `sbatch`는 작업이 번호를 받자마자 돌아온다. 작업이 `PD` 상태로 기다리는 동안 사유가 이유를 말한다. `Priority`(다른 작업이 먼저), `Resources`(노드가 비기를 기다림), `Dependency`(다른 작업을 기다림, §5)다. 돌기 시작하면 `R` 상태이고 `logs/ft1-<작업 번호>.out`을 쓴다. 모든 프로세스가 코드 0으로 끝나면 `COMPLETED`, 아니면 `FAILED`, `TIMEOUT`(한도에 이름), `CANCELLED`, `OUT_OF_MEMORY`, `NODE_FAIL`, `PREEMPTED`로 끝나고, 그 뒤 `sacct`가 상태, 종료 코드, 태스크의 최대 메모리를 보여 준다.

**함정.**

- *한도는 죽인다.* 한도에 이르면 모든 태스크가 SIGTERM을, 그다음 SIGKILL을 받는다. Slurm의 기본 설정에서는 30 s 뒤이고, 사이트가 정한 대로다. 저장하지 않은 것은 사라진다. FT-1은 `--signal=USR1@600`으로 10분 먼저 경고를 받아 그때 저장한다(§6).
- *스케줄러를 쉬지 않고 묻기.* `squeue`는 부를 때마다 Slurm 컨트롤러에 요청을 보내고, Slurm 문서는 스크립트 안의 반복문에서 부르는 클라이언트 명령이 모두를 위해 컨트롤러를 느리게 할 수 있다고 경고한다. `watch -n 1 squeue`가 바로 그런 반복문이다. 대신 `--mail-type=END,FAIL`이 알려 주게 한다.

> [!note]- 더 깊이 · Deeper
> 대기 사유 몇 개 더. `PartitionTimeLimit`(한도가 파티션의 것을 넘음: 영원히 기다린다. 사이트가 `EnforcePartLimits`를 켜 두었다면 `sbatch`가 제출 때 거절한다), `QOSMaxGRESPerUser`(그 서비스 품질에서 사용자 한 명이 쥘 수 있는 GPU 수를 넘는 요청), `DependencyNeverSatisfied`(§5). `squeue --me --start`는 대기 중인 작업마다 스케줄러가 예상하는 시작 시각을 보여 준다. `sacct`는 `-j`나 시작 시각을 주지 않으면 자정 이후의 작업만 보여 준다. `--mail-type`은 `TIME_LIMIT_80`(한도의 80% 사용)과 `INVALID_DEPEND`도 받는다. `sbatch --test-only`는 제출하지 않은 채 스크립트를 점검하고 언제 시작할지 어림한다.

### 5. 한도보다 긴 학습: 작업 사슬, 작업 배열, 대화형 작업

*한 문장으로:* 50시간의 학습은 48시간 한도에 들어가지 않으므로 학습은 저마다 마지막 체크포인트에서 이어 가는 작업들의 사슬이 되고, 그 사슬을 잇는 의존성의 종류가 사슬이 한도를 넘어 살아남을지를 정한다 — 그리고 정직하고 짧은 시간 한도가 작업마다 더 일찍 시작하게 한다.

**문제.** FT-1에는 50 h의 학습이 필요한데, 파티션은 48 h까지 허락한다.

**생각.** 학습을 **창**(window)으로 자른다. 창은 저마다 최신 체크포인트에서 이어 가며 자기 한도까지 학습하는 작업이고, 앞의 창이 끝나면 시작하도록 대기열에 걸어 둔다. 창은 시작할 때 고정 비용 — 데이터 스테이징, 체크포인트 불러오기 — 으로 조금, 도중의 저장으로 조금을 잃고, 나머지가 학습이다.

**규칙.** 창은 먼저 고정 비용 $o$를 치르고, 그다음 학습 $\tau$마다 $C$씩 멈춰 저장하므로(§6–§7), 꽉 찬 창 하나는

$$w=(L-o)\,\frac{\tau}{\tau+C},\qquad k=\Big\lceil\frac{W}{w}\Big\rceil$$

시간의 학습을 담는다. 고정 비용이 남긴 시간의 $C/(\tau+C)$만큼을 저장이 가져가기 때문이고, $k$는 필요한 창의 수다.

**대상 위에서.** $o=180.1+3.6=183.7$ s $=0.0510$ h(샤드 200개 스테이징, 3.6 GB 불러오기), $C=7.2$ s, $\tau=12$분이면 $w=(48-0.0510)\times0.2/0.202=47.47$ h이므로 $k=\lceil50/47.47\rceil=2$다. 두 번째 창에는 $0.0510+(50-47.47)\times1.01=2.60$ h만 필요하고, 48이 아니라 3 h를 요청한다. **백필**(backfill) 때문이다. Slurm은 우선순위가 더 높은 어떤 작업의 예상 시작도 늦추지 않는다면 낮은 우선순위의 작업을 먼저 시작시키는데, 그 예상 시작은 시간 한도로부터 계산되므로, 앞으로 5 h 동안 비는 노드는 3 h 작업은 받을 수 있어도 48 h 작업은 받을 수 없다. 교과용 숫자로 3 h 요청은 2 h, 48 h 요청은 20 h를 기다린다. 사슬은 영어 절의 두 줄이다(Slurm 문서로 확인, 여기서 실행하지 않음). 첫 창을 `--parsable`로 제출해 번호를 받아 두고, 두 번째 창을 `--time=03:00:00 --dependency=afterany:<그 번호>`로 낸다. 첫 창이 어떻게 끝나든 끝나면 자격을 얻는다. `--dependency=singleton`도 이름으로 같은 일을 한다. 여러분의 앞선 `ft1` 작업이 모두 끝나면 시작할 수 있다.

> **작업 의존성의 정의.** **작업 의존성**(job dependency)은 *대기 중인 작업에 붙인 조건으로, 다른 작업들을 지목하고 그 작업들이 어떻게 끝나야 이 작업이 시작할 수 있는지를 말한다*. 스케줄러가 평가하는 규칙이지, 스크립트를 쓴 순서가 아니다. 정의 조건 넷. **종류**가 어떤 끝을 인정할지 정한다. `afterany`는 어떤 끝이든, `afterok`은 종료 코드 0의 완료, `afternotok`은 실패한 끝 — 0이 아닌 종료, 노드 고장, 시간 초과 — 을, `singleton`은 같은 이름을 가진 여러분의 앞선 작업이 모두 끝난 것을 인정한다. 조건이 충족되기 전까지 작업은 **`Dependency` 사유로 대기한다**. 조건이 **더는 충족될 수 없게 되면** 작업은 결코 돌지 않는다. 사유는 `DependencyNeverSatisfied`가 되고, 앞선 작업이 나중에 다시 대기열에 들어가도 되살아나지 않는다. 그리고 충족된 의존성은 작업을 **자격 있게** 만들 뿐이다. 그다음에는 다른 작업처럼 자원을 기다린다.
>
> $$t_{\text{eligible}}(B)=\begin{cases}t_{\text{end}}(A)&\text{if state}(A)\in S_{\text{type}}\\ \infty&\text{otherwise}\end{cases},\qquad S_{\text{afterok}}=\{\text{COMPLETED}\},\quad S_{\text{afterany}}=\{\text{every end state}\}$$
>
> 여기서 $A$는 앞선 작업, $B$는 의존하는 작업, $S_{\text{type}}$은 그 종류가 인정하는 $A$의 끝 상태들이다. 그러니 $B$는 $A$의 끝에 자기 자원 대기를 더한 때보다 일찍 시작하지 못하고, $A$가 그 집합 밖에서 끝나면 영영 시작하지 못한다.
>
> - **예**: FT-1의 두 번째 창, `--dependency=afterany:$JOB1`. 첫 창은 48 h에 `TIMEOUT`으로 끝나고 `afterany`는 그것을 인정하므로, 두 번째 창은 곧바로 자격을 얻고, 3 h를 요청했으니 교과용 숫자로 2 h 뒤에 시작한다.
> - **비예**: 같은 사슬을 자연스러워 보이는 `afterok`으로. 시간 초과로 끝난 작업은 종료 코드 0으로 완료되지 않았으므로 두 번째 창은 결코 자격을 얻지 못한다. `DependencyNeverSatisfied`로 기다리는 사이 주말이 학습 없이 지나간다. (경고에 저장하고 코드 0으로 끝나는 창이라면 `afterok`을 만족시킨다. 그러니 그런 사슬은 모든 창이 깨끗하게 끝나는 동안만 버틴다.)
> - **왜 중요한가**: 사슬은 한도보다 긴 학습이 여러분이 자는 동안 이어지는 방법이다. 종류가 사슬이 자신이 넘으려고 만든 바로 그 한도에서 살아남을지를 정하고, `--mail-type=INVALID_DEPEND`는 의존성이 더는 충족될 수 없게 되는 순간 메일을 보낸다.

**여러 설정 돌리기: 작업 배열.** 한 학습의 여러 변형은 번호가 붙은 스크립트 하나다. `--array=0-11%4`는 작업 번호 하나 아래 태스크 12개를 내고 한 번에 넷까지만 돌리며, 태스크마다 `SLURM_ARRAY_TASK_ID`에서 자기 번호를 읽는다. 태스크당 5 h로 줄인 FT-1의 학습률 × 시드 탐색은 $12\times4\times5=240$ GPU-시간이고, 동시에 GPU 16개를 넘지 않는다. 태스크는 서로 독립이다. `%4`는 몇 개가 도는지를 제한할 뿐 순서를 정하지 않으므로, "학습한 다음 평가"는 배열이 아니라 의존성이다.

**디버깅: 대화형 할당.** `salloc --partition=gpu --gres=gpu:1 --time=01:00:00`은 GPU 하나를 한 시간 쥐고 셸을 준다. `srun <명령>`은 할당된 노드에서 명령을 돌리고, `exit`는 할당을 돌려준다. 함정은 그 셸이 도는 곳이다. 사이트가 따로 설정하지 않았다면 로그인 노드다. 일을 시작하기 전에 `hostname`과 `srun hostname`을 견준다. 그리고 할당은 셸과 함께 끝난다. 노트북을 덮으면 끊긴 `ssh` 연결이 둘을 함께 데려간다.

> [!note]- 더 깊이 · Deeper
> - **대화형 셸.** 명령을 주지 않으면 `salloc`은 여러분의 기본 셸을 돌리고, 그것이 끝나면 할당을 돌려준다. 사이트 설정에 `LaunchParameters=use_interactive_step`이 있으면 그 셸을 할당된 노드에서 띄운다. Slurm FAQ는 20.11부터 이것을 대화형 셸을 얻는 권장 방법이라 하고, `srun --pty bash -i`는 더는 권하지 않는다.
> - **배열.** `%A`와 `%a`는 배열의 작업 번호와 태스크 번호를 파일 이름에 넣는다. `scancel <번호>`는 모든 태스크를, `scancel <번호>_3`은 하나를 취소한다. 번호는 사이트의 `MaxArraySize`보다 하나 작은 값까지이고, 기본값은 1,001이다. 영어 절의 탐색 스크립트는 태스크 번호 $i$를 4로 나눈 몫으로 학습률을, 나머지로 시드를 고른다. 노트북의 bash에서 `python` 대신 `echo`를 넣어 $i=0,\dots,11$에 대해 그 산수를 확인했다. 태스크 0–3은 첫째 학습률에 시드 0–3, 4–7은 둘째, 8–11은 셋째다.
> - **시간 한도.** `--time-min`은 더 일찍 시작할 수 있다면 Slurm이 작업의 한도를 주어진 값까지 낮추도록 허락한다.

### 6. 체크포인트: 무엇을 어떻게 저장하나

*한 문장으로:* 어떤 중단이든 마지막 저장 이후의 모든 것을 잃게 하고 재개는 저장한 것만큼만 좋으므로, 체크포인트는 스텝 경계에서 본 실행의 완전한 상태를 작업보다 오래 사는 저장소에 원자적으로 쓴 것이어야 하고, 그래야 재개한 실행이 같은 실행이 된다.

**문제.** `gpu-preempt`에서 FT-1은 50시간 동안 다섯 번쯤 멈춰지고(§7), 그때마다 다음 작업은 앞 작업이 저장해 둔 것에서 시작한다. 아무것도 없으면 스텝 0부터 다시, 가중치만 있으면 설정 파일이 말하는 것과는 다른 실행으로 시작한다.

**생각.** 다음 스텝이 읽을 모든 것을, 스텝과 스텝 사이에, 공유 저장소에, 임시 이름으로 써서 제자리로 이름을 바꿔 저장한다. 그리고 Slurm이 한도가 가깝다고 경고할 때 한 번 더 저장한다. 학습 재개에 대한 PyTorch의 안내도 옵티마이저에 대해 같은 말을 한다. 옵티마이저는 학습하는 동안 갱신되는 버퍼와 파라미터를 품고 있으니 모델의 상태 곁에 그 상태도 저장하고, 에폭도 저장하라는 것이다.

**대상 위에서: 무엇이 들어가나.** FT-1은 혼합 정밀도의 Adam으로 학습하므로([[02-foundations/ml-practice|9. ML 실무 §6]]) 체크포인트는 fp32 마스터 가중치와 Adam의 두 모멘트를 파라미터당 각 4바이트씩 담는다. $S=12\times3.0\times10^8=3.6$ GB이고, $C=3.6/0.5=7.2$ s에 쓴다. [[03-deep-learning/foundations/training-at-scale|1.3 §5]]의 16바이트 장부 가운데 16비트 사본과 기울기는 다음 스텝이 다시 만든다. 그다음이 *어느* 실행을 잇는지를 정하는 작은 것들이다. 학습률 스케줄이 스텝 카운터의 함수이니 스텝 카운터, 미니배치를 뽑으니 모든 난수 생성기의 상태, 에폭 안에서 로더의 위치, 레시피가 둔다면 EMA 사본(가중치의 지수 이동 평균), 그리고 설정·코드·이미지의 버전이다. 체크포인트는 최근 둘을 work에 둔다.

**어떻게.** 한 파일시스템 안의 이름 바꾸기는 원자적이므로, 저장 도중에 죽은 작업도 마지막으로 온전한 체크포인트를 그대로 남긴다. 그리고 시그널 처리기는 깃발만 세우고, 루프가 옵티마이저 스텝 사이에서 그 깃발을 본다. 파이썬은 처리기를 나중에, 메인 스레드에서, 바이트코드 두 개 사이에 돌리므로, 스스로 저장하는 처리기는 갱신이 절반쯤 된 가중치를 붙잡을 수 있다. 영어 절의 루프는 이 모두를 작은 문제 위에서 한다. Slurm의 경고 대신 프로세스가 자기에게 시그널을 보낸다. Adam으로 4,096개 점에 선형 모형을 맞추고, 미니배치는 시드를 준 생성기에서 뽑으며, 학습률은 1,000 스텝에 걸친 코사인 스케줄이다. 상태는 가중치, Adam의 두 모멘트, 스텝 카운터, 생성기 상태의 다섯 가지이고, 저장은 임시 이름으로 쓴 뒤 `os.replace`로 이름을 바꾼다. 출력은 영어 절과 같고, 요약하면 이렇다.

| 실행 | 재개한 스텝 | 재개 때 학습률 | 더 돈 스텝 | 마지막 손실 | 중단 없는 실행과의 최대 차이 |
|---|---:|---:|---:|---:|---:|
| 첫 창 | — | — | 400에서 저장하고 멈춤 | — | 파일에 m, rng, t, v, w |
| 전체 상태에서 재개 | 400 | 0.0327 | 600 | 0.003350 | 0.0e+00 |
| 가중치만으로 재개 | 0 | 0.0500 | 1,000 | 0.003352 | 1.7e-03 |
| 중단 없음 | — | — | 1,000 | 0.003350 | — |

전체 상태에서 재개한 실행은 한 번도 멈추지 않은 실행과 비트 하나까지 같다. 가중치만으로 재개한 실행은 스케줄을 0.0327이 아니라 꼭대기의 0.0500에서 다시 시작하고, 처음 400개 미니배치를 다시 뽑고, 400 스텝을 더 — 모두 1,400 스텝 — 학습해 다른 가중치에서 끝난다. 이 볼록한 장난감에서는 손실이 거의 알아채지 못하지만(0.003352 대 0.003350), 학습 후반의 정책에서 학습률이 꼭대기로 되돌아가면 스케줄의 감쇠가 이룬 것의 상당 부분을 무를 수 있다. 어느 쪽이든 결과는 더는 설정 파일이 말하는 그 실행이 아니다.

> **체크포인트의 정의.** **체크포인트**(checkpoint)는 *학습 실행이 멈춘 적 없는 것처럼 그대로 이어 갈 수 있게 해 주는 저장된 상태*다. 한 스텝 경계에서 본 실행의 완전한 상태이지, 모델의 사본이 아니다. 정의 조건 넷. **완전하다**: 다음 스텝이 읽는 모든 양 — 가중치, 옵티마이저 모멘트, 스텝 카운터, 모든 난수 생성기의 상태, 데이터 위치 — 과 그것을 해석하는 버전들을 담는다. **스텝 경계에서** 찍고, 갱신 도중에는 찍지 않는다. **원자적으로 쓴다**: 임시 이름으로 쓴 뒤 옛 파일 위로 이름을 바꾸므로, 새 파일이 온전해질 때까지 앞의 체크포인트가 유효하다. 그리고 **오래 간다**: 작업보다 오래 살고 다음 작업의 노드가 볼 수 있는 저장소에 있다.
>
> $$S=b\,N,\qquad C=\frac{S}{\beta_w},\qquad b=\underbrace{4}_{\text{fp32 weights}}+\underbrace{4+4}_{\text{Adam's }m,\ v}\ \big(+\,4\ \text{with an EMA copy}\big)$$
>
> 여기서 $N$은 파라미터 수, $b$는 파라미터당 바이트, $S$는 체크포인트의 크기, $\beta_w$는 저장하는 곳의 쓰기 대역폭, $C$는 쓰는 동안 학습이 멈춰 서는 시간이다. 그러니 체크포인트의 비용은 데이터가 아니라 모델과 함께 자란다.
>
> - **예**: FT-1: work에서 $S=3.6$ GB, $C=7.2$ s. 위의 루프는 체크포인트에서 비트 하나까지 같게 재개한다.
> - **비예**: 가중치만. 위의 루프를 가중치만으로 재개하면 스케줄이 꼭대기에서 다시 시작하고, 미니배치 400개를 되풀이하고, 400 스텝을 더 학습해 $1.7\times10^{-3}$만큼 떨어진 곳에서 끝난다. 저장한 가중치는 [[02-foundations/ml-practice|9. ML 실무 §1]]이 검증 점수로 고르는 체크포인트다. 모델을 평가하기에는 충분하지만 실행을 이어 가기에는 모자란다.
> - **비예**: 노드 자신의 디스크에 쓴 완전한 체크포인트. 모든 항목이 들어 있지만, 다른 노드에서 도는 다음 작업은 그것을 보지 못한다.
> - **왜 중요한가**: §7의 산수는 중단 한 번의 값이 저장하지 않은 작업과 재시작뿐이라고 가정한다. 불완전한 체크포인트는 어떤 간격으로도 고칠 수 없는 값을 더한다. 재개한 실행이 다른 실험이 되기 때문이다([[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §6]]).

**함정.** 가중치만 저장하기, 노드 자신의 디스크에 저장하기, 시그널 처리기 안에서 저장하기, 그리고 한도에서 SIGTERM과 SIGKILL 사이의 30 s를 믿기다. FT-1의 7.2 s는 조용한 파일시스템에서 들어맞았을 뿐이고, 그것은 계획이 아니다.

> [!note]- 더 깊이 · Deeper
> **경고가 파이썬에 닿을까?** `--signal=USR1@600`은 한도 약 600 s 전에 — Slurm의 사건 처리 해상도 때문에 최대 60 s 더 일찍 — 모든 작업 단계에 SIGUSR1을 보내고, 기본적으로 배치 셸에는 보내지 않는다. `B:` 접두어를 붙이면 배치 셸만 받는다. 그것이 여러분의 파이썬 프로세스에 닿는지는 그 프로세스가 어떻게 시작됐는지 — `srun`으로, 컨테이너 안에서, 워커 프로세스를 띄우는 실행기 밑에서 — 에 달렸으니, 짧은 작업에 `scancel --signal=USR1 <작업 번호>`로 한 번 시험하고 로그에서 처리기가 남긴 줄을 찾는다. **이름 바꾸기가 안전한 이유.** 리눅스의 `rename(2)`는 이미 있는 이름을 원자적으로 바꾸므로 어떤 프로세스도 그 이름이 비어 있는 순간을 보지 못하고, 파이썬의 `os.replace`는 성공한 이름 바꾸기가 POSIX 시스템에서 원자적이라고 밝힌다. 한 파일시스템 안에서의 이야기이고, 두 파일시스템 사이에서는 실패할 수 있다.

### 7. 얼마나 자주 저장하나: 체크포인트 간격

*한 문장으로:* 자주 저장하면 쓰는 데 시간을 버리고 드물게 저장하면 다시 하는 데 시간을 버리며, 중단이 무작위로 오면 가장 좋은 간격은 저장 시간과 중단 사이 평균 시간의 곱의 두 배에 제곱근을 씌운 값이다.

**문제.** `gpu-preempt`에서 FT-1은 평균 10 h마다 멈춰진다. 1분마다 저장하면 학습의 많은 부분이 쓰기에 가고, 몇 시간마다 저장하면 많은 부분이 잃은 작업을 다시 하는 데 간다. 그 사이 어딘가에 가장 좋은 간격이 있다.

**쉬운 말로 한 생각.** 두 비용이 서로 반대로 당긴다. 저장은 할 때마다 $C$가 들어서 학습에서 저장이 차지하는 몫은 $1/\tau$처럼 줄어든다. 중단은 올 때마다 마지막 저장 이후의 작업 — 평균으로 간격의 절반 — 을 버리므로 그 손실은 $\tau$와 함께 커진다. 가장 좋은 간격은 둘을 맞추는 곳이고, 가장 좋은 간격에서 둘은 정확히 같아진다.

**규칙.** 중단이 서로 독립으로, 평균 간격 $M$이 일정하게 온다고 하자. 간격이 평균 $M$의 지수분포를 따르는 포아송 과정이다([[02-foundations/probability|3. 확률 §2]]). 학습 한 시간마다 저장은 $C/\tau$를 치르고, 중단은 $1/M$의 비율로 와서 평균 $\tau/2$씩을 잃는다. $C\ll\tau\ll M$이어서 한 구간이 두 번 중단되는 일은 드물다. 그러니 $W$ 가운데 버려지는 몫은

$$w(\tau)=\frac{C}{\tau}+\frac{\tau}{2M}$$

이다. 저장이 드물어질수록 첫 항은 줄고, 저장하지 않은 구간이 길어질수록 둘째 항은 늘기 때문이다. 도함수를 0으로 놓으면, $-C/\tau^2+1/(2M)=0$([[02-foundations/engineering-math|0.5 §1]]), 상자 안의 간격이 나온다. 체크포인트 문헌이 Young과 Daly에게 돌리는 고전적인 1차 분석이 이것이다(Aupy 외, 2013). 이 페이지는 그 논문들을 인용하는 대신 직접 유도한다.

> **체크포인트 간격의 정의.** **체크포인트 간격**(checkpoint interval) $\tau$는 *두 저장 사이의 학습 시간*이다. 저장에 쓰는 시간과 중단으로 잃는 작업을 맞바꾸는, 작업이 하는 선택이지 클러스터의 성질이 아니다. 1차 최적의 정의 조건 넷. 중단은 **무작위이고 기억이 없다**: 서로 독립이고, 평균 간격 $M$이 일정하다. 저장은 **고정된 $C$가 들고**, 그동안 학습은 멈춰 선다. 중단은 **마지막으로 끝난 저장 이후의 작업을 정확히 잃는다**. 완전한 체크포인트(§6)가 이것을 보장한다. 그리고 **저장 시간은 간격보다, 간격은 중단 사이 시간보다 훨씬 짧다**($C\ll\tau\ll M$). 그래서 한 구간이 두 번 중단되는 일은 거의 없고, 한 번 중단되면 평균으로 자기 절반을 잃는다.
>
> $$\tau^\star=\sqrt{2CM},\qquad w(\tau^\star)=\sqrt{\frac{2C}{M}},\qquad \frac{C}{\tau^\star}=\frac{\tau^\star}{2M}=\sqrt{\frac{C}{2M}}$$
>
> 여기서 $\tau^\star$는 $w(\tau)=C/\tau+\tau/2M$을 최소로 만드는 간격이다. 그러니 최적에서 두 낭비는 같아서 각각 전체의 절반이고, 간격은 $C$와 $M$의 곱으로만, 낭비는 그 비로만 정해진다.
>
> - **예**: `gpu-preempt` 위의 FT-1. $C=7.2$ s $=0.002$ h, $M=10$ h이면 $\tau^\star=\sqrt{0.04}=0.2$ h $=12$분이고 $w=0.02$다. 1차 근사로 50 h 동안 저장에 0.50 h, 잃는 작업에 0.50 h다.
> - **비예**: 48 h 한도. 무작위가 아니다 — 언제 오는지 안다 — 그러니 $M$이 아니다. 그에 대한 답은 더 짧은 $\tau$가 아니라 아무것도 잃지 않는 §6의 경고 때 저장이다.
> - **비예**: "안전하게 1분마다". 그러면 저장만으로 실행의 $C/\tau=0.002/0.0167=12\%$, FT-1의 50 h 가운데 6 h를 치른다. $\tau^\star$에서의 낭비의 여섯 배다.
> - **왜 중요한가**: 최솟값 근처는 평평하고 양 끝은 가파르므로, 규칙이 할 일은 열 배쯤 틀린 간격을 걸러 내는 것이다. 그리고 무엇을 살 수 있는지 말해 준다. $C$를 반으로(더 빠른 파일시스템, 더 작은 체크포인트), 또는 $M$을 두 배로(조용한 파티션) 하면 낭비가 $\sqrt2$배 준다.

**정확한 모형.** 1차 규칙은 한 구간에 중단이 많아야 한 번이라고 가정하고, 돌아오는 데 걸리는 시간을 잊는다. 둘을 모두 세는 것은 짧은 계산이다. 학습 $\tau$와 그 저장으로 된 구간 하나, $s=\tau+C$를 보자. 이 구간은 확률 $e^{-s/M}$로 중단 없이 돌므로, 깨끗하게 한 번 돌기 전까지의 중단 횟수는 평균이 $(1-e^{-s/M})/e^{-s/M}=e^{s/M}-1$인 기하분포다([[02-foundations/engineering-math|0.5 §5]]). 중단은 저마다 그 구간에서 이미 쓴 시간 — $s$보다 먼저 왔다는 조건에서 평균 $M-s/(e^{s/M}-1)$로, $\int_0^s x\,e^{-x/M}\,dx/M$을 부분적분한 뒤 중단이 $s$보다 먼저 올 확률 $1-e^{-s/M}$로 나눈 값이다 — 에 재시작 $R$을 더한 값을 치른다. $R$은 대기열 대기, 다시 스테이징, 다시 불러오기로, FT-1에서는 $0.2+0.0500+0.0010=0.2510$ h다. 깨끗한 한 번의 $s$를 더하면

$$E[T_{\text{seg}}]=s+\big(e^{s/M}-1\big)\Big(M-\frac{s}{e^{s/M}-1}+R\Big)=\big(e^{s/M}-1\big)\big(M+R\big)$$

이다. 두 $s$ 항이 지워지기 때문이다. 실행 전체는 $E[T]=(W/\tau)(M+R)(e^{(\tau+C)/M}-1)$이 걸린다. $x=(\tau+C)/M$로 두고 $e^x-1\approx x+x^2/2$로 펼치면([[02-foundations/engineering-math|0.5 §2]]) 1차 항이 $W(1+C/\tau)(1+R/M)$을, 제곱 항이 약 $W\tau/2M$을 주어, 합하면 $W(1+C/\tau+\tau/2M+R/M)$에 더 작은 항들이 붙는다. 1차 낭비에, 어떤 $\tau$도 건드리지 못하는 재시작의 몫 $R/M$을 더한 것이다.

**대상 위에서.** $\tau=12$분에서 $E[T]=250\times10.2510\times(e^{0.0202}-1)=52.29$ h다. 저장 0.50 h, 잃는 작업 0.51 h, 예상 선점 5.10번에 걸친 재시작 1.28 h다. §11은 정확한 최적을 11.92분에서 찾고, 거기서 초과분은 반올림하면 같은 2.29 h다.

| 간격 $\tau$ | 예상 시간 (h) | 저장 (h) | 잃는 작업 (h) | 재시작 (h) |
|---|---:|---:|---:|---:|
| 3분마다 | 53.44 | 2.00 | 0.14 | 1.31 |
| $\tau^\star=12$분 | 52.29 | 0.50 | 0.51 | 1.28 |
| 에폭마다, 19.5분 | 52.42 | 0.31 | 0.83 | 1.28 |
| 10 에폭마다, 3.26 h | 60.62 | 0.03 | 9.11 | 1.48 |
| 끝에서만 | 1,511.44 | 0.00 | 1,424.43 | 37.01 |

**함정.** N 에폭이 얼마나 걸리는지 묻지 않고 습관처럼 "N 에폭마다" 저장하기. 10 에폭마다는 3.26 h이고, $\tau^\star$보다 8.3 h를 더 치른다. 아예 저장하지 않기. 그러면 FT-1은 평균 10 h마다 선점하는 파티션에서 50 h를 한 번에 깨끗하게 달려야 하고, 그전에 $e^{5}-1=147$번의 중단이 예상되며, 실행은 63일이 걸린다. 체크포인트야말로 선점형 파티션을 쓸 수 있게 해 주는 것이다. 그리고 작은 $\tau$가 모든 것을 고쳐 주리라 기대하기. 재시작 1.28 h는 중단마다 치르는 값이어서, 더 작은 $R$이나 더 큰 $M$만이 줄인다.

> [!note]- 더 깊이 · Deeper
> **선점이 보내는 것.** Slurm은 선점할 작업을 고르면 작업의 끝을 지금에 유예 시간(grace time)을 더한 시각으로 정하고, 곧바로 SIGCONT와 SIGTERM을 보내며, 그 끝이 오면 SIGCONT, SIGTERM, SIGKILL을 차례로 보낸다. 유예 시간은 사이트가 정하지 않으면 0이다. 그다음 작업이 취소될지, 다시 대기열에 들어갈지, 일시 정지될지는 사이트의 `PreemptMode`가 정한다(Slurm, 선점 문서). 다시 대기열에 들어간 배치 작업은 같은 작업 번호로 스크립트를 처음부터 다시 시작한다. 그래서 `latest`에서 재개하는 스크립트가 다시 대기열에 들어갈 때에도 맞는 스크립트다. **정확한 최적**은 §11 탐색의 모든 $M$에서 $\tau^\star$보다 0.08분, 4.8 s 짧다. **`gpu`에서는** 무작위 중단이 노드 고장이고 선점보다 훨씬 드물다. §11의 $M=160$ h 열은 $\tau^\star$를 48분에 둔다.

### 8. 데이터를 GPU까지: 스테이징과 입력 파이프라인

*한 문장으로:* 초당 샘플 1,024개를 먹는 GPU 넷은 데이터가 그만큼 빨리 오지 못하면 굶고, 같은 180 GB가 몇 개의 파일로 나뉘었는지만으로 복사에 3분이나 33분이 걸리고 학습에 50시간이나 77시간이 걸린다 — 파일마다 바이트는 치르지 않는 메타데이터 요청을 한 번씩 치르기 때문이다.

**문제.** FT-1의 GPU 넷은 50시간 동안 초당 샘플 1,024개 — 이미지 3,072장, 153.6 MB — 를 먹고, 코퍼스는 모두와 함께 쓰는 파일시스템에 있다.

**생각.** 파일은 두 가지 값을 치른다. 열어 달라는 요청 한 번과, 그다음의 바이트다. 작은 파일에서는 요청이 느린 쪽이다. 그러니 코퍼스를 커다란 **샤드**(shard) 몇 개로 저장하고, 작업이 시작할 때마다 노드 자신의 디스크로 한 번 복사하고 — 이것이 **스테이징**(staging)이다 — 학습은 로컬에서 읽게 한다. Slurm은 작업의 스크립트 말고는 어떤 파일도 옮겨 주지 않으므로, 복사는 스크립트의 한 줄이다(§4). 그리고 파이프라인 전체는 가장 느린 단계의 속도로 간다는 것을 기억한다.

**규칙.** 합쳐서 $B$바이트인 파일 $n$개를 스테이징하는 데는

$$t_{\text{stage}}=\frac{n}{r_f}+\frac{B}{\beta_r}$$

가 걸린다. 파일마다 $r_f$의 비율로 한 번 열고, 바이트는 $\beta_r$로 흘러오기 때문이다. 교과용 클러스터에서 파일 하나가 $\beta_r/r_f=500$ kB보다 작으면 크기가 아니라 파일 수가 시간을 정한다. 학습이 돌기 시작하면 입력 파이프라인이 따라와야 한다.

> **입력 파이프라인 처리량의 정의.** 학습 작업의 **입력 처리량**(input throughput)은 *데이터 로더가 준비된 샘플을 내놓는 속도*다. 데이터를 어디서 읽고 어떻게 저장했는지가 정하는 여러 독립적인 상한 가운데 가장 작은 것이고, GPU의 성질이 아니다. 정의 조건 셋. **모든 단계가 상한을 건다**: 초당 여는 파일 수를 샘플당 파일 수로 나눈 것, 읽기 대역폭을 샘플당 바이트로 나눈 것, 할당된 CPU 코어가 샘플을 디코딩하는 속도다. GPU는 **정해진 속도 $r_{\text{need}}$로 먹는다**. 배치를 스텝의 계산 시간으로 나눈 값이다. 그리고 **파이프라인이 내놓지 못하는 것은 GPU가 기다린다**. 스텝은 자기 계산 시간과 배치가 도착하는 시간 가운데 긴 쪽이 걸린다.
>
> $$r_{\text{in}}=\min\Big(\frac{r_f}{f},\ \frac{\beta}{s},\ r_{\text{cpu}}\Big),\qquad u=\min\Big(1,\ \frac{r_{\text{in}}}{r_{\text{need}}}\Big),\qquad t_{\text{train}}=\frac{W}{u}$$
>
> 여기서 $f$는 샘플당 파일 수, $s$는 샘플당 바이트, $\beta$는 데이터를 읽는 곳의 대역폭, $r_{\text{cpu}}$는 디코딩 속도, $u$는 GPU가 바쁜 시간의 비율이다. 그러니 가장 느린 단계가 속도를 정하고, 그보다 빠른 GPU는 더 오래 기다릴 뿐이다.
>
> - **예**: 작은 파일을 제자리에서 읽는 FT-1. $\beta/s=10^9/150{,}000=6{,}667$에 비해 $r_f/f=2{,}000/3=666.7$ 샘플/s이므로 $r_{\text{in}}=666.7$, $u=666.7/1{,}024=0.651$이다. 스텝마다 $0.25/0.651=0.384$ s가 걸리고 그 가운데 0.134 s는 데이터를 기다리며, 50 h의 학습이 76.8 h가 된다. 스테이징한 샤드에서는 바이트 상한이 $2\times10^9/150{,}000=13{,}333$ 샘플/s이므로, 코어가 따라온다면 $u=1$이다.
> - **비예**: 작은 파일 배치에 더 빠른 GPU. $r_{\text{need}}$를 올려 $u$를 낮추고, 76.8 h는 그대로 둔다.
> - **왜 중요한가**: 학습 작업의 GPU가 일부 노는 가장 흔한 이유이고, §9의 사용률 수치가 경고하는 바로 그것이다.

**대상 위에서.** 샤드 200개를 스테이징하면 $200/2{,}000+180=180.1$ s, 3.0분이고, 이미지마다 파일 하나면 $3{,}600{,}000/2{,}000+180=1{,}980$ s, 33.0분이다. 같은 바이트에 열한 배의 시간이고, 선점될 때마다 다시 치르므로 §7의 재시작 $R$이 15.06분에서 45.06분으로 는다. 샤드는 제자리에서 읽어도 GPU를 바쁘게 한다. 바이트는 애초에 문제가 아니었다. 다만 그러면 에폭마다 공유 파일시스템으로 돌아가서, 실행 동안 $153.6\times180$ GB $=27.6$ TB를 모두가 함께 쓰는 서버에서 읽는다.

**함정.**

- *샘플이나 이미지마다 파일 하나.* 쿼터가 거절하고(§2), 스테이징은 열한 배가 걸리고, 제자리에서 읽으면 GPU를 굶긴다.
- *`--cpus-per-task`를 잊기.* Slurm은 따로 말하지 않으면 태스크당 프로세서 하나를 준다. 작업을 할당된 코어에 가두는 사이트라면 로더의 워커 프로세스가 모두 코어 하나를 나누어 쓰고, 데이터를 어떻게 저장했든 $r_{\text{cpu}}$가 상한이 된다.
- *scratch로 "스테이징"하기.* 같은 메타데이터 서버를 쓰는 같은 공유 파일시스템이다. 파일은 자리만 옮겼다.

샤드는 샘플을 여럿 담은 파일이면 무엇이든 된다. 에피소드의 이미지를 묶은 `tar` 묶음, HDF5 파일, Parquet 파일이다. 어느 형식을 쓸지는 따로 따질 문제다. 로더는 3,600,000개 대신 200개를 열고, 하나하나를 앞에서 뒤로 읽는다.

> [!note]- 더 깊이 · Deeper
> **노트북에서 본 것.** 같은 효과가, 더 작게, 노트북의 내장 SSD에서도 보인다. 5 kB 파일 30,000개(150 MB)로 된 작은 코퍼스를 `rsync`로 다섯 번 복사하고(시도마다 사본을 지웠다), 같은 파일을 묶은 `tar` 하나도 그렇게 복사했다. 이 페이지를 쓴 macOS 노트북에서다. 명령은 영어 절에 있다. 파일 세기, `tar`로 묶기, `/usr/bin/time -p rsync -a`로 두 가지를 복사하기다. `--no-xattrs --no-mac-metadata`는 macOS의 `tar`가 파일 속성을 저장하지 않게 하고, 리눅스의 GNU `tar`는 `--xattrs`로 청하지 않는 한 속성을 저장하지 않는다.
>
> | 시도 | 파일 30,000개 (s) | 169 MB 묶음 하나 (s) | 비 |
> |---:|---:|---:|---:|
> | 1 | 49.78 | 4.56 | 10.9 |
> | 2 | 37.10 | 2.76 | 13.4 |
> | 3 | 31.54 | 2.59 | 12.2 |
> | 4 | 11.80 | 1.41 | 8.4 |
> | 5 | 11.08 | 1.30 | 8.5 |
>
> 시간은 `time -p`의 `real` 줄이고 나머지는 잘라 냈다. 노트북이 그때 달리 무엇을 하느냐에 따라 절대 시간은 네 배까지 움직였지만, 모든 시도에서 파일 쪽이 8배에서 13배 걸렸다. 노트북은 병렬 파일시스템이 아니고 이것은 교과용 클러스터의 숫자도 아니지만, 방향은 같다.

### 9. 도는 작업 지켜보기

*한 문장으로:* 며칠씩 도는 작업은 방해하지 않고 살펴야 한다 — 대기열 상태, 로그, GPU, 사후 기록을 통해서 — 그리고 100%에 한참 못 미치는 GPU 사용률은 시간이 GPU 아닌 어딘가로 새고 있다는 경고다.

**문제.** 작업이 여섯 시간째 돌고 있다. 건강한가, 그리고 빠른가?

**생각.** 창이 넷이다. 대기열: `squeue --me`의 상태와 사유(§4). 로그: 100 스텝마다 FT-1의 스크립트는 스텝, 손실, 초당 샘플 수, 그리고 스텝마다 데이터를 기다린 초를 찍는다. 마지막 숫자 하나가 §8의 굶주림을 다른 모든 원인과 갈라 준다. GPU: 배치 스크립트에서 `srun` 앞에 둔 한 줄이 1분마다 모든 GPU의 사용률을 로그로 남긴다. 그리고 끝난 뒤의 `sacct`: 요청에 가까운 `MaxRSS`와 함께 `OUT_OF_MEMORY`면 메모리를 더 달라거나 한 번에 덜 불러오라는 뜻이고, `TIMEOUT`이면 §5의 사슬이 필요했다는 뜻이다. 영어 절의 두 줄은 NVIDIA의 `nvidia-smi` 문서로 확인했고 여기서 실행하지 않았다. 작업 내내 1분마다 모든 GPU의 사용률을 기록하는 `nvidia-smi dmon -s u -d 60`을 뒤에서 돌리는 줄과, 자세한 읽기 한 번인 `nvidia-smi -q -d UTILIZATION`이다.

작업 안에서 기록하는 것이 믿을 만한 방법이다. 밖에서 `srun --jobid=<번호>`로 띄운 단계는 작업 자신의 단계 뒤에서 기다릴 수 있다. Slurm의 작업 단계는 20.11판부터 기본적으로 배타적이기 때문이다(Slurm FAQ).

> **GPU 사용률의 정의.** `nvidia-smi`가 보고하는 **GPU 사용률**(GPU utilization)은 *최근 표본 기간 가운데 하나 이상의 커널이 GPU에서 실행되고 있던 시간의 백분율*이다. 일이 아니라 시간을 재는 값이고, 표본 기간은 제품에 따라 1/6 s에서 1 s 사이다(NVIDIA, `nvidia-smi` 문서). 정의 조건 셋. **순간마다 전부 아니면 전무다**: GPU의 작은 부분만 바쁘게 하는 커널도 GPU를 가득 채우는 커널과 똑같이 셈한다. **표본 기간에 걸친 평균이다**: 기간보다 짧은 틈은 그 안에 뭉개진다. 그리고 **원인에 대해 말이 없다**: 노는 GPU는 데이터를 기다리든, 호스트를 기다리든, 아무것도 기다리지 않든 똑같아 보인다.
>
> $$U=\frac{t_{\text{kernel}}}{t_{\text{sample}}}\times100\%,\qquad U\le u\times100\%\ \ \text{when the input pipeline caps the steps}$$
>
> 여기서 $t_{\text{kernel}}$은 기간 $t_{\text{sample}}$ 안에서 커널이 하나라도 실행되던 시간이고, $u$는 §8의 바쁜 비율이다. 그러니 굶주린 입력은 $u$ 이하의 사용률로 드러나고, 꽉 찬 수치는 커널이 돌고 있었다는 것만 말한다.
>
> - **예**: 작은 파일을 제자리에서 읽는 FT-1. 0.384 s 스텝마다 0.134 s를 데이터에 기다리므로 $u=0.651$이고, 네 GPU의 수치는 65%를 넘을 수 없다.
> - **비예**: 100%를 "GPU를 잘 쓰고 있다"로 읽기. 루프라인에서 한참 아래 있는 커널 — 메모리에 묶였거나 GPU를 채우기엔 너무 작은 커널 — 은 산술 장치 대부분을 놀리면서도 수치를 100%로 둔다([[03-deep-learning/foundations/gpu-computing|1.4 §3]]).
> - **왜 중요한가**: 가장 싼 경보다. 65%에서 도는 작업은 할당의 3분의 1을 흘리고 있고, 그 새는 곳은 거의 언제나 GPU 바깥이다.

**함정.** 반사적으로 데이터를 탓하기. launch 오버헤드와 호스트 동기화도 커널 사이에 틈을 남긴다([[03-deep-learning/foundations/gpu-computing|1.4 §4, §7]]). 로그의 데이터 대기 열이 입력 굶주림을 그것들과 갈라 준다. 작은 파일을 읽는 FT-1은 0.384 s 스텝마다 0.134 s를 기다린다. 35% 전부다.

### 10. GPU를 더, GPU를 빌려서, 그리고 함께 쓰는 기계

*한 문장으로:* GPU 넷이 모자라거나 대기열이 너무 길 때, GPU를 늘리면 데이터가 도착해야 하는 속도가 배로 늘고, GPU를 빌리면 대기열을 청구서와 바꾸며, 남과 함께 쓰는 기계는 쓰는 만큼만 가져가라고 요구한다.

**문제.** 마감이 가까우면 `gpu`에서 학습된 정책까지 걸리는 FT-1의 72.60 h가 너무 길 수 있고, 정책이 더 커지면 GPU 넷으로는 모자란다. 빠져나갈 두 길 — GPU를 더 쓰거나, 빌려 쓰거나 — 은 저마다 이 페이지가 계산한 숫자 하나를 움직이고, 어느 쪽이든 함께 쓰는 기계는 여러분에게 요구하는 것이 있다.

**GPU를 더.** FT-1은 이미 넷에서 데이터 병렬로 학습한다. `torchrun`이 GPU마다 워커 프로세스를 하나씩 띄우고, 저마다 정책의 복제본을 가지고 배치 256개 가운데 64개를 맡는다. PyTorch의 `DistributedDataParallel`은 만들어질 때 랭크 0의 상태를 모든 복제본에 복사하고, 역전파 동안 기울기를 버킷 단위로 프로세스 사이에서 평균 내므로 모든 복제본이 같은 스텝을 밟는다. 복제본이 늘 같으니 체크포인트는 프로세스 하나 — 번호가 매겨진 워커 가운데 첫째인 랭크 0 — 가 쓴다. GPU마다 전체 모델 상태, 파라미터당 16바이트, FT-1이면 4.8 GB를 쥐며, 이것을 나누는 것은 샤딩 기법의 일이다([[03-deep-learning/foundations/training-at-scale|1.3 §5]]). GPU와 함께 커지는 것은 입력이다. GPU 여덟 개는 초당 2,048 샘플을 먹고, 작은 파일 배치는 그들을 32.6%의 시간만 먹일 것이다. 노드 여럿이면 `--nodes=2`, 노드마다의 실행기, 그 사이의 네트워크가 더해진다. 이 페이지 너머다.

**GPU를 빌려서.** 클라우드 GPU에는 클러스터와 같은 뜻의 대기열이 없다. 자원이 남아 있으면 요청하는 대로 인스턴스가 시작하고, 바쁘든 놀든 할당된 모든 시간에 값이 매겨진다. GPU-시간당 USD 2.00이라는 교과용 값으로, FT-1은 스테이징한 샤드로 USD 405(202.4 GPU-시간, §11), 제자리에서 읽는 작은 파일로 USD 621(310.3 GPU-시간)이다. 느린 저장 배치가 더 쓴 108 GPU-시간이 청구서에서 USD 216이 되고, 저장소와 데이터 전송이 그 위에 청구될 수 있다. 제공자가 도로 가져갈 수 있는 용량은 흔히 할인해서 파는데, `gpu-preempt`처럼 움직이므로 제공자의 $M$으로 §7을 그대로 쓴다. 교과용 클러스터에서 48 h 작업이 기다리는 20 h가 돈으로 되사는 것이다.

**함께 쓰는 기계.**

- 로그인 노드에서는 무거운 일을 하지 않는다(§1). 시험은 짧은 대화형 할당에서(§5).
- 쓰는 만큼 요청한다. GPU 넷을 쥐고 하나만 쓰는 작업은 셋을 남에게서 빼앗고 여러분의 공정 분배 몫을 쓴다.
- 스케줄러를 반복문으로 묻지 않는다(§4). `--mail-type`을 쓴다.
- 프로젝트가 끝나면 scratch를 치우고, 코퍼스는 실험마다가 아니라 한 벌만 둔다.
- 암호문구로 보호한 SSH 키로 로그인하고, 계정이나 키를 나누지 않으며, 작업 스크립트, 로그, 노트북, 저장소에 비밀번호나 접근 토큰을 절대 적지 않는다. 작업 스크립트와 로그는 공유 파일시스템에 있고, 거기서 누가 읽을지는 의도가 아니라 파일 권한이 정한다.

### 대상으로 한 번 끝까지 · Worked case

제출부터 학습된 정책까지의 FT-1을 여섯 단계로 따라간다. 단계마다 기호에서 규칙으로, 규칙에서 숫자로 가고, 모든 숫자는 §11이 출력한다.

**1단계 — 예산.** 학습 시간은 스텝 수 곱하기 스텝 시간이고, 할당은 거기에 GPU 수를 곱한 것이다.

$$W=n_{\text{steps}}\,t_{\text{step}}=720{,}000\times0.25\ \text{s}=180{,}000\ \text{s}=50\ \text{h},\qquad G\,W=4\times50=200\ \text{GPU-hours}$$

스텝 하나가 GPU 넷을 함께 써서 0.25 s 걸리기 때문이다. 에폭으로는 $720{,}000\times256/1{,}200{,}000=153.6$번, 한 번에 19.5분이고, GPU는 초당 $r_{\text{need}}=256/0.25=1{,}024$ 샘플, 153.6 MB를 먹는다.

**2단계 — 쿼터에 비춘 저장 배치(§2).** $B=1{,}200{,}000\times3\times50$ kB $=180$ GB $\le1$ TB는 지켜진다. 이미지마다 파일 하나는 $n=3{,}600{,}000>1{,}000{,}000$이라 실패하고, 샤드 200개는 $n=200$이라 들어간다.

**3단계 — 스테이징과 입력 속도(§8).** $t_{\text{stage}}=n/r_f+B/\beta_r$는 작은 파일이면 $1{,}800+180=1{,}980$ s $=33.0$분, 샤드면 $0.1+180=180.1$ s $=3.0$분이다. 바이트는 어느 쪽이든 180 s이고, 나머지 30분은 파일 열기다. 제자리에서 읽으면 작은 파일은 $r_{\text{in}}=\min(2{,}000/3,\ 10^9/150{,}000)=666.7$ 샘플/s를 내놓으므로 $u=0.651$, 학습은 $50/0.651=76.8$ h가 걸린다. 스테이징한 샤드는 13,333 샘플/s를 내놓아 $u=1$, 50 h다.

**4단계 — `gpu`의 창(§5).** 창 하나는 $o=0.0510$ h를 치르고 12분마다 7.2 s씩 저장하므로 $w=(48-0.0510)\times0.2/0.202=47.47$ h의 학습을 담고, FT-1에는 $k=\lceil50/47.47\rceil=2$개의 창이 필요하다. 48 h, 그다음 $0.0510+(50-47.47)\times1.01=2.60$ h, 모두 $4\times50.60=202.4$ GPU-시간이다. 제자리에서 읽는 작은 파일은 76.8 h의 학습이 필요하다. 창 둘, 48 h와 29.57 h, 310.3 GPU-시간이다. 저장 배치 하나가 108 GPU-시간을 치르게 한다.

**5단계 — `gpu-preempt`의 간격(§6–§7).** $C=S/\beta_w=3.6/0.5=7.2$ s $=0.002$ h. $M=10$ h이면

$$\tau^\star=\sqrt{2CM}=\sqrt{2\times0.002\times10}=0.2\ \text{h}=12\ \text{min},\qquad w(\tau^\star)=\sqrt{2C/M}=0.02$$

이다. 거기서 저장과 잃는 작업이 각각 1%로 같기 때문이다. $R=0.2510$ h를 넣은 정확한 모형은 예상 선점 5.10번에 걸쳐 $E[T]=250\times10.2510\times(e^{0.0202}-1)=52.29$ h를 준다. 10 에폭마다 저장하면 60.62 h, 저장하지 않으면 1,511 h다.

**6단계 — 어느 파티션인가.** `gpu`에서는 대기열 20 h, 48 h 창, 3 h 창이 백필로 들어가기까지 2 h, 그리고 그 2.60 h — 학습된 정책까지 72.60 h다. `gpu-preempt`에서는 대기열 0.2 h와 예상 52.29 h — 52.49 h이고, 시뮬레이션한 실행 4,000개(§11) 가운데 95%가 시작 후 53.70 h 안에 끝난다. 선점형 파티션은 FT-1을 20 h 일찍 돌려주는데, 오로지 12분마다 체크포인트를 쓰기 때문이다. 대기 시간은 교과용 숫자다. 여러분 사이트에서 같은 비교는 그 사이트의 숫자로 여러분이 해야 한다.

### 11. 실습: 예산, 배치, 창, 체크포인트 간격

강의와 계산 절의 숫자는 모두 누구나 다시 돌려 확인할 수 있는 한 곳에서 나와야 한다. 고정한 대상 위의 여섯 부분을 NumPy와 표준 라이브러리로 된 코드 한 덩이가 출력한다. 영어 절의 코드가 그것이다. 예산, 쿼터에 비춘 두 저장 배치와 그 스테이징 시간, 입력 속도와 바쁜 비율, GPU-시간과 교과용 가격을 곁들인 `gpu`의 창, 체크포인트 간격 — 이름 붙인 간격들, $\tau$와 $M$에 대한 탐색, $M$마다의 정확한 최적, 정확한 공식을 검산하는 시뮬레이션 실행 4,000개 — 그리고 파티션마다 학습된 정책까지의 시간이다. 어디에도 시간 측정은 없다. 모든 숫자가 모형의 것이라 어느 기계에서나 출력이 같다.

**1–3부, 예산, 저장 배치, 입력:** GPU 4개로 $W=50.0$ h, 200 GPU-시간, 한 번에 19.5분인 153.6 에폭, 그리고 필요한 초당 1,024 샘플, 153.6 MB/s.

| 저장 배치 | 파일 | GB | work 쿼터에 들어가나 | 스테이징 |
|---|---:|---:|---|---:|
| 이미지마다 파일 하나 | 3,600,000 | 180.0 | 아니오 | 1,980.0 s = 33.0분 |
| 샤드 200개 | 200 | 180.0 | 예 | 180.1 s = 3.0분 |

| 읽는 곳 | 샘플/s | GPU 바쁜 비율 | 학습 (h) | 스텝당 데이터 대기 (s) |
|---|---:|---:|---:|---:|
| 작은 파일, 제자리 | 666.7 | 65.1% | 76.8 | 0.134 |
| 샤드, 제자리 | 6,666.7 | 100.0% | 50.0 | 0.000 |
| 샤드, 노드로 스테이징 | 13,333.3 | 100.0% | 50.0 | 0.000 |

**4부, 창:**

| 저장 배치 | 창 하나가 담는 학습 (h) | 창 | 경과 (h) | GPU-시간 | USD 2.00일 때 |
|---|---:|---:|---|---:|---:|
| 샤드, 스테이징 | 47.47 | 2 | 48.00 + 2.60 | 202.4 | 405 |
| 작은 파일, 제자리 | 47.52 | 2 | 48.00 + 29.57 | 310.3 | 621 |

**5부, 체크포인트 간격:** $C=7.2$ s, 불러오기 3.6 s, $R=15.06$분, 그리고 1차 근사로 $\tau^\star=12.00$분에 낭비 2.00%다. 이름 붙인 간격들은 §7의 표다. 탐색은 예상 초과분 $E[T]-W$를 시간으로, 잃는 작업을 괄호 안에 준다.

| $\tau$ \ $M$ | 2.5 h | 10 h | 40 h | 160 h |
|---:|---:|---:|---:|---:|
| 3분 | 7.82 (0.54) | 3.44 (0.14) | 2.36 (0.03) | 2.09 (0.01) |
| 6분 | 7.28 (1.05) | 2.55 (0.26) | 1.39 (0.07) | 1.10 (0.02) |
| 12분 | 7.88 (2.10) | 2.29 (0.51) | 0.95 (0.13) | 0.61 (0.03) |
| 30분 | 11.18 (5.40) | 2.77 (1.28) | 0.83 (0.32) | 0.36 (0.08) |
| 60분 | 17.82 (11.53) | 4.02 (2.60) | 1.05 (0.63) | 0.34 (0.16) |
| 120분 | 34.41 (26.66) | 6.80 (5.36) | 1.65 (1.27) | 0.44 (0.31) |
| 240분 | 86.07 (73.63) | 13.06 (11.49) | 2.94 (2.59) | 0.74 (0.63) |

| $M$ (h) | $\tau^\star$, 1차 근사 (분) | 정확한 최적 (분) | $\tau^\star$에서 초과분 (h) | 정확한 최적에서 (h) | 중단 횟수 |
|---:|---:|---:|---:|---:|---:|
| 2.5 | 6.00 | 5.92 | 7.28 | 7.28 | 20.82 |
| 10 | 12.00 | 11.92 | 2.29 | 2.29 | 5.10 |
| 40 | 24.00 | 23.92 | 0.82 | 0.82 | 1.26 |
| 160 | 48.00 | 47.92 | 0.33 | 0.33 | 0.31 |

$\tau=12$분, $M=10$ h에서 시뮬레이션한 실행 4,000개는 평균 52.29 h(표준오차 0.01 h)가 걸려 정확한 값 52.29 h와 같고, 95번째 백분위수는 53.70 h다.

**6부, 정책까지의 시간:** `gpu`에서 $20.0+48.00+2.0+2.60=72.60$ h, `gpu-preempt`에서 예상 $0.2+52.29=52.49$ h.

**표 읽기.** 강의가 예측했고 숫자가 이제 보여 주는 것 넷.

- **바이트가 아니라 파일 수가 데이터 경로를 정한다.** 같은 180 GB가 파일 3,600,000개로는 열한 배 느리게 스테이징되고, work에는 아예 들어가지 못하며, 제자리에서 읽으면 GPU를 65.1%만 바쁘게 해 학습 26.8 h와 108 GPU-시간을 잃는다. 샤드로는 같은 바이트가 제자리에서 읽어도 GPU를 바쁘게 한다.
- **최적 근처는 평평하고 양 끝은 가파르다.** $M=10$ h에서 6분부터 30분까지는 무엇이든 가장 좋은 값에서 0.5 h 안이지만, 10 에폭마다는 8.3 h를, 저장하지 않으면 1,459 h를 더 치른다.
- **$\tau^\star$는 $\sqrt M$처럼 자란다.** $M=2.5$, 10, 40, 160 h에 대해 6, 12, 24, 48분이다. 중단 간격 $M$이 네 배면 저장 간격은 두 배다.
- **공식과 시뮬레이션이 맞고, 재시작이 바닥이다.** 양쪽 모두 52.29 h이고 실행의 95%가 평균에서 1.41 h 안에 끝난다. $\tau^\star$에서 재시작 1.28 h가 저장과 잃는 작업을 합친 1.01 h보다 크다.

### 12. 이 페이지가 다루지 않는 것

모든 스케줄러, 모든 사이트, 모든 규모를 다루려는 페이지는 어느 것도 잘 가르치지 못하므로, 다음은 다른 페이지와 매뉴얼에 맡긴다. 다른 스케줄러 — PBS, LSF, Kubernetes 기반의 시스템 — 는 같은 생각을 다른 명령으로 말한다. 여러 노드에 걸친 학습의 깊은 이야기와 [[03-deep-learning/foundations/training-at-scale|1.3 §5]]가 이름을 대는 샤딩 기법, 비동기 체크포인트 라이브러리와 탄력적(elastic) 학습, 작업 사슬을 대신 짜 주는 워크플로 관리자는 다루지 않는다. GPU의 내부와 프로파일러는 [[03-deep-learning/foundations/gpu-computing|1.4]]다. 리눅스, 셸, `ssh`([[02-foundations/tools/linux-shell|12.1]]), Git([[02-foundations/tools/git-research-code|12.2]]), 파이썬 환경([[02-foundations/tools/python-research-code|12.3]]), 데이터 형식([[02-foundations/tools/config-data-formats|12.4]])은 이 트랙의 다른 페이지들이 맡는다. 데이터 로더의 워커 프로세스와 암달의 법칙이 거기에 거는 한계는 [[02-foundations/tools/concurrency|12.8 동시성 §7, §9]]다. 그리고 어느 한 사이트의 정책은 그 사이트의 사용자 안내서가 말한다.

### 읽고 나면

- [ ] 로그인 노드에서 도는 것과 계산 노드에서 도는 것을 말하고, 작업이 요청하지 않으면 GPU를 받지 못하는 이유를 말한다.
- [ ] 자기 작업의 배치 스크립트를 쓰고, `#SBATCH` 줄 안의 변수가 펼쳐지지 않는 이유를 말한다.
- [ ] `PD`, `R`, 끝 상태를 거치는 작업을 따라가고, 대기 사유를 읽는다.
- [ ] 데이터셋을 바이트와 파일 수의 쿼터에 비추어 보고, 코퍼스·체크포인트·환경이 어디에 있어야 하는지 말한다.
- [ ] 한도보다 긴 학습을 창으로 자르고($k=\lceil W/w\rceil$), 시간 초과를 견디는 의존성으로 잇고, 마지막 창이 짧은 시간을 요청하는 이유를 말한다.
- [ ] 체크포인트에 들어가야 할 것을 늘어놓고, 원자적으로 쓰고, 경고 시그널에 저장한다.
- [ ] $\tau^\star=\sqrt{2CM}$과 $E[T]=(W/\tau)(M+R)(e^{(\tau+C)/M}-1)$을 유도하고, 어떤 간격도 없애지 못하는 $R$의 몫을 말한다.
- [ ] 파일 수, 바이트, 속도로 스테이징 시간과 입력 처리량을 계산하고, 65%의 GPU 사용률을 그 원인까지 거슬러 읽는다.

### 스스로 점검

1. 작업이 `--partition=gpu --time=48:00:00`만 요청한다. 무엇을 받고, GPU를 "있으면" 쓰는 학습 스크립트는 어떻게 되는가?
2. FT-1에는 50 h의 학습이 필요하고 한도는 48 h다. 창은 몇 개이고, 마지막 창은 얼마나 길며, 무엇을 요청해야 하고, 그 요청이 왜 중요한가?
3. $M=40$ h인 파티션에서 FT-1의 $\tau^\star$와 1차 낭비는 얼마이고, $M=10$ h와 어떻게 다른가?
4. `afterok`으로 이은 창의 사슬이 첫 창 뒤에 멈춘다. 왜이고, 고치는 방법 둘은 무엇인가?
5. `nvidia-smi`가 네 GPU 모두 65%를 보인다. 원인 둘과, 둘을 갈라 주는 작업 로그의 숫자 하나를 대라.
6. 체크포인트에 모델 가중치만 들어 있다. 무엇이 빠졌고, 빠진 것마다 재개한 실행에 무슨 일을 하는가?
7. 같은 180 GB가 샤드 200개로는 3.0분, 파일 3,600,000개로는 33.0분에 스테이징된다. 나머지 30분은 어디로 가고, 뒤의 배치는 어떤 한도를 또 깨는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 노드의 코어와 메모리 몫이고, GPU는 없다. Slurm은 `--gres`나 `--gpus`로 요청한 작업에만 GPU를 준다. 스크립트는 실패하는 대신 CPU에서 느리게 학습한다. `--gres=gpu:4`를 더하고, GPU를 기대하는 스크립트는 GPU가 없으면 멈추게 한다.
> 2. 둘이다. 창 하나가 $(48-0.0510)\times0.2/0.202=47.47$ h를 담으니 $k=\lceil50/47.47\rceil=2$이고, 마지막에는 2.60 h가 필요하다. 3 h쯤 요청한다. 백필은 우선순위 높은 작업의 예정된 시작 전의 틈에 짧은 작업을 끼워 넣을 수 있지만 48 h 요청은 그 틈을 쓰지 못한다. 교과용 숫자로 대기가 20 h가 아니라 2 h다.
> 3. $\tau^\star=\sqrt{2\times0.002\times40}=0.4$ h $=24$분, $w=\sqrt{2\times0.002/40}=0.01$이다. 중단 간격이 네 배면 저장 간격은 두 배, 낭비는 절반이다. 정확한 초과분은 2.29 h에 비해 0.82 h다(§11).
> 4. 첫 창은 종료 코드 0의 완료가 아니라 `TIMEOUT`으로 끝나므로 `afterok`은 결코 충족될 수 없고, 두 번째 창은 `DependencyNeverSatisfied`로 기다린다. `afterany`나 `singleton`을 쓰거나, 모든 창이 경고에 저장하고 코드 0으로 끝나게 한다. 뒤의 방법은 한 번의 깨끗하지 못한 끝이 깨뜨린다.
> 5. 입력 굶주림 — 작은 파일, 로더에 모자란 코어(§8) — 이나 launch 오버헤드와 동기화가 남기는 호스트 쪽 틈이다([[03-deep-learning/foundations/gpu-computing|1.4 §4, §7]]). 스텝마다 데이터를 기다린 초가 둘을 갈라 준다. FT-1의 작은 파일에서는 0.384 s 스텝마다 0.134 s, 35% 전부다.
> 6. Adam의 두 모멘트, 스텝 카운터, 생성기 상태, 데이터 위치, EMA 사본이다. 이것들이 없으면 Adam은 평균을 처음부터 다시 쌓고, 스케줄은 꼭대기에서 다시 시작해 스텝을 더 돌며, 미니배치가 되풀이된다. §6의 루프에서는 학습률이 0.0327이 아니라 0.0500이고, 400 스텝을 더 돌며, 가중치가 $1.7\times10^{-3}$만큼 떨어진다.
> 7. 초당 2,000번의 속도로 여는 3,600,000번, 1,800 s로 간다. 바이트는 어느 쪽이든 180 s다. 그 배치는 work의 파일 쿼터도 깬다. 1,000,000개에 대해 3,600,000개다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, 위에서 고정한 두 대상만 쓴다. 문제마다 손잡이 하나 — 모델의 크기, 스텝 시간, 중단 비율, 저장 배치, 스크립트 — 를 바꾸므로 페이지의 숫자를 그대로 옮길 수 없다.

변형 **FT-2**는 FT-1에서 정책이 네 배 크고, $N=1.2\times10^9$($S=14.4$ GB, $C=28.8$ s), 스텝이 네 배 느린, $t_{\text{step}}=1.0$ s로 180,000 스텝을 도는 작업이어서 역시 $W=50$ h다. 코퍼스와 클러스터는 그대로다.

1. **그리기.** $M=2.5$ h인 파티션 위 FT-2의 그림을 그린다. 패널 (a)에서는 바뀌는 이름표를, 패널 (b)에서는 로그-로그 축 위의 $C/\tau$와 $\tau/2M$, 최솟값을 표시한 그 합, 그리고 $\tau^\star$에서 정확한 곡선의 값을 그린다. $\tau^\star$가 FT-1의 것에서 왜 움직이지 않았고 무엇이 움직였는지 말하라.
2. **유도.** (a) $w(\tau)=C/\tau+\tau/2M$에서 $\tau^\star$와 $w(\tau^\star)$를 유도하고, $\tau^\star$에서 두 항이 같음을 보여라. (b) 기하분포를 따르는 중단 횟수와, 중단이 구간에 들어와서 오는 평균 시각으로부터 $E[T_{\text{seg}}]=(e^{s/M}-1)(M+R)$을 유도하고, $s\ll M$에서 펼쳐 1차 낭비에 $R/M$이 더해짐을 되찾아라. (c) `gpu`에서 작은 파일을 제자리에서 읽는 FT-1: 학습 시간, 창의 수와 길이, GPU-시간. (d) FT-1의 코퍼스가 work 파일 쿼터의 1%만 쓰려면 샤드 하나에 샘플이 몇 개 들어가야 하고, 샤드 하나는 얼마나 크며, 스테이징은 얼마나 걸리는가?
3. **실행.** 영어 절 템플릿의 `?` 빈칸을 채운 뒤 FT-2를 $M=2.5$ h와 $M=10$ h에서 돌린다. $\tau^\star$, 1차 낭비, $\tau^\star$에서와 에폭마다 저장할 때의 예상 시간, 그리고 제자리에서 읽는 작은 파일과 스테이징한 샤드의 입력 속도와 바쁜 비율을 보고하라. 각각을 FT-1과 비교하라.
4. **해석.** 연구실 동료가 금요일 저녁에 영어 절의 스크립트를 제출하고 `sbatch --dependency=afterok:<번호> bc-part2.sbatch`로 두 번째 작업을 잇는다. 제출 전에는 "잘 시작하는지 보려고" 로그인 노드에서 `python train.py --data . --epochs 1`을 한 시간 돌렸고, 지난주에는 환경을 활성화해 둔 터미널에서 제출했을 때 작업이 잘 돌았다. 스크립트는 파티션 `gpu`, GPU 넷, `--time=72:00:00`, `--output=$HOME/logs/bc-%j.out`을 요청하고, 5월에 복사해 둔 JPEG 파일 3,600,000개가 있는 scratch 디렉터리로 가서 `--ckpt-dir /tmp/bc --save-every-epochs 50`으로 학습한다. 월요일, 아무것도 학습되지 않았다. 문제마다 이름과 증상과 고치는 법을 대라.

> [!note]- 그리는 법 · How to draw it
> - 두 축을 모두 로그로 하고 가로에 $\tau$, 세로에 $W$ 대비 비율을 둔다. 거기서 $C/\tau$는 기울기 $-1$, $\tau/2M$은 기울기 $+1$의 직선이다. 눈대중이 아니라 두 간격에서의 값으로 선마다 그린다.
> - 두 선은 $\tau^\star$에서 만나고, 거기서 각각 $w(\tau^\star)/2$다. 합의 최솟값은 교차점 바로 위에 있다.
> - $C$를 4배, $M$을 4분의 1로 하면 두 선이 모두 4배 올라가 — 로그 축에서는 같은 크기의 수직 이동이다 — 교차점이 옆이 아니라 위로 움직인다. $C$만 바뀌면 옆으로 움직인다.
> - 정확한 곡선을 합 위에 그리고 $\tau^\star$에서의 값을 적는다. 그 틈은 대부분 어떤 $\tau$도 없애지 못하는 재시작, $R/M$이다.
> - 패널 (a)에서는 FT-2가 바꾸는 것 — 체크포인트의 크기와 저장 시간, 그리고 간격 — 만 바꾼다. 스테이징 막대는 코퍼스의 것이고, 코퍼스는 같다.

> [!tip]- 정답 · Solutions
> 1. $C=14.4/0.5=28.8$ s $=0.008$ h이고 $M=2.5$ h이니 $CM=0.02$ h²로 FT-1의 $0.002\times10$과 같다. 그래서 $\tau^\star=\sqrt{0.04}=0.2$ h $=12$분 그대로다. 낭비는 $\sqrt{2\times0.008/2.5}=0.08$로 FT-1의 네 배다. $C/M$이 열여섯 배가 되었고 낭비는 그 제곱근을 따르기 때문이다. 두 선이 모두 4배 올라가 각각 4%에서 만나고, 합의 최솟값은 8.0%, 정확한 곡선은 거기서 19.47%이며 그 가운데 약 10.2%포인트가 $R/M=0.2540/2.5$다. 패널 (a): 12분마다 28.8 s에 쓰는 14.4 GB 체크포인트. 스테이징 막대는 그대로다.
> 2. (a) $dw/d\tau=-C/\tau^2+1/(2M)=0$에서 $\tau^\star=\sqrt{2CM}$이고, 그러면 $C/\tau^\star=\sqrt{C/2M}=\tau^\star/2M$, 합은 $\sqrt{2C/M}$이다. (b) 구간은 확률 $p=e^{-s/M}$로 깨끗하게 돌므로 첫 깨끗한 실행 전의 중단은 평균 $(1-p)/p=e^{s/M}-1$인 기하분포다. $s$보다 먼저 오는 중단은 평균 $M-s/(e^{s/M}-1)$에 오고 재시작 $R$을 더 치르므로 $E[T_{\text{seg}}]=s+(e^{s/M}-1)(M-s/(e^{s/M}-1)+R)=(e^{s/M}-1)(M+R)$이다. $e^x-1\approx x+x^2/2$와 구간 $W/\tau$개로, $C\ll\tau\ll M$이고 $R\ll M$일 때 $E[T]\approx W(1+C/\tau+\tau/2M+R/M)$이다. (c) $u=0.651$이니 학습 76.8 h. 스테이징이 없으면 창은 3.6 s 불러오기, $o=0.001$ h만 치르고 $(48-0.001)\times0.2/0.202=47.52$ h를 담는다. $k=\lceil76.8/47.52\rceil=2$, 48.00 h와 $0.001+(76.8-47.52)\times1.01=29.57$ h — 경과 77.57 h, 202.4에 비해 310.3 GPU-시간이다. (d) 1,000,000의 1%는 파일 10,000개이므로 샤드마다 적어도 $1{,}200{,}000/10{,}000=120$ 샘플, $120\times150$ kB $=18$ MB다. 스테이징은 $10{,}000/2{,}000+180=185$ s로 샤드 200개와 5 s 차이다. 파일 하나가 약 500 kB를 넘으면 바이트가 시간을 정한다.
> 3. 빈칸은 `STEPS * T_STEP / H`, `BATCH / T_STEP`, `N_PARAM * B_PER_PARAM / FS_WRITE / H`, `(SHARDS / FS_FILES + N_SAMPLES * B_SAMPLE / FS_READ) / H`, `min(FS_FILES / FILES_PER_SAMPLE, FS_READ / B_SAMPLE)`, `min(1.0, rate / NEED)`, `math.expm1((tau + c) / M)`, `(w / tau) * (M + r) * fails`, `math.sqrt(2 * C * M)`, `math.sqrt(2 * C / M)`이다. 출력은 영어 절의 정답 3과 같고, 요약하면:
>
>    | 항목 | $M=2.5$ h | $M=10$ h |
>    |---|---:|---:|
>    | $\tau^\star$ (분) | 12.00 | 24.00 |
>    | 1차 낭비 | 8.00% | 4.00% |
>    | $\tau^\star$에서 예상 시간 (h) | 59.73 | 53.38 |
>    | 에폭(78.1분)마다 저장할 때 (h) | 72.85 | 55.12 |
>
>    $W=50.0$ h, 200 GPU-시간, 필요한 초당 256 샘플, $C=28.8$ s, 불러오기 14.4 s, 스테이징 3.0분이고, 작은 파일은 제자리에서 666.7 샘플/s, 스테이징한 샤드는 13,333.3 샘플/s로 둘 다 GPU를 100% 바쁘게 하며 학습은 50.0 h다. $M=10$ h에서 FT-2의 간격은 FT-1의 12분에 비해 24분이다. $C$가 네 배이고 $\tau^\star$는 그 제곱근으로 자라기 때문이다. 낭비는 2%에 비해 4%, 예상 시간은 52.29에 비해 53.38 h다. $M=2.5$ h에서는 간격이 다시 12분, 낭비 8%로 59.73 h다. FT-2의 에폭 78.1분은 $\tau^\star$를 한참 지나므로, 에폭마다 저장하면 $M=2.5$ h에서 13.1 h, $M=10$ h에서 1.7 h를 더 치른다. 그리고 FT-2의 느린 스텝은 초당 256 샘플만 필요해 작은 파일의 666.7보다 적다. GPU는 더는 굶지 않지만, 그 배치는 여전히 work 쿼터가 거절하고 선점될 때마다 여전히 33분 동안 스테이징한다. 처리량 문제는 사라졌고, 저장소 문제는 남았다.
> 4. 문제 일곱, 저마다 증상과 고치는 법. (1) 48 h 파티션에 `--time=72:00:00`: `PartitionTimeLimit`으로 영원히 대기한다. 48 h를 요청하고 창을 잇는다. (2) `--output` 줄: Slurm은 홈 디렉터리 변수를 펼치지 않으므로 로그가 `~/logs`에 가지 않는다. 경로를 풀어 쓰거나, `logs/`를 먼저 만들고 `logs/bc-%j.out`을 쓴다. (3) 스크립트에 환경 준비가 없다: 지난주에는 터미널에서 물려받은 환경으로 돌았고, 새로 로그인해 내면 `import`에서 실패한다. `module` 줄이나 컨테이너를 스크립트에 넣는다. (4) 5월부터 scratch에 둔 작은 파일 3,600,000개: 30일 동안 안 읽힌 파일은 지워지고, 남은 것도 제자리에서 읽으면 GPU를 약 65%만 바쁘게 한다. 샤드 200개를 work에 두고 스테이징한다. (5) `--ckpt-dir /tmp/bc`: 노드 자신의 디스크여서 두 번째 작업의 노드는 보지 못한다. work에 원자적으로 쓴다. (6) `--save-every-epochs 50`: 전속력으로 학습해도 16.3 h에 한 번 — 작은 파일을 제자리에서 읽으면 25 h에 한 번 — 저장하므로, 한도나 선점이 그만큼을 버릴 수 있다. 12분마다, 그리고 `--signal` 경고에 저장한다. (7) `afterok`: 첫 작업이 `TIMEOUT`으로 끝나니 두 번째는 `DependencyNeverSatisfied`로 영원히 기다린다. `afterany`나 `singleton`을 쓴다. 그리고 로그인 노드에서의 한 시간은 GPU 없이 모든 사용자와 기계를 나누어 썼다. 그 시험은 짧은 `salloc` 안에서 해야 한다.

### 출처

- SchedMD, *Slurm* 문서, 26.05 ([slurm.schedmd.com](https://slurm.schedmd.com/documentation.html)) — 명령 페이지들, `slurm.conf`, FAQ, 그리고 작업 사유, 작업 배열, GRES, 선점, 스케줄링, 다요인 우선순위 페이지: 위에 적은 Slurm의 모든 옵션, 상태, 기본값, 동작.
- Apptainer 사용자 안내서, 1.5 ([apptainer.org](https://apptainer.org/docs/user/latest/introduction.html)) — 보안 모형, SIF, 빌드, `--nv`, 묶는 경로.
- Lmod 사용자 안내서 ([lmod.readthedocs.io](https://lmod.readthedocs.io/en/latest/010_user.html)) — `module` 명령.
- Lustre 위키, "Introduction to Lustre" ([wiki.lustre.org](https://wiki.lustre.org/Introduction_to_Lustre)) — 메타데이터 서버가 이름·권한·배치를 쥐고, 클라이언트는 파일 데이터를 객체 저장 서버에서 곧바로 읽는다.
- NVIDIA, *nvidia-smi* 문서 ([docs.nvidia.com](https://docs.nvidia.com/deploy/nvidia-smi/index.html)) — 사용률의 정의와 표본 기간, `-q -d`, `dmon`.
- PyTorch 2.14 문서 ([docs.pytorch.org](https://docs.pytorch.org/tutorials/beginner/saving_loading_models.html)) — 일반 체크포인트에서의 재개, DDP 설계 노트, `torchrun`.
- 파이썬 3 문서 ([docs.python.org](https://docs.python.org/3/library/signal.html)) — `signal` 처리기, `os.replace`. NumPy 2 문서 ([numpy.org](https://numpy.org/doc/stable/reference/random/generator.html)) — `default_rng`, `PCG64.state`.
- 리눅스 man-pages ([man7.org](https://man7.org/linux/man-pages/man2/rename.2.html)) — `rename(2)`, `open(2)`, `errno(3)`, `time(1)`. GNU Bash 매뉴얼 "The Set Builtin", rsync 매뉴얼, GNU tar 매뉴얼 "Extended File Attributes".
- Aupy, Robert, Vivien & Zaidouni, "Checkpointing algorithms and fault prediction", [arXiv:1302.3752](https://arxiv.org/abs/1302.3752), 2013 — "Young과 Daly의 고전적인 1차 분석".
- Young, *Communications of the ACM* 17(9):530–531, 1974, 그리고 Daly, *Future Generation Computer Systems* 22(3):303–312, 2006 — 서지 정보만 확인했고, 이 페이지는 결과를 스스로 유도한다.
