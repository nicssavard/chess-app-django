from api.models import Chat, Message;
from api.serializers import MessageSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json
from urllib.parse import parse_qs
import time
from .classes.ChessBoard import ChessPosition
from .classes.ChessBoard import Chessboard
# connected_websockets = set()
chat_connections = {}
chess_boards = {}
queue = []
friend_waiting = {} #used when a user is waiting for a friend to join their game


class Player:
    queue = []


    def __init__(self, sender, user_id, game_id= None):
        self.sender = sender
        self.color = None
        self.user_id = user_id
        self.game_id = game_id

    def set_game_id(self, game_id):
        self.game_id = game_id

    def get_game_id(self):
        return self.game_id
    
    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color
    
    def add_to_queue(self):
        chessGameId = str(time.time())
        self.set_game_id(chessGameId)
        Player.queue.append(self)

    def remove_from_queue(self):
        self.queue.remove(self)

    def get_opponent_from_queue(self):
        return self.queue.pop(0)
    
    def start_game(self, opponent):
        game = ChessGame(self.game_id, self, opponent)
        return game

    def remove_from_games(self):
        del self.games[self.game_id]

    def get_color(self):
        return self.color
    
class ChessGame:
    games = {}
    def __init__(self, player1, player2):
        self.game_id = player1.get_game_id()
        player2.set_game_id(self.game_id)
        player1.set_color('w')
        player2.set_color('b')
        self.player1 = player1
        self.player2 = player2
        self.board = Chessboard()
        self.games[self.game_id] = self

    def get_players(self):
        return (self.player1, self.player2)


async def chessGame(scope, receive, send):
    
    event = await receive()

    if event['type'] == 'websocket.connect':
        await send({
            'type': 'websocket.accept'
        })

    query_string = scope.get('query_string', b'').decode('utf-8')
    query_params = parse_qs(query_string)
    chessGameId = query_params.get('chessGameId', [None])[0]
    userId = query_params.get('userId', [None])[0]
    
    
    if chessGameId is None:   #No game id, random opponent game
        player = Player(send, userId)
        if len(Player.queue) == 0:  #No opponent in queue
            player.add_to_queue()
        else:
            opponent = player.get_opponent_from_queue()            
            game = ChessGame(opponent, player)

            for player in game.get_players():
                await player.sender({
                    'type': 'websocket.send',
                    'text': game.board.get_serialized_board()
                })     
    else:  #Game id, provided 
        player = Player(send, userId, chessGameId)
        if chessGameId not in friend_waiting:
            print ('no opponent')
            friend_waiting[chessGameId] = player   
        else:
            print('opponent connected')
            opponent = friend_waiting[chessGameId]
            game = ChessGame(opponent, player)
            del friend_waiting[chessGameId]

            for player in game.get_players():
                await player.sender({
                    'type': 'websocket.send',
                    'text': game.board.get_serialized_board()
                })     
    print(Player.queue)
    print(friend_waiting)
    print('games: ', ChessGame.games)
    
    try:
        while True:
            print('receiving', player.get_game_id())
            print(player.user_id)            
            print(ChessGame.games)
            event = await receive()

            if event['type'] == 'websocket.disconnect':
                break

            if event['type'] == 'websocket.receive':
                chessBoard = chess_boards[chessGameId]
                event_data = json.loads(event['text'])
                start = event_data.get('start')
                start = ChessPosition(start['x'], start['y'])
                end = event_data.get('end')
                end = ChessPosition(end['x'], end['y'])
                chessBoard.movePiece(start, end)
                board_data = chessBoard.to_dict()
                serialized_board_data = json.dumps(board_data)
                for ws in chat_connections.get(chessGameId, []):
                    await ws({
                        'type': 'websocket.send',
                        'text': serialized_board_data
                    })

                

    finally:
        # Remove the client from the set when it disconnects
        print('disconnected')
        if (send, chessGameId) in queue:
            queue.remove((send, chessGameId))
        print(queue)
        chat_connections[chessGameId].remove(send)
        if len(chat_connections[chessGameId]) == 0:
            del chat_connections[chessGameId]
            del chess_boards[chessGameId]