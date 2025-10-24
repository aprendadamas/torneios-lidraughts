#!/usr/bin/env python3
"""
Manual deep analysis of exercises 3 and 4
Try to understand what the tactical idea is
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def explore_deeply(number, fen, first_moves_to_try):
    """Manually explore specific move sequences"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number} - MANUAL EXPLORATION")
    print(f"{'='*70}")
    print(f"\nFEN: {fen}\n")

    board = Board(variant="brazilian", fen=fen)
    print(board)
    print()

    for move_sequence in first_moves_to_try:
        print(f"\nTrying sequence: {' → '.join(move_sequence)}")
        print("-" * 70)

        test_board = board.copy()
        all_moves_legal = True

        for i, move_pdn in enumerate(move_sequence):
            # Find and execute the move
            legal_moves = list(test_board.legal_moves())
            found_move = None

            for move in legal_moves:
                if move.pdn_move == move_pdn:
                    found_move = move
                    break

            if not found_move:
                print(f"  ✗ Move {i+1} ({move_pdn}) is NOT legal!")
                print(f"    Legal moves: {[m.pdn_move for m in legal_moves[:5]]}")
                all_moves_legal = False
                break

            # Execute the move
            test_board.push(found_move)
            print(f"  {i+1}. {move_pdn} - OK")

        if all_moves_legal:
            print(f"\n  Final position after {len(move_sequence)} moves:")
            print(test_board)

            # Check if it's mate
            final_moves = list(test_board.legal_moves())
            if not final_moves:
                print(f"\n  *** MATE! {('White' if test_board.turn == 2 else 'Black')} has no moves ***")
            else:
                print(f"\n  Next player has {len(final_moves)} moves: {[m.pdn_move for m in final_moves[:5]]}")


def analyze_all_captures(number, fen):
    """Analyze all possible capture sequences"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number} - ALL CAPTURE SEQUENCES")
    print(f"{'='*70}\n")

    board = Board(variant="brazilian", fen=fen)

    legal_moves = list(board.legal_moves())

    print("Testing each first move and looking for forcing lines:\n")

    for first_move in legal_moves:
        pdn = first_move.pdn_move
        print(f"After {pdn}:")

        test_board = board.copy()
        test_board.push(first_move)

        black_moves = list(test_board.legal_moves())
        black_captures = [m for m in black_moves if 'x' in m.pdn_move]

        # If Black has only one move (forced), continue analyzing
        if len(black_moves) == 1:
            print(f"  Black forced: {black_moves[0].pdn_move}")

            test_board2 = test_board.copy()
            test_board2.push(black_moves[0])

            white_moves2 = list(test_board2.legal_moves())
            print(f"  White then has {len(white_moves2)} moves:")

            # Check for captures
            white_captures2 = [m for m in white_moves2 if 'x' in m.pdn_move]
            if white_captures2:
                print(f"    Captures: {[m.pdn_move for m in white_captures2[:3]]}")

                # Try each white capture
                for white_cap in white_captures2[:3]:
                    test_board3 = test_board2.copy()
                    test_board3.push(white_cap)

                    black_moves3 = list(test_board3.legal_moves())
                    if not black_moves3:
                        print(f"      {white_cap.pdn_move} → MATE!")
                    elif len(black_moves3) == 1:
                        print(f"      {white_cap.pdn_move} → Black forced: {black_moves3[0].pdn_move}")
        else:
            print(f"  Black has {len(black_moves)} moves ({len(black_captures)} captures)")

        print()


def main():
    """Analyze exercises 3 and 4 manually"""

    # Exercise 3
    fen_3 = "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"

    # Try some promising sequences for Ex 3
    sequences_3 = [
        ["13-18", "23x14", "10x19"],  # b4-c5, f6xd4, c3xe5
        ["16-20", "23x16", "13-18"],  # h4-g5, f6xh4, b4-c5
        ["5-9", "14x5"],               # b2-a3, d4xb2
    ]

    analyze_all_captures(3, fen_3)
    explore_deeply(3, fen_3, sequences_3)

    # Exercise 4
    fen_4 = "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"

    sequences_4 = [
        ["16-20", "23x16", "10-13"],  # h4-g5, f6xh4, c3-b4
        ["7-11", "14x7", "2x11"],     # f2-e3, d4xf2, g1xe3
    ]

    analyze_all_captures(4, fen_4)
    explore_deeply(4, fen_4, sequences_4)


if __name__ == "__main__":
    main()
