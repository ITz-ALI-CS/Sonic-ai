from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os, shutil

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

db = None

def load_db():
    global db
    if os.path.exists("vectorstore"):
        db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

load_db()

class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global db

    os.makedirs("data", exist_ok=True)

    existing_files = os.listdir("data")
    if len(existing_files) >= 5:
        return {"error": "Maximum 5 documents allowed. Click Clear Docs to upload more."}

    file_path = os.path.join("data", file.filename.replace(" ", "_"))
    print(f"Saving file to: {file_path}")

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    all_documents = []
    for f in os.listdir("data"):
        fp = os.path.join("data", f)
        if f.endswith(".pdf"):
            loader = PyPDFLoader(fp)
        elif f.endswith(".txt"):
            loader = TextLoader(fp, encoding="utf-8")
        else:
            continue
        all_documents.extend(loader.load())

    if not all_documents:
        return {"error": "Document is empty or could not be read."}

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_documents)

    if not chunks:
        return {"error": "Document has no content to process."}

    if os.path.exists("vectorstore"):
        shutil.rmtree("vectorstore")

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("vectorstore")

    total = len(os.listdir("data"))
    return {"message": f"✅ '{file.filename}' uploaded! Total: {total}/5 documents"}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    load_db()

    if db is None:
        return {"answer": "⚠️ Please upload a document first before asking questions."}

    docs = db.similarity_search(request.question, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""You are a document assistant. You ONLY answer questions related to the uploaded documents.
If the user sends greetings like "hi", "hello", "how are you" or anything not related to the document, reply with a SHORT varied response like:
- "Hey! I'm here to help with your documents. What would you like to know?"
- "Hello! Ask me anything from your uploaded documents."
- "Hi there! I can answer questions from your documents. Go ahead!"
- "Hey! Ready to help. Ask me something from your documents."
Pick one randomly and vary it each time. Never repeat the same response twice in a row.
If the answer is in the context below, answer directly and confidently.
If the question is document-related but answer is not found, say "I don't have that information in the document."

Context:
{context}

Question: {request.question}
Answer:"""

    response = llm.invoke(prompt)
    return {"answer": response.content}

@app.post("/clear")
def clear_documents():
    global db
    if os.path.exists("data"):
        shutil.rmtree("data")
    if os.path.exists("vectorstore"):
        shutil.rmtree("vectorstore")
    db = None
    return {"message": "✅ All documents cleared!"}

@app.get("/")
def root():
    return {"status": "RAG Agent is running ✅"}

@app.get("/chat")
def serve_frontend():
    return FileResponse("index.html")