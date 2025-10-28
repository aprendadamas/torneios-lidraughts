"""
Exercício #14 - Busca profundidade 18
Para garantir que encontramos toda a sequência vencedora
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - BUSCA PROFUNDIDADE 18")
print("=" * 70)
print()

white_men = {30, 27, 23, 18, 19, 20}
black_men = {21, 17, 11, 12, 6, 7}

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Melhor lance: f4 → g5")
print()

# Executar f4 → g5
game.make_move(19, 16, [], False)

print("Após f4 → g5:")
print(f"  Turno: {game.turn}")
print()

# Buscar com profundidade 18 para obter sequência completa
print("Buscando com profundidade 18...")
engine = TacticalSearchEngine()
_, score, sequence = engine.search_best_move(game, max_depth=18)

print(f"Score (ponto de vista das pretas): {score}")
print(f"Score das brancas: {-score}")
print(f"Nós pesquisados: {engine.nodes_searched}")
print()

if -score >= 9000:
    print("✅ VITÓRIA FORÇADA CONFIRMADA para as BRANCAS!")
else:
    print(f"⚠️  Score: {-score}")

print()
print("=" * 70)
print("SEQUÊNCIA COMPLETA (até 30 lances)")
print("=" * 70)
print()

full_sequence = ["f4 → g5"] + sequence[:30]

for i, move in enumerate(full_sequence, 1):
    print(f"{i:2d}. {move}")

# Agora simular toda a sequência para verificar
print()
print("=" * 70)
print("SIMULANDO TODA A SEQUÊNCIA")
print("=" * 70)
print()

# Resetar o jogo
game = BrazilianGameComplete(white_men, black_men)

move_count = 0

for i, move_str in enumerate(full_sequence, 1):
    move_count = i

    if i > 50:
        print("Limite de 50 lances atingido")
        break

    print(f"Lance {i}: {move_str}")

    # Executar
    if ' x ' in move_str:
        # Captura
        caps = game.find_all_captures()
        executed = False

        for cap in caps:
            cap_notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                cap_notation += f" x {Pos64(cf).to_algebraic()}"
            cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

            if move_str.startswith(cap_notation.split(' ♛')[0]):
                game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                executed = True
                break

        if not executed:
            print(f"  ⚠️  Erro ao executar captura")
            break
    else:
        # Movimento simples
        parts = move_str.split(' → ')
        if len(parts) == 2:
            from_alg = parts[0]
            to_alg = parts[1].replace(' ♛', '')

            try:
                from_f = Pos64.from_algebraic(from_alg).field
                to_f = Pos64.from_algebraic(to_alg).field
                promotes = '♛' in move_str

                game.make_move(from_f, to_f, [], promotes)
            except:
                print(f"  ⚠️  Erro ao executar movimento")
                break

    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)

    if i % 5 == 0 or b_total == 0 or i <= 3:
        game.print_board(f"Após lance {i}")
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
print("RESULTADO FINAL")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Lances executados: {move_count}")
print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print()

if b_total == 0:
    print("✅ EXERCÍCIO #14 RESOLVIDO!")
    print("✅ Solução: f4 → g5")
    print(f"✅ Vitória em {move_count} lances")
elif w_total > b_total:
    print(f"✅ Brancas com vantagem: +{w_total - b_total}")
else:
    print(f"⚠️  Material: B={w_total} P={b_total}")
