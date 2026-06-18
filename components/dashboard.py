import streamlit as st
import json
from database.db import get_notes

def show_dashboard():

    notes = get_notes()

    total_notes = len(notes)
    total_summaries = 0
    total_quizzes = 0
    total_flashcards = 0

    for note in notes:

        # Summary exists
        if note[2]:
            total_summaries += 1

        # Quiz count
        try:
            quiz = json.loads(note[3])
            total_quizzes += len(quiz)
        except:
            pass

        # Flashcard count
        try:
            flashcards = json.loads(note[4])
            total_flashcards += len(flashcards)
        except:
            pass

    st.markdown("## 👋 Welcome Back")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Notes", total_notes)
    c2.metric("Summaries", total_summaries)
    c3.metric("Quiz Questions", total_quizzes)
    c4.metric("Flashcards", total_flashcards)

    st.markdown("---")

    left, right = st.columns([1.2, 1])

    with left:

        st.markdown("### 🎤 Upload Lecture Audio")

        uploaded_file = st.file_uploader(
            "Upload Audio",
            type=["wav", "mp3", "m4a"]
        )

        if uploaded_file:
            st.success(uploaded_file.name)

        if st.button("Start Transcription"):
            st.session_state.page = "Transcript"

    with right:

        st.markdown("### 📄 Current Transcript")

        if notes:

            latest_note = notes[-1]

            st.text_area(
                "",
                latest_note[1],  # transcript
                height=250
            )

        else:

            st.text_area(
                "",
                "No transcript available",
                height=250
            )