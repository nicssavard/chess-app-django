from django.contrib.auth.models import User
import json
from urllib.parse import parse_qs
import time
from .classes.ChessBoard import Chessboard
from chess.classes.BoardPosition import BoardPosition


def printStatus():
    print('queue')
    for player in Player.queue:
        print(player.user_id)
    print('games')
    for game in ChessGame.games:
        print(game)
    print('')


async def chessGame(scope, receive, send):
    printStatus()
    event = await receive()
    print(event)
    if event['type'] == 'websocket.connect':
        await send({
            'type': 'websocket.accept'
        })

    query_string = scope.get('query_string', b'').decode('utf-8')
    query_params = parse_qs(query_string)
    chessGameId = query_params.get('chessGameId', [None])[0]
    userId = query_params.get('userId', [None])[0]

    player = Player(send, userId)
    if len(Player.queue) == 0:  # No opponent in queue
        print(f'player {userId} added to queue')
        player.add_to_queue()
        await player.sender({
            'type': 'websocket.send',
            'text': json.dumps({
                'messageType': 'WAITING_FOR_OPPONENT',
                'gameId': player.get_game_id(),
                'userId': player.user_id,
                'games': len(ChessGame.games),
                'queue': len(Player.queue),
            })
        })
    else:
        opponent = player.get_opponent_from_queue()
        game = ChessGame(opponent, player)
        print(
            f'game {game.game_id} started - player {userId} vs player {opponent.user_id}')

        for p in game.get_players():
            await p.sender({
                'type': 'websocket.send',
                'text': json.dumps({
                    'messageType': 'GAME_STARTED',
                    'board': game.board.get_serialized_board(),
                    'color': p.get_color()
                })
            })
    printStatus()
    try:
        while True:
            event = await receive()
            gameId = player.get_game_id()

            if event['type'] == 'websocket.disconnect':
                break

            if event['type'] == 'websocket.receive':
                game = ChessGame.games.get(gameId)
                chessBoard = game.board
                event_data = json.loads(event['text'])
                start = event_data.get('start')
                end = event_data.get('end')
                start = BoardPosition(start['x'], start['y'])
                end = BoardPosition(end['x'], end['y'])
                chessBoard.move(start, end)
                for player in game.get_players():
                    await player.sender({
                        'type': 'websocket.send',
                        'text': game.board.get_serialized_board()
                    })
    finally:
        # Remove the client from the set when it disconnects
        print('disconnected')
        if player in Player.queue:
            player.remove_from_queue()
        print(chessGameId)
        if ChessGame.games.get(gameId) is not None:
            print(f'game {gameId} deleted - player {userId} lost')
            del ChessGame.games[gameId]
        printStatus()


class Player:
    queue = []

    def __init__(self, sender, user_id, game_id=None):
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
