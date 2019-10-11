import requests
url = 'http://172.31.10.24:3000/api/login'
h = {'Content-Type': 'application/json',}
d = '{"cardId": "1234567"}'
r = requests.post(url, headers=h, data=d)
print(r.status_code)
