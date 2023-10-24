import unittest
from chess.classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


class TestPawn(unittest.TestCase):

    def test_pawn(self):
        chessBoard = Chessboard()
        pawn = chessBoard.getPieceAtPosition(BoardPosition(3, 1))

        self.assertEqual(pawn.getType(), "Pawn")
        self.assertEqual(pawn.getColor(), "w")
        self.assertEqual(pawn.getMoves(), [
                         BoardPosition(3, 2), BoardPosition(3, 3)])
        self.assertEqual(pawn.getAttacks(), [])
        chessBoard.move(BoardPosition(3, 1), BoardPosition(3, 3))
        chessBoard.move(BoardPosition(4, 6), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 3), BoardPosition(4, 4))
        chessBoard.move(BoardPosition(3, 6), BoardPosition(3, 4))
        chessBoard.move(BoardPosition(4, 4), BoardPosition(3, 5))
        self.assertEqual(chessBoard.getFEN(
        ), 'rnbqkbnr/ppp2ppp/3P4/8/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 3')
