#!/usr/bin/env python3
"""
Mate-finding solver for Brazilian Draughts
Specifically looks for forced wins (checkmate sequences)
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board


class MateSolver:
    """Find forced wins (mates)"""

    def __init__(self):
        self.nodes = 0

    def find_mate(self, fen, max_depth=20):
        """Find mate in N moves"""
        board = Board(variant="brazilian", fen=fen)

        print("=" * 70)
        print("MATE SOLVER - Finding forced wins")
        print("=" * 70)
        print(f"\nFEN: {fen}")
        print(f"Turn: {'White' if board.turn else 'Black'}\n")
        print(board)
        print()

        # Try to find mate at each depth
        for mate_in in range(1, max_depth + 1):
            print(f"Searching for mate in {mate_in}... ", end='', flush=True)
            self.nodes = 0

            result = self.search_mate(board, mate_in, True)

            if result:
                print(f"FOUND! ({self.nodes} nodes)")
                print("\n" + "=" * 70)
                print(f"MATE IN {mate_in}")
                print("=" * 70)
                print()
                self.display_solution(board, result)
                return result
            else:
                print(f"not found ({self.nodes} nodes)")

        print("\nNo mate found within search depth")
        return None

    def search_mate(self, board, depth, is_white_turn):
        """
        Search for forced mate
        Returns a list of moves leading to mate, or None
        """
        self.nodes += 1

        legal_moves = list(board.legal_moves())

        # Check if game is over
        if not legal_moves:
            # No legal moves - current side to move loses
            if board.turn == is_white_turn:
                # We're looking for White to win, and Black has no moves
                # This is a mate!
                return []
            else:
                # White has no moves, this is not what we want
                return None

        if depth == 0:
            return None

        # If it's our turn (the side we're trying to win for)
        if board.turn == is_white_turn:
            # We need to find at least ONE move that leads to mate
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.search_mate(test_board, depth, is_white_turn)
                if result is not None:
                    # Found a winning line!
                    return [move] + result

            # No winning move found
            return None
        else:
            # It's opponent's turn - ALL their moves must lead to our mate
            opponent_can_avoid = False

            # Try each opponent move
            for move in legal_moves:
                test_board = board.copy()
                test_board.push(move)

                result = self.search_mate(test_board, depth - 1, is_white_turn)
                if result is None:
                    # Opponent can avoid mate with this move
                    opponent_can_avoid = True
                    break

            if opponent_can_avoid:
                return None

            # All opponent moves lead to mate!
            # Pick the first one for the principal variation
            first_move = legal_moves[0]
            test_board = board.copy()
            test_board.push(first_move)
            result = self.search_mate(test_board, depth - 1, is_white_turn)

            if result is not None:
                return [first_move] + result

            return None

    def display_solution(self, board, moves):
        """Display the mate sequence"""
        temp_board = board.copy()

        print("Mate sequence:")
        print()

        move_number = 1
        white_move = None

        for i, move in enumerate(moves):
            notation = move.pdn_move
            alg = self.pdn_to_algebraic(notation)

            if i % 2 == 0:  # White move
                print(f"{move_number}. {alg:20} ", end='')
                white_move = alg
                temp_board.push(move)
            else:  # Black move
                print(f"{alg}")
                temp_board.push(move)
                move_number += 1

        # If last move was by white
        if len(moves) % 2 == 1:
            print()

        print()
        print("Final position:")
        print(temp_board)
        print()

        # Verify it's mate
        final_moves = list(temp_board.legal_moves())
        if not final_moves:
            print("*** CHECKMATE! Black has no legal moves ***")
        else:
            print(f"Warning: Position is not mate (Black has {len(final_moves)} legal moves)")

    def pdn_to_algebraic(self, pdn):
        """Convert PDN to algebraic"""
        if 'x' in pdn:
            parts = pdn.split('x')
            from_sq = int(parts[0])
            to_sq = int(parts[-1])
            from_alg = self.sq_to_alg(from_sq)
            to_alg = self.sq_to_alg(to_sq)

            if len(parts) > 2:
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
    fen = "W:Wa1,b2,c3:Ba5,e5,g7"

    print("\nExercise 1 - Mate Finder")
    print("\nExpected solution: 1. c3-b4 a5xc3 2. b2xd4xf6xh8#")
    print()

    solver = MateSolver()
    solution = solver.find_mate(fen, max_depth=6)

    if solution:
        print("\n" + "=" * 70)
        print("SUCCESS!")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("FAILED TO FIND MATE")
        print("=" * 70)


if __name__ == "__main__":
    main()
