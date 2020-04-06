from collections.abc import Iterable
from .node import Node
from .utils import calc_area
from bisect import bisect_left, bisect


class QuadTree:

    # TODO if verify_input is True add a check for extensions in the index function
    def __init__(self, data=[], indices=[], tree_extent=None, max_depth=8, copy_data=True, verify_inputs=True, ndims=2):
        """QuadTree initializer.
            Number of dimensions of the data can be chosen. 1D - point(x, y) | 2D - extent(minx, miny, maxx, maxy) | 3D - 3D extent(minx, miny, maxx, maxy, minz, maxz)

        ..Note: If verify_inputs is True and the data you input into the tree is not in the correct format, it will be forced into the format and therfore might be errornous.
        Args:
            data (list or tuple, optional): A list of all the data points to index in the tree or a single data point of either type list or tuple in the correct format for the dimensions.
            indices (list or int, optional): A list of all the data points indices in the tree. TODO finish fixing the documentation and make sure that data and indices don't have to be lists (indices)
            tree_extent (tuple, optional): A 4 element list or tuple that contains the extent of the tree in the format of minx,miny,maxx,maxy.
            max_depth (int, optional): The maximum depth of this QuadTree.
            copy_data (bool, optional): Whether to copy the data or use the original list.
            verify_inputs (bool, optional): Whether to verify inputs or not.
            ndims (int): How many dimensions is this tree going to expand. (up to 3)

        Returns:
            NoneType: None.
        """
        if verify_inputs:
            if not isinstance(ndims, int):
                raise TypeError(f"parameter 'ndim' of type: '{type(ndims)}' should be of type 'int'.")

            if max_depth < 1:
                raise ValueError("parameter 'max_depth' with value of {max_depth} can't be lower than 1.")

            if len(data) != len(indices):
                raise IndexError(f"data of length {len(data)} is not the same as indices of length {len(indices)}")

        # If no extent is specified, calculate it
        if tree_extent is None:
            if isinstance(data, Iterable):
                bottom_x = min([p[0] for p in data])
                top_x = max([p[0] for p in data])
                bottom_y = min([p[1] for p in data])
                top_y = max([p[1] for p in data])
                tree_extent = (bottom_x, top_x, bottom_y, top_y)
            else:
                raise ValueError(f"Your input did not include an extent for the tree, and it was not possible to get an extent from your input of type {type(data)}")

        if copy_data:
            data = data.copy()

        self.root = Node(*tree_extent, verify_inputs=verify_inputs, depth=0)
        self.max_depth = max_depth

        if isinstance(indices, Iterable):
            self.index(data, indices)

    @property
    def extent(self):
        """Return the extent of this trees root.

        Returns:
            Extent: The extent of the root of this tree.
        """
        return self.root.extent

    def _find_deepest_node(self, data):
        if data in self.root.extent:
            node = self.root
            prev_node = None
            while not node.is_leaf and node is not prev_node:
                prev_node = node
                node = node.get_relevant_child(data)
            return node
        raise RuntimeError("Data extent {data} not in this tree's extent: {self.root.extent}")

    def _index_data_point(self, data, index):
        # Find the deepest node that this data point might be in.
        node = self._find_deepest_node(data)

        # If the data and indices list in this node are empty, append the data and index to them.
        if not node.data:
            node.data.append(data)
            node.indices.append(index)

        elif (data, index) not in node:
            # Only try to split the node if the area of data is smaller than the area of node.
            if calc_area(*data) <= node.extent.area:
                # If max depth is reached, don't split no matter what.
                if node.depth == self.max_depth:
                    pass

                elif node.is_leaf:
                    node.split()
                    node = node.get_relevant_child(data)

                insertion = bisect_left(node.data, data)
                node.data.insert(insertion, data)
                node.indices.insert(insertion, index)

    def index(self, data, index):
        if isinstance(data, Iterable) and isinstance(index, Iterable):
            # TODO add if they are not of the same length, raise exception
            for d, i in zip(data, index):
                self._index_data_point(d, i)

        elif isinstance(data, Iterable) and isinstance(index, int):
            # TODO add if data is not a list of floats or ints, raise exception
            self._index_data_point(data, index)

    def search(self, data):
        if data in self.root.extent:
            node = self.root
            parent = node
            while not node.is_leaf:
                node = node.get_relevant_child(data)
                # If there is no progress in the tree structure, break out of the while loop.
                if node is parent:
                    break
                parent = node

            # If data is inside node.data return the node, otherwise print a message that this data is not in the tree.
            index = bisect_left(node.data, data)
            if index != len(node.data) and node.data[index] == data:
                return node
            else:
                print(f"{data} is not inside this QuadTree")  # TODO maybe raise because it will raise an exception anyway

    def __iter__(self):
        yield from self.root
