from io import StringIO

import numpy as np

from main import next_iteration


def test_next_iteration():
    step_0 = StringIO(
        """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
    )
    data_0 = np.genfromtxt(step_0, dtype=int, delimiter=1)
    step_1 = StringIO(
        """6594254334
3856965822
6375667284
7252447257
7468496589
5278635756
3287952832
7993992245
5957959665
6394862637"""
    )
    data_1 = np.genfromtxt(step_1, dtype=int, delimiter=1)
    step_2 = StringIO(
        """8807476555
5089087054
8597889608
8485769600
8700908800
6600088989
6800005943
0000007456
9000000876
8700006848"""
    )
    data_2 = np.genfromtxt(step_2, dtype=int, delimiter=1)

    pred, _ = next_iteration(data_0)
    np.testing.assert_equal(pred, data_1)
    pred, _ = next_iteration(data_1)
    print()
    print(pred)
    print(data_2)
    np.testing.assert_equal(pred, data_2, verbose=True)
