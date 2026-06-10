from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()

# Step 1: Load vectorstore
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

# Step 2: Load Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# Step 3: Ask question
question = "Who is Ali and what does he want to become?"

# Step 4: Search vectorstore for relevant chunks
docs = db.similarity_search(question, k=3)
context = "\n".join([doc.page_content for doc in docs])

# Step 5: Send to LLM with context
prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}
Answer:"""

response = llm.invoke(prompt)
print("Question:", question)
print("Answer:", response.content)