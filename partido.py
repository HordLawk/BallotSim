from __future__ import annotations
from typing import TYPE_CHECKING

from candidato import Candidato
if TYPE_CHECKING:
    from cargo import Cargo

class Partido:
    def __init__(self, nome: str, numero: str, sigla: str) -> None:
        self.nome = nome
        self.numero = numero
        self.sigla = sigla
        self.candidatos: list[Candidato] = []

    def inserir_candidato(self, candidato: Candidato) -> None:
        self.candidatos.append(candidato)
    
    def relatorio(self) -> str:
        return (
            f'{self}\n' +
            ''.join([f'{candidato} ({candidato.cargo}) - {len(candidato.votos)} voto(s)\n' for candidato in self.candidatos])
        )
    
    def __str__(self) -> str:
        return f'{self.nome} ({self.sigla})'