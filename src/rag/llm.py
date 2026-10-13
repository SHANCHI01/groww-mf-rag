import os, re
from groq import Groq
from src.config import GROQ_MODEL

def chat(system, user, max_tokens=300):
    key = os.getenv("GROQ_API_KEY")
    if not key: raise RuntimeError("GROQ_API_KEY missing. Add it to .env (local) or Render env vars.")
    r = Groq(api_key=key).chat.completions.create(
        model=GROQ_MODEL, temperature=0, max_tokens=max(max_tokens, 1500),
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}])
    return re.sub(r"<think>.*?</think>", "", r.choices[0].message.content, flags=re.S).strip()
