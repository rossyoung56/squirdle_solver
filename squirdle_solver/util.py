import time


def function_time(f):
    def wrapper(*args, **kwargs):
        start = time.perf_counter_ns()
        return_val = f(*args, **kwargs)
        end = time.perf_counter_ns()
        print('{0}: {1}ms'.format(f.__name__, (end - start) / 1000000.0))
        return return_val

    return wrapper
