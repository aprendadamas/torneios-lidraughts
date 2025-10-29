"""
Exercício #18 - Verificação DETALHADA com listagem de peças
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

def show_pieces(game, label):
    print(f"\n{label}")
    print("Peças brancas:")
    for f in sorted(game.white_men):
        print(f"  Peão: {Pos64(f).to_algebraic()} (campo {f})")
    for f in sorted(game.white_kings):
        print(f"  DAMA: {Pos64(f).to_algebraic()} (campo {f})")

    print("Peças pretas:")
    for f in sorted(game.black_men):
        print(f"  Peão: {Pos64(f).to_algebraic()} (campo {f})")
    for f in sorted(game.black_kings):
        print(f"  DAMA: {Pos64(f).to_algebraic()} (campo {f})")
    print()

print("=" * 70)
print("EXERCÍCIO #18 - VERIFICAÇÃO DETALHADA")
print("=" * 70)

# Posição inicial
white_men = {26, 27, 28, 22, 17, 20, 13}  # d2, f2, h2, c3, b4, h4, a5
black_men = {19, 15, 6, 7, 8, 1, 2}  # f4, e5, c7, e7, g7, b8, d8

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL")
show_pieces(game, "PEÇAS INICIAIS:")

print("=" * 70)
print("Lance 1.1: a5 → b6")
print("=" * 70)
game.make_move(13, 9, [], False)  # a5 (13) → b6 (9)
game.print_board("Após a5 → b6")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 1.2: c7 x b6 → a5")
print("=" * 70)
game.make_move(6, 13, [9], False)  # c7 (6) x b6 (9) → a5 (13)
game.print_board("Após c7 x b6 → a5")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 2.1: d2 → e3")
print("=" * 70)
game.make_move(26, 23, [], False)  # d2 (26) → e3 (23)
game.print_board("Após d2 → e3")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 2.2: f4 x e3 → d2")
print("=" * 70)
game.make_move(19, 26, [23], False)  # f4 (19) x e3 (23) → d2 (26)
game.print_board("Após f4 x e3 → d2")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 3.1: c3 x d2 → e1 ♛")
print("=" * 70)
game.make_move(22, 31, [26], True)  # c3 (22) x d2 (26) → e1 (31), promove
game.print_board("Após c3 x d2 → e1 ♛")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 3.2: a5 x b4 → c3")
print("=" * 70)
game.make_move(13, 22, [17], False)  # a5 (13) x b4 (17) → c3 (22)
game.print_board("Após a5 x b4 → c3")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 4.1: e1 → d2 (dama move)")
print("=" * 70)
game.make_move(31, 26, [], False)  # e1 (31) → d2 (26)
game.print_board("Após e1 → d2")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 4.2: c3 x d2 → e1 ♛ x f2 → g3")
print("=" * 70)
game.make_move(22, 24, [26, 27], True)  # c3 (22) x d2 (26) x f2 (27) → g3 (24), promove
game.print_board("Após c3 x d2 → e1 ♛ x f2 → g3")
show_pieces(game, "PEÇAS:")

print("=" * 70)
print("Lance 5: CAPTURA MÚLTIPLA")
print("=" * 70)
print("\nCapturas disponíveis:")
caps = game.find_all_captures()
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    captured_notation = []
    for cf in cap.captured_fields:
        captured_notation.append(Pos64(cf).to_algebraic())
    notation += " x " + " x ".join(captured_notation)
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")
    print(f"    Origem: campo {cap.from_field}")
    print(f"    Destino: campo {cap.to_field}")
    print(f"    Capturas: {cap.captured_fields}")

# Executar a maior captura
if caps:
    best_cap = max(caps, key=lambda c: len(c.captured_fields))
    print(f"\nExecutando captura com {len(best_cap.captured_fields)} peças:")
    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    if best_cap.promotes:
        notation += " ♛"
    print(notation)

    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board("POSIÇÃO FINAL")
    show_pieces(game, "PEÇAS FINAIS:")

    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)
    print(f"Material: Brancas {w_total} vs Pretas {b_total}")
    if w_total > b_total:
        print(f"✅ BRANCAS VENCEM (+{w_total - b_total})")
    elif w_total == b_total:
        print("⚖️  EMPATE")
    else:
        print(f"⚠️  PRETAS VENCEM (+{b_total - w_total})")
