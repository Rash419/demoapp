import requests
import json
import secrets
import sys

url = f"{sys.argv[1]}/serverId?RouteToken="
print(f"starting script with url[{url}]")
def create_serverid_map():
    for i in range(1000):
       route_token = generate_random_token()
       serverid = get_serverid(f"{url}{route_token}")
       serverid_map[serverid] = route_token

    print("Map of serverid<->route_token:")
    for key,value in serverid_map.items():
        print(f"{key}<->{value}")


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

def test_serverid_mismatch():
    print('Testing for serverId mismatch...')
    for expected_serverid, route_token in serverid_map.items():
       actual_serverid = get_serverid(f"{url}{route_token}") 
       if expected_serverid != actual_serverid:
            print(f"Mismatch for route_token[{route_token}], expected_serverid[{expected_serverid}] but actual_serverid[{actual_serverid}]")
            return
    print('No mismatch found')

serverid_map = {}
create_serverid_map()

# test mismatch by sending /serverId request with route_token from map and check if we get same serverId
test_serverid_mismatch()
