"""
streamlit_app.py
-----------------
Frontend for the Multi-Agent RAG system. Pure Python (no JS/TS needed) —
talks to the FastAPI backend over HTTP, the same way any real frontend would.

Run the backend first:
    uvicorn app.main:app --reload

Then, in a SEPARATE terminal, run this:
    streamlit run streamlit_app.py
"""

import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Multi-Agent RAG — Medicine Assistant", page_icon="💊", layout="centered")

st.title("💊 Medicine RAG Assistant")
st.caption("Multi-agent RAG: Router → Retriever/Web-Search → Synthesizer → Critic")

# --- Sidebar: backend status + history ---
with st.sidebar:
    st.header("Backend")
    try:
        health = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if health.status_code == 200:
            st.success("Connected to FastAPI backend")
        else:
            st.error(f"Backend returned {health.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend not reachable — is `uvicorn app.main:app --reload` running?")

    st.divider()
    st.header("Recent Queries")
    if st.button("Refresh history"):
        st.session_state["refresh_history"] = True

    try:
        history = requests.get(f"{API_BASE_URL}/history", params={"limit": 5}, timeout=5).json()
        if history:
            for h in history:
                icon = "✅" if h.get("grounded") else "⚠️"
                st.markdown(f"{icon} **{h['query'][:40]}{'...' if len(h['query']) > 40 else ''}**")
                st.caption(f"route: {h.get('route_used', '—')}")
        else:
            st.caption("No queries logged yet.")
    except Exception:
        st.caption("History unavailable (is the backend running?)")

# --- Main: ask a question ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for entry in st.session_state["chat_history"]:
    with st.chat_message("user"):
        st.write(entry["question"])
    with st.chat_message("assistant"):
        st.write(entry["answer"])
        badge = "🟢 Grounded" if entry["grounded"] else "🟡 Not fully grounded"
        st.caption(f"{badge} · route: {entry['route_used']} · retries: {entry['retry_count']}")
        if entry["sources"]:
            with st.expander(f"View {len(entry['sources'])} source(s)"):
                for i, src in enumerate(entry["sources"], 1):
                    st.text(f"[{i}] {src}")

question = st.chat_input("Ask about a medicine, e.g. 'What medicines contain Paracetamol?'")

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Routing → retrieving → synthesizing → checking grounding..."):
            try:
                resp = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={"query": question},
                    timeout=120,
                )
                resp.raise_for_status()
                result = resp.json()

                st.write(result["answer"])
                badge = "🟢 Grounded" if result["grounded"] else "🟡 Not fully grounded"
                st.caption(
                    f"{badge} · route: {result['route_used']} · retries: {result['retry_count']}"
                )
                if result["sources"]:
                    with st.expander(f"View {len(result['sources'])} source(s)"):
                        for i, src in enumerate(result["sources"], 1):
                            st.text(f"[{i}] {src}")

                st.session_state["chat_history"].append({
                    "question": question,
                    **result,
                })

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not reach the backend. Make sure it's running:\n\n"
                    "`uvicorn app.main:app --reload`"
                )
            except requests.exceptions.HTTPError as e:
                st.error(f"Backend returned an error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
