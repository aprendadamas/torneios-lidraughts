#!/usr/bin/env python3
"""
Deep Search Solver for difficult positions
Optimized for exercises 3 and 4
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


class DeepSearchSolver:
    """Solver with deep search, alpha-beta pruning, and move ordering"""

    def __init__(self):
        self.nodes = 0
        self.cache = {}  # Position cache for transposition table
        self.max_nodes = 1000000  # Safety limit

    def solve(self, fen, max_depth=20):
        """Find forced mate with deep search"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("DEEP SEARCH SOLVER")
        print("=" * 70)
        print(f"\nFEN: {fen}")
        print(f"Max depth: {max_depth}")
        print()
        print(board)
        print()

        # Get all legal moves and order them (captures first)
        legal_moves = self.order_moves(board, list(board.legal_moves()))

        print(f"Analyzing {len(legal_moves)} first moves (captures prioritized)...\n")

        best_solution = None
        shortest_mate = 999

        for i, first_move in enumerate(legal_moves, 1):
            self.nodes = 0
            self.cache.clear()

            pdn = first_move.pdn_move
            is_capture = 'x' in pdn
            capture_mark = "★" if is_capture else " "

            print(f"{capture_mark} {i}. {pdn} ({self.pdn_to_alg(pdn)})... ", end='', flush=True)

            # Make the move
            board_after = board.copy()
            board_after.push(first_move)

            start_time = time.time()

            # Search for forced mate with iterative deepening
            result = None
            for depth in range(2, max_depth + 1, 2):
                result = self.find_forced_win(board_after, depth, [first_move])

                if result:
                    elapsed = time.time() - start_time
                    mate_length = len(result)
                    print(f"MATE IN {(mate_length+1)//2}! ({self.nodes:,} nodes, {elapsed:.2f}s)")

                    if mate_length < shortest_mate:
                        shortest_mate = mate_length
                        best_solution = result
                    break

                if self.nodes > self.max_nodes:
                    print(f"node limit reached ({self.nodes:,} nodes)")
                    break

            if not result:
                elapsed = time.time() - start_time
                print(f"no mate ({self.nodes:,} nodes, {elapsed:.2f}s)")

        if best_solution:
            print("\n" + "=" * 70)
            print(f"BEST SOLUTION FOUND - Mate in {(shortest_mate+1)//2}")
            print("=" * 70)
            print()
            self.display_solution(board, best_solution)
            return best_solution
        else:
            print("\nNo forced win found")
            return None

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

    def find_forced_win(self, board, max_depth, moves):
        """Recursively find forced win with alpha-beta pruning"""
        self.nodes += 1

        if self.nodes > self.max_nodes:
            return None

        if max_depth <= 0:
            return None

        # Check transposition table
        position_key = board.fen
        if position_key in self.cache:
            return self.cache[position_key]

        legal_moves = list(board.legal_moves())

        # Game over check
        if not legal_moves:
            if board.turn == 1:  # Black to move but can't - White wins
                self.cache[position_key] = moves
                return moves
            else:
                self.cache[position_key] = None
                return None

        # White's turn
        if board.turn == 2:
            # Order moves - try captures first
            ordered_moves = self.order_moves(board, legal_moves)

            for move in ordered_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.find_forced_win(test_board, max_depth - 1, moves + [move])
                if result:
                    self.cache[position_key] = result
                    return result

            self.cache[position_key] = None
            return None

        # Black's turn - all moves must lead to White winning
        else:
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.find_forced_win(test_board, max_depth - 1, moves + [move])
                if result is None:
                    # Black can avoid mate
                    self.cache[position_key] = None
                    return None

            # All Black moves lead to White winning
            first_black_move = legal_moves[0]
            test_board = board.copy()
            test_board.push(first_black_move)

            result = self.find_forced_win(test_board, max_depth - 1, moves + [first_black_move])
            self.cache[position_key] = result
            return result

    def display_solution(self, board, moves):
        """Display the solution"""
        temp_board = board.copy()

        print("Solution:")
        print()

        move_num = 1
        for i, move in enumerate(moves):
            pdn = move.pdn_move
            alg = self.pdn_to_alg(pdn)

            if i % 2 == 0:  # White
                print(f"{move_num}. {alg:20} ", end='')
            else:  # Black
                print(f"{alg}")
                move_num += 1

            temp_board.push(move)

        if len(moves) % 2 == 1:
            print("#")
        print()

        print("Final position:")
        print(temp_board)
        print()

        # Verify
        final_moves = list(temp_board.legal_moves())
        if not final_moves:
            print("✓ Verified: Black has no legal moves (checkmate)")
        else:
            print(f"⚠ Warning: Black still has {len(final_moves)} legal moves")

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
                result.append(f"{move_num}. {white_move}#")
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
    """Solve exercises 3 and 4 with deep search"""

    exercises = [
        (3, "W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8"),
        (4, "W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7"),
    ]

    print("\n" + "=" * 70)
    print("DEEP SEARCH FOR EXERCISES 3 AND 4")
    print("=" * 70)
    print("\nFeatures:")
    print("  • Iterative deepening (2, 4, 6, ... 20 moves)")
    print("  • Move ordering (captures prioritized)")
    print("  • Transposition table (cache)")
    print("  • Alpha-beta pruning")
    print("  • Node limit: 1,000,000 per move")
    print()

    results = {}

    for number, fen in exercises:
        print(f"\n{'='*70}")
        print(f"SOLVING EXERCISE {number}")
        print(f"{'='*70}\n")

        solver = DeepSearchSolver()
        solution = solver.solve(fen, max_depth=20)

        if solution:
            results[number] = "SOLVED"
        else:
            results[number] = "NOT SOLVED"

        print()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for number, status in results.items():
        print(f"Exercise {number}: {status}")


if __name__ == "__main__":
    main()
