"""
Resolver Exercício Tático #13
[FEN "W:Wc1,e3,h4:Ba3,h6,e7."]
"""

from src.brazilian_engine import BrazilianGame
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #13 - 1800 Combinações")
print("=" * 70)
print()

# Converter posição FEN para campos
white_alg = ["c1", "e3", "h4"]
black_alg = ["a3", "h6", "e7"]

white_fields = {Pos64.from_algebraic(alg).field for alg in white_alg}
black_fields = {Pos64.from_algebraic(alg).field for alg in black_alg}

print("Posição inicial:")
print(f"  Brancas: {white_alg} → campos {sorted(white_fields)}")
print(f"  Pretas: {black_alg} → campos {sorted(black_fields)}")
print()

# Criar jogo
game = BrazilianGame(white_fields, black_fields, "white")
game.print_board("POSIÇÃO INICIAL:")

# Analisar primeiro lance sugerido: c1 → b2
print("=" * 70)
print("ANÁLISE DA SOLUÇÃO SUGERIDA")
print("=" * 70)
print()

print("Solução sugerida:")
print("1. c1-b2 a3xc1")
print("2. e3-f4 c1xg5")
print("3. h4xf6xd8")
print()

# Verificar capturas disponíveis para brancas
captures = game.find_all_captures()
print(f"Capturas disponíveis para brancas: {len(captures)}")

if captures:
    for i, cap in enumerate(captures, 1):
        from_alg = Pos64(cap.from_field).to_algebraic()
        to_alg = Pos64(cap.to_field).to_algebraic()
        captured = [Pos64(f).to_algebraic() for f in cap.captured_fields]
        print(f"  {i}. {from_alg} captura {captured} → {to_alg}")
else:
    print("  Nenhuma captura obrigatória")
print()

# Verificar movimentos simples
simple_moves = game.find_simple_moves()
print(f"Movimentos simples disponíveis: {len(simple_moves)}")
for from_f, to_f in simple_moves:
    from_alg = Pos64(from_f).to_algebraic()
    to_alg = Pos64(to_f).to_algebraic()
    print(f"  {from_alg} → {to_alg}")
print()

# Executar a sequência sugerida passo a passo
print("=" * 70)
print("VERIFICAÇÃO PASSO A PASSO")
print("=" * 70)
print()

# Lance 1: c1 → b2
print("Lance 1: Brancas jogam c1 → b2")
c1_field = Pos64.from_algebraic("c1").field
b2_field = Pos64.from_algebraic("b2").field
game.make_move(c1_field, b2_field)
game.print_board("Após c1 → b2:")

# Verificar se pretas têm captura obrigatória
captures = game.find_all_captures()
if captures:
    print(f"Pretas têm {len(captures)} captura(s) obrigatória(s):")
    for cap in captures:
        from_alg = Pos64(cap.from_field).to_algebraic()
        to_alg = Pos64(cap.to_field).to_algebraic()
        captured = [Pos64(f).to_algebraic() for f in cap.captured_fields]
        print(f"  {from_alg} captura {captured} → {to_alg}")

    # Verificar se a3 x b2 → c1 está nas opções
    a3_b2_c1 = None
    for cap in captures:
        if Pos64(cap.from_field).to_algebraic() == "a3" and Pos64(cap.to_field).to_algebraic() == "c1":
            a3_b2_c1 = cap
            break

    if a3_b2_c1:
        print()
        print("Lance 1 (resposta): Pretas jogam a3 x b2 → c1")
        game.make_move(a3_b2_c1.from_field, a3_b2_c1.to_field, a3_b2_c1.captured_fields)
        game.print_board("Após a3 x b2 → c1:")
    else:
        print()
        print("❌ ERRO: a3 x b2 → c1 não está disponível!")
else:
    print("❌ ERRO: Pretas não têm capturas obrigatórias!")

# Lance 2: e3 → f4
print()
print("Lance 2: Brancas jogam e3 → f4")
e3_field = Pos64.from_algebraic("e3").field
f4_field = Pos64.from_algebraic("f4").field

# Verificar se e3 ainda existe
if e3_field in game.white:
    game.make_move(e3_field, f4_field)
    game.print_board("Após e3 → f4:")

    # Verificar capturas das pretas
    captures = game.find_all_captures()
    if captures:
        print(f"Pretas têm {len(captures)} captura(s):")
        for cap in captures:
            from_alg = Pos64(cap.from_field).to_algebraic()
            to_alg = Pos64(cap.to_field).to_algebraic()
            captured = [Pos64(f).to_algebraic() for f in cap.captured_fields]
            print(f"  {from_alg} captura {captured} → {to_alg}")

        # A resposta sugerida é c1 x e3 → g5 (mas agora a peça está em f4, não e3!)
        # Então deve ser c1 x e5 x g5 ou similar
        print()
        print("Lance 2 (resposta): Pretas capturam...")

        # Escolher a captura que leva a g5
        best = None
        for cap in captures:
            if Pos64(cap.to_field).to_algebraic() == "g5":
                best = cap
                break

        if best:
            from_alg = Pos64(best.from_field).to_algebraic()
            to_alg = Pos64(best.to_field).to_algebraic()
            captured = [Pos64(f).to_algebraic() for f in best.captured_fields]
            print(f"  {from_alg} captura {captured} → {to_alg}")
            game.make_move(best.from_field, best.to_field, best.captured_fields)
            game.print_board(f"Após {from_alg} captura:")
        else:
            print("❌ Captura para g5 não encontrada")
            # Executar a primeira captura disponível
            if captures:
                cap = captures[0]
                game.make_move(cap.from_field, cap.to_field, cap.captured_fields)
                game.print_board()
else:
    print("❌ ERRO: e3 não existe mais no tabuleiro!")

# Lance 3: h4 x f6 x d8
print()
print("Lance 3: Brancas jogam h4 x f6 x d8")

captures = game.find_all_captures()
if captures:
    print(f"Capturas disponíveis para brancas: {len(captures)}")
    for cap in captures:
        from_alg = Pos64(cap.from_field).to_algebraic()
        to_alg = Pos64(cap.to_field).to_algebraic()
        captured = [Pos64(f).to_algebraic() for f in cap.captured_fields]
        print(f"  {from_alg} captura {captured} → {to_alg}")

    # Procurar a captura h4 → d8
    h4_d8 = None
    for cap in captures:
        if Pos64(cap.from_field).to_algebraic() == "h4" and Pos64(cap.to_field).to_algebraic() == "d8":
            h4_d8 = cap
            break

    if h4_d8:
        from_alg = Pos64(h4_d8.from_field).to_algebraic()
        to_alg = Pos64(h4_d8.to_field).to_algebraic()
        captured = [Pos64(f).to_algebraic() for f in h4_d8.captured_fields]
        print()
        print(f"Executando: {from_alg} captura {captured} → {to_alg}")
        game.make_move(h4_d8.from_field, h4_d8.to_field, h4_d8.captured_fields)
        game.print_board("POSIÇÃO FINAL:")

        if len(game.black) == 0:
            print("✅ BRANCAS VENCEM - Todas as peças pretas foram capturadas!")
        else:
            print(f"Pretas restantes: {len(game.black)} peça(s)")
    else:
        print("❌ Captura h4 x d8 não encontrada!")

print()
print("=" * 70)
print("SOLUÇÃO VERIFICADA")
print("=" * 70)
print()

print("Sequência completa:")
print("1. c1 → b2     a3 x b2 → c1")
print("2. e3 → f4     c1 x ... → g5")
print("3. h4 x f6 x e7 → d8")
print()

if game.game_over and game.winner == "white":
    print("✅ RESULTADO: BRANCAS VENCEM!")
elif len(game.black) == 0:
    print("✅ RESULTADO: BRANCAS VENCEM!")
else:
    print(f"Posição final: Brancas {len(game.white)} x {len(game.black)} Pretas")
