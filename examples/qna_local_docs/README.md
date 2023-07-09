# Local Docs Knowledge Extraction Tasks
## Steps to follow:
Consider the example of [Uber 10Q filings](https://investor.uber.com/financials/default.aspx). 
    - Download the quaterly reports pdf files for year 2022 and 2023 and save it locally in a directory (here `reports`).
- For optimal results, it is recommended to rename your PDFs using a concise description about the file. For instance, you can rename quarterly 10Q reports as `Q1-23.pdf`, `Q4-22.pdf`, and so on. Please avoid using spaces between words and instead use a hyphen `-` to separate them.
- Create a config YAML file `uber10q.yaml` inside a `configs` dir.
- In the configuration file, under the `data.about` section, please provide a concise summary that represents the content of all the documents. For instance, you can use a summary like `Uber 10Q Filing` to describe the nature of the documents.
- As the task is to extract information from these pdfs, so task chosen is `qna_local_docs`. Based on these tasks ServifAI chooses *toolbox* which contains specific tools required for task completion. We will be adding more *toolbox* later.
- Run Python Code
```python
from servifai import ServifAI
myagent = ServifAI('configs/uber10q.yaml')

while True:
    text_input = input("Me: ")
    if text_input == "exit":
        break
    response = myagent.chat(text_input)
    print(f'ServifAI: {response}\n')
```

### Output
```
Me: Analyze the revenue growth of Uber across last few quarters
ServifAI: Based on the provided context, Uber's revenue growth in the last few quarters can be summarized as follows:

- Q3 2022: 72% year-over-year or 81% on a constant currency basis.
- Q4 2022: 49% year-over-year.
- Q1 2023: 29% year-over-year or 33% on a constant currency basis.

Therefore, Uber's revenue growth in the last few quarters has been positive, with varying rates of growth.

Me: How much cash did Uber have in last quarter of 2022?
ServifAI: Based on the provided context, the cash balance for Uber in Q4 2022 was $4.3 billion.

Me: exit
```
