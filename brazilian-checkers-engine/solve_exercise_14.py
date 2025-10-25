"""
Resolver Exercício Tático #14
[FEN "W:Wc1,f2,e3,d4,f4,h4:Ba3,b4,f6,h6,c7,e7."]
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - 1800 Combinações")
print("=" * 70)
print()

# Converter posição FEN para campos
white_alg = ["c1", "f2", "e3", "d4", "f4", "h4"]
black_alg = ["a3", "b4", "f6", "h6", "c7", "e7"]

print("Posição inicial:")
print(f"  Brancas: {white_alg}")
print(f"  Pretas: {black_alg}")
print()

# Converter para campos
white_fields = {Pos64.from_algebraic(alg).field for alg in white_alg}
black_fields = {Pos64.from_algebraic(alg).field for alg in black_alg}

print(f"  Brancas (campos): {sorted(white_fields)}")
print(f"  Pretas (campos): {sorted(black_fields)}")
print()

# Criar jogo
game = BrazilianGameComplete(white_fields, black_fields)
game.print_board("POSIÇÃO INICIAL:")

# Analisar capturas disponíveis
print("=" * 70)
print("ANÁLISE INICIAL")
print("=" * 70)
print()

captures = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(captures)}")

if captures:
    for i, cap in enumerate(captures, 1):
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " (PROMOVE!)"
        print(f"  {i}. {notation} ({len(cap.captured_fields)} peça(s))")
    print()
else:
    print("  Nenhuma captura obrigatória")
    print()

# Verificar movimentos simples se não houver capturas
if not captures:
    simple_moves = game.find_simple_moves()
    print(f"Movimentos simples disponíveis: {len(simple_moves)}")
    for from_f, to_f, promotes in simple_moves[:10]:
        from_alg = Pos64(from_f).to_algebraic()
        to_alg = Pos64(to_f).to_algebraic()
        promo_str = " (PROMOVE!)" if promotes else ""
        print(f"  {from_alg} → {to_alg}{promo_str}")
    print()

# Estratégia: Testar cada movimento possível e ver qual leva à melhor posição
print("=" * 70)
print("BUSCANDO MELHOR SEQUÊNCIA")
print("=" * 70)
print()

def evaluate_position(game):
    """Avalia uma posição (positivo = brancas melhor)"""
    white_total = len(game.white_men) + len(game.white_kings) * 3
    black_total = len(game.black_men) + len(game.black_kings) * 3
    return white_total - black_total

def simulate_moves(game, depth=0, max_depth=5):
    """Simula movimentos e retorna (score, sequência)"""

    # Verificar fim de jogo
    white_total = len(game.white_men) + len(game.white_kings)
    black_total = len(game.black_men) + len(game.black_kings)

    if white_total == 0:
        return (-10000, [])
    if black_total == 0:
        return (10000, [])

    if depth >= max_depth:
        return (evaluate_position(game), [])

    # Verificar capturas (obrigatórias)
    captures = game.find_all_captures()

    if captures:
        best_score = -10000 if game.turn == "white" else 10000
        best_sequence = []

        for cap in captures:
            # Fazer cópia e executar
            test_game = BrazilianGameComplete(
                game.white_men.copy(), game.black_men.copy(),
                game.white_kings.copy(), game.black_kings.copy(),
                game.turn
            )

            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            if cap.promotes:
                notation += " (PROMOVE!)"

            test_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

            score, seq = simulate_moves(test_game, depth + 1, max_depth)

            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_sequence = [f"{depth+1}. white: {notation}"] + seq
            else:
                if score < best_score:
                    best_score = score
                    best_sequence = [f"{depth+1}. black: {notation}"] + seq

        return (best_score, best_sequence)

    # Movimentos simples
    moves = game.find_simple_moves()

    if not moves:
        # Sem movimentos
        if game.turn == "white":
            return (-10000, [])
        else:
            return (10000, [])

    best_score = -10000 if game.turn == "white" else 10000
    best_sequence = []

    # Limitar busca para primeiros 5 movimentos
    for from_f, to_f, promotes in moves[:5]:
        test_game = BrazilianGameComplete(
            game.white_men.copy(), game.black_men.copy(),
            game.white_kings.copy(), game.black_kings.copy(),
            game.turn
        )

        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " (PROMOVE!)"

        test_game.make_move(from_f, to_f, [], promotes)

        score, seq = simulate_moves(test_game, depth + 1, max_depth)

        if game.turn == "white":
            if score > best_score:
                best_score = score
                best_sequence = [f"{depth+1}. white: {notation}"] + seq
        else:
            if score < best_score:
                best_score = score
                best_sequence = [f"{depth+1}. black: {notation}"] + seq

    return (best_score, best_sequence)

print("Executando busca em profundidade (pode levar alguns segundos)...")
print()

score, sequence = simulate_moves(game, 0, 6)

print(f"Avaliação final: {score}")
print()

if score >= 1000:
    print("✅ BRANCAS VENCEM!")
elif score <= -1000:
    print("❌ Pretas vencem")
else:
    print(f"⚖️  Posição equilibrada (vantagem: {'+' if score > 0 else ''}{score/10:.1f})")

print()
print("Melhor sequência encontrada:")
for i, move in enumerate(sequence[:10], 1):
    print(f"  {move}")

print()
print("=" * 70)
print("VERIFICAÇÃO DA SEQUÊNCIA")
print("=" * 70)
print()

# Executar a sequência encontrada manualmente
if captures:
    # Se há capturas, executar a melhor
    best_cap = max(captures, key=lambda c: len(c.captured_fields))

    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    if best_cap.promotes:
        notation += " (PROMOVE!)"

    print(f"Melhor primeiro lance: {notation}")
    print()

    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board("Após primeiro lance:")

    # Continuar simulação
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
            # Escolher movimento que avança
            best = moves[0]
            game.make_move(best[0], best[1], [], best[2])

    game.print_board("POSIÇÃO FINAL:")

    if game.winner == "white":
        print("✅ BRANCAS VENCEM!")
    elif game.winner == "black":
        print("❌ PRETAS VENCEM!")
    else:
        white_total = len(game.white_men) + len(game.white_kings)
        black_total = len(game.black_men) + len(game.black_kings)
        print(f"Resultado: Brancas {white_total} x {black_total} Pretas")
