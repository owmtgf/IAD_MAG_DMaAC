import pytest
import random
from rmq_w_lca import RMQ_LCA

random.seed(42)

# ---------------------------------------------------------------------
# TEST GENERATOR: several arrays of different sizes
# ---------------------------------------------------------------------

INT_TEST_CASES = [
    (lambda: [random.randint(-100, 100) for _ in range(1)], 10_000),
    (lambda: [random.randint(-100, 100) for _ in range(2)], 10_000),
    (lambda: [random.randint(-100, 100) for _ in range(7)], 10_000),
    (lambda: [random.randint(-1000, 1000) for _ in range(100)], 10_000),
    (lambda: [random.randint(-100, 100) for _ in range(751)], 10_000),
    (lambda: [random.randint(0, 10000) for _ in range(10_000)], 10_000),
    (lambda: [random.randint(0, 10000) for _ in range(100_000)], 10_000),
    (lambda: [random.randint(-1, 10000) for _ in range(100_000)], 10_000),
]
FLOAT_TEST_CASES = [
    (lambda: [random.uniform(-10, 10) for _ in range(30)], 10_000),
    (lambda: [random.uniform(-1e6, 1e6) for _ in range(100)], 10_000),
    (lambda: [random.gauss(0, 1) for _ in range(50)], 10_000),            # normal distribution
    (lambda:[random.random() for _ in range(20)], 10_000),                # uniform 0..1
    (lambda: [random.uniform(-1, 1) for _ in range(10_000)], 10_000),         # dense small magnitudes
    (lambda: [float(i) for i in range(1000)], 10_000),                     # monotonic floats
]


@pytest.mark.parametrize("arr_gen, num_tests", INT_TEST_CASES + FLOAT_TEST_CASES)
def test_rmq_against_naive(arr_gen, num_tests):
    """
    Compare RMQ via LCA against naive min(arr[L:R+1])
    """
    # Generate array (important: generate inside test)
    arr = arr_gen()
    n = len(arr)

    # Build LCA RMQ structures
    rmq = RMQ_LCA(arr)

    # Run random RMQ queries
    for _ in range(num_tests):
        L = random.randint(0, n - 1)
        R = random.randint(0, n - 1)
        if L > R:
            L, R = R, L

        _, rmq_val = rmq.rmq(L, R)
        naive_val = min(arr[L:R + 1])

        assert rmq_val == naive_val, (
            f"Mismatch on test case\n"
            f"range=({L},{R}) expected={naive_val}, got={rmq_val}"
        )