import pytest

from main import Packet, OperatorPacket, LiteralPacket


@pytest.mark.parametrize(
    "data, expected",
    [
        ("8A004A801A8002F478", 16),
        ("620080001611562C8802118E34", 12),
        ("C0015000016115A2E0802F182340", 23),
        ("A0016C880162017C3686B18A3D4780", 31),
    ],
)
def test_parse(data, expected):
    data = "".join(bin(int(char, 16))[2:].zfill(4) for char in data)

    packet = Packet.parse(data)
    assert packet.total_version() == expected
