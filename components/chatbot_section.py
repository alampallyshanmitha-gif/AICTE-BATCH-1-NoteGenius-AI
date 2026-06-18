import streamlit as st
from utils.chatbot import ask_question


def show_chatbot():

    st.title("🤖 AI Study Chatbot")

    st.markdown(
        "Ask questions about your uploaded lecture, transcript, or notes."
    )

    # Check transcript exists
    if "transcript" not in st.session_state:

        st.warning(
            "Please upload and transcribe a lecture first."
        )

        return

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat Input
    prompt = st.chat_input(
        "Ask something about your lecture..."
    )

    if prompt:

        # User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        # AI Response
        with st.spinner("Thinking..."):

            answer = ask_question(
                st.session_state["transcript"],
                prompt
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)

    st.divider()

    st.subheader("💡 Example Questions")

    st.info("What is the main topic of this lecture?")

    st.info("Summarize this lecture in simple words.")

    st.info("Give me important exam questions.")

    st.info("Explain the difficult concepts.")