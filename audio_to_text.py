import base64
import speech_recognition as sr

def base64_to_text(base64_string):
    # Decode base64 to binary
    binary_audio_data = base64.b64decode(base64_string)

    # Save binary audio data to a file (optional)
    with open("audio.wav", "wb") as audio_file:
        audio_file.write(binary_audio_data)

    # Use SpeechRecognition library to convert audio to text
    recognizer = sr.Recognizer()

    with sr.AudioFile("audio.wav") as source:
        audio_data = recognizer.record(source)

    try:
        # Use Google Web Speech API for speech-to-text
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Failed to translate audio"
    except sr.RequestError as e:
        return "Cannot requst Google API"
# Replace 'your_base64_string' with the actual base64-encoded audio string
# base64_string = 'String Base 64'

# result_text = base64_to_text(base64_string)
# print("Result:", result_text)
