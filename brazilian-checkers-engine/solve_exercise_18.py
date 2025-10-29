"""
Exercício #18 - Testar Motor Tático V2
FEN: W:Wd2,f2,h2,c3,b4,h4,a5:Bf4,e5,c7,e7,g7,b8,d8.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18")
print("=" * 70)
print()

# Converter FEN para campos pos64
# White: Wd2,f2,h2,c3,b4,h4,a5
# Black: Bf4,e5,c7,e7,g7,b8,d8

print("Convertendo posição...")

# Brancas (White)
white_pieces = ["d2", "f2", "h2", "c3", "b4", "h4", "a5"]
white_kings_notation = ["d2"]  # d2 é dama

white_men = set()
white_kings = set()

for piece in white_pieces:
    field = Pos64.from_algebraic(piece).field
    if piece in white_kings_notation:
        white_kings.add(field)
        print(f"  Branca (DAMA): {piece} → campo {field}")
    else:
        white_men.add(field)
        print(f"  Branca: {piece} → campo {field}")

print()

# Pretas (Black) - todas peões
black_pieces = ["f4", "e5", "c7", "e7", "g7", "b8", "d8"]
black_men = set()

for piece in black_pieces:
    field = Pos64.from_algebraic(piece).field
    black_men.add(field)
    print(f"  Preta (peão): {piece} → campo {field}")

print()
print("=" * 70)
print()

# Criar jogo
game = BrazilianGameComplete(white_men, black_men, white_kings, set())
game.print_board("POSIÇÃO INICIAL:")

print()
print("Análise da posição:")
w_total = len(white_men) + len(white_kings)
b_total = len(black_men)
print(f"  Material: Brancas {w_total} ({len(white_men)} peões + {len(white_kings)} dama)")
print(f"           Pretas {b_total} peões")
print(f"  Brancas têm DAMA em d2!")
print()

# Movimentos disponíveis
print("=" * 70)
print("MOVIMENTOS DISPONÍVEIS PARA BRANCAS")
print("=" * 70)
print()

# Verificar capturas
captures = game.find_all_captures()
if captures:
    print(f"Capturas obrigatórias: {len(captures)}")
    for cap in captures[:10]:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation}")
else:
    # Movimentos simples
    moves = game.find_all_moves()
    print(f"Movimentos simples: {len(moves)}")
    for move in moves[:15]:
        from_pos = Pos64(move.from_field).to_algebraic()
        to_pos = Pos64(move.to_field).to_algebraic()
        piece_type = "dama" if move.from_field in game.white_kings else "peão"
        print(f"  {from_pos} → {to_pos} ({piece_type})")

print()

# Testar com Motor V2
motor = ImprovedTacticalSearchEngine()

for depth in [8, 10, 12]:
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
            print("⚠️  Posição complexa ou equilibrada")
        else:
            print("⚠️  Posição desfavorável")

        # Mostrar linha principal
        if pv_sequence:
            print()
            print(f"Sequência principal (primeiros {min(12, len(pv_sequence))} lances):")
            for i, move in enumerate(pv_sequence[:12], 1):
                print(f"  {i}. {move}")
    else:
        print("❌ Motor não encontrou lance válido")

    print()

# Análise
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

print("Características da posição:")
print("  - Brancas têm DAMA em d2")
print("  - Material: 7 peões brancos vs 7 peões pretos")
print("  - Mas brancas têm dama = grande vantagem!")
print()
print("Possíveis sacrifícios para considerar:")

# Verificar quais peões brancas podem sacrificar
simple_moves = game.find_all_moves() if not captures else []
for move in simple_moves:
    from_pos = Pos64(move.from_field).to_algebraic()
    to_pos = Pos64(move.to_field).to_algebraic()

    # Verificar se move pode ser capturado
    # (análise superficial - ver se tem peão preto adjacente)
    if move.from_field not in game.white_kings:  # Apenas peões
        print(f"  - {from_pos} → {to_pos}")
