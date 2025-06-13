import os
import json

def load_tarot_data():
    json_path = os.path.join('data', 'tarot_data.json')
    if not os.path.exists(json_path):
        print("Json data not found. Make sure it's in the data directory")
        exit(1)
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

tarot_data = load_tarot_data()
