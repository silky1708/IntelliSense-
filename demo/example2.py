# variables, and functions
import numpy as np

b = 4
a = b

def add(x: int, y):
    return x+y
    
c = add(4, 5)

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
        
d = fib(10)

np.linspace()