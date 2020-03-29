import csv
import dataBaseCompany as db

file = '.\Dados CVM\SPW_CIA_ABERTA.txt'
path = ".\data.db"

###########################################################################

def obtem_dados(file):
    companhias = []
    with open(file, 'rt', encoding='ansi') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
        for row in reader:
            situacaoRegistro = row['SIT_REG']

            if situacaoRegistro == 'ATIVO':
                cod_cvm = int(row['CD_CVM'])
                denominacaoSocial = row['DENOM_SOCIAL']
                denominacaoComercial = row['DENOM_COMERC']
                cnpjEmpresa = int(row['CNPJ'])
                dataConstituicao = row['DT_CONST']

                companhia = (cod_cvm, denominacaoSocial, denominacaoComercial, dataConstituicao, cnpjEmpresa)
                companhias.append(companhia)
    return companhias

###########################################################################

def adiciona_companhias():
    companhias = obtem_dados(file)
    conexao = db.cria_conexao(path)
    db.cria_tabelas(conexao)
    with conexao:
        db.adiciona_companhias(conexao, companhias)
        conexao.commit()

###########################################################################

def atualiza_data_fundacao_companhias():
    companhias = obtem_dados(file)
    conexao = db.cria_conexao(path)
    with conexao:
        db.atualiza_data_fundacao_companhia(conexao, companhias)

###########################################################################

if __name__ == '__main__':
    atualiza_data_fundacao_companhias()