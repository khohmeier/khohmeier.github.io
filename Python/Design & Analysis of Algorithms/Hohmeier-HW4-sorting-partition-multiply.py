# Kaitlyn Hohmeier
# Homework 4
# CSC 380
import time
import random
import math


def insertion_sort(a_list):
    """
    Implementation of insertion sort algorithm

    Parameters:
        a_list: a list of n orderable elements

    """
    n = len(a_list)
    count = 0
    for i in range(1, n):
        v = a_list[i]
        j = i - 1
        while j >= 0 and a_list[j] > v:
            count += 1
            a_list[j + 1] = a_list[j]
            j -= 1
        a_list[j + 1] = v
    return count


def peasant(n, m):
    """
    Implementation of the Russian Peasant Multiplication algorithm

    Parameters
        n: a positive integer
        m: a positive integer

    Return:
        A list with the result of the multiplication, the number of multiplications, the number of divisions, and the
        number of additions
    """
    answer = 0
    multi_count = 0
    div_count = 0
    add_count = 0

    while m != 0:
        if m % 2 != 0:
            answer = answer + n
            n = n * 2
            m = m // 2
            add_count += 1
            multi_count += 1
            div_count += 1
        if m % 2 == 0:
            n = n * 2
            m = m // 2
            multi_count += 1
            div_count += 1

    return multi_count + div_count + add_count


def lomuto_partition(arr, low, high):
    """
    Implements the Lomuto partition algorithm using the first position as a pivot

    Parameters:
        arr: a list of orderable elements
        low: the left index
        high: the right index

    Return:
        the new position of the pivot
    """
    # pivot
    pivot = arr[low]
    s = low
    count = 0
    for j in range(low + 1, high + 1):

        # If current element is smaller than or equal to pivot
        count += 1
        if arr[j] < pivot:
            # increment index of smaller element
            s += 1
            arr[s], arr[j] = arr[j], arr[s]
    arr[low], arr[s] = arr[s], arr[low]
    return s, count


def quickselect(a_list, k, low, high):
    """
    Solves the selection problem by recursive partition-based algorithm

    Parameters:
        a_list: a list of orderable elements
        k: an integer

    Return:
        the value of the kth smallest element in a_list
    """
    s, c = lomuto_partition(a_list, low, high)
    if s == k - 1:
        return a_list[s], c
    elif s > k - 1:
        value, c2 = quickselect(a_list, k, low, s-1)
    else:
        value, c2 = quickselect(a_list, k, s + 1, high)

    return a_list[k-1], (c + c2)


def gen_list(size):
    """
    Helper function to create a list of numbers of a specified size.

    Parameters:
        size: the size of the list

    Return:
        a list of randomly generated numbers
    """
    list_rand = []
    for i in range(size + 1):
        list_rand.append(random.randint(-10000, 10000))
    return list_rand


def time_this(function, *args):
    """
    A helper function. time_this measures the elapsed time when a function is executed

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


# Demonstration of insertion sort
a_list = [10, 25, 0, -15, 1405, -1240, 420, 2]
print("List: ", a_list)
print("Number of comparisons: ", insertion_sort(a_list))
print("Sorted list: ", a_list)
print()

# Demonstration of RPM
print("Multiplication using RPM")
print("33 x 33 in RPM performs", peasant(33,33), "number of multiplications, divisions, and additions")
print()

# Demonstration of QuickSelect
a_list = [4, 1, 10, 8, 7, 12, 9, 2, 15]
print("List: ", a_list)
k = math.ceil(len(a_list)/2)
value, count = quickselect(a_list, k, 0, len(a_list) - 1)
print("The kth smallest element in the list, where k = ", str(k), "is ", value, "with ", str(count), "comparisons")
print()

# Timing experiments
# Problem 1
print("Size" + '\t' + '\t' + "Num Comps")
for n in range(100, 3001, 100):
    test_list = gen_list(n)
    comps = insertion_sort(test_list)
    print(str(n) + '\t' + '\t' + str(comps))
print()

# Problem 3
print("n" + '\t' + '\t' + '\t' + "m" '\t' + '\t' + '\t' + "Multis" + '\t' + '\t' + "Divs" + '\t' + '\t' + "Adds")
for num in range(100000, 100100001, 1000000):
    num_exp = 10
    rpm = 0
    for i in range(num_exp):
        n = random.randint(num, num + random.randint(500, 10000))
        m = random.randint(num, num + random.randint(500, 10000))
        rpm += peasant(n, m)
    print(str(n) + '\t' + '\t' + str(m) + '\t' + '\t' + str(rpm//10))
print()

# Problem 4
print("List Size", '\t', '\t', "Num Comps")
for num in range(10, 10000, 250):
    num_exp = 10
    total = 0
    for _ in range(num_exp):
        test_list = gen_list(num)
        value, count = quickselect(test_list, len(test_list)//2, 0, len(test_list) - 1)
        total += count
    print(num, '\t', '\t', total//num_exp)
