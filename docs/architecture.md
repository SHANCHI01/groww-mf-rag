# Architecture
Ingest: load (requests+BeautifulSoup) -> section-aware chunk (700 chars, 100 overlap) -> embed (all-MiniLM-L6-v2, 384-d) -> ChromaDB (persisted in data/chroma).
Query: question -> guardrails -> memory rewrite (last 10 msgs) -> embed -> top-4 chunks (scheme-filtered if named) -> Groq LLM -> trim to 3 sentences -> append source link + last-updated.
Folders: src/ingest, src/rag, src/pages (Weekly Pulse), scripts, data (raw, chunks, chroma, pulse), docs.
Milestone 5 reuses retrieval so the fee explainer is grounded in the same corpus.
