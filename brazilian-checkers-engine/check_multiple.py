"""
Verificar se d6 pode fazer captura múltipla após capturar e5
"""

from src.pos64 import Pos64

def print_board(white, black, title=""):
    """Imprime tabuleiro visual"""
    if title:
        print(f"\n{title}")
    print("    a  b  c  d  e  f  g  h")
    print("  ┌─────────────────────────┐")

    for row in range(8, 0, -1):
        print(f"{row} │", end="")
        for col in 'abcdefgh':
            alg = f"{col}{row}"
            pos = Pos64.from_algebraic(alg)
            if pos:
                if pos.field in white:
                    print(" w", end="")
                elif pos.field in black:
                    print(" b", end="")
                else:
                    print(" ·", end="")
            else:
                print("  ", end="")
        print(" │")
    print("  └─────────────────────────┘\n")

# Após f4 → e5
white = {30, 25, 26, 15, 20}  # c1, b2, d2, e5, h4
black = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

print("="*70)
print("VERIFICAR CAPTURA MÚLTIPLA DAS PRETAS")
print("="*70)

print_board(white, black, "Após f4 → e5, antes das pretas capturarem:")

print("d6 está em campo 10")
print("e5 está em campo 15")
print()

pos_d6 = Pos64(10)
print("d6 captura e5:")

# d6 captura e5 via baixo-direita e vai para f4 (campo 19)
print("  d6 x e5 → f4")
print()

# Após a primeira captura
white_after = {30, 25, 26, 20}  # perdeu e5
black_after = {21, 19, 12, 7, 3}  # d6 foi para f4

print_board(white_after, black_after, "Após d6 x e5 → f4:")

print("AGORA, de f4 (campo 19), d6 pode capturar MAIS?")
print()

pos_f4 = Pos64(19)
print(f"De f4 (campo {pos_f4.field}):")

down_left = pos_f4.move_down_left()
down_right = pos_f4.move_down_right()

print(f"  Baixo-esquerda: {down_left}")
print(f"  Baixo-direita: {down_right}")

if down_left:
    print(f"\n  Baixo-esquerda = {down_left.to_algebraic()} (campo {down_left.field})")
    if down_left.field in white_after:
        print(f"    TEM PEÇA BRANCA! Pode capturar!")
        jump = down_left.move_down_left()
        if jump and jump.field not in white_after and jump.field not in black_after:
            print(f"    f4 x {down_left.to_algebraic()} → {jump.to_algebraic()}")
            print()
            print(f"✅ CAPTURA MÚLTIPLA: d6 x e5 x {down_left.to_algebraic()} → {jump.to_algebraic()}")

if down_right:
    print(f"\n  Baixo-direita = {down_right.to_algebraic()} (campo {down_right.field})")
    if down_right.field in white_after:
        print(f"    TEM PEÇA BRANCA! Pode capturar!")
        jump = down_right.move_down_right()
        if jump and jump.field not in white_after and jump.field not in black_after:
            print(f"    f4 x {down_right.to_algebraic()} → {jump.to_algebraic()}")
            print()
            print(f"✅ CAPTURA MÚLTIPLA: d6 x e5 x {down_right.to_algebraic()} → {jump.to_algebraic()}")

print()
print("="*70)
print("E SE AS PRETAS NÃO FOREM OBRIGADAS A CAPTURAR?")
print("="*70)
print()
print("Verificar se as pretas têm OUTRAS capturas disponíveis na posição:")
print()

# Verificar todas as peças pretas
for b_field in black:
    pos_b = Pos64(b_field)
    b_alg = pos_b.to_algebraic()

    # Verificar capturas
    for direction, move_func, jump_func in [
        ("baixo-esquerda", pos_b.move_down_left, lambda p: p.move_down_left()),
        ("baixo-direita", pos_b.move_down_right, lambda p: p.move_down_right()),
    ]:
        adjacent = move_func()
        if adjacent and adjacent.field in white:
            dest = jump_func(adjacent)
            if dest and dest.field not in white and dest.field not in black:
                print(f"  {b_alg} x {adjacent.to_algebraic()} → {dest.to_algebraic()}")
