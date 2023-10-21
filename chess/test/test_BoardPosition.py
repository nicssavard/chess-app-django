import unittest

from chess.classes.BoardPosition import BoardPosition


class TestBoardPosition(unittest.TestCase):

    def test_board_position(self):
        bPosition = BoardPosition(3, 3)
        self.assertEqual(bPosition.x, 3)
        self.assertEqual(bPosition.y, 3)
        self.assertEqual(bPosition.toChessNotation(), "d4")
        self.assertEqual(bPosition.add(1, 1).toChessNotation(), "e5")
        self.assertEqual(bPosition.add(-1, -1).toChessNotation(), "c3")
        self.assertEqual(bPosition.add(0, 0).toChessNotation(), "d4")
        self.assertEqual(bPosition.add(0, 1).toChessNotation(), "d5")
        self.assertEqual(bPosition.add(1, 0).toChessNotation(), "e4")
        self.assertEqual(bPosition.add(-1, 0).toChessNotation(), "c4")
        self.assertEqual(bPosition.add(0, -1).toChessNotation(), "d3")
        self.assertTrue(BoardPosition(1, 1).isOnBoard())
        self.assertFalse(BoardPosition(8, 8).isOnBoard())
        self.assertFalse(BoardPosition(-1, -1).isOnBoard())


if __name__ == "__main__":
    unittest.main()
