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
import os
import sys

# Função para obter o IP atual
def get_current_ip():
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

# Função para obter o record id
def get_record_id(api_token, zone_id, record_name):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers).json()
    for record in response['result']:
        if record['name'] == record_name:
            return record['id']
    return None

# Função para atualizar o registro DNS
def update_dns_record(api_token, zone_id, record_id, ip, record_name):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'type': 'A',
        'name': record_name,  # Usar o nome do registro atual
        'content': ip,
        'ttl': 120, 
        'proxied': False
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Função para ler a configuração do arquivo
def read_config():
    config = {}
    with open('config.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

# Função para salvar a configuração no arquivo
def save_config(api_token, zone_id, record_name):
    with open('config.txt', 'w') as file:
        file.write(f'api_token={api_token}\n')
        file.write(f'zone_id={zone_id}\n')
        file.write(f'record_name={record_name}\n')

# Função para reconfigurar os dados
def reconfigure():
    api_token = input("Digite seu API token: ")
    zone_id = input("Digite seu Zone ID: ")
    record_name = input("Digite o nome do registro DNS: ")
    save_config(api_token, zone_id, record_name)

# Verificar argumentos da linha de comando
if len(sys.argv) > 1 and sys.argv[1] == '--reconfigure':
    reconfigure()
else:
    # Verificar se o arquivo de configuração existe
    if not os.path.isfile('config.txt'):
        reconfigure()
    else:
        config = read_config()
        api_token = config['api_token']
        zone_id = config['zone_id']
        record_name = config['record_name']

        # Verificar e atualizar o IP se necessário
        current_ip = get_current_ip()
        saved_ip = None
        try:
            with open('current_ip.txt', 'r') as file:
                saved_ip = file.read().strip()
        except FileNotFoundError:
            pass

        if current_ip != saved_ip:
            record_id = get_record_id(api_token, zone_id, record_name)
            if record_id:
                update_dns_record(api_token, zone_id, record_id, current_ip, record_name)
                with open('current_ip.txt', 'w') as file:
                    file.write(current_ip)
                print(f"Registrado com sucesso endereço: {current_ip}")
            else:
                print("Record ID não encontrado.")
        else:
            print("O IP atual é o mesmo. Nenhuma atualização necessária.")
