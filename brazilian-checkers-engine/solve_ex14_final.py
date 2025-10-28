"""
Exercício #14 - Análise Final Correta
Com cuidado especial na inversão de scores
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - ANÁLISE FINAL")
print("=" * 70)
print()

white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Testando TODOS os movimentos com profundidade 12")
print("=" * 70)
print()

moves = game.find_simple_moves()

results = []

for from_f, to_f, promotes in sorted(moves):
    notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
    if promotes:
        notation += " ♛"

    # Fazer o lance
    test_game = game.copy()
    test_game.make_move(from_f, to_f, [], promotes)

    # Buscar com profundidade 12
    engine = TacticalSearchEngine()
    _, score, sequence = engine.search_best_move(test_game, max_depth=12)

    # O score retornado é do ponto de vista de quem vai jogar agora
    # Após o lance das brancas, é turno das pretas
    # Então score negativo é bom para brancas!
    # Inverter o score para ter o ponto de vista das brancas
    white_perspective_score = -score

    results.append((notation, white_perspective_score, engine.nodes_searched, sequence))

    status = ""
    if white_perspective_score >= 9000:
        status = "✅ VITÓRIA FORÇADA!"
    elif white_perspective_score >= 500:
        status = "✅ Grande vantagem"
    elif white_perspective_score >= 200:
        status = "⚠️  Pequena vantagem"
    elif white_perspective_score >= -200:
        status = "= Equilibrado"
    elif white_perspective_score >= -500:
        status = "⚠️  Pequena desvantagem"
    else:
        status = "❌ Grande desvantagem"

    print(f"{notation:15s} | Score: {white_perspective_score:6d} | Nós: {engine.nodes_searched:7d} | {status}")

print()
print("=" * 70)
print("MELHOR LANCE")
print("=" * 70)
print()

best = max(results, key=lambda x: x[1])
notation, score, nodes, sequence = best

print(f"Lance: {notation}")
print(f"Avaliação: {score}")
print(f"Nós pesquisados: {nodes}")
print()

if score >= 9000:
    print("✅ VITÓRIA FORÇADA ENCONTRADA!")
elif score >= 500:
    print("✅ Grande vantagem encontrada")
elif score >= 0:
    print("⚠️  Pequena vantagem ou equilibrado")
else:
    print("❌ Nenhum lance bom encontrado")

print()
print("Sequência principal (primeiros 12 lances):")
for i, move in enumerate(sequence[:12], 1):
    print(f"  {i}. {move}")

# Se não encontrou vitória, tentar profundidade maior no melhor lance
if score < 9000:
    print()
    print("=" * 70)
    print(f"BUSCA MAIS PROFUNDA - {notation} - Profundidade 16")
    print("=" * 70)
    print()

    # Executar o melhor lance
    parts = notation.split(" → ")
    if len(parts) == 2:
        from_alg = parts[0]
        to_alg = parts[1].replace(" ♛", "")

        from_f = Pos64.from_algebraic(from_alg).field
        to_f = Pos64.from_algebraic(to_alg).field
        promotes = "♛" in notation

        test_game = game.copy()
        test_game.make_move(from_f, to_f, [], promotes)

        engine = TacticalSearchEngine()
        _, score2, sequence2 = engine.search_best_move(test_game, max_depth=16)

        white_score2 = -score2

        print(f"Avaliação profundidade 16: {white_score2}")
        print(f"Nós pesquisados: {engine.nodes_searched}")
        print()

        if white_score2 >= 9000:
            print("✅ VITÓRIA FORÇADA CONFIRMADA!")
        elif white_score2 >= 500:
            print("✅ Grande vantagem confirmada")
        else:
            print("⚠️  Ainda não encontrou vitória clara")

        print()
        print("Sequência (primeiros 20 lances):")
        full_seq = [notation] + sequence2
        for i, move in enumerate(full_seq[:20], 1):
            print(f"  {i}. {move}")
