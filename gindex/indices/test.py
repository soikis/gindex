from quadTree.qtree import QuadTree
from quadTree.utils import calc_area
from timeit import default_timer
from random import randint, seed


def main():
    sample_size = 500
    seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(sample_size)]
    data = [(d[0], d[1], d[0] + randint(0, 128 - d[0]), d[1] + randint(0, 128 - d[1])) for d in data]
    indices = range(sample_size)

    # data = [(0, 0, 20, 20), (10, 0, 20, 20), (15, 10, 20, 20)]
    # indices = range(3)
    sp = default_timer()
    # qt = QuadTree([], [], (0, 0, 128, 128), 4)
    qt = QuadTree(data, list(indices), (0, 0, 128, 128), 4)

    # for i, d in enumerate(data):
    #     # print(i, d)
    #     # print(d in qt.indexed_points)
    #     qt.index_data(d, indices[i])
    #     if i == len(data):
    #         print(len(qt.indexed_points), len(set(data)))
    #         assert len(set(data)) == len(qt.indexed_points)

    np = default_timer()
    print(f'index time: {np-sp} seconds')

    sp = default_timer()

    # print(data)
    for point in data:
        # qt.search(point)
        node = qt.search(point)
        # print('found', node)
        # node.extent
        # if not isinstance(node, None):
        print(node.extent, "-----", point, node.extent.area, " > ", calc_area(*point))
        # print(node)

    np = default_timer()
    print(f'search time: {np-sp} seconds')


if __name__ == "__main__":
    main()
