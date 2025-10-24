#!/usr/bin/env python3
"""Teste de geração de movimentos"""

from draughts_solver import Board

fen = "W:Wa1,b2,c3:Ba5,e5,g7."
board = Board.from_fen(fen)

print(f"Peões brancos: {sorted(board.white_men)}")
print(f"Peões pretos: {sorted(board.black_men)}")
print()

# Testar cada peça branca
for pos in sorted(board.white_men):
    print(f"\nTestando peça branca em {pos}:")
    row, col = board.pos_to_coords(pos)
    print(f"  Coordenadas: row={row}, col={col}")

    # Vizinhos
    neighbors = board.get_neighbors(pos)
    print(f"  Vizinhos: {neighbors}")

    # Tentar capturar
    print("  Tentando capturas:")
    for direction in [(1, -1), (1, 1)]:
        result = board.can_capture(pos, direction, white=True)
        if result:
            print(f"    Direção {direction}: captura possível! {result}")
        else:
            # Debug do motivo
            dr, dc = direction
            cap_row = row + dr
            cap_col = col + dc
            print(f"    Direção {direction}: cap_row={cap_row}, cap_col={cap_col}")
            cap_pos = board.coords_to_pos(cap_row, cap_col)
            if cap_pos:
                piece = board.get_piece_at(cap_pos)
                print(f"      Casa {cap_pos}: peça={piece}")
                if piece:
                    dest_row = cap_row + dr
                    dest_col = cap_col + dc
                    dest_pos = board.coords_to_pos(dest_row, dest_col)
                    print(f"      Destino: row={dest_row}, col={dest_col}, pos={dest_pos}")
                    if dest_pos:
                        occupied = board.is_occupied(dest_pos)
                        print(f"        Ocupado: {occupied}")

    # Movimentos simples
    simple_moves = board.generate_simple_moves(pos, white=True, is_king=False)
    print(f"  Movimentos simples: {[m.to_notation() for m in simple_moves]}")

    # Todas as capturas
    captures = board.generate_captures(pos, white=True, is_king=False)
    print(f"  Capturas: {[m.to_notation() for m in captures]}")

print("\n" + "="*60)
print("Movimentos finais gerados:")
moves = board.generate_moves(True)
for move in moves:
    print(f"  {move.to_notation()}")
