import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestQueen(unittest.TestCase):

    def test_queen(self):
        chessBoard = Chessboard()

        chessBoard.move(BoardPosition(4, 1), BoardPosition(4, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 0), BoardPosition(6, 3))
        chessBoard.move(BoardPosition(3, 6), BoardPosition(3, 5))
        chessBoard.move(BoardPosition(6, 3), BoardPosition(6, 6))
        self.assertEqual(chessBoard.getFEN(
        ), "rnbqkbnr/ppp2pQp/3p4/4p3/4P3/8/PPPP1PPP/RNB1KBNR b KQkq - 0 3")
