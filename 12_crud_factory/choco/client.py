import requests
import json

url = "http://localhost:8000/chocolates"
headers = {"Content-Type": "application/json"}

new_choco_data = {
    "tipo": "bombones",
    "peso": 10,
    "sabor": "surtido",
    "relleno": "menta"
}
response = requests.post(url=url, json=new_choco_data, headers=headers)
print(response.json())

new_choco_data = {
    "tipo": "trufas",
    "peso": 15,
    "sabor": "leche",
    "relleno": "coco"
}
response = requests.post(url=url, json=new_choco_data, headers=headers)
print(response.json())


response = requests.get(url=url)
print(response.json())


choco_id_to_update = 1
updated_choco_data = {
    "tipo": "bombones"
}
response = requests.put(f"{url}/{choco_id_to_update}", json=updated_choco_data)
print("Chocolate actualizado:", response.json())

response = requests.get(url=url)
print(response.json())

choco_id_to_delete = 1
response = requests.delete(f"{url}/{choco_id_to_delete}")
print("Chocolate eliminado:", response.json())

response = requests.get(url=url)
print(response.json())