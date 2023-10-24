import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestKing(unittest.TestCase):

    def test_king(self):
        chessBoard = Chessboard()

        chessBoard.move(BoardPosition(4, 1), BoardPosition(4, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 0), BoardPosition(5, 2))
        chessBoard.move(BoardPosition(3, 6), BoardPosition(3, 5))
        chessBoard.move(BoardPosition(5, 2), BoardPosition(5, 6))
        chessBoard.move(BoardPosition(4, 7), BoardPosition(5, 6))
        self.assertEqual(chessBoard.getFEN(
        ), "rnbq1bnr/ppp2kpp/3p4/4p3/4P3/8/PPPP1PPP/RNB1KBNR w KQ - 0 4")
