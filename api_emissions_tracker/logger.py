class Logger:
    def __init__(self):
        self.emissions = 0.0

    def add_emissions(self, amount):
        self.emissions += amount


# Create an instance of the GlobalObject
logger = Logger()
