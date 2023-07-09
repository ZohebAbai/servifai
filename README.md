# ServifAI

*A mini framework built on top of Langchain and Llamaindex to provide LLM powered Autonomous Agents as a simplified service to assist users with their tasks.*

![PyPI](https://img.shields.io/github/license/zohebabai/servifai)
![PyPI](https://img.shields.io/pypi/v/servifai)

## Overview

**ServifAI (Task-based Agent) = LLM + Memory + Planning + Toolbox**

![agent_pic](https://lilianweng.github.io/posts/2023-06-23-agent/agent-overview.png)

Instead of feeding all kinds of tools to a single agent and confusing it while selection, **ServifAI** narrows down the selection by combining only necessary tools on basis of the task at hand.

Read [this article to get an overview on Agents](https://lilianweng.github.io/posts/2023-06-23-agent/). 

Currently we only support `OpenAI` models. If you are privacy concerned you should apply for `Azure OpenAI` services. The reason for not yet supporting `opensource local` models are:
- You need a lot of money - either to buy a great GPU or host it on cloud with a great GPU
- even if you tick the first point, it won't help you much as currently opensource models are good for chat but lag behind `OpenAI` models in enabling complex agent workflows

### Current Supported Tasks:
|  Tasks | Toolbox Tools | Required File Extensions |
| :------ | :---------------: | ------: |
| `default` | DuckDuckGo + LLM Math + PAL Math | None |
| `qna_local_docs` | Vector Index + Knowledge Graphs | `PDF`/`DOCX` |


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
Create a `.env` file for openai
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

**Check [Examples](https://github.com/ZohebAbai/servifai/tree/main/examples) for more.**

# TODO:
- [x] Add support for popular unstructured data formats
- [ ] Add support for other VectorDBs
- [ ] Add other task based tools
- [ ] Add support for structured data formats
- [ ] Support for OpenAI funcs
