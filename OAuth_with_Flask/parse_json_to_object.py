# Source - https://stackoverflow.com/a/15882054
# Posted by DS., modified by community. See post 'Timeline' for change history
# Retrieved 2026-06-21, License - CC BY-SA 4.0

import json
from types import SimpleNamespace

try:
    # Read and parse JSON from file
    with open("env/google_oauth2.json", "r") as f:
        file_data = json.load(f, object_hook=SimpleNamespace)
        print("\nParsed from file:")
        print("     Project ID   : ", file_data.oauth2_google.web.project_id)
        print("     Client ID    : ", file_data.oauth2_google.web.client_id)
        print("     Client Secret: ", file_data.oauth2_google.web.client_secret)
except FileNotFoundError:
    print("File not found.")
except json.JSONDecodeError as e:
    print("Error parsing JSON file:", e)
except Exception as e:
    print("Unexpected error:", e)


#=========[ original example for additional info ]==================================
#
# data = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'

# # Parse JSON into an object with attributes corresponding to dict keys.
# # x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
# # Or, in Python 3.13+:
# #   json.loads(data, object_hook=SimpleNamespace)
# print(x.name, x.hometown.name, x.hometown.id)
