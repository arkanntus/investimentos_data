import dataBaseCompany as db
import requestCompanyRegistrationData as rq
from sqlite3 import Error

###########################################################################

def updateCompanyRegistrationData(connection, codCVM):
    try:
        with connection:
            urlFrame = rq.get_frame_dados_companhia(codCVM)
            dadosCompanhia = None
            if urlFrame:
                dadosCompanhia = rq.get_dados_companhias(urlFrame)

            sectors = []
            if dadosCompanhia:
                sectors = rq.get_classificacao_setorial_companhia(dadosCompanhia)
                
                website = rq.get_site_companhia(dadosCompanhia)
                db.update_website_comcod_cvmonnection, codCVM, website)
                
                main_activity = rq.get_atividade_companhia(dadosCompanhia)
                db.atualiza_atividade_principal_conpanhia(connection, codCVM, main_activity)
                
                tickers = rq.get_codigos_companhia(dadosCompanhia)
                if len(tickers) > 0:
                    db.adiciona_tickers(connection, codCVM, tickers)
            else:
                sectors = ['Invalid', 'Invalid', 'Invalid']
            
            db.add_sectors_into_company(connection, codCVM, sectors)
            
            company = db.seleciona_companhia_por_COD_CVM(connection, codCVM)
            company_segment = company[1]
            sector_consult = db.select_sectors_name(connection, company_segment)
            ticker_consult = db.seleciona_tickers_por_companhia(connection, codCVM)
            
            success = "Sucesso" if dadosCompanhia else "Erro" 
            print(success, company[0], company[2], company[5], company[6], " - ", 
                  sector_consult[1], "/", sector_consult[3], "/", sector_consult[5], ticker_consult)
    except Error as e:
        print(e)
        urlFrame = rq.get_frame_dados_companhia(codCVM)
        print("Erro ver urlFrame: ", urlFrame)

###########################################################################

def updateCompaniesRegistrationData(connection, codigosCVM):
    db.cria_tabelas(connection)
    for codCVM in codigosCVM:
        updateCompanyRegistrationData(connection, codCVM)

#############################################################cod_cvm########

def raiseCodOfCompaniesWithoutRegisteredSectors(connection, limit = -1):
    # sql = """ SELECT cod_cvm FROM company WHERE id_segment is null limit (?); """
    sql = """ SELECT cod_cvm FROM company WHERE id_segment != 0 AND main_activity is null limit (?); """
    codigosCVM = []

    cursor = connection.cursor()
    cursor.execute(sql, [limit])
    records = cursor.fetchall()
    for row in records:
        codigosCVM.append(row[0])
    
    cursor.close()
    return codigosCVM

###########################################################################

def main():
    dbPath = ".\data.db"
    connection = db.create_connection(dbPath)
    db.cria_tabelas(connection)
    codigosCVM = raiseCodOfCompaniesWithoutRegisteredSectors(connection)
    updateCompaniesRegistrationData(connection, codigosCVM)

if __name__ == '__main__':
    main()