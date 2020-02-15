from collections import namedtuple, deque, Counter
from random import randint
import sys
import itertools as it
from qtree import QTree

class Rect(namedtuple("_Rect", "x, y, w, h")):
    def __contains__(self, point):
        """
        Checks if point is inside the rect.
        @type point: tuple
        @param point
        @return: bool
        """
        x, y = point
        if not self.x <= x <= self.x + self.w:
            return False
        if not self.y <= y <= self.y + self.h:
            return False
        return True

    def split(self):
        """
        Splits the rectangle.
        @return: List of splits.
        """
        w2, h2 = self.w / 2, self.h / 2
        return [Rect(self.x + w_r, self.y + h_r, w2, h2)
                for (h_r, w_r) in it.product([0, h2], [0, w2])]

    def __str__(self):
        return "[{}, {}, {}, {}]".format(self.x, self.y, self.w, self.h)


class Node:
    __slots__ = ("nw", "ne", "sw", "se", "val", "bounds")

    def __init__(self, nw=None, ne=None, sw=None, se=None, val=None, bounds=None):
        """
        Creates a node.
        @param nw: the nw son.
        @type nw: Node
        @param ne: the ne son.
        @type ne: Node
        @param sw: the sw son.
        @type sw: Node
        @param se: the se son.
        @type se: Node
        @param val: the node content
        @param bounds: the node bound
        @type bounds: Rect
        """
        self.nw, self.ne, self.sw, self.se = nw, ne, sw, se
        self.val = val
        self.bounds = bounds

    def __str__(self):
        return "<{}, {}>".format(self.val, self.bounds)

    @property
    def sons(self):
        """
        @return: tuple of sons (nw,ne,sw,se)
        """
        return self.nw, self.ne, self.sw, self.se

    @property
    def leaf(self):
        """
        @return: True if not any(self.sons)
        """
        return not any(self.sons)

    def __iter__(self):
        yield self
        for n in filter(None, self.sons):
            yield from n


class QuadTree:
    def __init__(self, data, width, height):
        """
        Creates a QT.
        @param data: sequence of contents.
        @type data: iterable
        @param width: The width of the area covered by the QT.
        @type width: float
        @param height: The height of the area covered by the QT.
        @type height: float
        @return:
        """
        rect = Rect(0, 0, width, height)
        self.size = 0
        self.root = Node(val=data, bounds=rect)
        if data:
            self._split(self.root)

    def add_node(self, val):
        """
        Adds a node containing val to the QT.
        @param val: the value to be added.
        @return: None
        """
        node = self.search_value(val)
        if node == None:
            return
        node.val.append(val)
        self._split(node)
        self.size += 1

    def _split(self, root):
        """
        @type node: Node
        """
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()
            if len(node.val) <= 1:
                continue
            if node.leaf:
                rects = node.bounds.split()
                for son, bounds_rect in zip(("nw", "ne", "sw", "se"), rects):
                    setattr(node, son, Node(val=[], bounds=bounds_rect))
            for val in node.val:
                for son in node.sons:
                    if val in son.bounds:
                        son.val.append(val)
                        break
            node.val.clear()
            node_list.extend(node.sons)

    def search(self, val):
        """
        Searches the value val in the QT.
        @param val: the value to be searched
        @return: the node containing the value, else None.
        """
        if val in self.root.bounds:
            depth = 0
            node = self.root
            while not node.leaf:
                for son_s in "nw", "ne", "sw", "se":
                    son = getattr(node, son_s)
                    if val in son.bounds:
                        # print('match!')
                        node = son
                        depth += 1
                        break
            return node
    
    def search_value(self, val):
        if val in self.root.bounds:
            node = self.root
            while not node.leaf:
                for son_s in "nw", "ne", "sw", "se":
                    son = getattr(node, son_s)
                    if son.val:
                        if val == son.val[0]:
                            return None
                    if val in son.bounds:
                        # print('match!')
                        node = son
                        break
            return node

    def __iter__(self):
        yield from self.root


def main():
    from timeit import default_timer
    import random
    random.seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(500)]
    st=default_timer()
    qt = QuadTree([],128,128)
    for i, d in enumerate(data, start=1):
        print(i,d)
        qt.add_node(d)
        if i == len(data):
            assert len(set(data)) == qt.size
    nt=default_timer()
    sp=default_timer()
    qt = QTree([], (0,0,128,128))
    for i, d in enumerate(data, start=1):
        print(i,d)
        qt.add_node(d)
        if i == len(data):
            print(qt.size)
            assert len(set(data)) == qt.size
    np=default_timer()
    print(nt-st)
    print(np-sp)
    # strt = default_timer()
    # for point in data:
    #     node = qt.search_with_list(point)
    #     print(node.extent,point)
    # end = default_timer()
    # print(end-strt)
if __name__ == "__main__":
    main()