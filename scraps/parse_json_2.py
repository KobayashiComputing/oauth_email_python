import json

# Example: Reading JSON from a file
try:
    # Read and parse JSON from file
    with open("env/google_oauth2.json", "r") as f:
        file_data = json.load(f)
    print("\nParsed from file:", file_data)
except FileNotFoundError:
    print("File not found.")
except json.JSONDecodeError as e:
    print("Error parsing JSON file:", e)
except Exception as e:
    print("Unexpected error:", e)
