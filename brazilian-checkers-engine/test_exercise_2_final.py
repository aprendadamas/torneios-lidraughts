"""
Teste FINAL Exercise #2

Mudanças implementadas:
1. Bonus posicional: linha 7 = +250
2. Bonus de ordenação: avanço para linha 7 = +50.000 prioridade

d6-e7 agora tem PRIORIDADE MÁXIMA!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE FINAL - Exercise #2")
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
print("Solução correta: 1. d6-e7")
print()
print("Mudanças implementadas:")
print("  ✓ Bonus avaliação: linha 7 = +250 (era +20)")
print("  ✓ Bonus ordenação: avanço para linha 7 = +50k prioridade")
print()
print("→ d6-e7 será avaliado PRIMEIRO e tem +250 de valor!")
print()
print("Testando com depth 14...")
print()

motor = ProfessionalEngine(tt_size_mb=256)

best_move, score, pv = motor.search_best_move(game, max_depth=14, max_time_seconds=120)

print()
print("=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

# Verificar se é d6-e7
if "d6" in best_move and "e7" in best_move:
    print("=" * 70)
    print("✅✅✅ SUCESSO! Motor encontrou d6-e7! ✅✅✅")
    print("=" * 70)
    print()
    print("🎉🎉🎉 Exercise #2 RESOLVIDO! 🎉🎉🎉")
    print()
    if abs(score) > 5000:
        print(f"Score {score:+.0f} confirma vitória forçada!")
else:
    print(f"Motor escolheu: {best_move}")
    print()
    if "b6" in best_move:
        print("Motor ainda prefere b6 (também avança peão)")
    elif "g3" in best_move:
        print("Motor voltou ao movimento antigo g3-h4")

print()
print("Variante principal:")
for i, move in enumerate(pv[:12], 1):
    print(f"  {i}. {move}")

print()
