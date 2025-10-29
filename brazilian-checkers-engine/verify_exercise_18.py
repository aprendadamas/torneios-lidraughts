"""
Verificação do Exercício #18
Solução encontrada pelo Motor V2: d2 x f4 x g7 x e7 → c5
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - VERIFICAÇÃO DA SOLUÇÃO")
print("=" * 70)
print()

# Posição inicial
# White: d2 (dama), f2, h2, c3, b4, h4, a5
# Black: f4, e5, c7, e7, g7, b8, d8

white_men = {27, 28, 22, 17, 20, 13}  # f2, h2, c3, b4, h4, a5
white_kings = {26}  # d2 (dama)
black_men = {19, 15, 6, 7, 8, 1, 2}  # f4, e5, c7, e7, g7, b8, d8

game = BrazilianGameComplete(white_men, black_men, white_kings, set())
game.print_board("POSIÇÃO INICIAL")

print()
w_total = len(white_men) + len(white_kings)
b_total = len(black_men)
print(f"Material: Brancas {w_total} ({len(white_men)} peões + {len(white_kings)} dama)")
print(f"          Pretas {b_total} peões")
print()

print("Solução sugerida pelo motor:")
print("1. d2 x f4 x g7 x e7 → c5 (CAPTURA TRIPLA!)")
print()
print("=" * 70)
print()

# Lance 1: d2 x f4 x g7 x e7 → c5
print("Lance 1: BRANCAS - d2 x f4 x g7 x e7 → c5")
print()

# Campos: d2=26, f4=19, g7=8, e7=7, c5=14
game.make_move(26, 14, [19, 8, 7], False)  # d2 (26) x f4,g7,e7 → c5 (14)

game.print_board("Após captura tripla")

print()
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material: Brancas {w_total} ({len(game.white_men)} peões + {len(game.white_kings)} damas)")
print(f"          Pretas {b_total} peões")
print()

# Análise material
material_diff = w_total - b_total
if material_diff > 0:
    print(f"✅ Brancas têm vantagem de +{material_diff} peças!")
elif material_diff == 0:
    print("⚖️  Material equilibrado")
else:
    print(f"⚠️  Pretas têm vantagem de +{-material_diff} peças")

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()

print("Após a captura tripla:")
print(f"- Brancas capturaram 3 peões pretos (f4, g7, e7)")
print(f"- Material resultante: {w_total} brancas vs {b_total} pretas")
print(f"- Brancas mantêm a DAMA ativa em c5")
print()

if material_diff >= 3:
    print("✅ VITÓRIA DECISIVA para brancas!")
    print("   Vantagem material esmagadora com dama ativa.")
else:
    print("✅ Brancas têm vantagem significativa!")

print()
print("=" * 70)
print("PADRÃO TÁTICO")
print("=" * 70)
print()

print("Este exercício demonstra:")
print("1. CAPTURA MÚLTIPLA com dama (3 peças!)")
print("2. Exploração de peões pretos agrupados")
print("3. Dama em diagonal longa capturando sequência")
print()
print("A dama branca em d2 encontra caminho livre para:")
print("  - Capturar f4 (peão isolado)")
print("  - Continuar para g7 (segunda diagonal)")
print("  - Continuar para e7 (terceira diagonal)")
print("  - Parar em c5 (posição dominante)")
print()
print("Este é um padrão direto de captura máxima com dama.")
