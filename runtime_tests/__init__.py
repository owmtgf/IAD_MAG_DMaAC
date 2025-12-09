import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from rmq_w_segment_tree import RMQ_SegmentTree
from rmq_w_lca import RMQ_LCA

__all__ = [
    "RMQ_SegmentTree",
    "RMQ_LCA"
]