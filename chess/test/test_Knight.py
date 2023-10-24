import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestKnight(unittest.TestCase):

    def test_knight(self):
        chessBoard = Chessboard()

        chessBoard.move(BoardPosition(1, 0), BoardPosition(2, 2))
        chessBoard.move(BoardPosition(1, 7), BoardPosition(2, 5))
        chessBoard.move(BoardPosition(2, 2), BoardPosition(3, 4))
        chessBoard.move(BoardPosition(2, 5), BoardPosition(1, 3))
        chessBoard.move(BoardPosition(3, 4), BoardPosition(4, 6))
        self.assertEqual(chessBoard.getFEN(
        ), "r1bqkbnr/ppppNppp/8/8/1n6/8/PPPPPPPP/R1BQKBNR b KQkq - 0 3")
