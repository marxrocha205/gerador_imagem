import requests
import webbrowser

def baixar_comprovante(nome_aluno, url_base_api):
    """
    Chama a API para gerar uma imagem com o nome do aluno e a salva localmente.
    """
    try:
        # 1. Monta a URL completa com o nome a ser inserido na imagem
        params = {'nome': nome_aluno}
        url_completa = f"{url_base_api}/gerar-imagem"

        print(f"Chamando a API em: {url_completa} com o nome '{nome_aluno}'...")

        # 2. Faz a requisição GET para a API
        response = requests.get(url_completa, params=params)

        # 3. Verifica se a requisição foi bem-sucedida (código 200 OK)
        if response.status_code == 200:
            # 4. Define o nome do arquivo de saída
            nome_arquivo = f"comprovante_{nome_aluno.replace(' ', '_').lower()}.png"

            # 5. Salva o conteúdo da resposta (a imagem) em um arquivo
            with open(nome_arquivo, 'wb') as f:
                f.write(response.content)

            print(f"Sucesso! Imagem salva como '{nome_arquivo}'")
            # Abre a imagem recém-criada
            webbrowser.open(nome_arquivo)
        else:
            # Mostra uma mensagem de erro se algo der errado
            print(f"Erro ao chamar a API: {response.status_code}")
            print(f"Mensagem: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")

# --- Exemplo de Uso ---
if __name__ == "__main__":
    # URL da sua API na Render
    minha_api = "https://gerador-imagem.onrender.com"

    # Nome que você quer que apareça na imagem
    nome_para_gerar = "Ana Julia"

    baixar_comprovante(nome_para_gerar, minha_api)