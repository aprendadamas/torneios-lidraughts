#!/usr/bin/env python3
"""
Verify the correct solution for Exercise 1
"""

import sys
try:
    import draughts
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydraughts", "-q"])
    import draughts

from draughts import Board, Move

def verify_solution():
    """Verify the correct solution: 1. c3-b4 a5xc3 2. b2xd4xf6xh8"""

    fen = "W:Wa1,b2,c3:Ba5,e5,g7"
    board = Board(variant="brazilian", fen=fen)

    print("=" * 70)
    print("VERIFICANDO SOLUÇÃO CORRETA")
    print("=" * 70)
    print(f"\nFEN: {fen}")
    print("\nPosição inicial:")
    print(board)

    # Lista todos os movimentos legais
    print("\nMovimentos legais para as Brancas:")
    legal_moves = list(board.legal_moves())
    for i, move in enumerate(legal_moves, 1):
        print(f"  {i}. {move.pdn_move}")

    print("\n" + "=" * 70)
    print("LANCE 1: c3-b4")
    print("=" * 70)

    # Procurar o movimento c3-b4 (que é 10-13 em PDN)
    move_10_13 = None
    for move in legal_moves:
        if move.pdn_move == "10-13":
            move_10_13 = move
            break

    if move_10_13:
        board.push(move_10_13)
        print(f"\nMovimento executado: {move_10_13.pdn_move} (c3-b4)")
        print(board)

        print("\n" + "=" * 70)
        print("Resposta das Pretas: a5xc3")
        print("=" * 70)

        # Agora é a vez das pretas - ver movimentos disponíveis
        black_moves = list(board.legal_moves())
        print(f"\nMovimentos legais para as Pretas:")
        for i, move in enumerate(black_moves, 1):
            print(f"  {i}. {move.pdn_move}")

        # Procurar captura a5xc3 (17x10 em PDN)
        capture_move = None
        for move in black_moves:
            if 'x' in move.pdn_move and '10' in move.pdn_move:
                capture_move = move
                print(f"\n  --> Captura encontrada: {move.pdn_move}")
                break

        if capture_move:
            board.push(capture_move)
            print(f"\nMovimento executado: {capture_move.pdn_move}")
            print(board)

            print("\n" + "=" * 70)
            print("LANCE 2: b2xd4xf6xh8 (captura tripla)")
            print("=" * 70)

            # Movimentos das brancas agora
            white_moves = list(board.legal_moves())
            print(f"\nMovimentos legais para as Brancas:")
            for i, move in enumerate(white_moves, 1):
                notation = move.pdn_move
                print(f"  {i}. {notation}")
                # Se for captura múltipla, destacar
                if notation.count('x') >= 3:
                    print(f"      ^^^ CAPTURA TRIPLA! ^^^")

            # Procurar a captura tripla (5x32 = b2 captura até h8)
            triple_capture = None
            for move in white_moves:
                # Captura múltipla: de 5 (b2) para 32 (h8)
                if move.pdn_move == "5x32":
                    triple_capture = move
                    break
                # Ou qualquer captura longa
                if 'x' in move.pdn_move:
                    parts = move.pdn_move.split('x')
                    if len(parts) == 2:
                        start = int(parts[0])
                        end = int(parts[1])
                        # Se a distância é grande, provavelmente é captura múltipla
                        if abs(end - start) > 10:
                            triple_capture = move
                            break

            if triple_capture:
                print(f"\n  --> Captura tripla encontrada: {triple_capture.pdn_move}")
                board.push(triple_capture)
                print(f"\nMovimento executado: {triple_capture.pdn_move}")
                print(board)

                print("\n" + "=" * 70)
                print("VERIFICANDO RESULTADO")
                print("=" * 70)

                # Verificar se as pretas têm movimentos
                final_moves = list(board.legal_moves())
                print(f"\nMovimentos legais para as Pretas: {len(final_moves)}")

                if len(final_moves) == 0:
                    print("\n*** AS BRANCAS VENCEM! Pretas não têm movimentos legais ***")
                else:
                    print(f"\nPretas ainda têm {len(final_moves)} movimentos:")
                    for move in final_moves:
                        print(f"  - {move.pdn_move}")
            else:
                print("\n❌ ERRO: Captura tripla não encontrada!")
                print("\nO motor deveria ter gerado uma captura tripla, mas não gerou.")
                print("Isso indica um problema com a biblioteca pydraughts ou com o")
                print("entendimento das regras de capturas múltiplas.")
        else:
            print("\n❌ ERRO: Captura a5xc3 não encontrada!")
    else:
        print("\n❌ ERRO: Movimento c3-b4 não encontrado!")


if __name__ == "__main__":
    verify_solution()
