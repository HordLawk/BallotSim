from candidato import Candidato

# classe para representar um cargo em disputa na eleicao
class Cargo:
    # construtor da classe, define nome e tamanho do codigo associado ao cargo
    # inicializa contador de votos invalidos e lista de candidatos disputando o cargo
    def __init__(self, nome: str, tamCod: int) -> None:
        self.nome = nome
        self.tamCod = tamCod
        self.votosInvalidos = 0
        self.candidatos: list[Candidato] = []

    # adiciona um candidato a lista de candidatos que disputam o cargo
    def inserir_candidato(self, candidato: Candidato) -> None:
        self.candidatos.append(candidato)

    # adiciona um voto ao candidato com o numero selecionado (se existir),
    # ou incrementa o contador de votos invalidos
    def inserir_voto(self, numero: int) -> None:
        candidato = self.buscar_candidato(numero)
        if candidato:
            return candidato.inserir_voto()

        self.votosInvalidos += 1

    # busca um candidato na lista de candidatos pelo seu numero associado
    # retorna objeto da classe candidato (se encontrar) ou None (se nao encontrar)
    def buscar_candidato(self, numero: str) -> (Candidato | None):
        for c in self.candidatos:
            if c.numero == numero:
                return c

        return None
    
    # retorna string com relatorio dos votos relativos aos candidatos disputando o cargo
    def relatorio(self) -> str:
        return (
            f'{self}\n' +
            ''.join([f'{candidato} ({candidato.partido}) - {len(candidato.votos)} voto(s)\n' for candidato in self.candidatos])
        )
    
    # retorna representacao do cargo em string
    def __str__(self) -> str:
        return self.nome
