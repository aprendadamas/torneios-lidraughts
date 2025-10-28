"""
Verificar a solução CORRETA do Exercício #14
Fornecida pelo usuário: c1-b2, a3xc1, d4-e5, f6xd4, e3xc5xa3, c1xg5, h4xf6xd8xb6
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - SOLUÇÃO CORRETA")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Solução fornecida:")
print("1. c1-b2 a3xc1")
print("2. d4-e5 f6xd4")
print("3. e3xc5xa3 c1xg5")
print("4. h4xf6xd8xb6 *")
print()
print("=" * 70)
print()

move_count = 0

# Lance 1: c1 → b2
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam c1 → b2")
print(f"  c1 = campo {Pos64.from_algebraic('c1').field}")
print(f"  b2 = campo {Pos64.from_algebraic('b2').field}")

game.make_move(30, 26, [], False)  # c1 (30) → b2 (26)
game.print_board(f"Após c1 → b2")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Verificar capturas
caps = game.find_all_captures()
print(f"Capturas obrigatórias para pretas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation}")
print()

# Lance 2: a3 x b2 → c1 ♛
move_count += 1
print(f"Lance {move_count}: PRETAS capturam a3 x b2 → c1 ♛")

# a3 = 21, b2 = 26, c1 = 30
game.make_move(21, 30, [26], True)
game.print_board(f"Após a3 x b2 → c1 ♛")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print(f"Pretas agora têm {len(game.black_kings)} dama(s)!")
print()

# Lance 3: d4 → e5
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam d4 → e5 (segundo sacrifício!)")

# d4 = 18, e5 = 15
game.make_move(18, 15, [], False)
game.print_board(f"Após d4 → e5")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Verificar capturas
caps = game.find_all_captures()
print(f"Capturas obrigatórias para pretas: {len(caps)}")
for cap in caps[:5]:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation}")
print()

# Lance 4: f6 x e5 → d4
move_count += 1
print(f"Lance {move_count}: PRETAS capturam f6 x e5 → d4")

# f6 = 11, e5 = 15, d4 = 18
game.make_move(11, 18, [15], False)
game.print_board(f"Após f6 x e5 → d4")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print("Brancas entregaram 2 peças! Parece desastroso...")
print()

# Lance 5: e3 x ... → a3 (captura múltipla)
move_count += 1
print(f"Lance {move_count}: BRANCAS capturam e3 x c5 x a3 (captura dupla!)")

# Verificar capturas disponíveis
caps = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")

# Encontrar e executar a captura e3 x ... x a3
best_cap = None
for cap in caps:
    if cap.from_field == 23 and cap.to_field == 21:  # e3 → a3
        best_cap = cap
        break

if best_cap:
    print()
    print(f"Executando: e3 x {' x '.join([Pos64(cf).to_algebraic() for cf in best_cap.captured_fields])} → a3")
    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board(f"Após captura múltipla")

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)
    print(f"Material: B={w_total} P={b_total}")
    print()

# Lance 6: c1 x g5 (dama captura)
move_count += 1
print(f"Lance {move_count}: PRETAS - dama captura")

# Verificar capturas da dama
caps = game.find_all_captures()
print(f"Capturas obrigatórias para pretas: {len(caps)}")
for cap in caps[:10]:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation}")

# Executar captura que vai para g5
best_cap = None
for cap in caps:
    if Pos64(cap.to_field).to_algebraic() == "g5":
        best_cap = cap
        break

if best_cap:
    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"

    print()
    print(f"Executando: {notation}")
    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board(f"Após dama capturar")

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)
    print(f"Material: B={w_total} P={b_total}")
    print()

# Lance 7: h4 x f6 x d8 x b6 (CAPTURA TRIPLA!)
move_count += 1
print(f"Lance {move_count}: BRANCAS - CAPTURA TRIPLA!")

# Verificar capturas disponíveis
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

# Encontrar a melhor captura (mais peças)
if caps:
    best_cap = max(caps, key=lambda c: len(c.captured_fields))

    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    if best_cap.promotes:
        notation += " ♛"

    print()
    print(f"Executando: {notation}")
    print(f"Captura {len(best_cap.captured_fields)} peças!")

    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board(f"POSIÇÃO FINAL")

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
else:
    print(f"Material: B={w_total} P={b_total}")

print()
print("=" * 70)
print("ANÁLISE DA SOLUÇÃO")
print("=" * 70)
print()

print("Padrão tático:")
print("1. DUPLO SACRIFÍCIO (c1→b2 e d4→e5)")
print("   - Entrega 2 peças!")
print("   - Força adversário a promover dama em c1")
print("   - Força capturas específicas")
print()
print("2. CAPTURA DUPLA (e3 x c5 x a3)")
print("   - Recupera material")
print("   - Abre linha para próxima captura")
print()
print("3. DAMA CAPTURA (c1 x ... → g5)")
print("   - Dama preta captura mas vai para posição vulnerável")
print()
print("4. CAPTURA TRIPLA COM PROMOÇÃO (h4 x f6 x d8 x b6 ♛)")
print("   - Captura 3 peças incluindo a dama!")
print("   - Promove nova dama")
print("   - Vitória!")
print()

print("Este é um padrão MUITO DIFÍCIL de encontrar porque:")
print("- Requer ver 7 lances à frente")
print("- Dois sacrifícios consecutivos parecem desastrosos")
print("- Após lance 4, brancas estão -2 em material")
print("- Apenas no lance 7 a vitória se materializa")
