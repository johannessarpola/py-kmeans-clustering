from collections import defaultdict
import multiprocessing as mp

def join_all(processes):
    for p in processes:
        p.join()


def gather_to_list(queue, processes):
    l = []
    for _ in processes:
        process_result = queue.get()
        l.append(process_result)
    return l

def gather_to_list_and_join(queue, processes):
    l = []
    for _ in processes:
        process_result = queue.get()
        l.append(process_result)
    join_all(processes)
    return l


def gather_to_dict_from_tuples(queue, processes):
    d = defaultdict(dict)
    for _ in processes:
        process_result = queue.get()
        d[process_result[0]] = process_result[1]
    return d

def gather_to_dict_from_tuples_and_join(queue, processes):
    d = defaultdict(dict)
    for _ in processes:
        process_result = queue.get()
        d[process_result[0]] = process_result[1]
    join_all(processes)
    return d


def create_process_and_start(target, args=(), msg=None):
    if msg is not None:
        print(msg)
    p = mp.Process(target=target, args=args)
    p.start()
    return p