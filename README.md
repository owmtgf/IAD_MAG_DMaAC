# Test Core

Run output validation for both algorithms (comparison with `min()`):
```sh
cd output_tests
pytest -v
```
All outputs is `OK` if all tests marked as `PASSED`.

Testing on 8 `integer` and 6 `float` arrays, each has various lenght and randomly initialized values, determined with fixed random state. All of 12 arrays tested on 10.000 random cuts `[L:R+1]`, which is totals to 120.000 tests.

You can also run `rmq_w_segment_tree.py` or `rmq_w_lca` itself with already prepared sample in `__main__` entry point.

# Evaluate Time

To evaluate build time, run:
```sh
python3 -m runtime_tests.evaluate_build_time
```
To evaluate query time, run:
```sh
python3 -m runtime_tests.evaluate_query_time
```

Time comparison in the `Measured Comparison` section.

# RMQ Implementations Complexity Analysis

## RMQ Using Segment Tree (`rmq_w_segment_tree.py`)

### Class: `RMQ_SegmentTree`

**Purpose:** Build a segment tree to answer RMQ in `O(log n)` time.

#### Functions & Time Complexity

| Function             | Complexity | Explanation                                                                                                   |
| -------------------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| `__init__`           | O(n)       | Calls `_build` once to recursively construct the tree; each array element corresponds to a leaf.              |
| `_build(l, r)`       | O(n)       | Recursively builds the tree. Each node is visited once; total nodes ~2n-1 → O(n).                             |
| `_query(node, L, R)` | O(log n)   | Each query traverses only relevant branches. In a binary tree of height ~log n, query visits ≤ 2*log n nodes. |
| `rmq(L, R)`          | O(log n)   | Wrapper around `_query`; tiny overhead.                                                                 |

#### Build Time Complexity

* **O(n)** — every node is created and initialized once.

#### Query Time Complexity

* **O(log n)** — only nodes along the path from root to leaves overlapping [L,R] are visited.

#### Memory Complexity

* **O(n)** — each node stores value, index, segment bounds, and two pointers. Total nodes ~2n-1.

---

## RMQ Using Cartesian Tree + Euler Tour + Sparse Table (`rmq_w_lca.py`)

### Class: `RMQ_LCA`

**Purpose:** Build RMQ using LCA (Lowest Common Ancestor) on Cartesian Tree. Queries are O(1) after preprocessing.

#### Functions & Time Complexity

| Function                      | Complexity | Explanation                                                                                |
| ----------------------------- | ---------- | ------------------------------------------------------------------------------------------ |
| `__init__`                    | O(n log n) | Builds Cartesian tree, Euler tour, and sparse table. Sparse table dominates.               |
| `_build_cartesian_tree(arr)`  | O(n)       | Uses stack to maintain nodes in increasing order. Each element pushed/popped at most once. |
| `_euler_tour(node)`           | O(n)       | Visits each tree node, recording tour and depth. Tour length ≤ 2n-1.                       |
| `_build_sparse_table(depths)` | O(n log n) | Sparse table is built for the depth array. Each of n positions fills up to log n levels.   |
| `_rmq_depths(l, r)`           | O(1)       | RMQ on depths using sparse table: 2 comparisons using precomputed intervals.               |
| `_lca(u_idx, v_idx)`          | O(1)       | Maps input indices to first occurrence in Euler tour, then calls `_rmq_depths`.            |
| `rmq(L, R)`                   | O(1)       | Calls `_lca` and returns minimum element; constant time after preprocessing.               |

#### Build Time Complexity

* **O(n log n)** — dominant step is building sparse table on Euler tour depths (~2n-1 length).
* Cartesian tree + Euler tour: O(n)
* Sparse table: O(n log n)

#### Query Time Complexity

* **O(1)** — uses precomputed sparse table to find minimum depth index in Euler tour, which gives LCA and RMQ.

#### Memory Complexity

* **O(n log n)** —

  * Euler tour: O(n) nodes (~2n-1)
  * Sparse table: O(n log n)
  * Cartesian tree nodes: O(n)

---

### Measured Comparison

**Build Time (seconds, minimum of 25 runs)**

| Array Size | SegmentTree RMQ (s) | LCA-RMQ (s) |
|------------|---------------------|-------------|
| 10         | 0.000010            | 0.000026    |
| 100        | 0.000096            | 0.000350    |
| 1,000      | 0.001097            | 0.005304    |
| 10,000     | 0.013677            | 0.078324    |
| 100,000    | 0.345162            | 1.099331    |
| 1,000,000  | 4.865172            | 15.826834   |

**Query Time (milliseconds, minimum of 50 runs; query window length = max(1, n / 100))**

| Array Size | Naive min() (ms) | SegmentTree RMQ (ms) | LCA-RMQ (ms) |
|------------|-----------------|----------------------|--------------|
| 10         | 0.000200        | 0.001300             | 0.000800     |
| 100        | 0.000300        | 0.004000             | 0.000900     |
| 1,000      | 0.000400        | 0.006400             | 0.001000     |
| 10,000     | 0.001600        | 0.010700             | 0.001300     |
| 100,000    | 0.030400        | 0.016300             | 0.001800     |
| 1,000,000  | 0.131600        | 0.026400             | 0.002700     |

### Notes
1. Segment Tree build is faster than LCA + Sparse Table, but queries are logarithmic.
2. LCA + Sparse Table has higher build cost but almost constant query time.
3. Naive `min()` query scales linearly with query length and array size, becoming very slow for large arrays.

