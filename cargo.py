from __future__ import annotations
from typing import TYPE_CHECKING

from candidato import Candidato
if TYPE_CHECKING:
    from partido import Partido

class Cargo:
    def __init__(self, nome: str, tamCod: int) -> None:
        self.nome = nome
        self.tamCod = tamCod
        self.votosInvalidos = 0
        self.candidatos: list[Candidato] = []

    def inserir_candidato(self, candidato: Candidato) -> None:
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
    
    def relatorio(self) -> str:
        return (
            f'{self}\n' +
            ''.join([f'{candidato} ({candidato.partido}) - {len(candidato.votos)} voto(s)\n' for candidato in self.candidatos])
        )
    
    def __str__(self) -> str:
        return self.nome