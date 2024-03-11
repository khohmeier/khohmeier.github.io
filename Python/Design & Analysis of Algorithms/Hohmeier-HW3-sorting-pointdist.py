# K. Hohmeier
# CSC 380
# Homework 3

import time
import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


def SelectionSort(A):
    """
    Implementation of the selection sort algorithm

    Parameters:
        A: a list with orderable elements
    """
    n = len(A)
    for i in range(0, n-1):
        min = i
        for j in range(i+1,n):
            if A[j] < A[min]:
                min = j

        A[i], A[min] = A[min], A[i]


def BubbleSort(A):
    """
    Implementation of the bubble sort algorithm

    Parameters:
        A a list of orderable elements
    """
    n = len(A)
    for i in range(0, n-1):
        for j in range(0,n-1-i):
            if A[j+1] < A[j]:
                A[j], A[j+1] = A[j+1], A[j]


def gen_list(num):
    """
    Helper function to create a list of numbers of a specified size. The numbers are arranged in decreasing order so as
    to ensure worst case performance during the timing experiments for selection sort and bubble sort.

    Parameters:
        num: the size of the list

    Return:
        a list of randomly generated numbers
    """
    list_asc = []
    for i in range(num,0,-1):
        list_asc.append(i)
    return list_asc


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


def BruteForceStringMatch(T, P):
    """
    Implements brute force string matching

    Pparameters:
        T: an array of n characters representing a text
        P: an array of m characters representing a pattern

    Return:
        a tuple containing the index of the first character in the text that starts a matching substring or -1 if the
        search is unsuccessful and the number of comparisons made
    """
    n = len(T)
    m = len(P)
    comps = 0
    for i in range(0, n - m + 1):
        j = 0
        while j < m and P[j] == T[i+j]:
            j += 1
            comps += 1
        comps += 1
        if j == m:
            return i, comps
    return -1, comps


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


def distance_wrong(p1, p2):
    """
    Helper function for the improved Brute Force Closest Pair Algorithm. It finds difference between the x and y
    coordinates of two points and then squares these values, but skips the square root in the distance formula.

    Parameters:
        p1: the first point (created from the Point class)
        p2: the second point (created from the Point class)

    Return:
        the squares of the difference between the x and y coordinates of p1 and p2
    """
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2


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
    index_one = float('inf')
    index_two = float('inf')
    points = []
    for i in range(1, n):
        for j in range(i+1, n):
            d = distance_right(P[i], P[j])
            if d < dmin:
                dmin = d
                index_one = i
                index_two = j

    points.append(P[index_one])
    points.append(P[index_two])
    return dmin, points


def other_closest_pair(P):
    """
    Alternate implementation of the brute force closest pair algorithm

    Parameters:
        P: A list of n(n≥2) points p1(x1,y1),...,pn(xn,yn)

    Return:
        the squares of the differences between the x and y coordinates of the two closest points
    """
    n = len(P)
    dmin = float('inf')
    index_one = float('inf')
    index_two = float('inf')
    points = []
    for i in range(1, n):
        for j in range(i + 1, n):
            d = distance_wrong(P[i], P[j])
            if d < dmin:
                dmin = d
                index_one = i
                index_two = j

    points.append(P[index_one])
    points.append(P[index_two])
    return dmin, points


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
        point_list.append(Point(random.randint(1000000000000000, 10000000000000000000000),
                                random.randint(1000000000000000, 10000000000000000000000)))

    return point_list


# Demonstration of Selection Sort
alist1 = [54,26,93,17,77,31,44,55,20]
SelectionSort(alist1)
print("Result of Selection Sort: ", alist1)

# Demonstration of Bubble Sort
alist2 = [54,26,93,17,77,31,44,55,20]
BubbleSort(alist2)
print("Result of Bubble Sort: ", alist2)

# Demonstration of brute force string matching
text = '000000000000001'
pat1 = '1000'
pat2 = '001'
print("Results of test on pattern ", pat1, " in text ", text, "(index, num. comparisons): ", BruteForceStringMatch(text,pat1))
print("Results of test on pattern ", pat2, " in text ", text, "(index, num. comparisons): ", BruteForceStringMatch(text,pat2))

# Demonstration of brute force closest pair
P = [Point(5, 2), Point(1, 30),
     Point(4, 5), Point(10, 5),
     Point(12, 10), Point(7, 4)]

print("Point list: ", P)
print("Closest pair in point list and the distance: ", BruteForceClosestPair(P))
print("Closest pair in point list is and its approx. distance without the square root: ", other_closest_pair(P))
print()

# Problem 1 Timing Experiment
print("Problem 1 Timing Experiments")
print()
print("Size" + '\t' + '\t' + "Selection Sort" + '\t' + '\t' + "Bubble Sort")
for size in range(100,3001,100):
    test_list1 = gen_list(size)
    test_list2 = test_list1.copy()
    sum_method1 = 0
    sum_method2 = 0
    num_exp = 30
    for i in range(num_exp):
        sum_method1 += round((time_this(SelectionSort, test_list1)[0]), 15)
        sum_method2 += round((time_this(BubbleSort, test_list2)[0]), 15)
    print(str(size) + '\t' + '\t' + str(round(sum_method1 / num_exp, 15)) + '\t' + '\t' + str(round(sum_method2 / num_exp, 15)))
print()

# Problem 2 comparison counting experiment
text = ''
for i in range(1000):
    text += '0'

t1 = '00001'
t2 = '10000'
t3 = '01010'

print(BruteForceStringMatch(text, t1))
print(BruteForceStringMatch(text, t2))
print(BruteForceStringMatch(text, t3))
print()

# Problem 3 Timing Experiments
print("Problem 3 Timing Experiments")
print()
print("Size" + '\t' + '\t' + "With Square Root" + '\t' + '\t' + 'Without Square Root')
for n in range(100, 3001, 100):
    point_list = point_list_gen(n)
    sum1 = 0
    sum2 = 0
    num_exp = 5
    for i in range(num_exp):
        sum1 += round(time_this(BruteForceClosestPair, point_list)[0], 15)
        sum2 += time_this(other_closest_pair, point_list)[0]
    print(str(n) + '\t' + '\t' + str(round(sum1 / num_exp, 15)) + '\t' + '\t' + str(round(sum2 / num_exp, 15)))
