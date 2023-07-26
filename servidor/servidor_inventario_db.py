##################################################################################
#####     Renan Brian                                                        #####
#####     Especialista em Programação | Transformando ideias em código       #####
#####     E-mail: renanmgx@hotmail.com                                       #####
##################################################################################

from flask import Flask, request, render_template
import openpyxl


app = Flask(__name__)


planilha = r"C:\Users\InnerRep.PATRIMAR\OneDrive - PATRIMAR ENGENHARIA S A\inventario_DP\inventario.db"

################    funções
def adicionar_dados_excel(planilha, dados):

    banco_dados = ""
    for key,dado in dados.items():
        banco_dados += dado + ";:;"
    
    with open(planilha, "a") as db:
        db.write(banco_dados + "\n")





def iniciar(dados):
    adicionar_dados_excel(planilha, dados)



@app.route('/patrimar', methods=['POST'])
def alterar_planilha():
    dados = request.get_json()

    try:
        iniciar(dados)
    except Exception as erro:
        iniciar(dados)
        app.logger.error(erro)

    return 'Planilha atualizada com sucesso!'


if __name__ == '__main__':
    app.run(host='INVENTARIO', port=5000)
