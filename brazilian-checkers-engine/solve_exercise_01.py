"""
Resolver Exercício #1 - BÁSICO
[FEN "W:Wa1,b2,c3:Ba5,e5,g7."]
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #1 - NÍVEL BÁSICO")
print("=" * 70)
print()

# Converter posição FEN
white_alg = ["a1", "b2", "c3"]
black_alg = ["a5", "e5", "g7"]

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
print("ANÁLISE")
print("=" * 70)
print()

captures = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(captures)}")

if captures:
    print()
    for i, cap in enumerate(captures, 1):
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {i}. {notation} ({len(cap.captured_fields)} peça(s))")

    # Executar a melhor captura (mais peças)
    best_cap = max(captures, key=lambda c: len(c.captured_fields))

    print()
    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    if best_cap.promotes:
        notation += " ♛"

    print(f"Melhor captura: {notation}")
    print()

    game.make_move(best_cap.from_field, best_cap.to_field,
                   best_cap.captured_fields, best_cap.promotes)
    game.print_board("Após captura:")

    # Continuar jogando até o fim
    print("Continuando simulação...")
    print()

    move_count = 1
    sequence = [f"1. white: {notation}"]

    while not game.game_over and move_count < 15:
        move_count += 1

        # Capturas obrigatórias
        caps = game.find_all_captures()

        if caps:
            # Escolher captura máxima
            best = max(caps, key=lambda c: len(c.captured_fields))

            notation = Pos64(best.from_field).to_algebraic()
            for cf in best.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(best.to_field).to_algebraic()}"
            if best.promotes:
                notation += " ♛"

            sequence.append(f"{move_count}. {game.turn}: {notation}")
            game.make_move(best.from_field, best.to_field,
                          best.captured_fields, best.promotes)
        else:
            # Movimento simples
            moves = game.find_simple_moves()

            if not moves:
                game.game_over = True
                game.winner = "black" if game.turn == "white" else "white"
                break

            # Estratégia: avançar
            if game.turn == "white":
                best = min(moves, key=lambda m: m[1])
            else:
                best = max(moves, key=lambda m: m[1])

            notation = f"{Pos64(best[0]).to_algebraic()} → {Pos64(best[1]).to_algebraic()}"
            if best[2]:
                notation += " ♛"

            sequence.append(f"{move_count}. {game.turn}: {notation}")
            game.make_move(best[0], best[1], [], best[2])

    game.print_board("POSIÇÃO FINAL:")

    print("=" * 70)
    print("SEQUÊNCIA COMPLETA")
    print("=" * 70)
    print()

    for move in sequence:
        print(move)
    print()

    # Resultado
    white_total = len(game.white_men) + len(game.white_kings)
    black_total = len(game.black_men) + len(game.black_kings)

    if game.winner == "white" or black_total == 0:
        print("✅ BRANCAS VENCEM!")
    elif game.winner == "black" or white_total == 0:
        print("❌ PRETAS VENCEM!")
    else:
        print(f"⚖️  Resultado: Brancas {white_total} x {black_total} Pretas")

else:
    print("  Nenhuma captura obrigatória")
    print()

    # Movimentos simples
    simple_moves = game.find_simple_moves()
    print(f"Movimentos simples disponíveis: {len(simple_moves)}")

    for from_f, to_f, promotes in simple_moves:
        from_alg = Pos64(from_f).to_algebraic()
        to_alg = Pos64(to_f).to_algebraic()
        promo_str = " ♛" if promotes else ""
        print(f"  {from_alg} → {to_alg}{promo_str}")

print()
print("=" * 70)
print("ANÁLISE DO EXERCÍCIO")
print("=" * 70)
print()

# Verificar se é vitória das brancas
if game.winner == "white" or (len(game.black_men) + len(game.black_kings)) == 0:
    print("✅ Exercício resolvido - Brancas vencem!")
    print()
    print("Lição tática:")
    if captures and len(captures[0].captured_fields) > 1:
        print("  - Captura múltipla decisiva")
    if any(cap.promotes for cap in captures):
        print("  - Promoção durante captura")
    print(f"  - Total de lances: {move_count}")
else:
    print("⚠️  Resultado diferente do esperado")
    print("   Pode indicar que há uma sequência melhor não explorada")
