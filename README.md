# ⚡ Sonic AI — Unstoppable 1.0

A full-stack AI chat application with real-time web search, document-grounded Q&A, and a custom-built admin control panel — built end-to-end with FastAPI, vanilla JS, and Django.

Sonic AI isn't just a chatbot wrapper. It's a complete product: a polished single-page chat client, a FastAPI brain powered by Groq's LLaMA 3.3 70B, a FAISS-backed document retrieval pipeline, and a fully custom Django admin dashboard for monitoring and managing the whole system — all sharing one database, with zero duplication.

---

## ✨ What makes this project different

Most AI chat demos stop at "call an LLM API and stream the response." Sonic AI goes further:

- **Two intelligence modes** — pick between deep, source-cited research (**Effort**) or instant, no-frills answers (**Fast**)
- **Two document modes** — chat with your uploaded files only, or blend them with live web results
- **A prompt improver** — one click rewrites a vague question into a sharper, more specific prompt before you even send it
- **A real admin backend** — not a Django tutorial afterthought, but a 4-page operational dashboard with live charts, audit logs, content moderation, and one-click backups

---

## 🧠 Core AI Features

### Smart format detection
Every question is automatically analyzed and answered in the best-fitting format — no manual toggling required:

| Trigger | Output style |
|---|---|
| "compare X vs Y" | Markdown table |
| "how to..." / "steps to..." | Numbered steps |
| "what are..." / "list..." | Bullet points |
| "explain in detail" | Full paragraphs |
| "write code" / "implement" | Syntax-highlighted code block |
| "what is..." (short factual) | 1–2 sentence direct answer |

You can also override the format manually at any time via the format panel (Auto / Bullets / Table / Steps / Short / Detail).

### Two AI modes
- **⚡ Effort mode** — thorough, deep-search answers with cited web sources (when in Doc+Web mode), built for accuracy over speed
- **🚀 Fast mode** — instant, 2–3 sentence answers with no web search overhead, built for speed over depth

### Document modes — chat with your own files
Upload up to 5 PDF/TXT documents and choose exactly how the AI should use them:

- **📄 Doc Only** — answers come *exclusively* from your uploaded documents. If the answer isn't in your files, the AI tells you instead of guessing or pulling from the web.
- **🌐 Doc + Web** — blends your documents with live web search results, so you get grounded answers that are also current.

Behind the scenes, every upload is chunked (500 chars, 100 overlap), embedded with HuggingFace's `all-MiniLM-L6-v2`, and stored in a FAISS vector index for fast semantic retrieval. Removed documents aren't fully forgotten either — their summary context is optionally retained so the conversation doesn't lose continuity.

### AI Prompt Improver
Typed something vague? Hit **✨ Improve** and the AI rewrites your exact question into a clearer, more specific version — keeping your original topic intact, just sharper. You can re-improve repeatedly from the original prompt, and the system tracks whether your current input has been improved or edited since.

### Real-time web search
Powered by Tavily, with adjustable search depth (`basic` vs `advanced`) and result count depending on whether you're in Effort or Fast mode. Sources are shown as clickable chips below the AI's answer — never buried in the text.

### Conversation memory & smart titles
Every chat is saved with an auto-generated title pulled from the most meaningful thing you actually asked (greetings and filler words like "ok," "thanks," and "hi" are automatically skipped when picking a title).

---

## 🎨 Frontend Experience

A single-file, framework-free HTML/CSS/JS chat interface with:

- **Custom neon dark theme** — cyan, gold, and purple color palette with an animated lightning-bolt logo, glowing text, and orbiting particle effects (light mode included)
- **Typewriter-style response animation** with adjustable speed, stoppable mid-generation
- **Per-message actions** — copy, text-to-speech (8 voice profiles), retry, pin, expand to full view, download as `.txt`
- **Voice input** via the Web Speech API with live interim transcription
- **8 output languages** with automatic instruction injection per response
- **Humanize toggle** — strips robotic phrasing ("certainly," "of course") for a more natural tone
- **Slash commands** — `/summarize`, `/clear`, `/save`, `/new`
- **In-chat search** with match highlighting and jump-to-next navigation
- **Full session history sidebar** with search/filter, per-session delete, and quick-action cards
- **Custom avatar picker** — ~50 emoji avatars across five categories
- **Settings panel** covering voice, appearance, AI behavior, and data management
- **Keyboard shortcuts** — `Ctrl+K` to focus input, `Ctrl+F` to search, `Enter`/`Shift+Enter` for send/newline

---

## 🔐 Authentication

- JWT-based sessions (30-day expiry)
- Passwords hashed with `passlib`'s `sha256_crypt` scheme
- Guest mode supported — chat without an account, sign in anytime to start saving history
- Per-IP rate limiting (40 requests/minute) on AI endpoints

---

## 🛡️ Admin Control Panel

A completely custom-built Django admin system, branded to match the Sonic AI theme, connected directly to the same database the chat app uses — no syncing, no duplication, no separate source of truth.

### 🏠 Dashboard
- Total users, chat sessions, and message counts at a glance
- Live FastAPI backend status (online/offline ping)
- 14-day signup and message trend chart
- Global search bar across users, session titles, and message content
- Recent admin action feed

### 📊 Analytics
- Busiest-hours bar chart — see exactly when your users are most active
- Leaderboard ranking users by total messages sent
- Average messages-per-session calculation

### 🖥️ System
- Live status of required API keys (Groq, Tavily, JWT secret)
- Vectorstore status and on-disk size
- Document manager — view every uploaded file with one-click delete
- One-click full database backup download
- Quick links to the FastAPI root, Swagger docs, and the live chat app

### 🔒 Security
- Automatic content flagging — any chat session containing unsafe keywords surfaces here for review
- Failed login attempt tracking with 24-hour rolling counter
- Full audit trail of every admin action ever taken (who, what, when)

### User & session management
- Ban / unban users
- One-click password reset (generates and displays a new password once)
- Bulk-delete inactive users (no sessions, 30+ days old)
- Export any user or session list to CSV
- Read actual conversations rendered as chat bubbles — not raw JSON
- Tag and bookmark sessions for later reference
- Role-based access via Django Groups — give limited staff view-only permissions without full admin rights

---

## 🏗️ Architecture

```
┌─────────────────────┐         ┌──────────────────────┐
│   Sonic AI Frontend   │ ◄────► │   FastAPI Backend      │
│   (HTML/CSS/JS)        │         │   Port 8000             │
└─────────────────────┘         └───────────┬──────────┘
                                              │
                                  shared SQLite database
                                              │
                                  ┌───────────┴──────────┐
                                  │   Django Admin Panel    │
                                  │   Port 8001              │
                                  └──────────────────────┘
```

Both backends read and write to the **same** SQLite file. Django connects to FastAPI's existing tables using unmanaged models (`managed=False`), meaning it can query and update them freely without ever running a migration against them — FastAPI's schema stays completely untouched. Django owns two additional tables of its own (`AdminLog`, `FailedLoginDB`) for audit tracking, created through normal Django migrations.

---

## 🧰 Tech Stack

**Backend (FastAPI)**
- FastAPI + Uvicorn
- SQLAlchemy + SQLite
- LangChain + Groq (`llama-3.3-70b-versatile`)
- HuggingFace Embeddings (`all-MiniLM-L6-v2`)
- FAISS vector store
- Tavily Search API
- `python-jose` (JWT) + `passlib` (`sha256_crypt`)

**Frontend**
- Vanilla HTML/CSS/JS — zero frameworks, zero build step
- Web Speech API (voice input + text-to-speech)
- Tabler Icons + Google Fonts (Orbitron, Inter, JetBrains Mono)

**Admin Panel**
- Django 6
- Chart.js (analytics visualizations)
- Custom theme system layered over Django's default admin

---

## 🚀 Getting Started

### 1. Backend (FastAPI)

```bash
pip install fastapi uvicorn sqlalchemy passlib python-jose langchain-community langchain-huggingface langchain-groq langchain-text-splitters faiss-cpu python-dotenv httpx
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
SECRET_KEY=your_jwt_secret_here
```

Run it:

```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/chat` to use Sonic AI.

### 2. Admin Panel (Django)

```bash
cd sonic_admin
pip install django passlib
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

Visit `http://127.0.0.1:8001/admin/` and log in with the superuser you created.

> Both servers need to be running at the same time for the admin panel's live backend status check to show "online."

---

## 📂 Project Structure

```
project-root/
├── main.py                  # FastAPI backend
├── index.html                # Chat frontend (single file)
├── data/                      # Uploaded documents
├── vectorstore/               # FAISS index
├── sonic_ai.db                 # Shared SQLite database
└── sonic_admin/                # Django admin project
    ├── core/
    │   ├── models.py              # Shared + admin-owned models
    │   ├── admin.py                 # All admin logic, views, dashboards
    │   ├── static/admin/css/         # Custom neon theme
    │   └── templates/admin/           # Dashboard, Analytics, System, Security pages
    └── manage.py
```

---

## 🗺️ Roadmap / Ideas for later

- Live API key validation (ping Groq/Tavily, not just check `.env` presence)
- Avatar popularity breakdown chart
- Per-user drill-down view (session list + account age inline)
- One-click vectorstore rebuild trigger from the admin panel

---

Built as a hands-on exploration of full-stack AI application design — from prompt engineering and retrieval-augmented generation down to the operational tooling that keeps a real product running.
