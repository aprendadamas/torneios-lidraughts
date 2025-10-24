#!/usr/bin/env python3
"""Deep exploration of Exercise 4 starting with 7-11"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def explore_line(fen, moves_sequence):
    """Explore a specific move sequence"""
    board = Board(variant="brazilian", fen=fen)

    print("Starting position:")
    print(board)
    print()

    for i, move_pdn in enumerate(moves_sequence, 1):
        legal_moves = list(board.legal_moves())

        # Find the move
        found_move = None
        for move in legal_moves:
            if move.pdn_move == move_pdn:
                found_move = move
                break

        if not found_move:
            print(f"\n✗ Move {i} ({move_pdn}) is NOT legal!")
            print(f"Legal moves: {[m.pdn_move for m in legal_moves]}")
            return None

        # Execute move
        board.push(found_move)

        player = "White" if i % 2 == 1 else "Black"
        print(f"{i}. {move_pdn} ({player})")

    print(f"\nPosition after {len(moves_sequence)} moves:")
    print(board)
    print()

    # Check final state
    final_moves = list(board.legal_moves())
    if not final_moves:
        winner = "White" if board.turn == 1 else "Black"
        print(f"*** MATE! {winner} wins! ***")
        return True
    else:
        print(f"Next to move: {'White' if board.turn == 2 else 'Black'}")
        print(f"Legal moves ({len(final_moves)}): {[m.pdn_move for m in final_moves[:10]]}")
        return False


def explore_recursively(board, moves_so_far, max_depth=30):
    """Recursively explore all forcing lines"""
    if max_depth <= 0:
        return None

    legal_moves = list(board.legal_moves())

    # Check for mate
    if not legal_moves:
        if board.turn == 1:  # Black to move - White wins
            return moves_so_far
        else:
            return None

    # If only one move (forced), continue
    if len(legal_moves) == 1:
        move = legal_moves[0]
        test_board = board.copy()
        test_board.push(move)

        return explore_recursively(test_board, moves_so_far + [move.pdn_move], max_depth - 1)

    # Multiple moves - need to check all
    # For White's turn (trying to win)
    if board.turn == 2:
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)

            result = explore_recursively(test_board, moves_so_far + [move.pdn_move], max_depth - 1)
            if result:
                return result
        return None

    # For Black's turn - all moves must lead to White winning
    else:
        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)

            result = explore_recursively(test_board, moves_so_far + [move.pdn_move], max_depth - 1)
            if result is None:
                # Black can avoid mate
                return None

        # All Black moves lead to mate - return one line
        first_move = legal_moves[0]
        test_board = board.copy()
        test_board.push(first_move)
        return explore_recursively(test_board, moves_so_far + [first_move.pdn_move], max_depth - 1)


def main():
    fen = "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"

    print("="*70)
    print("EXERCISE 4 - DEEP EXPLORATION")
    print("="*70)
    print(f"\nFEN: {fen}\n")

    # Start with the promising line: 7-11 (f2-e3)
    print("Exploring: 7-11 (f2-e3)...")
    print("-"*70)

    board = Board(variant="brazilian", fen=fen)

    # Make first move
    for move in board.legal_moves():
        if move.pdn_move == "7-11":
            board.push(move)
            break

    print("\nAfter 1. f2-e3 (7-11):")
    print(board)
    print()

    # Now explore all possibilities from here
    print("Searching for forced win from this position...")
    result = explore_recursively(board, ["7-11"], max_depth=30)

    if result:
        print("\n" + "="*70)
        print("SOLUTION FOUND!")
        print("="*70)
        print()
        print("Move sequence (PDN):")
        print(" → ".join(result))
        print()

        # Verify by replaying
        print("Verifying solution:")
        print("-"*70)
        explore_line(fen, result)
    else:
        print("\nNo forced win found starting with 7-11")


if __name__ == "__main__":
    main()
