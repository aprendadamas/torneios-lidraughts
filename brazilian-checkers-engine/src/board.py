"""
Módulo do tabuleiro de damas brasileiro
Define o tabuleiro 8x8 e operações básicas
"""

from typing import List, Tuple, Optional, Dict
from .piece import Piece, Color, PieceType


class Board:
    """
    Representa o tabuleiro de damas brasileiro (8x8)

    Coordenadas:
    - (0,0) é o canto superior esquerdo
    - (7,7) é o canto inferior direito
    - Peças pretas começam nas linhas 5, 6, 7
    - Peças brancas começam nas linhas 0, 1, 2
    """

    def __init__(self, size: int = 8):
        """
        Inicializa o tabuleiro

        Args:
            size: Tamanho do tabuleiro (padrão: 8x8)
        """
        self.size = size
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(size)] for _ in range(size)]
        self.pieces: Dict[Color, List[Piece]] = {Color.WHITE: [], Color.BLACK: []}

    def setup_initial_position(self):
        """
        Configura a posição inicial do jogo
        Convenção: linha 0 do array = linha 8 da notação (topo/pretas)
                   linha 7 do array = linha 1 da notação (base/brancas)
        """
        # Peças brancas nas linhas 5, 6, 7 do array (linhas 3, 2, 1 da notação)
        for row in range(5, 8):
            for col in range(self.size):
                # Apenas casas escuras (soma de linha + coluna é ímpar)
                if (row + col) % 2 == 1:
                    piece = Piece(Color.WHITE, (row, col))
                    self.board[row][col] = piece
                    self.pieces[Color.WHITE].append(piece)

        # Peças pretas nas linhas 0, 1, 2 do array (linhas 8, 7, 6 da notação)
        for row in range(3):
            for col in range(self.size):
                # Apenas casas escuras
                if (row + col) % 2 == 1:
                    piece = Piece(Color.BLACK, (row, col))
                    self.board[row][col] = piece
                    self.pieces[Color.BLACK].append(piece)

    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """Verifica se uma posição é válida no tabuleiro"""
        row, col = pos
        return 0 <= row < self.size and 0 <= col < self.size

    def is_dark_square(self, pos: Tuple[int, int]) -> bool:
        """Verifica se uma casa é escura (jogável)"""
        row, col = pos
        return (row + col) % 2 == 1

    def get_piece(self, pos: Tuple[int, int]) -> Optional[Piece]:
        """Retorna a peça em uma posição, ou None se vazia"""
        if not self.is_valid_position(pos):
            return None
        row, col = pos
        return self.board[row][col]

    def is_empty(self, pos: Tuple[int, int]) -> bool:
        """Verifica se uma posição está vazia"""
        return self.get_piece(pos) is None

    def place_piece(self, piece: Piece, pos: Tuple[int, int]):
        """Coloca uma peça em uma posição"""
        if not self.is_valid_position(pos):
            raise ValueError(f"Posição inválida: {pos}")

        row, col = pos
        self.board[row][col] = piece
        piece.position = pos

    def remove_piece(self, pos: Tuple[int, int]) -> Optional[Piece]:
        """Remove e retorna a peça de uma posição"""
        piece = self.get_piece(pos)
        if piece:
            row, col = pos
            self.board[row][col] = None
            if piece in self.pieces[piece.color]:
                self.pieces[piece.color].remove(piece)
        return piece

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """
        Move uma peça de uma posição para outra
        Não valida se o movimento é legal - apenas executa
        """
        piece = self.remove_piece(from_pos)
        if piece:
            self.place_piece(piece, to_pos)

            # Verificar coroação
            if piece.should_be_crowned(self.size):
                piece.promote_to_king()

    def get_pieces_by_color(self, color: Color) -> List[Piece]:
        """Retorna todas as peças de uma cor"""
        return self.pieces[color].copy()

    def count_pieces(self, color: Color) -> int:
        """Conta quantas peças de uma cor existem no tabuleiro"""
        return len(self.pieces[color])

    def get_diagonal_path(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Retorna o caminho diagonal entre duas posições
        Não inclui as posições de origem e destino
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_step = 1 if to_row > from_row else -1
        col_step = 1 if to_col > from_col else -1

        path = []
        row, col = from_row + row_step, from_col + col_step

        while (row, col) != to_pos:
            path.append((row, col))
            row += row_step
            col += col_step

        return path

    def display(self):
        """Exibe o tabuleiro no console"""
        print("\n  ", end="")
        for col in range(self.size):
            print(f" {col} ", end="")
        print()

        for row in range(self.size):
            print(f"{row} ", end="")
            for col in range(self.size):
                piece = self.board[row][col]
                if piece:
                    print(f" {str(piece)} ", end="")
                elif self.is_dark_square((row, col)):
                    print(" . ", end="")
                else:
                    print("   ", end="")
            print()
        print()

    def copy(self):
        """Cria uma cópia profunda do tabuleiro"""
        new_board = Board(self.size)

        for color in [Color.WHITE, Color.BLACK]:
            for piece in self.pieces[color]:
                new_piece = piece.copy()
                new_board.place_piece(new_piece, piece.position)
                new_board.pieces[color].append(new_piece)

        return new_board

    def __repr__(self) -> str:
        """Representação em string do tabuleiro"""
        return f"Board({self.size}x{self.size}, White: {self.count_pieces(Color.WHITE)}, Black: {self.count_pieces(Color.BLACK)})"
