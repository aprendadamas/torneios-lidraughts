"""
Testes para o módulo do tabuleiro
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from src.board import Board
from src.piece import Piece, Color, PieceType


class TestBoard(unittest.TestCase):
    """Testes para a classe Board"""

    def setUp(self):
        """Configuração antes de cada teste"""
        self.board = Board()

    def test_board_creation(self):
        """Testa criação do tabuleiro"""
        self.assertEqual(self.board.size, 8)
        self.assertEqual(len(self.board.board), 8)
        self.assertEqual(len(self.board.board[0]), 8)

    def test_initial_position(self):
        """Testa configuração inicial"""
        self.board.setup_initial_position()

        # Verificar número de peças
        self.assertEqual(self.board.count_pieces(Color.WHITE), 12)
        self.assertEqual(self.board.count_pieces(Color.BLACK), 12)

        # Verificar que peças brancas estão nas linhas 0-2
        white_pieces = self.board.get_pieces_by_color(Color.WHITE)
        for piece in white_pieces:
            self.assertIn(piece.position[0], [0, 1, 2])

        # Verificar que peças pretas estão nas linhas 5-7
        black_pieces = self.board.get_pieces_by_color(Color.BLACK)
        for piece in black_pieces:
            self.assertIn(piece.position[0], [5, 6, 7])

    def test_is_valid_position(self):
        """Testa validação de posições"""
        self.assertTrue(self.board.is_valid_position((0, 0)))
        self.assertTrue(self.board.is_valid_position((7, 7)))
        self.assertTrue(self.board.is_valid_position((3, 4)))

        self.assertFalse(self.board.is_valid_position((-1, 0)))
        self.assertFalse(self.board.is_valid_position((0, -1)))
        self.assertFalse(self.board.is_valid_position((8, 0)))
        self.assertFalse(self.board.is_valid_position((0, 8)))

    def test_is_dark_square(self):
        """Testa identificação de casas escuras"""
        # Casas escuras (soma ímpar)
        self.assertTrue(self.board.is_dark_square((0, 1)))
        self.assertTrue(self.board.is_dark_square((1, 0)))
        self.assertTrue(self.board.is_dark_square((2, 3)))

        # Casas claras (soma par)
        self.assertFalse(self.board.is_dark_square((0, 0)))
        self.assertFalse(self.board.is_dark_square((1, 1)))
        self.assertFalse(self.board.is_dark_square((2, 2)))

    def test_place_and_get_piece(self):
        """Testa colocação e obtenção de peças"""
        piece = Piece(Color.WHITE, (3, 2))
        self.board.place_piece(piece, (3, 2))

        retrieved = self.board.get_piece((3, 2))
        self.assertIs(piece, retrieved)
        self.assertEqual(retrieved.position, (3, 2))

    def test_is_empty(self):
        """Testa verificação de casa vazia"""
        self.assertTrue(self.board.is_empty((3, 2)))

        piece = Piece(Color.WHITE, (3, 2))
        self.board.place_piece(piece, (3, 2))

        self.assertFalse(self.board.is_empty((3, 2)))

    def test_remove_piece(self):
        """Testa remoção de peças"""
        piece = Piece(Color.WHITE, (3, 2))
        self.board.place_piece(piece, (3, 2))
        self.board.pieces[Color.WHITE].append(piece)

        removed = self.board.remove_piece((3, 2))
        self.assertIs(piece, removed)
        self.assertTrue(self.board.is_empty((3, 2)))
        self.assertNotIn(piece, self.board.pieces[Color.WHITE])

    def test_move_piece(self):
        """Testa movimento de peças"""
        piece = Piece(Color.WHITE, (2, 1))
        self.board.place_piece(piece, (2, 1))

        self.board.move_piece((2, 1), (3, 2))

        self.assertTrue(self.board.is_empty((2, 1)))
        self.assertEqual(self.board.get_piece((3, 2)), piece)
        self.assertEqual(piece.position, (3, 2))

    def test_move_piece_with_promotion(self):
        """Testa movimento com coroação"""
        # Peça branca na linha 6
        piece = Piece(Color.WHITE, (6, 1))
        self.board.place_piece(piece, (6, 1))

        self.assertFalse(piece.is_king())

        # Mover para linha 7 (coroação)
        self.board.move_piece((6, 1), (7, 2))

        self.assertTrue(piece.is_king())

    def test_get_diagonal_path(self):
        """Testa obtenção do caminho diagonal"""
        # Diagonal descendente à direita
        path = self.board.get_diagonal_path((1, 0), (4, 3))
        self.assertEqual(path, [(2, 1), (3, 2)])

        # Diagonal ascendente à esquerda
        path = self.board.get_diagonal_path((5, 6), (3, 4))
        self.assertEqual(path, [(4, 5)])

        # Posições adjacentes (sem caminho intermediário)
        path = self.board.get_diagonal_path((2, 1), (3, 2))
        self.assertEqual(path, [])

    def test_board_copy(self):
        """Testa cópia do tabuleiro"""
        self.board.setup_initial_position()

        copy = self.board.copy()

        # Verificar que é uma cópia independente
        self.assertIsNot(self.board, copy)
        self.assertEqual(self.board.size, copy.size)
        self.assertEqual(self.board.count_pieces(Color.WHITE),
                         copy.count_pieces(Color.WHITE))
        self.assertEqual(self.board.count_pieces(Color.BLACK),
                         copy.count_pieces(Color.BLACK))

        # Modificar cópia não deve afetar original
        copy.remove_piece((0, 1))
        self.assertIsNotNone(self.board.get_piece((0, 1)))
        self.assertIsNone(copy.get_piece((0, 1)))

    def test_count_pieces(self):
        """Testa contagem de peças"""
        self.board.setup_initial_position()

        self.assertEqual(self.board.count_pieces(Color.WHITE), 12)
        self.assertEqual(self.board.count_pieces(Color.BLACK), 12)

        # Remover uma peça branca
        white_pieces = self.board.get_pieces_by_color(Color.WHITE)
        self.board.remove_piece(white_pieces[0].position)

        self.assertEqual(self.board.count_pieces(Color.WHITE), 11)
        self.assertEqual(self.board.count_pieces(Color.BLACK), 12)


if __name__ == '__main__':
    unittest.main()
