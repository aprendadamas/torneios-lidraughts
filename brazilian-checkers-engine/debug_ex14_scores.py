"""
Debug dos scores do Exercício #14
Verificar CUIDADOSAMENTE a lógica de inversão
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("DEBUG - Scores do Exercício #14")
print("=" * 70)
print()

white_men = {30, 27, 23, 18, 19, 20}
black_men = {21, 17, 11, 12, 6, 7}

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Turno: {game.turn}")
print()

# Testar f4 → g5
print("=" * 70)
print("Testando: f4 → g5")
print("=" * 70)
print()

test_game = game.copy()
test_game.make_move(19, 16, [], False)  # f4 (19) → g5 (16)

print(f"Após f4 → g5, turno é: {test_game.turn}")
print()

# Buscar com profundidade 16
engine = TacticalSearchEngine()
_, score, sequence = engine.search_best_move(test_game, max_depth=16)

print(f"Score retornado pelo motor: {score}")
print(f"Este é o score do ponto de vista de: {test_game.turn}")
print()

if test_game.turn == "black":
    print("Como é turno das PRETAS:")
    print(f"  Score positivo = bom para pretas = ruim para brancas")
    print(f"  Score negativo = ruim para pretas = bom para brancas")
    print()
    print(f"  Score das brancas = -{score} = {-score}")
elif test_game.turn == "white":
    print("Como é turno das BRANCAS:")
    print(f"  Score positivo = bom para brancas")
    print(f"  Score negativo = ruim para brancas")
    print()
    print(f"  Score das brancas = {score}")

print()
print("Sequência (primeiros 10 lances):")
for i, move in enumerate(sequence[:10], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("Testando TODOS os lances e ordenando corretamente")
print("=" * 70)
print()

moves = game.find_simple_moves()

results = []

for from_f, to_f, promotes in moves:
    notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
    if promotes:
        notation += " ♛"

    test_game = game.copy()
    test_game.make_move(from_f, to_f, [], promotes)

    engine = TacticalSearchEngine()
    _, score, _ = engine.search_best_move(test_game, max_depth=12)

    # Score é do ponto de vista das PRETAS (pois após lance das brancas, é turno delas)
    # Score NEGATIVO = ruim para pretas = BOM para brancas!
    # Então queremos o lance com MENOR score (mais negativo)

    results.append((notation, score))

print("Ordenando por score (do ponto de vista das PRETAS):")
print("Lembrando: score NEGATIVO é BOM para brancas!")
print()

results.sort(key=lambda x: x[1])

for notation, score in results:
    white_advantage = -score
    status = ""
    if white_advantage >= 9000:
        status = "✅ VITÓRIA FORÇADA BRANCAS!"
    elif white_advantage >= 500:
        status = "✅ Grande vantagem brancas"
    elif white_advantage >= 0:
        status = "⚠️  Pequena vantagem ou equilibrado"
    else:
        status = "❌ Vantagem pretas"

    print(f"{notation:15s} | Score pretas: {score:6d} | Vantagem brancas: {white_advantage:6d} | {status}")

print()
print("MELHOR LANCE PARA BRANCAS:")
best = results[0]  # Menor score das pretas = melhor para brancas
print(f"  {best[0]}")
print(f"  Score (ponto de vista pretas): {best[1]}")
print(f"  Vantagem brancas: {-best[1]}")
