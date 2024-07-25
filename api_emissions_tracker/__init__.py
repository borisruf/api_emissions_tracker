import importlib.util

from api_emissions_tracker.api_emissions_tracker import APIEmissionsTracker

if importlib.util.find_spec("openai") is not None:
    from .azure_open_ai import AzureOpenAIInstrumentor    

if importlib.util.find_spec("stub_ai") is not None:
    from api_emissions_tracker.stub_azure_open_ai import StubAzureOpenAI