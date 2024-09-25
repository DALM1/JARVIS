import speech_recognition as sr
import pyttsx3

class SpeechHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def listen_google(self):
        with sr.Microphone() as source:
            print("Je vous écoute...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio, language="fr-FR")
                return text
            except sr.UnknownValueError:
                return "Je n'ai pas compris, pouvez-vous répéter ?"
            except sr.RequestError:
                return "Problème de connexion au service de reconnaissance vocale."

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
