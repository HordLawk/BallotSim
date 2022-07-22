from __future__ import annotations
from typing import TYPE_CHECKING

from voto import Voto
if TYPE_CHECKING:
    from partido import Partido
    from cargo import Cargo

# classe para representar um candidato em disputa na eleicao
class Candidato:
    # construtor da classe, define o nome, numero, partido e cargo disputado do candidato
    def __init__(self, nome: str, numero: str, partido: Partido, cargo: Cargo) -> None:
        self.nome = nome
        self.numero = numero
        self.votos: list[Voto] = []
        self.partido = partido
        self.cargo = cargo

    # adiciona um voto a lista de votos do candidato
    def inserir_voto(self) -> None:
        v = Voto()
        self.votos.append(v)

    # retorna representacao do candidato em string
    def __str__(self) -> str:
        return self.nome
