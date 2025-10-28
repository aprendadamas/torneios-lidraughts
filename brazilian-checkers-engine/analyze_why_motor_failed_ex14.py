"""
Analisar por que o motor tático não encontrou c1→b2 no Exercício #14
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("ANÁLISE: Por que o motor não encontrou c1→b2?")
print("=" * 70)
print()

white_men = {30, 27, 23, 18, 19, 20}
black_men = {21, 17, 11, 12, 6, 7}

game = BrazilianGameComplete(white_men, black_men)

print("Testando TODOS os lances em múltiplas profundidades...")
print()

moves = list(game.find_simple_moves())

# Testar em profundidades crescentes
for depth in [6, 8, 10, 12, 14]:
    print("=" * 70)
    print(f"PROFUNDIDADE {depth}")
    print("=" * 70)
    print()

    results = []

    for from_f, to_f, promotes in moves:
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"

        test_game = game.copy()
        test_game.make_move(from_f, to_f, [], promotes)

        engine = TacticalSearchEngine()
        _, score, _ = engine.search_best_move(test_game, max_depth=depth)

        # Score do ponto de vista das brancas (inverter pois é turno das pretas)
        white_score = -score

        results.append((notation, white_score, engine.nodes_searched))

    # Ordenar por score
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"{'Lance':<15} | {'Score':>8} | {'Nós':>10} | Resultado")
    print("-" * 70)

    for notation, score, nodes in results:
        status = ""
        if notation == "c1 → b2":
            status = " ← SOLUÇÃO CORRETA!"
        elif score >= 9000:
            status = " (vitória forçada)"
        elif score >= 500:
            status = " (grande vantagem)"

        print(f"{notation:<15} | {score:8d} | {nodes:10d} | {status}")

    # Destacar onde c1→b2 está no ranking
    c1b2_result = next((r for r in results if r[0] == "c1 → b2"), None)
    if c1b2_result:
        rank = results.index(c1b2_result) + 1
        print()
        print(f"c1→b2 está em {rank}º lugar de {len(results)}")
        print(f"Score: {c1b2_result[1]}")
        print()

        if rank == 1:
            print("✅ Motor encontrou a solução correta!")
        else:
            best = results[0]
            print(f"Motor preferiu: {best[0]} (score: {best[1]})")
            diff = best[1] - c1b2_result[1]
            print(f"Diferença de avaliação: {diff} pontos")

    print()

print()
print("=" * 70)
print("CONCLUSÕES")
print("=" * 70)
print()

print("Testando c1→b2 especificamente com profundidade 16...")
test_game = game.copy()
test_game.make_move(30, 26, [], False)  # c1 → b2

engine = TacticalSearchEngine()
_, score, sequence = engine.search_best_move(test_game, max_depth=16)
white_score = -score

print(f"Score após c1→b2: {white_score}")
print(f"Nós pesquisados: {engine.nodes_searched}")
print()

if white_score >= 9000:
    print("✅ Com profundidade 16, o motor reconhece que c1→b2 leva à vitória!")
elif white_score >= 500:
    print("✅ Com profundidade 16, o motor vê grande vantagem")
else:
    print(f"⚠️  Mesmo com prof. 16, score é apenas {white_score}")

print()
print("Sequência prevista após c1→b2 (primeiros 10 lances):")
for i, move in enumerate(sequence[:10], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("ANÁLISE DO PROBLEMA")
print("=" * 70)
print()

print("Este exercício é extremamente difícil porque:")
print()
print("1. DUPLO SACRIFÍCIO:")
print("   - c1→b2 entrega uma peça")
print("   - d4→e5 entrega outra peça")
print("   - Após 4 lances, brancas estão -2 em material")
print()
print("2. PROFUNDIDADE NECESSÁRIA:")
print("   - Solução tem 7 lances")
print("   - Motor precisa ver TODOS os 7 lances")
print("   - Com variantes, pode precisar prof. 12-16")
print()
print("3. AVALIAÇÃO INTERMEDIÁRIA RUIM:")
print("   - Após lance 2: B=5 P=6 (dama preta!)")
print("   - Após lance 4: B=4 P=6 (-2 material)")
print("   - Só no lance 7 vence")
print()
print("4. PADRÃO TÁTICO COMPLEXO:")
print("   - Dois sacrifícios forçam movimentos específicos")
print("   - Captura múltipla no meio")
print("   - Captura final com promoção")
print()

print("MELHORIAS NECESSÁRIAS NO MOTOR:")
print()
print("1. Aumentar bônus para sequências de sacrifícios")
print("2. Reconhecer padrões de 'sacrifício duplo'")
print("3. Avaliar melhor posições com capturas múltiplas futuras")
print("4. Buscar mais profundamente em linhas com múltiplos sacrifícios")
print("5. Dar bônus extra para capturas que incluem damas")
