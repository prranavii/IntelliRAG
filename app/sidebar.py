import streamlit as st


def render_sidebar():

    st.sidebar.title("📚 Knowledge Sources")

    source = st.sidebar.radio(

        "Choose Source",

        [

            "PDF",

            "GitHub Repository",


        ]

    )

    return source