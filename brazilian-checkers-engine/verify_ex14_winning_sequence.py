"""
Verificar a sequência completa vencedora do Exercício #14
Lance vencedor: f4 → g5 (requer profundidade 16 para encontrar!)
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64
from src.tactical_engine import TacticalSearchEngine

print("=" * 70)
print("EXERCÍCIO #14 - SEQUÊNCIA VENCEDORA COMPLETA")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("SOLUÇÃO: f4 → g5")
print("(Requer profundidade 16 para o motor encontrar!)")
print()
print("=" * 70)
print()

# Sequência completa encontrada
moves_str = [
    ("f4 → g5", "white", "move"),
    ("h6 x g5 x e3 → d2", "black", "capture"),
    ("c1 x d2 → e3", "white", "capture"),
    ("b4 → c3", "black", "move"),
    ("d4 x c3 → b2", "white", "capture"),
    ("a3 x b2 → c1", "black", "capture"),
    ("e3 → d4", "white", "move"),
    ("c7 → d6", "black", "move"),
    ("d4 → c5", "white", "move"),
    ("d6 x c5 → b4", "black", "capture"),
    ("f2 → g3", "white", "move"),
    ("b4 → a3", "black", "move"),
    ("g3 → f4", "white", "move"),
    ("c1 x f4 → g5", "black", "capture"),
]

move_count = 0

for move_str, turn, move_type in moves_str:
    move_count += 1

    print(f"Lance {move_count}: {turn.upper()} - {move_str}")

    # Executar o movimento
    if move_type == "capture":
        # É captura
        caps = game.find_all_captures()
        executed = False

        for cap in caps:
            cap_notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                cap_notation += f" x {Pos64(cf).to_algebraic()}"
            cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

            if move_str.startswith(cap_notation) or cap_notation == move_str.split()[0]:
                game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                executed = True
                break

        if not executed:
            print(f"  ⚠️  Não consegui executar: {move_str}")
    else:
        # Movimento simples
        parts = move_str.split(' → ')
        if len(parts) == 2:
            from_alg = parts[0]
            to_alg = parts[1].replace(' ♛', '')

            from_f = Pos64.from_algebraic(from_alg).field
            to_f = Pos64.from_algebraic(to_alg).field
            promotes = '♛' in move_str

            game.make_move(from_f, to_f, [], promotes)

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)

    # Mostrar tabuleiro a cada 4 lances ou quando material muda significativamente
    if move_count % 4 == 0 or move_count == 1 or move_count == 2:
        game.print_board(f"Após lance {move_count}")
        print(f"Material: Brancas {w_total} vs Pretas {b_total}")
        print()

    if b_total == 0:
        print()
        game.print_board("POSIÇÃO FINAL")
        print()
        print("🏆 BRANCAS VENCERAM - Todas as peças pretas eliminadas!")
        break

print()
print("=" * 70)
print("CONTINUANDO A PARTIR DESTE PONTO")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

if b_total > 0:
    print(f"Material atual: Brancas {w_total} vs Pretas {b_total}")
    print()
    print("Usando motor tático para continuar (profundidade 14)...")
    print()

    engine = TacticalSearchEngine()

    while b_total > 0 and w_total > 0 and move_count < 50:
        _, score, sequence = engine.search_best_move(game, max_depth=14)

        if not sequence or len(sequence) == 0:
            print("Sem movimentos disponíveis!")
            break

        next_move = sequence[0]
        move_count += 1

        print(f"Lance {move_count}: {next_move}")

        # Executar o movimento
        if ' x ' in next_move:
            # É captura
            caps = game.find_all_captures()
            executed = False

            for cap in caps:
                cap_notation = Pos64(cap.from_field).to_algebraic()
                for cf in cap.captured_fields:
                    cap_notation += f" x {Pos64(cf).to_algebraic()}"
                cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                if next_move.startswith(cap_notation):
                    game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                    executed = True
                    break

            if not executed:
                print(f"  ⚠️  Não consegui executar captura")
                break
        else:
            # Movimento simples
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

        if move_count % 5 == 0 or b_total == 0:
            game.print_board(f"Após lance {move_count}")
            print(f"Material: B={w_total} P={b_total}")
            print()

        if b_total == 0:
            print("🏆 BRANCAS VENCERAM!")
            break

        if move_count >= 50:
            print("⚠️  Limite de 50 lances atingido")
            break

print()
print("=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Total de lances: {move_count}")
print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print()

if b_total == 0:
    print("✅ EXERCÍCIO #14 RESOLVIDO!")
    print("✅ Brancas vencem com f4 → g5!")
    print()
    print(f"Solução requer {move_count} lances")
    print("Motor tático precisa de profundidade 16 para encontrar esta solução")
elif w_total > b_total:
    print(f"✅ Brancas têm grande vantagem: +{w_total - b_total}")
else:
    print(f"⚠️  Posição complexa: B={w_total} P={b_total}")
