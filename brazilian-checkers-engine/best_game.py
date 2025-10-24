"""
Jogar partida completa começando com o melhor movimento: b2 → c3
"""

from src.pos64 import Pos64
from play_full_game import GameState

white_start = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_start = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

game = GameState(white_start, black_start, "white")

print("="*70)
print("PARTIDA COMPLETA COMEÇANDO COM: b2 → c3")
print("="*70)

game.print_board("POSIÇÃO INICIAL:")

# Lance 1: b2 → c3 (campo 25 → 22)
print("1. white: b2 → c3")
game.make_move(25, 22)

moves_notation = ["1. b2 → c3"]

# Continuar jogando
while not game.game_over and game.move_count < 50:
    # Obter capturas
    captures = game.get_all_captures()

    if captures:
        # Escolher melhor captura
        best = max(captures, key=lambda c: len(c[1]))
        from_field, captured_fields, to_field = best

        from_alg = Pos64(from_field).to_algebraic()
        to_alg = Pos64(to_field).to_algebraic()

        notation = from_alg
        for cap in captured_fields:
            notation += f" x {Pos64(cap).to_algebraic()}"
        notation += f" → {to_alg}"

        print(f"{game.move_count + 1}. {game.turn}: {notation}")
        moves_notation.append(f"{game.move_count + 1}. {notation}")

        game.make_move(from_field, to_field, captured_fields)

    else:
        moves = game.get_simple_moves()
        if not moves:
            game.game_over = True
            game.winner = "black" if game.turn == "white" else "white"
            break

        # Escolher movimento (avançar centralmente)
        best_move = moves[0]
        for move in moves:
            if game.turn == "white" and move[1] < best_move[1]:
                best_move = move
            elif game.turn == "black" and move[1] > best_move[1]:
                best_move = move

        from_field, to_field = best_move
        from_alg = Pos64(from_field).to_algebraic()
        to_alg = Pos64(to_field).to_algebraic()

        print(f"{game.move_count + 1}. {game.turn}: {from_alg} → {to_alg}")
        moves_notation.append(f"{game.move_count + 1}. {from_alg} → {to_alg}")

        game.make_move(from_field, to_field)

game.print_board("POSIÇÃO FINAL:")

print("="*70)
print("RESULTADO")
print("="*70)
if game.winner:
    print(f"Vencedor: {game.winner.upper()}")
else:
    print("Partida interrompida")

print()
print("="*70)
print("NOTAÇÃO ALGÉBRICA COMPLETA")
print("="*70)
for notation in moves_notation:
    print(notation)

print()
print("="*70)
print("ANÁLISE")
print("="*70)
print(f"Total de lances: {game.move_count}")
print(f"Peças brancas: {len(game.white)}")
print(f"Peças pretas: {len(game.black)}")
print(f"Diferença: {len(game.white) - len(game.black):+d}")
