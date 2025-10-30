"""
Debug para identificar fonte exata dos scores infinitos
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
import math

# Contadores de debug
inf_sources = {
    'tt_exact': 0,
    'tt_cutoff': 0,
    'quiescence': 0,
    'static_eval': 0,
    'null_move': 0,
    'no_moves': 0,
    'search_loop': 0,
    'search_root': 0
}

# Patch _negamax para detectar infinitos
original_negamax = ProfessionalEngine._negamax

def debug_negamax(self, game, depth, alpha, beta, zobrist_key, allow_null=True):
    result_score, result_pv = original_negamax(self, game, depth, alpha, beta, zobrist_key, allow_null)

    if math.isinf(result_score) or abs(result_score) > 100000:
        # Score infinito retornado - tentar identificar fonte
        print(f"⚠️  _negamax retornou {result_score:+.0f} at depth={depth}, turn={game.turn}")

    return result_score, result_pv

# Patch _search_root
original_search_root = ProfessionalEngine._search_root

def debug_search_root(self, game, depth, alpha, beta, zobrist_key):
    result_score, result_move, result_pv = original_search_root(self, game, depth, alpha, beta, zobrist_key)

    if math.isinf(result_score) or abs(result_score) > 100000:
        print(f"⚠️  _search_root retornou {result_score:+.0f} at depth={depth}, turn={game.turn}")

    return result_score, result_move, result_pv

# Aplicar patches
ProfessionalEngine._negamax = debug_negamax
ProfessionalEngine._search_root = debug_search_root

print("=" * 70)
print("DEBUG: Identificar fonte de scores infinitos")
print("=" * 70)
print()

# Posição do exercício #1
white_men = {22, 24, 20, 13, 15, 11}
white_kings = {29}
black_men = {14, 12}
black_kings = {30, 3}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print("Testando depths 1-8 com debug...")
print()

motor = ProfessionalEngine(tt_size_mb=64)

try:
    best_move, score, pv = motor.search_best_move(game, max_depth=8)

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    print(f"Melhor lance: {best_move}")
    print(f"Score: {score:+.0f}")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print()
