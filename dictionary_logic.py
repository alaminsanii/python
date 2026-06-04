import colorama as c
import os
import json

birthday = {
    "gates": "july 10",
    "alice": "aug 15",
    "bob": "june 13"
}


if os.path.exists("birthday/file.txt"):
    with open("birthday/file.txt", "r") as f:
        content = f.read()

        if content:  # if file not empty
            birthday = eval(content)


while True:
    name = input("enter blank to out> ").lower()

    if name == "":
        print("you r exiting.")
        break
# print(c.Back.GREEN + f"{name} birthday is {birthday[name]}" + c.Style.RESET_ALL)
    elif name in birthday:
        c.init(autoreset= True)
        print(c.Back.GREEN + f"{name} birthday is {birthday[name]}")
        c.Style.RESET_ALL

    else:
        print('I do not have birthday information for ' + name)
        print('What is their birthday?')

        bday = input()
        birthday[name] = bday

        print('Birthday database updated.')

        # create folder
        os.makedirs("birthday", exist_ok=True)

        # save file inside birthday folder
        with open("birthday/file.txt", "w") as f:
            f.write(str(birthday))
        print("your list has been saved") 

