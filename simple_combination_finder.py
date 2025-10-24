#!/usr/bin/env python3
"""
Simple Combination Finder
Tests all 3-7 move sequences and looks for Queen promotions
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def count_queens(board):
    """Count queens on the board"""
    fen = board.fen
    parts = fen.split(':')

    white_queens = 0
    black_queens = 0

    for part in parts:
        if part.startswith('W'):
            pieces = part[1:].replace('.', '').split(',')
            white_queens = len([p for p in pieces if p and p[0].isupper()])
        elif part.startswith('B'):
            pieces = part[1:].replace('.', '').split(',')
            black_queens = len([p for p in pieces if p and p[0].isupper()])

    return white_queens, black_queens


def find_combinations(fen, target_depth=7):
    """Find all sequences of target_depth moves"""
    board = Board(variant="brazilian", fen=fen)

    print(f"Searching sequences up to {target_depth} moves...")
    print()

    initial_wq, initial_bq = count_queens(board)

    combinations = []

    def search(board, moves_so_far, depth):
        if depth == 0:
            # Check if we gained a Queen
            wq, bq = count_queens(board)
            if wq > initial_wq and bq == initial_bq:
                # We promoted to Queen!
                combinations.append(list(moves_so_far))
            return

        legal_moves = list(board.legal_moves())

        # Game over
        if not legal_moves:
            return

        # If forced (only 1 move), always follow it
        if len(legal_moves) == 1:
            test_board = board.copy()
            test_board.push(legal_moves[0])
            search(test_board, moves_so_far + [legal_moves[0].pdn_move], depth - 1)
        else:
            # Try all moves
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)
                search(test_board, moves_so_far + [move.pdn_move], depth - 1)

    # Start search
    search(board, [], target_depth)

    return combinations


def main():
    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
    ]

    for number, fen in exercises:
        print("=" * 70)
        print(f"EXERCISE {number}")
        print("=" * 70)
        print(f"FEN: {fen}")
        print()

        board = Board(variant="brazilian", fen=fen)
        print(board)
        print()

        # Search for 7-move combinations
        combinations = find_combinations(fen, target_depth=7)

        print(f"\nFound {len(combinations)} combinations leading to Queen promotion:\n")

        for i, combo in enumerate(combinations[:5], 1):  # Show first 5
            print(f"{i}. {' → '.join(combo)}")

        if len(combinations) > 5:
            print(f"... and {len(combinations) - 5} more")

        # Verify first combination
        if combinations:
            print(f"\nVerifying first combination:")
            print("-" * 70)

            test_board = Board(variant="brazilian", fen=fen)

            for j, move_pdn in enumerate(combinations[0], 1):
                # Find and execute move
                found = False
                for move in test_board.legal_moves():
                    if move.pdn_move == move_pdn:
                        test_board.push(move)
                        player = "White" if j % 2 == 1 else "Black"
                        print(f"{j}. {move_pdn} ({player})")
                        found = True
                        break

                if not found:
                    print(f"ERROR: Move {move_pdn} not found!")
                    break

            print()
            print("Final position:")
            print(test_board)
            print()

            # Check queens
            wq, bq = count_queens(test_board)
            print(f"Queens: White {wq}, Black {bq}")

            if wq > 0 and bq == 0:
                print("\n✓ WHITE HAS QUEEN ADVANTAGE!")

        print()


if __name__ == "__main__":
    main()
