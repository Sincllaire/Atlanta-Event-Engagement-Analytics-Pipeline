import requests

url = "https://www.googleapis.com/youtube/v3/search"

params = {
    "part": "snippet",
    "q": "Atlanta music",
    "type": "video",
    "maxResults": 5,
    "order": "viewCount",
    "key": "AIzaSyCfx1vS0og7au8ZO3KcslJ44ms_e-r0dDE"
}

response = requests.get(url, params=params)
print(response.status_code)
print(response.json())