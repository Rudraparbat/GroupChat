"""
ASGI config for chats project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path , re_path
from conn.consumers import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chats.settings')

application = ProtocolTypeRouter({
    # Django's ASGI application to handle traditional HTTP requests
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'^(?P<room_name>[a-zA-Z]+)/(?P<room_id>\d+)/$',Chatapp.as_asgi())
            ])
        )
    ),
})
