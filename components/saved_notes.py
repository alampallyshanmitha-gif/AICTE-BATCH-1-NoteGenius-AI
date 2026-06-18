import streamlit as st
import json

from database.db import (
    get_notes,
    delete_note
)

def show_saved_notes():

    st.title("💾 Saved Notes")

    # ======================
    # GET LOGGED IN USER
    # ======================
    user_id = st.session_state.get("user_id")

    if not user_id:
        st.warning("🔐 Please login to view your saved notes.")
        return

    # ======================
    # FETCH ONLY USER NOTES
    # ======================
    notes = get_notes(user_id)

    if not notes:
        st.info("No saved notes found.")
        return

    # ======================
    # DISPLAY NOTES
    # ======================
    for note in notes:

        with st.expander(f"📌 Note {note[0]} | {note[6]}"):

            # Transcript
            st.write("### 📝 Transcript")
            st.write(note[1])

            # Summary
            st.write("### 📄 Summary")
            st.write(note[2])

            # Quiz
            st.write("### ❓ Quiz")
            try:
                st.write(json.loads(note[3]) if note[3] else [])
            except:
                st.write("No quiz data")

            # Flashcards
            st.write("### 🧠 Flashcards")
            try:
                st.write(json.loads(note[4]) if note[4] else [])
            except:
                st.write("No flashcards")

            # Keywords
            st.write("### 🔑 Keywords")
            try:
                st.write(json.loads(note[5]) if note[5] else [])
            except:
                st.write("No keywords")

            # ======================
            # DELETE BUTTON
            # ======================
            if st.button(
                f"🗑️ Delete Note {note[0]}",
                key=f"del_{note[0]}"
            ):
                delete_note(note[0])
                st.success("Deleted successfully!")
                st.rerun()