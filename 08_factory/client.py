import requests
url = "http://localhost:8000/"
headers = {"Content-Type": "application/json"}

package = {"weight": 1, "destination": "689 Calle Lopez"}
vehicle_type = "Drone"
data = {"vehicle_type": vehicle_type, "package": package}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    print("Delivery successfully scheduled.")
else:
    print("Error scheduling delivery:", response.text)
    
package = {"weight": 2, "destination": "356 Calle Perez"}
vehicle_type = "MotorCycle"
data = {"vehicle_type": vehicle_type, "package": package}
response = requests.post(url, json=data, headers=headers)
if response.status_code == 200:
    print("Delivery successfully scheduled.")
else:
    print("Error scheduling delivery:", response.text)