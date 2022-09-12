from pandas_datareader import data as web
import pandas as pd
import datetime as dt
import datetime as dt

def leitura_base():
    base_compra = pd.read_csv(r'C:\Users\natha\Documents\01-Projetos\carteira_ações\base_compras_acoes.csv')
    
    return base_compra

def verifica_acoes_hoje(base, sum):
    base_compra = base
    acoes = base_compra['Codigo'].unique()

    base_sumarizada = base_compra.groupby(['Codigo']).sum(['Valor Compra','Quantidade'])
    base_sumarizada

    # Busca as datas a serem usadas na consulta
    hoje = dt.date.today().strftime('%m/%d/%Y')

    # Leva para a dia util mais recente
    if dt.date.today().weekday() == 6:
        n = 2
    else:
        n = 1

    ontem = dt.date.today() - dt.timedelta(n)
    ontem = ontem.strftime('%m/%d/%Y')

    # dividendos = pd.DataFrame()
    cotacao = pd.DataFrame()

    for acao in acoes:
        temp = web.DataReader(
                        acao + '.SA',
                        data_source='yahoo',
                        start=ontem,
                        end=hoje)
        temp['acao'] = acao
        cotacao = cotacao.append(temp)

        # Busca os casos de dividendos (em construção)
        # temp = web.DataReader(
        #                 acao + '.SA',
        #                 data_source='yahoo-dividends',
        #                 start=hoje,
        #                 end=hoje)
        # temp['acao'] = acao
        # dividendos = dividendos.append(temp)
        
    cotacao.reset_index()

    cotacao = cotacao.drop(columns=['High','Low','Open','Volume'])

    base_completa = base_compra.merge(cotacao, how='left', left_on=['Codigo'], right_on=['acao'])
    base_completa

    base_completa['fechamento']= base_completa['Close'].round(2)
    base_completa['preco_ajustado']= base_completa['Adj Close'].round(2)

    base_completa['Valor Compra'] = base_completa['Valor Compra'].str.replace(',','.')
    base_completa['Valor Compra'] = pd.to_numeric(base_completa['Valor Compra'])

    base_completa.drop(columns=['Close','Adj Close','acao'],inplace=True)

    base_completa['total_investido_compra'] = base_completa['Valor Compra'] * base_completa['Quantidade']
    base_completa['total_investido_hoje'] = base_completa['fechamento'] * base_completa['Quantidade']

    base_completa['ganho_perda_hoje'] = base_completa['total_investido_hoje'] - base_completa['total_investido_compra'] 
    base_completa['ganho_perda_hoje_percentual'] = round((base_completa['ganho_perda_hoje'] / base_completa['total_investido_compra']) *100, 2)

    base_completa['total_investido_compra']= base_completa['total_investido_compra'].round(2)
    base_completa['total_investido_hoje']= base_completa['total_investido_hoje'].round(2)
    base_completa['ganho_perda_hoje']= base_completa['ganho_perda_hoje'].round(2)

    if sum == False:
        return base_completa

    # Funcao sumarizada
    base_completa2 = base_completa.drop(columns=[ 'data_compra',
        'Valor Compra', 'Quantidade', 'fechamento', 'preco_ajustado','ganho_perda_hoje_percentual'])

    base_completa2.groupby(['Tipo de investimento', 'Especidade', 'Codigo', 'Setor']).sum().reset_index()

    if sum:
        return base_completa2