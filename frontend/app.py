import os
import sys
import streamlit as st

# Setup sys.path for src and models directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
MODELS_DIR = os.path.join(BASE_DIR, "models")

for d in [BASE_DIR, SRC_DIR, MODELS_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

from rag_engine import process_user_query, DISCLAIMER_TEXT

# Page Config
st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# App Header
st.title("⚖️ AI Legal Assistant")
st.write("Search government laws and legal documents in simple plain language.")

# User Input Field
question = st.text_input(
    "Enter your legal question:",
    placeholder="e.g. What is the procedure for filing an RTI application?"
)

# Search & Results Display
if st.button("Search Legal Documents", type="primary") or question:
    if question.strip():
        with st.spinner("Searching legal documents..."):
            result = process_user_query(question)

        col1, col2 = st.columns([1.2, 0.8])

        with col1:
            st.subheader("💡 Plain Language Summary")
            st.markdown(result.get("summary", "No summary available."))

        with col2:
            st.subheader("📖 Relevant Legal Sources")
            citations = result.get("citations", [])
            if not citations:
                st.info("No relevant sections found.")
            else:
                for i, c in enumerate(citations, 1):
                    with st.expander(f"{i}. {c.get('act_short_name', 'Act')} - Section {c.get('section', 'N/A')}"):
                        st.write(f"**Act:** {c.get('act_name', '')}")
                        st.write(f"**Section Title:** {c.get('section_title', '')}")
                        st.write(f"**Page:** {c.get('page', '')}")
                        st.write(f"**Text:** {c.get('text', '')}")

        st.markdown("---")
        st.caption(result.get("disclaimer", DISCLAIMER_TEXT))
