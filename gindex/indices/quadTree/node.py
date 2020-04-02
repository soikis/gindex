from itertools import product


class Extent():
    __slots__ = ('minx', 'miny', 'maxx', 'maxy')

    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def __contains__(self, point):
        return self.minx <= point[0] <= self.maxx and \
            self.miny <= point[1] <= self.maxy

    def __str__(self):
        return f"(bottom_left=({self.minx},{self.miny}),"\
            f"top_right=({self.maxx},{self.maxy}))"


class Node():
    __slots__ = ('nw', 'ne', 'sw', 'se', 'extent', 'data', 'depth', 'indices')

    def __init__(self, data, indices, minx, miny, maxx, maxy, depth=8):
        self.nw, self.ne, self.sw, self.se = [None, None, None, None]
        self.extent = Extent(minx, miny, maxx, maxy)
        self.data = data
        self.indices = indices
        self.depth = depth

    def __contains__(self, point):
        return point in self.data

    def __iter__(self):
        yield self
        for child in filter(None, self.children):
            yield from child

    @property
    def children(self):
        return self.nw, self.sw, self.se, self.ne

    @children.setter
    def children(self, nodes):
        self.nw, self.sw, self.ne, self.se = nodes

    @property
    def isleaf(self):
        return not any(self.children)

    def split(self):
        x_split = (self.extent.maxx - self.extent.minx) / 2
        y_split = (self.extent.maxy - self.extent.miny) / 2

        child_vertices = [(vertex, (vertex[0] + x_split, vertex[1] + y_split)) for vertex in
                        product([self.extent.minx, self.extent.minx + x_split],
                                [self.extent.miny + y_split, self.extent.miny])]

        self.children = [Node([], [], *corners[0], *corners[1], self.depth + 1) for corners
                        in child_vertices]

    def __str__(self):
        return f"\nNode{'_______________'*4}\n" + self.extent.__str__() + \
            f"\n data: {str(list(zip(self.data,self.indices)))} \n{'_______________'*4}"
