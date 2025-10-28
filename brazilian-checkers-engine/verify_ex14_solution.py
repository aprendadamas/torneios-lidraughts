"""
Verificar a solução do Exercício #14
Lance vencedor: f4 → g5
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("VERIFICAÇÃO DA SOLUÇÃO - EXERCÍCIO #14")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("Lance #0 - POSIÇÃO INICIAL")

print()
print("Solução encontrada pelo motor (profundidade 14):")
print("  Lance inicial: f4 → g5")
print("  Avaliação: 9987 (VITÓRIA FORÇADA!)")
print()
print("=" * 70)
print()

move_count = 0

# Lance 1: f4 → g5 (SACRIFÍCIO!)
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam f4 → g5 (SACRIFÍCIO!)")
game.make_move(19, 14, [], False)  # f4 (19) → g5 (14)
game.print_board(f"Após f4 → g5")

# Verificar capturas
caps = game.find_all_captures()
if caps:
    print(f"Pretas têm {len(caps)} captura(s) obrigatória(s):")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")
print()

# Lance 2: h6 x g5 x e3 → d2 (captura dupla!)
move_count += 1
print(f"Lance {move_count}: PRETAS capturam h6 x g5 x e3 → d2")
game.make_move(12, 31, [14, 23], False)  # h6 (12) x g5 (14) x e3 (23) → d2 (31)
game.print_board(f"Após h6 x g5 x e3 → d2")

print(f"Pretas capturaram 2 peças!")
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Lance 3: c1 x d2 → e3
move_count += 1
print(f"Lance {move_count}: BRANCAS capturam c1 x d2 → e3")
game.make_move(30, 23, [31], False)  # c1 (30) x d2 (31) → e3 (23)
game.print_board(f"Após c1 x d2 → e3")

print(f"Brancas recuperam uma peça")
w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Lance 4: b4 → c3
move_count += 1
print(f"Lance {move_count}: PRETAS jogam b4 → c3")
game.make_move(17, 22, [], False)  # b4 (17) → c3 (22)
game.print_board(f"Após b4 → c3")
print()

# Lance 5: d4 x c3 → b2
move_count += 1
print(f"Lance {move_count}: BRANCAS capturam d4 x c3 → b2")
game.make_move(18, 26, [22], False)  # d4 (18) x c3 (22) → b2 (26)
game.print_board(f"Após d4 x c3 → b2")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Lance 6: a3 x b2 → c1
move_count += 1
print(f"Lance {move_count}: PRETAS capturam a3 x b2 → c1")
game.make_move(21, 30, [26], False)  # a3 (21) x b2 (26) → c1 (30)
game.print_board(f"Após a3 x b2 → c1")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Lance 7: e3 → d4
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam e3 → d4")
game.make_move(23, 18, [], False)  # e3 (23) → d4 (18)
game.print_board(f"Após e3 → d4")
print()

# Lance 8: c7 → d6
move_count += 1
print(f"Lance {move_count}: PRETAS jogam c7 → d6")
game.make_move(6, 10, [], False)  # c7 (6) → d6 (10)
game.print_board(f"Após c7 → d6")
print()

# Lance 9: d4 → c5
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam d4 → c5")
game.make_move(18, 13, [], False)  # d4 (18) → c5 (13)
game.print_board(f"Após d4 → c5")

# Verificar capturas
caps = game.find_all_captures()
if caps:
    print(f"Pretas têm captura obrigatória!")
print()

# Lance 10: d6 x c5 → b4
move_count += 1
print(f"Lance {move_count}: PRETAS capturam d6 x c5 → b4")
game.make_move(10, 17, [13], False)  # d6 (10) x c5 (13) → b4 (17)
game.print_board(f"Após d6 x c5 → b4")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Continuar até posição final
print("=" * 70)
print("Continuando a sequência...")
print("=" * 70)
print()

# Lance 11: f2 → g3
move_count += 1
print(f"Lance {move_count}: f2 → g3")
game.make_move(27, 24, [], False)
game.print_board(f"Após lance {move_count}")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: B={w_total} P={b_total}")
print()

# Lance 12: b4 → a3
move_count += 1
print(f"Lance {move_count}: b4 → a3")
game.make_move(17, 21, [], False)
game.print_board(f"Após lance {move_count}")
print()

# Lance 13: g3 → f4
move_count += 1
print(f"Lance {move_count}: g3 → f4")
game.make_move(24, 19, [], False)
game.print_board(f"Após lance {move_count}")

# Verificar capturas
caps = game.find_all_captures()
if caps:
    print(f"Pretas têm {len(caps)} captura(s) obrigatória(s):")
    for cap in caps[:5]:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation}")
print()

# Lance 14: c1 x f4 → g5
move_count += 1
print(f"Lance {move_count}: c1 x f4 → g5")
game.make_move(30, 14, [19], False)
game.print_board(f"Após lance {move_count}")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

print("=" * 70)
print("ANÁLISE FINAL DA POSIÇÃO")
print("=" * 70)
print()

print(f"Total de lances: {move_count}")
print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print()

if b_total == 0:
    print("🏆 BRANCAS VENCERAM - Todas as peças pretas eliminadas!")
elif w_total > b_total:
    print(f"✅ Brancas têm VANTAGEM MATERIAL: +{w_total - b_total}")
    print("Posição vencedora para as brancas!")
else:
    print(f"Material: B={w_total} P={b_total}")
    # Continuar buscando
    from src.tactical_engine import TacticalSearchEngine
    engine = TacticalSearchEngine()
    _, score, sequence = engine.search_best_move(game, max_depth=8)

    print()
    print("Busca tática da posição atual:")
    print(f"  Avaliação: {score}")

    if score >= 9000:
        print("  ✅ VITÓRIA FORÇADA CONFIRMADA!")
    elif score >= 500:
        print("  ✅ Grande vantagem para brancas")

    print()
    print("Continuação sugerida:")
    for i, move in enumerate(sequence[:10], move_count + 1):
        print(f"  {i}. {move}")
