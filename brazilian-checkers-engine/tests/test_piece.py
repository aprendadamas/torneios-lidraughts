"""
Testes para o módulo de peças
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from src.piece import Piece, Color, PieceType


class TestPiece(unittest.TestCase):
    """Testes para a classe Piece"""

    def test_piece_creation(self):
        """Testa criação de peça"""
        piece = Piece(Color.WHITE, (2, 1))
        self.assertEqual(piece.color, Color.WHITE)
        self.assertEqual(piece.position, (2, 1))
        self.assertEqual(piece.piece_type, PieceType.MAN)
        self.assertFalse(piece.is_king())

    def test_piece_promotion(self):
        """Testa promoção a dama"""
        piece = Piece(Color.WHITE, (6, 1))
        self.assertFalse(piece.is_king())

        piece.promote_to_king()
        self.assertTrue(piece.is_king())

    def test_forward_direction(self):
        """Testa direção de avanço"""
        white_piece = Piece(Color.WHITE, (2, 1))
        black_piece = Piece(Color.BLACK, (5, 2))

        self.assertEqual(white_piece.get_forward_direction(), 1)
        self.assertEqual(black_piece.get_forward_direction(), -1)

    def test_should_be_crowned_white(self):
        """Testa coroação para peças brancas"""
        # Peça branca não deve ser coroada na linha 6
        piece = Piece(Color.WHITE, (6, 1))
        self.assertFalse(piece.should_be_crowned())

        # Peça branca deve ser coroada na linha 7
        piece.position = (7, 2)
        self.assertTrue(piece.should_be_crowned())

    def test_should_be_crowned_black(self):
        """Testa coroação para peças pretas"""
        # Peça preta não deve ser coroada na linha 1
        piece = Piece(Color.BLACK, (1, 2))
        self.assertFalse(piece.should_be_crowned())

        # Peça preta deve ser coroada na linha 0
        piece.position = (0, 1)
        self.assertTrue(piece.should_be_crowned())

    def test_king_not_crowned_again(self):
        """Testa que damas não são coroadas novamente"""
        piece = Piece(Color.WHITE, (7, 2), PieceType.KING)
        self.assertFalse(piece.should_be_crowned())

    def test_can_move_backward(self):
        """Testa movimento para trás"""
        # Peças simples não podem mover para trás (exceto capturas)
        man = Piece(Color.WHITE, (3, 2))
        self.assertFalse(man.can_move_backward())

        # Damas podem mover para trás
        king = Piece(Color.WHITE, (3, 2), PieceType.KING)
        self.assertTrue(king.can_move_backward())

    def test_piece_copy(self):
        """Testa cópia de peça"""
        original = Piece(Color.WHITE, (2, 1), PieceType.KING)
        copy = original.copy()

        self.assertEqual(original.color, copy.color)
        self.assertEqual(original.position, copy.position)
        self.assertEqual(original.piece_type, copy.piece_type)
        self.assertIsNot(original, copy)

    def test_piece_string_representation(self):
        """Testa representação em string"""
        white_man = Piece(Color.WHITE, (2, 1))
        white_king = Piece(Color.WHITE, (3, 2), PieceType.KING)
        black_man = Piece(Color.BLACK, (5, 2))
        black_king = Piece(Color.BLACK, (6, 3), PieceType.KING)

        self.assertEqual(str(white_man), "w")
        self.assertEqual(str(white_king), "W")
        self.assertEqual(str(black_man), "b")
        self.assertEqual(str(black_king), "B")


if __name__ == '__main__':
    unittest.main()
