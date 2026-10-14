# ClearPulse — Groww Customer Insights & Weekly Product Pulse

**Milestone 5 | Product Management Fellowship**

ClearPulse is a prototype for analysing Groww customer reviews, identifying recurring customer concerns, preparing a weekly product pulse, and explaining transaction charges using official source links.

**Live dashboard:** https://shanchi01.github.io/groww-mf-rag/

**GitHub repository:** https://github.com/SHANCHI01/groww-mf-rag

## Key Features

- Weekly product pulse with customer quotes, insights, and proposed actions.
- Exploratory review analysis to identify potential fee-transparency concerns.
- Facts-focused fee explainer with source links and a last-checked date.
- Local approval workflow that appends a JSONL notes entry and creates an unsent email draft.
- Static dashboard published using GitHub Pages.

## Project Structure

- `site/template.html` — dashboard interface template.
- `scripts/build_site.py` — builds the static dashboard.
- `scripts/approve_and_log.py` — requests local approval before saving notes and replacing the email draft.
- `docs/index.html` — generated dashboard published through GitHub Pages.
- `deliverables/weekly_pulse.md` — weekly product pulse.
- `deliverables/fee_explainer.md` — transaction-charge explanation.
- `deliverables/notes_entry.jsonl` — saved notes history.
- `deliverables/email_draft.eml` — local email draft; it is not sent.
- `sources.csv` — project source list, where available.

## Setup and Run Locally

Requirements: Python 3.10 or later.

From the repository root, run:

```powershell
python .\scripts\build_site.py
Start-Process .\docs\index.html
```

The first command regenerates the static dashboard. The second opens it in your browser.

## Approval Workflow

Run:

```powershell
python .\scripts\approve_and_log.py
```

Review the weekly pulse and fee explainer. Type `APPROVE` when prompted to append a notes entry and replace the local email draft. Any other response cancels the operation.

**No email is sent.** This implementation uses a local Python approval prompt; it is not a live MCP server or MCP integration.

## Exploratory Findings

The current analysis used 10,000 Groww reviews from an exploratory dataset without review dates. A keyword filter identified 428 reviews mentioning fee-related terms; 289 of those had ratings of 1 or 2.

Three illustrative customer comments are included in the weekly pulse. These counts are exploratory and are not validated theme classifications.

**Data limitation:** The required 8–12-week review window has not been verified. Do not interpret these findings as a date-bounded weekly trend or proof of incorrect billing.

## Fee Transparency Issue

Some customer comments describe difficulty understanding brokerage and other transaction deductions. The prototype proposes auditing the transaction-level breakdown and validating explanations against official pricing information.

The fee explainer links to:

- https://groww.in/pricing
- https://groww.in/help/stocks/searchable/when-are-dp-charges-levied

Verify applicable rates and conditions against the official sources before relying on them.

## Known Limitations

- The current review dataset does not establish an 8–12-week date range.
- Keyword-based review counts are exploratory, not manually validated classifications.
- The approval workflow is local; the dashboard does not execute server-side approval actions.
- The email draft is a local `.eml` file and is not a Gmail or other mail-provider draft.
- The static dashboard displays saved results; it does not fetch new reviews automatically.

## Disclaimer

This prototype is for product research and educational demonstration. Customer complaints indicate reported experiences and do not establish incorrect billing. Fee details can change; verify current terms using the linked official sources.