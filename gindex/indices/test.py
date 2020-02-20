from quadTree.qtree import QuadTree
from timeit import default_timer
from random import randint, seed


def main():
    sample_size = 500
    seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(sample_size)]
    # data = [[(x, y, x + randint(0, 128 - x), y + randint(0, 128 - y)) for x, y in zip([randint(0, 128)], [randint(0, 128)])] for _ in range(sample_size)]
    indices = range(sample_size)

    sp = default_timer()
    # qt = QuadTree([], [], (0, 0, 128, 128), 4)
    qt = QuadTree(data, list(indices), (0, 0, 128, 128), 4)

    # for i, d in enumerate(data):
    #     # print(i, d)
    #     # print(d in qt.indexed_points)
    #     qt.index_data(d, indices[i])
    #     if i == len(data)-1:
    #         print(len(qt.indexed_points), len(set(data)))
    #         assert len(set(data)) == len(qt.indexed_points)

    np = default_timer()
    print(f'index time: {np-sp} seconds')

    sp = default_timer()

    for point in data:
        # qt.search(point)
        node = qt.search(point)
        # print(node.extent, node.data, node.indices, point in node.data, point, node.depth)
        # print(node)

    np = default_timer()
    print(f'search time: {np-sp} seconds')


if __name__ == "__main__":
    main()
