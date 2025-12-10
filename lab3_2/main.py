from log_level import LogLevel
from filters import LevelFilter, SimpleLogFilter
from formatters import StandardLogFormatter
from handlers import ConsoleHandler, FileHandler, EventLogHandler
from logger import Logger


def main() -> None:
    
    formatter = StandardLogFormatter()
    console_handler = ConsoleHandler()
    file_handler = FileHandler("../lab3_2/logs.txt")
    eventlog_handler = EventLogHandler('MyLoggingApp')
    logger = Logger(
        # filters=[LevelFilter(LogLevel.WARN), SimpleLogFilter("connection")],
        filters=[],
        formatters=[formatter],
        handlers=[console_handler, file_handler, eventlog_handler]
    )
    logger.log_info("Application started successfully")
    logger.log_info("User logged in")
    logger.log_info("Connection success")
    logger.log_warn("Low disk space warning")
    logger.log_warn("Connection timeout")
    logger.log_error("Database connection failed")
    logger.log_error("Critical ERROR in module X")
    logger.log_error("System crash occurred")


if __name__ == "__main__":
    main()
