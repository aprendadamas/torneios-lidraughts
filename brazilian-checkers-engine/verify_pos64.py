"""
Verificar se o sistema Pos64 está correto
"""

from src.pos64 import Pos64

print("=" * 70)
print("VERIFICAR SISTEMA POS64")
print("=" * 70)
print()

# Posição inicial do Russian/Brazilian
# W:W21,22,23,24,25,26,27,28,29,30,31,32:B1,2,3,4,5,6,7,8,9,10,11,12
print("POSIÇÃO INICIAL (Russian/Brazilian):")
print("Brancas: campos 21-32")
print("Pretas: campos 1-12")
print()

# Converter alguns campos para algébrico
test_fields = [1, 2, 3, 4, 21, 22, 23, 24, 29, 30, 31, 32]
print("Conversão campo → algébrico:")
for field in test_fields:
    pos = Pos64(field)
    alg = pos.to_algebraic()
    print(f"  Campo {field:2d} → {alg}")
print()

# Agora testar a posição do exercício
# [FEN "W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8."]
print("=" * 70)
print("EXERCÍCIO #15")
print("=" * 70)
print()

white_pieces = ["c1", "b2", "d2", "f4", "h4"]
black_pieces = ["a3", "d6", "h6", "e7", "f8"]

print("Brancas (notação algébrica → campo):")
for alg in white_pieces:
    pos = Pos64.from_algebraic(alg)
    if pos:
        print(f"  {alg} → campo {pos.field}")
    else:
        print(f"  {alg} → ERRO: não é uma casa escura válida")
print()

print("Pretas (notação algébrica → campo):")
for alg in black_pieces:
    pos = Pos64.from_algebraic(alg)
    if pos:
        print(f"  {alg} → campo {pos.field}")
    else:
        print(f"  {alg} → ERRO: não é uma casa escura válida")
print()

# Verificar movimentos das brancas (move UP = UpLeft, UpRight)
print("=" * 70)
print("MOVIMENTOS POSSÍVEIS DAS BRANCAS")
print("=" * 70)
print()

white_fields = set()
for alg in white_pieces:
    pos = Pos64.from_algebraic(alg)
    if pos:
        white_fields.add(pos.field)

black_fields = set()
for alg in black_pieces:
    pos = Pos64.from_algebraic(alg)
    if pos:
        black_fields.add(pos.field)

all_pieces = white_fields | black_fields

print(f"Brancas: {white_fields}")
print(f"Pretas: {black_fields}")
print()

for alg in white_pieces:
    pos = Pos64.from_algebraic(alg)
    if not pos:
        continue

    print(f"{alg} (campo {pos.field}):")

    # Brancas movem para CIMA (UpLeft, UpRight)
    up_left = pos.move_up_left()
    up_right = pos.move_up_right()

    if up_left:
        status = "ocupado" if up_left.field in all_pieces else "livre"
        print(f"  ↖ Cima-esquerda: {up_left.to_algebraic()} (campo {up_left.field}) - {status}")
    else:
        print(f"  ↖ Cima-esquerda: impossível (fora do tabuleiro)")

    if up_right:
        status = "ocupado" if up_right.field in all_pieces else "livre"
        print(f"  ↗ Cima-direita: {up_right.to_algebraic()} (campo {up_right.field}) - {status}")
    else:
        print(f"  ↗ Cima-direita: impossível (fora do tabuleiro)")
    print()

print("=" * 70)
print("TABULEIRO VISUAL")
print("=" * 70)
print()

print("    a  b  c  d  e  f  g  h")
print("  ┌─────────────────────────┐")

for row in range(8, 0, -1):
    print(f"{row} │", end="")
    for col in 'abcdefgh':
        alg = f"{col}{row}"
        pos = Pos64.from_algebraic(alg)
        if pos:
            if pos.field in white_fields:
                print(" W", end="")
            elif pos.field in black_fields:
                print(" B", end="")
            else:
                print(" ·", end="")
        else:
            print("  ", end="")
    print(" │")
print("  └─────────────────────────┘")
