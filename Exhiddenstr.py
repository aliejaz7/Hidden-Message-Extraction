import streamlit as st
import wave

def extract_message(audiofile):
    try:
        waveaudio = wave.open(audiofile, mode='rb')
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str, extracted[i:i+8])), 2)) for i in range(0, len(extracted), 8))
        msg = string.split("###")[0]
        waveaudio.close()
        return msg
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit Interface
st.title("Audio Steganography: Secret Message Extractor")
st.write("Upload a WAV file to extract the hidden secret message.")

uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format="audio/wav")
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())
    secret_message = extract_message("temp_audio.wav")
    st.write("### Extracted Secret Message:")
    st.code(secret_message, language='text')
