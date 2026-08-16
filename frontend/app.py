import os
import sys
import streamlit as st
from dotenv import load_dotenv

# Page Title & Layout Configuration
st.set_page_config(page_title="AI Legal Assistant — Q&A", page_icon="⚖️", layout="wide")

# Setup Candidate Paths for Backend Modules
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
SRC_CANDIDATES = [
    os.path.join(BASE_DIR, "src"),
    os.path.join(PARENT_DIR, "AI-Legal-Assistant", "src"),
    os.path.join(PARENT_DIR, "src"),
    os.path.join(PARENT_DIR, "models"),
    BASE_DIR,
]
for src_path in SRC_CANDIDATES:
    if os.path.exists(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)

# Load Environment Variables (.env)
ENV_CANDIDATES = [
    os.path.join(BASE_DIR, ".env"),
    os.path.join(PARENT_DIR, ".env"),
    os.path.join(PARENT_DIR, "AI-Legal-Assistant", ".env"),
]
for env_path in ENV_CANDIDATES:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)

# Import RAG Modules
try:
    from search import search
    from llm import generate_answer, expand_query
    RAG_AVAILABLE = True
except Exception:
    RAG_AVAILABLE = False

# Helper to locate dataset and index files


def get_file_path(filename):
    candidates = [
        os.path.join(BASE_DIR, "data", filename),
        os.path.join(PARENT_DIR, "AI-Legal-Assistant", "data", filename),
        os.path.join(PARENT_DIR, "data", filename),
        os.path.join(BASE_DIR, filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


# Streamlit App Header
st.title("⚖️ AI Legal Assistant — Q&A Engine")
st.write("Ask any Indian legal question and get precise **AI Answers** grounded in statutory laws (BNS, BNSS, BSA, COI, IT Act, etc.).")

# Load settings from environment
groq_api_key = os.getenv("GROQ_API_KEY", "")
top_k = 5

st.markdown("---")

# Main Q&A Input Box
st.subheader("❓ Ask Your Legal Question")

col_q, col_btn = st.columns([4, 1])
with col_q:
    user_question = st.text_input(
        "Enter your legal question",
        placeholder="e.g. What is the punishment for theft under BNS? Or What is cyber terrorism?"
    )
with col_btn:
    st.write("")
    st.write("")
    ask_clicked = st.button("🤖 Get AI Answer", type="primary", use_container_width=True)

# Sample Question Pills
st.markdown("**💡 Sample Questions:**")
col1, col2, col3 = st.columns(3)
if col1.button("📌 Punishment for Theft under BNS"):
    user_question = "What is the punishment for theft under Bharatiya Nyaya Sanhita (BNS)?"
    ask_clicked = True
if col2.button("📌 Fundamental Rights under COI"):
    user_question = "What are the Fundamental Rights guaranteed under the Constitution of India?"
    ask_clicked = True
if col3.button("📌 Cyber Terrorism under IT Act"):
    user_question = "What is cyber terrorism under the Information Technology Act?"
    ask_clicked = True

st.markdown("---")

# Execute Q&A Workflow when user submits question
if (ask_clicked or user_question.strip()) and user_question.strip():
    st.subheader("💡 Answer")

    index_path = get_file_path("bm25_index.pkl")

    with st.spinner("🔍 Searching legal documents and generating answer..."):
        try:
            # Step 1: Search relevant legal clauses
            search_query = user_question
            if groq_api_key and RAG_AVAILABLE:
                expanded = expand_query(user_question)
                if expanded:
                    search_query = expanded
                    st.info(f"🧠 AI expanded your search to: `{search_query}`")

            results = search(query=search_query, top_k=top_k, index_path=index_path)

            # Step 2: Generate Answer using Groq LLM
            if groq_api_key and RAG_AVAILABLE:
                try:
                    answer = generate_answer(user_question, results)
                except Exception as llm_err:
                    st.warning(f"⚠️ LLM generation error: {llm_err}")
                    answer = None
            elif not RAG_AVAILABLE:
                st.warning("⚠️ RAG module (llm.py) is not yet implemented. Displaying raw BM25 legal sections instead.")
                answer = None
            else:
                st.warning("⚠️ GROQ_API_KEY is missing. Please enter your Groq API Key in the sidebar.")
                answer = None

            # Display ONLY the Direct AI Answer
            if answer:
                st.markdown("### 🤖 Direct AI Legal Answer:")
                st.success(answer)

        except Exception as e:
            st.error(f"Error executing Q&A pipeline: {e}")
