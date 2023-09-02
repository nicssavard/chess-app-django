connected_websockets = set()

async def websocket_application(scope, receive, send):
    print('websocket_application')

    # Add the new client to the set
    connected_websockets.add(send)
    print(connected_websockets)

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
                if event['text'] == 'ping':
                    print('pong')

                    # Send 'pong!' to all connected clients
                    for ws in connected_websockets:
                        await ws({
                            'type': 'websocket.send',
                            'text': event['text']
                        })
                    print('pong sent')

    finally:
        # Remove the client from the set when it disconnects
        print('finally')
        connected_websockets.remove(send)