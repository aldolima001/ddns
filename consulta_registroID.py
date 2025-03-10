Scripts Faz Consulta a Registro DNS CloudFlare.

Aviso: O código presente neste repositório é destinado a fins educacionais e demonstrativos. Ele foi desenvolvido com o objetivo de auxiliar na configuração do DDNS utilizando as plataformas Cloudflare e DigitalOcean. No entanto, o autor não oferece suporte técnico ou garante a sua funcionalidade em todos os cenários.

É fundamental que você:

Revise o código: Analise linha por linha para entender o funcionamento e identificar possíveis vulnerabilidades.

Adapte o código: Faça as modificações necessárias para que o script se ajuste ao seu ambiente específico.

Teste o código: Execute o script em um ambiente de testes antes de implementá-lo em produção.

Consulte a documentação: Consulte a documentação oficial da Cloudflare para obter informações mais detalhadas sobre as APIs e as melhores práticas de segurança.

O autor não se responsabiliza por:

Erros ou omissões: O código pode conter erros ou omissões que podem causar problemas inesperados.

Danos: O uso indevido deste código pode causar danos ao seu sistema ou a terceiros.

Violação de segurança: O código pode ser vulnerável a ataques de segurança.

import requests

# Variáveis
api_token = 'Seu Token API'
zone_id = 'ID da Sua Zona'
registro_nome_completo = 'hostname completo do registro Exemplo teste.aldolima.com.br'  # Especifique o nome completo do registro

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
