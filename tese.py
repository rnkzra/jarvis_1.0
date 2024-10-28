import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
#https://ai.google.dev/api?hl=pt-br&lang=python

genai.configure(api_key="AIzaSyAeIyxBnLT83maf-1x8PH3Q1o7tp0F3N8Y")
lang = 'pt-br'
model = genai.GenerativeModel("gemini-1.5-flash")


# Inicializa a engine de text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio, language=lang)
        except:
            print("Speech not recognized")

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    model.generate_content("Aja como se você fosse o Jarvis do Homem de Ferro, e eu o Homem de Ferro")
    jarvis_activated = False
    while True:
        if not jarvis_activated:
            print("Diga JARVIS para ativar...")
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                audio = recognizer.listen(source)
                try:
                    transcription = recognizer.recognize_google(audio, language=lang)
                    if transcription.lower() == "jarvis":
                        jarvis_activated = True
                        print("JARVIS ativado! Pergunte algo...")
                except Exception as e:
                    print("Ocorreu um erro: {}".format(e))
                    continue

        else:
            filename = "input.wav"
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

            text = transcribe_audio_to_text(filename)

            if text:
                response = model.generate_content(text)
                response_content = response.text
                print(f"Gemini: {response_content}")
                speak_text(response_content)

if __name__ == "__main__":
    main()
