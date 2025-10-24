#!/usr/bin/env python3
"""
Debug: Step through the correct solution and analyze each position
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def analyze_all_moves_at_depth(board, depth, current_line=""):
    """Recursively analyze all possible moves"""
    if depth == 0:
        return

    legal_moves = list(board.legal_moves())

    if not legal_moves:
        print(f"{current_line} -> GAME OVER ({'White' if not board.turn else 'Black'} wins)")
        return

    for move in legal_moves:
        new_board = board.copy()
        new_board.push(move)

        new_line = current_line + (" -> " if current_line else "") + move.pdn_move

        # Check if this leads to immediate mate
        after_moves = list(new_board.legal_moves())
        if not after_moves:
            print(f"✓ MATE FOUND: {new_line}")
            print(f"  Final position:")
            print(f"  {new_board.fen}")
            return

        # Continue search
        if depth > 1:
            analyze_all_moves_at_depth(new_board, depth - 1, new_line)


def main():
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("=" * 70)
    print("DEBUG: Exhaustive search for mate sequences")
    print("=" * 70)
    print(f"\nStarting FEN: {fen}")
    print()

    board = Board(variant="brazilian", fen=fen)

    print("All legal first moves for White:")
    for i, move in enumerate(board.legal_moves(), 1):
        print(f"  {i}. {move.pdn_move}")

    print("\n" + "=" * 70)
    print("EXPLORING: 10-13 (c3-b4) - The supposed correct first move")
    print("=" * 70)

    # Make first move: 10-13
    board_after_1 = board.copy()
    move_1 = None
    for m in board.legal_moves():
        if m.pdn_move == "10-13":
            move_1 = m
            break

    if not move_1:
        print("ERROR: Move 10-13 not found!")
        return

    board_after_1.push(move_1)
    print(f"\nAfter 1. 10-13 (c3-b4):")
    print(board_after_1)

    print("\nBlack's legal moves:")
    black_moves = list(board_after_1.legal_moves())
    for i, move in enumerate(black_moves, 1):
        print(f"  {i}. {move.pdn_move}")

    # Black's forced capture
    if len(black_moves) == 1:
        print("\n  --> Black has only ONE legal move (forced capture)")
        capture = black_moves[0]

        board_after_2 = board_after_1.copy()
        board_after_2.push(capture)

        print(f"\nAfter 1. 10-13 {capture.pdn_move}:")
        print(board_after_2)

        print("\nWhite's legal moves:")
        white_moves = list(board_after_2.legal_moves())
        for i, move in enumerate(white_moves, 1):
            print(f"  {i}. {move.pdn_move}")

            # Test each white move
            test_board = board_after_2.copy()
            test_board.push(move)

            # Check if Black has moves
            black_responses = list(test_board.legal_moves())
            if not black_responses:
                print(f"      *** THIS MOVE LEADS TO MATE! ***")
                print(f"\n      Final position after 2. {move.pdn_move}:")
                print(test_board)
                print(f"\n      FEN: {test_board.fen}")
            else:
                print(f"      Black has {len(black_responses)} moves: {[m.pdn_move for m in black_responses[:3]]}")

    print("\n" + "=" * 70)
    print("COMPLETE TREE SEARCH (depth 4)")
    print("=" * 70)
    print()

    analyze_all_moves_at_depth(board, 4)


if __name__ == "__main__":
    main()
