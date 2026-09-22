---
title: 11.7 Interview-Ready Code in Python & C++
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Run a 45-minute problem from clarifying questions to tested code out loud, catch your own bugs with edge cases and a stress test, and avoid the standard traps of Python and C++."
mastery-when: "Raise to Mastery only if the target role writes performance-critical or real-time C++ as its main job, where the language rules themselves become the work."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/complexity-recursion|11.1 Complexity, Recursion & Backtracking]] (stating a bound, the time budget in §1, recursion depth in §5) · [[02-foundations/algorithms/data-structures|11.2 Core Data Structures]] (which structure gives which operation)
> [[02-foundations/algorithms/complexity-recursion|11.1 복잡도, 재귀, 백트래킹]](상한 말하기, §1의 시간 예산, §5의 재귀 깊이) · [[02-foundations/algorithms/data-structures|11.2 핵심 자료구조]](어떤 구조가 어떤 연산을 주는가)
>
> Track map · 트랙 지도: [[02-foundations/algorithms/index|11. Algorithms & Data Structures]]

## English

*The craft page of the algorithms track. The other pages teach what to compute; this one teaches how to get correct code out of your hands in 45 minutes, in the two languages robotics interviews use.*

Knowing the right algorithm is about half of a coding interview. The other half is visible process: whether you ask before assuming, whether you start from something correct, whether your code runs the first time, and whether you find your own bug before the interviewer points at it. Research-lab interviews add a third question — would I want to read this person's code in our repository? This page covers all three: a routine to follow and narrate (§1), testing habits that catch bugs early (§2), the parts of Python and C++ that trip people under pressure (§3, §4), the habits that make numeric and research code readable (§5), the rules that change inside a control loop (§6), and how to answer "can you do better?" (§7).

> [!note] First pass · 처음이라면
> Read §1 and §2 first and practise them on every problem you solve from now on. Then read the section for the language you will interview in (§3 or §4). Those two sections change format: they are lookup tables of self-contained traps rather than one worked story, so read them through once and come back to single entries later. §5 to §7 matter most for research-lab interviews, and the drill list before the self-check turns the whole page into a practice plan.

### 1. The solving routine for a 45-minute interview

A programming problem is solved in a fixed order: understand the statement and its limits, design an algorithm and convince yourself it is right, write it, then test and debug it. Kulikov and Pevzner build their book around this sequence. An interview adds one requirement: you do each step **out loud**, because the interviewer grades the reasoning they can hear, not the thinking they cannot. Silence reads as being stuck.

| Step | What you do | Rough time |
|---|---|---|
| 1. Restate and ask | Repeat the problem in your own words; ask about sizes, value ranges, and edge cases | 3–5 min |
| 2. Small example by hand | Work one input to its output on the whiteboard or in a comment | 2–3 min |
| 3. Brute force first | Describe the obviously correct method and its complexity | 2–3 min |
| 4. Improve | Find the repeated or wasted work and remove it | 5–10 min |
| 5. Code | Write clean code for the chosen method | 10–15 min |
| 6. Test by hand | Trace the small example and the edge cases through your code | 5 min |
| 7. State complexity | Time and space, with the case named | 1–2 min |

The times are a rough guide. What matters is the order, and not skipping step 6.

**The example problem.** A camera driver delivers frame numbers out of order and sometimes twice. Report the length of the longest block of consecutive frame numbers that arrived. For `[12, 10, 11, 11, 20, 13]` the answer is 4 (frames 10 to 13).

**Step 1 — restate and ask.** Restating catches misreadings before they cost ten minutes. Then ask the questions whose answers change the code:

- *Sizes and ranges.* How many numbers, and how large? This picks the complexity target (use the time budget in [[02-foundations/algorithms/complexity-recursion|11.1 §1]]) and, in C++, the integer type.
- *Edge cases.* Can the input be empty? Can values repeat, or be negative?
- *Output.* Only the length, or the block itself? If several blocks tie, which one?
- *Freedom.* May I modify the input? Is there a memory limit?

> **Say:** "So I get an unsorted list of frame numbers that can contain repeats, and I return the length of the longest unbroken run of values. Can the list be empty — I'll return 0 then. Roughly how many frames: thousands, or hundreds of millions? And do repeats count once?"

**Step 2 — a small example by hand.** Pick an input small enough to finish in a minute but large enough to contain the tricky parts: here a repeat and a gap. Doing it by hand shows you the structure of the answer (sort the values mentally: 10, 11, 11, 12, 13, 20) and gives you a test for step 6.

> **Say:** "Sorted, that's 10, 11, 11, 12, 13, 20. The repeat of 11 should not break the run or lengthen it, so the run is 10 through 13, length 4."

**Step 3 — brute force first.** State a method that is plainly correct, even if slow, and give its cost. It proves you understood the problem, gives you something to fall back on, and later becomes the reference for a stress test (§2). Here: for each value, count upward while the next value is present in the list. Each membership test scans the list, O(n), and a walk can take up to n steps, so the total is O(n³) in the worst case.

> **Say:** "A correct baseline: from every value, walk upward while the next number is in the list. That's O(n³) because each `in` on a list is linear. I don't want to code that, but it tells me what to speed up."

**Step 4 — improve.** Look for work that is repeated or wasted. Two things are wasted here. Membership in a list is linear, but in a hash set it is O(1) on average. And the walk from 11 repeats most of the walk from 10: we only need to walk from values that *start* a run, meaning their predecessor is absent. Then every value is stepped over by at most one walk, so all the walks together take O(n) steps.

> **Say:** "Put the values in a set, so membership is O(1) on average. Only start a walk at `x` if `x - 1` is not in the set. Each value then belongs to exactly one walk, so the total work is linear. An alternative is to sort and scan in O(n log n) with less extra memory — I'll mention that trade-off at the end."

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="The frame numbers 12, 10, 11, 11, 20, 13 become the set 10, 11, 12, 13, 20 on a number line. Only 10 and 20 start a walk, because 9 and 19 are absent; the walk from 10 steps through 11, 12 and 13 and stops at the missing 14, length 4; the walk from 20 has length 1; 11, 12 and 13 are skipped because their predecessor is present.">
  <defs><marker id="aicRun" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="8" y="20" font-size="12" fill="currentColor">input [12, 10, 11, 11, 20, 13] → set {10, 11, 12, 13, 20}</text>
  <line x1="28.8" y1="88" x2="515.2" y2="88" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <text x="44" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">9</text>
  <circle cx="82" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="82" y="110" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <circle cx="120" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="120" y="110" font-size="11" fill="currentColor" text-anchor="middle">11</text>
  <circle cx="158" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="158" y="110" font-size="11" fill="currentColor" text-anchor="middle">12</text>
  <circle cx="196" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="196" y="110" font-size="11" fill="currentColor" text-anchor="middle">13</text>
  <text x="234" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">14</text>
  <line x1="272" y1="84" x2="272" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="272" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">15</text>
  <line x1="310" y1="84" x2="310" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="310" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">16</text>
  <line x1="348" y1="84" x2="348" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="348" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">17</text>
  <line x1="386" y1="84" x2="386" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="386" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">18</text>
  <text x="424" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">19</text>
  <circle cx="462" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="462" y="110" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <text x="500" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">21</text>
  <text x="82" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85" font-weight="bold">start</text>
  <text x="120" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">skip</text>
  <text x="158" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">skip</text>
  <text x="196" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">skip</text>
  <text x="462" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85" font-weight="bold">start</text>
  <path d="M 82 80 A 19 19 0 0 1 120 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRun)"/>
  <path d="M 120 80 A 19 19 0 0 1 158 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRun)"/>
  <path d="M 158 80 A 19 19 0 0 1 196 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRun)"/>
  <path d="M 196 80 A 19 19 0 0 1 234 80" stroke="currentColor" stroke-width="1.4" fill="none" stroke-opacity="0.6" stroke-dasharray="3 2" marker-end="url(#aicRun)"/>
  <circle cx="44" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="44" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">absent</text>
  <circle cx="234" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="234" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">absent</text>
  <circle cx="424" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="424" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">absent</text>
  <circle cx="500" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="500" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">absent</text>
  <text x="8" y="162" font-size="11" fill="currentColor">walk from 10: 11, 12, 13 present, 14 absent → length 4</text>
  <text x="8" y="182" font-size="11" fill="currentColor">walk from 20: 21 absent → length 1; best = 4</text>
  <text x="8" y="202" font-size="11" fill="currentColor" fill-opacity="0.85">each value is stepped over by at most one walk, so all walks together take O(n)</text>
</svg>

**Step 5 — code.** Name things for what they mean, keep the function small, and say what each block does as you write it.

```python
def longest_run(nums):
    """Length of the longest block of consecutive integers in nums (repeats count once)."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:            # not the start of a run: its start will count it
            continue
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best

assert longest_run([12, 10, 11, 11, 20, 13]) == 4
assert longest_run([]) == 0
assert longest_run([5]) == 1
assert longest_run([-2, -1, 0, 7]) == 3
assert longest_run([3, 3, 3]) == 1
```

**Step 6 — test by hand.** Run your example through the code, not through your idea of the code. Then run the edge cases from §2. This is where most candidates lose points: they declare victory as soon as the code is written.

> **Say:** "The set is {10, 11, 12, 13, 20}. At 10, 9 is missing, so I walk: 11, 12, 13 are present, 14 isn't, length 4. At 11, 12 and 13, the predecessor is present, so I skip. At 20, 19 is missing, length 1. Best is 4. Empty input: the loop never runs and I return 0. One element: length 1."

**Step 7 — state complexity.** Name the sizes, the case, and the space ([[02-foundations/algorithms/complexity-recursion|11.1 §7]] has the full five-part answer).

> **Say:** "O(n) expected time, because set operations are O(1) on average and each value is visited by at most one walk. The worst case with a degenerate hash is O(n²). Extra space is O(n) for the set."

**When you are stuck.** Say what you are trying and why it fails ("a heap gives me the minimum, but I need the successor of an arbitrary value"). Try the checklist of standard moves: sort first; use a hash map; two pointers; a heap; binary search on the answer; think of it as a graph. Asking for a hint costs less than five silent minutes.

### 2. Testing like an engineer

A program that looks right is not evidence of a program that is right. Three habits, in increasing strength, find the bugs before someone else does.

**Hand-tracing.** Choose the smallest input that exercises the logic, and track every variable in a small table, one row per loop iteration. The discipline is to execute the code *as written*: an off-by-one shows up when you write down the actual value of `i` at the last iteration, not when you think "and then it reaches the end".

> [!example] Worked example · 계산 예제
> Trace `longest_run([4, 2, 3, 2])`. The set is {2, 3, 4} (iteration order in a real run may differ; it does not change the result).
>
> | `x` | `x - 1` in set? | walk | `length` | `best` |
> |---|---|---|---|---|
> | 2 | no | 3 yes, 4 yes, 5 no | 3 | 3 |
> | 3 | yes | skipped | — | 3 |
> | 4 | yes | skipped | — | 3 |
>
> Result 3. The repeated 2 vanished when the set was built, which is exactly why this version handles duplicates — and why a version that works on the raw list might not.

**The edge-case checklist.** Run through this list for every problem. Most items take seconds to check, and each one catches a typical bug.

| Case | Example | What it catches |
|---|---|---|
| Empty input | `[]`, `""`, a graph with no edges | indexing `nums[0]`, `max()` of an empty sequence, a missing base case |
| One element | `[7]` | loops over pairs that never run, a `best` initialised wrongly |
| Duplicates | `[2, 2, 2]` | logic that assumes distinct values, `>` versus `>=` |
| Negative numbers and zero | `[-3, 0, 2]` | a "maximum" initialised to 0, modulo of negatives (§3, §4) |
| Overflow | 10⁵ values of 10⁹ summed in C++ | a sum or product in `int` instead of `long long` |
| Already sorted, or reverse sorted | `[1, 2, 3, 4]`, `[4, 3, 2, 1]` | a pivot choice that goes quadratic, an early exit that never fires |
| Maximum size | n at the stated limit | a hidden O(n²), recursion depth, memory |

Add problem-specific cases: for graphs, a disconnected graph and a self-loop; for strings, one repeated character; for geometry, collinear or coincident points; for intervals, intervals that touch at an endpoint.

**Stress testing.** Hand tests only find the bugs you thought of. A stress test finds the ones you did not. It has four parts: the fast solution you want to trust; a slow reference solution simple enough to be obviously correct (your brute force from step 3); a generator of random small inputs; and a loop that runs both on each input and stops at the first disagreement. Two independent programs rarely share the same bug, so any disagreement points at one of them. Two refinements make it much more useful. **Keep the inputs small and the value range narrow,** so repeats, zeros and ties actually occur. **Shrink the failing input** before debugging it, because a four-element counterexample is readable and a forty-element one is not.

The harness below tests a sort-based version of `longest_run`. It looks right and passes `[1, 2, 3]`, `[5, 9]` and `[]`, but it contains a bug that the harness finds in well under a second.

```python
import random

def longest_run_slow(nums):
    """Reference: obviously correct, far too slow for large inputs."""
    best = 0
    for start in nums:
        length = 0
        while start + length in nums:              # linear scan of the list each time
            length += 1
        best = max(best, length)
    return best

def longest_run_sorted(nums):
    """Candidate: sort, then count steps of +1 between neighbours."""
    if not nums:
        return 0
    xs = sorted(nums)
    best = run = 1
    for prev, cur in zip(xs, xs[1:]):
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    return best

def longest_run_sorted_fixed(nums):
    if not nums:
        return 0
    xs = sorted(nums)
    best = run = 1
    for prev, cur in zip(xs, xs[1:]):
        if cur == prev:
            continue                               # a repeat neither extends nor breaks a run
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    return best

def shrink(nums, fails):
    """Delete elements one at a time while the input still fails."""
    i = 0
    while i < len(nums):
        smaller = nums[:i] + nums[i + 1:]
        if fails(smaller):
            nums = smaller
        else:
            i += 1
    return nums

def stress(fast, slow, trials=3000, seed=0):
    rng = random.Random(seed)                      # fixed seed: a failure can be replayed
    for trial in range(trials):
        n = rng.randint(0, 2 + trial // 100)       # start tiny, grow slowly
        nums = [rng.randint(-3, 3) for _ in range(n)]
        if fast(nums) != slow(nums):
            small = shrink(nums, lambda xs: fast(xs) != slow(xs))
            return small, slow(small), fast(small)
    return None                                    # no disagreement found

print(stress(longest_run_sorted, longest_run_slow))       # ([1, -1, 0, 0], 3, 2)
assert stress(longest_run_sorted_fixed, longest_run_slow) is None
```

The harness reports that on `[1, -1, 0, 0]` the reference answers 3 and the candidate answers 2. Shrinking stopped at four elements because deleting any one of them makes the failure disappear, and with four elements the bug is visible at once. Sorted, the input is −1, 0, 0, 1. The step from −1 to 0 makes a run of 2; the repeated 0 differs from its neighbour by 0, not 1, so the run is reset to 1; the step from 0 to 1 then only reaches 2. A repeat must neither extend nor break a run, so the fix skips equal neighbours. After the fix, the same seed runs all 3000 trials without a disagreement; then rerun with larger `n` and a wider value range.

Know the limits of the method. If the problem has several correct outputs (any shortest path, any valid ordering), compare with a *checker* that verifies the output's properties rather than with an exact answer. Bugs in shared code — the input parser, or the generator never producing an empty list — are invisible to it. And it tests only the sizes the slow solution can handle, so still run one maximum-size input for time. Property-based testing libraries such as Hypothesis for Python automate generation and shrinking; knowing how to write the fifteen-line version yourself is what the interview checks.

### 3. Python for interviews

*From here the page changes format. §3 and §4 are lookup tables: each bold entry is one self-contained trap with a runnable check, and no entry depends on the one before. Read them straight through once, then return to single entries before an interview.*

Python lets you write an interview solution in half the lines of C++, provided you know the standard library and its costs. Ask which Python version the environment runs: a few tools below need 3.9 or 3.10.

| Need | Tool | Cost |
|---|---|---|
| Queue, sliding window | `collections.deque` | append and pop at both ends O(1) |
| Counting | `collections.Counter` | O(1) average per update |
| Map with a default value | `collections.defaultdict` | O(1) average |
| Repeated minimum, top-k | `heapq` on a list | push and pop O(log n), `heapify` O(n) |
| Search in a sorted list | `bisect` | search O(log n); `insort` is O(n) because it shifts |
| Prefix sums, pairs, products | `itertools` | lazy, O(1) memory per step |
| Memoised recursion | `functools.cache` | one dictionary entry per distinct argument tuple |

The "Cost" column uses two words with exact meanings that are defined elsewhere in the track. **Average O(1)** for a hash-based container is the *expected* cost per operation when keys spread evenly over the buckets, not a guarantee for every operation ([[02-foundations/algorithms/data-structures|11.2 §3]]). **Amortised O(1)**, used for `append` and `push_back` below, is a guarantee about sequences: any $k$ operations starting from an empty structure cost at most a constant times $k$ in total, so a single expensive resize is paid for by the many cheap appends before it ([[02-foundations/algorithms/complexity-recursion|11.1 §4]]).

**collections.** A `Counter` reads a missing key as 0 without inserting it. A `defaultdict(list)` creates the missing entry on first access. A `deque(maxlen=k)` is a ready-made fixed-size window.

```python
from collections import Counter, defaultdict, deque

words = "the robot saw the wall and the door".split()
counts = Counter(words)
assert counts["the"] == 3 and counts["window"] == 0     # missing key reads as 0
assert "window" not in counts                            # ...and was not inserted
assert counts.most_common(1) == [("the", 3)]

by_length = defaultdict(list)                            # missing key starts as list()
for word in words:
    by_length[len(word)].append(word)
assert by_length[4] == ["wall", "door"]

recent = deque(maxlen=3)                                 # oldest item falls off the left
for reading in [5, 6, 7, 8]:
    recent.append(reading)
assert list(recent) == [6, 7, 8]
assert recent.popleft() == 6                             # O(1); list.pop(0) is O(n)
```

**heapq.** It is a min-heap stored in a plain list: the list satisfies `a[i] <= a[2*i + 1]` and `a[i] <= a[2*i + 2]` for every index where those children exist, so `a[0]` is always the smallest ([[02-foundations/algorithms/data-structures|11.2 §4]] defines the heap and proves the costs). For a max-heap, push negated keys, since a > b exactly when −a < −b, so the smallest negated key belongs to the largest original (Python 3.14 added `heappush_max` and related functions, but interview environments are often older). Entries are usually tuples, compared element by element, so put a counter before any payload that cannot be compared.

```python
import heapq
from itertools import count

def k_closest(points, k):
    """The k points nearest the origin, in O(n log k) time and O(k) memory."""
    heap = []                                   # (-squared distance, x, y): root is the farthest kept
    for x, y in points:
        d2 = x * x + y * y                      # squared distances: exact integers, no sqrt
        if len(heap) < k:
            heapq.heappush(heap, (-d2, x, y))
        elif d2 < -heap[0][0]:
            heapq.heapreplace(heap, (-d2, x, y))
    return sorted((x, y) for _, x, y in heap)

assert k_closest([(3, 3), (1, 0), (-2, 2), (0, -1), (5, 1)], 2) == [(0, -1), (1, 0)]

order = count()                                 # tie-breaker: dicts cannot be compared
tasks = []
heapq.heappush(tasks, (1, next(order), {"name": "scan"}))
heapq.heappush(tasks, (1, next(order), {"name": "grasp"}))
assert heapq.heappop(tasks)[2]["name"] == "scan"
assert heapq.nsmallest(2, [7, 1, 5, 3]) == [1, 3]
```

**bisect.** `bisect_left(a, x)` is the first index whose value is at least `x`; `bisect_right(a, x)` is the first index whose value is greater than `x`. Together they cut out a range of a sorted list, which is how you match a message to the nearest sensor timestamp.

```python
from bisect import bisect_left, bisect_right

stamps = [0.0, 0.1, 0.1, 0.2, 0.35, 0.5]                # sorted timestamps, seconds
lo, hi = bisect_left(stamps, 0.1), bisect_right(stamps, 0.35)
assert stamps[lo:hi] == [0.1, 0.1, 0.2, 0.35]            # every sample with 0.1 <= t <= 0.35

def nearest_index(sorted_values, target):
    """Index of the value closest to target; ties go to the earlier value."""
    i = bisect_left(sorted_values, target)
    if i == 0:
        return 0
    if i == len(sorted_values):
        return i - 1
    before, after = sorted_values[i - 1], sorted_values[i]
    return i - 1 if target - before <= after - target else i

assert nearest_index(stamps, 0.27) == 3
assert nearest_index(stamps, -1.0) == 0 and nearest_index(stamps, 9.0) == 5

scans = [(0.05, "a"), (0.3, "b")]                        # key= needs Python 3.10+
assert bisect_left(scans, 0.3, key=lambda scan: scan[0]) == 1
```

**itertools and functools.cache.** `accumulate` builds prefix sums, `pairwise` gives neighbours, `combinations` and `product` enumerate small search spaces. `@cache` memoises a recursive function; its arguments must be hashable (a list argument raises `TypeError`, so pass a tuple), and the cache lives as long as the function, so call `cache_clear()` between unrelated test cases.

```python
from functools import cache
from itertools import accumulate, combinations, pairwise, product

readings = [3, 1, 4, 1, 5]
prefix = [0, *accumulate(readings)]                      # prefix[i] = sum(readings[:i])
assert prefix[4] - prefix[1] == 1 + 4 + 1                # any range sum in O(1)
assert [b - a for a, b in pairwise(readings)] == [-2, 3, -3, 4]   # Python 3.10+
assert len(list(combinations(range(5), 2))) == 10        # unordered pairs
assert len(list(product([0, 1], repeat=3))) == 8         # every 3-bit pattern

@cache                                                   # Python 3.9+; before: lru_cache(maxsize=None)
def ways(steps):
    """Ways to climb a staircase taking 1 or 2 steps at a time."""
    if steps <= 1:
        return 1
    return ways(steps - 1) + ways(steps - 2)

assert ways(80) == 37889062373143906
```

**Correctness pitfalls.** Each of these produces code that runs and returns a wrong answer, which is the worst kind of bug in an interview.

- **Mutable default arguments.** The default value is evaluated once, when `def` runs, so a default list is shared by every call.
- **Aliased rows.** `[ [0] * m ] * n` makes a list of n references to *one* row. Build rows in a comprehension.
- **Integer division and negative numbers.** `//` rounds toward minus infinity and `%` takes the sign of the divisor: `-7 // 2` is `-4` and `-7 % 2` is `1`. C++ and Java give `-3` and `-1`. `int(a / b)` truncates but goes through a float and is wrong for large integers. Precisely, both languages define quotient $q$ and remainder $r$ of $a$ by $b \ne 0$ through the same identity, and differ only in how $q$ is rounded, so the remainder's sign follows from the choice of $q$:
$$a = b\,q + r, \qquad q_{\text{Python}} = \lfloor a / b \rfloor, \qquad q_{\text{C++}} = \operatorname{trunc}(a / b)$$
  Python's floor gives $0 \le r < b$ for $b > 0$; C++'s truncation toward zero gives $r$ the sign of $a$. Check with $a = -7$, $b = 2$: Python $q = -4$, $r = -7 - 2(-4) = 1$; C++ $q = -3$, $r = -7 - 2(-3) = -1$.
- **Recursion limit.** CPython stops at about 1000 frames by default; see [[02-foundations/algorithms/complexity-recursion|11.1 §5]] for the fixes.
- **Float comparison.** `0.1 + 0.2 == 0.3` is false. Compare with `math.isclose`, or avoid floats entirely by comparing squared integer distances or cross-multiplied fractions.
- **`is` versus `==`.** `is` asks whether two names refer to the same object; `==` asks whether the values are equal. Use `is` only for `None` and deliberate sentinels. Small integers happen to be cached in CPython, so `is` on numbers sometimes works in testing and fails on real data.
- **Sorting.** `list.sort` and `sorted` are guaranteed stable, including with `reverse=True`. A sort is **stable** when elements with equal keys keep their input order: if $\text{key}(a) = \text{key}(b)$ and $a$ comes before $b$ in the input, then $a$ comes before $b$ in the output. That property is what makes the two-pass sort in the code below correct, since the second pass (by count) leaves the first pass's name order intact among equal counts; with an unstable sort, `("c", 2)` could land before `("b", 2)`. Sort by a `key` function (computed once per element), or by a tuple key such as `(-score, name)`; `functools.cmp_to_key` exists but is rarely needed.

```python
import math

def add_bad(item, bucket=[]):            # one list, created when def runs
    bucket.append(item)
    return bucket

def add_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

assert add_bad(1) == [1] and add_bad(2) == [1, 2]        # the first call's item is still there
assert add_good(1) == [1] and add_good(2) == [2]

n, m = 2, 3
aliased = [ [0] * m ] * n
aliased[0][0] = 7
assert aliased[1][0] == 7                                # both "rows" are the same list
grid = [ [0] * m for _ in range(n)]
grid[0][0] = 7
assert grid[1][0] == 0

assert -7 // 2 == -4 and -7 % 2 == 1                     # floor toward minus infinity
def div_toward_zero(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
assert div_toward_zero(-7, 2) == -3
assert div_toward_zero(-(10**20 + 1), 1) == -(10**20 + 1)
assert int(-(10**20 + 1) / 1) != -(10**20 + 1)           # the float route loses the last digit

assert 0.1 + 0.2 != 0.3 and math.isclose(0.1 + 0.2, 0.3)

runs = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
runs.sort(key=lambda r: r[0])                            # secondary key first...
runs.sort(key=lambda r: r[1], reverse=True)              # ...then primary; stability keeps the order
assert runs == [("b", 2), ("c", 2), ("a", 1), ("d", 1)]
assert sorted(runs, key=lambda r: (-r[1], r[0])) == runs # the same in one pass
```

**Performance pitfalls.** These give the right answer too slowly, and they hide inside code that looks linear.

- `list.pop(0)` and `list.insert(0, x)` shift every element: O(n). Use a `deque`.
- `x in some_list` is a linear scan; `x in some_set` is O(1) on average. Inside a loop, that is the difference between O(n²) and O(n).
- Strings are immutable, so `s += piece` in a loop may copy the whole string each time (CPython sometimes avoids the copy; do not rely on it). Collect pieces in a list and `"".join` once.
- Slicing copies: `nums[1:]` inside a recursion turns O(n) into O(n²). Pass indices instead.

```python
import timeit
from collections import deque

pieces = [str(i) for i in range(10_000)]
text = "".join(pieces)                                   # one pass over all pieces
assert text.startswith("0123")

ids_list = list(range(100_000))
ids_set = set(ids_list)
t_list = timeit.timeit(lambda: 99_999 in ids_list, number=200)
t_set = timeit.timeit(lambda: 99_999 in ids_set, number=200)
print(f"in list: {t_list:.4f} s   in set: {t_set:.6f} s")

queue_list, queue_deque = list(range(50_000)), deque(range(50_000))
t_pop0 = timeit.timeit(lambda: queue_list.pop(0), number=20_000)
t_popleft = timeit.timeit(lambda: queue_deque.popleft(), number=20_000)
print(f"list.pop(0): {t_pop0:.4f} s   deque.popleft(): {t_popleft:.4f} s")
```

On a laptop the set lookup is thousands of times faster than the list scan, and `pop(0)` on a 50 000-element list is roughly a hundred times slower than `popleft`. The exact numbers do not matter; the ratio grows with n.

### 4. C++ for interviews

C++ interviews check the same algorithms plus whether you know what the language does not protect you from: overflow, invalidated iterators, and contracts whose violation is undefined behaviour rather than an error message. **Undefined behaviour** (UB) is a category in the C++ standard with two defining parts: (1) the program performs an operation for which the standard imposes *no requirements at all*, such as signed integer overflow, reading past the end of an array, or dereferencing a dangling iterator; and (2) because nothing is required, the compiler may assume the operation never happens and optimise on that assumption. So UB is not "some unspecified result": the same code can print the expected value in a debug build, a different value with `-O2`, or crash. *Example:* `2 * big` with `int big = 2'000'000'000` is UB, because $4 \times 10^9$ exceeds `INT_MAX` $= 2\,147\,483\,647$. *Non-example:* unsigned overflow is defined, since unsigned arithmetic wraps modulo $2^{\text{bits}}$, which is exactly why `v.size() - 1` on an empty vector is a huge number instead of UB. Every snippet below is a complete program that compiles with `c++ -std=c++17` and checks its claims with `assert`.

| Python habit | C++ tool | Cost | Trap |
|---|---|---|---|
| `list` | `std::vector` | push_back amortised O(1) | reallocation invalidates iterators and references |
| `dict`, `set` | `std::unordered_map`, `std::unordered_set` | average O(1), worst O(n) | `operator[]` inserts; no hash for `std::pair` |
| sorted containers | `std::map`, `std::set` | O(log n), ordered iteration | use the member `lower_bound`, not `std::lower_bound` |
| `heapq` | `std::priority_queue` | push and pop O(log n) | **max**-heap by default |
| tuples | `std::pair`, `std::tuple`, a small `struct` | — | `first` and `second` say nothing about meaning |

**Containers, heaps, and structured bindings.** `std::priority_queue<T>` keeps the *largest* element on top; pass `std::greater<>` as the comparator for a min-heap. Structured bindings (C++17) unpack pairs and tuples by name. `std::map` and `std::set` have their own `lower_bound`, which is O(log n); the free function `std::lower_bound` on their iterators makes only O(log n) comparisons, but those iterators are bidirectional rather than random access, so each jump to the middle of a range must step through the tree one node at a time, which is O(n).

```cpp
#include <algorithm>
#include <cassert>
#include <functional>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

int main() {
    std::vector<int> readings = {5, 1, 4, 1, 5, 9, 2, 6};

    std::unordered_map<int, int> count;
    for (int r : readings) ++count[r];              // operator[] inserts 0, then increments
    assert(count.at(5) == 2);
    assert(count.find(7) == count.end());           // look up without inserting
    assert(count[7] == 0 && count.count(7) == 1);   // operator[] just inserted key 7

    std::map<std::string, int> rate_hz = {{"lidar", 10}, {"imu", 200}};
    assert(rate_hz.begin()->first == "imu");        // iteration is in key order

    std::set<int> seen(readings.begin(), readings.end());
    assert(*seen.lower_bound(3) == 4);              // member function: O(log n)

    std::priority_queue<int> max_heap(readings.begin(), readings.end());
    assert(max_heap.top() == 9);                    // largest on top
    std::priority_queue<int, std::vector<int>, std::greater<>> min_heap(readings.begin(), readings.end());
    assert(min_heap.top() == 1);

    std::vector<std::pair<int, std::string>> jobs = {{3, "plan"}, {1, "sense"}, {2, "act"}};
    std::sort(jobs.begin(), jobs.end());            // pairs compare first, then second
    std::string order;
    for (const auto& [priority, name] : jobs) order += name + " ";
    assert(order == "sense act plan ");
}
```

**References versus copies, overflow, and division.** `for (auto x : v)` copies each element, so changes are lost and large elements are copied; `for (auto& x : v)` modifies in place; `for (const auto& x : v)` reads without copying. Signed overflow is undefined behaviour, and an `int` holds only up to about 2.1 × 10⁹. Widen *before* the arithmetic, write the binary-search midpoint as `lo + (hi - lo) / 2`, and give `std::accumulate` a `0LL` start value, because its result type is the type of that argument. Integer division truncates toward zero, and `size()` is unsigned, so `v.size() - 1` on an empty vector is a huge number.

```cpp
#include <cassert>
#include <cstddef>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3};
    for (auto x : v) x *= 10;                   // x is a copy: v is unchanged
    assert(v[0] == 1);
    for (auto& x : v) x *= 10;                  // x is a reference: v changes
    assert(v[0] == 10);

    int big = 2'000'000'000;                    // fits: INT_MAX is 2'147'483'647
    long long doubled = 2LL * big;              // widen first; `2 * big` overflows (undefined behaviour)
    assert(doubled == 4'000'000'000LL);

    std::vector<int> large(3, big);
    assert(std::accumulate(large.begin(), large.end(), 0LL) == 6'000'000'000LL);  // 0LL, not 0

    int lo = 1'500'000'000, hi = 2'000'000'000;
    int mid = lo + (hi - lo) / 2;               // (lo + hi) / 2 would overflow
    assert(mid == 1'750'000'000);

    assert(-7 / 2 == -3 && -7 % 2 == -1);       // truncation toward zero; Python gives -4 and 1
    int a = -7, m = 5;
    assert(((a % m) + m) % m == 3);             // a non-negative remainder

    std::vector<int> empty;
    int iterations = 0;
    for (std::size_t i = 0; i + 1 < empty.size(); ++i) ++iterations;   // not: i < empty.size() - 1
    assert(iterations == 0);
}
```

**Iterator invalidation.** When `push_back` needs more capacity than the vector has, it moves every element to a new buffer, and all iterators, pointers and references into the old buffer dangle. When it does not reallocate, only `end()` is invalidated. `erase` invalidates iterators and references at and after the erased position. The safe patterns: keep an *index* rather than a pointer into a growing vector; inside a loop, continue from the iterator that `erase` returns; and to remove many elements, use the erase–remove idiom (one O(n) pass) rather than repeated `erase` calls (O(n) each). C++20 adds `std::erase_if` for the same thing.

```cpp
#include <algorithm>
#include <cassert>
#include <cstddef>
#include <vector>

int main() {
    std::vector<int> path = {10};
    std::size_t start_index = 0;                // an index survives reallocation
    // int& start = path[0];                    // a reference would dangle after the loop below
    for (int k = 0; k < 1000; ++k) path.push_back(k);
    assert(path[start_index] == 10);

    std::vector<int> ids = {1, 2, 3, 4, 6, 7};
    for (auto it = ids.begin(); it != ids.end();) {
        if (*it % 2 == 0) it = ids.erase(it);   // erase returns the next valid iterator
        else ++it;
    }
    assert((ids == std::vector<int>{1, 3, 7}));

    std::vector<int> ids2 = {1, 2, 3, 4, 6, 7};
    ids2.erase(std::remove_if(ids2.begin(), ids2.end(), [](int x) { return x % 2 == 0; }), ids2.end());
    assert((ids2 == std::vector<int>{1, 3, 7}));
}
```

**`unordered_map`: worst case and custom hashes.** Average O(1) assumes keys spread over the buckets. If many keys land in the same bucket — a weak hash on structured keys, or inputs chosen against a known hash — every operation degrades toward O(n). The standard library provides no `std::hash` for `std::pair`, so a grid-cell key needs your own hash; combine the two coordinates into one 64-bit value and mix its bits (below, the finalizer of the SplitMix64 generator). Its multiply–xor–shift steps let every input bit change about half of the output bits, so neighbouring cells such as `{0, 0}` and `{0, 1}`, whose raw keys differ in one bit, land in unrelated buckets instead of clustering in adjacent ones. When inputs may be adversarial, some programmers also add a random per-run offset to the key; in research code, reproducibility usually matters more. Call `reserve` before a large insert loop to avoid repeated rehashing, which also invalidates iterators (but not references to elements).

```cpp
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <unordered_map>
#include <unordered_set>
#include <utility>

struct CellHash {
    std::size_t operator()(const std::pair<int, int>& cell) const noexcept {
        std::uint64_t key = (static_cast<std::uint64_t>(static_cast<std::uint32_t>(cell.first)) << 32)
                          | static_cast<std::uint32_t>(cell.second);
        key += 0x9e3779b97f4a7c15ULL;                         // SplitMix64 finalizer
        key = (key ^ (key >> 30)) * 0xbf58476d1ce4e5b9ULL;
        key = (key ^ (key >> 27)) * 0x94d049bb133111ebULL;
        return static_cast<std::size_t>(key ^ (key >> 31));
    }
};

int main() {
    std::unordered_set<std::pair<int, int>, CellHash> occupied;
    occupied.insert({-1, 2});
    occupied.insert({2, -1});                                 // swapped coordinates: a different cell
    assert(occupied.size() == 2 && occupied.count({-1, 2}) == 1);

    std::unordered_map<std::pair<int, int>, int, CellHash> hits;
    hits.reserve(1 << 12);                                    // allocate buckets once, up front
    for (int x = -30; x < 30; ++x)
        for (int y = -30; y < 30; ++y) ++hits[{x / 3, y / 3}];
    assert(hits.at({0, 0}) == 25);                            // x/3 == 0 for x in -2..2
}
```

**`std::sort` needs a strict weak ordering.** The comparator must behave like `<`: `comp(a, a)` is false; if `comp(a, b)` then not `comp(b, a)`; and it is transitive, including for "neither is less". Writing `<=` breaks the first rule, and comparing floating-point keys that contain NaN breaks the last one. Written as the four conditions of the *Compare* requirement, with $a \prec b$ meaning `comp(a, b)` is true and **incomparability** $a \sim b$ meaning neither is less:
$$a \sim b \iff \neg(a \prec b) \wedge \neg(b \prec a)$$

- **Irreflexivity:** $\neg(a \prec a)$ for every $a$.
- **Asymmetry:** $a \prec b$ implies $\neg(b \prec a)$.
- **Transitivity:** $a \prec b$ and $b \prec c$ imply $a \prec c$.
- **Transitivity of incomparability:** $a \sim b$ and $b \sim c$ imply $a \sim c$, so "equal for sorting purposes" groups the elements into clean equivalence classes that the sort can place side by side.

*Non-examples.* `<=` fails irreflexivity, because `comp(a, a)` is true. An "approximately less" comparator `a < b - 1` satisfies the first three but fails the fourth: $0 \sim 0.8$ and $0.8 \sim 1.6$, yet $0 \prec 1.6$ because $0 < 0.6$. NaN fails the fourth for plain `<`: every comparison with NaN is false, so $1 \sim \text{NaN}$ and $\text{NaN} \sim 2$ although $1 \prec 2$.

The result is undefined behaviour — in practice wrong orders, infinite loops or out-of-bounds reads, depending on the library. Compare field by field, or build `std::tie` tuples. `std::sort` is not stable; use `std::stable_sort` when ties must keep their input order.

```cpp
#include <algorithm>
#include <cassert>
#include <string>
#include <utility>
#include <vector>

struct Task {
    int priority;
    double deadline_s;
    std::string name;
};

int main() {
    std::vector<Task> tasks = {{2, 5.0, "grasp"}, {1, 3.0, "scan"}, {2, 1.0, "move"}, {1, 3.0, "log"}};
    // Higher priority first, then earlier deadline, then name. Never `>=` or `<=` here.
    std::sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        if (a.priority != b.priority) return a.priority > b.priority;
        if (a.deadline_s != b.deadline_s) return a.deadline_s < b.deadline_s;
        return a.name < b.name;
    });
    assert(tasks[0].name == "move" && tasks[1].name == "grasp");
    assert(tasks[2].name == "log" && tasks[3].name == "scan");

    std::vector<std::pair<int, char>> v = {{1, 'b'}, {0, 'z'}, {1, 'a'}};
    std::stable_sort(v.begin(), v.end(), [](const auto& x, const auto& y) { return x.first < y.first; });
    assert(v[1].second == 'b' && v[2].second == 'a');         // ties keep their input order
}
```

**Fast input and output.** By default the C++ streams stay synchronised with C's `stdio` and `std::cin` flushes `std::cout` before every read. For large inputs, switch both off at the start of `main`, and end lines with `'\n'`: `std::endl` also flushes, once per line.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);       // stop synchronising with C stdio
    std::cin.tie(nullptr);                  // do not flush cout before each read
    int n = 0;
    if (!(std::cin >> n)) return 0;
    std::vector<long long> values(n);
    for (auto& value : values) std::cin >> value;
    long long total = 0;
    for (long long value : values) total += value;
    std::cout << total << '\n';             // '\n', not std::endl
}
```

Fed `3 1 2 3` on standard input, it prints `6`. After turning synchronisation off, do not mix `scanf`/`printf` with the streams in the same program.

### 5. Code that research labs read

A research-lab interviewer reads your code the way a labmate will: will it be obvious what this computes, in which frame and units, and will it fail loudly when an assumption breaks? The habits are the same ones that keep interview code bug-free.

- **Names carry meaning and units.** `dist_m`, `dt_s`, `omega_radps`, `T_world_base` instead of `d`, `t`, `w`, `T`. A one-letter name is fine for a three-line loop counter; two nested loops with `i` and `j` are where the swapped-index bug lives, so name them `row` and `col`.
- **Small functions, one job each.** Keep reading input, computing, and printing in separate functions. The computing function can then be called from a stress test or a unit test without faking input files.
- **Assertions for invariants.** An `assert` states something that must be true if *your* code is correct: a probability sums to 1, an index is in range, a quaternion has unit norm. It documents the reasoning and turns a silent wrong answer into an immediate failure. Do not use `assert` to validate *inputs* from callers or files — `python -O` strips assertions — and raise `ValueError` instead.
- **Shapes and units in comments for numeric code.** Write the shape of every array argument and result, such as `(N, 3) points in metres, world frame`. Most bugs in numeric code are shape and frame bugs, and NumPy broadcasting will silently turn a wrong shape into a wrong answer.
- **Vectorize when asked, and say what it costs.** Loops in Python run at interpreter speed; one NumPy expression runs the loop in compiled code. **Broadcasting** is NumPy's rule for combining arrays of different shapes elementwise, in three steps: (1) align the two shapes at their *right* ends, padding the shorter one with leading 1s; (2) each aligned pair of axis lengths must be equal or contain a 1, otherwise NumPy raises an error; (3) the result takes the larger length on every axis, and an axis of length 1 is reused (stretched) along it without copying. So for aligned lengths $p$ and $r$, the check that step (2) performs and the output length are
$$p = r \ \text{ or } \ p = 1 \ \text{ or } \ r = 1, \qquad \text{out} = \max(p, r)$$
  *Example:* `(2, 3)` with `(3,)` pads to `(1, 3)` and gives `(2, 3)`. *Non-example:* `(2, 3)` with `(2,)` pads to `(1, 2)`, and $3$ against $2$ fails, so it raises; `(2, 1)` is what "one value per row" needs. Broadcasting aligns shapes from the right and stretches axes of length 1, so an `(N, 1, D)` array minus a `(1, M, D)` array gives every pairwise difference as `(N, M, D)`. That array uses N·M·D floats of memory; multiplying out (a − b)·(a − b) gives the expanded form ‖a‖² + ‖b‖² − 2a·b, which needs only `(N, M)`, but rounding can make a tiny true distance slightly negative, so clamp at zero before the square root.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="Broadcasting. Top: a 2 by 3 array plus a length-3 vector; the vector is padded to shape (1, 3) and its single row is reused for both rows, giving (2, 3). Bottom: shapes aligned at the right. (2, 3) with (3,) gives (2, 3); (2, 3) with (2,) pads to (1, 2) and 3 against 2 fails; (N, 1, D) with (1, M, D) gives (N, M, D).">
  <defs><marker id="aicBc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="20" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="40" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="60" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="20" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="40" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="60" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="50" y="92" font-size="11" fill="currentColor" text-anchor="middle">(2, 3)</text>
  <text x="100" y="59" font-size="14" fill="currentColor" text-anchor="middle">+</text>
  <rect x="118" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="138" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="158" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <text x="148" y="92" font-size="11" fill="currentColor" text-anchor="middle">(3,)</text>
  <text x="206" y="59" font-size="14" fill="currentColor" text-anchor="middle">→</text>
  <rect x="224" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="244" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="264" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="224" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <rect x="244" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <rect x="264" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <line x1="294" y1="44" x2="294" y2="64" stroke="currentColor" stroke-width="1.1" marker-end="url(#aicBc)"/>
  <text x="254" y="92" font-size="11" fill="currentColor" text-anchor="middle">(1, 3), one row reused</text>
  <text x="334" y="59" font-size="14" fill="currentColor" text-anchor="middle">=</text>
  <rect x="352" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="372" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="392" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="352" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="372" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="392" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <text x="382" y="92" font-size="11" fill="currentColor" text-anchor="middle">(2, 3)</text>
  <text x="8" y="124" font-size="12" fill="currentColor">align at the right; each pair must be equal or contain a 1</text>
  <text x="78" y="150" font-size="11" fill="currentColor" font-weight="bold">example</text>
  <text x="70" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="78" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="95" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <rect x="116" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="133" y="174" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="70" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="78" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="95" y="200" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <rect x="116" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="133" y="200" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="95" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="133" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="78" y="250" font-size="11" fill="currentColor">result: (2, 3)</text>
  <text x="78" y="268" font-size="10" fill="currentColor" fill-opacity="0.8">padded 1 (dashed)</text>
  <text x="258" y="150" font-size="11" fill="currentColor" font-weight="bold">non-example</text>
  <text x="250" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="258" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="275" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <rect x="296" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="313" y="174" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="250" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="258" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="275" y="200" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <rect x="296" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="313" y="200" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="275" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="313" y="226" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">✗</text>
  <text x="258" y="250" font-size="11" fill="currentColor">error: 3 vs 2</text>
  <text x="258" y="268" font-size="10" fill="currentColor" fill-opacity="0.8">padded 1 (dashed)</text>
  <text x="420" y="150" font-size="11" fill="currentColor" font-weight="bold">pairwise differences</text>
  <text x="412" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="420" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="437" y="174" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">N</text>
  <rect x="458" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="475" y="174" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <rect x="496" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="513" y="174" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">D</text>
  <text x="412" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="420" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="437" y="200" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <rect x="458" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="475" y="200" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">M</text>
  <rect x="496" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="513" y="200" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">D</text>
  <text x="437" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="475" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="513" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="420" y="250" font-size="11" fill="currentColor">result: (N, M, D)</text>
</svg>

- **Determinism.** Seed every random source and pass generators explicitly, so a failure can be replayed. Iteration order over a `set` of strings changes between interpreter runs (string hashing is randomised per process), so sort before iterating when order affects the output.

```python
import math

def wrap_to_pi(angle_rad):
    """Map an angle in radians into [-pi, pi]."""
    wrapped = (angle_rad + math.pi) % (2.0 * math.pi) - math.pi
    assert -math.pi <= wrapped <= math.pi, wrapped      # closed on purpose: see the self-check
    return wrapped

def unicycle_step(pose, v_mps, omega_radps, dt_s):
    """One explicit Euler step. pose = (x_m, y_m, theta_rad) in the world frame."""
    if dt_s <= 0.0:
        raise ValueError(f"dt_s must be positive, got {dt_s}")   # input check: not an assert
    x_m, y_m, theta_rad = pose
    return (x_m + v_mps * math.cos(theta_rad) * dt_s,
            y_m + v_mps * math.sin(theta_rad) * dt_s,
            wrap_to_pi(theta_rad + omega_radps * dt_s))

pose = unicycle_step((0.0, 0.0, 3.1), v_mps=1.0, omega_radps=1.0, dt_s=0.1)
assert -math.pi <= pose[2] < 0.0                         # 3.2 rad wrapped to about -3.08
assert wrap_to_pi(math.nextafter(-math.pi, -math.inf)) == math.pi
```

```python
import numpy as np

def pairwise_distances(a, b):
    """Euclidean distance between every row of a and every row of b.

    a: (N, D) points, metres;  b: (M, D) points, metres;  returns (N, M), metres.
    Memory: a temporary (N, M, D) array.
    """
    assert a.ndim == 2 and b.ndim == 2 and a.shape[1] == b.shape[1], (a.shape, b.shape)
    diff = a[:, None, :] - b[None, :, :]                 # (N, 1, D) - (1, M, D) -> (N, M, D)
    return np.sqrt((diff ** 2).sum(axis=-1))             # (N, M)

def pairwise_distances_low_memory(a, b):
    """Same result with only (N, M) temporaries."""
    sq = (a ** 2).sum(axis=1)[:, None] + (b ** 2).sum(axis=1)[None, :] - 2.0 * (a @ b.T)
    return np.sqrt(np.maximum(sq, 0.0))                  # rounding can make sq slightly negative

rng = np.random.default_rng(seed=0)                      # a local, seeded generator
a = rng.normal(size=(50, 3))
b = rng.normal(size=(40, 3))
reference = np.empty((50, 40))
for i in range(50):
    for j in range(40):
        reference[i, j] = np.linalg.norm(a[i] - b[j])
assert np.allclose(pairwise_distances(a, b), reference)
assert np.allclose(pairwise_distances_low_memory(a, b), reference, atol=1e-6)
assert np.array_equal(np.random.default_rng(7).normal(size=3), np.random.default_rng(7).normal(size=3))
```

### 6. Real-time and robotics caveats

A control loop that runs at 1 kHz has a deadline every millisecond, and a late answer is a wrong answer. Code that is fast on average is not enough; what matters is the *worst-case* time of one iteration, because that decides whether a deadline is missed. Three ordinary tools have unbounded or unpredictable worst cases, so real-time code keeps them out of the hot path — the code that runs every cycle.

**Real-time, defined.** A periodic real-time task has three named parts: a **period** $T$ (1 ms at 1 kHz), a **deadline** $D$ by which each cycle's output must be ready (usually $D = T$), and a **worst-case execution time** (WCET) $C$, the longest one cycle can ever take on that hardware. The task is correct only if every cycle meets the deadline, which needs
$$C \le D$$
In a **hard** real-time system a single miss counts as a failure (a torque loop), while a **soft** one only degrades quality with each miss (a video stream). *Non-example of "real-time":* a loop averaging 0.2 ms per cycle but taking 3 ms once every 10 000 cycles is fast on average and still misses a 1 ms deadline about every $10\,000 / 1000 = 10$ seconds at 1 kHz.

- **Heap allocation.** `new`, `malloc`, and anything that calls them — `std::vector::push_back` past capacity, building a `std::string`, inserting into a `std::map` — may take a lock inside the allocator, search free lists, or ask the operating system for pages. Preallocate everything at start-up: `reserve`, fixed-size `std::array`, and buffers reused every cycle. In an interview, the answer is "allocate in the constructor, never in the loop".
- **Locks.** A mutex held by a lower-priority thread can block the control thread for as long as that thread runs, and a medium-priority thread can stretch that further (priority inversion). **Priority inversion** is a scheduling failure with three parts: a high-priority thread H waits for a lock held by a low-priority thread L; a medium-priority thread M, which needs no lock, becomes ready and preempts L because it outranks L; so H is effectively blocked by M, a thread of *lower* priority, for as long as M runs. Priority-inheritance mutexes fix it by temporarily raising L to H's priority while L holds the lock. Keep critical sections tiny, use `try_lock` and skip the update when it fails, or pass data through a single-producer single-consumer lock-free queue.
- **Exceptions.** Throwing usually allocates the exception object, and unwinding takes time that depends on the stack. Mark hot-path functions `noexcept`, report failure with return values or status flags, and handle errors in a non-real-time thread. The same applies to logging and console output: formatting allocates and writing to a terminal can block.

Python, with its garbage collector and interpreter, belongs outside hard real-time loops; it is fine for planning, perception, and supervision at lower rates. For the ROS 2 side of the same problem — why a long callback stalls a control timer on a single-threaded executor, and which clock a timer follows — read [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]], which also points to real-time scheduling analysis.

The standard structure for "keep the last N samples" in a hot path is a ring buffer over a fixed array: pushing overwrites the oldest sample, and nothing is ever allocated. A **ring buffer** (circular buffer) of capacity $N$ is a fixed array plus two integers, `head` (the slot of the oldest sample) and `size` (how many slots are in use, $0 \le$ `size` $\le N$); indices wrap modulo $N$, so the $i$-th oldest sample and the slot the next push writes are
$$\text{slot}(i) = (\text{head} + i) \bmod N, \qquad \text{write slot} = (\text{head} + \text{size}) \bmod N$$
*Example:* with $N = 3$, pushing 0.1 to 0.5 writes slots 0, 1, 2, then 0 and 1 again, leaving the array `[0.4, 0.5, 0.3]` with `head` = 2, so slots 2, 0, 1 read back 0.3, 0.4, 0.5, oldest first, as the test in the code asserts.

<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="A ring buffer with three slots receiving 0.1 to 0.5. Each row shows the array after one push, the slot written, (head + size) mod 3, and the head after the push. After 0.4 and 0.5 overwrite slots 0 and 1 the array is 0.4, 0.5, 0.3 with head 2, and reading slot (2 + i) mod 3 for i = 0, 1, 2 returns 0.3, 0.4, 0.5, oldest first.">
  <defs><marker id="aicRb" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="106" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <text x="150" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">1</text>
  <text x="194" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">2</text>
  <text x="74" y="34" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.75">slot</text>
  <text x="8" y="60" font-size="11" fill="currentColor">push 0.1</text>
  <rect x="84" y="44" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="106" y="60" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.1</text>
  <rect x="128" y="44" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <rect x="172" y="44" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <path d="M106 70 L101.5 77 L110.5 77 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="60" font-size="11" fill="currentColor">(0 + 0) mod 3 = 0</text>
  <text x="8" y="96" font-size="11" fill="currentColor">push 0.2</text>
  <rect x="84" y="80" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="96" font-size="11" fill="currentColor" text-anchor="middle">0.1</text>
  <rect x="128" y="80" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="150" y="96" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.2</text>
  <rect x="172" y="80" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <path d="M106 106 L101.5 113 L110.5 113 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="96" font-size="11" fill="currentColor">(0 + 1) mod 3 = 1</text>
  <text x="8" y="132" font-size="11" fill="currentColor">push 0.3</text>
  <rect x="84" y="116" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="132" font-size="11" fill="currentColor" text-anchor="middle">0.1</text>
  <rect x="128" y="116" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="150" y="132" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
  <rect x="172" y="116" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="194" y="132" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.3</text>
  <path d="M106 142 L101.5 149 L110.5 149 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="132" font-size="11" fill="currentColor">(0 + 2) mod 3 = 2</text>
  <text x="8" y="168" font-size="11" fill="currentColor">push 0.4</text>
  <rect x="84" y="152" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="106" y="168" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.4</text>
  <rect x="128" y="152" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="150" y="168" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
  <rect x="172" y="152" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="194" y="168" font-size="11" fill="currentColor" text-anchor="middle">0.3</text>
  <path d="M150 178 L145.5 185 L154.5 185 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="168" font-size="11" fill="currentColor">(0 + 3) mod 3 = 0</text>
  <text x="8" y="204" font-size="11" fill="currentColor">push 0.5</text>
  <rect x="84" y="188" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="204" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
  <rect x="128" y="188" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="150" y="204" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.5</text>
  <rect x="172" y="188" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="194" y="204" font-size="11" fill="currentColor" text-anchor="middle">0.3</text>
  <path d="M194 214 L189.5 221 L198.5 221 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="204" font-size="11" fill="currentColor">(1 + 3) mod 3 = 1</text>
  <text x="452" y="30" font-size="11" fill="currentColor" text-anchor="middle">read: slot(i) = (2 + i) mod 3</text>
  <path d="M 502.2 107.0 A 58.0 58.0 0 0 0 401.8 107.0 L 426.0 121.0 A 30.0 30.0 0 0 1 478.0 121.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.06"/>
  <text x="452" y="96" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
  <text x="452" y="50" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">slot 0</text>
  <text x="452" y="63" font-size="10" fill="currentColor" text-anchor="middle" font-weight="bold">i = 1</text>
  <path d="M 452.0 194.0 A 58.0 58.0 0 0 0 502.2 107.0 L 478.0 121.0 A 30.0 30.0 0 0 1 452.0 166.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.06"/>
  <text x="490.1" y="162" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="512.6" y="181" font-size="10" fill="currentColor" fill-opacity="0.85">slot 1</text>
  <text x="512.6" y="194" font-size="10" fill="currentColor" font-weight="bold">i = 2</text>
  <path d="M 401.8 107.0 A 58.0 58.0 0 0 0 452.0 194.0 L 452.0 166.0 A 30.0 30.0 0 0 1 426.0 121.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.2"/>
  <text x="413.9" y="162" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.3</text>
  <text x="391.4" y="181" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.85">slot 2</text>
  <text x="391.4" y="194" font-size="10" fill="currentColor" text-anchor="end" font-weight="bold">i = 0</text>
  <path d="M 433 144.9 A 21 21 0 1 1 471 144.9" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aicRb)"/>
  <text x="8" y="256" font-size="11" fill="currentColor">▲ head after the push: the oldest sample; a push into a full buffer overwrites it</text>
</svg>

```cpp
#include <array>
#include <cassert>
#include <cstddef>

template <typename T, std::size_t N>
class RingBuffer {
public:
    void push(const T& value) noexcept {            // O(1); overwrites the oldest sample when full
        data_[(head_ + size_) % N] = value;
        if (size_ < N) ++size_;
        else head_ = (head_ + 1) % N;
    }
    std::size_t size() const noexcept { return size_; }
    const T& operator[](std::size_t i) const noexcept { return data_[(head_ + i) % N]; }  // 0 = oldest
private:
    std::array<T, N> data_{};                       // storage lives inside the object: no heap
    std::size_t head_ = 0;                          // index of the oldest sample
    std::size_t size_ = 0;
};

int main() {
    RingBuffer<double, 3> torque_nm;
    for (double sample : {0.1, 0.2, 0.3, 0.4, 0.5}) torque_nm.push(sample);
    assert(torque_nm.size() == 3);
    assert(torque_nm[0] == 0.3 && torque_nm[2] == 0.5);
}
```

### 7. Talking about complexity and trade-offs

"Can you do better?" is rarely a request for a cleverer trick. It asks whether you know where your solution stands: against a lower bound, and against the other resources you could spend. State the complexity first in the five-part form of [[02-foundations/algorithms/complexity-recursion|11.1 §7]], then work through the following.

1. **Ask what "better" means.** Faster in the worst case, less memory, fewer passes over a stream, or simpler to maintain? The answers differ, and asking shows you know they differ.
2. **Find the dominant term.** If sorting costs O(n log n) and everything else is O(n), only the sort is worth attacking.
3. **Check for a lower bound.** A lower bound $\Omega(g(n))$ for a *problem* says every algorithm needs at least a constant times $g(n)$ steps on some input of size $n$, for all large $n$ ([[02-foundations/algorithms/complexity-recursion|11.1 §2]] defines $O$, $\Omega$ and $\Theta$). Any algorithm must read its input, so O(n) cannot be beaten for a problem that depends on every element. Sorting by comparisons needs Ω(n log n) comparisons. Producing K answers costs at least K. If you are already at the bound, say so, and turn to constants and memory.
4. **Name the trade-off you would make.**
   - *Time against memory:* a hash set gives O(n) expected time with O(n) extra memory; sorting in place gives O(n log n) with O(1) extra memory (C++ `std::sort` on the input; Python's `list.sort` also needs up to n/2 pointers of temporary space).
   - *Preprocessing against queries:* sort once and binary-search many queries; build prefix sums once and answer range sums in O(1).
   - *Expected against worst case:* a hash table is O(1) expected but O(n) in the worst case; a balanced tree is O(log n) guaranteed and keeps order.
   - *Exact against approximate:* approximate nearest neighbours or a Bloom filter trade a small, controlled error for large savings.
   - *Batch against streaming:* a size-k heap finds the top k of a stream in O(n log k) time and O(k) memory without storing the stream.
   - *Asymptotics against constants:* an O(n²) vectorized NumPy computation can beat an O(n log n) pure-Python loop for n in the thousands. Measure before claiming.

> [!example] Worked example · 계산 예제
> **Interviewer:** "Your `longest_run` is O(n). Can you do better?"
>
> **Answer, spoken:** "Not in time: the answer depends on every element, so any algorithm has to read all n of them. Where I can do better is memory. The set costs O(n) extra space. If memory is the constraint, I sort in place and scan once, which is O(n log n) time and O(1) extra space in C++. And if frame numbers are known to lie in a range of size U that isn't much larger than n, a bit array of U bits gives O(n + U) time with U/8 bytes, which beats hashing on constants. For a stream of frames I'd ask whether you need the answer at the end only or continuously — continuously, I'd keep a map from each run's endpoints to its length and merge runs as frames arrive, which is O(1) expected per frame."
>
> The answer names the lower bound, turns to the resource that can still improve, and asks a clarifying question instead of guessing.

### How to drill this page

1. **Run the §1 routine on every problem you solve**, out loud or in comments: restate, hand example, brute force, improve, code, hand-test, complexity. For the first ten problems, time each step against the table in §1.
2. **Keep one stress-test file.** For each problem, write the brute force first and reuse `stress` and `shrink` from §2; stop only when all 3000 trials agree.
3. **Drill §3 and §4 as a lookup table.** Hide the code, read one bold entry name, predict what its snippet prints or which assertion it checks, then run it.
4. **Rewrite one function a week in the §5 style**: units in names, shapes in comments, one assertion for an invariant, a seeded generator.
5. **Answer "can you do better?" aloud** for every solution with the four moves of §7, and only then read §7's worked example.

### Self-check

1. A problem says n ≤ 2 × 10⁵ and values up to 10⁹, and asks for the sum of the products of all pairs. Before designing anything, what two things do these constraints tell you in C++?
2. Your stress test reports a failure on a 40-element input with values up to 10⁶. What do you change before you start debugging, and why?
3. What does `rows = [ [0] * 2 ] * 2; rows[0][1] = 5; print(rows)` print, and how do you fix it?
4. Give `-7 // 2` and `-7 % 2` in Python and `-7 / 2` and `-7 % 2` in C++. How do you get a non-negative remainder in C++?
5. A teammate sorts with `std::sort(v.begin(), v.end(), [](const Item& a, const Item& b) { return a.cost <= b.cost; });`. It passed their tests. What is wrong, and what is the fix?
6. Why can `std::lower_bound(s.begin(), s.end(), x)` be slow when `s` is a `std::set`, and what should you write instead?
7. In `wrap_to_pi` (§5), the first version asserted `-math.pi <= wrapped < math.pi`. A stress test with random angles near −π failed it. Why, and was loosening the assertion the right response?
8. A 1 kHz controller appends every sample to a `std::vector` and prints a status line with `std::cout << ... << std::endl` each cycle. It usually meets its deadline but misses one every few seconds. Name two causes and their fixes.
9. You wrote `k_closest` with a size-k heap in O(n log k). The interviewer asks "can you do better?". Give a faster expected-time method and one reason you might still keep the heap.

> [!tip]- Answers
> 1. First, the target complexity: n = 2 × 10⁵ rules out O(n²) (4 × 10¹⁰ steps) and points to O(n log n) or O(n) — here the sum over pairs is ((Σx)² − Σx²)/2, computable in O(n). Second, the types: a single product reaches 10¹⁸, and the sum over about 2 × 10¹⁰ pairs goes far beyond the range of `long long` (about 9.2 × 10¹⁸), so ask whether the answer is taken modulo something or needs 128-bit or big-integer arithmetic; `int` is wrong even for a single product.
> 2. Shrink the input size and the value range (say, n ≤ 8 and values in −3…3), keep the random seed fixed, and shrink the failing input by deleting elements while it still fails. Small inputs with narrow ranges make repeats and ties likely and give a counterexample you can trace by hand; a fixed seed makes every run reproduce the same failure.
> 3. It prints `[ [0, 5], [0, 5] ]` (without the space after the first bracket), because both entries refer to the same inner list. Build independent rows: `[ [0] * 2 for _ in range(2)]`.
> 4. Python: `-4` and `1` (floor toward minus infinity; the remainder has the sign of the divisor). C++: `-3` and `-1` (truncation toward zero; the remainder has the sign of the dividend). Non-negative remainder in C++: `((a % m) + m) % m` for positive `m`.
> 5. `<=` returns true for equal elements, so `comp(a, a)` is true, which violates the strict weak ordering that `std::sort` requires. The behaviour is undefined: it often works on small tests with few ties and then produces wrong orders, crashes or reads out of bounds on real data with many equal costs. Use `a.cost < b.cost` (and make sure no cost is NaN).
> 6. `std::set` iterators are bidirectional, not random access. `std::lower_bound` still makes only O(log n) comparisons, but moving to the middle of a range means stepping node by node, so the time is O(n). Use the member function `s.lower_bound(x)`, which walks the tree in O(log n).
> 7. For an angle just below −π, `angle + pi` is a tiny negative number, and Python's `%` returns a result with the sign of the divisor; the exact result 2π − ε is not representable and rounds to exactly 2π, so `wrapped` equals π. The assertion was right to fire: it exposed an assumption (a half-open interval) that floating-point arithmetic does not guarantee. The right response is a decision, not a reflex: either accept the closed interval [−π, π] and document it (as §5 does), or map π to −π explicitly if downstream code relies on the half-open range. Deleting the assertion would have been the wrong response.
> 8. First, `push_back` occasionally exceeds the capacity and reallocates, copying the whole vector — a spike that grows with run time. Preallocate, or keep a fixed-size ring buffer (§6) and hand samples to a logging thread. Second, `std::endl` flushes, and formatting and writing to a terminal can allocate and block. Remove output from the loop; record a status in a preallocated structure and print it from a non-real-time thread.
> 9. Quickselect (`std::nth_element` in C++) partitions around the k-th smallest distance in O(n) expected time, after which the first k elements are the answer; sorting those k adds O(k log k). Reasons to keep the heap: it works on a stream without storing all n points (O(k) memory), it has a guaranteed O(n log k) worst case, and for small k, log k is a small constant anyway.

### Problem set · 과제

One extra, not a rewrite of the interview track. **P2** from [[02-foundations/lab-plants|0.6]] at the frozen pose. $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$, $F=(0,-10)$.

1. Write `joint_torque(F)` (Python or C++) that returns $\tau=J^\top F$ for that frozen $J$ and a length-2 force. Evaluate at $F=(0,-10)$. Units. No time loop.

> [!tip]- Solutions
> $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$, so $\tau=J^\top F=(-10,\,0)\,\mathrm{N{\cdot}m}$. Python: `tau = J.T @ F` with catalog $J$. C++: `tau[0] = -F[0] + F[1]; tau[1] = -F[0]`. The statics dual of $v=J\dot\theta$; same $J$, no inverse.

### Sources

- A. S. Kulikov, P. A. Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — chapter 3 (solving a programming challenge in stages, testing, and stress testing against a naive solution) and chapter 8 (good programming practices, language-independent and for C++ and Python). The routine, checklist and examples on this page are written independently.
- cppreference.com, *C++ reference* — containers library (`std::vector` iterator invalidation, `std::unordered_map`, `std::map`, `std::set`, `std::priority_queue`), `std::sort`, `std::stable_sort` and the *Compare* named requirement, `std::hash`, `std::accumulate`, arithmetic operators (integer division and remainder), structured binding declarations, and `std::ios_base::sync_with_stdio`.
- Python Software Foundation, *The Python Standard Library* and *The Python Language Reference* (docs.python.org, version 3.12) — `collections`, `heapq`, `bisect`, `itertools`, `functools`, `timeit`, `sys.setrecursionlimit`; the Sorting HOW-TO (stability); the tutorial chapter on floating-point arithmetic; the Programming FAQ entries on shared default arguments and multidimensional lists; binary arithmetic operations (floor division and modulo); `PYTHONHASHSEED`.
- NumPy documentation (numpy.org) — broadcasting rules, and random `Generator` / `default_rng`.
- K. Claessen, J. Hughes, "QuickCheck: a lightweight tool for random testing of Haskell programs," *Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP)*, 2000. DOI: 10.1145/351240.351266 — the origin of property-based random testing with automatic shrinking.
- ROS 2 design article — *Introduction to Real-time Systems* (design.ros2.org) — why real-time code avoids dynamic allocation, blocking synchronisation and unbounded operations in the control loop.

## 한국어

*알고리즘 트랙의 기술(craft) 페이지다. 다른 페이지들이 무엇을 계산할지 가르친다면, 이 페이지는 로보틱스 인터뷰가 쓰는 두 언어로 45분 안에 올바른 코드를 손으로 뽑아내는 법을 가르친다.*

코딩 인터뷰에서 알맞은 알고리즘을 아는 것은 절반쯤이다. 나머지 절반은 겉으로 보이는 과정이다. 가정하기 전에 묻는가, 올바른 것에서 출발하는가, 코드가 처음부터 돌아가는가, 면접관이 짚기 전에 스스로 버그를 찾는가. 연구실 인터뷰는 세 번째 질문을 더한다. 이 사람의 코드를 우리 저장소에서 읽고 싶은가? 이 페이지는 셋을 모두 다룬다. 따라가며 소리 내어 말할 절차(§1), 버그를 일찍 잡는 테스트 습관(§2), 압박 속에서 사람을 넘어뜨리는 Python과 C++의 부분들(§3, §4), 수치 코드와 연구 코드를 읽기 쉽게 만드는 습관(§5), 제어 루프 안에서 달라지는 규칙(§6), 그리고 "더 잘할 수 있나요?"에 답하는 법(§7)이다.

> [!note] 처음이라면 · First pass
> §1과 §2를 먼저 읽고, 앞으로 푸는 모든 문제에서 연습하라. 그다음 인터뷰에서 쓸 언어의 절(§3 또는 §4)을 읽어라. 이 두 절은 형식이 바뀐다. 하나의 풀이 이야기가 아니라 서로 독립인 함정들을 모은 참조표이므로, 한 번 끝까지 읽은 뒤 필요한 항목만 다시 찾아본다. §5부터 §7까지는 연구실 인터뷰에서 가장 중요하고, 스스로 점검 앞의 연습 목록이 페이지 전체를 연습 계획으로 바꿔 준다.

### 1. 45분 인터뷰를 위한 풀이 절차

프로그래밍 문제는 정해진 순서로 푼다. 문제와 그 제한을 이해하고, 알고리즘을 설계해 옳다고 스스로 납득하고, 구현한 다음, 테스트하고 디버깅한다. Kulikov와 Pevzner는 책 전체를 이 순서 위에 짠다. 인터뷰는 요구를 하나 더한다. 각 단계를 **소리 내어** 해야 한다. 면접관은 들을 수 있는 추론을 채점하지, 들리지 않는 생각을 채점하지 않기 때문이다. 침묵은 막혔다는 뜻으로 읽힌다.

| 단계 | 하는 일 | 대략의 시간 |
|---|---|---|
| 1. 다시 말하고 묻기 | 문제를 자기 말로 되풀이하고, 크기·값의 범위·경계 사례를 묻는다 | 3–5분 |
| 2. 손으로 작은 예제 | 입력 하나를 화이트보드나 주석에서 출력까지 풀어 본다 | 2–3분 |
| 3. 무차별 대입부터 | 명백히 옳은 방법과 그 복잡도를 설명한다 | 2–3분 |
| 4. 개선 | 반복되거나 낭비되는 일을 찾아 없앤다 | 5–10분 |
| 5. 코드 | 고른 방법을 깔끔한 코드로 쓴다 | 10–15분 |
| 6. 손으로 테스트 | 작은 예제와 경계 사례를 코드에 따라 추적한다 | 5분 |
| 7. 복잡도 말하기 | 시간과 공간, 어떤 경우인지까지 | 1–2분 |

시간은 대략의 기준이다. 중요한 것은 순서이고, 6단계를 건너뛰지 않는 것이다.

**예제 문제.** 카메라 드라이버가 프레임 번호를 순서 없이, 가끔은 두 번씩 보낸다. 도착한 프레임 번호 중 연속된 가장 긴 블록의 길이를 보고하라. `[12, 10, 11, 11, 20, 13]`이면 답은 4다(프레임 10부터 13까지).

**1단계 — 다시 말하고 묻기.** 다시 말하면 오독이 10분을 잡아먹기 전에 드러난다. 그다음 답에 따라 코드가 달라지는 질문을 한다.

- *크기와 범위.* 수가 몇 개이고, 얼마나 큰가? 이것이 복잡도 목표를 정하고([[02-foundations/algorithms/complexity-recursion|11.1 §1]]의 시간 예산을 쓴다), C++에서는 정수 타입을 정한다.
- *경계 사례.* 입력이 비어 있을 수 있는가? 값이 반복되거나 음수일 수 있는가?
- *출력.* 길이만인가, 블록 자체인가? 여러 블록이 같으면 어느 것인가?
- *자유도.* 입력을 수정해도 되는가? 메모리 제한이 있는가?

> **이렇게 말한다:** "그러니까 반복이 섞인 정렬 안 된 프레임 번호 리스트를 받고, 값이 끊기지 않고 이어지는 가장 긴 구간의 길이를 반환하는 거죠. 리스트가 비어 있을 수 있나요? 그러면 0을 반환하겠습니다. 프레임은 대략 몇 개인가요, 수천 개인가요 수억 개인가요? 그리고 반복은 한 번으로 세나요?"

**2단계 — 손으로 작은 예제.** 1분 안에 끝낼 만큼 작지만 까다로운 부분 — 여기서는 반복과 빈틈 — 을 담을 만큼 큰 입력을 고른다. 손으로 풀면 답의 구조가 보이고(머릿속으로 정렬하면 10, 11, 11, 12, 13, 20) 6단계에서 쓸 테스트가 생긴다.

> **이렇게 말한다:** "정렬하면 10, 11, 11, 12, 13, 20입니다. 11의 반복은 구간을 끊지도 늘리지도 않아야 하니까 구간은 10부터 13, 길이 4입니다."

**3단계 — 무차별 대입부터.** 느리더라도 뻔히 옳은 방법을 말하고 그 비용을 말한다. 문제를 이해했다는 증거가 되고, 돌아갈 곳이 생기고, 나중에 스트레스 테스트의 기준(§2)이 된다. 여기서는 각 값에서 시작해, 다음 값이 리스트에 있는 동안 위로 센다. 소속 검사 하나가 리스트를 훑으니 O(n)이고, 걷기 한 번이 최대 n걸음이므로 최악의 경우 합계는 O(n³)이다.

> **이렇게 말한다:** "올바른 기준선은 이렇습니다. 모든 값에서 다음 수가 리스트에 있는 동안 위로 걸어갑니다. 리스트에 대한 `in`이 선형이라 O(n³)입니다. 이걸 코딩하고 싶지는 않지만, 무엇을 빠르게 해야 하는지 알려 줍니다."

**4단계 — 개선.** 반복되거나 낭비되는 일을 찾는다. 여기에는 낭비가 둘 있다. 리스트에서의 소속 검사는 선형이지만 해시 집합에서는 평균 O(1)이다. 그리고 11에서 시작한 걷기는 10에서 시작한 걷기의 대부분을 되풀이한다. 구간을 *시작하는* 값, 즉 바로 앞 값이 없는 값에서만 걸으면 된다. 그러면 각 값은 최대 한 번의 걷기에서만 지나가므로 모든 걷기를 합쳐도 O(n)걸음이다.

> **이렇게 말한다:** "값을 집합에 넣어서 소속 검사를 평균 O(1)로 만듭니다. `x - 1`이 집합에 없을 때만 `x`에서 걷기를 시작합니다. 그러면 각 값은 정확히 한 번의 걷기에 속하니까 전체 작업은 선형입니다. 정렬 후 훑어서 O(n log n)에 추가 메모리를 덜 쓰는 대안도 있는데, 그 트레이드오프는 마지막에 말하겠습니다."

<svg viewBox="0 0 560 214" style="max-width:100%;height:auto" role="img" aria-label="프레임 번호 12, 10, 11, 11, 20, 13은 수직선 위 집합 10, 11, 12, 13, 20이 된다. 9와 19가 없으므로 걷기는 10과 20에서만 시작한다. 10에서의 걷기는 11, 12, 13을 지나 없는 14에서 멈춰 길이 4, 20에서의 걷기는 길이 1이다. 11, 12, 13은 앞 값이 있으므로 건너뛴다.">
  <defs><marker id="aicRunk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="8" y="20" font-size="12" fill="currentColor">입력 [12, 10, 11, 11, 20, 13] → 집합 {10, 11, 12, 13, 20}</text>
  <line x1="28.8" y1="88" x2="515.2" y2="88" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <text x="44" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">9</text>
  <circle cx="82" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="82" y="110" font-size="11" fill="currentColor" text-anchor="middle">10</text>
  <circle cx="120" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="120" y="110" font-size="11" fill="currentColor" text-anchor="middle">11</text>
  <circle cx="158" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="158" y="110" font-size="11" fill="currentColor" text-anchor="middle">12</text>
  <circle cx="196" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="196" y="110" font-size="11" fill="currentColor" text-anchor="middle">13</text>
  <text x="234" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">14</text>
  <line x1="272" y1="84" x2="272" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="272" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">15</text>
  <line x1="310" y1="84" x2="310" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="310" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">16</text>
  <line x1="348" y1="84" x2="348" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="348" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">17</text>
  <line x1="386" y1="84" x2="386" y2="92" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <text x="386" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">18</text>
  <text x="424" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">19</text>
  <circle cx="462" cy="88" r="6.5" stroke="none" fill="currentColor"/>
  <text x="462" y="110" font-size="11" fill="currentColor" text-anchor="middle">20</text>
  <text x="500" y="110" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.6">21</text>
  <text x="82" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85" font-weight="bold">시작</text>
  <text x="120" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">건너뜀</text>
  <text x="158" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">건너뜀</text>
  <text x="196" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">건너뜀</text>
  <text x="462" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85" font-weight="bold">시작</text>
  <path d="M 82 80 A 19 19 0 0 1 120 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRunk)"/>
  <path d="M 120 80 A 19 19 0 0 1 158 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRunk)"/>
  <path d="M 158 80 A 19 19 0 0 1 196 80" stroke="currentColor" stroke-width="1.4" fill="none" marker-end="url(#aicRunk)"/>
  <path d="M 196 80 A 19 19 0 0 1 234 80" stroke="currentColor" stroke-width="1.4" fill="none" stroke-opacity="0.6" stroke-dasharray="3 2" marker-end="url(#aicRunk)"/>
  <circle cx="44" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="44" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">없음</text>
  <circle cx="234" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="234" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">없음</text>
  <circle cx="424" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="424" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">없음</text>
  <circle cx="500" cy="88" r="6.5" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.0" stroke-opacity="0.8" stroke-dasharray="2 2"/>
  <text x="500" y="126" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.65">없음</text>
  <text x="8" y="162" font-size="11" fill="currentColor">10에서 걷기: 11, 12, 13 있음, 14 없음 → 길이 4</text>
  <text x="8" y="182" font-size="11" fill="currentColor">20에서 걷기: 21 없음 → 길이 1; 최댓값 = 4</text>
  <text x="8" y="202" font-size="11" fill="currentColor" fill-opacity="0.85">각 값은 많아야 한 번의 걷기에서만 밟히므로 모든 걷기를 합쳐도 O(n)</text>
</svg>

**5단계 — 코드.** 의미대로 이름을 짓고, 함수를 작게 유지하고, 쓰면서 각 블록이 하는 일을 말한다.

```python
def longest_run(nums):
    """Length of the longest block of consecutive integers in nums (repeats count once)."""
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:            # not the start of a run: its start will count it
            continue
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best

assert longest_run([12, 10, 11, 11, 20, 13]) == 4
assert longest_run([]) == 0
assert longest_run([5]) == 1
assert longest_run([-2, -1, 0, 7]) == 3
assert longest_run([3, 3, 3]) == 1
```

**6단계 — 손으로 테스트.** 예제를 코드에 따라 돌려라. 코드에 대한 머릿속 생각에 따라서가 아니다. 그다음 §2의 경계 사례를 돌린다. 대부분의 지원자가 여기서 점수를 잃는다. 코드를 다 쓰자마자 끝났다고 선언하기 때문이다.

> **이렇게 말한다:** "집합은 {10, 11, 12, 13, 20}입니다. 10에서는 9가 없으니 걷습니다. 11, 12, 13이 있고 14가 없으니 길이 4. 11, 12, 13에서는 앞 값이 있으니 건너뜁니다. 20에서는 19가 없으니 길이 1. 최댓값은 4입니다. 빈 입력이면 루프가 돌지 않고 0을 반환합니다. 원소 하나면 길이 1입니다."

**7단계 — 복잡도 말하기.** 크기, 경우, 공간을 말한다(다섯 부분으로 된 완전한 답은 [[02-foundations/algorithms/complexity-recursion|11.1 §7]]에 있다).

> **이렇게 말한다:** "기대 시간 O(n)입니다. 집합 연산이 평균 O(1)이고 각 값은 최대 한 번의 걷기에서만 방문되기 때문입니다. 해시가 퇴화하는 최악의 경우는 O(n²)입니다. 추가 공간은 집합에 O(n)입니다."

**막혔을 때.** 무엇을 시도하고 있고 왜 안 되는지 말하라("힙은 최솟값을 주지만, 저는 임의의 값의 후속자가 필요합니다"). 표준적인 수를 차례로 대 보라. 먼저 정렬하기, 해시 맵, 투 포인터, 힙, 답에 대한 이진 탐색, 그래프로 보기. 힌트를 요청하는 것이 조용한 5분보다 싸다.

### 2. 엔지니어처럼 테스트하기

옳아 보이는 프로그램은 옳은 프로그램이라는 증거가 아니다. 점점 강해지는 세 가지 습관이 남보다 먼저 버그를 찾는다.

**손으로 추적하기.** 논리를 모두 거치는 가장 작은 입력을 골라, 반복 한 번에 한 행씩 모든 변수를 작은 표에 적는다. 요점은 코드를 *쓰인 그대로* 실행하는 것이다. 한 칸 어긋남(off-by-one)은 "그리고 끝에 도달한다"고 생각할 때가 아니라, 마지막 반복에서 `i`의 실제 값을 적을 때 드러난다.

> [!example] 계산 예제 · Worked example
> `longest_run([4, 2, 3, 2])`를 추적한다. 집합은 {2, 3, 4}다(실제 실행의 순회 순서는 다를 수 있지만 결과는 같다).
>
> | `x` | `x - 1`이 집합에? | 걷기 | `length` | `best` |
> |---|---|---|---|---|
> | 2 | 아니오 | 3 있음, 4 있음, 5 없음 | 3 | 3 |
> | 3 | 예 | 건너뜀 | — | 3 |
> | 4 | 예 | 건너뜀 | — | 3 |
>
> 결과는 3이다. 반복된 2는 집합을 만들 때 사라졌다. 바로 그래서 이 버전은 중복을 처리하고, 원래 리스트 위에서 동작하는 버전은 못 할 수도 있다.

**경계 사례 체크리스트.** 모든 문제에서 이 목록을 훑어라. 대부분 몇 초면 확인되고, 하나하나가 전형적인 버그를 잡는다.

| 사례 | 예 | 잡아내는 것 |
|---|---|---|
| 빈 입력 | `[]`, `""`, 간선 없는 그래프 | `nums[0]` 인덱싱, 빈 시퀀스의 `max()`, 빠진 기저 사례 |
| 원소 하나 | `[7]` | 한 번도 돌지 않는 쌍 루프, 잘못 초기화된 `best` |
| 중복 | `[2, 2, 2]` | 값이 서로 다르다고 가정하는 논리, `>` 대 `>=` |
| 음수와 0 | `[-3, 0, 2]` | 0으로 초기화된 "최댓값", 음수의 나머지(§3, §4) |
| 오버플로 | C++에서 10⁹짜리 값 10⁵개의 합 | `long long` 대신 `int`에 담은 합이나 곱 |
| 이미 정렬됨, 역순 정렬됨 | `[1, 2, 3, 4]`, `[4, 3, 2, 1]` | 이차로 떨어지는 피벗 선택, 한 번도 발동하지 않는 조기 종료 |
| 최대 크기 | 명시된 한계의 n | 숨은 O(n²), 재귀 깊이, 메모리 |

문제별 사례를 더하라. 그래프면 연결되지 않은 그래프와 자기 루프, 문자열이면 한 글자의 반복, 기하면 일직선이거나 겹치는 점, 구간이면 끝점에서 맞닿는 구간.

**스트레스 테스트.** 손 테스트는 생각해 낸 버그만 찾는다. 스트레스 테스트는 생각하지 못한 버그를 찾는다. 네 부분으로 이루어진다. 믿고 싶은 빠른 해법, 뻔히 옳을 만큼 단순한 느린 기준 해법(3단계의 무차별 대입), 작은 무작위 입력 생성기, 그리고 각 입력에 둘을 돌려 처음 어긋나는 곳에서 멈추는 루프다. 독립적인 두 프로그램이 같은 버그를 공유하는 일은 드물기 때문에, 어긋남은 둘 중 하나를 가리킨다. 두 가지 다듬기가 훨씬 쓸모 있게 만든다. 첫째, 입력은 작게, 값의 범위는 좁게 유지한다. 그래야 반복, 0, 동점이 실제로 생긴다. 둘째, 디버깅하기 전에 실패한 입력을 줄인다. 원소 네 개짜리 반례는 읽히지만 마흔 개짜리는 읽히지 않는다.

아래 하네스는 `longest_run`의 정렬 기반 버전을 테스트한다. 옳아 보이고 `[1, 2, 3]`, `[5, 9]`, `[]`를 통과하지만, 하네스가 1초도 안 되어 찾아내는 버그가 있다.

```python
import random

def longest_run_slow(nums):
    """Reference: obviously correct, far too slow for large inputs."""
    best = 0
    for start in nums:
        length = 0
        while start + length in nums:              # linear scan of the list each time
            length += 1
        best = max(best, length)
    return best

def longest_run_sorted(nums):
    """Candidate: sort, then count steps of +1 between neighbours."""
    if not nums:
        return 0
    xs = sorted(nums)
    best = run = 1
    for prev, cur in zip(xs, xs[1:]):
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    return best

def longest_run_sorted_fixed(nums):
    if not nums:
        return 0
    xs = sorted(nums)
    best = run = 1
    for prev, cur in zip(xs, xs[1:]):
        if cur == prev:
            continue                               # a repeat neither extends nor breaks a run
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    return best

def shrink(nums, fails):
    """Delete elements one at a time while the input still fails."""
    i = 0
    while i < len(nums):
        smaller = nums[:i] + nums[i + 1:]
        if fails(smaller):
            nums = smaller
        else:
            i += 1
    return nums

def stress(fast, slow, trials=3000, seed=0):
    rng = random.Random(seed)                      # fixed seed: a failure can be replayed
    for trial in range(trials):
        n = rng.randint(0, 2 + trial // 100)       # start tiny, grow slowly
        nums = [rng.randint(-3, 3) for _ in range(n)]
        if fast(nums) != slow(nums):
            small = shrink(nums, lambda xs: fast(xs) != slow(xs))
            return small, slow(small), fast(small)
    return None                                    # no disagreement found

print(stress(longest_run_sorted, longest_run_slow))       # ([1, -1, 0, 0], 3, 2)
assert stress(longest_run_sorted_fixed, longest_run_slow) is None
```

하네스는 `[1, -1, 0, 0]`에서 기준 해법이 3, 후보가 2라고 알린다. 원소를 하나라도 지우면 실패가 사라지기 때문에 줄이기는 네 원소에서 멈췄고, 네 원소면 버그가 한눈에 보인다. 정렬하면 −1, 0, 0, 1이다. −1에서 0으로 가는 걸음이 길이 2의 구간을 만든다. 반복된 0은 이웃과 1이 아니라 0만큼 차이 나므로 구간이 1로 초기화된다. 그래서 0에서 1로 가는 걸음은 2에만 이른다. 반복은 구간을 늘리지도 끊지도 않아야 하므로, 고친 버전은 같은 값의 이웃을 건너뛴다. 고친 뒤 같은 시드로 3000번의 시도가 어긋남 없이 끝난다. 그다음 더 큰 `n`과 더 넓은 값 범위로 다시 돌린다.

이 방법의 한계를 알아 두라. 올바른 출력이 여러 개인 문제(아무 최단 경로, 아무 유효한 순서)라면 정확한 답과 비교하지 말고 출력의 성질을 검증하는 *검사기*와 비교한다. 공유되는 코드의 버그 — 입력 파서, 또는 빈 리스트를 한 번도 만들지 않는 생성기 — 는 보이지 않는다. 그리고 느린 해법이 감당하는 크기만 테스트하므로, 시간 확인용으로 최대 크기 입력 하나는 여전히 돌려야 한다. Python의 Hypothesis 같은 속성 기반 테스트 라이브러리가 생성과 줄이기를 자동화해 주지만, 인터뷰가 확인하는 것은 열다섯 줄짜리 버전을 직접 쓸 줄 아는가다.

### 3. 인터뷰를 위한 Python

*여기서부터 페이지의 형식이 바뀐다. §3과 §4는 참조표다. 굵은 글씨로 시작하는 항목 하나가 실행 가능한 확인 코드를 가진 독립된 함정 하나이고, 어떤 항목도 앞 항목에 기대지 않는다. 한 번 끝까지 읽은 뒤, 면접 전에는 필요한 항목만 다시 찾아본다.*

표준 라이브러리와 그 비용을 알면, Python으로는 C++의 절반 줄 수로 인터뷰 답을 쓸 수 있다. 환경의 Python 버전을 물어보라. 아래 도구 몇 개는 3.9나 3.10이 필요하다.

| 필요한 것 | 도구 | 비용 |
|---|---|---|
| 큐, 슬라이딩 윈도 | `collections.deque` | 양 끝 append와 pop O(1) |
| 개수 세기 | `collections.Counter` | 갱신당 평균 O(1) |
| 기본값이 있는 맵 | `collections.defaultdict` | 평균 O(1) |
| 반복되는 최솟값, top-k | 리스트 위의 `heapq` | push와 pop O(log n), `heapify` O(n) |
| 정렬된 리스트에서 탐색 | `bisect` | 탐색 O(log n); `insort`는 원소를 밀어내므로 O(n) |
| 누적 합, 쌍, 곱집합 | `itertools` | 지연 평가, 한 걸음에 O(1) 메모리 |
| 메모이제이션 재귀 | `functools.cache` | 서로 다른 인자 튜플마다 딕셔너리 항목 하나 |

"비용" 열은 트랙의 다른 곳에서 정의한, 뜻이 정확한 두 낱말을 쓴다. 해시 기반 컨테이너의 평균 O(1)(**average O(1)**)은 키가 버킷에 고르게 퍼질 때 연산 하나의 *기대* 비용이지, 모든 연산에 대한 보장이 아니다([[02-foundations/algorithms/data-structures|11.2 §3]]). 아래 `append`와 `push_back`에 쓰는 분할상환 O(1)(**amortised O(1)**)은 연산의 열에 대한 보장이다. 빈 구조에서 시작한 임의의 연산 $k$개는 모두 합쳐 $k$의 상수배 이하의 비용이 들므로, 비싼 크기 조정 한 번은 그 앞의 많은 싼 append가 갚는다([[02-foundations/algorithms/complexity-recursion|11.1 §4]]).

**collections.** `Counter`는 없는 키를 넣지 않고 0으로 읽는다. `defaultdict(list)`는 처음 접근할 때 없는 항목을 만든다. `deque(maxlen=k)`는 바로 쓸 수 있는 고정 크기 윈도다.

```python
from collections import Counter, defaultdict, deque

words = "the robot saw the wall and the door".split()
counts = Counter(words)
assert counts["the"] == 3 and counts["window"] == 0     # missing key reads as 0
assert "window" not in counts                            # ...and was not inserted
assert counts.most_common(1) == [("the", 3)]

by_length = defaultdict(list)                            # missing key starts as list()
for word in words:
    by_length[len(word)].append(word)
assert by_length[4] == ["wall", "door"]

recent = deque(maxlen=3)                                 # oldest item falls off the left
for reading in [5, 6, 7, 8]:
    recent.append(reading)
assert list(recent) == [6, 7, 8]
assert recent.popleft() == 6                             # O(1); list.pop(0) is O(n)
```

**heapq.** 평범한 리스트에 저장된 최소 힙이다. 자식이 있는 모든 인덱스에서 리스트가 `a[i] <= a[2*i + 1]`과 `a[i] <= a[2*i + 2]`를 만족하므로 `a[0]`이 항상 가장 작다(힙의 정의와 비용 증명은 [[02-foundations/algorithms/data-structures|11.2 §4]]). 최대 힙이 필요하면 키를 음수로 바꿔 넣는다. a > b일 때에만 −a < −b이므로, 음수로 바꾼 키 중 가장 작은 것이 원래 가장 큰 키다(Python 3.14에서 `heappush_max` 등의 함수가 추가되었지만, 인터뷰 환경은 더 오래된 버전인 경우가 많다). 항목은 보통 원소별로 비교되는 튜플이므로, 비교할 수 없는 데이터 앞에는 카운터를 넣어라.

```python
import heapq
from itertools import count

def k_closest(points, k):
    """The k points nearest the origin, in O(n log k) time and O(k) memory."""
    heap = []                                   # (-squared distance, x, y): root is the farthest kept
    for x, y in points:
        d2 = x * x + y * y                      # squared distances: exact integers, no sqrt
        if len(heap) < k:
            heapq.heappush(heap, (-d2, x, y))
        elif d2 < -heap[0][0]:
            heapq.heapreplace(heap, (-d2, x, y))
    return sorted((x, y) for _, x, y in heap)

assert k_closest([(3, 3), (1, 0), (-2, 2), (0, -1), (5, 1)], 2) == [(0, -1), (1, 0)]

order = count()                                 # tie-breaker: dicts cannot be compared
tasks = []
heapq.heappush(tasks, (1, next(order), {"name": "scan"}))
heapq.heappush(tasks, (1, next(order), {"name": "grasp"}))
assert heapq.heappop(tasks)[2]["name"] == "scan"
assert heapq.nsmallest(2, [7, 1, 5, 3]) == [1, 3]
```

**bisect.** `bisect_left(a, x)`는 값이 `x` 이상인 첫 인덱스이고, `bisect_right(a, x)`는 값이 `x`보다 큰 첫 인덱스다. 둘을 함께 쓰면 정렬된 리스트에서 범위를 잘라 낼 수 있다. 메시지를 가장 가까운 센서 타임스탬프에 맞추는 방법이 이것이다.

```python
from bisect import bisect_left, bisect_right

stamps = [0.0, 0.1, 0.1, 0.2, 0.35, 0.5]                # sorted timestamps, seconds
lo, hi = bisect_left(stamps, 0.1), bisect_right(stamps, 0.35)
assert stamps[lo:hi] == [0.1, 0.1, 0.2, 0.35]            # every sample with 0.1 <= t <= 0.35

def nearest_index(sorted_values, target):
    """Index of the value closest to target; ties go to the earlier value."""
    i = bisect_left(sorted_values, target)
    if i == 0:
        return 0
    if i == len(sorted_values):
        return i - 1
    before, after = sorted_values[i - 1], sorted_values[i]
    return i - 1 if target - before <= after - target else i

assert nearest_index(stamps, 0.27) == 3
assert nearest_index(stamps, -1.0) == 0 and nearest_index(stamps, 9.0) == 5

scans = [(0.05, "a"), (0.3, "b")]                        # key= needs Python 3.10+
assert bisect_left(scans, 0.3, key=lambda scan: scan[0]) == 1
```

**itertools와 functools.cache.** `accumulate`는 누적 합을, `pairwise`는 이웃 쌍을 만들고, `combinations`와 `product`는 작은 탐색 공간을 열거한다. `@cache`는 재귀 함수를 메모이제이션한다. 인자는 해시 가능해야 하고(리스트 인자는 `TypeError`를 내므로 튜플을 넘긴다), 캐시는 함수가 살아 있는 동안 유지되므로 서로 무관한 테스트 사례 사이에서는 `cache_clear()`를 부른다.

```python
from functools import cache
from itertools import accumulate, combinations, pairwise, product

readings = [3, 1, 4, 1, 5]
prefix = [0, *accumulate(readings)]                      # prefix[i] = sum(readings[:i])
assert prefix[4] - prefix[1] == 1 + 4 + 1                # any range sum in O(1)
assert [b - a for a, b in pairwise(readings)] == [-2, 3, -3, 4]   # Python 3.10+
assert len(list(combinations(range(5), 2))) == 10        # unordered pairs
assert len(list(product([0, 1], repeat=3))) == 8         # every 3-bit pattern

@cache                                                   # Python 3.9+; before: lru_cache(maxsize=None)
def ways(steps):
    """Ways to climb a staircase taking 1 or 2 steps at a time."""
    if steps <= 1:
        return 1
    return ways(steps - 1) + ways(steps - 2)

assert ways(80) == 37889062373143906
```

**정확성 함정.** 아래 하나하나는 돌아가면서 틀린 답을 내는 코드를 만든다. 인터뷰에서 가장 나쁜 종류의 버그다.

- **변경 가능한 기본 인자.** 기본값은 `def`가 실행될 때 한 번 평가되므로, 기본 리스트는 모든 호출이 공유한다.
- **별칭이 된 행.** `[ [0] * m ] * n`은 *하나의* 행을 가리키는 참조 n개의 리스트를 만든다. 행은 컴프리헨션으로 만들어라.
- **정수 나눗셈과 음수.** `//`는 음의 무한대 쪽으로 내림하고 `%`는 나누는 수의 부호를 따른다. `-7 // 2`는 `-4`, `-7 % 2`는 `1`이다. C++와 Java는 `-3`과 `-1`을 준다. `int(a / b)`는 0 쪽으로 자르지만 float을 거치므로 큰 정수에서 틀린다. 정확히 말하면 두 언어 모두 $a$를 $b \ne 0$으로 나눈 몫 $q$와 나머지 $r$을 같은 항등식으로 정의하고, $q$를 어떻게 반올림하느냐만 다르다. 그래서 나머지의 부호는 $q$의 선택에서 따라 나온다.
$$a = b\,q + r, \qquad q_{\text{Python}} = \lfloor a / b \rfloor, \qquad q_{\text{C++}} = \operatorname{trunc}(a / b)$$
  Python의 내림은 $b > 0$일 때 $0 \le r < b$를 주고, C++의 0 쪽 자르기는 $r$에 $a$의 부호를 준다. $a = -7$, $b = 2$로 확인하면 Python은 $q = -4$, $r = -7 - 2(-4) = 1$이고, C++는 $q = -3$, $r = -7 - 2(-3) = -1$이다.
- **재귀 한계.** CPython은 기본적으로 약 1000 프레임에서 멈춘다. 해법은 [[02-foundations/algorithms/complexity-recursion|11.1 §5]]를 보라.
- **부동소수점 비교.** `0.1 + 0.2 == 0.3`은 거짓이다. `math.isclose`로 비교하거나, 제곱한 정수 거리나 교차 곱한 분수를 비교해 부동소수점을 아예 피하라.
- **`is` 대 `==`.** `is`는 두 이름이 같은 객체를 가리키는지 묻고, `==`는 값이 같은지 묻는다. `is`는 `None`과 의도한 센티널에만 써라. CPython은 작은 정수를 우연히 캐시하므로, 숫자에 `is`를 쓰면 테스트에서는 되고 실제 데이터에서는 실패하기도 한다.
- **정렬.** `list.sort`와 `sorted`는 `reverse=True`일 때를 포함해 안정성이 보장된다. 정렬이 안정적(**stable**)이라는 것은 키가 같은 원소들이 입력 순서를 유지한다는 뜻이다. $\text{key}(a) = \text{key}(b)$이고 입력에서 $a$가 $b$보다 앞서면 출력에서도 $a$가 $b$보다 앞선다. 아래 코드의 두 번 정렬이 옳은 것은 이 성질 덕분이다. 두 번째 정렬(개수 기준)이 개수가 같은 원소들 사이에서 첫 번째 정렬의 이름 순서를 그대로 두기 때문이다. 불안정 정렬이면 `("c", 2)`가 `("b", 2)`보다 앞에 올 수 있다. `key` 함수(원소마다 한 번 계산된다)나 `(-score, name)` 같은 튜플 키로 정렬하라. `functools.cmp_to_key`도 있지만 필요한 일은 드물다.

```python
import math

def add_bad(item, bucket=[]):            # one list, created when def runs
    bucket.append(item)
    return bucket

def add_good(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

assert add_bad(1) == [1] and add_bad(2) == [1, 2]        # the first call's item is still there
assert add_good(1) == [1] and add_good(2) == [2]

n, m = 2, 3
aliased = [ [0] * m ] * n
aliased[0][0] = 7
assert aliased[1][0] == 7                                # both "rows" are the same list
grid = [ [0] * m for _ in range(n)]
grid[0][0] = 7
assert grid[1][0] == 0

assert -7 // 2 == -4 and -7 % 2 == 1                     # floor toward minus infinity
def div_toward_zero(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q
assert div_toward_zero(-7, 2) == -3
assert div_toward_zero(-(10**20 + 1), 1) == -(10**20 + 1)
assert int(-(10**20 + 1) / 1) != -(10**20 + 1)           # the float route loses the last digit

assert 0.1 + 0.2 != 0.3 and math.isclose(0.1 + 0.2, 0.3)

runs = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
runs.sort(key=lambda r: r[0])                            # secondary key first...
runs.sort(key=lambda r: r[1], reverse=True)              # ...then primary; stability keeps the order
assert runs == [("b", 2), ("c", 2), ("a", 1), ("d", 1)]
assert sorted(runs, key=lambda r: (-r[1], r[0])) == runs # the same in one pass
```

**성능 함정.** 이것들은 옳은 답을 너무 느리게 내고, 선형처럼 보이는 코드 안에 숨는다.

- `list.pop(0)`과 `list.insert(0, x)`는 모든 원소를 밀어내므로 O(n)이다. `deque`를 써라.
- `x in some_list`는 선형 탐색이고, `x in some_set`은 평균 O(1)이다. 루프 안에서는 이것이 O(n²)와 O(n)의 차이다.
- 문자열은 불변이므로 루프 안의 `s += piece`는 매번 문자열 전체를 복사할 수 있다(CPython이 복사를 피할 때도 있지만 기대지 마라). 조각을 리스트에 모은 뒤 `"".join`을 한 번 하라.
- 슬라이싱은 복사한다. 재귀 안의 `nums[1:]`은 O(n)을 O(n²)로 만든다. 인덱스를 넘겨라.

```python
import timeit
from collections import deque

pieces = [str(i) for i in range(10_000)]
text = "".join(pieces)                                   # one pass over all pieces
assert text.startswith("0123")

ids_list = list(range(100_000))
ids_set = set(ids_list)
t_list = timeit.timeit(lambda: 99_999 in ids_list, number=200)
t_set = timeit.timeit(lambda: 99_999 in ids_set, number=200)
print(f"in list: {t_list:.4f} s   in set: {t_set:.6f} s")

queue_list, queue_deque = list(range(50_000)), deque(range(50_000))
t_pop0 = timeit.timeit(lambda: queue_list.pop(0), number=20_000)
t_popleft = timeit.timeit(lambda: queue_deque.popleft(), number=20_000)
print(f"list.pop(0): {t_pop0:.4f} s   deque.popleft(): {t_popleft:.4f} s")
```

노트북에서 집합 조회는 리스트 탐색보다 수천 배 빠르고, 원소 50 000개짜리 리스트의 `pop(0)`은 `popleft`보다 대략 백 배 느리다. 정확한 숫자는 중요하지 않다. 비율이 n과 함께 커진다는 것이 중요하다.

### 4. 인터뷰를 위한 C++

C++ 인터뷰는 같은 알고리즘에 더해, 언어가 지켜 주지 않는 것들을 아는지 확인한다. 오버플로, 무효화된 반복자, 그리고 어기면 오류 메시지가 아니라 정의되지 않은 동작(undefined behaviour)이 되는 계약들이다. 정의되지 않은 동작(**undefined behaviour**, UB)은 C++ 표준의 한 범주로, 정의하는 부분이 둘이다. (1) 프로그램이 표준이 *아무 요구도* 하지 않는 연산을 수행한다. 부호 있는 정수 오버플로, 배열 끝을 넘어 읽기, 허공을 가리키는 반복자 역참조 같은 것이다. (2) 요구가 없으므로 컴파일러는 그 연산이 절대 일어나지 않는다고 가정하고 그 가정 위에서 최적화해도 된다. 그래서 UB는 "어떤 정해지지 않은 결과"가 아니다. 같은 코드가 디버그 빌드에서는 기대한 값을, `-O2`에서는 다른 값을 출력하거나 크래시할 수 있다. *예:* `int big = 2'000'000'000`에서 `2 * big`은 $4 \times 10^9$가 `INT_MAX` $= 2\,147\,483\,647$을 넘으므로 UB다. *반례:* 부호 없는 오버플로는 정의되어 있다. 부호 없는 산술은 $2^{\text{bits}}$를 법으로 감싸 돌기 때문이고, 빈 벡터에서 `v.size() - 1`이 UB가 아니라 거대한 수가 되는 이유가 바로 이것이다. 아래 조각은 모두 `c++ -std=c++17`로 컴파일되는 완전한 프로그램이고, 주장한 내용을 `assert`로 확인한다.

| Python 습관 | C++ 도구 | 비용 | 함정 |
|---|---|---|---|
| `list` | `std::vector` | push_back 분할상환 O(1) | 재할당이 반복자와 참조를 무효화한다 |
| `dict`, `set` | `std::unordered_map`, `std::unordered_set` | 평균 O(1), 최악 O(n) | `operator[]`가 삽입한다; `std::pair`용 해시가 없다 |
| 정렬된 컨테이너 | `std::map`, `std::set` | O(log n), 순서대로 순회 | `std::lower_bound`가 아니라 멤버 `lower_bound`를 쓴다 |
| `heapq` | `std::priority_queue` | push와 pop O(log n) | 기본이 **최대** 힙 |
| 튜플 | `std::pair`, `std::tuple`, 작은 `struct` | — | `first`와 `second`는 의미를 말해 주지 않는다 |

**컨테이너, 힙, 구조적 바인딩.** `std::priority_queue<T>`는 *가장 큰* 원소를 맨 위에 둔다. 최소 힙이 필요하면 비교자로 `std::greater<>`를 넘긴다. 구조적 바인딩(C++17)은 pair와 tuple을 이름으로 풀어 준다. `std::map`과 `std::set`에는 O(log n)인 자체 `lower_bound`가 있다. 이들의 반복자에 자유 함수 `std::lower_bound`를 쓰면 비교는 O(log n)번뿐이지만, 그 반복자는 임의 접근이 아니라 양방향이라 범위 가운데로 갈 때마다 트리를 한 노드씩 걸어가야 하므로 O(n)이다.

```cpp
#include <algorithm>
#include <cassert>
#include <functional>
#include <map>
#include <queue>
#include <set>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

int main() {
    std::vector<int> readings = {5, 1, 4, 1, 5, 9, 2, 6};

    std::unordered_map<int, int> count;
    for (int r : readings) ++count[r];              // operator[] inserts 0, then increments
    assert(count.at(5) == 2);
    assert(count.find(7) == count.end());           // look up without inserting
    assert(count[7] == 0 && count.count(7) == 1);   // operator[] just inserted key 7

    std::map<std::string, int> rate_hz = {{"lidar", 10}, {"imu", 200}};
    assert(rate_hz.begin()->first == "imu");        // iteration is in key order

    std::set<int> seen(readings.begin(), readings.end());
    assert(*seen.lower_bound(3) == 4);              // member function: O(log n)

    std::priority_queue<int> max_heap(readings.begin(), readings.end());
    assert(max_heap.top() == 9);                    // largest on top
    std::priority_queue<int, std::vector<int>, std::greater<>> min_heap(readings.begin(), readings.end());
    assert(min_heap.top() == 1);

    std::vector<std::pair<int, std::string>> jobs = {{3, "plan"}, {1, "sense"}, {2, "act"}};
    std::sort(jobs.begin(), jobs.end());            // pairs compare first, then second
    std::string order;
    for (const auto& [priority, name] : jobs) order += name + " ";
    assert(order == "sense act plan ");
}
```

**참조 대 복사, 오버플로, 나눗셈.** `for (auto x : v)`는 원소마다 복사하므로 변경은 사라지고 큰 원소는 복사된다. `for (auto& x : v)`는 제자리에서 바꾸고, `for (const auto& x : v)`는 복사 없이 읽는다. 부호 있는 정수의 오버플로는 정의되지 않은 동작이고, `int`는 약 2.1 × 10⁹까지만 담는다. 산술 *전에* 넓히고, 이진 탐색의 중간점은 `lo + (hi - lo) / 2`로 쓰고, `std::accumulate`에는 시작값 `0LL`을 줘라. 결과 타입이 그 인자의 타입이기 때문이다. 정수 나눗셈은 0 쪽으로 자르고, `size()`는 부호 없는 타입이라 빈 벡터에서 `v.size() - 1`은 거대한 수가 된다.

```cpp
#include <cassert>
#include <cstddef>
#include <numeric>
#include <vector>

int main() {
    std::vector<int> v = {1, 2, 3};
    for (auto x : v) x *= 10;                   // x is a copy: v is unchanged
    assert(v[0] == 1);
    for (auto& x : v) x *= 10;                  // x is a reference: v changes
    assert(v[0] == 10);

    int big = 2'000'000'000;                    // fits: INT_MAX is 2'147'483'647
    long long doubled = 2LL * big;              // widen first; `2 * big` overflows (undefined behaviour)
    assert(doubled == 4'000'000'000LL);

    std::vector<int> large(3, big);
    assert(std::accumulate(large.begin(), large.end(), 0LL) == 6'000'000'000LL);  // 0LL, not 0

    int lo = 1'500'000'000, hi = 2'000'000'000;
    int mid = lo + (hi - lo) / 2;               // (lo + hi) / 2 would overflow
    assert(mid == 1'750'000'000);

    assert(-7 / 2 == -3 && -7 % 2 == -1);       // truncation toward zero; Python gives -4 and 1
    int a = -7, m = 5;
    assert(((a % m) + m) % m == 3);             // a non-negative remainder

    std::vector<int> empty;
    int iterations = 0;
    for (std::size_t i = 0; i + 1 < empty.size(); ++i) ++iterations;   // not: i < empty.size() - 1
    assert(iterations == 0);
}
```

**반복자 무효화.** `push_back`이 벡터가 가진 용량보다 더 필요하면 모든 원소를 새 버퍼로 옮기고, 옛 버퍼를 가리키던 반복자, 포인터, 참조는 모두 허공을 가리킨다. 재할당하지 않으면 `end()`만 무효화된다. `erase`는 지워진 위치와 그 뒤의 반복자와 참조를 무효화한다. 안전한 패턴은 이렇다. 커지는 벡터에는 포인터 대신 *인덱스*를 보관한다. 루프 안에서는 `erase`가 반환한 반복자에서 이어 간다. 여러 원소를 지울 때는 `erase`를 반복 호출(각각 O(n))하지 말고 erase–remove 관용구(한 번의 O(n) 순회)를 쓴다. C++20은 같은 일을 하는 `std::erase_if`를 더한다.

```cpp
#include <algorithm>
#include <cassert>
#include <cstddef>
#include <vector>

int main() {
    std::vector<int> path = {10};
    std::size_t start_index = 0;                // an index survives reallocation
    // int& start = path[0];                    // a reference would dangle after the loop below
    for (int k = 0; k < 1000; ++k) path.push_back(k);
    assert(path[start_index] == 10);

    std::vector<int> ids = {1, 2, 3, 4, 6, 7};
    for (auto it = ids.begin(); it != ids.end();) {
        if (*it % 2 == 0) it = ids.erase(it);   // erase returns the next valid iterator
        else ++it;
    }
    assert((ids == std::vector<int>{1, 3, 7}));

    std::vector<int> ids2 = {1, 2, 3, 4, 6, 7};
    ids2.erase(std::remove_if(ids2.begin(), ids2.end(), [](int x) { return x % 2 == 0; }), ids2.end());
    assert((ids2 == std::vector<int>{1, 3, 7}));
}
```

**`unordered_map`: 최악의 경우와 사용자 정의 해시.** 평균 O(1)은 키가 버킷에 고르게 퍼진다는 가정이다. 많은 키가 같은 버킷에 떨어지면 — 구조가 있는 키에 약한 해시를 썼거나, 알려진 해시를 노린 입력이 들어오면 — 모든 연산이 O(n) 쪽으로 나빠진다. 표준 라이브러리는 `std::pair`용 `std::hash`를 제공하지 않으므로, 격자 칸 키에는 해시를 직접 만들어야 한다. 두 좌표를 64비트 값 하나로 합치고 비트를 섞는다(아래는 SplitMix64 생성기의 마무리 함수). 곱셈·xor·시프트 단계가 입력 비트 하나가 출력 비트의 절반가량을 바꾸게 하므로, 원래 키가 한 비트만 다른 `{0, 0}`과 `{0, 1}` 같은 이웃 칸이 인접한 버킷에 몰리지 않고 서로 무관한 버킷으로 흩어진다. 입력이 적대적일 수 있으면 실행마다 무작위 오프셋을 키에 더하는 프로그래머도 있지만, 연구 코드에서는 보통 재현성이 더 중요하다. 큰 삽입 루프 전에는 `reserve`를 불러 반복적인 재해싱을 피하라. 재해싱은 반복자도 무효화한다(원소에 대한 참조는 아니다).

```cpp
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <unordered_map>
#include <unordered_set>
#include <utility>

struct CellHash {
    std::size_t operator()(const std::pair<int, int>& cell) const noexcept {
        std::uint64_t key = (static_cast<std::uint64_t>(static_cast<std::uint32_t>(cell.first)) << 32)
                          | static_cast<std::uint32_t>(cell.second);
        key += 0x9e3779b97f4a7c15ULL;                         // SplitMix64 finalizer
        key = (key ^ (key >> 30)) * 0xbf58476d1ce4e5b9ULL;
        key = (key ^ (key >> 27)) * 0x94d049bb133111ebULL;
        return static_cast<std::size_t>(key ^ (key >> 31));
    }
};

int main() {
    std::unordered_set<std::pair<int, int>, CellHash> occupied;
    occupied.insert({-1, 2});
    occupied.insert({2, -1});                                 // swapped coordinates: a different cell
    assert(occupied.size() == 2 && occupied.count({-1, 2}) == 1);

    std::unordered_map<std::pair<int, int>, int, CellHash> hits;
    hits.reserve(1 << 12);                                    // allocate buckets once, up front
    for (int x = -30; x < 30; ++x)
        for (int y = -30; y < 30; ++y) ++hits[{x / 3, y / 3}];
    assert(hits.at({0, 0}) == 25);                            // x/3 == 0 for x in -2..2
}
```

**`std::sort`에는 엄격한 약순서(strict weak ordering)가 필요하다.** 비교자는 `<`처럼 행동해야 한다. `comp(a, a)`는 거짓이고, `comp(a, b)`이면 `comp(b, a)`가 아니며, "어느 쪽도 작지 않음"까지 포함해 추이적이어야 한다. `<=`를 쓰면 첫 규칙이 깨지고, NaN이 섞인 부동소수점 키를 비교하면 마지막 규칙이 깨진다. *Compare* 요구사항의 네 조건으로 쓰면 이렇다. $a \prec b$는 `comp(a, b)`가 참이라는 뜻이고, 비교 불가능(**incomparability**) $a \sim b$는 어느 쪽도 작지 않다는 뜻이다.
$$a \sim b \iff \neg(a \prec b) \wedge \neg(b \prec a)$$

- **비반사성:** 모든 $a$에 대해 $\neg(a \prec a)$.
- **비대칭성:** $a \prec b$이면 $\neg(b \prec a)$.
- **추이성:** $a \prec b$이고 $b \prec c$이면 $a \prec c$.
- **비교 불가능성의 추이성:** $a \sim b$이고 $b \sim c$이면 $a \sim c$. 그래서 "정렬 기준으로 같음"이 원소들을 깔끔한 동치류로 묶고, 정렬은 그 동치류를 나란히 놓을 수 있다.

*반례.* `<=`는 `comp(a, a)`가 참이므로 비반사성을 어긴다. "대략 작다" 비교자 `a < b - 1`은 앞의 세 조건은 만족하지만 넷째를 어긴다. $0 \sim 0.8$이고 $0.8 \sim 1.6$인데 $0 < 0.6$이므로 $0 \prec 1.6$이다. 보통의 `<`에서 NaN은 넷째를 어긴다. NaN과의 비교는 모두 거짓이므로 $1 \prec 2$인데도 $1 \sim \text{NaN}$이고 $\text{NaN} \sim 2$다.

결과는 정의되지 않은 동작이다. 실제로는 라이브러리에 따라 틀린 순서, 무한 루프, 범위 밖 읽기가 된다. 필드별로 비교하거나 `std::tie` 튜플을 만들어라. `std::sort`는 안정 정렬이 아니므로, 동점이 입력 순서를 지켜야 하면 `std::stable_sort`를 써라.

```cpp
#include <algorithm>
#include <cassert>
#include <string>
#include <utility>
#include <vector>

struct Task {
    int priority;
    double deadline_s;
    std::string name;
};

int main() {
    std::vector<Task> tasks = {{2, 5.0, "grasp"}, {1, 3.0, "scan"}, {2, 1.0, "move"}, {1, 3.0, "log"}};
    // Higher priority first, then earlier deadline, then name. Never `>=` or `<=` here.
    std::sort(tasks.begin(), tasks.end(), [](const Task& a, const Task& b) {
        if (a.priority != b.priority) return a.priority > b.priority;
        if (a.deadline_s != b.deadline_s) return a.deadline_s < b.deadline_s;
        return a.name < b.name;
    });
    assert(tasks[0].name == "move" && tasks[1].name == "grasp");
    assert(tasks[2].name == "log" && tasks[3].name == "scan");

    std::vector<std::pair<int, char>> v = {{1, 'b'}, {0, 'z'}, {1, 'a'}};
    std::stable_sort(v.begin(), v.end(), [](const auto& x, const auto& y) { return x.first < y.first; });
    assert(v[1].second == 'b' && v[2].second == 'a');         // ties keep their input order
}
```

**빠른 입출력.** 기본적으로 C++ 스트림은 C의 `stdio`와 동기화되어 있고, `std::cin`은 읽기마다 먼저 `std::cout`을 비운다(flush). 큰 입력에서는 `main` 시작에서 둘 다 끄고, 줄 끝은 `'\n'`으로 써라. `std::endl`은 줄마다 flush까지 한다.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::ios::sync_with_stdio(false);       // stop synchronising with C stdio
    std::cin.tie(nullptr);                  // do not flush cout before each read
    int n = 0;
    if (!(std::cin >> n)) return 0;
    std::vector<long long> values(n);
    for (auto& value : values) std::cin >> value;
    long long total = 0;
    for (long long value : values) total += value;
    std::cout << total << '\n';             // '\n', not std::endl
}
```

표준 입력으로 `3 1 2 3`을 주면 `6`을 출력한다. 동기화를 끈 뒤에는 한 프로그램에서 `scanf`/`printf`와 스트림을 섞어 쓰지 마라.

### 5. 연구실이 읽는 코드

연구실 면접관은 동료가 읽듯이 코드를 읽는다. 이것이 무엇을, 어느 좌표계와 단위로 계산하는지 분명한가? 가정이 깨지면 요란하게 실패하는가? 그 습관은 인터뷰 코드에서 버그를 없애 주는 습관과 같다.

- **이름이 의미와 단위를 담는다.** `d`, `t`, `w`, `T` 대신 `dist_m`, `dt_s`, `omega_radps`, `T_world_base`. 세 줄짜리 루프 카운터라면 한 글자 이름도 괜찮다. 하지만 `i`와 `j`로 된 중첩 루프 두 개는 인덱스를 바꿔 쓰는 버그가 사는 곳이므로 `row`와 `col`로 이름을 지어라.
- **작은 함수, 함수마다 일 하나.** 입력 읽기, 계산, 출력을 서로 다른 함수에 둔다. 그러면 계산 함수를 입력 파일을 흉내 내지 않고도 스트레스 테스트나 단위 테스트에서 부를 수 있다.
- **불변식에는 단언문(assertion).** `assert`는 *내* 코드가 옳다면 반드시 참이어야 하는 것을 적는다. 확률의 합은 1이다, 인덱스는 범위 안이다, 쿼터니언의 노름은 1이다. 추론을 문서로 남기고, 조용히 틀린 답을 즉시 실패로 바꾼다. 호출자나 파일에서 온 *입력*을 검증하는 데 `assert`를 쓰지는 마라. `python -O`가 단언문을 없앤다. 대신 `ValueError`를 던져라.
- **수치 코드에는 형상과 단위를 주석으로.** 모든 배열 인자와 결과의 형상을 `(N, 3) points in metres, world frame`처럼 적는다. 수치 코드 버그의 대부분은 형상과 좌표계 버그이고, NumPy 브로드캐스팅은 틀린 형상을 조용히 틀린 답으로 바꾼다.
- **요청받으면 벡터화하고, 그 비용을 말하라.** Python 루프는 인터프리터 속도로 돈다. NumPy 식 하나는 그 루프를 컴파일된 코드에서 돌린다. 브로드캐스팅(**broadcasting**)은 형상이 다른 배열을 원소별로 결합하는 NumPy의 규칙이며 세 단계로 되어 있다. (1) 두 형상을 *오른쪽* 끝에 맞추고, 짧은 쪽 앞에 1을 채운다. (2) 맞춰진 축 길이 쌍은 서로 같거나 하나가 1이어야 하고, 아니면 NumPy가 오류를 낸다. (3) 결과는 각 축에서 더 긴 길이를 가지며, 길이 1인 축은 복사 없이 그 축을 따라 재사용(늘리기)된다. 그래서 맞춰진 길이 $p$와 $r$에 대해 (2)단계의 검사와 출력 길이는 다음과 같다.
$$p = r \ \text{ or } \ p = 1 \ \text{ or } \ r = 1, \qquad \text{out} = \max(p, r)$$
  *예:* `(2, 3)`과 `(3,)`은 `(1, 3)`으로 채워져 `(2, 3)`이 된다. *반례:* `(2, 3)`과 `(2,)`는 `(1, 2)`로 채워지고 $3$과 $2$가 맞지 않아 오류가 난다. "행마다 값 하나"에 필요한 것은 `(2, 1)`이다. 브로드캐스팅은 형상을 오른쪽부터 맞추고 길이 1인 축을 늘리므로, `(N, 1, D)` 배열에서 `(1, M, D)` 배열을 빼면 모든 쌍의 차이가 `(N, M, D)`로 나온다. 그 배열은 N·M·D개의 float 메모리를 쓴다. (a − b)·(a − b)를 전개한 형태 ‖a‖² + ‖b‖² − 2a·b는 `(N, M)`만 필요하지만, 반올림 때문에 아주 작은 실제 거리가 살짝 음수가 될 수 있으니 제곱근 전에 0으로 자른다.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="브로드캐스팅. 위: 2×3 배열과 길이 3 벡터. 벡터는 (1, 3) 모양으로 채워지고 그 한 행이 두 행 모두에 재사용되어 (2, 3)이 된다. 아래: 오른쪽 끝을 맞춘 모양들. (2, 3)과 (3,)은 (2, 3), (2, 3)과 (2,)는 (1, 2)로 채워져 3과 2가 맞지 않아 실패, (N, 1, D)와 (1, M, D)는 (N, M, D)가 된다.">
  <defs><marker id="aicBck" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="20" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="40" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="60" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="20" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="40" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <rect x="60" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="50" y="92" font-size="11" fill="currentColor" text-anchor="middle">(2, 3)</text>
  <text x="100" y="59" font-size="14" fill="currentColor" text-anchor="middle">+</text>
  <rect x="118" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="138" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="158" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <text x="148" y="92" font-size="11" fill="currentColor" text-anchor="middle">(3,)</text>
  <text x="206" y="59" font-size="14" fill="currentColor" text-anchor="middle">→</text>
  <rect x="224" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="244" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="264" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.2" stroke-opacity="0.9"/>
  <rect x="224" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <rect x="244" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <rect x="264" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.5" stroke-dasharray="3 2"/>
  <line x1="294" y1="44" x2="294" y2="64" stroke="currentColor" stroke-width="1.1" marker-end="url(#aicBck)"/>
  <text x="254" y="92" font-size="11" fill="currentColor" text-anchor="middle">(1, 3), 한 행 재사용</text>
  <text x="334" y="59" font-size="14" fill="currentColor" text-anchor="middle">=</text>
  <rect x="352" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="372" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="392" y="34" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="352" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="372" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <rect x="392" y="54" width="20" height="20" stroke="currentColor" stroke-width="1.1" fill="currentColor" fill-opacity="0.14" stroke-opacity="0.9"/>
  <text x="382" y="92" font-size="11" fill="currentColor" text-anchor="middle">(2, 3)</text>
  <text x="8" y="124" font-size="12" fill="currentColor">오른쪽 끝을 맞추고, 각 쌍은 같거나 한쪽이 1이어야 한다</text>
  <text x="78" y="150" font-size="11" fill="currentColor" font-weight="bold">예</text>
  <text x="70" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="78" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="95" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <rect x="116" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="133" y="174" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="70" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="78" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="95" y="200" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <rect x="116" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="133" y="200" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="95" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="133" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="78" y="250" font-size="11" fill="currentColor">결과: (2, 3)</text>
  <text x="78" y="268" font-size="10" fill="currentColor" fill-opacity="0.8">채운 1 (점선)</text>
  <text x="258" y="150" font-size="11" fill="currentColor" font-weight="bold">반례</text>
  <text x="250" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="258" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="275" y="174" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <rect x="296" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="313" y="174" font-size="11" fill="currentColor" text-anchor="middle">3</text>
  <text x="250" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="258" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.02" stroke-opacity="0.6" stroke-dasharray="3 2"/>
  <text x="275" y="200" font-size="11" fill="currentColor" text-anchor="middle" fill-opacity="0.7">1</text>
  <rect x="296" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="313" y="200" font-size="11" fill="currentColor" text-anchor="middle">2</text>
  <text x="275" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="313" y="226" font-size="12" fill="currentColor" text-anchor="middle" font-weight="bold">✗</text>
  <text x="258" y="250" font-size="11" fill="currentColor">오류: 3 대 2</text>
  <text x="258" y="268" font-size="10" fill="currentColor" fill-opacity="0.8">채운 1 (점선)</text>
  <text x="420" y="150" font-size="11" fill="currentColor" font-weight="bold">모든 쌍의 차</text>
  <text x="412" y="174" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">A</text>
  <rect x="420" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="437" y="174" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">N</text>
  <rect x="458" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="475" y="174" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <rect x="496" y="160" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="513" y="174" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">D</text>
  <text x="412" y="200" font-size="11" fill="currentColor" text-anchor="end" font-style="italic">b</text>
  <rect x="420" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="437" y="200" font-size="11" fill="currentColor" text-anchor="middle">1</text>
  <rect x="458" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="475" y="200" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">M</text>
  <rect x="496" y="186" width="34" height="20" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.08" stroke-opacity="0.9"/>
  <text x="513" y="200" font-size="11" fill="currentColor" text-anchor="middle" font-style="italic">D</text>
  <text x="437" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="475" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="513" y="226" font-size="12" fill="currentColor" text-anchor="middle">✓</text>
  <text x="420" y="250" font-size="11" fill="currentColor">결과: (N, M, D)</text>
</svg>

- **결정성.** 모든 난수원에 시드를 주고 생성기를 명시적으로 넘겨서 실패를 재현할 수 있게 하라. 문자열 `set`의 순회 순서는 인터프리터 실행마다 바뀐다(문자열 해싱이 프로세스마다 무작위화된다). 순서가 출력에 영향을 주면 순회 전에 정렬하라.

```python
import math

def wrap_to_pi(angle_rad):
    """Map an angle in radians into [-pi, pi]."""
    wrapped = (angle_rad + math.pi) % (2.0 * math.pi) - math.pi
    assert -math.pi <= wrapped <= math.pi, wrapped      # closed on purpose: see the self-check
    return wrapped

def unicycle_step(pose, v_mps, omega_radps, dt_s):
    """One explicit Euler step. pose = (x_m, y_m, theta_rad) in the world frame."""
    if dt_s <= 0.0:
        raise ValueError(f"dt_s must be positive, got {dt_s}")   # input check: not an assert
    x_m, y_m, theta_rad = pose
    return (x_m + v_mps * math.cos(theta_rad) * dt_s,
            y_m + v_mps * math.sin(theta_rad) * dt_s,
            wrap_to_pi(theta_rad + omega_radps * dt_s))

pose = unicycle_step((0.0, 0.0, 3.1), v_mps=1.0, omega_radps=1.0, dt_s=0.1)
assert -math.pi <= pose[2] < 0.0                         # 3.2 rad wrapped to about -3.08
assert wrap_to_pi(math.nextafter(-math.pi, -math.inf)) == math.pi
```

```python
import numpy as np

def pairwise_distances(a, b):
    """Euclidean distance between every row of a and every row of b.

    a: (N, D) points, metres;  b: (M, D) points, metres;  returns (N, M), metres.
    Memory: a temporary (N, M, D) array.
    """
    assert a.ndim == 2 and b.ndim == 2 and a.shape[1] == b.shape[1], (a.shape, b.shape)
    diff = a[:, None, :] - b[None, :, :]                 # (N, 1, D) - (1, M, D) -> (N, M, D)
    return np.sqrt((diff ** 2).sum(axis=-1))             # (N, M)

def pairwise_distances_low_memory(a, b):
    """Same result with only (N, M) temporaries."""
    sq = (a ** 2).sum(axis=1)[:, None] + (b ** 2).sum(axis=1)[None, :] - 2.0 * (a @ b.T)
    return np.sqrt(np.maximum(sq, 0.0))                  # rounding can make sq slightly negative

rng = np.random.default_rng(seed=0)                      # a local, seeded generator
a = rng.normal(size=(50, 3))
b = rng.normal(size=(40, 3))
reference = np.empty((50, 40))
for i in range(50):
    for j in range(40):
        reference[i, j] = np.linalg.norm(a[i] - b[j])
assert np.allclose(pairwise_distances(a, b), reference)
assert np.allclose(pairwise_distances_low_memory(a, b), reference, atol=1e-6)
assert np.array_equal(np.random.default_rng(7).normal(size=3), np.random.default_rng(7).normal(size=3))
```

### 6. 실시간과 로보틱스에서의 주의점

1 kHz로 도는 제어 루프는 밀리초마다 마감이 있고, 늦은 답은 틀린 답이다. 평균적으로 빠른 코드로는 부족하다. 중요한 것은 반복 한 번의 *최악* 시간이다. 그것이 마감을 놓치는지를 결정하기 때문이다. 흔한 도구 세 가지는 최악의 경우가 무한하거나 예측할 수 없으므로, 실시간 코드는 이것들을 핫 패스 — 매 주기 도는 코드 — 밖에 둔다.

**실시간의 정의.** 주기적 실시간 작업에는 이름 붙은 세 부분이 있다. 주기(**period**) $T$(1 kHz면 1 ms), 각 주기의 출력이 준비되어야 하는 마감(**deadline**) $D$(보통 $D = T$), 그리고 그 하드웨어에서 한 주기가 걸릴 수 있는 가장 긴 시간인 최악 실행 시간(**worst-case execution time**, WCET) $C$다. 모든 주기가 마감을 지켜야만 작업이 옳으므로 다음이 필요하다.
$$C \le D$$
경성(**hard**) 실시간 시스템에서는 한 번 놓치는 것이 곧 실패이고(토크 루프), 연성(**soft**) 시스템에서는 놓칠 때마다 품질만 떨어진다(비디오 스트림). *"실시간"의 반례:* 주기당 평균 0.2 ms이지만 10 000 주기에 한 번 3 ms가 걸리는 루프는 평균적으로 빠르지만, 1 kHz에서 약 $10\,000 / 1000 = 10$초마다 1 ms 마감을 놓친다.

- **힙 할당.** `new`, `malloc`, 그리고 이들을 부르는 모든 것 — 용량을 넘는 `std::vector::push_back`, `std::string` 만들기, `std::map`에 삽입하기 — 은 할당기 안에서 락을 잡거나, 빈 블록 목록을 뒤지거나, 운영체제에 페이지를 요청할 수 있다. 모든 것을 시작할 때 미리 할당하라. `reserve`, 고정 크기 `std::array`, 매 주기 재사용하는 버퍼. 인터뷰에서의 답은 "생성자에서 할당하고, 루프에서는 절대 하지 않는다"이다.
- **락.** 우선순위가 낮은 스레드가 잡은 뮤텍스는 그 스레드가 도는 동안 제어 스레드를 막을 수 있고, 중간 우선순위 스레드가 그 시간을 더 늘릴 수 있다(우선순위 역전). 우선순위 역전(**priority inversion**)은 세 부분으로 된 스케줄링 실패다. 높은 우선순위 스레드 H가 낮은 우선순위 스레드 L이 잡은 락을 기다린다. 락이 필요 없는 중간 우선순위 스레드 M이 준비되면 L보다 높으므로 L을 선점한다. 그래서 M이 도는 동안 H는 사실상 자기보다 *낮은* 우선순위인 M에게 막힌다. 우선순위 상속 뮤텍스는 L이 락을 잡고 있는 동안 L을 H의 우선순위로 잠시 올려 이를 고친다. 임계 구역을 아주 작게 유지하거나, `try_lock`을 쓰고 실패하면 그 갱신을 건너뛰거나, 단일 생산자·단일 소비자 락-프리 큐로 데이터를 넘겨라.
- **예외.** throw는 보통 예외 객체를 할당하고, 스택 되감기에는 스택에 따라 달라지는 시간이 든다. 핫 패스 함수에는 `noexcept`를 붙이고, 실패는 반환값이나 상태 플래그로 알리고, 오류는 실시간이 아닌 스레드에서 처리하라. 로깅과 콘솔 출력도 마찬가지다. 서식화는 할당하고, 터미널에 쓰기는 블록될 수 있다.

가비지 컬렉터와 인터프리터를 가진 Python은 경성 실시간 루프 밖에 둔다. 더 낮은 주기의 계획, 인식, 감독에는 괜찮다. 같은 문제의 ROS 2 쪽 — 단일 스레드 executor에서 긴 콜백이 왜 제어 타이머를 멈추게 하는지, 타이머가 어느 시계를 따르는지 — 은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]을 읽어라. 실시간 스케줄링 분석으로 가는 길도 거기서 안내한다.

핫 패스에서 "최근 N개 샘플 유지"의 표준 구조는 고정 배열 위의 링 버퍼다. push는 가장 오래된 샘플을 덮어쓰고, 아무것도 할당하지 않는다. 용량 $N$인 링 버퍼(**ring buffer**, 원형 버퍼)는 고정 배열에 정수 두 개, `head`(가장 오래된 샘플의 칸)와 `size`(쓰고 있는 칸 수, $0 \le$ `size` $\le N$)를 더한 것이다. 인덱스는 $N$을 법으로 감싸 돌므로, $i$번째로 오래된 샘플의 칸과 다음 push가 쓸 칸은 다음과 같다.
$$\text{slot}(i) = (\text{head} + i) \bmod N, \qquad \text{write slot} = (\text{head} + \text{size}) \bmod N$$
*예:* $N = 3$에서 0.1부터 0.5까지 넣으면 칸 0, 1, 2에 쓴 뒤 다시 0과 1에 써서 배열은 `[0.4, 0.5, 0.3]`, `head` = 2가 된다. 그래서 칸 2, 0, 1이 오래된 순서로 0.3, 0.4, 0.5를 돌려주고, 코드의 테스트가 이를 단언한다.

<svg viewBox="0 0 560 268" style="max-width:100%;height:auto" role="img" aria-label="칸 세 개짜리 링 버퍼에 0.1부터 0.5까지 넣는다. 각 행은 한 번 넣은 뒤의 배열, 쓴 칸 (head + size) mod 3, 넣은 뒤의 head를 보여 준다. 0.4와 0.5가 칸 0과 1을 덮어쓰면 배열은 0.4, 0.5, 0.3이고 head는 2다. i = 0, 1, 2에 대해 칸 (2 + i) mod 3을 읽으면 오래된 순서로 0.3, 0.4, 0.5가 나온다.">
  <defs><marker id="aicRbk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="106" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">0</text>
  <text x="150" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">1</text>
  <text x="194" y="34" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.75">2</text>
  <text x="74" y="34" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.75">칸</text>
  <text x="8" y="60" font-size="11" fill="currentColor">0.1 넣기</text>
  <rect x="84" y="44" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="106" y="60" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.1</text>
  <rect x="128" y="44" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <rect x="172" y="44" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <path d="M106 70 L101.5 77 L110.5 77 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="60" font-size="11" fill="currentColor">(0 + 0) mod 3 = 0</text>
  <text x="8" y="96" font-size="11" fill="currentColor">0.2 넣기</text>
  <rect x="84" y="80" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="96" font-size="11" fill="currentColor" text-anchor="middle">0.1</text>
  <rect x="128" y="80" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="150" y="96" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.2</text>
  <rect x="172" y="80" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <path d="M106 106 L101.5 113 L110.5 113 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="96" font-size="11" fill="currentColor">(0 + 1) mod 3 = 1</text>
  <text x="8" y="132" font-size="11" fill="currentColor">0.3 넣기</text>
  <rect x="84" y="116" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="132" font-size="11" fill="currentColor" text-anchor="middle">0.1</text>
  <rect x="128" y="116" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="150" y="132" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
  <rect x="172" y="116" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="194" y="132" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.3</text>
  <path d="M106 142 L101.5 149 L110.5 149 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="132" font-size="11" fill="currentColor">(0 + 2) mod 3 = 2</text>
  <text x="8" y="168" font-size="11" fill="currentColor">0.4 넣기</text>
  <rect x="84" y="152" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="106" y="168" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.4</text>
  <rect x="128" y="152" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="150" y="168" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
  <rect x="172" y="152" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="194" y="168" font-size="11" fill="currentColor" text-anchor="middle">0.3</text>
  <path d="M150 178 L145.5 185 L154.5 185 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="168" font-size="11" fill="currentColor">(0 + 3) mod 3 = 0</text>
  <text x="8" y="204" font-size="11" fill="currentColor">0.5 넣기</text>
  <rect x="84" y="188" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="106" y="204" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
  <rect x="128" y="188" width="44" height="24" stroke="currentColor" stroke-width="2.0" fill="currentColor" fill-opacity="0.18"/>
  <text x="150" y="204" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.5</text>
  <rect x="172" y="188" width="44" height="24" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.03"/>
  <text x="194" y="204" font-size="11" fill="currentColor" text-anchor="middle">0.3</text>
  <path d="M194 214 L189.5 221 L198.5 221 Z" stroke="none" fill="currentColor" stroke-linejoin="round"/>
  <text x="228" y="204" font-size="11" fill="currentColor">(1 + 3) mod 3 = 1</text>
  <text x="452" y="30" font-size="11" fill="currentColor" text-anchor="middle">읽기: slot(i) = (2 + i) mod 3</text>
  <path d="M 502.2 107.0 A 58.0 58.0 0 0 0 401.8 107.0 L 426.0 121.0 A 30.0 30.0 0 0 1 478.0 121.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.06"/>
  <text x="452" y="96" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
  <text x="452" y="50" font-size="10" fill="currentColor" text-anchor="middle" fill-opacity="0.85">칸 0</text>
  <text x="452" y="63" font-size="10" fill="currentColor" text-anchor="middle" font-weight="bold">i = 1</text>
  <path d="M 452.0 194.0 A 58.0 58.0 0 0 0 502.2 107.0 L 478.0 121.0 A 30.0 30.0 0 0 1 452.0 166.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.06"/>
  <text x="490.1" y="162" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
  <text x="512.6" y="181" font-size="10" fill="currentColor" fill-opacity="0.85">칸 1</text>
  <text x="512.6" y="194" font-size="10" fill="currentColor" font-weight="bold">i = 2</text>
  <path d="M 401.8 107.0 A 58.0 58.0 0 0 0 452.0 194.0 L 452.0 166.0 A 30.0 30.0 0 0 1 426.0 121.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.2"/>
  <text x="413.9" y="162" font-size="11" fill="currentColor" text-anchor="middle" font-weight="bold">0.3</text>
  <text x="391.4" y="181" font-size="10" fill="currentColor" text-anchor="end" fill-opacity="0.85">칸 2</text>
  <text x="391.4" y="194" font-size="10" fill="currentColor" text-anchor="end" font-weight="bold">i = 0</text>
  <path d="M 433 144.9 A 21 21 0 1 1 471 144.9" stroke="currentColor" stroke-width="1.3" fill="none" marker-end="url(#aicRbk)"/>
  <text x="8" y="256" font-size="11" fill="currentColor">▲ 넣은 뒤의 head: 가장 오래된 샘플. 가득 찬 버퍼에 넣으면 이것을 덮어쓴다</text>
</svg>

```cpp
#include <array>
#include <cassert>
#include <cstddef>

template <typename T, std::size_t N>
class RingBuffer {
public:
    void push(const T& value) noexcept {            // O(1); overwrites the oldest sample when full
        data_[(head_ + size_) % N] = value;
        if (size_ < N) ++size_;
        else head_ = (head_ + 1) % N;
    }
    std::size_t size() const noexcept { return size_; }
    const T& operator[](std::size_t i) const noexcept { return data_[(head_ + i) % N]; }  // 0 = oldest
private:
    std::array<T, N> data_{};                       // storage lives inside the object: no heap
    std::size_t head_ = 0;                          // index of the oldest sample
    std::size_t size_ = 0;
};

int main() {
    RingBuffer<double, 3> torque_nm;
    for (double sample : {0.1, 0.2, 0.3, 0.4, 0.5}) torque_nm.push(sample);
    assert(torque_nm.size() == 3);
    assert(torque_nm[0] == 0.3 && torque_nm[2] == 0.5);
}
```

### 7. 복잡도와 트레이드오프에 대해 말하기

"더 잘할 수 있나요?"는 더 영리한 요령을 달라는 요청인 경우가 드물다. 내 해법이 어디에 서 있는지 아는지 묻는 것이다. 하한에 비해, 그리고 대신 쓸 수 있는 다른 자원에 비해. 먼저 [[02-foundations/algorithms/complexity-recursion|11.1 §7]]의 다섯 부분 형식으로 복잡도를 말하고, 다음을 차례로 짚는다.

1. **"더 잘한다"가 무슨 뜻인지 묻는다.** 최악의 경우에 더 빠르게? 메모리를 덜? 스트림을 더 적게 훑기? 유지보수가 더 쉽게? 답이 서로 다르고, 묻는 것 자체가 다르다는 것을 안다는 표시다.
2. **지배적인 항을 찾는다.** 정렬이 O(n log n)이고 나머지가 모두 O(n)이면, 공략할 가치가 있는 것은 정렬뿐이다.
3. **하한을 확인한다.** *문제*에 대한 하한 $\Omega(g(n))$은 충분히 큰 모든 $n$에서, 어떤 알고리즘이든 크기 $n$인 어떤 입력에서는 적어도 $g(n)$의 상수배 걸음이 필요하다는 뜻이다($O$, $\Omega$, $\Theta$의 정의는 [[02-foundations/algorithms/complexity-recursion|11.1 §2]]). 어떤 알고리즘이든 입력을 읽어야 하므로, 모든 원소에 의존하는 문제에서 O(n)은 이길 수 없다. 비교 기반 정렬은 Ω(n log n)번의 비교가 필요하다. 답 K개를 만드는 데는 적어도 K가 든다. 이미 하한에 있다면 그렇게 말하고, 상수와 메모리로 넘어가라.
4. **어떤 트레이드오프를 택할지 말한다.**
   - *시간 대 메모리:* 해시 집합은 O(n) 추가 메모리로 기대 O(n) 시간을 준다. 제자리 정렬은 O(1) 추가 메모리로 O(n log n)을 준다(입력에 대한 C++ `std::sort`. Python의 `list.sort`도 최대 n/2개 포인터의 임시 공간이 필요하다).
   - *전처리 대 질의:* 한 번 정렬하고 많은 질의를 이진 탐색한다. 누적 합을 한 번 만들고 구간 합을 O(1)에 답한다.
   - *기대 대 최악:* 해시 테이블은 기대 O(1)이지만 최악 O(n)이다. 균형 트리는 O(log n)이 보장되고 순서를 유지한다.
   - *정확 대 근사:* 근사 최근접 이웃이나 Bloom 필터는 작고 통제된 오차를 큰 절약과 맞바꾼다.
   - *일괄 대 스트리밍:* 크기 k인 힙은 스트림을 저장하지 않고 O(n log k) 시간과 O(k) 메모리로 상위 k개를 찾는다.
   - *점근 대 상수:* 벡터화한 O(n²) NumPy 계산이 n이 수천일 때 순수 Python O(n log n) 루프를 이길 수 있다. 주장하기 전에 측정하라.

> [!example] 계산 예제 · Worked example
> **면접관:** "`longest_run`이 O(n)이네요. 더 잘할 수 있나요?"
>
> **소리 내어 한 답:** "시간으로는 안 됩니다. 답이 모든 원소에 의존하니까 어떤 알고리즘이든 n개를 다 읽어야 합니다. 더 잘할 수 있는 건 메모리입니다. 집합이 O(n) 추가 공간을 씁니다. 메모리가 제약이라면 제자리 정렬 후 한 번 훑겠습니다. C++에서 O(n log n) 시간, O(1) 추가 공간입니다. 그리고 프레임 번호가 n보다 크게 넓지 않은 크기 U의 범위에 있다고 알려져 있다면, U비트 비트 배열이 U/8바이트로 O(n + U) 시간을 주고 상수에서 해싱을 이깁니다. 프레임 스트림이라면 답이 마지막에만 필요한지 계속 필요한지 여쭤보겠습니다. 계속 필요하다면 각 구간의 끝점에서 길이로 가는 맵을 두고 프레임이 올 때마다 구간을 합치겠습니다. 프레임당 기대 O(1)입니다."
>
> 이 답은 하한을 말하고, 아직 개선할 수 있는 자원으로 넘어가고, 추측하는 대신 확인 질문을 한다.

### 이 페이지를 연습하는 법

1. **푸는 모든 문제에 §1의 절차를 적용한다.** 소리 내어, 또는 주석으로 한다: 다시 말하기, 손 예제, 전수 탐색, 개선, 코드, 손 테스트, 복잡도. 처음 열 문제는 단계마다 걸린 시간을 §1의 표와 비교한다.
2. **스트레스 테스트 파일을 하나 둔다.** 문제마다 전수 탐색을 먼저 쓰고 §2의 `stress`와 `shrink`를 재사용한다. 3000번 시행이 모두 일치할 때까지 멈추지 않는다.
3. **§3과 §4는 참조표로 연습한다.** 코드를 가리고 굵은 항목 이름 하나를 읽은 뒤, 그 코드가 무엇을 출력하거나 무엇을 단언하는지 예측하고 실행해 확인한다.
4. **매주 함수 하나를 §5의 방식으로 다시 쓴다.** 이름에 단위, 주석에 모양, 불변식 하나에 대한 단언, 시드를 준 생성기.
5. **모든 풀이에 "더 잘할 수 있나요?"를 소리 내어 답한다.** §7의 네 단계로 답한 다음에야 §7의 계산 예제를 읽는다.

### 스스로 점검

1. 어떤 문제가 n ≤ 2 × 10⁵, 값은 최대 10⁹이라고 하고 모든 쌍의 곱의 합을 묻는다. 설계를 시작하기 전에, 이 제약이 C++에서 알려 주는 두 가지는 무엇인가?
2. 스트레스 테스트가 값이 최대 10⁶인 원소 40개짜리 입력에서 실패를 알린다. 디버깅을 시작하기 전에 무엇을 바꾸고, 왜 그런가?
3. `rows = [ [0] * 2 ] * 2; rows[0][1] = 5; print(rows)`는 무엇을 출력하고, 어떻게 고치는가?
4. Python의 `-7 // 2`와 `-7 % 2`, C++의 `-7 / 2`와 `-7 % 2`를 말하라. C++에서 음수가 아닌 나머지는 어떻게 얻는가?
5. 동료가 `std::sort(v.begin(), v.end(), [](const Item& a, const Item& b) { return a.cost <= b.cost; });`로 정렬했다. 그의 테스트는 통과했다. 무엇이 틀렸고, 어떻게 고치는가?
6. `s`가 `std::set`일 때 `std::lower_bound(s.begin(), s.end(), x)`가 왜 느릴 수 있고, 대신 무엇을 써야 하는가?
7. `wrap_to_pi`(§5)의 첫 버전은 `-math.pi <= wrapped < math.pi`를 단언했다. −π 근처의 무작위 각도로 한 스트레스 테스트가 이를 실패시켰다. 왜 그런가? 그리고 단언을 느슨하게 한 것이 옳은 대응이었는가?
8. 1 kHz 제어기가 매 주기 샘플을 `std::vector`에 append하고 `std::cout << ... << std::endl`로 상태 한 줄을 출력한다. 대개 마감을 지키지만 몇 초마다 한 번씩 놓친다. 원인 두 가지와 해법을 말하라.
9. 크기 k인 힙으로 `k_closest`를 O(n log k)에 썼다. 면접관이 "더 잘할 수 있나요?"라고 묻는다. 기대 시간이 더 빠른 방법 하나와, 그래도 힙을 유지할 수 있는 이유 하나를 말하라.

> [!tip]- 스스로 점검 정답 · Answers
> 1. 첫째, 목표 복잡도다. n = 2 × 10⁵이면 O(n²)(4 × 10¹⁰걸음)는 안 되고 O(n log n)이나 O(n)을 가리킨다 — 여기서 모든 쌍의 합은 ((Σx)² − Σx²)/2이므로 O(n)에 계산된다. 둘째, 타입이다. 곱 하나가 10¹⁸에 이르고, 약 2 × 10¹⁰개 쌍의 합은 `long long`의 범위(약 9.2 × 10¹⁸)를 훨씬 넘으므로, 답을 어떤 수로 나눈 나머지로 내는지, 아니면 128비트나 큰 정수 산술이 필요한지 물어야 한다. `int`는 곱 하나에도 틀리다.
> 2. 입력 크기와 값 범위를 줄이고(예: n ≤ 8, 값은 −3…3), 난수 시드를 고정하고, 실패가 유지되는 동안 원소를 지워 실패 입력을 줄인다. 범위가 좁은 작은 입력은 반복과 동점을 자주 만들고 손으로 추적할 수 있는 반례를 준다. 고정된 시드는 매 실행이 같은 실패를 재현하게 한다.
> 3. `[ [0, 5], [0, 5] ]`를 출력한다(첫 괄호 뒤의 공백은 없다). 두 항목이 같은 안쪽 리스트를 가리키기 때문이다. 독립된 행을 만들어라: `[ [0] * 2 for _ in range(2)]`.
> 4. Python: `-4`와 `1`(음의 무한대 쪽으로 내림, 나머지는 나누는 수의 부호). C++: `-3`과 `-1`(0 쪽으로 자름, 나머지는 나뉘는 수의 부호). C++에서 음수가 아닌 나머지: 양수 `m`에 대해 `((a % m) + m) % m`.
> 5. `<=`는 같은 원소에 참을 반환하므로 `comp(a, a)`가 참이고, `std::sort`가 요구하는 엄격한 약순서를 어긴다. 동작은 정의되지 않는다. 동점이 적은 작은 테스트에서는 흔히 되다가, 같은 비용이 많은 실제 데이터에서 틀린 순서, 크래시, 범위 밖 읽기를 낸다. `a.cost < b.cost`를 쓰라(그리고 NaN인 비용이 없는지 확인하라).
> 6. `std::set`의 반복자는 임의 접근이 아니라 양방향이다. `std::lower_bound`는 여전히 비교를 O(log n)번만 하지만, 범위의 가운데로 가려면 노드를 하나씩 밟아야 하므로 시간은 O(n)이다. 트리를 O(log n)에 걷는 멤버 함수 `s.lower_bound(x)`를 써라.
> 7. −π 바로 아래의 각도에서 `angle + pi`는 아주 작은 음수이고, Python의 `%`는 나누는 수의 부호를 가진 결과를 낸다. 정확한 결과 2π − ε는 표현할 수 없어 정확히 2π로 반올림되므로 `wrapped`는 π가 된다. 단언은 제대로 발동한 것이다. 부동소수점 산술이 보장하지 않는 가정(반열린 구간)을 드러냈다. 옳은 대응은 반사적 수정이 아니라 결정이다. 닫힌 구간 [−π, π]를 받아들이고 문서화하거나(§5가 그렇게 한다), 하류 코드가 반열린 범위에 기댄다면 π를 명시적으로 −π로 보낸다. 단언을 지우는 것이 틀린 대응이었을 것이다.
> 8. 첫째, `push_back`이 가끔 용량을 넘어 재할당하면서 벡터 전체를 복사한다 — 실행 시간이 길어질수록 커지는 스파이크다. 미리 할당하거나, 고정 크기 링 버퍼(§6)를 두고 샘플을 로깅 스레드에 넘겨라. 둘째, `std::endl`은 flush하고, 서식화와 터미널 쓰기는 할당하고 블록될 수 있다. 루프에서 출력을 빼고, 상태는 미리 할당한 구조에 기록해 실시간이 아닌 스레드에서 출력하라.
> 9. Quickselect(C++의 `std::nth_element`)는 k번째로 작은 거리를 기준으로 기대 O(n) 시간에 분할하고, 그러면 앞의 k개가 답이다. 그 k개를 정렬하면 O(k log k)가 더해진다. 힙을 유지할 이유: 점 n개를 모두 저장하지 않고 스트림에서 동작하고(O(k) 메모리), 최악 O(n log k)가 보장되며, k가 작으면 log k는 어차피 작은 상수다.

### 과제 · Problem set

면접 트랙을 다시 쓰지 않는 추가 한 문제. [[02-foundations/lab-plants|0.6]]의 **P2**, 고정 자세. $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$, $F=(0,-10)$.

1. 그 고정 $J$와 길이 2인 힘에 대해 $\tau=J^\top F$를 돌려주는 `joint_torque(F)`(Python 또는 C++). $F=(0,-10)$에서 값을 말하라. 단위. 시간 루프 없음.

> [!tip]- 정답 · Solutions
> $J^\top=\begin{pmatrix}-1&1\\-1&0\end{pmatrix}$이므로 $\tau=(-10,\,0)\,\mathrm{N{\cdot}m}$. Python: 카탈로그 $J$에 `tau = J.T @ F`. C++: `tau[0] = -F[0] + F[1]; tau[1] = -F[0]`. $v=J\dot\theta$의 정역학 쌍대. 같은 $J$, 역행렬 없음.

### 출처

- A. S. Kulikov, P. A. Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — 3장(프로그래밍 과제를 단계별로 풀기, 테스트, 순진한 해법에 대한 스트레스 테스트)과 8장(좋은 프로그래밍 관행: 언어 공통, C++, Python). 이 페이지의 절차, 체크리스트, 예제는 독립적으로 작성했다.
- cppreference.com, *C++ reference* — 컨테이너 라이브러리(`std::vector` 반복자 무효화, `std::unordered_map`, `std::map`, `std::set`, `std::priority_queue`), `std::sort`, `std::stable_sort`와 *Compare* 명명 요구사항, `std::hash`, `std::accumulate`, 산술 연산자(정수 나눗셈과 나머지), 구조적 바인딩 선언, `std::ios_base::sync_with_stdio`.
- Python Software Foundation, *The Python Standard Library*와 *The Python Language Reference*(docs.python.org, 3.12판) — `collections`, `heapq`, `bisect`, `itertools`, `functools`, `timeit`, `sys.setrecursionlimit`; Sorting HOW-TO(안정성); 튜토리얼의 부동소수점 산술 장; 공유되는 기본 인자와 다차원 리스트에 관한 Programming FAQ 항목; 이항 산술 연산(내림 나눗셈과 나머지); `PYTHONHASHSEED`.
- NumPy documentation(numpy.org) — 브로드캐스팅 규칙, 난수 `Generator` / `default_rng`.
- K. Claessen, J. Hughes, "QuickCheck: a lightweight tool for random testing of Haskell programs," *Proceedings of the Fifth ACM SIGPLAN International Conference on Functional Programming (ICFP)*, 2000. DOI: 10.1145/351240.351266 — 자동 줄이기를 갖춘 속성 기반 무작위 테스트의 기원.
- ROS 2 design article — *Introduction to Real-time Systems*(design.ros2.org) — 실시간 코드가 제어 루프에서 동적 할당, 블로킹 동기화, 한계 없는 연산을 피하는 이유.
