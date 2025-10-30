"""
Motor V4 - Versão DEBUG com logging extensivo
Para identificar fonte dos scores infinitos
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64

# Patch para adicionar debug
original_negamax = ProfessionalEngine._negamax
original_quiescence = ProfessionalEngine._quiescence

debug_calls = []

def debug_negamax(self, game, depth, alpha, beta, zobrist_key, allow_null=True):
    """Versão com debug do negamax"""
    result_score, result_pv = original_negamax(self, game, depth, alpha, beta, zobrist_key, allow_null)

    # Log se retornar infinito
    if abs(result_score) > 9000:
        debug_calls.append({
            'function': 'negamax',
            'depth': depth,
            'score': result_score,
            'alpha': alpha,
            'beta': beta,
            'turn': game.turn
        })

    return result_score, result_pv

def debug_quiescence(self, game, alpha, beta, zobrist_key, ply=0):
    """Versão com debug do quiescence"""
    result = original_quiescence(self, game, alpha, beta, zobrist_key, ply)

    # Log se retornar infinito
    if abs(result) > 9000:
        debug_calls.append({
            'function': 'quiescence',
            'ply': ply,
            'score': result,
            'alpha': alpha,
            'beta': beta,
            'turn': game.turn
        })

    return result

# Aplicar patches
ProfessionalEngine._negamax = debug_negamax
ProfessionalEngine._quiescence = debug_quiescence

print("=" * 70)
print("DEBUG: Motor V4 com Logging Extensivo")
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
print("Testando profundidades 1-10 com debug ativado...")
print()

motor = ProfessionalEngine(tt_size_mb=64)

try:
    best_move, score, pv = motor.search_best_move(game, max_depth=10)

    print()
    print("=" * 70)
    print("ANÁLISE DE DEBUG")
    print("=" * 70)
    print()

    if debug_calls:
        print(f"Total de chamadas que retornaram score infinito: {len(debug_calls)}")
        print()

        # Agrupar por função
        by_function = {}
        for call in debug_calls:
            func = call['function']
            if func not in by_function:
                by_function[func] = []
            by_function[func].append(call)

        for func, calls in by_function.items():
            print(f"\n{func.upper()}: {len(calls)} chamadas com infinito")

            # Mostrar primeiras 5
            for i, call in enumerate(calls[:5], 1):
                print(f"  {i}. depth={call.get('depth', 'N/A')} "
                      f"ply={call.get('ply', 'N/A')} "
                      f"score={call['score']:+.0f} "
                      f"turn={call['turn']}")

        print()
        print("=" * 70)
        print("DIAGNÓSTICO")
        print("=" * 70)
        print()

        if len(by_function.get('quiescence', [])) > 0:
            print("⚠️  PROBLEMA IDENTIFICADO: Quiescence Search")
            print("   Quiescence está retornando scores infinitos")
            print("   Isso acontece quando não há capturas ou stand-pat retorna infinito")
            print()

        if len(by_function.get('negamax', [])) > 0:
            print("⚠️  PROBLEMA IDENTIFICADO: Negamax")
            print("   Negamax está retornando scores infinitos")
            print("   Verificar:")
            print("   - Condição de parada (depth <= 0)")
            print("   - Detecção de sem movimentos (-10000)")
            print("   - Propagação de scores da TT")
            print()
    else:
        print("✓ Nenhum score infinito detectado até depth 10")
        print("  Bug pode estar em profundidades maiores ou em aspiration windows")

    print()
    print(f"Resultado final: {best_move} (score: {score:+.0f})")

except Exception as e:
    print(f"\n❌ Erro: {e}")
    import traceback
    traceback.print_exc()

print()
