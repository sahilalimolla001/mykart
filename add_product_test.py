import requests

url = "http://127.0.0.1:5000/product/add"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NjQ0NDU2NCwianRpIjoiZDdhNWYwZTItMTU0My00YmIyLWJhNjYtYTZlYzAwNDU1OTQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzc2NDQ0NTY0LCJjc3JmIjoiNGJmOTY4N2YtYTE1OC00OGFkLWJjMzMtYjZmYzBkMGY1MDQ5IiwiZXhwIjoxNzc2NDQ1NDY0fQ.dBUHUU9IE9islk-b63K5D1QyyplEHtsUV4sjM9kJubg"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

data = {
    "name": "Shoes",
    "description": "Running shoes",
    "price": 2500,
    "stock": 10,
    "image_url": "image.jpg"
}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())