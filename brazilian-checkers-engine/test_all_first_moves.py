"""
Testar TODOS os primeiros movimentos possíveis das brancas
e simular 5-10 lances para ver qual é mais promissor
"""

from src.pos64 import Pos64
from play_full_game import GameState

white_start = {30, 25, 26, 19, 20}  # c1, b2, d2, f4, h4
black_start = {21, 10, 12, 7, 3}     # a3, d6, h6, e7, f8

print("="*70)
print("TESTAR TODOS OS PRIMEIROS MOVIMENTOS DAS BRANCAS")
print("="*70)
print()

# Obter todos os movimentos simples possíveis
initial_state = GameState(white_start, black_start, "white")

simple_moves = initial_state.get_simple_moves()
captures = initial_state.get_all_captures()

print(f"Movimentos simples disponíveis: {len(simple_moves)}")
print(f"Capturas disponíveis: {len(captures)}")
print()

# Testar cada movimento e jogar 15 lances
results = []

for from_field, to_field in simple_moves:
    from_alg = Pos64(from_field).to_algebraic()
    to_alg = Pos64(to_field).to_algebraic()

    # Criar novo jogo com esse movimento
    test_game = initial_state.copy()
    test_game.make_move(from_field, to_field)

    # Jogar mais 14 lances (total 15)
    for _ in range(14):
        if test_game.game_over:
            break

        # Priorizar capturas
        captures = test_game.get_all_captures()
        if captures:
            best = max(captures, key=lambda c: len(c[1]))
            test_game.make_move(best[0], best[2], best[1])
        else:
            moves = test_game.get_simple_moves()
            if not moves:
                test_game.game_over = True
                test_game.winner = "black" if test_game.turn == "white" else "white"
                break
            test_game.make_move(moves[0][0], moves[0][1])

    # Avaliar resultado
    white_pieces = len(test_game.white)
    black_pieces = len(test_game.black)
    material_diff = white_pieces - black_pieces

    status = ""
    if test_game.winner == "white":
        status = "✅ BRANCAS VENCEM"
    elif test_game.winner == "black":
        status = "❌ Pretas vencem"
    else:
        if material_diff > 0:
            status = f"⚪ Brancas +{material_diff}"
        elif material_diff < 0:
            status = f"⚫ Pretas +{-material_diff}"
        else:
            status = "⚖️  Igual"

    results.append({
        'move': f"{from_alg} → {to_alg}",
        'from': from_field,
        'to': to_field,
        'white': white_pieces,
        'black': black_pieces,
        'diff': material_diff,
        'status': status,
        'winner': test_game.winner
    })

    print(f"{from_alg} → {to_alg}: {status} (W:{white_pieces} B:{black_pieces})")

# Ordenar por diferença de material
results.sort(key=lambda r: r['diff'], reverse=True)

print()
print("="*70)
print("RANKING DOS MELHORES MOVIMENTOS")
print("="*70)
print()

for i, r in enumerate(results[:5], 1):
    print(f"{i}. {r['move']:15} {r['status']:20} (Material: {r['diff']:+d})")

print()
print("="*70)
print("MELHOR MOVIMENTO ENCONTRADO:")
print("="*70)
print()

best = results[0]
print(f"1. {best['move']}")
print(f"   Status: {best['status']}")
print(f"   Diferença de material: {best['diff']:+d}")

if best['winner'] == 'white':
    print(f"   🎯 Este movimento leva à VITÓRIA DAS BRANCAS!")

print()
print("Agora vou jogar uma partida completa começando com este movimento...")
print()
