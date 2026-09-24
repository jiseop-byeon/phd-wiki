---
title: "12.4 Config and Data Formats"
tags: [foundations, tools, formats, data]
study-depth: Working
wiki-support: Working
depth-goal: "Pick the format for a robot's configuration, log or dataset by what it promises, and prove the choice on one 60-second P6 run: bytes per sample and per hour in binary, CSV and JSON, the round-trip error at any number of printed decimals, the type each YAML reader gives a scalar, and the header, alignment and framing of a .npy file and an MCAP record."
mastery-when: "Raise when the thesis releases a dataset or a logging pipeline that other groups will load — a LeRobot- or robomimic-style dataset, or a recorder whose bags are the experiment's evidence."
---

> [!note] Prerequisites · 선수 지식
> **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] — the cart, its $2048$ counts/m encoder, its $200\,\mathrm{Hz}$ controller and $50\,\mathrm{Hz}$ vision goal · [[02-foundations/lab-kernel|0.7 Lab Kernel §3 and §5]] — the semi-implicit Euler step that generates the run, and the blank-and-solve pattern of the problem set · [[02-foundations/signal-processing|6. Signal Processing §2]] — a quantizer's step and its half-step error, which §2 applies to printed decimals · enough Python and NumPy to read a 100-line script. The ROS 2 pages linked below come later in the study order; each is read only where a section names it.
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** — 카트, $2048$ counts/m 엔코더, $200\,\mathrm{Hz}$ 제어기와 $50\,\mathrm{Hz}$ 비전 목표 · [[02-foundations/lab-kernel|0.7 Lab Kernel §3과 §5]] — 실행 데이터를 만드는 반암시적 오일러 스텝과, 과제의 빈칸 채우기 패턴 · [[02-foundations/signal-processing|6. 신호처리 §2]] — 양자화기의 계단과 반 계단 오차. §2가 이것을 출력 소수 자릿수에 적용한다 · 100줄짜리 스크립트를 읽을 만큼의 Python과 NumPy. 아래에 링크한 ROS 2 페이지들은 학습 순서상 뒤에 오며, 절이 이름을 댈 때 그 부분만 읽으면 된다.

## English

*Stands on [[02-foundations/signal-processing|6. Signal Processing §2]], whose quantizer is exactly what a printed decimal is. A later use of plant **P6** (*plant*: control's word for the system being controlled): the ROS 2 track runs it as nodes and topics ([[04-robotics/ros2/nodes-topics-messages|25.2]]), starts it from a launch file with a parameter file ([[04-robotics/ros2/workspaces-packages-launch|25.4]]) and records it in a bag ([[04-robotics/ros2/debugging-data-reproducibility|25.10]]). This page opens the files those pages write and read.*

> [!note] Why this matters · 왜 배우는가
> Formats are the floor beneath the physical-AI stack of [[07-research-program/index|7 §5]]: every layer hands its data to the next as bytes — a parameter file into the controller, a bag out of the robot, a dataset into the learning layer — and in "install that panel on the frame" they carry the demonstrations of the fitting step and the logs that verify completion (its place is marked on the [[physical-ai-map|Physical AI Map]]). Get a format wrong and a run is lost without an error: a time column printed with `%.3f` deletes the jitter a latency study measures, a float32 stamp turns a minute of P6's samples into one instant, and a hand-edited `device_id: 0123` starts a node with 83. The need arrives in block 2 of the dissertation path ([[07-research-program/index|7 §8]]), when the ROS 2 track loads parameter files and records bags ([[04-robotics/ros2/services-actions-parameters|25.3 §7]], [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), and again in block 7, when [[05-construction-robotics/imitating-contact|10. Imitating Contact §2]] trains on the seating demonstrations of S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]). After this page you can pick the format for a config, a log or a dataset by what it promises, and prove the choice in bytes and in round-trip error.

> [!note] First pass · 처음이라면
> Two sessions of about 90 minutes. **Session 1 — numbers as bytes.** Look at the picture, then work the Worked case by hand: one sample of P6's run in binary, CSV and JSON, per sample and per hour, and its time read back from three and from seven printed decimals. Read §1 and §2, then answer Self-check 1 and 2. **Session 2 — the formats you edit and record.** Read §3 and §4 before you edit a config, §6–§8 before you choose a log or dataset format, run §10's lab, and answer Self-check 3–6. §5 and §9 can wait for the day you edit a URDF or a Markdown table, and every *Deeper* callout can be skipped on a first pass.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], run once for one minute. The catalog fixes the cart, its encoder ($2048$ counts/m) and its two rates. A log needs more than that — a clock, a goal, a controller, a command — so this page freezes one run completely. Every number below is this page's own course number, chosen so that §10's code regenerates the run bit for bit; none of them is a measurement.

| Symbol | Value | What it is |
|---|---:|---|
| $D$, $f$, $T$ | $60\,\mathrm{s}$, $200\,\mathrm{Hz}$, $5\,\mathrm{ms}$ | run length; P6's control rate and period |
| $n$ | $fD=12{,}000$ | samples, one per control tick $k=0,\dots,11{,}999$ |
| $t_0$ | $1{,}790{,}000{,}000\,\mathrm{s}$ | run start, in seconds since 1970-01-01 UTC: 21 September 2026, 14:13:20 UTC |
| $\ell_k$ | $(123{,}607\,k)\bmod 200{,}001\ \mathrm{ns}$ | how late tick $k$ is stamped, $0$ to $200\,\mu\mathrm{s}$: a deterministic stand-in for scheduling jitter |
| $t_k$ | $t_0+(5{,}000{,}000\,k+\ell_k)\times10^{-9}\,\mathrm{s}$ | the time column: float64, 8 bytes |
| $c_k$ | int32, 4 bytes | the encoder count, $2048$ per metre (P6) |
| $u_k$ | float64, 8 bytes | the motor command in newtons, a PD law on the counts |
| $m$ | $2\,\mathrm{kg}$ | cart mass, used only to generate the run; P6 leaves it open |
| $k_p$, $k_d$ | $200\,\mathrm{N/m}$, $40\,\mathrm{N\,s/m}$ | the controller's gains; with $m$ the loop is critically damped, $k_d/(2\sqrt{k_pm})=1$ |
| $g$ | $0.1\to0.6\to0.1\,\mathrm{m}$ every $20\,\mathrm{s}$ | the vision goal, a triangle wave, renewed every 4th tick ($50\,\mathrm{Hz}$) |

At every tick the controller computes

$$u_k=k_p\Big(g-\frac{c_k}{2048}\Big)-k_d\,\frac{(c_k-c_{k-1})\,f}{2048}$$

so its velocity estimate is one count difference per period, $0.0977\,\mathrm{m/s}$ a count at $200\,\mathrm{Hz}$ (the worked case of [[04-robotics/ros2/nodes-topics-messages|25.2]]), which is why the logged command chatters by $k_d\times0.0977=3.9\,\mathrm{N}$ from tick to tick. The cart starts at rest at $0.1\,\mathrm{m}$ and is stepped with the semi-implicit Euler of [[02-foundations/lab-kernel|0.7 §3]]. One record of the log is the triple $(t_k,c_k,u_k)$.

The run's configuration is the parameter file its controller would be started with, in the structure [[04-robotics/ros2/services-actions-parameters|25.3 §7]] defines:

```yaml
# P6 run 042: the controller's parameters (this page's course numbers)
/cart/controller:
  ros__parameters:
    counts_per_metre: 2048   # encoder scale (P6)
    control_period: 0.005    # s, 200 Hz
    kp: 200.0                # N/m
    kd: 40.0                 # N s/m
    goal_topic: goal         # relative name: resolves to /cart/goal
    cmd_topic: cmd           # relative name: resolves to /cart/cmd
```

§3 adds the run's JSON sidecar, and §10 generates all $12{,}000$ records.

*Scope: the formats a robot-learning researcher reads and writes every week — JSON, YAML, XML, CSV and Markdown as text; NumPy's `.npy`, HDF5, Parquet and MCAP as binary — at the level of what each promises, what it costs in bytes, what it loses in a round trip and which of its traps costs days. The ROS 2 machinery around these files, codecs, databases and compression are left to the pages §11 names. HDF5 and Parquet are described from their documentation only; the lab uses NumPy and the Python standard library.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 330" style="max-width:100%;height:auto" role="img" aria-label="Six horizontal bars drawn to one scale, 7 pixels per byte, each holding sample 2407 of the P6 run: the packed binary record of 20 bytes split into t, counts and u, with its hex bytes; the aligned record of 24 bytes with 4 padding bytes; the CSV line at full precision, 44 bytes; the CSV line at three decimals, 27 bytes; one JSON object, 69 bytes; and the np.savetxt default line, 76 bytes. Each label gives the whole run's rate, from 14.40 to 54.36 megabytes per hour.">
  <text x="12" y="18" font-size="12" fill="currentColor" fill-opacity="0.85">Tick 2407 of the P6 run, byte by byte (7 px = 1 byte)</text>
  <text x="12" y="40" font-size="11" fill="currentColor" fill-opacity="0.85">binary, struct '&lt;did': 20 B · whole run 14.40 MB/h</text>
  <rect x="12" y="46" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="40.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">t · f8</text>
  <rect x="68" y="46" width="28" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="82.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">i4</text>
  <rect x="96" y="46" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="124.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">u · f8</text>
  <text x="162" y="59" font-size="10" fill="currentColor" fill-opacity="0.8" font-family="ui-monospace,monospace">6a3f02e34eacda41 12040000 343333333353ffbf</text>
  <text x="12" y="86" font-size="11" fill="currentColor" fill-opacity="0.85">binary, aligned (align=True): 24 B · whole run 17.28 MB/h</text>
  <rect x="12" y="92" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="40.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">t · f8</text>
  <rect x="68" y="92" width="28" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="82.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">i4</text>
  <rect x="96" y="92" width="28" height="18" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2"/>
  <text x="110.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">pad</text>
  <rect x="124" y="92" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="152.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">u · f8</text>
  <text x="190" y="105" font-size="10" fill="currentColor" fill-opacity="0.8">4 padding bytes put u on an 8-byte boundary</text>
  <text x="12" y="132" font-size="11" fill="currentColor" fill-opacity="0.85">CSV, repr: 44 B · whole run 42.03 B/sample, 30.26 MB/h</text>
  <rect x="12" y="138" width="308" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="153" x2="82" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="153" x2="152" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="153" x2="222" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="153" x2="292" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="151" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="306" lengthAdjust="spacing">1790000012.0351205,1042,-1.9578125000000002↵</text>
  <text x="12" y="178" font-size="11" fill="currentColor" fill-opacity="0.85">CSV, %.3f: 27 B · 18.52 MB/h · t reads back 120.4 µs early</text>
  <rect x="12" y="184" width="189" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="199" x2="82" y2="202" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="199" x2="152" y2="202" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="197" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="187" lengthAdjust="spacing">1790000012.035,1042,-1.958↵</text>
  <text x="12" y="224" font-size="11" fill="currentColor" fill-opacity="0.85">JSON, one object per sample: 69 B · whole run 48.26 MB/h</text>
  <rect x="12" y="230" width="483" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="245" x2="82" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="245" x2="152" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="245" x2="222" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="245" x2="292" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="362" y1="245" x2="362" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="432" y1="245" x2="432" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="243" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="481" lengthAdjust="spacing">{"t": 1790000012.0351205, "counts": 1042, "u": -1.9578125000000002}, </text>
  <text x="12" y="270" font-size="11" fill="currentColor" fill-opacity="0.85">np.savetxt, default '%.18e': 76 B · 54.36 MB/h</text>
  <rect x="12" y="276" width="532" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="291" x2="82" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="291" x2="152" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="291" x2="222" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="291" x2="292" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="362" y1="291" x2="362" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="432" y1="291" x2="432" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="502" y1="291" x2="502" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="289" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="530" lengthAdjust="spacing">1.790000012035120487e+09,1.042000000000000000e+03,-1.957812500000000178e+00↵</text>
  <line x1="12" y1="312" x2="544" y2="312" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="12" y1="312" x2="12" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="12" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">0</text>
  <line x1="82" y1="312" x2="82" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="82" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10</text>
  <line x1="152" y1="312" x2="152" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="152" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">20</text>
  <line x1="222" y1="312" x2="222" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="222" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">30</text>
  <line x1="292" y1="312" x2="292" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="292" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">40</text>
  <line x1="362" y1="312" x2="362" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="362" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">50</text>
  <line x1="432" y1="312" x2="432" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="432" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">60</text>
  <line x1="502" y1="312" x2="502" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="502" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">70</text>
  <text x="514" y="308" font-size="10" fill="currentColor" fill-opacity="0.8">bytes</text>
</svg>

Tick 2407 of the run — stamped $1{,}790{,}000{,}012.0351205\,\mathrm{s}$, $1042$ counts, $-1.9578125000000002\,\mathrm{N}$ — as the bytes each file spends on it, to one scale of $7$ px a byte: $20$ packed, $24$ aligned, $44$ as full-precision CSV, $27$ at three decimals, $69$ as a JSON object and $76$ from `np.savetxt`'s default. The labels give the whole run's rate from §10, from $14.40\,\mathrm{MB/h}$ for the packed record to $54.36\,\mathrm{MB/h}$ for `np.savetxt`, and only the three-decimal line does not read back exactly: its time returns $120.4\,\mu\mathrm{s}$ early.

### Worked case · 대상으로 한 번 끝까지

The object is one record and the hour it belongs to. The problem set changes the record — an integer clock and a fourth column — so do this version by hand first. Four one-line glosses, each derived later: `repr`, Python's default text for a float, is the shortest decimal that reads back to the same float (§2); a text format spends one byte per character of the printed value, delimiters and line end included (§1); printing a number to $d$ decimals rounds it to a multiple of $10^{-d}$, so it reads back off by at most half that step, plus half the spacing of the float grid it is parsed onto (§2); and float64 numbers near $t_0$ are $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$ apart, float32 numbers there $128\,\mathrm{s}$ apart (§2).

**Step 1 — the record in memory.** Tick $k=2407$ comes $12.035\,\mathrm{s}$ into the run and was stamped $\ell_{2407}=120{,}562\,\mathrm{ns}$ late:

| field | as Python prints it (`repr`) | type | bytes |
|---|---|---|---:|
| $t$ | `1790000012.0351205` | float64 | 8 |
| $c$ | `1042` | int32 | 4 |
| $u$ | `-1.9578125000000002` | float64 | 8 |

The count is $1042/2048=0.5087890625\,\mathrm{m}$. The command's real-number value is $200\,(0.499-0.5087890625)=-1.9578125\,\mathrm{N}$, since the goal was $0.499\,\mathrm{m}$ and the count had not changed since the tick before; but $0.499$ has no exact binary form, so the float carries a tail in its last bit, and naming that float takes `repr` 17 significant digits.

**Step 2 — binary.** A binary record is its fields' widths, and an hour at $200\,\mathrm{Hz}$ is $720{,}000$ records:

$$B_{\text{bin}}=8+4+8=20\ \text{bytes},\qquad 20\times720\,000=14{,}400\,000\ \text{bytes}=14.4\ \text{MB/h}$$

because a binary field holds its value's own bytes whatever the value: $1042$ and $-1.9578125000000002$ cost what $0$ costs.

**Step 3 — CSV at full precision.** The line is `1790000012.0351205,1042,-1.9578125000000002` and a newline:

$$B_{\text{csv}}=18+1+4+1+19+1=44\ \text{bytes}=2.2\,B_{\text{bin}}$$

since each character is a byte. Over the whole run a line averages $42.03$ bytes, $30.26\,\mathrm{MB/h}$ (§10), and nothing is lost, because every value was printed with `repr`.

**Step 4 — JSON, one object per sample.** `{"t": 1790000012.0351205, "counts": 1042, "u": -1.9578125000000002}` is $67$ characters, and a list separates its objects with a comma and a space, so a record costs $69$ bytes, $3.45\times$ the binary. $26$ of the $67$ characters are names, quotes, colons, commas and spaces, written again for each of the $720{,}000$ records of an hour; the run averages $67.03$ bytes a record, $48.26\,\mathrm{MB/h}$ (§10).

**Step 5 — three decimals.** `%.3f` on both floats gives `1790000012.035,1042,-1.958`, $27$ bytes, only $1.35\times$ the binary — and a time that reads back as the float nearest to $1{,}790{,}000{,}012.035$, which is $120.4\,\mu\mathrm{s}$ below $t$. The bound holds with room to spare,

$$|\hat t-t|=120.4\ \mu\text{s}\ \le\ \tfrac12\,10^{-3}\ \text{s}+\tfrac12\,2^{-22}\ \text{s}=500.12\ \mu\text{s}$$

so the error is legal, and it is also exactly the wrong thing to lose. Every nominal tick time is a whole number of milliseconds, three decimals keep exactly that, and the $120.562\,\mu\mathrm{s}$ by which this tick ran late — what a latency study measures ([[04-robotics/robot-systems-deployment|10. Robot Systems §3]]) — is gone. Over the run the worst loss is $200\,\mu\mathrm{s}$, the largest lateness (§10). The command comes back as $-1.958$, off by $0.19\,\mathrm{mN}$.

**Step 6 — how many decimals are enough.** The read-back is exact once the printed step is finer than the float spacing,

$$10^{-7}\ \text{s}=0.1\ \mu\text{s}\ <\ 2^{-22}\ \text{s}=0.238\ \mu\text{s}\quad\Rightarrow\quad d=7$$

because then the printed decimal lies within half a float spacing of $t$, and the parser, which rounds to the nearest float, lands on $t$ itself. Ten digits before the point and seven after are $17$ significant digits, the length of `repr(t)` here. At six decimals the time is still off by up to $0.48\,\mu\mathrm{s}$ (§10).

**Step 7 — the column's type.** Stored as float32 instead, a time keeps $24$ significant bits, and near $t_0$ float32 numbers are $2^{30-23}=128\,\mathrm{s}$ apart. $t_0=128\times13{,}984{,}375$ is one of them, and every stamp of the run lies less than $60\,\mathrm{s}$ after it, so rounding each stamp to the nearest float32 — written $\operatorname{fl}_{32}$ — gives $t_0$ itself:

$$\operatorname{fl}_{32}(t_k)=t_0\quad\text{for every }k,\qquad\text{since}\quad t_k-t_0<60\ \text{s}<\tfrac12\times128\ \text{s}$$

so the $12{,}000$ stamps collapse to one value (§10 counts $1$ distinct stamp), and tick 2407 reads back $12.035\,\mathrm{s}$ early. Seconds since the run start fit float32 to within $2.02\,\mu\mathrm{s}$, and integer nanoseconds fit int64 exactly — the problem set's variant.

| file | bytes for tick 2407 | × binary | run average, bytes a sample | MB an hour | reads back exactly |
|---|---:|---:|---:|---:|---|
| binary record | 20 | 1.00 | 20.00 | 14.40 | yes |
| CSV, `repr` | 44 | 2.20 | 42.03 | 30.26 | yes |
| JSON, object per sample | 69 | 3.45 | 67.03 | 48.26 | yes |
| CSV, `%.3f` | 27 | 1.35 | 25.73 | 18.52 | no: $t$ by $-120.4\,\mu\mathrm{s}$, $u$ by $-0.19\,\mathrm{mN}$ |

### 1. What a format promises: text or binary

*In one sentence:* a file must let a reader who has only its bytes recover what the writer meant; a format is the contract about bytes that makes this possible, and five promises — types, schema, precision, comments and streaming — decide which job it can do.

A file outlives the program that wrote it. Its reader may be a colleague's analysis script next month, a C++ node at start-up, a training loader in another language, or you in two years, and all the reader has is the bytes. A format is what lets it get back what the writer meant, and it promises — or fails to promise — five things.

1. **Types.** Does `1042` come back as an integer, `0.005` as a float, `true` as a boolean — or as characters the reader must guess about? A binary format carries the type beside the data (a `.npy` header says `<f8`, a little-endian 8-byte float); CSV carries none; JSON has six; YAML infers them from spelling, and two readers can infer differently (§4).
2. **Schema.** Where are the field names, units and meanings written? In the file (a `.npy` header, a Parquet footer, MCAP's schema records), beside it (a JSON sidecar, rosbag2's `metadata.yaml`), or only in someone's memory? A column called `u` does not say newtons.
3. **Precision.** Does a number come back bit for bit? Binary always does; text does only if enough digits were printed (§2).
4. **Comments.** Can a person annotate the file, and does the note survive a program that loads and rewrites it? YAML and XML have comments, JSON and CSV have none, and parsers drop the ones that exist: the YAML specification calls comments a presentation detail with no effect on the data, and Python's `xml.etree` skips them while parsing (§5).
5. **Streaming.** Can a recorder append one sample at a time, and does a crash leave a readable prefix? A CSV file, or a file of one JSON text per line, grows line by line; a JSON array needs its closing bracket and a `.npy` header states the array's shape; a Parquet file writes its metadata after the data, at the very end; an MCAP file frames every record with its own length (§8).

The first fork is text or binary. A **text** format prints each value as characters and the reader parses them back; with ASCII characters in UTF-8, the encoding JSON requires between systems, every character is one byte, so a value costs as many bytes as its printed form has characters. A **binary** format stores each value's own bytes: a float64 costs 8 bytes and an int32 costs 4 whatever the value, but the reader must know the layout — the order, width and byte order of the fields — before the bytes mean anything (§7). Text buys readability in any editor and a line-by-line diff in Git; binary buys size, speed and exactness.

| format | text or binary | types | schema lives | floats exact | comments | append a sample | where a robot researcher meets it |
|---|---|---|---|---|---|---|---|
| JSON | text | six (§3) | nowhere; a sidecar | with `repr` | no | as one JSON text per line | robomimic configs, LeRobot's `meta/info.json` |
| YAML | text | by spelling (§4) | nowhere | with enough digits | yes | — | ROS 2 parameter files, Hydra configs |
| XML | text | none: all strings (§5) | an optional schema | — | yes | — | URDF, `package.xml`, launch files |
| CSV | text | none (§6) | a header row, at best | with enough digits | no | yes | quick logs, spreadsheets |
| Markdown | text | — | front matter (§9) | — | yes | — | notes, this wiki |
| `.npy`, `.npz` | binary | a dtype (§7) | the header | yes | no | no | arrays, results |
| HDF5 | binary | per dataset (§8) | groups, attributes | yes | — | if chunked | robomimic datasets |
| Parquet | binary | per column (§8) | the footer | yes | — | no | LeRobot datasets |
| MCAP | binary | per schema (§8) | schema records | yes | — | yes | rosbag2 bags |

> **Serialization format, defined.** A **serialization format** is a *contract between a writer and a reader about bytes*: a specification of how values in memory become a byte string and come back — not a file extension and not a library. Four conditions. An **encoder** turns each allowed value into bytes; a **decoder** turns those bytes back into values; a **specification** both sides follow — a grammar for text, a layout of widths and byte order for binary; and a **domain**, the set of values it accepts: JSON has no NaN, and a YAML plain scalar's type comes from its spelling.
>
> $$B_{\text{bin}}=\sum_{i=1}^{m}w_i,\qquad B_{\text{text}}=\sum_{i=1}^{m}\ell_i+(m-1)+\lambda$$
>
> where $m$ is the number of fields in one record, $w_i$ the width in bytes of field $i$'s binary type, $\ell_i$ the number of characters of its printed form, $m-1$ the delimiters and $\lambda$ the line terminator's bytes — so a binary record has a fixed size, and a text record's size moves with every value's digits.
>
> - **Example**: tick 2407 of the run: $B_{\text{bin}}=8+4+8=20$ bytes, and as a CSV line $B_{\text{text}}=18+4+19+2+1=44$.
> - **Non-example**: "a CSV file". Until the delimiter, the quoting, the digits printed and the meaning of each column are fixed, "CSV" names a family of formats (§6), and two programs can both read CSV and disagree about the same file.
> - **Why it matters**: every later section is one of the four conditions failing — a decoder guessing types (§4), a domain that quietly lacks NaN (§3), a specification nobody wrote down (§6), a layout read with the wrong byte order (§7).

The rest of the page takes the formats one at a time, but the choice between them comes from the job. A **configuration** is small, written by people and read at start-up, so it is text with comments: YAML in ROS 2, YAML or JSON in learning code. A **log** is large and written sample by sample, so it is binary and appendable: MCAP through rosbag2, with a small JSON or YAML sidecar for what the bytes cannot say. A **dataset** is read many times by a loader, so it is whatever that loader reads fastest and whatever the community's tools expect: HDF5 for robomimic, Parquet and MP4 for LeRobot. A **result** worth one table is `.npy` or CSV printed with `repr`.

### 2. Numbers as text: decimals, digits and the round trip

*In one sentence:* a log written as text can silently lose what its floats held, because a printed float reads back exactly only when enough digits were printed — and how many is enough depends on the number's size, not on how many of its digits look meaningful.

A float64 holds a binary fraction with 53 significant bits. Most decimal fractions — $0.005$, $0.499$ — have no exact binary form, so the float holds the nearest one, and printing it is a second, separate choice: how many digits to write. There are two ways to choose. **Fixed decimals** — `%.3f`, `round(x, 3)`, `np.savetxt(fmt="%.3f")` — keep the absolute error constant. **Significant digits** — `%.17g`, `repr` — keep the relative error constant. Python's `repr` writes the shortest string that reads back to the same float (since Python 3.1), and since Python 3.2 `str` of a float is that same string. So the two standard writers are exact by default: `json.dumps` calls `float.__repr__`, and the `csv` module writes every non-string with `str`. Precision is lost only when someone chooses fewer digits — which is exactly what `"%.3f"` in a logging line does.

A fixed number of decimals is a quantizer in the sense of [[02-foundations/signal-processing|6. Signal Processing §2]], with step $q=10^{-d}$: the printed value is off by at most $q/2$, and when the values fall at random against the step the error spreads uniformly, with RMS $q/\sqrt{12}$. Parsing adds a second rounding, onto the float grid. For $2^e\le|x|<2^{e+1}$ the float64 neighbours of $x$ are $2^{e-52}$ apart ([[03-deep-learning/foundations/training-at-scale|1.3 §4]] tabulates the spacing of the common formats near $1$). At $t_0\approx1.79\times10^9\,\mathrm{s}$, $e=30$ and the spacing is $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$; at tick 2407's command, $1\le|u|<2$ gives $2^{-52}=2.2\times10^{-16}\,\mathrm{N}$.

That is why one rule of thumb cannot serve both columns. The time is always near $t_0$, so one fixed $d$ fits every sample: $d=7$ is exact for all of them (Worked case, step 6). The command runs from about $-4.3$ to $+4.0\,\mathrm{N}$ and passes near zero, where the float spacing shrinks with the value, so no fixed $d$ is exact for every value; it needs significant digits, which shrink with the value too. Seventeen significant digits always identify a float64 (the callout below proves it), sixteen do not always, and tick 2407's command is a float that needs its seventeenth:

```python
import numpy as np

t, u = 1790000012.0351205, -1.9578125000000002    # sample 2407 of the run (the lab in section 10 prints it)
for text in (repr(t), "%.3f" % t, "%.6f" % t, "%.7f" % t):
    print("t as %-19s reads back %+.4e s off" % (text, float(text) - t))
for text in (repr(u), "%.3f" % u, "%.8f" % u, "%.16g" % u, "%.17g" % u):
    print("u as %-19s reads back %+.4e N off" % (text, float(text) - u))
print("float64 spacing at t: %.4g s, at u: %.4g N; float32 spacing at t: %g s"
      % (np.spacing(t), np.spacing(abs(u)), np.spacing(np.float32(t))))
```

```text
t as 1790000012.0351205  reads back +0.0000e+00 s off
t as 1790000012.035      reads back -1.2040e-04 s off
t as 1790000012.035120   reads back -4.7684e-07 s off
t as 1790000012.0351205  reads back +0.0000e+00 s off
u as -1.9578125000000002 reads back +0.0000e+00 N off
u as -1.958              reads back -1.8750e-04 N off
u as -1.95781250         reads back +2.2204e-16 N off
u as -1.9578125          reads back +2.2204e-16 N off
u as -1.9578125000000002 reads back +0.0000e+00 N off
float64 spacing at t: 2.384e-07 s, at u: 2.22e-16 N; float32 spacing at t: 128 s
```

The time is exact with `repr` and `%.7f`, and off by $120.4\,\mu\mathrm{s}$ with `%.3f` and $0.48\,\mu\mathrm{s}$ with `%.6f`. The command is still off by its last bit, $2.2\times10^{-16}\,\mathrm{N}$, with `%.8f` and with `%.16g`, and exact only with `%.17g` and `repr`.

> [!note]- Deeper · 더 깊이
> **Why seventeen digits always suffice.** For $10^j\le |x|<10^{j+1}$ the seventeenth significant digit has weight $10^{j-16}\le |x|\cdot10^{-16}$, so the printed decimal is within
>
> $$\tfrac12\,10^{j-16}\ \le\ 5\times10^{-17}\,|x|\ <\ 2^{-54}\,|x|\ \le\ \tfrac12\,s(x)$$
>
> of $x$, since $2^{-54}=5.55\times10^{-17}$ and the gap $s(x)$ from $x$ to its nearer float64 neighbour is at least $2^{-53}|x|$ — and half a spacing is all the parser needs to return $x$. Sixteen digits allow an error up to $5\times10^{-16}|x|$, which for some $x$ is more than half a spacing.

> **Round trip, defined.** A **round trip** is the *composition of a format's decoder with its encoder*, $x\mapsto\hat x=\mathrm{d}(\mathrm{e}(x))$, applied to a value in memory — a property of an encoder–decoder pair on a set of values, not of a number alone and not of a format's name. An **exact** round trip needs four conditions: the value is **in the format's domain** (NaN is not in JSON's); the bytes are **read by the matching decoder** (a float parsed as a float, a count as an integer); the decoded value has **the same type** (a count that comes back as `1042.0` has changed type, §6); and **$\hat x=x$ bit for bit**, the equality that a regression test or a hash of a results table checks. For text printed with $d$ decimals and parsed to the nearest float,
>
> $$|\hat x-x|\le\tfrac12\,10^{-d}+\tfrac12\,s(x),\qquad \hat x=x\ \text{ whenever }\ 10^{-d}<s(x)$$
>
> where $s(x)$ is the gap between $x$ and its nearer float64 neighbour, $2^{-22}\,\mathrm{s}$ at $t_0$ — because the printed decimal lies within half a printed step of $x$, and the parser moves it by at most half a float spacing.
>
> - **Example**: tick 2407's time. At $d=3$ it reads back $120.4\,\mu\mathrm{s}$ early, inside the bound of $500.12\,\mu\mathrm{s}$; at $d=7$ it reads back exactly, since $10^{-7}<2^{-22}$.
> - **Non-example**: the command at eight or nine decimals. Over the run its worst error is $1.55\times10^{-14}\,\mathrm{N}$ — no force sensor could see it — and still the read-back is not exact (§10). "Physically lossless" and "bit-exact" are two different promises, and a regression test that compares two logs with `==` needs the second.
> - **Why it matters**: a result that is reproduced "to the digits printed" can differ from the original in every float, so a check of reproducibility must say which of the two promises it tests; and a time column printed with fixed decimals erases exactly the scale below the step — here, the jitter.

The practical rules follow in one line each. Log floats with `repr` (the default of `json` and `csv`) or in binary. If you must print fixed decimals, choose $d$ from the spacing: $d=7$ for seconds since 1970, and for a signal, significant digits instead. Never round before saving to "save space": `%.3f` saves about $16$ bytes a sample over `repr` here (§10), and binary saves $22$ without losing anything.

### 3. JSON: six types, no comments, numbers as text

*In one sentence:* JSON solves "one small file that every language can read" with a text grammar of six value types, and for a robot its traps are in the numbers — no NaN, and integers exact only up to $2^{53}$ in many readers — and in having no comments.

JSON is defined by RFC 8259 (December 2017), and its whole grammar fits on a page: a JSON text is one value — a string, a number, `true` or `false`, `null`, an object of name–value pairs or an array — whitespace between tokens means nothing, there is no comment syntax at all, and text exchanged between systems must be UTF-8. The definition box below states the rules; three details decide what a robot can put in it:

- **A number is decimal text**: an optional minus, digits, an optional fraction and exponent, no leading zeros — and no NaN or Infinity. The RFC lets each implementation limit range and precision and names the IEEE 754 double as the baseline, which is where the limit of $2^{53}$ below comes from.
- **Object names should be unique.** When they are not, the RFC calls the receiver's behaviour unpredictable; Python's `json` keeps the last value and raises nothing.
- **Nothing says what a number means.** `"u": -1.958` carries no unit, and a JSON file has no place for the comment that would.

Python's `json` module adds one trap of its own. By default it writes a float NaN as `NaN` and infinity as `Infinity`, the JavaScript spellings, which RFC 8259 does not permit; a strict parser in another language refuses the file. On a robot that is the dropped vision goal a logger stored as NaN. With `allow_nan=False` the writer raises `ValueError` instead, which is the behaviour you want from a logger.

```python
import json

meta = {"run": "042", "rate_hz": 200, "start_unix_s": 1790000000, "vision_ok": True, "operator": None,
        "columns": ["t", "counts", "u"], "units": {"t": "s since 1970-01-01 UTC", "counts": "1/2048 m", "u": "N"}}
text = json.dumps(meta)
print(len(text), "bytes; reads back equal:", json.loads(text) == meta)
print(json.dumps({"goal": float("nan")}))                  # a dropped goal: Python writes NaN, which RFC 8259 forbids
try:
    json.dumps({"goal": float("nan")}, allow_nan=False)
except ValueError as err:
    print("allow_nan=False raises", type(err).__name__)
print(json.loads('{"kp": 200.0, "kp": 20.0}'))             # a repeated name: Python keeps the last one
stamp_ns = 1790000012035120562                             # tick 2407's clock reading, integer ns since 1970
print(stamp_ns > 2 ** 53 - 1, int(float(stamp_ns)) - stamp_ns)   # past the exact range of a binary64 reader
```

```text
202 bytes; reads back equal: True
{"goal": NaN}
allow_nan=False raises ValueError
{'kp': 20.0}
True 78
```

The `meta` dictionary is run 042's **sidecar**, the small file that travels beside a log and says what the log's bytes cannot: which columns, which units, which clock. It uses all six types — strings, numbers, a boolean, `null`, arrays and objects — and reads back equal. The last line is the subtle one. Tick 2407's clock reading in integer nanoseconds since 1970 is $1.79\times10^{18}$, far past $2^{53}-1\approx9.0\times10^{15}$; Python keeps it exact, because Python integers have no size limit, but a reader that parses JSON numbers as doubles — common, as Python's `json` documentation warns — gets the nearest double, $78\,\mathrm{ns}$ off here and up to $128\,\mathrm{ns}$ over the run (§10). The file is valid JSON and still not portable. Write such stamps as two integers, seconds and nanoseconds — the shape of the ROS 2 time stamp ([[04-robotics/ros2/nodes-topics-messages|25.2 §4]]) — or as nanoseconds since the run start, which stay below $6.0\times10^{10}$.

> **JSON text, defined.** A **JSON text** is a *text serialization of one value from a tree of six value types*, as RFC 8259 specifies — a format, not a Python dictionary and not a JavaScript object. Five conditions. Every value is **one of six types**: object, array, string, number, `true`/`false`, `null`; **numbers are decimal text**, with no NaN, no Infinity and no leading zeros; there are **no comments**; the **names within an object should be unique**; and text exchanged between open systems is **UTF-8**. The integers every reader keeps exactly are
>
> $$|n|\le 2^{53}-1=9\,007\,199\,254\,740\,991$$
>
> because a binary64 double has a 53-bit significand, so every integer up to $2^{53}$ has its own double and past it the doubles are $2$, then $4$, then more apart — at $1.79\times10^{18}$, $2^{60-52}=256$ apart.
>
> - **Example**: run 042's sidecar above, $202$ bytes, and every count of the run: $1042$ is an exact JSON number in any language.
> - **Non-example**: `{"goal": NaN}`, which Python writes by default and RFC 8259 forbids; and the stamp $1{,}790{,}000{,}012{,}035{,}120{,}562$, valid JSON that a double-based reader silently moves by $78\,\mathrm{ns}$.
> - **Why it matters**: configurations and metadata cross languages — a Python trainer, a C++ node, a web dashboard — and each reader's domain, not Python's, decides what survives.

**Where JSON is used, and where it is not.** robomimic keeps each training run's configuration as a JSON file passed to its trainer with `--config`, and LeRobot describes a dataset in `meta/info.json` and `meta/stats.json` (§8). For configs JSON's lack of comments is its cost: a gain cannot carry the note that says why it is $200$. For logs its cost is size: one object per sample repeats every name, $26$ of $67$ characters for tick 2407, and even one array per column, which writes each name once, spends $45.03$ bytes a sample against the binary $20$ (§10). A file with **one JSON text per line** — a convention, not part of RFC 8259 — can at least be appended to and read line by line; LeRobot's earlier dataset versions kept their episode list that way, in `meta/episodes.jsonl`.

### 4. YAML: indentation, types by spelling, and two readers in one robot

*In one sentence:* YAML lets people write configuration by hand, with comments and without quotes, but it gives an unquoted value the type its spelling matches in the reader's table — and a ROS 2 system contains two readers with different tables.

YAML is the format of ROS 2 parameter files, of rosbag2's `metadata.yaml`, of launch files written in YAML, and of much of the configuration in learning code. Its structure is indentation: a key followed by a colon holds whatever is indented under it, and a line starting with `- ` is an item of a list. Indentation must be spaces — the specification forbids tabs there. A `#` after whitespace starts a comment, and comments are a presentation detail with no effect on the loaded data, so a program that loads a config and writes it back loses every comment. YAML 1.2 (2009; revision 1.2.2, 2021) made YAML a superset of JSON and dropped most of version 1.1's implicit typing, but much software still reads YAML 1.1 — which is the next paragraph's problem.

The part that bites is **types by spelling**. A quoted value is a string. An unquoted one — a *plain scalar* — gets its type from the first pattern it matches in the reader's schema, and the schemas differ. YAML 1.2's core schema knows `true`/`false` in three capitalizations, decimal integers, `0o` octal, `0x` hex and floats; YAML 1.1's type repository also reads `y`, `yes`, `on`, `n`, `no`, `off` as booleans, a leading `0` as octal, `1_000` as a thousand and `12:30` as a base-60 number, and it demands a decimal point in a float. And a ROS 2 system contains two YAML readers:

- **At start-up**, a node given `--params-file` — which is how a launch file hands it a parameter file, even one built from a Python dictionary — reads the file with rcl's C parser. It takes a quoted value as a string; otherwise it tests YAML 1.1's 22 boolean words, `y` and `n` included, then C's number parsing, which reads a leading `0` as octal and accepts `5e-3`, `nan` and `inf`; anything else is a string.
- **At run time**, `ros2 param set` and `ros2 param load` parse with PyYAML (Jazzy's rclpy), which calls itself a complete YAML 1.1 parser but leaves the single letters `y`, `Y`, `n`, `N` out of its booleans. `ros2 param load` even parses twice: it loads the file, turns each value back into text and parses that text again, so a quoted string that looks like a boolean or a number loses its quotes on the way.

The table resolves ten plain scalars three ways; the code that prints it, a transcription of each reader's rules, is in the callout under the table.

| plain scalar | YAML 1.2 core | PyYAML (YAML 1.1) | ROS 2 rcl, at start-up |
|---|---|---|---|
| `0.005` | float 0.005 | float 0.005 | float 0.005 |
| `5e-3` | float 0.005 | str `'5e-3'` | float 0.005 |
| `1.10` | float 1.1 | float 1.1 | float 1.1 |
| `0123` | int 123 | int 83 | int 83 |
| `08` | int 8 | str `'08'` | float 8.0 |
| `y` | str `'y'` | str `'y'` | bool True |
| `off` | str `'off'` | bool False | bool False |
| `12:30` | str `'12:30'` | int 750 | str `'12:30'` |
| `1_000` | str `'1_000'` | int 1000 | str `'1_000'` |
| `2026-09-21` | str `'2026-09-21'` | date 2026-09-21 | str `'2026-09-21'` |

> [!note]- Deeper · 더 깊이
> **How the table was computed.** Each resolver is a transcription, restricted to plain scalars: the core-schema table of YAML 1.2.2 §10.3.2; PyYAML's `resolver.py`; and `get_value()` in rcl's `rcl_yaml_param_parser` on the Jazzy branch, which tests the `!!str` tag and quotes first, then the 22 boolean words, then `strtoll` with base 0, then `strtod`. Every row agrees with PyYAML 6.0.1 and with the C library's `strtoll` and `strtod`, run separately on the machine that wrote this page. The PyYAML calls behind `ros2 param set` and `ros2 param load` are rclpy's `get_parameter_value` and `parameter_dict_from_yaml_file`; the second passes each loaded value through `str()` into the first, which is the double parse above.
>
> ```python
> import datetime, re
>
> def first_match(table, s):
>     """The type of a plain scalar: the first pattern that matches all of it; a string if none does."""
>     for pattern, convert in table:
>         if re.fullmatch(pattern, s):
>             return convert(s)
>     return s
>
> def int_1_1(s):                                    # PyYAML's int: underscores, 0b, 0x, leading-0 octal, base 60
>     s = s.replace("_", "")
>     sign, s = (-1 if s[0] == "-" else 1), s.lstrip("+-")
>     if ":" in s:
>         return sign * sum(int(x) * 60 ** i for i, x in enumerate(reversed(s.split(":"))))
>     base = 2 if s[:2] == "0b" else 16 if s[:2] == "0x" else 8 if s[0] == "0" and len(s) > 1 else 10
>     return sign * int(s, base)
>
> CORE_1_2 = [                                       # YAML 1.2.2, section 10.3.2 (core schema)
>     (r"null|Null|NULL|~|", lambda s: None),
>     (r"true|True|TRUE|false|False|FALSE", lambda s: s.lower() == "true"),
>     (r"[-+]?[0-9]+", int),
>     (r"0o[0-7]+", lambda s: int(s[2:], 8)),
>     (r"0x[0-9a-fA-F]+", lambda s: int(s[2:], 16)),
>     (r"[-+]?(\.[0-9]+|[0-9]+(\.[0-9]*)?)([eE][-+]?[0-9]+)?", float),
>     (r"[-+]?\.(inf|Inf|INF)|\.(nan|NaN|NAN)", lambda s: float(s.replace(".", ""))),
> ]
> PYYAML_1_1 = [                                     # PyYAML's resolver.py: YAML 1.1 without y, Y, n, N
>     (r"yes|Yes|YES|no|No|NO|true|True|TRUE|false|False|FALSE|on|On|ON|off|Off|OFF",
>      lambda s: s.lower() in ("yes", "true", "on")),
>     (r"[-+]?[0-9][0-9_]*\.[0-9_]*([eE][-+][0-9]+)?|\.[0-9][0-9_]*([eE][-+][0-9]+)?",
>      lambda s: float(s.replace("_", ""))),         # (its base-60, .inf and .nan floats are left out here)
>     (r"[-+]?0b[0-1_]+|[-+]?0[0-7_]+|[-+]?(0|[1-9][0-9_]*)|[-+]?0x[0-9a-fA-F_]+|[-+]?[1-9][0-9_]*(:[0-5]?[0-9])+",
>      int_1_1),
>     (r"~|null|Null|NULL|", lambda s: None),
>     (r"[0-9]{4}-[0-9]{2}-[0-9]{2}", datetime.date.fromisoformat),   # the date form of its timestamp rule
> ]
> RCL_TRUE = "Y y yes Yes YES true True TRUE on On ON".split()
> RCL_FALSE = "N n no No NO false False FALSE off Off OFF".split()
>
> def int_strtoll(s):                                # C strtoll(s, &end, 0) reading all of s
>     sign, s = ("-" if s[0] == "-" else ""), s.lstrip("+-")
>     return int(sign + s, 16 if s[:2] in ("0x", "0X") else 8 if s[0] == "0" and len(s) > 1 else 10)
>
> RCL = [                                            # rcl_yaml_param_parser get_value(), Jazzy: the order it tries
>     ("|".join(RCL_TRUE + RCL_FALSE), lambda s: s in RCL_TRUE),
>     (r"[-+]?(0[xX][0-9a-fA-F]+|0[0-7]*|[1-9][0-9]*)", int_strtoll),
>     (r"[-+]?\.(inf|Inf|INF)|\.(nan|NaN|NAN)", lambda s: float(s.replace(".", ""))),
>     (r"[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?|[-+]?(?i:inf|infinity|nan)", float),   # strtod
> ]
>
> def show(v):
>     return "%s %r" % (type(v).__name__, v) if not isinstance(v, datetime.date) else "date " + v.isoformat()
>
> print("%-12s %-20s %-20s %s" % ("scalar", "YAML 1.2 core", "PyYAML (YAML 1.1)", "ROS 2 rcl"))
> for s in ("0.005", "5e-3", "1.10", "0123", "08", "y", "off", "12:30", "1_000", "2026-09-21"):
>     print("%-12s %-20s %-20s %s" % (s, show(first_match(CORE_1_2, s)), show(first_match(PYYAML_1_1, s)),
>                                     show(first_match(RCL, s))))
> ```

Read the rows as P6's config edited by hand:

- `control_period: 5e-3` starts the controller at $200\,\mathrm{Hz}$, because rcl reads a double; typed later as `ros2 param set /cart/controller control_period 5e-3`, the same text reaches PyYAML, arrives as a string and is refused by the parameter's declared type — the type clause of [[04-robotics/ros2/services-actions-parameters|25.3 §6]].
- A driver parameter `motion_axis: y` becomes a boolean at start-up while `x` and `z` stay strings, so exactly one of three axes fails.
- A zero-padded `device_id: 0123` is 83 to both ROS readers and 123 to a YAML 1.2 tool; `version: 1.10` is the float 1.1 everywhere.
- A run date `date: 2026-09-21`, loaded in a Python script, becomes a `datetime.date`, which `json.dumps` refuses to write.

None of these is an error in the YAML; each is a value whose type depends on who reads it. The cure is the same every time: quote any string that could look like a number or a boolean, write floats with a point and digits on both sides (`0.005`), and never zero-pad an integer. Quoting protects a string at start-up and in `ros2 param set`, but not in `ros2 param load`, whose second parse reads a quoted `"on"` as the boolean true — so the safest string is one no reader could take for anything else.

> **Implicit typing, defined.** **Implicit typing** — YAML's *tag resolution* — is a *rule of the reader's schema*: a function from a plain scalar's text to a type, applied by whoever loads the file; the file itself carries no type. Four conditions. It applies **only to plain scalars**: a quoted scalar is a string and an explicit tag such as `!!str` overrides everything; the schema holds an **ordered list of patterns**, each tied to a type; the **first pattern that matches the whole text** decides; and **no match means a string** in the core schema (the JSON schema calls it an error instead).
>
> $$\operatorname{type}(s)=\tau_{j^\star},\qquad j^\star=\min\{\,j:\ s\in L(r_j)\,\},\qquad \operatorname{type}(s)=\text{str if no }r_j\text{ matches}$$
>
> where $s$ is the scalar's text, $r_1,r_2,\dots$ the schema's patterns in order, $L(r_j)$ the set of strings pattern $r_j$ matches in full and $\tau_j$ its type — so the same text has as many types as there are schemas that read it.
>
> - **Example**: `5e-3` matches the core float pattern, which allows an exponent without a point, and becomes $0.005$; PyYAML's float pattern requires a decimal point (and a sign on any exponent), so `5e-3` falls through to a string.
> - **Non-example**: `"5e-3"` in quotes, a string for every reader — quoting switches implicit typing off. Nor is the parameter file's shape, a node name over the literal key `ros__parameters`, a typing rule: that is a convention of the ROS 2 reader, defined in [[04-robotics/ros2/services-actions-parameters|25.3 §7]], with its namespace pitfalls in [[04-robotics/ros2/workspaces-packages-launch|25.4 §11]].
> - **Why it matters**: a config is read by more than one program — the node at start-up, the command line, your analysis script — and a value whose type depends on the reader is a bug that waits for the second reader.

**Configs in learning code.** Hydra, a Python framework common in robot-learning code, composes a hierarchical configuration from several YAML files and lets any value be overridden on the command line; for every run it writes the composed configuration to `.hydra/config.yaml` in the run's output directory, with the overrides beside it in `overrides.yaml`. That is the configuration snapshot the artifact checklist of [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility §7]] asks every reported run to keep. Whatever builds the config, save the exact file a run used, beside its log.

### 5. XML: a tree of elements whose values are all strings

*In one sentence:* XML writes a tree — which is why ROS uses it for a robot's links and joints — but every value in it is a string, so a URDF's numbers are only as right as the reader that converts them.

XML 1.0 (W3C, fifth edition, 2008) is older than JSON and YAML and still describes most of a ROS robot: its URDF ([[04-robotics/ros2/describing-a-robot|25.6 §2]]), the Xacro macros that generate it (§5 there), every package's `package.xml` ([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]) and launch files written in XML (§9 there). An XML document is a tree of **elements**. Each element is a start tag and an end tag with content between them, or one empty-element tag such as `<link name="base_link"/>`; a start tag may carry **attributes**, `name="value"` pairs with quoted values. The rules that make a document **well-formed** are few: exactly one root element contains all the others; an element that starts inside another ends inside it; an attribute name appears at most once in a tag; `<` and `&` in text are escaped as `&lt;` and `&amp;`; and a comment, `<!-- … -->`, must not contain two hyphens in a row.

What XML does not have is types. Every attribute value and every piece of text is a string, and the program that reads the file decides what the string means. A URDF joint origin, `<origin xyz="0.10 0 0.25" rpy="0 0 0"/>`, is two strings of three space-separated numbers, and it is the URDF reader, not XML, that splits them and converts them to metres and radians. Here is P6's camera mount, the one fixed joint that [[04-robotics/ros2/describing-a-robot|25.6]] freezes, read with the standard library:

```python
import xml.etree.ElementTree as ET

urdf = """<robot name="p6_cart">
  <link name="base_link"/>
  <link name="camera_link"/>
  <!-- the camera mount frozen on 25.6: 0.10 m ahead, 0.25 m above -->
  <joint name="camera_mount" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.10 0 0.25" rpy="0 0 0"/>
  </joint>
</robot>"""
root = ET.fromstring(urdf)
xyz = root.find("joint/origin").get("xyz")
print(root.tag, len(list(root.iter())), "elements;", repr(xyz), "->", [float(s) for s in xyz.split()])
print("comments after parsing:", ET.tostring(root, encoding="unicode").count("<!--"))
try:
    ET.fromstring(urdf + "\n<robot name='second'/>")      # a second root element
except ET.ParseError as err:
    print("ParseError:", err)
```

```text
robot 7 elements; '0.10 0 0.25' -> [0.1, 0.0, 0.25]
comments after parsing: 0
ParseError: junk after document element: line 11, column 0
```

Three lessons in three lines of output. The attribute came back as the string `'0.10 0 0.25'`, and turning it into numbers was this script's job. The comment that said where the numbers came from did not survive parsing — Python's `ElementTree` skips comments — so a tool that loads a URDF and writes it back drops its documentation, exactly like a YAML load–dump cycle (§4). And two robots pasted into one file are not a larger robot but no document at all: the parser stops at the second root.

**Well-formed is not correct.** The parser checks only XML's own syntax, the rules listed at the top of this section, without knowing what any element means. A URDF whose `xyz` is misspelled `xzy` is still well-formed, because nothing in XML knows which attributes an `origin` should have; that check falls to the URDF reader — so "the file parses" says nothing about the numbers in it.

**Use it as you find it.** A researcher rarely chooses XML; ROS chose it for URDF and `package.xml`, and the XML launch format exists beside the Python and YAML ones. What the format asks of you is to keep units in a comment or a README (the file cannot carry them in a type), to let a tool such as Xacro generate repeated structure instead of copying it, and to parse untrusted XML carefully — Python's documentation of `xml.etree` points to its XML security notes for exactly that case.

### 6. CSV: a table with no types

*In one sentence:* CSV solves "a table anyone can open" at the price of having no types, no units and no single standard, so everything a reader needs beyond the characters lives outside the file.

CSV is the format everyone can open and nobody specified until late: RFC 4180 (October 2005) is an informational memo that describes the common practice rather than a standard that defines it, and Python's `csv` documentation says that the lack of a well-defined standard leaves subtle differences between the files different applications produce and accept. The practice RFC 4180 records is this: one record per line, the line ending in CRLF; an optional first line of field names; fields separated by commas, with spaces counting as part of a field; and any field that contains a comma, a double quote or a line break enclosed in double quotes, with a double quote inside it written twice.

```python
import csv, io

buf = io.StringIO()
w = csv.writer(buf)                                        # the default dialect: minimal quoting, rows end "\r\n"
w.writerow(["run", "topics", "note", "kp"])
w.writerow(["042", "/cart/goal,/cart/cmd", 'goal "held" at 0.6 m', 200.0])
print(repr(buf.getvalue()))
rows = list(csv.reader(io.StringIO(buf.getvalue())))
print(rows[1], [type(x).__name__ for x in rows[1]])       # four fields back, every one a str
```

```text
'run,topics,note,kp\r\n042,"/cart/goal,/cart/cmd","goal ""held"" at 0.6 m",200.0\r\n'
['042', '/cart/goal,/cart/cmd', 'goal "held" at 0.6 m', '200.0'] ['str', 'str', 'str', 'str']
```

The writer quoted the field with the comma and doubled the quotes inside the note, and it ended each row with `\r\n`, the module's default terminator; the documentation asks you to open CSV files with `newline=""`, without which newlines inside quoted fields are misread and some platforms write an extra `\r`. The reader gave back four strings. **CSV has no types**: `'200.0'` is text until someone calls `float`, `'042'` becomes $42$ if someone calls `int` on a run ID, and the reader performs no conversion unless told to treat every unquoted field as a float (`QUOTE_NONNUMERIC`). The header row is the only schema, and it holds names, not units; `u` does not say newtons, and `t_s,counts,u_N` is a cheap improvement.

For logs the questions are precision and size, and both are the writer's choice, not the format's. The `csv` module writes a float with `str`, which is `repr` (§2), so a run written from Python floats reads back exactly: $42.03$ bytes a sample for P6, $2.10\times$ the binary (§10). The loss comes from a format string. `"%.3f"` shrinks the line to $25.73$ bytes and loses up to $200\,\mu\mathrm{s}$ of the time — all of the jitter — and $0.5\,\mathrm{mN}$ of the command. NumPy's `np.savetxt` goes the other way: its default `fmt="%.18e"` prints 19 significant digits in exponent form, exact but $75.50$ bytes a sample, larger than JSON, and it writes the count $1042$ as `1.042000000000000000e+03`, which reads back as the float `1042.0` — the value survives, the type does not.

> **CSV table, defined.** A **CSV table** is a *delimited text table*: a sequence of records, each a line of text fields — a way of writing rows, with no types and no schema of its own. Four conditions: **one record per line**; **fields separated by a delimiter**, a comma; a field that contains the delimiter, a quote or a line break is **enclosed in quotes, with inner quotes doubled**; and **every field is text** until a reader converts it, with at most one header line of names. A file of $n$ records of $m$ fields plus a header takes
>
> $$B=\sum_{r=0}^{n}\Big(\sum_{i=1}^{m}\ell_{ri}+(m-1)+\lambda\Big)$$
>
> bytes, where $r=0$ is the header, $\ell_{ri}$ the characters of field $i$ in record $r$ with any quotes, $m-1$ the commas and $\lambda$ the terminator: $1$ for `\n`, $2$ for the module's default `\r\n` — since every character, comma and line end of an ASCII file is one byte.
>
> - **Example**: run 042 written with `repr` and `\n`: an $11$-byte header `t,counts,u` plus $504{,}329$ bytes of records, $504{,}340$ in all (§10); with `\r\n` it would be $12{,}001$ bytes more.
> - **Non-example**: a "CSV" with a semicolon delimiter and a decimal comma, which is a different dialect that a comma-reader splits into the wrong fields; and the count column of `np.savetxt`, which is valid CSV whose values read back as floats — a table can keep every value and still lose a type.
> - **Why it matters**: a CSV file is the easiest thing to send and the easiest to misread, because everything the reader needs beyond the characters — delimiter, quoting, digits, units, types — lives outside the file.

**When to use it.** CSV is right for a small table a person will open, and for a quick log from a script that appends a line per sample and can crash without losing more than the last line. Write it with `repr` or with enough digits (§2), name the units in the header, keep the sidecar (§3) beside it, and move to binary for anything logged by the hour: P6's hour is $30\,\mathrm{MB}$ of text against $14.4\,\mathrm{MB}$ of binary, and every read parses every character again.

### 7. Binary records: widths, byte order, alignment and the `.npy` header

*In one sentence:* binary records keep samples small, fast and exact — each field's own bytes, laid out by a rule of widths, offsets, byte order and padding — and a file is useful only if that rule travels with it.

A float64 is the 8 bytes of an IEEE 754 binary64 number and an int32 is 4 bytes, whatever their values. Written one after another they make a **record**, and a file of records needs three facts before its bytes mean anything. **Byte order**: x86-64 processors and the Apple M1 laptop that ran this page's code are little-endian, and the `struct` module's `<` prefix writes little-endian whatever the machine. **Offsets**: where each field starts. **Alignment**: whether fields are packed back to back or padded so that each starts at a multiple of its own size, as a C compiler lays out a struct. Python's `struct` module adds no padding in its standard modes (`<`, `>`, `=`, `!`) and pads like the local C compiler in native mode (`@`); NumPy packs a structured dtype by default and pads it like a C struct with `align=True`, including trailing padding up to a multiple of the largest field's alignment.

```python
import io, struct
import numpy as np

rec = struct.pack("<did", 1790000012.0351205, 1042, -1.9578125000000002)   # sample 2407: t, counts, u
print(len(rec), rec.hex(" "))
print("struct sizes: '<did' %d, native '@did' %d" % (struct.calcsize("<did"), struct.calcsize("@did")))
print("the count's 4 bytes read little-endian %d, big-endian %d"
      % (int.from_bytes(rec[8:12], "little"), int.from_bytes(rec[8:12], "big")))
fields = [("t", "<f8"), ("counts", "<i4"), ("u", "<f8")]
packed, aligned = np.dtype(fields), np.dtype(fields, align=True)
print("itemsize packed %d, offsets %s; aligned %d, offsets %s"
      % (packed.itemsize, [packed.fields[f][1] for f in packed.names],
         aligned.itemsize, [aligned.fields[f][1] for f in aligned.names]))
buf = io.BytesIO()
np.save(buf, np.zeros(12000, dtype=packed))
blob = buf.getvalue()
hlen = int.from_bytes(blob[8:10], "little")
print(blob[:8], "header length", hlen, "-> data starts at byte", 10 + hlen, "; file", len(blob), "bytes")
print(blob[10:10 + hlen].decode().strip())
wrong = np.frombuffer(rec * 12000, dtype=aligned)          # 12,000 packed records read with the aligned layout
print(len(wrong), "records; the first reads t = %r, counts = %d, u = %r"
      % (float(wrong[0]["t"]), wrong[0]["counts"], float(wrong[0]["u"])))
```

```text
20 6a 3f 02 e3 4e ac da 41 12 04 00 00 34 33 33 33 33 53 ff bf
struct sizes: '<did' 20, native '@did' 24
the count's 4 bytes read little-endian 1042, big-endian 302252032
itemsize packed 20, offsets [0, 8, 12]; aligned 24, offsets [0, 8, 16]
b'\x93NUMPY\x01\x00' header length 182 -> data starts at byte 192 ; file 240192 bytes
{'descr': [('t', '<f8'), ('counts', '<i4'), ('u', '<f8')], 'fortran_order': False, 'shape': (12000,), }
10000 records; the first reads t = 1790000012.0351205, counts = 1042, u = -8.608277440935864e+168
```

The picture's top two bars are these lines. The count $1042$ is `0x0412`, stored low byte first as `12 04 00 00`; read big-endian, the same four bytes are $302{,}252{,}032$, with no error — a wrong byte order does not fail, it lies. Aligned, the count's field is followed by 4 padding bytes so that $u$ starts at byte $16$, a multiple of $8$, and each record grows from $20$ to $24$ bytes, $17.28$ instead of $14.40\,\mathrm{MB}$ an hour for nothing but alignment.

**The `.npy` file** is NumPy's answer to "the layout must travel with the bytes": a short text header that names the dtype — NumPy's record of each field's name, type, width and byte order, here `[('t', '<f8'), ('counts', '<i4'), ('u', '<f8')]` — and the shape, then the raw data. Here the header ends at byte $192$, and $192+12{,}000\times20=240{,}192$ bytes is the whole file. Two more facts belong to daily use. An **`.npz`** file is a zip archive of `.npy` files, one per array, stored uncompressed by `np.savez` and deflate-compressed by `np.savez_compressed`. And **`np.load` refuses pickled object arrays by default** (`allow_pickle=False`), because loading a pickle can execute arbitrary code — never switch it on for a file you did not write.

> [!note]- Deeper · 더 깊이
> **The `.npy` header, byte by byte.** The format is documented so that other languages can read it: the magic string `\x93NUMPY`, one byte each of major and minor version, a two-byte little-endian header length (version 1.0), and a header that is a Python dictionary literal — `descr`, the dtype; `fortran_order`; `shape` — padded with spaces and a final newline so that magic, version, length and header together fill a multiple of $64$ bytes. Here that is $10+182=192=3\times64$, which is what the listing printed.

> **Binary record layout, defined.** A **binary record layout** is the *fixed arrangement of typed fields in bytes* that a binary file's rows follow — a C struct, a NumPy structured dtype, a `struct` format string. Four conditions. Every field has a **type of fixed width**; every field has an **offset** from the record's start; the multi-byte values have one **byte order**; and one **alignment rule** fixes the offsets — packed, each field starting where the last ended, or aligned, each offset a multiple of its field's alignment and the record padded to a multiple of the largest. In one formula,
>
> $$o_1=0,\qquad o_{i+1}=\big\lceil (o_i+w_i)/a_{i+1}\big\rceil\,a_{i+1},\qquad S=\big\lceil (o_m+w_m)/a^\star\big\rceil\,a^\star,\qquad B_{\text{file}}=H+nS$$
>
> where $w_i$ is field $i$'s width, $a_i$ its alignment ($1$ when packed, usually $w_i$ when aligned), $a^\star=\max_i a_i$, $S$ the record size, $n$ the number of records and $H$ the header — so padding appears exactly where a narrow field precedes a wider one.
>
> - **Example**: P6's record `t` f8, `counts` i4, `u` f8. Packed: offsets $0, 8, 12$ and $S=20$; aligned: offsets $0, 8, 16$ and $S=24$; as `.npy`, $B_{\text{file}}=192+12{,}000\times20=240{,}192$ bytes.
> - **Non-example**: "a file of 20-byte samples" with no layout written anywhere. Read with `>` instead of `<`, the count becomes $302{,}252{,}032$; read with the aligned layout, the $240{,}000$ bytes of $12{,}000$ packed records become $10{,}000$ records whose first command is $-8.6\times10^{168}\,\mathrm{N}$, since $240{,}000$ happens to divide by $24$ — and neither mistake raises an error.
> - **Why it matters**: binary is where robot data is small, fast and exact, and it keeps those properties only while the layout is stored with it — in a header, a schema or at least a sidecar.

### 8. Containers for robot data: HDF5, Parquet and MCAP

*In one sentence:* a run or a dataset is many arrays or messages plus their names and schema, a container keeps them in one file, and the three a robot-learning researcher meets are organized differently — HDF5 as a tree of arrays, Parquet as columns, MCAP as a time-ordered stream of messages.

This section describes HDF5 and Parquet from their documentation and from the dataset formats that use them; their libraries are not part of this page's lab. MCAP's record framing is simple enough to build with `struct`, and the code below does.

**HDF5.** An HDF5 file is a container made of two kinds of object, *groups* and *datasets*, addressed by paths the way directories and files are: `/` is the root group, and `/data/demo_0/actions` is a dataset two groups down. A dataset is a multidimensional array with its type and shape; any object can carry *attributes*, small named values of metadata. A dataset is stored contiguous by default; the *chunked* layout, equal blocks that the library always reads and writes whole, is required for compression and for datasets that can grow. **robomimic**, the benchmark of learning from human demonstrations, stores each dataset as one HDF5 file with one group per demonstration; P6's run would sit there as one demonstration, `u` in `actions` as a $(12{,}000, 1)$ array and the counts under `obs`. See [[01-canonical-papers/notes/4-vla/robomimic|robomimic]] for what the benchmark measures.

**Parquet.** Apache Parquet is a column-oriented file format: a file holds one or more *row groups*, each row group holds exactly one *column chunk* per column, contiguous in the file, and each column chunk is divided into *pages*, the indivisible unit of encoding and compression. The file starts and ends with the four bytes `PAR1`, and its metadata — among it, where every column chunk starts — is written after the data, so that a writer can stream in one pass and a reader starts at the footer. **LeRobot**'s dataset format, version 3.0, is built on it: frames (states, actions, timestamps) in Parquet files that hold many episodes each, the schema and frame rate in `meta/info.json`, normalization statistics in `meta/stats.json`, and camera streams as MP4 video.

> [!note]- Deeper · 더 깊이
> **The two dataset layouts in full.** *robomimic*: a group `data` whose attributes give the total number of samples and, in `env_args`, the environment's metadata as a JSON string; under it one group per demonstration, `demo_0`, `demo_1`, …, with an attribute `num_samples` and datasets `actions` of shape $(N, A)$, `rewards`, `dones`, `states`, and groups `obs` and `next_obs` holding one dataset per observation key; and a `mask` group whose filter keys list the demonstrations of subsets such as train and validation. *LeRobot v3.0*: frame data under `data/chunk-000/file-000.parquet`, each file capped at 100 MB by default; per-episode records — lengths, tasks and the offsets that recover each episode's rows — as Parquet under `meta/episodes/`; path templates beside the schema in `meta/info.json`; and one set of MP4 files per camera. Version 3.0 replaced version 2's one file per episode with many episodes per file, to put fewer, larger files on the file system.

**MCAP.** MCAP is rosbag2's default storage format since ROS 2 Iron Irwini (May 2023), whose release replaced the previous default, sqlite3, and so it is what Jazzy's `ros2 bag record` writes ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §7]]). A file is the magic bytes `0x89 M C A P 0 \r \n`, then a sequence of records, each a one-byte opcode, a uint64 length and the content, all little-endian. *Schema* records say how a message type is encoded, *Channel* records tie a topic to a schema, and each *Message* record holds a channel id (uint16), a sequence number (uint32), a log time and a publish time (uint64 nanoseconds each) and then the serialized message. Records can be grouped into *chunks*, compressed with zstd or lz4, and indexed so that a reader can seek by time; the summary section with those indexes is optional and written at the end. Because every record states its own length, a reader can walk the data section from the front with no index at all.

```python
import struct

payload = struct.pack("<did", 1790000012.0351205, 1042, -1.9578125000000002)   # the 20-byte sample
log_ns = 1790000012035120562                                                   # its clock reading, ns
content = struct.pack("<HIQQ", 1, 2407, log_ns, log_ns) + payload             # channel, sequence, log, publish
record = struct.pack("<BQ", 0x05, len(content)) + content                      # opcode 0x05, length, content
print("MCAP message record: %d bytes, %d of them framing" % (len(record), len(record) - len(payload)))
per_hour = 200 * 3600
for batch in (1, 200):                              # samples packed into one message
    size = per_hour // batch * 31 + per_hour * 20
    print("%3d sample(s) per message: %.2f MB/h, framing %.2f%%" % (batch, size / 1e6, 100 * (size - per_hour * 20) / size))
n, widths = 12000, {"t": 8, "counts": 4, "u": 8}
print("bytes read for u alone: row layout %d, column layout %d" % (n * sum(widths.values()), n * widths["u"]))
```

```text
MCAP message record: 51 bytes, 31 of them framing
  1 sample(s) per message: 36.72 MB/h, framing 60.78%
200 sample(s) per message: 14.51 MB/h, framing 0.77%
bytes read for u alone: row layout 240000, column layout 96000
```

A message record costs $1+8+2+4+8+8=31$ bytes before its payload. If each P6 sample were a 20-byte message, framing would be $61\%$ of the file, $36.72$ against $14.40\,\mathrm{MB/h}$, before any index; batched $200$ samples to a message, $0.77\%$. A real ROS 2 message is usually larger than these 20 bytes — P6's would carry a `Header` with a stamp and a frame id ([[04-robotics/ros2/nodes-topics-messages|25.2 §4]]) — so the framing share is smaller; the arithmetic is the point: a fixed cost per message is paid at the message rate, not at the data rate.

> **Columnar layout, defined.** A **columnar layout** is a *way of ordering a table's bytes* in which all the values of one column are stored together, as opposed to a row layout, in which each record's fields sit together — a property of the file, not of the table. Four conditions: a table of $n$ rows and $m$ **typed columns**; each column's values **contiguous**, at least within a row group; **per-column metadata** — type, encoding, compression — in a footer; and a reader that **selects columns before reading data**. Loading the columns in a set $S$ reads
>
> $$B^{\text{row}}=n\sum_{i=1}^{m}w_i,\qquad B^{\text{col}}(S)=n\sum_{i\in S}w_i$$
>
> bytes before compression, where $w_i$ is column $i$'s width — because a row layout interleaves the columns you skip with the ones you want.
>
> - **Example**: a loader that trains on P6's commands alone reads $12{,}000\times8=96{,}000$ bytes from a columnar file against $240{,}000$ from the packed record file, $40\%$; for an hour, $5.76$ against $14.4\,\mathrm{MB}$.
> - **Non-example**: MCAP. A bag is a stream of whole messages in the order they were logged, which is a row layout on purpose: a recorder appends each message as it arrives and a player replays them in time order, and reading one field of one topic still means decoding every message of that topic.
> - **Why it matters**: a robot records rows and a learning pipeline reads columns, which is why the dataset formats of learning code — LeRobot's Parquet, robomimic's one dataset per key — are not the recorder's format.

### 9. Markdown: CommonMark, tables, front matter and math in this wiki

*In one sentence:* Markdown is how this wiki and most research notes are written — text a person reads and Git diffs line by line — and the three formats inside this wiki's pages, front matter, tables and math, each carry a rule that bites.

Markdown is text with light markup — `#` for a heading, `*` for emphasis, a blank line between paragraphs — and every page of this wiki is written in it. Its core is specified by **CommonMark** (version 0.31.2, January 2024), which has no tables; tables come from **GitHub Flavored Markdown** (GFM), a strict superset of CommonMark: a header row, a delimiter row of hyphens whose colons set each column's alignment, and data rows, with cells separated by `|` and a `|` inside a cell written `\|`. This wiki is built with Quartz, whose `quartz.config.yaml` enables GFM, the Obsidian-flavored extensions — wikilinks and callouts such as `> [!note]` — and KaTeX, which renders math written between dollar signs, one for inline math and two for a display.

Three pieces of this wiki are formats in their own right:

- **Front matter.** The block between two `---` lines at the top of a page is YAML (§4) — `title`, `tags`, `study-depth` and the rest — and it is not Markdown at all: in CommonMark a line of text followed by `---` is a heading, since a setext underline takes precedence over a thematic break, so the site generator must remove the front matter before the Markdown parser sees it. Being YAML, it obeys §4: a title of `1.10` would be the float $1.1$, and a title containing `: ` needs quotes.
- **Tables of results.** A Markdown table is a presentation of numbers, not their source. On a Tier A page of this wiki every published table is the printed output of the published code, which is the discipline §10 follows; a table typed by hand is a place where a number and its computation can drift apart.
- **Emphasis next to a gloss.** CommonMark decides whether `**` can close bold from the characters on either side of it: after punctuation such as `)`, a `**` closes only if whitespace or punctuation follows. So `**용어(term)**이` renders with its asterisks showing, because `)` comes before them and the particle `이` after, while `**용어**(term)이`, with a letter before the asterisks, renders bold. This wiki's content check rejects the first form; the callout below states the rule and runs it.

> [!note]- Deeper · 더 깊이
> **The right-flanking rule, run.** A run of `*` or `_` is *right-flanking* — and a `**` can close strong emphasis only if it is — when it is not preceded by Unicode whitespace and either is not preceded by punctuation, or is preceded by punctuation and followed by whitespace or punctuation; the start and end of a line count as whitespace, and punctuation means the Unicode categories P and S (CommonMark §6.2). With $b$ and $a$ the characters before and after the run,
>
> $$R(b,a)=\neg W(b)\ \wedge\ \big(\neg P(b)\ \vee\ W(a)\ \vee\ P(a)\big)$$
>
> where $W$ is "is whitespace" and $P$ "is punctuation or symbol" — so after a closing parenthesis a `**` closes only if a space or another punctuation mark follows. The listing tests the last `**` of three strings:
>
> ```python
> import unicodedata
>
> def punct(ch):                                     # CommonMark counts Unicode categories P and S
>     return unicodedata.category(ch)[0] in "PS"
>
> def closes(text):
>     """Is the last double asterisk in text right-flanking, so that it can close strong emphasis?"""
>     i = text.rindex("*" * 2)
>     before, after = text[i - 1], (text[i + 2:] or " ")[0]      # the end of a line counts as whitespace
>     return before, after, not before.isspace() and (not punct(before) or after.isspace() or punct(after))
>
> star = "*" * 2
> for text in (star + "용어" + star + "(term)이", star + "용어(term)" + star + "이", star + "term" + star + "s"):
>     print("before %r, after %r -> closes: %s" % closes(text))
> ```
>
> ```text
> before '어', after '(' -> closes: True
> before ')', after '이' -> closes: False
> before 'm', after 's' -> closes: True
> ```
>
> In the second case the closing asterisks sit after `)`, a punctuation character, and before `이`, which is neither whitespace nor punctuation, so $R$ is false and the reader sees four literal asterisks; `**term**s` closes, because $b$ is the letter `m`.

**The format of this page, as a format.** Markdown promises the least of any format here — no types, no schema, and meaning that depends on the renderer's extensions — and it is still the right one for notes, because a person reads it as text and Git diffs it line by line. What makes it dependable is the same thing that makes CSV dependable: rules written down outside the file, and a check that enforces them.

### 10. The lab: one run, eight files, and a sweep over printed decimals

Four parts on the frozen run. Part 0 generates it — the clock, the goal, the PD controller on the counts and the cart stepped by semi-implicit Euler — and prints the Worked case's sample with its bytes in five formats. Part 1 writes the run eight ways into memory, with `io.BytesIO` and `io.StringIO` instead of files, reads each back with its own decoder, and prints the size, the rate per hour and the worst round-trip error of each column. Part 2 sweeps the number of printed decimals $d$ from $0$ to $9$ against `%.17g` and `repr`. Part 3 asks what four types for the time column keep of the integer-nanosecond clock. Nothing is timed and nothing is random, so the output is the same on any machine with NumPy 2.

```python
# 12.4 lab: one P6 run, written to eight files in memory, sized, read back, and swept over printed decimals.
import csv, io, json, struct
import numpy as np

# --- 0. the frozen run (Running object) ------------------------------------------------------------
F, D, CPM = 200, 60, 2048                   # P6: control rate (Hz), encoder (counts/m); run length (s)
N = F * D                                   # 12,000 samples
T0 = 1_790_000_000                          # run start, s since 1970-01-01 UTC (page-local)
M, KP, KD = 2.0, 200.0, 40.0                # page-local: cart mass (kg), PD gains (N/m, N s/m)

k = np.arange(N)
late_ns = (123_607 * k) % 200_001                  # tick k is stamped 0-200 us late: a deterministic stand-in
t_ns = T0 * 10 ** 9 + 5_000_000 * k + late_ns      # the clock, integer ns since 1970 (int64)
t = T0 + (5_000_000 * k + late_ns) / 1e9           # the logged time column: float64 s since 1970
counts = np.zeros(N, dtype=np.int32)               # encoder counts
u = np.zeros(N)                                    # motor command, N
goal = np.zeros(N)                                 # the vision goal each tick used, m (problem 3 logs it)
p, v, c_prev, g = 0.1, 0.0, 205, 0.1               # the cart starts at rest at 0.1 m, 205 counts
for i in range(N):
    if i % 4 == 0:                                 # a new vision goal every 4th tick, 50 Hz:
        g = 0.1 + 0.5 * (1 - abs(i % 4000 / 2000 - 1))    # a triangle, 0.1 -> 0.6 -> 0.1 m every 20 s
    c = round(p * CPM)                             # the encoder reads the cart
    u[i] = KP * (g - c / CPM) - KD * (c - c_prev) * F / CPM   # PD on counts; velocity from one difference
    counts[i], goal[i], c_prev = c, g, c
    v += u[i] / M / F                              # semi-implicit Euler (0.7 Lab Kernel, section 3)
    p += v / F
K = 2407                                           # the Worked case's sample
print("run: %d samples, counts %d..%d, u %.3f..%.3f N" % (N, counts.min(), counts.max(), u.min(), u.max()))
one = (float(t[K]), int(counts[K]), float(u[K]))
print("sample %d: t = %r s, counts = %d, u = %r N, stamped %d ns late" % (K, *one, late_ns[K]))
print("its bytes: struct %d, CSV repr %d, CSV %%.3f %d, JSON object %d (+2 between objects), np.savetxt %d"
      % (len(struct.pack("<did", *one)), len("%r,%d,%r\n" % one), len("%.3f,%d,%.3f\n" % one),
         len(json.dumps(dict(zip(("t", "counts", "u"), one)))), len("%.18e,%.18e,%.18e\n" % one)))

# --- 1. eight files in memory, each read back --------------------------------------------------------
cols = (t.tolist(), counts.tolist(), u.tolist())   # Python floats and ints, as a logger holds them

def to_csv(fmt):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")       # the module's default would end every row with "\r\n"
    w.writerow(["t", "counts", "u"])
    w.writerows([fmt(a), b, fmt(c)] for a, b, c in zip(*cols))
    return buf.getvalue().encode()

def from_csv(blob):
    rows = list(csv.reader(io.StringIO(blob.decode())))[1:]    # every field comes back as a str
    return [np.array([typ(r[j]) for r in rows]) for j, typ in enumerate((float, int, float))]

def npy(a):
    buf = io.BytesIO()
    np.save(buf, a)
    return buf.getvalue()

rec = np.zeros(N, dtype=[("t", "<f8"), ("counts", "<i4"), ("u", "<f8")])   # packed: 20 bytes a sample
rec["t"], rec["counts"], rec["u"] = t, counts, u
mat = np.column_stack([t, counts, u])                                      # float64 N x 3: 24 bytes a sample
txt = io.StringIO()
np.savetxt(txt, mat, delimiter=",")                                        # NumPy's default fmt is '%.18e'
files = {
    "struct '<did', no header": (b"".join(struct.pack("<did", *s) for s in zip(*cols)),
                                 lambda b: [np.array(x) for x in zip(*struct.iter_unpack("<did", b))]),
    ".npy, structured record": (npy(rec), lambda b: [np.load(io.BytesIO(b))[f] for f in ("t", "counts", "u")]),
    ".npy, float64 N x 3": (npy(mat), lambda b: list(np.load(io.BytesIO(b)).T)),
    "np.savetxt, default": (txt.getvalue().encode(),
                            lambda b: list(np.loadtxt(io.StringIO(b.decode()), delimiter=",").T)),
    "CSV, repr": (to_csv(repr), from_csv),
    "CSV, %.3f": (to_csv("%.3f".__mod__), from_csv),
    "JSON, object per sample": (json.dumps([{"t": a, "counts": b, "u": c} for a, b, c in zip(*cols)]).encode(),
                                lambda b: [np.array([o[key] for o in json.loads(b)]) for key in ("t", "counts", "u")]),
    "JSON, array per column": (json.dumps(dict(zip(("t", "counts", "u"), cols))).encode(),
                               lambda b: [np.array(json.loads(b)[key]) for key in ("t", "counts", "u")]),
}
base = len(files["struct '<did', no header"][0])
for name, (blob, read) in files.items():
    bt, bc, bu = read(blob)
    print("%-25s %7d bytes %6.2f B/sample %5.2fx %6.2f MB/h   max|dt| %.3g s   max|du| %.3g N   counts exact %s"
          % (name, len(blob), len(blob) / N, len(blob) / base, len(blob) / N * F * 3600 / 1e6,
             np.abs(bt - t).max(), np.abs(bu - u).max(), np.array_equal(bc, counts)))

# --- 2. the sweep: decimals printed against bytes and round-trip error ---------------------------------
for d in list(range(10)) + ["%.17g", "repr"]:
    fmt = repr if d == "repr" else d.__mod__ if isinstance(d, str) else ("%%.%df" % d).__mod__
    blob = to_csv(fmt)
    bt, bc, bu = from_csv(blob)
    print("%-6s %6.2f B/sample   max|dt| %.3e s   t exact %-5s   max|du| %.3e N   u exact %s"
          % (d, len(blob) / N, np.abs(bt - t).max(), np.array_equal(bt, t), np.abs(bu - u).max(),
             np.array_equal(bu, u)))

# --- 3. the time column's type: what each choice keeps of the integer-ns clock -------------------------
rel_ns = 5_000_000 * k + late_ns                   # the clock, ns since the run start (exact)
kinds = {"float64, s since 1970": t - T0,
         "float32, s since 1970": t.astype(np.float32).astype(np.float64) - T0,
         "float32, s since the start": (t - T0).astype(np.float32).astype(np.float64)}
for name, rel in kinds.items():
    print("%-27s %5d distinct stamps   worst error %.3g s" % (name, len(np.unique(rel)), np.abs(rel - rel_ns / 1e9).max()))
worst = max(abs(int(float(x)) - x) for x in t_ns.tolist())
print("int64 ns since 1970         %5d distinct stamps   exact; a binary64 JSON reader errs by up to %d ns"
      % (len(np.unique(t_ns)), worst))
```

**The sample**, Part 0: tick 2407, $t=1790000012.0351205\,\mathrm{s}$, $1042$ counts, $u=-1.9578125000000002\,\mathrm{N}$, stamped $120{,}562\,\mathrm{ns}$ late; its bytes are $20$ as a struct, $44$ as a `repr` CSV line, $27$ at `%.3f`, $67$ as a JSON object ($+2$ between objects) and $76$ from `np.savetxt`. Over the run the counts go from $205$ to $1218$ and the command from $-4.252$ to $4.013\,\mathrm{N}$.

**Eight files**, Part 1:

| file | bytes | bytes a sample | × struct | MB an hour | worst time error (s) | worst command error (N) | counts exact |
|---|---:|---:|---:|---:|---:|---:|---|
| struct `'<did'`, no header | 240,000 | 20.00 | 1.00 | 14.40 | 0 | 0 | yes |
| `.npy`, structured record | 240,192 | 20.02 | 1.00 | 14.41 | 0 | 0 | yes |
| `.npy`, float64 $N\times3$ | 288,128 | 24.01 | 1.20 | 17.29 | 0 | 0 | yes |
| `np.savetxt`, default | 906,001 | 75.50 | 3.78 | 54.36 | 0 | 0 | yes |
| CSV, `repr` | 504,340 | 42.03 | 2.10 | 30.26 | 0 | 0 | yes |
| CSV, `%.3f` | 308,700 | 25.73 | 1.29 | 18.52 | 0.0002 | 0.0005 | yes |
| JSON, object per sample | 804,329 | 67.03 | 3.35 | 48.26 | 0 | 0 | yes |
| JSON, array per column | 540,355 | 45.03 | 2.25 | 32.42 | 0 | 0 | yes |

**The sweep**, Part 2, both floats printed with the same format:

| printed as | bytes a sample | worst time error (s) | time exact | worst command error (N) | command exact |
|---|---:|---:|---|---:|---|
| $d=0$ | 17.73 | 5.000e-01 | no | 4.969e-01 | no |
| $d=1$ | 21.73 | 5.000e-02 | no | 5.000e-02 | no |
| $d=2$ | 23.73 | 5.000e-03 | no | 5.000e-03 | no |
| $d=3$ | 25.73 | 2.000e-04 | no | 5.000e-04 | no |
| $d=4$ | 27.73 | 5.007e-05 | no | 5.000e-05 | no |
| $d=5$ | 29.73 | 5.007e-06 | no | 5.000e-06 | no |
| $d=6$ | 31.73 | 4.768e-07 | no | 5.000e-07 | no |
| $d=7$ | 33.73 | 0 | yes | 5.000e-08 | no |
| $d=8$ | 35.73 | 0 | yes | 1.554e-14 | no |
| $d=9$ | 37.73 | 0 | yes | 1.554e-14 | no |
| `%.17g` | 42.46 | 0 | yes | 0 | yes |
| `repr` | 42.03 | 0 | yes | 0 | yes |

**The time column's type**, Part 3:

| time stored as | distinct stamps of 12,000 | worst error against the clock |
|---|---:|---:|
| float64, s since 1970 | 12,000 | 1.19e-07 s |
| float32, s since 1970 | 1 | 60 s |
| float32, s since the run start | 12,000 | 2.02e-06 s |
| int64, ns since 1970 | 12,000 | exact; 128 ns once read as a JSON number by a binary64 reader |

**Reading the tables.** Five predictions of the sections above, now counted.

- **Binary is the floor and text pays for readability.** The packed record is $20$ bytes a sample and the `.npy` file adds only its $192$-byte header; the float64 matrix pays $4$ bytes a sample to store an integer column as float64. Full-precision CSV costs $2.10\times$, JSON $2.25\times$ by columns and $3.35\times$ by objects, and `np.savetxt`'s default $3.78\times$, all of them exact.
- **The cheap text file is the lossy one.** `%.3f` is the only text file under $1.3\times$ binary, and the only one that does not read back: $0.2\,\mathrm{ms}$ of time and $0.5\,\mathrm{mN}$ of command gone.
- **Decimals buy exactness per column, not per file.** The time becomes exact at $d=7$, as the Worked case derived from its spacing; the command never does at a fixed $d$, and from $d=8$ its error is stuck at $1.554\times10^{-14}\,\mathrm{N}$ — the last bits of floats like $-1.9578125000000002$. Only significant digits, `%.17g` or `repr`, make both exact, and `repr` does it in fewer bytes because it stops at the shortest string that works.
- **The bound is a bound.** At $d=3$ the time's worst error is $200\,\mu\mathrm{s}$, well inside $500\,\mu\mathrm{s}$, because every nominal stamp is a whole millisecond and only the lateness is cut off; at $d=4$ and $5$ it is $50.07$ and $5.007\,\mu\mathrm{s}$, just past $\tfrac12 10^{-d}$ by the float grid, as §2's formula allows.
- **The type of a column is a precision decision.** Float32 seconds since 1970 turn the run into one instant; float32 seconds since the start keep $2\,\mu\mathrm{s}$; float64 seconds since 1970 keep $0.12\,\mu\mathrm{s}$; integer nanoseconds keep everything, until a double-based JSON reader rounds them to $128\,\mathrm{ns}$.

### 11. What this page does not cover

The ROS 2 machinery around these files is taught where it lives: parameters and the parameter file in [[04-robotics/ros2/services-actions-parameters|25.3 §6–§7]], launch files and namespaced parameter keys in [[04-robotics/ros2/workspaces-packages-launch|25.4 §9–§11]], URDF and Xacro in [[04-robotics/ros2/describing-a-robot|25.6]], and recording, inspecting and replaying bags in [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6–§8]]. Floating-point formats beyond what §2 needs — fp16, bf16 and quantized weights — are [[03-deep-learning/foundations/training-at-scale|1.3 §4]]. What a dataset must contain for a claim to stand — splits, provenance, the configuration snapshot — is [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility §7]] and [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]]. Images and video (PNG, JPEG, the MP4 streams of a LeRobot dataset), compression algorithms, databases, protocol buffers and the CDR serialization inside a ROS 2 message are outside this page, and so are the HDF5 and Parquet libraries themselves, which §8 describes from their documentation only. The tools around these files are this track's other pages: copying a day of them off the robot is [[02-foundations/tools/linux-shell|12.1 §8]], versioning the small ones and naming the large ones by checksum is [[02-foundations/tools/git-research-code|12.2 §6]], reading them into arrays is [[02-foundations/tools/python-research-code|12.3 §3]], printing a table's numbers to the digits the data support is [[02-foundations/tools/latex-figures-references|12.6 §9]], and the STEP and STL files a CAD program writes are [[02-foundations/tools/mechanical-design-fabrication|12.9 §2]].

### After reading

- [ ] Name the five promises of a format — types, schema, precision, comments, streaming — and place JSON, YAML, XML, CSV, `.npy`, HDF5, Parquet and MCAP on them.
- [ ] Count a record's bytes in binary and in text, per sample and per hour, and say why the binary size is fixed and the text size is not.
- [ ] Bound the round-trip error of a number printed with $d$ decimals, find the $d$ that makes it exact from the float spacing, and say why a signal near zero needs significant digits instead.
- [ ] Write valid JSON for a sidecar, and name what Python writes that RFC 8259 forbids and which integers every JSON reader keeps exactly.
- [ ] Resolve a plain YAML scalar under the YAML 1.2 core schema, PyYAML and ROS 2's rcl parser, and say which of the three reads a parameter file at start-up and which serves `ros2 param set`.
- [ ] Say what makes an XML file well-formed and why a well-formed URDF can still hold wrong numbers.
- [ ] Write a CSV file that reads back exactly, and name what the header cannot say.
- [ ] Lay out a binary record packed and aligned from its fields' widths, read a `.npy` header, and say what a wrong byte order or layout produces.
- [ ] Say how HDF5, Parquet and MCAP organize data, which one robomimic, LeRobot and rosbag2 use, and what an MCAP message costs in framing.
- [ ] Explain why `**용어(term)**이` renders with asterisks, and where this wiki's front matter, tables and math come from.

### Self-check

1. A colleague's log prints the time column, in seconds since 1970, with `%.3f`. What did the file lose, how much at most, and how many decimals would have kept it exactly?
2. The time column of run 042 becomes exact at seven decimals. Why does the command column not become exact at any fixed number of decimals, and what should its writer use?
3. `control_period: 5e-3` in P6's parameter file starts the controller at $200\,\mathrm{Hz}$, but `ros2 param set /cart/controller control_period 5e-3` is refused. Why?
4. Your sidecar stores a stamp as integer nanoseconds since 1970, and a dashboard whose JSON reader keeps numbers as doubles shows it $78\,\mathrm{ns}$ off. Which reader is wrong, and what would you write instead?
5. A $240{,}000$-byte file of P6 samples arrives with no header and no note. What three facts do you need before reading it, and what happens if you guess the alignment wrong?
6. Why is MCAP the right format to record P6 and Parquet a good one to train from the same data?
7. A Korean page shows `**용어(term)**이` with its asterisks visible. What rule did it break, and what is the fix?

> [!tip]- Answers
> 1. It lost everything below a millisecond — the tick's lateness, up to $0.5\,\mathrm{ms}$ by the bound, $0.2\,\mathrm{ms}$ in run 042 — so the file looks perfectly periodic because its jitter was deleted. Seven decimals keep it exactly, because $10^{-7}\,\mathrm{s}$ is finer than the float64 spacing near $t_0$, $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$, and a decimal within half a spacing parses back to the same float.
> 2. A float's spacing scales with its size. The time always sits near $1.79\times10^9\,\mathrm{s}$, so one step fits every sample; the command ranges over $\pm4\,\mathrm{N}$ and passes near zero, where the spacing shrinks with the value, so any fixed $d$ leaves some values off — $1.554\times10^{-14}\,\mathrm{N}$ at $d=8$ and $9$ in run 042. Significant digits scale with the value: `repr`, the default of `json` and `csv`, or `%.17g`, since seventeen significant digits always identify a float64.
> 3. Two readers. At start-up the node reads the file through rcl's C parser, which hands `5e-3` to `strtod` and gets the double $0.005$. `ros2 param set` parses its value with PyYAML, whose YAML 1.1 float pattern needs a decimal point (and a sign on any exponent), so `5e-3` stays the string `'5e-3'`, and the double parameter refuses a string. Write `0.005`.
> 4. Neither: the file is valid JSON, but $1.79\times10^{18}$ is past $2^{53}-1\approx9.0\times10^{15}$, the range RFC 8259 names as exact for every implementation, and a reader that stores numbers as doubles rounds to a spacing of $256\,\mathrm{ns}$. Write the stamp as two integers, seconds and nanoseconds, or as nanoseconds since the run start ($\le6.0\times10^{10}$), or as a string.
> 5. The byte order, the fields' order and widths, and whether the records are packed or aligned — the layout of §7. Guess aligned 24-byte records for a packed 20-byte file and the $240{,}000$ bytes, which happen to divide by $24$, become $10{,}000$ records of nonsense, the first command $-8.6\times10^{168}\,\mathrm{N}$, with no error.
> 6. Recording appends whole messages in time order, which MCAP frames one record at a time at $31$ bytes of framing each, readable from the front even without its index; training reads a few columns of many episodes, which a columnar file serves without touching the rest — the commands alone are $96{,}000$ of $240{,}000$ bytes for run 042.
> 7. CommonMark's right-flanking rule: the closing `**` follows `)`, a punctuation character, and precedes `이`, which is neither whitespace nor punctuation, so it cannot close the bold. Put the gloss outside, `**용어**(term)이`.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and [[02-foundations/lab-plants|0.6 Lab Plants]]. The object is P6's run 042; every problem changes a knob — the clock's type, a fourth column, a hand-edited config, the batch of a bag — so none of the page's numbers can be copied.

1. **Draw.** The picture for problem 3's variant log: tick 2407 with its time as int64 nanoseconds since the run start and the vision goal $g$ as a fourth float64 column, drawn as the packed struct `'<qidd'`, the aligned record, one `repr` CSV line and one JSON object, to one scale of $7$ px a byte, each labelled with its bytes and the whole run's rate per hour from problem 3.
2. **Derive.** (a) For the variant record (`t_ns` int64, `counts` int32, `u` float64, `g` float64), compute the packed and the aligned offsets and sizes with §7's formula; write tick 2407's CSV line — $t_{\text{ns}}=12{,}035{,}120{,}562$, $1042$ counts, the command above, $g=0.499$ — and count its bytes and those of its JSON object; and give the packed record's megabytes per hour. (b) Why is a stamp in integer nanoseconds since the run start exact for every JSON reader while one since 1970 is not? Compare both largest values with $2^{53}-1$. In which year will a float64 "seconds since 1970" column lose its $0.238\,\mu\mathrm{s}$ spacing, and what does it become? (c) For run 042's float64 time printed with $d$ decimals, find by §2's bound the smallest $d$ that keeps every stamp within $1\%$ of the period, and check it against §10's sweep. (d) A hand-edited parameter file holds `kd: 4e1`, `motion_axis: Y`, `device_id: 0755`, `start: 9:30` and `enable: "on"`, declared as a double, a string, an integer, a string and a boolean. Resolve each under the YAML 1.2 core schema, PyYAML and rcl, and say which fail when the node starts, which fail under `ros2 param load`, and which load silently wrong. (e) A recorder logs run 042 at $50$ samples per MCAP message: how many megabytes an hour, and what share of them is framing?
3. **Do.** Fill the `?` blanks and run the template after §10's lab: run 042 logged with an integer clock and the goal as a fourth column. Report the bytes a sample of the struct, the aligned record, the `repr` CSV and the JSON objects; their megabytes an hour; whether the largest stamp is exact for a binary64 JSON reader; and, for `%.3f`, `%.6f`, `%.17g` and `repr`, the bytes a sample, whether the time is exact and the worst errors of $u$ and $g$. Compare each with §10.

```python
# Problem 3 (Do). Run 042 logged with an integer clock and the goal as a fourth column. Run section 10 first; fill ?.
rel = t_ns - ?                                              # int64 ns since the run start
cols4 = (rel.tolist(), counts.tolist(), u.tolist(), goal.tolist())
fmt4 = ?                                                    # struct: little-endian int64, int32, float64, float64
raw4 = b"".join(struct.pack(fmt4, *s) for s in zip(*cols4))
aligned4 = np.dtype([("t_ns", "<i8"), ("counts", "<i4"), ("u", "<f8"), ("g", "<f8")], align=?)

def csv4(fmt):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["t_ns", "counts", "u_N", "g_m"])
    w.writerows([a, b, fmt(c), fmt(e)] for a, b, c, e in zip(*cols4))   # the two integers are written as they are
    return buf.getvalue().encode()

js4 = json.dumps([{"t_ns": a, "counts": b, "u": c, "g": e} for a, b, c, e in zip(*cols4)]).encode()
print("bytes a sample: struct %.2f, aligned itemsize %d, CSV repr %.2f, JSON object %.2f"
      % (len(raw4) / N, aligned4.itemsize, len(csv4(repr)) / N, len(js4) / N))
print("MB an hour: struct %.2f, CSV repr %.2f, JSON %.2f"
      % tuple(n / N * F * 3600 / 1e6 for n in (len(raw4), len(csv4(repr)), len(js4))))
print("largest stamp %d ns; exact for a binary64 JSON reader: %s" % (rel.max(), rel.max() <= ?))
for name, fmt in (("%.3f", "%.3f".__mod__), ("%.6f", "%.6f".__mod__), ("%.17g", "%.17g".__mod__), ("repr", repr)):
    rows = list(csv.reader(io.StringIO(csv4(fmt).decode())))[1:]
    t_back = np.array([int(r[0]) for r in rows])
    u_back, g_back = (np.array([float(r[j]) for r in rows]) for j in (2, 3))
    print("%-6s %.2f bytes a sample  t exact %s  worst |du| %.3e N  worst |dg| %.3e m  g exact %s"
          % (name, ?, np.array_equal(t_back, rel), ?, ?, ?))
```

> [!note]- How to draw it · 그리는 법
> - Use one scale for every bar — here $7$ px a byte — and put a byte ruler under them; bars of different formats are only comparable when a byte has one length.
> - Split a binary bar into its fields at their offsets, and draw padding as its own dashed segment where a narrow field precedes a wider one: in the variant, the $4$ bytes after `counts`.
> - Write a text bar's actual characters inside it, one character per byte, the newline and the separator between JSON objects included; count them rather than estimating.
> - Label each bar with two numbers that must not be confused: this sample's bytes, and the whole run's average rate per hour, since text lengths vary from sample to sample.
> - Mark which bars read back exactly. In the variant every integer does at any format; the floats do only with `repr` or `%.17g`.

> [!tip]- Solutions
> 1. Four bars at $7$ px a byte. Packed `'<qidd'`: $28$ bytes, `t_ns` $8$, `counts` $4$, `u` $8$, `g` $8$ at offsets $0, 8, 12, 20$, $20.16\,\mathrm{MB/h}$. Aligned: $32$ bytes, $4$ bytes of padding after `counts` so that `u` starts at $16$ and `g` at $24$, $23.04\,\mathrm{MB/h}$. CSV: `12035120562,1042,-1.9578125000000002,0.499` and a newline, $43$ bytes; the run averages $47.76$ bytes a sample, $34.38\,\mathrm{MB/h}$. JSON: `{"t_ns": 12035120562, "counts": 1042, "u": -1.9578125000000002, "g": 0.499}`, $75$ characters and $2$ of separator, $77$ bytes; the run averages $81.75$, $58.86\,\mathrm{MB/h}$. Only the text bars vary with the values; all four read back exactly.
> 2. (a) Packed: $o=0, 8, 12, 20$, $S=28$. Aligned with $a=8, 4, 8, 8$: $o_2=\lceil 8/4\rceil 4=8$, $o_3=\lceil 12/8\rceil 8=16$, $o_4=\lceil 24/8\rceil 8=24$, $S=\lceil 32/8\rceil 8=32$. The CSV line is $11+1+4+1+19+1+5+1=43$ bytes and the JSON object $75$, $77$ with its separator. Packed per hour: $28\times720{,}000=20{,}160{,}000$ bytes, $20.16\,\mathrm{MB}$. (b) The largest stamp since the start is $59{,}995{,}152{,}978\approx6.0\times10^{10}$, about $150{,}000$ times below $2^{53}-1=9{,}007{,}199{,}254{,}740{,}991$, so every double holds it exactly; since 1970 the stamps are $1.79\times10^{18}$, about $199$ times above it, where doubles are $256\,\mathrm{ns}$ apart. The float64 spacing of seconds since 1970 is $2^{-22}\,\mathrm{s}$ for every date from $2^{30}\,\mathrm{s}$ (10 January 2004) to $2^{31}\,\mathrm{s}$, which is 19 January 2038, 03:14:08 UTC; from then on it is $2^{-21}\,\mathrm{s}=0.477\,\mu\mathrm{s}$. (c) One percent of $5\,\mathrm{ms}$ is $50\,\mu\mathrm{s}$. The bound $\tfrac12 10^{-d}+\tfrac12\,2^{-22}\,\mathrm{s}$ is $50.12\,\mu\mathrm{s}$ at $d=4$, just over, and $5.12\,\mu\mathrm{s}$ at $d=5$, so $d=5$. §10 agrees: at $d=4$ the worst error is $50.07\,\mu\mathrm{s}$, $1.0014\%$ of the period — the float grid's $0.12\,\mu\mathrm{s}$ is what tips it — and at $d=5$ it is $5.007\,\mu\mathrm{s}$. (d) `4e1`: core float $40.0$, PyYAML the string `'4e1'`, rcl float $40.0$. `Y`: string, string, rcl the boolean true. `0755`: core int $755$, PyYAML and rcl int $493$ (octal). `9:30`: string, PyYAML int $570$ (base 60), rcl string. `"on"`: quoted, a string in all three. At start-up (rcl) `motion_axis` fails as a boolean for a string parameter and `enable` fails as a string for a boolean one; `device_id` loads silently as $493$. Under `ros2 param load`, which parses with PyYAML twice (§4), `kd` fails as a string, `start` fails as the integer $570$ and `device_id` is again $493$; `enable` is the surprise — the first parse removes its quotes, the second reads `on` as the boolean true, and it loads. (e) $720{,}000/50=14{,}400$ messages, $14{,}400\times31=446{,}400$ bytes of framing on $14{,}400{,}000$ of payload: $14{,}846{,}400$ bytes, $14.85\,\mathrm{MB/h}$, $3.01\%$ framing.
> 3. Blanks: `T0 * 10 ** 9`, `"<qidd"`, `True`, `2 ** 53 - 1`, `len(csv4(fmt)) / N`, `np.abs(u_back - u).max()`, `np.abs(g_back - goal).max()` and `np.array_equal(g_back, goal)`. The output:
>
>    ```text
>    bytes a sample: struct 28.00, aligned itemsize 32, CSV repr 47.76, JSON object 81.75
>    MB an hour: struct 20.16, CSV repr 34.38, JSON 58.86
>    largest stamp 59995152978 ns; exact for a binary64 JSON reader: True
>    %.3f   28.54 bytes a sample  t exact True  worst |du| 5.000e-04 N  worst |dg| 1.110e-16 m  g exact False
>    %.6f   34.54 bytes a sample  t exact True  worst |du| 5.000e-07 N  worst |dg| 1.110e-16 m  g exact False
>    %.17g  54.13 bytes a sample  t exact True  worst |du| 0.000e+00 N  worst |dg| 0.000e+00 m  g exact True
>    repr   47.76 bytes a sample  t exact True  worst |du| 0.000e+00 N  worst |dg| 0.000e+00 m  g exact True
>    ```
>
>    The integer clock costs the same $8$ bytes as the float64 time in binary and is exact in every format, and in text it is shorter: $11$ digits against $18$ characters, so the variant's `repr` CSV is only $5.7$ bytes a sample longer than §10's although it carries a fourth column. The goal looks like a three-decimal number — $0.1$ plus multiples of $0.001$ — yet `%.3f` does not return it exactly: some goals are floats such as $0.30000000000000004$, one spacing off the decimal, and the worst error is $1.11\times10^{-16}\,\mathrm{m}$. `%.17g` is exact but costs $54.13$ bytes against `repr`'s $47.76$, since it writes about half of the goals at full length — $0.1$ becomes `0.10000000000000001` (tick 2407's $0.499$ happens to come out as `0.499`); `repr` is exact and shortest. The JSON objects grow to $81.75$ bytes, $2.92\times$ the struct, against $3.35\times$ in §10.

### Sources

- RFC 8259, *The JSON Data Interchange Format*, 2017 ([rfc-editor.org/rfc/rfc8259](https://www.rfc-editor.org/rfc/rfc8259)) — the six value types, numbers without NaN or leading zeros, unique names, UTF-8, the interoperable integers up to $2^{53}-1$.
- RFC 4180, *Common Format and MIME Type for CSV Files*, Informational, 2005 ([rfc-editor.org/rfc/rfc4180](https://www.rfc-editor.org/rfc/rfc4180)) — CRLF records, the optional header, quoting and doubled quotes.
- *YAML 1.2.2*, 2021 ([yaml.org/spec/1.2.2](https://yaml.org/spec/1.2.2/)) and the YAML 1.1 type repository ([yaml.org/type](https://yaml.org/type/index.html)) — comments, no tabs in indentation, the core and JSON schemas; 1.1's bool, int and float.
- PyYAML ([pyyaml.org/wiki/PyYAML](https://pyyaml.org/wiki/PyYAML)) and its [`resolver.py`](https://github.com/yaml/pyyaml/blob/main/lib/yaml/resolver.py) — "a complete YAML 1.1 parser" and its implicit resolvers; version 6.0.1 was used only to check §4's table.
- ROS 2 sources, Jazzy branches: rcl's [`parse.c`](https://github.com/ros2/rcl/blob/jazzy/rcl_yaml_param_parser/src/parse.c) (`get_value()`), rclpy's [`parameter.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/parameter.py) (`get_parameter_value`, `parameter_dict_from_yaml_file` and its `str()` re-parse), ros2cli's `ros2param` and launch_ros's [`node.py`](https://github.com/ros2/launch_ros/blob/jazzy/launch_ros/launch_ros/actions/node.py) — the two readers of §4.
- ROS 2 documentation, Jazzy branch ([ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — parameter files keyed by node name over `ros__parameters`; the Iron Irwini release notes (MCAP the default bag format, May 2023).
- Python 3 documentation ([docs.python.org](https://docs.python.org/3/)) — `json`, `csv`, `struct`, `xml.etree.ElementTree`, the floating-point tutorial and "What's New in Python 3.2"; CPython's [`Lib/json/encoder.py`](https://github.com/python/cpython/blob/3.12/Lib/json/encoder.py) (`float.__repr__`).
- NumPy documentation ([numpy.org/doc](https://numpy.org/doc/stable/)) — `numpy.lib.format` (the `.npy` header), `numpy.load` (`allow_pickle`), `numpy.savez_compressed`, `numpy.savetxt` (`'%.18e'`) and structured arrays (`align=True`).
- W3C, *Extensible Markup Language (XML) 1.0*, fifth edition, 2008 ([w3.org/TR/xml](https://www.w3.org/TR/xml/)) — one root element, escaping, comments, unique quoted attributes.
- The HDF Group, *HDF5 documentation* ([support.hdfgroup.org](https://support.hdfgroup.org/documentation/hdf5/latest/_learn_basics.html)) — groups, datasets, attributes; contiguous and chunked storage.
- robomimic documentation ([robomimic.github.io/docs](https://robomimic.github.io/docs/datasets/overview.html)) — the HDF5 dataset structure; JSON configs passed with `--config`.
- Apache Parquet documentation ([parquet.apache.org/docs](https://parquet.apache.org/docs/overview/)) and [`parquet.thrift`](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift) — row groups, column chunks and pages; `PAR1` and the footer metadata.
- LeRobot ([github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)) — `docs/source/lerobot-dataset-v3.mdx` and `src/lerobot/datasets/utils.py`: the v3 layout, 100 MB data files, the legacy `meta/episodes.jsonl`.
- MCAP specification ([mcap.dev/spec](https://mcap.dev/spec)) — magic bytes, record framing, Schema, Channel and Message records, chunks and the optional summary.
- *CommonMark Spec* 0.31.2, 2024 ([spec.commonmark.org/0.31.2](https://spec.commonmark.org/0.31.2/)) and *GitHub Flavored Markdown Spec* 0.29-gfm ([github.github.com/gfm](https://github.github.com/gfm/)) — setext headings, right-flanking delimiter runs, tables.
- Hydra documentation ([hydra.cc/docs](https://hydra.cc/docs/intro/)) — composition, command-line overrides, `.hydra/config.yaml` per run.
- This wiki's `quartz.config.yaml` — the GFM, Obsidian-flavored and KaTeX plugins.

## 한국어

*[[02-foundations/signal-processing|6. 신호처리 §2]] 위에 선다. 소수 몇 자리까지 찍은 숫자는 그 페이지의 양자화기 그 자체다. 장치 **P6**(레일 위 카트와 그 시계들, [[02-foundations/lab-plants|0.6]])를 다시 쓰는 페이지이기도 하다. ROS 2 트랙은 P6를 노드와 토픽으로 돌리고([[04-robotics/ros2/nodes-topics-messages|25.2]]), 파라미터 파일을 붙인 launch 파일로 띄우고([[04-robotics/ros2/workspaces-packages-launch|25.4]]), bag에 기록한다([[04-robotics/ros2/debugging-data-reproducibility|25.10]]). 이 페이지는 그 페이지들이 쓰고 읽는 파일을 열어 본다.*

> [!note] 왜 배우는가 · Why this matters
> 형식은 [[07-research-program/index|7 §5]]의 물리 AI 스택 아래에 깔린 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 모든 층은 자기 데이터를 바이트로 다음 층에 넘기고 — 제어기로 들어가는 파라미터 파일, 로봇에서 나오는 bag, 학습 층으로 들어가는 데이터셋 — "그 패널을 프레임에 설치해"에서는 끼워 맞추기 단계의 시연과 완료를 확인하는 로그를 나른다. 형식을 잘못 고르면 실행은 오류 하나 없이 망가진다. `%.3f`로 찍은 시간 열은 지연 분석이 재는 바로 그 지터를 지우고, float32 시각은 P6 샘플 1분을 한 순간으로 뭉개며, 손으로 고친 `device_id: 0123`은 노드를 83으로 띄운다. 이 지식이 처음 필요해지는 것은 학위논문 경로([[07-research-program/index|7 §8]])의 2블록, ROS 2 트랙이 파라미터 파일을 읽고 bag을 기록할 때이고([[04-robotics/ros2/services-actions-parameters|25.3 §7]], [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), 다시 필요해지는 것은 7블록에서 [[05-construction-robotics/imitating-contact|10. 접촉 모방 §2]]이 S1(건설 트랙의 외장 패널 과제, [[05-construction-robotics/site-engineering|2.5]])의 안착 시연으로 학습할 때다. 이 페이지를 마치면 설정, 로그, 데이터셋의 형식을 그것이 약속하는 것으로 고르고, 그 선택을 바이트와 왕복 오차로 증명할 수 있다.

> [!note] 처음이라면 · First pass
> 90분 안팎으로 두 번 앉으면 된다. **첫 번째 — 바이트가 된 숫자.** 그림을 보고 계산 절을 손으로 따라간다. P6 실행의 샘플 하나를 이진, CSV, JSON으로 적었을 때 샘플당·시간당 몇 바이트인지, 그리고 소수 셋째 자리와 일곱째 자리까지 찍은 시간을 다시 읽으면 무엇이 돌아오는지다. §1과 §2를 읽고 스스로 점검 1, 2에 답한다. **두 번째 — 고치고 기록하게 될 형식.** 설정 파일을 고치기 전에 §3과 §4를, 로그나 데이터셋 형식을 고르기 전에 §6–§8을 읽고, §10의 실습을 돌린 뒤 스스로 점검 3–6에 답한다. §5와 §9는 URDF나 Markdown 표를 고치는 날까지 미뤄도 되고, *더 깊이* 콜아웃은 처음 읽을 때 모두 건너뛰어도 된다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**를 1분 동안 한 번 돌린다. 카탈로그가 고정하는 것은 카트, 엔코더($2048$ counts/m), 두 주기다. 로그에는 그보다 많은 것 — 시계, 목표, 제어기, 명령 — 이 들어가므로, 이 페이지가 실행 하나를 통째로 고정한다. 아래 숫자는 모두 이 페이지의 교과용 숫자이고, §10의 코드가 실행을 비트 하나까지 똑같이 다시 만들도록 골랐다. 측정값은 하나도 없다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $D$, $f$, $T$ | $60\,\mathrm{s}$, $200\,\mathrm{Hz}$, $5\,\mathrm{ms}$ | 실행 길이, P6의 제어 주파수와 주기 |
| $n$ | $fD=12{,}000$ | 샘플 수. 제어 틱 $k=0,\dots,11{,}999$마다 하나 |
| $t_0$ | $1{,}790{,}000{,}000\,\mathrm{s}$ | 실행 시작. 1970-01-01 UTC부터 센 초로, 2026년 9월 21일 14:13:20 UTC |
| $\ell_k$ | $(123{,}607\,k)\bmod 200{,}001\ \mathrm{ns}$ | 틱 $k$의 시각이 늦게 찍힌 정도, $0$–$200\,\mu\mathrm{s}$. 스케줄링 지터 대신 쓰는 결정론적 값 |
| $t_k$ | $t_0+(5{,}000{,}000\,k+\ell_k)\times10^{-9}\,\mathrm{s}$ | 시간 열. float64, 8바이트 |
| $c_k$ | int32, 4바이트 | 엔코더 카운트, 미터당 $2048$(P6) |
| $u_k$ | float64, 8바이트 | 뉴턴 단위의 모터 명령. 카운트에 건 PD 법칙 |
| $m$ | $2\,\mathrm{kg}$ | 카트 질량. 실행을 만들 때만 쓴다. P6는 이 값을 정하지 않는다 |
| $k_p$, $k_d$ | $200\,\mathrm{N/m}$, $40\,\mathrm{N\,s/m}$ | 제어기 이득. $m$과 함께 루프를 임계 감쇠로 만든다($k_d/(2\sqrt{k_pm})=1$) |
| $g$ | $0.1\to0.6\to0.1\,\mathrm{m}$, $20\,\mathrm{s}$마다 | 비전 목표. 삼각파이고 넷째 틱마다($50\,\mathrm{Hz}$) 새로 온다 |

제어기는 틱마다 다음을 계산한다.

$$u_k=k_p\Big(g-\frac{c_k}{2048}\Big)-k_d\,\frac{(c_k-c_{k-1})\,f}{2048}$$

속도 추정이 한 주기의 카운트 차이 하나이므로 $200\,\mathrm{Hz}$에서 카운트 하나가 $0.0977\,\mathrm{m/s}$이고([[04-robotics/ros2/nodes-topics-messages|25.2]]의 계산 절), 그래서 기록된 명령은 틱마다 $k_d\times0.0977=3.9\,\mathrm{N}$씩 떨린다. 카트는 $0.1\,\mathrm{m}$에 정지한 상태로 시작해 [[02-foundations/lab-kernel|0.7 §3]]의 반암시적 오일러로 전진한다. 로그의 레코드 하나는 세 값 $(t_k,c_k,u_k)$다.

실행의 설정은 제어기를 띄울 때 넘길 파라미터 파일이고, 그 구조는 [[04-robotics/ros2/services-actions-parameters|25.3 §7]]이 정의한 그대로다. 파일 자체는 영어 절에 있다. 최상위 키 `/cart/controller` 아래 글자 그대로의 키 `ros__parameters`가 오고, 그 아래에 `counts_per_metre: 2048`, `control_period: 0.005`, `kp: 200.0`, `kd: 40.0`, 그리고 상대 이름 `goal_topic: goal`과 `cmd_topic: cmd`가 단위와 해석을 적은 주석과 함께 놓인다. §3이 실행의 JSON 사이드카를 더하고, §10이 레코드 $12{,}000$개를 모두 만든다.

*범위: 로봇 학습 연구자가 매주 읽고 쓰는 형식 — 텍스트로는 JSON, YAML, XML, CSV, Markdown, 이진으로는 NumPy의 `.npy`, HDF5, Parquet, MCAP — 을 각각이 무엇을 약속하는지, 바이트로 얼마를 치르는지, 왕복에서 무엇을 잃는지, 어떤 함정이 며칠을 잡아먹는지의 수준에서 가르친다. 이 파일들을 둘러싼 ROS 2 장치, 코덱, 데이터베이스, 압축은 §11이 이름을 대는 페이지들의 몫이다. HDF5와 Parquet은 문서에 근거해서만 설명하고, 실습은 NumPy와 Python 표준 라이브러리만 쓴다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 330" style="max-width:100%;height:auto" role="img" aria-label="한 척도(1바이트 = 7픽셀)로 그린 가로 막대 여섯 개. 각각 P6 실행의 2407번째 샘플을 담는다. t, counts, u로 나뉜 20바이트짜리 packed 이진 레코드와 그 16진 바이트, 패딩 4바이트가 든 24바이트짜리 정렬 레코드, 전체 정밀도의 CSV 줄 44바이트, 소수 셋째 자리까지의 CSV 줄 27바이트, JSON 객체 하나 69바이트, np.savetxt 기본값 줄 76바이트. 각 라벨에 실행 전체의 시간당 크기가 14.40에서 54.36 MB까지 적혀 있다.">
  <text x="12" y="18" font-size="12" fill="currentColor" fill-opacity="0.85">P6 실행의 2407번째 틱, 바이트 단위로 (7 px = 1바이트)</text>
  <text x="12" y="40" font-size="11" fill="currentColor" fill-opacity="0.85">이진, struct '&lt;did': 20 B · 실행 전체 14.40 MB/h</text>
  <rect x="12" y="46" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="40.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">t · f8</text>
  <rect x="68" y="46" width="28" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="82.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">i4</text>
  <rect x="96" y="46" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="124.0" y="59" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">u · f8</text>
  <text x="162" y="59" font-size="10" fill="currentColor" fill-opacity="0.8" font-family="ui-monospace,monospace">6a3f02e34eacda41 12040000 343333333353ffbf</text>
  <text x="12" y="86" font-size="11" fill="currentColor" fill-opacity="0.85">이진, 정렬(align=True): 24 B · 실행 전체 17.28 MB/h</text>
  <rect x="12" y="92" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="40.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">t · f8</text>
  <rect x="68" y="92" width="28" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="82.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">i4</text>
  <rect x="96" y="92" width="28" height="18" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2"/>
  <text x="110.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">패딩</text>
  <rect x="124" y="92" width="56" height="18" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="152.0" y="105" font-size="10" text-anchor="middle" fill="currentColor" font-family="ui-monospace,monospace">u · f8</text>
  <text x="190" y="105" font-size="10" fill="currentColor" fill-opacity="0.8">패딩 4바이트가 u를 8바이트 경계에 놓는다</text>
  <text x="12" y="132" font-size="11" fill="currentColor" fill-opacity="0.85">CSV, repr: 44 B · 실행 전체 샘플당 42.03 B, 30.26 MB/h</text>
  <rect x="12" y="138" width="308" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="153" x2="82" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="153" x2="152" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="153" x2="222" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="153" x2="292" y2="156" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="151" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="306" lengthAdjust="spacing">1790000012.0351205,1042,-1.9578125000000002↵</text>
  <text x="12" y="178" font-size="11" fill="currentColor" fill-opacity="0.85">CSV, %.3f: 27 B · 18.52 MB/h · t가 120.4 µs 이르게 읽힌다</text>
  <rect x="12" y="184" width="189" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="199" x2="82" y2="202" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="199" x2="152" y2="202" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="197" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="187" lengthAdjust="spacing">1790000012.035,1042,-1.958↵</text>
  <text x="12" y="224" font-size="11" fill="currentColor" fill-opacity="0.85">JSON, 샘플마다 객체 하나: 69 B · 실행 전체 48.26 MB/h</text>
  <rect x="12" y="230" width="483" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="245" x2="82" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="245" x2="152" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="245" x2="222" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="245" x2="292" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="362" y1="245" x2="362" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="432" y1="245" x2="432" y2="248" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="243" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="481" lengthAdjust="spacing">{"t": 1790000012.0351205, "counts": 1042, "u": -1.9578125000000002}, </text>
  <text x="12" y="270" font-size="11" fill="currentColor" fill-opacity="0.85">np.savetxt 기본 '%.18e': 76 B · 54.36 MB/h</text>
  <rect x="12" y="276" width="532" height="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <line x1="82" y1="291" x2="82" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="152" y1="291" x2="152" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="222" y1="291" x2="222" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="292" y1="291" x2="292" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="362" y1="291" x2="362" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="432" y1="291" x2="432" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <line x1="502" y1="291" x2="502" y2="294" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.35"/>
  <text x="13" y="289" font-size="10" fill="currentColor" font-family="ui-monospace,monospace" textLength="530" lengthAdjust="spacing">1.790000012035120487e+09,1.042000000000000000e+03,-1.957812500000000178e+00↵</text>
  <line x1="12" y1="312" x2="544" y2="312" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="12" y1="312" x2="12" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="12" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">0</text>
  <line x1="82" y1="312" x2="82" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="82" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">10</text>
  <line x1="152" y1="312" x2="152" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="152" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">20</text>
  <line x1="222" y1="312" x2="222" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="222" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">30</text>
  <line x1="292" y1="312" x2="292" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="292" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">40</text>
  <line x1="362" y1="312" x2="362" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="362" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">50</text>
  <line x1="432" y1="312" x2="432" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="432" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">60</text>
  <line x1="502" y1="312" x2="502" y2="316" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="502" y="327" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">70</text>
  <text x="514" y="308" font-size="10" fill="currentColor" fill-opacity="0.8">바이트</text>
</svg>

실행의 2407번째 틱 — 시각 $1{,}790{,}000{,}012.0351205\,\mathrm{s}$, $1042$ 카운트, $-1.9578125000000002\,\mathrm{N}$ — 을 각 파일이 치르는 바이트로, 바이트당 $7$ px라는 한 척도로 그렸다. packed 이진은 $20$, 정렬된 이진은 $24$, 전체 정밀도의 CSV는 $44$, 소수 셋째 자리 CSV는 $27$, JSON 객체는 $69$, `np.savetxt` 기본값은 $76$바이트다. 라벨의 시간당 크기는 §10에서 잰 실행 전체의 값으로 packed 레코드의 $14.40\,\mathrm{MB/h}$부터 `np.savetxt`의 $54.36\,\mathrm{MB/h}$까지이고, 정확히 되돌아오지 않는 것은 소수 셋째 자리 줄 하나뿐으로, 그 시간은 $120.4\,\mu\mathrm{s}$ 이르게 돌아온다.

### 대상으로 한 번 끝까지 · Worked case

대상은 레코드 하나와 그 레코드가 속한 한 시간이다. 과제는 레코드를 바꾼다 — 정수 시계와 넷째 열 — 그러니 이 판을 먼저 손으로 풀어 둔다. 미리 알아 둘 것 넷을 한 줄씩 적고, 유도는 뒤에서 한다. Python이 float를 찍는 기본 방식인 `repr`는 같은 float로 되돌아오는 가장 짧은 소수를 쓴다(§2). 텍스트 형식은 찍힌 값의 글자 하나에 1바이트를 쓰고, 구분자와 줄 끝도 센다(§1). 숫자를 소수 $d$째 자리까지 찍으면 $10^{-d}$의 배수로 반올림되므로, 다시 읽은 값은 많아야 그 계단의 절반에, 파싱하면서 가장 가까운 float로 맞춰지는 몫인 float 간격의 절반을 더한 만큼 어긋난다(§2). $t_0$ 근처에서 float64는 $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$ 간격이고, float32는 $128\,\mathrm{s}$ 간격이다(§2).

**1단계 — 메모리 속의 레코드.** 틱 $k=2407$은 실행 $12.035\,\mathrm{s}$ 지점에 있고, 시각이 $\ell_{2407}=120{,}562\,\mathrm{ns}$ 늦게 찍혔다.

| 필드 | Python이 찍는 모양(`repr`) | 타입 | 바이트 |
|---|---|---|---:|
| $t$ | `1790000012.0351205` | float64 | 8 |
| $c$ | `1042` | int32 | 4 |
| $u$ | `-1.9578125000000002` | float64 | 8 |

카운트는 $1042/2048=0.5087890625\,\mathrm{m}$다. 명령의 실수 값은 $200\,(0.499-0.5087890625)=-1.9578125\,\mathrm{N}$이다. 목표가 $0.499\,\mathrm{m}$였고 카운트는 직전 틱과 같았기 때문이다. 그런데 $0.499$는 이진으로 정확히 적히지 않으므로 float의 마지막 비트에 꼬리가 붙고, 그 float를 이름으로 부르려면 `repr`에 유효 숫자 17개가 필요하다.

**2단계 — 이진.** 이진 레코드는 필드 폭의 합이고, $200\,\mathrm{Hz}$에서 한 시간은 레코드 $720{,}000$개다.

$$B_{\text{bin}}=8+4+8=20\ \text{bytes},\qquad 20\times720\,000=14{,}400\,000\ \text{bytes}=14.4\ \text{MB/h}$$

이진 필드는 값이 무엇이든 그 값 자신의 바이트를 담기 때문이다. $1042$도 $-1.9578125000000002$도 $0$과 같은 값을 치른다.

**3단계 — 전체 정밀도의 CSV.** 줄은 `1790000012.0351205,1042,-1.9578125000000002`와 줄바꿈 하나다.

$$B_{\text{csv}}=18+1+4+1+19+1=44\ \text{bytes}=2.2\,B_{\text{bin}}$$

글자 하나가 1바이트이기 때문이다. 실행 전체로는 줄 하나가 평균 $42.03$바이트, $30.26\,\mathrm{MB/h}$이고(§10), 모든 값을 `repr`로 찍었으므로 잃는 것은 없다.

**4단계 — 샘플마다 JSON 객체 하나.** `{"t": 1790000012.0351205, "counts": 1042, "u": -1.9578125000000002}`는 $67$자이고, 리스트는 객체 사이를 쉼표와 공백으로 가르므로 레코드 하나가 $69$바이트, 이진의 $3.45$배다. $67$자 중 $26$자가 이름, 따옴표, 콜론, 쉼표, 공백이고, 한 시간의 레코드 $720{,}000$개마다 다시 적힌다. 실행 전체의 평균은 레코드당 $67.03$바이트, $48.26\,\mathrm{MB/h}$다(§10).

**5단계 — 소수 셋째 자리.** 두 float에 `%.3f`를 쓰면 `1790000012.035,1042,-1.958`, $27$바이트로 이진의 $1.35$배에 그친다. 그러나 시간은 $1{,}790{,}000{,}012.035$에 가장 가까운 float로 돌아오고, 그것은 $t$보다 $120.4\,\mu\mathrm{s}$ 아래다. 한계 안에는 여유 있게 들어간다.

$$|\hat t-t|=120.4\ \mu\text{s}\ \le\ \tfrac12\,10^{-3}\ \text{s}+\tfrac12\,2^{-22}\ \text{s}=500.12\ \mu\text{s}$$

그러니 이 오차는 허용 범위 안이다. 그리고 동시에 잃으면 안 되는 바로 그것이기도 하다. 틱의 명목 시각은 모두 밀리초의 정수배라서 세 자리는 정확히 그것만 남기고, 이 틱이 늦게 돈 $120.562\,\mu\mathrm{s}$ — 지연 분석이 재는 바로 그 양([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]) — 는 사라진다. 실행 전체에서 가장 크게 잃는 것은 $200\,\mu\mathrm{s}$로, 가장 늦게 찍힌 틱의 지연이다(§10). 명령은 $-1.958$로 돌아와 $0.19\,\mathrm{mN}$ 어긋난다.

**6단계 — 몇 자리면 충분한가.** 찍는 계단이 float 간격보다 촘촘해지면 다시 읽기가 정확해진다.

$$10^{-7}\ \text{s}=0.1\ \mu\text{s}\ <\ 2^{-22}\ \text{s}=0.238\ \mu\text{s}\quad\Rightarrow\quad d=7$$

그러면 찍힌 소수가 $t$에서 float 간격의 절반 안에 놓이고, 가장 가까운 float로 반올림하는 파서가 $t$ 자신에 떨어지기 때문이다. 소수점 앞 열 자리와 뒤 일곱 자리는 유효 숫자 $17$개로, 여기서 `repr(t)`의 길이와 같다. 여섯 자리에서는 시간이 아직 최대 $0.48\,\mu\mathrm{s}$ 어긋난다(§10).

**7단계 — 열의 타입.** 시간을 float32로 저장하면 유효 비트가 $24$개뿐이고, $t_0$ 근처에서 float32는 $2^{30-23}=128\,\mathrm{s}$ 간격이다. $t_0=128\times13{,}984{,}375$는 그중 하나이고, 실행의 모든 시각은 그보다 $60\,\mathrm{s}$ 미만 뒤에 있으므로, 각 시각을 가장 가까운 float32로 반올림하면 — $\operatorname{fl}_{32}$로 적는다 — $t_0$ 자신이 된다.

$$\operatorname{fl}_{32}(t_k)=t_0\quad\text{for every }k,\qquad\text{since}\quad t_k-t_0<60\ \text{s}<\tfrac12\times128\ \text{s}$$

그래서 시각 $12{,}000$개가 값 하나로 무너지고(§10은 서로 다른 시각을 $1$개로 센다), 틱 2407은 $12.035\,\mathrm{s}$ 이르게 돌아온다. 실행 시작부터 센 초는 float32에서도 $2.02\,\mu\mathrm{s}$ 안으로 맞고, 정수 나노초는 int64에 정확히 맞는다. 이것이 과제의 변형이다.

| 파일 | 틱 2407의 바이트 | 이진 대비 | 실행 평균, 샘플당 바이트 | 시간당 MB | 정확히 되돌아오는가 |
|---|---:|---:|---:|---:|---|
| 이진 레코드 | 20 | 1.00 | 20.00 | 14.40 | 예 |
| CSV, `repr` | 44 | 2.20 | 42.03 | 30.26 | 예 |
| JSON, 샘플마다 객체 | 69 | 3.45 | 67.03 | 48.26 | 예 |
| CSV, `%.3f` | 27 | 1.35 | 25.73 | 18.52 | 아니오: $t$가 $-120.4\,\mu\mathrm{s}$, $u$가 $-0.19\,\mathrm{mN}$ |

### 1. 형식이 약속하는 것: 텍스트냐 이진이냐

*한 문장으로:* 파일은 바이트밖에 갖지 못한 독자가 쓴 사람의 뜻을 되찾게 해 주어야 하고, 형식은 그것을 가능하게 하는 바이트에 관한 계약이며, 타입·스키마·정밀도·주석·스트리밍이라는 다섯 약속이 그 형식이 어떤 일을 맡을 수 있는지를 정한다.

파일은 그것을 쓴 프로그램보다 오래 산다. 읽는 쪽은 다음 달 동료의 분석 스크립트일 수도, 기동하는 C++ 노드일 수도, 다른 언어로 된 학습 로더일 수도, 2년 뒤의 나일 수도 있는데, 그 독자가 가진 것은 바이트뿐이다. 쓴 사람이 뜻한 것을 되찾게 해 주는 것이 형식이고, 형식은 다섯 가지를 약속하거나 약속하지 못한다.

1. **타입.** `1042`는 정수로, `0.005`는 실수로, `true`는 불리언으로 돌아오는가, 아니면 독자가 짐작해야 할 글자로 돌아오는가? 이진 형식은 데이터 옆에 타입을 싣는다(`.npy` 헤더에는 리틀 엔디언 8바이트 실수라는 뜻의 `<f8`가 적혀 있다). CSV는 아무 타입도 싣지 않는다. JSON에는 여섯 가지가 있다. YAML은 철자로 타입을 짐작하고, 두 독자가 서로 다르게 짐작할 수 있다(§4).
2. **스키마.** 필드 이름, 단위, 뜻은 어디에 적혀 있는가? 파일 안(`.npy` 헤더, Parquet 꼬리말, MCAP의 스키마 레코드)인가, 파일 옆(JSON 사이드카, rosbag2의 `metadata.yaml`)인가, 누군가의 기억 속인가? `u`라는 열 이름은 뉴턴이라고 말해 주지 않는다.
3. **정밀도.** 숫자가 비트 하나까지 그대로 돌아오는가? 이진은 언제나 그렇다. 텍스트는 충분한 자릿수를 찍었을 때만 그렇다(§2).
4. **주석.** 사람이 파일에 메모를 달 수 있고, 그 메모가 파일을 읽었다 다시 쓰는 프로그램을 거쳐도 살아남는가? YAML과 XML에는 주석이 있고 JSON과 CSV에는 없다. 게다가 있는 주석도 파서가 버린다. YAML 명세는 주석을 데이터에 아무 영향이 없는 표현상의 세부라고 부르고, Python의 `xml.etree`는 파싱하면서 주석을 건너뛴다(§5).
5. **스트리밍.** 기록기가 샘플을 하나씩 덧붙일 수 있는가, 그리고 도중에 죽으면 읽을 수 있는 앞부분이 남는가? CSV 파일이나 줄마다 JSON 텍스트 하나인 파일은 줄 단위로 자란다. JSON 배열은 닫는 괄호가 있어야 하고, `.npy` 헤더는 배열의 shape을 적어 둔다. Parquet 파일은 메타데이터를 데이터 뒤, 맨 끝에 쓴다. MCAP 파일은 레코드마다 자기 길이를 붙인다(§8).

첫 갈림길은 텍스트냐 이진이냐다. **텍스트** 형식은 값을 글자로 찍고 독자가 그것을 다시 파싱한다. JSON이 시스템 사이에서 요구하는 UTF-8에서 ASCII 글자는 하나가 1바이트이므로, 값 하나는 찍힌 모양의 글자 수만큼 바이트를 치른다. **이진** 형식은 값 자신의 바이트를 저장한다. float64는 값이 무엇이든 8바이트, int32는 4바이트다. 그 대신 독자는 배치 — 필드의 순서, 폭, 바이트 순서 — 를 알아야 바이트가 뜻을 갖는다(§7). 텍스트는 어느 편집기로나 읽히고 Git에서 줄 단위로 diff된다는 장점을, 이진은 크기와 속도와 정확함을 가진다.

| 형식 | 텍스트/이진 | 타입 | 스키마가 사는 곳 | float가 정확한가 | 주석 | 샘플 덧붙이기 | 로봇 연구자가 만나는 곳 |
|---|---|---|---|---|---|---|---|
| JSON | 텍스트 | 여섯 가지(§3) | 없음, 사이드카 | `repr`로 쓰면 | 없음 | 줄마다 JSON 텍스트 하나로 | robomimic 설정, LeRobot의 `meta/info.json` |
| YAML | 텍스트 | 철자로(§4) | 없음 | 자릿수가 충분하면 | 있음 | — | ROS 2 파라미터 파일, Hydra 설정 |
| XML | 텍스트 | 없음, 모두 문자열(§5) | 선택적 스키마 | — | 있음 | — | URDF, `package.xml`, launch 파일 |
| CSV | 텍스트 | 없음(§6) | 기껏해야 헤더 줄 | 자릿수가 충분하면 | 없음 | 가능 | 간단한 로그, 스프레드시트 |
| Markdown | 텍스트 | — | front matter(§9) | — | 있음 | — | 노트, 이 위키 |
| `.npy`, `.npz` | 이진 | dtype(§7) | 헤더 | 예 | 없음 | 불가 | 배열, 결과 |
| HDF5 | 이진 | 데이터셋마다(§8) | 그룹, 속성 | 예 | — | 청크 저장이면 | robomimic 데이터셋 |
| Parquet | 이진 | 열마다(§8) | 꼬리말 | 예 | — | 불가 | LeRobot 데이터셋 |
| MCAP | 이진 | 스키마마다(§8) | 스키마 레코드 | 예 | — | 가능 | rosbag2 bag |

> **직렬화 형식의 정의.** **직렬화 형식**(serialization format)은 *쓰는 쪽과 읽는 쪽 사이의 바이트에 관한 계약*이다. 메모리 속 값이 바이트열이 되었다가 되돌아오는 방식을 정한 명세이고, 파일 확장자도 라이브러리도 아니다. 조건은 넷이다. **인코더**가 허용된 값을 바이트로 바꾼다. **디코더**가 그 바이트를 값으로 되돌린다. 양쪽이 따르는 **명세**가 있다 — 텍스트라면 문법, 이진이라면 폭과 바이트 순서의 배치다. 그리고 **정의역**, 곧 받아들이는 값의 집합이 있다. JSON에는 NaN이 없고, YAML의 plain 스칼라는 철자로 타입이 정해진다.
>
> $$B_{\text{bin}}=\sum_{i=1}^{m}w_i,\qquad B_{\text{text}}=\sum_{i=1}^{m}\ell_i+(m-1)+\lambda$$
>
> $m$은 레코드 하나의 필드 수, $w_i$는 필드 $i$의 이진 타입 폭(바이트), $\ell_i$는 찍힌 모양의 글자 수, $m-1$은 구분자, $\lambda$는 줄 끝 문자의 바이트다. 그래서 이진 레코드는 크기가 고정되고, 텍스트 레코드의 크기는 값마다 자릿수를 따라 움직인다.
>
> - **예**: 실행의 2407번째 틱. $B_{\text{bin}}=8+4+8=20$바이트이고, CSV 줄로는 $B_{\text{text}}=18+4+19+2+1=44$다.
> - **비예**: "CSV 파일". 구분자, 따옴표 규칙, 찍는 자릿수, 열마다의 뜻이 정해지기 전까지 "CSV"는 형식 하나가 아니라 형식의 집안 이름이고(§6), 두 프로그램이 둘 다 CSV를 읽으면서 같은 파일을 다르게 읽을 수 있다.
> - **왜 중요한가**: 뒤의 모든 절이 이 네 조건 중 하나가 깨지는 경우다 — 타입을 짐작하는 디코더(§4), NaN이 조용히 빠진 정의역(§3), 아무도 적지 않은 명세(§6), 틀린 바이트 순서로 읽힌 배치(§7).

나머지 절은 형식을 하나씩 다루지만, 무엇을 고를지는 일이 정한다. **설정**은 작고 사람이 쓰며 기동할 때 읽히므로 주석이 되는 텍스트다. ROS 2에서는 YAML, 학습 코드에서는 YAML이나 JSON이다. **로그**는 크고 샘플 단위로 쓰이므로 덧붙일 수 있는 이진이다. rosbag2를 통한 MCAP에, 바이트가 말하지 못하는 것을 적은 작은 JSON이나 YAML 사이드카를 곁들인다. **데이터셋**은 로더가 여러 번 읽으므로 그 로더가 가장 빨리 읽고 커뮤니티의 도구가 기대하는 형식이다. robomimic은 HDF5, LeRobot은 Parquet과 MP4다. 표 하나 분량의 **결과**는 `.npy`나 `repr`로 찍은 CSV면 된다.

### 2. 텍스트가 된 숫자: 소수 자릿수, 유효 숫자, 왕복

*한 문장으로:* 텍스트로 쓴 로그는 float가 담았던 것을 소리 없이 잃을 수 있는데, 찍은 float는 충분한 자릿수를 찍었을 때만 정확히 되돌아오고, 몇 자리가 충분한지는 숫자 중 몇 자리가 의미 있어 보이는지가 아니라 숫자의 크기가 정하기 때문이다.

float64는 유효 비트 53개짜리 이진 분수를 담는다. 대부분의 십진 분수 — $0.005$, $0.499$ — 는 이진으로 정확히 적히지 않으므로 float는 가장 가까운 이진 분수를 담고, 그것을 찍는 일은 별개의 두 번째 선택, 곧 몇 자리를 쓸지의 선택이다. 고르는 방법은 둘이다. **고정 소수 자릿수** — `%.3f`, `round(x, 3)`, `np.savetxt(fmt="%.3f")` — 는 절대 오차를 일정하게 둔다. **유효 숫자** — `%.17g`, `repr` — 는 상대 오차를 일정하게 둔다. Python의 `repr`는 같은 float로 되돌아오는 가장 짧은 문자열을 쓰고(Python 3.1부터), Python 3.2부터는 float의 `str`도 그 문자열과 같다. 그래서 표준 작성기 둘은 기본값으로 정확하다. `json.dumps`는 `float.__repr__`를 부르고, `csv` 모듈은 문자열이 아닌 것을 모두 `str`로 쓴다. 정밀도는 누군가 더 적은 자릿수를 고를 때만 사라진다 — 로깅 줄의 `"%.3f"`가 정확히 그 일을 한다.

고정 소수 자릿수는 [[02-foundations/signal-processing|6. 신호처리 §2]]의 뜻에서 계단 $q=10^{-d}$인 양자화기다. 찍힌 값은 최대 $q/2$ 어긋나고, 값들이 계단에 대해 무작위로 떨어지면 오차는 균일하게 퍼져 RMS가 $q/\sqrt{12}$다. 파싱이 두 번째 반올림, 곧 float 격자로의 반올림을 더한다. $2^e\le|x|<2^{e+1}$이면 $x$의 float64 이웃은 $2^{e-52}$ 간격이다([[03-deep-learning/foundations/training-at-scale|1.3 §4]]가 흔한 형식들의 $1$ 근처 간격을 표로 준다). $t_0\approx1.79\times10^9\,\mathrm{s}$에서는 $e=30$이라 간격이 $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$이고, 틱 2407의 명령에서는 $1\le|u|<2$라 $2^{-52}=2.2\times10^{-16}\,\mathrm{N}$이다.

그래서 요령 하나로 두 열을 다 다룰 수는 없다. 시간은 늘 $t_0$ 근처에 있으므로 고정된 $d$ 하나가 모든 샘플에 맞는다. $d=7$이면 모두 정확하다(계산 절 6단계). 명령은 대략 $-4.3$에서 $+4.0\,\mathrm{N}$까지 오가며 $0$ 근처를 지나는데, 거기서는 float 간격도 값을 따라 줄어들므로 어떤 고정 $d$도 모든 값에 정확할 수 없다. 명령에는 값을 따라 함께 작아지는 유효 숫자가 필요하다. float64 하나를 가려내는 데 유효 숫자 17개면 언제나 충분하고(아래 콜아웃이 증명한다) 16개는 늘 충분하지는 않으며, 틱 2407의 명령이 바로 열일곱째 자리가 필요한 float다. 영어 절의 코드가 틱 2407의 시간과 명령을 여러 모양으로 찍고 다시 읽는다. 출력은 다음과 같다.

```text
t as 1790000012.0351205  reads back +0.0000e+00 s off
t as 1790000012.035      reads back -1.2040e-04 s off
t as 1790000012.035120   reads back -4.7684e-07 s off
t as 1790000012.0351205  reads back +0.0000e+00 s off
u as -1.9578125000000002 reads back +0.0000e+00 N off
u as -1.958              reads back -1.8750e-04 N off
u as -1.95781250         reads back +2.2204e-16 N off
u as -1.9578125          reads back +2.2204e-16 N off
u as -1.9578125000000002 reads back +0.0000e+00 N off
float64 spacing at t: 2.384e-07 s, at u: 2.22e-16 N; float32 spacing at t: 128 s
```

시간은 `repr`와 `%.7f`에서 정확하고, `%.3f`에서 $120.4\,\mu\mathrm{s}$, `%.6f`에서 $0.48\,\mu\mathrm{s}$ 어긋난다. 명령은 `%.8f`와 `%.16g`에서도 마지막 비트 하나, $2.2\times10^{-16}\,\mathrm{N}$가 어긋나고, `%.17g`와 `repr`에서만 정확하다.

> [!note]- 더 깊이 · Deeper
> **유효 숫자 17개가 언제나 충분한 이유.** $10^j\le |x|<10^{j+1}$이면 열일곱째 유효 숫자의 무게가 $10^{j-16}\le |x|\cdot10^{-16}$이므로, 찍힌 소수는 $x$에서
>
> $$\tfrac12\,10^{j-16}\ \le\ 5\times10^{-17}\,|x|\ <\ 2^{-54}\,|x|\ \le\ \tfrac12\,s(x)$$
>
> 안에 있다. $2^{-54}=5.55\times10^{-17}$이고, $x$에서 더 가까운 float64 이웃까지의 간격 $s(x)$는 적어도 $2^{-53}|x|$이기 때문이다. 파서가 $x$를 돌려주는 데는 간격의 절반이면 된다. 유효 숫자 16개는 $5\times10^{-16}|x|$까지 어긋날 수 있고, 이것은 어떤 $x$에서는 간격의 절반보다 크다.

> **왕복의 정의.** **왕복**(round trip)은 *형식의 인코더 뒤에 디코더를 합성한 것* $x\mapsto\hat x=\mathrm{d}(\mathrm{e}(x))$을 메모리 속 값에 적용한 것이다. 값의 집합 위에서 인코더–디코더 쌍이 갖는 성질이지, 숫자 하나의 성질도 형식 이름의 성질도 아니다. **정확한** 왕복에는 조건 넷이 필요하다. 값이 **형식의 정의역 안**에 있어야 한다(NaN은 JSON의 정의역 밖이다). 바이트를 **짝이 맞는 디코더**가 읽어야 한다(float는 float로, 카운트는 정수로). 디코딩된 값의 **타입이 같아야** 한다(`1042.0`으로 돌아온 카운트는 타입이 바뀐 것이다, §6). 그리고 **$\hat x=x$가 비트 하나까지** 성립해야 한다. 회귀 테스트나 결과 표의 해시가 확인하는 등식이 이것이다. 소수 $d$째 자리까지 찍고 가장 가까운 float로 파싱하는 텍스트라면
>
> $$|\hat x-x|\le\tfrac12\,10^{-d}+\tfrac12\,s(x),\qquad \hat x=x\ \text{ whenever }\ 10^{-d}<s(x)$$
>
> 이고, $s(x)$는 $x$와 더 가까운 float64 이웃 사이의 간격으로 $t_0$에서 $2^{-22}\,\mathrm{s}$다. 찍힌 소수는 $x$에서 찍는 계단의 절반 안에 있고, 파서는 그것을 float 간격의 절반까지만 옮기기 때문이다.
>
> - **예**: 틱 2407의 시간. $d=3$이면 $120.4\,\mu\mathrm{s}$ 이르게 돌아오고 이는 한계 $500.12\,\mu\mathrm{s}$ 안이다. $d=7$이면 $10^{-7}<2^{-22}$이므로 정확히 돌아온다.
> - **비예**: 소수 여덟째나 아홉째 자리까지 찍은 명령. 실행 전체에서 최악의 오차가 $1.55\times10^{-14}\,\mathrm{N}$ — 어떤 힘 센서도 볼 수 없는 크기 — 인데도 정확히 돌아오지는 않는다(§10). "물리적으로 손실 없음"과 "비트까지 같음"은 서로 다른 약속이고, 두 로그를 `==`로 비교하는 회귀 테스트에는 뒤의 약속이 필요하다.
> - **왜 중요한가**: "찍은 자릿수까지" 재현된 결과는 모든 float에서 원본과 다를 수 있으므로, 재현성 검사는 두 약속 중 어느 것을 시험하는지 밝혀야 한다. 그리고 고정 자릿수로 찍은 시간 열은 계단보다 작은 규모를 정확히 지운다. 여기서는 지터다.

실무 규칙은 한 줄씩이다. float는 `repr`(`json`과 `csv`의 기본값)나 이진으로 기록한다. 고정 자릿수를 꼭 써야 한다면 $d$를 간격에서 고른다. 1970년부터 센 초라면 $d=7$이고, 신호라면 고정 자릿수 대신 유효 숫자를 쓴다. "공간을 아끼려고" 저장 전에 반올림하지 않는다. 여기서 `%.3f`가 `repr`보다 샘플당 아끼는 것은 약 $16$바이트이고(§10), 이진은 아무것도 잃지 않고 $22$바이트를 아낀다.

### 3. JSON: 여섯 가지 타입, 주석 없음, 텍스트인 숫자

*한 문장으로:* JSON은 "모든 언어가 읽을 수 있는 작은 파일 하나"라는 문제를 값 타입 여섯 가지짜리 텍스트 문법으로 풀고, 로봇에게 그 함정은 숫자 — NaN이 없고, 많은 독자에게 정수는 $2^{53}$까지만 정확하다 — 와 주석이 없다는 데 있다.

JSON은 RFC 8259(2017년 12월)가 정의하고, 문법 전체가 한 쪽에 들어간다. JSON 텍스트는 값 하나 — 문자열, 숫자, `true`나 `false`, `null`, 이름–값 쌍의 객체, 배열 — 이고, 토큰 사이의 공백은 아무 뜻이 없으며, 주석 문법은 아예 없고, 시스템 사이에서 주고받는 텍스트는 UTF-8이어야 한다. 규칙은 아래 정의 상자가 적는다. 로봇이 JSON에 무엇을 담을 수 있는지는 세 가지 세부가 정한다.

- **숫자는 십진 텍스트다.** 선택적인 마이너스, 숫자들, 선택적인 소수부와 지수부로 이루어지고, 앞자리 0은 허용되지 않으며, NaN과 Infinity는 쓸 수 없다. RFC는 구현마다 받아들이는 범위와 정밀도를 제한해도 된다고 하면서 IEEE 754 double을 상호운용의 기준으로 드는데, 아래의 $2^{53}$ 한계가 여기서 나온다.
- **객체 안의 이름은 유일해야 한다(SHOULD).** 그렇지 않으면 받는 소프트웨어의 동작은 예측할 수 없다고 RFC는 적는다. Python의 `json`은 마지막 값을 남기고 아무 오류도 내지 않는다.
- **숫자의 뜻은 어디에도 없다.** `"u": -1.958`에는 단위가 없고, 단위를 적을 주석을 둘 자리도 JSON 파일에는 없다.

Python의 `json` 모듈은 함정 하나를 더한다. 기본값으로 float NaN을 `NaN`, 무한대를 `Infinity`라는 JavaScript 철자로 쓰는데, RFC 8259는 이것을 허용하지 않으므로 다른 언어의 엄격한 파서는 그 파일을 거부한다. 로봇에서는 기록기가 NaN으로 적어 둔 끊긴 비전 목표가 그 경우다. `allow_nan=False`를 주면 작성기가 대신 `ValueError`를 낸다. 기록기에 바라는 동작이 이쪽이다. 영어 절의 코드가 실행 042의 사이드카를 쓰고 다시 읽은 뒤 세 함정을 차례로 보이며, 출력은 다음과 같다.

```text
202 bytes; reads back equal: True
{"goal": NaN}
allow_nan=False raises ValueError
{'kp': 20.0}
True 78
```

코드의 `meta` 사전이 실행 042의 **사이드카**, 곧 로그 옆에 붙어 다니며 로그의 바이트가 말하지 못하는 것 — 어떤 열, 어떤 단위, 어떤 시계 — 을 말하는 작은 파일이다. 여섯 타입 — 문자열, 숫자, 불리언, `null`, 배열, 객체 — 을 모두 쓰고, 다시 읽으면 같다. 미묘한 것은 마지막 줄이다. 틱 2407의 시계 값을 1970년부터 센 정수 나노초로 적으면 $1.79\times10^{18}$로, $2^{53}-1\approx9.0\times10^{15}$을 훨씬 넘는다. Python은 정수에 크기 제한이 없어 정확히 간직하지만, JSON 숫자를 double로 파싱하는 독자 — Python의 `json` 문서가 경고하듯 흔한 일이다 — 는 가장 가까운 double을 받으므로 여기서 $78\,\mathrm{ns}$, 실행 전체에서 최대 $128\,\mathrm{ns}$ 어긋난다(§10). 올바른 JSON이면서 이식성은 없는 파일이다. 이런 시각은 초와 나노초 두 정수 — ROS 2 시각 스탬프의 모양([[04-robotics/ros2/nodes-topics-messages|25.2 §4]]) — 로 쓰거나, $6.0\times10^{10}$ 아래에 머무는 실행 시작부터의 나노초로 쓴다.

> **JSON 텍스트의 정의.** **JSON 텍스트**(JSON text)는 *여섯 가지 값 타입으로 된 트리에서 값 하나를 적은 텍스트 직렬화*로, RFC 8259가 규정한다. 형식이지 Python 사전도 JavaScript 객체도 아니다. 조건은 다섯이다. 모든 값은 **여섯 타입 중 하나**다: 객체, 배열, 문자열, 숫자, `true`/`false`, `null`. **숫자는 십진 텍스트**이고 NaN, Infinity, 앞자리 0이 없다. **주석이 없다.** **객체 안의 이름은 유일해야 한다.** 그리고 열린 시스템 사이에서 주고받는 텍스트는 **UTF-8**이다. 모든 독자가 정확히 간직하는 정수는
>
> $$|n|\le 2^{53}-1=9\,007\,199\,254\,740\,991$$
>
> 이다. binary64 double의 유효 비트가 53개라서 $2^{53}$까지의 정수는 저마다 제 double을 갖지만, 그 너머에서 double은 $2$, $4$, 그 이상 간격으로 벌어지기 때문이다. $1.79\times10^{18}$에서는 $2^{60-52}=256$ 간격이다.
>
> - **예**: 위의 실행 042 사이드카 $202$바이트, 그리고 실행의 모든 카운트. $1042$는 어느 언어에서나 정확한 JSON 숫자다.
> - **비예**: Python이 기본값으로 쓰고 RFC 8259가 금지하는 `{"goal": NaN}`. 그리고 시각 $1{,}790{,}000{,}012{,}035{,}120{,}562$. 올바른 JSON이지만 double 기반 독자는 조용히 $78\,\mathrm{ns}$를 옮긴다.
> - **왜 중요한가**: 설정과 메타데이터는 언어를 건넌다 — Python 학습 코드, C++ 노드, 웹 대시보드 — 그리고 무엇이 살아남는지는 Python이 아니라 각 독자의 정의역이 정한다.

**JSON을 쓰는 곳과 쓰지 않는 곳.** robomimic은 학습 실행마다의 설정을 JSON 파일로 두고 `--config`로 학습기에 넘기며, LeRobot은 데이터셋을 `meta/info.json`과 `meta/stats.json`으로 기술한다(§8). 설정에서 JSON의 대가는 주석이 없다는 것이다. 이득 옆에 왜 $200$인지 적을 수 없다. 로그에서의 대가는 크기다. 샘플마다 객체 하나를 쓰면 이름이 모두 되풀이되어 틱 2407에서 $67$자 중 $26$자이고, 이름을 한 번만 쓰는 열마다 배열 하나로도 샘플당 $45.03$바이트, 이진의 $20$에 비해 크다(§10). **줄마다 JSON 텍스트 하나**인 파일 — RFC 8259의 일부가 아닌 관례 — 은 적어도 덧붙이기와 줄 단위 읽기가 된다. LeRobot의 이전 데이터셋 버전은 에피소드 목록을 그렇게 `meta/episodes.jsonl`에 두었다.

### 4. YAML: 들여쓰기, 철자로 정해지는 타입, 한 로봇 안의 두 독자

*한 문장으로:* YAML은 사람이 주석을 달며 따옴표 없이 설정을 손으로 쓰게 해 주지만, 따옴표 없는 값에는 독자의 표에서 그 철자가 맞는 타입을 주고 — ROS 2 시스템 안에는 표가 서로 다른 독자가 둘 있다.

YAML은 ROS 2 파라미터 파일, rosbag2의 `metadata.yaml`, YAML로 쓴 launch 파일, 그리고 학습 코드 설정의 상당수가 쓰는 형식이다. 구조는 들여쓰기다. 콜론이 붙은 키는 그 아래 들여 쓴 것을 모두 담고, `- `로 시작하는 줄은 리스트의 항목이다. 들여쓰기는 스페이스여야 하고, 명세가 들여쓰기에 탭을 금지한다. 공백 뒤의 `#`는 주석을 시작하는데, 주석은 읽어 들인 데이터에 아무 영향이 없는 표현상의 세부이므로 설정을 읽었다가 다시 쓰는 프로그램은 주석을 모두 잃는다. YAML 1.2(2009, 지금의 개정판은 2021년의 1.2.2)는 YAML을 JSON의 상위 집합으로 만들고 1.1판의 암묵적 타입 규칙을 대부분 없앴지만, 많은 소프트웨어가 아직 YAML 1.1로 읽는다. 다음 문단의 문제가 그것이다.

탈이 나는 곳은 **철자로 정해지는 타입**이다. 따옴표를 친 값은 문자열이다. 따옴표 없는 값 — *plain 스칼라* — 은 독자의 스키마에서 처음 맞는 패턴의 타입을 받고, 스키마는 서로 다르다. YAML 1.2의 core 스키마는 대소문자 세 가지의 `true`/`false`, 십진 정수, `0o` 8진수, `0x` 16진수, 실수를 안다. YAML 1.1의 타입 저장소는 그 밖에 `y`, `yes`, `on`, `n`, `no`, `off`도 불리언으로, 앞자리 `0`을 8진수로, `1_000`을 천으로, `12:30`을 60진수로 읽고, 실수에는 소수점을 요구한다. 그리고 ROS 2 시스템 안에는 YAML 독자가 둘 있다.

- **기동할 때**, `--params-file`을 받은 노드 — launch 파일이 파라미터 파일을 넘기는 방식이 이것이고, Python 사전으로 만든 파라미터도 마찬가지다 — 는 rcl의 C 파서로 파일을 읽는다. 따옴표를 친 값은 문자열로 받고, 아니면 YAML 1.1 불리언 목록의 22개 낱말(`y`와 `n` 포함)을 보고, 그다음 C의 숫자 파싱을 쓴다. 이 파싱은 앞자리 `0`을 8진수로 읽고 `5e-3`, `nan`, `inf`도 받아들인다. 나머지는 모두 문자열이다.
- **실행 중에는** `ros2 param set`과 `ros2 param load`가 PyYAML로 파싱한다(Jazzy의 rclpy). PyYAML은 스스로를 완전한 YAML 1.1 파서라고 소개하지만, 한 글자짜리 `y`, `Y`, `n`, `N`은 불리언에서 뺐다. `ros2 param load`는 심지어 두 번 파싱한다. 파일을 읽고, 값마다 다시 텍스트로 바꾼 뒤 그 텍스트를 또 파싱하므로, 불리언이나 숫자처럼 보이는 문자열은 따옴표를 쳐도 도중에 따옴표를 잃는다.

아래 표는 plain 스칼라 열 개를 세 독자로 결정한다. 표를 찍는 코드, 곧 각 독자의 규칙을 옮겨 적은 것은 표 아래 콜아웃에 있다.

| plain 스칼라 | YAML 1.2 core | PyYAML (YAML 1.1) | ROS 2 rcl, 기동 시 |
|---|---|---|---|
| `0.005` | float 0.005 | float 0.005 | float 0.005 |
| `5e-3` | float 0.005 | str `'5e-3'` | float 0.005 |
| `1.10` | float 1.1 | float 1.1 | float 1.1 |
| `0123` | int 123 | int 83 | int 83 |
| `08` | int 8 | str `'08'` | float 8.0 |
| `y` | str `'y'` | str `'y'` | bool True |
| `off` | str `'off'` | bool False | bool False |
| `12:30` | str `'12:30'` | int 750 | str `'12:30'` |
| `1_000` | str `'1_000'` | int 1000 | str `'1_000'` |
| `2026-09-21` | str `'2026-09-21'` | date 2026-09-21 | str `'2026-09-21'` |

> [!note]- 더 깊이 · Deeper
> **표를 어떻게 계산했나.** 영어 절의 같은 자리에 있는 코드의 resolver 셋은 각각 plain 스칼라에 한정해 옮겨 적은 것이다. YAML 1.2.2 §10.3.2의 core 스키마 표, PyYAML의 `resolver.py`, 그리고 Jazzy 브랜치 rcl의 `rcl_yaml_param_parser`에 있는 `get_value()`인데, 이 함수는 먼저 `!!str` 태그와 따옴표를, 그다음 불리언 낱말 22개를, 그다음 기수 0의 `strtoll`을, 그다음 `strtod`를 시험한다. 모든 행은 이 페이지를 쓴 기계에서 따로 돌린 PyYAML 6.0.1, 그리고 C 라이브러리의 `strtoll`·`strtod`와 일치한다. `ros2 param set`과 `ros2 param load` 뒤의 PyYAML 호출은 rclpy의 `get_parameter_value`와 `parameter_dict_from_yaml_file`이고, 뒤의 것이 읽은 값마다 `str()`을 거쳐 앞의 것에 넘기는 것이 위에서 말한 두 번 파싱이다.

행들을 손으로 고친 P6 설정이라고 생각하고 읽어 보자.

- `control_period: 5e-3`는 rcl이 double로 읽으므로 제어기를 $200\,\mathrm{Hz}$로 띄운다. 그런데 같은 글자를 나중에 `ros2 param set /cart/controller control_period 5e-3`로 넣으면 PyYAML에 닿아 문자열로 도착하고, 파라미터의 선언 타입이 그것을 거부한다 — [[04-robotics/ros2/services-actions-parameters|25.3 §6]]의 타입 조항이다.
- 드라이버 파라미터 `motion_axis: y`는 기동할 때 불리언이 되는데 `x`와 `z`는 문자열로 남으므로, 세 축 중 정확히 하나만 실패한다.
- 앞을 0으로 채운 `device_id: 0123`은 두 ROS 독자 모두에게 83이고 YAML 1.2 도구에게는 123이다. `version: 1.10`은 어디서나 float 1.1이다.
- 실행 날짜 `date: 2026-09-21`을 Python 스크립트에서 읽으면 `datetime.date`가 되고, `json.dumps`는 그것을 쓰기를 거부한다.

어느 것도 YAML의 오류가 아니다. 저마다 누가 읽느냐에 따라 타입이 달라지는 값일 뿐이다. 처방은 매번 같다. 숫자나 불리언처럼 보일 수 있는 문자열에는 따옴표를 치고, 실수는 소수점 양쪽에 숫자를 두어 쓰고(`0.005`), 정수는 절대 0으로 채우지 않는다. 따옴표는 기동할 때와 `ros2 param set`에서는 문자열을 지켜 주지만 `ros2 param load`에서는 못 지킨다. 두 번째 파싱이 따옴표 친 `"on"`을 불리언 참으로 읽기 때문이다. 그러니 가장 안전한 문자열은 어느 독자도 다른 것으로 오해할 수 없는 문자열이다.

> **암묵적 타입 결정의 정의.** **암묵적 타입 결정**(implicit typing) — YAML의 *태그 결정*(tag resolution) — 은 *독자의 스키마가 가진 규칙*이다. plain 스칼라의 텍스트에서 타입으로 가는 함수이고, 파일을 읽는 쪽이 적용한다. 파일 자체는 타입을 싣지 않는다. 조건은 넷이다. **plain 스칼라에만** 적용된다. 따옴표를 친 스칼라는 문자열이고, `!!str` 같은 명시적 태그는 모든 것에 우선한다. 스키마는 타입이 하나씩 달린 **패턴들의 순서 있는 목록**을 갖는다. **텍스트 전체와 맞는 첫 패턴**이 정한다. 그리고 core 스키마에서는 **맞는 패턴이 없으면 문자열**이다(JSON 스키마는 이를 오류로 본다).
>
> $$\operatorname{type}(s)=\tau_{j^\star},\qquad j^\star=\min\{\,j:\ s\in L(r_j)\,\},\qquad \operatorname{type}(s)=\text{str if no }r_j\text{ matches}$$
>
> $s$는 스칼라의 텍스트, $r_1,r_2,\dots$는 순서대로 놓인 스키마의 패턴, $L(r_j)$는 패턴 $r_j$가 전체로 맞추는 문자열의 집합, $\tau_j$는 그 타입이다. 그래서 같은 텍스트가 그것을 읽는 스키마의 수만큼 타입을 가질 수 있다.
>
> - **예**: `5e-3`은 소수점 없는 지수를 허용하는 core 실수 패턴에 맞아 $0.005$가 된다. PyYAML의 실수 패턴은 소수점을 요구하고(지수가 있으면 부호도) `5e-3`에는 소수점이 없으므로 문자열까지 내려간다.
> - **비예**: 따옴표를 친 `"5e-3"`. 모든 독자에게 문자열이다 — 따옴표가 암묵적 타입 결정을 끈다. 파라미터 파일의 모양, 곧 노드 이름 아래 글자 그대로의 키 `ros__parameters`도 타입 규칙이 아니다. 그것은 ROS 2 독자의 관례이고 [[04-robotics/ros2/services-actions-parameters|25.3 §7]]이 정의하며, 네임스페이스의 함정은 [[04-robotics/ros2/workspaces-packages-launch|25.4 §11]]에 있다.
> - **왜 중요한가**: 설정 파일은 둘 이상의 프로그램이 읽는다 — 기동하는 노드, 명령줄, 내 분석 스크립트 — 그리고 누가 읽느냐에 따라 타입이 달라지는 값은 두 번째 독자를 기다리는 버그다.

**학습 코드의 설정.** 로봇 학습 코드에서 흔한 Python 프레임워크 Hydra는 여러 YAML 파일을 합성해 계층적인 설정을 만들고, 어떤 값이든 명령줄에서 덮어쓰게 해 준다. 그리고 실행마다 합성된 설정을 그 실행의 출력 디렉터리 `.hydra/config.yaml`에, 덮어쓴 값을 그 옆 `overrides.yaml`에 적는다. [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성 §7]]의 산출물 체크리스트가 보고하는 모든 실행에 남기라고 요구하는 설정 스냅숏이 바로 그것이다. 설정을 무엇으로 만들든, 실행이 실제로 쓴 파일을 그 로그 옆에 남겨 둔다.

### 5. XML: 값이 모두 문자열인 요소의 트리

*한 문장으로:* XML은 트리를 적는다 — 그래서 ROS가 로봇의 링크와 관절에 XML을 쓴다 — 그러나 그 안의 값은 모두 문자열이므로, URDF의 숫자는 그것을 변환하는 독자만큼만 옳다.

XML 1.0(W3C, 제5판, 2008)은 JSON이나 YAML보다 오래되었지만 지금도 ROS 로봇의 대부분을 기술한다. URDF([[04-robotics/ros2/describing-a-robot|25.6 §2]]), 그것을 만들어 내는 Xacro 매크로(그 페이지의 §5), 모든 패키지의 `package.xml`([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]), 그리고 XML로 쓴 launch 파일(그 페이지의 §9)이 그렇다. XML 문서는 **요소**의 트리다. 요소는 시작 태그와 끝 태그 사이에 내용이 든 것이거나, `<link name="base_link"/>` 같은 빈 요소 태그 하나다. 시작 태그는 **속성**, 곧 값에 따옴표를 친 `name="value"` 쌍을 가질 수 있다. 문서를 **형식이 올바르게**(well-formed) 만드는 규칙은 몇 되지 않는다. 뿌리 요소가 정확히 하나이고 나머지를 모두 담는다. 다른 요소 안에서 시작한 요소는 그 안에서 끝난다. 한 태그에서 속성 이름은 한 번만 나온다. 텍스트 속의 `<`와 `&`는 `&lt;`와 `&amp;`로 이스케이프한다. 주석 `<!-- … -->` 안에는 하이픈 두 개가 연달아 올 수 없다.

XML에 없는 것은 타입이다. 모든 속성 값과 모든 텍스트 조각은 문자열이고, 그 문자열의 뜻은 파일을 읽는 프로그램이 정한다. URDF 관절의 원점 `<origin xyz="0.10 0 0.25" rpy="0 0 0"/>`는 공백으로 가른 숫자 세 개짜리 문자열 둘이고, 그것을 쪼개 미터와 라디안으로 바꾸는 것은 XML이 아니라 URDF 독자다. 영어 절의 코드는 [[04-robotics/ros2/describing-a-robot|25.6]]이 고정한 P6의 유일한 고정 관절, 카메라 마운트를 표준 라이브러리로 읽는다. 출력은 다음과 같다.

```text
robot 7 elements; '0.10 0 0.25' -> [0.1, 0.0, 0.25]
comments after parsing: 0
ParseError: junk after document element: line 11, column 0
```

출력 세 줄에 교훈이 셋이다. 속성은 문자열 `'0.10 0 0.25'`로 돌아왔고, 그것을 숫자로 바꾸는 것은 이 스크립트의 일이었다. 숫자의 출처를 적어 둔 주석은 파싱을 거치며 사라졌다 — Python의 `ElementTree`는 주석을 건너뛴다 — 그러니 URDF를 읽었다가 다시 쓰는 도구는 그 문서화를 버린다. YAML을 읽고 다시 쓸 때(§4)와 똑같다. 그리고 한 파일에 붙여 넣은 로봇 둘은 더 큰 로봇이 아니라 문서가 아예 아니다. 파서는 두 번째 뿌리에서 멈춘다.

**형식이 올바르다고 옳은 것은 아니다.** 파서는 이 절 첫머리에 적은 XML 자체의 문법만 검사하고, 어떤 요소의 뜻도 모른다. `xyz`를 `xzy`로 잘못 쓴 URDF도 여전히 형식이 올바르다. `origin`이 어떤 속성을 가져야 하는지 XML은 모르므로 그 검사는 URDF 독자의 몫이고, 그래서 "파일이 파싱된다"는 확인은 그 안의 숫자에 대해 아무것도 말해 주지 않는다.

**만난 대로 쓴다.** 연구자가 XML을 고르는 일은 드물다. URDF와 `package.xml`에 XML을 고른 것은 ROS이고, XML launch 형식은 Python·YAML 형식 옆에 있다. 이 형식이 요구하는 것은 단위를 주석이나 README에 남기는 것(파일이 타입으로 실어 줄 수 없으니까), 반복되는 구조를 복사하지 말고 Xacro 같은 도구가 만들게 하는 것, 그리고 신뢰할 수 없는 XML은 조심해서 파싱하는 것이다. Python의 `xml.etree` 문서는 바로 그 경우를 위해 XML 보안 안내로 이어진다.

### 6. CSV: 타입 없는 표

*한 문장으로:* CSV는 "누구나 열 수 있는 표"라는 문제를 풀지만, 그 값으로 타입도 단위도 하나의 표준도 없으므로, 독자에게 글자 이상으로 필요한 것은 모두 파일 밖에 있다.

CSV는 누구나 열 수 있고 오랫동안 아무도 명세하지 않은 형식이다. RFC 4180(2005년 10월)은 흔한 관행을 기술하는 정보 제공용 메모이지 표준을 정의하는 문서가 아니고, Python의 `csv` 문서는 잘 정의된 표준이 없어서 응용 프로그램마다 만들고 받아들이는 파일에 미묘한 차이가 남는다고 적는다. RFC 4180이 기록한 관행은 이렇다. 레코드는 한 줄에 하나이고 줄은 CRLF로 끝난다. 첫 줄에 필드 이름이 올 수 있다. 필드는 쉼표로 가르고, 공백도 필드의 일부로 친다. 쉼표, 큰따옴표, 줄바꿈이 든 필드는 큰따옴표로 감싸고, 그 안의 큰따옴표는 두 번 쓴다.

영어 절의 코드는 따옴표가 필요한 필드가 든 한 줄을 `csv` 모듈로 쓰고 다시 읽는다. 출력은 다음과 같다.

```text
'run,topics,note,kp\r\n042,"/cart/goal,/cart/cmd","goal ""held"" at 0.6 m",200.0\r\n'
['042', '/cart/goal,/cart/cmd', 'goal "held" at 0.6 m', '200.0'] ['str', 'str', 'str', 'str']
```

작성기는 쉼표가 든 필드를 따옴표로 감싸고 메모 안의 따옴표를 두 번 썼으며, 모듈의 기본 줄 끝인 `\r\n`으로 줄을 마쳤다. 문서는 CSV 파일을 `newline=""`로 열라고 한다. 그러지 않으면 따옴표 친 필드 안의 줄바꿈을 잘못 읽고, 어떤 플랫폼에서는 `\r`이 하나 더 쓰인다. 독자는 문자열 넷을 돌려주었다. **CSV에는 타입이 없다.** `'200.0'`은 누군가 `float`를 부르기 전까지 텍스트이고, 실행 ID `'042'`에 누군가 `int`를 부르면 $42$가 된다. 따옴표 없는 필드를 모두 float로 다루라고(`QUOTE_NONNUMERIC`) 지시하지 않는 한 독자는 아무 변환도 하지 않는다. 헤더 줄이 유일한 스키마이고, 그것은 이름을 담을 뿐 단위를 담지 않는다. `u`는 뉴턴이라고 말하지 않으며, `t_s,counts,u_N`은 값싼 개선이다.

로그에서의 문제는 정밀도와 크기이고, 둘 다 형식이 아니라 작성기의 선택이다. `csv` 모듈은 float를 `str`, 곧 `repr`(§2)로 쓰므로, Python float로 쓴 실행은 정확히 되돌아온다. P6에서 샘플당 $42.03$바이트, 이진의 $2.10$배다(§10). 손실은 형식 문자열에서 온다. `"%.3f"`는 줄을 $25.73$바이트로 줄이는 대신 시간에서 최대 $200\,\mu\mathrm{s}$ — 지터 전부 — 를, 명령에서 $0.5\,\mathrm{mN}$을 잃는다. NumPy의 `np.savetxt`는 반대로 간다. 기본값 `fmt="%.18e"`는 유효 숫자 19개를 지수 꼴로 찍어 정확하지만 샘플당 $75.50$바이트로 JSON보다 크고, 카운트 $1042$를 `1.042000000000000000e+03`으로 써서 float `1042.0`으로 돌아오게 한다. 값은 살아남고 타입은 살아남지 못한다.

> **CSV 표의 정의.** **CSV 표**(CSV table)는 *구분자로 가른 텍스트 표*다. 레코드의 나열이고 레코드마다 한 줄의 텍스트 필드다. 행을 적는 방식일 뿐 자기 타입도 스키마도 없다. 조건은 넷이다. **레코드는 한 줄에 하나**다. **필드는 구분자**, 곧 쉼표로 **가른다.** 구분자나 따옴표나 줄바꿈이 든 필드는 **따옴표로 감싸고 안쪽 따옴표는 두 번 쓴다.** 그리고 독자가 변환하기 전까지 **모든 필드는 텍스트**이고, 이름을 적은 헤더 줄이 기껏해야 하나 있다. 헤더와 $m$개 필드의 레코드 $n$개로 된 파일은
>
> $$B=\sum_{r=0}^{n}\Big(\sum_{i=1}^{m}\ell_{ri}+(m-1)+\lambda\Big)$$
>
> 바이트를 차지한다. $r=0$은 헤더, $\ell_{ri}$는 레코드 $r$의 필드 $i$가 따옴표까지 포함해 차지하는 글자 수, $m-1$은 쉼표, $\lambda$는 줄 끝 문자로 `\n`이면 $1$, 모듈 기본값 `\r\n`이면 $2$다. ASCII 파일에서는 글자도 쉼표도 줄 끝도 하나가 1바이트이기 때문이다.
>
> - **예**: `repr`와 `\n`으로 쓴 실행 042. $11$바이트 헤더 `t,counts,u`에 레코드 $504{,}329$바이트, 모두 $504{,}340$바이트다(§10). `\r\n`이었다면 $12{,}001$바이트가 더 붙는다.
> - **비예**: 세미콜론 구분자와 소수점 쉼표를 쓰는 "CSV". 다른 방언이라서 쉼표로 읽는 독자는 필드를 엉뚱하게 가른다. 그리고 `np.savetxt`의 카운트 열. 올바른 CSV이지만 값이 float로 돌아온다 — 표는 모든 값을 지키고도 타입을 잃을 수 있다.
> - **왜 중요한가**: CSV 파일은 보내기 가장 쉽고 잘못 읽기도 가장 쉽다. 독자에게 글자 이상으로 필요한 것 — 구분자, 따옴표 규칙, 자릿수, 단위, 타입 — 이 모두 파일 밖에 있기 때문이다.

**언제 쓰는가.** CSV는 사람이 열어 볼 작은 표에, 그리고 샘플마다 한 줄을 덧붙이고 죽어도 마지막 줄 하나만 잃는 스크립트의 간단한 로그에 알맞다. `repr`나 충분한 자릿수로 쓰고(§2), 헤더에 단위를 적고, 사이드카(§3)를 옆에 두고, 시간 단위로 기록하는 것은 이진으로 옮긴다. P6의 한 시간은 텍스트로 $30\,\mathrm{MB}$, 이진으로 $14.4\,\mathrm{MB}$이고, 읽을 때마다 모든 글자를 다시 파싱한다.

### 7. 이진 레코드: 폭, 바이트 순서, 정렬, `.npy` 헤더

*한 문장으로:* 이진 레코드는 샘플을 작고 빠르고 정확하게 담는다 — 필드 자신의 바이트를 폭, 오프셋, 바이트 순서, 패딩이라는 규칙에 따라 늘어놓은 것이다 — 그리고 파일은 그 규칙이 함께 다닐 때만 쓸모가 있다.

float64는 IEEE 754 binary64 수의 8바이트이고 int32는 4바이트다. 값이 무엇이든 그렇다. 이것들을 이어 적으면 **레코드**가 되고, 레코드들의 파일은 바이트가 뜻을 갖기 전에 세 가지 사실이 필요하다. **바이트 순서**: x86-64 프로세서와, 이 페이지의 코드를 돌린 Apple M1 노트북은 리틀 엔디언이고, `struct` 모듈의 접두사 `<`는 기계와 상관없이 리틀 엔디언으로 쓴다. **오프셋**: 각 필드가 어디서 시작하는가. **정렬**: 필드를 빈틈없이 잇는가(packed), 아니면 C 컴파일러가 구조체를 배치하듯 각 필드가 자기 크기의 배수에서 시작하도록 패딩하는가. Python의 `struct` 모듈은 표준 모드(`<`, `>`, `=`, `!`)에서 패딩을 넣지 않고 네이티브 모드(`@`)에서는 그 기계의 C 컴파일러처럼 패딩한다. NumPy는 구조화 dtype을 기본으로 빈틈없이 잇고, `align=True`면 가장 큰 필드 정렬의 배수까지 채우는 꼬리 패딩까지 포함해 C 구조체처럼 패딩한다.

영어 절의 코드가 틱 2407을 `struct`로 싸고, 두 배치의 오프셋을 재고, `.npy` 헤더를 열어 보고, 배치를 잘못 짐작해 읽어 본다. 출력은 다음과 같다.

```text
20 6a 3f 02 e3 4e ac da 41 12 04 00 00 34 33 33 33 33 53 ff bf
struct sizes: '<did' 20, native '@did' 24
the count's 4 bytes read little-endian 1042, big-endian 302252032
itemsize packed 20, offsets [0, 8, 12]; aligned 24, offsets [0, 8, 16]
b'\x93NUMPY\x01\x00' header length 182 -> data starts at byte 192 ; file 240192 bytes
{'descr': [('t', '<f8'), ('counts', '<i4'), ('u', '<f8')], 'fortran_order': False, 'shape': (12000,), }
10000 records; the first reads t = 1790000012.0351205, counts = 1042, u = -8.608277440935864e+168
```

그림의 위쪽 막대 두 개가 이 줄들이다. 카운트 $1042$는 `0x0412`이고 낮은 바이트부터 `12 04 00 00`으로 저장된다. 같은 네 바이트를 빅 엔디언으로 읽으면 $302{,}252{,}032$이고 오류는 없다 — 틀린 바이트 순서는 실패하지 않고 거짓말을 한다. 정렬하면 카운트 필드 뒤에 패딩 4바이트가 붙어 $u$가 $8$의 배수인 바이트 $16$에서 시작하고, 레코드는 $20$에서 $24$바이트로 늘어 시간당 $14.40$ 대신 $17.28\,\mathrm{MB}$가 된다. 정렬 말고는 얻는 것이 없는 증가다.

**`.npy` 파일**은 "배치가 바이트와 함께 다녀야 한다"는 요구에 대한 NumPy의 답이다. dtype — 필드마다의 이름, 타입, 폭, 바이트 순서를 적은 NumPy의 기록으로, 여기서는 `[('t', '<f8'), ('counts', '<i4'), ('u', '<f8')]` — 과 shape을 적은 짧은 텍스트 헤더 뒤에 날 데이터가 온다. 여기서 헤더는 바이트 $192$에서 끝나고, $192+12{,}000\times20=240{,}192$바이트가 파일 전체다. 일상에 속하는 사실이 둘 더 있다. **`.npz`** 파일은 배열마다 하나씩 `.npy` 파일을 담은 zip 아카이브이고, `np.savez`는 압축하지 않고 `np.savez_compressed`는 deflate로 압축한다. 그리고 **`np.load`는 기본값으로 pickle 객체 배열을 거부한다**(`allow_pickle=False`). pickle을 읽으면 임의의 코드가 실행될 수 있기 때문이다. 내가 쓰지 않은 파일에 대해서는 절대 켜지 않는다.

> [!note]- 더 깊이 · Deeper
> **`.npy` 헤더, 바이트 단위로.** 형식은 다른 언어에서도 읽을 수 있도록 문서화되어 있다. 매직 문자열 `\x93NUMPY`, 주 버전과 부 버전 한 바이트씩, 두 바이트 리틀 엔디언 헤더 길이(1.0판), 그리고 Python 사전 리터럴인 헤더 — `descr`(dtype), `fortran_order`, `shape` — 가 오며, 헤더는 매직·버전·길이·헤더를 합쳐 $64$바이트의 배수가 되도록 공백과 마지막 줄바꿈으로 채운다. 여기서는 $10+182=192=3\times64$이고, 목록이 찍은 값이 이것이다.

> **이진 레코드 배치의 정의.** **이진 레코드 배치**(binary record layout)는 *이진 파일의 행이 따르는, 타입 있는 필드들의 바이트 속 고정된 배열*이다. C 구조체, NumPy 구조화 dtype, `struct` 형식 문자열이 그것이다. 조건은 넷이다. 모든 필드는 **폭이 고정된 타입**을 갖는다. 모든 필드는 레코드 시작부터의 **오프셋**을 갖는다. 여러 바이트짜리 값들은 **바이트 순서** 하나를 따른다. 그리고 **정렬 규칙** 하나가 오프셋을 정한다. packed면 각 필드가 앞 필드가 끝난 곳에서 시작하고, aligned면 각 오프셋이 그 필드 정렬의 배수이며 레코드는 가장 큰 정렬의 배수까지 채운다. 식 하나로는
>
> $$o_1=0,\qquad o_{i+1}=\big\lceil (o_i+w_i)/a_{i+1}\big\rceil\,a_{i+1},\qquad S=\big\lceil (o_m+w_m)/a^\star\big\rceil\,a^\star,\qquad B_{\text{file}}=H+nS$$
>
> 이다. $w_i$는 필드 $i$의 폭, $a_i$는 그 정렬(packed면 $1$, aligned면 보통 $w_i$), $a^\star=\max_i a_i$, $S$는 레코드 크기, $n$은 레코드 수, $H$는 헤더다. 그래서 패딩은 좁은 필드 뒤에 넓은 필드가 올 때 정확히 그 자리에 생긴다.
>
> - **예**: P6의 레코드 `t` f8, `counts` i4, `u` f8. packed: 오프셋 $0, 8, 12$, $S=20$. aligned: 오프셋 $0, 8, 16$, $S=24$. `.npy`로는 $B_{\text{file}}=192+12{,}000\times20=240{,}192$바이트.
> - **비예**: 배치가 어디에도 적혀 있지 않은 "20바이트짜리 샘플들의 파일". `<` 대신 `>`로 읽으면 카운트가 $302{,}252{,}032$가 된다. aligned 배치로 읽으면 packed 레코드 $12{,}000$개의 $240{,}000$바이트가 레코드 $10{,}000$개가 되고, 첫 명령은 $-8.6\times10^{168}\,\mathrm{N}$이다. $240{,}000$이 공교롭게 $24$로 나누어떨어지기 때문이다 — 두 실수 모두 오류를 내지 않는다.
> - **왜 중요한가**: 로봇 데이터가 작고 빠르고 정확한 곳이 이진이고, 이진은 배치가 함께 저장될 때 — 헤더든, 스키마든, 적어도 사이드카든 — 에만 그 성질을 지킨다.

### 8. 로봇 데이터의 컨테이너: HDF5, Parquet, MCAP

*한 문장으로:* 실행이나 데이터셋은 여러 배열이나 메시지에 그 이름과 스키마를 더한 것이고, 컨테이너는 그것을 파일 하나에 담으며, 로봇 학습 연구자가 만나는 셋은 조직 방식이 다르다 — HDF5는 배열의 트리, Parquet은 열, MCAP은 시간 순서의 메시지 흐름이다.

이 절은 HDF5와 Parquet을 그 문서와, 그것을 쓰는 데이터셋 형식에 근거해 설명한다. 두 라이브러리는 이 페이지의 실습에 들어가지 않는다. MCAP의 레코드 틀은 `struct`로 직접 만들 수 있을 만큼 단순하고, 아래 코드가 그렇게 한다.

**HDF5.** HDF5 파일은 두 종류의 객체, *그룹*과 *데이터셋*으로 된 컨테이너이고, 디렉터리와 파일처럼 경로로 가리킨다. `/`가 뿌리 그룹이고 `/data/demo_0/actions`는 그룹 둘 아래의 데이터셋이다. 데이터셋은 타입과 shape을 가진 다차원 배열이고, 어떤 객체든 작은 이름 붙은 메타데이터 값인 *속성*을 가질 수 있다. 데이터셋은 기본적으로 연속으로 저장된다. 라이브러리가 언제나 통째로 읽고 쓰는 같은 크기의 블록인 *청크* 배치는 압축과, 자랄 수 있는 데이터셋에 필수다. 사람의 시연에서 배우는 일을 다룬 벤치마크 **robomimic**은 데이터셋마다 HDF5 파일 하나를 쓰고, 시연마다 그룹 하나를 둔다. P6의 실행은 거기서 시연 하나가 되어 `u`가 `actions`에 $(12{,}000, 1)$ 배열로, 카운트가 `obs` 아래에 놓일 것이다. 벤치마크가 무엇을 재는지는 [[01-canonical-papers/notes/4-vla/robomimic|robomimic]]을 본다.

**Parquet.** Apache Parquet은 열 지향 파일 형식이다. 파일은 하나 이상의 *행 그룹*을 담고, 행 그룹은 열마다 정확히 하나씩 파일 안에서 연속인 *열 청크*를 담으며, 열 청크는 인코딩과 압축의 나눌 수 없는 단위인 *페이지*로 나뉜다. 파일은 네 바이트 `PAR1`으로 시작하고 끝나며, 메타데이터 — 그중에는 각 열 청크가 어디서 시작하는지가 있다 — 는 데이터 뒤에 쓰인다. 그래서 작성기는 한 번에 흘려 쓸 수 있고 독자는 꼬리말부터 읽는다. **LeRobot**의 데이터셋 형식 3.0판이 이 위에 서 있다. 프레임(상태, 행동, 타임스탬프)은 파일마다 에피소드 여럿을 담는 Parquet 파일에, 스키마와 프레임 속도는 `meta/info.json`에, 정규화 통계는 `meta/stats.json`에 두고, 카메라 스트림은 MP4 비디오다.

> [!note]- 더 깊이 · Deeper
> **두 데이터셋 배치의 전체 모습.** *robomimic*: 그룹 `data`의 속성이 전체 샘플 수와, `env_args`에 JSON 문자열로 적은 환경 메타데이터를 준다. 그 아래 시연마다 그룹 하나 — `demo_0`, `demo_1`, … — 가 있고, 각각 속성 `num_samples`와 shape $(N, A)$의 데이터셋 `actions`, `rewards`, `dones`, `states`, 그리고 관측 키마다 데이터셋 하나를 담는 그룹 `obs`와 `next_obs`를 갖는다. 그리고 `mask` 그룹의 필터 키가 train, validation 같은 부분집합에 속한 시연을 나열한다. *LeRobot 3.0판*: 프레임 데이터는 `data/chunk-000/file-000.parquet` 아래에 있고 파일마다 기본 상한이 100 MB다. 에피소드마다의 기록 — 길이, 과제, 각 에피소드의 행을 되찾는 오프셋 — 은 `meta/episodes/` 아래 Parquet으로, 경로 템플릿은 스키마 옆 `meta/info.json`에 있고, MP4 파일은 카메라마다 한 벌이다. 3.0판은 2판의 에피소드당 파일 하나를 파일당 에피소드 여럿으로 바꾸어, 파일 시스템에 더 적고 더 큰 파일을 둔다.

**MCAP.** MCAP은 ROS 2 Iron Irwini(2023년 5월)부터 rosbag2의 기본 저장 형식이고, 그 릴리스가 이전 기본값 sqlite3를 대체했다. 그래서 Jazzy의 `ros2 bag record`가 쓰는 것도 이것이다([[04-robotics/ros2/debugging-data-reproducibility|25.10 §7]]). 파일은 매직 바이트 `0x89 M C A P 0 \r \n` 뒤에 레코드의 나열이 오는 구조다. 레코드는 1바이트 opcode, uint64 길이, 내용이고, 모두 리틀 엔디언이다. *Schema* 레코드는 메시지 타입이 어떻게 인코딩되는지, *Channel* 레코드는 토픽이 어느 스키마를 쓰는지 말하고, *Message* 레코드는 채널 id(uint16), 순번(uint32), 기록 시각과 발행 시각(각각 uint64 나노초), 그리고 직렬화된 메시지를 담는다. 레코드는 zstd나 lz4로 압축한 *청크*로 묶이고 시각으로 찾아가도록 색인될 수 있으며, 그 색인을 담는 요약 절은 선택이고 끝에 쓰인다. 레코드마다 자기 길이를 밝히므로, 독자는 색인 없이도 데이터 절을 앞에서부터 따라갈 수 있다.

영어 절의 코드가 틱 2407을 MCAP Message 레코드로 싸고 시간당 크기를 계산한다. 출력은 다음과 같다.

```text
MCAP message record: 51 bytes, 31 of them framing
  1 sample(s) per message: 36.72 MB/h, framing 60.78%
200 sample(s) per message: 14.51 MB/h, framing 0.77%
bytes read for u alone: row layout 240000, column layout 96000
```

메시지 레코드는 페이로드 앞에 $1+8+2+4+8+8=31$바이트를 치른다. P6의 샘플 하나하나가 20바이트짜리 메시지라면 틀이 파일의 $61\%$, 색인도 넣기 전에 $14.40$ 대신 $36.72\,\mathrm{MB/h}$다. 메시지 하나에 샘플 $200$개를 묶으면 $0.77\%$다. 실제 ROS 2 메시지는 보통 이 20바이트보다 크므로 — P6의 것이라면 스탬프와 프레임 id를 담은 `Header`가 붙는다([[04-robotics/ros2/nodes-topics-messages|25.2 §4]]) — 틀의 몫은 더 작다. 요점은 계산이다. 메시지당 고정 비용은 데이터 속도가 아니라 메시지 속도로 치른다.

> **열 지향 배치의 정의.** **열 지향 배치**(columnar layout)는 *표의 바이트를 늘어놓는 방식*으로, 열 하나의 값을 모두 함께 저장한다. 레코드의 필드가 함께 놓이는 행 배치와 반대이고, 표가 아니라 파일의 성질이다. 조건은 넷이다. $n$개 행과 $m$개의 **타입 있는 열**로 된 표가 있다. 각 열의 값이 적어도 행 그룹 안에서는 **연속**이다. 타입·인코딩·압축 같은 **열마다의 메타데이터**가 꼬리말에 있다. 그리고 독자가 **데이터를 읽기 전에 열을 고른다.** 집합 $S$의 열을 읽으면
>
> $$B^{\text{row}}=n\sum_{i=1}^{m}w_i,\qquad B^{\text{col}}(S)=n\sum_{i\in S}w_i$$
>
> 바이트를 압축 전에 읽는다. $w_i$는 열 $i$의 폭이다. 행 배치는 건너뛰려는 열을 원하는 열과 섞어 두기 때문이다.
>
> - **예**: P6의 명령만으로 학습하는 로더는 열 지향 파일에서 $12{,}000\times8=96{,}000$바이트를 읽는다. packed 레코드 파일이라면 $240{,}000$바이트를 모두 읽어야 하니, 그 $40\%$다. 한 시간이면 $5.76$ 대 $14.4\,\mathrm{MB}$다.
> - **비예**: MCAP. bag은 기록된 순서대로 온전한 메시지가 흘러가는 것이고, 일부러 고른 행 배치다. 기록기는 메시지가 도착하는 대로 덧붙이고 재생기는 시간 순서로 다시 내보내며, 토픽 하나의 필드 하나를 읽으려 해도 그 토픽의 메시지를 모두 디코딩해야 한다.
> - **왜 중요한가**: 로봇은 행을 기록하고 학습 파이프라인은 열을 읽는다. 학습 코드의 데이터셋 형식 — LeRobot의 Parquet, robomimic의 키마다 데이터셋 하나 — 이 기록기의 형식이 아닌 이유가 이것이다.

### 9. Markdown: CommonMark, 표, front matter, 이 위키의 수식

*한 문장으로:* Markdown은 이 위키와 대부분의 연구 노트를 쓰는 방식 — 사람이 텍스트로 읽고 Git이 줄 단위로 diff하는 글 — 이고, 이 위키의 페이지 안에 든 세 형식, 곧 front matter, 표, 수식에는 저마다 물리는 규칙이 있다.

Markdown은 가벼운 마크업을 얹은 텍스트다 — 제목은 `#`, 강조는 `*`, 문단 사이는 빈 줄 — 그리고 이 위키의 모든 페이지가 Markdown으로 쓰여 있다. 핵심은 **CommonMark**(0.31.2판, 2024년 1월)가 명세하는데, 여기에는 표가 없다. 표는 CommonMark의 엄격한 상위 집합인 **GitHub Flavored Markdown**(GFM)에서 온다. 헤더 행, 하이픈으로 된 구분 행(콜론이 열마다의 정렬을 정한다), 데이터 행으로 되어 있고, 셀은 `|`로 가르며 셀 안의 `|`는 `\|`로 쓴다. 이 위키는 Quartz로 빌드되고, 그 설정 `quartz.config.yaml`은 GFM, 위키링크와 `> [!note]` 같은 콜아웃을 주는 Obsidian 계열 확장, 그리고 달러 기호 사이의 수식을 그리는 KaTeX를 켠다. 달러 하나면 문장 속 수식, 둘이면 따로 선 수식이다.

이 위키의 세 부분은 그 자체로 형식이다.

- **Front matter.** 페이지 맨 위 두 `---` 줄 사이의 블록은 YAML(§4) — `title`, `tags`, `study-depth` 같은 것 — 이고 Markdown이 전혀 아니다. CommonMark에서 텍스트 한 줄 아래의 `---`는 제목이 된다. setext 밑줄이 주제 구분선보다 우선하기 때문이다. 그래서 사이트 생성기는 Markdown 파서가 보기 전에 front matter를 떼어 내야 한다. YAML이므로 §4를 따른다. 제목이 `1.10`이면 float $1.1$이 되고, `: `가 든 제목에는 따옴표가 필요하다.
- **결과 표.** Markdown 표는 숫자를 보여 주는 것이지 숫자의 출처가 아니다. 이 위키의 Tier A 페이지에서는 게시한 모든 표가 게시한 코드의 출력이어야 하고, §10이 그 규율을 따른다. 손으로 친 표는 숫자와 그 계산이 서로 멀어지는 자리다.
- **풀이 옆의 강조.** CommonMark는 `**`가 굵은 글씨를 닫을 수 있는지를 그 양옆 글자로 정한다. `)` 같은 구두점 뒤의 `**`는 공백이나 구두점이 뒤따를 때만 닫는다. 그래서 `**용어(term)**이`는 별표가 그대로 보인다. 별표 앞에 `)`가, 뒤에 조사 `이`가 오기 때문이다. 별표 앞에 글자가 오는 `**용어**(term)이`는 굵게 그려진다. 이 위키의 콘텐츠 검사가 앞의 꼴을 거부하고, 아래 콜아웃이 규칙을 적고 돌려 본다.

> [!note]- 더 깊이 · Deeper
> **오른쪽 붙음 규칙, 돌려 보기.** `*`나 `_`의 묶음은 유니코드 공백 뒤에 오지 않고, 구두점 뒤에 오지 않거나 구두점 뒤에 오되 공백이나 구두점 앞에 올 때 *오른쪽 붙음*(right-flanking)이며, `**`는 오른쪽 붙음일 때만 굵은 글씨를 닫을 수 있다. 줄의 처음과 끝은 공백으로 치고, 구두점은 유니코드 범주 P와 S를 뜻한다(CommonMark §6.2). 묶음 앞과 뒤의 글자를 $b$와 $a$라 하면
>
> $$R(b,a)=\neg W(b)\ \wedge\ \big(\neg P(b)\ \vee\ W(a)\ \vee\ P(a)\big)$$
>
> 이고, $W$는 "공백이다", $P$는 "구두점이나 기호다"이다. 그래서 닫는 괄호 뒤의 `**`는 공백이나 다른 구두점이 뒤따를 때만 닫는다. 영어 절의 코드가 세 문자열의 마지막 `**`에 이 판정을 적용한다. 출력은 다음과 같다.
>
> ```text
> before '어', after '(' -> closes: True
> before ')', after '이' -> closes: False
> before 'm', after 's' -> closes: True
> ```
>
> 둘째 경우에서 닫는 별표는 구두점인 `)` 뒤에, 공백도 구두점도 아닌 `이` 앞에 있으므로 $R$이 거짓이 되고, 독자는 별표 네 개를 그대로 본다. `**term**s`는 $b$가 글자 `m`이라서 닫힌다.

**이 페이지의 형식을, 형식으로서.** Markdown은 여기 나온 형식 중 가장 적게 약속한다. 타입도 스키마도 없고, 뜻은 렌더러의 확장에 달렸다. 그래도 노트에는 알맞은 형식이다. 사람이 텍스트로 읽고 Git이 줄 단위로 diff하기 때문이다. Markdown을 믿을 만하게 만드는 것은 CSV를 믿을 만하게 만드는 것과 같다. 파일 밖에 적어 둔 규칙과, 그것을 강제하는 검사다.

### 10. 실습: 실행 하나, 파일 여덟 개, 출력 소수 자릿수 스윕

고정된 실행 위의 네 부분이다. 영어 절의 코드가 그것이다. 0부는 실행을 만든다 — 시계, 목표, 카운트에 건 PD 제어기, 반암시적 오일러로 전진하는 카트 — 그리고 계산 절의 샘플과 그 샘플이 다섯 형식에서 차지하는 바이트를 출력한다. 1부는 실행을 파일 대신 `io.BytesIO`와 `io.StringIO`를 써서 메모리 안에 여덟 가지로 쓰고, 각각을 제 디코더로 다시 읽어 크기, 시간당 크기, 열마다의 최악 왕복 오차를 출력한다. 2부는 찍는 소수 자릿수 $d$를 $0$부터 $9$까지 훑고 `%.17g`, `repr`와 견준다. 3부는 시간 열의 타입 네 가지가 정수 나노초 시계에서 무엇을 남기는지 묻는다. 시간을 재는 곳도 난수도 없으므로 NumPy 2가 있는 어느 기계에서나 출력이 같다.

**샘플**, 0부: 틱 2407, $t=1790000012.0351205\,\mathrm{s}$, $1042$ 카운트, $u=-1.9578125000000002\,\mathrm{N}$, $120{,}562\,\mathrm{ns}$ 늦게 찍힘. 바이트는 struct로 $20$, `repr` CSV 줄로 $44$, `%.3f`로 $27$, JSON 객체로 $67$(객체 사이에 $+2$), `np.savetxt`로 $76$이다. 실행 전체에서 카운트는 $205$에서 $1218$까지, 명령은 $-4.252$에서 $4.013\,\mathrm{N}$까지다.

**파일 여덟 개**, 1부:

| 파일 | 바이트 | 샘플당 바이트 | struct 대비 | 시간당 MB | 시간 최악 오차 (s) | 명령 최악 오차 (N) | 카운트 정확 |
|---|---:|---:|---:|---:|---:|---:|---|
| struct `'<did'`, 헤더 없음 | 240,000 | 20.00 | 1.00 | 14.40 | 0 | 0 | 예 |
| `.npy`, 구조화 레코드 | 240,192 | 20.02 | 1.00 | 14.41 | 0 | 0 | 예 |
| `.npy`, float64 $N\times3$ | 288,128 | 24.01 | 1.20 | 17.29 | 0 | 0 | 예 |
| `np.savetxt` 기본값 | 906,001 | 75.50 | 3.78 | 54.36 | 0 | 0 | 예 |
| CSV, `repr` | 504,340 | 42.03 | 2.10 | 30.26 | 0 | 0 | 예 |
| CSV, `%.3f` | 308,700 | 25.73 | 1.29 | 18.52 | 0.0002 | 0.0005 | 예 |
| JSON, 샘플마다 객체 | 804,329 | 67.03 | 3.35 | 48.26 | 0 | 0 | 예 |
| JSON, 열마다 배열 | 540,355 | 45.03 | 2.25 | 32.42 | 0 | 0 | 예 |

**스윕**, 2부. 두 float를 같은 형식으로 찍었다.

| 찍은 모양 | 샘플당 바이트 | 시간 최악 오차 (s) | 시간 정확 | 명령 최악 오차 (N) | 명령 정확 |
|---|---:|---:|---|---:|---|
| $d=0$ | 17.73 | 5.000e-01 | 아니오 | 4.969e-01 | 아니오 |
| $d=1$ | 21.73 | 5.000e-02 | 아니오 | 5.000e-02 | 아니오 |
| $d=2$ | 23.73 | 5.000e-03 | 아니오 | 5.000e-03 | 아니오 |
| $d=3$ | 25.73 | 2.000e-04 | 아니오 | 5.000e-04 | 아니오 |
| $d=4$ | 27.73 | 5.007e-05 | 아니오 | 5.000e-05 | 아니오 |
| $d=5$ | 29.73 | 5.007e-06 | 아니오 | 5.000e-06 | 아니오 |
| $d=6$ | 31.73 | 4.768e-07 | 아니오 | 5.000e-07 | 아니오 |
| $d=7$ | 33.73 | 0 | 예 | 5.000e-08 | 아니오 |
| $d=8$ | 35.73 | 0 | 예 | 1.554e-14 | 아니오 |
| $d=9$ | 37.73 | 0 | 예 | 1.554e-14 | 아니오 |
| `%.17g` | 42.46 | 0 | 예 | 0 | 예 |
| `repr` | 42.03 | 0 | 예 | 0 | 예 |

**시간 열의 타입**, 3부:

| 시간 저장 방식 | 12,000개 중 서로 다른 시각 | 시계에 대한 최악 오차 |
|---|---:|---:|
| float64, 1970년부터의 초 | 12,000 | 1.19e-07 s |
| float32, 1970년부터의 초 | 1 | 60 s |
| float32, 실행 시작부터의 초 | 12,000 | 2.02e-06 s |
| int64, 1970년부터의 나노초 | 12,000 | 정확. binary64로 읽는 JSON 독자에게는 128 ns |

**표 읽기.** 앞 절들이 예측한 것 다섯을 이제 센다.

- **이진이 바닥이고, 텍스트는 읽기 쉬움의 값을 치른다.** packed 레코드는 샘플당 $20$바이트이고 `.npy` 파일은 $192$바이트 헤더만 더한다. float64 행렬은 정수 열을 float64로 저장하느라 샘플당 $4$바이트를 더 낸다. 전체 정밀도의 CSV는 $2.10$배, JSON은 열마다 배열이면 $2.25$배, 샘플마다 객체면 $3.35$배, `np.savetxt` 기본값은 $3.78$배이고, 모두 정확하다.
- **싼 텍스트 파일이 손실 있는 파일이다.** `%.3f`는 이진의 $1.3$배 아래인 유일한 텍스트 파일이고, 되돌아오지 않는 유일한 파일이기도 하다. 시간 $0.2\,\mathrm{ms}$와 명령 $0.5\,\mathrm{mN}$이 사라졌다.
- **자릿수가 주는 정확함은 파일 단위가 아니라 열 단위다.** 시간은 계산 절이 간격에서 유도한 대로 $d=7$에서 정확해진다. 명령은 어떤 고정 $d$에서도 정확해지지 않고, $d=8$부터는 오차가 $1.554\times10^{-14}\,\mathrm{N}$에 머문다 — $-1.9578125000000002$ 같은 float의 마지막 비트들이다. 두 열을 모두 정확하게 하는 것은 유효 숫자, 곧 `%.17g`나 `repr`뿐이고, `repr`는 통하는 가장 짧은 문자열에서 멈추므로 더 적은 바이트로 해낸다.
- **한계는 한계일 뿐이다.** $d=3$에서 시간의 최악 오차는 $200\,\mu\mathrm{s}$로 $500\,\mu\mathrm{s}$ 안에 넉넉히 든다. 명목 시각이 모두 밀리초의 정수배라서 잘려 나가는 것이 늦음뿐이기 때문이다. $d=4$와 $5$에서는 $50.07$과 $5.007\,\mu\mathrm{s}$로, float 격자 때문에 $\tfrac12 10^{-d}$를 살짝 넘는다. §2의 식이 허용하는 만큼이다.
- **열의 타입은 정밀도의 결정이다.** 1970년부터의 float32 초는 실행을 한 순간으로 만든다. 실행 시작부터의 float32 초는 $2\,\mu\mathrm{s}$를, 1970년부터의 float64 초는 $0.12\,\mu\mathrm{s}$를 남긴다. 정수 나노초는 모든 것을 남긴다 — double 기반 JSON 독자가 그것을 $128\,\mathrm{ns}$로 반올림하기 전까지는.

### 11. 이 페이지가 다루지 않는 것

이 파일들을 둘러싼 ROS 2 장치는 그것이 사는 곳에서 가르친다. 파라미터와 파라미터 파일은 [[04-robotics/ros2/services-actions-parameters|25.3 §6–§7]], launch 파일과 네임스페이스가 붙은 파라미터 키는 [[04-robotics/ros2/workspaces-packages-launch|25.4 §9–§11]], URDF와 Xacro는 [[04-robotics/ros2/describing-a-robot|25.6]], bag의 기록·검사·재생은 [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6–§8]]이다. §2에 필요한 것 너머의 부동소수점 형식 — fp16, bf16, 양자화된 가중치 — 은 [[03-deep-learning/foundations/training-at-scale|1.3 §4]]다. 주장이 서려면 데이터셋에 무엇이 있어야 하는지 — 분할, 출처, 설정 스냅숏 — 는 [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성 §7]]과 [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]]이다. 이미지와 비디오(PNG, JPEG, LeRobot 데이터셋의 MP4 스트림), 압축 알고리즘, 데이터베이스, 프로토콜 버퍼, ROS 2 메시지 안의 CDR 직렬화는 이 페이지 밖이고, §8이 문서에 근거해서만 설명한 HDF5와 Parquet 라이브러리 자체도 그렇다. 이 파일들 둘레의 도구는 이 트랙의 다른 페이지다. 하루치 파일을 로봇에서 복사해 오는 법은 [[02-foundations/tools/linux-shell|12.1 §8]], 작은 파일은 버전으로 관리하고 큰 파일은 체크섬으로 이름 붙이는 법은 [[02-foundations/tools/git-research-code|12.2 §6]], 그것을 배열로 읽는 법은 [[02-foundations/tools/python-research-code|12.3 §3]], 표의 숫자를 데이터가 받쳐 주는 자릿수로 찍는 법은 [[02-foundations/tools/latex-figures-references|12.6 §9]], CAD 프로그램이 쓰는 STEP과 STL 파일은 [[02-foundations/tools/mechanical-design-fabrication|12.9 §2]]다.

### 읽고 나면

- [ ] 형식의 다섯 약속 — 타입, 스키마, 정밀도, 주석, 스트리밍 — 을 대고, JSON, YAML, XML, CSV, `.npy`, HDF5, Parquet, MCAP을 그 위에 놓는다.
- [ ] 레코드의 바이트를 이진과 텍스트로, 샘플당과 시간당으로 세고, 이진 크기는 고정인데 텍스트 크기는 왜 아닌지 말한다.
- [ ] 소수 $d$째 자리까지 찍은 숫자의 왕복 오차에 한계를 매기고, float 간격에서 정확해지는 $d$를 찾고, $0$ 근처를 지나는 신호에는 왜 유효 숫자가 필요한지 말한다.
- [ ] 사이드카를 올바른 JSON으로 쓰고, Python이 쓰지만 RFC 8259가 금지하는 것과 모든 JSON 독자가 정확히 간직하는 정수의 범위를 댄다.
- [ ] plain YAML 스칼라를 YAML 1.2 core 스키마, PyYAML, ROS 2의 rcl 파서로 각각 결정하고, 셋 중 무엇이 기동 시 파라미터 파일을 읽고 무엇이 `ros2 param set`을 받는지 말한다.
- [ ] XML 파일이 형식이 올바르려면 무엇이 필요한지, 형식이 올바른 URDF가 왜 여전히 틀린 숫자를 담을 수 있는지 말한다.
- [ ] 정확히 되돌아오는 CSV 파일을 쓰고, 헤더가 말하지 못하는 것을 댄다.
- [ ] 필드 폭에서 이진 레코드를 packed와 aligned로 배치하고, `.npy` 헤더를 읽고, 틀린 바이트 순서나 배치가 무엇을 만드는지 말한다.
- [ ] HDF5, Parquet, MCAP이 데이터를 어떻게 조직하는지, robomimic, LeRobot, rosbag2가 각각 무엇을 쓰는지, MCAP 메시지 하나가 틀에 얼마를 치르는지 말한다.
- [ ] `**용어(term)**이`가 왜 별표와 함께 그려지는지, 이 위키의 front matter, 표, 수식이 어디서 오는지 설명한다.

### 스스로 점검

1. 동료의 로그가 1970년부터 센 초 단위 시간 열을 `%.3f`로 찍는다. 파일은 무엇을, 최대 얼마나 잃었는가? 몇 자리였다면 정확히 남았겠는가?
2. 실행 042의 시간 열은 소수 일곱째 자리에서 정확해진다. 명령 열은 왜 어떤 고정 자릿수에서도 정확해지지 않으며, 작성기는 무엇을 써야 하는가?
3. P6 파라미터 파일의 `control_period: 5e-3`는 제어기를 $200\,\mathrm{Hz}$로 띄우는데, `ros2 param set /cart/controller control_period 5e-3`는 거부된다. 왜인가?
4. 사이드카가 시각 하나를 1970년부터 센 정수 나노초로 저장했는데, 숫자를 double로 담는 JSON 독자를 쓴 대시보드가 그것을 $78\,\mathrm{ns}$ 어긋나게 보여 준다. 어느 독자가 틀렸고, 대신 무엇을 쓰겠는가?
5. P6 샘플이 든 $240{,}000$바이트 파일이 헤더도 메모도 없이 도착했다. 읽기 전에 필요한 세 가지 사실은 무엇이고, 정렬을 잘못 짐작하면 무슨 일이 생기는가?
6. 같은 데이터에서, P6를 기록하기에는 왜 MCAP이 맞고 학습하기에는 왜 Parquet이 좋은가?
7. 한국어 페이지에 `**용어(term)**이`가 별표째 보인다. 어떤 규칙을 어겼고, 고치는 법은 무엇인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 밀리초 아래의 모든 것, 곧 틱의 늦음을 잃었다. 한계로는 최대 $0.5\,\mathrm{ms}$, 실행 042에서는 $0.2\,\mathrm{ms}$다. 그래서 지터가 지워진 파일은 완벽하게 주기적으로 보인다. 일곱 자리면 정확히 남는다. $10^{-7}\,\mathrm{s}$가 $t_0$ 근처의 float64 간격 $2^{-22}\,\mathrm{s}=0.238\,\mu\mathrm{s}$보다 촘촘하고, 간격의 절반 안에 있는 소수는 같은 float로 파싱되기 때문이다.
> 2. float의 간격은 크기에 비례한다. 시간은 늘 $1.79\times10^9\,\mathrm{s}$ 근처에 있으므로 계단 하나가 모든 샘플에 맞는다. 명령은 $\pm4\,\mathrm{N}$ 범위를 오가며 $0$ 근처를 지나고, 거기서는 간격도 값을 따라 줄어들므로 어떤 고정 $d$도 일부 값을 어긋나게 남긴다 — 실행 042에서 $d=8$과 $9$일 때 $1.554\times10^{-14}\,\mathrm{N}$이다. 유효 숫자는 값의 크기를 따라가므로 `json`과 `csv`의 기본값인 `repr`나 `%.17g`를 쓴다. 유효 숫자 17개는 언제나 float64 하나를 가려낸다.
> 3. 독자가 둘이다. 기동할 때 노드는 rcl의 C 파서로 파일을 읽고, 이 파서는 `5e-3`을 `strtod`에 넘겨 double $0.005$를 얻는다. `ros2 param set`은 값을 PyYAML로 파싱하는데, 그 YAML 1.1 실수 패턴은 소수점을 요구하므로(지수가 있으면 부호도) `5e-3`은 문자열 `'5e-3'`로 남고, double 파라미터는 문자열을 거부한다. `0.005`로 쓴다.
> 4. 둘 다 틀리지 않았다. 파일은 올바른 JSON이지만 $1.79\times10^{18}$은 RFC 8259가 모든 구현에서 정확하다고 밝히는 범위 $2^{53}-1\approx9.0\times10^{15}$을 넘고, 숫자를 double로 담는 독자는 $256\,\mathrm{ns}$ 간격으로 반올림한다. 시각은 초와 나노초 두 정수로, 또는 실행 시작부터의 나노초($\le6.0\times10^{10}$)로, 또는 문자열로 쓴다.
> 5. 바이트 순서, 필드의 순서와 폭, 레코드가 packed인지 aligned인지 — §7의 배치다. packed 20바이트 파일을 aligned 24바이트 레코드로 짐작하면, 공교롭게 $24$로 나누어떨어지는 $240{,}000$바이트가 쓰레기 레코드 $10{,}000$개가 되고, 첫 명령은 $-8.6\times10^{168}\,\mathrm{N}$이며, 오류는 없다.
> 6. 기록은 온전한 메시지를 시간 순서로 덧붙이는 일이고, MCAP은 레코드 하나씩 $31$바이트의 틀을 붙여 기록하며 색인 없이도 앞에서부터 읽힌다. 학습은 많은 에피소드의 몇 개 열을 읽는 일이고, 열 지향 파일은 나머지를 건드리지 않고 그것을 내준다 — 실행 042에서 명령만이면 $240{,}000$바이트 중 $96{,}000$바이트다.
> 7. CommonMark의 오른쪽 붙음 규칙이다. 닫는 `**`가 구두점 `)` 뒤에, 공백도 구두점도 아닌 `이` 앞에 있으므로 굵은 글씨를 닫지 못한다. 풀이를 바깥으로 옮겨 `**용어**(term)이`로 쓴다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6 Lab Plants]]만 쓴다. 대상은 P6의 실행 042이고, 모든 문제가 손잡이 하나를 바꾸므로 — 시계의 타입, 넷째 열, 손으로 고친 설정, bag의 묶음 크기 — 페이지의 숫자를 그대로 옮길 수 없다.

1. **그리기.** 과제 3의 변형 로그에 대한 그림을 그린다. 시간을 실행 시작부터의 int64 나노초로, 비전 목표 $g$를 넷째 float64 열로 둔 틱 2407을 packed struct `'<qidd'`, 정렬된 레코드, `repr` CSV 줄 하나, JSON 객체 하나로, 바이트당 $7$ px라는 한 척도로 그리고, 막대마다 그 바이트와 과제 3에서 얻은 실행 전체의 시간당 크기를 적는다.
2. **유도.** (a) 변형 레코드(`t_ns` int64, `counts` int32, `u` float64, `g` float64)의 packed와 aligned 오프셋과 크기를 §7의 식으로 구하라. 틱 2407의 CSV 줄 — $t_{\text{ns}}=12{,}035{,}120{,}562$, $1042$ 카운트, 위의 명령, $g=0.499$ — 을 쓰고 그 바이트와 JSON 객체의 바이트를 세고, packed 레코드의 시간당 메가바이트를 구하라. (b) 실행 시작부터의 정수 나노초 시각은 왜 모든 JSON 독자에게 정확하고 1970년부터의 것은 그렇지 않은가? 두 최댓값을 $2^{53}-1$과 비교하라. float64 "1970년부터의 초" 열은 몇 년에 $0.238\,\mu\mathrm{s}$ 간격을 잃고, 간격은 얼마가 되는가? (c) 실행 042의 float64 시간을 소수 $d$째 자리까지 찍을 때, 모든 시각을 주기의 $1\%$ 안에 두는 가장 작은 $d$를 §2의 한계로 구하고 §10의 스윕과 대조하라. (d) 손으로 고친 파라미터 파일에 `kd: 4e1`, `motion_axis: Y`, `device_id: 0755`, `start: 9:30`, `enable: "on"`이 있고, 각각 double, 문자열, 정수, 문자열, 불리언으로 선언되어 있다. 각 값을 YAML 1.2 core 스키마, PyYAML, rcl로 결정하고, 노드가 기동할 때 실패하는 것, `ros2 param load`에서 실패하는 것, 조용히 틀리게 들어가는 것을 가려라. (e) 기록기가 실행 042를 MCAP 메시지 하나에 샘플 $50$개씩 담아 기록한다. 시간당 몇 메가바이트이고, 그중 틀의 몫은 얼마인가?
3. **실행.** 영어 절 템플릿의 `?`를 채우고 §10의 실습 뒤에 돌린다. 정수 시계와 넷째 열인 목표를 둔 실행 042의 로그다. struct, 정렬된 레코드, `repr` CSV, JSON 객체의 샘플당 바이트와 시간당 메가바이트, 가장 큰 시각이 binary64 JSON 독자에게 정확한지, 그리고 `%.3f`, `%.6f`, `%.17g`, `repr` 각각의 샘플당 바이트, 시간이 정확한지, $u$와 $g$의 최악 오차를 보고하라. 각각을 §10과 비교하라.

> [!note]- 그리는 법 · How to draw it
> - 모든 막대에 한 척도를 쓰고 — 여기서는 바이트당 $7$ px — 아래에 바이트 눈금자를 둔다. 바이트 하나의 길이가 같아야 서로 다른 형식의 막대를 견줄 수 있다.
> - 이진 막대는 오프셋에서 필드로 나누고, 좁은 필드 뒤에 넓은 필드가 오는 곳에는 패딩을 따로 된 점선 토막으로 그린다. 변형에서는 `counts` 뒤의 $4$바이트다.
> - 텍스트 막대 안에는 실제 글자를, 바이트 하나에 글자 하나씩, 줄바꿈과 JSON 객체 사이의 구분자까지 적는다. 어림하지 말고 센다.
> - 막대마다 헷갈리면 안 되는 숫자 둘을 적는다. 이 샘플의 바이트, 그리고 실행 전체의 평균 시간당 크기다. 텍스트 길이는 샘플마다 다르기 때문이다.
> - 어느 막대가 정확히 되돌아오는지 표시한다. 변형에서 정수는 어떤 형식에서든 정확하고, float는 `repr`나 `%.17g`에서만 정확하다.

> [!tip]- 정답 · Solutions
> 1. 바이트당 $7$ px의 막대 넷. packed `'<qidd'`: $28$바이트, 오프셋 $0, 8, 12, 20$에 `t_ns` $8$, `counts` $4$, `u` $8$, `g` $8$, $20.16\,\mathrm{MB/h}$. aligned: $32$바이트, `u`가 $16$에서, `g`가 $24$에서 시작하도록 `counts` 뒤에 패딩 $4$바이트, $23.04\,\mathrm{MB/h}$. CSV: `12035120562,1042,-1.9578125000000002,0.499`와 줄바꿈으로 $43$바이트, 실행 평균은 샘플당 $47.76$바이트, $34.38\,\mathrm{MB/h}$. JSON: `{"t_ns": 12035120562, "counts": 1042, "u": -1.9578125000000002, "g": 0.499}`는 $75$자에 구분자 $2$를 더해 $77$바이트, 실행 평균은 $81.75$, $58.86\,\mathrm{MB/h}$. 값에 따라 길이가 변하는 것은 텍스트 막대뿐이고, 넷 모두 정확히 되돌아온다.
> 2. (a) packed: $o=0, 8, 12, 20$, $S=28$. $a=8, 4, 8, 8$로 aligned: $o_2=\lceil 8/4\rceil 4=8$, $o_3=\lceil 12/8\rceil 8=16$, $o_4=\lceil 24/8\rceil 8=24$, $S=\lceil 32/8\rceil 8=32$. CSV 줄은 $11+1+4+1+19+1+5+1=43$바이트, JSON 객체는 $75$, 구분자와 함께 $77$이다. packed의 시간당 크기는 $28\times720{,}000=20{,}160{,}000$바이트, $20.16\,\mathrm{MB}$. (b) 실행 시작부터의 가장 큰 시각은 $59{,}995{,}152{,}978\approx6.0\times10^{10}$으로 $2^{53}-1=9{,}007{,}199{,}254{,}740{,}991$보다 약 $150{,}000$배 작으므로 모든 double이 정확히 담는다. 1970년부터의 시각은 $1.79\times10^{18}$로 그보다 약 $199$배 크고, 거기서 double은 $256\,\mathrm{ns}$ 간격이다. 1970년부터의 초의 float64 간격은 $2^{30}\,\mathrm{s}$(2004년 1월 10일)부터 $2^{31}\,\mathrm{s}$까지의 모든 날짜에서 $2^{-22}\,\mathrm{s}$이고, $2^{31}\,\mathrm{s}$는 2038년 1월 19일 03:14:08 UTC다. 그때부터 간격은 $2^{-21}\,\mathrm{s}=0.477\,\mu\mathrm{s}$가 된다. (c) $5\,\mathrm{ms}$의 $1\%$는 $50\,\mu\mathrm{s}$다. 한계 $\tfrac12 10^{-d}+\tfrac12\,2^{-22}\,\mathrm{s}$는 $d=4$에서 $50.12\,\mu\mathrm{s}$로 살짝 넘고 $d=5$에서 $5.12\,\mu\mathrm{s}$이므로 $d=5$다. §10도 같다. $d=4$의 최악 오차는 $50.07\,\mu\mathrm{s}$로 주기의 $1.0014\%$ — 넘기게 만든 것은 float 격자의 $0.12\,\mu\mathrm{s}$다 — 이고, $d=5$에서는 $5.007\,\mu\mathrm{s}$다. (d) `4e1`: core float $40.0$, PyYAML 문자열 `'4e1'`, rcl float $40.0$. `Y`: 문자열, 문자열, rcl에서는 불리언 참. `0755`: core int $755$, PyYAML과 rcl int $493$(8진수). `9:30`: 문자열, PyYAML int $570$(60진수), rcl 문자열. `"on"`: 따옴표가 있으므로 셋 모두 문자열. 기동할 때(rcl) `motion_axis`는 문자열 파라미터에 불리언이라 실패하고, `enable`은 불리언 파라미터에 문자열이라 실패한다. `device_id`는 조용히 $493$으로 들어간다. PyYAML로 두 번 파싱하는 `ros2 param load`(§4)에서는 `kd`가 문자열이라 실패하고, `start`가 정수 $570$이라 실패하며, `device_id`는 역시 $493$이다. 뜻밖인 것은 `enable`이다. 첫 파싱이 따옴표를 벗기고, 둘째 파싱이 `on`을 불리언 참으로 읽으므로 들어간다. (e) $720{,}000/50=14{,}400$개 메시지, 페이로드 $14{,}400{,}000$바이트 위에 틀 $14{,}400\times31=446{,}400$바이트로 모두 $14{,}846{,}400$바이트, $14.85\,\mathrm{MB/h}$이고 틀은 $3.01\%$다.
> 3. 빈칸은 `T0 * 10 ** 9`, `"<qidd"`, `True`, `2 ** 53 - 1`, `len(csv4(fmt)) / N`, `np.abs(u_back - u).max()`, `np.abs(g_back - goal).max()`, `np.array_equal(g_back, goal)`이다. 출력은 영어 절의 정답 3과 같고, 요약하면:
>
>    | | 샘플당 바이트 | 시간 정확 | 명령 최악 오차 (N) | 목표 최악 오차 (m) | 목표 정확 |
>    |---|---:|---|---:|---:|---|
>    | `%.3f` | 28.54 | 예 | 5.000e-04 | 1.110e-16 | 아니오 |
>    | `%.6f` | 34.54 | 예 | 5.000e-07 | 1.110e-16 | 아니오 |
>    | `%.17g` | 54.13 | 예 | 0 | 0 | 예 |
>    | `repr` | 47.76 | 예 | 0 | 0 | 예 |
>
>    struct는 샘플당 $28.00$바이트, 정렬된 레코드는 $32$, `repr` CSV는 $47.76$, JSON 객체는 $81.75$이고, 시간당으로는 $20.16$, $34.38$, $58.86\,\mathrm{MB}$다. 가장 큰 시각 $59{,}995{,}152{,}978\,\mathrm{ns}$는 binary64 JSON 독자에게 정확하다. 정수 시계는 이진에서 float64 시간과 같은 $8$바이트이고 모든 형식에서 정확하며, 텍스트에서는 더 짧다. $18$자 대신 $11$자리라서, 변형의 `repr` CSV는 넷째 열을 싣고도 §10보다 샘플당 $5.7$바이트 길 뿐이다. 목표는 소수 셋째 자리 숫자처럼 보이지만 — $0.1$에 $0.001$의 배수를 더한 값 — `%.3f`로는 정확히 돌아오지 않는다. $0.30000000000000004$처럼 십진수에서 간격 하나만큼 떨어진 float가 섞여 있어서, 최악 오차가 $1.11\times10^{-16}\,\mathrm{m}$다. `%.17g`는 정확하지만 목표의 절반가량을 끝자리까지 다 쓰느라 — $0.1$이 `0.10000000000000001`이 된다(틱 2407의 $0.499$는 마침 `0.499`로 나온다) — `repr`의 $47.76$ 대신 $54.13$바이트를 치른다. `repr`가 정확하면서 가장 짧다. JSON 객체는 $81.75$바이트로 struct의 $2.92$배이고, §10의 $3.35$배와 비교된다.

### 출처

- RFC 8259, *The JSON Data Interchange Format*, 2017 ([rfc-editor.org/rfc/rfc8259](https://www.rfc-editor.org/rfc/rfc8259)) — 값 타입 여섯, NaN과 앞자리 0이 없는 숫자, 유일한 이름, UTF-8, $2^{53}-1$까지의 상호운용 정수.
- RFC 4180, *Common Format and MIME Type for CSV Files*, 정보 제공용, 2005 ([rfc-editor.org/rfc/rfc4180](https://www.rfc-editor.org/rfc/rfc4180)) — CRLF 레코드, 선택적 헤더, 따옴표와 두 번 쓰는 따옴표.
- *YAML 1.2.2*, 2021 ([yaml.org/spec/1.2.2](https://yaml.org/spec/1.2.2/))와 YAML 1.1 타입 저장소([yaml.org/type](https://yaml.org/type/index.html)) — 주석, 들여쓰기의 탭 금지, core·JSON 스키마, 1.1의 bool·int·float.
- PyYAML([pyyaml.org/wiki/PyYAML](https://pyyaml.org/wiki/PyYAML))과 그 [`resolver.py`](https://github.com/yaml/pyyaml/blob/main/lib/yaml/resolver.py) — "완전한 YAML 1.1 파서"와 암묵적 resolver. 6.0.1판은 §4의 표를 확인하는 데만 썼다.
- ROS 2 소스, Jazzy 브랜치: rcl의 [`parse.c`](https://github.com/ros2/rcl/blob/jazzy/rcl_yaml_param_parser/src/parse.c)(`get_value()`), rclpy의 [`parameter.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/parameter.py)(`get_parameter_value`, `str()`로 다시 파싱하는 `parameter_dict_from_yaml_file`), ros2cli의 `ros2param`, launch_ros의 [`node.py`](https://github.com/ros2/launch_ros/blob/jazzy/launch_ros/launch_ros/actions/node.py) — §4의 두 독자.
- ROS 2 문서, Jazzy 브랜치([ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — 노드 이름 아래 `ros__parameters`로 키를 잡은 파라미터 파일, Iron Irwini 릴리스 노트(2023년 5월부터 MCAP이 기본 bag 형식).
- Python 3 문서([docs.python.org](https://docs.python.org/3/)) — `json`, `csv`, `struct`, `xml.etree.ElementTree`, 부동소수점 튜토리얼과 "What's New in Python 3.2". CPython의 [`Lib/json/encoder.py`](https://github.com/python/cpython/blob/3.12/Lib/json/encoder.py)(`float.__repr__`).
- NumPy 문서([numpy.org/doc](https://numpy.org/doc/stable/)) — `numpy.lib.format`(`.npy` 헤더), `numpy.load`(`allow_pickle`), `numpy.savez_compressed`, `numpy.savetxt`(`'%.18e'`), 구조화 배열(`align=True`).
- W3C, *Extensible Markup Language (XML) 1.0*, 제5판, 2008 ([w3.org/TR/xml](https://www.w3.org/TR/xml/)) — 뿌리 요소 하나, 이스케이프, 주석, 유일하고 따옴표 친 속성.
- The HDF Group, *HDF5 문서*([support.hdfgroup.org](https://support.hdfgroup.org/documentation/hdf5/latest/_learn_basics.html)) — 그룹, 데이터셋, 속성, 연속 저장과 청크 저장.
- robomimic 문서([robomimic.github.io/docs](https://robomimic.github.io/docs/datasets/overview.html)) — HDF5 데이터셋 구조, `--config`로 넘기는 JSON 설정.
- Apache Parquet 문서([parquet.apache.org/docs](https://parquet.apache.org/docs/overview/))와 [`parquet.thrift`](https://github.com/apache/parquet-format/blob/master/src/main/thrift/parquet.thrift) — 행 그룹, 열 청크, 페이지, `PAR1`과 꼬리말 메타데이터.
- LeRobot([github.com/huggingface/lerobot](https://github.com/huggingface/lerobot)) — `docs/source/lerobot-dataset-v3.mdx`와 `src/lerobot/datasets/utils.py`: 3판 배치, 100 MB 데이터 파일, 옛 `meta/episodes.jsonl`.
- MCAP 명세([mcap.dev/spec](https://mcap.dev/spec)) — 매직 바이트, 레코드 틀, Schema·Channel·Message 레코드, 청크와 선택적 요약.
- *CommonMark Spec* 0.31.2, 2024 ([spec.commonmark.org/0.31.2](https://spec.commonmark.org/0.31.2/))와 *GitHub Flavored Markdown Spec* 0.29-gfm([github.github.com/gfm](https://github.github.com/gfm/)) — setext 제목, 오른쪽 붙음 구분자 묶음, 표.
- Hydra 문서([hydra.cc/docs](https://hydra.cc/docs/intro/)) — 합성, 명령줄 덮어쓰기, 실행마다의 `.hydra/config.yaml`.
- 이 위키의 `quartz.config.yaml` — GFM, Obsidian 계열, KaTeX 플러그인.

