import requests

# Base URL of the FastAPI server
base_url = "http://localhost:8000"

requests.post(f"{base_url}/add_user/2812")


response = requests.post(f"{base_url}/join/Treadmill/2812")