from .ChessPiece import Pawn, Rook, Knight, Bishop, Queen, King, ChessPosition, ChessPiece

class PieceColor:
    White = "white"
    Black = "black"


class Chessboard:
    def __init__(self):
        self.turn = PieceColor.White
        self.board = []
        self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w'
        self.check = False
        self.checkmate = False
        self.winner = None
        self.alive_pieces = []
        self.dead_pieces = []
        self.moveHistory = []
        self.wPawn1 = Pawn(PieceColor.White, ChessPosition(0,1), self)
        self.wPawn2 = Pawn(PieceColor.White, ChessPosition(1,1), self)
        self.wPawn3 = Pawn(PieceColor.White, ChessPosition(2,1), self)
        self.wPawn4 = Pawn(PieceColor.White, ChessPosition(3,1), self)
        self.wPawn5 = Pawn(PieceColor.White, ChessPosition(4,1), self)
        self.wPawn6 = Pawn(PieceColor.White, ChessPosition(5,1), self)
        self.wPawn7 = Pawn(PieceColor.White, ChessPosition(6,1), self)
        self.wPawn8 = Pawn(PieceColor.White, ChessPosition(7,1), self)
        self.bPawn1 = Pawn(PieceColor.Black, ChessPosition(0,6), self)
        self.bPawn2 = Pawn(PieceColor.Black, ChessPosition(1,6), self)
        self.bPawn3 = Pawn(PieceColor.Black, ChessPosition(2,6), self)
        self.bPawn4 = Pawn(PieceColor.Black, ChessPosition(3,6), self)
        self.bPawn5 = Pawn(PieceColor.Black, ChessPosition(4,6), self)
        self.bPawn6 = Pawn(PieceColor.Black, ChessPosition(5,6), self)
        self.bPawn7 = Pawn(PieceColor.Black, ChessPosition(6,6), self)
        self.bPawn8 = Pawn(PieceColor.Black, ChessPosition(7,6), self)
        self.wRook1 = Rook(PieceColor.White, ChessPosition(0,0), self)
        self.wRook2 = Rook(PieceColor.White, ChessPosition(7,0), self)
        self.bRook1 = Rook(PieceColor.Black, ChessPosition(0,7), self)
        self.bRook2 = Rook(PieceColor.Black, ChessPosition(7,7), self)
        self.wKnight1 = Knight(PieceColor.White, ChessPosition(1,0), self)
        self.wKnight2 = Knight(PieceColor.White, ChessPosition(6,0), self)
        self.bKnight1 = Knight(PieceColor.Black, ChessPosition(1,7), self)
        self.bKnight2 = Knight(PieceColor.Black, ChessPosition(6,7), self)
        self.wBishop1 = Bishop(PieceColor.White, ChessPosition(2,0), self)
        self.wBishop2 = Bishop(PieceColor.White, ChessPosition(5,0), self)
        self.bBishop1 = Bishop(PieceColor.Black, ChessPosition(2,7), self)
        self.bBishop2 = Bishop(PieceColor.Black, ChessPosition(5,7), self)
        self.wQueen = Queen(PieceColor.White, ChessPosition(3,0), self)
        self.bQueen = Queen(PieceColor.Black, ChessPosition(3,7), self)
        self.wKing = King(PieceColor.White, ChessPosition(4,0), self)
        self.bKing = King(PieceColor.Black, ChessPosition(4,7), self)
        self.board.append([self.wRook1, self.wKnight1, self.wBishop1, self.wQueen, self.wKing, self.wBishop2, self.wKnight2, self.wRook2])
        self.board.append([self.wPawn1, self.wPawn2, self.wPawn3, self.wPawn4, self.wPawn5, self.wPawn6, self.wPawn7, self.wPawn8])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([None, None, None, None, None, None, None, None])
        self.board.append([self.bPawn1, self.bPawn2, self.bPawn3, self.bPawn4, self.bPawn5, self.bPawn6, self.bPawn7, self.bPawn8])
        self.board.append([self.bRook1, self.bKnight1, self.bBishop1, self.bQueen, self.bKing, self.bBishop2, self.bKnight2, self.bRook2])

        self.wPawn = []
        self.bPawn = []
        self.wRook = []
        self.bRook = []
        self.wKnight = []
        self.bKnight = []
        self.wBishop = []
        self.bBishop = []
        self.wQueen = []
        self.bQueen = []
        self.wKing = []
        self.bKing = []
        #self.setupPieces()

    def setupPieces(self):
        for i in range(8):
            self.wPawn.append(Pawn(PieceColor.White, ChessPosition(i,1), self))
            self.bPawn.append(Pawn(PieceColor.Black, ChessPosition(i,6), self))
        
        self.wRook.append(Rook(PieceColor.White, ChessPosition(0,0), self), Rook(PieceColor.White, ChessPosition(7,0), self))
        self.bRook.append(Rook(PieceColor.Black, ChessPosition(0,7), self), Rook(PieceColor.Black, ChessPosition(7,7), self))

        self.wKnight.append(Knight(PieceColor.White, ChessPosition(1,0), self), Knight(PieceColor.White, ChessPosition(6,0), self))
        self.bKnight.append(Knight(PieceColor.Black, ChessPosition(1,7), self), Knight(PieceColor.Black, ChessPosition(6,7), self))

        self.wBishop.append(Bishop(PieceColor.White, ChessPosition(2,0), self), Bishop(PieceColor.White, ChessPosition(5,0), self))
        self.bBishop.append(Bishop(PieceColor.Black, ChessPosition(2,7), self), Bishop(PieceColor.Black, ChessPosition(5,7), self))

        self.wQueen.append(Queen(PieceColor.White, ChessPosition(3,0), self))
        self.bQueen.append(Queen(PieceColor.Black, ChessPosition(3,7), self))

        self.wKing.append(King(PieceColor.White, ChessPosition(4,0), self))
        self.bKing.append(King(PieceColor.Black, ChessPosition(4,7), self))

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
            # 'board': [
            #     [
            #         piece.to_dict() if piece else {'type': 'empty'} for piece in row
            #     ] for row in self.board
            # ],
            'fen': self.fen, # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w
            'check': self.check,
            'checkmate': self.checkmate,
            'winner': self.winner,
            'alive_pieces': [[piece.to_dict() for piece in piece_list] for piece_list in self.alive_pieces],
            # Add other attributes as needed
        }
    def movePiece(self, start: ChessPosition, end: ChessPosition):
        print("movePiece")
        self.makeMove(start, end)

    def makeMove(self, start: ChessPosition, end: ChessPosition):
        piece = self.getPieceAtPosition(start)
        print(piece)
        self.board[start['y']][start['x']] = None
        self.board[end['y']][end['x']] = piece
        piece.position = end
        self.turn = PieceColor.Black if self.turn == PieceColor.White else PieceColor.White
        self.fen = self.to_FEN()



    def getPieceAtPosition(self, position: ChessPosition):
        return self.board[position['y']][position['x']]
