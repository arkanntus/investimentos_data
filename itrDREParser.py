import csv
from datetime import datetime

_file = '.\Dados CVM\ITR_CIA_ABERTA_DRE_con_2018.csv'
minData = datetime.strptime('2018-01-01', '%Y-%m-%d').date()
maxData = datetime.strptime('2018-12-31', '%Y-%m-%d').date()
_exercicio = 'ÚLTIMO'
_codCVMEmpresa = 23590 #WIZ

with open(_file, 'rt', encoding='ansi') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        dataReferencia = row['DT_REFER']
        codCVMEmpresa = int(row['CD_CVM'])
        tipoDemonstrativo = row['GRUPO_DFP']
        exercicio = row['ORDEM_EXERC']
        dataInicioExercio = row['DT_INI_EXERC']
        dataFimExercio = row['DT_FIM_EXERC']
        codConta = row['CD_CONTA']
        descricaoConta = row['DS_CONTA']
        valorConta = row['VL_CONTA']

        if codCVMEmpresa == _codCVMEmpresa and exercicio == _exercicio:
            if minData <= datetime.strptime(dataReferencia, '%Y-%m-%d').date() <= maxData:
                print(dataReferencia, codCVMEmpresa, tipoDemonstrativo, exercicio, dataInicioExercio, dataFimExercio, codConta, valorConta )