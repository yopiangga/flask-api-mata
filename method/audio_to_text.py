import base64
import speech_recognition as sr
import config.app as config

def base64_to_text(base64_string):
    binary_audio_data = base64.b64decode(base64_string)

    with open(config.path + "temp/audio.wav", "wb") as audio_file:
        audio_file.write(binary_audio_data)

    recognizer = sr.Recognizer()

    with sr.AudioFile(config.path + "temp/audio.wav") as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Failed to translate audio"
    except sr.RequestError as e:
        return "Cannot requst Google API"
