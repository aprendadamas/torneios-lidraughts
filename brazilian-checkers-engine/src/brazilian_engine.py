"""
Motor de jogo de Damas Brasileiras
Baseado na implementação do Lidraughts (Russian/Brazilian variant)
"""

from typing import Set, List, Tuple, Optional
from dataclasses import dataclass
from src.pos64 import Pos64


@dataclass
class Capture:
    """Representa uma captura (possivelmente múltipla)"""
    from_field: int
    to_field: int
    captured_fields: List[int]

    def length(self) -> int:
        return len(self.captured_fields)


class BrazilianGame:
    """Motor de jogo de Damas Brasileiras"""

    def __init__(self, white: Set[int], black: Set[int], turn: str = "white"):
        """
        Inicializa o jogo

        Args:
            white: Conjunto de campos das peças brancas
            black: Conjunto de campos das peças pretas
            turn: Turno atual ("white" ou "black")
        """
        self.white = white.copy()
        self.black = black.copy()
        self.turn = turn
        self.move_count = 0
        self.game_over = False
        self.winner: Optional[str] = None

    def copy(self) -> 'BrazilianGame':
        """Cria uma cópia do estado do jogo"""
        game = BrazilianGame(self.white, self.black, self.turn)
        game.move_count = self.move_count
        game.game_over = self.game_over
        game.winner = self.winner
        return game

    def get_all_pieces(self) -> Set[int]:
        """Retorna todas as peças no tabuleiro"""
        return self.white | self.black

    def get_current_pieces(self) -> Set[int]:
        """Retorna as peças do jogador atual"""
        return self.white if self.turn == "white" else self.black

    def get_enemy_pieces(self) -> Set[int]:
        """Retorna as peças do adversário"""
        return self.black if self.turn == "white" else self.white

    def find_all_captures(self) -> List[Capture]:
        """
        Encontra todas as capturas possíveis para o jogador atual

        IMPORTANTE: Peões capturam em TODAS as 4 direções diagonais,
        mesmo que só possam mover para frente normalmente.

        Returns:
            Lista de todas as capturas possíveis
        """
        captures = []
        current_pieces = self.get_current_pieces()

        for piece_field in current_pieces:
            piece_captures = self._find_captures_from(
                piece_field,
                piece_field,  # original_from
                self.get_all_pieces().copy(),
                []
            )
            captures.extend(piece_captures)

        return captures

    def _find_captures_from(
        self,
        current_field: int,
        original_from: int,
        occupied: Set[int],
        already_captured: List[int]
    ) -> List[Capture]:
        """
        Busca recursiva de capturas a partir de um campo

        Args:
            current_field: Campo atual da peça (pode ser intermediário)
            original_from: Campo original de onde a peça começou
            occupied: Conjunto de campos ocupados (exceto os já capturados)
            already_captured: Lista de campos já capturados nesta sequência

        Returns:
            Lista de capturas possíveis (incluindo capturas múltiplas)
        """
        pos = Pos64(current_field)
        enemy_pieces = self.get_enemy_pieces()
        captures = []

        # Verificar capturas em TODAS as 4 direções diagonais
        # (mesmo peões capturam para trás em damas brasileiras!)
        directions = [
            (pos.move_up_left, lambda p: p.move_up_left()),      # ↖
            (pos.move_up_right, lambda p: p.move_up_right()),    # ↗
            (pos.move_down_left, lambda p: p.move_down_left()),  # ↙
            (pos.move_down_right, lambda p: p.move_down_right()) # ↘
        ]

        for get_adjacent, get_beyond in directions:
            adjacent = get_adjacent()

            if not adjacent:
                continue

            # Verificar se há peça inimiga adjacente não capturada ainda
            if adjacent.field not in enemy_pieces:
                continue

            if adjacent.field in already_captured:
                continue

            # Verificar se o campo além está livre
            beyond = get_beyond(adjacent)
            if not beyond:
                continue

            if beyond.field in occupied:
                continue

            # Captura válida!
            new_captured = already_captured + [adjacent.field]

            # Atualizar campos ocupados (remover a peça capturada)
            new_occupied = occupied.copy()
            new_occupied.discard(adjacent.field)
            new_occupied.discard(current_field)  # Peça saiu do campo atual
            new_occupied.add(beyond.field)        # Peça chegou no novo campo

            # Verificar capturas adicionais a partir do novo campo
            further_captures = self._find_captures_from(
                beyond.field,
                original_from,  # Preservar o campo original!
                new_occupied,
                new_captured
            )

            if further_captures:
                # Há capturas adicionais - adicionar todas
                captures.extend(further_captures)
            else:
                # Sem capturas adicionais - esta é uma sequência final
                captures.append(Capture(
                    from_field=original_from,  # Usar o campo original!
                    to_field=beyond.field,
                    captured_fields=new_captured
                ))

        return captures

    def find_simple_moves(self) -> List[Tuple[int, int]]:
        """
        Encontra todos os movimentos simples (sem captura)

        IMPORTANTE: Só válido se não houver capturas disponíveis!

        Returns:
            Lista de tuplas (from_field, to_field)
        """
        moves = []
        current_pieces = self.get_current_pieces()
        occupied = self.get_all_pieces()

        for piece_field in current_pieces:
            pos = Pos64(piece_field)

            # Direções de movimento (apenas para frente!)
            # Brancas movem para CIMA (UpLeft, UpRight)
            # Pretas movem para BAIXO (DownLeft, DownRight)
            if self.turn == "white":
                directions = [pos.move_up_left(), pos.move_up_right()]
            else:
                directions = [pos.move_down_left(), pos.move_down_right()]

            for dest in directions:
                if dest and dest.field not in occupied:
                    moves.append((piece_field, dest.field))

        return moves

    def make_move(self, from_field: int, to_field: int, captured: Optional[List[int]] = None) -> bool:
        """
        Executa um movimento

        Args:
            from_field: Campo de origem
            to_field: Campo de destino
            captured: Lista de campos capturados (None se movimento simples)

        Returns:
            True se o movimento foi executado com sucesso
        """
        if captured is None:
            captured = []

        # Mover peça
        current_pieces = self.white if self.turn == "white" else self.black

        if from_field in current_pieces:
            current_pieces.remove(from_field)
        current_pieces.add(to_field)

        # Remover peças capturadas
        for cap_field in captured:
            if cap_field in self.white:
                self.white.remove(cap_field)
            if cap_field in self.black:
                self.black.remove(cap_field)

        # Alternar turno
        self.turn = "black" if self.turn == "white" else "white"
        self.move_count += 1

        # Verificar fim de jogo
        if len(self.white) == 0:
            self.game_over = True
            self.winner = "black"
        elif len(self.black) == 0:
            self.game_over = True
            self.winner = "white"

        return True

    def print_board(self, title: str = ""):
        """Imprime o tabuleiro"""
        if title:
            print(f"\n{title}")
        print(f"Lance #{self.move_count} - Vez: {self.turn}")
        print("    a  b  c  d  e  f  g  h")
        print("  ┌─────────────────────────┐")

        for row in range(8, 0, -1):
            print(f"{row} │", end="")
            for col in 'abcdefgh':
                alg = f"{col}{row}"
                pos = Pos64.from_algebraic(alg)
                if pos:
                    if pos.field in self.white:
                        print(" W", end="")
                    elif pos.field in self.black:
                        print(" B", end="")
                    else:
                        print(" ·", end="")
                else:
                    print("  ", end="")
            print(" │")
        print("  └─────────────────────────┘")
        print()
