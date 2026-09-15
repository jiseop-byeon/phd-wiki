---
title: 11.1 Complexity, Recursion & Backtracking
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "State and defend the time and space complexity of any loop, recursion, or backtracking search you write, and write those recursions correctly under interview pressure."
mastery-when: "Raise to Mastery only if the thesis contribution is itself an algorithm whose complexity must be proved rather than measured."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §5]] (the geometric sum, used for doubling arrays and recursion trees) · [[02-foundations/engineering-math|0.5 §6]] (logarithms)
> [[02-foundations/engineering-math|0.5 §5]](기하급수 합 — 배열 두 배 증가와 재귀 트리에 쓰인다) · [[02-foundations/engineering-math|0.5 §6]](로그)
>
> Track map · 트랙 지도: [[02-foundations/algorithms/index|11. Algorithms & Data Structures]]

## English

*The first page of the algorithms track. Every later page states a complexity and expects you to be able to check it; this page is where that checking skill is built.*

Almost every coding interview ends with "what is the time and space complexity?", and a research-lab interview adds "why is this slow on the real data?". Both questions have the same answer: count how many times the dominant operation runs as a function of the input size, and say which case you are counting. This page gives you the vocabulary (O, Ω, Θ), the three counting tools (loops, recurrences, amortization), and the one search pattern — backtracking — that turns "try everything" into correct code.

> [!note] First pass · 처음이라면
> Read §1, §2 and §7 first: they are what you will say out loud in every interview. §3 and §4 are needed the first time a recursion or a growing array appears in your answer. §5 and §6 are the code patterns — practise them from a blank file.

### 1. What an interviewer means by "efficient"

"Efficient" in an interview means three agreed simplifications.

- **Input size $n$.** Running time is a function of how big the input is — the number of points, the length of the string, the number of vertices and edges. When there are several sizes, keep them separate: a graph algorithm is $O(V + E)$, not $O(n)$.
- **Worst case, unless you say otherwise.** For each $n$ we take the slowest input of that size. A worst-case bound is a guarantee: no input of that size will be slower. Average case, expected (for randomized algorithms) and amortized (§4) are different promises and must be named when you use them.
- **Constants and lower-order terms are dropped.** $3n^2 + 40n + 7$ becomes $n^2$. The reason is not that constants are unimportant — a 10× constant matters on a robot — but that they depend on the machine, the language and the compiler, while the growth rate belongs to the algorithm. For large enough $n$, a lower growth rate wins over any constant factor.

**The doubling check.** Growth rates make a testable prediction: what happens to the running time when $n$ doubles. Measure the time at $n$ and at $2n$; the ratio tells you the class.

| Growth | Time when $n$ doubles |
|---|---|
| $\Theta(1)$ | unchanged |
| $\Theta(\log n)$ | grows by a constant amount |
| $\Theta(n)$ | ×2 |
| $\Theta(n \log n)$ | a little over ×2 |
| $\Theta(n^2)$ | ×4 |
| $\Theta(n^3)$ | ×8 |
| $\Theta(2^n)$ | squared — already ×2 when $n$ grows by one |

For polynomial growth $n^k$, $\log_2(\text{ratio}) \approx k$. This is the fastest way to find out whether code you did not write is secretly quadratic.

```python
import time

def doubling_ratios(f, sizes):
    """Time f(n) for each size; return the ratios t(next) / t(previous)."""
    times = []
    for n in sizes:
        start = time.perf_counter()
        f(n)
        times.append(time.perf_counter() - start)
    return [later / earlier for earlier, later in zip(times, times[1:])]

def all_pairs(n):                  # deliberately quadratic
    return sum(1 for i in range(n) for j in range(n))

print(doubling_ratios(all_pairs, [800, 1600, 3200]))  # each ratio roughly 4 (timing is noisy)
```

**A time budget (rough rule, not a law).** Assume a compiled language does on the order of $10^8$ simple operations per second. Then the largest input that finishes in about a second is roughly:

| Complexity | Largest $n$ in ~1 s (compiled) |
|---|---|
| $O(n!)$ | ~11 |
| $O(2^n)$, $O(n\,2^n)$ | ~25, ~20 |
| $O(n^3)$ | a few hundred |
| $O(n^2)$ | ~$10^4$ |
| $O(n \log n)$ | ~$10^6$ to $10^7$ |
| $O(n)$ | ~$10^8$ |

Pure-Python loops with realistic bodies (indexing, dictionary lookups, function calls) are roughly 10 to 100 times slower — even a bare `for` loop doing one addition manages only about $2 \times 10^7$ iterations per second on a current laptop — so divide those limits accordingly; NumPy operations that stay inside compiled code are closer to the compiled row. Read the table backwards in an interview: a constraint "$n \le 10^5$" is telling you that $O(n^2)$ will not pass and $O(n \log n)$ will.

### 2. Big-O, Ω, Θ precisely, and reading loops

The three symbols are statements about eventual growth, each with a constant you get to choose. We say $f = O(g)$ when $f$ is eventually at most a constant multiple of $g$, written out because the definition is what you fall back on when intuition fails:

$$f(n) = O(g(n)) \iff \exists\, c > 0,\ n_0 \text{ such that } 0 \le f(n) \le c\,g(n) \text{ for all } n \ge n_0$$

- $f = \Omega(g)$: the same with $f(n) \ge c\,g(n)$ — $g$ is an eventual **lower** bound.
- $f = \Theta(g)$: both — $c_1 g(n) \le f(n) \le c_2 g(n)$ for large $n$. This is the **tight** bound, and it is what people usually mean when they say "big-O" in conversation.
- The constants $c$ and $n_0$ must not depend on $n$. That one rule is what makes "$n^2 = O(n)$" false: it would need $c \ge n$.

Example: $3n^2 + 10n + 5 = \Theta(n^2)$. For $n \ge 1$, $3n^2 \le 3n^2 + 10n + 5 \le 3n^2 + 10n^2 + 5n^2 = 18n^2$, so $c_1 = 3$, $c_2 = 18$, $n_0 = 1$ work.

Two distinctions that interviewers probe:

- **Bound versus case.** O/Ω/Θ describe functions; worst/best/average case says *which* function you are describing. Insertion sort's worst-case time is $\Theta(n^2)$ and its best-case time is $\Theta(n)$. "Insertion sort is $O(n^2)$" is true for every input; "insertion sort is $\Theta(n^2)$" is false as a claim about every input.
- **Log bases do not matter; exponential bases do.** $\log_2 n$ and $\log_{10} n$ differ by a constant factor, so we write $O(\log n)$. But $4^n = (2^n)^2$ is not $O(2^n)$.

**Reading loops.** Three rules cover most interview code:

1. **Sequential blocks add**, and the largest term survives: $O(n) + O(n \log n) = O(n \log n)$. With two different sizes keep both: $O(n + m)$.
2. **Nested loops multiply** when the inner count does not depend on the outer variable. When it does, **sum** the inner counts instead of multiplying the maxima.
3. **A loop variable multiplied or divided by a constant** runs $\Theta(\log n)$ times, because after $k$ halvings $n/2^k$ reaches 1 when $k = \log_2 n$.

> [!example] Worked example · 계산 예제
> **1. A triangular double loop.** In `for i in range(n): for j in range(i + 1, n)`, the inner loop runs $n-1, n-2, \dots, 0$ times. The sum is $n(n-1)/2$, so the pair loop is $\Theta(n^2)$ — the same class as the full square, even though it does half the work.
>
> **2. Halving.** `while n > 1: n //= 2` runs $\lfloor \log_2 n \rfloor$ times: 10 times for $n = 1024$, 9 for $n = 1000$. Put it inside a loop over $n$ items and the total is $\Theta(n \log n)$.
>
> **3. A nested loop that is linear.** In a sliding window (code below) the inner `while` can run many times for one value of `right`, so "nested, therefore $n^2$" is tempting. But `left` only moves forward and never passes $n$, so across the whole run the inner body executes at most $n$ times in total. Outer $n$ plus inner $n$ is $\Theta(n)$. Counting the total work of a pointer rather than its worst single step is the idea §4 formalizes.

```python
def triangle(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count                    # n(n-1)/2  ->  Theta(n^2)

def halvings(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps                    # floor(log2 n)  ->  Theta(log n)

def longest_window(xs, limit):
    """Length of the longest run of consecutive non-negative xs with sum <= limit."""
    best = left = total = 0
    for right, x in enumerate(xs):
        total += x
        while total > limit:        # left advances at most len(xs) times overall
            total -= xs[left]
            left += 1
        best = max(best, right - left + 1)
    return best                     # Theta(n)

print(triangle(10), halvings(1024), longest_window([2, 1, 3, 1, 1, 4], 5))  # 45 10 3
```

**Hidden costs in one line of Python.** Many "linear" solutions are quadratic because a single call hides a loop:

| Operation (CPython) | Cost |
|---|---|
| `x in some_list`, `lst.index(x)`, `lst.remove(x)` | $O(n)$ |
| `lst.pop(0)`, `lst.insert(0, x)` | $O(n)$ — use `collections.deque` |
| `lst[a:b]`, `lst.copy()`, `lst + other` | $O(\text{length copied})$ |
| `s += t` on strings inside a loop | may copy the whole string each time — build a list and `''.join` it |
| `x in some_set`, `d[key]` | $O(1)$ on average, $O(n)$ in the worst case |
| `sorted(xs)`, `xs.sort()` | $O(n \log n)$ |
| `heapq.heappush`, `heapq.heappop` | $O(\log n)$ |
| `lst.append(x)`, `lst.pop()` | $O(1)$ amortized (§4) |

### 3. Recurrences: the recursion tree and the master method

A recursive function's cost is described by a **recurrence**: the cost for size $n$ in terms of the cost of its recursive calls plus the work done outside them. The universal way to solve one is the **recursion tree**: draw one node per call, write the non-recursive work in each node, add up each level, then add up the levels.

For divide-and-conquer with equal-sized pieces, the tree has a regular shape. Suppose each call on size $n$ makes $a$ recursive calls on size $n/b$ and does $O(n^d)$ work to split and combine, which in symbols is

$$T(n) = a\,T(n/b) + O(n^d)$$

Level $j$ of the tree has $a^j$ calls, each on a piece of size $n/b^j$, so the work on that level is $a^j \cdot c\,(n/b^j)^d$, which rearranges into a form that shows the whole analysis:

$$\text{work at level } j = c\,n^d \left(\frac{a}{b^d}\right)^j$$

So the level totals form a geometric series with ratio $r = a/b^d$ over $\log_b n + 1$ levels, and a geometric series is dominated by its largest term ([[02-foundations/engineering-math|0.5 §5]]). That gives the **master method's three cases, in words**:

1. **$a < b^d$ — work shrinks level by level.** The root dominates: $T(n) = \Theta(n^d)$. Splitting is cheap compared to the top-level combine.
2. **$a = b^d$ — every level does the same work.** Multiply one level by the number of levels: $T(n) = \Theta(n^d \log n)$.
3. **$a > b^d$ — work grows toward the leaves.** The leaves dominate; there are $a^{\log_b n} = n^{\log_b a}$ of them: $T(n) = \Theta(n^{\log_b a})$.

The idea to remember is the tug-of-war: $a$ is the rate at which subproblems multiply, $b^d$ is the rate at which the work per subproblem shrinks.

> [!example] Worked example · 계산 예제
> **$T(n) = 2T(n/2) + n$** (merge sort's shape). Here $a = 2$, $b = 2$, $d = 1$, so $a = b^d$: case 2, $\Theta(n \log n)$. From the tree directly: level $j$ has $2^j$ pieces of size $n/2^j$, each costing $n/2^j$, so every level costs $n$; there are $\log_2 n + 1$ levels, so the total is $n(\log_2 n + 1)$. Check with $n = 8$: levels cost $8, 8, 8, 8$ — four levels, total 32, and $8 \cdot (3 + 1) = 32$.
>
> **$T(n) = T(n/2) + 1$** (binary search's shape). Here $a = 1$, $b = 2$, $d = 0$, so $a = b^d = 1$: case 2 again, $\Theta(n^0 \log n) = \Theta(\log n)$. The tree is a single path — one call per level, constant work each, $\log_2 n$ levels.
>
> **The same shapes with one change.** $T(n) = 2T(n/2) + 1$ has $a = 2 > b^d = 1$: case 3, $\Theta(n^{\log_2 2}) = \Theta(n)$. This is exactly the mistake of calling a recursive helper twice when once would do (§5).

You can check a recurrence numerically before trusting the algebra:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def T_merge(n):                     # T(n) = 2 T(n/2) + n,  T(1) = 1
    return 1 if n <= 1 else 2 * T_merge(n // 2) + n

@lru_cache(maxsize=None)
def T_search(n):                    # T(n) = T(n/2) + 1,  T(1) = 1
    return 1 if n <= 1 else T_search(n // 2) + 1

for k in (4, 10, 20):
    n = 2 ** k
    print(n, T_merge(n) / (n * (k + 1)), T_search(n) - k)   # prints 1.0 and 1 each time
```

**When the master method does not apply**, go back to the tree or unroll the recurrence by hand:

- **Subtract-one recurrences.** $T(n) = T(n-1) + n$ sums to $n + (n-1) + \dots + 1 = \Theta(n^2)$ — quicksort with a bad pivot, selection sort. $T(n) = 2T(n-1) + 1$ doubles at each step and gives $\Theta(2^n)$.
- **Overlapping calls.** Naive Fibonacci, $T(n) = T(n-1) + T(n-2) + 1$, grows like the Fibonacci numbers themselves, $\Theta(\varphi^n)$ with $\varphi \approx 1.618$. Memoization (§5) removes the overlap.
- **Unequal pieces**, such as a split into $n/3$ and $2n/3$: draw the tree; every level still costs at most $n$, and the deepest path has $\log_{3/2} n$ levels, so $\Theta(n \log n)$.

### 4. Amortized cost: why `append` is O(1)

**Amortized cost** is the total cost of a sequence of $n$ operations, divided by $n$, in the worst case over sequences. It involves no probability — it is a worst-case guarantee on the *total*, not on each step.

**Dynamic arrays** are the example every interview expects. An array has a fixed capacity. When `append` finds it full, it allocates a larger block and copies every element — a single $\Theta(n)$ step. How the capacity grows decides everything.

- **Grow by a factor (doubling).** Starting from capacity 1, $n$ appends trigger copies of $1, 2, 4, \dots, 2^k$ elements, where $2^k < n$. The total number of copies is below $2n$, because the geometric sum is less than twice its largest term:

$$1 + 2 + 4 + \cdots + 2^k = 2^{k+1} - 1 < 2n$$

  Add the $n$ writes themselves and $n$ appends cost fewer than $3n$ element operations: **$O(1)$ amortized per append**. Any growth factor $g > 1$ works — the total copies are about $n/(g-1)$ — only the constant changes.
- **Grow by a constant $k$.** Copies happen at sizes $k, 2k, 3k, \dots$, so the total is about $k(1 + 2 + \dots + n/k) \approx n^2/(2k)$: **$\Theta(n^2)$ total, $\Theta(n)$ per append**. A larger $k$ only divides the constant.

A second way to see it, useful when asked to *explain* rather than sum: charge each append 3 units. One pays for writing the element; two are saved. By the time the array of capacity $m$ is full again, the $m/2$ elements added since the last resize have saved $m$ units, which is exactly what copying $m$ elements costs. The savings never go negative, so 3 per append always suffices.

Shrinking needs the same care: halve the capacity only when the array is a quarter full, not half full. Otherwise alternating append and pop at the boundary resizes every time.

```python
class DynamicArray:
    """Append-only array that counts the element copies its resizes cause."""
    def __init__(self, grow):
        self.grow = grow              # old capacity -> new capacity
        self.cap, self.n = 1, 0
        self.data = [None]
        self.copies = 0

    def append(self, x):
        if self.n == self.cap:        # full: the one expensive step
            bigger = [None] * self.grow(self.cap)
            for i in range(self.n):
                bigger[i] = self.data[i]
            self.copies += self.n
            self.data, self.cap = bigger, len(bigger)
        self.data[self.n] = x
        self.n += 1

double, plus16 = DynamicArray(lambda c: 2 * c), DynamicArray(lambda c: c + 16)
for i in range(4096):
    double.append(i)
    plus16.append(i)
print(double.copies, plus16.copies)   # 4095 522496
```

**What real containers do.**

- **Python `list`** is a dynamic array of references. CPython over-allocates by roughly one eighth plus a small constant (an implementation detail, visible with `sys.getsizeof`), so `append` and `pop()` are $O(1)$ amortized, while `pop(0)` and `insert(0, x)` shift everything and are $O(n)$.
- **C++ `std::vector`**: the standard requires `push_back` to be amortized constant time, which forces geometric growth; the factor is implementation-defined (2 in libstdc++ and libc++, 1.5 in MSVC). A reallocation invalidates every iterator, pointer and reference into the vector — a classic crash when you hold `&v[0]` across a `push_back`.

```python
import sys

xs, last, resizes = [], sys.getsizeof([]), []
for i in range(300):
    xs.append(i)
    size = sys.getsizeof(xs)
    if size != last:
        resizes.append(len(xs))       # the append that triggered a reallocation
        last = size
print(resizes)                        # gaps between resizes keep growing
```

**Amortized is not worst-case per operation.** On a robot this distinction is real. A control callback that appends to a vector at 1 kHz is fast on average, but the one call that reallocates can blow the deadline. In real-time code, call `reserve(n)` (C++) or preallocate (`[0.0] * n`, a NumPy array) before the loop starts. Where callbacks run and what a missed deadline does to the rest of the system is [[04-robotics/ros2/qos-executors-time|25.5 QoS, Executors and Time §8]].

### 5. Recursion done right

A correct recursive function needs three things.

1. **A base case** that returns without recursing — and every valid input must eventually reach it.
2. **Progress**: each recursive call is on a strictly smaller instance (smaller $n$, shorter list, fewer remaining choices).
3. **Trust the call.** When writing the recursive case, assume the call on the smaller input already returns the right answer, and only ask: how do I build my answer from it? This is proof by induction — the base case is the base step, and trusting the call is the inductive hypothesis. Tracing ten levels of calls in your head is the wrong way to convince yourself.

**Space counts.** Each active call holds a stack frame, so a recursion of depth $D$ uses $\Theta(D)$ extra space even if it allocates nothing. Say this in the space analysis.

```python
def power(x, n):
    """x ** n for an integer n >= 0 with O(log n) multiplications."""
    if n == 0:                        # base case
        return 1
    half = power(x, n // 2)           # progress: n halves; trust the call
    return half * half * (x if n % 2 else 1)

print(power(3, 13), 3 ** 13)          # 1594323 1594323
```

The recurrence is $T(n) = T(n/2) + 1$, so $\Theta(\log n)$ time and $\Theta(\log n)$ stack. **Pitfall:** writing `power(x, n // 2) * power(x, n // 2)` computes the same thing twice, which gives $T(n) = 2T(n/2) + 1 = \Theta(n)$ — the correct answer, exponentially more slowly.

**Memoization.** When recursive calls overlap — the same arguments are requested again and again — store each result the first time and look it up afterwards. The cost becomes (number of distinct arguments) × (work per call, not counting the sub-calls). Naive Fibonacci makes $2F(n+1) - 1$ calls, about 2.7 million for $n = 30$; the memoized version makes $n + 1$ distinct computations.

Two ways to write it:

- **`functools.lru_cache(maxsize=None)`** (or `functools.cache` in Python 3.9+) as a decorator. The arguments must be hashable, so pass tuples, not lists. The cache persists between calls — clear it with `.cache_clear()` if a test harness reuses the function on unrelated inputs.
- **An explicit dictionary inside a wrapper.** The public function creates the cache and defines a nested helper that does the recursion. Nothing leaks between calls, the key can be any tuple you build, and the pattern translates directly to C++ (an `unordered_map` or a 2-D `vector` passed by reference). Never use a mutable default argument such as `memo={}` as the cache: it is shared by every call of the function.

```python
from functools import lru_cache

calls = 0
def fib_naive(n):
    global calls
    calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def count_paths(grid):
    """Right/down paths from top-left to bottom-right; grid cells with 1 are blocked."""
    rows, cols, memo = len(grid), len(grid[0]), {}
    def helper(r, c):
        if r >= rows or c >= cols or grid[r][c]:
            return 0
        if (r, c) == (rows - 1, cols - 1):
            return 1
        if (r, c) not in memo:
            memo[(r, c)] = helper(r + 1, c) + helper(r, c + 1)
        return memo[(r, c)]
    return helper(0, 0)

print(fib_naive(20), calls, fib(90))                  # 6765 21891 2880067194370816120
open_row, blocked_middle = [0, 0, 0], [0, 1, 0]
print(count_paths([open_row, blocked_middle, open_row]))  # 2
```

`count_paths` has $rows \times cols$ distinct states and does $O(1)$ work in each, so it is $\Theta(rows \cdot cols)$ time and space. It is also a small dynamic program; turning it into a table filled in loop order is the subject of the DP page, and the same "reuse the value of the successor state" idea is the Bellman backup in [[02-foundations/rl-basics|7. RL Basics §3]].

**Recursion depth in Python.** CPython stops runaway recursion with a limit of 1000 frames by default (`sys.getrecursionlimit()`), raising `RecursionError`. This bites memoized code too: calling `fib(5000)` on an empty cache recurses 5000 deep and fails, and `count_paths` on a 1000 × 1000 occupancy grid recurses about 2000 deep. `sys.setrecursionlimit` raises the limit, but setting it far above what the interpreter's C stack can hold crashes the process instead of raising an exception. The robust fixes are: fill the cache bottom-up in a loop, or replace the call stack with an explicit list used as a stack. C++ has no limit check at all; exceeding the thread's stack (commonly 8 MB on Linux, 1 MB on Windows) is a segmentation fault.

```python
def fib_iter(n):                      # bottom-up: Theta(n) time, Theta(1) space, no recursion
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(len(str(fib_iter(5000))))       # 1045 digits, no RecursionError
```

### 6. Backtracking: choose, explore, un-choose

**Backtracking** builds a solution one decision at a time, and abandons a partial solution as soon as it cannot be completed. The shape of every backtracking function is the same:

```text
def backtrack(state):
    if state is a complete solution: record a copy; return
    for each choice allowed from state:
        if choice cannot lead to a solution: skip it      # pruning
        make the choice                                    # choose
        backtrack(new state)                               # explore
        undo the choice                                    # un-choose
```

Before coding, answer four questions: *What is one decision? What are the options for it? How is a choice undone? When is a solution complete?* The calls form a **decision tree**: the root is the empty partial solution, each edge is one choice, each leaf is a complete candidate.

- **Subsets.** One decision per element: leave it out, or take it. The tree has $2^n$ leaves; copying each finished subset costs $O(n)$, so $\Theta(n\,2^n)$ time — unavoidable, since the output itself has that size — and $O(n)$ extra space for the path and the stack.
- **Permutations.** Decision $i$ is which unused element goes in position $i$. There are $n!$ leaves and fewer than $e \cdot n!$ nodes in total, so $\Theta(n \cdot n!)$ time including the copies.
- **N-Queens.** Place $n$ queens on an $n \times n$ board so that none attack each other. Choosing one queen *per row* builds the row constraint into the decision; keeping sets of used columns and diagonals makes each safety check $O(1)$. Squares on the same "\\" diagonal share $r - c$, and squares on the same "/" diagonal share $r + c$.

```python
def subsets(nums):
    out, path = [], []
    def backtrack(i):
        if i == len(nums):
            out.append(path[:])       # copy: path keeps changing after this
            return
        backtrack(i + 1)              # decision: leave nums[i] out
        path.append(nums[i])          # choose
        backtrack(i + 1)              # explore
        path.pop()                    # un-choose
    backtrack(0)
    return out

def permutations(nums):
    out, path, used = [], [], [False] * len(nums)
    def backtrack():
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True; path.append(x)       # choose
                backtrack()                          # explore
                path.pop(); used[i] = False          # un-choose
    backtrack()
    return out

def n_queens(n):
    """Number of ways to place n non-attacking queens on an n x n board."""
    cols, diag, anti = set(), set(), set()
    def place(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue                             # prune: square is attacked
            cols.add(c); diag.add(r - c); anti.add(r + c)
            total += place(r + 1)
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
        return total
    return place(0)

print(len(subsets([1, 2, 3])), len(permutations([1, 2, 3])), n_queens(4), n_queens(8))  # 8 6 2 92
```

**Pruning** is where backtracking earns its keep: a test at an internal node removes the whole subtree below it. The strongest prunes come from ordering. If the values are sorted, the first value that overshoots a target proves that every later value overshoots too, so the loop can `break` rather than `continue`. Sorting also lets you skip equal values at the same depth, which removes duplicate answers without a set.

```python
def subsets_with_sum(nums, target):
    """All distinct multisets drawn from positive nums that sum to target."""
    nums, out, path = sorted(nums), [], []
    def backtrack(start, remaining):
        if remaining == 0:
            out.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break                                # prune: later values are larger still
            if i > start and nums[i] == nums[i - 1]:
                continue                             # same value at the same depth: duplicate
            path.append(nums[i])
            backtrack(i + 1, remaining - nums[i])
            path.pop()
    backtrack(0, target)
    return out

print(subsets_with_sum([3, 1, 4, 1, 5, 2], 6))  # four lists: [1, 1, 4] [1, 2, 3] [1, 5] [2, 4]
```

**Complexity of a search tree.** With branching factor at most $b$ and depth at most $d$ there are at most $b^d$ leaves, and the running time is (number of nodes visited) × (work per node). Pruning rarely improves the worst-case bound — N-Queens with column sets is still bounded only by $n!$ — but it changes what is practical by orders of magnitude, and the honest interview answer says both: "worst case $O(n!)$; in practice the diagonal checks cut most branches early."

**Interview pitfalls.** Appending `path` instead of a copy (every recorded answer ends up as the same, finally empty, list). Forgetting the un-choose step, so state from one branch leaks into its siblings. Checking validity only at the leaves, which turns backtracking back into brute force. Using `continue` where sorted order allows `break`.

In robotics, backtracking is the right tool for small, hard combinatorial choices — the order in which to place a handful of blocks when each needs support from those already placed, or which grasp to use on each of a few objects when grasps must not collide. Past roughly twenty decisions the tree is too large, and the tools become dynamic programming, heuristic graph search, or a constraint solver; the task-level view is [[04-robotics/planning-decision-making|Planning & Decision-Making §7]].

### 7. How to talk through complexity in an interview

A complete complexity answer has five parts, and saying them in order sounds organized even when you are thinking on your feet.

1. **Name the sizes.** "Let $n$ be the number of points and $k$ the window length." Never leave $n$ undefined, and never merge two independent sizes into one.
2. **Name the dominant operation and count it.** "Each point is pushed and popped from the heap once, and each heap operation is $O(\log k)$."
3. **State the time bound with its qualifier:** worst case, average case (hash tables), expected (randomized pivots), or amortized (dynamic arrays, the sliding-window pointer).
4. **State the space:** auxiliary structures, the recursion stack, and the output if it is large (all subsets alone take $\Theta(n\,2^n)$).
5. **Connect to the constraints and offer the trade-off.** "With $n \le 10^5$, the $O(n^2)$ brute force is about $10^{10}$ steps, too slow; sorting first gives $O(n \log n)$ at the cost of $O(n)$ extra memory."

> [!example] Worked example · 계산 예제
> **Question:** given $n$ 2-D lidar points, report every pair closer than $r$.
>
> **Answer, spoken:** "Let $n$ be the number of points and $K$ the number of pairs reported. Brute force compares all $n(n-1)/2$ pairs: $\Theta(n^2)$ time, $O(1)$ extra space besides the output. Better: hash each point into a grid cell of side $r$; any close pair lies in the same or an adjacent cell, so each point checks 9 cells. Building the grid is $O(n)$ expected, since dictionary operations are $O(1)$ on average, and the search is $O(n + K)$ as long as no cell holds a huge number of points. The worst case is still $\Theta(n^2)$ — if all points lie within $r$ of each other, $K$ itself is $\Theta(n^2)$, so no algorithm can do better. Extra space is $O(n)$ for the grid."
>
> That answer names both sizes, states the case, explains the average-case assumption, and says why the worst case cannot be improved. The same reasoning is why a sampling planner that scans all tree nodes for the nearest neighbour costs $O(n)$ per sample and $O(n^2)$ over $n$ samples, and why real planners use a spatial index ([[04-robotics/modern-robotics/ch10-motion-planning|MR Ch.10 — Motion Planning]]).

**Statements that lose points:**

- "Hash map lookup is $O(1)$." — Average $O(1)$ with a reasonable hash; worst case $O(n)$.
- "Recursion uses no extra space." — It uses $O(\text{depth})$ stack.
- "Two nested loops, so $O(n^2)$." — Not when the inner pointer never moves backwards (§2, example 3).
- "Sorting is $O(n \log n)$." — For comparison sorts; counting sort on small integer keys is $O(n + \text{range})$.
- "It's $O(n)$" for a graph algorithm. — Say $O(V + E)$; a dense graph has $E = \Theta(V^2)$.
- Forgetting the cost of building the answer: copying paths, slicing strings, joining output.

### Self-check

1. A function takes 0.8 s at $n = 10^5$ and 3.3 s at $n = 2 \times 10^5$. What growth rate does this suggest, and how long do you predict at $n = 4 \times 10^5$?
2. Give a Θ bound for: `for i in range(1, n): j = 1; while j < i: j *= 2`.
3. Solve with the master method: (a) $T(n) = 4T(n/2) + n^2$; (b) $T(n) = 3T(n/2) + n$; (c) $T(n) = 2T(n/2) + n^2$.
4. A dynamic array grows by 1000 slots whenever it is full. Roughly how many element copies do $10^6$ appends cause, and how many would doubling cause?
5. `fib` is decorated with `@lru_cache(maxsize=None)`. Why does calling `fib(5000)` on a fresh interpreter raise `RecursionError`, and what are two fixes?
6. In `subsets`, someone writes `out.append(path)` instead of `out.append(path[:])`. What does `subsets([1, 2])` return, and why?
7. For N-Queens, why does placing exactly one queen per row shrink the search space from $\binom{n^2}{n}$ placements to at most $n^n$, and what further bound do the column sets give?

> [!tip]- Answers
> 1. The ratio is $3.3/0.8 \approx 4.1$, and $\log_2 4.1 \approx 2$: quadratic. Doubling again multiplies by about 4, so about 13 s.
> 2. The inner loop runs about $\log_2 i$ times, so the total is $\sum_{i<n} \log_2 i = \log_2 (n-1)! = \Theta(n \log n)$. (Upper bound: each term is at most $\log_2 n$. Lower bound: the top half of the terms are each at least $\log_2(n/2)$.)
> 3. (a) $a = 4 = b^d = 2^2$: case 2, $\Theta(n^2 \log n)$. (b) $a = 3 > b^d = 2$: case 3, $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$ — Karatsuba multiplication's bound. (c) $a = 2 < b^d = 4$: case 1, $\Theta(n^2)$.
> 4. Copies happen at sizes 1000, 2000, …, up to $10^6$, totalling about $1000 \cdot (1 + 2 + \dots + 1000) \approx 5 \times 10^8$. Doubling gives fewer than $2 \times 10^6$ — about 250 times fewer.
> 5. On an empty cache, `fib(5000)` must call `fib(4999)` before anything is stored, which calls `fib(4998)`, and so on: the stack reaches depth 5000, above the default limit of 1000. Fixes: compute bottom-up in a loop (or warm the cache by calling `fib(i)` for increasing `i`), or use an explicit stack. Raising `sys.setrecursionlimit` works only while the C stack holds out.
> 6. A list of four empty lists, `[ [], [], [], [] ]`. Every entry is a reference to the same list object; each `append` is later undone by `pop`, so after the search ends that single list is empty and all four entries show it.
> 7. Two queens in the same row attack, so any valid placement has exactly one queen per row; choosing a column for each of $n$ rows gives $n^n$ candidates. Two queens in the same column also attack, so the columns must all differ — a permutation — giving at most $n!$ leaves. The diagonal sets prune further, but no simple closed form is known for the nodes actually visited.

### Sources

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — the chapters on asymptotic notation, divide-and-conquer recurrences and the master theorem, and amortized analysis.
- T. Roughgarden, *Algorithms Illuminated, Part 1: The Basics*, Soundlikeyourself Publishing, 2017 — asymptotic notation and the $a$ versus $b^d$ form of the master method used in §3.
- A. S. Kulikov, P. A. Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — chapters 1–2: running time, big-O rules, recursion trees, and design techniques.
- D. E. Knuth, "Big Omicron and big Omega and big Theta," *ACM SIGACT News* 8(2), 1976, pp. 18–24. DOI: 10.1145/1008328.1008329 — the paper that fixed the modern meanings of O, Ω and Θ.
- J. L. Bentley, D. Haken, J. B. Saxe, "A general method for solving divide-and-conquer recurrences," *ACM SIGACT News* 12(3), 1980 — the origin of the master theorem.
- R. E. Tarjan, "Amortized computational complexity," *SIAM Journal on Algebraic and Discrete Methods* 6(2), 1985. DOI: 10.1137/0606031 — amortized analysis named and systematized.
- S. W. Golomb, L. D. Baumert, "Backtrack programming," *Journal of the ACM* 12(4), 1965 — the early systematic treatment of backtracking search.

## 한국어

*알고리즘 트랙의 첫 페이지다. 뒤의 모든 페이지가 복잡도를 말하고 독자가 그것을 확인할 수 있다고 전제한다. 그 확인하는 능력을 여기서 만든다.*

코딩 인터뷰는 거의 언제나 "시간·공간 복잡도는?"으로 끝나고, 연구실 인터뷰는 "실제 데이터에서는 왜 느린가?"를 덧붙인다. 두 질문의 답은 같다. 가장 지배적인 연산이 입력 크기의 함수로 몇 번 실행되는지 세고, 어떤 경우(case)를 세었는지 말하는 것이다. 이 페이지는 그 어휘(O, Ω, Θ), 세는 도구 세 가지(반복문, 점화식, 분할상환), 그리고 "전부 시도하기"를 올바른 코드로 바꾸는 탐색 패턴 하나 — 백트래킹 — 를 준다.

> [!note] 처음이라면 · First pass
> §1, §2, §7을 먼저 읽어라. 모든 인터뷰에서 소리 내어 말하게 될 내용이다. §3과 §4는 답에 재귀나 늘어나는 배열이 처음 등장할 때 필요하다. §5와 §6은 코드 패턴이다 — 빈 파일에서 연습하라.

### 1. 인터뷰에서 말하는 "효율적"의 뜻

인터뷰에서 "효율적"이란 합의된 세 가지 단순화를 뜻한다.

- **입력 크기 $n$.** 실행 시간은 입력이 얼마나 큰지 — 점의 개수, 문자열 길이, 정점과 간선의 수 — 의 함수다. 크기가 여럿이면 따로 둔다. 그래프 알고리즘은 $O(n)$이 아니라 $O(V + E)$다.
- **따로 말하지 않으면 최악의 경우.** 각 $n$마다 그 크기에서 가장 느린 입력을 본다. 최악 경우 상한은 보장이다: 그 크기의 어떤 입력도 그보다 느리지 않다. 평균 경우, 기대값(무작위 알고리즘), 분할상환(§4)은 다른 약속이므로 쓸 때 이름을 붙여야 한다.
- **상수와 낮은 차수 항은 버린다.** $3n^2 + 40n + 7$은 $n^2$이 된다. 상수가 중요하지 않아서가 아니다 — 로봇에서 10배 상수는 중요하다. 상수는 기계·언어·컴파일러에 따라 달라지지만 증가율은 알고리즘의 성질이기 때문이다. $n$이 충분히 크면 증가율이 낮은 쪽이 어떤 상수 배도 이긴다.

**두 배 점검.** 증가율은 검증 가능한 예측을 준다: $n$을 두 배로 늘리면 실행 시간이 어떻게 되는가. $n$과 $2n$에서 시간을 재면 그 비율이 복잡도 부류를 알려 준다.

| 증가율 | $n$이 두 배일 때 시간 |
|---|---|
| $\Theta(1)$ | 그대로 |
| $\Theta(\log n)$ | 일정한 양만큼 증가 |
| $\Theta(n)$ | ×2 |
| $\Theta(n \log n)$ | ×2보다 조금 더 |
| $\Theta(n^2)$ | ×4 |
| $\Theta(n^3)$ | ×8 |
| $\Theta(2^n)$ | 제곱 — $n$이 1만 늘어도 이미 ×2 |

다항 증가 $n^k$에서는 $\log_2(\text{비율}) \approx k$다. 남이 쓴 코드가 몰래 이차인지 알아내는 가장 빠른 방법이다.

```python
import time

def doubling_ratios(f, sizes):
    """Time f(n) for each size; return the ratios t(next) / t(previous)."""
    times = []
    for n in sizes:
        start = time.perf_counter()
        f(n)
        times.append(time.perf_counter() - start)
    return [later / earlier for earlier, later in zip(times, times[1:])]

def all_pairs(n):                  # deliberately quadratic
    return sum(1 for i in range(n) for j in range(n))

print(doubling_ratios(all_pairs, [800, 1600, 3200]))  # each ratio roughly 4 (timing is noisy)
```

**시간 예산 (대략적인 경험칙이지 법칙이 아니다).** 컴파일 언어가 초당 $10^8$ 정도의 단순 연산을 한다고 가정하자. 그러면 약 1초 안에 끝나는 가장 큰 입력은 대략 다음과 같다.

| 복잡도 | ~1초에 가능한 최대 $n$ (컴파일 언어) |
|---|---|
| $O(n!)$ | ~11 |
| $O(2^n)$, $O(n\,2^n)$ | ~25, ~20 |
| $O(n^3)$ | 수백 |
| $O(n^2)$ | ~$10^4$ |
| $O(n \log n)$ | ~$10^6$~$10^7$ |
| $O(n)$ | ~$10^8$ |

현실적인 본문(인덱싱, 딕셔너리 조회, 함수 호출)을 가진 순수 Python 반복문은 대략 10~100배 느리다 — 덧셈 하나만 하는 `for` 루프조차 요즘 노트북에서 초당 약 $2 \times 10^7$회에 그친다. 그러니 위 한계를 그만큼 나눠라. 컴파일된 코드 안에서 도는 NumPy 연산은 컴파일 언어 쪽에 가깝다. 인터뷰에서는 표를 거꾸로 읽는다. "$n \le 10^5$"라는 제약은 $O(n^2)$은 통과하지 못하고 $O(n \log n)$은 통과한다는 신호다.

### 2. Big-O, Ω, Θ의 정확한 뜻과 반복문 읽기

세 기호는 결국의 증가에 대한 진술이고, 각각 고를 수 있는 상수가 붙는다. $f$가 결국 $g$의 상수 배 이하일 때 $f = O(g)$라고 쓴다. 직관이 흔들릴 때 돌아갈 곳이 정의이기 때문에 그대로 적어 둔다:

$$f(n) = O(g(n)) \iff \exists\, c > 0,\ n_0 \text{ such that } 0 \le f(n) \le c\,g(n) \text{ for all } n \ge n_0$$

- $f = \Omega(g)$: 같은 식에서 $f(n) \ge c\,g(n)$ — $g$가 결국의 하한이다.
- $f = \Theta(g)$: 둘 다 — 큰 $n$에서 $c_1 g(n) \le f(n) \le c_2 g(n)$. 이것이 딱 맞는(tight) 상한·하한이고, 대화에서 "빅오"라고 할 때 사람들이 보통 뜻하는 것이 이것이다.
- 상수 $c$와 $n_0$은 $n$에 의존하면 안 된다. 이 규칙 하나 때문에 "$n^2 = O(n)$"이 거짓이 된다. 그러려면 $c \ge n$이어야 하기 때문이다.

예: $3n^2 + 10n + 5 = \Theta(n^2)$. $n \ge 1$이면 $3n^2 \le 3n^2 + 10n + 5 \le 3n^2 + 10n^2 + 5n^2 = 18n^2$이므로 $c_1 = 3$, $c_2 = 18$, $n_0 = 1$이면 된다.

인터뷰어가 파고드는 구분 두 가지:

- **상한·하한 대 경우.** O/Ω/Θ는 함수를 묘사하고, 최악/최선/평균 경우는 *어떤* 함수를 묘사하는지를 말한다. 삽입 정렬의 최악 경우 시간은 $\Theta(n^2)$, 최선 경우 시간은 $\Theta(n)$이다. "삽입 정렬은 $O(n^2)$"는 모든 입력에 참이지만, "삽입 정렬은 $\Theta(n^2)$"는 모든 입력에 대한 주장으로는 거짓이다.
- **로그의 밑은 상관없고, 지수의 밑은 상관있다.** $\log_2 n$과 $\log_{10} n$은 상수 배만 다르므로 $O(\log n)$으로 쓴다. 하지만 $4^n = (2^n)^2$은 $O(2^n)$이 아니다.

**반복문 읽기.** 인터뷰 코드는 대부분 세 규칙으로 해결된다.

1. **이어진 블록은 더하고**, 가장 큰 항이 남는다: $O(n) + O(n \log n) = O(n \log n)$. 크기가 둘이면 둘 다 남긴다: $O(n + m)$.
2. **중첩 반복문은 곱한다** — 안쪽 횟수가 바깥 변수에 의존하지 않을 때. 의존하면 최댓값끼리 곱하지 말고 안쪽 횟수를 **더한다**.
3. **반복 변수에 상수를 곱하거나 나누면** 루프는 $\Theta(\log n)$번 돈다. $k$번 반으로 나누면 $n/2^k$가 $k = \log_2 n$에서 1에 닿기 때문이다.

> [!example] 계산 예제 · Worked example
> **1. 삼각형 이중 루프.** `for i in range(n): for j in range(i + 1, n)`에서 안쪽 루프는 $n-1, n-2, \dots, 0$번 돈다. 합은 $n(n-1)/2$이므로 이 쌍 루프는 $\Theta(n^2)$이다 — 일은 절반이지만 정사각형 전체와 같은 부류다.
>
> **2. 반으로 나누기.** `while n > 1: n //= 2`는 $\lfloor \log_2 n \rfloor$번 돈다. $n = 1024$면 10번, $n = 1000$이면 9번이다. 이것을 $n$개 원소에 대한 루프 안에 넣으면 전체는 $\Theta(n \log n)$이다.
>
> **3. 선형인 중첩 루프.** 슬라이딩 윈도(아래 코드)에서 안쪽 `while`은 `right` 하나에 대해 여러 번 돌 수 있어서 "중첩이니 $n^2$"이라고 말하고 싶어진다. 하지만 `left`는 앞으로만 움직이고 $n$을 넘지 않으므로, 실행 전체에 걸쳐 안쪽 본문은 모두 합해 최대 $n$번 실행된다. 바깥 $n$ + 안쪽 $n$ = $\Theta(n)$. 포인터 한 번의 최악 이동이 아니라 포인터가 한 일의 총량을 세는 것 — 이것을 §4가 형식화한다.

```python
def triangle(n):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            count += 1
    return count                    # n(n-1)/2  ->  Theta(n^2)

def halvings(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps                    # floor(log2 n)  ->  Theta(log n)

def longest_window(xs, limit):
    """Length of the longest run of consecutive non-negative xs with sum <= limit."""
    best = left = total = 0
    for right, x in enumerate(xs):
        total += x
        while total > limit:        # left advances at most len(xs) times overall
            total -= xs[left]
            left += 1
        best = max(best, right - left + 1)
    return best                     # Theta(n)

print(triangle(10), halvings(1024), longest_window([2, 1, 3, 1, 1, 4], 5))  # 45 10 3
```

**Python 한 줄에 숨은 비용.** "선형" 풀이가 이차가 되는 흔한 이유는 호출 하나가 루프를 숨기고 있어서다.

| 연산 (CPython) | 비용 |
|---|---|
| `x in some_list`, `lst.index(x)`, `lst.remove(x)` | $O(n)$ |
| `lst.pop(0)`, `lst.insert(0, x)` | $O(n)$ — `collections.deque`를 써라 |
| `lst[a:b]`, `lst.copy()`, `lst + other` | $O(\text{복사된 길이})$ |
| 루프 안에서 문자열 `s += t` | 매번 문자열 전체를 복사할 수 있다 — 리스트에 모아 `''.join` |
| `x in some_set`, `d[key]` | 평균 $O(1)$, 최악 $O(n)$ |
| `sorted(xs)`, `xs.sort()` | $O(n \log n)$ |
| `heapq.heappush`, `heapq.heappop` | $O(\log n)$ |
| `lst.append(x)`, `lst.pop()` | 분할상환 $O(1)$ (§4) |

### 3. 점화식: 재귀 트리와 마스터 방법

재귀 함수의 비용은 점화식(**recurrence**)으로 표현된다. 크기 $n$의 비용을, 재귀 호출들의 비용과 그 바깥에서 하는 일의 합으로 쓴 것이다. 점화식을 푸는 만능 방법은 재귀 트리(**recursion tree**)다. 호출마다 노드를 하나 그리고, 각 노드에 재귀가 아닌 일의 양을 적고, 층마다 더한 뒤 층들을 더한다.

크기가 같은 조각으로 나누는 분할정복에서는 트리 모양이 규칙적이다. 크기 $n$의 호출이 크기 $n/b$의 재귀 호출을 $a$번 하고, 나누고 합치는 데 $O(n^d)$ 일을 한다고 하자. 기호로 쓰면 다음과 같다:

$$T(n) = a\,T(n/b) + O(n^d)$$

트리의 $j$층에는 호출이 $a^j$개 있고, 각각 크기 $n/b^j$ 조각을 다루므로 그 층의 일은 $a^j \cdot c\,(n/b^j)^d$이다. 따라서:

$$\text{work at level } j = c\,n^d \left(\frac{a}{b^d}\right)^j$$

그래서 층별 합은 $\log_b n + 1$개 층에 걸친 공비 $r = a/b^d$의 기하급수가 되고, 기하급수는 가장 큰 항이 지배한다([[02-foundations/engineering-math|0.5 §5]]). 이것을 말로 옮기면 **마스터 방법의 세 경우**가 된다:

1. **$a < b^d$ — 층을 내려갈수록 일이 줄어든다.** 뿌리가 지배한다: $T(n) = \Theta(n^d)$. 맨 위에서 합치는 일에 비해 나누는 것이 싸다.
2. **$a = b^d$ — 모든 층이 같은 양의 일을 한다.** 한 층의 일에 층 수를 곱한다: $T(n) = \Theta(n^d \log n)$.
3. **$a > b^d$ — 잎으로 갈수록 일이 늘어난다.** 잎이 지배하고, 잎은 $a^{\log_b n} = n^{\log_b a}$개다: $T(n) = \Theta(n^{\log_b a})$.

기억할 그림은 줄다리기다. $a$는 부분문제가 불어나는 속도, $b^d$는 부분문제 하나당 일이 줄어드는 속도다.

> [!example] 계산 예제 · Worked example
> **$T(n) = 2T(n/2) + n$** (병합 정렬의 모양). $a = 2$, $b = 2$, $d = 1$이므로 $a = b^d$: 경우 2, $\Theta(n \log n)$. 트리로 직접 보면: $j$층에 크기 $n/2^j$ 조각이 $2^j$개 있고 각각 $n/2^j$ 비용이므로 모든 층이 $n$이다. 층은 $\log_2 n + 1$개이므로 합은 $n(\log_2 n + 1)$. $n = 8$로 확인: 층 비용이 $8, 8, 8, 8$ — 네 층, 합 32, 그리고 $8 \cdot (3 + 1) = 32$.
>
> **$T(n) = T(n/2) + 1$** (이진 탐색의 모양). $a = 1$, $b = 2$, $d = 0$이므로 $a = b^d = 1$: 역시 경우 2, $\Theta(n^0 \log n) = \Theta(\log n)$. 트리는 한 줄짜리 경로다 — 층마다 호출 하나, 각각 상수 일, $\log_2 n$개 층.
>
> **한 곳만 바꾼 같은 모양.** $T(n) = 2T(n/2) + 1$은 $a = 2 > b^d = 1$: 경우 3, $\Theta(n^{\log_2 2}) = \Theta(n)$. 한 번이면 될 재귀 호출을 두 번 하는 실수가 정확히 이것이다(§5).

대수를 믿기 전에 점화식을 수치로 확인할 수 있다:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def T_merge(n):                     # T(n) = 2 T(n/2) + n,  T(1) = 1
    return 1 if n <= 1 else 2 * T_merge(n // 2) + n

@lru_cache(maxsize=None)
def T_search(n):                    # T(n) = T(n/2) + 1,  T(1) = 1
    return 1 if n <= 1 else T_search(n // 2) + 1

for k in (4, 10, 20):
    n = 2 ** k
    print(n, T_merge(n) / (n * (k + 1)), T_search(n) - k)   # prints 1.0 and 1 each time
```

**마스터 방법이 적용되지 않을 때:** 트리로 돌아가거나 점화식을 손으로 펼친다.

- **1씩 줄어드는 점화식.** $T(n) = T(n-1) + n$은 $n + (n-1) + \dots + 1 = \Theta(n^2)$ — 피벗이 나쁜 퀵정렬, 선택 정렬. $T(n) = 2T(n-1) + 1$은 단계마다 두 배가 되어 $\Theta(2^n)$.
- **겹치는 호출.** 순진한 피보나치 $T(n) = T(n-1) + T(n-2) + 1$은 피보나치 수 자체처럼 자라서 $\Theta(\varphi^n)$, $\varphi \approx 1.618$. 메모이제이션(§5)이 겹침을 없앤다.
- **크기가 다른 조각**, 예컨대 $n/3$과 $2n/3$으로 나누기: 트리를 그린다. 모든 층의 비용은 여전히 $n$ 이하이고 가장 깊은 경로가 $\log_{3/2} n$층이므로 $\Theta(n \log n)$.

### 4. 분할상환 비용: `append`가 O(1)인 이유

**분할상환 비용(amortized cost).** 연산 $n$개로 이루어진 수열의 총비용을 $n$으로 나눈 것이며, 수열에 대한 최악 경우로 잰다. 확률은 들어가지 않는다 — 각 단계가 아니라 *총합*에 대한 최악 경우 보장이다.

**동적 배열.** 모든 인터뷰가 기대하는 예가 이것이다. 배열에는 고정된 용량이 있다. `append`가 가득 찬 배열을 만나면 더 큰 블록을 할당하고 원소를 모두 복사한다 — 단 한 번에 $\Theta(n)$인 단계다. 용량을 어떻게 늘리느냐가 모든 것을 결정한다.

- **배수로 늘리기(두 배).** 용량 1에서 시작하면 $n$번의 append가 $1, 2, 4, \dots, 2^k$개 원소의 복사를 일으키고, $2^k < n$이다. 기하급수 합은 가장 큰 항의 두 배보다 작으므로 복사 총수는 $2n$ 미만이다:

$$1 + 2 + 4 + \cdots + 2^k = 2^{k+1} - 1 < 2n$$

  원소를 쓰는 $n$번을 더해도 $n$번의 append는 $3n$ 미만의 원소 연산이다: **append당 분할상환 $O(1)$**. 증가 배수 $g > 1$이면 무엇이든 된다 — 복사 총수가 약 $n/(g-1)$ — 상수만 달라진다.
- **상수 $k$씩 늘리기.** 복사가 크기 $k, 2k, 3k, \dots$에서 일어나므로 합은 약 $k(1 + 2 + \dots + n/k) \approx n^2/(2k)$: **총 $\Theta(n^2)$, append당 $\Theta(n)$**. $k$를 키워도 상수만 나눌 뿐이다.

합을 계산하기보다 *설명*하라는 요청을 받을 때 쓸 두 번째 관점: append마다 3단위를 청구한다. 1단위는 원소를 쓰는 데 쓰고 2단위는 저축한다. 용량 $m$인 배열이 다시 가득 찰 때까지, 지난 확장 이후 추가된 $m/2$개 원소가 $m$단위를 모았고, 이것이 원소 $m$개를 복사하는 비용과 정확히 같다. 저축이 음수가 되는 일이 없으므로 append당 3이면 언제나 충분하다.

줄이는 쪽도 같은 주의가 필요하다. 배열이 절반이 아니라 4분의 1만 찼을 때 용량을 반으로 줄인다. 그렇지 않으면 경계에서 append와 pop을 번갈아 할 때마다 크기 조정이 일어난다.

```python
class DynamicArray:
    """Append-only array that counts the element copies its resizes cause."""
    def __init__(self, grow):
        self.grow = grow              # old capacity -> new capacity
        self.cap, self.n = 1, 0
        self.data = [None]
        self.copies = 0

    def append(self, x):
        if self.n == self.cap:        # full: the one expensive step
            bigger = [None] * self.grow(self.cap)
            for i in range(self.n):
                bigger[i] = self.data[i]
            self.copies += self.n
            self.data, self.cap = bigger, len(bigger)
        self.data[self.n] = x
        self.n += 1

double, plus16 = DynamicArray(lambda c: 2 * c), DynamicArray(lambda c: c + 16)
for i in range(4096):
    double.append(i)
    plus16.append(i)
print(double.copies, plus16.copies)   # 4095 522496
```

**실제 컨테이너가 하는 일.**

- **Python `list`** 는 참조의 동적 배열이다. CPython은 대략 8분의 1에 작은 상수를 더해 여유 할당한다(구현 세부 사항이며 `sys.getsizeof`로 보인다). 그래서 `append`와 `pop()`은 분할상환 $O(1)$이고, 전부를 밀어야 하는 `pop(0)`과 `insert(0, x)`는 $O(n)$이다.
- **C++ `std::vector`**: 표준은 `push_back`이 분할상환 상수 시간이기를 요구하고, 이것이 기하급수적 증가를 강제한다. 배수는 구현 정의다(libstdc++·libc++는 2, MSVC는 1.5). 재할당은 벡터를 가리키는 모든 반복자·포인터·참조를 무효로 만든다 — `&v[0]`을 쥔 채 `push_back`하면 생기는 고전적 크래시다.

```python
import sys

xs, last, resizes = [], sys.getsizeof([]), []
for i in range(300):
    xs.append(i)
    size = sys.getsizeof(xs)
    if size != last:
        resizes.append(len(xs))       # the append that triggered a reallocation
        last = size
print(resizes)                        # gaps between resizes keep growing
```

**분할상환은 연산 하나하나의 최악 경우가 아니다.** 로봇에서는 이 구분이 실제 문제다. 1 kHz로 벡터에 append하는 제어 콜백은 평균적으로 빠르지만, 재할당이 일어나는 그 한 번의 호출이 마감 시간을 넘길 수 있다. 실시간 코드에서는 루프가 시작되기 전에 `reserve(n)`(C++)을 부르거나 미리 할당하라(`[0.0] * n`, NumPy 배열). 콜백이 어디서 실행되고 마감을 놓치면 나머지 시스템에 무슨 일이 생기는지는 [[04-robotics/ros2/qos-executors-time|25.5 QoS, 실행기와 시간 §8]]에 있다.

### 5. 재귀를 제대로 쓰기

올바른 재귀 함수에는 세 가지가 필요하다.

1. **기저 사례** — 재귀 없이 반환한다. 그리고 모든 유효한 입력이 결국 여기에 닿아야 한다.
2. **진행** — 재귀 호출은 언제나 엄밀히 더 작은 인스턴스에 대해 한다(더 작은 $n$, 더 짧은 리스트, 더 적은 남은 선택).
3. **호출을 믿어라.** 재귀 사례를 쓸 때는 더 작은 입력에 대한 호출이 이미 올바른 답을 돌려준다고 가정하고, 오직 그것으로 내 답을 어떻게 만드는지만 묻는다. 이것이 수학적 귀납법이다 — 기저 사례가 기저 단계, 호출을 믿는 것이 귀납 가정이다. 머릿속에서 호출 열 단계를 추적하는 것은 스스로를 설득하는 잘못된 방법이다.

**공간도 센다.** 활성 호출마다 스택 프레임을 차지하므로, 깊이 $D$의 재귀는 아무것도 할당하지 않아도 $\Theta(D)$ 추가 공간을 쓴다. 공간 분석에서 이것을 말하라.

```python
def power(x, n):
    """x ** n for an integer n >= 0 with O(log n) multiplications."""
    if n == 0:                        # base case
        return 1
    half = power(x, n // 2)           # progress: n halves; trust the call
    return half * half * (x if n % 2 else 1)

print(power(3, 13), 3 ** 13)          # 1594323 1594323
```

점화식은 $T(n) = T(n/2) + 1$이므로 시간 $\Theta(\log n)$, 스택 $\Theta(\log n)$이다. **함정:** `power(x, n // 2) * power(x, n // 2)`라고 쓰면 같은 것을 두 번 계산해서 $T(n) = 2T(n/2) + 1 = \Theta(n)$이 된다 — 답은 맞지만 지수적으로 느리다.

**메모이제이션.** 재귀 호출이 겹칠 때 — 같은 인자가 거듭 요청될 때 — 결과를 처음 계산할 때 저장하고 그 뒤로는 찾아 쓴다. 비용은 (서로 다른 인자의 수) × (하위 호출을 뺀 호출당 일)이 된다. 순진한 피보나치는 $2F(n+1) - 1$번 호출하는데, $n = 30$이면 약 270만 번이다. 메모이제이션한 버전은 서로 다른 계산 $n + 1$번이다.

쓰는 방법 두 가지:

- **`functools.lru_cache(maxsize=None)`** (Python 3.9+에서는 `functools.cache`)를 데코레이터로. 인자는 해시 가능해야 하므로 리스트가 아니라 튜플을 넘긴다. 캐시는 호출 사이에 남는다 — 테스트 하네스가 서로 무관한 입력에 함수를 재사용하면 `.cache_clear()`로 비워라.
- **래퍼 안의 명시적 딕셔너리.** 공개 함수가 캐시를 만들고, 재귀를 하는 중첩 헬퍼를 정의한다. 호출 사이에 새는 것이 없고, 키는 직접 만든 어떤 튜플이든 되며, 이 패턴은 C++로 그대로 옮겨진다(참조로 넘기는 `unordered_map`이나 2차원 `vector`). `memo={}` 같은 가변 기본 인자를 캐시로 쓰지 마라. 함수의 모든 호출이 그것을 공유한다.

```python
from functools import lru_cache

calls = 0
def fib_naive(n):
    global calls
    calls += 1
    return n if n < 2 else fib_naive(n - 1) + fib_naive(n - 2)

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

def count_paths(grid):
    """Right/down paths from top-left to bottom-right; grid cells with 1 are blocked."""
    rows, cols, memo = len(grid), len(grid[0]), {}
    def helper(r, c):
        if r >= rows or c >= cols or grid[r][c]:
            return 0
        if (r, c) == (rows - 1, cols - 1):
            return 1
        if (r, c) not in memo:
            memo[(r, c)] = helper(r + 1, c) + helper(r, c + 1)
        return memo[(r, c)]
    return helper(0, 0)

print(fib_naive(20), calls, fib(90))                  # 6765 21891 2880067194370816120
open_row, blocked_middle = [0, 0, 0], [0, 1, 0]
print(count_paths([open_row, blocked_middle, open_row]))  # 2
```

`count_paths`에는 서로 다른 상태가 $rows \times cols$개 있고 각 상태에서 $O(1)$ 일을 하므로 시간·공간 모두 $\Theta(rows \cdot cols)$다. 이것은 작은 동적 계획법이기도 하다. 반복문 순서로 채우는 표로 바꾸는 것은 DP 페이지의 주제이고, 같은 "다음 상태의 값을 재사용한다"는 생각이 [[02-foundations/rl-basics|7. 강화학습 기초 §3]]의 벨만 백업이다.

**Python의 재귀 깊이.** CPython은 폭주하는 재귀를 기본 1000 프레임 한계(`sys.getrecursionlimit()`)로 막고 `RecursionError`를 낸다. 메모이제이션한 코드도 여기에 걸린다. 빈 캐시에서 `fib(5000)`을 부르면 5000 깊이로 재귀해서 실패하고, 1000 × 1000 점유 격자에 대한 `count_paths`는 약 2000 깊이로 재귀한다. `sys.setrecursionlimit`로 한계를 올릴 수 있지만, 인터프리터의 C 스택이 감당할 수 있는 수준보다 훨씬 높게 잡으면 예외 대신 프로세스가 죽는다. 견고한 해법은 캐시를 반복문으로 아래에서부터 채우거나, 호출 스택을 스택으로 쓰는 명시적 리스트로 바꾸는 것이다. C++에는 한계 검사가 아예 없다. 스레드 스택(Linux에서 흔히 8 MB, Windows에서 1 MB)을 넘으면 세그멘테이션 오류다.

```python
def fib_iter(n):                      # bottom-up: Theta(n) time, Theta(1) space, no recursion
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(len(str(fib_iter(5000))))       # 1045 digits, no RecursionError
```

### 6. 백트래킹: 선택, 탐색, 선택 취소

**백트래킹(backtracking).** 해를 한 번에 결정 하나씩 쌓아 가다가, 부분해가 완성될 수 없다는 것이 드러나는 즉시 버린다. 모든 백트래킹 함수의 모양은 같다:

```text
def backtrack(state):
    if state is a complete solution: record a copy; return
    for each choice allowed from state:
        if choice cannot lead to a solution: skip it      # pruning
        make the choice                                    # choose
        backtrack(new state)                               # explore
        undo the choice                                    # un-choose
```

코딩하기 전에 네 질문에 답하라. *결정 하나는 무엇인가? 그 선택지는 무엇인가? 선택은 어떻게 되돌리는가? 해는 언제 완성되는가?* 호출들은 결정 트리(**decision tree**)를 이룬다. 뿌리는 빈 부분해, 각 간선은 선택 하나, 각 잎은 완성된 후보다.

- **부분집합.** 원소마다 결정 하나: 빼거나 넣는다. 트리의 잎은 $2^n$개이고 완성된 부분집합을 복사하는 데 $O(n)$이 드므로 시간은 $\Theta(n\,2^n)$ — 출력 자체가 그 크기이니 피할 수 없다 — 이고, 경로와 스택에 $O(n)$ 추가 공간을 쓴다.
- **순열.** $i$번째 결정은 아직 쓰지 않은 원소 중 무엇을 $i$번 자리에 둘지다. 잎은 $n!$개, 전체 노드는 $e \cdot n!$개 미만이므로 복사까지 포함해 $\Theta(n \cdot n!)$.
- **N-Queens.** $n \times n$ 판에 서로 공격하지 않게 퀸 $n$개를 놓는다. *행마다* 퀸 하나를 고르면 행 제약이 결정 자체에 들어간다. 사용한 열과 대각선을 집합으로 들고 있으면 안전 검사가 $O(1)$이다. 같은 "\\" 대각선의 칸은 $r - c$가 같고, 같은 "/" 대각선의 칸은 $r + c$가 같다.

```python
def subsets(nums):
    out, path = [], []
    def backtrack(i):
        if i == len(nums):
            out.append(path[:])       # copy: path keeps changing after this
            return
        backtrack(i + 1)              # decision: leave nums[i] out
        path.append(nums[i])          # choose
        backtrack(i + 1)              # explore
        path.pop()                    # un-choose
    backtrack(0)
    return out

def permutations(nums):
    out, path, used = [], [], [False] * len(nums)
    def backtrack():
        if len(path) == len(nums):
            out.append(path[:])
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True; path.append(x)       # choose
                backtrack()                          # explore
                path.pop(); used[i] = False          # un-choose
    backtrack()
    return out

def n_queens(n):
    """Number of ways to place n non-attacking queens on an n x n board."""
    cols, diag, anti = set(), set(), set()
    def place(r):
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or r - c in diag or r + c in anti:
                continue                             # prune: square is attacked
            cols.add(c); diag.add(r - c); anti.add(r + c)
            total += place(r + 1)
            cols.remove(c); diag.remove(r - c); anti.remove(r + c)
        return total
    return place(0)

print(len(subsets([1, 2, 3])), len(permutations([1, 2, 3])), n_queens(4), n_queens(8))  # 8 6 2 92
```

**가지치기(pruning)** — 백트래킹의 값어치는 여기서 나온다. 내부 노드에서의 검사 하나가 그 아래 부분 트리 전체를 없앤다. 가장 강한 가지치기는 순서에서 나온다. 값이 정렬되어 있으면 목표를 처음 넘는 값이 그 뒤 모든 값도 넘는다는 증명이 되므로, 루프는 `continue`가 아니라 `break`할 수 있다. 정렬하면 같은 깊이에서 같은 값을 건너뛸 수도 있어서, 집합 없이 중복 답을 없앤다.

```python
def subsets_with_sum(nums, target):
    """All distinct multisets drawn from positive nums that sum to target."""
    nums, out, path = sorted(nums), [], []
    def backtrack(start, remaining):
        if remaining == 0:
            out.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remaining:
                break                                # prune: later values are larger still
            if i > start and nums[i] == nums[i - 1]:
                continue                             # same value at the same depth: duplicate
            path.append(nums[i])
            backtrack(i + 1, remaining - nums[i])
            path.pop()
    backtrack(0, target)
    return out

print(subsets_with_sum([3, 1, 4, 1, 5, 2], 6))  # four lists: [1, 1, 4] [1, 2, 3] [1, 5] [2, 4]
```

**탐색 트리의 복잡도.** 분기 계수가 최대 $b$, 깊이가 최대 $d$이면 잎은 최대 $b^d$개이고, 실행 시간은 (방문한 노드 수) × (노드당 일)이다. 가지치기는 최악 경우 상한을 거의 개선하지 못한다 — 열 집합을 쓴 N-Queens도 상한은 $n!$뿐이다 — 하지만 실용 범위를 몇 자릿수 바꾼다. 정직한 인터뷰 답은 둘 다 말한다: "최악 $O(n!)$, 실제로는 대각선 검사가 대부분의 가지를 일찍 자른다."

**인터뷰 함정.** 복사본 대신 `path`를 그대로 추가하기(기록된 답이 전부 같은, 결국 빈 리스트가 된다). 선택 취소 단계를 잊어서 한 가지의 상태가 형제 가지로 새기. 유효성을 잎에서만 검사해서 백트래킹을 다시 무차별 탐색으로 만들기. 정렬 순서가 `break`를 허락하는데 `continue`를 쓰기.

로봇에서 백트래킹은 작고 어려운 조합 선택에 맞는 도구다 — 각 블록이 이미 놓인 블록의 지지를 받아야 할 때 몇 개 안 되는 블록을 놓는 순서, 또는 파지끼리 충돌하면 안 될 때 몇 개 물체 각각에 어떤 파지를 쓸지. 결정이 대략 스무 개를 넘으면 트리가 너무 커지고, 도구는 동적 계획법, 휴리스틱 그래프 탐색, 제약 해결기로 바뀐다. 과제 수준의 관점은 [[04-robotics/planning-decision-making|4. 계획과 의사결정 §7]]에 있다.

### 7. 인터뷰에서 복잡도를 말하는 법

완전한 복잡도 답에는 다섯 부분이 있고, 이 순서로 말하면 즉석에서 생각하는 중에도 정리되어 들린다.

1. **크기에 이름을 붙인다.** "$n$을 점의 개수, $k$를 윈도 길이라 하자." $n$을 정의하지 않은 채 두지 말고, 독립인 두 크기를 하나로 합치지 마라.
2. **지배적인 연산을 말하고 센다.** "각 점은 힙에 한 번 넣고 한 번 빼며, 힙 연산 하나는 $O(\log k)$다."
3. **시간 상한을 수식어와 함께 말한다:** 최악 경우, 평균 경우(해시 테이블), 기대값(무작위 피벗), 분할상환(동적 배열, 슬라이딩 윈도 포인터).
4. **공간을 말한다:** 보조 자료구조, 재귀 스택, 그리고 출력이 크면 출력(모든 부분집합은 그것만으로 $\Theta(n\,2^n)$).
5. **제약과 연결하고 트레이드오프를 제시한다.** "$n \le 10^5$이면 $O(n^2)$ 무차별 탐색은 약 $10^{10}$ 단계라 너무 느리다. 먼저 정렬하면 $O(n)$ 추가 메모리를 대가로 $O(n \log n)$이 된다."

> [!example] 계산 예제 · Worked example
> **질문:** 2차원 라이다 점 $n$개가 주어질 때, 거리가 $r$보다 가까운 쌍을 모두 보고하라.
>
> **말로 하는 답:** "$n$을 점의 개수, $K$를 보고하는 쌍의 개수라 하자. 무차별 탐색은 $n(n-1)/2$쌍을 모두 비교한다: 시간 $\Theta(n^2)$, 출력 외 추가 공간 $O(1)$. 더 나은 방법: 각 점을 한 변이 $r$인 격자 칸에 해시한다. 가까운 쌍은 같은 칸이나 인접 칸에 있으므로 점마다 9칸을 확인한다. 딕셔너리 연산이 평균 $O(1)$이므로 격자 구축은 기대 $O(n)$이고, 어느 칸에도 점이 지나치게 몰리지 않는 한 탐색은 $O(n + K)$다. 최악 경우는 여전히 $\Theta(n^2)$이다 — 모든 점이 서로 $r$ 이내에 있으면 $K$ 자체가 $\Theta(n^2)$이므로 어떤 알고리즘도 더 잘할 수 없다. 추가 공간은 격자에 $O(n)$."
>
> 이 답은 두 크기에 이름을 붙이고, 경우를 말하고, 평균 경우의 가정을 설명하고, 최악 경우를 개선할 수 없는 이유를 말한다. 같은 추론으로, 최근접 이웃을 찾으려고 트리 노드를 전부 훑는 샘플링 계획기는 표본당 $O(n)$, 표본 $n$개에 걸쳐 $O(n^2)$이 들고, 그래서 실제 계획기는 공간 색인을 쓴다([[04-robotics/modern-robotics/ch10-motion-planning|MR 10장 — 모션 계획]]).

**점수를 잃는 말:**

- "해시 맵 조회는 $O(1)$이다." — 괜찮은 해시에서 평균 $O(1)$, 최악 $O(n)$.
- "재귀는 추가 공간을 쓰지 않는다." — $O(\text{깊이})$ 스택을 쓴다.
- "중첩 루프 두 개니까 $O(n^2)$." — 안쪽 포인터가 뒤로 가지 않으면 아니다(§2, 예제 3).
- "정렬은 $O(n \log n)$이다." — 비교 정렬의 경우다. 작은 정수 키에 대한 계수 정렬은 $O(n + \text{범위})$.
- 그래프 알고리즘에 "$O(n)$이다." — $O(V + E)$라고 말하라. 조밀한 그래프는 $E = \Theta(V^2)$다.
- 답을 만드는 비용을 잊기: 경로 복사, 문자열 슬라이싱, 출력 이어 붙이기.

### 스스로 점검

1. 어떤 함수가 $n = 10^5$에서 0.8초, $n = 2 \times 10^5$에서 3.3초 걸린다. 어떤 증가율이 의심되고, $n = 4 \times 10^5$에서는 얼마로 예측하는가?
2. 다음의 Θ 상한·하한을 구하라: `for i in range(1, n): j = 1; while j < i: j *= 2`.
3. 마스터 방법으로 풀어라: (a) $T(n) = 4T(n/2) + n^2$; (b) $T(n) = 3T(n/2) + n$; (c) $T(n) = 2T(n/2) + n^2$.
4. 동적 배열이 가득 찰 때마다 1000칸씩 늘어난다. $10^6$번 append하면 원소 복사가 대략 몇 번 일어나고, 두 배 증가라면 몇 번인가?
5. `fib`에 `@lru_cache(maxsize=None)`가 붙어 있다. 새 인터프리터에서 `fib(5000)`을 부르면 왜 `RecursionError`가 나고, 해법 두 가지는 무엇인가?
6. `subsets`에서 누군가 `out.append(path[:])` 대신 `out.append(path)`라고 썼다. `subsets([1, 2])`는 무엇을 반환하고, 왜 그런가?
7. N-Queens에서 행마다 퀸을 정확히 하나 놓으면 왜 탐색 공간이 $\binom{n^2}{n}$가지 배치에서 최대 $n^n$으로 줄고, 열 집합은 어떤 상한을 더 주는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 비율은 $3.3/0.8 \approx 4.1$이고 $\log_2 4.1 \approx 2$: 이차다. 한 번 더 두 배면 약 4배이므로 약 13초.
> 2. 안쪽 루프는 약 $\log_2 i$번 돌므로 합은 $\sum_{i<n} \log_2 i = \log_2 (n-1)! = \Theta(n \log n)$. (상한: 각 항이 $\log_2 n$ 이하. 하한: 위쪽 절반의 항이 각각 $\log_2(n/2)$ 이상.)
> 3. (a) $a = 4 = b^d = 2^2$: 경우 2, $\Theta(n^2 \log n)$. (b) $a = 3 > b^d = 2$: 경우 3, $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$ — 카라츠바 곱셈의 상한이다. (c) $a = 2 < b^d = 4$: 경우 1, $\Theta(n^2)$.
> 4. 복사는 크기 1000, 2000, …, $10^6$에서 일어나므로 합은 약 $1000 \cdot (1 + 2 + \dots + 1000) \approx 5 \times 10^8$. 두 배 증가는 $2 \times 10^6$ 미만 — 약 250분의 1이다.
> 5. 빈 캐시에서 `fib(5000)`은 아무것도 저장되기 전에 `fib(4999)`를 불러야 하고, 그것은 `fib(4998)`을 부르고, 계속 이어진다. 스택 깊이가 5000에 이르러 기본 한계 1000을 넘는다. 해법: 반복문으로 아래에서부터 계산하기(또는 `i`를 늘려 가며 `fib(i)`를 불러 캐시를 데우기), 또는 명시적 스택 쓰기. `sys.setrecursionlimit`를 올리는 것은 C 스택이 버티는 동안만 통한다.
> 6. 빈 리스트 네 개로 된 리스트, `[ [], [], [], [] ]`. 모든 항목이 같은 리스트 객체를 가리키는 참조다. 각 `append`는 나중에 `pop`으로 되돌려지므로, 탐색이 끝나면 그 리스트 하나는 비어 있고 네 항목 모두 그것을 보여 준다.
> 7. 같은 행의 두 퀸은 서로 공격하므로 유효한 배치는 행마다 퀸이 정확히 하나다. $n$개 행 각각에 열을 고르면 후보는 $n^n$개다. 같은 열의 두 퀸도 공격하므로 열이 모두 달라야 한다 — 순열이다 — 그래서 잎은 최대 $n!$개다. 대각선 집합이 더 가지치기하지만, 실제로 방문하는 노드 수에 대한 간단한 닫힌 식은 알려져 있지 않다.

### 출처

- T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — 점근 표기법, 분할정복 점화식과 마스터 정리, 분할상환 분석 장.
- T. Roughgarden, *Algorithms Illuminated, Part 1: The Basics*, Soundlikeyourself Publishing, 2017 — 점근 표기법과 §3에서 쓴 $a$ 대 $b^d$ 형태의 마스터 방법.
- A. S. Kulikov, P. A. Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — 1–2장: 실행 시간, big-O 규칙, 재귀 트리, 설계 기법.
- D. E. Knuth, "Big Omicron and big Omega and big Theta," *ACM SIGACT News* 8(2), 1976, pp. 18–24. DOI: 10.1145/1008328.1008329 — O, Ω, Θ의 현대적 의미를 정한 글.
- J. L. Bentley, D. Haken, J. B. Saxe, "A general method for solving divide-and-conquer recurrences," *ACM SIGACT News* 12(3), 1980 — 마스터 정리의 기원.
- R. E. Tarjan, "Amortized computational complexity," *SIAM Journal on Algebraic and Discrete Methods* 6(2), 1985. DOI: 10.1137/0606031 — 분할상환 분석에 이름을 붙이고 체계화한 논문.
- S. W. Golomb, L. D. Baumert, "Backtrack programming," *Journal of the ACM* 12(4), 1965 — 백트래킹 탐색의 초기 체계적 서술.
