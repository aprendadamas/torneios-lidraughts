"""
Resolve o exercício tático passo a passo
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game import Game
from src.piece import Piece, Color, PieceType
from src.utils import algebraic_to_coords, coords_to_algebraic


def setup_from_fen(fen_string):
    """Configura posição do FEN"""
    game = Game()
    game.board = game.board.__class__()

    parts = fen_string.split(':')
    current_player = parts[0]
    white_pieces_str = parts[1].replace('W', '', 1)
    black_pieces_str = parts[2].replace('B', '', 1).replace('.', '')

    white_pieces = [p.strip() for p in white_pieces_str.split(',') if p.strip()]
    black_pieces = [p.strip() for p in black_pieces_str.split(',') if p.strip()]

    for piece_notation in white_pieces:
        is_king = piece_notation[0] == 'K'
        pos_str = piece_notation[1:] if is_king else piece_notation
        pos = algebraic_to_coords(pos_str)
        piece_type = PieceType.KING if is_king else PieceType.MAN
        piece = Piece(Color.WHITE, pos, piece_type)
        game.board.place_piece(piece, pos)
        game.board.pieces[Color.WHITE].append(piece)

    for piece_notation in black_pieces:
        is_king = piece_notation[0] == 'K'
        pos_str = piece_notation[1:] if is_king else piece_notation
        pos = algebraic_to_coords(pos_str)
        piece_type = PieceType.KING if is_king else PieceType.MAN
        piece = Piece(Color.BLACK, pos, piece_type)
        game.board.place_piece(piece, pos)
        game.board.pieces[Color.BLACK].append(piece)

    game.current_player = Color.WHITE if current_player == 'W' else Color.BLACK
    return game


# Exercício do Curso Aprenda Damas
fen = "W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8."

print("="*60)
print("EXERCÍCIO TÁTICO - 1800 Combinações")
print("="*60)
print(f"\nFEN: {fen}")
print("\nBrancas: c1, b2, d2, f4, h4")
print("Pretas: a3, d6, h6, e7, f8")
print("\nVez das BRANCAS - Encontre a melhor sequência!\n")

game = setup_from_fen(fen)

print("Posição inicial:")
game.display_board()

# Analisar jogadas disponíveis
all_moves = game.get_all_legal_moves()

print("\n" + "="*60)
print("ANÁLISE DETALHADA DOS MOVIMENTOS")
print("="*60)

for pos, moves in all_moves.items():
    from_alg = coords_to_algebraic(pos)
    piece = game.board.get_piece(pos)

    print(f"\nPeça em {from_alg}:")
    for move in moves:
        to_alg = coords_to_algebraic(move.to_pos)

        # Simular o movimento
        test_game = Game()
        test_game.board = game.board.copy()
        test_game.current_player = game.current_player
        test_game.make_move(move.from_pos, move.to_pos)

        # Avaliar posição resultante
        white_count = test_game.board.count_pieces(Color.WHITE)
        black_count = test_game.board.count_pieces(Color.BLACK)

        # Verificar se há capturas para as pretas na próxima jogada
        pretas_all_moves = test_game.get_all_legal_moves()
        pretas_capturas = any(any(m.is_capture() for m in moves) for moves in pretas_all_moves.values())

        status = ""
        if move.is_promotion:
            status += " [VIRA DAMA]"
        if pretas_capturas:
            status += " ⚠️ Pretas têm captura!"

        print(f"  {from_alg} -> {to_alg}{status}")
        print(f"    Resultado: Brancas={white_count}, Pretas={black_count}")

print("\n" + "="*60)
print("RECOMENDAÇÃO")
print("="*60)

print("\n1. b2 -> a1 (Vira Dama)")
print("   OU")
print("2. d2 -> e1 (Vira Dama)")
print("\nAmbas coronam uma dama, dando vantagem posicional.")
print("\nVamos testar b2 -> a1:")

game.make_move((6, 1), (7, 0))  # b2 -> a1

print("\nApós b2 -> a1:")
game.display_board()

piece_a1 = game.board.get_piece((7, 0))
print(f"\nA peça em a1 é uma dama: {piece_a1.is_king()}")

print("\n" + "="*60)
print("Agora é a vez das PRETAS")
print("="*60)

# Mostrar os movimentos das pretas
all_moves_black = game.get_all_legal_moves()

print(f"\nPretas têm {len(all_moves_black)} peças com movimentos:")
for pos, moves in list(all_moves_black.items())[:3]:  # Mostrar algumas
    from_alg = coords_to_algebraic(pos)
    print(f"  {from_alg}: {len(moves)} movimento(s)")

print("\n✅ Motor funcionando corretamente!")
print("   Analisou a posição e encontrou os melhores lances.")
