import speech_recognition as sr
from cryptography.fernet import Fernet
import os

# --- 1. KEY MANAGEMENT ---
def initialize_system():
    """Checks for a key; if none exists, creates one."""
    if not os.path.exists("secret.key"):
        print(" No key found. Generating new master key...")
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        print("Master key loaded.")

def load_key():
    """Reads the key from the secret.key file."""
    return open("secret.key", "rb").read()

# --- 2. ENCRYPTION & DECRYPTION LOGIC ---
def encrypt_complaint(plain_text):
    """Encrypts the text on the IVR side."""
    key = load_key()
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(plain_text.encode())
    return encrypted_text

def decrypt_complaint(encrypted_text):
    """Decrypts the text on the Officer side."""
    key = load_key()
    cipher_suite = Fernet(key)
    decrypted_bytes = cipher_suite.decrypt(encrypted_text)
    return decrypted_bytes.decode()

def process_complaint(complaint):
    # Example processing: return the complaint in uppercase
    return complaint.upper()

if __name__ == "__main__":
    initialize_system()
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Say something...")
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start.")
                exit(1)
        try:
            # Recognize speech using Google Web Speech API
            original_complaint = r.recognize_google(audio)
            print(f"\n[USER SAYS]: {original_complaint}")

            # Step A: Encrypting (This goes to the database/server)
            encrypted_data = encrypt_complaint(original_complaint)
            print(f"[ENCRYPTED]: {encrypted_data}")

            # Step B: Decrypting (This happens at the Officer's Desk)
            decrypted_data = decrypt_complaint(encrypted_data)
            print(f"[OFFICER READS]: {decrypted_data}")

            # Process the decrypted complaint
            processed = process_complaint(decrypted_data)
            print(f"[PROCESSED]: {processed}")

            if original_complaint == decrypted_data:
                print("\n TEST PASSED: Data is secure and accurate!")
        except sr.UnknownValueError:
            print("Sorry, could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    except AttributeError:
        print("PyAudio is not installed. Please install it with 'pip install pyaudio'.")
    except OSError:
        print("Microphone not found or not accessible.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
