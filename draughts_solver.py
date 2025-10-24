#!/usr/bin/env python3
"""
Solver de Damas Brasileiras (Brazilian Draughts)
Resolve exercícios táticos usando busca minimax
"""

from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Move:
    """Representa um movimento no jogo de damas"""
    from_pos: int
    to_pos: int
    captures: List[int]  # Peças capturadas
    promotes: bool = False

    def __str__(self):
        """Retorna notação do movimento"""
        if self.captures:
            return f"{self.from_pos}x{self.to_pos}"
        return f"{self.from_pos}-{self.to_pos}"

    def to_notation(self):
        """Retorna notação completa com todas as capturas"""
        if self.captures:
            # Para capturas múltiplas, mostrar a sequência
            return f"{self.from_pos}x{self.to_pos}"
        return f"{self.from_pos}-{self.to_pos}"


class Board:
    """Tabuleiro de damas 8x8 (casas escuras numeradas 1-32)"""

    def __init__(self):
        self.white_men = set()      # Peões brancos
        self.white_kings = set()    # Damas brancas
        self.black_men = set()      # Peões pretos
        self.black_kings = set()    # Damas pretas

    def copy(self):
        """Cria uma cópia do tabuleiro"""
        new_board = Board()
        new_board.white_men = self.white_men.copy()
        new_board.white_kings = self.white_kings.copy()
        new_board.black_men = self.black_men.copy()
        new_board.black_kings = self.black_kings.copy()
        return new_board

    @staticmethod
    def from_fen(fen: str):
        """
        Cria tabuleiro a partir de notação FEN
        Formato: W:Wa1,b2:Ba5,e5 (W/B para turno, W/B para peças, maiúscula para damas)
        """
        board = Board()

        # Mapear notação algébrica para números (1-32)
        # Em damas brasileiras:
        # Linha 1: a1=1, c1=2, e1=3, g1=4
        # Linha 2: b2=5, d2=6, f2=7, h2=8
        # Linha 3: a3=9, c3=10, e3=11, g3=12
        # etc.
        def algebraic_to_num(square: str) -> int:
            col = ord(square[0]) - ord('a')  # 0-7
            row = int(square[1]) - 1  # 0-7

            # Linhas ímpares (0,2,4,6): casas escuras em colunas pares (a,c,e,g = 0,2,4,6)
            # Linhas pares (1,3,5,7): casas escuras em colunas ímpares (b,d,f,h = 1,3,5,7)

            if row % 2 == 0:  # Linhas 1,3,5,7 (row=0,2,4,6)
                # Colunas a,c,e,g (col=0,2,4,6)
                square_num = row * 4 + (col // 2) + 1
            else:  # Linhas 2,4,6,8 (row=1,3,5,7)
                # Colunas b,d,f,h (col=1,3,5,7)
                square_num = row * 4 + ((col + 1) // 2) + 1

            return square_num

        parts = fen.split(':')

        for part in parts[1:]:  # Pular a primeira parte (turno)
            if not part:
                continue

            color = part[0]  # W ou B
            pieces = part[1:].split(',')

            for piece in pieces:
                if not piece:
                    continue

                is_king = piece[0] in ['W', 'B']
                square = piece[1:] if is_king else piece

                try:
                    pos = algebraic_to_num(square)

                    if color == 'W':
                        if is_king:
                            board.white_kings.add(pos)
                        else:
                            board.white_men.add(pos)
                    else:
                        if is_king:
                            board.black_kings.add(pos)
                        else:
                            board.black_men.add(pos)
                except:
                    print(f"Erro ao processar peça: {piece}")

        return board

    def get_all_pieces(self, white: bool) -> Tuple[Set[int], Set[int]]:
        """Retorna (peões, damas) para o jogador especificado"""
        if white:
            return self.white_men, self.white_kings
        return self.black_men, self.black_kings

    def is_occupied(self, pos: int) -> bool:
        """Verifica se a posição está ocupada"""
        return (pos in self.white_men or pos in self.white_kings or
                pos in self.black_men or pos in self.black_kings)

    def get_piece_at(self, pos: int) -> Optional[str]:
        """Retorna o tipo de peça na posição ('WM', 'WK', 'BM', 'BK' ou None)"""
        if pos in self.white_men:
            return 'WM'
        if pos in self.white_kings:
            return 'WK'
        if pos in self.black_men:
            return 'BM'
        if pos in self.black_kings:
            return 'BK'
        return None

    def pos_to_coords(self, pos: int) -> Tuple[int, int]:
        """Converte número da casa (1-32) para coordenadas (row, col)"""
        pos_idx = pos - 1  # 0-31
        row = pos_idx // 4

        if row % 2 == 0:  # Linhas 1,3,5,7
            col = (pos_idx % 4) * 2  # a,c,e,g (0,2,4,6)
        else:  # Linhas 2,4,6,8
            col = (pos_idx % 4) * 2 + 1  # b,d,f,h (1,3,5,7)

        return (row, col)

    def coords_to_pos(self, row: int, col: int) -> Optional[int]:
        """Converte coordenadas (row, col) para número da casa (1-32)"""
        if not (0 <= row < 8 and 0 <= col < 8):
            return None

        # Verificar se é casa escura (soma PAR nas damas brasileiras)
        if (row + col) % 2 != 0:
            return None

        # Ambas as linhas usam a mesma fórmula
        pos = row * 4 + (col // 2) + 1

        return pos if 1 <= pos <= 32 else None

    def get_neighbors(self, pos: int) -> List[int]:
        """Retorna posições vizinhas diagonais"""
        row, col = self.pos_to_coords(pos)
        neighbors = []

        # Quatro direções diagonais
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            new_pos = self.coords_to_pos(new_row, new_col)
            if new_pos:
                neighbors.append(new_pos)

        return neighbors

    def can_capture(self, from_pos: int, direction: Tuple[int, int], white: bool) -> Optional[Tuple[int, int]]:
        """
        Verifica se pode capturar nesta direção
        Retorna (posição_capturada, posição_destino) ou None
        """
        row, col = self.pos_to_coords(from_pos)
        dr, dc = direction

        # Posição da peça a capturar
        cap_row = row + dr
        cap_col = col + dc

        cap_pos = self.coords_to_pos(cap_row, cap_col)
        if not cap_pos:
            return None

        # Verificar se tem peça inimiga
        piece = self.get_piece_at(cap_pos)
        if not piece:
            return None

        is_enemy = (white and piece[0] == 'B') or (not white and piece[0] == 'W')
        if not is_enemy:
            return None

        # Posição de destino (após captura)
        dest_row = cap_row + dr
        dest_col = cap_col + dc

        dest_pos = self.coords_to_pos(dest_row, dest_col)
        if not dest_pos:
            return None

        # Verificar se destino está livre
        if self.is_occupied(dest_pos):
            return None

        return (cap_pos, dest_pos)

    def generate_captures(self, pos: int, white: bool, is_king: bool, captured: Set[int] = None) -> List[Move]:
        """Gera todas as capturas possíveis a partir de uma posição (incluindo múltiplas)"""
        if captured is None:
            captured = set()

        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Para peões, só capturam para frente também nas damas brasileiras
        # Mas após captura, podem continuar em qualquer direção

        for direction in directions:
            result = self.can_capture(pos, direction, white)
            if result:
                cap_pos, dest_pos = result

                # Não capturar a mesma peça duas vezes
                if cap_pos in captured:
                    continue

                # Criar movimento
                new_captured = captured | {cap_pos}

                # Verificar se promove (chega na última linha)
                promotes = False
                dest_row = (dest_pos - 1) // 4
                if not is_king:
                    if white and dest_row == 7:
                        promotes = True
                    elif not white and dest_row == 0:
                        promotes = True

                # Criar tabuleiro temporário para continuar capturas
                temp_board = self.copy()

                # Remover peça capturada
                temp_board.white_men.discard(cap_pos)
                temp_board.white_kings.discard(cap_pos)
                temp_board.black_men.discard(cap_pos)
                temp_board.black_kings.discard(cap_pos)

                # Mover peça
                if white:
                    temp_board.white_men.discard(pos)
                    temp_board.white_kings.discard(pos)
                    if promotes or is_king:
                        temp_board.white_kings.add(dest_pos)
                    else:
                        temp_board.white_men.add(dest_pos)
                else:
                    temp_board.black_men.discard(pos)
                    temp_board.black_kings.discard(pos)
                    if promotes or is_king:
                        temp_board.black_kings.add(dest_pos)
                    else:
                        temp_board.black_men.add(dest_pos)

                # Tentar continuar capturando
                further_captures = temp_board.generate_captures(
                    dest_pos, white, is_king or promotes, new_captured
                )

                if further_captures:
                    # Adicionar capturas continuadas
                    for further_move in further_captures:
                        full_move = Move(
                            from_pos=pos,
                            to_pos=further_move.to_pos,
                            captures=list(new_captured) + further_move.captures,
                            promotes=further_move.promotes
                        )
                        moves.append(full_move)
                else:
                    # Captura simples
                    move = Move(
                        from_pos=pos,
                        to_pos=dest_pos,
                        captures=list(new_captured),
                        promotes=promotes
                    )
                    moves.append(move)

        return moves

    def generate_simple_moves(self, pos: int, white: bool, is_king: bool) -> List[Move]:
        """Gera movimentos simples (não capturas)"""
        moves = []

        row, col = self.pos_to_coords(pos)

        # Direções possíveis
        if is_king:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Peões só movem para frente
            if white:
                directions = [(1, -1), (1, 1)]
            else:
                directions = [(-1, -1), (-1, 1)]

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            dest_pos = self.coords_to_pos(new_row, new_col)
            if not dest_pos:
                continue

            if self.is_occupied(dest_pos):
                continue

            # Verificar promoção
            promotes = False
            if not is_king:
                if white and new_row == 7:
                    promotes = True
                elif not white and new_row == 0:
                    promotes = True

            move = Move(from_pos=pos, to_pos=dest_pos, captures=[], promotes=promotes)
            moves.append(move)

        return moves

    def generate_moves(self, white: bool) -> List[Move]:
        """Gera todos os movimentos legais para o jogador"""
        men, kings = self.get_all_pieces(white)

        # Primeiro, verificar se há capturas (obrigatórias)
        all_captures = []

        for pos in men:
            captures = self.generate_captures(pos, white, False)
            all_captures.extend(captures)

        for pos in kings:
            captures = self.generate_captures(pos, white, True)
            all_captures.extend(captures)

        # Se há capturas, elas são obrigatórias
        if all_captures:
            # Regra: capturar o máximo de peças possível
            max_captures = max(len(move.captures) for move in all_captures)
            return [move for move in all_captures if len(move.captures) == max_captures]

        # Senão, gerar movimentos simples
        all_moves = []

        for pos in men:
            moves = self.generate_simple_moves(pos, white, False)
            all_moves.extend(moves)

        for pos in kings:
            moves = self.generate_simple_moves(pos, white, True)
            all_moves.extend(moves)

        return all_moves

    def make_move(self, move: Move, white: bool) -> 'Board':
        """Executa um movimento e retorna novo tabuleiro"""
        new_board = self.copy()

        # Remover peça da posição original
        if white:
            new_board.white_men.discard(move.from_pos)
            is_king = move.from_pos in self.white_kings
            new_board.white_kings.discard(move.from_pos)
        else:
            new_board.black_men.discard(move.from_pos)
            is_king = move.from_pos in self.black_kings
            new_board.black_kings.discard(move.from_pos)

        # Remover peças capturadas
        for cap_pos in move.captures:
            new_board.white_men.discard(cap_pos)
            new_board.white_kings.discard(cap_pos)
            new_board.black_men.discard(cap_pos)
            new_board.black_kings.discard(cap_pos)

        # Adicionar peça na nova posição
        if white:
            if is_king or move.promotes:
                new_board.white_kings.add(move.to_pos)
            else:
                new_board.white_men.add(move.to_pos)
        else:
            if is_king or move.promotes:
                new_board.black_kings.add(move.to_pos)
            else:
                new_board.black_men.add(move.to_pos)

        return new_board

    def evaluate(self) -> float:
        """Avalia a posição (positivo = brancas ganham, negativo = pretas ganham)"""
        score = 0.0

        # Material
        score += len(self.white_men) * 100
        score += len(self.white_kings) * 300
        score -= len(self.black_men) * 100
        score -= len(self.black_kings) * 300

        # Posição (peças avançadas valem mais)
        for pos in self.white_men:
            row = (pos - 1) // 4
            score += row * 5

        for pos in self.black_men:
            row = (pos - 1) // 4
            score -= (7 - row) * 5

        return score

    def is_game_over(self) -> Optional[str]:
        """Verifica se o jogo terminou (retorna 'W', 'B' ou None)"""
        white_has_pieces = bool(self.white_men or self.white_kings)
        black_has_pieces = bool(self.black_men or self.black_kings)

        if not white_has_pieces:
            return 'B'
        if not black_has_pieces:
            return 'W'

        # Verificar se tem movimentos legais
        if not self.generate_moves(True):
            return 'B'
        if not self.generate_moves(False):
            return 'W'

        return None


def minimax(board: Board, depth: int, alpha: float, beta: float, white: bool) -> Tuple[float, Optional[Move]]:
    """Algoritmo minimax com poda alpha-beta"""

    # Verificar fim de jogo
    game_over = board.is_game_over()
    if game_over:
        if game_over == 'W':
            return (10000, None)
        else:
            return (-10000, None)

    if depth == 0:
        return (board.evaluate(), None)

    moves = board.generate_moves(white)
    if not moves:
        return (board.evaluate(), None)

    best_move = None

    if white:
        max_eval = float('-inf')
        for move in moves:
            new_board = board.make_move(move, white)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break

        return (max_eval, best_move)
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = board.make_move(move, white)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break

        return (min_eval, best_move)


def solve_exercise(fen: str, depth: int = 10) -> List[str]:
    """
    Resolve um exercício tático
    Retorna a sequência de movimentos que leva à vitória
    """
    board = Board.from_fen(fen)
    solution = []

    # Assumir que brancas jogam (W no FEN)
    white_turn = True

    for _ in range(20):  # Máximo 20 movimentos
        game_over = board.is_game_over()
        if game_over:
            break

        score, best_move = minimax(board, depth, float('-inf'), float('inf'), white_turn)

        if best_move is None:
            break

        solution.append(best_move.to_notation())
        board = board.make_move(best_move, white_turn)
        white_turn = not white_turn

        # Se a vantagem for decisiva, parar
        if abs(score) > 500:
            # Continuar só mais alguns movimentos para completar a combinação
            if abs(score) > 5000:
                break

    return solution


if __name__ == "__main__":
    # Exercícios
    exercises = [
        {
            "number": 1,
            "fen": "W:Wa1,b2,c3:Ba5,e5,g7."
        },
        {
            "number": 2,
            "fen": "W:Wa1,b2,c3,h4:Ba5,e5,f6,g7."
        },
        {
            "number": 3,
            "fen": "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8."
        },
        {
            "number": 4,
            "fen": "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7."
        },
        {
            "number": 5,
            "fen": "W:We1,f2:Bb4,f4,b6,d6."
        }
    ]

    print("=" * 60)
    print("SOLUÇÕES DOS EXERCÍCIOS DE DAMAS")
    print("=" * 60)

    for ex in exercises:
        print(f"\n{'='*60}")
        print(f"EXERCÍCIO {ex['number']}")
        print(f"{'='*60}")
        print(f"FEN: {ex['fen']}")
        print()

        try:
            solution = solve_exercise(ex['fen'], depth=12)

            if solution:
                print("SOLUÇÃO:")
                print(" → ".join(solution))
                print(f"\nTotal de lances: {len(solution)}")
            else:
                print("Nenhuma solução encontrada (posição pode estar empatada)")
        except Exception as e:
            print(f"ERRO ao resolver: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print("FIM DAS SOLUÇÕES")
    print(f"{'='*60}")
