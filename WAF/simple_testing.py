import os
import requests
import json

# Resolve the file path dynamically
script_dir = os.path.dirname(__file__)  # Get script's directory
file_path = os.path.join(script_dir, 'testing_requests.json')

try:
    with open(file_path, 'r') as f:
        reqs = json.load(f)

    for req in reqs:
        response = requests.request(**req)
        print(f"Request sent: {req}, Response: {response.status_code}")
except FileNotFoundError:
    print(f"File not found: {file_path}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
