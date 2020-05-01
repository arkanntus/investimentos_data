import sqlite3
from sqlite3 import Error
from datetime import datetime
import dataBaseComum as db


###########################################################################

def cria_tabela_modelo_fixa(conexao, tabela):
    tabela_modelo = """ CREATE TABLE IF NOT EXISTS """ + tabela + """ (
                         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                         cod_cvm INTEGER REFERENCES Company (cod_cvm),
                         id_modelo INTEGER REFERENCES ModeloPlanoContas (id),
                         data_referencia DATE NOT NULL,
                         conta VARCHAR NOT NULL,
                         descricao VARCHAR NOT NULL,
                         valor INTEGER NOT NULL
                 ); """
    cursor = conexao.cursor()
    cursor.execute(tabela_modelo)
    cursor.close()

###########################################################################

def cria_tabela_modelo(conexao, tabela):
    tabela_modelo = """ CREATE TABLE IF NOT EXISTS """ + tabela + """ (
                         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                         cod_cvm INTEGER REFERENCES Company (cod_cvm),
                         id_modelo INTEGER REFERENCES ModeloPlanoContas (id),
                         data_referencia DATE NOT NULL,
                         inicio_exercicio DATE NOT NULL,
                         fim_exercicio DATE NOT NULL,
                         conta VARCHAR NOT NULL,
                         descricao VARCHAR NOT NULL,
                         valor INTEGER NOT NULL
                 ); """
    cursor = conexao.cursor()
    cursor.execute(tabela_modelo)
    cursor.close()

###########################################################################

def cria_tabelas(conexao):
    tabela_modelo_plano_contas = """ CREATE TABLE IF NOT EXISTS ModeloPlanoContas (
                                      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                      descricao VARCHAR UNIQUE NOT NULL
                                ); """

    if conexao is not None:
        db.cria_tabela(conexao, tabela_modelo_plano_contas)
        cria_tabela_modelo(conexao, 'DRE')
        cria_tabela_modelo(conexao, 'FluxoCaixa')
        cria_tabela_modelo_fixa(conexao, 'Ativo')
        cria_tabela_modelo_fixa(conexao, 'Passivo')
    else:
       print("Erro! Não foi possivel criar uma conexão com o banco de dados.")

###########################################################################

# def cria_view_ativo_sintetico(conexao, tabela):
#     sql = """ CREATE VIEW xxxxx IF NOT EXISTS (
#                          id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
#                          cod_cvm INTEGER REFERENCES Company (cod_cvm),
#                          id_modelo INTEGER REFERENCES ModeloPlanoContas (id),
#                          data_referencia DATE NOT NULL,
#                          inicio_exercicio DATE NOT NULL,
#                          fim_exercicio DATE NOT NULL,
#                          conta VARCHAR NOT NULL,
#                          descricao VARCHAR NOT NULL,
#                          valor INTEGER NOT NULL
#                  ); """
#     cursor = conexao.cursor()
#     cursor.execute(sql)
#     cursor.close()

###########################################################################

def adiciona_dados_demonstracao(conexao, tabela, dadosTabela):
    try:
        numColunas = len(dadosTabela)
        if numColunas < 6:
            raise Exception('Os dados da tabela devem ter pelo menos 6 colunas')
        
        cod_cvm = dadosTabela[0]
        id_modelo = dadosTabela[1]
        conta = dadosTabela[2]
        data_referencia = dadosTabela[4]

        # buscaSQL = ''' SELECT * FROM ''' + tabela + ''' WHERE cod_cvm = ? AND id_modelo = ? AND conta = ? AND data_referencia = ?'''

        cursor = conexao.cursor()
        # result = cursor.execute(buscaSQL, (cod_cvm, id_modelo, conta, data_referencia))
        # demonstracao = cursor.fetchone()

        # rowid = None

        # if demonstracao:
        #     rowid = demonstracao[0]
        # else:
        params = ''' cod_cvm, id_modelo, conta, descricao, data_referencia, valor '''
        numParams = '''?, ?, ?, ?, ?, ?'''
        if numColunas > 6:
            params = params + ''', inicio_exercicio, fim_exercicio'''
            numParams = numParams + ''', ?, ?'''

        insertSQL = ''' INSERT INTO ''' + tabela + ''' ( ''' +  params + ''' ) VALUES( '''+ numParams + ''' ) '''

        cursor.execute(insertSQL, dadosTabela)
        rowid = cursor.lastrowid

        cursor.close()
        return rowid
    except Error as e:
        print(e)

###########################################################################

def adiciona_lista_dados_demonstracao(conexao, tabela, listaDadosTabela):
    for dadosTabela in listaDadosTabela:
        rowid = adiciona_dados_demonstracao(conexao, tabela, dadosTabela)
        #print('Ultimo id criado:  ', rowid)

###########################################################################

def main():
    arquivo = ".\data.db"
    conexao = db.cria_conexao(arquivo)

    with conexao:
        cria_tabelas(conexao)

        tabela = 'Ativo'
        data_referencia = db.converte_itr_formato_data('2018-12-31')
        dadosTabela = [1023, 1, '3.01', 'Receita Liquida', data_referencia, 9999.00]
        
        rowid = adiciona_dados_demonstracao(conexao, tabela, dadosTabela)
        print(rowid)

if __name__ == '__main__':
    main()