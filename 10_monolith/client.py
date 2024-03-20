import requests
url = "http://localhost:8000"

response = requests.get(f"{url}/posts")
print(response.text)

response = requests.get(f"{url}/post/2")
print(response.text)

post={"title":"Mi experiencia como dev", "content":"regular"}
response=requests.post(f"{url}/posts",post)
print (response.text)