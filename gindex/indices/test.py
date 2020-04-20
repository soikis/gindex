from quadTree.qtree import QuadTree
from quadTree.utils import calc_area
from timeit import default_timer
from random import randint, seed
import numpy as np
import cProfile
import json


def main(data=None, extent=None):
    iters = 1
    sample_size = 500
    seed(a=10)
    data = [(randint(0, 128), randint(0, 128)) for _ in range(sample_size)]
    data = [(d[0], d[1], d[0] + randint(0, 128 - d[0]), d[1] + randint(0, 128 - d[1])) for d in data]
    indices = list(range(sample_size))
    extent = (0, 0, 128, 128)

    avg_bulk_index = []

    for i in range(iters):
        sp = default_timer()
        qt = QuadTree(extent, max_depth=4)
        qt.index(data, indices)
        ep = default_timer()
        avg_bulk_index.append(ep - sp)

    # avg_single_index = []

    # for i in range(iters):
    #     sp = default_timer()
    #     qt = QuadTree(extent, max_depth=8)
    #     for d, i in zip(data, indices):
    #         qt.index(d, i)
    #     ep = default_timer()
    #     avg_single_index.append(ep - sp)

    avg_search = []

    for i in range(iters):
        sp = default_timer()
        for point in data:
            qt.search(point)
        ep = default_timer()
        avg_search.append(ep - sp)

    avg_bulk_index = np.array(avg_bulk_index)
    # avg_single_index = np.array(avg_single_index)
    avg_search = np.array(avg_search)

    print(np.std(avg_bulk_index), avg_bulk_index.mean())
    # print(np.std(avg_single_index), avg_single_index.mean())
    print(np.std(avg_search), avg_search.mean())

    # print(qt.root.extent.area)
    # print(qt.root.children[0].extent.area)
    # print([node.depth for node in qt])

    # sp = default_timer()
    # qt.to_file(r"C:\Users\Tal\Downloads", compress=False)
    # ep = default_timer()
    # print(f"\nwrite uncompressed time {ep-sp}")

    # sp = default_timer()
    # test = QuadTree.from_file(r"C:\Users\Tal\Downloads\qtree.json")
    # ep = default_timer()
    # print(f"read uncompressed time {ep-sp}")

    # sp = default_timer()
    # qt.to_file(r"C:\Users\Tal\Downloads", compress=True)
    # ep = default_timer()
    # print(f"\nwrite compressed time {ep-sp}")
    
    # sp = default_timer()
    # test = QuadTree.from_file(r"C:\Users\Tal\Downloads\qtree.gz")
    # ep = default_timer()
    # print(f"read compressed time {ep-sp}")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    # qt.to_file(r"C:\Users\Tal\Downloads", compress=False)
    # test = QuadTree.from_json(r"C:\Users\Tal\Downloads\qtree.json")
    # test
    # for d in data:
    #     node = qt.search(d)
    #     print(node.extent, "-----", d, node.extent.area, " > ", calc_area(*d), node.extent.area > calc_area(*d))
    # print(f'search time: {np-sp} seconds')
    # print(f'index time: {ep-sp} seconds')


if __name__ == "__main__":
    with open(r"C:\Users\Tal\Documents\python_scripts\gindex\testing_for_gindex.geojson") as la:
        layer = json.load(la)
        data = [list(map(tuple, d["geometry"]["coordinates"])) for d in layer["features"]]
        indices = list([i["properties"]["fid"] for i in layer["features"]])

    formated_data = []
    for d in data:
        x = [xy[0] for point in d for xy in point[:-1]]
        y = [xy[1] for point in d for xy in point[:-1]]
        minx = min(x)
        miny = min(y)
        maxx = max(x)
        maxy = max(y)
        formated_data.append((minx, miny, maxx, maxy))

    minx = min([p[0] for p in formated_data])
    maxx = max([p[2] for p in formated_data])
    miny = min([p[1] for p in formated_data])
    maxy = max([p[3] for p in formated_data])
    extent = (minx, miny, maxx, maxy)

    import tracemalloc
    tracemalloc.start()
    main(formated_data, extent)
    # cProfile.run("main(formated_data, extent)", sort='cumtime')
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    tracemalloc.stop()
    # main(formated_data, extent)
