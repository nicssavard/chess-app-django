
class BoardPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isOnBoard(self):
        return self.x >= 0 and self.x <= 7 and self.y >= 0 and self.y <= 7

    def toChessNotation(self):
        return chr(self.x + 97) + str(self.y + 1)

    def add(self, x, y):
        return BoardPosition(self.x + x, self.y + y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"BoardPosition({self.x}, {self.y})"

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __repr__(self):
        return f"BoardPosition({self.x}, {self.y})"
