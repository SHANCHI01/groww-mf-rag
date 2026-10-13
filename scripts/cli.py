"""python -m scripts.cli  -> test retrieval + answers in the terminal."""
from src.rag.pipeline import answer
hist = []
while True:
    q = input("\nQ> ").strip()
    if not q: break
    r = answer(q, hist)
    print(r["answer"], "\nSource:", r["source"], "| refused:", r["refused"])
    for c in r["chunks"]: print(f"  - {c['meta']['section']} (dist {c['dist']:.2f})")
    hist += [{"role": "user", "content": q}, {"role": "assistant", "content": r["answer"]}]
