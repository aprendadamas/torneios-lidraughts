"""
Busca mais profunda para Exercício #14
Tentando até profundidade 10
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64
from typing import List, Tuple, Optional

def minimax_search_winning(game, depth, max_depth, sequence, memo=None):
    """
    Busca minimax focada em encontrar VITÓRIA
    Retorna (score, sequência, é_vitória)
    """
    if memo is None:
        memo = {}

    # Criar hash da posição
    state = (
        frozenset(game.white_men), frozenset(game.white_kings),
        frozenset(game.black_men), frozenset(game.black_kings),
        game.turn, depth
    )

    if state in memo:
        return memo[state]

    # Verificar vitória
    b_total = len(game.black_men) + len(game.black_kings)
    w_total = len(game.white_men) + len(game.white_kings)

    if b_total == 0:
        result = (10000, sequence, True)
        memo[state] = result
        return result

    if w_total == 0:
        result = (-10000, sequence, False)
        memo[state] = result
        return result

    if depth >= max_depth:
        material = (w_total - b_total) * 100
        result = (material, sequence, False)
        memo[state] = result
        return result

    # Capturas obrigatórias
    caps = game.find_all_captures()

    if caps:
        best_score = -20000 if game.turn == "white" else 20000
        best_seq = sequence
        is_winning = False

        for cap in caps:
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            if cap.promotes:
                notation += " ♛"

            move_str = f"{game.turn}: {notation}"

            new_game = game.copy()
            new_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

            score, seq, win = minimax_search_winning(
                new_game, depth + 1, max_depth, sequence + [move_str], memo
            )

            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_seq = seq
                    is_winning = win
                    if win:
                        break  # Vitória encontrada
            else:
                if score < best_score:
                    best_score = score
                    best_seq = seq
                    is_winning = win

        result = (best_score, best_seq, is_winning)
        memo[state] = result
        return result

    # Movimentos simples
    moves = game.find_simple_moves()

    if not moves:
        # Sem movimentos
        if game.turn == "white":
            result = (-10000, sequence, False)
        else:
            result = (10000, sequence, True)
        memo[state] = result
        return result

    best_score = -20000 if game.turn == "white" else 20000
    best_seq = sequence
    is_winning = False

    for from_f, to_f, promotes in moves:
        notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
        if promotes:
            notation += " ♛"

        move_str = f"{game.turn}: {notation}"

        new_game = game.copy()
        new_game.make_move(from_f, to_f, [], promotes)

        score, seq, win = minimax_search_winning(
            new_game, depth + 1, max_depth, sequence + [move_str], memo
        )

        if game.turn == "white":
            if score > best_score:
                best_score = score
                best_seq = seq
                is_winning = win
                if win:
                    break
        else:
            if score < best_score:
                best_score = score
                best_seq = seq
                is_winning = win

    result = (best_score, best_seq, is_winning)
    memo[state] = result
    return result


print("=" * 80)
print("EXERCÍCIO #14 - BUSCA PROFUNDA COM MEMOIZAÇÃO")
print("=" * 80)
print()

white = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white, black)
game.print_board("POSIÇÃO INICIAL:")

print("Buscando até profundidade 10...")
print("(Usando memoização para otimizar)")
print()

score, sequence, is_winning = minimax_search_winning(game, 0, 10, [])

print("=" * 80)
print("RESULTADO")
print("=" * 80)
print()

print(f"Score: {score}")
print(f"É vitória: {is_winning}")
print()

if sequence:
    print("Melhor sequência encontrada:")
    for i, move in enumerate(sequence, 1):
        print(f"  {i}. {move}")
    print()

    if is_winning:
        print("✅ SEQUÊNCIA VENCEDORA ENCONTRADA!")
        print()
        print(f"Vitória em {len(sequence)} lances totais")

        # Contar lances das brancas
        white_moves = sum(1 for m in sequence if m.startswith("white:"))
        print(f"Movimentos das brancas: {white_moves}")
    else:
        print("⚠️  Não encontrou vitória forçada até profundidade 10")
else:
    print("❌ Nenhuma sequência encontrada")

# Verificar a sequência executando
if sequence and is_winning:
    print()
    print("=" * 80)
    print("VERIFICANDO SEQUÊNCIA")
    print("=" * 80)
    print()

    verify_game = BrazilianGameComplete(white, black)

    for move in sequence:
        parts = move.split(": ", 1)
        if len(parts) == 2:
            turn, notation = parts

            if 'x' in notation:
                caps = verify_game.find_all_captures()
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
                from_alg, to_alg = notation.replace(' ♛', '').split(' → ')
                from_f = Pos64.from_algebraic(from_alg).field
                to_f = Pos64.from_algebraic(to_alg).field
                promotes = '♛' in notation
                verify_game.make_move(from_f, to_f, [], promotes)

    verify_game.print_board("RESULTADO FINAL:")

    if len(verify_game.black_men) + len(verify_game.black_kings) == 0:
        print("✅ TODAS AS PEÇAS PRETAS ELIMINADAS!")
    else:
        print(f"Peças restantes: W={len(verify_game.white_men) + len(verify_game.white_kings)}, "
              f"B={len(verify_game.black_men) + len(verify_game.black_kings)}")
