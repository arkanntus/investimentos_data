import xml.dom.minidom
import xml.etree.ElementTree as ET

###########################################################################

def identificacao_periodo(codigo):
    codigos = {
        1: 'Exercício social em curso',
        2: 'Trimestre atual',
        3: 'Exercício social anterior',
        4: 'Igual ao trimestre do exercício anterior'
    }
    return codigos.get(codigo, 'Período inválido.')

###########################################################################

def obtem_periodos(path):
    arquivo = path + "PeriodoDemonstracaoFinanceira.xml"
    root = ET.parse(arquivo).getroot()
    periodos = root.findall('PeriodoDemonstracaoFinanceira')

    print("PeriodoDemonstracaoFinanceira: ", len(periodos))

    for item in periodos:
        # {1: Exercício social em curso, 2: Trimestre atual, 3: Exercício social anterior, 4: Igual ao trimestre do exercício anterior}
        numeroIdentificacaoPeriodo = item.find('NumeroIdentificacaoPeriodo') 
        periodo = identificacao_periodo(int(numeroIdentificacaoPeriodo.text))
        dataInicioPeriodo = item.find('DataInicioPeriodo')
        dataFimPeriodo = item.find('DataFimPeriodo')
        numeroTrimestre = item.find('NumeroTrimestre')
        print(dataInicioPeriodo.tag, dataInicioPeriodo.text, 
              dataFimPeriodo.tag, dataFimPeriodo.text, 
              numeroTrimestre.tag, numeroTrimestre.text,
              periodo, numeroIdentificacaoPeriodo.text)

###########################################################################

def tipo_demostracao(codigo):
    codigos = {
        1: 'Informação Financeira',
        2: 'Balanço Patrimonial Ativo',
        3: 'Balanço Patrimonial Passivo',
        4: 'Demonstração do Resultado',
        5: 'Demonstração de Resultado Abrangente',
        6: 'Demonstração do Fluxo de Caixa (Método Direto)',
        7: 'Demonstração do Fluxo de Caixa (Método Indireto)',
        8: 'Demonstração das Mutações do Patrimônio Líquido',
        9: 'Demonstração de Valor Adicionado'
    }
    return codigos.get(codigo, 'Código inválido.')

###########################################################################

def obtem_info_financeiras(path):
    arquivo = path + "InfoFinaDFin.xml"
    root = ET.parse(arquivo).getroot()
    infoFinaDFin = root.findall('InfoFinaDFin')

    print("InfoFinaDFin: ", len(infoFinaDFin))
    limite = 1000

    for index, item in enumerate(infoFinaDFin):
        planoConta = item.find('PlanoConta')
        versaoPlanoConta = planoConta.find('VersaoPlanoConta')
        codigoTipoInformacaoFinanceira = versaoPlanoConta.find('CodigoTipoInformacaoFinanceira') #Domínio 48 {1: Individual, 2: Consolidado, 3: Individual e Consolidado}
        codigoTipoDemonstracaoFinanceira = versaoPlanoConta.find('CodigoTipoDemonstracaoFinanceira') #Domínio 50 {2: BPA, 3: BPP; 4: DRE, 5: DRA, 6: DFC-MD, 7: DFC-MI...}

        if codigoTipoInformacaoFinanceira.text == '2' and codigoTipoDemonstracaoFinanceira.text == '4':
            # if index == limite:
            #     break

            numeroIdentificadorInfoFinaDFin = item.find('NumeroIdentificadorInfoFinaDFin')
            numeroConta = planoConta.find('NumeroConta')

            tipoDemonstracaoStr = tipo_demostracao(int(codigoTipoDemonstracaoFinanceira.text))

            #print(tipoDemonstracaoStr, "TipoInfo", codigoTipoInformacaoFinanceira.text, "Identificador", numeroIdentificadorInfoFinaDFin.text)

            descricaoConta1 = item.find('DescricaoConta1')
            valorConta1 = item.find('ValorConta1')
            valorConta2 = item.find('ValorConta2')
            valorConta3 = item.find('ValorConta3')
            valorConta4 = item.find('ValorConta4')
            valorConta5 = item.find('ValorConta5')
            valorConta6 = item.find('ValorConta6')
            valorConta7 = item.find('ValorConta7')
            valorConta8 = item.find('ValorConta8')
            valorConta9 = item.find('ValorConta9')
            valorConta10 = item.find('ValorConta10')
            valorConta11 = item.find('ValorConta11')
            valorConta12 = item.find('ValorConta12')
            print(numeroConta.text, descricaoConta1.text, 
                  float(valorConta1.text), float(valorConta2.text), float(valorConta3.text),
                  float(valorConta4.text), float(valorConta5.text), float(valorConta6.text),
                  float(valorConta7.text), float(valorConta8.text), float(valorConta9.text),
                  float(valorConta10.text), float(valorConta11.text), float(valorConta12.text))
    

###########################################################################

def main():
    # path = ".\\Downloads\\2019 09 30 ITR COD_CVM 20800\\" #Tegma
    # path = ".\\Downloads\\2019 09 30 ITR COD_CVM 19879\\" #LIGT3
    # path = ".\\Downloads\\2019 12 31 DFP COD_CVM 20257\\" #Taesa
    path = ".\\Downloads\\COD_CVM 21431\\2019 12 31 DFP\\" #Hypera
    path = ".\\Downloads\\COD_CVM 21431\\2020 03 31 ITR\\" #Hypera
    path = ".\\Downloads\\COD_CVM 21431\\2019 09 30 ITR\\" #Hypera
    path = ".\\Downloads\\COD_CVM 21431\\2019 06 30 ITR\\" #Hypera
    path = ".\\Downloads\\COD_CVM 21431\\2019 03 31 ITR\\" #Hypera

    obtem_periodos(path)
    obtem_info_financeiras(path)

if __name__ == '__main__':
    main()