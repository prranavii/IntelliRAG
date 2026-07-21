import streamlit as st


def pdf_component():
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Step 2 & 3: Ingestion Source
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">
                Upload Source Documents
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem; line-height: 1.5;">
                Select one or more PDF files to index. The engine parses, chunks, and commits them to the vector search index.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Use a dynamic key based on workspace_id to reset the widget state upon new workspace creation
    ws_id = st.session_state.get("workspace_id", 0)
    uploaded_files = st.file_uploader(
        "Upload one or more PDFs",
        type="pdf",
        accept_multiple_files=True,
        key=f"pdf_upload_{ws_id}",
        label_visibility="collapsed"
    )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    build = st.button(
        "Build Knowledge Base",
        key=f"pdf_build_{ws_id}",
        type="primary",
        use_container_width=True
    )

    return uploaded_files, build


def github_component():
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Step 2 & 3: Repository Connection
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">
                Index public repository
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem; line-height: 1.5;">
                Enter a public GitHub repository link. The engine clones the source branch and extracts code documents.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Use a dynamic key based on workspace_id to reset the widget state upon new workspace creation
    ws_id = st.session_state.get("workspace_id", 0)
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository",
        label_visibility="collapsed",
        key=f"github_url_{ws_id}"
    )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    build = st.button(
        "Build Knowledge Base",
        key=f"github_build_{ws_id}",
        type="primary",
        use_container_width=True
    )

    return github_url, build


def website_component():
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem;">
                Step 2 & 3: Web Ingestion
            </div>
            <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">
                Crawl Website URL
            </div>
            <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem; line-height: 1.5;">
                Enter the URL to target. The web spider harvests structural documents and references.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Use a dynamic key based on workspace_id to reset the widget state upon new workspace creation
    ws_id = st.session_state.get("workspace_id", 0)
    website_url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com",
        label_visibility="collapsed",
        key=f"website_url_{ws_id}"
    )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    build = st.button(
        "Build Knowledge Base",
        key=f"website_build_{ws_id}",
        type="primary",
        use_container_width=True
    )

    return website_url, build