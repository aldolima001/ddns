# Aviso: O código presente neste repositório é destinado a fins educacionais e demonstrativos. Ele foi desenvolvido com o objetivo de auxiliar na configuração do DDNS utilizando as plataformas Cloudflare e DigitalOcean. No entanto, o autor não oferece suporte técnico ou garante a sua funcionalidade em todos os cenários.

# É fundamental que você:

# Revise o código: Analise linha por linha para entender o funcionamento e identificar possíveis vulnerabilidades.
# Adapte o código: Faça as modificações necessárias para que o script se ajuste ao seu ambiente específico.
# Teste o código: Execute o script em um ambiente de testes antes de implementá-lo em produção.
# Consulte a documentação: Consulte a documentação oficial da Cloudflare e DigitalOcean para obter informações mais detalhadas sobre as APIs e as melhores práticas de segurança.
# O autor não se responsabiliza por:

# Erros ou omissões: O código pode conter erros ou omissões que podem causar problemas inesperados.
# Danos: O uso indevido deste código pode causar danos ao seu sistema ou a terceiros.
# Violação de segurança: O código pode ser vulnerável a ataques de segurança.

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
