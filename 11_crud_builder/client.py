import requests

url = "http://localhost:8000/tacos"
headers = {'Content-type': 'application/json'}

# GET /tacos
response = requests.get(url)
print(response.json())

# POST /tacos 
mi_taco = {
    "base": "Suadero",
    "guiso": "Mole Verde",
    "toppings": ["Cebolla", "Carne"],
    "salsa": "Roja"
}
response = requests.post(url, json=mi_taco, headers=headers)
print(response.json())

# GET /tacos
response = requests.get(url)
print(response.json())

# PUT /tacos/1
edit_tacos = {
    "base": "Bistec",
    "guiso": "Rajas",
    "toppings": ["Guacamole", "Carnita de Pavo"],
    "salsa": "Verde con Aguacate"
}
response = requests.post(url, json=edit_tacos, headers=headers)
print(response.json())

# GET /tacos
response = requests.get(url)
print(response.json())

# DELETE /tacos/1

response = requests.delete(url + "/1")
print(response.json())

# GET /tacos
response = requests.get(url)
print(response.json())