"""
Exercício #18 - Verificação da SOLUÇÃO COMPLETA
Sequência fornecida pelo usuário:
1. a5-b6 c7xa5
2. d2-e3 f4xd2
3. c3xe1 a5xc3
4. e1-d2 c3xe1xg3
5. h2xf4xd6xf8xh6
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - VERIFICAÇÃO DA SOLUÇÃO COMPLETA")
print("=" * 70)
print()

# Posição inicial
white_men = set()
for piece in ["d2", "f2", "h2", "c3", "b4", "h4", "a5"]:
    white_men.add(Pos64.from_algebraic(piece).field)

black_men = set()
for piece in ["f4", "e5", "c7", "e7", "g7", "b8", "d8"]:
    black_men.add(Pos64.from_algebraic(piece).field)

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL")

print()
print("Sequência fornecida:")
print("1. a5-b6 c7xa5")
print("2. d2-e3 f4xd2")
print("3. c3xe1 a5xc3")
print("4. e1-d2 c3xe1xg3")
print("5. h2xf4xd6xf8xh6")
print()
print("=" * 70)
print()

# Lance 1.1: a5 → b6
print("Lance 1.1: BRANCAS - a5 → b6 (PRIMEIRO SACRIFÍCIO)")
game.make_move(13, 9, [], False)  # a5 (13) → b6 (9)
game.print_board("Após a5 → b6")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 1.2: c7 x a5 (mas a notação diz c7xa5, então captura b6 e vai para a5)
print("Lance 1.2: PRETAS - c7 x b6 → a5")
game.make_move(6, 13, [9], False)  # c7 (6) x b6 (9) → a5 (13)
game.print_board("Após c7 x b6 → a5")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 2.1: d2 → e3
print("Lance 2.1: BRANCAS - d2 → e3 (SEGUNDO SACRIFÍCIO)")
game.make_move(26, 23, [], False)  # d2 (26) → e3 (23)
game.print_board("Após d2 → e3")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 2.2: f4 x d2
print("Lance 2.2: PRETAS - f4 x e3 → d2")
game.make_move(19, 26, [23], False)  # f4 (19) x e3 (23) → d2 (26)
game.print_board("Após f4 x e3 → d2")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 3.1: c3 x e1 (captura d2 e promove em e1)
print("Lance 3.1: BRANCAS - c3 x d2 → e1 ♛ (CAPTURA E PROMOVE)")
game.make_move(22, 31, [26], True)  # c3 (22) x d2 (26) → e1 (31), promove
game.print_board("Após c3 x d2 → e1 ♛")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print(f"Brancas têm {len(game.white_kings)} dama!")
print()

# Lance 3.2: a5 x c3
print("Lance 3.2: PRETAS - a5 x b4 → c3")
# Verificar onde está o peão preto (deve estar em a5=13)
# Capturar b4 (17) e ir para c3 (22)
game.make_move(13, 22, [17], False)  # a5 (13) x b4 (17) → c3 (22)
game.print_board("Após a5 x b4 → c3")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 4.1: e1 → d2 (dama se move)
print("Lance 4.1: BRANCAS - e1 → d2 (DAMA SE MOVE)")
game.make_move(31, 26, [], False)  # e1 (31) → d2 (26)
game.print_board("Após e1 → d2")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 4.2: c3 x e1 x g3 (CAPTURA DUPLA!)
print("Lance 4.2: PRETAS - c3 x d2 → e1 ♛ x f2 → g3 (CAPTURA DUPLA + PROMOVE)")
# c3 (22) captura d2 (26), vai para e1 (31), promove, depois captura f2 (27), vai para g3 (24)
game.make_move(22, 24, [26, 27], True)  # c3 (22) x d2,f2 → g3 (24), promove
game.print_board("Após c3 x d2 → e1 ♛ x f2 → g3")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print(f"Pretas promoveram dama em e1 e continuaram capturando!")
print()

# Lance 5: h2 x f4 x d6 x f8 x h6 (CAPTURA QUÁDRUPLA!!!)
print("Lance 5: BRANCAS - h2 x g3 x e5 x c7/e7 x ... (CAPTURA MÚLTIPLA)")
print()
print("Capturas disponíveis para brancas:")
caps = game.find_all_captures()
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")

# Procurar a captura que parte de h2 (28) e captura o máximo
best_cap = max(caps, key=lambda c: len(c.captured_fields))
notation = Pos64(best_cap.from_field).to_algebraic()
for cf in best_cap.captured_fields:
    notation += f" x {Pos64(cf).to_algebraic()}"
notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
if best_cap.promotes:
    notation += " ♛"

print()
print(f"Executando melhor captura: {notation}")
print(f"Captura {len(best_cap.captured_fields)} peças!")

game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
game.print_board("POSIÇÃO FINAL")

print()
print("=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print(f"  Brancas: {len(game.white_men)} peões + {len(game.white_kings)} damas")
print(f"  Pretas: {len(game.black_men)} peões + {len(game.black_kings)} damas")
print()

if w_total > b_total:
    print(f"✅ VITÓRIA PARA BRANCAS! (+{w_total - b_total})")
elif w_total == b_total:
    print("⚖️  EMPATE")
else:
    print(f"⚠️  Vantagem para pretas (+{b_total - w_total})")

print()
print("=" * 70)
print("PADRÃO TÁTICO")
print("=" * 70)
print()

print("Este exercício usa um padrão complexo:")
print("1. DUPLO SACRIFÍCIO (a5→b6 e d2→e3)")
print("2. Promoção com captura (c3xd2→e1♛)")
print("3. Troca de peças e promoção adversária")
print("4. CAPTURA MÚLTIPLA FINAL (h2 captura várias peças)")
print()
print("Similar ao Exercício #14 (duplo sacrifício)!")
