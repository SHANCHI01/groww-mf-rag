"""Phase 5a: embed the question with the SAME model, fetch top-k chunks, plus keyword rescue."""
import chromadb
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from src.config import EMB_MODEL, CHROMA_DIR, COLLECTION, TOP_K, SCHEMES

# question word -> exact label that appears in the page text
KEYWORDS = {"lock": "Lock-in", "benchmark": "benchmark", "exit load": "Exit load",
            "expense": "Expense ratio", "sip": "SIP", "risk": "risk"}

@lru_cache(maxsize=1)
def _model(): return SentenceTransformer(EMB_MODEL)

@lru_cache(maxsize=1)
def _col(): return chromadb.PersistentClient(path=CHROMA_DIR).get_collection(COLLECTION)

def detect_scheme(q):
    ql = q.lower()
    hits = [k for k, (_, _, kws) in SCHEMES.items() if any(w in ql for w in kws)]
    return hits[0] if len(hits) == 1 else None

def _pack(r, cap=None):
    return [{"text": d, "meta": m, "dist": (min(s, cap) if cap is not None else s)}
            for d, m, s in zip(r["documents"][0], r["metadatas"][0], r["distances"][0])]

def retrieve(q, k=TOP_K):
    vec = _model().encode([q], normalize_embeddings=True).tolist()
    key = detect_scheme(q)
    where = {"scheme_key": key} if key else None
    found = _pack(_col().query(query_embeddings=vec, n_results=k, where=where))
    ql = q.lower()
    for word, term in KEYWORDS.items():
        if word in ql:
            try:
                r = _col().query(query_embeddings=vec, n_results=2, where=where,
                                 where_document={"$contains": term})
                seen = {c["text"] for c in found}
                extra = [c for c in _pack(r, cap=0.3) if c["text"] not in seen]  # exact-label hit counts as relevant
                found = extra + found
            except Exception:
                pass
            break
    return found[:k + 2]