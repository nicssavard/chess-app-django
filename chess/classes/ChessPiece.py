class PieceColor:
    White = "white"
    Black = "black"

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
        if self.isLinear(start, end):
            return self.lineClear(start, end)
        elif self.isDiagonal(start, end):
            return self.diagonalClear(start, end)
        return False


    def isLinear(start: ChessPosition, end: ChessPosition):
        return start.x == end.x or start.y == end.y
    
    def isDiagonal(start: ChessPosition, end: ChessPosition):
        return abs(start.x - end.x) == abs(start.y - end.y)
    
    def lineClear(self, start: ChessPosition, end: ChessPosition):
        direction = self.moveDirection(start, end)
        for i in range(1, max(abs(start.x - end.x), abs(start.y - end.y))):
            if self.board.getPieceAtPosition(ChessPosition(start.x + i * direction["x"], start.y + i * direction["y"])) is not None:
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


class Rook(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Rook")


class Knight(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Knight")


class Bishop(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Bishop")


class Queen(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Queen")


class King(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "King")


