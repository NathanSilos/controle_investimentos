from email import header
from tkinter import Scrollbar
from turtle import color
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
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))

hoje = dt.date.today().strftime('%d/%m/%Y')

# Decidindo a parte de cima da tela
barra_titulo = [[sg.Text('Stock Wallet' + ' ' * 165, background_color=DARK_HEADER_COLOR),
               sg.Text('Data de atualização: {}'.format(str(hoje)), background_color=DARK_HEADER_COLOR)]]

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
    valor_ganho_perda = sg.Text('{}'.format(ganho_perda_total), font='Any 12', background_color='green')
else:
    texto_ganho_perda = sg.Text('Perda:')
    valor_ganho_perda = sg.Text('{}'.format(ganho_perda_total), font='Any 12',background_color='red')

# Bloco inferior esquerdo
bloco_compra_acao = [[sg.Text('Insira aqui sua compra de ação', font='Any 13')],
            [sg.Text('Código da ação:')],
            [sg.Input(size=(20,20)), sg.Text('Exemplo: ITSA4')],
            [sg.Text('Quantidade:')],
            [sg.Input(size=(20,20)), sg.Text('Exemplo: 4')],
            [sg.Button('Cadastrar')]  ]

acompanhamento_geral = [[sg.Text('Acompanhamento Geral:', font='Any 13')],
            [texto_ganho_perda, valor_ganho_perda],
            [sg.Text('Total investido: {}'.format(total_investido))],
            [sg.Text('Total investido hoje: {}'.format(total_investido_atualmente))]]
            # [sg.Image(data=sg.DEFAULT_BASE64_ICON)]  

# Busca base nao sumarizada
data = acompanhamento_acoes.verifica_acoes_hoje(df, sum=False)
# header = [f'{col}' for col in range(len(data[0]))]
header = list(data.columns)
print('\n\n\n\n\n')
print(data)
tabela_compras = [[sg.Text('Acompanhamento Específico', font='Any 20')],
           [sg.Table(values=data.values.tolist(), 
                        headings=header, max_col_width=25,
                        auto_size_columns=True,
                        # display_row_numbers=True,
                        justification='left',
                        # Numero de linhas da base
                        num_rows=data.shape[1],
                        alternating_row_color=sg.theme_button_color()[1],
                        key='-TABLE-',
                        # selected_row_colors='red on yellow',
                        # enable_events=True,
                        # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True,  # Comment out to not enable header and other clicks
                        )
                        ]]

layout = [[sg.Column(barra_titulo, size=(960, 25), pad=(0,0), background_color=DARK_HEADER_COLOR)],
        #   [sg.Column(top, size=(920, 90), pad=BPAD_TOP)],
          [sg.Column([[sg.Column(acompanhamento_geral, size=(300,150), pad=BPAD_LEFT_INSIDE)],
                      [sg.Column(bloco_compra_acao, size=(300,200),  pad=BPAD_LEFT_INSIDE)]], pad=BPAD_LEFT, background_color=BORDER_COLOR),
           sg.Column(tabela_compras, size=(600, 370), pad=BPAD_RIGHT,scrollable=True)]]

window = sg.Window('Stock Wallet', layout, margins=(0,0), background_color=BORDER_COLOR, grab_anywhere=True)

while True:      
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()