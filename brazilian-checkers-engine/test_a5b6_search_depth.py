"""
Teste: Motor consegue VER o endgame favorável ao buscar em a5→b6?

Vou forçar o motor a buscar APENAS a partir de a5→b6 e ver:
1. Qual score ele retorna?
2. Ele consegue ver a posição de endgame +8500?
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64
import copy

print("=" * 70)
print("TESTE: Busca profunda a partir de a5→b6")
print("=" * 70)
print()

# Posição inicial
white_men = {22, 24, 20, 13, 15, 11}
white_kings = {29}
black_men = {14, 12}
black_kings = {30, 3}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Posição Inicial")

print()
print("Fazer o lance a5→b6...")
game_after_a5b6 = copy.deepcopy(game)
game_after_a5b6.make_move(13, 9, [], False)  # a5(13) → b6(9)

game_after_a5b6.print_board("Após a5→b6 (vez das pretas)")

print()
print("=" * 70)
print("Buscar com Motor V4 a partir desta posição")
print("=" * 70)
print()

motor = ProfessionalEngine(tt_size_mb=128)

print("Buscando depth 14...")
best_move, score, pv = motor.search_best_move(game_after_a5b6, max_depth=14)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print(f"Melhor lance para pretas: {best_move}")
print(f"Score (perspectiva pretas): {score:+.0f}")
print()

if score < -5000:
    print("✓ Motor VÊ que pretas estão perdendo gravemente!")
    print(f"  Score {score:+.0f} indica posição muito ruim para pretas")
elif score < -1000:
    print("⚠️  Motor vê desvantagem para pretas mas não catastrófica")
    print(f"  Score {score:+.0f}")
else:
    print("❌ Motor NÃO vê que pretas estão perdendo")
    print(f"  Score {score:+.0f} indica posição aproximadamente igual")

print()
print("Variante principal (primeiros 10 lances):")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

if score < -5000:
    print("Se motor vê score muito negativo após a5→b6, então:")
    print("- Motor CONSEGUE avaliar corretamente esta linha")
    print("- Problema é na RAIZ: motor prefere g3→f4")
    print()
    print("Próximo passo: comparar score de g3→f4 vs a5→b6 na raiz")
else:
    print("Motor NÃO está vendo o endgame favorável.")
    print("Possíveis causas:")
    print("- Profundidade 14 não é suficiente")
    print("- Poda agressiva cortando a linha vencedora")
    print("- Endgame evaluator não sendo chamado")

print()
