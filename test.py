import requests

def tests():
  # post_response = requests.post('http://localhost:8000/sports')
  # print(post_response.json())

  # response = requests.get('http://localhost:8000/sports')
  # print(response.json())
  response = requests.post('http://localhost:8000/sports', json={
    "id": 8,
    "name": "soccer",
    "description": "a sport"
  })
  print(response.json())

  response2 = requests.get('http://localhost:8000/sports')
  print(response2.json())

if __name__ == '__main__':
  tests()