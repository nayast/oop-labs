from typing import List
from log_level import LogLevel
from filters import ILogFilter
from formatters import ILogFormatter
from handlers import ILogHandler
import main


class Logger:
    def __init__(self, filters: List[ILogFilter], formatters: List[ILogFormatter], handlers: List[ILogHandler]) -> None:
        self.filters = filters
        self.formatters = formatters
        self.handlers = handlers

    def log(self, log_level: LogLevel, text: str) -> None:

        if log_level not in [LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR]:
            raise ValueError(f"Invalid log level: {log_level}")
        if not all(f.match(log_level, text) for f in self.filters):
            return

        formatted_text = text
        for formatter in self.formatters:
            formatted_text = formatter.format(log_level, formatted_text)

        for handler in self.handlers:
            try:
                handler.handle(log_level, formatted_text)
            except Exception as e:
                print(f"Handler {handler.__class__.__name__} failed: {e}")

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)

print(__name__)
