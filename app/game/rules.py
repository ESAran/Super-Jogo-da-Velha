from app.game.board import Tabuleiro


class RegrasJogo:
    """Regras puras da partida, sem entrada ou saida."""

    def obter_proximo_mini(self, linha: int, coluna: int) -> int:
        return linha * 3 + coluna

    def mini_destino_esta_disponivel(self, tabuleiro: Tabuleiro, mini_id: int) -> bool:
        return not tabuleiro.mini_esta_encerrado(mini_id)

    def jogada_valida(
        self,
        tabuleiro: Tabuleiro,
        mini_escolhido: int,
        linha: int,
        coluna: int,
        mini_obrigatorio: int | None,
    ) -> bool:
        if not tabuleiro.mini_tabuleiro_valido(mini_escolhido):
            return False

        if tabuleiro.mini_esta_encerrado(mini_escolhido):
            return False

        if self._deve_jogar_no_mini_obrigatorio(
            tabuleiro,
            mini_escolhido,
            mini_obrigatorio,
        ):
            return False

        mini_tabuleiro = tabuleiro.obter_mini_tabuleiro(mini_escolhido)
        return mini_tabuleiro.celula_esta_vazia(linha, coluna)

    def _deve_jogar_no_mini_obrigatorio(
        self,
        tabuleiro: Tabuleiro,
        mini_escolhido: int,
        mini_obrigatorio: int | None,
    ) -> bool:
        return (
            mini_obrigatorio is not None
            and self.mini_destino_esta_disponivel(tabuleiro, mini_obrigatorio)
            and mini_escolhido != mini_obrigatorio
        )
