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
import json
import click
import configparser
import os

# Nome do arquivo de configuração
config_file = 'config.ini'

def get_public_ip():
    """Obtém o endereço IP público do dispositivo."""
    response = requests.get('https://api.ipify.org?format=json')
    return json.loads(response.text)['ip']

def update_dns_record(token, domain_name, record_name, new_ip):
    """Atualiza o registro DNS A na DigitalOcean."""
    headers = {'Authorization': 'Bearer ' + token}
    url = f"https://api.digitalocean.com/v2/domains/{domain_name}/records"
    records = requests.get(url, headers=headers).json()['domain_records']
    for record in records:
        if record['name'] == record_name and record['type'] == 'A':
            record_id = record['id']
            data = {'type': 'A', 'name': record_name, 'data': new_ip}
            response = requests.put(f"{url}/{record_id}", headers=headers, json=data)
            if response.status_code == 200:
                print(f"Registro {record_name} atualizado com sucesso para {new_ip}")
            else:
                print("Erro ao atualizar o registro:", response.text)

@click.command()
@click.option('--token', required=False, help='Seu token de acesso à API da DigitalOcean')
@click.option('--domain', required=False, help='O nome do domínio a ser atualizado')
@click.option('--record', required=False, help='O nome do registro DNS a ser modificado')
def update_dns(token, domain, record):
    # Carrega as configurações do arquivo, se existir
    config = configparser.ConfigParser()

    # Verifica se o arquivo de configuração existe
    if os.path.exists(config_file):
        config.read(config_file)
        saved_token = config.get('DEFAULT', 'token', fallback=None)
        saved_domain = config.get('DEFAULT', 'domain', fallback=None)
        saved_record = config.get('DEFAULT', 'record', fallback=None)
    else:
        saved_token = None
        saved_domain = None
        saved_record = None

    # Utiliza as configurações salvas se as opções não forem fornecidas
    token = token or saved_token
    domain = domain or saved_domain
    record = record or saved_record

    if not token or not domain or not record:
        # Solicita as informações do usuário se não foram fornecidas e não estão salvas
        if not token:
            token = click.prompt('Digite seu token de acesso da DigitalOcean', type=str)
        if not domain:
            domain = click.prompt('Digite o nome do domínio', type=str)
        if not record:
            record = click.prompt('Digite o nome do registro DNS', type=str)

        # Atualiza as configurações salvas
        config['DEFAULT'] = {
            'token': token,
            'domain': domain,
            'record': record
        }

        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        print("Utilizando configurações do arquivo config.ini")

    try:
        ip = get_public_ip()
        update_dns_record(token, domain, record, ip)
    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    update_dns()
