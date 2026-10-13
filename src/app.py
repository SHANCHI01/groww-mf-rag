import streamlit as st
from src.rag.pipeline import answer
        r = answer(q, hist)
from src.config import HISTORY_LIMIT

st.set_page_config(page_title="Groww MF Facts Assistant", page_icon="📊")
st.title("Groww Mutual Fund Facts Assistant")
st.write("Hi! Ask me factual questions about 5 Groww Mutual Fund schemes: Large Cap, ELSS, Aggressive Hybrid, Value, Multicap.")
st.caption("Facts-only. No investment advice.")

EXAMPLES = ["What is the expense ratio of Groww Large Cap Fund?", "What is the minimum SIP for Groww ELSS Tax Saver Fund?", "What is the exit load of Groww Value Fund?"]
if "msgs" not in st.session_state: st.session_state.msgs = []
cols = st.columns(3)
clicked = None
for c, e in zip(cols, EXAMPLES):
    if c.button(e, use_container_width=True): clicked = e
if st.sidebar.button("Clear chat"): st.session_state.msgs = []; st.rerun()

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m.get("chunks"):
            with st.expander("Sources"):
                for c in m["chunks"]: st.caption(f"{c['meta']['scheme']} · {c['meta']['section']}"); st.text(c["text"][:300])

q = st.chat_input("Ask a factual question...") or clicked
if q:
    hist = [{"role": m["role"], "content": m["content"]} for m in st.session_state.msgs][-HISTORY_LIMIT:]
    st.session_state.msgs.append({"role": "user", "content": q})
    try:
        r = answer(q, hist)
        txt = f"{r['answer']}\n\n🔗 Source: {r['source']}\n\n_Last updated from sources: {r['updated']}_"
    except Exception as e:
        r, txt = {"chunks": []}, f"Sorry, something went wrong: {e}"
    st.session_state.msgs.append({"role": "assistant", "content": txt, "chunks": r["chunks"]})
    st.rerun()
