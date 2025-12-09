def tree_height(node):
    if not node:
        return 0
    return 1 + max(tree_height(node.left), tree_height(node.right))


def collect_levels(root):
    """Returns list of levels, each is list of nodes or None."""
    h = tree_height(root)
    levels = []
    current = [root]
    for _ in range(h):
        levels.append(current)
        nxt = []
        for n in current:
            if n:
                nxt.append(n.left)
                nxt.append(n.right)
            else:
                nxt.append(None)
                nxt.append(None)
        current = nxt
    return levels


def print_tree(root):
    if not root:
        print("<empty>")
        return

    levels = collect_levels(root)
    H = len(levels)

    if H > 8:
        print(f'{__name__}: Tree heihgt={H} seems to large for console output. Tree can\'t be printed.')
        return

    # Compute node widths on last level
    last = levels[-1]
    widths = [len(f'[{n.start}:{n.end}]' if hasattr(n, 'start') else str(n.idx)) if n else 1 for n in last]
    total_width = sum(widths) + (len(widths) - 1) * 1  # spaces = 1 between leaves

    # For every level, segments = 2^level
    for lvl, nodes in enumerate(levels):
        seg_count = len(nodes)
        seg_width = total_width / seg_count  # float, but OK

        # ----------- PRINT BRANCHES (for lvl>0) ------------
        if lvl > 0:
            line = [" "] * total_width
            parents = levels[lvl - 1]
            parent_seg_width = total_width / len(parents)

            for i, p in enumerate(parents):
                if not p:
                    continue
                parent_center = int((i + 0.5) * parent_seg_width)

                left_i = 2 * i
                right_i = 2 * i + 1

                # left branch
                if nodes[left_i]:
                    left_center = int((left_i + 0.5) * seg_width)
                    line[left_center] = "/"

                # right branch
                if nodes[right_i]:
                    right_center = int((right_i + 0.5) * seg_width)
                    line[right_center] = "\\"

            print("".join(line))

        # ------------- PRINT NODE LINE -------------
        line = [" "] * total_width

        for i, n in enumerate(nodes):
            if not n:
                continue
            if hasattr(n, 'start'):
                s = f'[{n.start}:{n.end}]'
            else:
                s = str(n.idx)
            c = int((i + 0.5) * seg_width)
            start = c - len(s) // 2
            for j, ch in enumerate(s):
                pos = start + j
                if 0 <= pos < total_width:
                    line[pos] = ch

        print("".join(line))