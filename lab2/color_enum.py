from enum import Enum

class Color(Enum):
    RESET = "\033[0m"
    RED = "\033[01;38;05;160m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    PINK = "\033[01;38;05;169m"
    DARKPINK = "\033[01;38;05;125m"
    ORANGE = "\033[01;38;05;215m"
