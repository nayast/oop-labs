from typing import Protocol
from log_level import LogLevel
import socket
import logging
import logging.handlers
import ftplib
import io


class ILogHandler(Protocol):
    def handle(self, log_level: LogLevel, text: str) -> None:
        ...


class FileHandler:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(text + '\n')
        except IOError as e:
            print(f"Failed to write to file {self.filename}: {e}")


class SocketHandler:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except Exception as e:
            print(f"Failed to connect to {host}:{port}: {e}")
            self.sock = None

    def handle(self, log_level: LogLevel, text: str) -> None:
        if self.sock:
            try:
                self.sock.sendall((text + '\n').encode('utf-8'))
            except Exception as e:
                print(f"Failed to send to socket: {e}")


class ConsoleHandler:
    def handle(self, log_level: LogLevel, text: str) -> None:
        color_map = {
            LogLevel.INFO: '\033[37m',
            LogLevel.WARN: '\033[33m',
            LogLevel.ERROR: '\033[31m'
        }
        reset = '\033[0m'
        colored_text = f"{color_map[log_level]}{text}{reset}"
        print(colored_text)


class EventLogHandler:
    def __init__(self, appname: str = 'MyApp') -> None:
        self.handler = logging.handlers.NTEventLogHandler(appname)
        self.logger = logging.getLogger('eventlog_logger')
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def handle(self, log_level: LogLevel, text: str) -> None:
        level_map = {
            LogLevel.INFO: logging.INFO,
            LogLevel.WARN: logging.WARNING,
            LogLevel.ERROR: logging.ERROR
        }
        try:
            self.logger.log(level_map[log_level], text)
        except Exception as e:
            print(f"Failed to log to Event Log: {e}")


class FtpHandler:
    def __init__(self, host: str, username: str, password: str, filename: str) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            ftp = ftplib.FTP(self.host)
            ftp.login(self.username, self.password)
            bio = io.BytesIO((text + '\n').encode('utf-8'))
            ftp.storbinary(f'STOR {self.filename}', bio)
            ftp.quit()
        except Exception as e:
            print(f"Failed to upload to FTP {self.host}: {e}")
