"""
AI Support Ticket Automation Agent (Local, No API Key Required)
"""
import json
from transformers import pipeline

print("Loading local AI model... (first run may take a minute)\n")

classifier = pipeline(
    "zero-shot-classification",
    model="valhalla/distilbart-mnli-12-3",
)

CATEGORY_LABELS = ["Billing", "Technical", "General"]
URGENCY_LABELS = ["Low urgency", "Medium urgency", "High urgency"]

REPLY_TEMPLATES = {
    "Billing": "Thanks for flagging this - I can see this is a billing concern and I am looking into it right away. I will follow up shortly with next steps.",
    "Technical": "Thanks for the report - I am looking into this technical issue now and will keep you posted on a fix.",
    "General": "Thanks so much for reaching out - really appreciate you taking the time to share this with us!",
}

URGENCY_PREFIX = {
    "High": "[Priority] ",
    "Medium": "",
    "Low": "",
}


def generate_reply(category, urgency):
    base_reply = REPLY_TEMPLATES.get(category, REPLY_TEMPLATES["General"])
    prefix = URGENCY_PREFIX.get(urgency, "")
    return prefix + base_reply


incoming_messages = [
    {"id": 1, "customer": "Alex R.", "message": "I was charged twice for my subscription this month. Can you fix this ASAP?"},
    {"id": 2, "customer": "Priya S.", "message": "The app keeps crashing when I try to upload a file. Happens every time."},
  
]


def analyze_message(message):
    category_result = classifier(message, CATEGORY_LABELS)
    category = category_result["labels"][0]

    urgency_result = classifier(message, URGENCY_LABELS)
    urgency = urgency_result["labels"][0].replace(" urgency", "")

    draft_reply = generate_reply(category, urgency)

    return {"category": category, "urgency": urgency, "draft_reply": draft_reply}


def run_automation():
    results = []
    print("Running AI Ticket Automation Agent (local models)...\n" + "-" * 50)

    for ticket in incoming_messages:
        analysis = analyze_message(ticket["message"])
        result = {"id": ticket["id"], "customer": ticket["customer"], "message": ticket["message"]}
        result.update(analysis)
        results.append(result)

        print("Ticket #" + str(ticket["id"]) + " - " + ticket["customer"])
        print("  Message : " + ticket["message"])
        print("  Category: " + result["category"])
        print("  Urgency : " + result["urgency"])
        print("  Draft   : " + result["draft_reply"])
        print("-" * 50)

    with open("automation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nDone! Results saved to automation_results.json")


if __name__ == "__main__":
    run_automation()
