from dotenv import load_dotenv

load_dotenv()

import os
from io import BytesIO
import tempfile
from pathlib import Path
import openai
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from ai.agent import run_agent


def ask_ai(prompt):
    history = st.session_state.messages if "messages" in st.session_state else []
    return run_agent(prompt, history)


def text_to_speech(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "temp.mp3"
        response = client.audio.speech.create(model="tts-1", voice="shimmer", input=text)
        response.stream_to_file(temp_path)

        audio_file = open(temp_path, "rb")
        audio_bytes = audio_file.read()
        audio_file.close()
        return audio_bytes


def speech_to_text(audio_bytes):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    audio_bytes_io = BytesIO(audio_bytes["bytes"])
    audio_bytes_io.name = "audio.mp3"

    transcription = client.audio.transcriptions.create(
        model="whisper-1", file=audio_bytes_io, response_format="text"
    )
    return transcription


st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar:
    wav_audio_data = mic_recorder(
        start_prompt="Click to record",
        stop_prompt="Stop recording",
        just_once=True
    )

if prompt := st.chat_input("Enter a message") or wav_audio_data:
    if wav_audio_data:
        prompt = speech_to_text(wav_audio_data)

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ask_ai(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
    audio_bytes = text_to_speech(response)
    st.audio(audio_bytes, format="audio/mpeg", autoplay=True)
