"""
Jogar partida completa a partir da posição do exercício
Brancas vs Pretas - ambos jogados logicamente
"""

from src.pos64 import Pos64
from typing import Set, List, Tuple, Optional

class GameState:
    def __init__(self, white: Set[int], black: Set[int], turn: str = "white"):
        self.white = white.copy()
        self.black = black.copy()
        self.turn = turn
        self.move_count = 0
        self.game_over = False
        self.winner = None

    def copy(self):
        return GameState(self.white, self.black, self.turn)

    def print_board(self, title=""):
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
                        print(" w", end="")
                    elif pos.field in self.black:
                        print(" b", end="")
                    else:
                        print(" ·", end="")
                else:
                    print("  ", end="")
            print(" │")
        print("  └─────────────────────────┘")
        print()

    def get_all_captures(self) -> List[Tuple[int, List[int], int]]:
        """Retorna todas as capturas possíveis (from_field, captured_fields, to_field)"""
        captures = []
        pieces = self.white if self.turn == "white" else self.black
        enemies = self.black if self.turn == "white" else self.white

        for piece_field in pieces:
            piece_captures = self._get_captures_from(piece_field, enemies, [])
            captures.extend(piece_captures)

        return captures

    def _get_captures_from(self, from_field: int, enemies: Set[int],
                          already_captured: List[int]) -> List[Tuple[int, List[int], int]]:
        """Busca recursiva de capturas (incluindo múltiplas)"""
        pos = Pos64(from_field)
        captures = []

        # Direções de movimento (brancas sobem = movesUp, pretas descem = movesDown)
        if self.turn == "white":
            # Brancas movem para cima
            directions = [
                (pos.move_up_left, lambda p: p.move_up_left()),
                (pos.move_up_right, lambda p: p.move_up_right()),
            ]
        else:
            # Pretas movem para baixo
            directions = [
                (pos.move_down_left, lambda p: p.move_down_left()),
                (pos.move_down_right, lambda p: p.move_down_right()),
            ]

        for get_adjacent, get_jump in directions:
            adjacent = get_adjacent()
            if adjacent and adjacent.field in enemies and adjacent.field not in already_captured:
                # Tem inimigo adjacente não capturado ainda
                jump_dest = get_jump(adjacent)
                if jump_dest:
                    # Verificar se destino está livre
                    all_pieces = self.white | self.black
                    # Remover peças já capturadas
                    for captured in already_captured:
                        all_pieces.discard(captured)

                    if jump_dest.field not in all_pieces:
                        # Captura válida
                        new_captured = already_captured + [adjacent.field]

                        # Verificar capturas adicionais
                        further = self._get_captures_from(jump_dest.field, enemies, new_captured)

                        if further:
                            # Tem capturas adicionais
                            captures.extend(further)
                        else:
                            # Sem mais capturas, esta é uma sequência final
                            captures.append((from_field, new_captured, jump_dest.field))

        return captures

    def get_simple_moves(self) -> List[Tuple[int, int]]:
        """Retorna movimentos simples (sem captura)"""
        moves = []
        pieces = self.white if self.turn == "white" else self.black
        all_pieces = self.white | self.black

        for piece_field in pieces:
            pos = Pos64(piece_field)

            # Direções (brancas sobem, pretas descem)
            if self.turn == "white":
                directions = [pos.move_up_left(), pos.move_up_right()]
            else:
                directions = [pos.move_down_left(), pos.move_down_right()]

            for dest in directions:
                if dest and dest.field not in all_pieces:
                    moves.append((piece_field, dest.field))

        return moves

    def make_move(self, from_field: int, to_field: int, captured: List[int] = None) -> bool:
        """Executa um movimento"""
        if captured is None:
            captured = []

        # Mover peça
        if self.turn == "white":
            if from_field in self.white:
                self.white.remove(from_field)
            self.white.add(to_field)
        else:
            if from_field in self.black:
                self.black.remove(from_field)
            self.black.add(to_field)

        # Remover capturadas
        for cap_field in captured:
            if cap_field in self.white:
                self.white.remove(cap_field)
            elif cap_field in self.black:
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

# Posição inicial do exercício
white_start = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_start = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

game = GameState(white_start, black_start, "white")

print("="*70)
print("PARTIDA COMPLETA - EXERCÍCIO #15")
print("="*70)

game.print_board("POSIÇÃO INICIAL:")

# Registro da partida
moves_notation = []

# Jogar até fim de jogo ou 50 lances
max_moves = 50
while not game.game_over and game.move_count < max_moves:
    # Verificar capturas obrigatórias
    captures = game.get_all_captures()

    if captures:
        # Escolher captura com mais peças capturadas
        best_capture = max(captures, key=lambda c: len(c[1]))
        from_field, captured_fields, to_field = best_capture

        from_alg = Pos64(from_field).to_algebraic()
        to_alg = Pos64(to_field).to_algebraic()

        # Criar notação com capturas
        capture_notation = from_alg
        for cap in captured_fields:
            capture_notation += f" x {Pos64(cap).to_algebraic()}"
        capture_notation += f" → {to_alg}"

        print(f"{game.move_count + 1}. {game.turn}: {capture_notation}")
        moves_notation.append(f"{game.move_count + 1}. {capture_notation}")

        game.make_move(from_field, to_field, captured_fields)

    else:
        # Sem capturas, fazer movimento simples
        simple_moves = game.get_simple_moves()

        if not simple_moves:
            print(f"\n{game.turn} não tem movimentos legais!")
            game.game_over = True
            game.winner = "black" if game.turn == "white" else "white"
            break

        # Escolher movimento (priorizar avanço central)
        best_move = simple_moves[0]
        for move in simple_moves:
            # Preferir movimentos centrais (campos menores para brancas, maiores para pretas)
            if game.turn == "white" and move[1] < best_move[1]:
                best_move = move
            elif game.turn == "black" and move[1] > best_move[1]:
                best_move = move

        from_field, to_field = best_move
        from_alg = Pos64(from_field).to_algebraic()
        to_alg = Pos64(to_field).to_algebraic()

        print(f"{game.move_count + 1}. {game.turn}: {from_alg} → {to_alg}")
        moves_notation.append(f"{game.move_count + 1}. {from_alg} → {to_alg}")

        game.make_move(from_field, to_field)

game.print_board("POSIÇÃO FINAL:")

print("="*70)
print("RESULTADO")
print("="*70)
print()
if game.winner:
    print(f"Vencedor: {game.winner.upper()}")
else:
    print("Partida interrompida (limite de lances)")

print()
print("="*70)
print("NOTAÇÃO ALGÉBRICA COMPLETA DA PARTIDA")
print("="*70)
print()
for notation in moves_notation:
    print(notation)

print()
print("="*70)
print("ANÁLISE")
print("="*70)
print(f"Total de lances: {game.move_count}")
print(f"Peças brancas restantes: {len(game.white)}")
print(f"Peças pretas restantes: {len(game.black)}")
