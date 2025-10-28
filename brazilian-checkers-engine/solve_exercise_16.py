"""
Exercício #16 - 1800 Combinações
FEN: W:Wc1,f2,h2,g3:Bc3,e5,c7,d8.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #16")
print("=" * 70)
print()

# Parsear FEN: W:Wc1,f2,h2,g3:Bc3,e5,c7,d8.
# Brancas (men): c1, f2, h2, g3
# Pretas (men): c3, e5, c7
# Pretas (king): d8 (indicado pelo ponto final)

white_alg = ["c1", "f2", "h2", "g3"]
black_men_alg = ["c3", "e5", "c7"]
black_kings_alg = ["d8"]

print("Convertendo posição...")
white_men = set()
for alg in white_alg:
    pos = Pos64.from_algebraic(alg)
    white_men.add(pos.field)
    print(f"  Branca: {alg} → campo {pos.field}")

print()
black_men = set()
for alg in black_men_alg:
    pos = Pos64.from_algebraic(alg)
    black_men.add(pos.field)
    print(f"  Preta (peão): {alg} → campo {pos.field}")

black_kings = set()
for alg in black_kings_alg:
    pos = Pos64.from_algebraic(alg)
    black_kings.add(pos.field)
    print(f"  Preta (DAMA): {alg} → campo {pos.field}")

print()
print("=" * 70)
print()

# Criar jogo
game = BrazilianGameComplete(white_men, black_men, set(), black_kings)
game.print_board("POSIÇÃO INICIAL:")

print()
print("Análise da posição:")
print(f"  Material: Brancas: 4 peões")
print(f"           Pretas: 3 peões + 1 DAMA")
print(f"  Pretas têm vantagem material significativa!")
print()

# Verificar movimentos possíveis
caps = game.find_all_captures()
moves = game.find_simple_moves()

print("=" * 70)
print("MOVIMENTOS DISPONÍVEIS PARA BRANCAS")
print("=" * 70)
print()

if caps:
    print(f"Capturas obrigatórias: {len(caps)}")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation}")
else:
    print(f"Movimentos simples: {len(moves)}")
    for from_f, to_f, promotes in sorted(moves)[:15]:
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"
        print(f"  {notation}")

print()
print("=" * 70)
print("BUSCA TÁTICA (Profundidade 8)")
print("=" * 70)
print()

engine = TacticalSearchEngine()
best_move, score, sequence = engine.search_best_move(game, max_depth=8)

if best_move:
    print(f"Melhor lance encontrado: {best_move}")
    print(f"Avaliação: {score}")
    print(f"Nós pesquisados: {engine.nodes_searched}")
    print()

    if score >= 9000:
        print("✅ Este lance leva à VITÓRIA FORÇADA!")
    elif score >= 500:
        print("✅ Este lance dá grande vantagem")
    elif score >= 200:
        print("⚠️  Este lance dá pequena vantagem")
    else:
        print("⚠️  Posição complexa")

    print()
    print("Sequência principal:")
    for i, move in enumerate(sequence[:10], 1):
        print(f"  {i}. {move}")

else:
    print("❌ Nenhum movimento encontrado!")

print()
print("=" * 70)
print("BUSCA MAIS PROFUNDA (Profundidade 10)")
print("=" * 70)
print()

engine2 = TacticalSearchEngine()
best_move2, score2, sequence2 = engine2.search_best_move(game, max_depth=10)

if best_move2:
    print(f"Melhor lance encontrado: {best_move2}")
    print(f"Avaliação: {score2}")
    print(f"Nós pesquisados: {engine2.nodes_searched}")
    print()

    if score2 >= 9000:
        print("✅ VITÓRIA FORÇADA ENCONTRADA!")
    elif score2 >= 500:
        print("✅ Grande vantagem encontrada")

    print()
    print("Sequência completa:")
    for i, move in enumerate(sequence2[:12], 1):
        print(f"  {i}. {move}")
