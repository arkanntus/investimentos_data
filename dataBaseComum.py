import sqlite3
from sqlite3 import Error
from datetime import datetime

###########################################################################

def converte_cvm_formato_data(date):
    return datetime.strptime(date, '%d/%m/%Y').date()

###########################################################################

def converte_itr_formato_data(date):
    # return datetime.strptime(date, '%Y-%m-%d').strftime("%d/%m/%Y")
    return datetime.strptime(date, '%Y-%m-%d').date()

###########################################################################

def cria_conexao(db_file):
    conexao = None
    try:
        conexao = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conexao

###########################################################################

def cria_tabela(conexao, create_table_sql):
    try:
        cursor = conexao.cursor()
        cursor.execute(create_table_sql)
        cursor.close()
    except Error as e:
        print(e)

###########################################################################

def apaga_tabela(conexao, table_name):
    try:
        cursor = conexao.cursor()
        cursor.execute(""" DROP TABLE """ + table_name)
        cursor.close()
    except Error as e:
        print(e)