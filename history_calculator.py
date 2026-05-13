import re

HISTORY_FILE = "highscore.txt"


def show_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("No History Found!!!")
        return
    if not lines:
        print("No History Found!!!")
    else:
        for line in reversed(lines):
            print(line.strip())


def clear_history():
    # Truncate (or create) the history file
    open(HISTORY_FILE, 'w').close()
    print("History is cleared!")


def save_to_history(equation, result):
    with open(HISTORY_FILE, 'a') as file:
        file.write(f"{equation} = {result}\n")


def calculation(user_input):
    """Parse expressions like '8+8' or '8 + 8' and compute result."""
    user_input = user_input.strip()
    # Accept integers/floats with optional sign, with or without spaces
    pattern = r'^\s*([+-]?\d+(?:\.\d+)?)\s*([+\-*/])\s*([+-]?\d+(?:\.\d+)?)\s*$'
    m = re.match(pattern, user_input)
    if not m:
        print("Invalid input. Please enter like: 8+8 or 8 + 8")
        return
    num1_s, op, num2_s = m.groups()
    num1 = float(num1_s)
    num2 = float(num2_s)

    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op == "/":
        if num2 == 0:
            print("You cannot divide by zero.")
            return
        result = num1 / num2
    else:
        print("Invalid operator please choose (+ - * / )!")
        return

    # Normalize integer-valued floats to int for nicer output
    if int(result) == result:
        result = int(result)

    print("Result : " + str(result))
    equation_str = f"{num1} {op} {num2}"
    save_to_history(equation_str, result)


def main():
    print("--Simple History Calculator--")
    while True:
        user_input = input("Enter calculation(+,-,*,/) or command (history, clear, exit): ").strip()
        if user_input.lower() == "exit":
            print("Good bye!")
            break
        elif user_input.lower() == "history":
            show_history()
        elif user_input.lower() == "clear":
            clear_history()
        else:
            calculation(user_input)


if __name__ == "__main__":
    main()


                                         