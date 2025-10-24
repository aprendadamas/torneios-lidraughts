"""
Jogo completo de Damas Brasileiras desde a posição inicial
White vs Black - Simulação automática
"""

from src.brazilian_engine import BrazilianGame
from src.pos64 import Pos64

# Posição inicial do Brazilian/Russian
# FEN: W:W21,22,23,24,25,26,27,28,29,30,31,32:B1,2,3,4,5,6,7,8,9,10,11,12

white_initial = {21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32}
black_initial = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}

print("=" * 70)
print("PARTIDA COMPLETA DE DAMAS BRASILEIRAS")
print("DESDE A POSIÇÃO INICIAL")
print("=" * 70)
print()

game = BrazilianGame(white_initial, black_initial, "white")

print("POSIÇÃO INICIAL:")
print()
print("FEN: W:W21,22,23,24,25,26,27,28,29,30,31,32:B1,2,3,4,5,6,7,8,9,10,11,12")
print()
print("Brancas (campos 21-32):")
white_alg = [Pos64(f).to_algebraic() for f in sorted(white_initial)]
print(f"  {', '.join(white_alg)}")
print()
print("Pretas (campos 1-12):")
black_alg = [Pos64(f).to_algebraic() for f in sorted(black_initial)]
print(f"  {', '.join(black_alg)}")
print()

game.print_board()

# Lista de todos os lances
all_moves = []

# Jogar a partida
move_number = 0
max_moves = 100  # Limite para evitar loops infinitos

while not game.game_over and move_number < max_moves:
    move_number += 1

    # Verificar capturas (obrigatórias)
    captures = game.find_all_captures()

    if captures:
        # Estratégia: escolher a captura que captura mais peças
        # Se empate, escolher a que avança mais
        best_capture = max(captures, key=lambda c: (
            c.length(),
            -c.to_field if game.turn == "white" else c.to_field
        ))

        # Criar notação detalhada
        from_alg = Pos64(best_capture.from_field).to_algebraic()
        to_alg = Pos64(best_capture.to_field).to_algebraic()

        # Notação com todas as capturas
        notation = from_alg
        for captured_field in best_capture.captured_fields:
            notation += f" x {Pos64(captured_field).to_algebraic()}"
        notation += f" → {to_alg}"

        move_desc = f"{move_number}. {game.turn}: {notation}"
        all_moves.append(move_desc)

        # Executar captura
        game.make_move(best_capture.from_field, best_capture.to_field, best_capture.captured_fields)

    else:
        # Movimento simples
        moves = game.find_simple_moves()

        if not moves:
            # Sem movimentos disponíveis - fim de jogo
            game.game_over = True
            game.winner = "black" if game.turn == "white" else "white"
            break

        # Estratégia com variedade:
        # - Alternar entre avanços centrais e laterais
        # - Desenvolver peças de forma balanceada
        best_move = None
        best_score = -1000

        for from_field, to_field in moves:
            score = 0
            from_pos = Pos64(from_field)
            to_pos = Pos64(to_field)

            # Preferir avançar (campos menores para white, maiores para black)
            if game.turn == "white":
                score += (from_field - to_field) * 10
            else:
                score += (to_field - from_field) * 10

            # Preferir colunas centrais (x = 2 ou 3) nos primeiros lances
            if move_number < 15 and to_pos.x in [2, 3]:
                score += 3

            # Adicionar variação para evitar repetição
            score += (from_field * 7 + to_field * 3) % 5

            if score > best_score:
                best_score = score
                best_move = (from_field, to_field)

        if best_move:
            from_alg = Pos64(best_move[0]).to_algebraic()
            to_alg = Pos64(best_move[1]).to_algebraic()

            move_desc = f"{move_number}. {game.turn}: {from_alg} → {to_alg}"
            all_moves.append(move_desc)

            # Executar movimento
            game.make_move(best_move[0], best_move[1])

# Resultado
print()
print("=" * 70)
print("NOTAÇÃO ALGÉBRICA COMPLETA DA PARTIDA")
print("=" * 70)
print()

for move in all_moves:
    print(move)

print()
print("=" * 70)
print("RESULTADO")
print("=" * 70)
print()

if game.winner == "white":
    print(f"✅ BRANCAS VENCEM em {move_number} lances!")
elif game.winner == "black":
    print(f"✅ PRETAS VENCEM em {move_number} lances!")
elif move_number >= max_moves:
    print(f"⚖️  JOGO INTERROMPIDO após {max_moves} lances (limite atingido)")
    print(f"   Posição: Brancas {len(game.white)} peças, Pretas {len(game.black)} peças")
else:
    print(f"⚖️  EMPATE ou sem movimentos")

print()
game.print_board("POSIÇÃO FINAL:")

# Estatísticas
print("=" * 70)
print("ESTATÍSTICAS")
print("=" * 70)
print()
print(f"Total de lances: {move_number}")
print(f"Peças restantes - Brancas: {len(game.white)}, Pretas: {len(game.black)}")

# Contar capturas
captures_count = sum(1 for move in all_moves if ' x ' in move)
simple_moves_count = move_number - captures_count

print(f"Capturas: {captures_count}")
print(f"Movimentos simples: {simple_moves_count}")
print()

# Mostrar posição final em campos
if game.white:
    print(f"Brancas (campos): {sorted(game.white)}")
    print(f"Brancas (algébrico): {', '.join([Pos64(f).to_algebraic() for f in sorted(game.white)])}")
else:
    print("Brancas: (sem peças)")

print()

if game.black:
    print(f"Pretas (campos): {sorted(game.black)}")
    print(f"Pretas (algébrico): {', '.join([Pos64(f).to_algebraic() for f in sorted(game.black)])}")
else:
    print("Pretas: (sem peças)")
