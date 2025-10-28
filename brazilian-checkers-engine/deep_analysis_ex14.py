"""
Análise MANUAL PROFUNDA do Exercício #14
Testando TODAS as sequências possíveis de forma sistemática
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64
from typing import List, Tuple

def print_position_summary(game):
    """Imprime resumo da posição"""
    w_men = len(game.white_men)
    w_kings = len(game.white_kings)
    b_men = len(game.black_men)
    b_kings = len(game.black_kings)

    print(f"  Material: W({w_men}p+{w_kings}d) vs B({b_men}p+{b_kings}d)")

    if w_men + w_kings > 0:
        white_pieces = sorted(game.white_men | game.white_kings)
        print(f"  Brancas: {[Pos64(f).to_algebraic() for f in white_pieces]}")

    if b_men + b_kings > 0:
        black_pieces = sorted(game.black_men | game.black_kings)
        print(f"  Pretas: {[Pos64(f).to_algebraic() for f in black_pieces]}")

def explore_all_sequences(game, depth, max_depth, sequence, all_results):
    """Explora TODAS as sequências possíveis até max_depth"""

    # Verificar vitória
    b_total = len(game.black_men) + len(game.black_kings)
    w_total = len(game.white_men) + len(game.white_kings)

    if b_total == 0:
        all_results.append({
            'sequence': sequence.copy(),
            'depth': depth,
            'winner': 'white',
            'w_pieces': w_total,
            'b_pieces': 0
        })
        return

    if w_total == 0:
        return

    if depth >= max_depth:
        return

    # Capturas obrigatórias
    caps = game.find_all_captures()

    if caps:
        for cap in caps:
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            if cap.promotes:
                notation += " ♛"

            new_game = BrazilianGameComplete(
                game.white_men.copy(), game.black_men.copy(),
                game.white_kings.copy(), game.black_kings.copy(),
                game.turn
            )
            new_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

            new_seq = sequence + [(depth + 1, game.turn, notation, len(cap.captured_fields))]
            explore_all_sequences(new_game, depth + 1, max_depth, new_seq, all_results)
    else:
        # Movimentos simples
        moves = game.find_simple_moves()

        for from_f, to_f, promotes in moves:
            notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
            if promotes:
                notation += " ♛"

            new_game = BrazilianGameComplete(
                game.white_men.copy(), game.black_men.copy(),
                game.white_kings.copy(), game.black_kings.copy(),
                game.turn
            )
            new_game.make_move(from_f, to_f, [], promotes)

            new_seq = sequence + [(depth + 1, game.turn, notation, 0)]
            explore_all_sequences(new_game, depth + 1, max_depth, new_seq, all_results)

print("=" * 80)
print("EXERCÍCIO #14 - EXPLORAÇÃO EXAUSTIVA DE TODAS AS SEQUÊNCIAS")
print("=" * 80)
print()

white = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white, black)
game.print_board("POSIÇÃO INICIAL:")

print("Explorando TODAS as sequências até profundidade 6...")
print("(Isso pode levar alguns minutos)")
print()

all_results = []
explore_all_sequences(game, 0, 6, [], all_results)

print(f"Total de sequências exploradas que levam à vitória: {len(all_results)}")
print()

# Filtrar sequências mais curtas
if all_results:
    min_depth = min(r['depth'] for r in all_results)
    shortest = [r for r in all_results if r['depth'] == min_depth]

    print(f"Menor número de lances para vitória: {min_depth}")
    print(f"Sequências com {min_depth} lances: {len(shortest)}")
    print()

    # Mostrar as 5 primeiras sequências mais curtas
    print("=" * 80)
    print(f"MELHORES SEQUÊNCIAS ({min_depth} LANCES)")
    print("=" * 80)
    print()

    for i, result in enumerate(shortest[:5], 1):
        print(f"Sequência {i}:")
        for move_num, turn, notation, captures in result['sequence']:
            print(f"  {move_num}. {turn}: {notation}")
        print()

    # Executar a primeira sequência encontrada
    if shortest:
        print("=" * 80)
        print("VERIFICANDO PRIMEIRA SEQUÊNCIA")
        print("=" * 80)
        print()

        verify_game = BrazilianGameComplete(white, black)

        for move_num, turn, notation, captures in shortest[0]['sequence']:
            print(f"Lance {move_num}: {turn} - {notation}")

            # Parsear e executar
            if 'x' in notation:
                # É captura
                caps = verify_game.find_all_captures()

                # Encontrar a captura correspondente
                for cap in caps:
                    cap_notation = Pos64(cap.from_field).to_algebraic()
                    for cf in cap.captured_fields:
                        cap_notation += f" x {Pos64(cf).to_algebraic()}"
                    cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                    if cap_notation in notation:
                        verify_game.make_move(cap.from_field, cap.to_field,
                                            cap.captured_fields, cap.promotes)
                        break
            else:
                # Movimento simples
                parts = notation.split(' → ')
                if len(parts) == 2:
                    from_alg = parts[0]
                    to_alg = parts[1].replace(' ♛', '')

                    from_f = Pos64.from_algebraic(from_alg).field
                    to_f = Pos64.from_algebraic(to_alg).field
                    promotes = '♛' in notation

                    verify_game.make_move(from_f, to_f, [], promotes)

            print_position_summary(verify_game)
            print()

        verify_game.print_board("POSIÇÃO FINAL:")

        if len(verify_game.black_men) + len(verify_game.black_kings) == 0:
            print("✅ TODAS AS PEÇAS PRETAS ELIMINADAS!")
        else:
            print(f"⚠️  Pretas ainda têm peças: {len(verify_game.black_men) + len(verify_game.black_kings)}")

else:
    print("❌ Nenhuma sequência vencedora encontrada até profundidade 6")
    print()
    print("Isso pode indicar:")
    print("  1. Bug no motor (regra não implementada corretamente)")
    print("  2. Solução requer mais de 6 lances")
    print("  3. Interpretação incorreta da posição FEN")
