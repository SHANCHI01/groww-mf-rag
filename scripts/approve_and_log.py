
from pathlib import Path
from datetime import date
from email.message import EmailMessage
import json
import re

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLES = ROOT / "deliverables"

PULSE = DELIVERABLES / "weekly_pulse.md"
FEE = DELIVERABLES / "fee_explainer.md"
NOTES = DELIVERABLES / "notes_entry.jsonl"
EMAIL = DELIVERABLES / "email_draft.eml"


def main():
    pulse = PULSE.read_text(encoding="utf-8-sig").strip()
    fee = FEE.read_text(encoding="utf-8-sig").strip()

    print("\nCLEARPULSE APPROVAL")
    print("This appends one notes entry and replaces the local email draft.")
    print("The email will NOT be sent.\n")
    print("Weekly pulse preview:\n")
    print(pulse)
    print("\nFee explainer preview:\n")
    print(fee)

    approval = input("\nType APPROVE to continue: ").strip()
    if approval != "APPROVE":
        print("Cancelled. No files were changed.")
        return

    bullets = []
    for line in fee.splitlines():
        cleaned = line.strip()
        cleaned = cleaned.replace("\\-", "-")
        if cleaned.startswith("- "):
            bullet = cleaned[2:].strip()
            bullet = re.sub(r"\\?\*{2}", "", bullet)
            bullets.append(bullet)

    sources = []
    for line in fee.splitlines():
        match = re.search(r"https://\S+", line)
        if match:
            sources.append(match.group(0).rstrip(".,)"))

    entry = {
        "date": date.today().isoformat(),
        "top_themes": [
            "Transaction-charge transparency",
            "Positive user experience",
            "Performance and stability"
        ],
        "weekly_pulse": pulse,
        "identified_fee_issue": "Transaction-charge transparency",
        "explanation_bullets": bullets[:6],
        "source_links": sources[:2]
    }

    with NOTES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    msg = EmailMessage()
    msg["Subject"] = "ClearPulse Weekly Product Pulse"
    msg["To"] = "product-team@example.com"
    msg["X-Unsent"] = "1"
    msg.set_content(
        "Weekly Product Pulse\n\n"
        + pulse
        + "\n\nFee explainer\n\n"
        + fee
    )
    EMAIL.write_bytes(msg.as_bytes())

    print("\nApproval recorded.")
    print(f"Notes appended to: {NOTES}")
    print(f"Unsent email draft saved to: {EMAIL}")
    print("No email was sent.")


if __name__ == "__main__":
    main()
