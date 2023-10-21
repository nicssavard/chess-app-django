from .ChessPiece import Pawn, Rook, Knight, Bishop, Queen, King, ChessPosition, ChessPiece
import json
from .BoardPosition import BoardPosition


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
        self.wKing = King(PieceColor.White, ChessPosition(4, 0), self)
        self.bKing = King(PieceColor.Black, ChessPosition(4, 7), self)
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
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
                    self.setPieceAtPosition(
                        ChessPosition(x, 7-i), self.createPieceFromFENLetter(letter, ChessPosition(x, 7 - i)))
                    pieces = pieces.replace(letter, '')
                    x += 1
        # set up dead pieces
        for letter in pieces:
            self.dead_pieces.append(
                self.createPieceFromFENLetter(letter, ChessPosition(-1, -1)))

        # set up game state
        self.turn = fen.split(' ')[1]
        self.enPassant = fen.split(' ')[3]
        self.halfMoves = int(fen.split(' ')[4])
        self.fullMoves = int(fen.split(' ')[5])

        # generate possible moves and attacks
        #
        #
        #

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

        wRook1 = self.getPieceAtPosition(ChessPosition(0, 0))
        wRook2 = self.getPieceAtPosition(ChessPosition(7, 0))
        bRook1 = self.getPieceAtPosition(ChessPosition(0, 7))
        bRook2 = self.getPieceAtPosition(ChessPosition(7, 7))

        castle = ''
        if not self.wKing.hasMoved:
            if wRook1 and not wRook1.hasMoved:
                castle += 'K'
            if wRook2 and not wRook2.hasMoved:
                castle += 'Q'
        if not self.bKing.hasMoved:
            if bRook1 and not bRook1.hasMoved:
                castle += 'k'
            if bRook2 and not bRook2.hasMoved:
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

    def setupPieces(self):
        for i in range(8):
            self.wPawn.append(
                Pawn(PieceColor.White, ChessPosition(i, 1), self))
            self.bPawn.append(
                Pawn(PieceColor.Black, ChessPosition(i, 6), self))

        self.wRook.append(Rook(PieceColor.White, ChessPosition(0, 0), self), Rook(
            PieceColor.White, ChessPosition(7, 0), self))
        self.bRook.append(Rook(PieceColor.Black, ChessPosition(0, 7), self), Rook(
            PieceColor.Black, ChessPosition(7, 7), self))

        self.wKnight.append(Knight(PieceColor.White, ChessPosition(
            1, 0), self), Knight(PieceColor.White, ChessPosition(6, 0), self))
        self.bKnight.append(Knight(PieceColor.Black, ChessPosition(
            1, 7), self), Knight(PieceColor.Black, ChessPosition(6, 7), self))

        self.wBishop.append(Bishop(PieceColor.White, ChessPosition(
            2, 0), self), Bishop(PieceColor.White, ChessPosition(5, 0), self))
        self.bBishop.append(Bishop(PieceColor.Black, ChessPosition(
            2, 7), self), Bishop(PieceColor.Black, ChessPosition(5, 7), self))

        self.wQueen.append(Queen(PieceColor.White, ChessPosition(3, 0), self))
        self.bQueen.append(Queen(PieceColor.Black, ChessPosition(3, 7), self))

        self.wKing.append(King(PieceColor.White, ChessPosition(4, 0), self))
        self.bKing.append(King(PieceColor.Black, ChessPosition(4, 7), self))

        self.alive_pieces.append(self.wPawn)
        self.alive_pieces.append(self.bPawn)
        self.alive_pieces.append(self.wRook)
        self.alive_pieces.append(self.bRook)
        self.alive_pieces.append(self.wKnight)
        self.alive_pieces.append(self.bKnight)
        self.alive_pieces.append(self.wBishop)
        self.alive_pieces.append(self.bBishop)
        self.alive_pieces.append(self.wQueen)
        self.alive_pieces.append(self.bQueen)
        self.alive_pieces.append(self.wKing)
        self.alive_pieces.append(self.bKing)

    def to_FEN(self):
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
        # fen += ' '
        # fen += 'K' if self.wKing[0].hasMoved == False else ''
        # fen += 'Q' if self.wRook[0].hasMoved == False else ''
        # fen += 'k' if self.bKing[0].hasMoved == False else ''
        # fen += 'q' if self.bRook[0].hasMoved == False else ''
        # fen += ' - 0 1'
        return fen

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

    def movePiece(self, start: ChessPosition, end: ChessPosition):
        piece = self.getPieceAtPosition(start)
        if piece is None:
            return False
        if piece.getColor() != self.turn:
            return False
        if not piece.move(end):
            return False
        # test check
        self.makeMove(start, end)
        # test check and checkmate
        return True

    def makeMove(self, start: ChessPosition, end: ChessPosition):
        piece = self.getPieceAtPosition(start)
        # check promotion
        if self.pawnPromotion(piece, end):
            piece = Queen(piece.color, piece.position, self)
        deadPiece = self.getPieceAtPosition(end)
        self.board[start.y][start.x] = None
        self.board[end.y][end.x] = piece
        piece.position = end
        self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
        self.fen = self.to_FEN()

    def pawnPromotion(self, piece: ChessPiece, end: ChessPosition):
        if piece.type != 'Pawn':
            return False
        if piece.color == PieceColor.White and end.y != 7:
            return False
        if piece.color == PieceColor.Black and end.y != 0:
            return False
        return True

    def getPieceAtPosition(self, position: BoardPosition):
        return self.board[position.y][position.x]

    def setPieceAtPosition(self, position: BoardPosition, piece: ChessPiece):
        self.board[position.y][position.x] = piece
        if piece:
            piece.setPositon(position)
