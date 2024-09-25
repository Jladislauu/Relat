import requests

# Configurações da API GLPI
GLPI_API_URL = "https://dev.suporte.riole.com.br/apirest.php"  # Substitua pelo URL correto
USER_TOKEN = "5SBUmU9fkOQDCzkqGzxeZ9M3GaaX4GDWD627Zr1p"  # Substitua pelo seu user token
APP_TOKEN = "LFuNVj6XVqCNLhR0q7GikQgj0eOEhnOmRiY5qZdb"  # Substitua pelo seu app token

def iniciar_sessao():
    headers = {
        'Authorization': f'user_token {USER_TOKEN}',
        'App-Token': APP_TOKEN
    }
    response = requests.get(f'{GLPI_API_URL}/initSession', headers=headers)
    if response.status_code == 200:
        return response.json()['session_token']
    raise Exception("Erro ao iniciar sessão: " + response.json())

def buscar_dados_chamado(session_token, id_chamado):
    headers = {
        'Authorization': f'user_token {USER_TOKEN}',
        'App-Token': APP_TOKEN,
        'Session-Token': session_token
    }
    response = requests.get(f'{GLPI_API_URL}/Ticket/{id_chamado}', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar chamado {id_chamado}: {response.json()}")
    return response.json()

def encerrar_sessao(session_token):
    headers = {
        'Authorization': f'user_token {USER_TOKEN}',
        'App-Token': APP_TOKEN,
        'Session-Token': session_token
    }
    response = requests.get(f'{GLPI_API_URL}/killSession', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro ao encerrar a sessão: {response.json()}")
    return response.json()
    
def main():
    session_token = iniciar_sessao()
    try:
        id_chamado = 75  # ID do chamado que você deseja buscar
        ticket_data = buscar_dados_chamado(session_token, id_chamado)
        print(ticket_data)
    finally:
        encerrar_sessao(session_token)  # Certifique-se de encerrar a sessão no final
if __name__ == "__main__":
    main()
