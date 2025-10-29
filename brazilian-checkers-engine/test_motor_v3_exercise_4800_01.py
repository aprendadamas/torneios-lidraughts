"""
Teste do Motor V3 no Exercício #1 (4800 Avançado)

Verificar se as melhorias permitem encontrar a5→b6
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v3 import ImprovedTacticalSearchEngineV3, EndgameEvaluator
from src.pos64 import Pos64

print("=" * 70)
print("TESTE MOTOR V3 - EXERCÍCIO #1 (4800 AVANÇADO)")
print("=" * 70)
print()

# Posição inicial
white_men = {22, 24, 20, 13, 15, 11}  # c3, g3, h4, a5, e5, f6
white_kings = {29}  # a1
black_men = {14, 12}  # c5, h6
black_kings = {30, 3}  # c1, f8

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print("Material:")
print(f"  Brancas: 1♛ + 6 peões = 7 peças")
print(f"  Pretas: 2♛ + 2 peões = 4 peças")
print()

# Testar detecção de bloqueio
print("=" * 70)
print("TESTE: Detecção de Peões Bloqueados")
print("=" * 70)
print()

for field in game.white_men:
    pos = Pos64(field).to_algebraic()
    blocked = EndgameEvaluator.is_pawn_blocked(game, field, "white")
    print(f"Peão branco em {pos}: {'BLOQUEADO' if blocked else 'móvel'}")

print()

for field in game.black_men:
    pos = Pos64(field).to_algebraic()
    blocked = EndgameEvaluator.is_pawn_blocked(game, field, "black")
    print(f"Peão preto em {pos}: {'BLOQUEADO' if blocked else 'móvel'}")

print()
print("=" * 70)
print("TESTE: Motor V3 com Profundidades Crescentes")
print("=" * 70)
print()

motor_v3 = ImprovedTacticalSearchEngineV3()

# Testar em profundidades crescentes
for depth in [6, 8, 10, 12]:
    print(f"\n--- Profundidade {depth} ---")

    try:
        best_move, score, pv_sequence = motor_v3.search_best_move(game, max_depth=depth)

        print(f"Melhor lance: {best_move}")
        print(f"Avaliação: {score:+.0f}")
        print(f"Nós pesquisados: {motor_v3.nodes_searched:,}")

        # Verificar se encontrou o lance correto
        if "a5" in best_move and "b6" in best_move:
            print("✅ ACERTOU! Encontrou a5→b6")
        else:
            print(f"❌ Errou. Esperado: a5→b6, Encontrado: {best_move}")

        if pv_sequence and len(pv_sequence) > 1:
            print(f"\nVariante principal ({len(pv_sequence)} lances):")
            for i, move in enumerate(pv_sequence[:10], 1):
                print(f"  {i}. {move}")

    except KeyboardInterrupt:
        print("\n⚠️  Busca interrompida (Ctrl+C)")
        break
    except Exception as e:
        print(f"❌ Erro durante busca: {e}")
        import traceback
        traceback.print_exc()
        break

print()
print("=" * 70)
print("CONCLUSÃO")
print("=" * 70)
print()

if "a5" in best_move and "b6" in best_move:
    print("✅ MOTOR V3 FUNCIONOU!")
    print(f"   Encontrou o lance correto: a5→b6")
    print(f"   Avaliação: {score:+.0f}")
    print()
    print("Melhorias que funcionaram:")
    print("  1. Detecção de peões bloqueados")
    print("  2. Avaliação de finais (dama vs peões)")
    print("  3. Maior sacrifice_tolerance (300pts vs 150pts)")
else:
    print("❌ Motor V3 ainda não encontrou")
    print(f"   Lance encontrado: {best_move}")
    print(f"   Lance correto: a5→b6")
    print()
    print("Possíveis problemas:")
    print("  - Profundidade ainda insuficiente (precisa 14 ply)")
    print("  - Sacrifice tolerance ainda não é suficiente")
    print("  - Poda alpha-beta cortando a linha vencedora")
    print()
    print("Próximos passos:")
    print("  - Aumentar ainda mais a profundidade")
    print("  - Implementar busca por extensões (quiescence search)")
    print("  - Usar ordenação de movimentos mais inteligente")

print()
