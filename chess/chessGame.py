from api.models import Chat, Message;
from api.serializers import MessageSerializer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json
from urllib.parse import parse_qs

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
            print(event)
            if event['type'] == 'websocket.connect':
                await send({
                    'type': 'websocket.accept'
                })

            if event['type'] == 'websocket.disconnect':
                break

            if event['type'] == 'websocket.receive':
                # event_data = json.loads(event['text'])
                # chat = await get_chat_by_id(event_data.get('chatId'))
                # sender = await get_user_by_id(event_data.get('senderId'))
                # message = event_data.get('message')
                # newMessage = await create_message(message, sender, chat)
                # serializedNewMessage = MessageSerializer(newMessage).data
                # serializedNewMessage_json = json.dumps(serializedNewMessage)
                for ws in chat_connections.get(chessGameId, []):
                    await ws({
                        'type': 'websocket.send',
                        'text': "welcome to chess"
                    })

                

    finally:
        # Remove the client from the set when it disconnects
        chat_connections[chessGameId].remove(send)