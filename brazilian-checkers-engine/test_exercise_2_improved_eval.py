"""
Teste Exercise #2 COM avaliação melhorada de peões avançados

Mudança: Peões na linha 7 ganham +150 (era +20)
Isso deve fazer d6-e7 muito mais atraente!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Exercise #2 COM AVALIAÇÃO MELHORADA")
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
print("Motor ANTES da melhoria escolhia: g3-h4")
print()
print("Mudança: Peões na linha 7 agora ganham +150 (era +20)")
print("         Peões na linha 6 agora ganham +50 (era +20)")
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
    print("✅✅✅ MOTOR ENCONTROU d6-e7! ✅✅✅")
    print()
    print("SUCESSO! Avaliação melhorada funcionou!")
    print()
    if abs(score) > 5000:
        print(f"Score {score:+.0f} indica vitória forçada para brancas!")
elif "g3" in best_move and "h4" in best_move:
    print("❌ Motor ainda escolhe g3-h4")
    print()
    print("Melhoria não foi suficiente. Preciso aumentar mais o bonus.")
else:
    print(f"⚠️  Motor escolheu movimento diferente: {best_move}")

print()
print("Variante principal (primeiros 10 lances):")
for i, move in enumerate(pv[:10], 1):
    print(f"  {i}. {move}")

print()
