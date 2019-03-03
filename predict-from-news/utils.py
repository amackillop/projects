import itertools as it
import pickle
import math
import multiprocessing as mp


def spagettify(iterable, strands):
    return [it.islice(iterable, i, None, strands) for i in range(strands)]


def pickle_data(data, fname):
    with open(fname, 'wb') as pfile:
        pickle.dump(data, pfile, protocol=pickle.HIGHEST_PROTOCOL)


def unpickle_data(fname):
    with open(fname, 'rb') as pfile:
        data = pickle.load(pfile)
    return data


def take(n, iterable):
    """Return first n items of the iterable as a list"""
    return list(it.islice(iterable, n))


def chunker(iterable, chunksize, fillvalue=None):
    """Yield `chunk_size` tuples of values from any iterable."""
    args = [iter(iterable)] * chunksize
    return it.zip_longest(*args, fillvalue=fillvalue)


def parallelize(func, args_list, n_processes=None):
    """Parallelize a function call across multiple processes.

    This function will create equal length batches of the provided `args_list`
    and kick off a process for each batch. If they cannot be split evenly
    across the n processes then the last batch will be shorter. If they can be
    split evenly across a lesser number of batches, then this will do that for
    you.

    For example, processing 6 files across 4 processes will just kick off 3
    processes that do 2 files each as this is more efficient.

    If you have to pass multiple arguments to your function, make sure that the
    `args_list` is a list of tuples wth the arguments in the correct order.

    One last note, the passed function must accept a multiprocessing.Queue()
    object as the last argument and instead of returning, use
    queue.put(<return value>) instead. This is how the function will determine
    when all processes are complete and be able to return all of the results to
    the parent process.

    Args
    ----
    func : <function>
        What function to call.
    args_list : list
        The list of arguments to batch and call in parallel.
    n_processes : int
        Number of processes to use. Defaults to system cpu count.

    """
    if n_processes is None:
        n_processes = mp.cpu_count()
    result_queue = mp.Queue()
    batch_size = int(math.ceil(len(list(args_list)) / n_processes))
    batched_args = chunker(args_list, batch_size)
    processes = []
    for batch in batched_args:
        # Gets rid of Nones if this is the short batch
        func_args = [arg for arg in batch if arg]
        p = mp.Process(target=func, args=tuple([*func_args, result_queue]))
        p.start()
        processes.append(p)

    result = [result_queue.get() for p in processes]

    for i, p in enumerate(processes):
        p.join()

    return result
