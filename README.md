# AI Ticket Automation Agent

A local, privacy-friendly AI agent that triages customer support tickets — no API key, no cloud calls, no cost. Runs entirely on your machine using open-source transformer models.

## What it does

Given a batch of incoming customer messages, the agent automatically:

1. **Categorizes** each ticket — `Billing`, `Technical`, or `General`
2. **Flags urgency** — `Low`, `Medium`, or `High`
3. **Drafts a reply** based on the detected category and urgency

Results are printed to the console and saved to `automation_results.json` for downstream use (e.g. piping into Slack, email, or a helpdesk tool).

## Why local models?

Most AI automation demos rely on a paid API key (OpenAI, Anthropic, etc.). This version uses Hugging Face's `transformers` library with a zero-shot classification model, so it:

- Requires **no API key or account**
- Runs **fully offline** after the first model download
- Costs **nothing** to run, at any scale

This makes it a good starting point for prototyping — swap in a larger model or a hosted LLM API later once you need higher-quality generated replies.

## Tech stack

- Python
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- `valhalla/distilbart-mnli-12-3` — zero-shot classification model

## Setup

```bash
pip install transformers torch
python ai_ticket_automation.py
```

The first run downloads the classification model (~1GB, one-time, cached afterward). Subsequent runs are fast.

## Sample output

```
Ticket #1 - Alex R.
  Message : I was charged twice for my subscription this month. Can you fix this ASAP?
  Category: Billing
  Urgency : Medium
  Draft   : Thanks for flagging this - I can see this is a billing concern and I am looking into it right away. I will follow up shortly with next steps.
--------------------------------------------------
Ticket #2 - Priya S.
  Message : The app keeps crashing when I try to upload a file. Happens every time.
  Category: Technical
  Urgency : Low
  Draft   : Thanks for the report - I am looking into this technical issue now and will keep you posted on a fix.
```

## Customization

- Swap `incoming_messages` for real data pulled from a CSV, Google Sheet, or support inbox API
- Add more categories/urgency levels by editing `CATEGORY_LABELS` / `URGENCY_LABELS`
- Replace the template-based replies in `REPLY_TEMPLATES` with a call to an LLM API for fully generated responses

## Roadmap

- [ ] Connect directly to a live inbox (Gmail, Zendesk, Intercom)
- [ ] Add a Slack/Discord notification hook for high-urgency tickets
- [ ] Optional: swap in a larger LLM (local or hosted) for richer generated replies

## License

MIT
