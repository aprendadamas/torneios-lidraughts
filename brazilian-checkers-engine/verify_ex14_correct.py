"""
Verificar a solução CORRETA do Exercício #14
Usando os campos corretos!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #14 - VERIFICAÇÃO CORRETA")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Solução: f4 → g5")
print()

move_count = 0

# Lance 1: f4 → g5
move_count += 1
print(f"Lance {move_count}: BRANCAS jogam f4 → g5 (SACRIFÍCIO!)")
print(f"  f4 = campo {Pos64.from_algebraic('f4').field}")
print(f"  g5 = campo {Pos64.from_algebraic('g5').field}")
print()

game.make_move(19, 16, [], False)  # f4 (19) → g5 (16) - CORRIGIDO!
game.print_board(f"Após f4 → g5")

# Verificar capturas
caps = game.find_all_captures()
print()
print(f"Capturas obrigatórias para pretas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")

# Encontrar a captura dupla
best_cap = None
for cap in caps:
    if len(cap.captured_fields) >= 2:
        best_cap = cap
        break

if not best_cap:
    best_cap = max(caps, key=lambda c: len(c.captured_fields))

print()
print(f"Melhor captura: {len(best_cap.captured_fields)} peça(s)")
notation = Pos64(best_cap.from_field).to_algebraic()
for cf in best_cap.captured_fields:
    notation += f" x {Pos64(cf).to_algebraic()}"
notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
print(f"  {notation}")
print()

# Lance 2: Executar melhor captura
move_count += 1
print(f"Lance {move_count}: PRETAS capturam {notation}")
game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
game.print_board(f"Após captura")

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)
print()
print(f"Material: Brancas {w_total} vs Pretas {b_total}")
print()

# Continuar com busca tática para os próximos lances
from src.tactical_engine import TacticalSearchEngine

engine = TacticalSearchEngine()
_, score, sequence = engine.search_best_move(game, max_depth=12)

print("Busca tática da posição atual (profundidade 12):")
print(f"  Avaliação: {score}")
print(f"  Nós pesquisados: {engine.nodes_searched}")
print()

if score >= 9000:
    print("✅ VITÓRIA FORÇADA para as BRANCAS!")
elif score <= -9000:
    print("❌ Vitória forçada para as pretas")
elif score >= 500:
    print("✅ Grande vantagem para brancas")
elif score <= -500:
    print("⚠️  Grande vantagem para pretas")

print()
print("Continuação (primeiros 15 lances):")
for i, move in enumerate(sequence[:15], move_count + 1):
    print(f"  {i}. {move}")

print()
print("=" * 70)
print("SIMULAÇÃO COMPLETA DA SEQUÊNCIA")
print("=" * 70)
print()

# Executar toda a sequência
full_sequence = [notation] + sequence[:20]

for i, move_str in enumerate(full_sequence, move_count + 1):
    if i > move_count:
        print(f"\nLance {i}: {move_str}")

        # Parse e executar o movimento
        if ' x ' in move_str:
            # É captura
            caps = game.find_all_captures()
            for cap in caps:
                cap_notation = Pos64(cap.from_field).to_algebraic()
                for cf in cap.captured_fields:
                    cap_notation += f" x {Pos64(cf).to_algebraic()}"
                cap_notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                if move_str.startswith(cap_notation) or cap_notation in move_str:
                    game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                    break
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

        if i % 4 == 0 or b_total == 0 or w_total == 0:
            game.print_board(f"Posição após lance {i}")
            print(f"Material: B={w_total} P={b_total}")

        if b_total == 0:
            print()
            print("🏆 BRANCAS VENCERAM!")
            break

        if w_total == 0:
            print()
            print("❌ Pretas venceram")
            break

print()
print("=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material final: Brancas {w_total} vs Pretas {b_total}")
print()

if b_total == 0:
    print("✅ BRANCAS VENCERAM - Todas as peças pretas eliminadas!")
elif w_total > b_total + 1:
    print(f"✅ Brancas têm grande vantagem: +{w_total - b_total}")
elif w_total > b_total:
    print(f"✅ Brancas têm pequena vantagem: +{w_total - b_total}")
elif w_total == b_total:
    print("= Material equilibrado")
else:
    print(f"⚠️  Pretas têm vantagem: +{b_total - w_total}")
