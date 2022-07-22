import datetime as dt

# classe para representar um voto inserido na urna
class Voto:
    # construtor da classe, define data e hora do voto
    def __init__(self) -> None:
        self.data = dt.datetime.now()

    # retorna representacao do voto em string
    def __str__(self) -> str:
        return f'{self.data}'
