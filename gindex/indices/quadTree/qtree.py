from collections import deque
from collections.abc import Iterable
from .node import Node
from .utils import calc_area


class QuadTree:

    def __init__(self, data=[], indices=[], tree_extent=None, max_depth=8, copy_data=True, verify_inputs=True, ndims=2):
        """QuadTree initializer.
            The format for 1D data: (x,y), 2D data: (minx,miny,maxx,maxy), 3D data: (minx,miny,maxx,maxy,minz,maxz)

        ..Note: If verify_inputs is True and the data you input into the tree is not in the correct format, it will be forced into the format and therfore might be errornous.
        Args:
            data (list, optional): A list of all the data points in the tree.
            indices (list, optional): A list of all the data points indices in the tree.
            tree_extent (list or tuple, optional): A 4 element list or tuple that contains the extent of the tree in the format of minx,miny,maxx,maxy.
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
                tree_extent = [bottom_x, top_x, bottom_y, top_y]
            else:
                raise ValueError(f"Your input did not include an extent for the tree, and it was not possible to get an extent from your input of type {type(data)}")

        if copy_data:
            data = data.copy()

        self.root = Node(*tree_extent, verify_inputs=verify_inputs, depth=0)
        self.max_depth = max_depth
        self.indexed_points = []  # TODO this is shit needs to be deleted

        if isinstance(data, Iterable):
            self.index_list(data, indices)

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
            prev_node = node
            while not node.isleaf:
                node = node.get_relevant_child(data)  # TODO might cause an exception and to fix, i need to check that children returned in Node
                if prev_node is node:
                    break
                prev_node = node
            return node
        raise RuntimeError("Data extent {data} not in this tree's extent: {self.root.extent}")

    def index_list(self, data_list, indices_list):
        for data, index in zip(data_list, indices_list):
            # Find the deepest node that this data point might be in.
            node = self._find_deepest_node(data)

            # If the data and indices list in this node are empty, append the data and index to them.
            if not node.data:
                node.data.append(data)
                node.indices.append(index)

            elif data not in node:
                # Only try to split the node if the area of data is smaller than the area of node.
                if calc_area(*data) <= node.extent.area:
                    if node.depth == self.max_depth:
                        pass
                    elif node.isleaf:
                        node.split()
                        node = node.get_relevant_child(data)
                    node.data.append(data)
                    node.indices.append(index)
            # TODO clear all unnecessary children      

    def index(self, root):
        node_list = deque([root])
        while node_list:
            node = node_list.popleft()
            if node.depth == self.max_depth:
                # self.indexed_points.extend(node.data)
                continue
            if len(node.data) <= 1:
                continue
            if node.isleaf:
                node.split()
            for i, value in enumerate(node.data):
                # TODO make formula to find which quad a point is in a node
                for child in node.children:
                    if child.data:
                        if value in child:
                            continue
                    if value in child.extent:
                        child.data.append(value)
                        child.indices.append(node.indices[i])
                        break

            node.data.clear()
            node.indices.clear()

            node_list.extend(node.children)

    def index_data(self, val, index):
        # Checking index correctness is responsibility of index correctness
        node = self.search(val)

        if node is None:
            raise ValueError(f"{val} not in this QuadTree extent: {self.extent}")

        if node.data:
            if val in node:
                return

        node.data.append(val)
        node.indices.append(index)

        self.index(node)
        self.indexed_points.append(val)
    
    def search(self, data):
        if data in self.root.extent:
            node = self.root
            parent = node
            while not node.isleaf:
                node = node.get_relevant_child(data)
                # If there is no progress in the tree structure, break out of the while loop.
                if node is parent:
                    break
                parent = node

            # If data is inside node.data return the node, otherwise print a message that this data is not in the tree.
            if data in node:
                return node
            else:
                print(f"{data} is not inside this QuadTree")

    def __iter__(self):
        yield from self.root
