from operator import itemgetter

import numpy as np

from main import view_to_dec


def test_view_to_dec():
    assert view_to_dec(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]])) == 34
