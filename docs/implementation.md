# Implementation phases
1. Setup: requirements.txt, folders, .gitignore, .env.example. Verify: `pip install -r requirements.txt`.
2. Load & chunk: src/ingest/load.py, chunk.py. Verify: data/raw/*.txt and data/chunks/chunks.txt exist.
3. Embed & store: embed_store.py. Verify: "stored N vectors"; restart and re-query without re-ingesting.
4. Guardrails: src/rag/guardrails.py. Verify: advice, PII, performance questions are refused.
5. Retrieval + LLM: retrieve.py, llm.py, pipeline.py, scripts/cli.py. Verify: `python -m scripts.cli`.
6. UI: src/app.py (+ src/pages/2_Weekly_Pulse.py). Verify: `python -m streamlit run src/app.py`.
