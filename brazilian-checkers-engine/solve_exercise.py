"""
Análise do exercício tático usando Pos64 (sistema correto do Lidraughts)
"""

from src.pos64 import Pos64

# Exercício: W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8
print("="*70)
print("EXERCÍCIO TÁTICO - 1800 Combinações #15")
print("="*70)
print()
print("FEN: W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8")
print()

# Converter posições
white_positions = ['c1', 'b2', 'd2', 'f4', 'h4']
black_positions = ['a3', 'd6', 'h6', 'e7', 'f8']

print("Peças BRANCAS (vez de jogar):")
white_fields = {}
for alg in white_positions:
    pos = Pos64.from_algebraic(alg)
    if pos:
        white_fields[pos.field] = alg
        print(f"  {alg:3} → Campo {pos.field:2}")

print()
print("Peças PRETAS:")
black_fields = {}
for alg in black_positions:
    pos = Pos64.from_algebraic(alg)
    if pos:
        black_fields[pos.field] = alg
        print(f"  {alg:3} → Campo {pos.field:2}")

print()
print("="*70)
print("VISUALIZAÇÃO DO TABULEIRO")
print("="*70)
print()

# Criar tabuleiro visual (campos 1-32)
# Layout do tabuleiro 8x8 com numeração de campos:
#
#  8 |    1    2    3    4       (linha 8 visual = y=1 interno)
#  7 |  5    6    7    8         (linha 7 visual = y=2 interno)
#  6 |    9   10   11   12       (linha 6 visual = y=3 interno)
#  5 | 13   14   15   16         (linha 5 visual = y=4 interno)
#  4 |   17   18   19   20       (linha 4 visual = y=5 interno)
#  3 | 21   22   23   24         (linha 6 visual = y=6 interno)
#  2 |   25   26   27   28       (linha 2 visual = y=7 interno)
#  1 | 29   30   31   32         (linha 1 visual = y=8 interno)
#     a  b  c  d  e  f  g  h

# Imprimir tabuleiro
print("    a  b  c  d  e  f  g  h")
print("  ┌─────────────────────────┐")

for visual_row in range(8, 0, -1):  # 8 até 1
    print(f"{visual_row} │", end="")

    for col in range(1, 9):  # a-h (1-8)
        alg = f"{chr(96 + col)}{visual_row}"
        pos = Pos64.from_algebraic(alg)

        if pos:
            field = pos.field
            if field in white_fields:
                print(" w", end="")
            elif field in black_fields:
                print(" b", end="")
            else:
                print(" ·", end="")
        else:
            print("  ", end="")  # Casa clara

    print(" │")

print("  └─────────────────────────┘")
print("    a  b  c  d  e  f  g  h")

print()
print("="*70)
print("ANÁLISE DE MOVIMENTOS POSSÍVEIS PARA AS BRANCAS")
print("="*70)
print()

# Analisar movimentos para cada peça branca
# Brancas movem "para cima" no tabuleiro visual (campos diminuem)
# Ou seja, usam movesUp do Pos64

for alg in white_positions:
    pos = Pos64.from_algebraic(alg)
    if not pos:
        continue

    print(f"\nPeça branca em {alg} (campo {pos.field}):")

    # Movimentos possíveis para cima (direção das brancas)
    up_left = pos.move_up_left()
    up_right = pos.move_up_right()

    if up_left:
        target_alg = up_left.to_algebraic()
        occupied = "OCUPADO" if up_left.field in white_fields or up_left.field in black_fields else "vazio"
        piece = ""
        if up_left.field in white_fields:
            piece = "(peça branca)"
        elif up_left.field in black_fields:
            piece = "(peça PRETA)"
        print(f"  ↖ Cima-esquerda: {target_alg} (campo {up_left.field}) - {occupied} {piece}")
    else:
        print(f"  ↖ Cima-esquerda: bloqueado")

    if up_right:
        target_alg = up_right.to_algebraic()
        occupied = "OCUPADO" if up_right.field in white_fields or up_right.field in black_fields else "vazio"
        piece = ""
        if up_right.field in white_fields:
            piece = "(peça branca)"
        elif up_right.field in black_fields:
            piece = "(peça PRETA)"
        print(f"  ↗ Cima-direita: {target_alg} (campo {up_right.field}) - {occupied} {piece}")
    else:
        print(f"  ↗ Cima-direita: bloqueado")

print()
print("="*70)
print("CAPTURAS POSSÍVEIS")
print("="*70)
print()

# Analisar capturas
# Uma captura requer: peça inimiga adjacente + casa vazia após ela
for alg in white_positions:
    pos = Pos64.from_algebraic(alg)
    if not pos:
        continue

    captures_found = False

    # Verificar captura cima-esquerda
    up_left = pos.move_up_left()
    if up_left and up_left.field in black_fields:
        # Tem peça preta adjacente, verificar se pode saltar
        jump_dest = up_left.move_up_left()
        if jump_dest and jump_dest.field not in white_fields and jump_dest.field not in black_fields:
            if not captures_found:
                print(f"\n🎯 Peça em {alg} (campo {pos.field}) pode capturar:")
                captures_found = True
            print(f"  ✓ {alg} x {up_left.to_algebraic()} → {jump_dest.to_algebraic()}")

    # Verificar captura cima-direita
    up_right = pos.move_up_right()
    if up_right and up_right.field in black_fields:
        jump_dest = up_right.move_up_right()
        if jump_dest and jump_dest.field not in white_fields and jump_dest.field not in black_fields:
            if not captures_found:
                print(f"\n🎯 Peça em {alg} (campo {pos.field}) pode capturar:")
                captures_found = True
            print(f"  ✓ {alg} x {up_right.to_algebraic()} → {jump_dest.to_algebraic()}")

print()
print("="*70)
