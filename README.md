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
Me: I am feeling bored at home, provide me a list of places in bengaluru to chill out on a sunday.
ServifAI: Here is a list of places in Bengaluru to chill out on a Sunday:

1. Cubbon Park
2. Rasta Cafe
3. Skandagiri
4. Uttari Betta Sunrise
5. Ranganathaswamy Betta
6. Adventure Camping at Nandi Hills
7. Riverside Manchanabele
8. Caving at AntaraGange
9. Clubbing at Hard Rock Café
10. High Ultra lounge
11. Toit
12. Dinning at Empire Hotel

These are just a few options, and there are many more places in Bengaluru where you can relax and have a good time on a Sunday.

Me: Too many options for a day. Provide a itinerary instead for one day
ServifAI: Based on the search results, here is a suggested one-day itinerary for Bengaluru:

Morning: Start your day with a visit to Cubbon Park and enjoy the greenery. Join the locals on their early morning walk.

Afternoon: Indulge in a classic South Indian breakfast and then head to Savandurga, a famous place known for its temples and rock climbing.

Evening: Explore the vibrant streets of Bengaluru and visit popular spots like MG Road or Brigade Road for shopping and dining.

Night: End your day by experiencing the nightlife of Bengaluru at one of the city's popular clubs or lounges.

Please note that this is just a suggested itinerary and you can customize it based on your preferences and interests.

Me: Do you think this would be possible to complete based on today's weather?
ServifAI: Based on the weather forecast, it is possible to complete the activity you mentioned. The maximum temperature in Bengaluru is expected to be around 32 degrees Celsius today.

Me: exit
```

**Check [Examples](https://github.com/ZohebAbai/servifai/tree/main/examples) for more.**

# TODO:
- [x] Add support for popular unstructured data formats
- [ ] Add support for other VectorDBs
- [ ] Add other task based tools
- [ ] Add support for structured data formats
- [ ] Support for OpenAI funcs
