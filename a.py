import streamlit as st
import time
import os
import io
import base64
import speech_recognition as sr
from cryptography.fernet import Fernet
from langdetect import detect
from gtts import gTTS

# --- 1. SYSTEM CONFIGURATION & STYLING ---
st.set_page_config(page_title="Secure Voice Intelligence", page_icon="🎙️")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stAudioInput { border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .status-card {
        padding: 20px; border-radius: 15px; background: white;
        border-left: 5px solid #3b82f6; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .badge {
        background: #dcfce7; color: #166534; padding: 4px 12px;
        border-radius: 10px; font-weight: bold; font-size: 0.7rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND LOGIC (Your Functions) ---
DEPARTMENT_ROUTING = {
    "water_management": {"number": "1800-WATER-01", "name": "Water Services"},
    "soil_management": {"number": "1800-SOIL-02", "name": "Agricultural Dept"},
    "billing": {"number": "1800-BILL-03", "name": "Accounts"},
    "technical_support": {"number": "1800-TECH-04", "name": "IT Support"}
}

def classify_and_route(text):
    text = text.lower()
    if any(k in text for k in ["water", "paani"]): return "water_management"
    if any(k in text for k in ["soil", "mitti"]): return "soil_management"
    if any(k in text for k in ["bill", "payment"]): return "billing"
    if any(k in text for k in ["tech", "support"]): return "technical_support"
    return "unknown"

def initialize_system():
    if not os.path.exists("secret.key"):
        with open("secret.key", "wb") as f: f.write(Fernet.generate_key())

def encrypt_complaint(plain_text):
    cipher = Fernet(open("secret.key", "rb").read())
    return cipher.encrypt(plain_text.encode())

def decrypt_complaint(enc_text):
    cipher = Fernet(open("secret.key", "rb").read())
    return cipher.decrypt(enc_text).decode()

def play_response(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    st.audio(fp.getvalue(), format="audio/mp3", autoplay=True)

# --- 3. UI LAYOUT ---
st.title("🎙️ VAANI AI")
st.write("Secure Complaint Management & Routing System")
initialize_system()

# Replacing old recording method with stable Streamlit Audio Input
audio_file = st.audio_input("Record your complaint")

if audio_file:
    # A. TRANSCRIPTION
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = r.record(source)
    
    try:
        complaint = r.recognize_google(audio_data)
        lang = detect(complaint)
        
        # B. ANALYZING PHASE (100% Progress)
        st.write("---")
        st.markdown(f'<p class="badge">DETECTED: {lang.upper()}</p>', unsafe_allow_html=True)
        bar = st.progress(0, text="Neural Analysis in progress...")
        for i in range(101):
            time.sleep(0.01)
            bar.progress(i)
        
        # C. ROUTING & SECURITY
        st.markdown('<div class="status-card">', unsafe_allow_html=True)
        st.subheader("Analysis Results")
        st.write(f"**Transcript:** {complaint}")
        
        route_msg = ""
        category = classify_and_route(complaint)
        if category in DEPARTMENT_ROUTING:
            dept = DEPARTMENT_ROUTING[category]
            route_msg = f"Routing you to {dept['name']} at {dept['number']}."
            st.success(route_msg)
        else:
            route_msg = "Routing you to a general representative."
            st.warning(route_msg)
        
        # D. ENCRYPTION DISPLAY
        enc = encrypt_complaint(complaint)
        st.write("**Encrypted Data (Secure Storage):**")
        st.code(enc.decode())
        
        st.markdown('</div>', unsafe_allow_html=True)

        # E. VOICE RESPONSE
        full_voice_resp = f"Analysis complete. {route_msg}"
        play_response(full_voice_resp)

    except Exception as e:
        st.error(f"Speech analysis failed: {e}")

else:
    st.info("Click the record button above to begin your secure session.")