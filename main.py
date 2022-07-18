import PySimpleGUI as sg
from classes import *
from time import sleep

def definir_layout(i: int) -> sg.Window:
    cor = ('white', '#0A0A0A')
    tam1 = (7, 2)
    tam2 = (10, 2)
    layout_teclado = [[
        sg.Frame(
            '',
            [
                [
                    sg.Button('1', button_color=cor, size=tam1),
                    sg.Button('2', button_color=cor, size=tam1),
                    sg.Button('3', button_color=cor, size=tam1),
                ],
                [
                    sg.Button('4', button_color=cor, size=tam1),
                    sg.Button('5', button_color=cor, size=tam1),
                    sg.Button('6', button_color=cor, size=tam1),
                ],
                [
                    sg.Button('7', button_color=cor, size=tam1),
                    sg.Button('8', button_color=cor, size=tam1),
                    sg.Button('9', button_color=cor, size=tam1),
                ],
                [sg.Button('0', button_color=cor, size=tam1)], 
                [
                    sg.Button('BRANCO', button_color=('black', 'white'), size=tam2), 
                    sg.Button('CORRIGE',  button_color=('black', '#FF6109'), size=tam2), 
                    sg.Button('CONFIRMA',  button_color=('black', '#00C883'), size=tam2),
                ],
            ], 
            background_color=('#404040'),
            element_justification='c',
            pad=20,
            border_width=0,
        ),
    ]]

    layout_esq = []
    # CPF
    if i == -1:
        layout_esq = [[sg.Text('Insira seu CPF:')], 
            [sg.Frame('', [[sg.VPush()],
                [sg.Text('', size=(2), key=('CPF' + str(j)), pad=(0,0), justification='center')],
                [sg.VPush()]]) for j in range(11)],
            [sg.Text('CPF inválido', key=('erroCPF'), visible=False)]]
    # votacao
    elif i <= 4:
        layout_esq = [
            [sg.Text(UrnaEletronica.Cargos[i].nome)],
            [sg.Frame('', [[sg.VPush()],
                [sg.Text('', size=(4), key=(j), pad=(0,0), justification='center')],
                [sg.VPush()]]) for j in range(UrnaEletronica.Cargos[i].tamCod)],
            [sg.Text('Nome:', key=('nomeLabel'), visible=False), sg.Text('testando', key=('nome'), visible=False)],
            [
                sg.Text('Partido:', key=('partidoLabel'), visible=False),
                sg.Text('teste', key=('partido'), visible=False),
            ],
        ]
    # FIM
    else:
        layout_esq = [[sg.Text('FIM', font=('Arial', 60), justification='c')]]

    layout = [[sg.Col(layout_esq, size=(400, 300)), 
            sg.Col(layout_teclado, background_color=('#404040'))]]
    window = sg.Window('Urna Eletrônica', layout, finalize=True)

    return window

def mostrar_candidato(candidato: Candidato = None) -> None:
    if candidato == None:
        window['nomeLabel'].update(visible=False)
        window['partidoLabel'].update(visible=False)
        window['nome'].update('', visible=False)
        window['partido'].update('', visible=False)
    else:
        window['nomeLabel'].update(visible=True)
        window['partidoLabel'].update(visible=True)
        window['nome'].update(candidato.nome, visible=True)
        window['partido'].update(str(candidato.partido), visible=True)

def validar_cpf(cpf: str) -> bool:
    if (len(cpf) < 11) or (cpf == (cpf[0] * 11)):
        return False
    digitos = [int(e) for e in cpf]
    soma1 = 0
    for i,e in enumerate(digitos[:9]):
        soma1 += e * (10 - i)
    if (((soma1 * 10) % 11) % 10) != digitos[9]:
        return False
    soma2 = 0
    for i,e in enumerate(digitos[:10]):
        soma2 += e * (11 - i)
    return (((soma2 * 10) % 11) % 10) == digitos[10]

sg.theme('GrayGrayGray')
sg.set_options(font=("Arial", 12))

numero = ''
urna = UrnaEletronica()
urna.inicializar_candidatos()

candidato = None
i = -1
j = 0

window = definir_layout(i)
while True:
    event, values = window.read()  # read the window
    if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
        break
    # digitar numero no teclado numerico
    if event in '1234567890':
        # CPF
        if i == -1:
            if j < 11:
                numero += event
                window['CPF' + str(j)].update(event)
                j += 1
                if j == 11 and validar_cpf(numero) == False:
                    window['erroCPF'].update(visible=True)
        # VOTO
        elif i < 5:
            if j >= UrnaEletronica.Cargos[i].tamCod:
                continue
            
            numero += event
            window[j].update(event)
            j += 1
            if j == UrnaEletronica.Cargos[i].tamCod:
                candidato = urna.buscar_candidato(numero, UrnaEletronica.Cargos[i])
                mostrar_candidato(candidato)
    
    # apaga os numeros digitados
    elif event == 'CORRIGE': 
        numero = ''
        # CPF
        if i == -1:
            window['erroCPF'].update(visible=False)
            for k in range(j):
                window['CPF' + str(k)].update('')
        # VOTO
        elif i < 5:
            for k in range(j):
                window[k].update('')
            mostrar_candidato()
            candidato = None
        j = 0

    # nao insere voto na urna / insere voto invalido; passa para proximo cargo
    elif event == 'BRANCO':
        if i != -1:
            window.close()
            numero = ''
            candidato = None
            i += 1
            j = 0
            window = definir_layout(i)
            if i == 7:
                urna.relatorio_votos()
                i = -1

    # tenta inserir voto na urna; passa para proximo cargo
    elif event == 'CONFIRMA':
        # CPF
        if i == -1:
            if j == 11 and validar_cpf(numero) == True:
                i += 1
                j = 0
                window.close()
                numero = ''
                window = definir_layout(i)
        # VOTO
        elif (i < 5) and (j == UrnaEletronica.Cargos[i].tamCod):
            urna.inserir_voto(numero, UrnaEletronica.Cargos[i].nome)
            i += 1
            j = 0
            window.close()
            candidato = None
            numero = ''
            window = definir_layout(i)
            if i == 5:
                i = -1
                sleep(10)
                window.close()
                window = definir_layout(i)
