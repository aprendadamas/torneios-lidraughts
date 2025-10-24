#!/usr/bin/env python3
"""Test the specific line: 1. c3-b4 a5xc3 2. b2xd4xf6xh8"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def test_line():
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"
    board = Board(variant="brazilian", fen=fen)

    print("Starting position:")
    print(f"FEN: {fen}")
    print(f"Turn: {board.turn} (True=White, False=Black)")
    print(board)
    print()

    # Move 1: 10-13 (c3-b4)
    print("Move 1: White plays 10-13 (c3-b4)")
    for m in board.legal_moves():
        if m.pdn_move == "10-13":
            board.push(m)
            break

    print(f"Turn: {board.turn}")
    print(board)
    black_moves = list(board.legal_moves())
    print(f"Black has {len(black_moves)} legal moves: {[m.pdn_move for m in black_moves]}")
    print()

    # Black is FORCED to capture
    print("Black's forced capture: 17x10 (a5xc3)")
    for m in black_moves:
        if m.pdn_move == "17x10":
            board.push(m)
            break

    print(f"Turn: {board.turn}")
    print(board)
    white_moves = list(board.legal_moves())
    print(f"White has {len(white_moves)} legal moves: {[m.pdn_move for m in white_moves]}")
    print()

    # Move 2: 5x32 (b2xd4xf6xh8)
    print("Move 2: White plays 5x32 (b2xd4xf6xh8)")
    for m in white_moves:
        if m.pdn_move == "5x32":
            board.push(m)
            break

    print(f"Turn: {board.turn}")
    print(board)
    final_moves = list(board.legal_moves())
    print(f"Black has {len(final_moves)} legal moves")
    print()

    if len(final_moves) == 0:
        print("✓ MATE! Black has no legal moves")
        print(f"Final turn indicator: {board.turn} (should be False for Black)")
        return True
    else:
        print("✗ Not mate, Black can still move")
        return False


if __name__ == "__main__":
    result = test_line()
    sys.exit(0 if result else 1)
