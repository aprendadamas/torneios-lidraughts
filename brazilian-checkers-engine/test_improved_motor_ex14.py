"""
Testar motor tático melhorado v2 no Exercício #14
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("TESTE DO MOTOR TÁTICO MELHORADO V2 - EXERCÍCIO #14")
print("=" * 70)
print()

white_men = {30, 27, 23, 18, 19, 20}
black_men = {21, 17, 11, 12, 6, 7}

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Solução esperada: c1 → b2")
print()

# Testar em profundidades crescentes
for depth in [8, 10, 12]:
    print("=" * 70)
    print(f"PROFUNDIDADE {depth}")
    print("=" * 70)
    print()

    engine = ImprovedTacticalSearchEngine()
    best_move, score, sequence = engine.search_best_move(game, max_depth=depth)

    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score}")
    print(f"Nós pesquisados: {engine.nodes_searched}")
    print()

    if best_move == "c1 → b2":
        print("✅ MOTOR ENCONTROU A SOLUÇÃO CORRETA!")
    else:
        print(f"⚠️  Motor preferiu outro lance")

    print()
    print("Sequência (primeiros 10 lances):")
    for i, move in enumerate(sequence[:10], 1):
        print(f"  {i}. {move}")

    print()

# Testar especificamente c1→b2
print("=" * 70)
print("TESTE ESPECÍFICO: c1 → b2")
print("=" * 70)
print()

test_game = game.copy()
test_game.make_move(30, 26, [], False)  # c1 (30) → b2 (26)

engine = ImprovedTacticalSearchEngine()
_, score, sequence = engine.search_best_move(test_game, max_depth=12)

white_score = -score  # Inverter pois é turno das pretas

print(f"Score após c1→b2: {white_score}")
print(f"Nós pesquisados: {engine.nodes_searched}")
print()

if white_score >= 9000:
    print("✅ Motor reconhece que c1→b2 leva à vitória!")
elif white_score >= 500:
    print("✅ Motor vê grande vantagem")
elif white_score >= 0:
    print("⚠️  Motor vê pequena vantagem")
else:
    print(f"❌ Motor ainda avalia negativamente: {white_score}")

print()
print("Sequência após c1→b2:")
for i, move in enumerate(sequence[:10], 1):
    print(f"  {i}. {move}")
