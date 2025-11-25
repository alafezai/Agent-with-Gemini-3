def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # Bug: No check for division by zero
    return a / b

def square(n):
    # Bug: Returns cube instead of square
    return n * n * n
