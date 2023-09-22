##################################################################################
#####     Renan Brian                                                        #####
#####     Especialista em Programação | Transformando ideias em código       #####
#####     E-mail: renanmgx@hotmail.com                                       #####
##################################################################################

from flask import Flask, request, render_template
import json


app = Flask(__name__)

def carregar_json():
    '''
    é responsavel por carregar um arquivo json contendo um dicionario com dados de login no sap.
    caso o arquivo não estiver presente durante a execução irá  criar um arquivo default no lugar.
    '''
    jason_default = {"endereco" : r"C:\Users\InnerRep.PATRIMAR\OneDrive - PATRIMAR ENGENHARIA S A\inventario_DP\inventario.db"}
    while True:
        try:
            with open("serv_inventario.json", "r")as arqui:
                return json.load(arqui)
        except Exception as error:
            print(error)
            with open("serv_inventario.json", "w")as arqui:
                json.dump(jason_default, arqui)

json_config = carregar_json()

planilha = json_config["endereco"]

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
