from collections import deque
from collections.abc import Iterable
from itertools import compress
from .node import Node
from operator import not_


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
        self.root = Node(data, indices, *tree_extent, depth=0)
        self.max_depth = max_depth
        self.indexed_points = []
        if isinstance(data, Iterable) and data:
            self.indexed_points = list(set(data.copy()))
            self.index(self.root)

    @property
    def extent(self):
        return self.root.extent

    def index(self, root):
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()

            if node.depth == self.max_depth:
                continue

            if not node.data:
                continue
            
            if node.isleaf:
                node.split()

            indexed = []
            for child in node.children:
                in_data = [True if d in child and d not in child.data else False for d in node.data]
                data = list(compress(node.data, in_data))
                indices = list(compress(node.indices, in_data))
                child.data.extend(data)
                child.indices.extend(indices)
                # indexed.extend(child.data)
                node.data = list(compress(node.data, map(not_, in_data)))
                node.indices = list(compress(node.indices, map(not_, in_data)))
            # node.data.clear()
            # node.indices.clear()

            # for i, value in enumerate(node.data):
            #     # TODO make formula to find which quad a point is in a node
            #     for child in node.children:
            #         if value in child:
            #             if value in child.data:
            #                 break
            #             child.data.append(value)
            #             child.indices.append(node.indices[i])
            #             break

            # node.data.clear()
            # node.indices.clear()

            node_list.extend(node.children)

    def index_data(self, val, index):
        # Checking index correctness is responsibility of user
        node = self.search(val)

        if node is None:
            raise ValueError(f"{val} not in this QuadTree extent: {self.extent}")

        if node.data:
            if val in node.data:
                return

        node.data.append(val)
        node.indices.append(index)

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
        raise f"{data} not in tree with extent {self.extent}"

    def __iter__(self):
        yield from self.root
