import requests

def tests():
  post_response = requests.post('http://localhost:8000/sports', json={
    "name": "soccer",
    "description": "a sport"
  })
  print(post_response.json())
  sport_id = (post_response.json())["id"]

  get_response = requests.get('http://localhost:8000/sports')
  print(get_response.json())

  patch_response = requests.patch(f"http://localhost:8000/sports/{sport_id}", json={
    "name": "not soccer",
    "description": "not a sport"
  })
  print(patch_response.json())

  get_id_response = requests.get(f"http://localhost:8000/sports/{sport_id}")
  print(get_id_response.json())

  delete_response = requests.delete(f"http://localhost:8000/sports/{sport_id}")
  print(delete_response.json())

  bad_get_response = requests.get(f"http://localhost:8000/sports/{sport_id}")
  print(bad_get_response.json())

if __name__ == '__main__':
  tests()