from wrapt import wrap_function_wrapper
import json
import warnings
import os

from .logger import logger


class APIEmissionsTracker:
    def __init__(self):
        logger.emissions = 0.0

    def start(self):
        # Start tracking emissions
        self.tracking = True

    def stop(self):
        # Stop tracking emissions
        if hasattr(self, 'tracking') and self.tracking:  # Check if tracking was started
            self.print_emissions()
        self.tracking = False

    def add_emissions(self, amount):
        if hasattr(self, 'tracking') and self.tracking:
            self.emissions += amount

    def print_emissions(self):
        # Plot the emission value and any relevant details
        print("emissions:", logger.emissions, "g CO2e")
        print(f"Compare: https://borisruf.github.io/carbon-footprint-modeling-tool/search.html?value={logger.emissions}&mass_unit=g&emission_type=co2e")

    def approximate_emissions(model, prompt_tokens, completion_tokens):
        path = os.path.join(os.path.dirname(__file__), 'emission_factors.json')
        with open(path, "r") as file:
            emission_factors = json.load(file)

            if model in emission_factors:
                return prompt_tokens*emission_factors[model]['per_prompt_token'] + completion_tokens*emission_factors[model]['per_completion_token']
            else:
                warnings.warn(f"No emission data available for the AI model '{model}'")
                return 0


