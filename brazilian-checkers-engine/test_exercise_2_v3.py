"""
Teste Exercise #2 - Versão 3 (bonus +250 para linha 7)

Agora peões na linha 7 ganham +250 (era +150)
d6-e7 deve ganhar +170 de bonus posicional!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE Exercise #2 - V3 (bonus máximo para peões avançados)")
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
print("Bonus posicional:")
print("  Linha 7 (y=2): +250")
print("  Linha 6 (y=3): +80")
print("  → d6-e7 ganha +170 de bonus!")
print()
print("Testando com depth 16...")
print()

motor = ProfessionalEngine(tt_size_mb=256)

best_move, score, pv = motor.search_best_move(game, max_depth=16, max_time_seconds=180)

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
    print("✅✅✅ SUCESSO! Motor encontrou d6-e7! ✅✅✅")
    print()
    print("🎉 Exercise #2 RESOLVIDO! 🎉")
    print()
elif "b6" in best_move and ("c7" in best_move or "a7" in best_move):
    print(f"⚠️  Motor escolheu {best_move} em vez de d6-e7")
    print()
    print("Ambos avançam peões, mas livro prefere d6-e7")
elif "g3" in best_move and "h4" in best_move:
    print("❌ Motor voltou a escolher g3-h4")
else:
    print(f"⚠️  Motor escolheu: {best_move}")

print()
print("Variante principal (primeiros 10 lances):")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
