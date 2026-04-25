from src.domain.tabuleiro import Tabuleiro


class RegrasJogo:
    """Contém as regras do Super Jogo da Velha."""

    def obter_proximo_mini(self, linha: int, coluna: int) -> int:
        """Converte a posição jogada no mini atual para o próximo mini obrigatório."""
        return linha * 3 + coluna

    def mini_destino_esta_disponivel(self, tabuleiro: Tabuleiro, mini_id: int) -> bool:
        """Retorna True se o mini tabuleiro de destino ainda aceita jogadas."""
        return not tabuleiro.mini_esta_encerrado(mini_id)

    def jogada_valida(
        self,
        tabuleiro: Tabuleiro,
        mini_escolhido: int,
        linha: int,
        coluna: int,
        mini_obrigatorio: int | None,
    ) -> bool:
        """Valida se a jogada respeita as regras atuais da partida."""
        if not tabuleiro.mini_tabuleiro_valido(mini_escolhido):
            return False

        if tabuleiro.mini_esta_encerrado(mini_escolhido):
            return False

        if (
            mini_obrigatorio is not None
            and self.mini_destino_esta_disponivel(tabuleiro, mini_obrigatorio)
            and mini_escolhido != mini_obrigatorio
        ):
            return False

        mini = tabuleiro.obter_mini_tabuleiro(mini_escolhido)
        return mini.celula_esta_vazia(linha, coluna)