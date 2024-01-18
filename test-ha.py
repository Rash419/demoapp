import requests
import json
import secrets

def create_serverid_map():
    url = "http://test.demoapp:30080/serverId?RouteToken="
    for i in range(1000):
       route_token = generate_random_token()
       serverid = get_serverid(f"{url}{route_token}")
       serverid_map[serverid] = route_token


def generate_random_token():
    token = secrets.token_hex(4)
    return token

def get_serverid(url):
    # Send an HTTP request to the HAProxy server to get a random token
    response = requests.get(url)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        serverid = json_data.get('serverId')
        return serverid
    else:
        print('Failed to get serverid, HAproxy returned status_code ' + str(response.status_code))

serverid_map = {}
create_serverid_map()
print("Map of serverid<->route_token:")
for key,value in serverid_map.items():
    print(f"{key}<->{value}")
