import os
import json

MAPPING = {}

with open(os.path.join(os.path.dirname(__file__), "sensor_space_mapping.json")) as file:
    MAPPING = json.load(file)
