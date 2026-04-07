# AI Clinical Copilot

A RAG-powered AI assistant for clinical documentation — built with FastAPI, Next.js, OpenAI GPT-4o, and Pinecone.

Upload clinical notes and ask questions, generate summaries, or produce structured SOAP notes.

---

## Architecture

```
User → Next.js UI → FastAPI → Agent Orchestrator
                                    ↓
                            Retrieval Layer (Pinecone)
                                    ↓
                           Clinical Documents (chunks)
```

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.11 |
| LLM | OpenAI GPT-4o |
| Embeddings | text-embedding-3-small |
| Vector DB | Pinecone |
| Containerization | Docker / docker-compose |

---

## Getting Started

### 1. Clone and configure

```bash
git clone https://github.com/YOUR_USERNAME/ai-clinical-copilot.git
cd ai-clinical-copilot

cp .env.example .env
# Fill in your OPENAI_API_KEY and PINECONE_API_KEY
```

### 2. Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000

### 4. Or run both with Docker

```bash
docker-compose up --build
```

---

## Project Structure

```
ai-clinical-copilot/
├── backend/
│   └── app/
│       ├── api/routes/       # chat, ingest, health endpoints
│       ├── agents/           # clinical agent + tools
│       ├── services/         # RAG, embedding, agent orchestration
│       ├── db/               # Pinecone vector store wrapper
│       └── utils/            # chunking, formatting
├── frontend/
│   ├── app/                  # Next.js pages
│   ├── components/           # ChatWindow, MessageBubble, UploadPanel
│   └── lib/api.ts            # typed API client
└── data/
    └── sample_clinical_notes/
```

---

## Build Phases

| Phase | Status | Description |
|---|---|---|
| 1 — Foundation | ✅ Complete | FastAPI + Next.js scaffold, stub endpoints |
| 2 — RAG Pipeline | 🔲 Next | Pinecone ingestion, chunking, retrieval |
| 3 — Agent Layer | 🔲 Planned | GPT-4o tool use, SOAP generation |
| 4 — Streaming UI | 🔲 Planned | Real-time token streaming |
| 5 — Polish | 🔲 Planned | README, demo, architecture diagram |

---

## Sample Usage (Phase 3+)

Upload `sample_note_001.txt`, then ask:

- *"Summarize this visit in 2 sentences"*
- *"Generate a SOAP note"*
- *"What medications was the patient on?"*
- *"What was the assessment?"*

---

## Author

Christopher Crumley — [LinkedIn](#) | [GitHub](#)
