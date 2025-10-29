"""
Exercício #1 - "4800 Combinações - Avançado"
FEN: W:WKa1,c3,g3,h4,a5,e5,f6:BKc1,c5,h6,Kf8.

Primeira posição do livro avançado - com DAMAS!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #1 - \"4800 COMBINAÇÕES - AVANÇADO\"")
print("=" * 70)
print()

# FEN: W:WKa1,c3,g3,h4,a5,e5,f6:BKc1,c5,h6,Kf8.
#
# Brancas:
# - WKa1 = dama branca em a1
# - Peões: c3, g3, h4, a5, e5, f6
# Total: 1 dama + 6 peões = 7 peças
#
# Pretas:
# - BKc1 = dama preta em c1
# - Kf8 = dama preta em f8 (notação alternativa)
# - Peões: c5, h6
# Total: 2 damas + 2 peões = 4 peças

white_men = {
    Pos64.from_algebraic("c3").field,  # 22
    Pos64.from_algebraic("g3").field,  # 24
    Pos64.from_algebraic("h4").field,  # 20
    Pos64.from_algebraic("a5").field,  # 13
    Pos64.from_algebraic("e5").field,  # 15
    Pos64.from_algebraic("f6").field,  # 11
}

white_kings = {
    Pos64.from_algebraic("a1").field,  # 29
}

black_men = {
    Pos64.from_algebraic("c5").field,  # 14
    Pos64.from_algebraic("h6").field,  # 12
}

black_kings = {
    Pos64.from_algebraic("c1").field,  # 30
    Pos64.from_algebraic("f8").field,  # 3
}

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Material:")
print(f"  Brancas: {len(white_kings)} dama + {len(white_men)} peões = {len(white_kings) + len(white_men)} peças")
print(f"  Pretas: {len(black_kings)} damas + {len(black_men)} peões = {len(black_kings) + len(black_men)} peças")
print()
print(f"Balanço: Pretas têm 1 dama a mais, mas brancas têm 4 peões a mais")
print()

# Verificar capturas disponíveis
captures = game.find_all_captures()

if captures:
    print(f"Capturas obrigatórias disponíveis: {len(captures)}")
    print()

    # Mostrar todas as capturas ordenadas
    captures_sorted = sorted(captures, key=lambda c: len(c.captured_fields), reverse=True)

    print("Top capturas (por número de peças):")
    for i, cap in enumerate(captures_sorted[:10], 1):
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
    print("Nenhuma captura obrigatória.")

    # Mostrar alguns movimentos simples
    simple_moves = game.find_simple_moves()
    if simple_moves:
        print(f"\nMovimentos simples disponíveis: {len(simple_moves)}")
        for move in simple_moves[:10]:
            from_pos = Pos64(move[0]).to_algebraic()
            to_pos = Pos64(move[1]).to_algebraic()
            print(f"  - {from_pos} → {to_pos}")

print()
print("=" * 70)
print("ANÁLISE COM MOTOR V2")
print("=" * 70)
print()

motor = ImprovedTacticalSearchEngine()

# Testar em múltiplas profundidades
for depth in [8, 10, 12]:
    print(f"\n--- Profundidade {depth} ---")
    best_move, score, pv_sequence = motor.search_best_move(game, max_depth=depth)

    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score:+.0f}")

    if pv_sequence and len(pv_sequence) > 1:
        print(f"Variante principal ({len(pv_sequence)} lances):")
        for i, move in enumerate(pv_sequence[:10], 1):
            print(f"  {i}. {move}")

print()
print("=" * 70)
print("CONCLUSÃO")
print("=" * 70)
print()

if score > 500:
    print("✅ Motor encontrou lance vencedor FORTE!")
    print(f"   Melhor lance: {best_move}")
    print(f"   Avaliação: {score:+.0f}")
elif score > 200:
    print("✅ Motor encontrou lance vencedor!")
    print(f"   Melhor lance: {best_move}")
    print(f"   Avaliação: {score:+.0f}")
elif abs(score) < 50:
    print("⚖️  Posição equilibrada")
elif score < -200:
    print("⚠️  Pretas têm vantagem")
    print(f"   Avaliação: {score:+.0f}")
else:
    print(f"📊 Avaliação: {score:+.0f}")

print()
print("=" * 70)
print("NOTA: Este é o primeiro exercício do livro AVANÇADO")
print("Esperamos táticas mais complexas e profundas!")
print("=" * 70)
