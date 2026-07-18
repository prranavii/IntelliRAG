import sys
import time
from pathlib import Path


# ------------------------------------------------------------
# Add project root to Python Path
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from app.styles import load_css
from app.sidebar import render_sidebar
from app.components import (
    pdf_component,
    github_component
)
from app.file_manager import (
    save_uploaded_files,
    get_uploaded_files,
)

from rag.ingest import IngestionManager
from rag.query_engine import QueryEngine
from app.database import clear_knowledge_base

# ------------------------------------------------------------
# Cache Query Engine
# ------------------------------------------------------------
@st.cache_resource
def get_query_engine():
    return QueryEngine()


# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="🚀 IntelliRAG",
    page_icon="🚀",
    layout="wide"
)

load_css()


# ------------------------------------------------------------
# Title
# ------------------------------------------------------------
st.title("🚀 IntelliRAG")
st.caption("AI-Powered Multi-Source RAG Assistant")


# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------
if "kb_ready" not in st.session_state:
    st.session_state.kb_ready = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

if "last_source" not in st.session_state:
    st.session_state.last_source = ""


# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
source = render_sidebar()
# ------------------------------------------------------------
# Uploaded Files in Sidebar
# ------------------------------------------------------------
uploaded_files = get_uploaded_files()

if uploaded_files:

    st.sidebar.divider()
    st.sidebar.subheader("📂 Uploaded Files")

    for file in uploaded_files:
        st.sidebar.write(f"📄 {file}")

st.sidebar.divider()

st.sidebar.subheader("📊 Knowledge Base")

st.sidebar.write(
    f"📄 Documents : {st.session_state.document_count}"
)

st.sidebar.write(
    f"🧩 Chunks : {st.session_state.chunk_count}"
)

st.sidebar.write(
    f"📚 Source : {st.session_state.last_source}"
)

st.sidebar.divider()

if st.sidebar.button("🗑 Clear Knowledge Base"):

    clear_knowledge_base()

    get_query_engine.clear()

    st.session_state.messages = []

    st.session_state.kb_ready = False

    st.session_state.chunk_count = 0

    st.session_state.document_count = 0

    st.session_state.last_source = ""

    st.rerun()


# ============================================================
# PDF INGESTION
# ============================================================

if source == "PDF":

    uploaded_files, build = pdf_component()

    if build:

        if not uploaded_files:

            st.warning("⚠ Please upload at least one PDF.")

        else:

            with st.spinner("📁 Saving uploaded PDFs..."):
                save_uploaded_files(uploaded_files)

            with st.spinner("🧠 Building Knowledge Base..."):

                manager = IngestionManager()

                chunk_count = manager.ingest_pdf("data/uploads")

            # Refresh Query Engine
            get_query_engine.clear()

            # Update Session State
            st.session_state.messages = []
            st.session_state.kb_ready = True
            st.session_state.chunk_count = chunk_count
            st.session_state.document_count = len(uploaded_files)
            st.session_state.last_source = "PDF"

            st.success("✅ Knowledge Base Created Successfully!")


# ============================================================
# GITHUB INGESTION
# ============================================================

elif source == "GitHub Repository":

    github_url, build = github_component()

    if build:

        if not github_url.strip():

            st.warning("⚠ Please enter a GitHub Repository URL.")

        else:

            with st.spinner("📦 Cloning Repository..."):

                manager = IngestionManager()

                chunk_count = manager.ingest_github(github_url)

            # Refresh Query Engine
            get_query_engine.clear()

            # Update Session State
            st.session_state.messages = []
            st.session_state.kb_ready = True
            st.session_state.chunk_count = chunk_count
            st.session_state.document_count = 1
            st.session_state.last_source = "GitHub"

            st.success("✅ GitHub Repository Indexed Successfully!")


# ============================================================
# KNOWLEDGE BASE STATUS
# ============================================================

if st.session_state.kb_ready:

    st.divider()

    st.subheader("📊 Knowledge Base Status")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📄 Documents", st.session_state.document_count)

    with col2:
        st.metric("🧩 Chunks", st.session_state.chunk_count)

    with col3:
        st.metric("📚 Source", st.session_state.last_source)


# ============================================================
# CHAT
# ============================================================

if st.session_state.kb_ready:

    st.divider()

    col1, col2 = st.columns([8, 1])

    with col1:
        st.header("💬 Chat with IntelliRAG")

    with col2:
        if st.button("🗑", help="Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Previous Messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Box
    question = st.chat_input(
        "Ask anything about your knowledge base..."
    )

    if question:

        # User Message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # Assistant Response
        with st.spinner("🤖 Thinking..."):

            engine = get_query_engine()

            start = time.time()

            response = engine.ask(question)

            end = time.time()

        answer = response["answer"]
       
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

            st.caption(f"⏱ Response generated in {end-start:.2f} sec")


            with st.expander("📚 Sources Used"):

                for i, doc in enumerate(response["documents"], start=1):

                    st.markdown(f"### Source {i}")

                    if "source" in doc.metadata:
                        st.write("**File:**", doc.metadata["source"])

                    st.write(doc.page_content[:800])

                    st.divider()

    else:

        st.divider()
       