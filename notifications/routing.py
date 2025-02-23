from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notification/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/chatroom/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    
    # path('ws/notification', )
]