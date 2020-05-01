import xml.dom.minidom
import xml.etree.ElementTree as ET


###########################################################################

def obtem_periodos(path):
    arquivo = path + "PeriodoDemonstracaoFinanceira.xml"
    root = ET.parse(arquivo).getroot()
    periodos = root.findall('PeriodoDemonstracaoFinanceira')

    print("PeriodoDemonstracaoFinanceira: ", len(periodos))

    for item in periodos:
        numeroIdentificacaoPeriodo = item.find('NumeroIdentificacaoPeriodo')
        dataInicioPeriodo = item.find('DataInicioPeriodo')
        dataFimPeriodo = item.find('DataFimPeriodo')
        numeroTrimestre = item.find('NumeroTrimestre')
        print(numeroIdentificacaoPeriodo.tag, numeroIdentificacaoPeriodo.text, 
              dataInicioPeriodo.tag, dataInicioPeriodo.text, 
              dataFimPeriodo.tag, dataFimPeriodo.text, 
              numeroTrimestre.tag, numeroTrimestre.text)

###########################################################################

def obtem_info_financeiras(path):
    arquivo = path + "InfoFinaDFin.xml"
    root = ET.parse(arquivo).getroot()
    infoFinaDFin = root.findall('InfoFinaDFin')

    print("InfoFinaDFin: ", len(infoFinaDFin))
    limite = 10

    for index, item in enumerate(infoFinaDFin):
        if index == limite:
            break

        numeroIdentificadorInfoFinaDFin = item.find('NumeroIdentificadorInfoFinaDFin')
        planoConta = item.find('PlanoConta')
        numeroConta = planoConta.find('NumeroConta')

        versaoPlanoConta = planoConta.find('VersaoPlanoConta')
        codigoTipoDemonstracaoFinanceira = versaoPlanoConta.find('CodigoTipoDemonstracaoFinanceira') #Domínio 50 {2: BPA, 3: BPP; 4: DRE, 5: DRA, 6: DFC-MD, 7: DFC-MI...}
        codigoTipoInformacaoFinanceira = versaoPlanoConta.find('CodigoTipoInformacaoFinanceira') #Domínio 48 {1: Individual, 2: Consolidado, 3: Individual e Consolidado}


        print("Identificador", numeroIdentificadorInfoFinaDFin.text,
              "TipoDemonstracao ", codigoTipoDemonstracaoFinanceira.text, "TipoInfo", codigoTipoInformacaoFinanceira.text)

        descricaoConta1 = item.find('DescricaoConta1')
        if descricaoConta1.text:
            valorConta1 = item.find('ValorConta1')
            valorConta2 = item.find('ValorConta2')
            valorConta3 = item.find('ValorConta3')
            print("\t", numeroConta.text, descricaoConta1.text, valorConta1.text, valorConta2.text, valorConta3.text)
        

###########################################################################

def main():
    path = ".\\Downloads\\2019 09 30 ITR COD_CVM 20800\\"
    obtem_periodos(path)
    obtem_info_financeiras(path)

if __name__ == '__main__':
    main()