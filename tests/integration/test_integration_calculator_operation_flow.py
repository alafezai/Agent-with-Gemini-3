import pytest
import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from calculator import add, subtract, multiply, divide

def test_calculator_operations():
    """
    Integration test to verify the calculator operations.
    """
    assert add(2, 3) == 5
    assert subtract(5, 2) == 3
    assert multiply(3, 4) == 12
    assert divide(10, 2) == 5.0
    
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)