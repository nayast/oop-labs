from io import StringIO
import sys
from keyboard import Keyboard
from commands import PrintCommand, VolumeUpCommand, VolumeDownCommand, MediaPlayerCommand
from memento import KeyboardStateSaver
from serializer import JsonSerializer, JsonDeserializer, CommandDictRepresenter
from text_editor import StringIOEditor


def main() -> None:
    editor = StringIOEditor()
    keyboard = Keyboard(editor)

    serializer = JsonSerializer()
    deserializer = JsonDeserializer()
    representer = CommandDictRepresenter()
    saver = KeyboardStateSaver('keyboard_state.json', serializer, deserializer, representer)

    saver.load(keyboard)

    if not keyboard.get_key_map():
        keyboard.add_association('a', PrintCommand('a'))
        keyboard.add_association('b', PrintCommand('b'))
        keyboard.add_association('c', PrintCommand('c'))
        keyboard.add_association('d', PrintCommand('d'))
        keyboard.add_association('ctrl++', VolumeUpCommand())
        keyboard.add_association('ctrl+-', VolumeDownCommand())
        keyboard.add_association('ctrl+p', MediaPlayerCommand())

    actions = ['a', 'b', 'c',  'undo', 'undo', 'redo', 'ctrl++', 'ctrl+-', 'ctrl+p', 'd', 'undo', 'undo']

    console_outputs = []
    for action in actions:
        if action == 'undo':
            keyboard.undo()
        elif action == 'redo':
            keyboard.redo()
        else:
            keyboard.execute_key(action)
        current_output = editor.get_current_text().strip()
        console_outputs.append(current_output)

    print("CONSOLE:")
    for i, action in enumerate(actions):
        print(action)
        print(console_outputs[i])

    saver.save(keyboard)

    try:
        with open('output.txt', 'w', encoding='utf-8') as f:
            for i, action in enumerate(actions):
                f.write(action + '\n')
                f.write(console_outputs[i] + '\n')
    except Exception as e:
        print(f"Ошибка записи в файл: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
