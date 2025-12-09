import math
import sys
sys.setrecursionlimit(10000)

from tree_visualizer import print_tree


class TreeNode:
    def __init__(self, val, idx):
        self.val = val
        self.idx = idx
        self.left = None
        self.right = None


class RMQ_LCA:
    def __init__(self, arr):
        """
        Build full RMQ structure on initialization.
        """
        self.arr = arr
        self.n = len(arr)

        # Step 1: Cartesian Tree
        self.root = self._build_cartesian_tree(arr)

        # Step 2: Euler tour
        self.tour, self.depths, self.first = self._euler_tour(self.root)

        # Step 3: Sparse Table on depths
        self.st = self._build_sparse_table(self.depths)

    def _build_cartesian_tree(self, arr):
        stack = []
        nodes = [TreeNode(v, i) for i, v in enumerate(arr)]
        root = None

        for node in nodes:
            last = None

            while stack and node.val < stack[-1].val:
                last = stack.pop()

            if stack:
                stack[-1].right = node
            if last:
                node.left = last

            stack.append(node)

        while len(stack) > 1:
            stack.pop()
        return stack[0]

    def _euler_tour(self, node, depth=0, tour=None, depths=None, first=None):
        if tour is None:
            tour = []
            depths = []
            first = {}

        if not tour or tour[-1] is not node:
            tour.append(node)
            depths.append(depth)
            if node.idx not in first:
                first[node.idx] = len(tour) - 1

        if node.left:
            self._euler_tour(node.left, depth + 1, tour, depths, first)
            if tour[-1] is not node:
                tour.append(node)
                depths.append(depth)

        if node.right:
            self._euler_tour(node.right, depth + 1, tour, depths, first)
            if tour[-1] is not node:
                tour.append(node)
                depths.append(depth)

        return tour, depths, first

    def _build_sparse_table(self, depths):
        n = len(depths)
        k = int(math.log2(n)) + 1

        st = [[0] * k for _ in range(n)]

        for i in range(n):
            st[i][0] = i

        j = 1
        while (1 << j) <= n:
            step = 1 << (j - 1)
            i = 0
            while i + (1 << j) <= n:
                left = st[i][j - 1]
                right = st[i + step][j - 1]
                st[i][j] = left if depths[left] < depths[right] else right
                i += 1
            j += 1

        return st

    def _rmq_depths(self, l, r):
        if l > r:
            l, r = r, l

        k = int(math.log2(r - l + 1))
        left = self.st[l][k]
        right = self.st[r - (1 << k) + 1][k]
        return left if self.depths[left] < self.depths[right] else right

    def _lca(self, u_idx, v_idx):
        l = self.first[u_idx]
        r = self.first[v_idx]
        best = self._rmq_depths(l, r)
        return self.tour[best]

    # API query
    def rmq(self, L, R):
        """
        Returns (index, value) of min element in arr[L:R].
        """
        node = self._lca(L, R)
        return node.idx, self.arr[node.idx]


if __name__ == "__main__":
    arr = [4, 2, 5, 1, 8, 0, 3, 1, 9]

    rmq = RMQ_LCA(arr)
    print('Tree:')
    print_tree(rmq.root)

    L, R = 3, 5
    idx, val = rmq.rmq(L, R)
    print(f"RMQ({L},{R}) = arr[{idx}] = {val}")
