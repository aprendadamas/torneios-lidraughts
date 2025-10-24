#!/usr/bin/env python3
"""
Analyze exercises 3 and 4 for MATERIAL GAIN instead of mate
Maybe these are not mate problems but tactical wins
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def count_material(board):
    """Count material on the board"""
    fen = board.fen
    parts = fen.split(':')

    white_count = 0
    black_count = 0

    for part in parts:
        if part.startswith('W'):
            pieces = part[1:].replace('.', '').split(',')
            white_count = len([p for p in pieces if p])
        elif part.startswith('B'):
            pieces = part[1:].replace('.', '').split(',')
            black_count = len([p for p in pieces if p])

    return white_count, black_count


def analyze_for_material_win(number, fen):
    """Analyze for forced material gain"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number} - MATERIAL GAIN ANALYSIS")
    print(f"{'='*70}")
    print(f"\nFEN: {fen}\n")

    board = Board(variant="brazilian", fen=fen)
    print(board)

    initial_white, initial_black = count_material(board)
    print(f"\nInitial material: White {initial_white} vs Black {initial_black}")
    print()

    legal_moves = list(board.legal_moves())

    print("Testing each first move for material gain:\n")

    best_gain = -999
    best_line = None

    for first_move in legal_moves:
        pdn = first_move.pdn_move

        test_board = board.copy()
        test_board.push(first_move)

        black_moves = list(test_board.legal_moves())

        # If Black has only one move (forced)
        if len(black_moves) == 1:
            test_board2 = test_board.copy()
            test_board2.push(black_moves[0])

            white_moves2 = list(test_board2.legal_moves())

            # Try each white response
            for white_move2 in white_moves2:
                test_board3 = test_board2.copy()
                test_board3.push(white_move2)

                white_count, black_count = count_material(test_board3)
                material_gain = (white_count - black_count) - (initial_white - initial_black)

                if material_gain > best_gain:
                    best_gain = material_gain
                    best_line = [pdn, black_moves[0].pdn_move, white_move2.pdn_move]

                if material_gain > 0:
                    print(f"{pdn} → {black_moves[0].pdn_move} → {white_move2.pdn_move}")
                    print(f"  Material: W{white_count} vs B{black_count} (gain: +{material_gain})")

    if best_line:
        print(f"\nBest material gain: +{best_gain}")
        print(f"Line: {' → '.join(best_line)}")

        # Verify the line
        print("\nVerifying best line:")
        print("-"*70)
        board2 = Board(variant="brazilian", fen=fen)

        for i, move_pdn in enumerate(best_line, 1):
            legal = list(board2.legal_moves())
            found = None
            for m in legal:
                if m.pdn_move == move_pdn:
                    found = m
                    break

            if found:
                board2.push(found)
                print(f"{i}. {move_pdn}")

        print()
        print(board2)

        white_final, black_final = count_material(board2)
        print(f"\nFinal material: White {white_final} vs Black {black_final}")

        # Continue analyzing
        final_moves = list(board2.legal_moves())
        print(f"Next to move: {'White' if board2.turn == 2 else 'Black'}")
        print(f"Legal moves: {len(final_moves)}")

        if len(final_moves) <= 5:
            print(f"Moves: {[m.pdn_move for m in final_moves]}")


def main():
    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
    ]

    print("\n" + "="*70)
    print("HYPOTHESIS: Exercises 3 & 4 are MATERIAL WIN problems")
    print("="*70)
    print("\nLooking for forced material gain, not necessarily mate...")

    for number, fen in exercises:
        analyze_for_material_win(number, fen)


if __name__ == "__main__":
    main()
