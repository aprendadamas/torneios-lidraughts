"""
Exercício #20 - "1800 Combinações"
FEN: W:Wg3,h4:Be3,c5,e5,c7.

Brancas: 2 peões vs Pretas: 4 peões
Grande desvantagem material - deve ter tática forte!
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #20 - Análise Inicial")
print("=" * 70)
print()

# FEN: W:Wg3,h4:Be3,c5,e5,c7.
# Brancas (2 peões): g3, h4
# Pretas (4 peões): e3, c5, e5, c7

white_men = {
    Pos64.from_algebraic("g3").field,  # 24
    Pos64.from_algebraic("h4").field,  # 20
}

black_men = {
    Pos64.from_algebraic("e3").field,  # 23
    Pos64.from_algebraic("c5").field,  # 14
    Pos64.from_algebraic("e5").field,  # 15
    Pos64.from_algebraic("c7").field,  # 6
}

white_kings = set()
black_kings = set()

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Material: Brancas {len(white_men)} peões vs Pretas {len(black_men)} peões")
print(f"Desvantagem: -2 peões (Brancas precisam de tática forte!)")
print()

# Verificar capturas disponíveis
captures = game.find_all_captures()

if captures:
    print(f"Capturas obrigatórias disponíveis: {len(captures)}")
    print()

    # Mostrar todas as capturas ordenadas
    captures_sorted = sorted(captures, key=lambda c: len(c.captured_fields), reverse=True)

    for i, cap in enumerate(captures_sorted, 1):
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

    # Mostrar movimentos simples disponíveis
    simple_moves = game.find_simple_moves()
    if simple_moves:
        print(f"\nMovimentos simples disponíveis: {len(simple_moves)}")
        for move in simple_moves[:10]:  # Mostrar até 10
            # simple_moves retorna tuplas (from_field, to_field)
            from_pos = Pos64(move[0]).to_algebraic()
            to_pos = Pos64(move[1]).to_algebraic()
            print(f"  - {from_pos} → {to_pos}")

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

    if pv_sequence and len(pv_sequence) > 1:
        print(f"Variante principal ({len(pv_sequence)} lances):")
        for i, move in enumerate(pv_sequence[:8], 1):  # Primeiros 8 lances
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
    print("   (Provavelmente vitória tática apesar da desvantagem material)")
elif score > 200:
    print("✅ Motor encontrou lance vencedor!")
    print(f"   Melhor lance: {best_move}")
    print(f"   Avaliação: {score:+.0f}")
elif abs(score) < 50:
    print("⚖️  Posição equilibrada (possível empate)")
elif score < -200:
    print("⚠️  Pretas têm vantagem decisiva")
    print(f"   Avaliação: {score:+.0f}")
else:
    print(f"📊 Avaliação: {score:+.0f}")

print()
