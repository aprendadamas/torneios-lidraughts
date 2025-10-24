#!/usr/bin/env python3
"""
Convert between PDN numeric notation and algebraic notation for Brazilian draughts
"""

# Brazilian draughts uses an 8x8 board with 32 playable dark squares
# Squares are numbered 1-32 in standard notation

def square_number_to_algebraic(square_num):
    """
    Convert square number (1-32) to algebraic notation (a1-h8)
    Brazilian draughts numbers the dark squares from bottom-left to top-right
    """
    # Mapping for 8x8 board (Brazilian draughts)
    # Dark squares only
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
    return mapping.get(square_num, f'?{square_num}?')


def algebraic_to_square_number(algebraic):
    """Convert algebraic notation to square number"""
    mapping = {
        'a1': 1, 'c1': 2, 'e1': 3, 'g1': 4,
        'b2': 5, 'd2': 6, 'f2': 7, 'h2': 8,
        'a3': 9, 'c3': 10, 'e3': 11, 'g3': 12,
        'b4': 13, 'd4': 14, 'f4': 15, 'h4': 16,
        'a5': 17, 'c5': 18, 'e5': 19, 'g5': 20,
        'b6': 21, 'd6': 22, 'f6': 23, 'h6': 24,
        'a7': 25, 'c7': 26, 'e7': 27, 'g7': 28,
        'b8': 29, 'd8': 30, 'f8': 31, 'h8': 32,
    }
    return mapping.get(algebraic.lower(), None)


def pdn_to_algebraic(pdn_move):
    """
    Convert PDN notation (like "5-9" or "9x18") to algebraic (like "b2-a3")
    """
    if 'x' in pdn_move:
        # Capture move
        parts = pdn_move.split('x')
        from_sq = int(parts[0])
        to_sq = int(parts[-1])
        from_alg = square_number_to_algebraic(from_sq)
        to_alg = square_number_to_algebraic(to_sq)
        return f"{from_alg}x{to_alg}"
    elif '-' in pdn_move:
        # Normal move
        parts = pdn_move.split('-')
        from_sq = int(parts[0])
        to_sq = int(parts[1])
        from_alg = square_number_to_algebraic(from_sq)
        to_alg = square_number_to_algebraic(to_sq)
        return f"{from_alg}-{to_alg}"
    else:
        return pdn_move


def convert_solution(pdn_moves):
    """Convert a list of PDN moves to algebraic notation"""
    return [pdn_to_algebraic(move) for move in pdn_moves]


def main():
    """Test the converter"""
    # Test with the solution from the solver
    pdn_solution = ['5-9', '17-13', '9x18', '19-14', '18x11', '28-23', '10-13', '23-19', '13-18', '19-15', '11x20']

    print("PDN to Algebraic Conversion")
    print("=" * 60)
    print()

    print("Square number mapping (partial):")
    print("  1 (a1), 5 (b2), 10 (c3), 17 (a5), 19 (e5), 28 (g7)")
    print()

    print("Solution conversion:")
    print()
    print("PDN notation:")
    print(" → ".join(pdn_solution))
    print()

    algebraic_solution = convert_solution(pdn_solution)
    print("Algebraic notation:")
    print(" → ".join(algebraic_solution))
    print()

    print("Move by move:")
    for i, (pdn, alg) in enumerate(zip(pdn_solution, algebraic_solution), 1):
        player = "White" if i % 2 == 1 else "Black"
        print(f"  {i}. {pdn:8} = {alg:12} ({player})")


if __name__ == "__main__":
    main()
