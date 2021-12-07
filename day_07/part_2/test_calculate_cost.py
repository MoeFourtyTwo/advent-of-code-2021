import numpy as np
import pytest

from main import calculate_cost


@pytest.mark.parametrize("data, target, expected", [
    (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 5, 168.0),
    (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 2, 206.0),
])
def test_calculate_cost(data, target, expected):
    assert calculate_cost(data, target) == expected
