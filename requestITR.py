import requests
import os.path
import xml.etree.ElementTree as ET

import urllib.request
import wget

# import zipfile, io
from datetime import datetime

###########################################################################

def requestXML(_data, arquivo, tipoDocumento):
    data = {
        "txtLogin" : "397dwlama",
        "txtSenha" : "19E72C72", 
        "txtData" : _data, 
        "txtHora" : "00:00", 
        "txtAssuntoIPE": "SIM",
        "txtDocumento" : tipoDocumento
    }

    url = 'http://seguro.bmfbovespa.com.br/rad/download/SolicitaDownload.asp'

    r = requests.post( url = url, data = data )

    with open(arquivo, 'wb') as file:
        file.write(r.content)

###########################################################################

def downloadZIP(links):
    for k, v in links.items():
        nome_arquivo = ".\\Downloads\\" + k +".zip"
        # urllib.request.urlretrieve(v, ".\\Downloads\\" + nome_arquivo)
        wget.download(v, nome_arquivo)
        print("Finalizado arquivo: " + nome_arquivo)

###########################################################################

def existeArquivo(nome_arquivo):
    return os.path.isfile(nome_arquivo)

###########################################################################

def linksCVM(file):
    links = {}
    root = ET.parse(file).getroot()
    for type_tag in root.findall('Link'):
        documento = type_tag.get('Documento')
        if documento == "ITR" or documento == "DFP": 
            url = type_tag.get('url')
            data = type_tag.get('DataRef')
            data = datetime.strptime(data, '%d/%m/%Y').date()
            cod_cvm = int(type_tag.get('ccvm'))
            nome_arquivo = data.strftime('%Y %m %d') + " " + documento + " COD_CVM " + str(cod_cvm)
            
            if not existeArquivo(nome_arquivo):
                links.update({nome_arquivo : url})
    return links

###########################################################################

def main():
    data = "08/11/2019"
    arquivo = "file.xml"
    tipoDocumento = "TODOS"
    
    # requestXML(data, arquivo, tipoDocumento)
    # print("Terminado requestXML")

    links = linksCVM(arquivo)
    print("Terminado linksCVM", len(links))

    # for k, v in links.items():
    #     print(k, v)

    downloadZIP(links)
    print("Terminado downloadZIP")

###########################################################################

if __name__ == '__main__':
    main()