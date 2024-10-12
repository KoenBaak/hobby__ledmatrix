import time
from dataclasses import dataclass
import RPi.GPIO as gpio

from driver.color import Color, ColorManager


@dataclass
class Profile:
    n_rows: int
    n_cols: int
    n_color_bits: int
    cycle_duration_ms: int
    fps: float


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
        self,
        n_rows: int = 64,
        n_cols: int = 64,
        n_color_bits: int = 8,
    ) -> None:
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.color_manager = ColorManager(n_bits=n_color_bits)
        self.cycle_duration_ms = sum(2**i for i in range(n_color_bits))
        self.frames_per_second = 1_000 / self.cycle_duration_ms
        self.prepare_pins()
        print(self.profile())

    def profile(self) -> Profile:
        return Profile(
            n_rows=self.n_rows,
            n_cols=self.n_cols,
            n_color_bits=self.color_manager.n_bits,
            cycle_duration_ms=self.cycle_duration_ms,
            fps=self.frames_per_second,
        )

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
            gpio.output(Pins.CLOCK, 0)

    def latch_data(self) -> None:
        gpio.output(Pins.LATCH, 1)
        gpio.output(Pins.LATCH, 0)

    def enable_output(self, delay_ms: int) -> None:
        gpio.output(Pins.OUTPUT_ENABLE, 1)
        time.sleep(delay_ms * 0.001)
        gpio.output(Pins.OUTPUT_ENABLE, 0)

    def display_row_pair(
        self, idx: int, top_row: list[Color], bottom_row: list[Color], bit_plane: int
    ) -> None:
        self.select_row_pair(idx=idx)
        self.clock_row_data(top_row=top_row, bottom_row=bottom_row, bit_plane=bit_plane)
        self.latch_data()
        self.enable_output(delay_ms=2**bit_plane)

    def run_pwm_cycle(self, frame: list[list[Color]]) -> None:
        for bit_plane in range(self.color_manager.n_bits - 1, -1, -1):
            for idx in range(self.n_rows // 2):
                self.display_row_pair(
                    idx=idx,
                    top_row=frame[idx],
                    bottom_row=frame[self.n_rows // 2 + idx],
                    bit_plane=bit_plane,
                )

    def show_frame(self, frame: list[list[Color]]) -> None:
        while True:
            self.run_pwm_cycle(frame=frame)
