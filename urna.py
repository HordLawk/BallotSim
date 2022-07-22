import csv
from candidato import Candidato
from cargo import Cargo
from partido import Partido
import numpy

# classe para representar uma urna eletronica
class UrnaEletronica:
    def __init__(self) -> None:
        self.partidos: list[Partido] = []
        self.cargos = [
            Cargo('DEPUTADO FEDERAL', 4),
            Cargo('DEPUTADO ESTADUAL', 5),
            Cargo('SENADOR', 3),
            Cargo('GOVERNADOR', 2),
            Cargo('PRESIDENTE', 2),
        ]
        self.cpfs: set[str] = set()

    def inicializar_candidatos(self) -> None:
        self.partidos = [Partido(linha[0], linha[1], linha[2]) for linha in csv.reader(open('partidos.csv'))]
        for linha in csv.reader(open('candidatos.csv')):
            if len(linha) < 3:
                continue
            partido = self.buscar_partido(linha[1])
            if not partido:
                continue
            cargo_codigo = int(linha[2])
            if cargo_codigo > len(self.cargos):
                continue
            cargo = self.cargos[cargo_codigo]
            candidato = Candidato(*linha[:2], partido, cargo)
            partido.inserir_candidato(candidato)
            cargo.inserir_candidato(candidato)
 
    # chama a funcao para adicionar um voto ao candidato de um cargo especifico com o numero selecionado
    def inserir_voto(self, numero: str, cargo_codigo: int) -> None:
        self.cargos[cargo_codigo].inserir_voto(numero)

    # verifica se o CPF informado ja foi utilizado para votacao; retorna True ou False   
    def novo_cpf(self, cpf: str) -> bool:
        if cpf in self.cpfs:
            return False
        self.cpfs.add(cpf)
        return True
    
    # busca um partido na lista de partidos pelo seu numero associado
    # retorna objeto da classe partido (se encontrar) ou None (se nao encontrar)
    def buscar_partido(self, numero: str) -> (Partido | None):
        for p in self.partidos:
            if p.numero == numero[:2]:
                return p
        return None
    
    # busca um candidato na lista de candidatos de um cargo especifico pelo seu numero associado
    # retorna objeto da classe candidato (se encontrar) ou None (se nao encontrar)
    def buscar_candidato(self, numero: str, cargo_codigo: int) -> (Candidato | None):
        return self.cargos[cargo_codigo].buscar_candidato(numero)

    # retorna string com relatorio de todos os votos inseridos na urna eletronica
    def relatorio_votos(self) -> None:
        votos_validos = sum([sum([len(candidato.votos) for candidato in cargo.candidatos]) for cargo in self.cargos])
        votos_invalidos = sum([cargo.votosInvalidos for cargo in self.cargos])
        return (
            f'TOTAL DE VOTOS: {votos_validos + votos_invalidos} voto(s)\n'
            f'Votos válidos: {votos_validos} voto(s)\n' +
            ''.join(
                list(
                    numpy.concatenate(
                        [
                            list(
                                numpy.concatenate(
                                    [
                                        [f'{voto} ({candidato.numero}) ({cargo})\n' for voto in candidato.votos]
                                        for candidato
                                        in cargo.candidatos
                                    ]
                                ).flat
                            )
                            for cargo
                            in self.cargos]
                    ).flat
                )
            ) +
            f'Votos inválidos: {votos_invalidos} voto(s)'
        )
    
    # retorna string com relatorio dos votos organizados por cargo
    def relatorio_cargos(self) -> str:
        return '\n'.join([cargo.relatorio() for cargo in self.cargos])
    
    # retorna string com relatorio dos votos organizados por partido
    def relatorio_partidos(self) -> str:
        return '\n'.join([partido.relatorio() for partido in self.partidos])