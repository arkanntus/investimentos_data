import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

###########################################################################

def get_frame_dados_companhia(codCVM):
    urlFrame = None
    try:
        root = 'http://bvmf.bmfbovespa.com.br/'
        page = requests.get(root + 'cias-listadas/empresas-listadas/ResumoEmpresaPrincipal.aspx?codigoCvm=' + str(codCVM))
        soup = BeautifulSoup(page.content, 'html.parser')
        iframe = soup.find(id = 'ctl00_contentPlaceHolderConteudo_iframeCarregadorPaginaExterna')
        iframeSrc = iframe.attrs['src'][6:]
        urlFrame = root + iframeSrc
    except:
        print("Não foi possivel obter dados para: " + page)

    return urlFrame

###########################################################################

def get_dados_companhias(urlFrame):
    response = urlopen(urlFrame)
    soup = BeautifulSoup(response, 'html.parser')
    return soup.find(id='accordionDados')

###########################################################################

def get_atividade_companhia(dadosCompanhia):
    atividade = dadosCompanhia.find("td", text = "Atividade Principal:")
    return atividade.find_next_sibling("td").text

###########################################################################

def get_classificacao_setorial_companhia(dadosCompanhia):
    classificacaoTitulo = dadosCompanhia.find("td", text = "Classificação Setorial:")
    classificacao = classificacaoTitulo.find_next_sibling("td").text
    return classificacao.split(" / ")

###########################################################################

def get_site_companhia(dadosCompanhia):
    try:
        siteTitulo = dadosCompanhia.find("td", text = "Site:")
        return siteTitulo.find_next_sibling("td").text
    except Exception as e:
        print(dadosCompanhia)
        print(e)

###########################################################################

def get_codigos_companhia(dadosCompanhia):
    tickersHtml = dadosCompanhia.findAll(href="javascript:;", class_="LinkCodNeg")
    tickers = []
    for t in tickersHtml:
        tickers.append(t.text)
    return tickers

###########################################################################

def main(codCVM = ""):
    urlFrame = ""
    if codCVM:
        urlFrame = get_frame_dados_companhia(codCVM)
    else:
        urlFrame = 'file:///D:/Projetos/investimentos/data/Requests%20Testes/ExecutaAcaoConsultaInfoEmp.htm'

    dadosCompanhia = get_dados_companhias(urlFrame)
    classificacao = get_classificacao_setorial_companhia(dadosCompanhia)
    atividade = get_atividade_companhia(dadosCompanhia)
    tickers = get_codigos_companhia(dadosCompanhia)
    site = get_site_companhia(dadosCompanhia)

    print(classificacao)
    print(tickers)
    print(site)
    print(atividade)


if __name__ == '__main__':
    main() #KLABIN
    # main(23590) #WIZ
    # main(11592)   #UNIPAR