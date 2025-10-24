#!/usr/bin/env python3
"""
Brazilian Draughts Solver
Uses the pydraughts library to solve draughts problems/exercises
"""

import sys
try:
    import draughts
except ImportError:
    print("Installing pydraughts library...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts"])
    import draughts

from draughts import Board, Move
from typing import List, Tuple, Optional
import time


class BrazilianDraughtsSolver:
    """Solver for Brazilian Draughts positions"""

    def __init__(self):
        self.nodes_searched = 0
        self.max_depth = 40  # Maximum depth for search

    def solve_position(self, fen: str, max_moves: int = 50) -> Optional[List[str]]:
        """
        Solve a Brazilian draughts position
        Returns the solution as a list of moves in algebraic notation
        """
        board = Board(variant="brazilian", fen=fen)

        print(f"\nInicial position:")
        print(f"FEN: {fen}")
        print(f"Turn: {'White' if board.turn else 'Black'}")
        print(board)
        print()

        # Try to find a winning sequence
        solution = self._search_solution(board, max_moves)

        print(f"\nNodes searched: {self.nodes_searched}")

        return solution

    def _search_solution(self, board: Board, max_moves: int) -> Optional[List[str]]:
        """
        Search for a solution using minimax-like approach
        For winning positions, find the sequence that leads to victory
        """
        solution = []
        current_board = board.copy()
        moves_made = 0

        while moves_made < max_moves:
            legal_moves = list(current_board.legal_moves())

            if not legal_moves:
                # No legal moves - game over
                if current_board.turn:  # White to move but can't
                    print("Black wins (White has no moves)")
                    return None
                else:  # Black to move but can't
                    print("White wins (Black has no moves)!")
                    return solution

            # Evaluate each move
            best_move = None
            best_score = float('-inf') if current_board.turn else float('inf')

            for move in legal_moves:
                self.nodes_searched += 1
                test_board = current_board.copy()
                test_board.push(move)

                # Evaluate position after this move
                score = self._evaluate_position(test_board, depth=3)

                if current_board.turn:  # White (maximizing)
                    if score > best_score:
                        best_score = score
                        best_move = move
                else:  # Black (minimizing)
                    if score < best_score:
                        best_score = score
                        best_move = move

            if best_move is None:
                break

            # Make the best move
            move_notation = best_move.pdn_move
            solution.append(move_notation)
            current_board.push(best_move)
            moves_made += 1

            print(f"Move {moves_made}: {move_notation} (score: {best_score:.2f})")

            # Check if game is over
            if current_board.is_over():
                print(f"\nGame over after {moves_made} moves")
                print(f"Result: {current_board.result()}")
                break

        return solution

    def _evaluate_position(self, board: Board, depth: int = 0) -> float:
        """
        Evaluate a position
        Positive = good for White, Negative = good for Black
        """
        if depth <= 0:
            return self._static_evaluation(board)

        legal_moves = list(board.legal_moves())

        # Game over
        if not legal_moves:
            if board.turn:  # White to move but can't - White loses
                return -10000
            else:  # Black to move but can't - White wins
                return 10000

        if board.turn:  # White to move (maximizing)
            max_eval = float('-inf')
            for move in legal_moves:
                self.nodes_searched += 1
                test_board = board.copy()
                test_board.push(move)
                eval_score = self._evaluate_position(test_board, depth - 1)
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:  # Black to move (minimizing)
            min_eval = float('inf')
            for move in legal_moves:
                self.nodes_searched += 1
                test_board = board.copy()
                test_board.push(move)
                eval_score = self._evaluate_position(test_board, depth - 1)
                min_eval = min(min_eval, eval_score)
            return min_eval

    def _static_evaluation(self, board: Board) -> float:
        """
        Static evaluation of position
        Returns a score (positive = good for White)
        """
        # Count pieces
        fen = board.fen

        # Parse FEN to count pieces
        # Format: W:Wa1,b2:Bc3,d4 (White pieces after W, Black after B)
        white_men = 0
        white_kings = 0
        black_men = 0
        black_kings = 0

        parts = fen.split(':')
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

        # Material evaluation
        score = (white_men * 100 + white_kings * 300) - (black_men * 100 + black_kings * 300)

        # Mobility (number of legal moves)
        legal_moves = list(board.legal_moves())
        if board.turn:  # White's turn
            score += len(legal_moves) * 10
        else:  # Black's turn
            score -= len(legal_moves) * 10

        return score


def format_solution(moves: List[str]) -> str:
    """Format solution in the requested format"""
    formatted = []
    for i, move in enumerate(moves):
        # Convert move format if needed
        formatted.append(move)
        if i < len(moves) - 1 and (i + 1) % 2 == 0:
            formatted.append("→")
        elif i < len(moves) - 1:
            formatted.append("→")

    return " ".join(formatted)


def main():
    # Original exercise FEN
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("=" * 60)
    print("BRAZILIAN DRAUGHTS SOLVER")
    print("=" * 60)
    print(f"\nExercise 1")
    print(f"FEN: {fen}")
    print(f"\nNote: The original solution started with d2-e3,")
    print(f"but there is no piece on d2 in the given FEN.")
    print(f"\nFinding correct solution...\n")

    solver = BrazilianDraughtsSolver()

    start_time = time.time()
    solution = solver.solve_position(fen, max_moves=50)
    elapsed = time.time() - start_time

    if solution:
        print("\n" + "=" * 60)
        print("SOLUTION FOUND!")
        print("=" * 60)
        print(f"\nSolution ({len(solution)} moves):")
        print(format_solution(solution))
        print(f"\nTime: {elapsed:.2f} seconds")
        print(f"Nodes searched: {solver.nodes_searched}")
    else:
        print("\n" + "=" * 60)
        print("NO SOLUTION FOUND")
        print("=" * 60)
        print("\nThe position might be:")
        print("- Already won/lost")
        print("- A draw")
        print("- Requires more than 50 moves")


if __name__ == "__main__":
    main()
