#!/usr/bin/env python3
"""Analyze exercises 3 and 4 in detail"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def analyze_position(number, fen):
    """Detailed analysis of a position"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number} - DETAILED ANALYSIS")
    print(f"{'='*70}")
    print(f"\nFEN: {fen}\n")

    board = Board(variant="brazilian", fen=fen)
    print(board)
    print()

    # Count pieces
    parts = fen.split(':')
    white_pieces = []
    black_pieces = []

    for part in parts:
        if part.startswith('W'):
            piece_str = part[1:].replace('.', '')
            white_pieces = [p for p in piece_str.split(',') if p]
        elif part.startswith('B'):
            piece_str = part[1:].replace('.', '')
            black_pieces = [p for p in piece_str.split(',') if p]

    white_men = len([p for p in white_pieces if p and not p[0].isupper()])
    white_kings = len([p for p in white_pieces if p and p[0].isupper()])
    black_men = len([p for p in black_pieces if p and not p[0].isupper()])
    black_kings = len([p for p in black_pieces if p and p[0].isupper()])

    print("Material count:")
    print(f"  White: {white_men} men, {white_kings} kings (total: {white_men + white_kings})")
    print(f"  Black: {black_men} men, {black_kings} kings (total: {black_men + black_kings})")
    print()

    # List all pieces
    print(f"White pieces: {', '.join(white_pieces)}")
    print(f"Black pieces: {', '.join(black_pieces)}")
    print()

    # Legal moves
    legal_moves = list(board.legal_moves())
    print(f"White has {len(legal_moves)} legal moves:")

    captures = [m for m in legal_moves if 'x' in m.pdn_move]
    regular = [m for m in legal_moves if 'x' not in m.pdn_move]

    if captures:
        print(f"\n  Captures ({len(captures)}):")
        for move in captures[:10]:
            print(f"    • {move.pdn_move}")
        if len(captures) > 10:
            print(f"    ... and {len(captures) - 10} more")

    if regular:
        print(f"\n  Regular moves ({len(regular)}):")
        for move in regular[:10]:
            print(f"    • {move.pdn_move}")
        if len(regular) > 10:
            print(f"    ... and {len(regular) - 10} more")

    # Try each move and see what happens
    print("\n" + "="*70)
    print("EXPLORING FIRST MOVES")
    print("="*70 + "\n")

    for i, move in enumerate(legal_moves[:5], 1):
        pdn = move.pdn_move
        print(f"{i}. {pdn}:")

        test_board = board.copy()
        test_board.push(move)

        black_moves = list(test_board.legal_moves())
        black_captures = [m for m in black_moves if 'x' in m.pdn_move]

        print(f"   → Black has {len(black_moves)} moves ({len(black_captures)} captures)")

        # Check if any Black response leads to immediate White mate
        for black_move in black_moves[:3]:
            test_board2 = test_board.copy()
            test_board2.push(black_move)

            white_moves2 = list(test_board2.legal_moves())
            white_captures2 = [m for m in white_moves2 if 'x' in m.pdn_move]

            if not white_moves2:
                print(f"      {black_move.pdn_move} → White has no moves (Black wins!)")
            else:
                # Check if any White move wins immediately
                for white_move2 in white_moves2[:3]:
                    test_board3 = test_board2.copy()
                    test_board3.push(white_move2)

                    final_moves = list(test_board3.legal_moves())
                    if not final_moves:
                        print(f"      {black_move.pdn_move} → {white_move2.pdn_move} → MATE!")

    print()


def main():
    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
    ]

    for number, fen in exercises:
        analyze_position(number, fen)


if __name__ == "__main__":
    main()
