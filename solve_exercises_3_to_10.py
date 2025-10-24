#!/usr/bin/env python3
"""Solve Exercises 3 to 10"""

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


def solve_exercise(number, fen):
    """Solve a single exercise and return algebraic notation"""
    print(f"\n{'='*70}")
    print(f"EXERCISE {number}")
    print(f"{'='*70}")
    print(f"FEN: {fen}")

    solver = TacticalSolver()
    solution = solver.solve(fen)

    if solution:
        # Convert to algebraic notation
        algebraic_moves = []
        for i, move in enumerate(solution):
            pdn = move.pdn_move
            alg = solver.pdn_to_alg(pdn)
            algebraic_moves.append(alg)

        # Format as moves
        result = []
        move_num = 1
        for i in range(0, len(algebraic_moves), 2):
            white_move = algebraic_moves[i]
            if i + 1 < len(algebraic_moves):
                black_move = algebraic_moves[i + 1]
                result.append(f"{move_num}. {white_move} {black_move}")
            else:
                result.append(f"{move_num}. {white_move}#")
            move_num += 1

        solution_str = " ".join(result)
        return solution_str
    else:
        return "NO SOLUTION FOUND"


def main():
    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
        (5, "W:We1,f2:Bb4,f4,b6,d6"),
        (6, "W:We1,f2:Bd4,f4,b6,d6"),
        (7, "W:We1,f2,h4:Bd4,b6,d6,h6"),
        (8, "W:We1,f2,h4,h6:Bd4,b6,d6,f8"),
        (9, "W:We1,d2,f2,h4,h6:Bb2,b6,d6,f8"),
        (10, "W:We1,d2,a3,c3:Ba5,c5,e7,g7"),
    ]

    print("\n" + "="*70)
    print("SOLVING EXERCISES 3 TO 10")
    print("="*70)

    results = {}
    for number, fen in exercises:
        solution = solve_exercise(number, fen)
        results[number] = solution

    print("\n\n" + "="*70)
    print("FINAL RESULTS - ALGEBRAIC NOTATION ONLY")
    print("="*70 + "\n")

    for number in sorted(results.keys()):
        print(f"Exercise {number}:")
        print(f"  {results[number]}")
        print()


if __name__ == "__main__":
    main()
