# Groww MF Facts-Only RAG Assistant + Weekly Pulse (Milestones 4 & 5)

**Scope:** AMC = Groww Mutual Fund; 5 schemes (Large Cap, ELSS, Aggressive Hybrid, Value, Multicap), Direct-Growth. Sources: see `sources.csv` (5 Groww pages).
**Disclaimer in UI:** Facts-only. No investment advice.

## Setup
1. Python 3.10+, then `pip install -r requirements.txt`
2. `cp .env.example .env` and add `GROQ_API_KEY` (console.groq.com/keys). Pick a current `GROQ_MODEL` from console.groq.com/docs/models.
3. Ingest once: `python -m src.ingest.run` (writes data/raw, data/chunks/chunks.txt, data/embeddings_preview.txt, data/chroma)
4. Test in terminal: `python -m scripts.cli`
5. Run UI: `python -m streamlit run src/app.py` (Weekly Pulse is the second page in the sidebar)
6. Sample Q&A: `python -m scripts.make_sample_qa` (creates SAMPLE_QA.md)

## Milestone 5: Weekly Pulse
`python -m scripts.fetch_reviews` -> open the Weekly Pulse page -> Generate insights -> Approve & run.
- MCP-style approval gate: tools `append_to_notes` and `create_email_draft` run only after clicking Approve. Email is a draft, never sent.
- The fee explainer is retrieved from the same ChromaDB corpus, so it is grounded in the 5 source pages.
- 7 eval checks are shown in the UI and saved with each notes entry.
- Fee issue identified from reviews: _fill in after your run_.

## Deploy on Render (Web Service)
Root Directory: (blank) | Build: `pip install -r requirements.txt && python -m src.ingest.run` | Start: `python -m streamlit run src/app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` | Env: GROQ_API_KEY, GROQ_MODEL

## Known limits
- Only the 5 pages are indexed; questions like "how to download a capital-gains statement" return "I don't know" plus the Groww AMC page link.
- Groww pages are third-party aggregator pages (the course brief's chosen corpus); figures change daily, hence "Last updated from sources".
- Page layout changes can affect cleaning in `src/ingest/load.py`; check `data/chunks/chunks.txt` after ingesting.
- Educational links in refusals (SEBI/AMFI roots) should be checked by you before submission.
