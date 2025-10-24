#!/usr/bin/env python3
"""Teste do solver com debug"""

from draughts_solver import Board, solve_exercise

# Teste do exercício 1
fen = "W:Wa1,b2,c3:Ba5,e5,g7."
print(f"Testando FEN: {fen}")
print()

board = Board.from_fen(fen)

print("Estado do tabuleiro:")
print(f"Peões brancos: {sorted(board.white_men)}")
print(f"Damas brancas: {sorted(board.white_kings)}")
print(f"Peões pretos: {sorted(board.black_men)}")
print(f"Damas pretas: {sorted(board.black_kings)}")
print()

print("Movimentos possíveis para brancas:")
moves = board.generate_moves(True)
for move in moves:
    print(f"  {move.to_notation()} (de {move.from_pos} para {move.to_pos}, capturas: {move.captures})")

print()
print(f"Avaliação: {board.evaluate()}")
print()

# Visualizar o tabuleiro
print("Tabuleiro visual (números 1-32):")
print("  +---+---+---+---+---+---+---+---+")
for row in range(7, -1, -1):
    print(f"{row+1} |", end="")
    for col in range(8):
        if (row + col) % 2 == 1:  # Casa escura
            # Calcular número da casa
            pos = board.coords_to_pos(row, col)

            # Verificar que peça está lá
            piece = board.get_piece_at(pos)
            if piece == 'WM':
                symbol = ' w '
            elif piece == 'WK':
                symbol = ' W '
            elif piece == 'BM':
                symbol = ' b '
            elif piece == 'BK':
                symbol = ' B '
            else:
                symbol = f'{pos:2d} '
            print(symbol, end="|")
        else:
            print("###", end="|")
    print()
    print("  +---+---+---+---+---+---+---+---+")
print("    a   b   c   d   e   f   g   h")
