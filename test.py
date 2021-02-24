import requests

def tests():
  post_response = requests.post('http://localhost:8000/sports')
  print(post_response.json())

  response = requests.get('http://localhost:8000/sports')
  print(response.json())

if __name__ == '__main__':
  tests()