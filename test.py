import subprocess
import requests
import json
cmd = 'wmic csproduct get uuid'
output = subprocess.check_output(cmd)
output = output.decode("utf-8")[4:]
output = ''.join(char for char in output if char.isalnum())
dictionary = {
    'auth_key': 'tipokey',
    'hardware_id': 'ABVXCS',
}
json_object = json.dumps(dictionary, indent = 2)

r = requests.post('https://authservice-production-ef9f.up.railway.app/api/auth', data =json_object)
print(r)