# BCG GenAI job simulation (Forage)

My work for the BCG GenAI job simulation on Forage, October 2026. This was a job simulation, not employment with BCG.

## Task 1: financial data analysis

I took five figures (total revenue, net income, total assets, total liabilities and operating cash flow) from the 2023–2025 10-K filings of Apple, Microsoft and Tesla on SEC EDGAR. I then analysed them in a Jupyter notebook with pandas: year-on-year growth for each metric, plus net margin, liabilities to assets and operating cash flow to net income.

- `BCG_GenAI_financial_analysis.ipynb`: the notebook (the `.html` version can be read in a browser without Python)
- `BCG_GenAI_financial_data.xlsx` and `financial_data.csv`: the data, in USD millions

Main findings:

- Microsoft grew revenue about 15% a year, and its net margin rose from 34% to 36%.
- Apple's revenue grew slowly (about 4% a year), but its profits are large and stable once a one-off $10.2bn EU tax charge in FY2024 is taken out.
- Tesla's revenue was flat while its net margin fell from 15.5% to 4.0%.

## Task 2: chatbot prototype

A command-line chatbot that answers five types of question about the three companies, using the Task 1 data. It's rule-based (keyword matching with if/elif) and adds a short note where the raw numbers would mislead, such as one-off tax items.

See [`bcg_genai_chatbot/README.md`](bcg_genai_chatbot/README.md) for how it works, how to run it, the test results and its limitations.
