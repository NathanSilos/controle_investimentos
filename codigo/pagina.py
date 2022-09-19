from ctypes import alignment
from email import header
from tkinter import Scrollbar, font
from turtle import color, left, right
from weakref import finalize
import PySimpleGUI as sg
import datetime as dt
import acompanhamento_acoes

# Decidindo o tema texto/ cores
theme_dict = {'BACKGROUND': '#2B475D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# Atribuindo os temas deifinido
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

# Defininfo cores e tamanhos
BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((10,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 12)
BPAD_RIGHT = ((10,20), (10, 20))

hoje = dt.date.today().strftime('%d/%m/%Y')

# Decidindo a parte de cima da tela
barra_titulo = [[
                sg.Text('Stock Wallet' + ' ' * 100, background_color=DARK_HEADER_COLOR), 
                sg.Button(  
                        'Atualizar',
                        size=(8, 1),    
                        enable_events=True,
                        key='atualizar',
                        pad=(5,0),
                        tooltip='Clique aqui para atualizar seus indicadores'),
                sg.Text(' ' * 70, background_color=DARK_HEADER_COLOR),
                sg.Text('Data de atualização: {}'.format(str(hoje)), justification='right', background_color=DARK_HEADER_COLOR)
            ]]

# Primeira barra apos o titulo (verificando necessidade)
# top  = [[sg.Text('The Weather Will Go Here', size=(50,1), justification='c', pad=BPAD_TOP, font='Any 20')],
#             [sg.T(f'{i*25}-{i*34}') for i in range(7)],]
df = acompanhamento_acoes.leitura_base()
# Le a base e retorna a sumarizacao
acoes_sumarizada = acompanhamento_acoes.verifica_acoes_hoje(df, sum=True)

ganho_perda_total = round(acoes_sumarizada['ganho_perda_hoje'].sum())
total_investido_atualmente = round(acoes_sumarizada['total_investido_hoje'].sum())
total_investido = round(acoes_sumarizada['total_investido_compra'].sum())

if ganho_perda_total > 0:
    texto_ganho_perda = sg.Text('Ganho:')
    valor_ganho_perda = sg.Text('{}'.format(ganho_perda_total), background_color='green')
else:
    texto_ganho_perda = sg.Text('Perda:')
    valor_ganho_perda = sg.Text('{}'.format(ganho_perda_total),background_color='red')

acompanhamento_geral = [[sg.Text('Acompanhamento Geral', font='Any 13')],
            [texto_ganho_perda, valor_ganho_perda],
            [sg.Text('Total investido: {:,}'.format(total_investido))],
            [sg.Text('Total investido hoje: {:,}'.format(total_investido_atualmente))]]
            # [sg.Image(data=sg.DEFAULT_BASE64_ICON)]  

# Bloco inferior esquerdo
bloco_compra_acao = [[sg.Text('Compra ou Venda', font='Any 13')],
            [sg.Text('Código da ação:'),],
            [sg.Input(size=(25,20), tooltip='Exemplo: ITSA4') ],
            [sg.Text('Data da compra:')],
            [sg.Input(size=(25,20), tooltip='Exemplo: 20/10/2022')],
            [sg.Text('Preço:'),],
            [sg.Input(size=(25,20), tooltip='Exemplo: 4'), ],
            [sg.Text('Quantidade:')],
            [sg.Input(size=(25,20), tooltip='Exemplo: 100')],
            [sg.Text('')],
            [sg.Button(
                'Cadastrar',
                tooltip='Preencha as informações acima para a sua nova compra de ações'
                ), 
             sg.Text(' ' * 13),
             sg.Button(
                'Venda',
                tooltip='Preencha as informações acima para a sua nova compra de ações'),
            ]
        ]

# Busca base nao sumarizada
data = acompanhamento_acoes.verifica_acoes_hoje(df, sum=False)
# header = [f'{col}' for col in range(len(data[0]))]
header = list(data.columns)
# print('\n\n\n\n\n')
# print(data)
tabela_compras = [[
                sg.Text('Tabela de Ações', font='Any 16'),
                sg.Text('Caminho da sua base de ações:', font='Any 10'), 
                sg.Input(size=(40,20)), 
                sg.FileBrowse('Buscar', key='caminho_base'),
                sg.Button('Ler Base', key='botao_caminho_base' ,tooltip='Clique aqui depois de encontrar o arquivo')],

            [sg.Table(values=data.values.tolist(), 
                        headings=header, 
                        col_widths= (10, 1),
                        # max_col_width=10,
                        # auto_size_columns=True,
                        # display_row_numbers=True,
                        justification='left',
                        # Numero de linhas da base
                        # default_element_size=(15, 1),
                        num_rows=data.shape[1],
                        alternating_row_color=sg.theme_button_color()[1],
                        key='tabela_acoes',
                        selected_row_colors='red on yellow',
                        enable_events=True,
                        # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True                        
                        # Comment out to not enable header and other clicks
                        )
                        ]]

graficos = [
    [sg.Text('Graficos', font='Any 16')],
    [sg.Canvas(size=(200, 180), key='grafico_pizza', background_color='white', )]]

layout = [[sg.Column(barra_titulo, size=(1070, 30), pad=(0,0), background_color=DARK_HEADER_COLOR)],
        #   [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          [sg.Column([[sg.Column(acompanhamento_geral, size=(200,140), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(bloco_compra_acao, size=(200,300),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
          sg.Column([[sg.Column(tabela_compras, size=(800, 220),scrollable=True)],
                    [sg.Column(graficos,size=(800, 225))]], pad=BPAD_LEFT, background_color=BORDER_COLOR)]]
        #    pad=BPAD_RIGHT

window = sg.Window('Stock Wallet', layout, margins=(0,0), background_color=BORDER_COLOR, grab_anywhere=True, finalize=True)

# Inclui o grafico de pizza no painel
acompanhamento_acoes.desenha_grafico(window['grafico_pizza'].TKCanvas, acompanhamento_acoes.gera_pizza(acoes_sumarizada))


while True:      
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'botao_caminho_base':
        print(values['caminho_base'])

    # Atualiza base para com a data mais recente
    if event == 'atualizar':
        data = acompanhamento_acoes.verifica_acoes_hoje(df, sum=False)
        window['tabela_acoes'].update(data.values.tolist())

    if event == 'tabela_acoes':
        print('tabela_acoes')
        print(event)
    if event == 'Cadastrar':
        print('\n\n\n\nCadastro')
        print(event)
window.close()