import json

my_data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}
result = json.dumps(my_data)

print(result)  # Output: {"name": "John Doe", "age": 30, "city": "New York"}
print(type(result))  # Output: <class 'str'>
