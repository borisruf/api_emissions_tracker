from stub_ai import StubAzureOpenAI

from .api_emissions_tracker import APIEmissionsTracker

from .logger import logger

# Store the original method
StubAzureOpenAI.chat._original_create = StubAzureOpenAI.chat.completions.create

def _new_create_stub_azure_open_ai(model, messages, temperature=1, max_tokens=16, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):

    response = StubAzureOpenAI.chat._original_create(model, messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stop)
    
    if response:
        # Collect meta data
        model = response.model
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens

        # Calculate emissions
        amount = APIEmissionsTracker.approximate_emissions(model, prompt_tokens, completion_tokens)
        
        record = {"model": model, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "co2e_in_g": amount}
        logger.add_record(record)

    return response


# Monkey patch the method of the StubAzureOpenAI class
StubAzureOpenAI.chat.completions.create = _new_create_stub_azure_open_ai