import sys

from pretty_printer import Printer
from color_enum import Color

print("\033[2J\033[H", end='')

Printer.print_static("THIS", Color.RED, (2, 10), "✂️", "fonts/size5.json")

Printer.print_static("IS", Color.ORANGE, (8, 5), "𓃘", "fonts/size5.json")

with Printer(Color.WHITE, (16, 5), "🐻", "fonts/size5.json") as printer:
    printer.print("BEAR")

with Printer(Color.PINK, (22, 5), "✧", "fonts/size7.json") as printer:
    printer.print("LABA")

with Printer(Color.DARKPINK, (30, 5), "۞", "fonts/size7.json") as printer:
    printer.print("YIPPIEE")

print("\033[40;1H", end='')
print(sys.getsizeof('𓃘'))
