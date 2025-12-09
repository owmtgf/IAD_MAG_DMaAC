import random
import time
from prettytable import PrettyTable

from . import RMQ_SegmentTree
from . import RMQ_LCA

random.seed(42)

# -------------------------------
# Measure RMQ query time
# -------------------------------
def measure_query_time(rmq_obj, queries, method='rmq'):
    times = []
    for L, R in queries:
        start = time.perf_counter()
        if method == 'rmq':
            rmq_obj.rmq(L, R)
        elif method == 'min':
            _ = min(rmq_obj[L:R+1])
        end = time.perf_counter()
        times.append(end - start)
    return min(times) * 1000  # minimum query time

# -------------------------------
# Main evaluation
# -------------------------------
if __name__ == "__main__":
    array_sizes = [10, 100, 1000, 10_000, 100_000, 1_000_000]
    queries_per_size = 50  # number of random L-R queries

    table = PrettyTable()
    table.field_names = ["Array Size", "Naive min() (ms)", "SegmentTree RMQ (ms)", "LCA-RMQ (ms)"]

    for n in array_sizes:
        # Generate one array per size (same array for all methods)
        arr = [random.randint(0, 10_000) for _ in range(n)]

        # Generate random queries
        query_len = max(1, n // 100)  
        queries = []

        for _ in range(queries_per_size):
            start = random.randint(0, n - query_len)
            end = start + query_len - 1
            queries.append((start, end))

        # Build RMQ structures
        seg_rmq = RMQ_SegmentTree(arr)
        lca_rmq = RMQ_LCA(arr)

        # Measure minimum query time for each
        min_seg = measure_query_time(seg_rmq, queries, method='rmq')
        min_lca = measure_query_time(lca_rmq, queries, method='rmq')
        min_naive = measure_query_time(arr, queries, method='min')

        table.add_row([f"{n:,}", f"{min_naive:.6f}", f"{min_seg:.6f}", f"{min_lca:.6f}"])
        print(f'Done for size: {n}')

    print(table)
