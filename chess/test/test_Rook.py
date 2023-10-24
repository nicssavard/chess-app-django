import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestRook(unittest.TestCase):

    def test_rook(self):
        chessBoard = Chessboard()

        chessBoard.move(BoardPosition(0, 1), BoardPosition(0, 3))
        chessBoard.move(BoardPosition(0, 6), BoardPosition(0, 4))
        chessBoard.move(BoardPosition(0, 0), BoardPosition(0, 2))
        chessBoard.move(BoardPosition(0, 7), BoardPosition(0, 5))
        chessBoard.move(BoardPosition(0, 2), BoardPosition(2, 2))
        chessBoard.move(BoardPosition(0, 5), BoardPosition(1, 5))
        chessBoard.move(BoardPosition(2, 2), BoardPosition(2, 6))
        self.assertEqual(chessBoard.getFEN(
        ), "1nbqkbnr/1pRppppp/1r6/p7/P7/8/1PPPPPPP/1NBQKBNR b Kk - 0 4")
