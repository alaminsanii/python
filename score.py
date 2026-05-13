import random
import os

def game():
    print("You are playing the game.")
    score = random.randint(1, 65)

    # Check if file exists
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            content = f.read().strip()

    else:
        highscore = 0

    print("Your score is:", score)

    if score > highscore:
        with open("highscore.txt", "w") as f:
            f.write(str(score))  # ✅ correct
        print("New high score!")

    return score

game()