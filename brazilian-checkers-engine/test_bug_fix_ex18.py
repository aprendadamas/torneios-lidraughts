"""
Test do bug fix - Promoção durante multi-captura
Exercício #18 - Lance 5

ANTES DO FIX: Motor parava em f8 com 3 capturas
DEPOIS DO FIX: Motor deve continuar até h6 com 4 capturas
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("TESTE DO BUG FIX - EXERCÍCIO #18 LANCE 5")
print("=" * 70)
print()

# Posição após lance 4 (antes do lance 5)
# Brancas: h2, h4 (peões)
# Pretas: b8, d8, e5, e7, g7, g3 (peões)

white_men = {28, 20}  # h2, h4
black_men = {1, 2, 15, 7, 8, 24}  # b8, d8, e5, e7, g7, g3

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO ANTES DO LANCE 5")

print()
print(f"Material: Brancas {len(white_men)} peões vs Pretas {len(black_men)} peões")
print()

print("=" * 70)
print("TESTE: Buscar capturas disponíveis")
print("=" * 70)
print()

captures = game.find_all_captures()

print(f"Total de capturas encontradas: {len(captures)}")
print()

# Procurar a captura que começa em h2
h2_captures = [c for c in captures if c.from_field == 28]

if h2_captures:
    print(f"Capturas de h2 (campo 28): {len(h2_captures)}")
    print()

    max_capture = max(h2_captures, key=lambda c: len(c.captured_fields))

    print("Melhor captura (mais peças):")
    notation = f"h2 ({28})"
    squares_visited = ["h2"]

    # Para construir a notação, precisamos das casas visitadas
    print(f"  De: {Pos64(max_capture.from_field).to_algebraic()} (campo {max_capture.from_field})")
    print(f"  Para: {Pos64(max_capture.to_field).to_algebraic()} (campo {max_capture.to_field})")
    print(f"  Captura {len(max_capture.captured_fields)} peças:")

    for cf in max_capture.captured_fields:
        print(f"    - {Pos64(cf).to_algebraic()} (campo {cf})")

    if max_capture.promotes:
        print(f"  Promove: ✅ SIM")
    else:
        print(f"  Promove: ❌ NÃO")

    print()
    print("=" * 70)
    print("RESULTADO DO TESTE")
    print("=" * 70)
    print()

    expected_captures = {24, 15, 7, 8}  # g3, e5, e7, g7
    expected_to = 12  # h6
    expected_promotes = False  # h6 não é linha de coroação

    actual_captures = set(max_capture.captured_fields)

    print(f"Esperado:")
    print(f"  - Capturar 4 peças: g3 (24), e5 (15), e7 (7), g7 (8)")
    print(f"  - Parar em h6 (campo 12)")
    print(f"  - NÃO promover (h6 = linha 6)")
    print()

    print(f"Obtido:")
    print(f"  - Capturar {len(actual_captures)} peças: {actual_captures}")
    print(f"  - Parar em campo {max_capture.to_field}")
    print(f"  - Promove: {max_capture.promotes}")
    print()

    # Verificação
    success = True

    if len(actual_captures) != 4:
        print(f"❌ ERRO: Esperava 4 capturas, obteve {len(actual_captures)}")
        success = False
    elif actual_captures != expected_captures:
        print(f"❌ ERRO: Peças capturadas incorretas")
        print(f"   Esperado: {expected_captures}")
        print(f"   Obtido: {actual_captures}")
        success = False

    if max_capture.to_field != expected_to:
        print(f"❌ ERRO: Campo final incorreto (esperado {expected_to}, obtido {max_capture.to_field})")
        success = False

    if max_capture.promotes != expected_promotes:
        print(f"❌ ERRO: Promoção incorreta (esperado {expected_promotes}, obtido {max_capture.promotes})")
        success = False

    if success:
        print("✅ BUG FIX FUNCIONOU!")
        print()
        print("O motor agora encontra corretamente:")
        print("  - Captura QUÁDRUPLA (4 peças)")
        print("  - Passa por f8 (linha 8) sem promover")
        print("  - Para em h6 (linha 6) como PEÃO")
        print()
        print("Regra FMJD aplicada corretamente:")
        print("  'Se alcança linha de coroação mas pode continuar")
        print("   capturando no mesmo curso, continua SEM promover'")
    else:
        print()
        print("⚠️  BUG AINDA PRESENTE - Fix não funcionou completamente")

else:
    print("❌ ERRO: Nenhuma captura de h2 encontrada!")
    print()
    print("Todas as capturas disponíveis:")
    for cap in captures:
        from_pos = Pos64(cap.from_field).to_algebraic()
        to_pos = Pos64(cap.to_field).to_algebraic()
        print(f"  {from_pos} ({cap.from_field}) → {to_pos} ({cap.to_field}): {len(cap.captured_fields)} peças")

print()
print("=" * 70)
