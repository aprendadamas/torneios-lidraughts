"""
Exercise #21 - 1800 Combinações (Básico ao Avançado)

FEN: W:Wc3,g3,h4,g5:Bc5,e5,e7,f8.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64

print("=" * 70)
print("Exercise #21 - 1800 Combinações (Básico ao Avançado)")
print("=" * 70)
print()

# Converter FEN para fields
print("Convertendo FEN: W:Wc3,g3,h4,g5:Bc5,e5,e7,f8.")
print()

# White pieces: c3, g3, h4, g5
white_positions = ["c3", "g3", "h4", "g5"]
white_men = set()
for pos in white_positions:
    field = Pos64.from_algebraic(pos).field
    white_men.add(field)
    print(f"  White {pos} → field {field}")

print()

# Black pieces: c5, e5, e7, f8
black_positions = ["c5", "e5", "e7", "f8"]
black_men = set()
for pos in black_positions:
    field = Pos64.from_algebraic(pos).field
    black_men.add(field)
    print(f"  Black {pos} → field {field}")

print()
print(f"White men: {white_men}")
print(f"Black men: {black_men}")
print()

# Criar posição
game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("Posição Inicial - Exercise #21")

print()
print("Testando com Motor V4 (depth 12)...")
print()

motor = ProfessionalEngine(tt_size_mb=128)

best_move, score, pv = motor.search_best_move(game, max_depth=12, max_time_seconds=60)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

if abs(score) >= 8000:
    print("✅ Motor encontrou vitória forçada!")
elif score > 500:
    print("✅ Motor encontrou grande vantagem")
elif score > 0:
    print("⚠️  Motor encontrou pequena vantagem")
else:
    print("❌ Motor não vê vantagem")

print()
print("Variante principal:")
for i, move in enumerate(pv[:8], 1):
    print(f"  {i}. {move}")

print()
