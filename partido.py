from __future__ import annotations
from typing import TYPE_CHECKING

from candidato import Candidato
if TYPE_CHECKING:
    from cargo import Cargo

# classe para representar um partido politico que disputa a eleicao
class Partido:
    # construtor da classe, define nome, numero e sigla do partido,
    # inicializa a lista de candidatos do partido
    def __init__(self, nome: str, numero: str, sigla: str) -> None:
        self.nome = nome
        self.numero = numero
        self.sigla = sigla
        self.candidatos: list[Candidato] = []

    # adiciona um candidato a lista de candidatos do partido
    def inserir_candidato(self, candidato: Candidato) -> None:
        self.candidatos.append(candidato)
    
    # retorna string com relatorio dos votos relativos aos candidatos do partido
    def relatorio(self) -> str:
        return (
            f'{self}\n' +
            ''.join([f'{candidato} ({candidato.cargo}) - {len(candidato.votos)} voto(s)\n' for candidato in self.candidatos])
        )
    
    # retorna representacao do partido em string
    def __str__(self) -> str:
        return f'{self.nome} ({self.sigla})'
