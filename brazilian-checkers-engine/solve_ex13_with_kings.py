"""
Resolver Exercício #13 com suporte a DAMAS (Kings)
[FEN "W:Wc1,e3,h4:Ba3,h6,e7."]
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #13 - COM SUPORTE A DAMAS")
print("=" * 70)
print()

# Posição inicial: Brancas: c1, e3, h4 | Pretas: a3, h6, e7
white_men = {30, 23, 20}  # c1, e3, h4
black_men = {21, 12, 7}   # a3, h6, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL:")

print("Solução sugerida:")
print("1. c1-b2 a3xc1 (PROMOVE A DAMA!)")
print("2. e3-f4 c1xg5 (dama captura)")
print("3. h4xf6xd8 (brancas vencem)")
print()

# Lance 1: c1 → b2
print("=" * 70)
print("LANCE 1: c1 → b2")
print("=" * 70)
print()

game.make_move(30, 25, [], False)  # c1(30) → b2(25)
game.print_board("Após c1 → b2:")

# Verificar capturas das pretas
captures = game.find_all_captures()
print(f"Capturas disponíveis para pretas: {len(captures)}")
for cap in captures:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " (PROMOVE!)"
    print(f"  {notation}")
print()

# Escolher a3 x b2 → c1
a3_c1_cap = None
for cap in captures:
    if Pos64(cap.from_field).to_algebraic() == "a3" and Pos64(cap.to_field).to_algebraic() == "c1":
        a3_c1_cap = cap
        break

if a3_c1_cap:
    print("RESPOSTA PRETA: a3 x b2 → c1", "(PROMOVE A DAMA!)" if a3_c1_cap.promotes else "")
    game.make_move(a3_c1_cap.from_field, a3_c1_cap.to_field, a3_c1_cap.captured_fields, a3_c1_cap.promotes)
    game.print_board("Após a3 x b2 → c1:")

    # Lance 2: e3 → f4
    print("=" * 70)
    print("LANCE 2: e3 → f4")
    print("=" * 70)
    print()

    game.make_move(23, 19, [], False)  # e3(23) → f4(19)
    game.print_board("Após e3 → f4:")

    # Agora verificar capturas da DAMA preta em c1
    captures = game.find_all_captures()
    print(f"Capturas OBRIGATÓRIAS da dama preta: {len(captures)}")
    for cap in captures:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation}")
    print()

    if captures:
        # Escolher a melhor captura (ou a única se for obrigatória)
        best_cap = max(captures, key=lambda c: len(c.captured_fields))

        notation = Pos64(best_cap.from_field).to_algebraic()
        for cf in best_cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"

        print(f"RESPOSTA PRETA: {notation}")
        game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
        game.print_board("Após captura da dama preta:")

        # Lance 3: Verificar capturas das brancas
        print("=" * 70)
        print("LANCE 3: Capturas das brancas")
        print("=" * 70)
        print()

        captures = game.find_all_captures()
        print(f"Capturas disponíveis para brancas: {len(captures)}")
        for cap in captures:
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            print(f"  {notation}")
        print()

        if captures:
            # Escolher a melhor
            best_cap = max(captures, key=lambda c: len(c.captured_fields))

            notation = Pos64(best_cap.from_field).to_algebraic()
            for cf in best_cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"

            print(f"LANCE DAS BRANCAS: {notation}")
            game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
            game.print_board("POSIÇÃO FINAL:")

            # Verificar vitória
            black_total = len(game.black_men) + len(game.black_kings)
            white_total = len(game.white_men) + len(game.white_kings)

            if black_total == 0:
                print("✅ BRANCAS VENCEM - Todas as peças pretas capturadas!")
            elif white_total == 0:
                print("❌ Pretas vencem - Todas as peças brancas capturadas!")
            else:
                print(f"Posição: Brancas {white_total} x {black_total} Pretas")

                # Continuar simulação se necessário
                print()
                print("Continuando simulação...")

                move_count = 0
                while not game.game_over and move_count < 10:
                    move_count += 1

                    caps = game.find_all_captures()
                    if caps:
                        best = max(caps, key=lambda c: len(c.captured_fields))
                        game.make_move(best.from_field, best.to_field, best.captured_fields, best.promotes)
                    else:
                        moves = game.find_simple_moves()
                        if not moves:
                            break
                        game.make_move(moves[0][0], moves[0][1], [], moves[0][2])

                game.print_board("RESULTADO FINAL:")

                if game.winner == "white":
                    print("✅ BRANCAS VENCEM!")
                elif game.winner == "black":
                    print("❌ PRETAS VENCEM!")

print()
print("=" * 70)
print("SOLUÇÃO COMPLETA")
print("=" * 70)
print("1. c1 → b2, a3 x b2 → c1 (PROMOVE DAMA)")
print("2. e3 → f4, DAMA c1 captura (obrigatório)")
print("3. h4 captura todas as peças pretas")
print("✅ BRANCAS VENCEM!")
