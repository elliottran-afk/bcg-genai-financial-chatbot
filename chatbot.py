"""
Financial chatbot prototype (BCG GenAI job simulation, Task 2)

Answers five predefined types of question about Apple, Microsoft and Tesla,
using the 10-K figures collected and analysed in Task 1 (financial_data.csv).

Run:   python chatbot.py
Type 'help' for example questions and 'quit' to exit.
"""

import os
import re

import pandas as pd

# The CSV sits next to this script, so the bot works from any folder.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financial_data.csv")

# Names and tickers the bot recognises for each company.
COMPANIES = {
    "Apple": ["apple", "aapl"],
    "Microsoft": ["microsoft", "msft"],
    "Tesla": ["tesla", "tsla"],
}

# Each company's financial year ends on a different date, so answers say which period they cover.
YEAR_END = {
    "Apple": {2023: "30 Sep 2023", 2024: "28 Sep 2024", 2025: "27 Sep 2025"},
    "Microsoft": {2023: "30 Jun 2023", 2024: "30 Jun 2024", 2025: "30 Jun 2025"},
    "Tesla": {2023: "31 Dec 2023", 2024: "31 Dec 2024", 2025: "31 Dec 2025"},
}

# Context the raw numbers don't show, taken from the Task 1 analysis.
# Keyed by (company, year, topic). A year of None means the note applies to every year.
NOTES = {
    ("Apple", 2024, "net income"): (
        "Note: FY2024 included a one-off tax charge of about $10.2bn (the EU ruling on "
        "Apple's Irish taxes). Without it, net income would have grown about 7%."
    ),
    ("Apple", 2025, "net income"): (
        "Note: this jump is flattered by the one-off tax charge of about $10.2bn in FY2024. "
        "Without it, growth was about 8%."
    ),
    ("Tesla", 2024, "net income"): (
        "Note: 2023 profit included a one-off tax benefit of about $5.9bn. "
        "Without it, the fall would have been about 22%."
    ),
    ("Apple", None, "liabilities"): (
        "Note: this is high mainly because Apple spends heavily buying back its own shares, "
        "which shrinks equity. It isn't a sign of financial trouble."
    ),
}

HELP = """I can answer these questions about Apple, Microsoft and Tesla (2023 to 2025):
  1. What is the total revenue?
  2. How has net income changed over the last year?
  3. What is the profit margin?  (or: Which company is the most profitable?)
  4. How much cash did they generate from operations?
  5. What are the total liabilities?
Name a company and/or a year to narrow it down, e.g. "What was Tesla's revenue in 2024?"
If you don't name a company, I'll answer for all three."""


# ---------- Loading the data ----------

def load_data(path):
    """Read the Task 1 CSV into a dictionary keyed by (company, year)."""
    df = pd.read_csv(path)
    data = {}
    for row in df.to_dict("records"):
        data[(row["Company"], int(row["Year"]))] = row
    return data


try:
    DATA = load_data(DATA_FILE)
except FileNotFoundError:
    raise SystemExit("Couldn't find financial_data.csv. Put it in the same folder as chatbot.py.")

YEARS = sorted({year for _, year in DATA})
LATEST = YEARS[-1]


# ---------- Small helpers ----------

def bn(millions):
    """Format a figure in $ millions as billions, e.g. 416161 -> '$416.2bn'."""
    return f"${millions / 1000:,.1f}bn"


def short(company, year):
    """'FY2025' for Apple and Microsoft, '2025' for Tesla (calendar year)."""
    return str(year) if company == "Tesla" else f"FY{year}"


def period(company, year):
    """Year label with the year-end date, e.g. 'FY2025 (year to 27 Sep 2025)'."""
    if company == "Tesla":
        return str(year)
    return f"FY{year} (year to {YEAR_END[company][year]})"


def find_companies(text):
    """Companies mentioned in the question. If none are named, use all three."""
    found = [name for name, aliases in COMPANIES.items() if any(a in text for a in aliases)]
    return found if found else list(COMPANIES)


def find_year(text):
    """First year mentioned in the question, or the latest year if none is given."""
    match = re.search(r"20\d{2}", text)
    return int(match.group()) if match else LATEST


def change(company, year, column):
    """Percentage change on the previous year, or None if the data has no previous year."""
    previous = DATA.get((company, year - 1))
    if previous is None:
        return None
    return (DATA[(company, year)][column] / previous[column] - 1) * 100


def note(company, year, topic):
    """Context note for this answer, if there is one."""
    return NOTES.get((company, year, topic)) or NOTES.get((company, None, topic))


# ---------- Building the answers ----------

def figure_answer(column, label, companies, year):
    """Revenue and operating cash flow: the figure plus its change on the year before."""
    lines = []
    for c in companies:
        line = f"{c}'s {label} in {period(c, year)} was {bn(DATA[(c, year)][column])}"
        pct = change(c, year, column)
        if pct is not None:
            line += f", {'up' if pct >= 0 else 'down'} {abs(pct):.1f}% on the year before"
        lines.append(line + ".")
    if len(companies) > 1:
        top = max(companies, key=lambda c: DATA[(c, year)][column])
        lines.append(f"Highest: {top}.")
    return "\n".join(lines)


def net_income_answer(companies, year):
    """How net income changed on the previous year, with any one-off items flagged."""
    lines = []
    for c in companies:
        now = DATA[(c, year)]["Net Income"]
        previous = DATA.get((c, year - 1))
        if previous is None:
            lines.append(
                f"{c}'s net income in {period(c, year)} was {bn(now)}. "
                f"My data starts in {YEARS[0]}, so I can't show the change."
            )
            continue
        pct = change(c, year, "Net Income")
        verb = "rose" if pct >= 0 else "fell"
        lines.append(
            f"{c}'s net income {verb} {abs(pct):.1f}%, from {bn(previous['Net Income'])} "
            f"in {short(c, year - 1)} to {bn(now)} in {period(c, year)}."
        )
        extra = note(c, year, "net income")
        if extra:
            lines.append("  " + extra)
    return "\n".join(lines)


def margin_answer(companies, year):
    """Net profit margin = net income / revenue."""
    lines = []
    margins = {}
    for c in companies:
        row = DATA[(c, year)]
        margins[c] = row["Net Income"] / row["Total Revenue"] * 100
        lines.append(
            f"{c}'s net profit margin in {period(c, year)} was {margins[c]:.1f}% "
            f"({bn(row['Net Income'])} of net income on {bn(row['Total Revenue'])} of revenue)."
        )
    if len(companies) > 1:
        lines.append(f"Most profitable: {max(margins, key=margins.get)}.")
    return "\n".join(lines)


def liabilities_answer(companies, year):
    """Total liabilities and what share of total assets they make up."""
    lines = []
    ratios = {}
    for c in companies:
        row = DATA[(c, year)]
        ratios[c] = row["Total Liabilities"] / row["Total Assets"] * 100
        lines.append(
            f"{c}'s total liabilities on {YEAR_END[c][year]} were {bn(row['Total Liabilities'])}, "
            f"{ratios[c]:.1f}% of its {bn(row['Total Assets'])} of total assets."
        )
        extra = note(c, year, "liabilities")
        if extra:
            lines.append("  " + extra)
    if len(companies) > 1:
        lines.append(f"Lowest share of assets: {min(ratios, key=ratios.get)}.")
    return "\n".join(lines)


# ---------- The chatbot ----------

def simple_chatbot(user_query):
    """Match the question to one of the predefined query types and return the answer."""
    q = user_query.lower()
    companies = find_companies(q)
    year = find_year(q)

    if year not in YEARS:
        return f"Sorry, I only have data for {YEARS[0]} to {YEARS[-1]}."

    if "help" in q:
        return HELP
    elif "margin" in q or "profitable" in q:
        return margin_answer(companies, year)
    elif "income" in q or "profit" in q or "earnings" in q:
        return net_income_answer(companies, year)
    elif "revenue" in q or "sales" in q or "growth" in q:
        return figure_answer("Total Revenue", "total revenue", companies, year)
    elif "cash" in q:
        return figure_answer("Cash Flow from Operating Activities", "operating cash flow", companies, year)
    elif "liabilit" in q or "debt" in q or "leverage" in q:
        return liabilities_answer(companies, year)
    else:
        return (
            "Sorry, I can only answer questions about revenue, net income, profit margin, "
            "operating cash flow and liabilities for Apple, Microsoft and Tesla. "
            "Type 'help' to see examples."
        )


def main():
    print("Financial chatbot: Apple, Microsoft and Tesla, 2023 to 2025 (from 10-K filings).")
    print("Type 'help' for example questions or 'quit' to exit.\n")
    while True:
        try:
            user_query = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user_query:
            continue
        if user_query.lower() in ("quit", "exit", "bye"):
            break
        answer = simple_chatbot(user_query)
        print("Bot: " + answer.replace("\n", "\n     ") + "\n")
    print("Bye.")


if __name__ == "__main__":
    main()
