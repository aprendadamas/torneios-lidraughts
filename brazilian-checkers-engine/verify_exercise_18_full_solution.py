"""
Exercício #18 - Verificação COMPLETA da solução
Com regras corretas de damas brasileiras
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - SOLUÇÃO COMPLETA")
print("=" * 70)
print()

# Posição inicial
white_men = {26, 27, 28, 22, 17, 20, 13}  # d2, f2, h2, c3, b4, h4, a5
black_men = {19, 15, 6, 7, 8, 1, 2}  # f4, e5, c7, e7, g7, b8, d8

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL")
print()

# Lance 1: a5-b6 c7xa5
print("Lance 1: a5-b6 c7xa5")
game.make_move(13, 9, [], False)  # a5 → b6
game.make_move(6, 13, [9], False)  # c7 x b6 → a5
game.print_board("Após lance 1")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 2: d2-e3 f4xd2
print("Lance 2: d2-e3 f4xd2 (preta captura PARA TRÁS)")
game.make_move(26, 23, [], False)  # d2 → e3
game.make_move(19, 26, [23], False)  # f4 x e3 → d2
game.print_board("Após lance 2")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 3: c3xe1 a5xc3
print("Lance 3: c3xe1 a5xc3 (branca captura PARA TRÁS)")
game.make_move(22, 31, [26], False)  # c3 x d2 → e1 (SEM promoção - e1 não é linha de promoção para brancas)
game.make_move(13, 22, [17], False)  # a5 x b4 → c3
game.print_board("Após lance 3")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 4: e1-d2 c3xe1xg3
print("Lance 4: e1-d2 c3xe1xg3 (captura dupla SEM promoção)")
print("  Preta passa por e1 mas NÃO para = NÃO promove")
game.make_move(31, 26, [], False)  # e1 → d2
game.make_move(22, 24, [26, 27], False)  # c3 x d2 x f2 → g3 (SEM promoção!)
game.print_board("Após lance 4")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 5: h2 x g3 x e5 x e7 x g7 → h6 ♛
print("Lance 5: h2 x g3 x e5 x e7 x g7 → h6 ♛")
print("  Captura QUÁDRUPLA com promoção!")
print("  h2 (28) captura g3 (24), e5 (15), e7 (7), g7 (8)")
print("  Para em h6 (12, linha 8) = PROMOVE!")
print()

caps = game.find_all_captures()
print("Capturas disponíveis:")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} ({len(cap.captured_fields)} peças)")

# Executar a captura quádrupla
# h2 (28) x g3 (24) x e5 (15) x e7 (7) x g7 (8) → h6 (12)
game.make_move(28, 12, [24, 15, 7, 8], True)
print()
game.print_board("POSIÇÃO FINAL")

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print(f"  Brancas: {len(game.white_men)} peões + {len(game.white_kings)} damas")
print(f"  Pretas: {len(game.black_men)} peões + {len(game.black_kings)} damas")
print()

if w_total > b_total:
    print(f"✅ BRANCAS VENCEM! (+{w_total - b_total})")
elif w_total == b_total:
    print("⚖️  EMPATE")
else:
    print(f"⚠️  PRETAS VENCEM (+{b_total - w_total})")

print()
print("=" * 70)
print("PADRÃO TÁTICO")
print("=" * 70)
print()
print("Exercício #18 usa o padrão de DUPLO SACRIFÍCIO:")
print()
print("1. DUPLO SACRIFÍCIO (a5→b6 e d2→e3)")
print("   - Brancas entregam 2 peões")
print("   - Forçam posição específica")
print()
print("2. CAPTURAS PARA TRÁS")
print("   - c3 captura d2 para trás → e1")
print("   - Demonstra regra brasileira: capturas em todas direções")
print()
print("3. CAPTURA DUPLA PRETA sem promoção")
print("   - c3 x d2 x f2 → g3")
print("   - Passa por e1 mas não para = não promove")
print()
print("4. CAPTURA QUÁDRUPLA FINAL com promoção")
print("   - h2 x g3 x e5 x e7 x g7 → h6 ♛")
print("   - Captura 4 peças incluindo a dama preta")
print("   - Para em h6 (linha 8) = PROMOVE!")
print()
print("Similar ao Exercício #14: Duplo sacrifício para vitória!")
