# Intellisense++

def add(x: int, y):
    return x+y


def max(a, b):
    if a >= b:
        return a
    return b


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
        

def factorial(num):
    factorial = 1

    # check if the number is negative, positive or zero
    if num < 0:
        print("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        print("The factorial of 0 is 1")
    else:
        for i in range(1,num + 1):
            factorial = factorial*i
        print("The factorial of",num,"is",factorial)


def isPalindrome(s):
    return s == s[::-1]


def is_subseq(x, y):
    it = iter(y)
    return all(c in it for c in x)

base = 4
another_base = base
sum_of_literals = add(4, 5)
fibonacci_10 = fib(10)

e = fib()
# f = factorial() 
