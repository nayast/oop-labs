import json
import math
import sys
from typing import Tuple
from color_enum import Color

class Printer:
    @staticmethod
    def print_static(text: str, color: Color, position: Tuple[int, int], symbol: str, font_path: str) -> None:
        with open(font_path, 'r') as f: # try
            font = json.load(f)
        row, col = position
        sample_char = next(iter(font.values()))
        height = len(sample_char)
        for i in range(height):
            print(f"\033[{row + i};{col}H", end='')  # func for position
            line_str = ""
            for char in text.upper():
                if char in font:
                    template = font[char]
                    math.ceil(sys.getsizeof(symbol) / 43)
                    line_part = template[i].replace('*', symbol)
                    line_str += line_part + " "
                else:
                    line_str += "  "
            print(f"{color.value}{line_str.rstrip()}{Color.RESET.value}", end='')
        print()

    def __init__(self, color: Color, position: Tuple[int, int], symbol: str, font_path: str) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font_path = font_path

    def __enter__(self) -> 'Printer':
        print("\033[s", end='')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print("\033[u", end='')

    def print(self, text: str) -> None:
        Printer.print_static(text, self.color, self.position, self.symbol, self.font_path)
