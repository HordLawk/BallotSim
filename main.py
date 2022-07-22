import PySimpleGUI as sg

from structures.urna import UrnaEletronica
from utils.layout import *

# exibe as informacoes do candidato selecionado na tela e 
# as instrucoes para a confirmacao ou correcao do voto
def exibir_info(numero: str, i: int) -> None:
    candidato = urna.buscar_candidato(numero, i)
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
# `i` representa o indice da janela da simulacao da urna que o usuario se encontra no momento
# `j` representa a quantidade de digitos entrados no input da simulacao da urna ate o momento
i, j = 0, 0
inicio = False
partidos_csv, cargos_csv, candidatos_csv = '', '', ''

# janelas da aplicacao
# window_controle: controle; window_votacao: votacao; window_relatorio: relatorio dos votos
window_controle, window_votacao, window_relatorio = layout_controle(), None, None

# loop principal da aplicacao
while True:
    window, event, values = sg.read_all_windows()

    match event:
        # fechar janela
        case sg.WIN_CLOSED:
            window.close()
            # janela de controle
            if window == window_controle:
                break
            
            # janela de votacao
            elif window == window_votacao:
                window_controle['inicio'].update(disabled=False)
                window_controle['fim'].update(disabled=False)
                window_votacao = None
            
            # janela de relatorio dos votos
            elif window == window_relatorio:
                window_relatorio = None
        
        # janela de controle da votacao/urna eletronica
        # iniciar o processo de votacao
        case 'inicio':
            if not inicio:
                try:
                    urna = UrnaEletronica(partidos_csv, cargos_csv, candidatos_csv)
                    inicio = True
                except Exception:
                    layout_erro()
                    continue

            window_controle['inicio'].update(disabled=True)
            window_controle['fim'].update(disabled=True)
            i = -1
            j = 0
            window_votacao = layout_votacao(i)
        
        # finalizar o processo de votacao
        case 'fim':
            window_controle['fbPartido'].update(disabled=True)
            window_controle['fbCandidato'].update(disabled=True)
            window_controle['fbCargo'].update(disabled=True)
            window_controle['inicio'].update(disabled=True)
            window_controle['fim'].update(disabled=True)
            window_controle['relat1'].update(disabled=False)
            window_controle['relat2'].update(disabled=False)
            window_controle['relat3'].update(disabled=False)
            window_controle['cargoInput'].update(values=['Todos', *urna.cargos], value='Todos')
            window_controle['partidoInput'].update(values=['Todos', *urna.partidos], value='Todos')
        
        # exibir o relatorio de todos os votos da urna
        case 'relat1':
            window_relatorio = layout_relatorio()
            window_relatorio['relat'].update(urna.relatorio_votos())

        # exibir o relatorio dos votos por partido
        case 'relat2':
            window_relatorio = layout_relatorio()
            window_relatorio['relat'].update(
                values['partidoInput'] == 'Todos'
                and urna.relatorio_partidos()
                or values['partidoInput'].relatorio()
            )

        # exibir o relatorio dos votos por cargo
        case 'relat3':
            window_relatorio = layout_relatorio()
            window_relatorio['relat'].update(
                values['cargoInput'] == 'Todos'
                and urna.relatorio_cargos()
                or values['cargoInput'].relatorio()
            )

        # arquivo com lista de partidos carregado
        case 'csvPartido':
            partidos_csv = values['csvPartido']
            if partidos_csv and candidatos_csv and cargos_csv:
                window_controle['inicio'].update(disabled=False)
                
        # arquivo com lista de candidatos carregado
        case 'csvCargo':
            cargos_csv = values['csvCargo']
            if partidos_csv and candidatos_csv and cargos_csv:
                window_controle['inicio'].update(disabled=False)
                
        # arquivo com lista de candidatos carregado
        case 'csvCandidato':
            candidatos_csv = values['csvCandidato']
            if partidos_csv and candidatos_csv and cargos_csv:
                window_controle['inicio'].update(disabled=False)

        # janela de votacao
        # tecla CORRIGE apertada no teclado
        case 'CORRIGE':
            playsound('./resources/tecla.wav', block=False)
            numero = ''
            # insercao do CPF
            if i == -1:
                window_votacao['erroCPF'].update(visible=False)
                for k in range(j):
                    window_votacao['CPF' + str(k)].update('')

            # votacao
            elif i < len(urna.cargos):
                for k in range(j):
                    window_votacao[k].update('')

                exibir_info(None, i)

            j = 0

        # tecla BRANCO apertada no teclado
        case 'BRANCO':
            playsound('./resources/tecla.wav', block=False)
            # votacao
            if i >= 0 and i < len(urna.cargos):
                urna.inserir_voto(None, i)
                window_votacao.close()
                numero = ''
                i += 1
                j = 0
                window_votacao = layout_votacao(i, urna.cargos)

        # tecla CONFIRMA apertada no teclado
        case 'CONFIRMA':
            playsound('./resources/tecla.wav', block=False)
            # insercao do CPF
            if i == -1:
                if (j != 11) or not validar_cpf(numero):
                    continue

                if not urna.novo_cpf(numero):
                    window_votacao['erroCPF'].update('CPF ja utilizado', visible=True)
                    continue

                i += 1
                j = 0
                window_votacao.close()
                numero = ''
                window_votacao = layout_votacao(i, urna.cargos)

            # votacao
            elif (i < len(urna.cargos)) and (j == urna.cargos[i].tamCod):
                urna.inserir_voto(numero, i)
                i += 1
                j = 0
                window_votacao.close()
                numero = ''
                window_votacao = layout_votacao(i, urna.cargos)
        
        # digito apertado no teclado
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0':
            playsound('./resources/tecla.wav', block=False)
            # insercao do CPF
            if i == -1:
                if j >= 11:
                    continue

                numero += event
                window_votacao['CPF' + str(j)].update(event)
                j += 1
                if j == 11:
                    if not validar_cpf(numero):
                        window_votacao['erroCPF'].update('CPF inválido', visible=True)

            # votacao
            elif i < len(urna.cargos):
                if j >= urna.cargos[i].tamCod:
                    continue
                
                numero += event
                window_votacao[j].update(event)
                j += 1
                if j == urna.cargos[i].tamCod:
                    exibir_info(numero, i)
