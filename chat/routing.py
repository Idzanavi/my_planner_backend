from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),
]