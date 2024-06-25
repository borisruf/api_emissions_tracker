# API Emissions Tracker
A Python library that estimates the carbon emissions linked to cloud-based API services, such as AI cloud services, for demonstration purposes.

## Installation

To install the package, you can use `pip`, the Python package manager. Open a command line or terminal and run the following command:

```bash
pip install git+https://github.com/borisruf/api_emissions_tracker.git
```

## Usage

Once the package is installed, you can include and use it in your Python code.

__Sample code:__
```python
from mockai import AzureOpenAI
from api_emissions_tracker import APIEmissionsTracker

AZURE_ENDPOINT = "[YOUR_AZURE_ENDPOINT]"
OPENAI_MODEL = "gpt-35-turbo"   # specify a supported model from the list
OPENAI_API_KEY = "[YOUR_OPENAI_API_KEY]"

tracker = APIEmissionsTracker()
tracker.start()

client = AzureOpenAI(azure_endpoint=AZURE_ENDPOINT, api_key=OPENAI_API_KEY)

response = client.chat.completions.create(model=OPENAI_MODEL, messages=[{"role": "system", "content": "What is the origin of the Olympic Games?"}])

print(response.choices)

tracker.stop()
```

__Sample output:__
```bash
[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='The Olympic Games originated in ancient Greece around the 8th century BCE. They were held in Olympia, a small town in the western region of the Peloponnese. The Games were a religious festival dedicated to the Greek god Zeus and were held every four years. The first recorded Olympic Games took place in 776 BCE, and they continued for nearly 12 centuries until they were abolished in 393 CE by the Christian Byzantine Emperor Theodosius I.', role='assistant', function_call=None, tool_calls=None), content_filter_results={'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}})]
emissions: 0.26814 g CO2e
```

For demonstration purposes you can also uses the Python library [MockAI](https://github.com/borisruf/mockai/) which mimics the API requests. Simply replace the following lines:

```python
from mockai import MockAzureOpenAI
...
client = MockAzureOpenAI(azure_endpoint=AZURE_ENDPOINT, api_key=OPENAI_API_KEY)
```

The emission factors can be checked, changed and extended in [emission_factors.json](https://github.com/borisruf/mockai/blob/main/emissions_tracker/emission_factors.json).


## Tutorials
- [Jupyter notebook](https://github.com/borisruf/api_emissions_tracker/blob/main/notebooks/RemoteCodeEmissions.ipynb) for estimating carbon emissions of __remotely__ executed code [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/borisruf/remotecodeemissions)
- [Jupyter notebook](https://github.com/borisruf/api_emissions_tracker/blob/main/notebooks/LocalCodeEmissions.ipynb) for estimating carbon emissions of __locally__ executed code [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/borisruf/localcodeemissions)
