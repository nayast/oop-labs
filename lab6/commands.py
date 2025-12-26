from abc import ABC, abstractmethod
from typing import Any, Optional, ClassVar, Dict
import sys
from editor_state import TextEditor


class Command(ABC):
    type_name: ClassVar[str]

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'type_name') or cls.type_name == Command.type_name:
            cls.type_name = cls.__name__

    @abstractmethod
    def execute(self, editor: TextEditor) -> None:
        pass

    @abstractmethod
    def undo(self, editor: TextEditor) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Command":
        pass


class PrintCommand(Command):
    def __init__(self, symbol: str) -> None:
        self.symbol: str = symbol

    def execute(self, editor: TextEditor) -> None:
        try:
            editor.insert_text(self.symbol)
        except Exception as e:
            print(f"Ошибка при выполнении команды печати: {e}", file=sys.stderr)

    def undo(self, editor: TextEditor) -> None:
        try:
            editor.delete_last_char()
        except Exception as e:
            print(f"Ошибка при отмене команды печати: {e}", file=sys.stderr)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_name,
            "symbol": self.symbol
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PrintCommand":
        return cls(symbol=data["symbol"])


class VolumeUpCommand(Command):
    def execute(self, editor: TextEditor) -> None:
        try:
            editor.log_message("volume increased +20%")
        except Exception as e:
            print(f"Ошибка при выполнении команды увеличения звука: {e}", file=sys.stderr)

    def undo(self, editor: TextEditor) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type_name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VolumeUpCommand":
        return cls()


class VolumeDownCommand(Command):
    def execute(self, editor: TextEditor) -> None:
        try:
            editor.log_message("volume decreased -20%")
        except Exception as e:
            print(f"Ошибка при выполнении команды уменьшения звука: {e}", file=sys.stderr)

    def undo(self, editor: TextEditor) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type_name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VolumeDownCommand":
        return cls()


class MediaPlayerCommand(Command):
    def execute(self, editor: TextEditor) -> None:
        try:
            editor.log_message("media player launched")
        except Exception as e:
            print(f"Ошибка при выполнении команды запуска медиа плеера: {e}", file=sys.stderr)

    def undo(self, editor: TextEditor) -> None:
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {"type": self.type_name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MediaPlayerCommand":
        return cls()
