from .BoardPosition import BoardPosition


class PieceColor:
    White = "w"
    Black = "b"


class ChessPiece:
    value = 0

    def __init__(self, color, position, board, type):
        self.color = color
        self.position = position
        self.board = board
        self.type = type
        self.hasMoved = False
        self.possibleMoves = []
        self.possibleAttacks = []

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

    def moveDirection(self, start: BoardPosition, end: BoardPosition) -> dict:
        return {
            "x": 1 if end.x > start.x else (-1 if end.x < start.x else 0),
            "y": 1 if end.y > start.y else (-1 if end.y < start.y else 0)
        }

    def generateMoves(self):
        pass

    def generateMovesLine(self, directions: list, lenght: int = 8):
        for dir in directions:
            d = 1
            while d <= lenght:
                pos = self.getPosition().add(d * dir.x, d * dir.y)
                endSquare = self.getBoard().getPieceAtPosition(pos)
                if endSquare == -1:
                    break
                if endSquare is None:
                    self.addMove(pos)
                elif endSquare.getColor() != self.getColor():
                    self.addAttack(pos)
                    break
                elif endSquare.getColor() == self.getColor():
                    break
                d += 1

    def move(self, end: BoardPosition):
        self.hasMoved = True
        self.getBoard().movePiece(self, end)

    def attack(self, end: BoardPosition):
        self.hasMoved = True
        self.getBoard().killPiece(end)
        self.getBoard().movePiece(self, end)

    def canMoveTo(self, end: BoardPosition):
        return True

    def basicMoveChecks(self, end: BoardPosition):
        if self.position.x == end.x and self.position.y == end.y:
            return False
        target = self.board.getPieceAtPosition(end)
        if target is not None and target.getColor() == self.color:
            return False
        return True

    def isPathClear(self, start: BoardPosition, end: BoardPosition):
        if self.isLinear(end):
            return self.lineClear(end)
        elif self.isDiagonal(start, end):
            return self.diagonalClear(start, end)
        return False

    def isLinear(self, end: BoardPosition):
        return self.getPosition().x == end.x or self.getPosition().y == end.y

    def isDiagonal(self, start: BoardPosition, end: BoardPosition):
        return abs(start.x - end.x) == abs(start.y - end.y)

    def lineClear(self, start: BoardPosition, end: BoardPosition):
        dir = self.moveDirection(start, end)
        lenght = abs(start.x - end.x)
        for i in range(1, lenght):
            if self.board.getPieceAtPosition(BoardPosition(start.x + i * dir["x"], start.y + i * dir["y"])) is not None:
                return False
        return True

    def lineNotThreatened(self, start: BoardPosition, end: BoardPosition):
        dir = self.moveDirection(start, end)
        lenght = abs(start.x - end.x)
        for i in range(1, lenght):
            if self.board.isThreatened(BoardPosition(start.x + i * dir["x"], start.y + i * dir["y"]), PieceColor.Black if self.getColor() == PieceColor.White else PieceColor.White):
                return False
        return True

    def diagonalClear(self, start: BoardPosition, end: BoardPosition):
        direction = self.moveDirection(start, end)
        for i in range(1, abs(start.x - end.x)):
            if self.board.getPieceAtPosition(BoardPosition(start.x + i * direction["x"], start.y + i * direction["y"])) is not None:
                return False
        return True

    def setPositon(self, position: BoardPosition):
        self.position = position

    def getMoves(self):
        return self.possibleMoves

    def getAttacks(self):
        return self.possibleAttacks

    def addMove(self, move: BoardPosition):
        self.possibleMoves.append(move)

    def addAttack(self, attack: BoardPosition):
        self.possibleAttacks.append(attack)

    def clearMoves(self):
        self.possibleMoves = []
        self.possibleAttacks = []

    def isInMoves(self, position: BoardPosition):
        return position in self.possibleMoves

    def isInAttacks(self, position: BoardPosition):
        return position in self.possibleAttacks

    def __str__(self):
        return self.color + " " + self.type + " " + str(self.position)

    def __repr__(self):
        return self.color + " " + self.type + " " + str(self.getPosition().x) + " " + str(self.getPosition().y)


class Pawn(ChessPiece):
    value = 1

    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Pawn")

    def attack(self, end: BoardPosition):
        if self.getBoard().enPassant == end.toChessNotation():
            self.getBoard().killPiece(end.add(0, -1 if self.getColor() == PieceColor.White else 1))
            self.getBoard().movePiece(self, end)
        else:
            super().attack(end)

    def generateMoves(self):
        self.clearMoves()
        p = self.getPosition()
        dir = 1 if self.getColor() == PieceColor.White else -1
        self.canMoveTo(p.add(0, dir))
        self.canMoveTo(p.add(0, dir * 2))
        self.canAttack(p.add(1, dir))
        self.canAttack(p.add(-1, dir))

    def canMoveTo(self, end: BoardPosition):
        if (not end.isOnBoard()):
            return False
        if (self.canMoveStraight(end)):
            self.addMove(end)
            return True
        return False

    def canMoveStraight(self, end: BoardPosition):
        if self.getPosition().x != end.x:
            return False
        if self.getColor() == PieceColor.White:
            if self.getPosition().y == 1 and end.y == 3:
                if not self.lineClear(self.getPosition(), end):
                    return False
            elif end.y != self.getPosition().y + 1:
                return False
        elif self.getColor() == PieceColor.Black:
            if self.getPosition().y == 6 and end.y == 4:
                if not self.lineClear(self.getPosition(), end):
                    return False
            elif end.y != self.getPosition().y - 1:
                return False
        return True

    def canAttack(self, end: BoardPosition):
        if (not end.isOnBoard()):
            return False
        pieceAttacked = self.getBoard().getPieceAtPosition(end)
        if pieceAttacked and pieceAttacked.getColor() != self.getColor():
            self.addAttack(end)
            return True
        if self.getBoard().turn == self.getColor():
            if self.getBoard().enPassant == end.toChessNotation():
                self.addAttack(end)
                return True
        return False


class Rook(ChessPiece):
    value = 5

    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Rook")

    def generateMoves(self):
        self.clearMoves()
        directions = [
            BoardPosition(1, 0),
            BoardPosition(-1, 0),
            BoardPosition(0, 1),
            BoardPosition(0, -1)
        ]
        self.generateMovesLine(directions)

    def canMoveTo(self,  end: BoardPosition):
        return self.isLinear(end) and self.isPathClear(self.getPosition(), end)


class Knight(ChessPiece):
    value = 3

    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Knight")

    def generateMoves(self):
        self.clearMoves()
        p = self.getPosition()
        self.canMoveTo(p.add(1, 2))
        self.canMoveTo(p.add(2, 1))
        self.canMoveTo(p.add(2, -1))
        self.canMoveTo(p.add(1, -2))
        self.canMoveTo(p.add(-1, -2))
        self.canMoveTo(p.add(-2, -1))
        self.canMoveTo(p.add(-2, 1))
        self.canMoveTo(p.add(-1, 2))

    def canMoveTo(self, end: BoardPosition):
        if not end.isOnBoard():
            return False
        if self.getBoard().getPieceAtPosition(end):
            if self.getColor() != self.getBoard().getPieceAtPosition(end).getColor():
                self.addAttack(end)
                return True
            else:
                return False
        else:
            self.addMove(end)
            return True


class Bishop(ChessPiece):
    value = 3

    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Bishop")

    def generateMoves(self):
        self.clearMoves()
        directions = [
            BoardPosition(1, 1),
            BoardPosition(-1, 1),
            BoardPosition(1, -1),
            BoardPosition(-1, -1)
        ]
        self.generateMovesLine(directions)


class Queen(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "Queen")

    def generateMoves(self):
        self.clearMoves()
        directions = [
            BoardPosition(1, 0),
            BoardPosition(-1, 0),
            BoardPosition(0, 1),
            BoardPosition(0, -1),
            BoardPosition(1, 1),
            BoardPosition(-1, 1),
            BoardPosition(1, -1),
            BoardPosition(-1, -1)
        ]
        self.generateMovesLine(directions)


class King(ChessPiece):
    def __init__(self, color, position, board):
        super().__init__(color, position, board, "King")

    def move(self, end: BoardPosition):
        if abs(self.getPosition().x - end.x) == 2:
            if end.x == 2:
                self.getBoard().movePiece(
                    self.getBoard().getPieceAtPosition(BoardPosition(0, self.getPosition().y)), BoardPosition(3, self.getPosition().y))
            elif end.x == 6:
                self.getBoard().movePiece(
                    self.getBoard().getPieceAtPosition(BoardPosition(7, self.getPosition().y)), BoardPosition(5, self.getPosition().y))
        super().move(end)

    def generateMoves(self):
        self.clearMoves()
        directions = [
            BoardPosition(1, 0),
            BoardPosition(-1, 0),
            BoardPosition(0, 1),
            BoardPosition(0, -1),
            BoardPosition(1, 1),
            BoardPosition(-1, 1),
            BoardPosition(1, -1),
            BoardPosition(-1, -1)
        ]
        self.generateMovesLine(directions, 1)
        self.generateCastlingMoves()

    def generateCastlingMoves(self):
        y = 0 if self.getColor() == PieceColor.White else 7
        if not self.hasMoved:
            self.tryCastling(BoardPosition(
                0, y), BoardPosition(2, y), BoardPosition(1, y))
            self.tryCastling(BoardPosition(
                7, y), BoardPosition(6, y), BoardPosition(6, y))

    def tryCastling(self, rookPosition: BoardPosition, castlingPosition: BoardPosition, checkPosition: BoardPosition):
        rook = self.getBoard().getPieceAtPosition(rookPosition)
        if rook and self.isCastlingPossible(checkPosition, rook):
            self.addMove(castlingPosition)

    def isCastlingPossible(self,  checkPosition: BoardPosition, rook):
        return self.lineClear(self.getPosition(), checkPosition) and self.lineNotThreatened(self.getPosition(), checkPosition) and self.lineNotThreatened(self.getPosition(), rook.getPosition())

    def canMoveTo(self, end: BoardPosition):
        return abs(self.getPosition().x - end.x) <= 1 and abs(self.getPosition().y - end.y) <= 1
