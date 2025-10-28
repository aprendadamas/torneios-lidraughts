"""
Exercício #14 - Nova Tentativa
Agora com 4 padrões táticos identificados!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - NOVA TENTATIVA")
print("=" * 70)
print()

# FEN: W:Wc1,f2,e3,d4,f4,h4:Ba3,b4,f6,h6,c7,e7.
white_alg = ["c1", "f2", "e3", "d4", "f4", "h4"]
black_alg = ["a3", "b4", "f6", "h6", "c7", "e7"]

print("Convertendo posição...")
white_men = set()
for alg in white_alg:
    pos = Pos64.from_algebraic(alg)
    white_men.add(pos.field)
    print(f"  Branca: {alg} → campo {pos.field}")

print()
black_men = set()
for alg in black_alg:
    pos = Pos64.from_algebraic(alg)
    black_men.add(pos.field)
    print(f"  Preta: {alg} → campo {pos.field}")

print()
print("=" * 70)
print()

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL:")

print()
print("Análise da posição:")
print(f"  Material: Brancas 6 peões vs Pretas 6 peões (equilibrado)")
print()

# Verificar movimentos possíveis
caps = game.find_all_captures()
moves = game.find_simple_moves()

print("=" * 70)
print("MOVIMENTOS DISPONÍVEIS")
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
    for from_f, to_f, promotes in sorted(moves):
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"
        print(f"  {notation}")

print()
print("=" * 70)
print("ANÁLISE TÁTICA - Testando cada lance")
print("=" * 70)
print()

# Testar cada movimento e ver qual dá melhor resultado
best_overall_move = None
best_overall_score = -99999
best_overall_seq = []

for from_f, to_f, promotes in sorted(moves):
    notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
    if promotes:
        notation += " ♛"

    # Testar com profundidade 12
    test_game = game.copy()
    test_game.make_move(from_f, to_f, [], promotes)

    engine = TacticalSearchEngine()
    _, score, sequence = engine.search_best_move(test_game, max_depth=12)

    # Inverter score (estamos vendo do ponto de vista das pretas)
    white_score = -score

    print(f"{notation}:")
    print(f"  Avaliação: {white_score}")
    print(f"  Nós: {engine.nodes_searched}")

    if white_score > best_overall_score:
        best_overall_score = white_score
        best_overall_move = notation
        best_overall_seq = [notation] + sequence

    if white_score >= 9000:
        print(f"  ✅ VITÓRIA FORÇADA!")
    elif white_score >= 500:
        print(f"  ✅ Grande vantagem")

    # Mostrar continuação
    if len(sequence) > 0:
        print(f"  Continuação: {' → '.join(sequence[:4])}")
    print()

print()
print("=" * 70)
print("MELHOR LANCE ENCONTRADO")
print("=" * 70)
print()

print(f"Lance: {best_overall_move}")
print(f"Avaliação: {best_overall_score}")
print()

if best_overall_score >= 9000:
    print("✅ VITÓRIA FORÇADA ENCONTRADA!")
elif best_overall_score >= 500:
    print("✅ Grande vantagem encontrada")
else:
    print("⚠️  Nenhuma vitória clara encontrada")

print()
print("Sequência completa:")
for i, move in enumerate(best_overall_seq[:15], 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("BUSCA AINDA MAIS PROFUNDA - Apenas melhor lance")
print("=" * 70)
print()

# Pegar o melhor lance e buscar com profundidade 14
if best_overall_move:
    parts = best_overall_move.split(" → ")
    if len(parts) == 2:
        from_alg = parts[0]
        to_alg = parts[1].replace(" ♛", "")

        from_f = Pos64.from_algebraic(from_alg).field
        to_f = Pos64.from_algebraic(to_alg).field
        promotes = "♛" in best_overall_move

        test_game = game.copy()
        test_game.make_move(from_f, to_f, [], promotes)

        print(f"Buscando profundidade 14 após {best_overall_move}...")
        engine = TacticalSearchEngine()
        _, score, sequence = engine.search_best_move(test_game, max_depth=14)

        white_score = -score

        print(f"Avaliação profundidade 14: {white_score}")
        print(f"Nós pesquisados: {engine.nodes_searched}")
        print()

        if white_score >= 9000:
            print("✅ VITÓRIA FORÇADA CONFIRMADA!")
        elif white_score >= 500:
            print("✅ Grande vantagem confirmada")

        print()
        print("Sequência (primeiros 20 lances):")
        full_seq = [best_overall_move] + sequence
        for i, move in enumerate(full_seq[:20], 1):
            print(f"  {i}. {move}")
