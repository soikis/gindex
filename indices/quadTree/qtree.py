from collections import deque
from collections.abc import Iterable 

from node import Extent, Node


class QTree:

    def __init__(self, data, tree_extent=None, depth=8):
        if tree_extent == None:
            if isinstance(data,Iterable):
                bx = min([p[0] for p in data])
                tx = max([p[0] for p in data])
                by = min([p[1] for p in data])
                ty = max([p[1] for p in data])
                tree_extent = [bx,by,tx,ty]
            else:
                raise ValueError(f"Your input did not include an extent for the tree, and it was not possible to get an extent from your input of type {type(data)}")
        self.root = Node(data, *tree_extent)
        self.size = 0
        self.indexed_points = []
        self.depth = depth
        if data:
            self.index(self.root)
        
    @property
    def extent(self):
        return self.root.extent

    def choose_child(self, node, data):
        for name,child in zip(['nw', 'sw', 'se', 'ne'], node.children):
            if data in child:
                return name

    def index(self, root):
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()
            if len(node.node_data) <= 1:
                continue
            if node.isleaf:
                node.split_node()
            for val in node.node_data:
                # TODO make formula to find which quad a point is in a node
                for child in node.children:
                    if child.node_data:
                        if val == child.node_data[0]:
                            return None
                    if val in child:
                        child.node_data.append(val)
                        break
            node.node_data.clear()
            node_list.extend(node.children)

    def add_node(self, val):
        """
        Adds a node containing val to the QT.
        @param val: the value to be added.
        @return: None
        """
        node = self.search_tree(val, self.root)
        if node == None:
            return
        if node.node_data:
            if node.node_data[0] == val:
                return None
        node.node_data.append(val)
        self.index(node)
        self.indexed_points.append(val)
        self.size += 1

    def search_tree(self, data, root=None):
        if root == None:
            root = self.root
        if root.isleaf:
            if data in root:
                return root
            return None
        else:
            children = [self.search_tree(data, child_node) for child_node in root.children]
            # print(children)
            return next(filter(None, children),None)

    def __iter__(self):
        yield from self.root


    # def search(self, point):
    #     pass

# if __name__=='__main__':
#     points = [(2.5,2.5),(0,0),(5,5)]
#     extent = [0,0,5,5]
#     qtree = QTree(points, extent)
