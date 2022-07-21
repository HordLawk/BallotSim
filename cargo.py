from candidato import Candidato
from partido import Partido

class Cargo:
    def __init__(self, nome: str, tamCod: int) -> None:
        self.nome = nome
        self.tamCod = tamCod
        self.votosInvalidos = 0
        self.candidatos: list[Candidato] = []

    def inserir_candidato(self, nome: str, numero: str, partido: Partido) -> None:
        candidato = Candidato(nome, numero, partido)
        self.candidatos.append(candidato)

    def inserir_voto(self, numero: int) -> None:
        candidato = self.buscar_candidato(numero)
        if candidato:
            return candidato.inserir_voto()
        self.votosInvalidos += 1

    def buscar_candidato(self, numero: str) -> (Candidato | None):
        for c in self.candidatos:
            if c.numero == numero:
                return c
        return None
    
    def __str__(self) -> str:
        return self.nome