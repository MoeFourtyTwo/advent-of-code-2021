import pytest

from main import Line, Point


@pytest.mark.parametrize("line, expected", [
    (Line(Point(0, 0), Point(1, 1)), True),
    (Line(Point(0, 0), Point(3, 0)), False),
    (Line(Point(0, 1), Point(1, 0)), False),
])
def test_is_45_degrees(line, expected):
    assert line.is_45_degrees() == expected


@pytest.mark.parametrize("line, expected", [
    (Line(Point(0, 0), Point(1, 1)), False),
    (Line(Point(0, 0), Point(3, 0)), False),
    (Line(Point(0, 1), Point(1, 0)), True),
])
def test_is_135_degrees(line, expected):
    assert line.is_135_degrees() == expected
