import random, time, sys
import colorama as c
# c.init()


width = 150
try:
    column = [0] * width
    while True:
        for i in range(width):
            if random.random() < 0.02:
                column[i] = random.randint(1,16)
            if column[i] == 0:
                print(' ', end= '')
            else:
                print(c.Fore.GREEN , random.choice([0,1]), end = '')
                column[i] -= 1
        print()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("You are exiting from the code")
    sys.exit()

