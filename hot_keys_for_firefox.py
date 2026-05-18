import keyboard
import sys
import time
from pywinauto.mouse import click



CLICKS = {
    'shift+1': (352, 274),
    'shift+2': (522, 352),
    'shift+3': (326, 279),
    'shift+4': (842, 265),
    'shift+5': (888, 705),
}

def make_clicker(coords):
    def clicker():
        try:
            click(button='left', coords=coords)
        except Exception as e:
            print(f"Click failed at {coords}: {e}")
    return clicker


for hotkey, coords in CLICKS.items():
    keyboard.add_hotkey(
        hotkey,
        make_clicker(coords),
        suppress=True,
        trigger_on_release=True
    )

print("Mission activeted. Press Ctrl+C to exit.")


try:
    while True:
        time.sleep(0.1)   # stable alternative to keyboard.wait()
except KeyboardInterrupt:
    print("You have exited.")
    keyboard.unhook_all()  # cleanly release all hooks
    sys.exit()