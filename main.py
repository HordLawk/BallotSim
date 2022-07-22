import PySimpleGUI as sg
from urna import UrnaEletronica
from layout import *
from time import sleep

# exibe as informacoes do candidato selecionado na tela e 
# as instrucoes para a confirmacao ou correcao do voto
def exibir_info(candidato: Candidato) -> None:
    if candidato == None:
        window['info'].update(visible=False)
    else:
        window['info'].update(visible=True)
        window['nome'].update(str(candidato.nome))
        window['partido'].update(str(candidato.partido))

# verifica se CPF informado e valido; retorna True ou False
def validar_cpf(cpf: str) -> bool:
    if (len(cpf) < 11) or (cpf == (cpf[0] * 11)):
        return False
    digitos = [int(e) for e in cpf]
    return (
        ((((sum([(e * (10 - i)) for i,e in enumerate(digitos[:9])]) * 10) % 11) % 10) == digitos[9])
        and
        ((((sum([(e * (11 - i)) for i,e in enumerate(digitos[:10])]) * 10) % 11) % 10) == digitos[10])
    )

# configuracoes do design das janelas
sg.theme('GrayGrayGray')
sg.set_options(font=("Arial", 12))

# configuracoes iniciais da urna eletronica
numero = ''
urna = None
i, j = 0, 0
inicio = False
partidos_csv, cargos_csv, candidatos_csv = '', '', ''

# janelas da aplicacao
# window1: controle; window2: votacao; window3: relatorio dos votos
window1, window2, window3 = layout_controle(), None, None

# loop principal da aplicacao
while True:
    window, event, values = sg.read_all_windows()

    match event:
        # fechar janela
        case sg.WIN_CLOSED:
            window.close()
            # janela de controle
            if window == window1:
                break
            
            # janela de votacao
            elif window == window2:
                window1['inicio'].update(disabled=False)
                window1['fim'].update(disabled=False)
                window2 = None
            
            # janela de relatorio dos votos
            elif window == window3:
                window3 = None
        
        # janela de controle da votacao/urna eletronica
        # iniciar o processo de votacao
        case 'inicio':
            if not inicio:
                inicio = True
                urna = UrnaEletronica(partidos_csv, cargos_csv, candidatos_csv)

            window1['inicio'].update(disabled=True)
            window1['fim'].update(disabled=True)
            i = -1
            j = 0
            window2 = layout_votacao(i)
        
        # finalizar o processo de votacao
        case 'fim':
            window1['fbPartido'].update(disabled=True)
            window1['fbCandidato'].update(disabled=True)
            window1['fbCargo'].update(disabled=True)
            window1['inicio'].update(disabled=True)
            window1['fim'].update(disabled=True)
            window1['relat1'].update(disabled=False)
            window1['relat2'].update(disabled=False)
            window1['relat3'].update(disabled=False)
            window1['cargoInput'].update(values=['Todos', *urna.cargos], value='Todos')
            window1['partidoInput'].update(values=['Todos', *urna.partidos], value='Todos')
        
        # exibir o relatorio de todos os votos da urna
        case 'relat1':
            window3 = layout_relatorio()
            window3['relat'].update(urna.relatorio_votos())

        # exibir o relatorio dos votos por partido
        case 'relat2':
            window3 = layout_relatorio()
            window3['relat'].update(
                values['partidoInput'] == 'Todos'
                and urna.relatorio_partidos()
                or values['partidoInput'].relatorio()
            )

        # exibir o relatorio dos votos por cargo
        case 'relat3':
            window3 = layout_relatorio()
            window3['relat'].update(
                values['cargoInput'] == 'Todos'
                and urna.relatorio_cargos()
                or values['cargoInput'].relatorio()
            )

        # arquivo com lista de partidos carregado
        case 'csvPartido':
            partidos_csv = values['csvPartido']
            if partidos_csv and candidatos_csv and cargos_csv:
                window1['inicio'].update(disabled=False)
                
        # arquivo com lista de candidatos carregado
        case 'csvCargo':
            cargos_csv = values['csvCargo']
            if partidos_csv and candidatos_csv and cargos_csv:
                window1['inicio'].update(disabled=False)
                
        # arquivo com lista de candidatos carregado
        case 'csvCandidato':
            candidatos_csv = values['csvCandidato']
            if partidos_csv and candidatos_csv and cargos_csv:
                window1['inicio'].update(disabled=False)

        # janela de votacao
        # tecla CORRIGE apertada no teclado
        case 'CORRIGE': 
            numero = ''
            # insercao do CPF
            if i == -1:
                window2['erroCPF'].update(visible=False)
                for k in range(j):
                    window2['CPF' + str(k)].update('')

            # votacao
            elif i < len(urna.cargos):
                for k in range(j):
                    window2[k].update('')

                exibir_info(None)

            j = 0

        # tecla BRANCO apertada no teclado
        case 'BRANCO':
            # votacao
            if i >= 0 and i < len(urna.cargos):
                window2.close()
                numero = ''
                i += 1
                j = 0
                window2 = layout_votacao(i, urna.cargos)

        # tecla CONFIRMA apertada no teclado
        case 'CONFIRMA':
            # insercao do CPF
            if i == -1:
                if (j != 11) or not validar_cpf(numero):
                    continue

                if not urna.novo_cpf(numero):
                    window2['erroCPF'].update('CPF ja utilizado', visible=True)
                    continue

                i += 1
                j = 0
                window2.close()
                numero = ''
                window2 = layout_votacao(i, urna.cargos)

            # votacao
            elif (i < len(urna.cargos)) and (j == urna.cargos[i].tamCod):
                urna.inserir_voto(numero, i)
                i += 1
                j = 0
                window2.close()
                numero = ''
                window2 = layout_votacao(i, urna.cargos)
        
        # digito apertado no teclado
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0':
            # insercao do CPF
            if i == -1:
                if j >= 11:
                    continue

                numero += event
                window2['CPF' + str(j)].update(event)
                j += 1
                if j == 11:
                    if not validar_cpf(numero):
                        window2['erroCPF'].update('CPF inválido', visible=True)

            # votacao
            elif i < len(urna.cargos):
                if j >= urna.cargos[i].tamCod:
                    continue
                
                numero += event
                window2[j].update(event)
                j += 1
                if j == urna.cargos[i].tamCod:
                    candidato = urna.buscar_candidato(numero, i)
                    exibir_info(candidato)