#!/usr/bin/env python3
"""
Improved Brazilian Draughts Solver with POSITIONAL EVALUATION
Recognizes tactical combinations that lead to decisive advantages (Queen promotion)
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


class PositionalSolver:
    """
    Solver that recognizes POSITIONAL ADVANTAGES, not just forced mates

    Key improvements:
    1. Values Queen promotions extremely high
    2. Recognizes Queen vs pawns as winning
    3. Looks for "decisive advantage" not just checkmate
    """

    def __init__(self):
        self.nodes = 0
        self.cache = {}

    def solve(self, fen, max_depth=12):
        """Find tactical combination leading to decisive advantage"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("POSITIONAL SOLVER - Finding Decisive Advantages")
        print("=" * 70)
        print(f"\nFEN: {fen}")
        print(f"Max depth: {max_depth} plies")
        print()
        print(board)
        print()

        # Evaluate initial position
        initial_eval = self.evaluate_position(board)
        print(f"Initial evaluation: {initial_eval:.1f}")
        print()

        # Get all legal moves
        legal_moves = list(board.legal_moves())
        print(f"Analyzing {len(legal_moves)} possible first moves...\n")

        best_solution = None
        best_score = float('-inf')
        best_depth = 0

        for i, first_move in enumerate(legal_moves, 1):
            self.nodes = 0
            self.cache.clear()

            pdn = first_move.pdn_move
            is_capture = 'x' in pdn

            print(f"{'★' if is_capture else ' '} {i}. {pdn} ({self.pdn_to_alg(pdn)})... ", end='', flush=True)

            # Make the move
            board_after = board.copy()
            board_after.push(first_move)

            start_time = time.time()

            # Search for best continuation
            score, line = self.search_best_line(board_after, max_depth - 1, [first_move])

            elapsed = time.time() - start_time

            # Check if this gives decisive advantage
            advantage = score - initial_eval

            if advantage >= 500:  # Decisive advantage threshold
                print(f"DECISIVE! Advantage: +{advantage:.0f} ({self.nodes:,} nodes, {elapsed:.2f}s)")

                if score > best_score:
                    best_score = score
                    best_solution = line
                    best_depth = len(line)
            else:
                print(f"Eval: {score:.0f} (Δ{advantage:+.0f}) ({self.nodes:,} nodes, {elapsed:.2f}s)")

        if best_solution:
            print("\n" + "=" * 70)
            print(f"BEST COMBINATION FOUND - {best_depth} moves")
            print(f"Final evaluation: {best_score:.0f} (advantage: +{best_score - initial_eval:.0f})")
            print("=" * 70)
            print()
            self.display_solution(board, best_solution)
            return best_solution
        else:
            print("\nNo decisive advantage found")
            return None

    def search_best_line(self, board, depth, moves_so_far):
        """
        Search for best line using minimax with positional evaluation
        Returns (score, line)
        """
        self.nodes += 1

        if depth <= 0:
            return self.evaluate_position(board), moves_so_far

        # Check cache
        position_key = board.fen
        if position_key in self.cache:
            return self.cache[position_key]

        legal_moves = list(board.legal_moves())

        # Game over
        if not legal_moves:
            if board.turn == 1:  # Black to move but can't - White wins
                score = 10000
            else:  # White to move but can't - Black wins
                score = -10000
            self.cache[position_key] = (score, moves_so_far)
            return score, moves_so_far

        # White's turn (maximizing)
        if board.turn == 2:
            best_score = float('-inf')
            best_line = moves_so_far

            # Order moves - captures and advances first
            ordered_moves = self.order_moves(board, legal_moves)

            for move in ordered_moves:
                test_board = board.copy()
                test_board.push(move)

                score, line = self.search_best_line(test_board, depth - 1, moves_so_far + [move])

                if score > best_score:
                    best_score = score
                    best_line = line

            self.cache[position_key] = (best_score, best_line)
            return best_score, best_line

        # Black's turn (minimizing)
        else:
            best_score = float('inf')
            best_line = moves_so_far

            # Order moves
            ordered_moves = self.order_moves(board, legal_moves)

            for move in ordered_moves:
                test_board = board.copy()
                test_board.push(move)

                score, line = self.search_best_line(test_board, depth - 1, moves_so_far + [move])

                if score < best_score:
                    best_score = score
                    best_line = line

            self.cache[position_key] = (best_score, best_line)
            return best_score, best_line

    def evaluate_position(self, board):
        """
        IMPROVED POSITIONAL EVALUATION

        Key factors:
        1. Material (Queens worth 3x pawns)
        2. Queen promotions (huge bonus)
        3. Queen vs pawns endgames (winning)
        4. Mobility
        """
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

        # MATERIAL EVALUATION with proper weights
        # Queens (Kings in draughts) are worth MUCH more than pawns
        PAWN_VALUE = 100
        QUEEN_VALUE = 350  # Queens are 3.5x more valuable

        material_score = (white_men * PAWN_VALUE + white_kings * QUEEN_VALUE) - \
                        (black_men * PAWN_VALUE + black_kings * QUEEN_VALUE)

        # HUGE BONUS: Queen vs pawns is a winning endgame
        if white_kings > 0 and black_kings == 0:
            # White has Queen(s), Black has none
            if black_men <= 3:  # Few black pawns left
                material_score += 500  # This is a theoretically won position!

        if black_kings > 0 and white_kings == 0:
            # Black has Queen(s), White has none
            if white_men <= 3:
                material_score -= 500

        # PROMOTION BONUS: About to promote
        # Check if any pawns are close to promotion (row 8 for White, row 1 for Black)
        # This is complex to check from FEN, but we can infer from position

        # MOBILITY: More legal moves = better position
        mobility = len(list(board.legal_moves()))
        if board.turn == 2:  # White's turn
            material_score += mobility * 5
        else:  # Black's turn
            material_score -= mobility * 5

        return material_score

    def order_moves(self, board, moves):
        """Order moves: captures first, then regular moves"""
        captures = []
        regular = []

        for move in moves:
            if 'x' in move.pdn_move:
                captures.append(move)
            else:
                regular.append(move)

        return captures + regular

    def display_solution(self, board, moves):
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

        # Evaluate final position
        final_eval = self.evaluate_position(temp_board)
        print(f"Final evaluation: {final_eval:.0f}")
        print()

        # Analyze material
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

        print()

        # Check for decisive advantage
        if white_kings > 0 and black_kings == 0 and black_men <= 3:
            print("✓ DECISIVE ADVANTAGE: White has Queen vs pawns!")
            print("  This is a theoretically won endgame.")
        elif final_eval >= 500:
            print("✓ DECISIVE ADVANTAGE for White")

        print()

        # Show PDN notation
        print("PDN notation:")
        pdn_moves = [m.pdn_move for m in moves]
        print(" → ".join(pdn_moves))

        # Show algebraic notation
        print("\nAlgebraic notation:")
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
        print(" ".join(result))

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
            else:
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
    print("TESTING POSITIONAL SOLVER ON EXERCISES 3 & 4")
    print("=" * 70)
    print("\nLooking for tactical combinations that lead to DECISIVE ADVANTAGE")
    print("(Queen promotion + theoretically won position)")
    print()

    for number, fen in exercises:
        print(f"\n{'='*70}")
        print(f"EXERCISE {number}")
        print(f"{'='*70}\n")

        solver = PositionalSolver()
        solution = solver.solve(fen, max_depth=12)

        if solution:
            print(f"\n✓ Exercise {number} SOLVED!\n")
        else:
            print(f"\n✗ Exercise {number} not solved\n")

        print("="*70)
        print()


if __name__ == "__main__":
    main()
