import requests

# Variáveis
api_token = 'cn9M5zW0kURqZviLx7sBfc4mrnV8K-RRpkDH6qoR'
zone_id = '6010b6df61f063e1c55ac3cced22901e'
registro_nome_completo = 'teste3.devemcasa.com.br'  # Especifique o nome completo do registro

# Cabeçalhos da API
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-Type': 'application/json'
}

# Requisição para listar os registros DNS e buscar pelo nome completo especificado
response = requests.get(
    f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records',
    headers=headers
)

if response.status_code == 200:
    dns_records = response.json()
    for record in dns_records['result']:
        if record['name'] == registro_nome_completo:
            print(f"ID: {record['id']}, Name: {record['name']}, Type: {record['type']}, Content: {record['content']}")
else:
    print('Falha ao listar os registros DNS:', response.status_code, response.text)
