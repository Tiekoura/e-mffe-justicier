import json
import subprocess
import requests

# Get GitHub token
token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip()

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

repo_data = {
    'name': 'e-mffe-justicier',
    'description': "Agent juridique ivoirien pour le droit de l'enfant, de la femme et de la famille",
    'private': False,
    'has_issues': True,
    'has_wiki': False,
    'has_pages': False
}

url = 'https://api.github.com/user/repos'
response = requests.post(url, headers=headers, data=json.dumps(repo_data))

if response.status_code == 201:
    data = response.json()
    print("✅ Dépôt créé !")
    print(f"   Nom : {data['full_name']}")
    print(f"   URL : {data['html_url']}")
    print(f"   Clone : {data['clone_url']}")
else:
    print(f"❌ Erreur {response.status_code}: {response.text}")
