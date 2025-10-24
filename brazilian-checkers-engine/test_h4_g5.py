"""
Testar h4 → g5 como sacrifício tático
"""

from src.pos64 import Pos64

white_fields = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_fields = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

field_to_alg = {
    30: 'c1', 25: 'b2', 26: 'd2', 19: 'f4', 20: 'h4',
    21: 'a3', 10: 'd6', 12: 'h6', 7: 'e7', 3: 'f8',
    15: 'e5', 16: 'g5', 11: 'e6', 14: 'c5', 18: 'd4',
    23: 'e3', 27: 'g3', 24: 'h2'
}

print("="*70)
print("TESTAR: h4 → g5 COMO SACRIFÍCIO")
print("="*70)
print()

print("1. Brancas: h4 → g5 (campo 20 → 16)")
print()

# Após h4 → g5
after_move_white = {30, 25, 26, 19, 16}
print("Pretas podem capturar:")
print("  - h6 x g5 → f4 (campo 12 x 16 → 19)")
print()

# Simular captura
print("2. Pretas CAPTURAM: h6 x g5 → f4")
print()

after_white = {30, 25, 26, 19}  # perdeu g5
after_black = {21, 10, 19, 7, 3}  # h6 foi para f4 (campo 19)

print("Posição após captura:")
print("  Brancas: c1(30), b2(25), d2(26), f4(19)")
print("  Pretas: a3(21), d6(10), f4(19), e7(7), f8(3)")
print()

print("ERRO: Agora f4 tem 2 peças!?")
print("Isso significa que f4 ORIGINAL (campo 19) ainda está lá!")
print()

print("RECALCULANDO:")
print()

# Corrigir: f4 está em campo 19, então após h6 capturar g5...
# h6 está em campo 12
# g5 está em campo 16
# Captura: 12 x 16 → ?

pos_h6 = Pos64(12)
print(f"h6 está em campo {pos_h6.field}")

down_left = pos_h6.move_down_left()
down_right = pos_h6.move_down_right()

print(f"  Baixo-esquerda: {down_left}")
print(f"  Baixo-direita: {down_right}")

if down_left:
    print(f"  Baixo-esquerda campo: {down_left.field} = {down_left.to_algebraic()}")
    jump = down_left.move_down_left()
    if jump:
        print(f"    Captura para: campo {jump.field} = {jump.to_algebraic()}")

if down_right:
    print(f"  Baixo-direita campo: {down_right.field} = {down_right.to_algebraic()}")
    jump = down_right.move_down_right()
    if jump:
        print(f"    Captura para: campo {jump.field} = {jump.to_algebraic()}")

print()
print("="*70)
print("VERIFICAR SE BRANCAS CAPTURAM APÓS ISSO")
print("="*70)
print()

# Após h6 capturar g5
# Assumindo que h6 vai para campo 20 (verificar!)
if down_left and down_left.field == 16:  # g5
    jump_dest = down_left.move_down_left()
    if jump_dest:
        print(f"h6 captura g5 e vai para {jump_dest.to_algebraic()} (campo {jump_dest.field})")

        # Nova posição
        final_white = {30, 25, 26, 19}  # perdeu h4 (que virou g5)
        final_black = {21, 10, jump_dest.field, 7, 3}  # h6 foi para jump_dest

        print()
        print(f"Posição após h6 x g5 → {jump_dest.to_algebraic()}:")
        print(f"  Brancas: c1(30), b2(25), d2(26), f4(19)")
        print(f"  Pretas: a3(21), d6(10), {jump_dest.to_algebraic()}({jump_dest.field}), e7(7), f8(3)")
        print()

        # Verificar capturas das brancas
        print("Brancas podem capturar?")
        for w_field in final_white:
            pos = Pos64(w_field)
            w_alg = field_to_alg.get(w_field, f"campo {w_field}")

            # Captura cima-esquerda
            up_left = pos.move_up_left()
            if up_left and up_left.field in final_black:
                jump = up_left.move_up_left()
                if jump and jump.field not in final_white and jump.field not in final_black:
                    over_alg = field_to_alg.get(up_left.field, f"campo {up_left.field}")
                    print(f"  ✓ {w_alg} x {over_alg} → {jump.to_algebraic()}")

            # Captura cima-direita
            up_right = pos.move_up_right()
            if up_right and up_right.field in final_black:
                jump = up_right.move_up_right()
                if jump and jump.field not in final_white and jump.field not in final_black:
                    over_alg = field_to_alg.get(up_right.field, f"campo {up_right.field}")
                    print(f"  ✓ {w_alg} x {over_alg} → {jump.to_algebraic()}")
