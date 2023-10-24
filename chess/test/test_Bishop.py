import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestBishop(unittest.TestCase):

    def test_bishop(self):
        chessBoard = Chessboard()

        chessBoard.move(BoardPosition(3, 1), BoardPosition(3, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(2, 0), BoardPosition(6, 4))
        chessBoard.move(BoardPosition(5, 7), BoardPosition(3, 5))
        chessBoard.move(BoardPosition(6, 4), BoardPosition(3, 7))
        self.assertEqual(chessBoard.getFEN(
        ), "rnbBk1nr/pppp1ppp/3b4/4p3/3P4/8/PPP1PPPP/RN1QKBNR b KQkq - 0 3")
