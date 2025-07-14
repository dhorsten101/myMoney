"""
ASGI config for myMoney project.
"""

import os

import django
import routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myMoney.settings')
django.setup()  # Setup Django before loading ASGI application

# # Define the actual application router
# asgi_app = ProtocolTypeRouter({
# 	"http": get_asgi_application(),
# 	"websocket": AuthMiddlewareStack(
# 		URLRouter(
# 			monitoring.routing.websocket_urlpatterns
# 		)
# 	),
# })

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter(routing.websocket_urlpatterns)
	),
})


# Wrap the router with debug middleware
class DebugMiddleware:
	def __init__(self, app):
		self.app = app
	
	async def __call__(self, scope, receive, send):
		print("🔍 Scope type:", scope["type"])
		await self.app(scope, receive, send)
