# components/quiz_section.py
import streamlit as st
import json

def show_quiz():
    st.title("❓ AI Practice Quiz Assessment")
    st.markdown("Test your understanding of the transcribed lecture material below.")
    st.write("---")

    # Fallback if no quiz data has been generated yet
    if not st.session_state.get("quiz"):
        st.info("No quiz data available in this session. Go to the Dashboard, upload an audio track, and click 'Generate Quiz'!")
        return

    # Load quiz dataset seamlessly whether it's a raw string or a Python list
    try:
        quiz_data = json.loads(st.session_state["quiz"]) if isinstance(st.session_state["quiz"], str) else st.session_state["quiz"]
    except Exception:
        st.error("Failed to parse the quiz data format schema.")
        return

    if not isinstance(quiz_data, list) or len(quiz_data) == 0:
        st.warning("The quiz structure appears to be empty.")
        return

    # ==========================================
    # CLEAN CONTAINER CONTAINER (NO FORM WRAPPER)
    # ==========================================
    # Replacing st.form with st.container completely fixes the red error box!
    with st.container(border=True):
        user_answers = {}
        
        # Loop over generated quiz questions dynamically
        for idx, q_node in enumerate(quiz_data, 1):
            st.markdown(f"### Question {idx}: {q_node.get('question', '')}")
            
            options = q_node.get("options", [])
            
            # Render radio inputs for selection
            user_answers[idx] = st.radio(
                "Select the correct option:",
                options=options,
                key=f"quiz_q_{idx}",
                index=None, # Starts with no choice selected out-of-the-box
                label_visibility="collapsed"
            )
            st.write("---")

        # Action layout buttons line
        col_submit, col_reset, _ = st.columns([1, 1, 2])
        
        submit_clicked = col_submit.button("Submit Answers 🚀", type="primary", use_container_width=True)
        if col_reset.button("Retake Quiz 🔄", use_container_width=True):
            # Reset selections by clearing element keys from session state
            for idx in range(1, len(quiz_data) + 1):
                if f"quiz_q_{idx}" in st.session_state:
                    del st.session_state[f"quiz_q_{idx}"]
            st.rerun()

    # ==========================================
    # EVALUATION & PERFORMANCE METRICS SUMMARY
    # ==========================================
    if submit_clicked:
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("## 📊 Evaluation Summary")
        
        correct_count = 0
        total_questions = len(quiz_data)

        for idx, q_node in enumerate(quiz_data, 1):
            selected = user_answers.get(idx)
            correct_ans = q_node.get("answer", "")

            # Match criteria evaluation checking
            if selected == correct_ans:
                correct_count += 1
                st.success(f"🏅 **Question {idx}: Correct!** You selected '{selected}'.")
            else:
                st.error(f"❌ **Question {idx}: Incorrect.** You selected '{selected if selected else 'None'}'. The correct answer was **'{correct_ans}'**.")

        # Compute accuracy scores safely
        accuracy_percentage = int((correct_count / total_questions) * 100) if total_questions > 0 else 0

        # Display performance scorecard layout row
        st.write("")
        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("FINAL SCORE", f"{correct_count} / {total_questions}")
        metric_col2.metric("ACCURACY PERCENTAGE", f"{accuracy_percentage}%")

        if accuracy_percentage >= 70:
            st.balloons()
            st.success("Great job! You have a solid grasp of this lecture material. 🎉")
        else:
            st.info("💡 Keep learning! Review your generated summaries or notes and try again.")