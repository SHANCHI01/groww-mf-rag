"""python -m scripts.make_sample_qa -> writes SAMPLE_QA.md with real answers + links."""
from src.rag.pipeline import answer
QS = ["What is the expense ratio of Groww Large Cap Fund?", "What is the minimum SIP for Groww Multicap Fund?",
      "What is the lock-in for Groww ELSS Tax Saver Fund?", "What is the exit load of Groww Value Fund?",
      "What is the benchmark of Groww Aggressive Hybrid Fund?", "What is the riskometer level of Groww Value Fund?",
      "How do I download my capital gains statement?", "Should I buy Groww Value Fund?",
      "Which fund gave better returns, large cap or multicap?", "My PAN is ABCDE1234F, check my account"]
with open("SAMPLE_QA.md", "w", encoding="utf-8") as f:
    f.write("# Sample Q&A\n\n")
    for q in QS:
        r = answer(q)
        f.write(f"**Q:** {q}\n\n**A:** {r['answer']}\n\n**Link:** {r['source']}  \n*Type: {r['refused'] or 'answered'}*\n\n---\n\n")
print("wrote SAMPLE_QA.md")
