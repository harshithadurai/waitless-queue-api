import requests

# Base URL of the FastAPI server
base_url = "http://localhost:8000"

# response = requests.post(f"{base_url}/add_user/{user}")

# Add users
users = ["1234", "5678", "9012"]
for user in users:
    response = requests.post(f"{base_url}/add_user/{user}")
    print(f"{base_url}/add_user/{user}")
    print(response.json())

# Join queues
queues_to_join = [("treadmill", "1234"), ("row", "5678"), ("cable", "9012"), ("treadmill", "5678")]
for queue in queues_to_join:
    response = requests.post(f"{base_url}/join/{queue[0]}/{queue[1]}")
    print(response.json())

# Leave queues
queues_to_leave = [("treadmill", "1234"), ("cable", "9012")]
for queue in queues_to_leave:
    response = requests.delete(f"{base_url}/leave/{queue[0]}/{queue[1]}")
    print(response.json())

# Get queue count for a machine
response = requests.get(f"{base_url}/waiting/treadmill")
print(response.json())

# Get queue count for a user
response = requests.get(f"{base_url}/queues/5678")
print(response.json())

# Get queues for a user
response = requests.get(f"{base_url}/queues/1234")
print(response.json())

response = requests.get(f"{base_url}/queues/9012")
print(response.json())
