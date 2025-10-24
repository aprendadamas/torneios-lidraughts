#!/usr/bin/env python3
"""
Solve Exercise 11 - Tactical Combination Finder
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

    score = (white_men * 100 + white_kings * 400) - (black_men * 100 + black_kings * 400)

    if white_kings > 0 and black_kings == 0:
        score += 500

    legal_moves = list(board.legal_moves())
    if not legal_moves:
        if board.turn == 1:  # Black to move - White wins
            score = 10000

    return score, (white_men, white_kings, black_men, black_kings)


def find_best_combinations(fen, max_depth=7):
    """Find combinations with optimized search"""
    board = Board(variant="brazilian", fen=fen)

    print(f"Searching sequences up to {max_depth} moves (optimized)...")

    combinations = []
    nodes_searched = 0
    max_nodes = 500000  # Limit total nodes

    def search(board, moves_so_far, depth):
        nonlocal nodes_searched

        nodes_searched += 1
        if nodes_searched > max_nodes:
            return

        if nodes_searched % 50000 == 0:
            print(f"  Searched {nodes_searched} nodes, found {len(combinations)} combinations...")

        if depth == 0:
            score, material = evaluate_position(board)
            if score >= 500:
                combinations.append((score, moves_so_far[:], material))
            return

        legal_moves = list(board.legal_moves())

        if not legal_moves:
            score, material = evaluate_position(board)
            if score >= 500:
                combinations.append((score, moves_so_far[:], material))
            return

        # Prioritize captures
        captures = [m for m in legal_moves if 'x' in m.pdn_move]
        non_captures = [m for m in legal_moves if 'x' not in m.pdn_move]

        # If there are captures, only search those
        moves_to_search = captures if captures else non_captures

        # Forced moves - search deeper
        if len(moves_to_search) == 1:
            test_board = board.copy()
            test_board.push(moves_to_search[0])
            search(test_board, moves_so_far + [moves_to_search[0].pdn_move], depth - 1)
        else:
            # Multiple moves - search all
            for move in moves_to_search:
                test_board = board.copy()
                test_board.push(move)
                search(test_board, moves_so_far + [move.pdn_move], depth - 1)

    search(board, [], max_depth)

    combinations.sort(key=lambda x: x[0], reverse=True)
    print(f"  Total nodes searched: {nodes_searched}")

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

    legal_moves = list(board.legal_moves())
    if not legal_moves:
        if board.turn == 1:
            print("\n*** CHECKMATE! Black has no legal moves ***")

    return board


def pdn_to_algebraic(move_pdn):
    """Convert PDN to algebraic"""
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
    fen = "W:We1,d2,a3,c3,f4:Ba5,c5,d6,e7,g7"

    print("=" * 70)
    print("EXERCISE 11")
    print("=" * 70)
    print(f"FEN: {fen}\n")

    # Display initial position
    board = Board(variant="brazilian", fen=fen)
    print("Initial position:")
    print(board)
    print()

    # Try with depth 7 first (optimized search)
    combinations = find_best_combinations(fen, max_depth=7)

    if not combinations:
        print("\nNo decisive combinations found at depth 7!")
        print("Trying depth 9...")
        combinations = find_best_combinations(fen, max_depth=9)

    if not combinations:
        print("\nNo decisive combinations found!")
        return

    print(f"\nFound {len(combinations)} decisive combinations.")
    print(f"\nTop 10 best combinations (by evaluation):\n")

    for i, (score, moves, material) in enumerate(combinations[:10], 1):
        mate_marker = " [MATE]" if score == 10000 else ""
        print(f"{i}. Score: {score}{mate_marker} | Material: W{material[0]}+{material[1]}Q vs B{material[2]}+{material[3]}Q")
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
            mate_suffix = "#" if best_score == 10000 else ""
            result.append(f"{move_num}. {white_move}{mate_suffix}")
        move_num += 1

    print("\nAlgebraic notation:")
    print(" ".join(result))
    print()


if __name__ == "__main__":
    main()
