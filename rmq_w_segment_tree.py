from tree_visualizer import print_tree

class TreeNode:
    def __init__(self, val, idx, start=None, end=None):
        self.val = val
        self.idx = idx
        self.start = start
        self.end = end
        self.left = None
        self.right = None


class RMQ_SegmentTree:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.root = self._build(0, self.n - 1)

    def _build(self, l, r):
        """Recursively build segment tree."""
        if l == r:
            return TreeNode(self.arr[l], l, l, r)

        mid = (l + r) // 2
        left_child = self._build(l, mid)
        right_child = self._build(mid + 1, r)

        if left_child.val <= right_child.val:
            node_val, node_idx = left_child.val, left_child.idx
        else:
            node_val, node_idx = right_child.val, right_child.idx

        node = TreeNode(node_val, node_idx, l, r)
        node.left = left_child
        node.right = right_child
        return node

    def _query(self, node, L, R):
        """Recursive RMQ query with segment bounds."""
        if node is None:
            return TreeNode(float('inf'), -1, 0, 0)

        if node.end < L or node.start > R:
            return TreeNode(float('inf'), -1, 0, 0)

        if L <= node.start and node.end <= R:
            return node

        left_res = self._query(node.left, L, R)
        right_res = self._query(node.right, L, R)

        return left_res if left_res.val <= right_res.val else right_res

    def rmq(self, L, R):
        """Return (index, value) of minimum element in arr[L:R]."""
        node = self._query(self.root, L, R)
        return node.idx, node.val
    
    
if __name__ == "__main__":
    arr = [4, 2, 5, 1, 8, 0, 3, 1, 9]

    rmq = RMQ_SegmentTree(arr)
    print('Tree:')
    print_tree(rmq.root)

    L, R = 3, 5
    idx, val = rmq.rmq(L, R)
    print(f"RMQ({L},{R}) = arr[{idx}] = {val}")
