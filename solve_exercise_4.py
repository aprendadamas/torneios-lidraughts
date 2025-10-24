#!/usr/bin/env python3
"""
Solve Exercise 4 - Tactical Combination Finder
Searches for combinations leading to Queen promotions
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def evaluate_position(board):
    """Evaluate final position quality"""
    fen = board.fen
    parts = fen.split(':')

    white_men = 0
    white_kings = 0
    black_men = 0
    black_kings = 0

    for part in parts:
        if part.startswith('W'):
            pieces = part[1:].replace('.', '').split(',')
            for piece in pieces:
                if piece and piece[0].isupper():
                    white_kings += 1
                elif piece:
                    white_men += 1
        elif part.startswith('B'):
            pieces = part[1:].replace('.', '').split(',')
            for piece in pieces:
                if piece and piece[0].isupper():
                    black_kings += 1
                elif piece:
                    black_men += 1

    # Score: Fewer black pieces = better
    # More white pieces = better
    # Queens worth much more
    score = (white_men * 100 + white_kings * 400) - (black_men * 100 + black_kings * 400)

    # Bonus for Queen vs pawns
    if white_kings > 0 and black_kings == 0:
        score += 500

    return score, (white_men, white_kings, black_men, black_kings)


def find_best_combinations(fen, target_depth=9):
    """Find and rank all combinations"""
    board = Board(variant="brazilian", fen=fen)

    print(f"Searching sequences up to {target_depth} moves...")

    combinations = []

    def search(board, moves_so_far, depth):
        if depth == 0:
            # Evaluate this position
            score, material = evaluate_position(board)

            # Check if we gained a Queen
            if material[1] > 0 and material[3] == 0:  # White has Queen, Black doesn't
                combinations.append((score, moves_so_far[:], material))
            return

        legal_moves = list(board.legal_moves())

        if not legal_moves:
            return

        # If forced, always follow
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

    search(board, [], target_depth)

    # Sort by score (best first)
    combinations.sort(key=lambda x: x[0], reverse=True)

    return combinations


def display_combination(fen, moves_pdn):
    """Display and verify a combination"""
    board = Board(variant="brazilian", fen=fen)

    for j, move_pdn in enumerate(moves_pdn, 1):
        for move in board.legal_moves():
            if move.pdn_move == move_pdn:
                board.push(move)
                player = "White" if j % 2 == 1 else "Black"
                print(f"{j}. {move_pdn} ({player})")
                break

    print()
    print(board)
    print()

    score, material = evaluate_position(board)
    print(f"Material: W:{material[0]}men+{material[1]}queens vs B:{material[2]}men+{material[3]}queens")
    print(f"Evaluation: {score}")

    return board


def pdn_to_algebraic(move_pdn):
    """Convert PDN to algebraic (simple)"""
    mapping = {
        1: 'a1', 2: 'c1', 3: 'e1', 4: 'g1',
        5: 'b2', 6: 'd2', 7: 'f2', 8: 'h2',
        9: 'a3', 10: 'c3', 11: 'e3', 12: 'g3',
        13: 'b4', 14: 'd4', 15: 'f4', 16: 'h4',
        17: 'a5', 18: 'c5', 19: 'e5', 20: 'g5',
        21: 'b6', 22: 'd6', 23: 'f6', 24: 'h6',
        25: 'a7', 26: 'c7', 27: 'e7', 28: 'g7',
        29: 'b8', 30: 'd8', 31: 'f8', 32: 'h8',
    }

    if 'x' in move_pdn:
        parts = move_pdn.split('x')
        from_sq = int(parts[0])
        to_sq = int(parts[-1])
        if len(parts) > 2 or abs(to_sq - from_sq) > 10:
            return f"{mapping[from_sq]}x...x{mapping[to_sq]}"
        return f"{mapping[from_sq]}x{mapping[to_sq]}"
    else:
        parts = move_pdn.split('-')
        from_sq = int(parts[0])
        to_sq = int(parts[1])
        return f"{mapping[from_sq]}-{mapping[to_sq]}"


def main():
    fen = "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"
    depth = 9

    print("=" * 70)
    print("EXERCISE 4")
    print("=" * 70)
    print(f"FEN: {fen}\n")

    # Find all combinations
    combinations = find_best_combinations(fen, depth)

    print(f"\nFound {len(combinations)} combinations.")
    print(f"\nTop 10 best combinations (by evaluation):\n")

    for i, (score, moves, material) in enumerate(combinations[:10], 1):
        print(f"{i}. Score: {score} | Material: W{material[0]}+{material[1]}Q vs B{material[2]}+{material[3]}Q")
        print(f"   {' → '.join(moves)}")

    # Show best solution
    print("\n" + "=" * 70)
    print("BEST SOLUTION")
    print("=" * 70)

    best_score, best_moves, best_material = combinations[0]

    print()
    display_combination(fen, best_moves)

    # Convert to algebraic
    alg_moves = [pdn_to_algebraic(m) for m in best_moves]
    result = []
    move_num = 1
    for i in range(0, len(alg_moves), 2):
        white_move = alg_moves[i]
        if i + 1 < len(alg_moves):
            black_move = alg_moves[i + 1]
            result.append(f"{move_num}. {white_move} {black_move}")
        else:
            result.append(f"{move_num}. {white_move}")
        move_num += 1

    print("\nAlgebraic notation:")
    print(" ".join(result))
    print()


if __name__ == "__main__":
    main()
