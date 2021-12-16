import functools
import operator
import timeit
import typing

import fire

T = typing.TypeVar("T")


class Packet:
    def __init__(self, version: int, packet_type: int, content: str):
        self.version = version
        self.packet_type = packet_type
        self.remaining_content = content

    @staticmethod
    def match_type(value: int) -> bool:
        raise NotImplementedError

    @classmethod
    def find_version_and_type(cls, content: str) -> tuple[int, int, str]:
        version = int(content[0:3], 2)
        packet_type = int(content[3:6], 2)

        return version, packet_type, content[6:]

    @classmethod
    def find_type(cls: T, value: int) -> T:
        for packet_type in cls.__subclasses__():
            if packet_type.match_type(value):
                return packet_type
        raise ValueError(f"No matching packet type for value {value}")

    @classmethod
    def parse(cls, content: str) -> "Packet":
        version, packet_type, content = cls.find_version_and_type(content)
        return cls.find_type(packet_type)(version, packet_type, content)

    def total_version(self) -> int:
        return 0

    def value(self) -> int:
        return 0


class LiteralPacket(Packet):
    def __init__(self, version: int, packet_type: int, content: str):
        super().__init__(version, packet_type, content)
        self.literal, self.remaining_content = self.parse_literal(self.remaining_content)

    def parse_literal(self, content: str) -> tuple[int, str]:
        continue_scanning = True
        value = ""
        while continue_scanning:
            continue_bit, *bits = content[:5]
            content = content[5:]
            continue_scanning = continue_bit == "1"
            value += "".join(bits)

        return int(value, 2), content

    @staticmethod
    def match_type(value: int) -> bool:
        return value == 4

    def total_version(self) -> int:
        return self.version

    def value(self) -> int:
        return self.literal


class OperatorPacket(Packet):
    def __init__(self, version: int, packet_type: int, content: str):
        super().__init__(version, packet_type, content)
        self.length_type_id, self.remaining_content = self.get_length_type_id(self.remaining_content)
        self.length, self.remaining_content = self.get_length(self.remaining_content)

        if self.length_type_id == 0:
            self.sub_packets, self.remaining_content = self.parse_sub_packets_via_length(self.remaining_content)
        else:
            self.sub_packets, self.remaining_content = self.parse_sub_packets_via_count(self.remaining_content)

    def get_length_type_id(self, content: str) -> tuple[int, str]:
        length_type_id = content[0]
        content = content[1:]
        return int(length_type_id), content

    def get_length(self, content: str) -> tuple[int, str]:
        length = 15 if self.length_type_id == 0 else 11
        return int(content[:length], 2), content[length:]

    def parse_sub_packets_via_count(self, content: str) -> tuple[list[Packet], str]:
        packets = []
        for _ in range(self.length):
            packet = Packet.parse(content)
            content = packet.remaining_content
            packets.append(packet)
        return packets, content

    def parse_sub_packets_via_length(self, content: str) -> tuple[list[Packet], str]:
        remaining_content = content[self.length :]
        content = content[: self.length]
        packets = []
        while content:
            packet = Packet.parse(content)
            content = packet.remaining_content
            packets.append(packet)
        return packets, remaining_content

    @staticmethod
    def match_type(value: int) -> bool:
        return value != 4

    def total_version(self) -> int:
        return self.version + sum(packet.total_version() for packet in self.sub_packets)

    def value(self) -> int:
        if self.packet_type == 0:
            return sum(packet.value() for packet in self.sub_packets)
        elif self.packet_type == 1:
            return functools.reduce(operator.mul, (packet.value() for packet in self.sub_packets))
        elif self.packet_type == 2:
            return min(packet.value() for packet in self.sub_packets)
        elif self.packet_type == 3:
            return max(packet.value() for packet in self.sub_packets)
        elif self.packet_type == 5:
            return int(self.sub_packets[0].value() > self.sub_packets[1].value())
        elif self.packet_type == 6:
            return int(self.sub_packets[0].value() < self.sub_packets[1].value())
        elif self.packet_type == 7:
            return int(self.sub_packets[0].value() == self.sub_packets[1].value())


def main(input_file: str = "input.txt") -> None:
    with open(input_file) as f:
        data = f.read().strip()

    data = "".join(bin(int(char, 16))[2:].zfill(4) for char in data)
    packet = Packet.parse(data)
    print(packet.value())


if __name__ == "__main__":
    print(timeit.Timer(lambda: fire.Fire(main)).timeit(1))
