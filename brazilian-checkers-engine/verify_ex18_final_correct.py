"""
Exercício #18 - Verificação FINAL CORRETA
Com notação e regras corretas
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

# Executar lances 1-4 rapidamente
print("Executando lances 1-4...")
game.make_move(13, 9, [], False)      # 1.1 a5 → b6
game.make_move(6, 13, [9], False)     # 1.2 c7 x b6 → a5
game.make_move(26, 23, [], False)     # 2.1 d2 → e3
game.make_move(19, 26, [23], False)   # 2.2 f4 x e3 → d2
game.make_move(22, 31, [26], False)   # 3.1 c3 x d2 → e1
game.make_move(13, 22, [17], False)   # 3.2 a5 x b4 → c3
game.make_move(31, 26, [], False)     # 4.1 e1 → d2
game.make_move(22, 24, [26, 27], False)  # 4.2 c3 x d2 x f2 → g3
print()

game.print_board("Posição antes do lance 5")

print()
print("Peças:")
print("  Brancas: h2, h4")
print("  Pretas: b8, d8, e5, e7, g7, g3 (peão)")
print()

print("=" * 70)
print("LANCE 5: h2xf4xd6xf8xh6")
print("=" * 70)
print()
print("Notação: mostra as CASAS por onde a peça passa")
print("  h2 → f4 → d6 → f8 → h6")
print()
print("Peças capturadas (não aparecem na notação):")
print("  - Entre h2 e f4: g3 (campo 24)")
print("  - Entre f4 e d6: e5 (campo 15)")
print("  - Entre d6 e f8: e7 (campo 7)")
print("  - Entre f8 e h6: g7 (campo 8)")
print()
print("Total: 4 peças capturadas")
print()

# Campos: h2=28, f4=19, d6=10, f8=3, h6=12
# Capturas: g3=24, e5=15, e7=7, g7=8

print("Executando manualmente (motor tem bug):")
print("  h2 (28) captura [24, 15, 7, 8] → h6 (12)")
print()

# h6 = campo 12 (linha 6, NÃO é linha de coroação)
# Portanto: NÃO promove
game.make_move(28, 12, [24, 15, 7, 8], False)  # SEM promoção!

game.print_board("POSIÇÃO FINAL")

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"\nMaterial final: Brancas {w_total} vs Pretas {b_total}")
print(f"  Brancas: {len(game.white_men)} peões + {len(game.white_kings)} damas")
print(f"  Pretas: {len(game.black_men)} peões + {len(game.black_kings)} damas")
print()

print("Peças finais:")
for f in sorted(game.white_men):
    print(f"  Branca peão: {Pos64(f).to_algebraic()} (campo {f})")
for f in sorted(game.white_kings):
    print(f"  Branca dama: {Pos64(f).to_algebraic()} (campo {f})")
for f in sorted(game.black_men):
    print(f"  Preta peão: {Pos64(f).to_algebraic()} (campo {f})")

print()
if w_total > b_total:
    print(f"✅ BRANCAS VENCEM! (+{w_total - b_total})")
elif w_total == b_total:
    print("⚖️  MATERIAL EMPATE")
else:
    print(f"⚠️  PRETAS VENCEM (+{b_total - w_total})")

print()
print("=" * 70)
print("REGRA APRENDIDA")
print("=" * 70)
print()
print("Regra FMJD sobre promoção durante multi-captura:")
print()
print("1. Se peão alcança linha de coroação E pode continuar")
print("   capturando 'no mesmo curso' (como peão):")
print("   → CONTINUA SEM PROMOVER")
print()
print("2. Se só pode continuar com movimentos de dama:")
print("   → PROMOVE e PARA")
print()
print("Neste exercício:")
print("  - h2 alcança f8 (linha 8)")
print("  - Pode continuar capturando g7 como peão (adjacente)")
print("  - Logo: CONTINUA SEM PROMOVER")
print("  - Para em h6 (linha 6) como PEÃO")
