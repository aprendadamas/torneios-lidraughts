"""
Exercícios táticos de damas brasileiras
Analisa posições e encontra a melhor sequência
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game import Game
from src.piece import Piece, Color, PieceType
from src.utils import algebraic_to_coords, coords_to_algebraic


def setup_position_from_fen(fen_string):
    """
    Configura posição a partir de notação FEN
    Formato: W:Wc1,b2,d2:Ba3,d6,h6
    W/B indica se é dama (maiúscula) ou peça simples (minúscula)
    """
    game = Game()
    game.board = game.board.__class__()

    parts = fen_string.split(':')
    current_player = parts[0]  # W ou B
    white_pieces_str = parts[1] if len(parts) > 1 else ""
    black_pieces_str = parts[2] if len(parts) > 2 else ""

    # Processar peças brancas
    # Remove o W inicial e divide por vírgula
    white_pieces_str = white_pieces_str.replace('W', '', 1)  # Remove apenas o primeiro W
    white_pieces = [p.strip() for p in white_pieces_str.split(',') if p.strip()]

    # Processar peças pretas
    black_pieces_str = black_pieces_str.replace('B', '', 1).replace('.', '')
    black_pieces = [p.strip() for p in black_pieces_str.split(',') if p.strip()]

    print(f"\nDebug - Peças brancas: {white_pieces}")
    print(f"Debug - Peças pretas: {black_pieces}")

    # Configurar peças brancas
    for piece_notation in white_pieces:
        if not piece_notation:
            continue

        # Em FEN de damas, K antes da posição indica dama (ex: Kc1)
        is_king = piece_notation[0] == 'K'
        pos_str = piece_notation[1:] if is_king else piece_notation

        # Converter notação para coordenadas
        pos = algebraic_to_coords(pos_str)

        piece_type = PieceType.KING if is_king else PieceType.MAN
        piece = Piece(Color.WHITE, pos, piece_type)
        game.board.place_piece(piece, pos)
        game.board.pieces[Color.WHITE].append(piece)

        print(f"  Branca em {pos_str} -> {pos} ({'dama' if is_king else 'simples'})")

    # Configurar peças pretas
    for piece_notation in black_pieces:
        if not piece_notation:
            continue

        is_king = piece_notation[0] == 'K'
        pos_str = piece_notation[1:] if is_king else piece_notation

        pos = algebraic_to_coords(pos_str)

        piece_type = PieceType.KING if is_king else PieceType.MAN
        piece = Piece(Color.BLACK, pos, piece_type)
        game.board.place_piece(piece, pos)
        game.board.pieces[Color.BLACK].append(piece)

        print(f"  Preta em {pos_str} -> {pos} ({'dama' if is_king else 'simples'})")

    # Definir jogador atual
    game.current_player = Color.WHITE if current_player == 'W' else Color.BLACK

    return game


def analyze_position(game):
    """Analisa uma posição e mostra os melhores lances"""
    print("\n" + "="*60)
    print("ANÁLISE DA POSIÇÃO")
    print("="*60)

    # Mostrar tabuleiro
    print("\nPosição atual:")
    game.display_board()

    # Informações
    print(f"\nJogador atual: {game.current_player.value}")
    print(f"Peças brancas: {game.board.count_pieces(Color.WHITE)}")
    print(f"Peças pretas: {game.board.count_pieces(Color.BLACK)}")

    # Obter todos os movimentos legais
    all_moves = game.get_all_legal_moves()

    if not all_moves:
        print("\n❌ Nenhum movimento legal disponível!")
        if game.is_game_over():
            winner = game.get_winner()
            print(f"🏆 Jogo terminado! Vencedor: {winner.value if winner else 'Empate'}")
        return None

    print(f"\nTotal de posições com movimentos: {len(all_moves)}")

    # Analisar capturas
    has_captures = any(any(m.is_capture() for m in moves) for moves in all_moves.values())

    if has_captures:
        print("\n🎯 CAPTURAS DISPONÍVEIS (obrigatórias):")

        # Encontrar a captura com mais peças
        max_captures = 0
        best_moves = []

        for pos, moves in all_moves.items():
            for move in moves:
                if move.is_capture():
                    num_captures = len(move.captures)
                    if num_captures > max_captures:
                        max_captures = num_captures
                        best_moves = [(pos, move)]
                    elif num_captures == max_captures:
                        best_moves.append((pos, move))

        print(f"\nCaptura máxima: {max_captures} peça(s)")
        print(f"Número de sequências possíveis: {len(best_moves)}")

        print("\n📋 MELHORES MOVIMENTOS:")
        for i, (pos, move) in enumerate(best_moves, 1):
            from_alg = coords_to_algebraic(move.from_pos)
            to_alg = coords_to_algebraic(move.to_pos)
            captures_str = " -> ".join([coords_to_algebraic(c) for c in move.captures])
            promo = " [VIRA DAMA!]" if move.is_promotion else ""

            print(f"\n{i}. {from_alg} -> {to_alg}")
            print(f"   Captura: {captures_str}{promo}")
            print(f"   Total de peças capturadas: {len(move.captures)}")

        return best_moves
    else:
        print("\n♟️  MOVIMENTOS SIMPLES DISPONÍVEIS:")

        count = 0
        for pos, moves in all_moves.items():
            from_alg = coords_to_algebraic(pos)
            print(f"\nPeça em {from_alg}:")
            for move in moves[:3]:  # Mostrar até 3 movimentos por peça
                to_alg = coords_to_algebraic(move.to_pos)
                promo = " [VIRA DAMA!]" if move.is_promotion else ""
                print(f"  - {from_alg} -> {to_alg}{promo}")
                count += 1

        print(f"\nTotal de movimentos simples: {count}")
        return None


def test_exercise_1():
    """
    Exercício 1 do Curso Aprenda Damas
    [White "15"]
    [Black "Curso Aprenda Damas"]
    [Event "1800 Combinacoes - Do basico ao Avancado"]
    FEN: W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8
    """
    print("\n" + "🎯"*30)
    print("EXERCÍCIO #1 - 1800 Combinações")
    print("Curso Aprenda Damas - Do Básico ao Avançado")
    print("🎯"*30)

    fen = "W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8."

    print(f"\nFEN: {fen}")
    print("\nPeças Brancas: c1, b2, d2, f4, h4")
    print("Peças Pretas: a3, d6, h6, e7, f8")
    print("Vez das: BRANCAS")

    game = setup_position_from_fen(fen)
    best_moves = analyze_position(game)

    if best_moves:
        print("\n" + "="*60)
        print("SOLUÇÃO RECOMENDADA")
        print("="*60)

        # Executar o melhor movimento
        pos, move = best_moves[0]
        from_alg = coords_to_algebraic(move.from_pos)
        to_alg = coords_to_algebraic(move.to_pos)

        print(f"\nMelhor lance: {from_alg} -> {to_alg}")
        print(f"Captura {len(move.captures)} peça(s)")

        # Mostrar a sequência
        print("\nSequência de capturas:")
        for i, capture_pos in enumerate(move.captures, 1):
            print(f"  {i}. Captura em {coords_to_algebraic(capture_pos)}")

        # Executar o movimento
        print("\n" + "-"*60)
        print("Executando o movimento...")
        print("-"*60)

        game.make_move(move.from_pos, move.to_pos)

        print("\nPosição após o movimento:")
        game.display_board()

        print(f"\nPeças brancas: {game.board.count_pieces(Color.WHITE)}")
        print(f"Peças pretas: {game.board.count_pieces(Color.BLACK)}")

        if game.is_game_over():
            winner = game.get_winner()
            print(f"\n🏆 JOGO TERMINADO! Vencedor: {winner.value if winner else 'Empate'}")


def interactive_fen():
    """Modo interativo para testar posições FEN"""
    print("\n" + "="*60)
    print("MODO INTERATIVO - ANÁLISE DE POSIÇÕES FEN")
    print("="*60)

    while True:
        print("\n" + "-"*60)
        fen = input("\nDigite a notação FEN (ou 'quit' para sair):\n> ").strip()

        if fen.lower() == 'quit':
            break

        try:
            game = setup_position_from_fen(fen)
            analyze_position(game)

            # Perguntar se quer executar um movimento
            exec_move = input("\nExecutar melhor movimento? (s/n): ").strip().lower()
            if exec_move == 's':
                all_moves = game.get_all_legal_moves()
                if all_moves:
                    # Pegar o primeiro movimento disponível
                    pos = list(all_moves.keys())[0]
                    move = all_moves[pos][0]

                    game.make_move(move.from_pos, move.to_pos)
                    print("\nPosição após o movimento:")
                    game.display_board()

        except Exception as e:
            print(f"\n❌ Erro ao processar FEN: {e}")
            import traceback
            traceback.print_exc()


def main():
    """Menu principal"""
    while True:
        print("\n" + "="*60)
        print("EXERCÍCIOS TÁTICOS DE DAMAS BRASILEIRAS")
        print("="*60)
        print("\n1. Exercício #1 (1800 Combinações)")
        print("2. Modo interativo (inserir FEN manualmente)")
        print("0. Sair")

        choice = input("\nEscolha uma opção: ").strip()

        if choice == '1':
            test_exercise_1()
        elif choice == '2':
            interactive_fen()
        elif choice == '0':
            print("\nAté logo!")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
