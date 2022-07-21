from voto import Voto

class Candidato:
    def __init__(self, nome: str, numero: str, partido) -> None:
        self.nome = nome
        self.numero = numero
        self.votos: list[Voto] = []
        self.partido = partido

    def inserir_voto(self) -> None:
        v = Voto()
        self.votos.append(v)

    def __str__(self) -> str:
        return self.nome