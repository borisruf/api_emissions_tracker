from wrapt import wrap_function_wrapper
import warnings

from .logger import logger
from .emission_factors import global_emission_factors


class APIEmissionsTracker:
    def __init__(self, emission_factors=None, write_log_file=False):

        self.write_log_file = write_log_file

        if emission_factors:
            global_emission_factors.update(emission_factors)

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

        total_co2e = sum(entry['co2e_in_g'] for entry in logger.records.values())

        # Plot the emission value and any relevant details
        print("Total emissions:", total_co2e, "g CO2e")
        print(f"Compare: https://borisruf.github.io/carbon-footprint-modeling-tool/search.html?value={total_co2e}&mass_unit=g&emission_type=co2e")

        if self.write_log_file:
            logger.write_log_file()
        

    def approximate_emissions(model, prompt_tokens, completion_tokens):
        
        if model in global_emission_factors.data:
            return prompt_tokens*global_emission_factors.data[model]['per_prompt_token'] + completion_tokens*global_emission_factors.data[model]['per_completion_token']
        else:
            warnings.warn(f"No emission data available for the AI model '{model}'")
            return None


