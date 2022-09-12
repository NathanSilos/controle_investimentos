import PySimpleGUI as sg

layout_tela_inicial = [
    [sg.Titlebar('Bem vindo ao Stock Wallet! ')],
    [sg.Text('Clique na opção desejada')],
    [sg.Button('Compra de ação')],
    [sg.Button('Acompanhamento de carteira')],
    [sg.Button('Fechar aplicativo')]
]

home = sg.Window("Home", layout_tela_inicial, margins=(400, 200))

while True:
    event, values = home.read()

    if event == 'Fechar aplicativo' or event == sg.WIN_CLOSED:
        break
    
home.close()