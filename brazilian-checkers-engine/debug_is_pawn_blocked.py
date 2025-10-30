"""
Debug detalhado: Por que is_pawn_blocked() retorna False?

Vou criar um peão que DEFINITIVAMENTE não pode se mover e rastrear
passo a passo o que is_pawn_blocked() faz.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v3 import EndgameEvaluator
from src.pos64 import Pos64

print("=" * 70)
print("DEBUG DETALHADO: is_pawn_blocked()")
print("=" * 70)
print()

# Configuração: Peão preto em a7, paredes em todos os lados
# a7 não pode avançar (linha 8 é limite do tabuleiro)
# a7 não pode capturar (sem peças brancas adjacentes)

white_men = set()
white_kings = set()
black_men = {5}  # a7
black_kings = set()

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("Peão preto ISOLADO em a7")

print()
print("Movimentos possíveis:")
simple_moves = game.find_simple_moves()
print(f"  Simple moves: {len(simple_moves)}")
for from_f, to_f, promotes in simple_moves:
    print(f"    {Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}")

captures = game.find_all_captures()
print(f"  Captures: {len(captures)}")

print()
print("=" * 70)
print("Chamar is_pawn_blocked(game, field=5, color='black')")
print("=" * 70)
print()

# Inserir código de is_pawn_blocked manualmente para debug
field = 5
color = "black"

pos = Pos64(field)
all_occupied = game.white_men | game.black_men | game.white_kings | game.black_kings

print(f"Field: {field} ({pos.to_algebraic()})")
print(f"Color: {color}")
print(f"All occupied: {all_occupied}")
print()

# Pretos avançam para baixo (y maior)
print("PASSO 1: Verificar se pode avançar")
forward_moves = [pos.move_down_left(), pos.move_down_right()]
print(f"Forward moves possíveis: {forward_moves}")

can_advance = False
for next_pos in forward_moves:
    if next_pos:
        print(f"  {next_pos.to_algebraic()} (field {next_pos.field}): ", end="")
        if next_pos.field not in all_occupied:
            print("LIVRE - pode avançar!")
            can_advance = True
        else:
            print("ocupado")
    else:
        print(f"  None (fora do tabuleiro)")

print(f"\ncan_advance = {can_advance}")

if can_advance:
    print("RETORNA False (não bloqueado) - FIM")
else:
    print("Continua para PASSO 2...")
    print()

    print("PASSO 2: Verificar se pode capturar")

    enemy_pieces = game.white_men | game.white_kings
    print(f"Enemy pieces: {enemy_pieces}")

    all_directions = [
        (pos.move_up_left, "up_left"),
        (pos.move_up_right, "up_right"),
        (pos.move_down_left, "down_left"),
        (pos.move_down_right, "down_right")
    ]

    can_capture = False

    for move_func, direction in all_directions:
        print(f"\n  Direção: {direction}")
        adjacent = move_func()

        if not adjacent:
            print(f"    Adjacent: None (fora do tabuleiro)")
            continue

        print(f"    Adjacent: {adjacent.to_algebraic()} (field {adjacent.field})")

        if adjacent.field in enemy_pieces:
            print(f"    ✓ Há inimigo em {adjacent.to_algebraic()}")

            # Continuar na mesma direção
            beyond = getattr(Pos64(adjacent.field), f"move_{direction}")()

            if beyond:
                print(f"    Beyond: {beyond.to_algebraic()} (field {beyond.field})")
                if beyond.field not in all_occupied:
                    print(f"    ✓✓ Beyond está LIVRE - PODE CAPTURAR!")
                    can_capture = True
                    break
                else:
                    print(f"    Beyond está ocupado - não pode capturar nesta direção")
            else:
                print(f"    Beyond: None (fora do tabuleiro)")
        else:
            print(f"    Sem inimigo em {adjacent.to_algebraic()}")

    print()
    if can_capture:
        print("RETORNA False (pode capturar, não bloqueado)")
    else:
        print("RETORNA True (BLOQUEADO)")

print()
print("=" * 70)
print("Resultado real de is_pawn_blocked():")
result = EndgameEvaluator.is_pawn_blocked(game, field, color)
print(f"is_pawn_blocked(game, {field}, '{color}') = {result}")
print("=" * 70)
print()

if result:
    print("✓ is_pawn_blocked retornou True - CORRETO")
else:
    print("❌ is_pawn_blocked retornou False - INCORRETO")
    print()
    print("BUG CONFIRMADO!")
