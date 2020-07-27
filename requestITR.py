import requests
import os.path
import xml.etree.ElementTree as ET
import wget
from pathlib import Path

# import zipfile, io
from datetime import datetime

###########################################################################

def requestXML(_data, arquivo, tipoDocumento):

    # url = 'http://seguro.bmfbovespa.com.br/rad/download/SolicitaDownload.asp'

    # r = requests.post( url = url, data = data )

    # with open(arquivo, 'wb') as file:
    #     file.write(r.content)

###########################################################################

def existeArquivo(nome_arquivo):
    return os.path.isfile(nome_arquivo)

###########################################################################

def downloadZIP(file):
    root = ET.parse(file).getroot()
    for type_tag in root.findall('Link'):
        documento = type_tag.get('Documento')
        if documento == "ITR" or documento == "DFP": 
            url = type_tag.get('url')
            data = type_tag.get('DataRef')
            data = datetime.strptime(data, '%d/%m/%Y').date()
            cod_cvm = int(type_tag.get('ccvm'))
            cod_cvm_str = "COD_CVM " + str(cod_cvm)
            
            caminho = ".\\Downloads\\" + cod_cvm_str + "\\"
            Path(caminho).mkdir(parents=True, exist_ok=True)

            nome_arquivo = data.strftime('%Y %m %d') + " " + documento + ".zip"
            caminho_completo = caminho + nome_arquivo

            print(nome_arquivo, existeArquivo(caminho_completo))
            
            if not existeArquivo(caminho_completo):
                wget.download(url, caminho_completo)
                print(" Finalizado arquivo: '" + nome_arquivo + "' " + cod_cvm_str)
            else:
                print("Arquivo '" + nome_arquivo + "' baixado anteriormente!!!")

###########################################################################

def main():
    data = "25/04/2019"
    arquivo = "file.xml"
    tipoDocumento = "ITR"
    
    requestXML(data, arquivo, tipoDocumento)
    print("Terminado requestXML")

    downloadZIP(arquivo)
    print("Terminado downloadZIP")

###########################################################################

if __name__ == '__main__':
    main()