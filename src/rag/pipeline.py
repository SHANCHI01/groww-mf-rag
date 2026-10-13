"""Phase 5b: guardrails -> (memory rewrite) -> retrieve -> LLM -> post-process."""
import json, re
from src.config import DATA, MAX_DIST, HISTORY_LIMIT, AMC_URL
from src.rag import guardrails, llm
from src.rag.retrieve import retrieve

SYSTEM = ("You are a facts-only mutual fund FAQ assistant. Answer ONLY from the CONTEXT. "
          "Max 3 sentences. No investment advice, no return comparisons. "
          "If the context does not contain the answer, reply exactly: I don't know based on the sources I have.")

def last_updated():
    try: return json.loads((DATA / "meta.json").read_text())["last_updated"]
    except Exception: return "unknown"

def rewrite(q, history):
    if not history: return q
    h = "\n".join(f"{m['role']}: {m['content']}" for m in history[-HISTORY_LIMIT:])
    return llm.chat("Rewrite the last user question as a standalone question using the chat history. Output only the question.",
                    f"HISTORY:\n{h}\n\nQUESTION: {q}", 80)

def trim(text, n=3):
    s = re.split(r"(?<=[.!?])\s+", text.strip())
    return " ".join(s[:n])

def answer(q, history=()):
    g = guardrails.check(q)
    if g:
        kind, msg, link = g
        return {"answer": msg, "source": link, "refused": kind, "chunks": [], "updated": last_updated()}
    standalone = rewrite(q, list(history))
    chunks = retrieve(standalone)
    if not chunks or chunks[0]["dist"] > MAX_DIST:
        return {"answer": "I don't know based on the sources I have.", "source": AMC_URL,
                "refused": "no_context", "chunks": chunks, "updated": last_updated()}
    ctx = "\n\n".join(c["text"] for c in chunks)
    text = trim(llm.chat(SYSTEM, f"CONTEXT:\n{ctx}\n\nQUESTION: {standalone}"))
    if text.lower().startswith("i don't know"):
        return {"answer": text, "source": AMC_URL, "refused": "no_context",
                "chunks": chunks, "updated": last_updated()}
    return {"answer": text, "source": chunks[0]["meta"]["source_url"], "refused": None,
            "chunks": chunks, "updated": last_updated()}
