"""
Verificar a solução do Exercício #17
Solução sugerida pelo motor: a3 → b4
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #17 - VERIFICAÇÃO DA SOLUÇÃO")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 28, 21, 24}  # c1, f2, h2, a3, g3
black_men = {13, 15, 11, 6}       # a5, e5, f6, c7
black_kings = {2}                  # d8

game = BrazilianGameComplete(white_men, black_men, set(), black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print("Solução sugerida pelo motor:")
print("1. a3 → b4 (sacrifício)")
print("2. a5 x b4 → c3")
print("3. c1 → d2 (segundo sacrifício)")
print("4. c3 x d2 → e1 ♛ (promove dama)")
print("5. g3 → h4 (lance intermediário)")
print("6. e1 x f2 → g3 (dama captura)")
print("7. h2 x g3 x e5 x c7 → b8 ♛ (captura tripla!)")
print()
print("=" * 70)
print()

move_count = 0

# Lance 1: a3 → b4
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam a3 → b4 (SACRIFÍCIO)")
game.make_move(21, 17, [], False)  # a3 (21) → b4 (17)
game.print_board(f"Após a3 → b4")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Verificar capturas
caps = game.find_all_captures()
if caps:
    print(f"Capturas obrigatórias para pretas: {len(caps)}")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation}")
print()

# Lance 2: a5 x b4 → c3
move_count += 1
print(f"Lance {move_count}: PRETAS capturam a5 x b4 → c3")
game.make_move(13, 22, [17], False)  # a5 (13) x b4 (17) → c3 (22)
game.print_board(f"Após a5 x b4 → c3")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Lance 3: c1 → d2 (segundo sacrifício)
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam c1 → d2 (SEGUNDO SACRIFÍCIO)")
game.make_move(30, 26, [], False)  # c1 (30) → d2 (26)
game.print_board(f"Após c1 → d2")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Verificar capturas
caps = game.find_all_captures()
if caps:
    print(f"Capturas obrigatórias para pretas:")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation}")
print()

# Lance 4: c3 x d2 → e1 ♛
move_count += 1
print(f"Lance {move_count}: PRETAS capturam c3 x d2 → e1 ♛ (PROMOVE DAMA)")
game.make_move(22, 32, [26], True)  # c3 (22) x d2 (26) → e1 (32), promove
game.print_board(f"Após c3 x d2 → e1 ♛")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print(f"Pretas agora têm {len(game.black_kings)} damas!")
print()

# Lance 5: g3 → h4
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam g3 → h4 (lance intermediário)")
game.make_move(24, 20, [], False)  # g3 (24) → h4 (20)
game.print_board(f"Após g3 → h4")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Verificar capturas para dama
caps = game.find_all_captures()
if caps:
    print(f"Capturas obrigatórias para pretas:")
    for cap in caps[:10]:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation}")
print()

# Lance 6: e1 x f2 → g3
move_count += 1
print(f"Lance {move_count}: PRETAS - dama captura e1 x f2 → g3")
# Encontrar captura que vai para g3
best_cap = None
for cap in caps:
    if Pos64(cap.to_field).to_algebraic() == "g3":
        best_cap = cap
        break

if best_cap:
    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    print(f"Executando: {notation}")

    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board(f"Após dama capturar")

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)
    print(f"Material: B={w_total} P={b_total}")
    print()

# Lance 7: h2 x g3 x e5 x c7 → b8 ♛ (CAPTURA TRIPLA!)
move_count += 1
print(f"Lance {move_count}: BRANCAS - CAPTURA TRIPLA!")

caps = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")

# Encontrar melhor captura
if caps:
    best_cap = max(caps, key=lambda c: len(c.captured_fields))

    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if best_cap.promotes:
        notation += " ♛"

    print()
    print(f"Executando: {notation}")
    print(f"Captura {len(best_cap.captured_fields)} peças!")

    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board(f"POSIÇÃO APÓS CAPTURA TRIPLA")

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)
    print(f"Material: B={w_total} P={b_total}")
    print()

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Lances totais: {move_count}")
print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print()

if b_total == 0:
    print("🏆 BRANCAS VENCERAM - Todas as peças pretas eliminadas!")
    print()
    print("✅ SOLUÇÃO VERIFICADA CORRETA!")
elif w_total > b_total + 1:
    print(f"✅ Brancas têm GRANDE VANTAGEM: +{w_total - b_total}")
    print("Posição vencedora!")
elif w_total > b_total:
    print(f"✅ Brancas têm pequena vantagem: +{w_total - b_total}")
else:
    print(f"Material: B={w_total} P={b_total}")
    if b_total > w_total:
        print(f"⚠️  Pretas têm vantagem: +{b_total - w_total}")

print()
print("=" * 70)
print("PADRÃO TÁTICO")
print("=" * 70)
print()

print("Este exercício usa o MESMO PADRÃO do Exercício #14 e #16:")
print()
print("1. DUPLO SACRIFÍCIO (a3→b4 e c1→d2)")
print("   - Entrega 2 peças!")
print("   - Força promoção da dama adversária")
print()
print("2. LANCE INTERMEDIÁRIO (g3→h4)")
print("   - Força a dama a capturar")
print("   - Coloca dama em posição vulnerável")
print()
print("3. CAPTURA TRIPLA (h2 x g3 x e5 x c7 → b8 ♛)")
print("   - Captura a dama recém-promovida")
print("   - Captura outras 2 peças")
print("   - Promove própria dama")
print("   - Vitória!")
