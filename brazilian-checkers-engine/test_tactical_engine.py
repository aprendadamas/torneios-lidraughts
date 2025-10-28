"""
Testar se o Motor Tático melhorado encontra soluções automaticamente
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine import TacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("TESTE DO MOTOR TÁTICO MELHORADO")
print("=" * 70)
print()

# TESTE 1: Exercício #1 (já resolvido manualmente)
print("TESTE 1: Exercício #1")
print("-" * 70)

white = {29, 25, 22}  # a1, b2, c3
black = {13, 15, 8}   # a5, e5, g7

game1 = BrazilianGameComplete(white, black)
game1.print_board("Posição:")

print("Solução conhecida:")
print("  1. c3 → b4 (sacrifício)")
print("  2. a5 x b4 → c3")
print("  3. b2 x c3 x e5 x g7 → h8")
print()

engine = TacticalSearchEngine()

print("Motor tático buscando (profundidade 6)...")
best_move, score, sequence = engine.search_best_move(game1, max_depth=6)

print(f"Nós pesquisados: {engine.nodes_searched}")
print(f"Melhor movimento encontrado: {best_move}")
print(f"Avaliação: {score}")
print()

if sequence:
    print("Sequência principal encontrada:")
    for i, move in enumerate(sequence[:6], 1):
        print(f"  {i}. {move}")
    print()

# Verificar se encontrou o sacrifício c3 → b4
if best_move and "c3" in best_move and "b4" in best_move:
    print("✅ Motor encontrou o SACRIFÍCIO TÁTICO correto!")
else:
    print(f"❌ Motor sugeriu: {best_move}")
    print("   Esperado: c3 → b4 (sacrifício)")

print()

# TESTE 2: Exercício #13 (também resolvido)
print("TESTE 2: Exercício #13")
print("-" * 70)

white2 = {30, 23, 20}  # c1, e3, h4
black2 = {21, 12, 7}   # a3, h6, e7

game2 = BrazilianGameComplete(white2, black2)
game2.print_board("Posição:")

print("Solução conhecida:")
print("  1. c1 → b2 (sacrifício)")
print("  2. a3 x b2 → c1 (promove dama)")
print("  3. e3 → f4")
print("  4. DAMA captura")
print()

engine2 = TacticalSearchEngine()

print("Motor tático buscando (profundidade 6)...")
best_move2, score2, sequence2 = engine2.search_best_move(game2, max_depth=6)

print(f"Nós pesquisados: {engine2.nodes_searched}")
print(f"Melhor movimento encontrado: {best_move2}")
print(f"Avaliação: {score2}")
print()

if sequence2:
    print("Sequência principal encontrada:")
    for i, move in enumerate(sequence2[:6], 1):
        print(f"  {i}. {move}")
    print()

# Verificar se encontrou o sacrifício c1 → b2
if best_move2 and "c1" in best_move2 and "b2" in best_move2:
    print("✅ Motor encontrou o SACRIFÍCIO TÁTICO correto!")
else:
    print(f"❌ Motor sugeriu: {best_move2}")
    print("   Esperado: c1 → b2 (sacrifício)")

print()

# TESTE 3: Aplicar no Exercício #14 (não resolvido ainda)
print("TESTE 3: Exercício #14 (DESAFIO)")
print("-" * 70)

white3 = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black3 = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game3 = BrazilianGameComplete(white3, black3)
game3.print_board("Posição:")

print("Solução: DESCONHECIDA (deve ser 4 lances)")
print()

engine3 = TacticalSearchEngine()

print("Motor tático buscando (profundidade 8)...")
best_move3, score3, sequence3 = engine3.search_best_move(game3, max_depth=8)

print(f"Nós pesquisados: {engine3.nodes_searched}")
print(f"Melhor movimento encontrado: {best_move3}")
print(f"Avaliação: {score3}")
print()

if sequence3:
    print("Sequência principal encontrada:")
    for i, move in enumerate(sequence3[:10], 1):
        print(f"  {i}. {move}")
    print()

    # Verificar se leva à vitória
    if score3 >= 9000:
        print("✅ Motor encontrou sequência VENCEDORA!")
        print()
        print("=" * 70)
        print("SOLUÇÃO DO EXERCÍCIO #14:")
        print("=" * 70)
        for i, move in enumerate(sequence3, 1):
            print(f"{i}. {move}")
    else:
        print("⚠️  Avaliação não indica vitória clara")
else:
    print("❌ Motor não encontrou sequência")

print()
print("=" * 70)
print("RESUMO DOS TESTES")
print("=" * 70)
print()
print("O motor tático consegue:")
print("1. Avaliar posições considerando capturas múltiplas")
print("2. Reconhecer sacrifícios táticos")
print("3. Buscar mais profundamente em linhas táticas")
print("4. Priorizar capturas que levam à vitória")
