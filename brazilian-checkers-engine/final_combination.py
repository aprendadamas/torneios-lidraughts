"""
ANÁLISE COMPLETA: f4 → e5 como início da combinação
Vou simular múltiplos lances à frente
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

# Posição inicial
white = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

print("="*70)
print("COMBINAÇÃO COMPLETA - f4 → e5")
print("="*70)

print_board(white, black, "POSIÇÃO INICIAL:")

print("1. Brancas jogam: f4 → e5")
white1 = {30, 25, 26, 15, 20}  # f4 (19) → e5 (15)
print_board(white1, black, "Após 1. f4 → e5:")

print("As pretas DEVEM capturar (captura obrigatória):")
print("   d6 x e5 → ... (campo 10 x 15 → ?)")
print()

# Calcular destino da captura
pos_d6 = Pos64(10)
print(f"d6 = campo {pos_d6.field}")

down_left = pos_d6.move_down_left()
down_right = pos_d6.move_down_right()

print(f"  Movimentos para baixo:")
if down_left:
    print(f"    Baixo-esquerda: {down_left.to_algebraic()} (campo {down_left.field})")
if down_right:
    print(f"    Baixo-direita: {down_right.to_algebraic()} (campo {down_right.field})")

# e5 = campo 15, então verificar qual movimento de d6 leva a 15
if down_left and down_left.field == 15:
    print(f"\n  d6 captura e5 via baixo-esquerda")
    jump = down_left.move_down_left()
    if jump:
        print(f"  Destino: {jump.to_algebraic()} (campo {jump.field})")
        captured_dest = jump.field
elif down_right and down_right.field == 15:
    print(f"\n  d6 captura e5 via baixo-direita")
    jump = down_right.move_down_right()
    if jump:
        print(f"  Destino: {jump.to_algebraic()} (campo {jump.field})")
        captured_dest = jump.field

print()
print(f"2. Pretas capturam: d6 x e5 → {Pos64(captured_dest).to_algebraic()}")

white2 = {30, 25, 26, 20}  # perdeu e5
black2 = black.copy()
black2.remove(10)  # d6 saiu
black2.add(captured_dest)  # d6 foi para destino

print_board(white2, black2, f"Após 2. d6 x e5 → {Pos64(captured_dest).to_algebraic()}:")

print("="*70)
print("3. AGORA É A VEZ DAS BRANCAS")
print("="*70)
print()

print("Verificando TODAS as capturas possíveis para as brancas:")
print()

captured_count = 0
for w_field in white2:
    pos_w = Pos64(w_field)
    w_alg = pos_w.to_algebraic()

    # Testar todas as direções de captura
    for direction, move_func, jump_func in [
        ("cima-esquerda", pos_w.move_up_left, lambda p: p.move_up_left()),
        ("cima-direita", pos_w.move_up_right, lambda p: p.move_up_right()),
    ]:
        adjacent = move_func()
        if adjacent and adjacent.field in black2:
            # Tem peça preta adjacente
            dest = jump_func(adjacent)
            if dest and dest.field not in white2 and dest.field not in black2:
                print(f"✓ {w_alg} x {adjacent.to_algebraic()} → {dest.to_algebraic()} ({direction})")
                captured_count += 1

                # VERIFICAR CAPTURA MÚLTIPLA!
                print(f"  Verificando se há captura múltipla de {dest.to_algebraic()}...")

                # Simular essa captura
                temp_white = white2.copy()
                temp_white.remove(w_field)
                temp_white.add(dest.field)

                temp_black = black2.copy()
                temp_black.remove(adjacent.field)

                # De dest, buscar mais capturas
                pos_dest = dest
                for dir2, move2, jump2 in [
                    ("cima-esq", pos_dest.move_up_left, lambda p: p.move_up_left()),
                    ("cima-dir", pos_dest.move_up_right, lambda p: p.move_up_right()),
                ]:
                    adj2 = move2()
                    if adj2 and adj2.field in temp_black:
                        dest2 = jump2(adj2)
                        if dest2 and dest2.field not in temp_white and dest2.field not in temp_black:
                            print(f"    ✓✓ CONTINUA: {dest.to_algebraic()} x {adj2.to_algebraic()} → {dest2.to_algebraic()}")

                            # Verificar mais uma vez
                            temp2_white = temp_white.copy()
                            temp2_white.remove(dest.field)
                            temp2_white.add(dest2.field)

                            temp2_black = temp_black.copy()
                            temp2_black.remove(adj2.field)

                            pos_dest2 = dest2
                            for dir3, move3, jump3 in [
                                ("cima-esq", pos_dest2.move_up_left, lambda p: p.move_up_left()),
                                ("cima-dir", pos_dest2.move_up_right, lambda p: p.move_up_right()),
                            ]:
                                adj3 = move3()
                                if adj3 and adj3.field in temp2_black:
                                    dest3 = jump3(adj3)
                                    if dest3 and dest3.field not in temp2_white and dest3.field not in temp2_black:
                                        print(f"      ✓✓✓ CONTINUA: {dest2.to_algebraic()} x {adj3.to_algebraic()} → {dest3.to_algebraic()}")

print()
if captured_count == 0:
    print("❌ Nenhuma captura encontrada para as brancas!")
    print("   Talvez as pretas tenham outra opção em vez de capturar?")
else:
    print(f"✅ Encontradas {captured_count} sequência(s) de captura!")
