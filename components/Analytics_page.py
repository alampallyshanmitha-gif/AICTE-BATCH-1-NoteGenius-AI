import streamlit as st
from database.db import get_notes
import json

def show_analytics():

    st.title("📊 Analytics Dashboard")

    # ✅ GET USER ID (VERY IMPORTANT)
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("Please login first to view analytics.")
        return

    # ✅ FIXED CALL
    notes = get_notes(user_id)

    total_notes = len(notes)

    total_summaries = 0
    total_quizzes = 0
    total_flashcards = 0
    total_keywords = 0

    for note in notes:

        # Summary
        if note[2]:
            total_summaries += 1

        # Quiz
        try:
            quiz = json.loads(note[3])
            total_quizzes += len(quiz)
        except:
            pass

        # Flashcards
        try:
            flashcards = json.loads(note[4])
            total_flashcards += len(flashcards)
        except:
            pass

        # Keywords
        try:
            keywords = json.loads(note[5])
            total_keywords += len(keywords)
        except:
            pass

    # ======================
    # METRICS UI
    # ======================
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📝 Total Notes", total_notes)
    c2.metric("📄 Summaries", total_summaries)
    c3.metric("❓ Quiz Questions", total_quizzes)
    c4.metric("🧠 Flashcards", total_flashcards)

    st.divider()

    # ======================
    # STATS
    # ======================
    st.subheader("📈 Content Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Total Keywords Extracted: {total_keywords}")
        st.info(f"Saved Notes: {total_notes}")

    with col2:
        st.success(f"Generated Summaries: {total_summaries}")
        st.success(f"Generated Flashcards: {total_flashcards}")

    st.divider()

    # ======================
    # RECENT ACTIVITY
    # ======================
    st.subheader("📂 Recent Activity")

    if not notes:
        st.warning("No data available.")
        return

    latest = notes[-5:]

    for note in reversed(latest):
        st.markdown(f"""
        **Note ID:** {note[0]}  
        **Created:** {note[6]}
        """)