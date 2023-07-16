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
def adicionar_dados_excel(planilha, nome_computador="None", nome_usuario="None", modelo_processador="None",
                          ram_total="None", ram_usado="None", sistema_operacional="None",
                          armazenamento_total="None", armazenamento_disponivel="None", tipo_maquina="None",
                          antivirus="None", criptografia="None", id_dispositivo="None", uso_processador="None",
                          wifi="None", data="None", placa_mae="None", placa_mae_serial="None"):
    
    banco_dados = nome_computador + ";:;"
    banco_dados = banco_dados + nome_usuario + ";:;"
    banco_dados = banco_dados + modelo_processador + ";:;"
    banco_dados = banco_dados + ram_total + ";:;"
    banco_dados = banco_dados + ram_usado + ";:;"
    banco_dados = banco_dados + sistema_operacional + ";:;"
    banco_dados = banco_dados + armazenamento_total + ";:;"
    banco_dados = banco_dados + armazenamento_disponivel + ";:;"
    banco_dados = banco_dados + tipo_maquina + ";:;"
    banco_dados = banco_dados + antivirus + ";:;"
    banco_dados = banco_dados + criptografia + ";:;"
    banco_dados = banco_dados + id_dispositivo + ";:;"
    banco_dados = banco_dados + uso_processador + ";:;"
    banco_dados = banco_dados + wifi + ";:;"
    banco_dados = banco_dados + data + ";:;"
    banco_dados = banco_dados + placa_mae + ";:;"
    banco_dados = banco_dados + placa_mae_serial + ";:;"

    
    with open(planilha, "a") as db:
        db.write(banco_dados + "\n")





def iniciar(dados):
    adicionar_dados_excel(planilha, nome_computador=dados["nome_computador"], nome_usuario=dados["nome_usuario"],
                          modelo_processador=dados["modelo_processador"], ram_total=dados["ram_total"],
                          ram_usado=dados["ram_usado"], sistema_operacional=dados["sistema_operacional"],
                          armazenamento_total=dados["armazenamento_total"],
                          armazenamento_disponivel=dados["armazenamento_disponivel"],
                          tipo_maquina=dados["tipo_maquina"], antivirus=dados["antivirus"],
                          criptografia=dados["criptografia"], id_dispositivo=dados["id_dispositivo"],
                          uso_processador=dados["uso_processador"], wifi=dados["wifi"], data=dados["data"],
                          placa_mae=dados["placa_mae"], placa_mae_serial=dados["placa_mae_serial"])



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
