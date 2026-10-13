"""Phase 2a: download the 5 public pages and save cleaned text to data/raw/."""
import re, requests
from bs4 import BeautifulSoup
from src.config import DATA, SCHEMES

UA = {"User-Agent": "Mozilla/5.0 (class-project RAG; facts-only)"}
SKIP = ("return calculator", "returns and rankings", "compare", "holdings", "fund management")
STOP = ("Download the App", "© 20", "Show More", "Others:", "Mutual Funds:")

def fetch_sections(url):
    html = requests.get(url, headers=UA, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style", "head", "noscript", "svg"]):
        t.decompose()
    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""
    heads = {h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3", "h4", "h5"])}
    lines = [re.sub(r"\s+", " ", l).strip() for l in soup.get_text("\n").split("\n")]
    lines = [l for l in lines if l]
    if title in lines:                      # drop the site menu above the fund title
        lines = lines[lines.index(title):]
    sections, cur, buf = [], "Overview", []
    for l in lines:
        if l.startswith(STOP): break
        if l in heads:
            if buf: sections.append((cur, buf))
            cur, buf = l, []
        elif "Also manages" not in l:
            buf.append(l)
    if buf: sections.append((cur, buf))
    return [(h, "\n".join(b)) for h, b in sections if not any(s in h.lower() for s in SKIP)]

def run():
    out = {}
    for key, (name, url, _) in SCHEMES.items():
        secs = fetch_sections(url)
        (DATA / "raw").mkdir(parents=True, exist_ok=True)
        text = "\n\n".join(f"## {h}\n{b}" for h, b in secs)
        (DATA / "raw" / f"{key}.txt").write_text(f"SOURCE: {url}\n\n{text}", encoding="utf-8")
        out[key] = secs
        print(f"loaded {name}: {len(secs)} sections")
    return out
