"""
Busca profunda para encontrar sequência vencedora no Exercício #13
"""

from src.brazilian_engine import BrazilianGame
from src.pos64 import Pos64
from typing import List, Optional, Tuple

def minimax_search(game: BrazilianGame, depth: int, max_depth: int, moves_so_far: List[str]) -> Tuple[Optional[int], List[str]]:
    """
    Busca minimax para encontrar melhor sequência
    Retorna (score, sequência_de_lances)
    score: positivo se brancas vencem, negativo se pretas vencem
    """

    # Condições de parada
    if len(game.white) == 0:
        return (-1000, moves_so_far)

    if len(game.black) == 0:
        return (1000, moves_so_far)

    if depth >= max_depth:
        # Avaliar posição
        material = len(game.white) - len(game.black)
        return (material * 10, moves_so_far)

    # Verificar capturas (obrigatórias)
    captures = game.find_all_captures()

    if captures:
        # Há capturas obrigatórias
        best_score = -2000 if game.turn == "white" else 2000
        best_sequence = moves_so_far

        for cap in captures:
            # Fazer cópia do jogo
            new_game = BrazilianGame(game.white.copy(), game.black.copy(), game.turn)
            new_game.move_count = game.move_count

            # Criar notação do lance
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"

            move_str = f"{depth + 1}. {game.turn}: {notation}"

            # Executar lance
            new_game.make_move(cap.from_field, cap.to_field, cap.captured_fields)

            # Recursão
            score, sequence = minimax_search(new_game, depth + 1, max_depth, moves_so_far + [move_str])

            # Atualizar melhor
            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_sequence = sequence
            else:
                if score < best_score:
                    best_score = score
                    best_sequence = sequence

        return (best_score, best_sequence)

    else:
        # Movimentos simples
        moves = game.find_simple_moves()

        if not moves:
            # Sem movimentos legais
            if game.turn == "white":
                return (-1000, moves_so_far)
            else:
                return (1000, moves_so_far)

        best_score = -2000 if game.turn == "white" else 2000
        best_sequence = moves_so_far

        for from_f, to_f in moves:
            # Fazer cópia do jogo
            new_game = BrazilianGame(game.white.copy(), game.black.copy(), game.turn)
            new_game.move_count = game.move_count

            notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
            move_str = f"{depth + 1}. {game.turn}: {notation}"

            # Executar lance
            new_game.make_move(from_f, to_f)

            # Recursão
            score, sequence = minimax_search(new_game, depth + 1, max_depth, moves_so_far + [move_str])

            # Atualizar melhor
            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_sequence = sequence
            else:
                if score < best_score:
                    best_score = score
                    best_sequence = sequence

        return (best_score, best_sequence)


print("=" * 70)
print("EXERCÍCIO #13 - BUSCA PROFUNDA")
print("=" * 70)
print()

# Posição inicial
white = {30, 23, 20}  # c1, e3, h4
black = {21, 12, 7}   # a3, h6, e7

game = BrazilianGame(white, black, "white")
game.print_board("POSIÇÃO INICIAL:")

print("Iniciando busca profunda (profundidade 10)...")
print("Isso pode levar alguns segundos...")
print()

score, best_sequence = minimax_search(game, 0, 10, [])

print("=" * 70)
print("RESULTADO DA BUSCA")
print("=" * 70)
print()

print(f"Score final: {score}")
print()

if score >= 1000:
    print("✅ BRANCAS PODEM VENCER!")
elif score <= -1000:
    print("❌ Pretas vencem")
else:
    print(f"⚖️  Posição aproximadamente igual (vantagem: {'+' if score > 0 else ''}{score/10:.1f} peças)")

print()
print("Melhor sequência encontrada:")
for move in best_sequence:
    print(f"  {move}")
print()

# Verificar a sequência
if best_sequence:
    print("=" * 70)
    print("VERIFICAÇÃO DA SEQUÊNCIA")
    print("=" * 70)
    print()

    verify_game = BrazilianGame(white, black, "white")

    # Infelizmente não posso reproduzir automaticamente porque a sequência está em texto
    # Mas posso mostrar o resultado

    print("Para verificar manualmente, execute os lances acima.")
