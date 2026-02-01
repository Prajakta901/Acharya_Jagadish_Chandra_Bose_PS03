import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Say something...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        # Recognize speech using Google Web Speech API
        text = r.recognize_google(audio)
        print("You said:", text)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
except AttributeError:
    print("PyAudio is not installed. Please install it with 'pip install pyaudio'.")
except OSError:
    print("Microphone not found or not accessible.")
except sr.WaitTimeoutError:
    print("Listening timed out while waiting for phrase to start.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
