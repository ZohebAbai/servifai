# ServifAI

*A mini framework built on top of Langchain and Llamaindex to provide LLM powered Autonomous Agents as a simplified service to assist users with their tasks.*

![PyPI](https://img.shields.io/github/license/zohebabai/servifai)
![PyPI](https://img.shields.io/pypi/v/servifai)

## Overview

**ServifAI (Task-based Agent) = LLM + Memory + Planning + Toolbox**

![agent_pic](https://lilianweng.github.io/posts/2023-06-23-agent/agent-overview.png)

Instead of feeding all kinds of tools to a single agent and confusing it while selection, **ServifAI** narrows down the selection by combining only necessary tools on basis of the task at hand.

Read [this article to get an overview on Agents](https://lilianweng.github.io/posts/2023-06-23-agent/). 

### Current Supported Tasks:
|  Tasks | Toolbox Tools |
| :------ | :---------------: |
| `default` | DuckDuckGo + LLM Math + PAL Math |
| `qna_local_docs` | Vector Index + Knowledge Graphs |


## Installation
Works best with [Poetry](https://python-poetry.org/docs/)
```bash
poetry add servifai
```
With pip, you might have to install dependencies manually
```bash
pip install servifai
```

## Usage
Create a `.env` file
```env
OPENAI_API_KEY='sk-...'
```

Run Python Code
```python
from servifai import ServifAI
myagent = ServifAI()

while True:
    text_input = input("Me: ")
    if text_input == "exit":
        break
    response = myagent.chat(text_input)
    print(f'ServifAI: {response}\n')
```
Output
```
Me: Hi, How are you?
ServifAI: Hi, I'm an AI language model, so I don't have feelings, but I'm here to help you with any questions or tasks you have!

Me: What is the current weather of Bengaluru?
ServifAI: The current weather in Bengaluru is mostly cloudy with a temperature of 81°F (27°C). The wind is coming from the north at 3 mph (5 km/h). Tomorrow's temperature is expected to be nearly the same as today.

```
## Data Creation Recipe for Local Knowledge Extraction Tasks
Consider the example of [Uber 10Q filings](https://investor.uber.com/financials/default.aspx). 
- Download the quaterly reports for year 2022 and 2023 as pdf and save it locally in a directory (here `reports`).
- Create a config YAML file `uber10q.yaml` inside a `configs` dir and fill details as:
```yaml
task: qna_local_docs

llm:
  org: openai
  model: gpt-3.5-turbo
  temperature: 0
  max_tokens: 3000

data:
  dir: reports
  about: "Uber 10Q Filing"

memory:
  dir: uber_10q
  max_input_size: 2500
  num_outputs: 1000
  max_chunk_overlap: 0.05
  chunk_size_limit: 1000
```
- As the task is to extract information from these pdfs, so task chosen is `qna_local_docs`. Based on these tasks ServifAI chooses *toolbox* which contains specific tools required for task completion. We will be adding more *toolbox* later.
- To achieve optimum results, its recommended to rename your pdfs as *few words description*. For example, we rename quarterly 10Q reports as `Q1-23.pdf`, `Q4-22.pdf` etc. Do not add blank spaces between words, instead use `hyphen -`. 
- Also in config file in `data.about`, provide a concise common summary of all these multiple pdfs. For example, here we write this as `Uber 10Q Filing`.
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
- Output
```
Me: Analyze the revenue growth of Uber across last few quarters
ServifAI: Based on the provided context, Uber's revenue growth in the last few quarters can be summarized as follows:

- Q3 2022: 72% year-over-year or 81% on a constant currency basis.
- Q4 2022: 49% year-over-year.
- Q1 2023: 29% year-over-year or 33% on a constant currency basis.

Therefore, Uber's revenue growth in the last few quarters has been positive, with varying rates of growth.

Me: How much cash did Uber have in last quarter of 2022?
ServifAI: Based on the provided context, the cash balance for Uber in Q4 2022 was $4.3 billion.

```

# TODO:
- [ ] Add other task based tools
- [ ] Add support for Local LLMs
- [ ] Add support for other VectorDBs
- [ ] Add support for other unstructured data
- [ ] Add support for structured data 
- [ ] OpenAI funcs
