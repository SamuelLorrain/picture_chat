"""
ASGI config for picture_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.urls import websocket_urlpatterns
# TODO channel authentication

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'picture_chat.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':URLRouter(websocket_urlpatterns)
})
