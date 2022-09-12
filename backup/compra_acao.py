import PySimpleGUI as sg

def home_page():
    # Criando página de compra de acoes 
    layout_tela_inclusao_acao = [
        [sg.Titlebar('Inclua sua compra: ')],
        [sg.Text('Ação: ', size =(15, 1)), sg.InputText()],
        [sg.Text('Quantidade:', size =(15, 1)), sg.InputText()],
        [sg.Button('Cadastrar ação')],
        [sg.Button('Fechar aplicativo')]
    ]
    tela_compra_acao = sg.Window("Compra", layout_tela_inclusao_acao, margins=(400, 200))

    while True:
        event, values = tela_compra_acao.read()

        if event == 'Cadastrar ação':
            # sg.MsgBoxOK('Ação cadastrada com sucesso')
            print(values)
            sg.MsgBox('Cadastrado com sucesso!')

        if event == 'Fechar aplicativo' or event == sg.WIN_CLOSED:
            break
        
    tela_compra_acao.close()