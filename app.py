# System SQLite override for Linux/Cloud environments (Chroma requires SQLite >= 3.35.0)
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import sys
import time
from pathlib import Path

# ------------------------------------------------------------
# Add project root to Python Path
# ------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
from git import Repo

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
from rag.github_reader import IGNORE_DIRS, SUPPORTED_EXTENSIONS
from rag.config import REPOS_DIR, UPLOAD_DIR

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
    page_title="INTELLIRAG // Research Workspace",
    page_icon="⚡",
    layout="wide"
)

load_css()


# ------------------------------------------------------------
# Session State Init & Reset Workspace
# ------------------------------------------------------------
if "workspace_id" not in st.session_state:
    st.session_state.workspace_id = 0

if "kb_ready" not in st.session_state:
    st.session_state.kb_ready = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_source" not in st.session_state:
    st.session_state.current_source = "PDF"
    
if "chunk_count" not in st.session_state:
    st.session_state.chunk_count = 0

if "document_count" not in st.session_state:
    st.session_state.document_count = 0

if "last_source" not in st.session_state:
    st.session_state.last_source = ""

if "repo_name" not in st.session_state:
    st.session_state.repo_name = ""

if "repo_branch" not in st.session_state:
    st.session_state.repo_branch = ""

if "indexed_time" not in st.session_state:
    st.session_state.indexed_time = ""


def reset_workspace():
    clear_knowledge_base()
    get_query_engine.clear()
    st.session_state.messages = []
    st.session_state.kb_ready = False
    st.session_state.chunk_count = 0
    st.session_state.document_count = 0
    st.session_state.last_source = ""
    st.session_state.repo_name = ""
    st.session_state.repo_branch = ""
    st.session_state.indexed_time = ""
    st.session_state.workspace_id = st.session_state.get("workspace_id", 0) + 1
    if "run_reset" in st.session_state:
        del st.session_state.run_reset


# Execute reset trigger if requested from sidebar
if st.session_state.get("run_reset", False):
    reset_workspace()
    st.rerun()


# ------------------------------------------------------------
# Sidebar Navigation & Workspace Controls
# ------------------------------------------------------------
source = render_sidebar()

# If source changes, reset everything
if st.session_state.current_source != source:
    st.session_state.current_source = source
    reset_workspace()
    st.rerun()

# Render indexed files in the sidebar
uploaded_files = get_uploaded_files()
if uploaded_files:
    st.sidebar.divider()
    st.sidebar.markdown(
        """
        <div class="custom-card-header" style="margin-bottom: 0.5rem; font-size: 0.75rem;">📂 Indexed Files</div>
        """,
        unsafe_allow_html=True
    )
    for file in uploaded_files:
        st.sidebar.markdown(
            f"""
            <div style="font-family: var(--font-mono); font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="{file}">
                📄 {file}
            </div>
            """,
            unsafe_allow_html=True
        )

# Render compact metrics in the sidebar
st.sidebar.divider()
st.sidebar.markdown(
    """
    <div class="custom-card-header" style="margin-bottom: 0.5rem; font-size: 0.75rem;">📊 Workspace Info</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    f"""
    <div style="display: grid; grid-template-columns: 1fr; gap: 0.35rem; font-family: var(--font-mono); font-size: 0.8rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">DOCUMENTS:</span>
            <span style="color: var(--text-primary); font-weight: 500;">{st.session_state.document_count}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">CHUNKS:</span>
            <span style="color: var(--text-primary); font-weight: 500;">{st.session_state.chunk_count}</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
            <span style="color: var(--text-muted);">SOURCE:</span>
            <span style="color: var(--text-primary); font-weight: 500;">{st.session_state.last_source if st.session_state.last_source else 'NONE'}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

# Sidebar reset workspace button
if st.sidebar.button("🗑 Clear Workspace Database", key="clear_kb_btn", type="secondary", use_container_width=True):
    reset_workspace()
    st.rerun()


# ------------------------------------------------------------
# Hero Section
# ------------------------------------------------------------
status_color = "var(--success)" if st.session_state.kb_ready else "var(--warning)"
status_label = "ACTIVE" if st.session_state.kb_ready else "IDLE"

st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
        <div>
            <h1 style="margin: 0; font-family: var(--font-sans); font-size: 2rem; font-weight: 700; letter-spacing: -0.03em; color: var(--text-primary);">
                IntelliRAG
            </h1>
            <p style="margin: 0.25rem 0 0 0; font-size: 0.9rem; color: var(--text-secondary);">
                AI-Powered Workspace for Structured Research and Retrieval
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem; font-family: var(--font-mono); font-size: 0.7rem; background-color: var(--bg-card); border: 1px solid var(--border-color); padding: 0.35rem 0.75rem; border-radius: 4px;">
            <span style="display: inline-block; width: 6px; height: 6px; background-color: {status_color}; border-radius: 50%;"></span>
            <span style="color: var(--text-muted);">STATUS:</span>
            <span style="color: var(--text-primary); font-weight: 500;">{status_label}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Dynamic Page Architecture
# ------------------------------------------------------------

if not st.session_state.kb_ready:
    # ============================================================
    # STATE 1: KNOWLEDGE BUILDER (No Knowledge Base Ingested)
    # ============================================================
    col_left, col_right = st.columns([6, 5], gap="large")
    
    with col_left:
        st.markdown(
            """
            <div class="custom-card-header">01 // INGESTION WORKSPACE</div>
            """,
            unsafe_allow_html=True
        )
        with st.container(border=True):
            if source == "PDF":
                uploaded_files, build = pdf_component()
                if build:
                    if not uploaded_files:
                        st.warning("⚠ Please upload at least one PDF.")
                    else:
                        with st.spinner("Saving uploaded PDFs..."):
                            save_uploaded_files(uploaded_files)
                        try:
                            with st.spinner("Extracting & Indexing content..."):
                                manager = IngestionManager()
                                chunk_count = manager.ingest_pdf(str(UPLOAD_DIR))
                            st.session_state.messages = []
                            st.session_state.kb_ready = True
                            st.session_state.chunk_count = chunk_count
                            st.session_state.document_count = len(uploaded_files)
                            st.session_state.last_source = "PDF"
                            st.session_state.repo_name = ""
                            st.session_state.repo_branch = ""
                            st.session_state.indexed_time = time.strftime("%Y-%m-%d %H:%M:%S")
                            get_query_engine.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ingestion failed: {e}")
            elif source == "GitHub Repository":
                github_url, build = github_component()
                if build:
                    if not github_url.strip():
                        st.warning("⚠ Please enter a GitHub Repository URL.")
                    else:
                        try:
                            with st.spinner("Cloning Repository..."):
                                manager = IngestionManager()
                                chunk_count = manager.ingest_github(github_url)
                            
                            # Extract GitHub metadata
                            repo_name = github_url.rstrip("/").split("/")[-1]
                            repo_path = REPOS_DIR / repo_name
                            try:
                                with Repo(repo_path) as repo:
                                    branch = repo.active_branch.name
                            except Exception:
                                branch = "main"
                                
                            file_count = 0
                            if repo_path.exists():
                                for file in repo_path.rglob("*"):
                                    if any(part in IGNORE_DIRS for part in file.parts):
                                        continue
                                    if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                                        continue
                                    file_count += 1
                                    
                            st.session_state.messages = []
                            st.session_state.kb_ready = True
                            st.session_state.chunk_count = chunk_count
                            st.session_state.document_count = file_count
                            st.session_state.last_source = "GitHub"
                            st.session_state.repo_name = repo_name
                            st.session_state.repo_branch = branch
                            st.session_state.indexed_time = time.strftime("%Y-%m-%d %H:%M:%S")
                            get_query_engine.clear()
                            st.rerun()
                        except Exception as e:
                            st.error(f"Ingestion failed: {e}")
                        
    with col_right:
        st.markdown(
            """
            <div class="custom-card-header">02 // INDEX METRICS</div>
            """,
            unsafe_allow_html=True
        )
        
        # Native metric boxes styled by custom css
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric("Documents", st.session_state.document_count)
        with m_col2:
            st.metric("Chunks Indexed", st.session_state.chunk_count)
            
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        # Guide walkthrough flow
        st.markdown(
            """
            <div class="custom-card-header">03 // GETTING STARTED</div>
            <div class="custom-card">
                <div class="onboarding-step active">
                    <div class="onboarding-step-num">STEP 01</div>
                    <div class="onboarding-step-title">Select Ingestion Vector</div>
                    <div class="onboarding-step-desc">Choose between local PDF documents or GitHub Repository ingestion in the sidebar panel.</div>
                </div>
                <div class="onboarding-step">
                    <div class="onboarding-step-num">STEP 02</div>
                    <div class="onboarding-step-title">Upload or Input Credentials</div>
                    <div class="onboarding-step-desc">Drag and drop PDFs or input a public repository URL in the editor panel on the left.</div>
                </div>
                <div class="onboarding-step">
                    <div class="onboarding-step-num">STEP 03</div>
                    <div class="onboarding-step-title">Compile Workspace Index</div>
                    <div class="onboarding-step-desc">Click "Build Knowledge Base" to process, chunk, embed, and load the semantic index.</div>
                </div>
                <div class="onboarding-step">
                    <div class="onboarding-step-num">STEP 04</div>
                    <div class="onboarding-step-title">Begin Workspace Analysis</div>
                    <div class="onboarding-step-desc">Ask questions to research data from source citations in real-time.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    # ============================================================
    # STATE 2: KNOWLEDGE WORKSPACE (Active Research Workspace)
    # ============================================================
    
    # 1. Collapsed secondary Ingestion settings at the top
    with st.expander("📂 Update / Reconfigure Knowledge Base Index", expanded=False):
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        if source == "PDF":
            uploaded_files, build = pdf_component()
            if build:
                if not uploaded_files:
                    st.warning("⚠ Please upload at least one PDF.")
                else:
                    with st.spinner("Saving uploaded PDFs..."):
                        save_uploaded_files(uploaded_files)
                    try:
                        with st.spinner("Extracting & Indexing content..."):
                            manager = IngestionManager()
                            chunk_count = manager.ingest_pdf(str(UPLOAD_DIR))
                        st.session_state.messages = []
                        st.session_state.kb_ready = True
                        st.session_state.chunk_count = chunk_count
                        st.session_state.document_count = len(uploaded_files)
                        st.session_state.last_source = "PDF"
                        st.session_state.repo_name = ""
                        st.session_state.repo_branch = ""
                        st.session_state.indexed_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        get_query_engine.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
        elif source == "GitHub Repository":
            github_url, build = github_component()
            if build:
                if not github_url.strip():
                    st.warning("⚠ Please enter a GitHub Repository URL.")
                else:
                    try:
                        with st.spinner("Cloning Repository..."):
                            manager = IngestionManager()
                            chunk_count = manager.ingest_github(github_url)
                        
                        # Extract GitHub metadata
                        repo_name = github_url.rstrip("/").split("/")[-1]
                        repo_path = REPOS_DIR / repo_name
                        try:
                            with Repo(repo_path) as repo:
                                branch = repo.active_branch.name
                        except Exception:
                            branch = "main"
                            
                        file_count = 0
                        if repo_path.exists():
                            for file in repo_path.rglob("*"):
                                if any(part in IGNORE_DIRS for part in file.parts):
                                    continue
                                if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
                                    continue
                                file_count += 1
                                
                        st.session_state.messages = []
                        st.session_state.kb_ready = True
                        st.session_state.chunk_count = chunk_count
                        st.session_state.document_count = file_count
                        st.session_state.last_source = "GitHub"
                        st.session_state.repo_name = repo_name
                        st.session_state.repo_branch = branch
                        st.session_state.indexed_time = time.strftime("%Y-%m-%d %H:%M:%S")
                        get_query_engine.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
                    
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    # 2. Main Conversation workspace
    col_chat_title, col_chat_actions = st.columns([8, 4])
    with col_chat_title:
        st.markdown(
            f"""
            <div>
                <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--success); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                    Active Workspace // {st.session_state.last_source} Data Ingested
                </div>
                <div style="font-size: 1.5rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">
                    Research Workspace
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_chat_actions:
        st.markdown("<div style='height: 1.1rem;'></div>", unsafe_allow_html=True)
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            if st.button("➕ New Workspace", key="new_ws_btn_main", type="primary", use_container_width=True):
                reset_workspace()
                st.rerun()
        with h_col2:
            if st.button("Clear Chat", key="clear_chat_btn", type="secondary", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
                
    # Show metadata headers (Repository Name, Branch, Chunks, Files, Time)
    if st.session_state.last_source == "GitHub":
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; font-family: var(--font-mono); font-size: 0.75rem;">
                <span class="source-badge">REPO: {st.session_state.repo_name}</span>
                <span class="source-badge">BRANCH: {st.session_state.repo_branch}</span>
                <span class="source-badge">FILES: {st.session_state.document_count}</span>
                <span class="source-badge">CHUNKS: {st.session_state.chunk_count}</span>
                <span class="source-badge">INDEXED: {st.session_state.indexed_time}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else: # PDF
        st.markdown(
            f"""
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.5rem; font-family: var(--font-mono); font-size: 0.75rem;">
                <span class="source-badge">SOURCE: PDF Documents</span>
                <span class="source-badge">FILES: {st.session_state.document_count}</span>
                <span class="source-badge">CHUNKS: {st.session_state.chunk_count}</span>
                <span class="source-badge">INDEXED: {st.session_state.indexed_time}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
            
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    
    # Empty Conversation State
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="custom-card" style="text-align: center; padding: 3rem 2rem; margin-top: 1rem;">
                <div style="font-size: 2.25rem; margin-bottom: 1rem; color: var(--accent);">⚡</div>
                <h3 style="margin-bottom: 0.5rem; font-family: var(--font-sans); color: var(--text-primary); font-size: 1.2rem; font-weight: 600; letter-spacing: -0.01em;">
                    Workspace Semantic Index Compiled
                </h3>
                <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 1.5rem auto; font-size: 0.9rem; line-height: 1.6;">
                    The vector database has been initialized. Query the workspace to perform semantic searches, synthesize documentation, or analyze control flows.
                </p>
                <div style="display: flex; flex-direction: column; gap: 0.5rem; max-width: 400px; margin: 0 auto; text-align: left;">
                    <div style="font-family: var(--font-mono); font-size: 0.7rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; text-align: center;">
                        Suggested Queries
                    </div>
                    <div style="font-size: 0.8rem; padding: 0.5rem 0.75rem; border: 1px solid var(--border-color); background-color: var(--bg-secondary); border-radius: 4px; color: var(--text-secondary); font-family: var(--font-mono);">
                        • Summarize the core structural flow of this project
                    </div>
                    <div style="font-size: 0.8rem; padding: 0.5rem 0.75rem; border: 1px solid var(--border-color); background-color: var(--bg-secondary); border-radius: 4px; color: var(--text-secondary); font-family: var(--font-mono);">
                        • What are the main interfaces or formats implemented?
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Render Message History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                if "duration" in message:
                    st.markdown(
                        f"""
                        <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                            <span>⏱ Latency: {message['duration']:.2f}s</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                if "documents" in message and message["documents"]:
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    with st.expander("📚 Sources Referenced", expanded=False):
                        for idx, doc in enumerate(message["documents"], start=1):
                            st.markdown(f"**Source {idx}:** `{doc.get('source', 'Unknown')}`")
                            st.markdown(
                                f"""
                                <div style="font-family: var(--font-mono); font-size: 0.8rem; background-color: var(--bg-secondary); border: 1px solid var(--border-color); padding: 0.75rem; border-radius: 4px; color: var(--text-secondary); margin-bottom: 0.75rem; max-height: 200px; overflow-y: auto; white-space: pre-wrap;">
{doc.get('page_content', '')[:800]}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

    # Chat Input Box
    question = st.chat_input("Query the semantic index...")
    
    if question:
        # Add user message to history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )
        with st.chat_message("user"):
            st.markdown(question)
            
        # Assistant Response processing
        with st.chat_message("assistant"):
            with st.spinner("Searching workspace index..."):
                engine = get_query_engine()
                start = time.time()
                response = engine.ask(question)
                end = time.time()
                
            answer = response["answer"]
            st.markdown(answer)
            
            # Print duration
            duration = end - start
            st.markdown(
                f"""
                <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>⏱ Latency: {duration:.2f}s</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Print sources expander
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            with st.expander("📚 Sources Referenced", expanded=False):
                for idx, doc in enumerate(response["documents"], start=1):
                    doc_src = doc.metadata.get("source", "Unknown")
                    st.markdown(f"**Source {idx}:** `{doc_src}`")
                    st.markdown(
                        f"""
                        <div style="font-family: var(--font-mono); font-size: 0.8rem; background-color: var(--bg-secondary); border: 1px solid var(--border-color); padding: 0.75rem; border-radius: 4px; color: var(--text-secondary); margin-bottom: 0.75rem; max-height: 200px; overflow-y: auto; white-space: pre-wrap;">
{doc.page_content[:800]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Serialize documents and save to session history
            docs_list = []
            for doc in response["documents"]:
                docs_list.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "page_content": doc.page_content
                })
            
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "duration": duration,
                    "documents": docs_list
                }
            )
            st.rerun()