from typing import Dict, List, Optional
from io import StringIO
import sys
from commands import Command
from editor_state import TextEditor


class Keyboard:
    def __init__(self, editor: TextEditor) -> None:

        self.key_map: Dict[str, Command] = {}
        self.history: List[Command] = []
        self.redo_stack: List[Command] = []
        self.editor: TextEditor = editor

    def add_association(self, key: str, command: Command) -> None:
        self.key_map[key] = command

    def execute_key(self, key: str) -> None:
        command = self.key_map.get(key)
        if command:
            try:
                command.execute(self.editor)
                self.history.append(command)
                self.redo_stack.clear()
            except Exception as e:
                print(f"Ошибка при выполнении команды для клавиши {key}: {e}", file=sys.stderr)
        else:
            print(f"Клавиша {key} не ассоциирована с командой.", file=sys.stderr)

    def undo(self) -> None:
        if self.history:
            command = self.history.pop()
            try:
                command.undo(self.editor)
                self.redo_stack.append(command)
            except Exception as e:
                print(f"Ошибка при отмене команды: {e}", file=sys.stderr)
        else:
            print("Нет команд для отмены.", file=sys.stderr)

    def redo(self) -> None:
        if self.redo_stack:
            command = self.redo_stack.pop()
            try:
                command.execute(self.editor)
                self.history.append(command)
            except Exception as e:
                print(f"Ошибка при повторении команды: {e}", file=sys.stderr)
        else:
            print("Нет команд для повторения.", file=sys.stderr)

    def get_key_map(self) -> Dict[str, Command]:
        return self.key_map.copy()
