"""
Teste Exercise #2 com profundidade MAIOR (depth 18-20)

Solução correta: 1. d6-e7 (não g3-h4)

Motor com depth 14 vê:
- d6-e7: score -515
- g3-h4: score -300

Mas d6-e7 é correto! Vou testar com depth maior.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Exercise #2 com depth 18")
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
print("Motor com depth 14 escolheu: g3-h4 (score -300)")
print("Motor com depth 14 avalia d6-e7: score -515")
print()
print("Testando com depth 18 para ver se encontra d6-e7...")
print()

motor = ProfessionalEngine(tt_size_mb=256)

best_move, score, pv = motor.search_best_move(game, max_depth=18, max_time_seconds=180)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

# Verificar se é d6-e7
if "d6" in best_move and "e7" in best_move:
    print("✅ MOTOR ENCONTROU d6-e7 com depth maior!")
    print()
    print("Isso confirma que depth 14 era insuficiente.")
elif "g3" in best_move and "h4" in best_move:
    print("❌ Motor ainda escolhe g3-h4 mesmo com depth 18")
    print()
    print("Isso indica que há um problema mais profundo na avaliação.")
else:
    print(f"⚠️  Motor escolheu movimento diferente: {best_move}")

print()
print("Variante principal (primeiros 14 lances):")
for i, move in enumerate(pv[:14], 1):
    print(f"  {i}. {move}")

print()

# Comparar com solução conhecida
print("=" * 70)
print("SOLUÇÃO CORRETA (do livro):")
print("=" * 70)
print()
print("1. d6-e7 a1xf6xd8xa5")
print("2. c5-d6 b4xe7")
print("3. e1-d2 a5xe1")
print("4. c1-b2 a3xc1")
print("5. g3-h4 e1xg3")
print("6. h2xf4 c1xg5")
print("7. h4xf6xd8 2-0")
print()
