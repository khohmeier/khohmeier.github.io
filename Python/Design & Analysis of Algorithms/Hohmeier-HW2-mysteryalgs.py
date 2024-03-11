# K. Hohmeier
# CSC 380
# Homework 2

import time
import random


def mystery(n):
    """
    This algorithm calculates the sum of the squares of the first n natural numbers

    Parameters:
        n: a positive integer

    Return:
        the sum of the squares of the first n natural numbers
    """
    s = 0

    for i in range(1, n+1):
        s = s + i*i
    return s


def enigma(A):
    """
    Determines whether a matrix is symmetric

    Parameters
        A: A square n x n matrix of real numbers

    Return:
        a Boolean value of False (if the matrix isn't symmetric) or True (if the given matrix is symmetric)
    """
    for i in range(0, len(A) - 1):
        print("i is ", i)
        for j in range(i+1, len(A)):
            print("j is ",j)
            if A[i][j] != A[j][i]:
                return False
    return True


def q(n):
    """
    Computes the square of a given integer n

    Parameters:
        n: a positive integer

    Return:
        a recursive call to the function that will eventually return the square of the given integer n
    """
    if n == 1:
        return 1
    else:
        return q(n-1) + 2*n - 1


def Riddle(A):
    """
    Finds the smallest element in a list

    Parameter:
        A: a list

    Return:
        a recursive call to the function, which ultimately returns the smallest element in the list A
    """
    n = len(A)
    if n == 1:
        return A[0]
    else:
        temp = Riddle(A[0:n-1])
        if temp <= A[n-1]:
            return temp
        else:
            return A[n-1]


def gen_list(num):
    """
    Helper function to create a list of random numbers of a specified size. A very small number is appended to the end
    of the list in order to guarantee worst-case performance for timing experiments.

    Parameters:
        num: the size of the list

    Return:
        a list of randomly generated numbers
    """
    rand_list = []
    for i in range(0,num-1):
        rand_list.append(random.randint(-100000, 100000))
    rand_list.append(-100000000)
    return rand_list


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


def sym_matrix_gen(size):
    """
    Helper function to create a symmetric square matrix consisting entirely of 0's

    Parameter:
        size: the size of the matrix to be created

    Return:
        a symmetric square matrix whose elements are all 0's, of the specified size
    """
    matrix = []
    inner = []
    for i in range(size):
        inner.append(0)
    for j in range(size):
        matrix.append(inner)
    return matrix


# Section to test and demonstrate each function
print("Demo for mystery(n) algorithm")
for num in range(26):
    print("The sum of squares up to ", num, " is ", mystery(num))
print()

print("Demo for Enigma(A) algorithm")
# Symmetric matrix
matrix1 = [[0,0,0],[0,0,0],[0,0,0]]
print(matrix1)
# Non-symmetric matrix
matrix2 = [[1,5,0],[3,1,9],[1,1,1]]
print(matrix2)
print(enigma(matrix1))
print(enigma(matrix2))
print()

print("Demo for q(n) algorithm")
for num in range(1,26):
    print(num, " squared is ", q(num))
print()

print("Demo for Riddle(A) algorithm")
test = [0,10,15,1,12,403,-1,-4,215,25]
print("The list is", test)
print("The minimum element in this list is ", Riddle(test))
print()

# Part 1 Experiment
print("Part 1 Time Experiment")
print()
for n in range(100,10001,100):
    sum_method = 0
    num_exp = 30
    for i in range(num_exp):
        sum_method += round((time_this(mystery, n)[0]),15)
    print(round(sum_method / num_exp, 15))
print()

# Part 2 Experiment
print("Part 2 Time Experiment")
print()
for n in range(10,1001,10):
    m = sym_matrix_gen(n)
    sum_method = 0
    num_exp = 30
    for i in range(num_exp):
        sum_method += round((time_this(enigma, m)[0]),15)
    print(round(sum_method / num_exp, 15))
print()

# Part 3 Experiment
print("Part 3 Time Experiment")
print()
for n in range(1,101,1):
    sum_method = 0
    num_exp = 30
    for i in range(num_exp):
        sum_method += round((time_this(q, n)[0]), 15)
    print(round(sum_method / num_exp, 15))
print()

# Part 4 Experiment
print("Part 4 Time Experiment")
print()

for size in range(10,1000,10):
    test_list = gen_list(size)
    sum_method = 0
    num_exp = 30
    for i in range(num_exp):
        sum_method += round((time_this(Riddle, test_list)[0]), 15)
    print(round(sum_method / num_exp, 15))
print()
