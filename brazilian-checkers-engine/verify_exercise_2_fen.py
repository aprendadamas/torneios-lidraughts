"""
Verificar mapeamento correto do FEN para Exercise #2

FEN: W:Wc1,e1,f2,h2,g3,c5,e5,b6,d6:BKa1,Ka3,Kb4,h6,g7,f8.

Preciso garantir que o mapeamento algébrico → field está correto.
"""

from src.pos64 import Pos64

print("=" * 70)
print("VERIFICAÇÃO: Mapeamento FEN → Fields")
print("=" * 70)
print()

# Mapa correto de notação algébrica para fields
# Numeração 64 vai de 1 (a8) até 32 (h1)

print("Notação 64 (apenas casas escuras):")
print()
print("    a  b  c  d  e  f  g  h")
print("8 │ 1  ·  2  ·  3  ·  4  · │")
print("7 │ ·  5  ·  6  ·  7  ·  8 │")
print("6 │ 9  · 10  · 11  · 12  · │")
print("5 │ · 13  · 14  · 15  · 16 │")
print("4 │17  · 18  · 19  · 20  · │")
print("3 │ · 21  · 22  · 23  · 24 │")
print("2 │25  · 26  · 27  · 28  · │")
print("1 │ · 29  · 30  · 31  · 32 │")
print()

print("=" * 70)
print("White pieces: c1,e1,f2,h2,g3,c5,e5,b6,d6")
print("=" * 70)

white_positions = ["c1", "e1", "f2", "h2", "g3", "c5", "e5", "b6", "d6"]
white_fields = []

for pos in white_positions:
    # Pos64.from_algebraic retorna o field number
    field = Pos64.from_algebraic(pos).field
    white_fields.append(field)
    print(f"{pos:3s} → field {field:2d}")

print()
print(f"white_men = {set(white_fields)}")
print()

print("=" * 70)
print("Black pieces: Ka1,Ka3,Kb4,h6,g7,f8")
print("=" * 70)

black_kings_positions = ["a1", "a3", "b4"]
black_men_positions = ["h6", "g7", "f8"]

black_kings_fields = []
black_men_fields = []

print("\nDamas (Kings):")
for pos in black_kings_positions:
    field = Pos64.from_algebraic(pos).field
    black_kings_fields.append(field)
    print(f"{pos:3s} → field {field:2d}")

print("\nPeões (Men):")
for pos in black_men_positions:
    field = Pos64.from_algebraic(pos).field
    black_men_fields.append(field)
    print(f"{pos:3s} → field {field:2d}")

print()
print(f"black_kings = {set(black_kings_fields)}")
print(f"black_men = {set(black_men_fields)}")
print()

print("=" * 70)
print("CÓDIGO CORRETO:")
print("=" * 70)
print()
print(f"white_men = {set(white_fields)}")
print(f"white_kings = set()")
print(f"black_men = {set(black_men_fields)}")
print(f"black_kings = {set(black_kings_fields)}")
print()
