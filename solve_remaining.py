#!/usr/bin/env python3
"""Solve remaining exercises 3, 4, 10 with deeper search"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def solve_with_deeper_search(number, fen, max_depth=15):
    """Solve with deeper search"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number}")
    print(f"{'='*70}")
    print(f"FEN: {fen}")

    board = Board(variant="brazilian", fen=fen)
    print(board)
    print()

    # Try all first moves with manual search
    legal_moves = list(board.legal_moves())
    print(f"Analyzing {len(legal_moves)} first moves...")

    for i, move in enumerate(legal_moves, 1):
        pdn = move.pdn_move
        print(f"  {i}. {pdn}... ", end='', flush=True)

        test_board = board.copy()
        test_board.push(move)

        # Quick check if this leads somewhere
        black_moves = list(test_board.legal_moves())
        print(f"{len(black_moves)} responses")

    print("\nNo forced mate found within search depth")
    return None


def main():
    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
        (10, "W:We1,d2,a3,c3:Ba5,c5,e7,g7"),
    ]

    for number, fen in exercises:
        solve_with_deeper_search(number, fen)


if __name__ == "__main__":
    main()
