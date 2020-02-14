from node import Extent, Node
from collections import deque

class QTree:

    def __init__(self, data, tree_extent):
        self.root = Node(data, *tree_extent)
        self.size = 0
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
        node = self.search(val)
        node.node_data.append(val)
        self.index(node)
        self.size += 1

    def search(self, val):
        """
        Searches the value val in the QT.
        @param val: the value to be searched
        @return: the node containing the value, else None.
        """
        if val in self.root:
            node = self.root
            while not node.isleaf:
                for son_s in "nw", "ne", "sw", "se":
                    son = getattr(node, son_s)
                    if val in son:
                        node = son
                        break
            return node

    def __iter__(self):
        yield from self.root

    def assert_correct(self):
        for node in self:
            if node.node_data:
                assert (node.node_data[0] in node)

    # def search(self, point):
    #     pass

if __name__=='__main__':
    points = [(2.5,2.5),(0,0),(5,5)]
    extent = [0,0,5,5]
    qtree = QTree(points, extent)
