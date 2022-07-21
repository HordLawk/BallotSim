from __future__ import annotations
from typing import TYPE_CHECKING

from voto import Voto
if TYPE_CHECKING:
    from partido import Partido
    from cargo import Cargo

class Candidato:
    def __init__(self, nome: str, numero: str, partido: Partido, cargo: Cargo) -> None:
        self.nome = nome
        self.numero = numero
        self.votos: list[Voto] = []
        self.partido = partido
        self.cargo = cargo

    def inserir_voto(self) -> None:
        v = Voto()
        self.votos.append(v)

    def __str__(self) -> str:
        return self.nome