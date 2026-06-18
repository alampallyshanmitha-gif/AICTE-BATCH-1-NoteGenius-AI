import streamlit as st

def show_summary():

    st.title("📝 AI Summary")

    if "summary" not in st.session_state:
        st.warning("No summary generated yet.")
        return

    st.markdown(
        """
        <div style="
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 2px 10px rgba(0,0,0,0.1);
        ">
        """,
        unsafe_allow_html=True
    )

    st.write(st.session_state["summary"])

    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📥 Download Summary",
            st.session_state["summary"],
            file_name="summary.txt"
        )

    with col2:
        if st.button("🗑 Clear Summary"):
            del st.session_state["summary"]
            st.rerun()