
from pathlib import Path
import json
import re
from email import policy
from email.parser import Parser

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"
OUTPUT = ROOT / "docs" / "index.html"
DELIVERABLES = ROOT / "deliverables"


def main():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE}")

    notes_path = DELIVERABLES / "notes_entry.jsonl"
    pulse_path = DELIVERABLES / "weekly_pulse.md"
    fee_path = DELIVERABLES / "fee_explainer.md"
    email_path = DELIVERABLES / "email_draft.eml"

    for path in (notes_path, pulse_path, fee_path, email_path):
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

    # Load the most recent saved notes entry.
    entries = [
        json.loads(line)
        for line in notes_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not entries:
        raise ValueError("notes_entry.jsonl contains no entries.")

    entry = entries[-1]

    pulse = pulse_path.read_text(encoding="utf-8").strip()
    fee_text = fee_path.read_text(encoding="utf-8").strip()

    # Extract the fee explanation bullets and source URLs.
    bullets = re.findall(r"(?m)^-\s+(.+)$", fee_text)
    sources_section = fee_text.split("Sources:", 1)
    source_links = (
        re.findall(r"https?://\S+", sources_section[1].split("Last checked:", 1)[0])
        if len(sources_section) > 1 else []
    )

    # Parse the saved email draft without sending it.
    email = Parser(policy=policy.default).parsestr(
        email_path.read_text(encoding="cp1252")
    )
    email_body = email.get_body(preferencelist=("plain",))
    body = email_body.get_content() if email_body else ""

    data = {
        "date": entry.get("date", "Date unavailable"),
        "range": entry.get("date", "Date unavailable"),
        "review_count": 50,
        "top_themes": entry.get("top_themes", []),
        "weekly_pulse": pulse,
        "identified_fee_issue": entry.get(
            "identified_fee_issue", "Fee issue"
        ),
        "explanation_bullets": bullets[:6],
        "source_links": source_links[:2],
        "entry": entry,
        "email_subject": email.get("Subject", "Weekly Product Pulse"),
        "email_body": body,
        "evals": entry.get("evals", {}),
    }

    template = TEMPLATE.read_text(encoding="utf-8")
    marker = "/*__DATA__*/null"

    if marker not in template:
        raise ValueError(
            "Template data placeholder not found. "
            "Expected /*__DATA__*/null"
        )

    # Safely serialize data for embedding in JavaScript.
    embedded = json.dumps(data, ensure_ascii=False)
    embedded = (
        embedded.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )

    page = template.replace(marker, embedded, 1)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")

    print(f"Built {OUTPUT}")
    print(f"Loaded {len(entries)} saved notes entries.")
    print(f"Dashboard review count: {data['review_count']}")
    print("Original deliverables were not modified.")


if __name__ == "__main__":
    main()
