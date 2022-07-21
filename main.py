import PySimpleGUI as sg
from urna import UrnaEletronica
from time import sleep

# nao sei se precisa de um botao pra abrir o csv ou se o filebrowse ja funciona como o botao tbm
# da pra botar filetype csv eu acho mas fica pra amanha por mim .
def layout_adm() -> sg.Window:
    tam1 = (10, 2)
    layout = [[
        sg.Frame(
            '',
            [
                [sg.Push(), sg.Text('Controle da votação', font=('Arial', 14)), sg.Push()],
                #[sg.FileBrowse(), sg.Button('Carregar lista de candidatos')],
                [sg.Text('Carregar lista de partidos'), sg.FileBrowse('Selecionar arquivo', size=(20))],
                [sg.Text('Carregar lista de candidatos'), sg.FileBrowse('Selecionar arquivo', size=(20))],
                [sg.Button('Iniciar votação', key=('inicio'), size=20)],
                [sg.Button('Finalizar votação', key=('fim'), size=20, disabled=True)],
                [sg.HorizontalSeparator(pad=(0,15))],
                [sg.Push(), sg.Text('Apuração dos votos', font=('Arial', 14)), sg.Push()],
                [sg.Button('Gerar relatório', key=('relat1'), size=20, disabled=True)],
                [sg.Text('Número do partido')],
                [sg.Input(key=('partidoInput'), size=(40)), sg.Button('Gerar relatório', key=('relat2'), size=20, disabled=True)],
                [sg.Text('Nome do cargo')],
                [sg.Input(key=('cargoInput'), size=(40)), sg.Button('Gerar relatório', key=('relat3'), size=20, disabled=True)]
            ],
            #size=(500, 350),
            pad=20,
            border_width=0,
        )
    ]]
    window = sg.Window('Controle da Urna Eletrônica', layout, finalize=True)

    return window

def janela_relatorio() -> sg.Window:
    layout = [[sg.Multiline(disabled=True, key=('relat'), pad=20, size=(50, 25))]]
    window = sg.Window('Relatório dos votos apurados', layout, finalize=True)

    return window


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
        layout_esq = [
            [sg.Text('Insira seu CPF:')], 
            [sg.Frame('', [[sg.VPush()],
                [sg.Text('', size=(2), key=('CPF' + str(j)), pad=(0,0), justification='center')],
                [sg.VPush()]]) for j in range(11)],
            [sg.Text('CPF inválido', key=('erroCPF'), visible=False)],
            [sg.Text('CPF já utilizado', key=('CPF_repetido'), visible=False)]
        ]
    # votacao
    elif i <= 4:
        layout_esq = [
            [sg.Text(urna.cargos[i].nome)],
            [sg.Frame('', [[sg.VPush()],
                [sg.Text('', size=(4), key=(j), pad=(0,0), justification='center')],
                [sg.VPush()]]) for j in range(urna.cargos[i].tamCod)],
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

def mostrar_candidato(numero: str, cargo_codigo: int) -> None:
    candidato = urna.buscar_candidato(numero, cargo_codigo)
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
    return (
        ((((sum([(e * (10 - i)) for i,e in enumerate(digitos[:9])]) * 10) % 11) % 10) == digitos[9])
        and
        ((((sum([(e * (11 - i)) for i,e in enumerate(digitos[:10])]) * 10) % 11) % 10) == digitos[10])
    )

sg.theme('GrayGrayGray')
sg.set_options(font=("Arial", 12))

numero = ''
urna = UrnaEletronica()
urna.inicializar_candidatos()

candidato = None
i = -1
j = 0

window1, window2, window3 = layout_adm(), None, None
#window = definir_layout(i)
#window = layout_adm()
#window = janela_relatorio()
while True:
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED:
        window.close()
        if window == window1:
            break
        elif window == window2:
            window2 = None
        elif window == window3:
            windoe3 = None
    
    # janela de adm
    # falta os eventos dos aruqivos n sei se precisa de um btoao a mais fica pra amanha tbm por mim . kk k
    # possivelmente so ativar inicio depois que escolher arquivo? e dps desativar
    if event == 'inicio':
        i = -1
        j = 0
        window['fim'].update(disabled=False) # fazer algo pra nao poder apertar no meio do voto?
        window2 = definir_layout(i)
    if event == 'fim':
        i = -5
        # nao sei se vc quer fazer assim mas sla to enlouqeucendo
        window['inicio'].update(disabled=True)
        window['fim'].update(disabled=True)
        window['relat1'].update(disabled=False)
        window['relat2'].update(disabled=False)
        window['relat3'].update(disabled=False)
    if event == 'relat1':
        window3 = janela_relatorio()
        window3['relat'].update(urna.relatorio_votos())
    if event == 'relat2':
        window3 = janela_relatorio()
        window3['relat'].update('teste partido')
    if event == 'relat3':
        window3 = janela_relatorio()
        window3['relat'].update('teste cargo')


    # janela de votacao
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
            if j >= urna.cargos[i].tamCod:
                continue
            
            numero += event
            window[j].update(event)
            j += 1
            if j == urna.cargos[i].tamCod:
                mostrar_candidato(numero, i)
    
    # apaga os numeros digitados
    elif event == 'CORRIGE': 
        numero = ''
        # CPF
        if i == -1:
            window['erroCPF'].update(visible=False)
            window['CPF_repetido'].update(visible=False)
            for k in range(j):
                window['CPF' + str(k)].update('')
        # VOTO
        elif i < 5:
            for k in range(j):
                window[k].update('')
            mostrar_candidato(None, i)
            candidato = None
        j = 0
    if event == 'BRANCO':
        if i > -1 and i < 5:
            window.close()
            numero = ''
            candidato = None
            i += 1
            j = 0
            window = definir_layout(i)
            if i == 5:
                i = -1
                sleep(5)
                window.close()
                window = definir_layout(i)
            elif i == 7:
                urna.relatorio_votos()
                i = -1
    if event == 'CONFIRMA':
        # CPF
        if i == -1:
            if (j != 11) or not validar_cpf(numero):
                continue
            if not urna.novo_cpf(numero):
                window['CPF_repetido'].update(visible=True)
                continue
            i += 1
            j = 0
            window.close()
            numero = ''
            window = definir_layout(i)
        # VOTO
        elif (i < 5) and (j == urna.cargos[i].tamCod):
            urna.inserir_voto(numero, i)
            i += 1
            j = 0
            window.close()
            candidato = None
            numero = ''
            window = definir_layout(i)
            if i == 5:
                i = -1
                sleep(5)
                window.close()
                window = definir_layout(i)