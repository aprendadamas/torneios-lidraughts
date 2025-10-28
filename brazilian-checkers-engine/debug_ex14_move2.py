"""
Debug do lance 2 do Exercício #14
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("DEBUG - Exercício #14 - Lance 2")
print("=" * 70)
print()

# Posição inicial
white_men = {30, 27, 23, 18, 19, 20}  # c1, f2, e3, d4, f4, h4
black_men = {21, 17, 11, 12, 6, 7}    # a3, b4, f6, h6, c7, e7

game = BrazilianGameComplete(white_men, black_men)
game.print_board("POSIÇÃO INICIAL")

print()
print("Lance 1: f4 → g5")
print()

# f4 está no campo 19
# g5 está no campo 14
print(f"f4 = campo {Pos64.from_algebraic('f4').field}")
print(f"g5 = campo {Pos64.from_algebraic('g5').field}")
print()

game.make_move(19, 14, [], False)  # f4 (19) → g5 (14)
game.print_board("Após f4 → g5")

print()
print("Verificando TODAS as capturas possíveis para as pretas:")
print()

caps = game.find_all_captures()
print(f"Total de capturas: {len(caps)}")
print()

for i, cap in enumerate(caps, 1):
    from_alg = Pos64(cap.from_field).to_algebraic()
    to_alg = Pos64(cap.to_field).to_algebraic()

    notation = from_alg
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {to_alg}"
    if cap.promotes:
        notation += " ♛"

    print(f"{i}. {notation}")
    print(f"   De: campo {cap.from_field} ({from_alg})")
    print(f"   Para: campo {cap.to_field} ({to_alg})")
    print(f"   Captura: {[Pos64(cf).to_algebraic() for cf in cap.captured_fields]}")
    print(f"   Promove: {cap.promotes}")
    print()

if len(caps) > 0:
    # Verificar qual delas é a captura dupla h6 x g5 x e3
    print("Procurando: h6 x g5 x e3 → d2")
    print()

    h6_field = Pos64.from_algebraic('h6').field
    print(f"h6 = campo {h6_field}")

    for cap in caps:
        if cap.from_field == h6_field:
            print(f"Encontrei captura de h6!")
            notation = Pos64(cap.from_field).to_algebraic()
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {Pos64(cap.to_field).to_algebraic()}"
            print(f"  {notation}")

            if len(cap.captured_fields) == 2:
                print(f"  É captura dupla!")
                captured_alg = [Pos64(cf).to_algebraic() for cf in cap.captured_fields]
                print(f"  Captura: {captured_alg}")

                if 'g5' in captured_alg and 'e3' in captured_alg:
                    print(f"  ✅ Esta é a captura correta!")
                    print()
                    print("Executando esta captura:")
                    game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)
                    game.print_board("Após h6 x g5 x e3 → d2")

                    w_total = len(game.white_men) + len(game.white_kings)
                    b_total = len(game.black_men) + len(game.black_kings)
                    print()
                    print(f"Material: Brancas {w_total} vs Pretas {b_total}")
                    print()

                    # Verificar próximas capturas
                    next_caps = game.find_all_captures()
                    if next_caps:
                        print("Capturas disponíveis para brancas:")
                        for ncap in next_caps:
                            notation = Pos64(ncap.from_field).to_algebraic()
                            for cf in ncap.captured_fields:
                                notation += f" x {Pos64(cf).to_algebraic()}"
                            notation += f" → {Pos64(ncap.to_field).to_algebraic()}"
                            print(f"  {notation}")
