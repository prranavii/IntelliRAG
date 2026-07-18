import streamlit as st


def chat_component():

    st.divider()

    col1, col2 = st.columns([6, 1])

    with col1:
        st.header("💬 Chat with IntelliRAG")

    with col2:
        if st.button("🗑 Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    question = st.chat_input(
        "Ask anything about your knowledge base..."
    )

    return question