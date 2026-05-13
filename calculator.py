def Calculation(First, Second):
    what_do = input("""What do you want to do?
    If it is division, type: divided
    If it is multiplication, type: multiple
    If it is addition, type: add 
    If it is substraction, type: subs\n""").lower()

    if what_do == "divided":
        if Second == 0:
            print("Error: Division by zero is not allowed.")
            return

        result = First / Second
        if result.is_integer():
            print(f"Your division result is: {int(result)}")
        else:
            result_1 = First // Second
            remainder = First % Second
            print(f"""Your division is: {result_1} 
            with a remainder of {remainder}""")

    elif what_do == "multiple":
        result = First * Second
        print(f"Multiplication result: {result}")
        
    elif what_do == "add":
        result = (First + Second)
        print(f"Multiplication result: {result}")
        
    elif what_do == "subs":
        result = (First - Second)
        print(f"Multiplication result: {result}")


    else:
        print("Invalid input. Please type 'divided' or 'multiple'.")

if __name__ == "__main__":
    First = int(input("Enter your first number: "))
    Second = int(input("Enter your second number: "))
    Calculation(First, Second)