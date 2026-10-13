import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_DIR = str(DATA / "chroma")
COLLECTION = "hdfc_mf"
TOP_K = 4
MAX_DIST = 0.80          # cosine distance; above this = "not in my sources"
HISTORY_LIMIT = 10       # conversation memory window
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# key -> (display name, url, keywords used to detect which scheme a question is about)
AMC_URL = "https://groww.in/mutual-funds/amc/groww-mutual-funds"
SCHEMES = {
    "large_cap": ("Groww Large Cap Fund", "https://groww.in/mutual-funds/groww-large-cap-fund-direct-growth", ["large cap", "largecap", "large-cap"]),
    "elss": ("Groww ELSS Tax Saver Fund", "https://groww.in/mutual-funds/groww-elss-tax-saver-fund-direct-growth", ["elss", "tax saver", "lock-in", "lock in"]),
    "hybrid": ("Groww Aggressive Hybrid Fund", "https://groww.in/mutual-funds/groww-aggressive-hybrid-fund-direct-growth", ["hybrid", "aggressive"]),
    "value": ("Groww Value Fund", "https://groww.in/mutual-funds/groww-value-fund-direct-growth", ["value fund"]),
    "multicap": ("Groww Multicap Fund", "https://groww.in/mutual-funds/groww-multicap-fund-direct-growth", ["multicap", "multi cap", "multi-cap"]),
}
