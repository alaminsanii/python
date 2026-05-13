import random

def game():
    print("You are playing the game.")
    score = random.randint(1, 65)

    # Read file if exists, else default
    try:
        with open("highscore.txt", "r") as f:
            content = f.read().strip()
            highscore = int(content) if content else 0
    except FileNotFoundError:
        highscore = 0

    print("Your score is:", score)

    # Write file (creates if not exists, like ex-1)
    if score > highscore:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
        print("New high score!")

    return score

game()