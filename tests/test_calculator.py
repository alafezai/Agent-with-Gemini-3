import pytest
from calculator import *

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_positive_and_negative():
    assert add(2, -3) == -1

def test_add_zero():
    assert add(5, 0) == 5

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000

def test_subtract_positive_numbers():
    assert subtract(5, 2) == 3

def test_subtract_negative_numbers():
    assert subtract(-5, -2) == -3

def test_subtract_positive_and_negative():
    assert subtract(5, -2) == 7

def test_subtract_zero():
    assert subtract(5, 0) == 5

def test_subtract_large_numbers():
    assert subtract(2000000, 1000000) == 1000000

def test_multiply_positive_numbers():
    assert multiply(2, 3) == 6

def test_multiply_negative_numbers():
    assert multiply(-2, -3) == 6

def test_multiply_positive_and_negative():
    assert multiply(2, -3) == -6

def test_multiply_zero():
    assert multiply(5, 0) == 0

def test_multiply_large_numbers():
    assert multiply(1000, 2000) == 2000000

def test_divide_positive_numbers():
    assert divide(6, 2) == 3

def test_divide_negative_numbers():
    assert divide(-6, -2) == 3

def test_divide_positive_and_negative():
    assert divide(6, -2) == -3

def test_divide_by_one():
    assert divide(5, 1) == 5

def test_divide_large_numbers():
    assert divide(2000000, 1000000) == 2

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

def test_square_positive_number():
    assert square(2) == 8

def test_square_negative_number():
    assert square(-2) == -8

def test_square_zero():
    assert square(0) == 0

def test_square_large_number():
    assert square(100) == 1000000