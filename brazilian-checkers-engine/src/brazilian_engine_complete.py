"""
Motor COMPLETO de Damas Brasileiras
Incluindo suporte a PROMOÇÃO e DAMAS (Kings)
Baseado na implementação do Lidraughts (Russian/Brazilian variant)
"""

from typing import Set, List, Tuple, Optional, Dict
from dataclasses import dataclass
from src.pos64 import Pos64


@dataclass
class Piece:
    """Representa uma peça (peão ou dama)"""
    field: int
    is_king: bool

    def __hash__(self):
        return hash((self.field, self.is_king))

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.field == other.field and self.is_king == other.is_king


@dataclass
class Capture:
    """Representa uma captura (possivelmente múltipla)"""
    from_field: int
    to_field: int
    captured_fields: List[int]
    promotes: bool = False  # Se promove a dama durante a captura

    def length(self) -> int:
        return len(self.captured_fields)


class BrazilianGameComplete:
    """Motor COMPLETO de jogo de Damas Brasileiras com suporte a Kings"""

    def __init__(self, white_men: Set[int], black_men: Set[int],
                 white_kings: Set[int] = None, black_kings: Set[int] = None,
                 turn: str = "white"):
        """
        Inicializa o jogo

        Args:
            white_men: Conjunto de campos dos peões brancos
            black_men: Conjunto de campos dos peões pretos
            white_kings: Conjunto de campos das damas brancas
            black_kings: Conjunto de campos das damas pretas
            turn: Turno atual ("white" ou "black")
        """
        self.white_men = white_men.copy()
        self.black_men = black_men.copy()
        self.white_kings = (white_kings or set()).copy()
        self.black_kings = (black_kings or set()).copy()
        self.turn = turn
        self.move_count = 0
        self.game_over = False
        self.winner: Optional[str] = None

    def copy(self) -> 'BrazilianGameComplete':
        """Cria uma cópia do estado do jogo"""
        game = BrazilianGameComplete(
            self.white_men, self.black_men,
            self.white_kings, self.black_kings,
            self.turn
        )
        game.move_count = self.move_count
        game.game_over = self.game_over
        game.winner = self.winner
        return game

    def get_all_pieces(self) -> Set[int]:
        """Retorna todos os campos ocupados"""
        return self.white_men | self.black_men | self.white_kings | self.black_kings

    def get_current_men(self) -> Set[int]:
        """Retorna os peões do jogador atual"""
        return self.white_men if self.turn == "white" else self.black_men

    def get_current_kings(self) -> Set[int]:
        """Retorna as damas do jogador atual"""
        return self.white_kings if self.turn == "white" else self.black_kings

    def get_enemy_pieces(self) -> Set[int]:
        """Retorna todas as peças do adversário"""
        if self.turn == "white":
            return self.black_men | self.black_kings
        else:
            return self.white_men | self.white_kings

    def is_promotion_square(self, field: int, color: str) -> bool:
        """Verifica se um campo é casa de promoção"""
        # Brancas promovem em campos 1-4 (linha 8)
        # Pretas promovem em campos 29-32 (linha 1)
        if color == "white":
            return field in {1, 2, 3, 4}
        else:
            return field in {29, 30, 31, 32}

    def find_all_captures(self) -> List[Capture]:
        """
        Encontra todas as capturas possíveis para o jogador atual

        Returns:
            Lista de todas as capturas possíveis
        """
        captures = []

        # Capturas de peões
        for piece_field in self.get_current_men():
            piece_captures = self._find_man_captures(
                piece_field,
                piece_field,
                self.get_all_pieces().copy(),
                [],
                False  # não é dama ainda
            )
            captures.extend(piece_captures)

        # Capturas de damas
        for piece_field in self.get_current_kings():
            piece_captures = self._find_king_captures(
                piece_field,
                piece_field,
                self.get_all_pieces().copy(),
                []
            )
            captures.extend(piece_captures)

        return captures

    def _find_man_captures(
        self,
        current_field: int,
        original_from: int,
        occupied: Set[int],
        already_captured: List[int],
        is_promoted: bool
    ) -> List[Capture]:
        """Busca recursiva de capturas para PEÕES"""
        pos = Pos64(current_field)
        enemy_pieces = self.get_enemy_pieces()
        captures = []

        # Peões capturam em TODAS as 4 direções diagonais
        directions = [
            (pos.move_up_left, lambda p: p.move_up_left()),
            (pos.move_up_right, lambda p: p.move_up_right()),
            (pos.move_down_left, lambda p: p.move_down_left()),
            (pos.move_down_right, lambda p: p.move_down_right())
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

            # Atualizar campos ocupados
            new_occupied = occupied.copy()
            new_occupied.discard(adjacent.field)
            new_occupied.discard(current_field)
            new_occupied.add(beyond.field)

            # Verificar se promove
            promotes = self.is_promotion_square(beyond.field, self.turn)

            if promotes and not is_promoted:
                # REGRA FMJD: Se alcança linha de coroação, PRIMEIRO tenta
                # continuar capturando "no mesmo curso" (como peão)
                further_captures = self._find_man_captures(
                    beyond.field,
                    original_from,
                    new_occupied,
                    new_captured,
                    is_promoted=False  # Tenta continuar como peão!
                )

                if further_captures:
                    # Há mais capturas como peão - continua SEM promover
                    captures.extend(further_captures)
                else:
                    # Sem mais capturas - promove e para
                    captures.append(Capture(
                        from_field=original_from,
                        to_field=beyond.field,
                        captured_fields=new_captured,
                        promotes=True
                    ))
            else:
                # Não é linha de promoção ou já é dama
                further_captures = self._find_man_captures(
                    beyond.field,
                    original_from,
                    new_occupied,
                    new_captured,
                    is_promoted or promotes
                )

                if further_captures:
                    captures.extend(further_captures)
                else:
                    # Sem capturas adicionais - esta é uma sequência final
                    captures.append(Capture(
                        from_field=original_from,
                        to_field=beyond.field,
                        captured_fields=new_captured,
                        promotes=promotes
                    ))

        return captures

    def _find_king_captures(
        self,
        current_field: int,
        original_from: int,
        occupied: Set[int],
        already_captured: List[int]
    ) -> List[Capture]:
        """Busca recursiva de capturas para DAMAS (long range)"""
        pos = Pos64(current_field)
        enemy_pieces = self.get_enemy_pieces()
        captures = []

        # Damas capturam em todas as 4 direções (long range)
        directions = [
            (lambda p: p.move_up_left(), 'up_left'),
            (lambda p: p.move_up_right(), 'up_right'),
            (lambda p: p.move_down_left(), 'down_left'),
            (lambda p: p.move_down_right(), 'down_right')
        ]

        for get_next, dir_name in directions:
            # Caminhar na direção até encontrar uma peça
            walk_pos = pos
            squares_walked = []

            while True:
                next_pos = get_next(walk_pos)
                if not next_pos:
                    break

                if next_pos.field in occupied and next_pos.field != current_field:
                    # Encontrou uma peça
                    if next_pos.field in enemy_pieces and next_pos.field not in already_captured:
                        # É inimigo não capturado - pode capturar!
                        captured_field = next_pos.field

                        # Continuar na mesma direção para landing squares
                        landing_pos = get_next(next_pos)

                        while landing_pos and landing_pos.field not in occupied:
                            # Landing square válido
                            new_captured = already_captured + [captured_field]
                            new_occupied = occupied.copy()
                            new_occupied.discard(captured_field)
                            new_occupied.discard(current_field)
                            new_occupied.add(landing_pos.field)

                            # Buscar capturas adicionais
                            further = self._find_king_captures(
                                landing_pos.field,
                                original_from,
                                new_occupied,
                                new_captured
                            )

                            if further:
                                captures.extend(further)
                            else:
                                # Sem capturas adicionais
                                captures.append(Capture(
                                    from_field=original_from,
                                    to_field=landing_pos.field,
                                    captured_fields=new_captured,
                                    promotes=False  # Já é dama
                                ))

                            landing_pos = get_next(landing_pos)

                    break  # Parou nesta direção

                squares_walked.append(next_pos)
                walk_pos = next_pos

        return captures

    def find_simple_moves(self) -> List[Tuple[int, int, bool]]:
        """
        Encontra todos os movimentos simples (sem captura)

        Returns:
            Lista de tuplas (from_field, to_field, promotes)
        """
        moves = []

        # Movimentos de peões
        for piece_field in self.get_current_men():
            pos = Pos64(piece_field)
            occupied = self.get_all_pieces()

            # Peões movem apenas para frente
            if self.turn == "white":
                directions = [pos.move_up_left(), pos.move_up_right()]
            else:
                directions = [pos.move_down_left(), pos.move_down_right()]

            for dest in directions:
                if dest and dest.field not in occupied:
                    promotes = self.is_promotion_square(dest.field, self.turn)
                    moves.append((piece_field, dest.field, promotes))

        # Movimentos de damas (long range em todas as direções)
        for piece_field in self.get_current_kings():
            pos = Pos64(piece_field)
            occupied = self.get_all_pieces()

            directions = [
                lambda p: p.move_up_left(),
                lambda p: p.move_up_right(),
                lambda p: p.move_down_left(),
                lambda p: p.move_down_right()
            ]

            for get_next in directions:
                walk_pos = pos
                while True:
                    next_pos = get_next(walk_pos)
                    if not next_pos or next_pos.field in occupied:
                        break
                    moves.append((piece_field, next_pos.field, False))
                    walk_pos = next_pos

        return moves

    def make_move(self, from_field: int, to_field: int, captured: List[int] = None, promotes: bool = False) -> bool:
        """Executa um movimento"""
        if captured is None:
            captured = []

        # Determinar se é peão ou dama
        is_king = False
        if self.turn == "white":
            if from_field in self.white_men:
                self.white_men.remove(from_field)
            elif from_field in self.white_kings:
                self.white_kings.remove(from_field)
                is_king = True

            # Adicionar no destino
            if promotes or is_king:
                self.white_kings.add(to_field)
            else:
                self.white_men.add(to_field)
        else:
            if from_field in self.black_men:
                self.black_men.remove(from_field)
            elif from_field in self.black_kings:
                self.black_kings.remove(from_field)
                is_king = True

            # Adicionar no destino
            if promotes or is_king:
                self.black_kings.add(to_field)
            else:
                self.black_men.add(to_field)

        # Remover peças capturadas
        for cap_field in captured:
            self.white_men.discard(cap_field)
            self.white_kings.discard(cap_field)
            self.black_men.discard(cap_field)
            self.black_kings.discard(cap_field)

        # Alternar turno
        self.turn = "black" if self.turn == "white" else "white"
        self.move_count += 1

        # Verificar fim de jogo
        white_total = len(self.white_men) + len(self.white_kings)
        black_total = len(self.black_men) + len(self.black_kings)

        if white_total == 0:
            self.game_over = True
            self.winner = "black"
        elif black_total == 0:
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
                    if pos.field in self.white_men:
                        print(" w", end="")
                    elif pos.field in self.white_kings:
                        print(" W", end="")  # Maiúscula = dama
                    elif pos.field in self.black_men:
                        print(" b", end="")
                    elif pos.field in self.black_kings:
                        print(" B", end="")  # Maiúscula = dama
                    else:
                        print(" ·", end="")
                else:
                    print("  ", end="")
            print(" │")
        print("  └─────────────────────────┘")

        # Mostrar contagem de peças
        white_total = len(self.white_men) + len(self.white_kings)
        black_total = len(self.black_men) + len(self.black_kings)
        print(f"Brancas: {len(self.white_men)} peões + {len(self.white_kings)} damas = {white_total}")
        print(f"Pretas: {len(self.black_men)} peões + {len(self.black_kings)} damas = {black_total}")
        print()
