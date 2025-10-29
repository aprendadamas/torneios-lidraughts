"""
Exercício #18 - CORREÇÃO - Testar Motor Tático V2
FEN: W:Wd2,f2,h2,c3,b4,h4,a5:Bf4,e5,c7,e7,g7,b8,d8.

CORREÇÃO: Todas as peças são PEÕES, não há damas na posição inicial!
W e B indicam apenas a COR (White/Black), não que sejam damas.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - CORREÇÃO")
print("=" * 70)
print()

print("ERRO ANTERIOR: Interpretei Wd2 como dama")
print("CORRETO: Wd2 significa apenas peça BRANCA (white) em d2")
print()

# Posição correta: TODAS AS PEÇAS SÃO PEÕES!
white_pieces = ["d2", "f2", "h2", "c3", "b4", "h4", "a5"]
black_pieces = ["f4", "e5", "c7", "e7", "g7", "b8", "d8"]

white_men = set()
white_kings = set()  # Vazio! Sem damas!

for piece in white_pieces:
    field = Pos64.from_algebraic(piece).field
    white_men.add(field)
    print(f"  Branca (peão): {piece} → campo {field}")

print()

black_men = set()
for piece in black_pieces:
    field = Pos64.from_algebraic(piece).field
    black_men.add(field)
    print(f"  Preta (peão): {piece} → campo {field}")

print()
print("=" * 70)
print()

# Criar jogo com ZERO damas
game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL CORRETA:")

print()
print("Análise da posição:")
w_total = len(white_men)
b_total = len(black_men)
print(f"  Material: Brancas {w_total} PEÕES")
print(f"           Pretas {b_total} PEÕES")
print(f"  SEM DAMAS na posição!")
print()

# Verificar capturas disponíveis
print("=" * 70)
print("CAPTURAS DISPONÍVEIS")
print("=" * 70)
print()

captures = game.find_all_captures()
if captures:
    print(f"Capturas obrigatórias: {len(captures)}")
    for cap in captures:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")
else:
    moves = game.find_simple_moves()
    print(f"Sem capturas. Movimentos simples: {len(moves)}")

print()

# Testar com Motor V2
motor = ImprovedTacticalSearchEngine()

for depth in [8, 10]:
    print("=" * 70)
    print(f"MOTOR TÁTICO V2 - PROFUNDIDADE {depth}")
    print("=" * 70)
    print()

    best_move, score, pv_sequence = motor.search_best_move(game, max_depth=depth)

    if best_move:
        print(f"Melhor lance: {best_move}")
        print(f"Avaliação: {score:+.0f}")
        print(f"Nós pesquisados: {motor.nodes_searched:,}")
        print()

        # Interpretar score
        if score >= 9000:
            print("✅ VITÓRIA FORÇADA ENCONTRADA!")
        elif score >= 500:
            print("✅ Grande vantagem encontrada")
        elif score >= 200:
            print("⚖️  Pequena vantagem")
        elif score > 0:
            print("⚖️  Ligeira vantagem para brancas")
        elif score == 0:
            print("⚠️  Posição equilibrada")
        else:
            print("⚠️  Posição desfavorável")

        # Mostrar linha principal
        if pv_sequence:
            print()
            print(f"Sequência principal (primeiros {min(8, len(pv_sequence))} lances):")
            for i, move in enumerate(pv_sequence[:8], 1):
                print(f"  {i}. {move}")
    else:
        print("❌ Motor não encontrou lance válido")

    print()
