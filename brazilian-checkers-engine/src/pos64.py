"""
Pos64 - Posições para tabuleiro 8x8 (32 casas escuras)
Adaptado de lidraughts: modules/draughts/src/main/Pos.scala

Sistema de numeração de campos 1-32:
Campo 1-4: linha 1 (linha 8 visual, onde pretas começam)
Campo 29-32: linha 8 (linha 1 visual, onde brancas começam)
"""

from typing import Optional, Tuple, Dict


class Pos64:
    """
    Representa uma posição no tabuleiro 8x8 usando numeração de campo 1-32
    """

    # Tabelas de movimento pré-calculadas (do Lidraughts)
    # Formato: campo -> [esquerda-diagonal, direita-diagonal, reto]
    # -1 significa movimento impossível (fora do tabuleiro)

    MOVES_DOWN: Dict[int, Tuple[int, int, int]] = {
        1: (5, 6, 9),
        2: (6, 7, 10),
        3: (7, 8, 11),
        4: (8, -1, 12),
        5: (-1, 9, 13),
        6: (9, 10, 14),
        7: (10, 11, 15),
        8: (11, 12, 16),
        9: (13, 14, 17),
        10: (14, 15, 18),
        11: (15, 16, 19),
        12: (16, -1, 20),
        13: (-1, 17, 21),
        14: (17, 18, 22),
        15: (18, 19, 23),
        16: (19, 20, 24),
        17: (21, 22, 25),
        18: (22, 23, 26),
        19: (23, 24, 27),
        20: (24, -1, 28),
        21: (-1, 25, 29),
        22: (25, 26, 30),
        23: (26, 27, 31),
        24: (27, 28, 32),
        25: (29, 30, -1),
        26: (30, 31, -1),
        27: (31, 32, -1),
        28: (32, -1, -1),
    }

    MOVES_UP: Dict[int, Tuple[int, int, int]] = {
        5: (-1, 1, -1),
        6: (1, 2, -1),
        7: (2, 3, -1),
        8: (3, 4, -1),
        9: (5, 6, 1),
        10: (6, 7, 2),
        11: (7, 8, 3),
        12: (8, -1, 4),
        13: (-1, 9, 5),
        14: (9, 10, 6),
        15: (10, 11, 7),
        16: (11, 12, 8),
        17: (13, 14, 9),
        18: (14, 15, 10),
        19: (15, 16, 11),
        20: (16, -1, 12),
        21: (-1, 17, 13),
        22: (17, 18, 14),
        23: (18, 19, 15),
        24: (19, 20, 16),
        25: (21, 22, 17),
        26: (22, 23, 18),
        27: (23, 24, 19),
        28: (24, -1, 20),
        29: (-1, 25, 21),
        30: (25, 26, 22),
        31: (26, 27, 23),
        32: (27, 28, 24),
    }

    MOVES_HORIZONTAL: Dict[int, Tuple[int, int]] = {
        1: (-1, 2),
        2: (1, 3),
        3: (2, 4),
        4: (3, -1),
        5: (-1, 6),
        6: (5, 7),
        7: (6, 8),
        8: (7, -1),
        9: (-1, 10),
        10: (9, 11),
        11: (10, 12),
        12: (11, -1),
        13: (-1, 14),
        14: (13, 15),
        15: (14, 16),
        16: (15, -1),
        17: (-1, 18),
        18: (17, 19),
        19: (18, 20),
        20: (19, -1),
        21: (-1, 22),
        22: (21, 23),
        23: (22, 24),
        24: (23, -1),
        25: (-1, 26),
        26: (25, 27),
        27: (26, 28),
        28: (27, -1),
        29: (-1, 30),
        30: (29, 31),
        31: (30, 32),
        32: (31, -1),
    }

    def __init__(self, field: int):
        """
        Cria uma posição a partir do número do campo (1-32)
        """
        if field < 1 or field > 32:
            raise ValueError(f"Campo deve estar entre 1 e 32, recebido: {field}")

        self.field = field

        # Calcular x, y baseado no campo
        # field = 4 * (y - 1) + x
        self.y = ((field - 1) // 4) + 1  # linha 1-8
        self.x = ((field - 1) % 4) + 1  # coluna 1-4

    @classmethod
    def from_xy(cls, x: int, y: int) -> Optional['Pos64']:
        """
        Cria uma posição a partir de coordenadas x,y (1-4, 1-8)
        """
        if x < 1 or x > 4 or y < 1 or y > 8:
            return None

        field = 4 * (y - 1) + x
        return cls(field)

    @classmethod
    def from_algebraic(cls, notation: str) -> Optional['Pos64']:
        """
        Converte notação algébrica (ex: "a1") para Pos64

        Algoritmo do Lidraughts:
        algY = 9 - pos.y
        algX = pos.x * 2 - algY % 2

        Invertendo:
        y = 9 - algY
        x = (algX + algY % 2) / 2
        """
        if len(notation) != 2:
            return None

        alg_col = notation[0].lower()
        alg_row = notation[1]

        if alg_col < 'a' or alg_col > 'h' or not alg_row.isdigit():
            return None

        alg_x = ord(alg_col) - ord('a') + 1  # 1-8
        alg_y = int(alg_row)  # 1-8

        if alg_y < 1 or alg_y > 8:
            return None

        # Invertendo a fórmula do Lidraughts
        # algY = 9 - y → y = 9 - algY
        # algX = x * 2 - algY % 2 → x = (algX + algY % 2) / 2
        y = 9 - alg_y
        x = (alg_x + alg_y % 2) // 2

        # Verificar se está dentro dos limites válidos
        if x < 1 or x > 4 or y < 1 or y > 8:
            return None  # Fora dos limites

        return cls.from_xy(x, y)

    def to_algebraic(self) -> str:
        """
        Converte para notação algébrica

        Algoritmo do Lidraughts:
        algY = 9 - pos.y
        algX = pos.x * 2 - algY % 2
        """
        alg_y = 9 - self.y
        alg_x = self.x * 2 - alg_y % 2
        return f"{chr(96 + alg_x)}{alg_y}"

    def move_down_left(self) -> Optional['Pos64']:
        """Move diagonal para baixo-esquerda"""
        moves = self.MOVES_DOWN.get(self.field)
        if not moves or moves[0] == -1:
            return None
        return Pos64(moves[0])

    def move_down_right(self) -> Optional['Pos64']:
        """Move diagonal para baixo-direita"""
        moves = self.MOVES_DOWN.get(self.field)
        if not moves or moves[1] == -1:
            return None
        return Pos64(moves[1])

    def move_up_left(self) -> Optional['Pos64']:
        """Move diagonal para cima-esquerda"""
        moves = self.MOVES_UP.get(self.field)
        if not moves or moves[0] == -1:
            return None
        return Pos64(moves[0])

    def move_up_right(self) -> Optional['Pos64']:
        """Move diagonal para cima-direita"""
        moves = self.MOVES_UP.get(self.field)
        if not moves or moves[1] == -1:
            return None
        return Pos64(moves[1])

    def __repr__(self) -> str:
        return f"Pos64({self.field})"

    def __str__(self) -> str:
        return str(self.field)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pos64):
            return False
        return self.field == other.field

    def __hash__(self) -> int:
        return self.field - 1


# Criar todas as posições
ALL_POSITIONS = [Pos64(i) for i in range(1, 33)]
