"""
Exercício #18 - Verificação com REGRAS CORRETAS
Regra aprendida: Peões podem capturar PARA TRÁS (não apenas para frente)!

Sequência:
1. a5-b6 c7xa5
2. d2-e3 f4xd2
3. c3xe1 a5xc3
4. e1-d2 c3xe1xg3
5. h2xf4xd6xf8xh6
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - VERIFICAÇÃO COM REGRAS CORRETAS")
print("=" * 70)
print()
print("REGRA IMPORTANTE: Peões capturam PARA FRENTE E PARA TRÁS!")
print("REGRA PROMOÇÃO: Só promove se PARA na linha de coroação")
print()

# Posição inicial
white_men = {26, 27, 28, 22, 17, 20, 13}  # d2, f2, h2, c3, b4, h4, a5
black_men = {19, 15, 6, 7, 8, 1, 2}  # f4, e5, c7, e7, g7, b8, d8

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL")

print()
print("Brancas promovem na LINHA 8")
print("Pretas promovem na LINHA 1")
print()
print("=" * 70)

# Lance 1.1: a5 → b6
print("\nLance 1.1: a5 → b6 (SACRIFÍCIO)")
game.make_move(13, 9, [], False)
game.print_board("Após a5 → b6")

# Lance 1.2: c7 x b6 → a5
print("\nLance 1.2: c7 x b6 → a5")
game.make_move(6, 13, [9], False)
game.print_board("Após c7 x b6 → a5")

# Lance 2.1: d2 → e3
print("\nLance 2.1: d2 → e3 (SEGUNDO SACRIFÍCIO)")
game.make_move(26, 23, [], False)
game.print_board("Após d2 → e3")

# Lance 2.2: f4 x e3 → d2
print("\nLance 2.2: f4 x e3 → d2 (captura PARA TRÁS!)")
game.make_move(19, 26, [23], False)
game.print_board("Após f4 x e3 → d2")

# Lance 3.1: c3 x d2 → e1
print("\nLance 3.1: c3 x d2 → e1 (captura PARA TRÁS!)")
print("  c3 (campo 22, linha 3) captura d2 (campo 26, linha 2)")
print("  Destino: e1 (campo 31, linha 1)")
print("  e1 NÃO é linha de promoção para brancas (seria linha 8)")
print("  Logo: NÃO promove!")

game.make_move(22, 31, [26], False)  # SEM promoção!
game.print_board("Após c3 x d2 → e1 (SEM promoção)")

# Lance 3.2: a5 x b4 → c3
print("\nLance 3.2: a5 x b4 → c3")
game.make_move(13, 22, [17], False)
game.print_board("Após a5 x b4 → c3")

# Lance 4.1: e1 → d2
print("\nLance 4.1: e1 → d2 (peão move)")
game.make_move(31, 26, [], False)
game.print_board("Após e1 → d2")

# Lance 4.2: c3 x d2 → e1 x f2 → g3
print("\nLance 4.2: c3 x d2 → e1 x f2 → g3 (CAPTURA DUPLA)")
print("  c3 (campo 22) captura d2 (campo 26) → e1 (campo 31)")
print("  e1 é linha 1 = PROMOVE para pretas!")
print("  MAS... continua capturando f2 (campo 27) → g3 (campo 24)")
print("  REGRA: Se não PARA em e1, NÃO promove!")
print("  Só promove se PARAR na linha de coroação")
print()
print("  Questão: A peça para em e1 ou continua direto para g3?")
print("  Se PARA em e1: Promove e depois captura como dama")
print("  Se NÃO para: Continua como peão")

# Vou assumir que NÃO para (continua capturando)
game.make_move(22, 24, [26, 27], False)  # SEM promoção!
game.print_board("Após c3 x d2 → e1 x f2 → g3 (SEM promoção - não parou em e1)")

# Lance 5: Captura múltipla
print("\nLance 5: Captura múltipla de brancas")
print("\nCapturas disponíveis:")
caps = game.find_all_captures()
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} ({len(cap.captured_fields)} peças)")

best_cap = max(caps, key=lambda c: len(c.captured_fields))
game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)

game.print_board("POSIÇÃO FINAL")

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
if w_total > b_total:
    print(f"✅ BRANCAS VENCEM (+{w_total - b_total})")
elif w_total == b_total:
    print("⚖️  EMPATE")
else:
    print(f"⚠️  PRETAS VENCEM (+{b_total - w_total})")

print()
print("=" * 70)
print("QUESTÃO PENDENTE:")
print("=" * 70)
print()
print("No lance 4.2, a peça preta:")
print("- PARA em e1 (promove) e depois captura f2 como dama?")
print("- OU continua direto sem parar (não promove)?")
print()
print("Isso muda completamente o resultado!")
