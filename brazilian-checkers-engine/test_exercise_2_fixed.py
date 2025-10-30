"""
Teste Exercise #2 COM correção na lógica de validação de scores

Correção: SEMPRE aceitar scores ±5000+ (endgame scores)
independente de mudanças extremas.

Isso deve permitir que motor veja vitória em d6-e7.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Exercise #2 COM CORREÇÃO")
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
print("Motor ANTES da correção escolhia: g3-h4")
print()
print("Testando com depth 16 APÓS correção...")
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
    print("SUCESSO! Correção funcionou!")
    print()
    if abs(score) > 5000:
        print(f"Score {score:+.0f} indica vitória forçada para brancas!")
elif "g3" in best_move and "h4" in best_move:
    print("❌ Motor ainda escolhe g3-h4")
    print()
    print("Correção não foi suficiente. Vou tentar depth maior.")
else:
    print(f"⚠️  Motor escolheu movimento diferente: {best_move}")

print()
print("Variante principal (primeiros 14 lances):")
for i, move in enumerate(pv[:14], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("SOLUÇÃO ESPERADA:")
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
