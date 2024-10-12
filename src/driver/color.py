from typing import NamedTuple


class Color(NamedTuple):
    red: int
    green: int
    blue: int


class ColorManager:
    def __init__(self, n_bits: int = 1) -> None:
        self.n_bits = n_bits
        self.max_value = 2**n_bits - 1

    def relative(self, red: float, green: float, blue: float) -> Color:
        return Color(
            red=int(self.max_value * red),
            green=int(self.max_value * green),
            blue=int(self.max_value * blue),
        )

    def red(self) -> Color:
        return self.relative(1, 0, 0)

    def green(self) -> Color:
        return self.relative(0, 1, 0)

    def blue(self) -> Color:
        return self.relative(0, 0, 1)
