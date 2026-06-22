import json

class Person:
    def __init__(self, name: str, age: int, city: str):
        self.name = name
        self.age = age
        self.city = city

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age}, city='{self.city}')"

# Custom hook to convert dict to Person object
def person_decoder(obj):
    # Validate required keys
    if all(k in obj for k in ("name", "age", "city")):
        try:
            return Person(
                name=str(obj["name"]),
                age=int(obj["age"]),
                city=str(obj["city"])
            )
        except (ValueError, TypeError):
            raise ValueError("Invalid data types in JSON for Person")
    return obj  # Return unchanged if not matching Person structure

# Example JSON string
json_data = '''
{
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
'''

try:
    # Parse JSON into Person object
    person = json.loads(json_data, object_hook=person_decoder)
    print(person)  # Output: Person(name='Alice', age=30, city='New York')
except json.JSONDecodeError as e:
    print(f"JSON parsing error: {e}")
except ValueError as e:
    print(f"Data validation error: {e}")
