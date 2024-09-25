from app.api import iniciar_sessao, buscar_dados_chamado, encerrar_sessao
from app.pdf_generator import gerar_relatorio_pdf

def main():
    # Iniciar sessão
    session_token = iniciar_sessao()
    print(f"Session Token: {session_token}")

    # Buscar os dados do chamado
    id_chamado = 75
    ticket_data = buscar_dados_chamado(session_token, id_chamado)

    # Gerar o PDF
    gerar_relatorio_pdf(ticket_data)

    # Encerrar sessão
    encerrar_sessao(session_token)

if __name__ == "__main__":
    main()
