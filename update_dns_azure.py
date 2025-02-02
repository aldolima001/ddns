import requests
from azure.identity import ClientSecretCredential
from azure.mgmt.dns import DnsManagementClient

# Solicitação de credenciais do usuário
tenant_id = input("Digite o ID do inquilino (tenant) do Azure: ")
client_id = input("Digite o ID do cliente (client) do Azure: ")
client_secret = input("Digite o segredo do cliente (client secret) do Azure: ")
subscription_id = input("Digite o ID da assinatura do Azure: ")
resource_group_name = input("Digite o nome do grupo de recursos: ")
zone_name = input("Digite o nome da zona DNS: ")
record_set_name = input("Digite o nome do conjunto de registros: ")

# Função para obter o IP público atual
def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

# Função para atualizar o registro DNS
def update_dns_record():
    credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    dns_client = DnsManagementClient(credential, subscription_id)

    ip_address = get_public_ip()
    record_set_params = {
        'ttl': 3600,
        'arecords': [{'ipv4_address': ip_address}]
    }

    dns_client.record_sets.create_or_update(
        resource_group_name,
        zone_name,
        record_set_name,
        'A',
        record_set_params
    )
    print(f"Registro DNS atualizado para {ip_address}")

# Atualizar o registro DNS uma vez
update_dns_record()
