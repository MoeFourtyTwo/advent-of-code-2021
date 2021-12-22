from main import Cuboid, Span


def test_cuboid_volume():
    cuboid = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )

    assert cuboid.volume == 27


def test_cuboid_intersection_all_overlap():
    cuboid_1 = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )
    cuboid_2 = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )

    intersections = cuboid_1.intersect(cuboid_2)

    assert sum(i.volume for i in intersections) == 27


def test_cuboid_intersection():
    cuboid_1 = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )
    cuboid_2 = Cuboid(
        x=Span.from_inclusive(11, 13), y=Span.from_inclusive(11, 13), z=Span.from_inclusive(11, 13), value=True
    )

    intersections = cuboid_1.intersect(cuboid_2)

    assert sum(i.volume for i in intersections) == 27 + 19


def test_cuboid_intersection_off():
    cuboid_1 = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )
    cuboid_2 = Cuboid(
        x=Span.from_inclusive(11, 13), y=Span.from_inclusive(11, 13), z=Span.from_inclusive(11, 13), value=False
    )

    intersections = cuboid_1.intersect(cuboid_2)

    assert sum(i.volume for i in intersections) == 19


def test_cuboid_no_intersection():
    cuboid_1 = Cuboid(
        x=Span.from_inclusive(10, 12), y=Span.from_inclusive(10, 12), z=Span.from_inclusive(10, 12), value=True
    )
    cuboid_2 = Cuboid(
        x=Span.from_inclusive(13, 13), y=Span.from_inclusive(11, 13), z=Span.from_inclusive(11, 13), value=True
    )

    cuboids = cuboid_1.intersect(cuboid_2)

    assert sum(i.volume for i in cuboids if i.value) == 27 + 9


def test_cuboid_intersection_example():
    cuboid_1 = Cuboid(
        x=Span.from_inclusive(-5, 47), y=Span.from_inclusive(-31, 22), z=Span.from_inclusive(-19, 33), value=True
    )
    cuboid_2 = Cuboid(
        x=Span.from_inclusive(-44, 5), y=Span.from_inclusive(-27, 21), z=Span.from_inclusive(-14, 35), value=True
    )

    cuboids = cuboid_1.intersect(cuboid_2)

    assert sum(i.volume for i in cuboids if i.value) == 27 + 9
