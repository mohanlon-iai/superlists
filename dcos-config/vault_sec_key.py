from decouple import config
import json, requests

task_id = config('MESOS_TASK_ID')
payload = {"task_id": task_id}
gtkpr_addr = config('GATE_KEEPER_ADDRESS', default='http://vault-gatekeeper.marathon.mesos')
gtkpr_port = config('GATE_KEEPER_PORT', default='9201')
gtkpr_token_path = config('GATE_KEEPER_TOKEN', default='/token')

r = requests.post(gtkpr_addr + ':' + gtkpr_port + gtkpr_token_path, data=json.dumps(payload))

try:
	temp_token = r.json()['token']
except KeyError as key:
	print("Key error: {0}".format(key))
	print(json.dumps(r.json(), sort_keys=True, indent=2))

tmp_token_headers = {'X-Vault-Token': temp_token}

vault_addr = 'https://vault.marathon.mesos:8200'
vault_wrap_path = '/v1/sys/wrapping/unwrap'

r = requests.put(vault_addr + vault_wrap_path, headers=tmp_token_headers, verify=False)

client_token = r.json()['auth']['client_token']
vault_sec_path = '/v1/secret/to-do/dev'
client_token_headers = {'X-Vault-Token': client_token}

r = requests.get(vault_addr + vault_sec_path, headers=client_token_headers, verify=False)

app_sec_key = r.json()['data']['key']

with open('sec_key', 'w') as s:
	s.write(app_sec_key)
