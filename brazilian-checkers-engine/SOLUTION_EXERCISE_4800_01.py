"""
SOLUÇÃO EXERCÍCIO #1 - "4800 Combinações - Avançado"
Análise Completa do Padrão de Bloqueio

Motor V2 NÃO encontrou a solução correta.
Este exercício expõe limitações importantes do motor.
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #1 (4800 AVANÇADO) - SOLUÇÃO CORRETA")
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
print("=" * 70)
print("SOLUÇÃO (14 MEIO-LANCES)")
print("=" * 70)
print()

print("Lance 1: a5-b6 c5xa7")
print("  Brancas sacrificam a5")
print("  Pretas capturam MAS vão para a7 (não b6!)")
print()

game.make_move(13, 9, [], False)  # a5 → b6
game.make_move(14, 5, [9], False)  # c5 x b6 → a7
game.print_board("Após lance 1")
print()

print("Lance 2: c3-b4 f8xa3")
print("  Brancas sacrificam c3")
print("  Dama preta f8 captura e vai para a3")
print()

game.make_move(22, 17, [], False)  # c3 → b4
game.make_move(3, 21, [17], False)  # f8 x b4 → a3
game.print_board("Após lance 2")
print()

print("Lance 3: f6-g7 h6xf8")
print("  Brancas sacrificam f6")
print("  Preta captura e PROMOVE em f8!")
print()

game.make_move(11, 8, [], False)  # f6 → g7
game.make_move(12, 3, [8], True)  # h6 x g7 → f8 ♛
game.print_board("Após lance 3")
print()

print("Lance 4: e5-d6 a3xe7")
print("  Brancas sacrificam e5")
print("  Dama preta captura e vai para e7")
print()

game.make_move(15, 10, [], False)  # e5 → d6
game.make_move(21, 7, [10], False)  # a3 x d6 → e7
game.print_board("Após lance 4")
print()

print("Lance 5: a1-g7 f8xh6")
print("  Dama branca a1 vai para g7")
print("  Dama preta f8 captura h4 (?) → h6")
print()

game.make_move(29, 8, [], False)  # a1 → g7
# Verificar se h4 ainda está no jogo
if 20 in game.white_men:
    game.make_move(3, 12, [20], False)  # f8 x h4 → h6
    game.print_board("Após lance 5")
else:
    print("ERRO: h4 já não está mais no tabuleiro!")
print()

print("Lance 6: g3-f4 c1xg5")
print("  Brancas sacrificam g3")
print("  Dama preta c1 captura e vai para g5")
print()

if 24 in game.white_men:
    game.make_move(24, 19, [], False)  # g3 → f4
    game.make_move(30, 16, [19], False)  # c1 x f4 → g5
    game.print_board("Após lance 6")
print()

print("Lance 7: h4xf6xd8 (captura dupla + promoção!)")
print("  Se h4 ainda existe, captura f4/g5 e depois e7")
print("  Promove em d8!")
print()

# Verificar posição final esperada
print("=" * 70)
print("POSIÇÃO FINAL ESPERADA")
print("=" * 70)
print()
print("Brancas: 1 dama em d8 ou g7")
print("Pretas: 2 peões BLOQUEADOS (a7 e possivelmente d8)")
print()
print("PADRÃO TÁTICO: BLOQUEIO")
print("  - Peões pretos não podem se mover sem serem capturados")
print("  - Dama branca vence facilmente")
print()

print("=" * 70)
print("POR QUE O MOTOR NÃO ENCONTROU?")
print("=" * 70)
print()
print("1. PROFUNDIDADE INSUFICIENTE")
print("   - Solução tem 14 meio-lances")
print("   - Motor analisou apenas depth 6-8")
print()
print("2. AVALIAÇÃO DE FINAIS")
print("   - Motor não reconhece '1♛ vs 2 peões bloqueados' = vitória")
print("   - Avalia por material: 1♛ (300) vs 2 peões (200) = +100")
print("   - Deveria avaliar como VITÓRIA FORÇADA (+9999)")
print()
print("3. SACRIFÍCIOS EXTREMOS")
print("   - Brancas sacrificam SEIS peões!")
print("   - Motor tem 'sacrifice_tolerance' mas não para tantos sacrifícios")
print()
print("4. FALTA AVALIAÇÃO DE BLOQUEIO")
print("   - Motor não detecta que peões estão bloqueados")
print("   - Peão bloqueado vale muito menos que peão móvel")
print()

print("=" * 70)
print("MELHORIAS NECESSÁRIAS")
print("=" * 70)
print()
print("1. Aumentar profundidade para exercícios avançados (depth 14+)")
print("2. Implementar avaliação de finais (dama vs peões)")
print("3. Detectar bloqueio de peões (mobilidade = 0)")
print("4. Aumentar sacrifice_tolerance para táticas profundas")
print()
