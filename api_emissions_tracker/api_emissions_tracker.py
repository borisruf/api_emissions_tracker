from wrapt import wrap_function_wrapper
from mockai import MockAzureOpenAI
from openai import AzureOpenAI
from openai.resources.chat import Completions
import json
import warnings
import os

class APIEmissionsTracker:
    def __init__(self):
        MockAzureOpenAI.tracker = self
        self.emissions = 0.0

    def start(self):
        # Start tracking emissions
        self.tracking = True

    def stop(self):
        # Stop tracking emissions
        if hasattr(self, 'tracking') and self.tracking:  # Check if tracking was started
            self.log_emission()
        self.tracking = False

    def add_emissions(self, amount):
        if hasattr(self, 'tracking') and self.tracking:
            self.emissions += amount

    def log_emission(self):
        # Plot the emission value and any relevant details
        print("emissions:", self.emissions, "g CO2e")
        print(f"Compare: https://borisruf.github.io/carbon-footprint-modeling-tool/search.html?value={self.emissions}&mass_unit=g&emission_type=co2e")

    def approximate_emissions(model, prompt_tokens, completion_tokens):
        path = os.path.join(os.path.dirname(__file__), 'emission_factors.json')
        with open(path, "r") as file:
            emission_factors = json.load(file)

            if model in emission_factors:
                return prompt_tokens*emission_factors[model]['per_prompt_token'] + completion_tokens*emission_factors[model]['per_completion_token']
            else:
                warnings.warn(f"No emission data available for the AI model '{model}'")
                return 0

############ MockAI

def _new_create_mock_azure_open_ai(model, messages, temperature=1, max_tokens=16, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
    
    # Call the original method to keep the old code
    response = MockAzureOpenAI.chat._original_create(model, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop)
    
    if response:
        # Collect meta data
        model = response.model
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        # Calculate emissions
        amount = APIEmissionsTracker.approximate_emissions(model, prompt_tokens, completion_tokens)
        MockAzureOpenAI.tracker.add_emissions(amount)

        return response

    else:
        return None


# Store the original method
MockAzureOpenAI.chat._original_create = MockAzureOpenAI.chat.completions.create

# Monkey patch the method of the MockAzureOpenAI class
MockAzureOpenAI.chat.completions.create = _new_create_mock_azure_open_ai


############ AzureOpenAI

def azure_openai_chat_wrapper(
    wrapped,
    instance: Completions,
    args,
    kwargs
):
    response = wrapped(*args, **kwargs)
    # Add code to run after the create method of OpenAI was executed
    if response:
        # Collect meta data
        model = response.model
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        # Calculate emissions
        amount = APIEmissionsTracker.approximate_emissions(model, prompt_tokens, completion_tokens)
        MockAzureOpenAI.tracker.add_emissions(amount)

        return response

    else:
        return None

class AzureOpenAIInstrumentor:
    def __init__(self):
        self.wrapped_methods = [
            {
                "module": "openai.resources.chat.completions",
                "name": "Completions.create",
                "wrapper": azure_openai_chat_wrapper,
            },
        ]

    def instrument(self):
        for wrapper in self.wrapped_methods:
            wrap_function_wrapper(
                wrapper["module"], wrapper["name"], wrapper["wrapper"]
            )


# instantiating the instrumentor
instrumentor = AzureOpenAIInstrumentor()
instrumentor.instrument()