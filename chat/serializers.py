from rest_framework import serializers
from chat.models import ChatUser, ChatRoom

class ChatUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatUser
        fields = ('username', 'anonymous', 'connected_time',)


class ChatRoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ('name', 'created_time', 'modified_time', 'guests',)
