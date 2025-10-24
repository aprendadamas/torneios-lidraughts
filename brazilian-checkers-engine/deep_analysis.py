"""
Análise profunda - simular jogadas e buscar táticas
"""

from src.pos64 import Pos64

# Estado inicial
white_fields = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_fields = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

field_to_alg = {
    30: 'c1', 25: 'b2', 26: 'd2', 19: 'f4', 20: 'h4',
    21: 'a3', 10: 'd6', 12: 'h6', 7: 'e7', 3: 'f8'
}

print("="*70)
print("ANÁLISE PROFUNDA - BUSCAR SEQUÊNCIAS TÁTICAS")
print("="*70)
print()

def simulate_move(from_field, to_field, white, black, verbose=True):
    """Simula um movimento e retorna novo estado"""
    new_white = white.copy()
    new_black = black.copy()

    new_white.remove(from_field)
    new_white.add(to_field)

    from_alg = field_to_alg.get(from_field, f"campo {from_field}")
    to_alg = Pos64(to_field).to_algebraic()

    if verbose:
        print(f"  Brancas: {from_alg} → {to_alg}")

    return new_white, new_black

def check_black_captures(white, black):
    """Verifica se pretas têm capturas após jogada das brancas"""
    captures = []

    for b_field in black:
        pos = Pos64(b_field)

        # Pretas movem para baixo (movesDown)
        # Verificar captura baixo-esquerda
        down_left = pos.move_down_left()
        if down_left and down_left.field in white:
            jump_dest = down_left.move_down_left()
            if jump_dest and jump_dest.field not in white and jump_dest.field not in black:
                captures.append((b_field, down_left.field, jump_dest.field))

        # Verificar captura baixo-direita
        down_right = pos.move_down_right()
        if down_right and down_right.field in white:
            jump_dest = down_right.move_down_right()
            if jump_dest and jump_dest.field not in white and jump_dest.field not in black:
                captures.append((b_field, down_right.field, jump_dest.field))

    return captures

print("Testando movimentos candidatos das BRANCAS:")
print()

# Testar movimento b2 → c3
print("1️⃣  Movimento: b2 → c3 (campo 25 → 22)")
new_white, new_black = simulate_move(25, 22, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

# Testar movimento d2 → c3
print("2️⃣  Movimento: d2 → c3 (campo 26 → 22)")
new_white, new_black = simulate_move(26, 22, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

# Testar movimento d2 → e3
print("3️⃣  Movimento: d2 → e3 (campo 26 → 23)")
new_white, new_black = simulate_move(26, 23, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

# Testar movimento f4 → e5
print("4️⃣  Movimento: f4 → e5 (campo 19 → 15)")
new_white, new_black = simulate_move(19, 15, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

# Testar movimento f4 → g5
print("5️⃣  Movimento: f4 → g5 (campo 19 → 16)")
new_white, new_black = simulate_move(19, 16, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

# Testar movimento h4 → g5
print("6️⃣  Movimento: h4 → g5 (campo 20 → 16)")
new_white, new_black = simulate_move(20, 16, white_fields, black_fields)
black_caps = check_black_captures(new_white, new_black)
if black_caps:
    print("  ⚠️  PRETAS CAPTURAM:")
    for from_f, over_f, to_f in black_caps:
        from_alg = field_to_alg.get(from_f, f"campo {from_f}")
        over_alg = field_to_alg.get(over_f, f"campo {over_f}")
        to_alg = Pos64(to_f).to_algebraic()
        print(f"      {from_alg} x {over_alg} → {to_alg}")
else:
    print("  ✓ Pretas não têm capturas")
print()

print("="*70)
print("CONCLUSÃO")
print("="*70)
print()
print("Nenhum movimento imediato cria capturas para as brancas.")
print("Vou analisar qual movimento cria mais ameaças táticas...")
