"""Milestone 5: reviews -> themes -> weekly pulse -> fee explainer (grounded in the M4 RAG corpus)
-> approval gate -> notes append + email draft (no auto-send)."""
import json, re, datetime
import pandas as pd, streamlit as st
from src.config import DATA
from src.rag import llm
from src.rag.retrieve import retrieve

st.title("Weekly Product Pulse + Fee Explainer")
PULSE = DATA / "pulse"; PULSE.mkdir(parents=True, exist_ok=True)
ADVICE = ["you should", "i recommend", "we recommend", "buy ", "sell ", "best fund", "guaranteed"]

def jload(t): return json.loads(re.sub(r"```json|```", "", t).strip())

def analyze(df):
    sample = "\n".join(f"- {t[:200]}" for t in df["text"].dropna().head(120))
    for _ in range(3):
        try:
            out = jload(llm.chat("You analyse app reviews. Return ONLY JSON.",
                'Cluster into max 5 themes. Return {"themes":[{"name":"","count":0,"summary":""}],"top3":["","",""],'
                '"quotes":["","",""],"fee_issue":{"name":"","confusion":""}}. Quotes VERBATIM from reviews. '
                "fee_issue = ONE recurring confusion about a fee/charge.\n\nREVIEWS:\n" + sample, 900))
            corpus = " ".join(df["text"].dropna()).lower()
            out["quotes"] = [q for q in out["quotes"] if q.lower().strip(' ."') in corpus][:3]
            return out
        except Exception: continue
    raise RuntimeError("Model returned invalid JSON 3 times. Try again.")

def pulse(ins):
    for _ in range(3):
        t = llm.chat("Write a structured internal weekly product note. Max 250 words.",
                     "Sections: Top themes, Supporting quotes, Key observation, 3 action ideas.\n" + json.dumps(ins), 500)
        if len(t.split()) <= 250: return t
    return " ".join(t.split()[:250])

def explainer(ins):
    fi = ins["fee_issue"]
    chunks = retrieve(f"{fi['name']} {fi['confusion']}", k=6)
    links = list(dict.fromkeys(c["meta"]["source_url"] for c in chunks))[:2]
    ctx = "\n\n".join(c["text"] for c in chunks)
    t = llm.chat("Facts-only, neutral tone. Use ONLY the context. No advice.",
                 f"Explain this fee confusion: {json.dumps(fi)}\nMax 6 bullets, each starting with '- '. No links.\n\nCONTEXT:\n{ctx}", 400)
    bullets = [b for b in t.splitlines() if b.strip().startswith("-")][:6]
    return bullets, links, f"Last checked: {datetime.date.today():%d %b %Y}"

def run_evals(ins, p, bullets, links, checked, df):
    corpus = " ".join(df["text"].dropna()).lower(); text = (p + " " + " ".join(bullets)).lower()
    return {"Pulse <= 250 words": len(p.split()) <= 250,
            "3 quotes, verbatim in CSV": len(ins["quotes"]) == 3,
            "Max 5 themes": len(ins["themes"]) <= 5,
            "Explainer <= 6 bullets": 0 < len(bullets) <= 6,
            "Exactly 2 source links": len(links) == 2,
            "'Last checked' present": checked.startswith("Last checked:"),
            "No advice language": not any(a in text for a in ADVICE)}

def tool_append_notes(entry):
    with open(PULSE / "notes.jsonl", "a") as f: f.write(json.dumps(entry) + "\n")
    return "Appended to data/pulse/notes.jsonl"

def tool_create_email_draft(subject, body):
    (PULSE / "email_draft.eml").write_text(f"Subject: {subject}\nX-Unsent: 1\n\n{body}")
    return "Draft saved to data/pulse/email_draft.eml (NOT sent)"

up = st.file_uploader("Reviews CSV (date, rating, text)", type="csv")
if up: pd.read_csv(up).to_csv(PULSE / "reviews.csv", index=False)
if not (PULSE / "reviews.csv").exists():
    st.info("Run `python -m scripts.fetch_reviews` or upload a CSV."); st.stop()
df = pd.read_csv(PULSE / "reviews.csv"); st.caption(f"{len(df)} reviews loaded")

if st.button("Generate insights"):
    ins = analyze(df); st.session_state["pz"] = (ins, pulse(ins), *explainer(ins))

if "pz" in st.session_state:
    ins, p, bullets, links, checked = st.session_state["pz"]
    st.subheader("Weekly pulse"); st.write(p)
    st.subheader(f"Fee explainer: {ins['fee_issue']['name']}")
    st.write("\n".join(bullets)); st.write(links); st.caption(checked)
    ev = run_evals(ins, p, bullets, links, checked, df)
    st.subheader("Eval checks")
    st.table(pd.DataFrame({"Check": list(ev), "Result": ["PASS" if v else "FAIL" for v in ev.values()]}))
    entry = {"date": str(datetime.date.today()), "top_themes": ins["top3"], "weekly_pulse": p,
             "identified_fee_issue": ins["fee_issue"]["name"], "explanation_bullets": bullets,
             "source_links": links, "evals": ev}
    subject = "Weekly Product Pulse + Customer Clarification — " + ins["fee_issue"]["name"]
    body = f"{p}\n\nSupport snippet:\n" + "\n".join(bullets) + f"\n{links}\n{checked}"
    st.warning("Approval required. Pending: (1) append to notes, (2) create email draft. Nothing is auto-sent.")
    if st.button("✅ Approve & run"):
        st.success(tool_append_notes(entry)); st.success(tool_create_email_draft(subject, body))
