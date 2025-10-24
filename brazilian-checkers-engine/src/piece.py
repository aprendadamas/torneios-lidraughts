"""
Módulo de peças do jogo de damas brasileiro
Define as peças (simples e damas) e suas propriedades
"""

from enum import Enum
from typing import Tuple


class PieceType(Enum):
    """Tipo da peça"""
    MAN = "man"      # Peça simples
    KING = "king"    # Dama


class Color(Enum):
    """Cor da peça"""
    WHITE = "white"
    BLACK = "black"


class Piece:
    """
    Representa uma peça no jogo de damas brasileiro

    Attributes:
        color (Color): Cor da peça (branca ou preta)
        piece_type (PieceType): Tipo da peça (simples ou dama)
        position (Tuple[int, int]): Posição atual da peça no tabuleiro (linha, coluna)
    """

    def __init__(self, color: Color, position: Tuple[int, int], piece_type: PieceType = PieceType.MAN):
        """
        Inicializa uma peça

        Args:
            color: Cor da peça
            position: Posição inicial (linha, coluna)
            piece_type: Tipo da peça (padrão: peça simples)
        """
        self.color = color
        self.piece_type = piece_type
        self.position = position

    def is_king(self) -> bool:
        """Verifica se a peça é uma dama"""
        return self.piece_type == PieceType.KING

    def promote_to_king(self):
        """Promove a peça a dama (coroação)"""
        self.piece_type = PieceType.KING

    def can_move_backward(self) -> bool:
        """
        Verifica se a peça pode mover para trás
        Peças simples não podem mover para trás (exceto em capturas)
        Damas podem mover em qualquer direção
        """
        return self.is_king()

    def get_forward_direction(self) -> int:
        """
        Retorna a direção de avanço da peça
        Brancas sobem (linha aumenta), pretas descem (linha diminui)
        """
        return 1 if self.color == Color.WHITE else -1

    def should_be_crowned(self, board_size: int = 8) -> bool:
        """
        Verifica se a peça deve ser coroada (virar dama)
        Brancas na última linha (7), pretas na primeira linha (0)
        """
        if self.is_king():
            return False

        row, _ = self.position
        if self.color == Color.WHITE:
            return row == board_size - 1
        else:
            return row == 0

    def __repr__(self) -> str:
        """Representação em string da peça"""
        symbol = "♔" if self.is_king() and self.color == Color.WHITE else \
                 "♚" if self.is_king() and self.color == Color.BLACK else \
                 "○" if self.color == Color.WHITE else "●"
        return f"{symbol}({self.position[0]},{self.position[1]})"

    def __str__(self) -> str:
        """String simplificada da peça para display"""
        if self.is_king():
            return "W" if self.color == Color.WHITE else "B"
        else:
            return "w" if self.color == Color.WHITE else "b"

    def copy(self):
        """Cria uma cópia da peça"""
        return Piece(self.color, self.position, self.piece_type)
