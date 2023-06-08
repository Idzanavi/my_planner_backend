from rest_framework import serializers
from chat.models import ChatUser

class ChatUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatUser
        fields = ('username', 'anonymous', 'connected_time',)
