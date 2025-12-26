from typing import Dict, Any
import os
from keyboard import Keyboard
from serializer import Serializer, Deserializer, DictRepresenter, JsonSerializer, JsonDeserializer, CommandDictRepresenter
from commands import Command
from editor_state import TextEditor


class KeyboardStateSaver:
    def __init__(self, file_path: str, serializer: Serializer, deserializer: Deserializer, representer: DictRepresenter) -> None:
        self.file_path: str = file_path
        self.serializer: Serializer = serializer
        self.deserializer: Deserializer = deserializer
        self.representer: DictRepresenter = representer

    def save(self, keyboard: Keyboard) -> None:
        key_map = keyboard.get_key_map()
        data: Dict[str, Any] = {}
        for key, command in key_map.items():
            data[key] = self.representer.to_dict(command)
        serialized = self.serializer.serialize(data)
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(serialized)
        except Exception as e:
            print(f"Ошибка сохранения состояния: {e}", file=__import__('sys').stderr)

    def load(self, keyboard: Keyboard) -> None:
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            data = self.deserializer.deserialize(content)
            for key, cmd_data in data.items():
                command = self.representer.from_dict(cmd_data)
                keyboard.add_association(key, command)
        except Exception as e:
            print(f"Ошибка загрузки состояния: {e}", file=__import__('sys').stderr)