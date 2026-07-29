import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import key_param

app = FastAPI(title="RAG Chatbot")

static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

DB_NAME = "singapore_pr_chunks"
COLLECTION_NAME = "chunked_data"
INDEX_NAME = "vector_index"

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=key_param.MONGODB_URI,
    namespace=f"{DB_NAME}.{COLLECTION_NAME}",
    embedding=embeddings,
    index_name=INDEX_NAME,
)

llm = ChatOllama(model="gemma3:4b", temperature=0)

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

chat_history = []

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def root():
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

@app.post("/chat")
async def chat(request: ChatRequest):
    question = request.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    results = vector_store.similarity_search_with_score(question, k=3)
    context = "\n\n".join(doc.page_content for doc, _ in results)

    history = ""
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Assistant: {msg.content}\n"

    messages = prompt.invoke({
        "history": history,
        "context": context,
        "question": question,
    })

    async def generate():
        answer = ""
        async for chunk in llm.astream(messages):
            if chunk.content:
                yield f"data: {json.dumps({'token': chunk.content})}\n\n"
                answer += chunk.content

        chat_history.append(HumanMessage(content=question))
        chat_history.append(AIMessage(content=answer))

        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/history")
async def get_history():
    messages = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            messages.append({"role": "user", "content": msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({"role": "assistant", "content": msg.content})
    return {"messages": messages}

@app.delete("/history")
async def clear_history():
    chat_history.clear()
    return {"status": "ok"}
