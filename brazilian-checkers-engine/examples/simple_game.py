"""
Exemplo simples de uso do motor de damas brasileiro
Demonstra como criar um jogo e fazer movimentos básicos
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.game import Game
from src.piece import Color
from src.utils import coords_to_algebraic, algebraic_to_coords


def print_game_state(game: Game):
    """Exibe o estado atual do jogo"""
    print("\n" + "="*50)
    print(f"Jogador atual: {game.get_current_player().value}")
    print(f"Movimentos realizados: {len(game.move_history)}")

    white_pieces = game.board.count_pieces(Color.WHITE)
    black_pieces = game.board.count_pieces(Color.BLACK)
    print(f"Peças brancas: {white_pieces} | Peças pretas: {black_pieces}")

    if game.is_game_over():
        winner = game.get_winner()
        print(f"\n*** JOGO FINALIZADO! Vencedor: {winner.value if winner else 'Empate'} ***")

    print("="*50)
    game.display_board()


def print_legal_moves(game: Game):
    """Exibe todos os movimentos legais disponíveis"""
    all_moves = game.get_all_legal_moves()

    if not all_moves:
        print("Nenhum movimento legal disponível!")
        return

    print("\nMovimentos legais disponíveis:")
    for pos, moves in all_moves.items():
        pos_algebraic = coords_to_algebraic(pos)
        print(f"\nPeça em {pos_algebraic} ({pos}):")
        for i, move in enumerate(moves):
            to_algebraic = coords_to_algebraic(move.to_pos)
            capture_info = f" - Captura {len(move.captures)} peça(s)" if move.is_capture() else ""
            promo_info = " [COROAÇÃO]" if move.is_promotion else ""
            print(f"  {i+1}. {pos_algebraic} -> {to_algebraic}{capture_info}{promo_info}")


def example_basic_moves():
    """Exemplo 1: Movimentos básicos"""
    print("\n### EXEMPLO 1: MOVIMENTOS BÁSICOS ###\n")

    game = Game()
    print_game_state(game)

    # Movimento 1: Brancas
    print("\n>>> Brancas movem: (2,1) -> (3,2)")
    success = game.make_move((2, 1), (3, 2))
    print(f"Movimento {'executado' if success else 'inválido'}!")
    print_game_state(game)

    # Movimento 2: Pretas
    print("\n>>> Pretas movem: (5,2) -> (4,3)")
    success = game.make_move((5, 2), (4, 3))
    print(f"Movimento {'executado' if success else 'inválido'}!")
    print_game_state(game)

    # Movimento 3: Brancas
    print("\n>>> Brancas movem: (2,3) -> (3,4)")
    success = game.make_move((2, 3), (3, 4))
    print(f"Movimento {'executado' if success else 'inválido'}!")
    print_game_state(game)


def example_capture():
    """Exemplo 2: Captura simples"""
    print("\n### EXEMPLO 2: CAPTURA SIMPLES ###\n")

    game = Game()

    # Preparar uma situação de captura
    moves = [
        ((2, 1), (3, 2)),  # Brancas
        ((5, 0), (4, 1)),  # Pretas
        ((3, 2), (4, 3)),  # Brancas
    ]

    for from_pos, to_pos in moves:
        game.make_move(from_pos, to_pos)

    print_game_state(game)
    print("\n>>> Pretas DEVEM capturar (captura obrigatória)")
    print_legal_moves(game)

    # Executar a captura
    print("\n>>> Pretas capturam: (4,1) -> (2,3)")
    success = game.make_move((4, 1), (2, 3))
    print(f"Movimento {'executado' if success else 'inválido'}!")
    print_game_state(game)


def example_multiple_captures():
    """Exemplo 3: Captura múltipla"""
    print("\n### EXEMPLO 3: CAPTURA MÚLTIPLA ###\n")

    # Criar um cenário customizado para captura múltipla
    game = Game()

    # Limpar o tabuleiro e criar posição específica
    game.board = game.board.__class__()

    from src.piece import Piece, PieceType

    # Configurar posição para captura múltipla
    # Peça branca que vai capturar
    white_piece = Piece(Color.WHITE, (2, 1))
    game.board.place_piece(white_piece, (2, 1))
    game.board.pieces[Color.WHITE].append(white_piece)

    # Peças pretas para serem capturadas
    black1 = Piece(Color.BLACK, (3, 2))
    game.board.place_piece(black1, (3, 2))
    game.board.pieces[Color.BLACK].append(black1)

    black2 = Piece(Color.BLACK, (3, 4))
    game.board.place_piece(black2, (3, 4))
    game.board.pieces[Color.BLACK].append(black2)

    # Uma peça preta adicional para contexto
    black3 = Piece(Color.BLACK, (5, 0))
    game.board.place_piece(black3, (5, 0))
    game.board.pieces[Color.BLACK].append(black3)

    print_game_state(game)
    print("\n>>> Brancas podem fazer captura múltipla!")
    print_legal_moves(game)

    # Primeira captura
    print("\n>>> Brancas capturam: (2,1) -> (4,3)")
    success = game.make_move((2, 1), (4, 3))
    print(f"Movimento {'executado' if success else 'inválido'}!")

    # Se a captura múltipla for automática, ela já foi feita
    # Se não, precisamos fazer a segunda captura
    print_game_state(game)


def example_promotion():
    """Exemplo 4: Coroação (virar dama)"""
    print("\n### EXEMPLO 4: COROAÇÃO ###\n")

    game = Game()
    game.board = game.board.__class__()

    from src.piece import Piece

    # Peça branca próxima à coroação
    white_piece = Piece(Color.WHITE, (6, 1))
    game.board.place_piece(white_piece, (6, 1))
    game.board.pieces[Color.WHITE].append(white_piece)

    # Peça preta para contexto
    black_piece = Piece(Color.BLACK, (5, 0))
    game.board.place_piece(black_piece, (5, 0))
    game.board.pieces[Color.BLACK].append(black_piece)

    print_game_state(game)
    print("\n>>> Brancas vão coroar!")
    print_legal_moves(game)

    print("\n>>> Brancas movem: (6,1) -> (7,2) e viram DAMA")
    success = game.make_move((6, 1), (7, 2))
    print(f"Movimento {'executado' if success else 'inválido'}!")
    print_game_state(game)

    # Verificar se é dama
    piece = game.board.get_piece((7, 2))
    print(f"\nA peça em (7,2) é uma dama: {piece.is_king()}")


def interactive_game():
    """Jogo interativo no terminal"""
    print("\n### JOGO INTERATIVO ###\n")
    print("Comandos:")
    print("  - Digite 'moves' para ver movimentos legais")
    print("  - Digite 'quit' para sair")
    print("  - Digite o movimento no formato: (linha,col)-(linha,col)")
    print("    Exemplo: (2,1)-(3,2)\n")

    game = Game()

    while not game.is_game_over():
        print_game_state(game)

        cmd = input(f"\n{game.get_current_player().value} > ").strip().lower()

        if cmd == 'quit':
            print("Saindo...")
            break
        elif cmd == 'moves':
            print_legal_moves(game)
        elif '-' in cmd:
            try:
                # Parse do movimento
                parts = cmd.split('-')
                from_pos = eval(parts[0])
                to_pos = eval(parts[1])

                success = game.make_move(from_pos, to_pos)
                if not success:
                    print("❌ Movimento inválido! Tente novamente.")
            except Exception as e:
                print(f"❌ Erro ao processar movimento: {e}")
                print("Use o formato: (linha,col)-(linha,col)")
        else:
            print("Comando não reconhecido. Digite 'moves' ou um movimento.")

    print_game_state(game)
    print("\nObrigado por jogar!")


def main():
    """Função principal - executa todos os exemplos"""
    print("="*50)
    print("MOTOR DE DAMAS BRASILEIRO - EXEMPLOS")
    print("="*50)

    while True:
        print("\n\nEscolha um exemplo:")
        print("1. Movimentos básicos")
        print("2. Captura simples")
        print("3. Captura múltipla")
        print("4. Coroação (virar dama)")
        print("5. Jogo interativo")
        print("0. Sair")

        choice = input("\nOpção: ").strip()

        if choice == '1':
            example_basic_moves()
        elif choice == '2':
            example_capture()
        elif choice == '3':
            example_multiple_captures()
        elif choice == '4':
            example_promotion()
        elif choice == '5':
            interactive_game()
        elif choice == '0':
            print("\nAté logo!")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
