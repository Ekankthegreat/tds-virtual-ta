# app/qa_engine.py
import json
from difflib import get_close_matches

def get_answer(question: str) -> str:
    # your logic here, for now you can just return dummy
    return "This is a placeholder answer for: " + question


# Load course site content
try:
    with open("app/data/tds_content.json", encoding="utf-8") as f:
        TDS_CONTENT = json.load(f)
except:
    TDS_CONTENT = []

# Load Discourse posts
try:
    with open("app/data/discourse.json", encoding="utf-8") as f:
        discourse_raw = json.load(f)
        # Extract all text content from each post
        DISCOURSE_CONTENT = [
            post.get("title", "") + " " + post.get("content", "")
            for post in discourse_raw
            if isinstance(post, dict)
        ]
except:
    DISCOURSE_CONTENT = []

# Combine both
ALL_CONTENT = TDS_CONTENT + DISCOURSE_CONTENT

def answer_question(question: str) -> str:
    matches = get_close_matches(question, ALL_CONTENT, n=1, cutoff=0.1)
    if matches:
        return matches[0]
    return "Sorry, I couldn't find a relevant answer from the course content or Discourse posts."
