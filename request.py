import requests

url = "http://127.0.0.1:8000/api/xray"

payload = {}
files = [
  ('image', open('./00000013_005.png','rb'))
]


response = requests.request("POST", url, files = files)

print(response.text.encode('utf8'))