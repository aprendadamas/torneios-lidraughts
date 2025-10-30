"""
Simular TODA a solução do Exercise #1 (14 meio-lances)

Solução do usuário:
1. a5-b6 c5xa7
2. c3-b4 f8xa3
3. f6-g7 h6xf8
4. e5-d6 a3xe7
5. a1-g7 f8xh6
6. g3-f4 c1xg5
7. h4xf6xd8

Preciso descobrir a posição EXATA final para entender o que "bloqueado" significa.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v3 import EndgameEvaluator, ImprovedTacticalEvaluationV3
from src.pos64 import Pos64

print("=" * 70)
print("SIMULAÇÃO COMPLETA: Exercise #1")
print("=" * 70)
print()

# Posição inicial
white_men = {22, 24, 20, 13, 15, 11}  # c3, g3, h4, a5, e5, f6
white_kings = {29}  # a1
black_men = {14, 12}  # c5, h6
black_kings = {30, 3}  # c1, f8

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Posição Inicial")

print()
print("=" * 70)
print("Simulando a solução lance por lance")
print("=" * 70)
print()

# Vou tentar deduzir os campos exatos de cada lance
# Usando o motor para encontrar as capturas corretas

move_num = 1

# Lance 1 brancas: a5→b6
print(f"{move_num}. a5→b6", end="")
game.make_move(13, 9, [], False)  # a5(13) → b6(9)

# Lance 1 pretas: c5xa7
print(" c5xa7")
captures = game.find_all_captures()
# Deve ser c5 captura b6 indo para a7
game.make_move(14, 5, [9], False)  # c5(14) x b6(9) → a7(5)

# Lance 2 brancas: c3→b4
move_num += 1
print(f"{move_num}. c3→b4", end="")
game.make_move(22, 17, [], False)  # c3(22) → b4(17)

# Lance 2 pretas: f8xa3
print(" f8xa3")
# f8 captura b4 indo para a3
game.make_move(3, 21, [17], False)  # f8(3) x b4(17) → a3(21)

# Lance 3 brancas: f6→g7
move_num += 1
print(f"{move_num}. f6→g7", end="")
game.make_move(11, 8, [], False)  # f6(11) → g7(8)

# Lance 3 pretas: h6xf8
print(" h6xf8")
# h6 captura g7 indo para f8 (PROMOVE para dama!)
game.make_move(12, 3, [8], True)  # h6(12) x g7(8) → f8(3) ♛

# Lance 4 brancas: e5→d6
move_num += 1
print(f"{move_num}. e5→d6", end="")
game.make_move(15, 10, [], False)  # e5(15) → d6(10)

# Lance 4 pretas: a3xe7
print(" a3xe7")
# a3 captura d6 indo para e7
game.make_move(21, 7, [10], False)  # a3(21) x d6(10) → e7(7)

# Lance 5 brancas: a1→g7
move_num += 1
print(f"{move_num}. a1→g7", end="")
# Dama a1 vai para g7
game.make_move(29, 8, [], False)  # a1(29) → g7(8)

# Lance 5 pretas: f8xh6
print(" f8xh6")
# f8 captura algo indo para h6
# Deve capturar h4(20) indo para h6(12)
game.make_move(3, 12, [20], False)  # f8(3) x h4(20) → h6(12)

# Lance 6 brancas: g3→f4
move_num += 1
print(f"{move_num}. g3→f4", end="")
game.make_move(24, 19, [], False)  # g3(24) → f4(19)

# Lance 6 pretas: c1xg5
print(" c1xg5")
# c1 captura f4 indo para g5
game.make_move(30, 16, [19], False)  # c1(30) x f4(19) → g5(16)

# Lance 7 brancas: h4xf6xd8
move_num += 1
print(f"{move_num}. ???")
print()
print("PROBLEMA: h4 já foi capturado no lance 5...")
print("Vou mostrar a posição atual:")
print()

game.print_board("Após 12 meio-lances")

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

evaluator = ImprovedTacticalEvaluationV3()
score = evaluator.evaluate_position(game)
print(f"Avaliação: {score:+.0f}")

endgame_score = EndgameEvaluator.evaluate_endgame(game)
if endgame_score:
    print(f"Endgame score: {endgame_score:+.0f}")
else:
    print("Endgame evaluator: None")

print()
print("Peças brancas:")
print(f"  Peões: {game.white_men}")
print(f"  Damas: {game.white_kings}")

print()
print("Peças pretas:")
print(f"  Peões: {game.black_men}")
print(f"  Damas: {game.black_kings}")

print()
print("NOTA: A solução do usuário parece ter um erro, ou estou")
print("interpretando a notação incorretamente. h4 não pode capturar")
print("no lance 7 se já foi capturado no lance 5.")
print()
print("Vou tentar uma abordagem diferente: usar o motor para")
print("DESCOBRIR a solução completa automaticamente...")
