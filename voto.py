import datetime as dt

class Voto:
    def __init__(self) -> None:
        self.data = dt.datetime.now()

    def __str__(self) -> str:
        return f'{self.data}'