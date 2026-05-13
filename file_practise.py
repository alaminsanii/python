"""Basic calculator CLI.

Accepts simple binary expressions like:
  4+4   10 - 3   -2.5 * 4   9/3

Prints the expression and the result, e.g. "4+4 = 8".
Supports +, -, *, / and handles division-by-zero and invalid input.
"""

import re
import threading
import time
import os

# Try to use the `keyboard` package for a clean global ESC watcher. If it's not
# available, fall back to the Windows `msvcrt` module.
try:
    import keyboard as _keyboard
except Exception:
    _keyboard = None
    import msvcrt


_EXPR_RE = re.compile(r'^\s*([+-]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\d+(?:\.\d+)?)\s*$')


def evaluate_expression(expr: str):
    """Evaluate a simple binary expression string and return result.

    Returns a tuple (success: bool, message_or_result).
    If success is True, message_or_result is the numeric result (int or float).
    If success is False, message_or_result is an error message string.
    """
    m = _EXPR_RE.match(expr)
    if not m:
        return False, "Invalid input. Enter like: 4+4 or 4 + 4"

    a_s, op, b_s = m.groups()
    a = float(a_s)
    b = float(b_s)

    if op == '+':
        res = a + b
    elif op == '-':
        res = a - b
    elif op == '*':
        res = a * b
    elif op == '/':
        if b == 0:
            return False, "Error: division by zero"
        res = a / b
    else:
        return False, "Invalid operator"

    # If result is an integer-valued float, convert to int for nicer display
    if isinstance(res, float) and res.is_integer():
        res = int(res)

    return True, res


def calculate_and_print(expr: str):
    """Evaluate expr and print a user-friendly line like '4+4 = 8'."""
    ok, r = evaluate_expression(expr)
    if not ok:
        print(r)
        return
    # Normalize expression display (remove extra spaces)
    display = re.sub(r'\s+', '', expr)
    print(f"{display} = {r}")


def main():
    print("Simple calculator. Enter expressions like 4+4, or 'exit' to quit.")
    while True:
        s = input('> ').strip()
        if not s:
            continue
        if s.lower() in ('exit', 'quit'):
            print('Goodbye!')
            break
        calculate_and_print(s)


# Global control flags
running = True
paused = False


def _monitor_esc():
    """Background thread: wait for ESC key (global) and then set running=False.

    Uses `keyboard` if available (clean, doesn't eat stdin). Otherwise polls
    `msvcrt.kbhit()` as a fallback (works on Windows consoles).
    """
    global running
    if _keyboard is not None:
        # If the `keyboard` package is available we can register a callback
        # that exits immediately. os._exit is used to ensure the program
        # terminates even if the main thread is blocked on input().
        def _on_esc(e):
            try:
                print('\nESC pressed, exiting...')
            except Exception:
                pass
            # Force immediate exit
            os._exit(0)

        try:
            _keyboard.on_press_key('esc', _on_esc)
            # keep thread alive until program ends
            while running:
                time.sleep(0.2)
        except Exception:
            # if registering fails, fall back to blocking wait
            _keyboard.wait('esc')
            print('\nESC pressed, exiting...')
            os._exit(0)

    # Fallback: poll msvcrt for ESC. Note: this can't interrupt input() on
    # Windows consoles, so the program will only exit after the user presses
    # Enter. Install the 'keyboard' package for immediate ESC termination.
    while running:
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch == '\x1b':
                print('\nESC pressed, exiting...')
                running = False
                return
        time.sleep(0.05)


def main_loop():
    """Main interactive loop supporting 'stop' to pause and ESC to exit."""
    global running, paused
    print("Simple calculator. Enter expressions like 4+4. Type 'stop' to pause; only ESC will exit.")
    while running:
        try:
            s = input('> ').strip()
        except EOFError:
            break
        if not running:
            break
        if not s:
            continue
        key = s.lower()
        if key == 'stop':
            paused = True
            print("Paused. Type anything to resume (program will only exit on ESC).")
            continue
        if paused:
            paused = False
            print('Resumed.')
        # process the expression
        calculate_and_print(s)


if __name__ == '__main__':
    # start monitor thread
    t = threading.Thread(target=_monitor_esc, daemon=True)
    t.start()
    main_loop()
  