#!/usr/bin/env python3
"""
Simple Brazilian Draughts Position Analyzer
Shows legal moves and allows manual exploration
"""

import sys
try:
    import draughts
except ImportError:
    print("Installing pydraughts library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


def analyze_position(fen: str):
    """Analyze a position and show all legal moves"""
    board = Board(variant="brazilian", fen=fen)

    print("=" * 60)
    print("BRAZILIAN DRAUGHTS POSITION ANALYZER")
    print("=" * 60)
    print(f"\nFEN: {fen}")
    print(f"Turn: {'White' if board.turn else 'Black'}\n")
    print(board)
    print()

    # Show piece counts
    fen_parts = board.fen.split(':')
    white_pieces = []
    black_pieces = []

    for part in fen_parts:
        if part.startswith('W'):
            white_pieces = part[1:].split(',') if len(part) > 1 else []
        elif part.startswith('B'):
            black_pieces = part[1:].split(',') if len(part) > 1 else []

    print(f"White pieces ({len([p for p in white_pieces if p])}): {', '.join(filter(None, white_pieces))}")
    print(f"Black pieces ({len([p for p in black_pieces if p])}): {', '.join(filter(None, black_pieces))}")
    print()

    # Get and display legal moves
    legal_moves = list(board.legal_moves())
    print(f"Legal moves ({len(legal_moves)}):")
    print()

    captures = []
    normal_moves = []

    for move in legal_moves:
        notation = move.pdn_move
        if 'x' in notation:
            captures.append(notation)
        else:
            normal_moves.append(notation)

    if captures:
        print("Captures:")
        for i, move in enumerate(captures, 1):
            print(f"  {i}. {move}")
        print()

    if normal_moves:
        print("Normal moves:")
        for i, move in enumerate(normal_moves, 1):
            print(f"  {i}. {move}")
        print()

    return board, legal_moves


def explore_move(board, move_notation):
    """Make a move and show resulting position"""
    legal_moves = list(board.legal_moves())

    # Find the move
    selected_move = None
    for move in legal_moves:
        if move.pdn_move == move_notation:
            selected_move = move
            break

    if not selected_move:
        print(f"Move {move_notation} is not legal in this position")
        return None

    new_board = board.copy()
    new_board.push(selected_move)

    print(f"\nAfter {move_notation}:")
    print(f"FEN: {new_board.fen}")
    print(new_board)
    print()

    return new_board


def find_best_tactical_move(board, depth=2):
    """
    Find the best tactical move using simple minimax
    Focus on captures and material gain
    """
    legal_moves = list(board.legal_moves())

    if not legal_moves:
        return None, float('-inf') if board.turn else float('inf')

    best_move = None
    best_score = float('-inf') if board.turn else float('inf')

    for move in legal_moves:
        test_board = board.copy()
        test_board.push(move)

        # Quick evaluation
        score = evaluate_position(test_board)

        # If this leads to checkmate, it's the best
        if not list(test_board.legal_moves()):
            if test_board.turn:  # Black to move but can't - White wins
                if board.turn:  # White just moved
                    return move, 10000
            else:  # White to move but can't - Black wins
                if not board.turn:  # Black just moved
                    return move, 10000

        # Deeper search if needed
        if depth > 1:
            _, future_score = find_best_tactical_move(test_board, depth - 1)
            score = future_score

        # Update best move
        if board.turn:  # White (maximizing)
            if score > best_score:
                best_score = score
                best_move = move
        else:  # Black (minimizing)
            if score < best_score:
                best_score = score
                best_move = move

    return best_move, best_score


def evaluate_position(board):
    """Quick position evaluation"""
    fen = board.fen
    parts = fen.split(':')

    white_men = 0
    white_kings = 0
    black_men = 0
    black_kings = 0

    for part in parts:
        if part.startswith('W'):
            pieces = part[1:].split(',') if len(part) > 1 else []
            for piece in pieces:
                if piece and piece[0].isupper():
                    white_kings += 1
                elif piece:
                    white_men += 1
        elif part.startswith('B'):
            pieces = part[1:].split(',') if len(part) > 1 else []
            for piece in pieces:
                if piece and piece[0].isupper():
                    black_kings += 1
                elif piece:
                    black_men += 1

    # Material score
    score = (white_men * 100 + white_kings * 300) - (black_men * 100 + black_kings * 300)

    # Mobility
    mobility = len(list(board.legal_moves()))
    if board.turn:
        score += mobility * 5
    else:
        score -= mobility * 5

    return score


def auto_solve(fen, max_moves=30):
    """Try to automatically solve the position"""
    board = Board(variant="brazilian", fen=fen)
    solution = []

    print("\n" + "=" * 60)
    print("AUTO-SOLVING...")
    print("=" * 60)
    print()

    for move_num in range(1, max_moves + 1):
        best_move, score = find_best_tactical_move(board, depth=2)

        if best_move is None:
            print("No more moves available")
            break

        notation = best_move.pdn_move
        solution.append(notation)

        print(f"Move {move_num}: {notation} (eval: {score:.1f})")

        board.push(best_move)

        # Check if game is over
        if not list(board.legal_moves()):
            if board.turn:  # White to move but can't
                print("\n*** Black wins! White has no legal moves ***")
            else:  # Black to move but can't
                print("\n*** White wins! Black has no legal moves ***")
            break

        # Check for material advantage
        eval_score = evaluate_position(board)
        if abs(eval_score) > 500:  # Significant material advantage
            print(f"\nPosition heavily favors {'White' if eval_score > 0 else 'Black'} (eval: {eval_score})")
            if move_num >= 10:  # Only stop if we've made a decent number of moves
                break

    print()
    print("Solution found:")
    print(" → ".join(solution))
    print()

    return solution


def main():
    # Exercise position
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("\nExercise 1")
    print("Note: The original solution had d2-e3, but there's no piece on d2")
    print()

    # Analyze initial position
    board, moves = analyze_position(fen)

    # Try to auto-solve
    solution = auto_solve(fen, max_moves=50)

    print("\n" + "=" * 60)
    print("FINAL SOLUTION")
    print("=" * 60)
    print()
    print("FEN:", fen)
    print()
    print("Solution:")
    print(" → ".join(solution))
    print()
    print(f"Total moves: {len(solution)}")


if __name__ == "__main__":
    main()
