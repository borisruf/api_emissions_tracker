import datetime
import json
import os


class Logger:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[str(datetime.datetime.now())] = record

    def write_log_file(self):
        with open('emissions.json', 'w') as file:
            json.dump(self.records, file, indent=4)


# Create an instance of the GlobalObject
logger = Logger()
