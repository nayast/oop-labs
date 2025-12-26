from io import StringIO
from typing import List
from editor_state import TextEditor

class StringIOEditor(TextEditor):
    def __init__(self) -> None:
        self.text: str = ""
        self.messages: List[str] = []

    def insert_text(self, s: str) -> None:
        self.text += s

    def delete_last_char(self) -> None:
        if self.text:
            self.text = self.text[:-1]

    def log_message(self, msg: str) -> None:
        self.messages.append(msg)
        self.text += msg + "\n"

    def get_current_text(self) -> str:
        return self.text

    def get_all_messages(self) -> List[str]:
        return self.messages.copy()
