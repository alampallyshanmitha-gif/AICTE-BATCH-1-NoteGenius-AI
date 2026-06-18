import streamlit as st

def show_transcript():

    st.title("📄 Transcript")

    if "transcript" not in st.session_state:
        st.warning("No transcript available.")
        return

    st.text_area(
        "Transcript",
        st.session_state["transcript"],
        height=500
    )