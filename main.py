# 1. IMPORTE A BIBLIOTECA CORS
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

# Inicializa a aplicação Flask
app = Flask(__name__)

# 2. HABILITE O CORS PARA TODA A APLICAÇÃO
#    Isso permite que seu chatbot (rodando no Live Server) acesse esta API.
CORS(app)

def gerar_imagem(nome_pessoa):
    """
    Gera uma imagem a partir do template, adicionando um nome e a data atual.

    :param nome_pessoa: O nome a ser inserido na imagem.
    :return: Um objeto de imagem da biblioteca Pillow.
    """
    try:
        # Caminho para o template e para a fonte
        template_path = "template.png"
        font_path = "arial.ttf"

        # Carrega a imagem do template
        img = Image.open(template_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        # ---- Definição de Fontes e Cores ----
        # Tente carregar a fonte, se não encontrar, usa uma padrão
        try:
            fonte_nome = ImageFont.truetype(font_path, 12) # Ajuste o tamanho conforme necessário
            fonte_data = ImageFont.truetype(font_path, 12) # Ajuste o tamanho conforme necessário
        except IOError:
            print(f"Fonte '{font_path}' não encontrada, usando fonte padrão.")
            fonte_nome = ImageFont.load_default()
            fonte_data = ImageFont.load_default()

        cor_texto = (0, 0, 0) # Cor preta

        # ---- Adiciona o Nome na Imagem ----
        # Coordenadas: x=48, y=144
        draw.text((48, 144), nome_pessoa, font=fonte_nome, fill=cor_texto)

        # ---- Adiciona a Data Atual na Imagem ----
        data_hoje = datetime.now().strftime('%d/%m/%Y')

        # Coordenadas 1: x=157, y=187
        draw.text((157, 187), data_hoje, font=fonte_data, fill=cor_texto)

        # Coordenadas 2: x=428, y=188
        draw.text((428, 188), data_hoje, font=fonte_data, fill=cor_texto)

        return img

    except FileNotFoundError:
        print(f"Erro: O arquivo de template '{template_path}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao gerar a imagem: {e}")
        return None

# ---- Definição do Endpoint da API ----
@app.route('/gerar-imagem', methods=['GET'])
def api_gerar_imagem():
    """
    Endpoint da API para gerar e retornar a imagem.
    Recebe o nome através de um parâmetro na URL.
    Exemplo de uso: http://127.0.0.1:5000/gerar-imagem?nome=Maria%20Souza
    """
    # Pega o parâmetro 'nome' da URL
    nome = request.args.get('nome')

    if not nome:
        return jsonify({"erro": "O parâmetro 'nome' é obrigatório."}), 400

    # Gera a imagem com o nome fornecido
    imagem_gerada = gerar_imagem(nome)

    if imagem_gerada is None:
        return jsonify({"erro": "Não foi possível gerar a imagem. Verifique os logs do servidor."}), 500

    # Salva a imagem em um buffer de memória em vez de um arquivo físico
    buffer = io.BytesIO()
    imagem_gerada.save(buffer, format='PNG')
    buffer.seek(0)

    # Retorna a imagem como um arquivo na resposta da API
    return send_file(
        buffer,
        mimetype='image/png'
        # 3. MUDANÇA IMPORTANTE: A linha abaixo foi REMOVIDA.
        #    O JavaScript agora cuida de iniciar o download.
        #    as_attachment=True, 
        #    download_name=f'imagem_{nome.replace(" ", "_").lower()}.png'
    )

# ---- Roda a Aplicação ----
if __name__ == '__main__':
    # 'host="0.0.0.0"' torna a API acessível na sua rede local
    app.run(host="0.0.0.0", port=5000, debug=True)