from collections import deque
from collections.abc import Iterable
from .node import Node


class QuadTree:

    def __init__(self, data=[], indices=[], tree_extent=None, max_depth=8, copy_data=True):
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
        self.root = Node([], [], *tree_extent, depth=0)
        self.max_depth = max_depth
        self.indexed_points = []
        if isinstance(data, Iterable):
            self.index(data, indices, self.root, copy_data)

    @property
    def extent(self):
        return self.root.extent

    def index(self, data, indices, root=None, copy=True):

        if copy:
            data = data.copy()

        while data:
            if data[-1] not in self.root:
                raise ValueError("{data} is not in this trees extent: {self.root.extent}")

            if root is None:
                node = self.root
            else:
                node = root

            while node.depth < self.max_depth:
                if node.data and node.isleaf:
                    node.split()
                    self.index(node.data, node.indices, node, False)
                    continue
                elif node.isleaf:
                    break

                children = [child for child in node.children if data[-1] in child]
                if children:
                    if data[-1] in children[0].data:
                        break
                    node = children[0]
            if data[-1] in node.data:
                break

            node.data.append(data.pop())
            node.indices.append(indices.pop())

            # node_list.extend(node.children)

    def index_data(self, val, index, copy=True):
        if copy:
            val = val.copy()
            index = index.copy()
        node = self.search(val)

        if node is None:
            self.index(val)
            self.indexed_points.append(val)

    def search(self, data):
        if data in self.root:
            node = self.root
            if data in node.data:
                return node
            while not node.isleaf:
                children = [child for child in node.children if data in child]
                if children:
                    if data in children[0].data:
                        return children[0]
                    node = children[0]
            return None
        raise ValueError("{data} is not in this trees extent: {self.root.extent}")

    def __iter__(self):
        yield from self.root
