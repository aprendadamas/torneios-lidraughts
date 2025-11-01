"""
Verificar solução do Exercise #23

Solução correta: 1. f2-g3 h4xf2 2. d2-e3 f2xd4 3. b4-c5 d4xb6 4. a5xc7xe5xg7

Vamos verificar se o motor vê esta linha e qual o score.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64
import copy

print("=" * 70)
print("VERIFICANDO SOLUÇÃO Exercise #23")
print("=" * 70)
print()

# White pieces: d2, f2, b4, a5
white_men = {26, 27, 17, 13}  # d2=26, f2=27, b4=17, a5=13

# Black pieces: h4, d6, f6, b8
black_men = {20, 10, 11, 1}  # h4=20, d6=10, f6=11, b8=1

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("Posição Inicial")

print()
print("Solução correta:")
print("1. f2-g3 h4xf2")
print("2. d2-e3 f2xd4")
print("3. b4-c5 d4xb6")
print("4. a5xc7xe5xg7")
print()

# Lance 1: f2→g3
print("=" * 70)
print("APÓS 1. f2→g3")
print("=" * 70)

# f2 = field 27, g3 = field 24
game1 = copy.deepcopy(game)
game1.make_move(27, 24, [], False)
game1.print_board("Após f2 → g3")

motor1 = ProfessionalEngine(tt_size_mb=128)
best_move1, score1, pv1 = motor1.search_best_move(game1, max_depth=14, max_time_seconds=30)

print()
print(f"Melhor resposta das pretas: {best_move1}")
print(f"Score (perspectiva pretas): {score1:+.0f}")
print(f"Score (perspectiva brancas): {-score1:+.0f}")
print()

# Verificar se pretos jogam h4xf2
if "h4" in best_move1 and ("f2" in best_move1 or "x" in best_move1):
    print("✅ Pretos capturaram em f2 (correto!)")

    # Simular h4xf2 (h4=20 captura g3=24 para f2=27)
    print()
    print("=" * 70)
    print("APÓS 1...h4xg3xf2")
    print("=" * 70)

    game2 = copy.deepcopy(game1)
    game2.make_move(20, 27, [24], False)
    game2.print_board("Após h4 x g3 → f2")

    motor2 = ProfessionalEngine(tt_size_mb=128)
    best_move2, score2, pv2 = motor2.search_best_move(game2, max_depth=14, max_time_seconds=30)

    print()
    print(f"Melhor lance brancas: {best_move2}")
    print(f"Score: {score2:+.0f}")
    print()

    # Verificar se brancas jogam d2-e3
    if "d2" in best_move2 and "e3" in best_move2:
        print("✅ Brancas jogam d2-e3 (correto!)")
    else:
        print(f"⚠️  Motor escolhe {best_move2} em vez de d2-e3")
else:
    print(f"⚠️  Pretos jogam {best_move1} em vez de capturar em f2")

print()
print("=" * 70)
print("TESTE DIRETO: Busca na posição inicial com depth 18")
print("=" * 70)
print()

motor_full = ProfessionalEngine(tt_size_mb=256)
best_move_full, score_full, pv_full = motor_full.search_best_move(game, max_depth=18, max_time_seconds=60)

print()
print(f"Melhor lance depth 18: {best_move_full}")
print(f"Score: {score_full:+.0f}")
print()

if "f2" in best_move_full and "g3" in best_move_full:
    print("✅✅✅ MOTOR ENCONTROU f2-g3! ✅✅✅")
else:
    print(f"❌ Motor escolhe {best_move_full}")

print()
print("PV completo:")
for i, move in enumerate(pv_full[:10], 1):
    print(f"  {i}. {move}")

print()
