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
        self.root = Node([], [], *tree_extent, depth=0)
        if max_depth == 0:
            raise ValueError("Max depth has to be >= 1")
        self.max_depth = max_depth
        self.indexed_points = []
        if isinstance(data, Iterable) and data:
            self.indexed_points = list(set(data.copy()))
            if self.max_depth == 1:
                self.root.data = list(data)
            else:
                self.index(data, indices)

    @property
    def extent(self):
        return self.root.extent

    # def index(self, root):
    #     node_list = deque([root])
    #     while node_list:
    #         node = node_list.popleft()

    #         if node.depth == self.max_depth:
    #             continue

    #         if not node.data:
    #             continue
            
    #         if node.isleaf:
    #             node.split()

    #         indexed = []
    #         for child in node.children:
    #             in_data = [True if d in child and d not in child.data else False for d in node.data]
    #             data = list(compress(node.data, in_data))
    #             indices = list(compress(node.indices, in_data))
    #             child.data.extend(data)
    #             child.indices.extend(indices)
    #             # indexed.extend(child.data)
    #             node.data = list(compress(node.data, map(not_, in_data)))
    #             node.indices = list(compress(node.indices, map(not_, in_data)))

    #         node_list.extend(node.children)

    def index(self, data, indices):
        if not isinstance(data, Iterable):
            data = list(data)
            indices = list(indices)
        for d, i in zip(data, indices):
            node = self.search(d)
            if isinstance(node, Node):
                continue
            node = self.root
            if node.depth == self.max_depth:
                node.data.append(d)
                node.indices.append(i)
                continue
            if node.isleaf:
                node.split()
            while not node.isleaf:
                for child in node.children:
                    if d in child:
                        child.data.append(d)
                        child.indices.append(i)
                        node = child
                        break
                node.data.remove(d)
                node.indices.remove(d)
                
            
            # bool_data = [True if d in child and d not in child.data else False for d in node.data]
            # child_data = list(compress(node.data, bool_data))
            # child_indices = list(compress(node.indices, bool_data))
            # child.data.extend(child_data)
            # child.indices.extend(child_indices)
            # node.data = list(compress(node.data, map(not_, bool_data)))
            # node.indices = list(compress(node.indices, map(not_, bool_data)))
            
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

    def search(self, data, root=None):
        if root is None:
            root = self.root
        if data in root:
            node = root
            while not node.isleaf:
                children = [child for child in node.children if data in child]
                for child in children:
                    if data in child.data:
                        return child
                    node = child
            return None
        raise f"{data} not in tree with extent {self.extent}"

    def __iter__(self):
        yield from self.root
