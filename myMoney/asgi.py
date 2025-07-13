"""
ASGI config for myMoney project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import monitoring.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myMoney.settings')
django.setup()  # Ensure Django apps are loaded before importing ASGI app

# HTTP and WebSocket protocol routing
application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter(
			monitoring.routing.websocket_urlpatterns
		)
	),
})
