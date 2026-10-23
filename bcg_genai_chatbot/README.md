# Financial chatbot prototype

BCG GenAI job simulation, Task 2. Elliott Randall, October 2026.

## What it does

This is a command-line chatbot that answers five types of question about Apple, Microsoft and Tesla. It uses the figures from their 2023–2025 10-K filings that I collected and analysed in Task 1 (`financial_data.csv`).

## Files

- `chatbot.py`: the chatbot
- `financial_data.csv`: the Task 1 dataset (USD millions)
- `test_chatbot.py`: runs 14 test questions and checks the answers
- `test_results.txt`: the output of the last test run
- `README.md`: this file

## How to run it

You need Python 3 and pandas. Keep `financial_data.csv` in the same folder as `chatbot.py`.

```
python chatbot.py
```

Type a question and press Enter. Type `help` to see examples and `quit` to exit. To run the tests:

```
python test_chatbot.py
```

## How it works

1. On start-up, the script reads `financial_data.csv` into a dictionary keyed by company and year.
2. When you type a question, it's converted to lower case and checked for a company name or ticker (e.g. "tesla" or "tsla") and a year. If no company is named, the bot answers for all three and says which one comes out top. If no year is given, it uses 2025.
3. An if/elif chain looks for keywords to work out which question was asked. For example, "margin" or "profitable" leads to the profit margin answer, and "revenue" or "sales" leads to the revenue answer. Anything that doesn't match gets a fallback reply.
4. Each answer is a fixed template filled in with figures from the dataset, so the numbers and percentage changes always match the data. I wrote no numbers into the responses by hand.
5. Where the raw numbers would mislead, the bot adds a short note. These come from my Task 1 analysis: Apple's one-off EU tax charge in FY2024, Tesla's one-off tax benefit in 2023, and Apple's high liabilities, which mostly reflect share buybacks.

Answers also give each company's financial year end, because Microsoft's year ends in June, Apple's in September and Tesla's in December.

## Questions it can answer

1. **What is the total revenue?** Revenue for the year and the change on the year before.
2. **How has net income changed over the last year?** The change in net income, with any one-off items flagged.
3. **What is the profit margin?** (also "Which company is the most profitable?") Net income as a share of revenue.
4. **How much cash did they generate from operations?** Operating cash flow and the change on the year before.
5. **What are the total liabilities?** Total liabilities and their share of total assets.

Each can be narrowed to a company, a year, or both, e.g. "What was Tesla's revenue in 2024?"

## Example

```
You: How has Apple's net income changed over the last year?
Bot: Apple's net income rose 19.5%, from $93.7bn in FY2024 to $112.0bn in FY2025 (year to 27 Sep 2025).
       Note: this jump is flattered by the one-off tax charge of about $10.2bn in FY2024. Without it, growth was about 8%.
```

## Testing

`test_chatbot.py` asks 14 questions and checks that each answer contains the expected figure or phrase. The questions cover all five question types, specific companies and years, a comparison between two companies, a year with no previous year to compare against (2023), a year outside the data (2021), an off-topic question and the help command. All 14 pass. The full transcript is in `test_results.txt`.

## Limitations

- Keyword matching is brittle. The bot doesn't understand language, it only spots words. "How much did Apple sell?" gets the fallback reply because it contains neither "revenue" nor "sales", and a question about two topics at once only gets an answer to the first one it matches.
- "Debt" is treated as total liabilities, which also includes things like money owed to suppliers and deferred revenue, not just borrowing.
- Narrow coverage. It only knows five metrics, for three companies, over three years.
- The context notes are written by hand. They only cover the one-off items I found in Task 1, so the bot can't flag anything else unusual.
- Different financial years. A "2025" comparison across the three companies covers different 12-month periods. The bot shows each year end but doesn't adjust for it.
- Static data. New filings would have to be added to the CSV manually.

## What I'd do next

Replace the if/elif matching with a language model (e.g. Google Gemini) that is given the dataset and the context notes with each question. It could then handle questions phrased any way, while its answers stay tied to the real figures.
