import keyboard
import sys
import time
from pywinauto.mouse import click
from pywinauto import mouse

HOTKEYS = {
    'alt + shift + 1': (30, 235, True),      # double click + Enter
    'alt + shift + 2': (260, 485, False),    # single click
    'shift + 1': (348, 270, False),
    'shift + 2': (534, 339, False),
    'shift + 3': (342, 266, False),
    'shift + 4': (769, 263, False),
    'shift + 5': (1027, 631, False)
}

def make_clicker(x, y, is_double=False):
    def click_action():
        try:
            # single click at pixel
            click(button='left', coords=(x, y))

            # extra action for "double mode"
            if is_double:
                click(button='left', coords=(x, y))
                keyboard.press_and_release('enter')

        except Exception as e:
            print(f"Click error: {e}")
            sys.exit()

    return click_action


for hotkey, (x, y, is_double) in HOTKEYS.items():
    keyboard.add_hotkey(
        hotkey,
        make_clicker(x, y, is_double),
        suppress=True,
        trigger_on_release=True
    )

print("Hotkeys active (pywinauto version). Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.07)
except KeyboardInterrupt:
    print("Exited cleanly.")
    keyboard.unhook_all()
    sys.exit()