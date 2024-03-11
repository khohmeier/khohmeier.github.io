# K. Hohmeier
# CSC 380
# Homework 1

import math
import time
import random


def gcd_euclid(m, n):
    """
    Calculates the greatest common divisor of two nonnegative, not-both-0 integers via the Eucliean algorithm

    Parameters:
        m: a non-negative integer
        n: a non-negative integer

    Return:
        the gcd of the two integers
    """

    while n != 0:
        r = m % n
        m = n
        n = r

    return m


def gcd_recursive(m, n):
    """
    Implements a recursive approach to finding the greatest common divisor of two integers

    Parameters:
        m: a non-negative integer
        n: a non-negative integer

    Return:
        a recursive call that eventually returns the greatest common divisor of m and n
    """
    if n == 0:
        return m
    else:
        return gcd_recursive(n, m % n)


def gcd_consecutive(m, n):
    """
    Implements the Consecutive Integer Checking Algorithm, which calculates the greatest common divisor of two integers

    Parameters:
        m: an integer
        n: an integer

    Return:
        the greatest common divisor of m and n
    """
    minimum = min(m, n)
    check_boolean = False

    while not check_boolean:
        result_one = m % minimum
        if result_one == 0:
            result_two = n % minimum
            if result_two == 0:
                check_boolean = True
                return minimum
        minimum -= 1


def sieve_of_e(n):
    """
    Implements the sieve of Eratosthenes

    Parameters:

        n: a positive integer greater than 1

    Return:
        A list of all prime numbers less than or equal to n
    """
    primes = [0,0]

    for p in range(2,n+1):
        primes.append(p)

    for p in range(2,math.floor(math.sqrt(n))+1):
        if primes[p] != 0:
            j = p*p
            while j <= n and j <= len(primes) - 1:
                primes[j] = 0
                j = j + p

    i = 0
    final_primes = []
    for p in range(2,n+1):
        if primes[p] != 0:
            final_primes.append(primes[p])
        i += 1
    return final_primes


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


def digit_gen(digits):
    """
    A helper function that creates a pseudorandom number of size digits

    Parameters:
        digits: the number of digits of the numbers to be created

    Return:
        a tuple of the two numbers of digit length
    """
    start = 10**(digits-1)
    end = (10**digits)-1
    return random.randint(start, end)


# Code for testing the functions in Problem 1: the GCD algorithms
print("Euclid's Algorithm:")
for n in range(3,300,3):
    sum_method = 0
    num_exp = 20
    print(str(n) + " digits:")
    for i in range(num_exp+1):
        num1 = digit_gen(n)
        num2 = digit_gen(n)
        sum_method += round((time_this(gcd_euclid, num1, num2)[0]), 15)
    print(round(sum_method / num_exp, 15))

print()
print("Recursive Algorithm:")
for n in range(3,300,3):
    sum_method = 0
    num_exp = 20
    print(str(n) + " digits:")
    for i in range(num_exp+1):
        num1 = digit_gen(n)
        num2 = digit_gen(n)
        sum_method += round((time_this(gcd_recursive, num1, num2)[0]), 15)
    print(round(sum_method / num_exp, 15))

print()
print("Consecutive Integer Checking:")
for n in range(3,10):
    num1 = digit_gen(n)
    num2 = digit_gen(n)
    print(str(n) + " digits:")
    print(round((time_this(gcd_consecutive, num1, num2)[0]), 15))


# Code for testing the Sieve of E function in Problem 2
print()
print("Experiments for Sieve of Eratosthenes")
for num in range(100,10001,100):
    sum_method = 0
    num_exp = 20
    for i in range(num_exp+1):
        sum_method += round((time_this(sieve_of_e, num)[0]), 15)
    print(round(sum_method/num_exp, 15))
