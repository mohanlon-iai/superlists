import json, requests, os

task_id = os.environ['MESOS_TASK_ID']
payload = {"task_id": task_id}
gtkpr_addr = 'http://vault-gatekeeper.marathon.mesos:9201'
gtkpr_token_path = '/token'

r = requests.post(gtkpr_addr + gtkpr_token_path, data=json.dumps(payload))

temp_token = r.json()['token']
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
