"""
Analisar qual movimento cria mais ameaças táticas
"""

from src.pos64 import Pos64

white_fields = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_fields = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

field_to_alg = {
    30: 'c1', 25: 'b2', 26: 'd2', 19: 'f4', 20: 'h4',
    21: 'a3', 10: 'd6', 12: 'h6', 7: 'e7', 3: 'f8'
}

def check_white_threats(white, black):
    """
    Verifica ameaças de captura das brancas
    Retorna lista de capturas possíveis no próximo lance
    """
    threats = []

    for w_field in white:
        pos = Pos64(w_field)

        # Brancas movem para cima (movesUp)
        # Verificar ameaça cima-esquerda
        up_left = pos.move_up_left()
        if up_left and up_left.field in black:
            jump_dest = up_left.move_up_left()
            if jump_dest and jump_dest.field not in white and jump_dest.field not in black:
                from_alg = field_to_alg.get(w_field, f"campo {w_field}")
                over_alg = field_to_alg.get(up_left.field, f"campo {up_left.field}")
                to_alg = jump_dest.to_algebraic()
                threats.append((from_alg, over_alg, to_alg))

        # Verificar ameaça cima-direita
        up_right = pos.move_up_right()
        if up_right and up_right.field in black:
            jump_dest = up_right.move_up_right()
            if jump_dest and jump_dest.field not in white and jump_dest.field not in black:
                from_alg = field_to_alg.get(w_field, f"campo {w_field}")
                over_alg = field_to_alg.get(up_right.field, f"campo {up_right.field}")
                to_alg = jump_dest.to_algebraic()
                threats.append((from_alg, over_alg, to_alg))

    return threats

print("="*70)
print("ANÁLISE DE AMEAÇAS APÓS CADA MOVIMENTO")
print("="*70)
print()

# Movimentos candidatos (apenas os seguros)
candidates = [
    (25, 22, "b2 → c3"),
    (26, 22, "d2 → c3"),
    (26, 23, "d2 → e3"),
    (20, 16, "h4 → g5"),
]

for from_field, to_field, move_desc in candidates:
    print(f"Após {move_desc}:")

    # Simular movimento
    new_white = white_fields.copy()
    new_white.remove(from_field)
    new_white.add(to_field)

    # Verificar ameaças criadas
    threats = check_white_threats(new_white, black_fields)

    if threats:
        print(f"  ✨ Cria {len(threats)} ameaça(s) de captura:")
        for from_alg, over_alg, to_alg in threats:
            print(f"      {from_alg} pode capturar {over_alg} → {to_alg}")
    else:
        print(f"  ⚪ Sem ameaças diretas de captura")

    print()

print("="*70)
print("ANÁLISE ADICIONAL: POSIÇÃO DAS PEÇAS")
print("="*70)
print()

# Analisar controle do centro e estrutura
print("Analisando cada movimento:")
print()

print("1. b2 → c3:")
print("   - Avança para o centro")
print("   - Apoia futuro avanço de d2")
print()

print("2. d2 → c3:")
print("   - Centraliza peça")
print("   - Cria dobradinha com b2")
print()

print("3. d2 → e3:")
print("   - Centraliza peça")
print("   - Avança na diagonal central")
print("   - Prepara coordenação com f4")
print()

print("4. h4 → g5:")
print("   - Avança na ala do rei")
print("   - Aproxima de h6")
print()

print("="*70)
print("BUSCA MAIS PROFUNDA - 2 LANCES À FRENTE")
print("="*70)
print()

# Simular d2 → e3 e ver resposta das pretas
print("Testando sequência: d2 → e3")
new_white = white_fields.copy()
new_white.remove(26)
new_white.add(23)

print("Após d2 → e3, as pretas podem jogar:")
print("  - a3 → b4")
print("  - d6 → c5 ou e5")
print("  - h6 → g5")
print("  - e7 → d6 ou f6")
print("  - f8 → e7")
print()

# Verificar se após d6→e5, as brancas podem capturar
print("Se pretas jogarem d6 → e5 (campo 10 → 15):")
test_black = black_fields.copy()
test_black.remove(10)
test_black.add(15)

# Campo 23 (e3) pode capturar campo 15 (e5)?
pos_e3 = Pos64(23)
up_left = pos_e3.move_up_left()
up_right = pos_e3.move_up_right()

if up_left:
    print(f"  e3 cima-esquerda: {up_left.to_algebraic()} (campo {up_left.field})")
if up_right:
    print(f"  e3 cima-direita: {up_right.to_algebraic()} (campo {up_right.field})")

if (up_left and up_left.field == 15) or (up_right and up_right.field == 15):
    print("  🎯 BRANCAS PODEM CAPTURAR!")
    # Verificar destino da captura
    if up_left and up_left.field == 15:
        jump = up_left.move_up_left()
        if jump:
            print(f"     e3 x e5 → {jump.to_algebraic()}")
    if up_right and up_right.field == 15:
        jump = up_right.move_up_right()
        if jump:
            print(f"     e3 x e5 → {jump.to_algebraic()}")
