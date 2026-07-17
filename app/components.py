import streamlit as st


def pdf_component():

    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload one or more PDFs",
        type="pdf",
        accept_multiple_files=True,
        key="pdf_upload"
    )

    build = st.button("🚀 Build Knowledge Base", key="pdf_build")

    return uploaded_files, build


def github_component():

    st.header("🐙 GitHub Repository")

    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository"
    )

    build = st.button("🚀 Build Knowledge Base", key="github_build")

    return github_url, build


def website_component():

    st.header("🌐 Website")

    website_url = st.text_input(
        "Website URL",
        placeholder="https://example.com"
    )

    build = st.button("🚀 Build Knowledge Base", key="website_build")

    return website_url, build