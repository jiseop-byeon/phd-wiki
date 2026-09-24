---
title: "12.3 Python for Research Code"
tags: [foundations, tools, python]
study-depth: Working
wiki-support: Working
depth-goal: "On P6's one-hour log, set up an isolated and pinned Python environment, predict which operations alias, view or copy, vectorize an estimate and prove it equal to the loop, compute by hand how a float32, a float64 and an integer clock drift over a day and where a narrow counter wraps, make randomness replayable, and pin the result in a regression test."
mastery-when: "Raise when the thesis ships software that others must rerun — a released package, a dataset pipeline or a benchmark harness — or when numerical precision on an embedded controller carries a result."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]] (**P6**: $2048$ counts/m, the $200\,\mathrm{Hz}$ loop, the $50\,\mathrm{Hz}$ goal) · [[02-foundations/lab-kernel|0.7 Lab Kernel]] (§1's time vector, built from an integer index, and §5's blank-and-solve pattern) · [[02-foundations/algorithms/interview-code|11.7 Interview-Ready Code]] (§3's Python traps, and §5's broadcasting rule and assertions, which this page applies to P6 instead of repeating) · [[02-foundations/ml-practice|9. ML Practice]] (§4, why results are reported over several seeds). Python you already write — functions, lists, dicts, loops — and a terminal in which you can run `python3`. The Tier A lab in §10 needs NumPy and nothing else.
> [[02-foundations/lab-plants|0.6 Lab Plants]](**P6**: $2048$ counts/m, $200\,\mathrm{Hz}$ 루프, $50\,\mathrm{Hz}$ 목표) · [[02-foundations/lab-kernel|0.7 Lab Kernel]](정수 인덱스로 만드는 §1의 시간 벡터와 §5의 빈칸 채우기 방식) · [[02-foundations/algorithms/interview-code|11.7 Python·C++ 인터뷰용 코드]](§3의 Python 함정, §5의 broadcasting 규칙과 assertion. 이 페이지는 되풀이하지 않고 P6에 적용한다) · [[02-foundations/ml-practice|9. ML 실무]](§4, 결과를 여러 seed로 보고하는 이유). 이미 쓸 줄 아는 Python — 함수, 리스트, 딕셔너리, 반복문 — 과 `python3`를 돌릴 터미널. §10의 Tier A 실습에는 NumPy만 있으면 된다.

## English

*Stands on [[02-foundations/lab-plants|0.6 Lab Plants]] and [[02-foundations/lab-kernel|0.7 Lab Kernel]], and applies the Python habits of [[02-foundations/algorithms/interview-code|11.7 Interview-Ready Code]] to a robot's data. A later use of plant **P6**, which [[04-robotics/ros2/index|25. ROS 2]] runs and [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] gives noise; here P6 is data on disk — one hour of its log, as the analysis script on your workstation reads it.*

> [!note] Why this matters · 왜 배우는가
> This page is the floor beneath the physical-AI stack of [[07-research-program/index|research program §5]]: every layer's research code — the perception model, the planner, the learned policy and the analysis of its trials — is written in Python and runs on arrays, and in that section's worked instance, "Install that panel on the frame", it is where "detects contact" and "verifies completion" become numbers computed from logged counts and timestamps (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it those numbers go wrong with no error message: a float32 clock that drifts 34.58 s in an hour, a view that rewrites the raw log, a 16-bit counter that wraps, a seed that stops replaying when someone adds a plot. Every Tier A lab from block 1's [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics]] on runs in NumPy, and [[05-construction-robotics/imitating-contact|10. Imitating Contact §9]] trains and scores policies over 2,000 seeded starts; the page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it with the first lab whose numbers you will keep — at the latest before block 1's lab in 10 — and reread §7 before block 4's learning pages. After it you can write analysis code whose numbers you can defend: isolated and pinned, exact where it must be, vectorized, replayable and tested.

> [!note] First pass · 처음이라면
> Two sessions. **Session 1** (about 90 minutes): the Running object, the picture and the Worked case with a calculator — P6's clock kept three ways for one hour — then §5, which derives what the Worked case used, and §6, integers that wrap. End with Self-check 2 and 3. **Session 2** (about 90 minutes): §2–§4 — names and mutability, arrays and views, vectorization — then run §10's lab and check its tables against the page. End with Self-check 1 and 5. Read §1 before you install anything on the robot computer, §7 before you simulate noise or split data, §8–§9 once a script becomes something you rerun, and do the problem set last.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] — a cart on a line with an encoder at $2048$ counts/m, a controller that samples it at $200\,\mathrm{Hz}$ and a vision node that publishes a goal at $50\,\mathrm{Hz}$ — seen as what it leaves on disk. The catalog freezes the cart; this page freezes one hour of its log and the motion that produced it. The rows marked *page-local* are this page's own course numbers, chosen for clean arithmetic; they are not measurements, and P6's catalog numbers are unchanged.

| Symbol | Value | What it is |
|---|---:|---|
| $N$ | $2048$ counts/m | P6's encoder; one count is $1/2048\,\mathrm m=0.488\,\mathrm{mm}$ |
| $f$, $T$ | $200\,\mathrm{Hz}$, $5\,\mathrm{ms}$ | P6's control rate; one log row per tick |
| $f_v$ | $50\,\mathrm{Hz}$ | P6's goal rate: every fourth tick |
| $D$ | $1\,\mathrm h$ | one log: $720{,}000$ ticks and $180{,}000$ goals *(page-local)* |
| $L$ | $20\,\mathrm m$ | the rail *(page-local)* |
| $v$ | $0.5\,\mathrm{m/s}$ | shuttle speed: $1024$ counts/s, $5.12$ counts per tick *(page-local)* |
| cycle | $100\,\mathrm s$ | $10\,\mathrm s$ at $0\,\mathrm m$, $40\,\mathrm s$ out to $20\,\mathrm m$, $10\,\mathrm s$ there, $40\,\mathrm s$ back; $36$ cycles per hour *(page-local)* |
| register | 16-bit, signed | the motor drive's raw count register, read every tick *(page-local)* |
| log columns | tick $k$, count $c_k$ | both 64-bit integers, $c_k=\lfloor 2048\,p(kT)\rfloor$ *(page-local)* |

The count is an exact integer function of the tick, and at $0.5\,\mathrm{m/s}$ the cart advances $2048\times0.5\times0.005=5.12$ counts per tick, so while it moves the log alternates steps of 5 and 6 counts — the same $5.12$ that [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR ch.13]] finds on P6's wheels. Nothing in the object is random; where §7 adds noise, it says so.

*Scope: this page teaches the Python a robot-learning researcher needs to get numbers right and get them fast — isolated and pinned environments, names and mutability, NumPy arrays and views, vectorization, the floating-point and integer limits that bite robot logs, replayable randomness, and the structure and checks that make a script rerunnable. It does not teach Python syntax from zero, which the official tutorial does; nor tensors and training, which start in [[03-deep-learning/foundations/index|1. Learning Systems]], with timing on a GPU in [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing §7]]; nor ROS 2 node code, which is [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]], or C++, which is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]]. §11 lists the rest and where it lives.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 440" style="max-width:100%;height:auto" role="img" aria-label="Two panels. (a) A ruler of float32 values near 3600 seconds, spaced u equal to 2 to the minus 12 seconds, 0.244 milliseconds. The exact sum t plus 5 milliseconds lands at 20.48 u; the stored result is the nearest grid point, t plus 20 u, 4.8828 milliseconds, so each tick loses 0.117 milliseconds. (b) The error of P6's float32 running clock over one hour of true time: slightly fast, reaching plus 1.84 seconds when it reads 2048 seconds at 34.1 minutes, then 2.34 percent slow, ending at minus 34.58 seconds when it reads 3565.42 seconds. A float64 clock, 55 nanoseconds off, and an integer tick count, exact, lie on the dashed zero line.">
  <defs><marker id="pyrcarr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) One tick near t = 3600 s, stored in float32</text>
  <text x="40" y="38" font-size="11" fill="currentColor">exact sum: t + 5 ms = t + 20.48 u</text>
  <line x1="40" y1="46" x2="488.6" y2="46" stroke="currentColor" stroke-width="1.3" marker-end="url(#pyrcarr)"/>
  <line x1="490.6" y1="46" x2="490.6" y2="70" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <line x1="40" y1="70" x2="502" y2="70" stroke="currentColor" stroke-width="1"/>
  <g stroke="currentColor" stroke-width="1"><line x1="40" y1="61" x2="40" y2="79"/><line x1="62" y1="65" x2="62" y2="75"/><line x1="84" y1="65" x2="84" y2="75"/><line x1="106" y1="65" x2="106" y2="75"/><line x1="128" y1="65" x2="128" y2="75"/><line x1="150" y1="61" x2="150" y2="79"/><line x1="172" y1="65" x2="172" y2="75"/><line x1="194" y1="65" x2="194" y2="75"/><line x1="216" y1="65" x2="216" y2="75"/><line x1="238" y1="65" x2="238" y2="75"/><line x1="260" y1="61" x2="260" y2="79"/><line x1="282" y1="65" x2="282" y2="75"/><line x1="304" y1="65" x2="304" y2="75"/><line x1="326" y1="65" x2="326" y2="75"/><line x1="348" y1="65" x2="348" y2="75"/><line x1="370" y1="61" x2="370" y2="79"/><line x1="392" y1="65" x2="392" y2="75"/><line x1="414" y1="65" x2="414" y2="75"/><line x1="436" y1="65" x2="436" y2="75"/><line x1="458" y1="65" x2="458" y2="75"/><line x1="480" y1="59" x2="480" y2="81" stroke-width="1.8"/><line x1="502" y1="65" x2="502" y2="75"/></g>
  <text x="40" y="92" font-size="10" fill="currentColor" text-anchor="middle">t</text>
  <text x="150" y="92" font-size="10" fill="currentColor" text-anchor="middle">+5 u</text>
  <text x="260" y="92" font-size="10" fill="currentColor" text-anchor="middle">+10 u</text>
  <text x="370" y="92" font-size="10" fill="currentColor" text-anchor="middle">+15 u</text>
  <text x="466" y="92" font-size="10" fill="currentColor" text-anchor="middle">+20 u</text>
  <line x1="480" y1="81" x2="480" y2="104" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <line x1="40" y1="104" x2="478" y2="104" stroke="currentColor" stroke-width="1.8" marker-end="url(#pyrcarr)"/>
  <text x="40" y="120" font-size="11" fill="currentColor">stored: nearest grid point, t + 20 u = t + 4.8828 ms</text>
  <text x="556" y="120" font-size="11" fill="currentColor" text-anchor="end">lost: 0.117 ms</text>
  <text x="12" y="140" font-size="11" fill="currentColor" fill-opacity="0.8">grid: float32 values on [2048, 4096) s, spacing u = 2⁻¹² s = 0.244 ms</text>
  <text x="12" y="166" font-size="12" fill="currentColor">(b) P6's float32 running clock for one hour: error = reading − true time</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.7" fill="none"><line x1="60" y1="176" x2="60" y2="406"/><line x1="60" y1="406" x2="540" y2="406"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.15"><line x1="60" y1="256.5" x2="540" y2="256.5"/><line x1="60" y1="314" x2="540" y2="314"/><line x1="60" y1="371.5" x2="540" y2="371.5"/></g>
  <line x1="60" y1="199" x2="540" y2="199" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3" stroke-opacity="0.8"/>
  <text x="52" y="203" font-size="10" fill="currentColor" text-anchor="end">0 s</text>
  <text x="52" y="260.5" font-size="10" fill="currentColor" text-anchor="end">−10</text>
  <text x="52" y="318" font-size="10" fill="currentColor" text-anchor="end">−20</text>
  <text x="52" y="375.5" font-size="10" fill="currentColor" text-anchor="end">−30</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.7"><line x1="60" y1="406" x2="60" y2="410"/><line x1="180" y1="406" x2="180" y2="410"/><line x1="300" y1="406" x2="300" y2="410"/><line x1="420" y1="406" x2="420" y2="410"/><line x1="540" y1="406" x2="540" y2="410"/></g>
  <text x="60" y="421" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <text x="180" y="421" font-size="10" fill="currentColor" text-anchor="middle">15</text>
  <text x="300" y="421" font-size="10" fill="currentColor" text-anchor="middle">30</text>
  <text x="420" y="421" font-size="10" fill="currentColor" text-anchor="middle">45</text>
  <text x="540" y="421" font-size="10" fill="currentColor" text-anchor="end">60 min</text>
  <text x="300" y="435" font-size="10" fill="currentColor" text-anchor="middle">true time</text>
  <polyline points="60.0,199.0 77.1,199.2 94.1,198.5 128.2,197.0 196.4,194.2 332.8,188.4 540.0,397.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <g fill="currentColor"><circle cx="94.1" cy="198.5" r="2"/><circle cx="128.2" cy="197.0" r="2"/><circle cx="196.4" cy="194.2" r="2"/><circle cx="332.8" cy="188.4" r="3.2"/><circle cx="540" cy="397.8" r="3.2"/></g>
  <text x="200" y="183" font-size="11" fill="currentColor" text-anchor="middle">0.098 % fast: 5.0049 ms per tick</text>
  <text x="340" y="180" font-size="11" fill="currentColor">reads 2048 s at 34.1 min, +1.84 s</text>
  <text x="66" y="217" font-size="11" fill="currentColor" fill-opacity="0.85">float64 (+55 ns), integer ticks (0): dashed line</text>
  <text x="428" y="330" font-size="11" fill="currentColor" text-anchor="end">2.34 % slow: 4.8828 ms per tick</text>
  <text x="528" y="400" font-size="11" fill="currentColor" text-anchor="end">1 h: reads 3565.42 s, −34.58 s</text>
</svg>

Top: on $[2048, 4096)$ s float32 values are $2^{-12}\,\mathrm s=0.244\,\mathrm{ms}$ apart, so the exact sum $t+5\,\mathrm{ms}$ falls $20.48$ spacings along and is stored at $20$, $4.8828\,\mathrm{ms}$ — $0.117\,\mathrm{ms}$ lost on every tick. Bottom: P6's float32 running clock over one true hour runs $0.098\%$ fast until it reads $2048\,\mathrm s$ at $34.1$ min, $1.84\,\mathrm s$ ahead, then $2.34\%$ slow, and reads $3565.42\,\mathrm s$ at the hour, $34.58\,\mathrm s$ behind; a float64 clock ($+55\,\mathrm{ns}$) and an integer tick count (exact) stay on the zero line.

### Worked case · 대상으로 한 번 끝까지

This is the homework object at its catalog rate: P6's logger keeps time the way most firmware does, `t += 0.005` once per tick, for one hour. The problem set changes the period; do the $5\,\mathrm{ms}$ version here first, so that the set is a change of knob rather than a first derivation. Three facts are glossed here and derived in §5: a float32 number carries 24 significant bits, so every value in the **binade** $[2^e,2^{e+1})$ is a multiple of the **spacing** $u=2^{e-23}$; each sum is **rounded to the nearest** such multiple; and $0.005$, which is not a binary fraction, is itself stored as $0.004999999888\,\mathrm s$.

**Step 1 — one tick near the end of the hour.** Any reading between $2048$ and $4096$ s is a multiple of

$$u=2^{11-23}=2^{-12}\ \mathrm s=0.244140625\ \mathrm{ms},\qquad \frac{T}{u}=\frac{0.005}{2^{-12}}=20.48$$

so the exact sum $t+T$ lies $0.48u$ past the grid point $t+20u$ and $0.52u$ short of $t+21u$. Rounding to the nearest keeps $t+20u$: each tick adds $20u=4.8828125\,\mathrm{ms}$ instead of $5\,\mathrm{ms}$, and the clock runs at $20/20.48=0.9765625$ of true speed, losing $0.1171875\,\mathrm{ms}$ a tick, $2.34\%$.

**Step 2 — the first 34 minutes.** Between $128$ and $2048$ s the spacing is $2^{-16}$ to $2^{-13}$ s, and $T/u=327.68$, $163.84$, $81.92$ and $40.96$ round *up*, to $328$, $164$, $82$ and $41$: every tick adds $41\cdot2^{-13}=5.0048828125\,\mathrm{ms}$, fast by $2^{-10}$, $0.098\%$. Below $128$ s the stored steps are within $0.06\%$ of $5\,\mathrm{ms}$, and §10 prints the clock first reading $128$ s at tick $25{,}607$, true time $128.035$ s, $0.031$ s behind. From there, $1920$ s of reading at $5.0048828125\,\mathrm{ms}$ a tick takes

$$\frac{1920}{0.0050048828125}\approx383{,}625\ \text{ticks}=1918.13\ \mathrm s,\qquad e=-0.031+(1920-1918.13)=+1.842\ \mathrm s$$

because a clock that runs fast by $2^{-10}$ covers its reading in less true time. So it reads $2048$ s at tick $25{,}607+383{,}625=409{,}232$, true time $2046.16$ s ($34.1$ min), $1.842$ s ahead.

**Step 3 — the rest of the hour.** The remaining $720{,}000-409{,}232=310{,}768$ ticks each lose $T-20u=0.1171875\,\mathrm{ms}$, so

$$e_{720\,000}=1.842-310{,}768\times0.1171875\times10^{-3}=1.842-36.418=-34.576\ \mathrm s$$

since the stored step stays $20u$ for as long as the reading stays below $4096$ s. The float32 clock reads $3565.42$ s after one true hour. §10's run prints $-34.575684$ s, and the same formula evaluated on the run's own entry state agrees to six decimals.

**Step 4 — the same loop in float64.** At $3600$ s float64's spacing is $2^{11-52}=4.55\times10^{-13}$ s, and each sum is off by at most half of it, so after $720{,}000$ ticks

$$|e|\le720{,}000\times\tfrac12\times2^{-41}\ \mathrm s=1.64\times10^{-7}\ \mathrm s$$

since no rounding exceeds half a spacing and the reading never reaches $4096$ s, where the spacing would double. The run gives $+5.54\times10^{-8}$ s: the same loop, eight orders of magnitude better, and still a number that grows with every tick.

**Step 5 — no running sum at all.** Keep the integer tick count $k$, exact in 64 bits for $2^{63}$ ticks, and compute the time only when it is needed, $t=k/200$: one division, rounded once, wrong by at most half a spacing whatever $k$ is. At $k=720{,}000$ it is exactly $3600.0$. This is the time vector of [[02-foundations/lab-kernel|0.7 Lab Kernel §1]], $t_0+iT$ built from the index, and it is how ROS 2 itself keeps time: whole nanoseconds in a 64-bit integer in its libraries, and a `Time` message of an `int32` second and a `uint32` nanosecond (§5).

**Step 6 — what it costs P6.**

| clock kept as | reads after 1 h | error |
|---|---:|---:|
| float32, `t += 0.005` | $3565.424316$ s | $-34.575684$ s |
| float64, `t += 0.005` | $3600.0000000554$ s | $+5.54\times10^{-8}$ s |
| 64-bit tick count, $t=k/200$ | $3600.0$ s | $0$ |

$34.58$ s is $6{,}915$ control periods and $494$ times P6's whole $70\,\mathrm{ms}$ budget. §10 finds the float32 clock more than one control period wrong after $81.23$ s and more than the whole budget wrong after $231.16$ s, under four minutes. If the commands carried this clock's stamps and the goals a correct one, the check in the Worked case of [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]], that every command lies within $20\,\mathrm{ms}$ of a goal, would fail from $108.53$ s. Nothing raised an error.

### 1. Which interpreter, and where its packages go

*In one sentence:* a result depends on your code and on the exact versions of everything it imports, so each project gets its own environment made from a known interpreter, with every package pinned to a version, and nothing is ever installed into the Python that belongs to the operating system.

The same analysis script can print different numbers on your laptop and on the robot computer only because it imported different versions of NumPy — or fail on the robot because a package went into the wrong Python. Both are questions of which interpreter runs and where its packages live.

**Which Python.** `python3` is whichever interpreter comes first on the shell's search path, and `sys.executable` names it. On the Mac this page was checked on, that is Anaconda's:

```bash
which python3
python3 -c "import sys; print(sys.version.split()[0], sys.executable)"
```

```text
/opt/anaconda3/bin/python3
3.12.4 /opt/anaconda3/bin/python3
```

Run the same two lines on the robot computer before anything else: they tell you which interpreter your scripts will use, and the last paragraph of this section is about why that answer matters to ROS 2.

**Where an import comes from.** `import numpy` looks first for a built-in module, then for the name in each directory of `sys.path` in order — the script's own directory, the directories in `PYTHONPATH`, and the installation's `site-packages` — and loads the first match. Installing a package means putting it into one of those directories. So a package installed for one interpreter is invisible to another, and a change to the environment the interpreter starts in, such as sourcing a ROS 2 setup file ([[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]), changes what `import` finds.

**Never the system Python.** On Linux, the Python that came with the distribution belongs to the distribution. Python's own documentation warns that installing into it needs root and can interfere with the system package manager and with other parts of the system when pip unexpectedly upgrades one of their components. Ubuntu goes further: its pip refuses, with an error that calls the environment *externally managed* and points to `apt install python3-xyz` or a virtual environment (the mechanism is PEP 668); the override flag, `--break-system-packages`, is named for what it risks. A `sudo pip install` that upgrades a package apt installed is how a working robot computer loses tools it never touched.

**A virtual environment.** The fix is one directory per project, created from a named interpreter. These commands ran in a scratch project directory on the Mac; the machine's long path is shortened to `…` in the `command` line:

```bash
python3 -m venv .venv
cat .venv/pyvenv.cfg
.venv/bin/python -c "import sys; print(sys.prefix != sys.base_prefix)"
ls .venv/lib/python3.12/site-packages
.venv/bin/python -m pip freeze
.venv/bin/python -c "import numpy"
```

```text
home = /opt/anaconda3/bin
include-system-site-packages = false
version = 3.12.4
executable = /opt/anaconda3/bin/python3.12
command = /opt/anaconda3/bin/python3 -m venv …/p6-analysis/.venv
True
pip
pip-24.0.dist-info
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'numpy'
```

Read it line by line. `pyvenv.cfg` records the base interpreter and its version: the environment belongs to that interpreter at that path, and the documentation's rule is to recreate an environment, never to move or copy it. `sys.prefix != sys.base_prefix` is `True`, the documented test for running inside one. Its `site-packages` holds pip alone, so `pip freeze` prints nothing. And the NumPy that the base Anaconda Python has is not visible: the environment is isolated by default. Activation is a convenience, not a requirement — calling `.venv/bin/python` directly is the same interpreter — and what it does is mainly to put the environment's `bin` first on the search path:

```bash
source .venv/bin/activate
which python
deactivate
which python
```

```text
…/p6-analysis/.venv/bin/python
/opt/anaconda3/bin/python
```

**Pinning.** The environment's contents live in a text file of exact versions, one `name==version` per line — here the one line this page's lab needs, pinned to the NumPy its outputs were produced with on the Mac:

```text
numpy==2.0.2
```

`python -m pip freeze > requirements.txt` writes the installed set in that form, and `python -m pip install -r requirements.txt` installs exactly that set into a fresh environment (Python tutorial, §12). The install downloads packages and was not run here; `pip freeze` was, above, and printed an empty set. Commit `requirements.txt`; never commit `.venv/`.

> **Virtual environment, defined.** A **virtual environment** is a *directory* — not a copy of Python and not a container — that gives one project its own installed packages on top of one base interpreter. Four defining conditions. It is **made from a base interpreter and records it**: `pyvenv.cfg` names that interpreter's directory and version, so the environment runs that Python and no other, and it is recreated rather than moved or copied. It has **its own `site-packages`**, which the base's packages do not enter by default. **Its interpreter installs there**: `.venv/bin/python -m pip install` writes into the environment and never into the system. And it is **disposable**: rebuilt from a pinned list and never committed.
>
> $$\text{inside an environment}\iff\texttt{sys.prefix}\neq\texttt{sys.base\_prefix},\qquad E=\big(\text{interpreter }X.Y,\ \{p_i{=}{=}v_i\}\big)$$
>
> where `sys.prefix` is the running environment's directory, `sys.base_prefix` the base interpreter's, and each $p_i{=}{=}v_i$ pins package $p_i$ to exactly version $v_i$ — so two machines that share the interpreter version and the pinned set import the same code.
>
> - **Example**: `p6-analysis/.venv`, made from the Mac's Python 3.12.4. The test prints `True`, `site-packages` holds pip alone, and `import numpy` fails until the pinned `numpy==2.0.2` is installed into it.
> - **Non-example**: `sudo pip install numpy --upgrade` on the robot computer. There is no separate directory, so the install lands among the packages apt manages and ROS 2 was built against; Ubuntu's pip refuses it, and forcing it risks the system's own Python tools.
> - **Why it matters**: a result is a function of the code *and* of the versions it imported. An environment rebuilt from pins fixes the second argument cheaply — and §7 shows that even NumPy's seeded random streams are guaranteed only on the same NumPy build.

**The ROS 2 case.** ROS 2 Jazzy's binaries are built for Ubuntu 24.04 and its Python 3.12 (REP 2000 lists 3.12.3), and the ROS 2 guide to Python packages states that the interpreter must match the one the binaries were built with — adding that with something like conda it very likely will not. So on the robot computer the order is: a rosdep key in `package.xml` ([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]); failing that, the apt package `python3-<name>`; and for what neither provides, a virtual environment created with the system `python3` inside the workspace, with an empty `COLCON_IGNORE` file in it so that colcon's crawl ([[04-robotics/ros2/workspaces-packages-launch|25.4 §3]]) skips it, pip-installed into, and the workspace then built after sourcing `/opt/ros/jazzy/setup.bash`. The guide adds that a package you mean to release with Bloom, ROS's release tool, should declare what it needs as rosdep keys instead. When the whole machine must be reproducible, the unit is a container image pinned by its digest ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]).

### 2. Names, objects and mutability

*In one sentence:* a Python variable is a name bound to an object, assignment never copies, and any change made in place to a mutable object is seen through every name bound to it — including a default argument that was built once and a nested dict that a shallow copy shared.

A "backup" of a log that changes when the log changes, and a parameter sweep whose every run used the last value, both come from how Python names objects. Every Python object has an identity, a type and a value; its identity never changes, and `is` compares identities where `==` compares values. Lists, dicts, sets and NumPy arrays are **mutable** — their value can change in place — while ints, floats, strings and tuples are **immutable**. Assignment does not copy anything; it binds a name to an object. Three consequences on P6's data:

```python
import copy

readings = [0, 5, 10, 16]                  # four encoder readings, counts
raw = readings                             # a second name bound to the same list
raw[0] = 999
print(readings[0], raw is readings)        # one object, two names

def record(sample, log=[]):                # the default list is built once, when def runs
    log.append(sample)
    return log

run_a = record(21)                         # run A logs one sample ...
run_b = record(37)                         # ... and run B appends to run A's list
print(run_a, run_b, run_a is run_b)

def record_fixed(sample, log=None):
    if log is None:
        log = []                           # a new list on every call
    log.append(sample)
    return log

print(record_fixed(21), record_fixed(37))

base = {"rate_hz": 200, "gains": {"kp": 40.0, "kd": 2.0}}
shallow = [copy.copy(base) for _ in range(3)]      # three new outer dicts, one shared "gains"
deep = [copy.deepcopy(base) for _ in range(3)]     # three independent copies, all the way down
for kp, cfg_s, cfg_d in zip((20.0, 40.0, 80.0), shallow, deep):
    cfg_s["gains"]["kp"] = kp
    cfg_d["gains"]["kp"] = kp
print([c["gains"]["kp"] for c in shallow], base["gains"]["kp"])
print([c["gains"]["kp"] for c in deep])
```

```text
999 True
[21, 37] [21, 37] True
[21] [37]
[80.0, 80.0, 80.0] 80.0
[20.0, 40.0, 80.0]
```

The first line is plain aliasing: `raw` was never a backup. The second is the **mutable default argument**: a default value is evaluated once, when `def` runs, so every call that omits `log` appends to the same list, and run B's "fresh" log already holds run A's sample. The `None` idiom makes a new list per call; §8's dataclasses refuse such a default outright. The last two lines are the sweep bug: three configurations for $k_p=20$, $40$ and $80$, built as shallow copies of one base, all end at $k_p=80$ — and so does the base — because the three share one `gains` dict; deep copies keep the three gains apart.

> **Aliasing, defined.** **Aliasing** is a *relation between names*: two or more names bound to one object. It is not the sampling artefact of [[02-foundations/signal-processing|6. Signal Processing §2]], which shares the word. Three conditions make it matter: the names are **bound to the same object**, because assignment binds and never copies; the object is **mutable**; and a change is made **in place** through one of the names — `append`, `x[i] = …`, `+=` on a list or an array — so every other name sees it.
>
> $$b=a\ \Rightarrow\ \texttt{id}(b)=\texttt{id}(a),\qquad \text{then after } b[i]\leftarrow x:\ \ a[i]=x$$
>
> where `id` is an object's identity, fixed for its lifetime, and `a`, `b` are names — so aliasing is a question of identity, which `is` answers and `==` cannot.
>
> - **Example**: `raw = readings; raw[0] = 999` leaves `readings[0] == 999`; and `record(37)` returns `[21, 37]`, the same list object as run A's, because the default list was made once.
> - **Non-example**: `x = 3.0; y = x; y += 1.0`. A float is immutable, so `+=` binds `y` to a new object and `x` stays `3.0`. The same line on a list or a NumPy array changes the one shared object.
> - **Why it matters**: two runs of a sweep that share a default list, or a "backup" that is only a second name for the live log, produce wrong numbers without any error.

A **shallow copy** — `copy.copy(d)`, `d.copy()`, `lst[:]` — is a new outer container whose items are the original's own objects: one level copied, everything below it shared, so it is safe exactly when every item is immutable. A **deep copy**, `copy.deepcopy(d)`, copies every level, so no mutable object is shared. That is the sweep bug above: three shallow copies of `{"rate_hz": 200, "gains": {"kp": 40.0, "kd": 2.0}}` given $k_p=20$, $40$ and $80$ all read $80$, and so does the base, while three deep copies read $20$, $40$ and $80$ — and the table a sweep prints looks perfectly normal either way. (The NumPy slice `counts[::4]` is neither kind of copy but a view of the same memory, §3.)

One more contrast before arrays: for a Python list, `lst[:]` is a shallow copy; for a NumPy array, the same `arr[:]` is a view. [[02-foundations/algorithms/interview-code|11.7 §3]] lists the interview-level versions of these traps — the grid whose rows are one list, `is` against `==`.

### 3. NumPy arrays: dtype, shape, strides and views

*In one sentence:* an ndarray is one block of memory read through a dtype, a shape and strides, so a slice can be a second way of reading the same bytes — a view — and a write through the view rewrites the log it came from.

A slice of a log can be a second window onto the same memory, so an innocent-looking in-place edit of the slice rewrites the raw log. To see when, look at what an array is. An **ndarray** is one block of memory read through four things: a single **dtype**, so every item has the same size in bytes, `itemsize`; a **shape**, the tuple of lengths; **strides**, the bytes to step along each axis; and a **data buffer**, owned by the array or borrowed from another. Indexing is arithmetic on these, not a lookup: item $(n_0,\dots,n_{d-1})$ sits $\sum_k s_k n_k$ bytes after the first, where $s_k$ is axis $k$'s stride, and the array takes $\texttt{itemsize}\times\prod_k\texttt{shape}_k$ bytes. P6's hour of counts is `int64`, shape `(720000,)`, strides `(8,)`, $5{,}760{,}000$ bytes ($1{,}440{,}000$ as `int16`); reshaped to `(180000, 4)`, one row per goal period, its strides are `(32, 8)`, so item $(12{,}345,\ 3)$ sits at byte $32\cdot12{,}345+8\cdot3=395{,}064$, which is `counts[49383]`. A Python list of the same counts holds $720{,}000$ pointers of 8 bytes to separate integer objects of 28 bytes each in this Mac's 64-bit CPython (`sys.getsizeof`) — up to 36 bytes a sample instead of 8, scattered in memory, with a type check on every access. Everything fast in NumPy, slicing without copying and vectorized arithmetic (§4), follows from the strided layout, and so does every silent bug with views.

Build the hour. The count is computed with integers only, $c_k=\lfloor 2048\,p(kT)\rfloor$, so the log is exact and the same on every machine:

```python
import numpy as np

RATE_HZ, N_PER_M = 200, 2048               # P6: control rate (Hz), encoder (counts/m)
k = np.arange(3600 * RATE_HZ)              # tick index of the hour
j = k % 20_000                             # tick within this page's 100 s shuttle cycle
out = np.clip(j - 2_000, 0, 8_000)         # ticks spent driving out at 0.5 m/s
back = np.clip(j - 12_000, 0, 8_000)       # ticks spent driving back
counts = (128 * out) // 25 - (128 * back + 24) // 25    # floor(2048 p), exactly, in integers
print(counts.dtype, counts.shape, counts.strides, counts.nbytes, counts.max())
for dt in (np.int16, np.int32, np.int64, np.float64):
    print(np.dtype(dt).name, np.dtype(dt).itemsize, np.dtype(dt).itemsize * counts.size)

frames = counts.reshape(-1, 4)             # one row per 50 Hz goal period
at_goal = counts[::4]                      # the count at each goal instant
print(frames.shape, frames.strides, at_goal.shape, at_goal.strides)
print(frames.base is counts, at_goal.base is counts, np.shares_memory(at_goal, counts))
print(frames[12_345, 3] == counts[4 * 12_345 + 3])
moving = counts[counts > 0]                # a boolean mask is advanced indexing: a copy
print(moving.base is None, np.shares_memory(moving, counts))
print(frames[1_000] - frames[1_000, 0], (frames - frames[:, :1]).shape)
try:
    frames - frames[:, 0]                  # (180000, 4) against (180000,): 4 is not 180000
except ValueError as err:
    print(type(err).__name__)
```

```text
int64 (720000,) (8,) 5760000 40960
int16 2 1440000
int32 4 2880000
int64 8 5760000
float64 8 5760000
(180000, 4) (32, 8) (180000,) (32,)
True True True
True
True False
[ 0  5 10 15] (180000, 4)
ValueError
```

The default integer is 64 bits on every 64-bit system in NumPy 2, so `counts` is `int64`, and the hour of one column costs 5.76 MB; the count never exceeds $40{,}960$, so `int32` would halve that with room to spare, and §6 is about what `int16` does. The reshape and the step-4 slice are **views**: new shapes and strides, same buffer, `base is counts`. The boolean mask is a **copy**. The last three lines are broadcasting, whose rule — shapes aligned at their right ends, each pair equal or one of them 1 — is in [[02-foundations/algorithms/interview-code|11.7 §5]]: `frames[:, :1]` has shape `(180000, 1)`, so subtracting it takes each goal period's first count from all four of its ticks, $[0, 5, 10, 15]$ in frame 1,000, where the cart is driving out; `frames[:, 0]`, shape `(180000,)`, lines $180{,}000$ up against $4$ and fails.

> **View, defined.** A **view** is an *ndarray whose data buffer belongs to another array*: new metadata, same bytes. Three defining conditions: it **shares the buffer** of its base — `v.base` is the original and `np.shares_memory(v, a)` is true; it reads that buffer with **its own offset and strides**, which is why only index patterns expressible that way can be views — basic slicing (`a[i:j:s]`, `a[:, 0]`) and most reshapes — while boolean and integer-array indexing always copy; and a **write through the view writes the base**.
>
> $$v=a[i_0::s]\ \Rightarrow\ v[m]\ \text{is at byte}\ (i_0+m\,s)\,\texttt{itemsize}\ \text{of } a\text{'s buffer},\qquad \texttt{v.strides}=s\cdot\texttt{a.strides}$$
>
> where $i_0$ is the slice's start, $s$ its step and $m$ the view's own index — so a slice of any size costs no copy, and a view keeps its whole base alive.
>
> - **Example**: `at_goal = counts[::4]`, shape `(180000,)`, strides `(32,)`, `base is counts`. Below, `at_goal -= 20480`, meant as "counts about mid-rail", moves every fourth sample of the raw log by 10 m.
> - **Non-example**: `counts[counts > 0]` and `counts[np.array([0, 4, 8])]`, boolean and integer-array indexing, which always copy; writing into them leaves the log alone. And a Python list's `lst[:]`, a copy with the same syntax as a NumPy view.
> - **Why it matters**: views are why NumPy slicing is free, and an in-place operation on one is the commonest way a raw log gets rewritten by the analysis that reads it.

Here is that bug, and its fix:

```python
centred = at_goal                          # meant: goal counts about mid-rail (20,480 = 10 m)
centred -= 20_480                          # in place, through the view
print(counts[4], counts[5], np.abs(np.diff(counts)).max() / (N_PER_M * 0.005))
counts[::4] += 20_480                      # undo it, so the rest of the page sees the true log
centred = counts[::4] - 20_480             # the intended result: a new array
print(counts[4], np.shares_memory(centred, counts), np.abs(np.diff(counts)).max() / (N_PER_M * 0.005))
```

```text
-20480 0 2000.5859375
0 False 0.5859375
```

After the in-place subtraction, `counts[4]` is $-20{,}480$ while its neighbour is $0$, and the largest one-tick speed in the log is $2000.59\,\mathrm{m/s}$ — a cart that crawls at $0.5\,\mathrm{m/s}$ now teleports every fourth tick. `centred = counts[::4] - 20_480` computes a new array, and the log's largest one-tick speed is back to $0.59\,\mathrm{m/s}$, six counts per tick. The habit: before any in-place operation — `-=`, `x[...] =`, an `out=` argument — ask `np.shares_memory(x, log)`, and `.copy()` when the answer is yes and you did not mean it.

### 4. Vectorization: moving the loop out of the interpreter

*In one sentence:* a Python loop pays the interpreter's per-item overhead on every sample, while one NumPy expression pays it once and runs the loop in compiled code over a typed buffer, so the same arithmetic on P6's hour runs tens to hundreds of times faster and gives bit-for-bit the same numbers.

P6 writes $720{,}000$ samples an hour, and an analysis that takes seconds per hour of log gets rerun far less often than one that takes milliseconds. A controller's speed estimate from counts is a difference over a window of $w$ ticks, $v_k=(c_k-c_{k-w})/(N\,w\,T)$. Written as a loop, every one of the $719{,}999$ samples costs the interpreter the same routine: fetch two objects from the list, find out what type they are and which subtraction applies, allocate a new integer object for the result, do the same for the division, append the result. Written as one expression on two views of the same buffer, the interpreter does that routine once, and NumPy's compiled loop does the subtraction and the division on raw 8-byte integers and floats:

```python
T_S = 1 / RATE_HZ                          # 0.005 s, one tick

def speed_loop(c, w):
    """Speed from counts over a window of w ticks, one element at a time (m/s)."""
    c = c.tolist()                         # plain Python ints
    denom = N_PER_M * w * T_S
    return np.array([(c[i] - c[i - w]) / denom for i in range(w, len(c))])

def speed_vec(c, w):
    """The same estimate as one expression on two views of c (m/s)."""
    return (c[w:] - c[:-w]) / (N_PER_M * w * T_S)

for w in (1, 4, 20):
    v_loop, v_vec = speed_loop(counts, w), speed_vec(counts, w)
    levels = np.unique(v_vec[2_000:9_000])            # while driving out at 0.5 m/s
    print(w, v_vec.size, np.array_equal(v_loop, v_vec), " ".join(f"{x:.5f}" for x in levels))
```

```text
1 719999 True 0.48828 0.58594
4 719996 True 0.48828 0.51270
20 719980 True 0.49805 0.50293
```

`np.array_equal` is `True` for every window: the two versions perform the same IEEE operations on the same values, so the results agree exactly, not approximately — the test to demand of any vectorized rewrite. The levels show what the estimate can say while the cart drives out at $0.5\,\mathrm{m/s}$: a one-tick window sees 5 or 6 counts, $0.488$ or $0.586\,\mathrm{m/s}$; a 20-tick window sees 102 or 103, within $0.005\,\mathrm{m/s}$ of the truth, but it describes the cart as it was $50\,\mathrm{ms}$ ago. That trade between resolution and delay belongs to the estimator, not to Python; [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]] derives the one-count velocity quantum in its Worked case, and [[04-robotics/sensor-models|3.2 §4]] treats the quantization as noise.

**Counting the work.** For $w=1$ the loop runs $719{,}999$ iterations, each with two list lookups, a subtraction, a division and an append — about five interpreted operations, $3.6$ million in all, each on boxed Python objects. The expression makes two passes of $719{,}999$ machine operations in compiled code plus one temporary array. On this page's Mac — an Apple M1, a measurement of one machine and so kept out of the page's tested code — the expression took about $1.2\,\mathrm{ms}$ per hour of log, the list loop above (which also builds its result array) $77\,\mathrm{ms}$, and a loop that indexes the NumPy array one element at a time about $660\,\mathrm{ms}$. Over a day of P6, 24 hours, that is thirty milliseconds against up to sixteen seconds: the difference between an analysis you rerun after every change and one you stop rerunning.

> [!note]- Deeper · 더 깊이
> The timing, with Python 3.12.4 and NumPy 2.0.2, best of five runs each (the expression's best runs fell between $1.2$ and $1.3\,\mathrm{ms}$):
>
> ```python
> # not-run: timing depends on the machine; the numbers in the text are one Apple M1
> import timeit
> 
> def speed_numpy_loop(c, w=1):
>     v = np.empty(len(c) - w)
>     for i in range(w, len(c)):
>         v[i - w] = (c[i] - c[i - w]) / (N_PER_M * w * T_S)
>     return v
> 
> for f in (speed_numpy_loop, speed_loop, speed_vec):
>     times = timeit.repeat(lambda: f(counts, 1), number=1, repeat=5)
>     print(f"{f.__name__:18s} best of 5: {min(times) * 1e3:9.2f} ms")
> ```

> **Vectorized operation, defined.** A **vectorized operation** is *one call that applies an operation to every item of an array inside compiled code* — a change in where the loop runs, not in what it computes. Three defining conditions: the data sit in **one typed buffer** (§3), so no item needs a type check; the loop over items runs **in compiled code**, one machine-level operation per item; and Python does a **constant amount of work per call**, however many items there are.
>
> $$t_{\text{loop}}\approx n\,(c_{\text{py}}+c_{\text{op}}),\qquad t_{\text{vec}}\approx c_{\text{call}}+n\,c_{\text{op}},\qquad c_{\text{py}}\gg c_{\text{op}}$$
>
> where $n$ is the number of items, $c_{\text{py}}$ the interpreter's cost per item (fetch, type dispatch, a new object for the result), $c_{\text{op}}$ the arithmetic itself and $c_{\text{call}}$ the fixed cost of one call — so the speed-up approaches $c_{\text{py}}/c_{\text{op}}$ as $n$ grows, and vanishes for arrays of a few items.
>
> - **Example**: `(c[w:] - c[:-w]) / (N_PER_M * w * T_S)` on P6's hour: two views, one subtraction and one division over $719{,}999$ items, equal bit for bit to the loop, and about 60 times faster than the list loop on the M1.
> - **Non-example**: a running sum written with slices, `t[1:] = t[:-1] + dt`. The right-hand side is computed from the *old* `t` before anything is stored, so each item becomes its predecessor's old value plus `dt`, not a running sum. A recursion — each item needs the one just computed — is not elementwise; NumPy provides the sum as `np.cumsum`, and a general recursion, such as a filter's state, stays a loop or moves to compiled code.
> - **Why it matters**: at $200\,\mathrm{Hz}$ one day of log is $17{,}280{,}000$ samples, and the per-item interpreter cost decides whether the analysis reruns in milliseconds or in tens of seconds — which decides how often it gets rerun.

### 5. Floating point in robot logs: spacing and drift

*In one sentence:* a float is a significand times a power of two, so the gap between neighbouring values doubles at every power of two, and a clock that adds a small step to a large running total is rounded to that gap on every tick — which is how P6's float32 clock loses $34.58$ s in an hour while an integer tick count loses nothing.

P6's logger loses $34.58$ s in an hour without a single error message; to see why, you need to know which numbers a float can hold. On almost every platform Python's `float` is IEEE 754 binary64, with 53 significant bits; NumPy adds `float32`, with 24. A normal number is stored as $\pm(1.f)\cdot2^{e}$, so within one binade $[2^e,2^{e+1})$ the representable values are evenly spaced, and the spacing doubles at each power of two. `np.finfo` reports a format's fraction bits and machine epsilon, the spacing just above $1$; `np.spacing(x)` and, for Python floats, `math.ulp(x)` give the spacing at $x$:

```python
import math

for dt in (np.float32, np.float64):
    fi = np.finfo(dt)
    print(fi.dtype, fi.nmant, float(fi.eps), float(np.spacing(dt(3600.0))))
print(f"{float(np.float32(0.005)):.20f} {0.005:.20f}")

n = 3600 * RATE_HZ                                            # 720,000 ticks
clock32 = np.cumsum(np.full(n, np.float32(T_S)))[-1]          # float t += dt, in float32
clock64 = np.cumsum(np.full(n, T_S))[-1]                      # the same in float64
ticks = np.int64(n)                                           # an integer tick counter
print(f"{float(clock32):.6f} {clock64:.10f} {ticks / RATE_HZ}")
print(clock64 == 3600.0, math.isclose(clock64, 3600.0), math.isclose(clock64 - 3600.0, 0.0),
      math.isclose(clock64 - 3600.0, 0.0, abs_tol=1e-6))
print(float(np.spacing(np.float32(1.79e9))), math.ulp(1.79e9))
```

```text
float32 23 1.1920928955078125e-07 0.000244140625
float64 52 2.220446049250313e-16 4.547473508864641e-13
0.00499999988824129105 0.00500000000000000010
3565.424316 3600.0000000554 3600.0
False True False True
128.0 2.384185791015625e-07
```

The first two lines are the rule below at $t=3600$ s: $2^{-12}$ s in float32, $2^{-41}$ s in float64. The third shows that $0.005$ is not a binary fraction, so both formats store a neighbour of it. The fourth is the Worked case in three lines of code. `np.cumsum` adds one item after another in the array's own dtype — exactly the firmware's `t += dt` — which §10 checks against a scalar loop.

> **Floating-point spacing, defined.** The **spacing** of a floating-point format at $x$, its **ulp** (unit in the last place), is *the gap between $x$ and the next representable number* — a property of the format at that magnitude, not an error of any computation. Three defining conditions: a binary float stores a sign, an exponent and $p$ fraction bits, so in each **binade** $[2^e,2^{e+1})$ the representable numbers are **evenly spaced**; the spacing **doubles** at each power of two; and an arithmetic result is **rounded to the nearest** representable number, so it is off by at most half a spacing.
>
> $$u(x)=2^{\lfloor\log_2|x|\rfloor-p},\qquad p=23\ (\texttt{float32}),\quad p=52\ (\texttt{float64}),\qquad \big|\mathrm{fl}(x)-x\big|\le\tfrac12\,u(x)$$
>
> where $x$ is a nonzero finite number in the normal range and $\mathrm{fl}$ is rounding to the format — so a stored time's absolute resolution gets coarser as the time grows, while its relative resolution stays near $2^{-p}$.
>
> - **Example**: at $t=3600$ s, $u=2^{11-23}=2^{-12}$ s $=0.244$ ms in float32 and $2^{11-52}=4.55\times10^{-13}$ s in float64. At 24 h float32's spacing is $7.81$ ms, more than one 5 ms tick, so of the last $1{,}000$ tick stamps of a day stored in float32 only $640$ are distinct (§10).
> - **Non-example**: the $5\,\mathrm{ms}$ step itself. $0.005$ is stored as $0.004999999888$ s in float32, a representation error of $1.1\times10^{-10}$ s that is fixed once and is not the spacing near the running time. Past the first few ticks it is far too small to change which multiple of the spacing a sum rounds to, so it plays no part in the Worked case's $34.58$ s.
> - **Why it matters**: a stamp's resolution is set by its distance from zero, so seconds since 1970 stored in float32 are resolved only to $128$ s — in float64 to $238$ ns — and a long log's time column can be coarser than the rate it records.

> **Accumulation drift, defined.** **Accumulation drift** is *the error of a running sum that is rounded after every addition* — a property of how a quantity is computed, not of the quantity. Three defining conditions: the value is built by **repeated addition** of a small increment, $t\leftarrow t+T$, instead of being computed from an index; **every sum is rounded** to the format, so the increment actually added is a whole number of spacings of the binade the sum lives in; and the rounding is **systematic** — within one binade the same increment rounds the same way on every tick, so the errors add up instead of cancelling.
>
> $$\hat t_{k+1}=\mathrm{fl}\big(\hat t_k+\mathrm{fl}(T)\big),\qquad \hat t_{k+1}-\hat t_k=u\cdot\mathrm{round}\big(\mathrm{fl}(T)/u\big)\ \ \text{inside a binade of spacing } u,\qquad e_k=\hat t_k-kT$$
>
> where $\hat t_k$ is the stored clock after $k$ ticks, $T$ the true period, $u$ the spacing of the binade holding $\hat t_k$ and $e_k$ the drift — so the clock runs at the rate $u\,\mathrm{round}(T/u)/T$, constant inside a binade and changing only at powers of two.
>
> - **Example**: P6's float32 clock: on $[2048,4096)$ s, $u=2^{-12}$ s and $T/u=20.48$, so each tick adds $20u=4.8828$ ms; the clock runs $2.34\%$ slow and ends the hour at $3565.42$ s (Worked case). Past $2^{17}=131{,}072$ s, where $T/u=0.32$ rounds to $0$, it stops for good.
> - **Non-example**: an integer tick count $k$ with $t=k/200$ computed when needed. Each time is rounded once, $|e|\le\tfrac12u(t)$, never more — exactly $0$ at every horizon of §10.
> - **Why it matters**: `t += dt` is a common line in firmware loops and simulators. In float32 it is wrong by more than P6's whole 70 ms budget after $231$ s; in float64 it is far better and still growing, $1.37\,\mu\mathrm s$ after 8 h.

**Keep time as an integer.** The fix for both problems is the Worked case's Step 5: count ticks, or nanoseconds, in a 64-bit integer, and convert to seconds once, at the edge, for display or for a formula. ROS 2 does exactly this: its libraries count nanoseconds in 64-bit integers, and its `Time` message carries an `int32` of seconds and a `uint32` of nanoseconds. A stamp converted to float64 seconds today is resolved to $2^{-22}\,\mathrm s=238\,\mathrm{ns}$, fine for P6's 5 ms ticks; converted to float32, to $128$ s — keep it as integers until the arithmetic is done.

> [!note]- Deeper · 더 깊이
> In ROS 2's C utility library `rcutils` a point in time is a 64-bit integer count of nanoseconds since the Unix epoch; `rclpy`'s `Time` holds its total nanoseconds as a Python integer and refuses totals of $2^{63}$ or more; and the `builtin_interfaces/Time` message's two fields are `int32 sec` and `uint32 nanosec`.

**Comparing floats.** Exact equality is the wrong test for computed floats: `clock64 == 3600.0` is `False` although the clock is $55$ ns off. `math.isclose(a, b)` tests

$$|a-b|\le\max\big(r\cdot\max(|a|,|b|),\ \varepsilon_{\text{abs}}\big),\qquad r=10^{-9},\ \ \varepsilon_{\text{abs}}=0\ \text{by default}$$

because a relative tolerance scales with the numbers compared, and so `math.isclose(clock64, 3600.0)` is `True`. Against zero the relative term vanishes — `math.isclose(5.5e-8, 0.0)` is `False` however small the error — so a comparison with $0$ needs an explicit `abs_tol`, in the quantity's units: `abs_tol=1e-6` for "within a microsecond". NumPy's `np.isclose(a, b)` is a different rule, $|a-b|\le\text{atol}+\text{rtol}\cdot|b|$ with $\text{atol}=10^{-8}$ and $\text{rtol}=10^{-5}$ by default: not symmetric in its arguments, and its default `atol` is too loose for quantities much smaller than one. The same spacing arithmetic, applied to 16-bit training formats rather than clocks, is [[03-deep-learning/foundations/training-at-scale|1.3 §4]].

### 6. Integers that wrap

*In one sentence:* NumPy integers and hardware counters have a fixed number of bits and wrap around silently, so P6's 16-bit count register jumps from $+16$ m to $-16$ m, and the only correct way to read it is to difference in its own width and accumulate in a wide one.

A 16-bit counter on the motor drive makes the cart appear to jump 32 m in one tick unless it is read the right way. Python's own `int` grows as needed and never overflows. NumPy's integer types, like the registers in a motor drive and the timers in a microcontroller, have a fixed width, and their arithmetic silently wraps. On the page's shuttle, the drive's 16-bit register holds the count modulo $2^{16}$:

> **Fixed-width integer, defined.** A **fixed-width integer** is *an integer type with exactly $n$ bits* — every NumPy integer dtype and every hardware counter; Python's `int` is not one. Three defining conditions: it has **a range of $2^n$ values**, $[-2^{n-1},\,2^{n-1}-1]$ for signed two's complement and $[0,\,2^n-1]$ for unsigned; its arithmetic is **modulo $2^n$**, so a result past one end reappears at the other; and in NumPy array arithmetic the wrap is **silent**, with no error and no warning.
>
> $$\mathrm{wrap}_n(x)=\big((x+2^{n-1})\bmod 2^n\big)-2^{n-1},\qquad \mathrm{wrap}_n\big(\mathrm{wrap}_n(a)-\mathrm{wrap}_n(b)\big)=a-b\ \ \text{whenever}\ |a-b|<2^{n-1}$$
>
> where $x$, $a$ and $b$ are true integer values and $n$ the width — so a narrow counter still gives exact *differences* between readings closer than half its range, which is how its wrap is undone.
>
> - **Example**: the drive's register, $n=16$. At $2048$ counts/m it holds $\pm16$ m: as the shuttle passes $16.0$ m the reading jumps from $32{,}762$ to $-32{,}768$, and at the rail's $20$ m end it reads $-24{,}576$. `np.diff` of the `int16` readings gives the true steps of 5 and 6 counts; widening to `int64` first gives a $6{,}399.4\,\mathrm{m/s}$ spike.
> - **Non-example**: `2**100` in Python, or the log's `int64` counts, which could hold about $4.5\times10^{15}$ m of travel at $2048$ counts/m. Nothing P6 does comes near either limit.
> - **Why it matters**: counters and timestamps on embedded hardware are often narrow, and every narrow counter wraps; code that differences in the counter's own width is right forever, and code that widens first is right only until the first wrap.

```python
def wrap(x, bits):
    """What an n-bit two's-complement register holds for the integer x."""
    half = 1 << (bits - 1)
    return (x + half) % (1 << bits) - half

raw16 = wrap(counts, 16).astype(np.int16)      # the drive's 16-bit count register, every tick
print(raw16.min(), raw16.max(), wrap(32_768, 16), 32_767 / N_PER_M, wrap(40_960, 16))
widened = raw16.astype(np.int64)               # widen first, then difference: wrong
in_16 = np.diff(raw16)                         # difference in 16 bits: the wrap cancels
print(np.abs(np.diff(widened)).max(), np.abs(in_16).max(), in_16.dtype)
unwrapped = raw16[0] + np.concatenate(([0], np.cumsum(in_16)))
print(unwrapped.dtype, np.array_equal(unwrapped, counts))
try:
    np.array([40_960], dtype=np.int16)         # a Python int that does not fit
except OverflowError as err:
    print(type(err).__name__)
print(2**100 > 0, np.array([32_767], dtype=np.int16) + 1)     # a Python int adopts int16, and wraps
import datetime
print(f"{2**32 / 1e6 / 60:.2f} min, {2**31 / RATE_HZ / 86_400:.1f} days,",
      datetime.datetime.fromtimestamp(2**31 - 1, datetime.timezone.utc))
```

```text
-32768 32762 -32768 15.99951171875 -24576
65530 6 int16
int64 True
OverflowError
True [-32768]
71.58 min, 124.3 days, 2038-01-19 03:14:07+00:00
```

Read the second line against the definition: across the wrap the widened readings differ by $65{,}530$ counts — the true $+6$ minus $2^{16}$ — while the 16-bit difference wraps back to $6$. `np.cumsum` then accumulates the 16-bit steps in the platform's 64-bit integer, which NumPy uses by default for any narrower integer input, so `unwrapped` reproduces all $720{,}000$ counts exactly. The next two lines are NumPy 2's promotion rules: a Python integer combined with an `int16` array takes the array's type, whatever its value, so `+ 1` on $32{,}767$ wraps silently; but a Python integer that does not fit the type it is converted to is an error, as `np.array([40_960], dtype=np.int16)` shows.

The last line prices three other narrow counters at P6's scale. A 32-bit microsecond timer wraps every $2^{32}\,\mu\mathrm s=71.58$ min — inside a two-hour log. A signed 32-bit tick counter at $200\,\mathrm{Hz}$ lasts $124.3$ days. And a signed 32-bit count of seconds since 1970 — the type of the `sec` field in a ROS 2 `Time` message — reaches its largest value at 03:14:07 UTC on 19 January 2038. The same rule undoes a timer's wrap as the register's: subtract two readings in the timer's own unsigned width, and the difference is right whenever the true interval is shorter than the timer's period.

### 7. Randomness you can replay

*In one sentence:* a pseudo-random generator is a deterministic sequence fixed by its seed, the calls made on it and the NumPy build, so replayable noise needs a generator object owned by the code that draws from it — not a global seed that any other line can disturb — and a pinned NumPy.

A seeded simulation that prints a different answer after a colleague adds one plotting line is not reproducible, and the cause is where the seed lives. Random numbers enter robot-learning code through simulated sensor noise, shuffled trials, data splits and initial weights. NumPy's pseudo-random generators are deterministic sequences, reproducible from a seed. The recommended constructor, `np.random.default_rng(seed)`, returns a `Generator` built on the PCG64 bit generator; the older functions `np.random.seed`, `np.random.random` and the rest are aliases of one global `RandomState` that the whole process shares, kept for old code:

```python
rng_a = np.random.default_rng(2048)
rng_b = np.random.default_rng(2048)
print(np.array_equal(rng_a.normal(size=5), rng_b.normal(size=5)))

np.random.seed(0)
first = np.random.normal(size=3)               # the legacy global stream
np.random.seed(0)
np.random.random()                             # some other module draws once ...
second = np.random.normal(size=3)              # ... and your "seeded" draws move
print(np.array_equal(first, second))

def noisy_counts(c, rng, sigma_counts=1.0):
    """Counts plus white noise from the generator the caller passes in."""
    return c + rng.normal(0.0, sigma_counts, size=c.shape)

trials = np.random.default_rng(2026).spawn(3)  # one independent child stream per trial
again = np.random.default_rng(2026).spawn(3)
print(all(np.array_equal(noisy_counts(counts[:8], a), noisy_counts(counts[:8], b))
          for a, b in zip(trials, again)))
```

```text
True
False
True
```

The output prints only comparisons, never the random numbers themselves, and for a reason §1 already gave: NumPy promises the same stream only on the same build, and may change a `Generator` method's stream between versions to fix a bug or improve it. The middle line is the case against a global seed. `np.random.seed(0)` at the top of a script fixes the stream only as long as nothing else draws from it; one call elsewhere — a plotting helper that jitters points, a library that shuffles — moves every later draw, and the script's "seeded" noise changes with no change to the script's own lines. Python's `random` module keeps a separate hidden generator of its own, which `np.random.seed` does not touch.

> **Seeded generator, defined.** A **seeded generator** is *a pseudo-random generator object whose whole output is fixed by its seed and by the calls made on it* — deterministic, not random, which is the point. Three defining conditions: it is **constructed from a seed**, as `np.random.default_rng(seed)` builds a `Generator` on PCG64; it is **owned and passed explicitly** to the function or trial that draws from it, rather than shared as global state; and **its environment is fixed**, because NumPy guarantees the same stream only for the same bit generator, seed and sequence of calls with the same arguments, on the same build, in the same environment, on the same machine.
>
> $$x_{1:m}=G\big(\text{seed},\ (c_1,\dots,c_r),\ \text{NumPy build}\big)$$
>
> where $x_{1:m}$ are the numbers drawn, $G$ the generator's deterministic map and $c_1,\dots,c_r$ the calls made on it in order — so anything that changes the call sequence, such as a new draw elsewhere, or the build, such as an unpinned upgrade, changes the numbers.
>
> - **Example**: two `default_rng(2048)` generators draw equal numbers; `default_rng(2026).spawn(3)` gives three trials independent child streams, and spawning again from 2026 reproduces all three, so P6's simulated encoder noise for trial 2 is the same whatever trial 1 drew.
> - **Non-example**: `np.random.seed(0)` followed by legacy draws. One extra `np.random.random()` anywhere in the process shifts the stream, and the comparison above prints `False`.
> - **Why it matters**: a result that depends on noise, a shuffle or a split is replayable only if the generator belongs to the code that uses it. Replaying it is not the same as knowing how much it varies: [[02-foundations/ml-practice|9. ML Practice §4]] is why results are reported over several seeds, and [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility §7]] lists the seeds with the code commit and the environment among what a run must record.

### 8. Structure: functions, a script entry point, a frozen config and a log file

*In one sentence:* a research script that will be rerun is a module of small functions, an entry point that runs only when the file is executed, a frozen configuration object that is written into a log file with every result, and type hints that document what each function takes.

A script you rerun for months has to be importable by its tests, record its settings beside every result, and be unable to change those settings in the middle of a run. Four habits do it.

**Functions and one entry point.** Split the work into functions with one job each — load, convert, estimate, report — in a module that can be imported without doing anything. Python sets a module's `__name__` to `"__main__"` when the file is the program being run, and to the module's own name when it is imported, so the idiom `if __name__ == "__main__":` separates the two: the block runs from the shell and not from a test or a notebook that imports the functions. The documentation's advice is to keep that block short and put the work in a `main()` function.

**A configuration as a frozen dataclass.** A `@dataclass` generates `__init__`, `__repr__` and `__eq__` from annotated fields; `frozen=True` makes assignment to a field raise `FrozenInstanceError`, so a run cannot quietly change its own settings. `dataclasses.replace` builds each variant of a sweep as a new object from the old one's field values; with fields that are numbers and strings, as here, the variants share nothing a later line could change, which designs out §2's shallow-copy bug (a field holding a dict or a list would still be shared, since the values are passed on, not copied). And since Python 3.11 a field whose default is unhashable, such as a list, is refused when the class is defined, which catches `record()`'s bug before it runs:

```python
import dataclasses
from dataclasses import dataclass

@dataclass(frozen=True)
class LogConfig:
    rate_hz: int = 200                 # P6 control rate
    counts_per_m: int = 2048           # P6 encoder
    seconds: int = 3600                # length of the log
    clock_dtype: str = "float32"       # how the running clock is stored

base_cfg = LogConfig()
sweep = [dataclasses.replace(base_cfg, seconds=s) for s in (60, 3_600, 28_800, 86_400)]
print([c.seconds for c in sweep], base_cfg.seconds, sweep[1] == base_cfg)
try:
    base_cfg.seconds = 7_200
except dataclasses.FrozenInstanceError as err:
    print(type(err).__name__)
try:
    @dataclass
    class BadConfig:
        topics: list = []              # a mutable default: record() again
except ValueError as err:
    print(type(err).__name__)

def ticks_to_seconds(k: int, rate_hz: int = 200) -> float:
    return k / rate_hz

print(ticks_to_seconds(720_000), ticks_to_seconds(720_000.7))
```

```text
[60, 3600, 28800, 86400] 3600 True
FrozenInstanceError
ValueError
3600.0 3600.0035
```

The last line is about **type hints**: `k: int` documents the argument for a reader, an editor and a type checker, but the interpreter does not enforce annotations, so a float tick count passes through and returns $3600.0035$ s without complaint. Hints document; assertions check (§9). What a configuration must record to make a run reconstructable — calibration, gains, units, frames, firmware, the software commit — is [[04-robotics/robot-systems-deployment|10. Robot Systems §8]].

**Logging to a file.** `print` goes to a terminal that closes; a log file stays with the result. `logging.basicConfig(filename=…, level=…, format=…)` attaches a file handler to the root logger, and each module takes its own logger with `logging.getLogger(__name__)`. One trap: `basicConfig` does nothing if the root logger already has a handler, unless `force=True` (Python 3.8 and later) — so in a notebook, or after a library has configured logging, changing the file name and rerunning silently keeps writing to the old file:

```python
import logging, os, tempfile

with tempfile.TemporaryDirectory() as tmp:
    first, second = os.path.join(tmp, "run1.log"), os.path.join(tmp, "run2.log")
    fmt = "%(levelname)s %(name)s: %(message)s"
    logging.basicConfig(filename=first, level=logging.INFO, format=fmt)
    log = logging.getLogger("p6_drift")
    log.info("config %s", dataclasses.asdict(sweep[1]))
    logging.basicConfig(filename=second, level=logging.INFO, format=fmt)   # does nothing
    log.info("meant for run2.log")
    print(os.path.exists(second), open(first).read().splitlines())
    logging.basicConfig(filename=second, level=logging.INFO, format=fmt, force=True)
    log.info("now in run2.log")
    print(open(second).read().splitlines())
    root = logging.getLogger()
    for handler in root.handlers[:]:       # close the file before the directory is deleted
        root.removeHandler(handler)
        handler.close()
```

```text
False ["INFO p6_drift: config {'rate_hz': 200, 'counts_per_m': 2048, 'seconds': 3600, 'clock_dtype': 'float32'}", 'INFO p6_drift: meant for run2.log']
['INFO p6_drift: now in run2.log']
```

**The pieces as one script.** Here they are together, as the file `p6_drift.py` in the scratch project of §1: a frozen configuration, two small functions with type hints, a module-level logger, a `main()` that parses two options and writes the configuration into the log before the result, and the entry-point guard. Its first line is a comment that tells this wiki's page checker the listing is a file to be run from the shell, not a cell:

```python
# not-run: p6_drift.py, a script; run it from the shell, as below
"""Clock drift of P6's logger: a float running clock against an integer tick count."""
import argparse
import dataclasses
import logging
from dataclasses import dataclass

import numpy as np

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class LogConfig:
    rate_hz: int = 200                 # P6 control rate
    seconds: int = 3600                # length of the log
    clock_dtype: str = "float32"       # how the running clock is stored


def running_clock(n_ticks: int, dtype: type, step: float) -> float:
    """t <- t + step, n_ticks times, every sum rounded to dtype."""
    steps = np.full(n_ticks, dtype(step), dtype=dtype)
    return float(np.cumsum(steps, dtype=dtype)[-1])


def clock_error(cfg: LogConfig) -> float:
    """Running clock minus the exact elapsed time after cfg.seconds, in seconds."""
    n = cfg.seconds * cfg.rate_hz                  # an integer tick count: exact
    dtype = np.dtype(cfg.clock_dtype).type
    return running_clock(n, dtype, 1 / cfg.rate_hz) - n / cfg.rate_hz


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=int, default=3600)
    parser.add_argument("--dtype", default="float32", choices=["float32", "float64"])
    args = parser.parse_args()
    cfg = LogConfig(seconds=args.seconds, clock_dtype=args.dtype)
    logging.basicConfig(filename="p6_drift.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    log.info("config %s", dataclasses.asdict(cfg))
    err = clock_error(cfg)
    log.info("clock error %+.6g s", err)
    print(f"{cfg.clock_dtype} clock after {cfg.seconds} s: error {err:+.6g} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Run twice from the shell, then imported, on the Mac:

```bash
python3 p6_drift.py
python3 p6_drift.py --seconds 60 --dtype float64
cat p6_drift.log
python3 -c "import p6_drift; print(p6_drift.__name__, p6_drift.clock_error(p6_drift.LogConfig()))"
wc -l p6_drift.log
```

```text
float32 clock after 3600 s: error -34.5757 s
float64 clock after 60 s: error +1.22427e-11 s
2026-09-23 19:12:58,178 INFO __main__: config {'rate_hz': 200, 'seconds': 3600, 'clock_dtype': 'float32'}
2026-09-23 19:12:58,182 INFO __main__: clock error -34.5757 s
2026-09-23 19:12:58,264 INFO __main__: config {'rate_hz': 200, 'seconds': 60, 'clock_dtype': 'float64'}
2026-09-23 19:12:58,264 INFO __main__: clock error +1.22427e-11 s
p6_drift -34.57568359375
       4 p6_drift.log
```

Every result in the log sits under the configuration that produced it, with a time. The logger's name shows the `__name__` rule at work: `__main__` when the file ran as the program, `p6_drift` when it was imported — and the import computed the drift without running `main()`, so the log still has four lines.

### 9. Checking results: assertions, regression tests and pytest

*In one sentence:* a check at a function's boundary stops a run the moment an assumption about shape, type, unit or range fails, and a regression test pins a result the page has derived, so that a later change which moves it fails loudly instead of changing a table quietly.

A wrong-length array or a quietly changed constant produces a table that looks normal. Checks turn such mistakes into loud failures, at the moment they happen.

**Checks at the boundary, assertions inside.** Check the things a numeric function silently assumes — shape, dtype, range, units — where the data come in, so that a wrong input becomes an immediate failure instead of a wrong answer. [[02-foundations/algorithms/interview-code|11.7 §5]] gives the rule of thumb, and the reason for it: `python -O` removes assertions, so inputs from files and callers are validated with an explicit `raise`, and an `assert` guards what your own code has computed. Units live in names — `t_s`, `p_m`, `counts` — and in docstrings.

```python
def check_log(c, rate_hz=200, seconds=3600, rail_m=20):
    """Validate a P6 count log: one int64 count per tick, inside the rail."""
    if c.shape != (rate_hz * seconds,) or c.dtype != np.int64:
        raise ValueError(f"expected int64 {(rate_hz * seconds,)}, got {c.dtype} {c.shape}")
    if c.min() < 0 or c.max() > rail_m * N_PER_M:
        raise ValueError(f"counts {c.min()} to {c.max()} leave the {rail_m} m rail")
    return True

print(check_log(counts))
try:
    check_log(counts[::4])                 # the goal-rate view, passed by mistake
except ValueError as err:
    print("ValueError:", err)

step = np.diff(counts)                     # our own derived array: counts per tick
assert step.shape == (counts.size - 1,) and np.abs(step).max() <= 6, np.abs(step).max()

FROZEN_F32_ERR_1H_S = -34.57568359375      # the Worked case's float32 drift, pinned

def test_float32_clock_drift_is_pinned():
    t = np.cumsum(np.full(720_000, np.float32(0.005)))[-1]
    assert abs((float(t) - 3600.0) - FROZEN_F32_ERR_1H_S) <= 1e-9

test_float32_clock_drift_is_pinned()
print("regression test passed")
```

```text
True
ValueError: expected int64 (720000,), got int64 (180000,)
regression test passed
```

The goal-rate view has a quarter of the samples, and the check names the problem in one line instead of letting a wrong-length array flow into a speed estimate. The `assert` after it states an invariant of an array the code derived itself — P6's shuttle never moves more than 6 counts a tick — and stays silent while it holds.

**A regression test** pins a result that has been derived and checked, so that code changes cannot move it unnoticed. Its rule is one inequality,

$$\text{pass}\iff\big|\,y'-y^\star\big|\le\varepsilon$$

where $y^\star$ is the frozen value, $y'$ what the current code computes and $\varepsilon$ a tolerance chosen on purpose, because the right $\varepsilon$ depends on what may legitimately change. $y^\star=-34.57568359375$ s comes from a fixed sequence of float32 additions, each correctly rounded, so any IEEE machine reproduces it and $\varepsilon=10^{-9}$ s is honest; a result whose summation order can change — `np.sum`'s pairwise summation, multi-threaded linear algebra, a GPU reduction — needs an $\varepsilon$ of the size of that change, stated. An integer count needs $\varepsilon=0$. 25.10 calls the same idea, applied to a whole run, a pinned run ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]).

**pytest, in one paragraph.** pytest collects files named `test_*.py` or `*_test.py`, runs every function in them whose name starts with `test`, and reports each plain `assert` that fails with the values of its subexpressions. `pytest.approx(expected, rel=…, abs=…)` compares floats — by default within a relative $10^{-6}$ or an absolute $10^{-12}$, whichever is met — and `with pytest.raises(Error):` asserts that an exception happens. The tests for `p6_drift.py`, in `test_p6_drift.py` beside it:

```python
# not-run: test_p6_drift.py, collected and run by pytest, as below
"""Regression tests for p6_drift.py; run them with: python3 -m pytest -q"""
import pytest

from p6_drift import LogConfig, clock_error

FROZEN_F32_ERR_1H_S = -34.57568359375          # pinned from the page's Worked case


def test_float32_drift_is_pinned():
    assert clock_error(LogConfig()) == pytest.approx(FROZEN_F32_ERR_1H_S, abs=1e-9)


def test_float64_drift_is_small():
    assert abs(clock_error(LogConfig(clock_dtype="float64"))) < 1e-6


def test_integer_ticks_are_exact():
    assert 3600 * 200 / 200 == 3600.0


def test_config_is_frozen():
    with pytest.raises(AttributeError):        # FrozenInstanceError is an AttributeError
        LogConfig().seconds = 60
```

```bash
python3 -m pytest -q
```

```text
....                                                                     [100%]
4 passed in 0.05s
```

Run on the Mac with the pytest 7.4.4 that its Anaconda Python already had; the time is that machine's. Each dot is a passing test. The first test imports the module, which is why the entry-point guard of §8 matters: without it, collecting the tests would run the script. Inside a ROS 2 package the same tests run under `colcon test`, and [[04-robotics/ros2/debugging-data-reproducibility|25.10 §10]] shows where they go and how to read the results.

### 10. The lab: three clocks, views, a vectorized speed and a 16-bit register

Each claim of §3–§6 is a number you can rerun. Six parts on the frozen object, NumPy only and deterministic, so the output is the same on any machine. Part 1 runs the three clocks of the Worked case to 1 min, 1 h, 8 h and 24 h. Part 2 explains the float32 column: it checks `np.cumsum` against a one-at-a-time scalar loop, prints the step float32 stores in every binade from $128$ s to $2^{18}$ s, re-derives the Worked case's end value from its formula, and finds when the error passes $5$, $20$ and $70$ ms and when the clock stops. Part 3 stores tick stamps in float32 without accumulating them. Part 4 applies an in-place subtraction through five ways of selecting P6's goal-rate samples. Part 5 is §4's vectorized speed against its loop for three windows, and Part 6 is §6's 16-bit register. The block redefines what it needs, so it runs on its own.

```python
# 12.3 lab: P6's one-hour log - three clocks, float spacing, views, a vectorized speed, a 16-bit register. NumPy only.
import numpy as np

# --- 0. the running object: P6 and this page's frozen numbers ------------------------------------
RATE_HZ, N_PER_M = 200, 2048                 # P6: control rate (Hz), encoder (counts/m)
T_S = 1 / RATE_HZ                            # one tick, 0.005 s
HORIZONS = (("1 min", 60), ("1 h", 3_600), ("8 h", 28_800), ("24 h", 86_400))

def running_clock(n_ticks, dtype, step=T_S, chunk=1_000_000):
    """t <- t + step, n_ticks times, each sum rounded to dtype: the firmware line 't += dt'."""
    t, done, s = dtype(0.0), 0, dtype(step)
    while done < n_ticks:
        m = min(chunk, n_ticks - done)
        t = np.cumsum(np.concatenate(([t], np.full(m, s, dtype=dtype))), dtype=dtype)[-1]
        done += m
    return t

def shuttle_counts(seconds):
    """This page's shuttle at 200 Hz: 10 s at 0 m, 40 s out to 20 m, 10 s there, 40 s back."""
    j = np.arange(seconds * RATE_HZ) % 20_000
    out = np.clip(j - 2_000, 0, 8_000)       # ticks driven out at 0.5 m/s = 5.12 counts per tick
    back = np.clip(j - 12_000, 0, 8_000)     # ticks driven back
    return (128 * out) // 25 - (128 * back + 24) // 25       # floor(2048 p), in exact integers

# --- 1. three clocks over four horizons ----------------------------------------------------------
print("| horizon | ticks | float32 clock (s) | float32 error (s) | float64 error (s) | integer ticks error (s) |")
print("|---|---:|---:|---:|---:|---:|")
for name, sec in HORIZONS:
    n = sec * RATE_HZ
    c32, c64 = float(running_clock(n, np.float32)), float(running_clock(n, np.float64))
    t_int = np.int64(n) / RATE_HZ                            # count ticks exactly, divide once
    print(f"| {name} | {n:,} | {c32:,.6f} | {c32 - sec:+,.6f} | {c64 - sec:+.2e} | {t_int - sec:.1f} |")

# --- 2. why: the step float32 actually adds, binade by binade ------------------------------------
t = running_clock(700_000, np.float32)       # 20,000 ticks before the hour ...
for _ in range(20_000):                      # ... then one scalar addition at a time
    t = np.float32(t + np.float32(T_S))
print("scalar loop equals cumsum at 1 h:", float(t) == float(running_clock(720_000, np.float32)))
print("| clock reading (s) | spacing u (s) | 5 ms / u | stored step (ms) | clock rate |")
print("|---|---:|---:|---:|---:|")
for e in range(7, 18):                       # binade [2^e, 2^(e+1)) seconds
    lo = np.float32(2.0 ** e)
    u = float(np.spacing(np.float32(1.5 * 2.0 ** e)))          # the spacing inside the binade
    step = float(np.float32(lo + np.float32(T_S)) - lo)      # what one tick adds there
    print(f"| {2**e:,}–{2**(e + 1):,} | $2^{{{e - 23}}}$ | {float(np.float32(T_S)) / u:.2f} | {step * 1e3!r} | {step / T_S:.7f} |")
hour = np.cumsum(np.full(720_000, np.float32(T_S)))          # every tick of the hour
err = hour - np.arange(1, 720_001) / RATE_HZ
for reading in (128, 512, 2048):
    k_in = int(np.argmax(hour >= reading)) + 1
    print(f"reads {reading} s first at tick {k_in:,}, true {k_in / RATE_HZ:.3f} s, error {err[k_in - 1]:+.4f} s")
step = (float(hour[-1]) - float(hour[-1001])) / 1000                  # the step in the last binade
print(f"last 1,000 ticks step {step * 1e3:.7f} ms; Worked case formula"
      f" {err[k_in - 1] - (720_000 - k_in) * (T_S - step):+.6f} s against the run {err[-1]:+.6f} s")
for tol in (0.005, 0.020, 0.070):
    k_bad = int(np.argmax(np.abs(err) > tol)) + 1
    print(f"error first exceeds {tol * 1e3:.0f} ms at tick {k_bad:,} ({k_bad / RATE_HZ:.2f} s)")
t24 = running_clock(86_400 * RATE_HZ, np.float32)
step24 = float(np.float32(t24 + np.float32(T_S)) - t24)
k_more = (131_072 - float(t24)) / step24
print(f"after 24 h: step {step24 * 1e3:.4f} ms, 2^17 s reached after {k_more:,.0f} more ticks"
      f" (true {24 + k_more / RATE_HZ / 3600:.2f} h); there t + 5 ms == t:",
      np.float32(131_072) + np.float32(T_S) == np.float32(131_072))

# --- 3. stamps stored (not accumulated) in float32 -----------------------------------------------
def human(s):
    """A duration in seconds, to three significant figures, with a unit."""
    for unit, scale in (("s", 1.0), ("ms", 1e-3), ("µs", 1e-6), ("ns", 1e-9), ("ps", 1e-12), ("fs", 1e-15)):
        if s >= scale:
            return f"{s / scale:.3g} {unit}"

print("| stamp | float32 spacing | float64 spacing | distinct float32 stamps in the last 1,000 ticks |")
print("|---|---:|---:|---:|")
for name, sec in HORIZONS + (("Unix time, 2026-09-23", 1_790_121_600),):
    s32, s64 = float(np.spacing(np.float32(sec))), float(np.spacing(float(sec)))
    last = np.arange(sec * RATE_HZ - 999, sec * RATE_HZ + 1) / RATE_HZ
    print(f"| {name} | $2^{{{int(np.log2(s32))}}}$ s = {human(s32)} | $2^{{{int(np.log2(s64))}}}$ s = {human(s64)}"
          f" | {np.unique(last.astype(np.float32)).size:,} |")

# --- 4. views and copies on the hour of counts ----------------------------------------------------
counts = shuttle_counts(3_600)
print("| expression | kind | shares memory | counts[4000] after x -= 20480 |")
print("|---|---|---|---:|")
for label, pick in (("c[::4]", lambda c: c[::4]),
                    ("c.reshape(-1, 4)[:, 0]", lambda c: c.reshape(-1, 4)[:, 0]),
                    ("c[c > 0]", lambda c: c[c > 0]),
                    ("c[np.arange(0, c.size, 4)]", lambda c: c[np.arange(0, c.size, 4)]),
                    ("c[::4].copy()", lambda c: c[::4].copy())):
    c = counts.copy()
    x = pick(c)
    kind = "view" if x.base is not None and np.shares_memory(x, c) else "copy"
    x -= 20_480
    print(f"| `{label}` | {kind} | {np.shares_memory(x, c)} | {c[4000]:,} |")

# --- 5. a vectorized speed, checked against a loop ------------------------------------------------
def speed_loop(c, w):
    c = c.tolist()
    denom = N_PER_M * w * T_S
    return np.array([(c[i] - c[i - w]) / denom for i in range(w, len(c))])

def speed_vec(c, w):
    return (c[w:] - c[:-w]) / (N_PER_M * w * T_S)            # two views, one subtraction, one division

print("| window w (ticks) | equal to the loop | values while driving out (m/s) | resolution (m/s) | delay (ms) |")
print("|---:|---|---|---:|---:|")
for w in (1, 4, 20):
    v = speed_vec(counts, w)
    levels = ", ".join(f"{x:.5f}" for x in np.unique(v[2_000:9_000]))
    print(f"| {w} | {np.array_equal(speed_loop(counts, w), v)} | {levels} | {1 / (N_PER_M * w * T_S):.5f} | {w * T_S / 2 * 1e3:.1f} |")

# --- 6. the drive's 16-bit register ---------------------------------------------------------------
raw16 = ((counts + 32_768) % 65_536 - 32_768).astype(np.int16)
k_wrap = int(np.argmax(raw16 < 0))
naive = np.abs(np.diff(raw16.astype(np.int64))).max() / (N_PER_M * T_S)
right = np.diff(raw16)                                       # int16 - int16 wraps back
rebuilt = raw16[0] + np.concatenate(([0], np.cumsum(right)))  # cumsum of int16 accumulates in int64
print(f"register wraps at tick {k_wrap:,}: count {counts[k_wrap]:,} = {counts[k_wrap] / N_PER_M:.4f} m reads {raw16[k_wrap]:,};"
      f" widened-then-differenced max speed {naive:,.1f} m/s; 16-bit differences max {np.abs(right).max() / (N_PER_M * T_S):.4f} m/s;"
      f" rebuilt {rebuilt.dtype} equals the counts: {np.array_equal(rebuilt, counts)}")
```

**Three clocks**, Part 1:

| horizon | ticks | float32 clock (s) | float32 error (s) | float64 error (s) | integer ticks error (s) |
|---|---:|---:|---:|---:|---:|
| 1 min | 12,000 | 60.003613 | +0.003613 | +1.22e-11 | 0.0 |
| 1 h | 720,000 | 3,565.424316 | -34.575684 | +5.54e-08 | 0.0 |
| 8 h | 5,760,000 | 30,532.958984 | +1,732.958984 | +1.37e-06 | 0.0 |
| 24 h | 17,280,000 | 87,019.945312 | +619.945312 | +4.45e-06 | 0.0 |

**Why**, Part 2 — first `scalar loop equals cumsum at 1 h: True`, then the step float32 stores in each binade:

| clock reading (s) | spacing u (s) | 5 ms / u | stored step (ms) | clock rate |
|---|---:|---:|---:|---:|
| 128–256 | $2^{-16}$ | 327.68 | 5.0048828125 | 1.0009766 |
| 256–512 | $2^{-15}$ | 163.84 | 5.0048828125 | 1.0009766 |
| 512–1,024 | $2^{-14}$ | 81.92 | 5.0048828125 | 1.0009766 |
| 1,024–2,048 | $2^{-13}$ | 40.96 | 5.0048828125 | 1.0009766 |
| 2,048–4,096 | $2^{-12}$ | 20.48 | 4.8828125 | 0.9765625 |
| 4,096–8,192 | $2^{-11}$ | 10.24 | 4.8828125 | 0.9765625 |
| 8,192–16,384 | $2^{-10}$ | 5.12 | 4.8828125 | 0.9765625 |
| 16,384–32,768 | $2^{-9}$ | 2.56 | 5.859375 | 1.1718750 |
| 32,768–65,536 | $2^{-8}$ | 1.28 | 3.90625 | 0.7812500 |
| 65,536–131,072 | $2^{-7}$ | 0.64 | 7.8125 | 1.5625000 |
| 131,072–262,144 | $2^{-6}$ | 0.32 | 0.0 | 0.0000000 |

and the rest of Part 2's output:

```text
reads 128 s first at tick 25,607, true 128.035 s, error -0.0307 s
reads 512 s first at tick 102,332, true 511.660 s, error +0.3439 s
reads 2048 s first at tick 409,232, true 2046.160 s, error +1.8424 s
last 1,000 ticks step 4.8828125 ms; Worked case formula -34.575684 s against the run -34.575684 s
error first exceeds 5 ms at tick 16,246 (81.23 s)
error first exceeds 20 ms at tick 21,707 (108.53 s)
error first exceeds 70 ms at tick 46,233 (231.16 s)
after 24 h: step 7.8125 ms, 2^17 s reached after 5,638,663 more ticks (true 31.83 h); there t + 5 ms == t: True
```

**Stamps stored in float32**, Part 3:

| stamp | float32 spacing | float64 spacing | distinct float32 stamps in the last 1,000 ticks |
|---|---:|---:|---:|
| 1 min | $2^{-18}$ s = 3.81 µs | $2^{-47}$ s = 7.11 fs | 1,000 |
| 1 h | $2^{-12}$ s = 244 µs | $2^{-41}$ s = 455 fs | 1,000 |
| 8 h | $2^{-9}$ s = 1.95 ms | $2^{-38}$ s = 3.64 ps | 1,000 |
| 24 h | $2^{-7}$ s = 7.81 ms | $2^{-36}$ s = 14.6 ps | 640 |
| Unix time, 2026-09-23 | $2^{7}$ s = 128 s | $2^{-22}$ s = 238 ns | 1 |

**Views and copies**, Part 4 — each row starts from a fresh copy `c` of the hour's counts, selects the goal-rate samples one way, subtracts $20{,}480$ in place, and reads tick 4,000, where the cart is driving out at count $10{,}240$:

| expression | kind | shares memory | counts[4000] after x -= 20480 |
|---|---|---|---:|
| `c[::4]` | view | True | -10,240 |
| `c.reshape(-1, 4)[:, 0]` | view | True | -10,240 |
| `c[c > 0]` | copy | False | 10,240 |
| `c[np.arange(0, c.size, 4)]` | copy | False | 10,240 |
| `c[::4].copy()` | copy | False | 10,240 |

**The vectorized speed**, Part 5:

| window w (ticks) | equal to the loop | values while driving out (m/s) | resolution (m/s) | delay (ms) |
|---:|---|---|---:|---:|
| 1 | True | 0.48828, 0.58594 | 0.09766 | 2.5 |
| 4 | True | 0.48828, 0.51270 | 0.02441 | 10.0 |
| 20 | True | 0.49805, 0.50293 | 0.00488 | 50.0 |

**The 16-bit register**, Part 6:

```text
register wraps at tick 8,400: count 32,768 = 16.0000 m reads -32,768; widened-then-differenced max speed 6,399.4 m/s; 16-bit differences max 0.5859 m/s; rebuilt int64 equals the counts: True
```

**Reading the tables.** Six things the lecture predicted and the numbers now show.

- **The float32 clock is never right for long, and not even wrong in one direction.** Its error at the four horizons — $+3.6$ ms, $-34.58$ s, $+1{,}733$ s, $+620$ s — is fixed by which binade the reading sits in, and Part 2's column of rates is the whole explanation: $1.0009766$ up to $2048$ s, $0.9765625$ to $16{,}384$ s, then $1.171875$, $0.78125$ and $1.5625$, and $0$ from $2^{17}$ s, where one tick no longer changes the reading. The Worked case's formula, run on the actual entry state, gives the hour's $-34.575684$ s to every printed digit.
- **float64 only postpones it.** Eight to nine orders of magnitude smaller, the running float64 error still grows, $1.37\,\mu\mathrm s$ at 8 h and $4.45\,\mu\mathrm s$ at 24 h; the integer tick count is exact at every horizon because it is never rounded until it is used.
- **Storing is enough to break a stamp.** Without any accumulation, float32's spacing passes the $5$ ms tick between 8 h and 24 h: only $640$ of the day's last $1{,}000$ ticks keep distinct stamps, so a $\Delta p/\Delta t$ divides by zero on the other $360$. Seconds since 1970 in float32 put five seconds of ticks on one stamp.
- **Basic slicing writes through; advanced indexing does not.** The two views move tick 4,000 from $10{,}240$ to $-10{,}240$; the mask, the integer index and `.copy()` leave it alone. The `kind` column is computed from `.base` and `np.shares_memory`, and the last column proves it from the log itself.
- **The vectorized estimate is the loop, exactly.** `True` for all three windows, and the levels are $1/(N\,w\,T)$ apart: resolution bought with delay, $w\,T/2$.
- **Difference in the register's width, accumulate wide.** The register wraps at tick $8{,}400$, $42$ s into the hour, when the cart passes $16.0$ m; the widened difference invents $6{,}399.4\,\mathrm{m/s}$, the 16-bit difference never exceeds the true $0.5859\,\mathrm{m/s}$, and the rebuilt counts match all $720{,}000$.

### 11. What this page does not cover

Python syntax from the start is the official tutorial's job, and the interview-level list of traps — sorting, integer division, recursion limits — is [[02-foundations/algorithms/interview-code|11.7 Interview-Ready Code]]. Packaging your own project for others (a `pyproject.toml`, wheels, publishing), notebooks, the debugger, profiling beyond the one timing of §4, threads and `asyncio` (they are [[02-foundations/tools/concurrency|12.8 Concurrency §8–§9]]), and numerical libraries beyond NumPy are not taught here. Tensors, automatic differentiation and training begin in [[03-deep-learning/foundations/index|1. Learning Systems]], and timing code on a GPU is [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing]]. Writing ROS 2 nodes is [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]], building them is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]], and C++ is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]]. Sampling, quantization and filtering as signal processing are [[02-foundations/signal-processing|6. Signal Processing]]. The shell, Git and the formats a log is saved in are [[02-foundations/tools/linux-shell|12.1]], [[02-foundations/tools/git-research-code|12.2]] and [[02-foundations/tools/config-data-formats|12.4]] of this track.

### After reading

- [ ] Say which interpreter a shell runs and where an `import` finds a package; create a virtual environment, test that you are inside it, and say why nothing is installed into the system Python and what the ROS 2 guide requires of the interpreter.
- [ ] Predict, for any assignment, default argument or copy, whether two names share one object, and show it with `is`.
- [ ] Give an array's dtype, shape, strides and bytes; say which indexing makes a view and which a copy, and check it with `.base` and `np.shares_memory`.
- [ ] Rewrite a loop over samples as one expression on views, prove it equal to the loop, and count the work each does.
- [ ] Compute the spacing of float32 and float64 at any value, and the step a running float clock actually adds in any binade.
- [ ] Derive, by hand, a float32 running clock's drift over an hour, and replace it with an integer tick count.
- [ ] Find where a narrow counter wraps and undo the wrap by differencing in its own width.
- [ ] Make a random draw replayable with an owned, seeded generator, and say what else must be pinned.
- [ ] Structure a script as functions, a frozen config, a log file and a `main()` behind the entry-point guard.
- [ ] Validate a function's inputs with an explicit `raise`, guard your own invariants with `assert`, and write a regression test with a deliberately chosen tolerance, run with pytest.

### Self-check

1. `a = np.arange(4); b = a[1:]; b[0] = 9` — what is `a` now? And after the same three lines with `a = list(range(4))`?
2. Why does P6's float32 running clock read $3565.42$ s after one true hour, and what representation of time avoids the problem entirely?
3. On the page's shuttle, when and where does the 16-bit count register wrap, and why does `np.diff` of its `int16` readings still give the right speed?
4. A script calls `np.random.seed(0)` at the top and adds simulated encoder noise. A colleague adds a plot that jitters its markers with `np.random.random`, and the published noise changes. Why, and what is the fix?
5. `math.isclose(err, 0.0)` returns `False` for `err = 5.5e-8` s. Why, and what should the call be?
6. A labmate ran `sudo pip install numpy --upgrade` on the robot computer to get a newer NumPy, and now ROS 2's Python tools misbehave. What went wrong, and what should they have done?
7. Your regression test pins $-34.57568359375$ s with a tolerance of $10^{-9}$ s. When is so tight a tolerance legitimate, and when must it be larger?

> [!tip]- Answers
> 1. `array([0, 9, 2, 3])`: `a[1:]` is a view, so writing `b[0]` writes `a[1]`. With a list, `a[1:]` is a shallow copy, so `a` stays `[0, 1, 2, 3]` and only `b` changes.
> 2. Past $2048$ s float32 values are $u=2^{-12}$ s apart, and $0.005/u=20.48$, so every tick's sum is rounded to $20u=4.8828$ ms: the clock runs $2.34\%$ slow for the last $26$ minutes after running $0.098\%$ fast before, and ends $34.58$ s behind. Keep an integer tick count, exact in 64 bits, and compute $t=k/200$ only when a time is needed — one rounding, never an accumulated one.
> 3. At tick $8{,}400$, $42$ s into the hour, when the count reaches $32{,}768$ and the cart passes $16.0$ m; the reading jumps from $32{,}762$ to $-32{,}768$. A difference taken in 16 bits is exact whenever the true change is smaller than $2^{15}$ counts, and P6 moves at most 6 counts a tick, so the wrap cancels; widening to 64 bits first keeps the jump and makes a $6{,}399.4\,\mathrm{m/s}$ spike.
> 4. The legacy functions share one global stream, so the plot's draw consumes numbers the noise used to get, and every later draw moves. Give the noise its own generator — `rng = np.random.default_rng(seed)`, passed to the function that draws, or one `spawn`ed child per trial — so no other code can reach its stream; and pin NumPy, since the stream is guaranteed only on the same build.
> 5. The relative term is $10^{-9}\times\max(5.5\times10^{-8},\,0)=5.5\times10^{-17}$, far below the difference, and against zero there is no other term: no nonzero value is ever relatively close to zero. Give the tolerance in the quantity's units: `math.isclose(err, 0.0, abs_tol=1e-6)` for "within a microsecond".
> 6. They upgraded, with root, a package that the distribution's tools and the ROS 2 binaries were built and tested against, which is what Python's documentation warns can interfere with the system package manager and the system's other components, and what Ubuntu's pip refuses by default. The fix is a rosdep key or the apt package `python3-numpy` for what ROS needs, and for a newer version a virtual environment made with the system `python3` in the workspace, marked `COLCON_IGNORE` (§1).
> 7. When the value comes from a fixed sequence of correctly rounded operations in one dtype — here float32 additions in order — so every IEEE machine reproduces it to the bit; then $10^{-9}$ s only absorbs printing. When the order or grouping of floating-point operations can change — `np.sum`'s pairwise summation, threaded linear algebra, GPU reductions, a new library version — the tolerance must cover that change, and it should be written down with its reason; an integer result takes $0$.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and [[02-foundations/lab-plants|0.6 Lab Plants]]. The object is P6's log; every problem changes a knob — the clock's period, a counter's width, the window — so no number on the page can be copied.

1. **Draw.** The picture above for P6's $50\,\mathrm{Hz}$ vision clock, which keeps its own time with `t += 0.02` in float32: (a) the float32 grid near $3600$ s with the exact sum and the stored step, and what each tick gains or loses, in spacings and in ms; (b) the error over one true hour, with the binade crossings you can compute, its value at the hour, and where a float64 clock and an integer tick count lie.
2. **Derive.** (a) Show that a float32 clock stepping $4T$ reads, after any number of ticks $k$, exactly four times what a float32 clock stepping $T$ reads after the same $k$; use that multiplying by a power of two changes only the exponent. From §10's crossing at $512$ s and the rate on $[512, 1024)$, compute the 20 ms clock's error after one true hour. (b) Give the stored step and the rate of the 20 ms clock on $[8192, 16384)$ s, and the reading at which it stops advancing, with the true time at which it gets there. (c) Find where each counter wraps: the drive's 16-bit register and a signed 32-bit count, in metres of P6's travel; a 32-bit microsecond timer, in minutes, and the 50 Hz vision tick at which it first wraps. Show that the difference of two timer readings taken in the timer's own unsigned width equals the true interval whenever that interval is shorter than $2^{32}\,\mu\mathrm s$. (d) Give the memory of the one-hour count column as `int16`, `int32` and `int64`; of a 24-hour log with a 64-bit tick column and a 64-bit count column; and of the one-hour counts as a Python list at up to 36 bytes a sample.
3. **Do.** Fill the `?` blanks and run the block after §10's lab. Report (a) the three-clock table for the 50 Hz vision clock at 1 min, 1 h, 8 h and 24 h; (b) the ratio of the 20 ms and 5 ms float32 clocks after the same $180{,}000$ ticks; (c) the goal-rate speed from `counts[::4]` over windows of 1 and 5 vision periods, with its resolution; (d) a 32-bit microsecond stamp at 50 Hz over two hours — where it wraps, and the range of its differences in 64 bits and in its own width. Compare each with the 5 ms results of §10.
4. **Interpret.** A labmate's script, below, computes P6's speed from the one-hour log saved as a `(720000, 2)` `int64` array of ticks and counts. It runs without an error. Name at least six mistakes, the section each belongs to, what each does to the result on P6's log, and the fix.

```python
# Problem 3 (Do). P6's 50 Hz vision clock and a 32-bit microsecond timer. Fill each ?, then run after the lab (§10).
VISION_HZ = 50                                   # P6's goal rate
T_V = ?                                          # one vision period, s

print("| horizon | vision ticks | float32 clock (s) | float32 error (s) | float64 error (s) |")
print("|---|---:|---:|---:|---:|")
for name, sec in HORIZONS:
    n = ?                                        # vision ticks in this horizon
    c32 = float(running_clock(n, np.float32, step=T_V))
    c64 = float(running_clock(n, np.float64, step=T_V))
    print(f"| {name} | {n:,} | {c32:,.6f} | {c32 - sec:+,.6f} | {c64 - sec:+.2e} |")

k = 180_000                                      # one hour of vision ticks
ratio = float(running_clock(k, np.float32, step=T_V)) / float(running_clock(k, np.float32, step=?))
print("20 ms clock / 5 ms clock after the same", f"{k:,}", "ticks:", ratio)

goal_counts = ?                                  # P6's counts at the goal instants, from the 200 Hz shuttle
for w in (1, 5):
    v = (goal_counts[w:] - goal_counts[:-w]) / ?                  # m/s over w vision periods
    levels = ", ".join(f"{x:.5f}" for x in np.unique(v[500:1_800]))
    print(f"w = {w} vision periods: {levels} m/s, resolution {1 / (N_PER_M * w * T_V):.5f} m/s")

stamp_us = (np.arange(2 * 3600 * VISION_HZ) * 20_000) % ?       # a 32-bit microsecond timer, 2 h
k_wrap = int(np.argmax(np.diff(stamp_us) < 0)) + 1
dt_wide = np.diff(stamp_us)                      # int64 differences
dt_u32 = np.diff(stamp_us.astype(?))             # differences in the timer's own width
print(f"wraps at vision tick {k_wrap:,} ({k_wrap / VISION_HZ / 60:.2f} min);"
      f" int64 differences {dt_wide.min():,} to {dt_wide.max():,} us; uint32 differences {dt_u32.min():,} to {dt_u32.max():,} us")
```

The labmate's script for problem 4:

```python
# not-run: a labmate's analysis script with at least six mistakes, for problem 4
import numpy as np

def load_log(path, cache=[]):
    cache.append(np.load(path))                  # (720000, 2) int64: tick, count
    return cache[-1]

def speed(path):
    log = load_log(path)
    t = np.zeros(len(log), dtype=np.float32)
    for i in range(1, len(log)):                 # rebuild the time column
        t[i] = t[i - 1] + 0.005
    small = log[:, 1].astype(np.int16)           # halve the memory
    v = np.diff(small.astype(np.int64)) / 2048 / np.diff(t)
    mid = log[:, 1]
    mid -= 20_480                                # positions about mid-rail, for the plot
    np.random.seed(0)
    return v + np.random.normal(0.0, 0.01, v.size), mid
```

> [!note]- How to draw it · 그리는 법
> - Draw the float32 grid around the reading with its spacing $u=2^{e-23}$ labelled in seconds and in ms; mark the exact sum at $T/u$ spacings and the stored value at $\mathrm{round}(T/u)$ spacings, and write the difference in spacings and in ms.
> - Plot the error, reading minus true time, against true time. A plot of the reading itself hides a $2.9$ s error in $3600$ s under the line's width.
> - Mark where the reading crosses powers of two: the slope changes only there and is constant between. For a clock scaled by four, every crossing moves to four times the reading.
> - Scale the error axis to the largest error over the hour, not to its end value; the 5 ms clock was $1.84$ s ahead before it was $34.58$ s behind.
> - Put float64 and the integer tick count on the same axes as a line at zero, labelled with their actual errors, which are far below a pixel.
> - Label the value at the hour and, for P6, where the error passes one control period and the $70\,\mathrm{ms}$ budget.

> [!tip]- Solutions
> 1. Near $3600$ s the spacing is still $u=2^{-12}$ s, and $0.02/u=81.92$ rounds up to $82$: each tick adds $82u=20.01953125$ ms, gaining $0.08u=0.0195$ ms, $0.098\%$ fast. Over the hour the 20 ms clock is the 5 ms clock scaled by four (problem 2a), so §10's crossings move with it: it reads $512$ s at tick $25{,}607$, true $512.14$ s, $0.12$ s behind, and $2048$ s at tick $102{,}332$, true $2046.64$ s, $1.38$ s ahead, and it reads $3602.89$ s at the hour, $2.89$ s ahead — a small dip to $-0.12$ s at $512$ s, then a straight rise at $2^{-10}$. Its first slow binade begins at a reading of $8192$ s, beyond the hour. A float64 clock ends the hour $3.0$ ns off and an integer tick count at $0$, both on the zero line.
> 2. (a) Write $\mathrm{fl}$ for rounding to float32. Multiplying by $4=2^2$ changes only the exponent, so $\mathrm{fl}(4x)=4\,\mathrm{fl}(x)$ for any $x$ in the normal range; hence $\mathrm{fl}(0.02)=4\,\mathrm{fl}(0.005)$, and if $\hat t'_k=4\hat t_k$ then $\hat t'_{k+1}=\mathrm{fl}\big(4\hat t_k+4\,\mathrm{fl}(T)\big)=4\,\mathrm{fl}\big(\hat t_k+\mathrm{fl}(T)\big)=4\hat t_{k+1}$. From $\hat t'_0=\hat t_0=0$ the two clocks differ by a factor of exactly four at every tick, and so do their errors, since $k\cdot4T=4\cdot kT$. One true hour of the vision clock is $k=180{,}000$ ticks, when the 5 ms clock has run $900$ s; it read $512$ s at true $511.66$ s, $+0.3439$ s, and on $[512,1024)$ it gains $2^{-10}$, so at $900$ s its error is $0.3439+(900-511.66)\times2^{-10}=0.723$ s, and the vision clock's error after one hour is $4\times0.723=+2.89$ s. The Do run prints $+2.892578$ s. (b) On $[8192,16384)$ s, $u=2^{-10}$ s and $0.02/u=20.48$ rounds down to $20$: the step is $19.53125$ ms and the rate $0.9765625$, $2.34\%$ slow — four times the 5 ms clock's $[2048,4096)$. It stops where $0.02/u$ rounds to $0$, first at $u=2^{-4}$ s, whose binade starts at $2^{19}=524{,}288$ s, four times $2^{17}$. By (a) it gets there after the same number of ticks as the 5 ms clock, $17{,}280{,}000+5{,}638{,}663=22{,}918{,}663$, which at $20$ ms is $458{,}373$ s of true time, $127.33$ h, four times $31.83$ h. (c) The register holds $[-32{,}768,\ 32{,}767]$ and wraps when the count reaches $32{,}768$, at $32{,}768/2048=16$ m; a signed 32-bit count wraps at $2^{31}/2048=1{,}048{,}576$ m. A 32-bit microsecond timer wraps every $2^{32}\,\mu\mathrm s=4294.97$ s $=71.58$ min; vision tick $k$ reads $20{,}000\,k\bmod 2^{32}$, which first falls below its predecessor at $k=\lceil2^{32}/20{,}000\rceil=214{,}749$. For true times $a\le b$ with $b-a<2^{32}$, the readings are $a\bmod2^{32}$ and $b\bmod2^{32}$, and their difference reduced modulo $2^{32}$ is $(b-a)\bmod2^{32}=b-a$, since reduction commutes with subtraction and $b-a$ is already in range — and unsigned 32-bit subtraction is exactly subtraction modulo $2^{32}$. (d) $720{,}000$ counts take $1.44$ MB as `int16`, $2.88$ MB as `int32` and $5.76$ MB as `int64`; a day's log with two 64-bit columns takes $17{,}280{,}000\times16=276.48$ MB; the hour as a list at up to 36 bytes a sample, up to $25.9$ MB. All of it fits in a laptop's memory. What the day's log needs is not less memory but the right types: a 64-bit tick column rather than float32 seconds (§5), and a count column wide enough, or differenced in its own width (§6).
> 3. Blanks: `1 / VISION_HZ`, `sec * VISION_HZ`, `T_S`, `shuttle_counts(3_600)[::4]`, `(N_PER_M * w * T_V)`, `2**32` and `np.uint32`. The filled block, which the page checker runs after the lab:
>
> ```python
> # Problem 3 (Do), filled in. Run after the lab: it reuses running_clock and shuttle_counts from §10.
> VISION_HZ = 50                                   # P6's goal rate
> T_V = 1 / VISION_HZ                              # one vision period, 0.02 s
> 
> print("| horizon | vision ticks | float32 clock (s) | float32 error (s) | float64 error (s) |")
> print("|---|---:|---:|---:|---:|")
> for name, sec in HORIZONS:
>     n = sec * VISION_HZ
>     c32 = float(running_clock(n, np.float32, step=T_V))
>     c64 = float(running_clock(n, np.float64, step=T_V))
>     print(f"| {name} | {n:,} | {c32:,.6f} | {c32 - sec:+,.6f} | {c64 - sec:+.2e} |")
> 
> k = 180_000                                      # one hour of vision ticks
> ratio = float(running_clock(k, np.float32, step=T_V)) / float(running_clock(k, np.float32, step=T_S))
> print("20 ms clock / 5 ms clock after the same", f"{k:,}", "ticks:", ratio)
> 
> goal_counts = shuttle_counts(3_600)[::4]         # P6's counts at the goal instants
> for w in (1, 5):
>     v = (goal_counts[w:] - goal_counts[:-w]) / (N_PER_M * w * T_V)
>     levels = ", ".join(f"{x:.5f}" for x in np.unique(v[500:1_800]))
>     print(f"w = {w} vision periods: {levels} m/s, resolution {1 / (N_PER_M * w * T_V):.5f} m/s")
> 
> stamp_us = (np.arange(2 * 3600 * VISION_HZ) * 20_000) % 2**32       # a 32-bit microsecond timer, 2 h
> k_wrap = int(np.argmax(np.diff(stamp_us) < 0)) + 1
> dt_wide = np.diff(stamp_us)                      # int64 differences: wrong across the wrap
> dt_u32 = np.diff(stamp_us.astype(np.uint32))     # 32-bit unsigned differences: wrap back
> print(f"wraps at vision tick {k_wrap:,} ({k_wrap / VISION_HZ / 60:.2f} min);"
>       f" int64 differences {dt_wide.min():,} to {dt_wide.max():,} us; uint32 differences {dt_u32.min():,} to {dt_u32.max():,} us")
> ```
>
> Its output:
>
> ```text
> | horizon | vision ticks | float32 clock (s) | float32 error (s) | float64 error (s) |
> |---|---:|---:|---:|---:|
> | 1 min | 3,000 | 60.001183 | +0.001183 | +3.78e-12 |
> | 1 h | 180,000 | 3,602.892578 | +2.892578 | -2.98e-09 |
> | 8 h | 1,440,000 | 28,324.197266 | -475.802734 | +5.36e-07 |
> | 24 h | 4,320,000 | 88,381.835938 | +1,981.835938 | -3.72e-07 |
> 20 ms clock / 5 ms clock after the same 180,000 ticks: 4.0
> w = 1 vision periods: 0.48828, 0.51270 m/s, resolution 0.02441 m/s
> w = 5 vision periods: 0.49805, 0.50293 m/s, resolution 0.00488 m/s
> wraps at vision tick 214,749 (71.58 min); int64 differences -4,294,947,296 to 20,000 us; uint32 differences 20,000 to 20,000 us
> ```
>
> (a) After one hour the vision clock is $2.89$ s *ahead* where the 5 ms clock was $34.58$ s behind: with a period four times longer, the same pattern of binades arrives at four times the reading, so at the hour it is still in the fast binades the 5 ms clock left at $2048$ s; it is $475.80$ s behind at 8 h and $1{,}981.84$ s ahead at 24 h. Its float64 errors, $-2.98$ ns at 1 h and $-3.72\times10^{-7}$ s at 24 h, come from a quarter as many additions. (b) The ratio is exactly $4.0$, as problem 2(a) proves. (c) One vision period gives $0.48828$ or $0.51270\,\mathrm{m/s}$, resolution $0.02441\,\mathrm{m/s}$, and five give $0.49805$ or $0.50293$, resolution $0.00488$ — the same as §10's 200 Hz windows of 4 and 20 ticks, because the resolution is $1/(N\cdot\text{window duration})$ whatever the rate. (d) The timer wraps at vision tick $214{,}749$, $71.58$ min; the 64-bit differences run from $-4{,}294{,}947{,}296$ to $20{,}000\,\mu\mathrm s$, the wrap showing as a negative interval of almost $2^{32}$, while the 32-bit differences are $20{,}000\,\mu\mathrm s$ everywhere — §6's rule for the register, applied to time.
> 4. Six mistakes, checked by running the script on the page's hour of counts on the Mac:
>    - **§2, a mutable default.** `cache=[]` is one list for the whole process: every call appends another $11.52$ MB log that is never freed, and the arrays kept there are the ones the fifth mistake rewrites. Fix: no default container; a cache, if needed, owned by the caller.
>    - **§4, a Python loop over $719{,}999$ ticks** to rebuild a column the file already holds. Fix: `t = log[:, 0] / 200`.
>    - **§5, a float32 running clock.** The time column ends the hour $34.58$ s short, and from $2046$ s on every `np.diff(t)` is $4.8828$ ms, so every speed in the last $26$ minutes is $2.4\%$ high — $0.5$ and $0.6\,\mathrm{m/s}$ where the counts say $0.48828$ and $0.58594$. Fix: the integer ticks, as above.
>    - **§6, a narrow type widened before differencing.** `astype(np.int16)` keeps only the low 16 bits of counts above $32{,}767$ — $40{,}960$ became $-24{,}576$ on the Mac — and widening before `np.diff` turns every wrap into a spike, the largest $6{,}553\,\mathrm{m/s}$ with the float32 time step. Fix: keep the `int64` counts, or difference the `int16` values in 16 bits and accumulate wide.
>    - **§3, an in-place write through a view.** `mid = log[:, 1]` is a view, so `mid -= 20_480` rewrites the loaded log, and the cached one: tick 4,000 reads $-10{,}240$ afterwards. Fix: `mid = log[:, 1] - 20_480`.
>    - **§7, a global seed.** `np.random.seed(0)` inside the function resets the process-wide stream on every call, so the caller's own seeded draws after it are no longer the ones it seeded, and the noise is only reproducible while no other code draws from that stream. Fix: take a `Generator` argument and call `rng.normal`.

### Sources

- Python 3 documentation ([docs.python.org](https://docs.python.org/3/), 3.14 pages, read 2026-09-23) — [Installing Python Modules](https://docs.python.org/3/installing/index.html) (not into the system Python), [venv](https://docs.python.org/3/library/venv.html) (`pyvenv.cfg`, `sys.prefix != sys.base_prefix`, not movable), tutorial [§12](https://docs.python.org/3/tutorial/venv.html) (`pip freeze`, `-r requirements.txt`), [§6.1.2](https://docs.python.org/3/tutorial/modules.html) (the module search path), [§4.9.1](https://docs.python.org/3/tutorial/controlflow.html) and [reference §8.7](https://docs.python.org/3/reference/compound_stmts.html) (defaults evaluated once), [reference §3.1](https://docs.python.org/3/reference/datamodel.html) (identity, mutability), [reference §7.3](https://docs.python.org/3/reference/simple_stmts.html) (`assert` removed under `-O`), [tutorial §15](https://docs.python.org/3/tutorial/floatingpoint.html) (binary64); library pages `copy`, `math` (`isclose`, `ulp`), `random`, `__main__`, `dataclasses` (`frozen`, unhashable defaults refused since 3.11, `replace`), `typing`, `logging` (`basicConfig` and `force=True`), `argparse`.
- NumPy 2.5 documentation ([numpy.org/doc/stable](https://numpy.org/doc/stable/)) — [the N-dimensional array](https://numpy.org/doc/stable/reference/arrays.ndarray.html) (strided offsets), [copies and views](https://numpy.org/doc/stable/user/basics.copies.html), [data types and overflow](https://numpy.org/doc/stable/user/basics.types.html), `cumsum`, `spacing`, `isclose`; [random generator](https://numpy.org/doc/stable/reference/random/generator.html) (`default_rng`, PCG64, `spawn`), [random sampling](https://numpy.org/doc/stable/reference/random/index.html) (the legacy global `RandomState`), [compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html) (same stream only on the same build); [NumPy 2.0 migration guide](https://numpy.org/doc/stable/numpy_2_0_migration_guide.html) (64-bit default integer) and [NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html) (Python scalars weakly typed).
- ROS 2 documentation, jazzy — [Using Python Packages with ROS 2](https://github.com/ros2/ros2_documentation/blob/jazzy/source/How-To-Guides/Using-Python-Packages.rst): the interpreter must match the binaries; rosdep, the system package manager, a virtual environment marked `COLCON_IGNORE`; Bloom and rosdep keys.
- ROS 2 sources, jazzy — [Time.msg](https://github.com/ros2/rcl_interfaces/blob/jazzy/builtin_interfaces/msg/Time.msg) (`int32 sec`, `uint32 nanosec`), [rcutils time.h](https://github.com/ros2/rcutils/blob/jazzy/include/rcutils/time.h) (`int64_t` nanoseconds), [rclpy time.py](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/time.py) (`OverflowError` at $2^{63}$).
- REP 2000 ([ros-infrastructure/rep](https://github.com/ros-infrastructure/rep/blob/master/rep-2000.rst)) — Jazzy on Ubuntu 24.04 with Python 3.12.3.
- Ubuntu, [Develop with Python on Ubuntu](https://ubuntu.com/developers/docs/tutorials/python-use/) — the "externally managed environment" error, `apt install python3-xyz` or a venv, PEP 668.
- pytest documentation ([docs.pytest.org](https://docs.pytest.org/en/stable/)) — test discovery, plain `assert`, `pytest.raises`, `pytest.approx` (relative $10^{-6}$, absolute $10^{-12}$ by default).

## 한국어

*[[02-foundations/lab-plants|0.6 Lab Plants]]와 [[02-foundations/lab-kernel|0.7 Lab Kernel]] 위에 서고, [[02-foundations/algorithms/interview-code|11.7 Python·C++ 인터뷰용 코드]]의 Python 습관을 로봇의 데이터에 적용한다. 장치 **P6**의 후속 사용이다. [[04-robotics/ros2/index|25. ROS 2]]가 P6을 돌리고 [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]이 거기에 잡음을 준다. 여기서 P6은 디스크 위의 데이터다. 워크스테이션의 분석 스크립트가 읽는 한 시간 분량의 로그다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]의 물리 AI 스택 아래 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 모든 층의 연구 코드 — 인식 모델, 계획기, 학습된 정책, 그리고 그 시행의 분석 — 가 Python으로 쓰이고 배열 위에서 돌며, 그 절의 예 "저 패널을 프레임에 설치해"에서 이 페이지는 "접촉을 감지하고"와 "완료를 검증한다"가 기록된 카운트와 타임스탬프로 계산한 숫자가 되는 자리다. 이것이 없으면 그 숫자들이 오류 메시지 없이 틀린다 — 한 시간에 34.58 s 어긋나는 float32 시계, 원시 로그를 다시 쓰는 뷰, 한 바퀴 도는 16비트 카운터, 누가 그림 하나를 더하자 재생되지 않는 시드. 블록 1의 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학]]부터 모든 Tier A 실습이 NumPy로 돌고 [[05-construction-robotics/imitating-contact|10. 접촉 모방 §9]]는 시드를 준 시작점 2,000개 위에서 정책을 학습하고 채점하는데, 이 페이지는 [[07-research-program/index|학위논문 경로(연구 프로그램 §8)]]의 일곱 블록 밖에 있으므로 숫자를 남길 첫 실습과 함께 — 늦어도 블록 1의 10 실습 전에 — 읽고, 블록 4의 학습 페이지 전에 §7을 다시 읽는다. 다 읽으면 방어할 수 있는 숫자를 내는 분석 코드 — 격리되고 고정되며, 필요한 곳에서 정확하고, 벡터화되고, 재생 가능하고, 검사된 코드 — 를 쓸 수 있다.

> [!note] 처음이라면 · First pass
> 두 회차로 읽는다. **1회차**(약 90분): 이 페이지의 대상, 그림, 그리고 계산기를 들고 따라가는 계산 절 — 한 시간 동안 세 가지 방식으로 간직한 P6의 시계 — 그다음 계산 절이 쓴 것을 유도하는 §5와, 감기는 정수 §6. 스스로 점검 2와 3으로 마친다. **2회차**(약 90분): §2–§4 — 이름과 가변성, 배열과 뷰, 벡터화 — 그다음 §10의 실습을 돌려 그 표를 페이지와 맞춰 본다. 스스로 점검 1과 5로 마친다. 로봇 컴퓨터에 무엇이든 설치하기 전에는 §1을, 잡음을 시뮬레이션하거나 데이터를 나누기 전에는 §7을, 스크립트를 되풀이해 돌리게 되면 §8–§9를 읽고, 과제는 맨 마지막에 푼다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** — 엔코더가 $2048$ counts/m인 직선 위의 카트, 그것을 $200\,\mathrm{Hz}$로 샘플하는 제어기, $50\,\mathrm{Hz}$로 목표를 내는 비전 노드 — 를, 그것이 디스크에 남기는 것으로 본다. 카탈로그는 카트를 고정하고, 이 페이지는 한 시간 분량의 로그와 그 로그를 만든 움직임을 고정한다. *페이지 고유*로 표시한 행은 산수가 깔끔하도록 고른 이 페이지의 교과용 숫자이며 측정값이 아니다. P6의 카탈로그 숫자는 그대로다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $N$ | $2048$ counts/m | P6의 엔코더. 한 카운트는 $1/2048\,\mathrm m=0.488\,\mathrm{mm}$ |
| $f$, $T$ | $200\,\mathrm{Hz}$, $5\,\mathrm{ms}$ | P6의 제어 주기. 틱 하나에 로그 한 행 |
| $f_v$ | $50\,\mathrm{Hz}$ | P6의 목표 주기. 네 번째 틱마다 |
| $D$ | $1\,\mathrm h$ | 로그 하나: 틱 $720{,}000$개, 목표 $180{,}000$개 *(페이지 고유)* |
| $L$ | $20\,\mathrm m$ | 레일 *(페이지 고유)* |
| $v$ | $0.5\,\mathrm{m/s}$ | 왕복 속도: $1024$ counts/s, 틱당 $5.12$ 카운트 *(페이지 고유)* |
| 한 주기 | $100\,\mathrm s$ | $0\,\mathrm m$에서 $10\,\mathrm s$, $20\,\mathrm m$까지 $40\,\mathrm s$, 거기서 $10\,\mathrm s$, 돌아오는 데 $40\,\mathrm s$. 한 시간에 $36$번 *(페이지 고유)* |
| 레지스터 | 16비트, 부호 있음 | 모터 드라이브의 원시 카운트 레지스터. 틱마다 읽는다 *(페이지 고유)* |
| 로그 열 | 틱 $k$, 카운트 $c_k$ | 둘 다 64비트 정수, $c_k=\lfloor 2048\,p(kT)\rfloor$ *(페이지 고유)* |

카운트는 틱의 정확한 정수 함수다. $0.5\,\mathrm{m/s}$에서 카트는 틱마다 $2048\times0.5\times0.005=5.12$ 카운트를 나아가므로, 움직이는 동안 로그는 5와 6 카운트의 걸음을 번갈아 적는다. [[04-robotics/modern-robotics/ch13-wheeled-mobile-robots|MR 13장]]이 P6의 바퀴에서 찾는 바로 그 $5.12$다. 대상 안에 무작위는 없다. §7이 잡음을 더할 때는 그렇다고 밝힌다.

*범위: 이 페이지는 로봇 학습 연구자가 숫자를 맞게, 그리고 빨리 얻는 데 필요한 Python을 가르친다. 격리되고 버전이 고정된 환경, 이름과 가변성, NumPy 배열과 뷰, 벡터화, 로봇 로그를 무는 부동소수점과 정수의 한계, 다시 재생할 수 있는 무작위성, 그리고 스크립트를 다시 돌릴 수 있게 만드는 구조와 점검이다. Python 문법을 처음부터 가르치지는 않는다. 그것은 공식 튜토리얼의 몫이다. 텐서와 학습도 아니다. 그것은 [[03-deep-learning/foundations/index|1. 학습 시스템]]에서 시작하고, GPU 위에서 시간을 재는 법은 [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산 §7]]이다. ROS 2 노드 코드는 [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]], C++은 [[04-robotics/ros2/cpp-for-robot-code|25.0 로봇 코드를 위한 C++]]이다. 나머지와 그것이 사는 곳은 §11이 적는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 440" style="max-width:100%;height:auto" role="img" aria-label="패널 두 개. (a) 3600초 근처의 float32 값을 늘어놓은 자. 간격 u는 2의 마이너스 12제곱 초, 0.244밀리초다. 정확한 합 t 더하기 5밀리초는 20.48 u에 떨어지고, 저장되는 값은 가장 가까운 눈금인 t 더하기 20 u, 4.8828밀리초라서 틱마다 0.117밀리초를 잃는다. (b) 참 시간 한 시간 동안 P6의 float32 누적 시계의 오차. 조금 빠르게 가다가 34.1분에 2048초를 읽을 때 플러스 1.84초에 이르고, 그 뒤 2.34퍼센트 느리게 가서 3565.42초를 읽을 때 마이너스 34.58초로 끝난다. 55나노초 틀린 float64 시계와 정확한 정수 틱 카운트는 영점의 점선 위에 있다.">
  <defs><marker id="pyrcarrk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" fill="currentColor">(a) t = 3600 s 근처의 한 틱, float32로 저장</text>
  <text x="40" y="38" font-size="11" fill="currentColor">정확한 합: t + 5 ms = t + 20.48 u</text>
  <line x1="40" y1="46" x2="488.6" y2="46" stroke="currentColor" stroke-width="1.3" marker-end="url(#pyrcarrk)"/>
  <line x1="490.6" y1="46" x2="490.6" y2="70" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <line x1="40" y1="70" x2="502" y2="70" stroke="currentColor" stroke-width="1"/>
  <g stroke="currentColor" stroke-width="1"><line x1="40" y1="61" x2="40" y2="79"/><line x1="62" y1="65" x2="62" y2="75"/><line x1="84" y1="65" x2="84" y2="75"/><line x1="106" y1="65" x2="106" y2="75"/><line x1="128" y1="65" x2="128" y2="75"/><line x1="150" y1="61" x2="150" y2="79"/><line x1="172" y1="65" x2="172" y2="75"/><line x1="194" y1="65" x2="194" y2="75"/><line x1="216" y1="65" x2="216" y2="75"/><line x1="238" y1="65" x2="238" y2="75"/><line x1="260" y1="61" x2="260" y2="79"/><line x1="282" y1="65" x2="282" y2="75"/><line x1="304" y1="65" x2="304" y2="75"/><line x1="326" y1="65" x2="326" y2="75"/><line x1="348" y1="65" x2="348" y2="75"/><line x1="370" y1="61" x2="370" y2="79"/><line x1="392" y1="65" x2="392" y2="75"/><line x1="414" y1="65" x2="414" y2="75"/><line x1="436" y1="65" x2="436" y2="75"/><line x1="458" y1="65" x2="458" y2="75"/><line x1="480" y1="59" x2="480" y2="81" stroke-width="1.8"/><line x1="502" y1="65" x2="502" y2="75"/></g>
  <text x="40" y="92" font-size="10" fill="currentColor" text-anchor="middle">t</text>
  <text x="150" y="92" font-size="10" fill="currentColor" text-anchor="middle">+5 u</text>
  <text x="260" y="92" font-size="10" fill="currentColor" text-anchor="middle">+10 u</text>
  <text x="370" y="92" font-size="10" fill="currentColor" text-anchor="middle">+15 u</text>
  <text x="466" y="92" font-size="10" fill="currentColor" text-anchor="middle">+20 u</text>
  <line x1="480" y1="81" x2="480" y2="104" stroke="currentColor" stroke-width="0.9" stroke-dasharray="3 2"/>
  <line x1="40" y1="104" x2="478" y2="104" stroke="currentColor" stroke-width="1.8" marker-end="url(#pyrcarrk)"/>
  <text x="40" y="120" font-size="11" fill="currentColor">저장: 가장 가까운 눈금, t + 20 u = t + 4.8828 ms</text>
  <text x="556" y="120" font-size="11" fill="currentColor" text-anchor="end">잃는 양: 0.117 ms</text>
  <text x="12" y="140" font-size="11" fill="currentColor" fill-opacity="0.8">눈금: [2048, 4096) s의 float32 값, 간격 u = 2⁻¹² s = 0.244 ms</text>
  <text x="12" y="166" font-size="12" fill="currentColor">(b) P6의 float32 누적 시계, 한 시간: 오차 = 읽은 값 − 참 시간</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.7" fill="none"><line x1="60" y1="176" x2="60" y2="406"/><line x1="60" y1="406" x2="540" y2="406"/></g>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.15"><line x1="60" y1="256.5" x2="540" y2="256.5"/><line x1="60" y1="314" x2="540" y2="314"/><line x1="60" y1="371.5" x2="540" y2="371.5"/></g>
  <line x1="60" y1="199" x2="540" y2="199" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3" stroke-opacity="0.8"/>
  <text x="52" y="203" font-size="10" fill="currentColor" text-anchor="end">0 s</text>
  <text x="52" y="260.5" font-size="10" fill="currentColor" text-anchor="end">−10</text>
  <text x="52" y="318" font-size="10" fill="currentColor" text-anchor="end">−20</text>
  <text x="52" y="375.5" font-size="10" fill="currentColor" text-anchor="end">−30</text>
  <g stroke="currentColor" stroke-width="1" stroke-opacity="0.7"><line x1="60" y1="406" x2="60" y2="410"/><line x1="180" y1="406" x2="180" y2="410"/><line x1="300" y1="406" x2="300" y2="410"/><line x1="420" y1="406" x2="420" y2="410"/><line x1="540" y1="406" x2="540" y2="410"/></g>
  <text x="60" y="421" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <text x="180" y="421" font-size="10" fill="currentColor" text-anchor="middle">15</text>
  <text x="300" y="421" font-size="10" fill="currentColor" text-anchor="middle">30</text>
  <text x="420" y="421" font-size="10" fill="currentColor" text-anchor="middle">45</text>
  <text x="540" y="421" font-size="10" fill="currentColor" text-anchor="end">60분</text>
  <text x="300" y="435" font-size="10" fill="currentColor" text-anchor="middle">참 시간</text>
  <polyline points="60.0,199.0 77.1,199.2 94.1,198.5 128.2,197.0 196.4,194.2 332.8,188.4 540.0,397.8" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <g fill="currentColor"><circle cx="94.1" cy="198.5" r="2"/><circle cx="128.2" cy="197.0" r="2"/><circle cx="196.4" cy="194.2" r="2"/><circle cx="332.8" cy="188.4" r="3.2"/><circle cx="540" cy="397.8" r="3.2"/></g>
  <text x="200" y="183" font-size="11" fill="currentColor" text-anchor="middle">0.098 % 빠름: 틱당 5.0049 ms</text>
  <text x="340" y="180" font-size="11" fill="currentColor">34.1분에 2048 s를 읽음, +1.84 s</text>
  <text x="66" y="217" font-size="11" fill="currentColor" fill-opacity="0.85">float64 (+55 ns), 정수 틱 (0): 점선</text>
  <text x="428" y="330" font-size="11" fill="currentColor" text-anchor="end">2.34 % 느림: 틱당 4.8828 ms</text>
  <text x="528" y="400" font-size="11" fill="currentColor" text-anchor="end">1시간: 3565.42 s를 읽음, −34.58 s</text>
</svg>

위: $[2048, 4096)$ s에서 float32 값은 $2^{-12}\,\mathrm s=0.244\,\mathrm{ms}$ 간격으로 놓이므로, 정확한 합 $t+5\,\mathrm{ms}$는 간격 $20.48$개만큼 떨어진 곳에 오고 $20$개, 곧 $4.8828\,\mathrm{ms}$로 저장된다. 틱마다 $0.117\,\mathrm{ms}$를 잃는다. 아래: 참 시간 한 시간 동안 P6의 float32 누적 시계는 $34.1$분에 $2048\,\mathrm s$를 읽을 때까지 $0.098\%$ 빠르게 가서 $1.84\,\mathrm s$ 앞서고, 그 뒤 $2.34\%$ 느리게 가서 한 시간째에 $3565.42\,\mathrm s$, 곧 $34.58\,\mathrm s$ 뒤처진 값을 읽는다. float64 시계($+55\,\mathrm{ns}$)와 정수 틱 카운트(정확)는 영점 선 위에 머문다.

### 대상으로 한 번 끝까지 · Worked case

이것이 카탈로그 주기에서의 과제 대상이다. P6의 로거는 대부분의 펌웨어처럼 틱마다 `t += 0.005`로 한 시간 동안 시간을 센다. 과제는 주기를 바꾼다. $5\,\mathrm{ms}$ 판을 여기서 먼저 풀어 두면 과제는 첫 유도가 아니라 손잡이 하나를 바꾸는 일이 된다. 사실 셋은 여기서 한 줄로 풀고 §5에서 유도한다. float32 수는 유효 비트 24개를 가지므로 **binade** $[2^e,2^{e+1})$ 안의 모든 값은 **간격**(spacing) $u=2^{e-23}$의 배수다. 합은 매번 그런 배수 중 **가장 가까운 것으로 반올림**된다. 그리고 이진 분수가 아닌 $0.005$ 자체는 $0.004999999888\,\mathrm s$로 저장된다.

**1단계 — 한 시간이 끝나 갈 무렵의 한 틱.** $2048$ s와 $4096$ s 사이의 읽은 값은 모두 다음의 배수다.

$$u=2^{11-23}=2^{-12}\ \mathrm s=0.244140625\ \mathrm{ms},\qquad \frac{T}{u}=\frac{0.005}{2^{-12}}=20.48$$

그러므로 정확한 합 $t+T$는 눈금 $t+20u$에서 $0.48u$ 지나고 $t+21u$에는 $0.52u$ 못 미친 곳에 있다. 가장 가까운 쪽으로 반올림하면 $t+20u$가 남는다. 틱마다 $5\,\mathrm{ms}$ 대신 $20u=4.8828125\,\mathrm{ms}$를 더하고, 시계는 참 속도의 $20/20.48=0.9765625$로 가며 틱마다 $0.1171875\,\mathrm{ms}$, 곧 $2.34\%$를 잃는다.

**2단계 — 처음 34분.** $128$ s와 $2048$ s 사이에서 간격은 $2^{-16}$부터 $2^{-13}$ s이고, $T/u=327.68$, $163.84$, $81.92$, $40.96$은 *위로* 반올림되어 $328$, $164$, $82$, $41$이 된다. 틱마다 $41\cdot2^{-13}=5.0048828125\,\mathrm{ms}$를 더하니 $2^{-10}$, 곧 $0.098\%$ 빠르다. $128$ s 아래에서 저장되는 걸음은 $5\,\mathrm{ms}$와 $0.06\%$ 안에서 다르고, §10은 시계가 틱 $25{,}607$, 참 시간 $128.035$ s에 처음 $128$ s를 읽으며 $0.031$ s 뒤처져 있다고 출력한다. 거기서부터 틱당 $5.0048828125\,\mathrm{ms}$로 $1920$ s어치를 읽는 데는

$$\frac{1920}{0.0050048828125}\approx383{,}625\ \text{틱}=1918.13\ \mathrm s,\qquad e=-0.031+(1920-1918.13)=+1.842\ \mathrm s$$

가 걸린다. $2^{-10}$만큼 빠른 시계는 제 읽은 값을 더 짧은 참 시간에 채우기 때문이다. 그래서 틱 $25{,}607+383{,}625=409{,}232$, 참 시간 $2046.16$ s($34.1$분)에 $2048$ s를 읽고 $1.842$ s 앞서 있다.

**3단계 — 한 시간의 나머지.** 남은 $720{,}000-409{,}232=310{,}768$틱은 저마다 $T-20u=0.1171875\,\mathrm{ms}$를 잃으므로

$$e_{720\,000}=1.842-310{,}768\times0.1171875\times10^{-3}=1.842-36.418=-34.576\ \mathrm s$$

다. 읽은 값이 $4096$ s 아래에 있는 동안 저장되는 걸음은 계속 $20u$이기 때문이다. float32 시계는 참 시간 한 시간 뒤에 $3565.42$ s를 읽는다. §10의 실행은 $-34.575684$ s를 출력하고, 실행이 실제로 들어간 상태에 같은 공식을 적용하면 소수점 여섯째 자리까지 같다.

**4단계 — float64로 같은 반복.** $3600$ s에서 float64의 간격은 $2^{11-52}=4.55\times10^{-13}$ s이고 합은 매번 많아야 그 절반만큼 틀리므로, $720{,}000$틱 뒤에는

$$|e|\le720{,}000\times\tfrac12\times2^{-41}\ \mathrm s=1.64\times10^{-7}\ \mathrm s$$

이다. 어떤 반올림도 간격의 절반을 넘지 않고, 읽은 값이 간격이 두 배가 되는 $4096$ s에 닿지 않기 때문이다. 실행 결과는 $+5.54\times10^{-8}$ s다. 같은 반복이 여덟 자릿수 더 낫지만, 여전히 틱마다 자라는 수다.

**5단계 — 누적 합을 아예 쓰지 않기.** 정수 틱 카운트 $k$를 간직한다. 64비트로 $2^{63}$틱까지 정확하다. 시간은 필요할 때만 $t=k/200$으로 계산한다. 나눗셈 한 번, 반올림 한 번이라서 $k$가 얼마든 간격의 절반보다 더 틀리지 않는다. $k=720{,}000$에서는 정확히 $3600.0$이다. 이것이 [[02-foundations/lab-kernel|0.7 Lab Kernel §1]]의 시간 벡터, 곧 인덱스로 만든 $t_0+iT$이고, ROS 2도 이렇게 시간을 간직한다. 라이브러리 안에서는 64비트 정수의 나노초로, `Time` 메시지에서는 `int32` 초와 `uint32` 나노초로다(§5).

**6단계 — P6이 치르는 값.**

| 시계를 간직하는 방식 | 한 시간 뒤 읽은 값 | 오차 |
|---|---:|---:|
| float32, `t += 0.005` | $3565.424316$ s | $-34.575684$ s |
| float64, `t += 0.005` | $3600.0000000554$ s | $+5.54\times10^{-8}$ s |
| 64비트 틱 카운트, $t=k/200$ | $3600.0$ s | $0$ |

$34.58$ s는 제어 주기 $6{,}915$개이고 P6의 $70\,\mathrm{ms}$ 예산 전체의 $494$배다. §10은 float32 시계가 $81.23$ s 뒤에는 제어 주기 하나보다 더, $231.16$ s 뒤에는 — 4분도 안 되어 — 예산 전체보다 더 틀린다는 것을 찾는다. 명령에는 이 시계의 스탬프가, 목표에는 맞는 시계의 스탬프가 붙어 있다면, 명령마다 $20\,\mathrm{ms}$ 안에 목표가 있어야 한다는 [[04-robotics/ros2/debugging-data-reproducibility|25.10 디버깅, 데이터, 재현성]] 계산 절의 검사는 $108.53$ s부터 실패할 것이다. 어떤 오류도 나지 않았다.

### 1. 어느 인터프리터이고, 패키지는 어디로 가는가

*한 문장으로:* 결과는 코드와 그 코드가 import하는 모든 것의 정확한 버전에 달려 있으므로, 프로젝트마다 알려진 인터프리터로 만든 자기 환경을 두고 패키지마다 버전을 고정하며, 운영체제의 것인 Python에는 아무것도 설치하지 않는다.

같은 분석 스크립트가 노트북과 로봇 컴퓨터에서 다른 숫자를 내는 이유가 서로 다른 NumPy 버전을 import했기 때문일 수 있고, 로봇에서 실패하는 이유가 패키지가 엉뚱한 Python에 들어갔기 때문일 수 있다. 둘 다 어느 인터프리터가 돌고 그 패키지가 어디 사는가의 문제다.

**어느 Python인가.** `python3`는 셸의 검색 경로에서 가장 먼저 나오는 인터프리터이고, `sys.executable`이 그 이름을 알려 준다. 이 페이지를 확인한 Mac에서 영어 절의 두 줄은 `/opt/anaconda3/bin/python3`와 `3.12.4 /opt/anaconda3/bin/python3`를 출력했다. Anaconda의 Python이다. 로봇 컴퓨터에서도 무엇보다 먼저 같은 두 줄을 돌려라. 스크립트가 어느 인터프리터로 돌지 알려 주고, 그 답이 ROS 2에 왜 중요한지는 이 절의 마지막 문단이 다룬다.

**import는 어디서 오는가.** `import numpy`는 먼저 내장 모듈을 찾고, 그다음 `sys.path`의 디렉터리를 차례로 — 스크립트 자신의 디렉터리, `PYTHONPATH`의 디렉터리, 설치본의 `site-packages` — 뒤져 처음 찾은 것을 적재한다. 패키지를 설치한다는 것은 그 디렉터리 중 하나에 넣는다는 뜻이다. 그러므로 한 인터프리터에 설치한 패키지는 다른 인터프리터에게 보이지 않고, ROS 2 설정 파일을 source하는 것처럼 인터프리터가 시작하는 환경을 바꾸면([[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]) import가 찾는 것도 바뀐다.

**시스템 Python에는 절대 설치하지 않는다.** Linux에서 배포판과 함께 온 Python은 배포판의 것이다. Python 공식 문서는 거기에 설치하려면 root가 필요하고, pip가 그 구성 요소를 예고 없이 업그레이드하면 시스템 패키지 관리자와 시스템의 다른 부분을 방해할 수 있다고 경고한다. Ubuntu는 한 걸음 더 나아가, pip가 설치를 거부하며 환경이 *외부에서 관리된다*(externally managed)는 오류를 내고 `apt install python3-xyz`나 가상 환경을 가리킨다(그 방식이 PEP 668이다). 이를 무시하는 플래그 `--break-system-packages`는 이름이 곧 그 위험이다. apt가 설치한 패키지를 `sudo pip install`로 업그레이드하는 것이, 잘 돌던 로봇 컴퓨터가 손대지도 않은 도구를 잃는 길이다.

**가상 환경.** 해결책은 프로젝트마다 디렉터리 하나를, 이름이 정해진 인터프리터로 만드는 것이다. 영어 절의 명령들은 Mac의 작업용 프로젝트 디렉터리에서 돌았고, `command` 줄의 긴 경로는 `…`로 줄였다. 출력을 한 줄씩 읽는다. `pyvenv.cfg`는 기반 인터프리터의 디렉터리(`home = /opt/anaconda3/bin`)와 버전(`3.12.4`)을 기록한다. 환경은 그 경로의 그 인터프리터에 속하고, 문서의 규칙은 환경을 옮기거나 복사하지 말고 다시 만들라는 것이다. `sys.prefix != sys.base_prefix`는 `True`이고, 이것이 환경 안에서 돌고 있는지 확인하는 문서화된 검사다. `site-packages`에는 pip만 있어서 `pip freeze`는 아무것도 출력하지 않는다. 그리고 기반 Anaconda Python이 가진 NumPy가 보이지 않아 `import numpy`는 `ModuleNotFoundError`로 끝난다. 환경은 기본적으로 격리된다. 활성화(activate)는 편의이지 필수가 아니다. `.venv/bin/python`을 직접 부르는 것이 같은 인터프리터이고, 활성화가 하는 일은 주로 환경의 `bin`을 검색 경로 맨 앞에 두는 것이다. 활성화한 셸에서 `which python`은 `…/p6-analysis/.venv/bin/python`을, `deactivate` 뒤에는 `/opt/anaconda3/bin/python`을 출력했다.

**버전 고정.** 환경의 내용은 정확한 버전을 한 줄에 하나씩 `이름==버전`으로 적은 텍스트 파일에 산다. 여기서는 이 페이지의 실습에 필요한 한 줄, `numpy==2.0.2`다. Mac에서 실습 출력을 만든 NumPy의 버전이다. `python -m pip freeze > requirements.txt`가 설치된 집합을 이 형식으로 쓰고, `python -m pip install -r requirements.txt`가 그 집합을 새 환경에 정확히 설치한다(Python 튜토리얼 12장). 설치는 패키지를 내려받으므로 여기서 돌리지 않았고, `pip freeze`는 위에서 돌려 빈 집합을 얻었다. `requirements.txt`는 커밋하고 `.venv/`는 절대 커밋하지 않는다.

> **가상 환경의 정의.** **가상 환경**(virtual environment)은 *디렉터리*다. Python의 사본도 컨테이너도 아니고, 기반 인터프리터 하나 위에 프로젝트 하나만의 설치 패키지를 주는 디렉터리다. 정의 조건 넷. **기반 인터프리터로 만들어지고 그것을 기록한다**: `pyvenv.cfg`가 그 인터프리터의 디렉터리와 버전을 적으므로 환경은 그 Python만 돌리고, 옮기거나 복사하지 않고 다시 만든다. **자기 `site-packages`를 가진다**: 기반의 패키지는 기본적으로 들어오지 않는다. **자기 인터프리터가 거기에 설치한다**: `.venv/bin/python -m pip install`은 환경 안에만 쓰고 시스템에는 절대 쓰지 않는다. 그리고 **버릴 수 있다**: 고정된 목록에서 다시 만들고, 커밋하지 않는다.
>
> $$\text{inside an environment}\iff\texttt{sys.prefix}\neq\texttt{sys.base\_prefix},\qquad E=\big(\text{interpreter }X.Y,\ \{p_i{=}{=}v_i\}\big)$$
>
> `sys.prefix`는 돌고 있는 환경의 디렉터리, `sys.base_prefix`는 기반 인터프리터의 디렉터리이고, $p_i{=}{=}v_i$는 패키지 $p_i$를 정확히 버전 $v_i$로 고정한다. 그러므로 인터프리터 버전과 고정된 집합을 공유하는 두 기계는 같은 코드를 import한다.
>
> - **예**: Mac의 Python 3.12.4로 만든 `p6-analysis/.venv`. 검사는 `True`를 출력하고, `site-packages`에는 pip만 있으며, 고정한 `numpy==2.0.2`를 그 안에 설치하기 전까지 `import numpy`는 실패한다.
> - **비예**: 로봇 컴퓨터에서의 `sudo pip install numpy --upgrade`. 따로 된 디렉터리가 없으니 설치는 apt가 관리하고 ROS 2가 기대어 빌드된 패키지들 사이에 떨어진다. Ubuntu의 pip는 이를 거부하고, 억지로 하면 시스템 자신의 Python 도구가 위험해진다.
> - **왜 중요한가**: 결과는 코드 *그리고* 그 코드가 import한 버전의 함수다. 고정 목록에서 다시 만든 환경은 그 두 번째 인자를 싸게 고정한다. §7은 NumPy의 시드 준 난수 흐름조차 같은 NumPy 빌드에서만 보장된다는 것을 보여 준다.

**ROS 2의 경우.** ROS 2 Jazzy의 바이너리는 Ubuntu 24.04와 그 Python 3.12를 위해 빌드되고(REP 2000은 3.12.3을 적는다), ROS 2의 Python 패키지 안내서는 인터프리터가 바이너리를 빌드한 것과 일치해야 한다고 적는다. conda 같은 것을 쓰면 아마 일치하지 않을 것이라는 말도 덧붙인다. 그래서 로봇 컴퓨터에서의 순서는 이렇다. 먼저 `package.xml`의 rosdep 키([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]). 없으면 apt 패키지 `python3-<이름>`. 둘 다 제공하지 않는 것은 워크스페이스 안에 시스템 `python3`로 만든 가상 환경에 설치하되, colcon의 탐색([[04-robotics/ros2/workspaces-packages-launch|25.4 §3]])이 건너뛰도록 그 안에 빈 `COLCON_IGNORE` 파일을 두고, `/opt/ros/jazzy/setup.bash`를 source한 뒤 워크스페이스를 빌드한다. 안내서는 ROS의 릴리스 도구 Bloom으로 내보낼 패키지라면 필요한 것을 rosdep 키로 선언해야 한다고 덧붙인다. 기계 전체가 재현 가능해야 할 때의 단위는 digest로 고정한 컨테이너 이미지다([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]).

### 2. 이름, 객체, 가변성

*한 문장으로:* Python 변수는 객체에 묶인 이름이고 대입은 절대 복사하지 않으므로, 가변 객체를 제자리에서 바꾸면 그 객체에 묶인 모든 이름이 그 변화를 본다. 한 번 만들어진 기본 인자도, 얕은 복사가 공유한 중첩 딕셔너리도 마찬가지다.

로그가 바뀌면 함께 바뀌는 로그의 "백업", 그리고 모든 실행이 마지막 값을 쓴 파라미터 스윕은 둘 다 Python이 객체에 이름을 붙이는 방식에서 나온다. 모든 Python 객체는 정체(identity), 타입, 값을 가진다. 정체는 바뀌지 않고, `==`가 값을 비교하는 곳에서 `is`는 정체를 비교한다. 리스트, 딕셔너리, 집합, NumPy 배열은 **가변**(mutable)이라 값이 제자리에서 바뀔 수 있고, int, float, 문자열, 튜플은 **불변**(immutable)이다. 대입은 아무것도 복사하지 않고 이름을 객체에 묶을 뿐이다. 영어 절의 코드가 P6의 데이터 위에서 그 세 가지 결과를 보여 준다.

첫 줄 `999 True`는 순수한 별칭이다. `raw`는 백업이었던 적이 없다. 둘째 줄 `[21, 37] [21, 37] True`는 **가변 기본 인자**(mutable default argument)다. 기본값은 `def`가 실행될 때 한 번만 평가되므로, `log`를 생략한 호출은 모두 같은 리스트에 덧붙이고, 실행 B의 "새" 로그에는 이미 실행 A의 샘플이 들어 있다. `None` 관용구는 호출마다 새 리스트를 만들어 `[21] [37]`을 준다. §8의 dataclass는 그런 기본값을 아예 거부한다. 마지막 두 줄은 스윕 버그다. 기반 설정 하나의 얕은 복사로 만든 $k_p=20$, $40$, $80$의 세 설정이 모두 $k_p=80$으로 끝나고 기반 설정도 그렇다(`[80.0, 80.0, 80.0] 80.0`). 셋이 `gains` 딕셔너리 하나를 공유하기 때문이다. 깊은 복사는 세 이득을 따로 지킨다(`[20.0, 40.0, 80.0]`).

> **별칭(aliasing)의 정의.** **별칭**(aliasing)은 *이름 사이의 관계*다. 둘 이상의 이름이 한 객체에 묶여 있는 것이다. 같은 단어를 쓰는 [[02-foundations/signal-processing|6. 신호처리 §2]]의 샘플링 현상과는 다르다. 세 조건이 모이면 문제가 된다. 이름들이 **같은 객체에 묶여 있다**. 대입은 묶을 뿐 복사하지 않기 때문이다. 그 객체가 **가변**이다. 그리고 이름 중 하나를 통해 **제자리에서** 바꾼다 — `append`, `x[i] = …`, 리스트나 배열에 대한 `+=` — 그러면 다른 모든 이름이 그 변화를 본다.
>
> $$b=a\ \Rightarrow\ \texttt{id}(b)=\texttt{id}(a),\qquad \text{then after } b[i]\leftarrow x:\ \ a[i]=x$$
>
> `id`는 객체의 정체로 수명 내내 고정되고, `a`, `b`는 이름이다. 그러므로 별칭은 정체의 문제이고, `is`는 답할 수 있어도 `==`는 답할 수 없다.
>
> - **예**: `raw = readings; raw[0] = 999`는 `readings[0] == 999`를 남긴다. 그리고 `record(37)`은 실행 A와 같은 리스트 객체인 `[21, 37]`을 돌려준다. 기본 리스트가 한 번만 만들어졌기 때문이다.
> - **비예**: `x = 3.0; y = x; y += 1.0`. float는 불변이라 `+=`는 `y`를 새 객체에 묶고 `x`는 `3.0`으로 남는다. 같은 줄을 리스트나 NumPy 배열에 쓰면 공유된 그 하나의 객체가 바뀐다.
> - **왜 중요한가**: 기본 리스트를 공유하는 스윕의 두 실행, 또는 살아 있는 로그의 두 번째 이름일 뿐인 "백업"은 아무 오류 없이 틀린 숫자를 만든다.

**얕은 복사**(shallow copy) — `copy.copy(d)`, `d.copy()`, `lst[:]` — 는 항목이 원본의 바로 그 객체들인 새 바깥 컨테이너다. 한 층만 복사되고 그 아래는 모두 공유되므로, 모든 항목이 불변일 때에만 안전하다. **깊은 복사**(deep copy) `copy.deepcopy(d)`는 모든 층을 복사하므로 어떤 가변 객체도 공유되지 않는다. 위의 스윕 버그가 이것이다. `{"rate_hz": 200, "gains": {"kp": 40.0, "kd": 2.0}}`의 얕은 복사 셋에 $k_p=20$, $40$, $80$을 주면 모두 $80$을 읽고 기반도 그렇지만, 깊은 복사 셋은 $20$, $40$, $80$을 읽는다 — 그리고 스윕이 출력하는 표는 어느 쪽이든 완벽하게 정상으로 보인다. (NumPy 슬라이스 `counts[::4]`는 어느 쪽 복사도 아니고 같은 메모리의 뷰다, §3.)

배열로 넘어가기 전에 대비 하나. Python 리스트에서 `lst[:]`는 얕은 복사이고, NumPy 배열에서 같은 `arr[:]`는 뷰다. [[02-foundations/algorithms/interview-code|11.7 §3]]이 이 함정들의 인터뷰판 — 행들이 한 리스트인 격자, `is`와 `==` — 을 정리한다.

### 3. NumPy 배열: dtype, shape, stride, 뷰

*한 문장으로:* ndarray는 dtype, shape, stride를 통해 읽는 메모리 한 덩어리이므로, 슬라이스는 같은 바이트를 읽는 두 번째 방법, 곧 뷰일 수 있고, 뷰를 통해 쓰면 그것이 나온 로그가 다시 쓰인다.

로그의 슬라이스는 같은 메모리를 보는 두 번째 창일 수 있어서, 슬라이스를 제자리에서 고치는 무해해 보이는 한 줄이 원시 로그를 다시 쓴다. 언제 그런지 보려면 배열이 무엇인지부터 본다. **ndarray**는 넷을 통해 읽는 메모리 한 덩어리다. **dtype** 하나(그래서 모든 항목의 바이트 크기 `itemsize`가 같다), 길이들의 튜플인 **shape**, 축마다 한 칸 가는 데 건너뛰는 바이트 수인 **stride**, 그리고 배열이 소유하거나 다른 배열에게서 빌린 **데이터 버퍼**다. 인덱싱은 이것들 위의 산수이지 조회가 아니다. 항목 $(n_0,\dots,n_{d-1})$은 첫 항목에서 $\sum_k s_k n_k$바이트 뒤에 있고($s_k$는 축 $k$의 stride), 배열은 $\texttt{itemsize}\times\prod_k\texttt{shape}_k$바이트를 차지한다. P6의 한 시간 카운트는 `int64`, shape `(720000,)`, stride `(8,)`, $5{,}760{,}000$바이트다(`int16`이면 $1{,}440{,}000$). 목표 주기 하나를 한 행으로 `(180000, 4)`로 reshape하면 stride는 `(32, 8)`이므로, 항목 $(12{,}345,\ 3)$은 바이트 $32\cdot12{,}345+8\cdot3=395{,}064$에 있고 그것은 `counts[49383]`이다. 같은 카운트의 Python 리스트는 8바이트 포인터 $720{,}000$개가 따로 떨어진 정수 객체 — 이 Mac의 64비트 CPython에서 각 28바이트(`sys.getsizeof`) — 를 가리키므로, 샘플당 8바이트가 아니라 최대 36바이트이고, 메모리에 흩어져 있으며, 접근할 때마다 타입을 확인한다. NumPy에서 빠른 모든 것, 곧 복사 없는 슬라이싱과 벡터화 산술(§4)이 이 stride 배치에서 나오고, 뷰가 만드는 모든 조용한 버그도 그렇다.

영어 절의 코드는 한 시간을 정수만으로, $c_k=\lfloor 2048\,p(kT)\rfloor$로 만든다. 그래서 로그는 정확하고 어느 기계에서나 같다. 출력을 읽는다. NumPy 2에서 기본 정수는 모든 64비트 시스템에서 64비트라서 `counts`는 `int64`이고, 한 열 한 시간이 5.76 MB다. 카운트는 $40{,}960$을 넘지 않으니 `int32`로도 여유 있게 반으로 줄일 수 있고, `int16`이 무엇을 하는지는 §6의 이야기다. reshape와 4칸 슬라이스는 **뷰**다. 새 shape과 stride, 같은 버퍼, `base is counts`. 불리언 마스크는 **복사**다. 마지막 세 줄은 broadcasting이고, 그 규칙 — shape을 오른쪽 끝에 맞추고, 짝마다 같거나 하나가 1 — 은 [[02-foundations/algorithms/interview-code|11.7 §5]]에 있다. `frames[:, :1]`은 shape이 `(180000, 1)`이라서, 빼면 목표 주기마다 첫 카운트를 그 주기의 네 틱에서 빼고, 카트가 나가는 중인 1,000번째 주기에서 $[0, 5, 10, 15]$를 준다. shape이 `(180000,)`인 `frames[:, 0]`은 $180{,}000$을 $4$에 맞대게 되어 `ValueError`로 실패한다.

> **뷰의 정의.** **뷰**(view)는 *데이터 버퍼가 다른 배열의 것인 ndarray*다. 메타데이터는 새것, 바이트는 같은 것. 정의 조건 셋. 기반 배열의 **버퍼를 공유한다**: `v.base`가 원본이고 `np.shares_memory(v, a)`가 참이다. 그 버퍼를 **자기 오프셋과 stride로** 읽는다: 그래서 그렇게 표현할 수 있는 인덱스 패턴 — 기본 슬라이싱(`a[i:j:s]`, `a[:, 0]`)과 대부분의 reshape — 만 뷰가 될 수 있고, 불리언 인덱싱과 정수 배열 인덱싱은 늘 복사한다. 그리고 **뷰를 통해 쓰면 기반에 쓰인다**.
>
> $$v=a[i_0::s]\ \Rightarrow\ v[m]\ \text{is at byte}\ (i_0+m\,s)\,\texttt{itemsize}\ \text{of } a\text{'s buffer},\qquad \texttt{v.strides}=s\cdot\texttt{a.strides}$$
>
> $i_0$는 슬라이스의 시작, $s$는 걸음, $m$은 뷰 자신의 인덱스다. 그러므로 어떤 크기의 슬라이스도 복사 비용이 없고, 뷰는 기반 전체를 살려 둔다.
>
> - **예**: `at_goal = counts[::4]`, shape `(180000,)`, stride `(32,)`, `base is counts`. 아래에서 "레일 중앙 기준 카운트"를 뜻한 `at_goal -= 20480`은 원시 로그의 네 번째 샘플마다 10 m씩 옮긴다.
> - **비예**: `counts[counts > 0]`와 `counts[np.array([0, 4, 8])]`. 불리언 인덱싱과 정수 배열 인덱싱은 늘 복사하므로, 거기에 써도 로그는 그대로다. 그리고 Python 리스트의 `lst[:]`. NumPy 뷰와 문법이 같은 복사다.
> - **왜 중요한가**: NumPy 슬라이싱이 공짜인 이유가 뷰이고, 뷰에 대한 제자리 연산은 원시 로그가 그것을 읽는 분석 코드에게 다시 쓰이는 가장 흔한 길이다.

영어 절의 다음 코드가 그 버그와 해결을 보여 준다. 제자리 뺄셈 뒤 `counts[4]`는 $-20{,}480$인데 이웃은 $0$이고, 로그에서 가장 큰 한 틱 속도는 $2000.59\,\mathrm{m/s}$다. $0.5\,\mathrm{m/s}$로 기어가는 카트가 네 번째 틱마다 순간 이동한다. `centred = counts[::4] - 20_480`은 새 배열을 계산하고, 로그의 가장 큰 한 틱 속도는 틱당 6카운트인 $0.59\,\mathrm{m/s}$로 돌아온다. 습관 하나: 제자리 연산 — `-=`, `x[...] =`, `out=` 인자 — 앞에서는 `np.shares_memory(x, log)`를 묻고, 답이 예인데 그럴 뜻이 없었다면 `.copy()`한다.

### 4. 벡터화: 반복을 인터프리터 밖으로

*한 문장으로:* Python 반복문은 샘플마다 인터프리터의 항목당 부담을 치르고, NumPy 식 하나는 그 부담을 한 번만 치른 뒤 타입이 정해진 버퍼 위에서 컴파일된 코드로 반복하므로, P6의 한 시간 위의 같은 산수가 수십에서 수백 배 빨리 돌고 비트 하나까지 같은 숫자를 준다.

P6은 한 시간에 샘플 $720{,}000$개를 쓰고, 로그 한 시간에 몇 초가 걸리는 분석은 밀리초가 걸리는 분석보다 훨씬 드물게 다시 돌려진다. 카운트로부터 제어기의 속도 추정은 $w$틱 창에 걸친 차분, $v_k=(c_k-c_{k-w})/(N\,w\,T)$다. 반복문으로 쓰면 $719{,}999$개 샘플 하나하나가 인터프리터에게 같은 절차를 치르게 한다. 리스트에서 객체 둘을 꺼내고, 그 타입이 무엇이고 어떤 뺄셈이 맞는지 알아내고, 결과를 담을 새 정수 객체를 만들고, 나눗셈도 그렇게 하고, 결과를 덧붙인다. 같은 버퍼의 두 뷰 위의 식 하나로 쓰면 인터프리터는 그 절차를 한 번만 하고, NumPy의 컴파일된 반복이 원시 8바이트 정수와 실수 위에서 뺄셈과 나눗셈을 한다.

영어 절의 코드 출력에서 `np.array_equal`은 모든 창에서 `True`다. 두 판이 같은 값에 같은 IEEE 연산을 하므로 결과가 근사적으로가 아니라 정확히 같다. 벡터화한 코드에 요구할 검사가 바로 이것이다. 수준(levels)은 카트가 $0.5\,\mathrm{m/s}$로 나갈 때 추정이 말할 수 있는 값이다. 한 틱 창은 5나 6카운트, 곧 $0.488$이나 $0.586\,\mathrm{m/s}$를 본다. 20틱 창은 102나 103카운트를 보아 참값과 $0.005\,\mathrm{m/s}$ 안에 있지만, $50\,\mathrm{ms}$ 전의 카트를 묘사한다. 해상도와 지연 사이의 이 거래는 Python이 아니라 추정기의 것이다. 한 카운트의 속도 양자를 [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]]의 계산 절이 유도하고, 양자화를 잡음으로 다루는 것이 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §4]]다.

**일을 세기.** $w=1$에서 반복은 $719{,}999$번 돌고, 매번 리스트 조회 둘, 뺄셈 하나, 나눗셈 하나, 덧붙이기 하나 — 해석되는 연산 약 다섯, 모두 약 $360$만 번 — 를 상자에 싸인(boxed) Python 객체 위에서 한다. 식은 컴파일된 코드에서 $719{,}999$번의 기계 연산을 두 바퀴 하고 임시 배열 하나를 만든다. 이 페이지의 Mac — Apple M1이고, 한 기계의 측정이라 페이지의 검사 대상 코드에 넣지 않았다 — 에서 식은 로그 한 시간에 약 $1.2\,\mathrm{ms}$, 위의 리스트 반복(결과 배열 만들기까지 포함)은 $77\,\mathrm{ms}$, NumPy 배열을 원소 하나씩 인덱싱하는 반복은 약 $660\,\mathrm{ms}$가 걸렸다. P6의 하루 24시간이면 30밀리초 대 많게는 16초다. 바꿀 때마다 다시 돌리는 분석과, 다시 돌리기를 그만두게 되는 분석의 차이다.

> [!note]- 더 깊이 · Deeper
> 영어 절의 시간 측정 코드는 Python 3.12.4와 NumPy 2.0.2에서 판마다 다섯 번 돌린 최선을 잰다. 식의 최선은 $1.2$에서 $1.3\,\mathrm{ms}$ 사이였다.

> **벡터화 연산의 정의.** **벡터화 연산**(vectorized operation)은 *배열의 모든 항목에 연산을 적용하는, 컴파일된 코드 안의 호출 하나*다. 반복이 어디서 도는지를 바꾸는 것이지, 무엇을 계산하는지를 바꾸는 것이 아니다. 정의 조건 셋. 데이터가 **타입이 정해진 버퍼 하나**에 있어(§3) 어떤 항목도 타입 확인이 필요 없다. 항목에 대한 반복이 **컴파일된 코드에서** 항목당 기계 수준 연산 하나로 돈다. 그리고 Python은 항목이 몇 개든 **호출당 일정한 양의 일**만 한다.
>
> $$t_{\text{loop}}\approx n\,(c_{\text{py}}+c_{\text{op}}),\qquad t_{\text{vec}}\approx c_{\text{call}}+n\,c_{\text{op}},\qquad c_{\text{py}}\gg c_{\text{op}}$$
>
> $n$은 항목 수, $c_{\text{py}}$는 항목당 인터프리터의 비용(꺼내기, 타입에 따른 분기, 결과를 담을 새 객체), $c_{\text{op}}$는 산수 자체, $c_{\text{call}}$은 호출 한 번의 고정 비용이다. 그러므로 $n$이 커지면 속도 향상은 $c_{\text{py}}/c_{\text{op}}$에 다가가고, 항목 몇 개짜리 배열에서는 사라진다.
>
> - **예**: P6의 한 시간 위의 `(c[w:] - c[:-w]) / (N_PER_M * w * T_S)`. 뷰 둘, $719{,}999$개 항목에 걸친 뺄셈 하나와 나눗셈 하나이고, 반복과 비트 하나까지 같으며, M1에서 리스트 반복보다 약 60배 빠르다.
> - **비예**: 슬라이스로 쓴 누적 합 `t[1:] = t[:-1] + dt`. 오른쪽은 무엇이든 저장되기 전에 *옛* `t`로 계산되므로, 각 항목은 누적 합이 아니라 앞 항목의 옛 값 더하기 `dt`가 된다. 점화식 — 각 항목이 방금 계산된 항목을 필요로 하는 것 — 은 원소별 연산이 아니다. NumPy는 합을 `np.cumsum`으로 제공하고, 필터의 상태 같은 일반 점화식은 반복으로 남거나 컴파일된 코드로 옮긴다.
> - **왜 중요한가**: $200\,\mathrm{Hz}$에서 로그 하루는 샘플 $17{,}280{,}000$개이고, 항목당 인터프리터 비용이 분석이 밀리초에 다시 도는지 수십 초에 도는지를 정한다. 그것이 얼마나 자주 다시 돌리는지를 정한다.

### 5. 로봇 로그의 부동소수점: 간격과 누적 드리프트

*한 문장으로:* 부동소수점 수는 유효숫자 곱하기 2의 거듭제곱이라서 이웃한 값 사이의 간격이 2의 거듭제곱마다 두 배가 되고, 큰 누적 합에 작은 걸음을 더하는 시계는 틱마다 그 간격으로 반올림된다. 그래서 P6의 float32 시계는 한 시간에 $34.58$ s를 잃고 정수 틱 카운트는 아무것도 잃지 않는다.

P6의 로거는 오류 메시지 하나 없이 한 시간에 $34.58$ s를 잃는다. 이유를 보려면 float가 어떤 수를 담을 수 있는지 알아야 한다. 거의 모든 플랫폼에서 Python의 `float`는 유효 비트 53개의 IEEE 754 binary64이고, NumPy는 24개인 `float32`를 더한다. 정규화된 수는 $\pm(1.f)\cdot2^{e}$로 저장되므로 binade $[2^e,2^{e+1})$ 하나 안에서 표현 가능한 값들은 고르게 놓이고, 간격은 2의 거듭제곱마다 두 배가 된다. `np.finfo`는 형식의 분수 비트 수와 기계 엡실론 — $1$ 바로 위의 간격 — 을, `np.spacing(x)`와 Python float의 `math.ulp(x)`는 $x$에서의 간격을 준다.

영어 절 코드의 출력을 읽는다. 처음 두 줄은 아래 규칙을 $t=3600$ s에 적용한 것이다. float32에서 $2^{-12}$ s($0.000244140625$), float64에서 $2^{-41}$ s($4.547\times10^{-13}$). 셋째 줄은 $0.005$가 이진 분수가 아니라서 두 형식 모두 그 이웃을 저장한다는 것을 보여 준다(float32는 $0.00499999988824129105$). 넷째 줄 `3565.424316 3600.0000000554 3600.0`은 계산 절을 코드 세 줄로 한 것이다. `np.cumsum`은 배열 자신의 dtype으로 항목을 하나씩 차례로 더한다. 펌웨어의 `t += dt` 그대로이고, §10이 이것을 스칼라 반복과 대조한다.

> **부동소수점 간격의 정의.** 부동소수점 형식의 $x$에서의 **간격**(spacing), 곧 **ulp**(unit in the last place)는 *$x$와 그다음 표현 가능한 수 사이의 틈*이다. 그 크기에서 형식이 가진 성질이지 어떤 계산의 오차가 아니다. 정의 조건 셋. 이진 부동소수점 수는 부호, 지수, 분수 비트 $p$개를 저장하므로 **binade** $[2^e,2^{e+1})$마다 표현 가능한 수가 **고르게 놓인다**. 간격은 2의 거듭제곱마다 **두 배가 된다**. 그리고 산술 결과는 표현 가능한 수 중 **가장 가까운 것으로 반올림**되므로 많아야 간격의 절반만큼 틀린다.
>
> $$u(x)=2^{\lfloor\log_2|x|\rfloor-p},\qquad p=23\ (\texttt{float32}),\quad p=52\ (\texttt{float64}),\qquad \big|\mathrm{fl}(x)-x\big|\le\tfrac12\,u(x)$$
>
> $x$는 정규 범위의 0 아닌 유한수, $\mathrm{fl}$은 형식으로의 반올림이다. 그러므로 저장된 시간의 절대 해상도는 시간이 자랄수록 거칠어지고, 상대 해상도는 $2^{-p}$ 근처에 머문다.
>
> - **예**: $t=3600$ s에서 $u$는 float32에서 $2^{11-23}=2^{-12}$ s $=0.244$ ms, float64에서 $2^{11-52}=4.55\times10^{-13}$ s다. 24시간에서 float32의 간격은 5 ms 틱 하나보다 큰 $7.81$ ms라서, float32로 저장한 하루의 마지막 틱 스탬프 $1{,}000$개 중 서로 다른 것은 $640$개뿐이다(§10).
> - **비예**: $5\,\mathrm{ms}$ 걸음 자체. $0.005$는 float32에서 $0.004999999888$ s로 저장되고, 이 $1.1\times10^{-10}$ s의 표현 오차는 한 번 정해지는 것이며 누적 시간 근처의 간격이 아니다. 처음 몇 틱이 지나면 합이 간격의 어느 배수로 반올림되는지를 바꾸기에는 너무 작아서, 계산 절의 $34.58$ s에는 아무 몫도 없다.
> - **왜 중요한가**: 스탬프의 해상도는 0에서 얼마나 먼가가 정하므로, float32로 저장한 1970년 이후의 초는 $128$ s까지만 — float64로는 $238$ ns까지 — 구분되고, 긴 로그의 시간 열은 그것이 기록하는 주기보다 거칠어질 수 있다.

> **누적 드리프트의 정의.** **누적 드리프트**(accumulation drift)는 *덧셈마다 반올림되는 누적 합의 오차*다. 양 자체가 아니라 그 양을 계산하는 방식의 성질이다. 정의 조건 셋. 값을 인덱스로 계산하지 않고 작은 증분의 **반복 덧셈** $t\leftarrow t+T$로 쌓는다. **합이 매번 형식으로 반올림**되므로 실제로 더해지는 증분은 합이 사는 binade의 간격의 정수배다. 그리고 반올림이 **계통적**이다. binade 하나 안에서는 같은 증분이 틱마다 같은 방향으로 반올림되므로 오차가 상쇄되지 않고 쌓인다.
>
> $$\hat t_{k+1}=\mathrm{fl}\big(\hat t_k+\mathrm{fl}(T)\big),\qquad \hat t_{k+1}-\hat t_k=u\cdot\mathrm{round}\big(\mathrm{fl}(T)/u\big)\ \ \text{inside a binade of spacing } u,\qquad e_k=\hat t_k-kT$$
>
> $\hat t_k$는 $k$틱 뒤에 저장된 시계, $T$는 참 주기, $u$는 $\hat t_k$가 든 binade의 간격, $e_k$는 드리프트다. 그러므로 시계는 $u\,\mathrm{round}(T/u)/T$의 속도로 가고, 그 속도는 binade 안에서 일정하며 2의 거듭제곱에서만 바뀐다.
>
> - **예**: P6의 float32 시계. $[2048,4096)$ s에서 $u=2^{-12}$ s, $T/u=20.48$이라 틱마다 $20u=4.8828$ ms를 더한다. 시계는 $2.34\%$ 느리게 가서 한 시간을 $3565.42$ s로 끝낸다(계산 절). $T/u=0.32$가 $0$으로 반올림되는 $2^{17}=131{,}072$ s를 넘으면 영영 멈춘다.
> - **비예**: 필요할 때 $t=k/200$으로 계산하는 정수 틱 카운트 $k$. 시간마다 반올림은 한 번, $|e|\le\tfrac12u(t)$이고 그 이상은 없다. §10의 모든 시간 범위에서 정확히 $0$이다.
> - **왜 중요한가**: `t += dt`는 펌웨어 반복과 시뮬레이터에 흔한 한 줄이다. float32에서는 $231$ s 뒤에 P6의 $70\,\mathrm{ms}$ 예산 전체보다 더 틀리고, float64에서는 훨씬 낫지만 여전히 자라서 8시간 뒤 $1.37\,\mu\mathrm s$다.

**시간은 정수로 간직한다.** 두 문제의 해결은 계산 절의 5단계다. 틱이나 나노초를 64비트 정수로 세고, 표시나 공식을 위해 가장자리에서 한 번만 초로 바꾼다. ROS 2가 정확히 이렇게 한다. 라이브러리는 나노초를 64비트 정수로 세고, `Time` 메시지는 `int32` 초와 `uint32` 나노초를 나른다. 오늘의 스탬프를 float64 초로 바꾸면 $2^{-22}\,\mathrm s=238\,\mathrm{ns}$까지 구분되어 P6의 5 ms 틱에는 충분하고, float32로 바꾸면 $128$ s까지만 구분된다. 산수가 끝날 때까지 정수로 둔다.

> [!note]- 더 깊이 · Deeper
> ROS 2의 C 유틸리티 라이브러리 `rcutils`에서 한 시점은 Unix epoch 이후 나노초의 64비트 정수다. `rclpy`의 `Time`은 전체 나노초를 Python 정수로 들고 $2^{63}$ 이상을 거부한다. 그리고 `builtin_interfaces/Time` 메시지의 두 필드는 `int32 sec`와 `uint32 nanosec`다.

**실수를 비교하기.** 계산된 실수에는 정확한 같음이 잘못된 검사다. 시계가 $55$ ns만 틀려도 `clock64 == 3600.0`은 `False`다. `math.isclose(a, b)`는 다음을 검사한다.

$$|a-b|\le\max\big(r\cdot\max(|a|,|b|),\ \varepsilon_{\text{abs}}\big),\qquad r=10^{-9},\ \ \varepsilon_{\text{abs}}=0\ \text{by default}$$

상대 허용 오차가 비교하는 수와 함께 커지기 때문이고, 그래서 `math.isclose(clock64, 3600.0)`은 `True`다. 0과 비교하면 상대 항이 사라진다. 오차가 아무리 작아도 `math.isclose(5.5e-8, 0.0)`은 `False`이므로, 0과의 비교에는 그 양의 단위로 된 `abs_tol`이 따로 필요하다. "1마이크로초 안"이면 `abs_tol=1e-6`이다. NumPy의 `np.isclose(a, b)`는 다른 규칙, 기본값 $\text{atol}=10^{-8}$, $\text{rtol}=10^{-5}$의 $|a-b|\le\text{atol}+\text{rtol}\cdot|b|$다. 두 인자에 대해 대칭이 아니고, 기본 `atol`은 1보다 훨씬 작은 양에는 너무 느슨하다. 같은 간격 산수를 시계가 아니라 16비트 학습 형식에 적용한 것이 [[03-deep-learning/foundations/training-at-scale|1.3 대규모 학습 §4]]다.

### 6. 감기는 정수

*한 문장으로:* NumPy 정수와 하드웨어 카운터는 비트 수가 고정되어 조용히 한 바퀴 돌아 감기므로, P6의 16비트 카운트 레지스터는 $+16$ m에서 $-16$ m로 뛰고, 그것을 바르게 읽는 유일한 방법은 그 자신의 폭으로 차분한 뒤 넓은 폭으로 누적하는 것이다.

모터 드라이브의 16비트 카운터는 바르게 읽지 않으면 카트가 한 틱에 32 m를 뛴 것처럼 보이게 한다. Python 자신의 `int`는 필요한 만큼 자라서 넘치지 않는다. NumPy의 정수 타입은 모터 드라이브의 레지스터나 마이크로컨트롤러의 타이머처럼 폭이 고정되어 있고, 그 산술은 조용히 감긴다. 페이지의 왕복 위에서 드라이브의 16비트 레지스터는 카운트를 $2^{16}$으로 나눈 나머지로 든다.

> **고정 폭 정수의 정의.** **고정 폭 정수**(fixed-width integer)는 *정확히 $n$비트인 정수 타입*이다. NumPy의 모든 정수 dtype과 모든 하드웨어 카운터가 그렇고, Python의 `int`는 그렇지 않다. 정의 조건 셋. **$2^n$개 값의 범위**를 가진다. 부호 있는 2의 보수는 $[-2^{n-1},\,2^{n-1}-1]$, 부호 없는 것은 $[0,\,2^n-1]$이다. 산술이 **$2^n$을 법으로** 이루어지므로 한쪽 끝을 넘은 결과는 반대쪽 끝에서 다시 나타난다. 그리고 NumPy 배열 산술에서 그 감김은 **조용하다**. 오류도 경고도 없다.
>
> $$\mathrm{wrap}_n(x)=\big((x+2^{n-1})\bmod 2^n\big)-2^{n-1},\qquad \mathrm{wrap}_n\big(\mathrm{wrap}_n(a)-\mathrm{wrap}_n(b)\big)=a-b\ \ \text{whenever}\ |a-b|<2^{n-1}$$
>
> $x$, $a$, $b$는 참 정수값, $n$은 폭이다. 그러므로 좁은 카운터도 범위의 절반보다 가까운 두 읽기 사이의 *차이*는 정확히 주고, 그것이 감김을 되돌리는 방법이다.
>
> - **예**: $n=16$인 드라이브의 레지스터. $2048$ counts/m에서 $\pm16$ m를 든다. 왕복이 $16.0$ m를 지날 때 읽기는 $32{,}762$에서 $-32{,}768$로 뛰고, 레일 끝 $20$ m에서는 $-24{,}576$을 읽는다. `int16` 읽기의 `np.diff`는 참 걸음 5와 6카운트를 주고, 먼저 `int64`로 넓히면 $6{,}399.4\,\mathrm{m/s}$의 스파이크가 나온다.
> - **비예**: Python의 `2**100`, 또는 $2048$ counts/m에서 약 $4.5\times10^{15}$ m의 이동을 담을 수 있는 로그의 `int64` 카운트. P6이 하는 어떤 일도 어느 한계 근처에 가지 않는다.
> - **왜 중요한가**: 임베디드 하드웨어의 카운터와 타임스탬프는 흔히 좁고, 좁은 카운터는 모두 감긴다. 카운터 자신의 폭으로 차분하는 코드는 영원히 맞고, 먼저 넓히는 코드는 첫 감김까지만 맞는다.

영어 절 코드의 둘째 줄을 정의에 대어 읽는다. 감김을 가로질러 넓힌 읽기는 $65{,}530$카운트 — 참 $+6$에서 $2^{16}$을 뺀 것 — 만큼 다르고, 16비트 차분은 다시 감겨 $6$이 된다. 그러면 `np.cumsum`이 16비트 걸음을 플랫폼의 64비트 정수로 누적한다. NumPy가 더 좁은 정수 입력에 기본으로 쓰는 타입이다. 그래서 `unwrapped`는 카운트 $720{,}000$개를 모두 정확히 재현한다. 다음 두 줄은 NumPy 2의 승격 규칙이다. `int16` 배열과 결합한 Python 정수는 값이 무엇이든 배열의 타입을 따르므로 $32{,}767$에 `+ 1`은 조용히 감긴다. 그러나 바뀔 타입에 맞지 않는 Python 정수는 오류다. `np.array([40_960], dtype=np.int16)`이 `OverflowError`를 낸다.

마지막 줄은 P6 규모에서 다른 좁은 카운터 셋의 값을 매긴다. 32비트 마이크로초 타이머는 $2^{32}\,\mu\mathrm s=71.58$분마다 감긴다. 두 시간짜리 로그 안이다. $200\,\mathrm{Hz}$의 부호 있는 32비트 틱 카운터는 $124.3$일 간다. 그리고 1970년 이후 초를 세는 부호 있는 32비트 수 — ROS 2 `Time` 메시지의 `sec` 필드의 타입 — 는 2038년 1월 19일 03:14:07 UTC에 가장 큰 값에 이른다. 타이머의 감김도 레지스터와 같은 규칙으로 되돌린다. 두 읽기를 타이머 자신의 부호 없는 폭으로 빼면, 참 간격이 타이머의 주기보다 짧은 한 차이가 맞다.

### 7. 다시 재생할 수 있는 무작위성

*한 문장으로:* 의사 난수 생성기는 시드, 그것에 한 호출, NumPy 빌드가 정하는 결정론적 수열이므로, 재생 가능한 잡음에는 다른 줄이 흔들 수 있는 전역 시드가 아니라 그것으로 뽑는 코드가 소유한 생성기 객체와, 버전을 고정한 NumPy가 필요하다.

동료가 그림 그리는 줄 하나를 더하자 다른 답을 내는 시드 준 시뮬레이션은 재현 가능하지 않다. 원인은 시드가 사는 자리다. 난수는 시뮬레이션한 센서 잡음, 섞은 시행 순서, 데이터 분할, 초기 가중치로 로봇 학습 코드에 들어온다. NumPy의 의사 난수 생성기는 시드로부터 재현되는 결정론적 수열이다. 권장 생성자 `np.random.default_rng(seed)`는 PCG64 비트 생성기 위의 `Generator`를 돌려준다. 예전 함수 `np.random.seed`, `np.random.random` 등은 프로세스 전체가 공유하는 전역 `RandomState` 하나의 별칭이고, 옛 코드를 위해 남아 있다.

영어 절 코드의 출력 `True`, `False`, `True`를 읽는다. 출력은 난수 자체를 찍지 않고 비교만 찍는데, 이유는 §1이 이미 말했다. NumPy는 같은 빌드에서만 같은 흐름을 약속하고, 버그를 고치거나 개선하려고 버전 사이에 `Generator` 메서드의 흐름을 바꿀 수 있다. 가운데 줄이 전역 시드에 반대하는 논거다. 스크립트 맨 위의 `np.random.seed(0)`은 다른 무엇도 그 흐름에서 뽑지 않는 동안에만 흐름을 고정한다. 다른 곳의 호출 하나 — 점을 흩뜨리는 그림 도우미, 섞는 라이브러리 — 가 뒤의 모든 뽑기를 옮기고, 스크립트 자신의 줄은 하나도 바뀌지 않았는데 "시드를 준" 잡음이 바뀐다. Python의 `random` 모듈은 따로 숨은 생성기를 가지며, `np.random.seed`는 그것을 건드리지 않는다.

> **시드를 준 생성기의 정의.** **시드를 준 생성기**(seeded generator)는 *출력 전체가 시드와 그것에 한 호출로 정해지는 의사 난수 생성기 객체*다. 무작위가 아니라 결정론적이고, 바로 그것이 요점이다. 정의 조건 셋. **시드로 만들어진다**: `np.random.default_rng(seed)`가 PCG64 위의 `Generator`를 만든다. **소유되고 명시적으로 전달된다**: 전역 상태로 공유되지 않고, 그것으로 뽑는 함수나 시행에 건네진다. 그리고 **환경이 고정된다**: NumPy는 같은 비트 생성기, 같은 시드, 같은 인자의 같은 호출 순서에 대해서만, 같은 빌드, 같은 환경, 같은 기계에서 같은 흐름을 보장한다.
>
> $$x_{1:m}=G\big(\text{seed},\ (c_1,\dots,c_r),\ \text{NumPy build}\big)$$
>
> $x_{1:m}$은 뽑은 수, $G$는 생성기의 결정론적 사상, $c_1,\dots,c_r$은 그것에 차례로 한 호출이다. 그러므로 호출 순서를 바꾸는 것 — 다른 곳의 새 뽑기 — 이나 빌드를 바꾸는 것 — 고정하지 않은 업그레이드 — 은 수를 바꾼다.
>
> - **예**: `default_rng(2048)` 생성기 둘은 같은 수를 뽑는다. `default_rng(2026).spawn(3)`은 시행 셋에 독립인 자식 흐름을 주고, 2026에서 다시 spawn하면 셋 모두 재현된다. 그래서 시행 2의 P6 엔코더 잡음은 시행 1이 무엇을 뽑았든 같다.
> - **비예**: `np.random.seed(0)` 뒤의 예전 방식 뽑기. 프로세스 어디서든 `np.random.random()` 하나가 더 불리면 흐름이 밀리고, 위의 비교는 `False`를 찍는다.
> - **왜 중요한가**: 잡음, 섞기, 분할에 달린 결과는 생성기가 그것을 쓰는 코드의 것일 때만 재생된다. 재생하는 것과 그것이 얼마나 흔들리는지 아는 것은 다르다. 결과를 seed 하나가 아니라 여럿으로 보고하는 이유가 [[02-foundations/ml-practice|9. ML 실무 §4]]이고, [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성 §7]]은 코드 커밋과 환경과 함께 seed를 실행이 기록해야 할 것에 넣는다.

### 8. 구조: 함수, 스크립트 진입점, 고정된 설정, 로그 파일

*한 문장으로:* 다시 돌릴 연구 스크립트는 작은 함수들의 모듈, 파일을 실행할 때만 도는 진입점, 결과마다 로그 파일에 함께 적히는 고정된 설정 객체, 그리고 함수마다 무엇을 받는지 적어 두는 타입 힌트로 이루어진다.

몇 달씩 다시 돌리는 스크립트는 테스트가 import할 수 있어야 하고, 결과마다 곁에 설정을 기록해야 하며, 실행 도중에 그 설정을 바꿀 수 없어야 한다. 습관 넷이 그것을 해 준다.

**함수와 진입점 하나.** 일을 하나씩 맡는 함수 — 읽기, 변환, 추정, 보고 — 로 나누고, 아무 일도 하지 않고 import할 수 있는 모듈에 둔다. Python은 파일이 실행되는 프로그램일 때 모듈의 `__name__`을 `"__main__"`으로, import될 때는 모듈 자신의 이름으로 둔다. 그래서 `if __name__ == "__main__":` 관용구가 둘을 가른다. 그 블록은 셸에서는 돌고, 함수를 import하는 테스트나 노트북에서는 돌지 않는다. 문서의 조언은 그 블록을 짧게 두고 일은 `main()` 함수에 넣으라는 것이다.

**고정된 dataclass로서의 설정.** `@dataclass`는 타입 주석이 붙은 필드로부터 `__init__`, `__repr__`, `__eq__`를 만든다. `frozen=True`는 필드에 대입하면 `FrozenInstanceError`를 내게 하므로, 실행이 제 설정을 몰래 바꿀 수 없다. `dataclasses.replace`는 스윕의 변형을 옛 객체의 필드 값으로 매번 새 객체로 만든다. 여기처럼 필드가 수와 문자열이면 변형들은 나중의 어떤 줄이 바꿀 수 있는 것을 하나도 공유하지 않으므로, §2의 얕은 복사 버그가 설계에서 빠진다(딕셔너리나 리스트를 담은 필드라면 값이 복사되지 않고 그대로 넘어가므로 여전히 공유된다). 그리고 Python 3.11부터 리스트처럼 해시할 수 없는 기본값을 가진 필드는 클래스를 정의할 때 거부되므로, `record()`의 버그를 돌기 전에 잡는다. 영어 절 코드의 출력이 그것을 보여 준다. 스윕은 `[60, 3600, 28800, 86400]`이고 기반은 `3600`으로 그대로이며, 대입은 `FrozenInstanceError`, 리스트 기본값은 `ValueError`로 끝난다.

마지막 줄 `3600.0 3600.0035`는 **타입 힌트**의 이야기다. `k: int`는 읽는 사람, 편집기, 타입 검사기에게 인자를 문서화하지만 인터프리터는 주석을 강제하지 않으므로, 실수 틱 카운트가 그대로 통과해 불평 없이 $3600.0035$ s를 돌려준다. 힌트는 문서화하고, assertion은 검사한다(§9). 실행을 재구성할 수 있으려면 설정이 무엇을 기록해야 하는지 — 보정, 이득, 단위, 좌표계, 펌웨어, 소프트웨어 커밋 — 는 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §8]]이다.

**파일로 로그 남기기.** `print`는 닫힐 터미널로 가고, 로그 파일은 결과와 함께 남는다. `logging.basicConfig(filename=…, level=…, format=…)`는 루트 로거에 파일 핸들러를 붙이고, 모듈마다 `logging.getLogger(__name__)`로 제 로거를 얻는다. 함정 하나. `basicConfig`는 루트 로거에 이미 핸들러가 있으면 `force=True`(Python 3.8 이후)가 아닌 한 아무것도 하지 않는다. 그래서 노트북에서, 또는 어떤 라이브러리가 먼저 로깅을 설정한 뒤에, 파일 이름을 바꾸고 다시 돌려도 조용히 옛 파일에 계속 쓴다. 영어 절 코드의 출력에서 두 번째 `basicConfig`가 무시되어 `run2.log`는 없고(`False`) 두 메시지가 모두 `run1.log`에 있으며, `force=True` 뒤에야 `run2.log`에 쓰인다.

**하나의 스크립트로 모으기.** 영어 절은 이 조각들을 §1의 작업용 프로젝트에 있는 파일 `p6_drift.py`로 모은다. 고정된 설정, 타입 힌트가 붙은 작은 함수 둘, 모듈 수준 로거, 옵션 둘을 읽어 결과보다 먼저 설정을 로그에 쓰는 `main()`, 그리고 진입점 가드다. 첫 줄은 이 위키의 페이지 검사기에게 이것이 셀이 아니라 셸에서 돌릴 파일임을 알리는 주석이다. Mac에서 셸로 두 번 돌리고 한 번 import했다. 실행은 `float32 clock after 3600 s: error -34.5757 s`와 `float64 clock after 60 s: error +1.22427e-11 s`를 찍었고, 로그 파일의 네 줄은 결과마다 그것을 만든 설정 아래에 시각과 함께 놓였다. 로거 이름이 `__name__` 규칙을 보여 준다. 파일이 프로그램으로 돌 때는 `__main__`, import될 때는 `p6_drift`다. 그리고 import는 `main()`을 돌리지 않고 드리프트 $-34.57568359375$ s를 계산했으므로 로그는 여전히 네 줄이다(`wc -l`).

### 9. 결과 점검: assertion, 회귀 테스트, pytest

*한 문장으로:* 함수 경계의 검사는 shape, 타입, 단위, 범위에 대한 가정이 깨지는 순간 실행을 멈추고, 회귀 테스트는 페이지가 유도한 결과를 고정해서, 그것을 옮기는 나중의 변경이 표를 조용히 바꾸지 않고 요란하게 실패하게 한다.

길이가 틀린 배열이나 조용히 바뀐 상수는 정상으로 보이는 표를 만든다. 검사는 그런 실수를, 그것이 일어나는 순간 요란한 실패로 바꾼다.

**경계에서는 검사, 안에서는 assertion.** 수치 함수가 말없이 가정하는 것 — shape, dtype, 범위, 단위 — 을 데이터가 들어오는 곳에서 검사해, 틀린 입력이 틀린 답이 아니라 즉시 실패가 되게 한다. [[02-foundations/algorithms/interview-code|11.7 §5]]가 그 경험칙과 이유를 준다. `python -O`는 assertion을 없애므로, 파일과 호출자로부터 오는 입력은 명시적인 `raise`로 검증하고, `assert`는 자기 코드가 계산한 것을 지킨다. 단위는 이름 — `t_s`, `p_m`, `counts` — 과 docstring에 산다. 영어 절 코드에서 목표 주기의 뷰는 샘플이 사분의 일이라, 검사가 틀린 길이의 배열이 속도 추정으로 흘러가게 두지 않고 `ValueError: expected int64 (720000,), got int64 (180000,)` 한 줄로 문제를 이름 짓는다. 그 뒤의 `assert`는 코드가 스스로 만든 배열의 불변식 — P6의 왕복은 틱당 6카운트보다 더 움직이지 않는다 — 을 적고, 그것이 성립하는 동안은 조용하다.

**회귀 테스트**(regression test)는 유도하고 확인한 결과를 고정해서, 코드 변경이 그것을 몰래 옮기지 못하게 한다. 규칙은 부등식 하나다.

$$\text{pass}\iff\big|\,y'-y^\star\big|\le\varepsilon$$

$y^\star$는 고정된 값, $y'$은 지금 코드가 계산한 값, $\varepsilon$은 일부러 고른 허용 오차다. 알맞은 $\varepsilon$은 정당하게 바뀔 수 있는 것에 달려 있기 때문이다. $y^\star=-34.57568359375$ s는 저마다 올바르게 반올림되는 float32 덧셈의 고정된 순서에서 나오므로 어느 IEEE 기계든 그것을 재현하고, $\varepsilon=10^{-9}$ s는 정직하다. 덧셈 순서가 바뀔 수 있는 결과 — `np.sum`의 쌍별 합, 다중 스레드 선형대수, GPU 축약 — 에는 그 변화 크기의 $\varepsilon$이 필요하고, 그것을 적어 두어야 한다. 정수 카운트는 $\varepsilon=0$이다. 같은 생각을 실행 전체에 적용한 것을 25.10은 고정된 실행(pinned run)이라 부른다([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]).

**pytest, 한 문단으로.** pytest는 `test_*.py`나 `*_test.py`라는 이름의 파일을 모아, 그 안에서 이름이 `test`로 시작하는 함수를 모두 돌리고, 실패한 평범한 `assert`를 그 하위 식의 값과 함께 보고한다. `pytest.approx(expected, rel=…, abs=…)`는 실수를 비교하고 — 기본으로 상대 $10^{-6}$ 또는 절대 $10^{-12}$ 중 하나를 만족하면 같다 — `with pytest.raises(Error):`는 예외가 난다는 것을 단언한다. 영어 절의 `test_p6_drift.py`에는 테스트 넷이 있다. float32 드리프트의 고정값, float64 드리프트가 $10^{-6}$ s보다 작다는 것, 정수 틱이 정확하다는 것, 설정이 고정되어 있다는 것이다. Mac에서 그 Anaconda Python에 이미 있던 pytest 7.4.4로 `python3 -m pytest -q`를 돌리니 `4 passed`였다(걸린 시간은 그 기계의 것). 점 하나가 통과한 테스트 하나다. 첫 테스트는 모듈을 import하는데, 그래서 §8의 진입점 가드가 중요하다. 가드가 없으면 테스트를 모으는 것만으로 스크립트가 돈다. ROS 2 패키지 안에서는 같은 테스트가 `colcon test` 아래에서 돌고, 그것을 어디에 두고 결과를 어떻게 읽는지는 [[04-robotics/ros2/debugging-data-reproducibility|25.10 §10]]이 보여 준다.

### 10. 실습: 시계 셋, 뷰, 벡터화한 속도, 16비트 레지스터

§3–§6의 주장 하나하나가 다시 돌릴 수 있는 숫자다. 고정된 대상 위의 여섯 부분이다. 영어 절의 코드가 그것이고, NumPy만 쓰며 결정론적이라 출력이 어느 기계에서나 같다. 1부는 계산 절의 세 시계를 1분, 1시간, 8시간, 24시간까지 돌린다. 2부는 float32 열을 설명한다. `np.cumsum`을 하나씩 더하는 스칼라 반복과 대조하고, $128$ s부터 $2^{18}$ s까지 binade마다 float32가 저장하는 걸음을 찍고, 계산 절의 끝값을 그 공식으로 다시 유도하고, 오차가 $5$, $20$, $70$ ms를 넘는 때와 시계가 멈추는 때를 찾는다. 3부는 틱 스탬프를 누적하지 않고 float32로 저장한다. 4부는 P6의 목표 주기 샘플을 고르는 다섯 방법 위에서 제자리 뺄셈을 한다. 5부는 §4의 벡터화한 속도를 세 창에서 반복과 대조하고, 6부는 §6의 16비트 레지스터다. 블록은 필요한 것을 다시 정의하므로 혼자서도 돈다.

**세 시계**, 1부:

| 시간 범위 | 틱 | float32 시계 (s) | float32 오차 (s) | float64 오차 (s) | 정수 틱 오차 (s) |
|---|---:|---:|---:|---:|---:|
| 1분 | 12,000 | 60.003613 | +0.003613 | +1.22e-11 | 0.0 |
| 1시간 | 720,000 | 3,565.424316 | -34.575684 | +5.54e-08 | 0.0 |
| 8시간 | 5,760,000 | 30,532.958984 | +1,732.958984 | +1.37e-06 | 0.0 |
| 24시간 | 17,280,000 | 87,019.945312 | +619.945312 | +4.45e-06 | 0.0 |

**이유**, 2부 — 먼저 스칼라 반복이 1시간에서 cumsum과 같다(`True`), 그리고 binade마다 float32가 저장하는 걸음:

| 시계가 읽은 값 (s) | 간격 u (s) | 5 ms / u | 저장되는 걸음 (ms) | 시계 속도 |
|---|---:|---:|---:|---:|
| 128–256 | $2^{-16}$ | 327.68 | 5.0048828125 | 1.0009766 |
| 256–512 | $2^{-15}$ | 163.84 | 5.0048828125 | 1.0009766 |
| 512–1,024 | $2^{-14}$ | 81.92 | 5.0048828125 | 1.0009766 |
| 1,024–2,048 | $2^{-13}$ | 40.96 | 5.0048828125 | 1.0009766 |
| 2,048–4,096 | $2^{-12}$ | 20.48 | 4.8828125 | 0.9765625 |
| 4,096–8,192 | $2^{-11}$ | 10.24 | 4.8828125 | 0.9765625 |
| 8,192–16,384 | $2^{-10}$ | 5.12 | 4.8828125 | 0.9765625 |
| 16,384–32,768 | $2^{-9}$ | 2.56 | 5.859375 | 1.1718750 |
| 32,768–65,536 | $2^{-8}$ | 1.28 | 3.90625 | 0.7812500 |
| 65,536–131,072 | $2^{-7}$ | 0.64 | 7.8125 | 1.5625000 |
| 131,072–262,144 | $2^{-6}$ | 0.32 | 0.0 | 0.0000000 |

2부의 나머지 출력: 시계는 틱 $25{,}607$(참 $128.035$ s, $-0.0307$ s)에 처음 $128$ s를, 틱 $102{,}332$(참 $511.660$ s, $+0.3439$ s)에 $512$ s를, 틱 $409{,}232$(참 $2046.160$ s, $+1.8424$ s)에 $2048$ s를 읽는다. 마지막 $1{,}000$틱의 걸음은 $4.8828125$ ms이고, 계산 절의 공식은 $-34.575684$ s를 주어 실행의 $-34.575684$ s와 같다. 오차는 틱 $16{,}246$($81.23$ s)에 처음 $5$ ms를, 틱 $21{,}707$($108.53$ s)에 $20$ ms를, 틱 $46{,}233$($231.16$ s)에 $70$ ms를 넘는다. 24시간 뒤 걸음은 $7.8125$ ms이고, $5{,}638{,}663$틱을 더 가서(참 $31.83$시간) $2^{17}$ s에 닿으며, 거기서는 $t$ + 5 ms == $t$가 `True`다.

**float32로 저장한 스탬프**, 3부:

| 스탬프 | float32 간격 | float64 간격 | 마지막 1,000틱 중 서로 다른 float32 스탬프 |
|---|---:|---:|---:|
| 1분 | $2^{-18}$ s = 3.81 µs | $2^{-47}$ s = 7.11 fs | 1,000 |
| 1시간 | $2^{-12}$ s = 244 µs | $2^{-41}$ s = 455 fs | 1,000 |
| 8시간 | $2^{-9}$ s = 1.95 ms | $2^{-38}$ s = 3.64 ps | 1,000 |
| 24시간 | $2^{-7}$ s = 7.81 ms | $2^{-36}$ s = 14.6 ps | 640 |
| Unix 시간, 2026-09-23 | $2^{7}$ s = 128 s | $2^{-22}$ s = 238 ns | 1 |

**뷰와 복사**, 4부 — 행마다 한 시간 카운트의 새 사본 `c`에서 시작해, 목표 주기 샘플을 한 방법으로 고르고, 제자리에서 $20{,}480$을 뺀 뒤, 카트가 카운트 $10{,}240$에서 나가는 중인 틱 4,000을 읽는다:

| 식 | 종류 | 메모리 공유 | x -= 20480 뒤의 counts[4000] |
|---|---|---|---:|
| `c[::4]` | 뷰 | True | -10,240 |
| `c.reshape(-1, 4)[:, 0]` | 뷰 | True | -10,240 |
| `c[c > 0]` | 복사 | False | 10,240 |
| `c[np.arange(0, c.size, 4)]` | 복사 | False | 10,240 |
| `c[::4].copy()` | 복사 | False | 10,240 |

**벡터화한 속도**, 5부:

| 창 w (틱) | 반복과 같은가 | 나가는 동안의 값 (m/s) | 해상도 (m/s) | 지연 (ms) |
|---:|---|---|---:|---:|
| 1 | True | 0.48828, 0.58594 | 0.09766 | 2.5 |
| 4 | True | 0.48828, 0.51270 | 0.02441 | 10.0 |
| 20 | True | 0.49805, 0.50293 | 0.00488 | 50.0 |

**16비트 레지스터**, 6부: 레지스터는 틱 $8{,}400$에서 감긴다. 카운트 $32{,}768$, 곧 $16.0000$ m를 $-32{,}768$로 읽는다. 넓힌 뒤 차분한 최대 속도는 $6{,}399.4$ m/s, 16비트 차분의 최대는 $0.5859$ m/s이고, 다시 만든 `int64`는 카운트와 같다(`True`).

**표 읽기.** 강의가 예측했고 숫자가 이제 보여 주는 것 여섯.

- **float32 시계는 오래 맞지 않고, 한 방향으로 틀리지도 않는다.** 네 시간 범위에서의 오차 — $+3.6$ ms, $-34.58$ s, $+1{,}733$ s, $+620$ s — 는 읽은 값이 어느 binade에 있는지가 정하고, 2부의 속도 열이 설명의 전부다. $2048$ s까지 $1.0009766$, $16{,}384$ s까지 $0.9765625$, 그다음 $1.171875$, $0.78125$, $1.5625$, 그리고 틱 하나가 더는 읽은 값을 바꾸지 못하는 $2^{17}$ s부터 $0$. 실제로 들어간 상태에 계산 절의 공식을 돌리면 한 시간의 $-34.575684$ s가 찍힌 모든 자리까지 나온다.
- **float64는 미룰 뿐이다.** 여덟에서 아홉 자릿수 작지만, float64 누적 오차는 여전히 자라 8시간에 $1.37\,\mu\mathrm s$, 24시간에 $4.45\,\mu\mathrm s$다. 정수 틱 카운트는 쓰일 때까지 반올림되지 않으므로 모든 범위에서 정확하다.
- **저장만으로도 스탬프가 깨진다.** 누적 없이도 float32의 간격은 8시간과 24시간 사이에서 $5$ ms 틱을 넘는다. 하루의 마지막 $1{,}000$틱 중 $640$개만 서로 다른 스탬프를 지키니, 나머지 $360$개에서 $\Delta p/\Delta t$는 0으로 나눈다. float32로 저장한 1970년 이후의 초는 5초어치 틱을 스탬프 하나에 올린다.
- **기본 슬라이싱은 통과해 쓰고, 고급 인덱싱은 그렇지 않다.** 두 뷰는 틱 4,000을 $10{,}240$에서 $-10{,}240$으로 옮기고, 마스크, 정수 인덱스, `.copy()`는 그대로 둔다. 종류 열은 `.base`와 `np.shares_memory`로 계산하고, 마지막 열은 로그 자체로 그것을 증명한다.
- **벡터화한 추정은 정확히 반복 그대로다.** 세 창 모두 `True`이고, 수준은 $1/(N\,w\,T)$ 간격이다. 지연 $w\,T/2$로 산 해상도다.
- **레지스터의 폭으로 차분하고, 넓게 누적한다.** 레지스터는 한 시간의 $42$ s째인 틱 $8{,}400$에서 카트가 $16.0$ m를 지날 때 감긴다. 넓힌 차분은 $6{,}399.4\,\mathrm{m/s}$를 지어내고, 16비트 차분은 참 $0.5859\,\mathrm{m/s}$를 넘지 않으며, 다시 만든 카운트는 $720{,}000$개 모두와 맞는다.

### 11. 이 페이지가 다루지 않는 것

Python 문법을 처음부터 가르치는 것은 공식 튜토리얼의 일이고, 인터뷰 수준의 함정 목록 — 정렬, 정수 나눗셈, 재귀 한도 — 은 [[02-foundations/algorithms/interview-code|11.7 Python·C++ 인터뷰용 코드]]다. 자기 프로젝트를 남에게 내보내는 패키징(`pyproject.toml`, wheel, 배포), 노트북, 디버거, §4의 시간 측정 하나를 넘는 프로파일링, 스레드와 `asyncio`([[02-foundations/tools/concurrency|12.8 동시성 §8–§9]]), NumPy 너머의 수치 라이브러리는 여기서 가르치지 않는다. 텐서, 자동 미분, 학습은 [[03-deep-learning/foundations/index|1. 학습 시스템]]에서 시작하고, GPU 위의 코드 시간 재기는 [[03-deep-learning/foundations/gpu-computing|1.4 GPU 계산]]이다. ROS 2 노드 쓰기는 [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]], 빌드하기는 [[04-robotics/ros2/workspaces-packages-launch|25.4 워크스페이스, 패키지, 빌드, 런치]]이고, C++은 [[04-robotics/ros2/cpp-for-robot-code|25.0 로봇 코드를 위한 C++]]이다. 신호처리로서의 샘플링, 양자화, 필터링은 [[02-foundations/signal-processing|6. 신호처리]]다. 셸, Git, 로그를 저장하는 형식은 이 트랙의 [[02-foundations/tools/linux-shell|12.1]], [[02-foundations/tools/git-research-code|12.2]], [[02-foundations/tools/config-data-formats|12.4]]다.

### 읽고 나면

- [ ] 셸이 어느 인터프리터를 돌리는지, `import`가 패키지를 어디서 찾는지 말한다. 가상 환경을 만들고 그 안에 있는지 검사하며, 시스템 Python에 왜 아무것도 설치하지 않는지와 ROS 2 안내서가 인터프리터에 무엇을 요구하는지 말한다.
- [ ] 어떤 대입, 기본 인자, 복사에 대해서든 두 이름이 한 객체를 공유하는지 예측하고 `is`로 보인다.
- [ ] 배열의 dtype, shape, stride, 바이트를 대고, 어떤 인덱싱이 뷰이고 어떤 것이 복사인지 말하며, `.base`와 `np.shares_memory`로 확인한다.
- [ ] 샘플에 대한 반복을 뷰 위의 식 하나로 다시 쓰고, 반복과 같음을 증명하고, 둘이 하는 일을 센다.
- [ ] 어떤 값에서든 float32와 float64의 간격을, 어떤 binade에서든 누적 float 시계가 실제로 더하는 걸음을 계산한다.
- [ ] float32 누적 시계의 한 시간 드리프트를 손으로 유도하고, 그것을 정수 틱 카운트로 바꾼다.
- [ ] 좁은 카운터가 어디서 감기는지 찾고, 그 자신의 폭으로 차분해 감김을 되돌린다.
- [ ] 소유한, 시드를 준 생성기로 난수 뽑기를 재생 가능하게 하고, 무엇이 더 고정되어야 하는지 말한다.
- [ ] 스크립트를 함수, 고정된 설정, 로그 파일, 진입점 가드 뒤의 `main()`으로 짠다.
- [ ] 함수의 입력은 명시적인 `raise`로 검증하고, 자기 불변식은 `assert`로 지키며, 일부러 고른 허용 오차로 회귀 테스트를 써서 pytest로 돌린다.

### 스스로 점검

1. `a = np.arange(4); b = a[1:]; b[0] = 9` — 이제 `a`는 무엇인가? `a = list(range(4))`로 같은 세 줄을 돌리면?
2. P6의 float32 누적 시계는 왜 참 시간 한 시간 뒤에 $3565.42$ s를 읽고, 어떤 시간 표현이 이 문제를 통째로 피하는가?
3. 페이지의 왕복에서 16비트 카운트 레지스터는 언제, 어디서 감기고, 그 `int16` 읽기의 `np.diff`는 왜 여전히 맞는 속도를 주는가?
4. 어떤 스크립트가 맨 위에서 `np.random.seed(0)`을 부르고 시뮬레이션한 엔코더 잡음을 더한다. 동료가 표식을 `np.random.random`으로 흩뜨리는 그림을 더하자, 발표한 잡음이 바뀐다. 왜 그런가, 그리고 해결은 무엇인가?
5. `err = 5.5e-8` s에 대해 `math.isclose(err, 0.0)`은 `False`를 돌려준다. 왜 그런가, 그리고 호출은 어떻게 써야 하는가?
6. 연구실 동료가 더 새 NumPy를 얻으려고 로봇 컴퓨터에서 `sudo pip install numpy --upgrade`를 돌렸고, 이제 ROS 2의 Python 도구가 이상하게 군다. 무엇이 잘못되었고, 무엇을 했어야 하는가?
7. 회귀 테스트가 $-34.57568359375$ s를 허용 오차 $10^{-9}$ s로 고정한다. 그렇게 빡빡한 허용 오차는 언제 정당하고, 언제 더 커야 하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. `array([0, 9, 2, 3])`. `a[1:]`는 뷰이므로 `b[0]`에 쓰면 `a[1]`에 쓰인다. 리스트에서 `a[1:]`는 얕은 복사라서 `a`는 `[0, 1, 2, 3]`으로 남고 `b`만 바뀐다.
> 2. $2048$ s를 넘으면 float32 값은 $u=2^{-12}$ s 간격이고 $0.005/u=20.48$이라서 틱마다의 합이 $20u=4.8828$ ms로 반올림된다. 그 전에는 $0.098\%$ 빠르다가 마지막 $26$분 동안 $2.34\%$ 느리게 가서 $34.58$ s 뒤처져 끝난다. 64비트로 정확한 정수 틱 카운트를 간직하고, 시간이 필요할 때만 $t=k/200$을 계산하면 반올림은 한 번이고 쌓이지 않는다.
> 3. 한 시간의 $42$ s째인 틱 $8{,}400$에서, 카운트가 $32{,}768$에 이르러 카트가 $16.0$ m를 지날 때다. 읽기는 $32{,}762$에서 $-32{,}768$로 뛴다. 16비트로 한 차분은 참 변화가 $2^{15}$카운트보다 작으면 정확하고, P6은 틱당 많아야 6카운트 움직이므로 감김이 상쇄된다. 먼저 64비트로 넓히면 그 뜀이 남아 $6{,}399.4\,\mathrm{m/s}$의 스파이크가 된다.
> 4. 예전 방식 함수들은 전역 흐름 하나를 공유하므로, 그림의 뽑기가 잡음이 받던 수를 먹고 뒤의 뽑기가 모두 밀린다. 잡음에 자기 생성기를 준다. `rng = np.random.default_rng(seed)`를 뽑는 함수에 건네거나, 시행마다 `spawn`한 자식 하나를 준다. 그러면 다른 코드가 그 흐름에 닿지 못한다. 그리고 흐름은 같은 빌드에서만 보장되므로 NumPy도 고정한다.
> 5. 상대 항은 $10^{-9}\times\max(5.5\times10^{-8},\,0)=5.5\times10^{-17}$로 차이보다 훨씬 작고, 0과 비교하면 다른 항이 없다. 0 아닌 값은 결코 0에 상대적으로 가깝지 않다. 허용 오차를 그 양의 단위로 준다. "1마이크로초 안"이면 `math.isclose(err, 0.0, abs_tol=1e-6)`이다.
> 6. 배포판의 도구와 ROS 2 바이너리가 기대어 빌드되고 시험된 패키지를 root 권한으로 업그레이드했다. Python 문서가 시스템 패키지 관리자와 시스템의 다른 구성 요소를 방해할 수 있다고 경고하는 일이고, Ubuntu의 pip가 기본으로 거부하는 일이다. ROS가 필요로 하는 것은 rosdep 키나 apt 패키지 `python3-numpy`로, 더 새 버전은 워크스페이스 안에 시스템 `python3`로 만들고 `COLCON_IGNORE`를 표시한 가상 환경으로 얻었어야 한다(§1).
> 7. 값이 한 dtype 안에서 올바르게 반올림되는 연산의 고정된 순서 — 여기서는 차례로 하는 float32 덧셈 — 에서 나와 어느 IEEE 기계든 비트 하나까지 재현할 때다. 그러면 $10^{-9}$ s는 출력의 반올림만 흡수한다. 부동소수점 연산의 순서나 묶음이 바뀔 수 있을 때 — `np.sum`의 쌍별 합, 스레드를 쓰는 선형대수, GPU 축약, 새 라이브러리 버전 — 허용 오차는 그 변화를 덮어야 하고 이유와 함께 적어 두어야 한다. 정수 결과는 $0$이다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6 Lab Plants]]만 쓴다. 대상은 P6의 로그이고, 모든 문제가 손잡이 하나 — 시계의 주기, 카운터의 폭, 창 — 를 바꾸므로 페이지의 어떤 숫자도 그대로 옮길 수 없다.

1. **그리기.** 위의 그림을, float32로 `t += 0.02`를 해서 제 시간을 세는 P6의 $50\,\mathrm{Hz}$ 비전 시계에 대해 다시 그린다. (a) $3600$ s 근처의 float32 눈금과 정확한 합, 저장되는 걸음, 그리고 틱마다 얻거나 잃는 양을 간격 단위와 ms로. (b) 참 시간 한 시간 동안의 오차. 계산할 수 있는 binade 교차점, 한 시간째의 값, float64 시계와 정수 틱 카운트의 자리를 넣는다.
2. **유도.** (a) $4T$씩 걷는 float32 시계가 어떤 틱 수 $k$ 뒤에든 $T$씩 걷는 float32 시계의 $k$틱 뒤 값의 정확히 네 배를 읽는다는 것을 보여라. 2의 거듭제곱을 곱하면 지수만 바뀐다는 것을 쓴다. §10이 찍은 $512$ s 교차점과 $[512, 1024)$에서의 속도로부터 20 ms 시계의 참 한 시간 뒤 오차를 계산하라. (b) $[8192, 16384)$ s에서 20 ms 시계가 저장하는 걸음과 속도, 그리고 더는 나아가지 않게 되는 읽은 값과 거기 닿는 참 시간을 구하라. (c) 각 카운터가 감기는 곳을 찾아라. 드라이브의 16비트 레지스터와 부호 있는 32비트 카운트는 P6의 이동 미터로, 32비트 마이크로초 타이머는 분으로, 그리고 그것이 처음 감기는 50 Hz 비전 틱을. 타이머 자신의 부호 없는 폭으로 한 두 읽기의 차가, 참 간격이 $2^{32}\,\mu\mathrm s$보다 짧으면 참 간격과 같다는 것을 보여라. (d) 한 시간 카운트 열을 `int16`, `int32`, `int64`로 둘 때의 메모리, 64비트 틱 열과 64비트 카운트 열을 가진 24시간 로그의 메모리, 그리고 샘플당 최대 36바이트인 Python 리스트로 둔 한 시간 카운트의 메모리를 구하라.
3. **실행.** 영어 절 템플릿의 `?` 빈칸을 채우고 §10의 실습 뒤에 돌린다. (a) 1분, 1시간, 8시간, 24시간에서 50 Hz 비전 시계의 세 시계 표, (b) 같은 $180{,}000$틱 뒤 20 ms와 5 ms float32 시계의 비, (c) 비전 주기 1개와 5개 창에 걸친 `counts[::4]`의 목표 주기 속도와 그 해상도, (d) 두 시간 동안 50 Hz의 32비트 마이크로초 스탬프 — 어디서 감기는지, 그리고 64비트와 자신의 폭에서 차분의 범위 — 를 보고하라. 각각을 §10의 5 ms 결과와 비교하라.
4. **해석.** 영어 절에 실린 연구실 동료의 스크립트는 틱과 카운트의 `(720000, 2)` `int64` 배열로 저장한 한 시간 로그에서 P6의 속도를 계산한다. 오류 없이 돈다. 실수를 여섯 개 이상 찾아, 각각이 속한 절, P6의 로그에서 결과에 미치는 영향, 해결을 말하라.

> [!note]- 그리는 법 · How to draw it
> - 읽은 값 둘레의 float32 눈금을 그리고, 간격 $u=2^{e-23}$을 초와 ms로 적는다. 정확한 합은 $T/u$칸, 저장된 값은 $\mathrm{round}(T/u)$칸에 표시하고, 차이를 칸 수와 ms로 적는다.
> - 오차, 곧 읽은 값 빼기 참 시간을 참 시간에 대해 그린다. 읽은 값 자체를 그리면 $3600$ s 중 $2.9$ s의 오차가 선 굵기 아래로 숨는다.
> - 읽은 값이 2의 거듭제곱을 지나는 곳을 표시한다. 기울기는 거기서만 바뀌고 그 사이에서는 일정하다. 네 배로 늘린 시계라면 모든 교차점이 읽은 값 네 배의 자리로 옮겨 간다.
> - 오차 축은 끝값이 아니라 한 시간 동안의 가장 큰 오차에 맞춘다. 5 ms 시계는 $34.58$ s 뒤처지기 전에 $1.84$ s 앞서 있었다.
> - float64와 정수 틱 카운트는 같은 축 위의 0선으로, 한 픽셀보다 훨씬 작은 실제 오차를 적어 둔다.
> - 한 시간째의 값과, P6이라면 오차가 제어 주기 하나와 $70\,\mathrm{ms}$ 예산을 넘는 곳을 적는다.

> [!tip]- 정답 · Solutions
> 1. $3600$ s 근처의 간격은 여전히 $u=2^{-12}$ s이고, $0.02/u=81.92$는 $82$로 올림된다. 틱마다 $82u=20.01953125$ ms를 더해 $0.08u=0.0195$ ms를 얻으니 $0.098\%$ 빠르다. 한 시간 동안 20 ms 시계는 5 ms 시계를 네 배 한 것이라서(문제 2a) §10의 교차점이 함께 옮겨 간다. 틱 $25{,}607$, 참 $512.14$ s에 $512$ s를 읽으며 $0.12$ s 뒤처지고, 틱 $102{,}332$, 참 $2046.64$ s에 $2048$ s를 읽으며 $1.38$ s 앞서고, 한 시간째에 $3602.89$ s를 읽어 $2.89$ s 앞선다. $512$ s에서 $-0.12$ s로 조금 꺼졌다가 $2^{-10}$로 곧게 오른다. 첫 느린 binade는 읽은 값 $8192$ s에서 시작해 한 시간 너머에 있다. float64 시계는 한 시간을 $3.0$ ns 틀려 끝내고 정수 틱 카운트는 $0$으로, 둘 다 0선 위에 있다.
> 2. (a) float32로의 반올림을 $\mathrm{fl}$이라 쓴다. $4=2^2$를 곱하면 지수만 바뀌므로 정규 범위의 어떤 $x$에서든 $\mathrm{fl}(4x)=4\,\mathrm{fl}(x)$다. 따라서 $\mathrm{fl}(0.02)=4\,\mathrm{fl}(0.005)$이고, $\hat t'_k=4\hat t_k$이면 $\hat t'_{k+1}=\mathrm{fl}\big(4\hat t_k+4\,\mathrm{fl}(T)\big)=4\,\mathrm{fl}\big(\hat t_k+\mathrm{fl}(T)\big)=4\hat t_{k+1}$이다. $\hat t'_0=\hat t_0=0$에서 시작하면 두 시계는 모든 틱에서 정확히 네 배 차이이고, $k\cdot4T=4\cdot kT$이므로 오차도 그렇다. 비전 시계의 참 한 시간은 $k=180{,}000$틱이고, 그때 5 ms 시계는 참 $900$ s를 돌았다. 그 시계는 참 $511.66$ s에 $+0.3439$ s로 $512$ s를 읽었고 $[512,1024)$에서 $2^{-10}$씩 얻으므로 $900$ s에서의 오차는 $0.3439+(900-511.66)\times2^{-10}=0.723$ s, 비전 시계의 한 시간 뒤 오차는 $4\times0.723=+2.89$ s다. 실행은 $+2.892578$ s를 찍는다. (b) $[8192,16384)$ s에서 $u=2^{-10}$ s, $0.02/u=20.48$은 $20$으로 내림된다. 걸음은 $19.53125$ ms, 속도는 $0.9765625$로 $2.34\%$ 느리다. 5 ms 시계의 $[2048,4096)$을 네 배 한 것이다. $0.02/u$가 $0$으로 반올림되는 곳, 곧 처음으로 $u=2^{-4}$ s인 곳에서 멈추고, 그 binade는 $2^{17}$의 네 배인 $2^{19}=524{,}288$ s에서 시작한다. (a)에 따라 5 ms 시계와 같은 틱 수, $17{,}280{,}000+5{,}638{,}663=22{,}918{,}663$틱 뒤에 거기 닿고, 20 ms로는 참 $458{,}373$ s, $127.33$시간으로 $31.83$시간의 네 배다. (c) 레지스터는 $[-32{,}768,\ 32{,}767]$을 들고 카운트가 $32{,}768$에 이를 때, 곧 $32{,}768/2048=16$ m에서 감긴다. 부호 있는 32비트 카운트는 $2^{31}/2048=1{,}048{,}576$ m에서 감긴다. 32비트 마이크로초 타이머는 $2^{32}\,\mu\mathrm s=4294.97$ s $=71.58$분마다 감긴다. 비전 틱 $k$는 $20{,}000\,k\bmod 2^{32}$를 읽으므로 처음으로 앞 값보다 작아지는 것은 $k=\lceil2^{32}/20{,}000\rceil=214{,}749$다. $b-a<2^{32}$인 참 시각 $a\le b$에서 읽기는 $a\bmod2^{32}$와 $b\bmod2^{32}$이고, 그 차를 $2^{32}$로 줄이면 $(b-a)\bmod2^{32}=b-a$다. 나머지 연산은 뺄셈과 교환되고 $b-a$는 이미 범위 안이기 때문이다. 부호 없는 32비트 뺄셈이 바로 $2^{32}$을 법으로 한 뺄셈이다. (d) 카운트 $720{,}000$개는 `int16`으로 $1.44$ MB, `int32`로 $2.88$ MB, `int64`로 $5.76$ MB다. 64비트 열 둘인 하루 로그는 $17{,}280{,}000\times16=276.48$ MB, 샘플당 최대 36바이트 리스트로 둔 한 시간은 최대 $25.9$ MB다. 모두 노트북 메모리에 들어간다. 하루 로그에 필요한 것은 더 적은 메모리가 아니라 맞는 타입이다. float32 초 대신 64비트 틱 열(§5), 충분히 넓거나 자신의 폭으로 차분하는 카운트 열(§6).
> 3. 빈칸은 `1 / VISION_HZ`, `sec * VISION_HZ`, `T_S`, `shuttle_counts(3_600)[::4]`, `(N_PER_M * w * T_V)`, `2**32`, `np.uint32`다. 채운 블록과 그 출력은 영어 절의 정답 3에 있고, 요약하면:
>
>    | 시간 범위 | 비전 틱 | float32 시계 (s) | float32 오차 (s) | float64 오차 (s) |
>    |---|---:|---:|---:|---:|
>    | 1분 | 3,000 | 60.001183 | +0.001183 | +3.78e-12 |
>    | 1시간 | 180,000 | 3,602.892578 | +2.892578 | -2.98e-09 |
>    | 8시간 | 1,440,000 | 28,324.197266 | -475.802734 | +5.36e-07 |
>    | 24시간 | 4,320,000 | 88,381.835938 | +1,981.835938 | -3.72e-07 |
>
>    같은 $180{,}000$틱 뒤 20 ms 시계와 5 ms 시계의 비는 $4.0$이다. 비전 주기 1개 창은 $0.48828$과 $0.51270$ m/s, 해상도 $0.02441$ m/s이고, 5개 창은 $0.49805$와 $0.50293$ m/s, 해상도 $0.00488$ m/s다. 타이머는 비전 틱 $214{,}749$($71.58$분)에서 감기고, 64비트 차분은 $-4{,}294{,}947{,}296$에서 $20{,}000\,\mu\mathrm s$까지, 32비트 차분은 어디서나 $20{,}000\,\mu\mathrm s$다. (a) 한 시간 뒤 비전 시계는 5 ms 시계가 $34.58$ s 뒤처졌던 곳에서 $2.89$ s *앞선다*. 주기가 네 배라 같은 binade 무늬가 읽은 값 네 배의 자리에 오므로, 한 시간째에는 5 ms 시계가 $2048$ s에서 떠났던 빠른 binade에 아직 있다. 8시간에 $475.80$ s 뒤처지고 24시간에 $1{,}981.84$ s 앞선다. float64 오차 — 한 시간에 $-2.98$ ns, 24시간에 $-3.72\times10^{-7}$ s — 는 사분의 일만큼의 덧셈에서 온다. (b) 비는 문제 2(a)가 증명하듯 정확히 $4.0$이다. (c) §10의 200 Hz 창 4틱과 20틱과 같다. 해상도는 주기와 상관없이 $1/(N\cdot\text{창의 길이})$이기 때문이다. (d) 64비트 차분에서 감김은 거의 $2^{32}$인 음의 간격으로 나타나고, 32비트 차분은 어디서나 맞다. §6의 레지스터 규칙을 시간에 적용한 것이다.
> 4. Mac에서 페이지의 한 시간 카운트 위에 스크립트를 돌려 확인한 실수 여섯:
>    - **§2, 가변 기본값.** `cache=[]`는 프로세스 전체에 리스트 하나다. 호출마다 $11.52$ MB 로그를 하나 더 붙이고 풀어 주지 않으며, 거기 간직된 배열은 다섯째 실수가 다시 쓰는 바로 그것이다. 해결: 기본 컨테이너를 두지 않고, 캐시가 필요하면 호출자가 소유한다.
>    - **§4, $719{,}999$틱에 대한 Python 반복.** 파일이 이미 가진 열을 다시 만든다. 해결: `t = log[:, 0] / 200`.
>    - **§5, float32 누적 시계.** 시간 열은 한 시간을 $34.58$ s 모자라게 끝내고, $2046$ s부터는 `np.diff(t)`가 모두 $4.8828$ ms라서 마지막 $26$분의 속도가 모두 $2.4\%$ 높다. 카운트로는 $0.48828$과 $0.58594$인 곳에서 $0.5$와 $0.6\,\mathrm{m/s}$가 나온다. 해결: 위의 정수 틱.
>    - **§6, 차분 전에 넓힌 좁은 타입.** `astype(np.int16)`은 $32{,}767$을 넘는 카운트의 아래 16비트만 남기고 — Mac에서 $40{,}960$이 $-24{,}576$이 되었다 — `np.diff` 전에 넓히면 감김마다 스파이크가 되어, float32 시간 걸음으로 가장 큰 것이 $6{,}553\,\mathrm{m/s}$다. 해결: `int64` 카운트를 그대로 두거나, `int16` 값을 16비트로 차분한 뒤 넓게 누적한다.
>    - **§3, 뷰를 통한 제자리 쓰기.** `mid = log[:, 1]`은 뷰라서 `mid -= 20_480`이 읽어 온 로그와 캐시된 로그를 다시 쓴다. 틱 4,000이 그 뒤 $-10{,}240$을 읽는다. 해결: `mid = log[:, 1] - 20_480`.
>    - **§7, 전역 시드.** 함수 안의 `np.random.seed(0)`은 부를 때마다 프로세스 전체의 흐름을 초기화하므로, 호출자가 그 뒤에 뽑는 자기 시드의 수는 더는 그것이 시드한 수가 아니고, 잡음은 다른 코드가 그 흐름에서 뽑지 않는 동안에만 재현된다. 해결: `Generator` 인자를 받아 `rng.normal`을 부른다.

### 출처

- Python 3 문서([docs.python.org](https://docs.python.org/3/), 3.14판, 2026-09-23에 읽음) — [Installing Python Modules](https://docs.python.org/3/installing/index.html)(시스템 Python에는 설치하지 않음), [venv](https://docs.python.org/3/library/venv.html)(`pyvenv.cfg`, `sys.prefix != sys.base_prefix`, 옮길 수 없음), 튜토리얼 [12장](https://docs.python.org/3/tutorial/venv.html)(`pip freeze`, `-r requirements.txt`), [§6.1.2](https://docs.python.org/3/tutorial/modules.html)(모듈 검색 경로), [§4.9.1](https://docs.python.org/3/tutorial/controlflow.html)과 [레퍼런스 §8.7](https://docs.python.org/3/reference/compound_stmts.html)(기본값은 한 번 평가), [레퍼런스 §3.1](https://docs.python.org/3/reference/datamodel.html)(정체, 가변성), [레퍼런스 §7.3](https://docs.python.org/3/reference/simple_stmts.html)(`-O`에서 `assert` 제거), [튜토리얼 15장](https://docs.python.org/3/tutorial/floatingpoint.html)(binary64). 라이브러리 페이지 `copy`, `math`(`isclose`, `ulp`), `random`, `__main__`, `dataclasses`(`frozen`, 3.11부터 해시할 수 없는 기본값 거부, `replace`), `typing`, `logging`(`basicConfig`와 `force=True`), `argparse`.
- NumPy 2.5 문서([numpy.org/doc/stable](https://numpy.org/doc/stable/)) — [N차원 배열](https://numpy.org/doc/stable/reference/arrays.ndarray.html)(stride 오프셋), [복사와 뷰](https://numpy.org/doc/stable/user/basics.copies.html), [데이터 타입과 넘침](https://numpy.org/doc/stable/user/basics.types.html), `cumsum`, `spacing`, `isclose`. [난수 생성기](https://numpy.org/doc/stable/reference/random/generator.html)(`default_rng`, PCG64, `spawn`), [난수 표집](https://numpy.org/doc/stable/reference/random/index.html)(예전의 전역 `RandomState`), [호환성 정책](https://numpy.org/doc/stable/reference/random/compatibility.html)(같은 빌드에서만 같은 흐름). [NumPy 2.0 이전 안내](https://numpy.org/doc/stable/numpy_2_0_migration_guide.html)(64비트 기본 정수)와 [NEP 50](https://numpy.org/neps/nep-0050-scalar-promotion.html)(Python 스칼라는 약한 타입).
- ROS 2 문서, jazzy — [Using Python Packages with ROS 2](https://github.com/ros2/ros2_documentation/blob/jazzy/source/How-To-Guides/Using-Python-Packages.rst): 인터프리터는 바이너리와 일치해야 함, rosdep, 시스템 패키지 관리자, `COLCON_IGNORE`를 표시한 가상 환경, Bloom과 rosdep 키.
- ROS 2 소스, jazzy — [Time.msg](https://github.com/ros2/rcl_interfaces/blob/jazzy/builtin_interfaces/msg/Time.msg)(`int32 sec`, `uint32 nanosec`), [rcutils time.h](https://github.com/ros2/rcutils/blob/jazzy/include/rcutils/time.h)(`int64_t` 나노초), [rclpy time.py](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/time.py)($2^{63}$에서 `OverflowError`).
- REP 2000([ros-infrastructure/rep](https://github.com/ros-infrastructure/rep/blob/master/rep-2000.rst)) — Ubuntu 24.04 위의 Jazzy, Python 3.12.3.
- Ubuntu의 [Develop with Python on Ubuntu](https://ubuntu.com/developers/docs/tutorials/python-use/) — "externally managed environment" 오류, `apt install python3-xyz` 또는 venv, PEP 668.
- pytest 문서([docs.pytest.org](https://docs.pytest.org/en/stable/)) — 테스트 발견, 평범한 `assert`, `pytest.raises`, `pytest.approx`(기본 상대 $10^{-6}$, 절대 $10^{-12}$).
