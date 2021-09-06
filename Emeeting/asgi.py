"""
ASGI config for Emeeting project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
#
# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Emeeting.settings')
#
# application = get_asgi_application()

import os

import channels.routing
import django.core.asgi
import channels.auth
import EmeetingApp.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":AuthMiddlewareStack(

        URLRouter(
            EmeetingApp.routing.websocket_urlpatterns
        )
    ),
    # Just HTTP for now. (We can add other protocols later.)
})