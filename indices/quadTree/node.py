from collections import namedtuple
from itertools import product
from copy import deepcopy

Extent = namedtuple('Extent', ['x', 'y', 'w', 'h'])

class Node():
    
    __slots__ = ('nw','ne','sw','se','extent','data')

    def __init__(self, data, x, y, w, h):
        self.nw, self.ne, self.sw, self.se = [None,None,None,None]
        self.extent = Extent(x, y, w, h)
        print(data)
        self.data = data

    def __contains__(self, point):
        return self.extent.x <= point[0] <= self.extent.x + self.extent.w and \
        self.extent.y <= point[1] <= self.extent.y + self.extent.h

    @property
    def children(self):
        return self.nw, self.ne, self.se, self.sw
    
    @children.setter
    def children(self, nodes):
        self.nw, self.sw, self.ne, self.se = nodes

    @property
    def isleaf(self):
        return not any(self.children)

    def split_node(self):
        sw = self.extent.w/2
        sh = self.extent.h/2
        self.children = [Node(self.data, *vertex, sw, sh) for vertex in 
        product([self.extent.x,self.extent.x+sw],[self.extent.y+sh,self.extent.y])]

if __name__=='__main__':
    point = (2.5,2.5)
    point2 = (0,0)
    point3 = (5,5)
    extent = [0,0,5,5]
    node = Node(point,*extent)
    print(point in node)
    print(point2 in node)
    print(point3 in node)
    node.split_node()
    for child in node.children:
        print(child.extent)
        print(point in child)
        print(point2 in child)
        print(point3 in child)