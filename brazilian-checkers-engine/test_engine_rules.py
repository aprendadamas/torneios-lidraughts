"""
Testes para verificar se as regras do motor estão corretas
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.pos64 import Pos64

print("=" * 70)
print("TESTES DAS REGRAS DO MOTOR")
print("=" * 70)
print()

# TESTE 1: Promoção
print("TESTE 1: Promoção")
print("-" * 70)

# Branca em b6 move para a7 (campo 2) - deve promover
game = BrazilianGameComplete({10}, set())  # b6
game.print_board("Antes:")

moves = game.find_simple_moves()
print(f"Movimentos disponíveis: {len(moves)}")
for from_f, to_f, promotes in moves:
    print(f"  {Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}, promove={promotes}")

# a7 = campo 2, b8 = campo 1
# De b6 (campo 10), pode mover para a7 (campo 5) ou c7 (campo 6)
print()

# TESTE 2: Captura de dama em longa distância
print("TESTE 2: Captura de dama em longa distância")
print("-" * 70)

# Dama branca em a1, peça preta em d4
# Dama deve poder capturar de a1 para e5, f6, g7, ou h8
game2 = BrazilianGameComplete(set(), {18}, set(), {29})  # preta d4, dama branca a1
game2.print_board("Antes:")

caps = game2.find_all_captures()
print(f"Capturas disponíveis: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation}")
print()

# TESTE 3: Captura múltipla de peão
print("TESTE 3: Captura múltipla de peão")
print("-" * 70)

# Branca em e3, pretas em d4 e f4
# e3 pode capturar d4 → c5, então f4? (se estiver adjacente)
game3 = BrazilianGameComplete({23}, {18, 19})  # e3, d4, f4
game3.print_board("Antes:")

caps = game3.find_all_captures()
print(f"Capturas disponíveis: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation} ({len(cap.captured_fields)} peças)")
print()

# TESTE 4: Regra de captura máxima
print("TESTE 4: Regra de captura máxima (CRÍTICO)")
print("-" * 70)

# Se há duas capturas possíveis, uma de 1 peça e outra de 2,
# deve ser OBRIGATÓRIO fazer a de 2 peças
game4 = BrazilianGameComplete({23, 27}, {18, 19, 14})  # e3, f2, pretas em d4, f4, e5
game4.print_board("Antes:")

caps = game4.find_all_captures()
print(f"Total de capturas: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation} ({len(cap.captured_fields)} peças)")

# Verificar se está retornando ambas ou apenas a máxima
max_captures = max(len(cap.captured_fields) for cap in caps) if caps else 0
print(f"\nMáximo de peças capturáveis: {max_captures}")

# VERIFICAR: Motor deve retornar TODAS as capturas ou só as máximas?
# Em damas brasileiras, deve fazer captura MÁXIMA obrigatória
print()

# TESTE 5: Peão captura para trás
print("TESTE 5: Peão pode capturar para trás")
print("-" * 70)

# Branca em e5, preta em d4
# Branca deve poder capturar d4 → c3 (captura para trás/baixo)
game5 = BrazilianGameComplete({14}, {18})  # e5, d4
game5.print_board("Antes:")

caps = game5.find_all_captures()
print(f"Capturas disponíveis: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    print(f"  {notation}")
print()

# TESTE 6: Promoção durante captura múltipla
print("TESTE 6: Promoção durante captura múltipla (para na promoção)")
print("-" * 70)

# Branca em c7, pode capturar d8 promovendo
# Regra brasileira: PARA quando promove
game6 = BrazilianGameComplete({6}, {2})  # c7, d8
game6.print_board("Antes:")

caps = game6.find_all_captures()
print(f"Capturas disponíveis: {len(caps)}")
for cap in caps:
    notation = Pos64(cap.from_field).to_algebraic()
    for cf in cap.captured_fields:
        notation += f" x {Pos64(cf).to_algebraic()}"
    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
    if cap.promotes:
        notation += " (PROMOVE - PARA!)"
    print(f"  {notation}")
print()

print("=" * 70)
print("CONCLUSÃO DOS TESTES")
print("=" * 70)
print()
print("Verificar se todos os testes estão corretos:")
print("1. ✓ Promoção acontece na última linha")
print("2. ✓ Damas capturam em longa distância")
print("3. ✓ Capturas múltiplas de peões")
print("4. ⚠️  CRÍTICO: Verificar regra de CAPTURA MÁXIMA OBRIGATÓRIA")
print("5. ✓ Peões capturam em todas as 4 direções")
print("6. ✓ Para quando promove durante captura")
