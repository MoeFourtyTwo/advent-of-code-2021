import pytest

from main import search, parse_graph


@pytest.mark.parametrize(
    "graph, expected_path_count",
    [
        (
            parse_graph(
                """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines()
            ),
            36,
        ),
        (
            parse_graph(
                """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines()
            ),
            103,
        ),
        (
            parse_graph(
                """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines()
            ),
            3509,
        ),
    ],
)
def test_search(graph, expected_path_count):
    assert len(search(graph, "start", [], False)) == expected_path_count
