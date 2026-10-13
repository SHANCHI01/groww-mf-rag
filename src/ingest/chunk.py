"""Phase 2b: section-aware chunking.
Strategy: pages are short, structured fact sheets (Min SIP, Expense ratio, Exit load, Benchmark...).
Split on section headings first so a fact never gets cut away from its label, then cap size at
700 chars with 100 chars overlap. Each chunk is prefixed '[Scheme | Section]' so retrieval matches
scheme names. Metadata: scheme_key, scheme, section, source_url, chunk_id, char_count."""
from src.config import DATA, SCHEMES

SIZE, OVERLAP = 700, 100

def split(text):
    if len(text) <= SIZE: return [text]
    parts, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > SIZE and cur:
            parts.append(cur)
            cur = cur[-OVERLAP:] + "\n" + line
        else:
            cur = (cur + "\n" + line) if cur else line
    if cur: parts.append(cur)
    return parts

def chunk_all(loaded):
    chunks = []
    for key, secs in loaded.items():
        name, url, _ = SCHEMES[key]
        for head, body in secs:
            for piece in split(body):
                text = f"[{name} | {head}]\n{piece}"
                chunks.append({"id": f"{key}-{len(chunks)}", "text": text,
                               "meta": {"scheme_key": key, "scheme": name, "section": head,
                                        "source_url": url, "char_count": len(text)}})
    out = DATA / "chunks"; out.mkdir(parents=True, exist_ok=True)
    with open(out / "chunks.txt", "w", encoding="utf-8") as f:
        for i, c in enumerate(chunks, 1):
            f.write(f"=== CHUNK {i} | {c['meta']['scheme']} | {c['meta']['section']} | {c['meta']['char_count']} chars ===\n"
                    f"{c['meta']['source_url']}\n{c['text']}\n\n")
    print(f"{len(chunks)} chunks -> data/chunks/chunks.txt")
    return chunks
