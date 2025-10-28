"""
Continuar Exercício #14 a partir do lance 14
Para ver como as brancas conseguem virar o jogo!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - CONTINUANDO APÓS LANCE 14")
print("=" * 70)
print()

# Posição após lance 14 (conforme simulação anterior)
# Brancas: 1 peão em h4
# Pretas: 1 dama em g5, 2 peões em e7 e f6, 1 peão em a3

# Vou reconstruir a posição manualmente
# Após lance 14: c1 x f4 → g5
# Brancas tinham: h4, g3
# g3 → f4 (lance 13)
# Então brancas tinham: h4, f4
# Pretas capturaram f4 com c1 x f4 → g5
# Então agora: h4 (brancas), g5 (dama preta)

# Peças pretas: a3, e7, f6, g5(dama)
# Peças brancas: h4

white_men = {20}  # h4
white_kings = set()
black_men = {21, 7, 11}  # a3, e7, f6
black_kings = {16}  # g5

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO APÓS LANCE 14")

print()
print(f"Material: Brancas {len(white_men) + len(white_kings)} vs Pretas {len(black_men) + len(black_kings)}")
print(f"Turno: {game.turn}")
print()

# Verificar movimentos disponíveis
caps = game.find_all_captures()
moves = game.find_simple_moves()

print("Movimentos disponíveis para brancas:")
if caps:
    print(f"  Capturas obrigatórias: {len(caps)}")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"    {notation}")
else:
    print(f"  Movimentos simples: {len(moves)}")
    for from_f, to_f, promotes in list(moves)[:10]:
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"
        print(f"    {notation}")

if len(caps) == 0 and len(moves) == 0:
    print()
    print("❌ BRANCAS NÃO TÊM MOVIMENTOS - PERDERAM!")
    print()
    print("Isso indica que o motor tático tem um BUG.")
    print("Ele disse que havia vitória forçada, mas a sequência leva à derrota.")
else:
    print()
    print("=" * 70)
    print("Continuando com busca tática (profundidade 16)")
    print("=" * 70)
    print()

    move_count = 14

    for _ in range(30):  # Até 30 lances adicionais
        engine = TacticalSearchEngine()
        _, score, sequence = engine.search_best_move(game, max_depth=16)

        if not sequence or len(sequence) == 0:
            print("Sem movimentos disponíveis")
            break

        move_count += 1
        next_move = sequence[0]

        print(f"Lance {move_count}: {next_move}")

        # Executar
        if ' x ' in next_move:
            caps = game.find_all_captures()
            executed = False
            for cap in caps:
                cap_notation = Pos64(cap.from_field).to_algebraic()
                for cf in cap.captured_fields:
                    cap_notation += f" x {Pos64(cf).to_algebraic()}"
                cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                if next_move.startswith(cap_notation.split(' ♛')[0]):
                    game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                    executed = True
                    break

            if not executed:
                print(f"  ⚠️  Erro ao executar")
                break
        else:
            parts = next_move.split(' → ')
            if len(parts) == 2:
                from_alg = parts[0]
                to_alg = parts[1].replace(' ♛', '')

                from_f = Pos64.from_algebraic(from_alg).field
                to_f = Pos64.from_algebraic(to_alg).field
                promotes = '♛' in next_move

                game.make_move(from_f, to_f, [], promotes)

        w_total = len(game.white_men) + len(game.white_kings)
        b_total = len(game.black_men) + len(game.black_kings)

        if move_count % 5 == 0 or b_total == 0 or w_total == 0:
            game.print_board(f"Após lance {move_count}")
            print(f"Material: B={w_total} P={b_total}")
            print()

        if b_total == 0:
            print("🏆 BRANCAS VENCERAM!")
            break

        if w_total == 0:
            print("❌ Pretas venceram")
            break

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    print()

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)

    print(f"Lances totais: {move_count}")
    print(f"Material final: B={w_total} P={b_total}")
