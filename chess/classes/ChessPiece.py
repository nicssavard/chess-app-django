class PieceColor:
    White = "w"
    Black = "b"

class ChessPosition:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class ChessPiece:
    def __init__(self, color, position, board, type):
        self.color = color
        self.position = position
        self.board = board
        self.type = type
    
    def __str__(self):
        return self.color + " " + self.type

    def to_dict(self):
        return {
            'color': self.color,
            'position': {'x': self.position.x, 'y': self.position.y},
            'type': self.type
        }
    
    def to_FEN(self):
        match self.type:
            case "Pawn":
                return "P" if self.color == PieceColor.White else "p"
            case "Rook":
                return "R" if self.color == PieceColor.White else "r"
            case "Knight":
                return "N" if self.color == PieceColor.White else "n"
            case "Bishop":
                return "B" if self.color == PieceColor.White else "b"
            case "Queen":
                return "Q" if self.color == PieceColor.White else "q"
            case "King":
                return "K" if self.color == PieceColor.White else "k"
            case _:
                return " "
            
        
    def getColor(self):
        return self.color
    
    def getPosition(self):
        return self.position
    
    def getBoard(self):
        return self.board
    
    def getType(self):
        return self.type

    def moveDirection(self, start: ChessPosition, end: ChessPosition) -> dict:
        return {
            "x": 1 if end.x > start.x else (-1 if end.x < start.x else 0),
            "y": 1 if end.y > start.y else (-1 if end.y < start.y else 0)
        }

    def move(self, end: ChessPosition):
        if not self.basicMoveChecks(end):
            return False
        return self.canMoveTo(end)
    
    def canMoveTo(self, end: ChessPosition):
        return True
    
    def basicMoveChecks(self, end: ChessPosition):
        if self.position.x == end.x and self.position.y == end.y:
            return False
        target = self.board.getPieceAtPosition(end)
        if target is not None and target.getColor() == self.color:
            return False
        return True
    
    def isPathClear(self, start: ChessPosition, end: ChessPosition):
        if self.isLinear(end):
            return self.lineClear(end)
        elif self.isDiagonal(start, end):
            return self.diagonalClear(start, end)
        return False


    def isLinear(self, end: ChessPosition):
        return self.getPosition().x == end.x or self.getPosition().y == end.y
    
    def isDiagonal(self, start: ChessPosition, end: ChessPosition):
        return abs(start.x - end.x) == abs(start.y - end.y)
    
    def lineClear(self, end: ChessPosition):
        direction = self.moveDirection(self.getPosition(), end)
        for i in range(1, max(abs(self.getPosition().x - end.x), abs(self.getPosition().y - end.y))):
            if self.board.getPieceAtPosition(ChessPosition(self.getPosition().x + i * direction["x"], self.getPosition().y + i * direction["y"])) is not None:
                return False
        return True
    
    def diagonalClear(self, start: ChessPosition, end: ChessPosition):
        direction = self.moveDirection(start, end)
        for i in range(1, abs(start.x - end.x)):
            if self.board.getPieceAtPosition(ChessPosition(start.x + i * direction["x"], start.y + i * direction["y"])) is not None:
                return False
        return True
    
    def setPositon(self, position: ChessPosition):
        self.position = position

class Pawn(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Pawn")

    def canMoveTo(self, end: ChessPosition):
        if self.getBoard().getPieceAtPosition(end) is not None:
            return self.canAttack(end)
        else:
            return self.isMovingStraight(end)
    
    def isMovingStraight(self, end: ChessPosition):
        if self.getPosition().x != end.x:
            return False
        if self.getColor() == PieceColor.White:
            if self.getPosition().y == 1 and end.y == 3:
                if not self.lineClear(end):
                    return False
            elif end.y != self.getPosition().y + 1:
                return False
        elif self.getColor() == PieceColor.Black:
            if self.getPosition().y == 6 and end.y == 4:
                if not self.lineClear(end):
                    return False
            elif end.y != self.getPosition().y - 1:
                return False
        return True
        
    def canAttack(self, end: ChessPosition):
        if abs(self.getPosition().x - end.x) != 1:
            return False
        if self.getColor() == PieceColor.White:
            if end.y != self.getPosition().y + 1:
                return False
        elif self.getColor() == PieceColor.Black:
            if end.y != self.getPosition().y - 1:
                return False
        return True


class Rook(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Rook")

    def canMoveTo(self,  end: ChessPosition):
        return self.isLinear(end) and self.isPathClear(self.getPosition(), end)

class Knight(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Knight")

    def canMoveTo(self, end: ChessPosition):
        if self.getPosition().x == end.x and self.getPosition().y == end.y:
            return False
        if abs(self.getPosition().x - end.x) == 2 and abs(self.getPosition().y - end.y) == 1:
            return True
        if abs(self.getPosition().x - end.x) == 1 and abs(self.getPosition().y - end.y) == 2:
            return True
        return False

class Bishop(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Bishop")

    def canMoveTo(self, end: ChessPosition):
        return self.isDiagonal(self.getPosition(), end) and self.isPathClear(self.getPosition(), end)

class Queen(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Queen")

    def canMoveTo(self, end: ChessPosition):
        return (self.isLinear(end) or self.isDiagonal(self.getPosition(), end)) and self.isPathClear(self.getPosition(), end)

class King(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "King")

    def canMoveTo(self, end: ChessPosition):
        if abs(self.getPosition().x - end.x) <= 1 and abs(self.getPosition().y - end.y) <= 1:
            return True
        return False

