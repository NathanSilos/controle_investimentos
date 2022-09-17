import PySimpleGUI as sg
import acompanhamento_acoes
import datetime as dt

class Dash:

    def __init__(self, barra_titulo, bloco_compra_acao, bloco_acompanhamento_geral, bloco_tabela_acoes):
        self.barra_titulo
        self.bloco_compra_acao
        self.bloco_acompanhamento_geral
        self.bloco_tabela_acoes
    
    def set_barra_titulo(self, barra_titulo):
        hoje = dt.date.today().strftime('%d/%m/%Y')
        DARK_HEADER_COLOR = '#1B2838'
        self.set_barra_titulo = [[sg.Text('Stock Wallet' + ' ' * 90, background_color=DARK_HEADER_COLOR), 
                sg.Button('Atualizar',
                          size=(8, 1),    
                          enable_events=True,
                          key='atualizar',
                          pad=(5,0),
                          tooltip='Clique aqui para atualizar seus indicadores'),
                sg.Text(' ' * 63, background_color=DARK_HEADER_COLOR),
                sg.Text('Data de atualização: {}'.format(str(hoje)), background_color=DARK_HEADER_COLOR)
            ]]
    
    def set_bloco_compra_acao(self, bloco_compra_acao):
        self.set_bloco_compra_acao

        