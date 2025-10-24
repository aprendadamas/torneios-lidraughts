#!/usr/bin/env python3
"""Test pydraughts API"""

import draughts
from draughts import Board, Move

# Create a board with the exercise position
fen = "W:Wa1,b2,c3:Ba5,e5,g7"
board = Board(variant="brazilian", fen=fen)

print("FEN:", board.fen)
print("Turn:", "White" if board.turn else "Black")
print("\nBoard:")
print(board)

print("\nLegal moves:")
for i, move in enumerate(board.legal_moves(), 1):
    print(f"{i}. {move} (type: {type(move).__name__})")
    print(f"   str: {str(move)}")
    print(f"   repr: {repr(move)}")

    # Try to access move attributes
    if hasattr(move, 'pdn_move'):
        print(f"   pdn_move: {move.pdn_move}")
    if hasattr(move, 'move'):
        print(f"   move: {move.move}")
    if hasattr(move, 'steps'):
        print(f"   steps: {move.steps}")

    if i >= 3:  # Just show first 3 moves
        break

print("\nTesting move execution:")
legal_moves = list(board.legal_moves())
if legal_moves:
    first_move = legal_moves[0]
    print(f"Making move: {first_move}")
    test_board = board.copy()
    test_board.push(first_move)
    print(f"New FEN: {test_board.fen}")
    print(f"New board:")
    print(test_board)
