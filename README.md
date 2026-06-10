# RAG Agent — Chat With Your Documents

I built this because I was tired of scrolling through long documents just to find one answer. So I made something that does it for me.

You upload a file, ask a question, and it tells you exactly what you need to know. No hallucinations, no made up answers — everything comes straight from your document.

The best part about this project is how simple it is to use. You do not need to be technical at all. Just open it in your browser, pick a file from your computer, hit upload, and start asking. It feels like chatting with someone who has read your entire document and remembers every word of it. You can load multiple files at once and ask questions that span across all of them. It will always tell you when something is not in the document instead of guessing, which makes it actually trustworthy.

---

## What it does

- You can upload up to 5 documents at once — PDF or TXT
- It only answers from what's actually in your files
- Shows a small preview of your document before you upload
- Every answer has a copy button so you can grab it quickly
- You can clear everything and start over anytime
- The interface is clean, dark and easy to use

---

## How to run it on your machine

First clone the project and open the folder:

```bash
git clone https://github.com/Ali-Aura/rag-agent.git
cd rag-agent
```

Create a virtual environment so things stay clean:

```bash
python -m venv venv
venv\Scripts\activate
```

Install all the packages it needs:

```bash
pip install langchain langchain-community langchain-groq langchain-huggingface langchain-text-splitters faiss-cpu fastapi uvicorn python-dotenv pypdf sentence-transformers python-multipart
```

Create a file called `.env` in the project folder and put your Groq API key inside it:

```
GROQ_API_KEY=your_key_here
```

You can get a free Groq API key from console.groq.com — it takes about 2 minutes.

Now start the app:

```bash
uvicorn main:app --reload
```

Open your browser and go to:

```
http://127.0.0.1:8000/chat
```

Upload a document, ask anything, and see it work.

---

## What's powering it behind the scenes

- FastAPI is running the backend server
- LangChain is the glue that connects everything
- FAISS stores the document data locally on your machine
- HuggingFace handles turning text into vectors
- Groq is running LLaMA 3.3 which is the brain of the whole thing
- The frontend is just plain HTML, CSS and JavaScript — nothing fancy

---

## A note on the API key

The `.env` file is not uploaded to GitHub for obvious reasons. You need to create your own and add your key. It's free and takes 2 minutes at console.groq.com.

---

## Built by

Ali Asif — CS student from Lahore who enjoys turning ideas into things that actually work. This is one of those things.
