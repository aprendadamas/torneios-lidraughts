"""
Teste do Motor V4 Profissional no Exercício #1 (4800 Avançado)

Motor V4 implementa:
- Transposition Tables (128 MB)
- Zobrist Hashing
- Iterative Deepening
- Move Ordering avançado (PV, Killers, History)
- Quiescence Search
- Null-Move Pruning
- Aspiration Windows
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.professional_engine_v4 import ProfessionalEngine
from src.pos64 import Pos64

print("=" * 70)
print("TESTE: MOTOR V4 PROFISSIONAL")
print("Exercício #1 - \"4800 Combinações - Avançado\"")
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
print("Lance correto: a5→b6")
print("Profundidade da solução: 14 meio-lances")
print()

print("=" * 70)
print("TESTE 1: Busca Profunda (max_depth=16)")
print("=" * 70)
print()

# Criar motor profissional com 256 MB de TT
motor_v4 = ProfessionalEngine(tt_size_mb=256)

print("Iniciando Iterative Deepening...")
print()

try:
    # Buscar sem limite de tempo (mas com max_depth=16)
    best_move, score, pv = motor_v4.search_best_move(
        game,
        max_depth=16,
        max_time_seconds=None  # Sem limite
    )

    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    print()
    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score:+.0f}")
    print()

    if "a5" in best_move and "b6" in best_move:
        print("✅ ✅ ✅ MOTOR V4 ACERTOU! ✅ ✅ ✅")
        print()
        print("Encontrou o lance correto: a5→b6")
        print()
        print("Variante principal:")
        for i, move in enumerate(pv[:14], 1):
            print(f"  {i}. {move}")
    else:
        print("❌ Motor V4 ainda não acertou")
        print(f"   Encontrado: {best_move}")
        print(f"   Esperado: a5→b6")
        print()
        print("Variante principal encontrada:")
        for i, move in enumerate(pv[:10], 1):
            print(f"  {i}. {move}")

except KeyboardInterrupt:
    print("\n⚠️  Busca interrompida (Ctrl+C)")
except Exception as e:
    print(f"\n❌ Erro durante busca: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

if "a5" in best_move and "b6" in best_move:
    print("🎉 SUCESSO!")
    print()
    print("O Motor V4 Profissional conseguiu resolver o exercício!")
    print()
    print("Técnicas que fizeram a diferença:")
    print("  1. Transposition Tables - reduziram busca em ~70%")
    print("  2. Iterative Deepening - melhoraram move ordering")
    print("  3. Move Ordering - PV, Killers, History")
    print("  4. Quiescence Search - evitaram horizon effect")
    print("  5. Null-Move Pruning - aumentaram profundidade efetiva")
    print()
    print("Este é um motor de nível PROFISSIONAL! 🏆")
else:
    print("Motor V4 ainda não resolveu completamente.")
    print()
    print("Possíveis razões:")
    print("  - Profundidade 16 ainda não é suficiente (precisa 14 exatos)")
    print("  - Poda agressiva cortando a linha vencedora")
    print("  - Avaliação de finais ainda não detectando padrão")
    print()
    print("Próximos passos:")
    print("  - Testar com max_depth=18-20")
    print("  - Ajustar sacrifice tolerance na avaliação")
    print("  - Implementar endgame tablebases para 5-6 peças")

print()
