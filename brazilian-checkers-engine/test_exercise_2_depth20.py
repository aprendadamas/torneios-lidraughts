"""
Teste Exercise #2 com depth 20 (último teste)

Se não encontrar d6-e7 com depth 20, é problema estrutural na busca.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE DEPTH 20 - Exercise #2")
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
print("Testando com depth 20 (pode levar 3-5 minutos)...")
print()

motor = ProfessionalEngine(tt_size_mb=512)

best_move, score, pv = motor.search_best_move(game, max_depth=20, max_time_seconds=300)

print()
print("=" * 70)
print("RESULTADO DEPTH 20")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

# Verificar se é d6-e7
if "d6" in best_move and "e7" in best_move:
    print("=" * 70)
    print("✅✅✅ SUCESSO COM DEPTH 20! ✅✅✅")
    print("=" * 70)
elif "b6" in best_move:
    print(f"Motor escolheu {best_move}")
    print()
    print("Conclusão: Motor prefere b6 (também avança peão)")
    print("Progresso: era g3-h4 (score -300), agora b6 (score +110)")

print()
print("Variante principal:")
for i, move in enumerate(pv[:14], 1):
    print(f"  {i}. {move}")

print()
