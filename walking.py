from typing import TypeVar
from pytermgui import (
    getch,
    keys,
    save_cursor,
    restore_cursor,
    report_cursor,
    Widget,
    clear,
    get_terminal,
    mouse_handler,
)

def inline(widget):
    # Make sure we use the global terminal
    terminal = get_terminal()

    widget.pos = report_cursor()

    def _print_widget():
        save_cursor()

        for line in widget.get_lines():
            print(line)

        restore_cursor()

    def _clear_widget():
        save_cursor()

        for _ in range(widget.height):
            clear("line")
            terminal.write("\n")

        restore_cursor()
        terminal.flush()

    _print_widget()

    with mouse_handler(["press_hold", "hover"], "decimal_xterm") as translate:
        while True:
            key = getch(interrupts=False)

            if key == keys.CTRL_C:
                break

            if not widget.handle_key(key):
                events = translate(key)
                # Don't try iterating when there are no events
                if events is None:
                    continue

                for event in events:
                    if event is None:
                        continue
                    widget.handle_mouse(event)

            _clear_widget()
            _print_widget()

    _clear_widget()
    return widget

