from itertools import product
from collections.abc import Iterable
from collections import OrderedDict
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
    __slots__ = ("minx", "miny", "maxx", "maxy", "area")

    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.area = (self.maxx - self.minx) * (self.maxy - self.miny)

    def __contains__(self, data):
        """Return True if a data (minx, miny, maxx, maxy) falls inside the extent with the *in* operator else, return False.

        Warning: It is the users responsebility to make sure that the data is in the correct format.
            e.g making sure that the minimum x of data IS bigger than or equal to the maximum x of data.

        Args:
            data (tuple(float, float, float ,float)): An (minx, miny, maxx, maxy) tuple.

        Returns:
            bool: True if data in extent, False otherwise.
        """
        return self.minx <= data[0] and data[2] <= self.maxx and \
            self.miny <= data[1] and data[3] <= self.maxy

    def __iter__(self):
        yield self.minx
        yield self.miny
        yield self.maxx
        yield self.maxy

    def __str__(self):
        return f"(bottom_left=({self.minx},{self.miny}),"\
            f"top_right=({self.maxx},{self.maxy}))"


# TODO make a Node1dD, Node2D and Node3D
# TODO make children into a dict with the names, use __setattr__ and __getattr__
# TODO for data use a binary tree (the index lookup will need to be different)
class Node():

    __slots__ = ("children", "extent", "data", "depth", "indices", "is_leaf")

    def __init__(self, minx, miny, maxx, maxy, depth, data=[], indices=[], verify_inputs=False, is_leaf=True):  # TODO change the order of input in tree.
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
        self.children = {"nw": None, "ne": None, "sw": None, "se": None}
        if verify_inputs:
            data, indices = self.verify_inputs(minx, miny, maxx, maxy, data, indices)
        self.extent = Extent(minx, miny, maxx, maxy)
        self.data = data
        self.indices = indices
        self.depth = depth
        self.is_leaf = is_leaf

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

        for name, corners in zip(self.children.keys(), child_vertices):
            self.children[name] = Node(*corners[0], *corners[1], data=[], indices=[], depth=self.depth + 1)  # data and indices need to be specified because, in the scope, they are equal to this nodes data and indices.
        # self.children = {name: Node(*corners[0], *corners[1], depth=self.depth + 1)
        #                 for (name, corners) in zip(self.children.keys(), child_vertices)}  # TODO make a verify input function in utils.

        self._pass_data_to_children()

        self.is_leaf = False

    def _pass_data_to_children(self):
        """Move the data from this node to it's children, if possible.

        Returns:
            NoneType: None.
        """
        # TODO might be able to use this with pop and recursion (tail-recursion)
        remove_list = []
        for data_point, index in zip(self.data, self.indices):
            if calc_area(*data_point) <= self.extent.area / 4:  # The area of 1 child is 1/4 of the parent.
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
        counter = 0
        res_child = self
        for child in self.children.values():
            if data_point in child.extent:
                counter += 1
                if counter > 1:
                    return self
                res_child = child
        return res_child

    # TODO might be able to use recursion
    def to_dict(self):
        node_dict = OrderedDict()
        node_dict["depth"] = self.depth
        node_dict["is_leaf"] = self.is_leaf
        node_dict["extent"] = tuple(self.extent)
        node_dict["data"] = self.data
        node_dict["indices"] = self.indices
        if not self.is_leaf:
            node_dict["children"] = dict()
            for name, child in self.children.items():
                node_dict["children"][name] = child.to_dict()
        return node_dict

    # TODO might be able to use recursion.
    @staticmethod
    def from_dict(node_dict):
        depth = node_dict["depth"]
        is_leaf = node_dict["is_leaf"]
        extent = node_dict["extent"]
        data = list(map(tuple, node_dict["data"]))
        indices = node_dict["indices"]
        node = Node(*extent, data=data, indices=indices, depth=depth, is_leaf=is_leaf)
        if not node.is_leaf:
            for name, child in node_dict["children"].items():
                node.children[name] = Node.from_dict(child)
        return node

    def __str__(self):
        return f"\nNode{'_______________'*4}\n" + self.extent.__str__() + \
            f"\n data: {str(tuple(zip(self.data,self.indices)))} \n{'_______________'*4}"
