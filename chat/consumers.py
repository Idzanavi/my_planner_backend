import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import ChatUser
from datetime import datetime

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.room_group_name = 'room_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        anonymous = self.scope['user'].username == ""
        username = "Anonymous - %s:%d" % (self.scope['client'][0], self.scope['client'][1]) \
            if anonymous else self.scope['user'].username
        ChatUser.objects.create(username=username, anonymous=anonymous)
        self.username = username
        self.anonymous = anonymous
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        ChatUser.objects.filter(username=self.username).delete()

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        nickname = data['nickname']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname,
                'user': self.username,
                'anonymous': self.anonymous,
                'time': datetime.now()
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = event['user']
        anonymous = event['anonymous']
        nickname = event['nickname']
        time = event["time"].strftime("%Y-%m-%d, %H:%M:%S")

        self.send(text_data=json.dumps({
            'type': 'message',
            'message': message,
            'user': user,
            'nickname': nickname,
            'time': time,
            'anonymous': anonymous,
        }))

    def log_event(self, event):
        user = event['user']
        week = event['week']
        day = event['day']
        slot = event['slot']
        action = event['action']
        title = event['title']
        time = event["time"].strftime("%Y-%m-%d, %H:%M:%S")

        self.send(text_data=json.dumps({
            'type': 'event',
            'title': title,
            'action': action,
            'week': week,
            'day': day,
            'slot': slot,
            'user': user,
            'time': time
        }))
