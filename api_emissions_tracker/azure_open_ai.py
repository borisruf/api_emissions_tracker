from openai import AzureOpenAI
from openai.resources.chat import Completions

from wrapt import wrap_function_wrapper

from .api_emissions_tracker import APIEmissionsTracker

from .logger import logger


def azure_openai_chat_wrapper(
    wrapped,
    instance: Completions,
    args,
    kwargs
):
    response = wrapped(*args, **kwargs)

    if response:
        # Collect meta data
        model = response.model
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        # Calculate emissions
        amount = APIEmissionsTracker.approximate_emissions(model, prompt_tokens, completion_tokens)
        logger.add_emissions(amount)

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


azure_open_ai_instrumentor = AzureOpenAIInstrumentor()
azure_open_ai_instrumentor.instrument()