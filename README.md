# ServifAI

*A mini framework built on top of Langchain and Llamaindex to provide LLM powered Autonomous Agents as a simplified service to assist users with their tasks.*

![PyPI](https://img.shields.io/github/license/zohebabai/servifai)
![PyPI](https://img.shields.io/pypi/v/servifai)

## Overview

**ServifAI (Task-based Agent) = LLM + Memory + Planning + Toolbox**

![agent_pic](https://lilianweng.github.io/posts/2023-06-23-agent/agent-overview.png)

Instead of feeding all kinds of tools to a single agent and confusing it while selection, **ServifAI** narrows down the selection by combining only necessary tools on basis of the task at hand.

Read [this article to understand How Agents works](https://lilianweng.github.io/posts/2023-06-23-agent/). 

By default, **ServifAI** can chat while browsing internet and solving common math problems.

### Current Toolbox Status:
- Default (DuckDuckgo + LLM Math + PAL Math)
- QA Knowledge Base (Vector Index + Knowledge Graphs)

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
    response = myagent.query(text_input)
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
- Create a config YAML file `uber_10q.yaml` inside a `configs` dir and fill details as:
```yaml
task: 'qa_knowledge_base'

vectordb:
  dir: "uber_10q"

data:
  dir: "reports"
  about: "Uber 10Q Filing"

text:
  max_input_size: 2500
  num_outputs: 1000
  max_chunk_overlap: 0.05
  chunk_size_limit: 1000

llm:
  org: openai
  temperature: 0
  model_name: "gpt-3.5-turbo"
```
- As the task is to extract information from these pdfs, so task chosen is `qa_knowledge_base`. Based on these tasks we choose our *toolbox* which contains specific tools required for task completion. We will be adding more *toolbox*.
- To achieve optimum results, its recommended to rename your pdfs as *few words description*. For example, we rename quarterly 10Q reports as `Q1-23.pdf`, `Q4-22.pdf` etc. Do not add blank spaces between words, instead use `hyphen -`. 
- Also in config file in `data.about`, provide a concise common summary of all these multiple pdfs. For example, here we write this as `Uber 10Q Filing`.
- Run Python Code
```python
from servifai import ServifAI
myagent = ServifAI('configs/uber_10q.yaml')

while True:
    text_input = input("Me: ")
    response = myagent.query(text_input)
    print(f'ServifAI: {response}\n')
```
- Output
```
Me: Analyze the revenue growth of Uber across quarters
ServifAI: Based on the provided context information, the revenue growth of Uber across quarters can be summarized as follows:

- Q3 2022: Revenue growth of 72% year-over-year or 81% on a constant currency basis.
- Q4 2022: Revenue growth of 59% on a constant currency basis, significantly outpacing the 19% growth in Gross Bookings.
- Q1 2023: Revenue of $8.8 billion is mentioned, but the growth rate for this quarter is not provided.

Therefore, the specific revenue growth rate for Q1 2023 cannot be determined with the given information.

Me: How much cash did Uber have in last quarter of 2022?
ServifAI: Based on the provided context, the cash balance for Uber at the end of Q4 2022 was $4.3 billion.

```

# TODO:
- [ ] Add other task based tools
- [ ] Add support for Local LLMs
- [ ] Add support for other VectorDBs
- [ ] Add support for other unstructured data
- [ ] Add support for structured data 
- [ ] OpenAI funcs
