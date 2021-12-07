import numpy as np
import pytest

from main import calculate_cost


@pytest.mark.parametrize(
    "data, target, expected",
    [
        (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 1, 41),
        (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 2, 37),
        (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 3, 39),
        (np.array([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 10, 71),
    ],
)
def test_calculate_cost(data, target, expected):
    assert calculate_cost(data, target) == expected
