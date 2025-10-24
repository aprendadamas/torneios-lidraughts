#!/usr/bin/env python3
"""Teste de conversão de coordenadas"""

from draughts_solver import Board

board = Board()

print("Testando conversão pos -> coords -> pos:")
print("="*60)

for pos in [1, 2, 3, 4, 5, 6, 7, 8, 17, 19, 28]:
    row, col = board.pos_to_coords(pos)
    col_letter = chr(ord('a') + col)
    print(f"Pos {pos:2d} -> row={row} ({row+1}), col={col} ({col_letter}) -> sum={row+col} ({'par' if (row+col)%2==0 else 'ímpar'})")

    # Tentar converter de volta
    back_pos = board.coords_to_pos(row, col)
    if back_pos == pos:
        print(f"  ✓ Conversão de volta: {back_pos}")
    else:
        print(f"  ✗ ERRO na conversão de volta: esperado={pos}, obtido={back_pos}")

print("\n" + "="*60)
print("Padrão esperado:")
print("Linha 1 (row=0): a1, c1, e1, g1 (cols 0,2,4,6) - soma PAR")
print("Linha 2 (row=1): b2, d2, f2, h2 (cols 1,3,5,7) - soma PAR")
print("Linha 3 (row=2): a3, c3, e3, g3 (cols 0,2,4,6) - soma PAR")
