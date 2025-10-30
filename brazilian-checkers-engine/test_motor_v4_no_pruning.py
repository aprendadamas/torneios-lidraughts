"""
Teste Motor V4 SEM podas agressivas

Desabilitar null-move pruning para garantir que nenhuma
linha vencedora está sendo cortada incorretamente.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Motor V4 SEM null-move pruning")
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
print(f"Lance correto: a5→b6")
print()

motor = ProfessionalEngine(tt_size_mb=256)

# DESABILITAR null-move pruning
motor.use_null_move = False

print("⚠️  NULL-MOVE PRUNING DESABILITADO")
print("Buscando com max_depth=14 (sem podas agressivas)...")
print()

best_move, score, pv = motor.search_best_move(game, max_depth=14, max_time_seconds=120)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

if "a5" in best_move and "b6" in best_move:
    print("✅ MOTOR ENCONTROU a5→b6!")
    print()
    print("Isso significa que null-move pruning estava cortando a linha vencedora!")
else:
    print(f"❌ Motor ainda encontra {best_move} mesmo sem null-move pruning")
    print()
    print("Isso indica que o problema NÃO é poda agressiva.")
    print("Possibilidades restantes:")
    print("  1. Posição inicial está configurada incorretamente")
    print("  2. a5→b6 não é objetivamente o melhor lance")
    print("  3. Profundidade necessária é maior que 14")

print()
print("Variante principal:")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
