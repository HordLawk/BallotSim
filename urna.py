import csv
from candidato import Candidato
from cargo import Cargo
from partido import Partido
import numpy

class UrnaEletronica:
    def __init__(self, partidos_csv: str, cargos_csv: str, candidatos_csv: str) -> None:
        self.partidos: list[Partido] = []
        self.cargos: list[Cargo] = []
        self.cpfs: set[str] = set()
        for linha in csv.reader(open(partidos_csv)):
            if len(linha) > 2:
                self.partidos.append(Partido(*linha[:3]))
        for linha in csv.reader(open(cargos_csv)):
            if len(linha) < 2:
                continue
            try:
                self.cargos.append(Cargo(linha[0], int(linha[1])))
            except ValueError:
                continue
        for linha in csv.reader(open(candidatos_csv)):
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

    def inserir_voto(self, numero: str, cargo_codigo: int) -> None:
        self.cargos[cargo_codigo].inserir_voto(numero)
    
    def novo_cpf(self, cpf: str) -> bool:
        if cpf in self.cpfs:
            return False
        self.cpfs.add(cpf)
        return True
    
    def buscar_partido(self, numero: str) -> (Partido | None):
        for p in self.partidos:
            if p.numero == numero[:2]:
                return p
        return None
    
    def buscar_candidato(self, numero: str, cargo_codigo: int) -> (Candidato | None):
        return self.cargos[cargo_codigo].buscar_candidato(numero)

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
    
    def relatorio_cargos(self) -> str:
        return '\n'.join([cargo.relatorio() for cargo in self.cargos])
    
    def relatorio_partidos(self) -> str:
        return '\n'.join([partido.relatorio() for partido in self.partidos])