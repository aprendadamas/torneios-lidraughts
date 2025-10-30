"""
Debug: Por que a5→b6 não é escolhido?

Analisar:
1. a5→b6 está na lista de movimentos?
2. Qual score a5→b6 recebe?
3. Endgame evaluator está detectando peões bloqueados?
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v3 import EndgameEvaluator, ImprovedTacticalEvaluationV3
from src.pos64 import Pos64
import copy

print("=" * 70)
print("DEBUG: Análise de a5→b6")
print("=" * 70)
print()

# Posição inicial
white_men = {22, 24, 20, 13, 15, 11}
white_kings = {29}
black_men = {14, 12}
black_kings = {30, 3}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print("=" * 70)
print("PASSO 1: Verificar movimentos disponíveis")
print("=" * 70)
print()

captures = game.find_all_captures()
if captures:
    print(f"❌ HÁ {len(captures)} CAPTURAS OBRIGATÓRIAS")
    for cap in captures:
        print(f"  {Pos64(cap.from_field).to_algebraic()} → ...")
else:
    simple_moves = game.find_simple_moves()
    print(f"✓ {len(simple_moves)} movimentos simples disponíveis:")

    a5b6_found = False
    for from_field, to_field, promotes in simple_moves:
        from_pos = Pos64(from_field).to_algebraic()
        to_pos = Pos64(to_field).to_algebraic()

        marker = ""
        if from_pos == "a5" and to_pos == "b6":
            marker = " ← ESTE É O MOVIMENTO CORRETO!"
            a5b6_found = True

        print(f"  {from_pos} → {to_pos}{marker}")

    print()
    if a5b6_found:
        print("✓ a5→b6 ESTÁ NA LISTA")
    else:
        print("❌ a5→b6 NÃO ESTÁ NA LISTA!")

print()
print("=" * 70)
print("PASSO 2: Simular a5→b6 e resposta c5xa7")
print("=" * 70)
print()

# Lance 1 brancas: a5→b6
game_after_a5b6 = copy.deepcopy(game)
game_after_a5b6.make_move(13, 9, [], False)  # a5(13) → b6(9)
game_after_a5b6.print_board("Após a5→b6")

print()
evaluator = ImprovedTacticalEvaluationV3()
score_after_a5b6 = evaluator.evaluate_position(game_after_a5b6)
print(f"Avaliação após a5→b6: {score_after_a5b6:+.0f} (perspectiva brancas)")

print()
print("Agora pretas devem responder...")
captures_black = game_after_a5b6.find_all_captures()
if captures_black:
    print(f"Pretas TÊM {len(captures_black)} captura(s) obrigatória(s):")
    for cap in captures_black:
        from_pos = Pos64(cap.from_field).to_algebraic()
        to_pos = Pos64(cap.to_field).to_algebraic()

        print(f"  {from_pos} captura e vai para {to_pos}")

        # Simular esta captura
        if from_pos == "c5" and to_pos == "a7":
            print(f"    ^ Esta é a resposta da solução!")

print()

# Lance 1 pretas: c5xa7
game_after_c5xa7 = copy.deepcopy(game_after_a5b6)
game_after_c5xa7.make_move(14, 5, [9], False)  # c5(14) x b6(9) → a7(5)
game_after_c5xa7.print_board("Após c5xa7 (peão em a7 BLOQUEADO?)")

print()
score_after_c5xa7 = evaluator.evaluate_position(game_after_c5xa7)
print(f"Avaliação após c5xa7: {score_after_c5xa7:+.0f} (perspectiva brancas)")

print()
print("=" * 70)
print("PASSO 3: Verificar se peão em a7 está bloqueado")
print("=" * 70)
print()

# Verificar se a7 está bloqueado
a7_field = 5
is_blocked = EndgameEvaluator.is_pawn_blocked(game_after_c5xa7, a7_field, "black")

print(f"Peão em a7 (field {a7_field}) está bloqueado? {is_blocked}")

if not is_blocked:
    print("  Movimentos disponíveis para a7:")
    # Tentar mover a7
    next_moves = game_after_c5xa7.find_simple_moves()
    for from_field, to_field, promotes in next_moves:
        if from_field == a7_field:
            print(f"    a7 → {Pos64(to_field).to_algebraic()}")

print()
print("=" * 70)
print("PASSO 4: Avaliar endgame após sequência completa")
print("=" * 70)
print()

print("Simulando todos os 7 lances da solução...")
print()

game_final = copy.deepcopy(game)

moves = [
    (13, 9, [], False, "1. a5→b6"),
    (14, 5, [9], False, "1...c5xa7"),
    (22, 17, [], False, "2. c3→b4"),
    (3, 21, [17], False, "2...f8xa3"),
    (11, 8, [], False, "3. f6→g7"),
    (12, 3, [8], True, "3...h6xf8♛"),
    (15, 10, [], False, "4. e5→d6"),
    (21, 7, [10], False, "4...a3xe7"),
    (29, 8, [], False, "5. a1→g7"),
    (3, 12, [20], False, "5...f8xh6"),
    (24, 19, [], False, "6. g3→f4"),
    (30, 16, [19], False, "6...c1xg5"),
    # Move 7 é uma captura múltipla: h4 x f4/g5 x e7 → d8♛
    # Preciso verificar os campos exatos
]

for i, (from_f, to_f, captured, promotes, notation) in enumerate(moves, 1):
    game_final.make_move(from_f, to_f, captured, promotes)
    print(f"Lance {i}: {notation}")

print()
game_final.print_board("Posição após 7 meio-lances")

print()
score_final = evaluator.evaluate_position(game_final)
print(f"Avaliação: {score_final:+.0f}")

# Verificar endgame
endgame_score = EndgameEvaluator.evaluate_endgame(game_final)
if endgame_score is not None:
    print(f"Endgame evaluator retornou: {endgame_score:+.0f}")
    print()
    if abs(endgame_score) >= 9000:
        print("✓ Endgame evaluator reconhece vitória forçada!")
    else:
        print(f"⚠️  Endgame score não indica vitória forçada")
else:
    print("⚠️  Endgame evaluator não foi ativado")

print()
print("=" * 70)
print("ANÁLISE FINAL")
print("=" * 70)
print()

print("Motor deveria:")
print("1. Encontrar a5→b6 na lista de movimentos ✓")
print("2. Buscar até depth 14+ para ver posição final ✓ (motor busca depth 16)")
print("3. Endgame evaluator detectar peões bloqueados ?")
print("4. Propagar score +9999 de volta para a5→b6 ?")
print()

print("Se endgame evaluator NÃO detectar peões bloqueados,")
print("então a5→b6 será avaliado apenas por material (+100~200),")
print("o que não é suficiente para superar g3→f4.")
print()
