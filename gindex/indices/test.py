from quadTree.qtree import QuadTree
from quadTree.utils import calc_area
from timeit import default_timer
from random import randint, seed
import numpy as np


def main():
    iters = 1
    sample_size = 500
    seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(sample_size)]
    data = [(d[0], d[1], d[0] + randint(0, 128 - d[0]), d[1] + randint(0, 128 - d[1])) for d in data]
    indices = range(sample_size)

    avg_bulk_index = []

    for i in range(iters):
        sp = default_timer()
        qt = QuadTree(data, list(indices), (0, 0, 128, 128), 4)
        ep = default_timer()
        avg_bulk_index.append(ep - sp)

    # avg_single_index = []

    # for i in range(iters):
    #     sp = default_timer()
    #     qt = QuadTree([], [], (0, 0, 128, 128), 4)
    #     for d, i in zip(data, indices):
    #         qt.index(d, i)
    #     ep = default_timer()
    #     avg_single_index.append(ep - sp)

    # avg_search = []

    # for i in range(iters):
    #     sp = default_timer()
    #     for point in data:
    #         qt.search(point)
    #     ep = default_timer()
    #     avg_search.append(ep - sp)

    avg_bulk_index = np.array(avg_bulk_index)
    # avg_single_index = np.array(avg_single_index)
    # avg_search = np.array(avg_search)

    print(np.std(avg_bulk_index), avg_bulk_index.mean())
    # print(np.std(avg_single_index), avg_single_index.mean())
    # print(np.std(avg_search), avg_search.mean())

    """ for d in data:
            node = qt.search(point)
            print(node.extent, "-----", point, node.extent.area, " > ", calc_area(*point), node.extent.area > calc_area(*point))
        print(f'search time: {np-sp} seconds')"""
    # print(f'index time: {ep-sp} seconds')


if __name__ == "__main__":
    main()
