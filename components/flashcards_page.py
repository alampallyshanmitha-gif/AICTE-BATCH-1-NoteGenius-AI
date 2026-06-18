import streamlit as st

def show_flashcards():
    st.markdown("## 🎴 Dynamic Study Flashcards")
    
    if "flashcards" not in st.session_state or not st.session_state["flashcards"]:
        st.warning("Please generate flashcards from your dashboard using a lecture transcript first.")
        return

    cards = st.session_state["flashcards"]

    st.markdown(f"📦 **Active Deck:** {len(cards)} Conceptual Review Cards")
    st.write("Read the specialized question on the front, formulate your answer, and click flip to check.")
    st.write("---")

    # Cycle through generated payload sets cleanly
    for card in cards:
        card_id = card["id"]
        flip_key = f"flipped_card_{card_id}"
        
        if flip_key not in st.session_state:
            st.session_state[flip_key] = False

        # Premium Card Front Layout Design System
        st.markdown(f"""
            <div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 24px; border-radius: 14px; margin-bottom: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                    <span style='font-size: 11px; text-transform: uppercase; color: #4F46E5; font-weight: 700; letter-spacing: 0.05em;'>Flashcard {card_id}</span>
                    <span style='font-size: 12px; color: #64748B;'>🧠 Active Recall</span>
                </div>
                <p style='font-size: 16px; font-weight: 600; color: #0F172A; line-height: 1.5; margin: 0;'>{card['question']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Bottom interaction row columns
        col1, col2 = st.columns([1, 4])
        
        with col1:
            if st.button("🔄 Flip Card", key=f"btn_flip_{card_id}", use_container_width=True):
                st.session_state[flip_key] = not st.session_state[flip_key]
                st.rerun()

        with col2:
            if st.session_state[flip_key]:
                st.markdown(f"""
                    <div style='background-color: #F0FDF4; border-left: 4px solid #16A34A; padding: 12px 18px; border-radius: 8px;'>
                        <strong style='color: #15803D; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em;'>Verified Lecture Answer:</strong>
                        <p style='color: #1E293B; margin-top: 6px; margin-bottom: 0; font-size: 14.5px; line-height: 1.5;'>{card['answer']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: #94A3B8; font-style: italic; font-size: 13px; margin-top: 10px; margin-left: 6px;'>🔒 Click the action button to show back payload answer details...</p>", unsafe_allow_html=True)
        
        st.write("---")