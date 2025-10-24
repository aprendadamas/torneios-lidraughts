#!/usr/bin/env python3
"""Solve Exercise 2"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board

# Import the working solver
sys.path.insert(0, '/home/user/torneios-lidraughts')
from final_solver import TacticalSolver


def main():
    fen = "W:Wa1,b2,c3,h4:Ba5,e5,f6,g7"

    print("\n" + "=" * 70)
    print("EXERCISE 2")
    print("=" * 70)
    print(f"\nFEN: {fen}")
    print()

    # Show initial position details
    board = Board(variant="brazilian", fen=fen)
    print("Initial position:")
    print(board)
    print()

    parts = fen.split(':')
    white_pieces = []
    black_pieces = []

    for part in parts:
        if part.startswith('W'):
            white_pieces = part[1:].replace('.', '').split(',')
        elif part.startswith('B'):
            black_pieces = part[1:].replace('.', '').split(',')

    print(f"White pieces ({len([p for p in white_pieces if p])}): {', '.join(filter(None, white_pieces))}")
    print(f"Black pieces ({len([p for p in black_pieces if p])}): {', '.join(filter(None, black_pieces))}")
    print()

    # Solve using tactical solver
    solver = TacticalSolver()
    solution = solver.solve(fen)

    if solution:
        print("\n" + "=" * 70)
        print("✓ SOLUTION FOUND!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗ No forced win found")
        print("=" * 70)
        print("\nTrying deeper search...")

        # Manual exploration of promising moves
        print("\nAnalyzing all first moves manually:")
        for move in board.legal_moves():
            print(f"\n  Testing {move.pdn_move}...")
            test_board = board.copy()
            test_board.push(move)
            black_moves = list(test_board.legal_moves())
            print(f"    Black has {len(black_moves)} responses")


if __name__ == "__main__":
    main()
