# EmissionsTracker
A Python library that estimates the carbon emissions linked to cloud-based API services, such as AI cloud services, for demonstration purposes.

## Installation

To install the package, you can use `pip`, the Python package manager. Open a command line or terminal and run the following command:

```bash
pip install git+https://github.com/borisruf/emissions_tracker.git
```

## Usage

Once the package is installed, you can include and use it in your Python code as follows:

```python
import os
from mockai import MockAzureOpenAI
from emissions_tracker import APIEmissionsTracker

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

tracker = APIEmissionsTracker()
tracker.start()

client = MockAzureOpenAI(azure_endpoint=AZURE_ENDPOINT, api_key=OPENAI_API_KEY)

response = client.chat.completions.create(model=OPENAI_MODEL, messages=[{"role": "system", "content": "What is the origin of the Olympic Games?"}])

print(response)

tracker.stop()
```

Please note that this sample code uses the Python library [MockAI](https://github.com/borisruf/mockai/) to mimic the API requests for demonstration purposes. Currently, the supported models include `gpt-35-turbo` and `gpt-4`. The emission factors can be checked, changed and extended in [emission_factors.json](https://github.com/borisruf/mockai/blob/main/emissions_tracker/emission_factors.json).
