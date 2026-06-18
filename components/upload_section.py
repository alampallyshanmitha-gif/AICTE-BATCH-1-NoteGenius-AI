import streamlit as st
import os
from utils.transcribe import transcribe_audio

def show_upload():

    st.title("🎤 Upload Lecture Audio")

    os.makedirs("uploads/audio_files", exist_ok=True)

    uploaded_file = st.file_uploader(
        "Choose Audio File",
        type=["wav", "mp3", "m4a"]
    )

    if uploaded_file is not None:

        file_path = os.path.join(
            "uploads/audio_files",
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Audio uploaded successfully")

        st.audio(file_path)

        if st.button("Convert Speech To Text"):

            with st.spinner("Transcribing..."):

                transcript = transcribe_audio(file_path)

                st.session_state["transcript"] = transcript

            st.success("Transcript generated")

            st.text_area(
                "Transcript",
                transcript,
                height=300
            )