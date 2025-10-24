#!/usr/bin/env python3
"""
Improved Brazilian Draughts Solver
Uses alpha-beta pruning with deeper search to find tactical sacrifices
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board
import time


class ImprovedSolver:
    """Improved solver with tactical awareness"""

    def __init__(self):
        self.nodes = 0
        self.best_line = []

    def solve(self, fen, max_depth=10):
        """Find the best winning line"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("IMPROVED BRAZILIAN DRAUGHTS SOLVER")
        print("=" * 70)
        print(f"\nFEN: {fen}")
        print(f"Turn: {'White' if board.turn else 'Black'}\n")
        print(board)
        print()

        self.nodes = 0
        start_time = time.time()

        best_move, best_score, principal_variation = self.search_best_move(
            board, max_depth
        )

        elapsed = time.time() - start_time

        print(f"\nSearch completed:")
        print(f"  Nodes: {self.nodes:,}")
        print(f"  Time: {elapsed:.2f}s")
        print(f"  NPS: {int(self.nodes/elapsed):,}")
        print(f"  Score: {best_score:.2f}")
        print()

        if principal_variation:
            print("Best line found:")
            self.display_line(board, principal_variation)

        return principal_variation

    def search_best_move(self, board, max_depth):
        """Find best move with principal variation"""
        best_move = None
        best_score = float('-inf') if board.turn else float('inf')
        best_pv = []

        legal_moves = list(board.legal_moves())

        for move in legal_moves:
            test_board = board.copy()
            test_board.push(move)

            score, pv = self.alphabeta(
                test_board,
                max_depth - 1,
                float('-inf'),
                float('inf'),
                not board.turn
            )

            if board.turn:  # White maximizing
                if score > best_score:
                    best_score = score
                    best_move = move
                    best_pv = [move] + pv
            else:  # Black minimizing
                if score < best_score:
                    best_score = score
                    best_move = move
                    best_pv = [move] + pv

        return best_move, best_score, best_pv

    def alphabeta(self, board, depth, alpha, beta, maximizing):
        """Alpha-beta search with principal variation"""
        self.nodes += 1

        # Terminal node or depth limit
        legal_moves = list(board.legal_moves())

        if not legal_moves:
            # Game over
            if board.turn:  # White to move but can't
                return -100000, []
            else:  # Black to move but can't
                return 100000, []

        if depth <= 0:
            return self.evaluate(board), []

        best_pv = []

        if maximizing:
            max_eval = float('-inf')
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)
                eval_score, pv = self.alphabeta(test_board, depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_pv = [move] + pv

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff

            return max_eval, best_pv
        else:
            min_eval = float('inf')
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)
                eval_score, pv = self.alphabeta(test_board, depth - 1, alpha, beta, True)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_pv = [move] + pv

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff

            return min_eval, best_pv

    def evaluate(self, board):
        """
        Evaluate position
        Positive = good for White, Negative = good for Black
        """
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
        # Kings are worth more than men
        score = (white_men * 100 + white_kings * 350) - (black_men * 100 + black_kings * 350)

        # Mobility bonus
        mobility = len(list(board.legal_moves()))
        if board.turn:
            score += mobility * 8
        else:
            score -= mobility * 8

        # Bonus for advanced pieces
        # (This would require parsing piece positions, skipping for now)

        return score

    def display_line(self, board, moves):
        """Display the principal variation"""
        temp_board = board.copy()

        algebraic_line = []

        for i, move in enumerate(moves):
            notation = move.pdn_move

            # Convert to algebraic
            parts = notation.replace('x', '-').split('-')
            from_sq = int(parts[0])
            to_sq = int(parts[-1])

            from_alg = self.square_to_alg(from_sq)
            to_alg = self.square_to_alg(to_sq)

            if 'x' in notation:
                alg_move = f"{from_alg}x...x{to_alg}"
            else:
                alg_move = f"{from_alg}-{to_alg}"

            player = "White" if i % 2 == 0 else "Black"
            print(f"  {i+1}. {notation:10} ({alg_move:15}) - {player}")

            algebraic_line.append(alg_move)
            temp_board.push(move)

        print(f"\nFinal position:")
        print(temp_board)

        # Check result
        final_moves = list(temp_board.legal_moves())
        if not final_moves:
            if temp_board.turn:
                print("\n*** WHITE WINS! Black has no legal moves ***")
            else:
                print("\n*** BLACK WINS! White has no legal moves ***")

        return algebraic_line

    def square_to_alg(self, sq):
        """Convert square number to algebraic"""
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
        return mapping.get(sq, f'?{sq}?')


def main():
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("\nExercise 1 - Finding the CORRECT solution")
    print("\nCorrect solution: 1. c3-b4 a5xc3 2. b2xd4xf6xh8")
    print("\nLet's see if the improved solver finds it...\n")

    solver = ImprovedSolver()

    # Try increasing depths
    for depth in [6, 8, 10]:
        print(f"\n{'=' * 70}")
        print(f"SEARCHING WITH DEPTH {depth}")
        print('=' * 70)

        solution = solver.solve(fen, max_depth=depth)

        # Check if we found the right first move (10-13 = c3-b4)
        if solution and solution[0].pdn_move == "10-13":
            print("\n✓ FOUND CORRECT FIRST MOVE: c3-b4 (10-13)")
            print("\nThis is the CORRECT solution!")
            break
        else:
            if solution:
                print(f"\n✗ Found different first move: {solution[0].pdn_move}")
            print("Trying deeper search...")


if __name__ == "__main__":
    main()
