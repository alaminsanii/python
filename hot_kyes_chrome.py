import keyboard
import sys
import pyautogui
import time

pyautogui.FAILSAFE = True  # move mouse to top-left corner to emergency-stop

HOTKEYS = {
    'shift+1': (348, 270),
    'shift+2': (534, 339),
    'shift+3': (342, 266),
    'shift+4': (769, 263),
    'shift+5': (1027, 631),
}

def make_clicker(x, y):
    def click():
        try:
            pyautogui.click(x, y)
        except pyautogui.FailSafeException:
            print("FailSafe triggered. Exiting.")
            sys.exit()
        except Exception as e:
            print(f"Click error: {e}")
    return click

for hotkey, (x, y) in HOTKEYS.items():
    keyboard.add_hotkey(hotkey, make_clicker(x, y), suppress=True, trigger_on_release=True)

print("Hotkeys active. Press Ctrl+C to exit.")

try:
    while True:
        time.sleep(0.09)  # more stable than keyboard.wait() for long runs
except KeyboardInterrupt:
    print("You have exited.")
    keyboard.unhook_all()
    sys.exit()