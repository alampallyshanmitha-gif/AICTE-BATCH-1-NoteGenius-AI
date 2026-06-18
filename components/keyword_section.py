import streamlit as st

def show_keywords():

    st.title("🔑 Important Keywords")

    if "keywords" not in st.session_state:
        st.warning("No keywords extracted yet.")
        return

    cols = st.columns(4)

    for i, keyword in enumerate(st.session_state["keywords"]):

        cols[i % 4].success(keyword)