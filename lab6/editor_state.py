from typing import Protocol


class TextEditor(Protocol):
    def insert_text(self, s: str) -> None:
        pass

    def delete_last_char(self) -> None:
        pass

    def log_message(self, msg: str) -> None:
        pass

    def get_current_text(self) -> str:
        pass
