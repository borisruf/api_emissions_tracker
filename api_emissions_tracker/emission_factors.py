import json
import os

class EmissionFactors:
    def __init__(self):
        path = os.path.join(os.path.dirname(__file__), 'emission_factors.json')
        with open(path, "r") as file:
            self.data = json.load(file)

    def update(self, new_factors):
        self.data.update(new_factors)

# Create an instance of the GlobalObject
global_emission_factors = EmissionFactors()
