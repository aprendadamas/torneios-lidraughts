"""
Investigar: Por que motor não encontra d6-e7?

Solução correta do Exercise #2:
1. d6-e7 a1xf6xd8xa5
2. c5-d6 b4xe7
3. e1-d2 a5xe1
4. c1-b2 a3xc1
5. g3-h4 e1xg3
6. h2xf4 c1xg5
7. h4xf6xd8 2-0

Vou:
1. Forçar busca a partir de d6-e7
2. Ver se motor consegue ver vitória nesta linha
3. Comparar scores de d6-e7 vs g3-h4
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64
import copy

print("=" * 70)
print("INVESTIGAÇÃO: Exercise #2 - Por que não encontra d6-e7?")
print("=" * 70)
print()

# Posição inicial
white_men = {9, 10, 14, 15, 24, 27, 28, 30, 31}  # b6,d6,c5,e5,g3,f2,h2,c1,e1
white_kings = set()
black_men = {8, 3, 12}  # g7, f8, h6
black_kings = {17, 21, 29}  # b4, a3, a1

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Posição Inicial")

print()
print("=" * 70)
print("TESTE 1: Buscar a partir de d6-e7 (movimento correto)")
print("=" * 70)
print()

# Fazer d6-e7: d6(10) → e7(7)
game_after_d6e7 = copy.deepcopy(game)
game_after_d6e7.make_move(10, 7, [], False)

game_after_d6e7.print_board("Após d6-e7 (vez das pretas)")

motor = ProfessionalEngine(tt_size_mb=128)

print()
print("Buscando com depth 14 a partir de d6-e7...")
print()

best_move, score, pv = motor.search_best_move(game_after_d6e7, max_depth=14, max_time_seconds=60)

print()
print("RESULTADO após d6-e7:")
print(f"  Melhor lance para pretas: {best_move}")
print(f"  Score (perspectiva pretas): {score:+.0f}")
print()

if score < -5000:
    print("✓ Motor VÊ que pretas estão perdendo fortemente após d6-e7!")
    print(f"  Isso significa que d6-e7 é excelente para brancas")
elif score < -1000:
    print("⚠️  Motor vê desvantagem para pretas (score negativo)")
else:
    print(f"❌ Motor ainda vê posição aproximadamente igual (score {score:+.0f})")

print()
print("Variante após d6-e7:")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("TESTE 2: Buscar a partir de g3-h4 (movimento que motor escolheu)")
print("=" * 70)
print()

# Fazer g3-h4: g3(24) → h4(20)
game_after_g3h4 = copy.deepcopy(game)
game_after_g3h4.make_move(24, 20, [], False)

game_after_g3h4.print_board("Após g3-h4 (vez das pretas)")

motor2 = ProfessionalEngine(tt_size_mb=128)

print()
print("Buscando com depth 14 a partir de g3-h4...")
print()

best_move2, score2, pv2 = motor2.search_best_move(game_after_g3h4, max_depth=14, max_time_seconds=60)

print()
print("RESULTADO após g3-h4:")
print(f"  Melhor lance para pretas: {best_move2}")
print(f"  Score (perspectiva pretas): {score2:+.0f}")
print()

print()
print("=" * 70)
print("COMPARAÇÃO")
print("=" * 70)
print()

print(f"Score após d6-e7 (correto): {-score:+.0f} (perspectiva brancas)")
print(f"Score após g3-h4 (motor):   {-score2:+.0f} (perspectiva brancas)")
print()

if -score > -score2:
    print("✓ d6-e7 é MELHOR que g3-h4!")
    print(f"  Diferença: {(-score) - (-score2):+.0f} pontos")
    print()
    print("CONCLUSÃO: Motor está avaliando INCORRETAMENTE na raiz!")
    print("  - Motor vê que d6-e7 é melhor quando busca a partir dele")
    print("  - Mas escolhe g3-h4 na busca da raiz")
    print()
    print("Possíveis causas:")
    print("  1. Bug na ordenação de movimentos")
    print("  2. Poda agressiva cortando d6-e7 na raiz")
    print("  3. TT collision fazendo motor pular d6-e7")
else:
    print("❌ Motor avalia g3-h4 como melhor ou igual a d6-e7")
    print("  Isso indica problema na avaliação de posições")

print()
