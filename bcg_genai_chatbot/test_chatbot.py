"""
Tests the chatbot against a fixed set of questions and saves the transcript.

Run:   python test_chatbot.py
Each answer is checked for a piece of text it must contain. Results go to test_results.txt.
"""

import os
from datetime import date

from chatbot import simple_chatbot

# (question, text the answer must contain)
TESTS = [
    ("What is the total revenue?", "Apple's total revenue in FY2025 (year to 27 Sep 2025) was $416.2bn"),
    ("What was Tesla's revenue in 2024?", "$97.7bn, up 0.9%"),
    ("How has net income changed over the last year?", "Tesla's net income fell 46.5%"),
    ("How has Apple's net income changed over the last year?", "one-off tax charge"),
    ("Did Tesla's profit change in 2024?", "Without it, the fall would have been about 22%"),
    ("Which company is the most profitable?", "Most profitable: Microsoft"),
    ("What is Tesla's profit margin?", "4.0%"),
    ("How much cash did Microsoft generate from operations?", "$136.2bn, up 14.9%"),
    ("What are Apple's total liabilities?", "buying back its own shares"),
    ("Compare liabilities for Microsoft and Tesla in 2023", "Lowest share of assets: Tesla"),
    ("How did Microsoft's net income change in 2023?", "can't show the change"),
    ("What was Microsoft's revenue in 2021?", "only have data for 2023 to 2025"),
    ("What's the weather like?", "Sorry, I can only answer"),
    ("help", "What is the total revenue?"),
]


def run_tests():
    lines = [f"Chatbot test results ({date.today():%d %b %Y})", ""]
    passed = 0
    for i, (question, expected) in enumerate(TESTS, start=1):
        answer = simple_chatbot(question)
        ok = expected in answer
        passed += ok
        lines.append(f"Test {i}: {'PASS' if ok else 'FAIL'}")
        lines.append(f"You: {question}")
        lines.append("Bot: " + answer.replace("\n", "\n     "))
        if not ok:
            lines.append(f"     (expected to contain: {expected})")
        lines.append("")
    lines.append(f"{passed} of {len(TESTS)} tests passed.")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nSaved to {out}")


if __name__ == "__main__":
    run_tests()
