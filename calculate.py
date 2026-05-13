HISTORY_FILE = "history1.txt"

def show_history():
    file = open(HISTORY_FILE, 'r')
    lines = file.readlines()
    if len(lines) == 0:
        print("No History Found!!!")
    else:
        for line in reversed(lines):
            print(line.strip()) 
    file.close()

def clear_history():
    file = open(HISTORY_FILE, 'w')
    file.close()
    print("History is cleared!")

def save_to_history(equation, result):
    file = open(HISTORY_FILE, 'a')
    file.write(equation + " = " + str(result) + "\n")
    file.close()

def calculation(user_input):
    parts = user_input.split()
    if len(parts) != 3:
        print("Invalid input. Please enter like: 8+8 or 8 + 8")
        return
    num1 = float(parts[0])
    op = parts[1]
    num2 = float(parts[2])
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
    if int(result) == result:
        result = int(result)
    print("Result : " + str(result))
    save_to_history(user_input, result)

def main():
    print("Welcome to the Calculator!")
    print("Type 'history' to view calculation history.")
    print("Type 'clear' to clear calculation history.") 
    while True:
        user_input = input("Enter calculation (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting the calculator. Goodbye!")
            break
        elif user_input.lower() == 'history':
            show_history()
        elif user_input.lower() == 'clear':
            clear_history()
        else:
            calculation(user_input)

if __name__ == "__main__":
    main()
    