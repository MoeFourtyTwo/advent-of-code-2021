import pytest

from main import Packet, OperatorPacket, LiteralPacket


@pytest.mark.parametrize(
    "data, expected",
    [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ],
)
def test_parse(data, expected):
    data = "".join(bin(int(char, 16))[2:].zfill(4) for char in data)

    packet = Packet.parse(data)
    assert packet.value() == expected
