from django.urls import re_path
from EmeetingApp import views

from EmeetingApp import consumers


print("in routing")
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/', consumers.ChatConsumer.as_asgi()),
    #re_path(r'ws/chat/testSocket/', consumers.ChatConsumer.as_asgi()),
   # re_path(r'ws/chat/(?P<room_name>\w+)/startgroup',views.startgroup)
    #re_path(r'ws/chat/(?P<room_name>\w+)/startpresentor',consumers.startpresentor)
]