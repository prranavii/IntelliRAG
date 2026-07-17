import streamlit as st


def chat_component():

    st.divider()

    st.header("💬 Chat with IntelliRAG")

    question = st.text_input(
        "Ask anything about your uploaded documents",
        placeholder="Example: Summarize this resume"
    )

    ask = st.button("🚀 Ask")

    return question, ask