import sqlite3
from sqlite3 import Error
from datetime import datetime
import dataBaseComum as db

###########################################################################

def seleciona_companhia_por_id(conexao, id_companhia):
    sql = """ SELECT * FROM Companhia WHERE id = (?); """

    cursor = conexao.cursor()
    cursor.execute(sql, [id_companhia])
    
    companhia = cursor.fetchone()
    cursor.close()
    return companhia

###########################################################################

def seleciona_companhia_por_COD_CVM(conexao, cod_cvm):
    sql = """ SELECT * FROM Companhia WHERE cod_cvm = (?); """

    cursor = conexao.cursor()
    cursor.execute(sql, [cod_cvm])

    companhia = cursor.fetchone()
    cursor.close()
    return companhia

###########################################################################

def seleciona_nome_setores(conexao, id_segmento):
    sql = """ SELECT 
                setor.id AS id_setor, setor.nome AS nome_setor, 
                subsetor.id AS id_subsetor, subsetor.nome AS nome_subsetor, 
                segmento.id AS id_segmento, segmento.nome AS nome_segmento
            FROM Segmento
            INNER JOIN Subsetor ON subsetor.id = segmento.id_subsetor
            INNER JOIN Setor ON setor.id = subsetor.id_setor
            WHERE segmento.id = (?); """

    cursor = conexao.cursor()
    cursor.execute(sql, [id_segmento])

    setores = cursor.fetchone()
    cursor.close()
    return setores

###########################################################################

def seleciona_setor_por_nome(conexao, tabela, nome):
    sql = """ SELECT * FROM Setor WHERE nome = ? """
    
    if tabela == 'Segmento':
        sql = """ SELECT * FROM Segmento WHERE nome = ? """
    elif tabela == 'Subsetor':
        sql = """ SELECT * FROM Subsetor WHERE nome = ? """

    cursor = conexao.cursor()
    cursor.execute(sql, [nome])

    setor = cursor.fetchone()
    cursor.close()
    return setor

###########################################################################

def seleciona_tickers_por_companhia(conexao, cod_cvm):
    sql = """ SELECT ticker FROM Tickers WHERE cod_cvm = (?); """

    cursor = conexao.cursor()
    cursor.execute(sql, [cod_cvm])

    records = cursor.fetchall()
    cursor.close()
    return records

###########################################################################

def adiciona_setor(conexao, nome_setor):
    try:
        setor = seleciona_setor_por_nome(conexao, 'Setor', nome_setor)
        setor_id = None

        if setor:
            setor_id = setor[0]
        else:
            sql = """ INSERT INTO Setor (nome) VALUES (?); """
            cursor = conexao.cursor()
            cursor.execute(sql, [nome_setor])

            setor_id = cursor.lastrowid
            cursor.close()

        return setor_id
    except Error as e:
        print(e)

###########################################################################

def adiciona_subsetor(conexao, id_setor, nome_subsetor):
    try:
        subsetor = seleciona_setor_por_nome(conexao, 'Subsetor', nome_subsetor)
        id_subsetor = None

        if subsetor:
            id_subsetor = subsetor[0]
        else:
            sql = """ INSERT INTO Subsetor (id_setor, nome) VALUES (?, ?); """
            cursor = conexao.cursor()
            cursor.execute(sql, (id_setor, nome_subsetor))
            id_subsetor =  cursor.lastrowid
            cursor.close()

        return id_subsetor
    except Error as e:
        print(e)

###########################################################################

def adiciona_segmento(conexao, id_subsetor, nome_segmento):
    try:
        segmento = seleciona_setor_por_nome(conexao, 'Segmento', nome_segmento)
        id_segmento = None
        if segmento:
            id_segmento = segmento[0] 
        else:
            sql = """ INSERT INTO Segmento (id_subsetor, nome) VALUES (?, ?); """
            cursor = conexao.cursor()
            cursor.execute(sql, (id_subsetor, nome_segmento))
            id_segmento = cursor.lastrowid
            cursor.close()

        return id_segmento
    except Error as e:
        print(e)

###########################################################################

def adiciona_setores(conexao, setores):
    try:
        if len(setores) != 3:
            raise Exception('A lista de Setores precisa de 3 items')

        cursor = conexao.cursor()
        
        nome_setor = setores[0]
        id_setor = adiciona_setor(conexao, nome_setor)
       
        nome_subsetor = setores[1]
        id_subsetor = adiciona_subsetor(conexao, id_setor, nome_subsetor)
    
        nome_segment = setores[2]
        id_segmento = adiciona_segmento(conexao, id_subsetor, nome_segment)

        conexao.commit()
        return [id_setor, id_subsetor, id_segmento]
    except Error as e:
        print(e)

###########################################################################

def atualiza_setores_companhia(conexao, cod_cvm, id_setores):
    try:
        sql =  """ UPDATE Companhia 
                   SET id_segmento = (?)
                   WHERE cod_cvm = (?); """

        cursor = conexao.cursor()
        sql_params = (id_setores[2], cod_cvm)
        
        cursor.execute(sql, sql_params)
        cursor.close()
    except Error as e:
        print(e)

###########################################################################

def add_setores_into_company(conexao, cod_cvm, setores):
    id_setores = adiciona_setores(conexao, setores)
    atualiza_setores_companhia(conexao, cod_cvm, id_setores)

###########################################################################

def atualiza_atividade_principal_conpanhia(conexao, cod_cvm, atividade_principal):
    try:
        sql =  """ UPDATE Companhia 
                   SET atividade_principal = (?)
                   WHERE cod_cvm = (?); """

        cursor = conexao.cursor()
        sql_params = (atividade_principal, cod_cvm)
        
        cursor.execute(sql, sql_params)
        cursor.close()
    except Error as e:
        print(e)
        

###########################################################################

def atualiza_website_companhia(conexao, cod_cvm, website):
    try:
        sql =  """ UPDATE Companhia 
                   SET website = (?)
                   WHERE cod_cvm = (?); """

        cursor = conexao.cursor()
        sql_params = (website, cod_cvm)
        
        cursor.execute(sql, sql_params)
        cursor.close()
    except Error as e:
        print(e)

###########################################################################

def adiciona_tickers(conexao, cod_cvm, tickers):
    try:
        if len(tickers) < 1:
            raise Exception('Tickers list does not have any items')

        sql = """ INSERT INTO tickers (cod_cvm, ticker) VALUES(?,?) """
        cursor = conexao.cursor()

        for ticker in tickers:
            sql_params = (cod_cvm, ticker)
            cursor.execute(sql, sql_params)
        
        cursor.close()
    except Error as e:
        print(e)

###########################################################################

def cria_tabelas(conexao):
    sql_cria_setor_tabela =  """ CREATE TABLE IF NOT EXISTS Setor (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                   nome VARCHAR UNIQUE NOT NULL
                             ); """
    sql_cria_subsetor_tabela =  """ CREATE TABLE IF NOT EXISTS Subsetor (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                        id_setor INT REFERENCES Setor (id), 
                                        nome VARCHAR UNIQUE NOT NULL
                                ); """
    sql_cria_segmento_tabela =  """ CREATE TABLE IF NOT EXISTS Segmento (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                        id_subsetor INT REFERENCES Subsetor (id),
                                        nome VARCHAR UNIQUE NOT NULL
                                ); """
    sql_cria_compania_tabela =  """ CREATE TABLE IF NOT EXISTS Companhia (
                                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                       cod_cvm INTEGER NOT NULL UNIQUE,
                                       nome VARCHAR NOT NULL,
                                       nome_comercial VARCHAR NOT NULL,
                                       data_fundacao DATE,
                                       cnpj INTEGER NOT NULL UNIQUE,
                                       website VARCHAR,
                                       atividade_principal TEXT,
                                       id_segment INT REFERENCES Segmento (id)
                                ); """
    sql_cria_tickers_tabela =  """ CREATE TABLE IF NOT EXISTS Tickers (
                                      id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                      cod_cvm INTEGER REFERENCES Companhia (cod_cvm),
                                      ticker VARCHAR UNIQUE NOT NULL
                               ); """

    if conexao is not None:
        db.cria_tabela(conexao, sql_cria_setor_tabela)
        db.cria_tabela(conexao, sql_cria_subsetor_tabela)
        db.cria_tabela(conexao, sql_cria_segmento_tabela)
        db.cria_tabela(conexao, sql_cria_compania_tabela)
        db.cria_tabela(conexao, sql_cria_tickers_tabela)
    else:
        print("Error! cannot create the database connection.")

###########################################################################

def adiciona_companhia(conexao, companhia):
    try:
        sql = ''' INSERT INTO Companhia (cod_cvm, nome, nome_comercial, data_fundacao, cnpj) VALUES (?,?,?,?,?) '''
        cursor = conexao.cursor()
        cursor.execute(sql, companhia)
        return cursor.lastrowid
    except Error as e:
        print(e)
    return -1

###########################################################################

def adiciona_companhias(conexao, companhias):
    for companhia in companhias:
        last_id = adiciona_companhia(conexao, companhia)
        print('Last id created ', last_id)

###########################################################################

def atualiza_data_fundacao_companhia(conexao, companhias):
    try:
        cursor = conexao.cursor()
        for companhia in companhias:
            cod_cvm = str(companhia[0])
            data_fundacao_str = companhia[3]
            if data_fundacao_str:
                data_fundacao = db.converte_cvm_formato_data(data_fundacao_str)
                sql = ''' UPDATE Companhia SET data_fundacao = (?) WHERE cod_cvm = (?)'''
                sql_params = (data_fundacao, cod_cvm)
                cursor.execute(sql, sql_params)
                
                r = seleciona_companhia_por_COD_CVM(conexao, cod_cvm)
                print(r)
            else:
                print('Data de fundação em branco.', companhia)

        cursor.close()
        conexao.commit()
    except Error as e:
        print(e)

###########################################################################

def main():
    arquivo = ".\data.db"
    conexao = db.cria_conexao(arquivo)
    cria_tabelas(conexao)

    with conexao:
        setores = ['Materiais Básicos', ' Madeira e Papel', 'Embalagens']  
        setores_id = adiciona_setores(conexao, setores)
        
        r = seleciona_nome_setores(conexao, setores_id[2])
        print(r)

if __name__ == '__main__':
    main()