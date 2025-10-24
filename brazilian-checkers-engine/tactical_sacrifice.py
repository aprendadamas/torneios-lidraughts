"""
ANÁLISE DE SACRIFÍCIO TÁTICO
Reanalisar f4 → e5 como possível combinação
"""

from src.pos64 import Pos64

white_fields = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_fields = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

field_to_alg = {
    30: 'c1', 25: 'b2', 26: 'd2', 19: 'f4', 20: 'h4',
    21: 'a3', 10: 'd6', 12: 'h6', 7: 'e7', 3: 'f8',
    15: 'e5', 22: 'c3', 23: 'e3', 16: 'g5', 18: 'd4',
    14: 'c5', 6: 'd7', 2: 'c8'
}

print("="*70)
print("ANÁLISE DE SACRIFÍCIO TÁTICO")
print("="*70)
print()

print("SEQUÊNCIA:")
print("1. Brancas: f4 → e5 (campo 19 → 15)")
print()

# Após f4 → e5
new_white = {30, 25, 26, 15, 20}  # moveu f4 para e5
print("Peças pretas podem capturar:")
print("  - d6 x e5 → f4 (campo 10 x 15 → 19)")
print()

print("2. Pretas CAPTURAM: d6 x e5 → f4")
print()

# Após d6 capturar em f4
after_white = {30, 25, 26, 20}  # perdeu a peça em e5
after_black = {21, 19, 12, 7, 3}  # d6 foi para f4

print("Posição após a captura:")
print("  Brancas: c1(30), b2(25), d2(26), h4(20)")
print("  Pretas: a3(21), f4(19), h6(12), e7(7), f8(3)")
print()

print("="*70)
print("AGORA AS BRANCAS PODEM CAPTURAR?")
print("="*70)
print()

# Verificar capturas possíveis para as brancas
for w_field in after_white:
    pos = Pos64(w_field)
    w_alg = field_to_alg.get(w_field, f"campo {w_field}")

    # Verificar captura cima-esquerda
    up_left = pos.move_up_left()
    if up_left and up_left.field in after_black:
        jump_dest = up_left.move_up_left()
        if jump_dest and jump_dest.field not in after_white and jump_dest.field not in after_black:
            over_alg = field_to_alg.get(up_left.field, f"campo {up_left.field}")
            to_alg = jump_dest.to_algebraic()
            print(f"✓ {w_alg} x {over_alg} → {to_alg} (campo {jump_dest.field})")

            # VERIFICAR CAPTURA MÚLTIPLA!
            print(f"  Após capturar em {to_alg}, verificando capturas adicionais...")
            next_pos = jump_dest

            # De jump_dest, verificar mais capturas
            next_up_left = next_pos.move_up_left()
            if next_up_left and next_up_left.field in after_black:
                next_jump = next_up_left.move_up_left()
                if next_jump:
                    next_over_alg = field_to_alg.get(next_up_left.field, f"campo {next_up_left.field}")
                    next_to_alg = next_jump.to_algebraic()
                    print(f"    ✓✓ Continua: {to_alg} x {next_over_alg} → {next_to_alg}")

            next_up_right = next_pos.move_up_right()
            if next_up_right and next_up_right.field in after_black:
                next_jump = next_up_right.move_up_right()
                if next_jump:
                    next_over_alg = field_to_alg.get(next_up_right.field, f"campo {next_up_right.field}")
                    next_to_alg = next_jump.to_algebraic()
                    print(f"    ✓✓ Continua: {to_alg} x {next_over_alg} → {next_to_alg}")

    # Verificar captura cima-direita
    up_right = pos.move_up_right()
    if up_right and up_right.field in after_black:
        jump_dest = up_right.move_up_right()
        if jump_dest and jump_dest.field not in after_white and jump_dest.field not in after_black:
            over_alg = field_to_alg.get(up_right.field, f"campo {up_right.field}")
            to_alg = jump_dest.to_algebraic()
            print(f"✓ {w_alg} x {over_alg} → {to_alg} (campo {jump_dest.field})")

            # VERIFICAR CAPTURA MÚLTIPLA!
            print(f"  Após capturar em {to_alg}, verificando capturas adicionais...")
            next_pos = jump_dest

            # De jump_dest, verificar mais capturas
            next_up_left = next_pos.move_up_left()
            if next_up_left and next_up_left.field in after_black:
                next_jump = next_up_left.move_up_left()
                if next_jump:
                    next_over_alg = field_to_alg.get(next_up_left.field, f"campo {next_up_left.field}")
                    next_to_alg = next_jump.to_algebraic()
                    print(f"    ✓✓ Continua: {to_alg} x {next_over_alg} → {next_to_alg}")

            next_up_right = next_pos.move_up_right()
            if next_up_right and next_up_right.field in after_black:
                next_jump = next_up_right.move_up_right()
                if next_jump:
                    next_over_alg = field_to_alg.get(next_up_right.field, f"campo {next_up_right.field}")
                    next_to_alg = next_jump.to_algebraic()
                    print(f"    ✓✓ Continua: {to_alg} x {next_over_alg} → {next_to_alg}")

print()
print("="*70)
print("CONTAGEM FINAL")
print("="*70)
print()
print("Se a sequência terminar com capturas múltiplas:")
print("  Brancas perdem: 1 peça (sacrificada em e5)")
print("  Brancas ganham: ? peças (a contar pelas capturas)")
print()
print("Se ganhar 2+ peças, é uma COMBINAÇÃO VENCEDORA! 🎯")
