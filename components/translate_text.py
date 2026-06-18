import streamlit as st
from utils.translate import translate_text

def show_translation():
    st.markdown("## 🌍 Premium Translation Desk")

    if "summary" not in st.session_state or not st.session_state["summary"]:
        st.warning("⚠️ Generate an AI summary from your lecture workspace first.")
        return

    # User Selectbox Input
    language = st.selectbox(
        "Select Target Language",
        [
            "English", "Telugu", "Hindi", "Tamil", "Kannada", 
            "Malayalam", "Marathi", "Gujarati", "Punjabi", 
            "Bengali", "Urdu", "French", "Spanish", "German"
        ]
    )

    # Trigger translation execution
    if st.button("Translate Notes Now", use_container_width=True):
        with st.spinner(f"Processing translation into {language}..."):
            translated = translate_text(
                st.session_state["summary"],
                language
            )
            # Store the single resulting string output back into session state memory
            st.session_state["translated_summary"] = translated
            st.rerun()

    # Dynamic Render Block for Results
    if "translated_summary" in st.session_state and st.session_state["translated_summary"]:
        st.write("---")
        st.markdown(f"### 📋 Translated Summary Output ({language})")
        
        # Display beautifully inside a premium presentation container card
        st.markdown(f"""
            <div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 22px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);'>
                <p style='color: #1E293B; line-height: 1.6; font-size: 15px; margin: 0;'>
                    {st.session_state["translated_summary"]}
                </p>
            </div>
        """, unsafe_allow_html=True)