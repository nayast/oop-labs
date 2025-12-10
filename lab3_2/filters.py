from typing import Protocol
from log_level import LogLevel
import re


class ILogFilter(Protocol):
    def match(self, log_level: LogLevel, text: str) -> bool:
        ...


class SimpleLogFilter:
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.pattern.lower() in text.lower()


class ReLogFilter:
    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern)

    def match(self, log_level: LogLevel, text: str) -> bool:
        return bool(self.pattern.search(text))


class LevelFilter:
    def __init__(self, min_level: LogLevel) -> None:
        self.min_level = min_level

    def match(self, log_level: LogLevel, text: str) -> bool:
        levels = [LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR]
        return levels.index(log_level) >= levels.index(self.min_level)