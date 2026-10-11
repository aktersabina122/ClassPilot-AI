from __future__ import annotations

import json
import os
import re
from datetime import date
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "classpilot_knowledge.json").read_text(encoding="utf-8"))
PROMPT = (ROOT / "prompts" / "system_prompt.txt").read_text(encoding="utf-8")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")
app = Flask(__name__)


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def choose_intent(question: str) -> dict | None:
    q = normalize(question)
    best, best_score = None, 0
    q_tokens = set(q.split())
    for intent in DATA["intents"]:
        score = 0
        for phrase in intent["phrases"]:
            p = normalize(phrase)
            if p and (p in q or q in p):
                score = max(score, 100 + len(p))
            else:
                p_tokens = set(p.split())
                # Token overlap is only a secondary fuzzy match. Require enough
                # shared words to avoid confusing unrelated student questions.
                overlap = len(q_tokens & p_tokens)
                if len(p_tokens) >= 2:
                    score = max(score, int(100 * overlap / len(p_tokens)))
        if score > best_score:
            best, best_score = intent, score
    return best if best_score >= 48 else None


def approved_context(intent: dict) -> dict:
    today = date.today().isoformat()
    assignments = DATA["assignments"]
    if intent["id"] == "next_deadline":
        upcoming = [a for a in assignments if a["status"] != "done" and a["due_date"] >= today]
        details = min(upcoming, key=lambda item: item["due_date"]) if upcoming else None
        return {"today": today, "assignment": details, "answer": DATA["no_upcoming"] if not details else None}
    if intent["id"] in {"all_assignments", "course_assignments"}:
        return {"today": today, "assignments": assignments}
    if intent["id"] == "study_plan":
        upcoming = sorted((a for a in assignments if a["status"] != "done" and a["due_date"] >= today), key=lambda x: x["due_date"])
        return {"today": today, "assignments": upcoming[:3], "study_advice": DATA["study_advice"]}
    if intent["id"] == "course_info":
        return {"course": DATA["course"], "assignments": assignments}
    if intent["id"] == "owner_identity":
        return {"app_identity": DATA["app_identity"]}
    if intent["id"] == "how_to_use":
        return {"help": DATA["help"]}
    return {"approved_answer": intent["answer"]}


def safe_fallback(intent: dict, context: dict) -> str:
    if intent["id"] == "next_deadline":
        item = context.get("assignment")
        if not item:
            return DATA["no_upcoming"]
        return f"Your next assignment is {item['title']} for {item['course']}, due {item['due_date']} ({item['due_time']})."
    if intent["id"] in {"all_assignments", "course_assignments"}:
        rows = context["assignments"]
        if not rows:
            return "There are no assignments in the sample schedule."
        return "Here are the assignments in the sample schedule:\n" + "\n".join(
            f"• {a['title']} — {a['course']}, due {a['due_date']} ({a['due_time']}); {a['status']}"
            for a in rows
        )
    if intent["id"] == "study_plan":
        rows = context["assignments"]
        if not rows:
            return DATA["no_upcoming"]
        return "Start with the earliest due item:\n" + "\n".join(
            f"{i}. {a['title']} — {a['course']}, due {a['due_date']}."
            for i, a in enumerate(rows, 1)
        ) + "\n" + DATA["study_advice"]
    if intent["id"] == "course_info":
        c = context["course"]
        return f"The demo course is {c['name']} ({c['code']}). {c['description']} Sample schedule: {len(context['assignments'])} assignments."
    if intent["id"] == "how_to_use":
        return DATA["help"]
    return intent["answer"]


@app.get("/")
def home():
    return render_template("index.html", model=OLLAMA_MODEL)


@app.get("/api/health")
def health():
    return jsonify(status="ok", model=OLLAMA_MODEL, data_file="data/classpilot_knowledge.json")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("message", "")).strip()[:1000]
    if not question:
        return jsonify(error="Please type a question first."), 400
    intent = choose_intent(question)
    if not intent:
        return jsonify(answer=DATA["fallback"], source="knowledge-base")
    context = approved_context(intent)
    approved_only = safe_fallback(intent, context)
    # The creator/owner answer is fixed, approved data. Return it directly so
    # a slow or unavailable local Ollama model cannot make this basic answer hang.
    if intent["id"] == "owner_identity":
        return jsonify(answer=approved_only, source="knowledge-base")
    messages = [
        {"role": "system", "content": PROMPT},
        {"role": "user", "content": (
            "APPROVED DATA (the only facts you may use):\n"
            + json.dumps(context, ensure_ascii=False)
            + "\n\nCUSTOMER QUESTION:\n" + question
        )},
    ]
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": OLLAMA_MODEL, "stream": False, "think": False,
                  "messages": messages, "options": {"temperature": 0, "num_predict": 180}},
            timeout=45,
        )
        response.raise_for_status()
        answer = response.json()["message"]["content"].strip()
        if not answer:
            raise ValueError("empty model response")
        return jsonify(answer=answer, source="ollama")
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return jsonify(answer=approved_only, source="knowledge-base")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
