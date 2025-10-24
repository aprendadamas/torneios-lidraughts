#!/usr/bin/env python3
"""
Final Brazilian Draughts Solver
Uses proper tactical search to find forced wins
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


class TacticalSolver:
    """Solver focused on finding forced wins through tactical sequences"""

    def __init__(self):
        self.nodes = 0

    def solve(self, fen):
        """Find the forced win in the position"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("TACTICAL SOLVER - Brazilian Draughts")
        print("=" * 70)
        print(f"\nFEN: {fen}\n")
        print(board)
        print()

        # Get all first moves
        legal_moves = list(board.legal_moves())

        print(f"Analyzing {len(legal_moves)} possible first moves...\n")

        best_solution = None
        shortest_mate = 999

        for first_move in legal_moves:
            self.nodes = 0
            print(f"Trying {first_move.pdn_move} ({self.pdn_to_alg(first_move.pdn_move)})... ", end='', flush=True)

            # Make the move
            board_after = board.copy()
            board_after.push(first_move)

            # Search for forced mate
            result = self.find_forced_win(board_after, max_depth=10, moves=[first_move])

            if result:
                mate_length = len(result)
                print(f"MATE IN {(mate_length+1)//2}! ({self.nodes} nodes)")

                if mate_length < shortest_mate:
                    shortest_mate = mate_length
                    best_solution = result
            else:
                print(f"no forced win ({self.nodes} nodes)")

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

    def find_forced_win(self, board, max_depth, moves):
        """
        Recursively find if current position leads to forced win
        Returns the complete move sequence if win is found, None otherwise
        """
        self.nodes += 1

        if max_depth <= 0:
            return None

        legal_moves = list(board.legal_moves())

        # Check if game is over
        if not legal_moves:
            # Current side to move has no moves - they lose
            # board.turn: 2 = White, 1 = Black
            # If it's Black's turn and they have no moves, White wins!
            if board.turn == 1:  # Black to move but can't
                return moves  # This is a winning line!
            else:
                return None  # White can't move, this is bad

        # Our turn (White)?
        if board.turn == 2:
            # We need to find at least ONE move that wins
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.find_forced_win(test_board, max_depth - 1, moves + [move])
                if result:
                    return result

            return None  # No winning move found

        else:
            # Opponent's turn (Black) - ALL their moves must lead to our win
            # We need to verify that no matter what Black does, White wins

            # First check: does Black have ANY move that doesn't lose?
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.find_forced_win(test_board, max_depth - 1, moves + [move])
                if result is None:
                    # Black can avoid forced win with this move
                    return None

            # All of Black's moves lead to White winning!
            # Return the line with Black's first move (for display)
            first_black_move = legal_moves[0]
            test_board = board.copy()
            test_board.push(first_black_move)

            return self.find_forced_win(test_board, max_depth - 1, moves + [first_black_move])

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
            print("#")  # Checkmate symbol
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

        # Show PDN notation too
        print("PDN notation:")
        pdn_moves = [m.pdn_move for m in moves]
        print(" → ".join(pdn_moves))

    def pdn_to_alg(self, pdn):
        """Convert PDN to algebraic"""
        if 'x' in pdn:
            parts = pdn.split('x')
            from_sq = int(parts[0])
            to_sq = int(parts[-1])
            from_alg = self.sq_to_alg(from_sq)
            to_alg = self.sq_to_alg(to_sq)

            # Multiple captures
            if len(parts) > 2:
                return f"{from_alg}x...x{to_alg}"
            else:
                # Check if it's a long capture (multiple pieces)
                if abs(to_sq - from_sq) > 10:
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
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("\n" + "=" * 70)
    print("EXERCISE 1")
    print("=" * 70)
    print("\nExpected solution: 1. c3-b4 a5xc3 2. b2xd4xf6xh8#\n")

    solver = TacticalSolver()
    solution = solver.solve(fen)

    if solution and solution[0].pdn_move == "10-13":
        print("\n" + "=" * 70)
        print("✓ SUCCESS! Found the correct solution!")
        print("=" * 70)
    elif solution:
        print("\n" + "=" * 70)
        print("⚠ Found a solution, but not the expected one")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("✗ Failed to find solution")
        print("=" * 70)


if __name__ == "__main__":
    main()
