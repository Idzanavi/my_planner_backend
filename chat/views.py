import datetime
import math

from channels.layers import get_channel_layer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from chat.models import ChatUser, ChatRoom
from chat.paginators import ChatUserPagination, ChatRoomPagination
from chat.serializers import ChatUserSerializer, ChatRoomSerializer
from chat.utils import prefix_remover


class ChatUsersView(APIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = ChatUserPagination

    def get(self, request):
        chat_users = ChatUser.objects.all().order_by('username')
        page = self.paginate_queryset(chat_users)
        if page is not None:
            serializer = ChatUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)


class RoomsView(APIView):
    pagination_class = ChatRoomPagination

    def get(self, request):
        chat_rooms = ChatRoom.objects.all().order_by('name')
        page = self.paginate_queryset(chat_rooms)
        if page is not None:
            serializer = ChatRoomSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data)