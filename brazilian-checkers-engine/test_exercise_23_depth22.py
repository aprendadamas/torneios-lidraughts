"""
Exercise #23 - Depth 22 (última tentativa)

O motor vê f2→g3 em depths baixos mas abandona porque não vê
profundo o suficiente para ver a vitória no lance 4.

Vamos tentar depth 22 para ver a combinação completa.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("Exercise #23 - DEPTH 22 (Teste Final)")
print("=" * 70)
print()

# White pieces: d2, f2, b4, a5
white_men = {26, 27, 17, 13}

# Black pieces: h4, d6, f6, b8
black_men = {20, 10, 11, 1}

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("Exercise #23")

print()
print("Solução: 1. f2-g3 h4xf2 2. d2-e3 f2xd4 3. b4-c5 d4xb6 4. a5xc7xe5xg7")
print()
print("Problema: Motor vê f2-g3 em depth 6-10, mas abandona em depth 11+")
print("          porque vê desvantagem material antes da vitória final.")
print()
print("Testando depth 22 para ver combinação completa...")
print()

motor = ProfessionalEngine(tt_size_mb=512)

best_move, score, pv = motor.search_best_move(game, max_depth=22, max_time_seconds=180)

print()
print("=" * 70)
print("RESULTADO DEPTH 22")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Score: {score:+.0f}")
print()

if "f2" in best_move and "g3" in best_move:
    print("✅✅✅ SUCESSO! Motor encontrou f2-g3! ✅✅✅")
    if abs(score) >= 8000:
        print("✅ E viu vitória forçada!")
else:
    print(f"❌ Motor ainda escolhe {best_move}")
    print()
    print("Conclusão: Combinação muito profunda para motor atual.")
    print("Precisa de melhorias na avaliação de sacrifícios táticos.")

print()
print("Variante principal:")
for i, move in enumerate(pv[:8], 1):
    print(f"  {i}. {move}")

print()
