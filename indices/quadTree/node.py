from collections import namedtuple
from copy import deepcopy
from itertools import product
from math import floor
# from functools import lru_cache


class Extent(namedtuple('Extent', ['x', 'y', 'w', 'h'])):
    def __str__(self):
        return f"(bottom_left=({self.x},{self.y}),"\
        f"top_right=({self.x+self.w},{self.y+self.h}))"


class Node():

    __slots__ = ('nw','ne','sw','se','extent','data','depth')

    def __init__(self, data, x, y, w, h,depth):
        self.nw, self.ne, self.sw, self.se = [None,None,None,None]
        self.extent = Extent(x, y, w, h)
        self.data = data
        self.depth = depth

    def __contains__(self, point):
        return self.extent.x <= point[0] <= self.extent.x + self.extent.w and \
            self.extent.y <= point[1] <= self.extent.y + self.extent.h


    def get_relevant_child(self, data):
        x = floor((data[0] - self.extent.x) / (self.extent.w/2))
        x = x - floor(x / 2)
        y = floor((data[1] - self.extent.y) / (self.extent.h/2))
        y = y - floor(y / 2)
        # print(x,y)
        # print(x*2+y)
        return self.get_children_for_index()[x * 2 + y]

    def __iter__(self):
        yield self
        for child in filter(None, self.children):
            yield from child


    def get_children_for_index(self):
        return self.sw,self.nw,self.se,self.ne

    @property
    def children(self):
        return self.se, self.sw, self.ne, self.nw
    
    @children.setter
    def children(self, nodes):
        self.nw, self.sw, self.ne, self.se = nodes

    @property
    def isleaf(self):
        return not any(self.children)

    def split_node(self):
        sw = self.extent.w/2
        sh = self.extent.h/2
        self.children = [Node([], *vertex, sw, sh, self.depth+1) for vertex in 
        product([self.extent.x,self.extent.x+sw],[self.extent.y+sh,self.extent.y])]

    def __str__(self):
        return "\nNode______________________________________________________________\n"+self.extent.__str__() + f"\n data: {(str(self.data))} \n__________________________________________________________________"
