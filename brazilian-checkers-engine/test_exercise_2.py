"""
Teste: Motor V4 Profissional - Exercise #2

FEN: W:Wc1,e1,f2,h2,g3,c5,e5,b6,d6:BKa1,Ka3,Kb4,h6,g7,f8.

Brancas: 9 peões
Pretas: 3 damas + 3 peões

Resultado esperado: 2-0 (vitória das brancas)
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine

print("=" * 70)
print("TESTE: Motor V4 Profissional")
print("Exercício #2 - \"4800 Combinações - Avançado\"")
print("=" * 70)
print()

# Converter FEN para fields (mapeamento correto!)
# White pieces: c1,e1,f2,h2,g3,c5,e5,b6,d6
# c1=30, e1=31, f2=27, h2=28, g3=24, c5=14, e5=15, b6=9, d6=10
white_men = {9, 10, 14, 15, 24, 27, 28, 30, 31}
white_kings = set()

# Black pieces: Ka1,Ka3,Kb4,h6,g7,f8
# a1=29, a3=21, b4=17, h6=12, g7=8, f8=3
black_men = {8, 3, 12}  # g7, f8, h6
black_kings = {17, 21, 29}  # b4, a3, a1

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)

print()
print("POSIÇÃO INICIAL")
game.print_board("Lance #0 - Vez: white")
print()

print("Material:")
print(f"  Brancas: {len(white_men)} peões + {len(white_kings)} damas = {len(white_men) + len(white_kings)}")
print(f"  Pretas: {len(black_men)} peões + {len(black_kings)} damas = {len(black_men) + len(black_kings)}")
print()

print("=" * 70)
print("TESTE 1: Busca Profunda (max_depth=16)")
print("=" * 70)
print()

motor = ProfessionalEngine(tt_size_mb=256)

print("Buscando melhor lance...")
print()

best_move, score, pv = motor.search_best_move(game, max_depth=16, max_time_seconds=120)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()
print(f"Melhor lance: {best_move}")
print(f"Avaliação: {score:+.0f}")
print()

if abs(score) > 5000:
    print(f"✓ Motor encontrou vitória forçada! (score {score:+.0f})")
elif abs(score) > 1000:
    print(f"⚠️  Motor vê grande vantagem (score {score:+.0f})")
else:
    print(f"⚠️  Motor não vê vitória clara (score {score:+.0f})")

print()
print("Variante principal encontrada:")
for i, move in enumerate(pv[:14], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

if abs(score) > 5000:
    print("🎉 Motor V4 reconheceu combinação vencedora!")
    print()
    print("Características da posição:")
    print("- Brancas têm 9 peões")
    print("- Pretas têm 3 damas + 3 peões")
    print("- Motor viu sequência tática forçada")
else:
    print("Motor não encontrou vitória forçada ainda.")
    print("Pode precisar:")
    print("- Maior profundidade de busca")
    print("- Ajustes na avaliação")
    print("- Conhecimento específico deste tipo de posição")

print()
