import random
import time
from prettytable import PrettyTable

from . import RMQ_SegmentTree
from . import RMQ_LCA

random.seed(42)

def measure_build_time(arr, rmq_class):
    start = time.perf_counter()
    rmq_class(arr)
    end = time.perf_counter()
    return end - start


if __name__ == "__main__":
    array_sizes = [10, 100, 1000, 10_000, 100_000, 1_000_000]
    trials_per_size = 25

    table = PrettyTable()
    table.field_names = ["Array Size", "SegmentTree Min (s)", "LCA-RMQ Min (s)"]

    for n in array_sizes:
        seg_times = []
        lca_times = []

        for _ in range(trials_per_size):
            arr = [random.randint(0, 10_000) for _ in range(n)]
            seg_times.append(measure_build_time(arr, RMQ_SegmentTree))
            lca_times.append(measure_build_time(arr, RMQ_LCA))

        min_seg = min(seg_times)
        min_lca = min(lca_times)

        table.add_row([f"{n:,}", f"{min_seg:.6f}", f"{min_lca:.6f}"])
        print(f'Done for size: {n}')

    print(table)
