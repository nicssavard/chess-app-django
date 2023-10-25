import unittest

from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition
from chess.classes.ChessPiece import PieceColor


class TestChessBoard(unittest.TestCase):

    def test_ChessBoard_initialization(self):
        chessBoard = Chessboard()
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "P", BoardPosition(0, 1)).to_FEN(), "P")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "p", BoardPosition(0, 1)).to_FEN(), "p")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "N", BoardPosition(0, 1)).to_FEN(),  "N")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "K", BoardPosition(0, 1)).to_FEN(), "K")
        self.assertEqual(chessBoard.createPieceFromFENLetter(
            "q", BoardPosition(0, 1)).to_FEN(), "q")
        self.assertEqual(chessBoard.getFEN(),
                         "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(len(chessBoard.getAlivePieces()), 32)
        self.assertEqual(len(chessBoard.getDeadPieces()), 0)

    def test_check(self):
        chessBoard = Chessboard()
        self.assertFalse(chessBoard.getCheck())
        chessBoard.move(BoardPosition(4, 1), BoardPosition(4, 3))
        chessBoard.move(BoardPosition(5, 6), BoardPosition(5, 4))
        chessBoard.move(BoardPosition(3, 0), BoardPosition(7, 4))
        self.assertTrue(chessBoard.getCheck())

    def test_checkmate(self):
        chessBoard = Chessboard()
        self.assertFalse(chessBoard.getCheckmate())
        chessBoard.move(BoardPosition(4, 1), BoardPosition(4, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 0), BoardPosition(7, 4))
        chessBoard.move(BoardPosition(4, 7), BoardPosition(4, 6))
        chessBoard.move(BoardPosition(7, 4), BoardPosition(4, 4))
        piece = chessBoard.getPieceAtPosition(BoardPosition(0, 0))
        self.assertTrue(chessBoard.getCheckmate())

    def testMoveForCheck(self):
        chessBoard = Chessboard()
        chessBoard.move(BoardPosition(4, 1), BoardPosition(4, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 0), BoardPosition(7, 4))
        self.assertFalse(chessBoard.move(BoardPosition(5, 6),
                                         BoardPosition(5, 5)))

    def test_isThreatened(self):
        chessBoard = Chessboard(
            "rn1qkbnr/ppp1pppp/8/3p3b/3PPB2/2NQ4/PPP2PPP/R3KBNR b KQkq e3 0 5")
        self.assertFalse(chessBoard.isThreatened(
            BoardPosition(4, 0), PieceColor.Black))
        self.assertTrue(chessBoard.isThreatened(
            BoardPosition(3, 0), PieceColor.Black))


if __name__ == "__main__":
    unittest.main()
