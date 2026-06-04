import pyttsx3
import time



engine = pyttsx3.init()

while True:
    text = input("You: ").lower()

    if "hello" in text:
        engine.say("Hello Sani")
        engine.runAndWait()

    elif "your name" in text:
        time.sleep(2)
        s = engine.say(
            "I am your personal assistant"
        )
        
        engine.runAndWait()
        

    elif "exit" in text:
        break