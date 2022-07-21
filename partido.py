from candidato import Candidato

class Partido:
    def __init__(self, nome: str, numero: str, sigla: str) -> None:
        self.nome = nome
        self.numero = numero
        self.sigla = sigla
        self.candidatos: list[Candidato] = []

    def inserir_candidato(self, nome: str, numero: str) -> None:
        candidato = Candidato(nome, numero, self)
        self.candidatos.append(candidato)
    
    def __str__(self) -> str:
        return f'{self.nome} ({self.sigla})'