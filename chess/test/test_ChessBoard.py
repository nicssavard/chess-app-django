import unittest

from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestChessBoard(unittest.TestCase):

    def test_ChessBoard_initialization(self):
        pass
        chessBoard = Chessboard()
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "P", BoardPosition(0, 1)).to_FEN(), "P")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "p", BoardPosition(0, 1)).to_FEN(), "p")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "N", BoardPosition(0, 1)).to_FEN(), "N")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "K", BoardPosition(0, 1)).to_FEN(), "K")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "q", BoardPosition(0, 1)).to_FEN(), "q")
        self.assertEqual(chessBoard.getFEN(),
                         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


if __name__ == "__main__":
    unittest.main()
