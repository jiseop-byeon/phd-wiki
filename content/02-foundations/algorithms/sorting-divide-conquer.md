---
title: 11.3 Sorting & Divide-and-Conquer
tags: [foundations, algorithms, interviews]
study-depth: Working
wiki-support: Working
depth-goal: "Implement merge sort, randomized quicksort, binary search on a monotone predicate, and quickselect from a blank file, and prove out loud why each is correct and what it costs."
mastery-when: "Raise to Mastery only if the research contribution depends on a new divide-and-conquer or selection algorithm whose bound must be proved, for example a spatial index or a batched nearest-neighbour method."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/algorithms/complexity-recursion|11.1 §3]] (recurrences and the master method) · [[02-foundations/probability|3. Probability]] (expectation and linearity, for §3 and §7)
> [[02-foundations/algorithms/complexity-recursion|11.1 §3]](점화식과 마스터 방법) · [[02-foundations/probability|3. 확률]](기댓값과 선형성, §3·§7에 필요)
>
> Track map · 트랙 지도: [[02-foundations/algorithms/index|11. Algorithms & Data Structures]]

## English

Sorting is the most studied problem in algorithms, and for an interview that is useful rather than boring: every idea you need for divide-and-conquer shows up in it in its simplest form. Merge sort puts the work in the combine step, quicksort puts it in the split, the lower bound tells you when to stop looking for something faster, and binary search, selection, and closest pair reuse the same moves on different problems.

What interviews ask: write merge sort or quicksort without bugs and explain why it is correct; say why quicksort is $O(n \log n)$ *in expectation* and when it is quadratic; count inversions; use the library sort correctly (stability, keys, comparators); write a binary search that has no off-by-one errors, including "binary search on the answer"; find the k-th smallest or the top k without sorting everything. Research-lab interviews add the robotics versions: a median filter, a KD-tree built by median splits, merging sensor streams by timestamp, and interpolating a signal at an arbitrary time.

> [!note] First pass · 처음이라면
> Read §1, §2, §3 and §6 first; they are what most problems test. §5 saves you from library bugs you will otherwise meet in real code. §4 and §7 are the "why can't we do better" and "we only need one element" questions. §8 is for recognizing classics when they appear.

### 1. The divide-and-conquer shape

**The idea in one sentence:** split the input into smaller instances of the same problem, solve those recursively, and combine their answers into the answer for the whole.

Every divide-and-conquer algorithm answers three questions, and an interviewer will ask you all three.

1. **How do you split, and what is the base case?** The pieces must be strictly smaller, or the recursion never ends. A base case of size 0 or 1 is almost always enough.
2. **Why is the combined answer correct?** The argument is induction on the input size: *assume* the recursive calls return correct answers for the smaller pieces, then show that the combine step turns them into a correct answer for the whole. You never trace the recursion to prove it.
3. **What does the split and combine cost?** That cost, together with the number and size of the pieces, is a recurrence. Solve it with the recursion tree or the master method from [[02-foundations/algorithms/complexity-recursion|11.1 §3]].

**The definition, precisely.** Divide-and-conquer is an algorithm-design paradigm, not one algorithm. An algorithm belongs to it when it has all three named parts.

- **Divide**: an instance of size $n$ above a base size $n_0$ is turned into $a \ge 1$ instances of the *same* problem, each strictly smaller than $n$.
- **Conquer**: each piece is solved by a recursive call, and an instance of size $n \le n_0$ is a **base case**, solved directly without recursion.
- **Combine**: the answer for the whole is built from the $a$ answers of the pieces.

When every piece has size $n/b$ for a constant $b > 1$, the running time satisfies the recurrence below, because the whole costs the $a$ recursive calls plus the non-recursive divide and combine work:
$$T(n) = a\,T(n/b) + f(n) \ \text{ for } n > n_0, \qquad T(n) = \Theta(1) \ \text{ for } n \le n_0$$
Here $a$ is the number of pieces, $n/b$ the size of each piece, $f(n)$ the cost of dividing and combining at size $n$, and $n_0$ the largest base-case size, usually 1. Merge sort has $a = 2$, $b = 2$ and $f(n) = \Theta(n)$; binary search has $a = 1$, $b = 2$ and $f(n) = \Theta(1)$. An unbalanced split writes the actual piece sizes instead, as quicksort's $T(q) + T(n - 1 - q)$ in §3 does. The symbols $O$, $\Omega$ and $\Theta$ are defined in [[02-foundations/algorithms/complexity-recursion|11.1 §2]].

**Non-example.** The recursion $F(n) = F(n-1) + F(n-2)$ for Fibonacci numbers also splits into smaller instances of the same problem, but its pieces overlap, since $F(n-1)$ calls $F(n-2)$ again. Plain recursion therefore makes 2,692,537 calls to compute $F(30)$ although only 31 distinct arguments exist, so it is the dynamic-programming case described below, not a useful divide-and-conquer.

Every algorithm on this page is one row of the table below. Learn the recurrence alongside the name, because "what is the recurrence?" is how you turn a new divide-and-conquer idea into a complexity in thirty seconds.

| Algorithm | Recurrence | Cost | Why |
|---|---|---|---|
| Binary search (§6) | $T(n) = T(n/2) + O(1)$ | $\Theta(\log n)$ | one piece, constant work, $\log_2 n$ levels |
| Merge sort (§2) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | every level costs $O(n)$ |
| Quicksort, median pivot (§3) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | same shape; random pivots give it in expectation |
| Quicksort, worst pivot (§3) | $T(n) = T(n-1) + O(n)$ | $\Theta(n^2)$ | the pieces shrink by one, not by half |
| Quickselect, good pivot (§7) | $T(n) = T(3n/4) + O(n)$ | $\Theta(n)$ | work shrinks geometrically, root dominates |
| Median of medians (§7) | $T(n) = T(n/5) + T(7n/10) + O(n)$ | $\Theta(n)$ | $1/5 + 7/10 < 1$, so levels shrink |
| Fast exponentiation (§8) | $T(n) = T(n/2) + O(1)$ | $\Theta(\log n)$ multiplications | halve the exponent |
| Closest pair (§8) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | the strip scan is linear |
| Karatsuba (§8) | $T(n) = 3T(n/2) + O(n)$ | $\Theta(n^{\log_2 3})$ | leaves dominate |

**When divide-and-conquer is the wrong tool.** If the pieces *overlap*, meaning the same subproblem is reached through many paths, plain recursion repeats work exponentially; that is the signal for dynamic programming ([[02-foundations/algorithms/dynamic-programming|11.5 §1]]). Merge sort's two halves never share an element, so there is nothing to cache.

**Two Python pitfalls that change the complexity.**

- **Slicing copies.** `a[mid:]` costs O(n). Inside merge sort that is harmless, because the combine step is O(n) anyway. Inside binary search it turns $O(\log n)$ into $O(n)$. Pass indices `lo, hi` instead of slices whenever the non-recursive work is supposed to be less than linear.
- **Recursion depth.** CPython's default limit is 1000 frames. A balanced split has depth $\log_2 n$, about 30 for a billion elements, so it is safe. An unbalanced split, such as quicksort with a bad pivot, has depth $n$ and crashes long before it gets slow. §3 shows the fix.

### 2. Merge sort, and counting inversions on the way

**The idea in one sentence:** sort the left half, sort the right half, then merge the two sorted halves by repeatedly taking the smaller of their two front elements.

**The merge invariant.** While merging `left` and `right` with pointers `i` and `j`, the output always holds the smallest `i + j` elements of both lists, in sorted order. It stays true because both inputs are sorted: `left[i]` is the smallest element left in `left`, and `right[j]` is the smallest element left in `right`, so the smaller of the two is the smallest element remaining anywhere. When one list runs out, the rest of the other is already sorted and larger than everything output, so it is appended as a block. The whole sort is then correct by induction (§1): if the recursive calls sort the halves, merging produces the sorted whole.

**Time: $\Theta(n \log n)$ on every input.** The recursion tree has $\log_2 n$ levels. At each level the pieces partition the whole array, and merging pieces of total length $n$ costs O(n). So the total is $n$ per level times $\log_2 n$ levels. Nothing depends on the input order: sorted, reversed and random inputs all cost the same, which is a strength when you need a guarantee. Written as a recurrence with its base case, charging $n$ for a merge of total length $n$:
$$T(n) = 2\,T(n/2) + n \ \text{ for } n \ge 2, \qquad T(1) = 1$$
For $n$ a power of 2 this solves exactly to $T(n) = n \log_2 n + n$, because each of the $\log_2 n$ merge levels adds $n$ and the $n$ single-element leaves add 1 each. For example $T(8) = 2\,T(4) + 8 = 2 \cdot 12 + 8 = 32 = 8 \cdot 3 + 8$.

**Space: O(n) extra.** The merge writes into a buffer the size of its two inputs. The recursion stack adds $O(\log n)$. In-place merging is possible but complicated and slow, so interviews accept O(n). On a **linked list** merge sort needs only O(1) extra space, because merging relinks nodes instead of copying them; that makes it the standard way to sort a linked list.

**Stability.** First, what any sort must produce. Given items $x_1, \dots, x_n$ with keys $k(x_i)$, a sort outputs a permutation $\pi$ of the positions that puts the keys in nondecreasing order, $k(x_{\pi(1)}) \le k(x_{\pi(2)}) \le \dots \le k(x_{\pi(n)})$. When keys repeat, several permutations do that. A sort is **stable** if it always outputs the one in which items with equal keys keep their input order:
$$i < j \ \text{ and } \ k(x_i) = k(x_j) \implies \pi^{-1}(i) < \pi^{-1}(j)$$
Here $\pi^{-1}(i)$ is the output position of input item $i$, so the condition says that of two equal-key items, the one that came first in the input also comes first in the output. The code below shows it: `("lidar", 3)` stays ahead of `("cam", 3)`. Merge sort is stable exactly when the merge takes from the left on ties, which is why the comparison below is `<=` and not `<`.

- **Non-example.** Selection sort, which swaps the smallest remaining item to the front, is not stable. On $[(2, a), (2, b), (1, c)]$ sorted by the number, the first swap exchanges $(2, a)$ with $(1, c)$ and gives $[(1, c), (2, b), (2, a)]$, so $a$ and $b$ have changed order. Quicksort and heapsort are not stable either.
- **Why it matters.** Stability matters whenever the order of equal keys carries information. If you sort detections by class after they were already in timestamp order, a stable sort keeps each class in time order for free. It is also what makes sorting by several keys in successive passes work (§5), and what makes radix sort correct (§4).

```python
def merge_sort(a, key=lambda x: x):
    """Return a new list with the items of a sorted by key. Stable."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid], key), merge_sort(a[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):     # ties go left: this is what makes it stable
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])                      # at most one of these two is non-empty
    out.extend(right[j:])
    return out

print(merge_sort([5, 2, 9, 2, 7, 1]))         # [1, 2, 2, 5, 7, 9]
events = [("lidar", 3), ("imu", 1), ("cam", 3), ("imu", 2), ("lidar", 1)]
print(merge_sort(events, key=lambda e: e[1])) # equal times keep input order
# [('imu', 1), ('lidar', 1), ('imu', 2), ('lidar', 3), ('cam', 3)]
```

The same merge, applied to $k$ sorted streams at once with a heap, is how you combine several time-ordered sensor logs into one: `heapq.merge(*streams, key=...)` costs $O(N \log k)$ for $N$ records in total and reads the streams lazily. It is also the core of **external sorting**, where the data does not fit in memory: sort chunks that do fit, write them out, then k-way merge the files.

**Counting inversions.** An **inversion** of a sequence $a[1], \dots, a[n]$ is a pair of positions $i < j$ whose values are out of order, $a[i] > a[j]$. The inversion count is the number of such pairs:
$$\operatorname{inv}(a) = \big|\{(i, j) : 1 \le i < j \le n,\ a[i] > a[j]\}\big|$$
The inequality is strict, so equal values never form an inversion: $[2, 2]$ has none. A sorted array has $\operatorname{inv}(a) = 0$, and a reversed array of distinct values has all $n(n-1)/2$, since every pair is out of order, so the count measures how far a sequence is from sorted. It also counts work: insertion sort swaps only adjacent out-of-order elements, and each such swap removes exactly one inversion, so it makes exactly $\operatorname{inv}(a)$ swaps, 3 for the $[3, 1, 4, 2]$ below. Checking all pairs costs $O(n^2)$. Merge sort counts them in $O(n \log n)$ with one extra line.

Split the inversions into those inside the left half, those inside the right half, and **split inversions** with one element in each half. The recursive calls return the first two counts. For the third, look at the merge. A left element $x$ and a right element $y$ form an inversion exactly when $x > y$, and that is exactly when $y$ is output before $x$. So when the merge outputs `right[j]`, every element still waiting in `left` forms an inversion with it, and there are `len(left) - i` of them. Adding that number at each such step counts all split inversions during the O(n) merge, so the recurrence is still $T(n) = 2T(n/2) + O(n)$.

> [!example] Worked example · 계산 예제
> Count the inversions of $[3, 1, 4, 2]$. The left half $[3, 1]$ has one inversion and sorts to $[1, 3]$. The right half $[4, 2]$ has one and sorts to $[2, 4]$. Now merge $[1, 3]$ with $[2, 4]$.
> - Output 1, from the left. Adds nothing.
> - Output 2, from the right, while $[3]$ is still waiting on the left. Adds 1: the pair (3, 2).
> - Output 3, then 4. Adds nothing.
>
> Total: $1 + 1 + 1 = 3$. Check by listing all pairs: (3, 1), (3, 2), (4, 2).

**Where this is used: ranking agreement.** Suppose two rankings of the same $n$ items: the order in which a simulator ranks ten policy checkpoints, and the order of their real-robot success rates; or a learned reward model's ranking of trajectories against a human's. A pair of items is **concordant** if both rankings put them in the same order and **discordant** otherwise. With $r_A(x)$ and $r_B(x)$ the positions of item $x$ in the two rankings, the pair $x, y$ is concordant when $(r_A(x) - r_A(y))(r_B(x) - r_B(y)) > 0$ and discordant when that product is negative; it is zero only for a tie. Kendall's tau is the fraction of concordant pairs minus the fraction of discordant ones:

$$\tau = \frac{C - D}{n(n-1)/2} = 1 - \frac{4D}{n(n-1)}$$

Here $C$ is the number of concordant pairs, $D$ the number of discordant pairs, and $n(n-1)/2$ the number of pairs of $n$ items. The second form follows because, without ties, every pair is one or the other, so $C + D = n(n-1)/2$. $\tau = 1$ means identical order, $\tau = -1$ means reversed. The key observation is that $D$ is an inversion count: list the items in the first ranking's order, write down each item's position in the second ranking, and the discordant pairs are exactly the inversions of that list. For example, take four items A, B, C, D in the first ranking's order, and suppose the second ranking puts them at positions 3, 1, 4, 2. The discordant pairs are the three inversions of $[3, 1, 4, 2]$ counted above, so $D = 3$, $C = 6 - 3 = 3$, and $\tau = (3 - 3)/6 = 0$: the two rankings agree on as many pairs as they disagree on. So Kendall's tau costs $O(n \log n)$ instead of $O(n^2)$ (Knight, 1966). With ties, use the tau-b correction, which is the default in `scipy.stats.kendalltau`.

```python
def sort_and_count(a):
    """Return (sorted copy of a, number of pairs i < j with a[i] > a[j])."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])
    out, i, j, split = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:                      # right[j] jumps ahead of every left item still waiting
            out.append(right[j])
            j += 1
            split += len(left) - i
    out += left[i:] + right[j:]
    return out, inv_left + inv_right + split

def kendall_tau(rank_a, rank_b):
    """Kendall tau of two rankings without ties; rank_x[item] is item's position."""
    n = len(rank_a)
    order = sorted(range(n), key=lambda item: rank_a[item])   # items in A's order
    _, discordant = sort_and_count([rank_b[item] for item in order])
    return 1 - 4 * discordant / (n * (n - 1))

print(sort_and_count([3, 1, 4, 2])[1])                        # 3
print(kendall_tau([0, 1, 2, 3, 4], [1, 0, 2, 4, 3]))          # 0.6
```

> [!example] Worked example · 계산 예제
> Five checkpoints A–E have real-robot success rates in the order A, B, C, D, E (best first). A simulator ranks them B, A, C, E, D. So `rank_a = [0, 1, 2, 3, 4]` (real) and `rank_b = [1, 0, 2, 4, 3]` (simulator), indexed A to E. Listed in real order, the simulator positions are $[1, 0, 2, 4, 3]$, which has two inversions: (A, B) and (D, E). So $D = 2$, $C = 10 - 2 = 8$, and $\tau = (8 - 2)/10 = 0.6$. The simulator picks the right top three as a set, but you should not trust its ranking of adjacent checkpoints.

**Interview pitfalls.**

- `left.pop(0)` in the merge is O(n) per call and makes the sort quadratic. Use indices, or `collections.deque` with `popleft`.
- Using `<` in the merge still sorts, but silently loses stability.
- In the inversion count, add `len(left) - i` (the items still waiting), not `len(left)` or `mid - j`.

### 3. Quicksort: partition, random pivots, and why it is fast

**The idea in one sentence:** pick a pivot, rearrange the array so smaller elements come before it and larger ones after it, then sort the two sides recursively.

Where merge sort does its work in the combine step and splits trivially, quicksort does its work in the split, the **partition**, and needs no combine at all. A partition of the range $a[lo..hi]$ around a pivot value $p$ rearranges the range and returns an index $q$ such that
$$a[i] \le p \ \text{ for } lo \le i < q, \qquad a[q] = p, \qquad a[i] \ge p \ \text{ for } q < i \le hi$$
so the pivot already sits at an index it can have in the sorted array, because everything before it is no larger and everything after it is no smaller. Lomuto's scheme below meets this with the stricter $<$ on the left; Hoare's meets a weaker form that does not fix the pivot at $q$. Once both sides are sorted in place, the array is sorted. Correctness is the same induction as §1. After partitioning, the pivot is in its final position, every element to its left belongs to its left, and the recursive calls sort each side.

**Lomuto partition.** Use the last element as the pivot, and scan left to right with one boundary index `i`. The invariant is that `a[lo:i]` holds elements smaller than the pivot and `a[i:j]` holds elements that are not. When `a[j]` is smaller than the pivot, swap it to position `i` and advance `i`. At the end, swap the pivot into position `i`, which is its final place. Lomuto is the easiest to write correctly and returns the pivot's index, which quickselect (§7) needs. It makes more swaps than Hoare's scheme, though, and with only a two-way test it degrades to $\Theta(n^2)$ when many elements equal the pivot: an array of identical values splits into $n - 1$ and $0$ at every level.

**Hoare partition.** Hoare's original scheme (1961) moves two indices toward each other from the ends. The left index stops at an element that is not smaller than the pivot, the right index stops at one that is not larger, and the two elements are swapped. When the indices cross, it returns `j` such that everything in `a[lo..j]` is ≤ the pivot and everything in `a[j+1..hi]` is ≥ it. The pivot is *not* necessarily at `j`, so the recursive calls are on `[lo, j]` and `[j+1, hi]`, and neither side excludes the pivot. Hoare usually makes fewer swaps than Lomuto and splits an all-equal array in the middle, where Lomuto degrades to quadratic time. The trap is that the pivot must not be `a[hi]`: then `j` can come back as `hi`, the recursive call gets the same range again, and the recursion never ends. Use the middle element, or swap a random element to `lo`.

```python
def lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around a[hi]; return the pivot's final index."""
    pivot, i = a[hi], lo              # invariant: a[lo:i] < pivot <= a[i:j]
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def hoare_partition(a, lo, hi):
    """Return j with a[lo..j] <= pivot <= a[j+1..hi]; the pivot need not sit at j."""
    pivot = a[(lo + hi) // 2]         # never a[hi]: j could equal hi and recurse forever
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]

a = [4, 7, 2, 9, 1, 5]
print(lomuto_partition(a, 0, 5), a)   # 3 [4, 2, 1, 5, 7, 9]
b = [4, 7, 2, 9, 1, 5]
print(hoare_partition(b, 0, 5), b)    # 1 [1, 2, 7, 9, 4, 5]
```

> [!example] Worked example · 계산 예제
> Lomuto on $[4, 7, 2, 9, 1, 5]$ with pivot 5, starting with `i = 0`.
> - `j=0`: 4 < 5, swap `a[0]` with itself, `i = 1`.
> - `j=1`: 7 is not smaller, nothing happens.
> - `j=2`: 2 < 5, swap `a[1]` and `a[2]`, giving $[4, 2, 7, 9, 1, 5]$, `i = 2`.
> - `j=3`: 9, nothing.
> - `j=4`: 1 < 5, swap `a[2]` and `a[4]`, giving $[4, 2, 1, 9, 7, 5]$, `i = 3`.
>
> Finally swap the pivot into `a[3]`, giving $[4, 2, 1, 5, 7, 9]$. The pivot 5 is at index 3, with smaller elements on its left and larger ones on its right.

**Why the pivot choice decides everything.** If the pivot lands at rank $q$, so that $q$ elements go left and $n - 1 - q$ go right, quicksort's cost satisfies
$$T(n) = T(q) + T(n - 1 - q) + \Theta(n), \qquad T(0) = T(1) = \Theta(1)$$
because the partition is linear and the pivot itself is in neither recursive call. If the pivot is always the median, the recurrence is $T(n) = 2T(n/2) + O(n)$, which is $\Theta(n \log n)$. If it is always the minimum or maximum, one side is empty and the other has $n - 1$ elements, so $T(n) = T(n-1) + O(n) = \Theta(n^2)$. A fixed rule such as "use the first element" hits that worst case on **already sorted or reverse-sorted input**, which is common in practice: timestamps, re-sorting a nearly sorted list, a list sorted by a previous stage. A **random pivot** (every element equally likely) removes the dependence on the input. The expected running time is then $O(n \log n)$ *for every input*, where the expectation is over the algorithm's own coin flips, not over some assumed distribution of inputs.

**The expected-time argument.** This proof is a favourite interview question because it avoids solving a messy random recurrence.

1. Let $z_1 < z_2 < \dots < z_n$ be the elements in sorted order, assumed distinct. The running time is proportional to the number of comparisons $C$, since each partition does $O(1)$ work per comparison.
2. Two elements are compared only when one of them is the pivot, and the pivot is then left out of both recursive calls. So each pair is compared **at most once**. Let $X_{ij}$ be 1 if $z_i$ and $z_j$ are ever compared and 0 otherwise. Then $C = \sum_{i<j} X_{ij}$, and by linearity of expectation ([[02-foundations/probability|3. Probability §2]]), $E[C] = \sum_{i<j} \Pr[z_i, z_j \text{ compared}]$.
3. **The key claim:** $z_i$ and $z_j$ are compared if and only if the first pivot chosen from $\{z_i, z_{i+1}, \dots, z_j\}$ is $z_i$ or $z_j$. Until some element of that set is chosen as a pivot, the whole set stays together in one subarray, because any pivot outside the set is smaller or larger than all of them. If the first one chosen is $z_i$ or $z_j$, it is compared with everything in its subarray, including the other one. If it is some $z_k$ strictly between them, $z_i$ goes left and $z_j$ goes right, and they are never compared.
4. The pivot is uniform, so each of the $j - i + 1$ elements of the set is equally likely to be the first one picked. Two of those choices lead to a comparison, so $\Pr[z_i, z_j \text{ compared}] = 2/(j-i+1)$.
5. Sum it. For each $i$, substitute $k = j - i + 1$, which runs from 2 to at most $n$:

$$E[C] = \sum_{i<j} \frac{2}{j-i+1} \le \sum_{i=1}^{n} \sum_{k=2}^{n} \frac{2}{k} \le 2n \ln n$$

The last step holds because $\sum_{k=2}^{n} 1/k = H_n - 1 \le \ln n$, where $H_n = 1 + \tfrac12 + \dots + \tfrac1n$ is the $n$-th harmonic number. So randomized quicksort makes at most $2n \ln n \approx 1.39\, n \log_2 n$ comparisons in expectation. Evaluating the same double sum exactly, instead of bounding it, gives $2(n+1)H_n - 4n$, and the simulation below matches it.

The same exact value comes out of the recurrence for the expected number of comparisons $C(n)$, which averages over the $n$ equally likely pivot ranks $q$:
$$C(n) = (n - 1) + \frac{2}{n} \sum_{q=0}^{n-1} C(q), \qquad C(0) = C(1) = 0$$
The $n - 1$ counts the partition's comparisons, and the factor 2 appears because each size $q$ occurs once as the left side and once as the right side. It gives $C(2) = 1$, $C(3) = 8/3$ and $C(4) = 29/6 \approx 4.83$, the value the example below finds from the pair sum.

```python
import math
import random

def count_comparisons(a):
    """Comparisons made by randomized quicksort on distinct values a."""
    if len(a) <= 1:
        return 0
    pivot = random.choice(a)
    smaller = [x for x in a if x < pivot]
    larger = [x for x in a if x > pivot]
    return len(a) - 1 + count_comparisons(smaller) + count_comparisons(larger)

n, trials = 1000, 100
average = sum(count_comparisons(list(range(n))) for _ in range(trials)) / trials
harmonic = sum(1 / k for k in range(1, n + 1))
print(round(average), round(2 * (n + 1) * harmonic - 4 * n), round(2 * n * math.log(n)))
# about 11000 (varies run to run), 10986 (exact expectation), 13816 (the 2 n ln n bound)
```

> [!example] Worked example · 계산 예제
> For $n = 4$ the sum has six terms. The three adjacent pairs, where $j - i = 1$, each contribute $2/2 = 1$. The two pairs with $j - i = 2$ each contribute $2/3$. The single pair $(z_1, z_4)$ contributes $2/4$. So $E[C] = 3 + 4/3 + 1/2 \approx 4.83$. The exact formula agrees: $2 \cdot 5 \cdot H_4 - 16 = 10 \cdot 25/12 - 16 \approx 4.83$. Adjacent elements are *always* compared, since nothing lies between them to separate them.

**When quicksort is still quadratic.** The worst case remains $\Theta(n^2)$: with random pivots it is simply very unlikely. In practice the quadratic cases come from three sources. A deterministic pivot rule meets sorted or adversarial input. A two-way partition meets **many duplicates**, which random pivots do not fix, because every choice is the same value. And a bad split also means recursion depth $n$, so a Python implementation crashes before it gets slow. The fixes are a random pivot, a three-way partition, and recursing on the smaller side while looping on the larger, which bounds the stack at $O(\log n)$ because each recursive call is on at most half the range.

**Three-way partition for duplicates.** Split the range into three regions, smaller than, equal to, and larger than the pivot (Dijkstra's "Dutch national flag"), and recurse only on the outer two. Precisely, it returns indices $lt \le gt$ with
$$a[i] < p \ \text{ for } lo \le i < lt, \qquad a[i] = p \ \text{ for } lt \le i \le gt, \qquad a[i] > p \ \text{ for } gt < i \le hi$$
so every copy of the pivot is already in its final place and none of them is passed to a recursive call. An array of identical values then finishes after a single O(n) pass, and inputs with few distinct keys become close to linear.

```python
import random

def quicksort(a, lo=0, hi=None):
    """Sort a in place: random pivot, three-way partition. Expected O(n log n)."""
    if hi is None:
        hi = len(a) - 1
    while lo < hi:
        pivot = a[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi        # a[lo:lt] < pivot, a[lt:i] == pivot, a[gt+1:hi+1] > pivot
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1               # do not advance i: the element swapped in is unexamined
            else:
                i += 1
        if lt - lo < hi - gt:         # recurse on the smaller side, loop on the larger,
            quicksort(a, lo, lt - 1)  # so the stack stays O(log n)
            lo = gt + 1
        else:
            quicksort(a, gt + 1, hi)
            hi = lt - 1

data = [3, 1, 3, 3, 9, 0, 3, 2, 3]
quicksort(data)
print(data)                           # [0, 1, 2, 3, 3, 3, 3, 3, 9]
```

**Merge sort or quicksort?** Quicksort sorts in place with $O(\log n)$ stack, scans memory sequentially, and has small constants, so it is usually faster on arrays. It is not stable, and its $O(n \log n)$ bound holds only in expectation. Merge sort is stable and guarantees $O(n \log n)$, at the price of O(n) extra memory. Production sorts combine them: C++ `std::sort` is typically an *introsort*, a quicksort that falls back to heapsort when the recursion gets too deep and uses insertion sort on small ranges. Python's sort is a merge sort (§5).

### 4. The Ω(n log n) lower bound, and how to get under it

A **comparison sort** is a sorting algorithm with one restriction: the only way it uses the keys is to ask, for two items, whether $k(x_i) \le k(x_j)$ (or $<$, or $=$), and everything it does next depends only on those yes/no answers. Equivalently, if two inputs $x$ and $y$ have the same relative order,
$$k(x_i) \le k(x_j) \iff k(y_i) \le k(y_j) \quad \text{for all } i, j,$$
the algorithm performs exactly the same steps on both, so it cannot tell $[1, 5, 3]$ from $[10, 50, 30]$. Merge sort, quicksort, heapsort and insertion sort are all comparison sorts. **Non-example:** counting sort, below, uses a key as an array index, which reads the key's value and not only its order. The claim is that every comparison sort needs $\Omega(n \log n)$ comparisons in the worst case, so merge sort is optimal up to a constant factor.

**The decision-tree argument.** Fix $n$ and any comparison sort, and run it on inputs that are permutations of $n$ distinct values. Draw its behaviour as a binary tree. Each internal node is one comparison, its two children are the two possible outcomes, and each leaf is a finished run, which has determined the rearrangement that sorts the input. Different input permutations need different rearrangements, so they must end at different leaves, and the tree needs at least $n!$ leaves. A binary tree of height $h$ has at most $2^h$ leaves, so $2^h \ge n!$, and the worst-case number of comparisons is $h \ge \log_2 n!$. To see how large that is, keep only the largest $n/2$ factors of $n!$, each of which is at least $n/2$:

$$\log_2 n! \ge \log_2 \left(\frac{n}{2}\right)^{n/2} = \frac{n}{2} \log_2 \frac{n}{2} = \Omega(n \log n)$$

So no comparison sort beats $n \log n$, because it cannot tell $n!$ inputs apart with fewer yes/no answers. The same counting applies to the *average* depth of the leaves, so the bound also holds on average and for randomized comparison sorts.

> [!example] Worked example · 계산 예제
> For $n = 4$ there are $4! = 24$ orderings, so the tree needs at least 24 leaves. $2^4 = 16 < 24 \le 32 = 2^5$, so some input needs at least **5** comparisons. Merge sort on 4 elements uses at most $1 + 1$ comparisons for the two halves and at most 3 for the final merge, 5 in total, so on 4 elements it is exactly optimal. For $n = 5$: $\log_2 120 \approx 6.9$, so at least 7 comparisons are needed.

**Getting under the bound.** The lower bound says nothing about algorithms that look at the keys themselves instead of only comparing them. When the keys are small integers, or can be cut into small digits, you can sort in linear time.

- **Counting sort.** For integer keys in `range(k)`, count how many items have each key. The prefix sums of the counts then give the first output slot for each key, because every item with a smaller key must come before it:
$$\text{start}[v] = \sum_{u < v} \text{count}[u]$$
  Here $\text{count}[u]$ is the number of items whose key is $u$. For keys $2, 0, 2, 1$ the counts are $1, 1, 2$ and the starts are $0, 1, 2$. A left-to-right pass then places the items, which keeps the sort stable. It costs $O(n + k)$ time and space, so it is linear when $k = O(n)$ and useless when $k$ is huge.
- **Radix sort.** Write each key in base $b$ with $d$ digits,
$$x = \sum_{t=0}^{d-1} x_t\, b^t, \qquad x_t = \lfloor x / b^t \rfloor \bmod b$$
  so the digit $x_t$ is what `(x // shift) % base` computes, and 802 in base 10 has $x_0 = 2$, $x_1 = 0$, $x_2 = 8$. Sort by the least significant digit first, then the next digit, and so on, with a *stable* counting sort per digit. After pass $t$, the items are sorted by their last $t$ digits, because stability keeps earlier ties in order. With $d$ digits in base $b$ it costs $O(d(n + b))$. 32-bit keys in base 256 need four linear passes. GPU bounding-volume-hierarchy builders, used for collision checking and ray casting, radix-sort the Morton codes of primitives this way, and an integer voxel index can be sorted the same way to group the points of a cloud by voxel.
- **Bucket sort.** For real keys spread roughly uniformly over $[0, 1)$, drop each item $x$ into bucket $\lfloor n x \rfloor$ of $n$ equal-width buckets (with $n = 4$, the key $0.62$ goes to bucket 2), sort each bucket, and concatenate. Each bucket holds $O(1)$ items in expectation, so the expected time is $O(n)$. If the data are clumped, one bucket gets everything and you are back to the cost of the inner sort.

```python
def counting_sort(items, key, k):
    """Stable sort of items by integer key(item) in range(k). O(n + k)."""
    start = [0] * (k + 1)
    for x in items:
        start[key(x) + 1] += 1
    for v in range(k):                    # prefix sums: start[v] = first output slot for key v
        start[v + 1] += start[v]
    out = [None] * len(items)
    for x in items:                       # a left-to-right pass keeps equal keys in order
        out[start[key(x)]] = x
        start[key(x)] += 1
    return out

def radix_sort(nums, base=256):
    """LSD radix sort of non-negative ints: one stable counting pass per digit."""
    out, shift = list(nums), 1
    while out and shift <= max(out):
        out = counting_sort(out, lambda x: (x // shift) % base, base)
        shift *= base
    return out

print(counting_sort(["b2", "a0", "c2", "d1"], key=lambda s: int(s[1]), k=3))
# ['a0', 'd1', 'b2', 'c2']
print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66], base=10))
# [2, 24, 45, 66, 75, 90, 170, 802]
```

In pure Python these rarely beat the built-in `sorted`, which runs in C; the linear-time sorts pay off in compiled code, in NumPy, and on GPUs. Radix sort as written needs non-negative integers. For negative keys, add an offset first.

### 5. What the library gives you

In real code you will almost never write a sort. You will call one, and the bugs are in how you call it.

**Python.** `list.sort()` sorts in place and returns `None`. `sorted(iterable)` returns a new list. Both use **Timsort**, a merge sort that first finds the runs already present in the data, which are ascending or strictly descending stretches, and merges them in an order that keeps the merges balanced. Since Python 3.11 that merge order follows the *powersort* rule. The consequences you should be able to state:

- **Stable, guaranteed by the language.** You can rely on it, and `reverse=True` keeps stability: equal items stay in their original order rather than being reversed.
- **$O(n)$ on already sorted or reverse-sorted input**, and $O(n \log n)$ in the worst case. It uses up to $n/2$ extra slots for merging.
- **`key=` is called once per item**, and the sort then compares the keys. This is faster and clearer than a comparison function.
- **Tuples compare field by field**, so `key=lambda g: (-g.score, g.time)` means "highest score first, then earliest time". To sort descending by a field you cannot negate, such as a string, use stability: sort by the secondary key, then sort by the primary key with `reverse=True`.
- **A pairwise rule** that no key expresses goes through `functools.cmp_to_key(cmp)`, where `cmp(a, b)` returns a negative number, zero, or a positive number.

```python
import math

grasps = [("g1", 0.82, 1), ("g2", 0.91, 5), ("g3", 0.82, 3), ("g4", 0.91, 2)]  # (name, score, time)

best_then_earliest = sorted(grasps, key=lambda g: (-g[1], g[2]))
print([g[0] for g in best_then_earliest])       # ['g4', 'g2', 'g1', 'g3']

by_name_desc = sorted(grasps, key=lambda g: g[0], reverse=True)       # secondary key first,
by_score_then_name = sorted(by_name_desc, key=lambda g: g[1], reverse=True)  # primary key last
print([g[0] for g in by_score_then_name])       # ['g4', 'g2', 'g3', 'g1']

losses = [0.3, float("nan"), 0.1, 0.2]
print(sorted(losses))                           # [0.3, nan, 0.1, 0.2]  -- not sorted
print(sorted(losses, key=lambda x: (math.isnan(x), x)))   # [0.1, 0.2, 0.3, nan]
```

The last two lines are a real bug in ML code. Every comparison with NaN is `False`, so NaN breaks the ordering the sort relies on, and the output is simply not sorted, without any error. Sorting losses or distances that may contain NaN needs a key that sends NaN to one end. NumPy's `np.sort` does place NaN at the end, but its default algorithm is not stable; pass `kind="stable"` when ties must keep their order.

Two more Python traps. If a key tuple ties on its first fields and the next field is something without an order, such as a dict, the sort raises `TypeError`, so add a tie-breaking index. And `sorted(d)` on a dict sorts the *keys*; use `sorted(d.items(), key=...)` when you need the pairs.

**C++.**

- `std::sort` is **not stable**. It is $O(n \log n)$ and usually an introsort. When equal elements must keep their order, use `std::stable_sort`, which is a merge sort: $O(n \log n)$ with a buffer, and $O(n \log^2 n)$ if it cannot get the extra memory.
- `std::partial_sort` sorts only the first $k$ positions in $O(n \log k)$, and `std::nth_element` performs selection (§7) in average linear time.
- A custom comparator **must be a strict weak ordering**. Write $a \prec b$ for `cmp(a, b)`, and call $a$ and $b$ *incomparable* when neither is less than the other:
$$a \sim b \iff \text{not } a \prec b \ \text{ and } \ \text{not } b \prec a$$
  A strict weak ordering satisfies four named conditions for all $a, b, c$:
  - *irreflexivity*: $a \prec a$ is false, so `cmp(a, a)` is false;
  - *asymmetry*: $a \prec b$ implies that $b \prec a$ is false, so `cmp(a, b)` and `cmp(b, a)` are never both true;
  - *transitivity*: $a \prec b$ and $b \prec c$ imply $a \prec c$;
  - *transitivity of incomparability*: $a \sim b$ and $b \sim c$ imply $a \sim c$.

  Together they make $\sim$ an equivalence relation whose classes, the groups of tied items, are totally ordered by $\prec$, so "sorted" has one meaning. `<` on integers satisfies all four.
- The classic violation is `return a <= b;`. It breaks the first rule, and it is undefined behaviour, not just a wrong order: real implementations can read past the end of the array and crash. Comparing floating-point values that may be NaN, or treating values within an epsilon as "equal", break the same rules. With NaN, $1 \sim \text{NaN}$ and $\text{NaN} \sim 2$, since every comparison with NaN is false, yet $1 < 2$, so incomparability is not transitive.
- For several fields, compare `std::tie(a.x, a.y) < std::tie(b.x, b.y)`, which is lexicographic and correct by construction.

### 6. Binary search done right

**The idea in one sentence:** if a yes/no question about positions is "no" up to some point and "yes" from then on, you can find that point by repeatedly asking in the middle of the range that is still undecided and throwing away the half that cannot contain it.

Almost every binary-search bug is an inconsistency about what `lo` and `hi` mean. Fix one convention and derive every line from it. The one that composes best is the **half-open interval** `[lo, hi)`: `lo` is included, `hi` is not, the range is empty when `lo == hi`, and its size is `hi - lo`. That is the convention of `range`, slices, and C++ iterators.

State the problem as **"find the first position where a monotone predicate becomes true"**: `pred` is False, …, False, True, …, True on `[lo, hi)`, and you want the first True, or `hi` if there is none. Every binary search is this one function with a different predicate.

Precisely, a predicate on the integers of the half-open range $[lo, hi) = \{x : lo \le x < hi\}$ is **monotone** when, once true, it stays true:
$$\text{pred}(x) \implies \text{pred}(y) \quad \text{for all } lo \le x \le y < hi$$
The answer is $x^* = \min\{x \in [lo, hi) : \text{pred}(x)\}$, with $x^* = hi$ when no $x$ makes it true. Monotonicity is what lets one probe discard half the range, because a False at `mid` proves that everything left of `mid` is False. **Non-example:** on `a = [5, 1, 4]` the predicate `a[i] >= 4` is True, False, True, which is not monotone. `first_true` probes index 1, sees False, discards index 0 and returns 2, although index 0 is the first True.

```python
from bisect import bisect_left, bisect_right

def first_true(lo, hi, pred):
    """Smallest x in [lo, hi) with pred(x) True, or hi if none.
    pred must be monotone on [lo, hi): False ... False True ... True."""
    while lo < hi:                  # invariant: the answer lies in [lo, hi]
        mid = (lo + hi) // 2        # lo <= mid < hi, so both branches shrink the range
        if pred(mid):
            hi = mid                # mid may be the answer: keep it
        else:
            lo = mid + 1            # mid is not the answer: drop it
    return lo

a = [2, 4, 4, 4, 7, 9]
lower = first_true(0, len(a), lambda i: a[i] >= 4)    # first index with a[i] >= 4
upper = first_true(0, len(a), lambda i: a[i] > 4)     # first index with a[i] > 4
print(lower, upper, upper - lower)                    # 1 4 3   (three 4s)
assert (lower, upper) == (bisect_left(a, 4), bisect_right(a, 4))
```

**Why it is correct and terminates.** The invariant is that the first True lies in `[lo, hi]`, where the value `hi` stands for "none". It holds at the start. If `pred(mid)` is True, the first True is at `mid` or earlier, so `hi = mid` keeps it. If it is False, then by monotonicity everything up to `mid` is False, so `lo = mid + 1` keeps it. Because `mid < hi`, both branches strictly shrink the range, so the loop ends, with `lo == hi` equal to the answer. It takes $\lceil \log_2(\text{hi} - \text{lo} + 1) \rceil$ steps.

**Lower and upper bound.** For a sorted array, the **lower bound** of `x` is the first index with `a[i] >= x`: where `x` is, or where it would be inserted before any equal items. The **upper bound** is the first index with `a[i] > x`, which is just past the last copy of `x`. As formulas,
$$\text{lower}(x) = \min\{i : a[i] \ge x\}, \qquad \text{upper}(x) = \min\{i : a[i] > x\}$$
with the minimum of an empty set taken as `len(a)`, so both are defined for every `x`. For `a = [2, 4, 4, 4, 7, 9]`: lower(4) = 1, upper(4) = 4, lower(5) = 4 and lower(10) = 6. Everything else follows from these two.

- `x` is present iff `lower < len(a) and a[lower] == x`.
- The number of copies of `x` is `upper - lower`.
- The last index with `a[i] <= x` is `upper - 1`.
- The number of elements in `[x, y)` is `lower(y) - lower(x)`.

**The standard libraries.** Python's `bisect_left` and `bisect_right` are lower and upper bound, and both take `lo`, `hi` and, since 3.10, `key=`. Watch the `key` behaviour: it is applied to the array elements but **not** to `x`, so `x` must already be a key. `insort` finds the position in $O(\log n)$ but inserts in $O(n)$, because the list shifts. C++ has `std::lower_bound`, `std::upper_bound` and `std::equal_range`; `std::partition_point` is exactly `first_true` on a range. `std::binary_search` returns only a `bool`, which is rarely what you need.

**Interview pitfalls.**

- **Mixing conventions.** Writing `while lo <= hi` (closed interval) together with `hi = mid` (half-open update) loops forever when `pred(mid)` is true and `lo == hi`.
- **`lo = mid` with a floor midpoint.** When `hi == lo + 1`, `mid == lo`, so nothing changes. That is why the template always sets `lo = mid + 1`.
- **Overflow in C++ and Java.** `(lo + hi) / 2` can overflow. Write `lo + (hi - lo) / 2`. Python integers do not overflow.
- **Real-valued answers.** Stop after a fixed number of iterations, say 100, instead of testing `hi - lo > eps`, which can loop forever when `eps` is below floating-point resolution.

**Robotics use: bracketing a timestamp.** To estimate a pose or a joint angle at an image's timestamp, find the two buffered samples that bracket it and interpolate between them. The buffer is sorted by time, so this is an upper-bound search. Stamps must be in the same clock, which is the subject of [[04-robotics/ros2/qos-executors-time|25.5 §10]].

```python
from bisect import bisect_right

def interpolate(stamps, values, t):
    """Linearly interpolate values at time t; stamps strictly increasing, len >= 2."""
    if not stamps[0] <= t <= stamps[-1]:
        raise ValueError("t is outside the buffer; refusing to extrapolate")
    k = min(bisect_right(stamps, t), len(stamps) - 1)   # stamps[k-1] <= t <= stamps[k]
    t0, t1 = stamps[k - 1], stamps[k]
    w = (t - t0) / (t1 - t0)
    return (1 - w) * values[k - 1] + w * values[k]

print(interpolate([0.00, 0.10, 0.20, 0.30], [0.0, 1.0, 4.0, 9.0], 0.25))   # 6.5
```

**Binary search on the answer.** Many optimization problems ask for the smallest value $x$ that makes something feasible. If feasibility is **monotone**, meaning that whenever $x$ works every larger $x$ works too,
$$\text{feasible}(x) \implies \text{feasible}(x') \quad \text{for all } x' \ge x,$$
so that the answer $x^* = \min\{x : \text{feasible}(x)\}$ is exactly `first_true` with `feasible` as the predicate, and if *checking* a given $x$ is much easier than finding the best $x$ directly, then binary search over $x$ with the feasibility check as the predicate. The cost is $O(\log(\text{range}))$ checks.

The standard example: packages with weights $w_1, \dots, w_n$ must leave a depot **in the given order**, over at most $D$ days, and each day's load cannot exceed the vehicle's capacity. What is the smallest capacity that works?

- **Checking** a capacity is greedy. Fill each day until the next package would overflow it, then start a new day. The greedy never uses more days than any other plan, because by induction its $k$-th day ends at or after the $k$-th day of any valid plan.
- **Monotone:** a plan that works for capacity $c$ also works for any $c' > c$.
- **Range:** the answer is at least $\max_i w_i$, since the heaviest package must fit, and at most $\sum_i w_i$, which ships everything in one day.

So `first_true(max(w), sum(w) + 1, fits)` finds it with $O(n \log \sum_i w_i)$ work in total.

```python
def first_true(lo, hi, pred):
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def min_capacity(weights, days):
    """Smallest capacity that ships weights, in order, within the given days."""
    def fits(cap):                  # greedy: fill a day until the next item would overflow
        used, load = 1, 0
        for w in weights:
            if load + w > cap:
                used, load = used + 1, 0
            load += w
        return used <= days
    return first_true(max(weights), sum(weights) + 1, fits)

print(min_capacity([3, 2, 2, 4, 1, 4], days=3))   # 6
```

> [!example] Worked example · 계산 예제
> Weights $[3, 2, 2, 4, 1, 4]$ over $D = 3$ days. The range is $[4, 17)$.
> - Capacity 10 fits in two days, $[3, 2, 2]$ and $[4, 1, 4]$, so the answer is at most 10: `hi = 10`.
> - Capacity 7 needs $[3, 2, 2]$, $[4, 1]$, $[4]$, three days, so `hi = 7`.
> - Capacity 5 needs $[3, 2]$, $[2]$, $[4, 1]$, $[4]$, four days, so `lo = 6`.
> - Capacity 6 needs $[3, 2]$, $[2, 4]$, $[1, 4]$, three days, so `hi = 6`.
>
> Now `lo == hi == 6`. Four checks of O(n) each replace trying all 13 capacities.

The same pattern appears in planning. Suppose you want the **largest clearance** a grid path can keep from obstacles. For a clearance $r$, inflate every obstacle by $r$ cells and run BFS ([[02-foundations/algorithms/graph-algorithms|11.6 §2]]). Feasibility is monotone decreasing: a path that keeps clearance $r$ also keeps every smaller clearance. So "no path at clearance $r$" is False…True as $r$ grows, `first_true(0, R + 1, blocked) - 1` is the largest feasible clearance, and the whole search costs $O(\log R)$ BFS runs instead of $R$. A result of $-1$ means that even $r = 0$ has no path.

### 7. Selection: the k-th smallest without sorting

Finding the median, a percentile, or the $k$ smallest items does not require a full sort. Sorting costs $O(n \log n)$; selection can be done in $O(n)$.

**What is being selected.** The **$k$-th smallest element**, or $k$-th order statistic (counting from $k = 0$, as the code does), of $n$ values is the value that would sit at index $k$ after sorting. It can be stated without sorting: it is the value $x$ of the array with
$$\#\{i : a[i] < x\} \le k < \#\{i : a[i] \le x\}$$
because exactly the elements smaller than $x$ come before its first copy, and its copies fill the positions up to $\#\{i : a[i] \le x\} - 1$. The **median** is $k = \lfloor n/2 \rfloor$. For the seven ranges in the code below, $x = 2.8$ has 3 smaller values and 4 values $\le 2.8$, so it is the element at $k = 3$, the median.

**Quickselect.** *The idea in one sentence:* partition around a random pivot as in quicksort, then continue only on the side that contains position $k$.

After a three-way partition, the positions `lt..gt` hold copies of the pivot. If `k` falls among them, the pivot is the answer. If `k < lt`, the answer is on the left; if `k > gt`, it is on the right. The position `k` stays the same because the array is not copied.

**Expected O(n).** A partition of $m$ elements costs $O(m)$. With probability at least 1/2 the random pivot lands in the middle half of the current range, and then the side we keep has at most $3m/4$ elements. Group the rounds into *phases*, where phase $j$ covers the time the range size is between $(3/4)^{j+1} n$ and $(3/4)^j n$. Each round ends the phase with probability at least 1/2, so a phase lasts at most 2 rounds in expectation (flipping a coin until heads: if each try succeeds with probability $p$, the expected number of tries is $1/p$, here $1/(1/2) = 2$), and each round in phase $j$ costs at most $c(3/4)^j n$. So the expected total is

$$E[T(n)] \le \sum_{j \ge 0} 2c \left(\frac{3}{4}\right)^j n = 8cn$$

which is $O(n)$ because the geometric series sums to 4. The worst case is still $\Theta(n^2)$ if every pivot is extreme.

```python
import random

def quickselect(a, k):
    """k-th smallest element of a (k = 0 is the minimum). Expected O(n); a is not modified."""
    a = list(a)
    lo, hi = 0, len(a) - 1
    while True:
        pivot = a[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi          # three-way partition of a[lo..hi], as in quicksort
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return pivot                # positions lt..gt all hold the pivot

ranges = [2.9, 0.4, 5.1, 0.5, 30.0, 0.45, 2.8]   # one spurious long return
print(quickselect(ranges, len(ranges) // 2))     # 2.8, the median; the mean is 6.02
```

**Median of medians: O(n) in the worst case.** Blum, Floyd, Pratt, Rivest and Tarjan (1973) choose the pivot deterministically. Split the elements into groups of 5, take each group's median, and recursively select the median of those $n/5$ medians as the pivot. Half of the group medians are at most this pivot, and each of them is at least as large as two more elements in its group, so the pivot is larger than about $3/10$ of all elements, and by symmetry smaller than about $3/10$. The side that remains has at most about $7n/10$ elements, so $T(n) \le T(n/5) + T(7n/10) + O(n)$ for $n$ above a small constant, with $T(n) = O(1)$ below it. Since $1/5 + 7/10 = 9/10 < 1$, the work per level shrinks geometrically and the total is $O(n)$. It is worth knowing as "selection is linear even in the worst case", but the constant is large, and in practice people use randomized selection or introselect: C++ `std::nth_element`, NumPy `np.partition` and `np.argpartition`.

**Top-k with a heap.** `heapq.nsmallest(k, items, key=...)` (and `nlargest`) keeps a max-heap of the best $k$ items seen so far. Each new item is compared with the heap's top and replaces it if it is better, at $O(\log k)$ cost. That gives $O(n \log k)$ time, $O(k)$ memory, and a result in sorted order. It also works on a stream or iterator that you cannot hold in memory, and it is stable. For $k = 1$ use `min`. When $k$ is close to $n$, `sorted(items)[:k]` is faster. With everything already in a NumPy array, `np.argpartition` gives the top $k$ in $O(n)$, and you sort just those $k$ afterwards if you need them in order.

```python
import heapq
import math

robot = (0.0, 0.0)
obstacles = [(2.0, 1.0), (-0.5, 0.2), (3.0, -4.0), (0.3, 0.4), (1.0, 1.0)]
nearest = heapq.nsmallest(3, obstacles, key=lambda p: math.dist(p, robot))
print(nearest)          # [(0.3, 0.4), (-0.5, 0.2), (1.0, 1.0)]
```

**Where selection is used in robotics.**

- **Median filtering** of range and depth data removes isolated spikes that a mean would smear into their neighbours, as in the quickselect example above.
- **Robust thresholds**, such as the median absolute deviation used to reject outliers before a fit, are selection problems.
- **KD-tree construction** splits at the median coordinate with `nth_element`, which is $O(n)$ per level and $O(n \log n)$ for the whole tree ([[02-foundations/algorithms/data-structures|11.2 §8]]).
- **Brute-force k-nearest neighbours** on a GPU is a distance matrix followed by a top-k.

### 8. Other divide-and-conquer classics worth recognizing

**Fast exponentiation.** *The idea in one sentence:* $x^n = (x^{n/2})^2$ when $n$ is even, and $x \cdot x^{n-1}$ when it is odd, so the exponent halves every other step. Written with its base case,
$$x^n = \begin{cases} 1 & n = 0 \\ (x^{n/2})^2 & n > 0 \text{ even} \\ x \cdot x^{n-1} & n \text{ odd} \end{cases}$$
and every case is valid because multiplication is **associative**, $(ab)c = a(bc)$, so a product of $n$ copies of $x$ may be grouped in any way, and because `one` is an identity, $1 \cdot x = x$. Written as a loop over the bits of $n$, the invariant is that `result * x**n` always equals the original $x_0^{n_0}$. Each step either multiplies the current bit into `result` or squares `x` and halves `n`, so it takes $O(\log n)$ multiplications. The method only needs an associative multiplication with an identity. Subtraction is a non-example: $(8 - 4) - 2 = 2$ but $8 - (4 - 2) = 6$, so regrouping changes the answer. With any associative multiplication, the same loop computes:

- modular powers, which Python's built-in `pow(a, n, m)` already does;
- powers of matrices, which give the $n$-th term of a linear recurrence in $O(\log n)$ matrix products (Fibonacci is the classic);
- $k$-step transition matrices $P^k$ of a Markov chain, or the discrete-time propagation $A^k$ of a linear system. `numpy.linalg.matrix_power` works this way.

Its cost counts multiplications, not bit operations. For huge integers the numbers themselves grow, and each multiplication gets more expensive.

```python
def power(x, n, mul=lambda a, b: a * b, one=1):
    """x**n for integer n >= 0 using O(log n) calls to an associative mul."""
    result = one
    while n > 0:                   # invariant: result * x**n == original x**n
        if n & 1:
            result = mul(result, x)
        x = mul(x, x)
        n >>= 1
    return result

def matmul(A, B):
    cols = list(zip(*B))
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in cols) for row in A)

print(power(3, 13))                                        # 1594323
fib = power(((1, 1), (1, 0)), 10, matmul, ((1, 0), (0, 1)))
print(fib[0][1])                                           # 55, the 10th Fibonacci number
```

**Closest pair of points in 2-D.** Given $n$ points, find two different points $p, q$ that minimize the Euclidean distance $\lVert p - q \rVert = \sqrt{(p_x - q_x)^2 + (p_y - q_y)^2}$. Checking all pairs costs $O(n^2)$. In 1-D you would sort and compare neighbours. In 2-D, divide-and-conquer reaches $O(n \log n)$.

1. **Split.** Sort the points by $x$ and divide them by a vertical line into a left half and a right half.
2. **Recurse.** Find the closest pair in each half, and let $\delta$ be the smaller of the two distances.
3. **Combine.** Any pair closer than $\delta$ that was not found yet must have one point on each side of the line, and both of its points must lie within $\delta$ of the line, since otherwise the horizontal gap alone exceeds $\delta$. So only the **strip** matters, the points within $\delta$ of the dividing line $x = \ell$, which is the set $\{p : \lvert p_x - \ell \rvert < \delta\}$ of width $2\delta$.

The strip can still contain almost every point, so the step that makes the combine linear is a packing argument. Sort the strip's points by $y$. A pair closer than $\delta$ has a $y$-difference below $\delta$. Above any point, cover the $2\delta \times \delta$ rectangle around the line with eight $\delta/2 \times \delta/2$ squares, four on each side. Two points in the same square would be on the same side and at most $\delta/\sqrt{2} < \delta$ apart, which contradicts $\delta$ being the smallest distance within a side. So each square holds at most one point, and each point needs to be compared only with the next **7** points in $y$-order. If you keep the $y$-order by merging, as merge sort does, instead of re-sorting the strip in every call, the combine is $O(n)$ and $T(n) = 2T(n/2) + O(n) = O(n \log n)$. Re-sorting in every call gives $O(n \log^2 n)$. In robotics code, "find all pairs closer than $r$" is usually solved with a grid or spatial hash of cell size $r$, or with a KD-tree. The divide-and-conquer version is the interview example of a combine step that a geometric argument makes linear.

**Karatsuba multiplication.** Split two $n$-digit numbers into high and low halves: with base $B$ (10 for decimal digits) and $m = n/2$, write $x = x_1 B^m + x_0$ and $y = y_1 B^m + y_0$. Their product is
$$xy = z_2 B^{2m} + z_1 B^m + z_0, \qquad z_2 = x_1 y_1, \quad z_0 = x_0 y_0, \quad z_1 = (x_1 + x_0)(y_1 + y_0) - z_2 - z_0$$
where the last identity holds because $(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0$, so subtracting $z_2$ and $z_0$ leaves the middle term $x_1 y_0 + x_0 y_1$. Karatsuba (1962) therefore needs three half-size multiplications instead of four. For $1234 \times 5678$: $z_2 = 12 \cdot 56 = 672$, $z_0 = 34 \cdot 78 = 2652$, $z_1 = 46 \cdot 134 - 672 - 2652 = 2840$, and $672 \cdot 10^4 + 2840 \cdot 10^2 + 2652 = 7006652$. That gives $T(n) = 3T(n/2) + O(n) = O(n^{\log_2 3}) \approx O(n^{1.585})$, which is the algorithm CPython uses for large integers.

### Self-check

1. A merge sort's merge uses `if left[i] < right[j]` instead of `<=`. Is the output still sorted? What property is lost? Give a two-item input where the difference is visible.
2. How many inversions does $[4, 3, 2, 1]$ have? In merge sort's final merge of $[3, 4]$ and $[1, 2]$, which steps add split inversions, and how many does each add?
3. In randomized quicksort on distinct values, what is the probability that the smallest and the largest elements are ever compared? And two elements that are adjacent in sorted order?
4. Randomized quicksort with a Lomuto partition is run on an array of $10^6$ copies of the same value. What is its running time, why does the random pivot not help, and what fixes it?
5. What does the decision-tree argument give as a lower bound on the worst-case comparisons needed to sort 6 elements? Why doesn't counting sort on 16-bit integers contradict the $\Omega(n \log n)$ bound?
6. Using only `first_true`, find the last index $i$ with `a[i] <= x` in a sorted array, and say what it returns when every element is larger than `x`.
7. A C++ program sorts with `std::sort(v.begin(), v.end(), [](double a, double b) { return a <= b; });` and crashes only on some inputs. Explain why, and name a second way the same comparator could break even with `<`.
8. You need the 100 largest scores from a stream of $10^8$ detections that does not fit in memory. Compare `heapq.nlargest`, sorting, and quickselect in time and memory. Which one can you actually use?
9. In the closest-pair combine step, why is it enough to compare each strip point with the next 7 points in $y$-order, and what would the running time be if you compared it with every point in the strip?

> [!tip]- Answers
> 1. Yes, it is still sorted: on a tie, taking the right element first still outputs the smaller-or-equal element. It is no longer stable. With `key` comparing the second field, the input `[("a", 1), ("b", 1)]` splits into `[("a", 1)]` and `[("b", 1)]`, and `<` is false on the tie, so the merge outputs `("b", 1)` first, reversing the two equal items.
> 2. Six, since the array is reversed and all $\binom{4}{2} = 6$ pairs are inversions. Each half contributes one: $[4, 3]$ and $[2, 1]$. In the final merge, 1 is output from the right while $[3, 4]$ waits, adding 2. Then 2 is output from the right while $[3, 4]$ still waits, adding 2 more. Outputting 3 and 4 adds nothing. So $1 + 1 + 4 = 6$.
> 3. For $z_1$ and $z_n$ the set between them is the whole array, so the probability is $2/n$: they are compared only if one of them is the very first pivot. For adjacent $z_i, z_{i+1}$ it is $2/2 = 1$. Nothing lies between them, so they stay together until one becomes the pivot, which is then compared with the other.
> 4. $\Theta(n^2)$, about $5 \times 10^{11}$ comparisons, and in a recursive Python implementation a recursion-depth crash long before that. Every pivot has the same value, so a two-way partition puts all other $n - 1$ elements on one side no matter which element is chosen. Randomness chooses among elements, but all the elements are equal. A three-way partition fixes it: the "equal" region absorbs the whole array in one O(n) pass.
> 5. $\lceil \log_2 720 \rceil = 10$, since $2^9 = 512 < 720 \le 1024$. Counting sort is not a comparison sort. It indexes an array by the key value, so each step gets far more than one bit of information about the input, and the decision-tree model does not apply. Its cost is $O(n + k)$ with $k = 65536$.
> 6. `first_true(0, len(a), lambda i: a[i] > x) - 1`, which is `bisect_right(a, x) - 1`. The first element greater than `x` is just past the last element that is `<= x`. If every element is greater than `x`, `first_true` returns 0, so the result is $-1$, meaning "no such index". Check for that before using it as an index, because in Python `a[-1]` silently reads the last element.
> 7. `a <= b` is true when `a == b`, so `cmp(a, a)` is true. That violates irreflexivity, one of the strict weak ordering requirements, and the behaviour is undefined: the implementation's partition loop can step past the range because it assumes an element is never "less than" itself. Even with `a < b`, the comparator breaks if the data contain NaN, because NaN is incomparable to every value while those values are comparable to each other, so "incomparable" is no longer transitive. Filter NaNs out first, or order them explicitly.
> 8. `heapq.nlargest(100, stream)`: $O(n \log k)$, about $10^8 \times 7$ cheap operations, with only 100 items in memory, and it consumes the iterator. Sorting needs all $10^8$ items in memory and $O(n \log n)$ time. Quickselect is $O(n)$ expected but also needs the whole array in memory, so it is not usable on the stream. The heap is the one to use.
> 9. Above a given strip point, any point closer than $\delta$ lies in a $2\delta \times \delta$ rectangle. That rectangle is covered by 8 squares of side $\delta/2$, and each square holds at most one point, since two points in one square would be on the same side at distance $\le \delta/\sqrt{2} < \delta$. So the rectangle holds at most 8 points, counting the point itself, and at most 7 others need checking. Comparing with every strip point costs up to $O(n^2)$ per combine when the strip holds most points, so the whole algorithm degrades to $O(n^2)$.

### Sources

- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — merge sort, quicksort and its randomized analysis, the sorting lower bound, counting/radix/bucket sort, medians and order statistics, closest pair.
- Roughgarden, *Algorithms Illuminated, Part 1: The Basics*, Soundlikeyourself Publishing, 2017 — divide-and-conquer, counting inversions, closest pair, the master method, quicksort's indicator-variable analysis, randomized and deterministic selection, the sorting lower bound.
- Kulikov & Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — chapter on divide-and-conquer: binary search with duplicates, three-way quicksort, inversions, closest points.
- Knuth, D. E. *The Art of Computer Programming, Vol. 3: Sorting and Searching*, 2nd ed., Addison-Wesley, 1998.
- Hoare, C. A. R. "Algorithm 64: Quicksort" and "Algorithm 65: Find." *Communications of the ACM* 4(7), 1961.
- Hoare, C. A. R. "Quicksort." *The Computer Journal* 5(1), 1962. doi:10.1093/comjnl/5.1.10
- Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L. & Tarjan, R. E. "Time bounds for selection." *Journal of Computer and System Sciences* 7(4), 1973. doi:10.1016/S0022-0000(73)80033-9
- Bentley, J. L. & McIlroy, M. D. "Engineering a sort function." *Software: Practice and Experience* 23(11), 1993 — three-way partitioning in a production sort.
- Dijkstra, E. W. *A Discipline of Programming*, Prentice-Hall, 1976 — the Dutch national flag problem.
- Kendall, M. G. "A new measure of rank correlation." *Biometrika* 30(1/2), 1938.
- Knight, W. R. "A computer method for calculating Kendall's tau with ungrouped data." *Journal of the American Statistical Association* 61(314), 1966.
- Shamos, M. I. & Hoey, D. "Closest-point problems." *IEEE Symposium on Foundations of Computer Science (FOCS)*, 1975.
- Karatsuba, A. & Ofman, Yu. "Multiplication of multidigit numbers on automata." *Soviet Physics Doklady* 7, 1963 (Russian original 1962).
- Munro, J. I. & Wild, S. "Nearly-optimal mergesorts: Fast, practical sorting methods that optimally adapt to existing runs." *European Symposium on Algorithms (ESA)*, 2018 — powersort.
- Bentley, J. *Programming Pearls*, 2nd ed., Addison-Wesley, 2000 — writing a correct binary search.

## 한국어

정렬은 알고리즘에서 가장 많이 연구된 문제이고, 인터뷰 준비에는 그 점이 지루함이 아니라 쓸모다. 분할 정복에 필요한 아이디어가 모두 가장 단순한 형태로 정렬 안에 들어 있다. 병합 정렬은 일을 합치는 단계에 두고, 퀵정렬은 나누는 단계에 둔다. 하한은 더 빠른 방법을 찾는 일을 언제 멈춰야 하는지 알려 주고, 이진 탐색·선택·최근접 쌍은 같은 수를 다른 문제에 다시 쓴다.

인터뷰가 묻는 것: 병합 정렬이나 퀵정렬을 버그 없이 쓰고 왜 맞는지 설명하기, 퀵정렬이 왜 *기댓값으로* $O(n \log n)$이고 언제 이차 시간이 되는지 말하기, 역순쌍 세기, 라이브러리 정렬을 올바르게 쓰기(안정성, key, 비교자), off-by-one 없는 이진 탐색과 "답에 대한 이진 탐색", 전부 정렬하지 않고 k번째 원소나 상위 k개 찾기. 연구실 인터뷰는 로보틱스 버전을 더한다: 메디안 필터, 중앙값 분할로 만드는 KD-tree, 타임스탬프 순으로 센서 스트림 병합하기, 임의의 시각에서 신호 보간하기.

> [!note] 처음이라면 · First pass
> §1, §2, §3, §6을 먼저 읽어라. 대부분의 문제가 시험하는 내용이다. §5는 실제 코드에서 언젠가 만나게 될 라이브러리 버그를 막아 준다. §4와 §7은 "왜 더 빨라질 수 없나"와 "원소 하나만 필요하다"는 질문이다. §8은 고전 문제가 나왔을 때 알아보기 위한 절이다.

### 1. 분할 정복의 모양

**한 문장 아이디어:** 입력을 같은 문제의 더 작은 사례로 나누고, 그것을 재귀로 풀고, 그 답들을 합쳐 전체의 답을 만든다.

모든 분할 정복 알고리즘은 세 질문에 답해야 하고, 인터뷰어는 세 가지를 모두 묻는다.

1. **어떻게 나누고, 기저 사례는 무엇인가?** 조각은 반드시 더 작아야 한다. 그렇지 않으면 재귀가 끝나지 않는다. 크기 0이나 1의 기저 사례면 거의 언제나 충분하다.
2. **합친 답이 왜 맞는가?** 논증은 입력 크기에 대한 귀납법이다. 재귀 호출이 더 작은 조각에 대해 맞는 답을 돌려준다고 *가정*하고, 합치는 단계가 그것을 전체에 대한 맞는 답으로 바꾼다는 것을 보인다. 증명하려고 재귀를 따라가 볼 필요는 없다.
3. **나누기와 합치기의 비용은 얼마인가?** 그 비용과 조각의 개수·크기가 점화식이 된다. [[02-foundations/algorithms/complexity-recursion|11.1 §3]]의 재귀 트리나 마스터 방법으로 푼다.

**정확한 정의.** 분할 정복은 알고리즘 하나가 아니라 알고리즘 설계 패러다임이다. 다음 세 부분을 모두 갖춘 알고리즘이 여기에 속한다.

- **나누기**(divide): 기저 크기 $n_0$보다 큰 크기 $n$의 사례를 *같은* 문제의 사례 $a \ge 1$개로 바꾸며, 각 사례는 $n$보다 엄격히 작다.
- **정복**(conquer): 각 조각을 재귀 호출로 푼다. 크기 $n \le n_0$인 사례는 **기저 사례**(base case)이며 재귀 없이 직접 푼다.
- **합치기**(combine): 조각 $a$개의 답으로 전체의 답을 만든다.

모든 조각의 크기가 상수 $b > 1$에 대해 $n/b$이면, 전체 비용은 재귀 호출 $a$번에 재귀 바깥의 나누기·합치기 작업을 더한 것이므로 실행 시간은 다음 점화식을 만족한다.
$$T(n) = a\,T(n/b) + f(n) \ \text{ for } n > n_0, \qquad T(n) = \Theta(1) \ \text{ for } n \le n_0$$
여기서 $a$는 조각 수, $n/b$는 조각 하나의 크기, $f(n)$은 크기 $n$에서 나누고 합치는 비용, $n_0$는 가장 큰 기저 사례 크기이며 보통 1이다. 병합 정렬은 $a = 2$, $b = 2$, $f(n) = \Theta(n)$이고, 이진 탐색은 $a = 1$, $b = 2$, $f(n) = \Theta(1)$이다. 불균형한 분할은 §3의 퀵정렬이 $T(q) + T(n - 1 - q)$로 쓰듯 실제 조각 크기를 적는다. 기호 $O$, $\Omega$, $\Theta$는 [[02-foundations/algorithms/complexity-recursion|11.1 §2]]에서 정의한다.

**반례.** 피보나치 수의 재귀 $F(n) = F(n-1) + F(n-2)$도 같은 문제의 더 작은 사례로 나누지만, $F(n-1)$이 $F(n-2)$를 다시 부르므로 조각이 겹친다. 그래서 단순한 재귀는 서로 다른 인자가 31개뿐인데도 $F(30)$을 계산하려고 2,692,537번 호출한다. 이것은 쓸모 있는 분할 정복이 아니라 아래에서 말하는 동적 계획법의 경우다.

이 페이지의 모든 알고리즘은 아래 표의 한 줄이다. 이름과 함께 점화식을 외워라. "점화식이 뭔가?"라고 묻는 것이 새로운 분할 정복 아이디어를 30초 만에 복잡도로 바꾸는 방법이다.

| 알고리즘 | 점화식 | 비용 | 이유 |
|---|---|---|---|
| 이진 탐색 (§6) | $T(n) = T(n/2) + O(1)$ | $\Theta(\log n)$ | 조각 하나, 상수 작업, $\log_2 n$ 레벨 |
| 병합 정렬 (§2) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | 레벨마다 $O(n)$ |
| 퀵정렬, 중앙값 피벗 (§3) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | 같은 모양; 무작위 피벗은 기댓값으로 이것을 준다 |
| 퀵정렬, 최악 피벗 (§3) | $T(n) = T(n-1) + O(n)$ | $\Theta(n^2)$ | 조각이 절반이 아니라 하나씩 줄어든다 |
| Quickselect, 좋은 피벗 (§7) | $T(n) = T(3n/4) + O(n)$ | $\Theta(n)$ | 작업이 기하급수로 줄어 루트가 지배 |
| Median of medians (§7) | $T(n) = T(n/5) + T(7n/10) + O(n)$ | $\Theta(n)$ | $1/5 + 7/10 < 1$이라 레벨이 줄어든다 |
| 빠른 거듭제곱 (§8) | $T(n) = T(n/2) + O(1)$ | 곱셈 $\Theta(\log n)$번 | 지수를 반으로 |
| 최근접 쌍 (§8) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ | 띠 스캔이 선형 |
| Karatsuba (§8) | $T(n) = 3T(n/2) + O(n)$ | $\Theta(n^{\log_2 3})$ | 리프가 지배 |

**분할 정복이 맞지 않는 경우.** 조각이 *겹치면*, 즉 같은 부분 문제에 여러 경로로 도달하면, 단순한 재귀는 같은 일을 지수적으로 반복한다. 그것이 동적 계획법의 신호다([[02-foundations/algorithms/dynamic-programming|11.5 §1]]). 병합 정렬의 두 절반은 원소를 공유하지 않으므로 캐시할 것이 없다.

**복잡도를 바꾸는 Python 함정 두 가지.**

- **슬라이싱은 복사다.** `a[mid:]`는 O(n)이다. 병합 정렬 안에서는 어차피 합치기가 O(n)이므로 해가 없다. 이진 탐색 안에서는 $O(\log n)$을 $O(n)$으로 만든다. 재귀 바깥의 작업이 선형보다 작아야 할 때는 슬라이스 대신 인덱스 `lo, hi`를 넘겨라.
- **재귀 깊이.** CPython의 기본 한도는 1000 프레임이다. 균형 잡힌 분할은 깊이가 $\log_2 n$, 10억 개 원소에서도 30 정도라 안전하다. 나쁜 피벗의 퀵정렬처럼 불균형한 분할은 깊이가 $n$이 되어, 느려지기 훨씬 전에 죽는다. 해결책은 §3에 있다.

### 2. 병합 정렬, 그리고 덤으로 역순쌍 세기

**한 문장 아이디어:** 왼쪽 절반을 정렬하고 오른쪽 절반을 정렬한 뒤, 두 정렬된 절반의 맨 앞 원소 중 작은 것을 반복해서 꺼내 병합한다.

**병합 불변식.** 포인터 `i`, `j`로 `left`와 `right`를 병합하는 동안, 출력에는 항상 두 리스트 전체에서 가장 작은 `i + j`개 원소가 정렬된 순서로 들어 있다. 두 입력이 정렬되어 있으므로 이 성질이 유지된다. `left[i]`는 `left`에 남은 것 중 최소이고 `right[j]`는 `right`에 남은 것 중 최소이므로, 둘 중 작은 것이 남은 전체의 최소다. 한쪽이 바닥나면 다른 쪽의 나머지는 이미 정렬되어 있고 출력된 모든 것보다 크므로 한꺼번에 붙인다. 정렬 전체의 정당성은 §1의 귀납법으로 따라온다. 재귀 호출이 두 절반을 정렬하면, 병합이 정렬된 전체를 만든다.

**시간: 모든 입력에서 $\Theta(n \log n)$.** 재귀 트리는 $\log_2 n$ 레벨이다. 각 레벨의 조각들은 배열 전체를 나눠 가지고, 총길이 $n$인 조각들을 병합하는 비용은 O(n)이다. 그러므로 레벨당 $n$에 레벨 수 $\log_2 n$을 곱한 것이 전체다. 입력 순서와 무관하다. 정렬된 입력, 역순, 무작위 입력의 비용이 모두 같고, 보장이 필요할 때는 이것이 장점이다. 총길이 $n$의 병합에 $n$을 매겨 기저 사례와 함께 점화식으로 쓰면 다음과 같다.
$$T(n) = 2\,T(n/2) + n \ \text{ for } n \ge 2, \qquad T(1) = 1$$
$n$이 2의 거듭제곱이면 병합 레벨 $\log_2 n$개가 각각 $n$을, 원소 하나짜리 리프 $n$개가 각각 1을 더하므로 정확히 $T(n) = n \log_2 n + n$이다. 예를 들어 $T(8) = 2\,T(4) + 8 = 2 \cdot 12 + 8 = 32 = 8 \cdot 3 + 8$이다.

**공간: 추가 O(n).** 병합은 두 입력 크기만 한 버퍼에 쓴다. 재귀 스택이 $O(\log n)$을 더한다. 제자리 병합도 가능하지만 복잡하고 느려서, 인터뷰에서는 O(n)이면 된다. **연결 리스트** 위에서는 병합이 복사가 아니라 노드 연결을 바꾸는 일이므로 추가 공간이 O(1)이고, 그래서 연결 리스트 정렬의 표준 방법이다.

**안정성.** 먼저 모든 정렬이 내놓아야 하는 것부터. 키 $k(x_i)$를 가진 항목 $x_1, \dots, x_n$이 주어지면, 정렬은 키를 감소하지 않는 순서 $k(x_{\pi(1)}) \le k(x_{\pi(2)}) \le \dots \le k(x_{\pi(n)})$로 놓는 위치의 순열 $\pi$를 출력한다. 키가 겹치면 그런 순열이 여러 개다. 그중 키가 같은 항목들이 입력 순서를 유지하는 것을 언제나 내놓는 정렬을 **안정 정렬**(stable)이라 한다.
$$i < j \ \text{ and } \ k(x_i) = k(x_j) \implies \pi^{-1}(i) < \pi^{-1}(j)$$
여기서 $\pi^{-1}(i)$는 입력 항목 $i$의 출력 위치다. 즉 키가 같은 두 항목 중 입력에서 먼저 온 것이 출력에서도 먼저 온다는 조건이다. 아래 코드에서 `("lidar", 3)`이 `("cam", 3)` 앞에 남는 것이 그 예다. 병합 정렬은 동점일 때 왼쪽에서 가져와야만 안정적이다. 아래 비교가 `<`가 아니라 `<=`인 이유다.

- **반례.** 남은 것 중 가장 작은 항목을 앞으로 스왑하는 선택 정렬은 안정적이지 않다. $[(2, a), (2, b), (1, c)]$를 숫자로 정렬하면 첫 스왑이 $(2, a)$와 $(1, c)$를 맞바꿔 $[(1, c), (2, b), (2, a)]$가 되고, $a$와 $b$의 순서가 바뀐다. 퀵정렬과 힙 정렬도 안정적이지 않다.
- **왜 중요한가.** 같은 키의 순서에 정보가 담겨 있을 때마다 안정성이 중요하다. 이미 타임스탬프 순인 검출 결과를 클래스별로 정렬하면, 안정 정렬은 각 클래스 안의 시간 순서를 공짜로 지켜 준다. 여러 키로 차례차례 정렬하는 방법(§5)과 기수 정렬의 정당성(§4)도 안정성에 기댄다.

```python
def merge_sort(a, key=lambda x: x):
    """Return a new list with the items of a sorted by key. Stable."""
    if len(a) <= 1:
        return list(a)
    mid = len(a) // 2
    left, right = merge_sort(a[:mid], key), merge_sort(a[mid:], key)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):     # ties go left: this is what makes it stable
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])                      # at most one of these two is non-empty
    out.extend(right[j:])
    return out

print(merge_sort([5, 2, 9, 2, 7, 1]))         # [1, 2, 2, 5, 7, 9]
events = [("lidar", 3), ("imu", 1), ("cam", 3), ("imu", 2), ("lidar", 1)]
print(merge_sort(events, key=lambda e: e[1])) # equal times keep input order
# [('imu', 1), ('lidar', 1), ('imu', 2), ('lidar', 3), ('cam', 3)]
```

같은 병합을 힙으로 $k$개의 정렬된 스트림에 한꺼번에 적용하면, 시간 순서인 센서 로그 여러 개를 하나로 합칠 수 있다. `heapq.merge(*streams, key=...)`는 전체 레코드 $N$개에 대해 $O(N \log k)$이고 스트림을 지연 읽기한다. 데이터가 메모리에 들어가지 않을 때 쓰는 **외부 정렬** 기법의 핵심도 이것이다. 메모리에 들어가는 덩어리를 정렬해 파일로 쓰고, 그 파일들을 k-way 병합한다.

**역순쌍 세기.** 수열 $a[1], \dots, a[n]$의 **역순쌍**(inversion)은 $i < j$이면서 값의 순서가 뒤집힌, 즉 $a[i] > a[j]$인 위치 쌍이다. 역순쌍 개수는 그런 쌍의 수다.
$$\operatorname{inv}(a) = \big|\{(i, j) : 1 \le i < j \le n,\ a[i] > a[j]\}\big|$$
부등호가 엄격하므로 같은 값끼리는 역순쌍이 되지 않는다. $[2, 2]$에는 하나도 없다. 정렬된 배열은 $\operatorname{inv}(a) = 0$이고, 서로 다른 값의 역순 배열은 모든 쌍이 뒤집혀 있으므로 $n(n-1)/2$개 전부를 가진다. 그래서 그 개수는 수열이 정렬 상태에서 얼마나 먼지를 잰다. 작업량도 센다. 삽입 정렬은 이웃한 뒤집힌 원소만 스왑하고 그런 스왑 한 번이 역순쌍을 정확히 하나 없애므로, 정확히 $\operatorname{inv}(a)$번 스왑한다. 아래 $[3, 1, 4, 2]$라면 3번이다. 모든 쌍을 확인하면 $O(n^2)$이다. 병합 정렬은 한 줄을 더해 $O(n \log n)$에 센다.

역순쌍을 왼쪽 절반 안의 것, 오른쪽 절반 안의 것, 그리고 양쪽에 하나씩 걸친 **분할 역순쌍**(split inversion)으로 나눈다. 앞의 두 개수는 재귀 호출이 돌려준다. 세 번째는 병합을 보면 된다. 왼쪽 원소 $x$와 오른쪽 원소 $y$가 역순쌍인 것은 정확히 $x > y$일 때이고, 그것은 정확히 $y$가 $x$보다 먼저 출력될 때다. 따라서 병합이 `right[j]`를 출력할 때 `left`에서 아직 기다리는 모든 원소가 그것과 역순쌍을 이루며, 그 수는 `len(left) - i`개다. 그런 단계마다 이 수를 더하면 O(n) 병합 안에서 분할 역순쌍이 모두 세어지므로, 점화식은 여전히 $T(n) = 2T(n/2) + O(n)$이다.

> [!example] 계산 예제 · Worked example
> $[3, 1, 4, 2]$의 역순쌍을 센다. 왼쪽 절반 $[3, 1]$에는 역순쌍이 하나 있고 $[1, 3]$으로 정렬된다. 오른쪽 절반 $[4, 2]$에도 하나 있고 $[2, 4]$로 정렬된다. 이제 $[1, 3]$과 $[2, 4]$를 병합한다.
> - 왼쪽에서 1을 출력한다. 더할 것 없음.
> - 왼쪽에 $[3]$이 기다리는 동안 오른쪽에서 2를 출력한다. 1을 더한다: 쌍 (3, 2).
> - 3, 그다음 4를 출력한다. 더할 것 없음.
>
> 합계: $1 + 1 + 1 = 3$. 모든 쌍을 나열해 확인: (3, 1), (3, 2), (4, 2).

**쓰이는 곳: 순위 일치도.** 같은 $n$개 항목에 대한 두 순위가 있다고 하자. 시뮬레이터가 매긴 정책 체크포인트 열 개의 순위와 실제 로봇 성공률의 순위, 또는 학습된 보상 모델이 매긴 궤적 순위와 사람이 매긴 순위. 두 순위가 어떤 쌍을 같은 순서로 두면 그 쌍은 **일치**(concordant), 아니면 **불일치**(discordant)다. 두 순위에서 항목 $x$의 위치를 $r_A(x)$, $r_B(x)$라 하면, 쌍 $x, y$는 $(r_A(x) - r_A(y))(r_B(x) - r_B(y)) > 0$일 때 일치, 그 곱이 음수일 때 불일치이며, 0은 동점일 때뿐이다. Kendall의 tau는 일치 쌍의 비율에서 불일치 쌍의 비율을 뺀 값이다.

$$\tau = \frac{C - D}{n(n-1)/2} = 1 - \frac{4D}{n(n-1)}$$

여기서 $C$는 일치 쌍의 수, $D$는 불일치 쌍의 수, $n(n-1)/2$는 항목 $n$개에서 나오는 쌍의 수다. 동점이 없으면 모든 쌍이 둘 중 하나이므로 $C + D = n(n-1)/2$이고, 그래서 두 번째 형태가 나온다. $\tau = 1$이면 순서가 같고, $\tau = -1$이면 정반대다. 핵심 관찰은 $D$가 역순쌍 개수라는 점이다. 항목들을 첫 번째 순위 순서로 늘어놓고 각 항목의 두 번째 순위 위치를 적으면, 불일치 쌍이 정확히 그 리스트의 역순쌍이다. 예를 들어 항목 A, B, C, D를 첫 번째 순위 순서로 두고, 두 번째 순위가 이들을 위치 3, 1, 4, 2에 놓는다고 하자. 불일치 쌍은 위에서 센 $[3, 1, 4, 2]$의 역순쌍 세 개이므로 $D = 3$, $C = 6 - 3 = 3$, $\tau = (3 - 3)/6 = 0$이다. 두 순위가 일치하는 쌍과 어긋나는 쌍의 수가 같다는 뜻이다. 그러므로 Kendall tau는 $O(n^2)$이 아니라 $O(n \log n)$에 계산된다(Knight, 1966). 동점이 있으면 tau-b 보정을 쓴다. `scipy.stats.kendalltau`의 기본값이 그것이다.

```python
def sort_and_count(a):
    """Return (sorted copy of a, number of pairs i < j with a[i] > a[j])."""
    if len(a) <= 1:
        return list(a), 0
    mid = len(a) // 2
    left, inv_left = sort_and_count(a[:mid])
    right, inv_right = sort_and_count(a[mid:])
    out, i, j, split = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:                      # right[j] jumps ahead of every left item still waiting
            out.append(right[j])
            j += 1
            split += len(left) - i
    out += left[i:] + right[j:]
    return out, inv_left + inv_right + split

def kendall_tau(rank_a, rank_b):
    """Kendall tau of two rankings without ties; rank_x[item] is item's position."""
    n = len(rank_a)
    order = sorted(range(n), key=lambda item: rank_a[item])   # items in A's order
    _, discordant = sort_and_count([rank_b[item] for item in order])
    return 1 - 4 * discordant / (n * (n - 1))

print(sort_and_count([3, 1, 4, 2])[1])                        # 3
print(kendall_tau([0, 1, 2, 3, 4], [1, 0, 2, 4, 3]))          # 0.6
```

> [!example] 계산 예제 · Worked example
> 체크포인트 A–E의 실제 로봇 성공률 순서가 A, B, C, D, E(좋은 순)다. 시뮬레이터는 B, A, C, E, D로 매긴다. 따라서 A부터 E까지 인덱스로 `rank_a = [0, 1, 2, 3, 4]`(실제), `rank_b = [1, 0, 2, 4, 3]`(시뮬레이터)이다. 실제 순서로 늘어놓은 시뮬레이터 위치는 $[1, 0, 2, 4, 3]$이고, 역순쌍은 (A, B)와 (D, E) 두 개다. 따라서 $D = 2$, $C = 10 - 2 = 8$, $\tau = (8 - 2)/10 = 0.6$이다. 시뮬레이터는 상위 세 개를 집합으로는 맞게 고르지만, 이웃한 체크포인트끼리의 순위는 믿으면 안 된다.

**인터뷰 함정.**

- 병합에서 `left.pop(0)`은 호출마다 O(n)이라 정렬이 이차 시간이 된다. 인덱스를 쓰거나 `collections.deque`의 `popleft`를 써라.
- 병합에서 `<`를 쓰면 정렬은 되지만 안정성이 조용히 사라진다.
- 역순쌍 개수에는 `len(left)`나 `mid - j`가 아니라 아직 기다리는 항목 수인 `len(left) - i`를 더한다.

### 3. 퀵정렬: 파티션, 무작위 피벗, 그리고 빠른 이유

**한 문장 아이디어:** 피벗을 하나 고르고, 더 작은 원소는 앞으로, 더 큰 원소는 뒤로 오도록 배열을 재배치한 뒤, 양쪽을 재귀로 정렬한다.

병합 정렬이 나누기는 거저 하고 합치기에서 일을 한다면, 퀵정렬은 나누기, 즉 **파티션**(partition) 단계에서 일을 하고 합치기가 아예 없다. 피벗 값 $p$에 대한 범위 $a[lo..hi]$의 파티션은 범위를 재배치하고 다음을 만족하는 인덱스 $q$를 돌려준다.
$$a[i] \le p \ \text{ for } lo \le i < q, \qquad a[q] = p, \qquad a[i] \ge p \ \text{ for } q < i \le hi$$
앞의 모든 원소가 크지 않고 뒤의 모든 원소가 작지 않으므로, 피벗은 이미 정렬된 배열에서 가질 수 있는 인덱스에 있다. 아래 Lomuto 방식은 왼쪽에 더 엄격한 $<$로 이것을 만족하고, Hoare 방식은 피벗을 $q$에 고정하지 않는 약한 형태를 만족한다. 양쪽이 제자리에서 정렬되면 배열 전체가 정렬된 것이다. 정당성은 §1과 같은 귀납법이다. 파티션 후 피벗은 최종 위치에 있고, 그 왼쪽의 모든 원소는 왼쪽에 속하며, 재귀 호출이 각 쪽을 정렬한다.

**Lomuto 파티션.** 마지막 원소를 피벗으로 쓰고, 경계 인덱스 `i` 하나를 두고 왼쪽에서 오른쪽으로 훑는다. 불변식은 `a[lo:i]`에는 피벗보다 작은 원소가, `a[i:j]`에는 그렇지 않은 원소가 있다는 것이다. `a[j]`가 피벗보다 작으면 위치 `i`로 스왑하고 `i`를 늘린다. 끝나면 피벗을 위치 `i`로 스왑하며, 그곳이 최종 자리다. Lomuto는 올바르게 쓰기 가장 쉽고 피벗의 인덱스를 돌려주므로 quickselect(§7)에 맞는다. 다만 Hoare 방식보다 스왑이 많고, 양방향 비교만으로는 피벗과 같은 원소가 많을 때 $\Theta(n^2)$로 나빠진다. 값이 모두 같은 배열은 모든 레벨에서 $n - 1$과 $0$으로 갈라진다.

**Hoare 파티션.** Hoare의 원래 방식(1961)은 양 끝에서 두 인덱스를 서로를 향해 움직인다. 왼쪽 인덱스는 피벗보다 작지 않은 원소에서, 오른쪽 인덱스는 피벗보다 크지 않은 원소에서 멈추고, 두 원소를 스왑한다. 인덱스가 교차하면 `a[lo..j]`의 모든 원소가 피벗 이하이고 `a[j+1..hi]`의 모든 원소가 피벗 이상인 `j`를 돌려준다. 피벗이 `j`에 있다는 보장은 *없으므로*, 재귀 호출은 `[lo, j]`와 `[j+1, hi]`에 대해 하고 어느 쪽도 피벗을 빼지 않는다. Hoare는 보통 Lomuto보다 스왑이 적고, 값이 모두 같은 배열도 가운데에서 가른다. Lomuto는 이 경우 이차 시간으로 나빠진다. 함정은 피벗이 `a[hi]`이면 안 된다는 점이다. 그러면 `j`가 `hi`로 돌아올 수 있고, 재귀 호출이 같은 범위를 다시 받아 끝나지 않는다. 가운데 원소를 쓰거나, 무작위 원소를 `lo`로 스왑해 두어라.

```python
def lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around a[hi]; return the pivot's final index."""
    pivot, i = a[hi], lo              # invariant: a[lo:i] < pivot <= a[i:j]
    for j in range(lo, hi):
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i

def hoare_partition(a, lo, hi):
    """Return j with a[lo..j] <= pivot <= a[j+1..hi]; the pivot need not sit at j."""
    pivot = a[(lo + hi) // 2]         # never a[hi]: j could equal hi and recurse forever
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]

a = [4, 7, 2, 9, 1, 5]
print(lomuto_partition(a, 0, 5), a)   # 3 [4, 2, 1, 5, 7, 9]
b = [4, 7, 2, 9, 1, 5]
print(hoare_partition(b, 0, 5), b)    # 1 [1, 2, 7, 9, 4, 5]
```

> [!example] 계산 예제 · Worked example
> $[4, 7, 2, 9, 1, 5]$에 피벗 5로 Lomuto를 적용한다. 시작은 `i = 0`.
> - `j=0`: 4 < 5, `a[0]`을 자기 자신과 스왑, `i = 1`.
> - `j=1`: 7은 작지 않으므로 아무 일도 없다.
> - `j=2`: 2 < 5, `a[1]`과 `a[2]`를 스왑해 $[4, 2, 7, 9, 1, 5]$, `i = 2`.
> - `j=3`: 9, 아무 일도 없다.
> - `j=4`: 1 < 5, `a[2]`와 `a[4]`를 스왑해 $[4, 2, 1, 9, 7, 5]$, `i = 3`.
>
> 마지막으로 피벗을 `a[3]`으로 스왑하면 $[4, 2, 1, 5, 7, 9]$. 피벗 5가 인덱스 3에 있고, 왼쪽에는 더 작은 원소, 오른쪽에는 더 큰 원소가 있다.

**피벗 선택이 모든 것을 정하는 이유.** 피벗이 순위 $q$에 떨어져 $q$개가 왼쪽, $n - 1 - q$개가 오른쪽으로 가면, 파티션은 선형이고 피벗 자신은 어느 재귀 호출에도 들어가지 않으므로 퀵정렬의 비용은 다음을 만족한다.
$$T(n) = T(q) + T(n - 1 - q) + \Theta(n), \qquad T(0) = T(1) = \Theta(1)$$
피벗이 늘 중앙값이면 점화식은 $T(n) = 2T(n/2) + O(n)$, 즉 $\Theta(n \log n)$이다. 늘 최솟값이나 최댓값이면 한쪽은 비고 다른 쪽은 $n - 1$개이므로 $T(n) = T(n-1) + O(n) = \Theta(n^2)$이다. "첫 원소를 쓴다" 같은 고정 규칙은 이미 정렬되었거나 역순인 입력에서 이 최악을 만나는데, 이런 입력은 실제로 흔하다. 타임스탬프, 거의 정렬된 리스트를 다시 정렬하기, 앞 단계에서 정렬된 리스트. **무작위 피벗**(모든 원소가 같은 확률)은 입력에 대한 의존을 없앤다. 그러면 기대 실행 시간이 *모든 입력에 대해* $O(n \log n)$이며, 여기서 기댓값은 가정한 입력 분포가 아니라 알고리즘 자신의 동전 던지기에 대한 것이다.

**기대 시간 논증.** 복잡한 무작위 점화식을 풀지 않아도 되어서 인터뷰에서 즐겨 묻는 증명이다.

1. $z_1 < z_2 < \dots < z_n$을 정렬된 순서의 원소라 하고 서로 다르다고 가정한다. 파티션은 비교 한 번당 $O(1)$ 일을 하므로, 실행 시간은 비교 횟수 $C$에 비례한다.
2. 두 원소는 둘 중 하나가 피벗일 때만 비교되고, 피벗은 이후 두 재귀 호출 모두에서 빠진다. 따라서 각 쌍은 **최대 한 번** 비교된다. $z_i$와 $z_j$가 한 번이라도 비교되면 1, 아니면 0인 $X_{ij}$를 두자. 그러면 $C = \sum_{i<j} X_{ij}$이고, 기댓값의 선형성([[02-foundations/probability|3. 확률 §2]])으로 $E[C] = \sum_{i<j} \Pr[z_i, z_j \text{ compared}]$이다.
3. **핵심 주장:** $z_i$와 $z_j$가 비교되는 것은 $\{z_i, z_{i+1}, \dots, z_j\}$에서 처음 뽑힌 피벗이 $z_i$ 또는 $z_j$일 때, 그리고 그때뿐이다. 이 집합의 원소가 피벗으로 뽑히기 전까지는 집합 전체가 한 부분 배열에 함께 남는다. 집합 밖의 피벗은 집합의 모든 원소보다 작거나 크기 때문이다. 처음 뽑힌 것이 $z_i$나 $z_j$이면, 그것은 자기 부분 배열의 모든 원소, 곧 다른 하나와도 비교된다. 둘 사이의 어떤 $z_k$가 먼저 뽑히면 $z_i$는 왼쪽, $z_j$는 오른쪽으로 가서 다시는 비교되지 않는다.
4. 피벗은 균등하게 뽑히므로, 집합의 $j - i + 1$개 원소 각각이 처음 뽑힐 확률은 같다. 그중 두 경우가 비교로 이어지므로 $\Pr[z_i, z_j \text{ compared}] = 2/(j-i+1)$이다.
5. 더한다. 각 $i$에 대해 $k = j - i + 1$로 치환하면 $k$는 2부터 많아야 $n$까지 간다.

$$E[C] = \sum_{i<j} \frac{2}{j-i+1} \le \sum_{i=1}^{n} \sum_{k=2}^{n} \frac{2}{k} \le 2n \ln n$$

마지막 단계는 $\sum_{k=2}^{n} 1/k = H_n - 1 \le \ln n$이기 때문에 성립한다. 여기서 $H_n = 1 + \tfrac12 + \dots + \tfrac1n$은 $n$번째 조화수다. 따라서 무작위 퀵정렬의 기대 비교 횟수는 많아야 $2n \ln n \approx 1.39\, n \log_2 n$이다. 같은 이중합을 부등식으로 누르지 않고 정확히 계산하면 $2(n+1)H_n - 4n$이고, 아래 시뮬레이션이 그것과 맞는다.

같은 정확한 값이 기대 비교 횟수 $C(n)$의 점화식에서도 나온다. 이 점화식은 똑같이 가능한 피벗 순위 $q$ $n$가지에 대해 평균을 낸다.
$$C(n) = (n - 1) + \frac{2}{n} \sum_{q=0}^{n-1} C(q), \qquad C(0) = C(1) = 0$$
$n - 1$은 파티션의 비교 횟수이고, 각 크기 $q$가 왼쪽으로 한 번, 오른쪽으로 한 번 나오므로 계수 2가 붙는다. 이것으로 $C(2) = 1$, $C(3) = 8/3$, $C(4) = 29/6 \approx 4.83$을 얻으며, 아래 예제가 쌍의 합으로 구하는 값과 같다.

```python
import math
import random

def count_comparisons(a):
    """Comparisons made by randomized quicksort on distinct values a."""
    if len(a) <= 1:
        return 0
    pivot = random.choice(a)
    smaller = [x for x in a if x < pivot]
    larger = [x for x in a if x > pivot]
    return len(a) - 1 + count_comparisons(smaller) + count_comparisons(larger)

n, trials = 1000, 100
average = sum(count_comparisons(list(range(n))) for _ in range(trials)) / trials
harmonic = sum(1 / k for k in range(1, n + 1))
print(round(average), round(2 * (n + 1) * harmonic - 4 * n), round(2 * n * math.log(n)))
# about 11000 (varies run to run), 10986 (exact expectation), 13816 (the 2 n ln n bound)
```

> [!example] 계산 예제 · Worked example
> $n = 4$이면 합의 항은 여섯 개다. $j - i = 1$인 이웃 쌍 세 개가 각각 $2/2 = 1$을 더한다. $j - i = 2$인 쌍 두 개가 각각 $2/3$을 더한다. 쌍 $(z_1, z_4)$ 하나가 $2/4$를 더한다. 따라서 $E[C] = 3 + 4/3 + 1/2 \approx 4.83$이다. 정확한 공식도 같다: $2 \cdot 5 \cdot H_4 - 16 = 10 \cdot 25/12 - 16 \approx 4.83$. 이웃한 원소는 둘을 갈라놓을 원소가 사이에 없으므로 *반드시* 비교된다.

**그래도 퀵정렬이 이차 시간이 되는 경우.** 최악은 여전히 $\Theta(n^2)$이다. 무작위 피벗에서는 그저 매우 드물 뿐이다. 실제로 이차 시간은 세 가지에서 온다. 결정적 피벗 규칙이 정렬된 입력이나 적대적 입력을 만날 때. 양방향 파티션이 **중복 원소가 많은** 입력을 만날 때인데, 어떤 원소를 골라도 같은 값이므로 무작위 피벗으로는 고쳐지지 않는다. 그리고 나쁜 분할은 재귀 깊이 $n$을 뜻하므로, Python 구현은 느려지기 전에 죽는다. 해결책은 무작위 피벗, 삼분할 파티션, 그리고 작은 쪽은 재귀하고 큰 쪽은 반복문으로 처리하기다. 마지막 방법은 각 재귀 호출이 범위의 절반 이하만 받으므로 스택을 $O(\log n)$으로 묶는다.

**중복을 위한 삼분할 파티션.** 범위를 피벗보다 작은 영역, 같은 영역, 큰 영역의 셋으로 나누고(Dijkstra의 "네덜란드 국기 문제"), 바깥 두 영역만 재귀한다. 정확히는 다음을 만족하는 인덱스 $lt \le gt$를 돌려준다.
$$a[i] < p \ \text{ for } lo \le i < lt, \qquad a[i] = p \ \text{ for } lt \le i \le gt, \qquad a[i] > p \ \text{ for } gt < i \le hi$$
그래서 피벗의 모든 복사본이 이미 최종 위치에 있고, 어느 것도 재귀 호출에 넘어가지 않는다. 그러면 값이 모두 같은 배열은 O(n) 한 번으로 끝나고, 서로 다른 키가 적은 입력은 선형에 가까워진다.

```python
import random

def quicksort(a, lo=0, hi=None):
    """Sort a in place: random pivot, three-way partition. Expected O(n log n)."""
    if hi is None:
        hi = len(a) - 1
    while lo < hi:
        pivot = a[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi        # a[lo:lt] < pivot, a[lt:i] == pivot, a[gt+1:hi+1] > pivot
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1               # do not advance i: the element swapped in is unexamined
            else:
                i += 1
        if lt - lo < hi - gt:         # recurse on the smaller side, loop on the larger,
            quicksort(a, lo, lt - 1)  # so the stack stays O(log n)
            lo = gt + 1
        else:
            quicksort(a, gt + 1, hi)
            hi = lt - 1

data = [3, 1, 3, 3, 9, 0, 3, 2, 3]
quicksort(data)
print(data)                           # [0, 1, 2, 3, 3, 3, 3, 3, 9]
```

**병합 정렬인가 퀵정렬인가?** 퀵정렬은 $O(\log n)$ 스택으로 제자리에서 정렬하고, 메모리를 순차적으로 훑고, 상수가 작아서 배열에서는 보통 더 빠르다. 안정적이지 않고 $O(n \log n)$은 기댓값으로만 성립한다. 병합 정렬은 O(n) 추가 메모리를 대가로 안정성과 $O(n \log n)$ 보장을 준다. 실제 라이브러리는 둘을 섞는다. C++ `std::sort`는 보통 *introsort*로, 재귀가 너무 깊어지면 힙 정렬로 넘어가고 작은 범위에는 삽입 정렬을 쓰는 퀵정렬이다. Python의 정렬은 병합 정렬이다(§5).

### 4. Ω(n log n) 하한과 그 아래로 내려가는 법

**비교 정렬**(comparison sort)은 제약 하나를 지키는 정렬 알고리즘이다. 키를 쓰는 유일한 방법이 두 항목에 대해 $k(x_i) \le k(x_j)$인지(또는 $<$, $=$인지) 묻는 것이고, 다음에 하는 일은 모두 그 예/아니오 답에만 달려 있다. 같은 말로, 두 입력 $x$와 $y$의 상대 순서가 같으면
$$k(x_i) \le k(x_j) \iff k(y_i) \le k(y_j) \quad \text{for all } i, j,$$
알고리즘은 두 입력에서 정확히 같은 단계를 밟으므로 $[1, 5, 3]$과 $[10, 50, 30]$을 구별하지 못한다. 병합 정렬, 퀵정렬, 힙 정렬, 삽입 정렬이 모두 비교 정렬이다. **반례:** 아래의 계수 정렬은 키를 배열 인덱스로 쓰므로 키의 순서만이 아니라 값 자체를 읽는다. 주장은 모든 비교 정렬이 최악의 경우 $\Omega(n \log n)$번 비교해야 한다는 것이고, 따라서 병합 정렬은 상수배 안에서 최적이다.

**결정 트리 논증.** $n$과 임의의 비교 정렬 하나를 고정하고, 서로 다른 $n$개 값의 순열을 입력으로 넣는다. 그 동작을 이진 트리로 그린다. 내부 노드는 비교 하나이고, 두 자식은 두 가지 결과이며, 리프는 끝난 실행으로서 입력을 정렬하는 재배치를 확정한 상태다. 서로 다른 입력 순열은 서로 다른 재배치가 필요하므로 서로 다른 리프에 도착해야 하고, 트리에는 리프가 적어도 $n!$개 필요하다. 높이 $h$인 이진 트리의 리프는 많아야 $2^h$개이므로 $2^h \ge n!$이고, 최악 비교 횟수는 $h \ge \log_2 n!$이다. 그것이 얼마나 큰지 보려고 $n!$의 인수 중 가장 큰 $n/2$개만 남기면, 각각이 $n/2$ 이상이므로

$$\log_2 n! \ge \log_2 \left(\frac{n}{2}\right)^{n/2} = \frac{n}{2} \log_2 \frac{n}{2} = \Omega(n \log n)$$

이다. 따라서 어떤 비교 정렬도 $n \log n$을 이기지 못한다. 예/아니오 답을 그보다 적게 받아서는 $n!$개 입력을 구별할 수 없기 때문이다. 같은 세기가 리프의 *평균* 깊이에도 적용되므로, 하한은 평균에서도, 무작위 비교 정렬에서도 성립한다.

> [!example] 계산 예제 · Worked example
> $n = 4$이면 순서가 $4! = 24$가지이므로 트리에 리프가 적어도 24개 필요하다. $2^4 = 16 < 24 \le 32 = 2^5$이므로 어떤 입력은 적어도 **5번** 비교해야 한다. 원소 4개에 대한 병합 정렬은 두 절반에 $1 + 1$번, 마지막 병합에 많아야 3번, 합해 많아야 5번 비교하므로 4개에서는 정확히 최적이다. $n = 5$이면 $\log_2 120 \approx 6.9$이므로 적어도 7번이 필요하다.

**하한 아래로 내려가기.** 하한은 키를 비교만 하지 않고 키 자체를 들여다보는 알고리즘에 대해서는 아무 말도 하지 않는다. 키가 작은 정수이거나 작은 자릿수로 자를 수 있으면 선형 시간에 정렬할 수 있다.

- **계수 정렬(counting sort).** `range(k)` 안의 정수 키에 대해 키마다 항목 수를 센다. 키가 더 작은 항목은 모두 앞에 와야 하므로, 그 누적합이 키마다 첫 출력 위치를 준다.
$$\text{start}[v] = \sum_{u < v} \text{count}[u]$$
  여기서 $\text{count}[u]$는 키가 $u$인 항목 수다. 키가 $2, 0, 2, 1$이면 개수는 $1, 1, 2$, 시작 위치는 $0, 1, 2$다. 그다음 왼쪽에서 오른쪽으로 한 번 훑으며 항목을 놓으면 안정성도 지켜진다. 시간과 공간이 $O(n + k)$이므로 $k = O(n)$이면 선형이고 $k$가 거대하면 쓸모없다.
- **기수 정렬(radix sort).** 각 키를 밑 $b$의 $d$자리로 쓴다.
$$x = \sum_{t=0}^{d-1} x_t\, b^t, \qquad x_t = \lfloor x / b^t \rfloor \bmod b$$
  자릿수 $x_t$가 바로 `(x // shift) % base`가 계산하는 값이며, 밑 10에서 802는 $x_0 = 2$, $x_1 = 0$, $x_2 = 8$이다. 가장 낮은 자릿수부터 정렬하고, 다음 자릿수, 그다음 자릿수로 가며 자릿수마다 *안정적인* 계수 정렬을 쓴다. $t$번째 패스 후에는 항목들이 마지막 $t$자리 기준으로 정렬되어 있다. 안정성이 앞선 동점의 순서를 지키기 때문이다. 밑 $b$로 $d$자리면 $O(d(n + b))$이다. 32비트 키를 밑 256으로 하면 선형 패스 네 번이다. 충돌 검사와 레이 캐스팅에 쓰는 GPU 경계 볼륨 계층(BVH) 빌더는 기본 도형의 Morton 코드를 이렇게 기수 정렬하고, 포인트 클라우드의 점을 복셀별로 묶을 때 정수 복셀 인덱스도 같은 방식으로 정렬할 수 있다.
- **버킷 정렬(bucket sort).** $[0, 1)$에 대략 균등하게 퍼진 실수 키라면, 각 항목 $x$를 너비가 같은 $n$개 버킷 중 $\lfloor n x \rfloor$번 버킷에 넣고($n = 4$이면 키 $0.62$는 2번 버킷), 버킷마다 정렬해 이어 붙인다. 버킷마다 기댓값으로 $O(1)$개가 들어가므로 기대 시간은 $O(n)$이다. 데이터가 뭉쳐 있으면 한 버킷에 전부 들어가 안쪽 정렬의 비용으로 돌아간다.

```python
def counting_sort(items, key, k):
    """Stable sort of items by integer key(item) in range(k). O(n + k)."""
    start = [0] * (k + 1)
    for x in items:
        start[key(x) + 1] += 1
    for v in range(k):                    # prefix sums: start[v] = first output slot for key v
        start[v + 1] += start[v]
    out = [None] * len(items)
    for x in items:                       # a left-to-right pass keeps equal keys in order
        out[start[key(x)]] = x
        start[key(x)] += 1
    return out

def radix_sort(nums, base=256):
    """LSD radix sort of non-negative ints: one stable counting pass per digit."""
    out, shift = list(nums), 1
    while out and shift <= max(out):
        out = counting_sort(out, lambda x: (x // shift) % base, base)
        shift *= base
    return out

print(counting_sort(["b2", "a0", "c2", "d1"], key=lambda s: int(s[1]), k=3))
# ['a0', 'd1', 'b2', 'c2']
print(radix_sort([170, 45, 75, 90, 802, 24, 2, 66], base=10))
# [2, 24, 45, 66, 75, 90, 170, 802]
```

순수 Python에서는 C로 도는 내장 `sorted`를 이기는 경우가 드물다. 선형 시간 정렬은 컴파일된 코드, NumPy, GPU에서 이득이 난다. 위에 쓴 기수 정렬은 음이 아닌 정수가 필요하다. 음수 키는 먼저 오프셋을 더하라.

### 5. 라이브러리가 주는 것

실제 코드에서 정렬을 직접 쓸 일은 거의 없다. 호출할 뿐이고, 버그는 호출 방식에 있다.

**Python.** `list.sort()`는 제자리에서 정렬하고 `None`을 돌려준다. `sorted(iterable)`은 새 리스트를 돌려준다. 둘 다 **Timsort** 알고리즘을 쓴다. 데이터에 이미 있는 런(run), 즉 오름차순이거나 엄격한 내림차순인 구간을 먼저 찾고, 병합이 균형을 유지하는 순서로 런들을 병합하는 병합 정렬이다. Python 3.11부터 그 병합 순서는 *powersort* 규칙을 따른다. 말할 수 있어야 하는 결과는 다음과 같다.

- **안정적이며, 언어가 보장한다.** 믿고 써도 되고, `reverse=True`도 안정성을 지킨다. 같은 항목들은 뒤집히지 않고 원래 순서를 유지한다.
- **이미 정렬되었거나 역순인 입력에서 $O(n)$**, 최악은 $O(n \log n)$이다. 병합에 추가 슬롯을 최대 $n/2$개 쓴다.
- **`key=`는 항목마다 한 번 호출되고**, 정렬은 그 키들을 비교한다. 비교 함수보다 빠르고 명확하다.
- **튜플은 필드 순서대로 비교된다.** 그래서 `key=lambda g: (-g.score, g.time)`은 "점수 높은 순, 그다음 시간 이른 순"이다. 문자열처럼 음수로 만들 수 없는 필드로 내림차순 정렬하려면 안정성을 쓴다. 보조 키로 먼저 정렬하고, 주 키로 `reverse=True` 정렬한다.
- **키로 표현되지 않는 쌍별 규칙:** `functools.cmp_to_key(cmp)`를 거친다. `cmp(a, b)`는 음수, 0, 양수를 돌려준다.

```python
import math

grasps = [("g1", 0.82, 1), ("g2", 0.91, 5), ("g3", 0.82, 3), ("g4", 0.91, 2)]  # (name, score, time)

best_then_earliest = sorted(grasps, key=lambda g: (-g[1], g[2]))
print([g[0] for g in best_then_earliest])       # ['g4', 'g2', 'g1', 'g3']

by_name_desc = sorted(grasps, key=lambda g: g[0], reverse=True)       # secondary key first,
by_score_then_name = sorted(by_name_desc, key=lambda g: g[1], reverse=True)  # primary key last
print([g[0] for g in by_score_then_name])       # ['g4', 'g2', 'g3', 'g1']

losses = [0.3, float("nan"), 0.1, 0.2]
print(sorted(losses))                           # [0.3, nan, 0.1, 0.2]  -- not sorted
print(sorted(losses, key=lambda x: (math.isnan(x), x)))   # [0.1, 0.2, 0.3, nan]
```

마지막 두 줄은 ML 코드의 실제 버그다. NaN과의 비교는 전부 `False`라서 정렬이 기대는 순서 관계가 깨지고, 출력은 오류 하나 없이 그냥 정렬되지 않은 상태가 된다. NaN이 섞일 수 있는 손실이나 거리를 정렬하려면 NaN을 한쪽 끝으로 보내는 키가 필요하다. NumPy의 `np.sort`는 NaN을 끝에 두지만 기본 알고리즘이 안정적이지 않다. 동점의 순서를 지켜야 하면 `kind="stable"`을 넘겨라.

Python 함정이 두 가지 더 있다. 키 튜플의 앞 필드가 동점이고 다음 필드가 dict처럼 순서가 없는 값이면 정렬이 `TypeError`를 낸다. 동점을 깨는 인덱스를 넣어라. 그리고 dict에 `sorted(d)`를 하면 *키*가 정렬된다. 쌍이 필요하면 `sorted(d.items(), key=...)`를 써라.

**C++.**

- `std::sort`는 **안정적이지 않다.** $O(n \log n)$이고 보통 introsort다. 같은 원소의 순서를 지켜야 하면 병합 정렬인 `std::stable_sort`를 쓴다. 버퍼가 있으면 $O(n \log n)$, 추가 메모리를 얻지 못하면 $O(n \log^2 n)$이다.
- `std::partial_sort`는 앞 $k$개 위치만 $O(n \log k)$에 정렬하고, `std::nth_element`는 평균 선형 시간에 선택(§7)을 한다.
- 사용자 비교자는 **strict weak ordering이어야 한다.** `cmp(a, b)`를 $a \prec b$로 쓰고, 어느 쪽도 다른 쪽보다 작지 않을 때 $a$와 $b$가 *비교 불가*라고 하자.
$$a \sim b \iff \text{not } a \prec b \ \text{ and } \ \text{not } b \prec a$$
  strict weak ordering은 모든 $a, b, c$에 대해 이름 붙은 네 조건을 만족한다.
  - *비반사성*(irreflexivity): $a \prec a$는 거짓이다. 즉 `cmp(a, a)`가 거짓이다.
  - *비대칭성*(asymmetry): $a \prec b$이면 $b \prec a$는 거짓이다. 즉 `cmp(a, b)`와 `cmp(b, a)`가 동시에 참일 수 없다.
  - *추이성*(transitivity): $a \prec b$이고 $b \prec c$이면 $a \prec c$다.
  - *비교 불가의 추이성*(transitivity of incomparability): $a \sim b$이고 $b \sim c$이면 $a \sim c$다.

  넷이 함께 $\sim$을 동치 관계로 만들고, 그 동치류, 즉 동점 항목의 묶음들이 $\prec$로 전순서를 이루므로 "정렬됨"의 뜻이 하나로 정해진다. 정수의 `<`는 네 조건을 모두 만족한다.
- 대표적인 위반은 `return a <= b;`다. 첫 규칙을 깨며, 이는 순서가 틀리는 정도가 아니라 정의되지 않은 동작이다. 실제 구현은 배열 끝을 넘어 읽다가 죽을 수 있다. NaN일 수 있는 부동소수점 값을 비교하거나, 엡실론 안의 값을 "같다"고 취급해도 같은 규칙이 깨진다. NaN과의 비교는 모두 거짓이므로 $1 \sim \text{NaN}$이고 $\text{NaN} \sim 2$인데 $1 < 2$다. 비교 불가가 추이적이지 않다.
- 필드가 여러 개면 `std::tie(a.x, a.y) < std::tie(b.x, b.y)`로 비교하라. 사전식이고 구조상 올바르다.

### 6. 이진 탐색 제대로 하기

**한 문장 아이디어:** 위치에 대한 예/아니오 질문의 답이 어떤 지점까지는 "아니오"이고 그 뒤로는 "예"라면, 아직 결정되지 않은 범위의 가운데를 반복해서 묻고 그 지점을 포함할 수 없는 절반을 버려서 그 지점을 찾을 수 있다.

이진 탐색 버그의 거의 전부는 `lo`와 `hi`가 무엇을 뜻하는지에 대한 불일치다. 규약 하나를 정하고 모든 줄을 거기서 끌어내라. 가장 잘 맞물리는 규약은 **반열린 구간** `[lo, hi)`다. `lo`는 포함, `hi`는 제외이고, `lo == hi`이면 범위가 비었으며, 크기는 `hi - lo`다. `range`, 슬라이스, C++ 반복자의 규약과 같다.

문제를 "단조 술어가 처음으로 참이 되는 위치 찾기"로 말하라. `pred`가 `[lo, hi)`에서 False, …, False, True, …, True이고, 첫 True를, 없으면 `hi`를 원한다. 모든 이진 탐색은 이 함수 하나에 술어만 바꾼 것이다.

정확히 말하면, 반열린 범위 $[lo, hi) = \{x : lo \le x < hi\}$의 정수 위에서 술어가 한 번 참이 되면 계속 참일 때 **단조**(monotone)라고 한다.
$$\text{pred}(x) \implies \text{pred}(y) \quad \text{for all } lo \le x \le y < hi$$
답은 $x^* = \min\{x \in [lo, hi) : \text{pred}(x)\}$이고, 참으로 만드는 $x$가 없으면 $x^* = hi$다. `mid`에서의 False는 `mid` 왼쪽이 모두 False임을 증명하므로, 단조성 덕분에 한 번의 검사로 범위의 절반을 버릴 수 있다. **반례:** `a = [5, 1, 4]`에서 술어 `a[i] >= 4`는 True, False, True로 단조가 아니다. `first_true`는 인덱스 1을 검사해 False를 보고 인덱스 0을 버린 뒤 2를 돌려주지만, 첫 True는 인덱스 0이다.

```python
from bisect import bisect_left, bisect_right

def first_true(lo, hi, pred):
    """Smallest x in [lo, hi) with pred(x) True, or hi if none.
    pred must be monotone on [lo, hi): False ... False True ... True."""
    while lo < hi:                  # invariant: the answer lies in [lo, hi]
        mid = (lo + hi) // 2        # lo <= mid < hi, so both branches shrink the range
        if pred(mid):
            hi = mid                # mid may be the answer: keep it
        else:
            lo = mid + 1            # mid is not the answer: drop it
    return lo

a = [2, 4, 4, 4, 7, 9]
lower = first_true(0, len(a), lambda i: a[i] >= 4)    # first index with a[i] >= 4
upper = first_true(0, len(a), lambda i: a[i] > 4)     # first index with a[i] > 4
print(lower, upper, upper - lower)                    # 1 4 3   (three 4s)
assert (lower, upper) == (bisect_left(a, 4), bisect_right(a, 4))
```

**왜 맞고 왜 끝나는가.** 불변식은 첫 True가 `[lo, hi]` 안에 있다는 것이며, 값 `hi`는 "없음"을 뜻한다. 시작할 때 성립한다. `pred(mid)`가 True이면 첫 True는 `mid`이거나 그 앞이므로 `hi = mid`가 그것을 지킨다. False이면 단조성에 의해 `mid`까지 모두 False이므로 `lo = mid + 1`이 그것을 지킨다. `mid < hi`이므로 두 분기 모두 범위를 엄격히 줄이고, 루프는 `lo == hi`가 답인 상태로 끝난다. 단계 수는 $\lceil \log_2(\text{hi} - \text{lo} + 1) \rceil$이다.

**lower bound와 upper bound.** 정렬된 배열에서 `x`의 **lower bound** 값은 `a[i] >= x`인 첫 인덱스로, `x`가 있는 곳 또는 같은 항목들 앞에 삽입될 곳이다. **upper bound** 값은 `a[i] > x`인 첫 인덱스로, `x`의 마지막 복사본 바로 뒤다. 식으로 쓰면
$$\text{lower}(x) = \min\{i : a[i] \ge x\}, \qquad \text{upper}(x) = \min\{i : a[i] > x\}$$
이고, 공집합의 최솟값은 `len(a)`로 두므로 모든 `x`에 대해 정의된다. `a = [2, 4, 4, 4, 7, 9]`이면 lower(4) = 1, upper(4) = 4, lower(5) = 4, lower(10) = 6이다. 나머지는 모두 이 둘에서 나온다.

- `x`가 있는 것은 `lower < len(a) and a[lower] == x`일 때, 그리고 그때뿐이다.
- `x`의 개수는 `upper - lower`다.
- `a[i] <= x`인 마지막 인덱스는 `upper - 1`이다.
- `[x, y)` 안의 원소 수는 `lower(y) - lower(x)`다.

**표준 라이브러리.** Python의 `bisect_left`와 `bisect_right`가 lower bound와 upper bound이며, 둘 다 `lo`, `hi`, 그리고 3.10부터 `key=`를 받는다. `key` 동작을 조심하라. 배열 원소에는 적용되지만 `x`에는 적용되지 않으므로, `x`는 이미 키 값이어야 한다. `insort`는 위치를 $O(\log n)$에 찾지만 리스트가 밀리므로 삽입은 $O(n)$이다. C++에는 `std::lower_bound`, `std::upper_bound`, `std::equal_range`가 있고, `std::partition_point`가 범위에 대한 `first_true` 그 자체다. `std::binary_search`는 `bool`만 돌려주므로 필요한 경우가 드물다.

**인터뷰 함정.**

- **규약 섞기.** `while lo <= hi`(닫힌 구간)와 `hi = mid`(반열린 갱신)를 함께 쓰면 `pred(mid)`가 참이고 `lo == hi`일 때 무한 루프다.
- **내림 중간값에서 `lo = mid`.** `hi == lo + 1`이면 `mid == lo`라 아무것도 바뀌지 않는다. 템플릿이 항상 `lo = mid + 1`로 두는 이유다.
- **C++과 Java의 오버플로.** `(lo + hi) / 2`는 넘칠 수 있다. `lo + (hi - lo) / 2`로 써라. Python 정수는 넘치지 않는다.
- **실수 값의 답.** `hi - lo > eps`를 검사하지 말고 100번 같은 고정 횟수 후에 멈춰라. `eps`가 부동소수점 해상도보다 작으면 영원히 돈다.

**로보틱스 활용: 타임스탬프 사이 찾기.** 이미지 타임스탬프에서의 자세나 관절각을 추정하려면, 그 시각을 사이에 둔 두 버퍼 샘플을 찾아 보간한다. 버퍼는 시간순으로 정렬되어 있으므로 이것은 upper bound 탐색이다. 스탬프는 같은 시계 기준이어야 하며, 그것이 [[04-robotics/ros2/qos-executors-time|25.5 §10]]의 주제다.

```python
from bisect import bisect_right

def interpolate(stamps, values, t):
    """Linearly interpolate values at time t; stamps strictly increasing, len >= 2."""
    if not stamps[0] <= t <= stamps[-1]:
        raise ValueError("t is outside the buffer; refusing to extrapolate")
    k = min(bisect_right(stamps, t), len(stamps) - 1)   # stamps[k-1] <= t <= stamps[k]
    t0, t1 = stamps[k - 1], stamps[k]
    w = (t - t0) / (t1 - t0)
    return (1 - w) * values[k - 1] + w * values[k]

print(interpolate([0.00, 0.10, 0.20, 0.30], [0.0, 1.0, 4.0, 9.0], 0.25))   # 6.5
```

**답에 대한 이진 탐색.** 많은 최적화 문제가 무언가를 가능하게 하는 가장 작은 값 $x$를 묻는다. 가능성이 **단조** 성질을 가지고, 즉 $x$가 되면 더 큰 $x$도 모두 되어
$$\text{feasible}(x) \implies \text{feasible}(x') \quad \text{for all } x' \ge x,$$
답 $x^* = \min\{x : \text{feasible}(x)\}$가 정확히 `feasible`을 술어로 한 `first_true`이고, 주어진 $x$를 *확인*하는 것이 최선의 $x$를 직접 찾는 것보다 훨씬 쉽다면, 가능성 검사를 술어로 삼아 $x$에 대해 이진 탐색하라. 비용은 검사 $O(\log(\text{범위}))$번이다.

표준 예: 무게 $w_1, \dots, w_n$인 짐들이 **주어진 순서대로** 창고를 떠나야 하고, 기간은 많아야 $D$일이며, 하루 적재량은 차량 용량을 넘을 수 없다. 가능한 가장 작은 용량은 얼마인가?

- 용량을 확인하는 것은 탐욕법이다. 다음 짐이 넘치게 할 때까지 하루를 채우고, 넘치면 새 날을 시작한다. 탐욕법은 다른 어떤 계획보다 날을 더 쓰지 않는다. 귀납적으로 탐욕법의 $k$번째 날은 어떤 유효한 계획의 $k$번째 날보다 같거나 늦게 끝나기 때문이다.
- **단조성:** 용량 $c$에서 되는 계획은 $c' > c$에서도 된다.
- **범위:** 가장 무거운 짐이 들어가야 하므로 답은 $\max_i w_i$ 이상이고, 하루에 전부 보내는 $\sum_i w_i$ 이하다.

그러므로 `first_true(max(w), sum(w) + 1, fits)`가 총 $O(n \log \sum_i w_i)$ 작업으로 답을 찾는다.

```python
def first_true(lo, hi, pred):
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo

def min_capacity(weights, days):
    """Smallest capacity that ships weights, in order, within the given days."""
    def fits(cap):                  # greedy: fill a day until the next item would overflow
        used, load = 1, 0
        for w in weights:
            if load + w > cap:
                used, load = used + 1, 0
            load += w
        return used <= days
    return first_true(max(weights), sum(weights) + 1, fits)

print(min_capacity([3, 2, 2, 4, 1, 4], days=3))   # 6
```

> [!example] 계산 예제 · Worked example
> 무게 $[3, 2, 2, 4, 1, 4]$, $D = 3$일. 범위는 $[4, 17)$이다.
> - 용량 10은 $[3, 2, 2]$, $[4, 1, 4]$ 이틀에 되므로 답은 10 이하: `hi = 10`.
> - 용량 7은 $[3, 2, 2]$, $[4, 1]$, $[4]$ 사흘이 필요하므로 `hi = 7`.
> - 용량 5는 $[3, 2]$, $[2]$, $[4, 1]$, $[4]$ 나흘이 필요하므로 `lo = 6`.
> - 용량 6은 $[3, 2]$, $[2, 4]$, $[1, 4]$ 사흘이 필요하므로 `hi = 6`.
>
> 이제 `lo == hi == 6`이다. O(n) 검사 네 번이 용량 13가지를 모두 시도하는 일을 대신한다.

같은 패턴이 계획 문제에도 나온다. 격자 경로가 장애물과 유지할 수 있는 **최대 여유 거리**(clearance)를 원한다고 하자. 여유 거리 $r$에 대해 모든 장애물을 $r$칸 부풀리고 BFS를 돌린다([[02-foundations/algorithms/graph-algorithms|11.6 §2]]). 가능성은 단조 감소한다. 여유 거리 $r$을 유지하는 경로는 더 작은 여유 거리도 모두 유지한다. 따라서 "여유 거리 $r$에서 경로 없음"은 $r$이 커질수록 False…True이고, `first_true(0, R + 1, blocked) - 1`이 가능한 최대 여유 거리이며, 탐색 전체는 BFS $R$번이 아니라 $O(\log R)$번이다. 결과가 $-1$이면 $r = 0$에서도 경로가 없다는 뜻이다.

### 7. 선택: 정렬 없이 k번째로 작은 원소

중앙값, 백분위수, 가장 작은 $k$개를 찾는 데 전체 정렬은 필요 없다. 정렬은 $O(n \log n)$이고, 선택은 $O(n)$에 할 수 있다.

**무엇을 선택하는가.** 값 $n$개의 **$k$번째로 작은 원소**(k-th order statistic, 코드처럼 $k = 0$부터 센다)는 정렬했을 때 인덱스 $k$에 올 값이다. 정렬 없이도 말할 수 있다. 배열의 값 $x$ 중
$$\#\{i : a[i] < x\} \le k < \#\{i : a[i] \le x\}$$
를 만족하는 것이다. $x$의 첫 복사본 앞에는 정확히 $x$보다 작은 원소들이 오고, 복사본들이 위치 $\#\{i : a[i] \le x\} - 1$까지를 채우기 때문이다. **중앙값**(median)은 $k = \lfloor n/2 \rfloor$이다. 아래 코드의 거리 값 일곱 개에서 $x = 2.8$은 더 작은 값이 3개, $2.8$ 이하인 값이 4개이므로 $k = 3$의 원소, 곧 중앙값이다.

**Quickselect.** *한 문장 아이디어:* 퀵정렬처럼 무작위 피벗으로 파티션한 뒤, 위치 $k$를 담은 쪽에서만 계속한다.

삼분할 파티션 후 위치 `lt..gt`에는 피벗의 복사본이 있다. `k`가 그 안에 있으면 피벗이 답이다. `k < lt`이면 답은 왼쪽에, `k > gt`이면 오른쪽에 있다. 배열을 복사하지 않으므로 위치 `k`는 그대로다.

**기대 O(n).** 원소 $m$개의 파티션은 $O(m)$이다. 확률 1/2 이상으로 무작위 피벗이 현재 범위의 가운데 절반에 떨어지고, 그러면 남기는 쪽은 많아야 $3m/4$개다. 라운드를 *단계*로 묶어, 단계 $j$를 범위 크기가 $(3/4)^{j+1} n$과 $(3/4)^j n$ 사이인 동안으로 정하자. 각 라운드는 확률 1/2 이상으로 단계를 끝내므로 한 단계는 기댓값으로 많아야 2라운드이고(앞면이 나올 때까지 동전 던지기: 매번 성공 확률이 $p$이면 기대 시도 횟수는 $1/p$, 여기서는 $1/(1/2) = 2$), 단계 $j$의 각 라운드 비용은 많아야 $c(3/4)^j n$이다. 그러므로 기대 총비용은

$$E[T(n)] \le \sum_{j \ge 0} 2c \left(\frac{3}{4}\right)^j n = 8cn$$

이고, 기하급수의 합이 4이므로 $O(n)$이다. 매번 극단적인 피벗이 뽑히면 최악은 여전히 $\Theta(n^2)$이다.

```python
import random

def quickselect(a, k):
    """k-th smallest element of a (k = 0 is the minimum). Expected O(n); a is not modified."""
    a = list(a)
    lo, hi = 0, len(a) - 1
    while True:
        pivot = a[random.randint(lo, hi)]
        lt, i, gt = lo, lo, hi          # three-way partition of a[lo..hi], as in quicksort
        while i <= gt:
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return pivot                # positions lt..gt all hold the pivot

ranges = [2.9, 0.4, 5.1, 0.5, 30.0, 0.45, 2.8]   # one spurious long return
print(quickselect(ranges, len(ranges) // 2))     # 2.8, the median; the mean is 6.02
```

**Median of medians: 최악에서도 O(n).** Blum, Floyd, Pratt, Rivest, Tarjan(1973)은 피벗을 결정적으로 고른다. 원소를 5개씩 묶고, 묶음마다 중앙값을 구하고, 그 $n/5$개 중앙값의 중앙값을 재귀로 선택해 피벗으로 쓴다. 묶음 중앙값의 절반은 이 피벗 이하이고, 그 각각은 자기 묶음의 다른 두 원소 이상이므로, 피벗은 전체 원소의 약 $3/10$보다 크고, 대칭으로 약 $3/10$보다 작다. 남는 쪽은 많아야 약 $7n/10$개이므로, 작은 상수보다 큰 $n$에서 $T(n) \le T(n/5) + T(7n/10) + O(n)$이고 그 아래에서는 $T(n) = O(1)$이다. $1/5 + 7/10 = 9/10 < 1$이므로 레벨당 작업이 기하급수로 줄고 전체는 $O(n)$이다. "선택은 최악에서도 선형이다"로 알아 둘 가치가 있지만 상수가 커서, 실제로는 무작위 선택이나 introselect를 쓴다: C++ `std::nth_element`, NumPy `np.partition`과 `np.argpartition`.

**힙으로 상위 k개.** `heapq.nsmallest(k, items, key=...)`(와 `nlargest`)는 지금까지 본 최선의 $k$개를 최대 힙에 유지한다. 새 항목은 힙의 top과 비교해 더 좋으면 $O(\log k)$ 비용으로 교체한다. 그래서 시간 $O(n \log k)$, 메모리 $O(k)$이고, 결과는 정렬된 순서로 나온다. 메모리에 담을 수 없는 스트림이나 이터레이터에도 쓸 수 있고 안정적이다. $k = 1$이면 `min`을 써라. $k$가 $n$에 가까우면 `sorted(items)[:k]`가 더 빠르다. 모두 NumPy 배열에 있다면 `np.argpartition`이 상위 $k$개를 $O(n)$에 주고, 순서가 필요하면 그 $k$개만 나중에 정렬한다.

```python
import heapq
import math

robot = (0.0, 0.0)
obstacles = [(2.0, 1.0), (-0.5, 0.2), (3.0, -4.0), (0.3, 0.4), (1.0, 1.0)]
nearest = heapq.nsmallest(3, obstacles, key=lambda p: math.dist(p, robot))
print(nearest)          # [(0.3, 0.4), (-0.5, 0.2), (1.0, 1.0)]
```

**로보틱스에서 선택이 쓰이는 곳.**

- 거리·깊이 데이터의 **메디안 필터** 처리는 평균이라면 이웃에 번져 버릴 고립된 튀는 값을 없앤다. 위의 quickselect 예제가 그것이다.
- 피팅 전에 이상치를 거르는 중앙값 절대 편차(MAD) 같은 **강건한 임계값** 계산은 선택 문제다.
- **KD-tree 구성** 과정은 `nth_element`로 중앙값 좌표에서 분할하며, 레벨당 $O(n)$, 트리 전체 $O(n \log n)$이다([[02-foundations/algorithms/data-structures|11.2 §8]]).
- GPU에서의 **전수 k-최근접 이웃** 계산은 거리 행렬 뒤에 top-k를 붙인 것이다.

### 8. 알아볼 만한 다른 분할 정복 고전

**빠른 거듭제곱.** *한 문장 아이디어:* $n$이 짝수면 $x^n = (x^{n/2})^2$, 홀수면 $x \cdot x^{n-1}$이므로 지수가 두 단계마다 반으로 준다. 기저 사례와 함께 쓰면
$$x^n = \begin{cases} 1 & n = 0 \\ (x^{n/2})^2 & n > 0 \text{ even} \\ x \cdot x^{n-1} & n \text{ odd} \end{cases}$$
이고, 곱셈이 **결합적**(associative)이어서 $(ab)c = a(bc)$, 즉 $x$ $n$개의 곱을 어떻게 묶어도 되고 `one`이 항등원 $1 \cdot x = x$이므로 모든 경우가 성립한다. $n$의 비트를 도는 루프로 쓰면 불변식은 `result * x**n`이 항상 원래의 $x_0^{n_0}$와 같다는 것이다. 각 단계는 현재 비트를 `result`에 곱하거나, `x`를 제곱하고 `n`을 반으로 줄이므로 곱셈 $O(\log n)$번이 든다. 항등원이 있는 결합적 곱셈만 있으면 된다. 뺄셈은 반례다. $(8 - 4) - 2 = 2$이지만 $8 - (4 - 2) = 6$이라 묶는 방식이 답을 바꾼다. 결합적 곱셈이면 같은 루프가 다음을 계산한다.

- 모듈러 거듭제곱. Python 내장 `pow(a, n, m)`이 이미 한다.
- 행렬 거듭제곱. 선형 점화식의 $n$번째 항을 행렬 곱 $O(\log n)$번에 준다(피보나치가 고전 예).
- 마르코프 연쇄의 $k$단계 전이 행렬 $P^k$, 또는 이산 시간 선형 시스템의 전파 $A^k$. `numpy.linalg.matrix_power`가 이 방식이다.

비용은 비트 연산이 아니라 곱셈 횟수로 센 것이다. 거대한 정수에서는 수 자체가 커져 곱셈 한 번이 점점 비싸진다.

```python
def power(x, n, mul=lambda a, b: a * b, one=1):
    """x**n for integer n >= 0 using O(log n) calls to an associative mul."""
    result = one
    while n > 0:                   # invariant: result * x**n == original x**n
        if n & 1:
            result = mul(result, x)
        x = mul(x, x)
        n >>= 1
    return result

def matmul(A, B):
    cols = list(zip(*B))
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) for col in cols) for row in A)

print(power(3, 13))                                        # 1594323
fib = power(((1, 1), (1, 0)), 10, matmul, ((1, 0), (0, 1)))
print(fib[0][1])                                           # 55, the 10th Fibonacci number
```

**2차원 최근접 점 쌍.** 점 $n$개가 주어지면 유클리드 거리 $\lVert p - q \rVert = \sqrt{(p_x - q_x)^2 + (p_y - q_y)^2}$를 최소로 하는 서로 다른 두 점 $p, q$를 찾는다. 모든 쌍을 확인하면 $O(n^2)$이다. 1차원이라면 정렬하고 이웃끼리 비교하면 된다. 2차원에서는 분할 정복이 $O(n \log n)$에 도달한다.

1. **나누기.** 점들을 $x$로 정렬하고 수직선으로 왼쪽 절반과 오른쪽 절반으로 나눈다.
2. **재귀.** 각 절반에서 최근접 쌍을 찾고, 두 거리 중 작은 것을 $\delta$라 한다.
3. **합치기.** 아직 찾지 못한 $\delta$보다 가까운 쌍은 선의 양쪽에 점이 하나씩 있어야 하고, 두 점 모두 선에서 $\delta$ 이내에 있어야 한다. 그렇지 않으면 가로 간격만으로 $\delta$를 넘기 때문이다. 따라서 **띠**(strip)만 보면 된다. 띠는 분할선 $x = \ell$에서 $\delta$ 이내에 있는 점들의 집합 $\{p : \lvert p_x - \ell \rvert < \delta\}$이고 너비는 $2\delta$다.

띠에도 거의 모든 점이 들어 있을 수 있으므로, 합치기를 선형으로 만드는 단계는 채우기(packing) 논증이다. 띠의 점들을 $y$로 정렬한다. $\delta$보다 가까운 쌍은 $y$ 차이가 $\delta$ 미만이다. 어떤 점 위쪽으로, 선을 가운데 둔 $2\delta \times \delta$ 직사각형을 한 변 $\delta/2$인 정사각형 여덟 개로 덮는다. 양쪽에 네 개씩이다. 같은 정사각형에 두 점이 있으면 같은 쪽에 있으면서 거리가 많아야 $\delta/\sqrt{2} < \delta$가 되어, $\delta$가 한쪽 안에서의 최소 거리라는 사실에 모순이다. 그러므로 정사각형마다 점은 많아야 하나이고, 각 점은 $y$ 순서로 다음 **7개** 점과만 비교하면 된다. 매 호출마다 띠를 다시 정렬하지 않고 병합 정렬처럼 병합으로 $y$ 순서를 유지하면 합치기가 $O(n)$이고 $T(n) = 2T(n/2) + O(n) = O(n \log n)$이다. 매 호출마다 다시 정렬하면 $O(n \log^2 n)$이다. 로보틱스 코드에서 "$r$보다 가까운 모든 쌍 찾기"는 보통 셀 크기 $r$인 격자나 공간 해시, 또는 KD-tree로 푼다. 분할 정복 버전은 기하학적 논증이 합치기를 선형으로 만드는 인터뷰 예제다.

**Karatsuba 곱셈.** 두 $n$자리 수를 윗절반과 아랫절반으로 나눈다. 밑 $B$(십진 자릿수라면 10)와 $m = n/2$로 $x = x_1 B^m + x_0$, $y = y_1 B^m + y_0$라 쓰면 곱은 다음과 같다.
$$xy = z_2 B^{2m} + z_1 B^m + z_0, \qquad z_2 = x_1 y_1, \quad z_0 = x_0 y_0, \quad z_1 = (x_1 + x_0)(y_1 + y_0) - z_2 - z_0$$
$(x_1 + x_0)(y_1 + y_0) = x_1 y_1 + x_1 y_0 + x_0 y_1 + x_0 y_0$이므로 $z_2$와 $z_0$를 빼면 가운데 항 $x_1 y_0 + x_0 y_1$만 남는다. 그래서 Karatsuba(1962)는 절반 크기 곱셈을 네 번이 아니라 세 번만 한다. $1234 \times 5678$이면 $z_2 = 12 \cdot 56 = 672$, $z_0 = 34 \cdot 78 = 2652$, $z_1 = 46 \cdot 134 - 672 - 2652 = 2840$이고 $672 \cdot 10^4 + 2840 \cdot 10^2 + 2652 = 7006652$다. 그러면 $T(n) = 3T(n/2) + O(n) = O(n^{\log_2 3}) \approx O(n^{1.585})$이고, CPython이 큰 정수에 쓰는 알고리즘이 이것이다.

### 스스로 점검

1. 병합 정렬의 병합이 `<=` 대신 `if left[i] < right[j]`를 쓴다. 출력은 여전히 정렬되는가? 어떤 성질을 잃는가? 차이가 보이는 항목 두 개짜리 입력을 들어라.
2. $[4, 3, 2, 1]$의 역순쌍은 몇 개인가? 병합 정렬의 마지막 병합에서 $[3, 4]$와 $[1, 2]$를 합칠 때, 어느 단계가 분할 역순쌍을 몇 개씩 더하는가?
3. 서로 다른 값에 대한 무작위 퀵정렬에서, 가장 작은 원소와 가장 큰 원소가 한 번이라도 비교될 확률은? 정렬 순서에서 이웃한 두 원소는?
4. Lomuto 파티션을 쓰는 무작위 퀵정렬을 같은 값 $10^6$개로 된 배열에 돌린다. 실행 시간은 얼마이고, 왜 무작위 피벗이 도움이 안 되며, 무엇이 고치는가?
5. 결정 트리 논증으로 원소 6개를 정렬하는 최악 비교 횟수의 하한은? 16비트 정수에 대한 계수 정렬은 왜 $\Omega(n \log n)$ 하한과 모순되지 않는가?
6. `first_true`만 써서 정렬된 배열에서 `a[i] <= x`인 마지막 인덱스 $i$를 찾고, 모든 원소가 `x`보다 클 때 무엇을 돌려주는지 말하라.
7. C++ 프로그램이 `std::sort(v.begin(), v.end(), [](double a, double b) { return a <= b; });`로 정렬하다가 어떤 입력에서만 죽는다. 이유를 설명하고, `<`로 바꿔도 같은 비교자가 깨질 수 있는 두 번째 경우를 들어라.
8. 메모리에 들어가지 않는 검출 결과 $10^8$개 스트림에서 점수 상위 100개가 필요하다. `heapq.nlargest`, 정렬, quickselect를 시간과 메모리로 비교하라. 실제로 쓸 수 있는 것은?
9. 최근접 쌍의 합치기 단계에서 각 띠 점을 $y$ 순서로 다음 7개 점과만 비교해도 되는 이유는? 띠의 모든 점과 비교하면 실행 시간은 어떻게 되는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 그렇다, 여전히 정렬된다. 동점에서 오른쪽 원소를 먼저 가져가도 작거나 같은 원소를 출력하기 때문이다. 안정성은 잃는다. `key`가 두 번째 필드를 비교할 때 입력 `[("a", 1), ("b", 1)]`은 `[("a", 1)]`과 `[("b", 1)]`로 나뉘고, 동점에서 `<`가 거짓이므로 병합이 `("b", 1)`을 먼저 출력해 같은 두 항목의 순서가 뒤집힌다.
> 2. 여섯 개다. 역순 배열이므로 $\binom{4}{2} = 6$쌍이 모두 역순쌍이다. 각 절반 $[4, 3]$과 $[2, 1]$이 하나씩 낸다. 마지막 병합에서 $[3, 4]$가 기다리는 동안 오른쪽에서 1이 출력되어 2를 더한다. 이어서 $[3, 4]$가 여전히 기다리는 동안 2가 출력되어 2를 더 더한다. 3과 4의 출력은 아무것도 더하지 않는다. 따라서 $1 + 1 + 4 = 6$.
> 3. $z_1$과 $z_n$ 사이의 집합은 배열 전체이므로 확률은 $2/n$이다. 둘 중 하나가 맨 첫 피벗일 때만 비교된다. 이웃한 $z_i, z_{i+1}$은 $2/2 = 1$이다. 사이에 아무것도 없으므로 하나가 피벗이 될 때까지 함께 남고, 피벗이 되면 다른 하나와 비교된다.
> 4. $\Theta(n^2)$, 약 $5 \times 10^{11}$번 비교이고, 재귀 Python 구현이라면 그보다 훨씬 전에 재귀 깊이 초과로 죽는다. 모든 피벗 값이 같으므로, 어느 원소를 고르든 양방향 파티션은 나머지 $n - 1$개를 한쪽에 몰아넣는다. 무작위성은 원소 사이에서 고르지만 원소가 모두 같다. 삼분할 파티션이 고친다. "같음" 영역이 O(n) 한 번에 배열 전체를 흡수한다.
> 5. $2^9 = 512 < 720 \le 1024$이므로 $\lceil \log_2 720 \rceil = 10$이다. 계수 정렬은 비교 정렬이 아니다. 키 값으로 배열을 인덱싱하므로 한 단계에서 입력에 대해 1비트보다 훨씬 많은 정보를 얻고, 결정 트리 모델이 적용되지 않는다. 비용은 $k = 65536$으로 $O(n + k)$다.
> 6. `first_true(0, len(a), lambda i: a[i] > x) - 1`, 즉 `bisect_right(a, x) - 1`이다. `x`보다 큰 첫 원소는 `<= x`인 마지막 원소 바로 뒤다. 모든 원소가 `x`보다 크면 `first_true`가 0을 돌려주므로 결과는 "그런 인덱스 없음"을 뜻하는 $-1$이다. 인덱스로 쓰기 전에 확인하라. Python에서 `a[-1]`은 조용히 마지막 원소를 읽는다.
> 7. `a == b`일 때 `a <= b`가 참이므로 `cmp(a, a)`가 참이다. 이것은 strict weak ordering의 요건 중 비반사성을 어기며, 동작은 정의되지 않는다. 구현의 파티션 루프는 원소가 자기 자신보다 "작을" 리 없다고 가정하므로 범위를 넘어갈 수 있다. `a < b`로 바꿔도 데이터에 NaN이 있으면 깨진다. NaN은 모든 값과 비교 불가능인데 그 값들끼리는 비교 가능하므로 "비교 불가능" 관계가 더 이상 추이적이지 않다. NaN을 먼저 걸러내거나 명시적으로 순서를 매겨라.
> 8. `heapq.nlargest(100, stream)`: $O(n \log k)$, 가벼운 연산 약 $10^8 \times 7$번이고, 메모리에는 100개만 두며, 이터레이터를 그대로 소비한다. 정렬은 $10^8$개 전부를 메모리에 올려야 하고 $O(n \log n)$ 시간이 든다. Quickselect는 기댓값 $O(n)$이지만 역시 배열 전체가 메모리에 있어야 하므로 스트림에는 쓸 수 없다. 힙을 써라.
> 9. 주어진 띠 점 위쪽에서 $\delta$보다 가까운 점은 $2\delta \times \delta$ 직사각형 안에 있다. 그 직사각형은 한 변 $\delta/2$인 정사각형 8개로 덮이고, 한 정사각형의 두 점은 같은 쪽에서 거리 $\le \delta/\sqrt{2} < \delta$가 되므로 정사각형마다 점은 많아야 하나다. 따라서 직사각형에는 자기 자신을 포함해 많아야 8개가 있고, 확인할 다른 점은 많아야 7개다. 띠의 모든 점과 비교하면 띠에 점이 대부분 들어 있을 때 합치기 한 번이 $O(n^2)$까지 들고, 알고리즘 전체가 $O(n^2)$로 나빠진다.

### 출처

- Cormen, Leiserson, Rivest & Stein, *Introduction to Algorithms*, 4th ed., MIT Press, 2022 — 병합 정렬, 퀵정렬과 그 무작위 분석, 정렬 하한, 계수·기수·버킷 정렬, 중앙값과 순서 통계량, 최근접 쌍.
- Roughgarden, *Algorithms Illuminated, Part 1: The Basics*, Soundlikeyourself Publishing, 2017 — 분할 정복, 역순쌍 세기, 최근접 쌍, 마스터 방법, 퀵정렬의 지시 변수 분석, 무작위·결정적 선택, 정렬 하한.
- Kulikov & Pevzner, *Learning Algorithms Through Programming and Puzzle Solving*, Active Learning Technologies, 2018 — 분할 정복 장: 중복이 있는 이진 탐색, 삼분할 퀵정렬, 역순쌍, 최근접 점.
- Knuth, D. E. *The Art of Computer Programming, Vol. 3: Sorting and Searching*, 2nd ed., Addison-Wesley, 1998.
- Hoare, C. A. R. "Algorithm 64: Quicksort" and "Algorithm 65: Find." *Communications of the ACM* 4(7), 1961.
- Hoare, C. A. R. "Quicksort." *The Computer Journal* 5(1), 1962. doi:10.1093/comjnl/5.1.10
- Blum, M., Floyd, R. W., Pratt, V., Rivest, R. L. & Tarjan, R. E. "Time bounds for selection." *Journal of Computer and System Sciences* 7(4), 1973. doi:10.1016/S0022-0000(73)80033-9
- Bentley, J. L. & McIlroy, M. D. "Engineering a sort function." *Software: Practice and Experience* 23(11), 1993 — 실제 정렬 구현의 삼분할 파티션.
- Dijkstra, E. W. *A Discipline of Programming*, Prentice-Hall, 1976 — 네덜란드 국기 문제.
- Kendall, M. G. "A new measure of rank correlation." *Biometrika* 30(1/2), 1938.
- Knight, W. R. "A computer method for calculating Kendall's tau with ungrouped data." *Journal of the American Statistical Association* 61(314), 1966.
- Shamos, M. I. & Hoey, D. "Closest-point problems." *IEEE Symposium on Foundations of Computer Science (FOCS)*, 1975.
- Karatsuba, A. & Ofman, Yu. "Multiplication of multidigit numbers on automata." *Soviet Physics Doklady* 7, 1963 (러시아어 원문 1962).
- Munro, J. I. & Wild, S. "Nearly-optimal mergesorts: Fast, practical sorting methods that optimally adapt to existing runs." *European Symposium on Algorithms (ESA)*, 2018 — powersort.
- Bentley, J. *Programming Pearls*, 2nd ed., Addison-Wesley, 2000 — 올바른 이진 탐색 작성.
