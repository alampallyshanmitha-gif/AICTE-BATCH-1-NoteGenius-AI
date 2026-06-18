# components/sidebar.py
import streamlit as st

def render_sidebar():
    with st.sidebar:
        # App Branding Header
        st.markdown("# 🎓 NoteGenius AI")
        st.markdown("---")

        # User Info Profile Card
        st.success(f"👤 Active Profile: {st.session_state.get('username', 'User')}")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["user_id"] = None
            st.session_state["username"] = None
            st.session_state["page"] = "Dashboard"
            st.rerun()

        st.markdown("---")
        st.markdown("### 🧭 Workspace Navigation")

        # ======================
        # NAVIGATION BUTTONS
        # ======================
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state["page"] = "Dashboard"
            st.rerun()

        if st.button("🎤 Upload Audio", use_container_width=True):
            st.session_state["page"] = "Upload"
            st.rerun()

        if st.button("📄 Transcript", use_container_width=True):
            st.session_state["page"] = "Transcript"
            st.rerun()

        if st.button("📝 Summary", use_container_width=True):
            st.session_state["page"] = "Summary"
            st.rerun()

        if st.button("❓ Quiz", use_container_width=True):
            st.session_state["page"] = "Quiz"
            st.rerun()

        if st.button("🧠 Flashcards", use_container_width=True):
            st.session_state["page"] = "Flashcards"
            st.rerun()

        if st.button("🔑 Keywords", use_container_width=True):
            st.session_state["page"] = "Keywords"
            st.rerun()

        if st.button("🌍 Translation", use_container_width=True):
            st.session_state["page"] = "Translation"
            st.rerun()

        if st.button("🤖 AI Chatbot", use_container_width=True):
            st.session_state["page"] = "Chatbot"
            st.rerun()

        if st.button("📊 Analytics", use_container_width=True):
            st.session_state["page"] = "Analytics"
            st.rerun()

        if st.button("💾 Saved Notes", use_container_width=True):
            st.session_state["page"] = "Saved Notes"
            st.rerun()