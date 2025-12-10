from typing import Protocol
from log_level import LogLevel
from datetime import datetime


class ILogFormatter(Protocol):
    def format(self, log_level: LogLevel, text: str) -> str:
        ...


class StandardLogFormatter:
    def format(self, log_level: LogLevel, text: str) -> str:
        timestamp = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        return f"[{log_level.value}] [{timestamp}] {text}"
