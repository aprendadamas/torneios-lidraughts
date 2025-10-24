#!/usr/bin/env python3
"""Verify the solution for Exercise 3"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def verify_solution_3():
    """Verify Exercise 3 solution"""
    fen = "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"

    # Solution in algebraic notation:
    # 1. b4-c5 d4xb6 2. h4-g5 f6xh4 3. c3-b4 a5xc3 4. b2xd4xf6xh8

    # Convert to PDN:
    # b4=13, c5=18, d4=14, b6=21
    # h4=16, g5=20, f6=23, h4=16
    # c3=10, b4=13, a5=17, c3=10
    # b2=5, d4=14, f6=23, h8=32

    solution_pdn = [
        "13-18",  # b4-c5
        "14x21",  # d4xb6
        "16-20",  # h4-g5
        "23x16",  # f6xh4
        "10-13",  # c3-b4
        "17x10",  # a5xc3
        "5x32",   # b2xd4xf6xh8 (triple capture!)
    ]

    print("="*70)
    print("EXERCISE 3 - VERIFYING SOLUTION")
    print("="*70)
    print(f"\nFEN: {fen}")
    print("\nSolution (algebraic):")
    print("1. b4-c5 d4xb6")
    print("2. h4-g5 f6xh4")
    print("3. c3-b4 a5xc3")
    print("4. b2xd4xf6xh8#")
    print()
    print("Solution (PDN):")
    print(" → ".join(solution_pdn))
    print()
    print("-"*70)
    print()

    board = Board(variant="brazilian", fen=fen)

    print("Initial position:")
    print(board)
    print()

    for i, move_pdn in enumerate(solution_pdn, 1):
        # Find the move
        legal_moves = list(board.legal_moves())
        found_move = None

        for move in legal_moves:
            if move.pdn_move == move_pdn:
                found_move = move
                break

        if not found_move:
            print(f"✗ ERROR: Move {i} ({move_pdn}) is NOT legal!")
            print(f"Legal moves: {[m.pdn_move for m in legal_moves]}")
            return False

        # Execute move
        board.push(found_move)

        player = "White" if i % 2 == 1 else "Black"
        print(f"{i}. {move_pdn} ({player})")

        if i % 2 == 0:  # After Black's move, show position
            print()
            print(f"After move {i//2}:")
            print(board)
            print()

    print("="*70)
    print("FINAL POSITION")
    print("="*70)
    print()
    print(board)
    print()

    # Check if it's mate
    final_moves = list(board.legal_moves())
    if not final_moves:
        print("*** CHECKMATE! Black has no legal moves ***")
        print(f"Turn: {board.turn} (1=Black, 2=White)")
        return True
    else:
        print(f"⚠ Not mate! Black has {len(final_moves)} legal moves:")
        for m in final_moves[:5]:
            print(f"  - {m.pdn_move}")
        return False


def analyze_why_solver_failed():
    """Analyze why the solver didn't find this"""
    print("\n" + "="*70)
    print("ANALYSIS: WHY THE SOLVER FAILED")
    print("="*70)
    print()
    print("The solution requires a TRIPLE SACRIFICE:")
    print()
    print("1. b4-c5  - FIRST SACRIFICE (sacrificing b4)")
    print("2. h4-g5  - SECOND SACRIFICE (sacrificing h4)")
    print("3. c3-b4  - THIRD SACRIFICE (sacrificing c3)")
    print("4. b2xd4xf6xh8# - TRIPLE CAPTURE with promotion to Queen")
    print()
    print("This is EXACTLY the same pattern as:")
    print("  • Exercise 1: 1 sacrifice + triple capture = Mate in 2")
    print("  • Exercise 2: 2 sacrifices + triple capture = Mate in 5")
    print("  • Exercise 3: 3 sacrifices + triple capture = Mate in 4")
    print()
    print("Why didn't the solver find it?")
    print()
    print("The solver stopped at move 1 (13-18) because it saw:")
    print("  - Black forced to capture: 14x21")
    print("  - But then didn't search deep enough to see the")
    print("    subsequent sacrifices and final triple capture.")
    print()
    print("The search depth needed:")
    print("  - 7 half-moves (plies) for Black to have no moves")
    print("  - Each sacrifice creates a forcing line")
    print("  - But the search terminated too early")
    print()
    print("LESSON: Need to search ALL forcing lines deeply,")
    print("not just stop at the first capture response!")


if __name__ == "__main__":
    result = verify_solution_3()

    if result:
        print("\n✓ SOLUTION VERIFIED!")
        analyze_why_solver_failed()
    else:
        print("\n✗ SOLUTION INVALID")
