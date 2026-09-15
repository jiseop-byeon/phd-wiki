---
title: 11.5 Dynamic Programming
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Define a DP subproblem in words, write its recurrence, fill the table in a valid order, and reconstruct the answer for the standard 1-D, 2-D, sequence, graph and bitmask patterns."
mastery-when: "Raise to Mastery only if your research runs DP at scale — value iteration on large state spaces, trajectory alignment, or exact combinatorial planning — where memory layout and pruning decide feasibility."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/complexity-recursion|11.1 Complexity, Recursion & Backtracking]] (recursion trees, counting work per call) · [[02-foundations/rl-basics|7. RL Basics §2]] (the Bellman equation, for §7)
> [[02-foundations/algorithms/complexity-recursion|11.1 복잡도·재귀·백트래킹]](재귀 트리, 호출당 작업량 세기) · [[02-foundations/rl-basics|7. RL 기초 §2]](§7을 위한 벨만 방정식)

## English

Dynamic programming (DP) is the technique interviewers reach for when they want to see whether
you can *design* an algorithm rather than recall one. The problems look different — coins,
strings, knapsacks, subsequences, tours — but the work is always the same: name a family of
subproblems, relate each one to smaller ones, fill a table in an order that respects that
relation, and walk back through the table to recover the actual choice, not just its cost.
Research-lab interviews add a second question: *where does this show up in robotics?* The honest
answer is value iteration (the Bellman equation is DP over time) and dynamic time warping for
comparing demonstrations, both in §7.

> [!note] First pass · 처음이라면
> Read §1 and §2 slowly — the recipe and the two implementation styles are what every later section reuses. Then do §3 and §4 with the code open. §5 and §6 are pattern libraries to revisit before an interview; §8 is the checklist to read the night before.

### 1. When DP applies, and how it differs from its neighbours

DP needs two properties.

- **Optimal substructure.** An optimal solution to the whole problem contains optimal solutions
  to smaller instances of the *same* problem. The proof is almost always a cut-and-paste
  argument: if the piece inside the optimum were not optimal, swap in a better piece and the
  whole would improve — a contradiction.
- **Overlapping subproblems.** The natural recursion asks the same smaller question many times.
  That is what makes caching pay: a problem with a few thousand *distinct* subproblems can have a
  recursion tree with billions of nodes.

**How it differs from the neighbours.**

| Paradigm | Subproblems | Choice at each step | Typical proof |
|---|---|---|---|
| Divide and conquer | Disjoint (merge sort's two halves never share work) | None — the split is fixed | Recurrence / Master theorem |
| Greedy | One remaining subproblem | Commit to one locally best choice, never revisit | Exchange argument: the greedy choice is in some optimum |
| Dynamic programming | Overlapping, reused many times | Try every option for the last decision, keep the best | Cut-and-paste + induction on subproblem size |

A useful way to hold this: greedy is a DP in which you have proven that one option always
suffices, and divide and conquer is a recursion whose subproblems happen never to repeat, so a
cache would sit unused.

**When optimal substructure fails.** Take the *longest simple path* between two vertices of a
graph with cycles. Split it at a middle vertex $v$: the two halves need not be longest simple paths
themselves, because the longest path from $s$ to $v$ and the longest from $v$ to $t$ may reuse the
same vertices, and gluing them breaks simplicity. The subproblem "longest path from $s$ to $v$" is
not self-contained — it needs to know which vertices are already used. Held–Karp in §6 is exactly
what you get when you add that missing information to the state, and it is why the state becomes
exponential.

**A 4-step recipe.** Say each step out loud in an interview.

1. **Define the subproblem in words.** "Let $f(i)$ be the fewest coins that sum to exactly $i$."
   If you cannot say it in one sentence, the recurrence will be wrong.
2. **Write the recurrence** by asking *what is the last decision?* — the last coin, whether the
   last item is taken, what the last column of an alignment holds. One case per option, take
   the min/max/sum.
3. **Fix the base cases and an evaluation order** in which every value a cell needs is already
   computed. Complexity = (number of subproblems) × (work per subproblem).
4. **Reconstruct.** Either store the winning choice per cell, or re-derive it from the finished
   table by checking which case produced the cell's value.

### 2. Top-down memoization vs bottom-up tabulation

The same recurrence can be run two ways.

- **Top-down (memoization):** write the recursion literally and cache each result the first time
  it is computed. Only the subproblems actually reached are solved, and the order is found for
  you. Costs: function-call overhead and Python's recursion limit (default depth 1000).
- **Bottom-up (tabulation):** allocate the table and fill it in an explicit order. No recursion,
  better cache locality, and the loop structure makes the complexity obvious. You must work out
  the order yourself.

> [!example] Worked example · 계산 예제
> A robot crosses a grid of floor cells from top-left to bottom-right, moving only right or down; each cell has a traversal cost. Grid rows: $[2, 1, 4]$, $[3, 9, 1]$, $[4, 2, 2]$. Subproblem: $f(r,c)$ = cheapest cost to reach cell $(r,c)$, including that cell. The last move came from above or from the left, so $f(r,c) = \text{cost}(r,c) + \min(f(r-1,c),\, f(r,c-1))$. Filling row by row gives $[2, 3, 7]$, $[5, 12, 8]$, $[9, 11, 10]$, so the answer is $10$ along $2 \to 1 \to 4 \to 1 \to 2$. Without the cache, the recursion reaches cell $(r,c)$ once per monotone path to it, $\binom{r+c}{r}$ times; with it, each of the $9$ cells is solved once.

```python
from functools import cache

def min_path_topdown(cost):
    rows, cols = len(cost), len(cost[0])

    @cache
    def f(r, c):                      # cheapest cost from (0, 0) to (r, c), inclusive
        if r == 0 and c == 0:
            return cost[0][0]
        best = float("inf")
        if r > 0:
            best = min(best, f(r - 1, c))
        if c > 0:
            best = min(best, f(r, c - 1))
        return best + cost[r][c]

    return f(rows - 1, cols - 1)


def min_path_bottomup(cost):
    rows, cols = len(cost), len(cost[0])
    INF = float("inf")
    dp = [0] + [INF] * (cols - 1)     # one rolling row instead of a rows x cols table
    for r in range(rows):
        for c in range(cols):
            left = dp[c - 1] if c > 0 else INF
            dp[c] = min(dp[c], left) + cost[r][c]   # dp[c] still holds the row above
    return dp[-1]
```

**Space optimization with rolling arrays.** When row $r$ reads only row $r-1$ (and cells to its
left in row $r$), keep one row: before `dp[c]` is overwritten it still holds the value from the row
above, and `dp[c - 1]` has already been updated to the current row. Memory drops from
$O(\text{rows}\cdot\text{cols})$ to $O(\text{cols})$. The price is reconstruction: once a row is
overwritten, the choices it recorded are gone. If you need the path, keep the full table, store
parent pointers, or use a divide-and-conquer trick (Hirschberg's method for alignments).

**Which to use.** In an interview, top-down is faster to write correctly when the order is not
obvious (trees, intervals, bitmasks) or when most states are unreachable; bottom-up is the default
when the order is a simple loop and when you want the rolling-array memory saving. In C++, a
top-down memo is usually a `std::vector` indexed by state with a sentinel for "not computed"
rather than a `std::map`, which is far slower.

### 3. 1-D DP

**Climbing stairs / counting paths.** If you can climb 1 or 2 steps at a time, the number of ways
to reach step $n$ is $w(n) = w(n-1) + w(n-2)$ with $w(0) = 1$ — the last move was a 1-step or a
2-step. It is the Fibonacci recurrence, and the same code as "number of ordered ways to make change
with coins $\{1, 2\}$" below.

**Coin change — minimum coins.** Subproblem: $f(a)$ = fewest coins summing to exactly $a$. The last
coin is some $c \le a$, so the recurrence below holds because removing that coin leaves an optimal
solution for $a - c$ (cut-and-paste):

$$f(a) = 1 + \min_{c \in \text{coins},\ c \le a} f(a - c), \qquad f(0) = 0$$

Complexity $O(a \cdot k)$ for $k$ denominations.

> [!example] Worked example · 계산 예제
> Coins $\{1, 3, 4\}$, target $6$. Greedy takes the largest coin that fits: $4$, then $1$, then $1$ — **three** coins. DP: $f(0..6) = 0, 1, 2, 1, 1, 2, 2$. At $a = 6$ the options are $f(5)+1 = 3$ (last coin 1), $f(3)+1 = 2$ (last coin 3), $f(2)+1 = 3$ (last coin 4), so $f(6) = 2$ via $3 + 3$. Greedy fails because taking $4$ leaves a remainder ($2$) that the other coins cover badly; no local rule can see that. Greedy is optimal for "canonical" systems such as $\{1, 5, 10, 25\}$, but that is a property of the denominations, and proving it is a separate argument.

```python
def min_coins(coins, target):
    INF = float("inf")
    best = [0] + [INF] * target       # best[a]: fewest coins summing to exactly a
    last = [None] * (target + 1)      # last[a]: the final coin of one optimal answer
    for a in range(1, target + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a], last[a] = best[a - c] + 1, c
    if best[target] == INF:
        return None                   # target cannot be formed
    used, a = [], target
    while a > 0:                      # reconstruction: peel off the recorded last coin
        used.append(last[a])
        a -= last[a]
    return used
```

**Coin change — number of ways.** Now $g(a)$ counts, and the base case is $g(0) = 1$ (one way to
make zero: take nothing). The subtle part is *what counts as different*, and it is decided purely
by loop order:

```python
def count_combinations(coins, target):   # 1+3 and 3+1 are the same way
    ways = [1] + [0] * target
    for c in coins:                       # coins outer: each multiset is built in one order
        for a in range(c, target + 1):
            ways[a] += ways[a - c]
    return ways[target]


def count_orderings(coins, target):      # 1+3 and 3+1 are different ways
    ways = [1] + [0] * target
    for a in range(1, target + 1):        # amount outer: any coin may come last
        for c in coins:
            if c <= a:
                ways[a] += ways[a - c]
    return ways[target]
```

With coins outer, by the time coin $c$ is processed every table entry only uses coins earlier in
the list, so each multiset is counted once, in list order. With amount outer, the last coin ranges
over all denominations, so sequences are counted. For $\{1, 3, 4\}$ and $6$: $4$ combinations
($1^6$, $3+1^3$, $3+3$, $4+1+1$) but $9$ orderings. `count_orderings([1, 2], n)` is climbing stairs.

**Maximum-weight independent set on a path.** Vertices $v_1, \dots, v_n$ in a line with weights
$w_i \ge 0$; pick non-adjacent vertices of maximum total weight. Subproblem: $A[i]$ = best total
using only the first $i$ vertices. Either $v_i$ is not in the optimum (then the optimum is $A[i-1]$)
or it is (then $v_{i-1}$ is excluded and the rest is an optimum for the first $i-2$), so the
recurrence is $A[i] = \max(A[i-1],\ A[i-2] + w_i)$ with $A[0] = 0$, $A[1] = w_1$. $O(n)$ time.

> [!example] Worked example · 계산 예제
> Weights $[3, 2, 5, 10, 7]$. $A = 0, 3, 3, 8, 13, 15$. Reconstruction walks back: $A[5] = 15 \ne A[4] = 13$, so $v_5$ is taken, jump to $i = 3$; $A[3] = 8 \ne A[2]$, take $v_3$, jump to $i = 1$; $A[1] = 3 \ne A[0]$, take $v_1$. Answer $\{v_1, v_3, v_5\}$, weight $15$. Greedy (take the heaviest vertex that is still allowed) takes $10$, which blocks $5$ and $7$, then takes $3$: total $13$.

```python
def max_weight_independent_set(w):
    n = len(w)
    A = [0] * (n + 1)                 # A[i]: best total using the first i vertices
    if n:
        A[1] = w[0]
    for i in range(2, n + 1):
        A[i] = max(A[i - 1], A[i - 2] + w[i - 1])
    chosen, i = [], n
    while i >= 1:                     # if skipping vertex i loses nothing, skip it
        if A[i] == A[i - 1]:
            i -= 1
        else:                         # vertex i must be in this optimum
            chosen.append(i - 1)
            i -= 2
    return A[n], chosen[::-1]         # 0-based indices
```

The reconstruction needs no extra storage: the finished table already says which case won.

### 4. 2-D DP

**0/1 knapsack.** $n$ items with integer weights $w_i$ and values $v_i$, capacity $W$; each item at
most once. Subproblem: $V[i][x]$ = best value using only the first $i$ items with capacity $x$. Item
$i$ is either left out or put in, and in the second case the remaining items must be optimal for
capacity $x - w_i$, so

$$V[i][x] = \max\big(V[i-1][x],\ V[i-1][x - w_i] + v_i\big), \qquad V[0][x] = 0$$

where the second option exists only if $w_i \le x$. There are $(n+1)(W+1)$ cells, each $O(1)$, so the
time is $O(nW)$.

```python
def knapsack_01(items, W):            # items: list of (weight, value), integer weights
    n = len(items)
    V = [ [0] * (W + 1) for _ in range(n + 1)]   # V[i][x]: first i items, capacity x
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for x in range(W + 1):
            V[i][x] = V[i - 1][x]
            if w <= x:
                V[i][x] = max(V[i][x], V[i - 1][x - w] + v)
    take, x = [], W
    for i in range(n, 0, -1):         # item i was taken iff it changed the value
        if V[i][x] != V[i - 1][x]:
            take.append(i - 1)
            x -= items[i - 1][0]
    return V[n][W], take[::-1]
```

> [!example] Worked example · 계산 예제
> Items (weight, value): $(1,1), (3,4), (4,5), (5,7)$, capacity $7$. Greedy by value density takes $(5,7)$ (density $1.4$), cannot fit $(3,4)$ or $(4,5)$, then adds $(1,1)$: value $8$. The table gives $V[4][7] = 9$ from $(3,4) + (4,5)$, which fills the capacity exactly. Reconstruction: $V[4][7] = V[3][7] = 9$, so item 4 was not needed; $V[3][7] = 9 \ne V[2][7] = 5$, take item 3 and move to $x = 3$; $V[2][3] = 4 \ne V[1][3] = 1$, take item 2, $x = 0$. Density-greedy is optimal only for the *fractional* knapsack, where you may cut the last item.

**Why $O(nW)$ is pseudo-polynomial.** "Polynomial" means polynomial in the *length of the input*.
The capacity $W$ is written in about $\log_2 W$ bits, so $W = 2^{\text{bits}}$ is exponential in its
own encoding. With $n = 100$ and $W = 10^9$ the input is a few kilobytes but the table has $10^{11}$
cells. This is consistent with 0/1 knapsack being NP-hard: the DP is fast only when the numbers are
small. Two practical consequences: dividing all weights by their greatest common divisor shrinks
$W$ for free, and when values are small but weights are huge, swap roles — index the table by
*value* and store the minimum weight that achieves it.

**Rolling the knapsack to 1-D — and the loop-direction trap.**

```python
def knapsack_01_1d(items, W):
    best = [0] * (W + 1)
    for w, v in items:
        for x in range(W, w - 1, -1):    # downward: best[x - w] still excludes this item
            best[x] = max(best[x], best[x - w] + v)
    return best[W]


def knapsack_unbounded(items, W):
    best = [0] * (W + 1)
    for w, v in items:
        for x in range(w, W + 1):        # upward: best[x - w] may already include it
            best[x] = max(best[x], best[x - w] + v)
    return best[W]
```

The two functions differ only in the direction of the inner loop. Going downward, `best[x - w]` is
read before this item's pass has touched it, so it still means "previous items only" — the 0/1
rule. Going upward, `best[x - w]` has already been updated in this pass and may contain the item, so
the item can be reused — the unbounded rule. With one item $(2, 3)$ and $W = 4$: downward gives $3$,
upward gives $6$.

**Edit distance (Levenshtein).** The minimum number of single-character insertions, deletions and
substitutions turning string $a$ into $b$. Subproblem: $D[i][j]$ = distance between the prefixes
$a[:i]$ and $b[:j]$. The last column of an optimal alignment either deletes $a_i$, inserts $b_j$, or
pairs $a_i$ with $b_j$ (free if equal, cost 1 otherwise), so

$$D[i][j] = \min\big(D[i-1][j] + 1,\ D[i][j-1] + 1,\ D[i-1][j-1] + [a_i \ne b_j]\big)$$

with $D[i][0] = i$ and $D[0][j] = j$ since an empty prefix is reached only by deleting or inserting
everything. $O(nm)$ time and space; $O(\min(n,m))$ space with two rolling rows if you only need the
number.

> [!example] Worked example · 계산 예제
> $a = \texttt{robot}$, $b = \texttt{orbit}$. Rows are prefixes of $a$, columns prefixes of $b$:
>
> | | ε | o | r | b | i | t |
> |---|---|---|---|---|---|---|
> | ε | 0 | 1 | 2 | 3 | 4 | 5 |
> | r | 1 | 1 | 1 | 2 | 3 | 4 |
> | o | 2 | 1 | 2 | 2 | 3 | 4 |
> | b | 3 | 2 | 2 | 2 | 3 | 4 |
> | o | 4 | 3 | 3 | 3 | 3 | 4 |
> | t | 5 | 4 | 4 | 4 | 4 | 3 |
>
> The distance is $D[5][5] = 3$. Backtrace from the corner: $D[5][5] = 3 = D[4][4] + 0$ ($t = t$), go diagonal; $D[4][4] = 3 = D[3][3] + 1$ (o → i), diagonal; $D[3][3] = 2 = D[2][2] + 0$ ($b = b$); $D[2][2] = 2 = D[1][1] + 1$ (o → r); $D[1][1] = 1 = D[0][0] + 1$ (r → o). Alignment `robot` / `orbit`: three substitutions. Ties give other optimal alignments: `-robot` over `or-bit` (insert o, match r, delete o, match b, substitute o → i, match t) also costs 3. Interviewers accept any one; say which tie-break your code uses.

```python
def edit_distance(a, b):
    n, m = len(a), len(b)
    D = [ [0] * (m + 1) for _ in range(n + 1)]   # D[i][j]: cost of turning a[:i] into b[:j]
    for i in range(n + 1):
        D[i][0] = i                              # delete everything
    for j in range(m + 1):
        D[0][j] = j                              # insert everything
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1,                           # delete a[i-1]
                          D[i][j - 1] + 1,                           # insert b[j-1]
                          D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))  # match or substitute
    pairs, i, j = [], n, m                       # backtrace from the bottom-right corner
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            pairs.append((a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            pairs.append((a[i - 1], "-"))
            i -= 1
        else:
            pairs.append(("-", b[j - 1]))
            j -= 1
    pairs.reverse()
    return D[n][m], "".join(p for p, _ in pairs), "".join(q for _, q in pairs)
```

The table is a DAG in disguise: each cell is a node with edges from its top, left and top-left
neighbours, and the distance is the shortest path from the top-left corner to the bottom-right.
Weighted variants (different costs per substitution, affine gap penalties) change only the edge
weights; that is sequence alignment as used in bioinformatics.

**Longest common subsequence (LCS).** The longest sequence that appears in both $a$ and $b$ in
order, not necessarily contiguously. Subproblem: $L[i][j]$ = LCS length of $a[:i]$ and $b[:j]$. If
$a_i = b_j$, some LCS ends by pairing them (any LCS that does not can be edited to do so without
getting shorter), so $L[i][j] = L[i-1][j-1] + 1$; otherwise at least one of the two last elements is
unused, so $L[i][j] = \max(L[i-1][j], L[i][j-1])$. Base cases are zero. $O(nm)$.

```python
def lcs(a, b):
    n, m = len(a), len(b)
    L = [ [0] * (m + 1) for _ in range(n + 1)]   # L[i][j]: LCS length of a[:i] and b[:j]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    out, i, j = [], n, m
    while i > 0 and j > 0:                       # walk back along the cells that won
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]
```

It works on any sequences, not only strings. Two demonstration logs of action primitives,
`[reach, grasp, lift, move, place, release]` and `[reach, push, grasp, move, lift, place, release]`,
share an LCS of length 5, such as `[reach, grasp, lift, place, release]`: the common skeleton of
the two task executions. LCS is edit distance with substitutions forbidden: the insert/delete-only
distance equals $n + m - 2\,L[n][m]$, because every element outside the LCS is deleted from $a$ or
inserted from $b$. The Unix `diff` tool is built on this idea.

### 5. Sequence DP: longest increasing subsequence

**$O(n^2)$ version.** Subproblem: $e[i]$ = length of the longest strictly increasing subsequence
that *ends at* index $i$. Ending at a fixed index is what makes the recurrence possible: the element
before $x_i$ is some earlier $x_j < x_i$, so $e[i] = 1 + \max\{e[j] : j < i,\ x_j < x_i\}$ (or $1$ if no
such $j$). The answer is $\max_i e[i]$, not $e[n-1]$ — a common slip.

```python
def lis_quadratic(xs):
    n = len(xs)
    end = [1] * n                     # end[i]: longest increasing run that ends at i
    prev = [-1] * n                   # prev[i]: index before i in that run
    for i in range(n):
        for j in range(i):
            if xs[j] < xs[i] and end[j] + 1 > end[i]:
                end[i], prev[i] = end[j] + 1, j
    if n == 0:
        return []
    i = max(range(n), key=end.__getitem__)       # best end point, not necessarily n-1
    out = []
    while i != -1:
        out.append(xs[i])
        i = prev[i]
    return out[::-1]
```

**$O(n \log n)$ patience-sorting version.** Keep `tails[k]` = the smallest possible last value of
an increasing subsequence of length $k+1$ seen so far. The invariant is that `tails` is strictly
increasing (a length-$(k+2)$ subsequence contains a length-$(k+1)$ one with a smaller last value).
For each new $x$, binary-search the first `tails[k]` $\ge x$: replacing it with $x$ keeps every
length's tail as small as possible, and if no such $k$ exists, $x$ extends the longest subsequence.
Each element costs one binary search, so $O(n \log n)$. The name comes from dealing cards onto piles
where each card goes on the leftmost pile whose top is not smaller; the number of piles is the LIS
length.

> [!example] Worked example · 계산 예제
> $xs = [3, 1, 4, 1, 5, 9, 2, 6]$. `tails` evolves as $[3] \to [1] \to [1,4] \to [1,4] \to [1,4,5] \to [1,4,5,9] \to [1,2,5,9] \to [1,2,5,6]$. Length $4$. Note that the final `tails` $= [1,2,5,6]$ is **not** a subsequence of $xs$ — the $2$ sits at index 6, after the $5$ at index 4. `tails` stores the best *tail per length*, not a solution; to recover one you must keep a predecessor for each element at the moment it is placed, which gives $[1, 4, 5, 6]$.

```python
from bisect import bisect_left

def lis_patience(xs):
    tails, tail_idx = [], []          # tails[k]: smallest tail of an increasing run of length k+1
    prev = [-1] * len(xs)             # predecessor links, fixed when each element is placed
    for i, x in enumerate(xs):
        k = bisect_left(tails, x)     # first pile whose top is >= x
        if k == len(tails):
            tails.append(x)
            tail_idx.append(i)
        else:
            tails[k], tail_idx[k] = x, i
        prev[i] = tail_idx[k - 1] if k > 0 else -1
    out, i = [], (tail_idx[-1] if tail_idx else -1)
    while i != -1:
        out.append(xs[i])
        i = prev[i]
    return out[::-1]
```

`bisect_left` gives *strictly* increasing; for non-decreasing use `bisect_right`. In C++ the same
two choices are `std::lower_bound` and `std::upper_bound`.

### 6. DP on graphs and bitmasks

**Shortest paths in a DAG via topological order.** In a directed acyclic graph, $d(v) = \min_{(u,v)}
[d(u) + w(u,v)]$ over incoming edges. The topological order *is* the evaluation order: when $u$ is
processed, every path into $u$ has already been relaxed, so $d(u)$ is final. Time $O(V + E)$ —
faster than Dijkstra, and negative edge weights are fine because there are no cycles to exploit
them. Replace min with max (or negate the weights) and you get the *longest* path in a DAG, which
is NP-hard in general graphs. Every table-filling DP above is a shortest or longest path in the
DAG whose nodes are its subproblems, which is why "find the order" and "find a topological sort" are
the same question. The graph pages cover Dijkstra and Bellman–Ford, which handle cycles; see
[[04-robotics/planning-decision-making|4. Planning §3]] for their use on planning graphs.

```python
from collections import deque

def dag_shortest_paths(n, edges, source):    # edges: (u, v, weight); weights may be negative
    adj = [list() for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    order, q = [], deque(i for i in range(n) if indeg[i] == 0)
    while q:                                  # Kahn's algorithm gives a topological order
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        raise ValueError("graph has a cycle")
    dist, parent = [float("inf")] * n, [None] * n
    dist[source] = 0
    for u in order:                           # all predecessors of u are already final
        if dist[u] < float("inf"):
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v], parent[v] = dist[u] + w, u
    return dist, parent
```

**Held–Karp for the travelling salesman problem.** Visit $n$ cities exactly once and return to the
start at minimum cost. §1 showed why "shortest path to $j$" is not a valid subproblem: it forgets
which cities were visited. Held–Karp puts that set into the state. $C(S, j)$ = cheapest path that
starts at city 0, visits exactly the cities in $S$ (0 excluded), and ends at $j \in S$. The city
before $j$ is some $k \in S \setminus \{j\}$, so

$$C(S, j) = \min_{k \in S \setminus \{j\}} \big[ C(S \setminus \{j\}, k) + d(k, j) \big], \qquad C(\{j\}, j) = d(0, j)$$

and the tour cost is $\min_j [C(\text{all}, j) + d(j, 0)]$. The state records *which* cities were
visited but not in *what order*, and that is exactly what cuts $n!$ down. Subsets are processed by
increasing size, since each one reads only subsets one element smaller.

```python
from itertools import combinations

def held_karp(dist):                  # dist[i][j]: cost i -> j; the tour starts and ends at 0
    n = len(dist)
    if n == 1:
        return 0, [0, 0]
    C = {}                            # C[(mask, j)] = (cost, predecessor of j)
    for j in range(1, n):
        C[(1 << j, j)] = (dist[0][j], 0)
    for size in range(2, n):          # subsets in order of size
        for subset in combinations(range(1, n), size):
            mask = sum(1 << k for k in subset)
            for j in subset:
                rest = mask & ~(1 << j)
                C[(mask, j)] = min((C[(rest, k)][0] + dist[k][j], k)
                                   for k in subset if k != j)
    full = (1 << n) - 2               # every city except 0
    cost, j = min((C[(full, j)][0] + dist[j][0], j) for j in range(1, n))
    tour, mask = [0], full
    while j != 0:                     # follow stored predecessors back to the start
        tour.append(j)
        mask, j = mask & ~(1 << j), C[(mask, j)][1]
    tour.append(0)
    return cost, tour[::-1]
```

**Complexity and limits.** There are $O(n\,2^n)$ states and each takes $O(n)$ to evaluate, so the
time is $O(n^2 2^n)$ and the memory is $O(n\,2^n)$. For $n = 20$: about $4 \times 10^8$ basic steps
and $2 \times 10^7$ table entries (roughly 160 MB as 8-byte floats) — feasible in C++ with a flat
array `dp[1 << n][n]`, not in this dictionary-based Python, which is for $n \lesssim 15$. Compared
with brute force over $(n-1)!/2 \approx 6 \times 10^{16}$ tours at $n = 20$, that is a giant win, but
it is still exponential: TSP is NP-hard, and no known exact algorithm is polynomial. Beyond a few
dozen cities, practice uses heuristics (nearest neighbour + 2-opt), approximation (Christofides for
metric instances), or integer-programming solvers. The same bitmask-over-subsets pattern appears
in interview problems about assigning $n \le 20$ tasks, covering all nodes, or ordering a small set
of waypoints; the robotics version is sequencing a handful of inspection or drilling points, where
$n$ is small enough for exact answers.

### 7. Bridge to robotics and RL

**The Bellman equation is DP over time.** Put the recipe on a finite-horizon decision problem.
Subproblem in words: $V_t(s)$ = best expected total reward obtainable from state $s$ with the
decisions at times $t, \dots, T-1$ still to make. The last-decision question becomes the *first*
decision: pick $a$ now, collect $r(s,a)$, and continue optimally from wherever you land. The
recurrence holds because the future after $t$ depends only on the state reached — the Markov
property is optimal substructure:

$$V_t(s) = \max_a \Big[ r(s,a) + \sum_{s'} p(s' \mid s, a)\, V_{t+1}(s') \Big], \qquad V_T(s) = 0$$

The evaluation order is backward in time; the reconstruction is the policy $\pi_t(s) = \arg\max_a$,
stored per cell like the coin in `min_coins`. One backward sweep costs $O(T\,\lvert S\rvert^2\lvert A\rvert)$
with dense transitions. For an infinite discounted horizon there is no final row to start from, so
you apply the same backup repeatedly until the values stop changing — **value iteration**, which
converges because the backup is a $\gamma$-contraction ([[02-foundations/rl-basics|7. RL Basics §3]]).

```python
def backward_induction(states, actions, step, reward, T):
    """Deterministic finite horizon. V[t][s]: best total reward from s at time t."""
    V = [{s: 0.0 for s in states} for _ in range(T + 1)]   # base case: V[T] = 0
    policy = [{} for _ in range(T)]
    for t in range(T - 1, -1, -1):                          # later times first
        for s in states:
            a = max(actions, key=lambda a: reward(s, a) + V[t + 1][step(s, a)])
            policy[t][s] = a
            V[t][s] = reward(s, a) + V[t + 1][step(s, a)]
    return V, policy
```

For a deterministic model this is literally §6's DAG shortest path on the *time-expanded graph*
whose nodes are $(t, s)$. Three consequences worth saying in a research interview:

- **The curse of dimensionality** (Bellman's own phrase) is the table size. Discretize a 6-DoF arm
  at 100 bins per joint and the state table has $100^6 = 10^{12}$ entries before velocities. That is
  why tabular DP stays on small or low-dimensional problems, and why deep RL replaces the table
  with a function approximator — and inherits instability the table never had.
- **LQR is DP with a closed-form value function.** For linear dynamics and quadratic cost, $V_t$ is
  quadratic, the max is solved analytically, and the backward sweep over the table becomes the
  Riccati recursion over one matrix per time step ([[04-robotics/lqr-lqg|6. LQR / LQG]]).
- **Graph-search planners are DP with a smart order.** Dijkstra and A* compute cost-to-go or
  cost-to-come on graphs that have cycles, where no topological order exists, by settling nodes
  in order of cost instead.

**Dynamic time warping (DTW): edit distance for trajectories.** Two demonstrations of the same
insertion or trowelling motion rarely have the same timing: one operator pauses, another rushes the
approach. Comparing them sample-by-sample penalizes timing rather than shape. DTW finds the monotone
alignment of the two time series that minimizes total local distance. Subproblem: $D(i,j)$ = cost of
the best alignment of $x_{1..i}$ with $y_{1..j}$ that pairs $x_i$ with $y_j$. The previous pair was
one step back in $x$, in $y$, or in both, so

$$D(i,j) = d(x_i, y_j) + \min\big(D(i-1,j),\ D(i,j-1),\ D(i-1,j-1)\big), \qquad D(0,0) = 0$$

with all other border cells at $+\infty$. The shape is the edit-distance table, with two
differences: there is no fixed insertion or deletion cost — "waiting" on one series costs the local
distance $d$ of the repeated pairing — and every sample must be matched to at least one sample of
the other series. Sakoe and Chiba (1978) introduced it for spoken-word recognition and added two
constraints that matter in practice: an **adjustment window** $\lvert i - j\rvert \le r$, which cuts
the cost from $O(nm)$ to $O(n r)$ and forbids pathological warps where one sample absorbs half the
other trajectory, and slope constraints; their symmetric form also weights the diagonal step
double and normalizes by $n + m$ so that sequences of different lengths are comparable.

```python
def dtw(x, y, band=None, d=lambda p, q: abs(p - q)):
    n, m = len(x), len(y)
    r = max(n, m) if band is None else max(band, abs(n - m))   # window must reach (n, m)
    INF = float("inf")
    D = [ [INF] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(1, n + 1):
        for j in range(max(1, i - r), min(m, i + r) + 1):      # Sakoe-Chiba window
            D[i][j] = d(x[i - 1], y[j - 1]) + min(D[i - 1][j],      # x advances
                                                  D[i][j - 1],      # y advances
                                                  D[i - 1][j - 1])  # both advance
    return D[n][m]
```

For example `dtw([0, 1, 2, 1, 0], [0, 0, 1, 1, 2, 2, 1, 0])` is $0$: the second series is the first
played slower, a comparison plain Euclidean distance cannot even make since the lengths differ.
Uses in robot learning: aligning several kinesthetic demonstrations to a common time base before
averaging them into a reference trajectory, comparing an executed trajectory against its
reference, and matching force profiles across trials. Three cautions: DTW is **not a metric** (the
triangle inequality can fail, so do not feed it to methods that assume one); it aligns *time* only,
so remove spatial offsets and choose units for $d$ first (position and orientation need weights);
and an unconstrained warp can make two genuinely different motions look identical, which is what
the window is for.

### 8. Interview pitfalls

- **Off-by-one table sizes.** Prefix DPs need $n+1$ rows because the empty prefix is a real
  subproblem; `dp[i]` then refers to element `xs[i - 1]`. Mixing "first $i$ items" with "item $i$"
  is the most common bug in knapsack, edit distance and LCS. Write the subproblem sentence as a
  comment above the table.
- **Base cases that encode the wrong thing.** Counting problems start at `ways[0] = 1`, not 0;
  minimization starts unreachable cells at infinity, not 0. In C++, `INT_MAX + 1` overflows — use
  a large finite sentinel such as `1e9` or check before adding.
- **Wrong iteration order.** 0/1 knapsack in one row goes *downward* over capacity; unbounded goes
  *upward*. Coin combinations put coins in the outer loop; orderings put amounts outer. Check the
  order by asking, for each cell, "has everything I read already been written, and written with
  the meaning I want?"
- **Forgetting reconstruction.** Many problems ask for the subset, alignment or path, not the
  number. Plan for it at the start: keep the full table or a parent array. A rolling array cannot
  reconstruct.
- **A state that forgets information.** If the recurrence needs to know something the index does
  not record — cities visited, whether a stock is held, the previous choice — add it to the state
  and re-count the states.
- **Answer location.** LIS ends anywhere (take the max over $i$); knapsack's answer is $V[n][W]$
  only because the table means "capacity at most $x$".
- **Recursion limits and unhashable arguments in Python.** `functools.cache` needs hashable
  arguments (pass tuples, not lists), and deep top-down recursion hits the 1000-frame default; go
  bottom-up for $n$ in the thousands.
- **Trusting a greedy hunch.** Before committing to greedy, brute-force tiny inputs and compare. A
  two-line counterexample such as coins $\{1,3,4\}$ for $6$ ends the discussion.
- **State the complexity from the table.** Number of states × transitions per state, plus the
  pseudo-polynomial caveat when a dimension is a numeric value rather than a count.

### Self-check

1. Coins $\{1, 5, 6, 9\}$, target $11$. What does the largest-coin-first greedy return, and what is
   the optimum?
2. A candidate writes the 1-D 0/1 knapsack with the capacity loop running upward. What does it
   return for a single item (weight 3, value 5) and capacity 6, and why?
3. Why does an $O(nW)$ knapsack algorithm not show that P = NP?
4. Compute the edit distance between `arm` and `ram` and give one optimal alignment.
5. Run patience sorting on $[2, 5, 3, 7, 11, 8, 10, 13, 6]$. What is the LIS length, what is the
   final `tails` array, and is `tails` itself an increasing subsequence of the input?
6. Why does Held–Karp's state need the *set* of visited cities, and why does it not need their
   order?
7. Name two differences between DTW and edit distance, and one reason to use an adjustment window.
8. Apply the 4-step recipe of §1 to finite-horizon value iteration: what are the subproblem, the
   evaluation order, the base case and the reconstruction?

> [!tip]- Answers
> 1. Greedy takes $9$, then $1$, then $1$: three coins. The optimum is $5 + 6$: two coins. The DP finds it because at $a = 11$ it tries every last coin, including $6$, and $f(5) = 1$.
> 2. It returns $10$. With the upward loop, `best[3]` becomes $5$ during the item's own pass, and then `best[6]` reads that updated `best[3]` and adds the item again — the item is used twice, which is the unbounded rule. Running the loop downward reads `best[3]` before it is updated and returns $5$.
> 3. Polynomial time means polynomial in the input length. $W$ takes only $O(\log W)$ bits, so $O(nW)$ is exponential in the size of the number $W$. The algorithm is pseudo-polynomial: fast when the numbers are small, not polynomial in general.
> 4. Distance $2$. One alignment: `-arm` over `ra-m` — insert r, match a, delete r, match m, which is 2 operations. Substituting both first letters (`arm` over `ram`: a → r, r → a, match m) also costs 2.
> 5. `tails` evolves $[2] \to [2,5] \to [2,3] \to [2,3,7] \to [2,3,7,11] \to [2,3,7,8] \to [2,3,7,8,10] \to [2,3,7,8,10,13] \to [2,3,6,8,10,13]$. Length $6$ (for example $2, 3, 7, 8, 10, 13$). The final `tails` is not a subsequence: $6$ comes after $8$, $10$ and $13$ in the input.
> 6. Extending a path to city $j$ is legal only if $j$ has not been visited, so the subproblem must know which cities are used; without that it would glue together paths that revisit cities (§1's failure of optimal substructure). The order is irrelevant because the cost of finishing the tour from $j$ depends only on which cities remain and where you stand, not on how you got there. That is what reduces $n!$ orderings to $2^n$ subsets.
> 7. DTW has no fixed insert or delete cost — a repeated match costs the local distance — and it forces every sample to be matched; edit distance charges a constant per operation and may delete elements outright. DTW's local cost is a real-valued distance, not a match/mismatch indicator. The window $\lvert i-j\rvert \le r$ cuts the cost to $O(nr)$ and prevents degenerate warps that make different motions look alike.
> 8. Subproblem: $V_t(s)$, the best total reward from state $s$ with decisions $t, \dots, T-1$ left. Order: $t$ from $T-1$ down to $0$. Base case: $V_T(s) = 0$ (or a terminal reward). Reconstruction: store $\arg\max_a$ per $(t, s)$, which is the optimal policy.

### Sources

- Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.), dynamic-programming chapter. MIT Press.
- Roughgarden, T. (2019). *Algorithms Illuminated, Part 3: Greedy Algorithms and Dynamic Programming*; (2020) *Part 4: Algorithms for NP-Hard Problems*. Soundlikeyourself Publishing.
- Kulikov, A., & Pevzner, P. (2018). *Learning Algorithms Through Programming and Puzzle Solving*, dynamic-programming chapter. Active Learning Technologies.
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707–710.
- Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168–173.
- Fredman, M. L. (1975). On computing the length of longest increasing subsequences. *Discrete Mathematics*, 11(1), 29–35.
- Held, M., & Karp, R. M. (1962). A dynamic programming approach to sequencing problems. *Journal of the Society for Industrial and Applied Mathematics*, 10(1), 196–210. https://doi.org/10.1137/0110015
- Bellman, R. (1962). Dynamic programming treatment of the travelling salesman problem. *Journal of the ACM*, 9(1), 61–63.
- Sakoe, H., & Chiba, S. (1978). Dynamic programming algorithm optimization for spoken word recognition. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 26(1), 43–49. https://doi.org/10.1109/TASSP.1978.1163055
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.), ch. 4. MIT Press.

## 한국어

동적 계획법(DP)은 면접관이 알고리즘을 *외웠는지*가 아니라 *설계할 수 있는지*를 보고 싶을 때
꺼내는 기법이다. 동전, 문자열, 배낭, 부분 수열, 순회 경로처럼 겉모습은 다르지만 할 일은 늘
같다. 부분 문제의 집합에 이름을 붙이고, 각 부분 문제를 더 작은 것들과 관계 짓고, 그 관계를
어기지 않는 순서로 표를 채운 다음, 표를 거꾸로 따라가 비용뿐 아니라 실제 선택까지 복원한다.
연구실 면접은 한 가지를 더 묻는다. *이게 로보틱스 어디에 나오는가?* 정직한 답은 가치 반복(벨만
방정식은 시간 축 위의 DP다)과 시연 궤적 비교를 위한 동적 시간 와핑이며, 둘 다 §7에 있다.

> [!note] 처음이라면 · First pass
> §1과 §2를 천천히 읽는다. 레시피와 두 가지 구현 방식은 이후 모든 절이 다시 쓴다. 그다음 코드를 열어 두고 §3과 §4를 푼다. §5와 §6은 면접 전에 다시 볼 패턴 모음이고, §8은 전날 밤에 읽을 점검표다.

### 1. DP가 적용되는 조건, 그리고 이웃 기법과의 차이

DP에는 두 성질이 필요하다.

- **최적 부분 구조.** 전체 문제의 최적해가 *같은* 문제의 더 작은 사례에 대한 최적해를 품고
  있다. 증명은 거의 언제나 잘라 붙이기 논법이다. 최적해 안의 조각이 최적이 아니라면 더 나은
  조각으로 바꿔 끼워 전체가 좋아지므로 모순이다.
- **겹치는 부분 문제.** 자연스러운 재귀가 같은 작은 질문을 여러 번 묻는다. 그래서 캐시가
  이득이 된다. *서로 다른* 부분 문제가 몇천 개뿐인 문제도 재귀 트리는 수십억 노드가 될 수 있다.

**이웃 기법과의 차이.**

| 패러다임 | 부분 문제 | 각 단계의 선택 | 전형적 증명 |
|---|---|---|---|
| 분할 정복 | 서로소(병합 정렬의 두 반쪽은 작업을 공유하지 않는다) | 없음 — 분할이 고정 | 점화식 / 마스터 정리 |
| 탐욕 | 남는 부분 문제가 하나 | 국소 최선 하나에 확정하고 되돌아보지 않음 | 교환 논법: 탐욕 선택이 어떤 최적해에 들어 있음 |
| 동적 계획법 | 겹치며 여러 번 재사용 | 마지막 결정의 모든 선택지를 시도해 최선을 남김 | 잘라 붙이기 + 부분 문제 크기에 대한 귀납 |

이렇게 기억하면 편하다. 탐욕은 선택지 하나로 충분함을 증명해 둔 DP이고, 분할 정복은 부분
문제가 우연히 반복되지 않아 캐시를 둬도 쓸 일이 없는 재귀다.

**최적 부분 구조가 깨지는 경우.** 사이클이 있는 그래프에서 두 정점 사이의 *가장 긴 단순 경로*를
생각하자. 중간 정점 $v$에서 자르면 두 반쪽이 각각 가장 긴 단순 경로일 필요가 없다. $s$에서
$v$까지의 최장 경로와 $v$에서 $t$까지의 최장 경로가 같은 정점을 쓸 수 있고, 이어 붙이면 단순성이
깨지기 때문이다. "$s$에서 $v$까지의 최장 경로"라는 부분 문제는 자기완결적이지 않다. 어떤
정점이 이미 쓰였는지 알아야 한다. §6의 Held–Karp가 바로 그 빠진 정보를 상태에 넣은 결과이고,
그래서 상태 수가 지수적으로 커진다.

**4단계 레시피.** 면접에서는 각 단계를 소리 내어 말한다.

1. **부분 문제를 말로 정의한다.** "$f(i)$는 합이 정확히 $i$가 되는 최소 동전 수." 한 문장으로
   말하지 못하면 점화식도 틀린다.
2. **점화식을 쓴다.** *마지막 결정이 무엇이었나?*를 묻는다 — 마지막 동전, 마지막 물건을
   넣었는지, 정렬의 마지막 열에 무엇이 있는지. 선택지마다 경우 하나를 두고 min/max/합을 취한다.
3. **기저 사례와 계산 순서를 정한다.** 각 칸이 필요로 하는 값이 이미 계산되어 있는 순서여야
   한다. 복잡도 = (부분 문제 수) × (부분 문제당 작업량).
4. **복원한다.** 칸마다 이긴 선택을 저장하거나, 완성된 표에서 어느 경우가 그 값을 만들었는지
   확인해 다시 유도한다.

### 2. 하향식 메모이제이션 vs 상향식 테이블 채우기

같은 점화식을 두 방식으로 돌릴 수 있다.

- **하향식(메모이제이션):** 재귀를 그대로 쓰고, 각 결과를 처음 계산할 때 캐시한다. 실제로 도달한
  부분 문제만 풀고 순서는 알아서 정해진다. 대가는 함수 호출 오버헤드와 파이썬 재귀 한도(기본
  깊이 1000)다.
- **상향식(테이블):** 표를 할당하고 명시적인 순서로 채운다. 재귀가 없고 캐시 지역성이 좋으며,
  루프 구조가 복잡도를 바로 보여 준다. 순서는 직접 찾아야 한다.

> [!example] 계산 예제 · Worked example
> 로봇이 바닥 칸으로 된 격자를 왼쪽 위에서 오른쪽 아래로 오른쪽 또는 아래로만 이동해 가로지른다. 칸마다 통과 비용이 있다. 격자 행: $[2, 1, 4]$, $[3, 9, 1]$, $[4, 2, 2]$. 부분 문제: $f(r,c)$ = 그 칸을 포함해 $(r,c)$에 도달하는 최소 비용. 마지막 이동은 위 또는 왼쪽에서 왔으므로 $f(r,c) = \text{cost}(r,c) + \min(f(r-1,c),\, f(r,c-1))$. 행 순서로 채우면 $[2, 3, 7]$, $[5, 12, 8]$, $[9, 11, 10]$이고, 답은 $2 \to 1 \to 4 \to 1 \to 2$ 경로의 $10$이다. 캐시가 없으면 재귀는 칸 $(r,c)$에 이르는 단조 경로마다 한 번씩, 즉 $\binom{r+c}{r}$번 그 칸에 도달한다. 캐시가 있으면 9개 칸을 각각 한 번만 푼다.

```python
from functools import cache

def min_path_topdown(cost):
    rows, cols = len(cost), len(cost[0])

    @cache
    def f(r, c):                      # cheapest cost from (0, 0) to (r, c), inclusive
        if r == 0 and c == 0:
            return cost[0][0]
        best = float("inf")
        if r > 0:
            best = min(best, f(r - 1, c))
        if c > 0:
            best = min(best, f(r, c - 1))
        return best + cost[r][c]

    return f(rows - 1, cols - 1)


def min_path_bottomup(cost):
    rows, cols = len(cost), len(cost[0])
    INF = float("inf")
    dp = [0] + [INF] * (cols - 1)     # one rolling row instead of a rows x cols table
    for r in range(rows):
        for c in range(cols):
            left = dp[c - 1] if c > 0 else INF
            dp[c] = min(dp[c], left) + cost[r][c]   # dp[c] still holds the row above
    return dp[-1]
```

**롤링 배열로 공간 줄이기.** 행 $r$이 행 $r-1$(과 같은 행의 왼쪽 칸)만 읽는다면 한 행만 두면
된다. `dp[c]`는 덮어쓰기 직전까지 위 행의 값을 갖고 있고, `dp[c - 1]`은 이미 현재 행 값으로
갱신되어 있다. 메모리가 $O(\text{rows}\cdot\text{cols})$에서 $O(\text{cols})$로 준다. 대가는
복원이다. 행을 덮어쓰면 그 행이 기록한 선택은 사라진다. 경로가 필요하면 표 전체를 두거나,
부모 포인터를 저장하거나, 분할 정복 기법(정렬 문제의 Hirschberg 방법)을 쓴다.

**무엇을 쓸까.** 면접에서 순서가 뻔하지 않거나(트리, 구간, 비트마스크) 대부분의 상태에 도달하지
않을 때는 하향식이 올바르게 빨리 쓰기 쉽다. 순서가 단순한 루프이고 롤링 배열로 메모리를 아끼고
싶을 때는 상향식이 기본이다. C++에서 하향식 메모는 보통 `std::map`이 아니라 "미계산" 표시값을
둔 `std::vector`로 상태를 인덱싱한다. `std::map`은 훨씬 느리다.

### 3. 1차원 DP

**계단 오르기 / 경로 수 세기.** 한 번에 1칸 또는 2칸 오를 수 있다면 $n$번째 칸에 이르는 방법
수는 $w(n) = w(n-1) + w(n-2)$, $w(0) = 1$이다. 마지막 이동이 1칸이거나 2칸이기 때문이다.
피보나치 점화식이며, 아래의 "동전 $\{1, 2\}$로 거스름돈을 만드는 순서 있는 방법 수" 코드와 같다.

**동전 교환 — 최소 동전 수.** 부분 문제: $f(a)$ = 합이 정확히 $a$인 최소 동전 수. 마지막 동전은
어떤 $c \le a$이고, 그 동전을 빼면 $a - c$에 대한 최적해가 남으므로(잘라 붙이기) 아래 점화식이
성립한다.

$$f(a) = 1 + \min_{c \in \text{coins},\ c \le a} f(a - c), \qquad f(0) = 0$$

액면 $k$종류일 때 복잡도는 $O(a \cdot k)$다.

> [!example] 계산 예제 · Worked example
> 동전 $\{1, 3, 4\}$, 목표 $6$. 탐욕은 들어가는 가장 큰 동전을 고른다. $4$, $1$, $1$로 **세 개**다. DP: $f(0..6) = 0, 1, 2, 1, 1, 2, 2$. $a = 6$에서 선택지는 $f(5)+1 = 3$(마지막 동전 1), $f(3)+1 = 2$(마지막 동전 3), $f(2)+1 = 3$(마지막 동전 4)이므로 $f(6) = 2$, 즉 $3 + 3$이다. 탐욕이 실패하는 이유는 $4$를 집으면 남는 $2$를 다른 동전들이 나쁘게 채우기 때문이고, 어떤 국소 규칙도 그것을 보지 못한다. $\{1, 5, 10, 25\}$ 같은 "정규" 체계에서는 탐욕이 최적이지만, 그건 액면 구성의 성질이며 따로 증명해야 한다.

```python
def min_coins(coins, target):
    INF = float("inf")
    best = [0] + [INF] * target       # best[a]: fewest coins summing to exactly a
    last = [None] * (target + 1)      # last[a]: the final coin of one optimal answer
    for a in range(1, target + 1):
        for c in coins:
            if c <= a and best[a - c] + 1 < best[a]:
                best[a], last[a] = best[a - c] + 1, c
    if best[target] == INF:
        return None                   # target cannot be formed
    used, a = [], target
    while a > 0:                      # reconstruction: peel off the recorded last coin
        used.append(last[a])
        a -= last[a]
    return used
```

**동전 교환 — 방법 수.** 이제 $g(a)$는 개수를 세고, 기저 사례는 $g(0) = 1$이다(0을 만드는
방법은 아무것도 안 고르는 한 가지). 미묘한 부분은 *무엇을 다른 방법으로 치느냐*이고, 이는
오직 루프 순서로 결정된다.

```python
def count_combinations(coins, target):   # 1+3 and 3+1 are the same way
    ways = [1] + [0] * target
    for c in coins:                       # coins outer: each multiset is built in one order
        for a in range(c, target + 1):
            ways[a] += ways[a - c]
    return ways[target]


def count_orderings(coins, target):      # 1+3 and 3+1 are different ways
    ways = [1] + [0] * target
    for a in range(1, target + 1):        # amount outer: any coin may come last
        for c in coins:
            if c <= a:
                ways[a] += ways[a - c]
    return ways[target]
```

동전을 바깥 루프에 두면, 동전 $c$를 처리하는 시점에 표의 모든 값은 목록에서 앞선 동전만 쓴다.
그래서 각 중복집합이 목록 순서대로 한 번만 세어진다. 금액을 바깥에 두면 마지막 동전이 모든
액면을 돌므로 순서열이 세어진다. $\{1, 3, 4\}$와 $6$이면 조합은 $4$가지($1^6$, $3+1^3$, $3+3$,
$4+1+1$)지만 순서열은 $9$가지다. `count_orderings([1, 2], n)`이 계단 오르기다.

**경로 그래프의 최대 가중 독립 집합.** 일렬로 놓인 정점 $v_1, \dots, v_n$에 가중치 $w_i \ge 0$이
있다. 서로 이웃하지 않는 정점들을 골라 가중치 합을 최대로 한다. 부분 문제: $A[i]$ = 앞의 $i$개
정점만 쓸 때의 최선 합. $v_i$가 최적해에 없으면 최적값은 $A[i-1]$이고, 있으면 $v_{i-1}$은
빠지며 나머지는 앞 $i-2$개에 대한 최적해다. 따라서 점화식은 $A[i] = \max(A[i-1],\ A[i-2] + w_i)$,
$A[0] = 0$, $A[1] = w_1$이다. 시간 $O(n)$.

> [!example] 계산 예제 · Worked example
> 가중치 $[3, 2, 5, 10, 7]$. $A = 0, 3, 3, 8, 13, 15$. 복원은 뒤에서부터 걷는다. $A[5] = 15 \ne A[4] = 13$이므로 $v_5$를 넣고 $i = 3$으로 건너뛴다. $A[3] = 8 \ne A[2]$이므로 $v_3$을 넣고 $i = 1$로. $A[1] = 3 \ne A[0]$이므로 $v_1$을 넣는다. 답은 $\{v_1, v_3, v_5\}$, 가중치 $15$다. 탐욕(아직 허용되는 가장 무거운 정점 고르기)은 $10$을 집어 $5$와 $7$을 막고, 이어 $3$을 집어 합계 $13$이 된다.

```python
def max_weight_independent_set(w):
    n = len(w)
    A = [0] * (n + 1)                 # A[i]: best total using the first i vertices
    if n:
        A[1] = w[0]
    for i in range(2, n + 1):
        A[i] = max(A[i - 1], A[i - 2] + w[i - 1])
    chosen, i = [], n
    while i >= 1:                     # if skipping vertex i loses nothing, skip it
        if A[i] == A[i - 1]:
            i -= 1
        else:                         # vertex i must be in this optimum
            chosen.append(i - 1)
            i -= 2
    return A[n], chosen[::-1]         # 0-based indices
```

복원에 추가 저장 공간이 필요 없다. 완성된 표가 어느 경우가 이겼는지 이미 말해 준다.

### 4. 2차원 DP

**0/1 배낭.** 정수 무게 $w_i$와 가치 $v_i$를 가진 물건 $n$개, 용량 $W$. 각 물건은 최대 한 번.
부분 문제: $V[i][x]$ = 앞의 $i$개 물건만 쓰고 용량이 $x$일 때의 최대 가치. 물건 $i$는 빼거나
넣는데, 넣는 경우 나머지 물건들은 용량 $x - w_i$에 대해 최적이어야 하므로

$$V[i][x] = \max\big(V[i-1][x],\ V[i-1][x - w_i] + v_i\big), \qquad V[0][x] = 0$$

이고 두 번째 선택지는 $w_i \le x$일 때만 존재한다. 칸이 $(n+1)(W+1)$개이고 각각 $O(1)$이므로
시간은 $O(nW)$다.

```python
def knapsack_01(items, W):            # items: list of (weight, value), integer weights
    n = len(items)
    V = [ [0] * (W + 1) for _ in range(n + 1)]   # V[i][x]: first i items, capacity x
    for i in range(1, n + 1):
        w, v = items[i - 1]
        for x in range(W + 1):
            V[i][x] = V[i - 1][x]
            if w <= x:
                V[i][x] = max(V[i][x], V[i - 1][x - w] + v)
    take, x = [], W
    for i in range(n, 0, -1):         # item i was taken iff it changed the value
        if V[i][x] != V[i - 1][x]:
            take.append(i - 1)
            x -= items[i - 1][0]
    return V[n][W], take[::-1]
```

> [!example] 계산 예제 · Worked example
> 물건(무게, 가치): $(1,1), (3,4), (4,5), (5,7)$, 용량 $7$. 가치 밀도 탐욕은 $(5,7)$(밀도 $1.4$)을 넣고, $(3,4)$와 $(4,5)$는 들어가지 않으니 $(1,1)$을 더해 가치 $8$이다. 표는 용량을 정확히 채우는 $(3,4) + (4,5)$로 $V[4][7] = 9$를 준다. 복원: $V[4][7] = V[3][7] = 9$이므로 물건 4는 필요 없다. $V[3][7] = 9 \ne V[2][7] = 5$이므로 물건 3을 넣고 $x = 3$으로. $V[2][3] = 4 \ne V[1][3] = 1$이므로 물건 2를 넣고 $x = 0$. 밀도 탐욕은 마지막 물건을 쪼갤 수 있는 *분할* 배낭에서만 최적이다.

**$O(nW)$가 의사 다항식인 이유.** "다항 시간"은 *입력 길이*에 대한 다항식이라는 뜻이다. 용량 $W$는
약 $\log_2 W$비트로 적히므로 $W = 2^{\text{bits}}$는 자기 표현 길이에 대해 지수적이다. $n = 100$,
$W = 10^9$이면 입력은 몇 킬로바이트인데 표는 $10^{11}$칸이다. 이는 0/1 배낭이 NP-난해라는 사실과
모순되지 않는다. DP는 수가 작을 때만 빠르다. 실용적 결과 두 가지. 모든 무게를 최대공약수로
나누면 $W$가 공짜로 줄어든다. 가치는 작고 무게가 거대하면 역할을 바꿔, 표를 *가치*로 인덱싱하고
그 가치를 달성하는 최소 무게를 저장한다.

**배낭을 1차원으로 굴리기 — 그리고 루프 방향의 함정.**

```python
def knapsack_01_1d(items, W):
    best = [0] * (W + 1)
    for w, v in items:
        for x in range(W, w - 1, -1):    # downward: best[x - w] still excludes this item
            best[x] = max(best[x], best[x - w] + v)
    return best[W]


def knapsack_unbounded(items, W):
    best = [0] * (W + 1)
    for w, v in items:
        for x in range(w, W + 1):        # upward: best[x - w] may already include it
            best[x] = max(best[x], best[x - w] + v)
    return best[W]
```

두 함수는 안쪽 루프의 방향만 다르다. 내려가며 돌면 `best[x - w]`는 이 물건의 패스가 건드리기
전에 읽히므로 여전히 "이전 물건만"을 뜻한다 — 0/1 규칙. 올라가며 돌면 `best[x - w]`는 이미 이
패스에서 갱신되어 그 물건을 포함할 수 있으므로 물건을 재사용하게 된다 — 무제한 규칙. 물건
$(2, 3)$ 하나와 $W = 4$라면 내림차순은 $3$, 오름차순은 $6$을 준다.

**편집 거리(Levenshtein).** 문자열 $a$를 $b$로 바꾸는 단일 문자 삽입·삭제·치환의 최소 횟수.
부분 문제: $D[i][j]$ = 접두사 $a[:i]$와 $b[:j]$ 사이의 거리. 최적 정렬의 마지막 열은 $a_i$를
삭제하거나, $b_j$를 삽입하거나, $a_i$와 $b_j$를 짝짓는다(같으면 0, 다르면 1). 따라서

$$D[i][j] = \min\big(D[i-1][j] + 1,\ D[i][j-1] + 1,\ D[i-1][j-1] + [a_i \ne b_j]\big)$$

이고, 빈 접두사에는 전부 삭제하거나 전부 삽입해야만 도달하므로 $D[i][0] = i$, $D[0][j] = j$다.
시간과 공간은 $O(nm)$이며, 수치만 필요하면 두 행을 굴려 공간 $O(\min(n,m))$로 줄인다.

> [!example] 계산 예제 · Worked example
> $a = \texttt{robot}$, $b = \texttt{orbit}$. 행은 $a$의 접두사, 열은 $b$의 접두사다.
>
> | | ε | o | r | b | i | t |
> |---|---|---|---|---|---|---|
> | ε | 0 | 1 | 2 | 3 | 4 | 5 |
> | r | 1 | 1 | 1 | 2 | 3 | 4 |
> | o | 2 | 1 | 2 | 2 | 3 | 4 |
> | b | 3 | 2 | 2 | 2 | 3 | 4 |
> | o | 4 | 3 | 3 | 3 | 3 | 4 |
> | t | 5 | 4 | 4 | 4 | 4 | 3 |
>
> 거리는 $D[5][5] = 3$이다. 모서리에서 역추적: $D[5][5] = 3 = D[4][4] + 0$($t = t$), 대각선으로. $D[4][4] = 3 = D[3][3] + 1$(o → i), 대각선. $D[3][3] = 2 = D[2][2] + 0$($b = b$). $D[2][2] = 2 = D[1][1] + 1$(o → r). $D[1][1] = 1 = D[0][0] + 1$(r → o). 정렬은 `robot` / `orbit`, 치환 세 번이다. 동점이면 다른 최적 정렬도 나온다. `-robot` 위 `or-bit`(o 삽입, r 일치, o 삭제, b 일치, o → i 치환, t 일치)도 비용 3이다. 면접관은 어느 것이든 받아 주니, 코드가 어떤 동점 규칙을 쓰는지 말하면 된다.

```python
def edit_distance(a, b):
    n, m = len(a), len(b)
    D = [ [0] * (m + 1) for _ in range(n + 1)]   # D[i][j]: cost of turning a[:i] into b[:j]
    for i in range(n + 1):
        D[i][0] = i                              # delete everything
    for j in range(m + 1):
        D[0][j] = j                              # insert everything
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1,                           # delete a[i-1]
                          D[i][j - 1] + 1,                           # insert b[j-1]
                          D[i - 1][j - 1] + (a[i - 1] != b[j - 1]))  # match or substitute
    pairs, i, j = [], n, m                       # backtrace from the bottom-right corner
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            pairs.append((a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            pairs.append((a[i - 1], "-"))
            i -= 1
        else:
            pairs.append(("-", b[j - 1]))
            j -= 1
    pairs.reverse()
    return D[n][m], "".join(p for p, _ in pairs), "".join(q for _, q in pairs)
```

이 표는 변장한 DAG다. 각 칸은 위·왼쪽·왼쪽 위 이웃에서 들어오는 간선을 가진 노드이고, 거리는
왼쪽 위 모서리에서 오른쪽 아래 모서리까지의 최단 경로다. 가중 변형(치환마다 다른 비용, 아핀 갭
벌점)은 간선 가중치만 바꾸며, 생물정보학의 서열 정렬이 바로 그것이다.

**최장 공통 부분 수열(LCS).** $a$와 $b$ 모두에 순서대로(연속일 필요는 없이) 나타나는 가장 긴
수열. 부분 문제: $L[i][j]$ = $a[:i]$와 $b[:j]$의 LCS 길이. $a_i = b_j$이면 둘을 짝지어 끝나는
LCS가 존재한다(그렇지 않은 LCS도 짧아지지 않게 그렇게 고칠 수 있다). 그래서
$L[i][j] = L[i-1][j-1] + 1$이다. 다르면 마지막 두 원소 중 적어도 하나는 쓰이지 않으므로
$L[i][j] = \max(L[i-1][j], L[i][j-1])$이다. 기저 사례는 0이다. $O(nm)$.

```python
def lcs(a, b):
    n, m = len(a), len(b)
    L = [ [0] * (m + 1) for _ in range(n + 1)]   # L[i][j]: LCS length of a[:i] and b[:j]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    out, i, j = [], n, m
    while i > 0 and j > 0:                       # walk back along the cells that won
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i, j = i - 1, j - 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return out[::-1]
```

문자열뿐 아니라 어떤 수열에도 쓸 수 있다. 동작 프리미티브로 기록한 두 시연 로그
`[reach, grasp, lift, move, place, release]`와 `[reach, push, grasp, move, lift, place, release]`는
`[reach, grasp, lift, place, release]` 같은 길이 5의 LCS를 공유한다. 두 작업 수행의 공통 골격이다.
LCS는 치환을 금지한 편집 거리다. 삽입·삭제만 허용한 거리는 $n + m - 2\,L[n][m]$인데, LCS 밖의
모든 원소는 $a$에서 삭제되거나 $b$에서 삽입되기 때문이다. 유닉스 `diff` 도구가 이 발상 위에
만들어졌다.

### 5. 수열 DP: 최장 증가 부분 수열

**$O(n^2)$ 버전.** 부분 문제: $e[i]$ = 인덱스 $i$에서 *끝나는* 가장 긴 순증가 부분 수열의 길이.
끝 인덱스를 고정해야 점화식이 가능해진다. $x_i$ 앞의 원소는 더 앞의 어떤 $x_j < x_i$이므로
$e[i] = 1 + \max\{e[j] : j < i,\ x_j < x_i\}$(그런 $j$가 없으면 $1$). 답은 $e[n-1]$이 아니라
$\max_i e[i]$다 — 흔한 실수다.

```python
def lis_quadratic(xs):
    n = len(xs)
    end = [1] * n                     # end[i]: longest increasing run that ends at i
    prev = [-1] * n                   # prev[i]: index before i in that run
    for i in range(n):
        for j in range(i):
            if xs[j] < xs[i] and end[j] + 1 > end[i]:
                end[i], prev[i] = end[j] + 1, j
    if n == 0:
        return []
    i = max(range(n), key=end.__getitem__)       # best end point, not necessarily n-1
    out = []
    while i != -1:
        out.append(xs[i])
        i = prev[i]
    return out[::-1]
```

**$O(n \log n)$ 인내 정렬(patience sorting) 버전.** `tails[k]` = 지금까지 본 길이 $k+1$ 증가 부분
수열의 마지막 값 중 가장 작은 것을 유지한다. 불변식은 `tails`가 순증가라는 것이다(길이 $k+2$
부분 수열은 마지막 값이 더 작은 길이 $k+1$ 부분 수열을 품는다). 새 $x$마다 `tails[k]` $\ge x$인
첫 위치를 이진 탐색한다. 그 자리를 $x$로 바꾸면 모든 길이의 꼬리가 가능한 한 작게 유지되고,
그런 $k$가 없으면 $x$가 가장 긴 부분 수열을 연장한다. 원소마다 이진 탐색 한 번이므로
$O(n \log n)$이다. 이름은 카드를 더미에 나눠 놓을 때 각 카드를 윗장이 자기보다 작지 않은 가장
왼쪽 더미에 올리는 게임에서 왔다. 더미 개수가 LIS 길이다.

> [!example] 계산 예제 · Worked example
> $xs = [3, 1, 4, 1, 5, 9, 2, 6]$. `tails`는 $[3] \to [1] \to [1,4] \to [1,4] \to [1,4,5] \to [1,4,5,9] \to [1,2,5,9] \to [1,2,5,6]$로 변한다. 길이 $4$. 최종 `tails` $= [1,2,5,6]$은 $xs$의 부분 수열이 **아니다** — $2$는 인덱스 6에 있어 인덱스 4의 $5$보다 뒤다. `tails`는 해가 아니라 *길이별 최선의 꼬리*를 저장한다. 해를 복원하려면 각 원소를 놓는 순간의 선행 원소를 기록해야 하고, 그러면 $[1, 4, 5, 6]$이 나온다.

```python
from bisect import bisect_left

def lis_patience(xs):
    tails, tail_idx = [], []          # tails[k]: smallest tail of an increasing run of length k+1
    prev = [-1] * len(xs)             # predecessor links, fixed when each element is placed
    for i, x in enumerate(xs):
        k = bisect_left(tails, x)     # first pile whose top is >= x
        if k == len(tails):
            tails.append(x)
            tail_idx.append(i)
        else:
            tails[k], tail_idx[k] = x, i
        prev[i] = tail_idx[k - 1] if k > 0 else -1
    out, i = [], (tail_idx[-1] if tail_idx else -1)
    while i != -1:
        out.append(xs[i])
        i = prev[i]
    return out[::-1]
```

`bisect_left`는 *순*증가를 준다. 비감소라면 `bisect_right`를 쓴다. C++에서는 같은 두 선택이
`std::lower_bound`와 `std::upper_bound`다.

### 6. 그래프와 비트마스크 위의 DP

**위상 순서로 DAG 최단 경로 구하기.** 방향 비순환 그래프에서 $d(v) = \min_{(u,v)} [d(u) + w(u,v)]$이고
최소는 들어오는 간선에 대해 취한다. 위상 순서가 *곧* 계산 순서다. $u$를 처리할 때 $u$로 들어오는
모든 경로는 이미 완화되었으므로 $d(u)$는 확정이다. 시간 $O(V + E)$로 Dijkstra보다 빠르고,
악용할 사이클이 없으니 음수 간선도 괜찮다. min을 max로 바꾸면(또는 가중치 부호를 뒤집으면)
DAG의 *최장* 경로가 되는데, 일반 그래프에서는 NP-난해다. 위의 모든 표 채우기 DP는 부분 문제를
노드로 하는 DAG 위의 최단 또는 최장 경로다. 그래서 "순서 찾기"와 "위상 정렬 찾기"는 같은
질문이다. 사이클을 다루는 Dijkstra와 Bellman–Ford는 그래프 페이지가 다루며, 계획 그래프에서의
쓰임은 [[04-robotics/planning-decision-making|4. 계획 §3]]을 보라.

```python
from collections import deque

def dag_shortest_paths(n, edges, source):    # edges: (u, v, weight); weights may be negative
    adj = [list() for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    order, q = [], deque(i for i in range(n) if indeg[i] == 0)
    while q:                                  # Kahn's algorithm gives a topological order
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        raise ValueError("graph has a cycle")
    dist, parent = [float("inf")] * n, [None] * n
    dist[source] = 0
    for u in order:                           # all predecessors of u are already final
        if dist[u] < float("inf"):
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v], parent[v] = dist[u] + w, u
    return dist, parent
```

**외판원 문제를 위한 Held–Karp.** 도시 $n$개를 정확히 한 번씩 방문하고 출발점으로 돌아오는 최소
비용 경로. §1에서 "$j$까지의 최단 경로"가 유효한 부분 문제가 아닌 이유를 봤다. 어느 도시를
방문했는지 잊어버린다. Held–Karp는 그 집합을 상태에 넣는다. $C(S, j)$ = 도시 0에서 출발해
$S$(0 제외)의 도시를 정확히 방문하고 $j \in S$에서 끝나는 최소 비용 경로. $j$ 직전 도시는 어떤
$k \in S \setminus \{j\}$이므로

$$C(S, j) = \min_{k \in S \setminus \{j\}} \big[ C(S \setminus \{j\}, k) + d(k, j) \big], \qquad C(\{j\}, j) = d(0, j)$$

이고 순회 비용은 $\min_j [C(\text{all}, j) + d(j, 0)]$이다. 상태는 *어느* 도시를 방문했는지는
기록하지만 *어떤 순서*였는지는 기록하지 않으며, 바로 그것이 $n!$을 줄인다. 각 부분집합은 원소가
하나 적은 부분집합만 읽으므로 크기 순서로 처리한다.

```python
from itertools import combinations

def held_karp(dist):                  # dist[i][j]: cost i -> j; the tour starts and ends at 0
    n = len(dist)
    if n == 1:
        return 0, [0, 0]
    C = {}                            # C[(mask, j)] = (cost, predecessor of j)
    for j in range(1, n):
        C[(1 << j, j)] = (dist[0][j], 0)
    for size in range(2, n):          # subsets in order of size
        for subset in combinations(range(1, n), size):
            mask = sum(1 << k for k in subset)
            for j in subset:
                rest = mask & ~(1 << j)
                C[(mask, j)] = min((C[(rest, k)][0] + dist[k][j], k)
                                   for k in subset if k != j)
    full = (1 << n) - 2               # every city except 0
    cost, j = min((C[(full, j)][0] + dist[j][0], j) for j in range(1, n))
    tour, mask = [0], full
    while j != 0:                     # follow stored predecessors back to the start
        tour.append(j)
        mask, j = mask & ~(1 << j), C[(mask, j)][1]
    tour.append(0)
    return cost, tour[::-1]
```

**복잡도와 한계.** 상태가 $O(n\,2^n)$개이고 각각 $O(n)$에 계산하므로 시간은 $O(n^2 2^n)$, 메모리는
$O(n\,2^n)$이다. $n = 20$이면 기본 연산 약 $4 \times 10^8$번, 표 항목 $2 \times 10^7$개(8바이트
실수로 약 160 MB)다. 평탄한 배열 `dp[1 << n][n]`을 쓰는 C++에서는 가능하지만, 이 딕셔너리 기반
파이썬 코드는 $n \lesssim 15$용이다. $n = 20$에서 $(n-1)!/2 \approx 6 \times 10^{16}$개 순회를
전수 조사하는 것에 비하면 엄청난 이득이지만 여전히 지수적이다. TSP는 NP-난해이며 다항 시간 정확
알고리즘은 알려져 있지 않다. 수십 개 도시를 넘으면 실무는 휴리스틱(최근접 이웃 + 2-opt), 근사(거리
공간 사례의 Christofides), 정수 계획 솔버를 쓴다. 같은 부분집합 비트마스크 패턴이 $n \le 20$개
작업 배정, 모든 노드 덮기, 소수 경유점 순서 정하기 같은 면접 문제에 나온다. 로보틱스 판은 몇 개
안 되는 점검·천공 지점의 순서를 정하는 일로, $n$이 작아 정확한 답을 낼 수 있다.

### 7. 로보틱스와 RL로 가는 다리

**벨만 방정식은 시간 축 위의 DP다.** 유한 지평 의사결정 문제에 레시피를 적용해 보자. 부분 문제를
말로 하면 $V_t(s)$ = 상태 $s$에서 시각 $t, \dots, T-1$의 결정이 남았을 때 얻을 수 있는 최대 기대
총보상이다. 마지막 결정을 묻던 질문이 여기서는 *첫* 결정이 된다. 지금 $a$를 골라 $r(s,a)$를 받고,
도착한 곳에서부터 최적으로 계속한다. $t$ 이후의 미래는 도달한 상태에만 의존하므로 점화식이
성립한다. 마르코프 성질이 곧 최적 부분 구조다.

$$V_t(s) = \max_a \Big[ r(s,a) + \sum_{s'} p(s' \mid s, a)\, V_{t+1}(s') \Big], \qquad V_T(s) = 0$$

계산 순서는 시간을 거꾸로 가는 것이고, 복원은 정책 $\pi_t(s) = \arg\max_a$이며 `min_coins`의
동전처럼 칸마다 저장한다. 조밀한 전이에서 역방향 한 번 훑기는 $O(T\,\lvert S\rvert^2\lvert A\rvert)$다.
무한 할인 지평에는 시작할 마지막 행이 없으므로 값이 변하지 않을 때까지 같은 백업을 반복 적용한다.
이것이 **가치 반복**이며, 백업이 $\gamma$-축약이라 수렴한다([[02-foundations/rl-basics|7. RL 기초 §3]]).

```python
def backward_induction(states, actions, step, reward, T):
    """Deterministic finite horizon. V[t][s]: best total reward from s at time t."""
    V = [{s: 0.0 for s in states} for _ in range(T + 1)]   # base case: V[T] = 0
    policy = [{} for _ in range(T)]
    for t in range(T - 1, -1, -1):                          # later times first
        for s in states:
            a = max(actions, key=lambda a: reward(s, a) + V[t + 1][step(s, a)])
            policy[t][s] = a
            V[t][s] = reward(s, a) + V[t + 1][step(s, a)]
    return V, policy
```

결정론적 모델이라면 이것은 노드가 $(t, s)$인 *시간 전개 그래프* 위에서 §6의 DAG 최단 경로를 푸는
것과 문자 그대로 같다. 연구 면접에서 말할 만한 결과 세 가지.

- **차원의 저주**(벨만 자신의 표현)는 표의 크기다. 6자유도 팔을 관절당 100칸으로 이산화하면 속도를
  넣기도 전에 상태 표가 $100^6 = 10^{12}$개 항목이다. 그래서 표 기반 DP는 작거나 저차원인 문제에
  머물고, 심층 RL은 표를 함수 근사기로 바꾸며 표에는 없던 불안정성을 물려받는다.
- **LQR은 가치 함수가 닫힌 형태인 DP다.** 선형 동역학과 이차 비용이면 $V_t$가 이차식이고 max가
  해석적으로 풀려, 표 위의 역방향 훑기가 시간 단계마다 행렬 하나를 갱신하는 리카티 재귀가 된다
  ([[04-robotics/lqr-lqg|6. LQR / LQG]]).
- **그래프 탐색 계획기는 순서를 영리하게 고른 DP다.** Dijkstra와 A*는 위상 순서가 없는, 사이클이
  있는 그래프에서 비용 순서로 노드를 확정하며 cost-to-go 또는 cost-to-come을 계산한다.

**동적 시간 와핑(DTW): 궤적을 위한 편집 거리.** 같은 삽입 동작이나 흙손질 동작의 두 시연은
타이밍이 거의 같지 않다. 한 작업자는 멈칫하고 다른 작업자는 접근을 서두른다. 표본끼리 그대로
비교하면 모양이 아니라 타이밍에 벌점을 준다. DTW는 두 시계열의 단조 정렬 중 국소 거리 총합이
최소인 것을 찾는다. 부분 문제: $D(i,j)$ = $x_i$와 $y_j$를 짝짓는, $x_{1..i}$와 $y_{1..j}$의 최선
정렬 비용. 직전 짝은 $x$에서 한 칸, $y$에서 한 칸, 또는 둘 다 한 칸 뒤였으므로

$$D(i,j) = d(x_i, y_j) + \min\big(D(i-1,j),\ D(i,j-1),\ D(i-1,j-1)\big), \qquad D(0,0) = 0$$

이고 나머지 경계 칸은 $+\infty$다. 모양은 편집 거리 표와 같지만 두 가지가 다르다. 고정된 삽입·삭제
비용이 없다 — 한 시계열에서 "기다리는" 비용은 반복된 짝의 국소 거리 $d$다. 그리고 모든 표본이 상대
시계열의 표본 하나 이상과 반드시 짝지어진다. Sakoe와 Chiba(1978)는 음성 단어 인식을 위해 이를
도입하며 실무에서 중요한 두 제약을 더했다. 비용을 $O(nm)$에서 $O(n r)$로 줄이고 한 표본이 상대
궤적의 절반을 삼키는 병적 와핑을 막는 **조정 창** $\lvert i - j\rvert \le r$, 그리고 기울기
제약이다. 그들의 대칭형은 대각선 이동에 가중치를 두 배로 주고 $n + m$으로 정규화해 길이가 다른
수열도 비교할 수 있게 한다.

```python
def dtw(x, y, band=None, d=lambda p, q: abs(p - q)):
    n, m = len(x), len(y)
    r = max(n, m) if band is None else max(band, abs(n - m))   # window must reach (n, m)
    INF = float("inf")
    D = [ [INF] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0.0
    for i in range(1, n + 1):
        for j in range(max(1, i - r), min(m, i + r) + 1):      # Sakoe-Chiba window
            D[i][j] = d(x[i - 1], y[j - 1]) + min(D[i - 1][j],      # x advances
                                                  D[i][j - 1],      # y advances
                                                  D[i - 1][j - 1])  # both advance
    return D[n][m]
```

예를 들어 `dtw([0, 1, 2, 1, 0], [0, 0, 1, 1, 2, 2, 1, 0])`은 $0$이다. 두 번째 시계열은 첫 번째를
느리게 재생한 것인데, 평범한 유클리드 거리는 길이가 달라 비교조차 못 한다. 로봇 학습에서의 쓰임:
여러 운동감각 교시 시연을 공통 시간축에 맞춘 뒤 평균 내어 기준 궤적을 만들기, 실행 궤적을 기준과
비교하기, 시행 간 힘 프로파일 맞추기. 주의 세 가지. DTW는 **거리 함수(metric)가 아니다**(삼각
부등식이 깨질 수 있으니 metric을 가정하는 방법에 넣지 말 것). *시간*만 정렬하므로 공간 오프셋을
먼저 제거하고 $d$의 단위를 정해야 한다(위치와 자세에는 가중치가 필요하다). 제약 없는 와핑은 실제로
다른 두 동작을 똑같아 보이게 만들 수 있고, 창이 그것을 막는다.

### 8. 면접 함정

- **표 크기의 off-by-one.** 접두사 DP는 빈 접두사도 진짜 부분 문제이므로 $n+1$행이 필요하고,
  그러면 `dp[i]`는 원소 `xs[i - 1]`을 가리킨다. "앞의 $i$개 물건"과 "물건 $i$"를 섞는 것이 배낭,
  편집 거리, LCS에서 가장 흔한 버그다. 표 위에 부분 문제 문장을 주석으로 적는다.
- **엉뚱한 것을 담은 기저 사례.** 개수 세기는 0이 아니라 `ways[0] = 1`에서 시작한다. 최소화는
  도달 불가 칸을 0이 아니라 무한대로 시작한다. C++에서 `INT_MAX + 1`은 오버플로하니 `1e9` 같은
  큰 유한 표시값을 쓰거나 더하기 전에 확인한다.
- **잘못된 반복 순서.** 한 행짜리 0/1 배낭은 용량을 *내려가며*, 무제한 배낭은 *올라가며* 돈다.
  동전 조합은 동전을 바깥 루프에, 순서열은 금액을 바깥에 둔다. 칸마다 "내가 읽는 값이 모두 이미
  쓰였고, 내가 원하는 의미로 쓰였는가?"를 물어 순서를 점검한다.
- **복원을 잊기.** 많은 문제가 수치가 아니라 부분집합·정렬·경로를 요구한다. 처음부터 계획한다.
  표 전체나 부모 배열을 둔다. 롤링 배열로는 복원할 수 없다.
- **정보를 잊는 상태.** 점화식이 인덱스가 기록하지 않는 것 — 방문한 도시, 주식 보유 여부, 직전
  선택 — 을 알아야 한다면 그것을 상태에 넣고 상태 수를 다시 센다.
- **답의 위치.** LIS는 어디서든 끝날 수 있다($i$에 대한 최댓값). 배낭의 답이 $V[n][W]$인 것은
  표가 "용량 최대 $x$"를 뜻하기 때문일 뿐이다.
- **파이썬의 재귀 한도와 해시 불가 인자.** `functools.cache`는 해시 가능한 인자가 필요하다(리스트
  대신 튜플). 깊은 하향식 재귀는 기본 1000프레임에 걸리니, $n$이 수천이면 상향식으로 간다.
- **탐욕 직감 믿기.** 탐욕으로 가기 전에 작은 입력을 전수 조사해 비교한다. 동전 $\{1,3,4\}$와 $6$
  같은 두 줄짜리 반례면 논의가 끝난다.
- **복잡도는 표에서 말한다.** 상태 수 × 상태당 전이 수, 그리고 차원 하나가 개수가 아니라 수치
  값이면 의사 다항식이라는 단서를 붙인다.

### 스스로 점검

1. 동전 $\{1, 5, 6, 9\}$, 목표 $11$. 큰 동전부터 고르는 탐욕은 무엇을 반환하고, 최적은 무엇인가?
2. 한 지원자가 1차원 0/1 배낭을 용량 루프를 올라가며 돌도록 썼다. 물건 하나(무게 3, 가치 5)와
   용량 6에서 무엇을 반환하며, 왜 그런가?
3. $O(nW)$ 배낭 알고리즘이 P = NP를 보이지 못하는 이유는?
4. `arm`과 `ram` 사이의 편집 거리를 구하고 최적 정렬 하나를 제시하라.
5. $[2, 5, 3, 7, 11, 8, 10, 13, 6]$에 인내 정렬을 돌려라. LIS 길이, 최종 `tails` 배열은 무엇이며,
   `tails` 자체가 입력의 증가 부분 수열인가?
6. Held–Karp의 상태에 방문한 도시의 *집합*이 필요한 이유는 무엇이고, 순서는 왜 필요 없는가?
7. DTW와 편집 거리의 차이 두 가지, 그리고 조정 창을 쓰는 이유 하나를 말하라.
8. §1의 4단계 레시피를 유한 지평 가치 반복에 적용하라. 부분 문제, 계산 순서, 기저 사례, 복원은
   각각 무엇인가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 탐욕은 $9$, $1$, $1$로 세 개. 최적은 $5 + 6$으로 두 개. DP는 $a = 11$에서 $6$을 포함한 모든 마지막 동전을 시도하고 $f(5) = 1$이므로 이를 찾는다.
> 2. $10$을 반환한다. 오름차순 루프에서는 물건 자신의 패스 중에 `best[3]`이 $5$가 되고, 이어 `best[6]`이 갱신된 `best[3]`을 읽어 같은 물건을 한 번 더 더한다. 물건을 두 번 쓰는 무제한 규칙이다. 내림차순으로 돌면 `best[3]`을 갱신 전에 읽어 $5$를 반환한다.
> 3. 다항 시간은 입력 길이에 대한 다항식이다. $W$는 $O(\log W)$비트뿐이므로 $O(nW)$는 수 $W$의 표현 크기에 대해 지수적이다. 이 알고리즘은 의사 다항식이다. 수가 작으면 빠르지만 일반적으로 다항 시간은 아니다.
> 4. 거리 $2$. 정렬 하나: `-arm` 위 `ra-m` — r 삽입, a 일치, r 삭제, m 일치로 연산 2번이다. 앞 두 글자를 모두 치환하는 `arm` 위 `ram`(a → r, r → a, m 일치)도 비용 2다.
> 5. `tails`는 $[2] \to [2,5] \to [2,3] \to [2,3,7] \to [2,3,7,11] \to [2,3,7,8] \to [2,3,7,8,10] \to [2,3,7,8,10,13] \to [2,3,6,8,10,13]$. 길이 $6$(예: $2, 3, 7, 8, 10, 13$). 최종 `tails`는 부분 수열이 아니다. 입력에서 $6$은 $8$, $10$, $13$보다 뒤에 온다.
> 6. 도시 $j$로 경로를 늘리는 것은 $j$를 아직 방문하지 않았을 때만 합법이므로 부분 문제가 어떤 도시를 썼는지 알아야 한다. 그렇지 않으면 도시를 재방문하는 경로들을 이어 붙이게 된다(§1의 최적 부분 구조 실패). 순서가 무관한 이유는 $j$에서 순회를 마치는 비용이 어느 도시가 남았고 지금 어디 있는지에만 달렸지, 어떻게 왔는지에는 달리지 않기 때문이다. 이것이 $n!$개 순서를 $2^n$개 부분집합으로 줄인다.
> 7. DTW에는 고정 삽입·삭제 비용이 없고(반복 짝은 국소 거리만큼 든다) 모든 표본을 반드시 짝짓는다. 편집 거리는 연산마다 상수를 매기고 원소를 통째로 삭제할 수 있다. 또 DTW의 국소 비용은 일치/불일치 표시가 아니라 실숫값 거리다. 창 $\lvert i-j\rvert \le r$은 비용을 $O(nr)$로 줄이고, 서로 다른 동작을 비슷해 보이게 만드는 퇴화 와핑을 막는다.
> 8. 부분 문제: $V_t(s)$, 결정 $t, \dots, T-1$이 남은 상태 $s$에서의 최대 총보상. 순서: $t$를 $T-1$에서 $0$까지 내려간다. 기저 사례: $V_T(s) = 0$(또는 종단 보상). 복원: $(t, s)$마다 $\arg\max_a$를 저장하면 그것이 최적 정책이다.

### 출처

- Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.), 동적 계획법 장. MIT Press.
- Roughgarden, T. (2019). *Algorithms Illuminated, Part 3: Greedy Algorithms and Dynamic Programming*; (2020) *Part 4: Algorithms for NP-Hard Problems*. Soundlikeyourself Publishing.
- Kulikov, A., & Pevzner, P. (2018). *Learning Algorithms Through Programming and Puzzle Solving*, 동적 계획법 장. Active Learning Technologies.
- Levenshtein, V. I. (1966). Binary codes capable of correcting deletions, insertions, and reversals. *Soviet Physics Doklady*, 10(8), 707–710.
- Wagner, R. A., & Fischer, M. J. (1974). The string-to-string correction problem. *Journal of the ACM*, 21(1), 168–173.
- Fredman, M. L. (1975). On computing the length of longest increasing subsequences. *Discrete Mathematics*, 11(1), 29–35.
- Held, M., & Karp, R. M. (1962). A dynamic programming approach to sequencing problems. *Journal of the Society for Industrial and Applied Mathematics*, 10(1), 196–210. https://doi.org/10.1137/0110015
- Bellman, R. (1962). Dynamic programming treatment of the travelling salesman problem. *Journal of the ACM*, 9(1), 61–63.
- Sakoe, H., & Chiba, S. (1978). Dynamic programming algorithm optimization for spoken word recognition. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 26(1), 43–49. https://doi.org/10.1109/TASSP.1978.1163055
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.), ch. 4. MIT Press.
