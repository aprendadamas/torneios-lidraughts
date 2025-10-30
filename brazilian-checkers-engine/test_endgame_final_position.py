"""
Teste: Endgame Evaluator reconhece posição final como vitória?

Posição final esperada (segundo usuário):
- Brancas: 1 dama
- Pretas: 2 peões BLOQUEADOS em a7 e d8

Score esperado: +9999 (vitória forçada para brancas)
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v3 import EndgameEvaluator, ImprovedTacticalEvaluationV3
from src.pos64 import Pos64

print("=" * 70)
print("TESTE: Endgame Evaluator - Posição Final Exercise #1")
print("=" * 70)
print()

# Vou tentar configurar a posição final descrita pelo usuário
# "1 queen vs 2 blocked pawns at a7 and d8"

# Tentar várias configurações possíveis
configurations = [
    {
        'name': 'Config 1: Dama em g7, peões em a7 e d8',
        'white_men': set(),
        'white_kings': {8},  # g7
        'black_men': {5, 4},  # a7, d8
        'black_kings': set()
    },
    {
        'name': 'Config 2: Dama em d8, peões em a7 e h6',
        'white_men': set(),
        'white_kings': {4},  # d8
        'black_men': {5, 12},  # a7, h6
        'black_kings': set()
    },
    {
        'name': 'Config 3: Dama em e7, peões em a7 e b8',
        'white_men': set(),
        'white_kings': {7},  # e7
        'black_men': {5, 4},  # a7, b8
        'black_kings': set()
    },
]

evaluator = ImprovedTacticalEvaluationV3()

for config in configurations:
    print("=" * 70)
    print(config['name'])
    print("=" * 70)

    game = BrazilianGameComplete(
        config['white_men'],
        config['black_men'],
        config['white_kings'],
        config['black_kings']
    )

    game.print_board("Configuração")
    print()

    # Avaliar
    score = evaluator.evaluate_position(game)
    print(f"ImprovedTacticalEvaluationV3.evaluate_position(): {score:+.0f}")

    # Endgame evaluator
    endgame_score = EndgameEvaluator.evaluate_endgame(game)
    if endgame_score is not None:
        print(f"EndgameEvaluator.evaluate_endgame(): {endgame_score:+.0f}")

        if abs(endgame_score) >= 9000:
            print("✓ RECONHECE COMO VITÓRIA FORÇADA!")
        else:
            print(f"⚠️  Score não indica vitória forçada")
    else:
        print("⚠️  Endgame evaluator retornou None (não ativado)")

    # Verificar se peões estão bloqueados
    print()
    print("Verificação de bloqueio:")
    for field in config['black_men']:
        is_blocked = EndgameEvaluator.is_pawn_blocked(game, field, "black")
        pos = Pos64(field).to_algebraic()
        print(f"  Peão em {pos} (field {field}): {'BLOQUEADO' if is_blocked else 'NÃO bloqueado'}")

    print()

print("=" * 70)
print("TESTE ADICIONAL: Criar situação clara de bloqueio")
print("=" * 70)
print()

# Criar uma situação onde é ÓBVIO que o peão está bloqueado
# Peão preto em a7, damas brancas controlando b8 e b6

white_men = set()
white_kings = {4, 10}  # b8, b6 - controlando escape de a7
black_men = {5}  # a7
black_kings = set()

game_clear = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game_clear.print_board("Peão a7 DEVE estar bloqueado")
print()

is_blocked_clear = EndgameEvaluator.is_pawn_blocked(game_clear, 5, "black")
print(f"Peão em a7 está bloqueado? {is_blocked_clear}")

if is_blocked_clear:
    print("✓ is_pawn_blocked FUNCIONA neste caso")
else:
    print("❌ BUG: a7 deveria estar bloqueado mas is_pawn_blocked retornou False")

    # Debug: verificar movimentos possíveis
    print()
    print("Debug: movimentos disponíveis para a7:")
    simple_moves = game_clear.find_simple_moves()
    for from_f, to_f, promotes in simple_moves:
        if from_f == 5:
            print(f"  a7 → {Pos64(to_f).to_algebraic()}")

    captures = game_clear.find_all_captures()
    for cap in captures:
        if cap.from_field == 5:
            print(f"  a7 captura → {Pos64(cap.to_field).to_algebraic()}")

print()
