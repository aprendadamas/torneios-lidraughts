"""
Exercício #18 - Verificação FINAL com notação correta
Notação: Lista TODAS as casas atravessadas, não apenas capturas

Lance 5: h2xf4xd6xf8xh6
- Captura peças em: g3, e5, e7 (e possivelmente outras)
- Atravessa casas: f4, d6, f8
- Para em: h6
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

# Executar lances 1-4 rapidamente
white_men = {26, 27, 28, 22, 17, 20, 13}
black_men = {19, 15, 6, 7, 8, 1, 2}
game = BrazilianGameComplete(white_men, black_men, set(), set())

# Lance 1
game.make_move(13, 9, [], False)  # a5 → b6
game.make_move(6, 13, [9], False)  # c7 x b6 → a5

# Lance 2
game.make_move(26, 23, [], False)  # d2 → e3
game.make_move(19, 26, [23], False)  # f4 x e3 → d2

# Lance 3
game.make_move(22, 31, [26], False)  # c3 x d2 → e1 (SEM promoção)
game.make_move(13, 22, [17], False)  # a5 x b4 → c3

# Lance 4
game.make_move(31, 26, [], False)  # e1 → d2
game.make_move(22, 24, [26, 27], False)  # c3 x d2 x f2 → g3 (SEM promoção)

print("=" * 70)
print("EXERCÍCIO #18 - LANCE 5")
print("=" * 70)
print()

game.print_board("Posição antes do lance 5")

print()
print("Peças no tabuleiro:")
print("  Brancas:")
for f in sorted(game.white_men):
    print(f"    Peão: {Pos64(f).to_algebraic()} (campo {f})")
for f in sorted(game.white_kings):
    print(f"    DAMA: {Pos64(f).to_algebraic()} (campo {f})")

print("  Pretas:")
for f in sorted(game.black_men):
    print(f"    Peão: {Pos64(f).to_algebraic()} (campo {f})")
for f in sorted(game.black_kings):
    print(f"    DAMA: {Pos64(f).to_algebraic()} (campo {f})")

print()
print("=" * 70)
print("Lance 5: h2xf4xd6xf8xh6")
print("=" * 70)
print()

print("h2 = campo 28")
print("h6 = campo 12")
print()

print("Peças pretas que podem ser capturadas:")
print(f"  g3 (campo 24) - adjacente a h2")
print(f"  e5 (campo 15)")
print(f"  e7 (campo 7)")
print(f"  g7 (campo 8)")
print()

print("Capturas disponíveis para brancas:")
caps = game.find_all_captures()
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    captured_list = []
    for cf in cap.captured_fields:
        captured_list.append(Pos64(cf).to_algebraic())
    notation += " x " + " x ".join(captured_list)
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " ♛"
    print(f"  {notation}")
    print(f"    Origem: campo {cap.from_field} ({Pos64(cap.from_field).to_algebraic()})")
    print(f"    Destino: campo {cap.to_field} ({Pos64(cap.to_field).to_algebraic()})")
    print(f"    Capturas: campos {cap.captured_fields}")
    if cap.promotes:
        print(f"    PROMOVE!")
    print()

# Procurar captura que parte de h2 (28) e vai para h6 (12)
target_cap = None
for cap in caps:
    if cap.from_field == 28 and cap.to_field == 12:
        target_cap = cap
        break

if target_cap:
    print("=" * 70)
    print("EXECUTANDO CAPTURA h2 → h6:")
    print("=" * 70)
    notation = Pos64(target_cap.from_field).to_algebraic()
    for cf in target_cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(target_cap.to_field).to_algebraic()}"
    if target_cap.promotes:
        notation += " ♛"

    print(f"\n{notation}")
    print(f"Captura {len(target_cap.captured_fields)} peças!")
    if target_cap.promotes:
        print("E PROMOVE!")

    game.make_move(target_cap.from_field, target_cap.to_field, target_cap.captured_fields, target_cap.promotes)

    game.print_board("POSIÇÃO FINAL")

    print()
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    w_total = len(game.white_men) + len(game.white_kings)
    b_total = len(game.black_men) + len(game.black_kings)

    print(f"\nMaterial: Brancas {w_total} vs Pretas {b_total}")
    print(f"  Brancas: {len(game.white_men)} peões + {len(game.white_kings)} damas")
    print(f"  Pretas: {len(game.black_men)} peões + {len(game.black_kings)} damas")
    print()

    if w_total > b_total:
        print(f"✅ BRANCAS VENCEM! (+{w_total - b_total})")
    elif w_total == b_total:
        print("⚖️  EMPATE")
    else:
        print(f"⚠️  PRETAS VENCEM (+{b_total - w_total})")
else:
    print("❌ ERRO: Não encontrei captura de h2 para h6!")
    print()
    print("Capturas disponíveis de h2:")
    for cap in caps:
        if cap.from_field == 28:
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            print(f"  {notation}")
