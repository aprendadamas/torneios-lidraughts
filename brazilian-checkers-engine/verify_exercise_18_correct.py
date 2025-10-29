"""
Exercício #18 - Verificação da solução correta
Primeiro lance: a5 → b6 (fornecido pelo usuário)
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #18 - VERIFICAÇÃO DA SOLUÇÃO CORRETA")
print("=" * 70)
print()

# Posição inicial - TODOS PEÕES
white_men = set()
for piece in ["d2", "f2", "h2", "c3", "b4", "h4", "a5"]:
    white_men.add(Pos64.from_algebraic(piece).field)

black_men = set()
for piece in ["f4", "e5", "c7", "e7", "g7", "b8", "d8"]:
    black_men.add(Pos64.from_algebraic(piece).field)

game = BrazilianGameComplete(white_men, black_men, set(), set())
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Material: Brancas {len(white_men)} peões vs Pretas {len(black_men)} peões")
print()

print("Solução fornecida:")
print("1. a5 → b6")
print()
print("=" * 70)
print()

# Lance 1: a5 → b6
print("Lance 1: BRANCAS jogam a5 → b6")
print()

# Campos: a5 = 13, b6 = 9
game.make_move(13, 9, [], False)  # a5 (13) → b6 (9)

game.print_board("Após a5 → b6")

print()
print(f"Material: B={len(game.white_men) + len(game.white_kings)} P={len(game.black_men) + len(game.black_kings)}")
print()

# Verificar capturas disponíveis para pretas
print("Capturas obrigatórias para pretas:")
caps = game.find_all_captures()

if caps:
    print(f"Total: {len(caps)} captura(s)")
    for cap in caps:
        notation = Pos64(cap.from_field).to_algebraic()
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {Pos64(cap.to_field).to_algebraic()}"
        if cap.promotes:
            notation += " ♛"
        print(f"  {notation} (captura {len(cap.captured_fields)} peça(s))")
else:
    print("  Nenhuma captura disponível")
    moves = game.find_simple_moves()
    print(f"\nMovimentos simples: {len(moves)}")
    for move in moves[:10]:
        from_pos = Pos64(move.from_field).to_algebraic()
        to_pos = Pos64(move.to_field).to_algebraic()
        print(f"  {from_pos} → {to_pos}")

print()
print("=" * 70)
print("ANÁLISE")
print("=" * 70)
print()

print("Lance a5 → b6:")
print("- Peão branco avança para a6ª fileira")
print("- Ameaça promover em a7/b8")
print("- Pode forçar resposta das pretas")
print()

if caps:
    print(f"⚠️  Pretas têm {len(caps)} captura(s) obrigatória(s)")
    print("Próximo lance será uma captura preta")
else:
    print("✓ Sem capturas obrigatórias para pretas")
    print("Pretas podem escolher lance livre")

print()
print("Você poderia fornecer a sequência completa?")
print("Por exemplo: 1. a5-b6 ... 2. ... 3. ... etc")
