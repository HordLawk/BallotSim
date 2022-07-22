import PySimpleGUI as sg

# define o layout da janela de controle da votação e da urna eletronica
# retorna elemento do tipo PySimpleGUI.Window
def layout_controle() -> sg.Window:
    layout = [[
        sg.Frame(
            '',
            [
                [sg.Push(), sg.Text('Controle da votação', font=('Arial', 14)), sg.Push()],
                [
                    sg.FileBrowse(
                        'Carregar cargos',
                        key='fbCargo',
                        file_types=[("CSV Files", "*.csv")],
                        target='csvCargo',
                        size=20,
                    ), 
                    sg.Input('', key='csvCargo', disabled=True, enable_events=True)
                ],
                [
                    sg.FileBrowse(
                        'Carregar partidos',
                        key='fbPartido',
                        file_types=[("CSV Files", "*.csv")],
                        target='csvPartido',
                        size=20,
                    ), 
                    sg.Input('', key='csvPartido', disabled=True, enable_events=True)
                ],
                [
                    sg.FileBrowse(
                        'Carregar candidatos',
                        key='fbCandidato',
                        file_types=[("CSV Files", "*.csv")],
                        target='csvCandidato',
                        size=20,
                    ), 
                    sg.Input('', key='csvCandidato', disabled=True, enable_events=True)
                ],
                [sg.Button('Iniciar voto', key='inicio', size=20, disabled=True)],
                [sg.Button('Finalizar votação', key='fim', size=20, disabled=True)],
                [sg.HorizontalSeparator(pad=(0,15))],
                [sg.Push(), sg.Text('Apuração dos votos', font=('Arial', 14)), sg.Push()],
                [sg.Button('Gerar relatório', key='relat1', size=20, disabled=True)],
                [sg.Text('Selecionar partido')],
                [
                    sg.Combo(
                        values=[],
                        key='partidoInput',
                        size=40,
                        readonly=True,
                        default_value='Todos',
                    ),
                    sg.Button(
                        'Gerar relatório',
                        key='relat2',
                        size=20,
                        disabled=True,
                    ),
                ],
                [sg.Text('Selecionar cargo')],
                [
                    sg.Combo(
                        values=[],
                        key='cargoInput',
                        size=40,
                        readonly=True,
                    ),
                    sg.Button(
                        'Gerar relatório',
                        key='relat3',
                        size=20,
                        disabled=True,
                    ),
                ],
            ],
            pad=20,
            border_width=0,
        ),
    ]]
    window = sg.Window('Controle da Urna Eletrônica', layout, finalize=True)

    return window

# define o layout da janela de relatorio dos votos apurados
# retorna elemento do tipo PySimpleGUI.Window
def layout_relatorio() -> sg.Window:
    layout = [[sg.Multiline(disabled=True, key='relat', pad=20, size=(50, 25))]]
    window = sg.Window('Relatório dos votos apurados', layout, finalize=True)

    return window

# define o layout da janela da urna eletronica, pode ser o layout de:
# insercao de CPF, votacao, ou fim do processo de votacao (dependendo do parametro i)
# retorna elemento do tipo PySimpleGUI.Window
def layout_votacao(i: int, cargos = None) -> sg.Window:
    cor = ('white', '#0A0A0A')
    tam1 = (7, 2)
    tam2 = (10, 2)

    # layout do teclado numerico da urna
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
            background_color='#404040',
            element_justification='c',
            pad=20,
            border_width=0,
        ),
    ]]

    # layout da tela (parte a esquerda) da urna
    layout_tela = []
    # insercao do CPF
    if i == -1:
        layout_tela = [
            [sg.Text('Insira seu CPF:')], 
            [sg.Frame('', [
                [sg.VPush()],
                [sg.Text('', size=2, key=('CPF' + str(j)), pad=(0,0), justification='center')],
                [sg.VPush()]
            ]) for j in range(11)],
            [sg.Text('', key='erroCPF', visible=False)]
        ]

    # votacao
    elif i < len(cargos):
        layout_tela = [
            [sg.Text('Seu voto para')],
            [sg.Text(str(cargos[i]))],
            [sg.Frame('', [
                [sg.VPush()],
                [sg.Text('', size=4, key=j, pad=(0,0), justification='center')],
                [sg.VPush()]
            ]) for j in range(cargos[i].tamCod)],
            [sg.Frame('', [
                [sg.Text('Nome:'), sg.Text('', key='nome')],
                [sg.Text('Partido:'), sg.Text('', key='partido')],
                [sg.HorizontalSeparator(pad=(0, 15))],
                [sg.Text('Aperte a tecla:')],
                [sg.Text('VERDE para CONFIRMAR')],
                [sg.Text('LARANJA para CORRIGIR')],
            ], key='info', visible=False, border_width=0, pad=0)]
        ]

    # fim do processo de votacao
    else:
        layout_tela = [[sg.Text('FIM', font=('Arial', 30), justification='c')]]

    layout = [[sg.Col(layout_tela, size=(400, 300)), sg.Col(layout_teclado, background_color='#404040')]]
    window = sg.Window('Urna Eletrônica', layout, finalize=True)

    return window
