"""
Exercise #23 - Tentativa com depth 16

Vamos tentar profundidade maior para encontrar a combinação.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64

print("=" * 70)
print("Exercise #23 - DEPTH 16")
print("=" * 70)
print()

# White pieces: d2, f2, b4, a5
white_men = {26, 27, 17, 13}  # d2, f2, b4, a5

# Black pieces: h4, d6, f6, b8
black_men = {20, 10, 11, 1}  # h4, d6, f6, b8

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("Exercise #23")

print()
print("Testando com depth 16...")
print()

motor = ProfessionalEngine(tt_size_mb=256)

best_move, score, pv = motor.search_best_move(game, max_depth=16, max_time_seconds=120)

print()
print("=" * 70)
print("RESULTADO DEPTH 16")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

if abs(score) >= 8000:
    print("✅✅✅ VITÓRIA FORÇADA ENCONTRADA! ✅✅✅")
elif score >= 500:
    print("✅ Grande vantagem encontrada!")
elif score > 0:
    print("⚠️  Pequena vantagem")
else:
    print("❌ Ainda não encontrou vitória")

print()
print("Variante principal:")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
