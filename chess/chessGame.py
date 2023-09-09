from api.models import Chat, Message;
from api.serializers import MessageSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json
from urllib.parse import parse_qs
from .classes.ChessBoard import Chessboard
# connected_websockets = set()
chat_connections = {}

@database_sync_to_async
def get_chat_by_id(chat_id):
    return Chat.objects.get(id=chat_id)

@database_sync_to_async
def get_user_by_id(chat_id):
    return User.objects.get(id=chat_id)

@database_sync_to_async
def create_message(message, sender, chat):
    newMessage = Message.objects.create(chat=chat, sender=sender, content=message)
    newMessage.save()
    return newMessage

async def chessGame(scope, receive, send):
    print('websocket_application')
    chessBoard = Chessboard()
    query_string = scope.get('query_string', b'').decode('utf-8')
    query_params = parse_qs(query_string)
    chessGameId = query_params.get('chessGameId', [None])[0]

    if chessGameId is None:
        print("chessGameId not provided")
        return
    
    # Add the new client to the list for this chatId
    if chessGameId not in chat_connections:
        chat_connections[chessGameId] = []
    chat_connections[chessGameId].append(send)
    
    
    try:
        while True:
            event = await receive()
            
            if event['type'] == 'websocket.connect':
                board_data = chessBoard.to_dict()
                serialized_board_data = json.dumps(board_data)
                await send({
                    'type': 'websocket.accept'
                })
                await send({
                    'type': 'websocket.send',
                    'text': serialized_board_data
                })



            if event['type'] == 'websocket.disconnect':
                break

            if event['type'] == 'websocket.receive':
                event_data = json.loads(event['text'])
                print(event_data)
                start = event_data.get('start')
                end = event_data.get('end')
                chessBoard.movePiece(start, end)
                print(chessBoard.to_FEN())
                # print(event.get('text'))
                # print(command['start'])

                # event_data = json.loads(event['text'])
                # print(event_data)
                # chat = await get_chat_by_id(event_data.get('chatId'))
                # sender = await get_user_by_id(event_data.get('senderId'))
                # message = event_data.get('message')
                # newMessage = await create_message(message, sender, chat)
                # serializedNewMessage = MessageSerializer(newMessage).data
                # serializedNewMessage_json = json.dumps(serializedNewMessage)
                board_data = chessBoard.to_dict()
                serialized_board_data = json.dumps(board_data)
                for ws in chat_connections.get(chessGameId, []):
                    await ws({
                        'type': 'websocket.send',
                        'text': serialized_board_data
                    })

                

    finally:
        # Remove the client from the set when it disconnects
        chat_connections[chessGameId].remove(send)