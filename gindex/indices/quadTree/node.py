from itertools import product
from collections.abc import Iterable
from .utils import calc_area
from bisect import bisect_left
from itertools import compress

"""
Todo: (needs sphinx.ext.todo extension)

Note:

Raises:
    AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
    ValueError: If `param2` is equal to `param1`.

Yields: (instead of return)

Examples:

Attributes:
    for public class attributes

if @property then just explain the variable by type

https://www.sphinx-doc.org/en/1.5/ext/example_google.html
"""

# TODO fix documentation for all this shit
class Extent():
    __slots__ = ("minx", "miny", "maxx", "maxy")

    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    @property
    def area(self):
        return (self.maxx - self.minx) * (self.maxy - self.miny)

    def __contains__(self, data):
        """Return True if a data (x,y) falls inside the extent with the *in* operator else, return False.

        Warning: It is the users responsebility to make sure that the data is in the correct format. 
            e.g making sure that the minimum x of data IS bigger than or equal to the maximum x of data

        Args:
            data (tuple(float)): An (x,y) tuple.

        Returns:
            bool: True if data in extent, False otherwise.
        """
        return self.minx <= data[0] and data[2] <= self.maxx and \
            self.miny <= data[1] and data[3] <= self.maxy

    def __str__(self):
        return f"(bottom_left=({self.minx},{self.miny}),"\
            f"top_right=({self.maxx},{self.maxy}))"


# TODO make a Node1dD, Node2D and Node3D


class Node():

    __slots__ = ("nw", "ne", "sw", "se", "extent", "data", "depth", "indices", "is_leaf")

    def __init__(self, minx, miny, maxx, maxy, data=[], indices=[], verify_inputs=True, depth=8):  # TODO change the order of input in tree.
        """Node initializer. TODO edit Node to NodexD

        Args:
            minx (float): A value for the minimum x value of the node.
            miny (float): A value for the minimum y value of the node.
            maxx (float): A value for the maximum x value of the node.
            maxy (float): A value for the maximum y value of the node.
            data (list, optional): A list of all the data points in in the node.
            indices (list, optional): A list of all the data points indices in the node.
            verify_inputs (bool, optional): Whether to verify that the inputs are correct.
            depth (int, optional): A value for the depth of the node.

        Returns:
            NoneType: None.
        """
        # north-west, north-east, south-west, south-east children nodes of the current node, respectively.
        self.nw, self.ne, self.sw, self.se = [None, None, None, None]
        if verify_inputs:
            data, indices = self.verify_inputs(minx, miny, maxx, maxy, data, indices)
        self.extent = Extent(minx, miny, maxx, maxy)
        self.data = data
        self.indices = indices
        self.depth = depth
        self.is_leaf = True

    # TODO when making 1D, 2D and 3D make sure to insure those sizes in this function.
    def verify_inputs(self, minx, miny, maxx, maxy, data, indices):
        """Return data and indices in the correct format aswell as make sure that minx and miny are not bigger than maxx and maxy respectively.

        Args:
            minx (float): A value for the minimum x value of the node.
            miny (float): A value for the minimum y value of the node.
            maxx (float): A value for the maximum x value of the node.
            maxy (float): A value for the maximum y value of the node.
            data (list): A list of all the data points in in the node.
            indices (list): A list of all the data points indices in in the node.

        Returns:
            tuple: A tuple containing data and indices as list of tuples and list respectively.

        Raises:
            ValueError: If either minx or miny is bigger than or equal to maxx or maxy respectively.
        """
        if not isinstance(data, list) and isinstance(data, Iterable):
            data = list(map(tuple, data))
        elif not isinstance(data, Iterable):
            raise TypeError(f"Parameter 'data' of type {type(data)} is not iterable.")

        if not isinstance(indices, list) and isinstance(indices, Iterable):
            indices = list(indices)
        elif not isinstance(indices, Iterable):
            raise TypeError(f"Parameter 'indices' of type {type(data)} is not iterable.")

        if minx >= maxx or miny >= maxy:
            raise ValueError(f"Either {minx} or {miny} are bigger than or equal to {maxx} or {maxy} respectively.")

        return data, indices

    def __contains__(self, data_index):
        """Return True if point is in this nodes data, otherwise reutrn False. TODO fix documentation for index

        Args:
            point (tuple(float,float)): A tuple of floats that represent a data point.

        Returns:
            bool: True if point is in self.data, otherwise False.
        """
        index = bisect_left(self.data, data_index[0])
        if index != len(self.data) and self.data[index] == data_index[0]:
            if self.indices[index] == data_index[1]:
                return True
        return False

    # TODO check if docstring is correct
    def __iter__(self):
        """Yield this node and if it's children

        Yields:
            Node: When first called,  #TODO currently when it is called it yeilds itself even if it's not necessary.
        """
        yield self
        for child in filter(None, self.children):
            yield from child

    @property
    def children(self):
        """Return a tuple of all the child nodes of this node. Also sets them.

        Returns:
            tuple: tuple of all child nodes of this node.
        """
        return self.nw, self.sw, self.ne, self.se  # TODO I changed from se and ne TO ne and se CHANGE DOCUMENTATION

    @children.setter
    def children(self, nodes):
        self.nw, self.sw, self.ne, self.se = nodes

    def split(self):
        """Split this node to 4 new nodes and if necessary and possible, pass the data to it's children.

        Returns:
            NoneType: None.
        """
        x_split = (self.extent.maxx - self.extent.minx) / 2
        y_split = (self.extent.maxy - self.extent.miny) / 2

        child_vertices = [(vertex, (vertex[0] + x_split, vertex[1] + y_split)) for vertex in
                        product([self.extent.minx, self.extent.minx + x_split],
                                [self.extent.miny + y_split, self.extent.miny])]

        self.children = [Node(*corners[0], *corners[1], [], [], False, self.depth + 1) for corners in child_vertices]  # TODO make a verify input function in utils.

        self._pass_data_to_children()

        self.is_leaf = False

    def _pass_data_to_children(self):
        """Move the data from this node to it's children, if possible.

        Returns:
            NoneType: None.
        """
        remove_list = []
        for data_point, index in zip(self.data, self.indices):
            if calc_area(*data_point) <= self.sw.extent.area:  # self.sw is used to avoid calling the children property. TODO add and self.children exists
                node = self.get_relevant_child(data_point)
                if node is not self:
                    insertion = bisect_left(node.data, data_point)
                    node.data.insert(insertion, data_point)
                    node.indices.insert(insertion, index)
                    remove_list.append(0)
                else:
                    remove_list.append(1)
            else:
                remove_list.append(1)
        self.data = list(compress(self.data, remove_list))
        self.indices = list(compress(self.indices, remove_list))

    def get_relevant_child(self, data_point):
        """Return the child that has data_point inside its extent.

        Note: If data_point falls within multiple children, the data_point is considered to be inside self.  TODO In a point it's a top left priority

        Args:
            data_point (tuple): A data point in the correct format (minx,miny,maxx,maxy) TODO make sure that every type of node has a different format

        Returns:
            Node: The child Node that can contain the data.
        """
        children = [child for child in self.children if data_point in child.extent]  # Maybe self.children is needed, we will see. TODO self.children is needed to avoid yielding the first self
        if len(children) == 1:
            return children[0]
        else:
            return self

    def __str__(self):
        return f"\nNode{'_______________'*4}\n" + self.extent.__str__() + \
            f"\n data: {str(tuple(zip(self.data,self.indices)))} \n{'_______________'*4}"
