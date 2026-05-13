import keyboard
import time

responses = {
    "hello": "hi",
    "how are you": "I am fine",
    "bye": "goodbye"
}

current_word = ""

print("Script running... Type anywhere!")

while True:
    event = keyboard.read_event(suppress=False)
    if event.event_type == keyboard.KEY_DOWN:
        if event.name in ["space", "enter"]:  # word ended
            word = current_word.strip()
            if word in responses:
                # erase the original word
                for _ in range(len(word)):
                    keyboard.press_and_release('backspace')
                # type the replacement
                keyboard.write(responses[word])
            current_word = ""  # reset after replacement

            # retype space or enter
            if event.name == "space":
                keyboard.write(" ")
            else:
                keyboard.write("\n")

        elif len(event.name) == 1:  # normal letters
            current_word += event.name
        elif event.name == "backspace":
            current_word = current_word[:-1]

    time.sleep(0.01)

    if keyboard.is_pressed('esc'):  # exit on 'esc' key
        print("Exiting...")
        break
