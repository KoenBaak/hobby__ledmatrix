import RPi.GPIO as gpio

from driver.color import Color, ColorManager


class Pins:
    R1 = 14
    G1 = 15
    B1 = 18
    R2 = 23
    G2 = 24
    B2 = 25
    A = 7
    B = 12
    C = 16
    D = 20
    E = 8
    CLOCK = 21
    LATCH = 26
    OUTPUT_ENABLE = 19


class MatrixDriver:
    def __init__(
        self, n_rows: int = 64, n_cols: int = 64, n_color_bits: int = 8
    ) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.color_manager = ColorManager(n_bits=n_color_bits)
        self.prepare_pins()

    def prepare_pins(self) -> None:
        gpio.setmode(gpio.BCM)
        for pin in [
            Pins.R1,
            Pins.G1,
            Pins.B1,
            Pins.R2,
            Pins.G2,
            Pins.B2,
            Pins.A,
            Pins.B,
            Pins.C,
            Pins.D,
            Pins.E,
            Pins.CLOCK,
            Pins.LATCH,
            Pins.OUTPUT_ENABLE,
        ]:
            gpio.setup(pin, gpio.OUT, initial=0)

    def select_row_pair(self, idx: int) -> None:
        gpio.output(Pins.A, idx & 1)
        gpio.output(Pins.B, idx & 2)
        gpio.output(Pins.C, idx & 4)
        gpio.output(Pins.D, idx & 8)
        gpio.output(Pins.E, idx & 16)

    def clock_row_data(
        self, top_row: list[Color], bottom_row: list[Color], bit_plane: int
    ) -> None:
        for col in range(self.n_cols):
            gpio.output(Pins.R1, (top_row[col].red >> bit_plane) & 1)
            gpio.output(Pins.G1, (top_row[col].green >> bit_plane) & 1)
            gpio.output(Pins.B1, (top_row[col].blue >> bit_plane) & 1)
            gpio.output(Pins.R2, (bottom_row[col].red >> bit_plane) & 1)
            gpio.output(Pins.G2, (bottom_row[col].green >> bit_plane) & 1)
            gpio.output(Pins.B2, (bottom_row[col].blue >> bit_plane) & 1)
            gpio.output(Pins.CLOCK, 1)
            gpio.output(Pins.OUTPUT_ENABLE, 0)
            gpio.output(Pins.CLOCK, 0)
            gpio.output(Pins.OUTPUT_ENABLE, 1)

    def latch_data(self) -> None:
        gpio.output(Pins.LATCH, 1)
        gpio.output(Pins.LATCH, 0)

    def display_row_pair(
        self, idx: int, top_row: list[Color], bottom_row: list[Color], bit_plane: int
    ) -> None:
        self.select_row_pair(idx=idx)
        self.clock_row_data(top_row=top_row, bottom_row=bottom_row, bit_plane=bit_plane)
        self.latch_data()

    def run_cycle(self, frame: list[list[Color]]) -> None:
        for bit_plane in range(self.color_manager.n_bits):
            for _ in range(10, 10*2**bit_plane):
                for idx in range(self.n_rows // 2):
                    self.display_row_pair(
                        idx=idx,
                        top_row=frame[idx],
                        bottom_row=frame[self.n_rows // 2 + idx],
                        bit_plane=bit_plane,
                    )

    def show_frame(self, frame: list[list[Color]]) -> None:
        while True:
            self.run_cycle(frame=frame)
