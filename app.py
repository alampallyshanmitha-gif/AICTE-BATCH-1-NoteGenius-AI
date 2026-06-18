import streamlit as st
import os
import json
import sqlite3
from datetime import datetime

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="NoteGenius AI",
    page_icon="🎤",
    layout="wide"
)

# ======================
# IMPORTS
# ======================
from database.db import create_table, save_note, get_notes, delete_note, login_user, register_user

from utils.transcribe import transcribe_audio
from utils.summarize import generate_summary
from utils.quiz_generator import generate_quiz
from utils.flashcards import generate_flashcards
from utils.keywords import extract_keywords
from utils.pdf_export import export_workspace_to_pdf

from components.sidebar import render_sidebar
from components.summary_section import show_summary
from components.quiz_section import show_quiz
from components.flashcards_page import show_flashcards
from components.transcript_section import show_transcript
from components.keyword_section import show_keywords
from components.translate_text import show_translation
from components.chatbot_section import show_chatbot
from components.saved_notes import show_saved_notes
from components.upload_section import show_upload
from components.Analytics_page import show_analytics

# ======================
# INIT SYSTEM
# ======================
create_table()
os.makedirs("uploads/audio_files", exist_ok=True)

# ======================
# SESSION STATE INIT
# ======================
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "Dashboard"

defaults = {
    "transcript": "", 
    "summary": "",
    "quiz": [],
    "flashcards": [],
    "keywords": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ======================
# CSS LOADER
# ======================
def load_css():
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ======================
# CENTER SCREEN AUTHENTICATION (LOGIN & SIGN UP)
# ======================
if st.session_state["user_id"] is None:
    st.empty()
    left_space, center_container, right_space = st.columns([1, 1.4, 1])
    
    with center_container:
        with st.container(border=True):
            st.title("🎓 NoteGenius AI")
            st.caption("Transform Lectures into Smart Study Materials")
            
            mode = st.radio("Choose Option", ["Login", "Sign Up"], horizontal=True)
            st.divider()
            
            email = st.text_input("Email", placeholder="name@example.com")
            password = st.text_input("Password", type="password", placeholder="Enter secure password")
            
            if mode == "Sign Up":
                username = st.text_input("Username", placeholder="Choose your display username")
                
                if st.button("Create Account ✨", use_container_width=True, type="primary"):
                    if username and email and password:
                        success = register_user(username, email, password)
                        if success:
                            st.success("Account created successfully! Now select 'Login' above to continue. 👇")
                        else:
                            st.error("This Email is already registered! ❌")
                    else:
                        st.warning("Please fill in all empty fields.")
            else:
                if st.button("Log In to Dashboard 🚀", use_container_width=True, type="primary"):
                    user = login_user(email, password)
                    if user:
                        st.session_state["user_id"] = user[0]
                        st.session_state["username"] = user[1]
                        st.success(f"Welcome back, {user[1]}!")
                        st.rerun()
                    else:
                        st.error("Invalid email credentials or password entry. ❌")
                        
    st.stop()

# ======================
# RENDER SIDEBAR
# ======================
render_sidebar()

# ======================
# SYSTEM METRICS DATA EXTRACTOR
# ======================
def get_database_metrics(user_id):
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT summary, quiz, flashcards FROM notes WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
    except:
        rows = []
    finally:
        conn.close()

    total_notes = len(rows)
    total_summaries = sum(1 for r in rows if r[0])
    total_quizzes = 0
    total_flashcards = 0

    for row in rows:
        try:
            if row[1]: total_quizzes += len(json.loads(row[1]))
        except: pass
        try:
            if row[2]: total_flashcards += len(json.loads(row[2]))
        except: pass

    return total_notes, total_summaries, total_quizzes, total_flashcards

# ======================
# CORE DASHBOARD INTERFACE
# ======================
if st.session_state["page"] == "Dashboard":
    
    col_header, col_date = st.columns([3, 1])
    current_live_date = datetime.now().strftime("%B %d, %Y")
    
    with col_header:
        st.title(f"Welcome back, {st.session_state['username']}! 👋")
    with col_date:
        st.markdown(f"<p style='text-align: right; padding-top:20px; color:#475569; font-weight:600;'>📅 {current_live_date}</p>", unsafe_allow_html=True)

    top_split_left, top_split_right = st.columns([7, 6])
    
    with top_split_left:
        st.caption("Hero Section")
        st.header("🎤 NoteGenius AI")
        st.markdown("Transform Lectures into Smart Study Materials")
        
        # High-visibility design tags modeled directly from your reference mockup
        tag_cols = st.columns([1.1, 1.3, 1.1, 1.3])
        tag_cols[0].markdown("<div style='background-color:#F3E8FF; color:#6B21A8; border-radius:20px; padding:4px 10px; font-size:11px; font-weight:600; text-align:center; border:1px solid #D8B4FE;'>⚡ AI Powered</div>", unsafe_allow_html=True)
        tag_cols[1].markdown("<div style='background-color:#E0E7FF; color:#3730A3; border-radius:20px; padding:4px 10px; font-size:11px; font-weight:600; text-align:center; border:1px solid #C7D2FE;'>🧠 Smart Learning</div>", unsafe_allow_html=True)
        tag_cols[2].markdown("<div style='background-color:#FCE7F3; color:#9D174D; border-radius:20px; padding:4px 10px; font-size:11px; font-weight:600; text-align:center; border:1px solid #FBCFE8;'>📝 Exam Ready</div>", unsafe_allow_html=True)
        tag_cols[3].markdown("<div style='background-color:#E0F2FE; color:#0369A1; border-radius:20px; padding:4px 10px; font-size:11px; font-weight:600; text-align:center; border:1px solid #BAE6FD;'>🌐 Multi-Language</div>", unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        notes, summaries, quizzes, flashcards = get_database_metrics(st.session_state["user_id"])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Notes", notes)
        m2.metric("Total Summaries", summaries)
        m3.metric("Total Quizzes", quizzes)
        m4.metric("Total Flashcards", flashcards)

    with top_split_right:
        st.subheader("Current Transcript")
        with st.container(border=True):
            col_card_title, col_card_actions = st.columns([1.6, 2])
            
            with col_card_title:
                st.markdown("**Lecture Workspace Data**")
            
            with col_card_actions:
                tr_btn1, tr_btn2 = st.columns(2)
                
                if tr_btn1.button("📋 Copy", key="main_cp_tr", use_container_width=True):
                    if st.session_state["transcript"]:
                        st.components.v1.html(f"""
                            <script>
                                navigator.clipboard.writeText(`{st.session_state["transcript"]}`);
                            </script>
                        """, height=0)
                        st.toast("Copied to clipboard! 📋")
                    else:
                        st.warning("Nothing to copy yet!")
                
                if st.session_state["transcript"]:
                    tr_btn2.download_button(
                        label="📥 Download",
                        data=st.session_state["transcript"],
                        file_name="Lecture_Transcript.txt",
                        mime="text/plain",
                        key="main_dl_tr_working",
                        use_container_width=True
                    )
                else:
                    tr_btn2.button("📥 Download", key="main_dl_tr_disabled", disabled=True, use_container_width=True)

            if st.session_state["transcript"]:
                edited_tr = st.text_area("Transcript Output Window", st.session_state["transcript"], height=140, label_visibility="collapsed")
                st.session_state["transcript"] = edited_tr
                
                word_count = len(st.session_state["transcript"].split())
                st.caption(f"✏️ Editable | {word_count:,} words")
            else:
                st.info("No text recorded yet. Upload a lecture audio track below to populate workspace data.")
            
            if st.session_state["transcript"]:
                if st.button("💾 Save to History Archive Gallery", key="main_save_note", use_container_width=True, type="primary"):
                    save_note(st.session_state["user_id"], st.session_state["transcript"], st.session_state["summary"], st.session_state["quiz"], st.session_state["flashcards"], st.session_state["keywords"])
                    st.success("Note structured and saved cleanly to your profile history!")
                    st.rerun()

    st.divider()

    mid_split_left, mid_split_right = st.columns([7, 6])

    with mid_split_left:
        st.subheader("Upload Lecture Audio")
        with st.container(border=True):
            uploaded_file = st.file_uploader("Upload Audio Box Panel", type=["mp3", "wav", "m4a"], label_visibility="collapsed")
            if uploaded_file:
                file_path = os.path.join("uploads/audio_files", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.audio(file_path)
                
            if st.button("Start Transcription", use_container_width=True, type="secondary"):
                if uploaded_file:
                    with st.spinner("Processing speech tracks..."):
                        st.session_state["transcript"] = transcribe_audio(file_path)
                    st.rerun()
                else:
                    st.warning("Please attach an audio track first.")

    with mid_split_right:
        st.subheader("AI Generation Tools")
        g_row1_c1, g_row1_c2, g_row1_c3 = st.columns(3)
        g_row2_c1, g_row2_c2, g_row2_c3 = st.columns(3)
        
        with g_row1_c1:
            with st.container(border=True):
                st.markdown("**Summary**")
                if st.button("Action Now", key="dash_sum_btn", use_container_width=True):
                    if st.session_state["transcript"]: st.session_state["summary"] = generate_summary(st.session_state["transcript"])
                    st.session_state["page"] = "Summary"; st.rerun()

        with g_row1_c2:
            with st.container(border=True):
                st.markdown("**Quiz**")
                if st.button("Action Now", key="dash_qz_btn", use_container_width=True):
                    if st.session_state["transcript"]: st.session_state["quiz"] = generate_quiz(st.session_state["transcript"])
                    st.session_state["page"] = "Quiz"; st.rerun()

        with g_row1_c3:
            with st.container(border=True):
                st.markdown("**Flashcards**")
                if st.button("Action Now", key="dash_fc_btn", use_container_width=True):
                    if st.session_state["transcript"]: st.session_state["flashcards"] = generate_flashcards(st.session_state["transcript"])
                    st.session_state["page"] = "Flashcards"; st.rerun()

        with g_row2_c1:
            with st.container(border=True):
                st.markdown("**Keywords**")
                if st.button("Action Now", key="dash_kw_btn", use_container_width=True):
                    if st.session_state["transcript"]: st.session_state["keywords"] = extract_keywords(st.session_state["transcript"])
                    st.session_state["page"] = "Keywords"; st.rerun()

        with g_row2_c2:
            with st.container(border=True):
                st.markdown("**Translate**")
                if st.button("Action Now", key="dash_tl_btn", use_container_width=True):
                    st.session_state["page"] = "Translation"; st.rerun()

        with g_row2_c3:
            with st.container(border=True):
                st.markdown("**Export PDF**")
                try:
                    pdf_bytes = export_workspace_to_pdf(st.session_state["transcript"], st.session_state["quiz"], st.session_state["flashcards"], st.session_state["keywords"])
                    st.download_button(label="Download PDF", data=pdf_bytes, file_name="NoteGenius_Export.pdf", mime="application/pdf", use_container_width=True)
                except Exception:
                    st.error("Verify fpdf2 package installation setup dependencies.")

    st.write("<br>", unsafe_allow_html=True)
    st.subheader("📂 Profile Archived Notes Gallery")
    db_notes = get_notes(st.session_state["user_id"])
    
    if not db_notes:
        st.info("No historical notes logged under this profile session index.")
    else:
        gallery_columns = st.columns(3)
        for i, entry in enumerate(db_notes):
            with gallery_columns[i % 3]:
                with st.container(border=True):
                    st.markdown(f"#### Note Entry #{entry[0]}")
                    with st.expander("Transcript Details"): st.write(entry[1])
                    if st.button(f"🗑️ Wipe Record #{entry[0]}", key=f"db_del_{entry[0]}", use_container_width=True):
                        delete_note(entry[0]); st.rerun()

# ======================
# NAVIGATION ROUTER PATHS
# ======================
elif st.session_state.page == "Upload": show_upload()
elif st.session_state.page == "Summary": show_summary()
elif st.session_state.page == "Quiz": show_quiz()
elif st.session_state.page == "Flashcards": show_flashcards()
elif st.session_state.page == "Transcript": show_transcript()
elif st.session_state.page == "Keywords": show_keywords()
elif st.session_state.page == "Translation": show_translation()
elif st.session_state.page == "Chatbot": show_chatbot()
elif st.session_state.page == "Saved Notes": show_saved_notes()
elif st.session_state.page == "Analytics": show_analytics()