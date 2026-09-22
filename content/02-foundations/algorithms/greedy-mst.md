---
title: 11.4 Greedy Algorithms & Spanning Trees
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Decide whether a locally best choice is safe, prove it with a stays-ahead or exchange argument or break it with a three-item counterexample, and write interval scheduling, Huffman coding, Prim and Kruskal from a blank file."
mastery-when: "Raise to Mastery only if coverage, view planning or sensor selection with approximation guarantees becomes part of the research contribution."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/complexity-recursion|11.1 Complexity, Recursion & Backtracking]] (Big-O, induction) · [[02-foundations/algorithms/data-structures|11.2 Core Data Structures]] (heaps §4, union-find §7) · optional for §5: [[02-foundations/information-theory|5. Information Theory]] (entropy)
> [[02-foundations/algorithms/complexity-recursion|11.1 복잡도·재귀·백트래킹]](Big-O, 귀납법) · [[02-foundations/algorithms/data-structures|11.2 핵심 자료구조]](힙 §4, union-find §7) · §5는 선택: [[02-foundations/information-theory|5. 정보 이론]](엔트로피)

## English

A greedy algorithm builds its answer one irrevocable choice at a time, always taking whatever looks best right now. Greedy algorithms are easy to invent and their running time is usually just the cost of one sort or one heap. What makes them hard is that most of them are wrong: in §1, paying 6 with coins $\{1, 3, 4\}$ by always taking the largest coin uses three coins when two suffice. So interviews test two skills. The first is choosing the right rule, for example which key to sort by. The second is knowing why that rule works, or finding the small input where it fails. This page covers the standard problems where greedy is exactly optimal: interval scheduling, weighted scheduling, fractional knapsack, Huffman codes and minimum spanning trees. It then covers the NP-hard problems (roughly, problems for which no polynomial-time exact algorithm is known; [[02-foundations/algorithms/complexity-recursion#P, NP, NP-hard, and pseudo-polynomial time|11.1 §1]] defines the term) where greedy is the best practical tool and comes with a proven approximation factor, which is how sensor placement and view planning papers use it.

What interviews ask: "maximum non-overlapping intervals", "minimum meeting rooms", "merge intervals", Huffman coding, Prim or Kruskal from scratch, and "prove it" or "why doesn't greedy work here". Robotics labs add Euclidean clustering of point clouds (§6) and greedy sensor or viewpoint selection (§7).

> [!note] First pass · 처음이라면
> Read §1 carefully, because the two proof patterns and the habit of looking for a counterexample are what the rest of the page reuses. Then do §2 and §6 with the code open, since those are the most frequently asked. §3–§5 are shorter single-problem sections. §7 is for research reading, and §8 is the checklist to read before an interview.

### 1. What makes a choice greedy, and how to prove or break it

**The idea in one sentence:** make the choice that is best by a simple local rule, commit to it, and solve what remains in the same way.

**What a greedy algorithm is.** It is an algorithm-design paradigm for optimization problems whose solution is built from a sequence of choices, and it has four named parts:

- **candidates**, the pieces a solution is made of (intervals, edges, coins);
- a **selection rule**, a simple key that ranks the candidates;
- a **feasibility test**, which says whether a candidate can join the partial solution;
- **irrevocable commitment**: a chosen candidate is never removed or reconsidered.

Largest-coin-first change making, Kruskal and Huffman coding all have exactly these parts.

**When it is correct.** Write $I$ for an instance, $g$ for the greedy first choice, $I_g$ for the smaller instance that remains after committing to $g$, and $\mathrm{OPT}(\cdot)$ for the optimal value. Two properties are needed.

- The **greedy-choice property**: some optimal solution of $I$ contains $g$. It need not be every optimal solution, only one.
- **Optimal substructure**: an optimal solution of $I$ that contains $g$ consists of $g$ together with an optimal solution of $I_g$, so for a cost that adds up over the choices
$$\mathrm{OPT}(I) = c(g) + \mathrm{OPT}(I_g)$$
  where $c(g)$ is the cost, or value, of the choice $g$ itself.

Together they prove greedy correct by induction on the instance size, because the first choice loses nothing and what remains is the same problem again. **Non-example:** paying $6$ with coins $\{1, 3, 4\}$, the greedy first choice is the coin $4$, but the only two-coin solution is $3 + 3$, so no optimal solution contains $4$ and the greedy-choice property fails. Optimal substructure still holds there, which is why dynamic programming solves it. Dynamic programming needs only the second property and pays for it by trying every option for each decision ([[02-foundations/algorithms/dynamic-programming|11.5 §1]]). Greedy trusts one option, so it needs a proof that the one option is enough.

There are two standard ways to write that proof.

**Method 1: greedy stays ahead.** Choose a measure of progress that you can compare after each step, such as "how far along the route", "how many intervals scheduled" or "the finish time of the last interval chosen". Show by induction that after every step $k$, greedy's measure is at least as good as that of *any* other valid solution after $k$ steps. With $m_k(S)$ the measure of solution $S$ after $k$ steps, the claim to prove is
$$m_k(G) \succeq m_k(O) \quad \text{for every step } k \text{ and every valid solution } O$$
where $\succeq$ means "at least as good as", so it is $\ge$ for a measure you want large and $\le$ for one you want small. Then show that being ahead at every step means greedy cannot finish later or with fewer items.

**Method 2: exchange argument.** Take any optimal solution $O$ that differs from the greedy solution $G$. Find the first place where they differ, and change $O$ at that place to agree with $G$, without making $O$ invalid and without making it worse: the changed solution $O'$ is valid and $\text{cost}(O') \le \text{cost}(O)$. Repeating this turns $O$ into $G$ step by step, and cost never increases along the way, so $G$ is optimal too. A shorter form of the same argument proves only that greedy's *first* choice can be swapped into some optimal solution, and then uses optimal substructure to repeat on the rest.

The two methods are often interchangeable. Stays-ahead fits problems where solutions are built along a line or through time. Exchange fits problems where the answer is an order or a set, and swapping two elements has a cost you can compute.

> [!example] Worked example · 계산 예제
> A mobile robot drives along a straight corridor from position $0$ to a goal at $20$ m. It starts fully charged and can drive $6$ m on one charge. Charging docks sit at $3, 5, 9, 12, 16$. Greedy rule: drive past docks while the next dock (or the goal) is still reachable, and charge only at the farthest reachable dock. From $0$ the farthest reachable dock is $5$, then $9$ (reach $11$), then $12$ (reach $15$), then $16$ (reach $18$). From $16$ the robot reaches $22 \ge 20$. That is **4 charges**. Stays-ahead proof: let $g_k$ and $o_k$ be the positions of greedy's and any other plan's $k$-th charge. Suppose $g_{k-1} \ge o_{k-1}$. The other plan's next dock satisfies $o_k \le o_{k-1} + 6 \le g_{k-1} + 6$, so it was reachable for greedy too, and greedy took the farthest such dock. So $g_k \ge o_k$. If the other plan reaches the goal after $m$ charges, then $g_m + 6 \ge o_m + 6 \ge 20$ and greedy reaches it after at most $m$ charges.

<svg viewBox="0 0 560 230" style="max-width:100%;height:auto" role="img" aria-label="Charging docks at 3, 5, 9, 12 and 16 m on a 20 m corridor with a 6 m reach: each row is one charge's reach window, and greedy charges at the farthest dock inside it, at 5, 9, 12 and 16, four charges; from 16 the reach 22 passes the goal at 20.">
  <text x="8" y="18" font-size="12" fill="currentColor">reach 6 m per charge; greedy charges at the farthest dock in reach</text>
  <rect x="30" y="38" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <rect x="94" y="41.5" width="7" height="7" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.8"/>
  <circle cx="142.5" cy="45" r="4.5" stroke="none" fill="currentColor"/>
  <text x="171" y="49" font-size="11" fill="currentColor">charge 1 at 5</text>
  <text x="97.5" y="35" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">3: passed by</text>
  <rect x="142.5" y="64" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="232.5" cy="71" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="142.5" y1="50" x2="142.5" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="283.5" y="75" font-size="11" fill="currentColor">charge 2 at 9</text>
  <rect x="232.5" y="90" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="300" cy="97" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="232.5" y1="76" x2="232.5" y2="90" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="373.5" y="101" font-size="11" fill="currentColor">charge 3 at 12</text>
  <rect x="300" y="116" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="390" cy="123" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="300" y1="102" x2="300" y2="116" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="441" y="127" font-size="11" fill="currentColor">charge 4 at 16</text>
  <rect x="390" y="142" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <line x1="390" y1="128" x2="390" y2="142" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="384" y="153" font-size="11" fill="currentColor" text-anchor="end">16 + 6 = 22 ≥ 20: goal</text>
  <line x1="30" y1="180" x2="525" y2="180" stroke="currentColor" stroke-width="1.2"/>
  <line x1="30" y1="176" x2="30" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="30" y="197" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="97.5" y1="176" x2="97.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="97.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <line x1="142.5" y1="176" x2="142.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="142.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="232.5" y1="176" x2="232.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="232.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">9</text>
  <line x1="300" y1="176" x2="300" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="300" y="197" font-size="11" fill="currentColor" text-anchor="middle">12</text>
  <line x1="390" y1="176" x2="390" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="197" font-size="11" fill="currentColor" text-anchor="middle">16</text>
  <line x1="480" y1="176" x2="480" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="197" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <rect x="94" y="176.5" width="7" height="7" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <rect x="139" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="229" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="296.5" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="386.5" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <line x1="480" y1="176" x2="480" y2="158" stroke="currentColor" stroke-width="1.4"/>
  <path d="M480 158 L491 161.5 L480 165 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="494" y="168" font-size="10" fill="currentColor" fill-opacity="0.85">goal</text>
  <text x="525" y="216" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">position along the corridor (m)</text>
</svg>

```python
def min_charges(docks, reach, goal):
    """Fewest charging stops from 0 to goal, or -1 if some gap exceeds reach."""
    docks = sorted(docks)
    stops, pos, i = 0, 0, 0
    while pos + reach < goal:
        farthest = pos
        while i < len(docks) and docks[i] <= pos + reach:
            farthest = docks[i]              # keep walking: a later dock is better
            i += 1
        if farthest == pos:
            return -1                        # no dock ahead within reach
        pos, stops = farthest, stops + 1
    return stops

print(min_charges([3, 5, 9, 12, 16], 6, 20))  # 4
print(min_charges([2, 9], 6, 12))             # -1
```

It runs in $O(n \log n)$ for the sort plus $O(n)$ for the scan, because the index `i` only moves forward.

**How to break a greedy idea quickly.** Before trying to prove anything, spend one minute looking for a counterexample with two or three items. Try items that are almost tied, one very large item against several small ones, and inputs where the greedy rule's first choice blocks two later choices.

- **Coin change with coins $\{1, 3, 4\}$ and amount $6$.** Largest-coin-first takes $4 + 1 + 1$, three coins. The optimum is $3 + 3$, two coins. For some coin systems, such as $\{1, 5, 10, 25\}$, largest-first happens to be optimal, but that is a property of those particular denominations. The general problem needs DP ([[02-foundations/algorithms/dynamic-programming|11.5 §3]]).
- **0/1 knapsack by value-to-weight ratio.** Capacity $10$. Items (weight, value): $(6, 9)$ with ratio $1.5$, and two copies of $(5, 7)$ with ratio $1.4$. Greedy takes $(6, 9)$ first, and then neither $(5, 7)$ fits: value $9$. The two $(5, 7)$ items fill the capacity exactly for value $14$. §4 explains why the same rule becomes correct once items can be cut.

A counterexample is a complete answer to "does this greedy work?". A proof is required only for the other answer.

### 2. Interval problems

Intervals are the most common greedy family in interviews. Choose an endpoint convention first and say it aloud. This page uses **half-open** intervals $[s, e) = \{t : s \le t < e\}$, which contain their start time but not their end time. Two intervals overlap exactly when they share a time:
$$[s_1, e_1) \cap [s_2, e_2) \ne \varnothing \iff s_1 < e_2 \ \text{ and } \ s_2 < e_1$$
since each must start before the other ends. So a booking that ends at $10$ does not conflict with one that starts at $10$: for $[8, 10)$ and $[10, 12)$ the test $10 < 10$ is false. Closed intervals $[s, e]$ use $\le$ in both places, and then $[1, 3]$ and $[3, 5]$ overlap at time $3$.

#### Activity selection: the most non-overlapping intervals

**Problem.** Given $n$ intervals, choose a subset $S$ of largest size $|S|$ in which no two intervals overlap in the sense above.

**The idea in one sentence:** repeatedly take the interval that *finishes* earliest among those that start after the last one taken.

**Why earliest finish is safe (exchange).** Let $a$ be the interval with the earliest finish time, and let $O$ be any optimal set of non-overlapping intervals, sorted by time. Replace the first interval $o_1$ of $O$ by $a$. Since $a$ finishes no later than $o_1$, $a$ ends before every other interval in $O$ begins, so the new set is still non-overlapping and has the same size. So some optimal solution contains $a$. Remove $a$ and every interval that overlaps it. What remains is the same problem on a smaller input, and the argument repeats.

**Why the other obvious keys fail.** *Earliest start:* $[0, 10), [1, 2), [3, 4)$ gives $1$ interval, but $2$ are possible. *Shortest first:* $[0, 5), [4, 6), [6, 10)$ picks the short $[4, 6)$, which blocks both others, giving $1$ instead of $2$. *Fewest overlaps* also has counterexamples, though they need more intervals to build.

```python
def max_activities(intervals):
    """intervals: (start, end), half-open. Returns a largest non-overlapping subset."""
    chosen = []
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):  # by finish time
        if start >= last_end:               # >= because [s, e) may touch
            chosen.append((start, end))
            last_end = end
    return chosen

jobs = [(0, 3), (1, 2), (2, 5), (4, 6), (5, 8), (7, 9), (8, 10)]
print(max_activities(jobs))  # [(1, 2), (2, 5), (5, 8), (8, 10)]
```

Sorting costs $O(n \log n)$ and the scan costs $O(n)$. A closely related problem is "fewest points that hit every interval", for example the fewest times to visit a site so that every tenant or crew is present at least once. Sorting by finish time and placing a point at each chosen finish time solves it, and the minimum number of points equals the maximum number of disjoint intervals.

<svg viewBox="0 0 560 297" style="max-width:100%;height:auto" role="img" aria-label="The seven jobs as bars on a time line, sorted by finish time. Earliest-finish greedy takes [1, 2), [2, 5), [5, 8) and [8, 10) and skips the three that start before the last taken end. Below, the number of jobs running at each time peaks at 2, the depth, so 2 rooms suffice.">
  <text x="8" y="18" font-size="12" fill="currentColor">sorted by finish time; filled = taken, dashed = skipped</text>
  <line x1="158" y1="30" x2="158" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="284" y1="30" x2="284" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="410" y1="30" x2="410" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="494" y1="30" x2="494" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <text x="64" y="45.5" font-size="11" fill="currentColor" text-anchor="end">[1, 2)</text>
  <rect x="116" y="36" width="42" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="164" y="45.5" font-size="10" fill="currentColor" fill-opacity="0.8">taken</text>
  <text x="64" y="66.5" font-size="11" fill="currentColor" text-anchor="end">[0, 3)</text>
  <rect x="74" y="57" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="206" y="66.5" font-size="10" fill="currentColor" fill-opacity="0.8">skip: 0 &lt; 2</text>
  <text x="64" y="87.5" font-size="11" fill="currentColor" text-anchor="end">[2, 5)</text>
  <rect x="158" y="78" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="290" y="87.5" font-size="10" fill="currentColor" fill-opacity="0.8">taken</text>
  <text x="64" y="108.5" font-size="11" fill="currentColor" text-anchor="end">[4, 6)</text>
  <rect x="242" y="99" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="332" y="108.5" font-size="10" fill="currentColor" fill-opacity="0.8">skip: 4 &lt; 5</text>
  <text x="64" y="129.5" font-size="11" fill="currentColor" text-anchor="end">[5, 8)</text>
  <rect x="284" y="120" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="416" y="129.5" font-size="10" fill="currentColor" fill-opacity="0.8">taken</text>
  <text x="64" y="150.5" font-size="11" fill="currentColor" text-anchor="end">[7, 9)</text>
  <rect x="368" y="141" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="458" y="150.5" font-size="10" fill="currentColor" fill-opacity="0.8">skip: 7 &lt; 8</text>
  <text x="64" y="171.5" font-size="11" fill="currentColor" text-anchor="end">[8, 10)</text>
  <rect x="410" y="162" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="500" y="171.5" font-size="10" fill="currentColor" fill-opacity="0.8">taken</text>
  <line x1="74" y1="187" x2="494" y2="187" stroke="currentColor" stroke-width="1.2"/>
  <line x1="74" y1="187" x2="74" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="74" y="203" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="116" y1="187" x2="116" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="116" y="203" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="158" y1="187" x2="158" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="158" y="203" font-size="10" fill="currentColor" text-anchor="middle">2</text>
  <line x1="200" y1="187" x2="200" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="203" font-size="10" fill="currentColor" text-anchor="middle">3</text>
  <line x1="242" y1="187" x2="242" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="242" y="203" font-size="10" fill="currentColor" text-anchor="middle">4</text>
  <line x1="284" y1="187" x2="284" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="203" font-size="10" fill="currentColor" text-anchor="middle">5</text>
  <line x1="326" y1="187" x2="326" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="326" y="203" font-size="10" fill="currentColor" text-anchor="middle">6</text>
  <line x1="368" y1="187" x2="368" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="368" y="203" font-size="10" fill="currentColor" text-anchor="middle">7</text>
  <line x1="410" y1="187" x2="410" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="203" font-size="10" fill="currentColor" text-anchor="middle">8</text>
  <line x1="452" y1="187" x2="452" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="452" y="203" font-size="10" fill="currentColor" text-anchor="middle">9</text>
  <line x1="494" y1="187" x2="494" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="494" y="203" font-size="10" fill="currentColor" text-anchor="middle">10</text>
  <text x="504" y="203" font-size="11" fill="currentColor" font-style="italic">t</text>
  <text x="8" y="229" font-size="11" fill="currentColor">jobs running at time t: at most 2, so 2 rooms</text>
  <text x="64" y="281" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="74" y1="277" x2="494" y2="277" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="64" y="263" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <line x1="74" y1="259" x2="494" y2="259" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <text x="64" y="245" font-size="10" fill="currentColor" text-anchor="end">2</text>
  <line x1="74" y1="241" x2="494" y2="241" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <path d="M74 277 L74 259 L116 259 L116 241 L158 241 L158 241 L200 241 L200 259 L242 259 L242 241 L284 241 L284 241 L326 241 L326 259 L368 259 L368 241 L410 241 L410 241 L452 241 L452 259 L494 259 L494 277" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.12" stroke-linejoin="round"/>
</svg>

#### Minimum rooms: how many resources run all intervals

**The idea in one sentence:** sweep intervals in order of start time and reuse the resource that frees up earliest, opening a new one only when every resource is still busy.

**Why it is optimal.** At any time $t$, every interval that contains $t$ needs its own resource, so the answer is at least the maximum number of intervals that contain a common point, the *depth*:
$$\text{depth} = \max_t \big|\{i : s_i \le t < e_i\}\big|$$
The set counts the intervals that contain time $t$, so the depth is the largest number running at once; for the seven jobs in the code below it is $2$. The algorithm opens a new resource only when the earliest end in the heap is later than the current start. At that moment every open resource holds an interval that started no later and is still running, so together with the new interval they all contain the current start time, and the new count is at most the depth. The algorithm therefore never uses more resources than the depth, which is the lower bound.

```python
import heapq

def min_rooms(intervals):
    """Fewest resources so that no two overlapping half-open intervals share one."""
    ends = []                               # min-heap: end time of each busy resource
    for start, end in sorted(intervals):    # by start time
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)    # reuse the resource that frees first
        else:
            heapq.heappush(ends, end)       # all busy: open a new one
    return len(ends)

print(min_rooms([(0, 3), (1, 2), (2, 5), (4, 6), (5, 8), (7, 9), (8, 10)]))  # 2
print(min_rooms([(1, 3), (3, 5), (2, 4)]))  # 2; with closed intervals it would be 3
```

Time $O(n \log n)$. An equivalent version without a heap turns each interval into a $+1$ event at its start and a $-1$ event at its end, sorts the events, and tracks the running sum. For half-open intervals, a $-1$ must sort before a $+1$ at the same time. In robotics this answers "how many robots, charging docks or crane slots do these time-windowed jobs need?"

#### Merging intervals

**The idea in one sentence:** sort by start, and either extend the last merged interval or start a new one.

```python
def merge_intervals(intervals):
    """Union of intervals as a sorted list of disjoint ones. Touching ones merge."""
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # max: the new one may be inside
        else:
            merged.append([start, end])
    return [tuple(iv) for iv in merged]

print(merge_intervals([(4, 7), (1, 3), (2, 5), (9, 10), (10, 12)]))  # [(1, 7), (9, 12)]
```

This is barely greedy, but it has two classic bugs: forgetting `max` when one interval lies inside another, and using `<` versus `<=` inconsistently with the endpoint convention. A robotics use: a 2-D scan gives blocked angular sectors, one per obstacle. Merging them leaves the free gaps a reactive planner can steer through. Angles wrap around at $\pm\pi$, so split any sector that crosses the wrap point before sorting.

### 3. Scheduling to minimize weighted completion time

**Problem.** One machine, such as a single robot arm, a printer or one CPU, must process jobs one at a time. Job $j$ has length $l_j > 0$ and weight $w_j$, which measures how much each unit of waiting costs. Job $j$'s completion time $C_j$ is the sum of the lengths of all jobs up to and including $j$. The goal is to minimize the total weighted completion time:
$$C_j = \sum_{k \preceq j} l_k, \qquad \text{minimize } \sum_j w_j C_j$$
Here $k \preceq j$ means that job $k$ runs before $j$ or is $j$ itself, so a job's completion time includes its own length and every length scheduled before it.

**The idea in one sentence:** run jobs in decreasing order of $w_j / l_j$, so the most weight per unit of processing time goes first (Smith 1956).

**Exchange proof.** Take any schedule and two *adjacent* jobs, $i$ then $j$. Swapping them does not change the completion time of any other job, because the pair still occupies the same block of time. After the swap $j$ finishes $l_i$ earlier and $i$ finishes $l_j$ later. So the swap changes the total cost by

$$\Delta = w_i\, l_j - w_j\, l_i,$$

and it helps exactly when $\Delta < 0$. Dividing by $l_i l_j > 0$, that is when $w_i / l_i < w_j / l_j$, so the swap helps whenever a lower-ratio job sits directly before a higher-ratio job. Now take an optimal schedule. If it is not in ratio order, it has an adjacent pair out of order, and swapping that pair does not increase the cost (it stays equal when the ratios tie). Each such swap removes one inverted pair, so after at most $\binom{n}{2}$ swaps the optimal schedule has become the greedy schedule with no increase in cost. Therefore greedy is optimal, ties included.

**Why ordering by the difference $w_j - l_j$ fails.** The difference is plausible because it agrees with both special cases: with equal lengths, heavier jobs go first, and with equal weights, shorter jobs go first. But it fails when the two pull in different directions. Job A has $w = 6, l = 4$, so its difference is $2$ and its ratio $1.5$. Job B has $w = 2, l = 1$, so its difference is $1$ and its ratio $2$.

- Difference order A, B: $C_A = 4$ and $C_B = 5$, cost $6 \cdot 4 + 2 \cdot 5 = 34$.
- Ratio order B, A: $C_B = 1$ and $C_A = 5$, cost $2 \cdot 1 + 6 \cdot 5 = 32$.

So ordering by difference is not optimal. This is the general way to choose between two candidate keys: find a small input where the keys disagree and compute both costs.

> [!example] Worked example · 계산 예제
> Jobs (weight, length): $(3, 1)$, $(5, 2)$, $(2, 4)$ with ratios $3$, $2.5$, $0.5$. Ratio order gives completion times $1, 3, 7$ and cost $3 \cdot 1 + 5 \cdot 3 + 2 \cdot 7 = 32$. Checking all $3! = 6$ orders by brute force confirms that $32$ is the minimum.

```python
from fractions import Fraction

def order_jobs(jobs):
    """jobs: (weight, length), length > 0. Order minimizing sum of w * C."""
    return sorted(jobs, key=lambda j: Fraction(-j[0], j[1]))  # exact ratio, descending

def weighted_completion(order):
    t = total = 0
    for w, l in order:
        t += l                    # completion time of this job
        total += w * t
    return total

print(weighted_completion(order_jobs([(3, 1), (5, 2), (2, 4)])))  # 32
print(weighted_completion([(6, 4), (2, 1)]), weighted_completion(order_jobs([(6, 4), (2, 1)])))  # 34 32
```

`Fraction` keeps ratio ties exact. With floats, two ratios that are mathematically equal can compare as unequal. Ties do not change the optimal cost here, but the same bug matters in problems where tie-breaking changes the answer. In C++, compare `a.w * b.l > b.w * a.l` in 64-bit integers rather than dividing.

### 4. Fractional knapsack (greedy works) vs 0/1 knapsack (it does not)

**Fractional knapsack.** Items have weight $w_i$ and value $v_i$, and you may take any fraction of each item. With $x_i$ the fraction of item $i$ taken and $W$ the capacity, the problem is
$$\max \sum_i v_i x_i \quad \text{subject to} \quad \sum_i w_i x_i \le W, \qquad 0 \le x_i \le 1$$
so the total weight carried fits the capacity and no item is taken more than once. The **0/1 knapsack** is the same problem with $x_i \in \{0, 1\}$, every item taken whole or not at all. On §1's instance with $W = 10$, the greedy rule below sets $x = (1, 0.8, 0)$ for the items $(6, 9), (5, 7), (5, 7)$ and gets $9 + 0.8 \cdot 7 = 14.6$. **The idea in one sentence:** take items in decreasing order of value density $v_i / w_i$, and cut the last item to fill the remaining capacity.

**Why it works (exchange).** Suppose a solution leaves some of the densest item unused while carrying some amount $\varepsilon$ of a less dense item. Replace that $\varepsilon$ weight of the less dense item with $\varepsilon$ weight of the densest item. Total weight stays the same and value goes up by $\varepsilon$ times the density difference. So an optimal solution takes as much of the densest item as fits, and the argument repeats on the remaining capacity. Time $O(n \log n)$ for the sort.

```python
def fractional_knapsack(items, capacity):
    """items: (weight, value), weight > 0. Best value when items may be cut."""
    total = 0.0
    for w, v in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        if capacity <= 0:
            break
        take = min(w, capacity)
        total += v * take / w
        capacity -= take
    return total

print(fractional_knapsack([(6, 9), (5, 7), (5, 7)], 10))  # 14.6
```

**0/1 knapsack.** Each item must be taken whole or left. The exchange step above fails, because you cannot trade $\varepsilon$ of one item for $\varepsilon$ of another. §1's instance shows the damage: the density rule gets $9$, while the optimum is $14$. The problem is NP-hard. The standard exact method is the $O(nW)$ dynamic program in [[02-foundations/algorithms/dynamic-programming|11.5 §4]], which is pseudo-polynomial: its running time grows with the numeric value of the capacity $W$, not with the number of bits used to write $W$ ([[02-foundations/algorithms/complexity-recursion#P, NP, NP-hard, and pseudo-polynomial time|11.1 §1]]). Two facts connect the two versions and appear in research code:

- **The fractional optimum is an upper bound on the 0/1 optimum.** Here $14.6 \ge 14$. Branch-and-bound solvers use this bound to prune subtrees that cannot beat the best solution found so far.
- **A cheap 1/2-approximation.** Assume every item fits on its own. Take the density-ordered items while they fit, compare that value with the single most valuable item, and keep the better. The result is at least half the 0/1 optimum, because the greedy prefix plus the first item that did not fit is worth at least the fractional optimum. In detail: let item $j$ be the first item in density order that does not fit. The fractional optimum takes items $1, \dots, j-1$ whole and part of item $j$, and that fills the capacity, so it is worth at most the prefix value $V_{\text{pre}}$ plus $v_j$. Hence $\mathrm{OPT}_{0/1} \le \mathrm{OPT}_{\text{frac}} \le V_{\text{pre}} + v_j \le 2 \max(V_{\text{pre}}, v_{\max})$, where $v_{\max}$ is the value of the most valuable single item. On §1's instance, $14 \le 14.6 \le 9 + 7 = 16$, and the rule returns $\max(9, 9) = 9 \ge 14/2$.

### 5. Huffman coding

**Problem.** Symbols appear with frequencies $p_i$. Give each symbol a binary codeword so that no codeword is a prefix of another. A code with codewords $c_1, \dots, c_n$ is **prefix-free** when
$$c_i \text{ is not a prefix of } c_j \quad \text{for all } i \ne j$$
where a prefix of a string is any initial part of it. This makes a bit stream decodable without separators, because reading bits until they spell a codeword can never stop too early. $\{0, 10, 11\}$ is prefix-free. $\{0, 01, 1\}$ is not: $0$ is a prefix of $01$, and the stream $01$ could mean $0, 1$ or $01$. The goal is to minimize the expected code length $L = \sum_i p_i \ell_i$, where $\ell_i$ is the length of symbol $i$'s codeword.

**Codes as trees.** A prefix-free code is a binary tree whose leaves are the symbols. A left edge writes $0$ and a right edge writes $1$, and each codeword length equals the depth of its leaf. The problem is to choose the tree that minimizes $\sum_i p_i \cdot \text{depth}_i$.

**The idea in one sentence:** repeatedly merge the two lightest trees into one whose weight is their sum, until a single tree remains (Huffman 1952).

**Why it is optimal (sketch).**

1. *The two lightest symbols can be siblings at the deepest level.* Take any optimal tree and two sibling leaves $x, y$ at its maximum depth. Swap the lightest symbol $a$ with $x$ and the second-lightest $b$ with $y$. Each swap moves a lighter symbol deeper and a heavier one shallower, so the cost does not increase. Some optimal tree therefore has $a$ and $b$ as deepest siblings. This is an exchange argument.
2. *Merging them loses nothing.* Replace $a$ and $b$ by one meta-symbol with weight $p_a + p_b$. Every tree in which $a$ and $b$ are siblings corresponds to a tree on the smaller alphabet, and the two costs differ by exactly $p_a + p_b$, the same constant for every such tree. So the best tree for the smaller alphabet, expanded back, is the best tree with $a$ and $b$ as siblings, which by step 1 is optimal overall. Induction on the alphabet size finishes the proof.

```python
import heapq
from itertools import count

def huffman_code(freq):
    """freq: dict symbol -> weight > 0 (symbols must not be tuples). Returns symbol -> bits."""
    if len(freq) == 1:
        return {s: "0" for s in freq}
    tie = count()                           # tiebreaker: heapq must never compare trees
    heap = [(w, next(tie), s) for s, w in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)      # the two lightest trees
        w2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(tie), (a, b)))
    code = {}
    stack = [(heap[0][2], "")]
    while stack:
        node, prefix = stack.pop()
        if isinstance(node, tuple):         # internal node: (left, right)
            stack.append((node[0], prefix + "0"))
            stack.append((node[1], prefix + "1"))
        else:
            code[node] = prefix
    return code

freq = {"A": 0.4, "B": 0.2, "C": 0.2, "D": 0.1, "E": 0.1}
code = huffman_code(freq)
print(sum(p * len(code[s]) for s, p in freq.items()))  # 2.2 (up to float rounding)
```

**Complexity.** Each of the $n - 1$ merges does two pops and one push, so the total is $O(n \log n)$. If the weights are already sorted, two FIFO queues replace the heap and the merging takes $O(n)$: one queue holds the original leaves and the other holds merged trees, whose weights come out in nondecreasing order. The `count()` tiebreaker matters in Python, because when two weights are equal `heapq` compares the next tuple element, and comparing a string with a tuple raises `TypeError`.

**Expected length and entropy.** Let $H(p) = -\sum_i p_i \log_2 p_i$ be the entropy ([[02-foundations/information-theory|5. Information Theory §1]]). The Huffman code satisfies

$$H(p) \le L_{\text{Huffman}} < H(p) + 1,$$

because of three facts. First, every prefix code satisfies the Kraft inequality $\sum_i 2^{-\ell_i} \le 1$, because in the code tree a leaf at depth $\ell_i$ owns a $2^{-\ell_i}$ share of the positions at the bottom level and no two leaves share a position. Second, Kraft forces $L \ge H(p)$, because $L - H(p) = \sum_i p_i \log_2 \bigl(p_i / 2^{-\ell_i}\bigr) \ge -\log_2 \sum_i 2^{-\ell_i} \ge 0$, where the first step is Jensen's inequality (the same step that makes KL divergence non-negative) and the second is Kraft. Third, the lengths $\ell_i = \lceil \log_2 (1/p_i) \rceil$ give $2^{-\ell_i} \le p_i$, so they satisfy Kraft and some prefix code has exactly those lengths; each is less than $\log_2(1/p_i) + 1$, so that code's expected length is below $H(p) + 1$, and Huffman, being optimal, does at least as well.

> [!example] Worked example · 계산 예제
> Frequencies $A{:}\,0.4$, $B{:}\,0.2$, $C{:}\,0.2$, $D{:}\,0.1$, $E{:}\,0.1$. Merge $D$ and $E$ into $0.2$. Now there are three trees of weight $0.2$, and which two are merged next is a tie. One tie-break produces lengths $A{:}\,1$, $B{:}\,2$, $C{:}\,3$, $D{:}\,4$, $E{:}\,4$. Another produces $A{:}\,2$, $B{:}\,2$, $C{:}\,2$, $D{:}\,3$, $E{:}\,3$. Both have $L = 2.2$ bits, so the codes differ but both are optimal. A fixed-length code needs $3$ bits for five symbols. The entropy is $H = 0.4 \log_2 2.5 + 2 \cdot 0.2 \log_2 5 + 2 \cdot 0.1 \log_2 10 \approx 2.12$ bits, so Huffman is within $0.08$ bits of the floor.

The gap to $H$ comes from rounding each codeword to a whole number of bits. It is worst for very skewed distributions: a symbol with $p = 0.99$ still costs one full bit. Arithmetic coding and ANS avoid the per-symbol rounding and get closer to $H$. Huffman codes are still the entropy stage of DEFLATE, the format inside zip, gzip and PNG.

### 6. Minimum spanning trees

**Definitions.** Let $G = (V, E)$ be an undirected graph, a set $V$ of vertices and a set $E$ of edges, each edge an unordered pair $\{u, v\}$ of distinct vertices written $u\text{–}v$ ([[02-foundations/algorithms/graph-algorithms|11.6 §1]] shows how to store one), with a weight $w(e)$ on each edge. $G$ is **connected** when every two vertices are joined by a path. A **cycle** is a closed path $v_0, v_1, \dots, v_k = v_0$ with $k \ge 3$ and $v_0, \dots, v_{k-1}$ distinct. A **tree** is a connected graph with no cycle. A **spanning tree** of a connected $G$ is an edge set $T \subseteq E$ that satisfies three conditions:

- **spanning**: it is taken on all of $V$, so every vertex is part of the graph $(V, T)$;
- **connected**: $(V, T)$ has a path between every two vertices;
- **acyclic**: $T$ contains no cycle.

Every spanning tree has exactly $|V| - 1$ edges, and for an edge set on all of $V$, any two of "connected", "acyclic" and "$|T| = |V| - 1$" imply the third. The reason is a count. Start from $|V|$ isolated vertices and add the edges one at a time. An edge that joins two different components reduces the number of components by one, and an edge inside one component closes a cycle and reduces nothing. So $|T|$ edges leave at least $|V| - |T|$ components, with equality exactly when no edge closed a cycle, and a single component without a cycle takes exactly $|V| - 1$ edges.

A **minimum spanning tree** (MST) is a spanning tree of least total weight:
$$T^* = \arg\min_{T \text{ spanning tree of } G} w(T), \qquad w(T) = \sum_{e \in T} w(e)$$
The minimum ranges over the finitely many spanning trees, so an MST exists whenever $G$ is connected, though it need not be unique when weights tie. Negative weights are allowed, and a maximum spanning tree is found by negating every weight.

**Example and non-example.** The five-vertex graph in the code below has 21 spanning trees, with total weights from $12$ to $20$. Its MST is the only one of weight $12$, $\{0\text{–}2, 1\text{–}3, 1\text{–}2, 3\text{–}4\}$. The edge set $\{0\text{–}1, 0\text{–}2, 1\text{–}2, 1\text{–}3\}$ also has $4 = |V| - 1$ edges but is not a spanning tree: it contains the cycle $0\text{–}1\text{–}2\text{–}0$ and never reaches vertex $4$.

**Cut property.** A *cut* splits the vertices into two nonempty groups $(S, V \setminus S)$. An edge **crosses** the cut when its endpoints lie on different sides, so the crossing edges are
$$\delta(S) = \{(u, v) \in E : u \in S,\ v \notin S\}$$
For $S = \{0\}$ in the example graph, $\delta(S) = \{0\text{–}1\,(4),\ 0\text{–}2\,(1)\}$, so by the property below every MST contains $0\text{–}2$. *If $e$ is the lightest edge crossing some cut, then some MST contains $e$. If $e$ is strictly lightest, every MST contains $e$.* Proof by exchange: take an MST $T$ that does not contain $e = (u, v)$. $T$ has a path from $u$ to $v$, and because $u$ and $v$ are on opposite sides of the cut, that path has an edge $f$ that also crosses the cut. Replacing $f$ by $e$ gives another spanning tree, since removing $f$ splits $T$ into two parts and $e$ reconnects them. Its weight is $w(T) - w(f) + w(e) \le w(T)$, so it is also an MST, and it contains $e$. The figure runs both steps on the example graph: the cut $S = \{0\}$, and the swap for the spanning tree $\{0\text{–}1, 1\text{–}2, 1\text{–}3, 3\text{–}4\}$ of weight $15$, whose path from $0$ to $2$ crosses the cut at $f = 0\text{–}1$.

<svg viewBox="0 0 560 290" style="max-width:100%;height:auto" role="img" aria-label="The five-vertex example graph drawn twice. Left: the cut S = {0} crosses edges 0–1 of weight 4 and 0–2 of weight 1, so the light edge 0–2 is in every MST; the MST edges 0–2, 1–2, 1–3, 3–4 weigh 12. Right: the spanning tree 0–1, 1–2, 1–3, 3–4 of weight 15 lacks e = 0–2; its path from 0 to 2 crosses the cut at f = 0–1, and swapping f for e gives 15 − 4 + 1 = 12.">
  <text x="12" y="22" font-size="12" fill="currentColor">(a) cut S = {0}</text>
  <ellipse cx="48" cy="116" rx="24" ry="34" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.05" stroke-opacity="0.7"/>
  <text x="21" y="90" font-size="12" fill="currentColor" text-anchor="end" font-style="italic">S</text>
  <line x1="56.6" y1="109.2" x2="107.4" y2="68.8" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="75.2" y="84.4" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <line x1="56.6" y1="122.8" x2="107.4" y2="163.2" stroke="currentColor" stroke-width="2.6"/>
  <text x="75.2" y="155.6" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">1</text>
  <line x1="116" y1="73" x2="116" y2="159" stroke="currentColor" stroke-width="2.6"/>
  <text x="105" y="120" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">3</text>
  <line x1="127" y1="62" x2="173" y2="62" stroke="currentColor" stroke-width="2.6"/>
  <text x="150" y="55" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <line x1="121.9" y1="160.7" x2="178.1" y2="71.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="159.3" y="125.9" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="127" y1="170" x2="241" y2="170" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="184" y="185" font-size="11" fill="currentColor" text-anchor="middle">7</text>
  <line x1="189.9" y1="71.3" x2="246.1" y2="160.7" stroke="currentColor" stroke-width="2.6"/>
  <text x="227.3" y="114.1" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">6</text>
  <circle cx="48" cy="116" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="48" y="120" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <circle cx="116" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="116" y="66" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="116" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="116" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="184" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="184" y="66" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="252" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="252" y="174" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <text x="12" y="242" font-size="11" fill="currentColor">crossing edges: 0–1 (4) and 0–2 (1)</text>
  <text x="12" y="260" font-size="11" fill="currentColor">lightest is 0–2, so every MST has it</text>
  <text x="12" y="278" font-size="11" fill="currentColor">MST (thick): 1 + 2 + 3 + 6 = 12</text>
  <line x1="280" y1="34" x2="280" y2="228" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="294" y="22" font-size="12" fill="currentColor">(b) exchange: swap f for e</text>
  <ellipse cx="330" cy="116" rx="24" ry="34" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.05" stroke-opacity="0.7"/>
  <text x="303" y="90" font-size="12" fill="currentColor" text-anchor="end" font-style="italic">S</text>
  <line x1="338.6" y1="109.2" x2="389.4" y2="68.8" stroke="currentColor" stroke-width="2.6" stroke-opacity="0.75" stroke-dasharray="5 4"/>
  <text x="353.4" y="79.7" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold" font-style="italic">f = 4</text>
  <line x1="338.6" y1="122.8" x2="389.4" y2="163.2" stroke="currentColor" stroke-width="3.0"/>
  <text x="353.4" y="160.3" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold" font-style="italic">e = 1</text>
  <line x1="398" y1="73" x2="398" y2="159" stroke="currentColor" stroke-width="2.6"/>
  <text x="387" y="120" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">3</text>
  <line x1="409" y1="62" x2="455" y2="62" stroke="currentColor" stroke-width="2.6"/>
  <text x="432" y="55" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <line x1="403.9" y1="160.7" x2="460.1" y2="71.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="441.3" y="125.9" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="409" y1="170" x2="523" y2="170" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="466" y="185" font-size="11" fill="currentColor" text-anchor="middle">7</text>
  <line x1="471.9" y1="71.3" x2="528.1" y2="160.7" stroke="currentColor" stroke-width="2.6"/>
  <text x="509.3" y="114.1" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">6</text>
  <circle cx="330" cy="116" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="330" y="120" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <circle cx="398" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="398" y="66" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="398" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="398" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="466" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="466" y="66" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="534" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="534" y="174" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <text x="294" y="242" font-size="11" fill="currentColor">T (thick): 4 + 3 + 2 + 6 = 15, lacks 0–2</text>
  <text x="294" y="260" font-size="11" fill="currentColor">its 0-to-2 path crosses at f = 0–1</text>
  <text x="294" y="278" font-size="11" fill="currentColor">T − f + e: 15 − 4 + 1 = 12, the MST</text>
</svg>

**Cycle property.** *If $e$ is the strictly heaviest edge on some cycle, no MST contains $e$.* If an MST contained $e$, removing $e$ would split it into two parts. Some other edge of the cycle crosses between those parts and is lighter, so swapping it in would give a cheaper spanning tree.

Both classic algorithms apply the cut property repeatedly. They differ in which cut they use.

#### Prim: grow one tree

**The idea in one sentence:** start from any vertex, and repeatedly add the lightest edge that leaves the tree built so far (Jarník 1930; Prim 1957).

The cut is (tree vertices, all other vertices), so every added edge is justified by the cut property. In code, a min-heap holds the edges that leave the tree, keyed by weight: pop the lightest, skip it if its far end has already joined the tree, and otherwise add that vertex and push its edges to vertices still outside. (If you already know Dijkstra's algorithm, [[02-foundations/algorithms/graph-algorithms|11.6 §4]], this is the same loop with the edge weight as the key in place of the distance from a source.)

```python
import heapq

def prim(n, adj, root=0):
    """adj[u] = list of (weight, v), undirected. Returns MST edges (w, parent, v) or None."""
    in_tree = [False] * n
    heap = [(0, root, root)]
    tree = []
    while heap:
        w, parent, u = heapq.heappop(heap)
        if in_tree[u]:
            continue                        # stale entry: u already joined more cheaply
        in_tree[u] = True
        if u != root:
            tree.append((w, parent, u))
        for wv, v in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wv, u, v))
    return tree if len(tree) == n - 1 else None   # None: graph is disconnected

edges = [(4, 0, 1), (1, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3), (7, 2, 4), (6, 3, 4)]
adj = [list() for _ in range(5)]
for w, u, v in edges:
    adj[u].append((w, v))
    adj[v].append((w, u))
print(sum(w for w, _, _ in prim(5, adj)))  # 12
```

**Complexity.** This "lazy" version pushes one heap entry per edge direction and skips stale entries when they are popped. That gives $O(E)$ heap operations of $O(\log E)$ each, so $O(E \log E) = O(E \log V)$, because $E \le V^2$ means $\log E \le 2 \log V$. On a dense graph given as an adjacency matrix, an array of keys scanned in $O(V)$ per step gives $O(V^2)$, which is faster when $E$ is close to $V^2$.

#### Kruskal: add edges lightest first

**The idea in one sentence:** sort all edges by weight and keep each one that connects two different components (Kruskal 1956). A **component** here is a maximal set of vertices joined by the edges kept so far.

**Why it is correct.** When Kruskal accepts $e = (u, v)$, take the cut (the component containing $u$, everything else). No edge crossing that cut was considered earlier, because Kruskal would have accepted it and $u$'s component would be larger. So $e$ is the lightest edge crossing this cut, and the cut property justifies it. Each rejected edge would close a cycle, and it is a heaviest edge on that cycle.

```python
def kruskal(n, edges):
    """edges: (weight, u, v). Returns MST edges (a spanning forest if disconnected)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    tree = []
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:                        # different components: no cycle
            parent[ru] = rv
            tree.append((w, u, v))
            if len(tree) == n - 1:
                break
    return tree

edges = [(4, 0, 1), (1, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3), (7, 2, 4), (6, 3, 4)]
print(kruskal(5, edges))  # [(1, 0, 2), (2, 1, 3), (3, 1, 2), (6, 3, 4)]
```

**Complexity.** Sorting costs $O(E \log E)$, and the union-find operations cost nearly $O(1)$ amortized each, so the sort dominates. The short `find` above uses path halving only. The version with union by size, and the $O(\alpha(n))$ bound, are in [[02-foundations/algorithms/data-structures|11.2 §7]].

> [!example] Worked example · 계산 예제
> Five site locations $0$–$4$ need a cable network, with the costs in `edges` above. Kruskal considers $0\text{–}2\,(1)$ and accepts it, then $1\text{–}3\,(2)$ and accepts it, then $1\text{–}2\,(3)$ and accepts it, which joins the two components. It rejects $0\text{–}1\,(4)$ because $0$ and $1$ are already connected through $2$, and rejects $2\text{–}3\,(5)$ for the same reason. It accepts $3\text{–}4\,(6)$ and stops at four edges. Total $1 + 2 + 3 + 6 = 12$. Prim from vertex $0$ adds the same edges in the order $1, 3, 2, 6$.

**Which to use.** Use Kruskal when the graph arrives as an edge list, or when you also want the components at intermediate thresholds (see clustering below). Use Prim with a heap for a sparse adjacency list, and Prim with an array for a dense matrix.

**Two properties worth knowing.**

- **An MST is not a shortest-path tree.** A shortest-path tree from a source $s$ is a spanning tree in which the tree path from $s$ to every vertex $v$ has length $d(s, v)$, the shortest distance in $G$. Take a triangle with $w(A,B) = 2$, $w(B,C) = 2$ and $w(A,C) = 3$. The MST is $\{AB, BC\}$ with weight $4$. The shortest-path tree from $A$ is $\{AB, AC\}$ with weight $5$, because in the MST the path from $A$ to $C$ has length $4$, not $3$. Use an MST to connect everything cheaply, and a shortest-path tree for cheap routes from one source.
- **The MST minimizes the bottleneck.** For any two vertices, the path between them in the MST has the smallest possible *largest* edge among all paths between them:
$$\max_{e \in P_{\text{MST}}(u, v)} w(e) = \min_{P \text{ from } u \text{ to } v} \ \max_{e \in P} w(e)$$
  Here $P_{\text{MST}}(u, v)$ is the path between $u$ and $v$ inside the tree, which is unique since a tree has no cycle, and $P$ ranges over all paths in $G$. In the example graph, the tree path $0\text{–}2\text{–}1\text{–}3\text{–}4$ has largest edge $6$, and no path from $0$ to $4$ does better, because every path must enter vertex $4$ through $3\text{–}4\,(6)$ or $2\text{–}4\,(7)$. For example, the smallest battery range that lets a robot hop between any two charging docks is the heaviest edge of the MST built on the dock distances.

#### Single-linkage clustering: Kruskal stopped early

**The idea in one sentence:** treat points as vertices and distances as edge weights, run Kruskal, and stop before the long edges.

There are two stopping rules. The name comes from how the method measures the distance between two clusters, by their single closest pair, $d_{\text{single}}(A, B) = \min_{p \in A,\, q \in B} d(p, q)$; complete linkage uses the $\max$ over pairs and average linkage the mean. Stop when **$k$ components** remain: this gives the $k$-clustering that maximizes *spacing*, the smallest distance between points in different clusters,
$$\text{spacing}(C_1, \dots, C_k) = \min_{a \ne b} \ \min_{p \in C_a,\, q \in C_b} d(p, q)$$
so a large spacing means every cluster is far from every other. The two clusters of the first call below have spacing $5$, the distance from $(1, 0)$ to $(6, 0)$. Or stop at **the first edge longer than a threshold $r$**: the clusters are then exactly the connected components of the graph that joins every pair of points closer than $r$ (Gower & Ross 1969).

```python
from itertools import combinations
from math import dist

def single_linkage(points, max_gap):
    """Cluster labels: points joined by any chain of hops no longer than max_gap."""
    parent = list(range(len(points)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pairs = sorted((dist(p, q), i, j) for (i, p), (j, q) in combinations(enumerate(points), 2))
    for d, i, j in pairs:
        if d > max_gap:
            break                             # Kruskal stopped early
        parent[find(i)] = find(j)
    roots = {}
    return [roots.setdefault(find(i), len(roots)) for i in range(len(points))]

box = [(0, 0), (0.5, 0.3), (1, 0)]
crate = [(6, 0), (6.4, 0.5), (7, 0)]
print(single_linkage(box + crate, 1.2))                             # [0, 0, 0, 1, 1, 1]
print(single_linkage(box + [(2, 0), (3, 0), (4, 0), (5, 0)] + crate, 1.2))  # all 0
```

Building all pairs costs $O(n^2 \log n)$, which is fine for a few hundred detections and far too slow for a point cloud. **The robotics use.** *Euclidean cluster extraction*, the standard way to split a LiDAR or depth point cloud into objects after the ground plane has been removed, is single linkage with a threshold $r$. Real implementations do not sort all pairs. They find each point's neighbours within $r$ using a KD-tree or voxel hash ([[02-foundations/algorithms/data-structures|11.2 §8]]) and join them with union-find or a BFS. The same rule groups detections from several cameras or consecutive frames that lie within $r$ of each other.

**The chaining weakness.** One chain of short hops is enough to merge two clusters. The second call above shows a thin line of points, such as a cable, a railing, remaining ground returns or a worker's arm resting on a wall, joining two objects into one cluster. Common fixes are to remove the ground plane first (for example with RANSAC), to require a minimum number of neighbours before a point may link, as density-based clustering does (DBSCAN, Ester et al. 1996), or to use average or complete linkage, which judge whole clusters rather than their single closest pair.

**Aside.** An MST also gives a 2-approximation for a shortest closed tour through points with metric distances (distances that, among the other metric axioms, satisfy the triangle inequality $d(a, c) \le d(a, b) + d(b, c)$), such as an inspection route. Walk around the MST, visiting each edge twice, and skip vertices already visited. The walk costs $2 \cdot w(\text{MST})$, and skipping vertices cannot lengthen it because of the triangle inequality. Every tour costs at least $w(\text{MST})$, because deleting one edge of a tour leaves a spanning tree.

### 7. Greedy as an approximation when exact is NP-hard

For many coverage and selection problems, exact optimization is NP-hard, and greedy is both the practical method and the one with the best guarantee known to be achievable in polynomial time.

**Approximation factor.** An algorithm is an **$\alpha$-approximation** when, on every instance $I$, its value $\mathrm{ALG}(I)$ is within a factor $\alpha$ of the optimum $\mathrm{OPT}(I)$:
$$\mathrm{ALG}(I) \le \alpha \cdot \mathrm{OPT}(I) \ \text{ for minimization } (\alpha \ge 1), \qquad \mathrm{ALG}(I) \ge \alpha \cdot \mathrm{OPT}(I) \ \text{ for maximization } (\alpha \le 1)$$
The factor is a worst-case guarantee over all instances, so one good run proves nothing and one bad instance disproves it. §4's knapsack rule is a $1/2$-approximation and §6's MST tour a $2$-approximation. Below, set cover gets $\alpha = H(d)$, and in its worked example greedy uses $3$ sets against an optimum of $2$, a ratio of $1.5$ within $H(4) \approx 2.08$; submodular maximization gets $\alpha = 1 - 1/e$.

#### Set cover

**Problem.** A universe $U$ of $n$ elements, for example surface patches of a structure to inspect, and a family of subsets, for example the patches visible from each candidate viewpoint. Choose the fewest subsets whose union is $U$. With subsets $S_1, \dots, S_m \subseteq U$ and costs $c_j$, the problem is
$$\min_{J \subseteq \{1, \dots, m\}} \sum_{j \in J} c_j \quad \text{subject to} \quad \bigcup_{j \in J} S_j = U$$
so the unweighted problem, with every $c_j = 1$, simply counts the chosen subsets.

**The idea in one sentence:** repeatedly choose the subset that covers the most still-uncovered elements. In the weighted version, choose the subset with the lowest cost per newly covered element.

**The guarantee.** Let $d$ be the size of the largest subset, and $H(d) = 1 + \tfrac12 + \dots + \tfrac1d$. Greedy's total cost is at most $H(d)$ times the optimum, and this holds for the weighted version too (Chvátal 1979). Since $d \le n$ and $H(n) \le \ln n + 1$, greedy is always within a factor of about $\ln n$ of optimal. The unweighted case was shown earlier by Johnson (1974) and Lovász (1975). This is essentially the best possible: no polynomial-time algorithm achieves a factor of $(1 - \varepsilon) \ln n$ unless P = NP (Dinur & Steurer 2014).

*Proof idea.* When greedy picks a set, charge its cost evenly to the elements it newly covers. When $k$ elements are still uncovered, the optimal cover covers all of them using sets of total cost OPT, so some set costs at most $\mathrm{OPT}/k$ per uncovered element, and greedy pays no more than that. Summing the charges as $k$ goes from $n$ down to $1$ gives $\mathrm{OPT} \cdot H(n)$. Chvátal's finer accounting, done set by set, gives $H(d)$.

```python
def greedy_set_cover(universe, subsets):
    """subsets: dict name -> set. Returns chosen names, or None if U cannot be covered."""
    uncovered = set(universe)
    chosen = []
    while uncovered:
        best = max(subsets, key=lambda s: len(subsets[s] & uncovered))
        if not subsets[best] & uncovered:
            return None                     # some element is in no subset
        chosen.append(best)
        uncovered -= subsets[best]
    return chosen

views = {"V1": {1, 2, 3, 4}, "V2": {1, 3, 5}, "V3": {2, 4, 6}}
print(greedy_set_cover(range(1, 7), views))  # ['V1', 'V2', 'V3']; optimum is V2, V3
```

> [!example] Worked example · 계산 예제
> Six wall patches and three candidate viewpoints as in `views`. Greedy takes $V1$, which sees four new patches. Then $V2$ and $V3$ each add one new patch, so greedy uses $3$ viewpoints. $V2 \cup V3$ already covers all six, so the optimum is $2$. This does not violate the guarantee, because $d = 4$ and $H(4) \cdot 2 \approx 4.17 \ge 3$. The first choice looked best and was not part of any optimal cover.

Each round scans every subset, so a direct implementation costs $O(\text{rounds} \times \sum_S \lvert S\rvert)$. That is fast enough for view-planning instances with thousands of candidates. The lazy evaluation described next makes it faster still.

#### Submodular maximization: the 1 − 1/e guarantee

Many objectives in sensor placement and active perception have **diminishing returns**. Adding a sensor to a small set helps at least as much as adding it to a larger set that already contains the small one. Formally, a set function $f$ is *submodular* if $f(A \cup \{x\}) - f(A) \ge f(B \cup \{x\}) - f(B)$ whenever $A \subseteq B$ and $x \notin B$, and *monotone* if adding elements never decreases $f$, that is, $f(A) \le f(B)$ whenever $A \subseteq B$. Writing $\Delta(x \mid A) = f(A \cup \{x\}) - f(A)$ for the **marginal gain** of $x$ given $A$, submodularity is the single line
$$\Delta(x \mid A) \ge \Delta(x \mid B) \quad \text{for all } A \subseteq B,\ x \notin B$$
so an element is worth less the more has already been chosen. For the coverage function $f(A) = \lvert \bigcup_{j \in A} \text{views}[j] \rvert$ of the set-cover example above, $\Delta(V3 \mid \varnothing) = 3$ but $\Delta(V3 \mid \{V1\}) = 1$, since $V1$ already sees patches $2$ and $4$. **Non-example:** $f(A) = \lvert A \rvert^2$ is monotone but not submodular, because the first element gains $1$ and the second gains $3$. The area covered by the union of sensor footprints is monotone submodular. So is the information that sensor readings give about a hidden state, when the readings are conditionally independent given that state (Krause & Guestrin 2005). Krause, Singh & Guestrin (2008) develop this for sensor placement. For a monotone submodular $f$ with $f(\varnothing) = 0$, choosing $k$ elements one at a time by largest marginal gain guarantees

$$f(\text{greedy}_k) \ge \left(1 - \tfrac{1}{e}\right) f(\text{OPT}_k) \approx 0.632\, f(\text{OPT}_k),$$

because at each step the $k$ elements of the optimum together would add at least the remaining gap $f(\text{OPT}_k) - f(\text{greedy}_i)$, so the best single element adds at least $1/k$ of that gap, and the gap shrinks by a factor of at least $(1 - 1/k)$ each step, leaving at most $(1 - 1/k)^k \le 1/e$ of it (Nemhauser, Wolsey & Fisher 1978). This is why next-best-view and sensor-selection papers can use plain greedy selection and still state a guarantee. The guarantee requires all of its conditions. It needs monotonicity, submodularity and a simple budget of $k$ elements. If the objective has synergies, where two sensors together are worth more than the sum of each alone, or if the constraint is a path or a travel budget, the bound no longer applies. A standard speed-up, *lazy greedy* (Minoux 1978), keeps the previous marginal gains in a max-heap. By submodularity those gains can only have decreased, so only the top entries need recomputing.

### 8. Interview pitfalls

- **Sorting by the wrong key.** Activity selection sorts by *finish* time, not start time or length. Merging sorts by *start*. Weighted scheduling sorts by the *ratio* $w/l$, not the difference. Before coding, say the key and one sentence explaining why it is safe, then test it on a three-item input where the other candidate keys disagree.
- **Ties and endpoints.** Decide whether intervals are closed or half-open and use `<` or `<=` consistently. `[(1, 3), (3, 5), (2, 4)]` needs 2 rooms if intervals are half-open and 3 if they are closed. In a sweep with $\pm 1$ events, the order of events at equal times encodes that decision. Ties in Kruskal or in Huffman merges are harmless for the total cost, but they can change *which* tree you output, so do not assert one exact code or edge list in tests.
- **Heap tuples in Python.** `heapq` compares tuples element by element. If two weights tie, it compares the payload next, and that crashes for unorderable objects such as dicts, tuples mixed with strings, or custom nodes. Insert a counter as the second element. In C++, `std::priority_queue` is a max-heap: use `std::greater<>` or negate keys for Prim and Huffman.
- **Floating-point ratios.** Compare $w_a l_b$ with $w_b l_a$ in integers, or use `Fraction`, when ties or exact order matter.
- **Disconnected graphs.** Prim from one root silently returns only that root's component. Kruskal returns a spanning forest. Check that the tree has $V - 1$ edges.
- **Confusing MST with shortest paths.** "Cheapest way to connect everything" is an MST. "Cheapest route from one place" is Dijkstra ([[02-foundations/algorithms/graph-algorithms|11.6]]).
- **Guessing instead of proving.** Interviewers accept "I'd check this with an exchange argument", followed by the swap and its cost change. They do not accept "it seems right". When you cannot find a proof quickly, brute-force tiny inputs and compare against greedy, as below. This takes two minutes and either produces a counterexample or gives you confidence.

```python
def greedy_coins(coins, amount):
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count                             # coin 1 is present, so amount ends at 0

def fewest_coins(coins, amount):             # exact, by DP (11.5)
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        best[a] = min(best[a - c] + 1 for c in coins if c <= a)
    return best[amount]

def first_counterexample(max_coin=6, max_amount=20):
    for a in range(2, max_coin + 1):
        for b in range(a + 1, max_coin + 1):
            for amount in range(1, max_amount + 1):
                if greedy_coins([1, a, b], amount) != fewest_coins([1, a, b], amount):
                    return [1, a, b], amount
    return None

print(first_counterexample())  # ([1, 3, 4], 6)
```

### Self-check

1. Intervals $[0,7), [1,3), [2,4), [4,6), [6,8)$. How many intervals does the earliest-*start* greedy select, and how many does earliest-*finish* select? How many rooms are needed to run all five?
2. State the exchange argument for activity selection in three sentences. Which property of the earliest-finishing interval does the swap rely on?
3. Two jobs: $P$ with $w = 9, l = 6$ and $Q$ with $w = 4, l = 2$. Which goes first by difference, and which by ratio? Compute both costs.
4. Build a Huffman code for frequencies $a{:}\,1$, $b{:}\,1$, $c{:}\,2$, $d{:}\,3$, $e{:}\,5$. Give the codeword lengths, the total number of bits for this 12-symbol message, and the cost of a fixed-length code.
5. Items (weight, value) $(4, 8)$, $(3, 5)$, $(3, 5)$ and capacity $6$. What are the fractional optimum, the density-greedy 0/1 value and the true 0/1 optimum?
6. In a graph with repeated edge weights, Kruskal can output different trees depending on how it breaks ties. Are they all MSTs? Which part of the cut-property proof covers this?
7. A LiDAR cluster step with $r = 0.3$ m merges a worker and the scaffold they are leaning on. Explain why in terms of the algorithm, and give two fixes.
8. Greedy set cover returned 3 viewpoints, and you later find a cover with 2. Does this contradict the guarantee? What conditions would you need to check before citing the $(1 - 1/e)$ bound for a "choose $k$ viewpoints" objective?

> [!tip]- Answers
> 1. Earliest start takes $[0,7)$ first, and every other interval starts before $7$, so it selects **1**. Earliest finish takes $[1,3)$, then $[4,6)$, then $[6,8)$, so it selects **3**. At time $2$, the intervals $[0,7)$, $[1,3)$ and $[2,4)$ all overlap, so at least 3 rooms are needed, and `min_rooms` returns $3$.
> 2. Let $a$ be the interval that finishes first, and $O$ an optimal solution whose first interval is $o_1$. Replace $o_1$ with $a$. Because $a$ ends no later than $o_1$, it ends before every other interval of $O$ starts, so the set stays non-overlapping and keeps its size. The swap relies on $a$ having the *earliest end time*. Recursing on the intervals that start at or after $a$ ends completes the proof.
> 3. Differences: $P$ has $3$ and $Q$ has $2$, so difference order runs $P$ first, with cost $9 \cdot 6 + 4 \cdot 8 = 86$. Ratios: $P$ has $1.5$ and $Q$ has $2$, so ratio order runs $Q$ first, with cost $4 \cdot 2 + 9 \cdot 8 = 80$. The ratio order is better, as the exchange formula $\Delta = w_P l_Q - w_Q l_P = 18 - 24 < 0$ predicts: moving $Q$ ahead of $P$ lowers the cost by $6$.
> 4. Merge $a + b = 2$. Then merge that tree with $c$ to get $4$ (the two weight-$2$ trees are the two lightest, and $d = 3$ is heavier). Then $d + 4 = 7$, then $e + 7 = 12$. The lengths are $e{:}\,1$, $d{:}\,2$, $c{:}\,3$, $a{:}\,4$, $b{:}\,4$. Total bits $= 5 \cdot 1 + 3 \cdot 2 + 2 \cdot 3 + 1 \cdot 4 + 1 \cdot 4 = 25$, about $2.08$ bits per symbol. A fixed-length code for 5 symbols needs 3 bits each, $36$ bits in total.
> 5. The densities are $2, 1.67, 1.67$. Fractional: take $(4, 8)$, then $2/3$ of a $(3, 5)$, for $8 + 10/3 \approx 11.33$. Density-greedy 0/1: take $(4, 8)$, after which neither $(3, 5)$ fits, for $8$. Optimum: both $(3, 5)$ items, weight $6$, value $10$. The fractional value $11.33$ is an upper bound on $10$, as expected.
> 6. Yes, they are all MSTs. The cut property in its non-strict form says a lightest edge crossing a cut (possibly tied) belongs to *some* MST, and the swap in its proof uses $w(e) \le w(f)$, which still holds under ties. Each accepted edge is a lightest edge crossing the cut around its component, so every tie-break yields an MST, and all of them have the same total weight.
> 7. Euclidean clustering is single linkage. It merges two groups as soon as *one* pair of points, one from each group, is within $r$, and it chains: points on the worker's hand are within $0.3$ m of the scaffold, so the two become one cluster. Fixes: remove known structure first (ground plane or map points), require a minimum neighbour count before a point may link (DBSCAN-style core points), use a smaller $r$ together with a second check on cluster shape or size, or segment with a learned model.
> 8. No. The set cover guarantee bounds greedy by $H(d) \cdot \mathrm{OPT}$, not by OPT itself. With $d = 4$ that bound is about $4.17$, and $3$ is within it. Before citing $(1 - 1/e)$, check that the objective is monotone (more views never hurt), submodular (a view adds less to a larger set, which holds for coverage area but can fail for objectives with synergy, such as triangulation needing two views together), that $f(\varnothing) = 0$, and that the constraint is a plain cardinality budget $k$ rather than a travel-cost or path constraint.

### Sources

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.), chapters on greedy algorithms and minimum spanning trees. MIT Press.
- Kleinberg, J., & Tardos, É. (2005). *Algorithm Design*, ch. 4 (greedy algorithms; the "stays ahead" and exchange proof styles). Pearson/Addison-Wesley.
- Roughgarden, T. (2019). *Algorithms Illuminated, Part 3: Greedy Algorithms and Dynamic Programming*. Soundlikeyourself Publishing.
- Kulikov, A., & Pevzner, P. (2018). *Learning Algorithms Through Programming and Puzzle Solving*, greedy-algorithms chapter. Active Learning Technologies.
- Smith, W. E. (1956). Various optimizers for single-stage production. *Naval Research Logistics Quarterly*, 3(1–2), 59–66.
- Huffman, D. A. (1952). A method for the construction of minimum-redundancy codes. *Proceedings of the IRE*, 40(9), 1098–1101. https://doi.org/10.1109/JRPROC.1952.273898
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.), ch. 5 (data compression). Wiley.
- Jarník, V. (1930). O jistém problému minimálním. *Práce moravské přírodovědecké společnosti*, 6, 57–63.
- Kruskal, J. B. (1956). On the shortest spanning subtree of a graph and the traveling salesman problem. *Proceedings of the American Mathematical Society*, 7(1), 48–50. https://doi.org/10.1090/S0002-9939-1956-0078686-7
- Prim, R. C. (1957). Shortest connection networks and some generalizations. *Bell System Technical Journal*, 36(6), 1389–1401. https://doi.org/10.1002/j.1538-7305.1957.tb01515.x
- Tarjan, R. E. (1975). Efficiency of a good but not linear set union algorithm. *Journal of the ACM*, 22(2), 215–225.
- Gower, J. C., & Ross, G. J. S. (1969). Minimum spanning trees and single linkage cluster analysis. *Journal of the Royal Statistical Society, Series C (Applied Statistics)*, 18(1), 54–64.
- Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining (KDD)*, 226–231.
- Johnson, D. S. (1974). Approximation algorithms for combinatorial problems. *Journal of Computer and System Sciences*, 9(3), 256–278.
- Lovász, L. (1975). On the ratio of optimal integral and fractional covers. *Discrete Mathematics*, 13(4), 383–390.
- Chvátal, V. (1979). A greedy heuristic for the set-covering problem. *Mathematics of Operations Research*, 4(3), 233–235. https://doi.org/10.1287/moor.4.3.233
- Dinur, I., & Steurer, D. (2014). Analytical approach to parallel repetition. *Proceedings of the 46th ACM Symposium on Theory of Computing (STOC)*.
- Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming*, 14(1), 265–294. https://doi.org/10.1007/BF01588971
- Minoux, M. (1978). Accelerated greedy algorithms for maximizing submodular set functions. In *Optimization Techniques*, Lecture Notes in Control and Information Sciences, vol. 7, 234–243. Springer.
- Krause, A., & Guestrin, C. (2005). Near-optimal nonmyopic value of information in graphical models. *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI)*.
- Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research*, 9, 235–284.

## 한국어

그리디(탐욕) 알고리즘은 되돌릴 수 없는 선택을 하나씩 쌓아 답을 만든다. 매번 지금 당장 가장 좋아 보이는 것을 고른다. 그리디 알고리즘은 떠올리기 쉽고, 실행 시간도 대개 정렬 한 번이나 힙 하나의 비용이면 끝난다. 어려운 점은 대부분이 틀렸다는 데 있다. §1에서 동전 $\{1, 3, 4\}$로 6을 낼 때 늘 가장 큰 동전부터 고르면 두 개로 될 것을 세 개 쓴다. 그래서 면접은 두 가지를 본다. 하나는 올바른 규칙, 예컨대 어떤 키로 정렬할지를 고르는 능력이다. 다른 하나는 그 규칙이 왜 맞는지 설명하거나, 틀리게 만드는 작은 입력을 찾아내는 능력이다. 이 페이지는 그리디가 정확히 최적인 표준 문제들, 즉 구간 스케줄링, 가중 스케줄링, 분할 가능 배낭, 허프만 부호, 최소 신장 트리를 다룬다. 이어서 NP-난해 문제(대략, 다항 시간 정확 알고리즘이 알려져 있지 않은 문제. 정의는 [[02-foundations/algorithms/complexity-recursion#P, NP, NP-난해, 의사 다항 시간|11.1 §1]])에서 그리디가 가장 실용적인 도구이면서 증명된 근사 비율까지 갖는 경우를 다룬다. 센서 배치와 시점 계획(view planning) 논문이 그리디를 쓰는 방식이 바로 이것이다.

면접이 묻는 것: "겹치지 않는 구간의 최대 개수", "최소 회의실 수", "구간 병합", 허프만 부호, 백지에서 Prim이나 Kruskal 구현, 그리고 "증명해 보라" 또는 "여기서는 왜 그리디가 안 되는가". 로봇 연구실은 여기에 점군의 유클리드 군집화(§6)와 그리디 센서·시점 선택(§7)을 더한다.

> [!note] 처음이라면 · First pass
> §1을 꼼꼼히 읽는다. 두 가지 증명 패턴과 반례부터 찾는 습관을 이후 모든 절이 다시 쓴다. 그다음 가장 자주 나오는 §2와 §6을 코드를 열어 두고 푼다. §3–§5는 문제 하나씩 다루는 짧은 절이다. §7은 연구 논문을 읽을 때 쓰고, §8은 면접 전에 읽을 점검표다.

### 1. 무엇이 선택을 그리디하게 만드는가, 그리고 증명하거나 깨뜨리는 법

**한 문장 요약:** 단순한 국소 규칙으로 가장 좋은 선택을 하고, 그 선택에 확정한 뒤, 남은 문제를 같은 방식으로 푼다.

**그리디 알고리즘이란.** 해가 선택의 연속으로 만들어지는 최적화 문제를 위한 알고리즘 설계 패러다임이며, 이름 붙은 네 부분을 갖는다.

- **후보**(candidates): 해를 이루는 조각들(구간, 간선, 동전).
- **선택 규칙**(selection rule): 후보에 순위를 매기는 단순한 키.
- **실현 가능성 검사**(feasibility test): 후보를 부분해에 더할 수 있는지 판정한다.
- **되돌리지 않는 확정**(irrevocable commitment): 한 번 고른 후보는 빼거나 다시 검토하지 않는다.

가장 큰 동전부터 내는 거스름돈, Kruskal, 허프만 부호가 모두 정확히 이 네 부분을 갖는다.

**옳을 조건.** 사례를 $I$, 그리디의 첫 선택을 $g$, $g$를 확정한 뒤 남는 더 작은 사례를 $I_g$, 최적값을 $\mathrm{OPT}(\cdot)$라 쓰자. 두 속성이 필요하다.

- **그리디 선택 속성**(greedy-choice property): $I$의 어떤 최적해가 $g$를 포함한다. 모든 최적해일 필요는 없고 하나면 된다.
- **최적 부분 구조**(optimal substructure): $g$를 포함하는 $I$의 최적해는 $g$와 $I_g$의 최적해로 이루어진다. 그래서 비용이 선택들에 대해 더해지는 경우
$$\mathrm{OPT}(I) = c(g) + \mathrm{OPT}(I_g)$$
  이다. 여기서 $c(g)$는 선택 $g$ 자체의 비용 또는 가치다.

첫 선택이 아무것도 잃지 않고 남는 것이 다시 같은 문제이므로, 두 속성이 함께 사례 크기에 대한 귀납법으로 그리디의 정당성을 증명한다. **반례:** 동전 $\{1, 3, 4\}$로 $6$을 낼 때 그리디의 첫 선택은 동전 $4$지만, 동전 두 개짜리 해는 $3 + 3$뿐이다. 어떤 최적해도 $4$를 포함하지 않으므로 그리디 선택 속성이 깨진다. 최적 부분 구조는 여전히 성립하며, 그래서 동적 계획법으로는 풀린다. 동적 계획법은 두 번째 속성만 필요하고, 그 대가로 결정마다 모든 선택지를 시도한다([[02-foundations/algorithms/dynamic-programming|11.5 §1]]). 그리디는 선택지 하나만 믿으므로, 그 하나로 충분하다는 증명이 필요하다.

그 증명을 쓰는 표준적인 방법은 두 가지다.

**방법 1: 그리디가 앞서 간다(greedy stays ahead).** 매 단계 뒤에 비교할 수 있는 진행 척도를 정한다. 예를 들어 "경로를 얼마나 갔나", "구간을 몇 개 배정했나", "마지막으로 고른 구간의 종료 시각" 같은 것이다. 모든 단계 $k$ 뒤에 그리디의 척도가 *다른 어떤* 유효한 해의 $k$단계 뒤 척도보다 나쁘지 않음을 귀납법으로 보인다. 해 $S$의 $k$단계 뒤 척도를 $m_k(S)$라 하면 증명할 주장은
$$m_k(G) \succeq m_k(O) \quad \text{for every step } k \text{ and every valid solution } O$$
이다. $\succeq$는 "적어도 그만큼 좋다"는 뜻이므로, 클수록 좋은 척도라면 $\ge$, 작을수록 좋은 척도라면 $\le$다. 그다음 매 단계 앞서 있다는 사실로부터 그리디가 더 늦게 끝나거나 더 적게 고를 수 없음을 보인다.

**방법 2: 교환 논증(exchange argument).** 그리디 해 $G$와 다른 임의의 최적해 $O$를 잡는다. 둘이 처음 달라지는 곳을 찾아, $O$를 무효로 만들지도 더 나쁘게 만들지도 않으면서 그 자리를 $G$와 같게 바꾼다. 즉 바뀐 해 $O'$는 유효하고 $\text{cost}(O') \le \text{cost}(O)$다. 이것을 반복하면 $O$가 한 단계씩 $G$로 바뀌고 그동안 비용은 늘지 않으므로 $G$도 최적이다. 같은 논증의 짧은 형태는 그리디의 *첫* 선택을 어떤 최적해에 끼워 넣을 수 있다는 것만 보이고, 나머지는 최적 부분 구조로 반복한다.

두 방법은 서로 바꿔 쓸 수 있는 경우가 많다. 앞서 가기 논증은 해가 직선을 따라 또는 시간 순으로 만들어지는 문제에 잘 맞는다. 교환 논증은 답이 순서나 집합이고, 두 원소를 맞바꿀 때의 비용 변화를 계산할 수 있는 문제에 잘 맞는다.

> [!example] 계산 예제 · Worked example
> 이동 로봇이 곧은 복도를 따라 위치 $0$에서 $20$ m 지점의 목표까지 간다. 완충 상태로 출발하고 한 번 충전으로 $6$ m를 간다. 충전 도크는 $3, 5, 9, 12, 16$에 있다. 그리디 규칙: 다음 도크(또는 목표)에 아직 닿을 수 있으면 지나치고, 닿을 수 있는 가장 먼 도크에서만 충전한다. $0$에서 닿는 가장 먼 도크는 $5$, 다음은 $9$(도달 한계 $11$), $12$(한계 $15$), $16$(한계 $18$)이다. $16$에서는 $22 \ge 20$까지 갈 수 있다. 총 **4번** 충전한다. 앞서 가기 증명: 그리디와 임의의 다른 계획의 $k$번째 충전 위치를 $g_k$, $o_k$라 하자. $g_{k-1} \ge o_{k-1}$이라 가정한다. 다른 계획의 다음 도크는 $o_k \le o_{k-1} + 6 \le g_{k-1} + 6$을 만족하므로 그리디도 닿을 수 있었고, 그리디는 그런 도크 중 가장 먼 것을 골랐다. 따라서 $g_k \ge o_k$다. 다른 계획이 $m$번 충전 후 목표에 닿는다면 $g_m + 6 \ge o_m + 6 \ge 20$이므로 그리디도 많아야 $m$번 충전으로 닿는다.

<svg viewBox="0 0 560 230" style="max-width:100%;height:auto" role="img" aria-label="20 m 복도에서 도크가 3, 5, 9, 12, 16 m에 있고 한 번 충전으로 6 m를 간다. 각 행은 충전 한 번의 도달 구간이고, 그리디는 그 안의 가장 먼 도크인 5, 9, 12, 16에서 충전해 모두 네 번 충전한다. 16에서는 도달 한계 22가 목표 20을 넘는다.">
  <text x="8" y="18" font-size="12" fill="currentColor">한 번 충전에 6 m; 그리디는 닿는 가장 먼 도크에서 충전한다</text>
  <rect x="30" y="38" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <rect x="94" y="41.5" width="7" height="7" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.8"/>
  <circle cx="142.5" cy="45" r="4.5" stroke="none" fill="currentColor"/>
  <text x="171" y="49" font-size="11" fill="currentColor">5에서 충전 1</text>
  <text x="97.5" y="35" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.8">3: 지나침</text>
  <rect x="142.5" y="64" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="232.5" cy="71" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="142.5" y1="50" x2="142.5" y2="64" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="283.5" y="75" font-size="11" fill="currentColor">9에서 충전 2</text>
  <rect x="232.5" y="90" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="300" cy="97" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="232.5" y1="76" x2="232.5" y2="90" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="373.5" y="101" font-size="11" fill="currentColor">12에서 충전 3</text>
  <rect x="300" y="116" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <circle cx="390" cy="123" r="4.5" stroke="none" fill="currentColor"/>
  <line x1="300" y1="102" x2="300" y2="116" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="441" y="127" font-size="11" fill="currentColor">16에서 충전 4</text>
  <rect x="390" y="142" width="135" height="14" stroke="currentColor" stroke-width="1" fill="currentColor" fill-opacity="0.07" stroke-opacity="0.55"/>
  <line x1="390" y1="128" x2="390" y2="142" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="2 2"/>
  <text x="384" y="153" font-size="11" fill="currentColor" text-anchor="end">16 + 6 = 22 ≥ 20: 목표 도착</text>
  <line x1="30" y1="180" x2="525" y2="180" stroke="currentColor" stroke-width="1.2"/>
  <line x1="30" y1="176" x2="30" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="30" y="197" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <line x1="97.5" y1="176" x2="97.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="97.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <line x1="142.5" y1="176" x2="142.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="142.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="232.5" y1="176" x2="232.5" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="232.5" y="197" font-size="11" fill="currentColor" text-anchor="middle">9</text>
  <line x1="300" y1="176" x2="300" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="300" y="197" font-size="11" fill="currentColor" text-anchor="middle">12</text>
  <line x1="390" y1="176" x2="390" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="197" font-size="11" fill="currentColor" text-anchor="middle">16</text>
  <line x1="480" y1="176" x2="480" y2="184" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="197" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <rect x="94" y="176.5" width="7" height="7" stroke="currentColor" stroke-width="1.2" fill="none"/>
  <rect x="139" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="229" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="296.5" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <rect x="386.5" y="176.5" width="7" height="7" stroke="none" fill="currentColor"/>
  <line x1="480" y1="176" x2="480" y2="158" stroke="currentColor" stroke-width="1.4"/>
  <path d="M480 158 L491 161.5 L480 165 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="494" y="168" font-size="10" fill="currentColor" fill-opacity="0.85">목표</text>
  <text x="525" y="216" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">복도 위치 (m)</text>
</svg>

```python
def min_charges(docks, reach, goal):
    """Fewest charging stops from 0 to goal, or -1 if some gap exceeds reach."""
    docks = sorted(docks)
    stops, pos, i = 0, 0, 0
    while pos + reach < goal:
        farthest = pos
        while i < len(docks) and docks[i] <= pos + reach:
            farthest = docks[i]              # keep walking: a later dock is better
            i += 1
        if farthest == pos:
            return -1                        # no dock ahead within reach
        pos, stops = farthest, stops + 1
    return stops

print(min_charges([3, 5, 9, 12, 16], 6, 20))  # 4
print(min_charges([2, 9], 6, 12))             # -1
```

정렬에 $O(n \log n)$, 훑기에 $O(n)$이 든다. 인덱스 `i`가 앞으로만 움직이기 때문이다.

**그리디 아이디어를 빨리 깨뜨리는 법.** 무엇이든 증명하려 들기 전에, 원소 두세 개짜리 반례를 1분 동안 찾아본다. 거의 동점인 원소들, 아주 큰 원소 하나와 작은 원소 여러 개, 그리디 규칙의 첫 선택이 이후 선택 두 개를 막아 버리는 입력을 시도한다.

- **동전 $\{1, 3, 4\}$로 금액 $6$ 거슬러 주기.** 큰 동전부터 고르면 $4 + 1 + 1$로 세 개다. 최적은 $3 + 3$으로 두 개다. $\{1, 5, 10, 25\}$ 같은 일부 동전 체계에서는 큰 동전 우선이 우연히 최적이지만, 그것은 그 액면가들의 성질이다. 일반 문제에는 DP가 필요하다([[02-foundations/algorithms/dynamic-programming|11.5 §3]]).
- **가치/무게 비율로 푸는 0/1 배낭.** 용량 $10$. 물건(무게, 가치): 비율 $1.5$인 $(6, 9)$ 하나와 비율 $1.4$인 $(5, 7)$ 두 개. 그리디는 $(6, 9)$를 먼저 넣고, 그러면 $(5, 7)$은 어느 것도 들어가지 않아 가치 $9$다. $(5, 7)$ 두 개는 용량을 정확히 채워 가치 $14$다. 물건을 자를 수 있게 되면 같은 규칙이 왜 옳아지는지는 §4에서 설명한다.

반례 하나는 "이 그리디가 맞는가?"에 대한 완전한 답이다. 증명은 반대쪽 답을 낼 때만 필요하다.

### 2. 구간 문제

구간은 면접에서 가장 흔한 그리디 유형이다. 먼저 끝점 규약을 정하고 소리 내어 말한다. 이 페이지는 **반열린** 구간 $[s, e) = \{t : s \le t < e\}$를 쓴다. 시작 시각은 포함하고 종료 시각은 포함하지 않는다. 두 구간은 시각을 공유할 때 정확히 겹친다.
$$[s_1, e_1) \cap [s_2, e_2) \ne \varnothing \iff s_1 < e_2 \ \text{ and } \ s_2 < e_1$$
각자 상대가 끝나기 전에 시작해야 하기 때문이다. 그래서 $10$에 끝나는 예약과 $10$에 시작하는 예약은 충돌하지 않는다. $[8, 10)$과 $[10, 12)$에서 $10 < 10$이 거짓이다. 닫힌 구간 $[s, e]$는 두 곳 모두 $\le$를 쓰며, 그러면 $[1, 3]$과 $[3, 5]$는 시각 $3$에서 겹친다.

#### 활동 선택: 겹치지 않는 구간을 최대한 많이

**문제.** 구간 $n$개가 주어지면, 위의 뜻으로 겹치는 두 구간이 없는 부분집합 $S$ 중 크기 $|S|$가 가장 큰 것을 고른다.

**한 문장 요약:** 마지막으로 고른 구간 이후에 시작하는 구간 중 가장 먼저 *끝나는* 것을 반복해서 고른다.

**가장 빠른 종료가 안전한 이유(교환).** 종료 시각이 가장 이른 구간을 $a$, 겹치지 않는 구간들의 임의의 최적 집합을 시간 순으로 정렬한 것을 $O$라 하자. $O$의 첫 구간 $o_1$을 $a$로 바꾼다. $a$는 $o_1$보다 늦게 끝나지 않으므로 $O$의 다른 모든 구간이 시작하기 전에 끝난다. 따라서 새 집합도 겹치지 않고 크기가 같다. 즉 어떤 최적해는 $a$를 포함한다. $a$와 $a$에 겹치는 구간들을 모두 지우면 남는 것은 더 작은 입력의 같은 문제이고, 논증이 반복된다.

**다른 그럴듯한 키가 실패하는 이유.** *가장 빠른 시작:* $[0, 10), [1, 2), [3, 4)$에서 1개를 고르지만 2개가 가능하다. *가장 짧은 것 먼저:* $[0, 5), [4, 6), [6, 10)$에서 짧은 $[4, 6)$을 고르면 나머지 둘이 모두 막혀 2개 대신 1개가 된다. *겹침이 가장 적은 것 먼저*도 반례가 있지만, 만들려면 구간이 더 많이 필요하다.

```python
def max_activities(intervals):
    """intervals: (start, end), half-open. Returns a largest non-overlapping subset."""
    chosen = []
    last_end = float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):  # by finish time
        if start >= last_end:               # >= because [s, e) may touch
            chosen.append((start, end))
            last_end = end
    return chosen

jobs = [(0, 3), (1, 2), (2, 5), (4, 6), (5, 8), (7, 9), (8, 10)]
print(max_activities(jobs))  # [(1, 2), (2, 5), (5, 8), (8, 10)]
```

정렬에 $O(n \log n)$, 훑기에 $O(n)$이 든다. 가까운 문제로 "모든 구간을 찌르는 최소 점 개수"가 있다. 예를 들어 모든 입주자나 작업조가 적어도 한 번은 있을 때 현장을 방문하려면 최소 몇 번 가야 하는가 하는 문제다. 종료 시각으로 정렬하고 고른 구간의 종료 시각마다 점을 찍으면 풀리며, 필요한 점의 최소 개수는 서로소 구간의 최대 개수와 같다.

<svg viewBox="0 0 560 297" style="max-width:100%;height:auto" role="img" aria-label="작업 일곱 개를 종료 시각 순으로 시간축 위 막대로 그렸다. 가장 빠른 종료 그리디는 [1, 2), [2, 5), [5, 8), [8, 10)을 고르고, 마지막으로 고른 종료 시각보다 먼저 시작하는 셋을 건너뛴다. 아래는 각 시각에 진행 중인 작업 수이며 최대 2, 즉 깊이가 2이므로 회의실 2개면 된다.">
  <text x="8" y="18" font-size="12" fill="currentColor">종료 시각 순 정렬; 채운 막대 = 선택, 점선 = 건너뜀</text>
  <line x1="158" y1="30" x2="158" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="284" y1="30" x2="284" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="410" y1="30" x2="410" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <line x1="494" y1="30" x2="494" y2="187" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="2 3"/>
  <text x="64" y="45.5" font-size="11" fill="currentColor" text-anchor="end">[1, 2)</text>
  <rect x="116" y="36" width="42" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="164" y="45.5" font-size="10" fill="currentColor" fill-opacity="0.8">선택</text>
  <text x="64" y="66.5" font-size="11" fill="currentColor" text-anchor="end">[0, 3)</text>
  <rect x="74" y="57" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="206" y="66.5" font-size="10" fill="currentColor" fill-opacity="0.8">건너뜀: 0 &lt; 2</text>
  <text x="64" y="87.5" font-size="11" fill="currentColor" text-anchor="end">[2, 5)</text>
  <rect x="158" y="78" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="290" y="87.5" font-size="10" fill="currentColor" fill-opacity="0.8">선택</text>
  <text x="64" y="108.5" font-size="11" fill="currentColor" text-anchor="end">[4, 6)</text>
  <rect x="242" y="99" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="332" y="108.5" font-size="10" fill="currentColor" fill-opacity="0.8">건너뜀: 4 &lt; 5</text>
  <text x="64" y="129.5" font-size="11" fill="currentColor" text-anchor="end">[5, 8)</text>
  <rect x="284" y="120" width="126" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="416" y="129.5" font-size="10" fill="currentColor" fill-opacity="0.8">선택</text>
  <text x="64" y="150.5" font-size="11" fill="currentColor" text-anchor="end">[7, 9)</text>
  <rect x="368" y="141" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="none" stroke-opacity="0.7" stroke-dasharray="4 3"/>
  <text x="458" y="150.5" font-size="10" fill="currentColor" fill-opacity="0.8">건너뜀: 7 &lt; 8</text>
  <text x="64" y="171.5" font-size="11" fill="currentColor" text-anchor="end">[8, 10)</text>
  <rect x="410" y="162" width="84" height="11" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.45"/>
  <text x="500" y="171.5" font-size="10" fill="currentColor" fill-opacity="0.8">선택</text>
  <line x1="74" y1="187" x2="494" y2="187" stroke="currentColor" stroke-width="1.2"/>
  <line x1="74" y1="187" x2="74" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="74" y="203" font-size="10" fill="currentColor" text-anchor="middle">0</text>
  <line x1="116" y1="187" x2="116" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="116" y="203" font-size="10" fill="currentColor" text-anchor="middle">1</text>
  <line x1="158" y1="187" x2="158" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="158" y="203" font-size="10" fill="currentColor" text-anchor="middle">2</text>
  <line x1="200" y1="187" x2="200" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="203" font-size="10" fill="currentColor" text-anchor="middle">3</text>
  <line x1="242" y1="187" x2="242" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="242" y="203" font-size="10" fill="currentColor" text-anchor="middle">4</text>
  <line x1="284" y1="187" x2="284" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="203" font-size="10" fill="currentColor" text-anchor="middle">5</text>
  <line x1="326" y1="187" x2="326" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="326" y="203" font-size="10" fill="currentColor" text-anchor="middle">6</text>
  <line x1="368" y1="187" x2="368" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="368" y="203" font-size="10" fill="currentColor" text-anchor="middle">7</text>
  <line x1="410" y1="187" x2="410" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="203" font-size="10" fill="currentColor" text-anchor="middle">8</text>
  <line x1="452" y1="187" x2="452" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="452" y="203" font-size="10" fill="currentColor" text-anchor="middle">9</text>
  <line x1="494" y1="187" x2="494" y2="191" stroke="currentColor" stroke-width="1"/>
  <text x="494" y="203" font-size="10" fill="currentColor" text-anchor="middle">10</text>
  <text x="504" y="203" font-size="11" fill="currentColor" font-style="italic">t</text>
  <text x="8" y="229" font-size="11" fill="currentColor">시각 t에 진행 중인 작업 수: 최대 2, 그래서 회의실 2개</text>
  <text x="64" y="281" font-size="10" fill="currentColor" text-anchor="end">0</text>
  <line x1="74" y1="277" x2="494" y2="277" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="64" y="263" font-size="10" fill="currentColor" text-anchor="end">1</text>
  <line x1="74" y1="259" x2="494" y2="259" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <text x="64" y="245" font-size="10" fill="currentColor" text-anchor="end">2</text>
  <line x1="74" y1="241" x2="494" y2="241" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25" stroke-dasharray="2 3"/>
  <path d="M74 277 L74 259 L116 259 L116 241 L158 241 L158 241 L200 241 L200 259 L242 259 L242 241 L284 241 L284 241 L326 241 L326 259 L368 259 L368 241 L410 241 L410 241 L452 241 L452 259 L494 259 L494 277" stroke="currentColor" stroke-width="1.6" fill="currentColor" fill-opacity="0.12" stroke-linejoin="round"/>
</svg>

#### 최소 회의실: 모든 구간을 돌리려면 자원이 몇 개 필요한가

**한 문장 요약:** 시작 시각 순으로 구간을 훑으며 가장 먼저 비는 자원을 재사용하고, 모든 자원이 아직 쓰이는 중일 때만 새 자원을 연다.

**최적인 이유.** 어느 시각 $t$에서든 $t$를 포함하는 구간은 각자 자원이 필요하므로, 답은 한 점을 공통으로 포함하는 구간의 최대 개수, 즉 *깊이* 이상이다.
$$\text{depth} = \max_t \big|\{i : s_i \le t < e_i\}\big|$$
집합은 시각 $t$를 포함하는 구간을 세므로, 깊이는 동시에 진행되는 구간의 최대 개수다. 아래 코드의 작업 일곱 개에서는 $2$다. 알고리즘은 힙의 가장 이른 종료 시각이 현재 시작 시각보다 늦을 때만 새 자원을 연다. 그 순간 열린 자원마다 더 일찍 또는 같은 시각에 시작해 아직 진행 중인 구간이 있으므로, 새 구간과 함께 모두 현재 시작 시각을 포함한다. 따라서 새 개수는 깊이 이하다. 알고리즘은 하한인 깊이보다 많은 자원을 쓰지 않는다.

```python
import heapq

def min_rooms(intervals):
    """Fewest resources so that no two overlapping half-open intervals share one."""
    ends = []                               # min-heap: end time of each busy resource
    for start, end in sorted(intervals):    # by start time
        if ends and ends[0] <= start:
            heapq.heapreplace(ends, end)    # reuse the resource that frees first
        else:
            heapq.heappush(ends, end)       # all busy: open a new one
    return len(ends)

print(min_rooms([(0, 3), (1, 2), (2, 5), (4, 6), (5, 8), (7, 9), (8, 10)]))  # 2
print(min_rooms([(1, 3), (3, 5), (2, 4)]))  # 2; with closed intervals it would be 3
```

시간 $O(n \log n)$. 힙 없이 같은 일을 하는 방법도 있다. 각 구간을 시작 시각의 $+1$ 사건과 종료 시각의 $-1$ 사건으로 바꿔 정렬하고 누적합을 추적한다. 반열린 구간이면 같은 시각에서 $-1$이 $+1$보다 앞에 와야 한다. 로보틱스에서는 "시간 창이 정해진 이 작업들을 돌리려면 로봇, 충전 도크, 크레인 슬롯이 몇 개 필요한가?"에 대한 답이다.

#### 구간 병합

**한 문장 요약:** 시작 시각으로 정렬하고, 마지막으로 병합한 구간을 늘리거나 새 구간을 시작한다.

```python
def merge_intervals(intervals):
    """Union of intervals as a sorted list of disjoint ones. Touching ones merge."""
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # max: the new one may be inside
        else:
            merged.append([start, end])
    return [tuple(iv) for iv in merged]

print(merge_intervals([(4, 7), (1, 3), (2, 5), (9, 10), (10, 12)]))  # [(1, 7), (9, 12)]
```

그리디라고 부르기도 민망할 만큼 단순하지만 고전적인 버그가 두 개 있다. 한 구간이 다른 구간 안에 들어 있을 때 `max`를 빠뜨리는 것, 그리고 끝점 규약과 맞지 않게 `<`와 `<=`를 섞어 쓰는 것이다. 로보틱스 활용: 2차원 스캔은 장애물마다 막힌 각도 구간을 준다. 이를 병합하면 반응형 플래너가 빠져나갈 수 있는 빈 틈이 남는다. 각도는 $\pm\pi$에서 한 바퀴 돌아오므로, 정렬하기 전에 그 경계를 가로지르는 구간은 둘로 나눈다.

### 3. 가중 완료 시간을 최소화하는 스케줄링

**문제.** 기계 하나(로봇 팔 하나, 프린터 하나, CPU 하나)가 작업을 하나씩 처리한다. 작업 $j$는 길이 $l_j > 0$와 가중치 $w_j$를 갖는다. 가중치는 기다리는 시간 한 단위가 얼마나 비싼지를 나타낸다. 작업 $j$의 완료 시간 $C_j$는 $j$까지(포함) 처리된 모든 작업 길이의 합이다. 목표는 총 가중 완료 시간의 최소화다.
$$C_j = \sum_{k \preceq j} l_k, \qquad \text{minimize } \sum_j w_j C_j$$
여기서 $k \preceq j$는 작업 $k$가 $j$보다 먼저 돌거나 $j$ 자신이라는 뜻이다. 그래서 작업의 완료 시간에는 자기 길이와 앞에 배정된 모든 길이가 들어간다.

**한 문장 요약:** $w_j / l_j$가 큰 순서로, 즉 처리 시간 한 단위당 가중치가 가장 큰 작업부터 돌린다(Smith 1956).

**교환 증명.** 임의의 스케줄에서 *이웃한* 두 작업 $i$, $j$(이 순서)를 잡는다. 둘을 맞바꿔도 다른 작업의 완료 시간은 바뀌지 않는다. 두 작업이 여전히 같은 시간 구간을 차지하기 때문이다. 맞바꾸면 $j$는 $l_i$만큼 일찍 끝나고 $i$는 $l_j$만큼 늦게 끝난다. 따라서 총비용의 변화는

$$\Delta = w_i\, l_j - w_j\, l_i,$$

이고, $\Delta < 0$일 때 정확히 이득이다. $l_i l_j > 0$으로 나누면 $w_i / l_i < w_j / l_j$일 때이므로, 비율이 낮은 작업이 비율이 높은 작업 바로 앞에 있으면 맞바꾸는 것이 이득이다. 이제 최적 스케줄을 잡자. 비율 순서가 아니라면 순서가 뒤집힌 이웃 쌍이 있고, 그 쌍을 맞바꿔도 비용은 늘지 않는다(비율이 같으면 그대로다). 맞바꿀 때마다 뒤집힌 쌍이 하나씩 줄어드므로, 많아야 $\binom{n}{2}$번 맞바꾸면 최적 스케줄이 비용 증가 없이 그리디 스케줄이 된다. 따라서 동점을 포함해 그리디가 최적이다.

**차이 $w_j - l_j$로 정렬하면 실패하는 이유.** 차이는 두 특수한 경우와 모두 맞아떨어져서 그럴듯해 보인다. 길이가 같으면 무거운 작업이 먼저, 가중치가 같으면 짧은 작업이 먼저다. 하지만 두 기준이 서로 반대 방향을 가리키면 실패한다. 작업 A는 $w = 6, l = 4$로 차이 $2$, 비율 $1.5$다. 작업 B는 $w = 2, l = 1$로 차이 $1$, 비율 $2$다.

- 차이 순서 A, B: $C_A = 4$, $C_B = 5$, 비용 $6 \cdot 4 + 2 \cdot 5 = 34$.
- 비율 순서 B, A: $C_B = 1$, $C_A = 5$, 비용 $2 \cdot 1 + 6 \cdot 5 = 32$.

따라서 차이 순서는 최적이 아니다. 후보 키 두 개 중 하나를 고르는 일반적인 방법이 이것이다. 두 키의 순서가 엇갈리는 작은 입력을 찾아 양쪽 비용을 계산한다.

> [!example] 계산 예제 · Worked example
> 작업(가중치, 길이): $(3, 1)$, $(5, 2)$, $(2, 4)$, 비율은 $3$, $2.5$, $0.5$. 비율 순서의 완료 시간은 $1, 3, 7$이고 비용은 $3 \cdot 1 + 5 \cdot 3 + 2 \cdot 7 = 32$다. $3! = 6$가지 순서를 모두 확인하면 $32$가 최소임을 알 수 있다.

```python
from fractions import Fraction

def order_jobs(jobs):
    """jobs: (weight, length), length > 0. Order minimizing sum of w * C."""
    return sorted(jobs, key=lambda j: Fraction(-j[0], j[1]))  # exact ratio, descending

def weighted_completion(order):
    t = total = 0
    for w, l in order:
        t += l                    # completion time of this job
        total += w * t
    return total

print(weighted_completion(order_jobs([(3, 1), (5, 2), (2, 4)])))  # 32
print(weighted_completion([(6, 4), (2, 1)]), weighted_completion(order_jobs([(6, 4), (2, 1)])))  # 34 32
```

`Fraction`은 비율의 동점을 정확히 유지한다. 부동소수점에서는 수학적으로 같은 두 비율이 다르게 비교될 수 있다. 여기서는 동점이 최적 비용을 바꾸지 않지만, 동점 처리가 답을 바꾸는 문제에서는 같은 버그가 문제가 된다. C++에서는 나누지 말고 64비트 정수로 `a.w * b.l > b.w * a.l`을 비교한다.

### 4. 분할 가능 배낭(그리디가 된다) vs 0/1 배낭(안 된다)

**분할 가능 배낭.** 물건은 무게 $w_i$와 가치 $v_i$를 갖고, 각 물건의 일부만 가져갈 수도 있다. 물건 $i$를 가져가는 비율을 $x_i$, 용량을 $W$라 하면 문제는 다음과 같다.
$$\max \sum_i v_i x_i \quad \text{subject to} \quad \sum_i w_i x_i \le W, \qquad 0 \le x_i \le 1$$
즉 담은 총무게가 용량에 맞고 어느 물건도 한 번보다 많이 담지 않는다. **0/1 배낭**(0/1 knapsack)은 $x_i \in \{0, 1\}$로 바꾼 같은 문제로, 모든 물건을 통째로 담거나 두고 간다. $W = 10$인 §1의 사례에서 아래 그리디 규칙은 물건 $(6, 9), (5, 7), (5, 7)$에 $x = (1, 0.8, 0)$을 주어 $9 + 0.8 \cdot 7 = 14.6$을 얻는다. **한 문장 요약:** 가치 밀도 $v_i / w_i$가 큰 순서로 담고, 남은 용량에 맞게 마지막 물건을 자른다.

**옳은 이유(교환).** 어떤 해가 가장 밀도 높은 물건을 다 담지 않은 채 덜 밀도 높은 물건을 어느 양 $\varepsilon$만큼 담고 있다고 하자. 덜 밀도 높은 물건의 무게 $\varepsilon$을 가장 밀도 높은 물건의 무게 $\varepsilon$으로 바꾼다. 총무게는 그대로이고 가치는 $\varepsilon$ 곱하기 밀도 차이만큼 오른다. 그러므로 최적해는 가장 밀도 높은 물건을 들어가는 만큼 담고, 남은 용량에서 논증이 반복된다. 정렬 때문에 시간은 $O(n \log n)$이다.

```python
def fractional_knapsack(items, capacity):
    """items: (weight, value), weight > 0. Best value when items may be cut."""
    total = 0.0
    for w, v in sorted(items, key=lambda it: it[1] / it[0], reverse=True):
        if capacity <= 0:
            break
        take = min(w, capacity)
        total += v * take / w
        capacity -= take
    return total

print(fractional_knapsack([(6, 9), (5, 7), (5, 7)], 10))  # 14.6
```

**0/1 배낭.** 물건은 통째로 담거나 두고 가야 한다. 위의 교환 단계가 실패한다. 한 물건의 $\varepsilon$을 다른 물건의 $\varepsilon$과 바꿀 수 없기 때문이다. §1의 사례가 그 피해를 보여 준다. 밀도 규칙은 $9$를 얻지만 최적은 $14$다. 이 문제는 NP-난해다. 표준적인 정확한 방법은 [[02-foundations/algorithms/dynamic-programming|11.5 §4]]의 $O(nW)$ 동적 계획법이며, 의사 다항 시간이다. 실행 시간이 $W$를 적는 비트 수가 아니라 용량 $W$의 값에 따라 늘어난다는 뜻이다([[02-foundations/algorithms/complexity-recursion#P, NP, NP-난해, 의사 다항 시간|11.1 §1]]). 두 버전을 잇는 사실 두 가지가 연구 코드에 등장한다.

- **분할 가능 최적값은 0/1 최적값의 상한이다.** 여기서는 $14.6 \ge 14$다. 분기 한정법 솔버는 이 상한으로 지금까지 찾은 최선을 이길 수 없는 부분 트리를 가지치기한다.
- **값싼 1/2 근사.** 모든 물건이 혼자서는 배낭에 들어간다고 가정한다. 밀도 순서로 들어가는 동안 담은 값과 가장 가치 큰 물건 하나의 값을 비교해 더 나은 쪽을 택한다. 결과는 0/1 최적값의 절반 이상이다. 그리디 접두부에 처음 들어가지 못한 물건 하나를 더한 값이 분할 가능 최적값 이상이기 때문이다. 자세히 보자. 밀도 순서에서 처음으로 들어가지 못하는 물건을 $j$라 하자. 분할 가능 최적해는 물건 $1, \dots, j-1$을 통째로, 물건 $j$를 일부만 담으면 용량이 가득 차므로, 그 값은 접두부 값 $V_{\text{pre}}$에 $v_j$를 더한 것 이하다. 따라서 $\mathrm{OPT}_{0/1} \le \mathrm{OPT}_{\text{frac}} \le V_{\text{pre}} + v_j \le 2 \max(V_{\text{pre}}, v_{\max})$이고, 여기서 $v_{\max}$는 가장 가치 큰 물건 하나의 값이다. §1의 사례에서는 $14 \le 14.6 \le 9 + 7 = 16$이고, 규칙은 $\max(9, 9) = 9 \ge 14/2$를 돌려준다.

### 5. 허프만 부호

**문제.** 기호들이 빈도 $p_i$로 나타난다. 어떤 부호어도 다른 부호어의 접두사가 되지 않도록 각 기호에 이진 부호어를 준다. 부호어 $c_1, \dots, c_n$을 가진 부호가
$$c_i \text{ is not a prefix of } c_j \quad \text{for all } i \ne j$$
를 만족하면 **접두사 없는 부호**(prefix-free code)라 한다. 문자열의 접두사는 그 문자열의 앞부분 전체를 말한다. 비트를 읽다가 부호어가 완성되는 순간 멈춰도 너무 일찍 멈출 일이 없으므로, 구분자 없이도 비트열을 해독할 수 있다. $\{0, 10, 11\}$은 접두사 없는 부호다. $\{0, 01, 1\}$은 아니다. $0$이 $01$의 접두사이고, 비트열 $01$이 $0, 1$인지 $01$인지 알 수 없다. 목표는 기대 부호 길이 $L = \sum_i p_i \ell_i$의 최소화다. $\ell_i$는 기호 $i$의 부호어 길이다.

**트리로서의 부호.** 접두사 없는 부호는 기호를 잎으로 갖는 이진 트리다. 왼쪽 간선은 $0$, 오른쪽 간선은 $1$을 쓰고, 부호어 길이는 잎의 깊이와 같다. 문제는 $\sum_i p_i \cdot \text{depth}_i$를 최소화하는 트리를 고르는 것이다.

**한 문장 요약:** 가장 가벼운 두 트리를 무게의 합을 갖는 하나로 합치는 일을 트리가 하나 남을 때까지 반복한다(Huffman 1952).

**최적인 이유(개요).**

1. *가장 가벼운 두 기호는 가장 깊은 곳의 형제가 될 수 있다.* 임의의 최적 트리에서 최대 깊이에 있는 형제 잎 $x, y$를 잡는다. 가장 가벼운 기호 $a$를 $x$와, 두 번째로 가벼운 $b$를 $y$와 맞바꾼다. 맞바꿀 때마다 더 가벼운 기호가 더 깊이, 더 무거운 기호가 더 얕게 가므로 비용은 늘지 않는다. 따라서 $a$와 $b$가 가장 깊은 형제인 최적 트리가 존재한다. 교환 논증이다.
2. *둘을 합쳐도 잃는 것이 없다.* $a$와 $b$를 무게 $p_a + p_b$인 메타 기호 하나로 바꾼다. $a$와 $b$가 형제인 모든 트리는 더 작은 알파벳 위의 트리에 대응하고, 두 비용의 차이는 정확히 $p_a + p_b$로 모든 트리에 같은 상수다. 그러므로 작은 알파벳의 최선 트리를 다시 펼치면 $a$와 $b$가 형제인 트리 중 최선이 되고, 1단계에 의해 그것이 전체 최적이다. 알파벳 크기에 대한 귀납으로 증명이 끝난다.

```python
import heapq
from itertools import count

def huffman_code(freq):
    """freq: dict symbol -> weight > 0 (symbols must not be tuples). Returns symbol -> bits."""
    if len(freq) == 1:
        return {s: "0" for s in freq}
    tie = count()                           # tiebreaker: heapq must never compare trees
    heap = [(w, next(tie), s) for s, w in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        w1, _, a = heapq.heappop(heap)      # the two lightest trees
        w2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, next(tie), (a, b)))
    code = {}
    stack = [(heap[0][2], "")]
    while stack:
        node, prefix = stack.pop()
        if isinstance(node, tuple):         # internal node: (left, right)
            stack.append((node[0], prefix + "0"))
            stack.append((node[1], prefix + "1"))
        else:
            code[node] = prefix
    return code

freq = {"A": 0.4, "B": 0.2, "C": 0.2, "D": 0.1, "E": 0.1}
code = huffman_code(freq)
print(sum(p * len(code[s]) for s, p in freq.items()))  # 2.2 (up to float rounding)
```

**복잡도.** $n - 1$번의 병합마다 pop 두 번과 push 한 번을 하므로 총 $O(n \log n)$이다. 무게가 이미 정렬되어 있다면 힙 대신 FIFO 큐 두 개로 $O(n)$에 병합할 수 있다. 한 큐에는 원래 잎을, 다른 큐에는 병합된 트리를 넣는데, 병합된 트리의 무게는 감소하지 않는 순서로 나온다. 파이썬에서는 `count()` 동점 처리 값이 중요하다. 무게가 같으면 `heapq`가 튜플의 다음 원소를 비교하는데, 문자열과 튜플을 비교하면 `TypeError`가 나기 때문이다.

**기대 길이와 엔트로피.** $H(p) = -\sum_i p_i \log_2 p_i$를 엔트로피라 하자([[02-foundations/information-theory|5. 정보 이론 §1]]). 허프만 부호는

$$H(p) \le L_{\text{Huffman}} < H(p) + 1$$

을 만족한다. 이유는 세 가지 사실이다. 첫째, 모든 접두사 없는 부호는 크래프트 부등식 $\sum_i 2^{-\ell_i} \le 1$을 만족한다. 부호 트리에서 깊이 $\ell_i$인 잎은 맨 아래 층 자리의 $2^{-\ell_i}$만큼을 차지하고, 두 잎이 같은 자리를 나눠 갖지 않기 때문이다. 둘째, 크래프트 부등식이 $L \ge H(p)$를 강제한다. $L - H(p) = \sum_i p_i \log_2 \bigl(p_i / 2^{-\ell_i}\bigr) \ge -\log_2 \sum_i 2^{-\ell_i} \ge 0$이기 때문인데, 첫 부등호는 젠센 부등식(KL divergence가 음수가 아니게 만드는 바로 그 단계)이고 둘째는 크래프트 부등식이다. 셋째, 길이 $\ell_i = \lceil \log_2 (1/p_i) \rceil$는 $2^{-\ell_i} \le p_i$를 주므로 크래프트 부등식을 만족하고, 정확히 그 길이를 갖는 접두사 없는 부호가 존재한다. 각 길이는 $\log_2(1/p_i) + 1$보다 작으므로 그 부호의 기대 길이는 $H(p) + 1$ 미만이고, 최적인 허프만은 적어도 그만큼 좋다.

> [!example] 계산 예제 · Worked example
> 빈도 $A{:}\,0.4$, $B{:}\,0.2$, $C{:}\,0.2$, $D{:}\,0.1$, $E{:}\,0.1$. $D$와 $E$를 합쳐 $0.2$를 만든다. 이제 무게 $0.2$인 트리가 셋이라 다음에 어느 둘을 합칠지는 동점이다. 한 가지 동점 처리는 길이 $A{:}\,1$, $B{:}\,2$, $C{:}\,3$, $D{:}\,4$, $E{:}\,4$를, 다른 처리는 $A{:}\,2$, $B{:}\,2$, $C{:}\,2$, $D{:}\,3$, $E{:}\,3$을 만든다. 둘 다 $L = 2.2$비트라서, 부호는 달라도 둘 다 최적이다. 기호 다섯 개의 고정 길이 부호는 $3$비트가 필요하다. 엔트로피는 $H = 0.4 \log_2 2.5 + 2 \cdot 0.2 \log_2 5 + 2 \cdot 0.1 \log_2 10 \approx 2.12$비트이므로, 허프만은 하한에서 $0.08$비트 이내다.

$H$와의 차이는 부호어마다 길이를 정수 비트로 반올림해서 생긴다. 분포가 매우 치우칠수록 나빠진다. $p = 0.99$인 기호도 여전히 한 비트를 쓴다. 산술 부호화와 ANS는 기호별 반올림을 피해 $H$에 더 가까워진다. 그래도 허프만 부호는 zip, gzip, PNG 안에 들어 있는 DEFLATE 형식의 엔트로피 부호화 단계로 여전히 쓰인다.

### 6. 최소 신장 트리

**정의.** $G = (V, E)$를 간선마다 가중치 $w(e)$가 있는 무방향 그래프라 하자. 무방향 그래프는 정점 집합 $V$와 간선 집합 $E$로 이루어지고, 각 간선은 서로 다른 두 정점의 순서 없는 쌍 $\{u, v\}$이며 $u\text{–}v$로 쓴다(저장하는 법은 [[02-foundations/algorithms/graph-algorithms|11.6 §1]]). 모든 두 정점이 경로로 이어져 있으면 $G$는 **연결**(connected)되어 있다. **사이클**(cycle)은 $k \ge 3$이고 $v_0, \dots, v_{k-1}$이 서로 다른 닫힌 경로 $v_0, v_1, \dots, v_k = v_0$이다. **트리**(tree)는 사이클이 없는 연결 그래프다. 연결된 $G$의 **신장 트리**(spanning tree)는 다음 세 조건을 만족하는 간선 집합 $T \subseteq E$다.

- **신장**(spanning): $V$ 전체 위에서 잡으므로 모든 정점이 그래프 $(V, T)$에 속한다.
- **연결**(connected): $(V, T)$에서 모든 두 정점 사이에 경로가 있다.
- **비순환**(acyclic): $T$에 사이클이 없다.

모든 신장 트리는 간선이 정확히 $|V| - 1$개이고, $V$ 전체 위의 간선 집합에서는 "연결", "비순환", "$|T| = |V| - 1$" 중 둘이 성립하면 나머지 하나도 성립한다. 이유는 세기다. 고립된 정점 $|V|$개에서 시작해 간선을 하나씩 더한다. 서로 다른 두 성분을 잇는 간선은 성분 수를 하나 줄이고, 한 성분 안의 간선은 사이클을 닫을 뿐 아무것도 줄이지 않는다. 그래서 간선 $|T|$개 뒤에는 성분이 적어도 $|V| - |T|$개 남고, 사이클을 닫은 간선이 없을 때만 등호가 성립하며, 사이클 없는 성분 하나에는 정확히 $|V| - 1$개의 간선이 필요하다.

**최소 신장 트리**(minimum spanning tree, MST)는 총가중치가 가장 작은 신장 트리다.
$$T^* = \arg\min_{T \text{ spanning tree of } G} w(T), \qquad w(T) = \sum_{e \in T} w(e)$$
최솟값은 유한 개의 신장 트리 위에서 잡으므로 $G$가 연결되어 있으면 MST가 항상 존재하지만, 가중치가 같으면 유일하지 않을 수 있다. 음의 가중치도 괜찮고, 최대 신장 트리는 모든 가중치의 부호를 바꿔 구한다.

**예와 반례.** 아래 코드의 정점 다섯 개 그래프에는 신장 트리가 21개 있고 총가중치는 $12$부터 $20$까지다. MST는 가중치 $12$인 유일한 트리 $\{0\text{–}2, 1\text{–}3, 1\text{–}2, 3\text{–}4\}$다. 간선 집합 $\{0\text{–}1, 0\text{–}2, 1\text{–}2, 1\text{–}3\}$도 간선이 $4 = |V| - 1$개지만 신장 트리가 아니다. 사이클 $0\text{–}1\text{–}2\text{–}0$을 포함하고 정점 $4$에 닿지 않는다.

**컷 속성.** *컷*은 정점을 공집합이 아닌 두 그룹 $(S, V \setminus S)$로 나눈 것이다. 두 끝점이 서로 다른 쪽에 있는 간선이 컷을 **가로지른다**(crosses). 가로지르는 간선의 집합은
$$\delta(S) = \{(u, v) \in E : u \in S,\ v \notin S\}$$
이다. 예제 그래프에서 $S = \{0\}$이면 $\delta(S) = \{0\text{–}1\,(4),\ 0\text{–}2\,(1)\}$이므로, 아래 속성에 따라 모든 MST가 $0\text{–}2$를 포함한다. *간선 $e$가 어떤 컷을 가로지르는 가장 가벼운 간선이면, 어떤 MST는 $e$를 포함한다. $e$가 엄격히 가장 가벼우면 모든 MST가 $e$를 포함한다.* 교환 증명: $e = (u, v)$를 포함하지 않는 MST $T$를 잡는다. $T$에는 $u$에서 $v$로 가는 경로가 있고, $u$와 $v$는 컷의 반대편에 있으므로 그 경로에는 컷을 가로지르는 간선 $f$가 있다. $f$를 $e$로 바꾸면 또 하나의 신장 트리가 된다. $f$를 지우면 $T$가 두 조각으로 나뉘고 $e$가 다시 잇기 때문이다. 그 가중치는 $w(T) - w(f) + w(e) \le w(T)$이므로 이것도 MST이고 $e$를 포함한다. 그림은 예제 그래프에서 두 단계를 모두 보여 준다. 컷 $S = \{0\}$, 그리고 가중치 $15$인 신장 트리 $\{0\text{–}1, 1\text{–}2, 1\text{–}3, 3\text{–}4\}$에서의 교환이다. 그 트리에서 $0$에서 $2$로 가는 경로는 $f = 0\text{–}1$에서 컷을 가로지른다.

<svg viewBox="0 0 560 290" style="max-width:100%;height:auto" role="img" aria-label="정점 다섯 개 예제 그래프를 두 번 그렸다. 왼쪽: 컷 S = {0}을 가로지르는 간선은 가중치 4인 0–1과 가중치 1인 0–2이므로 가벼운 간선 0–2는 모든 MST에 들어간다. MST 간선 0–2, 1–2, 1–3, 3–4의 합은 12다. 오른쪽: 가중치 15인 신장 트리 0–1, 1–2, 1–3, 3–4에는 e = 0–2가 없다. 그 트리에서 0에서 2로 가는 경로가 f = 0–1에서 컷을 가로지르고, f를 e로 바꾸면 15 − 4 + 1 = 12가 된다.">
  <text x="12" y="22" font-size="12" fill="currentColor">(a) 컷 S = {0}</text>
  <ellipse cx="48" cy="116" rx="24" ry="34" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.05" stroke-opacity="0.7"/>
  <text x="21" y="90" font-size="12" fill="currentColor" text-anchor="end" font-style="italic">S</text>
  <line x1="56.6" y1="109.2" x2="107.4" y2="68.8" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="75.2" y="84.4" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <line x1="56.6" y1="122.8" x2="107.4" y2="163.2" stroke="currentColor" stroke-width="2.6"/>
  <text x="75.2" y="155.6" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">1</text>
  <line x1="116" y1="73" x2="116" y2="159" stroke="currentColor" stroke-width="2.6"/>
  <text x="105" y="120" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">3</text>
  <line x1="127" y1="62" x2="173" y2="62" stroke="currentColor" stroke-width="2.6"/>
  <text x="150" y="55" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <line x1="121.9" y1="160.7" x2="178.1" y2="71.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="159.3" y="125.9" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="127" y1="170" x2="241" y2="170" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="184" y="185" font-size="11" fill="currentColor" text-anchor="middle">7</text>
  <line x1="189.9" y1="71.3" x2="246.1" y2="160.7" stroke="currentColor" stroke-width="2.6"/>
  <text x="227.3" y="114.1" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">6</text>
  <circle cx="48" cy="116" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="48" y="120" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <circle cx="116" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="116" y="66" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="116" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="116" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="184" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="184" y="66" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="252" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="252" y="174" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <text x="12" y="242" font-size="11" fill="currentColor">가로지르는 간선: 0–1 (4), 0–2 (1)</text>
  <text x="12" y="260" font-size="11" fill="currentColor">가장 가벼운 0–2는 모든 MST에 있다</text>
  <text x="12" y="278" font-size="11" fill="currentColor">MST (굵은 선): 1 + 2 + 3 + 6 = 12</text>
  <line x1="280" y1="34" x2="280" y2="228" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="294" y="22" font-size="12" fill="currentColor">(b) 교환: f를 e로 바꾼다</text>
  <ellipse cx="330" cy="116" rx="24" ry="34" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.05" stroke-opacity="0.7"/>
  <text x="303" y="90" font-size="12" fill="currentColor" text-anchor="end" font-style="italic">S</text>
  <line x1="338.6" y1="109.2" x2="389.4" y2="68.8" stroke="currentColor" stroke-width="2.6" stroke-opacity="0.75" stroke-dasharray="5 4"/>
  <text x="353.4" y="79.7" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold" font-style="italic">f = 4</text>
  <line x1="338.6" y1="122.8" x2="389.4" y2="163.2" stroke="currentColor" stroke-width="3.0"/>
  <text x="353.4" y="160.3" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold" font-style="italic">e = 1</text>
  <line x1="398" y1="73" x2="398" y2="159" stroke="currentColor" stroke-width="2.6"/>
  <text x="387" y="120" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">3</text>
  <line x1="409" y1="62" x2="455" y2="62" stroke="currentColor" stroke-width="2.6"/>
  <text x="432" y="55" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">2</text>
  <line x1="403.9" y1="160.7" x2="460.1" y2="71.3" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="441.3" y="125.9" font-size="11" fill="currentColor" text-anchor="middle">5</text>
  <line x1="409" y1="170" x2="523" y2="170" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.4"/>
  <text x="466" y="185" font-size="11" fill="currentColor" text-anchor="middle">7</text>
  <line x1="471.9" y1="71.3" x2="528.1" y2="160.7" stroke="currentColor" stroke-width="2.6"/>
  <text x="509.3" y="114.1" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">6</text>
  <circle cx="330" cy="116" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="330" y="120" font-size="11" fill="currentColor" text-anchor="middle">0</text>
  <circle cx="398" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="398" y="66" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <circle cx="398" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="398" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <circle cx="466" cy="62" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="466" y="66" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <circle cx="534" cy="170" r="11" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.08"/>
  <text x="534" y="174" font-size="11" fill="currentColor" text-anchor="middle">4</text>
  <text x="294" y="242" font-size="11" fill="currentColor">T (굵은 선): 4 + 3 + 2 + 6 = 15, 0–2 없음</text>
  <text x="294" y="260" font-size="11" fill="currentColor">0에서 2로 가는 경로가 f = 0–1에서 컷을 넘는다</text>
  <text x="294" y="278" font-size="11" fill="currentColor">T − f + e: 15 − 4 + 1 = 12, 곧 MST</text>
</svg>

**사이클 속성.** *$e$가 어떤 사이클에서 엄격히 가장 무거운 간선이면, 어떤 MST도 $e$를 포함하지 않는다.* MST가 $e$를 포함한다면 $e$를 지웠을 때 두 조각으로 나뉜다. 사이클의 다른 간선 하나가 두 조각 사이를 가로지르고 더 가벼우므로, 그것으로 바꾸면 더 싼 신장 트리가 된다.

두 고전 알고리즘은 모두 컷 속성을 반복해서 적용한다. 차이는 어떤 컷을 쓰느냐에 있다.

#### Prim: 트리 하나를 키운다

**한 문장 요약:** 아무 정점에서 시작해, 지금까지 만든 트리를 떠나는 가장 가벼운 간선을 반복해서 더한다(Jarník 1930; Prim 1957).

컷은 (트리 정점, 나머지 정점)이므로 더하는 간선마다 컷 속성으로 정당화된다. 코드에서는 트리를 떠나는 간선들을 가중치를 키로 최소 힙에 담는다. 가장 가벼운 것을 꺼내, 반대쪽 끝이 이미 트리에 들어왔으면 건너뛰고, 아니면 그 정점을 더한 뒤 아직 밖에 있는 정점으로 가는 간선들을 넣는다. (Dijkstra 알고리즘([[02-foundations/algorithms/graph-algorithms|11.6 §4]])을 이미 안다면, 이것은 출발점으로부터의 거리 대신 간선 가중치를 키로 쓰는 같은 루프다.)

```python
import heapq

def prim(n, adj, root=0):
    """adj[u] = list of (weight, v), undirected. Returns MST edges (w, parent, v) or None."""
    in_tree = [False] * n
    heap = [(0, root, root)]
    tree = []
    while heap:
        w, parent, u = heapq.heappop(heap)
        if in_tree[u]:
            continue                        # stale entry: u already joined more cheaply
        in_tree[u] = True
        if u != root:
            tree.append((w, parent, u))
        for wv, v in adj[u]:
            if not in_tree[v]:
                heapq.heappush(heap, (wv, u, v))
    return tree if len(tree) == n - 1 else None   # None: graph is disconnected

edges = [(4, 0, 1), (1, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3), (7, 2, 4), (6, 3, 4)]
adj = [list() for _ in range(5)]
for w, u, v in edges:
    adj[u].append((w, v))
    adj[v].append((w, u))
print(sum(w for w, _, _ in prim(5, adj)))  # 12
```

**복잡도.** 이 "게으른(lazy)" 버전은 간선 방향마다 힙 항목을 하나씩 넣고, 꺼낼 때 낡은 항목은 건너뛴다. 힙 연산은 $O(E)$번이고 각각 $O(\log E)$이므로 $O(E \log E) = O(E \log V)$다. $E \le V^2$이라 $\log E \le 2 \log V$이기 때문이다. 인접 행렬로 주어진 조밀한 그래프에서는 키 배열을 단계마다 $O(V)$로 훑어 $O(V^2)$에 끝낼 수 있고, $E$가 $V^2$에 가까우면 이쪽이 더 빠르다.

#### Kruskal: 가벼운 간선부터 더한다

**한 문장 요약:** 모든 간선을 가중치로 정렬하고, 서로 다른 두 성분을 잇는 간선만 남긴다(Kruskal 1956). 여기서 **성분**(component)은 지금까지 남긴 간선으로 이어진 정점들의 극대 집합이다.

**옳은 이유.** Kruskal이 $e = (u, v)$를 받아들일 때 컷 ($u$가 속한 성분, 나머지 전부)를 잡는다. 이 컷을 가로지르는 간선은 전에 검토된 적이 없다. 검토되었다면 Kruskal이 받아들였을 것이고 $u$의 성분이 더 컸을 것이기 때문이다. 따라서 $e$는 이 컷을 가로지르는 가장 가벼운 간선이고 컷 속성이 정당화한다. 거부된 간선은 각각 사이클을 닫았을 것이고, 그 사이클에서 가장 무거운 간선 중 하나다.

```python
def kruskal(n, edges):
    """edges: (weight, u, v). Returns MST edges (a spanning forest if disconnected)."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    tree = []
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:                        # different components: no cycle
            parent[ru] = rv
            tree.append((w, u, v))
            if len(tree) == n - 1:
                break
    return tree

edges = [(4, 0, 1), (1, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3), (7, 2, 4), (6, 3, 4)]
print(kruskal(5, edges))  # [(1, 0, 2), (2, 1, 3), (3, 1, 2), (6, 3, 4)]
```

**복잡도.** 정렬에 $O(E \log E)$가 들고, union-find 연산은 분할상환으로 거의 $O(1)$씩이므로 정렬이 지배한다. 위의 짧은 `find`는 경로 반감만 쓴다. 크기 기준 합치기를 더한 버전과 $O(\alpha(n))$ 경계는 [[02-foundations/algorithms/data-structures|11.2 §7]]에 있다.

> [!example] 계산 예제 · Worked example
> 현장 위치 다섯 곳 $0$–$4$를 위의 `edges` 비용으로 케이블망으로 이어야 한다. Kruskal은 $0\text{–}2\,(1)$을 받아들이고, $1\text{–}3\,(2)$를 받아들이고, 두 성분을 잇는 $1\text{–}2\,(3)$을 받아들인다. $0\text{–}1\,(4)$는 $0$과 $1$이 이미 $2$를 거쳐 이어져 있으므로 거부하고, $2\text{–}3\,(5)$도 같은 이유로 거부한다. $3\text{–}4\,(6)$을 받아들이면 간선 네 개로 끝난다. 총합 $1 + 2 + 3 + 6 = 12$. 정점 $0$에서 시작한 Prim은 같은 간선을 $1, 3, 2, 6$ 순서로 더한다.

**어느 것을 쓸까.** 그래프가 간선 목록으로 오거나 중간 임계값에서의 성분도 필요하면(아래 군집화) Kruskal을 쓴다. 희소한 인접 리스트에는 힙을 쓴 Prim, 조밀한 행렬에는 배열을 쓴 Prim을 쓴다.

**알아 둘 성질 두 가지.**

- **MST는 최단 경로 트리가 아니다.** 출발점 $s$의 최단 경로 트리는 $s$에서 모든 정점 $v$까지의 트리 경로 길이가 $G$에서의 최단 거리 $d(s, v)$인 신장 트리다. $w(A,B) = 2$, $w(B,C) = 2$, $w(A,C) = 3$인 삼각형을 보자. MST는 가중치 $4$인 $\{AB, BC\}$다. $A$에서의 최단 경로 트리는 가중치 $5$인 $\{AB, AC\}$다. MST 안에서 $A$에서 $C$로 가는 경로의 길이가 $3$이 아니라 $4$이기 때문이다. 모든 것을 싸게 이을 때는 MST, 한 출발점에서 싸게 가는 경로에는 최단 경로 트리를 쓴다.
- **MST는 병목을 최소화한다.** 어떤 두 정점에 대해서든 MST 안의 경로는 두 정점 사이 모든 경로 중에서 *가장 큰* 간선이 가장 작다.
$$\max_{e \in P_{\text{MST}}(u, v)} w(e) = \min_{P \text{ from } u \text{ to } v} \ \max_{e \in P} w(e)$$
  여기서 $P_{\text{MST}}(u, v)$는 트리 안에서 $u$와 $v$를 잇는 경로로, 트리에는 사이클이 없어 유일하다. $P$는 $G$의 모든 경로를 돈다. 예제 그래프에서 트리 경로 $0\text{–}2\text{–}1\text{–}3\text{–}4$의 가장 큰 간선은 $6$이고, 정점 $4$로 들어가는 모든 경로가 $3\text{–}4\,(6)$이나 $2\text{–}4\,(7)$을 지나야 하므로 $0$에서 $4$로 가는 어떤 경로도 이보다 낫지 않다. 예를 들어 로봇이 어느 두 충전 도크 사이든 건너다닐 수 있게 하는 최소 배터리 주행 거리는, 도크 간 거리로 만든 MST의 가장 무거운 간선이다.

#### 단일 연결 군집화: 일찍 멈춘 Kruskal

**한 문장 요약:** 점을 정점으로, 거리를 간선 가중치로 보고 Kruskal을 돌리다가 긴 간선 앞에서 멈춘다.

이름은 두 군집 사이의 거리를 가장 가까운 한 쌍으로 재는 방식 $d_{\text{single}}(A, B) = \min_{p \in A,\, q \in B} d(p, q)$에서 왔다. 완전 연결은 쌍들의 $\max$를, 평균 연결은 평균을 쓴다. 멈추는 규칙은 두 가지다. **성분이 $k$개** 남으면 멈추면, 서로 다른 군집에 속한 점들 사이의 최소 거리인 *간격*(spacing)을 최대화하는 $k$-군집화가 나온다.
$$\text{spacing}(C_1, \dots, C_k) = \min_{a \ne b} \ \min_{p \in C_a,\, q \in C_b} d(p, q)$$
간격이 크면 모든 군집이 다른 모든 군집에서 멀다. 아래 첫 번째 호출의 두 군집은 $(1, 0)$과 $(6, 0)$ 사이의 거리인 간격 $5$를 갖는다. 또는 **임계값 $r$보다 긴 첫 간선에서** 멈추면, 군집은 $r$보다 가까운 모든 점 쌍을 이은 그래프의 연결 성분과 정확히 같다(Gower & Ross 1969).

```python
from itertools import combinations
from math import dist

def single_linkage(points, max_gap):
    """Cluster labels: points joined by any chain of hops no longer than max_gap."""
    parent = list(range(len(points)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pairs = sorted((dist(p, q), i, j) for (i, p), (j, q) in combinations(enumerate(points), 2))
    for d, i, j in pairs:
        if d > max_gap:
            break                             # Kruskal stopped early
        parent[find(i)] = find(j)
    roots = {}
    return [roots.setdefault(find(i), len(roots)) for i in range(len(points))]

box = [(0, 0), (0.5, 0.3), (1, 0)]
crate = [(6, 0), (6.4, 0.5), (7, 0)]
print(single_linkage(box + crate, 1.2))                             # [0, 0, 0, 1, 1, 1]
print(single_linkage(box + [(2, 0), (3, 0), (4, 0), (5, 0)] + crate, 1.2))  # all 0
```

모든 쌍을 만드는 데 $O(n^2 \log n)$이 들어, 검출 몇백 개에는 괜찮지만 점군에는 너무 느리다. **로보틱스 활용.** 지면을 제거한 뒤 LiDAR나 깊이 점군을 물체별로 나누는 표준 방법인 *유클리드 군집 추출*(Euclidean cluster extraction)이 임계값 $r$을 쓰는 단일 연결 군집화다. 실제 구현은 모든 쌍을 정렬하지 않는다. KD-tree나 복셀 해시로 각 점의 반경 $r$ 이내 이웃을 찾고([[02-foundations/algorithms/data-structures|11.2 §8]]) union-find나 BFS로 잇는다. 같은 규칙으로 여러 카메라나 연속 프레임에서 서로 $r$ 이내에 있는 검출을 묶는다.

**사슬(chaining) 약점.** 짧은 도약 한 줄이면 두 군집이 합쳐진다. 위의 두 번째 호출이 보여 주듯, 케이블, 난간, 남아 있는 지면 점, 벽에 기댄 작업자의 팔 같은 가느다란 점의 줄이 두 물체를 하나의 군집으로 잇는다. 흔한 해결책은 지면 평면을 먼저 제거하는 것(예: RANSAC), 점이 연결되려면 최소 이웃 수를 요구하는 밀도 기반 군집화(DBSCAN, Ester et al. 1996), 또는 가장 가까운 한 쌍이 아니라 군집 전체로 판단하는 평균·완전 연결 군집화를 쓰는 것이다.

**곁가지.** MST는 거리가 거리 공리(그중 하나가 삼각 부등식 $d(a, c) \le d(a, b) + d(b, c)$)를 만족할 때 점들을 도는 최단 순회(예: 점검 경로)의 2-근사도 준다. MST를 따라 각 간선을 두 번씩 지나며 한 바퀴 돌고, 이미 방문한 정점은 건너뛴다. 이 순회의 비용은 $2 \cdot w(\text{MST})$이고, 삼각 부등식 때문에 건너뛰어도 길어지지 않는다. 순회에서 간선 하나를 지우면 신장 트리가 남으므로 모든 순회는 $w(\text{MST})$ 이상이다.

### 7. 정확한 풀이가 NP-난해할 때 근사로서의 그리디

많은 커버리지·선택 문제에서 정확한 최적화는 NP-난해하고, 그리디는 실용적인 방법이자 다항 시간에 달성 가능하다고 알려진 최선의 보장을 갖는 방법이다.

**근사 비율.** 모든 사례 $I$에서 알고리즘의 값 $\mathrm{ALG}(I)$가 최적값 $\mathrm{OPT}(I)$의 $\alpha$배 안에 들면 그 알고리즘을 **$\alpha$-근사**($\alpha$-approximation)라 한다.
$$\mathrm{ALG}(I) \le \alpha \cdot \mathrm{OPT}(I) \ \text{ for minimization } (\alpha \ge 1), \qquad \mathrm{ALG}(I) \ge \alpha \cdot \mathrm{OPT}(I) \ \text{ for maximization } (\alpha \le 1)$$
이 비율은 모든 사례에 대한 최악의 보장이므로, 잘 된 실행 하나는 아무것도 증명하지 못하고 나쁜 사례 하나는 반증한다. §4의 배낭 규칙은 $1/2$-근사, §6의 MST 순회는 $2$-근사다. 아래 집합 덮개는 $\alpha = H(d)$를 얻고, 그 계산 예제에서 그리디는 최적 $2$개 대신 $3$개를 써서 비율 $1.5$가 $H(4) \approx 2.08$ 안에 든다. 부분모듈 최대화는 $\alpha = 1 - 1/e$를 얻는다.

#### 집합 덮개

**문제.** 원소 $n$개의 전체 집합 $U$(예: 점검할 구조물 표면 조각들)와 부분집합들의 모음(예: 후보 시점마다 보이는 조각들)이 있다. 합집합이 $U$가 되는 부분집합을 가장 적게 고른다. 부분집합 $S_1, \dots, S_m \subseteq U$와 비용 $c_j$가 있으면 문제는
$$\min_{J \subseteq \{1, \dots, m\}} \sum_{j \in J} c_j \quad \text{subject to} \quad \bigcup_{j \in J} S_j = U$$
이고, 모든 $c_j = 1$인 가중치 없는 문제는 고른 부분집합의 개수를 세는 것이다.

**한 문장 요약:** 아직 덮이지 않은 원소를 가장 많이 덮는 부분집합을 반복해서 고른다. 가중 버전에서는 새로 덮는 원소당 비용이 가장 낮은 부분집합을 고른다.

**보장.** 가장 큰 부분집합의 크기를 $d$, $H(d) = 1 + \tfrac12 + \dots + \tfrac1d$라 하자. 그리디의 총비용은 최적값의 $H(d)$배 이하이고, 가중 버전에서도 성립한다(Chvátal 1979). $d \le n$이고 $H(n) \le \ln n + 1$이므로 그리디는 항상 최적의 약 $\ln n$배 이내다. 가중치 없는 경우는 앞서 Johnson(1974)과 Lovász(1975)가 보였다. 이것은 사실상 최선이다. P = NP가 아니라면 어떤 다항 시간 알고리즘도 $(1 - \varepsilon) \ln n$배를 달성할 수 없다(Dinur & Steurer 2014).

*증명 아이디어.* 그리디가 집합을 하나 고를 때 그 비용을 새로 덮는 원소들에게 고르게 나눠 청구한다. 덮이지 않은 원소가 $k$개 남았을 때, 최적 덮개는 총비용 OPT인 집합들로 이 원소를 모두 덮으므로, 덮이지 않은 원소당 비용이 $\mathrm{OPT}/k$ 이하인 집합이 반드시 있고 그리디는 그 이상 내지 않는다. $k$가 $n$에서 $1$까지 내려가며 청구액을 더하면 $\mathrm{OPT} \cdot H(n)$이 된다. Chvátal은 집합별로 더 세밀하게 계산해 $H(d)$를 얻는다.

```python
def greedy_set_cover(universe, subsets):
    """subsets: dict name -> set. Returns chosen names, or None if U cannot be covered."""
    uncovered = set(universe)
    chosen = []
    while uncovered:
        best = max(subsets, key=lambda s: len(subsets[s] & uncovered))
        if not subsets[best] & uncovered:
            return None                     # some element is in no subset
        chosen.append(best)
        uncovered -= subsets[best]
    return chosen

views = {"V1": {1, 2, 3, 4}, "V2": {1, 3, 5}, "V3": {2, 4, 6}}
print(greedy_set_cover(range(1, 7), views))  # ['V1', 'V2', 'V3']; optimum is V2, V3
```

> [!example] 계산 예제 · Worked example
> `views`처럼 벽 조각 여섯 개와 후보 시점 세 개가 있다. 그리디는 새 조각 네 개를 보는 $V1$을 고른다. 그다음 $V2$와 $V3$가 각각 새 조각 하나씩을 더해 그리디는 시점 $3$개를 쓴다. $V2 \cup V3$가 이미 여섯 개를 모두 덮으므로 최적은 $2$다. 이것은 보장을 어기지 않는다. $d = 4$이고 $H(4) \cdot 2 \approx 4.17 \ge 3$이기 때문이다. 가장 좋아 보였던 첫 선택이 어떤 최적 덮개에도 들어 있지 않았다.

매 라운드 모든 부분집합을 훑으므로 직접 구현은 $O(\text{라운드 수} \times \sum_S \lvert S\rvert)$가 든다. 후보가 수천 개인 시점 계획 사례에는 충분히 빠르고, 다음에 설명할 게으른 평가로 더 빨라진다.

#### 부분모듈 최대화: 1 − 1/e 보장

센서 배치와 능동 인식의 많은 목적 함수는 **한계 효용 체감** 성질을 보인다. 작은 집합에 센서 하나를 더하는 이득은, 그 작은 집합을 포함하는 더 큰 집합에 같은 센서를 더하는 이득 이상이다. 형식적으로, $A \subseteq B$이고 $x \notin B$일 때마다 $f(A \cup \{x\}) - f(A) \ge f(B \cup \{x\}) - f(B)$이면 집합 함수 $f$는 *부분모듈*(submodular)이고, 원소를 더해도 $f$가 줄지 않으면, 즉 $A \subseteq B$일 때마다 $f(A) \le f(B)$이면 *단조*다. $A$가 주어졌을 때 $x$의 **한계 이득**(marginal gain)을 $\Delta(x \mid A) = f(A \cup \{x\}) - f(A)$라 쓰면, 부분모듈성은 한 줄로
$$\Delta(x \mid A) \ge \Delta(x \mid B) \quad \text{for all } A \subseteq B,\ x \notin B$$
이다. 이미 많이 골랐을수록 원소 하나의 가치가 작아진다는 뜻이다. 위 집합 덮개 예제의 커버리지 함수 $f(A) = \lvert \bigcup_{j \in A} \text{views}[j] \rvert$에서 $\Delta(V3 \mid \varnothing) = 3$이지만, $V1$이 이미 조각 $2$와 $4$를 보므로 $\Delta(V3 \mid \{V1\}) = 1$이다. **반례:** $f(A) = \lvert A \rvert^2$은 단조지만 부분모듈이 아니다. 첫 원소는 $1$을, 두 번째 원소는 $3$을 얻기 때문이다. 센서 탐지 영역의 합집합 넓이는 단조 부분모듈이다. 숨은 상태가 주어졌을 때 센서 측정들이 조건부 독립이면, 측정이 그 상태에 대해 주는 정보량도 단조 부분모듈이다(Krause & Guestrin 2005). Krause, Singh & Guestrin(2008)은 이를 센서 배치에 적용했다. $f(\varnothing) = 0$인 단조 부분모듈 $f$에 대해, 한계 이득이 가장 큰 원소를 하나씩 $k$개 고르면

$$f(\text{greedy}_k) \ge \left(1 - \tfrac{1}{e}\right) f(\text{OPT}_k) \approx 0.632\, f(\text{OPT}_k)$$

가 보장된다. 매 단계 최적해의 $k$개 원소를 함께 더하면 남은 격차 $f(\text{OPT}_k) - f(\text{greedy}_i)$ 이상을 더하므로 가장 좋은 원소 하나는 그 격차의 $1/k$ 이상을 더하고, 따라서 격차는 단계마다 $(1 - 1/k)$배 이하로 줄어 $(1 - 1/k)^k \le 1/e$ 이하만 남기 때문이다(Nemhauser, Wolsey & Fisher 1978). 다음 최선 시점(next-best-view)과 센서 선택 논문이 단순한 그리디 선택을 쓰면서도 보장을 말할 수 있는 이유가 이것이다. 이 보장은 조건이 모두 필요하다. 단조성, 부분모듈성, 그리고 원소 $k$개라는 단순한 예산이 있어야 한다. 센서 두 개를 함께 쓸 때의 가치가 각각의 합보다 큰 시너지가 있거나, 제약이 경로나 이동 예산이면 이 경계는 더 이상 적용되지 않는다. 표준 가속 기법인 *게으른 그리디*(Minoux 1978)는 이전의 한계 이득을 최대 힙에 둔다. 부분모듈성 때문에 그 이득은 줄어들 수만 있으므로 맨 위 항목만 다시 계산하면 된다.

### 8. 면접 함정

- **틀린 키로 정렬하기.** 활동 선택은 시작 시각이나 길이가 아니라 *종료* 시각으로 정렬한다. 병합은 *시작* 시각으로 정렬한다. 가중 스케줄링은 차이가 아니라 *비율* $w/l$로 정렬한다. 코딩 전에 키와 그것이 안전한 이유 한 문장을 말하고, 다른 후보 키와 순서가 엇갈리는 원소 세 개짜리 입력으로 시험한다.
- **동점과 끝점.** 구간이 닫힌 구간인지 반열린 구간인지 정하고 `<`와 `<=`를 일관되게 쓴다. `[(1, 3), (3, 5), (2, 4)]`는 반열린 구간이면 회의실 2개, 닫힌 구간이면 3개가 필요하다. $\pm 1$ 사건으로 훑을 때는 같은 시각의 사건 순서가 그 결정을 담는다. Kruskal이나 허프만 병합의 동점은 총비용에는 해가 없지만 *어떤* 트리를 출력하는지는 바꿀 수 있으므로, 테스트에서 특정 부호나 간선 목록 하나를 단언하지 않는다.
- **파이썬 힙의 튜플.** `heapq`는 튜플을 원소 순서대로 비교한다. 무게가 같으면 다음으로 내용물을 비교하는데, dict, 문자열과 섞인 튜플, 사용자 정의 노드처럼 순서를 매길 수 없는 객체에서는 오류가 난다. 두 번째 원소로 카운터를 넣는다. C++의 `std::priority_queue`는 최대 힙이므로 Prim과 허프만에는 `std::greater<>`를 쓰거나 키의 부호를 바꾼다.
- **부동소수점 비율.** 동점이나 정확한 순서가 중요하면 $w_a l_b$와 $w_b l_a$를 정수로 비교하거나 `Fraction`을 쓴다.
- **연결되지 않은 그래프.** 루트 하나에서 시작한 Prim은 그 루트의 성분만 조용히 반환한다. Kruskal은 신장 숲을 반환한다. 트리의 간선이 $V - 1$개인지 확인한다.
- **MST와 최단 경로의 혼동.** "모든 것을 가장 싸게 잇기"는 MST다. "한 곳에서 가장 싸게 가는 경로"는 Dijkstra다([[02-foundations/algorithms/graph-algorithms|11.6]]).
- **증명 대신 추측하기.** 면접관은 "교환 논증으로 확인하겠다"와 그 맞바꿈 및 비용 변화까지는 받아들인다. "맞는 것 같다"는 받아들이지 않는다. 증명이 빨리 떠오르지 않으면 아래처럼 작은 입력을 전수 조사해 그리디와 비교한다. 2분이면 끝나고, 반례를 찾거나 확신을 준다.

```python
def greedy_coins(coins, amount):
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count                             # coin 1 is present, so amount ends at 0

def fewest_coins(coins, amount):             # exact, by DP (11.5)
    best = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        best[a] = min(best[a - c] + 1 for c in coins if c <= a)
    return best[amount]

def first_counterexample(max_coin=6, max_amount=20):
    for a in range(2, max_coin + 1):
        for b in range(a + 1, max_coin + 1):
            for amount in range(1, max_amount + 1):
                if greedy_coins([1, a, b], amount) != fewest_coins([1, a, b], amount):
                    return [1, a, b], amount
    return None

print(first_counterexample())  # ([1, 3, 4], 6)
```

### 스스로 점검

1. 구간 $[0,7), [1,3), [2,4), [4,6), [6,8)$. 가장 빠른 *시작* 그리디와 가장 빠른 *종료* 그리디는 각각 몇 개를 고르는가? 다섯 개를 모두 돌리려면 회의실이 몇 개 필요한가?
2. 활동 선택의 교환 논증을 세 문장으로 말하라. 맞바꿈은 가장 먼저 끝나는 구간의 어떤 성질에 기대는가?
3. 작업 두 개: $P$는 $w = 9, l = 6$, $Q$는 $w = 4, l = 2$. 차이로는 어느 것이 먼저이고, 비율로는 어느 것이 먼저인가? 두 비용을 계산하라.
4. 빈도 $a{:}\,1$, $b{:}\,1$, $c{:}\,2$, $d{:}\,3$, $e{:}\,5$에 대한 허프만 부호를 만들라. 부호어 길이, 이 12기호 메시지의 총 비트 수, 고정 길이 부호의 비용을 말하라.
5. 물건(무게, 가치) $(4, 8)$, $(3, 5)$, $(3, 5)$, 용량 $6$. 분할 가능 최적값, 밀도 그리디의 0/1 값, 실제 0/1 최적값은 각각 얼마인가?
6. 간선 가중치가 겹치는 그래프에서 Kruskal은 동점 처리에 따라 다른 트리를 출력할 수 있다. 모두 MST인가? 컷 속성 증명의 어느 부분이 이를 보장하는가?
7. $r = 0.3$ m인 LiDAR 군집화 단계가 작업자와 그가 기대선 비계를 하나로 합쳤다. 알고리즘 관점에서 이유를 설명하고 해결책 두 가지를 제시하라.
8. 그리디 집합 덮개가 시점 3개를 반환했는데, 나중에 2개짜리 덮개를 찾았다. 보장과 모순인가? "시점 $k$개 고르기" 목적 함수에 $(1 - 1/e)$ 경계를 인용하기 전에 어떤 조건을 확인해야 하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 가장 빠른 시작은 $[0,7)$을 먼저 고르고, 나머지는 모두 $7$ 전에 시작하므로 고르는 수는 **1개**. 가장 빠른 종료는 $[1,3)$, $[4,6)$, $[6,8)$을 고르므로 **3개**. 시각 $2$에서 $[0,7)$, $[1,3)$, $[2,4)$가 모두 겹치므로 회의실이 적어도 3개 필요하고, `min_rooms`도 $3$을 반환한다.
> 2. 가장 먼저 끝나는 구간을 $a$, 첫 구간이 $o_1$인 최적해를 $O$라 하자. $o_1$을 $a$로 바꾼다. $a$는 $o_1$보다 늦게 끝나지 않으므로 $O$의 다른 모든 구간이 시작하기 전에 끝나고, 집합은 겹치지 않은 채 크기를 유지한다. 맞바꿈은 $a$의 *종료 시각이 가장 이르다*는 성질에 기댄다. $a$가 끝난 뒤에 시작하는 구간들에 재귀하면 증명이 끝난다.
> 3. 차이: $P$는 $3$, $Q$는 $2$이므로 차이 순서는 $P$가 먼저이고 비용은 $9 \cdot 6 + 4 \cdot 8 = 86$이다. 비율: $P$는 $1.5$, $Q$는 $2$이므로 비율 순서는 $Q$가 먼저이고 비용은 $4 \cdot 2 + 9 \cdot 8 = 80$이다. 교환 공식 $\Delta = w_P l_Q - w_Q l_P = 18 - 24 < 0$이 예측하듯 비율 순서가 낫다. $Q$를 $P$ 앞으로 옮기면 비용이 $6$ 줄어든다.
> 4. $a + b = 2$로 합친다. 그 트리를 $c$와 합쳐 $4$를 만든다(무게 $2$인 두 트리가 가장 가볍고 $d = 3$은 더 무겁다). 다음 $d + 4 = 7$, 그다음 $e + 7 = 12$. 길이는 $e{:}\,1$, $d{:}\,2$, $c{:}\,3$, $a{:}\,4$, $b{:}\,4$다. 총 비트 $= 5 \cdot 1 + 3 \cdot 2 + 2 \cdot 3 + 1 \cdot 4 + 1 \cdot 4 = 25$, 기호당 약 $2.08$비트다. 기호 5개의 고정 길이 부호는 기호당 3비트, 총 $36$비트다.
> 5. 밀도는 $2, 1.67, 1.67$이다. 분할 가능: $(4, 8)$을 담고 $(3, 5)$의 $2/3$을 담아 $8 + 10/3 \approx 11.33$. 밀도 그리디 0/1: $(4, 8)$을 담으면 $(3, 5)$는 어느 것도 들어가지 않아 $8$. 최적: $(3, 5)$ 두 개로 무게 $6$, 가치 $10$. 예상대로 분할 가능 값 $11.33$이 $10$의 상한이다.
> 6. 그렇다, 모두 MST다. 엄격하지 않은 형태의 컷 속성은 컷을 가로지르는 (동점일 수도 있는) 가장 가벼운 간선이 *어떤* MST에 속한다고 말하고, 증명의 맞바꿈은 동점에서도 성립하는 $w(e) \le w(f)$만 쓴다. 받아들인 간선마다 자기 성분 둘레의 컷을 가로지르는 가장 가벼운 간선이므로, 어떤 동점 처리든 MST를 내고 모두 총가중치가 같다.
> 7. 유클리드 군집화는 단일 연결 군집화다. 두 그룹에서 하나씩 뽑은 점 *한* 쌍만 $r$ 이내면 합치고, 사슬로 이어진다. 작업자 손의 점이 비계에서 $0.3$ m 이내라서 둘이 한 군집이 된다. 해결책: 알려진 구조(지면 평면, 지도 점)를 먼저 제거한다. 점이 연결되려면 최소 이웃 수를 요구한다(DBSCAN식 핵심점). 더 작은 $r$에 군집 모양·크기 검사를 덧붙인다. 또는 학습된 모델로 분할한다.
> 8. 아니다. 집합 덮개 보장은 그리디를 OPT 자체가 아니라 $H(d) \cdot \mathrm{OPT}$로 묶는다. $d = 4$이면 그 경계는 약 $4.17$이고 $3$은 그 안에 있다. $(1 - 1/e)$를 인용하기 전에 목적 함수가 단조인지(시점을 더해도 손해가 없는지), 부분모듈인지(큰 집합에 더할수록 이득이 작은지; 커버리지 넓이는 성립하지만 두 시점이 함께 있어야 하는 삼각측량처럼 시너지가 있는 목적 함수에서는 깨질 수 있다), $f(\varnothing) = 0$인지, 그리고 제약이 이동 비용이나 경로 제약이 아닌 단순한 개수 예산 $k$인지 확인한다.

### 출처

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.), 그리디 알고리즘·최소 신장 트리 장. MIT Press.
- Kleinberg, J., & Tardos, É. (2005). *Algorithm Design*, 4장(그리디 알고리즘; "앞서 가기"와 교환 증명 방식). Pearson/Addison-Wesley.
- Roughgarden, T. (2019). *Algorithms Illuminated, Part 3: Greedy Algorithms and Dynamic Programming*. Soundlikeyourself Publishing.
- Kulikov, A., & Pevzner, P. (2018). *Learning Algorithms Through Programming and Puzzle Solving*, 그리디 알고리즘 장. Active Learning Technologies.
- Smith, W. E. (1956). Various optimizers for single-stage production. *Naval Research Logistics Quarterly*, 3(1–2), 59–66.
- Huffman, D. A. (1952). A method for the construction of minimum-redundancy codes. *Proceedings of the IRE*, 40(9), 1098–1101. https://doi.org/10.1109/JRPROC.1952.273898
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.), 5장(데이터 압축). Wiley.
- Jarník, V. (1930). O jistém problému minimálním. *Práce moravské přírodovědecké společnosti*, 6, 57–63.
- Kruskal, J. B. (1956). On the shortest spanning subtree of a graph and the traveling salesman problem. *Proceedings of the American Mathematical Society*, 7(1), 48–50. https://doi.org/10.1090/S0002-9939-1956-0078686-7
- Prim, R. C. (1957). Shortest connection networks and some generalizations. *Bell System Technical Journal*, 36(6), 1389–1401. https://doi.org/10.1002/j.1538-7305.1957.tb01515.x
- Tarjan, R. E. (1975). Efficiency of a good but not linear set union algorithm. *Journal of the ACM*, 22(2), 215–225.
- Gower, J. C., & Ross, G. J. S. (1969). Minimum spanning trees and single linkage cluster analysis. *Journal of the Royal Statistical Society, Series C (Applied Statistics)*, 18(1), 54–64.
- Ester, M., Kriegel, H.-P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. *Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining (KDD)*, 226–231.
- Johnson, D. S. (1974). Approximation algorithms for combinatorial problems. *Journal of Computer and System Sciences*, 9(3), 256–278.
- Lovász, L. (1975). On the ratio of optimal integral and fractional covers. *Discrete Mathematics*, 13(4), 383–390.
- Chvátal, V. (1979). A greedy heuristic for the set-covering problem. *Mathematics of Operations Research*, 4(3), 233–235. https://doi.org/10.1287/moor.4.3.233
- Dinur, I., & Steurer, D. (2014). Analytical approach to parallel repetition. *Proceedings of the 46th ACM Symposium on Theory of Computing (STOC)*.
- Nemhauser, G. L., Wolsey, L. A., & Fisher, M. L. (1978). An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming*, 14(1), 265–294. https://doi.org/10.1007/BF01588971
- Minoux, M. (1978). Accelerated greedy algorithms for maximizing submodular set functions. In *Optimization Techniques*, Lecture Notes in Control and Information Sciences, vol. 7, 234–243. Springer.
- Krause, A., & Guestrin, C. (2005). Near-optimal nonmyopic value of information in graphical models. *Proceedings of the 21st Conference on Uncertainty in Artificial Intelligence (UAI)*.
- Krause, A., Singh, A., & Guestrin, C. (2008). Near-optimal sensor placements in Gaussian processes: Theory, efficient algorithms and empirical studies. *Journal of Machine Learning Research*, 9, 235–284.
