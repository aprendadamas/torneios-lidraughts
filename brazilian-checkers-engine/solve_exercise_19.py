"""
Exercício #19 - "1800 Combinações"
FEN: W:Wd2,f2,h2,a3,g3,h4:Bf4,a5,e5,e7,g7,d8.

Análise com Motor V2 (com bug fix FMJD 3.7)
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #19 - Análise Inicial")
print("=" * 70)
print()

# FEN: W:Wd2,f2,h2,a3,g3,h4:Bf4,a5,e5,e7,g7,d8.
# W e B = COR apenas, todas são peões!

# Brancas (6 peões): d2, f2, h2, a3, g3, h4
# Pretas (6 peões): f4, a5, e5, e7, g7, d8

white_men = {
    Pos64.from_algebraic("d2").field,  # 26
    Pos64.from_algebraic("f2").field,  # 27
    Pos64.from_algebraic("h2").field,  # 28
    Pos64.from_algebraic("a3").field,  # 21
    Pos64.from_algebraic("g3").field,  # 24
    Pos64.from_algebraic("h4").field,  # 20
}

black_men = {
    Pos64.from_algebraic("f4").field,  # 19
    Pos64.from_algebraic("a5").field,  # 13
    Pos64.from_algebraic("e5").field,  # 15
    Pos64.from_algebraic("e7").field,  # 7
    Pos64.from_algebraic("g7").field,  # 8
    Pos64.from_algebraic("d8").field,  # 2
}

white_kings = set()
black_kings = set()

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Material: Brancas {len(white_men)} peões vs Pretas {len(black_men)} peões")
print()

# Verificar capturas disponíveis
captures = game.find_all_captures()

if captures:
    print(f"Capturas disponíveis: {len(captures)}")
    print()

    # Mostrar capturas ordenadas por quantidade de peças capturadas
    captures_sorted = sorted(captures, key=lambda c: len(c.captured_fields), reverse=True)

    for i, cap in enumerate(captures_sorted[:5], 1):  # Top 5
        from_pos = Pos64(cap.from_field).to_algebraic()
        to_pos = Pos64(cap.to_field).to_algebraic()
        num_pieces = len(cap.captured_fields)

        notation = f"{from_pos}"
        for cf in cap.captured_fields:
            notation += f" x {Pos64(cf).to_algebraic()}"
        notation += f" → {to_pos}"

        if cap.promotes:
            notation += " ♛"

        print(f"{i}. {notation} ({num_pieces} peça{'s' if num_pieces > 1 else ''})")
else:
    print("Nenhuma captura obrigatória. Movimentos simples disponíveis.")

print()
print("=" * 70)
print("ANÁLISE COM MOTOR V2 (Profundidade Adaptativa)")
print("=" * 70)
print()

motor = ImprovedTacticalSearchEngine()

# Testar em múltiplas profundidades
for depth in [8, 10, 12]:
    print(f"\n--- Profundidade {depth} ---")
    best_move, score, pv_sequence = motor.search_best_move(game, max_depth=depth)

    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score:+.0f}")

    if pv_sequence:
        print(f"Variante principal ({len(pv_sequence)} lances):")
        for i, move in enumerate(pv_sequence[:5], 1):  # Primeiros 5 lances
            print(f"  {i}. {move}")

print()
print("=" * 70)
print("CONCLUSÃO")
print("=" * 70)
print()

if score > 300:
    print("✅ Motor encontrou lance vencedor!")
    print(f"   Melhor lance: {best_move}")
    print(f"   Avaliação: {score:+.0f}")
elif abs(score) < 50:
    print("⚖️  Posição equilibrada (possível empate)")
elif score < -300:
    print("⚠️  Pretas têm vantagem")
else:
    print("📊 Posição complexa, avaliação moderada")

print()
