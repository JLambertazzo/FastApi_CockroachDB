import requests

post_response = requests.post('http://localhost:8000/sports')
print(post_response.json())

response = requests.get('http://localhost:8000/')
print(response.json())