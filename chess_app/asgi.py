"""
ASGI config for chess_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from django.urls import path
from .consumers import websocket_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chess_app.settings')

async def chat(scope, receive, send):
        await websocket_application(scope, receive, send)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter([
        path('chat', chat)
   ]),
})
#application = get_asgi_application()
