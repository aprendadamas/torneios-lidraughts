"""
Exercício #17 - Teste com Motor Tático V2
FEN: W:Wc1,f2,h2,a3,g3:Ba5,e5,f6,c7,d8.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #17")
print("=" * 70)
print()

# Parsear FEN: W:Wc1,f2,h2,a3,g3:Ba5,e5,f6,c7,d8.
# Brancas (men): c1, f2, h2, a3, g3
# Pretas (men): a5, e5, f6, c7
# Pretas (king): d8 (indicado pelo ponto)

white_alg = ["c1", "f2", "h2", "a3", "g3"]
black_men_alg = ["a5", "e5", "f6", "c7"]
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
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"  Material: Brancas {w_total} peões")
print(f"           Pretas {len(game.black_men)} peões + {len(game.black_kings)} DAMA = {b_total}")
print(f"  Pretas têm vantagem material (dama)!")
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
    for from_f, to_f, promotes in sorted(moves)[:10]:
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"
        print(f"  {notation}")

print()

# Testar com Motor Tático V2 em múltiplas profundidades
for depth in [8, 10, 12]:
    print("=" * 70)
    print(f"MOTOR TÁTICO V2 - PROFUNDIDADE {depth}")
    print("=" * 70)
    print()

    engine = ImprovedTacticalSearchEngine()
    best_move, score, sequence = engine.search_best_move(game, max_depth=depth)

    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score}")
    print(f"Nós pesquisados: {engine.nodes_searched}")
    print()

    if score >= 9000:
        print("✅ VITÓRIA FORÇADA ENCONTRADA!")
    elif score >= 500:
        print("✅ Grande vantagem encontrada")
    elif score >= 200:
        print("⚠️  Pequena vantagem")
    else:
        print("⚠️  Posição complexa ou equilibrada")

    print()
    print("Sequência principal (primeiros 12 lances):")
    for i, move in enumerate(sequence[:12], 1):
        print(f"  {i}. {move}")

    print()

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

print("Características da posição:")
print("  - Pretas têm dama em d8")
print("  - Material aproximadamente equilibrado")
print("  - Brancas precisam encontrar tática precisa")
print()

# Verificar se há algum sacrifício óbvio
print("Possíveis sacrifícios para considerar:")
for from_f, to_f, promotes in moves:
    notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"

    # Simular e ver se é sacrifício
    test_game = game.copy()
    test_game.make_move(from_f, to_f, [], promotes)

    enemy_caps = test_game.find_all_captures()
    is_sacrifice = any(to_f in cap.captured_fields for cap in enemy_caps)

    if is_sacrifice:
        print(f"  - {notation} (pode ser capturado)")
