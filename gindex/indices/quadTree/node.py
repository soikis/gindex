from itertools import product


class Extent():

    __slots__ = ['x', 'y', 'w', 'h']

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __contains__(self, other_extent):
        # return self.x <= other_extent[0] <= other_extent[2] <= self.x + self.w and \
        #     self.y <= other_extent[1] <= other_extent[3] <= self.y + self.h
        return self.x <= other_extent[0] <= self.x + self.w and \
            self.y <= other_extent[1] <= self.y + self.h

    def area(self):
        return (self.w - self.x)**2

    def __str__(self):
        return f"(bottom_left=({self.x},{self.y}),"\
            f"top_right=({self.x+self.w},{self.y+self.h}))"


class Node():

    __slots__ = ('nw', 'ne', 'sw', 'se', 'extent', 'data', 'depth', 'indices', 'area')

    def __init__(self, data, indices, x, y, w, h, depth=8):
        self.nw, self.ne, self.sw, self.se = [None, None, None, None]
        self.extent = Extent(x, y, w, h)
        self.data = list(data)
        self.indices = list(indices)
        self.depth = depth
        self.area = self.extent.area()

    def __contains__(self, check_extent):
        return check_extent in self.extent

    def __iter__(self):
        yield self
        for child in filter(None, self.children):
            yield from child

    @property
    def children(self):
        return self.sw, self.nw, self.se, self.ne

    @children.setter
    def children(self, nodes):
        self.sw, self.nw, self.se, self.ne = nodes

    @property
    def isleaf(self):
        return self.sw is None

    def split(self):
        """Return order = sw,nw,se,ne"""
        sw = self.extent.w / 2
        sh = self.extent.h / 2
        self.children = [Node([], [], *vertex, sw, sh, self.depth + 1) for vertex in
                        product([self.extent.x, self.extent.x + sw],
                        [self.extent.y, self.extent.y + sh])]

    def __str__(self):
        return f"\nNode{'_______________'*4}\n" + self.extent.__str__() + \
            f"\n data: {str(list(zip(self.data,self.indices)))} \n{'_______________'*4}"
