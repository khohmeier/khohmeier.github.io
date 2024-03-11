import random


def random_list(size, low, high):
    # return a list of length size filled with random ints in the range low-->high, both inclusive
    random.seed()
    a = [random.randint(low, high) for r in range(size)]
    return a
