"""Phase 4: guardrails. Returns (kind, message, link) if the question must be refused, else None."""
import re

AMFI = "https://www.amfiindia.com/investor-corner"
SEBI = "https://investor.sebi.gov.in/"
from src.config import AMC_URL
HDFC = AMC_URL  # scheme/factsheet hub for the chosen AMC

PII = [r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", r"\b\d{4}\s?\d{4}\s?\d{4}\b", r"[\w.+-]+@[\w-]+\.[\w.]+",
       r"\b(?:\+?91[- ]?)?[6-9]\d{9}\b", r"\botp\b", r"\bpan\b|\baadhaar\b|\baadhar\b|account number"]
ADVICE = [r"\bshould i\b", r"\b(buy|sell|hold|switch)\b", r"\bis it (good|safe|worth)\b", r"\bbest (fund|scheme)\b",
          r"\bwhich (fund|scheme) (is|should)\b", r"\brecommend", r"\bbetter than\b", r"\bgood investment\b"]
PERF = [r"\breturns?\b", r"\bcagr\b", r"\boutperform", r"\bperformance\b", r"\bprofit\b", r"\bcompare\b"]

def _hit(patterns, q, flags=re.I):
    return any(re.search(p, q, flags) for p in patterns)

def check(q):
    if any(re.search(p, q) for p in PII[:2]) or _hit(PII[2:], q):
        return ("pii", "Please don't share personal details such as PAN, Aadhaar, account numbers, OTPs, emails or phone numbers. I don't need them and can't store them.", SEBI)
    if _hit(ADVICE, q):
        return ("advice", "I can only share facts from official scheme pages, so I can't say whether to buy, sell or pick a fund. This guide explains how to evaluate mutual funds.", SEBI)
    if _hit(PERF, q):
        return ("performance", "I don't compute or compare returns. Please see the official factsheet for performance data.", HDFC)
    return None
