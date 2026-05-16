import keyboard
import sys
import pyautogui

def first():
    pyautogui.click(348, 270)

def second():
    pyautogui.click(534, 339)

def third():
    pyautogui.click(342, 266)

def fourth():
    pyautogui.click(769, 263)

def fifth():
    pyautogui.click(1027, 631)

keyboard.add_hotkey('shift + 1', first, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('shift + 2', second, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('shift + 3', third, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('shift + 4', fourth, suppress=True, trigger_on_release=True)
keyboard.add_hotkey('shift + 5', fifth, suppress=True, trigger_on_release=True)



print("Hotkeys active. Press Ctrl+C to exit.")

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("You have exited.")
    sys.exit()