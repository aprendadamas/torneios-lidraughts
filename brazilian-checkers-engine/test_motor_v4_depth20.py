"""
Teste Motor V4 com depth 18-20

Talvez depth 16 não seja suficiente para ver o endgame final.
Vou testar com profundidades maiores.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Motor V4 com depth 18")
print("=" * 70)
print()

# Posição inicial Exercise #1
white_men = {22, 24, 20, 13, 15, 11}
white_kings = {29}
black_men = {14, 12}
black_kings = {30, 3}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Posição Inicial")

print()
print(f"Lance correto: a5→b6")
print(f"Motor precisa buscar profundamente para ver endgame +8500")
print()

motor = ProfessionalEngine(tt_size_mb=256)

print("Buscando com max_depth=18...")
print()

best_move, score, pv = motor.search_best_move(game, max_depth=18, max_time_seconds=120)

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
    print("SUCESSO! Motor V4 resolveu Exercise #1")
else:
    print(f"❌ Motor encontrou {best_move} em vez de a5→b6")

    if score > 5000:
        print(f"   Score {score:+.0f} indica vitória forçada")
        print(f"   Mas movimento está incorreto")
    elif score > 1000:
        print(f"   Score {score:+.0f} indica grande vantagem")
    else:
        print(f"   Score {score:+.0f} indica vantagem pequena")

print()
print("Variante principal (primeiros 12 lances):")
for i, move in enumerate(pv[:12], 1):
    print(f"  {i}. {move}")

print()
