from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os

# ==========================================
# MongoDB Configuration
# ==========================================
DB_NAME = "singapore_pr_chunks"
COLLECTION_NAME = "chunked_data"
INDEX_NAME = "vector_index"
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# ==========================================
# Embedding Model
# ==========================================
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# ==========================================
# MongoDB Vector Store
# ==========================================
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=MONGODB_URI,
    namespace=f"{DB_NAME}.{COLLECTION_NAME}",
    embedding=embeddings,
    index_name=INDEX_NAME,
)

# ==========================================
# Local LLM
# ==========================================
llm = ChatOllama(
    model="gemma3:4b",
    temperature=0,
)

# ==========================================
# Prompt Template
# ==========================================
prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply exactly:

"I couldn't find that information in the provided document."

Conversation History:
{history}

Context:
{context}

Question:
{question}
""")

# ==========================================
# Chat Memory
# ==========================================
chat_history = []

print("\n==============================")
print(" Singapore PR RAG Assistant")
print("==============================")
print("Type 'exit' or 'quit' to close.\n")

while True:

    question = input("You: ").strip()

    # Exit Program
    if question.lower() in ["exit", "quit"]:
        print("\n👋 Goodbye!")
        break

    # ==========================================
    # Retrieve Relevant Documents
    # ==========================================
    results = vector_store.similarity_search_with_score(
        question,
        k=3
    )

    context = ""

    for doc, score in results:
        context += doc.page_content + "\n\n"

    # ==========================================
    # Build Conversation History
    # ==========================================
    history = ""

    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Assistant: {msg.content}\n"

    # ==========================================
    # Build Prompt
    # ==========================================
    messages = prompt.invoke(
        {
            "history": history,
            "context": context,
            "question": question,
        }
    )

    print("\nAssistant: ", end="", flush=True)

    answer = ""

    # ==========================================
    # Stream Response
    # ==========================================
    for chunk in llm.stream(messages):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            answer += chunk.content

    print("\n")

    # ==========================================
    # Save Chat History
    # ==========================================
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=answer))