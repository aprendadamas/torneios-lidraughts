"""
Funções auxiliares para o motor de damas brasileiro
"""

from typing import Tuple, List
from .piece import Color


def algebraic_to_coords(notation: str) -> Tuple[int, int]:
    """
    Converte notação algébrica para coordenadas
    Exemplo: 'a1' -> (7, 0), 'h8' -> (0, 7)

    Args:
        notation: Notação algébrica (ex: 'a1', 'h8')

    Returns:
        Tupla (linha, coluna)
    """
    col = ord(notation[0].lower()) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)


def coords_to_algebraic(coords: Tuple[int, int]) -> str:
    """
    Converte coordenadas para notação algébrica
    Exemplo: (7, 0) -> 'a1', (0, 7) -> 'h8'

    Args:
        coords: Tupla (linha, coluna)

    Returns:
        Notação algébrica (ex: 'a1')
    """
    row, col = coords
    return f"{chr(ord('a') + col)}{8 - row}"


def numeric_to_coords(pos: int) -> Tuple[int, int]:
    """
    Converte notação numérica (1-32) para coordenadas
    Usada em algumas variantes de damas

    Args:
        pos: Posição numérica (1-32)

    Returns:
        Tupla (linha, coluna)
    """
    if not 1 <= pos <= 32:
        raise ValueError("Posição deve estar entre 1 e 32")

    # Ajustar para índice 0
    pos -= 1

    # Calcular linha e coluna
    row = pos // 4
    col = (pos % 4) * 2

    # Ajustar para casa escura
    if row % 2 == 0:
        col += 1

    return (row, col)


def coords_to_numeric(coords: Tuple[int, int]) -> int:
    """
    Converte coordenadas para notação numérica (1-32)

    Args:
        coords: Tupla (linha, coluna)

    Returns:
        Posição numérica (1-32)
    """
    row, col = coords

    # Verificar se é casa escura
    if (row + col) % 2 == 0:
        raise ValueError("Coordenadas devem corresponder a uma casa escura")

    # Calcular posição
    pos = row * 4 + col // 2

    # Ajustar para índice 1
    return pos + 1


def parse_move_string(move_str: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Converte string de movimento para coordenadas
    Formatos aceitos:
    - 'a1-b2' (notação algébrica)
    - '1-5' (notação numérica)
    - '(0,1)-(1,2)' (coordenadas)

    Args:
        move_str: String representando o movimento

    Returns:
        Tupla com (posição_origem, posição_destino)
    """
    if '-' in move_str:
        parts = move_str.split('-')
        if len(parts) != 2:
            raise ValueError(f"Formato de movimento inválido: {move_str}")

        from_str, to_str = parts

        # Verificar formato
        if from_str[0].isalpha():
            # Notação algébrica
            return (algebraic_to_coords(from_str.strip()),
                    algebraic_to_coords(to_str.strip()))
        elif from_str[0] == '(':
            # Coordenadas
            from_pos = eval(from_str.strip())
            to_pos = eval(to_str.strip())
            return (from_pos, to_pos)
        else:
            # Notação numérica
            return (numeric_to_coords(int(from_str.strip())),
                    numeric_to_coords(int(to_str.strip())))

    raise ValueError(f"Formato de movimento inválido: {move_str}")


def format_move(from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                notation: str = 'algebraic') -> str:
    """
    Formata um movimento como string

    Args:
        from_pos: Posição de origem
        to_pos: Posição de destino
        notation: Tipo de notação ('algebraic', 'numeric', 'coords')

    Returns:
        String formatada do movimento
    """
    if notation == 'algebraic':
        return f"{coords_to_algebraic(from_pos)}-{coords_to_algebraic(to_pos)}"
    elif notation == 'numeric':
        return f"{coords_to_numeric(from_pos)}-{coords_to_numeric(to_pos)}"
    elif notation == 'coords':
        return f"{from_pos}-{to_pos}"
    else:
        raise ValueError(f"Notação inválida: {notation}")


def get_opponent_color(color: Color) -> Color:
    """Retorna a cor do oponente"""
    return Color.BLACK if color == Color.WHITE else Color.WHITE


def is_draw_by_repetition(move_history: List, max_repetitions: int = 3) -> bool:
    """
    Verifica se houve empate por repetição de posições

    Args:
        move_history: Histórico de movimentos
        max_repetitions: Número máximo de repetições permitidas

    Returns:
        True se houver empate por repetição
    """
    # Implementação simplificada - pode ser expandida
    if len(move_history) < max_repetitions * 2:
        return False

    # Verificar últimos movimentos para repetição
    # TODO: Implementar verificação completa de posições
    return False


def count_material(board, color: Color) -> int:
    """
    Conta o material de um jogador
    Peças simples = 1, Damas = 3

    Args:
        board: Tabuleiro do jogo
        color: Cor do jogador

    Returns:
        Valor total do material
    """
    pieces = board.get_pieces_by_color(color)
    total = 0

    for piece in pieces:
        if piece.is_king():
            total += 3
        else:
            total += 1

    return total
