import multiprocessing
from typing import Callable


def func_wrapper(args):
    (f, offset, *args) = args
    items = f(*args)
    return list(
        (i + offset, item)
        for i, item in enumerate(items)
    )


def get_items(
    func: Callable,
    *args,
    parse: Callable = lambda _: _,
    chunk_size: int = 100,
    processes: int = 5,
):
    """
    This function performs pagination on a function that supports
    `limit`/`offset` parameters and it runs API requests in parallel to speed
    things up.
    """
    items = []
    offsets = [-chunk_size]
    remaining = chunk_size * processes

    with multiprocessing.Pool(processes=processes) as pool:
        while remaining == chunk_size * processes:
            offsets = [
                offsets[-1] + chunk_size * (i + 1)
                for i in range(processes)
            ]

            pool_results = pool.map(
                func_wrapper,
                [
                    (
                        func,
                        offset,
                        *args,
                        chunk_size,   # limit
                        offset,       # offset
                    )
                    for offset in offsets
                ]
            )

            new_items = []
            for results in pool_results:
                new_items.extend(results)

            remaining = len(new_items)
            items.extend(new_items)

    items = [_ for _ in items if _]
    sorted_items = list(map(
        lambda item: item[1],
        sorted(items, key=lambda item: item[0])
    ))

    return list(map(parse, sorted_items))