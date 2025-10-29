"""
Debug: Por que o motor não encontra h2 x g3 x e5 x e7 x g7 → h6?
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

# Recriar a posição antes do lance 5
white_men = {28, 20}  # h2, h4
black_men = {1, 2, 8, 15, 7, 24}  # b8, d8, g7, e5, e7, g3

game = BrazilianGameComplete(white_men, set(), set(), set())
game.black_men = black_men
game.turn = "white"

game.print_board("Posição antes do lance 5")

print()
print("Peças brancas:", [Pos64(f).to_algebraic() for f in sorted(game.white_men)])
print("Peças pretas:", [Pos64(f).to_algebraic() for f in sorted(game.black_men)])
print()

caps = game.find_all_captures()
print(f"Capturas encontradas: {len(caps)}")
print()

for i, cap in enumerate(caps, 1):
    from_pos = Pos64(cap.from_field).to_algebraic()
    to_pos = Pos64(cap.to_field).to_algebraic()
    captured = [Pos64(f).to_algebraic() for f in cap.captured_fields]

    print(f"{i}. {from_pos} → {to_pos}")
    print(f"   Captura: {' x '.join(captured)}")
    print(f"   Total: {len(cap.captured_fields)} peças")
    print(f"   Promove: {cap.promotes}")
    print()

# Verificar manualmente se g7 pode ser capturado após f8
print("=" * 70)
print("ANÁLISE MANUAL:")
print("=" * 70)
print()

print("Após h2 captura g3, e5, e7 e chega em f8 (campo 3):")
print("- f8 está na linha 8")
print("- g7 (campo 8) está em linha 7")
print("- Diagonal de f8: e7 (já capturado), d6, c5, b4, a3 (para trás)")
print("- Diagonal de f8: g7 (campo 8), h6 (campo 12) (para frente/direita)")
print()

print("Para capturar g7:")
print("- Peça em f8 (campo 3)")
print("- Captura g7 (campo 8)")
print("- Pode parar em h6 (campo 12)?")
print()

# Verificar adjacência
print("Campos adjacentes a f8 (campo 3):")
print("  Diagonal: 7, 8 (e7=7 já capturado, g7=8 disponível)")
print()

print("Se g7 NÃO está nas capturas, pode ser porque:")
print("1. O motor não suporta capturas de peões com > 3 capturas")
print("2. Bug no find_all_captures para capturas longas")
print("3. Regra de captura máxima não está implementada corretamente")
