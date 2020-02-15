from collections import deque
from collections.abc import Iterable
from node import Node


class QuadTree:

    def __init__(self, data, tree_extent=None, max_depth=8, copy_data=True):
        if tree_extent is None:
            if isinstance(data, Iterable):
                bx = min([p[0] for p in data])
                tx = max([p[0] for p in data])
                by = min([p[1] for p in data])
                ty = max([p[1] for p in data])
                tree_extent = [bx, by, tx, ty]
            else:
                raise ValueError(f"Your input did not include an extent for the tree, and it was not possible to get an extent from your input of type {type(data)}")
        if copy_data:
            data = data.copy()
        self.root = Node(data, *tree_extent, depth=0)
        self.max_depth = max_depth
        self.indexed_points = []
        if isinstance(data, Iterable):
            self.index(self.root)

    @property
    def extent(self):
        return self.root.extent

    def index(self, root):
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()
            if node.depth == self.max_depth:
                # self.indexed_points.extend(node.data)
                continue
            if len(node.data) <= 1:
                continue
            if node.isleaf:
                node.split_node()
            for i, value in enumerate(node.data):
                # TODO make formula to find which quad a point is in a node
                for child in node.children:
                    if child.data:
                        if value in child.data:
                            continue
                    if value in child:
                        child.data.append(value)
                        break
            node.data.clear()
            node_list.extend(node.children)

    def index_data(self, val):
        node = self.search(val)
        if node is None:
            return
        if node.data:
            if val in node.data:
                return
        node.data.append(val)
        self.index(node)
        self.indexed_points.append(val)

    def search(self, data):
        if data in self.root:
            node = self.root
            while not node.isleaf:
                t = [child for child in node.children if data in child]
                for n in t:
                    if data in n.data:
                        return n
                    node = n
                    break
            return node

    def __iter__(self):
        yield from self.root
