from abc import ABC, abstractmethod
from typing import Dict, Any, Type
import json
import sys
from commands import Command


command_dict: Dict[str, Type["Command"]] = {}


class DictRepresenter(ABC):
    @abstractmethod
    def to_dict(self, obj: Any) -> Dict[str, Any]:
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> Any:
        pass


class Serializer(ABC):
    @abstractmethod
    def serialize(self, data: Dict[str, Any]) -> str:
        pass


class Deserializer(ABC):
    @abstractmethod
    def deserialize(self, data: str) -> Dict[str, Any]:
        pass


class JsonSerializer(Serializer):
    def serialize(self, data: Dict[str, Any]) -> str:
        try:
            return json.dumps(data, indent=4)
        except Exception as e:
            print(f"Ошибка сериализации: {e}", file=sys.stderr)
            return ""


class JsonDeserializer(Deserializer):
    def deserialize(self, data: str) -> Dict[str, Any]:
        try:
            return json.loads(data)
        except Exception as e:
            print(f"Ошибка десериализации: {e}", file=sys.stderr)
            return {}


def register_command(cls: Type["Command"]) -> Type["Command"]:
    command_dict[cls.type_name] = cls
    return cls

class CommandDictRepresenter(DictRepresenter):
    def to_dict(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, Command):
            return obj.to_dict()
        raise ValueError(f"Объект не является командой: {type(obj)}")

    def from_dict(self, data: Dict[str, Any]) -> Any:
        cmd_type = data.get("type")
        if not cmd_type:
            raise ValueError("Поле 'type' отсутствует в данных команды")

        import commands

        if not command_dict:
            for attr_name in dir(commands):
                attr = getattr(commands, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Command)
                    and attr is not Command
                ):
                    command_dict[attr.type_name] = attr

        if cmd_type not in command_dict:
            raise ValueError(f"Неизвестный тип команды: {cmd_type}")

        cls = command_dict[cmd_type]
        return cls.from_dict(data)
