"""
Exercício #1 - "4800 Combinações - Avançado" (Análise Focada)
FEN: W:WKa1,c3,g3,h4,a5,e5,f6:BKc1,c5,h6,Kf8.

Análise rápida com foco em capturas disponíveis
"""

from src.brazilian_engine_complete import BrazilianGameComplete
from src.tactical_engine_v2 import ImprovedTacticalSearchEngine
from src.pos64 import Pos64

print("=" * 70)
print("EXERCÍCIO #1 - \"4800 AVANÇADO\" - ANÁLISE FOCADA")
print("=" * 70)
print()

# Brancas: 1♛ (a1) + 6 peões (c3, g3, h4, a5, e5, f6)
# Pretas: 2♛ (c1, f8) + 2 peões (c5, h6)

white_men = {22, 24, 20, 13, 15, 11}  # c3, g3, h4, a5, e5, f6
white_kings = {29}  # a1
black_men = {14, 12}  # c5, h6
black_kings = {30, 3}  # c1, f8

game = BrazilianGameComplete(white_men, black_men, white_kings, black_kings)
game.print_board("POSIÇÃO INICIAL")

print()
print(f"Material:")
print(f"  Brancas: 1♛ + 6 peões = 7 peças")
print(f"  Pretas: 2♛ + 2 peões = 4 peças")
print()

# Analisar capturas disponíveis em detalhe
captures = game.find_all_captures()

if captures:
    print(f"❌ HÁ CAPTURAS OBRIGATÓRIAS: {len(captures)}")
    print()

    # Agrupar por peça de origem
    from_fields = {}
    for cap in captures:
        if cap.from_field not in from_fields:
            from_fields[cap.from_field] = []
        from_fields[cap.from_field].append(cap)

    # Mostrar capturas por peça
    for from_field in sorted(from_fields.keys()):
        from_pos = Pos64(from_field).to_algebraic()
        caps = from_fields[from_field]

        # Verificar se é dama ou peão
        is_king = from_field in white_kings
        piece_type = "♛" if is_king else "peão"

        print(f"{from_pos} ({piece_type}): {len(caps)} captura(s)")

        # Mostrar cada captura
        for cap in sorted(caps, key=lambda c: len(c.captured_fields), reverse=True):
            to_pos = Pos64(cap.to_field).to_algebraic()
            num_pieces = len(cap.captured_fields)

            notation = f"  {from_pos}"
            for cf in cap.captured_fields:
                notation += f" x {Pos64(cf).to_algebraic()}"
            notation += f" → {to_pos}"

            if cap.promotes:
                notation += " ♛"

            print(f"{notation} ({num_pieces} peça{'s' if num_pieces > 1 else ''})")
        print()

    # Encontrar a melhor captura (mais peças)
    best_capture = max(captures, key=lambda c: len(c.captured_fields))
    from_pos = Pos64(best_capture.from_field).to_algebraic()
    to_pos = Pos64(best_capture.to_field).to_algebraic()

    print("=" * 70)
    print(f"MELHOR CAPTURA: {from_pos} captura {len(best_capture.captured_fields)} peça(s)")
    print("=" * 70)

else:
    print("✓ Não há capturas obrigatórias")
    print()

    # Análise com motor (profundidade reduzida)
    print("=" * 70)
    print("ANÁLISE COM MOTOR V2 (Profundidade 6)")
    print("=" * 70)
    print()

    motor = ImprovedTacticalSearchEngine()

    best_move, score, pv_sequence = motor.search_best_move(game, max_depth=6)

    print(f"Melhor lance: {best_move}")
    print(f"Avaliação: {score:+.0f}")

    if pv_sequence:
        print(f"\nVariante principal ({len(pv_sequence)} lances):")
        for i, move in enumerate(pv_sequence[:8], 1):
            print(f"  {i}. {move}")

    print()
    print("=" * 70)
    print("CONCLUSÃO")
    print("=" * 70)

    if score > 300:
        print("✅ Lance vencedor encontrado!")
    elif score > 100:
        print("✅ Vantagem significativa")
    elif abs(score) < 50:
        print("⚖️  Posição equilibrada")
    else:
        print(f"📊 Avaliação: {score:+.0f}")

print()
