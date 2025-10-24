"""
Motor de Damas Brasileiras
Implementação das regras oficiais do jogo de damas brasileiro
"""

__version__ = "0.1.0"
__author__ = "Aprenda Damas"

from .piece import Piece, PieceType
from .board import Board
from .game import Game

__all__ = ['Piece', 'PieceType', 'Board', 'Game']
