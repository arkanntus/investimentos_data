import csv
import sys
import dataBaseComum as dbc
import dataBaseITR as dbi

###########################################################################

def nome_arquivo(tabela):
    if tabela == 'DRE':
        return 'itr_cia_aberta_dre_con_'
    elif tabela == 'FluxoCaixa':
        return 'itr_cia_aberta_dfc_mi_con_'
    elif tabela == 'Ativo':
        return 'itr_cia_aberta_bpa_con_'
    elif tabela == 'Passivo':
        return 'itr_cia_aberta_bpp_con_'
    else:
        return ''

###########################################################################

def obtem_dados(arquivo, considUltimo, tabelaCompleta):
    dados = []
    ordem_exercicio = 'ÚLTIMO' if considUltimo else 'PENÚLTIMO'
    try:
        with open(arquivo, 'rt', encoding='ansi') as arquivoCSV:
            reader = csv.DictReader(arquivoCSV, delimiter=';', quotechar='"')
            for row in reader:
                exercicio = row['ORDEM_EXERC']
                if exercicio == ordem_exercicio:
                    cod_cvm = int(row['CD_CVM'])
                    idModeloPlanoContas = 1
                    cod_conta = row['CD_CONTA']
                    descricao = row['DS_CONTA']
                    data_referencia = row['DT_FIM_EXERC']
                    data_referencia = dbc.converte_itr_formato_data(data_referencia)
                    valor = float(row['VL_CONTA'])

                    if tabelaCompleta:
                        inicio_exercicio = row['DT_INI_EXERC']
                        inicio_exercicio = dbc.converte_itr_formato_data(inicio_exercicio)

                        linha = (cod_cvm, idModeloPlanoContas, cod_conta, descricao, data_referencia, valor, inicio_exercicio, data_referencia)
                        dados.append(linha)
                    else:
                        linha = (cod_cvm, idModeloPlanoContas, cod_conta, descricao, data_referencia, valor)
                        dados.append(linha)
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
    except: #handle other exceptions such as attribute errors
        print("Unexpected error:", sys.exc_info()[0])
    return dados

###########################################################################

def adiciona_dados_ITR(tabela, ano, considUltimo = True):
    if tabela:
        arquivo = nome_arquivo(tabela)
        if arquivo:
            arquivoDB = ".\data.db"
            arquivoCSV = ".\Dados CVM\\" + ano + "\\" + arquivo + ano + ".csv"
            tabelaCompleta = tabela != 'Ativo' and tabela != 'Passivo'

            conexao = dbc.cria_conexao(arquivoDB)
            with conexao:
                dbi.cria_tabelas(conexao)
                dados = obtem_dados(arquivoCSV, considUltimo, tabelaCompleta)

                dbi.adiciona_lista_dados_demonstracao(conexao, tabela, dados)
                print("Terminado para ", tabela, " no ano ", ano, ". Tamanho: ", len(dados))
        else:
            print('Tabela informada é inválida')
    else:
        print('Informar a tabela para execução')

###########################################################################

def main():
    tabela = sys.argv[1] if len(sys.argv) > 1 else ''

    adiciona_dados_ITR(tabela, '2011', False)

    anos = range(2011, 2020)
    for ano in anos:
        adiciona_dados_ITR(tabela, str(ano))

if __name__ == '__main__':
    main()