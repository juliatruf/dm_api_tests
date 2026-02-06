"""
curl -X 'POST' \
  'http://185.185.143.231:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "string",
  "email": "string",
  "password": "string"
}'

curl -X 'PUT' \
  'http://185.185.143.231:5051/v1/account/2bf12c78-c18d-4efb-a111-f8de56a9be4b' \
  -H 'accept: text/plain'
"""

import pprint

import requests

# url = 'http://185.185.143.231:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "juliat_test",
#     "email": "juliat_test@mail.ru",
#     "password": "1233456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )
#
# print(response.status_code)
# pprint.pprint(response.json())

url = 'http://185.185.143.231:5051/v1/account/2bf12c78-c18d-4efb-a111-f8de56a9be4b'
headers = {
    'accept': 'text/plain'
}

response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])
