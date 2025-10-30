"""
Comparar avaliações de d6-e7 vs b6-c7

Motor agora escolhe b6-c7 (score +20)
Livro diz que d6-e7 é correto
Vamos comparar os dois!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
import copy

print("=" * 70)
print("COMPARAÇÃO: d6-e7 vs b6-c7")
print("=" * 70)
print()

# Posição inicial
white_men = {9, 10, 14, 15, 24, 27, 28, 30, 31}
white_kings = set()
black_men = {8, 3, 12}
black_kings = {17, 21, 29}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Posição Inicial")

print()
print("=" * 70)
print("TESTE 1: Avaliar após d6-e7 (solução do livro)")
print("=" * 70)
print()

# d6 = field 10, e7 = field 7
game_d6e7 = copy.deepcopy(game)
game_d6e7.make_move(10, 7, [], False)
game_d6e7.print_board("Após d6 → e7")

motor1 = ProfessionalEngine(tt_size_mb=128)

print()
print("Buscando com depth 12...")
print()

best_move1, score1, pv1 = motor1.search_best_move(game_d6e7, max_depth=12, max_time_seconds=60)

print()
print(f"Melhor resposta das pretas: {best_move1}")
print(f"Score (perspectiva pretas): {score1:+.0f}")
print(f"Score (perspectiva brancas): {-score1:+.0f}")
print()

print()
print("=" * 70)
print("TESTE 2: Avaliar após b6-c7 (escolha atual do motor)")
print("=" * 70)
print()

# b6 = field 9, c7 = field 6
game_b6c7 = copy.deepcopy(game)
game_b6c7.make_move(9, 6, [], False)
game_b6c7.print_board("Após b6 → c7")

motor2 = ProfessionalEngine(tt_size_mb=128)

print()
print("Buscando com depth 12...")
print()

best_move2, score2, pv2 = motor2.search_best_move(game_b6c7, max_depth=12, max_time_seconds=60)

print()
print(f"Melhor resposta das pretas: {best_move2}")
print(f"Score (perspectiva pretas): {score2:+.0f}")
print(f"Score (perspectiva brancas): {-score2:+.0f}")
print()

print()
print("=" * 70)
print("COMPARAÇÃO FINAL")
print("=" * 70)
print()

print(f"Após d6-e7: score {-score1:+.0f} (brancas)")
print(f"Após b6-c7: score {-score2:+.0f} (brancas)")
print()

if -score1 > -score2:
    diff = (-score1) - (-score2)
    print(f"✅ d6-e7 é MELHOR por {diff:+.0f} pontos!")
    print()
    print("Conclusão: Motor deveria escolher d6-e7, não b6-c7")
elif -score1 < -score2:
    diff = (-score2) - (-score1)
    print(f"⚠️  b6-c7 é melhor por {diff:+.0f} pontos")
    print()
    print("Isso explica por que motor escolhe b6-c7")
else:
    print("Ambos têm score igual - posição pode transpor")

print()
print("Variantes:")
print()
print("Após d6-e7:")
for i, move in enumerate(pv1[:6], 1):
    print(f"  {i}. {move}")
print()
print("Após b6-c7:")
for i, move in enumerate(pv2[:6], 1):
    print(f"  {i}. {move}")
print()
