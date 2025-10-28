"""
Verificar a solução do Exercício #16
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("VERIFICAÇÃO DA SOLUÇÃO - EXERCÍCIO #16")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 28, 24}  # c1, f2, h2, g3
black_men = {22, 15, 6}       # c3, e5, c7
black_kings = {2}              # d8

game = BrazilianGameComplete(white_men, black_men, set(), black_kings)
game.print_board("Lance #0 - POSIÇÃO INICIAL")

print()
print("Sequência sugerida pelo motor:")
print("  1. c1 → d2 (sacrifício)")
print("  2. c3 x d2 → e1 ♛ (promove dama)")
print("  3. g3 → h4")
print("  4. e1 x f2 → g3 (dama captura)")
print("  5. h2 x g3 x e5 x c7 → b8 ♛ (captura tripla!)")
print()
print("=" * 70)
print()

# Lance 1: c1 → d2
print("Lance 1: BRANCAS jogam c1 → d2 (SACRIFÍCIO)")
game.make_move(30, 31, [], False)  # c1 (30) → d2 (31)
game.print_board("Após c1 → d2")

# Verificar se é realmente um sacrifício
caps = game.find_all_captures()
if caps:
    print("✓ Pretas têm capturas obrigatórias!")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation}")

print()

# Lance 2: c3 x d2 → e1 (captura forçada com promoção)
print("Lance 2: PRETAS capturam c3 x d2 → e1 ♛ (PROMOVE DAMA)")
game.make_move(22, 32, [31], True)  # c3 (22) x d2 (31) → e1 (32), promotes
game.print_board("Após c3 x d2 → e1 ♛")

print(f"Pretas agora têm {len(game.black_kings)} damas!")
print()

# Lance 3: g3 → h4
print("Lance 3: BRANCAS jogam g3 → h4")
game.make_move(24, 20, [], False)  # g3 (24) → h4 (20)
game.print_board("Após g3 → h4")

# Verificar capturas disponíveis
caps = game.find_all_captures()
if caps:
    print("Pretas têm capturas obrigatórias!")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation}")

print()

# Lance 4: e1 x f2 → g3 (dama captura)
print("Lance 4: PRETAS capturam e1 x f2 → g3")
game.make_move(32, 24, [27], False)  # e1 (32) x f2 (27) → g3 (24)
game.print_board("Após e1 x f2 → g3")

# Verificar se há mais capturas para a dama
print(f"Dama preta parou em g3")
print()

# Lance 5: h2 x g3 x e5 x c7 → b8 ♛ (captura múltipla!)
print("Lance 5: BRANCAS capturam h2 x g3 x e5 x c7 → b8 ♛ (TRIPLA!)")

# Verificar todas as capturas disponíveis
caps = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation} (captura {len(cap.captured_fields)} peças)")

print()

# Executar a melhor captura
best_cap = max(caps, key=lambda c: len(c.captured_fields))
print(f"Executando melhor captura: {len(best_cap.captured_fields)} peças")
game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
game.print_board("Após captura múltipla")

print()
print("=" * 70)
print("ANÁLISE DA POSIÇÃO RESULTANTE")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material final (após 5 lances):")
print(f"  Brancas: {len(game.white_men)} peões + {len(game.white_kings)} damas = {w_total}")
print(f"  Pretas: {len(game.black_men)} peões + {len(game.black_kings)} damas = {b_total}")
print()

if w_total > b_total:
    print(f"✅ Brancas têm VANTAGEM MATERIAL: +{w_total - b_total}")
elif b_total > w_total:
    print(f"⚠️  Pretas têm VANTAGEM MATERIAL: +{b_total - w_total}")
else:
    print("= Material equilibrado")

print()

# Verificar se a posição é vencedora
if b_total == 0:
    print("🏆 BRANCAS VENCERAM - Todas as peças pretas eliminadas!")
elif w_total == 0:
    print("❌ Pretas venceram")
else:
    print("Jogo continua...")
    print()
    print("Próximos lances possíveis para pretas:")
    caps = game.find_all_captures()
    if caps:
        print("  Capturas obrigatórias:")
        for cap in caps[:5]:
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            print(f"    {notation}")
    else:
        moves = game.find_simple_moves()
        print(f"  {len(moves)} movimentos simples disponíveis")
        for from_f, to_f, promotes in list(moves)[:5]:
            notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
            if promotes:
                notation += " ♛"
            print(f"    {notation}")
