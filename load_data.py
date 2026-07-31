from pymongo import MongoClient
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch

from dotenv import load_dotenv
import os

# ==========================
# Connect to MongoDB Atlas
# ==========================
load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))

db_name = os.getenv("DB_NAME")
collection_name = os.getenv("COLLECTION_NAME")

db = client[db_name]
collection = db[collection_name]

# Optional: Clear old data
collection.delete_many({})
print("✅ Old documents deleted.")

# ==========================
# Load PDF
# ==========================
loader = PyPDFLoader("sample_files\singpore_pr_details.pdf")
pages = loader.load()

print(f"📄 Total pages in PDF: {len(pages)}")

# ==========================
# Remove empty pages
# ==========================
cleaned_pages = []

for page in pages:
    if len(page.page_content.split()) > 20:
        cleaned_pages.append(page)

print(f"✅ Pages after cleaning: {len(cleaned_pages)}")

# ==========================
# Split into chunks
# ==========================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=150
)

split_docs = text_splitter.split_documents(cleaned_pages)

print(f"✂️ Total chunks created: {len(split_docs)}")

# ==========================
# Ollama Embeddings
# ==========================
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

print("🧠 Creating embeddings and storing in MongoDB...")

# ==========================
# Store in MongoDB Atlas
# ==========================
vector_store = MongoDBAtlasVectorSearch.from_documents(
    documents=split_docs,
    embedding=embeddings,
    collection=collection,
)

print("🎉 Data successfully stored in MongoDB Atlas!")
print(f"Database   : {db_name}")
print(f"Collection : {collection_name}")