from main import find_mapping


def test_find_mapping():
    patterns = [
        set("acedgfb"),
        set("cdfbe"),
        set("gcdfa"),
        set("fbcad"),
        set("dab"),
        set("cefabd"),
        set("cdfgeb"),
        set("eafb"),
        set("cagedb"),
        set("ab"),
    ]

    assert find_mapping(patterns) == {
        "d": "a",
        "e": "b",
        "a": "c",
        "f": "d",
        "g": "e",
        "b": "f",
        "c": "g",
    }
