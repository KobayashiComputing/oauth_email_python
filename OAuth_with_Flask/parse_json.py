import json

# Example JSON string
json_string = '{"name": "Alice", "age": 30, "skills": ["Python", "Data Analysis"]}'

try:
    # Parse JSON string into a Python dictionary
    data = json.loads(json_string)
    print("Parsed from string:", data)
    print("Name:", data.get("name"))
    print("Skills:", ", ".join(data.get("skills", [])))
except json.JSONDecodeError as e:
    print("Error parsing JSON string:", e)

# Example: Reading JSON from a file
try:
    # Create a sample JSON file
    with open("sample.json", "w") as f:
        json.dump(data, f, indent=4)

    # Read and parse JSON from file
    with open("sample.json", "r") as f:
        file_data = json.load(f)
    print("\nParsed from file:", file_data)
except FileNotFoundError:
    print("File not found.")
except json.JSONDecodeError as e:
    print("Error parsing JSON file:", e)
except Exception as e:
    print("Unexpected error:", e)
