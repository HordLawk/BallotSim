import csv

from structures.candidato import Candidato
from structures.cargo import Cargo
from structures.partido import Partido

# classe para representar uma urna eletronica
class UrnaEletronica:
    # construtor da classe, inicializa lista de cargos, partidos, candidatos e CPFs que ja votaram
    # lista de cargos deve ser um arquivo csv com a formatacao por linha: nome,tamanhoCodigo
    # lista de partidos deve ser um arquivo csv com a formatacao por linha: nome,numero,sigla
    # lista de candidatos deve ser um arquivo csv com a formatacao por linha: nome,numero,indiceCargo
    def __init__(self, partidos_csv: str, cargos_csv: str, candidatos_csv: str) -> None:
        self.cargos: list[Cargo] = []
        self.cpfs: set[str] = set()
        self.partidos = [Partido(*linha[:3]) for linha in csv.reader(open(partidos_csv)) if len(linha) > 2]
        for linha in csv.reader(open(cargos_csv)):
            if len(linha) < 2:
                continue

            try:
                self.cargos.append(Cargo(linha[0], int(linha[1])))

            except ValueError:
                pass

        for linha in csv.reader(open(candidatos_csv)):
            if len(linha) < 3:
                continue

            partido = self.buscar_partido(linha[1])
            if not partido:
                continue

            try:
                cargo_codigo = int(linha[2])
                if cargo_codigo > len(self.cargos):
                    continue

                cargo = self.cargos[cargo_codigo]
                candidato = Candidato(*linha[:2], partido, cargo)
                partido.inserir_candidato(candidato)
                cargo.inserir_candidato(candidato)

            except ValueError:
                pass

    # chama a funcao para adicionar um voto ao candidato de um cargo especifico com o numero selecionado
    def inserir_voto(self, numero: (str | None), cargo_codigo: int) -> None:
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
            f'TOTAL DE VOTOS: {votos_validos + votos_invalidos} voto(s)\n\n'
            f'Votos válidos: {votos_validos} voto(s)\n' +
            ''.join(
                [
                    ''.join(
                        [
                            ''.join([f'- {voto} - {candidato.numero} ({cargo})\n' for voto in candidato.votos])
                            for candidato
                            in cargo.candidatos
                            if len(candidato.votos)
                        ]
                    )
                    for cargo
                    in self.cargos
                    if len(cargo.candidatos)
                ]
            ) + '\n'
            f'Votos inválidos: {votos_invalidos} voto(s)'
        )
    
    # retorna string com relatorio dos votos organizados por cargo
    def relatorio_cargos(self) -> str:
        return '\n'.join([cargo.relatorio() for cargo in self.cargos])
    
    # retorna string com relatorio dos votos organizados por partido
    def relatorio_partidos(self) -> str:
        return '\n'.join([partido.relatorio() for partido in self.partidos])
