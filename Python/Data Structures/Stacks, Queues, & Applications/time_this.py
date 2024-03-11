import time


def time_this(function, *args):
    """time_this measures the elapsed time when a function is executed

        Parameters:
            function: Reference to function whose execution time is being measured
            *args: comma-separated list of arguments to function

        Returns:
            a tuple representing the elapsed time and the result returned by the function

    """

    start = time.perf_counter()  # record initial time
    result = function(*args)  # call the specified function, passing it the specified parameters
    end = time.perf_counter()  # record final time
    return float("%.20f" % (end - start)), result  # return elapsed time and value returned by function
