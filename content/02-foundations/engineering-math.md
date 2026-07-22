---
title: 0.5 Engineering Math
tags: [foundations]
---

> [[02-foundations/overview|0. Overview]] — 이 페이지가 어디에 쓰이는지의 지도 · where this page fits

## English

The engineering math that pages 1–7 silently assume, self-contained in one place. Each
section says exactly which foundation page uses it. If all of this reads easily, skip
straight to [[02-foundations/linear-algebra|1. Linear Algebra]].

### 1. Derivatives (→ used by 2. Calculus, 4. Optimization)

- Definition as sensitivity: $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ — "nudge the
  input, how much does the output move?"
- The rules you actually use:

| Rule | Formula |
|---|---|
| Power | $(x^n)' = nx^{n-1}$ |
| Product | $(fg)' = f'g + fg'$ |
| **Chain** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — the rule backprop is built on |
| Exp/Log | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **Partial derivative** $\partial f/\partial x_i$: differentiate w.r.t. one variable,
  hold the rest fixed. The **gradient** $\nabla f = (\partial f/\partial x_1, \ldots)$
  stacks them into a vector.
- Worked example (the shape of every loss-gradient computation):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — outer derivative
  times inner derivative, chain rule in action.

### 2. Taylor expansion (→ 2. Calculus, 4. Optimization)

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"Any smooth function is locally a line (1st order) or a parabola (2nd order)."
Gradient descent trusts the line; Newton's method trusts the parabola. Sanity check with
$f = x^2$ at $x=1$: $f(1+\delta) = 1 + 2\delta + \delta^2$ — exact, because $x^2$ *is* a
parabola.

### 3. Integrals and expectations (→ 3. Probability)

- An integral is a weighted sum in the continuum limit: $\int f(x)\,dx$.
- The only integral pattern the foundations really use:
  $E[g(X)] = \int g(x)\,p(x)\,dx$ — "average $g$ over the distribution $p$."
  In code this is always a sample mean; you almost never solve integrals by hand here.
- $\int p(x)\,dx = 1$ (probabilities sum to one) is the identity used in half the proofs
  (e.g., KL non-negativity in [[02-foundations/information-theory|5. Information Theory]]).

### 4. Matrix arithmetic (→ 1. Linear Algebra — its entry requirement)

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: row of $A$ · column of $B$. Shapes:
  $(m\times n)(n \times p) = m \times p$.
- Worked 2×2:
  $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}2&1\\4&3\end{pmatrix}$
  (it swapped the columns — matrices *do things*).
- Not commutative: $AB \ne BA$ in general. Transpose flips indices ($A^\top_{ij} = A_{ji}$);
  identity $I$ changes nothing; the inverse $A^{-1}$ undoes ($A^{-1}A = I$) and only exists
  for square, full-rank $A$.

### 5. Series and the geometric sum (→ 7. RL Basics)

$$1 + \gamma + \gamma^2 + \cdots = \frac{1}{1-\gamma} \quad (|\gamma| < 1)$$

Two-line proof: let $S$ be the sum; $\gamma S = S - 1$ ⇒ $S = 1/(1-\gamma)$.
This single identity is why a discount factor $\gamma = 0.99$ means "an effective horizon
of about $1/(1-\gamma) = 100$ steps" in [[02-foundations/rl-basics|RL]].

### 6. Exponentials and logarithms (→ 5. Information Theory — its entry requirement)

- $e^x$: the function that is its own derivative; growth at a rate proportional to itself.
- $\log$ is its inverse: $\log(e^x) = x$. The three rules that carry all of information
  theory and every likelihood computation:

| Rule | Why it matters |
|---|---|
| $\log(ab) = \log a + \log b$ | products of probabilities → **sums** of log-probs (why losses are sums) |
| $\log(a^n) = n\log a$ | powers become multiplications |
| $\log_b x = \ln x / \ln b$ | base 2 (bits) vs base e (nats) differ by a constant — that's all |

- Numbers to internalize: $\log 1 = 0$; $\log x < 0$ for $x<1$ (log-probs are negative!);
  $\log$ grows painfully slowly.
- **Log-sum-exp**: $\log \sum_i e^{x_i}$ — computed stably as
  $x_{max} + \log\sum_i e^{x_i - x_{max}}$; the reason softmax+cross-entropy code never
  overflows ([[02-foundations/calculus-backprop|2. Calculus §4]]).

### 7. Complex numbers and Euler's formula (→ 6. Signal Processing — its entry requirement)

- $j = \sqrt{-1}$; a complex number $a + jb$ is a point in the 2D plane;
  $|a+jb| = \sqrt{a^2+b^2}$ is its length, and its angle is $\theta = \arctan(b/a)$.
- **Euler's formula**: $e^{j\theta} = \cos\theta + j\sin\theta$ — the unit-circle point at
  angle $\theta$. Consequence: multiplying by $e^{j\theta}$ **rotates** by $\theta$.
- That is the whole reason Fourier analysis works: a sinusoid is the real part of a
  rotating $e^{j\omega t}$, so "decompose into sinusoids" = "project onto rotations" — the
  DFT formula in [[02-foundations/signal-processing|6. Signal Processing]] is exactly this
  projection.

### 8. Linear differential equations (→ control: [[04-robotics/control-theory-ce397|CE397]], [[04-robotics/lqr-lqg|LQR]])

Physical systems are described by ODEs — this is the modeling language of all of control.

- **First order**: $\dot x = ax$ has solution $x(t) = x(0)\,e^{at}$. Everything follows from
  this one fact: $a < 0$ decays (stable), $a > 0$ blows up (unstable). A robot joint,
  a heating room, a draining tank — all locally this equation.
- **With input**: $\dot x = ax + bu$ — the solution is "decayed initial state + accumulated
  input"; this is the scalar version of the state-space model
  $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$ ([[02-foundations/linear-algebra|linear algebra §5]]),
  and $e^{at}$ becomes the matrix exponential $e^{At}$ with eigenvalues playing the role of $a$.
- **Second order**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — the
  mass-spring-damper. Two numbers describe every response: natural frequency $\omega_n$
  (how fast it oscillates) and damping ratio $\zeta$ (whether it rings: $\zeta<1$
  oscillates, $\zeta \ge 1$ doesn't). Robot arms and suspension systems are tuned in this
  vocabulary.
- Discrete time (what code runs): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — stable iff
  $|a| < 1$. The continuous/discrete stability conditions ($\text{Re} < 0$ vs $|\cdot|<1$)
  are the two halves of one story.

### 9. Laplace transform and the s-plane (→ control, [[02-foundations/signal-processing|6. Signal Processing §5]])

The Laplace transform turns ODEs into algebra:

- Definition: $F(s) = \int_0^\infty f(t)\,e^{-st}\,dt$; the one property that matters:
  **differentiation becomes multiplication by $s$** — $\mathcal{L}[\dot f] = sF(s) - f(0)$.
- Consequence: an ODE becomes a polynomial equation, and a system becomes a
  **transfer function** $G(s) = \frac{\text{output}(s)}{\text{input}(s)}$ — e.g.,
  $\dot x = ax + u$ gives $G(s) = \frac{1}{s - a}$.
- **Poles** = roots of the denominator = the $a$'s of section 8 = eigenvalues of the
  state-space $A$. Plotted in the complex **s-plane**:
  - left half-plane (negative real part) → decaying → **stable**
  - right half-plane → growing → **unstable**
  - imaginary part → oscillation frequency; distance from axis → decay speed
- This is why [[02-foundations/engineering-math|§7]]'s complex plane matters for control:
  *a system's entire qualitative behavior is a picture — where its poles sit.* Frequency
  response is $G(j\omega)$ — evaluate on the imaginary axis, and you recover
  [[02-foundations/signal-processing|signal processing]]'s filters. (Discrete-time twin:
  the Z-transform, unit circle instead of left half-plane.)

### 10. Notation dictionary (all pages)

| Symbol | Read as |
|---|---|
| $\sum_i$, $\prod_i$ | sum / product over index $i$ |
| $\arg\max_x f(x)$ | the $x$ that maximizes $f$ (not the max value itself) |
| $E[\cdot]$, $\text{Var}(\cdot)$ | expectation, variance |
| $x \sim p$ | $x$ is sampled from distribution $p$ |
| $\propto$ | proportional to (equal up to a constant) |
| $\|x\|$ | norm (length) of $x$ |
| $\mathbb{1}[\cdot]$ | indicator: 1 if true, 0 if false |
| $\odot$ | element-wise product |
| $:=$ | defined as |

### Self-check

1. Differentiate $f(x) = \log(1 + e^x)$ (softplus) using the chain rule; show the result
   is the sigmoid.
2. Use the geometric sum to explain why rewards ~200 steps away are nearly invisible to an
   agent with $\gamma = 0.99$.
3. Show $\log \frac{a}{b} = \log a - \log b$ from the product rule.
4. Compute $e^{j\pi}$ from Euler's formula and interpret the result as a rotation.

## 한국어

1~7 페이지가 말없이 전제하는 공업수학을 한곳에 자체 완결로 정리했다.
각 절이 정확히 어느 기초 페이지에 쓰이는지 표시했다. 전부 술술 읽히면 바로
[[02-foundations/linear-algebra|1. 선형대수]]로 건너뛰어라.

### 1. 미분 (→ 2. 미적분, 4. 최적화에서 사용)

- 민감도로서의 정의: $f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$ — "입력을 살짝 밀면
  출력이 얼마나 움직이는가?"
- 실제로 쓰는 규칙들:

| 규칙 | 공식 |
|---|---|
| 거듭제곱 | $(x^n)' = nx^{n-1}$ |
| 곱 | $(fg)' = f'g + fg'$ |
| **연쇄** | $(f(g(x)))' = f'(g(x))\,g'(x)$ — 역전파가 세워진 그 규칙 |
| 지수/로그 | $(e^x)' = e^x$, $(\ln x)' = 1/x$ |

- **편미분** $\partial f/\partial x_i$: 한 변수로만 미분하고 나머지는 고정.
  **그래디언트** $\nabla f = (\partial f/\partial x_1, \ldots)$는 그것들을 벡터로 쌓은 것.
- 계산 예제 (모든 손실-그래디언트 계산의 원형):
  $f(x, y) = (xy - 3)^2$ ⇒ $\partial f/\partial x = 2(xy-3)\cdot y$ — 바깥 미분 × 안쪽
  미분, 연쇄 법칙의 실전.

### 2. 테일러 전개 (→ 2. 미적분, 4. 최적화)

$$f(x + \delta) \approx f(x) + f'(x)\,\delta + \tfrac12 f''(x)\,\delta^2$$

"매끄러운 함수는 국소적으로 직선(1차)이거나 포물선(2차)이다." 경사 하강은 직선을 믿고,
뉴턴법은 포물선을 믿는다. $f = x^2$, $x=1$에서 검산: $f(1+\delta) = 1 + 2\delta + \delta^2$
— 정확히 맞다, $x^2$ 자체가 포물선이니까.

### 3. 적분과 기댓값 (→ 3. 확률)

- 적분은 연속 극한의 가중합이다: $\int f(x)\,dx$.
- 기초 페이지들이 실제로 쓰는 적분 패턴은 사실상 하나:
  $E[g(X)] = \int g(x)\,p(x)\,dx$ — "분포 $p$ 위에서 $g$의 평균." 코드에서는 언제나 샘플
  평균이 되고, 여기서 적분을 손으로 풀 일은 거의 없다.
- $\int p(x)\,dx = 1$ (확률의 합은 1) — 증명의 절반에 쓰이는 항등식이다
  (예: [[02-foundations/information-theory|5. 정보이론]]의 KL 비음수성).

### 4. 행렬 연산 (→ 1. 선형대수의 입장 조건)

- $(AB)_{ij} = \sum_k A_{ik}B_{kj}$: $A$의 행 · $B$의 열. 모양:
  $(m\times n)(n \times p) = m \times p$.
- 2×2 계산 예제:
  $\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}0&1\\1&0\end{pmatrix} = \begin{pmatrix}2&1\\4&3\end{pmatrix}$
  (열이 서로 바뀌었다 — 행렬은 *무언가를 한다*).
- 교환 법칙 없음: 일반적으로 $AB \ne BA$. 전치는 인덱스를 뒤집고($A^\top_{ij} = A_{ji}$),
  항등 행렬 $I$는 아무것도 바꾸지 않으며, 역행렬 $A^{-1}$은 되돌린다($A^{-1}A = I$) —
  정방·풀랭크일 때만 존재.

### 5. 급수와 기하급수 합 (→ 7. RL 기초)

$$1 + \gamma + \gamma^2 + \cdots = \frac{1}{1-\gamma} \quad (|\gamma| < 1)$$

두 줄 증명: 합을 $S$라 하면 $\gamma S = S - 1$ ⇒ $S = 1/(1-\gamma)$.
이 항등식 하나가 [[02-foundations/rl-basics|RL]]에서 할인율 $\gamma = 0.99$가 "유효 지평
약 $1/(1-\gamma) = 100$ 스텝"을 뜻하는 이유다.

### 6. 지수와 로그 (→ 5. 정보이론의 입장 조건)

- $e^x$: 자기 자신이 도함수인 함수; 자신에 비례하는 속도로 성장.
- $\log$는 그 역함수: $\log(e^x) = x$. 정보이론 전체와 모든 우도 계산을 떠받치는 세 규칙:

| 규칙 | 왜 중요한가 |
|---|---|
| $\log(ab) = \log a + \log b$ | 확률의 곱 → 로그 확률의 **합** (손실이 합인 이유) |
| $\log(a^n) = n\log a$ | 거듭제곱이 곱셈이 된다 |
| $\log_b x = \ln x / \ln b$ | 밑 2(비트)와 밑 e(나트)는 상수배 차이 — 그게 전부다 |

- 몸에 익힐 숫자 감각: $\log 1 = 0$; $x<1$이면 $\log x < 0$ (로그 확률은 음수다!);
  $\log$는 고통스럽게 천천히 자란다.
- **Log-sum-exp**: $\log \sum_i e^{x_i}$ — 안정적으로는
  $x_{max} + \log\sum_i e^{x_i - x_{max}}$로 계산; softmax+교차 엔트로피 코드가 오버플로
  하지 않는 이유다 ([[02-foundations/calculus-backprop|2. 미적분 §4]]).

### 7. 복소수와 오일러 공식 (→ 6. 신호처리의 입장 조건)

- $j = \sqrt{-1}$; 복소수 $a + jb$는 2차원 평면의 점;
  $|a+jb| = \sqrt{a^2+b^2}$가 길이, 각도는 $\theta = \arctan(b/a)$.
- **오일러 공식**: $e^{j\theta} = \cos\theta + j\sin\theta$ — 각도 $\theta$의 단위원 위의 점.
  따름정리: $e^{j\theta}$를 곱하는 것 = $\theta$만큼 **회전**.
- 푸리에 분석이 작동하는 이유의 전부가 이것이다: 사인파는 회전하는 $e^{j\omega t}$의
  실수부이므로, "사인파로 분해" = "회전들에 투영" —
  [[02-foundations/signal-processing|6. 신호처리]]의 DFT 공식이 정확히 이 투영이다.

### 8. 선형 미분방정식 (→ 제어: [[04-robotics/control-theory-ce397|CE397]], [[04-robotics/lqr-lqg|LQR]])

물리 시스템은 미분방정식으로 기술된다 — 제어 전체의 모델링 언어다.

- **1차**: $\dot x = ax$의 해는 $x(t) = x(0)\,e^{at}$. 모든 것이 이 한 사실에서 나온다:
  $a < 0$이면 감쇠(안정), $a > 0$이면 폭발(불안정). 로봇 관절, 데워지는 방, 빠지는 물탱크
  — 전부 국소적으로 이 방정식이다.
- **입력이 있으면**: $\dot x = ax + bu$ — 해는 "감쇠한 초기 상태 + 누적된 입력";
  상태공간 모델 $\dot{\mathbf{x}} = A\mathbf{x} + B\mathbf{u}$
  ([[02-foundations/linear-algebra|선형대수 §5]])의 스칼라판이고, $e^{at}$는 행렬 지수
  $e^{At}$가 되며 고유값이 $a$의 역할을 한다.
- **2차**: $\ddot x + 2\zeta\omega_n \dot x + \omega_n^2 x = 0$ — 질량-스프링-댐퍼.
  모든 응답을 두 숫자가 기술한다: 고유 진동수 $\omega_n$(얼마나 빨리 진동하나)과 감쇠비
  $\zeta$(울리는가: $\zeta<1$이면 진동, $\zeta \ge 1$이면 안 함). 로봇 팔과 서스펜션이
  이 어휘로 튜닝된다.
- 이산 시간 (코드가 실제로 도는 곳): $x_{t+1} = a x_t$ ⇒ $x_t = a^t x_0$ — $|a| < 1$일
  때만 안정. 연속/이산의 안정 조건($\text{Re} < 0$ vs $|\cdot|<1$)은 한 이야기의 두 반쪽이다.

### 9. 라플라스 변환과 s-평면 (→ 제어, [[02-foundations/signal-processing|6. 신호처리 §5]])

라플라스 변환은 미분방정식을 대수로 바꾼다:

- 정의: $F(s) = \int_0^\infty f(t)\,e^{-st}\,dt$; 중요한 성질은 하나:
  **미분이 $s$ 곱하기가 된다** — $\mathcal{L}[\dot f] = sF(s) - f(0)$.
- 따름정리: 미분방정식이 다항 방정식이 되고, 시스템이 **전달함수**
  $G(s) = \frac{\text{출력}(s)}{\text{입력}(s)}$가 된다 — 예: $\dot x = ax + u$이면
  $G(s) = \frac{1}{s - a}$.
- **극점** = 분모의 근 = 8절의 $a$들 = 상태공간 $A$의 고유값. 복소 **s-평면**에 그리면:
  - 좌반평면(실수부 음수) → 감쇠 → **안정**
  - 우반평면 → 성장 → **불안정**
  - 허수부 → 진동 주파수; 축에서의 거리 → 감쇠 속도
- [[02-foundations/engineering-math|§7]]의 복소평면이 제어에서 중요한 이유가 이것이다:
  *시스템의 정성적 거동 전체가 그림 하나 — 극점이 어디에 앉아 있는가 — 다.* 주파수 응답은
  $G(j\omega)$ — 허수축 위에서 평가하면 [[02-foundations/signal-processing|신호처리]]의
  필터가 복원된다. (이산 시간의 쌍둥이: Z-변환, 좌반평면 대신 단위원.)

### 10. 표기법 사전 (전 페이지 공용)

| 기호 | 읽는 법 |
|---|---|
| $\sum_i$, $\prod_i$ | 인덱스 $i$에 대한 합 / 곱 |
| $\arg\max_x f(x)$ | $f$를 최대화하는 $x$ (최댓값 자체가 아니라) |
| $E[\cdot]$, $\text{Var}(\cdot)$ | 기댓값, 분산 |
| $x \sim p$ | $x$를 분포 $p$에서 샘플링 |
| $\propto$ | 비례 (상수배를 무시하면 같음) |
| $\|x\|$ | $x$의 노름(길이) |
| $\mathbb{1}[\cdot]$ | 지시 함수: 참이면 1, 거짓이면 0 |
| $\odot$ | 원소별 곱 |
| $:=$ | ~로 정의함 |

### 스스로 점검

1. $f(x) = \log(1 + e^x)$ (softplus)를 연쇄 법칙으로 미분하고, 결과가 시그모이드임을 보여라.
2. 기하급수 합으로, $\gamma = 0.99$인 에이전트에게 200 스텝 뒤의 보상이 거의 안 보이는
   이유를 설명하라.
3. 곱 규칙에서 $\log \frac{a}{b} = \log a - \log b$를 유도하라.
4. 오일러 공식으로 $e^{j\pi}$를 계산하고, 그 결과를 회전으로 해석하라.
