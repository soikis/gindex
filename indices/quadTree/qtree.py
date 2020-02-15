from collections import Counter, deque
from collections.abc import Iterable
from itertools import compress
from node import Extent, Node

class QTree:

    def __init__(self, data, tree_extent=None, max_depth=8, copy_data=True):
        if tree_extent == None:
            if isinstance(data,Iterable):
                bx = min([p[0] for p in data])
                tx = max([p[0] for p in data])
                by = min([p[1] for p in data])
                ty = max([p[1] for p in data])
                tree_extent = [bx,by,tx,ty]
            else:
                raise ValueError(f"Your input did not include an extent for the tree, and it was not possible to get an extent from your input of type {type(data)}")
        if copy_data:
            data = data.copy()
        self.root = Node(data, *tree_extent, depth=0)
        self.max_depth = max_depth
        self.indexed_points = []
        if isinstance(data,Iterable):
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
            if len(node.data) <= 1:
                continue
            if node.isleaf:
                node.split_node()
            for i,value in enumerate(node.data):
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

    # def add_to_index(self, data):
    #     node = self.search_tree(data, self.root)
    #     if node == None:
    #         return
    #     if node.data:
    #         if node.data[0] == data:
    #             return
    #     node.data.append(data)
    #     self.index(node)
    #     self.indexed_points.append(data)

    def add_node(self, val):
        """
        Adds a node containing val to the QT.
        @param val: the value to be added.
        @return: None
        """
        node = self.search_with_list(val)
        if node == None:
            return
        if node.data:
            if val in node.data:
                return
        node.data.append(val)
        self.index(node)
        self.indexed_points.append(val)

    # def add_data(self, val):
    #     node = self.search_tree(val, self.root)
    #     if node == None:
    #         return
    #     if node.data:
    #         if val in node.data:
    #             return
    #     node.data.append(val)
    #     self.index(node)
    #     self.indexed_points.append(val)

    # def search(self, val):
    #     """
    #     Searches the value val in the QT.
    #     @param val: the value to be searched
    #     @return: the node containing the value, else None.
    #     """
    #     assert val in self.root, f"{val} not in this index extent: {self.extent}"
    #     node = self.root
    #     while not node.isleaf:
    #         for son_s in "nw", "ne", "sw", "se":
    #             son = getattr(node, son_s)
    #             if son.data:
    #                 if val == son.data[0]:
    #                     return None
    #             if val in son:
    #                 node = son
    #                 break
    #     return node

    # def search_with_list2(self, data):
    #     if data in self.root:
    #         node = self.root
    #         while not node.isleaf:
    #             in_data = [1 if data in node.data else 0 for child in node.children]
    #             if any(in_data):
    #                 return node.children[in_data.index(1)]
    #             bool_list = [True if data in child else False for child in node.children]
    #             # t = [child for child in node.children if data in child]
    #             # for n in t:
    #             #     if any(n.data):
    #             #         if data in n.data:
    #             #             return 
    #             #     node = n
    #             #     break
    #             node = next(compress(node.children,bool_list))
    #         return node

    def search_with_list(self, data):
        if data in self.root:
            node = self.root
            while not node.isleaf:
                # in_data = [1 if (child.data[0] == data if any(child.data) else False) else 0 for child in node.children]
                # if any(in_data):
                #     return node.children[in_data.index(1)]
                # bool_list = [True if data in child else False for child in node.children]
                t = [child for child in node.children if data in child]
                for n in t:
                    if data in n.data:
                        return n
                    node = n
                    break
                # node = next(compress(node.children,bool_list))
            return node


    # def search_tree(self, data, root=None):
    #     if root == None:
    #         root = self.root
    #     if root.isleaf:
    #         if data in root:
    #             return root
    #         return None
    #     else:
    #         children = [self.search_tree(data, child_node) for child_node in root.children]
    #         return next(filter(None, children),None)

    def __iter__(self):
        yield from self.root


def main():
    from timeit import default_timer
    import random
    random.seed(a=10)
    data = [(random.randint(0, 128), random.randint(0, 128)) for _ in range(500)]
    sp=default_timer()
    qt = QTree(data, (0,0,128,128),4)
    # for i, d in enumerate(data, start=1):
    #     # print(i,d)
    #     # print(d in qt.indexed_points)
    #     qt.add_node(d)
    #     # qt.add_data(d)
    #     if i == len(data):
    #         # print(len(qt.indexed_points),len(set(data)))
    #         assert len(set(data)) == len(qt.indexed_points)
    np=default_timer()
    print(f'index time: {np-sp} seconds')
    sp=default_timer()
    for point in data:
        # node = qt.search_tree(point)
        node = qt.search_with_list(point)
        # print(node)
        # print(node.extent,node.data)
        # if len(node.data) > 1:
        #     print(node.extent,node.data)
    np=default_timer()
    print(f'search time: {np-sp} seconds')
if __name__ == "__main__":
    main()

# TODO check list search for correctnes vs new baseline