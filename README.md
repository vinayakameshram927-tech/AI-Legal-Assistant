# ⚖️ AI-Legal-Assistant

An intelligent legal document search pipeline that processes Indian legal codes (PDFs), builds a highly efficient BM25 search index, and provides an interactive UI to quickly retrieve the most relevant legal sections based on natural language queries.

## 🚀 Project Overview

The project is built on a modular pipeline architecture designed to process, index, and query complex legal documents.

### 1. Data Processing Pipeline (`src/pdf_loader.py` & `src/chunker.py`)
- **PDF Extraction**: Reads legal PDFs using PyMuPDF (`pypdf`).
- **Semantic Chunking**: Automatically detects legal sections, splits the text into logical chunks, and attaches metadata (Act Name, Section Title, Page Number).
- **Export**: Saves the structured chunks to a highly optimized `.csv` dataset for indexing.

### 2. BM25 Search Engine (`src/build_index.py` & `src/search.py`)
- **Indexing**: Tokenizes and preprocesses the legal chunks to build a highly optimized BM25 statistical search index.
- **Retrieval**: Takes user queries and ranks the most relevant chunks using BM25 scoring, returning the top matches instantly.

### 3. Interactive UI (`frontend/app.py`)
- **Streamlit App**: Provides a clean, user-friendly web interface where users can ask legal questions and dynamically select how many results they want to retrieve.
- **Results Display**: Beautifully formats the retrieved data, showing the exact Act, Section, Page, and original legal text alongside the relevance score.

---

## 🛠️ Setup & Installation

### Prerequisites
Make sure you have Python installed.

### 1. Install Dependencies
Install all required packages by running:
```bash
pip install -r requirements.txt
```

*(This will install `pypdf`, `pandas`, `joblib`, `rank_bm25`, and `streamlit`)*

---

## 🏃‍♂️ How to Run the Project

### Step 1: Process PDFs and Build the Index
Before searching, you must parse the raw PDFs and generate the BM25 index. You can do this easily via the main CLI tool.
```bash
python src/main.py
```
*Select **Option 1** to process the PDFs, then **Option 2** to build the BM25 index.*

### Step 2: Start the Web UI
Once the index is built, you can start the Streamlit web application to start querying:
```bash
streamlit run frontend/app.py
```
*(Alternatively, you can test the search engine directly in the terminal by selecting **Option 3** in `src/main.py`)*

---

## 📁 Directory Structure
```
AI-Legal-Assistant/
├── data/
│   └── pdfs/             # Raw legal PDF documents
├── src/
│   ├── build_data.py     # Script to generate chunks.csv from PDFs
│   ├── build_index.py    # Script to build BM25 index from chunks.csv
│   ├── chunker.py        # Logic for splitting text into legal sections
│   ├── main.py           # CLI Interface for the pipeline
│   ├── pdf_loader.py     # PDF parsing logic
│   └── search.py         # BM25 Retrieval logic
├── frontend/
│   └── app.py            # Streamlit Web UI
└── requirements.txt      # Python dependencies