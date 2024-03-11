# K. Hohmeier
# Homework 5
# CSC 380
import time
import random
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


def mergesort(a_list):
    """
    Implementation of the mergesort sorting algorithm. Outputs a list sorted in non-decreasing order

    Parameter:
        a_list: a list of orderable elements of length n
    """
    n = len(a_list)
    if n > 1:
        # Create a midpoint in a_list
        midpoint = n//2
        # Dividing list into two halves
        b_list = a_list[:midpoint]
        c_list = a_list[midpoint:]
        # Sorting each half of the list
        mergesort(b_list)
        mergesort(c_list)
        # merge all pieces of the list
        merge(b_list, c_list, a_list)


def merge(b_list, c_list, a_list):
    """
    Merges two sorted arrays into one sorted array. Outputs a sorted array of the elements of B and C

    Parameters:
        b_list: a sorted array
        c_list: a sorted array
        a_list: sorted array of the elements of b_list and c_list
    """
    i = 0
    j = 0
    k = 0
    p = len(b_list)
    q = len(c_list)
    while i < p and j < q:
        if b_list[i] <= c_list[j]:
            a_list[k] = b_list[i]
            i += 1
        else:
            a_list[k] = c_list[j]
            j += 1
        k += 1
    if i == p:
        a_list[k:p+q] = c_list[j:q]
    else:
        a_list[k:p+q] = b_list[i:p]


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


def hoare_partition(array, low, high):
    """
    Implementation of Hoare's partitioning algorithm.

    Parameters:
        array: a list of orderable elements
        low: the left mark
        high: the right mark

    Return:
        the new right mark
    """
    p = array[low]
    left = low + 1
    right = high

    done = False

    while not done:
        while left <= right and array[left] <= p:
            left += 1
        while array[right] >= p and right >= left:
            right -= 1
        if right < left:
            done = True
        else:
            array[left], array[right] = array[right], array[left]
    array[low], array[right] = array[right], array[low]
    return right


def quicksort(a_list, first, last):
    """
    Implementation of quicksort recursive sorting algorithm. Uses Hoare's partition algorithm to find pivot. Outputs a
    sorted list

    Parameters:
        a_list: a list of orderable elements
        first: the leftmost end point
        last: the rightmost end point
    """
    if first < last:
        splitpoint = hoare_partition(a_list, first, last)

        quicksort(a_list, first, splitpoint - 1)
        quicksort(a_list, splitpoint + 1, last)


def median_of_three(one, two, three):
    """
    Implements a pivot selection method by choosing the median of three elements

    Parameters
        one: the first number (the first element in a list)
        two: the second number (the element at the middle of a list)
        three: the third number (the last element in a list)
    Return:
        the median of the three given numbers
    """
    if one > two:
        if one < three:
            median = one
        elif two > three:
            median = two
        else:
            median = three
    else:
        if one > three:
            median = one
        elif two < three:
            median = two
        else:
            median = three
    return median


def hoare_with_med_of_three(array, low, high):
    """
    Hoare's partitioning algorithm with median of three as pivot selection method

    Parameters:
        array: a list of orderable elements
        low: the left mark
        high: the right mark

    Return:
        the new right mark
    """
    p = median_of_three(array[low], array[len(array)//2], array[high])
    index = array.index(p)
    array[index], array[low] = array[low], array[index]
    left = low + 1
    right = high

    done = False

    while not done:
        while left <= right and array[left] <= p:
            left += 1
        while array[right] >= p and right >= left:
            right -= 1
        if right < left:
            done = True
        else:
            array[left], array[right] = array[right], array[left]
    array[low], array[right] = array[right], array[low]
    return right


def other_quicksort(a_list, first, last):
    """
    Alternate implementation of quicksort using median-of-three method of choosing pivot. Outputs a
    sorted list

    Parameters:
        a_list: a list of orderable elements
        first: the leftmost end point
        last: the rightmost end point
    """
    if first < last:
        splitpoint = hoare_with_med_of_three(a_list, first, last)

        other_quicksort(a_list, first, splitpoint - 1)
        other_quicksort(a_list, splitpoint + 1, last)


def distance_right(p1, p2):
    """
    Helper function for the Brute Force Closest Pair Algorithm for calculating the distance between two points

    Parameters:
        p1: the first point (created from the Point class)
        p2: the second point (created from the Point class)

    Return:
        the distance between p1 and p2
    """
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def BruteForceClosestPair(P):
    """
    Finds distance between two closest points in the plane by brute force

    Parameters:
        P: A list of n(n≥2) points p1(x1,y1),...,pn(xn,yn)

    Return:
        The distance between the closest pair of points
    """
    n = len(P)
    dmin = float('inf')

    for i in range(0, n):
        for j in range(i+1, n):
            d = distance_right(P[i], P[j])
            if d < dmin:
                dmin = d

    return dmin


def sorting_points(points):
    """
    Takes a list of points and sorts two copies of the list, one sorted by x coordinates and one sorted by y
    coordinates

    Parameters:
        points: a random list of points

    Return:
        A call to the Efficient Closest Pair algorithm. It passes the two sorted lists, P and Q, as arguments.
    """
    P = points.copy()
    Q = points.copy()
    P.sort(key=lambda p: p.x)
    Q.sort(key=lambda p: p.y)
    return efficient_closest_pair(P, Q)


def efficient_closest_pair(P, Q):
    """
    Implementation of an efficient algorithm for finding the closest pair in a list of points. Utilizes a divide and
    conquer approach.

    Parameters:
        P: a list of >= 2 points sorted in nondecreasing order of their x coordinates
        Q: the same list of points p, but sorted by y coordinates

    Return:
        the Eucliean distance between the closest pair of points
    """
    n = len(P)
    if n <= 1:
        return math.inf
    if n <= 3:
        return BruteForceClosestPair(P)
    else:
        # Create sublists
        PL = P[:n//2]
        QL = [p for p in Q if p in PL]
        PR = P[n//2:]
        QR = [p for p in Q if p in PR]

        # Run algorithm on sublists of points
        dL = efficient_closest_pair(PL, QL)
        dR = efficient_closest_pair(PR, QR)

        d = min(dL, dR)
        m = P[int(math.ceil(n/2.0)) - 1].x
        S = []
        # print(d)
        for p in Q:
            if math.fabs(p.x - m) < d:
                S.append(p)
        dminsq = d*d
        num = len(S)
        for i in range(0, num):
            k = i + 1
            while k <= num - 1 and (S[k].y - S[i].y)**2 < dminsq:
                diffX = S[k].x - S[i].x
                diffXsq = diffX * diffX
                diffY = S[k].y - S[i].y
                diffYsq = diffY * diffY
                dminsq = min(diffXsq + diffYsq, dminsq)
                k += 1
        return math.sqrt(dminsq)


def point_list_gen(size):
    """
    Helper function to generate a list of points (create via the Point class) of the specified size

    Parameters:
        size: size of the list to be created

    Return:
        the list of points
    """
    point_list = []
    for n in range(size):
        point_list.append(Point(random.randint(-100, 100000),
                                random.randint(-100, 100000)))

    return point_list


def sorted_list_gen(size):
    """
    Helper function to generate a sorted list of a given size

    Parameter:
        size: size of the sorted list to be generated

    Return:
        the sorted list
    """
    a_list = []
    for i in range(0, size):
        a_list.append(i)
    return a_list

# Demonstration of merge sort
print("Demonstration of mergesort")
test_list = [8, 3, 2, 9, 7, 1, 5, 4]
print("List before sorting: ", test_list)
mergesort(test_list)
print("List after sorting: ", test_list)
print()

# Demonstration of quicksort
print("Demonstration of quicksort")
test_list = [8, 3, 2, 9, 7, 1, 5, 4]
print("List before sorting: ", test_list)
quicksort(test_list, 0, len(test_list) - 1)
print("List after sorting: ", test_list)
print()

# Demonstration of other_quicksort
print("Demonstration of quicksort using median-of-three")
test_list = [8, 3, 2, 9, 7, 1, 5, 4]
print("List before sorting: ", test_list)
other_quicksort(test_list, 0, len(test_list) - 1)
print("List after sorting: ", test_list)
print()

# Demonstration of other quicksort on a concatenated list
print("Demonstration of quicksort using median-of-three on a concatenated list")
test1 = sorted_list_gen(5)
print(test1)
test2 = sorted_list_gen(10)
print(test2)
test3 = test1 + test2
print(test3)
other_quicksort(test3, 0, len(test3) - 1)
print("The sorted list is", test3)
print()

# Can't run quicksort on this list!
l = []
for n in range(1000, 0, -1):
    l.append(n)
print("Can't run quicksort on a list sorted in descending order!")
print("Length of list: ", str(len(l)))
print("Quick sort throws an error if it tries to sort this list.")
# quicksort(l, 0, len(l) - 1)
print()

# Demonstration of efficient closest pairs
demo1 = [Point(-1, 10), Point(4, 2), Point(-9, 0), Point(1, 2)]
demo2 = point_list_gen(10)
print("First list of points: ", demo1)
print("Efficient CP: ", sorting_points(demo1))
print("Brute force: ", BruteForceClosestPair(demo1))
print()
print("Second List of points: ", demo2)
print("Efficient CP: ", sorting_points(demo2))
print("Brute force: ", BruteForceClosestPair(demo2))
print()

# Experiments with mergesort and quicksort
print("Size" + '\t' + '\t' + "Mergesort" + '\t' + '\t' + "Quicksort")
for size in range(10000, 1060001, 50000):
    # num_exp = 10
    sum1 = 0
    sum2 = 0
    # num_exp = 3
    # for num in range(num_exp):
    test_list_a = gen_list(size)
    test_list_b = test_list_a.copy()
    sum1 += round(time_this(mergesort, test_list_a)[0], 15)
    sum2 += round(time_this(quicksort, test_list_b, 0, len(test_list_b) - 1)[0], 15)
    print(str(size) + '\t' + '\t' + str(sum1) + '\t' + '\t' + str(sum2))
print()

print("Size" + '\t' + '\t' + "Mergesort" + '\t' + '\t' + "Med of 3 Quicksort")
for size in range(10, 1001, 10):
    # num_exp = 10
    sum1 = 0
    sum2 = 0
    # num_exp = 3
    # for num in range(num_exp):
    temp = random.randint(395, 405)
    L1 = sorted_list_gen(temp)
    L2 = sorted_list_gen(size)
    test_list_a = L1 + L2
    test_list_b = test_list_a.copy()
    sum1 += round(time_this(mergesort, test_list_a)[0], 15)
    sum2 += round(time_this(other_quicksort, test_list_b, 0, len(test_list_b) - 1)[0], 15)
    print(str(size + temp) + '\t' + '\t' + str(sum1) + '\t' + '\t' + str(sum2))
print()

# Experiments with Efficient Closest Pair and Brute Force Closest Pair
print("Size" + '\t' + '\t' + "Brute Force" + '\t' + '\t' + "Efficient CP")
for n in range(100, 3001, 100):
    point_list = point_list_gen(n)
    sum1 = 0
    sum2 = 0
    num_exp = 5
    for i in range(num_exp):
        sum1 += time_this(BruteForceClosestPair, point_list)[0]
        sum2 += time_this(sorting_points, point_list)[0]
    print(str(n) + '\t' + '\t' + str(round(sum1 / num_exp, 15)) + '\t' + '\t' + str(round(sum2 / num_exp, 15)))
