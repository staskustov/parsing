from pprint import pprint
import requests
import json
URL = 'https://api.vk.com/method/friends.get'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
          'Accept':'*/*'}
nickname = 'nickname'
user_id = '7464770'
token = '57e099cd57e099cd57e099cda357917e8f557e057e099cd095caab0fbc25058ea1a437f'
version = '5.52'
params = {'v': version,
          'user_id': user_id,
          'fields': nickname,
          'access_token': token}
response = requests.get(URL, headers=header, params=params)

if response.ok:
    data = json.loads(response.text)



pprint(f"Количество друзей {data['response']['count']}")

with open('file.pdf','wb') as f:
    f.write(response.content)










# with open('file.pdf','wb') as f:
#     f.write(response.content)