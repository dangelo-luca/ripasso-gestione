import requests

def Api():
    response = requests.get(f'http://api.open-notify.org/astros.json')
    data = response.json() #converte da json a dict python
    return data.get("people",[])
    
