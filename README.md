# 📚 RAG Application using MongoDB Atlas + Ollama

A Retrieval-Augmented Generation (RAG) application that allows users to chat with PDF documents using **MongoDB Atlas Vector Search**, **Ollama**, **Gemma 3**, and **LangChain**.

The application converts PDF documents into vector embeddings, stores them in MongoDB Atlas, retrieves the most relevant document chunks using Vector Search, and generates accurate answers using a locally running LLM.

---

# 🚀 Features

- 📄 Load PDF documents
- ✂️ Split documents into chunks
- 🧠 Generate embeddings locally using Ollama
- 💾 Store embeddings in MongoDB Atlas
- 🔍 Perform semantic search with MongoDB Vector Search
- 🤖 Generate answers using Gemma 3
- 💬 Interactive terminal chatbot
- 🆓 Completely free (No OpenAI API required)

---

# 🏗️ Tech Stack

- Python 3.11
- LangChain
- MongoDB Atlas
- MongoDB Vector Search
- Ollama
- Gemma 3:4b
- nomic-embed-text
- PyPDF

---

# 📂 Project Structure

```
RAG Application/
│
├── sample_files/
│     └── singpore_pr_details.pdf
│
├── load_data.py
├── rag.py
├── key_param.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Prerequisites

- Python 3.11+
- MongoDB Atlas Account
- Ollama

---

# Step 1 - Install Ollama

Download and install Ollama

https://ollama.com/download

Verify Installation

```bash
ollama --version
```

---

# Step 2 - Download Gemma 3

```bash
ollama pull gemma3:4b
```

Verify

```bash
ollama list
```

Expected Output

```
gemma3:4b
```

---

# Step 3 - Download Embedding Model

```bash
ollama pull nomic-embed-text
```

Verify

```bash
ollama list
```

Expected Output

```
gemma3:4b
nomic-embed-text
```

---

# Step 4 - Install Python Packages

```bash
pip install langchain
pip install langchain-community
pip install langchain-core
pip install langchain-text-splitters
pip install langchain-ollama
pip install langchain-mongodb
pip install pymongo
pip install pypdf
```

or

```bash
pip install langchain langchain-community langchain-core langchain-text-splitters langchain-ollama langchain-mongodb pymongo pypdf
```

---

# Step 5 - Create MongoDB Atlas Cluster

1. Create a MongoDB Atlas account.
2. Create an M0 Free Cluster.
3. Create a Database User.
4. Allow Network Access (`0.0.0.0/0`).
5. Copy the MongoDB Connection String.

Example

```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

---

# Step 6 - Create key_param.py

```python
MONGODB_URI = "YOUR_MONGODB_CONNECTION_STRING"
```

---

# Step 7 - Add PDF

Create a folder

```
sample_files/
```

Place your PDF inside.

Example

```
sample_files/
    singpore_pr_details.pdf
```

---

# Step 8 - Load Data into MongoDB

Run

```bash
python load_data.py
```

This will

- Read the PDF
- Remove empty pages
- Split into chunks
- Generate embeddings using `nomic-embed-text`
- Store vectors in MongoDB Atlas

Expected Output

```
Old documents deleted.
Total pages loaded.
Pages cleaned.
Chunks created.
Creating embeddings...
Data successfully stored.
```

---

# Step 9 - Create Vector Search Index

Open

```
MongoDB Atlas
```

Go to

```
Database
    ↓
Search
    ↓
Create Search Index
```

Choose

```
Bring your own embeddings
```

Index Name

```
vector_index
```

Database

```
singapore_pr_chunks
```

Collection

```
chunked_data
```

Vector Field

```
embedding
```

Dimensions

```
768
```

Similarity

```
Cosine
```

Wait until the index status becomes

```
READY
```

---

# Step 10 - Run the RAG Application

```bash
python rag.py
```

Example

```
==============================
 Singapore PR RAG Assistant
==============================

You:
```

Ask

```
Who is eligible for Singapore PR?
```

Output

```
Assistant:

A foreigner granted permanent residence status, allowing indefinite stay in Singapore.
```

Exit

```
exit
```

or

```
quit
```

---

# RAG Workflow

```
                PDF
                 │
                 ▼
        PyPDFLoader
                 │
                 ▼
      Recursive Chunking
                 │
                 ▼
      Ollama Embeddings
    (nomic-embed-text)
                 │
                 ▼
       MongoDB Atlas
      Vector Database
                 │
                 ▼
      Vector Search Index
                 │
                 ▼
       User Question
                 │
                 ▼
 Question Embedding
                 │
                 ▼
 Semantic Search
                 │
                 ▼
 Top Relevant Chunks
                 │
                 ▼
      Gemma 3 (LLM)
                 │
                 ▼
      Final Response
```

---

# Commands Summary

## Install Ollama

```bash
ollama --version
```

## Download Gemma

```bash
ollama pull gemma3:4b
```

## Download Embedding Model

```bash
ollama pull nomic-embed-text
```

## View Installed Models

```bash
ollama list
```

## Load PDF

```bash
python load_data.py
```

## Run Chatbot

```bash
python rag.py
```

---

# Future Improvements

- Streamlit Web Interface
- Multi-PDF Support
- PDF Upload Feature
- Chat History Storage
- Source Citation
- User Authentication
- Multiple Collections
- Hybrid Search
- Metadata Filtering

---

# Author

**Santhosh P**

- Robotics
- Artificial Intelligence
- IoT
- Computer Vision
