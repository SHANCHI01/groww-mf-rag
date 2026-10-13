"""Phase 3: embed chunks (all-MiniLM-L6-v2, 384-d) and persist them in ChromaDB."""
import json, datetime, chromadb
from sentence_transformers import SentenceTransformer
from src.config import DATA, EMB_MODEL, CHROMA_DIR, COLLECTION

def embed_and_store(chunks):
    model = SentenceTransformer(EMB_MODEL)
    vecs = model.encode([c["text"] for c in chunks], normalize_embeddings=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try: client.delete_collection(COLLECTION)
    except Exception: pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
    col.add(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks],
            embeddings=vecs.tolist(), metadatas=[c["meta"] for c in chunks])
    with open(DATA / "embeddings_preview.txt", "w") as f:
        for c, v in list(zip(chunks, vecs))[:5]:
            f.write(f"{c['id']} (dim={len(v)}): {[round(float(x), 4) for x in v[:10]]}\n")
    (DATA / "meta.json").write_text(json.dumps({"last_updated": datetime.date.today().strftime("%d %b %Y")}))
    print(f"stored {col.count()} vectors in {CHROMA_DIR}")
