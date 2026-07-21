import streamlit as st


def render_sidebar():
    # Determine the system status
    kb_ready = st.session_state.get("kb_ready", False)
    beacon_color = "var(--success)" if kb_ready else "var(--text-muted)"
    beacon_label = "READY" if kb_ready else "EMPTY"
    
    # 1. Brand Identity Header
    st.sidebar.markdown(
        f"""
        <div style="margin-bottom: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1.25rem;">
            <div style="font-family: var(--font-mono); font-size: 1.1rem; font-weight: 700; letter-spacing: -0.05em; color: var(--text-primary); display: flex; align-items: center; justify-content: space-between;">
                <span>INTELLIRAG</span>
                <span class="source-badge" style="margin: 0; color: {beacon_color}; border-color: {beacon_color}; font-size: 0.65rem; padding: 0.1rem 0.35rem;">
                    ● {beacon_label}
                </span>
            </div>
            <div style="font-size: 0.7rem; font-family: var(--font-mono); color: var(--text-muted); margin-top: 0.25rem; letter-spacing: 0.05em;">
                ENGINEERING WORKSPACE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1.5 Prominent reset action if knowledge base is active
    if kb_ready:
        if st.sidebar.button("➕ Index New Knowledge", key="new_ws_btn", type="primary", use_container_width=True):
            st.session_state.run_reset = True
            st.rerun()
        st.sidebar.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    # 2. Navigation Section Label
    st.sidebar.markdown(
        """
        <div class="custom-card-header" style="margin-bottom: 0.5rem; font-size: 0.75rem;">Workspace Source</div>
        """,
        unsafe_allow_html=True
    )

    # Choose Source Selector
    source = st.sidebar.radio(
        "Choose Source",
        [
            "PDF",
            "GitHub Repository",
        ],
        label_visibility="collapsed"
    )

    return source