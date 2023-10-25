from .ChessPiece import Pawn, Rook, Knight, Bishop, Queen, King, ChessPiece
import json
from .BoardPosition import BoardPosition
import copy


class PieceColor:
    White = "w"
    Black = "b"


class Chessboard:
    defaultFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=defaultFEN):
        self.turn = PieceColor.White
        self.board = []
        self.halfMoves = 0
        self.fullMoves = 1
        self.enPassant = '-'
        self.fen = ''
        self.check = False
        self.checkmate = False
        self.winner = None
        self.alive_pieces = []
        self.dead_pieces = []
        self.moveHistory = []
        self.pieces = 'rnbqkbnrppppppppPPPPPPPPRNBQKBNR'
        self.possibleMoves = []
        self.possibleAttacks = []
        self.whiteAttacks = []
        self.blackAttacks = []
        self.whiteMoves = []
        self.blackMoves = []
        self.wKing = King(PieceColor.White, BoardPosition(4, 0), self)
        self.bKing = King(PieceColor.Black, BoardPosition(4, 7), self)
        for i in range(8):
            self.board.append([None, None, None, None, None, None, None, None])
        self.initializeBoard(fen)
        self.generateFEN()

    def initializeBoard(self, fen):
        pieces = self.pieces
        fenBoard = fen.split(' ')[0]
        fenRows = fenBoard.split('/')
        # set up board
        for i in range(len(fenRows)):
            row = fenRows[i]
            x = 0
            for j in range(len(row)):
                letter = row[j]
                if letter.isdigit():
                    x += int(letter)
                else:
                    piece = self.createPieceFromFENLetter(
                        letter, BoardPosition(x, 7 - i))
                    self.setPieceAtPosition(
                        BoardPosition(x, 7-i), piece)
                    pieces = pieces.replace(letter, '', 1)
                    self.alive_pieces.append(piece)
                    x += 1
        # set up dead pieces
        for letter in pieces:
            self.dead_pieces.append(
                self.createPieceFromFENLetter(letter, BoardPosition(-1, -1)))

        # set up game state
        self.turn = fen.split(' ')[1]
        self.enPassant = fen.split(' ')[3]
        self.halfMoves = int(fen.split(' ')[4])
        self.fullMoves = int(fen.split(' ')[5])

        # generate possible moves and attacks
        self.generatePossibleMovesAndAttacks()

    def move(self, start: BoardPosition, end: BoardPosition, pawnPromotionPiece: ChessPiece = ''):
        piece = self.getPieceAtPosition(start)
        if piece is None:
            return False
        if piece.getColor() != self.turn:
            return False
        if piece.isInMoves(end):
            moveType = 'move'
        elif piece.isInAttacks(end):
            moveType = 'attack'
        else:
            return False

        # test move for check
        if not self.testMoveForCheck(start, end, moveType):
            return False
        # test check
        if moveType == 'move':
            piece.move(end)
        elif moveType == 'attack':
            piece.attack(end)

        # test check and checkmate

        self.updateState(start, end, piece, moveType)
        self.generatePossibleMovesAndAttacks()
        # self.check = self.isCheck(self.turn)
        self.check = self.isCheck(self.turn)
        if self.check:
            if self.isCheckmate(self.turn):
                self.checkmate = True
                self.winner = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
        self.generateFEN()
        return True

    def movePiece(self, piece: ChessPiece, end: BoardPosition):
        start = piece.getPosition()
        self.setPieceAtPosition(end, piece)
        self.setPieceAtPosition(start, None)
        return True

    def makeMove(self, start: BoardPosition, end: BoardPosition):
        piece = self.getPieceAtPosition(start)
        # check promotion
        if self.pawnPromotion(piece, end):
            piece = Queen(piece.color, piece.position, self)
        deadPiece = self.getPieceAtPosition(end)
        self.board[start.y][start.x] = None
        self.board[end.y][end.x] = piece
        piece.position = end
        self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
        self.fen = self.generateFEN()

    def killPiece(self, location: BoardPosition):
        piece = self.getPieceAtPosition(location)
        if piece:
            self.board[location.y][location.x] = None
            self.dead_pieces.append(piece)
            self.alive_pieces.remove(piece)

    def generatePossibleMovesAndAttacks(self):
        self.possibleMoves = []
        self.possibleAttacks = []
        self.whiteAttacks = []
        self.blackAttacks = []
        self.whiteMoves = []
        self.blackMoves = []
        for piece in self.getAlivePieces(PieceColor.White):
            piece.generateMoves()
            self.whiteMoves += piece.getMoves()
            self.whiteAttacks += piece.getAttacks()
        for piece in self.getAlivePieces(PieceColor.Black):
            piece.generateMoves()
            self.blackMoves += piece.getMoves()
            self.blackAttacks += piece.getAttacks()
        self.possibleMoves = self.whiteMoves + self.blackMoves
        self.possibleAttacks = self.whiteAttacks + self.blackAttacks

    def getPossibleMoves(self, color=None):
        if color is None:
            return self.possibleMoves
        if color == PieceColor.White:
            return self.whiteMoves
        return self.blackMoves

    def getPossibleAttacks(self, color=None):
        if color is None:
            return self.possibleAttacks
        if color == PieceColor.White:
            return self.whiteAttacks
        return self.blackAttacks

    def getAlivePieces(self, color=None):
        if color is None:
            return self.alive_pieces
        return filter(lambda piece: piece.getColor() == color, self.alive_pieces)

    def pawnPromotion(self, piece: ChessPiece, end: BoardPosition):
        pass

    def testMoveForCheck(self, start: BoardPosition, end: BoardPosition, moveType: str):
        chessBoardCopy = copy.deepcopy(self)
        piece = chessBoardCopy.getPieceAtPosition(start)
        if moveType == 'move':
            piece.move(end)
        elif moveType == 'attack':
            piece.attack(end)
        chessBoardCopy.generatePossibleMovesAndAttacks()
        if chessBoardCopy.isCheck(self.turn):
            return False
        return True

    def isCheck(self, color: PieceColor):
        king = self.wKing if color == PieceColor.White else self.bKing
        return king.getPosition() in self.getPossibleAttacks(PieceColor.White if color == PieceColor.Black else PieceColor.Black)

    def isCheckmate(self, color: PieceColor):
        isCheckmate = True
        for piece in self.getAlivePieces(color):
            for move in piece.getMoves():
                if self.testMoveForCheck(piece.getPosition(), move, 'move'):
                    isCheckmate = False
                    break
            for attack in piece.getAttacks():
                if self.testMoveForCheck(piece.getPosition(), attack, 'attack'):
                    isCheckmate = False
                    break
        return isCheckmate

    def isThreatened(self, position: BoardPosition, color: PieceColor):
        isThreatened = position in self.getPossibleAttacks(
            color) or position in self.getPossibleMoves(color)
        return isThreatened

    def getPieceAtPosition(self, position: BoardPosition):
        if position.x < 0 or position.x > 7 or position.y < 0 or position.y > 7:
            return -1
        try:
            return self.board[position.y][position.x]
        except:
            return None

    def setPieceAtPosition(self, position: BoardPosition, piece: ChessPiece):
        self.board[position.y][position.x] = piece
        if piece:
            piece.setPositon(position)

    def getDeadPieces(self):
        return self.dead_pieces

    def getCheck(self):
        return self.check

    def getCheckmate(self):
        return self.checkmate

    def getWinner(self):
        return self.winner

    def changeTurn(self):
        self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White

    def updateState(self, start: BoardPosition, end: BoardPosition, piece: ChessPiece, moveType: str):
        dir = 1 if piece.color == PieceColor.White else -1
        self.halfMoves += 1
        if self.turn == PieceColor.Black:
            self.fullMoves += 1
        self.changeTurn()
        self.enPassant = '-'
        if moveType == 'attack':
            self.halfMoves = 0
        elif piece.getType() == 'Pawn':
            self.halfMoves = 0
            if (end.y == start.y + dir * 2):
                self.enPassant = start.add(0, dir).toChessNotation()

    def generateFEN(self):
        fen = ''
        for i in range(8):
            empty = 0
            for j in range(8):
                if self.board[7-i][j] is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += self.board[7-i][j].to_FEN()
            if empty > 0:
                fen += str(empty)
            if i < 7:
                fen += '/'
        fen += ' ' + self.turn[0].lower()
        fen += ' '

        wRook1 = self.getPieceAtPosition(BoardPosition(0, 0))
        wRook2 = self.getPieceAtPosition(BoardPosition(7, 0))
        bRook1 = self.getPieceAtPosition(BoardPosition(0, 7))
        bRook2 = self.getPieceAtPosition(BoardPosition(7, 7))

        castle = ''
        if not self.wKing.hasMoved:
            if wRook2 and not wRook2.hasMoved:
                castle += 'K'
            if wRook1 and not wRook1.hasMoved:
                castle += 'Q'
        if not self.bKing.hasMoved:
            if bRook2 and not bRook2.hasMoved:
                castle += 'k'
            if bRook1 and not bRook1.hasMoved:
                castle += 'q'
        if castle == '':
            castle = '-'
        fen += f'{castle} {self.enPassant} {self.halfMoves} {self.fullMoves}'
        self.fen = fen
        return fen

    def getFEN(self):
        return self.fen

    def createPieceFromFENLetter(self, letter, position):
        color = PieceColor.White if letter.isupper() else PieceColor.Black
        letter = letter.lower()
        if letter == 'p':
            return Pawn(color, position, self)
        elif letter == 'r':
            return Rook(color, position, self)
        elif letter == 'n':
            return Knight(color, position, self)
        elif letter == 'b':
            return Bishop(color, position, self)
        elif letter == 'q':
            return Queen(color, position, self)
        elif letter == 'k':
            if color == PieceColor.White:
                self.wKing = King(color, position, self)
                return self.wKing
            else:
                self.bKing = King(color, position, self)
                return self.bKing
        else:
            return None

    def to_dict(self):
        return {
            'turn': self.turn,
            'fen': self.fen,  # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
            'check': self.check,
            'checkmate': self.checkmate,
            'winner': self.winner,
            'dead_pieces': [piece.to_FEN() for piece in self.alive_pieces],
            # 'alive_pieces': [[piece.to_dict() for piece in piece_list] for piece_list in self.alive_pieces],
            # Add other attributes as needed
        }

    def get_serialized_board(self):
        return json.dumps(self.to_dict())
