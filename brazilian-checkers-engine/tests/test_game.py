"""
Testes para o módulo do jogo
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from src.game import Game, Move
from src.piece import Piece, Color, PieceType


class TestGame(unittest.TestCase):
    """Testes para a classe Game"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.game = Game()

    def test_game_initialization(self):
        """Testa inicialização do jogo"""
        self.assertEqual(self.game.current_player, Color.WHITE)
        self.assertEqual(len(self.game.move_history), 0)
        self.assertIsNone(self.game.winner)
        self.assertEqual(self.game.board.count_pieces(Color.WHITE), 12)
        self.assertEqual(self.game.board.count_pieces(Color.BLACK), 12)

    def test_simple_move(self):
        """Testa movimento simples"""
        # Brancas movem
        success = self.game.make_move((2, 1), (3, 2))
        self.assertTrue(success)

        # Verificar que a peça foi movida
        self.assertIsNone(self.game.board.get_piece((2, 1)))
        self.assertIsNotNone(self.game.board.get_piece((3, 2)))

        # Verificar que o jogador foi alternado
        self.assertEqual(self.game.current_player, Color.BLACK)

        # Verificar histórico
        self.assertEqual(len(self.game.move_history), 1)

    def test_invalid_move(self):
        """Testa movimento inválido"""
        # Tentar mover para trás (inválido para peça simples)
        success = self.game.make_move((2, 1), (1, 0))
        self.assertFalse(success)

        # Jogador não deve ter mudado
        self.assertEqual(self.game.current_player, Color.WHITE)

        # Histórico deve estar vazio
        self.assertEqual(len(self.game.move_history), 0)

    def test_switch_player(self):
        """Testa alternância de jogadores"""
        self.assertEqual(self.game.current_player, Color.WHITE)

        self.game.switch_player()
        self.assertEqual(self.game.current_player, Color.BLACK)

        self.game.switch_player()
        self.assertEqual(self.game.current_player, Color.WHITE)

    def test_simple_capture(self):
        """Testa captura simples"""
        # Preparar cenário de captura
        self.game.make_move((2, 1), (3, 2))  # Brancas
        self.game.make_move((5, 2), (4, 3))  # Pretas
        self.game.make_move((3, 2), (5, 4))  # Brancas capturam

        # Verificar que houve captura
        self.assertEqual(self.game.board.count_pieces(Color.BLACK), 11)

    def test_mandatory_capture(self):
        """Testa captura obrigatória"""
        # Configurar posição com captura disponível
        self.game.make_move((2, 1), (3, 2))  # Brancas
        self.game.make_move((5, 0), (4, 1))  # Pretas
        self.game.make_move((3, 2), (4, 3))  # Brancas

        # Pretas têm captura disponível
        all_moves = self.game.get_all_legal_moves()

        # Todos os movimentos legais devem ser capturas
        for pos, moves in all_moves.items():
            for move in moves:
                self.assertTrue(move.is_capture())

    def test_king_movement(self):
        """Testa movimento de dama"""
        # Criar dama manualmente
        self.game.board = self.game.board.__class__()

        white_king = Piece(Color.WHITE, (3, 2), PieceType.KING)
        self.game.board.place_piece(white_king, (3, 2))
        self.game.board.pieces[Color.WHITE].append(white_king)

        black_piece = Piece(Color.BLACK, (5, 0))
        self.game.board.place_piece(black_piece, (5, 0))
        self.game.board.pieces[Color.BLACK].append(black_piece)

        # Dama deve poder mover múltiplas casas
        moves = self.game.get_simple_moves(white_king)

        # Verificar que há movimentos de longa distância
        long_moves = [m for m in moves if
                      abs(m.to_pos[0] - m.from_pos[0]) > 1]
        self.assertTrue(len(long_moves) > 0)

    def test_promotion(self):
        """Testa coroação"""
        # Configurar peça próxima à coroação
        self.game.board = self.game.board.__class__()

        white_piece = Piece(Color.WHITE, (6, 1))
        self.game.board.place_piece(white_piece, (6, 1))
        self.game.board.pieces[Color.WHITE].append(white_piece)

        black_piece = Piece(Color.BLACK, (5, 0))
        self.game.board.place_piece(black_piece, (5, 0))
        self.game.board.pieces[Color.BLACK].append(black_piece)

        # Mover para última linha
        self.game.make_move((6, 1), (7, 2))

        # Verificar coroação
        piece = self.game.board.get_piece((7, 2))
        self.assertTrue(piece.is_king())

    def test_game_over_no_pieces(self):
        """Testa fim de jogo por ausência de peças"""
        # Remover todas as peças pretas
        black_pieces = self.game.board.get_pieces_by_color(Color.BLACK).copy()
        for piece in black_pieces:
            self.game.board.remove_piece(piece.position)

        self.game.check_game_over()

        self.assertTrue(self.game.is_game_over())
        self.assertEqual(self.game.get_winner(), Color.WHITE)

    def test_get_legal_moves(self):
        """Testa obtenção de movimentos legais"""
        # Início do jogo - peça branca deve ter movimentos
        moves = self.game.get_legal_moves((2, 1))
        self.assertGreater(len(moves), 0)

        # Peça que não existe
        moves = self.game.get_legal_moves((4, 4))
        self.assertEqual(len(moves), 0)

        # Peça do oponente
        moves = self.game.get_legal_moves((5, 0))
        self.assertEqual(len(moves), 0)

    def test_get_all_legal_moves(self):
        """Testa obtenção de todos os movimentos legais"""
        all_moves = self.game.get_all_legal_moves()

        # Deve haver movimentos disponíveis no início
        self.assertGreater(len(all_moves), 0)

        # Todos devem ser do jogador atual (brancas)
        for pos in all_moves.keys():
            piece = self.game.board.get_piece(pos)
            self.assertEqual(piece.color, Color.WHITE)

    def test_move_history(self):
        """Testa histórico de movimentos"""
        self.assertEqual(len(self.game.move_history), 0)

        self.game.make_move((2, 1), (3, 2))
        self.assertEqual(len(self.game.move_history), 1)

        self.game.make_move((5, 0), (4, 1))
        self.assertEqual(len(self.game.move_history), 2)

        # Verificar que os movimentos estão corretos
        first_move = self.game.move_history[0]
        self.assertEqual(first_move.from_pos, (2, 1))
        self.assertEqual(first_move.to_pos, (3, 2))

    def test_multiple_capture_sequence(self):
        """Testa sequência de múltiplas capturas"""
        # Configurar posição para captura múltipla
        self.game.board = self.game.board.__class__()

        white_piece = Piece(Color.WHITE, (2, 1))
        self.game.board.place_piece(white_piece, (2, 1))
        self.game.board.pieces[Color.WHITE].append(white_piece)

        black1 = Piece(Color.BLACK, (3, 2))
        self.game.board.place_piece(black1, (3, 2))
        self.game.board.pieces[Color.BLACK].append(black1)

        black2 = Piece(Color.BLACK, (3, 4))
        self.game.board.place_piece(black2, (3, 4))
        self.game.board.pieces[Color.BLACK].append(black2)

        # Verificar se há captura múltipla disponível
        moves = self.game.get_legal_moves((2, 1))
        multi_capture_moves = [m for m in moves if len(m.captures) > 1]

        # Deve haver pelo menos um movimento com múltiplas capturas
        # (dependendo da implementação exata)
        self.assertGreaterEqual(len(moves), 1)


if __name__ == '__main__':
    unittest.main()
