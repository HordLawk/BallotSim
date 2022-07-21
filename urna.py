import csv
from candidato import Candidato
from cargo import Cargo
from partido import Partido

class UrnaEletronica:
    def __init__(self) -> None:
        self.partidos: list[Partido] = []
        self.cargos = [
            Cargo('DEPUTADO FEDERAL', 4),
            Cargo('DEPUTADO ESTADUAL', 5),
            Cargo('SENADOR', 3),
            Cargo('GOVERNADDOR', 2),
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
            partido.inserir_candidato(linha[0], linha[1])
            cargo.inserir_candidato(linha[0], linha[1], partido)

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

    # def relatorio_votos(self) -> None:
    #     print(f'TOTAL DE VOTOS: {len(self.votos) + self.votosInvalidos} voto(s)')
    #     print(f'Votos válidos: {len(self.votos)} voto(s)')
    #     for v in self.votos:
    #         print(v)
    #     print(f'Votos inválidos: {self.votosInvalidos} voto(s)')

    # def relatorio_cargo(self, cargo: (Cargo | None) = None) -> None:
    #     for c in UrnaEletronica.Cargos:
    #         if cargo == None or cargo == c:
    #             print(c)
    #             for cand in self.candidatos:
    #                 if cand.cargo == c:
    #                     print(f'{cand} ({cand.partido}) - {cand.votos} voto(s)')
    #             print('')

    # def relatorio_partido(self, partido: (Partido | None) = None, sigla: (str | None) = None) -> None:
    #     for p in self.partidos: 
    #         if (partido == None and sigla == None) or (partido == p) or (sigla == p.sigla):
    #             print(p)
    #             for cand in self.candidatos:
    #                 if cand.partido == p:
    #                     print(f'{cand} ({cand.cargo}) - {cand.votos} voto(s)')
    #             print('')