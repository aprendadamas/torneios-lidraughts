"""
Teste Exercise #2 com depth 22 (teste final de profundidade)

Se depth 22 não encontrar d6-e7, então o problema NÃO é profundidade.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE FINAL: Exercise #2 com depth 22")
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
print("Testando com depth 22 (teste definitivo)...")
print("Isso pode levar vários minutos...")
print()

motor = ProfessionalEngine(tt_size_mb=512)  # Mais memória para depths maiores

best_move, score, pv = motor.search_best_move(game, max_depth=22, max_time_seconds=600)

print()
print("=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

# Verificar resultado
if "d6" in best_move and "e7" in best_move:
    print("✅✅✅ SUCESSO! Motor encontrou d6-e7 com depth 22! ✅✅✅")
    print()
    print("Isso confirma que depth 16-18 era insuficiente.")
elif "g3" in best_move and "h4" in best_move:
    print("❌ Motor AINDA escolhe g3-h4 mesmo com depth 22")
    print()
    print("Conclusão: O problema NÃO é profundidade insuficiente.")
    print()
    print("O motor precisa de conhecimento tático adicional ou")
    print("há algo fundamentalmente diferente nesta posição que")
    print("requer abordagem especializada.")
else:
    print(f"⚠️  Motor escolheu: {best_move}")

print()
print("Variante (primeiros 14 lances):")
for i, move in enumerate(pv[:14], 1):
    print(f"  {i}. {move}")

print()
