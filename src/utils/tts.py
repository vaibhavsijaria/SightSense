import pyttsx3

def tts(text):
    engine = pyttsx3.init()
    
    voices = engine.getProperty('voices')
    
    engine.setProperty('voice', voices[1].id)

    rate = engine.getProperty('rate')

    engine.setProperty('rate', rate + 50)

    engine.say(text)
    engine.runAndWait()