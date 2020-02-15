from quadTree.qtree import QTree


def main():
    from timeit import default_timer
    from random import randint, seed
    seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(500)]
    sp = default_timer()
    qt = QTree(data, (0, 0, 128, 128), 4)
    # for i, d in enumerate(data, start=1):
    #     # print(i,d)
    #     # print(d in qt.indexed_points)
    #     qt.add_data(d)
    #     if i == len(data):
    #         print(len(qt.indexed_points),len(set(data)))
    #         assert len(set(data)) == len(qt.indexed_points)
    np = default_timer()
    print(f'index time: {np-sp} seconds')
    sp = default_timer()
    for point in data:
        # node = qt.search(point)
        qt.search(point)
        # print(node)
        # print(node.extent,node.data)
    np = default_timer()
    print(f'search time: {np-sp} seconds')


if __name__ == "__main__":
    main()
