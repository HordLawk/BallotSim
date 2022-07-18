import datetime as dt
import csv

class Cargo:
    def __init__(self, nome: str, tamCod: int) -> None:
        self.nome = nome
        self.tamCod = tamCod
    
    def __str__(self) -> str:
        return self.nome

class Partido:
    def __init__(self, nome: str, numero: str, sigla: str) -> None:
        self.nome = nome
        self.numero = numero
        self.sigla = sigla
    
    def __str__(self) -> str:
        return f'{self.nome} ({self.sigla})'

class Candidato:
    def __init__(self, nome: str, partido: Partido, numero: str, cargo: Cargo) -> None:
        self.nome = nome
        self.partido = partido
        self.numero = numero
        self.cargo = cargo
        self.votos = 0

    def __str__(self) -> str:
        return self.nome

class UrnaEletronica:
    Cargos = [
        Cargo('DEPUTADO FEDERAL', 4),
        Cargo('DEPUTADO ESTADUAL', 5),
        Cargo('SENADOR', 3),
        Cargo('GOVERNADDOR', 2),
        Cargo('PRESIDENTE', 2),
    ]

    def __init__(self) -> None:
        self.votos: list[Voto] = []
        self.candidatos: list[Candidato] = []
        self.partidos: list[Partido] = []
        self.votosInvalidos = 0

    def inicializar_candidatos(self) -> None:
        self.partidos = [Partido(linha[0], linha[1], linha[2]) for linha in csv.reader(open('partidos.csv'))]
        self.candidatos = [
            Candidato(linha[0], self.buscar_partido(linha[1]), linha[1], UrnaEletronica.Cargos[int(linha[2])])
            for linha
            in csv.reader(open('candidatos.csv'))
        ]

    def inserir_voto(self, numero: str, cargo: Cargo) -> None:
        candidato = self.buscar_candidato(numero, cargo)
        if candidato != None:
            v = Voto(numero)
            candidato.votos += 1
            self.votos.append(v)
        else:
            self.votosInvalidos += 1

    # meio anti etico
    def relatorio_votos(self) -> None:
        print(f'TOTAL DE VOTOS: {len(self.votos) + self.votosInvalidos} voto(s)')
        print(f'Votos válidos: {len(self.votos)} voto(s)')
        for v in self.votos:
            print(v)
        print(f'Votos inválidos: {self.votosInvalidos} voto(s)')

    def relatorio_cargo(self, cargo: (Cargo | None) = None) -> None:
        for c in UrnaEletronica.Cargos:
            if cargo == None or cargo == c:
                print(c)
                for cand in self.candidatos:
                    if cand.cargo == c:
                        print(f'{cand} ({cand.partido}) - {cand.votos} voto(s)')
                print('')

    def relatorio_partido(self, partido: (Partido | None) = None, sigla: (str | None) = None) -> None:
        for p in self.partidos: 
            if (partido == None and sigla == None) or (partido == p) or (sigla == p.sigla):
                print(p)
                for cand in self.candidatos:
                    if cand.partido == p:
                        print(f'{cand} ({cand.cargo}) - {cand.votos} voto(s)')
                print('')

    def buscar_candidato(self, numero: str, cargo: Cargo) -> (Candidato | None):
        for c in self.candidatos:
            if (c.cargo == cargo) and (c.numero == numero):
                return c
        return None
    
    def buscar_partido(self, numero: str) -> (Partido | None):
        for p in self.partidos:
            if p.numero == numero[:2]:
                return p
        return None

class Voto:
    def __init__(self, numero: str) -> None:
        self.data = dt.datetime.now()
        self.numero = numero

    def __str__(self) -> str:
        return f'{self.data} {self.numero}'
    