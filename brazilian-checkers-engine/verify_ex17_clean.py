"""
Verificação LIMPA do Exercício #17
Executar a sequência sugerida pelo motor e verificar posição após move 7
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #17 - VERIFICAÇÃO LIMPA")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 28, 21, 24}  # c1, f2, h2, a3, g3
black_men = {13, 15, 11, 6}       # a5, e5, f6, c7
black_kings = {2}                  # d8

game = BrazilianGameComplete(white_men, black_men, set(), black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print("Sequência sugerida pelo Motor V2:")
print("1. a3 → b4")
print("2. a5 x b4 → c3")
print("3. c1 → d2")
print("4. c3 x d2 → e1 ♛")
print("5. g3 → h4")
print("6. e1 x f2 → g3")
print("7. h2 x g3 x e5 x c7 → b8 ♛")
print()
print("=" * 70)
print()

# Lance 1: a3 → b4
print("Lance 1: a3 → b4 (SACRIFÍCIO)")
game.make_move(21, 17, [], False)  # a3 (21) → b4 (17)
game.print_board("Após Lance 1")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 2: a5 x b4 → c3
print("Lance 2: a5 x b4 → c3")
game.make_move(13, 22, [17], False)  # a5 (13) x b4 (17) → c3 (22)
game.print_board("Após Lance 2")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 3: c1 → d2
print("Lance 3: c1 → d2 (SEGUNDO SACRIFÍCIO)")
game.make_move(30, 26, [], False)  # c1 (30) → d2 (26)
game.print_board("Após Lance 3")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Lance 4: c3 x d2 → e1 ♛
print("Lance 4: c3 x d2 → e1 ♛ (PROMOVE DAMA)")
game.make_move(22, 31, [26], True)  # c3 (22) x d2 (26) → e1 (31), promove
game.print_board("Após Lance 4")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print(f"Pretas têm {len(game.black_kings)} damas")
print()

# Lance 5: g3 → h4
print("Lance 5: g3 → h4 (LANCE INTERMEDIÁRIO)")
game.make_move(24, 20, [], False)  # g3 (24) → h4 (20)
game.print_board("Após Lance 5")
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Verificar capturas disponíveis para as pretas
print("Capturas disponíveis para pretas:")
caps = game.find_all_captures()
for cap in caps[:10]:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")
print()

# Lance 6: Dama captura f2
print("Lance 6: e1 x f2 → ??? (Encontrar melhor captura)")

# Encontrar captura da dama em e1 (campo 31)
best_cap = None
for cap in caps:
    if cap.from_field == 31 and 27 in cap.captured_fields:  # e1 captura f2
        # Escolher a que leva a g3 se possível
        if Pos64(cap.to_field).to_algebraic() == "g3":
            best_cap = cap
            break

if not best_cap:
    # Se não encontrou g3, pegar qualquer captura que inclui f2
    for cap in caps:
        if cap.from_field == 31 and 27 in cap.captured_fields:
            best_cap = cap
            break

if best_cap:
    notation = Pos64(best_cap.from_field).to_algebraic()
    for cf in best_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(best_cap.to_field).to_algebraic()}"
    print(f"Executando: {notation}")
    game.make_move(best_cap.from_field, best_cap.to_field, best_cap.captured_fields, best_cap.promotes)
    game.print_board("Após Lance 6")
    print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
    print()
else:
    print("❌ ERRO: Não encontrou captura de f2!")
    print()

# Lance 7: Captura tripla
print("Lance 7: CAPTURA TRIPLA")
print("Buscando: h2 x g3 x e5 x c7 → b8 ♛")
print()

caps = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(caps)}")

# Procurar captura que parte de h2 (campo 28)
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"

    if cap.from_field == 28:  # h2
        print(f"  {notation} (captura {len(cap.captured_fields)} peça(s)) ← ORIGEM h2")
    else:
        print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")

print()

if not caps:
    print("❌ ERRO: Nenhuma captura disponível após lance 6!")
    print("Isso indica um problema na sequência.")
    exit(1)

# Encontrar a melhor (maior número de capturas)
best_triple = max(caps, key=lambda c: len(c.captured_fields))

notation = Pos64(best_triple.from_field).to_algebraic()
for cf in best_triple.captured_fields:
    notation += f" x {Pos64(cf).to_algebraic()}"
notation += f" → {Pos64(best_triple.to_field).to_algebraic()}"
if best_triple.promotes:
    notation += " ♛"

print(f"Executando melhor captura: {notation}")
print(f"Captura {len(best_triple.captured_fields)} peças!")

if best_triple.promotes:
    print("E PROMOVE DAMA!")

print()

game.make_move(best_triple.from_field, best_triple.to_field, best_triple.captured_fields, best_triple.promotes)
game.print_board("POSIÇÃO APÓS CAPTURA TRIPLA")

print()
print("=" * 70)
print("ANÁLISE DA POSIÇÃO FINAL (após lance 7)")
print("=" * 70)
print()

w_total = len(game.white_men) + len(game.white_kings)
b_total = len(game.black_men) + len(game.black_kings)

print(f"Material: Brancas {w_total} ({len(game.white_men)} peões + {len(game.white_kings)} damas)")
print(f"          Pretas {b_total} ({len(game.black_men)} peões + {len(game.black_kings)} damas)")
print()

if w_total > b_total:
    print(f"✅ Brancas têm vantagem: +{w_total - b_total}")
elif w_total == b_total:
    print("⚖️  Material EQUILIBRADO")
    print()
    print("ISSO EXPLICA por que Motor V2 deu score 0!")
    print("Após a sequência tática brilhante, a posição fica igual.")
else:
    print(f"⚠️  Pretas têm vantagem: +{b_total - w_total}")

print()
print("=" * 70)
print("CONCLUSÃO")
print("=" * 70)
print()

if w_total == b_total:
    print("O Motor V2 está CORRETO!")
    print()
    print("Ele encontrou a sequência tática mais espetacular")
    print("(duplo sacrifício + captura tripla),")
    print("mas reconheceu que após essa sequência")
    print("a posição fica EMPATADA.")
    print()
    print("Possibilidades:")
    print("1. Este exercício é um empate teórico")
    print("2. Há uma continuação diferente que vence")
    print("3. A vitória vem do endgame dama+peão vs dama+peão")
