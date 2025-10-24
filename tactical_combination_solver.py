#!/usr/bin/env python3
"""
Tactical Combination Solver
Focuses on FORCING LINES (mandatory captures) to find combinations faster
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


class TacticalCombinationSolver:
    """
    Solver optimized for TACTICAL COMBINATIONS

    Key features:
    1. Focuses on FORCING LINES (positions with only 1 legal move)
    2. Values Queen promotions extremely high
    3. Recognizes Queen vs pawns as winning
    4. Faster search by following forced sequences
    """

    def __init__(self):
        self.nodes = 0

    def solve(self, fen, max_depth=20):
        """Find tactical combination"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("TACTICAL COMBINATION SOLVER")
        print("=" * 70)
        print(f"\nFEN: {fen}\n")
        print(board)
        print()

        # Evaluate initial position
        initial_eval = self.evaluate(board)
        print(f"Initial eval: {initial_eval:.0f}\n")

        legal_moves = list(board.legal_moves())
        print(f"Testing {len(legal_moves)} first moves:\n")

        best_line = None
        best_eval = float('-inf')

        for first_move in legal_moves:
            self.nodes = 0
            pdn = first_move.pdn_move
            alg = self.pdn_to_alg(pdn)

            print(f"{pdn:8} ({alg:15}) ... ", end='', flush=True)

            board_after = board.copy()
            board_after.push(first_move)

            start = time.time()

            # Follow the forcing line
            line, final_eval = self.follow_forcing_line(board_after, [first_move], max_depth - 1)

            elapsed = time.time() - start

            advantage = final_eval - initial_eval

            if advantage >= 500:  # Decisive advantage!
                print(f"DECISIVE! +{advantage:.0f} ({self.nodes} nodes, {elapsed:.2f}s)")

                if final_eval > best_eval:
                    best_eval = final_eval
                    best_line = line
            else:
                print(f"{final_eval:.0f} (Δ{advantage:+.0f}) ({self.nodes} nodes, {elapsed:.2f}s)")

        if best_line:
            print("\n" + "=" * 70)
            print("COMBINATION FOUND!")
            print("=" * 70)
            print()
            self.display_solution(board, best_line, best_eval)
            return best_line
        else:
            print("\nNo decisive combination found")
            return None

    def follow_forcing_line(self, board, line_so_far, max_depth):
        """
        Follow a FORCING LINE (where moves are forced by captures)
        Returns (complete_line, final_evaluation)
        """
        if max_depth <= 0:
            return line_so_far, self.evaluate(board)

        legal_moves = list(board.legal_moves())
        self.nodes += 1

        # Game over?
        if not legal_moves:
            if board.turn == 1:  # Black has no moves
                return line_so_far, 10000  # White wins
            else:
                return line_so_far, -10000  # Black wins

        # If only ONE legal move (FORCED), continue following
        if len(legal_moves) == 1:
            forced_move = legal_moves[0]
            new_board = board.copy()
            new_board.push(forced_move)

            return self.follow_forcing_line(new_board, line_so_far + [forced_move], max_depth - 1)

        # Multiple moves - need to evaluate each
        if board.turn == 2:  # White's turn - maximize
            best_eval = float('-inf')
            best_line = line_so_far

            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                line, eval_score = self.follow_forcing_line(test_board, line_so_far + [move], max_depth - 1)

                if eval_score > best_eval:
                    best_eval = eval_score
                    best_line = line

            return best_line, best_eval

        else:  # Black's turn - minimize
            best_eval = float('inf')
            best_line = line_so_far

            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                line, eval_score = self.follow_forcing_line(test_board, line_so_far + [move], max_depth - 1)

                if eval_score < best_eval:
                    best_eval = eval_score
                    best_line = line

            return best_line, best_eval

    def evaluate(self, board):
        """Evaluate position with strong emphasis on Queens"""
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

        # Material with proper weights
        score = (white_men * 100 + white_kings * 400) - (black_men * 100 + black_kings * 400)

        # HUGE bonus for Queen vs pawns
        if white_kings > 0 and black_kings == 0:
            score += 600  # Theoretically won!

        if black_kings > 0 and white_kings == 0:
            score -= 600

        # Mobility
        mobility = len(list(board.legal_moves()))
        if board.turn == 2:
            score += mobility * 5
        else:
            score -= mobility * 5

        return score

    def display_solution(self, board, moves, final_eval):
        """Display the solution"""
        temp_board = board.copy()

        print("Tactical combination:")
        print()

        for i, move in enumerate(moves, 1):
            pdn = move.pdn_move
            alg = self.pdn_to_alg(pdn)

            if i % 2 == 1:  # White
                print(f"{(i+1)//2}. {alg:20} ", end='')
            else:  # Black
                print(f"{alg}")

            temp_board.push(move)

        if len(moves) % 2 == 1:
            print()
        print()

        print("Final position:")
        print(temp_board)
        print()

        # Material analysis
        fen_parts = temp_board.fen.split(':')
        for part in fen_parts:
            if part.startswith('W'):
                white_pieces = [p for p in part[1:].replace('.', '').split(',') if p]
                white_men = len([p for p in white_pieces if p and not p[0].isupper()])
                white_kings = len([p for p in white_pieces if p and p[0].isupper()])
                print(f"White: {white_men} pawns, {white_kings} queens")
            elif part.startswith('B'):
                black_pieces = [p for p in part[1:].replace('.', '').split(',') if p]
                black_men = len([p for p in black_pieces if p and not p[0].isupper()])
                black_kings = len([p for p in black_pieces if p and p[0].isupper()])
                print(f"Black: {black_men} pawns, {black_kings} queens")

        print(f"\nFinal evaluation: {final_eval:.0f}")

        if white_kings > 0 and black_kings == 0:
            print("\n✓ WHITE HAS DECISIVE ADVANTAGE (Queen vs pawns)")

        print()
        print("PDN: " + " → ".join([m.pdn_move for m in moves]))

        # Algebraic
        alg_moves = [self.pdn_to_alg(m.pdn_move) for m in moves]
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
        print("\nAlgebraic: " + " ".join(result))

    def pdn_to_alg(self, pdn):
        """Convert PDN to algebraic"""
        if 'x' in pdn:
            parts = pdn.split('x')
            from_sq = int(parts[0])
            to_sq = int(parts[-1])
            from_alg = self.sq_to_alg(from_sq)
            to_alg = self.sq_to_alg(to_sq)
            if len(parts) > 2 or abs(to_sq - from_sq) > 10:
                return f"{from_alg}x...x{to_alg}"
            return f"{from_alg}x{to_alg}"
        else:
            parts = pdn.split('-')
            from_sq = int(parts[0])
            to_sq = int(parts[1])
            return f"{self.sq_to_alg(from_sq)}-{self.sq_to_alg(to_sq)}"

    def sq_to_alg(self, sq):
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
    """Test on Exercises 3 and 4"""

    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
    ]

    print("\n" + "=" * 70)
    print("TACTICAL COMBINATION SOLVER - Exercises 3 & 4")
    print("=" * 70)
    print("\nSearching for forcing lines with decisive advantages...")
    print()

    for number, fen in exercises:
        print(f"\n{'='*70}")
        print(f"EXERCISE {number}")
        print(f"{'='*70}\n")

        solver = TacticalCombinationSolver()
        solution = solver.solve(fen, max_depth=20)

        if solution:
            print(f"\n✓ SOLVED!\n")
        else:
            print(f"\n✗ Not solved\n")


if __name__ == "__main__":
    main()
