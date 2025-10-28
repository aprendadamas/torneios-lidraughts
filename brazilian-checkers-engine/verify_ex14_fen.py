"""
Verificar se o FEN do Exercício #14 está correto
"""

from src.pos64 import Pos64
from src.brazilian_engine_complete import BrazilianGameComplete

print("=" * 80)
print("VERIFICAÇÃO DO FEN - EXERCÍCIO #14")
print("=" * 80)
print()

# FEN original: W:Wc1,e3,f2,d4,f4,h4:Ba3,b4,f6,h6,c7,e7

print("FEN: W:Wc1,e3,f2,d4,f4,h4:Ba3,b4,f6,h6,c7,e7")
print()

# Converter algebricas para campos
white_alg = ["c1", "e3", "f2", "d4", "f4", "h4"]
black_alg = ["a3", "b4", "f6", "h6", "c7", "e7"]

print("Peças BRANCAS:")
white_fields = set()
for alg in white_alg:
    pos = Pos64.from_algebraic(alg)
    if pos:
        white_fields.add(pos.field)
        print(f"  {alg} → campo {pos.field}")
    else:
        print(f"  {alg} → INVÁLIDO!")

print()
print("Peças PRETAS:")
black_fields = set()
for alg in black_alg:
    pos = Pos64.from_algebraic(alg)
    if pos:
        black_fields.add(pos.field)
        print(f"  {alg} → campo {pos.field}")
    else:
        print(f"  {alg} → INVÁLIDO!")

print()
print("=" * 80)
print("TABULEIRO RESULTANTE")
print("=" * 80)
print()

game = BrazilianGameComplete(white_fields, black_fields)
game.print_board()

print()
print("=" * 80)
print("VERIFICAR MOVIMENTOS POSSÍVEIS")
print("=" * 80)
print()

# Capturas
caps = game.find_all_captures()
print(f"Capturas obrigatórias: {len(caps)}")
if caps:
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        print(f"  {notation}")
else:
    print("  Nenhuma")

print()

# Movimentos simples
moves = game.find_simple_moves()
print(f"Movimentos simples: {len(moves)}")
for from_f, to_f, promotes in sorted(moves)[:10]:
    notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
    if promotes:
        notation += " ♛"
    print(f"  {notation}")

if len(moves) > 10:
    print(f"  ... e mais {len(moves) - 10}")

print()
print("=" * 80)
print("ANÁLISE DA POSIÇÃO")
print("=" * 80)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material: Brancas {w_total} x {b_total} Pretas (equilibrado)")
print()

# Verificar se há peças avançadas
white_advanced = [f for f in white_fields if f <= 8]
black_advanced = [f for f in black_fields if f >= 25]

print("Peças avançadas:")
print(f"  Brancas perto da promoção (campos 1-8): {[Pos64(f).to_algebraic() for f in white_advanced]}")
print(f"  Pretas perto da promoção (campos 25-32): {[Pos64(f).to_algebraic() for f in black_advanced]}")
print()

# Verificar se posição corresponde ao diagrama esperado
print("=" * 80)
print("DIAGRAMA ESPERADO (do exercício):")
print("=" * 80)
print()
print("Linha 7: c7, e7 (pretas)")
print("Linha 6: f6, h6 (pretas)")
print("Linha 4: b4 (preta), d4, f4, h4 (brancas)")
print("Linha 3: a3 (preta), e3 (branca)")
print("Linha 2: f2 (branca)")
print("Linha 1: c1 (branca)")
print()

# Verificar se bate com o que temos
print("Verificação:")
checks = [
    ("c7", 6 in black_fields),
    ("e7", 7 in black_fields),
    ("f6", 11 in black_fields),
    ("h6", 12 in black_fields),
    ("b4", 17 in black_fields),
    ("d4", 18 in white_fields),
    ("f4", 19 in white_fields),
    ("h4", 20 in white_fields),
    ("a3", 21 in black_fields),
    ("e3", 23 in white_fields),
    ("f2", 27 in white_fields),
    ("c1", 30 in white_fields),
]

all_correct = True
for alg, correct in checks:
    status = "✓" if correct else "✗"
    print(f"  {status} {alg}")
    if not correct:
        all_correct = False

print()
if all_correct:
    print("✅ Todas as peças estão nas posições corretas!")
else:
    print("❌ Há peças em posições incorretas!")
